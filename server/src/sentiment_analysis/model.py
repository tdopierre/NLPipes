import os
from copy import deepcopy
from typing import Callable

import numpy as np
import torch
import argparse

import tqdm
from torch.nn import Softmax
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from src.ml.classification.methods import Dataset
from src.util import get_device


class SentimentAnalysisModel:
    def __init__(self, status_setter: Callable[[str], None] = None):
        self.device = get_device()
        self.tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
        self.model = AutoModelForSequenceClassification.from_pretrained(
            "nlptown/bert-base-multilingual-uncased-sentiment").to(self.device)
        self.batch_size = 32
        self.status_setter = status_setter

    def set_status(self, status: str):
        if self.status_setter:
            self.status_setter(status)

    def predict_sentiment(self, dataset: Dataset):
        dataset_copy = deepcopy(dataset)
        n_batches = len(range(0, len(dataset), self.batch_size))

        for batch_ix in range(0, len(dataset), self.batch_size):
            batch = dataset_copy[batch_ix:batch_ix + self.batch_size]
            sentences_batch = [sample.text for sample in batch]
            model_batch = self.tokenizer(sentences_batch, return_tensors="pt", padding=True, truncation=True)
            model_batch = {k: v.to(self.device) for k, v in model_batch.items()}
            fw = self.model(**model_batch)[0]
            scores = Softmax(dim=-1)(fw).cpu().detach().numpy().tolist()

            for sample_ix, (sample, score) in enumerate(zip(batch, scores)):
                scores_dict = {
                    f'score_{i + 1}': f'{s:.3f}' for i, s in zip(range(0, 5), score)
                }
                scores_dict["score"] = f'{float(score @ np.linspace(0, 1, 5)):.3f}'
                sample.sentiment = scores_dict

                if batch_ix == 0 and sample_ix == 0:
                    self.set_status(f'first sentiment is {sample} {score}')

            self.set_status(f"Looking for sentiment [{batch_ix + len(batch)}/{len(dataset)}]")

        # make space
        del self.model
        torch.cuda.empty_cache()

        return dataset_copy


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--in-file", type=str, required=True)
    parser.add_argument("--out-file", type=str, required=True)
    args = parser.parse_args()
    assert os.path.exists(args.in_file)
    assert not os.path.exists(args.out_file)
    return args


def main():
    args = parse_args()
    model = SentimentAnalysisModel()
    with open(args.in_file, "r") as file:
        in_sentences = [line.strip() for line in file.readlines()]

    output = list()
    model.predict_sentiment(sentences=in_sentences)
    return
    for s in tqdm.tqdm(in_sentences):
        predictions = predict(s)
        predictions["sentence"] = s
        output.append(predictions)

    import pandas as pd
    df = pd.DataFrame(output)
    df.to_excel(args.out_file, index=False)

    from src.ml.data import Dataset, DataSample
    sample = DataSample(text="This is shit")
    dataset = Dataset([sample] * 100)
    model = SentimentAnalysisModel()
    dataset_bis = model.predict_sentiment(dataset)
    dataset_bis[0].__dict__


if __name__ == "__main__":
    main()
    