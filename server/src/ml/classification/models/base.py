from typing import Dict, List, Callable

from src.ml.data import Dataset


class ClassificationModel:
    def __init__(self, set_status: Callable[[str], None] = None, **kwargs):
        self.set_status = set_status

    def fit(self, dataset: Dataset) -> Dict:
        raise NotImplementedError

    def predict(self, dataset: Dataset) -> Dataset:
        raise NotImplementedError
