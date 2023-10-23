import typing

from BaseClasses import MultiWorld
from Options import Choice, Range, Option, Toggle, DefaultOnToggle, DeathLink, StartInventoryPool, PlandoBosses


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


class OpenPyramid(Choice):
    """Determines whether the hole at the top of pyramid is open.
    Goal will open the pyramid if the goal requires you to kill Ganon, without needing to kill Agahnim 2.
    Auto is the same as goal except if Ganon's dropdown is in another location, the hole will be closed."""
    display_name = "Open Pyramid Hole"
    option_closed = 0
    option_open = 1
    option_goal = 2
    option_auto = 3
    default = option_goal

    alias_true = option_open
    alias_false = option_closed

    def to_bool(self, world: MultiWorld, player: int) -> bool:
        if self.value == self.option_goal:
            return world.goal[player] in {'crystals', 'ganontriforcehunt', 'localganontriforcehunt', 'ganonpedestal'}
        elif self.value == self.option_auto:
            return world.goal[player] in {'crystals', 'ganontriforcehunt', 'localganontriforcehunt', 'ganonpedestal'} \
            and (world.shuffle[player] in {'vanilla', 'dungeonssimple', 'dungeonsfull', 'dungeonscrossed'} or not
                 world.shuffle_ganon)
        elif self.value == self.option_open:
            return True
        else:
            return False


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

    @property
    def hints_useful(self):
        """Indicates if hints for this Item are useful in any way."""
        return self.value in {1, 2, 3, 4}


class bigkey_shuffle(DungeonItem):
    """Big Key Placement"""
    item_name_group = "Big Keys"
    display_name = "Big Key Shuffle"


class smallkey_shuffle(DungeonItem):
    """Small Key Placement"""
    option_universal = 5
    item_name_group = "Small Keys"
    display_name = "Small Key Shuffle"


class compass_shuffle(DungeonItem):
    """Compass Placement"""
    item_name_group = "Compasses"
    display_name = "Compass Shuffle"


class map_shuffle(DungeonItem):
    """Map Placement"""
    item_name_group = "Maps"
    display_name = "Map Shuffle"


class key_drop_shuffle(Toggle):
    """Shuffle keys found in pots and dropped from killed enemies."""
    display_name = "Key Drop Shuffle"
    default = False

class Crystals(Range):
    range_start = 0
    range_end = 7


class CrystalsTower(Crystals):
    """Number of crystals needed to open Ganon's Tower"""
    display_name = "Crystals for GT"
    default = 7


class CrystalsGanon(Crystals):
    """Number of crystals needed to damage Ganon"""
    display_name = "Crystals for Ganon"
    default = 7


class TriforcePieces(Range):
    default = 30
    range_start = 1
    range_end = 90


class ShopItemSlots(Range):
    """Number of slots in all shops available to have items from the multiworld"""
    display_name = "Available Shop Slots"
    range_start = 0
    range_end = 30


class ShopPriceModifier(Range):
    """Percentage modifier for shuffled item prices in shops"""
    display_name = "Shop Price Cost Percent"
    range_start = 0
    default = 100
    range_end = 400


class WorldState(Choice):
    option_standard = 1
    option_open = 0
    option_inverted = 2


class LTTPBosses(PlandoBosses):
    """Shuffles bosses around to different locations.
    Basic will shuffle all bosses except Ganon and Agahnim anywhere they can be placed.
    Full chooses 3 bosses at random to be placed twice instead of Lanmolas, Moldorm, and Helmasaur.
    Chaos allows any boss to appear any number of times.
    Singularity places a single boss in as many places as possible, and a second boss in any remaining locations.
    Supports plando placement."""
    display_name = "Boss Shuffle"
    option_none = 0
    option_basic = 1
    option_full = 2
    option_chaos = 3
    option_singularity = 4

    duplicate_bosses = True

    bosses = {
        "Armos Knights",
        "Lanmolas",
        "Moldorm",
        "Helmasaur King",
        "Arrghus",
        "Mothula",
        "Blind",
        "Kholdstare",
        "Vitreous",
        "Trinexx",
    }

    locations = {
        "Ganons Tower Top",
        "Tower of Hera",
        "Skull Woods",
        "Ganons Tower Middle",
        "Eastern Palace",
        "Desert Palace",
        "Palace of Darkness",
        "Swamp Palace",
        "Thieves Town",
        "Ice Palace",
        "Misery Mire",
        "Turtle Rock",
        "Ganons Tower Bottom"
    }

    @classmethod
    def can_place_boss(cls, boss: str, location: str) -> bool:
        from worlds.alttp.Bosses import can_place_boss
        level = ''
        words = location.split(" ")
        if words[-1] in ("top", "middle", "bottom"):
            level = words[-1]
            location = " ".join(words[:-1])
        location = location.title().replace("Of", "of")
        return can_place_boss(boss.title(), location, level)


