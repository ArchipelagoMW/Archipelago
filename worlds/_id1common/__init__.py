# id1Common - Common library for Doom/Heretic/derived games in Archipelago
#
# This file is copyright (C) Kay "Kaito" Sinclaire,
# and is released under the terms of the zlib license.
# See "LICENSE" for more details
#
# Brief:
#   Main library functions and custom world class.

import json
import logging
import typing
from collections.abc import Iterable
from copy import deepcopy
from pkgutil import get_data

from BaseClasses import Entrance, Item, ItemClassification, Location, LocationProgressType, MultiWorld, Region
from Options import OptionError
from worlds.AutoWorld import AutoWorldRegister, World

from .options import Episode, id1CommonOptions

if typing.TYPE_CHECKING:
    from BaseClasses import CollectionState
    from Options import OptionSet, PerGameCommonOptions, Range

    from .options import CheckSanity

DOOM_TYPE_LEVEL_UNLOCK = -1
DOOM_TYPE_LEVEL_COMPLETE = -2


class FillerPoolRatio(typing.NamedTuple):
    helpful: int
    random: int
    # junk is implied to be whatever's left out ot 100


class ConnectionCriteriaData(typing.NamedTuple):
    criteria_and: list[str]
    criteria_or: list[str]

    def make_rule(self, player: int) -> typing.Callable[["CollectionState"], bool]:
        if len(self.criteria_and) > 0:
            if len(self.criteria_or) > 0:
                return lambda state: state.has_all(self.criteria_and, player) \
                                     and state.has_any(self.criteria_or, player)
            return lambda state: state.has_all(self.criteria_and, player)
        if len(self.criteria_or) > 0:
            return lambda state: state.has_any(self.criteria_or, player)
        return lambda state: True


class ConnectionData:
    target: str  # target region
    requires: list[str]  # option requirements for connection to exist
    rules: list[ConnectionCriteriaData]  # items required

    def __init__(self, obj: dict[str, typing.Any]):
        self.target = obj["_target"]
        self.requires = obj.get("requires", [])
        self.rules = [ConnectionCriteriaData(obj2.get("and", []), obj2.get("or", []))
            for obj2 in obj.get("rules", [])]

    def requirements_met(self, spec: dict[str, typing.Callable[[typing.Any], bool]], world: "id1CommonWorld") -> bool:
        for requirement in self.requires:
            if requirement not in spec or not spec[requirement](world):
                return False
        return True


class RegionData:
    name: str  # as _name in json
    episode: int  # as exmx[0] in json
    gamemap: int  # as exmx[1] in json
    connections: list[ConnectionData]

    def __init__(self, obj: dict[str, typing.Any]):
        self.name = obj["_name"]
        self.episode, self.gamemap = obj.get("exmx", (-1, -1))
        self.connections = [ConnectionData(obj2) for obj2 in obj.get("connections", [])]

    def get_connection_to(self, other_region: str) -> ConnectionData | None:
        if self.name == other_region:
            return None  # No connections to ourselves allowed
        for connection in self.connections:
            if connection.target == other_region:
                return connection
        return None


class LocationData:
    name: str  # as _name in json
    episode: int  # as exmx[0] in json
    gamemap: int  # as exmx[1] in json
    doom_type: int
    region: str
    check_sanity: bool

    def __init__(self, obj: dict[str, typing.Any]):
        self.name = obj["_name"]
        self.episode, self.gamemap = obj.get("exmx", (-1, -1))
        self.doom_type = obj["doom_type"]
        self.region = obj["region"]
        self.check_sanity = obj.get("check_sanity", False)


class ItemData:
    name: str  # as _name in json
    episode: int  # as exmx[0] in json
    gamemap: int  # as exmx[1] in json
    doom_type: int
    count: int
    classification: ItemClassification

    def __init__(self, obj: dict[str, typing.Any]):
        self.name = obj["_name"]
        self.episode, self.gamemap = obj.get("exmx", (-1, -1))
        self.doom_type = obj["doom_type"]
        self.count = obj.get("count", 0)
        self.classification = ItemClassification(obj.get("classification", 0))


