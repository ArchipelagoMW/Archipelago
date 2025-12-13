import csv
import enum
import logging
from dataclasses import dataclass
from random import Random
from typing import Optional, Dict, Protocol, List, Iterable

from . import data
from .bundles.bundle_room import BundleRoom
from .content.game_content import StardewContent
from .content.vanilla.ginger_island import ginger_island_content_pack
from .content.vanilla.qi_board import qi_board_content_pack
from .data.game_item import ItemTag
from .data.museum_data import all_museum_items
from .mods.mod_data import ModNames
from .options import ArcadeMachineLocations, SpecialOrderLocations, Museumsanity, \
    FestivalLocations, ElevatorProgression, BackpackProgression, FarmType
from .options import StardewValleyOptions, Craftsanity, Chefsanity, Cooksanity, Shipsanity, Monstersanity
from .options.options import BackpackSize, Moviesanity, Eatsanity, IncludeEndgameLocations, Friendsanity
from .strings.ap_names.ap_option_names import WalnutsanityOptionName, SecretsanityOptionName, EatsanityOptionName, ChefsanityOptionName, StartWithoutOptionName
from .strings.backpack_tiers import Backpack
from .strings.goal_names import Goal
from .strings.quest_names import ModQuest, Quest
from .strings.region_names import Region, LogicRegion
from .strings.villager_names import NPC

LOCATION_CODE_OFFSET = 717000

logger = logging.getLogger(__name__)


class LocationTags(enum.Enum):
    MANDATORY = enum.auto()
    BUNDLE = enum.auto()
    TRASH_BEAR = enum.auto()
    COMMUNITY_CENTER_BUNDLE = enum.auto()
    CRAFTS_ROOM_BUNDLE = enum.auto()
    PANTRY_BUNDLE = enum.auto()
    FISH_TANK_BUNDLE = enum.auto()
    BOILER_ROOM_BUNDLE = enum.auto()
    BULLETIN_BOARD_BUNDLE = enum.auto()
    VAULT_BUNDLE = enum.auto()
    COMMUNITY_CENTER_ROOM = enum.auto()
    RACCOON_BUNDLES = enum.auto()
    MEME_BUNDLE = enum.auto()
    BACKPACK = enum.auto()
    BACKPACK_TIER = enum.auto()
    SPLIT_BACKPACK = enum.auto()
    TOOL_UPGRADE = enum.auto()
    HOE_UPGRADE = enum.auto()
    PICKAXE_UPGRADE = enum.auto()
    AXE_UPGRADE = enum.auto()
    WATERING_CAN_UPGRADE = enum.auto()
    TRASH_CAN_UPGRADE = enum.auto()
    FISHING_ROD_UPGRADE = enum.auto()
    PAN_UPGRADE = enum.auto()
    STARTING_TOOLS = enum.auto()
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
    CRAFTSANITY_CRAFT = enum.auto()
    CRAFTSANITY_RECIPE = enum.auto()
    BOOKSANITY = enum.auto()
    BOOKSANITY_POWER = enum.auto()
    BOOKSANITY_SKILL = enum.auto()
    BOOKSANITY_LOST = enum.auto()
    SECRETSANITY = enum.auto()
    EASY_SECRET = enum.auto()
    FISHING_SECRET = enum.auto()
    DIFFICULT_SECRET = enum.auto()
    SECRET_NOTE = enum.auto()
    REPLACES_PREVIOUS_LOCATION = enum.auto()
    ANY_MOVIE = enum.auto()
    MOVIE = enum.auto()
    MOVIE_SNACK = enum.auto()
    HATSANITY = enum.auto()
    HAT_EASY = enum.auto()
    HAT_TAILORING = enum.auto()
    HAT_MEDIUM = enum.auto()
    HAT_DIFFICULT = enum.auto()
    HAT_RNG = enum.auto()
    HAT_NEAR_PERFECTION = enum.auto()
    HAT_POST_PERFECTION = enum.auto()
    HAT_IMPOSSIBLE = enum.auto()
    EATSANITY = enum.auto()
    EATSANITY_CROP = enum.auto()
    EATSANITY_COOKING = enum.auto()
    EATSANITY_FISH = enum.auto()
    EATSANITY_ARTISAN = enum.auto()
    EATSANITY_SHOP = enum.auto()
    EATSANITY_POISONOUS = enum.auto()
    ENDGAME_LOCATIONS = enum.auto()
    REQUIRES_FRIENDSANITY = enum.auto()
    REQUIRES_FRIENDSANITY_MARRIAGE = enum.auto()

    BEACH_FARM = enum.auto()
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
    code_without_offset: int | None
    region: str
    name: str
    content_packs: frozenset[str] = frozenset()
    """All the content packs required for this location to be active."""
    tags: frozenset[LocationTags] = frozenset()

    @property
    def code(self) -> int | None:
        return LOCATION_CODE_OFFSET + self.code_without_offset if self.code_without_offset is not None else None


