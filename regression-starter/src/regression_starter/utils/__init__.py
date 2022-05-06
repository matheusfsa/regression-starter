from sklearn.pipeline import Pipeline

__all__ = [
    "join_sk_pipelines"
]
def join_sk_pipelines(*pipelines):
    """Function to join pipelines"""
    return Pipeline(steps=pipelines)