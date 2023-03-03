import bisect
import csv
import enum
import itertools
import logging
import math
import typing
from collections import OrderedDict
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from random import Random
from typing import Dict, List, Protocol, Union, Set, Optional, FrozenSet

from BaseClasses import Item, ItemClassification
from . import options, data

ITEM_CODE_OFFSET = 717000

logger = logging.getLogger(__name__)
world_folder = Path(__file__).parent


class Group(enum.Enum):
    RESOURCE_PACK = enum.auto()
    FRIENDSHIP_PACK = enum.auto()
    COMMUNITY_REWARD = enum.auto()
    TRASH = enum.auto()
    MINES_FLOOR_10 = enum.auto()
    MINES_FLOOR_20 = enum.auto()
    MINES_FLOOR_50 = enum.auto()
    MINES_FLOOR_60 = enum.auto()
    MINES_FLOOR_80 = enum.auto()
    MINES_FLOOR_90 = enum.auto()
    MINES_FLOOR_110 = enum.auto()
    FOOTWEAR = enum.auto()
    HATS = enum.auto()
    RING = enum.auto()
    WEAPON = enum.auto()
    PROGRESSIVE_TOOLS = enum.auto()
    SKILL_LEVEL_UP = enum.auto()
    ARCADE_MACHINE_BUFFS = enum.auto()
    GALAXY_WEAPONS = enum.auto()
    BASE_RESOURCE = enum.auto()
    WARP_TOTEM = enum.auto()
    GEODE = enum.auto()
    ORE = enum.auto()
    FERTILIZER = enum.auto()
    SEED = enum.auto()
    FISHING_RESOURCE = enum.auto()


@dataclass(frozen=True)
class ItemData:
    code_without_offset: Optional[int]
    name: str
    classification: ItemClassification
    groups: Set[Group] = field(default_factory=frozenset)

    def __post_init__(self):
        if not isinstance(self.groups, frozenset):
            super().__setattr__("groups", frozenset(self.groups))

    @property
    def code(self):
        return ITEM_CODE_OFFSET + self.code_without_offset if self.code_without_offset is not None else None

    def has_any_group(self, *group: Group) -> bool:
        groups = set(group)
        return bool(groups.intersection(self.groups))


@dataclass(frozen=True)
class ResourcePackData:
    name: str
    default_amount: int = 1
    scaling_factor: int = 1
    classification: ItemClassification = ItemClassification.filler
    groups: FrozenSet[Group] = frozenset()

    def as_item_data(self, counter: itertools.count) -> [ItemData]:
        return [ItemData(next(counter), self.create_item_name(quantity), self.classification,
                         {Group.RESOURCE_PACK} | self.groups)
                for quantity in self.scale_quantity.values()]

    def create_item_name(self, quantity: int) -> str:
        return f"Resource Pack: {quantity} {self.name}"

    @cached_property
    def scale_quantity(self) -> typing.OrderedDict[int, int]:
        """Discrete scaling of the resource pack quantities.
        100 is default, 200 is double, 50 is half (if the scaling_factor allows it).
        """
        levels = math.ceil(self.default_amount / self.scaling_factor) * 2
        first_level = self.default_amount % self.scaling_factor
        if first_level == 0:
            first_level = self.scaling_factor
        quantities = sorted(set(range(first_level, self.scaling_factor * levels, self.scaling_factor))
                            | {self.default_amount * 2})

        return OrderedDict({round(quantity / self.default_amount * 100): quantity
                            for quantity in quantities
                            if quantity <= self.default_amount * 2})

    def calculate_quantity(self, multiplier: int) -> int:
        scales = list(self.scale_quantity)
        left_scale = bisect.bisect_left(scales, multiplier)
        closest_scale = min([scales[left_scale], scales[left_scale - 1]],
                            key=lambda x: abs(multiplier - x))
        return self.scale_quantity[closest_scale]

    def create_name_from_multiplier(self, multiplier: int) -> str:
        return self.create_item_name(self.calculate_quantity(multiplier))


