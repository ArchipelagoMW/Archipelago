# fmt: off
"""Collectible logic file for Gloomy Galleon."""

from randomizer.Enums.Collectibles import Collectibles
from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Regions import Regions
from randomizer.LogicClasses import Collectible

LogicRegions = {
    Regions.GloomyGalleonStart: [
        Collectible(Collectibles.balloon, Kongs.donkey, lambda l: l.coconut, None, 1),
        Collectible(Collectibles.bunch, Kongs.diddy, lambda _: True, None, 2),
        Collectible(Collectibles.banana, Kongs.lanky, lambda _: True, None, 5),
        Collectible(Collectibles.balloon, Kongs.lanky, lambda l: l.grape and ((l.punch and l.chunky) or l.CanPhase()), None, 2),
        Collectible(Collectibles.banana, Kongs.tiny, lambda _: True, None, 5),  # tunnel side 1
        Collectible(Collectibles.banana, Kongs.tiny, lambda _: True, None, 4),  # tunnel side 2
        Collectible(Collectibles.banana, Kongs.chunky, lambda _: True, None, 2),  # Near Warp 1
        Collectible(Collectibles.bunch, Kongs.chunky, lambda _: True, None, 1),  # On Warp 2
        Collectible(Collectibles.banana, Kongs.chunky, lambda _: True, None, 5),  # Chests

        Collectible(Collectibles.coin, Kongs.diddy, lambda _: True, None, 5),  # Cranky's lab
        Collectible(Collectibles.coin, Kongs.chunky, lambda _: True, None, 3),  # Towards chests
    ],
    Regions.GalleonPastVines: [
        Collectible(Collectibles.banana, Kongs.tiny, lambda _: True, None, 3),  # Near Warp 3
        Collectible(Collectibles.bunch, Kongs.tiny, lambda _: True, None, 1),  # On Warp 3
        Collectible(Collectibles.banana, Kongs.chunky, lambda _: True, None, 3),  # Near Warp 3
    ],
    Regions.GalleonBeyondPineappleGate: [
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: (Events.WaterRaised in l.Events), None, 3),
        Collectible(Collectibles.balloon, Kongs.chunky, lambda l: l.pineapple and (Events.WaterRaised in l.Events or (l.monkey_maneuvers and l.ischunky)), None, 1),

        Collectible(Collectibles.coin, Kongs.tiny, lambda _: True, None, 3),
        Collectible(Collectibles.coin, Kongs.chunky, lambda _: True, None, 3),
    ],
    Regions.LighthouseSurface: [
        Collectible(Collectibles.balloon, Kongs.tiny, lambda l: l.feather and Events.WaterLowered in l.Events, None, 1),  # Near Diddy BP
    ],
    Regions.LighthousePlatform: [
        Collectible(Collectibles.balloon, Kongs.donkey, lambda l: l.coconut, None, 1),
        Collectible(Collectibles.balloon, Kongs.diddy, lambda l: l.peanut, None, 1),  # Seal Cage
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: l.jetpack, None, 2),  # Top lighthouse

        Collectible(Collectibles.coin, Kongs.diddy, lambda l: l.jetpack, None, 3),  # On seal cage
        Collectible(Collectibles.coin, Kongs.chunky, lambda l: (Events.WaterRaised in l.Events or (l.monkey_maneuvers and (l.ischunky or l.islanky))), None, 3),  # Around W1
    ],
    Regions.LighthouseUnderwater: [
        Collectible(Collectibles.banana, Kongs.lanky, lambda _: True, None, 5),  # Near Enguarde
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: (Events.LighthouseEnguarde in l.Events or l.CanPhaseswim()), None, 4),  # Enguarde chests
        Collectible(Collectibles.banana, Kongs.chunky, lambda _: True, None, 10),  # Underwater

        Collectible(Collectibles.coin, Kongs.lanky, lambda _: True, None, 3),  # Under enguarde box
        Collectible(Collectibles.coin, Kongs.tiny, lambda _: True, None, 5),  # In front of Mermaid room
        Collectible(Collectibles.coin, Kongs.chunky, lambda _: True, None, 5),  # Under tag barrel by Mermaid room
        Collectible(Collectibles.coin, Kongs.chunky, lambda _: True, None, 3),  # By T&S in the deep hole
    ],
    Regions.LighthouseEnguardeDoor: [
        Collectible(Collectibles.banana, Kongs.donkey, lambda _: True, None, 10),  # Behind Enguarde wall

        Collectible(Collectibles.coin, Kongs.lanky, lambda _: True, None, 3),  # Behind Enguarde wall
    ],
    Regions.LighthouseSnideAlcove: [
        Collectible(Collectibles.bunch, Kongs.tiny, lambda _: True, None, 1),  # On Warp 3
        Collectible(Collectibles.balloon, Kongs.tiny, lambda l: l.feather, None, 1),  # Snide
    ],
    Regions.GalleonBaboonBlast: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda _: True, None, 3),

        Collectible(Collectibles.coin, Kongs.donkey, lambda _: True, None, 2),
    ],
    Regions.Lighthouse: [
        Collectible(Collectibles.balloon, Kongs.donkey, lambda l: l.coconut, None, 1),

        # Collectible(Collectibles.coin, Kongs.any, lambda l: l.shockwave, None, 1),
    ],
    Regions.LighthouseAboveLadder: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda _: True, None, 4),
    ],
    Regions.MermaidRoom: [
        Collectible(Collectibles.coin, Kongs.tiny, lambda _: True, None, 3),
    ],
    Regions.SickBay: [
        Collectible(Collectibles.bunch, Kongs.chunky, lambda _: True, None, 4),
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: l.punch or l.CanPhase(), None, 1),  # One bunch behind gate
        Collectible(Collectibles.coin, Kongs.chunky, lambda l: l.punch or l.CanPhase(), None, 3),
    ],
    Regions.Shipyard: [
        Collectible(Collectibles.balloon, Kongs.diddy, lambda l: l.peanut, None, 1),  # Cactus
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: l.swim or Events.WaterLowered in l.Events, None, 1),  # Cactus
        Collectible(Collectibles.balloon, Kongs.lanky, lambda l: l.grape, None, 1),  # Over the main area
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: Events.WaterRaised in l.Events, None, 1),  # Above Warp 2
        Collectible(Collectibles.balloon, Kongs.chunky, lambda l: l.pineapple, None, 1),  # Near Warp 2
        Collectible(Collectibles.balloon, Kongs.chunky, lambda l: l.pineapple, None, 1),  # Cactus

        Collectible(Collectibles.coin, Kongs.donkey, lambda l: Events.WaterRaised in l.Events or l.CanMoonkick(), None, 4),  # On floating plank near W5
        Collectible(Collectibles.coin, Kongs.chunky, lambda _: True, None, 5),  # Near Chunky BP
    ],
    Regions.ShipyardUnderwater: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda _: True, None, 3),  # Underwater in an overturned ship
        Collectible(Collectibles.banana, Kongs.diddy, lambda _: True, None, 10),  # Around 2DShip
        Collectible(Collectibles.banana, Kongs.diddy, lambda _: True, None, 6),  # To Gold Tower
        Collectible(Collectibles.bunch, Kongs.diddy, lambda _: True, None, 4),  # By mechfish grate
        Collectible(Collectibles.bunch, Kongs.lanky, lambda _: True, None, 1),  # Enguarde
        Collectible(Collectibles.bunch, Kongs.chunky, lambda _: True, None, 3),  # Underwater in an overturned ship

        Collectible(Collectibles.coin, Kongs.donkey, lambda l: Events.ShipyardEnguarde in l.Events or l.CanPhaseswim(), None, 3),  # In chest around 5DS
        Collectible(Collectibles.coin, Kongs.diddy, lambda _: True, None, 4),  # Around cactus underwater
        Collectible(Collectibles.coin, Kongs.diddy, lambda l: Events.ShipyardEnguarde in l.Events or l.CanPhaseswim(), None, 3),  # In chest near mech fish
        Collectible(Collectibles.coin, Kongs.lanky, lambda l: Events.ShipyardEnguarde in l.Events or l.CanPhaseswim(), None, 3),  # In chest around 5DS
        Collectible(Collectibles.coin, Kongs.tiny, lambda l: Events.ShipyardEnguarde in l.Events or l.CanPhaseswim(), None, 3),  # In chest around 5DS
        # Collectible(Collectibles.coin, Kongs.chunky, lambda l: Events.ShipyardEnguarde in l.Events or l.CanPhaseswim(), None, 3),  # In chest around 5DS (Out of Bounds)
    ],
    Regions.SealRace: [
        Collectible(Collectibles.racecoin, Kongs.any, lambda _: True, None, 19),  # Race Coins
    ],
    Regions.TreasureRoom: [
        Collectible(Collectibles.balloon, Kongs.diddy, lambda l: l.peanut, None, 1),
        Collectible(Collectibles.banana, Kongs.lanky, lambda l: Events.WaterRaised in l.Events, None, 1),  # First on Gold tower
        Collectible(Collectibles.banana, Kongs.lanky, lambda l: Events.WaterRaised in l.Events and l.balloon, None, 4),  # Upper gold tower
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: l.swim, None, 1),
        Collectible(Collectibles.balloon, Kongs.tiny, lambda l: l.feather, None, 1),
    ],
    Regions.TreasureRoomDiddyGoldTower: [
    ],
    Regions.TinyChest: [
        Collectible(Collectibles.coin, Kongs.tiny, lambda _: True, None, 4),
    ],
    Regions.Submarine: [
    ],
    Regions.Mechafish: [
    ],
    Regions.LankyShip: [
        Collectible(Collectibles.banana, Kongs.lanky, lambda _: True, None, 5),
        Collectible(Collectibles.bunch, Kongs.lanky, lambda _: True, None, 1),
        Collectible(Collectibles.coin, Kongs.lanky, lambda _: True, None, 3),  # In chests
        Collectible(Collectibles.coin, Kongs.lanky, lambda _: True, None, 1),  # In tunnel
    ],
    Regions.TinyShip: [
        Collectible(Collectibles.bunch, Kongs.tiny, lambda _: True, None, 2),
    ],
    Regions.BongosShip: [
        Collectible(Collectibles.banana, Kongs.donkey, lambda _: True, None, 10),

        Collectible(Collectibles.coin, Kongs.donkey, lambda _: True, None, 3),
    ],
    Regions.GuitarShip: [
        Collectible(Collectibles.banana, Kongs.diddy, lambda _: True, None, 4),
        Collectible(Collectibles.bunch, Kongs.diddy, lambda _: True, None, 2),
    ],
    Regions.TromboneShip: [
        Collectible(Collectibles.bunch, Kongs.lanky, lambda _: True, None, 3),

        Collectible(Collectibles.coin, Kongs.lanky, lambda _: True, None, 3),
    ],
    Regions.SaxophoneShip: [
        Collectible(Collectibles.banana, Kongs.tiny, lambda _: True, None, 8),
        Collectible(Collectibles.bunch, Kongs.tiny, lambda _: True, None, 2),
        Collectible(Collectibles.coin, Kongs.tiny, lambda _: True, None, 2),
    ],
    Regions.TriangleShip: [
        Collectible(Collectibles.coin, Kongs.chunky, lambda _: True, None, 3)
    ],
}