class StardewLocationCollector(Protocol):
    def __call__(self, name: str, code: Optional[int], region: str) -> None:
        raise NotImplementedError


def load_location_csv() -> List[LocationData]:
    from importlib.resources import files

    locations = []
    with files(data).joinpath("locations.csv").open() as file:
        location_reader = csv.DictReader(file)
        for location in location_reader:
            location_id = int(location["id"]) if location["id"] else None
            location_name = location["name"]
            csv_tags = [LocationTags[tag] for tag in location["tags"].split(",") if tag]
            tags = frozenset(csv_tags)
            csv_content_packs = [cp for cp in location["content_packs"].split(",") if cp]
            content_packs = frozenset(csv_content_packs)

            assert len(csv_tags) == len(tags), f"Location '{location_name}' has duplicate tags: {csv_tags}"
            assert len(csv_content_packs) == len(content_packs)

            if LocationTags.GINGER_ISLAND in tags:
                content_packs |= {ginger_island_content_pack.name}
            if LocationTags.SPECIAL_ORDER_QI in tags or LocationTags.REQUIRES_QI_ORDERS in tags:
                content_packs |= {qi_board_content_pack.name}

            locations.append(LocationData(location_id, location["region"], location_name, content_packs, tags))

    return locations


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
    LocationData(None, Region.farm, Goal.mad_hatter),
    LocationData(None, Region.farm, Goal.ultimate_foodie),
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
    if options.quest_locations.has_no_story_quests():
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


def extend_building_locations(randomized_locations: List[LocationData], content: StardewContent):
    building_progression = content.features.building_progression
    if not building_progression.is_progressive:
        return

    for building in content.farm_buildings.values():
        if building.name in building_progression.starting_buildings:
            continue

        location_name = building_progression.to_location_name(building.name)
        randomized_locations.append(location_table[location_name])


def extend_festival_locations(randomized_locations: List[LocationData], options: StardewValleyOptions, random: Random):
    if options.festival_locations == FestivalLocations.option_disabled:
        return

    festival_locations = locations_by_tag[LocationTags.FESTIVAL]
    if not options.museumsanity:
        festival_locations = [location for location in festival_locations if location.name not in ("Rarecrow #7 (Tanuki)", "Rarecrow #8 (Tribal Mask)")]

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

    if content.is_enabled(qi_board_content_pack):
        include_arcade = options.arcade_machine_locations != ArcadeMachineLocations.option_disabled
        qi_orders = [location for location in locations_by_tag[LocationTags.SPECIAL_ORDER_QI] if
                     include_arcade or LocationTags.JUNIMO_KART not in location.tags]
        randomized_locations.extend(qi_orders)


def extend_walnut_purchase_locations(randomized_locations: List[LocationData], content: StardewContent):
    if not content.is_enabled(ginger_island_content_pack):
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


