# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods
# pylint: disable=unused-import
# pylint: disable=import-error
# pylint: disable=W

import numpy as np

from src.axis import Point, Threshold
from src.metrics import Metrics
from src.utils import generate_example_points


class Data:
    _true_pos = None
    _true_neg = None
    _false_pos = None
    _false_neg = None
    _precision = None
    _recall = None
    _specificity = None
    _balanced_accuracy = None
    _f1_score = None

    def __init__(self):
        self.save_file = "res.csv"
        self.points = []
        self.threshold = None
        self.y_true = np.array([])
        self.y_pred = np.array([])
        self.y_vals = np.array([])
        self.metrics = Metrics()

    def init_axis_data(self, min, max):
        self.__init_random_points(min, max)
        self.__init__threshold()

    def load_points(self, source_file_name):
        pass

    def update(self):
        # preparations
        self._get_points_as_arrays()
        self.__update_true_pos()
        self.__update_true_neg()
        self.__update_false_pos()
        self.__update_false_neg()
        # metrics
        self.__update_precision()
        self.__update_recall()
        self.__update_specificity()
        self.__update_balanced_accuracy()
        self.__update_f1_score()
        # self.__update_accuracy_score()
        # self.__update_roc_curve()
        # self.__update_matrix()
        # self.__update_mmc_score()
        # self.__update_recall_score()
        # self.__update_auc_score()

    def add_point(self, x_position, value):
        self.points.append(Point(x_position, value))
        self.update()

    def switch_points_values(self):
        for point in self.points:
            point.value = not point.value

    def delete_point(self, point):
        self.points.remove(point)
        self.update()

    def __init_random_points(self, min, max):
        self.points = generate_example_points((min, max), Point)

    def __init__threshold(self):
        self.threshold = Threshold(400)

    def _get_points_as_arrays(self):
        y_true = np.zeros(len(self.points))
        self.y_vals = np.zeros(len(self.points))
        for i, point in enumerate(self.points):
            self.y_vals[i] = point.x_pos
            y_true[i] = point.get_value()
        self.y_pred = self.metrics.convert_to_binary(self.y_vals,
                                                     self.threshold.x_pos)
        self.y_true = y_true.astype(int)

    @property
    def __true_pos(self):
        if self._true_pos is None:
            self._true_pos = self.metrics.get_true_pos(self.y_true,
                                                       self.y_pred)
        return self._true_pos

    def __update_true_pos(self):
        self._true_pos = self.metrics.get_true_pos(self.y_true,
                                                   self.y_pred)

    @property
    def __true_neg(self):
        if self._true_neg is None:
            self._true_neg = self.metrics.get_true_neg(self.y_true,
                                                       self.y_pred)
        return self._true_neg

    def __update_true_neg(self):
        self._true_neg = self.metrics.get_true_neg(self.y_true,
                                                   self.y_pred)

    @property
    def __false_pos(self):
        if self._false_pos is None:
            self._false_pos = self.metrics.get_false_pos(self.y_true,
                                                         self.y_pred)
        return self._false_pos

    def __update_false_pos(self):
        self._false_pos = self.metrics.get_false_pos(self.y_true,
                                                     self.y_pred)

    @property
    def __false_neg(self):
        if self._false_neg is None:
            self._false_neg = self.metrics.get_false_neg(self.y_true,
                                                         self.y_pred)
        return self._false_neg

    def __update_false_neg(self):
        self._false_neg = self.metrics.get_false_neg(self.y_true,
                                                     self.y_pred)

    @property
    def __precision(self):
        if self._precision is None:
            precision = self.metrics.calculate_precision(self.y_pred,
                                                         self.__true_pos)
            self._precision = [0, precision]
        return self._precision

    def __update_precision(self):
        old_precision = self.__precision
        cur_precision = self.metrics.calculate_precision(self.y_pred,
                                                         self.__true_pos)
        self._precision = [old_precision[1], cur_precision]

    @property
    def __recall(self):
        if self._recall is None:
            recall = self.metrics.calculate_recall(self.y_true,
                                                   self.__true_pos)
            self._recall = [0, recall]
        return self._recall

    def __update_recall(self):
        old_recall = self.__recall
        cur_recall = self.metrics.calculate_recall(self.y_true,
                                                   self.__true_pos)
        self._recall = [old_recall[1], cur_recall]

    @property
    def __specificity(self):
        if self._specificity is None:
            specificity = self.metrics.calculate_specificity(self.y_true,
                                                             self.__true_neg)
            self._specificity = [0, specificity]
        return self._specificity

    def __update_specificity(self):
        old_specificity = self.__specificity
        cur_specificity = self.metrics.calculate_specificity(self.y_true,
                                                             self.__true_neg)
        self._specificity = [old_specificity[1], cur_specificity]

    @property
    def __balanced_accuracy(self):
        if self._balanced_accuracy is None:
            balanced_accuracy = (self.__recall[1] + self.__specificity[1])/2
            self._balanced_accuracy = [0, balanced_accuracy]
        return self._balanced_accuracy

    def __update_balanced_accuracy(self):
        old_bal_acc = self.__balanced_accuracy
        cur_bal_acc = (self.__recall[1] + self.__specificity[1])/2
        self._balanced_accuracy = [old_bal_acc[1], cur_bal_acc]

    @property
    def __f1_score(self):
        if self._f1_score is None:
            f1_score = self.metrics.calculate_f1_score(self.__precision[1],
                                                       self.__recall[1])
            self._f1_score = [0, f1_score]
        return self._f1_score

    def __update_f1_score(self):
        old_f1 = self.__f1_score
        cur_f1 = self.metrics.calculate_f1_score(self.__precision[1],
                                                 self.__recall[1])
        self._f1_score = [old_f1[1], cur_f1]

    def __update_accuracy_score(self):
        self.metrics = Metrics()

    # def update(self):
    #     _ = self._update_accuracy_score(true_pos, true_neg, y_true)
    #     matrix = np.array([[true_pos, false_pos], [false_neg, true_neg]])
    #     self._update_matrix(matrix)
    #     _ = self._update_mcc_score(matrix, y_true, y_pred)
    #     fpr, tpr = self._update_roc_curve(y_true, y_vals)
    #     _ = self._update_auc(fpr, tpr)

    def _update_precision_score(self, y_pred, true_pos):
        precision = self.metrics.calculate_precision(y_pred, true_pos)
        # update ...
        # try catch?
        return precision

    def _update_recall_score(self, y_true, true_pos):
        recall = self.metrics.calculate_recall(y_true, true_pos)
        return recall

    def _update_specificity(self, y_true, true_neg):
        specificity = self.metrics.calculate_specificity(y_true, true_neg)
        return specificity

    def _update_accuracy_score(self, true_pos, true_neg, y_true):
        accuracy = self.metrics.calculate_accuracy(true_pos, true_neg, y_true)
        return accuracy

    def _update_balanced_accuracy(self, sensitivity, specificity):
        balanced_accuracy = (sensitivity + specificity)/2
        return balanced_accuracy

    def _update_roc_curve(self, y_true, y_val):
        fpr, tpr = self.metrics.calculate_roc(y_true, y_val)
        # plot the data
        return fpr, tpr

    def _update_auc(self, fpr, tpr):
        auc = self.metrics.calculate_auc(fpr, tpr)
        return auc

    def _update_mcc_score(self, confusion_matrix, y_true, y_pred):
        mcc_score = self.metrics.calculate_mcc(confusion_matrix,
                                               y_true, y_pred)
        return mcc_score

    def _update_matrix(self, matrix):
        # update the matrix
        print(matrix)

    def save(self):
        pass
