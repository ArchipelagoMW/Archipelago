"""Compile a list of hints based on the settings."""

from __future__ import annotations

import json
from math import ceil, floor, sqrt
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, Tuple, Union
from randomizer.Enums.MoveTypes import MoveTypes

import randomizer.ItemPool as ItemPool
from randomizer.Enums.Events import Events
from randomizer.Enums.HintType import HintType
from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Maps import Maps
from randomizer.Enums.Regions import Regions
from randomizer.Enums.HintRegion import HintRegion, MEDAL_REWARD_REGIONS, HINT_REGION_PAIRING
from randomizer.Enums.Settings import (
    BananaportRando,
    ClimbingStatus,
    ProgressiveHintItem,
    ActivateAllBananaports,
    LogicType,
    MicrohintsEnabled,
    MoveRando,
    ShockwaveStatus,
    ShuffleLoadingZones,
    SpoilerHints,
    TrainingBarrels,
    WinConditionComplex,
    WrinklyHints,
    KongModels,
    SlamRequirement,
    HardBossesSelected,
)
from randomizer.Enums.Transitions import Transitions
from randomizer.Enums.Types import Types, BarrierItems
from randomizer.Enums.Switches import Switches
from randomizer.Enums.SwitchTypes import SwitchType
from randomizer.Lists.Item import ItemList
from randomizer.Lists.Location import PreGivenLocations, SharedShopLocations, TrainingBarrelLocations
from randomizer.Lists.MapsAndExits import GetMapId
from randomizer.Lists.PathHintTree import BuildPathHintTree
from randomizer.Lists.ShufflableExit import ShufflableExits
from randomizer.Lists.WrinklyHints import ClearHintMessages, hints
from randomizer.Patching.UpdateHints import UpdateHint
from randomizer.Patching.Library.Generic import plando_colors, IsItemSelected

if TYPE_CHECKING:
    from randomizer.Lists.WrinklyHints import HintLocation
    from randomizer.LogicClasses import Region
    from randomizer.Spoiler import Spoiler


class Hint:
    """Hint object for Wrinkly hint text."""

    def __init__(
        self,
        *,
        hint="",
        important=True,
        priority=1,
        kongs=[Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky],
        repeats=1,
        base=False,
        keywords=[],
        permitted_levels=[
            Levels.JungleJapes,
            Levels.AngryAztec,
            Levels.FranticFactory,
            Levels.GloomyGalleon,
            Levels.FungiForest,
            Levels.CrystalCaves,
            Levels.CreepyCastle,
        ],
        subtype="joke",
        joke=False,
        joke_defined=False,
    ) -> None:
        """Create wrinkly hint text object."""
        self.kongs = kongs.copy()
        self.hint = hint
        self.important = important
        self.priority = priority
        self.repeats = repeats
        self.base = base
        self.used = False
        self.was_important = important
        self.original_repeats = repeats
        self.original_priority = priority
        self.keywords = keywords.copy()
        self.permitted_levels = permitted_levels.copy()
        self.subtype = subtype
        self.joke = base
        if joke_defined:
            self.joke = joke

    def use_hint(self):
        """Set hint as used."""
        if self.repeats == 1:
            self.used = True
            self.repeats = 0
        else:
            self.repeats -= 1
            self.priority += 1

    def downgrade(self):
        """Downgrade hint status."""
        self.important = False


class MoveInfo:
    """Move Info for Wrinkly hint text."""

    def __init__(self, *, name="", kong="", move_type="", move_level=0, important=False) -> None:
        """Create move info object."""
        self.name = name
        self.kong = kong
        move_types = ["special", "slam", "gun", "ammo_belt", "instrument"]
        encoded_move_type = move_types.index(move_type)
        self.move_type = encoded_move_type
        self.move_level = move_level
        self.important = important
        ref_kong = kong
        if ref_kong == Kongs.any:
            ref_kong = Kongs.donkey
        self.item_key = {"move_type": move_type, "move_lvl": move_level - 1, "move_kong": ref_kong}


class StartingSpoiler:
    """Spoiler for overall seed info you need to know at the start."""

    def __init__(self, settings):
        """Create starting info spoiler with the seed settings."""
        self.krool_order = settings.krool_order.copy()
        self.helm_order = settings.kong_helm_order.copy()
        self.starting_kongs = settings.starting_kong_list.copy()
        self.starting_keys = [ItemList[key].name for key in settings.starting_key_list]
        self.starting_moves = []
        self.starting_moves_not_hintable = []
        self.starting_moves_woth_count = 0
        if settings.spoiler_include_level_order:
            self.level_order = [
                settings.level_order[1],
                settings.level_order[2],
                settings.level_order[3],
                settings.level_order[4],
                settings.level_order[5],
                settings.level_order[6],
                settings.level_order[7],
                settings.level_order[8],
            ]

    def toJSON(self):
        """Convert this object to JSON for the purposes of the spoiler log."""
        return json.dumps(self, default=lambda o: o.__dict__)


class LevelSpoiler:
    """Spoiler for a given level in spoiler-style hints."""

    def __init__(self, level_name):
        """Create level spoiler object info."""
        self.level_name = level_name
        self.vial_colors = []
        self.points = 0
        self.woth_count = 0

    def toJSON(self):
        """Convert this object to JSON for the purposes of the spoiler log."""
        return json.dumps(self, default=lambda o: o.__dict__)


hint_list = [
    Hint(hint="Did you know - Donkey Kong officially features in Donkey Kong 64.", important=False, base=True),
    Hint(
        hint="Fungi Forest was originally intended to be in the other N64 Rareware title, Banjo Kazooie.",
        important=False,
        base=True,
    ),
    Hint(
        hint="Holding up-left when trapped inside of a trap bubble will break you out of it without spinning your stick.",
        important=False,
        base=True,
    ),
    Hint(hint="Tiny Kong is the youngest sister of Dixie Kong.", important=False, base=True),
    Hint(hint="Mornin.", important=False, base=True),
    Hint(
        hint="Lanky Kong is the only kong with no canonical relation to the main Kong family tree.",
        important=False,
        base=True,
    ),
    Hint(
        hint="Despite the line in the DK Rap stating otherwise, Chunky is the kong who can jump highest in DK64.",
        important=False,
        base=True,
    ),
    Hint(
        hint="Despite the line in the DK Rap stating otherwise, Tiny is one of the two slowest kongs in DK64.",
        important=False,
        base=True,
    ),
    Hint(
        hint="If you fail the twelfth round of K. Rool, the game will dictate that K. Rool is victorious and end the fight.",
        important=False,
        base=True,
    ),
    Hint(
        hint="Donkey Kong 64 Randomizer started as a LUA Script in early 2019, evolving into a ROM Hack in 2021.",
        important=False,
        base=True,
    ),
    Hint(
        hint="The maximum in-game time that the vanilla file screen time can display is 1165 hours and 5 minutes.",
        important=False,
        base=True,
    ),
    Hint(hint="Chunky Kong is the brother of Kiddy Kong.", important=False, base=True),
    Hint(hint="Fungi Forest contains mushrooms.", important=False, base=True),
    Hint(hint="Igloos can be found in Crystal Caves.", important=False, base=True),
    Hint(hint="Frantic Factory has multiple floors where things can be found.", important=False, base=True),
    Hint(hint="Angry Aztec has so much sand, it's even in the wind.", important=False, base=True),
    Hint(hint="You can find a rabbit in Fungi Forest and in Crystal Caves.", important=False, base=True),
    Hint(hint="You can find a beetle in Angry Aztec and in Crystal Caves.", important=False, base=True),
    Hint(hint="You can find a vulture in Angry Aztec.", important=False, base=True),
    Hint(hint="You can find an owl in Fungi Forest.", important=False, base=True),
    Hint(hint="You can find two boulders in Jungle Japes", important=False, base=True),
    Hint(hint="To buy moves, you will need coins.", important=False, base=True),
    Hint(
        hint="You can change the music and sound effects volume in the sound settings on the main menu.",
        important=False,
        base=True,
    ),
    Hint(
        hint="Coin Hoard is a Monkey Smash game mode where players compete to collect the most coins.",
        important=False,
        base=True,
    ),
    Hint(
        hint="Capture Pad is a Monkey Smash game mode where players attempt to capture pads in different corners of the arena.",
        important=False,
        base=True,
    ),
    Hint(hint="I have nothing to say to you.", important=False, base=True),
    Hint(hint="I had something to tell you, but I forgot what it is.", important=False, base=True),
    Hint(hint="I don't know anything.", important=False, base=True),
    Hint(hint="I'm as lost as you are. Good luck!", important=False, base=True),
    Hint(hint="Wrinkly? Never heard of him.", important=False, base=True),
    Hint(
        hint="This is it. The peak of all randomizers. No other randomizer exists besides DK64 Randomizer where you can listen to the dk rap in its natural habitat while freeing Chunky Kong in Jungle Japes.",
        important=False,
        base=True,
    ),
    Hint(
        hint="Why do they call it oven when you of in the cold food of out hot eat the food?",
        important=False,
        base=True,
    ),
    Hint(
        hint="Wanna become famous? Buy followers, coconuts and donks at DK64Randomizer (DK64Randomizer . com)!",
        important=False,
        base=True,
    ),
    Hint(hint="What you gonna do, SpikeVegeta?", important=False, base=True),
    Hint(hint="You don't care? Just give it to me? Okay, here it is.", important=False, base=True),
    Hint(hint="Rumor has it this game was developed in a cave with only a box of scraps!", important=False, base=True),
    Hint(hint="BOINNG! BOINNG! The current time is: 8:01!", important=False, base=True),
    Hint(
        hint="If you backflip right before Chunky punches K. Rool, you must go into first person camera to face him before the punch.",
        important=False,
        base=True,
    ),
    Hint(
        hint="The barrier to \x08Hideout Helm\x08 can be cleared by obtaining \x04801 Golden Bananas\x04. It can also be cleared with fewer than that.",
        important=False,
        base=True,
    ),
    Hint(
        hint="It would be \x05foolish\x05 to \x04not save your spoiler logs\x04 from the dev site.",
        important=False,
        base=True,
    ),
    Hint(
        hint="\x04W\x04\x05O\x05\x06A\x06\x07H\x07\x08,\x08 \x04I\x04 \x05D\x05\x06R\x06\x07O\x07\x08P\x08\x04P\x04\x05E\x05\x06D\x06 \x07A\x07\x08L\x08\x04L\x04 \x05M\x05\x06Y\x06 \x07C\x07\x08R\x08\x04A\x04\x05Y\x05\x06O\x06\x07N\x07\x08S\x08\x04!\x04",
        important=False,
        base=True,
    ),
    Hint(hint="[[WOTB]]", important=False, base=True),
    Hint(
        hint="By using DK64Randomizer.com, users agree to release the developers from any claims, damages, bad seeds, or liabilities. Please exercise caution and randomizer responsibly.",
        important=False,
        base=True,
    ),
    Hint(
        hint="Bothered? I was bothered once. They put me in a barrel, a bonus barrel. A bonus barrel with beavers, and beavers make me bothered.",
        important=False,
        base=True,
    ),
    Hint(hint="Looking for useful information? Try looking at another hint.", important=False, base=True),
    Hint(
        hint="Can I interest you in some casino chips? They're tastefully decorated with Hunky Chunky.",
        important=False,
        base=True,
    ),
    Hint(hint="Have faith, beanlievers. Your time will come.", important=False, base=True),
    Hint(hint="I have horrible news. Your seed just got \x0510 percent worse.\x05", important=False, base=True),
    Hint(hint="Great news! Your seed just got \x0810 percent better!\x08", important=False, base=True),
    Hint(hint="This is not a joke hint.", important=False, base=True),
    Hint(hint="I'll get back to you after this colossal dump of blueprints.", important=False, base=True),
    Hint(
        hint="Something in the \x0dHalt! The remainder of this hint has been confiscated by the top Kop on the force.\x0d",
        important=False,
        base=True,
    ),
    Hint(hint="When I finish Pizza Tower, this hint will update.", important=False, base=True),
    Hint(
        hint="Will we see a sub hour seasonal seed? Not a chance. The movement is too optimized at this point. I expect at most 10-20 more seconds can be saved, maybe a minute with TAS.",
        important=False,
        base=True,
    ),
    Hint(hint="The dk64randomizer.com wiki has lots of helpful information about hints.", important=False, base=True),
    Hint(
        hint="If you're watching on YouTube, be sure to like, comment, subscribe, and smash that bell.",
        important=False,
        base=True,
    ),
    Hint(hint="I could really go for a hot dog right now.", important=False, base=True),
    Hint(hint="You can find statues of dinosnakes in Angry Aztec.", important=False, base=True),
    Hint(
        hint="If this seed was a channel point redemption, you have my condolences. If it wasn't, you have many options for victims.",
        important=False,
        base=True,
    ),
    Hint(
        hint="You wouldn't steal a coin. You wouldn't steal a banana. You wouldn't fail to report a bug to the devs.",
        important=False,
        base=True,
    ),
    Hint(hint="It's time to get your counting practice in: 1, 2, 3, 4, 5, 6, 9...", important=False, base=True),
]

kong_list = ["\x04Donkey\x04", "\x05Diddy\x05", "\x06Lanky\x06", "\x07Tiny\x07", "\x08Chunky\x08", "\x04Any kong\x04"]
colorless_kong_list = ["Donkey", "Diddy", "Lanky", "Tiny", "Chunky"]
kong_colors = ["\x04", "\x05", "\x06", "\x07", "\x08", "\x0c"]

kong_cryptic = [
    [
        "The kong who is bigger, faster and potentially stronger too",
        "The kong who fires in spurts",
        "The kong with a tie",
        "The kong who slaps their instrument to the jungle beat",
    ],
    [
        "The kong who can fly real high",
        "The kong who features in the first two Donkey Kong Country games",
        "The kong who wants to see red",
        "The kong who frees the only female playable kong",
    ],
    [
        "The kong who inflates like a balloon, just like a balloon",
        "The kong who waddles in his overalls",
        "The kong who has a cold race with an insect",
        "The kong who lacks style, grace but not a funny face",
    ],
    [
        "The kong who likes jazz",
        "The kong who shoots K. Rool's tiny toes",
        "The kong who has ammo that is light as a feather",
        "The kong who can shrink in size",
    ],
    [
        "The kong who is one hell of a guy",
        "The kong who can pick up boulders",
        "The kong who fights a blocky boss",
        "The kong who bows down to a dragonfly",
    ],
    ["Members of the DK Crew", "A specific set of relatives", "A number of playable characters"],
]

all_levels = [
    Levels.JungleJapes,
    Levels.AngryAztec,
    Levels.FranticFactory,
    Levels.GloomyGalleon,
    Levels.FungiForest,
    Levels.CrystalCaves,
    Levels.CreepyCastle,
]
level_colors = ["\x08", "\x04", "\x0c", "\x06", "\x07", "\x0a", "\x09", "\x05", "\x0b", "\x0d"]
level_list = [
    "Jungle Japes",
    "Angry Aztec",
    "Frantic Factory",
    "Gloomy Galleon",
    "Fungi Forest",
    "Crystal Caves",
    "Creepy Castle",
    "Hideout Helm",
    "DK Isles",
    "Cranky's Lab",
]
short_level_list = [
    "Japes",
    "Aztec",
    "Factory",
    "Galleon",
    "Forest",
    "Caves",
    "Castle",
    "Helm",
    "Isles",
    "Cranky's Lab",
]
vacation_levels_properties = [
    "Glorious Hills",
    "Arid Sands",
    "OSHA Violation Hotspot",
    "Murky Depths",
    "Blissful Greens",
    "Miners Paradise",
    "Haunted Architecture",
    "Timeless Corridors",
    "Undeniable Serenity",
    "Arcade Dwellers Paradise",
]

level_cryptic = [
    [
        "The level with a localized storm",
        "The level with a dirt mountain",
        "The level which has two retailers and no race",
    ],
    ["The level with four vases", "The level with two kongs cages", "The level with a spinning totem"],
    [
        "The level with a toy production facility",
        "The level with a tower of blocks",
        "The level with a game from 1981",
        "The level where you need two quarters to play",
    ],
    ["The level with the most water", "The level where you free a water dweller", "The level with stacks of gold"],
    [
        "The level with only two retailers and two races",
        "The level where night can be acquired at will",
        "The level with a nocturnal tree dweller",
    ],
    ["The level with two inches of water", "The level with two ice shields", "The level with an Ice Tomato"],
    [
        "The level with battlements",
        "The level with a dungeon, ballroom and a library",
        "The level with drawbridge and a moat",
    ],
    ["The timed level", "The level with no boss", "The level with no small bananas"],
]
level_cryptic_isles = level_cryptic.copy()
level_cryptic_isles.remove(level_cryptic_isles[-1])
level_cryptic_isles.append(["The hub world", "The world with DK's ugly mug on it", "The world with only a Cranky's Lab and Snide's HQ in it"])

level_cryptic_helm_isles = level_cryptic.copy()
level_cryptic_helm_isles.append(level_cryptic_isles[-1])

shop_owners = ["\x04Cranky\x04", "\x04Funky\x04", "\x04Candy\x04"]
shop_cryptic = [
    [
        "The shop owner with a walking stick",
        "The shop owner who is old",
        "The shop owner who is persistently grumpy",
        "The shop owner who resides near your Treehouse",
    ],
    [
        "The shop owner who has an armory",
        "The shop owner who has a banana on his shop",
        "The shop owner with sunglasses",
        "The shop owner who calls everyone Dude",
    ],
    [
        "The shop owner who is flirtatious",
        "The shop owner who is not present in Fungi Forest",
        "The shop owner who is not present in Jungle Japes",
        "The shop owner with blonde hair",
    ],
]

crankys_cryptic = ["a location out of this world", "a location 5000 points deep", "a mad scientist's laboratory"]

item_type_names = {
    Types.Blueprint: "\x06a kasplat\x06",
    Types.Fairy: "\x06a fairy\x06",
    Types.Crown: "\x06a battle arena\x06",
    Types.RainbowCoin: "\x06a dirt patch\x06",
    Types.CrateItem: "\x06a melon crate\x06",
    Types.Enemies: "\x06an enemy\x06",
    Types.Hint: "\x06a hint door\x06",
}
item_type_names_cryptic = {
    Types.Blueprint: ["a minion of K. Rool", "a shockwaving foe", "a colorfully haired henchman"],
    Types.Fairy: ["an aerial ace", "a bit of flying magic", "a Queenly representative"],
    Types.Crown: ["a contest of endurance", "a crowning achievement", "the visage of K. Rool"],
    Types.RainbowCoin: ["the initials of DK", "a muddy mess", "buried treasure"],
    Types.CrateItem: ["a bouncing box", "a breakable cube", "a crate of goodies"],
    Types.Enemies: ["a minor discouragement", "an obstacle along the way", "something found in mad maze maul"],
    Types.Hint: ["a source of a riddle", "the old granny house", "a door to the granny"],
}

moves_data = [
    # Commented out logic sections are saved if we need to revert to the old hint system
    # Donkey
    MoveInfo(name="Baboon Blast", move_level=1, move_type="special", kong=Kongs.donkey),
    MoveInfo(name="Strong Kong", move_level=2, move_type="special", kong=Kongs.donkey),
    MoveInfo(name="Gorilla Grab", move_level=3, move_type="special", kong=Kongs.donkey),
    # Diddy
    MoveInfo(name="Chimpy Charge", move_level=1, move_type="special", kong=Kongs.diddy),
    MoveInfo(name="Rocketbarrel Boost", move_level=2, move_type="special", kong=Kongs.diddy, important=True),  # (spoiler.settings.krool_diddy or spoiler.settings.helm_diddy)),
    MoveInfo(name="Simian Spring", move_level=3, move_type="special", kong=Kongs.diddy),
    # Lanky
    MoveInfo(name="Orangstand", move_level=1, move_type="special", kong=Kongs.lanky),
    MoveInfo(name="Baboon Balloon", move_level=2, move_type="special", kong=Kongs.lanky),
    MoveInfo(name="Orangstand Sprint", move_level=3, move_type="special", kong=Kongs.lanky),
    # Tiny
    MoveInfo(name="Mini Monkey", move_level=1, move_type="special", kong=Kongs.tiny, important=True),  # spoiler.settings.krool_tiny),
    MoveInfo(name="Ponytail Twirl", move_level=2, move_type="special", kong=Kongs.tiny),
    MoveInfo(name="Monkeyport", move_level=3, move_type="special", kong=Kongs.tiny, important=True),
    # Chunky
    MoveInfo(name="Hunky Chunky", move_level=1, move_type="special", kong=Kongs.chunky, important=True),  # spoiler.settings.krool_chunky),
    MoveInfo(name="Primate Punch", move_level=2, move_type="special", kong=Kongs.chunky, important=True),  # spoiler.settings.krool_chunky),
    MoveInfo(name="Gorilla Gone", move_level=3, move_type="special", kong=Kongs.chunky, important=True),  # spoiler.settings.krool_chunky),
    # Slam
    MoveInfo(name="Slam Upgrade", move_level=1, move_type="slam", kong=Kongs.any),
    MoveInfo(name="Slam Upgrade", move_level=2, move_type="slam", kong=Kongs.any),
    MoveInfo(name="Slam Upgrade", move_level=3, move_type="slam", kong=Kongs.any),
    # Guns
    MoveInfo(name="Coconut Shooter", move_level=1, move_type="gun", kong=Kongs.donkey, important=True),
    MoveInfo(name="Peanut Popguns", move_level=1, move_type="gun", kong=Kongs.diddy, important=True),  # spoiler.settings.krool_diddy),
    MoveInfo(name="Grape Shooter", move_level=1, move_type="gun", kong=Kongs.lanky),
    MoveInfo(name="Feather Bow", move_level=1, move_type="gun", kong=Kongs.tiny, important=True),  # spoiler.settings.krool_tiny),
    MoveInfo(name="Pineapple Launcher", move_level=1, move_type="gun", kong=Kongs.chunky),
    # Gun Upgrades
    MoveInfo(name="Homing Ammo", move_level=2, move_type="gun", kong=Kongs.any),
    MoveInfo(name="Sniper Scope", move_level=3, move_type="gun", kong=Kongs.any),
    # Ammo Belt
    MoveInfo(name="Ammo Belt Upgrade", move_level=1, move_type="ammo_belt", kong=Kongs.any),
    MoveInfo(name="Ammo Belt Upgrade", move_level=2, move_type="ammo_belt", kong=Kongs.any),
    # Instruments
    MoveInfo(name="Bongo Blast", move_level=1, move_type="instrument", kong=Kongs.donkey, important=True),  # spoiler.settings.helm_donkey),
    MoveInfo(name="Guitar Gazump", move_level=1, move_type="instrument", kong=Kongs.diddy, important=True),  # spoiler.settings.helm_diddy),
    MoveInfo(name="Trombone Tremor", move_level=1, move_type="instrument", kong=Kongs.lanky, important=True),  # (spoiler.settings.helm_lanky or spoiler.settings.krool_lanky)),
    MoveInfo(name="Saxophone Slam", move_level=1, move_type="instrument", kong=Kongs.tiny, important=True),  # spoiler.settings.helm_tiny),
    MoveInfo(name="Triangle Trample", move_level=1, move_type="instrument", kong=Kongs.chunky, important=True),  # spoiler.settings.helm_chunky),
    # Instrument Upgrades
    MoveInfo(name="Instrument Upgrade", move_level=2, move_type="instrument", kong=Kongs.any),
    MoveInfo(name="Instrument Upgrade", move_level=3, move_type="instrument", kong=Kongs.any),
    MoveInfo(name="Instrument Upgrade", move_level=4, move_type="instrument", kong=Kongs.any),
]

kong_placement_levels = [
    {"name": "Jungle Japes", "level": 0},
    {"name": "Llama Temple", "level": 1},
    {"name": "Tiny Temple", "level": 1},
    {"name": "Frantic Factory", "level": 2},
]

