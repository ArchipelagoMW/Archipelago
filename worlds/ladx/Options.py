import os.path
import typing
import logging
from Options import Choice, Option, Toggle, DefaultOnToggle, Range, FreeText
from collections import defaultdict

DefaultOffToggle = Toggle

logger = logging.getLogger("Link's Awakening Logger")


class LADXROption:
    def to_ladxr_option(self, all_options):
        if not self.ladxr_name:
            return None, None
        
        return (self.ladxr_name, self.name_lookup[self.value].replace("_", ""))


class Logic(Choice, LADXROption):
    """Affects where items are allowed to be placed.
    [Casual] Same as normal, except that a few more complex options are removed, like removing bushes with powder and killing enemies with powder or bombs.
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
    On - adds the trade items to the pool (the trade locations will always be local items)
    Off - (default) doesn't add them
    """
    ladxr_name = "tradequest"


#            Setting('forwardfactor', 'Main', 'F', 'Forward Factor', default=0.0,
#                description="Forward item weight adjustment factor, lower values generate more rear heavy seeds while higher values generate front heavy seeds. Default is 0.5."),
#            Setting('accessibility', 'Main', 'A', 'Accessibility', options=[('all', 'a', '100% Locations'), ('goal', 'g', 'Beatable')], default='all',
#                description="""
#[100% Locations] guaranteed that every single item can be reached and gained.
#[Beatable] only guarantees that the game is beatable. Certain items/chests might never be reachable."""),
#            Setting('race', 'Main', 'V', 'Race mode', default=False, multiworld=False,
#                description="""
#Spoiler logs can not be generated for ROMs generated with race mode enabled, and seed generation is slightly different."""),
#             Setting('spoilerformat', 'Main', 'Spoiler Format', options=[('none', 'None'), ('text', 'Text'), ('json', 'JSON')], default='none', multiworld=False,
#                 description="""Affects how the spoiler log is generated.
# [None] No spoiler log is generated. One can still be manually dumped later.
# [Text] Creates a .txt file meant for a human to read.
# [JSON] Creates a .json file with a little more information and meant for a computer to read.""")


class Boomerang(Choice):
    """
    [Normal], requires Magnifying Lens to get the boomerang.
    [Gift], The boomerang salesman will give you a random item, and the boomerang is shuffled.
    """

    normal = 0
    gift = 1
    default = gift

# TODO: translate to lttp parlance
class EntranceShuffle(Choice, LADXROption):
    """
    [WARNING] Experimental, may break generation
    Randomizes where overworld entrances lead to.
    [Simple] Single-entrance caves/houses that have items are shuffled amongst each other.
    [Advanced] Simple, but two-way connector caves are shuffled in their own pool as well.
    [Expert] Advanced, but caves/houses without items are also shuffled into the Simple entrance pool.
    [Insanity] Expert, but the Raft Minigame hut and Mamu's cave are added to the non-connector pool.
    If random start location and/or dungeon shuffle is enabled, then these will be shuffled with all the non-connector entrance pool.
    Note, some entrances can lead into water, use the warp-to-home from the save&quit menu to escape this."""
    option_none = 0
    option_simple = 1
    #option_advanced = 2
    #option_expert = 3    
    #option_insanity = 4
    default = option_none
    ladxr_name = "entranceshuffle"

class DungeonShuffle(DefaultOffToggle, LADXROption):
    """
    [WARNING] Experimental, may break generation
    Randomizes
    """
    ladxr_name = "dungeonshuffle"

class BossShuffle(Choice):
    none = 0
    shuffle = 1
    random = 2
    default = none


class DungeonItemShuffle(Choice):
    option_original_dungeon = 0
    option_own_dungeons = 1
    option_own_world = 2
    option_any_world = 3
    option_different_world = 4
    #option_delete = 5
    #option_start_with = 6
    alias_true = 3
    alias_false = 0

class ShuffleNightmareKeys(DungeonItemShuffle):
    """
    Shuffle Nightmare Keys
    """
    ladxr_item = "NIGHTMARE_KEY"
