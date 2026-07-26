# RAIMScope 점검 보고서 (2026-07-26, 검토 반영 개정판)

> 본 문서는 최초 작성본을 `REVIEW_OF_ANALYSIS_REPORT_2026-07-26.md`의 검증 결과에 따라 전면 수정한 개정판이다. 원본의 핵심 결론(학습 자체는 성공, 원인은 클래스 스키마 불일치)은 유지하되, 수치 오류·과도한 인과 단정·용어 혼용·보안 점검 누락을 정정했다.

## 개요

이번 점검은 세 가지 축으로 진행됐다.
1. 프로젝트 구조 전반의 정리 필요성 점검 및 정리 작업 수행
2. `Onion-Cell-Merged-v5-2` 데이터셋 병합 학습이 "실패"로 기록된 원인 조사
3. (개정) 위 두 항목에 대한 독립 검토·검증 및 보안 점검

---

## 0. 보안 조치 (최우선, 개정 시 추가)

**심각도: 매우 높음 — 검토 과정에서 신규 발견**

Git이 추적하던 `Yolo11_Exec_01.ipynb`에 Roboflow API 키(`u1LNm...YM9f`)가 평문으로 포함되어 있었고, 프로젝트 초기 정리 커밋(`5178dfe`)을 통해 GitHub 원격 저장소(`domafordarwin/RAIMScope`)에 이미 push된 상태였다.

**조치 완료:**
1. 노트북의 하드코딩된 키를 `os.getenv("ROBOFLOW_API_KEY")` 방식으로 교체 (같은 노트북의 다른 셀들이 이미 사용하던 패턴과 통일)
2. `git filter-repo --replace-text`로 전체 Git 이력(모든 커밋의 블롭)에서 해당 문자열을 제거
3. `git push --force`로 원격 이력을 정리된 이력으로 교체
4. `.env` 자체는 애초에 Git에 커밋된 적이 없음을 확인 (`git log --all -- .env` 결과 없음)

**사용자 조치 필요 (본 조치와 별개):** 이미 공개 이력에 노출됐던 키이므로, Roboflow 콘솔에서 해당 키를 폐기하고 재발급해야 한다. 단순 이력 삭제만으로는 키가 노출됐던 시점에 제3자가 이미 확보했을 가능성을 배제할 수 없다.

---

## 1. 프로젝트 구조 점검

### 발견된 문제점

| 영역 | 문제점 |
|---|---|
| 버전 관리 | 프로젝트 전체가 git 저장소가 아니었음 — 코드/실험 변경 이력 추적 불가 |
| 프로젝트 혼재 | 세포분열 탐지와 무관한 `rock-paper-scissors/`, `RockPaperScissors.zip`이 루트에 섞여 있음 |
| 데이터 중복 | `cells_OB_yolov11.zip`, `cells_yolov11.zip`이 이미 압축 해제된 `cell_OB_yolo11/`, `Mitosis-1/`과 내용 중복 |
| 실험 결과 누적 | `runs/detect/`에 정리되지 않은 추론 결과(`predict-*`)와 구버전 mitosis 실험이 다수 누적 |
| 파이프라인 혼선 | `onion_yolo_project/`(레거시 yolo11n 파이프라인)와 루트의 최신 `train_improved.py`(yolo11s, phase-of-cell-6 기반)가 구분 없이 병존 |
| 문서 부재 | 루트에 README, 데이터셋 설명 문서 없음 |
| 캐시/시스템 파일 | `.ipynb_checkpoints`, `__pycache__`, `.DS_Store`가 정리되지 않고 방치됨 |
| **보안 (개정 시 추가)** | **Git 이력에 평문 API 키 포함 — 0장 참고** |

### 조치 내역

- git 저장소 초기화 후 기존 GitHub 원격 저장소(`domafordarwin/RAIMScope`, 설문조사·발표자료 보유)와 `--allow-unrelated-histories`로 병합 — 양쪽 이력 모두 보존
- `rock-paper-scissors/`, `RockPaperScissors.zip` → 워크스페이스 별도 폴더(`../rock-paper-scissors-project/`)로 분리
- 중복 zip, 오래된 `runs/predict-*` 및 구버전 실험 → `RAIMScope/_archive/`로 이동 (git 미추적, 디스크에는 보존 — 삭제 아님)
- `runs/detect/`에는 현재 유효한 `phase_cell_improved_v1_stage1/2`만 남김
- 현재 최고 성능 가중치를 `models/phase_cell_v1_best.pt`로 승격
- `README.md`, `DATASETS.md` 신규 작성 (이후 0장 반영해 추가 수정, 3장 참고)
- `.gitignore` 정비 (venv, 데이터셋, `*.pt`, `*.zip`, `.bkit/`, 캐시 등 제외)
- macOS 파일명 유니코드 정규화(NFD/NFC) 불일치 문제 발견 및 수정
- (개정 시 추가) 노트북 평문 API 키 제거 및 Git 이력 정리 — 0장 참고

