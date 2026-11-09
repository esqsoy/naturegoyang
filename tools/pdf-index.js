// 교과서 PDF 색인 도구 (macOS 내장 PDFKit, 설치할 것 없음)
//
//   osascript -l JavaScript tools/pdf-index.js info    <pdf>
//   osascript -l JavaScript tools/pdf-index.js outline <pdf> <out.json>
//   osascript -l JavaScript tools/pdf-index.js text    <pdf> <out.txt> [첫쪽] [끝쪽]
//   osascript -l JavaScript tools/pdf-index.js png     <pdf> <쪽> <out.png|out.jpg> [가로px=1400]
//   osascript -l JavaScript tools/pdf-index.js ocr     <pdf> <out.txt> [첫쪽] [끝쪽] [가로px=1800]   (스캔본)
//
// 쪽 번호는 모두 PDF 쪽 순서(1부터)다. 책에 찍힌 쪽 번호는 label로 따로 적는다.
// text는 쪽마다 "\f=== p.<쪽> [<label>] ===" 줄로 나눈다. grep으로 찾고 그 쪽만 읽으면 된다.
// png는 큰 PDF를 통째로 열지 않고 한 쪽만 줄여서 그린다(그림·수식 확인용).
// 결과물(목차·글자·그림)은 원문이라 공개 저장소에 넣지 않는다. 비공개 폴더에 둔다.

ObjC.import('Foundation');
ObjC.import('PDFKit');
ObjC.import('AppKit');
ObjC.import('Vision');

function openDoc(path) {
  var doc = $.PDFDocument.alloc.initWithURL($.NSURL.fileURLWithPath(path));
  if (!doc || (doc.isNil && doc.isNil())) throw new Error('PDF를 열 수 없다: ' + path);
  return doc;
}

function str(x) { return (x && !(x.isNil && x.isNil())) ? ObjC.unwrap(x) : ''; }

function write(path, s) {
  var ok = $(s).writeToFileAtomicallyEncodingError(path, true, $.NSUTF8StringEncoding, null);
  if (!ok) throw new Error('쓸 수 없다: ' + path);
}

function pageInfo(doc, page) {
  if (!page || (page.isNil && page.isNil())) return null;
  return { page: Number(doc.indexForPage(page)) + 1, label: str(page.label) };
}

function walk(doc, node, level, out) {
  var n = Number(node.numberOfChildren);
  for (var i = 0; i < n; i++) {
    var c = node.childAtIndex(i);
    var dest = c.destination;
    var p = (dest && !(dest.isNil && dest.isNil())) ? pageInfo(doc, dest.page) : null;
    out.push({ level: level, title: str(c.label).replace(/\s+/g, ' ').trim(), page: p ? p.page : null, label: p ? p.label : '' });
    walk(doc, c, level + 1, out);
  }
}

