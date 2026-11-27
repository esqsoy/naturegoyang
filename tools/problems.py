#!/usr/bin/env python3
"""교재 문제 번호 목록(sources/problems-*.json)을 앱의 `const PROBS=…;` 한 줄로 다시 만든다.

    python3 -I tools/problems.py            # 앱의 PROBS 줄을 고쳐 쓰고 단원별 문제 수를 보인다
    python3 -I tools/problems.py --check    # 고쳐 쓸 것이 있으면 1로 끝난다

앱의 한 줄: 단원 id → [책, 묶음, 첫 번호, 끝 번호, 답(odd|some|all|none), 이름, 뺄 범위|0, 목표?] 의 목록.
책 순서는 BOOK_ORDER, 같은 책 안에서는 json의 순서(풀 순서)를 따른다. 문제 글은 어디에도 두지 않는다.
목표: sources/problem-objs.json이 번호 범위마다 단원 목표(1~3)를 정하면 줄을 그 범위로 나누고 끝 칸에 목표를 붙인다.
앱은 목표 k의 문제를 설명의 목표 k 끝에 끼운다. 목표가 없는 번호는 암기 뒤 교재 단계에서 푼다(26.11.16).
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
APP = os.path.join(REPO, 'app', 'naturegoyang.html')
BOOK_ORDER = ['thomas13', 'epp5', 'lang3', 'serway9', 'mcmurry8', 'campbell12']
THOMAS_END = {'P': '장 연습 문제', 'A': '장 추가·심화', 'R': '장 복습 질문'}


def thomas_rows(d):
    """sources/problems-thomas13.json(절 → 끝 번호)은 꼴이 달라서 따로 푼다."""
    S, out = d['sections'], {}
    for u, v in d['units'].items():
        rows = []
        for s in v['sections']:
            x = S[s]
            if s.startswith('end'):
                ch = s[3:]
                rows += [['thomas13', ch + k, 1, x[f], 'none' if k == 'R' else 'odd', ch + lab]
                         for k, f, lab in (('P', 'practice', THOMAS_END['P']), ('A', 'additional', THOMAS_END['A']), ('R', 'review', THOMAS_END['R']))]
            else:
                r = ['thomas13', s, 1, x['n'], 'odd', f'{s}절']
                if 'ce' in x:
                    r.append(x['ce'])
                rows.append(r)
        out[u] = rows
    return out


def build():
    per_book = {}
    for p in sorted(glob.glob(os.path.join(REPO, 'sources', 'problems-*.json'))):
        d = json.load(open(p, encoding='utf-8'))
        b = d.get('book')
        if b == 'thomas13':
            per_book[b] = thomas_rows(d)
            continue
        rows = {}
        for g in d['groups']:
            if not g.get('unit') or g.get('exclude'):
                continue
            ans = g.get('ans', 'none')
            if g.get('blue'):  # 책 뒤에 답이 있는 번호(Epp 부록 B): 앱이 이 번호를 숙달 문제로 삼는다(26.11.26)
                ans = 'b:' + ','.join(str(i) for i in sorted(set(int(x) for x in g['blue'])))
            r = [b, g['sec'], int(g['from']), int(g['to']), ans, g.get('label') or g['sec']]
            if g.get('skip'):
                r.append(g['skip'])
            rows.setdefault(g['unit'], []).append(r)
        per_book[b] = rows
    probs = {}
    for b in sorted(per_book, key=lambda x: BOOK_ORDER.index(x) if x in BOOK_ORDER else 99):
        for u, rows in per_book[b].items():
            probs.setdefault(u, []).extend(rows)
    return probs


def count(rows):
    n = 0
    for r in rows:
        n += r[3] - r[2] + 1
        if len(r) > 6 and r[6]:
            lo, hi = max(r[6][0], r[2]), min(r[6][1], r[3])
            n -= max(0, hi - lo + 1)
    return n


def apply_objs(probs, warn):
    """sources/problem-objs.json: {"units": {단원: [[책, 묶음, 첫, 끝, 목표], ...]}} — 줄을 목표 범위로 나눈다."""
    path = os.path.join(REPO, 'sources', 'problem-objs.json')
    if not os.path.exists(path):
        return probs
    objs = json.load(open(path, encoding='utf-8')).get('units', {})
    for u, ranges in objs.items():
        rows = probs.get(u)
        if not rows:
            warn.append(f'{u}: 문제 목록이 없는데 목표 범위가 있다')
            continue
        by = {}
        for b, sec, a, z, o in ranges:
            if o not in (1, 2, 3):
                warn.append(f'{u} {b}|{sec} {a}-{z}: 목표 {o}')
            by.setdefault((b, sec), []).append((int(a), int(z), int(o)))
        known = {(r[0], r[1]) for r in rows}
        for key in by:
            if key not in known:
                warn.append(f'{u}: 목록에 없는 묶음 {key[0]}|{key[1]}')
        out = []
        for r in rows:
            b, sec, a, z = r[0], r[1], r[2], r[3]
            skip = r[6] if len(r) > 6 else 0
            rs = sorted(by.get((b, sec), []))
            o_of = {}
            for x, y, o in rs:
                if x < a or y > z:
                    warn.append(f'{u} {b}|{sec}: 범위 {x}-{y}가 {a}-{z} 밖')
                for i in range(max(x, a), min(y, z) + 1):
                    if i in o_of:
                        warn.append(f'{u} {b}|{sec} {i}번: 목표가 겹친다')
                    o_of[i] = o
            miss = [i for i in range(a, z + 1) if i not in o_of and not (skip and skip[0] <= i <= skip[1])]
            if rs and miss:
                warn.append(f'{u} {b}|{sec}: 목표 없는 번호 {len(miss)}개 ({miss[0]}…)')
            if not rs:
                out.append(r)
                continue
            i = a
            while i <= z:
                o, j = o_of.get(i, 0), i
                while j + 1 <= z and o_of.get(j + 1, 0) == o:
                    j += 1
                nr = [b, sec, i, j, r[4], r[5], skip or 0]
                if o:
                    nr.append(o)
                elif not skip:
                    nr = nr[:6]
                out.append(nr)
                i = j + 1
        probs[u] = out
    return probs


def apply_moves(probs, warn):
    """problems-*.json의 "moves": [{"sec", "from", "to", "unit", "o", "why"}] — 그 번호를 맡던 단원에서 빼고 unit으로 옮긴다.
    토마스 목록은 절 단위라 한 문제를 옮길 장치가 없었다(HANDOFF '문제 목표 정하기에서 나온 빈 곳'). 목표(o)는 옮겨 간 단원의 것이다."""
    for p in sorted(glob.glob(os.path.join(REPO, 'sources', 'problems-*.json'))):
        d = json.load(open(p, encoding='utf-8'))
        b = d.get('book')
        for mv in d.get('moves', []):
            sec, ma, mz, to, o = mv['sec'], int(mv['from']), int(mv['to']), mv['unit'], int(mv.get('o', 0))
            moved = None
            for u, rows in probs.items():
                out = []
                for r in rows:
                    if r[0] != b or r[1] != sec or r[3] < ma or r[2] > mz:
                        out.append(r)
                        continue
                    if r[2] > ma or r[3] < mz:
                        warn.append(f'{b}|{sec} {ma}-{mz}: 한 줄 안에 다 들지 않는다({u} {r[2]}-{r[3]})')
                    moved = moved or r
                    for lo, hi in ((r[2], ma - 1), (mz + 1, r[3])):
                        if lo <= hi:
                            out.append([r[0], r[1], lo, hi] + r[4:])
                probs[u] = out
            if not moved:
                warn.append(f'{b}|{sec} {ma}-{mz}: 옮길 번호를 맡은 단원이 없다')
                continue
            nr = [b, sec, ma, mz, moved[4], moved[5], 0]
            if o:
                nr.append(o)
            probs.setdefault(to, []).append(nr)
    return probs


def apply_noans(probs, warn):
    """problems-*.json의 "noans": [{"sec", "n": [번호, …], "why"}] — 책 뒤 답이 실리는 범위(odd 등) 안인데 답이 없는 번호(증명 문제 등).
    그 번호를 제 줄로 떼어 ans를 'none'으로 둔다. 앱은 그 문제를 처음부터 'Claude에게 판정'으로 연다
    (26.11.26 플레이테스트: 책 답 칸이 먼저 떠서 '책 답이 없어'를 한 번 더 눌러야 했다)."""
    for p in sorted(glob.glob(os.path.join(REPO, 'sources', 'problems-*.json'))):
        d = json.load(open(p, encoding='utf-8'))
        b = d.get('book')
        for na in d.get('noans', []):
            sec = na['sec']
            for n in sorted(int(x) for x in na['n']):
                hit = False
                for u, rows in probs.items():
                    out = []
                    for r in rows:
                        if r[0] != b or r[1] != sec or not (r[2] <= n <= r[3]):
                            out.append(r)
                            continue
                        hit = True
                        if r[2] <= n - 1:
                            out.append([b, sec, r[2], n - 1] + r[4:])
                        out.append([b, sec, n, n, 'none'] + r[5:])
                        if n + 1 <= r[3]:
                            out.append([b, sec, n + 1, r[3]] + r[4:])
                    probs[u] = out
                if not hit:
                    warn.append(f'{b}|{sec} {n}번: 답 없음으로 둘 번호를 맡은 단원이 없다')
    return probs


def main():
    warn = []
    probs = apply_noans(apply_moves(apply_objs(build(), warn), warn), warn)
    for w in warn:
        print('경고:', w, file=sys.stderr)
    src = open(APP, encoding='utf-8', newline='').read()
    m = re.search(r'^const PROBS=.*;\r?$', src, re.M)
    if not m:
        print('앱에 const PROBS 줄이 없다', file=sys.stderr)
        return 2
    line = 'const PROBS=' + json.dumps(probs, ensure_ascii=False, separators=(',', ':')) + ';'
    if m.group(0).rstrip('\r') == line:
        print('같다')
        return 0
    if '--check' in sys.argv:
        print('PROBS를 다시 만들어야 한다')
        return 1
    src = src[:m.start()] + line + ('\r' if m.group(0).endswith('\r') else '') + src[m.end():]
    open(APP, 'w', encoding='utf-8', newline='').write(src)
    for u in sorted(probs):
        print(f'{u}\t{count(probs[u])}')
    print('합계', sum(count(v) for v in probs.values()))
    return 0


if __name__ == '__main__':
    sys.exit(main())
