import csv
import enum
from dataclasses import dataclass
from random import Random
from typing import Optional, Dict, Protocol, List, FrozenSet, Iterable

from . import data
from .bundles.bundle_room import BundleRoom
from .content.game_content import StardewContent
from .data.game_item import ItemTag
from .data.museum_data import all_museum_items
from .mods.mod_data import ModNames
from .options import ExcludeGingerIsland, ArcadeMachineLocations, SpecialOrderLocations, Museumsanity, \
    FestivalLocations, BuildingProgression, ToolProgression, ElevatorProgression, BackpackProgression, FarmType
from .options import StardewValleyOptions, Craftsanity, Chefsanity, Cooksanity, Shipsanity, Monstersanity
from .strings.goal_names import Goal
from .strings.quest_names import ModQuest, Quest
from .strings.region_names import Region, LogicRegion
from .strings.villager_names import NPC

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
    RACCOON_BUNDLES = enum.auto()
    BACKPACK = enum.auto()
    TOOL_UPGRADE = enum.auto()
    HOE_UPGRADE = enum.auto()
    PICKAXE_UPGRADE = enum.auto()
    AXE_UPGRADE = enum.auto()
    WATERING_CAN_UPGRADE = enum.auto()
    TRASH_CAN_UPGRADE = enum.auto()
    FISHING_ROD_UPGRADE = enum.auto()
    PAN_UPGRADE = enum.auto()
    THE_MINES_TREASURE = enum.auto()
    CROPSANITY = enum.auto()
    ELEVATOR = enum.auto()
    SKILL_LEVEL = enum.auto()
    FARMING_LEVEL = enum.auto()
    FISHING_LEVEL = enum.auto()
    FORAGING_LEVEL = enum.auto()
    COMBAT_LEVEL = enum.auto()
    MINING_LEVEL = enum.auto()
    MASTERY_LEVEL = enum.auto()
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
    DESERT_FESTIVAL_CHEF = enum.auto()
    SPECIAL_ORDER_BOARD = enum.auto()
    SPECIAL_ORDER_QI = enum.auto()
    REQUIRES_QI_ORDERS = enum.auto()
    REQUIRES_MASTERIES = enum.auto()
    GINGER_ISLAND = enum.auto()
    WALNUT_PURCHASE = enum.auto()
    WALNUTSANITY = enum.auto()
    WALNUTSANITY_PUZZLE = enum.auto()
    WALNUTSANITY_BUSH = enum.auto()
    WALNUTSANITY_DIG = enum.auto()
    WALNUTSANITY_REPEATABLE = enum.auto()

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
    BOOKSANITY = enum.auto()
    BOOKSANITY_POWER = enum.auto()
    BOOKSANITY_SKILL = enum.auto()
    BOOKSANITY_LOST = enum.auto()
    # Mods
    # Skill Mods
    LUCK_LEVEL = enum.auto()
    BINNING_LEVEL = enum.auto()
    COOKING_LEVEL = enum.auto()
    SOCIALIZING_LEVEL = enum.auto()
    MAGIC_LEVEL = enum.auto()
    ARCHAEOLOGY_LEVEL = enum.auto()

    DEPRECATED = enum.auto()


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
    from importlib.resources import files

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
    LocationData(None, LogicRegion.shipping, Goal.full_shipment),
    LocationData(None, LogicRegion.kitchen, Goal.gourmet_chef),
    LocationData(None, Region.farm, Goal.craft_master),
    LocationData(None, LogicRegion.shipping, Goal.legend),
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


def extend_cropsanity_locations(randomized_locations: List[LocationData], content: StardewContent):
    cropsanity = content.features.cropsanity
    if not cropsanity.is_enabled:
        return

    randomized_locations.extend(location_table[cropsanity.to_location_name(item.name)]
                                for item in content.find_tagged_items(ItemTag.CROPSANITY))


def extend_quests_locations(randomized_locations: List[LocationData], options: StardewValleyOptions, content: StardewContent):
    if options.quest_locations < 0:
        return

    story_quest_locations = locations_by_tag[LocationTags.STORY_QUEST]
    story_quest_locations = filter_disabled_locations(options, content, story_quest_locations)
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


def extend_fishsanity_locations(randomized_locations: List[LocationData], content: StardewContent, random: Random):
    fishsanity = content.features.fishsanity
    if not fishsanity.is_enabled:
        return

    for fish in content.fishes.values():
        if not fishsanity.is_included(fish):
            continue

        if fishsanity.is_randomized and random.random() >= fishsanity.randomization_ratio:
            continue

        randomized_locations.append(location_table[fishsanity.to_location_name(fish.name)])


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


