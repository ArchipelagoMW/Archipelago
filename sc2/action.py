from __future__ import annotations

from itertools import groupby
from typing import TYPE_CHECKING, Union

from s2clientprotocol import raw_pb2 as raw_pb

from sc2.position import Point2
from sc2.unit import Unit

if TYPE_CHECKING:
    from sc2.ids.ability_id import AbilityId
    from sc2.unit_command import UnitCommand


# pylint: disable=R0912
def combine_actions(action_iter):
    """
    Example input:
    [
        # Each entry in the list is a unit command, with an ability, unit, target, and queue=boolean
        UnitCommand(AbilityId.TRAINQUEEN_QUEEN, Unit(name='Hive', tag=4353687554), None, False),
        UnitCommand(AbilityId.TRAINQUEEN_QUEEN, Unit(name='Lair', tag=4359979012), None, False),
        UnitCommand(AbilityId.TRAINQUEEN_QUEEN, Unit(name='Hatchery', tag=4359454723), None, False),
    ]
    """
    for key, items in groupby(action_iter, key=lambda a: a.combining_tuple):
        ability: AbilityId
        target: Union[None, Point2, Unit]
        queue: bool
        # See constants.py for combineable abilities
        combineable: bool
        ability, target, queue, combineable = key

        if combineable:
            # Combine actions with no target, e.g. lift, burrowup, burrowdown, siege, unsiege, uproot spines
            cmd = raw_pb.ActionRawUnitCommand(
                ability_id=ability.value, unit_tags={u.unit.tag
                                                     for u in items}, queue_command=queue
            )
            # Combine actions with target point, e.g. attack_move or move commands on a position
            if isinstance(target, Point2):
                cmd.target_world_space_pos.x = target.x
                cmd.target_world_space_pos.y = target.y
            # Combine actions with target unit, e.g. attack commands directly on a unit
            elif isinstance(target, Unit):
                cmd.target_unit_tag = target.tag
            elif target is not None:
                raise RuntimeError(f"Must target a unit, point or None, found '{target !r}'")

            yield raw_pb.ActionRaw(unit_command=cmd)

        else:
            """
            Return one action for each unit; this is required for certain commands that would otherwise be grouped, and only executed once
            Examples:
            Select 3 hatcheries, build a queen with each hatch - the grouping function would group these unit tags and only issue one train command once to all 3 unit tags - resulting in one total train command
            I imagine the same thing would happen to certain other abilities: Battlecruiser yamato on same target, queen transfuse on same target, ghost snipe on same target, all build commands with the same unit type and also all morphs (zergling to banelings)
            However, other abilities can and should be grouped, see constants.py 'COMBINEABLE_ABILITIES'
            """
            u: UnitCommand
            if target is None:
                for u in items:
                    cmd = raw_pb.ActionRawUnitCommand(
                        ability_id=ability.value, unit_tags={u.unit.tag}, queue_command=queue
                    )
                    yield raw_pb.ActionRaw(unit_command=cmd)
            elif isinstance(target, Point2):
                for u in items:
                    cmd = raw_pb.ActionRawUnitCommand(
                        ability_id=ability.value,
                        unit_tags={u.unit.tag},
                        queue_command=queue,
                        target_world_space_pos=target.as_Point2D,
                    )
                    yield raw_pb.ActionRaw(unit_command=cmd)

            elif isinstance(target, Unit):
                for u in items:
                    cmd = raw_pb.ActionRawUnitCommand(
                        ability_id=ability.value,
                        unit_tags={u.unit.tag},
                        queue_command=queue,
                        target_unit_tag=target.tag,
                    )
                    yield raw_pb.ActionRaw(unit_command=cmd)
            else:
                raise RuntimeError(f"Must target a unit, point or None, found '{target !r}'")
