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
from .strings.ap_names.ap_weapon_names import APWeapon
from .strings.ap_names.buff_names import Buff

ITEM_CODE_OFFSET = 717000

logger = logging.getLogger(__name__)
world_folder = Path(__file__).parent


class Group(enum.Enum):
    RESOURCE_PACK = enum.auto()
    FRIENDSHIP_PACK = enum.auto()
    COMMUNITY_REWARD = enum.auto()
    TRASH = enum.auto()
    FOOTWEAR = enum.auto()
    HATS = enum.auto()
    RING = enum.auto()
    WEAPON = enum.auto()
    WEAPON_GENERIC = enum.auto()
    WEAPON_SWORD = enum.auto()
    WEAPON_CLUB = enum.auto()
    WEAPON_DAGGER = enum.auto()
    WEAPON_SLINGSHOT = enum.auto()
    PROGRESSIVE_TOOLS = enum.auto()
    SKILL_LEVEL_UP = enum.auto()
    BUILDING = enum.auto()
    WIZARD_BUILDING = enum.auto()
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
    def __call__(self, name: Union[str, ItemData], override_classification: ItemClassification = None) -> Item:
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

    assert len(
        unique_items) <= locations_count, f"There should be at least as many locations [{locations_count}] as there are mandatory items [{len(unique_items)}]"
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
    create_weapons(item_factory, world_options, items)
    items.append(item_factory("Skull Key"))
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
    create_player_buffs(item_factory, options, items)
    create_traveling_merchant_items(item_factory, items)
    items.append(item_factory("Return Scepter"))
    create_seasons(item_factory, world_options, items)
    create_seeds(item_factory, world_options, items)
    create_friendsanity_items(item_factory, world_options, items, random)
    create_festival_rewards(item_factory, world_options, items)
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


def create_weapons(item_factory: StardewItemFactory, world_options: StardewOptions, items: List[Item]):
    items.extend(item_factory(item) for item in [APWeapon.slingshot] * 2)
    monstersanity = options.Monstersanity
    monstersanity_option = world_options[monstersanity]
    if monstersanity_option == options.Monstersanity.option_none:  # Without monstersanity, might not be enough checks to split the weapons
        items.extend(item_factory(item) for item in [APWeapon.weapon] * 5)
        items.extend(item_factory(item) for item in [APWeapon.footwear] * 3)  # 1-2 | 3-4 | 6-7-8
        return

    items.extend(item_factory(item) for item in [APWeapon.sword] * 5)
    items.extend(item_factory(item) for item in [APWeapon.club] * 5)
    items.extend(item_factory(item) for item in [APWeapon.dagger] * 5)
    items.extend(item_factory(item) for item in [APWeapon.footwear] * 4)  # 1-2 | 3-4 | 6-7-8 | 11-13
    if monstersanity_option == monstersanity.option_goals or monstersanity_option == monstersanity.option_one_per_category or \
            monstersanity_option == monstersanity.option_short_goals or monstersanity_option == monstersanity.option_very_short_goals:
        return
    if world_options[options.ExcludeGingerIsland] == options.ExcludeGingerIsland.option_true:
        rings_items = [item for item in items_by_group[Group.RING] if item.classification is not ItemClassification.filler]
    else:
        rings_items = [item for item in items_by_group[Group.RING]]
    items.extend(item_factory(item) for item in rings_items)


def create_elevators(item_factory: StardewItemFactory, world_options: StardewOptions, items: List[Item]):
    if world_options[options.ElevatorProgression] == options.ElevatorProgression.option_vanilla:
        return

    items.extend([item_factory(item) for item in ["Progressive Mine Elevator"] * 24])
    if ModNames.deepwoods in options.mods:
        items.extend([item_factory(item) for item in ["Progressive Woods Obelisk Sigils"] * 10])
    if ModNames.skull_cavern_elevator in options.mods:
        items.extend([item_factory(item) for item in ["Progressive Skull Cavern Elevator"] * 8])


