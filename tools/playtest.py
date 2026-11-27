#!/usr/bin/env python3
"""플레이테스트용 연습 앱을 만든다(영신 기록은 건드리지 않는다).

    python3 -I tools/playtest.py --out <폴더> [--state state.json] [단원 id …]

영신 26.11.26: "첫 플레이하기전에 플레이할 부분을 팀원들이 한번 풀어보는건 어때",
"푸는게 아니라 내가 할 그 과정을 그대로 따라가보는걸 말하는거야".
팀원이 영신과 같은 앱 화면으로 같은 과정을 밟도록, 앱 원본에 가짜 런타임을 앞에 붙인 한 파일을 만든다.

- 저장소(db): 메모리 + 브라우저 localStorage. content/의 설명·카드·확인 문제 은행을 `lessons/`·`cards/`·`quiz/`에
  미리 넣는다(`content-check.py --upload`와 같은 꼴). `--state`는 사용자 문서({"progress": {...}, ...})를 처음 값으로 넣는다.
- 사용자(user): id는 'tester'.
- Claude 호출(sample): 앱이 보내는 요청을 `window.__calls`에 쌓는다. 플레이하는 팀원이 `__pending()`으로 읽고
  `__answer(id, 글)`로 모델 대신 답한다(json 요청은 JSON 글).
- 시계: 쪽마다 읽을 시간을 실제로 기다리지 않게 `__skip(초)`가 시계를 앞당긴다. 앞당긴 시간은 `__skipped`에 쌓여
  실제 걸릴 시간 어림에 쓴다.
- 고칠 점으로 남기기(fixes)는 `window.__fixes`에 쌓인다.
결과 파일과 img/는 --out 폴더에 둔다. 공개 저장소에 넣지 않는다(영신 진도 같은 개인 기록이 들어갈 수 있다).
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
APP = os.path.join(REPO, 'app', 'naturegoyang.html')
CONTENT = os.path.join(REPO, 'content')

MOCK = r"""<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script>
(function(){
  'use strict';
  const SEED = __SEED__, INIT = __INIT__, RUN = 'nyplay:' + __RUN__;
  let skew = Number(localStorage.getItem(RUN + ':skew') || 0);
  // Date.now와 인자 없는 new Date()를 함께 앞당긴다(앱이 날짜를 둘 다로 센다. 26.11.27: Date.now만 앞당겨 하루를 넘겨도 홈 날짜가 그대로였다)
  const RealDate = Date;
  class SkewDate extends RealDate {
    constructor(...a) { if (a.length) super(...a); else super(RealDate.now() + skew); }
    static now() { return RealDate.now() + skew; }
  }
  window.Date = SkewDate;
  window.__skipped = Number(localStorage.getItem(RUN + ':skipped') || 0);
  window.__skip = (s) => { skew += s * 1000; window.__skipped += s; localStorage.setItem(RUN + ':skew', skew); localStorage.setItem(RUN + ':skipped', window.__skipped);
    try { if (typeof render === 'function') { if (UI && UI.study && UI.study.step === 'lesson' && typeof paintLesson === 'function') paintLesson(); else render(); } } catch (e) {} return window.__skipped; };
  let store = {};
  try { store = JSON.parse(localStorage.getItem(RUN) || 'null') || {}; } catch (e) {}
  if (!localStorage.getItem(RUN)) { for (const [k, v] of Object.entries(INIT)) store['data/users/tester/' + k] = v; }
  const persist = () => { try { localStorage.setItem(RUN, JSON.stringify(store)); } catch (e) {} };
  persist();
  const clone = (x) => x == null ? x : JSON.parse(JSON.stringify(x));
  const read = (p) => (p in store) ? store[p] : (SEED[p] ?? null);
  const snap = (p) => { const d = read(p); return { exists: d != null, id: p.split('/').pop(), data: () => clone(d) }; };
  window.__fixes = [];
  const db = {
    doc: (p) => ({ get: async () => snap(p), set: async (d) => { store[p] = clone(d); persist(); }, update: async (d) => { store[p] = Object.assign(clone(read(p)) || {}, clone(d)); persist(); }, delete: async () => { delete store[p]; persist(); } }),
    collection: (c) => ({
      add: async (d) => { const id = Math.random().toString(36).slice(2, 10); store[c + '/' + id] = clone(d); window.__fixes.push(clone(d)); persist(); return { id }; },
      where: () => ({ get: async () => ({ docs: Object.entries(store).filter(([k]) => k.startsWith(c + '/')).map(([k, v]) => ({ id: k.split('/').pop(), data: () => clone(v) })) }) }),
      get: async () => ({ docs: [] }),
    }),
  };
  window.__calls = [];
  function call(input, opts, json) {
    return new Promise((res, rej) => {
      const c = { id: window.__calls.length, input, opts: opts || {}, json, done: false, res, rej };
      window.__calls.push(c);
      if (opts && opts.signal) opts.signal.addEventListener('abort', () => { if (!c.done) { c.done = true; rej(Object.assign(new Error('aborted'), { name: 'AbortError', code: 'aborted' })); } });
    });
  }
  const sample = (input, opts) => call(input, opts, false);
  sample.json = (input, opts) => call(input, opts, true);
  sample.limits = async () => ({});
  window.__pending = () => window.__calls.filter((c) => !c.done).map((c) => ({ id: c.id, json: c.json, input: typeof c.input === 'string' ? c.input : JSON.stringify(c.input) }));
  window.__answer = (id, text) => {
    const c = window.__calls[id]; if (!c || c.done) return 'no such pending call';
    c.done = true;
    if (c.json) { try { c.res(typeof text === 'string' ? JSON.parse(text) : text); } catch (e) { c.rej(e); } }
    else { try { c.opts.onText && c.opts.onText({ text }); } catch (e) {} c.res({ text }); }
    return 'ok';
  };
  window.__reset = () => { localStorage.removeItem(RUN); localStorage.removeItem(RUN + ':skew'); localStorage.removeItem(RUN + ':skipped'); location.reload(); };
  window.claude = { use: async (n) => n === 'db' ? db : n === 'user' ? { id: async () => 'tester' } : n === 'sample' ? sample : null };
})();
</script>
"""


def seed_for(ids):
    seed = {}
    with tempfile.TemporaryDirectory() as tmp:
        for u in ids:
            r = subprocess.run([sys.executable, '-I', os.path.join(HERE, 'content-check.py'), '--upload', u, '--out', tmp],
                               capture_output=True, text=True)
            got = False
            for name, key in ((f'{u}--v3.lesson.json', f'lessons/{u}--v3'), (f'{u}.cards.json', f'cards/{u}'), (f'{u}.quiz.json', f'quiz/{u}')):
                fp = os.path.join(tmp, name)
                if os.path.exists(fp):
                    seed[key] = json.load(open(fp, encoding='utf-8'))
                    got = True
            if not got:
                print(f'{u}: 올릴 파일을 만들지 못했다(content-check 오류)\n{r.stdout[-400:]}', file=sys.stderr)
    return seed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('ids', nargs='*')
    ap.add_argument('--out', required=True)
    ap.add_argument('--state')
    ap.add_argument('--run', default='play')
    o = ap.parse_args()
    ids = o.ids or sorted(x for x in os.listdir(CONTENT) if os.path.isfile(os.path.join(CONTENT, x, 'lesson.md')))
    seed = seed_for(ids)
    init = json.load(open(o.state, encoding='utf-8')) if o.state else {}
    app = open(APP, encoding='utf-8').read()
    mock = (MOCK.replace('__SEED__', json.dumps(seed, ensure_ascii=False).replace('</', '<\\/'))
                .replace('__INIT__', json.dumps(init, ensure_ascii=False).replace('</', '<\\/'))
                .replace('__RUN__', json.dumps(o.run)))
    os.makedirs(o.out, exist_ok=True)
    out = os.path.join(o.out, 'play-app.html')
    open(out, 'w', encoding='utf-8').write(mock + app)
    src_img = os.path.join(REPO, 'app', 'img')
    if os.path.isdir(src_img):
        shutil.copytree(src_img, os.path.join(o.out, 'img'), dirs_exist_ok=True)
    print(f'{len(seed)}개 문서 → {out}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
