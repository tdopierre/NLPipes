import os
import logging

logging.basicConfig()


def get_logger(name):
    logger = logging.getLogger(name)
    if os.environ.get("APP_LOG_LEVEL") is not None:
        logger.setLevel(int(os.environ["APP_LOG_LEVEL"]))
    else:
        logger.setLevel(logging.DEBUG)
    return logger


def get_device():
    import torch
    if torch.cuda.is_available():
        return torch.device("cuda")
    else:
        return torch.device("cpu")
