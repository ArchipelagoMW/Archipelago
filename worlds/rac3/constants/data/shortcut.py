"""This module contains the dataclass for Shortcuts in Ratchet and Clank 3"""
from dataclasses import dataclass

from worlds.rac3.constants.items import RAC3ITEM
from worlds.rac3.constants.progress_flag import RAC3PROGRESSFLAG
from worlds.rac3.constants.region import RAC3REGION
from worlds.rac3.constants.shortcuts import RAC3SHORTCUTS


@dataclass
class RAC3SHORTCUTDATA:
    """Data structure for Shortcuts"""
    NAME: str
    PLANET: str
    ITEMS: list[list[str]] | None
    FLAG_ADDRESSES: list[tuple[int, int]] | None
    VISIT_ADDRESSES: list[str] | None

    def __init__(self,
                 planet: str,
                 items: list[list[str]] = None,
                 flag: list[tuple[int, int]] = None,
                 visit: list[str] = None):
        self.PLANET = planet
        self.ITEMS = items
        self.FLAG_ADDRESSES = flag
        self.VISIT_ADDRESSES = visit


# Todo: Replace logic checks here with rule builder
RAC3_SHORTCUT_DATA_TABLE: dict[str, RAC3SHORTCUTDATA] = {
    # RAC3SHORTCUTS.VELDIN_SKIP: RAC3SHORTCUTDATA(RAC3REGION.VELDIN),
    RAC3SHORTCUTS.FLORANA_BRIDGE: RAC3SHORTCUTDATA(RAC3REGION.FLORANA, [[RAC3ITEM.HELI_PACK, RAC3ITEM.CLANK,
                                                                         RAC3ITEM.PROGRESSIVE_PACK,
                                                                         RAC3ITEM.CHARGE_BOOTS]],
                                                   [RAC3PROGRESSFLAG.FLORANA_REACH_PATH_OF_DEATH]),
    RAC3SHORTCUTS.MARCADIA_DROPSHIP: RAC3SHORTCUTDATA(RAC3REGION.MARCADIA,
                                                      flag=[RAC3PROGRESSFLAG.MARCADIA_REACH_THE_DROPSHIP]),
    RAC3SHORTCUTS.MARCADIA_LDF: RAC3SHORTCUTDATA(RAC3REGION.MARCADIA,
                                                 flag=[RAC3PROGRESSFLAG.MARCADIA_COMPLETE_RANGER_MISSIONS]),
    RAC3SHORTCUTS.DAXX_TELEPORTER: RAC3SHORTCUTDATA(RAC3REGION.DAXX, [[RAC3ITEM.HYPERSHOT, RAC3ITEM.HELI_PACK],
                                                                      [RAC3ITEM.HYPERSHOT, RAC3ITEM.CLANK],
                                                                      [RAC3ITEM.HYPERSHOT, RAC3ITEM.PROGRESSIVE_PACK]],
                                                    [RAC3PROGRESSFLAG.DAXX_WARSHIP_PRE_FIGHT_CHECKPOINT]),
    RAC3SHORTCUTS.AQUATOS_SHUTTLE: RAC3SHORTCUTDATA(RAC3REGION.AQUATOS, visit=[RAC3REGION.AQUATOS_SEWERS]),
    RAC3SHORTCUTS.TYHRRANOSIS_INTRO: RAC3SHORTCUTDATA(RAC3REGION.TYHRRANOSIS,
                                                      flag=[RAC3PROGRESSFLAG.TYHRRANOSIS_COMPLETE_PROLOGUE]),
    RAC3SHORTCUTS.TYHRRANOSIS_DROPSHIP: RAC3SHORTCUTDATA(RAC3REGION.TYHRRANOSIS,
                                                         flag=[RAC3PROGRESSFLAG.TYHRRANOSIS_RANGER_DROPSHIP_SPAWNS]),
    RAC3SHORTCUTS.OBANI_GEMINI_TELEPORTER: RAC3SHORTCUTDATA(RAC3REGION.OBANI_GEMINI, [[RAC3ITEM.REFRACTOR]],
                                                            [RAC3PROGRESSFLAG.OBANI_GEMINI_TELEPORT_TO_POLUX_3]),
    RAC3SHORTCUTS.HOLOSTAR_CLANK: RAC3SHORTCUTDATA(RAC3REGION.HOLOSTAR_STUDIOS,
                                                   visit=[RAC3REGION.HOLOSTAR_STUDIOS_CLANK]),
    RAC3SHORTCUTS.HOLOSTAR_TELEPORTER: RAC3SHORTCUTDATA(RAC3REGION.HOLOSTAR_STUDIOS,
                                                        [[RAC3ITEM.HACKER, RAC3ITEM.HYPERSHOT]],
                                                        [RAC3PROGRESSFLAG.HOLOSTAR_STUDIOS_REACH_THE_SHIP]),
    RAC3SHORTCUTS.KOROS_TELEPORTER: RAC3SHORTCUTDATA(RAC3REGION.KOROS, flag=[RAC3PROGRESSFLAG.KOROS_HALFWAY_CHECKPOINT,
                                                                             RAC3PROGRESSFLAG.KOROS_FIRE_THE_CANNON]),
    RAC3SHORTCUTS.METROPOLIS_TAXI: RAC3SHORTCUTDATA(RAC3REGION.METROPOLIS, [[RAC3ITEM.GRAV_BOOTS,
                                                                             RAC3ITEM.REFRACTOR]],
                                                    [RAC3PROGRESSFLAG.METROPOLIS_TAXI_SPAWN,
                                                     RAC3PROGRESSFLAG.METROPOLIS_KLUNK_FIGHT_START]),
    RAC3SHORTCUTS.METROPOLIS_DROPSHIP: RAC3SHORTCUTDATA(RAC3REGION.METROPOLIS, [[RAC3ITEM.GRAV_BOOTS,
                                                                                 RAC3ITEM.REFRACTOR]],
                                                        [RAC3PROGRESSFLAG.METROPOLIS_DEFEATED_KLUNK]),
    RAC3SHORTCUTS.HIDEOUT_TELEPORTER: RAC3SHORTCUTDATA(RAC3REGION.QWARKS_HIDEOUT, [[RAC3ITEM.GRAV_BOOTS]],
                                                       [RAC3PROGRESSFLAG.QWARKS_HIDEOUT_REACH_PDA_VENDOR]),
    RAC3SHORTCUTS.HIDEOUT_TAXI: RAC3SHORTCUTDATA(RAC3REGION.QWARKS_HIDEOUT, [[RAC3ITEM.WARP_PAD, RAC3ITEM.HYPERSHOT]],
                                                 [RAC3PROGRESSFLAG.QWARKS_HIDEOUT_FINISHED_CLANK_SECTION]),
    RAC3SHORTCUTS.DRACO_TELEPORTER: RAC3SHORTCUTDATA(RAC3REGION.OBANI_DRACO, [[RAC3ITEM.GRAV_BOOTS]],
                                                     [RAC3PROGRESSFLAG.OBANI_DRACO_REACH_THE_CONTROL_ROOM]),
    RAC3SHORTCUTS.COMMAND_DROPSHIP: RAC3SHORTCUTDATA(RAC3REGION.COMMAND_CENTER, [[RAC3ITEM.HYPERSHOT,
                                                                                  RAC3ITEM.HACKER,
                                                                                  RAC3ITEM.GRAV_BOOTS,
                                                                                  RAC3ITEM.TYHRRA_GUISE,
                                                                                  RAC3ITEM.REFRACTOR]],
                                                     [RAC3PROGRESSFLAG.COMMAND_CENTER_FORCE_SPAWN_DROPSHIP_BY_SHIP]),
}
