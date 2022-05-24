from typing import Dict, Type, Union
from .random_embedder import RandomEmbedder
from .tfidf_embedder import TfIdfEmbedder
from .transformer_embedder import TransformerEmbedder
from .base import EmbeddingModel

embedding_models: Dict[str, Type[EmbeddingModel]] = {
    "random": RandomEmbedder,
    "tfidf": TfIdfEmbedder,
    "transformer": TransformerEmbedder
}


def get_embedding_model_by_name(model_name: str):
    return embedding_models[model_name]


def create_embedding_model(
        model_name_or_class: Union[str, EmbeddingModel],
        model_config: Union[Dict, None] = None,
        **kwargs
):
    if model_config is None:
        model_config = dict()
    if type(model_name_or_class) == str:
        model_name_or_class = get_embedding_model_by_name(model_name=model_name_or_class)
    model = model_name_or_class(**model_config, **kwargs)
    return model, model_config
