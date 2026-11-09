#!/usr/bin/env python3
"""『대학기초물리학』(a~d 네 PDF)은 PDF 목차가 없어서 본문 글자로 목차를 만든다.

    python3 -I tools/kphys-outline.py [--private ../비공개/과학고양]

읽는 것: <private>/text/kphys-{a,b,c,d}.txt (tools/pdf-index.js text로 뽑은 것)
쓰는 것: <private>/outline/kphys.json (tools/unit-sources.py가 읽는 꼴)

본문에서 장은 "NN장" 한 줄, 절은 "N.N" 뒤에 사용자 영역 글자(장식 기호)가 붙은 줄로 시작한다.
장 제목은 책 차례의 짧은 제목이다.
"""
import argparse
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PRIVATE = os.path.join(os.path.dirname(os.path.dirname(HERE)), '비공개', '과학고양')

CHAPTERS = {
    1: '물리학의 발달', 2: '물리량', 3: '운동의 기술', 4: '운동법칙',
    5: '간단한 힘을 받는 물체의 운동 I', 6: '간단한 힘을 받는 물체의 운동 II', 7: '일과 에너지',
    8: '여러 물체의 운동', 9: '회전운동', 10: '강체의 운동', 11: '유체의 운동', 12: '진동과 파동',
    13: '열현상', 14: '열역학 법칙', 15: '전하와 전기력', 16: '전위와 전기에너지', 17: '전류와 전기회로',
    18: '전류와 자기력', 19: '전자기 유도', 20: '교류와 교류회로', 21: '전자기파', 22: '광학',
    23: '미시세계의 발견', 24: '양자역학', 25: '특수 상대성이론', 26: '핵물리학', 27: '기본입자',
    28: '일반 상대성이론',
}
CH_RE = re.compile(r'^(\d{2})장$')
SEC_RE = re.compile(r'^(\d{1,2})\.(\d{1,2})[\U000F0000-\U000FFFFF-]\s*(.*)$')
PAGE_RE = re.compile(r'\f=== p\.(\d+) \[[^\]]*\] ===\n')


def pages_of(path):
    parts = PAGE_RE.split(open(path, encoding='utf-8').read())[1:]
    return [(int(parts[i]), parts[i + 1]) for i in range(0, len(parts), 2)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--private', default=DEFAULT_PRIVATE)
    o = ap.parse_args()
    entries, seen, files = [], set(), []
    for part in 'abcd':
        f = f'kphys-{part}'
        path = os.path.join(o.private, 'text', f + '.txt')
        if not os.path.exists(path):
            continue
        files.append(f)
        for page, body in pages_of(path):
            if page < 12 and part == 'a':  # 앞쪽 차례는 건너뛴다
                continue
            lines = [l.strip() for l in body.splitlines()]
            for j, l in enumerate(lines):
                m = CH_RE.match(l)
                if m and int(m.group(1)) in CHAPTERS and ('ch', int(m.group(1))) not in seen:
                    n = int(m.group(1))
                    seen.add(('ch', n))
                    entries.append({'level': 0, 'title': f'제{n}장 {CHAPTERS[n]}', 'page': page, 'file': f})
                    continue
                m = SEC_RE.match(l)
                if m:
                    key = (int(m.group(1)), int(m.group(2)))
                    if key in seen or key[0] not in CHAPTERS:
                        continue
                    seen.add(key)
                    title = m.group(3) or (lines[j + 1] if j + 1 < len(lines) else '')
                    entries.append({'level': 1, 'title': f'{key[0]}.{key[1]} {title}'.strip(), 'page': page, 'file': f})
    # 장 시작 쪽이 절보다 늦게 잡히면(장 표지가 그림뿐인 경우) 첫 절 쪽으로 당긴다
    order = {f: i for i, f in enumerate(files)}
    entries.sort(key=lambda e: (order[e['file']], e['page'], e['level']))
    out = os.path.join(o.private, 'outline', 'kphys.json')
    json.dump({'pages': None, 'files': files, 'entries': entries}, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    chs = sorted(k[1] for k in seen if k[0] == 'ch')
    print(f'파일 {files}, 장 {len(chs)} {chs[:1]}~{chs[-1:]}, 절 {sum(1 for k in seen if k[0] != "ch")} → {out}')


if __name__ == '__main__':
    main()
