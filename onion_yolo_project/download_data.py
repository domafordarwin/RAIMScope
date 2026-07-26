import os
import shutil
import zipfile
from pathlib import Path
from dotenv import load_dotenv
from roboflow import Roboflow


# ============================================================
# Roboflow Universe 후보 분석 결과
# ------------------------------------------------------------
# 1순위:
#   workspace: foo
#   project  : mitosis-wuz7h
#   version  : 3
#   format   : yolov8
#
# 이유:
#   - 객체 탐지(object-detection) 데이터셋
#   - 클래스가 체세포 분열 단계와 가장 유사함
#   - YOLOv11 detect 학습용 사전학습 데이터로 적합
# ============================================================

DATASET_CONFIG = {
    "workspace": "foo",
    "project": "mitosis-wuz7h",
    "version": 3,
    "format": "yolov8",
    "location": "./dataset_pretrain",
}


def inspect_download_result(location: str):
    """
    Roboflow SDK가 실패했을 때 생성한 roboflow.zip이
    진짜 ZIP인지, XML/HTML/JSON 에러 응답인지 확인한다.
    """
    location_path = Path(location)
    zip_path = location_path / "roboflow.zip"

    print("\n🔍 다운로드 결과 검사")

    if not location_path.exists():
        print(f"❌ 다운로드 폴더가 없습니다: {location_path}")
        return

    if not zip_path.exists():
        print("❌ roboflow.zip 파일이 없습니다.")
        print("현재 폴더 내용:")
        for p in location_path.rglob("*"):
            print("-", p)
        return

    print(f"파일 위치: {zip_path}")
    print(f"파일 크기: {zip_path.stat().st_size} bytes")

    first_bytes = zip_path.read_bytes()[:10]
    print(f"시작 바이트: {first_bytes}")

    if first_bytes.startswith(b"PK"):
        print("✅ ZIP 파일 형식으로 보입니다.")

        try:
            with zipfile.ZipFile(zip_path, "r") as zf:
                bad_file = zf.testzip()
                if bad_file is None:
                    print("✅ ZIP 무결성 검사 통과")
                else:
                    print(f"❌ ZIP 내부 손상 파일 발견: {bad_file}")
        except zipfile.BadZipFile:
            print("❌ ZIP 파일처럼 보이지만 실제로는 손상되었습니다.")
    else:
        print("❌ 정상 ZIP 파일이 아닙니다.")
        print("\n파일 내용 일부:")
        try:
            text = zip_path.read_text(errors="ignore")
            print(text[:1000])
        except Exception as e:
            print("파일 내용을 읽을 수 없습니다:", e)


def verify_yolo_dataset(location: str):
    """
    YOLO 학습에 필요한 data.yaml과 images/labels 구조가 있는지 확인한다.
    """
    location_path = Path(location)
    data_yaml = location_path / "data.yaml"

    print("\n📁 YOLO 데이터셋 구조 확인")

    if not data_yaml.exists():
        print("❌ data.yaml 파일이 없습니다.")
        print("다운로드 또는 압축 해제가 제대로 완료되지 않았을 수 있습니다.")
        return False

    print("✅ data.yaml 발견:", data_yaml)

    expected_dirs = [
        location_path / "train",
        location_path / "valid",
        location_path / "test",
    ]

    for d in expected_dirs:
        if d.exists():
            print(f"✅ {d} 폴더 있음")
        else:
            print(f"⚠️ {d} 폴더 없음")

    print("\n📄 data.yaml 내용:")
    print("-" * 60)
    print(data_yaml.read_text(errors="ignore"))
    print("-" * 60)

    return True


def download_datasets():
    load_dotenv()
    api_key = os.getenv("ROBOFLOW_API_KEY")

    if not api_key:
        print("❌ 오류: .env 파일에서 ROBOFLOW_API_KEY를 찾을 수 없습니다.")
        return

    workspace_id = DATASET_CONFIG["workspace"]
    project_id = DATASET_CONFIG["project"]
    version_number = DATASET_CONFIG["version"]
    export_format = DATASET_CONFIG["format"]
    location = DATASET_CONFIG["location"]

    print("🚀 사전 학습용 체세포 분열 데이터셋 다운로드 시작")
    print(f"Workspace : {workspace_id}")
    print(f"Project   : {project_id}")
    print(f"Version   : {version_number}")
    print(f"Format    : {export_format}")
    print(f"Location  : {location}")

    # 이전 실패 다운로드 결과 삭제
    if Path(location).exists():
        print(f"\n🧹 기존 폴더 삭제: {location}")
        shutil.rmtree(location)

    rf = Roboflow(api_key=api_key)

    try:
        project = rf.workspace(workspace_id).project(project_id)
        version = project.version(version_number)

        dataset = version.download(
            export_format,
            location=location
        )

        print("\n✅ Roboflow 다운로드 완료")
        print("저장 위치:", dataset.location)

        verify_yolo_dataset(location)

    except Exception as e:
        print("\n❌ 다운로드 실패")
        print("오류 유형:", type(e).__name__)
        print("오류 내용:", e)

        inspect_download_result(location)

        print("\n해결 방법:")
        print("1. Roboflow 웹에서 해당 데이터셋 Version 3 페이지에 접속")
        print("2. Download Dataset → YOLOv8 → Generate/Export 다시 실행")
        print("3. Show Download Code에서 workspace/project/version 값 재확인")
        print("4. 필요하면 curl 다운로드 링크로 직접 다운로드")


if __name__ == "__main__":
    download_datasets()