def extend_situational_quest_locations(randomized_locations: List[LocationData], options: StardewValleyOptions, content: StardewContent):
    if options.quest_locations.has_no_story_quests():
        return
    if ModNames.distant_lands in content.registered_packs:
        if ModNames.alecto in content.registered_packs:
            randomized_locations.append(location_table[f"Quest: {ModQuest.WitchOrder}"])
        else:
            randomized_locations.append(location_table[f"Quest: {ModQuest.CorruptedCropsTask}"])


def extend_bundle_locations(randomized_locations: List[LocationData], bundle_rooms: List[BundleRoom]):
    for room in bundle_rooms:
        room_location = f"Complete {room.name}"
        if room_location in location_table:
            randomized_locations.append(location_table[room_location])
        for bundle in room.bundles:
            randomized_locations.append(location_table[bundle.name])


def extend_trash_bear_locations(randomized_locations: List[LocationData], trash_bear_requests: Dict[str, List[str]]):
    for request_type in trash_bear_requests:
        randomized_locations.append(location_table[f"Trash Bear {request_type}"])


def extend_backpack_locations(randomized_locations: List[LocationData], options: StardewValleyOptions, content: StardewContent):
    if options.backpack_progression == BackpackProgression.option_vanilla:
        return

    no_start_backpack = StartWithoutOptionName.backpack in options.start_without
    if options.backpack_size == BackpackSize.option_12:
        backpack_locations = [location for location in locations_by_tag[LocationTags.BACKPACK_TIER] if no_start_backpack or LocationTags.STARTING_TOOLS not in location.tags]
    else:
        num_per_tier = options.backpack_size.count_per_tier()
        backpack_tier_names = Backpack.get_purchasable_tiers(ModNames.big_backpack in content.registered_packs, no_start_backpack)
        backpack_locations = []
        for tier in backpack_tier_names:
            for i in range(1, num_per_tier + 1):
                backpack_locations.append(location_table[f"{tier} {i}"])

    filtered_backpack_locations = filter_modded_locations(backpack_locations, content)
    randomized_locations.extend(filtered_backpack_locations)


def extend_elevator_locations(randomized_locations: List[LocationData], options: StardewValleyOptions, content: StardewContent):
    if options.elevator_progression == ElevatorProgression.option_vanilla:
        return
    elevator_locations = [location for location in locations_by_tag[LocationTags.ELEVATOR]]
    filtered_elevator_locations = filter_modded_locations(elevator_locations, content)
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
    if shipsanity == Shipsanity.option_fish or shipsanity == Shipsanity.option_crops_and_fish or shipsanity == Shipsanity.option_full_shipment_with_fish:
        shipsanity_locations = shipsanity_locations.union({location for location in locations_by_tag[LocationTags.SHIPSANITY_FISH]})
    if shipsanity == Shipsanity.option_crops or shipsanity == Shipsanity.option_crops_and_fish:
        shipsanity_locations = shipsanity_locations.union({location for location in locations_by_tag[LocationTags.SHIPSANITY_CROP]})
    if shipsanity == Shipsanity.option_full_shipment or shipsanity == Shipsanity.option_full_shipment_with_fish:
        shipsanity_locations = shipsanity_locations.union({location for location in locations_by_tag[LocationTags.SHIPSANITY_FULL_SHIPMENT]})

    filtered_shipsanity_locations = filter_disabled_locations(options, content, sorted(list(shipsanity_locations), key=lambda x: x.name))
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
    if chefsanity == Chefsanity.preset_none:
        return

    chefsanity_locations_by_name = {}  # Dictionary to not make duplicates

    if ChefsanityOptionName.queen_of_sauce in chefsanity:
        chefsanity_locations_by_name.update({location.name: location for location in locations_by_tag[LocationTags.CHEFSANITY_QOS]})
    if ChefsanityOptionName.purchases in chefsanity:
        chefsanity_locations_by_name.update({location.name: location for location in locations_by_tag[LocationTags.CHEFSANITY_PURCHASE]})
    if ChefsanityOptionName.friendship in chefsanity:
        chefsanity_locations_by_name.update({location.name: location for location in locations_by_tag[LocationTags.CHEFSANITY_FRIENDSHIP]})
    if ChefsanityOptionName.skills in chefsanity:
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

    if WalnutsanityOptionName.puzzles in options.walnutsanity:
        randomized_locations.extend(locations_by_tag[LocationTags.WALNUTSANITY_PUZZLE])
    if WalnutsanityOptionName.bushes in options.walnutsanity:
        randomized_locations.extend(locations_by_tag[LocationTags.WALNUTSANITY_BUSH])
    if WalnutsanityOptionName.dig_spots in options.walnutsanity:
        randomized_locations.extend(locations_by_tag[LocationTags.WALNUTSANITY_DIG])
    if WalnutsanityOptionName.repeatables in options.walnutsanity:
        randomized_locations.extend(locations_by_tag[LocationTags.WALNUTSANITY_REPEATABLE])


