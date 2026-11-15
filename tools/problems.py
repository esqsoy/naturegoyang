#!/usr/bin/env python3
"""교재 문제 번호 목록(sources/problems-*.json)을 앱의 `const PROBS=…;` 한 줄로 다시 만든다.

    python3 -I tools/problems.py            # 앱의 PROBS 줄을 고쳐 쓰고 단원별 문제 수를 보인다
    python3 -I tools/problems.py --check    # 고쳐 쓸 것이 있으면 1로 끝난다

앱의 한 줄: 단원 id → [책, 묶음, 첫 번호, 끝 번호, 답(odd|some|all|none), 이름, 뺄 범위?] 의 목록.
책 순서는 BOOK_ORDER, 같은 책 안에서는 json의 순서(풀 순서)를 따른다. 문제 글은 어디에도 두지 않는다.
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
            r = [b, g['sec'], int(g['from']), int(g['to']), g.get('ans', 'none'), g.get('label') or g['sec']]
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
        if len(r) > 6:
            n -= r[6][1] - r[6][0] + 1
    return n


def main():
    probs = build()
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
