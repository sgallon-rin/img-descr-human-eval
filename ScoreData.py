#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/6/9 19:17
# @Author      : sgallon
# @Email       : shcmsgallon@outlook.com
# @File        : Scorer.py
# @Description :
import os
from typing import Dict, List
import numpy as np

from utils import save_json

import logging

logger = logging.getLogger(__name__)

TEST_MODEL_NAMES = ["original", "ours"]

TEST_ITEMS = [
    {
        "img": "test/test-images/36979.jpg",
        "original": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "ours": "aaaa Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    },
    {
        "img": "test/test-images/65567.jpg",
        "original": "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
        "ours": "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
    },
    {
        "img": "test/test-images/81641.jpg",
        "original": "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
        "ours": "bbbb Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
    },
    {
        "img": "test/test-images/134206.jpg",
        "original": "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        "ours": "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
    },
    {
        "img": "test/test-images/148284.jpg",
        "original": "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        "ours": "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
    },
    {
        "img": "test/test-images/178045.jpg",
        "original": "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        "ours": "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
    }
]


class ScoreData:
    def __init__(self, model_names, items: List[Dict], save_path: str):
        if os.path.exists(save_path):
            logger.error("Output path is not empty!")
            raise RuntimeError("Output path is not empty!")
        self.model_names = model_names
        self.save_path = save_path
        self.items = items
        self.len = len(self.items)
        logger.info("Scorer initiated with {} samples".format(self.len))

    def score_single(self, idx, model_name, score):
        self.items[idx]["score_{}".format(model_name)] = score

    def save(self):
        save_json(self.items, self.save_path)
        logger.info("Saved score result to {}".format(self.save_path))

    @staticmethod
    def read_score_single(model_name: str, score_dict: dict):
        score = score_dict.get("score_{}".format(model_name))
        if not score:
            score = 0
        return np.array([score])


if __name__ == "__main__":
    pass
