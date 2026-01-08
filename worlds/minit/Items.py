from BaseClasses import Item, ItemClassification
from worlds.AutoWorld import World
from typing import NamedTuple, Callable


class MinitItem(Item):
    game = "Minit"


class MinitItemData(NamedTuple):
    offset: int = None
    classification: ItemClassification = ItemClassification.filler
    can_create: Callable[[World], bool] = lambda world: True

    @property
    def code(self):
        if self.offset is None:
            raise Exception(f"Invalid item code, offset = {self.offset}")
        return 60000 + self.offset


prog_skip = ItemClassification.progression_skip_balancing
prog = ItemClassification.progression
useful = ItemClassification.useful
filler = ItemClassification.filler


item_table: dict[str, MinitItemData] = {
    "Coin": MinitItemData(offset=0, classification=prog_skip),
    "HeartPiece": MinitItemData(
        offset=1, classification=useful,
        can_create=lambda world:
        not bool(world.options.min_hp)),
    "Tentacle": MinitItemData(offset=2, classification=prog),
    "ItemCoffee": MinitItemData(offset=3, classification=prog),
    "ItemFlashLight": MinitItemData(offset=4, classification=prog),
    "ItemSwim": MinitItemData(offset=5, classification=prog),
    "ItemKey": MinitItemData(offset=6, classification=prog),
    "ItemWateringCan": MinitItemData(offset=7, classification=prog),
    "ItemThrow": MinitItemData(offset=8, classification=prog),
    "ItemShoes": MinitItemData(offset=9, classification=prog),
    "ItemGlove": MinitItemData(offset=10, classification=prog),
    "ItemBoat": MinitItemData(offset=11, classification=prog),
    # could be granted again, will play with the idea
    "ItemCamera": MinitItemData(
        offset=12, classification=filler,
        can_create=lambda world: False),
    "ItemBasement": MinitItemData(offset=13, classification=prog),
    "ItemMegaSword": MinitItemData(
        offset=14, classification=prog,
        can_create=lambda world:
        world.options.progressive_sword == "off"),
    "ItemBrokenSword": MinitItemData(
        offset=15, classification=prog,
        can_create=lambda world:
        world.options.progressive_sword == "off"),
    "ItemTurboInk": MinitItemData(offset=16, classification=useful),
    "ItemGrinder": MinitItemData(offset=17, classification=prog),
    "ItemTrophy": MinitItemData(offset=18, classification=filler),
    "ItemPressPass": MinitItemData(offset=19, classification=prog),
    "ItemSword": MinitItemData(
        offset=20, classification=prog,
        can_create=lambda world:
        world.options.progressive_sword == "off"),
    "Progressive Sword": MinitItemData(
        offset=21, classification=prog,
        can_create=lambda world:
        world.options.progressive_sword == "forward_progressive"),
    "Reverse Progressive Sword": MinitItemData(
        offset=22, classification=prog,
        can_create=lambda world:
        world.options.progressive_sword == "reverse_progressive"),

    # "Boss dead": MinitItemData(classification=prog),
    # added manually in init
}

item_frequencies = {
    "Coin": 19,
    "HeartPiece": 6,
    "Tentacle": 8,
    "Progressive Sword": 3,
    "Reverse Progressive Sword": 3,
}


item_groups: dict[str, set[str]] = {
    "swords": {
        "ItemBrokenSword",
        "ItemSword",
        "ItemMegaSword",
        "Progressive Sword",
        "Reverse Progressive Sword",
        },
    "swim": {"ItemSwim"},
    "push": {"ItemCoffee"},
    "cut": {"ItemGlove"},
    "press pass": {"ItemPressPass"},
    "shoes": {"ItemShoes"},
    "watering can": {"ItemWateringCan"},
    "flashlight": {"ItemFlashLight"},
    "lighthouse key": {"ItemKey"},
    "basement key": {"ItemBasement"},
    "grinder": {"ItemGrinder"},
    "throw": {"ItemThrow"},
    "boatwood": {"ItemBoat"},
}
