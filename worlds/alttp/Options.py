import typing

from Options import Choice, Range, Option, Toggle, DefaultOnToggle, DeathLink


class Logic(Choice):
    """Determine the logic used to reach locations."""
    option_no_glitches = 0
    option_minor_glitches = 1
    option_overworld_glitches = 2
    option_hybrid_major_glitches = 3
    option_no_logic = 4
    alias_owg = 2
    alias_hmg = 3


class DarkRoomLogic(Choice):
    """Item required to traverse unlit dark rooms."""
    option_lamp = 0
    option_torches = 1
    option_none = 2


class GlitchBoots(DefaultOnToggle):
    """Start with Pegasus Boots if any glitches that use them are required."""


class BossItem(Toggle):
    """Unshuffled dungeon items won't be place on the dungeon boss."""


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


class BigKey(DungeonItem):
    """Big Key Placement"""
    item_name_group = "Big Keys"
    display_name = "Big Key Shuffle"


class SmallKey(DungeonItem):
    """Small Key Placement"""
    option_universal = 5
    item_name_group = "Small Keys"
    display_name = "Small Key Shuffle"


class Compass(DungeonItem):
    """Compass Placement"""
    item_name_group = "Compasses"
    display_name = "Compass Shuffle"


class Map(DungeonItem):
    """Map Placement"""
    item_name_group = "Maps"
    display_name = "Map Shuffle"


class DungeonCounters(Choice):
    """Whether to display a counter for locations checked in a dungeon.
    Shuffled compass will only display counter if you have the compass and the compass is shuffled."""
    option_compass_pickup = 0
    option_on = 1
    option_shuffled_compass = 2
    option_off = 3
    alias_true = 1
    alias_false = 3


class Progressives(Choice):
    """Enable or disable swords, shields, bows, gloves, and boomerangs being progressive.
    Grouped random decides randomly per group of progressive items."""
    option_all = 0
    option_none = 1
    option_grouped_random = 2
    alias_on = 0
    alias_true = 0
    alias_off = 1
    alias_false = 1

    def want_progressive(self, random):
        return random.choice([True, False]) if self.value == self.option_grouped_random else bool(self.value)


class EntranceShuffle(Choice):
    """Type of entrance shuffle to use.
    Dungeons simple shuffles dungeon locations around but keep the dungeon grouped together.
    Dungeons full can have any dungeon entrance lead to any dungeon interior but each dungeon will be kept to one world state.
    Dungeons crossed can have any dungeon entrance lead to any other and allow cross-world traversal through dungeons.
    Simple groups entrances together before randomizing them. Vanilla connectors will always be connectors, dungeons will be dungeons etc.
    Restricted shuffles like simple except all non-dungeon entrances are shuffled amongst each other.
    Full is like restricted except all dungeons are shuffled in the pool as well.
    Crossed shuffles all entrances in the game and allows for connectors to lead between world states.
    Insanity works like crossed except entrances are decoupled from each other. The chain stops at single entrance caves."""
    option_none = 0
    option_dungeons_simple = 1
    option_dungeons_full = 2
    option_dungeons_crossed = 3
    option_simple = 4
    option_restricted = 5
    option_full = 6
    option_crossed = 7
    option_insanity = 8
    alias_off = 0
    alias_false = 0


class Goal(Choice):
    """Objective to finish the game."""
    option_kill_ganon = 0
    option_kill_ganon_and_gt_agahnim = 1
    option_all_bosses = 2
    option_pedestal = 3
    option_pedestal_ganon = 4
    option_triforce_hunt = 5
    option_triforce_hunt_ganon = 6
    option_icerod_hunt = 7


class Pyramid(Choice):
    """Determines whether the pyramid hole will be open."""
    option_goal = 0
    option_auto = 1
    option_open = 2
    option_closed = 3
    alias_yes = 2
    alias_true = 2
    alias_no = 3
    alias_false = 3


class TriforceMode(Choice):
    """Determine how to calculate extra available triforce pieces."""
    option_available = 0
    option_extra = 1
    option_percentage = 2


class TriforcePieces(Range):
    default = 20
    range_start = 1
    range_end = 90