class AutoLoadJsonData(AutoWorldRegister):
    """Metaclass that automatically loads id1 Json data into the World class, if requested.

    Expects the world subclass to contain an "import_data" argument, like so:
        class ExampleWorld(id1CommonWorld, import_data=(__name__, "data.json"))
    """
    def __new__(cls, name, bases, dct, *, import_data: tuple[str, str] | None = None):
        if import_data is not None:
            pkg_name, file_name = import_data
            json_data = get_data(pkg_name, file_name)
            assert json_data is not None
            json_data = json.loads(json_data.decode("utf-8"))

            dct["item_table"] = {int(idx): ItemData(obj) for (idx, obj) in json_data["item_table"].items()}
            dct["location_table"] = {int(idx): LocationData(obj) for (idx, obj) in json_data["location_table"].items()}

            dct["item_name_to_id"] = {item.name: idx for (idx, item) in dct["item_table"].items()}
            dct["item_name_groups"] = json_data["item_name_groups"]
            dct["location_name_to_id"] = {loc.name: idx for (idx, loc) in dct["location_table"].items()}
            dct["location_name_groups"] = json_data["location_name_groups"]

            dct["region_data"] = [RegionData(obj) for obj in json_data["regions"]]
            dct["death_logic_excluded_locations"] = json_data["death_logic_excluded_locations"]
            dct["starting_levels_by_episode"] = {int(idx): name
                                                 for (idx, name) in json_data["starting_levels_by_episode"].items()}

            dct["filler_item_weight"] = json_data.get("filler_item_weight", {})
            dct["custom_pool_ratio"] = {int(idx): FillerPoolRatio(*data)
                                         for (idx, data) in json_data.get("custom_pool_ratio", {}).items()}
        return super().__new__(cls, name, bases, dct)


