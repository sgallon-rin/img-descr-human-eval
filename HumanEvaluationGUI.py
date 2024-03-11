#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/06/06 15:17
# @Author      : shenjl
# @Email       : shenjl@lr.pi.titech.ac.jp
# @File        : HumanEvaluationGUI.py
# @Description :

import sys
import PySimpleGUI as sg
from collections import defaultdict

from ScoreData import ScoreData, TEST_MODEL_NAMES, TEST_ITEMS
from utils import jpg2png

import logging

logger = logging.getLogger(__name__)
# For DEBUG
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# theme_name_list = sg.theme_list()
# sg.preview_all_look_and_feel_themes()


class HumanEvaluationGUI:
    def __init__(self, score_data: ScoreData, min_score=1, max_score=5, default_score=3, hide_model_name=True, auto_save=True):
        sg.theme('DarkBlue')
        self.score_data = score_data
        assert min_score <= default_score <= max_score, "Wrong score setting!"
        self.min_score = min_score
        self.max_score = max_score
        self.default_score = default_score
        self.hide_model_name = hide_model_name
        self.auto_save = auto_save
        self.layout = []
        self.window = None
        self.idx = 0
        self._init_layout()
        logger.info("HumanEvaluationGUI initialized")

    @staticmethod
    def _read_jpg_as_png_data(jpg_path):
        assert jpg_path.endswith(".jpg"), "flickr30k-images has format jpg"
        return jpg2png(jpg_path)

    def _init_layout(self):
        item = self.score_data.items[0]
        layout = [
            [sg.Text('No.{}/{}'.format(1, self.score_data.len), key="idx")],
            # [sg.Image(self._read_jpg_as_png_data(item.get("img")), key="img", size=(700, 500))],
        ]
        for model_idx, model_name in enumerate(self.score_data.model_names):
            if self.hide_model_name:  # Model1, Model2, ...
                layout.append([sg.Text("Model{}:".format(model_idx + 1)),
                               sg.Text(item.get(model_name), key=model_name, size=(80, 4), background_color='white', text_color='black')])
            else:
                layout.append([sg.Text(model_name + ":"),
                               sg.Text(item.get(model_name), key=model_name, size=(80, 4), background_color='white', text_color='black')])
            # radios; deal with init from existing data later
            radios = [[sg.Text("Score:")]]
            for k in range(self.min_score, self.max_score + 1):
                r1 = sg.Radio(str(k), group_id='score_{}'.format(model_name),
                              key="score_{}_{}".format(model_name, k), default=(k == self.default_score))
                radios[0].append(r1)
            layout.extend(radios)
        buttons = [sg.Button('Save'), sg.Button('Previous'), sg.Button('Next'), sg.Button('Exit')]
        layout.append(buttons)
        img = [sg.Image(self._read_jpg_as_png_data(item.get("img")), key="img")]
        layout.append(img)
        self.layout = layout

    def _radio2score(self, window_value):
        res = dict()
        for m in self.score_data.model_names:
            for i in range(1, 6):
                if window_value.get("score_{}_{}".format(m, i)):
                    res["score_{}".format(m)] = i
                    break
        return res

    def _score2radio(self, item):
        res = dict()
        for m in self.score_data.model_names:
            s_m = item.get("score_{}".format(m))  # score of model
            for i in range(1, 6):
                res["score_{}_{}".format(m, i)] = False
            if s_m:
                res["score_{}_{}".format(m, s_m)] = True
            else:
                res["score_{}_{}".format(m, self.default_score)] = True
        return res

    def _check_same_text(self, item, value):
        model_scores = self._radio2score(value)
        short2model = defaultdict(list)
        for m in self.score_data.model_names:
            short = item[m]
            short2model[short].append(m)
        for short, models in short2model.items():
            if len(models) > 1:
                scores = [model_scores.get("score_{}".format(m)) for m in models]
                logger.debug(scores)
                if len(set(scores)) > 1:
                    logger.info("Same text should have same score! {}".format(model_scores))
                    return False
        return True

    def _make_layout_update_dict(self):
        item = self.score_data.items[self.idx]
        res = {"img": self._read_jpg_as_png_data(item.get("img")),
               "idx": 'No.{}/{}'.format(self.idx + 1, self.score_data.len)}
        for model_name in self.score_data.model_names:
            res[model_name] = item.get(model_name)
        radios = self._score2radio(item)
        res.update(radios)
        return res

    def _save_one(self, values):
        score = self._radio2score(values)
        self._check_same_text(self.score_data.items[self.idx], score)
        self.score_data.items[self.idx].update(score)

    def run(self):
        logger.info("Running HumanEvaluationGUI")
        self.window = sg.Window('Human Evaluation', self.layout, size=(1000, 800), resizable=True, finalize=True)
        while True:
            event, values = self.window.read()
            if not self._check_same_text(self.score_data.items[self.idx], values):
                sg.popup_error("Same text should have same score!")
            else:
                if event == sg.WIN_CLOSED or event == 'Exit':
                    self._save_one(values)
                    self.score_data.save()
                    sg.popup_notify("お疲れ様でした〜", display_duration_in_ms=10)
                    break
                elif event == 'Save':
                    # print(event)
                    # print(values)
                    self._save_one(values)
                    self.score_data.save()
                    sg.popup_quick_message("Saved!")
                elif event == 'Previous':
                    if self.idx == 0:
                        self._save_one(values)
                        self.score_data.save()
                        sg.popup_quick_message("This is the first item! Cannot go to previous item! Automatically saved result.")
                    else:
                        self._save_one(values)
                        if self.auto_save:
                            self.score_data.save()
                        self.idx -= 1
                        self._update_window()
                elif event == 'Next':
                    if self.idx == self.score_data.len - 1:
                        self._save_one(values)
                        self.score_data.save()
                        sg.popup_quick_message("This is the last item! Cannot go to next item! Automatically saved result.")
                    else:
                        self._save_one(values)
                        if self.auto_save:
                            self.score_data.save()
                        self.idx += 1
                        self._update_window()
        self.window.close()

    def _update_window(self):
        updates = self._make_layout_update_dict()
        for k, v in updates.items():
            self.window[k].update(v)


if __name__ == "__main__":
    # test
    test_scorer = ScoreData(TEST_MODEL_NAMES, TEST_ITEMS, "test/test_output.json")
    gui = HumanEvaluationGUI(test_scorer)
    gui.run()
