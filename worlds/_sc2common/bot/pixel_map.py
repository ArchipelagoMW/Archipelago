from typing import Callable, FrozenSet, List, Set, Tuple, Union

from .position import Point2


class PixelMap:

    def __init__(self, proto, in_bits: bool = False):
        """
        :param proto:
        :param in_bits:
        """
        self._proto = proto
        # Used for copying pixelmaps
        self._in_bits: bool = in_bits

        assert self.width * self.height == (8 if in_bits else 1) * len(
            self._proto.data
        ), f"{self.width * self.height} {(8 if in_bits else 1)*len(self._proto.data)}"

    @property
    def width(self) -> int:
        return self._proto.size.x

    @property
    def height(self) -> int:
        return self._proto.size.y

    @property
    def bits_per_pixel(self) -> int:
        return self._proto.bits_per_pixel

    @property
    def bytes_per_pixel(self) -> int:
        return self._proto.bits_per_pixel // 8

    def __getitem__(self, pos: Tuple[int, int]) -> int:
        """ Example usage: is_pathable = self._game_info.pathing_grid[Point2((20, 20))] != 0 """
        assert 0 <= pos[0] < self.width, f"x is {pos[0]}, self.width is {self.width}"
        assert 0 <= pos[1] < self.height, f"y is {pos[1]}, self.height is {self.height}"
        return int(self.data_numpy[pos[1], pos[0]])

    def __setitem__(self, pos: Tuple[int, int], value: int):
        """ Example usage: self._game_info.pathing_grid[Point2((20, 20))] = 255 """
        assert 0 <= pos[0] < self.width, f"x is {pos[0]}, self.width is {self.width}"
        assert 0 <= pos[1] < self.height, f"y is {pos[1]}, self.height is {self.height}"
        assert (
            0 <= value <= 254 * self._in_bits + 1
        ), f"value is {value}, it should be between 0 and {254 * self._in_bits + 1}"
        assert isinstance(value, int), f"value is of type {type(value)}, it should be an integer"
        self.data_numpy[pos[1], pos[0]] = value

    def is_set(self, p: Tuple[int, int]) -> bool:
        return self[p] != 0

    def is_empty(self, p: Tuple[int, int]) -> bool:
        return not self.is_set(p)

    def copy(self) -> "PixelMap":
        return PixelMap(self._proto, in_bits=self._in_bits)

    def flood_fill(self, start_point: Point2, pred: Callable[[int], bool]) -> Set[Point2]:
        nodes: Set[Point2] = set()
        queue: List[Point2] = [start_point]

        while queue:
            x, y = queue.pop()

            if not (0 <= x < self.width and 0 <= y < self.height):
                continue

            if Point2((x, y)) in nodes:
                continue

            if pred(self[x, y]):
                nodes.add(Point2((x, y)))
                queue += [Point2((x + a, y + b)) for a in [-1, 0, 1] for b in [-1, 0, 1] if not (a == 0 and b == 0)]
        return nodes

    def flood_fill_all(self, pred: Callable[[int], bool]) -> Set[FrozenSet[Point2]]:
        groups: Set[FrozenSet[Point2]] = set()

        for x in range(self.width):
            for y in range(self.height):
                if any((x, y) in g for g in groups):
                    continue

                if pred(self[x, y]):
                    groups.add(frozenset(self.flood_fill(Point2((x, y)), pred)))

        return groups

    def print(self, wide: bool = False) -> None:
        for y in range(self.height):
            for x in range(self.width):
                print("#" if self.is_set((x, y)) else " ", end=(" " if wide else ""))
            print("")

