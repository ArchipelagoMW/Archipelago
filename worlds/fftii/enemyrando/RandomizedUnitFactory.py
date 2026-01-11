from random import Random

from worlds.fftii.enemyrando.RandomizedUnits import RandomizedUnit


class RandomizedUnitFactory:
    units: dict[type[RandomizedUnit], int]
    random: Random

    def __init__(self, units: dict[type[RandomizedUnit], int], random: Random = Random()):
        self.units = units
        self.random = random


    def get_lowest_difficulty(self) -> int:
        return min([unit.difficulty for unit in self.units.keys()])

    def get_unit(self, difficulty: int) -> type[RandomizedUnit] | None:
        """Returns a unit from the factory with a difficulty less than or equal to the specified difficulty"""
        if difficulty < self.get_lowest_difficulty():
            return None
        eligible_units = {unit: self.units[unit] for unit in self.units.keys() if self.units[unit] <= difficulty}
        chosen_unit: type[RandomizedUnit] = self.random.sample(eligible_units, k=1, counts=eligible_units.values()).pop()
        return chosen_unit