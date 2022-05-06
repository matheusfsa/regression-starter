"""
This is a boilerplate pipeline 'feature_engineering'
generated using Kedro 0.18.0
"""
import pandas as pd
import numpy as np
from regression_starter.transformers.preprocessing import DropColumns

def drop_weak_features(df:pd.DataFrame, target_column: str, corr_th: float):
    """This node drop features with low correlation.

    Args:
        df (pd.DataFrame): Input data.
        target_column (str): Target column.
        corr_th (float): Correlation threshold.

    Returns:
        _type_: _description_
    """
    corr = df.corr()[target_column]
    corr  = np.abs(corr)
    weak_features = corr[corr < target_column].index
    drop_features_transform = DropColumns(weak_features)
    df = drop_features_transform.fit_transform(df)
    return {"output_data": df, "transformer": drop_features_transform}