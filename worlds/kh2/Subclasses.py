import typing

from BaseClasses import Location, Item


class KH2Location(Location):
    game: str = "Kingdom Hearts 2"


class LocationData(typing.NamedTuple):
    locid: int
    yml: str
    charName: str = "Sora"
    charNumber: int = 1


class KH2Item(Item):
    game: str = "Kingdom Hearts 2"


class ItemData(typing.NamedTuple):
    quantity: int = 0
    kh2id: int = 0
    # Save+ mem addr
    memaddr: int = 0
    # some items have bitmasks. if bitmask>0 bitor to give item else
    bitmask: int = 0
    # if ability then
    ability: bool = False
