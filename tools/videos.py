#!/usr/bin/env python3
"""3Blue1Brown 영상 목록(sources/videos-3b1b.json)과 설명 안 ```link 블록이 맞는지 본다(앱 18판).

영신(26.11.18): "영상은 봐야하는거라면 설명에 녹여서 보고 지나가게 하자". 영상은 옆 칸 목록이 아니라
설명의 그 자리에 ```link 카드로 넣는다. 목록은 짝지은 영상과 그 까닭을 모아 두는 곳이고, 앱은 목록을 읽지 않는다.

    python3 -I tools/videos.py              # 설명이 있는 단원마다: 넣은 영상, 안 넣은 영상, 뺀 영상(skip)
    python3 -I tools/videos.py block <id>   # 그 단원의 목록 영상을 ```link 블록 꼴로 찍는다(붙여 넣을 초안)

목록의 영상에 "skip": "까닭"이 있으면 일부러 넣지 않은 것이다. 설명이 있는 단원에 넣지도 빼지도 않은 영상이 있으면 1로 끝난다.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SRC = os.path.join(REPO, 'sources', 'videos-3b1b.json')
CONTENT = os.path.join(REPO, 'content')
YT = re.compile(r'(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]{11})')


def placed(u):
    p = os.path.join(CONTENT, u, 'lesson.md')
    if not os.path.isfile(p):
        return None
    md = open(p, encoding='utf-8').read()
    return {m.group(1) for b in re.findall(r'^```link\n([\s\S]*?)^```', md, re.M) for m in YT.finditer(b)}


def block(v):
    lines = ['```link', f'url https://www.youtube.com/watch?v={v["id"]}', f'title {v["title"]}', 'kind 영상', 'who 3Blue1Brown']
    if v.get('minutes'):
        lines.append(f'min {v["minutes"]}')
    if v.get('ko'):
        lines.append('note 한국어 자막')
    lines += [f'why {v.get("why", "")}', '```']
    return '\n'.join(lines)


def main():
    d = json.load(open(SRC, encoding='utf-8'))['units']
    if len(sys.argv) > 2 and sys.argv[1] == 'block':
        for v in d.get(sys.argv[2], []):
            print(block(v) + '\n')
        return 0
    bad = 0
    later = []
    for u, vs in d.items():
        got = placed(u)
        if got is None:
            later.append(f'{u}({len(vs)})')
            continue
        ids = {v['id'] for v in vs}
        todo = [v['id'] for v in vs if v['id'] not in got and not v.get('skip')]
        skip = [v['id'] for v in vs if v.get('skip') and v['id'] not in got]
        extra = sorted(got - ids)
        bad += len(todo) + len(extra)
        mark = '맞음' if not todo and not extra else '할 것'
        print(f'{mark} {u}: 넣음 {len(got & ids)}' + (f', 안 넣음 {todo}' if todo else '') + (f', 뺌 {skip}' if skip else '')
              + (f', 목록에 없는 영상 {extra}' if extra else ''))
    print(f'설명이 아직 없는 단원(쓸 때 넣는다): {", ".join(later)}')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
