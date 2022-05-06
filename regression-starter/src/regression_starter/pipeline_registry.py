"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline, pipeline

from regression_starter.pipelines import feature_engineering as fe
from regression_starter.pipelines import preprocessing as pp


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    pp_pipeline = pp.create_pipeline()
    fe_pipeline = fe.create_pipeline()
    return {
        "pp": pp_pipeline,
        "fe": fe_pipeline,
        "__default__": pp_pipeline + fe_pipeline,
    }
