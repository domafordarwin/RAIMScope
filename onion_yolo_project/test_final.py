import os
import glob
from ultralytics import YOLO

def find_latest_best_pt():
    print("🔍 학습된 모델(best.pt)을 자동으로 찾는 중...")
    all_best_pts = glob.glob("**/*best.pt", recursive=True)
    
    if not all_best_pts:
        return None
        
    latest_best_pt = max(all_best_pts, key=os.path.getmtime)
    return latest_best_pt

def test_final_model():
    # 1. 모델 로드
    model_path = find_latest_best_pt()
    
    if not model_path:
        print("❌ 모델 가중치(best.pt)를 찾을 수 없습니다.")
        return

    print(f"✅ 모델을 찾았습니다! 경로: {model_path}")
    model = YOLO(model_path)

    # 2. 분석할 폴더 지정 (outData 폴더)
    source_folder = "./outData"
    
    # 폴더가 존재하는지 확인
    if not os.path.exists(source_folder):
        print(f"❌ '{source_folder}' 폴더를 찾을 수 없습니다. 프로젝트 폴더 안에 outData 폴더를 만들고 사진을 넣어주세요.")
        return

    print(f"🚀 '{source_folder}' 폴더 안의 모든 이미지 분석을 시작합니다...")

    # 3. 추론(예측) 실행 - source에 폴더 경로를 통째로 넣습니다!
    results = model.predict(
        source=source_folder,
        conf=0.25,  # 신뢰도 25% 이상
        iou=0.5,    # 겹침 허용치 50%
        save=True,  # 결과 이미지 저장
        project="onion_project",
        name="outData_results" # 결과가 저장될 새 폴더 이름
    )
    
    # 4. 결과 확인 및 폴더 자동 열기 (Mac 전용)
    if results:
        save_dir = results[0].save_dir
        print(f"🎉 모든 이미지 분석 완료! 결과가 다음 경로에 저장되었습니다: {save_dir}")
        print("📂 결과 폴더를 화면에 띄웁니다...")
        
        # 사진이 여러 장이므로, 사진 대신 '결과 폴더' 자체를 엽니다.
        os.system(f"open '{save_dir}'")
    else:
        print("⚠️ 분석할 이미지가 없거나 분석에 실패했습니다.")

if __name__ == "__main__":
    test_final_model()
