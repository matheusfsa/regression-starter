"""
This is a boilerplate pipeline 'preprocessing'
generated using Kedro 0.18.0
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import fill_na, drop_missing


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=drop_missing,
                inputs={
                    "df": "master_table",
                    "missing_rate": "params:missing_rate",
                },
                outputs={
                    "output_data": "data_wo_missing_columns",
                    "imputer": "drop_transform",
                },
                name="filled_data",
            ),
            node(
                func=fill_na,
                inputs={
                    "df": "master_table",
                    "imputers": "params:imputers",
                    "default_fill_strategy": "params:default_fill_strategy",
                    "fill_skew_th": "params:fill_skew_th",
                },
                outputs={
                    "output_data": "filled_data",
                    "imputer": "imputer_transform",
                },
                name="filled_data",
            )
        ]
    )
