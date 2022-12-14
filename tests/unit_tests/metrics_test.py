# pylint: skip-file
# pylint: disable-msg=R0801
import numpy as np
import pytest

from src.metrics import Metrics


def generate_example_labels():
    y_true = np.array([1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                      dtype=int)
    y_pred = np.array([0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
                      dtype=int)
    # tn: 4
    # fp: 3
    # tp: 1
    # fn: 2
    return y_true, y_pred


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
    assert tp == 1
    assert metrics.get_true_pos(y_empty, y_empty) == 0


def test_metrics_calculates_tn():
    y_true, y_pred = generate_example_labels()
    y_empty = np.array([])
    metrics = Metrics()
    tn = metrics.get_true_neg(y_true, y_pred)
    assert tn == 4
    assert metrics.get_true_neg(y_empty, y_empty) == 0


def test_metrics_calculates_fp():
    y_true, y_pred = generate_example_labels()
    y_empty = np.array([])
    metrics = Metrics()
    fp = metrics.get_false_pos(y_true, y_pred)
    assert fp == 3
    assert metrics.get_false_pos(y_empty, y_empty) == 0


def test_metrics_calculates_fn():
    y_true, y_pred = generate_example_labels()
    y_empty = np.array([])
    metrics = Metrics()
    fn = metrics.get_false_neg(y_true, y_pred)
    assert fn == 2
    assert metrics.get_false_neg(y_empty, y_empty) == 0


def test_metrics_calculates_precision():
    y_true, y_pred = generate_example_labels()

    y_zeros = np.zeros(y_true.shape, dtype=int)
    y_empty = np.array([])
    metrics = Metrics()
    true_pos = metrics.get_true_pos(y_true, y_pred)
    precision = metrics.calculate_precision(y_pred, true_pos)
    # 1/(4)
    assert precision == 0.25
    precision = metrics.calculate_precision(y_empty, 0)
    assert precision == "NaN"
    precision = metrics.calculate_precision(y_zeros, 0)
    assert precision == "NaN"


def test_metrics_calculates_recall():
    y_true, y_pred = generate_example_labels()
    y_zeros = np.zeros(y_true.shape, dtype=int)
    y_empty = np.array([])
    metrics = Metrics()
    true_pos = metrics.get_true_pos(y_true, y_pred)
    recall = metrics.calculate_recall(y_true, true_pos)
    # 1/(3)
    assert recall == 1/3
    recall = metrics.calculate_recall(y_empty, 0)
    assert recall == "NaN"
    recall = metrics.calculate_recall(y_zeros, 0)
    assert recall == "NaN"


def test_metrics_calculates_f1():
    # 2*1/3*1/4/(3/12+4/12) = (2/12)/(7/12) = 2/7
    precision = 1/4
    recall = 1/3
    metrics = Metrics()
    f1_score = metrics.calculate_f1_score(precision, recall)
    assert f1_score == pytest.approx(2/7)
    f1_score = metrics.calculate_f1_score(0, 0)
    assert f1_score == "NaN"


def test_metrics_calculates_accuracy():
    # 5/10
    y_true, y_pred = generate_example_labels()
    y_empty = np.array([])
    metrics = Metrics()
    true_pos = metrics.get_true_pos(y_true, y_pred)
    true_neg = metrics.get_true_neg(y_true, y_pred)
    accuracy_score = metrics.calculate_accuracy(true_pos,
                                                true_neg,
                                                y_true)
    assert accuracy_score == 0.5
    accuracy_score = metrics.calculate_accuracy(0, 0, y_empty)
    assert accuracy_score == "NaN"


def test_metrics_calculates_mcc():
    matrix = np.array([[1, 3], [2, 4]])
    matrix_zeros = np.zeros((2, 2))
    y_true, y_pred = generate_example_labels()
    y_empty = np.array([])
    y_zeros = np.zeros(y_true.shape, dtype=int)
    y_ones = np.ones(y_true.shape, dtype=int)
    metrics = Metrics()
    # (1*4 - 3*2)/sqrt(4*3*6*7)
    mcc = metrics.calculate_mcc(matrix, y_true, y_pred)
    assert mcc == pytest.approx((1*4 - 3*2)/np.sqrt(4*3*6*7))
    mcc = metrics.calculate_mcc(matrix_zeros, y_empty, y_empty)
    assert mcc == "NaN"
    mcc = metrics.calculate_mcc(matrix_zeros, y_zeros, y_pred)
    assert mcc == "NaN"
    mcc = metrics.calculate_mcc(matrix_zeros, y_true, y_zeros)
    assert mcc == "NaN"
    mcc = metrics.calculate_mcc(matrix_zeros, y_ones, y_pred)
    assert mcc == "NaN"
    mcc = metrics.calculate_mcc(matrix_zeros, y_true, y_ones)
    assert mcc == "NaN"


def test_metrics_calculates_specificity():
    y_true, y_pred = generate_example_labels()
    y_ones = np.ones(y_true.shape, dtype=int)
    y_empty = np.array([])
    metrics = Metrics()
    true_neg = metrics.get_true_neg(y_true, y_pred)
    specificity = metrics.calculate_specificity(y_true, true_neg)
    # 4/(7)
    assert specificity == 4/7
    specificity = metrics.calculate_specificity(y_empty, 0)
    assert specificity == "NaN"
    specificity = metrics.calculate_specificity(y_ones, 0)
    assert specificity == "NaN"
