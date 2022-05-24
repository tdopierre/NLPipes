from typing import List, Callable
from sentence_transformers import SentenceTransformer
import numpy as np
from src.util import get_logger, get_device
from .base import EmbeddingModel
from ..data import Dataset

logger = get_logger(__name__)


class TransformerEmbedder(EmbeddingModel):
    def __init__(self, model_name_or_path: str, batch_size: int = 32, **kwargs):
        super().__init__(set_status=kwargs.get('set_status'))
        self.device = get_device()
        self.transformer = SentenceTransformer(model_name_or_path=model_name_or_path).to(device=self.device)
        self.batch_size = batch_size

    def fit(self, dataset: Dataset) -> None:
        # Nothing to fit here!
        pass

    def predict(self, corpus: List[str]):
        assert type(corpus) == list and all([type(item) == str for item in corpus])
        x = list()
        for ix in range(0, len(corpus), self.batch_size):
            batch = corpus[ix:ix + self.batch_size]
            x += self.transformer.encode(batch).astype(np.float64).round(4).tolist()
            if self.set_status:
                self.set_status(f"Embedding corpus ({int(100 * len(x) / len(corpus))}%)")

        return x
