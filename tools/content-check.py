#!/usr/bin/env python3
"""미리 만든 설명·카드가 앱 형식과 과학고양 규칙에 맞는지 검사한다.

    python3 -I tools/content-check.py f-measure      # 한 단원
    python3 -I tools/content-check.py --all          # content/ 아래 전부
    python3 -I tools/content-check.py f-method --related   # [[id]]로 쓸 수 있는 단원 보기
    python3 -I tools/content-check.py --upload f-method --out <폴더>   # Artifact 저장소에 올릴 JSON 만들기

규칙은 content/README.md. 오류가 있으면 1로 끝난다. 경고는 사람이 보고 판단한다.
"""
import argparse
import ast
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
APP = os.path.join(REPO, 'app', 'naturegoyang.html')
CONTENT = os.path.join(REPO, 'content')

SECTIONS = ['핵심 질문', '원리', '예제', '흔한 오개념', '연결', '요약']
LAYERS = {'직관', '통상', '엄밀', '직관·통상', '통상·엄밀', '직관·엄밀', '직관·통상·엄밀'}
KINDS = ['정의', '기호', '법칙', '상수', '분류', '사실', '용어']
LINK = re.compile(r'\[\[([a-z]+-[a-z]+)(?:\|[^\]]*)?\]\]')
# 단원 번호처럼 보이는 "45번", "35·36번" (횟수·염색체·원자 번호 같은 것도 걸리므로 경고로만)
NUMREF = re.compile(r'(?<![\d.])\d{1,3}(?:[·~]\d{1,3})*번(?!째)')
ids_all = set()
titles = {}


def shown(s):
    """화면에 보이는 글: [[id|#]]는 "45번", [[id|이름]]은 이름, [[id]]는 단원 제목."""
    s = re.sub(r'\[\[([a-z]+-[a-z]+)\|#\]\]', '00번', s)
    s = re.sub(r'\[\[([a-z]+-[a-z]+)\|([^\]]*)\]\]', r'\2', s)
    return re.sub(r'\[\[([a-z]+-[a-z]+)\]\]', lambda m: titles.get(m.group(1), m.group(1)), s)


def load_nodes():
    src = open(APP, encoding='utf-8').read()
    nodes = []
    for m in re.finditer(r"^N\((.*)\);\s*$", src, re.M):
        a = ast.literal_eval('(' + m.group(1) + ')')
        nodes.append(dict(id=a[0], sym=a[1], d=a[2], tier=a[3], t=a[4], s=a[5], q=a[6], pre=a[7], ideas=a[8], obj=a[9]))
    by = {n['id']: n for n in nodes}
    ids_all.update(by)
    titles.update({k: v['t'] for k, v in by.items()})
    unlocks = {n['id']: [m['id'] for m in nodes if n['id'] in m['pre']] for n in nodes}
    # 번호: CURRICULUM.md 표(앱이 열 때 계산한 것을 뽑아 둔 것)
    num = {}
    cur = open(os.path.join(REPO, 'CURRICULUM.md'), encoding='utf-8').read()
    title2id = {n['t']: n['id'] for n in nodes}
    for row in re.finditer(r'^\|\s*(\d+)\s*\|\s*\w+\s*\|\s*([^|]+?)\s*\|', cur, re.M):
        t = row.group(2)
        if t in title2id:
            num[title2id[t]] = int(row.group(1))
    return nodes, by, unlocks, num


def related(nid, nodes, by, unlocks):
    """앱 related()와 같은 계산."""
    n = by[nid]
    s = []
    def add(x):
        if x not in s:
            s.append(x)
    for p in n['pre']:
        add(p)
        for q in by[p]['pre']:
            add(q)
    for u in unlocks[nid]:
        add(u)
    extra = [m['id'] for m in nodes if m['id'] != nid and m['d'] != n['d']
             and any(i in n['ideas'] for i in m['ideas']) and m['id'] not in s][:8]
    for x in extra:
        add(x)
    return [x for x in s if x != nid]


def plain_len(s):
    s = shown(s)
    s = re.sub(r'\$\$[\s\S]*?\$\$', '수식수식수식', s)
    s = re.sub(r'\$[^$\n]+\$', '수식', s)
    s = re.sub(r'[#*>|`\-:]', '', s)
    return len(re.sub(r'\s+', '', s))