function run(argv) {
  var mode = argv[0], pdf = argv[1];
  if (!mode || !pdf) return '쓰는 법은 파일 맨 위 주석을 본다.';
  var doc = openDoc(pdf);
  var n = Number(doc.pageCount); // PDFKit 숫자가 글자로 넘어올 때가 있어 숫자로 바꾼다

  if (mode === 'info') {
    var root = doc.outlineRoot;
    var hasOutline = !!(root && !(root.isNil && root.isNil()) && root.numberOfChildren > 0);
    var b = doc.pageAtIndex(0).boundsForBox(0);
    return JSON.stringify({ pages: n, outline: hasOutline, firstLabel: str(doc.pageAtIndex(0).label),
      size: [Math.round(b.size.width), Math.round(b.size.height)] });
  }

  if (mode === 'outline') {
    var out = [];
    var r = doc.outlineRoot;
    if (r && !(r.isNil && r.isNil())) walk(doc, r, 0, out);
    write(argv[2], JSON.stringify({ pages: n, entries: out }, null, 1));
    return 'outline ' + out.length + '항목 → ' + argv[2];
  }

  if (mode === 'text') {
    var a = argv[3] ? parseInt(argv[3], 10) : 1, z = argv[4] ? parseInt(argv[4], 10) : n;
    var parts = [], chars = 0, empty = 0;
    for (var i = a; i <= Math.min(z, n); i++) {
      var pg = doc.pageAtIndex(i - 1);
      var s = str(pg.string);
      if (!s.trim()) empty++;
      chars += s.length;
      parts.push('\f=== p.' + i + ' [' + str(pg.label) + '] ===\n' + s);
    }
    write(argv[2], parts.join('\n'));
    return 'text ' + a + '-' + Math.min(z, n) + '쪽, ' + chars + '자, 글자 없는 쪽 ' + empty + ' → ' + argv[2];
  }

  if (mode === 'png') {
    var k = parseInt(argv[2], 10), outp = argv[3], w = argv[4] ? parseInt(argv[4], 10) : 1400;
    var page = doc.pageAtIndex(k - 1);
    var bb = page.boundsForBox(0);
    var h = Math.round(w * bb.size.height / bb.size.width);
    var img = page.thumbnailOfSizeForBox($.NSMakeSize(w, h), 0);
    var rep = $.NSBitmapImageRep.imageRepWithData(img.TIFFRepresentation);
    var jpg = /\.jpe?g$/i.test(outp);
    var props = jpg ? $({ NSImageCompressionFactor: 0.8 }) : $({});
    var data = rep.representationUsingTypeProperties(jpg ? 3 : 4, props);
    data.writeToFileAtomically(outp, true);
    return 'p.' + k + ' ' + w + 'x' + h + ' → ' + outp;
  }

  if (mode === 'ocr') {
    // 스캔본(글자 층 없음)용. 쪽을 그려 macOS Vision으로 글자를 읽는다(한국어·영어).
    var outo = argv[2], a2 = argv[3] ? parseInt(argv[3], 10) : 1, z2 = argv[4] ? parseInt(argv[4], 10) : n;
    var width = argv[5] ? parseInt(argv[5], 10) : 1800;
    var parts2 = [], chars2 = 0;
    for (var p = a2; p <= Math.min(z2, n); p++) {
      var pg2 = doc.pageAtIndex(p - 1);
      var b2 = pg2.boundsForBox(0);
      var h2 = Math.round(width * b2.size.height / b2.size.width);
      var im2 = pg2.thumbnailOfSizeForBox($.NSMakeSize(width, h2), 0);
      var handler = $.VNImageRequestHandler.alloc.initWithDataOptions(im2.TIFFRepresentation, $.NSDictionary.dictionary);
      var req = $.VNRecognizeTextRequest.alloc.init;
      req.recognitionLanguages = $(['ko-KR', 'en-US']);
      req.recognitionLevel = 0; // 정확하게
      req.usesLanguageCorrection = true;
      handler.performRequestsError($([req]), null);
      var res = req.results, lines = [];
      var cnt = (res && !(res.isNil && res.isNil())) ? Number(res.count) : 0;
      for (var r = 0; r < cnt; r++) {
        var obs = res.objectAtIndex(r);
        var cand = obs.topCandidates(1);
        if (Number(cand.count) < 1) continue;
        var bb2 = obs.boundingBox;
        lines.push({ y: bb2.origin.y + bb2.size.height, x: bb2.origin.x, s: str(cand.objectAtIndex(0).string) });
      }
      // 위에서 아래로, 같은 줄이면 왼쪽부터 (두 단 편집은 단마다 섞일 수 있다)
      lines.sort(function (u, v) { return Math.abs(u.y - v.y) > 0.012 ? v.y - u.y : u.x - v.x; });
      var s2 = lines.map(function (l) { return l.s; }).join('\n');
      chars2 += s2.length;
      parts2.push('\f=== p.' + p + ' [' + str(pg2.label) + '] ===\n' + s2);
    }
    write(outo, parts2.join('\n'));
    return 'ocr ' + a2 + '-' + Math.min(z2, n) + '쪽, ' + chars2 + '자 → ' + outo;
  }

  return '모르는 mode: ' + mode;
}
