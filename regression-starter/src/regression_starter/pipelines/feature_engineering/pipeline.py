"""
This is a boilerplate pipeline 'feature_engineering'
generated using Kedro 0.18.0
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import drop_weak_features

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=drop_weak_features,
                inputs={
                    "df": "preprocessed_data",
                    "target_column": "params:target_column",
                    "corr_th": "params:corr_threshold",
                },
                outputs={
                    "output_data": "feature_data",
                    "transformer": "drop_features_transform",
                },
                name="drop_weak_features",
            )
        ]
    )
