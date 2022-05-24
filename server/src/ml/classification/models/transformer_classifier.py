from copy import deepcopy
from typing import Union, Type, Dict, Callable

from src.util import get_logger
from .base import ClassificationModel
from src.ml.classification import ClassificationMethod, LRClassifier, create_classification_method
from src.ml.data import Dataset
from src.ml.embedding import EmbeddingModel, create_embedding_model


class TransformerClassifier(ClassificationModel):
    def __init__(
            self,
            embedder_class: Union[str, Type[EmbeddingModel]],
            embedder_config: Dict = None,
            classification_method: Union[str, Type[ClassificationMethod]] = LRClassifier,
            classification_method_config: Dict = None,
            set_status: Callable[[str], None] = lambda x: None,
    ):
        super().__init__()
        self.logger = get_logger('TransformerClassifier')

        # Embedder
        self.logger.debug(f"Embedding model class: {embedder_class} / config: {embedder_config}")
        self.embedder, self.embedder_config = create_embedding_model(
            embedder_class,
            embedder_config,
            set_status=set_status
        )

        # Model
        self.logger.debug(f"Model class: {classification_method} / config: {classification_method_config}")
        self.model, self.model_config = create_classification_method(
            classification_method,
            classification_method_config,
            set_status=set_status
        )

    def fit(self, dataset: Dataset) -> Dict[str, float]:
        # Checking dataset
        assert ("text" in sample for sample in dataset), f"Some items in the `dataset` do not contain a `text` field."

        # Embed texts
        self.embedder.fit(dataset=dataset)
        embeddings = self.embedder.predict([sample.text for sample in dataset])
        dataset_copy = deepcopy(dataset)
        assert len(embeddings) == len(dataset_copy)
        for sample, embedding in zip(dataset_copy, embeddings):
            sample.embedding = embedding

        # Train model
        self.model.fit(dataset=dataset_copy, evaluate=True)
        metrics = self.model.evaluate(dataset=dataset_copy)
        return metrics

    def predict(self, dataset: Dataset) -> Dataset:
        # Checking dataset
        assert ("text" in sample for sample in dataset), f"Some items in the `dataset` do not contain a `text` field."

        # Embed texts
        embeddings = self.embedder.predict([sample.text for sample in dataset])
        dataset_copy = deepcopy(dataset)
        assert len(embeddings) == len(dataset_copy)
        for sample, embedding in zip(dataset_copy, embeddings):
            sample.embedding = embedding

        # Predict
        y_hat = self.model.predict(dataset_copy)
        assert len(y_hat) == len(dataset_copy)
        for sample, y_ in zip(dataset_copy, y_hat):
            sample.prediction = y_

        return dataset_copy
