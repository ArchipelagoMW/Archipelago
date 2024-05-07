import csv
import enum
from dataclasses import dataclass
from random import Random
from typing import Optional, Dict, Protocol, List, FrozenSet, Iterable

from . import data
from .bundles.bundle_room import BundleRoom
from .data.fish_data import special_fish, get_fish_for_mods
from .data.museum_data import all_museum_items
from .data.villagers_data import get_villagers_for_mods
from .mods.mod_data import ModNames
from .options import ExcludeGingerIsland, Friendsanity, ArcadeMachineLocations, SpecialOrderLocations, Cropsanity, Fishsanity, Museumsanity, FestivalLocations, \
    SkillProgression, BuildingProgression, ToolProgression, ElevatorProgression, BackpackProgression
from .options import StardewValleyOptions, Craftsanity, Chefsanity, Cooksanity, Shipsanity, Monstersanity
from .strings.goal_names import Goal
from .strings.quest_names import ModQuest
from .strings.region_names import Region
from .strings.villager_names import NPC, ModNPC

LOCATION_CODE_OFFSET = 717000


class LocationTags(enum.Enum):
    MANDATORY = enum.auto()
    BUNDLE = enum.auto()
    COMMUNITY_CENTER_BUNDLE = enum.auto()
    CRAFTS_ROOM_BUNDLE = enum.auto()
    PANTRY_BUNDLE = enum.auto()
    FISH_TANK_BUNDLE = enum.auto()
    BOILER_ROOM_BUNDLE = enum.auto()
    BULLETIN_BOARD_BUNDLE = enum.auto()
    VAULT_BUNDLE = enum.auto()
    COMMUNITY_CENTER_ROOM = enum.auto()
    BACKPACK = enum.auto()
    TOOL_UPGRADE = enum.auto()
    HOE_UPGRADE = enum.auto()
    PICKAXE_UPGRADE = enum.auto()
    AXE_UPGRADE = enum.auto()
    WATERING_CAN_UPGRADE = enum.auto()
    TRASH_CAN_UPGRADE = enum.auto()
    FISHING_ROD_UPGRADE = enum.auto()
    THE_MINES_TREASURE = enum.auto()
    CROPSANITY = enum.auto()
    ELEVATOR = enum.auto()
    SKILL_LEVEL = enum.auto()
    FARMING_LEVEL = enum.auto()
    FISHING_LEVEL = enum.auto()
    FORAGING_LEVEL = enum.auto()
    COMBAT_LEVEL = enum.auto()
    MINING_LEVEL = enum.auto()
    BUILDING_BLUEPRINT = enum.auto()
    STORY_QUEST = enum.auto()
    ARCADE_MACHINE = enum.auto()
    ARCADE_MACHINE_VICTORY = enum.auto()
    JOTPK = enum.auto()
    JUNIMO_KART = enum.auto()
    HELP_WANTED = enum.auto()
    TRAVELING_MERCHANT = enum.auto()
    FISHSANITY = enum.auto()
    MUSEUM_MILESTONES = enum.auto()
    MUSEUM_DONATIONS = enum.auto()
    FRIENDSANITY = enum.auto()
    FESTIVAL = enum.auto()
    FESTIVAL_HARD = enum.auto()
    SPECIAL_ORDER_BOARD = enum.auto()
    SPECIAL_ORDER_QI = enum.auto()
    REQUIRES_QI_ORDERS = enum.auto()
    GINGER_ISLAND = enum.auto()
    WALNUT_PURCHASE = enum.auto()

    BABY = enum.auto()
    MONSTERSANITY = enum.auto()
    MONSTERSANITY_GOALS = enum.auto()
    MONSTERSANITY_PROGRESSIVE_GOALS = enum.auto()
    MONSTERSANITY_MONSTER = enum.auto()
    SHIPSANITY = enum.auto()
    SHIPSANITY_CROP = enum.auto()
    SHIPSANITY_FISH = enum.auto()
    SHIPSANITY_FULL_SHIPMENT = enum.auto()
    COOKSANITY = enum.auto()
    COOKSANITY_QOS = enum.auto()
    CHEFSANITY = enum.auto()
    CHEFSANITY_QOS = enum.auto()
    CHEFSANITY_PURCHASE = enum.auto()
    CHEFSANITY_FRIENDSHIP = enum.auto()
    CHEFSANITY_SKILL = enum.auto()
    CHEFSANITY_STARTER = enum.auto()
    CRAFTSANITY = enum.auto()
    # Mods
    # Skill Mods
    LUCK_LEVEL = enum.auto()
    BINNING_LEVEL = enum.auto()
    COOKING_LEVEL = enum.auto()
    SOCIALIZING_LEVEL = enum.auto()
    MAGIC_LEVEL = enum.auto()
    ARCHAEOLOGY_LEVEL = enum.auto()


