from dataclasses import dataclass

import os.path
import typing
import logging
from Options import Choice, Toggle, DefaultOnToggle, Range, FreeText, PerGameCommonOptions, OptionGroup, Removed, StartInventoryPool
from collections import defaultdict
import Utils

DefaultOffToggle = Toggle

logger = logging.getLogger("Link's Awakening Logger")


class LADXROption:
    def to_ladxr_option(self, all_options):
        if not self.ladxr_name:
            return None, None

        return (self.ladxr_name, self.name_lookup[self.value].replace("_", ""))


class Logic(Choice, LADXROption):
    """
    Affects where items are allowed to be placed.

    **Normal:** Playable without using any tricks or glitches. Can require
    knowledge from a vanilla playthrough, such as how to open Color Dungeon.

    **Hard:** More advanced techniques may be required, but glitches are not.
    Examples include tricky jumps, killing enemies with only pots.

    **Glitched:** Advanced glitches and techniques may be required, but
    extremely difficult or tedious tricks are not required. Examples include
    Bomb Triggers, Super Jumps and Jesus Jumps.

    **Hell:** Obscure knowledge and hard techniques may be required. Examples
    include featherless jumping with boots and/or hookshot, sequential pit
    buffers and unclipped superjumps. Things in here can be extremely hard to do
    or very time consuming.
    """
    display_name = "Logic"
    rich_text_doc = True
    ladxr_name = "logic"
    # option_casual = 0
    option_normal = 1
    option_hard = 2
    option_glitched = 3
    option_hell = 4

    default = option_normal


class TradeQuest(DefaultOffToggle, LADXROption):
    """
    Trade quest items are randomized. Each NPC takes its normal trade quest
    item and gives a randomized item in return.
    """
    display_name = "Trade Quest"
    ladxr_name = "tradequest"


class TextShuffle(DefaultOffToggle):
    """
    Shuffles all text in the game.
    """
    display_name = "Text Shuffle"


class Rooster(DefaultOnToggle, LADXROption):
    """
    Adds the rooster to the item pool. If disabled, the overworld will be
    modified so that any location requiring the rooster is accessible by other
    means.
    """
    display_name = "Rooster"
    ladxr_name = "rooster"


class EntranceShuffle(Choice, LADXROption):
    """
    Randomizes where overworld entrances lead.

    **Simple:** Single-entrance caves/houses that have items are shuffled
    amongst each other.

    If *Dungeon Shuffle* is enabled, then dungeons will be shuffled with all the
    non-connector entrances in the pool. Note, some entrances can lead into water, use
    the warp-to-home from the save&quit menu to escape this.
    """

    # [Advanced] Simple, but two-way connector caves are shuffled in their own pool as well.
    # [Expert] Advanced, but caves/houses without items are also shuffled into the Simple entrance pool.
    # [Insanity] Expert, but the Raft Minigame hut and Mamu's cave are added to the non-connector pool.

    option_none = 0
    option_simple = 1
    # option_advanced = 2
    # option_expert = 3
    # option_insanity = 4
    default = option_none
    display_name = "Entrance Shuffle"
    ladxr_name = "entranceshuffle"
    rich_text_doc = True


class DungeonShuffle(DefaultOffToggle, LADXROption):
    """
    Randomizes dungeon entrances with each other.
    """
    display_name = "Dungeon Shuffle"
    ladxr_name = "dungeonshuffle"


class APTitleScreen(DefaultOnToggle):
    """
    Enables AP specific title screen and disables the intro cutscene.
    """
    display_name = "AP Title Screen"


class BossShuffle(Choice):
    display_name = "Boss Shuffle"
    none = 0
    shuffle = 1
    random = 2
    default = none


class DungeonItemShuffle(Choice):
    display_name = "Dungeon Item Shuffle"
    rich_text_doc = True
    option_original_dungeon = 0
    option_own_dungeons = 1
    option_own_world = 2
    option_any_world = 3
    option_different_world = 4
    # option_delete = 5
    # option_start_with = 6
    alias_true = 3
    alias_false = 0
    ladxr_item: str


class ShuffleNightmareKeys(DungeonItemShuffle):
    """
    **Original Dungeon:** The item will be within its original dungeon.

    **Own Dungeons:** The item will be within a dungeon in your world.

    **Own World:** The item will be somewhere in your world.

    **Any World:** The item could be anywhere.

    **Different World:** The item will be somewhere in another world.
    """
    display_name = "Shuffle Nightmare Keys"
    ladxr_item = "NIGHTMARE_KEY"


