# pylint: disable=W0212,R0916,R0904
from __future__ import annotations

import math
from functools import cached_property
from typing import TYPE_CHECKING, Dict, List, Optional, Set, Tuple, Union

from .bot_ai_internal import BotAIInternal
from .cache import property_cache_once_per_frame
from .data import Alert, Result
from .position import Point2
from .unit import Unit
from .units import Units

if TYPE_CHECKING:
    from .game_info import Ramp


class BotAI(BotAIInternal):
    """Base class for bots."""

    EXPANSION_GAP_THRESHOLD = 15

    @property
    def time(self) -> float:
        """ Returns time in seconds, assumes the game is played on 'faster' """
        return self.state.game_loop / 22.4  # / (1/1.4) * (1/16)

    @property
    def time_formatted(self) -> str:
        """ Returns time as string in min:sec format """
        t = self.time
        return f"{int(t // 60):02}:{int(t % 60):02}"

    @property
    def step_time(self) -> Tuple[float, float, float, float]:
        """Returns a tuple of step duration in milliseconds.
        First value is the minimum step duration - the shortest the bot ever took
        Second value is the average step duration
        Third value is the maximum step duration - the longest the bot ever took (including on_start())
        Fourth value is the step duration the bot took last iteration
        If called in the first iteration, it returns (inf, 0, 0, 0)"""
        avg_step_duration = (
            (self._total_time_in_on_step / self._total_steps_iterations) if self._total_steps_iterations else 0
        )
        return (
            self._min_step_time * 1000,
            avg_step_duration * 1000,
            self._max_step_time * 1000,
            self._last_step_step_time * 1000,
        )

    def alert(self, alert_code: Alert) -> bool:
        """
        Check if alert is triggered in the current step.
        Possible alerts are listed here https://github.com/Blizzard/s2client-proto/blob/e38efed74c03bec90f74b330ea1adda9215e655f/s2clientprotocol/sc2api.proto#L679-L702

        Example use::

            from sc2.data import Alert
            if self.alert(Alert.AddOnComplete):
                print("Addon Complete")

        Alert codes::

            AlertError
            AddOnComplete
            BuildingComplete
            BuildingUnderAttack
            LarvaHatched
            MergeComplete
            MineralsExhausted
            MorphComplete
            MothershipComplete
            MULEExpired
            NuclearLaunchDetected
            NukeComplete
            NydusWormDetected
            ResearchComplete
            TrainError
            TrainUnitComplete
            TrainWorkerComplete
            TransformationComplete
            UnitUnderAttack
            UpgradeComplete
            VespeneExhausted
            WarpInComplete

        :param alert_code:
        """
        assert isinstance(alert_code, Alert), f"alert_code {alert_code} is no Alert"
        return alert_code.value in self.state.alerts

    @property
    def start_location(self) -> Point2:
        """
        Returns the spawn location of the bot, using the position of the first created townhall.
        This will be None if the bot is run on an arcade or custom map that does not feature townhalls at game start.
        """
        return self.game_info.player_start_location

    @property
    def enemy_start_locations(self) -> List[Point2]:
        """Possible start locations for enemies."""
        return self.game_info.start_locations

    @cached_property
    def main_base_ramp(self) -> Ramp:
        """Returns the Ramp instance of the closest main-ramp to start location.
        Look in game_info.py for more information about the Ramp class

        Example: See terran ramp wall bot
        """
        # The reason for len(ramp.upper) in {2, 5} is:
        # ParaSite map has 5 upper points, and most other maps have 2 upper points at the main ramp.
        # The map Acolyte has 4 upper points at the wrong ramp (which is closest to the start position).
        try:
            found_main_base_ramp = min(
                (ramp for ramp in self.game_info.map_ramps if len(ramp.upper) in {2, 5}),
                key=lambda r: self.start_location.distance_to(r.top_center),
            )
        except ValueError:
            # Hardcoded hotfix for Honorgrounds LE map, as that map has a large main base ramp with inbase natural
            found_main_base_ramp = min(
                (ramp for ramp in self.game_info.map_ramps if len(ramp.upper) in {4, 9}),
                key=lambda r: self.start_location.distance_to(r.top_center),
            )
        return found_main_base_ramp

    @property_cache_once_per_frame
    def expansion_locations_list(self) -> List[Point2]:
        """ Returns a list of expansion positions, not sorted in any way. """
        assert (
            self._expansion_positions_list
        ), "self._find_expansion_locations() has not been run yet, so accessing the list of expansion locations is pointless."
        return self._expansion_positions_list

    @property_cache_once_per_frame
    def expansion_locations_dict(self) -> Dict[Point2, Units]:
        """
        Returns dict with the correct expansion position Point2 object as key,
        resources as Units (mineral fields and vespene geysers) as value.

        Caution: This function is slow. If you only need the expansion locations, use the property above.
        """
        assert (
            self._expansion_positions_list
        ), "self._find_expansion_locations() has not been run yet, so accessing the list of expansion locations is pointless."
        expansion_locations: Dict[Point2, Units] = {pos: Units([], self) for pos in self._expansion_positions_list}
        for resource in self.resources:
            # It may be that some resources are not mapped to an expansion location
            exp_position: Point2 = self._resource_location_to_expansion_position_dict.get(resource.position, None)
            if exp_position:
                assert exp_position in expansion_locations
                expansion_locations[exp_position].append(resource)
        return expansion_locations

    async def get_next_expansion(self) -> Optional[Point2]:
        """Find next expansion location."""

        closest = None
        distance = math.inf
        for el in self.expansion_locations_list:

            def is_near_to_expansion(t):
                return t.distance_to(el) < self.EXPANSION_GAP_THRESHOLD

            if any(map(is_near_to_expansion, self.townhalls)):
                # already taken
                continue

            startp = self.game_info.player_start_location
            d = await self.client.query_pathing(startp, el)
            if d is None:
                continue

            if d < distance:
                distance = d
                closest = el

        return closest

    # pylint: disable=R0912
    async def distribute_workers(self, resource_ratio: float = 2):
        """
        Distributes workers across all the bases taken.
        Keyword `resource_ratio` takes a float. If the current minerals to gas
        ratio is bigger than `resource_ratio`, this function prefer filling gas_buildings
        first, if it is lower, it will prefer sending workers to minerals first.

        NOTE: This function is far from optimal, if you really want to have
        refined worker control, you should write your own distribution function.
        For example long distance mining control and moving workers if a base was killed
        are not being handled.

        WARNING: This is quite slow when there are lots of workers or multiple bases.

        :param resource_ratio:"""
        if not self.mineral_field or not self.workers or not self.townhalls.ready:
            return
        worker_pool = self.workers.idle
        bases = self.townhalls.ready
        gas_buildings = self.gas_buildings.ready

        # list of places that need more workers
        deficit_mining_places = []

        for mining_place in bases | gas_buildings:
            difference = mining_place.surplus_harvesters
            # perfect amount of workers, skip mining place
            if not difference:
                continue
            if mining_place.has_vespene:
                # get all workers that target the gas extraction site
                # or are on their way back from it
                local_workers = self.workers.filter(
                    lambda unit: unit.order_target == mining_place.tag or
                    (unit.is_carrying_vespene and unit.order_target == bases.closest_to(mining_place).tag)
                )
            else:
                # get tags of minerals around expansion
                local_minerals_tags = {
                    mineral.tag
                    for mineral in self.mineral_field if mineral.distance_to(mining_place) <= 8
                }
                # get all target tags a worker can have
                # tags of the minerals he could mine at that base
                # get workers that work at that gather site
                local_workers = self.workers.filter(
                    lambda unit: unit.order_target in local_minerals_tags or
                    (unit.is_carrying_minerals and unit.order_target == mining_place.tag)
                )
            # too many workers
            if difference > 0:
                for worker in local_workers[:difference]:
                    worker_pool.append(worker)
            # too few workers
            # add mining place to deficit bases for every missing worker
            else:
                deficit_mining_places += [mining_place for _ in range(-difference)]

        # prepare all minerals near a base if we have too many workers
        # and need to send them to the closest patch
        if len(worker_pool) > len(deficit_mining_places):
            all_minerals_near_base = [
                mineral for mineral in self.mineral_field
                if any(mineral.distance_to(base) <= 8 for base in self.townhalls.ready)
            ]
        # distribute every worker in the pool
        for worker in worker_pool:
            # as long as have workers and mining places
            if deficit_mining_places:
                # choose only mineral fields first if current mineral to gas ratio is less than target ratio
                if self.vespene and self.minerals / self.vespene < resource_ratio:
                    possible_mining_places = [place for place in deficit_mining_places if not place.vespene_contents]
                # else prefer gas
                else:
                    possible_mining_places = [place for place in deficit_mining_places if place.vespene_contents]
                # if preferred type is not available any more, get all other places
                if not possible_mining_places:
                    possible_mining_places = deficit_mining_places
                # find closest mining place
                current_place = min(deficit_mining_places, key=lambda place: place.distance_to(worker))
                # remove it from the list
                deficit_mining_places.remove(current_place)
                # if current place is a gas extraction site, go there
                if current_place.vespene_contents:
                    worker.gather(current_place)
                # if current place is a gas extraction site,
                # go to the mineral field that is near and has the most minerals left
                else:
                    local_minerals = (
                        mineral for mineral in self.mineral_field if mineral.distance_to(current_place) <= 8
                    )
                    # local_minerals can be empty if townhall is misplaced
                    target_mineral = max(local_minerals, key=lambda mineral: mineral.mineral_contents, default=None)
                    if target_mineral:
                        worker.gather(target_mineral)
            # more workers to distribute than free mining spots
            # send to closest if worker is doing nothing
            elif worker.is_idle and all_minerals_near_base:
                target_mineral = min(all_minerals_near_base, key=lambda mineral: mineral.distance_to(worker))
                worker.gather(target_mineral)
            else:
                # there are no deficit mining places and worker is not idle
                # so dont move him
                pass

    @property_cache_once_per_frame
    def owned_expansions(self) -> Dict[Point2, Unit]:
        """Dict of expansions owned by the player with mapping {expansion_location: townhall_structure}."""
        owned = {}
        for el in self.expansion_locations_list:

            def is_near_to_expansion(t):
                return t.distance_to(el) < self.EXPANSION_GAP_THRESHOLD

            th = next((x for x in self.townhalls if is_near_to_expansion(x)), None)
            if th:
                owned[el] = th
        return owned

    async def chat_send(self, message: str, team_only: bool = False):
        """Send a chat message to the SC2 Client.

        Example::

            await self.chat_send("Hello, this is a message from my bot!")

        :param message:
        :param team_only:"""
        assert isinstance(message, str), f"{message} is not a string"
        await self.client.chat_send(message, team_only)

    def in_map_bounds(self, pos: Union[Point2, tuple, list]) -> bool:
        """Tests if a 2 dimensional point is within the map boundaries of the pixelmaps.

        :param pos:"""
        return (
            self.game_info.playable_area.x <= pos[0] <
            self.game_info.playable_area.x + self.game_info.playable_area.width and self.game_info.playable_area.y <=
            pos[1] < self.game_info.playable_area.y + self.game_info.playable_area.height
        )

    # For the functions below, make sure you are inside the boundaries of the map size.
    def get_terrain_height(self, pos: Union[Point2, Unit]) -> int:
        """Returns terrain height at a position.
        Caution: terrain height is different from a unit's z-coordinate.

        :param pos:"""
        assert isinstance(pos, (Point2, Unit)), "pos is not of type Point2 or Unit"
        pos = pos.position.rounded
        return self.game_info.terrain_height[pos]

    def get_terrain_z_height(self, pos: Union[Point2, Unit]) -> float:
        """Returns terrain z-height at a position.

        :param pos:"""
        assert isinstance(pos, (Point2, Unit)), "pos is not of type Point2 or Unit"
        pos = pos.position.rounded
        return -16 + 32 * self.game_info.terrain_height[pos] / 255

    def in_placement_grid(self, pos: Union[Point2, Unit]) -> bool:
        """Returns True if you can place something at a position.
        Remember, buildings usually use 2x2, 3x3 or 5x5 of these grid points.
        Caution: some x and y offset might be required, see ramp code in game_info.py

        :param pos:"""
        assert isinstance(pos, (Point2, Unit)), "pos is not of type Point2 or Unit"
        pos = pos.position.rounded
        return self.game_info.placement_grid[pos] == 1

    def in_pathing_grid(self, pos: Union[Point2, Unit]) -> bool:
        """Returns True if a ground unit can pass through a grid point.

        :param pos:"""
        assert isinstance(pos, (Point2, Unit)), "pos is not of type Point2 or Unit"
        pos = pos.position.rounded
        return self.game_info.pathing_grid[pos] == 1

    def is_visible(self, pos: Union[Point2, Unit]) -> bool:
        """Returns True if you have vision on a grid point.

        :param pos:"""
        # more info: https://github.com/Blizzard/s2client-proto/blob/9906df71d6909511907d8419b33acc1a3bd51ec0/s2clientprotocol/spatial.proto#L19
        assert isinstance(pos, (Point2, Unit)), "pos is not of type Point2 or Unit"
        pos = pos.position.rounded
        return self.state.visibility[pos] == 2

    def has_creep(self, pos: Union[Point2, Unit]) -> bool:
        """Returns True if there is creep on the grid point.

        :param pos:"""
        assert isinstance(pos, (Point2, Unit)), "pos is not of type Point2 or Unit"
        pos = pos.position.rounded
        return self.state.creep[pos] == 1

    async def on_unit_destroyed(self, unit_tag: int):
        """
        Override this in your bot class.
        Note that this function uses unit tags and not the unit objects
        because the unit does not exist any more.
        This will event will be called when a unit (or structure, friendly or enemy) dies.
        For enemy units, this only works if the enemy unit was in vision on death.

        :param unit_tag:
        """

    async def on_unit_created(self, unit: Unit):
        """Override this in your bot class. This function is called when a unit is created.

        :param unit:"""

    async def on_building_construction_started(self, unit: Unit):
        """
        Override this in your bot class.
        This function is called when a building construction has started.

        :param unit:
        """

    async def on_building_construction_complete(self, unit: Unit):
        """
        Override this in your bot class. This function is called when a building
        construction is completed.

        :param unit:
        """

    async def on_unit_took_damage(self, unit: Unit, amount_damage_taken: float):
        """
        Override this in your bot class. This function is called when your own unit (unit or structure) took damage.
        It will not be called if the unit died this frame.

        This may be called frequently for terran structures that are burning down, or zerg buildings that are off creep,
        or terran bio units that just used stimpack ability.
        TODO: If there is a demand for it, then I can add a similar event for when enemy units took damage

        Examples::

            print(f"My unit took damage: {unit} took {amount_damage_taken} damage")

        :param unit:
        :param amount_damage_taken:
        """

    async def on_enemy_unit_entered_vision(self, unit: Unit):
        """
        Override this in your bot class. This function is called when an enemy unit (unit or structure) entered vision (which was not visible last frame).

        :param unit:
        """

    async def on_enemy_unit_left_vision(self, unit_tag: int):
        """
        Override this in your bot class. This function is called when an enemy unit (unit or structure) left vision (which was visible last frame).
        Same as the self.on_unit_destroyed event, this function is called with the unit's tag because the unit is no longer visible anymore.
        If you want to store a snapshot of the unit, use self._enemy_units_previous_map[unit_tag] for units or self._enemy_structures_previous_map[unit_tag] for structures.

        Examples::

            last_known_unit = self._enemy_units_previous_map.get(unit_tag, None) or self._enemy_structures_previous_map[unit_tag]
            print(f"Enemy unit left vision, last known location: {last_known_unit.position}")

        :param unit_tag:
        """

    async def on_before_start(self):
        """
        Override this in your bot class. This function is called before "on_start"
        and before "prepare_first_step" that calculates expansion locations.
        Not all data is available yet.
        This function is useful in realtime=True mode to split your workers or start producing the first worker.
        """

    async def on_start(self):
        """
        Override this in your bot class.
        At this point, game_data, game_info and the first iteration of game_state (self.state) are available.
        """

    async def on_step(self, iteration: int):
        """
        You need to implement this function!
        Override this in your bot class.
        This function is called on every game step (looped in realtime mode).

        :param iteration:
        """
        raise NotImplementedError

    async def on_end(self, game_result: Result):
        """Override this in your bot class. This function is called at the end of a game.
        Unsure if this function will be called on the laddermanager client as the bot process may forcefully be terminated.

        :param game_result:"""