boss_names = {
    Maps.JapesBoss: "Army Dillo 1",
    Maps.AztecBoss: "Dogadon 1",
    Maps.FactoryBoss: "Mad Jack",
    Maps.GalleonBoss: "Pufftoss",
    Maps.FungiBoss: "Dogadon 2",
    Maps.CavesBoss: "Army Dillo 2",
    Maps.CastleBoss: "King Kut Out",
    Maps.KroolDonkeyPhase: "DK Phase",
    Maps.KroolDiddyPhase: "Diddy Phase",
    Maps.KroolLankyPhase: "Lanky Phase",
    Maps.KroolTinyPhase: "Tiny Phase",
    Maps.KroolChunkyPhase: "Chunky Phase",
}
boss_colors = {
    Maps.JapesBoss: "\x08",
    Maps.AztecBoss: "\x04",
    Maps.FactoryBoss: "\x0c",
    Maps.GalleonBoss: "\x06",
    Maps.FungiBoss: "\x07",
    Maps.CavesBoss: "\x0a",
    Maps.CastleBoss: "\x09",
    Maps.KroolDonkeyPhase: "\x04",
    Maps.KroolDiddyPhase: "\x05",
    Maps.KroolLankyPhase: "\x06",
    Maps.KroolTinyPhase: "\x07",
    Maps.KroolChunkyPhase: "\x08",
}

# Hint distribution that will be adjusted based on settings
# These values are "if this is an option, then you must have at least X of this hint"
hint_distribution_default = {
    HintType.Joke: 1,
    HintType.KRoolOrder: 1,
    HintType.HelmOrder: 1,  # must have one on the path
    HintType.MoveLocation: 7,  # must be placed before you can buy the move
    # HintType.DirtPatch: 0,
    HintType.BLocker: 0,  # must be placed on the path and before the level they hint
    HintType.TroffNScoff: 0,
    HintType.KongLocation: 1,  # must be placed before you find them and placed in a door of a free kong
    # HintType.MedalsRequired: 1,
    HintType.Entrance: 5,
    HintType.EntranceV2: 5,
    HintType.RequiredKongHint: -1,  # Fixed number based on the number of locked kongs
    HintType.RequiredKeyHint: -1,  # Fixed number based on the number of keys to be obtained over the seed
    HintType.RequiredWinConditionHint: 0,  # Fixed number based on what K. Rool phases you must defeat
    HintType.RequiredHelmDoorHint: 0,  # Fixed number based on how many Helm doors have random requirements
    HintType.WothLocation: 8,
    HintType.FullShopWithItems: 8,
    # HintType.FoolishMove: 0,  # Used to be 2, added to FoolishRegion when it was removed
    HintType.FoolishRegion: 3,
    HintType.ForeseenPathless: 0,
    HintType.Multipath: 0,
    HintType.RegionItemCount: 2,  # Also known as scouring hints
    HintType.ItemHinting: 0,
    HintType.Plando: 0,
    HintType.RequiredSlamHint: 1,  # Essentially the slam microhint placed on a door
}
HINT_CAP = 35  # There are this many total slots for hints

# The racing preset has a fixed hint distribution as follows - format should include all hint types to not throw errors
race_hint_distribution = {
    HintType.Joke: 0,
    HintType.KRoolOrder: 0,
    HintType.HelmOrder: 1,
    HintType.MoveLocation: 0,
    # HintType.DirtPatch: 0,
    HintType.BLocker: 0,
    HintType.TroffNScoff: 0,
    HintType.KongLocation: 0,
    # HintType.MedalsRequired: 0,
    HintType.Entrance: 0,
    HintType.EntranceV2: 0,
    HintType.RequiredKongHint: 3,
    HintType.RequiredKeyHint: 0,
    HintType.RequiredWinConditionHint: 0,
    HintType.RequiredHelmDoorHint: 0,
    HintType.WothLocation: 9,
    HintType.FullShopWithItems: 0,
    # HintType.FoolishMove: 0,
    HintType.FoolishRegion: 5,
    HintType.ForeseenPathless: 0,
    HintType.Multipath: 14,
    HintType.RegionItemCount: 3,
    HintType.ItemHinting: 0,
    HintType.Plando: 0,
    HintType.RequiredSlamHint: 0,
}

# The item-hinting distribution has a K. Rool hint, a Helm hint, and then every other hint will point to a move.
item_hint_distribution = {
    HintType.Joke: 0,
    HintType.KRoolOrder: 0,
    HintType.HelmOrder: 0,
    HintType.MoveLocation: 0,
    # HintType.DirtPatch: 0,
    HintType.BLocker: 0,
    HintType.TroffNScoff: 0,
    HintType.KongLocation: 0,
    # HintType.MedalsRequired: 0,
    HintType.Entrance: 0,
    HintType.EntranceV2: 0,
    HintType.RequiredKongHint: 0,
    HintType.RequiredKeyHint: 0,
    HintType.RequiredWinConditionHint: 0,
    HintType.RequiredHelmDoorHint: 0,
    HintType.WothLocation: 0,
    HintType.FullShopWithItems: 0,
    # HintType.FoolishMove: 0,
    HintType.FoolishRegion: 0,
    HintType.ForeseenPathless: 0,
    HintType.Multipath: 0,
    HintType.RegionItemCount: 0,
    HintType.ItemHinting: 35,
    HintType.Plando: 0,
    HintType.RequiredSlamHint: 0,
}

hint_reroll_cap = 2  # How many times are you willing to reroll a hinted location?
hint_reroll_chance = 1.0  # What % of the time (from 0-1) do you reroll in conditions that could trigger a reroll?
globally_hinted_location_ids = []


