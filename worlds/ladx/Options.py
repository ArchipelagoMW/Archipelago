from dataclasses import dataclass

import os.path
import typing
import logging
from Options import Choice, Toggle, DefaultOnToggle, Range, FreeText, PerGameCommonOptions, OptionGroup, Removed
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
    [Normal] Playable without using any tricks or glitches. Can require knowledge from a vanilla playthrough, such as how to open Color Dungeon.
    [Hard] More advanced techniques may be required, but glitches are not. Examples include tricky jumps, killing enemies with only pots.
    [Glitched] Advanced glitches and techniques may be required, but extremely difficult or tedious tricks are not required. Examples include Bomb Triggers, Super Jumps and Jesus Jumps.
    [Hell] Obscure knowledge and hard techniques may be required. Examples include featherless jumping with boots and/or hookshot, sequential pit buffers and unclipped superjumps. Things in here can be extremely hard to do or very time consuming."""
    display_name = "Logic"
    ladxr_name = "logic"
    # option_casual = 0
    option_normal = 1
    option_hard = 2
    option_glitched = 3
    option_hell = 4

    default = option_normal


class TradeQuest(DefaultOffToggle, LADXROption):
    """
    [On] adds the trade items to the pool (the trade locations will always be local items)
    [Off] (default) doesn't add them
    """
    display_name = "Trade Quest"
    ladxr_name = "tradequest"


class TextShuffle(DefaultOffToggle):
    """
    [On] Shuffles all the text in the game
    [Off] (default) doesn't shuffle them.
    """
    display_name = "Text Shuffle"


class Rooster(DefaultOnToggle, LADXROption):
    """
    [On] Adds the rooster to the item pool.
    [Off] The rooster spot is still a check giving an item. But you will never find the rooster. In that case, any rooster spot is accessible without rooster by other means.
    """
    display_name = "Rooster"
    ladxr_name = "rooster"


class Boomerang(Choice):
    """
    [Normal] requires Magnifying Lens to get the boomerang.
    [Gift] The boomerang salesman will give you a random item, and the boomerang is shuffled.
    """
    display_name = "Boomerang"

    normal = 0
    gift = 1
    default = gift


class EntranceShuffle(Choice, LADXROption):
    """
    [WARNING] Experimental, may fail to fill
    Randomizes where overworld entrances lead to.
    [Simple] Single-entrance caves/houses that have items are shuffled amongst each other.
    If random start location and/or dungeon shuffle is enabled, then these will be shuffled with all the non-connector entrance pool.
    Note, some entrances can lead into water, use the warp-to-home from the save&quit menu to escape this."""

    # [Advanced] Simple, but two-way connector caves are shuffled in their own pool as well.
    # [Expert] Advanced, but caves/houses without items are also shuffled into the Simple entrance pool.
    # [Insanity] Expert, but the Raft Minigame hut and Mamu's cave are added to the non-connector pool.

    option_none = 0
    option_simple = 1
    # option_advanced = 2
    # option_expert = 3
    # option_insanity = 4
    default = option_none
    display_name = "Experimental Entrance Shuffle"
    ladxr_name = "entranceshuffle"


class DungeonShuffle(DefaultOffToggle, LADXROption):
    """
    [WARNING] Experimental, may fail to fill
    Randomizes dungeon entrances within eachother
    """
    display_name = "Experimental Dungeon Shuffle"
    ladxr_name = "dungeonshuffle"


class APTitleScreen(DefaultOnToggle):
    """
    Enables AP specific title screen and disables the intro cutscene
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
    Shuffle Nightmare Keys
    [Original Dungeon] The item will be within its original dungeon
    [Own Dungeons] The item will be within a dungeon in your world
    [Own World] The item will be somewhere in your world
    [Any World] The item could be anywhere
    [Different World] The item will be somewhere in another world
    """
    display_name = "Shuffle Nightmare Keys"
    ladxr_item = "NIGHTMARE_KEY"


class ShuffleSmallKeys(DungeonItemShuffle):
    """
    Shuffle Small Keys
    [Original Dungeon] The item will be within its original dungeon
    [Own Dungeons] The item will be within a dungeon in your world
    [Own World] The item will be somewhere in your world
    [Any World] The item could be anywhere
    [Different World] The item will be somewhere in another world
    """
    display_name = "Shuffle Small Keys"
    ladxr_item = "KEY"


class ShuffleMaps(DungeonItemShuffle):
    """
    Shuffle Dungeon Maps
    [Original Dungeon] The item will be within its original dungeon
    [Own Dungeons] The item will be within a dungeon in your world
    [Own World] The item will be somewhere in your world
    [Any World] The item could be anywhere
    [Different World] The item will be somewhere in another world
    """
    display_name = "Shuffle Maps"
    ladxr_item = "MAP"


class ShuffleCompasses(DungeonItemShuffle):
    """
    Shuffle Dungeon Compasses
    [Original Dungeon] The item will be within its original dungeon
    [Own Dungeons] The item will be within a dungeon in your world
    [Own World] The item will be somewhere in your world
    [Any World] The item could be anywhere
    [Different World] The item will be somewhere in another world
    """
    display_name = "Shuffle Compasses"
    ladxr_item = "COMPASS"


class ShuffleStoneBeaks(DungeonItemShuffle):
    """
    Shuffle Owl Beaks
    [Original Dungeon] The item will be within its original dungeon
    [Own Dungeons] The item will be within a dungeon in your world
    [Own World] The item will be somewhere in your world
    [Any World] The item could be anywhere
    [Different World] The item will be somewhere in another world
    """
    display_name = "Shuffle Stone Beaks"
    ladxr_item = "STONE_BEAK"


class ShuffleInstruments(DungeonItemShuffle):
    """
    Shuffle Instruments
    [Original Dungeon] The item will be within its original dungeon
    [Own Dungeons] The item will be within a dungeon in your world
    [Own World] The item will be somewhere in your world
    [Any World] The item could be anywhere
    [Different World] The item will be somewhere in another world
    [Vanilla] The item will be in its vanilla location in your world
    """
    display_name = "Shuffle Instruments"
    ladxr_item = "INSTRUMENT"
    default = 100
    option_vanilla = 100
    alias_false = 100


class Goal(Choice, LADXROption):
    """
    The Goal of the game
    [Instruments] The Wind Fish's Egg will only open if you have the required number of Instruments of the Sirens, and play the Ballad of the Wind Fish.
    [Seashells] The Egg will open when you bring 20 seashells. The Ballad and Ocarina are not needed.
    [Open] The Egg will start pre-opened.
    """
    display_name = "Goal"
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
    Sets the number of instruments required to open the Egg
    """
    display_name = "Instrument Count"
    ladxr_name = None
    range_start = 0
    range_end = 8
    default = 8