class ShuffleSmallKeys(DungeonItemShuffle):
    """
    **Original Dungeon:** The item will be within its original dungeon.

    **Own Dungeons:** The item will be within a dungeon in your world.

    **Own World:** The item will be somewhere in your world.

    **Any World:** The item could be anywhere.

    **Different World:** The item will be somewhere in another world.
    """
    display_name = "Shuffle Small Keys"
    ladxr_item = "KEY"


class ShuffleMaps(DungeonItemShuffle):
    """
    **Original Dungeon:** The item will be within its original dungeon.

    **Own Dungeons:** The item will be within a dungeon in your world.

    **Own World:** The item will be somewhere in your world.

    **Any World:** The item could be anywhere.

    **Different World:** The item will be somewhere in another world.
    """
    display_name = "Shuffle Maps"
    ladxr_item = "MAP"


class ShuffleCompasses(DungeonItemShuffle):
    """
    **Original Dungeon:** The item will be within its original dungeon.

    **Own Dungeons:** The item will be within a dungeon in your world.

    **Own World:** The item will be somewhere in your world.

    **Any World:** The item could be anywhere.

    **Different World:** The item will be somewhere in another world.
    """
    display_name = "Shuffle Compasses"
    ladxr_item = "COMPASS"


class ShuffleStoneBeaks(DungeonItemShuffle):
    """
    **Original Dungeon:** The item will be within its original dungeon.

    **Own Dungeons:** The item will be within a dungeon in your world.

    **Own World:** The item will be somewhere in your world.

    **Any World:** The item could be anywhere.

    **Different World:** The item will be somewhere in another world.
    """
    display_name = "Shuffle Stone Beaks"
    ladxr_item = "STONE_BEAK"


class ShuffleInstruments(DungeonItemShuffle):
    """
    **Original Dungeon:** The item will be within its original dungeon.

    **Own Dungeons:** The item will be within a dungeon in your world.

    **Own World:** The item will be somewhere in your world.

    **Any World:** The item could be anywhere.

    **Different World:** The item will be somewhere in another world.

    **Vanilla:** The item will be in its vanilla location in your world.
    """
    display_name = "Shuffle Instruments"
    ladxr_item = "INSTRUMENT"
    default = 100
    option_vanilla = 100
    alias_false = 100


class Goal(Choice, LADXROption):
    """
    The Goal of the game.

    **Instruments:** The Wind Fish's Egg will only open if you have the required
    number of Instruments of the Sirens, and play the Ballad of the Wind Fish.

    **Seashells:** The Egg will open when you bring 20 seashells. The Ballad and
    Ocarina are not needed.

    **Open:** The Egg will start pre-opened.
    """
    display_name = "Goal"
    rich_text_doc = True
    ladxr_name = "goal"
    option_instruments = 1
    option_seashells = 2
    option_open = 3

    default = option_instruments

    def to_ladxr_option(self, all_options):
        if self.value == self.option_instruments:
            return ("goal", all_options["instrument_count"])
        else:
            return LADXROption.to_ladxr_option(self, all_options)


class InstrumentCount(Range, LADXROption):
    """
    Sets the number of instruments required to open the Egg.
    """
    display_name = "Instrument Count"
    ladxr_name = None
    range_start = 0
    range_end = 8
    default = 8


class NagMessages(DefaultOffToggle, LADXROption):
    """
    Controls if nag messages are shown when rocks and crystals are touched.
    Useful for glitches, annoying for everything else.
    """
    display_name = "Nag Messages"
    ladxr_name = "nagmessages"


class MusicChangeCondition(Choice):
    """
    Controls how the music changes.

    **Sword:** When you pick up a sword, the music changes.

    **Always:** You always have the post-sword music.
    """
    display_name = "Music Change Condition"
    rich_text_doc = True
    option_sword = 0
    option_always = 1
    default = option_always


class HardMode(Choice, LADXROption):
    """
    **Oracle:** Less iframes and health from drops. Bombs damage yourself. Water
    damages you without flippers. No pieces of power or acorns.

    **Hero:** Switch version hero mode, double damage, no heart/fairy drops.

    **OHKO:** You die on a single hit, always.
    """
    display_name = "Hard Mode"
    ladxr_name = "hardmode"
    rich_text_doc = True
    option_none = 0
    option_oracle = 1
    option_hero = 2
    option_ohko = 3
    default = option_none


class Stealing(Choice, LADXROption):
    """
    Puts stealing from the shop in logic if the player has a sword.
    """
    display_name = "Stealing"
    ladxr_name = "steal"
    option_in_logic = 1
    option_out_of_logic = 2
    option_disabled = 3
    default = option_out_of_logic


