# pylint: disable=W0212
from __future__ import annotations

import random
from itertools import chain
from typing import TYPE_CHECKING, Any, Callable, Generator, Iterable, List, Optional, Set, Tuple, Union

from .position import Point2
from .unit import Unit

if TYPE_CHECKING:
    from .bot_ai import BotAI


# pylint: disable=R0904
class Units(list):
    """A collection of Unit objects. Makes it easy to select units by selectors."""

    @classmethod
    def from_proto(cls, units, bot_object: BotAI):
        # pylint: disable=E1120
        return cls((Unit(raw_unit, bot_object=bot_object) for raw_unit in units))

    def __init__(self, units: Iterable[Unit], bot_object: BotAI):
        """
        :param units:
        :param bot_object:
        """
        super().__init__(units)
        self._bot_object = bot_object

    def __call__(self) -> Units:
        """Creates a new mutable Units object from Units or list object.

        :param unit_types:
        """
        return self

    def __iter__(self) -> Generator[Unit, None, None]:
        return (item for item in super().__iter__())

    def copy(self) -> Units:
        """Creates a new mutable Units object from Units or list object.

        :param units:
        """
        return Units(self, self._bot_object)

    def __or__(self, other: Units) -> Units:
        """
        :param other:
        """
        return Units(
            chain(
                iter(self),
                (other_unit for other_unit in other if other_unit.tag not in (self_unit.tag for self_unit in self)),
            ),
            self._bot_object,
        )

    def __add__(self, other: Units) -> Units:
        """
        :param other:
        """
        return Units(
            chain(
                iter(self),
                (other_unit for other_unit in other if other_unit.tag not in (self_unit.tag for self_unit in self)),
            ),
            self._bot_object,
        )

    def __and__(self, other: Units) -> Units:
        """
        :param other:
        """
        return Units(
            (other_unit for other_unit in other if other_unit.tag in (self_unit.tag for self_unit in self)),
            self._bot_object,
        )

    def __sub__(self, other: Units) -> Units:
        """
        :param other:
        """
        return Units(
            (self_unit for self_unit in self if self_unit.tag not in (other_unit.tag for other_unit in other)),
            self._bot_object,
        )

    def __hash__(self) -> int:
        return hash(unit.tag for unit in self)

    @property
    def amount(self) -> int:
        return len(self)

    @property
    def empty(self) -> bool:
        return not bool(self)

    @property
    def exists(self) -> bool:
        return bool(self)

    def find_by_tag(self, tag: int) -> Optional[Unit]:
        """
        :param tag:
        """
        for unit in self:
            if unit.tag == tag:
                return unit
        return None

    def by_tag(self, tag: int) -> Unit:
        """
        :param tag:
        """
        unit = self.find_by_tag(tag)
        if unit is None:
            raise KeyError("Unit not found")
        return unit

    @property
    def first(self) -> Unit:
        assert self, "Units object is empty"
        return self[0]

    def take(self, n: int) -> Units:
        """
        :param n:
        """
        if n >= self.amount:
            return self
        return self.subgroup(self[:n])

    @property
    def random(self) -> Unit:
        assert self, "Units object is empty"
        return random.choice(self)

    def random_or(self, other: any) -> Unit:
        return random.choice(self) if self else other

    def random_group_of(self, n: int) -> Units:
        """ Returns self if n >= self.amount. """
        if n < 1:
            return Units([], self._bot_object)
        if n >= self.amount:
            return self
        return self.subgroup(random.sample(self, n))

    def in_attack_range_of(self, unit: Unit, bonus_distance: float = 0) -> Units:
        """Filters units that are in attack range of the given unit.
        This uses the unit and target unit.radius when calculating the distance, so it should be accurate.
        Caution: This may not work well for static structures (bunker, sieged tank, planetary fortress, photon cannon, spine and spore crawler) because it seems attack ranges differ for static / immovable units.

        Example::

            enemy_zerglings = self.enemy_units(UnitTypeId.ZERGLING)
            my_marine = next((unit for unit in self.units if unit.type_id == UnitTypeId.MARINE), None)
            if my_marine:
                all_zerglings_my_marine_can_attack = enemy_zerglings.in_attack_range_of(my_marine)

        Example::

            enemy_mutalisks = self.enemy_units(UnitTypeId.MUTALISK)
            my_marauder = next((unit for unit in self.units if unit.type_id == UnitTypeId.MARAUDER), None)
            if my_marauder:
                all_mutalisks_my_marauder_can_attack = enemy_mutaliskss.in_attack_range_of(my_marauder)
                # Is empty because mutalisk are flying and marauder cannot attack air

        :param unit:
        :param bonus_distance:
        """
        return self.filter(lambda x: unit.target_in_range(x, bonus_distance=bonus_distance))

    def closest_distance_to(self, position: Union[Unit, Point2]) -> float:
        """Returns the distance between the closest unit from this group to the target unit.

        Example::

            enemy_zerglings = self.enemy_units(UnitTypeId.ZERGLING)
            my_marine = next((unit for unit in self.units if unit.type_id == UnitTypeId.MARINE), None)
            if my_marine:
                closest_zergling_distance = enemy_zerglings.closest_distance_to(my_marine)
            # Contains the distance between the marine and the closest zergling

        :param position:
        """
        assert self, "Units object is empty"
        if isinstance(position, Unit):
            return min(self._bot_object._distance_squared_unit_to_unit(unit, position) for unit in self)**0.5
        return min(self._bot_object._distance_units_to_pos(self, position))

    def furthest_distance_to(self, position: Union[Unit, Point2]) -> float:
        """Returns the distance between the furthest unit from this group to the target unit


        Example::

            enemy_zerglings = self.enemy_units(UnitTypeId.ZERGLING)
            my_marine = next((unit for unit in self.units if unit.type_id == UnitTypeId.MARINE), None)
            if my_marine:
                furthest_zergling_distance = enemy_zerglings.furthest_distance_to(my_marine)
                # Contains the distance between the marine and the furthest away zergling

        :param position:
        """
        assert self, "Units object is empty"
        if isinstance(position, Unit):
            return max(self._bot_object._distance_squared_unit_to_unit(unit, position) for unit in self)**0.5
        return max(self._bot_object._distance_units_to_pos(self, position))

    def closest_to(self, position: Union[Unit, Point2]) -> Unit:
        """Returns the closest unit (from this Units object) to the target unit or position.

        Example::

            enemy_zerglings = self.enemy_units(UnitTypeId.ZERGLING)
            my_marine = next((unit for unit in self.units if unit.type_id == UnitTypeId.MARINE), None)
            if my_marine:
                closest_zergling = enemy_zerglings.closest_to(my_marine)
                # Contains the zergling that is closest to the target marine

        :param position:
        """
        assert self, "Units object is empty"
        if isinstance(position, Unit):
            return min(
                (unit1 for unit1 in self),
                key=lambda unit2: self._bot_object._distance_squared_unit_to_unit(unit2, position),
            )

        distances = self._bot_object._distance_units_to_pos(self, position)
        return min(((unit, dist) for unit, dist in zip(self, distances)), key=lambda my_tuple: my_tuple[1])[0]

    def furthest_to(self, position: Union[Unit, Point2]) -> Unit:
        """Returns the furhest unit (from this Units object) to the target unit or position.

        Example::

            enemy_zerglings = self.enemy_units(UnitTypeId.ZERGLING)
            my_marine = next((unit for unit in self.units if unit.type_id == UnitTypeId.MARINE), None)
            if my_marine:
                furthest_zergling = enemy_zerglings.furthest_to(my_marine)
                # Contains the zergling that is furthest away to the target marine

        :param position:
        """
        assert self, "Units object is empty"
        if isinstance(position, Unit):
            return max(
                (unit1 for unit1 in self),
                key=lambda unit2: self._bot_object._distance_squared_unit_to_unit(unit2, position),
            )
        distances = self._bot_object._distance_units_to_pos(self, position)
        return max(((unit, dist) for unit, dist in zip(self, distances)), key=lambda my_tuple: my_tuple[1])[0]

    def closer_than(self, distance: float, position: Union[Unit, Point2]) -> Units:
        """Returns all units (from this Units object) that are closer than 'distance' away from target unit or position.

        Example::

            enemy_zerglings = self.enemy_units(UnitTypeId.ZERGLING)
            my_marine = next((unit for unit in self.units if unit.type_id == UnitTypeId.MARINE), None)
            if my_marine:
                close_zerglings = enemy_zerglings.closer_than(3, my_marine)
                # Contains all zerglings that are distance 3 or less away from the marine (does not include unit radius in calculation)

        :param distance:
        :param position:
        """
        if not self:
            return self
        if isinstance(position, Unit):
            distance_squared = distance**2
            return self.subgroup(
                unit for unit in self
                if self._bot_object._distance_squared_unit_to_unit(unit, position) < distance_squared
            )
        distances = self._bot_object._distance_units_to_pos(self, position)
        return self.subgroup(unit for unit, dist in zip(self, distances) if dist < distance)

    def further_than(self, distance: float, position: Union[Unit, Point2]) -> Units:
        """Returns all units (from this Units object) that are further than 'distance' away from target unit or position.

        Example::

            enemy_zerglings = self.enemy_units(UnitTypeId.ZERGLING)
            my_marine = next((unit for unit in self.units if unit.type_id == UnitTypeId.MARINE), None)
            if my_marine:
                far_zerglings = enemy_zerglings.further_than(3, my_marine)
                # Contains all zerglings that are distance 3 or more away from the marine (does not include unit radius in calculation)

        :param distance:
        :param position:
        """
        if not self:
            return self
        if isinstance(position, Unit):
            distance_squared = distance**2
            return self.subgroup(
                unit for unit in self
                if distance_squared < self._bot_object._distance_squared_unit_to_unit(unit, position)
            )
        distances = self._bot_object._distance_units_to_pos(self, position)
        return self.subgroup(unit for unit, dist in zip(self, distances) if distance < dist)

    def in_distance_between(
        self, position: Union[Unit, Point2, Tuple[float, float]], distance1: float, distance2: float
    ) -> Units:
        """Returns units that are further than distance1 and closer than distance2 to unit or position.

        Example::

            enemy_zerglings = self.enemy_units(UnitTypeId.ZERGLING)
            my_marine = next((unit for unit in self.units if unit.type_id == UnitTypeId.MARINE), None)
            if my_marine:
                zerglings_filtered = enemy_zerglings.in_distance_between(my_marine, 3, 5)
                # Contains all zerglings that are between distance 3 and 5 away from the marine (does not include unit radius in calculation)

        :param position:
        :param distance1:
        :param distance2:
        """
        if not self:
            return self
        if isinstance(position, Unit):
            distance1_squared = distance1**2
            distance2_squared = distance2**2
            return self.subgroup(
                unit for unit in self if
                distance1_squared < self._bot_object._distance_squared_unit_to_unit(unit, position) < distance2_squared
            )
        distances = self._bot_object._distance_units_to_pos(self, position)
        return self.subgroup(unit for unit, dist in zip(self, distances) if distance1 < dist < distance2)

    def closest_n_units(self, position: Union[Unit, Point2], n: int) -> Units:
        """Returns the n closest units in distance to position.

        Example::

            enemy_zerglings = self.enemy_units(UnitTypeId.ZERGLING)
            my_marine = next((unit for unit in self.units if unit.type_id == UnitTypeId.MARINE), None)
            if my_marine:
                zerglings_filtered = enemy_zerglings.closest_n_units(my_marine, 5)
                # Contains 5 zerglings that are the closest to the marine

        :param position:
        :param n:
        """
        if not self:
            return self
        return self.subgroup(self._list_sorted_by_distance_to(position)[:n])

    def furthest_n_units(self, position: Union[Unit, Point2], n: int) -> Units:
        """Returns the n furhest units in distance to position.

        Example::

            enemy_zerglings = self.enemy_units(UnitTypeId.ZERGLING)
            my_marine = next((unit for unit in self.units if unit.type_id == UnitTypeId.MARINE), None)
            if my_marine:
                zerglings_filtered = enemy_zerglings.furthest_n_units(my_marine, 5)
                # Contains 5 zerglings that are the furthest to the marine

        :param position:
        :param n:
        """
        if not self:
            return self
        return self.subgroup(self._list_sorted_by_distance_to(position)[-n:])

    def in_distance_of_group(self, other_units: Units, distance: float) -> Units:
        """Returns units that are closer than distance from any unit in the other units object.

        :param other_units:
        :param distance:
        """
        assert other_units, "Other units object is empty"
        # Return self because there are no enemies
        if not self:
            return self
        distance_squared = distance**2
        if len(self) == 1:
            if any(
                self._bot_object._distance_squared_unit_to_unit(self[0], target) < distance_squared
                for target in other_units
            ):
                return self
            return self.subgroup([])

        return self.subgroup(
            self_unit for self_unit in self if any(
                self._bot_object._distance_squared_unit_to_unit(self_unit, other_unit) < distance_squared
                for other_unit in other_units
            )
        )

    def in_closest_distance_to_group(self, other_units: Units) -> Unit:
        """Returns unit in shortest distance from any unit in self to any unit in group.

        Loops over all units in self, then loops over all units in other_units and calculates the shortest distance. Returns the units that is closest to any unit of 'other_units'.

        :param other_units:
        """
        assert self, "Units object is empty"
        assert other_units, "Given units object is empty"
        return min(
            self,
            key=lambda self_unit:
            min(self._bot_object._distance_squared_unit_to_unit(self_unit, other_unit) for other_unit in other_units),
        )

    def _list_sorted_closest_to_distance(self, position: Union[Unit, Point2], distance: float) -> List[Unit]:
        """This function should be a bit faster than using units.sorted(key=lambda u: u.distance_to(position))

        :param position:
        :param distance:
        """
        if isinstance(position, Unit):
            return sorted(
                self,
                key=lambda unit: abs(self._bot_object._distance_squared_unit_to_unit(unit, position) - distance),
                reverse=True,
            )
        distances = self._bot_object._distance_units_to_pos(self, position)
        unit_dist_dict = {unit.tag: dist for unit, dist in zip(self, distances)}
        return sorted(self, key=lambda unit2: abs(unit_dist_dict[unit2.tag] - distance), reverse=True)

    def n_closest_to_distance(self, position: Point2, distance: float, n: int) -> Units:
        """Returns n units that are the closest to distance away.
        For example if the distance is set to 5 and you want 3 units, from units with distance [3, 4, 5, 6, 7] to position,
        the units with distance [4, 5, 6] will be returned

        :param position:
        :param distance:
        """
        return self.subgroup(self._list_sorted_closest_to_distance(position=position, distance=distance)[:n])

    def n_furthest_to_distance(self, position: Point2, distance: float, n: int) -> Units:
        """Inverse of the function 'n_closest_to_distance', returns the furthest units instead

        :param position:
        :param distance:
        """
        return self.subgroup(self._list_sorted_closest_to_distance(position=position, distance=distance)[-n:])

    def subgroup(self, units: Iterable[Unit]) -> Units:
        """Creates a new mutable Units object from Units or list object.

        :param units:
        """
        return Units(units, self._bot_object)

    def filter(self, pred: Callable[[Unit], Any]) -> Units:
        """Filters the current Units object and returns a new Units object.

        Example::

            from sc2.ids.unit_typeid import UnitTypeId
            my_marines = self.units.filter(lambda unit: unit.type_id == UnitTypeId.MARINE)

            completed_structures = self.structures.filter(lambda structure: structure.is_ready)

            queens_with_energy_to_inject = self.units.filter(lambda unit: unit.type_id == UnitTypeId.QUEEN and unit.energy >= 25)

            orbitals_with_energy_to_mule = self.structures.filter(lambda structure: structure.type_id == UnitTypeId.ORBITALCOMMAND and structure.energy >= 50)

            my_units_that_can_shoot_up = self.units.filter(lambda unit: unit.can_attack_air)

        See more unit properties in unit.py

        :param pred:
        """
        assert callable(pred), "Function is not callable"
        return self.subgroup(filter(pred, self))

    def sorted(self, key: Callable[[Unit], Any], reverse: bool = False) -> Units:
        return self.subgroup(sorted(self, key=key, reverse=reverse))

    def _list_sorted_by_distance_to(self, position: Union[Unit, Point2], reverse: bool = False) -> List[Unit]:
        """This function should be a bit faster than using units.sorted(key=lambda u: u.distance_to(position))

        :param position:
        :param reverse:
        """
        if isinstance(position, Unit):
            return sorted(
                self, key=lambda unit: self._bot_object._distance_squared_unit_to_unit(unit, position), reverse=reverse
            )
        distances = self._bot_object._distance_units_to_pos(self, position)
        unit_dist_dict = {unit.tag: dist for unit, dist in zip(self, distances)}
        return sorted(self, key=lambda unit2: unit_dist_dict[unit2.tag], reverse=reverse)

    def sorted_by_distance_to(self, position: Union[Unit, Point2], reverse: bool = False) -> Units:
        """This function should be a bit faster than using units.sorted(key=lambda u: u.distance_to(position))

        :param position:
        :param reverse:
        """
        return self.subgroup(self._list_sorted_by_distance_to(position, reverse=reverse))

    def tags_in(self, other: Iterable[int]) -> Units:
        """Filters all units that have their tags in the 'other' set/list/dict

        Example::

            my_inject_queens = self.units.tags_in(self.queen_tags_assigned_to_do_injects)

            # Do not use the following as it is slower because it first loops over all units to filter out if they are queens and loops over those again to check if their tags are in the list/set
            my_inject_queens_slow = self.units(QUEEN).tags_in(self.queen_tags_assigned_to_do_injects)

        :param other:
        """
        return self.filter(lambda unit: unit.tag in other)

    def tags_not_in(self, other: Iterable[int]) -> Units:
        """Filters all units that have their tags not in the 'other' set/list/dict

        Example::

            my_non_inject_queens = self.units.tags_not_in(self.queen_tags_assigned_to_do_injects)

            # Do not use the following as it is slower because it first loops over all units to filter out if they are queens and loops over those again to check if their tags are in the list/set
            my_non_inject_queens_slow = self.units(QUEEN).tags_not_in(self.queen_tags_assigned_to_do_injects)

        :param other:
        """
        return self.filter(lambda unit: unit.tag not in other)

    @property
    def center(self) -> Point2:
        """ Returns the central position of all units. """
        assert self, "Units object is empty"
        return Point2(
            (
                sum(unit._proto.pos.x for unit in self) / self.amount,
                sum(unit._proto.pos.y for unit in self) / self.amount,
            )
        )

    @property
    def selected(self) -> Units:
        """ Returns all units that are selected by the human player. """
        return self.filter(lambda unit: unit.is_selected)

    @property
    def tags(self) -> Set[int]:
        """ Returns all unit tags as a set. """
        return {unit.tag for unit in self}

    @property
    def ready(self) -> Units:
        """ Returns all structures that are ready (construction complete). """
        return self.filter(lambda unit: unit.is_ready)

    @property
    def not_ready(self) -> Units:
        """ Returns all structures that are not ready (construction not complete). """
        return self.filter(lambda unit: not unit.is_ready)

    @property
    def idle(self) -> Units:
        """ Returns all units or structures that are doing nothing (unit is standing still, structure is doing nothing). """
        return self.filter(lambda unit: unit.is_idle)

    @property
    def owned(self) -> Units:
        """ Deprecated: All your units. """
        return self.filter(lambda unit: unit.is_mine)

    @property
    def enemy(self) -> Units:
        """ Deprecated: All enemy units."""
        return self.filter(lambda unit: unit.is_enemy)

    @property
    def flying(self) -> Units:
        """ Returns all units that are flying. """
        return self.filter(lambda unit: unit.is_flying)

    @property
    def not_flying(self) -> Units:
        """ Returns all units that not are flying. """
        return self.filter(lambda unit: not unit.is_flying)

    @property
    def structure(self) -> Units:
        """ Deprecated: All structures. """
        return self.filter(lambda unit: unit.is_structure)

    @property
    def not_structure(self) -> Units:
        """ Deprecated: All units that are not structures. """
        return self.filter(lambda unit: not unit.is_structure)

    @property
    def gathering(self) -> Units:
        """ Returns all workers that are mining minerals or vespene (gather command). """
        return self.filter(lambda unit: unit.is_gathering)

    @property
    def returning(self) -> Units:
        """ Returns all workers that are carrying minerals or vespene and are returning to a townhall. """
        return self.filter(lambda unit: unit.is_returning)

    @property
    def collecting(self) -> Units:
        """ Returns all workers that are mining or returning resources. """
        return self.filter(lambda unit: unit.is_collecting)

    @property
    def visible(self) -> Units:
        """Returns all units or structures that are visible.
        TODO: add proper description on which units are exactly visible (not snapshots?)"""
        return self.filter(lambda unit: unit.is_visible)

    @property
    def mineral_field(self) -> Units:
        """ Returns all units that are mineral fields. """
        return self.filter(lambda unit: unit.is_mineral_field)

    @property
    def vespene_geyser(self) -> Units:
        """ Returns all units that are vespene geysers. """
        return self.filter(lambda unit: unit.is_vespene_geyser)

    @property
    def prefer_idle(self) -> Units:
        """ Sorts units based on if they are idle. Idle units come first. """
        return self.sorted(lambda unit: unit.is_idle, reverse=True)