class Enemies(Choice):
    option_vanilla = 0
    option_shuffled = 1
    option_chaos = 2


class Progressive(Choice):
    """How item types that have multiple tiers (armor, bows, gloves, shields, and swords) should be rewarded"""
    display_name = "Progressive Items"
    option_off = 0
    option_grouped_random = 1
    option_on = 2
    default = 2

    def want_progressives(self, random):
        return random.choice([True, False]) if self.value == self.option_grouped_random else bool(self.value)


class Swordless(Toggle):
    """No swords. Curtains in Skull Woods and Agahnim's
    Tower are removed, Agahnim's Tower barrier can be
    destroyed with hammer. Misery Mire and Turtle Rock
    can be opened without a sword. Hammer damages Ganon.
    Ether and Bombos Tablet can be activated with Hammer
    (and Book)."""
    display_name = "Swordless"


# Might be a decent idea to split "Bow" into its own option with choices of
# Defer to Progressive Option (default), Progressive, Non-Progressive, Bow + Silvers, Retro
class RetroBow(Toggle):
    """Zelda-1 like mode. You have to purchase a quiver to shoot arrows using rupees."""
    display_name = "Retro Bow"


class RetroCaves(Toggle):
    """Zelda-1 like mode. There are randomly placed take-any caves that contain one Sword and
    choices of Heart Container/Blue Potion."""
    display_name = "Retro Caves"


class RestrictBossItem(Toggle):
    """Don't place dungeon-native items on the dungeon's boss."""
    display_name = "Prevent Dungeon Item on Boss"


class Hints(Choice):
    """On/Full: Put item and entrance placement hints on telepathic tiles and some NPCs, Full removes joke hints."""
    display_name = "Hints"
    option_off = 0
    option_on = 2
    option_full = 3
    default = 2


class Scams(Choice):
    """If on, these Merchants will no longer tell you what they're selling."""
    display_name = "Scams"
    option_off = 0
    option_king_zora = 1
    option_bottle_merchant = 2
    option_all = 3

    @property
    def gives_king_zora_hint(self):
        return self.value in {0, 2}

    @property
    def gives_bottle_merchant_hint(self):
        return self.value in {0, 1}


class EnemyShuffle(Toggle):
    """Randomize every enemy spawn.
    If mode is Standard, Hyrule Castle is left out (may result in visually wrong enemy sprites in that area.)"""
    display_name = "Enemy Shuffle"


class KillableThieves(Toggle):
    """Makes Thieves killable."""
    display_name = "Killable Thieves"


class BushShuffle(Toggle):
    """Randomize chance that a bush contains an enemy as well as which enemy may spawn."""
    display_name = "Bush Shuffle"


class TileShuffle(Toggle):
    """Randomize flying tiles floor patterns."""
    display_name = "Tile Shuffle"


class PotShuffle(Toggle):
    """Shuffle contents of pots within "supertiles" (item will still be nearby original placement)."""
    display_name = "Pot Shuffle"


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
    """The type of palette shuffle to use for the overworld"""
    display_name = "Overworld Palette"


class UWPalette(Palette):
    """The type of palette shuffle to use for the underworld (caves, dungeons, etc.)"""
    display_name = "Underworld Palette"


class HUDPalette(Palette):
    """The type of palette shuffle to use for the HUD"""
    display_name = "Menu Palette"


