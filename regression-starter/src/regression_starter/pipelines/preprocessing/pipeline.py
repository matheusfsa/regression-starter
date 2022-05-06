"""
This is a boilerplate pipeline 'preprocessing'
generated using Kedro 0.18.0
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import fill_na


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
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