class ShuffleSmallKeys(DungeonItemShuffle):
    """
    Shuffle Small Keys
    """
    ladxr_item = "KEY"
class ShuffleMaps(DungeonItemShuffle):
    """
    Shuffle Dungeon Maps
    """
    ladxr_item = "MAP"
class ShuffleCompasses(DungeonItemShuffle):
    """
    Shuffle Dungeon Compasses
    """
    ladxr_item = "COMPASS"
class ShuffleStoneBeaks(DungeonItemShuffle):
    """
    Shuffle Owl Beaks
    """
    ladxr_item = "STONE_BEAK"
class Goal(Choice, LADXROption):
    """
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
    ladxr_name = None
    range_start = 0
    range_end = 8
    default = 8

#class SeashellCount(Range):
#    range_start = 0
#    range_end = 20
#    default = 20

#             Setting('goal', 'Gameplay', 'G', 'Goal', options=[('8', '8', '8 instruments'), ('7', '7', '7 instruments'), ('6', '6', '6 instruments'),
#                                                          ('5', '5', '5 instruments'), ('4', '4', '4 instruments'), ('3', '3', '3 instruments'),
#                                                          ('2', '2', '2 instruments'), ('1', '1', '1 instrument'), ('0', '0', 'No instruments'),
#                                                          ('open', 'O', 'Egg already open'), ('random', 'R', 'Random instrument count'),
#                                                          ('open-4', '<', 'Random short game (0-4)'), ('5-8', '>', 'Random long game (5-8)'),
#                                                          ('seashells', 'S', 'Seashell hunt (20)'), ('bingo', 'b', 'Bingo!'),
#                                                          ('bingo-full', 'B', 'Bingo-25!')], default='8',
#                 description="""Changes the goal of the game.
# [1-8 instruments], number of instruments required to open the egg.
# [No instruments] open the egg without instruments, still requires the ocarina with the balled of the windfish
# [Egg already open] the egg is already open, just head for it once you have the items needed to defeat the boss.
# [Randomized instrument count] random number of instruments required to open the egg, between 0 and 8.
# [Random short/long game] random number of instruments required to open the egg, chosen between 0-4 and 5-8 respectively.
# [Seashell hunt] egg will open once you collected 20 seashells. Instruments are replaced by seashells and shuffled.
# [Bingo] Generate a 5x5 bingo board with various goals. Complete one row/column or diagonal to win!
# [Bingo-25] Bingo, but need to fill the whole bingo card to win!"""),
class ItemPool(Choice):
    """Effects which items are shuffled.
[Casual] Places multiple copies of key items.
[More keys] Adds additional small/nightmare keys so that dungeons are faster.
[Path of Pain]. Adds negative heart containers to the item pool."""
    casual = 0
    more_keys = 1
    normal = 2
    painful = 3
    default = normal

#             Setting('hpmode', 'Gameplay', 'm', 'Health mode', options=[('default', '', 'Normal'), ('inverted', 'i', 'Inverted'), ('1', '1', 'Start with 1 heart'), ('low', 'l', 'Low max')], default='default',
#                 description="""
# [Normal} health works as you would expect.
# [Inverted] you start with 9 heart containers, but killing a boss will take a heartcontainer instead of giving one.
# [Start with 1] normal game, you just start with 1 heart instead of 3.
# [Low max] replace heart containers with heart pieces."""),

#             Setting('hardmode', 'Gameplay', 'X', 'Hard mode', options=[('none', '', 'Disabled'), ('oracle', 'O', 'Oracle'), ('hero', 'H', 'Hero'), ('ohko', '1', 'One hit KO')], default='none',
#                 description="""
# [Oracle] Less iframes and heath from drops. Bombs damage yourself. Water damages you without flippers. No piece of power or acorn.
# [Hero] Switch version hero mode, double damage, no heart/fairy drops.
# [One hit KO] You die on a single hit, always."""),

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
    normal = 0
    swordless = 1
    default = normal

