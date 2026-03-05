import random
from collections.abc import Callable
from enum import Enum
from operator import add, mul, sub, truediv
from typing import NamedTuple

_random = random.Random()

class NumberChoiceConstraints(NamedTuple):
    num_1_min: int
    num_1_max: int
    num_2_min: int
    num_2_max: int
    commutative: bool
    operator: Callable[[int, int], int | float]


class MathProblemType(Enum):
    PLUS = 1
    MINUS = 2
    TIMES = 3
    DIVIDE = 4


MATH_PROBLEM_CONSTRAINTS = {
    MathProblemType.PLUS: NumberChoiceConstraints(1, 99, 1, 99, True, add),
    MathProblemType.MINUS: NumberChoiceConstraints(2, 99, 1, 99, False, sub),
    MathProblemType.TIMES: NumberChoiceConstraints(2, 10, 2, 50, True, mul),
    MathProblemType.DIVIDE: NumberChoiceConstraints(4, 99, 2, 50, False, truediv),
}


class MathProblem(NamedTuple):
    problem_type: MathProblemType
    num_1: int
    num_2: int
    result: int


def generate_math_problem(random_object: random.Random = _random) -> MathProblem:
    problem_type: MathProblemType = random_object.choice(list(MathProblemType))
    number_choice_constraints = MATH_PROBLEM_CONSTRAINTS[problem_type]

    for _ in range(10000):
        num_1 = random.randint(number_choice_constraints.num_1_min, number_choice_constraints.num_1_max)
        num_2 = random.randint(number_choice_constraints.num_2_min, number_choice_constraints.num_2_max)

        result = number_choice_constraints.operator(num_1, num_2)

        result_int = int(result)
        if not result_int == result:
            continue

        if result_int < 2 or result_int > 99:
            continue

        if number_choice_constraints.commutative:
            if random.randint(0, 1):
                num_1, num_2 = num_2, num_1

        return MathProblem(problem_type, num_1, num_2, result_int)

    return MathProblem(MathProblemType.PLUS, 1, 1, 2)
