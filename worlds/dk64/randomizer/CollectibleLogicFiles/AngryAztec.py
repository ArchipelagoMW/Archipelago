# fmt: off
"""Collectible logic file for Angry Aztec."""

from randomizer.Enums.Collectibles import Collectibles
from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Settings import DamageAmount
from randomizer.Enums.Switches import Switches
from randomizer.LogicClasses import Collectible

LogicRegions = {
    Regions.AngryAztecStart: [
    ],
    Regions.BetweenVinesByPortal: [
        Collectible(Collectibles.banana, Kongs.chunky, lambda _: True, None, 5),
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: l.pineapple or l.CanPhase(), None, 4),
    ],
    Regions.AngryAztecOasis: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: (l.hasMoveSwitchsanity(Switches.AztecBlueprintDoor, False) or l.CanPhase()) and l.strongKong, None, 2),
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: l.climbing, None, 3),
        Collectible(Collectibles.banana, Kongs.donkey, lambda _: True, None, 3),
        Collectible(Collectibles.balloon, Kongs.diddy, lambda l: l.peanut, None, 1),
        Collectible(Collectibles.bunch, Kongs.diddy, lambda _: True, None, 1),
        Collectible(Collectibles.banana, Kongs.lanky, lambda _: True, None, 5),

        Collectible(Collectibles.coin, Kongs.donkey, lambda _: True, None, 2),  # Llama cage
        Collectible(Collectibles.coin, Kongs.donkey, lambda l: (l.hasMoveSwitchsanity(Switches.AztecBlueprintDoor, False) or l.CanPhase()) and l.strongKong, None, 3),  # DK BP room
        # Collectible(Collectibles.coin, Kongs.any, lambda l: l.shockwave, None, 1),  # Oasis
        Collectible(Collectibles.coin, Kongs.diddy, lambda _: True, None, 5),  # W2
        Collectible(Collectibles.coin, Kongs.tiny, lambda _: True, None, 4),  # Oasis
        Collectible(Collectibles.coin, Kongs.chunky, lambda _: True, None, 4),  # Outside Tiny Temple
    ],
    Regions.TempleStart: [
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: l.CanSlamSwitch(Levels.AngryAztec, 1) and l.peanut, None, 3),
        Collectible(Collectibles.banana, Kongs.diddy, lambda l: l.CanSlamSwitch(Levels.AngryAztec, 1), None, 3),
        Collectible(Collectibles.bunch, Kongs.chunky, lambda _: True, None, 5),
        Collectible(Collectibles.banana, Kongs.chunky, lambda _: True, None, 4),

        Collectible(Collectibles.coin, Kongs.lanky, lambda _: True, None, 3),
        Collectible(Collectibles.coin, Kongs.chunky, lambda _: True, None, 3),
    ],
    Regions.TempleGuitarPad: [
        Collectible(Collectibles.coin, Kongs.diddy, lambda _: True, None, 1),  # On Guitar pad
    ],
    Regions.TempleUnderwater: [
        Collectible(Collectibles.banana, Kongs.diddy, lambda _: True, None, 7),
        Collectible(Collectibles.banana, Kongs.tiny, lambda l: l.mini or l.CanPhaseswim(), None, 5),
    ],
    Regions.TempleVultureRoom: [
        Collectible(Collectibles.banana, Kongs.lanky, lambda _: True, None, 9),
        Collectible(Collectibles.bunch, Kongs.lanky, lambda _: True, None, 1),
        Collectible(Collectibles.balloon, Kongs.chunky, lambda l: l.pineapple, None, 1),
        Collectible(Collectibles.coin, Kongs.tiny, lambda _: True, None, 4),  # In vulture room
    ],
    Regions.TempleKONGRoom: [
        Collectible(Collectibles.balloon, Kongs.tiny, lambda l: l.feather, None, 2),
        Collectible(Collectibles.coin, Kongs.diddy, lambda _: True, None, 5),  # By Chimpy charge switch
    ],
    Regions.AngryAztecMain: [
        Collectible(Collectibles.balloon, Kongs.donkey, lambda l: l.coconut, None, 2),  # Cranky
        Collectible(Collectibles.balloon, Kongs.donkey, lambda l: l.coconut, None, 1),  # Behind Llama Temple
        Collectible(Collectibles.banana, Kongs.donkey, lambda _: True, None, 3),  # Near Snide
        Collectible(Collectibles.banana, Kongs.donkey, lambda _: True, None, 4),  # Near Llama Temple

        Collectible(Collectibles.banana, Kongs.diddy, lambda _: True, None, 5),  # Behind Guitar Door
        Collectible(Collectibles.banana, Kongs.diddy, lambda _: True, None, 3),  # Near Rocketbarrel
        Collectible(Collectibles.banana, Kongs.diddy, lambda _: True, None, 3),  # Gongs steps
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: l.climbing or l.jetpack, None, 3),  # Gongs Trees
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: l.jetpack, None, 1),  # Sun Ring
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: l.jetpack, None, 1),  # On top llama temple
        Collectible(Collectibles.banana, Kongs.diddy, lambda _: True, None, 4),  # 5DTemple Steps

        Collectible(Collectibles.banana, Kongs.lanky, lambda _: True, None, 5),  # Snake Road
        Collectible(Collectibles.bunch, Kongs.lanky, lambda _: True, None, 1),  # Cranky
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: l.climbing, None, 5),  # Treetops

        Collectible(Collectibles.banana, Kongs.tiny, lambda _: True, None, 10),  # Tunnel
        Collectible(Collectibles.bunch, Kongs.tiny, lambda _: True, None, 1),  # Beetle Slide
        Collectible(Collectibles.bunch, Kongs.tiny, lambda _: True, None, 1),  # Warp 5
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: l.climbing or l.twirl, None, 5),  # Treetops around 5DTemple
        Collectible(Collectibles.banana, Kongs.tiny, lambda _: True, None, 5),  # 5DTemple path

        Collectible(Collectibles.banana, Kongs.chunky, lambda _: True, None, 10),  # Around Totem
        Collectible(Collectibles.banana, Kongs.chunky, lambda _: True, None, 6),  # Snide

        Collectible(Collectibles.coin, Kongs.donkey, lambda _: True, None, 3),  # Around big boulder
        Collectible(Collectibles.coin, Kongs.donkey, lambda _: True, None, 3),  # Near Snide's
        Collectible(Collectibles.coin, Kongs.diddy, lambda _: True, None, 4),  # Around caged bonus barrel
        Collectible(Collectibles.coin, Kongs.lanky, lambda _: True, None, 5),  # W4
        Collectible(Collectibles.coin, Kongs.lanky, lambda _: True, None, 4),  # By Cranky
        Collectible(Collectibles.coin, Kongs.lanky, lambda _: True, None, 3),  # Behind 5DT
        Collectible(Collectibles.coin, Kongs.tiny, lambda _: True, None, 3),  # Around Hunky Chunky barrel
        Collectible(Collectibles.coin, Kongs.tiny, lambda _: True, None, 5),  # W5
        Collectible(Collectibles.coin, Kongs.chunky, lambda l: l.can_use_vines and l.climbing, None, 4),  # Vines by Snide's
    ],
    Regions.AztecDonkeyQuicksandCave: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: l.strongKong, None, 4),

        Collectible(Collectibles.balloon, Kongs.diddy, lambda l: l.peanut, None, 1),

        Collectible(Collectibles.coin, Kongs.chunky, lambda _: True, None, 4),  # Behind W5
    ],
    Regions.AztecBaboonBlast: [
    ],
    Regions.DonkeyTemple: [
        Collectible(Collectibles.coin, Kongs.donkey, lambda l: l.coconut or l.CanPhase(), None, 2),  # By second switch
    ],
    Regions.DiddyTemple: [
        Collectible(Collectibles.balloon, Kongs.diddy, lambda l: l.peanut, None, 1),

        Collectible(Collectibles.coin, Kongs.diddy, lambda l: l.peanut or l.CanPhase(), None, 1),  # First dead end
    ],
    Regions.DiddyTempleDeadEndRight: [
        Collectible(Collectibles.coin, Kongs.diddy, lambda _: True, None, 1),  # Second dead end
    ],
    Regions.LankyTemple: [
        Collectible(Collectibles.balloon, Kongs.lanky, lambda l: l.grape, None, 1),
    ],
    Regions.TinyTempleEntrance: [
        Collectible(Collectibles.coin, Kongs.tiny, lambda _: True, None, 1),  # Under first switch
    ],
    Regions.TinyTemple: [
        Collectible(Collectibles.coin, Kongs.tiny, lambda _: True, None, 1),  # Under second switch
        Collectible(Collectibles.coin, Kongs.tiny, lambda l: l.feather or l.CanPhase(), None, 1),  # Dead end
    ],
    Regions.ChunkyTemple: [
        Collectible(Collectibles.balloon, Kongs.chunky, lambda l: l.pineapple, None, 2),

        # Collectible(Collectibles.coin, Kongs.any, lambda l: l.shockwave, None, 1),
        Collectible(Collectibles.coin, Kongs.chunky, lambda _: True, None, 1),  # Start of second section
        Collectible(Collectibles.coin, Kongs.chunky, lambda _: True, None, 1),  # Under second pineapple switch
        Collectible(Collectibles.coin, Kongs.chunky, lambda l: l.pineapple or l.CanPhase(), None, 1),  # Under third pineapple switch
        Collectible(Collectibles.coin, Kongs.chunky, lambda l: l.pineapple or l.CanPhase(), None, 1),  # In front of door to GB
    ],
    Regions.AztecTinyRace: [
        Collectible(Collectibles.racecoin, Kongs.any, lambda _: True, None, 71),  # Race Coins
    ],
    Regions.LlamaTemple: [
        Collectible(Collectibles.banana, Kongs.donkey, lambda _: True, None, 15),
        Collectible(Collectibles.banana, Kongs.lanky, lambda _: True, None, 6),
        Collectible(Collectibles.bunch, Kongs.lanky, lambda _: True, None, 1),  # Warp 1
        Collectible(Collectibles.balloon, Kongs.lanky, lambda l: ((Events.AztecLlamaSpit in l.Events and l.swim) or (l.CanPhaseswim() and l.settings.damage_amount != DamageAmount.ohko) or l.CanPhase()) and l.grape, None, 2),

        Collectible(Collectibles.balloon, Kongs.tiny, lambda l: l.feather, None, 1),
        Collectible(Collectibles.banana, Kongs.tiny, lambda _: True, None, 3),

        Collectible(Collectibles.coin, Kongs.donkey, lambda _: True, None, 5),  # Instrument pad
        Collectible(Collectibles.coin, Kongs.tiny, lambda _: True, None, 3),  # By tag barrel
    ],
    Regions.LlamaTempleMatching: [
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: l.can_use_vines, None, 1),  # Matching game left vines

        Collectible(Collectibles.coin, Kongs.lanky, lambda l: l.can_use_vines, None, 2),  # Matching game right vines
    ],
    Regions.LlamaTempleBack: [
        Collectible(Collectibles.banana, Kongs.tiny, lambda _: True, None, 2),
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: l.CanSlamSwitch(Levels.AngryAztec, 1) or (l.twirl and l.monkey_maneuvers), None, 2),  # Behind Mini tunnel
    ],
    Regions.AngryAztecConnectorTunnel: [
    ],
    Regions.AztecTunnelBeforeOasis: [
    ],
}
