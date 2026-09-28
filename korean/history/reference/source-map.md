# 원본 폴더를 독자용 질문에 연결하기

[English](../../../history/reference/source-map.md)

13개 신규 분석과 기존 연락처 분석을 합쳐 14개 근거 단위를 조사했습니다. 아래는 출처 탐색용 지도입니다. 본문은 각 폴더에서 확인한 문제와 전환점을 중심으로 구성했습니다.

| 참고 패키지 | 공개 서사에서의 역할 | 연결 |
|---|---|---|
| game | 입력 범위·기존 OCR·공개 이미지에서 새 OCR을 만드는 계획 | E01–03, 사례 1/6 |
| phone_mail_masking_webp | 초기 과잉·누락, 마스크 밀착, 기하 원장 회복 | 사례 4 |
| voku-read-only-masking | 저장 OCR 판독·분류·신원·공용 상태·정식 제출 | 사례 2 |
| human-review | 출력과 보류 원본을 나눈 검토, 이미지 버전과 검토 상태의 결합 | 사례 3 |
| VOKU_Execution_Plan | 기존 신원 재사용, 두 글자 호칭에 한정한 pilot | 사례 3 |
| boriu | 초기 완료본 검수 230쪽의 독립 교정 | 사례 3 |
| boriu-hold-1988-1999 | 초기 보류 2,057쪽과 시점별 범위 규칙 | 사례 3 |
| boriu-hold-2000-2019 | 후기 2,230쪽 대상의 설계·부분 실행·복원 및 캐시 오류 | 사례 3 |
| new-boryu | 같은 후기 대상을 OCR 중심으로 처리한 별도 완료본 | 사례 3 |
| seal-sign-masking | 외부 잉크 적용의 rollback, 고정 칸 처리, 7번 칸 추가 | 사례 4 |
| supplement-2000-2019 | 검토 대상 재발견, 범위·방향·복원 보정 | 사례 3/5 |
| imsi-2013-2018 | 후기 결과를 다시 보는 검토 UI와 export의 왕복 | 사례 3 |
| final-boriu-zebal | 후보 → 사용자 수정 → 선택 적용과 수신 측 연결 | 사례 5/6 |
| final-tri-force | 레이어 합성·이력 재생·최종 이미지 OCR | 사례 5/6 |

추가로 memory가 가리킨 P0 신원 작업의 실패 분석·재OCR 실험·v2 attempt·명단 통합 중단 보고를 읽었습니다. OCR/overlay의 실행·중단과 대체 패키지의 제작 이후 실행도 시점별로 연결했습니다.

## 이력 밖으로 가져오지 않은 자료

기존 공개 구현 `written`에는 공통 profile/CLI로 다시 구성한 인터페이스가 있었습니다. 이를 실제 초기 VOKU 구조로 삼지 않았습니다. 그 근거 색인은 출처의 경계를 확인하는 데 참고했으며, 이번 저장소에서는 역사 도구들을 공통 실행기로 다시 합치지 않았습니다.

원본 note, DB, memory, 코드 전체 archive는 배포하지 않습니다. 필요한 코드는 [코드 목록](../historical/README.md)에서 출처와 실행 여부를 확인할 수 있습니다.

## Documents 추가 탐색에서 연결한 자료

| 참고 패키지·보관본 | 현재 History를 보강한 지점 | 근거 |
|---|---|---|
| tmptest | 실제 실패 → 기하·신원 참조 수리 → 운영 코드 반영 | [E27](evidence.md#e27) |
| 보관 voku-read-v2.zip | 제작 뒤의 85쪽 텍스트 판독과 미제출 packet | [E28](evidence.md#e28) |
| voku-read-next | 주 처리의 세션 분기와 82쪽 실제 제출 | [E29](evidence.md#e29) |
| voku_2000_2019_planning_bundle_local_paths | 빈 수동 검수 표시의 누락과 선정 정정 | [E31](evidence.md#e31) |
| voku-name-repair | OCR 우선 이주, 이전 영수증 호환, 279쪽 출력 | [E31](evidence.md#e31) |
| tri-force-gumsu | 합성 뒤의 누락 조사와 bbox 가이드의 입력 범위 | [E32](evidence.md#e32) |
| voku-luna-economy-v3 | 실제 worker 보고의 정정과 활성 작업을 마친 뒤의 중단 | [E33](evidence.md#e33) |
| voku-ocr-readonly | 저장된 줄 bbox를 이용한 재기입과 현재 영수증 | [E34](evidence.md#e34) |
| staff-identity/test-spark | 연도별 명단 통합 결과 | [E35](evidence.md#e35) |

미러·공개 초안·보관 사본의 채택 기준은 [History 수정 기록](history-revision.md)에 있습니다.
