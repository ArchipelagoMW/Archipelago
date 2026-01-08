from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional

from BaseClasses import ItemClassification
from .Regions import RegionEnum, Street, Apartment, Beach, Bedroom, Cell, Cliffs, Circus, Crowd, Fields, Forest, Go, \
    Hotel, Overworld, Red_Cave, Red_Sea, Suburb, Space, Terminal, Windmill, Blue, Happy

item_types: list[type['ItemEnum']] = []


@dataclass
class ItemData:
    full_name: str
    item_id: int
    map: Optional[type[RegionEnum]]
    classification: ItemClassification


class ItemEnum(int, Enum):
    __items: dict[Optional[type[RegionEnum]], ItemData]

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name.replace('_', ' '), count

    def __init_subclass__(cls):
        item_types.append(cls)

    def __new__(cls, name, local_id):
        obj = int.__new__(cls, local_id)
        obj._value_ = local_id
        return obj

    def __init__(self, name, local_id):
        self.__items = {
            map_t: ItemData(self._format_name(name, map_t),
                            10 ** 9 + 10 ** 6 * len(item_types) + 10 ** 3 * (
                                map_t.area_id() if map_t is not None else 0)
                            + local_id, map_t, self._classification())
            for map_t in self._maps()
        }

    def __repr__(self):
        return f"<{self.__class__.__name__}.{self.name}: {self.__items}>"

    def __getitem__(self, item: type[RegionEnum]):
        return self.__items[item]

    def __len__(self):
        return len(self.__items)

    def __iter__(self):
        return (i for i in self.__items.values())

    @classmethod
    def all(cls):
        return [item for val in cls for item in val]

    @classmethod
    def names(cls):
        return [item.full_name for item in cls.all()]

    @staticmethod
    def _classification():
        return ItemClassification.progression

    @property
    def item(self):
        return self.__items[None]

    @staticmethod
    def _maps() -> list[Optional[type[RegionEnum]]]:
        return [None]

    @staticmethod
    def _format_name(name: str, map_t: Optional[type[RegionEnum]]):
        return name


class Inventory(ItemEnum):
    Broom = auto()
    Widen = auto()
    Extend = auto()
    Jump_Shoes = auto()
    Swap = auto()
    Progressive_Swap = auto()


class Cicada(ItemEnum):
    @staticmethod
    def _classification():
        return ItemClassification.useful

    Health_Cicada = auto()


class Card(ItemEnum):
    @staticmethod
    def _format_name(name: str, map_t: Optional[type[RegionEnum]]):
        return f"Card ({name})"

    @staticmethod
    def _classification():
        return ItemClassification.progression_deprioritized

    Edward = auto()
    Annoyer = auto()
    Seer = auto()
    Shieldy = auto()
    Slime = auto()
    PewLaser = auto()
    Suburbian = auto()
    Watcher = auto()
    Silverfish = auto()
    Gas_Guy = auto()
    Mitra = auto()
    Miao = auto()
    Windmill = auto()
    Mushroom = auto()
    Dog = auto()
    Rock = auto()
    Fisherman = auto()
    Walker = auto()
    Mover = auto()
    Slasher = auto()
    Rogue = auto()
    Chaser = auto()
    Fire_Pillar = auto()
    Contorts = auto()
    Lion = auto()
    Arthur_and_Javiera = auto()
    Frog = auto()
    Person = auto()
    Wall = auto()
    Blue_Cube_King = auto()
    Orange_Cube_King = auto()
    Dust_Maid = auto()
    Dasher = auto()
    Burst_Plant = auto()
    Manager = auto()
    Sage = auto()
    Young = auto()
    Carved_Rock = auto()
    City_Man = auto()
    Intra = auto()
    Torch = auto()
    Triangle_NPC = auto()
    Killer = auto()
    Goldman = auto()
    Broom = auto()
    Rank = auto()
    Follower = auto()
    Rock_Creature = auto()
    Null = auto()


postgame_cards = [card.item for card in [
    Card.Young,
    Card.Carved_Rock,
    Card.City_Man,
    Card.Intra,
    Card.Torch,
    Card.Triangle_NPC,
    Card.Killer,
    Card.Broom,
    Card.Rank,
    Card.Follower,
    Card.Rock_Creature,
    Card.Null
]]