def compileHints(spoiler: Spoiler) -> bool:
    """Create a hint distribution, generate buff hints, and place them in locations."""
    replaceKongNameWithKrusha(spoiler)
    ClearHintMessages()
    hint_distribution = hint_distribution_default.copy()
    plando_hints_placed = 0
    if spoiler.settings.enable_plandomizer:
        plando_hints_placed = ApplyPlandoHints(spoiler)
        hint_distribution[HintType.Plando] = plando_hints_placed
    level_order_matters = spoiler.settings.logic_type != LogicType.nologic and spoiler.settings.shuffle_loading_zones != ShuffleLoadingZones.all
    globally_hinted_location_ids = []
    # Stores the number of hints each key will get
    key_hint_dict = {
        Items.JungleJapesKey: 0,
        Items.AngryAztecKey: 0,
        Items.FranticFactoryKey: 0,
        Items.GloomyGalleonKey: 0,
        Items.FungiForestKey: 0,
        Items.CrystalCavesKey: 0,
        Items.CreepyCastleKey: 0,
        Items.HideoutHelmKey: 0,
    }
    woth_key_ids = [
        spoiler.LocationList[woth_loc].item for woth_loc in spoiler.woth_locations if ItemList[spoiler.LocationList[woth_loc].item].type == Types.Key and woth_loc in spoiler.woth_paths.keys()
    ]
    # Precalculate the locations of the Keys - this info is used by distribution generation and hint generation
    key_location_ids = {}
    for location_id, location in spoiler.LocationList.items():
        if location.item in ItemPool.Keys():
            key_location_ids[location.item] = location_id

    # Some locations are particularly useless to hint
    useless_locations = {
        Items.HideoutHelmKey: [],
        Maps.KroolDonkeyPhase: [],
        Maps.KroolDiddyPhase: [],
        Maps.KroolLankyPhase: [],
        Maps.KroolTinyPhase: [],
        Maps.KroolChunkyPhase: [],
    }
    # Your training in Gorilla Gone, Monkeyport, Climbing and Vines are always pointless hints if Key 8 is in Helm, so let's not
    if spoiler.settings.key_8_helm and Locations.HelmKey in spoiler.woth_paths.keys():
        useless_moves = []
        if spoiler.settings.activate_all_bananaports != ActivateAllBananaports.isles_inc_helm_lobby:
            useless_moves.append(Items.Vines)
        if not spoiler.settings.switchsanity:
            useless_moves.append(Items.Monkeyport)
        if not spoiler.settings.switchsanity and spoiler.settings.activate_all_bananaports != ActivateAllBananaports.isles_inc_helm_lobby:
            useless_moves.append(Items.GorillaGone)
        useless_locations[Items.HideoutHelmKey] = [
            loc for loc in spoiler.woth_paths[Locations.HelmKey] if (loc in TrainingBarrelLocations or loc in PreGivenLocations) and spoiler.LocationList[loc].item in useless_moves
        ]
        useless_locations[Items.HideoutHelmKey].append(Locations.HelmKey)  # Also don't count the known location of the key itself
    # Your training in moves which you know are always needed beat the final battle are pointless to hint
    dk_phase_requirement = [Items.Climbing]
    chunky_phase_requirement = [Items.PrimatePunch, Items.HunkyChunky, Items.GorillaGone]
    if spoiler.settings.cannons_require_blast:
        dk_phase_requirement.append(Items.BaboonBlast)
    if spoiler.settings.chunky_phase_slam_req_internal != SlamRequirement.green:
        chunky_phase_requirement.append(Items.ProgressiveSlam)
    required_moves = {
        Maps.JapesBoss: [Items.Barrels],
        Maps.AztecBoss: [Items.Barrels],
        Maps.FactoryBoss: [Items.PonyTailTwirl],
        Maps.GalleonBoss: [],
        Maps.FungiBoss: [Items.Barrels, Items.HunkyChunky],
        Maps.CavesBoss: [Items.Barrels],
        Maps.CastleBoss: [],
        Maps.KroolDonkeyPhase: dk_phase_requirement,
        Maps.KroolDiddyPhase: [Items.Peanut, Items.RocketbarrelBoost],
        Maps.KroolLankyPhase: [Items.Barrels, Items.Trombone],
        Maps.KroolTinyPhase: [Items.Feather, Items.MiniMonkey],
        Maps.KroolChunkyPhase: chunky_phase_requirement,
    }
    if IsItemSelected(spoiler.settings.hard_bosses, spoiler.settings.hard_bosses_selected, HardBossesSelected.beta_lanky_phase, False):
        required_moves[Maps.KroolLankyPhase] = [Items.Barrels, Items.Grape]
    for map_id in required_moves:
        if map_id in spoiler.settings.krool_order and map_id in spoiler.krool_paths.keys():
            useless_locations[map_id] = [
                loc for loc in spoiler.krool_paths[map_id] if (loc in TrainingBarrelLocations or loc in PreGivenLocations) and spoiler.LocationList[loc].item in required_moves[map_id]
            ]

    multipath_dict_hints, multipath_dict_goals = GenerateMultipathDict(spoiler, useless_locations)

    locked_hint_types = [
        HintType.RequiredKongHint,
        HintType.RequiredKeyHint,
        HintType.RequiredWinConditionHint,
        HintType.RequiredHelmDoorHint,
        HintType.Multipath,
        HintType.ItemHinting,
        HintType.Plando,
        HintType.RequiredSlamHint,
    ]  # Some hint types cannot have their value changed... unless plando gets in the way
    maxed_hint_types = []  # Some hint types cannot have additional hints placed
    minned_hint_types = []  # Some hint types cannot have all their hints removed
    # If we're using the racing hints preset, we use the predetermined distribution with no exceptions
    if spoiler.settings.wrinkly_hints == WrinklyHints.fixed_racing:
        hint_distribution = race_hint_distribution.copy()
        # Extract plando hints from foolish hints - gotta pick something and I think these are the least impactful
        if spoiler.settings.enable_plandomizer:
            hint_distribution[HintType.Plando] = plando_hints_placed
            hint_distribution[HintType.FoolishRegion] -= plando_hints_placed
        # We know how many key path hints will be placed, now we need to distribute them reasonably
        key_difficulty_score = {}
        # Every woth key is guaranteed one
        for key_id in woth_key_ids:
            key_hint_dict[key_id] = 1
            path_length = len(spoiler.woth_paths[key_location_ids[key_id]])
            if key_id == Items.HideoutHelmKey:
                path_length -= len(useless_locations[Items.HideoutHelmKey])
            key_difficulty_score[key_id] = path_length  # The length of the path serves as a "score" for how much this key needs hints
        # Determine what keys can get more hints
        keys_eligible_for_more_hints = woth_key_ids.copy()
        # In simple level order, the Japes and Aztec keys will be treated as "early" keys and get direct hints - they get no more hints
        if level_order_matters and not spoiler.settings.hard_level_progression:
            if Items.JungleJapesKey in keys_eligible_for_more_hints:
                keys_eligible_for_more_hints.remove(Items.JungleJapesKey)
            if Items.AngryAztecKey in keys_eligible_for_more_hints:
                keys_eligible_for_more_hints.remove(Items.AngryAztecKey)
        # For each key hint we have left to place, find the "most unhinted" key and give that key another hint
        for i in range(hint_distribution[HintType.RequiredKeyHint] - len(woth_key_ids)):
            key_most_needing_hint = None
            most_unhinted_key_score = 1000  # Lower = needs hint more, should never be higher than 1
            for key_id in keys_eligible_for_more_hints:
                score = key_hint_dict[key_id] / key_difficulty_score[key_id]
                # If this score beats the previous score OR it ties and (has a longer path OR is a key found later in the seed), it is the new key most in need of a hint
                if score < most_unhinted_key_score or (score == most_unhinted_key_score and key_difficulty_score[key_id] >= key_difficulty_score[key_most_needing_hint]):
                    key_most_needing_hint = key_id
                    most_unhinted_key_score = score
            key_hint_dict[key_most_needing_hint] += 1  # Bless this key with an additional hint
    # If we're doing the item-hinting system, use that distribution
    elif spoiler.settings.wrinkly_hints in (WrinklyHints.item_hinting, WrinklyHints.item_hinting_advanced):
        hint_distribution = item_hint_distribution.copy()
        hint_distribution[HintType.ItemHinting] = HINT_CAP
        if spoiler.settings.enable_plandomizer:
            hint_distribution[HintType.Plando] = plando_hints_placed
            hint_distribution[HintType.ItemHinting] -= plando_hints_placed
        valid_types = [HintType.ItemHinting, HintType.Joke]
        # Build the list of valid hint types
        # If K. Rool is live it is guaranteed a hint in this distribution if it is not hinted otherwise via spoiler hints
        if (
            (spoiler.settings.krool_phase_count < 5 or spoiler.settings.krool_random)
            and spoiler.settings.win_condition_item == WinConditionComplex.beat_krool
            and spoiler.settings.spoiler_hints == SpoilerHints.off
        ):
            valid_types.append(HintType.KRoolOrder)
            hint_distribution[HintType.KRoolOrder] = 1
            hint_distribution[HintType.ItemHinting] -= 1
        # Helm order hint has been moved to Snide
        # If Helm is live it is guaranteed a hint in this distribution
        # if spoiler.settings.helm_setting != HelmSetting.skip_all and (spoiler.settings.helm_phase_count < 5 or spoiler.settings.helm_random):
        #     valid_types.append(HintType.HelmOrder)
        #     hint_distribution[HintType.HelmOrder] = 1
        #     hint_distribution[HintType.ItemHinting] -= 1
        # Each random Helm door is also guaranteed a hint
        if spoiler.settings.crown_door_random or spoiler.settings.coin_door_random:
            valid_types.append(HintType.RequiredHelmDoorHint)
            if spoiler.settings.crown_door_random:
                hint_distribution[HintType.RequiredHelmDoorHint] += 1
                hint_distribution[HintType.ItemHinting] -= 1
            if spoiler.settings.coin_door_random:
                hint_distribution[HintType.RequiredHelmDoorHint] += 1
                hint_distribution[HintType.ItemHinting] -= 1
        hint_distribution[HintType.ItemHinting] = max(0, hint_distribution[HintType.ItemHinting])
        # These filler hint types should never get added if you have enough moves placed in the world.
        # These would only be relevant if you picked this hint system and also started with a ton of moves which might error anyway. (Why would you ever do this?)
        if spoiler.settings.randomize_blocker_required_amounts and spoiler.settings.blocker_max > 1:
            valid_types.append(HintType.BLocker)
        if (
            spoiler.settings.randomize_cb_required_amounts
            and len(spoiler.settings.krool_keys_required) > 0
            and spoiler.settings.krool_keys_required != [Events.HelmKeyTurnedIn]
            and spoiler.settings.troff_max > 0
        ):
            valid_types.append(HintType.TroffNScoff)
        # We have at most 35 doors, we have to prioritize what item hints go in the doors.
        # List of locations to hint IN ORDER, starting from placing index 0 first, 1 second, and so on
        item_region_locations_to_hint = []
        kongs_to_hint = [kong for kong in ItemPool.Kongs(spoiler.settings) if ItemPool.GetKongForItem(kong) not in spoiler.settings.starting_kong_list]
        if spoiler.settings.shuffle_items and Types.Key in spoiler.settings.shuffled_location_types:
            item_region_locations_to_hint.extend([key_loc for key_loc in key_location_ids.values()])  # Keys you don't start with
            if spoiler.settings.key_8_helm and Locations.HelmKey in item_region_locations_to_hint:  # You may know that Key 8 is in Helm and that's pointless to hint
                item_region_locations_to_hint.remove(Locations.HelmKey)
        # Determine what moves are hintable
        all_hintable_moves = ItemPool.AllKongMoves() + ItemPool.TrainingBarrelAbilities() + kongs_to_hint
        if spoiler.settings.shockwave_status != ShockwaveStatus.start_with:
            all_hintable_moves.extend(ItemPool.ShockwaveTypeItems(spoiler.settings))
        if spoiler.settings.climbing_status != ClimbingStatus.normal:
            all_hintable_moves.extend(ItemPool.ClimbingAbilities())
        if spoiler.settings.shuffle_items:
            if Types.Bean in spoiler.settings.shuffled_location_types:
                all_hintable_moves.append(Items.Bean)
            if Types.Cranky in spoiler.settings.shuffled_location_types:
                all_hintable_moves.append(Items.Cranky)
            if Types.Funky in spoiler.settings.shuffled_location_types:
                all_hintable_moves.append(Items.Funky)
            if Types.Candy in spoiler.settings.shuffled_location_types:
                all_hintable_moves.append(Items.Candy)
            if Types.Snide in spoiler.settings.shuffled_location_types:
                all_hintable_moves.append(Items.Snide)
        optional_hintable_locations = []
        slam_locations = []
        # Loop through all locations, finding the location of all of these hintable moves
        for id, location in spoiler.LocationList.items():
            # Note the location of slams - these will always be at least optionally hintable and sometimes required to be hinted
            if location.item == Items.ProgressiveSlam:
                slam_locations.append(id)
            # Never hint training moves for obvious reasons
            if location.type in (Types.TrainingBarrel, Types.PreGivenMove, Types.Climbing, Types.Cranky, Types.Funky, Types.Candy, Types.Snide):
                continue
            # If it's a woth item, it must be hinted so put it in the list
            if id in spoiler.woth_locations:
                if location.item in kongs_to_hint:
                    item_region_locations_to_hint.insert(0, id)
                elif location.item in all_hintable_moves:
                    item_region_locations_to_hint.append(id)
            # To be hintable, it can't be a starting move
            elif location.item in all_hintable_moves:
                optional_hintable_locations.append(id)
        # Sort the locations we plan on hinting by the number of doors they have available - this should roughly place hints in order of importance
        item_region_locations_to_hint.sort(key=lambda loc_id: (len(spoiler.accessible_hints_for_location[loc_id]) if loc_id in spoiler.accessible_hints_for_location.keys() else 10000))
        # If there's room, always hint a slam if we haven't hinted one already
        hinted_slam_locations = [loc for loc in slam_locations if loc in item_region_locations_to_hint or spoiler.LocationList[loc].type in (Types.TrainingBarrel, Types.PreGivenMove, Types.Climbing)]
        if len(item_region_locations_to_hint) < hint_distribution[HintType.ItemHinting] and len(hinted_slam_locations) < 2:
            loc_to_hint = spoiler.settings.random.choice([loc for loc in slam_locations if loc not in hinted_slam_locations])
            item_region_locations_to_hint.append(loc_to_hint)
            optional_hintable_locations.remove(loc_to_hint)
        # Fill with other random move locations as best as we can
        spoiler.settings.random.shuffle(optional_hintable_locations)
        while len(item_region_locations_to_hint) < hint_distribution[HintType.ItemHinting] and len(optional_hintable_locations) > 0:
            item_region_locations_to_hint.append(optional_hintable_locations.pop())
        # If there's so many WotH things we can't hint them all, some WotH things will go unhinted. Unlucky.
        if len(item_region_locations_to_hint) > hint_distribution[HintType.ItemHinting]:
            too_many_count = len(item_region_locations_to_hint) - hint_distribution[HintType.ItemHinting]
            # That said, whatever goes unhinted probably shouldn't be something important
            less_important_location_ids = []
            for loc_id in item_region_locations_to_hint:
                # Don't remove hints to Kongs or Keys - the rest is fair game
                if ItemList[spoiler.LocationList[loc_id].item].type not in (Types.Kong, Types.Key):
                    less_important_location_ids.append(loc_id)
            # Randomly remove some of them so we don't bias towards early/late items - if you miss it, unlucky
            spoiler.settings.random.shuffle(less_important_location_ids)
            while too_many_count > 0:
                # If we can, remove less important moves first
                if len(less_important_location_ids) > 0:
                    item_region_locations_to_hint.remove(less_important_location_ids.pop())
                # Otherwise, tough luck - this is probably just for plando though
                else:
                    removed_hint = spoiler.settings.random.choice(item_region_locations_to_hint)
                    item_region_locations_to_hint.remove(removed_hint)
                too_many_count -= 1
        # If you start with a ton of moves, there may be only a handful of things to hint
        if len(item_region_locations_to_hint) < hint_distribution[HintType.ItemHinting]:
            hint_distribution[HintType.ItemHinting] = len(item_region_locations_to_hint)
        # Make sure we still have exactly 35 hints planned
        hint_count = 0
        for type in hint_distribution:
            if type in valid_types or type == HintType.Plando:
                hint_count += hint_distribution[type]
            else:
                hint_distribution[type] = 0
        # We may be over the cap if plando wills it
        while hint_count > HINT_CAP:
            # If we can find an unlocked valid hint type (I think this is impossible?), let's remove that
            unlocked_valid_hint_types = [typ for typ in valid_types if typ not in locked_hint_types and hint_distribution[typ] > 0]
            if len(unlocked_valid_hint_types) > 0:
                removed_type = spoiler.settings.random.choice(unlocked_valid_hint_types)
            # Otherwise, remove anything that isn't a Plando hint - hopefully this doesn't brick the hints!
            else:
                removed_type = spoiler.settings.random.choice([typ for typ in valid_types if hint_distribution[typ] > 0 and typ != HintType.Plando])
            hint_distribution[removed_type] -= 1
            hint_count -= 1
        # In some unusual cases we may be under the cap here - fill extra hints if we need them
        while hint_count < HINT_CAP:
            filler_type = spoiler.settings.random.choice(valid_types)
            if filler_type == HintType.Joke:
                # Make it roll joke twice to add an extra joke hint
                filler_type = spoiler.settings.random.choice(valid_types)
            if filler_type in locked_hint_types or filler_type in maxed_hint_types:
                continue  # Some hint types cannot be filled with
            hint_distribution[filler_type] += 1
            hint_count += 1
    # Otherwise we dynamically generate the hint distribution
    else:
        # In level order (or vanilla) progression, there are hints that we want to be in the player's path
        # Determine what hint types are valid for these settings
        valid_types = []
        if not spoiler.settings.serious_hints:
            valid_types.append(HintType.Joke)
        if spoiler.settings.randomize_blocker_required_amounts and spoiler.settings.blocker_max > 1:
            valid_types.append(HintType.BLocker)
        if (
            spoiler.settings.randomize_cb_required_amounts
            and len(spoiler.settings.krool_keys_required) > 0
            and spoiler.settings.krool_keys_required != [Events.HelmKeyTurnedIn]
            and spoiler.settings.troff_max > 0
        ):
            valid_types.append(HintType.TroffNScoff)
        if spoiler.settings.kong_rando:
            if spoiler.settings.shuffle_items and Types.Kong in spoiler.settings.shuffled_location_types:
                valid_types.append(HintType.RequiredKongHint)
                hint_distribution[HintType.RequiredKongHint] = 5 - spoiler.settings.starting_kongs_count
            else:
                valid_types.append(HintType.KongLocation)
        # if spoiler.settings.coin_door_open == "need_both" or spoiler.settings.coin_door_open == "need_rw":
        #     valid_types.append(HintType.MedalsRequired)
        if spoiler.settings.shuffle_loading_zones == ShuffleLoadingZones.all:
            # In entrance rando, we care more about T&S than B. Locker
            temp = hint_distribution[HintType.BLocker]
            if spoiler.settings.randomize_blocker_required_amounts and not spoiler.settings.maximize_helm_blocker:
                hint_distribution[HintType.BLocker] = max(1, hint_distribution[HintType.TroffNScoff])  # Always want a helm hint in there
            hint_distribution[HintType.TroffNScoff] = temp
            # V2 Entrance hints are only valid in full item rando where we have a proper WotH throughout the world
            if spoiler.settings.shuffle_items and Types.Shop in spoiler.settings.shuffled_location_types:
                valid_types.append(HintType.EntranceV2)
            # OG Entrance hints are still solid outside of item rando because they will point to whole levels
            else:
                valid_types.append(HintType.Entrance)
        # If K. Rool is live it can get one hint if it is not hinted otherwise via spoiler hints
        if (
            (spoiler.settings.krool_phase_count < 5 or spoiler.settings.krool_random)
            and spoiler.settings.win_condition_item == WinConditionComplex.beat_krool
            and spoiler.settings.spoiler_hints == SpoilerHints.off
        ):
            valid_types.append(HintType.KRoolOrder)
            maxed_hint_types.append(HintType.KRoolOrder)
            # If the seed doesn't funnel you into helm, guarantee one K. Rool order hint
            if Events.HelmKeyTurnedIn not in spoiler.settings.krool_keys_required or not spoiler.settings.key_8_helm:
                minned_hint_types.append(HintType.KRoolOrder)
        # Helm order hint has been moved to Snide
        # if spoiler.settings.helm_setting != HelmSetting.skip_all and (spoiler.settings.helm_phase_count < 5 or spoiler.settings.helm_random):
        #     valid_types.append(HintType.HelmOrder)
        #     locked_hint_types.append(HintType.HelmOrder)
        if spoiler.settings.move_rando not in (MoveRando.off, MoveRando.item_shuffle) and Types.Shop not in spoiler.settings.shuffled_location_types:
            valid_types.append(HintType.FullShopWithItems)
            valid_types.append(HintType.MoveLocation)
        if spoiler.settings.shuffle_items and Types.Shop in spoiler.settings.shuffled_location_types:
            starting_slam_count = 0
            for loc in TrainingBarrelLocations.union(PreGivenLocations):
                if spoiler.LocationList[loc].item == Items.ProgressiveSlam:
                    starting_slam_count += 1
            if starting_slam_count < 2:
                valid_types.append(HintType.RequiredSlamHint)
            # With no logic WOTH isn't built correctly so we can't make any hints with it
            if spoiler.settings.logic_type != LogicType.nologic:
                # If we're in full item rando with shops in the pool, we need to replace our bad filler with good filler
                # Get rid of the bad filler
                if HintType.BLocker in valid_types:
                    valid_types.remove(HintType.BLocker)
                if HintType.TroffNScoff in valid_types:
                    valid_types.remove(HintType.TroffNScoff)
                # Add the good filler
                valid_types.append(HintType.FoolishRegion)
                # If there are more foolish region hints than regions, lower this number and prevent more from being added
                if len(spoiler.foolish_region_names) < hint_distribution[HintType.FoolishRegion]:
                    hint_distribution[HintType.FoolishRegion] = len(spoiler.foolish_region_names)
                    maxed_hint_types.append(HintType.FoolishRegion)

                # valid_types.append(HintType.ForeseenPathless)
                # # If there are more pathless move hints than pathless moves, lower this number and prevent more from being added
                # if len(spoiler.pathless_moves) < hint_distribution[HintType.ForeseenPathless]:
                #     hint_distribution[HintType.ForeseenPathless] = len(spoiler.pathless_moves)
                #     maxed_hint_types.append(HintType.ForeseenPathless)

                valid_types.append(HintType.RegionItemCount)
                # If there are more region item count hints than regions containing moves (????), lower this number and prevent more from being added
                if len(spoiler.region_hintable_count.keys()) < hint_distribution[HintType.RegionItemCount]:
                    hint_distribution[HintType.RegionItemCount] = len(spoiler.region_hintable_count.keys())
                    maxed_hint_types.append(HintType.RegionItemCount)

                valid_types.append(HintType.WothLocation)
                # K. Rool seeds could use some help finding the last pesky moves
                if spoiler.settings.win_condition_item == WinConditionComplex.beat_krool:
                    valid_types.append(HintType.RequiredWinConditionHint)
                    # Count the number of non-trivial phases
                    hint_distribution[HintType.RequiredWinConditionHint] = len([kong for kong in spoiler.settings.krool_order if len(spoiler.krool_paths[kong]) - len(useless_locations[kong]) > 0])
                # Some win conditions need help finding the camera (if you don't start with it) - variable amount of unique hints for it
                if spoiler.settings.win_condition_item in (WinConditionComplex.req_fairy, WinConditionComplex.krem_kapture) and spoiler.settings.shockwave_status != ShockwaveStatus.start_with:
                    camera_location_id = None
                    for id, loc in spoiler.LocationList.items():
                        if loc.item in (Items.Camera, Items.CameraAndShockwave):
                            camera_location_id = id
                            break
                    # Don't make a Camera path hint if Camera isn't woth
                    if camera_location_id in spoiler.woth_paths.keys():
                        valid_types.append(HintType.RequiredWinConditionHint)
                        hint_distribution[HintType.RequiredWinConditionHint] = 1
        if spoiler.settings.crown_door_random or spoiler.settings.coin_door_random:
            valid_types.append(HintType.RequiredHelmDoorHint)
            if spoiler.settings.crown_door_random:
                hint_distribution[HintType.RequiredHelmDoorHint] += 1
            if spoiler.settings.coin_door_random:
                hint_distribution[HintType.RequiredHelmDoorHint] += 1
        # if spoiler.settings.random_patches:
        #     valid_types.append(HintType.DirtPatch)

        # There are no paths in no logic so multipath doesn't function
        if spoiler.settings.logic_type != LogicType.nologic:
            # Dynamically calculate the number of key hints that need to be placed per key. Any WotH keys should have paths that we should hint.
            if spoiler.settings.shuffle_items and len(woth_key_ids) > 0:
                valid_types.append(HintType.RequiredKeyHint)
                # Only guarantee hints for keys that are in the Way of the Hoard
                hint_distribution[HintType.RequiredKeyHint] = len(woth_key_ids)
            # Convert all path hints into multipath hints
            min_value = hint_distribution[HintType.RequiredWinConditionHint] + hint_distribution[HintType.RequiredKeyHint]
            hint_distribution[HintType.RequiredWinConditionHint] = 0
            hint_distribution[HintType.RequiredKeyHint] = 0
            if HintType.RequiredWinConditionHint in valid_types:
                valid_types.remove(HintType.RequiredWinConditionHint)
            if HintType.RequiredKeyHint in valid_types:
                valid_types.remove(HintType.RequiredKeyHint)
            # The number of multipath hints is a percentage of all eligible locations while still guaranteeing every goal gets at least one hint
            hint_distribution[HintType.Multipath] = max(len(multipath_dict_hints.keys()) * 0.59, min_value)
            # That percentage likely turns out a decimal - that decimal becomes a % chance to get an extra hint
            rng = spoiler.settings.random.random()
            if hint_distribution[HintType.Multipath] % 1 > rng:
                hint_distribution[HintType.Multipath] = ceil(hint_distribution[HintType.Multipath])
            else:
                hint_distribution[HintType.Multipath] = floor(hint_distribution[HintType.Multipath])
            # If we somehow have more multipath hints than there are locations, cap it (this should be impossible now?)
            if hint_distribution[HintType.Multipath] >= len(multipath_dict_hints.keys()):
                hint_distribution[HintType.Multipath] = len(multipath_dict_hints.keys())
                maxed_hint_types.append(HintType.Multipath)
            valid_types.append(HintType.Multipath)
            # Multipath hints are designed to passively hint your K. Rool order - you don't need it hinted directly in full
            if HintType.KRoolOrder in valid_types:
                valid_types.remove(HintType.KRoolOrder)
        # If somehow you threaded the needle with no valid hint types, you'll get joke hints whether you like it or not
        if len(valid_types) == 0:
            valid_types = [HintType.Joke]

        # Make sure we have exactly 35 hints placed
        hint_count = 0
        for type in hint_distribution:
            if type in valid_types or type == HintType.Plando:
                hint_count += hint_distribution[type]
            else:
                hint_distribution[type] = 0
        # Fill extra hints if we need them
        while hint_count < HINT_CAP:
            filler_type = spoiler.settings.random.choice(valid_types)
            if filler_type == HintType.Joke:
                # Make it roll joke twice to add an extra joke hint
                filler_type = spoiler.settings.random.choice(valid_types)
                if filler_type == HintType.Joke:
                    # Just kidding, make it roll joke thrice to add an extra joke hint
                    filler_type = spoiler.settings.random.choice(valid_types)
            if filler_type in locked_hint_types or filler_type in maxed_hint_types:
                continue  # Some hint types cannot be filled with
            hint_distribution[filler_type] += 1
            hint_count += 1
            # In theory, you could overload on multipath hints here, let's prevent that
            if filler_type == HintType.Multipath and hint_distribution[HintType.Multipath] >= len(multipath_dict_hints.keys()):
                maxed_hint_types.append(HintType.Multipath)
        # Remove random hints if we went over the cap
        while hint_count > HINT_CAP:
            # In many settings, you may have more required hints than you have doors
            locked_hint_count = sum([hint_distribution[typ] for typ in locked_hint_types]) + sum([hint_distribution[typ] for typ in minned_hint_types])
            # If this is the case (again, INSANELY rare) then you lose a random path hint
            if locked_hint_count > HINT_CAP:
                # Pull out path hints where possible - unlucky
                if HintType.Multipath in valid_types and hint_distribution[HintType.Multipath] > 0:
                    hint_distribution[HintType.Multipath] -= 1
                elif hint_distribution[HintType.RequiredKeyHint] > 0:
                    key_to_lose_a_hint = spoiler.settings.random.choice([key for key in key_hint_dict.keys() if key_hint_dict[key] > 0])
                    key_hint_dict[key_to_lose_a_hint] -= 1
                    hint_distribution[HintType.RequiredKeyHint] -= 1
                # We may have to remove a random required hint - this is highly unfortunate and hopefully should only happen in plando
                else:
                    # typ for typ in valid_types if hint_distribution[typ] > 0 and typ != HintType.Plando
                    removed_type = spoiler.settings.random.choice([typ for typ in valid_types if hint_distribution[typ] > 0 and typ != HintType.Plando])
                    hint_distribution[removed_type] -= 1
                hint_count -= 1
                continue
            # In all other cases, remove a random hint that is eligible to be removed
            removed_type = spoiler.settings.random.choice(valid_types)
            if removed_type in locked_hint_types:
                continue  # Some hint types cannot have fewer than specified by the settings
            if removed_type in minned_hint_types and hint_distribution[removed_type] == 1:
                continue  # Some hint types cannot have 0 hints if they're a possible hint type
            if hint_distribution[removed_type] > 0:
                hint_distribution[removed_type] -= 1
                hint_count -= 1

    progression_hint_locations = None
    if level_order_matters:
        # These hint locations are *much* more likely to be seen, as they'll be available as players pass through lobbies on their first visit
        progression_hint_locations = []
        for level in all_levels:
            for kong in spoiler.settings.owned_kongs_by_level[level]:
                # In hint door location rando, it's too complicated to determine if the door will be accessible on the first trip
                # Assume they'll see the hint doors for the kongs they have available
                # NOTE: this is a quick and dirty solution that can bury critical hints - better solution would be to set up accessible_hints_by_level array like moves/kongs
                if not spoiler.settings.wrinkly_location_rando:
                    # If we don't have DK + Grab then these hints are skipped basically every time so they're not on the player's path
                    if (
                        level == Levels.FranticFactory
                        and kong not in [Kongs.donkey, Kongs.chunky]
                        and (Kongs.donkey not in spoiler.settings.owned_kongs_by_level[level] or Items.GorillaGrab not in spoiler.settings.owned_moves_by_level[level])
                    ):
                        continue
                    if (
                        level == Levels.FungiForest
                        and kong is not Kongs.chunky
                        and (Kongs.donkey not in spoiler.settings.owned_kongs_by_level[level] or Items.GorillaGrab not in spoiler.settings.owned_moves_by_level[level])
                    ):
                        continue
                    # Caves Diddy needs a whole suite of moves to see this hint
                    if (
                        level == Levels.CrystalCaves
                        and kong is Kongs.diddy
                        and (
                            Kongs.chunky not in spoiler.settings.owned_kongs_by_level[level]
                            or Items.PrimatePunch not in spoiler.settings.owned_moves_by_level[level]
                            or Items.RocketbarrelBoost not in spoiler.settings.owned_moves_by_level[level]
                            or Items.Barrels not in spoiler.settings.owned_moves_by_level[level]
                        )
                    ):
                        continue
                    # Everyone else in Caves still needs Chunky + Punch + Barrels
                    if level == Levels.CrystalCaves and (
                        Kongs.chunky not in spoiler.settings.owned_kongs_by_level[level]
                        or Items.PrimatePunch not in spoiler.settings.owned_moves_by_level[level]
                        or Items.Barrels not in spoiler.settings.owned_moves_by_level[level]
                    ):
                        continue
                    # Aztec Chunky also needs Tiny + Feather + Hunky Chunky
                    if (
                        level == Levels.AngryAztec
                        and kong is Kongs.chunky
                        and (
                            Kongs.tiny not in spoiler.settings.owned_kongs_by_level[level]
                            or Items.Feather not in spoiler.settings.owned_moves_by_level[level]
                            or Items.HunkyChunky not in spoiler.settings.owned_moves_by_level[level]
                        )
                    ):
                        continue
                hint_for_location = [hint for hint in hints if hint.level == level and hint.kong == kong][0]  # Should only match one
                progression_hint_locations.append(hint_for_location)

    # Now place hints by type from most-restrictive to least restrictive. Usually anything we want on the player's path should get placed first
    # The required slam hint must go in a very specific door on progressive hints, so it must be placed first. Fortunately we're not likely to get conflicts for this door
    if hint_distribution[HintType.RequiredSlamHint] > 0:
        # If we're using hint doors, put it on a random hint door
        hint_location = getRandomHintLocation(random=spoiler.settings.random)
        # If we're using progressive hints, put it on the last hint
        if spoiler.settings.progressive_hint_item != ProgressiveHintItem.off:
            hint_location = [hint for hint in hints if hint.level == Levels.CreepyCastle and hint.kong == Kongs.chunky][0]
            if hint_location.hint_type == HintType.Plando:
                hint_location = getRandomHintLocation(random=spoiler.settings.random)
        # If hint_location is none, then there's no room for the slam hint. This is very likely plando's fault and intentionally done.
        if hint_location is not None:
            # Loop through locations looking for the slams - from prior calculations we can guarantee there are at least two in non-starting move locations
            slam_levels = []
            for id, location in spoiler.LocationList.items():
                if location.item == Items.ProgressiveSlam and id not in PreGivenLocations and id not in TrainingBarrelLocations:  # Ignore anything pre-given
                    if location.level not in slam_levels:
                        slam_levels.append(location.level)
            slam_levels.sort(key=lambda level: level.value)  # Sort the slam levels by vanilla level order so as to disguise any information from the traversal
            # Assemble a hint that resembles the microhint - only hint the levels the slams are in
            slam_text_entries = [f"{level_colors[x]}{level_list[x]}{level_colors[x]}" for x in slam_levels]
            slam_text = " or ".join(slam_text_entries)
            message = f"Still looking for some \x04super slam strength?\x04 Try looking in {slam_text}."
            hint_location.hint_type = HintType.RequiredSlamHint
            UpdateHint(hint_location, message)
    # Item rando kong hints are required and highly restrictive, only hinted to free kongs before (or as) the location is available
    if hint_distribution[HintType.RequiredKongHint] > 0:
        placed_requiredkonghints = 0
        # The length of this list should match hint_distribution[HintType.RequiredKongHint]
        kong_location_ids = [id for id, location in spoiler.LocationList.items() if location.item in (Items.Donkey, Items.Diddy, Items.Lanky, Items.Tiny, Items.Chunky)]
        for kong_location_id in kong_location_ids:
            # In some rare circumstances, you may not have enough hints allocated for all kongs - whoever you missed a hint for is sad and you should feel bad
            if placed_requiredkonghints >= hint_distribution[HintType.RequiredKongHint]:
                break
            kong_location = spoiler.LocationList[kong_location_id]
            hint_options = []
            # Attempt to find a door that will be accessible before the Kong
            if kong_location_id in spoiler.accessible_hints_for_location.keys():  # This will fail if the Kong is not WotH
                hint_options = getHintLocationsForAccessibleHintItems(spoiler.accessible_hints_for_location[kong_location_id])  # This will return [] if there are no hint doors available
            if len(hint_options) > 0:
                hint_location = spoiler.settings.random.choice(hint_options)
            # If there are no doors available early (very rare) or the Kong is not WotH (obscenely rare) then just get a random one. Tough luck.
            else:
                if spoiler.settings.progressive_hint_item != ProgressiveHintItem.off:  # In progressive hints we'll still stick the hint in the first 20 hints
                    hint_location = getRandomHintLocation(random=spoiler.settings.random, levels=[Levels.JungleJapes, Levels.AngryAztec, Levels.FranticFactory, Levels.GloomyGalleon])
                else:
                    hint_location = getRandomHintLocation(random=spoiler.settings.random)
            globally_hinted_location_ids.append(kong_location_id)
            freeing_kong_name = kong_list[kong_location.kong]
            if spoiler.settings.wrinkly_hints == WrinklyHints.cryptic:
                if kong_location.level == Levels.Shops:  # Exactly Jetpac
                    level_name = "\x08" + spoiler.settings.random.choice(crankys_cryptic) + "\x08"
                else:
                    level_name = "\x08" + spoiler.settings.random.choice(level_cryptic_helm_isles[kong_location.level]) + "\x08"
            else:
                if kong_location.level == Levels.Shops:  # Exactly Jetpac
                    level_name = "Cranky's Lab"
                else:
                    level_name = level_colors[kong_location.level] + level_list[kong_location.level] + level_colors[kong_location.level]
            freed_kong = kong_list[ItemPool.GetKongForItem(kong_location.item)]
            message = ""
            if kong_location.type in item_type_names.keys():
                location_name = item_type_names[kong_location.type]
                if spoiler.settings.wrinkly_hints == WrinklyHints.cryptic:
                    location_name = "\x06" + spoiler.settings.random.choice(item_type_names_cryptic[kong_location.type]) + "\x06"
                message = f"{freed_kong} is held by {location_name} in {level_name}."
            elif kong_location.type == Types.Shop:
                message = f"{freed_kong} can be bought in {level_name}."
            elif freeing_kong_name == freed_kong:
                grammar = "himself"
                if kong_location.kong == Kongs.tiny:
                    grammar = "herself"
                message = f"{freeing_kong_name} can be found by {grammar} in {level_name}? How odd..."
            else:
                message = f"{freed_kong} can be found by {freeing_kong_name} in {level_name}."
            hint_location.related_location = kong_location_id
            hint_location.hint_type = HintType.RequiredKongHint
            UpdateHint(hint_location, message)
            placed_requiredkonghints += 1
    # In non-item rando, Kongs should be hinted before they're available and should only be hinted to free Kongs, making them very restrictive
    hinted_kongs = []
    placed_kong_hints = 0
    while placed_kong_hints < hint_distribution[HintType.KongLocation]:
        kong_map = spoiler.settings.random.choice(kong_placement_levels)
        kong_index = spoiler.shuffled_kong_placement[kong_map["name"]]["locked"]["kong"]
        free_kong = spoiler.shuffled_kong_placement[kong_map["name"]]["puzzle"]["kong"]
        level_index = kong_map["level"]

        level_restriction = None
        # If this is the first time we're hinting this kong, attempt to put it in an earlier level (regardless of whether or not you can read it)
        # This only matters if level order matters
        if level_order_matters and kong_index not in hinted_kongs:
            level_restriction = [level for level in all_levels if spoiler.settings.BLockerEntryCount[level] <= spoiler.settings.BLockerEntryCount[kong_map["level"]]]
        # This list of free kongs is sometimes only a subset of the correct list. A more precise list could be calculated but it would be slow.
        free_kongs = spoiler.settings.starting_kong_list.copy()
        free_kongs.append(free_kong)
        hint_location = getRandomHintLocation(random=spoiler.settings.random, kongs=free_kongs, levels=level_restriction)
        # If this fails, it's extremely likely there's already a very useful hint in the very few spot(s) this could be
        if hint_location is None:
            if level_restriction is not None:
                # Can't make it too easy on em - put this hint in any hint door for these kongs
                hint_location = getRandomHintLocation(random=spoiler.settings.random, kongs=free_kongs)
            else:
                # In the unfathomably rare world where our freeing kong is out of hint doors, replace this hint with a joke hint
                # When I say unfathomably, I'm talking "you start with all moves and free B. Lockers but only 4 Kongs"
                hint_distribution[HintType.Joke] += 1  # Adding meme hints to meme seeds is just thematic at this point
                hint_distribution[HintType.KongLocation] -= 1
                continue

        if hint_location is not None:
            freeing_kong_name = kong_list[free_kong]
            if spoiler.settings.wrinkly_hints == WrinklyHints.cryptic:
                if not kong_index == Kongs.any:
                    kong_name = "\x07" + spoiler.settings.random.choice(kong_cryptic[kong_index]) + "\x07"
                level_name = "\x08" + spoiler.settings.random.choice(level_cryptic[level_index]) + "\x08"
            else:
                if not kong_index == Kongs.any:
                    kong_name = kong_list[kong_index]
                level_name = level_colors[level_index] + level_list[level_index] + level_colors[level_index]
            unlock_verb = "frees"
            if kong_index == Kongs.any:
                unlock_verb = "accesses"
                kong_name = "an empty cage"
            message = f"{freeing_kong_name} {unlock_verb} {kong_name} in {level_name}."
            hinted_kongs.append(kong_index)
            hint_location.hint_type = HintType.KongLocation
            UpdateHint(hint_location, message)
            placed_kong_hints += 1

    # B. Locker hints need to be on the player's path to be useful
    hinted_blocker_combos = []
    for i in range(hint_distribution[HintType.BLocker]):
        # If there's a specific level order to the seed, place the hints on the player's path so these hints aren't useless
        location_restriction = None
        if level_order_matters:
            location_restriction = progression_hint_locations
        # Pick random hint locations until we get one that can hint a future level
        hintable_levels = []
        while len(hintable_levels) == 0:
            hint_location = getRandomHintLocation(random=spoiler.settings.random, location_list=location_restriction)
            if hint_location is not None:
                # Only hint levels more expensive than the current one AND we care about level order AND this hint's lobby doesn't already hint this level
                hintable_levels = [
                    level
                    for level in all_levels
                    if (not level_order_matters or spoiler.settings.BLockerEntryCount[level] > spoiler.settings.BLockerEntryCount[hint_location.level])
                    and (hint_location.level, level) not in hinted_blocker_combos
                ]
                # If Helm is random, always place at least one Helm hint - this helps non-maximized Helm seeds and slightly nerfs this category of hints otherwise.
                if not spoiler.settings.maximize_helm_blocker:
                    if i == 0:
                        hintable_levels = [Levels.HideoutHelm]
                    else:
                        hintable_levels.append(Levels.HideoutHelm)
        hinted_level = spoiler.settings.random.choice(hintable_levels)
        hinted_blocker_combos.append((hint_location.level, hinted_level))
        level_name = level_colors[hinted_level] + level_list[hinted_level] + level_colors[hinted_level]
        if spoiler.settings.wrinkly_hints == WrinklyHints.cryptic:
            level_name = "\x08" + spoiler.settings.random.choice(level_cryptic[hinted_level]) + "\x08"
        message = f"The barrier to {level_name} can be cleared by obtaining \x04{spoiler.settings.BLockerEntryCount[hinted_level]} Golden Bananas\x04."
        hint_location.hint_type = HintType.BLocker
        UpdateHint(hint_location, message)

    # Item region hints take up a ton of hint doors, and some hints have restrictions on placement
    if hint_distribution[HintType.ItemHinting] > 0:
        # This array is arranged in such a way as to place the more important items to hint (kongs, keys, woth moves) first
        for loc_id in item_region_locations_to_hint:
            hint_location = None
            # If this hint does have hint door restrictions, attempt to abide by them. Items placed earlier are more likely to have restrictions, hence the rough order of hint placement.
            if loc_id in spoiler.accessible_hints_for_location.keys():
                hint_options = getHintLocationsForAccessibleHintItems(spoiler.accessible_hints_for_location[loc_id])
                if len(hint_options) > 0:
                    hint_location = spoiler.settings.random.choice(hint_options)
            # If this location's goals do not restrict hint door location OR all the restricted hint door options are taken (staggeringly unlikely), get a random hint door
            if hint_location is None or len(hint_options) == 0:
                level_limit = None
                # Limit our level options to the first 4 if we're on progressive hints and this is a Kong
                if ItemList[spoiler.LocationList[loc_id].item].type == Types.Kong and spoiler.settings.progressive_hint_item != ProgressiveHintItem.off:
                    level_limit = [Levels.JungleJapes, Levels.AngryAztec, Levels.FranticFactory, Levels.GloomyGalleon]
                hint_location = getRandomHintLocation(random=spoiler.settings.random, levels=level_limit)
            location = spoiler.LocationList[loc_id]
            item = ItemList[location.item]
            item_color = kong_colors[item.kong]  # Color based on the Kong of the item
            if item.type == Types.Key:  # Except Keys are gold
                item_color = kong_colors[Kongs.donkey]
            elif item.type == Types.Kong:  # Kong items are any kong items, but these make more intuitive sense as their respective color
                item_color = kong_colors[ItemPool.GetKongForItem(location.item)]
            item_name = item.name
            # In advanced item hinting hints, hint a category of the item, not the exact item.
            if spoiler.settings.wrinkly_hints == WrinklyHints.item_hinting_advanced:
                if item.type == Types.Kong:
                    item_name = "kongs"
                    item_color = kong_colors[Kongs.donkey]  # Genericize the color to be even more vague
                elif item.type == Types.Key:
                    item_name = "keys"
                elif item.type == Types.Shockwave:
                    item_name = "fairy moves"
                    item_color = "\x06"
                elif item.type in (Types.TrainingBarrel, Types.Climbing):
                    item_name = "training moves"
                elif item.type in (Types.Cranky, Types.Funky, Types.Candy, Types.Snide):
                    item_name = "shopkeepers"
                elif item.type == Types.Shop:
                    if item.kong == Kongs.any:
                        item_name = "shared kong moves"
                    else:
                        # 50/50 chance for kong moves to either...
                        coin_flip = spoiler.settings.random.choice([1, 2])
                        if coin_flip == 1:
                            # Hint the kong the move belongs to
                            item_name = colorless_kong_list[item.kong] + " moves"
                        else:
                            # Hint the type of move it is
                            item_color = kong_colors[Kongs.donkey]  # Genericize the color to be even more vague
                            if item.movetype == MoveTypes.Guns:
                                item_name = "guns"
                            elif item.movetype == MoveTypes.Instruments:
                                item_name = "instruments"
                            elif location.item in (
                                Items.GorillaGrab,
                                Items.ChimpyCharge,
                                Items.Orangstand,
                                Items.PonyTailTwirl,
                                Items.PrimatePunch,
                            ):
                                item_name = "active kong moves"
                            elif location.item in (
                                Items.StrongKong,
                                Items.RocketbarrelBoost,
                                Items.OrangstandSprint,
                                Items.MiniMonkey,
                                Items.HunkyChunky,
                            ):
                                item_name = "kong barrel moves"
                            elif location.item in (
                                Items.BaboonBlast,
                                Items.SimianSpring,
                                Items.BaboonBalloon,
                                Items.Monkeyport,
                                Items.GorillaGone,
                            ):
                                item_name = "kong pad moves"
            message = f"Looking for {item_color}{item_name}{item_color}?"
            # If this hint tries to offer help finding Krusha, make sure to get his name right
            if item.type == Types.Kong and spoiler.settings.wrinkly_hints != WrinklyHints.item_hinting_advanced:
                settings_values = [
                    spoiler.settings.kong_model_dk,
                    spoiler.settings.kong_model_diddy,
                    spoiler.settings.kong_model_lanky,
                    spoiler.settings.kong_model_tiny,
                    spoiler.settings.kong_model_chunky,
                ]
                for index, val in enumerate(settings_values):
                    if val == KongModels.krusha:
                        if ItemPool.GetKongForItem(location.item) == index:
                            message = message.replace(item.name, "Krusha")
            # Two options for hinting the location, do a coin flip
            coin_flip = spoiler.settings.random.choice([1, 2])
            if coin_flip == 1:
                # Option A: hint the region the item is in
                region = spoiler.RegionList[GetRegionIdOfLocation(spoiler, loc_id)]
                if not region.isCBRegion():
                    hinted_location_text = level_colors[region.level] + region.getHintRegionName() + level_colors[region.level]
                    message += f" Try looking in the {hinted_location_text}."
                else:
                    hinted_location_text = level_colors[region.level] + level_list[location.level] + level_colors[region.level]
                    message += f" Try collecting colored bananas in {hinted_location_text}."
            else:
                # Option B: hint the kong + level the item is in, using similar systems as other hints to instead hint kasplats/shops/specific types of items
                level_color = level_colors[location.level]
                if location.type in item_type_names.keys():
                    message += f" Seek {item_type_names[location.type]} in {level_color}{level_list[location.level]}{level_color}."
                elif location.type == Types.Shop:
                    message += f" Seek shops in {level_color}{level_list[location.level]}{level_color}."
                else:
                    message += f" Try looking in {level_color}{level_list[location.level]}{level_color} with {kong_list[location.kong]}."
            hint_location.related_location = loc_id
            hint_location.hint_type = HintType.ItemHinting
            UpdateHint(hint_location, message)

    # Multipath hints have some complicated restrictions on placement
    if hint_distribution[HintType.Multipath] > 0:
        hinted_path_locations = []
        # Ensure one location from each key's path is to be hinted to guarantee that goal gets a hint
        for key_id in woth_key_ids:
            # Determine if any location we're already hinting is on the path to this key
            hinted_locations_on_this_path = set(spoiler.woth_paths[key_location_ids[key_id]]) & set(hinted_path_locations)
            # If we haven't hinted anything on this path, pick something
            if not any(hinted_locations_on_this_path):
                location_options = [loc for loc in spoiler.woth_paths[key_location_ids[key_id]] if loc in multipath_dict_hints.keys()]
                # If there are no valid options, that means everything on this path is either worthless to hint or already hinted, so we're good
                if len(location_options) != 0:
                    # Otherwise pick a random location on this path - this guarantees each Key has at least one hint in its direction
                    location_to_hint = spoiler.settings.random.choice(location_options)
                    hinted_path_locations.append(location_to_hint)
        # If K. Rool is our goal, do the same with K. Rool phases
        if spoiler.settings.win_condition_item == WinConditionComplex.beat_krool:
            for kong in spoiler.krool_paths.keys():
                # Determine if any location we're already hinting is on the path to this phase of K. Rool
                hinted_locations_on_this_path = set(spoiler.krool_paths[kong]) & set(hinted_path_locations)
                # If we haven't hinted anything on this path, pick something
                if not any(hinted_locations_on_this_path):
                    location_options = [loc for loc in spoiler.krool_paths[kong] if loc in multipath_dict_hints.keys()]
                    # If there are no valid options, that means everything on this path is worthless to hint/already hinted or there's nothing on the path at all (Donkey...) so we're good
                    if len(location_options) != 0:
                        # Otherwise pick a random location on this path - this guarantees each K. Rool phase has at least one hint in its direction
                        location_to_hint = spoiler.settings.random.choice(location_options)
                        hinted_path_locations.append(location_to_hint)
        # If the camera is critical to the win condition, guarantee one path hint for it
        if spoiler.settings.win_condition_item in (WinConditionComplex.req_fairy, WinConditionComplex.krem_kapture) and spoiler.settings.shockwave_status != ShockwaveStatus.start_with:
            # Find the camera's location
            camera_location_id = None
            for location_id in multipath_dict_hints.keys():
                if spoiler.LocationList[location_id].item in (Items.Camera, Items.CameraAndShockwave):
                    camera_location_id = location_id
                    break
            # If we found the camera in a hintable location, ensure that we have at least one hint for it
            if camera_location_id is not None:
                # Determine if any location we're already hinting is on the path to the camera
                hinted_locations_on_this_path = set(spoiler.woth_paths[camera_location_id]) & set(hinted_path_locations)
                # If we haven't hinted anything on this path, pick something
                if not any(hinted_locations_on_this_path):
                    location_options = [loc for loc in spoiler.woth_paths[camera_location_id] if loc in multipath_dict_hints.keys()]
                    # If there are no valid options, that means everything on this path is worthless to hint (but I don't think the camera interacts with this)
                    if len(location_options) != 0:
                        # Otherwise pick a random location on this path - this guarantees the camera has at least one hint in its direction
                        location_to_hint = spoiler.settings.random.choice(location_options)
                        hinted_path_locations.append(location_to_hint)
        # If we attempt to hint more locations than the distribution allows for, we'll error
        # This should only happen if we're plandoing a ton of hints
        if len(hinted_path_locations) > hint_distribution[HintType.Multipath]:
            # We have to randomly choose from what we want to hint - if this culls some endpoints out of being hinted, so be it
            hinted_path_locations = spoiler.settings.random.sample(hinted_path_locations, hint_distribution[HintType.Multipath])
        # pick randomly from remaining locations in the keys to the multipath dict
        while len(hinted_path_locations) < hint_distribution[HintType.Multipath]:
            location_to_hint = spoiler.settings.random.choice([loc for loc in multipath_dict_hints.keys() if loc not in hinted_path_locations])
            hinted_path_locations.append(location_to_hint)
        # When placing hints, go from start to finish by woth_locations - this *roughly* places hints in most-restricted to least-restricted order
        for loc in spoiler.woth_locations:
            if loc not in hinted_path_locations:
                continue
            hint_location = None
            # When choosing hint location, consider ALL goals when restricting location choice
            goal_hint_options = set()  # This represents the set of accessible hint items without acquiring any goals this item is on the path to
            for goal_location in [goal for goal in multipath_dict_goals[loc] if goal in spoiler.accessible_hints_for_location.keys()]:
                if len(goal_hint_options) == 0:
                    goal_hint_options = set(spoiler.accessible_hints_for_location[goal_location])
                else:
                    goal_hint_options = goal_hint_options & set(spoiler.accessible_hints_for_location[goal_location])
            # The best hint doors for this item are the ones that are accessible without this item
            # It isn't necessary to put the hint in one of these, as you still receive valuable information from a multipath hint either way,
            # but it is much nicer to the player to put the hint in an accessible door
            premier_hint_location_options = getHintLocationsForAccessibleHintItems(spoiler.accessible_hints_for_location[loc])
            if len(premier_hint_location_options) > 0:
                hint_location = spoiler.settings.random.choice(premier_hint_location_options)
            # If there isn't a premier hint location available, we should still respect this location's goals
            elif len(goal_hint_options) > 0:
                hint_options = getHintLocationsForAccessibleHintItems(goal_hint_options)
                if len(hint_options) > 0:
                    hint_location = spoiler.settings.random.choice(hint_options)
            # If this the previous approach failed to get a hint door (staggeringly unlikely) or the item doesn't lock any goals, get a random hint door
            if hint_location is None:
                hint_location = getRandomHintLocation(random=spoiler.settings.random)

            globally_hinted_location_ids.append(loc)
            message = GenerateMultipathHintMessageForLocation(spoiler, loc, multipath_dict_hints)
            hint_location.related_location = loc
            hint_location.hint_type = HintType.Multipath
            UpdateHint(hint_location, message)
            if IsMultipathHintTooLong(message):
                hint_location.short_hint = GenerateMultipathHintMessageForLocation(spoiler, loc, multipath_dict_hints, shortenText=True)

    # Key location hints should be placed at or before the level they are for (e.g. Key 4 shows up in level 4 lobby or earlier)
    if hint_distribution[HintType.RequiredKeyHint] > 0:
        placed_requiredkeyhints = 0
        for key_id in key_hint_dict:
            # In some rare circumstances, you may not have enough hints allocated for all keys - probably not a problem cause these hints aren't real anymore
            if placed_requiredkeyhints >= hint_distribution[HintType.RequiredKeyHint]:
                break
            if key_hint_dict[key_id] == 0:
                continue
            # For early Keys 1-2, place one hint with their required Kong and the level they're in
            if key_id in (Items.JungleJapesKey, Items.AngryAztecKey) and level_order_matters and not spoiler.settings.hard_level_progression:
                globally_hinted_location_ids.append(key_location_ids[key_id])
                location = spoiler.LocationList[key_location_ids[key_id]]
                key_item = ItemList[key_id]
                kong_index = location.kong
                # Boss locations actually have a specific kong, go look it up
                if location.kong == Kongs.any and location.type == Types.Key and location.level != Levels.HideoutHelm:
                    kong_index = spoiler.settings.boss_kongs[location.level]
                if spoiler.settings.wrinkly_hints == WrinklyHints.cryptic:
                    if location.level == Levels.Shops:
                        level_name = "\x08" + spoiler.settings.random.choice(crankys_cryptic) + "\x08"
                    else:
                        level_name = "\x08" + spoiler.settings.random.choice(level_cryptic_helm_isles[location.level]) + "\x08"
                    kong_name = "\x07" + spoiler.settings.random.choice(kong_cryptic[kong_index]) + "\x07"
                else:
                    level_name = level_colors[location.level] + level_list[location.level] + level_colors[location.level]
                    kong_name = kong_list[kong_index]
                # Attempt to find a door that will be accessible before the Key
                hint_options = getHintLocationsForAccessibleHintItems(spoiler.accessible_hints_for_location[key_location_ids[key_id]])
                if len(hint_options) > 0:
                    hint_location = spoiler.settings.random.choice(hint_options)
                # If there are no doors available (pretty unlikely) then just get a random one. Tough luck.
                else:
                    hint_location = getRandomHintLocation(random=spoiler.settings.random)
                if location.type in item_type_names.keys():
                    location_name = item_type_names[location.type]
                    if spoiler.settings.wrinkly_hints == WrinklyHints.cryptic:
                        location_name = "\x06" + spoiler.settings.random.choice(item_type_names_cryptic[location.type]) + "\x06"
                    message = f"\x04{key_item.name}\x04 is held by {location_name} in {level_name}."
                elif location.type == Types.Shop:
                    message = f"\x04{key_item.name}\x04 can be bought in {level_name}."
                else:
                    message = f"\x04{key_item.name}\x04 can be acquired with {kong_name} in {level_name}."
                hint_location.related_location = key_location_ids[key_id]
                hint_location.hint_type = HintType.RequiredKeyHint
                UpdateHint(hint_location, message)
                placed_requiredkeyhints += 1
            # For later or complex Keys, place hints that hint the "path" to the key
            else:
                # Prevent the same hint referring to the same location twice
                # This means if you get a duplicate path hint, each hint refers to a different item
                already_hinted_locations = []
                for i in range(key_hint_dict[key_id]):
                    path = spoiler.woth_paths[key_location_ids[key_id]]
                    key_item = ItemList[key_id]
                    # Don't hint the Helm Key in Helm when you know it's there
                    if key_id == Items.HideoutHelmKey and spoiler.settings.key_8_helm:
                        path = [loc for loc in path if loc != Locations.HelmKey]
                    # Never hint the same location for the same path twice and avoid useless locations for Key 8 (if applicable)
                    hintable_location_ids = [loc for loc in path if loc not in already_hinted_locations and not (key_id == Items.HideoutHelmKey and loc in useless_locations[Items.HideoutHelmKey])]
                    path_location_id = spoiler.settings.random.choice(hintable_location_ids)
                    # Soft reroll duplicate hints based on hint reroll parameters
                    rerolls = 0
                    while rerolls < hint_reroll_cap and path_location_id in globally_hinted_location_ids and spoiler.settings.random.random() <= hint_reroll_chance:
                        path_location_id = spoiler.settings.random.choice(hintable_location_ids)
                        rerolls += 1
                    # After this point, the path_location_id is locked in and cannot be changed!

                    globally_hinted_location_ids.append(path_location_id)
                    already_hinted_locations.append(path_location_id)
                    region = spoiler.RegionList[GetRegionIdOfLocation(spoiler, path_location_id)]
                    hinted_location_text = level_colors[region.level] + region.getHintRegionName() + level_colors[region.level]
                    # Attempt to find a door that will be accessible before the Key
                    hint_options = getHintLocationsForAccessibleHintItems(spoiler.accessible_hints_for_location[key_location_ids[key_id]])
                    if len(hint_options) > 0:
                        hint_location = spoiler.settings.random.choice(hint_options)
                    # If there are no doors available (very unlikely) then just get a random one. Tough luck.
                    else:
                        hint_location = getRandomHintLocation(random=spoiler.settings.random)
                    if path_location_id in TrainingBarrelLocations or path_location_id in PreGivenLocations:
                        # Starting moves could be a lot of things - instead of being super vague we'll hint the specific item directly.
                        hinted_item_name = ItemList[spoiler.LocationList[path_location_id].item].name
                        message = f"\x0b{hinted_item_name}\x0b is on the path to \x04{key_item.name}\x04."
                    elif region.isCBRegion():
                        # Medal rewards and bosses are treated as "collecting colored bananas" for their region
                        hinted_location_text = f"{level_colors[region.level]}{short_level_list[region.level]} Colored Bananas{level_colors[region.level]}"
                        message = f"Something about collecting {hinted_location_text} is on the path to \x04{key_item.name}\x04."
                    else:
                        message = f"Something in the {hinted_location_text} is on the path to \x04{key_item.name}\x04."
                    hint_location.related_location = path_location_id
                    hint_location.hint_type = HintType.RequiredKeyHint
                    UpdateHint(hint_location, message)
                    placed_requiredkeyhints += 1

    # Some win conditions need very specific items that we really should hint
    # Path hints have been obsoleted by Multipath hints - if we ever undo that here's a todo list:
    # - Prevent 35 plando hints from causing problems here (I don't think it will, but double check it)
    if hint_distribution[HintType.RequiredWinConditionHint] > 0:
        # To aid K. Rool goals create a number of path hints to help find items required specifically for K. Rool
        if spoiler.settings.win_condition_item == WinConditionComplex.beat_krool:
            path = spoiler.woth_paths[Locations.BananaHoard]
            already_chosen_krool_path_locations = []
            chosen_krool_path_location_cap = hint_distribution[HintType.RequiredWinConditionHint]
            while len(already_chosen_krool_path_locations) < chosen_krool_path_location_cap:
                hintable_location_ids = [loc for loc in path if loc not in already_chosen_krool_path_locations and loc != Locations.BananaHoard]
                if len(hintable_location_ids) == 0 and spoiler.settings.wrinkly_hints == WrinklyHints.fixed_racing:
                    # This rarely happens when you're on a fixed hint distribution - some specific fills can have fewer items on the path to K. Rool than you have dedicated hints for
                    # It could also happen if you start with a ton of moves
                    hint_location = getRandomHintLocation(random=spoiler.settings.random)
                    hint_location.hint_type = HintType.RequiredWinConditionHint
                    message = "\x05Very little\x05 is on the path to \x0ddefeating K. Rool.\x0d"  # So we'll hint exactly that - there's very little on the path to K. Rool
                    UpdateHint(hint_location, message)
                    chosen_krool_path_location_cap -= 1  # This is a K. Rool hint, but isn't a location so we have to lower the cap on the loop
                    continue
                path_location_id = spoiler.settings.random.choice(hintable_location_ids)
                # Soft reroll duplicate hints based on hint reroll parameters
                rerolls = 0
                while rerolls < hint_reroll_cap and path_location_id in globally_hinted_location_ids and spoiler.settings.random.random() <= hint_reroll_chance:
                    path_location_id = spoiler.settings.random.choice(hintable_location_ids)
                    rerolls += 1
                # After this point, the path_location_id is locked in and cannot be changed!

                # Determine what phases this item could be for
                phases_needing_this_item = [map_id for map_id in spoiler.krool_paths.keys() if path_location_id in spoiler.krool_paths[map_id]]  # All phases this item is on the path to
                useless_kongs = [
                    kong for kong in phases_needing_this_item if path_location_id in useless_locations[kong]
                ]  # All kongs that it would be useless to hint for (e.g. Training in Peanut is path to Diddy K. Rool)
                hintable_phases = [kong for kong in phases_needing_this_item if kong not in useless_kongs]
                # If there are no valid phases to hint for this location, it's a training barrel with no useful information
                if len(hintable_phases) == 0:
                    # Therefore, we treat it as hinted and go again - this may lead to more often "very little is on the path" hints but that's fine cause it's still true
                    already_chosen_krool_path_locations.append(path_location_id)
                    chosen_krool_path_location_cap += 1  # Increment this by one so we go through the loop an extra time and don't lose a hint
                    continue
                hinted_kong = spoiler.settings.random.choice(hintable_phases)
                hinted_item_id = spoiler.LocationList[path_location_id].item
                # Every hint door is available before K. Rool so we can pick randomly...
                hint_location = getRandomHintLocation(random=spoiler.settings.random)
                # ...unless the hinted location is specifically the end of a phase path - in this case, we do not want the hint to lock itself
                if (
                    (hinted_kong == Kongs.diddy and hinted_item_id in (Items.Peanut, Items.RocketbarrelBoost))
                    or (hinted_kong == Kongs.lanky and hinted_item_id in (Items.Barrels, Items.Trombone))
                    or (hinted_kong == Kongs.tiny and hinted_item_id in (Items.Feather, Items.MiniMonkey))
                    or (hinted_kong == Kongs.chunky and hinted_item_id in (Items.ProgressiveSlam, Items.PrimatePunch, Items.HunkyChunky, Items.GorillaGone))
                ):
                    hint_options = getHintLocationsForAccessibleHintItems(spoiler.accessible_hints_for_location[path_location_id])
                    # If no hint options are available (this should be quite unlikely), it will default to the random one
                    if len(hint_options) > 0:
                        hint_location = spoiler.settings.random.choice(hint_options)
                globally_hinted_location_ids.append(path_location_id)
                already_chosen_krool_path_locations.append(path_location_id)
                # Begin to build the hint - determine the region of the location
                region = spoiler.RegionList[GetRegionIdOfLocation(spoiler, path_location_id)]
                hinted_location_text = level_colors[region.level] + region.getHintRegionName() + level_colors[region.level]
                kong_color = kong_colors[hinted_kong]
                if path_location_id in TrainingBarrelLocations or path_location_id in PreGivenLocations:
                    # Starting moves could be a lot of things - instead of being super vague we'll hint the specific item directly.
                    hinted_item_name = ItemList[hinted_item_id].name
                    message = f"\x0b{hinted_item_name}\x0b is on the path to {kong_color} {colorless_kong_list[hinted_kong]}'s K. Rool fight.{kong_color}"
                elif region.isCBRegion():
                    # Medal rewards and bosses are treated as "collecting colored bananas" for their region
                    hinted_location_text = f"{level_colors[region.level]}{short_level_list[region.level]} Colored Bananas{level_colors[region.level]}"
                    message = f"Something about collecting {hinted_location_text} is on the path to {kong_color} {colorless_kong_list[hinted_kong]}'s K. Rool fight.{kong_color}"
                else:
                    message = f"Something in the {hinted_location_text} is on the path to {kong_color} {colorless_kong_list[hinted_kong]}'s K. Rool fight.{kong_color}"
                hint_location.related_location = path_location_id
                hint_location.hint_type = HintType.RequiredWinConditionHint
                UpdateHint(hint_location, message)
        # All fairies seeds get 2 path hints for the camera
        if spoiler.settings.win_condition_item in (WinConditionComplex.req_fairy, WinConditionComplex.krem_kapture):
            camera_location_id = None
            for location_id in spoiler.woth_paths.keys():
                if spoiler.LocationList[location_id].item in (Items.Camera, Items.CameraAndShockwave):
                    camera_location_id = location_id
                    break
            path = spoiler.woth_paths[camera_location_id]
            already_chosen_camera_path_locations = []
            for i in range(hint_distribution[HintType.RequiredWinConditionHint]):
                hintable_location_ids = [loc for loc in path if loc not in already_chosen_camera_path_locations]
                path_location_id = spoiler.settings.random.choice(hintable_location_ids)
                # Soft reroll duplicate hints based on hint reroll parameters
                rerolls = 0
                while rerolls < hint_reroll_cap and path_location_id in globally_hinted_location_ids and spoiler.settings.random.random() <= hint_reroll_chance:
                    path_location_id = spoiler.settings.random.choice(hintable_location_ids)
                    rerolls += 1
                # After this point, the path_location_id is locked in and cannot be changed!

                globally_hinted_location_ids.append(path_location_id)
                already_chosen_camera_path_locations.append(path_location_id)
                region = spoiler.RegionList[GetRegionIdOfLocation(spoiler, path_location_id)]
                hinted_location_text = level_colors[region.level] + region.getHintRegionName() + level_colors[region.level]
                # Attempt to find a door that will be accessible before the Camera
                hint_options = getHintLocationsForAccessibleHintItems(spoiler.accessible_hints_for_location[camera_location_id])
                if len(hint_options) > 0:
                    hint_location = spoiler.settings.random.choice(hint_options)
                # If there are no doors available (unlikely by now) then just get a random one. Tough luck.
                else:
                    hint_location = getRandomHintLocation(random=spoiler.settings.random)
                if path_location_id in TrainingBarrelLocations or path_location_id in PreGivenLocations:
                    # Starting moves could be a lot of things - instead of being super vague we'll hint the specific item directly.
                    hinted_item_name = ItemList[spoiler.LocationList[path_location_id].item].name
                    message = f"\x0b{hinted_item_name}\x0b is on the path to \x07taking photos\x07."
                elif region.isCBRegion():
                    # Medal rewards and bosses are treated as "collecting colored bananas" for their region
                    hinted_location_text = f"{level_colors[region.level]}{short_level_list[region.level]} Colored Bananas{level_colors[region.level]}"
                    message = f"Something about collecting {hinted_location_text} is on the path to \x07taking photos\x07."
                else:
                    message = f"Something in the {hinted_location_text} is on the path to \x07taking photos\x07."
                hint_location.related_location = path_location_id
                hint_location.hint_type = HintType.RequiredWinConditionHint
                UpdateHint(hint_location, message)

    # Moves should be hinted before they're available
    moves_hinted_and_lobbies = {}  # Avoid putting a hint for the same move in the same lobby twice
    locationless_move_keys = []  # Keep track of moves we know have run out of locations to hint
    placed_move_hints = 0
    while placed_move_hints < hint_distribution[HintType.MoveLocation]:
        # First pick a random item from the WOTH - valid items are moves (not kongs) and must not be one of our known impossible-to-place items
        woth_item = None
        valid_woth_item_locations = [loc for loc in spoiler.woth_locations if loc not in locationless_move_keys and spoiler.LocationList[loc].type == Types.Shop]
        if len(valid_woth_item_locations) == 0:
            # In the OBSCENELY rare case that we can't hint any more moves, then we'll settle for joke hints
            # This would only happen in the case where all moves are in early worlds, coins are plentiful, and the distribution here is insanely high
            # Your punishment for these extreme settings is more joke hints
            hint_diff = hint_distribution[HintType.MoveLocation] - placed_move_hints
            hint_distribution[HintType.Joke] += hint_diff
            hint_distribution[HintType.MoveLocation] -= hint_diff
            break
        woth_item_location = spoiler.settings.random.choice(valid_woth_item_locations)
        index_of_level_with_location = spoiler.LocationList[woth_item_location].level
        # Now we need to find the Item object associated with this name
        woth_item = spoiler.LocationList[woth_item_location].item
        # Don't hint slams with these hints - it's slightly misleading and saves some headache to not do this
        if woth_item == Items.ProgressiveSlam:
            continue
        # Determine what levels are before this level
        hintable_levels = all_levels.copy()
        # Only if we care about the level order do we restrict these hints' locations
        # We lack the tools (or creativity) to figure out proper locations for hints in hard level progression (for now?)
        if level_order_matters and not spoiler.settings.hard_level_progression:
            # Determine a sorted order of levels by B. Lockers - this may not be the actual "progression" but it'll do for now
            levels_in_order = all_levels.copy()
            levels_in_order.sort(key=lambda l: spoiler.settings.BLockerEntryCount[l])

            hintable_levels = []
            cheapest_levels_with_item = []
            # Go through our levels in progression order
            for level in levels_in_order:
                # If the level doesn't have access to the move, we can hint it in the lobby
                if woth_item not in spoiler.settings.owned_moves_by_level[level]:
                    hintable_levels.append(level)
                # We hit our first level that has logical access to the move, time to get to work
                else:
                    # Find all levels with B. Lockers of the same price as this one
                    cheapest_levels_candidates = [
                        candidate for candidate in all_levels if spoiler.settings.BLockerEntryCount[candidate] == spoiler.settings.BLockerEntryCount[level] and candidate not in hintable_levels
                    ]
                    # If there's only one candidate then this is the level that gives logical access to the move, so we're done
                    # If it's an Isles shop we're hinting we don't need to pare down the lobby options, so we're done
                    if len(cheapest_levels_candidates) == 1 or index_of_level_with_location >= 7:
                        cheapest_levels_with_item = cheapest_levels_candidates
                    # In normal level progression, we need to remove levels that are beyond the shop's level
                    else:
                        # Determine the level order of the shop
                        level_order_of_shop_location = -1
                        for order in spoiler.settings.level_order:
                            if index_of_level_with_location == spoiler.settings.level_order[order]:
                                level_order_of_shop_location = order
                                break
                        # For each of our cheap levels
                        for cheap_level in cheapest_levels_candidates:
                            # Get the level order of this cheap level (will only match one)
                            cheap_level_order = [o for o in spoiler.settings.level_order if cheap_level == spoiler.settings.level_order[o]][0]
                            # If this level is before our shop's level in the order, it can have the hint
                            if cheap_level_order <= level_order_of_shop_location:
                                cheapest_levels_with_item.append(cheap_level)
                    break
            # We can also hint the cheapest levels that have access to this item
            # This manifests in the form of finding a hint in Japes lobby for Pineapple in an earlier level if Chunky is unlocked in Japes
            hintable_levels.extend(cheapest_levels_with_item)
        # Don't place the same hint in the same lobby
        if woth_item in moves_hinted_and_lobbies.keys():
            for lobby_with_this_hint in moves_hinted_and_lobbies[woth_item]:
                if lobby_with_this_hint in hintable_levels:
                    hintable_levels.remove(lobby_with_this_hint)
        else:
            moves_hinted_and_lobbies[woth_item] = []

        hint_location = getRandomHintLocation(random=spoiler.settings.random, levels=hintable_levels, move_name=ItemList[woth_item].name)
        # If we've been too restrictive and ran out of spots for this move to be hinted in, don't bother trying to fix it. Just pick another move
        if hint_location is None:
            locationless_move_keys.append(woth_item_location)
            continue

        shop_level = level_colors[index_of_level_with_location] + level_list[index_of_level_with_location] + level_colors[index_of_level_with_location]
        if spoiler.settings.wrinkly_hints == WrinklyHints.cryptic:
            shop_level = "\x08" + spoiler.settings.random.choice(level_cryptic_helm_isles[index_of_level_with_location]) + "\x08"
        shop_name = shop_owners[spoiler.LocationList[woth_item_location].vendor]
        message = f"On the Way of the Hoard, \x05{ItemList[woth_item].name}\x05 is bought from {shop_name} in {shop_level}."
        moves_hinted_and_lobbies[woth_item].append(hint_location.level)
        hint_location.related_location = woth_item_location
        hint_location.hint_type = HintType.MoveLocation
        UpdateHint(hint_location, message)
        placed_move_hints += 1

    # For T&S hints, we want to hint levels after the hint location and only levels that we don't start with keys for
    if hint_distribution[HintType.TroffNScoff] > 0:
        # Determine what levels have incomplete T&S
        levels_with_tns = []
        for keyEvent in spoiler.settings.krool_keys_required:
            if keyEvent == Events.JapesKeyTurnedIn:
                levels_with_tns.append(spoiler.settings.level_order[1])
            if keyEvent == Events.AztecKeyTurnedIn:
                levels_with_tns.append(spoiler.settings.level_order[2])
            if keyEvent == Events.FactoryKeyTurnedIn:
                levels_with_tns.append(spoiler.settings.level_order[3])
            if keyEvent == Events.GalleonKeyTurnedIn:
                levels_with_tns.append(spoiler.settings.level_order[4])
            if keyEvent == Events.ForestKeyTurnedIn:
                levels_with_tns.append(spoiler.settings.level_order[5])
            if keyEvent == Events.CavesKeyTurnedIn:
                levels_with_tns.append(spoiler.settings.level_order[6])
            if keyEvent == Events.CastleKeyTurnedIn:
                levels_with_tns.append(spoiler.settings.level_order[7])
        placed_tns_hints = 0
        while placed_tns_hints < hint_distribution[HintType.TroffNScoff]:
            attempts = 0
            # Make sure the location we randomly pick either is a level or is before a level that has a T&S
            future_tns_levels = []
            while not any(future_tns_levels):
                # If you can't find a location that can fit a T&S hint in 15 tries, it's either impossible or very likely redundant
                attempts += 1
                if attempts > 15:
                    break
                hint_location = getRandomHintLocation(random=spoiler.settings.random)
                future_tns_levels = [
                    level
                    for level in all_levels
                    if level in levels_with_tns and (not level_order_matters or spoiler.settings.BLockerEntryCount[level] >= spoiler.settings.BLockerEntryCount[hint_location.level])
                ]
            # If we failed to find it in 15 attempts, convert remaining T&S hints to joke hints
            # This is a disgustingly rare scenario, likely involving very few and early keys required
            if attempts > 15:
                hint_diff = hint_distribution[HintType.TroffNScoff] - placed_tns_hints
                hint_distribution[HintType.Joke] += hint_diff
                hint_distribution[HintType.TroffNScoff] -= hint_diff
                break
            hinted_level = spoiler.settings.random.choice(future_tns_levels)
            level_name = level_colors[hinted_level] + level_list[hinted_level] + level_colors[hinted_level]
            if spoiler.settings.wrinkly_hints == WrinklyHints.cryptic:
                level_name = "\x08" + spoiler.settings.random.choice(level_cryptic[hinted_level]) + "\x08"
            count = spoiler.settings.BossBananas[hinted_level]
            cb_name = "Small Bananas"
            if count == 1:
                cb_name = "Small Banana"
            message = f"The barrier to the boss in {level_name} can be cleared by obtaining \x04{count} {cb_name}\x04."
            hint_location.hint_type = HintType.TroffNScoff
            UpdateHint(hint_location, message)
            placed_tns_hints += 1

    if hint_distribution[HintType.EntranceV2] > 0:
        # Dictionaries of exceptions for locations and regions that have to be handled with care
        location_exceptions = {
            # Japes Diddy Top of Mountain cares much more about the Mine than Japes Main
            Locations.JapesDiddyMountain: [Regions.Mine, Maps.JapesMountain],
            # Forest Diddy Winch naturally needs to find the Winch room very badly rather than Forest Main
            Locations.ForestDiddyCagedBanana: [Regions.WinchRoom, Maps.ForestWinchRoom],
        }
        region_exceptions = {
            # Most Galleon ships share a Map but have segmented sections. We want to be sure we're looking for the correct transition for each check.
            Regions.TinyShip: [Transitions.GalleonTinyToShipyard],
            Regions.LankyShip: [Transitions.GalleonLankyToShipyard],
            Regions.BongosShip: [Transitions.GalleonBongosToShipyard],
            Regions.SaxophoneShip: [Transitions.GalleonSaxophoneToShipyard],
            Regions.GuitarShip: [Transitions.GalleonGuitarToShipyard],
            Regions.TromboneShip: [Transitions.GalleonTromboneToShipyard],
            Regions.TriangleShip: [Transitions.GalleonTriangleToShipyard],
            # The Castle Museum Map is segmented by glass walls. Different regions of the Museum care about different transitions.
            Regions.Museum: [Transitions.CastleMuseumToMain],
            Regions.MuseumBehindGlass: [Transitions.CastleMuseumToBallroom, Transitions.CastleMuseumToCarRace],
        }
        # These are the maps we classify as "connectors" - they are regions with exactly two entrances
        connector_maps = {
            Maps.TrainingGrounds: [Regions.TrainingGrounds],
            Maps.JungleJapesLobby: [Regions.JungleJapesLobby],
            Maps.AngryAztecLobby: [Regions.AngryAztecLobby],
            Maps.FranticFactoryLobby: [Regions.FranticFactoryLobby],
            Maps.GloomyGalleonLobby: [Regions.GloomyGalleonLobby, Regions.GloomyGalleonLobbyEntrance],
            Maps.FungiForestLobby: [Regions.FungiForestLobby],
            Maps.CrystalCavesLobby: [Regions.CrystalCavesLobby],
            Maps.CreepyCastleLobby: [Regions.CreepyCastleLobby],
            Maps.HideoutHelmLobby: [Regions.HideoutHelmLobby, Regions.HideoutHelmLobbyPastVines],
            Maps.ForestMillFront: [Regions.GrinderRoom],  # The Mini entrance counts
            Maps.CastleMuseum: [Regions.MuseumBehindGlass],  # Weird, but technically a connector between MP and Mini entrances
            Maps.CastleBallroom: [Regions.Ballroom],  # Also weird, as one side is all-kong and the other side is a MP pad
            Maps.CastleCrypt: [Regions.Crypt, Regions.CryptDonkeyRoom],  # Similar to Ballroom, just replace MP pad with a Coconut + Grab locked door
            Maps.JapesMountain: [Regions.Mine],  # If Diddy Minecart is WotH, we want to hint the way to get into the mountain, not the Minecart entrance
            # These are not real connectors, as one of their entrances is a one-way ticket to zilch
            # Maps.CastleGreenhouse: [Regions.Greenhouse],  # Always kicks you out to Castle Main
            # Maps.CastleTree: [Regions.CastleTree],  # Always kicks you out to Castle Main
            # These larger connectors have enough entrances it should be somewhat less painful to have to find them for a hinted entrance there
            # Maps.ForestMillBack: [Regions.MillChunkyTinyArea],
            # Maps.ForestGiantMushroom: [Regions.MushroomLower, Regions.MushroomLowerMid, Regions.MushroomMiddle, Regions.MushroomUpperMid, Regions.MushroomUpper, Regions.MushroomNightDoor],
            # Maps.CastleUpperCave: [Regions.UpperCave],
            # Maps.CastleLowerCave: [Regions.LowerCave],
        }
        # If warps are pre-activated and cross-map, we can't treat the Castle Crypt as a connector because you are decently likely to just warp into it.
        if spoiler.settings.activate_all_bananaports == ActivateAllBananaports.all and spoiler.settings.bananaport_rando in (BananaportRando.crossmap_coupled, BananaportRando.crossmap_decoupled):
            del connector_maps[Maps.CastleCrypt]
        # First identify which maps contain WotH items - some maps are more interesting than others
        isolated_interesting_transitions = []
        # Lists to prevent duplicate entrance hints from existing
        tracked_maps = []
        tracked_regions = []
        priority_transition_to_helm = None
        for woth_location_id in spoiler.woth_locations:
            location = spoiler.LocationList[woth_location_id]
            # If Helm is not shuffled, Helm is not an interesting map - we know where it is
            if location.level == Levels.HideoutHelm and not spoiler.settings.shuffle_helm_location:
                continue
            # Some locations are exceptions to their own positioning due to other circumstances - see the dict for details
            if woth_location_id in location_exceptions.keys():
                region_id = location_exceptions[woth_location_id][0]
                woth_map = location_exceptions[woth_location_id][1]
            # For every other normal location...
            else:
                # These types of locations (Helm locations are special) don't have a single map, so they don't really work for what we're trying to go for here
                if location.level != Levels.HideoutHelm and location.type in (
                    Types.Shop,  # TODO: Investigate the feasibility of hinting shops if they're outside of the level's main map (while still taking into consideration shop location shuffle)
                    Types.Medal,
                    Types.Key,
                    Types.RarewareCoin,
                    Types.TrainingBarrel,
                    Types.PreGivenMove,
                    Types.Cranky,
                    Types.Funky,
                    Types.Candy,
                    Types.Snide,
                    Types.Constant,
                    Types.IslesMedal,
                    Types.Climbing,
                ):
                    continue
                region_id = GetRegionIdOfLocation(spoiler, woth_location_id)
                woth_map = GetMapId(spoiler.settings, region_id)
            # Ignore the main map of each level, these should be fairly straightforward to find - mind the exceptions!
            main_level_maps = (
                Maps.Isles,
                Maps.JungleJapes,
                Maps.AngryAztec,
                Maps.FranticFactory,
                Maps.GloomyGalleon,
                Maps.FungiForest,
                Maps.CrystalCaves,
                Maps.CreepyCastle,
            )
            if woth_map in main_level_maps:
                continue
            # Blast maps all happen to be contained in the main map of the respective level
            if woth_map in (
                Maps.JapesBaboonBlast,
                Maps.AztecBaboonBlast,
                Maps.FactoryBaboonBlast,
                Maps.GalleonBaboonBlast,
                Maps.ForestBaboonBlast,
                Maps.CavesBaboonBlast,
                Maps.CastleBaboonBlast,
            ):
                continue
            # If warps are pre-activated and cross-map, you might enter the Castle Crypt or the Llama Temple via the warps, and those transitions aren't hintable.
            if spoiler.settings.activate_all_bananaports == ActivateAllBananaports.all and spoiler.settings.bananaport_rando in (BananaportRando.crossmap_coupled, BananaportRando.crossmap_decoupled):
                # Best to not entrance hint these maps in those worlds just in case.
                if woth_map in (Maps.CastleCrypt, Maps.AztecLlamaTemple):
                    continue
            # Avoid hinting the same map section twice
            if woth_map in tracked_maps and (region_id in tracked_regions or region_id not in region_exceptions.keys()):
                continue
            hint_candidate_entrances = []
            # Find all the transitions that lead to this Map. Some regions need to target specific transitions within the Map.
            target_transitions = []
            if region_id in region_exceptions.keys():
                # If this WotH Region triggers the exception protocol, only very specific entrances are considered to be connected
                target_transitions = region_exceptions[region_id]
            connected_entrances = GetConnectedEntrances(spoiler, woth_map, target_transitions)
            # In coupled LZR, getting a connector's entrance hinted isn't really helpful, as you still have to find the connector
            if not spoiler.settings.decoupled_loading_zones:
                # So far we're one layer in - find any entrances that come from connectors
                entrances_sourced_from_connectors = []
                for transitionId in connected_entrances:
                    exit = ShufflableExits[transitionId]
                    sourceMap = GetMapId(spoiler.settings, exit.region)
                    # If this location's source is a connector, note it down to find a transition to a non-connector map
                    if sourceMap in connector_maps.keys() and exit.region in connector_maps[sourceMap]:
                        entrances_sourced_from_connectors.append(transitionId)
                    # If not, it's a more relevant entrance to hint for this region
                    else:
                        hint_candidate_entrances.append(transitionId)
                # If any of our connections came from a connector, we have to go arbitrarily deeper until we find it
                seenMaps = [woth_map]
                while any(entrances_sourced_from_connectors):
                    # Repeat the same process as we did for the woth_map
                    transitionId = entrances_sourced_from_connectors.pop()
                    exit = ShufflableExits[transitionId]
                    sourceMap = GetMapId(spoiler.settings, exit.region)
                    # Find all connected entrances, keeping in mind the specific transitions some regions need to track down
                    target_transitions = []
                    if exit.region in region_exceptions.keys():
                        target_transitions = region_exceptions[exit.region]
                    deeper_connected_entrances = GetConnectedEntrances(spoiler, sourceMap, target_transitions)
                    # Check if any of these entrances also lead to connectors
                    for deeper_transitionId in deeper_connected_entrances:
                        deeper_exit = ShufflableExits[deeper_transitionId]
                        deeperMap = GetMapId(spoiler.settings, deeper_exit.region)
                        # New to this second-level checking: make sure we're not potentially returning to any map we've already checked, this would make a loop
                        if deeperMap in seenMaps:
                            continue
                        # If the deeper transition's source is a connector, WE HAVE TO GO DEEPER
                        if deeperMap in connector_maps.keys() and deeper_exit.region in connector_maps[deeperMap]:
                            entrances_sourced_from_connectors.append(deeper_transitionId)
                        # If not, it's a more relevant entrance to hint for our woth location
                        else:
                            hint_candidate_entrances.append(deeper_transitionId)
                    seenMaps.append(sourceMap)
            else:
                hint_candidate_entrances = connected_entrances
            tracked_maps.append(woth_map)
            tracked_regions.append(region_id)
            # If Helm is eligible to be hinted, we may want to guarantee it gets hinted - note that Helm only ever has one entry transition
            # We always want to hint Helm in worlds where we know Key 8 is in Helm and that it is required
            if location.level == Levels.HideoutHelm and spoiler.settings.key_8_helm and Locations.HelmKey in spoiler.woth_locations:
                priority_transition_to_helm = hint_candidate_entrances[0]
                continue
            # If this map has only one entrance, it's an isolated entrance that would be among the most helpful to hint
            if len(hint_candidate_entrances) == 1:
                isolated_interesting_transitions.append([hint_candidate_entrances[0], woth_location_id])
            # Every map has at least one entrance (or else you couldn't get to it, duh)
            # If there are no relevant entrances, it's probably a region accessed by unshuffled entrances (e.g. Chunky Minecart in coupled)
            elif len(hint_candidate_entrances) != 0:
                # For connectors, pick the entrance that the playthrough finds first
                for transition_id in spoiler.playthroughTransitionOrder:
                    if transition_id in hint_candidate_entrances:
                        isolated_interesting_transitions.append([transition_id, woth_location_id])
                        break
        spoiler.settings.random.shuffle(isolated_interesting_transitions)
        # If Helm access must be prioritized, force it to be hinted first
        if priority_transition_to_helm is not None:
            isolated_interesting_transitions.insert(0, [priority_transition_to_helm, Locations.HelmKey])
        # If there are more entrance hints planned than interesting transitions to hint, sounds like we need more WotH hints for the locations on larger maps
        if len(isolated_interesting_transitions) < hint_distribution[HintType.EntranceV2]:
            diff = hint_distribution[HintType.EntranceV2] - len(isolated_interesting_transitions)
            hint_distribution[HintType.WothLocation] += diff
            hint_distribution[HintType.EntranceV2] -= diff
        for i in range(hint_distribution[HintType.EntranceV2]):
            pair_to_hint = isolated_interesting_transitions[i]
            hint_location = getRandomHintLocation(random=spoiler.settings.random)
            entranceName = ShufflableExits[pair_to_hint[0]].name
            message = f"Entering \x08{entranceName}\x08 should be of great interest to your quest."
            hint_location.hint_type = HintType.EntranceV2
            hint_location.related_location = pair_to_hint[1]
            globally_hinted_location_ids.append(pair_to_hint[1])
            UpdateHint(hint_location, message)

    # WotH Location hints list a location that is Way of the Hoard. Most applicable in item rando.
    if hint_distribution[HintType.WothLocation] > 0:
        hintable_location_ids = []
        for location_id in spoiler.woth_locations:
            location = spoiler.LocationList[location_id]
            # Only hint things that are in shuffled locations - don't hint starting moves because you can't know which move it refers to and don't hint the Helm Key if you know key 8 is there
            if (
                location.type in spoiler.settings.shuffled_location_types
                and location.type not in (Types.TrainingBarrel, Types.PreGivenMove, Types.Climbing)
                and not (spoiler.settings.key_8_helm and location_id == Locations.HelmKey)
            ):
                # WotH Keys that are in Shops and have nothing else on the path to them will already be entirely covered and solved with the guaranteed multipath hint
                if ItemList[location.item].type == Types.Key and location.type == Types.Shop and location_id in spoiler.woth_paths.keys() and len(spoiler.woth_paths[location_id]) == 1:
                    continue
                hintable_location_ids.append(location_id)
        spoiler.settings.random.shuffle(hintable_location_ids)
        placed_woth_hints = 0
        while placed_woth_hints < hint_distribution[HintType.WothLocation]:
            # If you run out of hintable woth locations, throw in a foolish for their troubles - this should only happen if there's very few late woth locations.
            # In (increasingly) obscenely rare circumstances, this might affect the Fixed distribution. I think this is too subtle to actually matter.
            if len(hintable_location_ids) == 0:
                hint_distribution[HintType.WothLocation] -= 1
                hint_distribution[HintType.FoolishRegion] += 1
                continue
            hinted_loc_id = spoiler.settings.random.choice(hintable_location_ids)
            # Soft reroll duplicate hints based on hint reroll parameters
            rerolls = 0
            while rerolls < hint_reroll_cap and hinted_loc_id in globally_hinted_location_ids and spoiler.settings.random.random() <= hint_reroll_chance:
                hinted_loc_id = spoiler.settings.random.choice(hintable_location_ids)
                rerolls += 1
            # After this point, the path_location_id is locked in and cannot be changed!

            globally_hinted_location_ids.append(hinted_loc_id)
            hintable_location_ids.remove(hinted_loc_id)
            # Attempt to find a door that will be accessible before the location is
            hint_options = getHintLocationsForAccessibleHintItems(spoiler.accessible_hints_for_location[hinted_loc_id])
            if len(hint_options) > 0:
                hint_location = spoiler.settings.random.choice(hint_options)
            # If there are no doors available, it's likely a very early woth location. Go find a better location to hint.
            else:
                continue
            hint_color = level_colors[spoiler.LocationList[hinted_loc_id].level]
            message = f"{hint_color}{spoiler.LocationList[hinted_loc_id].name}{hint_color} is on the \x04Way of the Hoard\x04."
            hint_location.related_location = hinted_loc_id
            hint_location.hint_type = HintType.WothLocation
            UpdateHint(hint_location, message)
            placed_woth_hints += 1

    # Foolish Region hints state that a hint region is foolish. Useful in item rando.
    # Foolish regions contain no major items that would block any amount of progression, even non-required progression
    if hint_distribution[HintType.FoolishRegion] > 0:
        # Determine how many locations are contained in the foolish regions
        total_foolish_location_score = 0
        foolish_region_location_score = {}
        for foolish_name in spoiler.foolish_region_names:
            foolish_location_score = 0
            shops_in_region = 0
            regions_in_region = [region for region in spoiler.RegionList.values() if region.hint_name == foolish_name]
            for region in regions_in_region:
                foolish_location_score += len(
                    [loc for loc in region.locations if not spoiler.LocationList[loc.id].inaccessible and spoiler.LocationList[loc.id].type in spoiler.settings.shuffled_location_types]
                )
                if region.level == Levels.Shops and region.hint_name != HintRegion.Jetpac:  # Jetpac isn't a "real" shop, it's in the Shops level for convenience
                    shops_in_region += 1
            # "Medal Rewards" regions are cb foolish hints, which are just generally more valuable to hint foolish (so long as medals are relevant)
            if foolish_name in MEDAL_REWARD_REGIONS and Types.Medal in spoiler.settings.shuffled_location_types:
                foolish_location_score += 3
            elif shops_in_region > 0:  # Shops are generally overvalued (4/6 locations per shop) with this method due to having mutually exclusive locations
                foolish_location_score -= 1 * shops_in_region  # With smaller shops, this reduces the location count to 3 locations per shop
                if foolish_location_score < 0:  # Prevent negative scores
                    foolish_location_score = 0
            foolish_location_score = foolish_location_score**1.25  # Exponentiation of this score puts additional emphasis (but not too much) on larger regions
            total_foolish_location_score += foolish_location_score
            foolish_region_location_score[foolish_name] = foolish_location_score
        spoiler.settings.random.shuffle(spoiler.foolish_region_names)
        for i in range(hint_distribution[HintType.FoolishRegion]):
            # If you run out of foolish regions (maybe in an all medals run?) - this *should* be covered by the distribution earlier but this is a good failsafe
            if len(spoiler.foolish_region_names) == 0 or sum(foolish_region_location_score.values()) == 0:  # You can either expend the whole list or run out of eligible regions
                # Replace remaining move hints with region item count hints, because it sounds like you need em
                hint_distribution[HintType.FoolishRegion] -= 1
                hint_distribution[HintType.RegionItemCount] += 1
                continue
            hinted_region_name = spoiler.settings.random.choices(list(foolish_region_location_score.keys()), foolish_region_location_score.values())[
                0
            ]  # Weighted random choice from list of foolish region names
            spoiler.foolish_region_names.remove(hinted_region_name)
            del foolish_region_location_score[hinted_region_name]
            hint_location = getRandomHintLocation(random=spoiler.settings.random)
            level_color = "\x05"
            level = Levels.DKIsles
            for region_id in Regions:
                if spoiler.RegionList[region_id].hint_name == hinted_region_name:
                    region_level = spoiler.RegionList[region_id].level
                    level_color = level_colors[region_level]
                    break
            if hinted_region_name in MEDAL_REWARD_REGIONS:
                message = f"It would be \x05foolish\x05 to collect {level_color}{short_level_list[region_level]} Colored Bananas{level_color}."
            else:
                message = f"It would be \x05foolish\x05 to explore the {level_color}{HINT_REGION_PAIRING.get(hinted_region_name, hinted_region_name.name)}{level_color}."
            hint_location.hint_type = HintType.FoolishRegion
            UpdateHint(hint_location, message)

    # TEMPORARILY SHELVED - may revisit in the future with either more processing power or a more clever approach
    # Pathless hints are the evolution of foolish moves - it hints a move that is not on the path to anything else.
    # You may use a pathless move as a part of an either/or, but it will not be strictly required for anything.
    # Slams are banned from being hinted this way cause I do not want to deal with that *at all*
    # Hints are weighted towards more impactful things: guns, instruments, and good training moves.
    if hint_distribution[HintType.ForeseenPathless] > 0:
        pathless_move_score = {}
        for move in spoiler.pathless_moves:
            # Some moves are just better than others - these are less likely to not be on paths, and it's really good to know that.
            if move in [
                Items.Coconut,  # All the guns
                Items.Peanut,
                Items.Grape,
                Items.Feather,
                Items.Pineapple,
                Items.Bongos,  # All the instruments
                Items.Guitar,
                Items.Trombone,
                Items.Saxophone,
                Items.Triangle,
                Items.Barrels,  # All the good training moves
                Items.Vines,
                Items.Climbing,
                Items.Swim,
                Items.Camera,  # Camera and Shockwave
                Items.Shockwave,
                Items.CameraAndShockwave,
                Items.RocketbarrelBoost,  # A few extra moves that are particularly useful
                Items.MiniMonkey,
                Items.PrimatePunch,
            ]:
                pathless_move_score[move] = 4  # These moves are four times as likely as any other move to get picked now
            else:
                pathless_move_score[move] = 1
        for i in range(hint_distribution[HintType.ForeseenPathless]):
            # If somehow you end up with more hints than there are pathless moves...
            if len(pathless_move_score.keys()) <= 0:
                # Convert to region item count hints because it sounds like you need em
                hint_distribution[HintType.ForeseenPathless] -= 1
                hint_distribution[HintType.RegionItemCount] += 1
                continue
            pathless_item = spoiler.settings.random.choices(list(pathless_move_score.keys()), pathless_move_score.values())[0]
            del pathless_move_score[pathless_item]
            hint_location = getRandomHintLocation(random=spoiler.settings.random)
            message = f"I have foreseen that there are \x0bno paths to the Hoard\x0b which contain \x04{ItemList[pathless_item].name}\x04."
            hint_location.hint_type = HintType.ForeseenPathless
            UpdateHint(hint_location, message)

    # Region Item Count hints tell you how many potions are in contained in the entirety of a hint region.
    # Currently it randomly picks a region that has a non-zero amount of potions in it, but it cannot hint shop regions.
    if hint_distribution[HintType.RegionItemCount] > 0:
        hintable_region_names = list(spoiler.region_hintable_count.keys())
        spoiler.settings.random.shuffle(hintable_region_names)
        for i in range(hint_distribution[HintType.RegionItemCount]):
            # If somehow you end up with more hints than there are regions with moves in them...
            if len(hintable_region_names) <= 0:
                # You made some meme of a seed so have some meme hints
                hint_distribution[HintType.RegionItemCount] -= 1
                hint_distribution[HintType.Joke] += 1
                continue
            region_name_to_hint = hintable_region_names.pop()
            hint_location = getRandomHintLocation(random=spoiler.settings.random)
            level_color = "\x05"
            for region_id in Regions:
                if spoiler.RegionList[region_id].hint_name == region_name_to_hint:
                    level_color = level_colors[spoiler.RegionList[region_id].level]
                    break
            plural = ""
            if spoiler.region_hintable_count[region_name_to_hint] > 1:
                plural = "s"
            message = f"Scouring the {level_color}{HINT_REGION_PAIRING.get(region_name_to_hint, region_name_to_hint.name)}{level_color} will yield you \x0d{spoiler.region_hintable_count[region_name_to_hint]} potion{plural}\x0d."
            hint_location.hint_type = HintType.RegionItemCount
            UpdateHint(hint_location, message)

    # Entrance hints are tricky, there's some requirements we must hit:
    # We must hint each of Japes, Aztec, and Factory at least once
    # The rest of the hints are tied to a variety of important locations
    if hint_distribution[HintType.Entrance] > 0:
        criticalJapesRegions = [
            Regions.JungleJapesEntryHandler,
            Regions.JungleJapesStart,
            Regions.JungleJapesMain,
            Regions.JapesHillTop,
            Regions.JapesHill,
            Regions.JapesCannonPlatform,
            Regions.JapesBeyondFeatherGate,
            Regions.TinyHive,
            Regions.JapesLankyCave,
            Regions.Mine,
        ]
        criticalAztecRegions = [
            Regions.AngryAztecEntryHandler,
            Regions.AngryAztecStart,
            Regions.AngryAztecOasis,
            Regions.AngryAztecMain,
            Regions.DonkeyTemple,
            Regions.DiddyTemple,
            Regions.LankyTemple,
            Regions.TinyTemple,
            Regions.ChunkyTemple,
            Regions.TempleStart,
            Regions.LlamaTemple,
        ]
        criticalFactoryRegions = [
            Regions.FranticFactoryEntryHandler,
            Regions.FranticFactoryStart,
            Regions.ChunkyRoomPlatform,
            Regions.PowerHut,
            Regions.BeyondHatch,
            Regions.FactoryArcadeTunnel,
            Regions.LowerCore,
            Regions.InsideCore,
        ]
        usefulRegions = [
            criticalJapesRegions,
            criticalAztecRegions,
            criticalFactoryRegions,
            [Regions.BananaFairyRoom],
            [Regions.TrainingGrounds],
            [
                Regions.GloomyGalleonEntryHandler,
                Regions.GloomyGalleonStart,
                Regions.LighthousePlatform,
                Regions.LighthouseUnderwater,
                Regions.ShipyardUnderwater,
                Regions.Shipyard,
            ],
            [
                Regions.FungiForestEntryHandler,
                Regions.FungiForestStart,
                Regions.GiantMushroomArea,
                Regions.MushroomLowerExterior,
                Regions.MushroomNightExterior,
                Regions.MushroomUpperExterior,
                Regions.MushroomUpperMidExterior,
                Regions.ForestVeryTopOfMill,
                Regions.ForestTopOfMill,
                Regions.MillArea,
                Regions.ThornvineArea,
            ],
            [Regions.CrystalCavesEntryHandler, Regions.CrystalCavesMain, Regions.IglooArea, Regions.CabinArea],
            [Regions.CreepyCastleEntryHandler, Regions.CreepyCastleMain, Regions.CastleWaterfall],
            [Regions.LowerCave],
            [Regions.UpperCave],
        ]
        placed_entrance_hints = 0
        while placed_entrance_hints < hint_distribution[HintType.Entrance]:
            message = ""
            # Always put in at least one Japes hint
            if placed_entrance_hints == 0:
                japesHintEntrances = [entrance for entrance, back in spoiler.shuffled_exit_data.items() if back.regionId in criticalJapesRegions]
                spoiler.settings.random.shuffle(japesHintEntrances)
                japesHintPlaced = False
                while len(japesHintEntrances) > 0:
                    japesHinted = japesHintEntrances.pop()
                    message = TryCreatingLoadingZoneHint(spoiler, japesHinted, criticalJapesRegions)
                    if message != "":
                        japesHintPlaced = True
                        break
                if not japesHintPlaced:
                    print("Japes LZR hint unable to be placed!")
            # Always put in at least one Aztec hint
            elif placed_entrance_hints == 1:
                aztecHintEntrances = [entrance for entrance, back in spoiler.shuffled_exit_data.items() if back.regionId in criticalAztecRegions]
                spoiler.settings.random.shuffle(aztecHintEntrances)
                aztecHintPlaced = False
                while len(aztecHintEntrances) > 0:
                    aztecHinted = aztecHintEntrances.pop()
                    message = TryCreatingLoadingZoneHint(spoiler, aztecHinted, criticalAztecRegions)
                    if message != "":
                        aztecHintPlaced = True
                        break
                if not aztecHintPlaced:
                    print("Aztec LZR hint unable to be placed!")
            # Always put in at least one Factory hint
            elif placed_entrance_hints == 2:
                factoryHintEntrances = [entrance for entrance, back in spoiler.shuffled_exit_data.items() if back.regionId in criticalFactoryRegions]
                spoiler.settings.random.shuffle(factoryHintEntrances)
                factoryHintPlaced = False
                while len(factoryHintEntrances) > 0:
                    factoryHinted = factoryHintEntrances.pop()
                    message = TryCreatingLoadingZoneHint(spoiler, factoryHinted, criticalFactoryRegions)
                    if message != "":
                        factoryHintPlaced = True
                        break
                if not factoryHintPlaced:
                    print("Factory LZR hint unable to be placed!")
            else:
                region_to_hint = spoiler.settings.random.choice(usefulRegions)
                usefulHintEntrances = [entrance for entrance, back in spoiler.shuffled_exit_data.items() if back.regionId in region_to_hint]
                spoiler.settings.random.shuffle(usefulHintEntrances)
                usefulHintPlaced = False
                while len(usefulHintEntrances) > 0:
                    usefulHinted = usefulHintEntrances.pop()
                    message = TryCreatingLoadingZoneHint(spoiler, usefulHinted, region_to_hint)
                    if message != "":
                        usefulHintPlaced = True
                        break
                if not usefulHintPlaced:
                    print(f"Useful LZR hint to {usefulHinted.name} unable to be placed!")
            if message == "":
                # Then we somehow managed to fail to create a hint. This is real bad but we'll just laugh it off with a joke hint. Hahaha!
                hint_distribution[HintType.Entrance] -= 1
                hint_distribution[HintType.Joke] += 1
                continue
            hint_location = getRandomHintLocation(random=spoiler.settings.random)
            hint_location.hint_type = HintType.Entrance
            UpdateHint(hint_location, message)
            placed_entrance_hints += 1

    # If any Helm doors are random, place a hint for each random door somewhere
    if hint_distribution[HintType.RequiredHelmDoorHint] > 0:
        placed_requiredhelmdoorhints = 0
        helmdoor_vars = {
            BarrierItems.GoldenBanana: "Golden Banana",
            BarrierItems.Blueprint: "Blueprint",
            BarrierItems.CompanyCoin: "Special Coin",
            BarrierItems.Key: "Key",
            BarrierItems.Medal: "Medal",
            BarrierItems.Crown: "Crown",
            BarrierItems.Fairy: "Fairy",
            BarrierItems.RainbowCoin: "Rainbow Coin",
            BarrierItems.Bean: "Bean",
            BarrierItems.Pearl: "Pearl",
        }
        if spoiler.settings.crown_door_random:
            item_name = helmdoor_vars[spoiler.settings.crown_door_item]
            if spoiler.settings.crown_door_item_count > 1:
                if spoiler.settings.crown_door_item == BarrierItems.Fairy:
                    item_name = "Fairies"  # English is so rude sometimes
                else:
                    item_name = item_name + "s"
            hint_location = getRandomHintLocation(random=spoiler.settings.random)
            message = f"There lies a \x05gate in Hideout Helm\x05 that requires \x04{spoiler.settings.crown_door_item_count} {item_name}\x04."
            hint_location.hint_type = HintType.RequiredHelmDoorHint
            UpdateHint(hint_location, message)
            placed_requiredhelmdoorhints += 1
        if spoiler.settings.coin_door_random and placed_requiredhelmdoorhints < hint_distribution[HintType.RequiredHelmDoorHint]:
            item_name = helmdoor_vars[spoiler.settings.coin_door_item]
            if spoiler.settings.coin_door_item_count > 1:
                if spoiler.settings.coin_door_item == BarrierItems.Fairy:
                    item_name = "Fairies"  # Plurals? Consistency? A pipe dream
                else:
                    item_name = item_name + "s"
            hint_location = getRandomHintLocation(random=spoiler.settings.random)
            message = f"There lies a \x05gate in Hideout Helm\x05 that requires \x04{spoiler.settings.coin_door_item_count} {item_name}\x04."
            hint_location.hint_type = HintType.RequiredHelmDoorHint
            UpdateHint(hint_location, message)

    # Full Shop With Items hints are essentially a rework of shop dump hints but with the ability to list any item instead of just moves.
    chosen_shops = []
    for i in range(hint_distribution[HintType.FullShopWithItems]):
        # Shared shop lists are a convenient list of all individual shops in the game, regardless of if something is there
        shared_shop_location = spoiler.settings.random.choice([shop for shop in SharedShopLocations if shop not in chosen_shops])
        # Ensure we always hint unique shops
        chosen_shops.append(shared_shop_location)
        # Get the level and vendor type from that location
        shop_info = spoiler.LocationList[shared_shop_location]
        # Find all locations for this shop
        kongLocationsAtThisShop = [
            location
            for id, location in spoiler.LocationList.items()
            if location.type == Types.Shop and location.level == shop_info.level and location.vendor == shop_info.vendor and location.kong != Kongs.any
        ]
        # If this is a shared shop dump...
        if shop_info.item is not None and shop_info.item != Items.NoItem:
            shop_vendor = shop_owners[shop_info.vendor]
            level_name = level_colors[shop_info.level] + level_list[shop_info.level] + level_colors[shop_info.level]
            if spoiler.settings.wrinkly_hints == WrinklyHints.cryptic:
                level_name = "\x08" + spoiler.settings.random.choice(level_cryptic_helm_isles[shop_info.level]) + "\x08"
            move_series = ItemList[shop_info.item].name
        # Else this is a series of Kong-specific purchases
        else:
            spoiler.settings.random.shuffle(kongLocationsAtThisShop)  # Shuffle this list so you don't know who buys what
            item_names = [ItemList[location.item].name for location in kongLocationsAtThisShop if location.item is not None and location.item != Items.NoItem]
            if len(item_names) == 0:
                move_series = "nothing"
            else:
                move_series = item_names[0]
                if len(item_names) > 1:
                    move_series = f"{', '.join(item_names[:-1])}, and {item_names[-1]}"
        shop_vendor = shop_owners[shop_info.vendor]
        level_name = level_colors[shop_info.level] + level_list[shop_info.level] + level_colors[shop_info.level]
        if spoiler.settings.wrinkly_hints == WrinklyHints.cryptic:
            level_name = "\x08" + spoiler.settings.random.choice(level_cryptic_helm_isles[shop_info.level]) + "\x08"
        hint_location = getRandomHintLocation(random=spoiler.settings.random)
        message = f"{shop_vendor}'s in {level_name} contains {move_series}."
        hint_location.hint_type = HintType.FullShopWithItems
        UpdateHint(hint_location, message)

    # At least one Helm Order hint should be placed, but they can be placed randomly. If the player needs the info, they can seek it out.
    for i in range(hint_distribution[HintType.HelmOrder]):
        hint_location = getRandomHintLocation(random=spoiler.settings.random)
        default_order = [Kongs.donkey, Kongs.chunky, Kongs.tiny, Kongs.lanky, Kongs.diddy]
        helm_order = [default_order[room] for room in spoiler.settings.helm_order]
        kong_helm_order = [kong_list[x] for x in helm_order]
        kong_helm_text = ", then ".join(kong_helm_order)
        associated_hint = f"The \x05Blast-O-Matic\x05 can be disabled by using {kong_helm_text}."
        hint_location.hint_type = HintType.HelmOrder
        UpdateHint(hint_location, associated_hint)

    # No need to do anything fancy here - there's often already a K. Rool hint on the player's path (the wall in Helm)
    for i in range(hint_distribution[HintType.KRoolOrder]):
        hint_location = getRandomHintLocation(random=spoiler.settings.random)
        kong_krool_order = [boss_colors[map_id] + boss_names[map_id] + boss_colors[map_id] for map_id in spoiler.settings.krool_order]
        kong_krool_text = ", then ".join(kong_krool_order)
        associated_hint = f"\x08The final battle\x08 will be against {kong_krool_text}."
        hint_location.hint_type = HintType.KRoolOrder
        UpdateHint(hint_location, associated_hint)

    # Dirt patch hints are already garbage anyway - no restrictions here
    # for i in range(hint_distribution[HintType.DirtPatch]):
    #     dirt_patch_name = spoiler.settings.random.choice(spoiler.dirt_patch_placement)
    #     hint_location = getRandomHintLocation()
    #     message = f"There is a dirt patch located at {dirt_patch_name}"
    #     hint_location.hint_type = HintType.DirtPatch
    #     UpdateHint(hint_location, message)

    # Very useless hint, can be found at Cranky's anyway
    # for i in range(hint_distribution[HintType.MedalsRequired]):
    #     hint_location = getRandomHintLocation()
    #     message = f"{spoiler.settings.medal_requirement} medals are required to access Jetpac."
    #     hint_location.hint_type = HintType.MedalsRequired
    #     UpdateHint(hint_location, message)

    # Finally, place our joke hints
    for i in range(hint_distribution[HintType.Joke]):
        hint_location = getRandomHintLocation(random=spoiler.settings.random)
        if i > 4:
            message = "What do you think I am, a comedian? Try again in another seed."
        else:
            joke_hint_list = hint_list.copy()
            spoiler.settings.random.shuffle(joke_hint_list)
            message = joke_hint_list.pop().hint
        # Way of the Bean joke hint - yes, this IS worth it
        if message == "[[WOTB]]":
            bean_location_id = None
            for id, location in spoiler.LocationList.items():
                if location.item == Items.Bean:
                    bean_location_id = id
            # If we didn't find the bean, just get another joke hint :(
            if bean_location_id is None:
                message = joke_hint_list.pop()
            else:
                bean_region = spoiler.RegionList[GetRegionIdOfLocation(spoiler, bean_location_id)]
                hinted_location_text = bean_region.getHintRegionName()
                message = f"The Way of the Bean concludes in the {hinted_location_text}."
                hint_location.related_location = bean_location_id
        hint_location.hint_type = HintType.Joke
        UpdateHint(hint_location, message)

    # # DEBUG CODE to alert when a hint is empty
    # for hint in hints:
    #     if hint.hint == "":
    #         print("RED ALERT")

    ScoreCompleteHintSet(spoiler, hint_distribution, multipath_dict_goals)
    # Commented out for now: a system to forcibly hint your most-unhinted location with a sufficiently low unhinted score
    # This may be implemented once I have a better idea of how effective the unhinted score is
    # If we have a seed with sufficient unhintedness
    # if spoiler.unhinted_score >= 1:
    #     # Find the ugliest unhinted location
    #     ugliest_location = None
    #     for location, score in spoiler.poor_scoring_locations.items():
    #         # Min score threshold to be "ugly" is set at 1.0
    #         if score >= 1 and (ugliest_location is None or spoiler.poor_scoring_locations[ugliest_location] < score):
    #             ugliest_location = location
    #     # If we have an ugly location worth making a new WotH hint for...
    #     if ugliest_location is not None:
    #         # And we have a lesser hint door to actually put the hint on...
    #         swappable_hint_count = hint_distribution[HintType.Joke] + hint_distribution[HintType.FoolishRegion] + hint_distribution[HintType.RegionItemCount]
    #         if swappable_hint_count > 0:
    #             # Pick one of those hint doors, ideally respecting hint location accessibility, but needs must
    #             eligible_hint_doors = [hint for hint in hints if hint.hint_type in (HintType.Joke, HintType.FoolishRegion, HintType.RegionItemCount)]
    #             if ugliest_location in spoiler.accessible_hints_for_location.keys():
    #                 eligible_hint_doors = [
    #                     hint for hint in eligible_hint_doors if hint in getHintLocationsForAccessibleHintItems(spoiler.accessible_hints_for_location[ugliest_location], include_occupied=True)
    #                 ]
    #             door_to_swap = spoiler.settings.random.choice(eligible_hint_doors)
    #             # Swap this door's hint type to WotHLocation and update the hint's message
    #             hint_distribution[door_to_swap.hint_type] -= 1
    #             hint_distribution[HintType.WothLocation] += 1
    #             door_to_swap.hint_type = HintType.WothLocation
    #             door_to_swap.related_location = ugliest_location
    #             globally_hinted_location_ids.append(ugliest_location)
    #             hint_color = level_colors[spoiler.LocationList[ugliest_location].level]
    #             message = f"{hint_color}{spoiler.LocationList[ugliest_location].name}{hint_color} is on the \x04Way of the Hoard\x04."
    #             UpdateHint(door_to_swap, message)
    #             ScoreCompleteHintSet(spoiler, hint_distribution, multipath_dict_goals)
    #             spoiler.hint_swap_advisory = spoiler.LocationList[ugliest_location].name + " was deemed too unhinted and given a hint."

    UpdateSpoilerHintList(spoiler)
    spoiler.hint_distribution = hint_distribution

    # Dim hints - these are only useful (and doable) if item rando is on
    if spoiler.settings.dim_solved_hints and spoiler.settings.shuffle_items:
        AssociateHintsWithFlags(spoiler)

    return True


