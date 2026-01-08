""" utility functions for logic """

from typing import TYPE_CHECKING

from .item_data import Item, Items
from .logic_shortcut import LogicShortcut
from .trick_data import Tricks

if TYPE_CHECKING:
    from .loadout import Loadout

# TODO: Does some logic around Ocean Shore need to be different
# if Metroid Suit and Supers are in early spaceport?
# If the ship is crashed,
# for example, getting from OceanShoreR to Sandy Gully, is harder.

STARTING_ENERGY = 99
ENERGY_PER_TANK = 100
FOR_N_TANKS = 12
LATER_ENERGY_PER_TANK = 50


def energy_from_tanks(n: int) -> int:
    first_tanks = min(FOR_N_TANKS, n) * ENERGY_PER_TANK
    later_tanks = max(0, n - FOR_N_TANKS) * LATER_ENERGY_PER_TANK
    return STARTING_ENERGY + first_tanks + later_tanks


def energy_req(amount: int) -> LogicShortcut:
    return LogicShortcut(lambda loadout: (
        energy_from_tanks(loadout.count(Items.Energy)) >= amount
    ))


_item_to_ammo: dict[Item, int] = {
    Items.Missile: 10,
    Items.Super: 10,
    Items.PowerBomb: 10,
    Items.LargeAmmo: 10,
    Items.SmallAmmo: 5,
}


def ammo_in_loadout(loadout: "Loadout") -> int:
    total = 0
    for item, value in _item_to_ammo.items():
        total += loadout.count(item) * value
    return total


def ammo_req(amount: int) -> LogicShortcut:
    return LogicShortcut(lambda loadout: (
        ammo_in_loadout(loadout) >= amount
    ))


crystal_flash = LogicShortcut(lambda loadout: (
    loadout.has_all(Items.Morph, Items.PowerBomb, ammo_req(100))
))


def hell_run_energy(min_energy: int, loadout: "Loadout") -> int:
    """
    utility function used in other hell run functions

    based on tricks
    """
    if Tricks.hell_run_hard in loadout:
        return min_energy
    if Tricks.hell_run_medium in loadout:
        return (min_energy * 3) // 2
    if Tricks.hell_run_easy in loadout:
        return min_energy * 2

    # this number is tuned to make it so
    # fiery trail with space jump and screw hell runs are barely unobtainable
    # (but sky temple hell runs are obtainable)
    return int(min_energy ** 1.5046)


def _adjust_for_other_suits(energy_required: int, loadout: "Loadout", heat_and_metroid_suit_not_required: bool) -> int:
    helping_suit_count = (
        int(Items.Aqua in loadout) +
        int(heat_and_metroid_suit_not_required and (Items.MetroidSuit in loadout))
    )
    return (energy_required * (4 - helping_suit_count)) // 4


def varia_or_hell_run(energy: int, *, heat_and_metroid_suit_not_required: bool = False) -> LogicShortcut:
    """
    needs varia or energy or (less energy and crystal flash)

    should be the amount you need if you don't have any suits (unless metroid suit is required)

    (use lava_run for hell runs in lava)

    `heat_and_metroid_suit_not_required` means this hell run is in heat (not cold)
    and the energy amount given is what it takes with 0 suits

    if `heat_and_metroid_suit_not_required` is false, then you can check for metroid suit in the logic
    and give an energy amount for doing the hell run with metroid suit
    """
    return LogicShortcut(lambda loadout: (
        (Items.Varia in loadout) or
        (energy_req(hell_run_energy(
            _adjust_for_other_suits(energy, loadout, heat_and_metroid_suit_not_required), loadout
        )) in loadout) or
        (
            (energy_req(hell_run_energy(
                _adjust_for_other_suits((energy + 100) // 2, loadout, heat_and_metroid_suit_not_required), loadout
            )) in loadout) and
            (crystal_flash in loadout) and
            # 130 because there are too many times when you'll need ammo for something else during hell run
            (ammo_req(130) in loadout)
        )
    ))


def lava_run(energy_with_aqua: int, energy_no_aqua: int) -> LogicShortcut:
    """
    for hell runs in lava that require metroid suit,
    because it slows you down if you don't have aqua suit

    This is not for lava baths without Metroid Suit.
    It's for going in lava with Metroid Suit and without Varia Suit.

    This does not check for Metroid Suit.
    """
    return LogicShortcut(lambda loadout: (
        (
            (Items.Aqua in loadout) and
            (varia_or_hell_run((energy_with_aqua * 4) // 3) in loadout)
            # this math will be reversed when that function sees I have aqua suit
        ) or (
            # no aqua
            (varia_or_hell_run(energy_no_aqua) in loadout)
        )
    ))


def can_use_pbs(pbs_needed: int) -> LogicShortcut:
    """ How many PBs do you need between opportunities to refill ammo? """
    return LogicShortcut(lambda loadout: (
        (Items.Morph in loadout) and
        (Items.PowerBomb in loadout) and
        (ammo_req(pbs_needed * 10) in loadout)
    ))


def can_bomb(pbs_needed: int) -> LogicShortcut:
    """
    If you don't have bombs, how many PBs do you need?
    (between opportunities to refill ammo)
    """
    return LogicShortcut(lambda loadout: (
        (Items.Morph in loadout) and
        ((Items.Bombs in loadout) or (
            (Items.PowerBomb in loadout) and
            (ammo_req(pbs_needed * 10) in loadout)
        ))
    ))
