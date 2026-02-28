# fmt: off
"""Logic file for DK Isles."""

from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.MinigameType import MinigameType
from randomizer.Enums.Regions import Regions
from randomizer.Enums.HintRegion import HintRegion
from randomizer.Enums.Settings import FungiTimeSetting, MinigameBarrels, CBRando, RemovedBarriersSelected
from randomizer.Enums.Transitions import Transitions
from randomizer.Enums.Switches import Switches
from randomizer.LogicClasses import (Event, LocationLogic, Region,
                                     TransitionFront)

LogicRegions = {
    Regions.GameStart: Region("Game Start", HintRegion.GameStart, Levels.DKIsles, False, None, [
        # The locations in this region should *only* be training barrels and starting moves - if you need to put something here, make another region (e.g. Credits)
        LocationLogic(Locations.IslesVinesTrainingBarrel, lambda l: l.settings.fast_start_beginning_of_game),
        LocationLogic(Locations.IslesSwimTrainingBarrel, lambda l: l.settings.fast_start_beginning_of_game),
        LocationLogic(Locations.IslesOrangesTrainingBarrel, lambda l: l.settings.fast_start_beginning_of_game),
        LocationLogic(Locations.IslesBarrelsTrainingBarrel, lambda l: l.settings.fast_start_beginning_of_game),
        # Starting Shop Owners
        LocationLogic(Locations.ShopOwner_Location00, lambda _: True),
        LocationLogic(Locations.ShopOwner_Location01, lambda _: True),
        LocationLogic(Locations.ShopOwner_Location02, lambda _: True),
        LocationLogic(Locations.ShopOwner_Location03, lambda _: True),
        # Starting Moves
        LocationLogic(Locations.IslesFirstMove, lambda l: l.settings.fast_start_beginning_of_game),
        LocationLogic(Locations.IslesClimbing, lambda _: True),
        LocationLogic(Locations.PreGiven_Location00, lambda _: True),
        LocationLogic(Locations.PreGiven_Location01, lambda _: True),
        LocationLogic(Locations.PreGiven_Location02, lambda _: True),
        LocationLogic(Locations.PreGiven_Location03, lambda _: True),
        LocationLogic(Locations.PreGiven_Location04, lambda _: True),
        LocationLogic(Locations.PreGiven_Location05, lambda _: True),
        LocationLogic(Locations.PreGiven_Location06, lambda _: True),
        LocationLogic(Locations.PreGiven_Location07, lambda _: True),
        LocationLogic(Locations.PreGiven_Location08, lambda _: True),
        LocationLogic(Locations.PreGiven_Location09, lambda _: True),
        LocationLogic(Locations.PreGiven_Location10, lambda _: True),
        LocationLogic(Locations.PreGiven_Location11, lambda _: True),
        LocationLogic(Locations.PreGiven_Location12, lambda _: True),
        LocationLogic(Locations.PreGiven_Location13, lambda _: True),
        LocationLogic(Locations.PreGiven_Location14, lambda _: True),
        LocationLogic(Locations.PreGiven_Location15, lambda _: True),
        LocationLogic(Locations.PreGiven_Location16, lambda _: True),
        LocationLogic(Locations.PreGiven_Location17, lambda _: True),
        LocationLogic(Locations.PreGiven_Location18, lambda _: True),
        LocationLogic(Locations.PreGiven_Location19, lambda _: True),
        LocationLogic(Locations.PreGiven_Location20, lambda _: True),
        LocationLogic(Locations.PreGiven_Location21, lambda _: True),
        LocationLogic(Locations.PreGiven_Location22, lambda _: True),
        LocationLogic(Locations.PreGiven_Location23, lambda _: True),
        LocationLogic(Locations.PreGiven_Location24, lambda _: True),
        LocationLogic(Locations.PreGiven_Location25, lambda _: True),
        LocationLogic(Locations.PreGiven_Location26, lambda _: True),
        LocationLogic(Locations.PreGiven_Location27, lambda _: True),
        LocationLogic(Locations.PreGiven_Location28, lambda _: True),
        LocationLogic(Locations.PreGiven_Location29, lambda _: True),
        LocationLogic(Locations.PreGiven_Location30, lambda _: True),
        LocationLogic(Locations.PreGiven_Location31, lambda _: True),
        LocationLogic(Locations.PreGiven_Location32, lambda _: True),
        LocationLogic(Locations.PreGiven_Location33, lambda _: True),
        LocationLogic(Locations.PreGiven_Location34, lambda _: True),
        LocationLogic(Locations.PreGiven_Location35, lambda _: True),
        LocationLogic(Locations.PreGiven_Location36, lambda _: True),
    ], [
        Event(Events.KLumsyTalkedTo, lambda l: l.settings.fast_start_beginning_of_game or l.settings.auto_keys),
        # Everything you can do in the prison is autocompleted with auto_keys - just copy-paste the logic from the Prison region events here
        Event(Events.JapesKeyTurnedIn, lambda l: l.settings.auto_keys and l.JapesKey and l.HasFillRequirementsForLevel(l.settings.level_order[2])),
        Event(Events.AztecKeyTurnedIn, lambda l: l.settings.auto_keys and l.AztecKey and l.HasFillRequirementsForLevel(l.settings.level_order[3])),
        Event(Events.FactoryKeyTurnedIn, lambda l: l.settings.auto_keys and l.FactoryKey),
        Event(Events.GalleonKeyTurnedIn, lambda l: l.settings.auto_keys and l.GalleonKey and l.HasFillRequirementsForLevel(l.settings.level_order[5])),
        Event(Events.ForestKeyTurnedIn, lambda l: l.settings.auto_keys and l.ForestKey and l.HasFillRequirementsForLevel(l.settings.level_order[6])),
        Event(Events.CavesKeyTurnedIn, lambda l: l.settings.auto_keys and l.CavesKey and l.HasFillRequirementsForLevel(l.settings.level_order[7])),
        Event(Events.CastleKeyTurnedIn, lambda l: l.settings.auto_keys and l.CastleKey and l.HasFillRequirementsForLevel(l.settings.level_order[7])),
        Event(Events.HelmKeyTurnedIn, lambda l: l.settings.auto_keys and l.HelmKey),
        Event(Events.Night, lambda l: l.settings.fungi_time_internal in (FungiTimeSetting.night, FungiTimeSetting.dusk, FungiTimeSetting.progressive)),
        Event(Events.Day, lambda l: l.settings.fungi_time_internal in (FungiTimeSetting.day, FungiTimeSetting.dusk, FungiTimeSetting.progressive)),
        Event(Events.AztecIceMelted, lambda l: l.checkBarrier(RemovedBarriersSelected.aztec_tiny_temple_ice)),
        Event(Events.TestingGateOpened, lambda l: l.checkBarrier(RemovedBarriersSelected.factory_testing_gate)),
        Event(Events.MainCoreActivated, lambda l: l.checkBarrier(RemovedBarriersSelected.factory_production_room)),
        Event(Events.LighthouseGateOpened, lambda l: l.checkBarrier(RemovedBarriersSelected.galleon_lighthouse_gate)),
        Event(Events.ShipyardGateOpened, lambda l: l.checkBarrier(RemovedBarriersSelected.galleon_shipyard_area_gate)),
        Event(Events.ActivatedLighthouse, lambda l: l.checkBarrier(RemovedBarriersSelected.galleon_seasick_ship)),
        Event(Events.ShipyardTreasureRoomOpened, lambda l: l.checkBarrier(RemovedBarriersSelected.galleon_treasure_room)),
        Event(Events.WormGatesOpened, lambda l: l.checkBarrier(RemovedBarriersSelected.forest_green_tunnel)),
        Event(Events.HollowTreeGateOpened, lambda l: l.checkBarrier(RemovedBarriersSelected.forest_yellow_tunnel)),
        Event(Events.DonkeyVerse, lambda l: l.coconut and l.strongKong),
        Event(Events.DiddyVerse, lambda l: l.jetpack and l.peanut and l.guitar),
        Event(Events.LankyVerse, lambda l: l.handstand and l.balloon and l.trombone),
        Event(Events.TinyVerse, lambda l: l.mini and l.twirl and l.climbing),
        Event(Events.ChunkyVerse, lambda l: l.barrels),
        Event(Events.FridgeVerse, lambda l: l.crankyAccess and l.peanut and l.pineapple and l.grape and l.oranges and l.coconut),
    ], [
        # These first 3 Transitions NEED to be in this order, due to Random Starting Location!
        TransitionFront(Regions.Credits, lambda _: True),
        # Replace these with the actual starting region if we choose to randomize it
        TransitionFront(Regions.IslesMain, lambda l: l.settings.fast_start_beginning_of_game),
        TransitionFront(Regions.Treehouse, lambda l: not l.settings.fast_start_beginning_of_game),
        # Medal regions
        TransitionFront(Regions.DKIslesMedals, lambda _: True),
        TransitionFront(Regions.JungleJapesMedals, lambda _: True),
        TransitionFront(Regions.AngryAztecMedals, lambda _: True),
        TransitionFront(Regions.FranticFactoryMedals, lambda _: True),
        TransitionFront(Regions.GloomyGalleonMedals, lambda _: True),
        TransitionFront(Regions.FungiForestMedals, lambda _: True),
        TransitionFront(Regions.CrystalCavesMedals, lambda _: True),
        TransitionFront(Regions.CreepyCastleMedals, lambda _: True),
    ]),

    Regions.DKIslesMedals: Region("DK Isles Medals", HintRegion.IslesCBs, Levels.DKIsles, False, None, [
        LocationLogic(Locations.IslesDonkeyMedal, lambda l: l.ColoredBananas[Levels.DKIsles][Kongs.donkey] >= l.settings.medal_cb_req_level[7]),
        LocationLogic(Locations.IslesDiddyMedal, lambda l: l.ColoredBananas[Levels.DKIsles][Kongs.diddy] >= l.settings.medal_cb_req_level[7]),
        LocationLogic(Locations.IslesLankyMedal, lambda l: l.ColoredBananas[Levels.DKIsles][Kongs.lanky] >= l.settings.medal_cb_req_level[7]),
        LocationLogic(Locations.IslesTinyMedal, lambda l: l.ColoredBananas[Levels.DKIsles][Kongs.tiny] >= l.settings.medal_cb_req_level[7]),
        LocationLogic(Locations.IslesChunkyMedal, lambda l: l.ColoredBananas[Levels.DKIsles][Kongs.chunky] >= l.settings.medal_cb_req_level[7]),
        LocationLogic(Locations.IslesDonkeyHalfMedal, lambda l: l.ColoredBananas[Levels.DKIsles][Kongs.donkey] >= max(1, int(l.settings.medal_cb_req_level[7] >> 1))),
        LocationLogic(Locations.IslesDiddyHalfMedal, lambda l: l.ColoredBananas[Levels.DKIsles][Kongs.diddy] >= max(1, int(l.settings.medal_cb_req_level[7] >> 1))),
        LocationLogic(Locations.IslesLankyHalfMedal, lambda l: l.ColoredBananas[Levels.DKIsles][Kongs.lanky] >= max(1, int(l.settings.medal_cb_req_level[7] >> 1))),
        LocationLogic(Locations.IslesTinyHalfMedal, lambda l: l.ColoredBananas[Levels.DKIsles][Kongs.tiny] >= max(1, int(l.settings.medal_cb_req_level[7] >> 1))),
        LocationLogic(Locations.IslesChunkyHalfMedal, lambda l: l.ColoredBananas[Levels.DKIsles][Kongs.chunky] >= max(1, int(l.settings.medal_cb_req_level[7] >> 1))),
    ], [], [], restart=-1),

    Regions.Credits: Region("Credits", HintRegion.Credits, Levels.DKIsles, False, None, [
        LocationLogic(Locations.BananaHoard, lambda l: l.WinConditionMet())
    ], [], []),

    Regions.Treehouse: Region("Treehouse", HintRegion.MainIsles, Levels.DKIsles, False, None, [], [], [
        TransitionFront(Regions.TrainingGrounds, lambda _: True, Transitions.IslesTreehouseToStart),
    ]),

    Regions.TrainingGrounds: Region("Training Grounds", HintRegion.MainIsles, Levels.DKIsles, False, None, [
        LocationLogic(Locations.IslesVinesTrainingBarrel, lambda l: Events.TrainingBarrelsSpawned in l.Events, MinigameType.TrainingBarrel, isAuxiliary=True),
        LocationLogic(Locations.IslesSwimTrainingBarrel, lambda l: Events.TrainingBarrelsSpawned in l.Events, MinigameType.TrainingBarrel, isAuxiliary=True),
        LocationLogic(Locations.IslesOrangesTrainingBarrel, lambda l: Events.TrainingBarrelsSpawned in l.Events, MinigameType.TrainingBarrel, isAuxiliary=True),
        LocationLogic(Locations.IslesBarrelsTrainingBarrel, lambda l: Events.TrainingBarrelsSpawned in l.Events, MinigameType.TrainingBarrel, isAuxiliary=True),
        LocationLogic(Locations.IslesFirstMove, lambda l: (l.allTrainingChecks and l.crankyAccess) or l.settings.fast_start_beginning_of_game, isAuxiliary=True),
        LocationLogic(Locations.RainbowCoin_Location13, lambda _: True),
        LocationLogic(Locations.RainbowCoin_Location14, lambda l: (l.can_use_vines or l.CanMoonkick()) and l.climbing),  # Banana Hoard patch
    ], [
        Event(Events.TrainingBarrelsSpawned, lambda l: l.crankyAccess or l.settings.fast_start_beginning_of_game),  # Requires Cranky to spawn the training barrels
    ], [
        TransitionFront(Regions.IslesMain, lambda l: l.Slam or l.settings.fast_start_beginning_of_game, Transitions.IslesStartToMain),
        TransitionFront(Regions.Treehouse, lambda l: l.climbing, Transitions.IslesStartToTreehouse),
        TransitionFront(Regions.CrankyIsles, lambda l: l.crankyAccess),
    ]),

    Regions.IslesMain: Region("Isles Main", HintRegion.MainIsles, Levels.DKIsles, True, None, [
        # Don't check for donkey for rock- If lobbies are closed and first B.Locker is not 0, this banana must be grabbable by
        # the starting kong, so for logic we assume any kong can grab it since that's practically true.
        LocationLogic(Locations.IslesDonkeyJapesRock, lambda l: (l.settings.open_lobbies or Events.KLumsyTalkedTo in l.Events)),
        LocationLogic(Locations.IslesChunkyCagedBanana, lambda l: (l.pineapple and l.chunky) or ((l.CanSTS() or l.CanPhase()) and (l.ischunky or l.settings.free_trade_items))),
        LocationLogic(Locations.IslesMainEnemy_PineappleCage0, lambda _: True),
        LocationLogic(Locations.IslesMainEnemy_FungiCannon0, lambda _: True),
        LocationLogic(Locations.IslesMainEnemy_JapesEntrance, lambda _: True),
        LocationLogic(Locations.IslesMainEnemy_FungiCannon1, lambda _: True),
        LocationLogic(Locations.IslesMainEnemy_PineappleCage1, lambda _: True),
        LocationLogic(Locations.KremKap_IslesMainEnemy_PineappleCage0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_IslesMainEnemy_FungiCannon0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_IslesMainEnemy_JapesEntrance, lambda l: l.camera),
        LocationLogic(Locations.KremKap_IslesMainEnemy_FungiCannon1, lambda l: l.camera),
        LocationLogic(Locations.KremKap_IslesMainEnemy_PineappleCage1, lambda l: l.camera),
    ], [
        Event(Events.IslesW1aTagged, lambda _: True),
        Event(Events.IslesW1bTagged, lambda _: True),
        Event(Events.IslesW2aTagged, lambda _: True),
        Event(Events.IslesW3aTagged, lambda _: True),
        Event(Events.IslesW3bTagged, lambda _: True),
        Event(Events.IslesW4aTagged, lambda _: True),
        Event(Events.IslesW5aTagged, lambda _: True),
    ], [
        TransitionFront(Regions.TrainingGrounds, lambda _: True, Transitions.IslesMainToStart),
        TransitionFront(Regions.OuterIsles, lambda _: True),
        TransitionFront(Regions.JungleJapesLobby, lambda l: l.settings.open_lobbies or Events.KLumsyTalkedTo in l.Events or l.CanPhase() or l.CanSTS(), Transitions.IslesMainToJapesLobby),
        TransitionFront(Regions.KremIsle, lambda _: True),
        TransitionFront(Regions.IslesHill, lambda l: l.climbing or l.assumeUpperIslesAccess),
        TransitionFront(Regions.CabinIsle, lambda l: l.settings.open_lobbies or Events.GalleonKeyTurnedIn in l.Events),
        TransitionFront(Regions.CreepyCastleLobby, lambda l: l.settings.open_lobbies or Events.ForestKeyTurnedIn in l.Events, Transitions.IslesMainToCastleLobby),
        TransitionFront(Regions.KremIsleTopLevel, lambda l: l.tbs),
        TransitionFront(Regions.KRool, lambda l: l.CanAccessKRool() or l.assumeKRoolAccess),
    ]),

    Regions.OuterIsles: Region("Outer Isles", HintRegion.OuterIsles, Levels.DKIsles, False, None, [
        LocationLogic(Locations.IslesTinyCagedBanana, lambda l: (l.feather and l.tiny) or ((l.CanPhase() or l.CanSTS()) and (l.istiny or l.settings.free_trade_items))),
        LocationLogic(Locations.IslesChunkyPoundtheX, lambda l: Events.IslesChunkyBarrelSpawn in l.Events and l.hunkyChunky and l.Slam and l.chunky),
        LocationLogic(Locations.IslesBananaFairyIsland, lambda l: l.camera),
    ], [
        Event(Events.IslesW5bTagged, lambda _: True),
    ], [
        TransitionFront(Regions.IslesMain, lambda _: True),
        TransitionFront(Regions.BananaFairyRoom, lambda l: (l.mini and l.istiny) or l.CanPhase() or l.CanSTS(), Transitions.IslesMainToFairy),
    ]),

    Regions.IslesHill: Region("Isles Hill", HintRegion.MainIsles, Levels.DKIsles, False, None, [
        LocationLogic(Locations.RainbowCoin_Location04, lambda _: True),
    ], [], [
        TransitionFront(Regions.IslesMain, lambda _: True),
        TransitionFront(Regions.IslesMainUpper, lambda l: l.can_use_vines or l.CanMoonkick() or l.assumeUpperIslesAccess),
        TransitionFront(Regions.IslesEar, lambda l: l.CanMoonkick()),
    ]),

    Regions.IslesMainUpper: Region("Isles Main Upper", HintRegion.MainIsles, Levels.DKIsles, False, None, [
        LocationLogic(Locations.IslesChunkyInstrumentPad, lambda l: l.triangle and l.chunky and l.barrels),
        LocationLogic(Locations.IslesMainEnemy_NearAztec, lambda _: True),
        LocationLogic(Locations.KremKap_IslesMainEnemy_NearAztec, lambda l: l.camera),
        LocationLogic(Locations.HoldableBoulderIslesNearAztec, lambda l: l.barrels and l.ischunky),
        LocationLogic(Locations.HoldableBoulderIslesNearCaves, lambda l: l.barrels and l.ischunky),
    ], [
        Event(Events.IslesDiddyBarrelSpawn, lambda l: l.chunky and l.hasMoveSwitchsanity(Switches.IslesSpawnRocketbarrel, False) and l.barrels),
        Event(Events.IslesW2bTagged, lambda _: True),
    ], [
        TransitionFront(Regions.IslesMain, lambda _: True),
        TransitionFront(Regions.IslesHill, lambda _: True),
        TransitionFront(Regions.AztecLobbyRoof, lambda l: l.CanMoonkick()),
        TransitionFront(Regions.AngryAztecLobby, lambda l: l.settings.open_lobbies or Events.JapesKeyTurnedIn in l.Events or l.CanPhase(), Transitions.IslesMainToAztecLobby),
        TransitionFront(Regions.IslesEar, lambda l: (l.settings.open_lobbies or Events.ForestKeyTurnedIn in l.Events) and ((l.istiny and l.twirl) or (l.isdonkey or l.ischunky or ((l.isdiddy or l.islanky) and l.monkey_maneuvers and not l.isKrushaAdjacent(l.kong))))),
    ]),

    Regions.IslesEar: Region("Isles Ear", HintRegion.MainIsles, Levels.DKIsles, False, None, [], [], [
        TransitionFront(Regions.CrystalCavesLobby, lambda _: True, Transitions.IslesMainToCavesLobby),
        TransitionFront(Regions.IslesHill, lambda _: True),
        TransitionFront(Regions.IslesMainUpper, lambda l: (l.istiny and l.twirl) or (l.isdonkey or l.ischunky or ((l.isdiddy or l.islanky) and l.monkey_maneuvers) and not l.isKrushaAdjacent(l.kong))),
    ]),

    Regions.Prison: Region("Prison", HintRegion.KremIsles, Levels.DKIsles, False, None, [
        LocationLogic(Locations.IslesLankyPrisonOrangsprint, lambda l: (l.sprint and l.islanky) or (l.CanPhase() and (l.islanky or l.settings.free_trade_items))),
        LocationLogic(Locations.RainbowCoin_Location12, lambda _: True),
    ], [
        # Changes should match GameStart region for auto_keys considerations
        Event(Events.KLumsyTalkedTo, lambda _: True),
        Event(Events.JapesKeyTurnedIn, lambda l: l.JapesKey and l.HasFillRequirementsForLevel(l.settings.level_order[2])),  # To be able to turn a key in, you must have the *fill moves* required to enter the next level
        Event(Events.AztecKeyTurnedIn, lambda l: l.AztecKey and l.HasFillRequirementsForLevel(l.settings.level_order[3])),  # Only the kongs and moves, not the GBs
        Event(Events.FactoryKeyTurnedIn, lambda l: l.FactoryKey),
        Event(Events.GalleonKeyTurnedIn, lambda l: l.GalleonKey and l.HasFillRequirementsForLevel(l.settings.level_order[5])),  # This helps prevent weird fill issues in simple level order
        Event(Events.ForestKeyTurnedIn, lambda l: l.ForestKey and l.HasFillRequirementsForLevel(l.settings.level_order[6])),  # For example, if a Kong were in lobby 7, this could wreak havoc on key placement
        Event(Events.CavesKeyTurnedIn, lambda l: l.CavesKey and l.HasFillRequirementsForLevel(l.settings.level_order[6])),
        Event(Events.CastleKeyTurnedIn, lambda l: l.CastleKey and l.HasFillRequirementsForLevel(l.settings.level_order[6])),
        Event(Events.HelmKeyTurnedIn, lambda l: l.HelmKey),
    ], [
        TransitionFront(Regions.KremIsle, lambda _: True, Transitions.IslesPrisonToMain),
    ]),

    Regions.BananaFairyRoom: Region("Banana Fairy Room", HintRegion.OuterIsles, Levels.DKIsles, False, None, [
        LocationLogic(Locations.CameraAndShockwave, lambda _: True),
        LocationLogic(Locations.KremKap_IslesNPC_BFIQueen, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.OuterIsles, lambda _: True, Transitions.IslesFairyToMain),
        TransitionFront(Regions.RarewareGBRoom, lambda l: l.CanGetRarewareGB()),
    ]),

    Regions.RarewareGBRoom: Region("Rareware GB Room", HintRegion.OuterIsles, Levels.DKIsles, False, None, [
        LocationLogic(Locations.RarewareBanana, lambda _: True),
    ], [], [
        TransitionFront(Regions.BananaFairyRoom, lambda _: True),
    ]),

    # All lobbies take you to themselves when you die
    Regions.JungleJapesLobby: Region("Jungle Japes Lobby", HintRegion.EarlyLobbies, Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesLankyInstrumentPad, lambda l: l.chunky and l.trombone and l.lanky and l.barrels),
        LocationLogic(Locations.JapesDonkeyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.JapesDiddyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.JapesLankyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.JapesTinyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.JapesChunkyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.JapesLobbyEnemy_Enemy0, lambda _: True),
        LocationLogic(Locations.JapesLobbyEnemy_Enemy1, lambda _: True),
        LocationLogic(Locations.KremKap_JapesLobbyEnemy_Enemy0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_JapesLobbyEnemy_Enemy1, lambda l: l.camera),
        LocationLogic(Locations.HoldableBoulderJapesLobby, lambda l: l.barrels and l.ischunky),
    ], [
        Event(Events.JapesLobbyAccessed, lambda _: True),
    ], [
        TransitionFront(Regions.IslesMain, lambda _: True, Transitions.IslesJapesLobbyToMain),
        TransitionFront(Regions.JungleJapesEntryHandler, lambda l: l.IsLevelEnterable(Levels.JungleJapes), Transitions.IslesToJapes),
    ]),

    Regions.AngryAztecLobby: Region("Angry Aztec Lobby", HintRegion.EarlyLobbies, Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesTinyAztecLobby, lambda l: (((l.charge and l.diddy and l.twirl) or l.settings.bonus_barrels == MinigameBarrels.skip) and l.istiny) or (l.settings.bonus_barrels == MinigameBarrels.skip and l.settings.free_trade_items), MinigameType.BonusBarrel),
        LocationLogic(Locations.AztecDonkeyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.AztecDiddyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.AztecLankyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.AztecTinyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.AztecChunkyDoor, lambda l: not l.settings.wrinkly_location_rando and (l.hasMoveSwitchsanity(Switches.IslesAztecLobbyFeather, False) or l.CanPhase()) and ((l.chunky and l.hunkyChunky) or l.settings.remove_wrinkly_puzzles)),
    ], [
        Event(Events.AztecLobbyAccessed, lambda _: True),
    ], [
        TransitionFront(Regions.IslesMainUpper, lambda _: True, Transitions.IslesAztecLobbyToMain),
        TransitionFront(Regions.AngryAztecEntryHandler, lambda l: l.IsLevelEnterable(Levels.AngryAztec), Transitions.IslesToAztec),
    ]),

    Regions.KremIsle: Region("Krem Isle Base", HintRegion.KremIsles, Levels.DKIsles, False, None, [
        LocationLogic(Locations.IslesLankyCagedBanana, lambda l: ((l.grape or l.CanPhaseswim() or l.CanPhase()) and l.lanky) or (l.CanPhase() and l.settings.free_trade_items)),
        LocationLogic(Locations.IslesMainEnemy_MonkeyportPad, lambda _: True),
        LocationLogic(Locations.KremKap_IslesMainEnemy_MonkeyportPad, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.IslesMain, lambda _: True),
        TransitionFront(Regions.Prison, lambda _: True, Transitions.IslesMainToPrison),
        TransitionFront(Regions.GloomyGalleonLobbyEntrance, lambda l: (l.settings.open_lobbies or Events.AztecKeyTurnedIn in l.Events or l.CanPhaseswim()) and (l.swim or l.assumeLevel4Entry), Transitions.IslesMainToGalleonLobby),
        TransitionFront(Regions.KremIsleBeyondLift, lambda l: l.settings.open_lobbies or Events.AztecKeyTurnedIn in l.Events or l.CanMoonkick() or l.tbs or l.CanMoontail()),
        TransitionFront(Regions.KremIsleTopLevel, lambda l: l.hasMoveSwitchsanity(Switches.IslesMonkeyport, not l.assumeLevel8Entry)),
        # This transition is to make the MP pad not on the path to everything in level 8 - the key requirement is covered in the KremIsleMouth region
        TransitionFront(Regions.KremIsleMouth, lambda l: l.assumeLevel8Entry),
    ]),

    Regions.KremIsleBeyondLift: Region("Krem Isle Beyond Lift", HintRegion.KremIsles, Levels.DKIsles, False, None, [
        LocationLogic(Locations.IslesDonkeyCagedBanana, lambda l: (l.coconut and l.isdonkey)),
        LocationLogic(Locations.IslesMainEnemy_UpperFactoryPath, lambda _: True),
        LocationLogic(Locations.IslesMainEnemy_LowerFactoryPath0, lambda _: True),
        LocationLogic(Locations.IslesMainEnemy_LowerFactoryPath1, lambda _: True),
        LocationLogic(Locations.KremKap_IslesMainEnemy_UpperFactoryPath, lambda l: l.camera),
        LocationLogic(Locations.KremKap_IslesMainEnemy_LowerFactoryPath0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_IslesMainEnemy_LowerFactoryPath1, lambda l: l.camera),
    ], [
        Event(Events.IslesW4bTagged, lambda _: True),
    ], [
        TransitionFront(Regions.KremIsle, lambda _: True),
        TransitionFront(Regions.IslesSnideRoom, lambda _: True, Transitions.IslesMainToSnideRoom),
        TransitionFront(Regions.FranticFactoryLobby, lambda l: l.settings.open_lobbies or Events.AztecKeyTurnedIn in l.Events, Transitions.IslesMainToFactoryLobby),
    ]),

    Regions.KremIsleTopLevel: Region("Krem Isle Top Level", HintRegion.KremIsles, Levels.DKIsles, False, None, [
        LocationLogic(Locations.IslesTinyInstrumentPad, lambda l: Events.IslesChunkyBarrelSpawn in l.Events and l.istiny),
        LocationLogic(Locations.IslesBananaFairyCrocodisleIsle, lambda l: l.camera),
    ], [
        Event(Events.IslesChunkyBarrelSpawn, lambda l: l.saxophone and l.istiny),
    ], [
        TransitionFront(Regions.HideoutHelmLobby, lambda l: (l.generalclips and l.twirl) or l.tbs, Transitions.IslesMainToHelmLobby, isGlitchTransition=True),
        TransitionFront(Regions.KremIsleMouth, lambda l: l.settings.open_lobbies or (Events.CavesKeyTurnedIn in l.Events and Events.CastleKeyTurnedIn in l.Events)),
        TransitionFront(Regions.KremIsleBeyondLift, lambda _: True),
    ]),

    Regions.KremIsleMouth: Region("Krem Isle Mouth", HintRegion.KremIsles, Levels.DKIsles, False, None, [], [], [
        # You fall through the mouth if the lobby hasn't been opened (if you used a glitch to get in or LZR)
        TransitionFront(Regions.HideoutHelmLobby, lambda l: l.settings.open_lobbies or (Events.CavesKeyTurnedIn in l.Events and Events.CastleKeyTurnedIn in l.Events), Transitions.IslesMainToHelmLobby),
        # These next two transitions are only necessary in LZR, so the assumption of level entry necessary for level 8 (that is never applied in LZR) is safe here
        TransitionFront(Regions.KremIsleTopLevel, lambda l: not l.assumeLevel8Entry and (l.settings.open_lobbies or (Events.CavesKeyTurnedIn in l.Events and Events.CastleKeyTurnedIn in l.Events))),
        # This fall could be a logical point of progression, but you have to survive the drop OR have the keys and crouch drop there - the Open Lobbies check effectively prevents keys from being on the path for this transition in very rare worlds
        TransitionFront(Regions.KremIsleBeyondLift, lambda l: l.CanSurviveFallDamage() or l.settings.open_lobbies or (Events.CavesKeyTurnedIn in l.Events and Events.CastleKeyTurnedIn in l.Events)),
        # If you were to die to fall damage here, you'd be sent to the Isles spawn. This is effectively a one-off deathwarp consideration (but only if dying isn't catastrophic!)
        TransitionFront(Regions.IslesMain, lambda l: not l.settings.perma_death and not l.settings.wipe_file_on_death),
    ]),

    Regions.IslesSnideRoom: Region("Isles Snide Room", HintRegion.KremIsles, Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesDiddySnidesLobby, lambda l: ((l.settings.bonus_barrels == MinigameBarrels.skip or l.spring) and l.isdiddy) or (l.settings.bonus_barrels == MinigameBarrels.skip and l.settings.free_trade_items), MinigameType.BonusBarrel),
        LocationLogic(Locations.IslesBattleArena1, lambda l: not l.settings.crown_placement_rando and l.chunky and l.barrels),
    ], [], [
        TransitionFront(Regions.KremIsleBeyondLift, lambda _: True, Transitions.IslesSnideRoomToMain),
        TransitionFront(Regions.Snide, lambda l: l.snideAccess),
    ]),

    Regions.FranticFactoryLobby: Region("Frantic Factory Lobby", HintRegion.EarlyLobbies, Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesDonkeyInstrumentPad, lambda l: (l.grab or l.CanMoonkick()) and l.bongos and l.donkey),
        LocationLogic(Locations.IslesKasplatFactoryLobby, lambda l: not l.settings.kasplat_rando and l.punch and l.chunky),
        LocationLogic(Locations.IslesBananaFairyFactoryLobby, lambda l: l.camera and l.punch and l.chunky),
        LocationLogic(Locations.FactoryDonkeyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.FactoryDiddyDoor, lambda l: not l.settings.wrinkly_location_rando and ((l.grab and l.donkey) or l.CanMoonkick() or (l.monkey_maneuvers and (l.istiny or l.isdiddy)))),
        LocationLogic(Locations.FactoryLankyDoor, lambda l: not l.settings.wrinkly_location_rando and ((l.grab and l.donkey) or l.CanMoonkick() or l.monkey_maneuvers)),
        LocationLogic(Locations.FactoryTinyDoor, lambda l: not l.settings.wrinkly_location_rando and ((l.grab and l.donkey) or l.CanMoonkick() or (l.monkey_maneuvers and (l.istiny or l.isdiddy)))),
        LocationLogic(Locations.FactoryChunkyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.FactoryLobbyEnemy_Enemy0, lambda _: True),
        LocationLogic(Locations.KremKap_FactoryLobbyEnemy_Enemy0, lambda l: l.camera),
    ], [
        Event(Events.FactoryLobbyAccessed, lambda _: True),
    ], [
        TransitionFront(Regions.KremIsleBeyondLift, lambda _: True, Transitions.IslesFactoryLobbyToMain),
        TransitionFront(Regions.FranticFactoryEntryHandler, lambda l: l.IsLevelEnterable(Levels.FranticFactory), Transitions.IslesToFactory),
    ]),

    Regions.GloomyGalleonLobbyEntrance: Region("Gloomy Galleon Lobby Entrance", HintRegion.EarlyLobbies, Levels.DKIsles, False, None, [], [], [
        TransitionFront(Regions.KremIsle, lambda _: True, Transitions.IslesGalleonLobbyToMain),
        TransitionFront(Regions.GloomyGalleonLobby, lambda _: True),
    ]),

    Regions.GloomyGalleonLobby: Region("Gloomy Galleon Lobby", HintRegion.EarlyLobbies, Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesTinyGalleonLobby, lambda l: ((l.chunky and l.CanSlamSwitch(Levels.GloomyGalleon, 2) and l.mini and l.twirl and l.swim and l.tiny) or (l.CanPhaseswim() and (l.istiny or l.settings.free_trade_items))) and (not l.IsLavaWater() or l.Melons >= 3)),
        LocationLogic(Locations.IslesKasplatGalleonLobby, lambda l: not l.settings.kasplat_rando),
        LocationLogic(Locations.GalleonDonkeyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.GalleonDiddyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.GalleonLankyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.GalleonTinyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.GalleonChunkyDoor, lambda l: not l.settings.wrinkly_location_rando),
    ], [
        Event(Events.GalleonLobbyAccessed, lambda _: True),
    ], [
        TransitionFront(Regions.GloomyGalleonLobbyEntrance, lambda l: l.swim),
        TransitionFront(Regions.GloomyGalleonEntryHandler, lambda l: l.IsLevelEnterable(Levels.GloomyGalleon), Transitions.IslesToGalleon),
    ]),

    Regions.CabinIsle: Region("Cabin Isle", HintRegion.OuterIsles, Levels.DKIsles, False, None, [
        LocationLogic(Locations.RainbowCoin_Location03, lambda _: True),
    ], [], [
        TransitionFront(Regions.IslesMain, lambda _: True),
        TransitionFront(Regions.IslesMainUpper, lambda l: l.twirl and l.istiny and l.monkey_maneuvers),
        TransitionFront(Regions.IslesAboveWaterfall, lambda l: l.monkey_maneuvers and (((l.isdiddy or l.isdonkey or l.ischunky) and not l.isKrushaAdjacent(l.kong)) or (l.istiny and l.twirl))),
        TransitionFront(Regions.IslesAirspace, lambda l: Events.IslesDiddyBarrelSpawn in l.Events and l.jetpack and l.isdiddy),
        TransitionFront(Regions.FungiForestLobby, lambda _: True, Transitions.IslesMainToForestLobby),
    ]),

    Regions.IslesAboveWaterfall: Region("Isles Above Waterfall", HintRegion.MainIsles, Levels.DKIsles, False, None, [
        LocationLogic(Locations.IslesDiddyCagedBanana, lambda l: l.peanut and l.isdiddy),
    ], [], [
        TransitionFront(Regions.IslesMain, lambda _: True),
        TransitionFront(Regions.IslesMainUpper, lambda l: l.monkey_maneuvers),
        TransitionFront(Regions.CabinIsle, lambda l: l.CanMoonkick() or (l.monkey_maneuvers and (((l.isdiddy or l.isdonkey or l.ischunky) and not l.isKrushaAdjacent(l.kong)) or (l.istiny and l.twirl)))),
        TransitionFront(Regions.AztecLobbyRoof, lambda l: l.monkey_maneuvers and l.istiny and l.twirl),
    ]),

    Regions.IslesAirspace: Region("Isles Airspace", HintRegion.MainIsles, Levels.DKIsles, False, None, [  # You are assumed to be on Rocketbarrel in this region
        LocationLogic(Locations.IslesDiddySummit, lambda _: True, MinigameType.BonusBarrel),
    ], [
        Event(Events.AirSpaceEntered, lambda _: True),
    ], [
        TransitionFront(Regions.IslesMain, lambda _: True),
        TransitionFront(Regions.IslesMainUpper, lambda _: True),
        TransitionFront(Regions.CabinIsle, lambda _: True),
        TransitionFront(Regions.AztecLobbyRoof, lambda _: True),
        TransitionFront(Regions.IslesAboveWaterfall, lambda _: True),
        TransitionFront(Regions.IslesEar, lambda l: (l.settings.open_lobbies or Events.ForestKeyTurnedIn in l.Events)),  # This is likely never relevant because it takes Chunky to spawn the Rocketbarrel
    ]),

    Regions.AztecLobbyRoof: Region("Aztec Lobby Roof", HintRegion.MainIsles, Levels.DKIsles, False, None, [
        LocationLogic(Locations.RainbowCoin_Location05, lambda _: True),
    ], [], [
        TransitionFront(Regions.IslesMainUpper, lambda _: True),
        TransitionFront(Regions.IslesAboveWaterfall, lambda l: l.CanMoonkick()),
    ]),

    Regions.FungiForestLobby: Region("Fungi Forest Lobby", HintRegion.EarlyLobbies, Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesBattleArena2, lambda l: not l.settings.crown_placement_rando and (l.CanOpenForestLobbyGoneDoor() and l.gorillaGone and l.ischunky)),
        LocationLogic(Locations.IslesBananaFairyForestLobby, lambda l: l.camera and l.hasMoveSwitchsanity(Switches.IslesFungiLobbyFeather, False)),
        LocationLogic(Locations.ForestDonkeyDoor, lambda l: not l.settings.wrinkly_location_rando),  # These might look strange
        LocationLogic(Locations.ForestDiddyDoor, lambda l: not l.settings.wrinkly_location_rando),  # But they're all covered
        LocationLogic(Locations.ForestLankyDoor, lambda l: not l.settings.wrinkly_location_rando),  # Check HintAccess() in Logic.py
        LocationLogic(Locations.ForestTinyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.ForestChunkyDoor, lambda l: not l.settings.wrinkly_location_rando),
    ], [
        Event(Events.ForestLobbyAccessed, lambda _: True),
    ], [
        TransitionFront(Regions.CabinIsle, lambda _: True, Transitions.IslesForestLobbyToMain),
        TransitionFront(Regions.FungiForestEntryHandler, lambda l: l.IsLevelEnterable(Levels.FungiForest), Transitions.IslesToForest),
    ]),

    Regions.CrystalCavesLobby: Region("Crystal Caves Lobby", HintRegion.LateLobbies, Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesDonkeyLavaBanana, lambda l: ((l.punch and l.chunky and l.strongKong) or l.CanPhase()) and l.donkey),
        LocationLogic(Locations.IslesDiddyInstrumentPad, lambda l: l.jetpack and l.guitar and l.diddy),
        LocationLogic(Locations.IslesKasplatCavesLobby, lambda l: not l.settings.kasplat_rando and ((l.punch and l.chunky) or l.CanPhase() or l.ledgeclip)),
        LocationLogic(Locations.CavesDonkeyDoor, lambda l: not l.settings.wrinkly_location_rando and ((l.punch and l.chunky and l.barrels) or l.settings.remove_wrinkly_puzzles)),
        LocationLogic(Locations.CavesDiddyDoor, lambda l: not l.settings.wrinkly_location_rando and ((l.punch and l.chunky and l.barrels) or l.settings.remove_wrinkly_puzzles) and ((l.isdiddy and l.jetpack) or l.CanMoonkick())),
        LocationLogic(Locations.CavesLankyDoor, lambda l: not l.settings.wrinkly_location_rando and ((l.punch and l.chunky and l.barrels) or l.settings.remove_wrinkly_puzzles)),
        LocationLogic(Locations.CavesTinyDoor, lambda l: not l.settings.wrinkly_location_rando and ((l.punch and l.chunky and l.barrels) or l.settings.remove_wrinkly_puzzles)),
        LocationLogic(Locations.CavesChunkyDoor, lambda l: not l.settings.wrinkly_location_rando and ((l.punch and l.chunky and l.barrels) or l.settings.remove_wrinkly_puzzles)),
        LocationLogic(Locations.HoldableBoulderCavesLobby, lambda l: l.barrels and l.chunky and (l.punch or l.CanPhase())),
    ], [
        Event(Events.CavesLobbyAccessed, lambda _: True),
    ], [
        TransitionFront(Regions.IslesEar, lambda _: True, Transitions.IslesCavesLobbyToMain),
        TransitionFront(Regions.CrystalCavesEntryHandler, lambda l: l.IsLevelEnterable(Levels.CrystalCaves), Transitions.IslesToCaves),
    ]),

    Regions.CreepyCastleLobby: Region("Creepy Castle Lobby", HintRegion.LateLobbies, Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesLankyCastleLobby, lambda l: (l.chunky and l.balloon and l.islanky and l.barrels) or ((l.CanMoonkick() or (l.monkey_maneuvers and l.istiny and l.twirl and (not l.isKrushaAdjacent(Kongs.tiny)))) and l.settings.free_trade_items), MinigameType.BonusBarrel),
        LocationLogic(Locations.IslesKasplatCastleLobby, lambda l: not l.settings.kasplat_rando and ((l.coconut and l.donkey) or l.CanPhase())),
        LocationLogic(Locations.CastleDonkeyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.CastleDiddyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.CastleLankyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.CastleTinyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.CastleChunkyDoor, lambda l: not l.settings.wrinkly_location_rando),
        LocationLogic(Locations.RainbowCoin_Location15, lambda l: (l.chunky and l.balloon and l.islanky and l.barrels) or l.CanMoonkick() or (l.monkey_maneuvers and l.istiny and l.twirl and (not l.isKrushaAdjacent(Kongs.tiny)))),
        LocationLogic(Locations.CastleLobbyEnemy_Left, lambda _: True),
        LocationLogic(Locations.CastleLobbyEnemy_FarRight, lambda _: True),
        LocationLogic(Locations.CastleLobbyEnemy_NearRight, lambda _: True),
        LocationLogic(Locations.KremKap_CastleLobbyEnemy_Left, lambda l: l.camera),
        LocationLogic(Locations.KremKap_CastleLobbyEnemy_FarRight, lambda l: l.camera),
        LocationLogic(Locations.KremKap_CastleLobbyEnemy_NearRight, lambda l: l.camera),
        LocationLogic(Locations.HoldableBoulderCastleLobby, lambda l: l.barrels and l.ischunky),
    ], [
        Event(Events.CastleLobbyAccessed, lambda _: True),
    ], [
        TransitionFront(Regions.IslesMain, lambda _: True, Transitions.IslesCastleLobbyToMain),
        TransitionFront(Regions.CreepyCastleEntryHandler, lambda l: l.IsLevelEnterable(Levels.CreepyCastle), Transitions.IslesToCastle),
    ]),

    Regions.HideoutHelmLobby: Region("Hideout Helm Lobby", HintRegion.LateLobbies, Levels.DKIsles, True, None, [
        LocationLogic(Locations.IslesChunkyHelmLobby, lambda l: (l.hasMoveSwitchsanity(Switches.IslesHelmLobbyGone, False) and l.ischunky and l.can_use_vines) or (l.settings.bonus_barrels == MinigameBarrels.skip and l.monkey_maneuvers and l.istiny and l.twirl and l.settings.free_trade_items), MinigameType.BonusBarrel),
        LocationLogic(Locations.IslesKasplatHelmLobby, lambda l: not l.settings.kasplat_rando and ((l.scope and l.coconut) or (l.twirl and l.tiny and l.monkey_maneuvers))),
    ], [
        Event(Events.HelmLobbyAccessed, lambda _: True),
        Event(Events.HelmLobbyW1aTagged, lambda _: True),
        Event(Events.HelmLobbyTraversable, lambda l: ((l.hasMoveSwitchsanity(Switches.IslesHelmLobbyGone) and l.can_use_vines) or (l.CanMoonkick() and l.donkey))),
    ], [
        TransitionFront(Regions.KremIsleMouth, lambda _: True, Transitions.IslesHelmLobbyToMain),
        TransitionFront(Regions.HideoutHelmLobbyPastVines, lambda l: Events.HelmLobbyTraversable in l.Events or Events.HelmLobbyW1bTagged in l.Events),
    ]),

    Regions.HideoutHelmLobbyPastVines: Region("Hideout Helm Lobby Past Vines", HintRegion.LateLobbies, Levels.DKIsles, False, Regions.HideoutHelmLobby, [], [
        Event(Events.HelmLobbyW1bTagged, lambda _: True),
    ], [
        TransitionFront(Regions.HideoutHelmLobby, lambda l: Events.HelmLobbyW1aTagged in l.Events),
        TransitionFront(Regions.HideoutHelmEntry, lambda l: l.IsLevelEnterable(Levels.HideoutHelm), Transitions.IslesToHelm),
    ]),

    Regions.KRool: Region("K. Rool", HintRegion.KRool, Levels.DKIsles, True, None, [], [
        Event(Events.KRoolDonkey, lambda l: not l.settings.krool_donkey or ((l.blast or not l.settings.cannons_require_blast) and l.donkey and l.climbing)),
        Event(Events.KRoolDiddy, lambda l: not l.settings.krool_diddy or (l.jetpack and l.peanut and l.diddy)),
        Event(Events.KRoolLanky, lambda l: not l.settings.krool_lanky or l.CanBeatLankyPhase()),
        Event(Events.KRoolTiny, lambda l: not l.settings.krool_tiny or (l.mini and l.feather and l.tiny)),
        Event(Events.KRoolChunky, lambda l: not l.settings.krool_chunky or (l.CanSlamChunkyPhaseSwitch() and l.gorillaGone and l.hunkyChunky and l.punch and l.chunky)),
        Event(Events.KRoolDillo1, lambda l: not l.settings.krool_dillo1 or l.barrels),
        Event(Events.KRoolDog1, lambda l: not l.settings.krool_dog1 or l.barrels),
        Event(Events.KRoolJack, lambda l: not l.settings.krool_madjack or (l.Slam and l.twirl and l.tiny)),
        Event(Events.KRoolPufftoss, lambda l: not l.settings.krool_pufftoss or True),
        Event(Events.KRoolDog2, lambda l: not l.settings.krool_dog2 or (l.barrels and l.hunkyChunky and l.chunky)),
        Event(Events.KRoolDillo2, lambda l: not l.settings.krool_dillo2 or l.barrels),
        Event(Events.KRoolKKO, lambda l: not l.settings.krool_kutout or ((not l.IsLavaWater()) or l.Melons >= 3)),
        Event(Events.KRoolDefeated, lambda l: Events.KRoolDonkey in l.Events and Events.KRoolDiddy in l.Events and Events.KRoolLanky in l.Events and Events.KRoolTiny in l.Events and Events.KRoolChunky in l.Events and Events.KRoolDillo1 in l.Events and Events.KRoolDillo2 in l.Events and Events.KRoolDog1 in l.Events and Events.KRoolDog2 in l.Events and Events.KRoolJack in l.Events and Events.KRoolPufftoss in l.Events and Events.KRoolKKO in l.Events)
    ], []),
}
