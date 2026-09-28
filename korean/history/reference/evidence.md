# 근거와 주장 연결

[English](../../../history/reference/evidence.md)

확인 기준: 2026-09-26. **원본 위치는 참고 패키지 안의 상대경로**이며 그 데이터가 공개 저장소에 들어 있다는 뜻은 아닙니다. `staff-identity`는 비공개 신원 작업 루트의 공개용 별칭입니다. `...` 또는 `*`는 공개하지 않은 중간 경로이며 실행 가능한 glob 지시가 아닙니다.

기초 조사에서 13개 신규 folder note와 기존 연락처 note를 모두 읽고, 208개 memory summary의 색인에서 주요 전환을 찾아 대조했습니다. 이번 History 보강에서는 Documents의 폴더 구조를 추가 탐색하고 보관 ZIP, 후속 실행 DB, 시험·이주·중단 보고를 확인했습니다. 채택 이유와 정정은 [수정 기록](history-revision.md)에 있습니다.

- **실행 사실:** DB·manifest·output·영수증 우선. 저장 검증 보고와 이번 재검증도 구분합니다.
- **당시 이유:** memory와 당시 계획/진단/사용자 정정 기록. 현재 코드에서 동기를 역산하지 않습니다.
- **회고의 설명:** 여러 출처를 연결한 인과관계. 미확인 연결은 실행 이력에 끼워 넣지 않습니다.

아래는 당시 이유, 실제 실행, 후속 결과를 연결한 비식별 근거 요약입니다. 원 코드의 해시·발췌 줄·편집은 [code-provenance](../../../history/reference/code-provenance.json)에 있습니다.

<a id="e01"></a>

## E01 — 초기 문제와 P0 계획

**출처:** game/reports/VOKU P0-4.5 Staff Identity Privacy Plan.md

**관측·실행 근거:** 목적, A/B/C 구분, 보호 우선순위의 원문을 직접 확인했습니다. 명단·후보·사람 판정·마스킹은 당시 구상이었으며, 학적까지 포함한 범위였습니다.

**당시 판단과 연결:** 당시 계획 문서 자체를 목적의 근거로 삼았습니다. 이후의 이름 전용 규칙을 이 계획에 소급하지 않습니다.

<a id="e02"></a>

## E02 — 입력·OCR·Public-WebP-First

**출처:** game: 복사 manifest, source inventory, OCR 품질 보고; reports/VOKU_P0_5_PUBLIC_WEBP_FIRST_ARCHITECTURE_AMENDMENT_20260821.md; folder-notes/game

**관측·실행 근거:** 노트 전체를 읽었습니다. 숫자 연도는 66,010쪽·5,330문서, Unknown은 4,413쪽·389문서였습니다. 현재 복사 도구와 생성기를 구분했습니다. 원래 manifest의 81,835행과 README의 81,836행 사이에 있는 충돌은 보존했습니다. 초기 변환기와 PDF가 현재 남아 있지 않은 경위는 미확인입니다.

**당시 판단과 연결:** 8/21 수정안의 ‘최종 이미지에서 새 OCR을 만든다’는 원칙을 후속 E24의 실행과 연결했습니다.

<a id="e03"></a>

## E03 — 초기 연락처 실패·복원

**출처:** game/phone_mail_masking_webp: 초기 audit/복원/outlined 처리 보고; folder-notes/phone_mail_masking_webp/WORKING_DRAFT.md

**관측·실행 근거:** 노트 전체를 읽고 원본의 현재 도구를 확인했습니다. 과잉·누락, line-ratio 좌표, nilError/0-line, 3,718쪽 복원은 당시 보고에 근거합니다. 초기 복원 파일을 현시점에 전수 재검증하지는 못했습니다.

**당시 판단과 연결:** 노트가 보존한 당시 지시와 시정 기록을 사용했습니다. 실제 초기 복원과 9/22 refit은 서로 다른 사건입니다.

<a id="e04"></a>

## E04 — 513건 검토가 드러낸 문제

**출처:** staff-identity/p0-4.5b/results/post_human_review/failure_analysis_v1/reports/FAILURE_ANALYSIS_REPORT.md; OCR_RECOVERY_ASSESSMENT.md

**관측·실행 근거:** 원본 분석 보고 두 개를 직접 읽었습니다. 정정 131건 중 61건은 기존 OCR에 있었고, 70건은 양쪽 OCR에서 미탐이었습니다. 사람 검토의 disposition과 의미 범위가 충돌했습니다.

