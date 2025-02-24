from collections import Counter
from dataclasses import dataclass
from typing import ClassVar, Literal, TypeGuard

from Options import Choice, DefaultOnToggle, NamedRange, OptionGroup, PerGameCommonOptions, Range, Removed, Toggle

from zilliandomizer.options import (
    Options as ZzOptions, char_to_gun, char_to_jump, ID,
    VBLR as ZzVBLR, Chars, ItemCounts as ZzItemCounts
)
from zilliandomizer.options.parsing import validate as zz_validate


class ZillionContinues(NamedRange):
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

    def to_zz_vblr(self) -> ZzVBLR:
        def is_vblr(o: str) -> TypeGuard[ZzVBLR]:
            """
            This function is because mypy doesn't support narrowing with `in`,
            https://github.com/python/mypy/issues/12535
            so this is the only way I see to get type narrowing to `Literal`.
            """
            return o in ("vanilla", "balanced", "low", "restrictive")

        key = self.current_key
        assert is_vblr(key), f"{key=}"
        return key


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

    _name_capitalization: ClassVar[dict[int, Chars]] = {
        option_jj: "JJ",
        option_apple: "Apple",
        option_champ: "Champ",
    }

    def get_char(self) -> Chars:
        return ZillionStartChar._name_capitalization[self.value]


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
    """
    the difficulty level of the game

    higher skill:
    - can require more precise platforming movement
    - lowers your defense
    - gives you less time to escape at the end
    """
    range_start = 0
    range_end = 5
    default = 2
    display_name = "skill"


class ZillionStartingCards(NamedRange):
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


class ZillionMapGen(Choice):
    """
    - none: vanilla map
    - rooms: random terrain inside rooms, but path through base is vanilla
    - full: random path through base
    """
    display_name = "map generation"
    option_none = 0
    option_rooms = 1
    option_full = 2
    default = 0

    def zz_value(self) -> Literal["none", "rooms", "full"]:
        if self.value == ZillionMapGen.option_none:
            return "none"
        if self.value == ZillionMapGen.option_rooms:
            return "rooms"
        assert self.value == ZillionMapGen.option_full
        return "full"


@dataclass
class ZillionOptions(PerGameCommonOptions):
    continues: ZillionContinues
    floppy_req: ZillionFloppyReq
    gun_levels: ZillionGunLevels
    jump_levels: ZillionJumpLevels
    randomize_alarms: ZillionRandomizeAlarms
    max_level: ZillionMaxLevel
    start_char: ZillionStartChar
    opas_per_level: ZillionOpasPerLevel
    id_card_count: ZillionIDCardCount
    bread_count: ZillionBreadCount
    opa_opa_count: ZillionOpaOpaCount
    zillion_count: ZillionZillionCount
    floppy_disk_count: ZillionFloppyDiskCount
    scope_count: ZillionScopeCount
    red_id_card_count: ZillionRedIDCardCount
    early_scope: ZillionEarlyScope
    skill: ZillionSkill
    starting_cards: ZillionStartingCards
    map_gen: ZillionMapGen

    room_gen: Removed


z_option_groups = [
    OptionGroup("item counts", [
        ZillionIDCardCount, ZillionBreadCount, ZillionOpaOpaCount, ZillionZillionCount,
        ZillionFloppyDiskCount, ZillionScopeCount, ZillionRedIDCardCount
    ])
]


def convert_item_counts(ic: Counter[str]) -> ZzItemCounts:
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


def validate(options: ZillionOptions) -> tuple[ZzOptions, Counter[str]]:
    """
    adjusts options to make game completion possible

    `options` parameter is ZillionOptions object that was put on my world by the core
    """

    skill = options.skill.value

    jump_option = options.jump_levels.to_zz_vblr()
    required_level = char_to_jump["Apple"][jump_option].index(3) + 1
    if skill == 0:
        # because of hp logic on final boss
        required_level = 8

    gun_option = options.gun_levels.to_zz_vblr()
    guns_required = char_to_gun["Champ"][gun_option].index(3)

    floppy_req = options.floppy_req

    item_counts = Counter({
        "ID Card": options.id_card_count,
        "Bread": options.bread_count,
        "Opa-Opa": options.opa_opa_count,
        "Zillion": options.zillion_count,
        "Floppy Disk": options.floppy_disk_count,
        "Scope": options.scope_count,
        "Red ID Card": options.red_id_card_count
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

    max_level = options.max_level
    max_level.value = max(required_level, max_level.value)

    opas_per_level = options.opas_per_level
    while (opas_per_level.value > 1) and (1 + item_counts["Opa-Opa"] // opas_per_level.value < max_level.value):
        # logging.warning(
        #     "zillion options validate: option opas_per_level incompatible with options max_level and opa_opa_count"
        # )
        opas_per_level.value -= 1

    # that should be all of the level requirements met

    starting_cards = options.starting_cards

    map_gen = options.map_gen.zz_value()

    zz_item_counts = convert_item_counts(item_counts)
    zz_op = ZzOptions(
        zz_item_counts,
        jump_option,
        gun_option,
        opas_per_level.value,
        max_level.value,
        False,  # tutorial
        skill,
        options.start_char.get_char(),
        floppy_req.value,
        options.continues.value,
        bool(options.randomize_alarms.value),
        bool(options.early_scope.value),
        True,  # balance defense
        starting_cards.value,
        map_gen
    )
    zz_validate(zz_op)
    return zz_op, item_counts
