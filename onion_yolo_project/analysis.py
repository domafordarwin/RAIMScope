import os
import glob
import csv
from ultralytics import YOLO

def find_latest_best_pt():
    all_best_pts = glob.glob("**/*best.pt", recursive=True)
    return max(all_best_pts, key=os.path.getmtime) if all_best_pts else None

def analyze_and_save_csv():
    model_path = find_latest_best_pt()
    if not model_path: return print("❌ 모델을 찾을 수 없습니다.")
    
    model = YOLO(model_path)
    source_folder = "./outData"
    
    print("🚀 이미지 분석 및 개수 카운팅 시작...")
    results = model.predict(source=source_folder, conf=0.25, save=True, project="onion_project", name="csv_results")
    
    # CSV 파일 생성 준비
    csv_filename = "cell_counts_result.csv"
    with open(csv_filename, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        # 엑셀 헤더(첫 줄) 작성
        writer.writerow(["파일명", "Interphase(간기)", "Prophase(전기)", "Metaphase(중기)", "Anaphase(후기)", "Telophase(말기)", "총합"])
        
        # 각 이미지별 결과 분석
        for r in results:
            img_name = os.path.basename(r.path)
            # 클래스별 개수를 저장할 딕셔너리 (0~4)
            counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
            
            # 검출된 박스들의 클래스 번호를 확인하여 개수 증가
            for cls in r.boxes.cls:
                counts[int(cls)] += 1
                
            total = sum(counts.values())
            # CSV에 한 줄씩 기록
            writer.writerow([img_name, counts[0], counts[1], counts[2], counts[3], counts[4], total])
            
    print(f"🎉 분석 완료! 개수 결과가 '{csv_filename}' 파일로 저장되었습니다.")
    os.system(f"open '{csv_filename}'") # Mac에서 CSV 파일 자동 실행

if __name__ == "__main__":
    analyze_and_save_csv()