def extend_movies_locations(randomized_locations: List[LocationData], options: StardewValleyOptions, content: StardewContent):
    if options.moviesanity == Moviesanity.option_none:
        return

    locations = []
    if options.moviesanity == Moviesanity.option_one:
        locations.extend(locations_by_tag[LocationTags.ANY_MOVIE])
    if options.moviesanity >= Moviesanity.option_all_movies:
        locations.extend(locations_by_tag[LocationTags.MOVIE])
    if options.moviesanity >= Moviesanity.option_all_movies_and_all_snacks:
        locations.extend(locations_by_tag[LocationTags.MOVIE_SNACK])
    filtered_locations = filter_disabled_locations(options, content, locations)
    randomized_locations.extend(filtered_locations)


def extend_secrets_locations(randomized_locations: List[LocationData], options: StardewValleyOptions, content: StardewContent):
    if not options.secretsanity:
        return

    locations = []
    if SecretsanityOptionName.easy in options.secretsanity:
        locations.extend(locations_by_tag[LocationTags.EASY_SECRET])
    if SecretsanityOptionName.fishing in options.secretsanity:
        locations.extend(locations_by_tag[LocationTags.FISHING_SECRET])
    if SecretsanityOptionName.difficult in options.secretsanity:
        locations.extend(locations_by_tag[LocationTags.DIFFICULT_SECRET])
    if SecretsanityOptionName.secret_notes in options.secretsanity:
        locations.extend(locations_by_tag[LocationTags.SECRET_NOTE])
        for location_dupe in locations_by_tag[LocationTags.REPLACES_PREVIOUS_LOCATION]:
            second_part_of_name = location_dupe.name.split(":")[-1]
            for location in randomized_locations:
                second_part_of_dupe_name = location.name.split(":")[-1]
                if second_part_of_name == second_part_of_dupe_name:
                    randomized_locations.remove(location)
    filtered_locations = filter_disabled_locations(options, content, locations)
    randomized_locations.extend(filtered_locations)


def extend_hats_locations(randomized_locations: List[LocationData], content: StardewContent):
    hatsanity = content.features.hatsanity
    if not hatsanity.is_enabled:
        return

    for hat in content.hats.values():
        if not hatsanity.is_included(hat):
            continue

        randomized_locations.append(location_table[hatsanity.to_location_name(hat)])


def eatsanity_item_is_included(location: LocationData, options: StardewValleyOptions, content: StardewContent) -> bool:
    eat_prefix = "Eat "
    drink_prefix = "Drink "
    if location.name.startswith(eat_prefix):
        item_name = location.name[len(eat_prefix):]
    elif location.name.startswith(drink_prefix):
        item_name = location.name[len(drink_prefix):]
    else:
        raise Exception(f"Eatsanity Location does not have a recognized prefix: '{location.name}'")

    # if not item_name in content.game_items:
    #     return False
    if EatsanityOptionName.poisonous in options.eatsanity.value:
        return True
    if location in locations_by_tag[LocationTags.EATSANITY_POISONOUS]:
        return False
    return True