class TriforceExtra(TriforcePieces):
    """Number of extra triforce pieces available to be collected."""
    default = 10
    range_end = 20


class TriforcePercent(Range):
    """Percentage of triforce pieces required that will be added as extras."""
    range_end = 100


class TriforceRequired(TriforcePieces):
    """How many triforce pieces are required for your goal."""


class Crystals(Range):
    range_end = 7
    default = 7


class CrystalsTower(Crystals):
    """Number of Crystals required to enter Ganon's Tower."""


class CrystalsGanon(Crystals):
    """Number of Crystals required to defeat Ganon."""


class WorldState(Choice):
    """Starting world state for the game.
    Standard starts with the rain sequence and uncle will have a guaranteed weapon.
    Open starts with you at Link's House in the Light world and free to go anywhere.
    Inverted begins with Link's House in the dark world and Moon Pearl is required for the Light World."""
    option_standard = 1
    option_open = 0
    option_inverted = 2


class Retro(Toggle):
    """Zelda-1 like mode. You have to purchase a quiver to shoot arrows using rupees
    and there are randomly placed take-any caves that contain one Sword and choices of Heart Container/Blue Potion."""


class Hints(Choice):
    """Vendors: King Zora and Bottle Merchant say what they're selling.
    On/Full: Put item and entrance placement hints on telepathic tiles and some NPCs, Full removes joke hints."""
    display_name = "Hints"
    option_off = 0
    option_vendors = 1
    option_on = 2
    option_full = 3
    default = 2
    alias_false = 0
    alias_true = 2


class Swordless(Toggle):
    """Swords get replaced with rupees and some gameplay accommodations are made.
    Curtains will always be open and Ganon can be harmed with silver arrows and a hammer."""


class ItemTypes(Choice):
    option_easy = 1
    option_normal = 0
    option_hard = 2
    option_expert = 3


class ItemPool(ItemTypes):
    """Availability of certain upgrades in the pool to make the game easier/harder.
    Easy doubles the amount of available upgrades/progressives.
    Normal is unchanged from vanilla.
    Hard allows you a max of 14 hearts, blue mail, tempered sword, red shield, and unable to use silvers outside Ganon.
    Expert allows you a max of 8 hearts, green mail, master sword, fighter shield, and unable to use silvers outside Ganon."""


class ItemFunctionality(ItemTypes):
    """Changes the functionality of certain items.
    Easy allows Hammer to damage ganon, collect tablets with hammer + book and no sword required to use medallions.
    Normal is vanilla functionality.
    Hard reduces how helpful items are (potions less effective, can't catch fairies, cape uses double magic,
    byrna does not grant invulnerability, boomerangs do not stun, no silvers outside Ganon.)
    Expert reduces helpful items even more (hard plus boomerangs and hookshot do not stun.)"""


class TileShuffle(Toggle):
    """Randomize flying tiles floor patterns."""
    display_name = "Tile Shuffle"


class Medallions(Choice):
    option_ether = 0
    option_bombos = 1
    option_quake = 2
    default = 'random'


class MireMedallions(Medallions):
    """Required medallion to open Misery Mire Entrance."""


class TurtleMedallions(Medallions):
    """Required medallion to open Turtle Rock Entrance."""


class Bosses(Choice):
    """Shuffles bosses in dungeons.
    Simple will take the existing bosses and move them to random locations.
    Full allows any boss anywhere they can exist but only 3 bosses may appear twice maximum.
    Chaos allows any boss anywhere they can exist.
    Singularity picks a boss and puts it everywhere it works, if any spots remain a second boss goes in those locations."""
    option_vanilla = 0
    option_simple = 1
    option_full = 2
    option_chaos = 3
    option_singularity = 4


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


class EnemyDamage(Choice):
    """Randomize damage that enemies deal.
    Shuffle allows enemies to deal 0-4 hearts and armor always helps.
    Chaos allows enemies to deal 0-8 hearts and armor reshuffles the damage they deal."""
    option_vanilla = 0
    option_shuffled = 1
    option_chaos = 2


class EnemyHealth(ItemTypes):
    """Reduces or increases the amount of HP enemies have."""


class PotShuffle(Toggle):
    """Shuffle contents of pots within "supertiles" (item will still be nearby original placement)."""
    display_name = "Pot Shuffle"