**당시 판단과 연결:** 8/24 당시 진단 문서에 근거합니다. 전수 재OCR를 권고한 것이 아니라, extraction/reconciliation 문제와 제한 실험을 먼저 구분한 기록입니다.

<a id="e05"></a>

## E05 — 제한 재OCR와 알려진 표본 재생

**출처:** staff-identity/p0-4.5b/archive/.../reports/P0_4_5B_TARGETED_PRINTED_OCR_RECOVERY_EXPERIMENT_20260825.md; HANDWRITING_MIXED_OVERRIDE_RECOVERY_EXPERIMENT; RECOVERED_OCR_513_REPLAY_EVALUATION

**관측·실행 근거:** 원본 보고의 결과·방법·한계 절을 직접 확인했습니다. 13건의 결과는 7/4/2/0, 56건의 결과는 22/11/14/9였습니다. 기존 대상 440/440건을 유지했고 새 노출은 0건이며 ID는 바뀌지 않았습니다. 전체 모집단에 실행한 실험은 아닙니다.

**당시 판단과 연결:** 8/25 실험의 additive evidence 원칙과 동결한 이전 결과를 근거로 삼았습니다. 원본의 실명별 표와 raw OCR은 공개본에서 제외했습니다.

<a id="e06"></a>

## E06 — 대규모 신원 재구성 (P0-4.5v2 attempt 008)

**출처:** staff-identity/p0-4.5v2/work/attempt_008/aggregate_summary.json; pipeline/src/global_identity_v3.py

**관측·실행 근거:** 현재 aggregate를 직접 조회하고 source 전체를 보존했습니다. 재구성은 실행됐으며 source_transformation_authorized=false였습니다.

**당시 판단과 연결:** 제공된 8/29 memory에서 eligibility-first 원칙, 불완전한 same-name 조합 598,223개의 집계, 로컬 소속이 불명인 probable occurrence 1,311개의 시정, 검증기의 비효율 수정을 확인했습니다.

<a id="e07"></a>

## E07 — 후보 의미 구조 수리 (P0-4.5v2 attempt 009 semantic repair)

**출처:** staff-identity/p0-4.5v2/work/attempt_009/validation/independent_semantic_verification_v4.json; 8/29 semantic repair memory.

**관측·실행 근거:** 99/99 검사를 통과했고 candidate_only=true였습니다. 공개 토큰 사용과 마스킹 실행은 false였습니다. 구조화한 이름 칸·소속·학적·신원 가설을 분리한 결과입니다.

**당시 판단과 연결:** QA가 UNRESOLVED_BINDING 16건을 NOT_STATED로 보여 주던 오류를 수정했습니다. 의미 상태를 화면에 옮기는 과정도 검증 대상이 됐습니다.

<a id="e08"></a>

## E08 — blind pilot 준비와 직접 이미지 오독

**출처:** staff-identity/p0-4.5v2/work/attempt_010/test 및 해당 준비 기록

**관측·실행 근거:** 연결된 원본 위치가 존재하는 것과 memory에 기록된 준비 완료·응답 부재를 구분했습니다. 준비 상태와 응답 상태를 따로 기록했습니다.

**당시 판단과 연결:** 제공된 8/30 memory에는 100개 방송·270쪽의 입력 묶음 준비와 응답 100개의 부재가 남아 있습니다. 별도 direct-vision 요청에서는 오독을 반복하다 사용자 지적 뒤 확대해 다시 판독했습니다. 실명은 공개하지 않았습니다.

<a id="e09"></a>

## E09 — 통합 검증기의 false negative

**출처:** staff-identity/Z-Broadcast-Staff-Roster-Merge-legacy/v4*/results/run/audits/blocked_run_report.json

**관측·실행 근거:** 원본 보고를 직접 읽었습니다. input_incomplete 2건과 blocked 1건이 있었는데도 complete와 issue 0건으로 표시했습니다. Cycle00 통과는 무효화됐고, Cycle01은 중단됐으며 Cycle02는 시작하지 않았습니다. 최종 공개 상태는 false였습니다.

**당시 판단과 연결:** 제공된 9/1 memory에서 고정 evaluator와 생성기가 같은 누락을 공유한 문제를 확인했습니다. 기존 run 안에서 임의로 수정하지 않고 중단했습니다. 후속 새 run은 지시였으며 그 자리에서 실행한 성과는 아닙니다.

<a id="e10"></a>

## E10 — 실제 이미지 작업자·overlay·취합

