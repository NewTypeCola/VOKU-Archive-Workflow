# 실제 도구의 보존본

[English](../../../history/historical/README.md)

현재 원본 패키지에서 가져온 **13개 파일 / 전체 파일 8개 / 함수 발췌 5개**입니다. 당시 코드의 형태를 보존했습니다. 원본 파일 해시, 원본 줄, 추가 import, 주석 편집, 배포 파일 해시는 [provenance](../../../history/reference/code-provenance.json)에 있습니다.

개인 홈 디렉터리 경로와 실제 입력·원장·이름·토큰 대조표는 가져오지 않았습니다. 한 예시 음절을 설명한 주석만 일반화했고 실행문은 유지했습니다. 발췌본에는 필요한 범용 import를 붙인 경우가 있습니다.

| 보존 코드 | 형태 | 실행 이력의 구분 | 적용 근거 |
|---|---|---|---|
| [identity/global_identity_v3.py](../../../history/historical/identity/global_identity_v3.py) | 전체 파일 | 신원 재구성 실행. 이미지 마스킹은 승인되지 않음 | 대규모 신원 재구성 (attempt_008)의 aggregate_summary와 독립 검증 |
| [names/spatial.py](../../../history/historical/names/spatial.py) | 전체 파일 | 운영 적용 | 주 마스킹 패키지의 현재 코드와 제출·기하·내보내기 기록 |
| [names/measured_characters.py](../../../history/historical/names/measured_characters.py) | 함수 발췌 | 운영 적용 | 주 기하 단계의 영수증. 보수적인 분할이 페이지를 보류할 수 있음 |
| [names/program_submission.py](../../../history/historical/names/program_submission.py) | 함수 발췌 | 운영 적용 | 편성 전체 제출 패치와 실제 47문서 제출 |
| [names/session_ownership.py](../../../history/historical/names/session_ownership.py) | 전체 파일 | 운영 적용 | 두 세션 패치, 현재 reading_sessions DB와 main/reverse 실행 기록 |
| [names/short_alias.py](../../../history/historical/names/short_alias.py) | 함수 발췌 | 운영 적용 | 28쪽 한정 pilot의 10곳·9쪽 |
| [repair/render_contract.py](../../../history/historical/repair/render_contract.py) | 전체 파일 | 구현·부분 적용. 후기 2,230쪽 전체 완료에는 이르지 않음 | 현재 artifact 이력 58행·고유 페이지 18쪽. 이후 후기 보류 해소 경로 (new-boryu)의 완료와 구분 |
| [review/geometry.js](../../../history/historical/review/geometry.js) | 전체 파일 | 운영 적용 | 현재 이미지 기록 21,009개를 가진 검토 앱 |
| [approval/masking.py](../../../history/historical/approval/masking.py) | 전체 파일 | 운영 적용 | 고정 칸 마스킹. 후대의 호출 설정이 3·5·7번 칸을 지정 |
| [contacts/paint_union.py](../../../history/historical/contacts/paint_union.py) | 함수 발췌 | 운영 적용 | 3,518쪽 refit과 이후 승인된 76쪽 빈틈 보정 |
| [contacts/recover_components.py](../../../history/historical/contacts/recover_components.py) | 함수 발췌 | 운영 적용 | refit에서 발견 원장 행과 실제 변경 픽셀의 연결 요소를 대조한 처리 |
| [composition/compose.py](../../../history/historical/composition/compose.py) | 전체 파일 | 운영 적용 | 최초 66,010쪽 합성과 후속 통합 영수증 |
| [ocr/vision_ocr_multiprocess.swift](../../../history/historical/ocr/vision_ocr_multiprocess.swift) | 전체 파일 | 운영 적용 | 최종 이미지의 전체·선택 OCR 생성과 원본·이미지 해시 연결 |

## 코드와 실행 근거 읽기

- review/geometry.js와 contacts/paint_union.py 등은 입력을 받는 작은 함수입니다.
- program_submission, session_ownership, render_contract, global_identity는 원래 패키지의 core/storage/판독·DB 계약에 의존합니다. 비공개 의존성과 운영 DB를 함께 배포하지 않아 단독 생산 실행을 제공하지 않습니다.
- composition/compose.py는 파일 쓰기와 상태 저장을 수행하는 실제 batch 도구입니다. 당시 plan과 이후 revision을 입력으로 받았으며, 실제 전체 실행은 그 시점의 영수증으로 설명합니다.
- OCR Swift 파일은 실제 macOS Vision 처리기입니다. 준비된 plan과 원본 이미지가 필요합니다.
- approval/masking.py의 기본값 3·5와 실제 후대 설정 3·5·7은 다릅니다. 이를 최신 기준으로 고치지 않고 보존했습니다.

현재 공개 검사기는 코드의 배포 해시와 Python 문법을 검사합니다. 원래 생산 실행은 당시 기록을 연결했습니다. 보존 코드에도 [MIT-0](../../LICENSE.md)을 적용합니다. 출처와 외부 구성요소는 [NOTICE](../../NOTICE.md)를 참고하세요.