### 용량·실험 수 표기에 대한 주의 (개정 시 추가)

최초 정리 작업 당시 `runs/detect/`에는 정리 전 기준 `predict-2`~`predict-18` 등을 포함해 약 40개에 가까운 실험이 있었고 용량은 약 572MB로 측정됐다. 이후 `_archive/`로 이동을 완료한 현재 시점 기준으로는:

- `_archive/runs_root/`: 약 470 MiB (detect 실험 36개, segment 실험 7개)
- 현재 `runs/`: 약 87 MiB (`phase_cell_improved_v1_stage1/2`만 유지)
- `_archive/duplicate_zips/`: 약 21 MiB

측정 시점(정리 전/후)과 포함 범위에 따라 수치가 달라지므로, 위와 같이 시점을 명시해 기록한다.

### 보류한 항목

- `onion_yolo_project/.venv`(약 1.2GiB, 십진 단위 약 1.3GB)는 그대로 유지 — venv 내부에 절대경로가 하드코딩되어 있어 이동 시 깨질 위험이 있고, `train_improved.py` 실행 시에도 이 venv를 그대로 사용 중이므로 손대지 않음. 다만 장기적으로는 재현 가능한 `requirements.txt`/잠금 파일을 정비하고, 새 가상환경에서 학습 스크립트가 정상 동작함을 확인한 뒤 레거시 폴더와 실행환경의 결합을 해소하는 것이 바람직하다.

---

## 2. `Onion-Cell-Merged-v5-2` 학습 실패 원인 조사

### 점검 방법

`Yolo11_Exec_01.ipynb`에 남아있는 실제 실행 로그(cell 44~68)를 셀 단위로 재구성하여 실행 순서, 코드 변경, 학습 로그, 추론 결과를 대조했다. 추가로 `ultralytics.data.utils.check_det_dataset()`을 직접 호출해 `data.yaml` 경로 해석 결과를 검증했고, 개정 과정에서 `mitosis_yolo11n_detect-2`·`mitosis_yolo11n_640-6`의 `args.yaml`/`results.csv` 원자료 및 전체 YOLO 라벨 파일을 재대조했다.

### 점검 결과

**(1) `data.yaml`의 `../train/images` 상대경로 — 실제로는 무해했음**

`Onion-Cell-Merged-v5-2/data.yaml`은 `train: ../train/images`처럼 상위 폴더를 가리키는 경로를 갖고 있어 언뜻 치명적 버그로 보였다. 그러나 `check_det_dataset()`으로 직접 검증한 결과, ultralytics가 내부 탐색 로직으로 올바른 경로(`Onion-Cell-Merged-v5-2/train/images`)를 정상적으로 찾아냈다. 즉 이 경로 문제는 실제 학습 실패의 원인이 아니다. 다만 이 동작은 Ultralytics의 경로 보정 로직에 의존하므로, 이식성과 명확성을 위해 YAML의 `train`/`val`/`test` 값을 `../` 없이 `train/images` 형태로 정규화하는 것은 여전히 권장된다.

**(2) 노트북 내 실제 버그: 수정본 저장 위치 오타**

Cell 45~46에서 경로를 바로잡은 새 yaml(`yaml_onion`)을 만들었지만, 저장 대상이 `Onion-Cell-Merged-v5-2/data.yaml`이 아니라 존재하지 않는 `Mitosis-15/data.yaml`(오타, 실제 폴더명은 `Mitosis-1`)이었다. 의도한 수정은 반영되지 않았으나, (1)에서 확인했듯 애초에 그 수정이 필요하지 않았기 때문에 결과에는 영향이 없었다.

**(3) 실제 학습 결과: 성공**

Cell 52에서 YOLO11n으로 100 epoch 학습이 조기 중단이나 크래시 없이 정상 완료됐다. 마지막(100번째) epoch와, 학습 종료 후 best checkpoint를 다시 검증한 결과는 서로 다른 값이므로 구분해서 기록한다.

| 시점 | Precision | Recall | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|
| 마지막(100번째) epoch | - | - | **0.895** | - |
| best checkpoint 재검증 | 0.874 | 0.831 | **0.899** | 0.714 |

