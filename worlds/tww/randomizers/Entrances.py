from collections import defaultdict
from collections.abc import Generator
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, Optional

from Fill import FillError
from Options import OptionError

from .. import Macros
from ..Locations import LOCATION_TABLE, TWWFlag, split_location_name_by_zone

if TYPE_CHECKING:
    from .. import TWWWorld


@dataclass(frozen=True)
class ZoneEntrance:
    """
    A data class that encapsulates information about a zone entrance.
    """

    entrance_name: str
    island_name: Optional[str] = None
    nested_in: Optional["ZoneExit"] = None

    @property
    def is_nested(self) -> bool:
        """
        Determine if this entrance is nested within another entrance.

        :return: `True` if the entrance is nested, `False` otherwise.
        """
        return self.nested_in is not None

    def __repr__(self) -> str:
        """
        Provide a string representation of the zone exit.

        :return: A string representing the zone exit.
        """
        return f"ZoneEntrance('{self.entrance_name}')"

    all: ClassVar[dict[str, "ZoneEntrance"]] = {}

    def __post_init__(self) -> None:
        ZoneEntrance.all[self.entrance_name] = self

        # Must be an island entrance XOR must be a nested entrance.
        assert (self.island_name is None) ^ (self.nested_in is None)


@dataclass(frozen=True)
class ZoneExit:
    """
    A data class that encapsulates information about a zone exit.
    """

    unique_name: str
    zone_name: Optional[str] = None

    def __repr__(self) -> str:
        """
        Provide a string representation of the zone exit.

        :return: A string representing the zone exit.
        """
        return f"ZoneExit('{self.unique_name}')"

    all: ClassVar[dict[str, "ZoneExit"]] = {}

    def __post_init__(self) -> None:
        ZoneExit.all[self.unique_name] = self


DUNGEON_ENTRANCES: list[ZoneEntrance] = [
    ZoneEntrance("Dungeon Entrance on Dragon Roost Island", "Dragon Roost Island"),
    ZoneEntrance("Dungeon Entrance in Forest Haven Sector", "Forest Haven"),
    ZoneEntrance("Dungeon Entrance in Tower of the Gods Sector", "Tower of the Gods Sector"),
    ZoneEntrance("Dungeon Entrance on Headstone Island", "Headstone Island"),
    ZoneEntrance("Dungeon Entrance on Gale Isle", "Gale Isle"),
]
DUNGEON_EXITS: list[ZoneExit] = [
    ZoneExit("Dragon Roost Cavern", "Dragon Roost Cavern"),
    ZoneExit("Forbidden Woods", "Forbidden Woods"),
    ZoneExit("Tower of the Gods", "Tower of the Gods"),
    ZoneExit("Earth Temple", "Earth Temple"),
    ZoneExit("Wind Temple", "Wind Temple"),
]

MINIBOSS_ENTRANCES: list[ZoneEntrance] = [
    ZoneEntrance("Miniboss Entrance in Forbidden Woods", nested_in=ZoneExit.all["Forbidden Woods"]),
    ZoneEntrance("Miniboss Entrance in Tower of the Gods", nested_in=ZoneExit.all["Tower of the Gods"]),
    ZoneEntrance("Miniboss Entrance in Earth Temple", nested_in=ZoneExit.all["Earth Temple"]),
    ZoneEntrance("Miniboss Entrance in Wind Temple", nested_in=ZoneExit.all["Wind Temple"]),
    ZoneEntrance("Miniboss Entrance in Hyrule Castle", "Tower of the Gods Sector"),
]
MINIBOSS_EXITS: list[ZoneExit] = [
    ZoneExit("Forbidden Woods Miniboss Arena"),
    ZoneExit("Tower of the Gods Miniboss Arena"),
    ZoneExit("Earth Temple Miniboss Arena"),
    ZoneExit("Wind Temple Miniboss Arena"),
    ZoneExit("Master Sword Chamber"),
]

BOSS_ENTRANCES: list[ZoneEntrance] = [
    ZoneEntrance("Boss Entrance in Dragon Roost Cavern", nested_in=ZoneExit.all["Dragon Roost Cavern"]),
    ZoneEntrance("Boss Entrance in Forbidden Woods", nested_in=ZoneExit.all["Forbidden Woods"]),
    ZoneEntrance("Boss Entrance in Tower of the Gods", nested_in=ZoneExit.all["Tower of the Gods"]),
    ZoneEntrance("Boss Entrance in Forsaken Fortress", "Forsaken Fortress Sector"),
    ZoneEntrance("Boss Entrance in Earth Temple", nested_in=ZoneExit.all["Earth Temple"]),
    ZoneEntrance("Boss Entrance in Wind Temple", nested_in=ZoneExit.all["Wind Temple"]),
]
BOSS_EXITS: list[ZoneExit] = [
    ZoneExit("Gohma Boss Arena"),
    ZoneExit("Kalle Demos Boss Arena"),
    ZoneExit("Gohdan Boss Arena"),
    ZoneExit("Helmaroc King Boss Arena"),
    ZoneExit("Jalhalla Boss Arena"),
    ZoneExit("Molgera Boss Arena"),
]

