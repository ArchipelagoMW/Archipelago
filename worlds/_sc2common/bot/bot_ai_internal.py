# pylint: disable=W0201,W0212,R0912
from __future__ import annotations

import math
import time
import warnings
from abc import ABC
from collections import Counter
from typing import TYPE_CHECKING, Any
from typing import Dict, Generator, Iterable, List, Set, Tuple, Union, final

from s2clientprotocol import sc2api_pb2 as sc_pb

from .constants import (
    IS_PLACEHOLDER,
)
from .data import Race
from .game_data import GameData
from .game_state import Blip, GameState
from .pixel_map import PixelMap
from .position import Point2
from .unit import Unit
from .units import Units

# with warnings.catch_warnings():
#     warnings.simplefilter("ignore")
#     from scipy.spatial.distance import cdist, pdist

if TYPE_CHECKING:
    from .client import Client
    from .game_info import GameInfo


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


    @final
    def _prepare_first_step(self):
        """First step extra preparations. Must not be called before _prepare_step."""
        if self.townhalls:
            self.game_info.player_start_location = self.townhalls.first.position
            # Calculate and cache expansion locations forever inside 'self._cache_expansion_locations', this is done to prevent a bug when this is run and cached later in the game
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

        index: int = 0
        for unit in self.state.observation_raw.units:
            if unit.is_blip:
                self.blips.add(Blip(unit))
            else:
                unit_type: int = unit.unit_type
                # Convert these units to effects: reaper grenade, parasitic bomb dummy, forcefield
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

    # Helper functions

    @final
    def square_to_condensed(self, i, j) -> int:
        # Converts indices of a square matrix to condensed matrix
        # https://stackoverflow.com/a/36867493/10882657
        assert i != j, "No diagonal elements in condensed matrix! Diagonal elements are zero"
        if i < j:
            i, j = j, i
        return self._units_count * j - j * (j + 1) // 2 + i - 1 - j

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
