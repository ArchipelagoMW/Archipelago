# pylint: disable=W0212
from __future__ import annotations

from bisect import bisect_left
from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, List, Optional, Union

from .data import Attribute, Race

# Set of parts of names of abilities that have no cost
# E.g every ability that has 'Hold' in its name is free
FREE_ABILITIES = {"Lower", "Raise", "Land", "Lift", "Hold", "Harvest"}


class GameData:

    def __init__(self, data):
        """
        :param data:
        """
        self.abilities: Dict[int, AbilityData] = {a.ability_id: AbilityData(self, a) for a in data.abilities if a.available}
        self.units: Dict[int, UnitTypeData] = {u.unit_id: UnitTypeData(self, u) for u in data.units if u.available}
        self.upgrades: Dict[int, UpgradeData] = {u.upgrade_id: UpgradeData(self, u) for u in data.upgrades}
        # Cached UnitTypeIds so that conversion does not take long. This needs to be moved elsewhere if a new GameData object is created multiple times per game


class AbilityData:

    @classmethod
    def id_exists(cls, ability_id):
        assert isinstance(ability_id, int), f"Wrong type: {ability_id} is not int"
        if ability_id == 0:
            return False
        i = bisect_left(cls.ability_ids, ability_id)  # quick binary search
        return i != len(cls.ability_ids) and cls.ability_ids[i] == ability_id

    def __init__(self, game_data, proto):
        self._game_data = game_data
        self._proto = proto

        # What happens if we comment this out? Should this not be commented out? What is its purpose?
        # assert self.id != 0 # let the world burn

    def __repr__(self) -> str:
        return f"AbilityData(name={self._proto.button_name})"

    @property
    def link_name(self) -> str:
        """ For Stimpack this returns 'BarracksTechLabResearch' """
        return self._proto.link_name

    @property
    def button_name(self) -> str:
        """ For Stimpack this returns 'Stimpack' """
        return self._proto.button_name

    @property
    def friendly_name(self) -> str:
        """ For Stimpack this returns 'Research Stimpack' """
        return self._proto.friendly_name

    @property
    def is_free_morph(self) -> bool:
        return any(free in self._proto.link_name for free in FREE_ABILITIES)

    @property
    def cost(self) -> Cost:
        return self._game_data.calculate_ability_cost(self.id)


class UnitTypeData:

    def __init__(self, game_data: GameData, proto):
        """
        :param game_data:
        :param proto:
        """
        self._game_data = game_data
        self._proto = proto

    def __repr__(self) -> str:
        return f"UnitTypeData(name={self.name})"

    @property
    def name(self) -> str:
        return self._proto.name

    @property
    def creation_ability(self) -> Optional[AbilityData]:
        if self._proto.ability_id == 0:
            return None
        if self._proto.ability_id not in self._game_data.abilities:
            return None
        return self._game_data.abilities[self._proto.ability_id]

    @property
    def footprint_radius(self) -> Optional[float]:
        """ See unit.py footprint_radius """
        if self.creation_ability is None:
            return None
        return self.creation_ability._proto.footprint_radius

    @property
    def attributes(self) -> List[Attribute]:
        return self._proto.attributes

    def has_attribute(self, attr) -> bool:
        assert isinstance(attr, Attribute)
        return attr in self.attributes

    @property
    def has_minerals(self) -> bool:
        return self._proto.has_minerals

    @property
    def has_vespene(self) -> bool:
        return self._proto.has_vespene

    @property
    def cargo_size(self) -> int:
        """ How much cargo this unit uses up in cargo_space """
        return self._proto.cargo_size

    @property
    def race(self) -> Race:
        return Race(self._proto.race)

    @property
    def cost(self) -> Cost:
        return Cost(self._proto.mineral_cost, self._proto.vespene_cost, self._proto.build_time)

    @property
    def cost_zerg_corrected(self) -> Cost:
        """ This returns 25 for extractor and 200 for spawning pool instead of 75 and 250 respectively """
        if self.race == Race.Zerg and Attribute.Structure.value in self.attributes:
            return Cost(self._proto.mineral_cost - 50, self._proto.vespene_cost, self._proto.build_time)
        return self.cost


class UpgradeData:

    def __init__(self, game_data: GameData, proto):
        """
        :param game_data:
        :param proto:
        """
        self._game_data = game_data
        self._proto = proto

    def __repr__(self):
        return f"UpgradeData({self.name} - research ability: {self.research_ability}, {self.cost})"

    @property
    def name(self) -> str:
        return self._proto.name

    @property
    def research_ability(self) -> Optional[AbilityData]:
        if self._proto.ability_id == 0:
            return None
        if self._proto.ability_id not in self._game_data.abilities:
            return None
        return self._game_data.abilities[self._proto.ability_id]

    @property
    def cost(self) -> Cost:
        return Cost(self._proto.mineral_cost, self._proto.vespene_cost, self._proto.research_time)


@dataclass
class Cost:
    """
    The cost of an action, a structure, a unit or a research upgrade.
    The time is given in frames (22.4 frames per game second).
    """
    minerals: int
    vespene: int
    time: Optional[float] = None

    def __repr__(self) -> str:
        return f"Cost({self.minerals}, {self.vespene})"

    def __eq__(self, other: Cost) -> bool:
        return self.minerals == other.minerals and self.vespene == other.vespene

    def __ne__(self, other: Cost) -> bool:
        return self.minerals != other.minerals or self.vespene != other.vespene

    def __bool__(self) -> bool:
        return self.minerals != 0 or self.vespene != 0

    def __add__(self, other) -> Cost:
        if not other:
            return self
        if not self:
            return other
        time = (self.time or 0) + (other.time or 0)
        return Cost(self.minerals + other.minerals, self.vespene + other.vespene, time=time)

    def __sub__(self, other: Cost) -> Cost:
        time = (self.time or 0) + (other.time or 0)
        return Cost(self.minerals - other.minerals, self.vespene - other.vespene, time=time)

    def __mul__(self, other: int) -> Cost:
        return Cost(self.minerals * other, self.vespene * other, time=self.time)

    def __rmul__(self, other: int) -> Cost:
        return Cost(self.minerals * other, self.vespene * other, time=self.time)
