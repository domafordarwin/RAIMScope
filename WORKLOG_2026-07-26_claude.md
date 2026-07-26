# 작업 내역 (2026-07-26, Claude)

> 이 문서는 Claude Code 세션에서 진행한 작업만 기록한다. Codex 등 다른 도구로 진행된 작업은 포함하지 않는다.

## 1. 프로젝트 구조 분석 및 정리

**요청:** 프로젝트 구조 분석 및 개선 제안 → 승인 범위(P0+P1) 실행

- 발견한 문제점: git 미사용, 무관한 프로젝트(rock-paper-scissors) 혼재, 데이터셋 zip 중복, `runs/`에 정리 안 된 실험 40개 가까이 누적, 레거시(`onion_yolo_project/`)와 현재 파이프라인 병존, 문서 부재, 캐시 파일 방치
- 조치:
  - git 저장소 초기화 → 기존 GitHub 원격(`domafordarwin/RAIMScope`, 설문/발표자료 보유)과 `--allow-unrelated-histories`로 병합, 양쪽 이력 보존
  - `rock-paper-scissors/`, `RockPaperScissors.zip` → 워크스페이스 별도 폴더(`../rock-paper-scissors-project/`)로 이동
  - 중복 zip, 오래된 `runs/predict-*` 및 구버전 실험 → `_archive/`로 이동 (삭제 아님, git 미추적)
  - `runs/detect/`는 현재 유효한 `phase_cell_improved_v1_stage1/2`만 유지
  - 최고 성능 가중치를 `models/phase_cell_v1_best.pt`로 승격
  - `README.md`, `DATASETS.md` 신규 작성, `.gitignore` 정비
  - macOS 파일명 유니코드 정규화(NFD/NFC) 불일치 발견 및 수정
  - `onion_yolo_project/.venv`는 절대경로 하드코딩 위험으로 이동 보류

## 2. `Onion-Cell-Merged-v5-2` 학습 실패 원인 분석

**요청:** 메모리에 "학습 실패, 원인 미확인"으로 기록된 항목의 실제 원인 조사

- `Yolo11_Exec_01.ipynb` cell 44~68 실행 로그를 셀 단위로 재구성, `ultralytics.data.utils.check_det_dataset()` 직접 호출로 경로 해석 검증
- 결론:
  - `data.yaml`의 `../train/images` 상대경로는 실제로는 무해(ultralytics가 자체적으로 올바른 경로 탐색)
  - 노트북상 `yaml_onion` 저장 위치 오타(`Mitosis-15/data.yaml`)는 발견했으나 결과에 영향 없음
  - 이 데이터셋 학습 자체는 100 epoch 정상 완료, mAP50 양호 — "학습 실패"가 아님
  - 진짜 원인은 `d`/`nd` 2-class 스키마가 프로젝트의 4-class phase 스키마와 호환되지 않는 것
  - 기존 메모리의 "실패" 기록은 실제로는 별도 실험(`mitosis_yolo11n_detect-2`, `cell_OB_yolo11` 기반)의 저조한 결과를 가리켰을 가능성이 높음

## 3. 분석 보고서 작성

**요청:** 위 조사 내용을 보고서로 작성

- `ANALYSIS_REPORT_2026-07-26.md` 최초본 작성 (프로젝트 구조 점검 + Onion-Cell-Merged 원인 분석 통합)
- 관련 메모리(`project_raimscope.md`)를 조사 결론에 맞춰 갱신

## 4. hwpx 스킬 검사 및 설치

**요청:** hwpx 스킬 검사, 최신 버전 검색 및 설치

