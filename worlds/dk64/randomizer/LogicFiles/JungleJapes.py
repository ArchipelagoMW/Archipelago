# fmt: off
"""Logic file for Jungle Japes."""

from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Maps import Maps
from randomizer.Enums.MinigameType import MinigameType
from randomizer.Enums.Regions import Regions
from randomizer.Enums.HintRegion import HintRegion
from randomizer.Enums.Settings import RemovedBarriersSelected
from randomizer.Enums.Switches import Switches
from randomizer.Enums.Transitions import Transitions
from randomizer.LogicClasses import (Event, LocationLogic, Region,
                                     TransitionFront)

LogicRegions = {
    Regions.JungleJapesMedals: Region("Jungle Japes Medals", HintRegion.JapesCBs, Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesDonkeyMedal, lambda l: l.ColoredBananas[Levels.JungleJapes][Kongs.donkey] >= l.settings.medal_cb_req_level[0]),
        LocationLogic(Locations.JapesDiddyMedal, lambda l: l.ColoredBananas[Levels.JungleJapes][Kongs.diddy] >= l.settings.medal_cb_req_level[0]),
        LocationLogic(Locations.JapesLankyMedal, lambda l: l.ColoredBananas[Levels.JungleJapes][Kongs.lanky] >= l.settings.medal_cb_req_level[0]),
        LocationLogic(Locations.JapesTinyMedal, lambda l: l.ColoredBananas[Levels.JungleJapes][Kongs.tiny] >= l.settings.medal_cb_req_level[0]),
        LocationLogic(Locations.JapesChunkyMedal, lambda l: l.ColoredBananas[Levels.JungleJapes][Kongs.chunky] >= l.settings.medal_cb_req_level[0]),
        LocationLogic(Locations.JapesDonkeyHalfMedal, lambda l: l.ColoredBananas[Levels.JungleJapes][Kongs.donkey] >= max(1, int(l.settings.medal_cb_req_level[0] >> 1))),
        LocationLogic(Locations.JapesDiddyHalfMedal, lambda l: l.ColoredBananas[Levels.JungleJapes][Kongs.diddy] >= max(1, int(l.settings.medal_cb_req_level[0] >> 1))),
        LocationLogic(Locations.JapesLankyHalfMedal, lambda l: l.ColoredBananas[Levels.JungleJapes][Kongs.lanky] >= max(1, int(l.settings.medal_cb_req_level[0] >> 1))),
        LocationLogic(Locations.JapesTinyHalfMedal, lambda l: l.ColoredBananas[Levels.JungleJapes][Kongs.tiny] >= max(1, int(l.settings.medal_cb_req_level[0] >> 1))),
        LocationLogic(Locations.JapesChunkyHalfMedal, lambda l: l.ColoredBananas[Levels.JungleJapes][Kongs.chunky] >= max(1, int(l.settings.medal_cb_req_level[0] >> 1))),
    ], [], [], restart=-1),

    # This region serves to set up the entry for the level based on the DK Portal Location
    Regions.JungleJapesEntryHandler: Region("Jungle Japes Entry Handler", HintRegion.Error, Levels.JungleJapes, False, None, [], [
        Event(Events.JapesEntered, lambda _: True),
    ], [
        TransitionFront(Regions.JungleJapesLobby, lambda _: True, Transitions.JapesToIsles),
        TransitionFront(Regions.JungleJapesStart, lambda _: True),  # Don't move this away from index 1 (ShuffleDoors.py relies on this being index 1)
    ], restart=-1),

    Regions.JungleJapesStart: Region("Jungle Japes Start", HintRegion.Lowlands, Levels.JungleJapes, True, None, [
        LocationLogic(Locations.JapesDonkeyCagedBanana, lambda l: ((Events.JapesDonkeySwitch in l.Events or l.CanPhaseswim() or l.CanSkew(True) or l.CanSkew(False)) and l.donkey) or ((l.CanPhaseswim() or l.CanSkew(True) or l.CanSkew(False)) and l.settings.free_trade_items)),
        LocationLogic(Locations.JapesChunkyBoulder, lambda l: l.chunky and l.barrels),
        LocationLogic(Locations.JapesMainEnemy_Start, lambda _: True),
        LocationLogic(Locations.JapesMainEnemy_Tunnel0, lambda _: True),
        LocationLogic(Locations.JapesMainEnemy_Tunnel1, lambda _: True),
        LocationLogic(Locations.JapesMainEnemy_KilledInDemo, lambda _: True),
        LocationLogic(Locations.JapesMainEnemy_NearUnderground, lambda _: True),
        LocationLogic(Locations.KremKap_JapesMainEnemy_Start, lambda l: l.camera),
        LocationLogic(Locations.KremKap_JapesMainEnemy_Tunnel0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_JapesMainEnemy_Tunnel1, lambda l: l.camera),
        LocationLogic(Locations.KremKap_JapesMainEnemy_KilledInDemo, lambda l: l.camera),
        LocationLogic(Locations.KremKap_JapesMainEnemy_NearUnderground, lambda l: l.camera),
    ], [
        Event(Events.JapesW1aTagged, lambda _: True),
        Event(Events.JapesW1bTagged, lambda _: True),
        Event(Events.JapesW2aTagged, lambda _: True),
        Event(Events.JapesW3bTagged, lambda _: True),
    ], [
        TransitionFront(Regions.JungleJapesMain, lambda _: True),
        TransitionFront(Regions.JapesHill, lambda l: l.climbing),
        TransitionFront(Regions.JapesBeyondPeanutGate, lambda l: l.hasMoveSwitchsanity(Switches.JapesDiddyCave, False) or l.CanPhase() or l.CanPhaseswim() or l.CanSkew(True) or l.CanSkew(False) or l.generalclips),
        TransitionFront(Regions.JapesBeyondCoconutGate1, lambda l: l.checkBarrier(RemovedBarriersSelected.japes_coconut_gates) or Events.JapesFreeKongOpenGates in l.Events or l.CanPhase() or l.CanPhaseswim() or l.CanSkew(True) or l.CanSkew(False) or l.generalclips),
        TransitionFront(Regions.JapesBeyondCoconutGate2, lambda l: l.checkBarrier(RemovedBarriersSelected.japes_coconut_gates) or Events.JapesFreeKongOpenGates in l.Events or l.CanPhase() or l.CanPhaseswim() or l.CanSkew(True) or l.CanSkew(False) or l.generalclips),
        TransitionFront(Regions.JapesCatacomb, lambda l: (l.Slam and l.chunky and l.barrels) or l.CanPhaseswim() or l.CanSkew(True) or l.CanSkew(False), Transitions.JapesMainToCatacomb),
        TransitionFront(Regions.JapesBlastPadPlatform, lambda l: (l.can_use_vines or l.CanMoonkick()) and l.climbing and (l.isdonkey or l.isdiddy or l.ischunky)),
    ]),

    Regions.JapesBlastPadPlatform: Region("Japes Blast Pad Platform", HintRegion.Lowlands, Levels.JungleJapes, False, None, [], [], [
        TransitionFront(Regions.JungleJapesStart, lambda _: True),
        TransitionFront(Regions.JapesBaboonBlast, lambda l: l.blast and l.isdonkey),  # , Transitions.JapesMainToBBlast)
    ]),

    Regions.JapesCannonPlatform: Region("Jungle Japes Cannon Platform", HintRegion.Hillside, Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesLankyCagedBanana, lambda l: ((Events.JapesLankySwitch in l.Events or ((not l.settings.shuffle_shops) and l.CanSkew(True)) or l.CanSkew(False)) and l.lanky) or (((not l.settings.shuffle_shops) and l.CanSkew(True)) or l.CanSkew(False) and l.settings.free_trade_items)),
    ], [
        Event(Events.JapesAccessToCannon, lambda _: True),
    ], [
        TransitionFront(Regions.JapesHillTop, lambda _: True),
        TransitionFront(Regions.JungleJapesMain, lambda _: True),
        TransitionFront(Regions.JapesHill, lambda l: l.can_use_vines),
    ]),

    Regions.JapesHillTop: Region("Jungle Japes Hilltop", HintRegion.Hillside, Levels.JungleJapes, True, None, [
        LocationLogic(Locations.DiddyKong, lambda l: l.CanFreeDiddy()),
        LocationLogic(Locations.JapesDonkeyFrontofCage, lambda l: l.HasKong(l.settings.diddy_freeing_kong) or l.settings.free_trade_items),
        LocationLogic(Locations.JapesDonkeyFreeDiddy, lambda l: Events.JapesFreeKongOpenGates in l.Events),
        LocationLogic(Locations.MelonCrate_Location00, lambda _: True),
        LocationLogic(Locations.JapesMainEnemy_Mountain, lambda _: True),
        LocationLogic(Locations.KremKap_JapesMainEnemy_Mountain, lambda l: l.camera),
        LocationLogic(Locations.JapesChunkyCagedBanana, lambda l: ((Events.JapesChunkySwitch in l.Events or l.CanPhase() or ((not l.settings.shuffle_shops) and (l.CanSkew(True) or l.CanSkew(False)))) and l.chunky) or ((l.CanPhase() or ((not l.settings.shuffle_shops) and (l.CanSkew(True) or l.CanSkew(False)))) and l.settings.free_trade_items)),
    ], [
        Event(Events.JapesFreeKongOpenGates, lambda l: l.CanOpenJapesGates()),
        Event(Events.JapesW2bTagged, lambda _: True),
    ], [
        TransitionFront(Regions.Snide, lambda l: l.snideAccess),
        TransitionFront(Regions.JapesTnSAlcove, lambda l: l.monkey_maneuvers and not l.IsHardFallDamage()),  # Falling from the top is now Monkey Maneuvers but you can't have hard fall damage on for it
        TransitionFront(Regions.Mine, lambda l: l.peanut and l.isdiddy, Transitions.JapesMainToMine),
        TransitionFront(Regions.JapesTopOfMountain, lambda l: (l.peanut and l.isdiddy) or l.CanMoonkick()),
        TransitionFront(Regions.JapesHill, lambda _: True),
        TransitionFront(Regions.JapesCannonPlatform, lambda _: True),
        TransitionFront(Regions.JungleJapesMain, lambda _: True),
    ]),

    Regions.JapesHill: Region("Jungle Japes Hill", HintRegion.Hillside, Levels.JungleJapes, True, None, [
        LocationLogic(Locations.JapesDiddyCagedBanana, lambda l: ((Events.JapesDiddySwitch1 in l.Events or l.CanPhase() or l.generalclips or l.CanSkew(True) or l.CanSkew(False)) and l.diddy) or ((l.CanPhase() or l.generalclips or l.CanSkew(True) or l.CanSkew(False)) and l.settings.free_trade_items)),
        LocationLogic(Locations.JapesBattleArena, lambda l: not l.settings.crown_placement_rando),
    ], [], [
        TransitionFront(Regions.JapesHillTop, lambda l: l.climbing),
        TransitionFront(Regions.JapesCannonPlatform, lambda l: l.can_use_vines),
        TransitionFront(Regions.FunkyJapes, lambda l: l.funkyAccess),
        TransitionFront(Regions.JungleJapesStart, lambda _: True),
    ]),

    Regions.JungleJapesMain: Region("Jungle Japes Main", HintRegion.Hillside, Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesTinyCagedBanana, lambda l: ((Events.JapesTinySwitch in l.Events or l.CanPhase() or l.CanPhaseswim() or l.CanSkew(True) or l.CanSkew(False)) and l.tiny) or ((l.CanPhase() or l.CanPhaseswim() or l.CanSkew(True) or l.CanSkew(False)) and l.settings.free_trade_items)),
        LocationLogic(Locations.JapesMainEnemy_NearPainting0, lambda _: True),
        LocationLogic(Locations.JapesMainEnemy_NearPainting1, lambda _: True),
        LocationLogic(Locations.JapesMainEnemy_NearPainting2, lambda _: True),
        LocationLogic(Locations.KremKap_JapesMainEnemy_NearPainting0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_JapesMainEnemy_NearPainting1, lambda l: l.camera),
        LocationLogic(Locations.KremKap_JapesMainEnemy_NearPainting2, lambda l: l.camera),
    ], [
        Event(Events.JapesW3aTagged, lambda _: True),
    ], [
        TransitionFront(Regions.JungleJapesStart, lambda _: True),
        TransitionFront(Regions.JapesCannonPlatform, lambda l: (l.handstand and l.lanky and l.monkey_maneuvers) or (l.tiny and l.slope_resets)),
        TransitionFront(Regions.JapesBeyondCoconutGate2, lambda l: l.checkBarrier(RemovedBarriersSelected.japes_coconut_gates) or Events.JapesFreeKongOpenGates in l.Events or l.CanPhase() or l.CanPhaseswim() or l.CanSkew(True) or l.CanSkew(False) or l.generalclips),
        TransitionFront(Regions.JapesPaintingRoomHill, lambda l: (l.handstand and l.islanky) or (l.twirl and l.istiny and l.climbing) or l.CanMoonkick() or l.CanSkew(True) or l.CanSkew(False) or l.slope_resets),
        TransitionFront(Regions.JapesLankyCave, lambda l: ((l.hasMoveSwitchsanity(Switches.JapesPainting, False) or l.CanSkew(True) or l.CanSkew(False)) and ((l.handstand and l.islanky) or (l.twirl and l.istiny and l.climbing) or l.CanMoonkick() or l.slope_resets)) or (l.CanMoonkick() and (l.CanPhase() or l.CanSkew(True) or l.CanSkew(False))) or ((l.CanPhase() or l.generalclips or l.CanSkew(True) or l.CanSkew(False)) and (l.isdiddy or l.istiny)), Transitions.JapesMainToLankyCave, isGlitchTransition=True),
        TransitionFront(Regions.BeyondRambiGate, lambda l: l.CanPhaseswim() or l.CanSkew(True) or l.CanSkew(False) or l.CanPhase() or l.generalclips),
        TransitionFront(Regions.JapesTnSAlcove, lambda l: (l.can_use_vines or l.CanMoonkick()) and l.climbing),
    ]),

    Regions.JapesPaintingRoomHill: Region("Japes Painting Room Hill", HintRegion.Hillside, Levels.JungleJapes, False, None, [
        LocationLogic(Locations.RainbowCoin_Location00, lambda _: True),
    ], [], [
        TransitionFront(Regions.JungleJapesMain, lambda _: True),
        TransitionFront(Regions.JapesLankyCave, lambda l: l.hasMoveSwitchsanity(Switches.JapesPainting, False) or l.CanSkew(True) or l.CanSkew(False) or l.CanPhase(), Transitions.JapesMainToLankyCave),
    ]),

    Regions.JapesTnSAlcove: Region("Japes T&S Alcove", HintRegion.Hillside, Levels.JungleJapes, False, None, [], [], [
        TransitionFront(Regions.JungleJapesMain, lambda _: True),
        TransitionFront(Regions.JapesBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.JapesTopOfMountain: Region("Japes Top of Mountain", HintRegion.Hillside, Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesDiddyMountain, lambda l: Events.JapesDiddySwitch2 in l.Events and (l.isdiddy or l.settings.free_trade_items)),
    ], [
        Event(Events.JapesW5bTagged, lambda l: Locations.JapesDiddyMountain in l.SpecialLocationsReached),
    ], [
        TransitionFront(Regions.JapesHillTop, lambda _: True),
    ]),

    Regions.JapesBaboonBlast: Region("Japes Baboon Blast", HintRegion.Lowlands, Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesDonkeyBaboonBlast, lambda l: l.isdonkey),
    ], [], [
        TransitionFront(Regions.JapesBlastPadPlatform, lambda _: True)
    ]),

    Regions.JapesBeyondPeanutGate: Region("Japes Beyond Peanut Gate", HintRegion.Lowlands, Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesDiddyTunnel, lambda l: l.isdiddy or l.settings.free_trade_items),
        LocationLogic(Locations.JapesLankyGrapeGate, lambda l: (l.grape and l.islanky) or ((l.CanPhase() or l.generalclips or l.CanSkew(True) or l.CanSkew(False)) and (l.islanky or l.settings.free_trade_items)), MinigameType.BonusBarrel),
        LocationLogic(Locations.JapesTinyFeatherGateBarrel, lambda l: (l.feather and l.istiny) or ((l.CanPhase() or l.CanSkew(True) or l.CanSkew(False)) and (l.istiny or l.settings.free_trade_items)), MinigameType.BonusBarrel),
        LocationLogic(Locations.JapesMainEnemy_DiddyCavern, lambda _: True),
        LocationLogic(Locations.KremKap_JapesMainEnemy_DiddyCavern, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.JungleJapesStart, lambda _: True),
        TransitionFront(Regions.JapesBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.JapesBeyondCoconutGate1: Region("Japes Beyond Coconut Gate 1", HintRegion.HiveTunnel, Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesKasplatLeftTunnelNear, lambda l: not l.settings.kasplat_rando),
        LocationLogic(Locations.JapesKasplatLeftTunnelFar, lambda l: not l.settings.kasplat_rando),
        LocationLogic(Locations.JapesMainEnemy_FeatherTunnel, lambda _: True),
        LocationLogic(Locations.KremKap_JapesMainEnemy_FeatherTunnel, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.JungleJapesStart, lambda _: True),
        TransitionFront(Regions.JapesBeyondFeatherGate, lambda l: l.checkBarrier(RemovedBarriersSelected.japes_shellhive_gate) or l.hasMoveSwitchsanity(Switches.JapesFeather, False) or l.CanPhase() or l.CanSkew(True) or l.CanSkew(False)),
    ]),

    Regions.JapesBeyondFeatherGate: Region("Japes Beyond Feather Gate", HintRegion.HiveTunnel, Levels.JungleJapes, True, None, [
        LocationLogic(Locations.JapesTinyStump, lambda l: (((l.mini and l.istiny) or l.CanPhase() or l.CanSkew(True) or l.CanSkew(False)) and l.istiny)),
        LocationLogic(Locations.JapesChunkyGiantBonusBarrel, lambda l: l.climbing and l.hunkyChunky and l.ischunky, MinigameType.BonusBarrel),
        LocationLogic(Locations.JapesMainEnemy_Hive0, lambda _: True),
        LocationLogic(Locations.JapesMainEnemy_Hive1, lambda _: True),
        LocationLogic(Locations.JapesMainEnemy_Hive2, lambda _: True),
        LocationLogic(Locations.JapesMainEnemy_Hive3, lambda _: True),
        LocationLogic(Locations.JapesMainEnemy_Hive4, lambda _: True),
        LocationLogic(Locations.KremKap_JapesMainEnemy_Hive0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_JapesMainEnemy_Hive1, lambda l: l.camera),
        LocationLogic(Locations.KremKap_JapesMainEnemy_Hive2, lambda l: l.camera),
        LocationLogic(Locations.KremKap_JapesMainEnemy_Hive3, lambda l: l.camera),
        LocationLogic(Locations.KremKap_JapesMainEnemy_Hive4, lambda l: l.camera),
    ], [
        Event(Events.JapesW5aTagged, lambda _: True),
    ], [
        TransitionFront(Regions.JapesBeyondCoconutGate1, lambda _: True),
        TransitionFront(Regions.TinyHive, lambda l: (l.mini and l.istiny) or l.CanPhase() or l.CanSkew(True) or l.CanSkew(False) or (l.hunkyChunky and l.ischunky and l.generalclips), Transitions.JapesMainToTinyHive),
        TransitionFront(Regions.BeyondRambiGate, lambda l: l.hunkyChunky and l.ischunky and l.generalclips),
    ]),

    Regions.TinyHive: Region("Tiny Hive", HintRegion.HiveTunnel, Levels.JungleJapes, False, -1, [
        LocationLogic(Locations.JapesTinyBeehive, lambda l: (l.istiny and ((l.CanSlamSwitch(Levels.JungleJapes, 1) and (l.saxophone or l.oranges)) or l.CanPhase() or l.generalclips)) or (l.settings.free_trade_items and l.CanPhase())),
        LocationLogic(Locations.JapesShellhiveEnemy_FirstRoom, lambda _: True),
        LocationLogic(Locations.JapesShellhiveEnemy_SecondRoom0, lambda l: (l.istiny and ((l.CanSlamSwitch(Levels.JungleJapes, 1) and (l.saxophone or l.oranges)) or l.CanPhase() or l.generalclips))),
        LocationLogic(Locations.JapesShellhiveEnemy_SecondRoom1, lambda l: (l.istiny and ((l.CanSlamSwitch(Levels.JungleJapes, 1) and (l.saxophone or l.oranges)) or l.CanPhase() or l.generalclips))),
        LocationLogic(Locations.JapesShellhiveEnemy_ThirdRoom0, lambda l: (l.istiny and ((l.CanSlamSwitch(Levels.JungleJapes, 1) and (l.saxophone or l.oranges)) or l.CanPhase() or l.generalclips))),
        LocationLogic(Locations.JapesShellhiveEnemy_ThirdRoom1, lambda l: (l.istiny and ((l.CanSlamSwitch(Levels.JungleJapes, 1) and (l.saxophone or l.oranges)) or l.CanPhase() or l.generalclips))),
        LocationLogic(Locations.JapesShellhiveEnemy_ThirdRoom2, lambda l: (l.istiny and ((l.CanSlamSwitch(Levels.JungleJapes, 1) and (l.saxophone or l.oranges)) or l.CanPhase() or l.generalclips))),
        LocationLogic(Locations.JapesShellhiveEnemy_ThirdRoom3, lambda l: (l.istiny and ((l.CanSlamSwitch(Levels.JungleJapes, 1) and (l.saxophone or l.oranges)) or l.CanPhase() or l.generalclips))),
        LocationLogic(Locations.JapesShellhiveEnemy_MainRoom, lambda _: True),
        LocationLogic(Locations.KremKap_JapesShellhiveEnemy_FirstRoom, lambda l: l.camera),
        LocationLogic(Locations.KremKap_JapesShellhiveEnemy_SecondRoom0, lambda l: l.camera and (l.istiny and ((l.CanSlamSwitch(Levels.JungleJapes, 1) and (l.saxophone or l.oranges)) or l.CanPhase() or l.generalclips))),
        LocationLogic(Locations.KremKap_JapesShellhiveEnemy_SecondRoom1, lambda l: l.camera and (l.istiny and ((l.CanSlamSwitch(Levels.JungleJapes, 1) and (l.saxophone or l.oranges)) or l.CanPhase() or l.generalclips))),
        LocationLogic(Locations.KremKap_JapesShellhiveEnemy_ThirdRoom0, lambda l: l.camera and (l.istiny and ((l.CanSlamSwitch(Levels.JungleJapes, 1) and (l.saxophone or l.oranges)) or l.CanPhase() or l.generalclips))),
        LocationLogic(Locations.KremKap_JapesShellhiveEnemy_ThirdRoom1, lambda l: l.camera and (l.istiny and ((l.CanSlamSwitch(Levels.JungleJapes, 1) and (l.saxophone or l.oranges)) or l.CanPhase() or l.generalclips))),
        LocationLogic(Locations.KremKap_JapesShellhiveEnemy_ThirdRoom2, lambda l: l.camera and (l.istiny and ((l.CanSlamSwitch(Levels.JungleJapes, 1) and (l.saxophone or l.oranges)) or l.CanPhase() or l.generalclips))),
        LocationLogic(Locations.KremKap_JapesShellhiveEnemy_ThirdRoom3, lambda l: l.camera and (l.istiny and ((l.CanSlamSwitch(Levels.JungleJapes, 1) and (l.saxophone or l.oranges)) or l.CanPhase() or l.generalclips))),
        LocationLogic(Locations.KremKap_JapesShellhiveEnemy_MainRoom, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.JapesBeyondFeatherGate, lambda l: l.isdiddy or l.istiny or l.islanky or l.CanPhase(), Transitions.JapesTinyHiveToMain),  # It is technically possible to leave with DK and Chunky, just tricky
    ]),

    Regions.JapesBeyondCoconutGate2: Region("Japes Beyond Coconut Gate 2", HintRegion.StormyTunnel, Levels.JungleJapes, True, None, [
        LocationLogic(Locations.JapesLankySlope, lambda l: (l.handstand and l.islanky) or l.slope_resets, MinigameType.BonusBarrel),
        LocationLogic(Locations.JapesKasplatNearPaintingRoom, lambda l: not l.settings.kasplat_rando),
        LocationLogic(Locations.JapesKasplatNearLab, lambda l: not l.settings.kasplat_rando),
        LocationLogic(Locations.JapesMainEnemy_Storm0, lambda _: True),
        LocationLogic(Locations.JapesMainEnemy_Storm1, lambda _: True),
        LocationLogic(Locations.JapesMainEnemy_Storm2, lambda _: True),
        LocationLogic(Locations.JapesMainEnemy_MiddleTunnel, lambda _: True),
        LocationLogic(Locations.KremKap_JapesMainEnemy_Storm0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_JapesMainEnemy_Storm1, lambda l: l.camera),
        LocationLogic(Locations.KremKap_JapesMainEnemy_Storm2, lambda l: l.camera),
        LocationLogic(Locations.KremKap_JapesMainEnemy_MiddleTunnel, lambda l: l.camera),
    ], [
        Event(Events.Rambi, lambda l: l.hasMoveSwitchsanity(Switches.JapesRambi, False) or l.CanPhase()),
        Event(Events.JapesDonkeySwitch, lambda l: (Events.Rambi in l.Events or l.CanPhase()) and l.CanSlamSwitch(Levels.JungleJapes, 1) and l.donkey),
        Event(Events.JapesDiddySwitch1, lambda l: (Events.Rambi in l.Events or l.CanPhase()) and l.CanSlamSwitch(Levels.JungleJapes, 1) and l.diddy),
        Event(Events.JapesLankySwitch, lambda l: (Events.Rambi in l.Events or l.CanPhase()) and l.CanSlamSwitch(Levels.JungleJapes, 1) and l.lanky),
        Event(Events.JapesTinySwitch, lambda l: (Events.Rambi in l.Events or l.CanPhase()) and l.CanSlamSwitch(Levels.JungleJapes, 1) and l.tiny),
        Event(Events.JapesW4aTagged, lambda _: True),
        Event(Events.JapesW4bTagged, lambda _: True),
    ], [
        TransitionFront(Regions.JungleJapesStart, lambda _: True),
        TransitionFront(Regions.JungleJapesMain, lambda _: True),
        TransitionFront(Regions.JapesUselessSlope, lambda l: (l.handstand and l.islanky) or l.CanPhase() or l.slope_resets),
        TransitionFront(Regions.BeyondRambiGate, lambda l: Events.Rambi in l.Events or l.CanPhase() or l.CanSkew(True) or l.CanSkew(False)),
        TransitionFront(Regions.CrankyJapes, lambda l: l.crankyAccess),
        TransitionFront(Regions.JapesBeyondFeatherGate, lambda l: l.CanMoonkick()),
    ]),

    Regions.JapesUselessSlope: Region("Japes Useless Slope", HintRegion.StormyTunnel, Levels.JungleJapes, False, None, [], [], [
        TransitionFront(Regions.JapesBeyondCoconutGate2, lambda _: True),
    ]),

    Regions.BeyondRambiGate: Region("Beyond Rambi Gate", HintRegion.StormyTunnel, Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesBananaFairyRambiCave, lambda l: l.camera),
        LocationLogic(Locations.MelonCrate_Location01, lambda _: True),
    ], [
        Event(Events.JapesChunkySwitch, lambda l: l.CanSlamSwitch(Levels.JungleJapes, 1) and l.ischunky and l.barrels),
    ], [
        TransitionFront(Regions.JapesBeyondCoconutGate2, lambda _: True),
        TransitionFront(Regions.JapesBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    # Lanky Cave deathwarp: Requires you to be lanky and have simian slam so you can slam the pegs and summon zingers to kill you
    Regions.JapesLankyCave: Region("Japes Lanky Cave", HintRegion.CavesAndMines, Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesLankyFairyCave, lambda l: (((l.grape or l.trombone or l.adv_orange_usage) and l.Slam) or l.generalclips) and l.islanky),
        LocationLogic(Locations.JapesBananaFairyLankyCave, lambda l: (((l.grape or l.trombone or l.adv_orange_usage) and l.Slam) or l.generalclips) and l.islanky and l.camera),
    ], [], [
        TransitionFront(Regions.JapesPaintingRoomHill, lambda _: True, Transitions.JapesLankyCaveToMain),
    ]),

    Regions.Mine: Region("Mine", HintRegion.CavesAndMines, Levels.JungleJapes, False, -1, [
        LocationLogic(Locations.JapesMountainEnemy_Start0, lambda _: True),
        LocationLogic(Locations.JapesMountainEnemy_Start1, lambda _: True),
        LocationLogic(Locations.JapesMountainEnemy_Start2, lambda _: True),
        LocationLogic(Locations.JapesMountainEnemy_Start3, lambda _: True),
        LocationLogic(Locations.JapesMountainEnemy_Start4, lambda _: True),
        LocationLogic(Locations.JapesMountainEnemy_NearGateSwitch0, lambda _: True),
        LocationLogic(Locations.JapesMountainEnemy_NearGateSwitch1, lambda _: True),
        LocationLogic(Locations.JapesMountainEnemy_HiLo, lambda l: (l.charge and l.isdiddy) or l.CanPhase()),
        LocationLogic(Locations.JapesMountainEnemy_Conveyor0, lambda l: (l.CanSlamSwitch(Levels.JungleJapes, 1) and l.isdiddy) or l.CanPhase()),
        LocationLogic(Locations.JapesMountainEnemy_Conveyor1, lambda l: (l.CanSlamSwitch(Levels.JungleJapes, 1) and l.isdiddy) or l.CanPhase()),
        LocationLogic(Locations.KremKap_JapesMountainEnemy_Start0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_JapesMountainEnemy_Start1, lambda l: l.camera),
        LocationLogic(Locations.KremKap_JapesMountainEnemy_Start2, lambda l: l.camera),
        LocationLogic(Locations.KremKap_JapesMountainEnemy_Start3, lambda l: l.camera),
        LocationLogic(Locations.KremKap_JapesMountainEnemy_Start4, lambda l: l.camera),
        LocationLogic(Locations.KremKap_JapesMountainEnemy_NearGateSwitch0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_JapesMountainEnemy_NearGateSwitch1, lambda l: l.camera),
        LocationLogic(Locations.KremKap_JapesMountainEnemy_HiLo, lambda l: l.camera and ((l.charge and l.isdiddy) or l.CanPhase())),
        LocationLogic(Locations.KremKap_JapesMountainEnemy_Conveyor0, lambda l: l.camera and ((l.CanSlamSwitch(Levels.JungleJapes, 1) and l.isdiddy) or l.CanPhase())),
        LocationLogic(Locations.KremKap_JapesMountainEnemy_Conveyor1, lambda l: l.camera and ((l.CanSlamSwitch(Levels.JungleJapes, 1) and l.isdiddy) or l.CanPhase())),
    ], [
        # You're supposed to get to the switch by shooting a peanut switch,
        # but can just jump without too much trouble.
        Event(Events.JapesDiddySwitch2, lambda l: l.CanSlamSwitch(Levels.JungleJapes, 1) and (l.peanut or l.monkey_maneuvers) and l.isdiddy),
    ], [
        TransitionFront(Regions.JapesHillTop, lambda _: True, Transitions.JapesMineToMain),
        TransitionFront(Regions.JapesMinecarts, lambda l: (l.CanSlamSwitch(Levels.JungleJapes, 1) or l.CanPhase()) and ((l.charge and l.isdiddy) or l.CanPhase() or (l.monkey_maneuvers and l.isdiddy))),
    ]),

    Regions.JapesMinecarts: Region("Japes Minecarts", HintRegion.CavesAndMines, Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesDiddyMinecarts, lambda l: l.HasEnoughRaceCoins(Maps.JapesMinecarts, Kongs.diddy, True)),
    ], [], [
        TransitionFront(Regions.JungleJapesMain, lambda _: True),
    ], Transitions.JapesMineToCarts
    ),

    # Catacomb deaths lead back to itself
    Regions.JapesCatacomb: Region("Japes Catacomb", HintRegion.CavesAndMines, Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesChunkyUnderground, lambda l: (l.can_use_vines and l.pineapple and l.ischunky) or (((l.twirl and l.istiny) or (l.can_use_vines and (l.isdiddy or l.istiny)) or (l.isdonkey and (not l.isKrushaAdjacent(Kongs.donkey)))) and l.monkey_maneuvers and l.settings.free_trade_items) or l.CanPhase()),
        LocationLogic(Locations.JapesKasplatUnderground, lambda l: not l.settings.kasplat_rando and ((l.can_use_vines and l.pineapple and l.ischunky) or (l.can_use_vines and (l.isdiddy or l.istiny) and l.monkey_maneuvers and l.settings.free_trade_items) or l.CanPhase())),
    ], [], [
        TransitionFront(Regions.JungleJapesStart, lambda _: True, Transitions.JapesCatacombToMain),
    ]),

    Regions.JapesBossLobby: Region("Japes Boss Lobby", HintRegion.Bosses, Levels.JungleJapes, True, None, [], [], [
        TransitionFront(Regions.JapesBoss, lambda l: l.IsBossReachable(Levels.JungleJapes)),
    ]),

    Regions.JapesBoss: Region("Japes Boss", HintRegion.Bosses, Levels.JungleJapes, False, None, [
        LocationLogic(Locations.JapesKey, lambda l: l.IsBossBeatable(Levels.JungleJapes)),
    ], [], []),
}