def extend_friendsanity_locations(randomized_locations: List[LocationData], content: StardewContent):
    friendsanity = content.features.friendsanity
    if not friendsanity.is_enabled:
        return

    randomized_locations.append(location_table[f"Spouse Stardrop"])
    extend_baby_locations(randomized_locations)

    for villager in content.villagers.values():
        for heart in friendsanity.get_randomized_hearts(villager):
            randomized_locations.append(location_table[friendsanity.to_location_name(villager.name, heart)])

    for heart in friendsanity.get_pet_randomized_hearts():
        randomized_locations.append(location_table[friendsanity.to_location_name(NPC.pet, heart)])


def extend_baby_locations(randomized_locations: List[LocationData]):
    baby_locations = [location for location in locations_by_tag[LocationTags.BABY]]
    randomized_locations.extend(baby_locations)


def extend_festival_locations(randomized_locations: List[LocationData], options: StardewValleyOptions, random: Random):
    if options.festival_locations == FestivalLocations.option_disabled:
        return

    festival_locations = locations_by_tag[LocationTags.FESTIVAL]
    randomized_locations.extend(festival_locations)
    extend_hard_festival_locations(randomized_locations, options)
    extend_desert_festival_chef_locations(randomized_locations, options, random)


def extend_hard_festival_locations(randomized_locations: List[LocationData], options: StardewValleyOptions):
    if options.festival_locations != FestivalLocations.option_hard:
        return

    hard_festival_locations = locations_by_tag[LocationTags.FESTIVAL_HARD]
    randomized_locations.extend(hard_festival_locations)


def extend_desert_festival_chef_locations(randomized_locations: List[LocationData], options: StardewValleyOptions, random: Random):
    festival_chef_locations = locations_by_tag[LocationTags.DESERT_FESTIVAL_CHEF]
    number_to_add = 5 if options.festival_locations == FestivalLocations.option_easy else 10
    locations_to_add = random.sample(festival_chef_locations, number_to_add)
    randomized_locations.extend(locations_to_add)


def extend_special_order_locations(randomized_locations: List[LocationData], options: StardewValleyOptions, content: StardewContent):
    if options.special_order_locations & SpecialOrderLocations.option_board:
        board_locations = filter_disabled_locations(options, content, locations_by_tag[LocationTags.SPECIAL_ORDER_BOARD])
        randomized_locations.extend(board_locations)

    include_island = options.exclude_ginger_island == ExcludeGingerIsland.option_false
    if options.special_order_locations & SpecialOrderLocations.value_qi and include_island:
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


def extend_mandatory_locations(randomized_locations: List[LocationData], options: StardewValleyOptions, content: StardewContent):
    mandatory_locations = [location for location in locations_by_tag[LocationTags.MANDATORY]]
    filtered_mandatory_locations = filter_disabled_locations(options, content, mandatory_locations)
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


def extend_monstersanity_locations(randomized_locations: List[LocationData], options: StardewValleyOptions, content: StardewContent):
    monstersanity = options.monstersanity
    if monstersanity == Monstersanity.option_none:
        return
    if monstersanity == Monstersanity.option_one_per_monster or monstersanity == Monstersanity.option_split_goals:
        monster_locations = [location for location in locations_by_tag[LocationTags.MONSTERSANITY_MONSTER]]
        filtered_monster_locations = filter_disabled_locations(options, content, monster_locations)
        randomized_locations.extend(filtered_monster_locations)
        return
    goal_locations = [location for location in locations_by_tag[LocationTags.MONSTERSANITY_GOALS]]
    filtered_goal_locations = filter_disabled_locations(options, content, goal_locations)
    randomized_locations.extend(filtered_goal_locations)
    if monstersanity != Monstersanity.option_progressive_goals:
        return
    progressive_goal_locations = [location for location in locations_by_tag[LocationTags.MONSTERSANITY_PROGRESSIVE_GOALS]]
    filtered_progressive_goal_locations = filter_disabled_locations(options, content, progressive_goal_locations)
    randomized_locations.extend(filtered_progressive_goal_locations)


