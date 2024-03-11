#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/06/06 15:38
# @Author      : shenjl
# @Email       : shenjl@lr.pi.titech.ac.jp
# @File        : main.py
# @Description :

import os
import sys
import numpy as np

from HumanEvaluation import HumanEvaluation
from ScoreData import ScoreData
from utils import load_json

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

INPUT_DIR = "data"
IMG_ROOT = "/Users/sgallon/Downloads/flickr30k-images"
OUTPUT_DIR = "output"
FILENAMES = ["original.csv", "gpt3.5.csv", "gpt4.csv"]
SAVE_FILENAME = "result.json"
MODEL_NAMES = [".".join(f.split(".")[:-1]) for f in FILENAMES]


def calc_total_score(model_names, scores):
    """
    :param model_names:
    :param scores:
    :return: {model_1: [score], model_2: [...], ...}
    """
    res = {}
    for m in model_names:
        res[m] = np.array([0.0])
        for item in scores:
            res[m] += ScoreData.read_score_single(m, item)
        res[m] = res[m] / len(scores)
    return res


def conclude():
    result = load_json(os.path.join(OUTPUT_DIR, SAVE_FILENAME))
    score = calc_total_score(MODEL_NAMES, result)
    print("Mean score is: {}".format(score))


def main():
    tsv_paths = [os.path.join(INPUT_DIR, f) for f in FILENAMES]
    save_name = os.path.join(OUTPUT_DIR, SAVE_FILENAME)
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        logger.info("Created output dir: {}".format(OUTPUT_DIR))
    task = HumanEvaluation(tsv_paths, IMG_ROOT, save_name)
    task.run()


if __name__ == "__main__":
    main()
    conclude()