class FriendshipPackData(ResourcePackData):
    def create_item_name(self, quantity: int) -> str:
        return f"Friendship Bonus ({quantity} <3)"

    def as_item_data(self, counter: itertools.count) -> [ItemData]:
        item_datas = super().as_item_data(counter)
        return [ItemData(item.code_without_offset, item.name, item.classification, {Group.FRIENDSHIP_PACK})
                for item in item_datas]


class StardewItemFactory(Protocol):
    def __call__(self, name: Union[str, ItemData]) -> Item:
        raise NotImplementedError


def load_item_csv():
    try:
        from importlib.resources import files
    except ImportError:
        from importlib_resources import files

    items = []
    with files(data).joinpath("items.csv").open() as file:
        item_reader = csv.DictReader(file)
        for item in item_reader:
            id = int(item["id"]) if item["id"] else None
            classification = ItemClassification[item["classification"]]
            groups = {Group[group] for group in item["groups"].split(",") if group}
            items.append(ItemData(id, item["name"], classification, groups))
    return items


def load_resource_pack_csv() -> List[ResourcePackData]:
    try:
        from importlib.resources import files
    except ImportError:
        from importlib_resources import files

    resource_packs = []
    with files(data).joinpath("resource_packs.csv").open() as file:
        resource_pack_reader = csv.DictReader(file)
        for resource_pack in resource_pack_reader:
            groups = frozenset(Group[group] for group in resource_pack["groups"].split(",") if group)
            resource_packs.append(ResourcePackData(resource_pack["name"],
                                                   int(resource_pack["default_amount"]),
                                                   int(resource_pack["scaling_factor"]),
                                                   ItemClassification[resource_pack["classification"]],
                                                   groups))
    return resource_packs


events = [
    ItemData(None, "Victory", ItemClassification.progression),
    ItemData(None, "Spring", ItemClassification.progression),
    ItemData(None, "Summer", ItemClassification.progression),
    ItemData(None, "Fall", ItemClassification.progression),
    ItemData(None, "Winter", ItemClassification.progression),
    ItemData(None, "Year Two", ItemClassification.progression),
]

all_items: List[ItemData] = load_item_csv() + events
item_table: Dict[str, ItemData] = {}
items_by_group: Dict[Group, List[ItemData]] = {}


def initialize_groups():
    for item in all_items:
        for group in item.groups:
            item_group = items_by_group.get(group, list())
            item_group.append(item)
            items_by_group[group] = item_group


def initialize_item_table():
    item_table.update({item.name: item for item in all_items})


friendship_pack = FriendshipPackData("Friendship Bonus", default_amount=2, classification=ItemClassification.useful)
all_resource_packs = load_resource_pack_csv()

initialize_item_table()
initialize_groups()


def create_items(item_factory: StardewItemFactory, locations_count: int, world_options: options.StardewOptions,
                 random: Random) \
        -> List[Item]:
    items = create_unique_items(item_factory, world_options, random)
    assert len(items) <= locations_count, \
        "There should be at least as many locations as there are mandatory items"
    logger.debug(f"Created {len(items)} unique items")

    resource_pack_items = fill_with_resource_packs(item_factory, world_options, random, locations_count - len(items))
    items += resource_pack_items
    logger.debug(f"Created {len(resource_pack_items)} resource packs")

    return items


def create_backpack_items(item_factory: StardewItemFactory, world_options: options.StardewOptions, items: List[Item]):
    if (world_options[options.BackpackProgression] == options.BackpackProgression.option_progressive or
            world_options[options.BackpackProgression] == options.BackpackProgression.option_early_progressive):
        items.extend(item_factory(item) for item in ["Progressive Backpack"] * 2)


