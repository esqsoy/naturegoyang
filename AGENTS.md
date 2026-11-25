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
- 숙달은 확인 문제 100점, 카드 전부 떠올리기, 그 단원 교재의 숙달 문제(책 답이 있는 쪽 번호) 전부. 짝꿍 문제는 섞어 풀기로 모두 풀어야 다음 단계가 열린다(PRINCIPLES 2-3, 2-4, 2-5. 26.11.13 결정, 26.11.25 영신 "홀수 숙달, 짝수는 섞어 복습").
- 단계 잠금과 인정·건너뛰기 없음, 이어하기와 골라서 하기(PRINCIPLES 3).
- 설명은 직관·통상·엄밀을 같이, 한 장씩 읽기, 버튼 자리 고정(PRINCIPLES 2-1, 2-2).
- 뒤 단원 개념도 써서 정확하게(순서 통제 없음), 용어 한글(漢字, English), 정의 완결·한정어 보존(PRINCIPLES 2-1, 2-1-1).
- 틀린 것은 따라 쓰고, 카드는 보지 않고 다시 써야 끝난다(PRINCIPLES 2-3).
- 단원을 더하거나 뺄 때는 영신 의견을 먼저 받는다(시리즈 공통).

## 일하는 법

- **시작할 때 `git pull`.** 맥미니와 Windows PC 두 곳에서 일한다. 받지 않고 작업하면 다른 쪽 결정과 어긋난다(26.11.13).
- **설명·카드는 미리 만들어 검수한다(PRINCIPLES 5, 26.11.09).** 원본은 `content/<단원 id>/`(lesson.md, cards.json, check.md, 확인 문제 은행 quiz.json), 형식은 [content/README](content/README.md). 순서: 초안 → 교과서 대조(`tools/unit-sources.py <id> --text`) → `python3 -I tools/content-check.py <id>` 오류 0 → `--upload <id> --out <폴더>`로 만든 JSON을 ArtifactData `batch`로 `lessons/<id>--v3`, `cards/<id>`, `quiz/<id>`에 올림(덮어쓸 때는 받은 판을 `if_version`으로) → 검수 페이지 다시 올림(`tools/review-page.py`) → DEPLOYMENT에 판 번호.
  - 영신이 그 단원에 닿기 전에 올린다. 앱은 저장소에 설명·카드가 없을 때만 그 자리에서 만든다.
  - 카드 id는 기록 열쇠다. 올린 카드의 id·뜻은 바꾸지 않고, 새 카드는 끝 번호 뒤에, 뺄 카드는 `"x": true`.
  - 다른 단원은 번호를 글로 적지 않고 `[[id|#]]`(앱이 지금 번호를 보인다)나 `[[id]]`로 가리킨다. 지도를 바꾸면 번호가 바뀐다(26.11.14, content/README).