def getRandomHintLocation(random, location_list=None, kongs=None, levels=None, move_name=None) -> HintLocation:
    """Return an unoccupied hint location. The parameters can be used to specify location requirements."""
    valid_unoccupied_hint_locations = [
        hint
        for hint in hints
        if hint.hint == ""
        and (location_list is None or hint in location_list)
        and (kongs is None or hint.kong in kongs)
        and (levels is None or hint.level in levels)
        and move_name not in hint.banned_keywords
    ]
    # If it's too specific, we may not be able to find any
    if len(valid_unoccupied_hint_locations) == 0:
        return None
    hint_location = random.choice(valid_unoccupied_hint_locations)
    # Update the reference so we're updating the main list instead of a copy of it
    for hint in hints:
        if hint.name == hint_location.name:
            return hint
    return None


def getHintLocationsForAccessibleHintItems(hint_item_ids: Union[Set[Items], List[Items]], include_occupied=False) -> List[Union[HintLocation, Any]]:
    """Given a list of hint item ids, return unoccupied HintLocation objects they correspond to, possibly returning an empty list."""
    accessible_hints = []
    for item_id in hint_item_ids:
        item = ItemList[item_id]
        matching_hint = [hint for hint in hints if hint.level == item.level and hint.kong == item.kong][0]  # Should only match one
        accessible_hints.append(matching_hint)
    if include_occupied:
        return accessible_hints
    return [hint for hint in accessible_hints if hint.hint == ""]  # Filter out the occupied ones