SECRET_CAVE_ENTRANCES: list[ZoneEntrance] = [
    ZoneEntrance("Secret Cave Entrance on Outset Island", "Outset Island"),
    ZoneEntrance("Secret Cave Entrance on Dragon Roost Island", "Dragon Roost Island"),
    ZoneEntrance("Secret Cave Entrance on Fire Mountain", "Fire Mountain"),
    ZoneEntrance("Secret Cave Entrance on Ice Ring Isle", "Ice Ring Isle"),
    ZoneEntrance("Secret Cave Entrance on Private Oasis", "Private Oasis"),
    ZoneEntrance("Secret Cave Entrance on Needle Rock Isle", "Needle Rock Isle"),
    ZoneEntrance("Secret Cave Entrance on Angular Isles", "Angular Isles"),
    ZoneEntrance("Secret Cave Entrance on Boating Course", "Boating Course"),
    ZoneEntrance("Secret Cave Entrance on Stone Watcher Island", "Stone Watcher Island"),
    ZoneEntrance("Secret Cave Entrance on Overlook Island", "Overlook Island"),
    ZoneEntrance("Secret Cave Entrance on Bird's Peak Rock", "Bird's Peak Rock"),
    ZoneEntrance("Secret Cave Entrance on Pawprint Isle", "Pawprint Isle"),
    ZoneEntrance("Secret Cave Entrance on Pawprint Isle Side Isle", "Pawprint Isle"),
    ZoneEntrance("Secret Cave Entrance on Diamond Steppe Island", "Diamond Steppe Island"),
    ZoneEntrance("Secret Cave Entrance on Bomb Island", "Bomb Island"),
    ZoneEntrance("Secret Cave Entrance on Rock Spire Isle", "Rock Spire Isle"),
    ZoneEntrance("Secret Cave Entrance on Shark Island", "Shark Island"),
    ZoneEntrance("Secret Cave Entrance on Cliff Plateau Isles", "Cliff Plateau Isles"),
    ZoneEntrance("Secret Cave Entrance on Horseshoe Island", "Horseshoe Island"),
    ZoneEntrance("Secret Cave Entrance on Star Island", "Star Island"),
]
SECRET_CAVE_EXITS: list[ZoneExit] = [
    ZoneExit("Savage Labyrinth", zone_name="Outset Island"),
    ZoneExit("Dragon Roost Island Secret Cave", zone_name="Dragon Roost Island"),
    ZoneExit("Fire Mountain Secret Cave", zone_name="Fire Mountain"),
    ZoneExit("Ice Ring Isle Secret Cave", zone_name="Ice Ring Isle"),
    ZoneExit("Cabana Labyrinth", zone_name="Private Oasis"),
    ZoneExit("Needle Rock Isle Secret Cave", zone_name="Needle Rock Isle"),
    ZoneExit("Angular Isles Secret Cave", zone_name="Angular Isles"),
    ZoneExit("Boating Course Secret Cave", zone_name="Boating Course"),
    ZoneExit("Stone Watcher Island Secret Cave", zone_name="Stone Watcher Island"),
    ZoneExit("Overlook Island Secret Cave", zone_name="Overlook Island"),
    ZoneExit("Bird's Peak Rock Secret Cave", zone_name="Bird's Peak Rock"),
    ZoneExit("Pawprint Isle Chuchu Cave", zone_name="Pawprint Isle"),
    ZoneExit("Pawprint Isle Wizzrobe Cave"),
    ZoneExit("Diamond Steppe Island Warp Maze Cave", zone_name="Diamond Steppe Island"),
    ZoneExit("Bomb Island Secret Cave", zone_name="Bomb Island"),
    ZoneExit("Rock Spire Isle Secret Cave", zone_name="Rock Spire Isle"),
    ZoneExit("Shark Island Secret Cave", zone_name="Shark Island"),
    ZoneExit("Cliff Plateau Isles Secret Cave", zone_name="Cliff Plateau Isles"),
    ZoneExit("Horseshoe Island Secret Cave", zone_name="Horseshoe Island"),
    ZoneExit("Star Island Secret Cave", zone_name="Star Island"),
]

SECRET_CAVE_INNER_ENTRANCES: list[ZoneEntrance] = [
    ZoneEntrance("Inner Entrance in Ice Ring Isle Secret Cave", nested_in=ZoneExit.all["Ice Ring Isle Secret Cave"]),
    ZoneEntrance(
        "Inner Entrance in Cliff Plateau Isles Secret Cave", nested_in=ZoneExit.all["Cliff Plateau Isles Secret Cave"]
    ),
]
SECRET_CAVE_INNER_EXITS: list[ZoneExit] = [
    ZoneExit("Ice Ring Isle Inner Cave"),
    ZoneExit("Cliff Plateau Isles Inner Cave"),
]

FAIRY_FOUNTAIN_ENTRANCES: list[ZoneEntrance] = [
    ZoneEntrance("Fairy Fountain Entrance on Outset Island", "Outset Island"),
    ZoneEntrance("Fairy Fountain Entrance on Thorned Fairy Island", "Thorned Fairy Island"),
    ZoneEntrance("Fairy Fountain Entrance on Eastern Fairy Island", "Eastern Fairy Island"),
    ZoneEntrance("Fairy Fountain Entrance on Western Fairy Island", "Western Fairy Island"),
    ZoneEntrance("Fairy Fountain Entrance on Southern Fairy Island", "Southern Fairy Island"),
    ZoneEntrance("Fairy Fountain Entrance on Northern Fairy Island", "Northern Fairy Island"),
]
FAIRY_FOUNTAIN_EXITS: list[ZoneExit] = [
    ZoneExit("Outset Fairy Fountain"),
    ZoneExit("Thorned Fairy Fountain", zone_name="Thorned Fairy Island"),
    ZoneExit("Eastern Fairy Fountain", zone_name="Eastern Fairy Island"),
    ZoneExit("Western Fairy Fountain", zone_name="Western Fairy Island"),
    ZoneExit("Southern Fairy Fountain", zone_name="Southern Fairy Island"),
    ZoneExit("Northern Fairy Fountain", zone_name="Northern Fairy Island"),
]

DUNGEON_INNER_EXITS: list[ZoneExit] = (
    MINIBOSS_EXITS
    + BOSS_EXITS
)