class Secret(ItemEnum):
    @staticmethod
    def _classification():
        return ItemClassification.filler

    Golden_Poop = auto()
    Spam_Can = auto()
    Glitch = auto()
    Heart = auto()
    Electric_Monster = auto()
    Cat_Statue = auto()
    Melos = auto()
    Marina = auto()
    Black_Cube = auto()
    Red_Cube = auto()
    Green_Cube = auto()
    Blue_Cube = auto()
    White_Cube = auto()
    Golden_Broom = auto()


early_secret_items = [
    Secret.Golden_Poop.item,
    Secret.Heart.item
]

secret_items_secret_paths = [
    Secret.Glitch.item,
    Secret.Spam_Can.item,
    Secret.Electric_Monster.item
]


class Keys(ItemEnum):
    @staticmethod
    def _maps() -> list[Optional[type[RegionEnum]]]:
        return [Street, Bedroom, Red_Cave, Crowd, Hotel, Apartment, Circus]

    @staticmethod
    def _format_name(name: str, map_t: Optional[type[RegionEnum]]):
        return f"{name} ({map_t.area_name()})"

    Small_Key = auto()
    Key_Ring = auto()


class BigKey(ItemEnum):
    @staticmethod
    def _format_name(name: str, map_t: Optional[type[RegionEnum]]):
        return name.title() + " Key"

    GREEN = auto()
    RED = auto()
    BLUE = auto()


class StatueUnlocks(ItemEnum):
    @staticmethod
    def _format_name(name: str, region: Optional[type[RegionEnum]]):
        return f"{region.area_name()} Statue"

    @staticmethod
    def _maps() -> list[Optional[type[RegionEnum]]]:
        return [Red_Cave, Bedroom, Crowd]

    STATUE = auto()


class Heal(ItemEnum):
    @staticmethod
    def _classification():
        return ItemClassification.filler

    Heal = auto()
    Big_Heal = auto()


class Nexus(ItemEnum):
    @staticmethod
    def _maps() -> list[Optional[type[RegionEnum]]]:
        return [Apartment, Beach, Bedroom, Blue, Cell, Cliffs, Circus, Crowd, Fields, Forest, Go,
                Happy, Hotel, Overworld, Red_Cave, Red_Sea, Suburb, Space, Terminal, Windmill]

    @staticmethod
    def _format_name(name: str, map_t: Optional[type[RegionEnum]]):
        return f"Nexus Gate ({map_t.area_name()})"

    GATE = auto()


class Trap(ItemEnum):
    @staticmethod
    def _format_name(name: str, map_t: Optional[type[RegionEnum]]):
        return name + " Trap"

    @staticmethod
    def _classification():
        return ItemClassification.trap

    Person = auto()
    Gas = auto()


class RedCaveUnlock(ItemEnum):
    @staticmethod
    def _maps() -> list[Optional[type[RegionEnum]]]:
        return [Red_Cave]

    @staticmethod
    def _format_name(name: str, map_t: Optional[type[RegionEnum]]):
        return "Progressive " + map_t.area_name()

    RED_CAVE = auto()


class Dam(ItemEnum):
    @staticmethod
    def _maps() -> list[Optional[type[RegionEnum]]]:
        return [Blue, Happy]

    @staticmethod
    def _format_name(name: str, map_t: Optional[type[RegionEnum]]):
        return f"{map_t.area_name()} Dam"

    DAM = auto()


class TradingQuest(ItemEnum):
    Miao = auto()
    Cardboard_Box = auto()
    Biking_Shoes = auto()


all_items = {item.full_name: item for item_enum in item_types for item in item_enum.all()}

brooms = [
    Inventory.Broom.item,
    Inventory.Extend.item,
    Inventory.Widen.item
]

item_groups = {
    "Cards": Card.names(),
    "Nexus Gates": Nexus.names(),
    "Keys": [item.full_name for item in Keys.Small_Key],
    "Key Rings": [item.full_name for item in Keys.Key_Ring],
    "Statues": StatueUnlocks.names(),
    "Brooms": [broom.full_name for broom in brooms],
    "Dams": Dam.names()
}
