from sklearn.metrics import f1_score
import numpy as np
from sklearn.linear_model import LogisticRegression
from typing import List, Dict, Union, Callable

from sklearn.multioutput import MultiOutputClassifier

from src.ml.data import Dataset, DataSample


class ClassificationMethod:
    def __init__(self, set_status: Callable[[str], None] = None, **kwargs):
        self.set_status = set_status
        pass

    def fit(self, dataset: Dataset, evaluate: bool = True) -> Union[None, Dict]:
        raise NotImplementedError

    def predict(self, dataset: Dataset) -> List:
        raise NotImplementedError

    def evaluate(self, dataset: Dataset) -> Dict:
        raise NotImplementedError


class LRClassifier(ClassificationMethod):
    def __init__(self, multi_label: bool = False, **kwargs):
        super().__init__(set_status=kwargs.get('set_status'))
        self.unique_labels: Union[List[str], None] = None
        self.label_to_ix: Union[Dict[str, int], None] = None
        self.ix_to_label: Union[Dict[int, str], None] = None
        self.model: Union[LogisticRegression, None] = None
        self.is_trained: bool = False
        self.multi_label: bool = multi_label
        self.metrics: Dict[str, Union[str, float, int]] = dict()

    def fit(self, dataset: Dataset, evaluate: bool = True):
        # sanity check
        assert (sample.labels for sample in dataset)
        assert (sample.embedding for sample in dataset)

        # Store labels info
        self.unique_labels = sorted(set([label for sample in dataset for label in sample.labels]))
        self.label_to_ix = {v: k for k, v in enumerate(self.unique_labels)}
        self.ix_to_label = {k: v for k, v in enumerate(self.unique_labels)}

        # initialize y
        if self.multi_label:
            y = np.zeros(shape=(len(dataset), len(self.unique_labels)))
            for sample_ix, sample in enumerate(dataset):
                for label in sample.labels:
                    y[sample_ix, self.label_to_ix[label]] = 1
            self.model = MultiOutputClassifier(estimator=LogisticRegression())
        else:
            assert all(len(sample.labels) == 1 for sample in dataset), f"Set {self.multi_label:} but found sample with !=1 label"
            y = np.array([self.label_to_ix[item.labels[0]] for item in dataset])
            self.model = LogisticRegression()

        x = [item.embedding for item in dataset]

        # initialize model
        self.model.fit(x, y)
        self.is_trained = True

        # Evaluate
        if evaluate:
            metrics = self.evaluate(dataset=dataset)
            return metrics
        return None

    def evaluate(self, dataset: Dataset):
        # sanity check
        assert (sample.labels for sample in dataset)
        assert (sample.embedding for sample in dataset)

        # initialize y
        if self.multi_label:
            y = np.zeros(shape=(len(dataset), len(self.unique_labels)))
            for sample_ix, sample in enumerate(dataset):
                for label in sample.labels:
                    y[sample_ix, self.label_to_ix[label]] = 1
        else:
            assert all(len(sample.labels) == 1 for sample in dataset), f"Set {self.multi_label:} but found sample with !=1 label"
            y = np.array([self.label_to_ix[item.labels[0]] for item in dataset])
        x = [item.embedding for item in dataset]

        # compute metrics
        y_hat = self.model.predict(x)
        accuracy = (y_hat == y).mean()
        f1 = f1_score(y, y_hat, average="micro")

        metrics = {
            "f1": f1,
            "accuracy": accuracy
        }

        return metrics

    def predict(self, dataset: Dataset):
        # sanity check
        assert self.is_trained, 'Model has not been trained yet! Use the `fit()` method.'

        # initialize x
        x = [item.embedding for item in dataset]
        y_hat = self.model.predict(x).tolist()
        output = list()

        if self.multi_label:
            for prediction_vector in y_hat:
                pred_readable = list()
                for class_ix, class_prediction in enumerate(prediction_vector):
                    if class_prediction:
                        pred_readable.append(self.ix_to_label[class_ix])
                output.append(pred_readable)
        else:
            for class_ix in y_hat:
                output.append([self.ix_to_label[class_ix]])

        return output


class MultiLabelLRClassifier(ClassificationMethod):
    def __init__(self):
        super().__init__()
        self.unique_labels: Union[List[str], None] = None
        self.label_to_ix: Union[Dict[str, int], None] = None
        self.ix_to_label: Union[Dict[int, str], None] = None
        self.model: Union[LogisticRegression, None] = None
        self.is_trained: bool = False
        self.metrics: Dict[str, Union[str, float, int]] = dict()

    def fit(self, dataset: Dataset, evaluate: bool = True):
        # sanity check
        assert (sample.label or sample.labels for sample in dataset)
        assert (sample.embedding for sample in dataset)

        # Store labels info
        self.unique_labels = sorted(set(sample.labels for sample in dataset))
        self.label_to_ix = {v: k for k, v in enumerate(self.unique_labels)}
        self.ix_to_label = {k: v for k, v in enumerate(self.unique_labels)}

        # initialize y
        y = np.zeros(shape=(len(dataset), len(self.unique_labels)))
        for sample_ix, sample in enumerate(dataset):
            for label in sample.label:
                y[sample_ix, self.label_to_ix[label]] = 1
        x = [item.embedding for item in dataset]

        # initialize model
        model = LogisticRegression()
        model.fit(x, y)
        self.model = model
        self.is_trained = True

        # Evaluate
        if evaluate:
            metrics = self.evaluate(dataset=dataset)
            return metrics
        return None

    def evaluate(self, dataset: Dataset):
        # sanity check
        assert (sample.labels or sample.label for sample in dataset)
        assert (sample.embedding for sample in dataset)

        # initialize y
        y = np.zeros(shape=(len(dataset), len(self.unique_labels)))
        for sample_ix, sample in enumerate(dataset):
            for label in sample.label:
                y[sample_ix, self.label_to_ix[label]] = 1
        x = [item.embedding for item in dataset]

        # compute metrics
        y_hat = self.model.predict(x)
        accuracy = (y_hat == y).mean()
        f1 = f1_score(y, y_hat, average="micro")

        metrics = {
            "f1": f1,
            "accuracy": accuracy
        }

        return metrics

    def predict(self, dataset: Dataset):
        # sanity check
        assert self.is_trained, 'Model has not been trained yet! Use the `fit()` method.'

        # initialize x
        x = [item.embedding for item in dataset]
        y_hat = self.model.predict(x).tolist()
        y_hat_readable = [
            [self.ix_to_label[y_] for y_ in y]
            for y in y_hat
        ]

        return y_hat_readable


def test():
    import numpy as np
    import string
    import json
    N = 50
    x = np.random.randn(N, 10)
    dataset = Dataset(
        [
            DataSample(
                text=''.join(np.random.choice(list(string.ascii_letters), size=5)),
                embedding=np.random.uniform(size=(10)).tolist(),
                label=np.random.choice(list('abcde'))
            )
            for _ in range(N)
        ]
    )

    classifier = LRClassifier()
    classifier.fit(dataset)
