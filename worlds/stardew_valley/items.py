import csv
import enum
import logging
from dataclasses import dataclass, field
from functools import reduce
from pathlib import Path
from random import Random
from typing import Dict, List, Protocol, Union, Set, Optional

from BaseClasses import Item, ItemClassification
from . import data
from .content.feature import friendsanity
from .content.game_content import StardewContent
from .data.game_item import ItemTag
from .logic.logic_event import all_events
from .mods.mod_data import ModNames
from .options import StardewValleyOptions, TrapItems, FestivalLocations, ExcludeGingerIsland, SpecialOrderLocations, SeasonRandomization, Museumsanity, \
    ElevatorProgression, BackpackProgression, ArcadeMachineLocations, Monstersanity, Goal, \
    Chefsanity, Craftsanity, BundleRandomization, EntranceRandomization, Shipsanity, Walnutsanity, EnabledFillerBuffs
from .strings.ap_names.ap_option_names import BuffOptionName, WalnutsanityOptionName
from .strings.ap_names.ap_weapon_names import APWeapon
from .strings.ap_names.buff_names import Buff
from .strings.ap_names.community_upgrade_names import CommunityUpgrade
from .strings.ap_names.mods.mod_items import SVEQuestItem
from .strings.currency_names import Currency
from .strings.tool_names import Tool
from .strings.wallet_item_names import Wallet

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
    SKILL_MASTERY = enum.auto()
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
    BONUS = enum.auto()
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
    # Mods
    MAGIC_SPELL = enum.auto()
    MOD_WARP = enum.auto()


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
    from importlib.resources import files

    items = []
    with files(data).joinpath("items.csv").open() as file:
        item_reader = csv.DictReader(file)
        for item in item_reader:
            id = int(item["id"]) if item["id"] else None
            classification = reduce((lambda a, b: a | b), {ItemClassification[str_classification] for str_classification in item["classification"].split(",")})
            groups = {Group[group] for group in item["groups"].split(",") if group}
            mod_name = str(item["mod_name"]) if item["mod_name"] else None
            items.append(ItemData(id, item["name"], classification, mod_name, groups))
    return items