def extend_shipsanity_locations(randomized_locations: List[LocationData], options: StardewValleyOptions, content: StardewContent):
    shipsanity = options.shipsanity
    if shipsanity == Shipsanity.option_none:
        return
    if shipsanity == Shipsanity.option_everything:
        ship_locations = [location for location in locations_by_tag[LocationTags.SHIPSANITY]]
        filtered_ship_locations = filter_disabled_locations(options, content, ship_locations)
        randomized_locations.extend(filtered_ship_locations)
        return
    shipsanity_locations = set()
    if shipsanity == Shipsanity.option_fish or shipsanity == Shipsanity.option_full_shipment_with_fish:
        shipsanity_locations = shipsanity_locations.union({location for location in locations_by_tag[LocationTags.SHIPSANITY_FISH]})
    if shipsanity == Shipsanity.option_crops:
        shipsanity_locations = shipsanity_locations.union({location for location in locations_by_tag[LocationTags.SHIPSANITY_CROP]})
    if shipsanity == Shipsanity.option_full_shipment or shipsanity == Shipsanity.option_full_shipment_with_fish:
        shipsanity_locations = shipsanity_locations.union({location for location in locations_by_tag[LocationTags.SHIPSANITY_FULL_SHIPMENT]})

    filtered_shipsanity_locations = filter_disabled_locations(options, content, list(shipsanity_locations))
    randomized_locations.extend(filtered_shipsanity_locations)


def extend_cooksanity_locations(randomized_locations: List[LocationData], options: StardewValleyOptions, content: StardewContent):
    cooksanity = options.cooksanity
    if cooksanity == Cooksanity.option_none:
        return
    if cooksanity == Cooksanity.option_queen_of_sauce:
        cooksanity_locations = (location for location in locations_by_tag[LocationTags.COOKSANITY_QOS])
    else:
        cooksanity_locations = (location for location in locations_by_tag[LocationTags.COOKSANITY])

    filtered_cooksanity_locations = filter_disabled_locations(options, content, cooksanity_locations)
    randomized_locations.extend(filtered_cooksanity_locations)


def extend_chefsanity_locations(randomized_locations: List[LocationData], options: StardewValleyOptions, content: StardewContent):
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

    filtered_chefsanity_locations = filter_disabled_locations(options, content, list(chefsanity_locations_by_name.values()))
    randomized_locations.extend(filtered_chefsanity_locations)


def extend_craftsanity_locations(randomized_locations: List[LocationData], options: StardewValleyOptions, content: StardewContent):
    if options.craftsanity == Craftsanity.option_none:
        return

    craftsanity_locations = [craft for craft in locations_by_tag[LocationTags.CRAFTSANITY]]
    filtered_craftsanity_locations = filter_disabled_locations(options, content, craftsanity_locations)
    randomized_locations.extend(filtered_craftsanity_locations)


def extend_book_locations(randomized_locations: List[LocationData], content: StardewContent):
    booksanity = content.features.booksanity
    if not booksanity.is_enabled:
        return

    book_locations = []
    for book in content.find_tagged_items(ItemTag.BOOK):
        if booksanity.is_included(book):
            book_locations.append(location_table[booksanity.to_location_name(book.name)])

    book_locations.extend(location_table[booksanity.to_location_name(book)] for book in booksanity.get_randomized_lost_books())

    randomized_locations.extend(book_locations)


def extend_walnutsanity_locations(randomized_locations: List[LocationData], options: StardewValleyOptions):
    if not options.walnutsanity:
        return

    if "Puzzles" in options.walnutsanity:
        randomized_locations.extend(locations_by_tag[LocationTags.WALNUTSANITY_PUZZLE])
    if "Bushes" in options.walnutsanity:
        randomized_locations.extend(locations_by_tag[LocationTags.WALNUTSANITY_BUSH])
    if "Dig Spots" in options.walnutsanity:
        randomized_locations.extend(locations_by_tag[LocationTags.WALNUTSANITY_DIG])
    if "Repeatables" in options.walnutsanity:
        randomized_locations.extend(locations_by_tag[LocationTags.WALNUTSANITY_REPEATABLE])