**출처:** voku-ocr-v3: pause_before_luna_test, luna_test_2017_3episodes, completed_artifacts; voku-fast-overlay: metrics 및 STOP_AFTER_ACTIVE

**관측·실행 근거:** 보존된 memory와 체크포인트의 당시 실행·중단 집계에 근거합니다. Luna v3의 후속 실행은 E33에서 실제 STOP 기록과 추가로 대조했습니다.

**당시 판단과 연결:** 제공된 9/5~6 memory의 재개·중단 기록 네 개와 취합·재배치 기록을 모두 읽었습니다. 누적 2,170쪽, 제한 시험 중단, 55+896쪽의 재개, 6,920쪽 취합은 서로 합산하지 않습니다.

<a id="e11"></a>

## E11 — 격리 시험의 실패와 대체 패키지 제작 시점

**출처:** 격리 기하 시험의 tmptest/archive/batch_before_20260907T014814/reports/test_2019_4_episodes; read-v2 audit/package_ready.json(보관 ZIP); read-next reports/migration_verification.json; academic policy test memory.

**관측·실행 근거:** 52쪽 시험의 결과는 12 verified / 30 no_changes / 8 partial / 2 hold였고 export는 0이었습니다. read-v2의 제작 검증은 29개, read-next의 제작 검증은 198개였습니다. 이 제작 보고의 production_started=false 이후에 실제 실행이 따로 있었습니다.

**당시 판단과 연결:** 9/6~7 시험의 기하·토큰 실패는 E27의 저장 판독 재사용·코드 반영으로 이어졌습니다. 9/7 단일 feedback 요청은 E28의 단계별 패키지와 후속 실행으로, 9/8 전체 작업 시간 절감 요청은 E29의 세션 대체본으로 연결했습니다. academic fixture의 text/lines 불일치로 시험 8개 중 1개가 실패한 당시 실행도 보존했습니다.

<a id="e12"></a>

## E12 — 1차 이름 처리의 현재 상태

**출처:** voku-read-only-masking/state/queue.sqlite3; outputs/manifest.jsonl; folder-notes/voku-read-only-masking/직접확인.json

**관측·실행 근거:** 현재 DB를 읽기 전용으로 재집계했습니다. 5,330문서 모두 공식 제출됐으며 페이지 상태는 verified 21,009 / no_changes 40,714 / partial 4,182 / hold 105였습니다. 보류 원인 분할은 노트에서 partial 4,182쪽의 현재 receipt를 재집계한 결과에 근거합니다.

**당시 판단과 연결:** 현재 POLICY와 과거 실행을 구분했습니다. 노트의 전체 본문과 근거 대조를 읽었으며, 이 상태에서 E30의 원인별 재작업 설계가 이어졌습니다.

<a id="e13"></a>

## E13 — 편성 단위·왕복 감소·독립 두 세션

**출처:** voku-read-only-masking/reports/program_work_unit_20260908; prompt_refinement_20260908.json; src/text_stage.py, orchestration.py, workflow.py

**관측·실행 근거:** 현재 제출·소유권 코드를 보존했습니다. 노트에 있는 47문서·320쪽의 공식 결정 연결을 현재 DB와 대조했습니다. 전달 문자 수와 수집 latency는 당시 표본의 관측값입니다.

**당시 판단과 연결:** 제공된 9/8 memory의 최적화 기록 두 개와 9/9 dual 분석에서 사용자 판단을 확인했습니다. 반복 판단·출력·왕복을 줄이면서 공용 ID의 권위를 유지하라는 요구였습니다.

<a id="e14"></a>

## E14 — 검토 앱과 버전 결합

**출처:** human-review/server.py, static/geometry.js, data/reviews.sqlite3; hold-review; folder-notes/human-review

**관측·실행 근거:** 현재 DB에서 ok 17,042 / issue 321 / needs 3,646을 직접 집계했습니다. 좌표 JS 전체를 보존했습니다. hold active 2,221쪽과 9쪽의 해제·복원은 노트의 직접 검증에 근거합니다.

**당시 판단과 연결:** 노트가 연결한 IME·초안·bbox·버전 변경 요청을 확인했습니다. 리뷰 상태, 문제 안내, 확정 인명, 실제 이미지 적용을 구분했습니다.

<a id="e15"></a>

## E15 — 짧은 호칭 파일과 초기 완료본 교정

**출처:** VOKU_Execution_Plan/repair.py 및 run 결과; boriu/src/render_corrections.py와 완료기록; 해당 두 folder notes

