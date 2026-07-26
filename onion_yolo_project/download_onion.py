import os
import zipfile
from pathlib import Path
from dotenv import load_dotenv
from roboflow import Roboflow

def download_onion_data():
    load_dotenv()
    api_key = os.getenv("ROBOFLOW_API_KEY")
    if not api_key:
        print("❌ .env 파일에서 ROBOFLOW_API_KEY를 찾을 수 없습니다.")
        return

    rf = Roboflow(api_key=api_key)

    print("🚀 양파 체세포 분열(5단계) 데이터셋 다운로드 중...")
    # Roboflow에 공개된 양파 세포 분열 단계 데이터셋
    project = rf.workspace("onion-cell").project("phase-of-cell")
    try:
        dataset = project.version(1).download("yolov8", location="./dataset_onion")
    except zipfile.BadZipFile:
        zip_path = Path("dataset_onion/roboflow.zip")
        print("❌ Roboflow가 정상 ZIP이 아닌 응답을 반환했습니다.")
        if zip_path.exists():
            preview = zip_path.read_text(errors="ignore")[:500]
            print("\n다운로드 응답 일부:")
            print(preview)
        print("\nRoboflow 웹에서 해당 dataset version의 export를 다시 생성한 뒤 재시도해 주세요.")
        return
    
    print("✅ 양파 데이터셋 다운로드 완료! (저장 위치: ./dataset_onion)")
    print("저장 위치:", dataset.location)

if __name__ == "__main__":
    download_onion_data()
