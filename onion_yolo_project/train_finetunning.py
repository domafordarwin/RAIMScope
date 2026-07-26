from ultralytics import YOLO
import torch

def finetune_model():
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    
    # 🌟 핵심: 기본 모델이 아닌, 우리가 방금 학습시킨 '사전 학습 가중치'를 불러옵니다.
    pretrained_weights = "runs/detect/onion_project/pretrain_mitosis/weights/best.pt"
    model = YOLO(pretrained_weights)

    print("🚀 양파 체세포 5단계 분류 파인튜닝을 시작합니다!")

    # 파인튜닝 학습 시작
    results = model.train(
        data="./dataset_onion/Mitosis/data.yaml",
        epochs=150,              # 100 → 150으로 증가
        imgsz=640,
        batch=8,                 # 소규모 데이터셋엔 작은 배치가 더 안정적
        device=device,
        lr0=0.0005,              # 학습률 더 낮춤 (사전학습 지식 보존)
        lrf=0.01,                # 최종 lr = lr0 * lrf
        cos_lr=True,             # cosine LR 스케줄러 (수렴 안정성)
        warmup_epochs=5,         # 초반 5 epoch warmup
        freeze=10,               # 백본 앞 10개 레이어 고정 → 헤드만 먼저 학습
        patience=30,             # 30 epoch 개선 없으면 early stop
        augment=True,
        mosaic=0.5,              # mosaic 확률 낮춤 (소규모 데이터 과증강 방지)
        mixup=0.1,
        project="onion_project",
        name="finetune_v2",
        plots=True
    )
    
    print("✅ 양파 체세포 파인튜닝이 모두 완료되었습니다!")

if __name__ == "__main__":
    finetune_model()
