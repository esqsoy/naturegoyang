# 배포 기록

## 지금 공개된 것

- **claude.ai Artifact(비공개, 영신 계정만 열 수 있다):** https://claude.ai/artifact/F41365G2ctAVkpdP9qnscp
  - 화면 제목: 과학고양 (5판까지 '자연과학 주기율표')
  - 쓰는 기능: Claude 호출(설명·카드·문제 생성), Artifact 저장소(기록, 만들어 둔 설명·카드), 보는 사람 id
  - 원본: `app/naturegoyang.html`
- **영신 검수 페이지(Artifact, 비공개):** https://claude.ai/artifact/4LuPsZwy4i4q2ye2NKnjN8 — 화면 제목 '과학고양 내용 검수', capabilities `comments: {composer_only: true}`, 원본 `tools/review-page.py`가 content/에서 만든다. 1판(26.11.09): 1~5단원. 2판(26.11.10): 2번 직관 문장 고침. 3판: 2번 직관 비유 뺌. 4판: 6~10번 더함. 5판: 11~15번. 6판: 16~20번. 7판: 21~25번. 8판: 26~30번. 9판: 31~35번. 10판: 36~40번. 11판: 41~45번. 12판: 46~50번. 13판: 51~55번. 14판: 56~60번. 15판: 61~65번. 16판: 66~70번. 17판: 71~75번. 18판: 76~84번(전 단원).
- GitHub Pages: 없음. 지금 앱은 claude.ai 안에서만 Claude 호출과 저장소를 쓸 수 있다(README '어디서 돌아가나').

## 판 (같은 주소에 덮어씀. 1~5판 2026-11-09, 6~9판 2026-11-13)

| 판 | 내용 |
|---|---|
| 1 | 73단원 주기율표, 설명 방식 고르기, 확인 5문제 80점, 시작 수준 인정, 응용 복습 |
| 2 | 마스터용: 84단원, 직관·통상·엄밀 층 설명, 암기 카드와 카드 간격 반복, 확인 8문제 85점, 인정 없앰, 반말 화면 |
| 3 | 숙달 100점, 이어하기, 단계 잠금, 서술형 통과 판정, 회차 실패 표시 |
| 4 | 한 장씩 읽기: 읽을 시간, 점검 질문, 끝까지 읽어야 암기, 옛 설명에 점검 끼우기 |
| 5 | 진행 막대 칸·목차로 읽은 장 이동, 암기 화면에서 설명 다시 읽기, 이전·다음 버튼 아래 띠 고정 |
| 6 | 이름 과학고양, 생성 지시에 용어 한글(漢字, English)·정의 완결·한정어·뒤 단원 개념 규칙, 따라쓰기(카드·확인·응용 복습). 이 판은 맥미니 작업을 받기 전에 만들어 설명 열쇠 `--v4`와 카드 핵심 받기(`cards/<id>`에 씀)가 들어 있었다 |
| 7 | 6판을 미리 만든 내용에 맞춤: 설명 열쇠 `--v3`로 되돌림, 카드 핵심 받기 없앰(뒷면에서 뽑기), 저장소에서 온 설명·카드의 '다시 쓰기'·'카드 전체 다시 만들기' 숨김, 학습 목표 다섯 고침(42·46·66·68·69번), 용어 카드 종류 |
| 8 | 모든 Claude 호출(설명·카드·확인·채점·응용 복습·질문·연결 정리)을 가장 유능한 등급(`complex`)으로. 기다림 안내를 1~2분으로 |
| 9 | 가독성: 용어는 형광펜 밑줄 + 작은 풀이, 핵심 식 상자, 오개념 오해·사실 두 줄, 단원 첫 장에 용어 미리 보기(좁은 화면은 학습 목표도), 점검 답 아래 "이 목표에서 외울 것", 요약 상자 |

판 번호는 Artifact 쪽 판 번호와 같다.

## Artifact 저장소 내용 고침 (페이지는 그대로)

