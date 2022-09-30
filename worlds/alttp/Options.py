import typing
from functools import lru_cache

from BaseClasses import MultiWorld
from Options import Choice, Range, Option, Toggle, DefaultOnToggle, DeathLink, TextChoice, OptionList


class Logic(Choice):
    """Determine the level of glitches expected for the player to use to reach locations."""
    display_name = "Glitch Logic"
    option_no_glitches = 0
    option_minor_glitches = 1
    option_overworld_glitches = 2
    option_hybrid_major_glitches = 3
    option_no_logic = 4
    alias_none = option_no_glitches
    alias_owg = option_overworld_glitches
    alias_hmg = option_hybrid_major_glitches


class DarkRoomLogic(Choice):
    """Requirement to traverse unlit dark rooms."""
    display_name = "Dark Room Logic"
    option_lamp = 0
    option_torches = 1
    option_none = 2


class GlitchBoots(DefaultOnToggle):
    """Start with Pegasus Boots if any glitches that use them are available."""
    display_name = "Glitched Starting Boots"


class Goal(Choice):
    """Goal required to finish your game.
    Ganon and tower requires climbing Ganon's tower and defeating Agahnim 2, and then Ganon.
    Ganon requires collecting enough crystals to get to and defeat Ganon.
    All Bosses requires defeating each end dungeon boss as well as both Agahnim fights, and finally Ganon.
    Pedestal requires collecting the three pendants and pulling the master sword pedestal.
    Pedestal Ganon requires pulling the master sword pedestal to then defeat Ganon.
    Triforce Hunt sends you on a magical journey to collect 'em all and return them to Murahdala.
    Triforce Hunt Ganon requires all the pieces to approach Ganon.
    Ice Rod Hunt gives you every item except the Ice Rod, which you must find to defeat Trinexx for his Triforce Piece."""
    display_name = "Goal"
    option_ganon_and_tower = 0
    option_ganon = 1
    option_all_bosses = 2
    option_pedestal = 3
    option_pedestal_ganon = 4
    option_triforce_hunt = 5
    option_triforce_hunt_ganon = 6
    option_ice_rod_hunt = 7


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

    alias_yes = option_open
    alias_no = option_closed

    def to_bool(self, world: MultiWorld, player: int) -> bool:
        if self.value == self.option_goal:
            return world.goal[player] in {Goal.option_ganon, Goal.option_triforce_hunt_ganon,
                                          Goal.option_pedestal_ganon}
        if self.value == self.option_auto:
            return world.goal[player] in {Goal.option_ganon, Goal.option_triforce_hunt_ganon,
                                          Goal.option_pedestal_ganon} \
                   and (world.shuffle[player] in {'vanilla', 'dungeonssimple', 'dungeonsfull', 'dungeonscrossed'} or not
            world.shuffle_ganon)
        if self.value == self.option_open:
            return True
        return False


class DungeonItem(Choice):
    value: int
    option_original_dungeon = 0
    option_own_dungeons = 1
    option_own_world = 2
    option_any_world = 3
    option_different_world = 4
    option_start_with = 6
    alias_true = option_any_world
    alias_false = option_original_dungeon

    @property
    def in_dungeon(self):
        return self.value in {0, 1}

    @property
    def hints_useful(self):
        """Indicates if hints for this Item are useful in any way."""
        return self.value in {1, 2, 3, 4}


class BigKeyShuffle(DungeonItem):
    """How Big Keys will be placed."""
    item_name_group = "Big Keys"
    display_name = "Big Key Shuffle"


class SmallKeyShuffle(DungeonItem):
    """How Small Keys will be placed."""
    option_universal = 5
    item_name_group = "Small Keys"
    display_name = "Small Key Shuffle"


class CompassShuffle(DungeonItem):
    """How Compasses will be placed."""
    item_name_group = "Compasses"
    display_name = "Compass Shuffle"


class MapShuffle(DungeonItem):
    """How maps will be placed."""
    item_name_group = "Maps"
    display_name = "Map Shuffle"


class Crystals(Range):
    range_start = 0
    range_end = 7
    default = 7


class CrystalsTower(Crystals):
    """Number of Crystals needed to enter Ganon's Tower."""
    display_name = "Crystals for Ganon's Tower"