def create_locations(location_collector: StardewLocationCollector,
                     bundle_rooms: List[BundleRoom],
                     options: StardewValleyOptions,
                     content: StardewContent,
                     random: Random):
    randomized_locations = []

    extend_mandatory_locations(randomized_locations, options, content)
    extend_bundle_locations(randomized_locations, bundle_rooms)
    extend_backpack_locations(randomized_locations, options)

    if options.tool_progression & ToolProgression.option_progressive:
        randomized_locations.extend(locations_by_tag[LocationTags.TOOL_UPGRADE])

    extend_elevator_locations(randomized_locations, options)

    skill_progression = content.features.skill_progression
    if skill_progression.is_progressive:
        for skill in content.skills.values():
            randomized_locations.extend([location_table[location_name] for _, location_name in skill_progression.get_randomized_level_names_by_level(skill)])
            if skill_progression.is_mastery_randomized(skill):
                randomized_locations.append(location_table[skill.mastery_name])

    if options.building_progression & BuildingProgression.option_progressive:
        for location in locations_by_tag[LocationTags.BUILDING_BLUEPRINT]:
            if location.mod_name is None or location.mod_name in options.mods:
                randomized_locations.append(location_table[location.name])

    if options.arcade_machine_locations != ArcadeMachineLocations.option_disabled:
        randomized_locations.extend(locations_by_tag[LocationTags.ARCADE_MACHINE_VICTORY])

    if options.arcade_machine_locations == ArcadeMachineLocations.option_full_shuffling:
        randomized_locations.extend(locations_by_tag[LocationTags.ARCADE_MACHINE])

    extend_cropsanity_locations(randomized_locations, content)
    extend_fishsanity_locations(randomized_locations, content, random)
    extend_museumsanity_locations(randomized_locations, options, random)
    extend_friendsanity_locations(randomized_locations, content)

    extend_festival_locations(randomized_locations, options, random)
    extend_special_order_locations(randomized_locations, options, content)
    extend_walnut_purchase_locations(randomized_locations, options)

    extend_monstersanity_locations(randomized_locations, options, content)
    extend_shipsanity_locations(randomized_locations, options, content)
    extend_cooksanity_locations(randomized_locations, options, content)
    extend_chefsanity_locations(randomized_locations, options, content)
    extend_craftsanity_locations(randomized_locations, options, content)
    extend_quests_locations(randomized_locations, options, content)
    extend_book_locations(randomized_locations, content)
    extend_walnutsanity_locations(randomized_locations, options)

    # Mods
    extend_situational_quest_locations(randomized_locations, options)

    for location_data in randomized_locations:
        location_collector(location_data.name, location_data.code, location_data.region)


def filter_deprecated_locations(locations: Iterable[LocationData]) -> Iterable[LocationData]:
    return [location for location in locations if LocationTags.DEPRECATED not in location.tags]


def filter_farm_type(options: StardewValleyOptions, locations: Iterable[LocationData]) -> Iterable[LocationData]:
    # On Meadowlands, "Feeding Animals" replaces "Raising Animals"
    if options.farm_type == FarmType.option_meadowlands:
        return (location for location in locations if location.name != Quest.raising_animals)
    else:
        return (location for location in locations if location.name != Quest.feeding_animals)


def filter_ginger_island(options: StardewValleyOptions, locations: Iterable[LocationData]) -> Iterable[LocationData]:
    include_island = options.exclude_ginger_island == ExcludeGingerIsland.option_false
    return (location for location in locations if include_island or LocationTags.GINGER_ISLAND not in location.tags)


def filter_qi_order_locations(options: StardewValleyOptions, locations: Iterable[LocationData]) -> Iterable[LocationData]:
    include_qi_orders = options.special_order_locations & SpecialOrderLocations.value_qi
    return (location for location in locations if include_qi_orders or LocationTags.REQUIRES_QI_ORDERS not in location.tags)


def filter_masteries_locations(content: StardewContent, locations: Iterable[LocationData]) -> Iterable[LocationData]:
    # FIXME Remove once recipes are handled by the content packs
    if content.features.skill_progression.are_masteries_shuffled:
        return locations
    return (location for location in locations if LocationTags.REQUIRES_MASTERIES not in location.tags)


def filter_modded_locations(options: StardewValleyOptions, locations: Iterable[LocationData]) -> Iterable[LocationData]:
    return (location for location in locations if location.mod_name is None or location.mod_name in options.mods)


def filter_disabled_locations(options: StardewValleyOptions, content: StardewContent, locations: Iterable[LocationData]) -> Iterable[LocationData]:
    locations_deprecated_filter = filter_deprecated_locations(locations)
    locations_farm_filter = filter_farm_type(options, locations_deprecated_filter)
    locations_island_filter = filter_ginger_island(options, locations_farm_filter)
    locations_qi_filter = filter_qi_order_locations(options, locations_island_filter)
    locations_masteries_filter = filter_masteries_locations(content, locations_qi_filter)
    locations_mod_filter = filter_modded_locations(options, locations_masteries_filter)
    return locations_mod_filter
