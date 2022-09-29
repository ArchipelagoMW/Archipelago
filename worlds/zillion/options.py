from typing import Any, Dict, cast
from Options import AssembleOptions, DefaultOnToggle, ItemDict, Range, SpecialRange, Toggle, Choice
from zilliandomizer.options import \
    Options as ZzOptions, char_to_gun, char_to_jump, ID, \
    VBLR as ZzVBLR, VBLR_CHOICES, chars, Chars, ItemCounts as ZzItemCounts
from zilliandomizer.options.parsing import validate as zz_validate


class ZillionContinues(SpecialRange):
    """
    number of continues before game over

    game over teleports you to your ship, keeping items and open doors
    """
    default = 3
    range_start = 0
    range_end = 21
    display_name = "continues"
    special_range_names = {
        "infinity": 21
    }


class ZillionEarlyScope(Toggle):
    display_name = "early scope"


ZillionEarlyScope.__doc__ = ZzOptions.early_scope.__doc__
assert ZillionEarlyScope.__doc__


class ZillionFloppyReq(Range):
    range_start = 0
    range_end = 8
    default = 5
    display_name = "floppies required"


ZillionFloppyReq.__doc__ = ZzOptions.floppy_req.__doc__


class VBLR(Choice):
    option_vanilla = 0
    option_balanced = 1
    option_low = 2
    option_restrictive = 3
    default = 1


class ZillionGunLevels(VBLR):
    display_name = "gun levels"


ZillionGunLevels.__doc__ = char_to_gun.__doc__
# TODO: implement at least fixed width font for `` in __doc__


class ZillionJumpLevels(VBLR):
    display_name = "jump levels"


ZillionJumpLevels.__doc__ = char_to_jump.__doc__


class ZillionRandomizeAlarms(DefaultOnToggle):
    display_name = "randomize alarms"


ZillionRandomizeAlarms.__doc__ = ZzOptions.randomize_alarms.__doc__


class ZillionMaxLevel(Range):
    range_start = 3
    range_end = 8
    default = 8
    display_name = "max level"


ZillionMaxLevel.__doc__ = ZzOptions.max_level.__doc__


class ZillionOpasPerLevel(Range):
    range_start = 1
    range_end = 5
    default = 2
    display_name = "opa-opas per level"


ZillionOpasPerLevel.__doc__ = ZzOptions.opas_per_level.__doc__


class ZillionStartChar(Choice):
    option_jj = 0
    option_apple = 1
    option_champ = 2
    display_name = "start character"
    default = 0  # "random"  # TODO: implement this


class ZillionItemCounts(ItemDict):
    """ how many of each item is in the game """
    default = {
        "ID Card": 50,
        "Bread": 35,
        "Opa-Opa": 26,
        "Zillion": 10,
        "Floppy Disk": 7,
        "Scope": 4,
        "Red ID Card": 2
    }
    display_name = "item counts"

    def __init__(self, value: Dict[str, int]) -> None:
        super().__init__(value)
        # need all items, so fill in missing items with default
        for name, number in ZillionItemCounts.default.items():
            if name not in self.value:
                self.value[name] = number


class ZillionSkill(Range):
    range_start = 0
    range_end = 5
    default = 2


class ZillionStartingCards(SpecialRange):
    default = 2
    range_start = 0
    range_end = 10
    display_name = "starting cards"
    special_range_names = {
        "vanilla": 0
    }


ZillionStartingCards.__doc__ = ZzOptions.starting_cards.__doc__


class ZillionRoomGen(Toggle):
    display_name = "room generation"


ZillionRoomGen.__doc__ = ZzOptions.room_gen.__doc__


zillion_options: Dict[str, AssembleOptions] = {
    "continues": ZillionContinues,
    # "early_scope": ZillionEarlyScope,  # TODO: implement
    "floppy_req": ZillionFloppyReq,
    "gun_levels": ZillionGunLevels,
    "jump_levels": ZillionJumpLevels,
    "randomize_alarms": ZillionRandomizeAlarms,
    "max_level": ZillionMaxLevel,
    "start_char": ZillionStartChar,
    "opas_per_level": ZillionOpasPerLevel,
    "item_counts": ZillionItemCounts,
    "skill": ZillionSkill,
    "starting_cards": ZillionStartingCards,
    "room_gen": ZillionRoomGen,
}


