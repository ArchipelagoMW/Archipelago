# fmt: off
"""Logic file for Frantic Factory."""


from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Maps import Maps
from randomizer.Enums.MinigameType import MinigameType
from randomizer.Enums.Regions import Regions
from randomizer.Enums.HintRegion import HintRegion
from randomizer.Enums.Settings import MinigameBarrels, ShuffleLoadingZones, FasterChecksSelected, RemovedBarriersSelected
from randomizer.Enums.Transitions import Transitions
from randomizer.LogicClasses import (Event, LocationLogic, Region,
                                     TransitionFront)

LogicRegions = {
    Regions.FranticFactoryMedals: Region("Frantic Factory Medals", HintRegion.FactoryCBs, Levels.FranticFactory, False, None, [
        LocationLogic(Locations.FactoryDonkeyMedal, lambda l: l.ColoredBananas[Levels.FranticFactory][Kongs.donkey] >= l.settings.medal_cb_req_level[2]),
        LocationLogic(Locations.FactoryDiddyMedal, lambda l: l.ColoredBananas[Levels.FranticFactory][Kongs.diddy] >= l.settings.medal_cb_req_level[2]),
        LocationLogic(Locations.FactoryLankyMedal, lambda l: l.ColoredBananas[Levels.FranticFactory][Kongs.lanky] >= l.settings.medal_cb_req_level[2]),
        LocationLogic(Locations.FactoryTinyMedal, lambda l: l.ColoredBananas[Levels.FranticFactory][Kongs.tiny] >= l.settings.medal_cb_req_level[2]),
        LocationLogic(Locations.FactoryChunkyMedal, lambda l: l.ColoredBananas[Levels.FranticFactory][Kongs.chunky] >= l.settings.medal_cb_req_level[2]),
        LocationLogic(Locations.FactoryDonkeyHalfMedal, lambda l: l.ColoredBananas[Levels.FranticFactory][Kongs.donkey] >= max(1, int(l.settings.medal_cb_req_level[2] >> 1))),
        LocationLogic(Locations.FactoryDiddyHalfMedal, lambda l: l.ColoredBananas[Levels.FranticFactory][Kongs.diddy] >= max(1, int(l.settings.medal_cb_req_level[2] >> 1))),
        LocationLogic(Locations.FactoryLankyHalfMedal, lambda l: l.ColoredBananas[Levels.FranticFactory][Kongs.lanky] >= max(1, int(l.settings.medal_cb_req_level[2] >> 1))),
        LocationLogic(Locations.FactoryTinyHalfMedal, lambda l: l.ColoredBananas[Levels.FranticFactory][Kongs.tiny] >= max(1, int(l.settings.medal_cb_req_level[2] >> 1))),
        LocationLogic(Locations.FactoryChunkyHalfMedal, lambda l: l.ColoredBananas[Levels.FranticFactory][Kongs.chunky] >= max(1, int(l.settings.medal_cb_req_level[2] >> 1))),
    ], [], [], restart=-1),

    # This region serves to set up the entry for the level based on the DK Portal Location
    Regions.FranticFactoryEntryHandler: Region("Frantic Factory Entry Handler", HintRegion.Error, Levels.FranticFactory, False, None, [], [
        Event(Events.FactoryEntered, lambda _: True),
        Event(Events.HatchOpened, lambda _: True),  # Always starts open in the randomizer - Placing in here to prevent logical issues (for now)
    ], [
        TransitionFront(Regions.FranticFactoryLobby, lambda _: True, Transitions.FactoryToIsles),
        TransitionFront(Regions.FranticFactoryStart, lambda _: True),  # Don't move this away from index 1 (ShuffleDoors.py relies on this being index 1)
    ], restart=-1),

    Regions.FranticFactoryStart: Region("Frantic Factory Foyer", HintRegion.FactoryStart, Levels.FranticFactory, False, None, [
        LocationLogic(Locations.FactoryMainEnemy_LobbyLeft, lambda _: True),
        LocationLogic(Locations.FactoryMainEnemy_LobbyRight, lambda _: True),
        LocationLogic(Locations.FactoryMainEnemy_TunnelToHatch, lambda _: True),
        LocationLogic(Locations.KremKap_FactoryMainEnemy_LobbyLeft, lambda l: l.camera),
        LocationLogic(Locations.KremKap_FactoryMainEnemy_LobbyRight, lambda l: l.camera),
        LocationLogic(Locations.KremKap_FactoryMainEnemy_TunnelToHatch, lambda l: l.camera),
    ], [
        Event(Events.HatchOpened, lambda _: True),  # Always starts open in the randomizer
        Event(Events.FactoryW1aTagged, lambda _: True),
        Event(Events.FactoryW2aTagged, lambda _: True),
        Event(Events.FactoryW3aTagged, lambda _: True),
    ], [
        TransitionFront(Regions.Testing, lambda l: (Events.TestingGateOpened in l.Events or l.CanPhase()) and l.climbing),
        TransitionFront(Regions.LowerCore, lambda l: Events.HatchOpened in l.Events or l.CanPhase()),
        TransitionFront(Regions.AlcoveBeyondHatch, lambda l: Events.HatchOpened in l.Events),  # Not sure how easy it is to get there, especially without damage boosting
    ]),

    Regions.Testing: Region("Testing", HintRegion.Testing, Levels.FranticFactory, True, -1, [
        LocationLogic(Locations.FactoryDonkeyNumberGame, lambda l: l.CanSlamSwitch(Levels.FranticFactory, 1) and l.isdonkey),
        LocationLogic(Locations.FactoryDiddyBlockTower, lambda l: ((l.spring or l.CanMoontail()) and l.isdiddy), MinigameType.BonusBarrel),
        LocationLogic(Locations.FactoryLankyTestingRoomBarrel, lambda l: (l.balloon or l.monkey_maneuvers) and l.islanky, MinigameType.BonusBarrel),
        LocationLogic(Locations.FactoryTinyDartboard, lambda l: Events.DartsPlayed in l.Events and l.tiny),
        LocationLogic(Locations.FactoryKasplatBlocks, lambda l: not l.settings.kasplat_rando),
        LocationLogic(Locations.FactoryBananaFairybyCounting, lambda l: l.camera),
        LocationLogic(Locations.FactoryBananaFairybyFunky, lambda l: l.camera and Events.DartsPlayed in l.Events),
        LocationLogic(Locations.MelonCrate_Location03, lambda _: True),
        LocationLogic(Locations.FactoryMainEnemy_BlockTower0, lambda _: True),
        LocationLogic(Locations.FactoryMainEnemy_BlockTower1, lambda _: True),
        LocationLogic(Locations.FactoryMainEnemy_BlockTower2, lambda _: True),
        LocationLogic(Locations.FactoryMainEnemy_TunnelToBlockTower, lambda _: True),
        LocationLogic(Locations.FactoryMainEnemy_ToBlockTowerTunnel, lambda _: True),
        LocationLogic(Locations.KremKap_FactoryMainEnemy_BlockTower0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_FactoryMainEnemy_BlockTower1, lambda l: l.camera),
        LocationLogic(Locations.KremKap_FactoryMainEnemy_BlockTower2, lambda l: l.camera),
        LocationLogic(Locations.KremKap_FactoryMainEnemy_TunnelToBlockTower, lambda l: l.camera),
        LocationLogic(Locations.KremKap_FactoryMainEnemy_ToBlockTowerTunnel, lambda l: l.camera),
        LocationLogic(Locations.FactoryDonkeyDKArcade, lambda l: (not l.checkFastCheck(FasterChecksSelected.factory_arcade_round_1)) and (l.CanOStandTBSNoclip() and l.spawn_snags), isAuxiliary=True),
    ], [
        Event(Events.DartsPlayed, lambda l: l.CanSlamSwitch(Levels.FranticFactory, 1) and (l.mini or l.CanPhase()) and l.feather and l.istiny),
        Event(Events.FactoryW3bTagged, lambda _: True),
        Event(Events.FactoryW5bTagged, lambda _: True),
    ], [
        TransitionFront(Regions.FranticFactoryStart, lambda l: Events.TestingGateOpened in l.Events or l.CanPhase()),
        TransitionFront(Regions.RandD, lambda l: l.climbing),
        TransitionFront(Regions.Snide, lambda l: l.snideAccess),
        TransitionFront(Regions.FunkyFactory, lambda l: l.funkyAccess),
        TransitionFront(Regions.FactoryBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.RandDUpper: Region("R&D Upper", HintRegion.ResearchAndDevelopment, Levels.FranticFactory, False, None, [
        LocationLogic(Locations.FactoryDiddyRandD, lambda l: (l.guitar or l.CanAccessRNDRoom()) and l.charge and l.isdiddy),
        LocationLogic(Locations.FactoryChunkyRandD, lambda l: ((l.triangle and l.climbing) or l.CanAccessRNDRoom()) and l.punch and l.hunkyChunky and l.ischunky),
        LocationLogic(Locations.FactoryKasplatRandD, lambda l: not l.settings.kasplat_rando),
        LocationLogic(Locations.FactoryBattleArena, lambda l: not l.settings.crown_placement_rando and ((l.grab and l.donkey) or l.CanAccessRNDRoom())),
    ], [], [
        TransitionFront(Regions.ChunkyRoomPlatform, lambda _: True),
        TransitionFront(Regions.RandD, lambda _: True),
    ]),

    Regions.RandD: Region("R&D", HintRegion.ResearchAndDevelopment, Levels.FranticFactory, True, None, [
        LocationLogic(Locations.FactoryLankyRandD, lambda l: (((l.trombone or l.CanAccessRNDRoom()) and l.CanSlamSwitch(Levels.FranticFactory, 1)) or (l.CanOStandTBSNoclip() and l.spawn_snags)) and l.islanky),
        LocationLogic(Locations.FactoryMainEnemy_TunnelToRace0, lambda _: True),
        LocationLogic(Locations.FactoryMainEnemy_TunnelToRace1, lambda _: True),
        LocationLogic(Locations.KremKap_FactoryMainEnemy_TunnelToRace0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_FactoryMainEnemy_TunnelToRace1, lambda l: l.camera),
    ], [
        Event(Events.FactoryW2bTagged, lambda _: True),
    ], [
        TransitionFront(Regions.Testing, lambda _: True),
        TransitionFront(Regions.RandDUpper, lambda l: (l.climbing or l.isdiddy or l.istiny) or l.monkey_maneuvers),
        TransitionFront(Regions.FactoryTinyRaceLobby, lambda l: (l.mini and l.istiny) or l.CanPhase() or l.CanOStandTBSNoclip()),
        TransitionFront(Regions.FactoryTinyRace, lambda l: l.CanPhase() or l.CanOStandTBSNoclip(), Transitions.FactoryRandDToRace, isGlitchTransition=True),
        TransitionFront(Regions.FactoryBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.FactoryTinyRaceLobby: Region("Factory Tiny Race Lobby", HintRegion.ResearchAndDevelopment, Levels.FranticFactory, False, None, [], [], [
        TransitionFront(Regions.RandD, lambda l: (l.mini and l.istiny) or l.CanPhase()),
        TransitionFront(Regions.FactoryTinyRace, lambda l: (l.mini and l.istiny) or l.CanPhase(), Transitions.FactoryRandDToRace)
    ]),

    Regions.FactoryTinyRace: Region("Factory Tiny Race", HintRegion.ResearchAndDevelopment, Levels.FranticFactory, False, None, [
        LocationLogic(Locations.FactoryTinyCarRace, lambda l: l.HasEnoughRaceCoins(Maps.FactoryTinyRace, Kongs.tiny, not l.settings.free_trade_items)),
    ], [], [
        TransitionFront(Regions.FactoryTinyRaceLobby, lambda _: True, Transitions.FactoryRaceToRandD),
    ], Transitions.FactoryRandDToRace
    ),

    Regions.ChunkyRoomPlatform: Region("Chunky Room Platform", HintRegion.Storage, Levels.FranticFactory, False, None, [
        LocationLogic(Locations.FactoryDiddyChunkyRoomBarrel, lambda l: l.CanSlamSwitch(Levels.FranticFactory, 1) and l.isdiddy and (l.can_use_vines or l.settings.bonus_barrels == MinigameBarrels.skip), MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.PowerHut, lambda l: (l.coconut and l.isdonkey) or l.CanPhase() or l.CanMoonkick(), Transitions.FactoryChunkyRoomToPower),
        TransitionFront(Regions.BeyondHatch, lambda _: True),
    ]),

    Regions.PowerHut: Region("Power Hut", HintRegion.Storage, Levels.FranticFactory, False, None, [
        LocationLogic(Locations.FactoryDonkeyPowerHut, lambda l: Events.MainCoreActivated in l.Events and (l.isdonkey or l.settings.free_trade_items)),
    ], [
        Event(Events.MainCoreActivated, lambda l: l.grab and l.isdonkey),
    ], [
        TransitionFront(Regions.ChunkyRoomPlatform, lambda _: True, Transitions.FactoryPowerToChunkyRoom),
    ]),

    Regions.BeyondHatch: Region("Beyond Hatch", HintRegion.Storage, Levels.FranticFactory, True, -1, [
        LocationLogic(Locations.ChunkyKong, lambda l: Events.ChunkyFreed in l.Events),
        LocationLogic(Locations.FactoryLankyFreeChunky, lambda l: Events.ChunkyFreed in l.Events),
        LocationLogic(Locations.FactoryChunkyDarkRoom, lambda l: ((l.punch and l.chunky) or l.CanPhase()) and ((l.punch and l.CanSlamSwitch(Levels.FranticFactory, 1)) or l.generalclips) and l.ischunky),
        LocationLogic(Locations.RainbowCoin_Location02, lambda l: (l.punch and l.chunky) or l.CanPhase()),
        LocationLogic(Locations.FactoryKasplatStorage, lambda l: not l.settings.kasplat_rando),
        LocationLogic(Locations.MelonCrate_Location04, lambda _: True),
        LocationLogic(Locations.FactoryMainEnemy_CandyCranky0, lambda _: True),
        LocationLogic(Locations.FactoryMainEnemy_CandyCranky1, lambda _: True),
        LocationLogic(Locations.FactoryMainEnemy_DarkRoom0, lambda l: (l.punch and l.chunky) or l.CanPhase()),
        LocationLogic(Locations.FactoryMainEnemy_DarkRoom1, lambda l: (l.punch and l.chunky) or l.CanPhase()),
        LocationLogic(Locations.FactoryMainEnemy_StorageRoom, lambda _: True),
        LocationLogic(Locations.KremKap_FactoryMainEnemy_CandyCranky0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_FactoryMainEnemy_CandyCranky1, lambda l: l.camera),
        LocationLogic(Locations.KremKap_FactoryMainEnemy_DarkRoom0, lambda l: l.camera and ((l.punch and l.chunky) or l.CanPhase())),
        LocationLogic(Locations.KremKap_FactoryMainEnemy_DarkRoom1, lambda l: l.camera and ((l.punch and l.chunky) or l.CanPhase())),
        LocationLogic(Locations.KremKap_FactoryMainEnemy_StorageRoom, lambda l: l.camera),
    ], [
        Event(Events.TestingGateOpened, lambda l: l.Slam),
        Event(Events.FactoryW1bTagged, lambda _: True),
    ], [
        TransitionFront(Regions.FactoryArcadePole, lambda l: l.climbing, Transitions.FactoryStorageToArcade),
        TransitionFront(Regions.LowerCore, lambda _: True),
        TransitionFront(Regions.ChunkyRoomPlatform, lambda l: l.CanMoonkick() or (l.twirl and l.istiny and l.monkey_maneuvers) or (l.isdiddy and l.monkey_maneuvers)),
        TransitionFront(Regions.CrankyFactory, lambda l: l.crankyAccess),
        TransitionFront(Regions.CandyFactory, lambda l: l.candyAccess),
        TransitionFront(Regions.FactoryStoragePipe, lambda l: (l.islanky and l.handstand) or l.slope_resets),
        TransitionFront(Regions.FactoryBossLobby, lambda l: not l.settings.tns_location_rando),
        TransitionFront(Regions.FactoryBaboonBlast, lambda l: l.blast and l.isdonkey)  # , Transitions.FactoryMainToBBlast)
    ]),

    Regions.FactoryStoragePipe: Region("Factory Storage Pipe", HintRegion.Storage, Levels.FranticFactory, False, None, [], [
        Event(Events.ChunkyFreed, lambda l: l.CanFreeChunky())
    ], [
        TransitionFront(Regions.BeyondHatch, lambda _: True),
    ]),

    # Fake region because actually getting out of the loading zone requires Climbing
    Regions.FactoryArcadePole: Region("Factory Arcade Upper Pole", HintRegion.Storage, Levels.FranticFactory, False, None, [], [], [
        TransitionFront(Regions.FactoryArcadeTunnel, lambda l: l.climbing),
        TransitionFront(Regions.BeyondHatch, lambda _: True, Transitions.FactoryArcadeToStorage)
    ], Transitions.FactoryStorageToArcade),

    Regions.FactoryArcadeTunnel: Region("Arcade Tunnel", HintRegion.Storage, Levels.FranticFactory, False, None, [
        LocationLogic(Locations.NintendoCoin, lambda l: Events.ArcadeLeverSpawned in l.Events and l.grab and l.isdonkey and (l.GetCoins(Kongs.donkey) >= 2)),
        LocationLogic(Locations.FactoryTinybyArcade, lambda l: (l.mini and l.tiny) or l.CanPhase()),
        LocationLogic(Locations.FactoryChunkybyArcade, lambda l: ((l.punch or l.CanPhase()) and l.ischunky) or (l.CanPhase() and l.settings.free_trade_items), MinigameType.BonusBarrel),
        LocationLogic(Locations.FactoryDonkeyDKArcade, lambda l: not l.checkFastCheck(FasterChecksSelected.factory_arcade_round_1) and (Events.ArcadeLeverSpawned in l.Events and l.grab and l.isdonkey)),
    ], [
        Event(Events.FactoryW5aTagged, lambda _: True),
    ], [
        TransitionFront(Regions.FactoryArcadePole, lambda _: True),
    ]),

    Regions.FactoryBaboonBlast: Region("Factory Baboon Blast", HintRegion.Storage, Levels.FranticFactory, False, None, [
        LocationLogic(Locations.FactoryDonkeyDKArcade, lambda l: l.checkFastCheck(FasterChecksSelected.factory_arcade_round_1) and l.isdonkey, isAuxiliary=True),  # The GB is moved here on fast GBs
    ], [
        Event(Events.ArcadeLeverSpawned, lambda l: l.isdonkey)
    ], [
        TransitionFront(Regions.BeyondHatch, lambda _: True)
    ]),

    Regions.AlcoveBeyondHatch: Region("Alcove Beyond Hatch", HintRegion.ProductionRoom, Levels.FranticFactory, False, None, [], [], [
        TransitionFront(Regions.LowerCore, lambda _: True),
        TransitionFront(Regions.FranticFactoryStart, lambda l: Events.HatchOpened in l.Events and l.climbing)
    ]),

    Regions.LowerCore: Region("Lower Core", HintRegion.ProductionRoom, Levels.FranticFactory, False, -1, [
        LocationLogic(Locations.FactoryKasplatProductionBottom, lambda l: not l.settings.kasplat_rando),
        LocationLogic(Locations.FactoryMainEnemy_LowWarp4, lambda _: True),
        LocationLogic(Locations.FactoryMainEnemy_DiddySwitch, lambda _: True),
        LocationLogic(Locations.FactoryMainEnemy_TunnelToProd0, lambda _: True),
        LocationLogic(Locations.FactoryMainEnemy_TunnelToProd1, lambda _: True),
        LocationLogic(Locations.KremKap_FactoryMainEnemy_LowWarp4, lambda l: l.camera),
        LocationLogic(Locations.KremKap_FactoryMainEnemy_DiddySwitch, lambda l: l.camera),
        LocationLogic(Locations.KremKap_FactoryMainEnemy_TunnelToProd0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_FactoryMainEnemy_TunnelToProd1, lambda l: l.camera),
    ], [
        Event(Events.DiddyCoreSwitch, lambda l: l.CanSlamSwitch(Levels.FranticFactory, 1) and l.diddy),
        Event(Events.LankyCoreSwitch, lambda l: l.CanSlamSwitch(Levels.FranticFactory, 1) and l.lanky),
        Event(Events.TinyCoreSwitch, lambda l: l.CanSlamSwitch(Levels.FranticFactory, 1) and l.tiny),
        Event(Events.ChunkyCoreSwitch, lambda l: l.CanSlamSwitch(Levels.FranticFactory, 1) and l.chunky),
        Event(Events.FactoryW4aTagged, lambda _: True),
    ], [
        TransitionFront(Regions.BeyondHatch, lambda _: True),
        TransitionFront(Regions.AlcoveBeyondHatch, lambda l: Events.HatchOpened in l.Events and l.climbing),
        TransitionFront(Regions.FranticFactoryStart, lambda l: Events.HatchOpened in l.Events and l.climbing),
        TransitionFront(Regions.InsideCore, lambda l: Events.MainCoreActivated in l.Events or l.CanPhase(), Transitions.FactoryLowerCoreToInsideCore),
        TransitionFront(Regions.MiddleCore, lambda l: Events.MainCoreActivated in l.Events),
    ]),

    Regions.InsideCore: Region("Inside Core", HintRegion.ProductionRoom, Levels.FranticFactory, False, -1, [
        LocationLogic(Locations.FactoryDonkeyCrusherRoom, lambda l: (l.strongKong and l.isdonkey) or l.generalclips or l.CanPhase()),
    ], [], [
        TransitionFront(Regions.LowerCore, lambda _: True, Transitions.FactoryInsideCoreToLowerCore),
    ]),

    Regions.MiddleCore: Region("Middle Core", HintRegion.ProductionRoom, Levels.FranticFactory, False, None, [], [], [
        TransitionFront(Regions.LowerCore, lambda _: True),
        TransitionFront(Regions.SpinningCore, lambda l: l.climbing),
        TransitionFront(Regions.InsideCore, lambda l: l.ledgeclip, Transitions.FactoryLowerCoreToInsideCore, isGlitchTransition=True),
    ]),

    Regions.SpinningCore: Region("Spinning Core", HintRegion.ProductionRoom, Levels.FranticFactory, True, None, [
        LocationLogic(Locations.FactoryChunkyProductionRoom, lambda l: Events.ChunkyCoreSwitch in l.Events and Events.MainCoreActivated in l.Events and l.chunky),
    ], [
        Event(Events.FactoryW4bTagged, lambda _: True),
    ], [
        TransitionFront(Regions.MiddleCore, lambda _: True),
        TransitionFront(Regions.UpperCore, lambda l: Events.MainCoreActivated in l.Events),
    ]),

    Regions.UpperCore: Region("Upper Core", HintRegion.ProductionRoom, Levels.FranticFactory, False, None, [
        LocationLogic(Locations.FactoryDiddyProductionRoom, lambda l: Events.DiddyCoreSwitch in l.Events and Events.MainCoreActivated in l.Events and l.spring and l.diddy),
        LocationLogic(Locations.FactoryLankyProductionRoom, lambda l: Events.LankyCoreSwitch in l.Events and Events.MainCoreActivated in l.Events and ((l.handstand and l.lanky) or (l.tiny and l.settings.free_trade_items and l.slope_resets))),
        LocationLogic(Locations.FactoryTinyProductionRoom, lambda l: Events.TinyCoreSwitch in l.Events and Events.MainCoreActivated in l.Events and l.twirl and l.istiny, MinigameType.BonusBarrel),
        LocationLogic(Locations.FactoryKasplatProductionTop, lambda l: not l.settings.kasplat_rando)
    ], [], [
        TransitionFront(Regions.LowerCore, lambda _: True),
        TransitionFront(Regions.SpinningCore, lambda _: True),
        TransitionFront(Regions.FactoryBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.FactoryBossLobby: Region("Factory Boss Lobby", HintRegion.Bosses, Levels.FranticFactory, False, None, [], [], [
        TransitionFront(Regions.FactoryBoss, lambda l: l.IsBossReachable(Levels.FranticFactory)),
    ]),

    Regions.FactoryBoss: Region("Factory Boss", HintRegion.Bosses, Levels.FranticFactory, False, None, [
        LocationLogic(Locations.FactoryKey, lambda l: l.IsBossBeatable(Levels.FranticFactory)),
    ], [], []),
}
