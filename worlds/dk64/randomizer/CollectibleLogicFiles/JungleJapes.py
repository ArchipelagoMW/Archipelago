# fmt: off
"""Collectible logic file for Jungle Japes."""

from randomizer.Enums.Collectibles import Collectibles
from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Switches import Switches
from randomizer.LogicClasses import Collectible

LogicRegions = {
    Regions.JungleJapesStart: [
        Collectible(Collectibles.banana, Kongs.donkey, lambda l: l.climbing and (l.can_use_vines or (l.monkey_maneuvers and (not l.isKrushaAdjacent(Kongs.donkey)))), None, 5),  # Starting area
        Collectible(Collectibles.bunch, Kongs.donkey, lambda _: True, None, 1),  # W3
        Collectible(Collectibles.balloon, Kongs.donkey, lambda l: l.coconut, None, 1),  # Above underground
        Collectible(Collectibles.banana, Kongs.diddy, lambda _: True, None, 5),  # Starting area
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: l.climbing, None, 2),  # Treetops, TB side
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: l.swim, None, 2),  # Underwater
        Collectible(Collectibles.banana, Kongs.lanky, lambda l: l.swim, None, 5),  # In river
        Collectible(Collectibles.banana, Kongs.lanky, lambda _: True, None, 1),  # Painting Slope
        Collectible(Collectibles.banana, Kongs.tiny, lambda _: True, None, 5),  # In first tunnel
        Collectible(Collectibles.banana, Kongs.chunky, lambda _: True, None, 5),  # Around entrance to underground
        Collectible(Collectibles.coin, Kongs.donkey, lambda _: True, None, 3),  # In first tunnel
        Collectible(Collectibles.coin, Kongs.diddy, lambda l: l.swim, None, 3),  # In river
        Collectible(Collectibles.coin, Kongs.lanky, lambda l: l.swim, None, 2),  # In river
        Collectible(Collectibles.coin, Kongs.chunky, lambda _: True, None, 3),  # By DK Portal
        Collectible(Collectibles.coin, Kongs.chunky, lambda l: l.swim, None, 3),  # In river
    ],
    Regions.JapesBlastPadPlatform: [
        Collectible(Collectibles.coin, Kongs.donkey, lambda _: True, None, 3),  # Around BBlast pad
    ],
    Regions.JapesHill: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: l.climbing, None, 1),  # Tree by Funky's
    ],
    Regions.JapesHillTop: [
        Collectible(Collectibles.banana, Kongs.donkey, lambda _: True, None, 6),  # Between Snide's and Diddy's cage
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: l.climbing, None, 1),  # Tree by Diddy's cage
        Collectible(Collectibles.balloon, Kongs.donkey, lambda l: l.coconut, None, 1),  # Snide's
        Collectible(Collectibles.banana, Kongs.diddy, lambda _: True, None, 7),  # Around mountain
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: l.climbing, None, 1),  # Treetop by Snide's
        Collectible(Collectibles.bunch, Kongs.lanky, lambda _: True, None, 1),  # Next to Snide's
        Collectible(Collectibles.bunch, Kongs.chunky, lambda _: True, None, 2),  # On Funky's store

        Collectible(Collectibles.coin, Kongs.lanky, lambda _: True, None, 5),  # By Snide's
    ],
    Regions.JapesCannonPlatform: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: l.climbing, None, 1),  # Tree by cannon
        Collectible(Collectibles.coin, Kongs.diddy, lambda _: True, None, 2),  # Cannon to Diddy's cage
    ],
    Regions.JungleJapesMain: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda _: True, None, 1),  # W3
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: l.climbing, None, 2),  # Treetops, Painting room side

        # Collectible(Collectibles.coin, Kongs.any, lambda l: l.shockwave and ((l.handstand and l.lanky) or (l.twirl and l.tiny) or l.CanMoonkick() or ((l.generalclips or l.CanPhase()) and (l.istiny or l.isdiddy))), None, 1),  # Rainbow coin
    ],
    Regions.JapesPaintingRoomHill: [
        Collectible(Collectibles.banana, Kongs.lanky, lambda _: True, None, 2),  # Slope to painting room
    ],
    Regions.JapesTnSAlcove: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda _: True, None, 1),  # By Troff n Scoff
    ],
    Regions.JapesBaboonBlast: [
        Collectible(Collectibles.bunch, Kongs.donkey, lambda _: True, None, 2),
        Collectible(Collectibles.coin, Kongs.donkey, lambda _: True, None, 2),
    ],
    Regions.JapesBeyondCoconutGate1: [
        Collectible(Collectibles.banana, Kongs.chunky, lambda _: True, None, 10),
        Collectible(Collectibles.coin, Kongs.donkey, lambda _: True, None, 3),  # By DK BP
        Collectible(Collectibles.coin, Kongs.tiny, lambda _: True, None, 3),  # By Tiny BP

    ],
    Regions.JapesBeyondCoconutGate2: [
        Collectible(Collectibles.banana, Kongs.donkey, lambda _: True, None, 9),  # Path to Cranky
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: l.hasMoveSwitchsanity(Switches.JapesRambi, False) or l.CanPhase(), None, 1),  # Under Rambi box
        Collectible(Collectibles.bunch, Kongs.donkey, lambda l: Events.Rambi in l.Events or l.CanPhase(), None, 1),  # In breakable hut
        Collectible(Collectibles.balloon, Kongs.donkey, lambda l: l.coconut, None, 1),  # In front of Cranky's
        Collectible(Collectibles.banana, Kongs.diddy, lambda _: True, None, 3),  # By Diddy BP
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: Events.Rambi in l.Events or l.CanPhase(), None, 1),  # In breakable hut
        Collectible(Collectibles.banana, Kongs.lanky, lambda _: True, None, 1),  # To Lanky BP room
        Collectible(Collectibles.banana, Kongs.lanky, lambda _: True, None, 2),  # Base of slippery slopes
        Collectible(Collectibles.banana, Kongs.lanky, lambda l: l.handstand or l.slope_resets, None, 2),  # To bonus barrel on slippery slope
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: l.climbing, None, 1),  # On treetop in Cranky area
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: Events.Rambi in l.Events or l.CanPhase(), None, 1),  # In breakable hut
        Collectible(Collectibles.balloon, Kongs.lanky, lambda l: l.grape, None, 1),  # In Lanky BP room
        Collectible(Collectibles.balloon, Kongs.lanky, lambda l: l.grape, None, 1),  # By hut
        Collectible(Collectibles.banana, Kongs.tiny, lambda _: True, None, 2),  # Before Rambi door
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: l.climbing, None, 1),  # On treetop in Cranky area
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: Events.Rambi in l.Events or l.CanPhase(), None, 1),  # In breakable hut
        Collectible(Collectibles.balloon, Kongs.tiny, lambda l: l.feather, None, 1),  # By hut
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: l.climbing, None, 1),  # On Cranky's Lab

        Collectible(Collectibles.coin, Kongs.donkey, lambda l: l.can_use_vines, None, 1),  # Between vines
        Collectible(Collectibles.coin, Kongs.donkey, lambda l: l.hasMoveSwitchsanity(Switches.JapesRambi, False) or l.CanPhase(), None, 3),  # In rambi box cage
        Collectible(Collectibles.coin, Kongs.diddy, lambda _: True, None, 3),  # By Diddy BP
        Collectible(Collectibles.coin, Kongs.lanky, lambda _: True, None, 3),  # By Lanky BP
    ],
    Regions.JapesUselessSlope: [
        Collectible(Collectibles.banana, Kongs.lanky, lambda _: True, None, 2),  # On useless slippery slope
        Collectible(Collectibles.bunch, Kongs.lanky, lambda _: True, None, 1),  # On top of slippery slope
    ],
    Regions.JapesBeyondFeatherGate: [
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: l.mini or l.CanPhase(), None, 3),  # In hollow trunk to the left
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: l.mini or l.CanPhase(), None, 3),  # In hollow trunk to the right
        Collectible(Collectibles.bunch, Kongs.tiny, lambda _: True, None, 1),  # By beehive
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: l.climbing and l.hunkyChunky, None, 4),

        Collectible(Collectibles.coin, Kongs.chunky, lambda _: True, None, 3),  # Behind stump
    ],
    Regions.JapesBeyondPeanutGate: [
        Collectible(Collectibles.balloon, Kongs.diddy, lambda l: l.peanut, None, 1),
        Collectible(Collectibles.bunch, Kongs.lanky, lambda l: l.grape or l.CanPhase() or l.generalclips, None, 1),
        Collectible(Collectibles.bunch, Kongs.tiny, lambda l: l.feather or l.CanPhase(), None, 1),

        Collectible(Collectibles.coin, Kongs.diddy, lambda _: True, None, 3),
        Collectible(Collectibles.coin, Kongs.lanky, lambda _: True, None, 3),
    ],
    Regions.Mine: [
        Collectible(Collectibles.banana, Kongs.diddy, lambda _: True, None, 5),  # In stream
        Collectible(Collectibles.bunch, Kongs.diddy, lambda _: True, None, 1),  # On mound by peanut switch
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: (l.CanSlamSwitch(Levels.JungleJapes, 1) or l.CanPhase()), None, 1),  # On box by conveyors
        Collectible(Collectibles.bunch, Kongs.diddy, lambda l: (l.CanSlamSwitch(Levels.JungleJapes, 1) or l.CanPhase()) and (l.charge or l.monkey_maneuvers), None, 1),  # In minecart
        Collectible(Collectibles.balloon, Kongs.diddy, lambda l: (l.CanSlamSwitch(Levels.JungleJapes, 1) or l.CanPhase()) and l.peanut, None, 1),  # In conveyor room

        Collectible(Collectibles.coin, Kongs.diddy, lambda l: l.peanut or l.monkey_maneuvers, None, 1),  # On bridge to switch
        Collectible(Collectibles.coin, Kongs.diddy, lambda _: True, None, 1),  # On coal pile
        Collectible(Collectibles.coin, Kongs.diddy, lambda l: l.charge or l.CanPhase(), None, 1),  # Next to conveyor control
        Collectible(Collectibles.coin, Kongs.diddy, lambda l: l.CanSlamSwitch(Levels.JungleJapes, 1) or l.CanPhase(), None, 1),  # Under conveyors
    ],
    Regions.JapesMinecarts: [
        Collectible(Collectibles.racecoin, Kongs.any, lambda _: True, None, 85),  # Race Coins
    ],
    Regions.JapesTopOfMountain: [
        Collectible(Collectibles.balloon, Kongs.diddy, lambda l: l.peanut, None, 1),  # Above mountain
        Collectible(Collectibles.coin, Kongs.tiny, lambda _: True, None, 5),  # Around W5
    ],
    Regions.JapesLankyCave: [
        Collectible(Collectibles.bunch, Kongs.lanky, lambda _: True, None, 2),  # On steps
        Collectible(Collectibles.bunch, Kongs.lanky, lambda _: True, None, 2),  # On pegs
        Collectible(Collectibles.balloon, Kongs.lanky, lambda l: l.grape, None, 1),

        Collectible(Collectibles.coin, Kongs.lanky, lambda _: True, None, 2),
    ],
    Regions.BeyondRambiGate: [
        Collectible(Collectibles.banana, Kongs.lanky, lambda _: True, None, 5),
        Collectible(Collectibles.banana, Kongs.tiny, lambda _: True, None, 5),
        Collectible(Collectibles.balloon, Kongs.tiny, lambda l: l.feather, None, 1),
        Collectible(Collectibles.bunch, Kongs.chunky, lambda l: l.barrels, None, 1),
        Collectible(Collectibles.balloon, Kongs.chunky, lambda l: l.pineapple, None, 3),

        Collectible(Collectibles.coin, Kongs.tiny, lambda l: l.swim, None, 5),  # In water by fairy
    ],
    Regions.TinyHive: [
        Collectible(Collectibles.banana, Kongs.tiny, lambda l: ((l.CanSlamSwitch(Levels.JungleJapes, 1) and (l.saxophone or l.oranges)) or l.CanPhase() or l.generalclips), None, 8),
        Collectible(Collectibles.balloon, Kongs.tiny, lambda l: l.feather, None, 1),

        Collectible(Collectibles.coin, Kongs.tiny, lambda l: ((l.CanSlamSwitch(Levels.JungleJapes, 1) and (l.saxophone or l.oranges)) or l.CanPhase() or l.generalclips), None, 2),
    ],
    Regions.JapesCatacomb: [
        Collectible(Collectibles.banana, Kongs.chunky, lambda _: True, None, 5),
        Collectible(Collectibles.bunch, Kongs.chunky, lambda _: True, None, 2),

        Collectible(Collectibles.coin, Kongs.tiny, lambda _: True, None, 3),
        Collectible(Collectibles.coin, Kongs.chunky, lambda l: (l.can_use_vines and l.pineapple and l.ischunky) or l.CanPhase(), None, 3),
    ]
}
