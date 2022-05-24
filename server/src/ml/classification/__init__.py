from typing import Type, Dict, Union, Tuple

from .methods import LRClassifier, ClassificationMethod

classification_methods: Dict[str, Type[ClassificationMethod]] = {
    "LRClassifier": LRClassifier
}


def get_classification_method_by_name(name: str):
    return classification_methods[name]


def create_classification_method(
        name_or_class: Union[str, ClassificationMethod],
        config: Union[Dict, None] = None,
        **kwargs
) -> Tuple[ClassificationMethod, Dict]:
    if config is None:
        config = dict()
    if type(name_or_class) == str:
        name_or_class = get_classification_method_by_name(name=name_or_class)
    model = name_or_class(**config, **kwargs)
    return model, config
