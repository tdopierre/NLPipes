from typing import List


class TopicExtractor:
    def __init__(self):
        pass

    @staticmethod
    def extract_topics_tfidf(
            texts: List[List[str]],
            n_topics: int = 10,
            n_gram_range: tuple = (1, 2),
            skip_stopwords: bool = True
    ) -> List[List[str]]:
        """

        Parameters
        ----------
        texts: Clustered documents, shaped as List[List[str]]. Each item is a list of documents.
        n_topics: number of topics per cluster.
        n_gram_range: tuple indicating which n_gram range to take into the decomposition.
        skip_stopwords: boolean check to ignore stop-words.

        Returns
        -------
        A List[List[str]], of the same length as `texts`. Each item is a list of tokens representing the cluster.

        """
        from sklearn.feature_extraction.text import TfidfVectorizer
        from nltk.corpus import stopwords
        import string

        ascii_stopwords = [
            stopword
            for stopword in stopwords.words()
            if all(c in string.ascii_letters for c in stopword)
        ]

        vectorizer = TfidfVectorizer(
            ngram_range=n_gram_range,
            stop_words=ascii_stopwords if skip_stopwords else None,
        )
        grouped_documents = [' '.join(docs) for docs in texts]
        X = vectorizer.fit_transform(grouped_documents)
        inverse_vocab = {v: k for k, v in vectorizer.vocabulary_.items()}
        output = list()

        for cluster_ix in range(len(texts)):
            cluster_topics = list()
            cluster_vec = X[cluster_ix].toarray().squeeze()
            best_vocabulary_indices = cluster_vec.argsort()[::-1]
            for topic_ix in range(n_topics):
                cluster_topics.append(inverse_vocab[best_vocabulary_indices[topic_ix]])
            output.append(cluster_topics)
        return output


def test():
    import json
    with open('/home/tdopierre/Projects/nlp-analyser/server/data/OOS.train.jsonl.txt', 'r') as file:
        lines = [json.loads(line) for line in file]
    from collections import defaultdict
    clusters = defaultdict(list)
    for line in lines:
        clusters[line["label"]].append(line["sentence"])
    clusters = [v for k, v in clusters.items()]

    skip_stopwords = True
    n_gram_range = (1, 2)
    TopicExtractor().extract_topics_tfidf(clusters)
    texts = clusters