class Overworld(Choice, LADXROption):
    """
    [Dungeon Dive] Create a different overworld where all the dungeons are directly accessible and almost no chests are located in the overworld.
    [Tiny dungeons] All dungeons only consist of a boss fight and a instrument reward. Rest of the dungeon is removed.
    """
    display_name = "Overworld"
    ladxr_name = "overworld"
    option_normal = 0
    option_dungeon_dive = 1
    option_tiny_dungeons = 2
    # option_shuffled = 3
    default = option_normal

# Ugh, this will change what 'progression' means??
#Setting('owlstatues', 'Special', 'o', 'Owl statues', options=[('', '', 'Never'), ('dungeon', 'D', 'In dungeons'), ('overworld', 'O', 'On the overworld'), ('both', 'B', 'Dungeons and Overworld')], default='',
#    description='Replaces the hints from owl statues with additional randomized items'),

#Setting('superweapons', 'Special', 'q', 'Enable super weapons', default=False,
#    description='All items will be more powerful, faster, harder, bigger stronger. You name it.'),
#Setting('quickswap', 'User options', 'Q', 'Quickswap', options=[('none', '', 'Disabled'), ('a', 'a', 'Swap A button'), ('b', 'b', 'Swap B button')], default='none',
#    description='Adds that the select button swaps with either A or B. The item is swapped with the top inventory slot. The map is not available when quickswap is enabled.',
#    aesthetic=True),
#             Setting('textmode', 'User options', 'f', 'Text mode', options=[('fast', '', 'Fast'), ('default', 'd', 'Normal'), ('none', 'n', 'No-text')], default='fast',
#                 description="""[Fast] makes text appear twice as fast.
# [No-Text] removes all text from the game""", aesthetic=True),
#             Setting('lowhpbeep', 'User options', 'p', 'Low HP beeps', options=[('none', 'D', 'Disabled'), ('slow', 'S', 'Slow'), ('default', 'N', 'Normal')], default='slow',
#                 description='Slows or disables the low health beeping sound', aesthetic=True),
#             Setting('noflash', 'User options', 'l', 'Remove flashing lights', default=True,
#                 description='Remove the flashing light effects from Mamu, shopkeeper and MadBatter. Useful for capture cards and people that are sensitive for these things.',
#                 aesthetic=True),
#             Setting('nagmessages', 'User options', 'S', 'Show nag messages', default=False,
#                 description='Enables the nag messages normally shown when touching stones and crystals',
#                 aesthetic=True),
#             Setting('gfxmod', 'User options', 'c', 'Graphics', options=gfx_options, default='',
#                 description='Generally affects at least Link\'s sprite, but can alter any graphics in the game',
#                 aesthetic=True),
#             Setting('linkspalette', 'User options', 'C', "Link's color",
#                 options=[('-1', '-', 'Normal'), ('0', '0', 'Green'), ('1', '1', 'Yellow'), ('2', '2', 'Red'), ('3', '3', 'Blue'),
#                          ('4', '4', '?? A'), ('5', '5', '?? B'), ('6', '6', '?? C'), ('7', '7', '?? D')], default='-1', aesthetic=True,
#                 description="""Allows you to force a certain color on link.
# [Normal] color of link depends on the tunic.
# [Green/Yellow/Red/Blue] forces link into one of these colors.
# [?? A/B/C/D] colors of link are usually inverted and color depends on the area you are in."""),
#             Setting('music', 'User options', 'M', 'Music', options=[('', '', 'Default'), ('random', 'r', 'Random'), ('off', 'o', 'Disable')], default='',
#                 description="""
# [Random] Randomizes overworld and dungeon music'
# [Disable] no music in the whole game""",
#                 aesthetic=True),

