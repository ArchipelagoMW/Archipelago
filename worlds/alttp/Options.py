import typing

from Options import Choice, Range, Option, Toggle, DefaultOnToggle, DeathLink


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


class DungeonItem(Choice):
    value: int
    option_original_dungeon = 0
    option_own_dungeons = 1
    option_own_world = 2
    option_any_world = 3
    option_different_world = 4
    option_start_with = 6
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

class ShopPriceModifier(Range):
    """Percentage modifier for shuffled item prices in shops"""
    range_start = 0
    default = 100
    range_end = 400

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


class Progressive(Choice):
    displayname = "Progressive Items"
    option_off = 0
    option_grouped_random = 1
    option_on = 2
    alias_false = 0
    alias_true = 2
    default = 2

    def want_progressives(self, random):
        return random.choice([True, False]) if self.value == self.option_grouped_random else bool(self.value)


class Swordless(Toggle):
    """No swords. Curtains in Skull Woods and Agahnim\'s
    Tower are removed, Agahnim\'s Tower barrier can be
    destroyed with hammer. Misery Mire and Turtle Rock
    can be opened without a sword. Hammer damages Ganon.
    Ether and Bombos Tablet can be activated with Hammer
    (and Book)."""
    displayname = "Swordless"


class Retro(Toggle):
    """Zelda-1 like mode. You have to purchase a quiver to shoot arrows using rupees
    and there are randomly placed take-any caves that contain one Sword and choices of Heart Container/Blue Potion."""
    displayname = "Retro"


class RestrictBossItem(Toggle):
    """Don't place dungeon-native items on the dungeon's boss."""
    displayname = "Prevent Dungeon Item on Boss"


class Hints(Choice):
    """Vendors: King Zora and Bottle Merchant say what they're selling.
    On/Full: Put item and entrance placement hints on telepathic tiles and some NPCs, Full removes joke hints."""
    displayname = "Hints"
    option_off = 0
    option_vendors = 1
    option_on = 2
    option_full = 3
    default = 2
    alias_false = 0
    alias_true = 2


class EnemyShuffle(Toggle):
    """Randomize every enemy spawn.
    If mode is Standard, Hyrule Castle is left out (may result in visually wrong enemy sprites in that area.)"""
    displayname = "Enemy Shuffle"


class KillableThieves(Toggle):
    """Makes Thieves killable."""
    displayname = "Killable Thieves"


class BushShuffle(Toggle):
    """Randomize chance that a bush contains an enemy as well as which enemy may spawn."""
    displayname = "Bush Shuffle"


class TileShuffle(Toggle):
    """Randomize flying tiles floor patterns."""
    displayname = "Tile Shuffle"


class PotShuffle(Toggle):
    """Shuffle contents of pots within "supertiles" (item will still be nearby original placement)."""
    displayname = "Pot Shuffle"


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


class OWPalette(Palette):
    displayname = "Overworld Palette"


class UWPalette(Palette):
    displayname = "Underworld Palette"


class HUDPalette(Palette):
    displayname = "Menu Palette"


class SwordPalette(Palette):
    displayname = "Sword Palette"


class ShieldPalette(Palette):
    displayname = "Shield Palette"


class LinkPalette(Palette):
    displayname = "Link Palette"


class HeartBeep(Choice):
    displayname = "Heart Beep Rate"
    option_normal = 0
    option_double = 1
    option_half = 2
    option_quarter = 3
    option_off = 4
    alias_false = 4


class HeartColor(Choice):
    displayname = "Heart Color"
    option_red = 0
    option_blue = 1
    option_green = 2
    option_yellow = 3


class QuickSwap(DefaultOnToggle):
    displayname = "L/R Quickswapping"


class MenuSpeed(Choice):
    displayname = "Menu Speed"
    option_normal = 0
    option_instant = 1,
    option_double = 2
    option_triple = 3
    option_quadruple = 4
    option_half = 5


class Music(DefaultOnToggle):
    displayname = "Play music"


class ReduceFlashing(DefaultOnToggle):
    displayname = "Reduce Screen Flashes"


class TriforceHud(Choice):
    displayname = "Display Method for Triforce Hunt"
    option_normal = 0
    option_hide_goal = 1
    option_hide_required = 2
    option_hide_both = 3


class BeemizerRange(Range):
    value: int
    range_start = 0
    range_end = 100


class BeemizerTotalChance(BeemizerRange):
    """Percentage chance for each junk-fill item (rupees, bombs, arrows) to be
    replaced with either a bee swarm trap or a single bottle-filling bee."""
    default = 0
    displayname = "Beemizer Total Chance"


class BeemizerTrapChance(BeemizerRange):
    """Percentage chance for each replaced junk-fill item to be a bee swarm
    trap; all other replaced items are single bottle-filling bees."""
    default = 60
    displayname = "Beemizer Trap Chance"


alttp_options: typing.Dict[str, type(Option)] = {
    "crystals_needed_for_gt": CrystalsTower,
    "crystals_needed_for_ganon": CrystalsGanon,
    "bigkey_shuffle": bigkey_shuffle,
    "smallkey_shuffle": smallkey_shuffle,
    "compass_shuffle": compass_shuffle,
    "map_shuffle": map_shuffle,
    "progressive": Progressive,
    "swordless": Swordless,
    "retro": Retro,
    "hints": Hints,
    "restrict_dungeon_item_on_boss": RestrictBossItem,
    "pot_shuffle": PotShuffle,
    "enemy_shuffle": EnemyShuffle,
    "killable_thieves": KillableThieves,
    "bush_shuffle": BushShuffle,
    "shop_item_slots": ShopItemSlots,
    "shop_price_modifier": ShopPriceModifier,
    "tile_shuffle": TileShuffle,
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
    "glitch_boots": DefaultOnToggle,
    "beemizer_total_chance": BeemizerTotalChance,
    "beemizer_trap_chance": BeemizerTrapChance,
    "death_link": DeathLink

}
