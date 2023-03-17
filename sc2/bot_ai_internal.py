# pylint: disable=W0201,W0212,R0912
from __future__ import annotations

import itertools
import math
import time
import warnings
from abc import ABC
from collections import Counter
from contextlib import suppress
from typing import TYPE_CHECKING, Any
from typing import Counter as CounterType
from typing import Dict, Generator, Iterable, List, Set, Tuple, Union, final

import numpy as np
from loguru import logger
from s2clientprotocol import sc2api_pb2 as sc_pb

from sc2.cache import property_cache_once_per_frame
from sc2.constants import (
    ALL_GAS,
    IS_PLACEHOLDER,
    TERRAN_STRUCTURES_REQUIRE_SCV,
    FakeEffectID,
    abilityid_to_unittypeid,
    geyser_ids,
    mineral_ids,
)
from sc2.data import ActionResult, Race, race_townhalls
from sc2.game_data import Cost, GameData
from sc2.game_state import Blip, EffectData, GameState
from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId
from sc2.pixel_map import PixelMap
from sc2.position import Point2
from sc2.unit import Unit
from sc2.unit_command import UnitCommand
from sc2.units import Units

# with warnings.catch_warnings():
#     warnings.simplefilter("ignore")
#     from scipy.spatial.distance import cdist, pdist

if TYPE_CHECKING:
    from sc2.client import Client
    from sc2.game_info import GameInfo