**관측·실행 근거:** 호칭 함수를 직접 읽고 보존했습니다. 28쪽 범위의 10곳·9쪽과 230쪽 대상에서 나온 229쪽 출력은 노트 전체의 산출물 대조에 근거합니다. 최초 발견자는 미확인입니다.

**당시 판단과 연결:** 초기 인물 판단을 재사용하고 기하 경계만 보완했습니다. boriu의 후속 2쪽은 사용자가 지정했으며 다른 출력 227개는 보존했습니다.

<a id="e16"></a>

## E16 — 초기 연도 보류

**출처:** boriu-hold-1988-1999: LOCAL_POLICY, render.py, queue/manifest/verification; 해당 folder note

**관측·실행 근거:** 2,057쪽을 로컬 완료했으며, 초기 10쪽의 군집형 처리와 후기 wholebox 처리가 공존합니다. 사람 승인 필드가 false인 것은 20쪽이며, 필드가 없는 것은 2,037쪽입니다.

**당시 판단과 연결:** 노트의 구체적인 사용자 답변과 399개 등록 승인을 연결했습니다. 초기 처리에 소급할 의도는 미확인으로 남긴 답변을 따랐습니다. 등록 대기 316개에 사용자 승인 399개가 더해진 뒤 처리가 이어진 당시 경로입니다.

<a id="e17"></a>

## E17 — 후기 보류의 부분 실행과 캐시 수정

**출처:** boriu-hold-2000-2019/state/work.sqlite3; src/render_contract.py, work_queue.py; folder note/direct-observations

**관측·실행 근거:** 현재 DB의 artifact 이력 58행과 고유 페이지 18쪽을 직접 조회했습니다. 새 출력 15개와 현행 엔진·구 엔진의 구분은 노트에 근거합니다. render_contract 전체를 보존했습니다.

**당시 판단과 연결:** 원본 코드와 노트에서 delta/restore/cache/finish_deferred의 실패와 수정을 확인했습니다. 이 구현만으로 2,230쪽 전체를 완료했다고 기록하지 않습니다.

<a id="e18"></a>

## E18 — 보류 페이지 OCR 중심의 독립 완료

**출처:** 후기 보류 해소 경로의 new-boryu/reports/FINAL_AUDIT_2001_2019.json; FINAL_VERIFICATION_2000; continuous state/manifest; src/engine_continuous.py

**관측·실행 근거:** 현재 최종 audit를 직접 조회했습니다. complete 2,035쪽, partial 0, unprocessed 0이었으며 source/human 상태는 false였습니다. 2000년의 195쪽은 노트와 해당 완료 기록에 근거합니다.

**당시 판단과 연결:** 제공된 9/19 memory 두 개에는 사용자가 빠른 텍스트 1차 처리와 자신의 최종 육안 검토를 선택한 이유가 남아 있습니다. 범위를 held_pages로 좁혔고, 기존 ID의 자동 연결은 inference로 기록했습니다.

<a id="e19"></a>

## E19 — supplement와 후기 검토의 왕복

**출처:** supplement-2000-2019 및 imsi-2013-2018의 manifest/exports/decisions; 해당 두 folder notes

**관측·실행 근거:** 노트 전체를 읽었습니다. 현재 대상 3,949쪽은 로컬 완료 3,800쪽과 변경 없음 149쪽으로 나뉩니다. 검토 export 76/200/78의 수신 연결을 확인했습니다. 270쪽 초안의 렌더는 0이며 후속 201쪽 적용은 별도 사건입니다.

**당시 판단과 연결:** 제공된 9/20 memory의 tight-mask revision에는 서식 선보다 이름 전체를 기준으로 삼고 1px의 여유를 두며 토큰 상자를 분리하라는 판단이 남아 있습니다. 한 글자 화자·회전·제외 처리는 후속 사용자가 지정한 범위에 따랐습니다.

<a id="e20"></a>

## E20 — 결재란 적용·되돌리기·고정 칸

**출처:** seal-sign-masking/reports/nonboundary_remediation_rollback.json; cell7_migration/director_repair; src/masking.py; folder note

**관측·실행 근거:** 현재 masking.py 전체를 보존했습니다. 12,194 / 53,816의 집계는 노트에서 직접 대조했습니다. 호출 측의 3·5·7번 칸 설정과 함수 기본값인 3·5번 칸을 구분했습니다.

**당시 판단과 연결:** 제공된 9/13~14 memory에서 대상 3,004쪽 중 2,632쪽 적용과 사용자 요청에 따른 rollback 과정을 모두 읽었습니다. 후속 고정 칸 처리와 7번 칸 추가는 노트의 시점별 기록에 근거합니다.

