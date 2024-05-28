from __future__ import annotations
from typing import List, Callable, Tuple
import math

from .structs import LayoutType, SC2MOGenMission

def _empty_slot() -> SC2MOGenMission:
    slot = SC2MOGenMission(None, None, set())
    slot.option_empty = True
    return slot

class Column(LayoutType):
    """Linear layout. Default entrance is index 0 at the top, default exit is index `size - 1` at the bottom."""

    def make_slots(self, mission_factory: Callable[[], SC2MOGenMission]) -> List[SC2MOGenMission]:
        missions = [mission_factory() for _ in range(self.size)]
        missions[0].option_entrance = True
        missions[-1].option_exit = True
        for i in range(self.size - 1):
            missions[i].next.add(missions[i + 1])
        return missions
    
    def get_slot_data(self, slots: List[SC2MOGenMission]) -> List[List[SC2MOGenMission]]:
        return [slots]

class Grid(LayoutType):
    """Rectangular grid. Default entrance is index 0 in the top left, default exit is index `size - 1` in the bottom right."""
    width: int
    height: int
    num_corners_to_remove: int

    def __init__(self, size: int, limit: int):
        super().__init__(size, limit)
        if limit == 0:
            self.width, self.height, self.num_corners_to_remove = Grid.get_grid_dimensions(size)
        else:
            self.width = limit
            self.height = math.ceil(size / self.width)
            self.num_corners_to_remove = self.height * limit - size
        
    def get_factors(number: int) -> Tuple[int, int]:
        """
        Simple factorization into pairs of numbers (x, y) using a sieve method.
        Returns the factorization that is most square, i.e. where x + y is minimized.
        Factor order is such that x <= y.
        """
        assert number > 0
        for divisor in range(math.floor(math.sqrt(number)), 1, -1):
            quotient = number // divisor
            if quotient * divisor == number:
                return divisor, quotient
        return 1, number

    def get_grid_dimensions(size: int) -> Tuple[int, int, int]:
        """
        Get the dimensions of a grid mission order from the number of missions, int the format (x, y, error).
        * Error will always be 0, 1, or 2, so the missions can be removed from the corners that aren't the start or end.
        * Dimensions are chosen such that x <= y, as buttons in the UI are wider than they are tall.
        * Dimensions are chosen to be maximally square. That is, x + y + error is minimized.
        * If multiple options of the same rating are possible, the one with the larger error is chosen,
        as it will appear more square. Compare 3x11 to 5x7-2 for an example of this.
        """
        dimension_candidates: List[Tuple[int, int, int]] = [(*Grid.get_factors(size + x), x) for x in (2, 1, 0)]
        best_dimension = min(dimension_candidates, key=sum)
        return best_dimension

    def get_grid_coordinates(self, idx: int) -> Tuple[int, int]:
        return math.floor(idx / self.width), (idx % self.width)
    
    def get_grid_index(self, x: int, y: int) -> int:
        return y * self.width + x
    
    def is_valid_coordinates(self, x: int, y: int) -> bool:
        return (
            x >= 0 and x < self.width and
            y >= 0 and y < self.height
        )

    def make_slots(self, mission_factory: Callable[[], SC2MOGenMission]) -> List[SC2MOGenMission]:
        missions = [mission_factory() for _ in range(self.width * self.height)]
        missions[0].option_entrance = True
        missions[-1].option_exit = True

        for x in range(self.width):
            left = x - 1
            right = x + 1
            for y in range(self.height):
                up = y - 1
                down = y + 1
                idx = self.get_grid_index(x, y)
                neighbours = [
                    self.get_grid_index(nb_x, nb_y)
                    for (nb_x, nb_y) in [(left, y), (right, y), (x, up), (x, down)]
                    if self.is_valid_coordinates(nb_x, nb_y)
                ]
                missions[idx].next = {missions[nb] for nb in neighbours}
        
        # Empty corners
        top_corners = math.floor(self.num_corners_to_remove / 2)
        bottom_corners = math.ceil(self.num_corners_to_remove / 2)

        # Bottom left corners
        y = self.height - 1
        x = 0
        leading_x = 0
        placed = 0
        while placed < bottom_corners:
            if x == -1 or y == 0:
                leading_x += 1
                x = leading_x
                y = self.height - 1
            missions[self.get_grid_index(x, y)].option_empty = True
            placed += 1
            x -= 1
            y -= 1

        # Top right corners
        y = 0
        x = self.width - 1
        leading_x = self.width - 1
        placed = 0
        while placed < top_corners:
            if x == self.width or y == self.height - 1:
                leading_x -= 1
                x = leading_x
                y = 0
            missions[self.get_grid_index(x, y)].option_empty = True
            placed += 1
            x += 1
            y += 1

        return missions
    
    def get_slot_data(self, slots: List[SC2MOGenMission]) -> List[List[SC2MOGenMission]]:
        columns = [
            [slots[self.get_grid_index(x, y)] for y in range(self.height)]
            for x in range(self.width)
        ]
        return columns