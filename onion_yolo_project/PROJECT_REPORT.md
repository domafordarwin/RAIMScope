# 양파 체세포 분열 탐지 프로젝트 보고서

**작성일**: 2026-05-14  
**프로젝트**: RAIMScope / onion_yolo_project  
**목표**: YOLOv11 기반 양파 체세포 분열 단계 자동 탐지 모델 개발

---

## 1. 프로젝트 개요

현미경 이미지/영상에서 양파 뿌리 세포의 분열 단계를 자동으로 탐지하는 Object Detection 모델을 구축한다.
YOLOv11n을 베이스로 체세포 분열 데이터로 사전학습(pretrain)한 뒤, 양파 특화 데이터로 파인튜닝(finetune)하는 2단계 전이학습 전략을 사용했다.

---

## 2. 환경

| 항목 | 값 |
|------|-----|
| 모델 베이스 | YOLOv11n (`yolo11n.pt`) |
| Ultralytics | 8.4.48 |
| PyTorch | 2.11.0 |
| 학습 디바이스 | Mac MPS (Apple Silicon GPU) |
| Python 가상환경 | `.venv` (프로젝트 로컬) |

---

## 3. 데이터셋

### 3-1. 사전학습용 (Pretrain)
- **출처**: Roboflow Universe — `foo / mitosis-wuz7h` (v3)
- **파일**: `dataset_pretrain/mitosis.v3-slava-marlow-3.yolov11.zip`
- **클래스 (4종)**: `ana-telophases`, `interphase`, `metaphase`, `prophase`
- **구조**: `train/` · `valid/` · `test/` (프로젝트 루트 기준)
- **상태**: ✅ 정상

### 3-2. 파인튜닝용 (Finetune)
- **출처**: Roboflow Universe — `noah-mitchell-cr4tb / mitosis-hncem` (v1)
- **파일**: `dataset_onion/Mitosis.v1i.yolov11.zip` → `dataset_onion/Mitosis/`
- **클래스 (4종)**: `Anaphase`, `Metaphase`, `Prophase`, `Telophase`
- **구조**: `dataset_onion/Mitosis/train|valid|test/`
- **상태**: ✅ 정상 (초기 `roboflow.zip`은 GCS 링크 만료로 XML 에러였으나 재다운로드 완료)

---

## 4. 학습 결과

### 4-1. 사전학습 (Pretrain)

| 항목 | 값 |
|------|-----|
| 실행 경로 | `runs/detect/onion_project/pretrain_mitosis/` |
| 가중치 | `weights/best.pt`, `weights/last.pt` |
| Epochs | 50 / 50 완료 |
| 최종 mAP@50 | **0.790** |
| 최종 mAP@50-95 | **0.764** |
| Precision | 0.369 |
| Recall | 0.322 |

> mAP@50이 0.79로 준수한 수준. 사전학습 가중치가 체세포 분열 패턴을 충분히 학습함.

### 4-2. 파인튜닝 (Finetune)

| 항목 | 값 |
|------|-----|
| 실행 경로 | `runs/detect/onion_project/finetune_onion_phases-3/` |
| 기반 가중치 | `pretrain_mitosis/weights/best.pt` |
| 가중치 | `weights/best.pt`, `weights/last.pt` |
| Epochs | 100 / 100 완료 |
| 최종 mAP@50 | **0.362** |
| 최종 mAP@50-95 | **0.203** |
| Precision | 0.265 |
| Recall | 0.512 |
| 학습률 (lr0) | 0.001 (낮게 설정 — 기존 지식 보존) |

> ⚠️ 사전학습 대비 mAP@50이 크게 하락(0.79 → 0.36). 파인튜닝 데이터셋이 소규모이거나
> 클래스 분포 불균형, 또는 추가 하이퍼파라미터 튜닝이 필요한 상태.

---

## 5. 실행 파일 목록

| 파일 | 역할 | 상태 |
|------|------|------|
| `download_data.py` | 사전학습 데이터 다운로드 (Roboflow) | ✅ |
| `download_onion.py` | 파인튜닝 데이터 다운로드 (Roboflow) | ✅ |
| `download_kaggle.py` | Kaggle 데이터 다운로드 (보조) | - |
| `train_pretrain.py` | 사전학습 실행 | ✅ 완료 |
| `train_finetunning.py` | 파인튜닝 실행 | ✅ 완료 |
| `pretest.py` | 사전학습 모델 추론 테스트 | ✅ |
| `test_final.py` | 파인튜닝 모델 추론 테스트 | ✅ (실행 가능) |
| `analysis_video.py` | 동영상 세포 추적 분석 | ✅ (영상 필요) |

---

## 6. 추론 / 테스트 결과

| 실행 | 저장 경로 |
|------|----------|
| 사전학습 모델 추론 × 4회 | `runs/detect/onion_project/predict_results(-2~-4)/` |
| 파인튜닝 모델 최종 테스트 × 2회 | `runs/detect/onion_project/final_test_results(-2)/` |
| 동영상 세포 추적 분석 | `runs/detect/onion_project/video_results/Mitosis.mp4` |
| outData 배치 추론 | `runs/detect/onion_project/outData_results/` |

---

## 7. 현재 이슈 및 개선 방향

### 이슈
1. **파인튜닝 mAP 저하** — 사전학습(0.79) 대비 파인튜닝(0.36)으로 성능 하락
2. **파인튜닝 시도 흔적 3건** — `finetune_onion_phases`, `-2`, `-3` 폴더 존재 (초기 data 경로 오류로 실패)

### 개선 방향
| 항목 | 제안 |
|------|------|
| Epochs 증가 | 100 → 150~200으로 늘려 수렴 확인 |
| 더 큰 모델 | `yolo11n.pt` → `yolo11s.pt` 또는 `yolo11m.pt` |
| 학습률 스케줄러 | `cosine` 스케줄러 또는 warmup 조정 |
| 데이터 증강 | `augment=True`, `mosaic`, `mixup` 강화 |
| Freeze 레이어 | 백본 레이어 고정 후 헤드만 먼저 학습 |
| 데이터 추가 | 파인튜닝 데이터셋이 소규모 → 추가 확보 필요 |

---

## 8. 다음 단계

```
1. test_final.py 실행 → 파인튜닝 모델 정성 평가
2. 성능 개선 실험 (위 개선 방향 적용)
3. analysis_video.py → 실제 현미경 영상으로 세포 추적 검증
```

---

*generated: 2026-05-14 | model: YOLOv11n | framework: Ultralytics 8.4.48*