@dataclass(frozen=True)
class LocationData:
    code_without_offset: Optional[int]
    region: str
    name: str
    mod_name: Optional[str] = None
    tags: FrozenSet[LocationTags] = frozenset()

    @property
    def code(self) -> Optional[int]:
        return LOCATION_CODE_OFFSET + self.code_without_offset if self.code_without_offset is not None else None


class StardewLocationCollector(Protocol):
    def __call__(self, name: str, code: Optional[int], region: str) -> None:
        raise NotImplementedError


def load_location_csv() -> List[LocationData]:
    try:
        from importlib.resources import files
    except ImportError:
        from importlib_resources import files

    with files(data).joinpath("locations.csv").open() as file:
        reader = csv.DictReader(file)
        return [LocationData(int(location["id"]) if location["id"] else None,
                             location["region"],
                             location["name"],
                             str(location["mod_name"]) if location["mod_name"] else None,
                             frozenset(LocationTags[group]
                                       for group in location["tags"].split(",")
                                       if group))
                for location in reader]


events_locations = [
    LocationData(None, Region.farm_house, Goal.grandpa_evaluation),
    LocationData(None, Region.community_center, Goal.community_center),
    LocationData(None, Region.mines_floor_120, Goal.bottom_of_the_mines),
    LocationData(None, Region.skull_cavern_100, Goal.cryptic_note),
    LocationData(None, Region.beach, Goal.master_angler),
    LocationData(None, Region.museum, Goal.complete_museum),
    LocationData(None, Region.farm_house, Goal.full_house),
    LocationData(None, Region.island_west, Goal.greatest_walnut_hunter),
    LocationData(None, Region.adventurer_guild, Goal.protector_of_the_valley),
    LocationData(None, Region.shipping, Goal.full_shipment),
    LocationData(None, Region.kitchen, Goal.gourmet_chef),
    LocationData(None, Region.farm, Goal.craft_master),
    LocationData(None, Region.shipping, Goal.legend),
    LocationData(None, Region.farm, Goal.mystery_of_the_stardrops),
    LocationData(None, Region.farm, Goal.allsanity),
    LocationData(None, Region.qi_walnut_room, Goal.perfection),
]

all_locations = load_location_csv() + events_locations
location_table: Dict[str, LocationData] = {location.name: location for location in all_locations}
locations_by_tag: Dict[LocationTags, List[LocationData]] = {}


def initialize_groups():
    for location in all_locations:
        for tag in location.tags:
            location_group = locations_by_tag.get(tag, list())
            location_group.append(location)
            locations_by_tag[tag] = location_group


initialize_groups()


def extend_cropsanity_locations(randomized_locations: List[LocationData], options: StardewValleyOptions):
    if options.cropsanity == Cropsanity.option_disabled:
        return

    cropsanity_locations = [item for item in locations_by_tag[LocationTags.CROPSANITY] if not item.mod_name or item.mod_name in options.mods]
    cropsanity_locations = filter_ginger_island(options, cropsanity_locations)
    randomized_locations.extend(cropsanity_locations)


def extend_quests_locations(randomized_locations: List[LocationData], options: StardewValleyOptions):
    if options.quest_locations < 0:
        return

    story_quest_locations = locations_by_tag[LocationTags.STORY_QUEST]
    story_quest_locations = filter_disabled_locations(options, story_quest_locations)
    randomized_locations.extend(story_quest_locations)

    for i in range(0, options.quest_locations.value):
        batch = i // 7
        index_this_batch = i % 7
        if index_this_batch < 4:
            randomized_locations.append(
                location_table[f"Help Wanted: Item Delivery {(batch * 4) + index_this_batch + 1}"])
        elif index_this_batch == 4:
            randomized_locations.append(location_table[f"Help Wanted: Fishing {batch + 1}"])
        elif index_this_batch == 5:
            randomized_locations.append(location_table[f"Help Wanted: Slay Monsters {batch + 1}"])
        elif index_this_batch == 6:
            randomized_locations.append(location_table[f"Help Wanted: Gathering {batch + 1}"])


