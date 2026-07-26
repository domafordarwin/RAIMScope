import os
import glob
from ultralytics import YOLO

def find_latest_best_pt():
    all_best_pts = glob.glob("**/*best.pt", recursive=True)
    return max(all_best_pts, key=os.path.getmtime) if all_best_pts else None

def analyze_video():
    model_path = find_latest_best_pt()
    if not model_path: return print("❌ 모델을 찾을 수 없습니다.")
    
    model = YOLO(model_path)
    
    # 분석할 동영상 파일 경로 (프로젝트 폴더에 test_video.mp4를 넣어주세요)
    video_path = "./outData/Mitosis.mp4" 
    
    if not os.path.exists(video_path):
        return print(f"❌ '{video_path}' 파일을 찾을 수 없습니다. 동영상을 준비해 주세요.")

    print("🚀 동영상 분석을 시작합니다. (시간이 조금 걸릴 수 있습니다...)")
    
    # predict 대신 track을 사용하면 프레임 간 동일한 세포를 추적(ID 부여)합니다.
    results = model.track(
        source=video_path,
        conf=0.25,
        iou=0.5,
        save=True,
        project="onion_project",
        name="video_results"
    )
    
    save_dir = results[0].save_dir
    print(f"🎉 동영상 분석 완료! 결과가 {save_dir} 에 저장되었습니다.")
    os.system(f"open '{save_dir}'")

if __name__ == "__main__":
    analyze_video()