def create_mine_rewards(item_factory: StardewItemFactory, items: List[Item], random: Random):
    items.append(item_factory("Rusty Sword"))
    items.append(item_factory(random.choice(items_by_group[Group.MINES_FLOOR_10])))
    items.append(item_factory(random.choice(items_by_group[Group.MINES_FLOOR_20])))
    items.append(item_factory("Slingshot"))
    items.append(item_factory(random.choice(items_by_group[Group.MINES_FLOOR_50])))
    items.append(item_factory(random.choice(items_by_group[Group.MINES_FLOOR_60])))
    items.append(item_factory("Master Slingshot"))
    items.append(item_factory(random.choice(items_by_group[Group.MINES_FLOOR_80])))
    items.append(item_factory(random.choice(items_by_group[Group.MINES_FLOOR_90])))
    items.append(item_factory(random.choice(items_by_group[Group.MINES_FLOOR_110])))
    items.append(item_factory("Skull Key"))


def create_mine_elevators(item_factory: StardewItemFactory, world_options: options.StardewOptions, items: List[Item]):
    if (world_options[options.TheMinesElevatorsProgression] ==
            options.TheMinesElevatorsProgression.option_progressive or
            world_options[options.TheMinesElevatorsProgression] ==
            options.TheMinesElevatorsProgression.option_progressive_from_previous_floor):
        items.extend([item_factory(item) for item in ["Progressive Mine Elevator"] * 24])


def create_tools(item_factory: StardewItemFactory, world_options: options.StardewOptions, items: List[Item]):
    if world_options[options.ToolProgression] == options.ToolProgression.option_progressive:
        items.extend(item_factory(item) for item in items_by_group[Group.PROGRESSIVE_TOOLS] * 4)
    items.append(item_factory("Golden Scythe"))


def create_skills(item_factory: StardewItemFactory, world_options: options.StardewOptions, items: List[Item]):
    if world_options[options.SkillProgression] == options.SkillProgression.option_progressive:
        items.extend([item_factory(item) for item in items_by_group[Group.SKILL_LEVEL_UP] * 10])


def create_wizard_buildings(item_factory: StardewItemFactory, items: List[Item]):
    items.append(item_factory("Earth Obelisk"))
    items.append(item_factory("Water Obelisk"))
    items.append(item_factory("Desert Obelisk"))
    items.append(item_factory("Island Obelisk"))
    items.append(item_factory("Junimo Hut"))
    items.append(item_factory("Gold Clock"))


def create_carpenter_buildings(item_factory: StardewItemFactory, world_options: options.StardewOptions,
                               items: List[Item]):
    if world_options[options.BuildingProgression] in {options.BuildingProgression.option_progressive,
                                                      options.BuildingProgression.option_progressive_early_shipping_bin}:
        items.append(item_factory("Progressive Coop"))
        items.append(item_factory("Progressive Coop"))
        items.append(item_factory("Progressive Coop"))
        items.append(item_factory("Progressive Barn"))
        items.append(item_factory("Progressive Barn"))
        items.append(item_factory("Progressive Barn"))
        items.append(item_factory("Well"))
        items.append(item_factory("Silo"))
        items.append(item_factory("Mill"))
        items.append(item_factory("Progressive Shed"))
        items.append(item_factory("Progressive Shed"))
        items.append(item_factory("Fish Pond"))
        items.append(item_factory("Stable"))
        items.append(item_factory("Slime Hutch"))
        items.append(item_factory("Shipping Bin"))
        items.append(item_factory("Progressive House"))
        items.append(item_factory("Progressive House"))
        items.append(item_factory("Progressive House"))


def create_special_quest_rewards(item_factory: StardewItemFactory, items: List[Item]):
    items.append(item_factory("Adventurer's Guild"))
    items.append(item_factory("Club Card"))
    items.append(item_factory("Magnifying Glass"))
    items.append(item_factory("Bear's Knowledge"))
    items.append(item_factory("Iridium Snake Milk"))


def create_stardrops(item_factory: StardewItemFactory, items: List[Item]):
    items.append(item_factory("Stardrop"))  # The Mines level 100
    items.append(item_factory("Stardrop"))  # Old Master Cannoli