<a id="e21"></a>

## E21 — 연락처 refit과 승인된 빈틈 보정

**출처:** game/phone_mail_masking_webp/tools/refit_contacts_20260922.py, refit_recover_components_20260922.py; reports/gap_masking_20260922/verification.json; contact note

**관측·실행 근거:** 원본 함수를 읽고 발췌했습니다. 노트는 3,518쪽 refit, 실제 마스크와 불일치한 108행의 회복, 면적 48.72% 감소를 기록합니다. 최종 출력 3,594쪽은 숫자 연도 3,563쪽과 Unknown 31쪽의 합입니다.

**당시 판단과 연결:** 제공된 9/22 memory에서 밀착·구분 기호·합집합·방향별 테두리 지시를 확인했습니다. 76쪽의 근거 82건에서 영역 90개를 실제 적용했으며 기존 출력 3,518개는 보존했습니다.

<a id="e22"></a>

## E22 — 최초 전체 레이어 합성

**출처:** final-tri-force/src/compose.py, prepare.py; work/supplement_update_20260923/before/reports/final_verification.json; folder note

**관측·실행 근거:** compose 전체를 보존하고, prepare.py가 restore·복원 상자를 받아 prior_target_rects를 전달하는 것을 확인했습니다. 보관된 초기 검증을 직접 조회했습니다. 출력 66,010개와 입력 219,031개 검증은 저장 보고에 근거하며, 현재 이미지 66,010개는 별도로 직접 셌습니다.

**당시 판단과 연결:** 제공된 9/22~23 memory에서 숫자 연도 선택, 하위 이름 보존과 상위 영역 우선, 후기 supplement 추가를 사용자의 명시적인 결정으로 확인했습니다.

<a id="e23"></a>

## E23 — 후속 통합의 수신 증거

**출처:** final-tri-force/reports/final_verification.json; backup/202609250005/apply_verification.json; final-boriu-zebal/final-tri-force folder notes

**관측·실행 근거:** 현재 최상위 검증 보고의 1,893쪽 부분집합과 backup의 1,538쪽 적용을 직접 조회했습니다. 1,893쪽 중 픽셀이 바뀐 것은 1,892쪽이었습니다. 노트의 현재 ready 1,539쪽을 별도 1쪽과 연결했습니다.

**당시 판단과 연결:** 생산자가 source_merged=false를 기록한 뒤 수신 측에서 실제 통합한 시점 차이를 확인했습니다. 생산자와 수신자의 서로 다른 시점을 연결했습니다.

<a id="e24"></a>

## E24 — 최종 이미지에서 새 OCR

**출처:** final-tri-force/ocr/_tools/vision_ocr_multiprocess.swift; ocr/_reports/verification.json; 62/52 selected refresh reports; final folder note

**관측·실행 근거:** Swift 전체를 보존했습니다. 현재 숫자 연도의 OCR JSON 5,330개를 읽어 66,010쪽·1,992,165줄·빈 페이지 7쪽을 재집계했습니다. 이 집계에서 현재 이미지 전체의 해시를 새로 대조한 것은 아닙니다. bbox 줄 15개·13쪽은 저장 보고에 근거합니다.

**당시 판단과 연결:** 8/21 이미지 우선 계획(E02) 이후의 전체 실행 2회와 선택 재생성은 최종 노트의 영수증으로 연결했습니다. 원본 bbox 보존, 빈 페이지에 대한 사용자 확인, Unicode 검증 수정을 함께 기록했습니다.

<a id="e25"></a>

## E25 — 과거 토큰 재생과 exact bbox

**출처:** final-tri-force: one-page eight-token applied_receipt; backup/202609250849/logs/verification.json; final folder note

**관측·실행 근거:** 15쪽·26영역의 영수증을 직접 조회했습니다. 1쪽의 토큰 8개에 대한 과거 glyph 재생과 비대상 보존은 해당 memory와 노트를 연결했습니다.

**당시 판단과 연결:** 제공된 9/24 memory에서 사용자가 이유부터 요청한 뒤, 최신 receipt만 본 준비 오류를 확인하고 8개만 2+2글자·13px로 고치도록 승인한 흐름을 확인했습니다. staff의 입력 bbox 밖에 있는 획을 유지한 것은 사용자가 명시한 범위에 따른 결과입니다.

<a id="e26"></a>

## E26 — 최상위 manifest와 후속 수정의 시점

**출처:** folder-notes/final-tri-force/EVIDENCE.md, 직접근거 및 final-boriu note; 현재 이미지/OCR/backup 연결

