# pylint: disable=W0212,R0916,R0904
from __future__ import annotations

import math
import random
import warnings
from collections import Counter
from functools import cached_property
from typing import TYPE_CHECKING, Dict, List, Optional, Set, Tuple, Union

from loguru import logger

from sc2.bot_ai_internal import BotAIInternal
from sc2.cache import property_cache_once_per_frame
from sc2.constants import (
    EQUIVALENTS_FOR_TECH_PROGRESS,
    PROTOSS_TECH_REQUIREMENT,
    TERRAN_STRUCTURES_REQUIRE_SCV,
    TERRAN_TECH_REQUIREMENT,
    ZERG_TECH_REQUIREMENT,
)
from sc2.data import Alert, Race, Result, Target
from sc2.dicts.unit_research_abilities import RESEARCH_INFO
from sc2.dicts.unit_train_build_abilities import TRAIN_INFO
from sc2.dicts.unit_trained_from import UNIT_TRAINED_FROM
from sc2.dicts.upgrade_researched_from import UPGRADE_RESEARCHED_FROM
from sc2.game_data import AbilityData, Cost
from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId
from sc2.position import Point2
from sc2.unit import Unit
from sc2.units import Units

if TYPE_CHECKING:
    from sc2.game_info import Ramp


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

    @property
    def units_created(self) -> Counter[UnitTypeId, int]:
        """Returns a Counter for all your units and buildings you have created so far.

        This may be used for statistics (at the end of the game) or for strategic decision making.

        CAUTION: This does not properly work at the moment for morphing units and structures. Please use the 'on_unit_type_changed' event to add these morphing unit types manually to 'self._units_created'.
        Issues would arrise in e.g. siege tank morphing to sieged tank, and then morphing back (suddenly the counter counts 2 tanks have been created).

        Examples::

            # Give attack command to enemy base every time 10 marines have been trained
            async def on_unit_created(self, unit: Unit):
                if unit.type_id == UnitTypeId.MARINE:
                    if self.units_created[MARINE] % 10 == 0:
                        for marine in self.units(UnitTypeId.MARINE):
                            marine.attack(self.enemy_start_locations[0])
        """
        return self._units_created

    async def get_available_abilities(
        self, units: Union[List[Unit], Units], ignore_resource_requirements: bool = False
    ) -> List[List[AbilityId]]:
        """Returns available abilities of one or more units. Right now only checks cooldown, energy cost, and whether the ability has been researched.

        Examples::

            units_abilities = await self.get_available_abilities(self.units)

        or::

            units_abilities = await self.get_available_abilities([self.units.random])

        :param units:
        :param ignore_resource_requirements:"""
        return await self.client.query_available_abilities(units, ignore_resource_requirements)

    async def expand_now(self, building: UnitTypeId = None, max_distance: int = 10, location: Optional[Point2] = None):
        """Finds the next possible expansion via 'self.get_next_expansion()'. If the target expansion is blocked (e.g. an enemy unit), it will misplace the expansion.

        :param building:
        :param max_distance:
        :param location:"""

        if not building:
            # self.race is never Race.Random
            start_townhall_type = {
                Race.Protoss: UnitTypeId.NEXUS,
                Race.Terran: UnitTypeId.COMMANDCENTER,
                Race.Zerg: UnitTypeId.HATCHERY,
            }
            building = start_townhall_type[self.race]

        assert isinstance(building, UnitTypeId), f"{building} is no UnitTypeId"

        if not location:
            location = await self.get_next_expansion()
        if not location:
            # All expansions are used up or mined out
            logger.warning("Trying to expand_now() but bot is out of locations to expand to")
            return
        await self.build(building, near=location, max_distance=max_distance, random_alternative=False, placement_step=1)

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

    def calculate_supply_cost(self, unit_type: UnitTypeId) -> float:
        """
        This function calculates the required supply to train or morph a unit.
        The total supply of a baneling is 0.5, but a zergling already uses up 0.5 supply, so the morph supply cost is 0.
        The total supply of a ravager is 3, but a roach already uses up 2 supply, so the morph supply cost is 1.
        The required supply to build zerglings is 1 because they pop in pairs, so this function returns 1 because the larva morph command requires 1 free supply.

        Example::

            roach_supply_cost = self.calculate_supply_cost(UnitTypeId.ROACH) # Is 2
            ravager_supply_cost = self.calculate_supply_cost(UnitTypeId.RAVAGER) # Is 1
            baneling_supply_cost = self.calculate_supply_cost(UnitTypeId.BANELING) # Is 0

        :param unit_type:"""
        if unit_type in {UnitTypeId.ZERGLING}:
            return 1
        unit_supply_cost = self.game_data.units[unit_type.value]._proto.food_required
        if unit_supply_cost > 0 and unit_type in UNIT_TRAINED_FROM and len(UNIT_TRAINED_FROM[unit_type]) == 1:
            producer: UnitTypeId
            for producer in UNIT_TRAINED_FROM[unit_type]:
                producer_unit_data = self.game_data.units[producer.value]
                if producer_unit_data._proto.food_required <= unit_supply_cost:
                    producer_supply_cost = producer_unit_data._proto.food_required
                    unit_supply_cost -= producer_supply_cost
        return unit_supply_cost

    def can_feed(self, unit_type: UnitTypeId) -> bool:
        """Checks if you have enough free supply to build the unit

        Example::

            cc = self.townhalls.idle.random_or(None)
            # self.townhalls can be empty or there are no idle townhalls
            if cc and self.can_feed(UnitTypeId.SCV):
                cc.train(UnitTypeId.SCV)

        :param unit_type:"""
        required = self.calculate_supply_cost(unit_type)
        # "required <= 0" in case self.supply_left is negative
        return required <= 0 or self.supply_left >= required

    def calculate_unit_value(self, unit_type: UnitTypeId) -> Cost:
        """
        Unlike the function below, this function returns the value of a unit given by the API (e.g. the resources lost value on kill).

        Examples::

            self.calculate_value(UnitTypeId.ORBITALCOMMAND) == Cost(550, 0)
            self.calculate_value(UnitTypeId.RAVAGER) == Cost(100, 100)
            self.calculate_value(UnitTypeId.ARCHON) == Cost(175, 275)

        :param unit_type:
        """
        unit_data = self.game_data.units[unit_type.value]
        return Cost(unit_data._proto.mineral_cost, unit_data._proto.vespene_cost)

    def calculate_cost(self, item_id: Union[UnitTypeId, UpgradeId, AbilityId]) -> Cost:
        """
        Calculate the required build, train or morph cost of a unit. It is recommended to use the UnitTypeId instead of the ability to create the unit.
        The total cost to create a ravager is 100/100, but the actual morph cost from roach to ravager is only 25/75, so this function returns 25/75.

        It is adviced to use the UnitTypeId instead of the AbilityId. Instead of::

            self.calculate_cost(AbilityId.UPGRADETOORBITAL_ORBITALCOMMAND)

        use::

            self.calculate_cost(UnitTypeId.ORBITALCOMMAND)

        More examples::

            from sc2.game_data import Cost

            self.calculate_cost(UnitTypeId.BROODLORD) == Cost(150, 150)
            self.calculate_cost(UnitTypeId.RAVAGER) == Cost(25, 75)
            self.calculate_cost(UnitTypeId.BANELING) == Cost(25, 25)
            self.calculate_cost(UnitTypeId.ORBITALCOMMAND) == Cost(150, 0)
            self.calculate_cost(UnitTypeId.REACTOR) == Cost(50, 50)
            self.calculate_cost(UnitTypeId.TECHLAB) == Cost(50, 25)
            self.calculate_cost(UnitTypeId.QUEEN) == Cost(150, 0)
            self.calculate_cost(UnitTypeId.HATCHERY) == Cost(300, 0)
            self.calculate_cost(UnitTypeId.LAIR) == Cost(150, 100)
            self.calculate_cost(UnitTypeId.HIVE) == Cost(200, 150)

        :param item_id:
        """
        if isinstance(item_id, UnitTypeId):
            # Fix cost for reactor and techlab where the API returns 0 for both
            if item_id in {UnitTypeId.REACTOR, UnitTypeId.TECHLAB, UnitTypeId.ARCHON}:
                if item_id == UnitTypeId.REACTOR:
                    return Cost(50, 50)
                if item_id == UnitTypeId.TECHLAB:
                    return Cost(50, 25)
                if item_id == UnitTypeId.ARCHON:
                    return self.calculate_unit_value(UnitTypeId.ARCHON)
            unit_data = self.game_data.units[item_id.value]
            # Cost of morphs is automatically correctly calculated by 'calculate_ability_cost'
            return self.game_data.calculate_ability_cost(unit_data.creation_ability.exact_id)

        if isinstance(item_id, UpgradeId):
            cost = self.game_data.upgrades[item_id.value].cost
        else:
            # Is already AbilityId
            cost = self.game_data.calculate_ability_cost(item_id)
        return cost

    def can_afford(self, item_id: Union[UnitTypeId, UpgradeId, AbilityId], check_supply_cost: bool = True) -> bool:
        """Tests if the player has enough resources to build a unit or structure.

        Example::

            cc = self.townhalls.idle.random_or(None)
            # self.townhalls can be empty or there are no idle townhalls
            if cc and self.can_afford(UnitTypeId.SCV):
                cc.train(UnitTypeId.SCV)

        Example::

            # Current state: we have 150 minerals and one command center and a barracks
            can_afford_morph = self.can_afford(UnitTypeId.ORBITALCOMMAND, check_supply_cost=False)
            # Will be 'True' although the API reports that an orbital is worth 550 minerals, but the morph cost is only 150 minerals

        :param item_id:
        :param check_supply_cost:"""
        cost = self.calculate_cost(item_id)
        if cost.minerals > self.minerals or cost.vespene > self.vespene:
            return False
        if check_supply_cost and isinstance(item_id, UnitTypeId):
            supply_cost = self.calculate_supply_cost(item_id)
            if supply_cost and supply_cost > self.supply_left:
                return False
        return True

    async def can_cast(
        self,
        unit: Unit,
        ability_id: AbilityId,
        target: Optional[Union[Unit, Point2]] = None,
        only_check_energy_and_cooldown: bool = False,
        cached_abilities_of_unit: List[AbilityId] = None,
    ) -> bool:
        """Tests if a unit has an ability available and enough energy to cast it.

        Example::

            stalkers = self.units(UnitTypeId.STALKER)
            stalkers_that_can_blink = stalkers.filter(lambda unit: unit.type_id == UnitTypeId.STALKER and (await self.can_cast(unit, AbilityId.EFFECT_BLINK_STALKER, only_check_energy_and_cooldown=True)))

        See data_pb2.py (line 161) for the numbers 1-5 to make sense

        :param unit:
        :param ability_id:
        :param target:
        :param only_check_energy_and_cooldown:
        :param cached_abilities_of_unit:"""
        assert isinstance(unit, Unit), f"{unit} is no Unit object"
        assert isinstance(ability_id, AbilityId), f"{ability_id} is no AbilityId"
        assert isinstance(target, (type(None), Unit, Point2))
        # check if unit has enough energy to cast or if ability is on cooldown
        if cached_abilities_of_unit:
            abilities = cached_abilities_of_unit
        else:
            abilities = (await self.get_available_abilities([unit], ignore_resource_requirements=False))[0]

        if ability_id in abilities:
            if only_check_energy_and_cooldown:
                return True
            cast_range = self.game_data.abilities[ability_id.value]._proto.cast_range
            ability_target: int = self.game_data.abilities[ability_id.value]._proto.target
            # Check if target is in range (or is a self cast like stimpack)
            if (
                ability_target == 1 or ability_target == Target.PointOrNone.value and isinstance(target, Point2)
                and unit.distance_to(target) <= unit.radius + target.radius + cast_range
            ):  # cant replace 1 with "Target.None.value" because ".None" doesnt seem to be a valid enum name
                return True
            # Check if able to use ability on a unit
            if (
                ability_target in {Target.Unit.value, Target.PointOrUnit.value} and isinstance(target, Unit)
                and unit.distance_to(target) <= unit.radius + target.radius + cast_range
            ):
                return True
            # Check if able to use ability on a position
            if (
                ability_target in {Target.Point.value, Target.PointOrUnit.value} and isinstance(target, Point2)
                and unit.distance_to(target) <= unit.radius + cast_range
            ):
                return True
        return False

    def select_build_worker(self, pos: Union[Unit, Point2], force: bool = False) -> Optional[Unit]:
        """Select a worker to build a building with.

        Example::

            barracks_placement_position = self.main_base_ramp.barracks_correct_placement
            worker = self.select_build_worker(barracks_placement_position)
            # Can return None
            if worker:
                worker.build(UnitTypeId.BARRACKS, barracks_placement_position)

        :param pos:
        :param force:"""
        workers = (
            self.workers.filter(lambda w: (w.is_gathering or w.is_idle) and w.distance_to(pos) < 20) or self.workers
        )
        if workers:
            for worker in workers.sorted_by_distance_to(pos).prefer_idle:
                if (
                    worker not in self.unit_tags_received_action and not worker.orders or len(worker.orders) == 1
                    and worker.orders[0].ability.id in {AbilityId.MOVE, AbilityId.HARVEST_GATHER}
                ):
                    return worker

            return workers.random if force else None
        return None

    async def can_place_single(self, building: Union[AbilityId, UnitTypeId], position: Point2) -> bool:
        """ Checks the placement for only one position. """
        if isinstance(building, UnitTypeId):
            creation_ability = self.game_data.units[building.value].creation_ability.id
            return (await self.client._query_building_placement_fast(creation_ability, [position]))[0]
        return (await self.client._query_building_placement_fast(building, [position]))[0]

    async def can_place(self, building: Union[AbilityData, AbilityId, UnitTypeId],
                        positions: List[Point2]) -> List[bool]:
        """Tests if a building can be placed in the given locations.

        Example::

            barracks_placement_position = self.main_base_ramp.barracks_correct_placement
            worker = self.select_build_worker(barracks_placement_position)
            # Can return None
            if worker and (await self.can_place(UnitTypeId.BARRACKS, [barracks_placement_position])[0]:
                worker.build(UnitTypeId.BARRACKS, barracks_placement_position)

        :param building:
        :param position:"""
        building_type = type(building)
        assert type(building) in {AbilityData, AbilityId, UnitTypeId}, f"{building}, {building_type}"
        if building_type == UnitTypeId:
            building = self.game_data.units[building.value].creation_ability.id
        elif building_type == AbilityData:
            warnings.warn(
                "Using AbilityData is deprecated and may be removed soon. Please use AbilityId or UnitTypeId instead.",
                DeprecationWarning,
                stacklevel=2,
            )
            building = building_type.id

        if isinstance(positions, (Point2, tuple)):
            warnings.warn(
                "The support for querying single entries will be removed soon. Please use either 'await self.can_place_single(building, position)' or 'await (self.can_place(building, [position]))[0]",
                DeprecationWarning,
                stacklevel=2,
            )
            return await self.can_place_single(building, positions)
        assert isinstance(positions, list), f"Expected an iterable (list, tuple), but was: {positions}"
        assert isinstance(
            positions[0], Point2
        ), f"List is expected to have Point2, but instead had: {positions[0]} {type(positions[0])}"
        return await self.client._query_building_placement_fast(building, positions)

    async def find_placement(
        self,
        building: Union[UnitTypeId, AbilityId],
        near: Point2,
        max_distance: int = 20,
        random_alternative: bool = True,
        placement_step: int = 2,
        addon_place: bool = False,
    ) -> Optional[Point2]:
        """Finds a placement location for building.

        Example::

            if self.townhalls:
                cc = self.townhalls[0]
                depot_position = await self.find_placement(UnitTypeId.SUPPLYDEPOT, near=cc)

        :param building:
        :param near:
        :param max_distance:
        :param random_alternative:
        :param placement_step:
        :param addon_place:"""

        assert isinstance(building, (AbilityId, UnitTypeId))
        assert isinstance(near, Point2), f"{near} is no Point2 object"

        if isinstance(building, UnitTypeId):
            building = self.game_data.units[building.value].creation_ability.id

        if await self.can_place_single(
            building, near
        ) and (not addon_place or await self.can_place_single(UnitTypeId.SUPPLYDEPOT, near.offset((2.5, -0.5)))):
            return near

        if max_distance == 0:
            return None

        for distance in range(placement_step, max_distance, placement_step):
            possible_positions = [
                Point2(p).offset(near).to2 for p in (
                    [(dx, -distance) for dx in range(-distance, distance + 1, placement_step)] +
                    [(dx, distance) for dx in range(-distance, distance + 1, placement_step)] +
                    [(-distance, dy) for dy in range(-distance, distance + 1, placement_step)] +
                    [(distance, dy) for dy in range(-distance, distance + 1, placement_step)]
                )
            ]
            res = await self.client._query_building_placement_fast(building, possible_positions)
            # Filter all positions if building can be placed
            possible = [p for r, p in zip(res, possible_positions) if r]

            if addon_place:
                # Filter remaining positions if addon can be placed
                res = await self.client._query_building_placement_fast(
                    AbilityId.TERRANBUILDDROP_SUPPLYDEPOTDROP,
                    [p.offset((2.5, -0.5)) for p in possible],
                )
                possible = [p for r, p in zip(res, possible) if r]

            if not possible:
                continue

            if random_alternative:
                return random.choice(possible)
            return min(possible, key=lambda p: p.distance_to_point2(near))
        return None

    # TODO: improve using cache per frame
    def already_pending_upgrade(self, upgrade_type: UpgradeId) -> float:
        """Check if an upgrade is being researched

        Returns values are::

            0 # not started
            0 < x < 1 # researching
            1 # completed

        Example::

            stim_completion_percentage = self.already_pending_upgrade(UpgradeId.STIMPACK)

        :param upgrade_type:
        """
        assert isinstance(upgrade_type, UpgradeId), f"{upgrade_type} is no UpgradeId"
        if upgrade_type in self.state.upgrades:
            return 1
        creationAbilityID = self.game_data.upgrades[upgrade_type.value].research_ability.exact_id
        for structure in self.structures.filter(lambda unit: unit.is_ready):
            for order in structure.orders:
                if order.ability.exact_id == creationAbilityID:
                    return order.progress
        return 0

    def structure_type_build_progress(self, structure_type: Union[UnitTypeId, int]) -> float:
        """
        Returns the build progress of a structure type.

        Return range: 0 <= x <= 1 where
            0: no such structure exists
            0 < x < 1: at least one structure is under construction, returns the progress of the one with the highest progress
            1: we have at least one such structure complete

        Example::

            # Assuming you have one barracks building at 0.5 build progress:
            progress = self.structure_type_build_progress(UnitTypeId.BARRACKS)
            print(progress)
            # This prints out 0.5

            # If you want to save up money for mutalisks, you can now save up once the spire is nearly completed:
            spire_almost_completed: bool = self.structure_type_build_progress(UnitTypeId.SPIRE) > 0.75

            # If you have a Hive completed but no lair, this function returns 1.0 for the following:
            self.structure_type_build_progress(UnitTypeId.LAIR)

            # Assume you have 2 command centers in production, one has 0.5 build_progress and the other 0.2, the following returns 0.5
            highest_progress_of_command_center: float = self.structure_type_build_progress(UnitTypeId.COMMANDCENTER)

        :param structure_type:
        """
        assert isinstance(
            structure_type, (int, UnitTypeId)
        ), f"Needs to be int or UnitTypeId, but was: {type(structure_type)}"
        if isinstance(structure_type, int):
            structure_type_value: int = structure_type
            structure_type = UnitTypeId(structure_type_value)
        else:
            structure_type_value = structure_type.value
        assert structure_type_value, f"structure_type can not be 0 or NOTAUNIT, but was: {structure_type_value}"
        equiv_values: Set[int] = {structure_type_value} | {
            s_type.value
            for s_type in EQUIVALENTS_FOR_TECH_PROGRESS.get(structure_type, set())
        }
        # SUPPLYDEPOTDROP is not in self.game_data.units, so bot_ai should not check the build progress via creation ability (worker abilities)
        if structure_type_value not in self.game_data.units:
            return max((s.build_progress for s in self.structures if s._proto.unit_type in equiv_values), default=0)
        creation_ability_data: AbilityData = self.game_data.units[structure_type_value].creation_ability
        if creation_ability_data is None:
            return 0
        creation_ability: AbilityId = creation_ability_data.exact_id
        max_value = max(
            [s.build_progress for s in self.structures if s._proto.unit_type in equiv_values] +
            [self._abilities_all_units[1].get(creation_ability, 0)],
            default=0,
        )
        return max_value

    def tech_requirement_progress(self, structure_type: UnitTypeId) -> float:
        """Returns the tech requirement progress for a specific building

        Example::

            # Current state: supply depot is at 50% completion
            tech_requirement = self.tech_requirement_progress(UnitTypeId.BARRACKS)
            print(tech_requirement) # Prints 0.5 because supply depot is half way done

        Example::

            # Current state: your bot has one hive, no lair
            tech_requirement = self.tech_requirement_progress(UnitTypeId.HYDRALISKDEN)
            print(tech_requirement) # Prints 1 because a hive exists even though only a lair is required

        Example::

            # Current state: One factory is flying and one is half way done
            tech_requirement = self.tech_requirement_progress(UnitTypeId.STARPORT)
            print(tech_requirement) # Prints 1 because even though the type id of the flying factory is different, it still has build progress of 1 and thus tech requirement is completed

        :param structure_type:"""
        race_dict = {
            Race.Protoss: PROTOSS_TECH_REQUIREMENT,
            Race.Terran: TERRAN_TECH_REQUIREMENT,
            Race.Zerg: ZERG_TECH_REQUIREMENT,
        }
        unit_info_id = race_dict[self.race][structure_type]
        unit_info_id_value = unit_info_id.value
        # The following commented out line is unreliable for ghost / thor as they return 0 which is incorrect
        # unit_info_id_value = self.game_data.units[structure_type.value]._proto.tech_requirement
        if not unit_info_id_value:  # Equivalent to "if unit_info_id_value == 0:"
            return 1
        progresses: List[float] = [self.structure_type_build_progress(unit_info_id_value)]
        for equiv_structure in EQUIVALENTS_FOR_TECH_PROGRESS.get(unit_info_id, []):
            progresses.append(self.structure_type_build_progress(equiv_structure.value))
        return max(progresses)

    def already_pending(self, unit_type: Union[UpgradeId, UnitTypeId]) -> float:
        """
        Returns a number of buildings or units already in progress, or if a
        worker is en route to build it. This also includes queued orders for
        workers and build queues of buildings.

        Example::

            amount_of_scv_in_production: int = self.already_pending(UnitTypeId.SCV)
            amount_of_CCs_in_queue_and_production: int = self.already_pending(UnitTypeId.COMMANDCENTER)
            amount_of_lairs_morphing: int = self.already_pending(UnitTypeId.LAIR)

        :param unit_type:
        """
        if isinstance(unit_type, UpgradeId):
            return self.already_pending_upgrade(unit_type)
        try:
            ability = self.game_data.units[unit_type.value].creation_ability.exact_id
        except AttributeError:
            # Hotfix for checking pending archons
            if unit_type == UnitTypeId.ARCHON:
                return self._abilities_all_units[0][AbilityId.ARCHON_WARP_TARGET] / 2
            logger.error(f"Uncaught UnitTypeId: {unit_type}")
            return 0
        return self._abilities_all_units[0][ability]

    def worker_en_route_to_build(self, unit_type: UnitTypeId) -> float:
        """This function counts how many workers are on the way to start the construction a building.

        :param unit_type:"""
        ability = self.game_data.units[unit_type.value].creation_ability.exact_id
        return self._worker_orders[ability]

    @property_cache_once_per_frame
    def structures_without_construction_SCVs(self) -> Units:
        """Returns all structures that do not have an SCV constructing it.
        Warning: this function may move to become a Units filter."""
        worker_targets: Set[Union[int, Point2]] = set()
        for worker in self.workers:
            # Ignore repairing workers
            if not worker.is_constructing_scv:
                continue
            for order in worker.orders:
                # When a construction is resumed, the worker.orders[0].target is the tag of the structure, else it is a Point2
                worker_targets.add(order.target)
        return self.structures.filter(
            lambda structure: structure.build_progress < 1
            # Redundant check?
            and structure.type_id in TERRAN_STRUCTURES_REQUIRE_SCV and structure.position not in worker_targets and
            structure.tag not in worker_targets and structure.tag in self._structures_previous_map and self.
            _structures_previous_map[structure.tag].build_progress == structure.build_progress
        )

    async def build(
        self,
        building: UnitTypeId,
        near: Union[Unit, Point2],
        max_distance: int = 20,
        build_worker: Optional[Unit] = None,
        random_alternative: bool = True,
        placement_step: int = 2,
    ) -> bool:
        """Not recommended as this function checks many positions if it "can place" on them until it found a valid
        position. Also if the given position is not placeable, this function tries to find a nearby position to place
        the structure. Then orders the worker to start the construction.

        :param building:
        :param near:
        :param max_distance:
        :param build_worker:
        :param random_alternative:
        :param placement_step:"""

        assert isinstance(near, (Unit, Point2))
        if not self.can_afford(building):
            return False
        p = None
        gas_buildings = {UnitTypeId.EXTRACTOR, UnitTypeId.ASSIMILATOR, UnitTypeId.REFINERY}
        if isinstance(near, Unit) and building not in gas_buildings:
            near = near.position
        if isinstance(near, Point2):
            near = near.to2
        if isinstance(near, Point2):
            p = await self.find_placement(building, near, max_distance, random_alternative, placement_step)
            if p is None:
                return False
        builder = build_worker or self.select_build_worker(near)
        if builder is None:
            return False
        if building in gas_buildings:
            assert isinstance(near, Unit)
            builder.build_gas(near)
            return True
        self.do(builder.build(building, p), subtract_cost=True, ignore_warning=True)
        return True

    def train(
        self,
        unit_type: UnitTypeId,
        amount: int = 1,
        closest_to: Point2 = None,
        train_only_idle_buildings: bool = True
    ) -> int:
        """Trains a specified number of units. Trains only one if amount is not specified.
        Warning: currently has issues with warp gate warp ins

        Very generic function. Please use with caution and report any bugs!

        Example Zerg::

            self.train(UnitTypeId.QUEEN, 5)
            # This should queue 5 queens in 5 different townhalls if you have enough townhalls, enough minerals and enough free supply left

        Example Terran::

            # Assuming you have 2 idle barracks with reactors, one barracks without addon and one with techlab
            # It should only queue 4 marines in the 2 idle barracks with reactors
            self.train(UnitTypeId.MARINE, 4)

        Example distance to::

            # If you want to train based on distance to a certain point, you can use "closest_to"
            self.train(UnitTypeId.MARINE, 4, closest_to = self.game_info.map_center)


        :param unit_type:
        :param amount:
        :param closest_to:
        :param train_only_idle_buildings:"""
        # Tech requirement not met
        if self.tech_requirement_progress(unit_type) < 1:
            race_dict = {
                Race.Protoss: PROTOSS_TECH_REQUIREMENT,
                Race.Terran: TERRAN_TECH_REQUIREMENT,
                Race.Zerg: ZERG_TECH_REQUIREMENT,
            }
            unit_info_id = race_dict[self.race][unit_type]
            logger.warning(
                f"{self.time_formatted} Trying to produce unit {unit_type} in self.train() but tech requirement is not met: {unit_info_id}"
            )
            return 0

        # Not affordable
        if not self.can_afford(unit_type):
            return 0

        trained_amount = 0
        # All train structure types: queen can made from hatchery, lair, hive
        train_structure_type: Set[UnitTypeId] = UNIT_TRAINED_FROM[unit_type]
        train_structures = self.structures if self.race != Race.Zerg else self.structures | self.larva
        requires_techlab = any(
            TRAIN_INFO[structure_type][unit_type].get("requires_techlab", False)
            for structure_type in train_structure_type
        )
        is_protoss = self.race == Race.Protoss
        is_terran = self.race == Race.Terran
        can_have_addons = any(
            # pylint: disable=C0208
            u in train_structure_type for u in {UnitTypeId.BARRACKS, UnitTypeId.FACTORY, UnitTypeId.STARPORT}
        )
        # Sort structures closest to a point
        if closest_to is not None:
            train_structures = train_structures.sorted_by_distance_to(closest_to)
        elif can_have_addons:
            # This should sort the structures in ascending order: first structures with reactor, then naked, then with techlab
            train_structures = train_structures.sorted(
                key=lambda structure: -1 * (structure.add_on_tag in self.reactor_tags) + 1 *
                (structure.add_on_tag in self.techlab_tags)
            )

        structure: Unit
        for structure in train_structures:
            # Exit early if we can't afford
            if not self.can_afford(unit_type):
                return trained_amount
            if (
                # If structure hasn't received an action/order this frame
                structure.tag not in self.unit_tags_received_action
                # If structure can train this unit at all
                and structure.type_id in train_structure_type
                # Structure has to be completed to be able to train
                and structure.build_progress == 1
                # If structure is protoss, it needs to be powered to train
                and (not is_protoss or structure.is_powered or structure.type_id == UnitTypeId.NEXUS)
                # Either parameter "train_only_idle_buildings" is False or structure is idle or structure has less than 2 orders and has reactor
                and (
                    not train_only_idle_buildings
                    or len(structure.orders) < 1 + int(structure.add_on_tag in self.reactor_tags)
                )
                # If structure type_id does not accept addons, it cant require a techlab
                # Else we have to check if building has techlab as addon
                and (not requires_techlab or structure.add_on_tag in self.techlab_tags)
            ):
                # Warp in at location
                # TODO: find fast warp in locations either random location or closest to the given parameter "closest_to"
                # TODO: find out which pylons have fast warp in by checking distance to nexus and warpgates.ready
                if structure.type_id == UnitTypeId.WARPGATE:
                    pylons = self.structures(UnitTypeId.PYLON)
                    location = pylons.random.position.random_on_distance(4)
                    successfully_trained = structure.warp_in(unit_type, location)
                else:
                    # Normal train a unit from larva or inside a structure
                    successfully_trained = self.do(
                        structure.train(unit_type), subtract_cost=True, subtract_supply=True, ignore_warning=True
                    )
                    # Check if structure has reactor: queue same unit again
                    if (
                        # Only terran can have reactors
                        is_terran
                        # Check if we have enough cost or supply for this unit type
                        and self.can_afford(unit_type)
                        # Structure needs to be idle in the current frame
                        and not structure.orders
                        # We are at least 2 away from goal
                        and trained_amount + 1 < amount
                        # Unit type does not require techlab
                        and not requires_techlab
                        # Train structure has reactor
                        and structure.add_on_tag in self.reactor_tags
                    ):
                        trained_amount += 1
                        # With one command queue=False and one queue=True, you can queue 2 marines in a reactored barracks in one frame
                        successfully_trained = self.do(
                            structure.train(unit_type, queue=True),
                            subtract_cost=True,
                            subtract_supply=True,
                            ignore_warning=True,
                        )

                if successfully_trained:
                    trained_amount += 1
                    if trained_amount == amount:
                        # Target unit train amount reached
                        return trained_amount
                else:
                    # Some error occured and we couldn't train the unit
                    return trained_amount
        return trained_amount

    def research(self, upgrade_type: UpgradeId) -> bool:
        """
        Researches an upgrade from a structure that can research it, if it is idle and powered (protoss).
        Returns True if the research was started.
        Return False if the requirement was not met, or the bot did not have enough resources to start the upgrade,
        or the building to research the upgrade was missing or not idle.

        New function. Please report any bugs!

        Example::

            # Try to research zergling movement speed if we can afford it
            # and if at least one pool is at build_progress == 1
            # and we are not researching it yet
            if self.already_pending_upgrade(UpgradeId.ZERGLINGMOVEMENTSPEED) == 0 and self.can_afford(UpgradeId.ZERGLINGMOVEMENTSPEED):
                spawning_pools_ready = self.structures(UnitTypeId.SPAWNINGPOOL).ready
                if spawning_pools_ready:
                    self.research(UpgradeId.ZERGLINGMOVEMENTSPEED)

        :param upgrade_type:
        """
        assert (
            upgrade_type in UPGRADE_RESEARCHED_FROM
        ), f"Could not find upgrade {upgrade_type} in 'research from'-dictionary"

        # Not affordable
        if not self.can_afford(upgrade_type):
            return False

        research_structure_types: UnitTypeId = UPGRADE_RESEARCHED_FROM[upgrade_type]
        required_tech_building: Optional[UnitTypeId] = RESEARCH_INFO[research_structure_types][upgrade_type].get(
            "required_building", None
        )

        requirement_met = (
            required_tech_building is None or self.structure_type_build_progress(required_tech_building) == 1
        )
        if not requirement_met:
            return False

        is_protoss = self.race == Race.Protoss

        # All upgrades right now that can be researched in spire and hatch can also be researched in their morphs
        equiv_structures = {
            UnitTypeId.SPIRE: {UnitTypeId.SPIRE, UnitTypeId.GREATERSPIRE},
            UnitTypeId.GREATERSPIRE: {UnitTypeId.SPIRE, UnitTypeId.GREATERSPIRE},
            UnitTypeId.HATCHERY: {UnitTypeId.HATCHERY, UnitTypeId.LAIR, UnitTypeId.HIVE},
            UnitTypeId.LAIR: {UnitTypeId.HATCHERY, UnitTypeId.LAIR, UnitTypeId.HIVE},
            UnitTypeId.HIVE: {UnitTypeId.HATCHERY, UnitTypeId.LAIR, UnitTypeId.HIVE},
        }
        # Convert to a set, or equivalent structures are chosen
        # Overlord speed upgrade can be researched from hatchery, lair or hive
        research_structure_types: Set[UnitTypeId] = equiv_structures.get(
            research_structure_types, {research_structure_types}
        )

        structure: Unit
        for structure in self.structures:
            if (
                # Structure can research this upgrade
                structure.type_id in research_structure_types
                # If structure hasn't received an action/order this frame
                and structure.tag not in self.unit_tags_received_action
                # Structure is idle
                and structure.is_idle
                # Structure belongs to protoss and is powered (near pylon)
                and (not is_protoss or structure.is_powered)
            ):
                # Can_afford check was already done earlier in this function
                successful_action: bool = self.do(
                    structure.research(upgrade_type), subtract_cost=True, ignore_warning=True
                )
                return successful_action
        return False

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

    async def on_unit_type_changed(self, unit: Unit, previous_type: UnitTypeId):
        """Override this in your bot class. This function is called when a unit type has changed. To get the current UnitTypeId of the unit, use 'unit.type_id'

        This may happen when a larva morphed to an egg, siege tank sieged, a zerg unit burrowed, a hatchery morphed to lair,
        a corruptor morphed to broodlordcocoon, etc..

        Examples::

            print(f"My unit changed type: {unit} from {previous_type} to {unit.type_id}")

        :param unit:
        :param previous_type:
        """

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

    async def on_upgrade_complete(self, upgrade: UpgradeId):
        """
        Override this in your bot class. This function is called with the upgrade id of an upgrade that was not finished last step and is now.

        :param upgrade:
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
