# RAIMScope

현미경 이미지에서 세포 분열 단계(interphase / metaphase / anaphase / telophase)를 자동 탐지하는 YOLOv11 기반 프로젝트.

## 현재 최고 성능

- 모델: YOLOv11s
- 데이터셋: `phase-of-cell-6/`
- mAP50: **0.7666** | mAP50-95: 0.4179 | Precision: 0.7644 | Recall: 0.7489
- 클래스별 mAP50: metaphase 0.919 / anaphasae 0.803 / telophase 0.789 / interphase 0.558 (최약점)
- 가중치: `models/phase_cell_v1_best.pt` (원본 학습 로그: `runs/detect/phase_cell_improved_v1_stage2/`)

## 학습 실행

학습 스크립트가 사용하는 가상환경은 `onion_yolo_project/.venv`에 위치한다 (레거시 프로젝트 폴더지만 현재도 공용 venv로 사용 중).

```bash
source onion_yolo_project/.venv/bin/activate
python train_improved.py
```

`train_improved.py`는 2단계 학습을 수행한다:
1. Stage1: backbone freeze, head warm-up (10 epoch)
2. Stage2: 전체 레이어 파인튜닝 (20 epoch)

## 디렉토리 구조

```
RAIMScope/
├── train_improved.py        # 현재 활성 학습 파이프라인 (phase-of-cell-6 기반)
├── phase-of-cell-6/          # 주력 학습 데이터셋 (Roboflow)
├── Onion-Cell-Merged-v5-2/   # 병합 시도 데이터셋 (학습 실패, 원인 미확인)
├── cell_OB_yolo11/           # 보조 데이터셋
├── Mitosis-1/                # 보조 데이터셋
├── models/                   # 승격된 최고 성능 가중치 보관
├── runs/                     # 현재 유효한 학습 로그만 유지 (오래된 실험은 _archive/ 참고)
├── onion_yolo_project/       # 레거시 파이프라인 (yolo11n 기반 초기 실험, pretrain/finetune)
├── Docs/                     # 세포 분열 관련 참고 자료 (PDF)
├── _archive/                 # 정리 과정에서 보관한 중복 데이터셋 zip, 오래된 runs 실험 (git 미추적)
└── test_image_dir/           # 수동 추론 테스트용 샘플 이미지
```

자세한 데이터셋 설명은 [DATASETS.md](DATASETS.md) 참고.

## 미해결 이슈

- interphase 클래스 탐지율 낮음 (mAP50 0.558) — background로 오탐 43%
- `Onion-Cell-Merged-v5-2` 병합 데이터 학습 실패 원인 미파악