ALL_ENTRANCES: list[ZoneEntrance] = (
    DUNGEON_ENTRANCES
    + MINIBOSS_ENTRANCES
    + BOSS_ENTRANCES
    + SECRET_CAVE_ENTRANCES
    + SECRET_CAVE_INNER_ENTRANCES
    + FAIRY_FOUNTAIN_ENTRANCES
)
ALL_EXITS: list[ZoneExit] = (
    DUNGEON_EXITS
    + MINIBOSS_EXITS
    + BOSS_EXITS
    + SECRET_CAVE_EXITS
    + SECRET_CAVE_INNER_EXITS
    + FAIRY_FOUNTAIN_EXITS
)

ENTRANCE_RANDOMIZABLE_ITEM_LOCATION_TYPES: list[TWWFlag] = [
    TWWFlag.DUNGEON,
    TWWFlag.PZL_CVE,
    TWWFlag.CBT_CVE,
    TWWFlag.SAVAGE,
    TWWFlag.GRT_FRY,
]
ITEM_LOCATION_NAME_TO_EXIT_OVERRIDES: dict[str, ZoneExit] = {
  "Forbidden Woods - Mothula Miniboss Room":           ZoneExit.all["Forbidden Woods Miniboss Arena"],
  "Tower of the Gods - Darknut Miniboss Room":         ZoneExit.all["Tower of the Gods Miniboss Arena"],
  "Earth Temple - Stalfos Miniboss Room":              ZoneExit.all["Earth Temple Miniboss Arena"],
  "Wind Temple - Wizzrobe Miniboss Room":              ZoneExit.all["Wind Temple Miniboss Arena"],
  "Hyrule - Master Sword Chamber":                     ZoneExit.all["Master Sword Chamber"],

  "Dragon Roost Cavern - Gohma Heart Container":       ZoneExit.all["Gohma Boss Arena"],
  "Forbidden Woods - Kalle Demos Heart Container":     ZoneExit.all["Kalle Demos Boss Arena"],
  "Tower of the Gods - Gohdan Heart Container":        ZoneExit.all["Gohdan Boss Arena"],
  "Forsaken Fortress - Helmaroc King Heart Container": ZoneExit.all["Helmaroc King Boss Arena"],
  "Earth Temple - Jalhalla Heart Container":           ZoneExit.all["Jalhalla Boss Arena"],
  "Wind Temple - Molgera Heart Container":             ZoneExit.all["Molgera Boss Arena"],

  "Pawprint Isle - Wizzrobe Cave":                     ZoneExit.all["Pawprint Isle Wizzrobe Cave"],

  "Ice Ring Isle - Inner Cave - Chest":                ZoneExit.all["Ice Ring Isle Inner Cave"],
  "Cliff Plateau Isles - Highest Isle":                ZoneExit.all["Cliff Plateau Isles Inner Cave"],

  "Outset Island - Great Fairy":                       ZoneExit.all["Outset Fairy Fountain"],
}

MINIBOSS_EXIT_TO_DUNGEON: dict[str, str] = {
    "Forbidden Woods Miniboss Arena":   "Forbidden Woods",
    "Tower of the Gods Miniboss Arena": "Tower of the Gods",
    "Earth Temple Miniboss Arena":      "Earth Temple",
    "Wind Temple Miniboss Arena":       "Wind Temple",
}

BOSS_EXIT_TO_DUNGEON: dict[str, str] = {
    "Gohma Boss Arena":         "Dragon Roost Cavern",
    "Kalle Demos Boss Arena":   "Forbidden Woods",
    "Gohdan Boss Arena":        "Tower of the Gods",
    "Helmaroc King Boss Arena": "Forsaken Fortress",
    "Jalhalla Boss Arena":      "Earth Temple",
    "Molgera Boss Arena":       "Wind Temple",
}

