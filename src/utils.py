# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods
# pylint: disable=unused-import
# pylint: disable=import-error
# pylint: disable=W

from random import choices, randint

def generate_example_points(
        x_range: tuple,
        point_class,
        nr_of_points: int = 10,
        true_or_false_prc: float = 0.5
):
    return [
        point_class(
            randint(*x_range),
            choices(
                [False, True],
                [1-true_or_false_prc, true_or_false_prc]
            )[0]
        ) for _ in range(nr_of_points)
    ]
