# fmt: off
"""Collectible logic file for Frantic Factory."""

from randomizer.Enums.Collectibles import Collectibles
from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Regions import Regions
from randomizer.LogicClasses import Collectible

LogicRegions = {
    Regions.FranticFactoryStart: [
        Collectible(Collectibles.banana, Kongs.donkey, lambda _: True, None, 5),  # First tunnel
        Collectible(Collectibles.bunch, Kongs.lanky, lambda _: True, None, 1),  # W2
        Collectible(Collectibles.banana, Kongs.tiny, lambda _: True, None, 3),  # Path to Testing
        Collectible(Collectibles.bunch, Kongs.chunky, lambda _: True, None, 1),  # W1
        Collectible(Collectibles.banana, Kongs.chunky, lambda l: Events.HatchOpened in l.Events, None, 10),  # On pole down the hatch
        Collectible(Collectibles.balloon, Kongs.chunky, lambda l: l.pineapple, None, 1),  # Around hatch

        Collectible(Collectibles.coin, Kongs.chunky, lambda _: True, None, 5),  # Around hatch
    ],
    Regions.Testing: [
        Collectible(Collectibles.banana, Kongs.donkey, lambda _: True, None, 5),  # Path to Numbers game
        Collectible(Collectibles.balloon, Kongs.donkey, lambda l: l.coconut, None, 1),  # Numbers game
        Collectible(Collectibles.banana, Kongs.diddy, lambda _: True, None, 3),  # Path to Funky
        Collectible(Collectibles.bunch, Kongs.diddy, lambda _: True, None, 1),  # W5
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: l.spring or l.CanMoontail(), None, 5),  # Block Tower
        Collectible(Collectibles.banana, Kongs.tiny, lambda _: True, None, 7),  # Path to testing room
        Collectible(Collectibles.bunch, Kongs.tiny, lambda _: True, None, 1),  # Block tower side of Mini Monkey tunnel
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: l.mini or l.CanPhase(), None, 1),  # Spinning wheel
        Collectible(Collectibles.balloon, Kongs.tiny, lambda l: l.feather, None, 1),  # By Snide's HQ
        Collectible(Collectibles.balloon, Kongs.tiny, lambda l: l.feather, None, 1),  # By Funky's
        Collectible(Collectibles.bunch, Kongs.chunky, lambda _: True, None, 1),  # W3
        Collectible(Collectibles.balloon, Kongs.chunky, lambda l: l.pineapple, None, 1),  # Above Snide's room

        Collectible(Collectibles.coin, Kongs.donkey, lambda _: True, None, 3),  # Steps in block tower room
        Collectible(Collectibles.coin, Kongs.donkey, lambda _: True, None, 3),  # Number game
        Collectible(Collectibles.coin, Kongs.diddy, lambda _: True, None, 5),  # Top of pole to Snide's
        Collectible(Collectibles.coin, Kongs.diddy, lambda _: True, None, 5),  # Bottom of pole to R&D
        Collectible(Collectibles.coin, Kongs.lanky, lambda _: True, None, 4),  # Behind boxes under spinning wheel
        Collectible(Collectibles.coin, Kongs.tiny, lambda _: True, None, 5),  # Bottom of pole to Testing floor
        Collectible(Collectibles.coin, Kongs.chunky, lambda _: True, None, 3),  # W3, Snide's side
        Collectible(Collectibles.coin, Kongs.chunky, lambda _: True, None, 4),  # Block Tower room, in alcoves
    ],
    Regions.RandDUpper: [
        Collectible(Collectibles.balloon, Kongs.donkey, lambda l: l.coconut, None, 1),
        Collectible(Collectibles.balloon, Kongs.diddy, lambda l: l.peanut and (l.guitar or l.CanAccessRNDRoom()), None, 3),
        Collectible(Collectibles.banana, Kongs.lanky, lambda _: True, None, 5),  # Around R&D
        Collectible(Collectibles.banana, Kongs.chunky, lambda l: (l.punch and l.triangle and l.climbing) or l.CanAccessRNDRoom(), None, 10),  # Toy Monster room
        Collectible(Collectibles.coin, Kongs.diddy, lambda _: True, None, 5),  # Around vent to Chunky room
        Collectible(Collectibles.coin, Kongs.chunky, lambda l: (l.grab and l.donkey) or l.CanAccessRNDRoom(), None, 4),  # In hole near Diddy's room
        Collectible(Collectibles.balloon, Kongs.chunky, lambda l: ((l.punch and l.triangle and l.climbing) or l.CanAccessRNDRoom()) and l.pineapple, None, 1),  # Toy Monster room
    ],
    Regions.RandD: [
        Collectible(Collectibles.banana, Kongs.lanky, lambda _: True, None, 5),  # Around R&D
        Collectible(Collectibles.bunch, Kongs.lanky, lambda _: True, None, 1),  # W2
        Collectible(Collectibles.balloon, Kongs.lanky, lambda l: (l.trombone or l.CanAccessRNDRoom()) and l.grape, None, 1),  # Piano game
        Collectible(Collectibles.banana, Kongs.tiny, lambda _: True, None, 10),  # To car race
        Collectible(Collectibles.coin, Kongs.donkey, lambda _: True, None, 3),  # By lever
        Collectible(Collectibles.coin, Kongs.lanky, lambda _: True, None, 5),  # Top of pole to Block Tower room
    ],
    Regions.FactoryTinyRaceLobby: [

    ],
    Regions.ChunkyRoomPlatform: [

    ],
    Regions.PowerHut: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda _: True, None, 3),

        Collectible(Collectibles.coin, Kongs.donkey, lambda _: True, None, 1),
    ],
    Regions.FactoryArcadeTunnel: [
        Collectible(Collectibles.banana, Kongs.diddy, lambda _: True, None, 5),  # Path to DK Arcade
        Collectible(Collectibles.bunch, Kongs.diddy, lambda _: True, None, 1),  # W5
        Collectible(Collectibles.bunch, Kongs.tiny, lambda _: True, None, 1),  # In arcade room

        Collectible(Collectibles.coin, Kongs.chunky, lambda l: l.punch or l.CanPhase(), None, 3),  # Behind Stash Snatch barrel
    ],
    Regions.AlcoveBeyondHatch: [
        Collectible(Collectibles.bunch, Kongs.tiny, lambda _: True, None, 2),  # Halfway down the hatch
    ],
    Regions.BeyondHatch: [
        Collectible(Collectibles.banana, Kongs.donkey, lambda _: True, None, 6),  # Tunnel to production room
        Collectible(Collectibles.banana, Kongs.donkey, lambda _: True, None, 4),  # Tunnel between production room and Chunky room
        Collectible(Collectibles.balloon, Kongs.donkey, lambda l: l.coconut, None, 1),  # By shops
        Collectible(Collectibles.banana, Kongs.diddy, lambda _: True, None, 12),  # Around bottom of production room
        Collectible(Collectibles.banana, Kongs.lanky, lambda _: True, None, 5),  # Path to shops
        Collectible(Collectibles.banana, Kongs.lanky, lambda _: True, None, 1),  # Base of pipe to free Chunky switch
        Collectible(Collectibles.bunch, Kongs.chunky, lambda _: True, None, 1),  # W1
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: l.punch, None, 3),  # Dark Room

        Collectible(Collectibles.coin, Kongs.donkey, lambda _: True, None, 3),  # Bottom of pole
        Collectible(Collectibles.coin, Kongs.diddy, lambda l: l.spring or l.CanPhase() or l.CanMoontail(), None, 3),  # High ledge in Chunky's room
        Collectible(Collectibles.coin, Kongs.lanky, lambda _: True, None, 3),  # On boxes in Chunky's room
        Collectible(Collectibles.coin, Kongs.tiny, lambda _: True, None, 5),  # Around Tiny BP
        Collectible(Collectibles.coin, Kongs.chunky, lambda _: True, None, 5),  # W1
    ],
    Regions.FactoryStoragePipe: [
        Collectible(Collectibles.banana, Kongs.lanky, lambda _: True, None, 4),  # Pipe to free Chunky switch
    ],
    Regions.FactoryBaboonBlast: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda _: True, None, 4),

    ],
    Regions.InsideCore: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: l.strongKong, None, 3),
        Collectible(Collectibles.balloon, Kongs.lanky, lambda l: l.grape, None, 1),

        Collectible(Collectibles.coin, Kongs.lanky, lambda _: True, None, 3),
    ],
    Regions.LowerCore: [

    ],
    Regions.SpinningCore: [
        Collectible(Collectibles.bunch, Kongs.lanky, lambda _: True, None, 3),  # On steps on middle level
        Collectible(Collectibles.bunch, Kongs.chunky, lambda _: True, None, 4),  # on rotating arms but reachable without machine on

        Collectible(Collectibles.coin, Kongs.lanky, lambda _: True, None, 2),  # First two coins on elevators by W4
        Collectible(Collectibles.coin, Kongs.tiny, lambda _: True, None, 5),  # W4
        Collectible(Collectibles.coin, Kongs.chunky, lambda _: True, None, 4),  # On middle level
    ],
    Regions.MiddleCore: [
        Collectible(Collectibles.balloon, Kongs.tiny, lambda l: l.feather, None, 1),  # On middle level
    ],
    Regions.UpperCore: [
        Collectible(Collectibles.bunch, Kongs.diddy, lambda _: True, None, 3),  # On cylinders and Simian Spring pad
        Collectible(Collectibles.bunch, Kongs.lanky, lambda _: True, None, 1),  # On pipe to production room GB (bottom bunch)
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: l.handstand or l.CanPhase(), None, 4),  # On pipe to production room GB
        Collectible(Collectibles.balloon, Kongs.lanky, lambda l: l.grape, None, 1),  # By T&S portal
        Collectible(Collectibles.bunch, Kongs.tiny, lambda _: True, None, 4),  # On conveyors to Bonus Barrel
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: l.twirl, None, 1),  # On platform past Bonus Barrel

        Collectible(Collectibles.coin, Kongs.lanky, lambda _: True, None, 1),  # High coin on elevators by W4
        Collectible(Collectibles.coin, Kongs.tiny, lambda l: l.twirl, None, 3),  # Past Tiny Bonus Barrel
    ],
    Regions.FactoryTinyRace: [
        Collectible(Collectibles.racecoin, Kongs.any, lambda _: True, None, 25),  # Race Coins
    ]
}
