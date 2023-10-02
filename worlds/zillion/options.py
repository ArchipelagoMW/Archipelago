from collections import Counter
# import logging
from typing import TYPE_CHECKING, Any, Dict, Tuple, cast
from Options import AssembleOptions, DefaultOnToggle, Range, SpecialRange, Toggle, Choice
from zilliandomizer.options import \
    Options as ZzOptions, char_to_gun, char_to_jump, ID, \
    VBLR as ZzVBLR, chars, Chars, ItemCounts as ZzItemCounts
from zilliandomizer.options.parsing import validate as zz_validate
if TYPE_CHECKING:
    from BaseClasses import MultiWorld


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
        "vanilla": 3,
        "infinity": 21
    }


class ZillionFloppyReq(Range):
    """ how many floppy disks are required """
    range_start = 0
    range_end = 8
    default = 5
    display_name = "floppies required"


class VBLR(Choice):
    option_vanilla = 0
    option_balanced = 1
    option_low = 2
    option_restrictive = 3
    default = 1


class ZillionGunLevels(VBLR):
    """
    Zillion gun power for the number of Zillion power ups you pick up

    For "restrictive", Champ is the only one that can get Zillion gun power level 3.
    """
    display_name = "gun levels"


class ZillionJumpLevels(VBLR):
    """
    jump levels for each character level

    For "restrictive", Apple is the only one that can get jump level 3.
    """
    display_name = "jump levels"


class ZillionRandomizeAlarms(DefaultOnToggle):
    """ whether to randomize the locations of alarm sensors """
    display_name = "randomize alarms"


class ZillionMaxLevel(Range):
    """ the highest level you can get """
    range_start = 3
    range_end = 8
    default = 8
    display_name = "max level"


class ZillionOpasPerLevel(Range):
    """
    how many Opa-Opas are required to level up

    Lower makes you level up faster.
    """
    range_start = 1
    range_end = 5
    default = 2
    display_name = "Opa-Opas per level"


class ZillionStartChar(Choice):
    """ which character you start with """
    option_jj = 0
    option_apple = 1
    option_champ = 2
    display_name = "start character"
    default = "random"


class ZillionIDCardCount(Range):
    """
    how many ID Cards are in the game

    Vanilla is 63

    maximum total for all items is 144
    """
    range_start = 0
    range_end = 126
    default = 42
    display_name = "ID Card count"


class ZillionBreadCount(Range):
    """
    how many Breads are in the game

    Vanilla is 33

    maximum total for all items is 144
    """
    range_start = 0
    range_end = 126
    default = 50
    display_name = "Bread count"


class ZillionOpaOpaCount(Range):
    """
    how many Opa-Opas are in the game

    Vanilla is 26

    maximum total for all items is 144
    """
    range_start = 0
    range_end = 126
    default = 26
    display_name = "Opa-Opa count"


class ZillionZillionCount(Range):
    """
    how many Zillion gun power ups are in the game

    Vanilla is 6

    maximum total for all items is 144
    """
    range_start = 0
    range_end = 126
    default = 8
    display_name = "Zillion power up count"


class ZillionFloppyDiskCount(Range):
    """
    how many Floppy Disks are in the game

    Vanilla is 5

    maximum total for all items is 144
    """
    range_start = 0
    range_end = 126
    default = 7
    display_name = "Floppy Disk count"


class ZillionScopeCount(Range):
    """
    how many Scopes are in the game

    Vanilla is 4

    maximum total for all items is 144
    """
    range_start = 0
    range_end = 126
    default = 4
    display_name = "Scope count"


class ZillionRedIDCardCount(Range):
    """
    how many Red ID Cards are in the game

    Vanilla is 1

    maximum total for all items is 144
    """
    range_start = 0
    range_end = 126
    default = 2
    display_name = "Red ID Card count"


class ZillionEarlyScope(Toggle):
    """ make sure Scope is available early """
    display_name = "early scope"


class ZillionSkill(Range):
    """ the difficulty level of the game """
    range_start = 0
    range_end = 5
    default = 2


class ZillionStartingCards(SpecialRange):
    """
    how many ID Cards to start the game with

    Refilling at the ship also ensures you have at least this many cards.
    0 gives vanilla behavior.
    """
    default = 2
    range_start = 0
    range_end = 10
    display_name = "starting cards"
    special_range_names = {
        "vanilla": 0
    }


class ZillionRoomGen(Toggle):
    """ whether to generate rooms with random terrain """
    display_name = "room generation"


zillion_options: Dict[str, AssembleOptions] = {
    "continues": ZillionContinues,
    "floppy_req": ZillionFloppyReq,
    "gun_levels": ZillionGunLevels,
    "jump_levels": ZillionJumpLevels,
    "randomize_alarms": ZillionRandomizeAlarms,
    "max_level": ZillionMaxLevel,
    "start_char": ZillionStartChar,
    "opas_per_level": ZillionOpasPerLevel,
    "id_card_count": ZillionIDCardCount,
    "bread_count": ZillionBreadCount,
    "opa_opa_count": ZillionOpaOpaCount,
    "zillion_count": ZillionZillionCount,
    "floppy_disk_count": ZillionFloppyDiskCount,
    "scope_count": ZillionScopeCount,
    "red_id_card_count": ZillionRedIDCardCount,
    "early_scope": ZillionEarlyScope,
    "skill": ZillionSkill,
    "starting_cards": ZillionStartingCards,
    "room_gen": ZillionRoomGen,
}