best checkpoint의 클래스별 mAP50: `d` 0.828, `nd` 0.970.

크래시나 미수렴 등 기술적 "실패"로 볼 근거가 없다. 다만 이 결과는 동일 데이터셋 내부 validation 성능일 뿐, 다른 현미경 환경에 대한 일반화 성능이나 실제 서비스 적합성까지 입증하지는 않는다 — 별도 test 평가 또는 외부 데이터 검증이 필요하다.

**(4) 근본 원인 — 클래스 스키마 불일치**

`Onion-Cell-Merged-v5-2`는 `['d', 'nd']` (dividing / non-dividing) 2-class 라벨만 갖는다. 반면 프로젝트가 채택한 스키마는 `interphase / metaphase / anaphase / telophase` 4-class(`phase-of-cell-6` 기준)다. `d`는 여러 분열 상태를 하나의 클래스에 뭉뚱그렸을 수 있어 특정 phase 하나에 직접 대응시킬 수 없고, `nd`가 프로젝트의 `interphase`와 완전히 같은 정의인지도 별도 검증이 필요하다.

따라서 **두 데이터셋의 라벨을 변환 없이 그대로 합쳐 동일한 4-class 모델을 학습하는 것은 불가능**하다 — 다만 이것이 이 데이터셋을 어떤 방식으로도 활용할 수 없다는 뜻은 아니다. 활용하려면 원본 라벨을 목표 클래스에 맞게 재라벨링하거나, 클래스 정의를 검증한 계층형·멀티태스크 파이프라인("먼저 분열 여부를 검출하고, 분열 중인 경우에만 phase를 분류")을 설계해야 한다. 코드 버그가 아니라 데이터셋 선정·설계 단계의 한계다.

부수적으로 클래스 불균형도 관찰된다. 전체 YOLO 라벨을 재집계한 결과는 다음과 같다.

| 분할 | `d` | `nd` | 합계 |
|---|---:|---:|---:|
| train | 2,103 | 12,499 | 14,602 |
| valid | 533 | 3,369 | 3,902 |
| test | 277 | 1,737 | 2,014 |
| 전체 | **2,913** | **17,605** | **20,518** |

전체 비율은 약 14.2 : 85.8이다. 소수 클래스인 `d`의 mAP50(0.828)이 `nd`(0.970)보다 낮게 나타났고, 클래스 불균형이 이 차이에 영향을 주었을 가능성이 있다. 다만 이 mAP50 차이의 원인을 불균형만으로 단정할 수는 없다 — 객체 크기, 형태 다양성, 시각적 난이도, 라벨 품질 등 다른 요인도 함께 작용할 수 있으며, 인과관계를 확정하려면 추가 실험이 필요하다.

**(5) 기존 메모리에 기록된 "학습 실패" 메모의 실제 출처 (해석, 미확정)**

노트북 실행 순서는 다음과 같다: Cell 52(`Onion-Cell-Merged-v5-2` 학습) → Cell 54(`mitosis_yolo11n_detect-2` 체크포인트 로드) → Cell 55(`cell_OB_yolo11/valid/images` 추론) → Cell 56 마크다운 메모("어떤 이유에인지 전혀 학습이 되지 않아 일단은 후퇴").

셀 배치와 실행 순서를 고려하면 이 메모는 Cell 52가 아니라 바로 앞 Cell 55의 결과, 즉 `cell_OB_yolo11` 데이터로 학습된 `mitosis_yolo11n_detect-2` 모델의 추론 결과를 지칭했을 가능성이 가장 높다. 보존된 `args.yaml`으로 이 모델이 실제로 `cell_OB_yolo11/data.yaml`을 사용해 학습됐음이 확인되며, `results.csv`상 마지막 epoch(50)의 검증 mAP50은 약 0.207에 불과했다. 같은 추론에서 일부 이미지는 실제 라벨에 없는 Interphase를 70개 이상 검출하는 등 과다한 false positive도 확인된다.

다만 다음은 증거보다 강한 단정이므로 완화한다.

- 메모가 이 실험을 가리킨다는 것은 셀 순서에 근거한 **유력한 해석**일 뿐, 작성자의 명시적 설명이 없어 확정적 사실로 단정할 수 없다.
- 모델 성능 저하의 원인을 "과적합"으로 단정하지 않는다 — 낮은 검증 mAP50과 과다 false positive는 확인되지만, 과적합/미수렴/라벨 품질/해상도/하이퍼파라미터 중 무엇이 실제 원인인지는 별도 진단이 필요하다.
- 다수의 중복 검출을 전부 "중복 검출"로 단정하지 않고, "과다 false positive"로 서술한다.

