from random import choices, randint

from axis import Point


def generate_example_points(
        x_range: tuple,
        nr_of_points: int = 10,
        true_or_false_prc: float = 0.5
        ):
    return [
        Point(
            randint(*x_range),
            choices(
                [False, True],
                [1-true_or_false_prc, true_or_false_prc]
            )[0]
        ) for i in range(nr_of_points)
    ]
