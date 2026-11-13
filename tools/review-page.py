#!/usr/bin/env python3
"""영신 검수 페이지(Artifact용 HTML)를 content/에서 만든다.

    python3 -I tools/review-page.py --out <파일.html> [단원 id ...]   # 없으면 content/ 전부

Artifact로 올릴 때: capabilities {"comments": {"composer_only": true}} (댓글 쓰기 창만 연다).
같은 Artifact 주소에 다시 올린다(HANDOFF·DEPLOYMENT에 주소).
"""
import argparse
import html
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CONTENT = os.path.join(REPO, 'content')

_spec = importlib.util.spec_from_file_location('cc', os.path.join(HERE, 'content-check.py'))
cc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cc)

DOMAIN = {'F': '기초 도구', 'P': '물리', 'C': '화학', 'B': '생명과학', 'E': '지구·우주'}
LAYER_CLS = {'직관': 'int', '통상': 'std', '엄밀': 'rig'}


def esc(s):
    return html.escape(s, quote=True)


def inline(s, by, num):
    """굵게, [[id]], $수식$을 HTML로. 수식은 data-tex로 두고 브라우저에서 KaTeX로 그린다."""
    out, i = [], 0
    for m in re.finditer(r'\$([^$\n]+)\$|\[\[([a-z]+-[a-z]+)(?:\|([^\]]*))?\]\]', s):
        out.append(_bold(esc(s[i:m.start()])))
        if m.group(1) is not None:
            out.append(f'<span class="tex" data-tex="{esc(m.group(1))}">{esc(m.group(1))}</span>')
        else:
            x, lab = m.group(2), m.group(3)
            t = by[x]['t'] if x in by else x
            if lab == '#':  # [[id|#]]: 앱처럼 지금 번호만 (26.11.14)
                out.append(f'<span class="xref" title="{esc(t)}">{num.get(x, "?")}번</span>')
            else:
                out.append(f'<span class="xref">{num.get(x, "?")} {esc(lab or t)}</span>')
        i = m.end()
    out.append(_bold(esc(s[i:])))
    return ''.join(out)


def _bold(s):
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)


def md_to_html(md, by, num, target_prefix):
    """설명 마크다운(앱과 같은 꼴)을 HTML로. 큰 덩어리마다 댓글 대상을 단다."""
    lines = md.replace('\r', '').split('\n')
    out, para, lst, tbl = [], [], None, []
    blk = [0]

    def flush_para():
        if para:
            out.append('<p>' + inline(' '.join(para), by, num) + '</p>')
            para.clear()

    def flush_list():
        nonlocal lst
        if lst:
            tag = lst[0]
            out.append(f'<{tag}>' + ''.join(f'<li>{inline(x, by, num)}</li>' for x in lst[1]) + f'</{tag}>')
            lst = None

    def flush_tbl():
        if tbl:
            rows = [r for r in tbl if not re.match(r'^\|\s*:?-{2,}', r)]
            cells = [[c.strip().replace('\x03', '|') for c in re.sub(r'\[\[([a-z]+-[a-z]+)\|', '[[\\1\x03', r.strip().strip('|')).split('|')] for r in rows]
            h = ''.join(f'<th>{inline(c, by, num)}</th>' for c in cells[0])
            b = ''.join('<tr>' + ''.join(f'<td>{inline(c, by, num)}</td>' for c in r) + '</tr>' for r in cells[1:])
            out.append(f'<div class="tbl"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>')
            tbl.clear()

    def flush():
        flush_para(); flush_list(); flush_tbl()

    open_block = [False]

    def start_block(kind, title):
        flush()
        if open_block[0]:
            out.append('</section>')
        blk[0] += 1
        out.append(f'<section class="blk {kind}" data-comment-target id="{target_prefix}-b{blk[0]}">'
                   f'<button type="button" class="cbtn" data-comment aria-label="이 덩어리에 댓글">댓글</button>')
        open_block[0] = True

    for raw in lines:
        l = raw.strip()
        m = re.match(r'^(#{2,4})\s+(.*)$', l)
        if m:
            lv, t = len(m.group(1)), m.group(2).strip()
            if lv == 2:
                start_block('h2blk', t)
                out.append(f'<h3 class="sec">{esc(t)}</h3>')
            elif lv == 3:
                flush()
                out.append(f'<h4 class="obj">{inline(t, by, num)}</h4>')
            else:
                if t.startswith('점검'):
                    start_block('check', t)
                    out.append('<p class="lyh"><span class="ly chk">점검</span></p>')
                else:
                    parts = t.split('·')
                    cls = LAYER_CLS.get(parts[-1], 'std')
                    start_block('layer l-' + cls, t)
                    out.append('<p class="lyh">' + '<span class="eq">=</span>'.join(f'<span class="ly">{esc(p)}</span>' for p in parts) + '</p>')
            continue
        if l.startswith('$$') and l.endswith('$$') and len(l) > 4:
            flush()
            out.append(f'<div class="mblock"><span class="tex" data-display="1" data-tex="{esc(l[2:-2].strip())}">{esc(l)}</span></div>')
            continue
        if l.startswith('|'):
            flush_para(); flush_list(); tbl.append(l); continue
        mm = re.match(r'^[-*]\s+(.*)$', l)
        if mm:
            flush_para(); flush_tbl()
            if not lst or lst[0] != 'ul':
                flush_list(); lst = ['ul', []]
            lst[1].append(mm.group(1)); continue
        mm = re.match(r'^(\d+)[.)]\s+(.*)$', l)
        if mm:
            flush_para(); flush_tbl()
            if not lst or lst[0] != 'ol':
                flush_list(); lst = ['ol', []]
            lst[1].append(mm.group(2)); continue
        if not l:
            flush(); continue
        if not open_block[0]:
            start_block('h2blk', '')
        flush_list(); flush_tbl(); para.append(l)
    flush()
    if open_block[0]:
        out.append('</section>')
    return '\n'.join(out)


