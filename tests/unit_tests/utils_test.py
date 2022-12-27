# pylint: skip-file
# pylint: disable-msg=R0801
from src.axis import Point
from src.utils import generate_example_points

def test_utils_value_range():
    min_val = 0
    max_val = 100
    generated_points = generate_example_points((min_val, max_val), Point)
    for point in generated_points:
        assert point.x_pos >= 0 and point.x_pos <= 100

def test_utils_point_class():
    min_val = 0
    max_val = 100
    generated_points = generate_example_points((min_val, max_val), Point)
    for point in generated_points:
        assert isinstance(point, Point)

def test_utils_number_of_points():
    min_val = 0
    max_val = 100
    nr_of_points = 10
    generated_points = generate_example_points((min_val, max_val), Point, nr_of_points)
    assert len(generated_points) == nr_of_points

def test_utils_always_true():
    min_val = 0
    max_val = 100
    generated_points = generate_example_points((min_val, max_val), Point, true_or_false_prc = 1.0)
    for point in generated_points:
        assert point.label == True

def test_utils_always_false():
    min_val = 0
    max_val = 100
    generated_points = generate_example_points((min_val, max_val), Point, true_or_false_prc = 0.0)
    for point in generated_points:
        assert point.label == False
