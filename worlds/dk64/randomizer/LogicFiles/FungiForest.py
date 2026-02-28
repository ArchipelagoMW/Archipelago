# fmt: off
"""Logic file for Fungi Forest."""

from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Maps import Maps
from randomizer.Enums.MinigameType import MinigameType
from randomizer.Enums.Regions import Regions
from randomizer.Enums.HintRegion import HintRegion
from randomizer.Enums.Time import Time
from randomizer.Enums.Switches import Switches
from randomizer.Enums.Transitions import Transitions
from randomizer.LogicClasses import (Event, LocationLogic, Region,
                                     TransitionFront)
from randomizer.Enums.Settings import FungiTimeSetting, MinigameBarrels, RemovedBarriersSelected

LogicRegions = {
    Regions.FungiForestMedals: Region("Fungi Forest Medals", HintRegion.ForestCBs, Levels.FungiForest, False, None, [
        LocationLogic(Locations.ForestDonkeyMedal, lambda l: l.ColoredBananas[Levels.FungiForest][Kongs.donkey] >= l.settings.medal_cb_req_level[4]),
        LocationLogic(Locations.ForestDiddyMedal, lambda l: l.ColoredBananas[Levels.FungiForest][Kongs.diddy] >= l.settings.medal_cb_req_level[4]),
        LocationLogic(Locations.ForestLankyMedal, lambda l: l.ColoredBananas[Levels.FungiForest][Kongs.lanky] >= l.settings.medal_cb_req_level[4]),
        LocationLogic(Locations.ForestTinyMedal, lambda l: l.ColoredBananas[Levels.FungiForest][Kongs.tiny] >= l.settings.medal_cb_req_level[4]),
        LocationLogic(Locations.ForestChunkyMedal, lambda l: l.ColoredBananas[Levels.FungiForest][Kongs.chunky] >= l.settings.medal_cb_req_level[4]),
        LocationLogic(Locations.ForestDonkeyHalfMedal, lambda l: l.ColoredBananas[Levels.FungiForest][Kongs.donkey] >= max(1, int(l.settings.medal_cb_req_level[4] >> 1))),
        LocationLogic(Locations.ForestDiddyHalfMedal, lambda l: l.ColoredBananas[Levels.FungiForest][Kongs.diddy] >= max(1, int(l.settings.medal_cb_req_level[4] >> 1))),
        LocationLogic(Locations.ForestLankyHalfMedal, lambda l: l.ColoredBananas[Levels.FungiForest][Kongs.lanky] >= max(1, int(l.settings.medal_cb_req_level[4] >> 1))),
        LocationLogic(Locations.ForestTinyHalfMedal, lambda l: l.ColoredBananas[Levels.FungiForest][Kongs.tiny] >= max(1, int(l.settings.medal_cb_req_level[4] >> 1))),
        LocationLogic(Locations.ForestChunkyHalfMedal, lambda l: l.ColoredBananas[Levels.FungiForest][Kongs.chunky] >= max(1, int(l.settings.medal_cb_req_level[4] >> 1))),
    ], [], [], restart=-1),

    # This region serves to set up the entry for the level based on the DK Portal Location
    Regions.FungiForestEntryHandler: Region("Fungi Forest Entry Handler", HintRegion.Error, Levels.FungiForest, False, None, [], [
        Event(Events.ForestEntered, lambda _: True),
    ], [
        TransitionFront(Regions.FungiForestLobby, lambda _: True, Transitions.ForestToIsles),
        TransitionFront(Regions.FungiForestStart, lambda _: True),  # Don't move this away from index 1 (ShuffleDoors.py relies on this being index 1)
    ], restart=-1),

    Regions.FungiForestStart: Region("Fungi Forest Start", HintRegion.ForestCenterAndBeanstalk, Levels.FungiForest, True, None, [
        LocationLogic(Locations.ForestMainEnemy_NearAppleDropoff, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_NearDKPortal, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_NearWellTag, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_GreenTunnel, lambda l: l.checkBarrier(RemovedBarriersSelected.forest_green_tunnel) or (l.hasMoveSwitchsanity(Switches.FungiGreenFeather, False))),
        LocationLogic(Locations.KremKap_ForestMainEnemy_NearAppleDropoff, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestMainEnemy_NearDKPortal, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestMainEnemy_NearWellTag, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestMainEnemy_GreenTunnel, lambda l: l.camera and (l.checkBarrier(RemovedBarriersSelected.forest_green_tunnel) or (l.hasMoveSwitchsanity(Switches.FungiGreenFeather, False)))),
    ], [
        Event(Events.Night, lambda l: l.HasGun(Kongs.any) or l.adv_orange_usage or l.settings.fungi_time_internal in (FungiTimeSetting.night, FungiTimeSetting.dusk, FungiTimeSetting.progressive)),
        Event(Events.Day, lambda l: l.HasGun(Kongs.any) or l.adv_orange_usage or l.settings.fungi_time_internal in (FungiTimeSetting.day, FungiTimeSetting.dusk, FungiTimeSetting.progressive)),
        Event(Events.WormGatesOpened, lambda l: l.checkBarrier(RemovedBarriersSelected.forest_green_tunnel) or (l.hasMoveSwitchsanity(Switches.FungiGreenFeather, False) and l.hasMoveSwitchsanity(Switches.FungiGreenPineapple, False))),
        Event(Events.ForestW1aTagged, lambda _: True),
        Event(Events.ForestW2aTagged, lambda _: True),
        Event(Events.ForestW3aTagged, lambda _: True),
        Event(Events.ForestW4aTagged, lambda _: True),
    ], [
        TransitionFront(Regions.ForestMinecarts, lambda l: l.Slam and l.ischunky),
        TransitionFront(Regions.GiantMushroomArea, lambda _: True),
        TransitionFront(Regions.MillArea, lambda _: True),
        TransitionFront(Regions.WormArea, lambda l: Events.WormGatesOpened in l.Events or l.CanPhase() or l.CanPhaseswim()),
    ]),

    Regions.ForestMinecarts: Region("Forest Minecarts", HintRegion.ForestCenterAndBeanstalk, Levels.FungiForest, False, None, [
        LocationLogic(Locations.ForestChunkyMinecarts, lambda l: l.HasEnoughRaceCoins(Maps.ForestMinecarts, Kongs.chunky, not l.settings.free_trade_items)),
    ], [], [
        TransitionFront(Regions.FungiForestStart, lambda _: True),
    ], Transitions.ForestMainToCarts
    ),

    Regions.GiantMushroomArea: Region("Giant Mushroom Area", HintRegion.MushroomExterior, Levels.FungiForest, True, None, [
        LocationLogic(Locations.ForestDiddyTopofMushroom, lambda l: l.jetpack and l.isdiddy, MinigameType.BonusBarrel),
        LocationLogic(Locations.ForestLankyRabbitRace, lambda l: (l.CanOStandTBSNoclip() and l.spawn_snags), isAuxiliary=True),
        LocationLogic(Locations.ForestMainEnemy_YellowTunnel0, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_NearLowWarp5, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_NearPinkTunnelBounceTag, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_NearGMRocketbarrel, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_BetweenYellowTunnelAndRB, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_NearCranky, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_NearPinkTunnelGM, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_GMRearTag, lambda _: True),
        LocationLogic(Locations.KremKap_ForestMainEnemy_YellowTunnel0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestMainEnemy_NearLowWarp5, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestMainEnemy_NearPinkTunnelBounceTag, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestMainEnemy_NearGMRocketbarrel, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestMainEnemy_BetweenYellowTunnelAndRB, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestMainEnemy_NearCranky, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestMainEnemy_NearPinkTunnelGM, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestMainEnemy_GMRearTag, lambda l: l.camera),
    ], [
        Event(Events.HollowTreeGateOpened, lambda l: l.hasMoveSwitchsanity(Switches.FungiYellow, False)),
        Event(Events.ForestW3bTagged, lambda _: True),
        Event(Events.ForestW5bTagged, lambda _: True),
    ], [
        TransitionFront(Regions.FungiForestStart, lambda _: True),
        TransitionFront(Regions.MushroomLower, lambda _: True, Transitions.ForestMainToLowerMushroom),
        TransitionFront(Regions.MushroomLowerExterior, lambda l: (l.jetpack and l.isdiddy) or (l.monkey_maneuvers and l.twirl and l.istiny) or (l.climbing and (l.isdonkey or l.ischunky) and l.monkey_maneuvers)),
        TransitionFront(Regions.MushroomBlastLevelExterior, lambda l: l.jetpack and l.isdiddy),
        TransitionFront(Regions.MushroomUpperMidExterior, lambda l: l.jetpack and l.isdiddy),
        TransitionFront(Regions.MushroomUpperExterior, lambda l: l.jetpack and l.isdiddy),
        TransitionFront(Regions.MushroomNightExterior, lambda l: l.jetpack and l.isdiddy),
        TransitionFront(Regions.MushroomVeryTopExterior, lambda l: l.jetpack and l.isdiddy),
        TransitionFront(Regions.HollowTreeArea, lambda l: l.checkBarrier(RemovedBarriersSelected.forest_yellow_tunnel) or Events.HollowTreeGateOpened in l.Events or l.CanPhaseswim() or l.CanPhase() or l.CanOStandTBSNoclip() or l.CanSkew(True)),
        TransitionFront(Regions.Anthill, lambda l: l.CanSkew(True), Transitions.ForestTreeToAnthill, isGlitchTransition=True),
        TransitionFront(Regions.CrankyForest, lambda l: l.crankyAccess),
    ]),

    Regions.MushroomLower: Region("Mushroom Lower", HintRegion.MushroomInterior, Levels.FungiForest, True, None, [], [
        Event(Events.MushroomCannonsSpawned, lambda l: l.coconut and l.peanut and l.grape and l.feather and l.pineapple
              and l.donkey and l.diddy and l.lanky and l.tiny and l.chunky),
        Event(Events.DonkeyMushroomSwitch, lambda l: l.CanSlamSwitch(Levels.FungiForest, 2) and l.donkey)
    ], [
        TransitionFront(Regions.MushroomLowerBetweenLadders, lambda l: l.climbing),
        TransitionFront(Regions.GiantMushroomArea, lambda _: True, Transitions.ForestLowerMushroomToMain),
        TransitionFront(Regions.MushroomUpper, lambda l: Events.MushroomCannonsSpawned in l.Events),
    ]),

    Regions.MushroomLowerBetweenLadders: Region("Mushroom Lower Between Ladders", HintRegion.MushroomInterior, Levels.FungiForest, False, -1, [], [], [
        TransitionFront(Regions.MushroomLower, lambda _: True),
        TransitionFront(Regions.MushroomLowerMid, lambda l: l.climbing),
    ]),

    Regions.MushroomLowerMid: Region("Mushroom Lower Middle", HintRegion.MushroomInterior, Levels.FungiForest, False, -1, [
        LocationLogic(Locations.ForestTinyMushroomBarrel, lambda l: l.CanSlamSwitch(Levels.FungiForest, 2) and l.istiny and l.climbing, MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.MushroomLowerBetweenLadders, lambda _: True),
        TransitionFront(Regions.MushroomLowerExterior, lambda _: True, Transitions.ForestLowerMushroomToLowerExterior),
    ]),

    Regions.MushroomUpperMidExterior: Region("Mushroom Upper Mid Exterior", HintRegion.MushroomExterior, Levels.FungiForest, False, None, [], [], [
        TransitionFront(Regions.GiantMushroomArea, lambda _: True),
        TransitionFront(Regions.MushroomBlastLevelExterior, lambda _: True),
        TransitionFront(Regions.MushroomMiddle, lambda _: True, Transitions.ForestLowerExteriorToUpperMushroom),
    ]),

    Regions.MushroomBlastLevelExterior: Region("Mushroom Blast Level Exterior", HintRegion.MushroomExterior, Levels.FungiForest, True, None, [
        LocationLogic(Locations.ForestMainEnemy_NearBBlast, lambda _: True),
        LocationLogic(Locations.KremKap_ForestMainEnemy_NearBBlast, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.MushroomLowerExterior, lambda _: True),
        TransitionFront(Regions.MushroomUpperMidExterior, lambda l: l.climbing),
        TransitionFront(Regions.ForestBaboonBlast, lambda l: l.blast and l.isdonkey)  # , Transitions.ForestMainToBBlast)
    ]),

    Regions.MushroomLowerExterior: Region("Mushroom Lower Exterior", HintRegion.MushroomExterior, Levels.FungiForest, False, None, [
        LocationLogic(Locations.ForestKasplatLowerMushroomExterior, lambda l: not l.settings.kasplat_rando),
    ], [], [
        TransitionFront(Regions.GiantMushroomArea, lambda _: True),
        TransitionFront(Regions.MushroomBlastLevelExterior, lambda l: l.climbing),
        TransitionFront(Regions.MushroomLowerMid, lambda _: True, Transitions.ForestLowerExteriorToLowerMushroom),
    ]),

    Regions.ForestBaboonBlast: Region("Forest Baboon Blast", HintRegion.MushroomExterior, Levels.FungiForest, False, None, [
        LocationLogic(Locations.ForestDonkeyBaboonBlast, lambda l: l.isdonkey, MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.MushroomBlastLevelExterior, lambda _: True)
    ]),

    Regions.MushroomMiddle: Region("Mushroom Middle", HintRegion.MushroomInterior, Levels.FungiForest, False, -1, [
        LocationLogic(Locations.ForestKasplatInsideMushroom, lambda l: not l.settings.kasplat_rando),
    ], [], [
        TransitionFront(Regions.MushroomLowerMid, lambda _: True),
        TransitionFront(Regions.MushroomUpperMid, lambda l: l.climbing),
        TransitionFront(Regions.MushroomUpperMidExterior, lambda _: True, Transitions.ForestUpperMushroomToLowerExterior),
    ]),

    Regions.MushroomUpperMid: Region("Mushroom Upper Middle", HintRegion.MushroomInterior, Levels.FungiForest, False, -1, [
        LocationLogic(Locations.ForestGMEnemy_Path0, lambda _: True),
        LocationLogic(Locations.ForestGMEnemy_Path1, lambda _: True),
        LocationLogic(Locations.KremKap_ForestGMEnemy_Path0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestGMEnemy_Path1, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.MushroomMiddle, lambda _: True),
        TransitionFront(Regions.MushroomUpperVineFloor, lambda l: l.climbing),
        TransitionFront(Regions.MushroomNightDoor, lambda l: l.can_use_vines),
    ]),

    Regions.MushroomUpperVineFloor: Region("Mushroom Upper Vine Floor", HintRegion.MushroomInterior, Levels.FungiForest, False, -1, [
        LocationLogic(Locations.ForestGMEnemy_AboveNightDoor, lambda _: True),
        LocationLogic(Locations.KremKap_ForestGMEnemy_AboveNightDoor, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.MushroomUpper, lambda l: l.climbing),
        TransitionFront(Regions.MushroomUpperMid, lambda _: True),
    ]),

    Regions.MushroomUpper: Region("Mushroom Upper", HintRegion.MushroomInterior, Levels.FungiForest, True, -1, [
        LocationLogic(Locations.ForestDonkeyMushroomCannons, lambda l: Events.MushroomCannonsSpawned in l.Events and Events.DonkeyMushroomSwitch in l.Events),
    ], [], [
        TransitionFront(Regions.MushroomUpperVineFloor, lambda _: True),
        TransitionFront(Regions.MushroomUpperExterior, lambda _: True, Transitions.ForestUpperMushroomToUpperExterior),
    ]),

    # This region basically just exists to facilitate the two entrances into upper mushroom
    Regions.MushroomNightDoor: Region("Mushroom Night Door", HintRegion.MushroomInterior, Levels.FungiForest, False, None, [], [], [
        TransitionFront(Regions.MushroomUpperMid, lambda l: l.can_use_vines),
        TransitionFront(Regions.MushroomMiddle, lambda _: True),
        TransitionFront(Regions.MushroomNightExterior, lambda _: True, Transitions.ForestNightToExterior, time=Time.Night),
    ]),

    Regions.MushroomNightExterior: Region("Mushroom Night Exterior", HintRegion.MushroomExterior, Levels.FungiForest, False, None, [
        LocationLogic(Locations.ForestKasplatUpperMushroomExterior, lambda l: not l.settings.kasplat_rando),
    ], [], [
        TransitionFront(Regions.MushroomNightDoor, lambda _: True, Transitions.ForestExteriorToNight, time=Time.Night),
        TransitionFront(Regions.GiantMushroomArea, lambda _: True),
    ]),

    Regions.MushroomUpperExterior: Region("Mushroom Upper Exterior", HintRegion.MushroomExterior, Levels.FungiForest, True, -1, [
        LocationLogic(Locations.ForestBattleArena, lambda l: not l.settings.crown_placement_rando and (not l.IsHardFallDamage() or (l.istiny and l.twirl) or (l.isdiddy and l.jetpack) or Events.Night in l.Events)),
        LocationLogic(Locations.ForestMainEnemy_NearFacePuzzle, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_NearCrown, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_NearHighWarp5, lambda _: True),
        LocationLogic(Locations.KremKap_ForestMainEnemy_NearFacePuzzle, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestMainEnemy_NearCrown, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestMainEnemy_NearHighWarp5, lambda l: l.camera),
    ], [
        Event(Events.ForestW5aTagged, lambda _: True),
    ], [
        TransitionFront(Regions.MushroomUpper, lambda _: True, Transitions.ForestUpperExteriorToUpperMushroom),
        TransitionFront(Regions.MushroomNightExterior, lambda l: (l.istiny and l.twirl) or not l.IsHardFallDamage()),
        TransitionFront(Regions.GiantMushroomArea, lambda _: True),
        TransitionFront(Regions.MushroomVeryTopExterior, lambda l: (l.handstand and l.islanky) or (l.slope_resets and l.isdiddy)),
        TransitionFront(Regions.MushroomChunkyRoom, lambda l: (l.CanSlamSwitch(Levels.FungiForest, 2) and l.ischunky) or l.CanPhase() or l.CanOStandTBSNoclip(), Transitions.ForestExteriorToChunky),
        TransitionFront(Regions.MushroomLankyZingersRoom, lambda l: Events.LankyMushroomSlamSwitch in l.Events or l.CanOStandTBSNoclip(), Transitions.ForestExteriorToZingers),
        TransitionFront(Regions.MushroomLankyMushroomsRoom, lambda l: Events.LankyMushroomSlamSwitch in l.Events or l.CanPhase() or l.CanOStandTBSNoclip(), Transitions.ForestExteriorToMushrooms),
        TransitionFront(Regions.ForestBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.MushroomVeryTopExterior: Region("Very Top of Mushroom", HintRegion.MushroomExterior, Levels.FungiForest, False, -1, [
        LocationLogic(Locations.ForestMainEnemy_TopOfMushroom, lambda _: True),
        LocationLogic(Locations.KremKap_ForestMainEnemy_TopOfMushroom, lambda l: l.camera),

    ], [
        Event(Events.LankyMushroomSlamSwitch, lambda l: l.CanSlamSwitch(Levels.FungiForest, 2) and l.islanky)
    ], [
        TransitionFront(Regions.MushroomUpperExterior, lambda _: True),
    ]),

    Regions.MushroomChunkyRoom: Region("Mushroom Chunky Room", HintRegion.MushroomInterior, Levels.FungiForest, False, -1, [
        LocationLogic(Locations.ForestChunkyFacePuzzle, lambda l: l.pineapple and l.CanSlamSwitch(Levels.FungiForest, 2) and l.ischunky),
        LocationLogic(Locations.ForestFacePuzzleEnemy_Enemy, lambda _: True),
        LocationLogic(Locations.KremKap_ForestFacePuzzleEnemy_Enemy, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.MushroomUpperExterior, lambda _: True, Transitions.ForestChunkyToExterior),
    ]),

    Regions.MushroomLankyZingersRoom: Region("Mushroom Lanky Zingers Room", HintRegion.MushroomInterior, Levels.FungiForest, False, -1, [
        LocationLogic(Locations.ForestLankyZingers, lambda l: l.islanky or l.settings.free_trade_items),
        LocationLogic(Locations.ForestLeapEnemy_Enemy0, lambda _: True),
        LocationLogic(Locations.ForestLeapEnemy_Enemy1, lambda _: True),
        LocationLogic(Locations.KremKap_ForestLeapEnemy_Enemy0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestLeapEnemy_Enemy1, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.MushroomUpperExterior, lambda _: True, Transitions.ForestZingersToExterior),
    ]),

    Regions.MushroomLankyMushroomsRoom: Region("Mushroom Lanky Mushrooms Room", HintRegion.MushroomInterior, Levels.FungiForest, False, None, [
        LocationLogic(Locations.ForestLankyColoredMushrooms, lambda l: l.Slam and (l.islanky or l.settings.free_trade_items), MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.MushroomUpperExterior, lambda _: True, Transitions.ForestMushroomsToExterior),
    ]),

    Regions.HollowTreeArea: Region("Hollow Tree Area", HintRegion.OwlTree, Levels.FungiForest, True, -1, [
        LocationLogic(Locations.ForestDiddyOwlRace, lambda l: l.TimeAccess(Regions.HollowTreeArea, Time.Night) and l.jetpack and l.guitar and l.isdiddy, MinigameType.BonusBarrel),
        LocationLogic(Locations.ForestLankyRabbitRace, lambda l: l.TimeAccess(Regions.HollowTreeArea, Time.Day) and l.trombone and l.sprint and l.lanky),
        LocationLogic(Locations.ForestKasplatOwlTree, lambda l: not l.settings.kasplat_rando),
        LocationLogic(Locations.MelonCrate_Location08, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_YellowTunnel1, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_YellowTunnel2, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_YellowTunnel3, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_HollowTree0, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_HollowTree1, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_HollowTreeEntrance, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_TreeMelonCrate0, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_TreeMelonCrate1, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_TreeMelonCrate2, lambda _: True),
        LocationLogic(Locations.KremKap_ForestMainEnemy_YellowTunnel1, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestMainEnemy_YellowTunnel2, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestMainEnemy_YellowTunnel3, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestMainEnemy_HollowTree0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestMainEnemy_HollowTree1, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestMainEnemy_HollowTreeEntrance, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestMainEnemy_TreeMelonCrate0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestMainEnemy_TreeMelonCrate1, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestMainEnemy_TreeMelonCrate2, lambda l: l.camera),
    ], [
        Event(Events.ForestW4bTagged, lambda _: True),
    ], [
        TransitionFront(Regions.GiantMushroomArea, lambda l: Events.HollowTreeGateOpened in l.Events or l.CanPhase()),
        TransitionFront(Regions.Anthill, lambda l: l.mini and l.saxophone and l.istiny, Transitions.ForestTreeToAnthill),
        TransitionFront(Regions.ForestBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.Anthill: Region("Anthill", HintRegion.OwlTree, Levels.FungiForest, False, -1, [
        LocationLogic(Locations.ForestTinyAnthill, lambda l: (l.istiny or l.settings.free_trade_items) and (l.oranges or l.saxophone or (l.settings.free_trade_items and l.HasInstrument(Kongs.any)))),
        LocationLogic(Locations.ForestBean, lambda l: (l.istiny or l.settings.free_trade_items) and (l.oranges or l.saxophone or (l.settings.free_trade_items and l.HasInstrument(Kongs.any)))),
        LocationLogic(Locations.ForestAnthillEnemy_Gauntlet0, lambda _: True),
        LocationLogic(Locations.ForestAnthillEnemy_Gauntlet1, lambda _: True),
        LocationLogic(Locations.ForestAnthillEnemy_Gauntlet2, lambda _: True),
        LocationLogic(Locations.ForestAnthillEnemy_Gauntlet3, lambda _: True),
        LocationLogic(Locations.KremKap_ForestAnthillEnemy_Gauntlet0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestAnthillEnemy_Gauntlet1, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestAnthillEnemy_Gauntlet2, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestAnthillEnemy_Gauntlet3, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.HollowTreeArea, lambda l: (l.istiny or l.settings.free_trade_items) and (l.oranges or l.saxophone or (l.settings.free_trade_items and l.HasInstrument(Kongs.any))), Transitions.ForestAnthillToTree),
    ]),

    Regions.ForestMillTopOfNightCage: Region("Mill top of Night Cage", HintRegion.Mills, Levels.FungiForest, False, None, [], [], [
        TransitionFront(Regions.MillArea, lambda _: True),
    ]),

    Regions.ForestVeryTopOfMill: Region("Very top of the Mill", HintRegion.Mills, Levels.FungiForest, False, None, [], [], [
        TransitionFront(Regions.ForestTopOfMill, lambda _: True),
        TransitionFront(Regions.MillArea, lambda _: True),
        TransitionFront(Regions.WinchRoom, lambda l: (l.CanSlamSwitch(Levels.FungiForest, 2) and l.isdiddy) or (l.CanMoonkick()), Transitions.ForestMainToWinch, time=Time.Night),
    ]),

    Regions.ForestTopOfMill: Region("Top of the Mill", HintRegion.Mills, Levels.FungiForest, False, None, [], [], [
        TransitionFront(Regions.MillArea, lambda _: True),
        TransitionFront(Regions.MillAttic, lambda _: True, Transitions.ForestMainToAttic, time=Time.Night),
        TransitionFront(Regions.ForestMillTopOfNightCage, lambda _: True),
    ]),

    Regions.MillArea: Region("Mill Area", HintRegion.Mills, Levels.FungiForest, True, None, [
        LocationLogic(Locations.ForestDonkeyMill, lambda l: (l.TimeAccess(Regions.MillArea, Time.Night) or l.CanPhase() or l.CanPhaseswim() or l.ledgeclip) and Events.ConveyorActivated in l.Events and l.donkey),
        LocationLogic(Locations.ForestDiddyCagedBanana, lambda l: (l.TimeAccess(Regions.MillArea, Time.Night) and Events.WinchRaised in l.Events and l.guitar and l.diddy) or ((l.CanPhaseswim() or l.ledgeclip) and (l.isdiddy or l.settings.free_trade_items))),
        LocationLogic(Locations.RainbowCoin_Location07, lambda _: True),
        LocationLogic(Locations.MelonCrate_Location10, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_NearSnide, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_NearIsoCoin, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_NearDarkAttic, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_NearWellExit, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_NearBlueTunnel, lambda _: True),
        LocationLogic(Locations.KremKap_ForestMainEnemy_NearSnide, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestMainEnemy_NearIsoCoin, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestMainEnemy_NearDarkAttic, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestMainEnemy_NearWellExit, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestMainEnemy_NearBlueTunnel, lambda l: l.camera),
    ], [
        Event(Events.ForestW1bTagged, lambda _: True),
    ], [
        TransitionFront(Regions.FungiForestStart, lambda _: True),
        TransitionFront(Regions.MillChunkyTinyArea, lambda l: (l.punch and l.ischunky) or l.CanPhase() or l.CanPhaseswim() or l.ledgeclip, Transitions.ForestMainToChunkyMill, time=Time.Day),
        TransitionFront(Regions.MillChunkyTinyArea, lambda l: (Events.MillBoxBroken in l.Events and l.mini and l.istiny) or l.CanPhase() or l.CanPhaseswim() or l.ledgeclip, Transitions.ForestMainToTinyMill),
        TransitionFront(Regions.GrinderRoom, lambda _: True, Transitions.ForestMainToGrinder, time=Time.Day),
        TransitionFront(Regions.MillRafters, lambda l: (l.spring or l.CanMoontail()) and l.isdiddy, Transitions.ForestMainToRafters, time=Time.Night),
        TransitionFront(Regions.ThornvineArea, lambda _: True, time=Time.Night),
        TransitionFront(Regions.ThornvineArea, lambda l: l.CanPhaseswim()),
        TransitionFront(Regions.Snide, lambda l: l.snideAccess, time=Time.Day),
        TransitionFront(Regions.ForestBossLobby, lambda l: not l.settings.tns_location_rando, time=Time.Day),
        TransitionFront(Regions.ThornvineBarn, lambda l: l.CanPhaseswim(), Transitions.ForestMainToBarn, isGlitchTransition=True),
        TransitionFront(Regions.ForestVeryTopOfMill, lambda l: l.climbing),
        TransitionFront(Regions.ForestTopOfMill, lambda l: l.balloon and l.islanky),
        TransitionFront(Regions.ForestMillTopOfNightCage, lambda l: l.isdiddy or l.istiny or l.ischunky),
    ]),

    Regions.MillChunkyTinyArea: Region("Mill Back Room", HintRegion.Mills, Levels.FungiForest, False, -1, [
        LocationLogic(Locations.ForestMillRearEnemy_Enemy, lambda _: True),
        LocationLogic(Locations.KremKap_ForestMillRearEnemy_Enemy, lambda l: l.camera),
        LocationLogic(Locations.HoldableKegMillRear, lambda l: l.barrels and l.ischunky),
    ], [
        Event(Events.GrinderActivated, lambda l: l.punch and l.triangle and l.ischunky),
        Event(Events.MillBoxBroken, lambda l: l.punch and l.ischunky),
    ], [
        TransitionFront(Regions.MillArea, lambda _: True, Transitions.ForestChunkyMillToMain, time=Time.Day),
        TransitionFront(Regions.MillArea, lambda l: (Events.MillBoxBroken in l.Events and l.mini and l.istiny) or l.CanPhase() or l.ledgeclip, Transitions.ForestTinyMillToMain),
        TransitionFront(Regions.SpiderRoom, lambda _: True, Transitions.ForestTinyMillToSpider, time=Time.Night),
        TransitionFront(Regions.GrinderRoom, lambda l: (l.mini and l.istiny) or l.CanPhase() or l.ledgeclip, Transitions.ForestTinyMillToGrinder),
    ]),

    Regions.SpiderRoom: Region("Spider Room", HintRegion.Mills, Levels.FungiForest, False, Regions.MillChunkyTinyArea, [
        LocationLogic(Locations.ForestTinySpiderBoss, lambda l: l.HasGun(Kongs.tiny) or (l.settings.free_trade_items and l.HasGun(Kongs.any))),
    ], [], [
        TransitionFront(Regions.MillChunkyTinyArea, lambda _: True, Transitions.ForestSpiderToTinyMill),
    ]),

    Regions.GrinderRoom: Region("Grinder Room", HintRegion.Mills, Levels.FungiForest, True, -1, [
        LocationLogic(Locations.ForestChunkyKegs, lambda l: Events.GrinderActivated in l.Events and Events.ConveyorActivated in l.Events and l.chunky and l.barrels),
        LocationLogic(Locations.ForestMillFrontEnemy_Enemy, lambda _: True),
        LocationLogic(Locations.KremKap_ForestMillFrontEnemy_Enemy, lambda l: l.camera),
        LocationLogic(Locations.HoldableKegMillFrontFar, lambda l: l.barrels and l.ischunky),
        LocationLogic(Locations.HoldableKegMillFrontNear, lambda l: l.barrels and l.ischunky),
    ], [
        Event(Events.ConveyorActivated, lambda l: (l.CanSlamSwitch(Levels.FungiForest, 2) or l.CanPhase() or l.generalclips) and l.grab and l.donkey),
    ], [
        TransitionFront(Regions.MillArea, lambda _: True, Transitions.ForestGrinderToMain, time=Time.Day),
        TransitionFront(Regions.MillChunkyTinyArea, lambda l: (l.mini and l.istiny) or l.CanPhase() or l.generalclips, Transitions.ForestGrinderToTinyMill),
    ]),

    Regions.MillRafters: Region("Mill Rafters", HintRegion.Mills, Levels.FungiForest, False, None, [
        LocationLogic(Locations.ForestDiddyRafters, lambda l: l.guitar and l.isdiddy),
        LocationLogic(Locations.ForestBananaFairyRafters, lambda l: l.guitar and l.isdiddy and l.camera),
    ], [], [
        TransitionFront(Regions.MillArea, lambda _: True, Transitions.ForestRaftersToMain),
    ]),

    Regions.WinchRoom: Region("Winch Room", HintRegion.Mills, Levels.FungiForest, False, -1, [
        LocationLogic(Locations.ForestWinchEnemy_Enemy, lambda _: True),
        LocationLogic(Locations.KremKap_ForestWinchEnemy_Enemy, lambda l: l.camera),
    ], [
        Event(Events.WinchRaised, lambda l: l.peanut and l.charge and l.isdiddy),
    ], [
        TransitionFront(Regions.ForestVeryTopOfMill, lambda _: True, Transitions.ForestWinchToMain),
    ]),

    Regions.MillAttic: Region("Mill Attic", HintRegion.Mills, Levels.FungiForest, False, None, [
        LocationLogic(Locations.ForestLankyAttic, lambda l: l.CanSlamSwitch(Levels.FungiForest, 2) and (l.homing or l.hard_shooting) and l.grape and l.islanky),
    ], [], [
        TransitionFront(Regions.ForestTopOfMill, lambda _: True, Transitions.ForestAtticToMain),
    ]),

    Regions.ThornvineArea: Region("Thornvine Area", HintRegion.Mills, Levels.FungiForest, True, -1, [
        LocationLogic(Locations.ForestKasplatNearBarn, lambda l: not l.settings.kasplat_rando),
        LocationLogic(Locations.MelonCrate_Location09, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_Thornvine0, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_Thornvine1, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_Thornvine2, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_ThornvineEntrance, lambda _: True),
        LocationLogic(Locations.KremKap_ForestMainEnemy_Thornvine0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestMainEnemy_Thornvine1, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestMainEnemy_Thornvine2, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestMainEnemy_ThornvineEntrance, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.MillArea, lambda _: True, time=Time.Night),
        TransitionFront(Regions.ThornvineBarn, lambda l: (l.CanSlamSwitch(Levels.FungiForest, 2) and l.isdonkey and l.strongKong) or l.CanPhase(), Transitions.ForestMainToBarn),
        TransitionFront(Regions.ForestBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.ThornvineBarn: Region("Thornvine Barn", HintRegion.Mills, Levels.FungiForest, False, -1, [
        LocationLogic(Locations.ForestDonkeyBarn, lambda l: l.CanSlamSwitch(Levels.FungiForest, 1) and l.isdonkey and l.climbing and (l.can_use_vines or l.monkey_maneuvers or l.settings.bonus_barrels == MinigameBarrels.skip), MinigameType.BonusBarrel),  # Krusha can make it by jumping onto the beam first.
        LocationLogic(Locations.MelonCrate_Location11, lambda _: True),
        LocationLogic(Locations.ForestThornBarnEnemy_Enemy, lambda _: True),
        LocationLogic(Locations.KremKap_ForestThornBarnEnemy_Enemy, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.ThornvineArea, lambda _: True, Transitions.ForestBarnToMain),
        TransitionFront(Regions.ThornvineBarnAboveLadder, lambda l: l.climbing),
    ]),

    Regions.ThornvineBarnAboveLadder: Region("Thornvine Barn Above Ladder", HintRegion.Mills, Levels.FungiForest, False, None, [
        LocationLogic(Locations.ForestBananaFairyThornvines, lambda l: l.isdonkey and l.Slam and l.camera),
    ], [], [
        TransitionFront(Regions.ThornvineBarn, lambda _: True),
    ]),

    Regions.WormArea: Region("Worm Area", HintRegion.ForestCenterAndBeanstalk, Levels.FungiForest, True, -1, [
        LocationLogic(Locations.ForestTinyBeanstalk, lambda l: l.saxophone and l.mini and l.istiny and l.Beans >= 1),
        LocationLogic(Locations.ForestChunkyApple, lambda l: Events.WormGatesOpened in l.Events and l.hunkyChunky and l.ischunky and l.barrels),
        LocationLogic(Locations.RainbowCoin_Location08, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_NearBeanstalk0, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_NearBeanstalk1, lambda _: True),
        LocationLogic(Locations.KremKap_ForestMainEnemy_NearBeanstalk0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestMainEnemy_NearBeanstalk1, lambda l: l.camera),
        LocationLogic(Locations.ForestMainEnemy_AppleGauntlet0, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_AppleGauntlet1, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_AppleGauntlet2, lambda _: True),
        LocationLogic(Locations.ForestMainEnemy_AppleGauntlet3, lambda _: True),
        LocationLogic(Locations.KremKap_ForestMainEnemy_AppleGauntlet0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestMainEnemy_AppleGauntlet1, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestMainEnemy_AppleGauntlet2, lambda l: l.camera),
        LocationLogic(Locations.KremKap_ForestMainEnemy_AppleGauntlet3, lambda l: l.camera),
    ], [
        Event(Events.ForestW2bTagged, lambda _: True),
    ], [
        TransitionFront(Regions.FungiForestStart, lambda l: Events.WormGatesOpened in l.Events),
        TransitionFront(Regions.FunkyForest, lambda l: l.funkyAccess),
        TransitionFront(Regions.ForestBossLobby, lambda l: not l.settings.tns_location_rando, time=Time.Night),
    ]),

    Regions.ForestBossLobby: Region("Forest Boss Lobby", HintRegion.Bosses, Levels.FungiForest, True, None, [], [], [
        TransitionFront(Regions.ForestBoss, lambda l: l.IsBossReachable(Levels.FungiForest)),
    ]),

    Regions.ForestBoss: Region("Forest Boss", HintRegion.Bosses, Levels.FungiForest, False, None, [
        LocationLogic(Locations.ForestKey, lambda l: l.IsBossBeatable(Levels.FungiForest)),
    ], [], []),
}