def check_to_html(src, by, num, uid):
    secs = re.split(r'^## ', src, flags=re.M)
    head = secs[0]
    st = re.search(r'^상태:\s*(.*)$', head, re.M)
    tb = re.search(r'^교과서:\s*(.*)$', head, re.M)
    body = []
    for s in secs[1:]:
        title, _, rest = s.partition('\n')
        items = [l[2:] for l in rest.split('\n') if l.startswith('- ')]
        paras = [l for l in rest.split('\n') if l.strip() and not l.startswith('- ')]
        inner = ''.join(f'<p>{inline(p, by, num)}</p>' for p in paras)
        if items:
            inner += '<ul>' + ''.join(f'<li>{inline(i, by, num)}</li>' for i in items) + '</ul>'
        body.append(f'<section class="chk-sec" data-comment-target id="{uid}-k-{len(body)}">'
                    f'<button type="button" class="cbtn" data-comment aria-label="이 기록에 댓글">댓글</button>'
                    f'<h4>{esc(title.strip())}</h4>{inner}</section>')
    note = [l for l in head.split('\n')[1:] if l.strip() and not l.startswith(('상태:', '교과서:', '# '))]
    return (st.group(1).strip() if st else '?', tb.group(1).strip() if tb else '',
            ''.join(f'<p class="note">{inline(n, by, num)}</p>' for n in note) + ''.join(body))


def build(ids):
    nodes, by, unlocks, num = cc.load_nodes()
    units = []
    for uid in ids:
        d = os.path.join(CONTENT, uid)
        md = open(os.path.join(d, 'lesson.md'), encoding='utf-8').read()
        cards = json.load(open(os.path.join(d, 'cards.json'), encoding='utf-8'))
        ck = open(os.path.join(d, 'check.md'), encoding='utf-8').read()
        st, tb, ckh = check_to_html(ck, by, num, uid)
        n = by[uid]
        live = [c for c in cards if not c.get('x')]
        rows = ''.join(
            f'<tr data-comment-target id="{uid}-{esc(c["id"])}"><td class="cid">{esc(c["id"])}</td>'
            f'<td><span class="kind k-{esc(c["k"])}">{esc(c["k"])}</span></td>'
            f'<td class="cq">{inline(c["q"], by, num)}</td><td class="ca">{inline(c["a"], by, num)}'
            + (f'<div class="ch">{inline(c["h"], by, num)}</div>' if c.get('h') else '') +
            f'</td><td><button type="button" class="cbtn in" data-comment aria-label="{esc(c["id"])} 카드에 댓글">댓글</button></td></tr>'
            for c in live)
        nterm = sum(1 for c in live if c['k'] == '용어')
        units.append(dict(id=uid, no=num.get(uid, 0), t=n['t'], q=n['q'], d=DOMAIN[n['d']], obj=n['obj'], st=st, tb=tb,
                          lesson=md_to_html(md, by, num, uid), rows=rows, ncards=len(live) - nterm, nterm=nterm,
                          chars=len(md), check=ckh))
    units.sort(key=lambda u: u['no'])
    return units


