import itertools
import logging
import operator
from collections import Counter, defaultdict
from copy import deepcopy
from typing import Any, ClassVar

from BaseClasses import CollectionState, Entrance, EntranceType, ItemClassification, LocationProgressType, MultiWorld
from entrance_rando import EntranceRandomizationError, randomize_entrances
from Options import OptionError
from worlds.AutoWorld import World

from .charms import charm_name_to_id, charm_names
from .classes import HKClause, HKEntrance, HKItem, HKLocation, HKRegion, HKSettings, HKWeb
from .constants import NearbySoul, gamename, randomizable_starting_items, shop_cost_types
from .options import (
    CostSanity,
    Goal,
    GrubHuntGoal,
    HKOptions,
    ShuffleEntrancesMode,
    StartLocation,
    WhitePalace,
    hollow_knight_options,
    shop_to_option,
)
from .parse_data import (
    datapackage_item_groups,
    datapackage_items,
    datapackage_location_groups,
    datapackage_locations,
    effects_items_by_term,
    effects_non_prog,
    effects_prog_lookup,
    effects_terms_by_item,
    event_locations,
    hk_locations,
    hk_regions,
    metadata_location_multi,
    options_logic_mappings,
    options_pool_mappings,
    structure_regions,
    structure_transition_to_region_map,
    trando_starts,
    trando_transitions,
    vanilla_location_costs,
    vanilla_shop_costs,
)
from .resource_state_vars import ResourceStateHandler
from .rules import cost_terms
from .state_mixin import HKLogicMixin as HKLogicMixin
from .state_mixin import hk_collect, hk_remove
from .template_world import RandomizerCoreWorld

logger = logging.getLogger("Hollow Knight")


