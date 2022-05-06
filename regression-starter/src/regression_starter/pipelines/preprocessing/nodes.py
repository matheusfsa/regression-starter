"""
This is a boilerplate pipeline 'preprocessing'
generated using Kedro 0.18.0
"""
from typing import Any, Dict, List, Union

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from regression_starter.transformers import DropMissingColumns

def drop_missing(
    df: pd.DataFrame,
    missing_rate: float) -> pd.DataFrame:
    drop_transform = DropMissingColumns(missing_rate=missing_rate)
    df = drop_transform.fit_transform(df)
    return {"output_data": df, "drop_transform": drop_transform}


def fill_na(
    df: pd.DataFrame,
    imputers: List[Dict[str, Any]],
    default_fill_strategy: Dict[str, Any],
    fill_skew_th: float,
) -> Dict[str, Union[pd.DataFrame, SimpleImputer]]:
    """This node fill NA values.

    Args:
        df (pd.DataFrame): Input DataFrame
        imputers (List[Dict[str, Any]]): Data with fill strategies by group of columns
        default_fill_strategy (Dict[str, Any]): Default fill strategies.
        fill_skew_th (float): Skeweness threshold to choice between median and mean fill.
    Returns:
        Dict[str, Union[pd.DataFrame, SimpleImputer]]: _description_
    """
    fill_steps = []
    fill_columns = []
    for i, imp in enumerate(imputers):
        fill_steps.append((f"fill_{i}", SimpleImputer(**imp["kwargs"]), imp["columns"]))
        fill_columns += imp["columns"]
    remaining_columns = list(set(df.columns) - set(fill_columns))

    numerics = ["int16", "int32", "int64", "float16", "float32", "float64"]
    numeric_columns = df[remaining_columns].select_dtypes(include=numerics).columns
    fill_steps += _fill_numeric_steps(
        df, numeric_columns, default_fill_strategy["numeric"], fill_skew_th
    )

    categorical_columns = df[remaining_columns].select_dtypes("O").columns

    fill_steps.append(
        (
            f"fill_categorical",
            SimpleImputer(
                strategy="constant", fill_value=default_fill_strategy["categorical"]
            ),
            categorical_columns,
        )
    )

    imputer_transformer = ColumnTransformer(transformers=fill_steps)
    df = imputer_transformer.fit_transform(df)
    return {"output_data": df, "imputer": imputer_transformer}


def _fill_numeric_steps(
    df: pd.DataFrame,
    numeric_columns: List[str],
    strategy: Union[int, float, str],
    fill_skew_th: float,
):
    fill_steps = []
    if isinstance(strategy, str):
        if strategy == "median_or_mean":
            # Get skeweness of each columns
            skew = df[numeric_columns].skew()

            # fill with mean in columns with low skeweness
            mean_columns = skew[skew <= fill_skew_th].index
            print(mean_columns)
            fill_steps.append(
                ("fill_numeric_mean", SimpleImputer(strategy="mean"), mean_columns)
            )

            # fill with median in columns with high skeweness
            median_columns = skew[skew > fill_skew_th].index
            fill_steps.append(
                (
                    "fill_numeric_median",
                    SimpleImputer(strategy="median"),
                    median_columns,
                )
            )

        elif strategy in ["mean", "median", "most_frequent"]:
            fill_steps.append(
                (
                    f"fill_numeric_{strategy}",
                    SimpleImputer(strategy=strategy),
                    numeric_columns,
                )
            )
        else:
            raise ValueError(
                f"Can only use these strategies: ['mean', 'median', 'most_frequent']  got strategy {strategy}"
            )
    else:
        fill_steps.append(
            (f"fill_numeric", SimpleImputer(fill_value=strategy), numeric_columns)
        )
    return fill_steps