class BeemizerRange(Range):
    range_end = 100


class BeemizerTotalChance(BeemizerRange):
    """Percentage chance for each junk-fill item (rupees, bombs, arrows) to be
    replaced with either a bee swarm trap or a single bottle-filling bee."""
    display_name = "Beemizer Total Chance"


class BeemizerTrapChance(BeemizerRange):
    """Percentage chance for each replaced junk-fill item to be a bee swarm
    trap; all other replaced items are single bottle-filling bees."""
    default = 60
    display_name = "Beemizer Trap Chance"


class ShopShuffle(Toggle):
    """Generates new inventories for shops and can allow other items based on shop item slots available."""


class ShopItemSlots(Range):
    """Maximum amount of shop slots to be filled with regular items."""
    range_end = 30


class ShopPriceModifier(Range):
    """Percentage modifier for shuffled item prices in shops"""
    default = 100
    range_end = 400


class CapacityUpgrades(Toggle):
    """Shuffles capacity upgrades for bombs and arrows into the item pool."""


class WitchHut(Toggle):
    """Allows witch hut to be a valid shop for shop shuffle."""


class PrizeDrops(Choice):
    """Shuffles various prize packs giving different drops.
    General shuffles the enemy, tree pull, and digging prize packs.
    Bonk shuffles only the prize packs from 'bonking' objects such as trees."""
    option_none = 1
    option_general = 0
    option_bonk = 2
    option_all = 3


class Timer(Choice):
    """Adds a timer to the game with different effects.
    Timed starts the timer counting up from 0. Green and blue subtract times whereas red adds time.
    Timed ohko starts the timer at ten minutes counting down.
    OHKO is permanent one hit KO.
    Display starts a timer counting up from zero. Has no effect on gameplay or item pool."""
    option_none = 0
    option_timed = 1
    option_timed_ohko = 2
    option_ohko = 3
    option_display = 4


class CountdownStart(Range):
    """For Timed OHKO mode determines the starting time on the timer in minutes."""
    range_end = 60
    default = 10


class Clock(Range):
    """For timed modes, amount of time in minutes to gain or lose on pickup."""


class RedClock(Clock):
    range_start = -4
    range_end = 1
    default = -2


class BlueClock(Clock):
    range_start = 1
    range_end = 3
    default = 2


class GreenClock(Clock):
    range_start = 4
    range_end = 15
    default = 4


class Sprite(Option):
    option_random_sprite = 0
    option_random_on_hit = 1
    option_random_on_enter = 2
    option_random_on_exit = 3
    option_random_on_slash = 4
    option_random_on_item = 5
    option_random_on_bonk = 6
    option_random_on_all = 7
    option_Link = 8
    default = 8


class Music(DefaultOnToggle):
    """Allows you to disable music playback."""


class QuickSwap(DefaultOnToggle):
    """Enables switching items by pressing the L and R shoulder buttons."""


class TriforceHud(Choice):
    """Disable Triforce HUD until collecting a piece or speaking to Murahdala."""
    option_show = 1
    option_hide_goal = 0
    option_hide_required = 2
    option_hide_both = 3


class ReduceFlashing(DefaultOnToggle):
    """Reduce instances of flashing such as lightning, weather, ether, etc."""


class MenuSpeed(Choice):
    """Controls how fast the item menu opens and closes."""
    option_normal = 0
    option_instant = 1
    option_double = 2
    option_triple = 3
    option_quadruple = 4
    option_half = 5


class HeartColor(Choice):
    """Controls the color of your health hearts."""
    option_red = 0
    option_blue = 1
    option_green = 2
    option_yellow = 3


class HeartBeep(Choice):
    """Controls the frequency of low-health beeping."""
    option_double = 1
    option_normal = 0
    option_half = 2
    option_quarter = 3
    option_off = 4
    alias_false = 4


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
    display_name = "Overworld Palette"


class UWPalette(Palette):
    display_name = "Underworld Palette"


class HUDPalette(Palette):
    display_name = "Menu Palette"


class SwordPalette(Palette):
    display_name = "Sword Palette"


