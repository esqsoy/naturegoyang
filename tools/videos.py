#!/usr/bin/env python3
"""3Blue1Brown 영상 짝(sources/videos-3b1b.json)을 앱의 `const VIDEOS=…;` 한 줄로 다시 만든다.

    python3 -I tools/videos.py            # 앱의 VIDEOS 줄을 고쳐 쓴다
    python3 -I tools/videos.py --check    # 고쳐 쓸 것이 있으면 1로 끝난다

앱의 한 줄: 단원 id → [[YouTube id, 제목, 분, 한국어 자막(1|0), 이 단원에 맞는 까닭], ...].
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
APP = os.path.join(REPO, 'app', 'naturegoyang.html')
SRC = os.path.join(REPO, 'sources', 'videos-3b1b.json')
YT = re.compile(r'^[A-Za-z0-9_-]{11}$')


def build():
    d = json.load(open(SRC, encoding='utf-8'))
    out = {}
    for u, vs in d['units'].items():
        rows = []
        for v in vs:
            if not YT.match(v['id']):
                raise SystemExit(f'{u}: YouTube id가 이상하다: {v["id"]}')
            rows.append([v['id'], v['title'], v.get('minutes') or 0, 1 if v.get('ko') else 0, v.get('why', '')])
        if rows:
            out[u] = rows
    return out


def main():
    vids = build()
    src = open(APP, encoding='utf-8', newline='').read()
    ids = set(re.findall(r"^N\('([a-z0-9-]+)'", src, re.M))
    bad = [u for u in vids if u not in ids]
    if bad:
        print('앱에 없는 단원:', bad, file=sys.stderr)
        return 2
    m = re.search(r'^const VIDEOS=.*;\r?$', src, re.M)
    if not m:
        print('앱에 const VIDEOS 줄이 없다', file=sys.stderr)
        return 2
    line = 'const VIDEOS=' + json.dumps(vids, ensure_ascii=False, separators=(',', ':')) + ';'
    if m.group(0).rstrip('\r') == line:
        print('같다')
        return 0
    if '--check' in sys.argv:
        print('VIDEOS를 다시 만들어야 한다')
        return 1
    src = src[:m.start()] + line + ('\r' if m.group(0).endswith('\r') else '') + src[m.end():]
    open(APP, 'w', encoding='utf-8', newline='').write(src)
    print(f'{len(vids)}단원, 영상 {sum(len(v) for v in vids.values())}개')
    return 0


if __name__ == '__main__':
    sys.exit(main())