def check_lesson(md, n, rel, num, errs, warns, info):
    lines = md.replace('\r', '').split('\n')
    h2 = [(i, l[3:].strip()) for i, l in enumerate(lines) if re.match(r'^## ', l)]
    names = [t for _, t in h2]
    if names != SECTIONS:
        errs.append(f'큰 제목 순서가 다르다: {names}')
    total = len(shown(md))
    info.append(f'설명 {total}자')
    if not 3000 <= total <= 5000:
        warns.append(f'분량 {total}자 (3000~5000)')
    # 원리 블록
    try:
        a = next(i for i, t in h2 if t == '원리')
        b = next(i for i, t in h2 if t == '예제')
    except StopIteration:
        return
    body = lines[a + 1:b]
    h3 = [i for i, l in enumerate(body) if l.startswith('### ')]
    if len(h3) != len(n['obj']):
        errs.append(f'원리의 ### 수 {len(h3)} ≠ 학습 목표 수 {len(n["obj"])}')
    for k, s in enumerate(h3):
        e = h3[k + 1] if k + 1 < len(h3) else len(body)
        blk = body[s:e]
        title = blk[0][4:].strip()
        h4 = [(j, l[5:].strip()) for j, l in enumerate(blk) if l.startswith('#### ')]
        lay = [t for _, t in h4 if not t.startswith('점검')]
        bad = [t for t in lay if t not in LAYERS]
        if bad:
            errs.append(f'"{title}": 층 제목이 규칙 밖이다 {bad}')
        if not lay:
            errs.append(f'"{title}": 층(####)이 없다')
        if not h4 or not h4[-1][1].startswith('점검'):
            errs.append(f'"{title}": 마지막이 점검 블록이 아니다')
        else:
            chk = '\n'.join(blk[h4[-1][0] + 1:])
            if not re.search(r'^\*\*Q\.\*\*\s*\S', chk, re.M) or not re.search(r'^\*\*A\.\*\*\s*\S', chk, re.M):
                errs.append(f'"{title}": 점검에 **Q.**/**A.** 줄이 없다')
        for j, (pos, t) in enumerate(h4):
            if t.startswith('점검'):
                continue
            end = h4[j + 1][0] if j + 1 < len(h4) else len(blk)
            pl = plain_len('\n'.join(blk[pos + 1:end]))
            if pl > 600:
                warns.append(f'"{title}" {t} 층 {pl}자 (600 안쪽)')
    # [[id]], [[id|#]], [[id|이름]]: '연결'에서는 related()만, 본문에서는 있는 단원이면 된다(26.11.14, 순서 통제 없음)
    c0 = next((i for i, t in h2 if t == '연결'), len(lines))
    c1 = next((i for i, t in h2 if t == '요약'), len(lines))
    link_part = '\n'.join(lines[c0:c1])
    for x in re.findall(r'\[\[([a-z]+-[a-z]+)\]\]', link_part):
        if x not in rel:
            warns.append(f'연결의 [[{x}]]는 related() 밖이다(지도가 바뀌어 선수가 달라졌는지 본다)')
    for x in LINK.findall(md):
        if x not in ids_all:
            errs.append(f'[[{x}]]는 앱에 없는 단원 id다')
    # 번호로 단원을 가리키면 지도가 바뀔 때 틀린다. [[id|#]]로 쓴다(앱이 지금 번호를 보인다)
    for i, l in enumerate(lines, 1):
        for m in NUMREF.finditer(l):
            warns.append(f'{i}줄: "{m.group(0)}" — 단원이면 [[id|#]]로')
    # 수식 짝
    for i, l in enumerate(lines, 1):
        t = l.replace('\\$', '')
        if t.strip().startswith('$$'):
            if not (t.strip().endswith('$$') and len(t.strip()) > 4):
                errs.append(f'{i}줄: $$는 한 줄에 열고 닫는다')
            continue
        if t.count('$') % 2:
            errs.append(f'{i}줄: $ 짝이 안 맞는다')
    # 굵은 용어
    terms = re.findall(r'\*\*([^*]+?)\*\*\(([^)]*)\)', md)
    return terms


