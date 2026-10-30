# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 성격

서울시 공공자전거 "따릉이"의 시간대별 대여량(`count`)을 예측하는 회귀 문제로, ML end-to-end 파이프라인 프로젝트다.

- `notebooks/01`~`05`는 마크다운 질문 + `# TODO` 주석만 있는 뼈대다. 원래는 사용자가 직접 채우는 학습용이었으나(README의 "직접 채워보세요"는 그때 문구), 이제는 Claude가 TODO 셀의 코드와 마크다운 질문에 대한 답을 채운다.
- 패키지/빌드/테스트/린트 설정은 없다. `src/`는 비어 있다.

## 환경 / 실행

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook
```

의존성: pandas, numpy, matplotlib, seaborn, scikit-learn, jupyter, xgboost.

## 노트북 파이프라인 (순서대로 진행)

1. `01_problem_definition_and_collection` — 문제 정의, 데이터 로드, 데이터 사전 작성
2. `02_preprocessing` — holdout 분리, 결측치/이상치 확인, 파생변수 → `data/processed/`에 `train.csv`/`holdout.csv`/`test.csv` 저장
3. `03_eda` — `data/processed/train.csv`만 불러와 분석
4. `04_modeling` — 베이스라인 → 모델 비교(CV) → 튜닝 → `models/final_model.joblib`에 `{'model': Pipeline, 'features': [...]}`로 저장. 튜닝 셀은 약 7분 걸린다(이 환경의 XGBoost가 트리 1개당 약 16ms로 느려서 탐색 범위를 줄여 둠). 실행은 `jupyter nbconvert --execute`에 `--ExecutePreprocessor.timeout`을 넉넉히 준다.
5. `05_evaluation_interpretation` — 저장된 모델로 RMSE/MAE/R2, 잔차 분석, feature importance

노트북 간 데이터 전달은 `data/processed/` 파일과 저장된 모델 파일로 이루어진다.

데이터 누수를 허용하지 않는다(사용자가 철저하게 지켜 달라고 요청함). 02는 기상값이 전부 빈 train 행을 지운 직후 train의 20%를 `holdout.csv`로 떼어 낸다(시간대 층화, `random_state=42`). holdout은 02의 이상치 확인, 03 EDA, 04 모델 선택·튜닝에 쓰지 않고 05 최종 평가에서 한 번만 쓴다. EDA에서도 holdout·test는 열지 않는다. 02에서는 통계를 쓰지 않는 처리(기상값이 전부 빈 train 행 삭제, `is_peak` 생성)만 하고, `data/processed/`에는 결측치가 남아 있다. 결측 대체·인코딩처럼 데이터에서 통계를 배우는 처리는 04의 sklearn Pipeline 안에 넣어 교차검증 fold마다 학습 fold로만 fit한다. 결측 대체용 `HourMedianImputer`는 `src/preprocessing.py`에 있다(노트북에서 `sys.path.append('..')` 후 import). 05에서 저장된 Pipeline을 불러올 때도 이 모듈이 import 가능해야 한다.

1시의 오존·미세먼지·초미세먼지는 train/test 모두 항상 비어 있고, 임의 값으로 채우지 않고 결측으로 둔다. 그래서 결측을 처리하지 못하는 모델(선형 회귀 등)에는 별도 처리가 필요하다.

`notebooks/베이스라인_코드.ipynb`는 Dacon 제공 베이스라인(결측치 0 채움 + RandomForest)이다. 경로가 이 저장소 구조와 맞지 않는다(`data/train.csv`, Colab 경로 `/content/data/submission.csv`).

## 데이터 (`data/raw/따릉이/`, Dacon 대회 235576)

- `train.csv` (1459행): `id, hour, hour_bef_temperature, hour_bef_precipitation, hour_bef_windspeed, hour_bef_humidity, hour_bef_visibility, hour_bef_ozone, hour_bef_pm10, hour_bef_pm2.5, count`
- `test.csv` (715행): `count`를 제외한 동일 컬럼
- `submission.csv`: `id, count` (count 비어 있음) — 제출 양식

주의: 날짜·요일 컬럼이 없고 시간 정보는 `hour`뿐이다. 노트북 질문에 나오는 요일/주말/계절 파생변수는 이 데이터로는 만들 수 없다. `id`는 식별자이므로 피처에서 제외해야 한다. 기상 피처는 모두 "1시간 전" 값이며 결측치가 있다.

노트북에서 상대경로를 쓸 때 Jupyter 작업 디렉터리는 `notebooks/`이므로 데이터는 `../data/raw/따릉이/train.csv` 형태로 접근한다.
