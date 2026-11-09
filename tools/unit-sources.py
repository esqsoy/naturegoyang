#!/usr/bin/env python3
"""단원 하나의 교과서 대조 쪽을 찾는다.

    python3 -I tools/unit-sources.py f-measure                 # 책·절·PDF 쪽
    python3 -I tools/unit-sources.py f-measure --text out.txt  # 그 쪽들의 글자를 한 파일로
    python3 -I tools/unit-sources.py --check                   # 대응표의 절이 모두 목차에 있는지

대응표는 sources/unit-map.json(공개, 절 번호만), 목차와 글자는 비공개 폴더
(기본: 저장소 옆 ../비공개/과학고양, 바꾸려면 --private)에 있다.
목차 파일 outline/<책>.json의 entries는 {level, title, page[, file]}이다.
title이 "1.5 ..."나 "Chapter 1: ..."처럼 절·장 번호로 시작하면 그 번호로 찾는다.
여러 PDF로 나뉜 책은 entries마다 file(text/<file>.txt)을 단다.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DEFAULT_PRIVATE = os.path.join(os.path.dirname(REPO), '비공개', '과학고양')

# "1.5 ...", "Chapter 10: ...", "제2장 ...", 부록 "A.1 ..."은 번호로 본다. "SI Units"·"A Closer Look"은 아니다.
# Halliday처럼 "1-1"로 쓰는 책도 있어 붙임표는 점으로 바꿔 읽는다.
SEC_RE = re.compile(r'^(?:Chapter|CHAPTER|Ch|제)?\s*((?:\d+|[A-Z](?=[.-]))(?:[.-]\d+)*)\s*(?:장)?[:.]?\s')
# 장 끝 정리·연습문제 같은 번호 없는 항목에서 절을 끊는다
STOP = ('Chapter Summary', 'Learning Outcomes', 'Key Equations', 'Exercises', 'Summary', 'Review',
        'Questions', 'Problems', '내용정리', '연습문제')
STOP_UP = tuple(s.upper() for s in STOP)


APP_RE = re.compile(r'^Appendix\s+([A-Z])\b')  # "Appendix A: ..." → "A" (부록 전체)


def sec_of(title):
    a = APP_RE.match(title)
    if a:
        return a.group(1)
    m = SEC_RE.match(title + ' ')
    return m.group(1).replace('-', '.') if m else None


def load_outline(private, book):
    path = os.path.join(private, 'outline', book + '.json')
    if not os.path.exists(path):
        return None
    d = json.load(open(path, encoding='utf-8'))
    entries = [e for e in d['entries'] if e.get('page')]
    for e in entries:
        e['sec'] = sec_of(e['title'])
        e.setdefault('file', book)
    return {'pages': d.get('pages'), 'entries': entries}


def span(outline, sec):
    """sec(예: '1.5' 또는 장 '10')의 [시작, 끝] PDF 쪽과 제목, 파일."""
    es = outline['entries']
    depth = sec.count('.')
    for i, e in enumerate(es):
        if e['sec'] != sec:
            continue
        start, end = e['page'], None
        for f in es[i + 1:]:
            if f['file'] != e['file']:
                continue
            s = f['sec']
            if f['page'] <= start:
                continue
            # 같은 깊이 이하의 다음 번호, 더 위 단계 항목, 장 끝 정리가 나오면 끝.
            # 번호 없는 같은 단계 항목(읽을거리 상자)은 목차 끝에 몰려 있어 보지 않는다.
            if (s and s.count('.') <= depth) or f['level'] < e['level'] or (not s and f['title'].upper().startswith(STOP_UP)):
                end = f['page'] - 1
                break
        return {'title': e['title'], 'start': start, 'end': end or start, 'file': e['file']}
    return None


def read_pages(private, file, a, b):
    path = os.path.join(private, 'text', file + '.txt')
    if not os.path.exists(path):
        return None
    t = open(path, encoding='utf-8').read()
    parts = re.split(r'\f=== p\.(\d+) \[[^\]]*\] ===\n', t)[1:]
    pages = {int(parts[i]): parts[i + 1] for i in range(0, len(parts), 2)}
    return '\n'.join(f'--- {file} p.{k}\n{pages.get(k, "")}' for k in range(a, b + 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('unit', nargs='?')
    ap.add_argument('--private', default=DEFAULT_PRIVATE)
    ap.add_argument('--text')
    ap.add_argument('--check', action='store_true')
    o = ap.parse_args()

    umap = json.load(open(os.path.join(REPO, 'sources', 'unit-map.json'), encoding='utf-8'))['units']
    outlines = {}

    def ol(book):
        if book not in outlines:
            outlines[book] = load_outline(o.private, book)
        return outlines[book]

    if o.check:
        bad = 0
        for u, books in umap.items():
            for book, secs in books.items():
                if ol(book) is None:
                    print(f'{u}: {book} 목차 없음(비공개 폴더)')
                    bad += 1
                    continue
                for s in secs:
                    if not span(ol(book), s):
                        print(f'{u}: {book} {s} 목차에 없음')
                        bad += 1
        empty = [u for u, b in umap.items() if not b]
        print(f'단원 {len(umap)}, 대조 없는 단원 {len(empty)}, 문제 {bad}')
        return 1 if bad else 0

    if not o.unit or o.unit not in umap:
        print('단원 id를 준다(예: f-measure).', file=sys.stderr)
        return 2
    texts = []
    for book, secs in umap[o.unit].items():
        outline = ol(book)
        for s in secs:
            sp = span(outline, s) if outline else None
            if not sp:
                print(f'{book} {s}: 목차에서 못 찾음')
                continue
            print(f'{book} {s} · {sp["title"][:60]} · {sp["file"]} p.{sp["start"]}-{sp["end"]}')
            if o.text:
                t = read_pages(o.private, sp['file'], sp['start'], sp['end'])
                texts.append(t if t is not None else f'--- {sp["file"]} 글자 파일 없음')
    if o.text:
        with open(o.text, 'w', encoding='utf-8') as f:
            f.write('\n'.join(texts))
        print(f'→ {o.text}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