class CrystalsGanon(Crystals):
    """Number of Crystals needed to damage Ganon."""
    display_name = "Crystals for Ganon"


class TriforcePieces(Range):
    default = 30
    range_start = 1
    range_end = 90


class TriforceMode(Choice):
    """Determines how extra available triforce pieces are calculated. Up to 90 can be available.
    Extra makes available pieces = extra + required.
    Percentage makes available pieces = percentage * required.
    Available makes available pieces = available value."""
    display_name = "Triforce Pieces Mode"
    option_extra = 0
    option_percentage = 1
    option_available = 2
    default = option_available


class TriforceExtra(TriforcePieces):
    """How many extra Triforce pieces are available."""
    display_name = "Extra Triforce Pieces"
    default = 10


class TriforcePercentage(Range):
    """Percentage of required Triforce pieces that will be available."""
    display_name = "Triforce Percent"
    range_start = 100
    range_end = 200
    default = 150


class TriforceAvailable(TriforcePieces):
    """Total number of available Triforce pieces."""
    display_name = "Triforce Pieces Available"
    default = 30


class TriforceRequired(TriforcePieces):
    """Number of Triforce pieces required to complete the goal."""
    display_name = "Triforce Pieces Required"
    default = 20


class ShopItemSlots(Range):
    """Number of shop slots that can contain items from the multiworld."""
    display_name = "Shop Item Slots"
    range_start = 0
    range_end = 30


class ShopPriceModifier(Range):
    """Percentage modifier for shuffled item prices in shops"""
    display_name = "Shop Item Price"
    range_start = 0
    default = 100
    range_end = 400


class PrizeShuffle(Choice):
    """Affects how prize packs that enemies drop get shuffled around."""
    display_name = "Prize Pack Shuffle"
    option_none = 0
    option_general = 1
    option_bonk = 2
    option_both = 3
    alias_g = option_general
    alias_b = option_bonk
    alias_bg = option_both
    default = option_general


class Timer(Choice):
    """Displays a timer that can count up or down while you play and can add clocks to the item pool that add or
    subtract time.
    Timed counts up from 0 and adds clocks to the pool.
    Timed ohko counts down with clocks in the pool.
    OHKO has the timer at 0 with no clocks. Permanent OHKO.
    Countdown counts down with clocks in the pool. No penalty at 0 though.
    Display counts up from 0 with no clocks in the pool."""
    display_name = "In Game Timer"
    option_none = 0
    option_timed = 1
    option_timed_ohko = 2
    option_ohko = 3
    option_timed_countdown = 4
    option_display = 5


class Countdown(Range):
    """Determines the starting time for the timed OHKO and timed countdown modes in minutes."""
    display_name = "Countdown Start Time"
    range_end = 60
    default = 20


class RedClock(Range):
    """The amount of time in minutes gained or lost from red clocks."""
    display_name = "Red Clock Time"
    range_start = -5
    range_end = 1
    default = -2


class BlueClock(Range):
    """The amount of time in minutes gained from blue clocks."""
    display_name = "Blue Clock Time"
    range_start = 1
    range_end = 3
    default = 2


class GreenClock(Range):
    """The amount of time in minutes gained from green clocks."""
    display_name = "Green Clock Time"
    range_start = 4
    range_end = 15
    default = 4


class WorldState(Choice):
    """Starting world state for the game.
    Standard starts with the rain sequence and uncle will have a guaranteed weapon including bombs.
    Open starts at Link's House in Light World with the player free to go anywhere.
    Inverted begins at Link's House in the Dark World, requiring Moon Pearl for Light World access as well as other
    changes."""
    display_name = "World State"
    option_standard = 1
    option_open = 0
    option_inverted = 2
    default = option_open

    @property
    def inverted(self) -> bool:
        return self.value == self.option_inverted


class Medallions(Choice):
    option_ether = 0
    option_bombos = 1
    option_quake = 2
    default = "random"


class MireMedallion(Medallions):
    """Required medallion to open Misery Mire entrance."""
    display_name = "Misery Mire Medallion"


class TurtleMedallion(Medallions):
    """Required medallion to open Turtle Rock entrance."""
    display_name = "Turtle Rock Medallion"