class NagMessages(DefaultOffToggle, LADXROption):
    """
    Controls if nag messages are shown when rocks and crystals are touched. Useful for glitches, annoying for everyone else.
    """
    display_name = "Nag Messages"
    ladxr_name = "nagmessages"


class MusicChangeCondition(Choice):
    """
    Controls how the music changes.
    [Sword] When you pick up a sword, the music changes
    [Always] You always have the post-sword music
    """
    display_name = "Music Change Condition"
    option_sword = 0
    option_always = 1
    default = option_always


#             Setting('hpmode', 'Gameplay', 'm', 'Health mode', options=[('default', '', 'Normal'), ('inverted', 'i', 'Inverted'), ('1', '1', 'Start with 1 heart'), ('low', 'l', 'Low max')], default='default',
#                 description="""
# [Normal} health works as you would expect.
# [Inverted] you start with 9 heart containers, but killing a boss will take a heartcontainer instead of giving one.
# [Start with 1] normal game, you just start with 1 heart instead of 3.
# [Low max] replace heart containers with heart pieces."""),


class HardMode(Choice, LADXROption):
    """
    [Oracle] Less iframes and health from drops. Bombs damage yourself. Water damages you without flippers. No piece of power or acorn.
    [Hero] Switch version hero mode, double damage, no heart/fairy drops.
    [One hit KO] You die on a single hit, always.
    """
    display_name = "Hard Mode"
    ladxr_name = "hardmode"
    option_none = 0
    option_oracle = 1
    option_hero = 2
    option_ohko = 3
    default = option_none


#             Setting('steal', 'Gameplay', 't', 'Stealing from the shop',
#                 options=[('always', 'a', 'Always'), ('never', 'n', 'Never'), ('default', '', 'Normal')], default='default',
#                 description="""Effects when you can steal from the shop. Stealing is bad and never in logic.
# [Normal] requires the sword before you can steal.
# [Always] you can always steal from the shop
# [Never] you can never steal from the shop."""),
class Bowwow(Choice):
    """Allows BowWow to be taken into any area.  Certain enemies and bosses are given a new weakness to BowWow.
    [Normal] BowWow is in the item pool, but can be logically expected as a damage source.
    [Swordless] The progressive swords are removed from the item pool.
    """
    display_name = "BowWow"
    normal = 0
    swordless = 1
    default = normal


class Overworld(Choice, LADXROption):
    """
    [Open Mabe] Replaces rock on the east side of Mabe Village with bushes, allowing access to Ukuku Prairie without Power Bracelet.
    """
    display_name = "Overworld"
    ladxr_name = "overworld"
    option_normal = 0
    option_open_mabe = 1
    default = option_normal


