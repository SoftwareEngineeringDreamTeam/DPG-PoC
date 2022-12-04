# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods
# pylint: disable=unused-import
# pylint: disable=import-error
# pylint: disable=W

import numpy as np


class Metrics:
    def get_true_pos(self, y_true, y_pred):
        if y_true.shape[0] == 0:
            return 0
        return np.sum(y_true & y_pred)

    def get_true_neg(self, y_true, y_pred):
        if y_true.shape[0] == 0:
            return 0
        y_true = y_true.astype(bool)
        y_pred = y_pred.astype(bool)
        return np.sum(~y_true & ~y_pred)

    def get_false_pos(self, y_true, y_pred):
        if y_true.shape[0] == 0:
            return 0
        y_true = y_true.astype(bool)
        return np.sum(~y_true & y_pred)

    def get_false_neg(self, y_true, y_pred):
        if y_true.shape[0] == 0:
            return 0
        y_pred = y_pred.astype(bool)
        return np.sum(y_true & ~y_pred)

    def convert_to_binary(self, y_vals, thr):
        labels = y_vals > thr
        return labels.astype(int)

    def calculate_precision(self, y_true, y_pred):
        pass

    def calculate_recall(self, y_true, y_pred):
        pass

    def calculate_f1_score(self, y_true, y_pred):
        pass

    def calculate_accuracy(self, y_true, y_pred):
        pass

    def calculate_tp_rate(self, y_true, y_pred):
        pass

    def calculate_fp_rate(self, y_true, y_pred):
        pass

    def calculate_mmc(self, y_true, y_pred):
        pass

    def calculate_confusion_matrix(self, y_true, y_pred):
        pass