class Overworld(Choice, LADXROption):
    """
    **Open Mabe:** Replaces rock on the east side of Mabe Village with bushes,
    allowing access to Ukuku Prairie without Power Bracelet.
    """
    display_name = "Overworld"
    ladxr_name = "overworld"
    rich_text_doc = True
    option_normal = 0
    option_open_mabe = 1
    default = option_normal


class Quickswap(Choice, LADXROption):
    """
    Instead of opening the map, the *SELECT* button swaps the top item of your inventory on to your *A* or *B* button.
    """
    display_name = "Quickswap"
    ladxr_name = "quickswap"
    rich_text_doc = True
    option_none = 0
    option_a = 1
    option_b = 2
    default = option_none


class TextMode(Choice, LADXROption):
    """
    **Fast:** Makes text appear twice as fast.
    """
    display_name = "Text Mode"
    ladxr_name = "textmode"
    rich_text_doc = True
    option_normal = 0
    option_fast = 1
    default = option_fast


class LowHpBeep(Choice, LADXROption):
    """
    Slows or disables the low health beeping sound.
    """
    display_name = "Low HP Beep"
    ladxr_name = "lowhpbeep"
    option_default = 0
    option_slow = 1
    option_none = 2
    default = option_default


class NoFlash(DefaultOnToggle, LADXROption):
    """
    Remove the flashing light effects from Mamu, shopkeeper and MadBatter.
    Useful for capture cards and people that are sensitive to these things.
    """
    display_name = "No Flash"
    ladxr_name = "noflash"


class BootsControls(Choice):
    """
    Adds an additional button to activate Pegasus Boots (does nothing if you
    haven't picked up your boots!)

    **Vanilla:** Nothing changes, you have to equip the boots to use them.

    **Bracelet:** Holding down the button for the bracelet also activates boots
    (somewhat like Link to the Past).

    **Press A:** Holding down A activates boots.

    **Press B:** Holding down B activates boots.
    """
    display_name = "Boots Controls"
    rich_text_doc = True
    option_vanilla = 0
    option_bracelet = 1
    option_press_a = 2
    alias_a = 2
    option_press_b = 3
    alias_b = 3


class LinkPalette(Choice, LADXROption):
    """
    Sets Link's palette.

    A-D are color palettes usually used during the damage animation and can
    change based on where you are.
    """
    display_name = "Link's Palette"
    ladxr_name = "linkspalette"
    option_normal = -1
    option_green = 0
    option_yellow = 1
    option_red = 2
    option_blue = 3
    option_invert_a = 4
    option_invert_b = 5
    option_invert_c = 6
    option_invert_d = 7
    default = option_normal

    def to_ladxr_option(self, all_options):
        return self.ladxr_name, str(self.value)


class TrendyGame(Choice):
    """
    **Easy:** All of the items hold still for you.

    **Normal:** The vanilla behavior.

    **Hard:** The trade item also moves.

    **Harder:** The items move faster.

    **Hardest:** The items move diagonally.

    **Impossible:** The items move impossibly fast, may scroll on and off the
    screen.
    """
    display_name = "Trendy Game"
    rich_text_doc = True
    option_easy = 0
    option_normal = 1
    option_hard = 2
    option_harder = 3
    option_hardest = 4
    option_impossible = 5
    default = option_normal


class GfxMod(DefaultOffToggle):
    """
    If enabled, the patcher will prompt the user for a modification file to change sprites in the game and optionally some text.
    """
    display_name = "GFX Modification"


class Palette(Choice):
    """
    Sets the palette for the game.

    Note: A few places aren't patched, such as the menu and a few color dungeon
    tiles.

    **Normal:** The vanilla palette.

    **1-Bit:** One bit of color per channel.

    **2-Bit:** Two bits of color per channel.

    **Greyscale:** Shades of grey.

    **Pink:** Aesthetic.

    **Inverted:** Inverted.
    """
    display_name = "Palette"
    rich_text_doc = True
    option_normal = 0
    option_1bit = 1
    option_2bit = 2
    option_greyscale = 3
    option_pink = 4
    option_inverted = 5


class Music(Choice, LADXROption):
    """
    **Vanilla:** Regular Music

    **Shuffled:** Shuffled Music

    **Off:** No music
    """
    display_name = "Music"
    ladxr_name = "music"
    rich_text_doc = True
    option_vanilla = 0
    option_shuffled = 1
    option_off = 2

    def to_ladxr_option(self, all_options):
        s = ""
        if self.value == self.option_shuffled:
            s = "random"
        elif self.value == self.option_off:
            s = "off"
        return self.ladxr_name, s