class SwordPalette(Palette):
    """The type of palette shuffle to use for the sword"""
    display_name = "Sword Palette"


class ShieldPalette(Palette):
    """The type of palette shuffle to use for the shield"""
    display_name = "Shield Palette"


# class LinkPalette(Palette):
#     display_name = "Link Palette"


class HeartBeep(Choice):
    """How quickly the heart beep sound effect will play"""
    display_name = "Heart Beep Rate"
    option_normal = 0
    option_double = 1
    option_half = 2
    option_quarter = 3
    option_off = 4


class HeartColor(Choice):
    """The color of hearts in the HUD"""
    display_name = "Heart Color"
    option_red = 0
    option_blue = 1
    option_green = 2
    option_yellow = 3


class QuickSwap(DefaultOnToggle):
    """Allows you to quickly swap items while playing with L/R"""
    display_name = "L/R Quickswapping"


class MenuSpeed(Choice):
    """How quickly the menu appears/disappears"""
    display_name = "Menu Speed"
    option_normal = 0
    option_instant = 1,
    option_double = 2
    option_triple = 3
    option_quadruple = 4
    option_half = 5


class Music(DefaultOnToggle):
    """Whether background music will play in game"""
    display_name = "Play music"


class ReduceFlashing(DefaultOnToggle):
    """Reduces flashing for certain scenes such as the Misery Mire and Ganon's Tower opening cutscenes"""
    display_name = "Reduce Screen Flashes"


class TriforceHud(Choice):
    """When and how the triforce hunt HUD should display"""
    display_name = "Display Method for Triforce Hunt"
    option_normal = 0
    option_hide_goal = 1
    option_hide_required = 2
    option_hide_both = 3


class GlitchBoots(DefaultOnToggle):
    """If this is enabled, the player will start with Pegasus Boots when playing with overworld glitches or harder logic."""
    display_name = "Glitched Starting Boots"


class BeemizerRange(Range):
    value: int
    range_start = 0
    range_end = 100


class BeemizerTotalChance(BeemizerRange):
    """Percentage chance for each junk-fill item (rupees, bombs, arrows) to be
    replaced with either a bee swarm trap or a single bottle-filling bee."""
    default = 0
    display_name = "Beemizer Total Chance"


class BeemizerTrapChance(BeemizerRange):
    """Percentage chance for each replaced junk-fill item to be a bee swarm
    trap; all other replaced items are single bottle-filling bees."""
    default = 60
    display_name = "Beemizer Trap Chance"


class AllowCollect(Toggle):
    """Allows for !collect / co-op to auto-open chests containing items for other players.
    Off by default, because it currently crashes on real hardware."""
    display_name = "Allow Collection of checks for other players"


alttp_options: typing.Dict[str, type(Option)] = {
    "crystals_needed_for_gt": CrystalsTower,
    "crystals_needed_for_ganon": CrystalsGanon,
    "open_pyramid": OpenPyramid,
    "bigkey_shuffle": bigkey_shuffle,
    "smallkey_shuffle": smallkey_shuffle,
    "key_drop_shuffle": key_drop_shuffle,
    "compass_shuffle": compass_shuffle,
    "map_shuffle": map_shuffle,
    "progressive": Progressive,
    "swordless": Swordless,
    "retro_bow": RetroBow,
    "retro_caves": RetroCaves,
    "hints": Hints,
    "scams": Scams,
    "restrict_dungeon_item_on_boss": RestrictBossItem,
    "boss_shuffle": LTTPBosses,
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
    # "link_palettes": LinkPalette,
    "heartbeep": HeartBeep,
    "heartcolor": HeartColor,
    "quickswap": QuickSwap,
    "menuspeed": MenuSpeed,
    "music": Music,
    "reduceflashing": ReduceFlashing,
    "triforcehud": TriforceHud,
    "glitch_boots": GlitchBoots,
    "beemizer_total_chance": BeemizerTotalChance,
    "beemizer_trap_chance": BeemizerTrapChance,
    "death_link": DeathLink,
    "allow_collect": AllowCollect,
    "start_inventory_from_pool": StartInventoryPool,
}