VANILLA_ENTRANCES_TO_EXITS: dict[str, str] = {
    "Dungeon Entrance on Dragon Roost Island": "Dragon Roost Cavern",
    "Dungeon Entrance in Forest Haven Sector": "Forbidden Woods",
    "Dungeon Entrance in Tower of the Gods Sector": "Tower of the Gods",
    "Dungeon Entrance on Headstone Island": "Earth Temple",
    "Dungeon Entrance on Gale Isle": "Wind Temple",

    "Miniboss Entrance in Forbidden Woods": "Forbidden Woods Miniboss Arena",
    "Miniboss Entrance in Tower of the Gods": "Tower of the Gods Miniboss Arena",
    "Miniboss Entrance in Earth Temple": "Earth Temple Miniboss Arena",
    "Miniboss Entrance in Wind Temple": "Wind Temple Miniboss Arena",
    "Miniboss Entrance in Hyrule Castle": "Master Sword Chamber",

    "Boss Entrance in Dragon Roost Cavern": "Gohma Boss Arena",
    "Boss Entrance in Forbidden Woods": "Kalle Demos Boss Arena",
    "Boss Entrance in Tower of the Gods": "Gohdan Boss Arena",
    "Boss Entrance in Forsaken Fortress": "Helmaroc King Boss Arena",
    "Boss Entrance in Earth Temple": "Jalhalla Boss Arena",
    "Boss Entrance in Wind Temple": "Molgera Boss Arena",

    "Secret Cave Entrance on Outset Island": "Savage Labyrinth",
    "Secret Cave Entrance on Dragon Roost Island": "Dragon Roost Island Secret Cave",
    "Secret Cave Entrance on Fire Mountain": "Fire Mountain Secret Cave",
    "Secret Cave Entrance on Ice Ring Isle": "Ice Ring Isle Secret Cave",
    "Secret Cave Entrance on Private Oasis": "Cabana Labyrinth",
    "Secret Cave Entrance on Needle Rock Isle": "Needle Rock Isle Secret Cave",
    "Secret Cave Entrance on Angular Isles": "Angular Isles Secret Cave",
    "Secret Cave Entrance on Boating Course": "Boating Course Secret Cave",
    "Secret Cave Entrance on Stone Watcher Island": "Stone Watcher Island Secret Cave",
    "Secret Cave Entrance on Overlook Island": "Overlook Island Secret Cave",
    "Secret Cave Entrance on Bird's Peak Rock": "Bird's Peak Rock Secret Cave",
    "Secret Cave Entrance on Pawprint Isle": "Pawprint Isle Chuchu Cave",
    "Secret Cave Entrance on Pawprint Isle Side Isle": "Pawprint Isle Wizzrobe Cave",
    "Secret Cave Entrance on Diamond Steppe Island": "Diamond Steppe Island Warp Maze Cave",
    "Secret Cave Entrance on Bomb Island": "Bomb Island Secret Cave",
    "Secret Cave Entrance on Rock Spire Isle": "Rock Spire Isle Secret Cave",
    "Secret Cave Entrance on Shark Island": "Shark Island Secret Cave",
    "Secret Cave Entrance on Cliff Plateau Isles": "Cliff Plateau Isles Secret Cave",
    "Secret Cave Entrance on Horseshoe Island": "Horseshoe Island Secret Cave",
    "Secret Cave Entrance on Star Island": "Star Island Secret Cave",

    "Inner Entrance in Ice Ring Isle Secret Cave": "Ice Ring Isle Inner Cave",
    "Inner Entrance in Cliff Plateau Isles Secret Cave": "Cliff Plateau Isles Inner Cave",

    "Fairy Fountain Entrance on Outset Island": "Outset Fairy Fountain",
    "Fairy Fountain Entrance on Thorned Fairy Island": "Thorned Fairy Fountain",
    "Fairy Fountain Entrance on Eastern Fairy Island": "Eastern Fairy Fountain",
    "Fairy Fountain Entrance on Western Fairy Island": "Western Fairy Fountain",
    "Fairy Fountain Entrance on Southern Fairy Island": "Southern Fairy Fountain",
    "Fairy Fountain Entrance on Northern Fairy Island": "Northern Fairy Fountain",
}


