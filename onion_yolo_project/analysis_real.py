import glob
from ultralytics import YOLO

def find_latest_best_pt():
    all_best_pts = glob.glob("**/*best.pt", recursive=True)
    return max(all_best_pts, key=os.path.getmtime) if all_best_pts else None

def analyze_realtime():
    model_path = find_latest_best_pt()
    if not model_path: return print("❌ 모델을 찾을 수 없습니다.")
    
    model = YOLO(model_path)
    
    print("🚀 실시간 카메라 분석을 시작합니다!")
    print("⚠️ 종료하려면 카메라 창을 클릭하고 키보드의 'q' 키를 누르세요.")
    
    # source="0"은 Mac의 기본 웹캠입니다. 
    # 외부 USB 현미경을 연결했다면 "1" 또는 "2"로 변경해 보세요.
    model.predict(
        source="0", 
        show=True,  # 화면에 실시간으로 띄움
        conf=0.25
    )

if __name__ == "__main__":
    analyze_realtime()
