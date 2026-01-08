from typing import Iterable, Iterator, NamedTuple, Sequence, Union


class AreaDoor(NamedTuple):
    address: str
    data: str
    """ the data of the vanilla door that goes here """
    area_name: str
    name: str
    region: int

    @staticmethod
    def from_jsonable(a: Sequence[Union[str, int]]) -> "AreaDoor":
        ad, d, an, n, r = a
        assert isinstance(ad, str)
        assert isinstance(d, str)
        assert isinstance(an, str)
        assert isinstance(n, str)
        assert isinstance(r, int)
        return AreaDoor(ad, d, an, n, r)


class DoorPairs:
    _list: list[tuple[AreaDoor, AreaDoor]]
    _pairs: dict[AreaDoor, AreaDoor]

    def __init__(self, connections: Iterable[tuple[AreaDoor, AreaDoor]]) -> None:
        self._list = list(connections)
        self._pairs = {}
        for door_1, door_2 in connections:
            self._pairs[door_1] = door_2
            self._pairs[door_2] = door_1

    def __eq__(self, __value: object) -> bool:
        return (
            isinstance(__value, DoorPairs) and
            __value._list == self._list and
            __value._pairs == self._pairs
        )

    def other(self, door: AreaDoor) -> AreaDoor:
        return self._pairs[door]

    def connections(self) -> Iterator[tuple[AreaDoor, AreaDoor]]:
        yield from self._list

    def to_jsonable(self) -> Sequence[tuple[AreaDoor, AreaDoor]]:
        return self._list

    @staticmethod
    def from_jsonable(connections: Iterable[Sequence[Sequence[Union[str, int]]]]) -> "DoorPairs":
        return DoorPairs([
            (AreaDoor.from_jsonable(c[0]), AreaDoor.from_jsonable(c[1]))
            for c in connections
        ])
