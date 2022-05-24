import json
import threading
import time
from copy import deepcopy
from threading import Event
from typing import Dict, List, Union, Type

from dataclasses import dataclass
from src.clustering.kmeans import KMeansClusterer, ClusteringOutput
from src.ml.embedding import TfIdfEmbedder
from src.ml.embedding import RandomEmbedder
from src.ml.embedding.transformer_embedder import TransformerEmbedder
from src.ml.embedding import embedding_models
from src.clustering import models
from src.sentiment_analysis.model import SentimentAnalysisModel
from src.util import get_logger
from src.socket import client as socket_client
import datetime
from src.ml.classification.methods import DataSample, Dataset, LRClassifier, ClassificationMethod
from src.ml.classification.models import classification_models, ClassificationModel, create_classification_model
from src.ml.embedding import create_embedding_model

logger = get_logger(__name__)


@dataclass
class PipeConfig:
    pipe_type: str
    name: str
    id: str
    config: Dict
    dependencies: List[str]

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_json(cls, j):
        pass


class Pipe(threading.Thread):
    results_type: str = None

    def __init__(self, name: str, id: str, x: Union[Dict, List[Dict]], events: List[Event] = None, **kwargs):
        super().__init__()
        self.logger = get_logger(name)
        self.name = name
        self.id = id
        self.status: Union[str, None] = None
        self.x = x  # input
        self.y = dict()  # pipe output
        self.output = dict()  # log output
        self.start_time: Union[datetime.datetime, None] = None
        self.end_time: Union[datetime.datetime, None] = None
        if not events:
            events = list()
        self.in_events = events
        self.out_event = Event()
        # self.logger.debug(f'pipe {self.name} received x {x}')

    def set_status(self, status: str):
        socket_client.emit("progress-update", {
            "id": self.id,
            "status": status
        })

        self.logger.debug(f'{self.name} New status: {status}')
        self.status = status

    def run(self):
        self.set_status("Waiting for prior tasks...")
        for event in self.in_events:
            event.wait()

        self.set_status("Starting...")
        self.start_time = datetime.datetime.now()

        # Setting input x
        if type(self.x) == list:
            x = dict()
            for x_ in self.x:
                for key, val in x_.items():
                    x[key] = val
            self.x = x
        try:
            self._run()
        except Exception as e:
            import traceback
            error_msg = traceback.format_exc()
            self.set_status(f"Error ({str(e)}): {error_msg}")
            return
        self.end_time = datetime.datetime.now()
        self.set_status("Complete")
        self.out_event.set()

    def _run(self):
        raise NotImplementedError

    def results_json(self):
        raise NotImplementedError


