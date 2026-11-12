# 작업자 안내

과학고양 저장소에서 일하는 세션이 먼저 읽는 문서다.

## 읽는 순서

AGENTS.md → [PRINCIPLES](PRINCIPLES.md)(결정과 그 이유) → [HANDOFF](HANDOFF.md)(지금 상태·대기 중인 일) → [WORK_LOG](WORK_LOG.md)(경위) → [DEPLOYMENT](DEPLOYMENT.md)(실제 공개된 것). 시리즈 공통 원칙은 tangogoyang PRINCIPLES 0절과 palagoyang goyang-common/에 있다.

## 대화

- 영신에게는 한국어 반말.
- 영신은 '영신초이'다. 부를 때는 "초이!"·"영신 쪼이!".
- 영신의 말은 의견이고 Claude가 주도해도 된다(PRINCIPLES 0). 그래도 아래 '바꾸지 않는 것'은 영신 결정이다.

## 바꾸지 않는 것 (바꾸려면 영신에게 먼저 묻는다)

- 빠진 계단 없이: 단원이 쓰는 도구는 반드시 앞 단원에서 얻고, 길은 하나뿐이다(따로 도는 트랙 없음)(PRINCIPLES 0, 1).
- 숙달은 확인 문제 100점, 카드 전부 떠올리기, 그 단원 교재 문제 전부(PRINCIPLES 2-3, 2-4, 2-5. 교재 문제는 26.11.13 결정, 설계 중).
- 단계 잠금과 인정·건너뛰기 없음, 이어하기와 골라서 하기(PRINCIPLES 3).
- 설명은 직관·통상·엄밀을 같이, 한 장씩 읽기, 버튼 자리 고정(PRINCIPLES 2-1, 2-2).
- 뒤 단원 개념도 써서 정확하게(순서 통제 없음), 용어 한글(漢字, English), 정의 완결·한정어 보존(PRINCIPLES 2-1, 2-1-1).
- 틀린 것은 따라 쓰고, 카드는 보지 않고 다시 써야 끝난다(PRINCIPLES 2-3).
- 단원을 더하거나 뺄 때는 영신 의견을 먼저 받는다(시리즈 공통).

## 일하는 법

- **시작할 때 `git pull`.** 맥미니와 Windows PC 두 곳에서 일한다. 받지 않고 작업하면 다른 쪽 결정과 어긋난다(26.11.13).
- **설명·카드는 미리 만들어 검수한다(PRINCIPLES 5, 26.11.09).** 원본은 `content/<단원 id>/`(lesson.md, cards.json, check.md), 형식은 [content/README](content/README.md). 순서: 초안 → 교과서 대조(`tools/unit-sources.py <id> --text`) → `python3 -I tools/content-check.py <id>` 오류 0 → `--upload <id> --out <폴더>`로 만든 JSON을 ArtifactData `batch`로 `lessons/<id>--v3`, `cards/<id>`에 올림(덮어쓸 때는 받은 판을 `if_version`으로) → 검수 페이지 다시 올림(`tools/review-page.py`) → DEPLOYMENT에 판 번호.
  - 영신이 그 단원에 닿기 전에 올린다. 앱은 저장소에 설명·카드가 없을 때만 그 자리에서 만든다.
  - 카드 id는 기록 열쇠다. 올린 카드의 id·뜻은 바꾸지 않고, 새 카드는 끝 번호 뒤에, 뺄 카드는 `"x": true`.
  - 영신의 검수 댓글은 검수 페이지 Artifact에 달린다. 고친 것은 check.md와 WORK_LOG에 적는다.
- 앱 원본은 `app/naturegoyang.html` 한 파일이다. 단원 데이터(`N(...)` 줄), 생성 지시(프롬프트), 화면이 모두 들어 있다.
- 고친 뒤에는 claude.ai Artifact에 **같은 주소**로 다시 올린다(DEPLOYMENT). 새 주소로 올리면 영신의 기록이 이어지지 않는다.
- 기록 열쇠: 단원 id(`f-measure` 등)와 카드 id(`c01`…)가 기록의 열쇠다. 단원 id를 바꾸지 않는다. 화면 번호는 열 때 계산하므로 단원을 더해도 기록은 그대로다.
- 설명 저장 열쇠는 `--v3`다(앱 `LESSON_VERS`). 미리 만든 설명도 여기에 올라가므로, 생성 지시를 바꿨다고 판을 올리지 않는다. 판을 올려야 하면 content/ 올림 도구와 같이 바꾸고 예전 판은 읽기 대체로 남긴다(26.11.13, 6판에서 `--v4`로 올렸다가 7판에서 되돌림).
- 결정을 하면 PRINCIPLES에 "왜"와 날짜, 영신의 말을 남긴다. 한 일은 WORK_LOG에, 지금 상태는 HANDOFF에, 올린 것은 DEPLOYMENT에 적는다.
- 저장소 파일에 모델 이름을 쓰지 않는다.
- 다른 고양 저장소는 읽기만 한다. 고칠 거리를 찾으면 '어느 저장소·어느 파일·무엇을·왜'로 정리해 영신에게 넘긴다.
- Artifact 저장소의 설명·카드(`lessons/`, `cards/`)를 직접 고칠 때는 먼저 비공개 폴더 `artifact-backup/<날짜>/`에 원본을 받아 두고, 읽던 쪽 앞은 건드리지 않는다(진도 `pos`가 쪽 순서다).

## 작업 환경 (26.11.09부터 맥미니)

- 저장소: 맥미니 iCloud Drive `10 언어/고양/naturegoyang/`(빨라고양 옆). 처음 저장소는 Windows PC에서 만들었다.
- 교과서: iCloud Drive `30 과학/`(영신 소장 PDF). **읽기만 한다.** 대조 원칙·책 목록·도구는 [sources/README](sources/README.md).
- 비공개 폴더: `10 언어/고양/비공개/과학고양/`(git 밖). 뽑은 목차·글자·쪽 그림, Artifact 백업. 안내는 그 폴더 README.
- 맥미니에는 node가 없다. PDF는 macOS 내장 PDFKit(`osascript -l JavaScript tools/pdf-index.js`)으로, 나머지 검사는 `python3 -I`로 한다.
- 큰 PDF(100MB 넘는 것)는 통째로 읽지 않는다. 쪽별 글자를 뽑아 grep으로 찾고, 그림이 필요한 쪽만 줄여 그린다(`pdf-index.js png <pdf> <쪽> <out.jpg> 1200`).
- iCloud에만 있는 파일(`ls -lO`에 `dataless`)은 샌드박스를 끄고 `brctl download <경로>`로 내려받는다. 안 내려오면 `killall bird`로 iCloud 데몬을 다시 띄운다(26.11.09에 이것으로 풀렸다, 비공개 폴더 README).
- 스캔본(글자 층 없음)은 `pdf-index.js ocr`로 읽는다(macOS Vision, 쪽당 약 4초). 두 단 편집은 줄이 섞일 수 있다.
