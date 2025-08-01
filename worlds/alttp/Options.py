from dataclasses import dataclass

from BaseClasses import MultiWorld
from Options import Choice, Range, DeathLink, DefaultOnToggle, FreeText, ItemsAccessibility, PerGameCommonOptions, \
    PlandoBosses, PlandoConnections, PlandoTexts, Removed, StartInventoryPool, Toggle
from .EntranceShuffle import default_connections, default_dungeon_connections, \
    inverted_default_connections, inverted_default_dungeon_connections
from .Text import TextTable


class GlitchesRequired(Choice):
    """Determine the logic required to complete the seed
    None: No glitches required
    Minor Glitches: Puts fake flipper, waterwalk, super bunny shenanigans, and etc into logic
    Overworld Glitches: Assumes the player has knowledge of both overworld major glitches (boots clips, mirror clips) and minor glitches
    Hybrid Major Glitches: In addition to overworld glitches, also requires underworld clips between dungeons.
    No Logic: Your own items are placed with no regard to any logic; such as your Fire Rod can be on your Trinexx."""
    display_name = "Glitches Required"
    option_no_glitches = 0
    option_minor_glitches = 1
    option_overworld_glitches = 2
    option_hybrid_major_glitches = 3
    option_no_logic = 4
    alias_owg = 2
    alias_hmg = 3
    alias_none = 0


class DarkRoomLogic(Choice):
    """Logic for unlit dark rooms. Lamp: require the Lamp for these rooms to be considered accessible.
    Torches: in addition to lamp, allow the fire rod and presence of easily accessible torches for access.
    None: all dark rooms are always considered doable, meaning this may force completion of rooms in complete darkness."""
    display_name = "Dark Room Logic"
    option_lamp = 0
    option_torches = 1
    option_none = 2
    default = 0


class Goal(Choice):
    """Ganon: Climb GT, defeat Agahnim 2, and then kill Ganon
    Crystals: Only killing Ganon is required. However, items may still be placed in GT
    Bosses: Defeat the boss of all dungeons, including Agahnim's tower and GT (Aga 2)
    Pedestal: Pull the Triforce from the Master Sword pedestal
    Ganon Pedestal: Pull the Master Sword pedestal, then kill Ganon
    Triforce Hunt: Collect Triforce pieces spread throughout the worlds, then turn them in to Murahadala in front of Hyrule Castle
    Local Triforce Hunt: Collect Triforce pieces spread throughout your world, then turn them in to Murahadala in front of Hyrule Castle
    Ganon Triforce Hunt: Collect Triforce pieces spread throughout the worlds, then kill Ganon
    Local Ganon Triforce Hunt: Collect Triforce pieces spread throughout your world, then kill Ganon"""
    display_name = "Goal"
    default = 0
    option_ganon = 0
    option_crystals = 1
    option_bosses = 2
    option_pedestal = 3
    option_ganon_pedestal = 4
    option_triforce_hunt = 5
    option_local_triforce_hunt = 6
    option_ganon_triforce_hunt = 7
    option_local_ganon_triforce_hunt = 8


class EntranceShuffle(Choice):
    """Dungeons Simple: Shuffle just dungeons amongst each other, swapping dungeons entirely, so Hyrule Castle is always 1 dungeon.
    Dungeons Full: Shuffle any dungeon entrance with any dungeon interior, so Hyrule Castle can be 4 different dungeons, but keep dungeons to a specific world.
    Dungeons Crossed: like dungeons_full, but allow cross-world traversal through a dungeon. Warning: May force repeated dungeon traversal.
    Simple: Entrances are grouped together before being randomized. Interiors with two entrances are grouped shuffled together with each other,
    and Death Mountain entrances are shuffled only on Death Mountain. Dungeons are swapped entirely.
    Restricted: Like Simple, but single entrance interiors, multi entrance interiors, and Death Mountain interior entrances are all shuffled with each other.
    Full: Like Restricted, but all Dungeon entrances are shuffled with all non-Dungeon entrances.
    Crossed: Like Full, but interiors with multiple entrances are no longer confined to the same world, which may allow crossing worlds.
    Insanity: Like Crossed, but entrances and exits may be decoupled from each other, so that leaving through an exit may not return you to the entrance you entered from."""
    display_name = "Entrance Shuffle"
    default = 0
    alias_none = 0
    option_vanilla = 0
    option_dungeons_simple = 1
    option_dungeons_full = 2
    option_dungeons_crossed = 3
    option_simple = 4
    option_restricted = 5
    option_full = 6
    option_crossed = 7
    option_insanity = 8
    alias_dungeonssimple = 1
    alias_dungeonsfull = 2
    alias_dungeonscrossed = 3


