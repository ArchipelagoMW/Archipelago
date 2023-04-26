import csv
import enum
from dataclasses import dataclass
from random import Random
from typing import Optional, Dict, Protocol, List, FrozenSet

from . import options, data
from .data.fish_data import legendary_fish, special_fish, all_fish
from .data.museum_data import all_museum_items
from .data.villagers_data import all_villagers

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
    THE_MINES_ELEVATOR = enum.auto()
    SKILL_LEVEL = enum.auto()
    FARMING_LEVEL = enum.auto()
    FISHING_LEVEL = enum.auto()
    FORAGING_LEVEL = enum.auto()
    COMBAT_LEVEL = enum.auto()
    MINING_LEVEL = enum.auto()
    BUILDING_BLUEPRINT = enum.auto()
    QUEST = enum.auto()
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
    SPECIAL_ORDER_BOARD = enum.auto()
    SPECIAL_ORDER_QI = enum.auto()
    GINGER_ISLAND = enum.auto()
    WALNUT_PURCHASE = enum.auto


@dataclass(frozen=True)
class LocationData:
    code_without_offset: Optional[int]
    region: str
    name: str
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
                             frozenset(LocationTags[group]
                                       for group in location["tags"].split(",")
                                       if group))
                for location in reader]


events_locations = [
    LocationData(None, "Stardew Valley", "Succeed Grandpa's Evaluation"),
    LocationData(None, "Community Center", "Complete Community Center"),
    LocationData(None, "The Mines - Floor 120", "Reach the Bottom of The Mines"),
    LocationData(None, "Skull Cavern", "Complete Quest Cryptic Note"),
    LocationData(None, "Stardew Valley", "Catch Every Fish"),
    LocationData(None, "Stardew Valley", "Complete the Museum Collection"),
    LocationData(None, "Stardew Valley", "Full House"),
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


def extend_help_wanted_quests(randomized_locations: List[LocationData], desired_number_of_quests: int):
    for i in range(0, desired_number_of_quests):
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


def extend_fishsanity_locations(randomized_locations: List[LocationData], world_options, random: Random):
    prefix = "Fishsanity: "
    include_ginger_island = world_options[options.ExcludeGingerIsland] == options.ExcludeGingerIsland.option_false
    if world_options[options.Fishsanity] == options.Fishsanity.option_none:
        return
    elif world_options[options.Fishsanity] == options.Fishsanity.option_legendaries:
        randomized_locations.extend(location_table[f"{prefix}{legendary.name}"] for legendary in legendary_fish)
    elif world_options[options.Fishsanity] == options.Fishsanity.option_special:
        randomized_locations.extend(location_table[f"{prefix}{special.name}"] for special in special_fish)
    elif world_options[options.Fishsanity] == options.Fishsanity.option_randomized:
        fish_locations = [location_table[f"{prefix}{fish.name}"] for fish in all_fish if random.random() < 0.4]
        randomized_locations.extend(location for location in fish_locations
                                    if include_ginger_island or LocationTags.GINGER_ISLAND not in location.tags)
    elif world_options[options.Fishsanity] == options.Fishsanity.option_all:
        fish_locations = [location_table[f"{prefix}{fish.name}"] for fish in all_fish]
        randomized_locations.extend(location for location in fish_locations
                                    if include_ginger_island or LocationTags.GINGER_ISLAND not in location.tags)


def extend_museumsanity_locations(randomized_locations: List[LocationData], museumsanity: int, random: Random):
    prefix = "Museumsanity: "
    if museumsanity == options.Museumsanity.option_none:
        return
    elif museumsanity == options.Museumsanity.option_milestones:
        randomized_locations.extend(locations_by_tag[LocationTags.MUSEUM_MILESTONES])
    elif museumsanity == options.Museumsanity.option_randomized:
        randomized_locations.extend(location_table[f"{prefix}{museum_item.name}"]
                                    for museum_item in all_museum_items if random.random() < 0.4)
    elif museumsanity == options.Museumsanity.option_all:
        randomized_locations.extend(location_table[f"{prefix}{museum_item.name}"] for museum_item in all_museum_items)


def extend_friendsanity_locations(randomized_locations: List[LocationData], world_options):
    if world_options[options.Friendsanity] == options.Friendsanity.option_none:
        return

    exclude_leo = world_options[options.ExcludeGingerIsland] == options.ExcludeGingerIsland.option_true
    exclude_non_bachelors = world_options[options.Friendsanity] == options.Friendsanity.option_bachelors
    exclude_locked_villagers = world_options[options.Friendsanity] == options.Friendsanity.option_starting_npcs or \
                               world_options[options.Friendsanity] == options.Friendsanity.option_bachelors
    exclude_post_marriage_hearts = world_options[options.Friendsanity] != options.Friendsanity.option_all_with_marriage
    for villager in all_villagers:
        if not villager.available and exclude_locked_villagers:
            continue
        if not villager.bachelor and exclude_non_bachelors:
            continue
        if villager.name == "Leo" and exclude_leo:
            continue
        for heart in range(1, 15):
            if villager.bachelor and exclude_post_marriage_hearts and heart > 8:
                continue
            if villager.bachelor or heart < 11:
                randomized_locations.append(location_table[f"Friendsanity: {villager.name} {heart} <3"])
    if not exclude_non_bachelors:
        for heart in range(1, 6):
            randomized_locations.append(location_table[f"Friendsanity: Pet {heart} <3"])


def extend_festival_locations(randomized_locations: List[LocationData], festival_option: int):
    if festival_option == options.FestivalLocations.option_disabled:
        return

    randomized_locations.append(location_table["Egg Hunt Victory"])
    randomized_locations.append(location_table["Egg Festival: Strawberry Seeds"])
    randomized_locations.append(location_table["Dance with someone"])
    randomized_locations.append(location_table["Rarecrow #5 (Woman)"])
    randomized_locations.append(location_table["Luau Soup"])
    randomized_locations.append(location_table["Dance of the Moonlight Jellies"])
    randomized_locations.append(location_table["Smashing Stone"])
    randomized_locations.append(location_table["Grange Display"])
    randomized_locations.append(location_table["Rarecrow #1 (Turnip Head)"])
    randomized_locations.append(location_table["Fair Stardrop"])
    randomized_locations.append(location_table["Spirit's Eve Maze"])
    randomized_locations.append(location_table["Rarecrow #2 (Witch)"])
    randomized_locations.append(location_table["Win Fishing Competition"])
    randomized_locations.append(location_table["Rarecrow #4 (Snowman)"])
    randomized_locations.append(location_table["Mermaid Pearl"])
    randomized_locations.append(location_table["Rarecrow #7 (Tanuki)"])
    randomized_locations.append(location_table["Rarecrow #8 (Tribal Mask)"])
    randomized_locations.append(location_table["Secret Santa"])
    randomized_locations.append(location_table["Lupini: Red Eagle"])
    randomized_locations.append(location_table["Lupini: Portrait Of A Mermaid"])
    randomized_locations.append(location_table["Lupini: Solar Kingdom"])
    extend_hard_festival_locations(randomized_locations, festival_option)


def extend_hard_festival_locations(randomized_locations, festival_option: int):
    if festival_option != options.FestivalLocations.option_hard:
        return
    randomized_locations.append(location_table["Cone Hat"])
    randomized_locations.append(location_table["Iridium Fireplace"])
    randomized_locations.append(location_table["Lupini: Clouds"])
    randomized_locations.append(location_table["Lupini: 1000 Years From Now"])
    randomized_locations.append(location_table["Lupini: Three Trees"])
    randomized_locations.append(location_table["Lupini: The Serpent"])
    randomized_locations.append(location_table["Lupini: 'Tropical Fish #173'"])
    randomized_locations.append(location_table["Lupini: Land Of Clay"])


def extend_special_order_locations(randomized_locations: List[LocationData], world_options):
    if world_options[options.SpecialOrderLocations] == options.SpecialOrderLocations.option_disabled:
        return

    include_island = world_options[options.ExcludeGingerIsland] == options.ExcludeGingerIsland.option_false
    board_locations = [location for location in locations_by_tag[LocationTags.SPECIAL_ORDER_BOARD]
                       if include_island or LocationTags.GINGER_ISLAND not in location.tags]
    randomized_locations.extend(board_locations)
    if world_options[options.SpecialOrderLocations] == options.SpecialOrderLocations.option_board_qi and include_island:
        randomized_locations.extend(locations_by_tag[LocationTags.SPECIAL_ORDER_QI])


def extend_walnut_purchase_locations(randomized_locations: List[LocationData], world_options):
    if world_options[options.ExcludeGingerIsland] == options.ExcludeGingerIsland.option_true:
        return
    randomized_locations.append(location_table["Repair Ticket Machine"])
    randomized_locations.append(location_table["Repair Boat Hull"])
    randomized_locations.append(location_table["Repair Boat Anchor"])
    randomized_locations.extend(locations_by_tag[LocationTags.WALNUT_PURCHASE])


def create_locations(location_collector: StardewLocationCollector,
                     world_options: options.StardewOptions,
                     random: Random):
    randomized_locations = []

    include_island = world_options[options.ExcludeGingerIsland] == options.ExcludeGingerIsland.option_false
    mandatory_locations = [location for location in locations_by_tag[LocationTags.MANDATORY]
                           if include_island or LocationTags.GINGER_ISLAND not in location.tags]
    randomized_locations.extend(mandatory_locations)

    if not world_options[options.BackpackProgression] == options.BackpackProgression.option_vanilla:
        randomized_locations.extend(locations_by_tag[LocationTags.BACKPACK])

    if not world_options[options.ToolProgression] == options.ToolProgression.option_vanilla:
        randomized_locations.extend(locations_by_tag[LocationTags.TOOL_UPGRADE])

    if not world_options[options.TheMinesElevatorsProgression] == options.TheMinesElevatorsProgression.option_vanilla:
        randomized_locations.extend(locations_by_tag[LocationTags.THE_MINES_ELEVATOR])

    if not world_options[options.SkillProgression] == options.SkillProgression.option_vanilla:
        randomized_locations.extend(locations_by_tag[LocationTags.SKILL_LEVEL])

    if not world_options[options.BuildingProgression] == options.BuildingProgression.option_vanilla:
        randomized_locations.extend(locations_by_tag[LocationTags.BUILDING_BLUEPRINT])

    if not world_options[options.ArcadeMachineLocations] == options.ArcadeMachineLocations.option_disabled:
        randomized_locations.extend(locations_by_tag[LocationTags.ARCADE_MACHINE_VICTORY])

    if world_options[options.ArcadeMachineLocations] == options.ArcadeMachineLocations.option_full_shuffling:
        randomized_locations.extend(locations_by_tag[LocationTags.ARCADE_MACHINE])

    extend_help_wanted_quests(randomized_locations, world_options[options.HelpWantedLocations])
    extend_fishsanity_locations(randomized_locations, world_options, random)
    extend_museumsanity_locations(randomized_locations, world_options[options.Museumsanity], random)
    extend_friendsanity_locations(randomized_locations, world_options)
    extend_festival_locations(randomized_locations, world_options[options.FestivalLocations])
    extend_special_order_locations(randomized_locations, world_options)
    extend_walnut_purchase_locations(randomized_locations, world_options)

    for location_data in randomized_locations:
        location_collector(location_data.name, location_data.code, location_data.region)
