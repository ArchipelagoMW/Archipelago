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
from .data.villagers_data import all_villagers
from .options import StardewOptions

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
    SEED_SHUFFLE = enum.auto()
    FISHING_RESOURCE = enum.auto()
    SEASON = enum.auto()
    TRAVELING_MERCHANT_DAY = enum.auto()
    MUSEUM = enum.auto()
    FRIENDSANITY = enum.auto()
    FESTIVAL = enum.auto()
    RARECROW = enum.auto()
    TRAP = enum.auto()
    MAXIMUM_ONE = enum.auto()
    EXACTLY_TWO = enum.auto
    DEPRECATED = enum.auto()
    RESOURCE_PACK_USEFUL = enum.auto()
    SPECIAL_ORDER_BOARD = enum.auto()
    SPECIAL_ORDER_QI = enum.auto()
    GINGER_ISLAND = enum.auto()


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


class StardewItemFactory(Protocol):
    def __call__(self, name: Union[str, ItemData]) -> Item:
        raise NotImplementedError


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


events = [
    ItemData(None, "Victory", ItemClassification.progression),
    ItemData(None, "Month End", ItemClassification.progression),
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


initialize_item_table()
initialize_groups()


def create_items(item_factory: StardewItemFactory, locations_count: int, items_to_exclude: List[Item],
                 world_options: StardewOptions,
                 random: Random) -> List[Item]:
    items = create_unique_items(item_factory, world_options, random)

    for item in items_to_exclude:
        if item in items:
            items.remove(item)

    assert len(items) <= locations_count, \
        "There should be at least as many locations as there are mandatory items"
    logger.debug(f"Created {len(items)} unique items")

    unique_filler_items = create_unique_filler_items(item_factory, world_options, random, locations_count - len(items))
    items += unique_filler_items
    logger.debug(f"Created {len(unique_filler_items)} unique filler items")

    resource_pack_items = fill_with_resource_packs(item_factory, world_options, random, items, locations_count)
    items += resource_pack_items
    logger.debug(f"Created {len(resource_pack_items)} resource packs")

    return items


def create_unique_items(item_factory: StardewItemFactory, world_options: StardewOptions, random: Random) -> List[Item]:
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
    create_museum_items(item_factory, world_options, items)
    create_arcade_machine_items(item_factory, world_options, items)
    items.append(item_factory(random.choice(items_by_group[Group.GALAXY_WEAPONS])))
    items.append(item_factory("Friendship Bonus (2 <3)"))
    create_player_buffs(item_factory, world_options, items)
    items.extend(create_traveling_merchant_items(item_factory))
    items.append(item_factory("Return Scepter"))
    items.extend(create_seasons(item_factory, world_options))
    items.extend(create_seeds(item_factory, world_options))
    create_friendsanity_items(item_factory, world_options, items)
    items.extend(create_festival_rewards(item_factory, world_options))

    return items


def create_backpack_items(item_factory: StardewItemFactory, world_options: StardewOptions, items: List[Item]):
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


def create_mine_elevators(item_factory: StardewItemFactory, world_options: StardewOptions, items: List[Item]):
    if (world_options[options.TheMinesElevatorsProgression] ==
            options.TheMinesElevatorsProgression.option_progressive or
            world_options[options.TheMinesElevatorsProgression] ==
            options.TheMinesElevatorsProgression.option_progressive_from_previous_floor):
        items.extend([item_factory(item) for item in ["Progressive Mine Elevator"] * 24])


def create_tools(item_factory: StardewItemFactory, world_options: StardewOptions, items: List[Item]):
    if world_options[options.ToolProgression] == options.ToolProgression.option_progressive:
        items.extend(item_factory(item) for item in items_by_group[Group.PROGRESSIVE_TOOLS] * 4)
    items.append(item_factory("Golden Scythe"))


def create_skills(item_factory: StardewItemFactory, world_options: StardewOptions, items: List[Item]):
    if world_options[options.SkillProgression] == options.SkillProgression.option_progressive:
        items.extend([item_factory(item) for item in items_by_group[Group.SKILL_LEVEL_UP] * 10])


def create_wizard_buildings(item_factory: StardewItemFactory, items: List[Item]):
    items.append(item_factory("Earth Obelisk"))
    items.append(item_factory("Water Obelisk"))
    items.append(item_factory("Desert Obelisk"))
    items.append(item_factory("Island Obelisk"))
    items.append(item_factory("Junimo Hut"))
    items.append(item_factory("Gold Clock"))


def create_carpenter_buildings(item_factory: StardewItemFactory, world_options: StardewOptions,
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


def create_museum_items(item_factory: StardewItemFactory, world_options: StardewOptions, items: List[Item]):
    if world_options[options.Museumsanity] == options.Museumsanity.option_none:
        return
    items.extend(item_factory(item) for item in ["Magic Rock Candy"] * 5)
    items.extend(item_factory(item) for item in ["Ancient Seeds"] * 5)
    items.extend(item_factory(item) for item in ["Traveling Merchant Metal Detector"] * 4)
    items.append(item_factory("Ancient Seeds Recipe"))
    items.append(item_factory("Stardrop"))
    items.append(item_factory("Rusty Key"))
    items.append(item_factory("Dwarvish Translation Guide"))


def create_friendsanity_items(item_factory: StardewItemFactory, world_options: StardewOptions, items: List[Item]):
    if world_options[options.Friendsanity] == options.Friendsanity.option_none:
        return
    exclude_non_bachelors = world_options[options.Friendsanity] == options.Friendsanity.option_bachelors
    exclude_locked_villagers = world_options[options.Friendsanity] == options.Friendsanity.option_starting_npcs or \
                               world_options[options.Friendsanity] == options.Friendsanity.option_bachelors
    exclude_post_marriage_hearts = world_options[options.Friendsanity] != options.Friendsanity.option_all_with_marriage
    exclude_ginger_island = world_options[options.ExcludeGingerIsland] == options.ExcludeGingerIsland.option_true
    for villager in all_villagers:
        if not villager.available and exclude_locked_villagers:
            continue
        if not villager.bachelor and exclude_non_bachelors:
            continue
        if villager.name == "Leo" and exclude_ginger_island:
            continue
        for heart in range(1, 15):
            if villager.bachelor and exclude_post_marriage_hearts and heart > 8:
                continue
            if villager.bachelor or heart < 11:
                items.append(item_factory(f"{villager.name}: 1 <3"))
    if not exclude_non_bachelors:
        for heart in range(1, 6):
            items.append(item_factory(f"Pet: 1 <3"))


def create_arcade_machine_items(item_factory: StardewItemFactory, world_options: StardewOptions,
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


def create_traveling_merchant_items(item_factory: StardewItemFactory) -> List[Item]:
    return [
        *(item_factory(item) for item in items_by_group[Group.TRAVELING_MERCHANT_DAY]),
        *(item_factory(item) for item in ["Traveling Merchant Stock Size"] * 6),
        *(item_factory(item) for item in ["Traveling Merchant Discount"] * 8),
    ]


def create_seasons(item_factory: StardewItemFactory, world_options: StardewOptions) -> List[Item]:
    if world_options[options.SeasonRandomization] == options.SeasonRandomization.option_disabled:
        return []

    if world_options[options.SeasonRandomization] == options.SeasonRandomization.option_progressive:
        return [item_factory(item) for item in ["Progressive Season"] * 3]

    return [item_factory(item) for item in items_by_group[Group.SEASON]]


def create_seeds(item_factory: StardewItemFactory, world_options: StardewOptions) -> List[Item]:
    if world_options[options.SeedShuffle] == options.SeedShuffle.option_disabled:
        return []

    include_ginger_island = world_options[options.ExcludeGingerIsland] != options.ExcludeGingerIsland.option_true
    return [item_factory(item) for item in items_by_group[Group.SEED_SHUFFLE]
            if include_ginger_island or Group.GINGER_ISLAND not in item.groups]


def create_festival_rewards(item_factory: StardewItemFactory, world_options: StardewOptions) -> List[Item]:
    if world_options[options.FestivalLocations] == options.FestivalLocations.option_disabled:
        return []

    return [
        *[item_factory(item) for item in items_by_group[Group.FESTIVAL] if
          item.classification != ItemClassification.filler],
        item_factory("Stardrop"),
    ]


def create_filler_festival_rewards(item_factory: StardewItemFactory, world_options: StardewOptions) -> List[Item]:
    if world_options[options.FestivalLocations] == options.FestivalLocations.option_disabled:
        return []

    return [item_factory(item) for item in items_by_group[Group.FESTIVAL] if
            item.classification == ItemClassification.filler]


def create_special_order_board_rewards(item_factory: StardewItemFactory, world_options: StardewOptions) -> List[Item]:
    if world_options[options.SpecialOrderLocations] == options.SpecialOrderLocations.option_disabled:
        return []

    return [item_factory(item) for item in items_by_group[Group.SPECIAL_ORDER_BOARD]]


def create_special_order_qi_rewards(item_factory: StardewItemFactory, world_options: StardewOptions) -> List[Item]:
    if (world_options[options.SpecialOrderLocations] != options.SpecialOrderLocations.option_board_qi or
        world_options[options.ExcludeGingerIsland] == options.ExcludeGingerIsland.option_true):
        return []

    return [item_factory("100 Qi Gems"), item_factory("10 Qi Gems"), item_factory("40 Qi Gems"),
            item_factory("25 Qi Gems"), item_factory("25 Qi Gems"), item_factory("40 Qi Gems"),
            item_factory("20 Qi Gems"), item_factory("50 Qi Gems"), item_factory("40 Qi Gems"),
            item_factory("35 Qi Gems")]


def create_unique_filler_items(item_factory: StardewItemFactory, world_options: options.StardewOptions, random: Random,
                               available_item_slots: int) -> List[Item]:
    items = []

    items.extend(create_filler_festival_rewards(item_factory, world_options))

    if len(items) > available_item_slots:
        items = random.sample(items, available_item_slots)
    return items


def fill_with_resource_packs(item_factory: StardewItemFactory, world_options: options.StardewOptions, random: Random, items_already_added: List[Item],
                             number_locations: int) -> List[Item]:
    all_resource_packs = items_by_group[Group.RESOURCE_PACK]
    items_already_added_names = [item.name for item in items_already_added]
    useful_resource_packs = [pack for pack in items_by_group[Group.RESOURCE_PACK_USEFUL]
                             if pack.name not in items_already_added_names]
    all_resource_packs.extend(items_by_group[Group.TRASH])
    # all_resource_packs.extend(items_by_group[Group.TRAP])

    all_resource_packs = [pack for pack in all_resource_packs if Group.DEPRECATED not in pack.groups]
    if world_options[options.ExcludeGingerIsland] == options.ExcludeGingerIsland.option_true:
        all_resource_packs = [pack for pack in all_resource_packs if Group.GINGER_ISLAND not in pack.groups]
        useful_resource_packs = [pack for pack in useful_resource_packs if Group.GINGER_ISLAND not in pack.groups]

    items = []
    number_useful_packs = len(useful_resource_packs)
    required_resource_pack = number_locations - len(items_already_added)
    if required_resource_pack < number_useful_packs:
        chosen_useful_packs = [item_factory(resource_pack) for resource_pack in
                               random.sample(useful_resource_packs, required_resource_pack)]
        items.extend(chosen_useful_packs)
        return items

    chosen_useful_packs = [item_factory(resource_pack) for resource_pack in useful_resource_packs]
    items.extend(chosen_useful_packs)
    required_resource_pack -= number_useful_packs

    for i in range(required_resource_pack - 1):
        resource_pack = random.choice(all_resource_packs)
        exactly_2 = Group.EXACTLY_TWO in resource_pack.groups
        items.append(item_factory(resource_pack))
        if exactly_2:
            items.append(item_factory(resource_pack))
            i += 1
        if exactly_2 or Group.MAXIMUM_ONE in resource_pack.groups:
            all_resource_packs.remove(resource_pack)

    # The last pack is added from the packs that don't need to exist twice
    all_solo_packs = [pack for pack in all_resource_packs if Group.EXACTLY_TWO not in pack.groups]
    last_resource_pack = random.choice(all_solo_packs)
    items.append(item_factory(last_resource_pack))

    return items
