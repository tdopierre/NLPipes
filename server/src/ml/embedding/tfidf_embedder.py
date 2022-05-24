from typing import List, Callable
from sklearn.feature_extraction.text import TfidfVectorizer
from .base import EmbeddingModel
from src.ml.data import Dataset


class TfIdfEmbedder(EmbeddingModel):
    def __init__(self, **kwargs):
        super().__init__(set_status=kwargs.pop('set_status'))
        self.tfidf = TfidfVectorizer(**kwargs)

    def fit(self, dataset: Dataset) -> None:
        self.tfidf.fit([sample.text for sample in dataset])

    def predict(self, corpus: List[str]):
        assert type(corpus) == list, '`corpus` is not a list!'
        for text in corpus:
            assert type(text) == str, f"Found item of type `{type(text)}` in corpus: `{text}`"
        x = self.tfidf.transform(corpus)
        return x.toarray()
