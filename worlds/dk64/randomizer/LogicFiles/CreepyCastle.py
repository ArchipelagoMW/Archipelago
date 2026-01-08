# fmt: off
"""Logic file for Creepy Castle."""

from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.MinigameType import MinigameType
from randomizer.Enums.Regions import Regions
from randomizer.Enums.HintRegion import HintRegion
from randomizer.Enums.Transitions import Transitions
from randomizer.Enums.Settings import RemovedBarriersSelected
from randomizer.LogicClasses import (Event, LocationLogic, Region,
                                     TransitionFront)

LogicRegions = {
    Regions.CreepyCastleMedals: Region("Creepy Castle Medals", HintRegion.CastleCBs, Levels.CreepyCastle, False, None, [
        LocationLogic(Locations.CastleDonkeyMedal, lambda l: l.ColoredBananas[Levels.CreepyCastle][Kongs.donkey] >= l.settings.medal_cb_req),
        LocationLogic(Locations.CastleDiddyMedal, lambda l: l.ColoredBananas[Levels.CreepyCastle][Kongs.diddy] >= l.settings.medal_cb_req),
        LocationLogic(Locations.CastleLankyMedal, lambda l: l.ColoredBananas[Levels.CreepyCastle][Kongs.lanky] >= l.settings.medal_cb_req),
        LocationLogic(Locations.CastleTinyMedal, lambda l: l.ColoredBananas[Levels.CreepyCastle][Kongs.tiny] >= l.settings.medal_cb_req),
        LocationLogic(Locations.CastleChunkyMedal, lambda l: l.ColoredBananas[Levels.CreepyCastle][Kongs.chunky] >= l.settings.medal_cb_req),
    ], [], [], restart=-1),

    # This region serves to set up the entry for the level based on the DK Portal Location
    Regions.CreepyCastleEntryHandler: Region("Creepy Castle Entry Handler", HintRegion.Error, Levels.CreepyCastle, False, None, [], [
        Event(Events.CastleEntered, lambda l: True),
    ], [
        TransitionFront(Regions.CreepyCastleLobby, lambda l: True, Transitions.CastleToIsles),
        TransitionFront(Regions.CreepyCastleMain, lambda l: True),  # Don't move this away from index 1 (ShuffleDoors.py relies on this being index 1)
    ], restart=-1),

    Regions.CreepyCastleMain: Region("Creepy Castle Main", HintRegion.CastleSurroundings, Levels.CreepyCastle, True, None, [
        LocationLogic(Locations.CastleDiddyAboveCastle, lambda l: l.jetpack and l.isdiddy, MinigameType.BonusBarrel),
        LocationLogic(Locations.CastleKasplatHalfway, lambda l: not l.settings.kasplat_rando),
        LocationLogic(Locations.RainbowCoin_Location11, lambda l: True),
        LocationLogic(Locations.CastleMainEnemy_NearBridge0, lambda l: True),
        LocationLogic(Locations.CastleMainEnemy_NearBridge1, lambda l: True),
        LocationLogic(Locations.CastleMainEnemy_WoodenExtrusion0, lambda l: True),
        LocationLogic(Locations.CastleMainEnemy_WoodenExtrusion1, lambda l: True),
        LocationLogic(Locations.CastleMainEnemy_NearShed, lambda l: True),
        LocationLogic(Locations.CastleMainEnemy_NearLibrary, lambda l: True),
        LocationLogic(Locations.CastleMainEnemy_NearTower, lambda l: True),
        LocationLogic(Locations.CastleMainEnemy_MuseumSteps, lambda l: True),
        LocationLogic(Locations.CastleMainEnemy_PathToDungeon, lambda l: True),
        LocationLogic(Locations.CastleMainEnemy_NearHeadphones, lambda l: True),
    ], [
        Event(Events.CastleW1aTagged, lambda l: True),
        Event(Events.CastleW1bTagged, lambda l: True),
        Event(Events.CastleW2aTagged, lambda l: True),
        Event(Events.CastleW2bTagged, lambda l: True),
        Event(Events.CastleW3aTagged, lambda l: True),
        Event(Events.CastleW3bTagged, lambda l: True),
        Event(Events.CastleW4aTagged, lambda l: True),
        Event(Events.CastleW4bTagged, lambda l: True),
        Event(Events.CastleW5aTagged, lambda l: True),
        Event(Events.CastleW5bTagged, lambda l: True),
    ], [
        TransitionFront(Regions.CastleWaterfall, lambda l: True),
        TransitionFront(Regions.CastleTree, lambda l: (Events.CastleTreeOpened in l.Events) or l.CanPhase() or l.CanPhaseswim(), Transitions.CastleMainToTree),
        TransitionFront(Regions.CastleGraveyardPlatform, lambda l: True),
        TransitionFront(Regions.CastleVeryBottom, lambda l: True),
        TransitionFront(Regions.Library, lambda l: (l.CanSlamSwitch(Levels.CreepyCastle, 3) and l.isdonkey), Transitions.CastleMainToLibraryStart),
        # Special Case for back door - it's only open right when you leave
        # TransitionFront(Regions.LibraryPastBooks, lambda l: True, Transitions.CastleMainToLibraryEnd),
        TransitionFront(Regions.Ballroom, lambda l: (l.CanSlamSwitch(Levels.CreepyCastle, 3) and l.diddy) or l.CanPhase() or l.CanSkew(True), Transitions.CastleMainToBallroom),  # Stays open
        TransitionFront(Regions.Tower, lambda l: (l.CanSlamSwitch(Levels.CreepyCastle, 3) and l.islanky) or l.CanPhase() or l.CanSkew(True), Transitions.CastleMainToTower),
        TransitionFront(Regions.Greenhouse, lambda l: (l.CanSlamSwitch(Levels.CreepyCastle, 3) and l.islanky) or l.CanPhase() or l.ledgeclip or l.CanSkew(True), Transitions.CastleMainToGreenhouse),
        TransitionFront(Regions.TrashCan, lambda l: (l.mini and l.istiny) or l.CanPhase() or l.CanSkew(True), Transitions.CastleMainToTrash),
        TransitionFront(Regions.Shed, lambda l: (l.punch and l.ischunky) or l.CanPhase() or l.CanSkew(True), Transitions.CastleMainToShed),
        TransitionFront(Regions.Museum, lambda l: (l.CanSlamSwitch(Levels.CreepyCastle, 3) and l.ischunky) or l.CanPhase() or l.CanSkew(True), Transitions.CastleMainToMuseum),
        TransitionFront(Regions.UpperCave, lambda l: True, Transitions.CastleMainToUpper),
        TransitionFront(Regions.CrankyCastle, lambda l: l.crankyAccess),
        TransitionFront(Regions.Snide, lambda l: l.snideAccess),
        TransitionFront(Regions.CastleBossLobby, lambda l: not l.settings.tns_location_rando),
        TransitionFront(Regions.CastleBaboonBlast, lambda l: l.blast and l.isdonkey)  # , Transitions.CastleMainToBBlast)
    ]),

    Regions.CastleVeryBottom: Region("Creepy Castle Very Bottom", HintRegion.CastleSurroundings, Levels.CreepyCastle, False, None, [
        LocationLogic(Locations.CastleKasplatLowerLedge, lambda l: not l.settings.kasplat_rando),
        LocationLogic(Locations.CastleMainEnemy_NearLowCave, lambda l: True),
        LocationLogic(Locations.CastleMainEnemy_PathToLowKasplat, lambda l: True),
        LocationLogic(Locations.CastleMainEnemy_LowTnS, lambda l: True)
    ], [], [
        TransitionFront(Regions.LowerCave, lambda l: True, Transitions.CastleMainToLower),
        TransitionFront(Regions.CastleGraveyardPlatform, lambda l: l.climbing),
        TransitionFront(Regions.CreepyCastleMain, lambda l: l.climbing),
        TransitionFront(Regions.CastleBossLobby, lambda l: not l.settings.tns_location_rando)
    ]),

    Regions.CastleGraveyardPlatform: Region("Creepy Graveyard Platform", HintRegion.CastleSurroundings, Levels.CreepyCastle, False, None, [], [], [
        TransitionFront(Regions.CreepyCastleMain, lambda l: l.climbing),
        TransitionFront(Regions.CastleVeryBottom, lambda l: True)
    ]),

    Regions.CastleBaboonBlast: Region("Castle Baboon Blast", HintRegion.CastleSurroundings, Levels.CreepyCastle, False, None, [], [
        Event(Events.CastleTreeOpened, lambda l: l.isdonkey)
    ], [
        TransitionFront(Regions.CreepyCastleMain, lambda l: True)
    ]),

    # This region just exists to facilitate the multiple exits from the upper cave
    Regions.CastleWaterfall: Region("Castle Waterfall", HintRegion.CastleSurroundings, Levels.CreepyCastle, False, None, [], [], [
        TransitionFront(Regions.CreepyCastleMain, lambda l: True),
        TransitionFront(Regions.UpperCave, lambda l: True, Transitions.CastleWaterfallToUpper),
    ]),

    Regions.CastleTree: Region("Castle Tree", HintRegion.CastleSurroundings, Levels.CreepyCastle, False, -1, [  # Deathwarp as long as Main to CastleTreeDrain doesn't become a thing
        LocationLogic(Locations.CastleDonkeyTree, lambda l: ((l.scope and l.coconut) or l.generalclips or l.CanPhase()) and l.isdonkey),
        LocationLogic(Locations.CastleKasplatTree, lambda l: not l.settings.kasplat_rando and (l.coconut or l.CanPhase() or l.generalclips) and l.isdonkey),
        LocationLogic(Locations.CastleBananaFairyTree, lambda l: l.camera and l.swim and (((l.coconut or l.generalclips) and l.isdonkey) or l.CanPhase())),
        LocationLogic(Locations.CastleTreeEnemy_StartRoom0, lambda l: True),
        LocationLogic(Locations.CastleTreeEnemy_StartRoom1, lambda l: True),
    ], [], [
        TransitionFront(Regions.CreepyCastleMain, lambda l: True, Transitions.CastleTreeToMain),
        TransitionFront(Regions.CastleTreePastPunch, lambda l: (l.punch and l.ischunky) or l.CanPhase()),
        # This doesn't always require swim, but if you ever get the GB it does
        TransitionFront(Regions.CreepyCastleMain, lambda l: (((l.coconut and l.swim) or l.generalclips) and l.isdonkey) or l.CanPhase(), Transitions.CastleTreeDrainToMain),
    ]),

    Regions.CastleTreePastPunch: Region("Castle Tree Past Punch", HintRegion.CastleSurroundings, Levels.CreepyCastle, False, None, [
        LocationLogic(Locations.CastleChunkyTree, lambda l: (((l.scope or l.settings.hard_shooting) and l.pineapple and l.ischunky) or l.CanPhase()) and (l.ischunky or l.settings.free_trade_items), MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.CastleTree, lambda l: True),
    ]),

    Regions.Library: Region("Library", HintRegion.CastleRooms, Levels.CreepyCastle, False, -1, [
        LocationLogic(Locations.CastleLibraryEnemy_ForkLeft0, lambda l: True),
        LocationLogic(Locations.CastleLibraryEnemy_ForkLeft1, lambda l: True),
        LocationLogic(Locations.CastleLibraryEnemy_ForkCenter, lambda l: True),
        LocationLogic(Locations.CastleLibraryEnemy_ForkRight, lambda l: True),
    ], [], [
        TransitionFront(Regions.CreepyCastleMain, lambda l: True, Transitions.CastleLibraryStartToMain),
        TransitionFront(Regions.LibraryPastSlam, lambda l: (l.CanSlamSwitch(Levels.CreepyCastle, 3) and l.isdonkey) or l.CanPhase() or l.ledgeclip),
        TransitionFront(Regions.CreepyCastleMain, lambda l: l.CanPhase() or l.ledgeclip, Transitions.CastleLibraryEndToMain, isGlitchTransition=True),  # Glitch straight to the exit
    ]),

    Regions.LibraryPastSlam: Region("Library Middle", HintRegion.CastleRooms, Levels.CreepyCastle, False, -1, [], [], [
        TransitionFront(Regions.Library, lambda l: True),
        TransitionFront(Regions.LibraryPastBooks, lambda l: (l.isdonkey and l.strongKong) or l.CanPhase() or l.ledgeclip)
    ]),

    Regions.LibraryPastBooks: Region("Library Rear", HintRegion.CastleRooms, Levels.CreepyCastle, False, -1, [
        LocationLogic(Locations.CastleDonkeyLibrary, lambda l: l.isdonkey or l.settings.free_trade_items),
    ], [], [
        TransitionFront(Regions.LibraryPastSlam, lambda l: (l.isdonkey and l.strongKong) or l.CanPhase()),
        TransitionFront(Regions.CreepyCastleMain, lambda l: l.isdonkey and l.coconut, Transitions.CastleLibraryEndToMain),
    ]),

    Regions.Ballroom: Region("Ballroom", HintRegion.CastleRooms, Levels.CreepyCastle, False, -1, [
        LocationLogic(Locations.CastleDiddyBallroom, lambda l: l.jetpack and l.isdiddy, MinigameType.BonusBarrel),
        LocationLogic(Locations.CastleBallroomEnemy_Start, lambda l: True),
    ], [], [
        TransitionFront(Regions.CreepyCastleMain, lambda l: True, Transitions.CastleBallroomToMain),
        TransitionFront(Regions.MuseumBehindGlass, lambda l: l.monkeyport and l.istiny, Transitions.CastleBallroomToMuseum),
    ]),

    Regions.MuseumBehindGlass: Region("Museum Behind Glass", HintRegion.CastleRooms, Levels.CreepyCastle, False, None, [
        LocationLogic(Locations.CastleBananaFairyBallroom, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.Ballroom, lambda l: l.monkeyport and l.istiny, Transitions.CastleMuseumToBallroom),
        TransitionFront(Regions.CastleTinyRace, lambda l: (l.mini and l.istiny) or l.CanPhase(), Transitions.CastleMuseumToCarRace),
        TransitionFront(Regions.Museum, lambda l: l.CanPhase()),
    ]),

    Regions.CastleTinyRace: Region("Castle Tiny Race", HintRegion.CastleRooms, Levels.CreepyCastle, False, None, [
        LocationLogic(Locations.CastleTinyCarRace, lambda l: l.istiny or l.settings.free_trade_items),
    ], [], [
        TransitionFront(Regions.MuseumBehindGlass, lambda l: True, Transitions.CastleRaceToMuseum)
    ], Transitions.CastleMuseumToCarRace
    ),

    Regions.Tower: Region("Tower", HintRegion.CastleRooms, Levels.CreepyCastle, False, None, [
        LocationLogic(Locations.CastleLankyTower, lambda l: (l.scope or (l.settings.hard_shooting and l.homing)) and l.balloon and l.grape and l.islanky, MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.CreepyCastleMain, lambda l: True, Transitions.CastleTowerToMain),
    ]),

    Regions.Greenhouse: Region("Greenhouse", HintRegion.CastleSurroundings, Levels.CreepyCastle, False, None, [
        # Sprint is not actually required
        LocationLogic(Locations.CastleLankyGreenhouse, lambda l: l.islanky or l.settings.free_trade_items),
        LocationLogic(Locations.CastleBattleArena, lambda l: not l.settings.crown_placement_rando and (l.islanky or l.settings.free_trade_items)),
    ], [], [
        TransitionFront(Regions.CreepyCastleMain, lambda l: True, Transitions.CastleGreenhouseStartToMain),
        TransitionFront(Regions.CreepyCastleMain, lambda l: l.islanky or l.settings.free_trade_items, Transitions.CastleGreenhouseEndToMain),
    ]),

    Regions.TrashCan: Region("Trash Can", HintRegion.CastleSurroundings, Levels.CreepyCastle, False, None, [
        LocationLogic(Locations.CastleTinyTrashCan, lambda l: (l.istiny and (l.saxophone or (l.feather and (l.homing or l.settings.hard_shooting)))) or (l.settings.free_trade_items and (l.HasInstrument(Kongs.any) or (l.HasGun(Kongs.any) and (l.homing or l.settings.hard_shooting))))),
    ], [], [
        TransitionFront(Regions.CreepyCastleMain, lambda l: True, Transitions.CastleTrashToMain),
    ]),

    Regions.Shed: Region("Shed", HintRegion.CastleSurroundings, Levels.CreepyCastle, False, None, [
        LocationLogic(Locations.CastleChunkyShed, lambda l: (l.punch or l.CanPhase()) and ((l.gorillaGone and l.pineapple) or l.triangle) and l.ischunky),
    ], [], [
        TransitionFront(Regions.CreepyCastleMain, lambda l: True, Transitions.CastleShedToMain),
    ]),

    Regions.Museum: Region("Museum", HintRegion.CastleRooms, Levels.CreepyCastle, False, -1, [
        LocationLogic(Locations.CastleChunkyMuseum, lambda l: (l.punch and l.ischunky and l.barrels) or (l.CanPhase() and (l.ischunky or l.settings.free_trade_items))),
        LocationLogic(Locations.CastleMuseumEnemy_MainFloor0, lambda l: True),
        LocationLogic(Locations.CastleMuseumEnemy_MainFloor1, lambda l: True),
        LocationLogic(Locations.CastleMuseumEnemy_MainFloor2, lambda l: True),
        LocationLogic(Locations.CastleMuseumEnemy_MainFloor3, lambda l: True),
        LocationLogic(Locations.CastleMuseumEnemy_Start, lambda l: True),
    ], [], [
        TransitionFront(Regions.CreepyCastleMain, lambda l: True, Transitions.CastleMuseumToMain),
        TransitionFront(Regions.MuseumBehindGlass, lambda l: l.CanPhase()),
    ]),

    Regions.LowerCave: Region("Lower Cave", HintRegion.CastleUnderground, Levels.CreepyCastle, True, -1, [
        LocationLogic(Locations.CastleKasplatCrypt, lambda l: not l.settings.kasplat_rando),
        LocationLogic(Locations.MelonCrate_Location12, lambda l: True),
        LocationLogic(Locations.CastleLowCaveEnemy_NearCrypt, lambda l: True),
        LocationLogic(Locations.CastleLowCaveEnemy_StairRight, lambda l: True),
        LocationLogic(Locations.CastleLowCaveEnemy_StairLeft, lambda l: True),
        LocationLogic(Locations.CastleLowCaveEnemy_NearMausoleum, lambda l: True),
        LocationLogic(Locations.CastleLowCaveEnemy_NearFunky, lambda l: True),
        LocationLogic(Locations.CastleLowCaveEnemy_NearTag, lambda l: True),
    ], [], [
        TransitionFront(Regions.CastleVeryBottom, lambda l: True, Transitions.CastleLowerToMain),
        TransitionFront(Regions.Crypt, lambda l: (l.coconut and l.isdonkey) or (l.peanut and l.isdiddy) or (l.pineapple and l.ischunky) or l.CanPhase() or l.ledgeclip or l.checkBarrier(RemovedBarriersSelected.castle_crypt_doors), Transitions.CastleLowerToCrypt),
        TransitionFront(Regions.Mausoleum, lambda l: (l.grape and l.islanky) or (l.feather and l.istiny) or l.CanPhase() or l.checkBarrier(RemovedBarriersSelected.castle_crypt_doors), Transitions.CastleLowerToMausoleum),
        TransitionFront(Regions.FunkyCastle, lambda l: l.funkyAccess),
        TransitionFront(Regions.CastleBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.Crypt: Region("Crypt", HintRegion.CastleUnderground, Levels.CreepyCastle, False, -1, [
        LocationLogic(Locations.CastleCryptEnemy_Fork, lambda l: True),
        LocationLogic(Locations.CastleCryptEnemy_NearDiddy, lambda l: True),
        LocationLogic(Locations.CastleCryptEnemy_NearChunky, lambda l: True),
    ], [
        Event(Events.CryptW1aTagged, lambda l: True),
        Event(Events.CryptW1bTagged, lambda l: True),
        Event(Events.CryptW2aTagged, lambda l: True),
        Event(Events.CryptW2bTagged, lambda l: True),
        Event(Events.CryptW3aTagged, lambda l: True),
        Event(Events.CryptW3bTagged, lambda l: True),
    ], [
        TransitionFront(Regions.LowerCave, lambda l: True, Transitions.CastleCryptToLower),
        TransitionFront(Regions.CryptDonkeyRoom, lambda l: (l.coconut and l.isdonkey) or l.checkBarrier(RemovedBarriersSelected.castle_crypt_doors) or l.CanPhase() or l.generalclips),
        TransitionFront(Regions.CryptDiddyRoom, lambda l: (l.peanut and l.isdiddy) or l.checkBarrier(RemovedBarriersSelected.castle_crypt_doors) or l.CanPhase() or l.generalclips),
        TransitionFront(Regions.CryptChunkyRoom, lambda l: (l.pineapple and l.ischunky) or l.checkBarrier(RemovedBarriersSelected.castle_crypt_doors) or l.CanPhase() or l.generalclips),
    ]),

    Regions.CryptDonkeyRoom: Region("Crypt Donkey Room", HintRegion.CastleUnderground, Levels.CreepyCastle, False, None, [
        LocationLogic(Locations.CastleCryptEnemy_MinecartEntry, lambda l: True),
    ], [], [
        TransitionFront(Regions.Crypt, lambda l: True),
        TransitionFront(Regions.CastleMinecarts, lambda l: (l.grab and l.isdonkey) or l.generalclips or l.CanPhase(), Transitions.CastleCryptToCarts),
    ]),

    Regions.CryptDiddyRoom: Region("Crypt Diddy Room", HintRegion.CastleUnderground, Levels.CreepyCastle, False, None, [
        LocationLogic(Locations.CastleDiddyCrypt, lambda l: l.charge and l.isdiddy),
        LocationLogic(Locations.CastleCryptEnemy_DiddyCoffin0, lambda l: l.isdiddy and l.charge),
        LocationLogic(Locations.CastleCryptEnemy_DiddyCoffin1, lambda l: l.isdiddy and l.charge),
        LocationLogic(Locations.CastleCryptEnemy_DiddyCoffin2, lambda l: l.isdiddy and l.charge),
        LocationLogic(Locations.CastleCryptEnemy_DiddyCoffin3, lambda l: l.isdiddy and l.charge),
    ], [], [
        TransitionFront(Regions.Crypt, lambda l: True),
    ]),

    Regions.CryptChunkyRoom: Region("Crypt Chunky Room", HintRegion.CastleUnderground, Levels.CreepyCastle, False, None, [
        LocationLogic(Locations.CastleChunkyCrypt, lambda l: (l.punch and l.ischunky) or ((l.ischunky or l.settings.free_trade_items) and (l.CanPhase() or l.generalclips)), MinigameType.BonusBarrel),
        LocationLogic(Locations.CastleCryptEnemy_ChunkyCoffin0, lambda l: l.ischunky and l.Slam),
        LocationLogic(Locations.CastleCryptEnemy_ChunkyCoffin1, lambda l: l.ischunky and l.Slam),
        LocationLogic(Locations.CastleCryptEnemy_ChunkyCoffin2, lambda l: l.ischunky and l.Slam),
        LocationLogic(Locations.CastleCryptEnemy_ChunkyCoffin3, lambda l: l.ischunky and l.Slam),
    ], [], [
        TransitionFront(Regions.Crypt, lambda l: True),
    ]),

    Regions.CastleMinecarts: Region("Castle Minecarts", HintRegion.CastleUnderground, Levels.CreepyCastle, False, None, [
        LocationLogic(Locations.CastleDonkeyMinecarts, lambda l: l.isdonkey or l.settings.free_trade_items),
    ], [], [
        TransitionFront(Regions.Crypt, lambda l: True, Transitions.CastleCartsToCrypt),
    ], Transitions.CastleCryptToCarts
    ),

    Regions.Mausoleum: Region("Mausoleum", HintRegion.CastleUnderground, Levels.CreepyCastle, False, None, [
        LocationLogic(Locations.CastleLankyMausoleum, lambda l: (((l.grape and l.sprint) or l.generalclips or l.CanPhase()) and ((l.trombone and l.can_use_vines) or (l.advanced_platforming and l.sprint)) and l.islanky) or (l.settings.free_trade_items and l.CanPhase())),
        LocationLogic(Locations.CastleTinyMausoleum, lambda l: l.CanSlamSwitch(Levels.CreepyCastle, 3) and l.twirl and l.istiny),
        LocationLogic(Locations.CastleMausoleumEnemy_TinyPath, lambda l: True),
        LocationLogic(Locations.CastleMausoleumEnemy_LankyPath0, lambda l: True),
        LocationLogic(Locations.CastleMausoleumEnemy_LankyPath1, lambda l: True),
    ], [], [
        TransitionFront(Regions.LowerCave, lambda l: True, Transitions.CastleMausoleumToLower),
    ]),

    Regions.UpperCave: Region("Upper Cave", HintRegion.CastleUnderground, Levels.CreepyCastle, True, -1, [
        LocationLogic(Locations.CastleTinyOverChasm, lambda l: (l.twirl or l.CanPhase()) and l.istiny, MinigameType.BonusBarrel),
        LocationLogic(Locations.CastleKasplatNearCandy, lambda l: not l.settings.kasplat_rando),
        LocationLogic(Locations.CastleUpperCaveEnemy_NearDungeon, lambda l: True),
        LocationLogic(Locations.CastleUpperCaveEnemy_NearPit, lambda l: True),
        LocationLogic(Locations.CastleUpperCaveEnemy_NearEntrance, lambda l: True),
    ], [], [
        TransitionFront(Regions.CreepyCastleMain, lambda l: True, Transitions.CastleUpperToMain),
        TransitionFront(Regions.CastleWaterfall, lambda l: True, Transitions.CastleUpperToWaterfall),
        TransitionFront(Regions.Dungeon, lambda l: True, Transitions.CastleUpperToDungeon),
        TransitionFront(Regions.CandyCastle, lambda l: l.candyAccess),
        TransitionFront(Regions.CastleBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.Dungeon: Region("Dungeon", HintRegion.CastleUnderground, Levels.CreepyCastle, True, None, [
        LocationLogic(Locations.CastleDonkeyDungeon, lambda l: (l.CanSlamSwitch(Levels.CreepyCastle, 3) or (l.Slam and l.CanPhase())) and l.donkey),
        LocationLogic(Locations.CastleDiddyDungeon, lambda l: (l.CanPhase() and (l.isdiddy or l.settings.free_trade_items)) or (l.CanSlamSwitch(Levels.CreepyCastle, 3) and l.isdiddy and (l.can_use_vines and ((l.scope and l.peanut and l.diddy) or (l.CanMoontail()))))),

        LocationLogic(Locations.CastleLankyDungeon, lambda l: (l.CanSlamSwitch(Levels.CreepyCastle, 3) or l.CanPhase()) and l.trombone and l.balloon and l.islanky, MinigameType.BonusBarrel),
        LocationLogic(Locations.CastleDungeonEnemy_FaceRoom, lambda l: (l.CanSlamSwitch(Levels.CreepyCastle, 3) and l.isdonkey) or l.CanPhase()),
        LocationLogic(Locations.CastleDungeonEnemy_ChairRoom, lambda l: (l.CanSlamSwitch(Levels.CreepyCastle, 3) and l.isdiddy) or l.CanPhase()),
        LocationLogic(Locations.CastleDungeonEnemy_OutsideLankyRoom, lambda l: True),
    ], [], [
        TransitionFront(Regions.UpperCave, lambda l: True, Transitions.CastleDungeonToUpper),
    ]),

    Regions.CastleBossLobby: Region("Castle Boss Lobby", HintRegion.Bosses, Levels.CreepyCastle, True, None, [], [], [
        TransitionFront(Regions.CastleBoss, lambda l: l.IsBossReachable(Levels.CreepyCastle)),
    ]),

    Regions.CastleBoss: Region("Castle Boss", HintRegion.Bosses, Levels.CreepyCastle, False, None, [
        LocationLogic(Locations.CastleKey, lambda l: l.IsBossBeatable(Levels.CreepyCastle)),
    ], [], []),
}