def create_arcade_machine_items(item_factory: StardewItemFactory, world_options: options.StardewOptions,
                                items: List[Item]):
    if world_options[options.ArcadeMachineLocations] == options.ArcadeMachineLocations.option_full_shuffling:
        items.append(item_factory("JotPK: Progressive Boots"))
        items.append(item_factory("JotPK: Progressive Boots"))
        items.append(item_factory("JotPK: Progressive Gun"))
        items.append(item_factory("JotPK: Progressive Gun"))
        items.append(item_factory("JotPK: Progressive Gun"))
        items.append(item_factory("JotPK: Progressive Gun"))
        items.append(item_factory("JotPK: Progressive Ammo"))
        items.append(item_factory("JotPK: Progressive Ammo"))
        items.append(item_factory("JotPK: Progressive Ammo"))
        items.append(item_factory("JotPK: Extra Life"))
        items.append(item_factory("JotPK: Extra Life"))
        items.append(item_factory("JotPK: Increased Drop Rate"))
        items.extend(item_factory(item) for item in ["Junimo Kart: Extra Life"] * 8)


def create_player_buffs(item_factory: StardewItemFactory, world_options: options.StardewOptions, items: List[Item]):
    number_of_buffs: int = world_options[options.NumberOfPlayerBuffs]
    items.extend(item_factory(item) for item in ["Movement Speed Bonus"] * number_of_buffs)
    items.extend(item_factory(item) for item in ["Luck Bonus"] * number_of_buffs)


def create_traveling_merchant_items(item_factory: StardewItemFactory, items: List[Item]):
    items.append(item_factory("Traveling Merchant: Sunday"))
    items.append(item_factory("Traveling Merchant: Monday"))
    items.append(item_factory("Traveling Merchant: Tuesday"))
    items.append(item_factory("Traveling Merchant: Wednesday"))
    items.append(item_factory("Traveling Merchant: Thursday"))
    items.append(item_factory("Traveling Merchant: Friday"))
    items.append(item_factory("Traveling Merchant: Saturday"))
    items.extend(item_factory(item) for item in ["Traveling Merchant Stock Size"] * 6)
    items.extend(item_factory(item) for item in ["Traveling Merchant Discount"] * 8)


def create_unique_items(item_factory: StardewItemFactory, world_options: options.StardewOptions, random: Random) -> \
        List[Item]:
    items = []

    items.extend(item_factory(item) for item in items_by_group[Group.COMMUNITY_REWARD])

    create_backpack_items(item_factory, world_options, items)
    create_mine_rewards(item_factory, items, random)
    create_mine_elevators(item_factory, world_options, items)
    create_tools(item_factory, world_options, items)
    create_skills(item_factory, world_options, items)
    create_wizard_buildings(item_factory, items)
    create_carpenter_buildings(item_factory, world_options, items)
    items.append(item_factory("Beach Bridge"))
    create_special_quest_rewards(item_factory, items)
    create_stardrops(item_factory, items)
    create_arcade_machine_items(item_factory, world_options, items)
    items.append(item_factory(random.choice(items_by_group[Group.GALAXY_WEAPONS])))
    items.append(
        item_factory(friendship_pack.create_name_from_multiplier(world_options[options.ResourcePackMultiplier])))
    create_player_buffs(item_factory, world_options, items)
    create_traveling_merchant_items(item_factory, items)
    items.append(item_factory("Return Scepter"))

    return items


def fill_with_resource_packs(item_factory: StardewItemFactory, world_options: options.StardewOptions, random: Random,
                             required_resource_pack: int) -> List[Item]:
    resource_pack_multiplier = world_options[options.ResourcePackMultiplier]

    if resource_pack_multiplier == 0:
        return [item_factory(cola) for cola in ["Joja Cola"] * required_resource_pack]

    items = []

    for i in range(required_resource_pack):
        resource_pack = random.choice(all_resource_packs)
        items.append(item_factory(resource_pack.create_name_from_multiplier(resource_pack_multiplier)))

    return items