def getDoorRestrictionsForItem(spoiler: Spoiler, item: Items):
    """Given the input item, return a list of HintLocation objects that hints for this item must be in."""
    accessible_hints = []
    # Progressive hints need additional restrictions to feel good
    if spoiler.settings.progressive_hint_item != ProgressiveHintItem.off:
        # If we're not in LZR, Keys that unlock levels are awful to get on the last few hints
        if spoiler.settings.logic_type != LogicType.nologic and spoiler.settings.shuffle_loading_zones != ShuffleLoadingZones.all:
            # In SLO, we know what order we'll find keys in, which can put early keys even earlier
            if not spoiler.settings.hard_level_progression:
                if item in (Items.JungleJapesKey, Items.AngryAztecKey):  # Key 1/2 hints by pack 5
                    accessible_hints = [hint for hint in Items if hint >= Items.JapesDonkeyHint and hint <= Items.GalleonChunkyHint]
                if item in (Items.FranticFactoryKey, Items.GloomyGalleonKey):  # Key 3/4 hints by pack 7
                    accessible_hints = [hint for hint in Items if hint >= Items.JapesDonkeyHint and hint <= Items.CavesLankyHint]
                if item == Items.FungiForestKey:  # Key 5 hints by pack 8
                    accessible_hints = [hint for hint in Items if hint >= Items.JapesDonkeyHint and hint <= Items.CastleDiddyHint]
            # We don't know what order we'll find these keys in, but level unlocking key hints should at least show up before last three hints
            else:
                if item in (Items.JungleJapesKey, Items.AngryAztecKey, Items.GloomyGalleonKey, Items.FungiForestKey):
                    accessible_hints = [hint for hint in Items if hint >= Items.JapesDonkeyHint and hint <= Items.CastleDiddyHint]
        # In progressive hints, Kongs hints must be available by or before pack 5
        if item in (Items.Donkey, Items.Diddy, Items.Lanky, Items.Tiny, Items.Chunky):
            accessible_hints = [hint for hint in Items if hint >= Items.JapesDonkeyHint and hint <= Items.GalleonChunkyHint]
    return accessible_hints


