# 공개 검토 앱 확인 기록

[English](../../../../workflow/assets/human-review/VERIFICATION.md)

확인일: 2026-09-26. **로컬 Chromium 검증이며 외부 배포는 수행하지 않았습니다.**

## 확인한 동작

- `/review-preview/repository/workflow/assets/human-review/` 및 다른 사이트 하위 경로에서 앱과 상대 링크 로딩. 선택한 8면의 입력·결과 WebP 16개를 공개 데모의 SHA-256과 대조했습니다.
- 공개 입력·최종 결과 전환, 입력 화면의 편집 방지와 결과용 BBOX 숨김, 결과 이미지에 대한 검토 기록 연결.
- 상태·복수 이상 유형·메모 자동 저장, 새로고침 복구, 미확정 BBOX 초안 복구.
- 실제 포인터로 영역 생성·이동·크기 조절, 확대와 90도 회전 뒤 이미지 픽셀 좌표 유지. 기존 순수 기하 검사도 6배율·4방향 회전·8개 크기 조절 핸들을 확인했습니다.
- 재검토 모드의 BBOX 확정·이름 입력·빈 이름 차단, 입력칸과 한글 조합 중 상태 변경 방지. 기존 키보드/IME 검사 18개 시나리오도 통과했습니다.
- 검색·상태 필터·빈 목록·목록 페이지 경계·이전/다음 이동. 이상 없음으로 전환하면서 현재 영역을 지워도 이전 메모·좌표를 이력에 보존합니다.
- 현재 검토와 전체 변경 이력의 JSONL 다운로드, 충돌 초안 JSON 다운로드.
- 오래된 탭 저장 거부와 동시 저장의 원자적 버전 검사. 다른 브라우저 문맥 및 같은 호스트의 다른 배포 경로에 기록이 섞이지 않습니다.
- 저장소 차단·저장 용량 오류에서 실패 표시와 초안 보관 경로. 잘못된 좌표 저장 거부.
- 1440×1000 데스크톱과 폭 390px 모바일 화면. [문서용 화면](../../../../workflow/assets/human-review/review-screen.png)은 공개 데이터에 조작 예시 메모를 붙여 캡처했습니다. 앱에 이 예시 검토 기록을 미리 넣지는 않았습니다.
- 검토 동작에서 서버 API·POST·외부 서비스 요청이 없고, 정상 검토 경로의 JavaScript 실행 오류도 없었습니다.

브라우저 검사는 15개 기능 묶음을 통과했습니다. 이는 공개 샘플의 UI·저장 동작 확인이며, 실제 원고의 전수 판독이나 아카이브 공개 승인 검사가 아닙니다. Safari·Firefox 및 실제 원격 호스팅 환경에서는 실행하지 않았습니다.

## 보존·파일 확인

기존 앱의 `static/index.html`, `style.css`, `app.js`, `geometry.js`를 출발점으로 사용했습니다. 화면·편집·단축키·이력 흐름을 유지하고, 서버 연결을 `browser-store.js`로 바꿨습니다. `geometry.js`는 참고 앱과 바이트가 같습니다. 실제 운영 DB·기록은 복사하거나 실행하지 않았습니다.

작업 전후 SHA-256 대조에서 History 기준본과 manifest 33개, 기존 공개 데모 193개, 참고 앱 UI 4개와 읽은 분석 자료 8개가 그대로입니다. 기존 workflow 문서 중 변경한 것은 `README.md`와 `pipeline.md`뿐입니다. 기존 데모 문서·인간–에이전트 운영 문서는 그대로입니다. 새 앱 전용 정적 검사는 8면·16개 이미지·로컬 링크 105개와 앱 텍스트 12개를 확인해 통과했습니다. 파일 해시·구문과 명백한 개인 경로/운영 ID/자격증명 패턴도 검사했습니다.

저장소 전체의 기존 `verify_public.py`는 History 해시 오류 없이, 다음 기존 경로 부재 3건을 보고했습니다. 상위 README와 공개 목록은 아직 Workflow·Demo를 빈 후속 영역으로 설명합니다. 이 파일들은 이번 수정 경계 밖이라 갱신하지 않았습니다. 앱 전용 검사의 통과를 저장소 전체 패키징 검사의 통과로 표현하지 않습니다.

- 상위 `README.md`의 `demo/` 링크
- 상위 `public-files.txt`의 `demo/.gitkeep`
- 상위 `public-files.txt`의 `workflow/.gitkeep`

## 재확인

저장소 루트의 공유 앱 폴더 `workflow/assets/human-review/`에서 다음을 실행합니다. 순수 기하·키보드 검사는 Node.js만, 브라우저 검사는 개발 환경의 Playwright와 Chromium을 사용합니다. 브라우저 검사는 임시 읽기 전용 서버를 열고 프로필·테스트 기록을 `workflow/.review-check/`에만 저장하며, 종료 시 서버와 브라우저를 닫습니다. 2026-09-27부터 새 검사 화면도 그 임시 폴더에 저장하며, 위의 2026-09-26 문서용 `review-screen.png`는 보존합니다. 필요하면 `CHROME_BIN`에 설치된 Chromium 계열 브라우저 실행 파일을 지정합니다. 이 도구들은 배포된 앱의 실행 의존성이 아닙니다.

```sh
node --check app.js
node --check browser-store.js
node tests/geometry.test.cjs
node tests/shortcuts.test.cjs
python3 -B tests/verify_static.py
node tests/browser.test.cjs
```