class Warps(Choice):
    """
    **Improved:** Adds remake style warp screen to the game. Choose your warp
    destination on the map after jumping in a portal and press *B* to select.

    **Improved Additional:** Improved warps, and adds a warp point at Crazy
    Tracy's house (the Mambo teleport spot) and Eagle's Tower.
    """
    display_name = "Warps"
    rich_text_doc = True
    option_vanilla = 0
    option_improved = 1
    option_improved_additional = 2
    default = option_vanilla


class InGameHints(DefaultOnToggle):
    """
    When enabled, owl statues and library books may indicate the location of
    your items in the multiworld.
    """
    display_name = "In-game Hints"


class TarinsGift(Choice):
    """
    **Local Progression:** Forces Tarin's gift to be an item that immediately
    opens up local checks. Has little effect in single player games, and isn't
    always necessary with randomized entrances.

    **Bush Breaker:** Forces Tarin's gift to be an item that can destroy bushes.

    **Any Item:** Tarin's gift can be any item for any world
    """
    display_name = "Tarin's Gift"
    rich_text_doc = True
    option_local_progression = 0
    option_bush_breaker = 1
    option_any_item = 2
    default = option_local_progression


class StabilizeItemPool(DefaultOffToggle):
    """
    By default, some rupees in the item pool are randomly swapped with bombs,
    arrows, powders, or capacity upgrades. This set of items is also used as
    filler. This option disables that swapping and makes *Nothing* the filler
    item.
    """
    display_name = "Stabilize Item Pool"
    rich_text_doc = True


class ForeignItemIcons(Choice):
    """
    Choose how to display foreign items.

    **Guess By Name:** Foreign items can look like any Link's Awakening item.

    **Indicate Progression:** Foreign items are either a Piece of Power
    (progression) or Guardian Acorn (non-progression).
    """
    display_name = "Foreign Item Icons"
    rich_text_doc = True
    option_guess_by_name = 0
    option_indicate_progression = 1
    default = option_guess_by_name


ladx_option_groups = [
    OptionGroup("Gameplay Adjustments", [
        InGameHints,
        TarinsGift,
        HardMode,
        TrendyGame,
    ]),
    OptionGroup("World Layout", [
        Overworld,
        Warps,
        DungeonShuffle,
        EntranceShuffle,
    ]),
    OptionGroup("Item Pool", [
        ShuffleInstruments,
        ShuffleNightmareKeys,
        ShuffleSmallKeys,
        ShuffleMaps,
        ShuffleCompasses,
        ShuffleStoneBeaks,
        TradeQuest,
        Rooster,
        StabilizeItemPool,
    ]),
    OptionGroup("Quality of Life & Aesthetic", [
        NagMessages,
        Quickswap,
        BootsControls,
        ForeignItemIcons,
        GfxMod,
        LinkPalette,
        Palette,
        APTitleScreen,
        TextShuffle,
        TextMode,
        Music,
        MusicChangeCondition,
        LowHpBeep,
        NoFlash,
    ])
]

@dataclass
class LinksAwakeningOptions(PerGameCommonOptions):
    logic: Logic
    tradequest: TradeQuest
    rooster: Rooster
    experimental_dungeon_shuffle: DungeonShuffle
    experimental_entrance_shuffle: EntranceShuffle
    goal: Goal
    instrument_count: InstrumentCount
    link_palette: LinkPalette
    warps: Warps
    trendy_game: TrendyGame
    gfxmod: GfxMod
    palette: Palette
    text_shuffle: TextShuffle
    foreign_item_icons: ForeignItemIcons
    shuffle_nightmare_keys: ShuffleNightmareKeys
    shuffle_small_keys: ShuffleSmallKeys
    shuffle_maps: ShuffleMaps
    shuffle_compasses: ShuffleCompasses
    shuffle_stone_beaks: ShuffleStoneBeaks
    music: Music
    shuffle_instruments: ShuffleInstruments
    music_change_condition: MusicChangeCondition
    nag_messages: NagMessages
    ap_title_screen: APTitleScreen
    boots_controls: BootsControls
    stealing: Stealing
    quickswap: Quickswap
    hard_mode: HardMode
    low_hp_beep: LowHpBeep
    text_mode: TextMode
    no_flash: NoFlash
    in_game_hints: InGameHints
    tarins_gift: TarinsGift
    overworld: Overworld
    stabilize_item_pool: StabilizeItemPool
    start_inventory_from_pool: StartInventoryPool

    warp_improvements: Removed
    additional_warp_points: Removed
