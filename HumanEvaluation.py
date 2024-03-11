#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/06/06 16:51
# @Author      : shenjl
# @Email       : shenjl@lr.pi.titech.ac.jp
# @File        : HumanEvaluation.py
# @Description :

import os.path
import pandas as pd
from typing import Dict, List

from utils import ModelResult
from ScoreData import ScoreData
from HumanEvaluationGUI import HumanEvaluationGUI

import logging

logger = logging.getLogger(__name__)


class HumanEvaluation:
    def __init__(self, tsv_paths: List[str], img_root: str, save_name: str):
        self.model_results = []
        self.combined_results = []
        self.img_root = img_root
        self.save_name = save_name
        self.model_names = []
        logger.info("Initializing HumanEvaluation")
        if not tsv_paths:
            logger.fatal("Empty tsv_paths: {}".format(tsv_paths))
            raise RuntimeError("Empty tsv_paths")
        self.init_from_tsvs(tsv_paths)
        self._check()
        self._combine()
        self.score_data = ScoreData(self.model_names, self.combined_results, self.save_name)
        self.gui = HumanEvaluationGUI(self.score_data)
        logger.info("HumanEvaluation successfully initialized")

    def run(self):
        self.gui.run()

    def save(self):
        raise NotImplementedError

    @staticmethod
    def read_tsv(tsv_path: str) -> pd.DataFrame:
        return pd.read_csv(tsv_path, encoding="utf-8", names=["img_no", "description"], delimiter='\t')

    def init_from_tsvs(self, tsv_paths: List[str]):
        assert len(tsv_paths) == len(set(tsv_paths))
        for tsv_path in tsv_paths:
            df = self.read_tsv(tsv_path)
            model_name = tsv_path.split(os.path.sep)[-1].split(".")
            model_name = ".".join(model_name[:-1])
            self.model_names.append(model_name)
            logger.info("Read result of model '{}' from '{}'".format(model_name, tsv_path))
            mr = ModelResult(model_name, df)
            self.model_results.append(mr)

    def _check(self):
        lens = [len(x.df) for x in self.model_results]
        if len(set(lens)) != 1:
            errmsg = "Data check failed! Wrong model results to combine! Lengths {} are not the same".format(lens)
            logger.error(errmsg)
            raise RuntimeError("Data check failed")
        logger.info("Data check passed")

    def _combine(self):
        model_names = [x.model_name for x in self.model_results]
        dfs = [x.df for x in self.model_results]
        res = []
        for i in range(len(dfs[0])):
            lines = [df.iloc[i] for df in dfs]
            img_no = [line["img_no"] for line in lines]
            descriptions = [line["description"] for line in lines]
            if len(set(img_no)) != 1:
                errmsg = "Wrong model results to combine! img_no {} are not the same".format(set(img_no))
                logger.error(errmsg)
                raise RuntimeError("Wrong model results to combine")
            img_no = img_no[0]
            item = {"img": "{}.jpg".format(os.path.join(self.img_root, str(img_no)))}
            for j in range(len(model_names)):
                model_name = model_names[j]
                assert model_name not in ["img_no", "description"], 'Model name cannot be ["img_no", "description"]'
                item[model_name] = descriptions[j]
            res.append(item)
        self.combined_results = res
