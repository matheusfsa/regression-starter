from typing import Any, List
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

__all__ = [
    "DropColumns",
    "DropMissingColumns"
]
class DropColumns(TransformerMixin, BaseEstimator):
    """ This transformer drop columns from data.
    """
    def __init__(self, columns: List[str]):
        self.columns = columns

    def fit(self, X: pd.DataFrame, y: Any = None):
        return self

    def transform(self, X: pd.DataFrame):
        return X.drop(columns=self.columns)


class DropMissingColumns(TransformerMixin, BaseEstimator):
    """This transformer drop columns with high missing rate.
    """
    def __init__(self, missing_rate: float):
        self.missing_rate = missing_rate
        self._columns = []

    def fit(self, X: pd.DataFrame, y: Any = None):
        missing = X.isna().sum()/X.shape[0]
        self._columns = missing[missing >= self.missing_rate].index
        return self

    def transform(self, X: pd.DataFrame):
        return X.drop(columns=self._columns)

