import csv
import enum
import logging
from dataclasses import dataclass, field
from pathlib import Path
from random import Random
from typing import Dict, List, Protocol, Union, Set, Optional

from BaseClasses import Item, ItemClassification
from . import data
from .data.villagers_data import all_villagers
from .mods.mod_data import ModNames
from .options import StardewValleyOptions, TrapItems, FestivalLocations, ExcludeGingerIsland, SpecialOrderLocations, SeasonRandomization, Cropsanity, Friendsanity, Museumsanity, \
    Fishsanity, BuildingProgression, SkillProgression, ToolProgression, ElevatorProgression, BackpackProgression, ArcadeMachineLocations
from .strings.ap_names.buff_names import Buff

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
    CROPSANITY = enum.auto()
    FISHING_RESOURCE = enum.auto()
    SEASON = enum.auto()
    TRAVELING_MERCHANT_DAY = enum.auto()
    MUSEUM = enum.auto()
    FRIENDSANITY = enum.auto()
    FESTIVAL = enum.auto()
    RARECROW = enum.auto()
    TRAP = enum.auto()
    MAXIMUM_ONE = enum.auto()
    EXACTLY_TWO = enum.auto()
    DEPRECATED = enum.auto()
    RESOURCE_PACK_USEFUL = enum.auto()
    SPECIAL_ORDER_BOARD = enum.auto()
    SPECIAL_ORDER_QI = enum.auto()
    BABY = enum.auto()
    GINGER_ISLAND = enum.auto()
    WALNUT_PURCHASE = enum.auto()
    TV_CHANNEL = enum.auto()
    MAGIC_SPELL = enum.auto()


@dataclass(frozen=True)
class ItemData:
    code_without_offset: Optional[int]
    name: str
    classification: ItemClassification
    mod_name: Optional[str] = None
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
            mod_name = str(item["mod_name"]) if item["mod_name"] else None
            items.append(ItemData(id, item["name"], classification, mod_name, groups))
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
                 options: StardewValleyOptions, random: Random) -> List[Item]:
    items = []
    unique_items = create_unique_items(item_factory, options, random)

    for item in items_to_exclude:
        if item in unique_items:
            unique_items.remove(item)

    assert len(unique_items) <= locations_count, f"There should be at least as many locations [{locations_count}] as there are mandatory items [{len(unique_items)}]"
    items += unique_items
    logger.debug(f"Created {len(unique_items)} unique items")

    unique_filler_items = create_unique_filler_items(item_factory, options, random, locations_count - len(items))
    items += unique_filler_items
    logger.debug(f"Created {len(unique_filler_items)} unique filler items")

    resource_pack_items = fill_with_resource_packs_and_traps(item_factory, options, random, items, locations_count)
    items += resource_pack_items
    logger.debug(f"Created {len(resource_pack_items)} resource packs")

    return items


def create_unique_items(item_factory: StardewItemFactory, options: StardewValleyOptions, random: Random) -> List[Item]:
    items = []

    items.extend(item_factory(item) for item in items_by_group[Group.COMMUNITY_REWARD])

    create_backpack_items(item_factory, options, items)
    create_mine_rewards(item_factory, items, random)
    create_elevators(item_factory, options, items)
    create_tools(item_factory, options, items)
    create_skills(item_factory, options, items)
    create_wizard_buildings(item_factory, options, items)
    create_carpenter_buildings(item_factory, options, items)
    items.append(item_factory("Beach Bridge"))
    items.append(item_factory("Dark Talisman"))
    create_tv_channels(item_factory, items)
    create_special_quest_rewards(item_factory, items)
    create_stardrops(item_factory, options, items)
    create_museum_items(item_factory, options, items)
    create_arcade_machine_items(item_factory, options, items)
    items.append(item_factory(random.choice(items_by_group[Group.GALAXY_WEAPONS])))
    create_player_buffs(item_factory, options, items)
    create_traveling_merchant_items(item_factory, items)
    items.append(item_factory("Return Scepter"))
    create_seasons(item_factory, options, items)
    create_seeds(item_factory, options, items)
    create_friendsanity_items(item_factory, options, items)
    create_festival_rewards(item_factory, options, items)
    create_babies(item_factory, items, random)
    create_special_order_board_rewards(item_factory, options, items)
    create_special_order_qi_rewards(item_factory, options, items)
    create_walnut_purchase_rewards(item_factory, options, items)
    create_magic_mod_spells(item_factory, options, items)

    return items