`workflow/.review-check/`는 배포 대상이 아닙니다. 기존 공개 데모 이미지와 문서를 함께 배포하는 방법은 [로컬 실행·정적 환경 안내](README.md)에 있습니다.

<a id="integration-20260927"></a>

## 2026-09-27 · 공개 리포지트리 통합 확인

위 2026-09-26 결과는 당시 기록으로 보존했습니다. 이번에는 루트 소개와 읽는 동선, 공개 파일 목록, 현재 배포 manifest와 검사 연결을 갱신했습니다. History의 `history-anchor-v3`와 과거 실행·비교용 해시는 유지했습니다.

- 저장소 검사 `python3 -B tools/verify_public.py` 통과: 공개 목록 249개, 텍스트 89개, 로컬 링크 513개, Python 구문 14개와 JSON 33개를 검사했습니다. 현재 workflow manifest 209개와 회차 manifest 130개, 데모 53면의 적용 기록·페이지 대응, 입력/최종 OCR의 이미지 해시 연결 106개와 OCR 사본 6개가 일치했습니다. 현재 manifest는 자기 자신을 제외한 workflow 공개 파일을 담고, 전체 저장소의 배포 목록은 `public-files.txt`입니다.
- 앱 정적 검사: 공개 샘플 8면, 입력·결과 이미지 16개와 해시·적용 영역·문서 연결을 확인했습니다.
- JavaScript 구문, 기존 기하 검사(6배율·4회전·8핸들), 키보드/IME 18개 시나리오가 통과했습니다.
- 설치된 Google Chrome에서 기존 브라우저 검사 15묶음이 통과했습니다. 공개 목록에 있는 파일만 제공하는 로컬 서버의 두 하위 경로에서 루트 → Workflow → 데모 → 앱 → 검토·보정 History, 앱의 프로젝트 소개·문서 복귀 링크, 이미지·JSON을 확인했습니다. 임시 검사 결과 경로는 HTTP 404로 차단했습니다. 1440×1000 데스크톱과 폭 390px 모바일 검사 화면도 확인했습니다.
- 검사기가 누락 파일, 브라우저 임시 파일·DB의 목록 유입, 현재 manifest의 잘못된 해시·크기, OCR 이미지 연결 오류, 없는 문서 앵커를 거부하는 7개 조건도 메모리 안의 가상 읽기로 확인했습니다. 검사 때문에 실제 입력·완료 파일을 고치지 않았습니다.
- 작업 전후 SHA-256 대조: History 33개(기준본 포함), 현재 배포 manifest 외 기존 데모 192개, 인간–에이전트 운영 문서, 기존 문서용 검토 화면과 `NOTICE.md`가 그대로입니다. 보존 파일의 수정 시각도 같으며 삭제한 파일은 없습니다. 공개 목록에서만 존재하지 않던 두 `.gitkeep` 항목을 제거했습니다. 이는 파일·연결 보존 검사이며 원고 전수 개인정보 검토나 OCR 정확도 검사가 아닙니다.

변경 파일은 루트 `README.md`, `.gitignore`, `public-files.txt`, `tools/verify_public.py`; workflow의 `README.md`, `pipeline.md`, `demo.md`, `assets/demo/asset-manifest.json`; 앱의 `README.md`, `VERIFICATION.md`, `index.html`, `tests/browser.test.cjs`, `tests/verify_static.py`입니다. 정적 게시 경로를 유지할 `.nojekyll` 하나를 루트에 추가했습니다. 새 글꼴이나 라이선스 문구는 추가하지 않았습니다.

최초 브라우저 실행은 샌드박스의 로컬 포트 제한으로 실패했고, 접근을 허용한 뒤에는 기본 Playwright 브라우저 실행 파일이 없어 설치된 Chrome을 지정했습니다. 최종 검사는 그 환경에서 완료했습니다. Safari·Firefox, 실제 외부 배포 환경에서는 검사하지 않았습니다. 원자료나 공개 데모의 마스킹·OCR을 다시 실행하지 않았으며, 원격 업로드·push·배포도 수행하지 않았습니다.

## 2026-09-27 · 공개 문구 마감

직접 운영할 서비스 주소를 기다리는 안내를 제거하고, 로컬 정적 실행과 선택 가능한 정적 호스팅을 설명하도록 정리했습니다. 앱의 검토·저장 로직과 공개 샘플은 유지했습니다. 이번 재확인 결과는 [공개본 검증 기록](../../../history/reference/publication-check.md)에 남겼습니다.

<a id="english-edition"></a>

## 2026-09-27 · 영어 인터페이스와 양쪽 언어 문서

공유 앱의 표시 문구와 샘플 설명을 영어로 번역하고 한국어 안내 링크를 연결했습니다. 문자열을 제외한 JavaScript 구문 트리와 표시 설명 필드를 제외한 샘플 데이터는 원본과 일치합니다. 좌표 계산과 스타일 파일은 바이트가 동일합니다.

JavaScript 구문, 기존 기하 검사, 키보드·IME 18개 시나리오 전체, 8개 논리면·16개 이미지의 정적 검사와 기존 브라우저 검사 15개 묶음이 설치된 Chrome에서 통과했습니다. 1440×1000 데스크톱과 390px 모바일 화면을 확인했습니다. 현재의 [영어 화면 예시](../../../../workflow/assets/human-review/review-screen-en.png)를 별도로 제공하며, 2026-09-26의 `review-screen.png`와 위의 과거 검증 결과는 유지했습니다. 전체 배포본과 원본 보존 결과는 [영어 기본본 검증 기록](../../../history/reference/publication-check.md#english-edition)에 있습니다.
