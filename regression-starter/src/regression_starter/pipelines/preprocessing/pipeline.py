"""
This is a boilerplate pipeline 'preprocessing'
generated using Kedro 0.18.0
"""

from kedro.pipeline import Pipeline, node, pipeline

from regression_starter.utils import join_sk_pipelines

from .nodes import drop_missing, fill_na


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
                    "drop_transform": "drop_transform",
                },
                name="drop_missing",
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
                    "output_data": "preprocessed_data",
                    "imputer": "imputer_transform",
                },
                name="filled_data",
            ),
            node(
                func=join_sk_pipelines,
                inputs=["drop_transform", "imputer_transform"],
                outputs="preprocess_pipeline",
                name="join_preprocess_pipe",
            ),
        ]
    )
