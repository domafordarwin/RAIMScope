# 데이터셋 정리

모든 데이터셋은 Roboflow 포맷(YOLO, `data.yaml` + `train/valid/test`)이다. 원본 압축 파일은 용량 문제로 git에서 제외되어 있으며(`_archive/duplicate_zips/`), 필요 시 재다운로드하거나 압축 해제된 폴더를 그대로 사용한다.

| 폴더 | 상태 | 규모 (train/valid/test) | 비고 |
|---|---|---|---|
| `phase-of-cell-6/` | **현재 채택 (주력)** | 2,460 / 61 / 61 | Roboflow `chinnaphat-hwhdt`. 클래스 불균형 있음 (interphase 66%, 나머지 각 7~14%) |
| `Onion-Cell-Merged-v5-2/` | 학습 성공, 목표 스키마와 비호환 | 452 / 129 / 63 (`d`+`nd` 인스턴스 합계 20,518, 비율 약 14.2:85.8) | YOLO11n 100 epoch 정상 완료, best checkpoint mAP50 0.899. 다만 클래스가 `d`/`nd` 2종(이진 분열 여부)이라 프로젝트의 4-class phase 스키마와 라벨 변환 없이 직접 병합 불가능. 자세한 내용은 `ANALYSIS_REPORT_2026-07-26.md` 참고 |
| `cell_OB_yolo11/` | 보조/구버전 | ~184 images | `_archive/duplicate_zips/cells_OB_yolov11.zip`과 동일 원본 압축본 보관 중 |
| `Mitosis-1/` | 보조/구버전 | 40 images | 초기 mitosis 실험용 소규모 데이터셋 |
| `test_image_dir/` | 수동 테스트용 | 4 images | 학습에 사용하지 않음, 추론 스팟체크용 |

## 정리 이력 (2026-07-26)

- `cells_OB_yolov11.zip`, `cells_yolov11.zip` → `_archive/duplicate_zips/`로 이동 (이미 압축 해제된 `cell_OB_yolo11/`, `Mitosis-1/`과 내용 중복)
- 세포 분열 프로젝트와 무관한 `rock-paper-scissors/`, `RockPaperScissors.zip`은 워크스페이스의 별도 폴더(`../rock-paper-scissors-project/`)로 이동