def pushHintToList(hint: Hint):
    """Push hint to hint list."""
    hint_list.append(hint)


def resetHintList():
    """Reset hint list to default state."""
    for hint in hint_list:
        if not hint.base:
            hint_list.remove(hint)
        else:
            hint.used = False
            hint.important = hint.was_important
            hint.repeats = hint.original_repeats
            hint.priority = hint.original_priority


def getHelmProgItems(spoiler: Spoiler) -> list:
    """Get the items needed to progress to helm."""
    base_list = [Items.Monkeyport, Items.GorillaGone]
    if spoiler.settings.switchsanity:
        switch_item_data = {
            SwitchType.PadMove: [
                Items.BaboonBlast,
                Items.SimianSpring,
                Items.BaboonBalloon,
                Items.Monkeyport,
                Items.GorillaGone,
            ],
            SwitchType.InstrumentPad: [Items.Bongos, Items.Guitar, Items.Trombone, Items.Saxophone, Items.Triangle],
            SwitchType.MiscActivator: [Items.GorillaGrab, Items.ChimpyCharge],
        }
        switches = [Switches.IslesMonkeyport, Switches.IslesHelmLobbyGone]
        for switch_index, switch in enumerate(switches):
            data = spoiler.settings.switchsanity_data[switch]
            base_list[switch_index] = switch_item_data[data.switch_type][data.kong]
    return base_list