- **지도(`N(...)` 줄)를 바꾸면** `python3 -I tools/curriculum.py`로 CURRICULUM.md를 다시 뽑는다. 단원을 더하거나 빼는 것은 영신 의견을 먼저 받는다.
- **큰 일은 서브에이전트 팀원과 나눠 한다(영신 26.11.14: "작업할때 이솝을 파트너로 협업해줘 모든 자원을 총동원해서 마스터피스를 만들어보자").** 조사·초안은 나누고, 합치고 정하고 검산하는 것은 Claude가 한다.
  - **팀 역할(26.11.26 과학 과제 면접, WORK_LOG):** 쓰기(설명 고침 초안, 확인 문제 은행)는 이솝(`judge`), 설명·카드 검토는 하산(`cross-checker`), 답을 가린 검산은 비루니(`ulpi`), 합치고 정하는 것은 콰리즈미(주 세션 Claude). 쓴 사람과 검산하는 사람은 다른 팀원이다. 영신이 "이솝만 말고 … 면접보고 팀을 구성해보는거 어때?"(26.11.26)라고 해서 같은 과제로 넷을 견주었다.
  - **플레이테스트(26.11.26):** 영신이 처음 플레이하기 전에 학습자 역할의 팀원(비루니)이 같은 과정을 앱 화면으로 먼저 밟는다(영신 "어차피 내가 플레이하는게 검수이자 학습이니까 첫 플레이하기전에 플레이할 부분을 팀원들이 한번 풀어보는건 어때", "푸는게 아니라 내가 할 그 과정을 그대로 따라가보는걸 말하는거야").
    - `python3 -I tools/playtest.py --out ~/naturegoyang-playtest --state <영신 진도 json> <단원 id…>`로 연습용 앱을 만든다. 가짜 저장소에 Claude 호출 대기열과 읽을 시간 앞당기기가 붙어 있다. 저장소 밖(iCloud 밖) 폴더에 두어야 로컬 서버가 읽는다.
    - 연습용 앱은 저장소 루트의 `.claude/launch.json`(CloudDocs) 설정 `naturegoyang-playtest`(8791번)로 띄운다.
    - 학습자 상태(의욕·스트레스·피로·자신감)를 들고 플레이한다(`design/playtest-human.md`, 영신 "'인간'의 설정 가중치를 주면 좋겠어").
    - 새 단원 흐름: 하산 검토 → 이솝 고침·은행 → 비루니 검산 → 콰리즈미 합치기 → **비루니 플레이테스트** → 고친 뒤 올림.
  - **과학고양의 팀 이름(26.11.26):** 법학고양의 법학자 이름(가이·파핀·울프)은 여기서 쓰지 않는다(영신 "여기서는 법학자들이름이어선 안되지 않을까?"). 합격한 셋이 두 차례 회의해 그리스 학자 안과 이슬람 황금기 과학자 안을 냈고, 영신이 이슬람 쪽을 골라 통용명을 정했다: "아이소포스, 이른바 이솝. 이븐 알하이삼 이른바 하산, 그리고 비루니, 콰리즈미 이렇게 부르는걸로 하겠습니다". 이솝은 시리즈 어디서나 이솝이다(영신 "이솝은 우화를 짓고 우화는 모든 이야기와 통용되거든"). 하산은 이븐 알하이삼의 자기 이름이다(라틴어 Alhazen도 여기서 왔다). '하이삼'만 부르면 할아버지 이름이 되므로 쓰지 않는다. 콰리즈미의 책 이름에서 나온 알자브르(al-jabr)가 '흩어진 것을 다시 맞추기'라서 합치기 자리에 두었다.
  - 영신의 검수 댓글은 검수 페이지 Artifact에 달린다. 고친 것은 check.md와 WORK_LOG에 적는다.
  - **시작할 때 앱의 고칠 점도 읽는다(26.11.21). 영신이 "췍"이라고 하면 이 일(고칠 점을 읽고 고치기)을 하라는 뜻이다(26.11.26 영신 "고칠거 고쳐달라고 하는건 그럼 이제 췍이라고 할게").** 앱 질문챗 옆 '메모로 남기기'(26.11.26 앱 32판까지 '고칠 점으로 남기기')로 남긴 것은 앱 저장소 `fixes/`에 있다. ArtifactData `list`(앱 주소, `fixes`)로 읽고, `state`가 `open`인 것을 고친 뒤 `update`로 `state`(`done` 고침, `kept` 그대로 둠)와 `reply`(무엇을 고쳤는지·왜 그대로 두는지 한 줄과 날짜)를 적는다. 영신 앱에 그대로 보인다. 고친 것은 검수 댓글처럼 check.md·WORK_LOG에 적는다. **메모(26.11.26, PRINCIPLES 2-2):** 고칠 제안이 아닌 메모는 그 단원 노트 `notes/<단원 id>`(`{u, md, at}`, ArtifactData `set`, 있으면 받은 판을 `if_version`으로)에 목표·쪽 순서로 정리해 넣고 `state`를 `noted`로. 영신의 말은 살리고 틀린 이해는 '바로잡기'로 옆에 단다. 교과서 글은 넣지 않는다.
- 그림은 설명 안 ` ```graph ` 블록으로 쓴다(content/README, PRINCIPLES 2-2-2). 식으로 못 그리는 실물은 자유 이용 그림을 ` ```img ` 블록으로(장부 `sources/images.json`, `tools/images.py fetch`·`credits`·`check`, 파일 `app/img/`는 앱을 올릴 때 `files`로 같이 올린다). 영상·글·시뮬레이션은 설명의 그 자리에 ` ```link ` 블록으로 녹인다(18판, 옆 칸 영상 목록은 없앴다). 단원을 쓸 때 `python3 -I tools/videos.py block <id>`로 그 단원의 3B1B 짝을 보고 맞는 것만 넣고, `tools/videos.py`로 넣은 것·뺀 것을 확인한다. 교재 문제의 목표(`sources/problem-objs.json`)를 바꾸면 `tools/problems.py`.
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
- **Windows PC(26.11.14):** 저장소 `C:\Users\Young\Documents\naturegoyang`, 책은 iCloud Drive `30 과학/`·`20 수학/`. Python 3.12(`%LOCALAPPDATA%\Programs\Python\Python312\python.exe -I -X utf8 tools/…`), PDF 글자는 Git의 `pdftotext`(한글 경로를 못 열어 ASCII 이름으로 복사). 비공개 폴더 `과학고양/`은 이 PC에 내려오지 않는다 → 저장소 백업은 `Documents\naturegoyang-private\artifact-backup\<날짜>\`.
