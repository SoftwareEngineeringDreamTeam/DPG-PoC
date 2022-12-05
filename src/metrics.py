# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods
# pylint: disable=unused-import
# pylint: disable=import-error
# pylint: disable=W

import numpy as np

from src import events


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

    def calculate_precision(self, y_pred, true_pos):
        all_pos_pred = np.sum(y_pred)
        if all_pos_pred == 0:
            raise events.PrecisionException
        return true_pos/all_pos_pred

    def calculate_recall(self, y_true, true_pos):
        all_pos_ground_truths = np.sum(y_true)
        if all_pos_ground_truths == 0:
            raise events.RecallException
        return true_pos/all_pos_ground_truths

    def calculate_specificity(self, y_true, true_neg):
        all_neg_ground_truths = y_true.shape[0] - np.sum(y_true)
        if all_neg_ground_truths == 0:
            raise events.SpecificityException
        return true_neg/all_neg_ground_truths

    def calculate_f1_score(self, precision, recall):
        if precision == 0 and recall == 0:
            raise events.F1Exception
        f1_score = 2*precision*recall/(precision+recall)
        return f1_score

    def calculate_accuracy(self, true_pos, true_neg, y_true):
        all_samples = y_true.shape[0]
        if all_samples == 0:
            raise events.AccuracyException
        accuracy = (true_pos + true_neg)/all_samples
        return accuracy

    def calculate_tp_rate(self, y_true, y_pred):
        pass

    def calculate_fp_rate(self, y_true, y_pred):
        pass

    def calculate_roc(self):
        pass

    def calculate_mcc(self, matrix, y_true, y_pred):
        true_vals = np.sum(y_true)*(y_true.shape - np.sum(y_true))
        pred_vals = np.sum(y_pred)*(y_pred.shape - np.sum(y_pred))
        denom = np.sqrt(pred_vals*true_vals)
        if denom == 0:
            raise events.MCCException
        correct_pred = matrix[0, 0]*matrix[1, 1]
        false_pred = matrix[0, 1]*matrix[1, 0]
        mcc = (correct_pred - false_pred)/denom
        return mcc
