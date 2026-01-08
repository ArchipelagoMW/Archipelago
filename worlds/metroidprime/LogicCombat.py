from enum import Enum

from BaseClasses import CollectionState
from .Items import SuitUpgrade, get_item_for_options
from .Logic import (
    can_charge_beam,
    can_plasma_beam,
    can_power_beam,
    can_wave_beam,
    can_xray,
    has_energy_tanks,
)
from .data.RoomNames import RoomName
import typing

if typing.TYPE_CHECKING:
    from . import MetroidPrimeWorld


class CombatLogicDifficulty(Enum):
    NO_LOGIC = -1
    NORMAL = 0
    MINIMAL = 1


def _can_combat_generic(
    world: "MetroidPrimeWorld",
    state: CollectionState,
    normal_tanks: int,
    minimal_tanks: int,
    requires_charge_beam: bool = True,
) -> bool:
    difficulty = CombatLogicDifficulty(world.options.combat_logic_difficulty)
    if difficulty == CombatLogicDifficulty.NO_LOGIC:
        return True
    elif difficulty == CombatLogicDifficulty.NORMAL:
        return has_energy_tanks(world, state, normal_tanks) and (
            can_charge_beam(world, state) or not requires_charge_beam
        )
    elif difficulty == CombatLogicDifficulty.MINIMAL:
        return has_energy_tanks(world, state, minimal_tanks) and (
            can_charge_beam(world, state) or not requires_charge_beam
        )
    return True


def can_combat_mines(world: "MetroidPrimeWorld", state: CollectionState) -> bool:
    return _can_combat_generic(world, state, 5, 3)


def can_combat_labs(world: "MetroidPrimeWorld", state: CollectionState) -> bool:
    return world.starting_room_name in [
        RoomName.East_Tower.value,
        RoomName.Save_Station_B.value,
        RoomName.Quarantine_Monitor.value,
    ] or _can_combat_generic(world, state, 1, 0, False)


def can_combat_thardus(world: "MetroidPrimeWorld", state: CollectionState) -> bool:
    """Require charge and plasma or power for thardus on normal"""
    if world.starting_room_name in [
        RoomName.Quarantine_Monitor.value,
        RoomName.Save_Station_B.value,
    ]:
        return (
            can_plasma_beam(world, state)
            or can_power_beam(world, state)
            or can_wave_beam(world, state)
        )
    difficulty = world.options.combat_logic_difficulty.value
    if difficulty == CombatLogicDifficulty.NO_LOGIC.value:
        return True
    elif difficulty == CombatLogicDifficulty.NORMAL.value:
        return has_energy_tanks(world, state, 3) and (
            can_charge_beam(world, state)
            and (can_plasma_beam(world, state) or can_power_beam(world, state))
        )
    elif difficulty == CombatLogicDifficulty.MINIMAL.value:
        return (
            can_plasma_beam(world, state)
            or can_power_beam(world, state)
            or can_wave_beam(world, state)
        )
    return True


def can_combat_omega_pirate(world: "MetroidPrimeWorld", state: CollectionState) -> bool:
    return _can_combat_generic(world, state, 6, 3) and can_xray(world, state, True)


def can_combat_flaahgra(world: "MetroidPrimeWorld", state: CollectionState) -> bool:
    return (
        world.starting_room_name == RoomName.Sunchamber_Lobby.value
        or _can_combat_generic(world, state, 2, 1, False)
    )


def can_combat_ridley(world: "MetroidPrimeWorld", state: CollectionState) -> bool:
    return _can_combat_generic(world, state, 8, 8)


def can_combat_prime(world: "MetroidPrimeWorld", state: CollectionState) -> bool:
    return _can_combat_generic(world, state, 8, 5)


def can_combat_ghosts(world: "MetroidPrimeWorld", state: CollectionState) -> bool:
    difficulty = world.options.combat_logic_difficulty.value
    if difficulty == CombatLogicDifficulty.NO_LOGIC.value:
        return True
    elif difficulty == CombatLogicDifficulty.NORMAL.value:
        return (
            can_charge_beam(world, state, SuitUpgrade.Power_Beam)
            and can_power_beam(world, state)
            and can_xray(world, state, True)
        )
    elif difficulty == CombatLogicDifficulty.MINIMAL.value:
        return can_power_beam(world, state)
    return True


def can_combat_beam_pirates(
    world: "MetroidPrimeWorld", state: CollectionState, beam_type: SuitUpgrade
) -> bool:
    if world.options.combat_logic_difficulty.value in [
        CombatLogicDifficulty.NO_LOGIC.value,
        CombatLogicDifficulty.MINIMAL.value,
    ]:
        return True
    return state.has(get_item_for_options(world, beam_type).value, world.player)
