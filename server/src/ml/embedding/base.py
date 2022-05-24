from typing import List, Callable

from src.ml.data import Dataset


class EmbeddingModel:
    def __init__(self, set_status: Callable[[str], None] = None, **kwargs):
        self.set_status = set_status
        pass

    def fit(self, dataset: Dataset) -> None:
        raise NotImplementedError

    def predict(self, corpus: List[str]) -> List[List[float]]:
        raise NotImplementedError
