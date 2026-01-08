from typing import Any, NoReturn

from .item_data import Item


class Trick:
    """ items: all the items needed to do this trick """
    desc: str
    items: tuple[Item, ...]
    __slots__ = ("desc", "items")

    def __init__(self, desc: str, *items: Item) -> None:
        self.desc = desc
        self.items = items

    def __hash__(self) -> int:
        return hash(id(self))

    def __eq__(self, __o: object) -> bool:
        return __o is self

    def __copy__(self) -> "Trick":
        return self

    def __deepcopy__(self, memo: dict[Any, Any]) -> "Trick":
        # singletons
        return self

    def __bool__(self) -> NoReturn:
        # TODO: unit test for this like the one for logic shortcut
        raise TypeError("cannot interpret Trick as bool - did you forget `in loadout`?")
