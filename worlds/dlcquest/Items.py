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
    Twice = enum.auto()
    Piece = enum.auto()
    Deprecated = enum.auto()



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


def create_trap_items(world, world_options: Options.DLCQuestOptions, trap_needed: int, random: Random) -> List[Item]:
    traps = []
    for i in range(trap_needed):
        trap = random.choice(items_by_group[Group.Trap])
        traps.append(world.create_item(trap, ItemClassification.trap))

    return traps


def create_items(world, world_options: Options.DLCQuestOptions, locations_count: int, excluded_items: list[str], random: Random):
    created_items = []
    if world_options.campaign == Options.Campaign.option_basic or world_options.campaign == Options.Campaign.option_both:
        create_items_basic(world_options, created_items, world, excluded_items)

    if (world_options.campaign == Options.Campaign.option_live_freemium_or_die or
            world_options.campaign == Options.Campaign.option_both):
        create_items_lfod(world_options, created_items, world, excluded_items)

    trap_items = create_trap_items(world, world_options, locations_count - len(created_items), random)
    created_items += trap_items

    return created_items


def create_items_lfod(world_options, created_items, world, excluded_items):
    for item in items_by_group[Group.Freemium]:
        if item.name in excluded_items:
            excluded_items.remove(item)
            continue

        if item.has_any_group(Group.DLC):
            created_items.append(world.create_item(item))
        if item.has_any_group(Group.Item) and world_options.item_shuffle == Options.ItemShuffle.option_shuffled:
            created_items.append(world.create_item(item))
            if item.has_any_group(Group.Twice):
                created_items.append(world.create_item(item))
    if world_options.coinsanity == Options.CoinSanity.option_coin:
        if world_options.coinbundlequantity == -1:
            create_coin_piece(created_items, world, 889, 200, Group.Freemium)
            return
        create_coin(world_options, created_items, world, 889, 200, Group.Freemium)


def create_items_basic(world_options, created_items, world, excluded_items):
    for item in items_by_group[Group.DLCQuest]:
        if item.name in excluded_items:
            excluded_items.remove(item.name)
            continue

        if item.has_any_group(Group.DLC):
            created_items.append(world.create_item(item))
        if item.has_any_group(Group.Item) and world_options.item_shuffle == Options.ItemShuffle.option_shuffled:
            created_items.append(world.create_item(item))
            if item.has_any_group(Group.Twice):
                created_items.append(world.create_item(item))
    if world_options.coinsanity == Options.CoinSanity.option_coin:
        if world_options.coinbundlequantity == -1:
            create_coin_piece(created_items, world, 825, 250, Group.DLCQuest)
            return
        create_coin(world_options, created_items, world, 825, 250, Group.DLCQuest)


def create_coin(world_options, created_items, world, total_coins, required_coins, group):
    coin_bundle_required = math.ceil(required_coins / world_options.coinbundlequantity)
    coin_bundle_useful = math.ceil((total_coins - coin_bundle_required * world_options.coinbundlequantity) / world_options.coinbundlequantity)
    for item in items_by_group[group]:
        if item.has_any_group(Group.Coin):
            for i in range(coin_bundle_required):
                created_items.append(world.create_item(item))
            for i in range(coin_bundle_useful):
                created_items.append(world.create_item(item, ItemClassification.useful))


def create_coin_piece(created_items, world, total_coins, required_coins, group):
    for item in items_by_group[group]:
        if item.has_any_group(Group.Piece):
            for i in range(required_coins*10):
                created_items.append(world.create_item(item))
            for i in range((total_coins - required_coins) * 10):
                created_items.append(world.create_item(item, ItemClassification.useful))
