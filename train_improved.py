"""
phase-of-cell-6 detection — 개선 학습 스크립트
개선 포인트:
  1. yolo11s (nano → small, 파라미터 약 3배)
  2. imgsz=800 (세포 미세 특징 포착)
  3. cos_lr=True (수렴 개선)
  4. patience=50 (조기 종료 여유)
  5. degrees=10 (세포는 방향 무관 — 회전 증강)
  6. mixup=0.1 (클래스 경계 학습 강화)
  7. 2단계 학습: backbone freeze(10) → 전체 학습
"""

from pathlib import Path
from ultralytics import YOLO

DATA = "phase-of-cell-6/data.yaml"
RUN_NAME = "phase_cell_improved_v1"

COMMON = dict(
    data=DATA,
    imgsz=800,
    batch=8,          # imgsz 800이므로 batch 줄임 (MPS 메모리)
    device="mps",
    workers=4,
    cos_lr=True,
    degrees=10.0,     # 세포 이미지 회전 불변성
    mixup=0.1,
    mosaic=1.0,
    patience=50,
    save=True,
    plots=True,
    verbose=True,
)

# ── 1단계: backbone freeze, head만 학습 (30 epoch) ──────────────────────────
print("=" * 60)
print("Stage 1: Backbone freeze (head warm-up, 30 epochs)")
print("=" * 60)

model = YOLO("yolo11s.pt")  # 자동 다운로드
results_s1 = model.train(
    **COMMON,
    epochs=10,
    freeze=10,        # backbone 10 layer 고정
    lr0=0.01,
    name=f"{RUN_NAME}_stage1",
)

stage1_best = Path(model.trainer.best)
print(f"\nStage1 best weights: {stage1_best}")

# ── 2단계: 전체 레이어 파인튜닝 ───────────────────────────────────────────
print("=" * 60)
print("Stage 2: Full fine-tuning (all layers, 200 epochs)")
print("=" * 60)

model2 = YOLO(str(stage1_best))
results_s2 = model2.train(
    **COMMON,
    epochs=20,
    freeze=None,      # 전체 학습
    lr0=0.001,        # stage1보다 낮은 lr
    name=f"{RUN_NAME}_stage2",
)

# ── 최종 결과 요약 ──────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("최종 결과 요약")
print("=" * 60)

import csv
for stage, run_name in [("Stage1", f"{RUN_NAME}_stage1"), ("Stage2", f"{RUN_NAME}_stage2")]:
    csv_path = Path(f"runs/detect/{run_name}/results.csv")
    if csv_path.exists():
        with open(csv_path) as f:
            rows = list(csv.DictReader(f))
        best = max(rows, key=lambda r: float(r["metrics/mAP50(B)"]))
        print(f"{stage} best → mAP50: {float(best['metrics/mAP50(B)']):.4f} | "
              f"mAP50-95: {float(best['metrics/mAP50-95(B)']):.4f} | "
              f"epoch: {int(float(best['epoch']))}")
