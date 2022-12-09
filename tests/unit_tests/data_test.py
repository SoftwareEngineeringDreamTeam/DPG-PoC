# pylint: skip-file
# pylint: disable-msg=R0801
import numpy as np

from src import data
from src.axis import Point, Threshold


def prepare_data():
    vals = [0, 0, 1, 1, 1, 1, 0, 0, 0]
    x_coord = np.linspace(0, 8, num=9)
    test_data = data.Data()
    test_data.threshold = Threshold(4)
    test_data.points = [Point(x_coord[i], vals[i]) for i in range(9)]
    test_data.add_point(9, 0)
    return test_data


def test_data_gets_arrays_from_points():
    vals = [0, 0, 1, 1, 1, 1, 0, 0, 0, 0]
    y_pred = np.zeros(5, dtype=int)
    y_pred = np.append(y_pred, np.ones(5, dtype=int))
    test_data = prepare_data()
    np.testing.assert_array_equal(np.array(vals), test_data.y_true)
    np.testing.assert_array_equal(y_pred, test_data.y_pred)
    np.testing.assert_array_equal(np.linspace(0, 9, num=10),
                                  test_data.y_vals)


def test_data_updates_true_pos():
    test_data = prepare_data()
    assert 1 == test_data._true_pos


def test_data_updates_true_neg():
    test_data = prepare_data()
    assert 2 == test_data._true_neg


def test_data_updates_false_pos():
    test_data = prepare_data()
    assert 4 == test_data._false_pos


def test_data_updates_false_neg():
    test_data = prepare_data()
    assert 3 == test_data._false_neg


def test_data_finds_precision_error():
    test_data = data.Data()
    test_data.threshold = Threshold(4)
    test_data.add_point(0, 1)
    assert "NaN" == test_data._precision[1]


def test_data_updates_precision():
    test_data = prepare_data()
    assert 1/5 == test_data._precision[1]
    test_data.add_point(10, 1)
    assert 1/5 == test_data._precision[0]
    assert 1/3 == test_data._precision[1]
    test_data.add_point(0.5, 0)
    assert 1/3 == test_data._precision[0]
    assert 1/3 == test_data._precision[1]


def test_data_finds_recall_error():
    test_data = data.Data()
    test_data.threshold = Threshold(4)
    test_data.add_point(6, 0)
    assert "NaN" == test_data._recall[1]


def test_data_updates_recall():
    test_data = prepare_data()
    assert 1/4 == test_data._recall[1]
    test_data.add_point(1, 1)
    assert 1/4 == test_data._recall[0]
    assert 1/5 == test_data._recall[1]
    test_data.add_point(1, 0)
    assert 1/5 == test_data._recall[0]
    assert 1/5 == test_data._recall[1]


def test_data_updates_specificity():
    test_data = prepare_data()
    assert 2/6 == test_data._specificity[1]
    test_data.add_point(0.5, 0)
    assert 2/6 == test_data._specificity[0]
    assert 3/7 == test_data._specificity[1]
    test_data.add_point(11, 1)
    assert 3/7 == test_data._specificity[0]
    assert 3/7 == test_data._specificity[1]


def test_data_updates_balanced_accuracy():
    test_data = prepare_data()
    assert (1/3+1/4)/2 == test_data._balanced_accuracy[1]
    test_data.add_point(0.5, 0)
    assert (1/3+1/4)/2 == test_data._balanced_accuracy[0]
    assert (3/7+1/4)/2 == test_data._balanced_accuracy[1]


def test_data_updates_f1():
    test_data = prepare_data()
    assert (1/10)/(9/20) == test_data._f1_score[1]
    test_data.add_point(0.5, 0)
    assert (1/10)/(9/20) == test_data._f1_score[0]
    assert (1/10)/(9/20) == test_data._f1_score[1]


def test_data_updates_accuracy():
    test_data = prepare_data()
    assert 3/10 == test_data._accuracy[1]
    test_data.add_point(1, 1)
    assert 3/10 == test_data._accuracy[0]
    assert 3/11 == test_data._accuracy[1]
    test_data.add_point(11, 1)
    assert 3/11 == test_data._accuracy[0]
    assert 4/12 == test_data._accuracy[1]


def test_data_updates_confusion_matrix():
    test_data = prepare_data()
    np.testing.assert_array_equal(np.array([[1, 4], [3, 2]]),
                                  test_data._confusion_matrix[1])
    test_data.add_point(11, 1)
    np.testing.assert_array_equal(np.array([[1, 4], [3, 2]]),
                                  test_data._confusion_matrix[0])
    np.testing.assert_array_equal(np.array([[2, 4], [3, 2]]),
                                  test_data._confusion_matrix[1])


def test_data_updates_mcc_score():
    test_data = prepare_data()
    assert (2-12)/np.sqrt(24*25) == test_data._mcc_score[1]
    test_data.add_point(11, 1)
    assert (2-12)/np.sqrt(24*25) == test_data._mcc_score[0]
    assert (4-12)/30 == test_data._mcc_score[1]
