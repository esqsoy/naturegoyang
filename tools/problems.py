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


def main():
    warn = []
    probs = apply_objs(build(), warn)
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