**관측·실행 근거:** 노트는 현재 해시·OCR·후속 receipt를 맞춰 stale 상태인 최상위 행의 표본을 확인했습니다. 이번 조사에서는 최종 JSON 전체의 집계를 새로 확인했으며 stale 행의 총수는 집계하지 않았습니다.

**당시 판단과 연결:** 현재 파일명만을 최종 권위로 삼지 않고 수정 event의 시점별로 읽었습니다. 과거 ready 수와 현재 ready 수의 차이도 구분했습니다.

<a id="e27"></a>

## E27 — tmptest 실패 수리와 운영 코드 반영

**출처:** tmptest/TMPTEST_CHANGES_20260907.md; stabilization/runs/04.json~07.json; stabilization/promotion.json; reports/test_2019_3_episodes_round07/result.json.

**당시 문제·판단:** 회전 좌표, 실제 잉크와 단순 상자 교차의 차이, 옅은 이웃 행, 한 쪽짜리 회차의 신원 문맥 부족이 문제였습니다. 이미 읽은 판단을 고정하고 기하를 재검증했습니다. 발견한 두 이름에 한해 다른 회차의 OCR을 참조하되 처리 큐는 확대하지 않았습니다. 이 판단은 당시 변경 내역과 실행별 보고에 기록돼 있습니다.

**실제 결과:** 4번째 실행에서는 1문서 완료·2문서 보류, 5번째 실행에서는 새 기하 사례 실패, 6번째 실행에서는 회귀 통과, 7번째 실행에서는 17쪽 완료(11 verified + 6 no_changes)가 남았습니다. 이름 삭제/토큰은 35/35였습니다. promotion에는 코드 8개·fixture 3개·문서 3개의 전후 해시와 적용·검증 시각이 있습니다. operating_data_merged=false였습니다.

**후속 연결:** 운영 큐 5,330문서·66,010쪽의 pending 상태를 유지하며 코드를 반영했습니다. 공개 보존 [spatial.py](../../../history/historical/names/spatial.py)의 해시는 반영 기록의 공간 변환 코드 해시와 같습니다. 테스트 신원·토큰을 운영 결과로 합치지 않았습니다.

<a id="e28"></a>

## E28 — read-v2의 제작 이후 실제 텍스트 실행

**출처:** 보관 ZIP voku-read-v2.zip 내부 state/pipeline.sqlite3; audit/migration.json; stages/01_text/checkpoints; stages/01_text/decisions; 9/7 18:12 및 18:25 시작 memory.

**당시 문제·판단:** 단일 feedback 패키지의 첫 한 쪽은 신원 판단 후 좌표/Vision 단계에서 실패했습니다. 사용자가 1단계만 진행하도록 요청해 RUN_PROMPT_STAGE1.md를 추가하고 후속 텍스트 처리를 실행했습니다.

**실제 결과:** ZIP DB의 text_state는 inherited 4,009 / read 85 / pending 61,916쪽이었습니다. submitted packet은 3개, open은 1개였으며 신규 read 페이지의 출력은 0개였습니다. checkpoint는 첫 1쪽 뒤 추가 4문서·73쪽과 1문서·11쪽의 제출을 기록합니다. 두 후속 memory의 geometry_started=false와 일치합니다.

**후속 연결:** 제출된 신원·분류와 다음 미제출 packet을 보존했습니다. 이미지 생산 전체 완료로 진행한 기록이나 주 처리에 역이관한 연결은 없습니다. 제작 시점의 미시작 문장을 패키지 전체 이력으로 쓰던 이전 서술을 정정했습니다.

<a id="e29"></a>

## E29 — read-next의 출발점과 82쪽 실제 실행

**출처:** voku-read-next/reports/MIGRATION.json, migration_verification.json; state/queue.sqlite3; 해당 work/programs의 session.json·정식 submission·source-review; 9/8 최적화/이주 memory와 9/9 실제 재개 memory.

**당시 문제·판단:** 주 처리에서 편성 전체 판독·compact 표시를 구현한 뒤, 수동 JSON 조립과 마무리 명령 반복을 줄이려고 별도 세션 패키지로 복사했습니다. 입력 전달과 실제 판독 선언을 분리했습니다.

**실제 결과:** 한 session에서 7문서·82쪽·3,651 OCR unit을 처리했으며 read_documents는 7, commit은 1이었습니다. 해당 문서의 현재 DB는 11 verified / 64 no_changes / 7 partial입니다. output_rel에 연결된 물리 파일은 18개(verified+partial)이며 program 상태는 running입니다. 당시 session-close는 review 단계였고 사용자 지정 연필 이름 보류와 기하 검토가 남았습니다.

