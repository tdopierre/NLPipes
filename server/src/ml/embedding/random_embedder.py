from typing import List

import numpy as np
from .base import EmbeddingModel
from src.ml.data import Dataset


class RandomEmbedder(EmbeddingModel):
    def __init__(self):
        super().__init__()
        pass

    def fit(self, dataset: Dataset) -> None:
        pass

    def predict(self, corpus: List[str]):
        return np.random.randn(len(corpus), 100).tolist()
