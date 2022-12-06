# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods
# pylint: disable=unused-import
# pylint: disable=import-error
# pylint: disable=W

import numpy as np

from src.metrics import Metrics
from src.utils import generate_example_points
from src.axis import Point, Threshold


class Data:
    def __init__(self):
        self.save_file = "res.csv"
        self.points = []
        self.threshold = None

    def init_axis_data(self, min, max):
        self.__init_random_points(min, max)
        self.__init__threshold()

    def load_points(self, souce_file_name):
        pass

    def update(self):
        self.__update_accuracy_score()
        self.__update_roc_curve()
        self.__update_f1_score()
        self.__update_matrix()
        self.__update_mmc_score()
        self.__update_recall_score()
        self.__update_auc_score()

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

    def __update_f1_score(self):
        pass

    def __update_accuracy_score(self):
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
        pass

    def _update_precision_score(self, y_pred, true_pos):
        precision = self.metrics.calculate_precision(y_pred, true_pos)
        # update ...
        # try catch?
        return precision

    def _update_f1_score(self):
        pass

    def __update_recall_score(self):
        pass

    def __update_roc_curve(self):
        pass

    def __update_auc_score(self):
        pass

    def __update_mmc_score(self):
        pass

    def __update_matrix(self):
        pass

    def save(self):
        pass