# Setting('superweapons', 'Special', 'q', 'Enable super weapons', default=False,
#    description='All items will be more powerful, faster, harder, bigger stronger. You name it.'),


class Quickswap(Choice, LADXROption):
    """
    Adds that the SELECT button swaps with either A or B. The item is swapped with the top inventory slot. The map is not available when quickswap is enabled.
    """
    display_name = "Quickswap"
    ladxr_name = "quickswap"
    option_none = 0
    option_a = 1
    option_b = 2
    default = option_none


class TextMode(Choice, LADXROption):
    """
    [Fast] Makes text appear twice as fast
    """
    display_name = "Text Mode"
    ladxr_name = "textmode"
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
    Remove the flashing light effects from Mamu, shopkeeper and MadBatter. Useful for capture cards and people that are sensitive to these things.
    """
    display_name = "No Flash"
    ladxr_name = "noflash"


class BootsControls(Choice):
    """
    Adds additional button to activate Pegasus Boots (does nothing if you haven't picked up your boots!)
    [Vanilla] Nothing changes, you have to equip the boots to use them
    [Bracelet] Holding down the button for the bracelet also activates boots (somewhat like Link to the Past)
    [Press A] Holding down A activates boots
    [Press B] Holding down B activates boots
    """
    display_name = "Boots Controls"
    option_vanilla = 0
    option_bracelet = 1
    option_press_a = 2
    option_press_b = 3


class LinkPalette(Choice, LADXROption):
    """
    Sets link's palette
    A-D are color palettes usually used during the damage animation and can change based on where you are.
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
    [Easy] All of the items hold still for you
    [Normal] The vanilla behavior
    [Hard] The trade item also moves
    [Harder] The items move faster
    [Hardest] The items move diagonally
    [Impossible] The items move impossibly fast, may scroll on and off the screen
    """
    display_name = "Trendy Game"
    option_easy = 0
    option_normal = 1
    option_hard = 2
    option_harder = 3
    option_hardest = 4
    option_impossible = 5
    default = option_normal


class GfxMod(FreeText, LADXROption):
    """
    Sets the sprite for link, among other things
    The option should be the same name as a with sprite (and optional name) file in data/sprites/ladx
    """
    display_name = "GFX Modification"
    ladxr_name = "gfxmod"
    normal = ''
    default = 'Link'

    __spriteDir: str = Utils.local_path(os.path.join('data', 'sprites', 'ladx'))
    __spriteFiles: typing.DefaultDict[str, typing.List[str]] = defaultdict(list)

    extensions = [".bin", ".bdiff", ".png", ".bmp"]

    for file in os.listdir(__spriteDir):
        name, extension = os.path.splitext(file)
        if extension in extensions:
            __spriteFiles[name].append(file)

    def __init__(self, value: str):
        super().__init__(value)

    def verify(self, world, player_name: str, plando_options) -> None:
        if self.value == "Link" or self.value in GfxMod.__spriteFiles:
            return
        raise Exception(
            f"LADX Sprite '{self.value}' not found. Possible sprites are: {['Link'] + list(GfxMod.__spriteFiles.keys())}")

    def to_ladxr_option(self, all_options):
        if self.value == -1 or self.value == "Link":
            return None, None

        assert self.value in GfxMod.__spriteFiles

        if len(GfxMod.__spriteFiles[self.value]) > 1:
            logger.warning(
                f"{self.value} does not uniquely identify a file. Possible matches: {GfxMod.__spriteFiles[self.value]}. Using {GfxMod.__spriteFiles[self.value][0]}")

        return self.ladxr_name, self.__spriteDir + "/" + GfxMod.__spriteFiles[self.value][0]


class Palette(Choice):
    """
    Sets the palette for the game.
    Note: A few places aren't patched, such as the menu and a few color dungeon tiles.
    [Normal] The vanilla palette
    [1-Bit] One bit of color per channel
    [2-Bit] Two bits of color per channel
    [Greyscale] Shades of grey
    [Pink] Aesthetic
    [Inverted] Inverted
    """
    display_name = "Palette"
    option_normal = 0
    option_1bit = 1
    option_2bit = 2
    option_greyscale = 3
    option_pink = 4
    option_inverted = 5


class Music(Choice, LADXROption):
    """
    [Vanilla] Regular Music
    [Shuffled] Shuffled Music
    [Off] No music
    """
    display_name = "Music"
    ladxr_name = "music"
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
    [Improved] Adds remake style warp screen to the game. Choose your warp destination on the map after jumping in a portal and press B to select.
    [Improved Additional] Improved warps, and adds a warp point at Crazy Tracy's house (the Mambo teleport spot) and Eagle's Tower.
    """
    display_name = "Warps"
    option_vanilla = 0
    option_improved = 1
    option_improved_additional = 2
    default = option_vanilla


class InGameHints(DefaultOnToggle):
    """
    When enabled, owl statues and library books may indicate the location of your items in the multiworld.
    """
    display_name = "In-game Hints"


class TarinsGift(Choice):
    """
    [Local Progression] Forces Tarin's gift to be an item that immediately opens up local checks.
    Has little effect in single player games, and isn't always necessary with randomized entrances.
    [Bush Breaker] Forces Tarin's gift to be an item that can destroy bushes.
    [Any Item] Tarin's gift can be any item for any world
    """
    display_name = "Tarin's Gift"
    option_local_progression = 0
    option_bush_breaker = 1
    option_any_item = 2
    default = option_local_progression


class StabilizeItemPool(DefaultOffToggle):
    """
    By default, rupees in the item pool may be randomly swapped with bombs, arrows, powders, or capacity upgrades. This option disables that swapping, which is useful for plando.
    """
    display_name = "Stabilize Item Pool"


class ForeignItemIcons(Choice):
    """
    Choose how to display foreign items.
    [Guess By Name] Foreign items can look like any Link's Awakening item.
    [Indicate Progression] Foreign items are either a Piece of Power (progression) or Guardian Acorn (non-progression).
    """
    display_name = "Foreign Item Icons"
    option_guess_by_name = 0
    option_indicate_progression = 1
    default = option_guess_by_name


ladx_option_groups = [
    OptionGroup("Goal Options", [
        Goal,
        InstrumentCount,
    ]),
    OptionGroup("Shuffles", [
        ShuffleInstruments,
        ShuffleNightmareKeys,
        ShuffleSmallKeys,
        ShuffleMaps,
        ShuffleCompasses,
        ShuffleStoneBeaks
    ]),
    OptionGroup("Warp Points", [
        Warps,
    ]),
    OptionGroup("Miscellaneous", [
        TradeQuest,
        Rooster,
        TarinsGift,
        Overworld,
        TrendyGame,
        InGameHints,
        NagMessages,
        StabilizeItemPool,
        Quickswap,
        HardMode,
        BootsControls
    ]),
    OptionGroup("Experimental", [
        DungeonShuffle,
        EntranceShuffle
    ]),
    OptionGroup("Visuals & Sound", [
        LinkPalette,
        Palette,
        TextShuffle,
        ForeignItemIcons,
        APTitleScreen,
        GfxMod,
        Music,
        MusicChangeCondition,
        LowHpBeep,
        TextMode,
        NoFlash,
    ])
]

@dataclass
class LinksAwakeningOptions(PerGameCommonOptions):
    logic: Logic
    # 'heartpiece': DefaultOnToggle, # description='Includes heart pieces in the item pool'),
    # 'seashells': DefaultOnToggle, # description='Randomizes the secret sea shells hiding in the ground/trees. (chest are always randomized)'),
    # 'heartcontainers': DefaultOnToggle, # description='Includes boss heart container drops in the item pool'),
    # 'instruments': DefaultOffToggle, # description='Instruments are placed on random locations, dungeon goal will just contain a random item.'),
    tradequest: TradeQuest  # description='Trade quest items are randomized, each NPC takes its normal trade quest item, but gives a random item'),
    # 'witch': DefaultOnToggle, # description='Adds both the toadstool and the reward for giving the toadstool to the witch to the item pool'),
    rooster: Rooster  # description='Adds the rooster to the item pool. Without this option, the rooster spot is still a check giving an item. But you will never find the rooster. Any rooster spot is accessible without rooster by other means.'),
    # 'boomerang': Boomerang,
    # 'randomstartlocation': DefaultOffToggle, # 'Randomize where your starting house is located'),
    experimental_dungeon_shuffle: DungeonShuffle  # 'Randomizes the dungeon that each dungeon entrance leads to'),
    experimental_entrance_shuffle: EntranceShuffle
    # 'bossshuffle': BossShuffle,
    # 'minibossshuffle': BossShuffle,
    goal: Goal
    instrument_count: InstrumentCount
    # 'itempool': ItemPool,
    # 'bowwow': Bowwow,
    # 'overworld': Overworld,
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
    quickswap: Quickswap
    hard_mode: HardMode
    low_hp_beep: LowHpBeep
    text_mode: TextMode
    no_flash: NoFlash
    in_game_hints: InGameHints
    tarins_gift: TarinsGift
    overworld: Overworld
    stabilize_item_pool: StabilizeItemPool

    warp_improvements: Removed
    additional_warp_points: Removed
