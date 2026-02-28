# fmt: off
"""Collectible logic file for Fungi Forest."""

from randomizer.Enums.Collectibles import Collectibles
from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Switches import Switches
from randomizer.Enums.Settings import FasterChecksSelected, RemovedBarriersSelected
from randomizer.Enums.Time import Time
from randomizer.LogicClasses import Collectible

LogicRegions = {
    Regions.FungiForestStart: [
        Collectible(Collectibles.banana, Kongs.donkey, lambda _: True, None, 5),  # To Giant Mushroom Area
        Collectible(Collectibles.banana, Kongs.donkey, lambda _: True, None, 5),  # To Mill Area
        Collectible(Collectibles.bunch, Kongs.diddy, lambda _: True, None, 2),  # Bounce
        Collectible(Collectibles.bunch, Kongs.diddy, lambda _: True, None, 1),  # Warp 4
        Collectible(Collectibles.bunch, Kongs.lanky, lambda _: True, None, 1),  # Warp 1
        Collectible(Collectibles.bunch, Kongs.tiny, lambda _: True, None, 1),  # Warp 3
        Collectible(Collectibles.banana, Kongs.tiny, lambda l: l.checkBarrier(RemovedBarriersSelected.forest_green_tunnel) or l.hasMoveSwitchsanity(Switches.FungiGreenFeather, False) or l.CanPhase() or l.CanPhaseswim(), None, 4),  # Behind feather gate only
        Collectible(Collectibles.bunch, Kongs.chunky, lambda _: True, None, 1),  # Warp 2
        Collectible(Collectibles.bunch, Kongs.chunky, lambda _: True, None, 1),  # Minecart Entry
        Collectible(Collectibles.coin, Kongs.donkey, lambda _: True, None, 3),  # Behind clock
        Collectible(Collectibles.coin, Kongs.lanky, lambda l: l.can_use_vines and l.climbing, None, 3),  # On roof of Chunky Minecart entrance
        Collectible(Collectibles.coin, Kongs.tiny, lambda l: l.twirl or l.monkey_maneuvers, None, 3),  # On pink tunnel entrance
        Collectible(Collectibles.coin, Kongs.chunky, lambda _: True, None, 3),  # Near Chunky Minecart entrance
    ],
    Regions.ForestMinecarts: [
        Collectible(Collectibles.racecoin, Kongs.any, lambda _: True, None, 83),  # Race Coins (87 is possible using ISG, but just doing glitchless here. Doesn't matter either way)
    ],
    Regions.GiantMushroomArea: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda _: True, None, 1),  # Lower Warp 5
        Collectible(Collectibles.bunch, Kongs.diddy, lambda _: True, None, 2),  # Rocketbarrel
        Collectible(Collectibles.bunch, Kongs.lanky, lambda _: True, None, 1),  # Warp 3
        Collectible(Collectibles.banana, Kongs.lanky, lambda _: True, None, 10),

        Collectible(Collectibles.coin, Kongs.lanky, lambda _: True, None, 3),  # Under tag barrel behind giant mushroom
    ],
    Regions.MushroomLower: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: Events.MushroomCannonsSpawned in l.Events, None, 3),  # Cannon shots pathway
        Collectible(Collectibles.balloon, Kongs.lanky, lambda l: l.grape, None, 1),
        Collectible(Collectibles.bunch, Kongs.tiny, lambda _: True, None, 1),
    ],
    Regions.MushroomLowerBetweenLadders: [
        Collectible(Collectibles.banana, Kongs.chunky, lambda _: True, None, 3),  # 1st Ladder
        Collectible(Collectibles.bunch, Kongs.chunky, lambda _: True, None, 1),  # After 1st Ladder
    ],
    Regions.MushroomLowerMid: [
        Collectible(Collectibles.banana, Kongs.chunky, lambda _: True, None, 3),  # 2nd Ladder
        Collectible(Collectibles.bunch, Kongs.chunky, lambda _: True, None, 1),  # After 2nd Ladder
    ],
    Regions.MushroomBlastLevelExterior: [
        Collectible(Collectibles.banana, Kongs.donkey, lambda _: True, None, 2),  # On the ladder up to this level
        Collectible(Collectibles.coin, Kongs.donkey, lambda _: True, None, 3),  # Around BBlast pad
    ],
    Regions.MushroomLowerExterior: [
        Collectible(Collectibles.banana, Kongs.donkey, lambda _: True, None, 13),
        Collectible(Collectibles.balloon, Kongs.tiny, lambda l: l.feather, None, 1),

        Collectible(Collectibles.coin, Kongs.tiny, lambda _: True, None, 5),  # Around Tiny BP
    ],
    Regions.ForestBaboonBlast: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda _: True, None, 2),
    ],
    Regions.MushroomMiddle: [
        Collectible(Collectibles.banana, Kongs.diddy, lambda _: True, None, 7),
    ],
    Regions.MushroomUpperMid: [
        Collectible(Collectibles.banana, Kongs.chunky, lambda _: True, None, 3),  # 3rd Ladder
        Collectible(Collectibles.bunch, Kongs.chunky, lambda _: True, None, 1),  # After 3rd Ladder
        Collectible(Collectibles.banana, Kongs.chunky, lambda _: True, None, 3),  # 4th Ladder
    ],
    Regions.MushroomUpperVineFloor: [
        Collectible(Collectibles.banana, Kongs.chunky, lambda _: True, None, 3),  # 5th Ladder, Leading to the Klump's vine floor
    ],
    Regions.MushroomUpperVineFloor: [
        Collectible(Collectibles.banana, Kongs.chunky, lambda _: True, None, 3),  # 5th Ladder, Leading to the Klump's vine floor
    ],
    Regions.MushroomUpper: [
        Collectible(Collectibles.balloon, Kongs.lanky, lambda l: l.grape, None, 1),  # Top
        Collectible(Collectibles.banana, Kongs.chunky, lambda _: True, None, 3),  # 6th Ladder
        Collectible(Collectibles.banana, Kongs.chunky, lambda _: True, None, 3),  # 7th Ladder
        Collectible(Collectibles.bunch, Kongs.chunky, lambda _: True, None, 1),  # Top
    ],
    Regions.MushroomNightDoor: [
        Collectible(Collectibles.bunch, Kongs.chunky, lambda _: True, None, 1),
    ],
    Regions.MushroomNightExterior: [
        Collectible(Collectibles.balloon, Kongs.chunky, lambda l: l.pineapple, None, 1),
    ],
    Regions.MushroomUpperExterior: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda _: True, None, 1),  # Upper Warp 5
        Collectible(Collectibles.banana, Kongs.diddy, lambda _: True, None, 10),

        Collectible(Collectibles.coin, Kongs.diddy, lambda _: True, None, 3),  # Around crown pad
        Collectible(Collectibles.coin, Kongs.chunky, lambda _: True, None, 3),  # On switch to face puzzle room
    ],
    Regions.MushroomVeryTopExterior: [
        Collectible(Collectibles.bunch, Kongs.lanky, lambda _: True, None, 1),  # Top of mushroom
    ],
    Regions.MushroomChunkyRoom: [
        Collectible(Collectibles.bunch, Kongs.chunky, lambda _: True, None, 1),
        Collectible(Collectibles.balloon, Kongs.chunky, lambda l: l.pineapple, None, 1),
    ],
    Regions.MushroomLankyZingersRoom: [
        Collectible(Collectibles.bunch, Kongs.lanky, lambda _: True, None, 2),
    ],
    Regions.MushroomLankyMushroomsRoom: [
        Collectible(Collectibles.bunch, Kongs.lanky, lambda _: True, None, 1),
    ],
    Regions.HollowTreeArea: [
        Collectible(Collectibles.banana, Kongs.diddy, lambda _: True, None, 10),  # Around Tree
        Collectible(Collectibles.bunch, Kongs.diddy, lambda _: True, None, 1),  # Warp 4
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: l.jetpack, None, 1),  # Top of Tree
        Collectible(Collectibles.banana, Kongs.lanky, lambda _: True, None, 10),  # Tunnel
        Collectible(Collectibles.banana, Kongs.lanky, lambda _: True, None, 3),  # To Rabbit
        Collectible(Collectibles.bunch, Kongs.lanky, lambda _: True, None, 1),  # To Rabbit
        Collectible(Collectibles.banana, Kongs.tiny, lambda _: True, None, 8),
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: l.saxophone and l.mini, None, 1),

        Collectible(Collectibles.coin, Kongs.diddy, lambda l: l.jetpack and l.TimeAccess(Regions.HollowTreeArea, Time.Night), None, 4),  # Alcove in tree
        Collectible(Collectibles.coin, Kongs.lanky, lambda _: True, None, 3),  # Near Lanky BP
        Collectible(Collectibles.coin, Kongs.lanky, lambda l: (not l.checkFastCheck(FasterChecksSelected.forest_rabbit_race) or l.sprint) and l.TimeAccess(Regions.HollowTreeArea, Time.Day) and l.trombone, None, 3, True, True, "vanilla", True),  # Beat first rabbit race
    ],
    Regions.Anthill: [
    ],
    Regions.ForestMillTopOfNightCage: [
    ],
    Regions.ForestVeryTopOfMill: [
        Collectible(Collectibles.banana, Kongs.lanky, lambda _: True, None, 2),  # Mill roof
    ],
    Regions.ForestTopOfMill: [
        Collectible(Collectibles.banana, Kongs.lanky, lambda _: True, None, 4),  # Mill roof
        Collectible(Collectibles.bunch, Kongs.lanky, lambda _: True, None, 1),  # Above Balloon pad
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: l.TimeAccess(Regions.MillArea, Time.Night), None, 1),  # Attic Entrance
    ],
    Regions.MillArea: [
        Collectible(Collectibles.banana, Kongs.lanky, lambda _: True, None, 1),  # Mill roof
        Collectible(Collectibles.balloon, Kongs.donkey, lambda l: l.coconut, None, 1),  # Behind Barn
        Collectible(Collectibles.balloon, Kongs.diddy, lambda l: l.peanut and (l.TimeAccess(Regions.MillArea, Time.Day) or l.monkey_maneuvers), None, 1),  # Snide
        Collectible(Collectibles.banana, Kongs.diddy, lambda _: True, None, 3),  # Near Rafter Barn
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: l.spring or l.CanMoontail(), None, 1),  # Near Rafter Barn
        Collectible(Collectibles.banana, Kongs.tiny, lambda l: l.swim, None, 17),  # Underwater

        # Collectible(Collectibles.coin, Kongs.any, lambda l: l.shockwave, None, 1),  # In patch of grass
        Collectible(Collectibles.coin, Kongs.diddy, lambda l: l.climbing, None, 3),  # On mushroom near back Tag Barrel
        Collectible(Collectibles.coin, Kongs.lanky, lambda l: l.climbing, None, 3),  # On mushroom near rafters attic
        Collectible(Collectibles.coin, Kongs.chunky, lambda l: l.climbing, None, 3),  # On mushroom near Chunky minecart exit
    ],
    Regions.MillChunkyTinyArea: [
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: l.punch, None, 1),
        Collectible(Collectibles.bunch, Kongs.tiny, lambda _: True, None, 2),  # Near Spider
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: Events.MillBoxBroken in l.Events, None, 1),  # Inside Box

        Collectible(Collectibles.coin, Kongs.chunky, lambda _: True, None, 3),
    ],
    Regions.SpiderRoom: [
        Collectible(Collectibles.bunch, Kongs.tiny, lambda _: True, None, 1),
    ],
    Regions.GrinderRoom: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: l.Slam, None, 1),  # In slam box
        Collectible(Collectibles.balloon, Kongs.donkey, lambda l: (l.CanSlamSwitch(Levels.FungiForest, 2) or l.generalclips or l.CanPhase()) and l.coconut, None, 1),  # Behind gate

        Collectible(Collectibles.coin, Kongs.lanky, lambda _: True, None, 3),
        Collectible(Collectibles.coin, Kongs.tiny, lambda _: True, None, 3),
    ],
    Regions.MillRafters: [
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: l.guitar and l.isdiddy, None, 2),
    ],
    Regions.WinchRoom: [
        Collectible(Collectibles.balloon, Kongs.diddy, lambda l: l.peanut, None, 1),

        Collectible(Collectibles.coin, Kongs.diddy, lambda _: True, None, 2),
    ],
    Regions.MillAttic: [
        Collectible(Collectibles.bunch, Kongs.lanky, lambda _: True, None, 1),

        Collectible(Collectibles.coin, Kongs.diddy, lambda _: True, None, 3),
    ],
    Regions.ThornvineArea: [
        Collectible(Collectibles.banana, Kongs.donkey, lambda _: True, None, 5),
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: l.strongKong, None, 1),  # Behind on switch
        Collectible(Collectibles.balloon, Kongs.tiny, lambda l: l.feather, None, 1),

        Collectible(Collectibles.coin, Kongs.donkey, lambda l: l.strongKong, None, 3),  # On thorn vines
    ],
    Regions.ThornvineBarn: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: l.Slam and l.isdonkey, None, 1),  # In slam box
        Collectible(Collectibles.coin, Kongs.donkey, lambda _: True, None, 3),  # In trough
    ],
    Regions.WormArea: [
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: l.climbing, None, 3),  # On top of Mushrooms around The Apple
        Collectible(Collectibles.banana, Kongs.tiny, lambda _: True, None, 1),  # Last one behind Pineapple gate
        Collectible(Collectibles.bunch, Kongs.chunky, lambda _: True, None, 1),  # Warp 2
        Collectible(Collectibles.banana, Kongs.chunky, lambda _: True, None, 9),

        # Collectible(Collectibles.coin, Kongs.any, lambda l: l.shockwave, None, 1),  # In front of beanstalk
        Collectible(Collectibles.coin, Kongs.tiny, lambda _: True, None, 3),  # By Mini Monkey barrel
        Collectible(Collectibles.coin, Kongs.chunky, lambda l: l.TimeAccess(Regions.WormArea, Time.Night) or l.CanPhase(), None, 3),  # By T&S portal
    ],
}
