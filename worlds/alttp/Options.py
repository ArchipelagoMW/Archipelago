import typing

from Options import Choice, Range, Option


class Logic(Choice):
    option_no_glitches = 0
    option_minor_glitches = 1
    option_overworld_glitches = 2
    option_hybrid_major_glitches = 3
    option_no_logic = 4
    alias_owg = 2
    alias_hmg = 3


class Objective(Choice):
    option_crystals = 0
    # option_pendants = 1
    option_triforce_pieces = 2
    option_pedestal = 3
    option_bingo = 4


class Goal(Choice):
    option_kill_ganon = 0
    option_kill_ganon_and_gt_agahnim = 1
    option_hand_in = 2


class Crystals(Range):
    range_start = 0
    range_end = 7


class CrystalsTower(Crystals):
    default = 7


class CrystalsGanon(Crystals):
    default = 7


class TriforcePieces(Range):
    default = 30
    range_start = 1
    range_end = 90


class ShopItemSlots(Range):
    range_start = 0
    range_end = 30


class WorldState(Choice):
    option_standard = 1
    option_open = 0
    option_inverted = 2


class Bosses(Choice):
    option_vanilla = 0
    option_simple = 1
    option_full = 2
    option_chaos = 3
    option_singularity = 4


class Enemies(Choice):
    option_vanilla = 0
    option_shuffled = 1
    option_chaos = 2

alttp_options: typing.Dict[str, type(Option)] = {
    "crystals_needed_for_gt": CrystalsTower,
    "crystals_needed_for_ganon": CrystalsGanon,
    "shop_item_slots": ShopItemSlots,
}