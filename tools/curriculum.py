#!/usr/bin/env python3
"""CURRICULUM.md(단원 목록)를 앱 원본에서 다시 만든다.

    python3 -I tools/curriculum.py            # CURRICULUM.md를 고쳐 쓴다
    python3 -I tools/curriculum.py --check    # 고쳐 쓸 것이 있으면 1로 끝난다

번호는 앱 number()와 같은 규칙으로 센다: 선수가 모두 놓인 단원 가운데 단계 → 영역 → N(...) 줄 순서가 가장 앞인 것.
"""
import ast
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
APP = os.path.join(REPO, 'app', 'naturegoyang.html')
OUT = os.path.join(REPO, 'CURRICULUM.md')
DKEYS = ['F', 'P', 'C', 'B', 'E']


def load():
    src = open(APP, encoding='utf-8').read()
    nodes = []
    for m in re.finditer(r"^N\((.*)\);\s*$", src, re.M):
        a = ast.literal_eval('(' + m.group(1) + ')')
        nodes.append(dict(id=a[0], sym=a[1], d=a[2], tier=a[3], t=a[4], s=a[5], q=a[6], pre=a[7], ideas=a[8], obj=a[9]))
    dom = dict(re.findall(r"^\s*([FPCBE]):\{name:'([^']+)'", src, re.M))
    tiers = {int(k): (l, d) for k, l, d in re.findall(r"^\s*(\d):\{label:'([^']+)', short:'[^']+', desc:'([^']+)'\}", src, re.M)}
    ideas = dict(re.findall(r"^\s*([A-Z]{2}):\{name:'([^']+)'", src, re.M))
    return nodes, dom, tiers, ideas


def number(nodes):
    di = {d: i for i, d in enumerate(DKEYS)}
    ix = {n['id']: i for i, n in enumerate(nodes)}
    placed, order = set(), []
    while len(order) < len(nodes):
        av = [n for n in nodes if n['id'] not in placed and all(p in placed for p in n['pre'])]
        if not av:
            raise SystemExit('선수 관계에 고리가 있다: ' + ', '.join(n['id'] for n in nodes if n['id'] not in placed))
        av.sort(key=lambda n: (n['tier'], di[n['d']], ix[n['id']]))
        order.append(av[0])
        placed.add(av[0]['id'])
    return {n['id']: k + 1 for k, n in enumerate(order)}, order


def render():
    nodes, dom, tiers, ideas = load()
    no, order = number(nodes)
    by = {n['id']: n for n in nodes}
    out = ['# 단원 목록', '',
           f"{len(nodes)}단원. 번호는 선수 관계를 지킨 순서이고 '이어하기' 순서다. 원본은 `app/naturegoyang.html`의 `N(...)` 줄이며, "
           "번호는 앱이 열릴 때 계산한다. 이 표는 `tools/curriculum.py`가 앱 원본에서 뽑는다(손으로 고치지 않는다). "
           "단원마다 학습 목표 3개와 핵심 질문은 앱 원본에 있다. 설명·카드는 다른 단원을 번호가 아니라 `[[id|#]]`로 가리키므로 번호가 바뀌어도 맞다.", '']
    for t in sorted(tiers):
        label, desc = tiers[t]
        out += [f'## {label} — {desc}', '', '| 번호 | 기호 | 단원 | 영역 | 선수 단원 | 큰 개념 |', '|---|---|---|---|---|---|']
        for n in order:
            if n['tier'] != t:
                continue
            pre = ', '.join(f"{no[p]} {by[p]['s']}" for p in sorted(n['pre'], key=lambda p: no[p])) or '—'
            out.append(f"| {no[n['id']]} | {n['sym']} | {n['t']} | {dom[n['d']]} | {pre} | {', '.join(ideas[i] for i in n['ideas'])} |")
        out.append('')
    return '\n'.join(out)


def main():
    text = render()
    old = open(OUT, encoding='utf-8').read() if os.path.exists(OUT) else ''
    if '--check' in sys.argv:
        print('같다' if old == text else 'CURRICULUM.md를 다시 만들어야 한다')
        return 0 if old == text else 1
    open(OUT, 'w', encoding='utf-8', newline='\n').write(text)
    print(f'→ {OUT}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