SHOPKEEPER_ITEMS = [Items.Cranky, Items.Candy, Items.Funky, Items.Snide]
INSTRUMENT_ITEMS = [Items.Bongos, Items.Guitar, Items.Trombone, Items.Saxophone, Items.Triangle]


def compileMicrohints(spoiler: Spoiler) -> None:
    """Create guaranteed level + kong hints for various items."""
    spoiler.microhints = {}
    slam_levels = []
    helm_prog_items = getHelmProgItems(spoiler)
    microhint_categories = {
        MicrohintsEnabled.off: SHOPKEEPER_ITEMS.copy(),
        MicrohintsEnabled.base: helm_prog_items.copy() + [Items.ProgressiveSlam] + SHOPKEEPER_ITEMS.copy(),
        MicrohintsEnabled.all: helm_prog_items.copy() + INSTRUMENT_ITEMS.copy() + SHOPKEEPER_ITEMS.copy() + [Items.ProgressiveSlam],
    }
    items_needing_microhints = microhint_categories[spoiler.settings.microhints_enabled].copy()
    # Loop through locations looking for the items that need a microhint
    for id, location in spoiler.LocationList.items():
        if location.item in items_needing_microhints:
            item = ItemList[location.item]
            level_color = level_colors[location.level]
            if location.item == Items.ProgressiveSlam:
                # Chunky Phase slam hint
                if id not in PreGivenLocations and id not in TrainingBarrelLocations:  # Ignore anything pre-given
                    if location.level not in slam_levels:
                        slam_levels.append(location.level)
            elif location.item in (Items.Cranky, Items.Funky, Items.Snide, Items.Candy):
                hint_text = f"{item.name} has gone on vacation to the {vacation_levels_properties[location.level]} of {level_color}{level_list[location.level]}{level_color}."
                spoiler.microhints[item.name] = hint_text.upper()
            else:
                if location.type in item_type_names.keys():
                    hint_text = f"You would be better off looking for {item_type_names[location.type]} in {level_color}{level_list[location.level]}{level_color} for this.".upper()
                elif location.type == Types.Shop:
                    hint_text = f"You would be better off looking for shops in {level_color}{level_list[location.level]}{level_color} for this.".upper()
                else:
                    hint_text = f"You would be better off looking in {level_color}{level_list[location.level]}{level_color} with {kong_list[location.kong]} for this.".upper()
                settings_values = [
                    spoiler.settings.kong_model_dk,
                    spoiler.settings.kong_model_diddy,
                    spoiler.settings.kong_model_lanky,
                    spoiler.settings.kong_model_tiny,
                    spoiler.settings.kong_model_chunky,
                ]
                for index, val in enumerate(settings_values):
                    if val == KongModels.krusha:
                        if index == location.kong:
                            hint_text = hint_text.replace(colorless_kong_list[location.kong].upper(), "KRUSHA")
                spoiler.microhints[item.name] = hint_text
    if len(slam_levels) > 0:
        slam_levels.sort(key=lambda level: level.value)  # Sort the slam levels so they are in order
        slam_text_entries = [f"{level_colors[x]}{level_list[x]}{level_colors[x]}" for x in slam_levels]
        slam_text = " or ".join(slam_text_entries)
        spoiler.microhints[ItemList[Items.ProgressiveSlam].name] = (
            f"Ladies and Gentlemen! It appears that one fighter has come unequipped to properly handle this reptilian beast. Perhaps they should have looked in {slam_text} for the elusive slam.".upper()
        )


def compileSpoilerHints(spoiler):
    """Assemble the specified spoiler-style hints. See SpoilerHints enum for a list of all options."""
    starting_info = StartingSpoiler(spoiler.settings)
    spoiler.level_spoiler = {
        Levels.JungleJapes: LevelSpoiler(level_list[Levels.JungleJapes]),
        Levels.AngryAztec: LevelSpoiler(level_list[Levels.AngryAztec]),
        Levels.FranticFactory: LevelSpoiler(level_list[Levels.FranticFactory]),
        Levels.GloomyGalleon: LevelSpoiler(level_list[Levels.GloomyGalleon]),
        Levels.FungiForest: LevelSpoiler(level_list[Levels.FungiForest]),
        Levels.CrystalCaves: LevelSpoiler(level_list[Levels.CrystalCaves]),
        Levels.CreepyCastle: LevelSpoiler(level_list[Levels.CreepyCastle]),
        Levels.HideoutHelm: LevelSpoiler(level_list[Levels.HideoutHelm]),
        Levels.DKIsles: LevelSpoiler(level_list[Levels.DKIsles]),
        # Levels.Shops: LevelSpoiler(level_list[Levels.Shops]),
    }
    # Identify which items are worth hinting
    important_items = (
        ItemPool.Keys()
        + ItemPool.Kongs(spoiler.settings)
        + ItemPool.AllKongMoves()
        + ItemPool.TrainingBarrelAbilities()
        + [Items.Bean, Items.Camera, Items.Shockwave, Items.CameraAndShockwave]
        + ItemPool.CrankyItems()
        + ItemPool.FunkyItems()
        + ItemPool.CandyItems()
        + ItemPool.SnideItems()
        + ItemPool.ClimbingAbilities()
    )
    # Idenfity what moves among our starting items cannot be hinted. This is to aid trackers in communicating what starting moves count towards the WotH count.
    if spoiler.settings.climbing_status == ClimbingStatus.normal:
        starting_info.starting_moves_not_hintable.append(Items.Climbing)
    if spoiler.settings.shockwave_status == ShockwaveStatus.start_with:
        starting_info.starting_moves_not_hintable.extend([Items.Camera, Items.Shockwave, Items.CameraAndShockwave])
    if spoiler.settings.training_barrels == TrainingBarrels.normal and spoiler.settings.fast_start_beginning_of_game:
        starting_info.starting_moves_not_hintable.extend(ItemPool.TrainingBarrelAbilities())
    if spoiler.settings.start_with_slam and spoiler.settings.fast_start_beginning_of_game:
        starting_info.starting_moves_not_hintable.append(Items.ProgressiveSlam)
    starting_info.starting_moves_not_hintable = [ItemList[item].name for item in starting_info.starting_moves_not_hintable]
    # Sort the items by level they're found in
    for location_id in spoiler.LocationList.keys():
        location = spoiler.LocationList[location_id]
        level_of_location = location.level
        if level_of_location == Levels.Shops:  # Jetpac and BlueprintBananas - we want Jetpac in Isles now, but we probably won't want BlueprintBananas there too when those start shuffling
            level_of_location = Levels.DKIsles
        if location.item in important_items:
            item_obj = ItemList[location.item]
            # If this location/item is pre-given before you even enter the seed, it doesn't count for points. This leads to a messy if statement, so here's the breakdown:
            # 1. The Climbing location, pre-given moves (with one exception!), and the pre-given shopkeeper locations are all always on the title screen.
            # 2. Training barrel locations are only pre-given if fast start is on
            # 3. The exception: IslesFirstMove (the Simian Slam location) is only pre-given if fast start is on
            if (
                (location.type in (Types.Climbing, Types.PreGivenMove, Types.Cranky, Types.Candy, Types.Funky, Types.Snide) and location_id != Locations.IslesFirstMove)
                or (spoiler.settings.fast_start_beginning_of_game and location.type == (Types.TrainingBarrel))
                or (location_id == Locations.IslesFirstMove and spoiler.settings.fast_start_beginning_of_game)
            ):
                starting_info.starting_moves.append(item_obj.name)
                # Starting shopkeepers are never hintable
                if location.type in (Types.Cranky, Types.Candy, Types.Funky, Types.Snide):
                    starting_info.starting_moves_not_hintable.append(item_obj.name)
                if location_id in spoiler.woth_locations:
                    starting_info.starting_moves_woth_count += 1
            else:
                spoiler.level_spoiler[level_of_location].vial_colors.append(CategorizeItem(item_obj))
                spoiler.level_spoiler[level_of_location].points += PointValueOfItem(spoiler.settings, location.item)
                if location_id in spoiler.woth_locations:
                    spoiler.level_spoiler[level_of_location].woth_count += 1
    # Convert those spoiler hints to readable text
    spoiler.level_spoiler_human_readable = {
        level_list[Levels.DKIsles]: "",
        level_list[Levels.JungleJapes]: "",
        level_list[Levels.AngryAztec]: "",
        level_list[Levels.FranticFactory]: "",
        level_list[Levels.GloomyGalleon]: "",
        level_list[Levels.FungiForest]: "",
        level_list[Levels.CrystalCaves]: "",
        level_list[Levels.CreepyCastle]: "",
        level_list[Levels.HideoutHelm]: "",
        # level_list[Levels.Shops]: "",
    }
    for level in spoiler.level_spoiler.keys():
        # Clear out variables if they're unused or undesired
        if not spoiler.settings.spoiler_include_woth_count:
            spoiler.level_spoiler[level].woth_count = -1
            starting_info.starting_moves_woth_count = -1
        if spoiler.settings.spoiler_hints != SpoilerHints.vial_colors:
            spoiler.level_spoiler[level].vial_colors = []
        if spoiler.settings.spoiler_hints != SpoilerHints.points:
            spoiler.level_spoiler[level].points = -1
        # Create the text that will be human-readable on the site
        if spoiler.settings.spoiler_hints == SpoilerHints.vial_colors:
            # Sort the kongs/keys/vials in each level for readability
            spoiler.level_spoiler[level].vial_colors.sort()
            spoiler.level_spoiler_human_readable[level_list[level]] = "Items: " + ", ".join(spoiler.level_spoiler[level].vial_colors)
        if spoiler.settings.spoiler_hints == SpoilerHints.points:
            spoiler.level_spoiler_human_readable[level_list[level]] = "Points: " + str(spoiler.level_spoiler[level].points)
        if spoiler.settings.spoiler_include_woth_count:
            spoiler.level_spoiler_human_readable[level_list[level]] += " | WotH Items: " + str(spoiler.level_spoiler[level].woth_count)
    spoiler.level_spoiler["starting_info"] = starting_info
    spoiler.level_spoiler_human_readable["Starting Info"] = "Starting Kongs: " + ", ".join([colorless_kong_list[kong] for kong in starting_info.starting_kongs])
    spoiler.level_spoiler_human_readable["Starting Info"] += " | Starting Keys: " + ", ".join(starting_info.starting_keys)
    spoiler.level_spoiler_human_readable["Starting Info"] += " | Starting Moves: " + ", ".join(starting_info.starting_moves)
    if spoiler.settings.spoiler_include_woth_count:
        spoiler.level_spoiler_human_readable["Starting Info"] += " | Starting Move WotH Count: " + str(starting_info.starting_moves_woth_count)
    spoiler.level_spoiler_human_readable["Starting Info"] += " | Helm Order: " + ", ".join([colorless_kong_list[kong] for kong in starting_info.helm_order])
    spoiler.level_spoiler_human_readable["Starting Info"] += " | K. Rool Order: " + ", ".join([boss_names[map_id] for map_id in starting_info.krool_order])
    if spoiler.settings.spoiler_include_level_order:
        spoiler.level_spoiler_human_readable["Starting Info"] += " | Level Order: " + ", ".join([level_list[level] for level in starting_info.level_order])
    if spoiler.settings.spoiler_hints == SpoilerHints.points:
        spoiler.level_spoiler["point_spread"] = {
            "kongs": spoiler.settings.points_list_kongs,
            "keys": spoiler.settings.points_list_keys,
            "guns": spoiler.settings.points_list_guns,
            "instruments": spoiler.settings.points_list_instruments,
            "active_moves": spoiler.settings.points_list_active_moves,
            "pad_moves": spoiler.settings.points_list_pad_moves,
            "barrel_moves": spoiler.settings.points_list_barrel_moves,
            "training_moves": spoiler.settings.points_list_training_moves,
            "fairy_moves": spoiler.settings.points_list_fairy_moves,
            "important_shared_moves": spoiler.settings.points_list_important_shared,
            "bean": spoiler.settings.points_list_bean,
            "shopkeepers": spoiler.settings.points_list_shopkeepers,
        }
        spoiler.level_spoiler_human_readable["Point Spread"] = (
            "Kongs: "
            + str(spoiler.settings.points_list_kongs)
            + " | Keys: "
            + str(spoiler.settings.points_list_keys)
            + " | Guns: "
            + str(spoiler.settings.points_list_guns)
            + " | Instruments: "
            + str(spoiler.settings.points_list_instruments)
            + " | Active Moves: "
            + str(spoiler.settings.points_list_active_moves)
            + " | Pad Moves: "
            + str(spoiler.settings.points_list_pad_moves)
            + " | Barrel Moves: "
            + str(spoiler.settings.points_list_barrel_moves)
            + " | Training Moves: "
            + str(spoiler.settings.points_list_training_moves)
            + " | Fairy Moves: "
            + str(spoiler.settings.points_list_fairy_moves)
            + " | Shared Moves: "
            + str(spoiler.settings.points_list_important_shared)
            + " | Bean: "
            + str(spoiler.settings.points_list_bean)
            + " | Shopkeepers: "
            + str(spoiler.settings.points_list_shopkeepers)
        )


def CategorizeItem(item):
    """Identify the hint string for the given item."""
    if item.type in (Types.Kong, Types.Cranky, Types.Funky, Types.Candy, Types.Snide):
        return "Kong"
    elif item.type == Types.Key:
        return "Key"
    elif item.type == Types.Bean:
        return "Bean"
    elif item.kong == Kongs.donkey:
        return "Yellow Vial"
    elif item.kong == Kongs.diddy:
        return "Red Vial"
    elif item.kong == Kongs.lanky:
        return "Blue Vial"
    elif item.kong == Kongs.tiny:
        return "Purple Vial"
    elif item.kong == Kongs.chunky:
        return "Green Vial"
    elif item.kong == Kongs.any:
        return "Clear Vial"


def PointValueOfItem(settings, item_id):
    """Determine the point value of this item."""
    if item_id in [Items.Donkey, Items.Diddy, Items.Lanky, Items.Tiny, Items.Chunky]:
        return settings.points_list_kongs
    elif item_id in ItemPool.Keys():
        return settings.points_list_keys
    elif item_id in [Items.Coconut, Items.Peanut, Items.Grape, Items.Feather, Items.Pineapple]:
        return settings.points_list_guns
    elif item_id in [Items.Bongos, Items.Guitar, Items.Trombone, Items.Saxophone, Items.Triangle]:
        return settings.points_list_instruments
    elif item_id in [Items.GorillaGrab, Items.ChimpyCharge, Items.Orangstand, Items.PonyTailTwirl, Items.PrimatePunch]:
        return settings.points_list_active_moves
    elif item_id in [Items.BaboonBlast, Items.SimianSpring, Items.BaboonBalloon, Items.Monkeyport, Items.GorillaGone]:
        return settings.points_list_pad_moves
    elif item_id in [
        Items.StrongKong,
        Items.RocketbarrelBoost,
        Items.OrangstandSprint,
        Items.MiniMonkey,
        Items.HunkyChunky,
    ]:
        return settings.points_list_barrel_moves
    elif item_id in ItemPool.TrainingBarrelAbilities():
        return settings.points_list_training_moves
    elif item_id in ItemPool.ClimbingAbilities():
        return settings.points_list_training_moves
    elif item_id in ItemPool.ImportantSharedMoves:
        return settings.points_list_important_shared
    elif item_id == Items.Bean:
        return settings.points_list_bean
    elif item_id in ItemPool.ShockwaveTypeItems(settings):
        return settings.points_list_fairy_moves
    elif item_id in [Items.Cranky, Items.Funky, Items.Candy, Items.Snide]:
        return settings.points_list_shopkeepers
    return 0


def TryCreatingLoadingZoneHint(spoiler: Spoiler, transition: Transitions, disallowedRegions: Optional[List[Regions]] = None) -> str:
    """Try to create a hint message for the given transition. If this hint is determined to be bad, it will return false and not place the hint."""
    if disallowedRegions is None:
        disallowedRegions = []
    pathToHint = transition
    # Don't hint entrances from dead-end rooms, follow the reverse pathway back until finding a place with multiple entrances
    if spoiler.settings.decoupled_loading_zones:
        while ShufflableExits[pathToHint].category is None:
            originPaths = [x for x, back in spoiler.shuffled_exit_data.items() if back.reverse == pathToHint]
            # In a few cases, there is no reverse loading zone. In this case we must keep the original path to hint
            if len(originPaths) == 0:
                break
            pathToHint = originPaths[0]
    # With coupled loading zones, never hint from a dead-end room, since it is forced to be coming from the same destination
    elif ShufflableExits[pathToHint].category is None:
        return ""
    # Validate the region of the hinted entrance is not in disallowedRegions
    if ShufflableExits[pathToHint].region in disallowedRegions:
        return ""
    # Validate the hinted destination is not the same as the hinted origin
    entranceMap = GetMapId(spoiler.settings, ShufflableExits[pathToHint].region)
    destinationMap = GetMapId(spoiler.settings, spoiler.shuffled_exit_data[transition].regionId)
    if entranceMap == destinationMap:
        return ""
    entranceName = ShufflableExits[pathToHint].name
    destinationName: str = spoiler.shuffled_exit_data[transition].spoilerName
    fromExitName = destinationName.find(" from ")
    if fromExitName != -1:
        # Remove exit name from destination
        destinationName = destinationName[:fromExitName]
    return f"If you're looking for \x04{destinationName}\x04, follow the path \x08from {entranceName}\x08."