즉 기존 메모리에 기록된 "Onion-Cell-Merged 병합 데이터 학습 실패"는, 최소한 노트북 상의 실행 순서로 볼 때 이 데이터셋 자체(Cell 52)가 아니라 그 직전 별개 실험(Cell 55, `cell_OB_yolo11` 기반 `detect-2` 모델)을 가리켰을 가능성이 높다는 것이 본 조사의 결론이다.

### 용어에 대한 주의 (개정 시 추가)

- 프로젝트의 네 클래스(`interphase / metaphase / anaphase / telophase`)는 표준적인 체세포분열(mitosis)의 4단계와 완전히 일치하지 않는다. Interphase는 일반적으로 유사분열 자체의 한 단계로 분류되지 않으며, 표준 4단계에 포함되는 Prophase가 이 스키마에는 없다. 과학적 표준 분류와 이 프로젝트가 채택한 데이터셋 클래스 체계는 구분해서 설명해야 한다.
- 현재 모델은 YOLO 객체 탐지 모델이므로, 기술적으로는 "phase 분류"보다 "세포 위치 검출 + 상태 클래스 예측을 함께 수행하는 4-class 객체 탐지"로 서술하는 것이 정확하다.
- `phase-of-cell-6/data.yaml`의 클래스명 `anaphasae`는 `anaphase`의 오탈자로 보인다. 클래스 인덱스를 바꾸지 않고 표시 이름만 정정할 수 있는지 검토가 필요하며, 이미 생성된 가중치의 클래스명 메타데이터·학습 결과 문서·GUI 표시 이름도 함께 확인해야 한다.

### 결론

> `Onion-Cell-Merged-v5-2`를 사용한 YOLO11n 학습은 100 epoch를 정상 완료했으며, best checkpoint의 내부 validation mAP50은 0.899(마지막 epoch 기준 0.895)였다. 따라서 해당 실험은 기술적인 학습 실패로 볼 수 없다.
>
> 다만 이 데이터셋의 클래스는 `d/nd` 이진 스키마이고, 현재 프로젝트의 목표는 `interphase/metaphase/anaphase/telophase` 4-class 객체 탐지이므로 라벨을 그대로 유지한 직접 병합은 불가능하다. 활용하려면 원본 라벨을 목표 클래스에 맞게 재라벨링하거나, 클래스 정의를 검증한 계층형·멀티태스크 파이프라인을 설계해야 한다.
>
> 노트북 Cell 56의 "학습이 되지 않았다"는 메모는 셀 순서상 `cell_OB_yolo11`로 학습한 `mitosis_yolo11n_detect-2`의 낮은 검증 성능(mAP50 약 0.207)과 과다 false positive를 지칭했을 가능성이 높다. 그러나 작성자의 명시적 설명이 없으므로 메모의 대상을 확정적으로 단정할 수는 없다.

### 후속 조치 제안

1. 이 데이터셋을 phase 분류에 활용하려면 `d` 라벨을 phase별로 재라벨링하거나, 별도의 보조 태스크("분열 여부 우선 검출 → phase 분류")로 파이프라인을 분리해야 한다. `d`/`nd` 각각의 정의와 원천 데이터 라벨링 정책도 먼저 확인해야 한다.
2. `mitosis_yolo11n_detect-2` 모델이 왜 낮은 성능을 보였는지는 별도로 진단되지 않았다 (과적합/미수렴/라벨 품질/해상도 등 후보 원인 중 미확정) — 필요 시 추가 점검 대상
3. Onion 데이터의 test split 또는 외부 데이터로 독립 평가 수행 검토
4. `anaphasae` 오탈자 정정 계획 수립 (클래스 인덱스 유지, 표시 이름만 정정)
5. 기존 메모리(`project_raimscope.md`)와 `README.md`, `DATASETS.md`의 "Onion-Cell-Merged-v5-2 병합 데이터 학습 실패 (원인 미확인)" 관련 기록을 본 보고서의 개정된 결론으로 갱신 필요 (3장 참고)

---

## 3. 문서 간 상태 정합성 (개정 시 추가)

검토 시점 기준으로 `README.md`, `DATASETS.md`가 여전히 `Onion-Cell-Merged-v5-2`를 "학습 실패, 원인 미확인" 또는 "실험 실패"로 표기하고 있어 본 보고서의 결론과 모순됐다. 두 문서를 본 개정판의 결론(학습은 성공, 원인은 클래스 스키마 불일치)에 맞춰 갱신했다.