class Bosses(TextChoice):
    """Shuffles bosses around to different locations.
    Basic will shuffle all bosses except Ganon and Agahnim anywhere they can be placed.
    Full chooses 3 bosses at random to be placed twice instead of Lanmolas, Moldorm, and Helmasaur.
    Chaos allows any boss to appear any number of times.
    Singularity places a single boss in as many places as possible, and a second boss in any remaining locations.
    Supports plando placement. Formatting here: https://archipelago.gg/tutorial/A%20Link%20to%20the%20Past/plando/en"""
    display_name = "Boss Shuffle"
    option_none = 0
    option_basic = 1
    option_full = 2
    option_chaos = 3
    option_singularity = 4

    bosses: set = {
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

    locations: set = {
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

    def __init__(self, value: typing.Union[str, int]):
        assert isinstance(value, str) or isinstance(value, int), \
            f"{value} is not a valid option for {self.__class__.__name__}"
        self.value = value

    @classmethod
    def from_text(cls, text: str):
        import random
        # set all of our text to lower case for name checking
        text = text.lower()
        cls.bosses = {boss_name.lower() for boss_name in cls.bosses}
        cls.locations = {boss_location.lower() for boss_location in cls.locations}
        if text == "random":
            return cls(random.choice(list(cls.options.values())))
        for option_name, value in cls.options.items():
            if option_name == text:
                return cls(value)
        options = text.split(";")

        # since plando exists in the option verify the plando values given are valid
        cls.validate_plando_bosses(options)

        # find out what type of boss shuffle we should use for placing bosses after plando
        # and add as a string to look nice in the spoiler
        if "random" in options:
            shuffle = random.choice(list(cls.options))
            options.remove("random")
            options = ";".join(options) + ";" + shuffle
            boss_class = cls(options)
        else:
            for option in options:
                if option in cls.options:
                    boss_class = cls(";".join(options))
                    break
            else:
                if len(options) == 1:
                    if cls.valid_boss_name(options[0]):
                        options = options[0] + ";singularity"
                        boss_class = cls(options)
                    else:
                        options = options[0] + ";none"
                        boss_class = cls(options)
                else:
                    options = ";".join(options) + ";none"
                    boss_class = cls(options)
        return boss_class

    @classmethod
    def validate_plando_bosses(cls, options: typing.List[str]) -> None:
        from .Bosses import can_place_boss, format_boss_location
        for option in options:
            if option == "random" or option in cls.options:
                if option != options[-1]:
                    raise ValueError(f"{option} option must be at the end of the boss_shuffle options!")
                continue
            if "-" in option:
                location, boss = option.split("-")
                level = ''
                if not cls.valid_boss_name(boss):
                    raise ValueError(f"{boss} is not a valid boss name for location {location}.")
                if not cls.valid_location_name(location):
                    raise ValueError(f"{location} is not a valid boss location name.")
                if location.split(" ")[-1] in ("top", "middle", "bottom"):
                    location = location.split(" ")
                    level = location[-1]
                    location = " ".join(location[:-1])
                location = location.title().replace("Of", "of")
                if not can_place_boss(boss.title(), location, level):
                    raise ValueError(f"{format_boss_location(location, level)} "
                                     f"is not a valid location for {boss.title()}.")
            else:
                if not cls.valid_boss_name(option):
                    raise ValueError(f"{option} is not a valid boss name.")

    @classmethod
    def valid_boss_name(cls, value: str) -> bool:
        return value.lower() in cls.bosses

    @classmethod
    def valid_location_name(cls, value: str) -> bool:
        return value in cls.locations

    def verify(self, world, player_name: str, plando_options) -> None:
        if isinstance(self.value, int):
            return
        from Generate import PlandoSettings
        if not (PlandoSettings.bosses & plando_options):
            import logging
            # plando is disabled but plando options were given so pull the option and change it to an int
            option = self.value.split(";")[-1]
            self.value = self.options[option]
            logging.warning(f"The plando bosses module is turned off, so {self.name_lookup[self.value].title()} "
                            f"boss shuffle will be used for player {player_name}.")


class Enemies(Choice):
    """Method of enemy shuffle to use"""
    display_name = "Enemy Shuffle"
    option_vanilla = 0
    option_shuffled = 1
    option_chaos = 2


class Counters(Choice):
    """Determines if an item counter shows up in dungeons.
    Default will be True if compasses are in their own dungeons, otherwise on pickup."""
    display_name = "Dungeon Item Counter"
    option_off = 0
    option_compass = 1
    option_default = 2
    option_on = 3
    alias_pickup = option_compass
    default = option_compass


class Progressive(Choice):
    """Determines if items with upgrades are gained progressively. This involves sword, bow, boomerang, gloves, armor,
    and shields. Grouped random will randomly choose whether each group is progressive or not: i.e. you could have
    progressive swords and still find Titan's Mitts before Power Glove."""
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


class Difficulty(Choice):
    option_easy = 0
    option_normal = 1
    option_hard = 2
    option_expert = 3
    default = option_normal


class ItemPool(Difficulty):
    """Determines the frequency of useful items in the pool.
    Easy doubles the number of upgrades and progressive weapons and armor.
    Hard has maximum of: 14 hearts, blue mail, tempered sword, red shield, and
    silvers are removed if glitch logic is enabled.
    Expert has maximum of: 8 hearts, green mail, master sword, fighter shield,
    and silvers are removed if glitch logic is enabled."""
    display_name = "Item Pool"


class ItemFunc(Difficulty):
    """Modifies the functionality of certain items within the item pool.
    Easy allows hammer to damage ganon and collect tablets, and medallions can be used anywhere without a sword.
    Hard makes potions less effective, faeries can't be caught,cape uses double magic,
    byrna does not grant invulnerability, boomerangs do not stun, and silvers are disabled outside Ganon.
    Expert is like hard except potions are even weaker, and hookshot does not stun."""
    display_name = "Item Functionality"


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


class EnemyDamage(Choice):
    """Randomizes the amount of damage enemies deal.
    Shuffled causes enemies to deal from 0-4 hearts and armor upgrades always help.
    Chaos causes enemies to deal from 0-8 hearts and armor reshuffles the damage."""
    display_name = "Enemy Damage"
    option_default = 0
    option_shuffled = 1
    option_chaos = 2
    alias_none = option_default


class EnemyHealth(Choice):
    """Modifies amount of health that enemies have.
    Easy reduces their health, hard increases it, and expert greatly increases it."""
    display_name = "Enemy Health"
    option_easy = 1
    option_normal = 0
    option_hard = 2
    option_expert = 3

    alias_default = option_normal
    default = option_normal


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
    """Determines the type of palette to be used for the Overworld layer."""
    display_name = "Overworld Palette"


class UWPalette(Palette):
    """Determines the type of palette to be used for the Underworld layer."""
    display_name = "Underworld Palette"


class HUDPalette(Palette):
    """Determines the type of palette to be used for the gameplay HUD."""
    display_name = "Menu Palette"


class SwordPalette(Palette):
    """Determines the type of palette to be used for Link's sword."""
    display_name = "Sword Palette"


class ShieldPalette(Palette):
    """Determines the type of palette to be used for Link's Shield."""
    display_name = "Shield Palette"


# class LinkPalette(Palette):
#     display_name = "Link Palette"


class HeartBeep(Choice):
    """Determines the speed of the heart beep sound effect."""
    display_name = "Heart Beep Rate"
    option_normal = 0
    option_double = 1
    option_half = 2
    option_quarter = 3
    option_off = 4


class HeartColor(Choice):
    """Sets colors of hearts representing your current health."""
    display_name = "Heart Color"
    option_red = 0
    option_blue = 1
    option_green = 2
    option_yellow = 3


class QuickSwap(DefaultOnToggle):
    """Allows swapping between items with the L/R buttons without opening the menu."""
    display_name = "L/R Quickswapping"


class MenuSpeed(Choice):
    """Determines the speed at which the menu opens and closes."""
    display_name = "Menu Speed"
    option_normal = 0
    option_instant = 1,
    option_double = 2
    option_triple = 3
    option_quadruple = 4
    option_half = 5


class RandomSprite(OptionList):
    """Allows different random sprite events to be simultaneously enabled."""
    display_name = "Random Sprite Events"
    valid_keys = {"on_hit", "on_enter", "on_exit", "on_slash", "on_item", "on_bonk"}


class RandomSpriteToggle(Toggle):
    """Enabling this will enable options in the random sprite event list, causing your sprite to be randomized from your
    sprite pool."""
    display_name = "Use Random Sprite Events"


class Sprites:
    @lru_cache(None)
    def __get__(self, instance, owner):
        from worlds.alttp.Rom import _populate_sprite_table
        sprite_table = {}
        _populate_sprite_table(sprite_table)
        return {sprite for sprite in sprite_table}


class SpritePool(OptionList):
    """Limits the pool of available sprites for random events to specified pool."""
    display_name = "Sprite Pool"
    valid_keys = Sprites()


class Sprite(TextChoice):
    """Allows you to either specify which sprite you'd like to use or use a random on event option with the sprite pool."""
    display_name = "Sprite"
    option_link = 0
    option_random_on_hit = 1
    option_random_on_enter = 2
    option_random_on_exit = 3
    option_random_on_slash = 4
    option_random_on_item = 5
    option_random_on_bonk = 6
    option_random_on_all = 7

    valid_keys = Sprites()

    def verify(self, world, player_name, plando_options) -> None:
        if isinstance(self.value, int):
            return
        if self.value in self.valid_keys:
            return
        raise ValueError(f"{self.value} for {player_name} is not a valid Sprite option.")


class Music(DefaultOnToggle):
    """If music is played in the game."""
    display_name = "Play music"


class ReduceFlashing(DefaultOnToggle):
    """If screen flashing should be reduced for certain events such as wall opening animations and misery mire
    opening."""
    display_name = "Reduce Screen Flashes"


class TriforceHud(Choice):
    """How the HUD for Triforce Hunt modes should appear. Goal shows the full counter once a piece is collected
    or Murahadala is spoken to."""
    display_name = "Display Method for Triforce Hunt"
    option_always_show = 0
    option_hide_goal = 1
    option_hide_required = 2
    option_hide_both = 3
    alias_normal = option_always_show


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
    "glitches_required": Logic,
    "dark_room_logic": DarkRoomLogic,
    "glitch_boots": GlitchBoots,
    "world_state": WorldState,
    "crystals_needed_for_gt": CrystalsTower,
    "crystals_needed_for_ganon": CrystalsGanon,
    "open_pyramid": OpenPyramid,
    "goal": Goal,
    "triforce_pieces_mode": TriforceMode,
    "triforce_pieces_extra": TriforceExtra,
    "triforce_pieces_percentage": TriforcePercentage,
    "triforce_pieces_available": TriforceAvailable,
    "triforce_pieces_required": TriforceRequired,
    "bigkey_shuffle": BigKeyShuffle,
    "smallkey_shuffle": SmallKeyShuffle,
    "compass_shuffle": CompassShuffle,
    "map_shuffle": MapShuffle,
    "dungeon_counters": Counters,
    "progressive": Progressive,
    "swordless": Swordless,
    "item_pool": ItemPool,
    "item_functionality": ItemFunc,
    "retro_bow": RetroBow,
    "retro_caves": RetroCaves,
    "hints": Hints,
    "scams": Scams,
    "restrict_dungeon_item_on_boss": RestrictBossItem,
    "boss_shuffle": Bosses,
    "pot_shuffle": PotShuffle,
    "misery_mire_medallion": MireMedallion,
    "turtle_rock_medallion": TurtleMedallion,
    "enemy_shuffle": EnemyShuffle,
    "enemy_damage": EnemyDamage,
    "enemy_health": EnemyHealth,
    "killable_thieves": KillableThieves,
    "bush_shuffle": BushShuffle,
    "shop_item_slots": ShopItemSlots,
    "shop_price_modifier": ShopPriceModifier,
    "timer": Timer,
    "countdown_start_time": Countdown,
    "red_clock_time": RedClock,
    "blue_clock_time": BlueClock,
    "green_clock_time": GreenClock,
    "shuffle_prizes": PrizeShuffle,
    "tile_shuffle": TileShuffle,
    "use_random_sprite_events": RandomSpriteToggle,
    "random_sprite_events": RandomSprite,
    "sprite_pool": SpritePool,
    "sprite": Sprite,
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
    "beemizer_total_chance": BeemizerTotalChance,
    "beemizer_trap_chance": BeemizerTrapChance,
    "death_link": DeathLink,
    "allow_collect": AllowCollect
}
