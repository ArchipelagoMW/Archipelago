import typing
import random

from Options import Choice, Range, Option, Toggle, DefaultOnToggle


class Logic(Choice):
    """Logic Rules used for item access."""
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
    """Goal to win."""
    option_kill_ganon = 0
    option_kill_ganon_and_gt_agahnim = 1
    option_hand_in = 2


class DungeonItem(Choice):
    value: int
    option_original_dungeon = 0
    option_own_dungeons = 1
    option_own_world = 2
    option_any_world = 3
    option_different_world = 4
    alias_true = 3
    alias_false = 0

    @property
    def in_dungeon(self):
        return self.value in {0, 1}


class bigkey_shuffle(DungeonItem):
    """Big Key Placement"""
    item_name_group = "Big Keys"
    displayname = "Big Key Shuffle"


class smallkey_shuffle(DungeonItem):
    """Small Key Placement"""
    option_universal = 5
    item_name_group = "Small Keys"
    displayname = "Small Key Shuffle"


class compass_shuffle(DungeonItem):
    """Compass Placement"""
    item_name_group = "Compasses"
    displayname = "Compass Shuffle"


class map_shuffle(DungeonItem):
    """Map Placement"""
    item_name_group = "Maps"
    displayname = "Map Shuffle"


class Crystals(Range):
    range_start = 0
    range_end = 7


class CrystalsTower(Crystals):
    """Number of crystals required to open Ganon's Tower."""
    default = 7


class CrystalsGanon(Crystals):
    """Number of crystals required to harm Ganon."""
    default = 7


class TriforcePieces(Range):
    """Number of triforce pieces required to complete the goal."""
    default = 30
    range_start = 1
    range_end = 90


class ShopItemSlots(Range):
    """Amount of items placed in shops."""
    range_start = 0
    range_end = 30


class WorldState(Choice):
    """Starting world state. Standard starts with the Princess Escape sequence.
    Open starts with full world access.
    Inverted starts with Link's house in the dark world and some other
    locations moved around for this altered world."""
    option_standard = 1
    option_open = 0
    option_inverted = 2


class Bosses(Choice):
    """Bosses get shuffled around. Simple will keep the number of appearances of each boss vanilla
    but shuffle them around. Therefor there will be two sets of Armos Knights, Lanmolas' and Moldorm.
    Full does the same as Simple except the 3 duplicated bosses are chosen randomly.
    Chaos chooses bosses entirely at random. Singularity will choose a random boss and place it in every
    location it can. If there are locations it can't put it in a second boss will be chosen for those locations."""
    option_vanilla = 0
    option_simple = 1
    option_full = 2
    option_chaos = 3
    option_singularity = 4


class Enemies(Choice):
    """Enemies get shuffled around the game."""
    option_vanilla = 0
    option_shuffled = 1
    option_chaos = 2


class Progressive(Choice):
    """Determines if items that are usually progressive stay progressive.
    For random, each category is grouped together then turned either progressive on or off.
    The groups are swords, gloves, boomerangs, shields, and mail."""
    displayname = "Progressive Items"
    option_off = 0
    option_grouped_random = 1
    option_on = 2
    alias_false = 0
    alias_true = 2
    default = 2
    alias_random = 1

    def want_progressives(self, random):
        return random.choice([True, False]) if self.value == self.option_grouped_random else bool(self.value)


class Palette(Choice):
    option_default = 0
    option_good = 1
    option_blackout = 2
    option_puke = 3
    option_classic = 4
    option_grayscale = 5
    option_negative = 6
    option_dizzy = 7
    option_sick = 8
    alias_random = 1


class OWPalette(Palette):
    """The Palette definition for the Overworld."""
    displayname = "Overworld Palette"


class UWPalette(Palette):
    """The Palette definition for the Underworld."""
    displayname = "Underworld Palette"


class HUDPalette(Palette):
    """The Palette definition for the HUD."""
    displayname = "Menu Palette"


class SwordPalette(Palette):
    """The Palette definition for Link's Sword."""
    displayname = "Sword Palette"


class ShieldPalette(Palette):
    """The Palette definition for Link's Shield."""
    displayname = "Shield Palette"


class LinkPalette(Palette):
    """The Palette definition for Link."""
    displayname = "Link Palette"


class HeartBeep(Choice):
    """How fast or slow the heart beep at low health is."""
    displayname = "Heart Beep Rate"
    option_normal = 0
    option_double = 1
    option_half = 2
    option_quarter = 3
    option_off = 4
    alias_false = 4


class HeartColor(Choice):
    """The color of your hearts in the HUD."""
    displayname = "Heart Color"
    option_red = 0
    option_blue = 1
    option_green = 2
    option_yellow = 3

    @classmethod
    def from_text(cls, text: str) -> Choice:
        # remove when this becomes a base Choice feature
        if text == "random":
            return cls(random.randint(0, 3))
        return super(HeartColor, cls).from_text(text)


class QuickSwap(DefaultOnToggle):
    """Enable/Disable Quickswapping items with the L/R buttons."""
    displayname = "L/R Quickswapping"


class MenuSpeed(Choice):
    """How fast relative to vanilla the menu screen appears and disappears."""
    displayname = "Menu Speed"
    option_normal = 0
    option_instant = 1,
    option_double = 2
    option_triple = 3
    option_quadruple = 4
    option_half = 5


class Music(DefaultOnToggle):
    """Enable/Disable whether music plays in the game."""
    displayname = "Play music"


class ReduceFlashing(DefaultOnToggle):
    """Reduces flashing of certain scenes."""
    displayname = "Reduce Screen Flashes"


class TriforceHud(Choice):
    """Decides whether the HUD for Triforce hunt goal should appear."""
    displayname = "Display Method for Triforce Hunt"
    option_normal = 0
    option_hide_goal = 1
    option_hide_required = 2
    option_hide_both = 3


alttp_options: typing.Dict[str, type(Option)] = {
    "crystals_needed_for_gt": CrystalsTower,
    "crystals_needed_for_ganon": CrystalsGanon,
    "bigkey_shuffle": bigkey_shuffle,
    "smallkey_shuffle": smallkey_shuffle,
    "compass_shuffle": compass_shuffle,
    "map_shuffle": map_shuffle,
    "progressive": Progressive,
    "shop_item_slots": ShopItemSlots,
    "ow_palettes": OWPalette,
    "uw_palettes": UWPalette,
    "hud_palettes": HUDPalette,
    "sword_palettes": SwordPalette,
    "shield_palettes": ShieldPalette,
    "link_palettes": LinkPalette,
    "heartbeep": HeartBeep,
    "heartcolor": HeartColor,
    "quickswap": QuickSwap,
    "menuspeed": MenuSpeed,
    "music": Music,
    "reduceflashing": ReduceFlashing,
    "triforcehud": TriforceHud,
    "glitch_boots": DefaultOnToggle

}
