# pylint: skip-file
# pylint: disable-msg=R0801
import numpy as np

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
    precision = metrics.calculate_precision(y_true, y_pred)
    # 1/(4)
    assert precision == 0.25
    precision_msg = metrics.calculate_precision(y_empty, y_empty)
    assert precision_msg == "No positive predictions."
    precision_msg = metrics.calculate_precision(y_true, y_zeros)
    assert precision_msg == "No positive predictions."


def test_metrics_calculates_recall():
    y_true, y_pred = generate_example_labels()
    y_zeros = np.zeros(y_true.shape, dtype=int)
    y_empty = np.array([])
    metrics = Metrics()
    recall = metrics.calculate_recall(y_true, y_pred)
    # 1/(3)
    assert recall == 1/3
    recall_msg = metrics.calculate_recall(y_empty, y_empty)
    assert recall_msg == "No positive ground truths."
    recall_msg = metrics.calculate_recall(y_zeros, y_pred)
    assert recall_msg == "No positive ground truths."
