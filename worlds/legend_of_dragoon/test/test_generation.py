import random
from .bases import LegendOfDragoonTestBase

from worlds.legend_of_dragoon.shop_randomization import generate_shop_randomization

class GenerationTest(LegendOfDragoonTestBase):

    def test_shop_generation(self):
        rng = random.Random(12345)
        assignment = generate_shop_randomization(rng)

        assert assignment
        assert len(assignment) == len(set(assignment.keys()))

        first = next(iter(assignment.items()))
        print(first)

        rng = random.Random(333333)
        assignment = generate_shop_randomization(rng)

        assert assignment
        assert len(assignment) == len(set(assignment.keys()))

        second = next(iter(assignment.items()))
        print(second)


