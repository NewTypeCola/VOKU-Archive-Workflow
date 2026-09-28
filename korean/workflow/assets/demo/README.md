# 데모 자산

[English](../../../../workflow/assets/demo/README.md)

세 회차 폴더에는 PDF의 물리 페이지 49쪽 전체가 세워 읽는 논리면 53개로 들어 있습니다. 두 면이 있는 원고 4쪽에는 안전 입력과 최종 결과를 재조립한 이미지도 있습니다. 보호할 개인 식별정보는 가상화했으며 공개 인명, 학과와 입학년도는 유지했습니다.

## 살펴보기

일반 폴더 또는 이미지 목록을 엽니다: [1994](1994/complete/README.md), [2003](2003/complete/README.md), [2017](2017/complete/README.md). 압축을 풀 필요는 없습니다. 각 폴더에는 `demo-source-safe/`와 `final/`의 WebP 이미지, `page-map.json`, 확정된 `operations.json`, `ocr/`의 편집하지 않은 Apple Vision 결과와 `manifest.json`이 있습니다.

기존 PNG 158개는 모두 해상도를 유지했습니다. 전체 회차 이미지 114개는 손실 WebP quality=90, method=6을 사용하고, 대표 그림 44개는 무손실 WebP입니다. [변환 기록](../../../../workflow/assets/demo/format-conversion.json)은 이전 PNG 해시, 중간 무손실 WebP 해시, 현재 파일과 디코딩 픽셀 해시를 보존합니다. 품질 90 이미지는 앞선 무손실 버전과 픽셀이 같지 않습니다.

배포된 압축 안전 입력에서 확정 연산을 다시 실행하고 최종 이미지를 품질 90으로 인코딩했습니다. 합성은 인코딩 전 단계에서 선언한 영역 안의 픽셀만 변경합니다. operations.json의 과거 레이어 해시는 원래 run-v4 PNG 중간 산출물을 가리키며, 압축 입력 재생과 인코딩 전 픽셀 해시는 별도로 기록합니다. 교정한 2017 페이지는 `current_layers` 픽셀 해시도 기록합니다. 두 면 원고는 배포 논리면을 정확히 재조립한 뒤 별도의 품질 90 인코딩을 수행합니다.

안전 입력과 최종 WebP는 Apple Vision으로 실제 판독했습니다. 취소 표시를 고친 뒤에는 변경된 최종 7면만 다시 읽고 비대상 페이지 객체를 유지했습니다. 모든 OCR sourceSHA256은 이 공유 자산 폴더를 기준으로 한 sourceRel의 파일과 일치합니다. OCR 텍스트와 좌표를 수동으로 고치지 않았습니다.

## 보호 처리 결과 재생

Python 3, Pillow, numpy와 기록된 macOS Apple SD Gothic Neo 글꼴을 사용합니다. 글꼴은 재배포하지 않습니다. 스크립트는 글꼴의 SHA-256을 검사하고 다르면 중단합니다. 바이트까지 같은 WebP 출력에는 operations.json에 기록된 Pillow/libwebp 버전을 사용하며 디코딩 픽셀 해시도 검사합니다.

저장소 루트의 공유 자산 폴더 `workflow/assets/demo/`에서 다음을 실행합니다.

```sh
python3 -m pip install Pillow numpy
python3 replay.py 2017/complete --out rebuilt-2017
```

이름 지움·토큰, 결재칸 처리와 연락처 마스크를 재생하고 각 영역을 합성한 뒤 모든 최종 WebP 해시를 검사합니다. 신원 판단은 이미 확정되어 있습니다. 재생은 OCR을 실행하지 않습니다. 새 OCR은 [보존 Swift 구현](../../../../history/historical/ocr/vision_ocr_multiprocess.swift)으로 별도 생성했습니다.

[데모의 작업 과정](../../demo.md#decisions-to-repair)과 `decisions.json`은 판단의 출처와 검토 뒤 바뀐 사항을 설명합니다. 재생 코드는 확정 연산의 렌더러이며 에이전트의 판독·판단 과정이 아닙니다. 모든 이름을 지운 뒤 토큰을 배치하고, `input_cancelled`인 staff 토큰의 이름 레이어에 새 1px 취소선을 그립니다. 2+2 토큰에는 줄마다 선 하나를 넣으며 원래 이름 획은 복원하지 않습니다.

비공개 준비 자료, 원본 crop, 실명–가상 이름 대응표와 ImageGen 참조 프롬프트는 제외했습니다. 공개 source-safe 이미지가 재생의 출발점입니다.

## 그림과 근거

`overview.webp`, 장면 비교 그림과 `2017/composition.gif`는 실제 처리 픽셀로 만들었습니다. GIF는 서로 다른 PDF 두 쪽을 보여줍니다. `*-regions.webp`는 설명용 기하 오버레이입니다. 대체 이름과 학적 정보 비교, GIF의 이름 장면은 취소 표시 보정을 반영합니다. 영향받지 않은 다른 그림은 앞선 처리 픽셀을 유지합니다.

`2017/input-review.webp`는 안전 입력 준비 당시의 고정된 비교 그림입니다. `2017/token-repair.webp`는 이름 전체를 먼저 지운 뒤 토큰을 놓도록 고쳤을 때의 이전·교정 비교이며 취소 표시 보정 이전입니다. 이 과거 이미지는 근거로 보존하며 현재 최종본으로 다시 표시하지 않습니다. 원시 OCR 발췌도 수동 교정하지 않습니다. [개정 검증](../../../../workflow/assets/demo/revision-verification.json)은 변경 출력, 유지 입력, 대표 이미지 출처와 검사를 기록합니다.

`execution-summary.json`은 실제 범위·버전·코드 재사용·수정·검토·검사를 기록합니다. `decisions.json`에는 가상 신원과 공개 판단 사례가 있습니다. `asset-manifest.json`은 현재 공개 Workflow 파일의 목록과 해시입니다.