class ShieldPalette(Palette):
    display_name = "Shield Palette"


class LinkPalette(Palette):
    display_name = "Link Palette"


class HeartBeep(Choice):
    display_name = "Heart Beep Rate"
    option_normal = 0
    option_double = 1
    option_half = 2
    option_quarter = 3
    option_off = 4
    alias_false = 4


class HeartColor(Choice):
    display_name = "Heart Color"
    option_red = 0
    option_blue = 1
    option_green = 2
    option_yellow = 3


class QuickSwap(DefaultOnToggle):
    display_name = "L/R Quickswapping"


class MenuSpeed(Choice):
    display_name = "Menu Speed"
    option_normal = 0
    option_instant = 1,
    option_double = 2
    option_triple = 3
    option_quadruple = 4
    option_half = 5


class Music(DefaultOnToggle):
    display_name = "Play music"


class ReduceFlashing(DefaultOnToggle):
    display_name = "Reduce Screen Flashes"


class TriforceHud(Choice):
    display_name = "Display Method for Triforce Hunt"
    option_normal = 0
    option_hide_goal = 1
    option_hide_required = 2
    option_hide_both = 3


class AllowCollect(Toggle):
    """Allows for !collect / co-op to auto-open chests containing items for other players.
    Off by default, because it currently crashes on real hardware."""
    display_name = "Allow Collection of checks for other players"


alttp_options: typing.Dict[str, type(Option)] = {
    "glitches_required": Logic,
    "dark_room_logic": DarkRoomLogic,
    "glitch_boots": GlitchBoots,
    
    "restrict_boss_item": BossItem,
    "bigkey_shuffle": BigKey,
    "smallkey_shuffle": SmallKey,
    "compass_shuffle": Compass,
    "map_shuffle": Map,
    "dungeon_counters": DungeonCounters,
    
    "progressive_items": Progressives,
    "entrance_shuffle": EntranceShuffle,
    
    "goals": Goal,
    "open_pyramid": Pyramid,
    "triforce_pieces_mode": TriforceMode,
    "triforce_pieces_available": TriforcePieces,
    "triforce_pieces_extra": TriforceExtra,
    "triforce_pieces_percentage": TriforcePercent,
    "triforce_pieces_required": TriforceRequired,
    "gt_crystals": CrystalsTower,
    "ganon_crystals": CrystalsGanon,
    
    "mode": WorldState,
    "retro": Retro,
    "hints": Hints,
    "swords": Swordless,
    "item_pool": ItemPool,
    "item_functionality": ItemFunctionality,
    "tile_shuffle": TileShuffle,
    "misery_mire_medallion": MireMedallions,
    "turtle_rock_medallion": TurtleMedallions,
    
    "boss_shuffle": Bosses,
    "enemy_shuffle": EnemyShuffle,
    "killable_thieves": KillableThieves,
    "bush_shuffle": BushShuffle,
    "enemy_damage": EnemyDamage,
    "enemy_health": EnemyHealth,
    "pot_shuffle": PotShuffle,
    
    "beemizer_total_chance": BeemizerTotalChance,
    "beemizer_trap_chance": BeemizerTrapChance,

    "shop_shuffle": ShopShuffle,
    "shop_item_slots": ShopItemSlots,
    "shop_price_modifier": ShopPriceModifier,
    "shuffle_shop_inventories"
    "capacity_upgrades": CapacityUpgrades,
    "shuffle_witch_hut": WitchHut,
    "shuffle_prizes": PrizeDrops,
    
    "timer": Timer,
    "countdown_start_time": CountdownStart,
    "red_clock_time": RedClock,
    "blue_clock_time": BlueClock,
    "green_clock_time": GreenClock,
    
    "sprite": Sprite,
    "music": Music,
    "quick_swap": QuickSwap,
    "triforce_hud": TriforceHud,
    "reduce_flashing": ReduceFlashing,
    "menu_speed": MenuSpeed,
    "heart_color": HeartColor,
    "heart_beep": HeartBeep,

    "ow_palettes": OWPalette,
    "uw_palettes": UWPalette,
    "hud_palettes": HUDPalette,
    "sword_palettes": SwordPalette,
    "shield_palettes": ShieldPalette
}
