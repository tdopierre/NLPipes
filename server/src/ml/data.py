from copy import deepcopy
from typing import List


class DataSample:
    # Those are possible fields for a data sample
    labels = None
    embedding = None
    text = None

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            if key == "text":
                val = str(val).strip()
            self.__dict__[key] = val

    def export_json(self):
        return {
            k: deepcopy(v) for k, v in self.__dict__.items()
            if (
                    v is not None
                    and k != 'embedding'
            )
        }

    def has_attribute(self, key: str):
        return key in self.__dict__


class LabeledSample:
    def __init__(
            self,
            sentence: str,
            labels: List[str],
            embedding: List[float] = None
    ):
        self.sentence = sentence
        self.labels = labels
        self.embedding = embedding

    def __repr__(self):
        return f'LabeledSample({self.labels}, `{self.sentence}`)'


class Dataset:
    def __init__(
            self,
            data: List[DataSample]
    ):
        self.data = data

    def __iter__(self):
        yield from self.data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        return self.data[item]

    def export_json(self):
        return [item.export_json() for item in self.data]
