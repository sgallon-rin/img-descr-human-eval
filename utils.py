#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/06/06 15:17
# @Author      : shenjl
# @Email       : shenjl@lr.pi.titech.ac.jp
# @File        : utils.py
# @Description :

import json
import pandas as pd
from PIL import Image
import io


def save_json(json_object, save_path: str, indent: int = 4):
    s = json.dumps(json_object, ensure_ascii=False, indent=indent)
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(s)


def load_json(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        res = json.load(f)
    return res


class ModelResult:
    def __init__(self, model_name: str, dataframe: pd.DataFrame):
        self.model_name = model_name
        self.df = dataframe


def jpg2png(jpg_file):
    # ref: https://3pysci.com/pysimplegui-10/
    img = Image.open(jpg_file)
    png_bio = io.BytesIO()
    img.save(png_bio, format="PNG")
    del img
    png_data = png_bio.getvalue()
    return png_data


def remove_duplicate_tab(input_tsv_path, output_tsv_path):
    with open(input_tsv_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open(output_tsv_path, "w", encoding="utf-8") as f:
        for line in lines:
            img_no, _, desc = line.strip().split("\t")
            f.write(img_no + "\t" + desc + "\n")
    print("Done")


if __name__ == "__main__":
    # remove_duplicate_tab("data/raw/original.csv", "data/original.csv")
    pass