def extend_fishsanity_locations(randomized_locations: List[LocationData], options: StardewValleyOptions, random: Random):
    prefix = "Fishsanity: "
    fishsanity = options.fishsanity
    active_fish = get_fish_for_mods(options.mods.value)
    if fishsanity == Fishsanity.option_none:
        return
    elif fishsanity == Fishsanity.option_legendaries:
        fish_locations = [location_table[f"{prefix}{fish.name}"] for fish in active_fish if fish.legendary]
        randomized_locations.extend(filter_disabled_locations(options, fish_locations))
    elif fishsanity == Fishsanity.option_special:
        randomized_locations.extend(location_table[f"{prefix}{special.name}"] for special in special_fish)
    elif fishsanity == Fishsanity.option_randomized:
        fish_locations = [location_table[f"{prefix}{fish.name}"] for fish in active_fish if random.random() < 0.4]
        randomized_locations.extend(filter_disabled_locations(options, fish_locations))
    elif fishsanity == Fishsanity.option_all:
        fish_locations = [location_table[f"{prefix}{fish.name}"] for fish in active_fish]
        randomized_locations.extend(filter_disabled_locations(options, fish_locations))
    elif fishsanity == Fishsanity.option_exclude_legendaries:
        fish_locations = [location_table[f"{prefix}{fish.name}"] for fish in active_fish if not fish.legendary]
        randomized_locations.extend(filter_disabled_locations(options, fish_locations))
    elif fishsanity == Fishsanity.option_exclude_hard_fish:
        fish_locations = [location_table[f"{prefix}{fish.name}"] for fish in active_fish if fish.difficulty < 80]
        randomized_locations.extend(filter_disabled_locations(options, fish_locations))
    elif options.fishsanity == Fishsanity.option_only_easy_fish:
        fish_locations = [location_table[f"{prefix}{fish.name}"] for fish in active_fish if fish.difficulty < 50]
        randomized_locations.extend(filter_disabled_locations(options, fish_locations))


def extend_museumsanity_locations(randomized_locations: List[LocationData], options: StardewValleyOptions, random: Random):
    prefix = "Museumsanity: "
    if options.museumsanity == Museumsanity.option_none:
        return
    elif options.museumsanity == Museumsanity.option_milestones:
        randomized_locations.extend(locations_by_tag[LocationTags.MUSEUM_MILESTONES])
    elif options.museumsanity == Museumsanity.option_randomized:
        randomized_locations.extend(location_table[f"{prefix}{museum_item.item_name}"]
                                    for museum_item in all_museum_items if random.random() < 0.4)
    elif options.museumsanity == Museumsanity.option_all:
        randomized_locations.extend(location_table[f"{prefix}{museum_item.item_name}"] for museum_item in all_museum_items)


def extend_friendsanity_locations(randomized_locations: List[LocationData], options: StardewValleyOptions):
    island_villagers = [NPC.leo, ModNPC.lance]
    if options.friendsanity == Friendsanity.option_none:
        return

    randomized_locations.append(location_table[f"Spouse Stardrop"])
    extend_baby_locations(randomized_locations)
    exclude_ginger_island = options.exclude_ginger_island == ExcludeGingerIsland.option_true
    exclude_non_bachelors = options.friendsanity == Friendsanity.option_bachelors
    exclude_locked_villagers = options.friendsanity == Friendsanity.option_starting_npcs or \
                               options.friendsanity == Friendsanity.option_bachelors
    include_post_marriage_hearts = options.friendsanity == Friendsanity.option_all_with_marriage
    heart_size = options.friendsanity_heart_size
    for villager in get_villagers_for_mods(options.mods.value):
        if not villager.available and exclude_locked_villagers:
            continue
        if not villager.bachelor and exclude_non_bachelors:
            continue
        if villager.name in island_villagers and exclude_ginger_island:
            continue
        heart_cap = 8 if villager.bachelor else 10
        if include_post_marriage_hearts and villager.bachelor:
            heart_cap = 14
        for heart in range(1, 15):
            if heart > heart_cap:
                break
            if heart % heart_size == 0 or heart == heart_cap:
                randomized_locations.append(location_table[f"Friendsanity: {villager.name} {heart} <3"])
    if not exclude_non_bachelors:
        for heart in range(1, 6):
            if heart % heart_size == 0 or heart == 5:
                randomized_locations.append(location_table[f"Friendsanity: Pet {heart} <3"])


