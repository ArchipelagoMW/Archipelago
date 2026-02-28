# fmt: off
"""Collectible logic file for Creepy Castle."""

from randomizer.Enums.Collectibles import Collectibles
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Regions import Regions
from randomizer.LogicClasses import Collectible

LogicRegions = {
    Regions.CreepyCastleMain: [
        Collectible(Collectibles.banana, Kongs.donkey, lambda _: True, None, 5),  # Bridge at the start
        Collectible(Collectibles.banana, Kongs.donkey, lambda _: True, None, 45),  # Entire path to W2
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: l.jetpack, None, 1),  # On pole near Cranky's Lab
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: l.jetpack, None, 1),  # On cloud at the top
        Collectible(Collectibles.balloon, Kongs.diddy, lambda l: l.peanut, None, 1),  # Above W1
        Collectible(Collectibles.banana, Kongs.tiny, lambda _: True, None, 45),  # Path from W2 to W5
        Collectible(Collectibles.bunch, Kongs.tiny, lambda _: True, None, 1),  # W5

        # Collectible(Collectibles.coin, Kongs.any, lambda l: l.shockwave, None, 1),  # Behind Snide's
        Collectible(Collectibles.coin, Kongs.donkey, lambda _: True, None, 3),  # W2
        Collectible(Collectibles.coin, Kongs.diddy, lambda l: l.jetpack, None, 4),  # Above main warps
        Collectible(Collectibles.coin, Kongs.diddy, lambda l: l.jetpack, None, 2),  # Above windows
        Collectible(Collectibles.coin, Kongs.tiny, lambda l: l.climbing, None, 2),  # Atop tree near big tree
        Collectible(Collectibles.coin, Kongs.chunky, lambda _: True, None, 3),  # Off the edge by big tree
    ],
    Regions.CastleVeryBottom: [
        Collectible(Collectibles.coin, Kongs.donkey, lambda _: True, None, 3),  # By Tiny BP
        Collectible(Collectibles.coin, Kongs.lanky, lambda l: l.climbing, None, 2),  # Atop tree near lower T&S
        Collectible(Collectibles.coin, Kongs.chunky, lambda _: True, None, 3),  # Behind gravestone near lower cave
        Collectible(Collectibles.coin, Kongs.tiny, lambda _: True, None, 3),  # Behind gravestone by lower cave
    ],
    Regions.CastleBaboonBlast: [
        Collectible(Collectibles.coin, Kongs.donkey, lambda _: True, None, 5),
    ],
    Regions.CastleTree: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: l.coconut, None, 1),  # On plank in water
        Collectible(Collectibles.balloon, Kongs.donkey, lambda l: l.coconut, None, 1),  # By BP
        Collectible(Collectibles.bunch, Kongs.chunky, lambda _: True, None, 1),  # By punchable wall
    ],
    Regions.CastleTreePastPunch: [
        Collectible(Collectibles.balloon, Kongs.chunky, lambda l: l.pineapple, None, 1),  # In Chunky's room

        Collectible(Collectibles.coin, Kongs.chunky, lambda _: True, None, 3),  # In Chunky's room
    ],
    Regions.Library: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda _: True, None, 1),  # In switch room
    ],
    Regions.LibraryPastSlam: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: l.strongKong, None, 2),  # In haunted books corridor
    ],
    Regions.LibraryPastBooks: [],
    Regions.Ballroom: [
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: l.jetpack, None, 3),  # On candles
        Collectible(Collectibles.balloon, Kongs.diddy, lambda l: l.peanut, None, 1),  # By bonus barrel
        Collectible(Collectibles.bunch, Kongs.tiny, lambda _: True, None, 1),  # On Monkeyport pad

        Collectible(Collectibles.coin, Kongs.tiny, lambda _: True, None, 3),  # Around Monkeyport pad
    ],
    Regions.MuseumBehindGlass: [
        Collectible(Collectibles.bunch, Kongs.tiny, lambda _: True, None, 2),  # In car race room
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: l.monkeyport or l.CanPhase(), None, 1),  # In weird room
        Collectible(Collectibles.balloon, Kongs.tiny, lambda l: l.feather and (l.monkeyport or l.CanPhase()), None, 1),  # In weird room
    ],
    Regions.CastleTinyRace: [
        Collectible(Collectibles.racecoin, Kongs.any, lambda _: True, None, 17),  # Race Coins
    ],
    Regions.Tower: [
        Collectible(Collectibles.balloon, Kongs.lanky, lambda l: l.grape, None, 1),

    ],
    Regions.Greenhouse: [
        Collectible(Collectibles.bunch, Kongs.lanky, lambda _: True, None, 6),

        Collectible(Collectibles.coin, Kongs.lanky, lambda _: True, None, 3),
    ],
    Regions.TrashCan: [
        Collectible(Collectibles.bunch, Kongs.tiny, lambda _: True, None, 1),

        Collectible(Collectibles.coin, Kongs.tiny, lambda _: True, None, 2),
    ],
    Regions.Shed: [
        Collectible(Collectibles.balloon, Kongs.chunky, lambda l: l.pineapple, None, 1),

        Collectible(Collectibles.coin, Kongs.chunky, lambda _: True, None, 4),
    ],
    Regions.Museum: [
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: l.punch and l.barrels, None, 1),  # Inside boulder (Chunky)
        Collectible(Collectibles.balloon, Kongs.chunky, lambda l: l.pineapple, None, 1),

        Collectible(Collectibles.coin, Kongs.chunky, lambda _: True, None, 3),
    ],
    Regions.LowerCave: [
        Collectible(Collectibles.balloon, Kongs.diddy, lambda l: l.peanut, None, 1),  # By crypt
        Collectible(Collectibles.banana, Kongs.lanky, lambda _: True, None, 5),  # Path to Funky
        Collectible(Collectibles.bunch, Kongs.lanky, lambda _: True, None, 5),  # Path to Funky
        Collectible(Collectibles.balloon, Kongs.tiny, lambda l: l.feather, None, 1),  # By Funky's

        Collectible(Collectibles.coin, Kongs.diddy, lambda _: True, None, 3),  # In front of crypt
        Collectible(Collectibles.coin, Kongs.lanky, lambda _: True, None, 4),  # Around mausoleum
    ],
    Regions.Crypt: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda _: True, None, 1),  # On W2
        Collectible(Collectibles.bunch, Kongs.diddy, lambda _: True, None, 1),  # On W1
    ],
    Regions.CryptDonkeyRoom: [
        Collectible(Collectibles.balloon, Kongs.donkey, lambda l: l.coconut, None, 1),  # In minecart room
    ],
    Regions.CastleMinecarts: [
        Collectible(Collectibles.racecoin, Kongs.any, lambda _: True, None, 68),  # Race Coins
    ],
    Regions.CryptDiddyRoom: [
        Collectible(Collectibles.balloon, Kongs.diddy, lambda l: l.peanut and (l.charge or l.generalclips or l.CanPhase()), None, 1),  # In Diddy's room

        Collectible(Collectibles.coin, Kongs.diddy, lambda l: l.charge or l.CanPhase() or l.generalclips, None, 3),  # In Diddy's room
    ],
    Regions.CryptChunkyRoom: [
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: l.punch or l.generalclips or l.CanPhase(), None, 2),  # In tombs in Chunky's room

        Collectible(Collectibles.coin, Kongs.chunky, lambda l: l.punch or l.CanPhase() or l.generalclips, None, 3),  # In tombs in Chunky's room
    ],
    Regions.Mausoleum: [
        Collectible(Collectibles.balloon, Kongs.lanky, lambda l: l.grape and (l.sprint or l.generalclips or l.CanPhase()), None, 1),
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: l.twirl or (l.monkey_maneuvers and (not l.isKrushaAdjacent(Kongs.tiny))), None, 1),  # In Green Goo Gap

        Collectible(Collectibles.coin, Kongs.lanky, lambda l: (l.grape and l.sprint) or l.generalclips or l.CanPhase() and ((l.trombone and l.can_use_vines) or l.monkey_maneuvers), None, 3),
        Collectible(Collectibles.coin, Kongs.tiny, lambda l: l.twirl or (l.monkey_maneuvers and (not l.isKrushaAdjacent(Kongs.tiny))) or l.CanPhase(), None, 2),
    ],
    Regions.UpperCave: [
        Collectible(Collectibles.banana, Kongs.chunky, lambda _: True, None, 30),

        Collectible(Collectibles.coin, Kongs.diddy, lambda _: True, None, 3),  # In front of dungeon door
        Collectible(Collectibles.coin, Kongs.tiny, lambda l: l.twirl, None, 3),  # Over pit to bonus barrel
        Collectible(Collectibles.coin, Kongs.chunky, lambda _: True, None, 3),  # By Candy's
    ],
    Regions.Dungeon: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: l.CanSlamSwitch(Levels.CreepyCastle, 3) or l.CanPhase(), None, 1),  # On face puzzle
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: l.punch or l.CanPhase(), None, 2),  # In cells by DK's door
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: l.punch or l.CanPhase(), None, 2),  # In cells by Lanky's door
        Collectible(Collectibles.balloon, Kongs.diddy, lambda l: (l.CanSlamSwitch(Levels.CreepyCastle, 3) or l.CanPhase()) and l.peanut, None, 1),  # In Diddy's room
        Collectible(Collectibles.balloon, Kongs.lanky, lambda l: l.grape and (l.CanSlamSwitch(Levels.CreepyCastle, 3) or l.CanPhase()), None, 1),  # Lanky's room (close)
        Collectible(Collectibles.balloon, Kongs.lanky, lambda l: l.grape and (l.CanSlamSwitch(Levels.CreepyCastle, 3) or l.CanPhase()) and l.trombone and l.balloon, None, 1),  # Lanky's room (far)
        Collectible(Collectibles.balloon, Kongs.chunky, lambda l: (l.punch or l.CanPhase() or l.generalclips) and l.pineapple, None, 2),  # In cells by Diddy's door

        Collectible(Collectibles.coin, Kongs.donkey, lambda _: True, None, 4),  # Around DK switch
        Collectible(Collectibles.coin, Kongs.lanky, lambda l: (l.CanSlamSwitch(Levels.CreepyCastle, 3) or l.CanPhase()) and l.trombone and l.balloon, None, 3),  # In Lanky's room
        Collectible(Collectibles.coin, Kongs.chunky, lambda l: l.punch or l.CanPhase(), None, 3),  # In a cell by Diddy's room
    ],
}
