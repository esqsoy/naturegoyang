#!/usr/bin/env python3
"""자유 이용 사진·그림 장부(sources/images.json)로 app/img/를 만든다(26.11.16, 앱 17판).

영신: "혹은 그림을 찾아서 넣는건 어때? 분명 자유 이용으로도 과학관련 이미지는 쓸만한게 많을텐데"

  python3 -I tools/images.py fetch [img/…]   장부에 있고 app/img/에 없는 파일을 받아 가로 1200px·세로 1400px 안으로 줄여 저장
  python3 -I tools/images.py credits         app/img/CREDITS.md(저작자·이용 허락·출처·고친 것)를 장부에서 다시 씀
  python3 -I tools/images.py check           장부·파일·설명(```img 블록)이 서로 맞는지

이용 허락은 공유 저작물·CC0·CC BY·CC BY-SA만 받는다(content-check.py와 같은 규칙). 받은 파일은 새 빈 임시 폴더에
두고 그림으로 열어 다시 저장한 것만 app/img/에 넣는다(메타데이터는 버린다). 웹 요청에는 사용자 정보를 넣지 않는다.
"""
import json
import os
import re
import sys
import tempfile
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
REG = os.path.join(REPO, 'sources', 'images.json')
IMG = os.path.join(REPO, 'app', 'img')
CONTENT = os.path.join(REPO, 'content')
LICENSES = re.compile(r'^(public domain|CC0 1\.0|CC BY(-SA)? \d\.\d)$')
UA = 'naturegoyang-images/1.0 (educational app; image fetch with attribution)'
MAXW = 1200
MAXH = 1400


def load():
    return json.load(open(REG, encoding='utf-8'))


def fetch(only):
    from PIL import Image
    reg = load()['images']
    todo = [k for k in reg if (not only or k in only) and not os.path.exists(os.path.join(REPO, 'app', k))]
    os.makedirs(IMG, exist_ok=True)
    for k in todo:
        r = reg[k]
        if not LICENSES.match(r.get('license', '')):
            print(f'건너뜀 {k}: 이용 허락 "{r.get("license")}"')
            continue
        tmp = tempfile.mkdtemp(prefix='ng-img-')
        raw = os.path.join(tmp, 'download')
        for attempt in range(8):  # 위키미디어는 몰아 받으면 429를 낸다: 기다렸다 다시
            try:
                req = urllib.request.Request(r.get('fetch_url') or r['file_url'], headers={'User-Agent': UA})  # fetch_url: 위키미디어 축소판(원본은 429가 잦다)
                with urllib.request.urlopen(req, timeout=60) as f, open(raw, 'wb') as o:
                    o.write(f.read(40 * 1024 * 1024))
                break
            except urllib.error.HTTPError as e:
                if e.code != 429 or attempt == 7:
                    raise
                wait = int(e.headers.get('Retry-After') or 0) or 30 * (attempt + 1)
                print(f'429, {wait}초 기다림')
                time.sleep(wait)
        time.sleep(30)
        im = Image.open(raw)
        im.load()
        if r.get('crop'):  # [왼, 위, 오른, 아래] 원본 픽셀
            im = im.crop(tuple(r['crop']))
        k_ = min(1, MAXW / im.width, MAXH / im.height)
        if k_ < 1:
            im = im.resize((round(im.width * k_), round(im.height * k_)), Image.LANCZOS)
        out = os.path.join(REPO, 'app', k)
        if k.lower().endswith(('.jpg', '.jpeg')):
            if im.mode in ('RGBA', 'LA', 'P'):
                bg = Image.new('RGB', im.size, 'white')
                im = im.convert('RGBA')
                bg.paste(im, mask=im.split()[-1])
                im = bg
            im.convert('RGB').save(out, 'JPEG', quality=84, optimize=True, progressive=True)
        else:
            im.save(out, 'PNG', optimize=True)
        print(f'받음 {k} {im.width}×{im.height} {os.path.getsize(out):,} bytes')


def credits():
    reg = load()['images']
    lines = ['# 그림 출처', '',
             '앱 설명에 넣은 자유 이용 사진·그림의 저작자와 이용 허락이다. 장부는 `sources/images.json`, 이 파일은 `tools/images.py credits`가 만든다(손으로 고치지 않는다).',
             '', '| 파일 | 단원 | 제목 | 저작자 | 이용 허락 | 출처 | 고친 것 |', '|---|---|---|---|---|---|---|']
    for k in sorted(reg):
        r = reg[k]
        lic = f'[{r["license"]}]({r["license_url"]})' if r.get('license_url') else r['license']
        src = r['source'].replace('(', '%28').replace(')', '%29')
        got = '' if os.path.exists(os.path.join(REPO, 'app', k)) else ' (받기 전)'
        lines.append(f'| `{k}`{got} | {r.get("unit", "")} | {r.get("title", "")} | {r.get("author", "")} | {lic} | [출처]({src}) | {r.get("changes", "")} |')
    open(os.path.join(IMG, 'CREDITS.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')
    print(f'CREDITS.md {len(reg)}개')


def check():
    reg = load()['images']
    errs = []
    used = {}
    for u in sorted(os.listdir(CONTENT)):
        p = os.path.join(CONTENT, u, 'lesson.md')
        if not os.path.isfile(p):
            continue
        for m in re.finditer(r'^```img\n([\s\S]*?)^```', open(p, encoding='utf-8').read(), re.M):
            src = re.search(r'^src\s+(\S+)', m.group(1), re.M)
            if src:
                used.setdefault(src.group(1), []).append(u)
    for k, r in reg.items():
        if not LICENSES.match(r.get('license', '')):
            errs.append(f'{k}: 이용 허락 "{r.get("license")}"')
        for f in ('title', 'author', 'license', 'source', 'file_url', 'unit'):
            if not r.get(f):
                errs.append(f'{k}: {f}가 없다')
        if not os.path.exists(os.path.join(REPO, 'app', k)):
            errs.append(f'{k}: 파일이 없다(fetch)')
        if k not in used:
            errs.append(f'{k}: 설명에서 쓰지 않는다')
    for k in used:
        if k not in reg:
            errs.append(f'{k}: 장부에 없다({", ".join(used[k])})')
    if os.path.isdir(IMG):
        for f in os.listdir(IMG):
            if f != 'CREDITS.md' and f'img/{f}' not in reg:
                errs.append(f'app/img/{f}: 장부에 없는 파일')
    print('\n'.join(errs) or f'맞음: 그림 {len(reg)}개, 설명에서 {sum(len(v) for v in used.values())}곳')
    return 1 if errs else 0


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'check'
    if cmd == 'fetch':
        fetch(set(sys.argv[2:]))
        return 0
    if cmd == 'credits':
        credits()
        return 0
    return check()


if __name__ == '__main__':
    sys.exit(main())
