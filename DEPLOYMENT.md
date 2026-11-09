# 배포 기록

## 지금 공개된 것

- **claude.ai Artifact(비공개, 영신 계정만 열 수 있다):** https://claude.ai/artifact/F41365G2ctAVkpdP9qnscp
  - 화면 제목: 자연과학 주기율표
  - 쓰는 기능: Claude 호출(설명·카드·문제 생성), Artifact 저장소(기록, 만들어 둔 설명·카드), 보는 사람 id
  - 원본: `app/naturegoyang.html`
- **영신 검수 페이지(Artifact, 비공개):** https://claude.ai/artifact/4LuPsZwy4i4q2ye2NKnjN8 — 화면 제목 '과학고양 내용 검수', capabilities `comments: {composer_only: true}`, 원본 `tools/review-page.py`가 content/에서 만든다. 1판(26.11.09): 1~5단원.
- GitHub Pages: 없음. 지금 앱은 claude.ai 안에서만 Claude 호출과 저장소를 쓸 수 있다(README '어디서 돌아가나').

## 판 (모두 2026-11-09, 같은 주소에 덮어씀)

| 판 | 내용 |
|---|---|
| 1 | 73단원 주기율표, 설명 방식 고르기, 확인 5문제 80점, 시작 수준 인정, 응용 복습 |
| 2 | 마스터용: 84단원, 직관·통상·엄밀 층 설명, 암기 카드와 카드 간격 반복, 확인 8문제 85점, 인정 없앰, 반말 화면 |
| 3 | 숙달 100점, 이어하기, 단계 잠금, 서술형 통과 판정, 회차 실패 표시 |
| 4 | 한 장씩 읽기: 읽을 시간, 점검 질문, 끝까지 읽어야 암기, 옛 설명에 점검 끼우기 |
| 5 | 진행 막대 칸·목차로 읽은 장 이동, 암기 화면에서 설명 다시 읽기, 이전·다음 버튼 아래 띠 고정 |

판 번호는 Artifact 쪽 판 번호와 같다.

## Artifact 저장소 내용 고침 (페이지는 그대로)

| 날짜 | 문서 | 판 | 내용 |
|---|---|---|---|
| 2026-11-09 | `lessons/f-measure--v3` | 1 → 4 | 교과서 대조(Brown 1.6): 소수점 없이 0으로 끝나는 수 규칙 더함. 연결 문장 둘 바로잡음([[c-matter]]의 몰 → 밀도 단위, 은하 규모 Gm 이상 → 약 10²¹ m). 고치기 전 원본은 비공개 폴더 `artifact-backup/2026-11-09/` |
| 2026-11-09 | `lessons/f-measure--v3` | 4 → 5 | content/f-measure로 옮김: 주요 용어 한자 병기(앞 두 덩어리는 그대로). |
| 2026-11-09 | `cards/f-measure` | 1 → 2 | 용어 카드 c25~c36 더함(c01~c24 그대로). |
| 2026-11-09 | `lessons/f-method--v3`, `f-ratio--v3`, `f-trig--v3`, `f-vector--v3` | 새로 1 | 미리 만든 설명(content/). |
| 2026-11-09 | `cards/f-method`, `f-ratio`, `f-trig`, `f-vector` | 새로 1 | 미리 만든 카드(용어 카드 포함). |