PAGE = r'''<title>과학고양 내용 검수</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans+KR:wght@400;500;600;700&family=Noto+Serif+KR:wght@400;600;700&display=swap">
<script src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js"></script>
<style>
/* 검수용 한 줄 읽기: 위에 단원 띠, 아래로 단원마다 설명 → 카드 → 대조 기록. 앱과 같은 글꼴·영역 색. */
:root{
  --bg:#EEF0F3; --surface:#FFFFFF; --sunk:#F5F6F8; --ink:#141B24; --ink-2:#4A5666; --ink-3:#7D8897; --line:#D3D9E1;
  --accent:#5A687B; --good:#1B7F47; --warn:#9A620C; --focus:#2457E6;
  --ui:"IBM Plex Sans KR","Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif;
  --read:"Noto Serif KR","AppleMyungjo","Batang",serif; --mono:"IBM Plex Mono",ui-monospace,Menlo,monospace;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
  --bg:#0E1319; --surface:#161D26; --sunk:#1C2531; --ink:#E5EBF2; --ink-2:#A6B1BF; --ink-3:#6F7C8B; --line:#2C3746;
  --accent:#9AA8BA; --good:#4CC57E; --warn:#E2A93F; --focus:#86A8FF; color-scheme:dark }}
:root[data-theme="dark"]{
  --bg:#0E1319; --surface:#161D26; --sunk:#1C2531; --ink:#E5EBF2; --ink-2:#A6B1BF; --ink-3:#6F7C8B; --line:#2C3746;
  --accent:#9AA8BA; --good:#4CC57E; --warn:#E2A93F; --focus:#86A8FF; color-scheme:dark }
*{box-sizing:border-box}
body{background:var(--bg); color:var(--ink); font:15px/1.65 var(--ui); -webkit-font-smoothing:antialiased}
body::before{content:""; position:fixed; inset:0 0 auto; height:env(safe-area-inset-top,0px); z-index:10; background:var(--surface)}
:focus-visible{outline:2px solid var(--focus); outline-offset:2px}
h1,h2,h3,h4{text-wrap:balance}
.bar{position:sticky; top:env(safe-area-inset-top,0px); z-index:5; background:var(--surface); border-bottom:1px solid var(--line)}
.bar-in{max-width:980px; margin:0 auto; padding-block:10px; padding-left:max(16px,env(safe-area-inset-left,0px)); padding-right:max(16px,env(safe-area-inset-right,0px)); display:flex; flex-wrap:wrap; gap:8px 16px; align-items:center}
.brand{font:700 15px/1.2 var(--ui); margin:0}
.chips{display:flex; flex-wrap:wrap; gap:6px; margin-left:auto}
.chip{display:inline-flex; gap:6px; align-items:center; padding:5px 10px; border:1px solid var(--line); border-radius:6px; color:var(--ink); text-decoration:none; font:500 13px/1.2 var(--ui); background:var(--surface)}
.chip b{font:600 12px var(--mono)}
.chip:hover{border-color:var(--accent)}
main{max-width:980px; margin:0 auto; padding-block:24px 80px; padding-left:max(16px,env(safe-area-inset-left,0px)); padding-right:max(16px,env(safe-area-inset-right,0px)); display:grid; gap:40px}
.intro{display:grid; gap:8px; max-width:68ch}
.intro h1{font:700 clamp(22px,3vw,28px)/1.3 var(--ui); margin:0}
.intro p{margin:0; color:var(--ink-2)}
.unit{display:grid; gap:18px; scroll-margin-top:72px}
.uhead{display:grid; grid-template-columns:auto minmax(0,1fr); gap:16px; align-items:center}
.tile{width:64px; height:70px; border:1.5px solid var(--accent); border-radius:4px; display:flex; flex-direction:column; justify-content:space-between; padding:5px 7px; background:var(--surface)}
.tile .no{font:500 11px var(--mono); color:var(--ink-3)}
.tile .dm{font:600 11px var(--ui); color:var(--accent)}
.uhead h2{font:700 21px/1.3 var(--ui); margin:0}
.uq{font:600 16px/1.6 var(--read); color:var(--ink-2); margin:2px 0 0}
.meta{display:flex; flex-wrap:wrap; gap:6px; margin-top:6px}
.pill{font:600 12px/1 var(--ui); padding:5px 8px; border-radius:99px; background:var(--sunk); color:var(--ink-2); border:1px solid var(--line)}
.pill.st{background:color-mix(in srgb,var(--warn) 14%,var(--surface)); color:var(--warn); border-color:transparent}
.pill.st.done{background:color-mix(in srgb,var(--good) 14%,var(--surface)); color:var(--good)}
.tabs{display:flex; gap:4px; border-bottom:1px solid var(--line)}
.tab{appearance:none; border:0; background:none; padding:8px 12px; font:500 14px/1 var(--ui); color:var(--ink-2); cursor:pointer; border-radius:6px 6px 0 0}
.tab[aria-selected="true"]{color:var(--ink); font-weight:700; box-shadow:inset 0 -2px 0 var(--ink)}
.panel{min-width:0}
.lesson{display:grid; gap:12px; max-width:74ch}
.blk{position:relative; background:var(--surface); border:1px solid var(--line); border-radius:8px; padding:14px 16px 12px; font:16px/1.85 var(--read); min-width:0; overflow-wrap:break-word}
.blk p{margin:0 0 .8em} .blk ul,.blk ol{margin:0 0 .8em; padding-left:1.3em} .blk li{margin:.25em 0}
.blk.layer{border-left:4px solid var(--line)}
.blk.l-int{border-left-color:color-mix(in srgb,var(--accent) 35%,var(--surface))}
.blk.l-std{border-left-color:color-mix(in srgb,var(--accent) 75%,var(--surface))}
.blk.l-rig{border-left-color:var(--ink)}
.blk.check{background:var(--sunk)}
.sec{font:700 17px/1.3 var(--ui); margin:0 0 8px}
.obj{font:700 15px/1.4 var(--ui); margin:4px 0 8px; color:var(--ink)}
.lyh{display:flex; gap:6px; align-items:center; margin:0 0 6px}
.ly{font:600 11.5px/1 var(--ui); padding:4px 7px; border-radius:4px; background:var(--sunk); color:var(--ink-2)}
.ly.chk{background:var(--ink); color:var(--surface)}
.eq{font:500 12px var(--mono); color:var(--ink-3)}
.mblock{overflow-x:auto; margin:.4em 0 .9em}
.tbl{overflow-x:auto; margin:.4em 0 .9em}
table{border-collapse:collapse; font:14px/1.55 var(--ui)}
th,td{border-bottom:1px solid var(--line); padding:7px 10px 7px 0; text-align:left; vertical-align:top}
th{font-weight:700}
.xref{font:600 .85em/1.6 var(--ui); padding:1px 6px; border:1px solid var(--line); border-radius:4px; white-space:nowrap}
math{font-size:1.05em}
.cbtn{position:absolute; top:8px; right:8px; appearance:none; border:1px solid var(--line); background:var(--surface); color:var(--ink-3); font:500 12px/1 var(--ui); padding:5px 8px; border-radius:5px; cursor:pointer; opacity:.7}
.cbtn:hover{opacity:1; color:var(--ink); border-color:var(--ink-3)}
.cbtn.in{position:static}
.cards{width:100%}
.cards td{font-size:14.5px}
.cid{font:500 12px var(--mono); color:var(--ink-3); white-space:nowrap}
.cq{font-weight:600; min-width:9em}
.ca{min-width:12em}
.ch{color:var(--ink-3); font-size:13px; margin-top:3px}
.kind{font:600 11.5px/1 var(--ui); padding:4px 6px; border-radius:4px; background:var(--sunk); color:var(--ink-2); white-space:nowrap}
.k-용어{background:color-mix(in srgb,var(--accent) 18%,var(--surface)); color:var(--ink)}
.chk-sec{position:relative; background:var(--surface); border:1px solid var(--line); border-radius:8px; padding:12px 16px; margin-bottom:10px}
.chk-sec h4{font:700 14px var(--ui); margin:0 0 6px}
.chk-sec ul{margin:0; padding-left:1.2em} .chk-sec p{margin:0 0 .5em}
.note{color:var(--ink-2); font-size:14px; margin:0 0 10px}
.hint{font-size:13px; color:var(--ink-3)}
@media (max-width:640px){ .cq,.ca{min-width:0} .cards td:first-child{display:none} }
@media (prefers-reduced-motion: reduce){ *{scroll-behavior:auto} }
</style>
<header class="bar"><div class="bar-in"><p class="brand">과학고양 내용 검수</p><nav class="chips" aria-label="단원">__CHIPS__</nav></div></header>
<main>
<section class="intro"><h1>미리 만든 설명·카드 검수</h1>
<p>읽다가 어색한 문장, 헷갈리는 설명, 길이, 한자·영어 표기에 '댓글'을 달아 줘. 과학 내용은 교과서로 대조했고 대조 기록 탭에 근거가 있어. 댓글은 Claude가 읽고 고쳐서 같은 주소에 다시 올린다.</p>
<p class="hint">__GEN__</p></section>
__UNITS__
</main>
<script>
'use strict';
function drawMath(root){
  if(!window.katex) return;
  root.querySelectorAll('.tex[data-tex]').forEach(function(el){
    if(el.dataset.done) return;
    try{ el.innerHTML = katex.renderToString(el.dataset.tex,{displayMode:!!el.dataset.display, output:'mathml', throwOnError:false, strict:'ignore'}); el.dataset.done='1'; }catch(e){}
  });
}
document.addEventListener('click', function(ev){
  var t = ev.target.closest('.tab');
  if(t){
    var u = t.closest('.unit');
    u.querySelectorAll('.tab').forEach(function(b){ b.setAttribute('aria-selected', b===t?'true':'false'); });
    u.querySelectorAll('.panel').forEach(function(p){ p.hidden = p.id !== t.getAttribute('aria-controls'); });
    try{ localStorage.setItem('tab-'+u.id, t.getAttribute('aria-controls')); }catch(e){}
    return;
  }
  var c = ev.target.closest('[data-comment]');
  if(c){
    var target = c.closest('[data-comment-target]');
    var cm = window.__cm;
    if(!cm){ c.textContent = '댓글 모드로 달아 줘'; return; }
    cm.openComposer({element: target}).catch(function(e){ if(e && e.code==='unavailable'){ document.querySelectorAll('[data-comment]').forEach(function(b){ b.hidden = true; }); } });
  }
});
document.querySelectorAll('.unit').forEach(function(u){
  var saved = null; try{ saved = localStorage.getItem('tab-'+u.id); }catch(e){}
  if(saved){ var b = u.querySelector('.tab[aria-controls="'+saved+'"]'); if(b) b.click(); }
});
drawMath(document);
window.addEventListener('load', function(){ drawMath(document); });
if(window.claude && window.claude.use){
  window.claude.use('comments').then(function(cm){ window.__cm = cm; if(!cm){ document.querySelectorAll('[data-comment]').forEach(function(b){ b.hidden = true; }); } });
}
</script>
'''


