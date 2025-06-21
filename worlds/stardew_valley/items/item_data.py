from __future__ import annotations

import csv
import enum
from dataclasses import dataclass, field
from functools import reduce
from typing import Protocol

from BaseClasses import ItemClassification, Item
from .. import data
from ..content.vanilla.ginger_island import ginger_island_content_pack
from ..logic.logic_event import all_events

ITEM_CODE_OFFSET = 717000


class StardewItemFactory(Protocol):
    def __call__(self, item: str | ItemData, /, *, classification_pre_fill: ItemClassification = None,
                 classification_post_fill: ItemClassification = None) -> Item:
        """
        :param item: The item to create. Can be the name of the item or the item data.
        :param classification_pre_fill: The classification to use for the item before the fill. If None, the basic classification of the item is used.
        :param classification_post_fill: The classification to use for the item after the fill. If None, the pre_fill classification will be used.
        """
        raise NotImplementedError


class Group(enum.Enum):
    RESOURCE_PACK = enum.auto()
    FRIENDSHIP_PACK = enum.auto()
    COMMUNITY_REWARD = enum.auto()
    TRASH_BEAR = enum.auto()
    TRASH = enum.auto()
    FOOTWEAR = enum.auto()
    HAT = enum.auto()
    RING = enum.auto()
    WEAPON = enum.auto()
    WEAPON_GENERIC = enum.auto()
    WEAPON_SWORD = enum.auto()
    WEAPON_CLUB = enum.auto()
    WEAPON_DAGGER = enum.auto()
    WEAPON_SLINGSHOT = enum.auto()
    PROGRESSIVE_TOOLS = enum.auto()
    SKILL_LEVEL_UP = enum.auto()
    SKILL_MASTERY = enum.auto()
    BUILDING = enum.auto()
    WIZARD_BUILDING = enum.auto()
    DESERT_TRANSPORTATION = enum.auto()
    ISLAND_TRANSPORTATION = enum.auto()
    ARCADE_MACHINE_BUFFS = enum.auto()
    BASE_RESOURCE = enum.auto()
    WARP_TOTEM = enum.auto()
    GEODE = enum.auto()
    ORE = enum.auto()
    FERTILIZER = enum.auto()
    SEED = enum.auto()
    CROPSANITY = enum.auto()
    FISHING_RESOURCE = enum.auto()
    SEASON = enum.auto()
    TRAVELING_MERCHANT_DAY = enum.auto()
    MUSEUM = enum.auto()
    FRIENDSANITY = enum.auto()
    FESTIVAL = enum.auto()
    RARECROW = enum.auto()
    TRAP = enum.auto()
    BONUS = enum.auto()
    MAXIMUM_ONE = enum.auto()
    AT_LEAST_TWO = enum.auto()
    DEPRECATED = enum.auto()
    RESOURCE_PACK_USEFUL = enum.auto()
    SPECIAL_ORDER_BOARD = enum.auto()
    SPECIAL_ORDER_QI = enum.auto()
    BABY = enum.auto()
    GINGER_ISLAND = enum.auto()
    WALNUT_PURCHASE = enum.auto()
    TV_CHANNEL = enum.auto()
    QI_CRAFTING_RECIPE = enum.auto()
    CHEFSANITY = enum.auto()
    CHEFSANITY_STARTER = enum.auto()
    CHEFSANITY_QOS = enum.auto()
    CHEFSANITY_PURCHASE = enum.auto()
    CHEFSANITY_FRIENDSHIP = enum.auto()
    CHEFSANITY_SKILL = enum.auto()
    CRAFTSANITY = enum.auto()
    BOOK_POWER = enum.auto()
    LOST_BOOK = enum.auto()
    PLAYER_BUFF = enum.auto()
    EASY_SECRET = enum.auto()
    FISHING_SECRET = enum.auto()
    SECRET_NOTES_SECRET = enum.auto()
    MOVIESANITY = enum.auto()
    TRINKET = enum.auto()
    EATSANITY_ENZYME = enum.auto()
    ENDGAME_LOCATION_ITEMS = enum.auto()
    REQUIRES_FRIENDSANITY_MARRIAGE = enum.auto()
    # Mods
    MAGIC_SPELL = enum.auto()
    MOD_WARP = enum.auto()


@dataclass(frozen=True)
class ItemData:
    code_without_offset: int | None
    name: str
    classification: ItemClassification
    content_packs: frozenset[str] = frozenset()
    """All the content packs required for this item to be available."""
    groups: set[Group] = field(default_factory=frozenset)

    def __post_init__(self):
        if not isinstance(self.groups, frozenset):
            super().__setattr__("groups", frozenset(self.groups))

    @property
    def code(self) -> int | None:
        return ITEM_CODE_OFFSET + self.code_without_offset if self.code_without_offset is not None else None

    def has_any_group(self, *group: Group) -> bool:
        groups = set(group)
        return bool(groups.intersection(self.groups))

    def has_all_groups(self, *group: Group) -> bool:
        groups = set(group)
        return bool(groups.issubset(self.groups))

    def has_limited_amount(self) -> bool:
        return self.has_any_group(Group.MAXIMUM_ONE, Group.AT_LEAST_TWO)


def load_item_csv():
    from importlib.resources import files

    items = []
    with files(data).joinpath("items.csv").open() as file:
        item_reader = csv.DictReader(file)
        for item in item_reader:
            item_id = int(item["id"]) if item["id"] else None
            classification = reduce((lambda a, b: a | b), {ItemClassification[str_classification] for str_classification in item["classification"].split(",")})
            groups = {Group[group] for group in item["groups"].split(",") if group}

            content_packs = frozenset(cp for cp in item["content_packs"].split(",") if cp)
            if Group.GINGER_ISLAND in groups:
                content_packs |= {ginger_island_content_pack.name}

            items.append(ItemData(item_id, item["name"], classification, content_packs, groups))
    return items


events = [
    ItemData(None, e, ItemClassification.progression)
    for e in sorted(all_events)
]

all_items: list[ItemData] = load_item_csv() + events
item_table: dict[str, ItemData] = {}
items_by_group: dict[Group, list[ItemData]] = {}


def initialize_groups():
    for item in all_items:
        for group in item.groups:
            item_group = items_by_group.get(group, list())
            item_group.append(item)
            items_by_group[group] = item_group


def initialize_item_table():
    item_table.update({item.name: item for item in all_items})


initialize_item_table()
initialize_groups()