class FileReaderPipe(Pipe):
    results_type = "file_read"

    def __init__(
            self,
            file_type: str,
            split_on_punctuation: bool = False,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.file_type = file_type
        self.split_on_punctuation = split_on_punctuation
        if self.file_type in ("csv", "tsv"):
            if "csv_separator" in kwargs:

                self.separator = kwargs["csv_separator"]
            else:
                self.separator = ','
                self.logger.debug(f"Setting CSV separator to `{self.separator}`")

    def _run(self):
        self.set_status("Reading file...")
        encodings = ("utf-8", "latin1")

        for encoding in encodings:
            logger.debug(f"trying to read file using encoding `{encoding}`")
            try:
                file_decoded = self.x["file_raw"].decode(encoding=encoding)
                break
            except Exception:
                logger.debug(f"Could not read file w/ {encoding} encoding")
        else:
            logger.error("Could not read file")
            raise UnicodeDecodeError(f"Could not read file using encodings {encodings}")

        logger.debug(f'Reading file type `{self.file_type}`')
        if self.file_type.strip() == "txt":
            import re
            corpus = re.split(r'[\r\n]', file_decoded)

            if self.split_on_punctuation:
                corpus = [
                    piece.strip()
                    for c in corpus
                    for piece in re.split(r'[!?.\n\r]+', c)
                    if len(piece.strip())
                ]

            data = [
                DataSample(text=text)
                for text in corpus
            ]

        elif self.file_type == "csv":
            from io import StringIO
            import re
            import pandas as pd
            df = pd.read_csv(StringIO(file_decoded), sep=self.separator)
            assert 'text' in df.columns, f'Did not find any column named `text`. Columns found: {df.columns}'
            data = list()

            for k, row in df.iterrows():
                row_dict = row.to_dict()
                text = str(row_dict.pop('text')).strip()

                if not len(text):
                    continue

                if self.split_on_punctuation:
                    pieces = [
                        piece.strip()
                        for piece in re.split(r'[!?.\n\r]+', text)
                        if len(piece.strip())
                    ]
                else:
                    pieces = [text]
                for piece in pieces:
                    data.append(DataSample(text=piece, **row_dict))
        elif self.file_type == "jsonl":
            data = list()
            import re
            for ix_line, line in enumerate(re.split(r'[\r\n]', file_decoded)):
                if not len(line.strip()):
                    continue
                try:
                    line_dict = json.loads(line.strip())
                except:
                    self.logger.error(f"Could not decode line {line}")
                    raise Exception
                assert 'text' in line_dict, f'line #{ix_line}: {line_dict} does not have a `text` key.'
                data.append(DataSample(**line_dict))

        else:
            raise NotImplementedError(f"File type `{self.file_type}` is not supported yet.")

        dataset = Dataset(data)
        logger.debug("setting dataset to output dictionary")
        self.y["dataset"]: Dataset = dataset

    def results_json(self):
        return {
            "dataset": self.y["dataset"].export_json()
        }


class EmbeddingPipe(Pipe):
    results_type = "embeddings"

    def __init__(
            self,
            embedder_class: Union[str, Type[Union[TransformerEmbedder, RandomEmbedder, TfIdfEmbedder]]],
            embedder_config: Dict = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if type(embedder_class) == str:
            embedder_class = embedding_models[embedder_class]
        if not embedder_config:
            embedder_config = dict()
        self.embedder_class = embedder_class
        self.logger.debug(f"Embedder class: {embedder_class}")
        self.embedder_config = embedder_config
        self.embedder = None

    def _run(self):
        self.set_status("Loading embedder...")
        self.embedder = self.embedder_class(**self.embedder_config, set_status=self.set_status)

        self.set_status(f"Embeddings corpus...")
        dataset: Dataset = self.x["dataset"]
        embeddings = self.embedder.predict([item.text for item in dataset])
        assert len(embeddings) == len(dataset)

        self.set_status("Wrapping corpus & embeddings...")
        for sample, embedding in zip(dataset, embeddings):
            if type(embedding) != list:
                embedding = list(embedding)
            sample.embedding = embedding
        self.y["dataset"] = dataset
        del self.embedder

    def results_json(self):
        return self.y["dataset"].export_json()


class ClusteringPipe(Pipe):
    results_type = "clusters"

    def __init__(
            self,
            model_class: Union[Type[Union[KMeansClusterer]], str],
            model_config: Dict = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if type(model_class) == str:
            model_class = models[model_class]
        if not model_config:
            model_config = dict()
        self.model_class = model_class
        self.model_config = model_config
        self.model = None

    def _run(self):
        self.set_status("Loading model...")
        self.model = self.model_class(**self.model_config)

        self.set_status("Running clustering...")
        dataset = self.x["dataset"]

        # logger.debug(f"found embedidngs {embeddings}")
        output: ClusteringOutput = self.model.process(dataset)
        self.y["clustering_output"] = output

    def results_json(self):
        return self.y["clustering_output"].export_json()


class SentimentAnalysisPipe(Pipe):
    results_type = "sentiment_analysis"

    def __init__(
            self,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.model: SentimentAnalysisModel = None

    def _run(self):
        self.set_status("Loading model...")
        self.model = SentimentAnalysisModel(status_setter=self.set_status)

        assert 'dataset' in self.x, f"`dataset` object not found in input of pipe {self.name} - {self.id}"
        dataset: Dataset = self.x["dataset"]
        dataset_with_sentiment = self.model.predict_sentiment(dataset=dataset)
        assert len(dataset) == len(dataset_with_sentiment), f'Mismatch between length of `dataset` and length of prediction of sentiment analysis.'

        self.output["dataset"] = dataset_with_sentiment
        self.y["dataset"] = dataset_with_sentiment

    def results_json(self):
        return self.y["dataset"].export_json()


class TrainClassifierPipe(Pipe):
    results_type = "trained_model"

    def __init__(
            self,
            classification_model: Union[str, Type[ClassificationModel]],
            classification_model_config: Dict,
            **kwargs
    ):
        super().__init__(**kwargs)

        # Model
        self.logger.debug(f"Classification model class: {classification_model} / config: {classification_model_config}")
        self.model, self.model_config = create_classification_model(classification_model, classification_model_config)

    def _run(self):
        self.set_status("Getting dataset...")

        # Checking dataset
        assert "dataset" in self.x, f"`dataset` not found in input of pipe ({self.name} - {self.id}) {self.x.keys()}"
        dataset: Dataset = self.x["dataset"]
        assert ("text" in sample for sample in dataset), f"Some items in the `dataset` do not contain a `text` field."

        # Train model
        metrics = self.model.fit(dataset=dataset)

        # Save output
        self.y["model"] = self.model
        self.y["metrics"] = metrics
        del self.model

    def results_json(self):
        return {
            "metrics": self.y["metrics"]
        }


class PredictClassifierPipe(Pipe):
    results_type = "classifier_prediction"

    def __init__(
            self,
            **kwargs
    ):
        super().__init__(**kwargs)

    def _run(self):
        # input checks
        for key in ("dataset", "model"):
            assert key in self.x, f"`{key}` not found in input of pipe ({self.name} - {self.id}) {self.x.keys()}"

        self.set_status("Checking inputs...")
        dataset: Dataset = self.x["dataset"]
        model: ClassificationModel = self.x["model"]

        self.set_status("Running prediction...")
        predicted_dataset = model.predict(dataset=dataset)

        self.y["dataset"] = predicted_dataset
        del self.x["model"], model

    def results_json(self):
        return self.y["dataset"].export_json()


class MainProcess(Pipe):
    def __init__(
            self,
            config: Dict[str, Union[str, float, int, Dict]],
            pipe_configs: List[PipeConfig],
            files: Dict,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.config = config
        self.pipe_configs: List[PipeConfig] = pipe_configs
        self.pipes: List[Pipe] = list()
        self.files = files
        self.files_raw = {
            file_id: file.read()
            for file_id, file in self.files.items()
        }
        # logger.debug(f'starting main process with files {self.files_raw}')
        self.processes: Dict[str, Pipe] = dict()

    def _run(self):
        while len(self.processes) != len(self.pipe_configs):
            self.logger.debug("looping....")
            for pipe_config in self.pipe_configs:
                pipe_id = pipe_config.id
                if pipe_id in self.processes:
                    continue
                dependencies = pipe_config.dependencies
                if not len(dependencies) or all([dep in self.processes for dep in dependencies]):
                    new_pipe_class = pipes[pipe_config.pipe_type]
                    if pipe_config.pipe_type == "file_reader":
                        # logger.debug('files_raw', self.files_raw)
                        x = {
                            "file_raw": self.files_raw[pipe_id]
                        }
                    else:
                        x = [self.processes[dep].y for dep in dependencies]
                    events = [self.processes[dep].out_event for dep in dependencies]

                    logger.debug(f"Instancing {new_pipe_class} with config {pipe_config.config} events {events}")
                    new_pipe = new_pipe_class(
                        x=x,
                        name=pipe_config.name,
                        id=pipe_id,
                        events=events,
                        **pipe_config.config
                    )
                    new_pipe.start()
                    self.processes[pipe_id] = new_pipe
                else:
                    logger.debug(f'cannot start {pipe_config} - Current pipes {self.processes.keys()}')
            time.sleep(0.1)
        socket_client.emit("new-process", self.export_config())

        # Wait for all processes to end!
        logger.debug('*' * 50 + 'LOOKS GOOD TO ME')
        for process_id, process in self.processes.items():
            self.set_status(f'Waiting for {process.name}...')
            process.out_event.wait()

    @property
    def time(self):
        output = {}
        if self.start_time:
            output["start"] = self.start_time.isoformat()
        if self.end_time:
            output["end"] = self.end_time.isoformat()
            output["elapsed"] = (self.end_time - self.start_time).seconds
        return output

    def export_config(self):
        return dict(
            **{k: v for k, v in self.config.items() if type(v) in (str, int, float, dict) and k is not 'x'},
            status=self.get_status,
            pipe_configs=[
                dict(
                    **pipe_config.to_dict(),
                    **(
                        dict(status=self.processes[
                            pipe_config.id].status) if pipe_config.id in self.processes else dict()))
                for pipe_config in self.pipe_configs],
            time=self.time
        )

    def results_json(self):
        self.logger.debug(f"Calling results for process {self.id}")
        return [
            {
                "result_type": process.results_type,
                "result_data": process.results_json(),
                "pipe": {
                    "name": process.name,
                    "id": process.id
                }
            }
            for process_id, process in self.processes.items()
        ]

    @property
    def get_status(self):
        if len(self.processes):
            if all([process.out_event.isSet() for process_id, process in self.processes.items()]):
                return 'Complete'
            return 'Progressing...'
        return "Not started"


pipes: Dict[str, Type[Pipe]] = {
    "embedding": EmbeddingPipe,
    "clustering": ClusteringPipe,
    "file_reader": FileReaderPipe,
    "sentiment_analysis": SentimentAnalysisPipe,
    "train_classifier": TrainClassifierPipe,
    "predict_classifier": PredictClassifierPipe
}


def test():
    config_embedding = PipeConfig(
        pipe_type="embedding",
        config={
            "embedder_class": "transformer",
            "embedder_config": dict(model_name_or_path='sentence-transformers/distilbert-base-nli-stsb-mean-tokens')
        },
        name="embedding_transformer",
        id="embed1",
        dependencies=[]
    )

    config_clustering = PipeConfig(
        pipe_type="clustering",
        config={
            "model_class": "kmeans",
            "model_config": dict()
        },
        name="clustering_kmeans",
        id="cluster",
        dependencies=["embed1"]
    )

    p = MainProcess(config=dict(), pipe_configs=[config_embedding, config_clustering], name="main", x={
        "corpus": ["salut", "ca va", "oui", "et", "toi", "ca", "va", "bien", "ou", "quoi"]})
    p.start()
    p.join()
    print(p.results())


if __name__ == "__main__":
    test()