def render(units, gen):
    chips = ''.join(f'<a class="chip" href="#u-{u["id"]}"><b>{u["no"]}</b>{esc(u["t"])}</a>' for u in units)
    blocks = []
    for u in units:
        done = 'done' if '영신 검수 끝' in u['st'] else ''
        obj = ''.join(f'<li>{esc(o)}</li>' for o in u['obj'])
        blocks.append(f'''<article class="unit" id="u-{u["id"]}">
<div class="uhead"><div class="tile" aria-hidden="true"><span class="no">{u["no"]}</span><span class="dm">{esc(u["d"])}</span></div>
<div><h2>{u["no"]}. {esc(u["t"])}</h2><p class="uq">{esc(u["q"])}</p>
<div class="meta"><span class="pill st {done}">{esc(u["st"])}</span><span class="pill">설명 {u["chars"]:,}자</span><span class="pill">카드 {u["ncards"]} + 용어 {u["nterm"]}</span></div></div></div>
<div class="tabs" role="tablist"><button type="button" class="tab" role="tab" aria-selected="true" aria-controls="{u["id"]}-p1">설명</button><button type="button" class="tab" role="tab" aria-selected="false" aria-controls="{u["id"]}-p2">카드</button><button type="button" class="tab" role="tab" aria-selected="false" aria-controls="{u["id"]}-p3">대조 기록</button></div>
<div class="panel" id="{u["id"]}-p1" role="tabpanel"><div class="lesson">{u["lesson"]}</div></div>
<div class="panel" id="{u["id"]}-p2" role="tabpanel" hidden><div class="tbl"><table class="cards"><thead><tr><th>id</th><th>종류</th><th>앞면</th><th>뒷면</th><th></th></tr></thead><tbody>{u["rows"]}</tbody></table></div></div>
<div class="panel" id="{u["id"]}-p3" role="tabpanel" hidden><p class="note">교과서: {esc(u["tb"])}</p><p class="note">학습 목표</p><ol class="note">{obj}</ol>{u["check"]}</div>
</article>''')
    return PAGE.replace('__CHIPS__', chips).replace('__UNITS__', '\n'.join(blocks)).replace('__GEN__', esc(gen))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('ids', nargs='*')
    ap.add_argument('--out', required=True)
    o = ap.parse_args()
    ids = o.ids or [x for x in os.listdir(CONTENT) if os.path.isfile(os.path.join(CONTENT, x, 'lesson.md'))]
    units = build(ids)
    import datetime
    gen = f'{datetime.date.today().isoformat()} · 단원 {len(units)}개 · 원본 content/ (esqsoy/naturegoyang)'
    open(o.out, 'w', encoding='utf-8').write(render(units, gen))
    print(f'{len(units)}단원 → {o.out} ({os.path.getsize(o.out):,} bytes)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