class id1CommonWorld(World, metaclass=AutoLoadJsonData):  # noqa: N801
    # Data parsed from JSON
    item_table: typing.ClassVar[dict[int, ItemData]]
    location_table: typing.ClassVar[dict[int, LocationData]]
    item_name_to_id: typing.ClassVar[dict[str, int]] = {}
    item_name_groups: typing.ClassVar[dict[str, set[str]]]
    location_name_to_id: typing.ClassVar[dict[str, int]] = {}
    location_name_groups: typing.ClassVar[dict[str, set[str]]]
    region_data: typing.ClassVar[list[RegionData]]
    death_logic_excluded_locations: typing.ClassVar[list[str]]
    starting_levels_by_episode: typing.ClassVar[dict[int, str]]

    filler_item_weight: typing.ClassVar[dict[str, int]]
    custom_pool_ratio: typing.ClassVar[dict[int, FillerPoolRatio]]

    options_dataclass: typing.ClassVar[type["PerGameCommonOptions"]] = id1CommonOptions
    options: id1CommonOptions  # type: ignore

    # Should be provided by subclass
    extra_connection_requirements: typing.ClassVar[dict[str, typing.Callable[[typing.Any], bool]]]

    # This gets populated by construct_regions, and is local to us.
    # Contains only the regions and connections that are present in our world with our settings.
    constructed_region_list: list[RegionData]

    # This gets populated by init_episodes, usually in generate_early.
    # Contains all episodes the player has chosen in their options, e.g. {1, 2, 3, 5}
    included_episodes: set[int]

    # This also gets populated by init_episodes, just contains the starting level names.
    # Can be modified if need be in generate_early.
    starting_levels: list[str]

    # This gets populated by place_level_complete_items.
    # Contains all level complete item names. Completion rules check these.
    level_complete_list: list[str]

    # These are only related to certain goals, and are only populated if those goals are chosen.
    _required_level_complete_list: list[str]
    _required_level_complete_count: int

    # If a custom_pool_ratio isn't set, these are the defaults. For each difficulty:
    #   "helpful" is the percentage of total item pool to be filled with powerups
    #   "random" is the percentage of total item pool with unweighted filler
    #   (all items after that are Junk)
    default_pool_ratio: typing.ClassVar[dict[int, FillerPoolRatio]] = {
        0: FillerPoolRatio(helpful=51, random=4),  # I'm Too Young To Die (55%)
        1: FillerPoolRatio(helpful=47, random=8),  # Hey, Not Too Rough (55%)
        2: FillerPoolRatio(helpful=41, random=9),  # Hurt Me Plenty (50%)
        3: FillerPoolRatio(helpful=36, random=7),  # Ultra-Violence (43%)
        4: FillerPoolRatio(helpful=36, random=7),  # Nightmare! (43%)
    }

    origin_region_name = "Hub"

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.included_episodes = set()
        self.starting_levels = []
        self.constructed_region_list = []
        self.level_complete_list = []
        self._required_level_complete_list = []
        self._required_level_complete_count = 0

    # -------------------------------------------------------------------------
    # Helper functions and properties
    def _episode_option_iterator(self) -> typing.Generator[tuple[int, Episode], None, None]:
        """Returns a tuple of (episode num, option) for every episode option this world supports."""
        ep = 1
        while (option := getattr(self.options, f"episode{ep}", None)) is not None:
            yield (ep, option)
            ep += 1
        if ep == 1:  # If there are no episode options, we yield a fake Episode option that is always set true.
            yield (1, Episode(1))

    @property
    def major_episodes(self):
        return {ep for ep, option in self._episode_option_iterator() if option.is_major_episode}

    @property
    def included_major_episodes(self) -> set[int]:
        return {i for i in self.included_episodes if i in self.major_episodes}

    @property
    def episode_count(self) -> int:
        return len(self.included_episodes)

    @property
    def major_episode_count(self) -> int:
        return len(self.included_major_episodes)

    def solo_episode(self, episode: int) -> bool:
        """
        Returns True if the player is running the given episode solo (no other major episodes), False otherwise.
        """
        return False if self.major_episode_count != 1 else (min(self.included_major_episodes) == episode)

    def matching_items(self, *, doom_type: Iterable[int] | int = 0) -> dict[int, ItemData]:
        """Gets item data that matches specific criteria."""
        doomtype_list: list[int] = list(doom_type) if isinstance(doom_type, Iterable) else [doom_type]
        return {idx: item for (idx, item) in self.item_table.items()
                if (len(doomtype_list) == 0 or item.doom_type in doomtype_list)}

    def get_random_levels(self, count: int) -> list[str]:
        """Returns count number of random level names that are present in our settings."""
        levels = [item.name for item in self.item_table.values()
                  if item.doom_type == DOOM_TYPE_LEVEL_UNLOCK and item.episode in self.included_episodes]
        self.random.shuffle(levels)

        count = max(0, min(count, len(levels)))
        # Bias against starting levels with lower counts.
        if count <= 13 and count <= len(self.starting_levels * 3):
            levels.sort(key=lambda value: 666 if value in self.starting_levels else 0)
        return levels[:count]

    def warning(self, content: str) -> None:
        logging.warning(f"{self.multiworld.get_player_name(self.player)}: {content}")

    # -------------------------------------------------------------------------
    # Goal completion rules, for each goal type
    def rule_complete_all_levels(self, state: "CollectionState") -> bool:
        return state.has_all(self.level_complete_list, self.player)

    def rule_complete_some_levels(self, state: "CollectionState") -> bool:
        return state.count_from_list_unique(self.level_complete_list, self.player) \
            >= self._required_level_complete_count

    def rule_complete_specific_levels(self, state: "CollectionState") -> bool:
        return state.has_all(self._required_level_complete_list, self.player)

    # -------------------------------------------------------------------------
    # World construction methods
    def init_episodes(self) -> None:
        """
        Initializes included_episodes with the player's options, and forces at least one major episode to be enabled.
        """
        self.included_episodes = {ep for ep, option in self._episode_option_iterator() if option.value}
        if self.major_episode_count == 0:
            first_major = min(self.major_episodes)
            self.warning(f"No major episodes were enabled.\n"
                         f"Enabling Episode {first_major}.")
            self.included_episodes.add(first_major)

        self.starting_levels = [name for (ep, name) in self.starting_levels_by_episode.items()
                                if ep in self.included_episodes]

        # Warn on skill 5, just like the original games did.
        # This is a kinda cutesy way of reminding the player that difficulty can be changed on the fly.
        if self.options.difficulty.value == 4:
            skill_5_warning = getattr(self.options.difficulty, "skill_5_warning", "")
            if len(skill_5_warning) > 0:
                self.warning(f"{skill_5_warning}\n"
                             f"Remember that the game difficulty can be turned down afterwards in the launcher.")

        # Do not allow the combination of ITYTD + Extreme tricks
        # Extreme tricks that require damage boosting may become impossible in ITYTD due to the damage reduction
        if self.options.difficulty.value == 0 and self.options.trick_difficulty.value >= 3:
            self.options.difficulty.value = 1
            self.warning("Difficulty automatically raised to Easy (2) because Extreme tricks are enabled.")

    def construct_regions(self) -> None:
        """
        Fills constructed_region_list with modified region data based on the player's options.
        (only including content from selected episodes, impossible connections cut, unreachable regions culled)
        Uses copies of the structures in region_data, to avoid multiple worlds clobbering each other.
        """
        if len(self.constructed_region_list) != 0:
            return

        allowed_episodes = set.union(self.included_episodes, {-1})
        regions = [deepcopy(region) for region in self.region_data if region.episode in allowed_episodes]

        all_region_names = {region.name for region in regions}

        # Go through each region, and remove connections that rely on options that aren't enabled.
        # We also remove connections to regions that don't exist, which basically only affects the Hub.
        for region in regions:
            unmet_connections = [i for i, connection in enumerate(region.connections)
                                 if not connection.requirements_met(self.extra_connection_requirements, world=self)
                                 or connection.target not in all_region_names]
            for index in sorted(unmet_connections, reverse=True):
                logging.debug(f"Removing connection {region.name} -> {region.connections[index].target}")
                del region.connections[index]

        # We now need to cull regions that aren't reachable, and repeatedly do this until nothing changes.
        while (True):
            to_cull = [i for i, region in enumerate(regions)
                       if region.name != "Hub"  # Never cull the Hub
                       and len([other for other in regions if other.get_connection_to(region.name) is not None]) == 0]
            if len(to_cull) == 0:
                break

            for index in sorted(to_cull, reverse=True):
                logging.debug(f"Culling region {index} ({regions[index].name})")
                del regions[index]

        # We now have our constructed region list, so save it for later.
        self.constructed_region_list = regions

    def make_regions(self, *, region_type: type = Region, location_type: type = Location) -> None:
        """
        Makes regions and locations based on the constructed region list, and submits them all to the multiworld.
        """
        # Check to see if CheckSanity is present.
        # This option may not exist in all games. If it isn't, we assume it's enabled (spawn all checks)
        check_sanity = True
        if check_sanity_opt := getattr(self.options, "check_sanity", None):
            if typing.TYPE_CHECKING:
                assert type(check_sanity_opt) is CheckSanity
            check_sanity = bool(check_sanity_opt.value)

        # Get every location that we need to make.
        locations_by_region: dict[str, dict[str, int | None]] = {re.name: {} for re in self.constructed_region_list}
        for loc_id, location in self.location_table.items():
            if location.check_sanity and not check_sanity:
                continue
            if location.region in locations_by_region:
                locations_by_region[location.region][location.name] = loc_id

        # Now we can make the actual Regions, and while we're at it, the locations too.
        for region_data in self.constructed_region_list:
            region = Region(region_data.name, self.player, self.multiworld)
            region.add_locations(locations_by_region[region_data.name])
            self.multiworld.regions.append(region)

        # With all regions made, we can now make connections...
        for region_data in self.constructed_region_list:
            if len(region_data.connections) == 0:
                continue  # It's rare, but possible, for a region to have no outbound connections

            source_region = self.multiworld.get_region(region_data.name, self.player)
            for connection in region_data.connections:
                target_region = self.multiworld.get_region(connection.target, self.player)
                source_region.connect(target_region, f"{region_data.name} -> {connection.target}")

        # Since we just finished making locations, let's also exclude locations if death logic isn't enabled.
        if not self.options.allow_death_logic.value:
            death_logic_locations = [loc for loc in self.multiworld.get_locations(self.player)
                                     if loc.name in self.death_logic_excluded_locations]
            for world_loc in death_logic_locations:
                world_loc.progress_type = LocationProgressType.EXCLUDED

    def make_rules(self) -> None:
        """
        Assigns access rules to connections between regions in this world. Also assigns the goal rule.

        Note that while ap_gen_tool currently only supports one rule per connection,
        this code has been written with the possibility of that changing in the future.
        """
        def add_criteria_to_connection(source: str, target: str, criteria: ConnectionCriteriaData) -> None:
            cx = self.multiworld.get_entrance(f"{source} -> {target}", self.player)
            old_rule = cx.access_rule
            new_rule = criteria.make_rule(self.player)
            if old_rule is Entrance.access_rule:
                cx.access_rule = new_rule
            else:
                cx.access_rule = lambda state: new_rule(state) or old_rule(state)

        for region_data in self.constructed_region_list:
            for connection in region_data.connections:
                for criteria in connection.rules:
                    add_criteria_to_connection(region_data.name, connection.target, criteria)

        # The completion condition is also a rule, so we'll set up the goals here.
        level_unlock_list: list[str] = []  # Only used for specific or random levels

        if self.options.goal == "complete_specific_levels":
            if levelset_opt := getattr(self.options, "goal_specific_levels", None):
                if typing.TYPE_CHECKING:
                    assert type(levelset_opt) is OptionSet
                level_unlock_list = list(levelset_opt.value)

                for level in level_unlock_list:
                    item_data = next(item for item in self.item_table.values()
                                     if item.doom_type == DOOM_TYPE_LEVEL_COMPLETE and item.name.startswith(level))
                    if item_data.name in self.level_complete_list:
                        self._required_level_complete_list.append(item_data.name)

            if len(self._required_level_complete_list) == 0:
                self.warning("Either the goal level list was empty, or all levels in it were disabled.\n"
                             "Goal changed to 'Complete All Levels'.")
                self.options.goal.value = self.options.goal.option_complete_all_levels

        elif self.options.goal == "complete_random_levels":
            # We basically treat this as "specific levels" where we choose the levels instead of the player.
            if count_opt := getattr(self.options, "goal_num_levels", None):
                if typing.TYPE_CHECKING:
                    assert type(count_opt) is Range
                level_unlock_list = self.get_random_levels(count_opt.value)

                for level in level_unlock_list:
                    item_data = next(item for item in self.item_table.values()
                                     if item.doom_type == DOOM_TYPE_LEVEL_COMPLETE and item.name.startswith(level))
                    if item_data.name in self.level_complete_list:
                        self._required_level_complete_list.append(item_data.name)

            # This basically only happens with malformed or nonexistant options, but it's here to catch that.
            if len(self._required_level_complete_list) == 0:
                self.warning("Attempted to use a 'Complete Random Levels' goal, but rolled no levels.\n"
                             "Goal changed to 'Complete All Levels'.")
                self.options.goal.value = self.options.goal.option_complete_all_levels

        elif self.options.goal == "complete_some_levels":
            # Silently limit the number of levels required to the number of levels available.
            if count_opt := getattr(self.options, "goal_num_levels", None):
                if typing.TYPE_CHECKING:
                    assert type(count_opt) is Range
                self._required_level_complete_count = max(0, min(count_opt.value, len(self.level_complete_list)))

            # This basically only happens with malformed or nonexistant options, but it's here to catch that.
            if self._required_level_complete_count == 0:
                self.warning("Attempted to use a 'Complete Some Levels' goal with a count of zero.\n"
                             "Goal changed to 'Complete All Levels'.")
                self.options.goal.value = self.options.goal.option_complete_all_levels

        if self.options.goal == "complete_random_levels" or self.options.goal == "complete_specific_levels":
            self.multiworld.completion_condition[self.player] = lambda state: self.rule_complete_specific_levels(state)
        elif self.options.goal == "complete_some_levels":
            self.multiworld.completion_condition[self.player] = lambda state: self.rule_complete_some_levels(state)
        else:  # implied complete_all_levels
            self.multiworld.completion_condition[self.player] = lambda state: self.rule_complete_all_levels(state)

        # While we're here... if we have a goal with set levels, make those levels skip balancing.
        if self.options.goal == "complete_random_levels" or self.options.goal == "complete_specific_levels":
            unlock_items = [item for item in self.multiworld.itempool
                            if item.player == self.player and item.name in level_unlock_list]
            for item in unlock_items:
                item.classification |= ItemClassification.skip_balancing

    def place_level_complete_items(self, *, item_type: type = Item) -> None:
        """
        Places a locked Map Complete item on each Map Exit location that exists in this world.
        """
        allowed_episodes = set.union(self.included_episodes, {-1})
        items = [item for item in self.item_table.values()
                 if item.episode in allowed_episodes and item.doom_type == DOOM_TYPE_LEVEL_COMPLETE]
        locations = [loc for loc in self.location_table.values()
                     if loc.episode in allowed_episodes and loc.doom_type == DOOM_TYPE_LEVEL_COMPLETE]

        for item in items:
            loc_data = next(loc for loc in locations
                            if loc.episode == item.episode and loc.gamemap == item.gamemap)
            self.multiworld.get_location(loc_data.name, self.player).place_locked_item(self.create_item(item.name))

        self.level_complete_list = [item.name for item in items]

    def construct_base_item_pool(self) -> list[str]:
        """
        Gets the base item pool, formed by taking all items in the item table and adding them (item.count) times.
        """
        allowed_episodes = set.union(self.included_episodes, {-1})
        items = [item for item in self.item_table.values() if item.episode in allowed_episodes]
        return [item.name for item in items for _ in range(item.count)]

    def fill_item_pool(self, item_pool: list[str], size: int) -> None:
        rest_items = size - len(item_pool)

        # Are there more items in the base item pool than there are locations to fill?
        # This is really hard to actually do, but I wouldn't rule it out.
        if rest_items < 0:
            raise OptionError(f"{self.multiworld.get_player_name(self.player)}: "
                              f"Too many base items in the item pool for locations. ({len(item_pool)} > {size})\n"
                              f"Please change your settings to add more locations or fewer items.")
        if rest_items == 0:
            return

        # The weighted filler pool is allowed to be empty. If it is, we only place "Junk".
        if len(self.filler_item_weight) > 0:
            diff = int(self.options.difficulty.value)
            pool_weight = self.custom_pool_ratio.get(diff, self.default_pool_ratio[diff])

            helpful_count = min(round(size * pool_weight.helpful / 100), rest_items)
            random_count = min(round(size * pool_weight.random / 100), rest_items - helpful_count)

            # Mix in powerups into the item pool, weighted based on the filler item ratio.
            item_pool.extend(self.random.choices(population=list(self.filler_item_weight.keys()),
                                                 weights=list(self.filler_item_weight.values()),
                                                 k=helpful_count))

            # Now mix in a bit of completely random, unweighted filler, for extra spice.
            set_filler = set(self.filler_item_weight.keys()) | set(self.item_name_groups["Junk"])
            all_filler = sorted(set_filler)
            item_pool.extend(self.random.choice(all_filler) for _ in range(random_count))

        # Any remaining slots get filled with items in the "Junk" group.
        item_pool.extend(self.get_filler_item_name() for _ in range(size - len(item_pool)))

    # -------------------------------------------------------------------------
    # Default overrides for World class methods
    def get_filler_item_name(self) -> str:
        return self.random.choice(sorted(self.item_name_groups["Junk"]))

    def fill_slot_data(self) -> dict[str, typing.Any]:
        # Fill in options guaranteed to exist.
        slot_data = self.options.as_dict(
            "death_link",
            "difficulty",
            "reset_level_on_death",
            "random_monsters",
            "random_pickups",
            "random_music",
            "flip_levels",
            "allow_death_logic",
            "trick_difficulty",
        )

        goal_data: dict[str, typing.Any] = { "type": int(self.options.goal.value) }
        if self.options.goal == "complete_random_levels" or self.options.goal == "complete_specific_levels":
            goal_data["levels"] = [[item.episode, item.gamemap] for item in self.item_table.values()
                                  if item.name in self._required_level_complete_list]
        elif self.options.goal == "complete_some_levels":
            goal_data["count"] = self._required_level_complete_count
        slot_data["goal"] = goal_data

        # Track locations that *should* exist but don't in slot_data.
        extant_locations = {loc.address for loc in self.multiworld.get_locations(self.player)}
        slot_data["suppressed_locations"] = [idx for idx, loc in self.location_table.items()
                                             if loc.episode in self.included_episodes and idx not in extant_locations]

        # Automatically add in the list of included episodes too.
        slot_data["episodes"] = list(self.included_episodes)
        return slot_data

    def write_spoiler_header(self, spoiler_handle: typing.TextIO):
        if self.options.goal == "complete_random_levels":
            # This gets them in order from first to last.
            levels = [i.name for i in self.item_table.values() if i.name in self._required_level_complete_list]

            spoiler_handle.write('\nGoal levels for "Complete Random Levels":\n')
            [spoiler_handle.write(f"- {level.removesuffix(' - Complete')}\n") for level in levels]
