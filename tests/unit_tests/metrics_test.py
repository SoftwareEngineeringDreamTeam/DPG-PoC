# pylint: skip-file
# pylint: disable-msg=R0801
import numpy as np

from src.metrics import Metrics


def generate_example_labels():
    zeros = np.zeros(30, dtype=int)
    ones = np.ones(20, dtype=int)
    # y_true: 60 no, 40 yes
    data1 = np.append(zeros, zeros)
    data1 = np.append(data1, ones)
    data1 = np.append(data1, ones)
    # 30 tn
    # 20 fp
    # 10 tn
    # 20 fn
    # 20 tp
    # y_pred: 30 no, 20 yes, 30 no, 20 yes
    data2 = np.append(zeros, ones)
    data2 = np.append(data2, data2)
    return data1, data2


def test_metrics_converts_to_binary():
    metrics = Metrics()
    y = np.linspace(0, 1, 100)
    y_pred = np.append(np.zeros(50, dtype=int),
                       np.ones(50, dtype=int))
    thr = 0.5
    y_binary = metrics.convert_to_binary(y, thr)
    np.testing.assert_array_equal(y_binary, y_pred)


def test_metrics_calculates_tp():
    y_true, y_pred = generate_example_labels()
    y_empty = np.array([])
    metrics = Metrics()
    tp = metrics.get_true_pos(y_true, y_pred)
    assert tp == 20
    assert metrics.get_true_pos(y_empty, y_empty) == 0


def test_metrics_calculates_tn():
    y_true, y_pred = generate_example_labels()
    y_empty = np.array([])
    metrics = Metrics()
    tn = metrics.get_true_neg(y_true, y_pred)
    assert tn == 40
    assert metrics.get_true_neg(y_empty, y_empty) == 0
