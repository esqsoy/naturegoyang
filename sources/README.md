# 교과서 대조

과학고양 설명·카드·문제를 영신의 교과서와 맞춰 보는 자리다. 교과서 PDF는 맥미니 iCloud Drive `30 과학/`에 있고(영신 소장), 이 저장소에는 넣지 않는다.

## 원칙

- **원문은 공개 저장소에 옮기지 않는다.** 여기에는 책 이름, 절 번호, 짧은 절 제목만 적는다. 뽑은 목차·글자·쪽 그림은 비공개 폴더 `10 언어/고양/비공개/과학고양/`(git 밖)에 둔다.
- **교과서는 사실 확인과 범위·순서 참고에 쓴다.** 과학고양 설명은 우리 말로 새로 쓰고, 교과서 문장을 옮기지 않는다.
- **용어는 한국어 교과서를 먼저 본다.** 같은 개념의 한국어 용어는 『대학기초물리학』, 완자, 마더텅(수능 기출)에서 확인한다.
- 대조한 결과(틀림, 빠짐, 한정어 문제)는 WORK_LOG에 적고, 고친 칸은 고친 판을 남긴다.

## 책 (줄임 이름)

| 줄임 | 책 | 쓰는 영역 | 상태 (26.11.09) |
|---|---|---|---|
| brown15 | Brown·LeMay·Bursten·Murphy·Woodward·Stoltzfus, *Chemistry: The Central Science*, 15판 Global SI, Pearson 2022 | 화학 둘째 대조, 측정·단위, 대기·물 | 목차·글자 뽑음 |
| crc85 | Lide 엮음, *CRC Handbook of Chemistry and Physics*, 85판, CRC Press 2004 | 상수·물성값 확인 (2019 SI 개정 전 판) | 목차·글자 뽑음 |
| kphys | 윤진희·차동우, 『대학기초물리학』, 테크미디어 2014 (PDF a~d 넷) | 물리 28장, 한국어 용어 | 글자 뽑음, 목차는 본문 절 제목으로 만듦 |
| halliday11 | Halliday·Resnick·Walker, *Fundamentals of Physics*, 11판, Wiley 2018 | 물리 전반 (절 번호 "1-1"은 "1.1"로 적는다) | 목차·글자 뽑음 |
| serway | Serway·Jewett, *Physics for Scientists and Engineers with Modern Physics*, Cengage | 물리, 현대물리(39~46장) | 목차·글자 뽑음 |
| mcmurry | Robinson·McMurry·Fay, *Chemistry*, 8판 Global Edition, Pearson 2020 | **화학 첫째 대조 책**(영신이 번역본 종이책으로 읽는다). 절 단위로 적어 번역본에서 같은 절을 찾는다. 부록 A는 수학 | 목차·글자 뽑음 |
| campbell12 | *Campbell Biology*, 12판 Global, Pearson | 생명과학 전반. **이 파일은 장 짜임이 미국판과 다르다**(7장 Cell Structure and Function, 8장 Cell Membranes, 12장 Mitosis 등). 장 번호는 이 파일을 따른다 | 목차(장 단위)·글자 뽑음 |
| sadava | Sadava 외, *Life: The Science of Biology*, W. H. Freeman 2016 | 생명과학 (절 단위) | 목차·글자 뽑음 |
| particle | Ne'eman·Kirsh, *The Particle Hunters* | 표준 모형 역사 | 글자 뽑음 (PDF 목차 없음, 대응표에는 아직 안 넣음) |
| leekj | 이광조, 『초중고물리 30일 완성』 | 1단계 물리 눈높이 | 글자 뽑음 (36쪽, 그림 위주) |
| wanja-chem1 | 『완자 고등 화학Ⅰ』 | 고등 화학 용어·범위. 절 번호는 대단원.중단원.소단원(예: 4.1.2 물의 자동 이온화) | 글자 뽑음, 목차는 차례 쪽으로 만듦 |
| maderteong-earth1·2 | 마더텅 2024 수능기출 지구과학 Ⅰ·Ⅱ 문제편 | 지구·우주 고등 범위, 문제 눈높이. 스캔본이라 글자는 OCR(`pdf-index.js ocr`). 절 번호는 대단원(Ⅰ→1).중단원.소단원 | OCR 글자, 목차는 차례 쪽으로 만듦 |
| maderteong (나머지 6권) | 마더텅 2024 수능기출 물리학·화학·생명과학 Ⅰ·Ⅱ 문제편 | 1~3단계 문제 눈높이 | 받지 않음 (디스크 여유 14GB, 필요할 때) |
| pilbara | *Discovery Trails to Early Earth* (서오스트레일리아 동필바라 안내서) | 초기 지구·암석·초기 생명 증거('Knowing' 1~3장) | 목차·글자 뽑음 |

serway·sadava는 판 번호를 아직 판권 쪽에서 확인하지 않아 줄임 이름에 판을 붙이지 않았다. mcmurry는 8판(판권 쪽 확인), 줄임 이름은 그대로 둔다.

**빈 곳:**
- 지구과학·천문 대학 교재가 없다. 지구·우주 13단원은 마더텅 지구과학 Ⅰ·Ⅱ(고등 범위, 문제집이라 설명이 짧다), Brown 18장, Halliday 13·43·44장, 생명과학 책의 지구 역사·기후 장, Pilbara 안내서로 덮는다. 4단계(은하·우주론, 외계 행성)는 대학 천문 교재가 있으면 좋다.
- 기초 도구 수학(비례·그래프, 확률·통계, 미적분)은 화학·물리 책 부록(McMurry A, Brown A, Serway B)뿐이다.
- 대조 절이 하나도 없는 단원: f-linalg(복소수와 행렬). 맞는 교재가 없다.

## 대응표와 도구

- [unit-map.json](unit-map.json): 단원 id → 책 → 절 번호. 장 전체는 `"10"`, 절은 `"1.5"`.
- `osascript -l JavaScript tools/pdf-index.js outline|text|png|ocr <pdf> ...`: PDF 목차·쪽별 글자·쪽 그림(줄여서)을 뽑고, 스캔본은 OCR로 읽는다. macOS 내장 PDFKit·Vision만 쓴다. 큰 PDF도 한 쪽씩 다룬다.
- `python3 -I tools/kphys-outline.py`: PDF 목차가 없는 『대학기초물리학』의 목차를 본문 절 제목으로 만든다.
- `python3 -I tools/unit-sources.py <단원 id> [--text <파일>]`: 그 단원의 책·절·PDF 쪽을 보이고, `--text`면 그 쪽들의 글자를 한 파일로 모은다. `--check`는 대응표 전체를 목차와 맞춰 본다.
