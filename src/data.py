# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods
# pylint: disable=unused-import
# pylint: disable=import-error
# pylint: disable=W

import numpy as np

from src.metrics import Metrics


class Data:
    def __init__(self):
        self.save_file = "res.csv"
        self.metrics = Metrics()

    def update(self):
        y_true = np.array([1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                          dtype=int)
        y_vals = np.array([0.2, 0.1, 0.9, 0.8, 0.7, 0.6, 0.3, 0.4, 0.2, 0.1],
                          dtype=int)
        thr = 0.5
        y_pred = self.metrics.convert_to_binary(y_vals, thr)

        true_pos = self.metrics.get_true_pos(y_true, y_pred)
        # false_pos = self.metrics.get_false_pos(y_true, y_pred)
        # false_neg = self.metrics.get_false_neg(y_true, y_pred)
        # true_neg = self.metrics.get_true_neg(y_true, y_pred)

        self._update_precision_score(y_pred, true_pos)
        self._update_recall_score(y_true, true_pos)

    def _update_precision_score(self, y_pred, true_pos):
        precision = self.metrics.calculate_precision(y_pred, true_pos)
        # update ...
        # try catch?
        return precision

    def _update_recall_score(self, y_true, true_pos):
        recall = self.metrics.calculate_recall(y_true, true_pos)
        return recall

    def _update_f1_score(self):
        pass

    def _update_accuracy_score(self):
        pass

    def _update_roc_curve(self):
        pass

    def _update_mmc_score(self):
        pass

    def _update_matrix(self):
        pass

    def save(self):
        pass
