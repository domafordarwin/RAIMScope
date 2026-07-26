from ultralytics import YOLO
import torch

def train_model():
    # 1. Mac GPU(MPS) 사용 가능 여부 확인
    if torch.backends.mps.is_available():
        device = "mps"
        print("🚀 Mac GPU(MPS)를 사용하여 학습을 시작합니다!")
    else:
        device = "cpu"
        print("⚠️ MPS를 찾을 수 없어 CPU로 학습을 진행합니다.")

    # 2. YOLOv11 기본 모델 로드 (가장 가볍고 빠른 Nano 모델 사용)
    # 성능을 더 높이고 싶다면 "yolo11s.pt" (Small) 모델로 변경하셔도 됩니다.
    model = YOLO("yolo11n.pt")

    # 3. 모델 학습 시작
    results = model.train(
        data="data.yaml",        # 다운로드 받은 데이터셋의 설정 파일 경로
        epochs=50,               # 전체 데이터셋을 반복 학습할 횟수 (필요시 조절)
        imgsz=640,               # 이미지 크기 (YOLO 기본값)
        batch=16,                # 한 번에 학습할 이미지 수 (메모리 부족 시 8로 낮춤)
        device=device,           # mps (Mac GPU)
        project="onion_project", # 학습 결과가 저장될 최상위 폴더 이름
        name="pretrain_mitosis", # 이번 학습 결과가 저장될 하위 폴더 이름
        plots=True               # 학습 결과 그래프 자동 생성
    )
    
    print("✅ 사전 학습이 완료되었습니다!")

if __name__ == "__main__":
    train_model()