class EntranceRandomizer:
    """
    This class handles the logic for The Wind Waker entrance randomizer.

    We reference the logic from the base randomizer with some modifications to suit it for Archipelago.
    Reference: https://github.com/LagoLunatic/wwrando/blob/master/randomizers/entrances.py

    :param world: The Wind Waker game world.
    """

    def __init__(self, world: "TWWWorld"):
        self.world = world
        self.multiworld = world.multiworld
        self.player = world.player

        self.item_location_to_containing_zone_exit: dict[str, ZoneExit] = {}
        self.zone_exit_to_logically_dependent_item_locations: dict[ZoneExit, list[str]] = defaultdict(list)
        self.register_mappings_between_item_locations_and_zone_exits()

        self.done_entrances_to_exits: dict[ZoneEntrance, ZoneExit] = {}
        self.done_exits_to_entrances: dict[ZoneExit, ZoneEntrance] = {}

        for entrance_name, exit_name in VANILLA_ENTRANCES_TO_EXITS.items():
            zone_entrance = ZoneEntrance.all[entrance_name]
            zone_exit = ZoneExit.all[exit_name]
            self.done_entrances_to_exits[zone_entrance] = zone_exit
            self.done_exits_to_entrances[zone_exit] = zone_entrance

        self.banned_exits: list[ZoneExit] = []
        self.islands_with_a_banned_dungeon: set[str] = set()

    def randomize_entrances(self) -> None:
        """
        Randomize entrances for The Wind Waker.
        """
        self.init_banned_exits()

        for relevant_entrances, relevant_exits in self.get_all_entrance_sets_to_be_randomized():
            self.randomize_one_set_of_entrances(relevant_entrances, relevant_exits)

        self.finalize_all_randomized_sets_of_entrances()

    def init_banned_exits(self) -> None:
        """
        Initialize the list of banned exits for the randomizer.

        Dungeon exits in banned dungeons should be prohibited from being randomized.
        Additionally, if dungeon entrances are not randomized, we can now note which island holds these banned dungeons.
        """
        options = self.world.options

        if options.required_bosses:
            for zone_exit in BOSS_EXITS:
                assert zone_exit.unique_name.endswith(" Boss Arena")
                boss_name = zone_exit.unique_name.removesuffix(" Boss Arena")
                if boss_name in self.world.boss_reqs.banned_bosses:
                    self.banned_exits.append(zone_exit)
            for zone_exit in DUNGEON_EXITS:
                dungeon_name = zone_exit.unique_name
                if dungeon_name in self.world.boss_reqs.banned_dungeons:
                    self.banned_exits.append(zone_exit)
            for zone_exit in MINIBOSS_EXITS:
                if zone_exit == ZoneExit.all["Master Sword Chamber"]:
                    # Hyrule cannot be chosen as a banned dungeon.
                    continue
                assert zone_exit.unique_name.endswith(" Miniboss Arena")
                dungeon_name = zone_exit.unique_name.removesuffix(" Miniboss Arena")
                if dungeon_name in self.world.boss_reqs.banned_dungeons:
                    self.banned_exits.append(zone_exit)

        if not options.randomize_dungeon_entrances:
            # If dungeon entrances are not randomized, `islands_with_a_banned_dungeon` can be initialized early since
            # it's preset and won't be updated later since we won't randomize the dungeon entrances.
            for en in DUNGEON_ENTRANCES:
                if self.done_entrances_to_exits[en].unique_name in self.world.boss_reqs.banned_dungeons:
                    assert en.island_name is not None
                    self.islands_with_a_banned_dungeon.add(en.island_name)

    def randomize_one_set_of_entrances(
        self, relevant_entrances: list[ZoneEntrance], relevant_exits: list[ZoneExit]
    ) -> None:
        """
        Randomize a single set of entrances and their corresponding exits.

        :param relevant_entrances: A list of entrances to be randomized.
        :param relevant_exits: A list of exits corresponding to the entrances.
        """
        # Keep miniboss and boss entrances vanilla in non-required bosses' dungeons.
        for zone_entrance in relevant_entrances.copy():
            zone_exit = self.done_entrances_to_exits[zone_entrance]
            if zone_exit in self.banned_exits and zone_exit in DUNGEON_INNER_EXITS:
                relevant_entrances.remove(zone_entrance)
            else:
                del self.done_entrances_to_exits[zone_entrance]
        for zone_exit in relevant_exits.copy():
            if zone_exit in self.banned_exits and zone_exit in DUNGEON_INNER_EXITS:
                relevant_exits.remove(zone_exit)
            else:
                del self.done_exits_to_entrances[zone_exit]

        self.multiworld.random.shuffle(relevant_entrances)

        # We calculate which exits are terminal (the end of a nested chain) per set instead of for all entrances.
        # This is so that, for example, Ice Ring Isle counts as terminal when its inner cave is not being randomized.
        non_terminal_exits = []
        for en in relevant_entrances:
            if en.nested_in is not None and en.nested_in not in non_terminal_exits:
                non_terminal_exits.append(en.nested_in)
        terminal_exits = {ex for ex in relevant_exits if ex not in non_terminal_exits}

        remaining_entrances = relevant_entrances.copy()
        remaining_exits = relevant_exits.copy()

        nonprogress_entrances, nonprogress_exits = self.split_nonprogress_entrances_and_exits(
            remaining_entrances, remaining_exits
        )
        if nonprogress_entrances:
            for en in nonprogress_entrances:
                remaining_entrances.remove(en)
            for ex in nonprogress_exits:
                remaining_exits.remove(ex)
            self.randomize_one_set_of_exits(nonprogress_entrances, nonprogress_exits, terminal_exits)

        self.randomize_one_set_of_exits(remaining_entrances, remaining_exits, terminal_exits)

    def check_if_one_exit_is_progress(self, zone_exit: ZoneExit) -> bool:
        """
        Determine if the zone exit leads to progress locations in the world.

        :param zone_exit: The zone exit to check.
        :return: Whether the zone exit leads to progress locations.
        """
        locs_for_exit = self.zone_exit_to_logically_dependent_item_locations[zone_exit]
        assert locs_for_exit, f"Could not find any item locations corresponding to zone exit: {zone_exit.unique_name}"

        # Banned required bosses mode dungeons still technically count as progress locations, so filter them out
        # separately first.
        nonbanned_locs = [loc for loc in locs_for_exit if loc not in self.world.boss_reqs.banned_locations]
        progress_locs = [loc for loc in nonbanned_locs if loc not in self.world.nonprogress_locations]
        return bool(progress_locs)

    def split_nonprogress_entrances_and_exits(
        self, relevant_entrances: list[ZoneEntrance], relevant_exits: list[ZoneExit]
    ) -> tuple[list[ZoneEntrance], list[ZoneExit]]:
        """
        Splits the entrance and exit lists into two pairs: ones that should be considered nonprogress on this seed (will
        never lead to any progress items) and ones that should be regarded as potentially required.

        This is so we can effectively randomize these two pairs separately without convoluted logic to ensure they don't
        connect.

        :param relevant_entrances: A list of entrances.
        :param relevant_exits: A list of exits corresponding to the entrances.
        :raises FillError: If the number of randomizable entrances does not equal the number of randomizable exits.
        """
        nonprogress_exits = [ex for ex in relevant_exits if not self.check_if_one_exit_is_progress(ex)]
        nonprogress_entrances = [
            en
            for en in relevant_entrances
            if en.nested_in is not None
            and (
                (en.nested_in in nonprogress_exits)
                # The area this entrance is nested in is not randomized, but we still need to determine whether it's
                # progression.
                or (en.nested_in not in relevant_exits and not self.check_if_one_exit_is_progress(en.nested_in))
            )
        ]

        # At this point, `nonprogress_entrances` includes only the inner entrances nested inside the main exits, not any
        # island entrances on the sea. So, we need to select `N` random island entrances to allow all of the nonprogress
        # exits to be accessible, where `N` is the difference between the number of entrances and exits we currently
        # have.
        possible_island_entrances = [en for en in relevant_entrances if en.island_name is not None]

        # We need special logic to handle Forsaken Fortress, as it is the only island entrance inside a dungeon.
        ff_boss_entrance = ZoneEntrance.all["Boss Entrance in Forsaken Fortress"]
        if ff_boss_entrance in possible_island_entrances:
            if self.world.options.progression_dungeons:
                if "Forsaken Fortress" in self.world.boss_reqs.banned_dungeons:
                    ff_progress = False
                else:
                    ff_progress = True
            else:
                ff_progress = False

            if ff_progress:
                # If it's progress, don't allow it to be randomly chosen to lead to nonprogress exits.
                possible_island_entrances.remove(ff_boss_entrance)
            else:
                # If it's not progress, manually mark it as such, and don't allow it to be chosen randomly.
                nonprogress_entrances.append(ff_boss_entrance)
                possible_island_entrances.remove(ff_boss_entrance)

        num_island_entrances_needed = len(nonprogress_exits) - len(nonprogress_entrances)
        if num_island_entrances_needed > len(possible_island_entrances):
            raise FillError("Not enough island entrances left to split entrances.")

        for _ in range(num_island_entrances_needed):
            # Note: `relevant_entrances` is already shuffled, so we can just take the first result from
            # `possible_island_entrances`—it's the same as picking one randomly.
            nonprogress_island_entrance = possible_island_entrances.pop(0)
            nonprogress_entrances.append(nonprogress_island_entrance)

        assert len(nonprogress_entrances) == len(nonprogress_exits)

        return nonprogress_entrances, nonprogress_exits

    def randomize_one_set_of_exits(
        self, relevant_entrances: list[ZoneEntrance], relevant_exits: list[ZoneExit], terminal_exits: set[ZoneExit]
    ) -> None:
        """
        Randomize a single set of entrances and their corresponding exits.

        :param relevant_entrances: A list of entrances to be randomized.
        :param relevant_exits: A list of exits corresponding to the entrances.
        :param terminal_exits: A set of exits which do not contain any entrances.
        :raises FillError: If there are no valid exits to assign to an entrance.
        """
        options = self.world.options

        remaining_entrances = relevant_entrances.copy()
        remaining_exits = relevant_exits.copy()

        doing_banned = False
        if any(ex in self.banned_exits for ex in relevant_exits):
            doing_banned = True

        if options.required_bosses and not doing_banned:
            # Prioritize entrances that share an island with an entrance randomized to lead into a
            # required-bosses-mode-banned dungeon. (e.g., DRI, Pawprint, Outset, TotG sector.)
            # This is because we need to prevent these islands from having a required boss or anything that could lead
            # to a required boss. If we don't do this first, we can get backed into a corner where there is no other
            # option left.
            entrances_not_on_unique_islands = []
            for zone_entrance in relevant_entrances:
                if zone_entrance.is_nested:
                    continue
                if zone_entrance.island_name in self.islands_with_a_banned_dungeon:
                    # This island was already used on a previous call to `randomize_one_set_of_exits`.
                    entrances_not_on_unique_islands.append(zone_entrance)
                    continue
            for zone_entrance in entrances_not_on_unique_islands:
                remaining_entrances.remove(zone_entrance)
            remaining_entrances = entrances_not_on_unique_islands + remaining_entrances

        while remaining_entrances:
            # Filter out boss entrances that aren't yet accessible from the sea.
            # We don't want to connect these to anything yet or we risk creating an infinite loop.
            possible_remaining_entrances = [
                en for en in remaining_entrances if self.get_outermost_entrance_for_entrance(en) is not None
            ]
            zone_entrance = possible_remaining_entrances.pop(0)
            remaining_entrances.remove(zone_entrance)

            possible_remaining_exits = remaining_exits.copy()

            if len(possible_remaining_entrances) == 0 and len(remaining_entrances) > 0:
                # If this is the last entrance we have left to attach exits to, we can't place a terminal exit here.
                # Terminal exits do not create another entrance, so one would leave us with no possible way to continue
                # placing the remaining exits on future loops.
                possible_remaining_exits = [ex for ex in possible_remaining_exits if ex not in terminal_exits]

            if options.required_bosses and zone_entrance.island_name is not None and not doing_banned:
                # Prevent required bosses (and non-terminal exits, which could lead to required bosses) from appearing
                # on islands where we already placed a banned boss or dungeon.
                # This can happen with DRI and Pawprint, as these islands have two entrances. This would be bad because
                # the required bosses mode's dungeon markers only tell you what island the required dungeons are on, not
                # which of the two entrances to enter.
                # So, if a banned dungeon is placed on DRI's main entrance, we will have to fill DRI's pit entrance with
                # either a miniboss or one of the caves that does not have a nested entrance inside. We allow multiple
                # banned and required dungeons on a single island.
                if zone_entrance.island_name in self.islands_with_a_banned_dungeon:
                    possible_remaining_exits = [
                        ex
                        for ex in possible_remaining_exits
                        if ex in terminal_exits and ex not in (DUNGEON_EXITS + BOSS_EXITS)
                    ]

            if not possible_remaining_exits:
                raise FillError(f"No valid exits to place for entrance: {zone_entrance.entrance_name}")

            zone_exit = self.multiworld.random.choice(possible_remaining_exits)
            remaining_exits.remove(zone_exit)

            self.done_entrances_to_exits[zone_entrance] = zone_exit
            self.done_exits_to_entrances[zone_exit] = zone_entrance

            if zone_exit in self.banned_exits:
                # Keep track of which islands have a required bosses mode banned dungeon to avoid marker overlap.
                if zone_exit in DUNGEON_EXITS + BOSS_EXITS:
                    # We only keep track of dungeon exits and boss exits, not miniboss exits.
                    # Banned miniboss exits can share an island with required dungeons/bosses.
                    outer_entrance = self.get_outermost_entrance_for_entrance(zone_entrance)

                    # Because we filter above so that we always assign entrances from the sea inwards, we can assume
                    # that when we assign an entrance, it has a path back to the sea.
                    # If we're assigning a non-terminal entrance, any nested entrances will get assigned after this one,
                    # and we'll run through this code again (so we can reason based on `zone_exit` only instead of
                    # having to recurse through the nested exits to find banned dungeons/bosses).
                    assert outer_entrance and outer_entrance.island_name is not None
                    self.islands_with_a_banned_dungeon.add(outer_entrance.island_name)

    def finalize_all_randomized_sets_of_entrances(self) -> None:
        """
        Finalize all randomized entrance sets.

        For all entrance-exit pairs, this function adds a connection with the appropriate access rule to the world.
        """

        def get_access_rule(entrance: ZoneEntrance) -> str:
            snake_case_region = entrance.entrance_name.lower().replace("'", "").replace(" ", "_")
            return getattr(Macros, f"can_access_{snake_case_region}")

        # Connect each entrance-exit pair in the multiworld with the access rule for the entrance.
        # The Great Sea is the parent_region for many entrances, so get it in advance.
        great_sea_region = self.world.get_region("The Great Sea")
        for zone_entrance, zone_exit in self.done_entrances_to_exits.items():
            # Get the parent region of the entrance.
            if zone_entrance.island_name is not None:
                # Entrances with an `island_name` are found in The Great Sea.
                parent_region = great_sea_region
            else:
                # All other entrances must be nested within some other region.
                parent_region = self.world.get_region(zone_entrance.nested_in.unique_name)
            exit_region_name = zone_exit.unique_name
            exit_region = self.world.get_region(exit_region_name)
            parent_region.connect(
                exit_region,
                # The default name uses the "parent_region -> connecting_region", but the parent_region would not be
                # useful for spoiler paths or debugging, so use the entrance name at the start.
                f"{zone_entrance.entrance_name} -> {exit_region_name}",
                rule=lambda state, rule=get_access_rule(zone_entrance): rule(state, self.player),
            )

        if __debug__ and self.world.options.required_bosses:
            # Ensure we didn't accidentally place a banned boss and a required boss on the same island.
            banned_island_names = set(
                self.get_entrance_zone_for_boss(boss_name) for boss_name in self.world.boss_reqs.banned_bosses
            )
            required_island_names = set(
                self.get_entrance_zone_for_boss(boss_name) for boss_name in self.world.boss_reqs.required_bosses
            )
            assert not banned_island_names & required_island_names

    def register_mappings_between_item_locations_and_zone_exits(self) -> None:
        """
        Map item locations to their corresponding zone exits.
        """
        for loc_name in list(LOCATION_TABLE.keys()):
            zone_exit = self.get_zone_exit_for_item_location(loc_name)
            if zone_exit is not None:
                self.item_location_to_containing_zone_exit[loc_name] = zone_exit
                self.zone_exit_to_logically_dependent_item_locations[zone_exit].append(loc_name)

            if loc_name == "The Great Sea - Withered Trees":
                # This location isn't inside a zone exit, but it does logically require the player to be able to reach
                # a different item location inside one.
                sub_zone_exit = self.get_zone_exit_for_item_location("Cliff Plateau Isles - Highest Isle")
                if sub_zone_exit is not None:
                    self.zone_exit_to_logically_dependent_item_locations[sub_zone_exit].append(loc_name)

    def get_all_entrance_sets_to_be_randomized(
        self,
    ) -> Generator[tuple[list[ZoneEntrance], list[ZoneExit]], None, None]:
        """
        Retrieve all entrance-exit pairs that need to be randomized.

        :raises OptionError: If an invalid randomization option is set in the world's options.
        :return: A generator that yields sets of entrances and exits to be randomized.
        """
        options = self.world.options

        dungeons = bool(options.randomize_dungeon_entrances)
        minibosses = bool(options.randomize_miniboss_entrances)
        bosses = bool(options.randomize_boss_entrances)
        secret_caves = bool(options.randomize_secret_cave_entrances)
        inner_caves = bool(options.randomize_secret_cave_inner_entrances)
        fountains = bool(options.randomize_fairy_fountain_entrances)

        mix_entrances = options.mix_entrances
        if mix_entrances == "separate_pools":
            if dungeons:
                yield self.get_one_entrance_set(dungeons=dungeons)
            if minibosses:
                yield self.get_one_entrance_set(minibosses=minibosses)
            if bosses:
                yield self.get_one_entrance_set(bosses=bosses)
            if secret_caves:
                yield self.get_one_entrance_set(caves=secret_caves)
            if inner_caves:
                yield self.get_one_entrance_set(inner_caves=inner_caves)
            if fountains:
                yield self.get_one_entrance_set(fountains=fountains)
        elif mix_entrances == "mix_pools":
            yield self.get_one_entrance_set(
                dungeons=dungeons,
                minibosses=minibosses,
                bosses=bosses,
                caves=secret_caves,
                inner_caves=inner_caves,
                fountains=fountains,
            )
        else:
            raise OptionError(f"Invalid entrance randomization option: {mix_entrances}")

    def get_one_entrance_set(
        self,
        *,
        dungeons: bool = False,
        caves: bool = False,
        minibosses: bool = False,
        bosses: bool = False,
        inner_caves: bool = False,
        fountains: bool = False,
    ) -> tuple[list[ZoneEntrance], list[ZoneExit]]:
        """
        Retrieve a single set of entrance-exit pairs that need to be randomized.

        :param dungeons: Whether to include dungeon entrances and exits. Defaults to `False`.
        :param caves: Whether to include secret cave entrances and exits. Defaults to `False`.
        :param minibosses: Whether to include miniboss entrances and exits. Defaults to `False`.
        :param bosses: Whether to include boss entrances and exits. Defaults to `False`.
        :param inner_caves: Whether to include inner cave entrances and exits. Defaults to `False`.
        :param fountains: Whether to include fairy fountain entrances and exits. Defaults to `False`.
        :return: A tuple of lists of entrances and exits that should be randomized together.
        """
        relevant_entrances: list[ZoneEntrance] = []
        relevant_exits: list[ZoneExit] = []
        if dungeons:
            relevant_entrances += DUNGEON_ENTRANCES
            relevant_exits += DUNGEON_EXITS
        if minibosses:
            relevant_entrances += MINIBOSS_ENTRANCES
            relevant_exits += MINIBOSS_EXITS
        if bosses:
            relevant_entrances += BOSS_ENTRANCES
            relevant_exits += BOSS_EXITS
        if caves:
            relevant_entrances += SECRET_CAVE_ENTRANCES
            relevant_exits += SECRET_CAVE_EXITS
        if inner_caves:
            relevant_entrances += SECRET_CAVE_INNER_ENTRANCES
            relevant_exits += SECRET_CAVE_INNER_EXITS
        if fountains:
            relevant_entrances += FAIRY_FOUNTAIN_ENTRANCES
            relevant_exits += FAIRY_FOUNTAIN_EXITS
        return relevant_entrances, relevant_exits

    def get_outermost_entrance_for_exit(self, zone_exit: ZoneExit) -> Optional[ZoneEntrance]:
        """
        Unrecurses nested dungeons to determine a given exit's outermost (island) entrance.

        :param zone_exit: The given exit.
        :return: The outermost (island) entrance for the exit, or `None` if entrances have yet to be randomized.
        """
        zone_entrance = self.done_exits_to_entrances[zone_exit]
        return self.get_outermost_entrance_for_entrance(zone_entrance)

    def get_outermost_entrance_for_entrance(self, zone_entrance: ZoneEntrance) -> Optional[ZoneEntrance]:
        """
        Unrecurses nested dungeons to determine a given entrance's outermost (island) entrance.

        :param zone_exit: The given entrance.
        :return: The outermost (island) entrance for the entrance, or `None` if entrances have yet to be randomized.
        """
        seen_entrances = self.get_all_entrances_on_path_to_entrance(zone_entrance)
        if seen_entrances is None:
            # Undecided.
            return None
        outermost_entrance = seen_entrances[-1]
        return outermost_entrance

    def get_all_entrances_on_path_to_entrance(self, zone_entrance: ZoneEntrance) -> Optional[list[ZoneEntrance]]:
        """
        Unrecurses nested dungeons to build a list of all entrances leading to a given entrance.

        :param zone_exit: The given entrance.
        :return: A list of entrances leading to the given entrance, or `None` if entrances have yet to be randomized.
        """
        seen_entrances: list[ZoneEntrance] = []
        while zone_entrance.is_nested:
            if zone_entrance in seen_entrances:
                path_str = ", ".join([e.entrance_name for e in seen_entrances])
                raise FillError(f"Entrances are in an infinite loop: {path_str}")
            seen_entrances.append(zone_entrance)
            if zone_entrance.nested_in not in self.done_exits_to_entrances:
                # Undecided.
                return None
            zone_entrance = self.done_exits_to_entrances[zone_entrance.nested_in]
        seen_entrances.append(zone_entrance)
        return seen_entrances

    def is_item_location_behind_randomizable_entrance(self, location_name: str) -> bool:
        """
        Determine if the location is behind a randomizable entrance.

        :param location_name: The location to check.
        :return: `True` if the location is behind a randomizable entrance, `False` otherwise.
        """
        loc_zone_name, _ = split_location_name_by_zone(location_name)
        if loc_zone_name in ["Ganon's Tower", "Mailbox"]:
            # Ganon's Tower and the handful of Mailbox locations that depend on beating dungeon bosses are considered
            # "Dungeon" location types by the logic, but the entrance randomizer does not need to consider them.
            # Although the mail locations are technically locked behind dungeons, we can still ignore them here because
            # if all of the locations in the dungeon itself are nonprogress, then any mail depending on that dungeon
            # should also be enforced as nonprogress by other parts of the code.
            return False

        types = LOCATION_TABLE[location_name].flags
        is_boss = TWWFlag.BOSS in types
        if loc_zone_name == "Forsaken Fortress" and not is_boss:
            # Special case. FF is a dungeon that is not randomized, except for the boss arena.
            return False

        is_big_octo = TWWFlag.BG_OCTO in types
        if is_big_octo:
            # The Big Octo Great Fairy is the only Great Fairy location that is not also a Fairy Fountain.
            return False

        # In the general case, we check if the location has a type corresponding to exits that can be randomized.
        if any(t in types for t in ENTRANCE_RANDOMIZABLE_ITEM_LOCATION_TYPES):
            return True

        return False

    def get_zone_exit_for_item_location(self, location_name: str) -> Optional[ZoneExit]:
        """
        Retrieve the zone exit for a given location.

        :param location_name: The name of the location.
        :raises Exception: If a location exit override should be used instead.
        :return: The zone exit for the location or `None` if the location is not behind a randomizable entrance.
        """
        if not self.is_item_location_behind_randomizable_entrance(location_name):
            return None

        zone_exit = ITEM_LOCATION_NAME_TO_EXIT_OVERRIDES.get(location_name, None)
        if zone_exit is not None:
            return zone_exit

        loc_zone_name, _ = split_location_name_by_zone(location_name)
        possible_exits = [ex for ex in ZoneExit.all.values() if ex.zone_name == loc_zone_name]
        if len(possible_exits) == 0:
            return None
        elif len(possible_exits) == 1:
            return possible_exits[0]
        else:
            raise Exception(
                f"Multiple zone exits share the same zone name: {loc_zone_name!r}. "
                "Use a location exit override instead."
            )

    def get_entrance_zone_for_boss(self, boss_name: str) -> str:
        """
        Retrieve the entrance zone for a given boss.

        :param boss_name: The name of the boss.
        :return: The name of the island on which the boss is located.
        """
        boss_arena_name = f"{boss_name} Boss Arena"
        zone_exit = ZoneExit.all[boss_arena_name]
        outermost_entrance = self.get_outermost_entrance_for_exit(zone_exit)
        assert outermost_entrance is not None and outermost_entrance.island_name is not None
        return outermost_entrance.island_name