**충돌 해소:** README/STOP_POINT는 복사 직후의 미시작 상태를 기록했습니다. 이후의 실제 제출·출력과 시점이 다릅니다. 이 제출분을 주 처리로 역이관한 기록은 확인되지 않았습니다. 사용자 요청과 달리 Python으로 제출 JSON을 조립한 실행상의 이탈도 memory에 기록돼 있습니다.

<a id="e30"></a>

## E30 — 1차 처리와 재작업을 나누라는 사용자 정정

**출처:** 9/10 independent hold rework memory; voku-read-only-masking/reports/held_episode_analysis_20260910의 summary·cached_range_diagnostics·extent_span_diagnostics와 개선 제안; 기존 folder note의 현재 상태 대조.

**당시 문제·판단:** 사용자는 1차 패키지를 재작업 실행기로 사용하지 않도록 정정하고, 당시에는 계획만 요청했습니다. 의미 큐가 소진된 세션에서 과거 보류에 접근하면 연도 소유권 검사에 막혔습니다. 완료 앱의 issue와 hold/partial 페이지는 당시 서로 겹치지 않았습니다.

**실제 결과:** 보류 원인은 기계 문제만 2,768쪽 / 의미 문제만 1,087쪽 / 혼합 426쪽 / 빈 OCR 6쪽으로 나뉘었습니다. 설계는 기존 결정을 읽기 전용 자료원으로 받아 외부에서 쟁점을 해결하고 페이지별 결과를 만드는 방향이었습니다. 당시 설계와 뒤의 E16~19 실제 구현을 구분합니다.

**후속 연결:** 원천 결과를 고치지 않는 초기·후기 보류 처리와 완료본 교정으로 이어졌습니다. 좌표계·page 연결·이전 출력·영수증을 수신한 별도 후속 결과가 E22의 합성 입력이 됐습니다.

<a id="e31"></a>

## E31 — 누락됐던 후기 이름 보정 경로

**출처:** voku_2000_2019_planning_bundle_local_paths/reports/review-selection-audit/REPORT.md; voku-name-repair/STATUS.md, _internal/reports/MIGRATION_AND_TEST_REPORT.md, UPDATE_REPORT.md, outputs; 9/14 선정 정정·이주, 9/15 호환 수정·생산 중단 memory.

**당시 문제·판단:** 빈 needs_review를 제외한 selector가 사람이 표시한 문제를 3쪽으로 축소했습니다. 메모·bbox·fingerprint의 유무보다 저장된 수동 상태의 시간순 이력을 사용하도록 수정했습니다. OCR을 우선해 새 연결·누락만 판단하라는 요청에 따라 패키지를 이주했습니다.

**실제 결과:** 선정 대상은 1,805쪽(1,803 needs_review + 2 issue)이며, 기계 후보가 0개인 4쪽도 포함했습니다. 과거 token_layout=null인 1,652항목·975쪽에 대한 호환 수정과 격리 검사 126개가 있었습니다. 잘못 복사한 표시 경로가 원래 이미지 한 개를 삭제한 사건은 동일 해시 복구와 시험 격리 수정으로 기록했습니다.

**진행·출처 경계:** 마지막 STOP 보고와 memory는 51/457편성 처리, 52편성 OCR 대조, 출력 279개를 기록하며 현재 물리 출력도 279개입니다. 현재 _internal/runs/production에는 숨김 메타데이터만 남아 있어, 해당 진행 상태를 현재 DB 재집계로 표현하지 않습니다. 최종 합성의 입력 목록에 이 279개가 들어간 연결은 확인되지 않았습니다.

<a id="e32"></a>

## E32 — 최종 합성 뒤의 이름 누락 조사와 가이드 전달

**출처:** tri-force-gumsu/reports/summary.json, AUDIT_COMPLETE.json; CURRENT_SCOPE.json, bbox-guide/data/scope_exclusions.json; final-tri-force/reports/BBOX_GUIDES_UPDATE_201.json; 9/23 조사/후속 통합 memory; supplement folder note.

**당시 문제·판단:** 사용자는 결재란 자체가 아니라 그 처리 페이지의 결재란 밖 이름을 조사하도록 범위를 정했습니다. 이름 레이어가 없는 554쪽도 곧바로 누락으로 판정하지 않고 후보·픽셀·기존 대상을 대조했습니다.

