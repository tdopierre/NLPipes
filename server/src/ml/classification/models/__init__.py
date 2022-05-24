from typing import Dict, Type, Union, Tuple

from .base import ClassificationModel
from .transformer_classifier import TransformerClassifier

classification_models: Dict[str, Type[ClassificationModel]] = {
    "TransformerClassifier": TransformerClassifier
}


def get_classification_model_by_name(name: str):
    return classification_models[name]


def create_classification_model(
        name_or_class: Union[str, ClassificationModel], config: Union[Dict, None] = None
) -> Tuple[ClassificationModel, Dict]:
    if config is None:
        config = dict()
    if type(name_or_class) == str:
        name_or_class = get_classification_model_by_name(name=name_or_class)
    model = name_or_class(**config)
    return model, config