class HKWorld(RandomizerCoreWorld, World):
    """Beneath the fading town of Dirtmouth sleeps a vast, ancient kingdom. Many are drawn beneath the surface,
    searching for riches, or glory, or answers to old secrets.

    As the enigmatic Knight, you’ll traverse the depths, unravel its mysteries and conquer its evils.
    """  # from https://www.hollowknight.com  # noqa: RUF002

    game = gamename
    web = HKWeb()
    item_name_to_id = datapackage_items
    location_name_to_id = datapackage_locations
    options_dataclass = HKOptions
    options: HKOptions
    settings: ClassVar[HKSettings]
    item_name_groups = datapackage_item_groups
    location_name_groups = datapackage_location_groups

    rc_regions: list[dict[str, Any]] = hk_regions
    rc_locations: list[dict[str, Any]] = hk_locations
    item_class = HKItem
    location_class = HKLocation
    region_class = HKRegion

    rule_lookup: ClassVar[dict[str, str]] = {
        location["name"]: location["logic"] for location in hk_locations if location["logic"]
    }
    region_lookup: ClassVar[dict[str, str]] = {location: r["name"] for r in hk_regions for location in r["locations"]}
    entrance_by_term: dict[str, list[str]]
    entrance_pairs: dict[str, str]
    entrance_groups: dict[str, list[HKEntrance]]
    entrance_state_modifier_by_term: dict[str, list[tuple[str, str]]]

    cached_filler_items: list[str]
    grub_count: int
    grub_player_count: dict[int, int]
    event_locations: list[str]
    ranges: dict[str, tuple[int, int]]
    charm_costs: list[int]
    charm_names_and_costs: dict[str, int]
    soul_modes: NearbySoul

    # imported class functions
    collect = hk_collect
    remove = hk_remove

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)
        self.created_multi_locations: dict[str, list[HKLocation]] = {
            location: [] for location in metadata_location_multi
            if location != "Start"
        }
        self.ranges = {}
        self.created_shop_items = 0
        self.vanilla_shop_costs = deepcopy(vanilla_shop_costs)
        self.cached_filler_items = []
        self.event_locations = deepcopy(event_locations)
        self.entrance_by_term = defaultdict(list)
        self.entrance_pairs = {}
        self.entrance_state_modifier_by_term = defaultdict(list)

    # generate_early
    def generate_early(self):
        options = self.options
        weights = {
            data.term: getattr(options, f"CostSanity{data.option}Weight").value
            for data in cost_terms.values()
        }
        if options.CostSanity:
            player_name = self.player_name
            if all(weight == 0 for weight in weights.values()):
                raise OptionError(f"CostSanity was on for {player_name} but no currencies are enabled")
            if all(weight == 0 for name, weight in weights.items() if name != "GEO"):
                raise OptionError(
                    f"CostSanityHybridChance was on for {player_name}"
                    "but no non-geo currencies are enabled for non-geo shops"
                )
            # hybrid_chance = options.CostSanityHybridChance.value
            # if hybrid_chance and len([name for name, weight in weights.items() if name is not "GEO" and weight != 0]):
            #     raise OptionError(f"temp")

        for term, data in cost_terms.items():
            mini = getattr(options, f"Minimum{data.option}Price")
            maxi = getattr(options, f"Maximum{data.option}Price")
            # if minimum > maximum, flip them
            if mini.value > maxi.value:
                self.ranges[term] = maxi.value, mini.value
            else:
                self.ranges[term] = mini.value, maxi.value

        charm_costs = options.RandomCharmCosts.get_costs(self.random)
        self.charm_costs = options.PlandoCharmCosts.get_costs(charm_costs)
        self.charm_names_and_costs = {name: (self.charm_costs[index] if name != "Void_Heart" else 0)
                                      for name, index in charm_name_to_id.items()}
        self.soul_modes = self.options.EntranceRandoType.soul_mode

        self.split_cloak_direction = self.random.randint(0, 1)

        if self.options.StartLocation == StartLocation.option_kings_pass:
            # Temporarily skip location validation on default start to workaround worlds with bad logicmixins
            self.start_location_region = structure_transition_to_region_map[
                trando_starts[self.options.StartLocation.current_key]["granted_transition"]
            ]
        else:
            start_location_key = self.options.StartLocation.current_key
            start_validation = self.validate_start(start_location_key)
            if start_validation:
                raise OptionError(f"Start Location {start_location_key} was invalid with other Options. "
                                  f"Requirements not met are:\n{start_validation}")
                # TODO consider warning and resetting to KP
            self.start_location_region = structure_transition_to_region_map[
                trando_starts[start_location_key]["granted_transition"]
            ]
            # actually connect it later once we have regions created

        # defaulting so completion condition isn't incorrect before pre_fill
        self.grub_count = (
            46 if options.GrubHuntGoal == GrubHuntGoal.special_range_names["all"]
            else options.GrubHuntGoal.value
            )
        self.grub_player_count = {self.player: self.grub_count}

    @classmethod
    def stage_generate_early(cls, multiworld):
        groups = [
            group for id, group in multiworld.groups.items()
            if id in multiworld.get_game_groups(cls.game)
            and "Left_Mothwing_Cloak" in group["item_pool"]
            ]
        for group in groups:
            # for a group sharing split cloaks make sure they share the same direction
            split_cloak_direction = multiworld.random.randint(0, 1)
            for player in group["players"]:
                # override the random value set in generate_early
                multiworld.worlds[player].split_cloak_direction = split_cloak_direction

        # initialize GER monkeypatch
        from entrance_rando import ERPlacementState

        original_connect_one_way = ERPlacementState._connect_one_way

        def edited_connect_one_way(self, source_exit: Entrance, target_entrance: Entrance) -> None:
            if not isinstance(source_exit, HKEntrance):
                original_connect_one_way(self, source_exit, target_entrance)
                return

            self.world._stateless_connect_one_way(source_exit, target_entrance)

            self.collection_state.stale[self.world.player] = True
            self.placements.append(source_exit)
            self.pairings.append((source_exit.name, target_entrance.name))
            self.entrance_lookup.remove(target_entrance)
            return

        ERPlacementState._connect_one_way = edited_connect_one_way

    def validate_start(self, start_location_key: str) -> list[list[str]]:
        test_state = CollectionState(self.multiworld)
        valid_items = ["2MASKS"]  # TODO: properly handle these assumptions (non-cursed masks)
        if self.options.EnemyPogos:
            valid_items.append("ENEMYPOGOS")
        if test_state.has_group("Vertical", self.player):
            valid_items.append("VERTICAL")
        if not self.options.RandomizeSwim:
            valid_items.append("SWIM")
        if self.options.DarkRooms:
            valid_items.append("DARKROOMS")
        if self.options.ShadeSkips:
            valid_items.append("SHADESKIPS")
        if self.options.PreciseMovement:
            valid_items.append("PRECISEMOVEMENT")
        if self.options.DangerousSkips:
            valid_items.append("DANGEROUSSKIPS")

        valid_items.append(self.options.EntranceRandoType.tag)

        start_location_logic = trando_starts[start_location_key]["logic"]

        if not start_location_logic:  # empty logic means always good
            return []
        for clause in start_location_logic:  # TODO: assuming only item_requirements are relevant
            if all(i in valid_items for i in clause["item_requirements"]):
                return []
        return [clause["item_requirements"] for clause in start_location_logic]

    # create_regions
    def create_regions(self):
        super().create_regions()  # Call RandomizerCoreWorld create_regions
        self.setup_connections()
        self.add_all_events()
        self.add_shop_locations()

        for loc in self.options.WhitePalace.location_exclusions():
            self.get_location(loc).progress_type = LocationProgressType.EXCLUDED

        location_to_option = {
            location: option
            for option, data in options_pool_mappings.items()
            for location in data["randomized"]["locations"]
        }
        location_to_option["Elevator_Pass"] = "RandomizeElevatorPass"
        for location, costs in vanilla_location_costs.items():
            if self.options.AddUnshuffledLocations or getattr(self.options, location_to_option[location]):
                self.get_location(location).costs = costs

        self.get_region("Menu").connect(self.get_region(self.start_location_region))

    def get_location_map(self) -> dict[str, dict[str, int | None]]:
        # # Vanilla placements of the following items have no impact on logic, thus we can avoid creating these items
        # # and locations entirely when the option to randomize them is disabled.
        # logicless_options = {
        #     "RandomizeVesselFragments", "RandomizeGeoChests", "RandomizeJunkPitChests", "RandomizeRelics",
        #     "RandomizeMaps", "RandomizeJournalEntries", "RandomizeGeoRocks", "RandomizeBossGeo",
        #     "RandomizeLoreTablets", "RandomizeSoulTotems", "RandomizeLifebloodCocoons",
        # }

        # make our location_list off of location per option
        # and add any necessary location for logic to event_locations to be create later
        exclusions = self.options.WhitePalace.location_exclusions()
        if "King_Fragment" in exclusions:
            exclusions.remove("King_Fragment")

        location_list = [
            location
            for option, data in options_pool_mappings.items()
            for location in data["randomized"]["locations"]
            if location not in self.event_locations and getattr(self.options, option)
            and location not in self.created_multi_locations
            ]

        # options not handled in options_pool_mappings
        if self.options.RandomizeElevatorPass:
            location_list.append("Elevator_Pass")
        # logic if random elevators is off just checks region access instead
        else:
            self.event_locations.append("Elevator_Pass")

        if self.options.SplitCrystalHeart:
            if "Crystal_Heart" in location_list:
                location_list.append("Split_Crystal_Heart")
            else:
                self.event_locations.append("Split_Crystal_Heart")

        directions = ("Left", "Right")
        if self.options.SplitMantisClaw:
            if not self.options.RandomizeSkills:
                raise OptionError("TODO: handle this")
            location_name = "Mantis_Claw"
            if "Mantis_Claw" in location_list:
                location_list.remove(location_name)
                location_list += [f"{prefix}_{location_name}" for prefix in directions]
            else:
                self.event_locations.remove(location_name)
                self.event_locations += [f"{prefix}_{location_name}" for prefix in directions]

        if self.options.SplitMothwingCloak:
            if "Mothwing_Cloak" in location_list:
                location_list.append("Split_Mothwing_Cloak")
            else:
                self.event_locations.append("Split_Mothwing_Cloak")

        if self.options.RandomizeFocus:
            location_list.append("Focus")

        # build out the map per location in the list
        location_map = {
            region["name"]: {
                location: self.location_name_to_id[location]
                for location in region["locations"]
                if location in location_list
            }
            for region in self.rc_regions
        }

        # TODO bandaid fix to make sure these don't ever get added to the pool
        assert not [1 for obj in location_map.values() if obj in ("Can_Warp_To_DG_Bench", "Can_Warp_To_Bench")]
        return location_map

    def create_rule(self, rule: Any) -> list[HKClause]:
        # TODO consider caching on these as they should be deterministic,
        # TODO Cont. but they need options so only deterministic per world
        def parse_item_logic(reqs: list) -> tuple[bool, Counter[str]]:  # Mapping[str, int]:
            # handle both keys of item name and keys of itemname>count
            ret: Counter[str] = Counter()
            for full_req in reqs:
                if full_req.split("=0")[0] in options_logic_mappings:
                    req = full_req.split("=")
                    if len(req) == 2 and req[1] == "0":
                        # handle RANDOMELEVATORS=0 checking for the option off
                        logic_bool = False
                    else:
                        logic_bool = True
                    if getattr(self.options, options_logic_mappings[req[0]]) == logic_bool:
                        # if the option is true, remove the requirement and let continue
                        continue
                    # else return skip_clause=True because the rest of the clause doesn't matter
                    return True, Counter({"FALSE": 1})

                req = full_req.split(">")
                if len(req) == 2:
                    ret[req[0]] = max(int(req[1]) + 1, ret[req[0]])
                    # handle item1>count so that another item1 in the clause is valid
                else:
                    ret[req[0]] = max(1, ret[req[0]])

            return False, ret

        assert rule != []
        hk_rule = []
        for clause in rule:
            item_requirements = clause["item_requirements"]
            state_requirements = []
            skip_clause = False

            for req in clause["state_modifiers"]:
                handler = ResourceStateHandler.get_handler(req, self.player)
                if handler.can_exclude(self.options):
                    skip_clause = True
                else:
                    state_requirements.append(handler)

            # checking for a False condition before and after item parsing for short circuiting
            if skip_clause:
                continue
            skip_clause, items = parse_item_logic(item_requirements)
            if skip_clause:
                continue
            for item in items:
                assert (
                    item == "FALSE"
                    or item in effects_items_by_term
                    or item in effects_terms_by_item
                    or item in self.event_locations
                ), f"{item} not found in advancements"
            hk_rule.append(HKClause(
                hk_item_requirements=dict(items),
                hk_region_requirements=clause["region_requirements"],
                hk_state_requirements=state_requirements,
                ))

        return hk_rule

    def set_rule(self, spot, rule):
        # set hk_rule instead of access_rule because our Location class defines a custom access_rule
        if isinstance(spot, HKEntrance):
            relevant_terms = {term for clause in rule for term in clause.hk_item_requirements.keys()}
            tried_modifiers = set()
            for clause in rule:
                state_modifier_id = "; ".join(handler.term_name for handler in clause.hk_state_requirements)
                if state_modifier_id in tried_modifiers:
                    continue
                tried_modifiers.add(state_modifier_id)
                cur_terms = set()
                for handler in clause.hk_state_requirements:
                    cur_terms.update(handler.terms)
                relevant_terms.update(cur_terms)
                for term in cur_terms:
                    self.entrance_state_modifier_by_term[term].append((spot.name, state_modifier_id))
            for term in relevant_terms:
                # could keep this a static method by doing spot.parent_region.multiworld.worlds[spot.player] but ugh
                self.entrance_by_term[term].append(spot.name)

        spot.set_hk_rule(rule)

    def set_victory(self) -> None:
        multiworld = self.multiworld
        player = self.player
        goal = self.options.Goal
        if goal == Goal.option_hollowknight:
            multiworld.completion_condition[player] = lambda state: state.has("Defeated_Any_Hollow_Knight", player)
        elif goal == Goal.option_siblings:
            multiworld.completion_condition[player] = lambda state: (state.has("Defeated_Any_Hollow_Knight", player)
                                                                     and state.has("WHITEFRAGMENT", player, 3))
        elif goal == Goal.option_radiance:
            multiworld.completion_condition[player] = lambda state: state.has("Defeated_Any_Radiance", player)
        elif goal == Goal.option_godhome:
            multiworld.completion_condition[player] = lambda state: state.has("Defeated_Pantheon_5", player)
        elif goal == Goal.option_godhome_flower:
            multiworld.completion_condition[player] = self.can_godhome_flower
        elif goal == Goal.option_grub_hunt:
            multiworld.completion_condition[player] = self.can_grub_goal
        else:
            # Any goal
            multiworld.completion_condition[player] = (
                lambda state: state.has("Defeated_Any_Hollow_Knight", player) and state.has("WHITEFRAGMENT", player, 3)
                and state.has("Defeated_Any_Radiance", player)
                and self.can_godhome_flower(state)
                and self.can_grub_goal(state)
            )

    def can_godhome_flower(self, state: CollectionState):
        return state.has_all_counts({"Godtuner": 1, "Defeated_Pantheon_5": 1, "Flower_Quest-Godseeker": 1}, self.player)

    def can_grub_goal(self, state: CollectionState) -> bool:
        if not state.can_reach_region("Crossroads_38[right1]", self.player):
            return False
        for owner, count in self.grub_player_count.items():
            if not state.has("Grub", owner, count):
                return False
        return True

    def _stateless_connect_one_way(self, source_exit: Entrance, target_entrance: Entrance) -> None:
        """Stolen from entrance_rando"""
        target_region = target_entrance.connected_region
        assert target_entrance.parent_region is None
        assert source_exit.connected_region is None

        target_region.entrances.remove(target_entrance)
        source_exit.connect(target_region)
        source_exit._er_connected = True
        target_entrance._er_connected = True

        self.entrance_pairs[source_exit.name] = target_entrance.name
        # pairings.append((source_exit.name, target_entrance.name))
        del target_entrance

    def connect_entrances(self):
        if not self.options.EntranceRandoType:
            return
        coupled = self.options.ShuffleEntrancesMode != ShuffleEntrancesMode.option_decoupled

        def _connect_entrances(group: str, entrances: list[HKEntrance] | None) -> None:
            target_group_lookup = {
                # assuming MatchingDirections for now
                "Left": ["Right"],
                "Right": ["Left"],
                "Top": ["Bot"],
                "Bot": ["Top"],
                # unnecessary for the ger call
                # "Door": ["Door"],
                # "OneWayIn": ["OneWayOut"],
                # "OneWayOut": ["OneWayIn"],
            }
            if entrances:
                exits = [e for e in entrances if e.connected_region is None and not e._er_connected]
                er_targets = [e for e in entrances if e.parent_region is None and not e._er_connected]

                if len(exits) == 0:
                    assert len(er_targets) == 0
                    logger.debug(f"returning early for group {group} "
                                 "as there was nothing to place after single entrance matching")
                    return

                # logger.debug(f"running er on {group} for {len(exits)} exits and {len(er_targets)} entrances")
            else:
                er_targets = None
                exits = None

            try:
                randomize_entrances(
                    world=self,
                    coupled=coupled,
                    target_group_lookup=target_group_lookup,
                    er_targets=er_targets,
                    exits=exits,
                )

            except EntranceRandomizationError as ex:
                # this pairing code is causing some impossible entrance pairings to happen.. TODO: revisit if possible

                # exits = [e for e in entrances if e.connected_region is None and not e._er_connected]
                # er_targets = [e for e in entrances if e.parent_region is None and not e._er_connected]
                # group_counts = Counter([e.randomization_group for e in exits])
                # for rand_group, count in group_counts.items():
                #     if count != 1:
                #         continue
                #     group_exits = [e for e in exits if e.randomization_group == rand_group]

                #     target_group = target_group_lookup[rand_group][0]
                #     assert target_group in group_counts
                #     group_targets = [e for e in er_targets if e.randomization_group == target_group]

                #     assert len(group_exits) == len(group_targets) == 1
                #     self._stateless_connect_one_way(group_exits[0], group_targets[0])
                #     logger.debug(f"successfully matched up single entrances for group {group}")
                #     exits.remove(group_exits[0])
                #     er_targets.remove(group_targets[0])

                if exits is None or exits or er_targets:
                    raise ex
                    # reraise for retry attempts if there is still unmatched Entrances

        RETRY_ATTEMPTS = 3
        for index in range(1, 1 + RETRY_ATTEMPTS):
            for group, entrances in self.entrance_groups.items():
                if group == "global":
                    # will do afterwards
                    continue
                raise Exception("idk i wanna move on from connected area er")
                filtered_entrances = len([e for e in entrances if not e._er_connected])
                if not filtered_entrances:
                    # logger.debug(f"Try {index} for group {group} skipped, as there were no filtered entrances")
                    continue
                try:
                    _connect_entrances(group, entrances)
                    logger.debug(f"Try {index} for group {group} succeeded, paired {filtered_entrances} entrances")
                except EntranceRandomizationError:
                    leftovers = len([1 for e in entrances if not e._er_connected])
                    if index == RETRY_ATTEMPTS:
                        logger.info(f"GER failed for group {group}, all remaining {leftovers}/{filtered_entrances} "
                                    "entrance will be retried without group restrictions")
                    else:
                        logger.debug(f"Try {index} for group {group} failed, "
                                     f"{leftovers}/{filtered_entrances} unplaced.")

        _connect_entrances("global", None)

        if self.options.accessibility != "minimal":
            all_state = self.multiworld.get_all_state(allow_partial_entrances=True)
            if not all_state.can_reach_location("Mask_Shard-Grey_Mourner", self.player):
                raise OptionError("GER created a map with no path to flower quest")
            if not self.multiworld.completion_condition[self.player](all_state):
                raise OptionError(
                    "GER created a map that cannot finish completion condition, "
                    "you can retry, but not including godhome_flower or any goal "
                    "(which includes godhome_flower) will reduce the chances of this."
                )

    def setup_connections(self):
        if self.options.WhitePalace < WhitePalace.option_include:
            self.options.SkipTitledAreaInER.value.add("Path of Pain")
        if self.options.WhitePalace < WhitePalace.option_kingfragment:
            self.options.SkipTitledAreaInER.value.add("White Palace")

        one_ways = defaultdict(list)
        reverse_lookup = {
            # to map doors to the opposite direction of their vanilla target
            "Left": "Right",
            "Right": "Left",
        }
        self.entrance_groups = defaultdict(list)
        er_type = self.options.EntranceRandoType
        skip_area = self.options.SkipTitledAreaInER
        for name, trans_data in trando_transitions.items():
            if er_type.test_transition(trans_data) and skip_area.test_transition(trans_data):

                assert er_type, f"attempted to create er entrance ({name}) without er enabled"
                # create partial entrance for GER

                region1 = self.get_region(structure_transition_to_region_map[name])
                direction = trans_data["direction"]  # Left/Right/Top/Bot/Door
                sides = trans_data["sides"]  # Both/OneWayIn/OneWayOut
                entrance_subgroup = er_type.get_subgroup(trans_data)

                entrance_type = EntranceType.TWO_WAY if sides == "Both" else EntranceType.ONE_WAY
                group = direction if sides == "Both" else sides
                if group == "Door":
                    vanilla_target = trando_transitions[trans_data["vanilla_target"]]
                    group = reverse_lookup[vanilla_target["direction"]]
                    assert group != "Door"

                if sides != "OneWayOut":
                    exit_obj = region1.create_exit(name)
                    exit_obj.randomization_type = entrance_type
                    exit_obj.randomization_group = group
                    self.entrance_groups[entrance_subgroup].append(exit_obj)
                    if sides in ("OneWayOut", "OneWayIn"):
                        one_ways[group].append(exit_obj)
                if sides != "OneWayIn":
                    exit_target = region1.create_er_target(name)
                    exit_target.randomization_type = entrance_type
                    exit_target.randomization_group = group
                    self.entrance_groups[entrance_subgroup].append(exit_target)
                    if sides in ("OneWayOut", "OneWayIn"):
                        one_ways[group].append(exit_target)
            else:
                # create the apppropriate vanilla entrance instead
                if trans_data["vanilla_target"] is None:
                    # is a one-way target
                    continue

                region1 = self.get_region(structure_transition_to_region_map[name])
                region2 = self.get_region(structure_transition_to_region_map[trans_data["vanilla_target"]])
                region1.connect(region2, name)

        if not one_ways:
            return

        self.random.shuffle(one_ways["OneWayIn"])

        for entrance, exit in zip(one_ways["OneWayOut"], one_ways["OneWayIn"], strict=True):
            self._stateless_connect_one_way(exit, entrance)

    def add_all_events(self):
        location_to_region = {loc: reg["name"] for reg in structure_regions for loc in reg["locations"]}

        def create_location(item: str, location: str, costs: list[dict]):
            from .parse_data import shop_locations
            if location in shop_locations:
                loc = self.add_shop_location(location)
                if item:
                    loc.vanilla = True
            else:
                region = self.get_region(location_to_region[location])
                if not self.options.AddUnshuffledLocations or location in self.event_locations:
                    loc_id = None
                else:
                    loc_id = self.location_name_to_id[location]
                loc = self.location_class(self.player, location, loc_id, region)
                region.locations.append(loc)

                rule = self.rule_lookup.get(location)
                if rule:
                    self.set_rule(loc, self.create_rule(rule))
            assert item
            if item:
                if not self.options.AddUnshuffledLocations or item in self.event_locations:
                    item_id = None
                    loc.address = None
                else:
                    item_id = self.item_name_to_id[item]
                loc.place_locked_item(
                    self.item_class(item, ItemClassification.progression, item_id, self.player)
                )
                loc.show_in_spoiler = False
            return loc

        for option, option_data in options_pool_mappings.items():
            if not getattr(self.options, option):
                for pair in option_data["vanilla"]:
                    if pair["location"] == "Start":
                        continue
                    create_location(pair["item"], pair["location"], pair["costs"])
        for event in self.event_locations:
            create_location(event, event, [])

    def add_shop_location(self, shop, index=None):
        if index is None:
            index = len(self.created_multi_locations[shop])
        lookup_shop = shop if "(Requires_Charms)" not in shop else "Salubra"
        # fix because Salubra_(Requires_Charms) isn't actually in the source data

        costs = None
        if shop in shop_cost_types:
            costs = {
                term: self.random.randint(*self.ranges[term])
                for term in shop_cost_types[shop]
            }

        rule = self.rule_lookup.get(lookup_shop)
        region = self.get_region(self.region_lookup[lookup_shop])
        location_name = f"{shop}_{index+1}"
        code = self.location_name_to_id[location_name]

        loc = self.location_class(self.player, location_name, code, region)
        if rule:
            self.set_rule(loc, self.create_rule(rule))
        if costs:
            loc.costs = costs
            loc.sort_costs()
        self.created_multi_locations[shop].append(loc)
        loc.basename = shop  # for costsanity pool checking
        region.locations.append(loc)
        return loc

    def add_shop_locations(self):
        # TODO logicless event items that get culled don't take up shop space
        for shop, shop_locations in self.created_multi_locations.items():
            for index in range(len(shop_locations), getattr(self.options, shop_to_option[shop]).value):
                # start index may be important if we pre-create unshuffled items in shops
                self.add_shop_location(shop, index)
        self.add_extra_shop_locations(self.options.ExtraShopSlots.value)

    def add_extra_shop_locations(self, count):
        # Add additional shop items, as needed.
        if not count > 0:
            return
        shops = [shop for shop, locations in self.created_multi_locations.items() if len(locations) < 16]
        if not self.options.EggShopSlots.value:  # No eggshop, so don't place items there
            shops.remove("Egg_Shop")

        if not shops:
            return
        for _ in range(count):
            shop = self.random.choice(shops)
            index = len(self.created_multi_locations[shop])
            self.add_shop_location(shop, index)
            if len(self.created_multi_locations[shop]) >= 16:
                shops.remove(shop)
                if not shops:
                    break

    # create_items
    def create_items(self):
        pool_count = super().create_items()  # Call RandomizerCoreWorld create_items

        item_difference = pool_count - len(self.multiworld.get_unfilled_locations(self.player))
        if item_difference > 0:
            self.add_extra_shop_locations(item_difference)

        self.handle_starting_inventory()
        self.apply_costsanity()
        self.sort_shops_by_cost()

    def get_item_list(self) -> list[str]:
        junk: set[str] = {"Downslash"}
        if self.options.RemoveSpellUpgrades:
            junk.update(("Abyss_Shriek", "Shade_Soul", "Descending_Dark"))
        exclusions = self.options.WhitePalace.location_exclusions()
        if "King_Fragment" in exclusions:
            exclusions.remove("King_Fragment")
        junk.update(exclusions)

        # build out item_table (including counts) by option, excluding items in junk
        item_table = [
            item
            for option, data in options_pool_mappings.items()
            for item in data["randomized"]["items"]
            if getattr(self.options, option) and item not in junk
        ]

        # options not handled in options_pool_mappings
        directions = ("Left", "Right")
        if self.options.SplitMothwingCloak and self.options.RandomizeSkills:
            item_name = "Mothwing_Cloak"
            item_table.remove(item_name)
            item_table += [f"{prefix}_{item_name}" for prefix in directions]

            item_table.remove("Shade_Cloak")
            item_table.append("Left_Mothwing_Cloak" if self.split_cloak_direction else "Right_Mothwing_Cloak")

        if self.options.SplitCrystalHeart and self.options.RandomizeSkills:
            item_name = "Crystal_Heart"
            item_table.remove(item_name)
            item_table += [f"{prefix}_{item_name}" for prefix in directions]

        if self.options.SplitMantisClaw and self.options.RandomizeSkills:
            item_name = "Mantis_Claw"
            item_table.remove(item_name)
            item_table += [f"{prefix}_{item_name}" for prefix in directions]

        # Grimmchild 2 added in the pool options but should be handled as 1 in vanilla event placement
        if "Grimmchild2" in item_table and (self.options.RandomizeGrimmkinFlames or not self.options.RandomizeCharms):
            item_table.remove("Grimmchild2")
            item_table.append("Grimmchild1")

        if self.options.RandomizeElevatorPass:
            item_table.append("Elevator_Pass")

        return item_table

    @staticmethod
    def get_item_classification(name: str) -> ItemClassification:
        progression_charms = {
            # Baldur Killers
            "Grubberfly's_Elegy", "Weaversong", "Glowing_Womb",
            # Spore Shroom spots in fungal wastes and elsewhere
            "Spore_Shroom",
            # Tuk gives egg,
            "Defender's_Crest",
            # Unlocks Grimm Troupe
            "Grimmchild1", "Grimmchild2"
        }

        if name in effects_non_prog:
            classification = ItemClassification.filler
            assert name not in effects_prog_lookup
        elif name in effects_prog_lookup:
            classification = ItemClassification.progression
        else:
            logger.warning(f"unknown item {name} setting to progression")
            classification = ItemClassification.progression
        if name in effects_items_by_term["DREAMER"] or \
                name in effects_items_by_term["GRUBS"] or \
                name in effects_items_by_term["ESSENCE"] or \
                name in effects_items_by_term["RANCIDEGGS"]:
            classification |= ItemClassification.skip_balancing
        if name in ("Pale_Ore", "Arcane_Egg", "King's_Idol", "Hallownest_Seal", "Wanderer's_Journal"):
            classification |= ItemClassification.useful
        if (name not in progression_charms and name in effects_items_by_term["CHARMS"]):
            classification |= ItemClassification.skip_balancing
        if name == "Mimic_Grub" or name == "Quill":
            classification |= ItemClassification.trap

        return classification

    def get_filler_items(self) -> list[str]:
        if not self.cached_filler_items:
            fillers = ["One_Geo", "Soul_Refill"]
            exclusions = self.options.WhitePalace.location_exclusions()
            for group in (
                    "RandomizeGeoRocks", "RandomizeSoulTotems", "RandomizeLoreTablets", "RandomizeJunkPitChests",
                    "RandomizeRancidEggs"
            ):
                if getattr(self.options, group):
                    fillers.extend(item for item in options_pool_mappings[group]["randomized"]["items"] if item not in
                                   exclusions)
            self.cached_filler_items = fillers
        return self.cached_filler_items

    def get_filler_item_name(self) -> str:
        return self.random.choice(self.get_filler_items())

    def handle_starting_inventory(self):
        def precollect(item, code):
            self.push_precollected(self.item_class(item, ItemClassification.progression, code, self.player))
        precollect("Downslash", self.item_name_to_id["Downslash"])
        for option, items in randomizable_starting_items.items():
            if not getattr(self.options, option):
                for item in items:
                    precollect(item, self.item_name_to_id[item])

    def apply_costsanity(self):
        setting = self.options.CostSanity.value
        if not setting:
            return  # noop

        def _compute_weights(weights: dict, desc: str) -> dict[str, int]:
            if all(x == 0 for x in weights.values()):
                logger.warning(
                    f"All {desc} weights were zero for {self.player_name}."
                    f" Setting them to one instead."
                )
                weights = dict.fromkeys(weights, 1)

            return {k: v for k, v in weights.items() if v}

        random = self.random
        hybrid_chance = self.options.CostSanityHybridChance.value
        weights = {
            data.term: getattr(self.options, f"CostSanity{data.option}Weight").value
            for data in cost_terms.values()
        }
        weights_geoless = dict(weights)
        del weights_geoless["GEO"]

        weights = _compute_weights(weights, "CostSanity")
        weights_geoless = _compute_weights(weights_geoless, "Geoless CostSanity")

        if hybrid_chance > 0:
            if len(weights) == 1:
                logger.warning(
                    f"Only one cost type is available for CostSanity in {self.player_name}'s world."
                    f" CostSanityHybridChance will not trigger in geo shop locations."
                )
            if len(weights_geoless) == 1:
                logger.warning(
                    f"Only one cost type is available for CostSanity in {self.player_name}'s world."
                    f" CostSanityHybridChance will not trigger in geoless locations."
                )

        for region in self.get_regions():
            for location in region.locations:
                if location.vanilla:
                    continue
                if not location.costs:
                    continue
                if location.name == "Vessel_Fragment-Basin":
                    continue
                if setting == CostSanity.option_notshops and location.basename in self.created_multi_locations:
                    continue
                if setting == CostSanity.option_shopsonly and location.basename not in self.created_multi_locations:
                    continue
                if location.basename in {"Grubfather", "Seer", "Egg_Shop"}:
                    our_weights = dict(weights_geoless)
                else:
                    our_weights = dict(weights)

                rolls = 1
                if random.randrange(100) < hybrid_chance:
                    rolls = 2

                if rolls > len(our_weights):
                    terms = list(our_weights.keys())  # Can't randomly choose cost types, using all of them.
                else:
                    terms = []
                    for _ in range(rolls):
                        term = random.choices(list(our_weights.keys()), list(our_weights.values()))[0]
                        del our_weights[term]
                        terms.append(term)

                location.costs = {term: random.randint(*self.ranges[term]) for term in terms}
                location.sort_costs()

    def sort_shops_by_cost(self):
        for _, shop_locations in self.created_multi_locations.items():
            randomized_locations = [loc for loc in shop_locations if not loc.vanilla]
            if not randomized_locations:
                continue
            prices = sorted(
                (loc.costs for loc in randomized_locations),
                key=lambda costs: (len(costs), *costs.values(),)
            )
            for loc, costs in zip(randomized_locations, prices, strict=True):
                loc.costs = costs

    # pre_fill
    @classmethod
    def stage_pre_fill(cls, multiworld: MultiWorld):
        worlds = [world for world in multiworld.get_game_worlds(cls.game) if world.options.Goal in ["any", "grub_hunt"]]
        if worlds:
            grubs = [item for item in multiworld.get_items() if item.name == "Grub"]
        all_grub_players = [
            world.player
            for world in worlds
            if world.options.GrubHuntGoal == GrubHuntGoal.special_range_names["all"]
            ]

        if all_grub_players:
            group_lookup = defaultdict(set)
            for group_id, group in multiworld.groups.items():
                for player in group["players"]:
                    group_lookup[group_id].add(player)

            grub_count_per_player = Counter()
            per_player_grubs_per_player = defaultdict(Counter)

            for grub in grubs:
                player = grub.player
                if player in group_lookup:
                    for real_player in group_lookup[player]:
                        per_player_grubs_per_player[real_player][player] += 1
                else:
                    per_player_grubs_per_player[player][player] += 1

                if grub.location and grub.location.player in group_lookup.keys():
                    # will count the item linked grub instead
                    pass
                elif player in group_lookup:
                    for real_player in group_lookup[player]:
                        grub_count_per_player[real_player] += 1
                else:
                    # for non-linked grubs
                    grub_count_per_player[player] += 1

            for player, count in grub_count_per_player.items():
                multiworld.worlds[player].grub_count = count

            for player, grub_player_count in per_player_grubs_per_player.items():
                if player in all_grub_players:
                    multiworld.worlds[player].grub_player_count = grub_player_count

        for world in worlds:
            if world.player not in all_grub_players:
                world.grub_count = world.options.GrubHuntGoal.value
                player = world.player
                world.grub_player_count = {player: world.grub_count}

    def pre_output(self):
        from .data.item_data import geo_cost_caps
        if not self.options.LimitGeoPrices:
            return
        for region in self.get_regions():
            for location in region.locations:
                if location.costs:
                    if location.item.name in geo_cost_caps and "GEO" in location.costs:
                        location.costs["GEO"] = min(location.costs["GEO"], geo_cost_caps[location.item.name])

    # fill_slot_data
    def fill_slot_data(self):
        slot_data = {}

        options = slot_data["options"] = {}
        for option_name in hollow_knight_options:
            option = getattr(self.options, option_name)
            try:
                # exclude more complex types - we only care about int, bool, enum for player options; the client
                # can get them back to the necessary type.
                optionvalue = int(option.value)
                options[option_name] = optionvalue
            except TypeError:
                pass

        slot_data["options"]["StartLocationName"] = trando_starts[self.options.StartLocation.current_key]["logic_name"]
        # slot_data["options"]["EntranceRandoTypeName"] = self.options.EntranceRandoType.current_key

        # 32 bit int
        slot_data["seed"] = self.random.randint(-2147483647, 2147483646)

        # HKAP 0.1.0 and later cost data.
        location_costs = {}
        for region in self.get_regions():
            for location in region.locations:
                if location.costs:
                    location_costs[location.name] = location.costs
        slot_data["location_costs"] = location_costs
        # TODO apply geo caps here and spoiler

        slot_data["notch_costs"] = self.charm_costs

        slot_data["grub_count"] = self.grub_count

        slot_data["is_race"] = self.settings.disable_spoilers or self.multiworld.is_race

        slot_data["entrance_pairs"] = self.entrance_pairs

        return slot_data

    # write_spoiler
    @classmethod
    def stage_write_spoiler(cls, multiworld: MultiWorld, spoiler_handle):
        hk_worlds = multiworld.get_game_worlds(cls.game)
        spoiler_handle.write("\n\nCharm Notches:")
        for hk_world in hk_worlds:
            player = hk_world.player
            name = multiworld.get_player_name(player)
            spoiler_handle.write(f"\n{name}\n")
            for charm_number, cost in enumerate(hk_world.charm_costs):
                spoiler_handle.write(f"\n{charm_names[charm_number]}: {cost}")

        spoiler_handle.write("\n\nShop Prices:")
        for hk_world in hk_worlds:
            player = hk_world.player
            name = hk_world.player_name
            spoiler_handle.write(f"\n{name}\n")

            if hk_world.options.CostSanity.value:
                for loc in sorted(
                    (
                        loc for loc in itertools.chain(*(region.locations for region in hk_world.get_regions()))
                        if loc.costs
                    ), key=operator.attrgetter("name")
                ):
                    spoiler_handle.write(f"\n{loc}: {loc.item} costing {loc.cost_text()}")
            else:
                for _, locations in hk_world.created_multi_locations.items():
                    for loc in locations:
                        spoiler_handle.write(f"\n{loc}: {loc.item} costing {loc.cost_text()}")

    def write_spoiler_end(self, spoiler_handle):
        # Entrance randomization spoiler
        if not self.entrance_pairs:
            return
        spoiler_handle.write(f"\n\n{self.player_name} Entrance Randomization:\n\nONE WAYS:")
        two_ways = set()
        for src, tgt in self.entrance_pairs.items():
            if (src, tgt) in two_ways:
                continue  # already recorded as a two_way
            if self.entrance_pairs.get(tgt) == src:
                two_ways.add((src, tgt))
            else:
                spoiler_handle.write(f"\n{src} -> {tgt}")

        if two_ways:
            spoiler_handle.write("\n\nTWO WAYS:")
            for src, tgt in two_ways:
                spoiler_handle.write(f"\n{src} <-> {tgt}")

    def extend_hint_information(self, hint_data: dict[int, dict[int, str]]) -> None:
        if not self.entrance_pairs:
            return

        hint_data.update({self.player: {}})

        all_state = self.multiworld.get_all_state()

        paths = all_state.path

        transition_names = self.entrance_pairs.keys()
        for loc in self.get_locations():
            path_to_loc = []
            if not loc.parent_region.can_reach(all_state):
                if loc.address is not None:
                    hint_data[self.player][loc.address] = "Unreachable"
                continue
            _, connection = paths[loc.parent_region]
            while connection is not None:
                entrance, (_, connection) = connection
                if entrance in transition_names:
                    path_to_loc.append(entrance)

            text = " => ".join(reversed(path_to_loc))
            # self.spoiler_hints[loc.name] = text
            if loc.address is not None:
                # we want spoiler paths to events but not hint text
                hint_data[self.player][loc.address] = text