def extend_eatsanity_locations(randomized_locations: List[LocationData], options: StardewValleyOptions, content: StardewContent):
    if options.eatsanity.value == Eatsanity.preset_none:
        return

    eatsanity_locations = []
    if EatsanityOptionName.crops in options.eatsanity:
        eatsanity_locations.extend(locations_by_tag[LocationTags.EATSANITY_CROP])
    if EatsanityOptionName.cooking in options.eatsanity:
        eatsanity_locations.extend(locations_by_tag[LocationTags.EATSANITY_COOKING])
    if EatsanityOptionName.fish in options.eatsanity:
        eatsanity_locations.extend(locations_by_tag[LocationTags.EATSANITY_FISH])
    if EatsanityOptionName.artisan in options.eatsanity:
        eatsanity_locations.extend(locations_by_tag[LocationTags.EATSANITY_ARTISAN])
    if EatsanityOptionName.shop in options.eatsanity:
        eatsanity_locations.extend(locations_by_tag[LocationTags.EATSANITY_SHOP])

    eatsanity_locations = [location for location in eatsanity_locations if eatsanity_item_is_included(location, options, content)]
    eatsanity_locations = filter_disabled_locations(options, content, eatsanity_locations)
    randomized_locations.extend(eatsanity_locations)


def extend_endgame_locations(randomized_locations: List[LocationData], options: StardewValleyOptions, content: StardewContent):
    if options.include_endgame_locations.value == IncludeEndgameLocations.option_false:
        return

    has_friendsanity_marriage = options.friendsanity == Friendsanity.option_all_with_marriage
    has_friendsanity = (not has_friendsanity_marriage) and options.friendsanity != Friendsanity.option_none

    endgame_locations = []
    endgame_locations.extend(locations_by_tag[LocationTags.ENDGAME_LOCATIONS])

    endgame_locations = [location for location in endgame_locations if
                         LocationTags.REQUIRES_FRIENDSANITY_MARRIAGE not in location.tags or has_friendsanity_marriage]
    endgame_locations = [location for location in endgame_locations if LocationTags.REQUIRES_FRIENDSANITY not in location.tags or has_friendsanity]
    endgame_locations = filter_disabled_locations(options, content, endgame_locations)
    randomized_locations.extend(endgame_locations)


def extend_filler_locations(randomized_locations: List[LocationData], options: StardewValleyOptions, content: StardewContent):
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    i = 1
    while len(randomized_locations) < 90:
        location_name = f"Traveling Merchant Sunday Item {i}"
        while any(location.name == location_name for location in randomized_locations):
            i += 1
            location_name = f"Traveling Merchant Sunday Item {i}"
        logger.debug(f"Player too few locations, adding Traveling Merchant Items #{i}")
        for day in days:
            location_name = f"Traveling Merchant {day} Item {i}"
            randomized_locations.append(location_table[location_name])



def create_locations(location_collector: StardewLocationCollector,
                     bundle_rooms: List[BundleRoom],
                     trash_bear_requests: Dict[str, List[str]],
                     options: StardewValleyOptions,
                     content: StardewContent,
                     random: Random):
    randomized_locations = []

    extend_mandatory_locations(randomized_locations, options, content)
    extend_bundle_locations(randomized_locations, bundle_rooms)
    extend_trash_bear_locations(randomized_locations, trash_bear_requests)
    extend_backpack_locations(randomized_locations, options, content)

    if content.features.tool_progression.is_progressive:
        randomized_locations.extend(locations_by_tag[LocationTags.TOOL_UPGRADE])

    extend_elevator_locations(randomized_locations, options, content)

    skill_progression = content.features.skill_progression
    if skill_progression.is_progressive:
        for skill in content.skills.values():
            randomized_locations.extend([location_table[location_name] for _, location_name in skill_progression.get_randomized_level_names_by_level(skill)])
            if skill_progression.is_mastery_randomized(skill):
                randomized_locations.append(location_table[skill.mastery_name])

    extend_building_locations(randomized_locations, content)

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
    extend_walnut_purchase_locations(randomized_locations, content)

    extend_monstersanity_locations(randomized_locations, options, content)
    extend_shipsanity_locations(randomized_locations, options, content)
    extend_cooksanity_locations(randomized_locations, options, content)
    extend_chefsanity_locations(randomized_locations, options, content)
    extend_craftsanity_locations(randomized_locations, options, content)
    extend_quests_locations(randomized_locations, options, content)
    extend_book_locations(randomized_locations, content)
    extend_walnutsanity_locations(randomized_locations, options)
    extend_movies_locations(randomized_locations, options, content)
    extend_secrets_locations(randomized_locations, options, content)
    extend_hats_locations(randomized_locations, content)
    extend_eatsanity_locations(randomized_locations, options, content)
    extend_endgame_locations(randomized_locations, options, content)

    # Mods
    extend_situational_quest_locations(randomized_locations, options, content)

    extend_filler_locations(randomized_locations, options, content)

    for location_data in randomized_locations:
        location_collector(location_data.name, location_data.code, location_data.region)