class BotAIInternal(ABC):
    """Base class for bots."""

    @final
    def _initialize_variables(self):
        """ Called from main.py internally """
        self.cache: Dict[str, Any] = {}
        # Specific opponent bot ID used in sc2ai ladder games http://sc2ai.net/ and on ai arena https://aiarena.net
        # The bot ID will stay the same each game so your bot can "adapt" to the opponent
        if not hasattr(self, "opponent_id"):
            # Prevent overwriting the opponent_id which is set here https://github.com/Hannessa/python-sc2-ladderbot/blob/master/__init__.py#L40
            # otherwise set it to None
            self.opponent_id: str = None
        # Select distance calculation method, see _distances_override_functions function
        if not hasattr(self, "distance_calculation_method"):
            self.distance_calculation_method: int = 2
        # Select if the Unit.command should return UnitCommand objects. Set this to True if your bot uses 'self.do(unit(ability, target))'
        if not hasattr(self, "unit_command_uses_self_do"):
            self.unit_command_uses_self_do: bool = False
        # This value will be set to True by main.py in self._prepare_start if game is played in realtime (if true, the bot will have limited time per step)
        self.realtime: bool = False
        self.base_build: int = -1
        self.all_units: Units = Units([], self)
        self.units: Units = Units([], self)
        self.workers: Units = Units([], self)
        self.larva: Units = Units([], self)
        self.structures: Units = Units([], self)
        self.townhalls: Units = Units([], self)
        self.gas_buildings: Units = Units([], self)
        self.all_own_units: Units = Units([], self)
        self.enemy_units: Units = Units([], self)
        self.enemy_structures: Units = Units([], self)
        self.all_enemy_units: Units = Units([], self)
        self.resources: Units = Units([], self)
        self.destructables: Units = Units([], self)
        self.watchtowers: Units = Units([], self)
        self.mineral_field: Units = Units([], self)
        self.vespene_geyser: Units = Units([], self)
        self.placeholders: Units = Units([], self)
        self.techlab_tags: Set[int] = set()
        self.reactor_tags: Set[int] = set()
        self.minerals: int = 50
        self.vespene: int = 0
        self.supply_army: float = 0
        self.supply_workers: float = 12  # Doesn't include workers in production
        self.supply_cap: float = 15
        self.supply_used: float = 12
        self.supply_left: float = 3
        self.idle_worker_count: int = 0
        self.army_count: int = 0
        self.warp_gate_count: int = 0
        self.actions: List[UnitCommand] = []
        self.blips: Set[Blip] = set()
        self.race: Race = None
        self.enemy_race: Race = None
        self._generated_frame = -100
        self._units_created: Counter = Counter()
        self._unit_tags_seen_this_game: Set[int] = set()
        self._units_previous_map: Dict[int, Unit] = {}
        self._structures_previous_map: Dict[int, Unit] = {}
        self._enemy_units_previous_map: Dict[int, Unit] = {}
        self._enemy_structures_previous_map: Dict[int, Unit] = {}
        self._all_units_previous_map: Dict[int, Unit] = {}
        self._previous_upgrades: Set[UpgradeId] = set()
        self._expansion_positions_list: List[Point2] = []
        self._resource_location_to_expansion_position_dict: Dict[Point2, Point2] = {}
        self._time_before_step: float = None
        self._time_after_step: float = None
        self._min_step_time: float = math.inf
        self._max_step_time: float = 0
        self._last_step_step_time: float = 0
        self._total_time_in_on_step: float = 0
        self._total_steps_iterations: int = 0
        # Internally used to keep track which units received an action in this frame, so that self.train() function does not give the same larva two orders - cleared every frame
        self.unit_tags_received_action: Set[int] = set()

    @final
    @property
    def _game_info(self) -> GameInfo:
        """ See game_info.py """
        warnings.warn(
            "Using self._game_info is deprecated and may be removed soon. Please use self.game_info directly.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.game_info

    @final
    @property
    def _game_data(self) -> GameData:
        """ See game_data.py """
        warnings.warn(
            "Using self._game_data is deprecated and may be removed soon. Please use self.game_data directly.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.game_data

    @final
    @property
    def _client(self) -> Client:
        """ See client.py """
        warnings.warn(
            "Using self._client is deprecated and may be removed soon. Please use self.client directly.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.client

    @final
    @property_cache_once_per_frame
    def expansion_locations(self) -> Dict[Point2, Units]:
        """ Same as the function above. """
        assert (
            self._expansion_positions_list
        ), "self._find_expansion_locations() has not been run yet, so accessing the list of expansion locations is pointless."
        warnings.warn(
            "You are using 'self.expansion_locations', please use 'self.expansion_locations_list' (fast) or 'self.expansion_locations_dict' (slow) instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.expansion_locations_dict

    @final
    def _find_expansion_locations(self):
        """ Ran once at the start of the game to calculate expansion locations. """
        # Idea: create a group for every resource, then merge these groups if
        # any resource in a group is closer than a threshold to any resource of another group

        # Distance we group resources by
        resource_spread_threshold: float = 8.5
        # Create a group for every resource
        resource_groups: List[List[Unit]] = [
            [resource] for resource in self.resources
            if resource.name != "MineralField450"  # dont use low mineral count patches
        ]
        # Loop the merging process as long as we change something
        merged_group = True
        while merged_group:
            merged_group = False
            # Check every combination of two groups
            for group_a, group_b in itertools.combinations(resource_groups, 2):
                # Check if any pair of resource of these groups is closer than threshold together
                if any(
                    resource_a.distance_to(resource_b) <= resource_spread_threshold
                    for resource_a, resource_b in itertools.product(group_a, group_b)
                ):
                    # Remove the single groups and add the merged group
                    resource_groups.remove(group_a)
                    resource_groups.remove(group_b)
                    resource_groups.append(group_a + group_b)
                    merged_group = True
                    break
        # Distance offsets we apply to center of each resource group to find expansion position
        offset_range = 7
        offsets = [
            (x, y) for x, y in itertools.product(range(-offset_range, offset_range + 1), repeat=2)
            if 4 < math.hypot(x, y) <= 8
        ]
        # Dict we want to return
        centers = {}
        # For every resource group:
        for resources in resource_groups:
            # Possible expansion points
            amount = len(resources)
            # Calculate center, round and add 0.5 because expansion location will have (x.5, y.5)
            # coordinates because bases have size 5.
            center_x = int(sum(resource.position.x for resource in resources) / amount) + 0.5
            center_y = int(sum(resource.position.y for resource in resources) / amount) + 0.5
            possible_points = (Point2((offset[0] + center_x, offset[1] + center_y)) for offset in offsets)
            # Filter out points that are too near
            possible_points = (
                point for point in possible_points
                # Check if point can be built on
                if self.game_info.placement_grid[point.rounded] == 1
                # Check if all resources have enough space to point
                and all(
                    point.distance_to(resource) >= (7 if resource._proto.unit_type in geyser_ids else 6)
                    for resource in resources
                )
            )
            # Choose best fitting point
            result: Point2 = min(
                possible_points, key=lambda point: sum(point.distance_to(resource_) for resource_ in resources)
            )
            centers[result] = resources
            # Put all expansion locations in a list
            self._expansion_positions_list.append(result)
            # Maps all resource positions to the expansion position
            for resource in resources:
                self._resource_location_to_expansion_position_dict[resource.position] = result

    @final
    def _correct_zerg_supply(self):
        """The client incorrectly rounds zerg supply down instead of up (see
        https://github.com/Blizzard/s2client-proto/issues/123), so self.supply_used
        and friends return the wrong value when there are an odd number of zerglings
        and banelings. This function corrects the bad values."""
        # TODO: remove when Blizzard/sc2client-proto#123 gets fixed.
        half_supply_units = {
            UnitTypeId.ZERGLING,
            UnitTypeId.ZERGLINGBURROWED,
            UnitTypeId.BANELING,
            UnitTypeId.BANELINGBURROWED,
            UnitTypeId.BANELINGCOCOON,
        }
        correction = self.units(half_supply_units).amount % 2
        self.supply_used += correction
        self.supply_army += correction
        self.supply_left -= correction

    @final
    @property_cache_once_per_frame
    def _abilities_all_units(self) -> Tuple[CounterType[AbilityId], Dict[AbilityId, float]]:
        """Cache for the already_pending function, includes protoss units warping in,
        all units in production and all structures, and all morphs"""
        abilities_amount: CounterType[AbilityId] = Counter()
        max_build_progress: Dict[AbilityId, float] = {}
        unit: Unit
        for unit in self.units + self.structures:
            for order in unit.orders:
                abilities_amount[order.ability.exact_id] += 1
            if not unit.is_ready:
                if self.race != Race.Terran or not unit.is_structure:
                    # If an SCV is constructing a building, already_pending would count this structure twice
                    # (once from the SCV order, and once from "not structure.is_ready")
                    if unit.type_id == UnitTypeId.ARCHON:
                        # Hotfix for archons in morph state
                        creation_ability = AbilityId.ARCHON_WARP_TARGET
                        abilities_amount[creation_ability] += 2
                    else:
                        creation_ability: AbilityId = self.game_data.units[unit.type_id.value].creation_ability.exact_id
                        abilities_amount[creation_ability] += 1
                    max_build_progress[creation_ability] = max(
                        max_build_progress.get(creation_ability, 0), unit.build_progress
                    )

        return abilities_amount, max_build_progress

    @final
    @property_cache_once_per_frame
    def _worker_orders(self) -> CounterType[AbilityId]:
        """ This function is used internally, do not use! It is to store all worker abilities. """
        abilities_amount: CounterType[AbilityId] = Counter()
        structures_in_production: Set[Union[Point2, int]] = set()
        for structure in self.structures:
            if structure.type_id in TERRAN_STRUCTURES_REQUIRE_SCV:
                structures_in_production.add(structure.position)
                structures_in_production.add(structure.tag)
        for worker in self.workers:
            for order in worker.orders:
                # Skip if the SCV is constructing (not isinstance(order.target, int))
                # or resuming construction (isinstance(order.target, int))
                if order.target in structures_in_production:
                    continue
                abilities_amount[order.ability.exact_id] += 1
        return abilities_amount

    @final
    def do(
        self,
        action: UnitCommand,
        subtract_cost: bool = False,
        subtract_supply: bool = False,
        can_afford_check: bool = False,
        ignore_warning: bool = False,
    ) -> bool:
        """Adds a unit action to the 'self.actions' list which is then executed at the end of the frame.

        Training a unit::

            # Train an SCV from a random idle command center
            cc = self.townhalls.idle.random_or(None)
            # self.townhalls can be empty or there are no idle townhalls
            if cc and self.can_afford(UnitTypeId.SCV):
                cc.train(UnitTypeId.SCV)

        Building a building::

            # Building a barracks at the main ramp, requires 150 minerals and a depot
            worker = self.workers.random_or(None)
            barracks_placement_position = self.main_base_ramp.barracks_correct_placement
            if worker and self.can_afford(UnitTypeId.BARRACKS):
                worker.build(UnitTypeId.BARRACKS, barracks_placement_position)

        Moving a unit::

            # Move a random worker to the center of the map
            worker = self.workers.random_or(None)
            # worker can be None if all are dead
            if worker:
                worker.move(self.game_info.map_center)

        :param action:
        :param subtract_cost:
        :param subtract_supply:
        :param can_afford_check:
        """
        if not self.unit_command_uses_self_do and isinstance(action, bool):
            if not ignore_warning:
                warnings.warn(
                    "You have used self.do(). Please consider putting 'self.unit_command_uses_self_do = True' in your bot __init__() function or removing self.do().",
                    DeprecationWarning,
                    stacklevel=2,
                )
            return action

        assert isinstance(
            action, UnitCommand
        ), f"Given unit command is not a command, but instead of type {type(action)}"
        if subtract_cost:
            cost: Cost = self.game_data.calculate_ability_cost(action.ability)
            if can_afford_check and not (self.minerals >= cost.minerals and self.vespene >= cost.vespene):
                # Dont do action if can't afford
                return False
            self.minerals -= cost.minerals
            self.vespene -= cost.vespene
        if subtract_supply and action.ability in abilityid_to_unittypeid:
            unit_type = abilityid_to_unittypeid[action.ability]
            required_supply = self.calculate_supply_cost(unit_type)
            # Overlord has -8
            if required_supply > 0:
                self.supply_used += required_supply
                self.supply_left -= required_supply
        self.actions.append(action)
        self.unit_tags_received_action.add(action.unit.tag)
        return True

    @final
    async def synchronous_do(self, action: UnitCommand):
        """
        Not recommended. Use self.do instead to reduce lag.
        This function is only useful for realtime=True in the first frame of the game to instantly produce a worker
        and split workers on the mineral patches.
        """
        assert isinstance(
            action, UnitCommand
        ), f"Given unit command is not a command, but instead of type {type(action)}"
        if not self.can_afford(action.ability):
            logger.warning(f"Cannot afford action {action}")
            return ActionResult.Error
        r = await self.client.actions(action)
        if not r:  # success
            cost = self.game_data.calculate_ability_cost(action.ability)
            self.minerals -= cost.minerals
            self.vespene -= cost.vespene
            self.unit_tags_received_action.add(action.unit.tag)
        else:
            logger.error(f"Error: {r} (action: {action})")
        return r

    @final
    async def _do_actions(self, actions: List[UnitCommand], prevent_double: bool = True):
        """Used internally by main.py automatically, use self.do() instead!

        :param actions:
        :param prevent_double:"""
        if not actions:
            return None
        if prevent_double:
            actions = list(filter(self.prevent_double_actions, actions))
        result = await self.client.actions(actions)
        return result

    @final
    @staticmethod
    def prevent_double_actions(action) -> bool:
        """
        :param action:
        """
        # Always add actions if queued
        if action.queue:
            return True
        if action.unit.orders:
            # action: UnitCommand
            # current_action: UnitOrder
            current_action = action.unit.orders[0]
            if action.ability not in {current_action.ability.id, current_action.ability.exact_id}:
                # Different action, return True
                return True
            with suppress(AttributeError):
                if current_action.target == action.target.tag:
                    # Same action, remove action if same target unit
                    return False
            with suppress(AttributeError):
                if action.target.x == current_action.target.x and action.target.y == current_action.target.y:
                    # Same action, remove action if same target position
                    return False
            return True
        return True

    @final
    def _prepare_start(self, client, player_id, game_info, game_data, realtime: bool = False, base_build: int = -1):
        """
        Ran until game start to set game and player data.

        :param client:
        :param player_id:
        :param game_info:
        :param game_data:
        :param realtime:
        """
        self.client: Client = client
        self.player_id: int = player_id
        self.game_info: GameInfo = game_info
        self.game_data: GameData = game_data
        self.realtime: bool = realtime
        self.base_build: int = base_build

        self.race: Race = Race(self.game_info.player_races[self.player_id])

        if len(self.game_info.player_races) == 2:
            self.enemy_race: Race = Race(self.game_info.player_races[3 - self.player_id])

        self._distances_override_functions(self.distance_calculation_method)

    @final
    def _prepare_first_step(self):
        """First step extra preparations. Must not be called before _prepare_step."""
        if self.townhalls:
            self.game_info.player_start_location = self.townhalls.first.position
            # Calculate and cache expansion locations forever inside 'self._cache_expansion_locations', this is done to prevent a bug when this is run and cached later in the game
            self._find_expansion_locations()
        self.game_info.map_ramps, self.game_info.vision_blockers = self.game_info._find_ramps_and_vision_blockers()
        self._time_before_step: float = time.perf_counter()

    @final
    def _prepare_step(self, state, proto_game_info):
        """
        :param state:
        :param proto_game_info:
        """
        # Set attributes from new state before on_step."""
        self.state: GameState = state  # See game_state.py
        # update pathing grid, which unfortunately is in GameInfo instead of GameState
        self.game_info.pathing_grid = PixelMap(proto_game_info.game_info.start_raw.pathing_grid, in_bits=True)
        # Required for events, needs to be before self.units are initialized so the old units are stored
        self._units_previous_map: Dict[int, Unit] = {unit.tag: unit for unit in self.units}
        self._structures_previous_map: Dict[int, Unit] = {structure.tag: structure for structure in self.structures}
        self._enemy_units_previous_map: Dict[int, Unit] = {unit.tag: unit for unit in self.enemy_units}
        self._enemy_structures_previous_map: Dict[int, Unit] = {
            structure.tag: structure
            for structure in self.enemy_structures
        }
        self._all_units_previous_map: Dict[int, Unit] = {unit.tag: unit for unit in self.all_units}

        self._prepare_units()
        self.minerals: int = state.common.minerals
        self.vespene: int = state.common.vespene
        self.supply_army: int = state.common.food_army
        self.supply_workers: int = state.common.food_workers  # Doesn't include workers in production
        self.supply_cap: int = state.common.food_cap
        self.supply_used: int = state.common.food_used
        self.supply_left: int = self.supply_cap - self.supply_used

        if self.race == Race.Zerg:
            # Workaround Zerg supply rounding bug
            pass
            # self._correct_zerg_supply()
        elif self.race == Race.Protoss:
            self.warp_gate_count: int = state.common.warp_gate_count

        self.idle_worker_count: int = state.common.idle_worker_count
        self.army_count: int = state.common.army_count
        self._time_before_step: float = time.perf_counter()

        if self.enemy_race == Race.Random and self.all_enemy_units:
            self.enemy_race = Race(self.all_enemy_units.first.race)

    @final
    def _prepare_units(self):
        # Set of enemy units detected by own sensor tower, as blips have less unit information than normal visible units
        self.blips: Set[Blip] = set()
        self.all_units: Units = Units([], self)
        self.units: Units = Units([], self)
        self.workers: Units = Units([], self)
        self.larva: Units = Units([], self)
        self.structures: Units = Units([], self)
        self.townhalls: Units = Units([], self)
        self.gas_buildings: Units = Units([], self)
        self.all_own_units: Units = Units([], self)
        self.enemy_units: Units = Units([], self)
        self.enemy_structures: Units = Units([], self)
        self.all_enemy_units: Units = Units([], self)
        self.resources: Units = Units([], self)
        self.destructables: Units = Units([], self)
        self.watchtowers: Units = Units([], self)
        self.mineral_field: Units = Units([], self)
        self.vespene_geyser: Units = Units([], self)
        self.placeholders: Units = Units([], self)
        self.techlab_tags: Set[int] = set()
        self.reactor_tags: Set[int] = set()

        worker_types: Set[UnitTypeId] = {UnitTypeId.DRONE, UnitTypeId.DRONEBURROWED, UnitTypeId.SCV, UnitTypeId.PROBE}

        index: int = 0
        for unit in self.state.observation_raw.units:
            if unit.is_blip:
                self.blips.add(Blip(unit))
            else:
                unit_type: int = unit.unit_type
                # Convert these units to effects: reaper grenade, parasitic bomb dummy, forcefield
                if unit_type in FakeEffectID:
                    self.state.effects.add(EffectData(unit, fake=True))
                    continue
                unit_obj = Unit(unit, self, distance_calculation_index=index, base_build=self.base_build)
                index += 1
                self.all_units.append(unit_obj)
                if unit.display_type == IS_PLACEHOLDER:
                    self.placeholders.append(unit_obj)
                    continue
                alliance = unit.alliance
                # Alliance.Neutral.value = 3
                if alliance == 3:
                    # XELNAGATOWER = 149
                    if unit_type == 149:
                        self.watchtowers.append(unit_obj)
                    # mineral field enums
                    elif unit_type in mineral_ids:
                        self.mineral_field.append(unit_obj)
                        self.resources.append(unit_obj)
                    # geyser enums
                    elif unit_type in geyser_ids:
                        self.vespene_geyser.append(unit_obj)
                        self.resources.append(unit_obj)
                    # all destructable rocks
                    else:
                        self.destructables.append(unit_obj)
                # Alliance.Self.value = 1
                elif alliance == 1:
                    self.all_own_units.append(unit_obj)
                    if unit_obj.is_structure:
                        self.structures.append(unit_obj)
                # Alliance.Enemy.value = 4
                elif alliance == 4:
                    self.all_enemy_units.append(unit_obj)
                    if unit_obj.is_structure:
                        self.enemy_structures.append(unit_obj)
                    else:
                        self.enemy_units.append(unit_obj)

        # Force distance calculation and caching on all units using scipy pdist or cdist
        if self.distance_calculation_method == 1:
            _ = self._pdist
        elif self.distance_calculation_method in {2, 3}:
            _ = self._cdist

    @final
    async def _after_step(self) -> int:
        """ Executed by main.py after each on_step function. """
        # Keep track of the bot on_step duration
        self._time_after_step: float = time.perf_counter()
        step_duration = self._time_after_step - self._time_before_step
        self._min_step_time = min(step_duration, self._min_step_time)
        self._max_step_time = max(step_duration, self._max_step_time)
        self._last_step_step_time = step_duration
        self._total_time_in_on_step += step_duration
        self._total_steps_iterations += 1
        # Commit and clear bot actions
        if self.actions:
            await self._do_actions(self.actions)
            self.actions.clear()
        # Clear set of unit tags that were given an order this frame by self.do()
        self.unit_tags_received_action.clear()
        # Commit debug queries
        await self.client._send_debug()

        return self.state.game_loop

    @final
    async def _advance_steps(self, steps: int):
        """Advances the game loop by amount of 'steps'. This function is meant to be used as a debugging and testing tool only.
        If you are using this, please be aware of the consequences, e.g. 'self.units' will be filled with completely new data."""
        await self._after_step()
        # Advance simulation by exactly "steps" frames
        await self.client.step(steps)
        state = await self.client.observation()
        gs = GameState(state.observation)
        proto_game_info = await self.client._execute(game_info=sc_pb.RequestGameInfo())
        self._prepare_step(gs, proto_game_info)
        await self.issue_events()

    @final
    async def issue_events(self):
        """This function will be automatically run from main.py and triggers the following functions:
        - on_unit_created
        - on_unit_destroyed
        - on_building_construction_started
        - on_building_construction_complete
        - on_upgrade_complete
        """
        await self._issue_unit_dead_events()
        await self._issue_unit_added_events()
        await self._issue_building_events()
        await self._issue_upgrade_events()
        await self._issue_vision_events()

    @final
    async def _issue_unit_added_events(self):
        pass
        # for unit in self.units:
        #     if unit.tag not in self._units_previous_map and unit.tag not in self._unit_tags_seen_this_game:
        #         self._unit_tags_seen_this_game.add(unit.tag)
        #         self._units_created[unit.type_id] += 1
        #         await self.on_unit_created(unit)
        #     elif unit.tag in self._units_previous_map:
        #         previous_frame_unit: Unit = self._units_previous_map[unit.tag]
        #         # Check if a unit took damage this frame and then trigger event
        #         if unit.health < previous_frame_unit.health or unit.shield < previous_frame_unit.shield:
        #             damage_amount = previous_frame_unit.health - unit.health + previous_frame_unit.shield - unit.shield
        #             await self.on_unit_took_damage(unit, damage_amount)
        #         # Check if a unit type has changed
        #         if previous_frame_unit.type_id != unit.type_id:
        #             await self.on_unit_type_changed(unit, previous_frame_unit.type_id)

    @final
    async def _issue_upgrade_events(self):
        pass
        # difference = self.state.upgrades - self._previous_upgrades
        # for upgrade_completed in difference:
        #     await self.on_upgrade_complete(upgrade_completed)
        # self._previous_upgrades = self.state.upgrades

    @final
    async def _issue_building_events(self):
        pass
        # for structure in self.structures:
        #     if structure.tag not in self._structures_previous_map:
        #         if structure.build_progress < 1:
        #             await self.on_building_construction_started(structure)
        #         else:
        #             # Include starting townhall
        #             self._units_created[structure.type_id] += 1
        #             await self.on_building_construction_complete(structure)
        #     elif structure.tag in self._structures_previous_map:
        #         # Check if a structure took damage this frame and then trigger event
        #         previous_frame_structure: Unit = self._structures_previous_map[structure.tag]
        #         if (
        #             structure.health < previous_frame_structure.health
        #             or structure.shield < previous_frame_structure.shield
        #         ):
        #             damage_amount = (
        #                 previous_frame_structure.health - structure.health + previous_frame_structure.shield -
        #                 structure.shield
        #             )
        #             await self.on_unit_took_damage(structure, damage_amount)
        #         # Check if a structure changed its type
        #         if previous_frame_structure.type_id != structure.type_id:
        #             await self.on_unit_type_changed(structure, previous_frame_structure.type_id)
        #         # Check if structure completed
        #         if structure.build_progress == 1 and previous_frame_structure.build_progress < 1:
        #             self._units_created[structure.type_id] += 1
        #             await self.on_building_construction_complete(structure)

    @final
    async def _issue_vision_events(self):
        pass
        # # Call events for enemy unit entered vision
        # for enemy_unit in self.enemy_units:
        #     if enemy_unit.tag not in self._enemy_units_previous_map:
        #         await self.on_enemy_unit_entered_vision(enemy_unit)
        # for enemy_structure in self.enemy_structures:
        #     if enemy_structure.tag not in self._enemy_structures_previous_map:
        #         await self.on_enemy_unit_entered_vision(enemy_structure)

        # # Call events for enemy unit left vision
        # enemy_units_left_vision: Set[int] = set(self._enemy_units_previous_map) - self.enemy_units.tags
        # for enemy_unit_tag in enemy_units_left_vision:
        #     await self.on_enemy_unit_left_vision(enemy_unit_tag)
        # enemy_structures_left_vision: Set[int] = (set(self._enemy_structures_previous_map) - self.enemy_structures.tags)
        # for enemy_structure_tag in enemy_structures_left_vision:
        #     await self.on_enemy_unit_left_vision(enemy_structure_tag)

    @final
    async def _issue_unit_dead_events(self):
        pass
        # for unit_tag in self.state.dead_units & set(self._all_units_previous_map):
        #     await self.on_unit_destroyed(unit_tag)

    # DISTANCE CALCULATION

    @final
    @property
    def _units_count(self) -> int:
        return len(self.all_units)

    @final
    @property
    def _pdist(self) -> np.ndarray:
        """ As property, so it will be recalculated each time it is called, or return from cache if it is called multiple times in teh same game_loop. """
        if self._generated_frame != self.state.game_loop:
            return self.calculate_distances()
        return self._cached_pdist

    @final
    @property
    def _cdist(self) -> np.ndarray:
        """ As property, so it will be recalculated each time it is called, or return from cache if it is called multiple times in teh same game_loop. """
        if self._generated_frame != self.state.game_loop:
            return self.calculate_distances()
        return self._cached_cdist

    @final
    def _calculate_distances_method1(self) -> np.ndarray:
        self._generated_frame = self.state.game_loop
        # Converts tuple [(1, 2), (3, 4)] to flat list like [1, 2, 3, 4]
        flat_positions = (coord for unit in self.all_units for coord in unit.position_tuple)
        # Converts to numpy array, then converts the flat array back to shape (n, 2): [[1, 2], [3, 4]]
        positions_array: np.ndarray = np.fromiter(
            flat_positions,
            dtype=float,
            count=2 * self._units_count,
        ).reshape((self._units_count, 2))
        assert len(positions_array) == self._units_count
        # See performance benchmarks
        self._cached_pdist = 0 #pdist(positions_array, "sqeuclidean")

        return self._cached_pdist

    @final
    def _calculate_distances_method2(self) -> np.ndarray:
        self._generated_frame = self.state.game_loop
        # Converts tuple [(1, 2), (3, 4)] to flat list like [1, 2, 3, 4]
        flat_positions = (coord for unit in self.all_units for coord in unit.position_tuple)
        # Converts to numpy array, then converts the flat array back to shape (n, 2): [[1, 2], [3, 4]]
        positions_array: np.ndarray = np.fromiter(
            flat_positions,
            dtype=float,
            count=2 * self._units_count,
        ).reshape((self._units_count, 2))
        assert len(positions_array) == self._units_count
        # See performance benchmarks
        self._cached_cdist = 0 #cdist(positions_array, positions_array, "sqeuclidean")

        return self._cached_cdist

    @final
    def _calculate_distances_method3(self) -> np.ndarray:
        """ Nearly same as above, but without asserts"""
        self._generated_frame = self.state.game_loop
        flat_positions = (coord for unit in self.all_units for coord in unit.position_tuple)
        positions_array: np.ndarray = np.fromiter(
            flat_positions,
            dtype=float,
            count=2 * self._units_count,
        ).reshape((-1, 2))
        # See performance benchmarks
        self._cached_cdist = 0 #cdist(positions_array, positions_array, "sqeuclidean")

        return self._cached_cdist

    # Helper functions

    @final
    def square_to_condensed(self, i, j) -> int:
        # Converts indices of a square matrix to condensed matrix
        # https://stackoverflow.com/a/36867493/10882657
        assert i != j, "No diagonal elements in condensed matrix! Diagonal elements are zero"
        if i < j:
            i, j = j, i
        return self._units_count * j - j * (j + 1) // 2 + i - 1 - j

    @final
    @staticmethod
    def convert_tuple_to_numpy_array(pos: Tuple[float, float]) -> np.ndarray:
        """ Converts a single position to a 2d numpy array with 1 row and 2 columns. """
        return np.fromiter(pos, dtype=float, count=2).reshape((1, 2))

    # Fast and simple calculation functions

    @final
    @staticmethod
    def distance_math_hypot(
        p1: Union[Tuple[float, float], Point2],
        p2: Union[Tuple[float, float], Point2],
    ) -> float:
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    @final
    @staticmethod
    def distance_math_hypot_squared(
        p1: Union[Tuple[float, float], Point2],
        p2: Union[Tuple[float, float], Point2],
    ) -> float:
        return pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2)

    @final
    def _distance_squared_unit_to_unit_method0(self, unit1: Unit, unit2: Unit) -> float:
        return self.distance_math_hypot_squared(unit1.position_tuple, unit2.position_tuple)

    # Distance calculation using the pre-calculated matrix above

    @final
    def _distance_squared_unit_to_unit_method1(self, unit1: Unit, unit2: Unit) -> float:
        # If checked on units if they have the same tag, return distance 0 as these are not in the 1 dimensional pdist array - would result in an error otherwise
        if unit1.tag == unit2.tag:
            return 0
        # Calculate index, needs to be after pdist has been calculated and cached
        condensed_index = self.square_to_condensed(unit1.distance_calculation_index, unit2.distance_calculation_index)
        assert condensed_index < len(
            self._cached_pdist
        ), f"Condensed index is larger than amount of calculated distances: {condensed_index} < {len(self._cached_pdist)}, units that caused the assert error: {unit1} and {unit2}"
        distance = self._pdist[condensed_index]
        return distance

    @final
    def _distance_squared_unit_to_unit_method2(self, unit1: Unit, unit2: Unit) -> float:
        # Calculate index, needs to be after cdist has been calculated and cached
        return self._cdist[unit1.distance_calculation_index, unit2.distance_calculation_index]

    # Distance calculation using the fastest distance calculation functions

    @final
    def _distance_pos_to_pos(
        self,
        pos1: Union[Tuple[float, float], Point2],
        pos2: Union[Tuple[float, float], Point2],
    ) -> float:
        return self.distance_math_hypot(pos1, pos2)

    @final
    def _distance_units_to_pos(
        self,
        units: Units,
        pos: Union[Tuple[float, float], Point2],
    ) -> Generator[float, None, None]:
        """ This function does not scale well, if len(units) > 100 it gets fairly slow """
        return (self.distance_math_hypot(u.position_tuple, pos) for u in units)

    @final
    def _distance_unit_to_points(
        self,
        unit: Unit,
        points: Iterable[Tuple[float, float]],
    ) -> Generator[float, None, None]:
        """ This function does not scale well, if len(points) > 100 it gets fairly slow """
        pos = unit.position_tuple
        return (self.distance_math_hypot(p, pos) for p in points)

    @final
    def _distances_override_functions(self, method: int = 0):
        """Overrides the internal distance calculation functions at game start in bot_ai.py self._prepare_start() function
        method 0: Use python's math.hypot
        The following methods calculate the distances between all units once:
        method 1: Use scipy's pdist condensed matrix (1d array)
        method 2: Use scipy's cidst square matrix (2d array)
        method 3: Use scipy's cidst square matrix (2d array) without asserts (careful: very weird error messages, but maybe slightly faster)"""
        assert 0 <= method <= 3, f"Selected method was: {method}"
        if method == 0:
            self._distance_squared_unit_to_unit = self._distance_squared_unit_to_unit_method0
        elif method == 1:
            self._distance_squared_unit_to_unit = self._distance_squared_unit_to_unit_method1
            self.calculate_distances = self._calculate_distances_method1
        elif method == 2:
            self._distance_squared_unit_to_unit = self._distance_squared_unit_to_unit_method2
            self.calculate_distances = self._calculate_distances_method2
        elif method == 3:
            self._distance_squared_unit_to_unit = self._distance_squared_unit_to_unit_method2
            self.calculate_distances = self._calculate_distances_method3