class LinkPalette(Choice, LADXROption):
    """
    A-D are color palettes usually used during the damage animation and can change based on where you are.
    """
    display_name = "Links Palette"
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
    [Hard] ?
    [Harder] ???
    [Hardest] ????
    [Impossible] ?????
    """
    option_easy = 0
    option_normal = 1
    option_hard = 2
    option_harder = 3
    option_hardest = 4
    option_impossible = 5
    default = option_normal

class GfxMod(FreeText, LADXROption):
    """
    options here correlate with sprite and name files in data/sprites/ladx
    """
    display_name = "GFX Modification"
    ladxr_name = "gfxmod"
    normal = ''
    default = 'Link'

    __spriteFiles: typing.DefaultDict[str, typing.List[str]] = defaultdict(list)
    __spriteDir = os.path.join('data', 'sprites','ladx')

    extensions = [".bin", ".bdiff", ".png", ".bmp"]
    def __init__(self, value: str):
        super().__init__(value)
        if not GfxMod.__spriteFiles:
            for file in os.listdir(GfxMod.__spriteDir):
                name, extension = os.path.splitext(file)
                if extension in self.extensions:
                    GfxMod.__spriteFiles[name].append(file)
                    

    def to_ladxr_option(self, all_options):
        if self.value == -1 or self.value == "Link":
            return None, None
        elif self.value in GfxMod.__spriteFiles:
            if len(GfxMod.__spriteFiles[self.value]) > 1:
                logger.warning(f"{self.value} does not uniquely identify a file. Possible matches: {GfxMod.__spriteFiles[self.value]}. Using {GfxMod.__spriteFiles[self.value][0]}")
                return self.ladxr_name, GfxMod.__spriteFiles[self.value][0]
            return self.ladxr_name, GfxMod.__spriteFiles[self.value][0]
        logger.error(f"Spritesheet {self.value} not found. Falling back to default sprite.")
        return None, None

class Palette(Choice):
    option_normal = 0
    option_1bit = 1
    option_2bit = 2
    option_greyscale = 3
    option_pink = 4
    option_inverted = 5
    
links_awakening_options: typing.Dict[str, typing.Type[Option]] = {
    'logic': Logic,
    # 'heartpiece': DefaultOnToggle, # description='Includes heart pieces in the item pool'),                
    # 'seashells': DefaultOnToggle, # description='Randomizes the secret sea shells hiding in the ground/trees. (chest are always randomized)'),                
    # 'heartcontainers': DefaultOnToggle, # description='Includes boss heart container drops in the item pool'),                
    # 'instruments': DefaultOffToggle, # description='Instruments are placed on random locations, dungeon goal will just contain a random item.'),                
    'tradequest': TradeQuest, # description='Trade quest items are randomized, each NPC takes its normal trade quest item, but gives a random item'),                
    # 'witch': DefaultOnToggle, # description='Adds both the toadstool and the reward for giving the toadstool to the witch to the item pool'),                
    # 'rooster': DefaultOnToggle, # description='Adds the rooster to the item pool. Without this option, the rooster spot is still a check giving an item. But you will never find the rooster. Any rooster spot is accessible without rooster by other means.'),                
    # 'boomerang': Boomerang,
    # 'randomstartlocation': DefaultOffToggle, # 'Randomize where your starting house is located'),
    'experimental_dungeon_shuffle': DungeonShuffle, # 'Randomizes the dungeon that each dungeon entrance leads to'),
    'experimental_entrance_shuffle': EntranceShuffle,
    # 'bossshuffle': BossShuffle,
    # 'minibossshuffle': BossShuffle,
    'goal': Goal,
    'instrument_count': InstrumentCount,
    # 'itempool': ItemPool,
    # 'bowwow': Bowwow,
    # 'overworld': Overworld,
    'link_palette': LinkPalette,
    'trendy_game': TrendyGame,
    'gfxmod': GfxMod,
    'palette': Palette,
    'shuffle_nightmare_keys': ShuffleNightmareKeys,
    'shuffle_small_keys': ShuffleSmallKeys,
    'shuffle_maps': ShuffleMaps,
    'shuffle_compasses': ShuffleCompasses,
    'shuffle_stone_beaks': ShuffleStoneBeaks,
}
