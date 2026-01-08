# fmt: off
"""Logic file for Crystal Caves."""

from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.MinigameType import MinigameType
from randomizer.Enums.Regions import Regions
from randomizer.Enums.HintRegion import HintRegion
from randomizer.Enums.Settings import RemovedBarriersSelected
from randomizer.Enums.Transitions import Transitions
from randomizer.LogicClasses import (Event, LocationLogic, Region,
                                     TransitionFront)

LogicRegions = {
    Regions.CrystalCavesMedals: Region("Crystal Caves Medals", HintRegion.CavesCBs, Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesDonkeyMedal, lambda l: l.ColoredBananas[Levels.CrystalCaves][Kongs.donkey] >= l.settings.medal_cb_req),
        LocationLogic(Locations.CavesDiddyMedal, lambda l: l.ColoredBananas[Levels.CrystalCaves][Kongs.diddy] >= l.settings.medal_cb_req),
        LocationLogic(Locations.CavesLankyMedal, lambda l: l.ColoredBananas[Levels.CrystalCaves][Kongs.lanky] >= l.settings.medal_cb_req),
        LocationLogic(Locations.CavesTinyMedal, lambda l: l.ColoredBananas[Levels.CrystalCaves][Kongs.tiny] >= l.settings.medal_cb_req),
        LocationLogic(Locations.CavesChunkyMedal, lambda l: l.ColoredBananas[Levels.CrystalCaves][Kongs.chunky] >= l.settings.medal_cb_req),
    ], [], [], restart=-1),

    # This region serves to set up the entry for the level based on the DK Portal Location
    Regions.CrystalCavesEntryHandler: Region("Crystal Caves Entry Handler", HintRegion.Error, Levels.CreepyCastle, False, None, [], [
        Event(Events.CavesEntered, lambda l: True),
    ], [
        TransitionFront(Regions.CrystalCavesLobby, lambda l: True, Transitions.CavesToIsles),
        TransitionFront(Regions.CrystalCavesMain, lambda l: True),  # Don't move this away from index 1 (ShuffleDoors.py relies on this being index 1)
    ], restart=-1),

    Regions.CrystalCavesMain: Region("Crystal Caves Main", HintRegion.MainCaves, Levels.CrystalCaves, True, None, [
        LocationLogic(Locations.CavesDiddyJetpackBarrel, lambda l: ((l.jetpack and l.isdiddy) or ((not l.settings.shuffle_shops) and l.advanced_platforming and ((l.isdonkey and (not l.isKrushaAdjacent(Kongs.donkey))) or (l.istiny and l.twirl)) and l.settings.free_trade_items)), MinigameType.BonusBarrel),
        LocationLogic(Locations.CavesKasplatNearLab, lambda l: not l.settings.kasplat_rando),
        LocationLogic(Locations.CavesMainEnemy_Start, lambda l: True),
        LocationLogic(Locations.CavesMainEnemy_NearIceCastle, lambda l: True),
        LocationLogic(Locations.CavesMainEnemy_NearFunky, lambda l: True),
        LocationLogic(Locations.CavesMainEnemy_NearBonusRoom, lambda l: True),
        LocationLogic(Locations.CavesMainEnemy_NearSnide, lambda l: True),
    ], [
        Event(Events.CavesSmallBoulderButton, lambda l: l.ischunky and l.barrels),
        Event(Events.CavesW1aTagged, lambda l: True),
        Event(Events.CavesW2aTagged, lambda l: True),
    ], [
        TransitionFront(Regions.CavesGGRoom, lambda l: (l.punch and l.chunky) or l.CanPhase() or l.CanPhaseswim() or l.checkBarrier(RemovedBarriersSelected.caves_ice_walls)),
        TransitionFront(Regions.CavesBlueprintCave, lambda l: (l.mini and l.twirl and l.istiny) or l.CanPhase() or l.CanSkew(True)),
        TransitionFront(Regions.CavesBonusCave, lambda l: (l.mini and l.istiny) or l.CanPhase() or l.CanSkew(True)),
        TransitionFront(Regions.CavesBlueprintPillar, lambda l: (l.jetpack and l.diddy) or (l.advanced_platforming and ((l.balloon and l.lanky) or ((not l.settings.shuffle_shops) and l.twirl and l.tiny)))),
        TransitionFront(Regions.CavesBananaportSpire, lambda l: (l.jetpack and l.diddy) or l.advanced_platforming),
        TransitionFront(Regions.BoulderCave, lambda l: (l.punch and l.chunky) or l.CanSkew(True) or l.checkBarrier(RemovedBarriersSelected.caves_ice_walls)),
        TransitionFront(Regions.CavesLankyRace, lambda l: (l.CanSlamSwitch(Levels.CrystalCaves, 2) and (l.balloon or l.advanced_platforming) and l.islanky) or l.CanPhase() or l.CanSkew(True), Transitions.CavesMainToRace),
        TransitionFront(Regions.FrozenCastle, lambda l: (l.CanSlamSwitch(Levels.CrystalCaves, 2) and l.islanky) or l.CanSkew(True), Transitions.CavesMainToCastle),
        TransitionFront(Regions.IglooArea, lambda l: True),
        TransitionFront(Regions.CabinArea, lambda l: True),
        TransitionFront(Regions.FunkyCaves, lambda l: l.funkyAccess),
        TransitionFront(Regions.CrankyCaves, lambda l: l.crankyAccess),
        TransitionFront(Regions.CavesSnideArea, lambda l: (l.punch and l.chunky) or l.CanPhase() or l.CanPhaseswim() or l.checkBarrier(RemovedBarriersSelected.caves_ice_walls)),
        TransitionFront(Regions.CavesBossLobby, lambda l: not l.settings.tns_location_rando and ((l.punch and l.chunky) or l.CanPhase() or l.CanPhaseswim() or l.checkBarrier(RemovedBarriersSelected.caves_ice_walls))),
        TransitionFront(Regions.CavesBaboonBlast, lambda l: l.blast and l.isdonkey)  # , Transitions.CavesMainToBBlast)
    ]),

    Regions.CavesGGRoom: Region("Caves GG Room", HintRegion.MainCaves, Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesChunkyGorillaGone, lambda l: l.gorillaGone and l.ischunky),
    ], [], [
        TransitionFront(Regions.CrystalCavesMain, lambda l: True),
    ]),

    Regions.CavesSnideArea: Region("Caves Snide Area", HintRegion.MainCaves, Levels.CrystalCaves, False, None, [], [], [
        TransitionFront(Regions.Snide, lambda l: l.snideAccess),
        TransitionFront(Regions.CrystalCavesMain, lambda l: True),
        TransitionFront(Regions.CavesBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.CavesBlueprintCave: Region("Caves Blueprint Cave", HintRegion.MainCaves, Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesKasplatNearFunky, lambda l: not l.settings.kasplat_rando),
    ], [
        Event(Events.CavesMonkeyportAccess, lambda l: l.istiny and l.monkeyport),
        Event(Events.CavesW4bTagged, lambda l: True),
    ], [
        TransitionFront(Regions.CrystalCavesMain, lambda l: (l.mini and l.istiny) or l.CanPhase() or l.CanSkew(True))
    ]),

    Regions.CavesBonusCave: Region("Caves Bonus Cave", HintRegion.MainCaves, Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesTinyCaveBarrel, lambda l: l.istiny or l.settings.free_trade_items, MinigameType.BonusBarrel),
    ], [
        Event(Events.CavesW3bTagged, lambda l: Locations.CavesTinyCaveBarrel in l.SpecialLocationsReached),
    ], [
        TransitionFront(Regions.CrystalCavesMain, lambda l: (l.mini and l.istiny) or l.CanPhase() or l.CanSkew(True))
    ]),

    Regions.CavesBlueprintPillar: Region("Caves Blueprint Pillar", HintRegion.MainCaves, Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesKasplatPillar, lambda l: not l.settings.kasplat_rando),
    ], [
        Event(Events.CavesW5aTagged, lambda l: True),
    ], [
        TransitionFront(Regions.CrystalCavesMain, lambda l: True),
    ]),

    Regions.CavesBananaportSpire: Region("Caves Bananaport Spire", HintRegion.MainCaves, Levels.CrystalCaves, False, None, [], [
        Event(Events.CavesW4aTagged, lambda l: True),
    ], [
        TransitionFront(Regions.CrystalCavesMain, lambda l: True)
    ]),

    Regions.CavesBaboonBlast: Region("Caves Baboon Blast", HintRegion.MainCaves, Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesDonkeyBaboonBlast, lambda l: l.isdonkey, MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.CrystalCavesMain, lambda l: True)
    ]),

    Regions.BoulderCave: Region("Boulder Cave", HintRegion.MainCaves, Levels.CrystalCaves, True, None, [], [
        Event(Events.CavesLargeBoulderButton, lambda l: Events.CavesSmallBoulderButton in l.Events and l.hunkyChunky and l.chunky and l.barrels),
    ], [
        TransitionFront(Regions.CrystalCavesMain, lambda l: True),
        TransitionFront(Regions.CavesBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.CavesLankyRace: Region("Caves Lanky Race", HintRegion.MainCaves, Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesLankyBeetleRace, lambda l: l.sprint and l.islanky),
    ], [], [
        TransitionFront(Regions.CrystalCavesMain, lambda l: True, Transitions.CavesRaceToMain),
    ], Transitions.CavesMainToRace
    ),

    Regions.FrozenCastle: Region("Frozen Castle", HintRegion.MainCaves, Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesLankyCastle, lambda l: l.Slam and (l.islanky or (l.settings.free_trade_items and (not l.isdonkey or l.superSlam)))),
    ], [], [
        TransitionFront(Regions.CrystalCavesMain, lambda l: True, Transitions.CavesCastleToMain),
    ]),

    Regions.IglooArea: Region("Igloo Area", HintRegion.Igloo, Levels.CrystalCaves, True, None, [
        LocationLogic(Locations.CavesTinyMonkeyportIgloo, lambda l: ((Events.CavesMonkeyportAccess in l.Events or l.CanPhaseswim()) and l.istiny) or (l.CanPhaseswim() and l.settings.free_trade_items)),  # GB is in this region but the rest is not
        LocationLogic(Locations.CavesChunkyTransparentIgloo, lambda l: ((Events.CavesLargeBoulderButton in l.Events or l.generalclips or l.CanPhaseswim()) and l.chunky) or ((l.generalclips or l.CanPhaseswim()) and l.settings.free_trade_items)),
        LocationLogic(Locations.CavesKasplatOn5DI, lambda l: not l.settings.kasplat_rando),
    ], [
        Event(Events.CavesW1bTagged, lambda l: True),
        Event(Events.CavesW3aTagged, lambda l: True),
    ], [
        TransitionFront(Regions.CrystalCavesMain, lambda l: True),
        TransitionFront(Regions.GiantKosha, lambda l: Events.CavesLargeBoulderButton in l.Events and l.monkeyport and l.istiny),
        TransitionFront(Regions.DonkeyIgloo, lambda l: ((l.checkBarrier(RemovedBarriersSelected.caves_igloo_pads) or (l.jetpack and l.diddy)) and (l.bongos and l.isdonkey)) or l.CanPhaseswim() or l.CanPhase(), Transitions.CavesIglooToDonkey),
        TransitionFront(Regions.DiddyIgloo, lambda l: ((l.checkBarrier(RemovedBarriersSelected.caves_igloo_pads) or (l.jetpack and l.diddy)) and (l.guitar and l.isdiddy)) or l.CanPhaseswim() or l.CanPhase(), Transitions.CavesIglooToDiddy),
        TransitionFront(Regions.LankyIgloo, lambda l: ((l.checkBarrier(RemovedBarriersSelected.caves_igloo_pads) or (l.jetpack and l.diddy)) and (l.trombone and l.islanky)) or l.CanPhaseswim() or l.CanPhase(), Transitions.CavesIglooToLanky),
        TransitionFront(Regions.TinyIgloo, lambda l: ((l.checkBarrier(RemovedBarriersSelected.caves_igloo_pads) or (l.jetpack and l.diddy)) and (l.saxophone and l.istiny)) or l.CanPhaseswim() or l.CanPhase(), Transitions.CavesIglooToTiny),
        TransitionFront(Regions.ChunkyIgloo, lambda l: ((l.checkBarrier(RemovedBarriersSelected.caves_igloo_pads) or (l.jetpack and l.diddy)) and (l.triangle and l.ischunky)) or l.CanPhaseswim() or l.CanPhase(), Transitions.CavesIglooToChunky),
        TransitionFront(Regions.CavesBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.GiantKosha: Region("Giant Kosha", HintRegion.Igloo, Levels.CrystalCaves, False, -1, [
        LocationLogic(Locations.RainbowCoin_Location10, lambda l: True),
    ], [
        Event(Events.GiantKoshaDefeated, lambda l: l.shockwave or l.HasInstrument(Kongs.any)),
    ], [
    ]),

    # Deaths in Donkey and Diddy's igloos take you back to them, the others to the beginning of the level
    Regions.DonkeyIgloo: Region("Donkey Igloo", HintRegion.Igloo, Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesDonkey5DoorIgloo, lambda l: (l.strongKong and l.isdonkey) or l.CanMoonkick()),
        LocationLogic(Locations.Caves5DIDKEnemy_Right, lambda l: True),
        LocationLogic(Locations.Caves5DIDKEnemy_Left, lambda l: True),
    ], [], [
        TransitionFront(Regions.IglooArea, lambda l: True, Transitions.CavesDonkeyToIgloo),
    ]),

    Regions.DiddyIgloo: Region("Diddy Igloo", HintRegion.Igloo, Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesDiddy5DoorIgloo, lambda l: (l.isdiddy or l.settings.free_trade_items) and l.barrels),
    ], [], [
        TransitionFront(Regions.IglooArea, lambda l: True, Transitions.CavesDiddyToIgloo),
    ]),

    Regions.LankyIgloo: Region("Lanky Igloo", HintRegion.Igloo, Levels.CrystalCaves, False, TransitionFront(Regions.CrystalCavesEntryHandler, lambda l: ((l.balloon or l.advanced_platforming) and l.islanky) or (l.settings.free_trade_items and l.advanced_platforming and (l.isdiddy or l.istiny))), [
        LocationLogic(Locations.CavesLanky5DoorIgloo, lambda l: ((l.balloon or l.advanced_platforming) and l.islanky) or (l.settings.free_trade_items and l.advanced_platforming and (l.isdiddy or l.istiny))),
    ], [], [
        TransitionFront(Regions.IglooArea, lambda l: True, Transitions.CavesLankyToIgloo),
    ]),

    Regions.TinyIgloo: Region("Tiny Igloo", HintRegion.Igloo, Levels.CrystalCaves, False, -1, [
        LocationLogic(Locations.CavesTiny5DoorIgloo, lambda l: l.Slam and l.istiny),
        LocationLogic(Locations.CavesBananaFairyIgloo, lambda l: l.Slam and l.istiny and l.camera),
        LocationLogic(Locations.Caves5DITinyEnemy_BigEnemy, lambda l: True),
    ], [], [
        TransitionFront(Regions.IglooArea, lambda l: True, Transitions.CavesTinyToIgloo),
    ]),

    Regions.ChunkyIgloo: Region("Chunky Igloo", HintRegion.Igloo, Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesChunky5DoorIgloo, lambda l: l.ischunky or l.settings.free_trade_items),
    ], [], [
        TransitionFront(Regions.IglooArea, lambda l: True, Transitions.CavesChunkyToIgloo),
    ]),

    Regions.CabinArea: Region("Cabin Area", HintRegion.Cabins, Levels.CrystalCaves, True, None, [
        LocationLogic(Locations.CavesKasplatNearCandy, lambda l: not l.settings.kasplat_rando),
        LocationLogic(Locations.CavesMainEnemy_Outside5DC, lambda l: True),
        LocationLogic(Locations.CavesMainEnemy_1DCWaterfall, lambda l: True),
        LocationLogic(Locations.CavesMainEnemy_1DCHeadphones, lambda l: True),
    ], [
        Event(Events.CavesW2bTagged, lambda l: True),
        Event(Events.CavesW5bTagged, lambda l: True),
    ], [
        TransitionFront(Regions.CrystalCavesMain, lambda l: True),
        TransitionFront(Regions.CavesRotatingCabinRoof, lambda l: (l.isdiddy and l.jetpack) or l.CanMoonkick() or ((l.isdiddy or l.istiny or (l.islanky and not l.isKrushaAdjacent(Kongs.lanky))) and l.advanced_platforming) or l.CanPhase()),
        TransitionFront(Regions.RotatingCabin, lambda l: (l.bongos and l.isdonkey) or l.CanPhase() or l.CanSkew(True), Transitions.CavesCabinToRotating),
        TransitionFront(Regions.DonkeyCabin, lambda l: (l.bongos and l.isdonkey) or l.CanPhase() or l.CanSkew(True) or l.generalclips, Transitions.CavesCabinToDonkey),
        TransitionFront(Regions.DiddyLowerCabin, lambda l: (l.guitar and l.isdiddy) or l.CanPhase() or l.CanSkew(True), Transitions.CavesCabinToDiddyLower),
        TransitionFront(Regions.DiddyUpperCabin, lambda l: (l.guitar and l.isdiddy) or l.CanPhase() or l.CanSkew(True), Transitions.CavesCabinToDiddyUpper),
        TransitionFront(Regions.CavesSprintCabinRoof, lambda l: (l.isdiddy and l.jetpack) or (l.islanky and l.balloon) or l.CanMoonkick() or l.CanPhase()),
        TransitionFront(Regions.LankyCabin, lambda l: (l.trombone and l.balloon and l.islanky) or l.CanPhase() or l.CanSkew(True), Transitions.CavesCabinToLanky),
        TransitionFront(Regions.TinyCabin, lambda l: (l.saxophone and l.istiny) or l.CanPhase() or l.CanSkew(True), Transitions.CavesCabinToTiny),
        TransitionFront(Regions.ChunkyCabin, lambda l: (l.triangle and l.ischunky) or l.CanPhase() or l.CanSkew(True), Transitions.CavesCabinToChunky),
        TransitionFront(Regions.CandyCaves, lambda l: l.candyAccess),
    ]),

    Regions.CavesSprintCabinRoof: Region("Caves Sprint Cabin Roof", HintRegion.Cabins, Levels.CrystalCaves, False, None, [], [], [
        TransitionFront(Regions.CabinArea, lambda l: True),
        TransitionFront(Regions.CavesBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.CavesRotatingCabinRoof: Region("Caves Rotating Cabin Roof", HintRegion.Cabins, Levels.CrystalCaves, False, None, [], [], [
        TransitionFront(Regions.CabinArea, lambda l: True),
        TransitionFront(Regions.CavesBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.RotatingCabin: Region("Rotating Cabin", HintRegion.Cabins, Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesDonkeyRotatingCabin, lambda l: (l.Slam and l.isdonkey) or l.CanMoonkick()),
        LocationLogic(Locations.CavesBattleArena, lambda l: not l.settings.crown_placement_rando and l.Slam and l.isdonkey),
    ], [], [
        TransitionFront(Regions.CabinArea, lambda l: True, Transitions.CavesRotatingToCabin),
    ]),

    # Lanky's and Diddy's cabins take you to the beginning of the level, others respawn there
    Regions.DonkeyCabin: Region("Donkey Cabin", HintRegion.Cabins, Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesDonkey5DoorCabin, lambda l: (l.homing or l.settings.hard_shooting) and (l.HasGun(Kongs.donkey) or (l.settings.free_trade_items and l.HasGun(Kongs.any)))),
    ], [], [
        TransitionFront(Regions.CabinArea, lambda l: True, Transitions.CavesDonkeyToCabin),
    ]),

    Regions.DiddyLowerCabin: Region("Diddy Lower Cabin", HintRegion.Cabins, Levels.CrystalCaves, False, None, [
        # You're supposed to use the jetpack to get up the platforms, but you can just backflip onto them
        LocationLogic(Locations.CavesDiddy5DoorCabinLower, lambda l: l.isdiddy and l.oranges and (l.jetpack or l.advanced_platforming)),
    ], [], [
        TransitionFront(Regions.CabinArea, lambda l: True, Transitions.CavesDiddyLowerToCabin),
    ]),

    Regions.DiddyUpperCabin: Region("Diddy Upper Cabin", HintRegion.Cabins, Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesDiddy5DoorCabinUpper, lambda l: (l.guitar or l.oranges) and (l.spring or (l.CanMoontail() and not l.cabinBarrelMoved())) and l.jetpack and l.isdiddy),
        LocationLogic(Locations.CavesBananaFairyCabin, lambda l: l.camera and (l.guitar or l.oranges) and (l.spring or (l.CanMoontail() and not l.cabinBarrelMoved())) and l.jetpack and l.isdiddy),
        # LocationLogic(Locations.Caves5DCDiddyUpperEnemy_Enemy0, lambda l: True),
        # LocationLogic(Locations.Caves5DCDiddyUpperEnemy_Enemy1, lambda l: True),
    ], [], [
        TransitionFront(Regions.CabinArea, lambda l: True, Transitions.CavesDiddyUpperToCabin),
    ]),

    Regions.LankyCabin: Region("Lanky Cabin", HintRegion.Cabins, Levels.CrystalCaves, False, -1, [
        LocationLogic(Locations.CavesLanky1DoorCabin, lambda l: l.sprint and l.balloon and l.islanky),
        LocationLogic(Locations.Caves1DCEnemy_Near, lambda l: True),
    ], [], [
        TransitionFront(Regions.CabinArea, lambda l: True, Transitions.CavesLankyToCabin),
    ]),

    Regions.TinyCabin: Region("Tiny Cabin", HintRegion.Cabins, Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesTiny5DoorCabin, lambda l: (l.istiny or l.settings.free_trade_items) and l.oranges),
    ], [], [
        TransitionFront(Regions.CabinArea, lambda l: True, Transitions.CavesTinyToCabin),
    ]),

    Regions.ChunkyCabin: Region("Chunky Cabin", HintRegion.Cabins, Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesChunky5DoorCabin, lambda l: l.gorillaGone and l.Slam and l.ischunky, MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.CabinArea, lambda l: True, Transitions.CavesChunkyToCabin),
    ]),

    Regions.CavesBossLobby: Region("Caves Boss Lobby", HintRegion.Bosses, Levels.CrystalCaves, True, None, [], [], [
        TransitionFront(Regions.CavesBoss, lambda l: l.IsBossReachable(Levels.CrystalCaves)),
    ]),

    Regions.CavesBoss: Region("Caves Boss", HintRegion.Bosses, Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesKey, lambda l: l.IsBossBeatable(Levels.CrystalCaves)),
    ], [], []),
}