**실제 결과:** 최종 저장 조사의 범위는 12,194쪽이었습니다. 실제 검토 후보는 1,684개·1,337쪽, 누락 확인은 1,137쪽, 추가 판단은 20쪽이며 두 집합은 2쪽이 겹쳤습니다. 확인된 이름들이 유효 대상 목록에 빠져 있었고, 조사 보고는 final merge loss evidence=false와 repair_performed=false를 기록했습니다.

**충돌·후속 연결:** memory의 초기 조사 중단 설명 뒤에 저장된 AUDIT_COMPLETE/summary가 있어 최종 조사 결과를 추가했습니다. 270쪽 초안에서 기존 처리 106쪽과 겹치는 41쪽을 제외해 229쪽 가이드가 됐습니다. 이후 28쪽 제외·201쪽 적용은 별도 결정이며, 수신 보고는 394개 연산과 다른 65,809쪽의 보존을 확인했습니다. 1,137쪽 조사 전체를 이 201쪽 적용과 같게 세지 않습니다.

<a id="e33"></a>

## E33 — Luna v3의 실제 재개와 보고 정정

**출처:** voku-luna-economy-v3/workspace.json; .state/STOP_AFTER_ACTIVE.json; .state/maintenance/approval-revocation-20260906; 9/6 재개·drain memory.

**당시 문제·판단:** 기존 완료분·가명·큐를 재사용하고 실제 Luna 작업자에게 원본·bbox·결과 검토를 맡겼습니다. 작업자의 완료 보고가 서명·날짜 겹침과 렌더 제한의 실제 결과에 어긋나, 승인 취소 → hold 경로를 보완했습니다.

**실제 결과:** 계약상 gpt-5.6-luna/max 작업자는 최대 3개이며 작업자당 최대 6쪽을 맡았습니다. STOP JSON에서 stopped, 활성 0, 미수집 0, drain 13쪽 = 12 masked + 1 hold를 직접 확인했습니다. 중앙 데이터는 voku-ocr-v3를 사용했습니다.

**후속 연결:** 승인 취소를 원자적·멱등적으로 처리하는 경로와 중단 상태를 남겼습니다. E10의 적용 전 중단된 제한 시험과는 별도 실행입니다.

<a id="e34"></a>

## E34 — 저장 OCR 줄 재기입의 별도 실행

**출처:** OCR 읽기 전용 실험의 voku-ocr-readonly/README.md; scripts/pipeline.py; _state/progress_history.jsonl; 2017/receipts 및 masking/redacted_webp.

**당시 처리 계약:** 새 OCR·직접 이미지 열람 없이 저장된 bbox를 사용했습니다. 정밀 bbox가 없으면 retypes_whole_line=true로 기록하고 1순위 OCR의 주변 문자열과 이름 토큰을 줄 전체에 다시 그렸습니다. 이 범위 선택은 당시 문서·코드로 확인했으며, 후대 주 처리로 전환한 이유는 추정하지 않았습니다.

**실제 결과:** 9/5 22:16~23:32 KST의 영수증은 59개·644쪽이며, 상태는 OCR_ONLY_PROCESSED 414 / OCR_ONLY_WITH_FLAGS 230이었습니다. 실제 출력 210개와 영수증의 output SHA-256 210개가 일치했습니다. applied의 saved_ocr_line_bbox는 538건이었습니다. progress와 summary의 40회차·485쪽·출력 153개는 중간 집계입니다.

**후속 연결:** 현재 자료는 별도 적용의 존재와 좌표 타협을 보여 줍니다. 이 결과를 주 처리로 이관하거나 폐기한 결정은 연결되지 않았습니다.

<a id="e35"></a>

## E35 — 연도별 명단 통합의 별도 결과

**출처:** staff-identity/test-spark/VOKU_Staff_Roster_2006-2019/manifest.json, validation_report.json; 9/3 역할별 worker 명단 통합 memory.

**실제 결과:** 연도 파일 14개, 연도별 인물 281명, resolved assignment 969건, 검토 204건이었습니다. 검토는 학과 충돌 20건 / 배정 미해결 132건 / 사용 불가 worker 상태 52건으로 나뉩니다. identity_scope=year_only, cross_year_merge=false이며 저장된 검증 13개를 통과했습니다.

**연결:** 역할별 결과를 연도 내부에서 통합한 산출물입니다. 281명을 전 기간의 고유 인원수로 바꾸지 않으며, 뒤의 운영 명단 전체와 행별로 승계된 연결은 미확인입니다.