def create_tools(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if options.tool_progression == ToolProgression.option_progressive:
        for item_data in items_by_group[Group.PROGRESSIVE_TOOLS]:
            name = item_data.name
            if "Trash Can" in name:
                items.extend([item_factory(item) for item in [item_data] * 3])
                items.append(item_factory(item_data, ItemClassification.useful))
            else:
                items.extend([item_factory(item) for item in [item_data] * 4])
    items.append(item_factory("Golden Scythe"))


def create_skills(item_factory: StardewItemFactory, world_options: StardewOptions, items: List[Item]):
    needs_level_10 = world_is_perfection(world_options) or world_options[options.SpecialOrderLocations] != options.SpecialOrderLocations.option_disabled
    if world_options[options.SkillProgression] == options.SkillProgression.option_progressive:
        for item in items_by_group[Group.SKILL_LEVEL_UP]:
            if item.mod_name not in options.mods and item.mod_name is not None:
                continue
            level_progression = 10 if needs_level_10 else 9
            level_useful = 10 - level_progression
            items.extend(item_factory(item) for item in [item.name] * level_progression)
            items.extend(item_factory(item, ItemClassification.useful) for item in [item.name] * level_useful)


def create_wizard_buildings(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    useless_buildings_classification = ItemClassification.progression_skip_balancing if world_is_perfection(world_options) else ItemClassification.useful
    items.append(item_factory("Earth Obelisk", useless_buildings_classification))
    items.append(item_factory("Water Obelisk", useless_buildings_classification))
    items.append(item_factory("Desert Obelisk"))
    items.append(item_factory("Junimo Hut"))
    items.append(item_factory("Gold Clock", useless_buildings_classification))
    if options.exclude_ginger_island == ExcludeGingerIsland.option_false:
        items.append(item_factory("Island Obelisk"))
    if ModNames.deepwoods in options.mods:
        items.append(item_factory("Woods Obelisk"))


def create_carpenter_buildings(item_factory: StardewItemFactory, world_options: StardewOptions, items: List[Item]):
    building_option = world_options[options.BuildingProgression]
    if building_option == options.BuildingProgression.option_vanilla:
        return
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
    items.append(item_factory("Progressive Shed", ItemClassification.useful))
    items.append(item_factory("Fish Pond"))
    items.append(item_factory("Stable"))
    items.append(item_factory("Slime Hutch"))
    needs_early_bin = building_option == options.BuildingProgression.option_progressive_early_shipping_bin
    has_shipsanity = world_options[options.Shipsanity] != options.Shipsanity.option_none
    need_shipping = needs_early_bin or has_shipsanity or world_is_perfection(world_options)
    items.append(item_factory("Shipping Bin", ItemClassification.progression if need_shipping else ItemClassification.useful))
    items.append(item_factory("Progressive House"))
    items.append(item_factory("Progressive House"))
    items.append(item_factory("Progressive House"))
    if ModNames.tractor in world_options[options.Mods]:
        items.append(item_factory("Tractor Garage"))


def create_special_quest_rewards(item_factory: StardewItemFactory, items: List[Item]):
    items.append(item_factory("Adventurer's Guild"))
    items.append(item_factory("Club Card"))
    items.append(item_factory("Magnifying Glass"))
    items.append(item_factory("Bear's Knowledge"))
    items.append(item_factory("Iridium Snake Milk"))


def create_stardrops(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    stardrops_classification = get_stardrop_classification(world_options)
    items.append(item_factory("Stardrop", stardrops_classification))  # The Mines level 100
    items.append(item_factory("Stardrop", stardrops_classification))  # Old Master Cannoli
    if options.fishsanity != Fishsanity.option_none:
        items.append(item_factory("Stardrop", stardrops_classification))  # Master Angler Stardrop
    if ModNames.deepwoods in options.mods:
        items.append(item_factory("Stardrop", stardrops_classification))  # Petting the Unicorn


def create_museum_items(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    items.append(item_factory("Rusty Key"))
    items.append(item_factory("Dwarvish Translation Guide"))
    items.append(item_factory("Ancient Seeds Recipe"))
    if options.museumsanity == Museumsanity.option_none:
        return
    items.extend(item_factory(item) for item in ["Magic Rock Candy"] * 10)
    items.extend(item_factory(item) for item in ["Ancient Seeds"] * 5)
    items.extend(item_factory(item) for item in ["Traveling Merchant Metal Detector"] * 4)
    items.append(item_factory("Stardrop", get_stardrop_classification(world_options)))


def create_friendsanity_items(item_factory: StardewItemFactory, world_options: StardewOptions, items: List[Item], random):
    if world_options[options.Friendsanity] == options.Friendsanity.option_none:
        return
    exclude_non_bachelors = world_options[options.Friendsanity] == options.Friendsanity.option_bachelors
    exclude_locked_villagers = world_options[options.Friendsanity] == options.Friendsanity.option_starting_npcs or \
                               world_options[options.Friendsanity] == options.Friendsanity.option_bachelors
    include_post_marriage_hearts = world_options[options.Friendsanity] == options.Friendsanity.option_all_with_marriage
    exclude_ginger_island = world_options[options.ExcludeGingerIsland] == options.ExcludeGingerIsland.option_true
    mods = world_options[options.Mods]
    heart_size = world_options[options.FriendsanityHeartSize]
    need_all_hearts_up_to_date = world_is_perfection(world_options)
    government_assigned_bachelor = random.choice([villager.name for villager in all_villagers if villager.bachelor and
                                                  (villager.mod_name is None or villager.mod_name in mods)])
    need_recipes = world_options[options.Shipsanity] == options.Shipsanity.option_everything
    for villager in all_villagers:
        if villager.mod_name not in mods and villager.mod_name is not None:
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
        classification = ItemClassification.progression
        for heart in range(1, 15):
            if heart > heart_cap:
                break
            if heart % heart_size == 0 or heart == heart_cap:
                items.append(item_factory(f"{villager.name} <3", classification))
                if should_next_hearts_be_useful(need_all_hearts_up_to_date, government_assigned_bachelor, need_recipes,
                                                villager, heart, heart_size, heart_cap):
                    classification = ItemClassification.useful
    if not exclude_non_bachelors:
        need_pet = world_options[options.Goal] == options.Goal.option_grandpa_evaluation
        for heart in range(1, 6):
            if heart % heart_size == 0 or heart == 5:
                items.append(item_factory(f"Pet <3", ItemClassification.progression_skip_balancing if need_pet else ItemClassification.useful))


def should_next_hearts_be_useful(need_all_hearts_up_to_date: bool, government_assigned_bachelor: str, need_recipes: bool, villager, heart: int,
                                 heart_size: int, heart_cap: int) -> bool:
    if heart + heart_size < heart_cap:  # If the next heart isn't the last one, it has to be progression
        return False
    if villager.name == government_assigned_bachelor:
        return False
    if need_all_hearts_up_to_date and (heart <= 8 or (heart <= 10 and not villager.bachelor)):
        return False
    if need_recipes and heart <= 7:
        return False
    if need_recipes and villager.name == "Willy":
        return False
    return True


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


def create_player_buffs(item_factory: StardewItemFactory, world_options: options.StardewOptions, items: List[Item]):
    movement_buffs: int = world_options[options.NumberOfMovementBuffs]
    luck_buffs: int = world_options[options.NumberOfLuckBuffs]
    need_all_buffs = world_options[options.SpecialOrderLocations] == options.SpecialOrderLocations.option_board_qi
    need_half_buffs = world_options[options.FestivalLocations] == options.FestivalLocations.option_easy
    create_player_buff(item_factory, Buff.movement, movement_buffs, need_all_buffs, need_half_buffs, items)
    create_player_buff(item_factory, Buff.luck, luck_buffs, need_all_buffs, need_half_buffs, items)


def create_player_buff(item_factory, buff: str, amount: int, need_all_buffs: bool, need_half_buffs: bool, items: List[Item]):
    progression_buffs = amount if need_all_buffs else (amount // 2 if need_half_buffs else 0)
    useful_buffs = amount - progression_buffs
    items.extend(item_factory(item) for item in [buff] * progression_buffs)
    items.extend(item_factory(item, ItemClassification.useful) for item in [buff] * useful_buffs)


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

    festival_rewards = [item_factory(item) for item in items_by_group[Group.FESTIVAL] if item.classification != ItemClassification.filler]
    items.extend([*festival_rewards, item_factory("Stardrop", get_stardrop_classification(world_options))])


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
    need_all_recipes = world_is_perfection(world_options)
    items_and_classifications = {item: (special_order_board_item_classification(item, need_all_recipes)) for item in items_by_group[Group.SPECIAL_ORDER_BOARD]}

    items.extend([item_factory(item, items_and_classifications[item]) for item in items_and_classifications])


def special_order_board_item_classification(item: ItemData, need_all_recipes: bool) -> ItemClassification:
    if item.classification is ItemClassification.useful:
        return ItemClassification.useful
    if item.name == "Special Order Board":
        return ItemClassification.progression
    if need_all_recipes and "Recipe" in item.name:
        return ItemClassification.progression_skip_balancing
    if item.name == "Monster Musk Recipe":
        return ItemClassification.progression_skip_balancing
    return ItemClassification.useful


def create_special_order_qi_rewards(item_factory: StardewItemFactory, world_options: StardewOptions, items: List[Item]):
    if (world_options[options.SpecialOrderLocations] != options.SpecialOrderLocations.option_board_qi or
            world_options[options.ExcludeGingerIsland] == options.ExcludeGingerIsland.option_true):
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

    exclude_ginger_island = options.exclude_ginger_island == ExcludeGingerIsland.option_true
    all_filler_packs = get_all_filler_items(include_traps, exclude_ginger_island)
    priority_filler_items = remove_excluded_packs(priority_filler_items, exclude_ginger_island)

    number_priority_items = len(priority_filler_items)
    required_resource_pack = number_locations - len(items_already_added)
    if required_resource_pack < number_priority_items:
        chosen_priority_items = [item_factory(resource_pack) for resource_pack in
                                 random.sample(priority_filler_items, required_resource_pack)]
        return chosen_priority_items

    items = []
    chosen_priority_items = [item_factory(resource_pack,
                                          ItemClassification.trap if resource_pack.classification == ItemClassification.trap else ItemClassification.useful)
                             for resource_pack in priority_filler_items]
    items.extend(chosen_priority_items)
    required_resource_pack -= number_priority_items
    all_filler_packs = [filler_pack for filler_pack in all_filler_packs
                        if Group.MAXIMUM_ONE not in filler_pack.groups or
                        (filler_pack.name not in [priority_item.name for priority_item in
                                                  priority_filler_items] and filler_pack.name not in items_already_added_names)]

    while required_resource_pack > 0:
        resource_pack = random.choice(all_filler_packs)
        exactly_2 = Group.EXACTLY_TWO in resource_pack.groups
        while exactly_2 and required_resource_pack == 1:
            resource_pack = random.choice(all_filler_packs)
            exactly_2 = Group.EXACTLY_TWO in resource_pack.groups
        classification = ItemClassification.useful if resource_pack.classification == ItemClassification.progression else resource_pack.classification
        items.append(item_factory(resource_pack, classification))
        required_resource_pack -= 1
        if exactly_2:
            items.append(item_factory(resource_pack, classification))
            required_resource_pack -= 1
        if exactly_2 or Group.MAXIMUM_ONE in resource_pack.groups:
            all_filler_packs.remove(resource_pack)

    return items


def remove_excluded_packs(packs, exclude_ginger_island: bool):
    included_packs = [pack for pack in packs if Group.DEPRECATED not in pack.groups]
    if exclude_ginger_island:
        included_packs = [pack for pack in included_packs if Group.GINGER_ISLAND not in pack.groups]
    return included_packs


def remove_limited_amount_packs(packs):
    return [pack for pack in packs if Group.MAXIMUM_ONE not in pack.groups and Group.EXACTLY_TWO not in pack.groups]


def get_all_filler_items(include_traps: bool, exclude_ginger_island: bool):
    all_filler_packs = [pack for pack in items_by_group[Group.RESOURCE_PACK]]
    all_filler_packs.extend(items_by_group[Group.TRASH])
    if include_traps:
        all_filler_packs.extend(items_by_group[Group.TRAP])
    all_filler_packs = remove_excluded_packs(all_filler_packs, exclude_ginger_island)
    return all_filler_packs


def get_stardrop_classification(world_options) -> ItemClassification:
    return ItemClassification.progression_skip_balancing if world_is_perfection(world_options) else ItemClassification.useful


def world_is_perfection(world_options) -> bool:
    return world_options[options.Goal] == options.Goal.option_perfection
