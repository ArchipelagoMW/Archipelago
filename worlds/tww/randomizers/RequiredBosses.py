from typing import TYPE_CHECKING

from Options import OptionError

from ..Locations import DUNGEON_NAMES, LOCATION_TABLE, TWWFlag, split_location_name_by_zone
from ..Options import TWWOptions

if TYPE_CHECKING:
    from .. import TWWWorld


class RequiredBossesRandomizer:
    """
    This class handles the randomization of the required bosses in The Wind Waker game based on user options.

    If the option is on, the required bosses must be defeated as part of the unlock condition of Puppet Ganon's door.
    The quadrants in which the bosses are located are marked on the player's Sea Chart.

    :param world: The Wind Waker game world.
    """

    def __init__(self, world: "TWWWorld"):
        self.world = world
        self.multiworld = world.multiworld

        self.required_boss_item_locations: list[str] = []
        self.required_dungeons: set[str] = set()
        self.required_bosses: list[str] = []
        self.banned_locations: set[str] = set()
        self.banned_dungeons: set[str] = set()
        self.banned_bosses: list[str] = []

    def validate_boss_options(self, options: TWWOptions) -> None:
        """
        Validate the user-defined boss options to ensure logical consistency.

        :param options: The game options set by the user.
        :raises OptionError: If the boss options are inconsistent.
        """
        if not options.progression_dungeons:
            raise OptionError("You cannot make bosses required when progression dungeons are disabled.")

        if len(options.included_dungeons.value & options.excluded_dungeons.value) != 0:
            raise OptionError(
                "A conflict was found in the lists of required and banned dungeons for required bosses mode."
            )

    def randomize_required_bosses(self) -> None:
        """
        Randomize the required bosses based on user-defined constraints and options.

        :raises OptionError: If the randomization fails to meet user-defined constraints.
        """
        options = self.world.options

        # Validate constraints on required bosses options.
        self.validate_boss_options(options)

        # If the user enforces a dungeon location to be priority, consider that when selecting required bosses.
        dungeon_names = set(DUNGEON_NAMES)
        required_dungeons = options.included_dungeons.value
        for location_name in options.priority_locations.value:
            dungeon_name, _ = split_location_name_by_zone(location_name)
            if dungeon_name in dungeon_names:
                required_dungeons.add(dungeon_name)

        # Ensure we aren't prioritizing more dungeon locations than the requested number of required bosses.
        num_required_bosses = options.num_required_bosses
        if len(required_dungeons) > num_required_bosses:
            raise OptionError(
                "Could not select required bosses to satisfy options set by the user. "
                "There are more dungeons with priority locations than the desired number of required bosses."
            )

        # Ensure that after removing excluded dungeons, we still have enough to satisfy user options.
        num_remaining = num_required_bosses - len(required_dungeons)
        remaining_dungeon_options = dungeon_names - required_dungeons - options.excluded_dungeons.value
        if len(remaining_dungeon_options) < num_remaining:
            raise OptionError(
                "Could not select required bosses to satisfy options set by the user. "
                "After removing the excluded dungeons, there are not enough to meet the desired number of required "
                "bosses."
            )

        # Finish selecting required bosses.
        required_dungeons.update(self.world.random.sample(sorted(remaining_dungeon_options), num_remaining))

        # Exclude locations that are not in the dungeon of a required boss.
        banned_dungeons = dungeon_names - required_dungeons
        for location_name, location_data in LOCATION_TABLE.items():
            dungeon_name, _ = split_location_name_by_zone(location_name)
            if dungeon_name in banned_dungeons and TWWFlag.DUNGEON in location_data.flags:
                self.banned_locations.add(location_name)
            elif location_name == "Mailbox - Letter from Orca" and "Forbidden Woods" in banned_dungeons:
                self.banned_locations.add(location_name)
            elif location_name == "Mailbox - Letter from Baito" and "Earth Temple" in banned_dungeons:
                self.banned_locations.add(location_name)
            elif location_name == "Mailbox - Letter from Aryll" and "Forsaken Fortress" in banned_dungeons:
                self.banned_locations.add(location_name)
            elif location_name == "Mailbox - Letter from Tingle" and "Forsaken Fortress" in banned_dungeons:
                self.banned_locations.add(location_name)
        for location_name in self.banned_locations:
            self.world.nonprogress_locations.add(location_name)

        # Record the item location names for required bosses.
        self.required_boss_item_locations = []
        self.required_bosses = []
        self.banned_bosses = []
        possible_boss_item_locations = [loc for loc, data in LOCATION_TABLE.items() if TWWFlag.BOSS in data.flags]
        for location_name in possible_boss_item_locations:
            dungeon_name, specific_location_name = split_location_name_by_zone(location_name)
            assert specific_location_name.endswith(" Heart Container")
            boss_name = specific_location_name.removesuffix(" Heart Container")

            if dungeon_name in required_dungeons:
                self.required_boss_item_locations.append(location_name)
                self.required_bosses.append(boss_name)
            else:
                self.banned_bosses.append(boss_name)
        self.required_dungeons = required_dungeons
        self.banned_dungeons = banned_dungeons