events = [
    ItemData(None, e, ItemClassification.progression)
    for e in sorted(all_events)
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


def get_too_many_items_error_message(locations_count: int, items_count: int) -> str:
    return f"There should be at least as many locations [{locations_count}] as there are mandatory items [{items_count}]"


def create_items(item_factory: StardewItemFactory, locations_count: int, items_to_exclude: List[Item],
                 options: StardewValleyOptions, content: StardewContent, random: Random) -> List[Item]:
    items = []
    unique_items = create_unique_items(item_factory, options, content, random)

    remove_items(items_to_exclude, unique_items)

    remove_items_if_no_room_for_them(unique_items, locations_count, random)

    items += unique_items
    logger.debug(f"Created {len(unique_items)} unique items")

    unique_filler_items = create_unique_filler_items(item_factory, options, random, locations_count - len(items))
    items += unique_filler_items
    logger.debug(f"Created {len(unique_filler_items)} unique filler items")

    resource_pack_items = fill_with_resource_packs_and_traps(item_factory, options, random, items, locations_count)
    items += resource_pack_items
    logger.debug(f"Created {len(resource_pack_items)} resource packs")

    return items


def remove_items(items_to_remove, items):
    for item in items_to_remove:
        if item in items:
            items.remove(item)


def remove_items_if_no_room_for_them(unique_items: List[Item], locations_count: int, random: Random):
    if len(unique_items) <= locations_count:
        return

    number_of_items_to_remove = len(unique_items) - locations_count
    removable_items = [item for item in unique_items if item.classification == ItemClassification.filler or item.classification == ItemClassification.trap]
    if len(removable_items) < number_of_items_to_remove:
        logger.debug(f"Player has more items than locations, trying to remove {number_of_items_to_remove} random non-progression items")
        removable_items = [item for item in unique_items if not item.classification & ItemClassification.progression]
    else:
        logger.debug(f"Player has more items than locations, trying to remove {number_of_items_to_remove} random filler items")
    assert len(removable_items) >= number_of_items_to_remove, get_too_many_items_error_message(locations_count, len(unique_items))
    items_to_remove = random.sample(removable_items, number_of_items_to_remove)
    remove_items(items_to_remove, unique_items)


def create_unique_items(item_factory: StardewItemFactory, options: StardewValleyOptions, content: StardewContent, random: Random) -> List[Item]:
    items = []

    items.extend(item_factory(item) for item in items_by_group[Group.COMMUNITY_REWARD])
    items.append(item_factory(CommunityUpgrade.movie_theater))  # It is a community reward, but we need two of them
    create_raccoons(item_factory, options, items)
    items.append(item_factory(Wallet.metal_detector))  # Always offer at least one metal detector

    create_backpack_items(item_factory, options, items)
    create_weapons(item_factory, options, items)
    items.append(item_factory("Skull Key"))
    create_elevators(item_factory, options, items)
    create_tools(item_factory, content, items)
    create_skills(item_factory, content, items)
    create_wizard_buildings(item_factory, options, items)
    create_carpenter_buildings(item_factory, content, items)
    items.append(item_factory("Railroad Boulder Removed"))
    items.append(item_factory(CommunityUpgrade.fruit_bats))
    items.append(item_factory(CommunityUpgrade.mushroom_boxes))
    items.append(item_factory("Beach Bridge"))
    create_tv_channels(item_factory, options, items)
    create_quest_rewards(item_factory, options, items)
    create_stardrops(item_factory, options, content, items)
    create_museum_items(item_factory, options, items)
    create_arcade_machine_items(item_factory, options, items)
    create_movement_buffs(item_factory, options, items)
    create_traveling_merchant_items(item_factory, items)
    items.append(item_factory("Return Scepter"))
    create_seasons(item_factory, options, items)
    create_seeds(item_factory, content, items)
    create_friendsanity_items(item_factory, options, content, items, random)
    create_festival_rewards(item_factory, options, items)
    create_special_order_board_rewards(item_factory, options, items)
    create_special_order_qi_rewards(item_factory, options, items)
    create_walnuts(item_factory, options, items)
    create_walnut_purchase_rewards(item_factory, options, items)
    create_crafting_recipes(item_factory, options, items)
    create_cooking_recipes(item_factory, options, items)
    create_shipsanity_items(item_factory, options, items)
    create_booksanity_items(item_factory, content, items)
    create_goal_items(item_factory, options, items)
    items.append(item_factory("Golden Egg"))
    items.append(item_factory(CommunityUpgrade.mr_qi_plane_ride))

    create_sve_special_items(item_factory, options, items)
    create_magic_mod_spells(item_factory, options, items)
    create_deepwoods_pendants(item_factory, options, items)
    create_archaeology_items(item_factory, options, items)

    return items


def create_raccoons(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    number_progressive_raccoons = 9
    if options.quest_locations.has_no_story_quests():
        number_progressive_raccoons = number_progressive_raccoons - 1

    items.extend(item_factory(item) for item in [CommunityUpgrade.raccoon] * number_progressive_raccoons)


def create_backpack_items(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if (options.backpack_progression == BackpackProgression.option_progressive or
            options.backpack_progression == BackpackProgression.option_early_progressive):
        items.extend(item_factory(item) for item in ["Progressive Backpack"] * 2)
        if ModNames.big_backpack in options.mods:
            items.append(item_factory("Progressive Backpack"))


def create_weapons(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    weapons = weapons_count(options)
    items.extend(item_factory(item) for item in [APWeapon.slingshot] * 2)
    monstersanity = options.monstersanity
    if monstersanity == Monstersanity.option_none:  # Without monstersanity, might not be enough checks to split the weapons
        items.extend(item_factory(item) for item in [APWeapon.weapon] * weapons)
        items.extend(item_factory(item) for item in [APWeapon.footwear] * 3)  # 1-2 | 3-4 | 6-7-8
        return

    items.extend(item_factory(item) for item in [APWeapon.sword] * weapons)
    items.extend(item_factory(item) for item in [APWeapon.club] * weapons)
    items.extend(item_factory(item) for item in [APWeapon.dagger] * weapons)
    items.extend(item_factory(item) for item in [APWeapon.footwear] * 4)  # 1-2 | 3-4 | 6-7-8 | 11-13
    if monstersanity == Monstersanity.option_goals or monstersanity == Monstersanity.option_one_per_category or \
            monstersanity == Monstersanity.option_short_goals or monstersanity == Monstersanity.option_very_short_goals:
        return
    if options.exclude_ginger_island == ExcludeGingerIsland.option_true:
        rings_items = [item for item in items_by_group[Group.RING] if item.classification is not ItemClassification.filler]
    else:
        rings_items = [item for item in items_by_group[Group.RING]]
    items.extend(item_factory(item) for item in rings_items)


def create_elevators(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if options.elevator_progression == ElevatorProgression.option_vanilla:
        return

    items.extend([item_factory(item) for item in ["Progressive Mine Elevator"] * 24])
    if ModNames.deepwoods in options.mods:
        items.extend([item_factory(item) for item in ["Progressive Woods Obelisk Sigils"] * 10])
    if ModNames.skull_cavern_elevator in options.mods:
        items.extend([item_factory(item) for item in ["Progressive Skull Cavern Elevator"] * 8])


def create_tools(item_factory: StardewItemFactory, content: StardewContent, items: List[Item]):
    tool_progression = content.features.tool_progression
    for tool, count in tool_progression.tool_distribution.items():
        item = item_table[tool_progression.to_progressive_item(tool)]

        # Trash can is only used in tool upgrade logic, so the last trash can is not progression because it basically does not unlock anything.
        if tool == Tool.trash_can:
            count -= 1
            items.append(item_factory(item, ItemClassification.useful))

        items.extend([item_factory(item) for _ in range(count)])


def create_skills(item_factory: StardewItemFactory, content: StardewContent, items: List[Item]):
    skill_progression = content.features.skill_progression
    if not skill_progression.is_progressive:
        return

    for skill in content.skills.values():
        items.extend(item_factory(skill.level_name) for _ in skill_progression.get_randomized_level_names_by_level(skill))

        if skill_progression.is_mastery_randomized(skill):
            items.append(item_factory(skill.mastery_name))

    if skill_progression.are_masteries_shuffled:
        items.append(item_factory(Wallet.mastery_of_the_five_ways))


def create_wizard_buildings(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    useless_buildings_classification = ItemClassification.progression_skip_balancing if world_is_perfection(options) else ItemClassification.useful
    items.append(item_factory("Earth Obelisk", useless_buildings_classification))
    items.append(item_factory("Water Obelisk", useless_buildings_classification))
    items.append(item_factory("Desert Obelisk"))
    items.append(item_factory("Junimo Hut"))
    items.append(item_factory("Gold Clock", useless_buildings_classification))
    if options.exclude_ginger_island == ExcludeGingerIsland.option_false:
        items.append(item_factory("Island Obelisk"))
    if ModNames.deepwoods in options.mods:
        items.append(item_factory("Woods Obelisk"))


def create_carpenter_buildings(item_factory: StardewItemFactory, content: StardewContent, items: List[Item]):
    building_progression = content.features.building_progression
    if not building_progression.is_progressive:
        return

    for building in content.farm_buildings.values():
        item_name, _ = building_progression.to_progressive_item(building.name)
        items.append(item_factory(item_name))


def create_quest_rewards(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    create_special_quest_rewards(item_factory, options, items)
    create_help_wanted_quest_rewards(item_factory, options, items)

    create_quest_rewards_sve(item_factory, options, items)


def create_special_quest_rewards(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if options.quest_locations.has_no_story_quests():
        return
    # items.append(item_factory("Adventurer's Guild")) # Now unlocked always!
    items.append(item_factory(Wallet.club_card))
    items.append(item_factory(Wallet.magnifying_glass))
    if ModNames.sve in options.mods:
        items.append(item_factory(Wallet.bears_knowledge))
    else:
        items.append(item_factory(Wallet.bears_knowledge, ItemClassification.useful))  # Not necessary outside of SVE
    items.append(item_factory(Wallet.iridium_snake_milk))
    items.append(item_factory("Dark Talisman"))
    if options.exclude_ginger_island == ExcludeGingerIsland.option_false:
        items.append(item_factory("Fairy Dust Recipe"))


def create_help_wanted_quest_rewards(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if options.quest_locations <= 0:
        return

    number_help_wanted = options.quest_locations.value
    quest_per_prize_ticket = 3
    number_prize_tickets = number_help_wanted // quest_per_prize_ticket
    items.extend(item_factory(item) for item in [Currency.prize_ticket] * number_prize_tickets)


def create_stardrops(item_factory: StardewItemFactory, options: StardewValleyOptions, content: StardewContent, items: List[Item]):
    stardrops_classification = get_stardrop_classification(options)
    items.append(item_factory("Stardrop", stardrops_classification))  # The Mines level 100
    items.append(item_factory("Stardrop", stardrops_classification))  # Old Master Cannoli
    items.append(item_factory("Stardrop", stardrops_classification))  # Krobus Stardrop
    if content.features.fishsanity.is_enabled:
        items.append(item_factory("Stardrop", stardrops_classification))  # Master Angler Stardrop
    if ModNames.deepwoods in options.mods:
        items.append(item_factory("Stardrop", stardrops_classification))  # Petting the Unicorn
    if content.features.friendsanity.is_enabled:
        items.append(item_factory("Stardrop", stardrops_classification))  # Spouse Stardrop


def create_museum_items(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    items.append(item_factory(Wallet.rusty_key))
    items.append(item_factory(Wallet.dwarvish_translation_guide))
    items.append(item_factory("Ancient Seeds Recipe"))
    items.append(item_factory("Stardrop", get_stardrop_classification(options)))
    if options.museumsanity == Museumsanity.option_none:
        return
    items.extend(item_factory(item) for item in ["Magic Rock Candy"] * 10)
    items.extend(item_factory(item) for item in ["Ancient Seeds"] * 5)
    items.append(item_factory(Wallet.metal_detector))


def create_friendsanity_items(item_factory: StardewItemFactory, options: StardewValleyOptions, content: StardewContent, items: List[Item], random: Random):
    if not content.features.friendsanity.is_enabled:
        return

    create_babies(item_factory, items, random)

    for villager in content.villagers.values():
        item_name = friendsanity.to_item_name(villager.name)

        for _ in content.features.friendsanity.get_randomized_hearts(villager):
            items.append(item_factory(item_name, ItemClassification.progression))

    need_pet = options.goal == Goal.option_grandpa_evaluation
    pet_item_classification = ItemClassification.progression_skip_balancing if need_pet else ItemClassification.useful

    for _ in content.features.friendsanity.get_pet_randomized_hearts():
        items.append(item_factory(friendsanity.pet_heart_item_name, pet_item_classification))


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


def create_movement_buffs(item_factory, options: StardewValleyOptions, items: List[Item]):
    movement_buffs: int = options.movement_buff_number.value
    items.extend(item_factory(item) for item in [Buff.movement] * movement_buffs)


def create_traveling_merchant_items(item_factory: StardewItemFactory, items: List[Item]):
    items.extend([*(item_factory(item) for item in items_by_group[Group.TRAVELING_MERCHANT_DAY]),
                  *(item_factory(item) for item in ["Traveling Merchant Stock Size"] * 6)])


def create_seasons(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if options.season_randomization == SeasonRandomization.option_disabled:
        return

    if options.season_randomization == SeasonRandomization.option_progressive:
        items.extend([item_factory(item) for item in ["Progressive Season"] * 3])
        return

    items.extend([item_factory(item) for item in items_by_group[Group.SEASON]])


def create_seeds(item_factory: StardewItemFactory, content: StardewContent, items: List[Item]):
    if not content.features.cropsanity.is_enabled:
        return

    items.extend(item_factory(item_table[seed.name]) for seed in content.find_tagged_items(ItemTag.CROPSANITY_SEED))


def create_festival_rewards(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    items.append(item_factory("Deluxe Scarecrow Recipe"))
    if options.festival_locations == FestivalLocations.option_disabled:
        return

    festival_rewards = [item_factory(item) for item in items_by_group[Group.FESTIVAL] if item.classification != ItemClassification.filler]
    items.extend([*festival_rewards, item_factory("Stardrop", get_stardrop_classification(options))])


def create_walnuts(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    walnutsanity = options.walnutsanity
    if options.exclude_ginger_island == ExcludeGingerIsland.option_true or walnutsanity == Walnutsanity.preset_none:
        return

    # Give baseline walnuts just to be nice
    num_single_walnuts = 0
    num_triple_walnuts = 2
    num_penta_walnuts = 1
    # https://stardewvalleywiki.com/Golden_Walnut
    # Totals should be accurate, but distribution is slightly offset to make room for baseline walnuts
    if WalnutsanityOptionName.puzzles in walnutsanity:  # 61
        num_single_walnuts += 6  # 6
        num_triple_walnuts += 5  # 15
        num_penta_walnuts += 8  # 40
    if WalnutsanityOptionName.bushes in walnutsanity:  # 25
        num_single_walnuts += 16  # 16
        num_triple_walnuts += 3  # 9
    if WalnutsanityOptionName.dig_spots in walnutsanity:  # 18
        num_single_walnuts += 18  # 18
    if WalnutsanityOptionName.repeatables in walnutsanity:  # 33
        num_single_walnuts += 30  # 30
        num_triple_walnuts += 1  # 3

    items.extend([item_factory(item) for item in ["Golden Walnut"] * num_single_walnuts])
    items.extend([item_factory(item) for item in ["3 Golden Walnuts"] * num_triple_walnuts])
    items.extend([item_factory(item) for item in ["5 Golden Walnuts"] * num_penta_walnuts])


def create_walnut_purchase_rewards(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if options.exclude_ginger_island == ExcludeGingerIsland.option_true:
        return

    items.extend([item_factory("Boat Repair"),
                  item_factory("Open Professor Snail Cave"),
                  item_factory("Ostrich Incubator Recipe"),
                  item_factory("Treehouse"),
                  *[item_factory(item) for item in items_by_group[Group.WALNUT_PURCHASE]]])


def create_special_order_board_rewards(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if options.special_order_locations & SpecialOrderLocations.option_board:
        special_order_board_items = [item for item in items_by_group[Group.SPECIAL_ORDER_BOARD]]
        items.extend([item_factory(item) for item in special_order_board_items])


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


def create_special_order_qi_rewards(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if options.exclude_ginger_island == ExcludeGingerIsland.option_true:
        return
    qi_gem_rewards = []
    if options.bundle_randomization >= BundleRandomization.option_remixed:
        qi_gem_rewards.append("15 Qi Gems")
        qi_gem_rewards.append("15 Qi Gems")

    if options.special_order_locations & SpecialOrderLocations.value_qi:
        qi_gem_rewards.extend(["100 Qi Gems", "10 Qi Gems", "40 Qi Gems", "25 Qi Gems", "25 Qi Gems",
                               "40 Qi Gems", "20 Qi Gems", "50 Qi Gems", "40 Qi Gems", "35 Qi Gems"])

    qi_gem_items = [item_factory(reward) for reward in qi_gem_rewards]
    items.extend(qi_gem_items)


def create_tv_channels(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    channels = [channel for channel in items_by_group[Group.TV_CHANNEL]]
    if options.entrance_randomization == EntranceRandomization.option_disabled:
        channels = [channel for channel in channels if channel.name != "The Gateway Gazette"]
    items.extend([item_factory(item) for item in channels])


def create_crafting_recipes(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    has_craftsanity = options.craftsanity == Craftsanity.option_all
    crafting_recipes = []
    crafting_recipes.extend([recipe for recipe in items_by_group[Group.QI_CRAFTING_RECIPE]])
    if has_craftsanity:
        crafting_recipes.extend([recipe for recipe in items_by_group[Group.CRAFTSANITY]])
    crafting_recipes = remove_excluded_items(crafting_recipes, options)
    items.extend([item_factory(item) for item in crafting_recipes])


def create_cooking_recipes(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    chefsanity = options.chefsanity
    if chefsanity == Chefsanity.option_none:
        return

    chefsanity_recipes_by_name = {recipe.name: recipe for recipe in items_by_group[Group.CHEFSANITY_STARTER]}  # Dictionary to not make duplicates

    if chefsanity & Chefsanity.option_queen_of_sauce:
        chefsanity_recipes_by_name.update({recipe.name: recipe for recipe in items_by_group[Group.CHEFSANITY_QOS]})
    if chefsanity & Chefsanity.option_purchases:
        chefsanity_recipes_by_name.update({recipe.name: recipe for recipe in items_by_group[Group.CHEFSANITY_PURCHASE]})
    if chefsanity & Chefsanity.option_friendship:
        chefsanity_recipes_by_name.update({recipe.name: recipe for recipe in items_by_group[Group.CHEFSANITY_FRIENDSHIP]})
    if chefsanity & Chefsanity.option_skills:
        chefsanity_recipes_by_name.update({recipe.name: recipe for recipe in items_by_group[Group.CHEFSANITY_SKILL]})

    filtered_chefsanity_recipes = remove_excluded_items(list(chefsanity_recipes_by_name.values()), options)
    items.extend([item_factory(item) for item in filtered_chefsanity_recipes])


def create_shipsanity_items(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    shipsanity = options.shipsanity
    if shipsanity != Shipsanity.option_everything:
        return

    items.append(item_factory(Wallet.metal_detector))


def create_booksanity_items(item_factory: StardewItemFactory, content: StardewContent, items: List[Item]):
    booksanity = content.features.booksanity
    if not booksanity.is_enabled:
        return

    items.extend(item_factory(item_table[booksanity.to_item_name(book.name)]) for book in content.find_tagged_items(ItemTag.BOOK_POWER))
    progressive_lost_book = item_table[booksanity.progressive_lost_book]
    items.extend(item_factory(progressive_lost_book) for _ in content.features.booksanity.get_randomized_lost_books())


def create_goal_items(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    goal = options.goal
    if goal != Goal.option_perfection and goal != Goal.option_complete_collection:
        return

    items.append(item_factory(Wallet.metal_detector))


def create_archaeology_items(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    mods = options.mods
    if ModNames.archaeology not in mods:
        return

    items.append(item_factory(Wallet.metal_detector))


def create_filler_festival_rewards(item_factory: StardewItemFactory, options: StardewValleyOptions) -> List[Item]:
    if options.festival_locations == FestivalLocations.option_disabled:
        return []

    return [item_factory(item) for item in items_by_group[Group.FESTIVAL] if
            item.classification == ItemClassification.filler]


def create_magic_mod_spells(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if ModNames.magic not in options.mods:
        return
    items.extend([item_factory(item) for item in items_by_group[Group.MAGIC_SPELL]])


def create_deepwoods_pendants(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if ModNames.deepwoods not in options.mods:
        return
    items.extend([item_factory(item) for item in ["Pendant of Elders", "Pendant of Community", "Pendant of Depths"]])


def create_sve_special_items(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if ModNames.sve not in options.mods:
        return

    items.extend([item_factory(item) for item in items_by_group[Group.MOD_WARP] if item.mod_name == ModNames.sve])


def create_quest_rewards_sve(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if ModNames.sve not in options.mods:
        return

    exclude_ginger_island = options.exclude_ginger_island == ExcludeGingerIsland.option_true
    items.extend([item_factory(item) for item in SVEQuestItem.sve_always_quest_items])
    if not exclude_ginger_island:
        items.extend([item_factory(item) for item in SVEQuestItem.sve_always_quest_items_ginger_island])

    if options.quest_locations.has_no_story_quests():
        return

    items.extend([item_factory(item) for item in SVEQuestItem.sve_quest_items])
    if exclude_ginger_island:
        return
    items.extend([item_factory(item) for item in SVEQuestItem.sve_quest_items_ginger_island])


def create_unique_filler_items(item_factory: StardewItemFactory, options: StardewValleyOptions, random: Random,
                               available_item_slots: int) -> List[Item]:
    items = []

    items.extend(create_filler_festival_rewards(item_factory, options))

    if len(items) > available_item_slots:
        items = random.sample(items, available_item_slots)
    return items


def weapons_count(options: StardewValleyOptions):
    weapon_count = 5
    if ModNames.sve in options.mods:
        weapon_count += 1
    return weapon_count


def fill_with_resource_packs_and_traps(item_factory: StardewItemFactory, options: StardewValleyOptions, random: Random,
                                       items_already_added: List[Item],
                                       number_locations: int) -> List[Item]:
    include_traps = options.trap_items != TrapItems.option_no_traps
    items_already_added_names = [item.name for item in items_already_added]
    useful_resource_packs = [pack for pack in items_by_group[Group.RESOURCE_PACK_USEFUL]
                             if pack.name not in items_already_added_names]
    trap_items = [trap for trap in items_by_group[Group.TRAP]
                  if trap.name not in items_already_added_names and
                  (trap.mod_name is None or trap.mod_name in options.mods)]
    player_buffs = get_allowed_player_buffs(options.enabled_filler_buffs)

    priority_filler_items = []
    priority_filler_items.extend(useful_resource_packs)
    priority_filler_items.extend(player_buffs)

    if include_traps:
        priority_filler_items.extend(trap_items)

    exclude_ginger_island = options.exclude_ginger_island == ExcludeGingerIsland.option_true
    all_filler_packs = remove_excluded_items(get_all_filler_items(include_traps, exclude_ginger_island), options)
    all_filler_packs.extend(player_buffs)
    priority_filler_items = remove_excluded_items(priority_filler_items, options)

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


def filter_deprecated_items(items: List[ItemData]) -> List[ItemData]:
    return [item for item in items if Group.DEPRECATED not in item.groups]


def filter_ginger_island_items(exclude_island: bool, items: List[ItemData]) -> List[ItemData]:
    return [item for item in items if not exclude_island or Group.GINGER_ISLAND not in item.groups]


def filter_mod_items(mods: Set[str], items: List[ItemData]) -> List[ItemData]:
    return [item for item in items if item.mod_name is None or item.mod_name in mods]


def remove_excluded_items(items, options: StardewValleyOptions):
    return remove_excluded_items_island_mods(items, options.exclude_ginger_island == ExcludeGingerIsland.option_true, options.mods.value)


def remove_excluded_items_island_mods(items, exclude_ginger_island: bool, mods: Set[str]):
    deprecated_filter = filter_deprecated_items(items)
    ginger_island_filter = filter_ginger_island_items(exclude_ginger_island, deprecated_filter)
    mod_filter = filter_mod_items(mods, ginger_island_filter)
    return mod_filter


def generate_filler_choice_pool(options: StardewValleyOptions) -> list[str]:
    include_traps = options.trap_items != TrapItems.option_no_traps
    exclude_island = options.exclude_ginger_island == ExcludeGingerIsland.option_true

    available_filler = get_all_filler_items(include_traps, exclude_island)
    available_filler = remove_limited_amount_packs(available_filler)

    return [item.name for item in available_filler]


def remove_limited_amount_packs(packs):
    return [pack for pack in packs if Group.MAXIMUM_ONE not in pack.groups and Group.EXACTLY_TWO not in pack.groups]


def get_all_filler_items(include_traps: bool, exclude_ginger_island: bool) -> List[ItemData]:
    all_filler_items = [pack for pack in items_by_group[Group.RESOURCE_PACK]]
    all_filler_items.extend(items_by_group[Group.TRASH])
    if include_traps:
        all_filler_items.extend(items_by_group[Group.TRAP])
    all_filler_items = remove_excluded_items_island_mods(all_filler_items, exclude_ginger_island, set())
    return all_filler_items


def get_allowed_player_buffs(buff_option: EnabledFillerBuffs) -> List[ItemData]:
    allowed_buffs = []
    if BuffOptionName.luck in buff_option:
        allowed_buffs.append(item_table[Buff.luck])
    if BuffOptionName.damage in buff_option:
        allowed_buffs.append(item_table[Buff.damage])
    if BuffOptionName.defense in buff_option:
        allowed_buffs.append(item_table[Buff.defense])
    if BuffOptionName.immunity in buff_option:
        allowed_buffs.append(item_table[Buff.immunity])
    if BuffOptionName.health in buff_option:
        allowed_buffs.append(item_table[Buff.health])
    if BuffOptionName.energy in buff_option:
        allowed_buffs.append(item_table[Buff.energy])
    if BuffOptionName.bite in buff_option:
        allowed_buffs.append(item_table[Buff.bite_rate])
    if BuffOptionName.fish_trap in buff_option:
        allowed_buffs.append(item_table[Buff.fish_trap])
    if BuffOptionName.fishing_bar in buff_option:
        allowed_buffs.append(item_table[Buff.fishing_bar])
    if BuffOptionName.quality in buff_option:
        allowed_buffs.append(item_table[Buff.quality])
    if BuffOptionName.glow in buff_option:
        allowed_buffs.append(item_table[Buff.glow])
    return allowed_buffs


def get_stardrop_classification(options) -> ItemClassification:
    return ItemClassification.progression_skip_balancing if world_is_perfection(options) or world_is_stardrops(options) else ItemClassification.useful


def world_is_perfection(options) -> bool:
    return options.goal == Goal.option_perfection


def world_is_stardrops(options) -> bool:
    return options.goal == Goal.option_mystery_of_the_stardrops
