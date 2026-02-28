# fmt: off
"""Collectible logic file for Crystal Caves."""

from randomizer.Enums.Collectibles import Collectibles
from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Regions import Regions
from randomizer.LogicClasses import Collectible

LogicRegions = {
    Regions.CrystalCavesMain: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda _: True, None, 1),  # Warp 1
        Collectible(Collectibles.banana, Kongs.donkey, lambda _: True, None, 5),  # Near BBlast

        Collectible(Collectibles.banana, Kongs.diddy, lambda _: True, None, 5),  # Near Funky
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: l.jetpack, None, 1),  # Near Bonus
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: l.jetpack or l.monkey_maneuvers, None, 1),  # Warp 4 pillar
        Collectible(Collectibles.balloon, Kongs.diddy, lambda l: l.peanut, None, 1),  # Near Warp 4 pillar

        Collectible(Collectibles.banana, Kongs.lanky, lambda _: True, None, 5),  # Level Start
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: (l.balloon or l.monkey_maneuvers) and l.CanSlamSwitch(Levels.CrystalCaves, 2), None, 1),  # Beetle Race entry
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: l.balloon, None, 3),  # Near Cranky

        Collectible(Collectibles.banana, Kongs.tiny, lambda _: True, None, 10),  # River To Igloo
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: l.mini or l.CanPhase(), None, 1),  # Warp 3 cave

        Collectible(Collectibles.bunch, Kongs.chunky, lambda _: True, None, 1),  # Warp 2
        Collectible(Collectibles.bunch, Kongs.chunky, lambda _: True, None, 1),  # On small boulder switch
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: l.barrels, None, 1),  # Underneath small boulder
        Collectible(Collectibles.banana, Kongs.chunky, lambda _: True, None, 3),  # On bridge to small boulder switch

        Collectible(Collectibles.coin, Kongs.diddy, lambda _: True, None, 4),  # On ice castle
        Collectible(Collectibles.coin, Kongs.lanky, lambda _: True, None, 3),  # In water below Funky
        Collectible(Collectibles.coin, Kongs.tiny, lambda l: l.twirl, None, 2),  # Pillar above warps
        Collectible(Collectibles.coin, Kongs.tiny, lambda _: True, None, 3),  # In front of tunnel to W4 cave
        Collectible(Collectibles.coin, Kongs.chunky, lambda _: True, None, 3),  # On slippery slope to Cranky
    ],
    Regions.CavesGGRoom: [
        Collectible(Collectibles.balloon, Kongs.donkey, lambda l: l.coconut, None, 1),  # GG room balloon
        Collectible(Collectibles.bunch, Kongs.chunky, lambda _: True, None, 1),  # Gorilla Gone room
        Collectible(Collectibles.banana, Kongs.chunky, lambda _: True, None, 3),  # GG room singles

        Collectible(Collectibles.coin, Kongs.donkey, lambda _: True, None, 3),  # GG room coins
    ],
    Regions.CavesSnideArea: [
        Collectible(Collectibles.banana, Kongs.chunky, lambda _: True, None, 3),  # Near Snide
        Collectible(Collectibles.balloon, Kongs.chunky, lambda l: l.pineapple, None, 1),  # Near Snide

        Collectible(Collectibles.coin, Kongs.chunky, lambda _: True, None, 3),  # Snide's room
    ],
    Regions.CavesBlueprintCave: [
        Collectible(Collectibles.bunch, Kongs.diddy, lambda _: True, None, 1),  # Warp 4 cave
        Collectible(Collectibles.banana, Kongs.diddy, lambda _: True, None, 5),  # Warp 4 cave

        Collectible(Collectibles.balloon, Kongs.tiny, lambda l: l.feather, None, 1),  # Warp 4 cave
    ],
    Regions.CavesBonusCave: [
        Collectible(Collectibles.balloon, Kongs.chunky, lambda l: l.pineapple, None, 1),  # Warp 3 cave

        Collectible(Collectibles.coin, Kongs.chunky, lambda _: True, None, 5),  # Warp 3 cave
    ],
    Regions.CavesBlueprintPillar: [
        Collectible(Collectibles.bunch, Kongs.lanky, lambda _: True, None, 4),  # Warp 5 platform
    ],
    Regions.CavesBananaportSpire: [
    ],
    Regions.CavesBaboonBlast: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda _: True, None, 4),

        Collectible(Collectibles.coin, Kongs.donkey, lambda _: True, None, 3),
    ],
    Regions.BoulderCave: [
        Collectible(Collectibles.banana, Kongs.donkey, lambda _: True, None, 3),
        Collectible(Collectibles.balloon, Kongs.donkey, lambda l: l.coconut, None, 1),

        Collectible(Collectibles.banana, Kongs.chunky, lambda l: Events.CavesSmallBoulderButton in l.Events or l.CanPhase(), None, 6),
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: Events.CavesSmallBoulderButton in l.Events and l.hunkyChunky and l.barrels, None, 1),

        Collectible(Collectibles.coin, Kongs.donkey, lambda _: True, None, 3),
    ],
    Regions.CavesLankyRace: [
        Collectible(Collectibles.racecoin, Kongs.any, lambda _: True, None, 74),  # Race Coins
    ],
    Regions.FrozenCastle: [
        Collectible(Collectibles.balloon, Kongs.lanky, lambda l: l.grape, None, 1),

        Collectible(Collectibles.coin, Kongs.lanky, lambda _: True, None, 2),
    ],
    Regions.IglooArea: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda _: True, None, 1),  # Warp 1
        Collectible(Collectibles.banana, Kongs.donkey, lambda _: True, None, 5),  # Around Igloo

        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: l.jetpack, None, 4),  # Above igloos

        Collectible(Collectibles.bunch, Kongs.tiny, lambda _: True, None, 1),  # Warp 3
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: Events.CavesMonkeyportAccess in l.Events or l.CanPhaseswim(), None, 1),  # Monkeyport Ice Shield

        Collectible(Collectibles.banana, Kongs.chunky, lambda l: Events.CavesLargeBoulderButton in l.Events or l.generalclips or l.CanPhaseswim(), None, 5),  # Ice Shield

        Collectible(Collectibles.coin, Kongs.lanky, lambda _: True, None, 3),  # In water by pillar
        Collectible(Collectibles.coin, Kongs.tiny, lambda _: True, None, 3),  # In water behind W1
        Collectible(Collectibles.coin, Kongs.chunky, lambda _: True, None, 3),  # In water behind tag barrel
    ],
    Regions.GiantKosha: [
        Collectible(Collectibles.bunch, Kongs.tiny, lambda _: True, None, 4),

        # Collectible(Collectibles.coin, Kongs.any, lambda l: l.shockwave, None, 1),
        Collectible(Collectibles.coin, Kongs.tiny, lambda _: True, None, 3),
    ],
    Regions.DonkeyIgloo: [
        Collectible(Collectibles.banana, Kongs.donkey, lambda l: (l.strongKong or l.CanMoonkick()) and l.isdonkey, None, 7),
        Collectible(Collectibles.bunch, Kongs.donkey, lambda _: True, None, 1),
        Collectible(Collectibles.balloon, Kongs.donkey, lambda l: l.coconut, None, 1),
    ],
    Regions.DiddyIgloo: [
        Collectible(Collectibles.balloon, Kongs.diddy, lambda l: l.peanut, None, 1),
    ],
    Regions.LankyIgloo: [
        Collectible(Collectibles.banana, Kongs.lanky, lambda _: True, None, 1),  # First single
        Collectible(Collectibles.banana, Kongs.lanky, lambda l: l.balloon or l.monkey_maneuvers, None, 4),  # Upper singles
        Collectible(Collectibles.balloon, Kongs.lanky, lambda l: l.grape, None, 1),
    ],
    Regions.TinyIgloo: [
        Collectible(Collectibles.bunch, Kongs.tiny, lambda _: True, None, 1),
        Collectible(Collectibles.balloon, Kongs.tiny, lambda l: l.feather, None, 1),
    ],
    Regions.ChunkyIgloo: [
        Collectible(Collectibles.balloon, Kongs.chunky, lambda l: l.pineapple, None, 1),
    ],
    Regions.CabinArea: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda _: True, None, 1),
        Collectible(Collectibles.balloon, Kongs.diddy, lambda l: l.peanut, None, 1),
        Collectible(Collectibles.banana, Kongs.lanky, lambda _: True, None, 10),  # River
        Collectible(Collectibles.balloon, Kongs.lanky, lambda l: l.grape, None, 1),
        Collectible(Collectibles.balloon, Kongs.tiny, lambda l: l.feather, None, 1),
        Collectible(Collectibles.bunch, Kongs.chunky, lambda _: True, None, 1),  # Warp 2

        Collectible(Collectibles.coin, Kongs.lanky, lambda _: True, None, 3),  # Waterfall area, on ledge below Lanky Cabin
        Collectible(Collectibles.coin, Kongs.chunky, lambda _: True, None, 3),  # In corner near rocketbarrel
    ],
    Regions.CavesSprintCabinRoof: [
        Collectible(Collectibles.bunch, Kongs.lanky, lambda _: True, None, 1),  # Top of Lanky cabin
    ],
    Regions.RotatingCabin: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda _: True, None, 1),
    ],
    Regions.DonkeyCabin: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda _: True, None, 1),

        Collectible(Collectibles.coin, Kongs.donkey, lambda _: True, None, 2),
    ],
    Regions.DiddyLowerCabin: [
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: l.jetpack or l.monkey_maneuvers, None, 1),
        Collectible(Collectibles.banana, Kongs.diddy, lambda _: True, None, 5),

        Collectible(Collectibles.coin, Kongs.diddy, lambda l: l.jetpack or l.monkey_maneuvers, None, 4),
    ],
    Regions.DiddyUpperCabin: [
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: l.jetpack and (l.guitar or l.oranges) and (l.spring or l.CanMoontail()), None, 3),
    ],
    Regions.LankyCabin: [
        Collectible(Collectibles.bunch, Kongs.lanky, lambda _: True, None, 1),
    ],
    Regions.TinyCabin: [
        Collectible(Collectibles.bunch, Kongs.tiny, lambda _: True, None, 2),
        Collectible(Collectibles.balloon, Kongs.tiny, lambda l: l.feather, None, 1),
    ],
    Regions.ChunkyCabin: [
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: l.gorillaGone and l.Slam, None, 4),
    ],
}