def extend_baby_locations(randomized_locations: List[LocationData]):
    baby_locations = [location for location in locations_by_tag[LocationTags.BABY]]
    randomized_locations.extend(baby_locations)


def extend_festival_locations(randomized_locations: List[LocationData], options: StardewValleyOptions):
    if options.festival_locations == FestivalLocations.option_disabled:
        return

    festival_locations = locations_by_tag[LocationTags.FESTIVAL]
    randomized_locations.extend(festival_locations)
    extend_hard_festival_locations(randomized_locations, options)


def extend_hard_festival_locations(randomized_locations, options: StardewValleyOptions):
    if options.festival_locations != FestivalLocations.option_hard:
        return

    hard_festival_locations = locations_by_tag[LocationTags.FESTIVAL_HARD]
    randomized_locations.extend(hard_festival_locations)


def extend_special_order_locations(randomized_locations: List[LocationData], options: StardewValleyOptions):
    if options.special_order_locations == SpecialOrderLocations.option_disabled:
        return

    include_island = options.exclude_ginger_island == ExcludeGingerIsland.option_false
    board_locations = filter_disabled_locations(options, locations_by_tag[LocationTags.SPECIAL_ORDER_BOARD])
    randomized_locations.extend(board_locations)
    if options.special_order_locations == SpecialOrderLocations.option_board_qi and include_island:
        include_arcade = options.arcade_machine_locations != ArcadeMachineLocations.option_disabled
        qi_orders = [location for location in locations_by_tag[LocationTags.SPECIAL_ORDER_QI] if
                     include_arcade or LocationTags.JUNIMO_KART not in location.tags]
        randomized_locations.extend(qi_orders)


def extend_walnut_purchase_locations(randomized_locations: List[LocationData], options: StardewValleyOptions):
    if options.exclude_ginger_island == ExcludeGingerIsland.option_true:
        return
    randomized_locations.append(location_table["Repair Ticket Machine"])
    randomized_locations.append(location_table["Repair Boat Hull"])
    randomized_locations.append(location_table["Repair Boat Anchor"])
    randomized_locations.append(location_table["Open Professor Snail Cave"])
    randomized_locations.append(location_table["Complete Island Field Office"])
    randomized_locations.extend(locations_by_tag[LocationTags.WALNUT_PURCHASE])


def extend_mandatory_locations(randomized_locations: List[LocationData], options: StardewValleyOptions):
    mandatory_locations = [location for location in locations_by_tag[LocationTags.MANDATORY]]
    filtered_mandatory_locations = filter_disabled_locations(options, mandatory_locations)
    randomized_locations.extend(filtered_mandatory_locations)


def extend_situational_quest_locations(randomized_locations: List[LocationData], options: StardewValleyOptions):
    if options.quest_locations < 0:
        return
    if ModNames.distant_lands in options.mods:
        if ModNames.alecto in options.mods:
            randomized_locations.append(location_table[ModQuest.WitchOrder])
        else:
            randomized_locations.append(location_table[ModQuest.CorruptedCropsTask])


def extend_bundle_locations(randomized_locations: List[LocationData], bundle_rooms: List[BundleRoom]):
    for room in bundle_rooms:
        room_location = f"Complete {room.name}"
        if room_location in location_table:
            randomized_locations.append(location_table[room_location])
        for bundle in room.bundles:
            randomized_locations.append(location_table[bundle.name])


def extend_backpack_locations(randomized_locations: List[LocationData], options: StardewValleyOptions):
    if options.backpack_progression == BackpackProgression.option_vanilla:
        return
    backpack_locations = [location for location in locations_by_tag[LocationTags.BACKPACK]]
    filtered_backpack_locations = filter_modded_locations(options, backpack_locations)
    randomized_locations.extend(filtered_backpack_locations)


