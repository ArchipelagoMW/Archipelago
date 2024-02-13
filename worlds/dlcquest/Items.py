import csv
import enum
import math
from dataclasses import dataclass, field
from random import Random
from typing import Dict, List, Set

from BaseClasses import Item, ItemClassification
from . import Options, data


class DLCQuestItem(Item):
    game: str = "DLCQuest"
    coins: int = 0
    coin_suffix: str = ""


offset = 120_000


class Group(enum.Enum):
    DLC = enum.auto()
    DLCQuest = enum.auto()
    Freemium = enum.auto()
    Item = enum.auto()
    Coin = enum.auto()
    Trap = enum.auto()


@dataclass(frozen=True)
class ItemData:
    code_without_offset: offset
    name: str
    classification: ItemClassification
    groups: Set[Group] = field(default_factory=frozenset)

    def __post_init__(self):
        if not isinstance(self.groups, frozenset):
            super().__setattr__("groups", frozenset(self.groups))

    @property
    def code(self):
        return offset + self.code_without_offset if self.code_without_offset is not None else None

    def has_any_group(self, *group: Group) -> bool:
        groups = set(group)
        return bool(groups.intersection(self.groups))


def load_item_csv():
    try:
        from importlib.resources import files
    except ImportError:
        from importlib_resources import files  # noqa

    items = []
    with files(data).joinpath("items.csv").open() as file:
        item_reader = csv.DictReader(file)
        for item in item_reader:
            id = int(item["id"]) if item["id"] else None
            classification = ItemClassification[item["classification"]]
            groups = {Group[group] for group in item["groups"].split(",") if group}
            items.append(ItemData(id, item["name"], classification, groups))
    return items


all_items: List[ItemData] = load_item_csv()
item_table: Dict[str, ItemData] = {}
items_by_group: Dict[Group, List[ItemData]] = {}


def initialize_item_table():
    item_table.update({item.name: item for item in all_items})


def initialize_groups():
    for item in all_items:
        for group in item.groups:
            item_group = items_by_group.get(group, list())
            item_group.append(item)
            items_by_group[group] = item_group


initialize_item_table()
initialize_groups()


def create_trap_items(world, World_Options: Options.DLCQuestOptions, trap_needed: int, random: Random) -> List[Item]:
    traps = []
    for i in range(trap_needed):
        trap = random.choice(items_by_group[Group.Trap])
        traps.append(world.create_item(trap))

    return traps


def create_items(world, World_Options: Options.DLCQuestOptions, locations_count: int, random: Random):
    created_items = []
    if World_Options.campaign == Options.Campaign.option_basic or World_Options.campaign == Options.Campaign.option_both:
        for item in items_by_group[Group.DLCQuest]:
            if item.has_any_group(Group.DLC):
                created_items.append(world.create_item(item))
            if item.has_any_group(Group.Item) and World_Options.item_shuffle == Options.ItemShuffle.option_shuffled:
                created_items.append(world.create_item(item))
        if World_Options.coinsanity == Options.CoinSanity.option_coin:
            coin_bundle_needed = math.floor(825 / World_Options.coinbundlequantity)
            for item in items_by_group[Group.DLCQuest]:
                if item.has_any_group(Group.Coin):
                    for i in range(coin_bundle_needed):
                        created_items.append(world.create_item(item))
                    if 825 % World_Options.coinbundlequantity != 0:
                        created_items.append(world.create_item(item))

    if (World_Options.campaign == Options.Campaign.option_live_freemium_or_die or
            World_Options.campaign == Options.Campaign.option_both):
        for item in items_by_group[Group.Freemium]:
            if item.has_any_group(Group.DLC):
                created_items.append(world.create_item(item))
            if item.has_any_group(Group.Item) and World_Options.item_shuffle == Options.ItemShuffle.option_shuffled:
                created_items.append(world.create_item(item))
        if World_Options.coinsanity == Options.CoinSanity.option_coin:
            coin_bundle_needed = math.floor(889 / World_Options.coinbundlequantity)
            for item in items_by_group[Group.Freemium]:
                if item.has_any_group(Group.Coin):
                    for i in range(coin_bundle_needed):
                        created_items.append(world.create_item(item))
                    if 889 % World_Options.coinbundlequantity != 0:
                        created_items.append(world.create_item(item))

    trap_items = create_trap_items(world, World_Options, locations_count - len(created_items), random)
    created_items += trap_items

    return created_items
