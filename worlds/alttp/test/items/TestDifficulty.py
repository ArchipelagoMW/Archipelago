from ...ItemPool import difficulties
from ..bases import TestBase

base_items = 41
extra_counts = (15, 15, 10, 5, 25)


class TestDifficulty(TestBase):
    pass


def build_difficulty_test(difficulty):
    # binds difficulty to definition local scope
    def build_for(function):
        def wrapped(self, *args):
            return function(self, difficulty, *args)

        return wrapped

    return build_for


def build_dynamic_tests():
    for name, difficulty in difficulties.items():

        @build_difficulty_test(difficulty)
        def test_dyn_difficulty(self, difficulty):
            base = len(difficulty.baseitems)
            self.assertEqual(base, base_items)

        setattr(TestDifficulty, f"testCountBase{name}", test_dyn_difficulty)

        @build_difficulty_test(difficulty)
        def test_dyn_difficulty(self, difficulty):
            self.assertEqual(len(extra_counts), len(difficulty.extras))

        setattr(TestDifficulty, f"testCountExtra{name}", test_dyn_difficulty)

        @build_difficulty_test(difficulty)
        def test_dyn_difficulty(self, difficulty):
            for i, extras in enumerate(extra_counts):
                self.assertEqual(extras, len(difficulty.extras[i]))

        setattr(TestDifficulty, f"testCountExtras{name}", test_dyn_difficulty)


build_dynamic_tests()