def filter_deprecated_locations(locations: Iterable[LocationData]) -> Iterable[LocationData]:
    return [location for location in locations if LocationTags.DEPRECATED not in location.tags]


def filter_animals_quest(options: StardewValleyOptions, locations: Iterable[LocationData]) -> Iterable[LocationData]:
    # On Meadowlands, "Feeding Animals" replaces "Raising Animals"
    if options.farm_type == FarmType.option_meadowlands:
        return (location for location in locations if location.name != f"Quest: {Quest.raising_animals}")
    else:
        return (location for location in locations if location.name != f"Quest: {Quest.feeding_animals}")


def filter_farm_exclusives(options: StardewValleyOptions, locations: Iterable[LocationData]) -> Iterable[LocationData]:
    # Some locations are only on specific farms
    if options.farm_type != FarmType.option_beach:
        return (location for location in locations if LocationTags.BEACH_FARM not in location.tags)
    return locations


def filter_farm_type(options: StardewValleyOptions, locations: Iterable[LocationData]) -> Iterable[LocationData]:
    animals_filter = filter_animals_quest(options, locations)
    exclusives_filter = filter_farm_exclusives(options, animals_filter)
    return exclusives_filter


def filter_ginger_island(content: StardewContent, locations: Iterable[LocationData]) -> Iterable[LocationData]:
    include_island = content.is_enabled(ginger_island_content_pack)
    return (location for location in locations if include_island or LocationTags.GINGER_ISLAND not in location.tags)


def filter_qi_order_locations(content: StardewContent, locations: Iterable[LocationData]) -> Iterable[LocationData]:
    include_qi_orders = content.is_enabled(qi_board_content_pack)
    return (location for location in locations if include_qi_orders or LocationTags.REQUIRES_QI_ORDERS not in location.tags)


def filter_masteries_locations(content: StardewContent, locations: Iterable[LocationData]) -> Iterable[LocationData]:
    # FIXME Remove once recipes are handled by the content packs
    if content.features.skill_progression.are_masteries_shuffled:
        return locations
    return (location for location in locations if LocationTags.REQUIRES_MASTERIES not in location.tags)


def filter_modded_locations(locations: Iterable[LocationData], content: StardewContent) -> Iterable[LocationData]:
    return (location for location in locations if content.are_all_enabled(location.content_packs))


def filter_disabled_locations(options: StardewValleyOptions, content: StardewContent, locations: Iterable[LocationData]) -> Iterable[LocationData]:
    locations_deprecated_filter = filter_deprecated_locations(locations)
    locations_farm_filter = filter_farm_type(options, locations_deprecated_filter)
    locations_island_filter = filter_ginger_island(content, locations_farm_filter)
    locations_qi_filter = filter_qi_order_locations(content, locations_island_filter)
    locations_masteries_filter = filter_masteries_locations(content, locations_qi_filter)
    locations_mod_filter = filter_modded_locations(locations_masteries_filter, content)
    return locations_mod_filter
