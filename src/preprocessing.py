import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class HourMedianImputer(BaseEstimator, TransformerMixin):
    """결측치를 fit 데이터의 시간대(hour)별 중앙값으로 채운다.

    Pipeline 안에서 쓰면 교차검증 fold마다 학습 fold로만 중앙값을 계산하므로 누수가 없다.
    fit 데이터에서 값이 전부 비어 있는 시간대(예: 1시의 오존·미세먼지)는 결측으로 남긴다.
    """

    def __init__(self, cols):
        self.cols = cols

    def fit(self, X, y=None):
        self.medians_ = X.groupby('hour')[self.cols].median()
        return self

    def transform(self, X):
        X = X.copy()
        medians = self.medians_.reindex(X['hour']).set_index(X.index)
        X[self.cols] = X[self.cols].fillna(medians)
        return X
