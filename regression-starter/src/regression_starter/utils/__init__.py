from sklearn.pipeline import Pipeline

__all__ = [
    "join_sk_pipelines"
]
def join_sk_pipelines(*pipelines):
    """Function to join pipelines"""
    steps = [(f"step_{i}", pipe) for i, pipe in enumerate(pipelines)]
    return Pipeline(steps=steps)