import random

from .daphne_gate_types import Block, BlockKey, DaphneBlocks
from .game import GameOptions
from .item_data import Items
from .logic_shortcut import LogicShortcut
from .terrain_patch import Patch, Space
from .terrain_patch_data import wrecked_air_lock, wrecked_air_lock_screw_bts, \
    wrecked_air_lock_screw_layer_1, air_lock_default, air_lock_non_default, \
    air_lock_hint_layer_1
from .trick_data import Tricks

NOT_REQUIRED_PROBABILITY = 0.9486832980505
""" 2 samples from this will have 10% chance of choosing at least one from required """

SPECIAL = 0xb0
SHOT = 0xc0
GRAPPLE = 0xe0

_BLOCKS: dict[BlockKey, Block] = {
    "Screw": (0xbf, SPECIAL, 0x08),
    "Ice": (0x78, SHOT, 0x0c),
    "Hyper": (0x4b, SHOT, 0x0d),  # TODO: 4b has yellow H (not red)  77 has red W (not H)
    "Spazer": (0x79, SHOT, 0x0e),
    "Plasma": (0x76, SHOT, 0x0f),
    "Grapple": (0xb7, GRAPPLE, 0x02),
    "Speed": (0xb6, SPECIAL, 0x0f),
    "PB": (0x57, SHOT, 0x09),
    "Super": (0x9f, SHOT, 0x0b),
}

_BLOCK_LOGIC: dict[BlockKey, LogicShortcut] = {
    "Screw": LogicShortcut(lambda loadout: (
        Items.Screw in loadout
    )),
    "Ice": LogicShortcut(lambda loadout: (
        Items.Ice in loadout
    )),
    "Hyper": LogicShortcut(lambda loadout: (
        (Items.Charge in loadout) and (Items.Hypercharge in loadout)
    )),
    "Spazer": LogicShortcut(lambda loadout: (
        Items.Spazer in loadout
    )),
    "Plasma": LogicShortcut(lambda loadout: (
        (Items.Plasma in loadout) or
        ((Items.Charge in loadout) and (Items.Hypercharge in loadout))
    )),
    "Grapple": LogicShortcut(lambda loadout: (
        Items.Grapple in loadout
    )),
    "Speed": LogicShortcut(lambda loadout: (
        Items.SpeedBooster in loadout
    )),
    "PB": LogicShortcut(lambda loadout: (
        (Items.Morph in loadout) and (Items.PowerBomb in loadout)
    )),
    "Super": LogicShortcut(lambda loadout: (
        Items.Super in loadout
    )),
}


def _get_required_and_not_required_blocks(options: GameOptions) -> tuple[list[BlockKey], list[BlockKey]]:
    """
    separate the possible blocks into
    what we know is required from looking at the options,
    and what we don't know is required from looking at the options
    """
    speed_required = not (options.escape_shortcuts or options.area_rando or (
        Tricks.super_sink_hard in options.logic
    ))
    grapple_required = not (Tricks.ice_clip in options.logic or Tricks.xray_climb in options.logic)

    not_required: list[BlockKey] = ["Screw", "Ice", "Hyper", "Spazer", "Plasma"]
    required: list[BlockKey] = ["PB", "Super"]

    if speed_required:
        required.append("Speed")
    else:
        not_required.append("Speed")

    if grapple_required:
        required.append("Grapple")
    else:
        not_required.append("Grapple")

    return required, not_required


def get_daphne_gate(options: GameOptions) -> DaphneBlocks:
    required, not_required = _get_required_and_not_required_blocks(options)

    if random.random() < NOT_REQUIRED_PROBABILITY:
        one = random.choice(not_required)
        not_required.remove(one)
    else:
        one = random.choice(required)
        required.remove(one)

    if random.random() < NOT_REQUIRED_PROBABILITY:
        two: BlockKey = random.choice(not_required)
        not_required.remove(two)
    else:
        two = random.choice(required)
        required.remove(two)

    # make sure screw is not on bottom
    if two == "Screw":  # screw
        one, two = two, one

    return DaphneBlocks(one, two)


def get_gate_logic(db: DaphneBlocks) -> LogicShortcut:
    two_logic = LogicShortcut(lambda loadout: (
        (_BLOCK_LOGIC[db.two] in loadout) and
        (Items.Morph in loadout) and
        (
            (
                (Items.Speedball in loadout) or
                ((Tricks.mockball_hard in loadout) and (Tricks.short_charge_2 in loadout))
            ) if db.two == "Speed" else True
        )
    ))

    return LogicShortcut(lambda loadout: (
        (_BLOCK_LOGIC[db.one] in loadout) or
        (two_logic in loadout)
    ))


def get_air_lock_bytes(db: DaphneBlocks) -> tuple[Patch, Patch, Patch]:
    """ wrecked, non-default, default """
    wrecked_air_lock_b = wrecked_air_lock.copy()
    for i, addr in enumerate(wrecked_air_lock_screw_layer_1):
        if i < 3:
            block = _BLOCKS[db.one]
        else:
            block = _BLOCKS[db.two]
        wrecked_air_lock_b[addr + 1] = block[1]
        wrecked_air_lock_b[addr] = block[0]
    for i, addr in enumerate(wrecked_air_lock_screw_bts):
        if i < 3:
            block = _BLOCKS[db.one]
        else:
            block = _BLOCKS[db.two]
        wrecked_air_lock_b[addr] = block[2]

    air_lock_non_default_b = air_lock_non_default.copy()
    air_lock_default_b = air_lock_default.copy()
    for i, addr in enumerate(air_lock_hint_layer_1):
        if i < 3:
            block = _BLOCKS[db.one]
        else:
            block = _BLOCKS[db.two]
        air_lock_non_default_b[addr + 1] = block[1]
        air_lock_non_default_b[addr] = block[0]
        air_lock_default_b[addr + 1] = block[1]
        air_lock_default_b[addr] = block[0]

    return (
        Patch(wrecked_air_lock_b, [0x782ab, 0x782c5], Space(412, 1564770)),
        Patch(air_lock_non_default_b, [0x7eb2d], Space(343, 1556578)),
        Patch(air_lock_default_b, [0x7eb13], Space(349, 1557973))
    )
