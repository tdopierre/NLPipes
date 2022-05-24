import {v4 as uuidv4} from 'uuid';

class ProcessConfig {
    constructor(title, description, pipes) {
        this.title = title;
        this.description = description;
        this.pipes = pipes;
    }
}

var predefinedConfigs = [];

function getProcessConfig(processName) {
    const fileId = uuidv4();

    if (processName === 'clustering') {
        const embedderId = uuidv4();
        const clusteringId = uuidv4();
        const pipes = [
            {
                'id': fileId,
                'pipe_type': 'file_reader',
                'name': 'File Reader',
                'config': {
                    file: null,
                    file_type: null,
                    split_on_punctuation: false,
                },
                'dependencies': [],
            },
            {
                'name': 'Embedding',
                'id': embedderId,
                'pipe_type': 'embedding',
                'config': {
                    'embedder_class': 'tfidf',
                },
                'dependencies': [
                    fileId,
                ],
            },
            {
                'name': 'Clustering',
                'id': clusteringId,
                'pipe_type': 'clustering',
                'config': {
                    'model_class': 'kmeans',
                    'model_config': {
                        'n_clusters': 10,
                    },
                },
                'dependencies': [
                    embedderId,
                ],
            },
        ];
        predefinedConfigs.push(new ProcessConfig('Clustering', 'Runs a clustering algorithm in raw inputs', pipes));
    } else if (processName === 'sentimentAnalysis') {
        const sentimentAnalyserId = uuidv4();
        const pipes = [
            {
                'id': fileId,
                'pipe_type': 'file_reader',
                'name': 'File Reader',
                'config': {
                    file: null,
                    file_type: null,
                    split_on_punctuation: false,
                },
                'dependencies': [],
            },
            {
                'name': 'Sentiment Analysis',
                'id': sentimentAnalyserId,
                'pipe_type': 'sentiment_analysis',
                'dependencies': [
                    fileId,
                ],
                'config': {},
            },
        ];
        predefinedConfigs.push(new ProcessConfig('Sentiment Analysis', 'Runs sentiment analysis on raw inputs', pipes));
    } else if (processName === 'clustering+sentimentAnalysis') {
        const embedderId = uuidv4();
        const clusteringId = uuidv4();
        const sentimentAnalyserId = uuidv4();
        const pipes = [
            {
                'id': fileId,
                'pipe_type': 'file_reader',
                'name': 'File Reader',
                'config': {
                    file: null,
                    file_type: null,
                    split_on_punctuation: false,
                },
                'dependencies': [],
            },
            {
                'name': 'Embedding',
                'id': embedderId,
                'pipe_type': 'embedding',
                'config': {
                    'embedder_config': {
                        'model_name_or_path': 'distiluse-base-multilingual-cased-v1',
                    },
                    'embedder_class': 'transformer',
                },
                'dependencies': [
                    fileId,
                ],
            },
            {
                'name': 'Clustering',
                'id': clusteringId,
                'pipe_type': 'clustering',
                'config': {
                    'model_class': 'kmeans',
                    'model_config': {
                        'n_clusters': 10,
                    },
                },
                'dependencies': [
                    embedderId,
                ],
            },
            {
                'name': 'Sentiment Analysis',
                'id': sentimentAnalyserId,
                'pipe_type': 'sentiment_analysis',
                'dependencies': [
                    fileId,
                ],
                'config': {},
            },
        ];
        predefinedConfigs.push(new ProcessConfig('Clustering + Sentiment Analysis', 'Runs Clustering & Sentiment Analysis on raw inputs', pipes));
    } else if (processName === 'fit-predict') {
        const labeledFileId = uuidv4();
        const unlabeledFileId = uuidv4();
        const modelId = uuidv4();
        const pipes = [
            {
                "id": labeledFileId,
                "pipe_type": "file_reader",
                "name": "Labeled File Reader",
                "config": {
                    "file_type": "csv",
                    "csv_separator": ",",
                    "file": {
                        "$path": ""
                    }
                },
                "dependencies": []
            },
            {
                "name": "Train model",
                "id": modelId,
                "pipe_type": "train_classifier",
                "dependencies": [
                    labeledFileId
                ],
                "config": {
                    "classification_model": "TransformerClassifier",
                    "classification_model_config": {
                        "embedder_class": "tfidf"
                    }
                }
            },
            {
                "id": unlabeledFileId,
                "pipe_type": "file_reader",
                "name": "Unlabeled File Reader",
                "config": {
                    "file_type": "txt",
                    "file": {
                        "$path": ""
                    }
                },
                "dependencies": []
            },
            {
                "name": "Prediction",
                "id": "prediction",
                "pipe_type": "predict_classifier",
                "config": {},
                "dependencies": [
                    unlabeledFileId,
                    modelId
                ]
            }
        ];
        predefinedConfigs.push(new ProcessConfig('Classifier Fit+Predict', 'Trains a classifier on labeled data, then predicts on unlabeled data', pipes));
    }
}

const predefinedConfigNames = ["clustering", "sentimentAnalysis", "clustering+sentimentAnalysis", "fit-predict"]
predefinedConfigNames.forEach(predefinedConfigName => {
    getProcessConfig(predefinedConfigName);
});


export {getProcessConfig, predefinedConfigs};