def check_cards(cards, terms, errs, warns, info):
    if not isinstance(cards, list) or not cards:
        errs.append('cards.json은 비어 있지 않은 배열이어야 한다')
        return
    ids = []
    for i, c in enumerate(cards, 1):
        cid = c.get('id')
        if cid != f'c{i:02d}':
            errs.append(f'{i}번째 카드 id가 {cid} (c{i:02d}이어야 한다)')
        ids.append(cid)
        if c.get('k') not in KINDS:
            errs.append(f'{cid}: k "{c.get("k")}"는 {KINDS} 밖이다')
        for f in ('q', 'a'):
            if not isinstance(c.get(f), str) or not c[f].strip():
                errs.append(f'{cid}: {f}가 비었다')
        if not isinstance(c.get('h', ''), str):
            errs.append(f'{cid}: h는 문자열')
        for f in ('q', 'a', 'h'):
            if isinstance(c.get(f), str) and c[f].replace('\\$', '').count('$') % 2:
                errs.append(f'{cid}: {f}의 $ 짝이 안 맞는다')
            if isinstance(c.get(f), str):
                for x in LINK.findall(c[f]):
                    if x not in ids_all:
                        errs.append(f'{cid}: [[{x}]]는 앱에 없는 단원 id다')
                for m in NUMREF.finditer(c[f]):
                    warns.append(f'{cid}: {f}의 "{m.group(0)}" — 단원이면 [[id|#]]로')
        if c.get('k') == '용어' and not re.search(r'[A-Za-z]', c.get('a', '')):
            warns.append(f'{cid}: 용어 카드 뒷면에 영어가 없다')
    live = [c for c in cards if not c.get('x')]
    nterm = sum(1 for c in live if c.get('k') == '용어')
    rest = len(live) - nterm
    info.append(f'카드 {rest}장 + 용어 {nterm}장')
    if not 12 <= rest <= 25:
        warns.append(f'용어 카드 뺀 카드 {rest}장 (12~25)')
    have = {c['q'].strip() for c in live if c.get('k') == '용어'}
    miss = [t for t, _ in terms or [] if t.strip() not in have]
    if miss:
        warns.append(f'굵게 병기한 용어 가운데 용어 카드가 없는 것: {miss}')


def check_unit(uid, ctx):
    nodes, by, unlocks, num = ctx
    errs, warns, info = [], [], []
    if uid not in by:
        print(f'{uid}: 앱에 없는 단원 id')
        return 1
    d = os.path.join(CONTENT, uid)
    rel = related(uid, nodes, by, unlocks)
    terms = None
    lp = os.path.join(d, 'lesson.md')
    if os.path.exists(lp):
        terms = check_lesson(open(lp, encoding='utf-8').read(), by[uid], rel, num, errs, warns, info)
    else:
        errs.append('lesson.md 없음')
    cp = os.path.join(d, 'cards.json')
    if os.path.exists(cp):
        try:
            check_cards(json.load(open(cp, encoding='utf-8')), terms, errs, warns, info)
        except json.JSONDecodeError as e:
            errs.append(f'cards.json JSON 오류: {e}')
    else:
        errs.append('cards.json 없음')
    kp = os.path.join(d, 'check.md')
    if not os.path.exists(kp) or not re.search(r'^상태:', open(kp, encoding='utf-8').read(), re.M):
        errs.append('check.md에 "상태:" 줄이 없다')
    print(f'## {num.get(uid, "?")} {by[uid]["t"]} ({uid}) · ' + ', '.join(info))
    for e in errs:
        print('  오류:', e)
    for w in warns:
        print('  경고:', w)
    if not errs and not warns:
        print('  통과')
    return 1 if errs else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('unit', nargs='?')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--related', action='store_true')
    ap.add_argument('--upload', metavar='ID')
    ap.add_argument('--out')
    o = ap.parse_args()
    ctx = load_nodes()
    nodes, by, unlocks, num = ctx
    if o.related and o.unit:
        for x in related(o.unit, nodes, by, unlocks):
            print(f'{x} = {num.get(x, "?")} {by[x]["t"]}')
        return 0
    if o.upload:
        if not o.out:
            print('--out 폴더를 준다', file=sys.stderr)
            return 2
        if check_unit(o.upload, ctx):
            print('오류가 있어 올릴 파일을 만들지 않는다')
            return 1
        os.makedirs(o.out, exist_ok=True)
        d = os.path.join(CONTENT, o.upload)
        now = int(time.time() * 1000)
        md = open(os.path.join(d, 'lesson.md'), encoding='utf-8').read()
        items = json.load(open(os.path.join(d, 'cards.json'), encoding='utf-8'))
        lp = os.path.join(o.out, f'{o.upload}--v3.lesson.json')
        cp = os.path.join(o.out, f'{o.upload}.cards.json')
        json.dump({'md': md, 'node': o.upload, 'at': now, 'src': 'content'}, open(lp, 'w', encoding='utf-8'), ensure_ascii=False)
        json.dump({'items': items, 'node': o.upload, 'at': now, 'src': 'content'}, open(cp, 'w', encoding='utf-8'), ensure_ascii=False)
        print(f'→ {lp}\n→ {cp}')
        return 0
    ids = sorted((x for x in os.listdir(CONTENT) if os.path.isdir(os.path.join(CONTENT, x))), key=lambda x: num.get(x, 999)) if o.all else [o.unit]
    if not ids or ids == [None]:
        ap.print_help()
        return 2
    return max(check_unit(u, ctx) for u in ids)


if __name__ == '__main__':
    sys.exit(main())