class EntranceShuffleSeed(FreeText):
    """You can specify a number to use as an entrance shuffle seed, or a group name. Everyone with the same group name
    will get the same entrance shuffle result as long as their Entrance Shuffle, Mode, Retro Caves, and Glitches
    Required options are the same."""
    default = "random"
    display_name = "Entrance Shuffle Seed"


class TriforcePiecesMode(Choice):
    """Determine how to calculate the extra available triforce pieces.
    Extra: available = triforce_pieces_extra + triforce_pieces_required
    Percentage: available = (triforce_pieces_percentage /100) * triforce_pieces_required
    Available: available = triforce_pieces_available"""
    display_name = "Triforce Pieces Mode"
    default = 2
    option_extra = 0
    option_percentage = 1
    option_available = 2


class TriforcePiecesPercentage(Range):
    """Set to how many triforce pieces according to a percentage of the required ones, are available to collect in the world."""
    display_name = "Triforce Pieces Percentage"
    range_start = 100
    range_end = 1000
    default = 150


class TriforcePiecesAvailable(Range):
    """Set to how many triforces pieces are available to collect in the world. Default is 30. Max is 90, Min is 1"""
    display_name = "Triforce Pieces Available"
    range_start = 1
    range_end = 90
    default = 30


class TriforcePiecesRequired(Range):
    """Set to how many out of X triforce pieces you need to win the game in a triforce hunt.
    Default is 20. Max is 90, Min is 1."""
    display_name = "Triforce Pieces Required"
    range_start = 1
    range_end = 90
    default = 20