def extend_elevator_locations(randomized_locations: List[LocationData], options: StardewValleyOptions):
    if options.elevator_progression == ElevatorProgression.option_vanilla:
        return
    elevator_locations = [location for location in locations_by_tag[LocationTags.ELEVATOR]]
    filtered_elevator_locations = filter_modded_locations(options, elevator_locations)
    randomized_locations.extend(filtered_elevator_locations)


def extend_monstersanity_locations(randomized_locations: List[LocationData], options):
    monstersanity = options.monstersanity
    if monstersanity == Monstersanity.option_none:
        return
    if monstersanity == Monstersanity.option_one_per_monster or monstersanity == Monstersanity.option_split_goals:
        monster_locations = [location for location in locations_by_tag[LocationTags.MONSTERSANITY_MONSTER]]
        filtered_monster_locations = filter_disabled_locations(options, monster_locations)
        randomized_locations.extend(filtered_monster_locations)
        return
    goal_locations = [location for location in locations_by_tag[LocationTags.MONSTERSANITY_GOALS]]
    filtered_goal_locations = filter_disabled_locations(options, goal_locations)
    randomized_locations.extend(filtered_goal_locations)
    if monstersanity != Monstersanity.option_progressive_goals:
        return
    progressive_goal_locations = [location for location in locations_by_tag[LocationTags.MONSTERSANITY_PROGRESSIVE_GOALS]]
    filtered_progressive_goal_locations = filter_disabled_locations(options, progressive_goal_locations)
    randomized_locations.extend(filtered_progressive_goal_locations)


def extend_shipsanity_locations(randomized_locations: List[LocationData], options: StardewValleyOptions):
    shipsanity = options.shipsanity
    if shipsanity == Shipsanity.option_none:
        return
    if shipsanity == Shipsanity.option_everything:
        ship_locations = [location for location in locations_by_tag[LocationTags.SHIPSANITY]]
        filtered_ship_locations = filter_disabled_locations(options, ship_locations)
        randomized_locations.extend(filtered_ship_locations)
        return
    shipsanity_locations = set()
    if shipsanity == Shipsanity.option_fish or shipsanity == Shipsanity.option_full_shipment_with_fish:
        shipsanity_locations = shipsanity_locations.union({location for location in locations_by_tag[LocationTags.SHIPSANITY_FISH]})
    if shipsanity == Shipsanity.option_crops:
        shipsanity_locations = shipsanity_locations.union({location for location in locations_by_tag[LocationTags.SHIPSANITY_CROP]})
    if shipsanity == Shipsanity.option_full_shipment or shipsanity == Shipsanity.option_full_shipment_with_fish:
        shipsanity_locations = shipsanity_locations.union({location for location in locations_by_tag[LocationTags.SHIPSANITY_FULL_SHIPMENT]})

    filtered_shipsanity_locations = filter_disabled_locations(options, list(shipsanity_locations))
    randomized_locations.extend(filtered_shipsanity_locations)


def extend_cooksanity_locations(randomized_locations: List[LocationData], options: StardewValleyOptions):
    cooksanity = options.cooksanity
    if cooksanity == Cooksanity.option_none:
        return
    if cooksanity == Cooksanity.option_queen_of_sauce:
        cooksanity_locations = (location for location in locations_by_tag[LocationTags.COOKSANITY_QOS])
    else:
        cooksanity_locations = (location for location in locations_by_tag[LocationTags.COOKSANITY])

    filtered_cooksanity_locations = filter_disabled_locations(options, cooksanity_locations)
    randomized_locations.extend(filtered_cooksanity_locations)


def extend_chefsanity_locations(randomized_locations: List[LocationData], options: StardewValleyOptions):
    chefsanity = options.chefsanity
    if chefsanity == Chefsanity.option_none:
        return

    chefsanity_locations_by_name = {}  # Dictionary to not make duplicates

    if chefsanity & Chefsanity.option_queen_of_sauce:
        chefsanity_locations_by_name.update({location.name: location for location in locations_by_tag[LocationTags.CHEFSANITY_QOS]})
    if chefsanity & Chefsanity.option_purchases:
        chefsanity_locations_by_name.update({location.name: location for location in locations_by_tag[LocationTags.CHEFSANITY_PURCHASE]})
    if chefsanity & Chefsanity.option_friendship:
        chefsanity_locations_by_name.update({location.name: location for location in locations_by_tag[LocationTags.CHEFSANITY_FRIENDSHIP]})
    if chefsanity & Chefsanity.option_skills:
        chefsanity_locations_by_name.update({location.name: location for location in locations_by_tag[LocationTags.CHEFSANITY_SKILL]})

    filtered_chefsanity_locations = filter_disabled_locations(options, list(chefsanity_locations_by_name.values()))
    randomized_locations.extend(filtered_chefsanity_locations)


