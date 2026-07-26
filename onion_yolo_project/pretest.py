from ultralytics import YOLO
import glob
import os

def run_inference():
    # 1. 방금 학습이 완료된 best.pt 가중치 로드
    # (이전 로그에 출력된 경로를 그대로 사용합니다)
    model_path = "runs/detect/onion_project/pretrain_mitosis/weights/best.pt"
    model = YOLO(model_path)

    # 2. 테스트할 이미지 선택
    # dataset_pretrain/test/images/ 폴더 안에 있는 첫 번째 이미지를 자동으로 가져옵니다.
    # (원하는 특정 이미지 경로가 있다면 "test_image.jpg" 처럼 직접 입력하셔도 됩니다.)
    test_images = glob.glob("./test/images/*.jpg")
    
    if not test_images:
        print("❌ 테스트 이미지를 찾을 수 없습니다. 경로를 확인해 주세요.")
        return
        
    test_image_path = test_images[0]
    print(f"🔍 테스트 이미지 분석 중: {test_image_path}")

    # 3. 추론(예측) 실행
    # conf=0.3 : 신뢰도가 30% 이상인 박스만 표시 (NMS 경고를 줄이고 확실한 것만 보기 위함)
    # save=True : 결과 이미지를 폴더에 저장
    results = model.predict(
        source=test_image_path,
        conf=0.6,
        iou=0.4,
        save=True,
        project="onion_project",
        name="predict_results"
    )
    
    # 4. 결과 저장 위치 안내
    save_dir = results[0].save_dir
    print(f"✅ 추론 완료! 결과 이미지가 다음 경로에 저장되었습니다: {save_dir}")

if __name__ == "__main__":
    run_inference()