def create_backpack_items(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if (options.backpack_progression == BackpackProgression.option_progressive or
            options.backpack_progression == BackpackProgression.option_early_progressive):
        items.extend(item_factory(item) for item in ["Progressive Backpack"] * 2)
        if ModNames.big_backpack in options.mods:
            items.append(item_factory("Progressive Backpack"))


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


def create_elevators(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if options.elevator_progression == ElevatorProgression.option_vanilla:
        return

    items.extend([item_factory(item) for item in ["Progressive Mine Elevator"] * 24])
    if ModNames.deepwoods in options.mods:
        items.extend([item_factory(item) for item in ["Progressive Woods Obelisk Sigils"] * 10])
    if ModNames.skull_cavern_elevator in options.mods:
        items.extend([item_factory(item) for item in ["Progressive Skull Cavern Elevator"] * 8])


def create_tools(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if options.tool_progression == ToolProgression.option_progressive:
        items.extend(item_factory(item) for item in items_by_group[Group.PROGRESSIVE_TOOLS] * 4)
    items.append(item_factory("Golden Scythe"))


def create_skills(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if options.skill_progression == SkillProgression.option_progressive:
        for item in items_by_group[Group.SKILL_LEVEL_UP]:
            if item.mod_name not in options.mods and item.mod_name is not None:
                continue
            items.extend(item_factory(item) for item in [item.name] * 10)


def create_wizard_buildings(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    items.append(item_factory("Earth Obelisk"))
    items.append(item_factory("Water Obelisk"))
    items.append(item_factory("Desert Obelisk"))
    items.append(item_factory("Junimo Hut"))
    items.append(item_factory("Gold Clock"))
    if options.exclude_ginger_island == ExcludeGingerIsland.option_false:
        items.append(item_factory("Island Obelisk"))
    if ModNames.deepwoods in options.mods:
        items.append(item_factory("Woods Obelisk"))


def create_carpenter_buildings(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if options.building_progression in {BuildingProgression.option_progressive,
                                                      BuildingProgression.option_progressive_early_shipping_bin}:
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
        if ModNames.tractor in options.mods:
            items.append(item_factory("Tractor Garage"))


def create_special_quest_rewards(item_factory: StardewItemFactory, items: List[Item]):
    items.append(item_factory("Adventurer's Guild"))
    items.append(item_factory("Club Card"))
    items.append(item_factory("Magnifying Glass"))
    items.append(item_factory("Bear's Knowledge"))
    items.append(item_factory("Iridium Snake Milk"))


def create_stardrops(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    items.append(item_factory("Stardrop"))  # The Mines level 100
    items.append(item_factory("Stardrop"))  # Old Master Cannoli
    if options.fishsanity != Fishsanity.option_none:
        items.append(item_factory("Stardrop"))  #Master Angler Stardrop
    if ModNames.deepwoods in options.mods:
        items.append(item_factory("Stardrop"))  # Petting the Unicorn


def create_museum_items(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if options.museumsanity == Museumsanity.option_none:
        return
    items.extend(item_factory(item) for item in ["Magic Rock Candy"] * 5)
    items.extend(item_factory(item) for item in ["Ancient Seeds"] * 5)
    items.extend(item_factory(item) for item in ["Traveling Merchant Metal Detector"] * 4)
    items.append(item_factory("Ancient Seeds Recipe"))
    items.append(item_factory("Stardrop"))
    items.append(item_factory("Rusty Key"))
    items.append(item_factory("Dwarvish Translation Guide"))


def create_friendsanity_items(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if options.friendsanity == Friendsanity.option_none:
        return
    exclude_non_bachelors = options.friendsanity == Friendsanity.option_bachelors
    exclude_locked_villagers = options.friendsanity == Friendsanity.option_starting_npcs or \
                               options.friendsanity == Friendsanity.option_bachelors
    include_post_marriage_hearts = options.friendsanity == Friendsanity.option_all_with_marriage
    exclude_ginger_island = options.exclude_ginger_island == ExcludeGingerIsland.option_true
    heart_size = options.friendsanity_heart_size
    for villager in all_villagers:
        if villager.mod_name not in options.mods and villager.mod_name is not None:
            continue
        if not villager.available and exclude_locked_villagers:
            continue
        if not villager.bachelor and exclude_non_bachelors:
            continue
        if villager.name == "Leo" and exclude_ginger_island:
            continue
        heart_cap = 8 if villager.bachelor else 10
        if include_post_marriage_hearts and villager.bachelor:
            heart_cap = 14
        for heart in range(1, 15):
            if heart > heart_cap:
                break
            if heart % heart_size == 0 or heart == heart_cap:
                items.append(item_factory(f"{villager.name} <3"))
    if not exclude_non_bachelors:
        for heart in range(1, 6):
            if heart % heart_size == 0 or heart == 5:
                items.append(item_factory(f"Pet <3"))


def create_babies(item_factory: StardewItemFactory, items: List[Item], random: Random):
    baby_items = [item for item in items_by_group[Group.BABY]]
    for i in range(2):
        chosen_baby = random.choice(baby_items)
        items.append(item_factory(chosen_baby))


def create_arcade_machine_items(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if options.arcade_machine_locations == ArcadeMachineLocations.option_full_shuffling:
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


def create_player_buffs(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    items.extend(item_factory(item) for item in [Buff.movement] * options.movement_buff_number.value)
    items.extend(item_factory(item) for item in [Buff.luck] * options.luck_buff_number.value)


def create_traveling_merchant_items(item_factory: StardewItemFactory, items: List[Item]):
    items.extend([*(item_factory(item) for item in items_by_group[Group.TRAVELING_MERCHANT_DAY]),
                  *(item_factory(item) for item in ["Traveling Merchant Stock Size"] * 6),
                  *(item_factory(item) for item in ["Traveling Merchant Discount"] * 8)])


def create_seasons(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if options.season_randomization == SeasonRandomization.option_disabled:
        return

    if options.season_randomization == SeasonRandomization.option_progressive:
        items.extend([item_factory(item) for item in ["Progressive Season"] * 3])
        return

    items.extend([item_factory(item) for item in items_by_group[Group.SEASON]])


def create_seeds(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if options.cropsanity == Cropsanity.option_disabled:
        return

    include_ginger_island = options.exclude_ginger_island != ExcludeGingerIsland.option_true
    seed_items = [item_factory(item) for item in items_by_group[Group.CROPSANITY] if include_ginger_island or Group.GINGER_ISLAND not in item.groups]
    items.extend(seed_items)


def create_festival_rewards(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if options.festival_locations == FestivalLocations.option_disabled:
        return

    items.extend([*[item_factory(item) for item in items_by_group[Group.FESTIVAL] if item.classification != ItemClassification.filler],
                  item_factory("Stardrop")])


def create_walnut_purchase_rewards(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if options.exclude_ginger_island == ExcludeGingerIsland.option_true:
        return

    items.extend([item_factory("Boat Repair"),
                  item_factory("Open Professor Snail Cave"),
                  item_factory("Ostrich Incubator Recipe"),
                  item_factory("Treehouse"),
                  *[item_factory(item) for item in items_by_group[Group.WALNUT_PURCHASE]]])



def create_special_order_board_rewards(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if options.special_order_locations == SpecialOrderLocations.option_disabled:
        return

    items.extend([item_factory(item) for item in items_by_group[Group.SPECIAL_ORDER_BOARD]])


def create_special_order_qi_rewards(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if (options.special_order_locations != SpecialOrderLocations.option_board_qi or
            options.exclude_ginger_island == ExcludeGingerIsland.option_true):
        return
    qi_gem_rewards = ["100 Qi Gems", "10 Qi Gems", "40 Qi Gems", "25 Qi Gems", "25 Qi Gems",
                      "40 Qi Gems", "20 Qi Gems", "50 Qi Gems", "40 Qi Gems", "35 Qi Gems"]
    qi_gem_items = [item_factory(reward) for reward in qi_gem_rewards]
    items.extend(qi_gem_items)


def create_tv_channels(item_factory: StardewItemFactory, items: List[Item]):
    items.extend([item_factory(item) for item in items_by_group[Group.TV_CHANNEL]])


def create_filler_festival_rewards(item_factory: StardewItemFactory, options: StardewValleyOptions) -> List[Item]:
    if options.festival_locations == FestivalLocations.option_disabled:
        return []

    return [item_factory(item) for item in items_by_group[Group.FESTIVAL] if
            item.classification == ItemClassification.filler]


def create_magic_mod_spells(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if ModNames.magic not in options.mods:
        return []
    items.extend([item_factory(item) for item in items_by_group[Group.MAGIC_SPELL]])


def create_unique_filler_items(item_factory: StardewItemFactory, options: StardewValleyOptions, random: Random,
                               available_item_slots: int) -> List[Item]:
    items = []

    items.extend(create_filler_festival_rewards(item_factory, options))

    if len(items) > available_item_slots:
        items = random.sample(items, available_item_slots)
    return items


def fill_with_resource_packs_and_traps(item_factory: StardewItemFactory, options: StardewValleyOptions, random: Random,
                                       items_already_added: List[Item],
                                       number_locations: int) -> List[Item]:
    include_traps = options.trap_items != TrapItems.option_no_traps
    all_filler_packs = [pack for pack in items_by_group[Group.RESOURCE_PACK]]
    all_filler_packs.extend(items_by_group[Group.TRASH])
    if include_traps:
        all_filler_packs.extend(items_by_group[Group.TRAP])
    items_already_added_names = [item.name for item in items_already_added]
    useful_resource_packs = [pack for pack in items_by_group[Group.RESOURCE_PACK_USEFUL]
                             if pack.name not in items_already_added_names]
    trap_items = [pack for pack in items_by_group[Group.TRAP]
                  if pack.name not in items_already_added_names and
                  (pack.mod_name is None or pack.mod_name in options.mods)]

    priority_filler_items = []
    priority_filler_items.extend(useful_resource_packs)
    if include_traps:
        priority_filler_items.extend(trap_items)

    all_filler_packs = remove_excluded_packs(all_filler_packs, options)
    priority_filler_items = remove_excluded_packs(priority_filler_items, options)

    number_priority_items = len(priority_filler_items)
    required_resource_pack = number_locations - len(items_already_added)
    if required_resource_pack < number_priority_items:
        chosen_priority_items = [item_factory(resource_pack) for resource_pack in
                               random.sample(priority_filler_items, required_resource_pack)]
        return chosen_priority_items

    items = []
    chosen_priority_items = [item_factory(resource_pack) for resource_pack in priority_filler_items]
    items.extend(chosen_priority_items)
    required_resource_pack -= number_priority_items
    all_filler_packs = [filler_pack for filler_pack in all_filler_packs
                        if Group.MAXIMUM_ONE not in filler_pack.groups or
                        filler_pack.name not in [priority_item.name for priority_item in priority_filler_items]]

    while required_resource_pack > 0:
        resource_pack = random.choice(all_filler_packs)
        exactly_2 = Group.EXACTLY_TWO in resource_pack.groups
        while exactly_2 and required_resource_pack == 1:
            resource_pack = random.choice(all_filler_packs)
            exactly_2 = Group.EXACTLY_TWO in resource_pack.groups
        items.append(item_factory(resource_pack))
        required_resource_pack -= 1
        if exactly_2:
            items.append(item_factory(resource_pack))
            required_resource_pack -= 1
        if exactly_2 or Group.MAXIMUM_ONE in resource_pack.groups:
            all_filler_packs.remove(resource_pack)

    return items


def remove_excluded_packs(packs, options: StardewValleyOptions):
    included_packs = [pack for pack in packs if Group.DEPRECATED not in pack.groups]
    if options.exclude_ginger_island == ExcludeGingerIsland.option_true:
        included_packs = [pack for pack in included_packs if Group.GINGER_ISLAND not in pack.groups]
    return included_packs