class TriforcePiecesExtra(Range):
    """Set to how many extra triforces pieces are available to collect in the world."""
    display_name = "Triforce Pieces Extra"
    range_start = 0
    range_end = 89
    default = 10


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
            return world.worlds[player].options.goal.current_key in {'crystals', 'ganon_triforce_hunt', 'local_ganon_triforce_hunt', 'ganon_pedestal'}
        elif self.value == self.option_auto:
            return world.worlds[player].options.goal.current_key in {'crystals', 'ganon_triforce_hunt', 'local_ganon_triforce_hunt', 'ganon_pedestal'} \
            and (world.worlds[player].options.entrance_shuffle.current_key in {'vanilla', 'dungeons_simple', 'dungeons_full', 'dungeons_crossed'} or not
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


class big_key_shuffle(DungeonItem):
    """Big Key Placement"""
    item_name_group = "Big Keys"
    display_name = "Big Key Shuffle"


class small_key_shuffle(DungeonItem):
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


class key_drop_shuffle(DefaultOnToggle):
    """Shuffle keys found in pots and dropped from killed enemies,
    respects the small key and big key shuffle options."""
    display_name = "Key Drop Shuffle"


class DungeonCounters(Choice):
    """On: Always display amount of items checked in a dungeon. Pickup: Show when compass is picked up.
    Default: Show when compass is picked up if the compass itself is shuffled. Off: Never show item count in dungeons."""
    display_name = "Dungeon Counters"
    default = 1
    option_on = 0
    option_pickup = 1
    option_default = 2
    option_off = 4


class Mode(Choice):
    """Standard: Begin the game by rescuing Zelda from her cell and escorting her to the Sanctuary
    Open: Begin the game from your choice of Link's House or the Sanctuary
    Inverted: Begin in the Dark World. The Moon Pearl is required to avoid bunny-state in Light World, and the Light World game map is altered"""
    option_standard = 0
    option_open = 1
    option_inverted = 2
    default = 1
    display_name = "Mode"


class ItemPool(Choice):
    """Easy: Doubled upgrades, progressives, and etc. Normal:  Item availability remains unchanged from vanilla game.
    Hard: Reduced upgrade availability (max: 14 hearts, blue mail, tempered sword, fire shield, no silvers unless swordless).
    Expert: Minimum upgrade availability (max: 8 hearts, green mail, master sword, fighter shield, no silvers unless swordless)."""
    display_name = "Item Pool"
    default = 1
    option_easy = 0
    option_normal = 1
    option_hard = 2
    option_expert = 3


class ItemFunctionality(Choice):
    """Easy: Allow Hammer to damage ganon, Allow Hammer tablet collection, Allow swordless medallion use everywhere.
    Normal: Vanilla item functionality
    Hard: Reduced helpfulness of items (potions less effective, can't catch faeries, cape uses double magic, byrna does not grant invulnerability, boomerangs do not stun, silvers disabled outside ganon)
    Expert: Vastly reduces the helpfulness of items (potions barely effective, can't catch faeries, cape uses double magic, byrna does not grant invulnerability, boomerangs and hookshot do not stun, silvers disabled outside ganon)"""
    display_name = "Item Functionality"
    default = 1
    option_easy = 0
    option_normal = 1
    option_hard = 2
    option_expert = 3


class EnemyHealth(Choice):
    """Default: Vanilla enemy HP. Easy: Enemies have reduced health. Hard: Enemies have increased health.
    Expert: Enemies have greatly increased health."""
    display_name = "Enemy Health"
    default = 1
    option_easy = 0
    option_default = 1
    option_hard = 2
    option_expert = 3


class EnemyDamage(Choice):
    """Default: Vanilla enemy damage. Shuffled: 0 # Enemies deal 0 to 4 hearts and armor helps.
    Chaos: Enemies deal 0 to 8 hearts and armor just reshuffles the damage."""
    display_name = "Enemy Damage"
    default = 0
    option_default = 0
    option_shuffled = 2
    option_chaos = 3


class ShufflePrizes(Choice):
    """Shuffle "general" prize packs, as in enemy, tree pull, dig etc.; "bonk" prizes; or both."""
    display_name = "Shuffle Prizes"
    default = 1
    option_off = 0
    option_general = 1
    option_bonk = 2
    option_both = 3


class Medallion(Choice):
    default = "random"
    option_ether = 0
    option_bombos = 1
    option_quake = 2


class MiseryMireMedallion(Medallion):
    """Required medallion to open Misery Mire front entrance."""
    display_name = "Misery Mire Medallion"


class TurtleRockMedallion(Medallion):
    """Required medallion to open Turtle Rock front entrance."""
    display_name = "Turtle Rock Medallion"


class Timer(Choice):
    """None: No timer will be displayed. OHKO: Timer always at zero. Permanent OHKO.
    Timed: Starts with clock at zero. Green clocks subtract 4 minutes (total 20). Blue clocks subtract 2 minutes (total 10). Red clocks add two minutes (total 10). Winner is the player with the lowest time at the end.
    Timed OHKO: Starts the clock at ten minutes. Green clocks add five minutes (total 25). As long as the clock as at zero, Link will die in one hit.
    Timed Countdown: Starts the clock with forty minutes. Same clocks as timed mode, but if the clock hits zero you lose. You can still keep playing, though.
    Display: Displays a timer, but otherwise does not affect gameplay or the item pool."""
    display_name = "Timer"
    option_none = 0
    option_timed = 1
    option_timed_ohko = 2
    option_ohko = 3
    option_timed_countdown = 4
    option_display = 5
    default = 0


class CountdownStartTime(Range):
    """For Timed OHKO and Timed Countdown timer modes, the amount of time in minutes to start with."""
    display_name = "Countdown Start Time"
    range_start = 0
    range_end = 480
    default = 10


class ClockTime(Range):
    range_start = -60
    range_end = 60


class RedClockTime(ClockTime):
    """For all timer modes, the amount of time in minutes to gain or lose when picking up a red clock."""
    display_name = "Red Clock Time"
    default = -2


class BlueClockTime(ClockTime):
    """For all timer modes, the amount of time in minutes to gain or lose when picking up a blue clock."""
    display_name = "Blue Clock Time"
    default = 2


class GreenClockTime(ClockTime):
    """For all timer modes, the amount of time in minutes to gain or lose when picking up a green clock."""
    display_name = "Green Clock Time"
    default = 4


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


class RandomizeShopInventories(Choice):
    """Generate new default inventories for overworld/underworld shops, and unique shops; or each shop independently"""
    display_name = "Randomize Shop Inventories"
    default = 0
    option_default = 0
    option_randomize_by_shop_type = 1
    option_randomize_each = 2


class ShuffleShopInventories(Toggle):
    """Shuffle default inventories of the shops around"""
    display_name = "Shuffle Shop Inventories"


class RandomizeShopPrices(Toggle):
    """Randomize the prices of the items in shop inventories"""
    display_name = "Randomize Shop Prices"


class RandomizeCostTypes(Toggle):
    """Prices of the items in shop inventories may cost hearts, arrow, or bombs instead of rupees"""
    display_name = "Randomize Cost Types"


class ShopPriceModifier(Range):
    """Percentage modifier for shuffled item prices in shops"""
    display_name = "Shop Price Modifier"
    range_start = 0
    default = 100
    range_end = 400


class IncludeWitchHut(Toggle):
    """Consider witch's hut like any other shop and shuffle/randomize it too"""
    display_name = "Include Witch's Hut"


class ShuffleCapacityUpgrades(Choice):
    """Shuffle capacity upgrades into the item pool (and allow them to traverse the multiworld).
    On Combined will shuffle only a single bomb upgrade and arrow upgrade each which bring you to the maximum capacity."""
    display_name = "Shuffle Capacity Upgrades"
    option_off = 0
    option_on = 1
    option_on_combined = 2
    alias_false = 0
    alias_true = 1


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
        from .Bosses import can_place_boss
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


class BomblessStart(Toggle):
    """Start with a max of 0 bombs available, requiring Bomb Upgrade items in order to use bombs"""
    display_name = "Bombless Start"


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


class AllowCollect(DefaultOnToggle):
    """Allows for !collect / co-op to auto-open chests containing items for other players."""
    display_name = "Allow Collection of checks for other players"


class ALttPPlandoConnections(PlandoConnections):
    entrances = set([connection[0] for connection in (
        *default_connections, *default_dungeon_connections, *inverted_default_connections,
        *inverted_default_dungeon_connections)])
    exits = set([connection[0] for connection in (
        *default_connections, *default_dungeon_connections, *inverted_default_connections,
        *inverted_default_dungeon_connections)])


class ALttPPlandoTexts(PlandoTexts):
    """Text plando. Format is:
    - text: 'This is your text'
      at: text_key
      percentage: 100
    Percentage is an integer from 1 to 100, and defaults to 100 when omitted."""
    valid_keys = TextTable.valid_keys


@dataclass
class ALTTPOptions(PerGameCommonOptions):
    accessibility: ItemsAccessibility
    plando_connections: ALttPPlandoConnections
    plando_texts: ALttPPlandoTexts
    start_inventory_from_pool: StartInventoryPool
    goal: Goal
    mode: Mode
    glitches_required: GlitchesRequired
    dark_room_logic: DarkRoomLogic
    open_pyramid: OpenPyramid
    crystals_needed_for_gt: CrystalsTower
    crystals_needed_for_ganon: CrystalsGanon
    triforce_pieces_mode: TriforcePiecesMode
    triforce_pieces_percentage: TriforcePiecesPercentage
    triforce_pieces_required: TriforcePiecesRequired
    triforce_pieces_available: TriforcePiecesAvailable
    triforce_pieces_extra: TriforcePiecesExtra
    entrance_shuffle: EntranceShuffle
    entrance_shuffle_seed: EntranceShuffleSeed
    big_key_shuffle: big_key_shuffle
    small_key_shuffle: small_key_shuffle
    key_drop_shuffle: key_drop_shuffle
    compass_shuffle: compass_shuffle
    map_shuffle: map_shuffle
    restrict_dungeon_item_on_boss: RestrictBossItem
    item_pool: ItemPool
    item_functionality: ItemFunctionality
    enemy_health: EnemyHealth
    enemy_damage: EnemyDamage
    progressive: Progressive
    swordless: Swordless
    dungeon_counters: DungeonCounters
    retro_bow: RetroBow
    retro_caves: RetroCaves
    hints: Hints
    scams: Scams
    boss_shuffle: LTTPBosses
    pot_shuffle: PotShuffle
    enemy_shuffle: EnemyShuffle
    killable_thieves: KillableThieves
    bush_shuffle: BushShuffle
    shop_item_slots: ShopItemSlots
    randomize_shop_inventories: RandomizeShopInventories
    shuffle_shop_inventories: ShuffleShopInventories
    include_witch_hut: IncludeWitchHut
    randomize_shop_prices: RandomizeShopPrices
    randomize_cost_types: RandomizeCostTypes
    shop_price_modifier: ShopPriceModifier
    shuffle_capacity_upgrades: ShuffleCapacityUpgrades
    bombless_start: BomblessStart
    shuffle_prizes: ShufflePrizes
    tile_shuffle: TileShuffle
    misery_mire_medallion: MiseryMireMedallion
    turtle_rock_medallion: TurtleRockMedallion
    glitch_boots: GlitchBoots
    beemizer_total_chance: BeemizerTotalChance
    beemizer_trap_chance: BeemizerTrapChance
    timer: Timer
    countdown_start_time: CountdownStartTime
    red_clock_time: RedClockTime
    blue_clock_time: BlueClockTime
    green_clock_time: GreenClockTime
    death_link: DeathLink
    allow_collect: AllowCollect
    ow_palettes: OWPalette
    uw_palettes: UWPalette
    hud_palettes: HUDPalette
    sword_palettes: SwordPalette
    shield_palettes: ShieldPalette
    # link_palettes: LinkPalette
    heartbeep: HeartBeep
    heartcolor: HeartColor
    quickswap: QuickSwap
    menuspeed: MenuSpeed
    music: Music
    reduceflashing: ReduceFlashing
    triforcehud: TriforceHud

    # removed:
    goals: Removed
    smallkey_shuffle: Removed
    bigkey_shuffle: Removed
