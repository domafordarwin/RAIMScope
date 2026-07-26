import os
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi

def download_midog_from_kaggle():
    api = KaggleApi()
    api.authenticate()


    dataset_name = "amarnassnaalhajali/midog-2021"

    download_path = "./kaggle_mitosis_data"
    os.makedirs(download_path, exist_ok = True)

    print(f"kaggle에서 '{dataset_name}' 데이터셋 다운로드를 시작합니다.")

    api.dataset_download_files(dataset_name, path = download_path, unzip=True)

    print(f"다운로드 및 압축 해체가 완료되었습니다! (저장위치: {download_path})")


if __name__ == "__main__":
    download_midog_from_kaggle()

