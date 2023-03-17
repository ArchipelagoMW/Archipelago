from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Union

from sc2.constants import COMBINEABLE_ABILITIES
from sc2.ids.ability_id import AbilityId
from sc2.position import Point2

if TYPE_CHECKING:
    from sc2.unit import Unit


class UnitCommand:

    def __init__(self, ability: AbilityId, unit: Unit, target: Union[Unit, Point2] = None, queue: bool = False):
        """
        :param ability:
        :param unit:
        :param target:
        :param queue:
        """
        assert ability in AbilityId, f"ability {ability} is not in AbilityId"
        assert unit.__class__.__name__ == "Unit", f"unit {unit} is of type {type(unit)}"
        assert any(
            [
                target is None,
                isinstance(target, Point2),
                unit.__class__.__name__ == "Unit",
            ]
        ), f"target {target} is of type {type(target)}"
        assert isinstance(queue, bool), f"queue flag {queue} is of type {type(queue)}"
        self.ability = ability
        self.unit = unit
        self.target = target
        self.queue = queue

    @property
    def combining_tuple(self) -> Tuple[AbilityId, Union[Unit, Point2], bool, bool]:
        return self.ability, self.target, self.queue, self.ability in COMBINEABLE_ABILITIES

    def __repr__(self):
        return f"UnitCommand({self.ability}, {self.unit}, {self.target}, {self.queue})"
