# 데이터셋 정리

모든 데이터셋은 Roboflow 포맷(YOLO, `data.yaml` + `train/valid/test`)이다. 원본 압축 파일은 용량 문제로 git에서 제외되어 있으며(`_archive/duplicate_zips/`), 필요 시 재다운로드하거나 압축 해제된 폴더를 그대로 사용한다.

| 폴더 | 상태 | 규모 (train/valid/test) | 비고 |
|---|---|---|---|
| `phase-of-cell-6/` | **현재 채택 (주력)** | 2,460 / 61 / 61 | Roboflow `chinnaphat-hwhdt`. 클래스 불균형 있음 (interphase 66%, 나머지 각 7~14%) |
| `Onion-Cell-Merged-v5-2/` | 실험 실패 | - | 여러 데이터셋 병합 시도, 학습 실패 원인 미파악 — 재시도 전 원인 조사 필요 |
| `cell_OB_yolo11/` | 보조/구버전 | ~184 images | `_archive/duplicate_zips/cells_OB_yolov11.zip`과 동일 원본 압축본 보관 중 |
| `Mitosis-1/` | 보조/구버전 | 40 images | 초기 mitosis 실험용 소규모 데이터셋 |
| `test_image_dir/` | 수동 테스트용 | 4 images | 학습에 사용하지 않음, 추론 스팟체크용 |

## 정리 이력 (2026-07-26)

- `cells_OB_yolov11.zip`, `cells_yolov11.zip` → `_archive/duplicate_zips/`로 이동 (이미 압축 해제된 `cell_OB_yolo11/`, `Mitosis-1/`과 내용 중복)
- 세포 분열 프로젝트와 무관한 `rock-paper-scissors/`, `RockPaperScissors.zip`은 워크스페이스의 별도 폴더(`../rock-paper-scissors-project/`)로 이동