def convert_item_counts(ic: ZillionItemCounts) -> ZzItemCounts:
    tr: ZzItemCounts = {
        ID.card: ic.value["ID Card"],
        ID.red: ic.value["Red ID Card"],
        ID.floppy: ic.value["Floppy Disk"],
        ID.bread: ic.value["Bread"],
        ID.gun: ic.value["Zillion"],
        ID.opa: ic.value["Opa-Opa"],
        ID.scope: ic.value["Scope"],
        ID.empty: ic.value["Empty"],
    }
    return tr


def validate(wo: Any, p: int) -> ZzOptions:
    """
    adjusts options to make game completion possible

    `wo` parameter is world object that has my options on it
    `p` is my player id
    """
    for option_name in zillion_options:
        assert hasattr(wo, option_name), f"Zillion option {option_name} didn't get put in world object"

    jump_levels = cast(ZillionJumpLevels, wo.jump_levels[p])
    jump_option = jump_levels.get_current_option_name().lower()
    assert jump_option in VBLR_CHOICES, f"{jump_option} in {VBLR_CHOICES}"
    required_level = char_to_jump["Apple"][cast(ZzVBLR, jump_option)].index(3) + 1

    gun_levels = cast(ZillionGunLevels, wo.gun_levels[p])
    gun_option = gun_levels.get_current_option_name().lower()
    assert gun_option in VBLR_CHOICES, f"{gun_option} in {VBLR_CHOICES}"
    guns_required = char_to_gun["Champ"][cast(ZzVBLR, gun_option)].index(3)

    item_counts = cast(ZillionItemCounts, wo.item_counts[p])
    item_counts.value["Opa-Opa"] = max(required_level - 1, item_counts.value["Opa-Opa"])
    item_counts.value["Zillion"] = max(guns_required, item_counts.value["Zillion"])
    while sum(item_counts.value.values()) > 144:
        total = sum(item_counts.value.values())
        scaler = 144 / total
        for key in item_counts.value:
            item_counts.value[key] = max(1, int(item_counts.value[key] * scaler))
    total = sum(item_counts.value.values())
    diff = 144 - total
    if "Empty" not in item_counts.value:
        item_counts.value["Empty"] = 0
    item_counts.value["Empty"] += diff
    assert sum(item_counts.value.values()) == 144

    max_level = cast(ZillionMaxLevel, wo.max_level[p])
    max_level.value = max(required_level, max_level.value)

    opas_per_level = cast(ZillionOpasPerLevel, wo.opas_per_level[p])
    while (opas_per_level.value > 1) and (1 + item_counts.value["Opa-Opa"] // opas_per_level.value < max_level.value):
        opas_per_level.value -= 1

    # that should be all of the level requirements met

    floppy_req = cast(ZillionFloppyReq, wo.floppy_req[p])
    floppy_req.value = min(item_counts.value["Floppy Disk"], floppy_req.value)

    start_char = cast(ZillionStartChar, wo.start_char[p])
    start_char_name = start_char.get_current_option_name()
    if start_char_name == "Jj":
        start_char_name = "JJ"
    assert start_char_name in chars
    start_char_name = cast(Chars, start_char_name)

    starting_cards = cast(ZillionStartingCards, wo.starting_cards[p])

    room_gen = cast(ZillionRoomGen, wo.room_gen[p])

    zz_item_counts = convert_item_counts(item_counts)
    zz_op = ZzOptions(
        zz_item_counts,
        cast(ZzVBLR, jump_option),
        cast(ZzVBLR, gun_option),
        opas_per_level.value,
        max_level.value,
        False,  # tutorial
        wo.skill[p].value,
        start_char_name,
        floppy_req.value,
        wo.continues[p].value,
        wo.randomize_alarms[p].value,
        False,  # wo.early_scope[p].value,
        True,  # balance defense
        starting_cards.value,
        bool(room_gen.value)
    )
    zz_validate(zz_op)
    return zz_op