def extend_craftsanity_locations(randomized_locations: List[LocationData], options: StardewValleyOptions):
    if options.craftsanity == Craftsanity.option_none:
        return

    craftsanity_locations = [craft for craft in locations_by_tag[LocationTags.CRAFTSANITY]]
    filtered_chefsanity_locations = filter_disabled_locations(options, craftsanity_locations)
    randomized_locations.extend(filtered_chefsanity_locations)


def create_locations(location_collector: StardewLocationCollector,
                     bundle_rooms: List[BundleRoom],
                     options: StardewValleyOptions,
                     random: Random):
    randomized_locations = []

    extend_mandatory_locations(randomized_locations, options)
    extend_bundle_locations(randomized_locations, bundle_rooms)
    extend_backpack_locations(randomized_locations, options)

    if options.tool_progression & ToolProgression.option_progressive:
        randomized_locations.extend(locations_by_tag[LocationTags.TOOL_UPGRADE])

    extend_elevator_locations(randomized_locations, options)

    if not options.skill_progression == SkillProgression.option_vanilla:
        for location in locations_by_tag[LocationTags.SKILL_LEVEL]:
            if location.mod_name is None or location.mod_name in options.mods:
                randomized_locations.append(location_table[location.name])

    if options.building_progression & BuildingProgression.option_progressive:
        for location in locations_by_tag[LocationTags.BUILDING_BLUEPRINT]:
            if location.mod_name is None or location.mod_name in options.mods:
                randomized_locations.append(location_table[location.name])

    if options.arcade_machine_locations != ArcadeMachineLocations.option_disabled:
        randomized_locations.extend(locations_by_tag[LocationTags.ARCADE_MACHINE_VICTORY])

    if options.arcade_machine_locations == ArcadeMachineLocations.option_full_shuffling:
        randomized_locations.extend(locations_by_tag[LocationTags.ARCADE_MACHINE])

    extend_cropsanity_locations(randomized_locations, options)
    extend_fishsanity_locations(randomized_locations, options, random)
    extend_museumsanity_locations(randomized_locations, options, random)
    extend_friendsanity_locations(randomized_locations, options)

    extend_festival_locations(randomized_locations, options)
    extend_special_order_locations(randomized_locations, options)
    extend_walnut_purchase_locations(randomized_locations, options)

    extend_monstersanity_locations(randomized_locations, options)
    extend_shipsanity_locations(randomized_locations, options)
    extend_cooksanity_locations(randomized_locations, options)
    extend_chefsanity_locations(randomized_locations, options)
    extend_craftsanity_locations(randomized_locations, options)
    extend_quests_locations(randomized_locations, options)
    extend_situational_quest_locations(randomized_locations, options)

    for location_data in randomized_locations:
        location_collector(location_data.name, location_data.code, location_data.region)


def filter_ginger_island(options: StardewValleyOptions, locations: Iterable[LocationData]) -> Iterable[LocationData]:
    include_island = options.exclude_ginger_island == ExcludeGingerIsland.option_false
    return (location for location in locations if include_island or LocationTags.GINGER_ISLAND not in location.tags)


def filter_qi_order_locations(options: StardewValleyOptions, locations: Iterable[LocationData]) -> Iterable[LocationData]:
    include_qi_orders = options.special_order_locations == SpecialOrderLocations.option_board_qi
    return (location for location in locations if include_qi_orders or LocationTags.REQUIRES_QI_ORDERS not in location.tags)


def filter_modded_locations(options: StardewValleyOptions, locations: Iterable[LocationData]) -> Iterable[LocationData]:
    return (location for location in locations if location.mod_name is None or location.mod_name in options.mods)


def filter_disabled_locations(options: StardewValleyOptions, locations: Iterable[LocationData]) -> Iterable[LocationData]:
    locations_island_filter = filter_ginger_island(options, locations)
    locations_qi_filter = filter_qi_order_locations(options, locations_island_filter)
    locations_mod_filter = filter_modded_locations(options, locations_qi_filter)
    return locations_mod_filter