| 날짜 | 문서 | 판 | 내용 |
|---|---|---|---|
| 2026-11-09 | `lessons/f-measure--v3` | 1 → 4 | 교과서 대조(Brown 1.6): 소수점 없이 0으로 끝나는 수 규칙 더함. 연결 문장 둘 바로잡음([[c-matter]]의 몰 → 밀도 단위, 은하 규모 Gm 이상 → 약 10²¹ m). 고치기 전 원본은 비공개 폴더 `artifact-backup/2026-11-09/` |
| 2026-11-09 | `lessons/f-measure--v3` | 4 → 5 | content/f-measure로 옮김: 주요 용어 한자 병기(앞 두 덩어리는 그대로). |
| 2026-11-09 | `cards/f-measure` | 1 → 2 | 용어 카드 c25~c36 더함(c01~c24 그대로). |
| 2026-11-09 | `lessons/f-method--v3`, `f-ratio--v3`, `f-trig--v3`, `f-vector--v3` | 새로 1 | 미리 만든 설명(content/). |
| 2026-11-09 | `cards/f-method`, `f-ratio`, `f-trig`, `f-vector` | 새로 1 | 미리 만든 카드(용어 카드 포함). |
| 2026-11-10 | `lessons/f-method--v3` | 1 → 2 | 영신 검수 댓글: 1절 직관의 '자백' 비유를 풀어 씀. 검수 페이지 2판. |
| 2026-11-10 | `lessons/f-method--v3` | 2 → 3 | 영신 검수 댓글(이어서): 형사 비유를 빼고 '지지 ≠ 증명'으로 고침. 검수 페이지 3판. |
| 2026-11-10 | `lessons/`·`cards/` p-motion, p-force, p-energy, p-wave, c-matter | 새로 1 | 6~10번 미리 만든 설명·카드. 검수 페이지 4판(10단원). |
| 2026-11-10 | `lessons/`·`cards/` c-particle, c-atom, b-life, b-cell, e-sphere | 새로 1 | 11~15번. 검수 페이지 5판(15단원). |
| 2026-11-10 | `lessons/`·`cards/` e-rock, e-surface, e-sky, f-sci, f-stats | 새로 1 | 16~20번. 검수 페이지 6판(20단원). |
| 2026-11-10 | `lessons/`·`cards/` p-momentum, p-gravity, p-rotation, p-fluid, p-heat | 새로 1 | 21~25번. 검수 페이지 7판(25단원). |
| 2026-11-10 | `lessons/`·`cards/` p-electric, p-circuit, p-magnet, p-light, c-periodic | 새로 1 | 26~30번. 검수 페이지 8판(30단원). |
| 2026-11-10 | `lessons/`·`cards/` c-bond, c-shape, c-mole, c-gas, c-solution | 새로 1 | 31~35번. 검수 페이지 9판(35단원). |
| 2026-11-10 | `lessons/`·`cards/` c-acid, c-redox, b-molecule, b-membrane, b-enzyme | 새로 1 | 36~40번. 검수 페이지 10판(40단원). |
| 2026-11-10 | `lessons/`·`cards/` b-respiration, b-photo, b-division, b-mendel, b-dna | 새로 1 | 41~45번. 검수 페이지 11판(45단원). |
| 2026-11-10 | `lessons/`·`cards/` b-body, b-ecology, e-plate, e-history, e-atmos | 새로 1 | 46~50번. 검수 페이지 12판(50단원). |
| 2026-11-10 | `lessons/`·`cards/` e-ocean, e-solar, f-rate, f-linalg, p-thermo | 새로 1 | 51~55번. 검수 페이지 13판(55단원). |
| 2026-11-10 | `lessons/`·`cards/` p-osc, p-relativity, p-quantum, c-thermochem, c-kinetics | 새로 1 | 56~60번. 검수 페이지 14판(60단원). |
| 2026-11-10 | `lessons/`·`cards/` c-equilibrium, c-electro, c-organic, b-evolution, b-nerve | 새로 1 | 61~65번. 검수 페이지 15판(65단원). |
| 2026-11-10 | `lessons/`·`cards/` b-immune, b-regulation, b-micro, e-climate, e-star | 새로 1 | 66~70번. 검수 페이지 16판(70단원). |
| 2026-11-10 | `lessons/`·`cards/` p-nuclear, p-qm, p-statmech, p-semicon, p-gr | 새로 1 | 71~75번. 검수 페이지 17판(75단원). |
| 2026-11-10 | `lessons/`·`cards/` p-field, c-buffer, c-spectro, c-qchem, b-biotech, b-origin, b-brain, e-galaxy, e-life | 새로 1 | 76~84번. 전 84단원 올림(DB 문서 171개). 검수 페이지 18판(84단원). |
