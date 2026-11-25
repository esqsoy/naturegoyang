#!/usr/bin/env python3
"""단원 학습 순서(앱의 `const PATH=[…];` 한 줄)를 만든다. HANDOFF '단원 순서 안'(26.11.25)의 계산.

    python3 -I tools/order.py            # 세 안을 견주어 보이고, 앱의 PATH 줄을 고른 안으로 고쳐 쓴다
    python3 -I tools/order.py --check    # 고쳐 쓸 것이 있으면 1로 끝난다
    python3 -I tools/order.py --show     # 고른 안의 순서를 번호·누적 시간과 함께 보인다

시간 어림(숙달 문제 = 책 답이 있는 쪽 번호만, 짝꿍은 따로): 단원마다 설명·카드·확인 4시간
+ 숙달 문제마다 (책별 분 + 2.5분). 책별 분: 토마스 6, 서웨이 11, 맥머리 7, Epp 10, 캠벨 7, Lang 18.

세 안(모두 선수 단원과 단계 순서는 지킨다):
  기본    단계 → 영역(F P C B E) → 정의 순서. 앱의 옛 순서
  번갈기  같은 단계 안에서 오래 안 한 영역을 먼저
  고른    1단계: 선수가 수학뿐인 과학 단원을 수학 사이에 시간으로 고르게(약 80시간마다) 끼운다.
          2단계부터: 번갈기와 같다.  ← 앱이 쓰는 안(영신 26.11.26 "다 추천대로 합시다")

앱은 PATH가 단원 전부를 한 번씩 담고 선수·단계를 지키면 그 순서로 번호를 매기고, 아니면 기본 순서로 돌아간다.
기록 열쇠는 단원 id라 순서를 바꿔도 기록은 그대로다.
"""
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
APP = os.path.join(REPO, 'app', 'naturegoyang.html')
DK = ['F', 'P', 'C', 'B', 'E']
BOOK_MIN = {'thomas13': 6, 'serway9': 11, 'mcmurry8': 7, 'epp5': 10, 'campbell12': 7, 'lang3': 18}
BASE_H, PER_PROB_MIN, SPACING_H = 4.0, 2.5, 80.0
Q = r"'(?:[^'\\]|\\.)*'"
NODE_RE = re.compile(r"^N\('([^']+)'," + Q + r",'(\w)',(\d)," + Q + "," + Q + "," + Q + r",\[([^\]]*)\]", re.M)


def load(src):
    nodes = []
    for m in NODE_RE.finditer(src):
        pre = [x.strip().strip("'") for x in m.group(4).split(',') if x.strip()]
        nodes.append({'id': m.group(1), 'd': m.group(2), 't': int(m.group(3)), 'pre': pre})
    probs = json.loads(re.search(r"^const PROBS=(\{.*\});$", src, re.M).group(1))
    return nodes, probs


def hours(nodes, probs):
    """단원 id → 어림 시간. 앱 probList·gateList와 같은 규칙으로 숙달 문제를 센다."""
    out = {}
    for n in nodes:
        mins = 0.0
        for row in probs.get(n['id'], []):
            b, a, z, ans = row[0], row[2], row[3], row[4]
            skip = row[6] if len(row) > 6 else 0
            blue = {int(x) for x in ans[2:].split(',')} if str(ans).startswith('b:') else None  # 책 답이 있는 번호(26.11.26)
            for i in range(a, z + 1):
                if skip and skip[0] <= i <= skip[1]:
                    continue
                if (i in blue) if blue is not None else (i % 2 == 0) if ans == 'even' else (i % 2 == 1):
                    mins += BOOK_MIN[b] + PER_PROB_MIN
        out[n['id']] = BASE_H + mins / 60
    return out


def build(nodes, H, plan):
    ix = {n['id']: i for i, n in enumerate(nodes)}
    di = {d: i for i, d in enumerate(DK)}
    done, order, clock, last = set(), [], 0.0, {}
    math_since = 0.0  # 1단계에서 마지막 과학 단원 뒤로 쌓인 수학 시간
    while len(done) < len(nodes):
        av = [n for n in nodes if n['id'] not in done and all(p in done for p in n['pre'])]
        if not av:
            raise SystemExit('선수 고리가 막혔다')
        tier = min(n['t'] for n in av)
        av = [n for n in av if n['t'] == tier]  # 단계 순서는 지킨다(앱의 단계 잠금)
        base = lambda n: (di[n['d']], ix[n['id']])
        if plan == 'default' or (plan == 'spread' and tier == 1):
            av.sort(key=base)
            pick = av[0]
            if plan == 'spread':
                sci = [n for n in av if n['d'] != 'F' and all(NODE[p]['d'] == 'F' for p in n['pre'])]
                if pick['d'] == 'F' and sci and math_since >= SPACING_H:
                    pick = sci[0]
        else:  # alternate: 오래 안 한 영역 먼저(한 번도 안 한 영역이 가장 오래다)
            av.sort(key=lambda n: (last.get(n['d'], -1.0), ) + base(n))
            pick = av[0]
        order.append(pick['id'])
        done.add(pick['id'])
        clock += H[pick['id']]
        last[pick['d']] = clock
        math_since = math_since + H[pick['id']] if pick['d'] == 'F' else 0.0
    return order


def metrics(order, H):
    start, end, t = {}, {}, 0.0
    for u in order:
        start[u] = t
        t += H[u]
        end[u] = t
    run = best = 0.0
    for u in order:
        run = run + H[u] if NODE[u]['d'] == 'F' else 0.0
        best = max(best, run)
    first_p = min(start[u] for u in order if NODE[u]['d'] == 'P')
    gaps = [start[u] - end[p] for u in order for p in NODE[u]['pre']]
    return {'수학만 가장 긴 구간': best, '첫 물리': first_p, '선수→사용 간격 가운데': statistics.median(gaps), '전체': t}


def path_line(order):
    return 'const PATH=' + json.dumps(order, separators=(',', ':')) + ';'


def main():
    global NODE
    src = open(APP, encoding='utf-8').read()
    nodes, probs = load(src)
    NODE = {n['id']: n for n in nodes}
    H = hours(nodes, probs)
    plans = {'default': '기본', 'alternate': '번갈기', 'spread': '고른'}
    orders = {p: build(nodes, H, p) for p in plans}
    chosen = orders['spread']
    if '--show' in sys.argv:
        t = 0.0
        for i, u in enumerate(chosen, 1):
            print(f'{i:3d} {u:14s} {NODE[u]["d"]} {NODE[u]["t"]} {t:7.0f}h +{H[u]:5.1f}')
            t += H[u]
        return 0
    for p, name in plans.items():
        m = metrics(orders[p], H)
        print(f'{name:4s} ' + ' · '.join(f'{k} {v:.0f}시간' for k, v in m.items()))
    line = path_line(chosen)
    m = re.search(r'^const PATH=.*;$', src, re.M)
    if not m:
        print('앱에 const PATH 줄이 없다(PROBS 줄 앞에 넣는다)')
        return 1
    if m.group(0) == line:
        print('PATH 그대로')
        return 0
    if '--check' in sys.argv:
        print('PATH를 고쳐 써야 한다')
        return 1
    open(APP, 'w', encoding='utf-8').write(src[:m.start()] + line + src[m.end():])
    print('PATH 고쳐 씀')
    return 0


NODE = {}
if __name__ == '__main__':
    sys.exit(main())