def GetConnectedEntrances(spoiler: Spoiler, target_map: Maps, target_transitions: List[Transitions]) -> List[Transitions]:
    """Given a map, find all entrances that lead to this map, possibly even seeking specific transitions."""
    relevant_entrances = []
    for transitionId, exit in ShufflableExits.items():
        destinationMap = None
        destinationTransition = None
        # If the exit of this transition is shuffled, check the shuffled data, otherwise check the bases data
        if exit.shuffled:
            shuffledBack = spoiler.shuffled_exit_data[transitionId]
            destinationMap = GetMapId(spoiler.settings, shuffledBack.regionId)
            destinationTransition = shuffledBack.reverse
        else:
            destinationMap = GetMapId(spoiler.settings, exit.back.regionId)
            destinationTransition = exit.back.reverse
        # If this transition reaches our target map, it's a relevant entrance
        if destinationMap == target_map and (not any(target_transitions) or destinationTransition in target_transitions):
            relevant_entrances.append(transitionId)
    return relevant_entrances


def UpdateSpoilerHintList(spoiler: Spoiler) -> None:
    """Write hints to spoiler object."""
    for hint in hints:
        spoiler.hint_list[hint.name] = hint.hint
        spoiler.short_hint_list[hint.name] = hint.short_hint if hint.short_hint is not None else hint.hint


def GetRegionIdOfLocation(spoiler: Spoiler, location_id: Locations) -> Regions:
    """Given the id of a Location, return the Region it belongs to."""
    location = spoiler.LocationList[location_id]
    # Shop locations are tied to the level, not the shop regions
    if location.type == Types.Shop:
        for region_id in [id for id, reg in spoiler.RegionList.items() if reg.level == Levels.Shops]:
            if location_id in [location_logic.id for location_logic in spoiler.RegionList[region_id].locations if not location_logic.isAuxiliaryLocation]:
                return region_id
    for region_id in Regions:
        region = spoiler.RegionList[region_id]
        if region.level == location.level or location.type == Types.Hint:
            if location_id in [location_logic.id for location_logic in region.locations if not location_logic.isAuxiliaryLocation]:
                return region_id
    raise Exception(f"Unable to find Region for Location {location_id.name}")  # This should never trigger!


def GenerateMultipathDict(
    spoiler: Spoiler, useless_locations: Dict[Union[Items, Kongs], List[Any]]
) -> Tuple[Dict[Union[Locations, int], str], Dict[Union[Locations, int], List[Union[Locations, int]]]]:
    """Create multipath hint text and identify relevant goal locations for each eligible woth location.

    Returns two dicts.
    The hints dict will contain the hint texted needed for a multipath hint of the key's location.
    The goals dict will contain relevant locations for the purposes of identifying valid hint doors when placing multipath hints.
    """
    multipath_dict_hints = {}
    multipath_dict_goals = {}
    training_slam_hinted = False
    for location in spoiler.woth_locations:
        # Kongs are never on the path to anything (yet?) so we can just skip right over them
        # We don't want the Kongs' locations to be path hinted, as they already get hinted elsewhere
        if spoiler.LocationList[location].item in [Items.Donkey, Items.Diddy, Items.Lanky, Items.Tiny, Items.Chunky]:
            continue
        # In worlds where you start with multiple slams and it could be hinted, you'll get identical-looking hints for each slam location. We only want to create that hint once.
        if location in TrainingBarrelLocations or location in PreGivenLocations and spoiler.LocationList[location].item == Items.ProgressiveSlam:
            if training_slam_hinted:
                continue
            training_slam_hinted = True
        path_to_keys = []
        path_to_krool_phases = []
        path_to_camera = []
        relevant_goal_locations = []
        path_to_family = False
        path_to_verses = [False] * 6
        has_path_to_verse = False
        verse_items = [
            # These do NOT contain the main kongs, as that's hinted by the freeing kongs path
            [Items.Coconut, Items.StrongKong],
            [Items.MiniMonkey, Items.PonyTailTwirl, Items.Climbing],
            [Items.Orangstand, Items.BaboonBalloon, Items.Trombone],
            [Items.RocketbarrelBoost, Items.Peanut, Items.Guitar],
            [Items.Barrels],
            [Items.Cranky, Items.Peanut, Items.Pineapple, Items.Grape, Items.Oranges, Items.Coconut],
        ]
        verse_names = ["Donkey", "Tiny", "Lanky", "Diddy", "Chunky", "The Fridge"]
        verse_colors = ["\x04", "\x07", "\x06", "\x05", "\x08", "\x0a"]
        # Determine which keys and kongs this location is on the path to
        for woth_loc in spoiler.woth_paths.keys():
            if location in spoiler.woth_paths[woth_loc]:
                endpoint_item = ItemList[spoiler.LocationList[woth_loc].item]
                if endpoint_item.type == Types.Key:
                    path_to_keys.append(str(endpoint_item.index))
                    relevant_goal_locations.append(Locations(woth_loc))
                if endpoint_item.type == Types.Kong:
                    path_to_family = True
                    relevant_goal_locations.append(Locations(woth_loc))
                if spoiler.settings.win_condition_item == WinConditionComplex.dk_rap_items:
                    item = spoiler.LocationList[woth_loc].item
                    for verse_index, verse in enumerate(verse_items):
                        if item in verse:
                            path_to_verses[verse_index] = True
                            has_path_to_verse = True
                            relevant_goal_locations.append(Locations(woth_loc))
        # For path to family, we also have to check non-woth paths
        for non_woth_loc in spoiler.other_paths.keys():
            if location in spoiler.other_paths[non_woth_loc]:
                endpoint_item = ItemList[spoiler.LocationList[non_woth_loc].item]
                if endpoint_item.type == Types.Kong:
                    path_to_family = True
        # Determine which K. Rool phases this is on the path to (if relevant)
        if spoiler.settings.win_condition_item == WinConditionComplex.beat_krool:
            for map_id in spoiler.krool_paths.keys():
                if location in spoiler.krool_paths[map_id]:
                    path_to_krool_phases.append(boss_colors[map_id] + boss_names[map_id] + boss_colors[map_id])
                    relevant_goal_locations.append(Maps(map_id))
        # Determine if this location is on the path to taking photos for certain win conditions
        if spoiler.settings.win_condition_item in (WinConditionComplex.req_fairy, WinConditionComplex.krem_kapture) and spoiler.settings.shockwave_status != ShockwaveStatus.start_with:
            camera_location_id = None
            for id, loc in spoiler.LocationList.items():
                if loc.item in (Items.Camera, Items.CameraAndShockwave):
                    camera_location_id = id
                    break
            if camera_location_id in spoiler.woth_paths.keys() and location in spoiler.woth_paths[camera_location_id]:
                path_to_camera.append("\x07taking photos\x07")
                relevant_goal_locations.append(Locations(camera_location_id))
        # Some locations are useless to hint on the path to some goals - every hint we construct should be useful
        if location in TrainingBarrelLocations or location in PreGivenLocations or location == Locations.HelmKey:
            # This is the assumed number of useful paths there are to hint for this location
            useful_path_count = len(path_to_keys) + len(path_to_krool_phases)
            for goal in useless_locations.keys():
                # If a goal contains this location as a useless path, it no longer counts as a useful path to hint
                if location in useless_locations[goal]:
                    useful_path_count -= 1
            # If at the end this location is not useful to hint on any paths, then it is not eligible for a multipath hint
            if useful_path_count <= 0:
                continue
        # Join the Key and K. Rool text together into what will be the core of the hint text
        hint_text_components = []
        if len(path_to_keys) > 0:
            path_to_keys.sort()
            key_text = "\x04Keys "
            if len(path_to_keys) == 1:
                key_text = "\x04Key "
            amount_of_keys_required = len(spoiler.settings.krool_keys_required)
            if amount_of_keys_required > 1 and len(path_to_keys) == amount_of_keys_required:
                hint_text_components.append("\x04All Keys\x04")
            else:
                hint_text_components.append(key_text + join_words(path_to_keys) + "\x04")
        if len(path_to_krool_phases) > 0:
            hint_text_components.append("Final " + join_words(path_to_krool_phases))
        if len(path_to_camera) > 0:
            hint_text_components.append(path_to_camera[0])
        if path_to_family:
            hint_text_components.append("\x04Free Kongs\x04")
        if spoiler.settings.win_condition_item == WinConditionComplex.dk_rap_items:
            all_verses = [xi for xi, x in enumerate(path_to_verses) if x]
            if len(all_verses) == 6:
                hint_text_components.append("All Verses")
            else:
                kong_verses = [xi for xi, x in enumerate(path_to_verses) if x and xi < 5]
                if len(kong_verses) == 5:
                    hint_text_components.append("All Kong Verses")
                else:
                    if len(kong_verses) == 1:
                        verse_index = kong_verses[0]
                        pushed_name = f"{verse_names[verse_index]} Verse"
                        hint_text_components.append(f"{verse_colors[verse_index]}{pushed_name}{verse_colors[verse_index]}")
                    elif len(kong_verses) > 1:
                        kong_names = [f"{verse_colors[x]}{verse_names[x]}{verse_colors[x]}" for x in kong_verses]
                        hint_text_components.append(f"{join_words(kong_names)} Verses")
                if path_to_verses[5]:
                    hint_text_components.append(f"{verse_colors[5]}The Fridge{verse_colors[5]}")
        if len(path_to_keys) + len(path_to_krool_phases) + len(path_to_camera) > 0 or path_to_family or has_path_to_verse:
            multipath_dict_hints[location] = join_words(hint_text_components)
            multipath_dict_goals[location] = relevant_goal_locations
    return multipath_dict_hints, multipath_dict_goals


def join_words(words: List[str]) -> str:
    """Join a list of words with an 'and' for grammatical perfection."""
    if len(words) > 2:
        return "%s, and %s" % (", ".join(words[:-1]), words[-1])
    else:
        return " and ".join(words)


def GenerateMultipathHintMessageForLocation(spoiler, loc, multipath_dict_hints, shortenText=False):
    """Generate a multipath hint message for the desired location, assuming it is a valid location."""
    region = spoiler.RegionList[GetRegionIdOfLocation(spoiler, loc)]
    hinted_location_text = level_colors[region.level] + region.getHintRegionName() + level_colors[region.level]
    if loc in TrainingBarrelLocations or loc in PreGivenLocations:
        # Starting moves could be a lot of things - instead of being super vague we'll hint the specific item directly.
        hinted_item_name = ItemList[spoiler.LocationList[loc].item].name
        message = f"\x0b{hinted_item_name}\x0b is on the path to {multipath_dict_hints[loc]}."
        hinted_location_text = f"\x0b{hinted_item_name}\x0b"
    elif region.isCBRegion():
        # Medal rewards and bosses are treated as "collecting colored bananas" for their region
        hinted_location_text = f"{level_colors[region.level]}{short_level_list[region.level]} Colored Bananas{level_colors[region.level]}"
        message = f"Something about collecting {hinted_location_text} is on the path to {multipath_dict_hints[loc]}."
    else:
        message = f"Something in the {hinted_location_text} is on the path to {multipath_dict_hints[loc]}."
    if shortenText:
        # In an attempt to avoid the dreaded '...' in the pause menu, remove more of the fluff for short_hint
        message = f"{hinted_location_text}: Path to {multipath_dict_hints[loc]}"
    return message


def IsMultipathHintTooLong(message):
    """Determine if the input multipath hint needs shortening."""
    measure_message_size = message
    measure_message_size_nospace = message
    for character in ["\x04", "\x05", "\x06", "\x07", "\x08", "\x09", "\x0a", "\x0b", "\x0c", "\x0d"]:
        if character in measure_message_size:
            measure_message_size = measure_message_size.replace(character, "")
    measure_message_size_nospace = measure_message_size.replace(" ", "")
    # Also account for the fact that words are kept together when splitting across lines
    cutOff_1 = getNumberOfCutoffCharacters(measure_message_size, 50)
    cutOff_2 = getNumberOfCutoffCharacters(measure_message_size[(50 - cutOff_1) :], 50)
    effective_length = len(measure_message_size) + cutOff_1 + cutOff_2
    return len(message) > 255 or effective_length > 150 or len(measure_message_size_nospace) > 125


def getNumberOfCutoffCharacters(message, number):
    """Determine how many characters early a line would get cut off."""
    if number < 2 or len(message) < number:
        return 0
    index = number - 1
    initial_index = index
    while message[index] != " ":
        index -= 1
        if index == 0:
            index = initial_index
            break
    return initial_index - index


def AssociateHintsWithFlags(spoiler):
    """Associate hints with the related flag at their related location as applicable."""
    for hint in hints:
        if hint.related_location is not None:
            for location_selection in spoiler.item_assignment:
                if location_selection.location == hint.related_location:
                    hint.related_flag = location_selection.new_flag
                    break
        if hint.name != "First Time Talk":
            spoiler.tied_hint_flags[hint.name] = hint.related_flag if hint.related_flag is not None else 0xFFFF


def ApplyColorToPlandoHint(hint):
    """Replace plandomizer color tags with the appropriate characters."""
    new_hint = hint
    color_replace_dict = {}
    for code in plando_colors:
        for key in plando_colors[code]:
            color_replace_dict[f"[{key}]"] = code
            color_replace_dict[f"[/{key}]"] = code
    for color_tag, color_character in color_replace_dict.items():
        new_hint = new_hint.replace(color_tag, color_character)
    return new_hint


def ApplyPlandoHints(spoiler):
    """Apply plandomizer hint messages, returning the number of hints placed."""
    plando_hints_placed = 0
    for loc_id, message in spoiler.settings.plandomizer_dict["hints"].items():
        if message != "":
            final_message = ApplyColorToPlandoHint(message)
            location = spoiler.LocationList[int(loc_id)]
            hint_location = [hint_loc for hint_loc in hints if hint_loc.level == location.level and hint_loc.kong == location.kong][0]  # Matches exactly one hint
            UpdateHint(hint_location, final_message)
            hint_location.hint_type = HintType.Plando
            plando_hints_placed += 1
    return plando_hints_placed


def replaceKongNameWithKrusha(spoiler):
    """Replace Krusha's kong name."""
    settings_values = [
        spoiler.settings.kong_model_dk,
        spoiler.settings.kong_model_diddy,
        spoiler.settings.kong_model_lanky,
        spoiler.settings.kong_model_tiny,
        spoiler.settings.kong_model_chunky,
    ]
    for kong_index, kong in enumerate(settings_values):
        if kong == KongModels.krusha:
            kong_list[kong_index] = f"{kong_colors[kong_index]}Krusha{kong_colors[kong_index]}"
            colorless_kong_list[kong_index] = "Krusha"
            kong_cryptic[kong_index] = [
                "The kong that has... scales ?",
                "The kong that is normally only available in multiplayer",
                "The kong that is not a monkey",
                "The Kong that is not in the DK Rap",
                "The Kong that Rivals Chunky in Strength",
                "The Kong that replaces another Kong",
                "The Kong that wears Camo",
                "The Kong that was K. Rool's Bodyguard",
            ]


def getHelmOrderHint(spoiler):
    """Compile the Snide hint for the helm order."""
    file_index = 11
    default_order = [Kongs.donkey, Kongs.chunky, Kongs.tiny, Kongs.lanky, Kongs.diddy]
    helm_order = [default_order[room] for room in spoiler.settings.helm_order]
    kong_helm_order = [kong_list[x].upper() for x in helm_order]
    kong_order_text = ""
    if len(kong_helm_order) == 0:
        return
    elif len(kong_helm_order) == 1:
        kong_order_text = kong_helm_order[0]
    else:
        early_entries = kong_helm_order[:-1]
        early_entry_text = ", ".join(early_entries)
        kong_order_text = f"{early_entry_text} AND {kong_helm_order[-1]}"
    text_entries = [
        {
            # This isn't a game text
            "text_index": 3,
            "search": "BLUEPRINTS ARE VITAL TO US BOTH",
            "replace": "BLUEPRINTS HELP BUY | TIME TO SHUT DOWN THE MACHINE",
        },
        {
            # This isn't a joke text
            "text_index": 4,
            "search": "BLUEPRINTS AND SO DO YOU",
            "replace": "BLUEPRINTS TO BUY | TIME TO SHUT DOWN THE MACHINE",
        },
    ]
    for entry in text_entries:
        data = {
            "textbox_index": entry["text_index"],
            "mode": "replace",
            "search": entry["search"],
            "target": entry["replace"].replace("|", kong_order_text),
        }
        if file_index in spoiler.text_changes:
            spoiler.text_changes[file_index].append(data)
        else:
            spoiler.text_changes[file_index] = [data]


def ScoreCompleteHintSet(spoiler, hint_distribution, multipath_dict_goals):
    """Evaluate the strength of the hints and attempt to distill it into a score."""
    spoiler.unhinted_score = -1
    spoiler.poor_scoring_locations = {"N/A": "this hint system does not get scored"}
    # This evaluation only matters with multipath hints
    if hint_distribution[HintType.Multipath] > 0:
        spoiler.unhinted_score = 0
        spoiler.poor_scoring_locations = {}
        hint_tree = BuildPathHintTree(spoiler.woth_paths)
        # Some locations are known quantities and can be pruned from the tree
        del hint_tree[Locations.BananaHoard]
        if spoiler.settings.key_8_helm:
            if Locations.HelmKey in hint_tree:
                del hint_tree[Locations.HelmKey]
        # Decorate the tree with information from our placed hints
        for hint in hints:
            if hint.related_location is not None and hint.related_location in hint_tree.keys() and hint.hint_type != HintType.Joke:  # The WotB hint is a real jokester, eh?
                if hint.hint_type == HintType.Multipath:
                    hint_tree[hint.related_location].path_hinted = True
                else:
                    hint_tree[hint.related_location].woth_hinted = True
        for loc in hint_tree.keys():
            if loc in multipath_dict_goals.keys():
                hint_tree[loc].goals = multipath_dict_goals[loc]
            # I'm pretty sure this can only happen to training moves
            else:
                hint_tree[loc].goals = []
        # Loop through nodes, front-to-back, earliest items to latest items, applying unhinted_score based on the connections
        for node in hint_tree.values():
            node_location = spoiler.LocationList[node.node_location_id]
            location_item = ItemList[node_location.item]
            # If the item here is a Kong, it both can't be on the path to anything and is already given a required Kong hint
            if location_item.type == Types.Kong:
                continue
            # Medal locations and Bosses get an automatic x1.5 unhinted multiplier because they are awful to orphan
            if node_location.type in (Types.Medal, Types.Key):
                node.score_multiplier *= 1.5
            # Scores get a multplier boost if the location is not in the main map of a level. This is to simulate having to go out of your way to find this unhinted item.
            # This isn't a foolproof metric, but you are generally more likely to peek or check locations in the main map of each level.
            elif node_location.level != Levels.DKIsles and node_location.type != Types.Shop and node.node_location_id != Locations.RarewareCoin:
                # The exceptions:
                # 1. No Isles checks get this boost - all Isles checks are relatively accessible compared to a check deeper in a level.
                # 2. Shops do not get this boost. You're reasonably likely to look at shops, as most of them fall in the main map. This includes Jetpac.
                # 3. Boss and Medal locations are already getting a *hefty* multiplier and don't need any more.
                node_map = GetMapId(spoiler.settings, GetRegionIdOfLocation(spoiler, node.node_location_id))
                if node_map not in (Maps.JungleJapes, Maps.AngryAztec, Maps.FranticFactory, Maps.GloomyGalleon, Maps.FungiForest, Maps.CrystalCaves, Maps.CreepyCastle):
                    node.score_multiplier *= 1.1
            # Shop locations are much easier (or at least predictable) to find and peek their contents
            if node_location.type == Types.Shop:
                node.score_multiplier *= 0.4
            # Keys are always an endpoint of a path (unless it's DK Rap win con). These items should be the culmination of other hints and therefore highly unlikely to be unhinted.
            if spoiler.settings.win_condition_item != WinConditionComplex.dk_rap_items and location_item.type == Types.Key:
                node.score_multiplier *= 0.7
            # Training barrel locations don't matter if they're hinted or not because you start with them
            if node.node_location_id in TrainingBarrelLocations or node.node_location_id in PreGivenLocations:
                node.score_multiplier *= 0
            # If this location is hinted or isn't on the path to any goals, there's no further unhinted score changes required here
            if node.path_hinted or node.woth_hinted or len(node.goals) == 0:
                continue
            # The baseline unhinted score for a node is inversely proportional to the number of goals this location is on the path to
            # If something is on the path to a lot of goals, it's often found early and usually less disastrous to be missed
            node.unhinted_score += sqrt(1.0 / len(node.goals))
            for parent_loc_id in node.parents:
                parent_node = hint_tree[parent_loc_id]
                # If this is the only child of this parent and the parent is directly hinted, this is the only location that can resolve that hint.
                if len(parent_node.children) == 1 and (parent_node.path_hinted or parent_node.woth_hinted):
                    # Halve the unhinted contribution of this node per hinted solo-parent
                    node.score_multiplier *= 0.5
                # A woth-hinted location with multiple children means it could resolve in many ways, which could possibly leave this item effectively unhinted
                # If the parents are path hinted, we need to analyze siblings' goals to determine if this location uniquely solves some portion of the parent's path
                elif len(parent_node.children) > 1 and parent_node.path_hinted:
                    # Compile a list of all goals that the siblings are on the path to - this is always a subset of the parent's goals!
                    sibling_nodes = [hint_tree[loc_id] for loc_id in parent_node.children if loc_id != node.node_location_id and loc_id in hint_tree.keys()]
                    sibling_goals = set([goal for node in sibling_nodes for goal in node.goals])
                    # If this node has *any* goals that are unique to this location, then this is the only location that can resolve that portion of the parent's path hint.
                    if any(set(node.goals).difference(sibling_goals)):
                        # Because of that, it makes this less unhinted
                        node.score_multiplier *= 0.6
                    # Identify any particularly problematic siblings more directly
                    for child_loc_id in parent_node.children:
                        if child_loc_id != node.node_location_id and child_loc_id in hint_tree.keys():
                            child_node = hint_tree[child_loc_id]
                            # If a parent is path hinted and this sibling could resolve this node's goals, one of the two would be effectively unhinted
                            if set(node.goals).issubset(set(child_node.goals)):
                                # Split the difference - the current node being evaluated gets half the value
                                node.unhinted_score += 0.5
                                # If the goals *exactly* match, then the current node could mask their sibling, even if the sibling is hinted!
                                if node.goals == child_node.goals:
                                    child_node.unhinted_score += 0.5
                                # Note that if both are unhinted you'll double the score, which is appropriate for two unhinted items that could resolve the same path hint
        # Now that we've completed tree decoration, we can assess the damage - we have to do this at the end because sibling calculations can affect nodes that were previously calculated
        for node in hint_tree.values():
            node_score = node.unhinted_score * node.score_multiplier
            spoiler.unhinted_score += node_score
            # Arbitrary threshold of .25 to be worth mentioning in the spoiler
            if node_score > 0.25:
                node_location = spoiler.LocationList[node.node_location_id]
                spoiler.poor_scoring_locations[node_location.name + " (" + ItemList[node_location.item].name + ")"] = node_score


def CompileArchipelagoHints(spoiler: Spoiler, woth_hints: list, major_hints: list, deep_hints: list):
    """Insert Archipelago hints."""
    # All input lists are in the form of [loc.name, multiworld.get_player_name(loc.player), loc.item.name, multiworld.get_player_name(loc.item.player), isForeign]
    replaceKongNameWithKrusha(spoiler)
    ClearHintMessages()
    hints = woth_hints + major_hints + deep_hints
    for hint in hints:
        hint_location = getRandomHintLocation(random=spoiler.settings.random)
        UpdateHint(hint_location, hint)
    UpdateSpoilerHintList(spoiler)
