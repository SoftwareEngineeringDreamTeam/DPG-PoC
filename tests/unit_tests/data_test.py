# pylint: skip-file
# pylint: disable-msg=R0801
import numpy as np

from src import data
from src.axis import Threshold


def test_data_gets_arrays_from_points():
    vals = [0, 0, 1, 1, 1, 1, 0, 0, 0, 0]
    y_pred = np.zeros(5, dtype=int)
    y_pred = np.append(y_pred, np.ones(5, dtype=int))
    test_data = data.Data()
    test_data.threshold = Threshold(4)
    for i in range(0, 10):
        test_data.add_point(i, vals[i])
    test_data._get_points_as_arrays()
    np.testing.assert_array_equal(np.array(vals), test_data.y_true)
    np.testing.assert_array_equal(y_pred, test_data.y_pred)
    np.testing.assert_array_equal(np.linspace(0, 9, num=10),
                                  test_data.y_vals)