def convert_item_counts(ic: "Counter[str]") -> ZzItemCounts:
    tr: ZzItemCounts = {
        ID.card: ic["ID Card"],
        ID.red: ic["Red ID Card"],
        ID.floppy: ic["Floppy Disk"],
        ID.bread: ic["Bread"],
        ID.gun: ic["Zillion"],
        ID.opa: ic["Opa-Opa"],
        ID.scope: ic["Scope"],
        ID.empty: ic["Empty"],
    }
    return tr


def validate(world: "MultiWorld", p: int) -> "Tuple[ZzOptions, Counter[str]]":
    """
    adjusts options to make game completion possible

    `world` parameter is MultiWorld object that has my options on it
    `p` is my player id
    """
    for option_name in zillion_options:
        assert hasattr(world, option_name), f"Zillion option {option_name} didn't get put in world object"
    wo = cast(Any, world)  # so I don't need getattr on all the options

    skill = wo.skill[p].value

    jump_levels = cast(ZillionJumpLevels, wo.jump_levels[p])
    jump_option = jump_levels.current_key
    required_level = char_to_jump["Apple"][cast(ZzVBLR, jump_option)].index(3) + 1
    if skill == 0:
        # because of hp logic on final boss
        required_level = 8

    gun_levels = cast(ZillionGunLevels, wo.gun_levels[p])
    gun_option = gun_levels.current_key
    guns_required = char_to_gun["Champ"][cast(ZzVBLR, gun_option)].index(3)

    floppy_req = cast(ZillionFloppyReq, wo.floppy_req[p])

    card = cast(ZillionIDCardCount, wo.id_card_count[p])
    bread = cast(ZillionBreadCount, wo.bread_count[p])
    opa = cast(ZillionOpaOpaCount, wo.opa_opa_count[p])
    gun = cast(ZillionZillionCount, wo.zillion_count[p])
    floppy = cast(ZillionFloppyDiskCount, wo.floppy_disk_count[p])
    scope = cast(ZillionScopeCount, wo.scope_count[p])
    red = cast(ZillionRedIDCardCount, wo.red_id_card_count[p])
    item_counts = Counter({
        "ID Card": card,
        "Bread": bread,
        "Opa-Opa": opa,
        "Zillion": gun,
        "Floppy Disk": floppy,
        "Scope": scope,
        "Red ID Card": red
    })
    minimums = Counter({
        "ID Card": 0,
        "Bread": 0,
        "Opa-Opa": required_level - 1,
        "Zillion": guns_required,
        "Floppy Disk": floppy_req.value,
        "Scope": 0,
        "Red ID Card": 1
    })
    for key in minimums:
        item_counts[key] = max(minimums[key], item_counts[key])
    max_movables = 144 - sum(minimums.values())
    movables = item_counts - minimums
    while sum(movables.values()) > max_movables:
        # logging.warning("zillion options validate: player options item counts too high")
        total = sum(movables.values())
        scaler = max_movables / total
        for key in movables:
            movables[key] = int(movables[key] * scaler)
    item_counts = movables + minimums

    # now have required items, and <= 144

    # now fill remaining with empty
    total = sum(item_counts.values())
    diff = 144 - total
    if "Empty" not in item_counts:
        item_counts["Empty"] = 0
    item_counts["Empty"] += diff
    assert sum(item_counts.values()) == 144

    max_level = cast(ZillionMaxLevel, wo.max_level[p])
    max_level.value = max(required_level, max_level.value)

    opas_per_level = cast(ZillionOpasPerLevel, wo.opas_per_level[p])
    while (opas_per_level.value > 1) and (1 + item_counts["Opa-Opa"] // opas_per_level.value < max_level.value):
        # logging.warning(
        #     "zillion options validate: option opas_per_level incompatible with options max_level and opa_opa_count"
        # )
        opas_per_level.value -= 1

    # that should be all of the level requirements met

    name_capitalization = {
        "jj": "JJ",
        "apple": "Apple",
        "champ": "Champ",
    }

    start_char = cast(ZillionStartChar, wo.start_char[p])
    start_char_name = name_capitalization[start_char.current_key]
    assert start_char_name in chars
    start_char_name = cast(Chars, start_char_name)

    starting_cards = cast(ZillionStartingCards, wo.starting_cards[p])

    room_gen = cast(ZillionRoomGen, wo.room_gen[p])

    early_scope = cast(ZillionEarlyScope, wo.early_scope[p])
    if early_scope:
        world.early_items[p]["Scope"] = 1

    zz_item_counts = convert_item_counts(item_counts)
    zz_op = ZzOptions(
        zz_item_counts,
        cast(ZzVBLR, jump_option),
        cast(ZzVBLR, gun_option),
        opas_per_level.value,
        max_level.value,
        False,  # tutorial
        skill,
        start_char_name,
        floppy_req.value,
        wo.continues[p].value,
        wo.randomize_alarms[p].value,
        False,  # early scope is done with AP early_items API
        True,  # balance defense
        starting_cards.value,
        bool(room_gen.value)
    )
    zz_validate(zz_op)
    return zz_op, item_counts