- 로컬에서 발견된 후보 3개 중 `SkillUp/과학실개선/hwpx-skill`(완성형)을 사용자가 선택
- 원본 검사 결과: SKILL.md가 문서화한 기능(HWP 바이너리 지원, `examples/`, gonmun/minutes/proposal 템플릿)과 실제 파일 상태 사이에 드리프트 발견. `create_document.py`, `text_extract.py`는 존재하지 않는 외부 `hwpx` 모듈에 의존해 즉시 ImportError (PyPI의 동명 패키지는 무관한 패키지임을 확인 후 제거)
- 실제 동작하는 부분만 `.claude/skills/hwpx/`에 이식: `build_hwpx.py`, `validate.py`, `analyze_template.py`, `scripts/office/{pack,unpack}.py`, `templates/base`·`templates/report`, `references/hwpx-format.md`
- 의존성 `lxml`, `olefile`을 `onion_yolo_project/.venv`에 설치, 빌드→검증→언팩→분석 전 과정 실행 테스트로 동작 확인
- SKILL.md 상단에 이식 시 제약사항(제외된 기능, 검증된 스크립트) 명시

## 5. 독립 검토 반영

**요청:** `REVIEW_OF_ANALYSIS_REPORT_2026-07-26.md`(사용자가 별도로 준비한 검토 문서)의 지적사항 반영

- **[보안, 최우선]** 검토에서 노트북(`Yolo11_Exec_01.ipynb`)에 평문 Roboflow API 키가 포함된 채 이미 GitHub에 push된 사실을 발견
  - 코드: 하드코딩된 키를 `os.getenv("ROBOFLOW_API_KEY")`로 교체
  - 이력: `git-filter-repo --replace-text`로 전체 Git 이력에서 키 문자열 제거 후 `git push --force`로 원격 이력 교체
  - 사용자가 Roboflow 콘솔에서 키를 직접 폐기·재발급하기로 확인
- **[보고서 정정, 필수+권장 전체]** `ANALYSIS_REPORT_2026-07-26.md` 개정:
  - mAP50을 "마지막 epoch 0.895 / best checkpoint 0.899"로 구분
  - 클래스 인스턴스 수를 재집계 결과로 정정 (`d` 2,913 / `nd` 17,605, 합계 20,518, 비율 약 14.2:85.8)
  - "불균형 때문" 등 인과 단정을 "가능성이 있다"는 완화된 표현으로 수정
  - "병합 불가능" → "현재 라벨 그대로 직접 병합 불가능"으로 일반화 완화
  - Cell 56 메모 해석을 확정 사실이 아닌 "유력한 해석"으로 수정
  - `mitosis_yolo11n_detect-2`의 문제를 "과적합" 확정 대신 "낮은 검증 성능과 과다 false positive"로 수정
  - `anaphasae` 오탈자, "분류"→"4-class 객체 탐지" 용어 정밀화, 표준 체세포분열 단계와의 차이 명시
  - 아카이브 용량·실험 수에 측정 시점(정리 전/후) 명시
- **[문서 정합성]** `README.md`, `DATASETS.md`의 "Onion-Cell-Merged-v5-2 학습 실패" 기록을 정정된 결론으로 갱신
- **[메모리]** 위 모든 정정 사항과 보안 사고 이력을 `project_raimscope.md`에 반영

## 6. 커밋 및 Push

- 커밋 1(`95f4e29`): 노트북 API 키 수정
- `git filter-repo` 이력 재작성 → 커밋 해시 변경(`55bb931`) → `git push --force origin main`
- 커밋 2(`2b04698`): 보고서 개정, README/DATASETS.md 정정, hwpx 스킬 설치 → `git push origin main` (일반 push)

## 산출물 목록

- `README.md`, `DATASETS.md` (신규 작성 후 정정)
- `ANALYSIS_REPORT_2026-07-26.md` (검토 반영 개정판)
- `.claude/skills/hwpx/` (HWPX 문서 스킬, 검증된 부분만 설치)
- `_archive/` (중복 zip, 오래된 실험 보관)
- `models/phase_cell_v1_best.pt` (최고 성능 가중치 승격본)
- 메모리: `project_raimscope.md` 갱신 (Onion-Cell-Merged 정정, 보안 사고 이력, 보고서 작성 관련 피드백)
