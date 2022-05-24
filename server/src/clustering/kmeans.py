import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from typing import Callable, List, Dict

from src.clustering.topic_extraction import TopicExtractor
from src.ml.classification.methods import Dataset, DataSample
from copy import deepcopy


class ClusterInfo:
    def __init__(
            self,
            cluster_representative: DataSample = None,
            cluster_topics: List[str] = None,
            avg_distance_to_centroid: float = None
    ):
        self.cluster_representative = cluster_representative
        self.cluster_topics = cluster_topics
        self.avg_distance_to_centroid = avg_distance_to_centroid

    def export_json(self):
        output = dict()
        if self.cluster_representative:
            output["representative"] = self.cluster_representative.export_json()
        if self.cluster_topics:
            output["topics"] = self.cluster_topics
        if self.avg_distance_to_centroid:
            output["avg_distance_to_centroid"] = self.avg_distance_to_centroid
        return output


class ClusteringOutput:
    def __init__(
            self,
            clusters_info: List[ClusterInfo],
            dataset: Dataset
    ):
        self.clusters_info: List[ClusterInfo] = clusters_info
        self.dataset: Dataset = dataset

        # sanity check
        assert (item.cluster for item in self.dataset), 'When outputing clusters, did not find `cluster` in dataset items'

    def export_json(self) -> Dict:
        output = {
            "clusters_info": list(),
            "dataset": list()
        }
        for cluster_info in self.clusters_info:
            output["clusters_info"].append(cluster_info.export_json())
        for sample in self.dataset:
            output["dataset"].append(sample.export_json())
        return output


class KMeansClusterer:
    def __init__(self, status_setter: Callable[[str], None] = None, **kwargs):
        self.status_setter = status_setter
        self.km = KMeans(**kwargs)
        self.pca = PCA(n_components=2)

    def maybe_set_status(self, status: str):
        if self.status_setter:
            self.status_setter(status)

    def process(self, dataset: Dataset):
        self.maybe_set_status("Fitting KMeans...")
        new_dataset: Dataset = deepcopy(dataset)
        x = [item.embedding for item in dataset]
        self.km.fit(x)
        cluster_assignment = self.km.labels_

        for label, sample in zip(cluster_assignment, new_dataset):
            sample.cluster = int(label)

        # Select a representative in each cluster
        centers = self.km.cluster_centers_
        representatives = list()
        avg_distances_to_centroids = list()
        for cluster_ix in range(len(centers)):
            cluster_items = [c for c, assignment in zip(new_dataset, self.km.labels_) if assignment == cluster_ix]
            cluster_items_embeddings = [x_ for x_, assignment in zip(x, self.km.labels_) if assignment == cluster_ix]
            from sklearn.metrics.pairwise import pairwise_distances
            distances = pairwise_distances(cluster_items_embeddings, [centers[cluster_ix]],
                                           metric="euclidean").squeeze()
            avg_distances_to_centroids.append(float(distances.mean()))
            sorted_index = np.argsort(distances)
            min_ix = sorted_index[0]
            representatives.append(cluster_items[min_ix])

        # Extract topics
        self.maybe_set_status(status="Extracting topics...")
        topics = TopicExtractor().extract_topics_tfidf(
            texts=[[sample.text for sample in new_dataset if sample.cluster == cluster_ix] for cluster_ix in range(len(centers))],
            n_topics=10,
            n_gram_range=(1, 2),
            skip_stopwords=True
        )

        # Wrap up clusters info
        clusters_info = list()
        for representative, topic_list, distance_to_centroid in zip(representatives, topics, avg_distances_to_centroids):
            clusters_info.append(ClusterInfo(
                cluster_representative=representative,
                cluster_topics=topic_list,
                avg_distance_to_centroid=distance_to_centroid
            ))

        # PCA
        self.maybe_set_status(status="Doing PCA...")
        x_reduced = self.pca.fit_transform(x)
        assert len(x_reduced) == len(new_dataset)
        for embedding_reduced, sample in zip(x_reduced, new_dataset):
            sample.embedding_2d = embedding_reduced.tolist()

            # Output
        clustering_output = ClusteringOutput(
            clusters_info=clusters_info,
            dataset=new_dataset
        )

        return clustering_output


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
                embedding=np.random.uniform(size=(10)).tolist()
            )
            for _ in range(N)
        ]
    )

    dataset[0]
    km = KMeansClusterer(n_clusters=5)
    processed = km.process(dataset)
    json.dumps(processed.export_json())
    json.dumps(processed.dataset.export_json())
    type(processed.clusters_info[0].export_json()["representative"]["cluster"])
    json.dumps(np.random.randn(10).tolist())


if __name__ == "__main__":
    test()
