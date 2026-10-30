# 따릉이 대여량 예측 프로젝트

머신러닝 end-to-end 파이프라인(문제 정의 → 데이터 수집 → 전처리 → EDA → 모델링 → 평가/해석)을
직접 체화하기 위한 개인 연습 프로젝트.

## 프로젝트 목표

서울시 공공자전거 "따릉이"의 시간대별 대여량을 예측하는 회귀 모델을 만든다.

## 데이터 소스 (택 1)

1. **Dacon "따릉이 대여량 예측" 데이터** (추천 — 바로 시작하기 쉬움)
   - https://dacon.io/competitions/official/235576/data
   - 무료 회원가입 후 train.csv / test.csv / submission.csv 다운로드
   - `data/raw/따릉이/` 폴더에 저장 (대회 데이터라 이 저장소에는 포함하지 않음)

2. **서울 열린데이터광장 공공자전거 대여이력 API** (더 실전에 가까움, API 키 발급 필요)
   - https://data.seoul.go.kr
   - "공공자전거 대여이력 정보" 검색 후 API 키 신청
   - 날씨 데이터는 기상청 API 별도 결합 필요 (난이도 상승)

처음이라면 1번(Dacon)으로 시작하는 걸 추천. 데이터 수집 자체도 연습하고 싶다면 2번 도전.

## 진행 순서 (notebooks/ 폴더)

1. `01_problem_definition_and_collection.ipynb` — 문제 정의 + 데이터 수집
2. `02_preprocessing.ipynb` — 결측치/이상치 처리, 타입 변환, 파생변수
3. `03_eda.ipynb` — 시각화, 상관관계, 패턴 발견
4. `04_modeling.ipynb` — 베이스라인 → 여러 모델 비교 → 튜닝
5. `05_evaluation_interpretation.ipynb` — 성능 평가, 오차 분석, 해석

각 노트북은 뼈대(마크다운 질문 + TODO)만 있고 코드는 비어있습니다. 직접 채워보세요.

## 환경 설정

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook
```
