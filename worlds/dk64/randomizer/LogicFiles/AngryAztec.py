# fmt: off
"""Logic file for Angry Aztec."""

from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Maps import Maps
from randomizer.Enums.MinigameType import MinigameType
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Transitions import Transitions
from randomizer.Enums.Settings import RemovedBarriersSelected
from randomizer.Enums.Switches import Switches
from randomizer.Enums.HintRegion import HintRegion
from randomizer.LogicClasses import (Event, LocationLogic, Region,
                                     TransitionFront)

LogicRegions = {
    Regions.AngryAztecMedals: Region("Angry Aztec Medals", HintRegion.AztecCBs, Levels.AngryAztec, False, None, [
        LocationLogic(Locations.AztecDonkeyMedal, lambda l: l.ColoredBananas[Levels.AngryAztec][Kongs.donkey] >= l.settings.medal_cb_req_level[1]),
        LocationLogic(Locations.AztecDiddyMedal, lambda l: l.ColoredBananas[Levels.AngryAztec][Kongs.diddy] >= l.settings.medal_cb_req_level[1]),
        LocationLogic(Locations.AztecLankyMedal, lambda l: l.ColoredBananas[Levels.AngryAztec][Kongs.lanky] >= l.settings.medal_cb_req_level[1]),
        LocationLogic(Locations.AztecTinyMedal, lambda l: l.ColoredBananas[Levels.AngryAztec][Kongs.tiny] >= l.settings.medal_cb_req_level[1]),
        LocationLogic(Locations.AztecChunkyMedal, lambda l: l.ColoredBananas[Levels.AngryAztec][Kongs.chunky] >= l.settings.medal_cb_req_level[1]),
        LocationLogic(Locations.AztecDonkeyHalfMedal, lambda l: l.ColoredBananas[Levels.AngryAztec][Kongs.donkey] >= max(1, int(l.settings.medal_cb_req_level[1] >> 1))),
        LocationLogic(Locations.AztecDiddyHalfMedal, lambda l: l.ColoredBananas[Levels.AngryAztec][Kongs.diddy] >= max(1, int(l.settings.medal_cb_req_level[1] >> 1))),
        LocationLogic(Locations.AztecLankyHalfMedal, lambda l: l.ColoredBananas[Levels.AngryAztec][Kongs.lanky] >= max(1, int(l.settings.medal_cb_req_level[1] >> 1))),
        LocationLogic(Locations.AztecTinyHalfMedal, lambda l: l.ColoredBananas[Levels.AngryAztec][Kongs.tiny] >= max(1, int(l.settings.medal_cb_req_level[1] >> 1))),
        LocationLogic(Locations.AztecChunkyHalfMedal, lambda l: l.ColoredBananas[Levels.AngryAztec][Kongs.chunky] >= max(1, int(l.settings.medal_cb_req_level[1] >> 1))),
    ], [], [], restart=-1),

    # This region serves to set up the entry for the level based on the DK Portal Location
    Regions.AngryAztecEntryHandler: Region("Angry Aztec Entry Handler", HintRegion.Error, Levels.AngryAztec, False, None, [], [
        Event(Events.AztecEntered, lambda _: True),
    ], [
        TransitionFront(Regions.AngryAztecLobby, lambda _: True, Transitions.AztecToIsles),
        TransitionFront(Regions.AngryAztecStart, lambda _: True),  # Don't move this away from index 1 (ShuffleDoors.py relies on this being index 1)
    ], restart=-1),

    Regions.AngryAztecStart: Region("Angry Aztec Start", HintRegion.AztecTunnels, Levels.AngryAztec, False, None, [], [], [
        TransitionFront(Regions.BetweenVinesByPortal, lambda l: l.assumeAztecEntry or l.can_use_vines or (l.istiny and l.twirl) or l.CanPhase()),
    ]),

    Regions.BetweenVinesByPortal: Region("Angry Aztec Between Vines By Portal", HintRegion.AztecTunnels, Levels.AngryAztec, False, -1, [
        LocationLogic(Locations.AztecChunkyVases, lambda l: (l.pineapple or l.CanPhase()) and l.chunky and l.barrels),
        LocationLogic(Locations.HoldableVaseCircle, lambda l: (l.pineapple or l.CanPhase()) and l.chunky and l.barrels),
        LocationLogic(Locations.HoldableVaseTriangle, lambda l: (l.pineapple or l.CanPhase()) and l.chunky and l.barrels),
        LocationLogic(Locations.HoldableVaseColon, lambda l: (l.pineapple or l.CanPhase()) and l.chunky and l.barrels),
        LocationLogic(Locations.HoldableVasePlus, lambda l: (l.pineapple or l.CanPhase()) and l.chunky and l.barrels),
        LocationLogic(Locations.AztecMainEnemy_VaseRoom0, lambda l: (l.pineapple and l.ischunky) or l.CanPhase()),
        LocationLogic(Locations.AztecMainEnemy_VaseRoom1, lambda l: (l.pineapple and l.ischunky) or l.CanPhase()),
        LocationLogic(Locations.AztecMainEnemy_VaseRoom2, lambda l: (l.pineapple and l.ischunky) or l.CanPhase()),
        LocationLogic(Locations.AztecMainEnemy_StartingTunnel0, lambda _: True),
        LocationLogic(Locations.AztecMainEnemy_StartingTunnel1, lambda _: True),
        LocationLogic(Locations.AztecMainEnemy_StartingTunnel2, lambda _: True),
        LocationLogic(Locations.KremKap_AztecMainEnemy_VaseRoom0, lambda l: l.camera and ((l.pineapple and l.ischunky) or l.CanPhase())),
        LocationLogic(Locations.KremKap_AztecMainEnemy_VaseRoom1, lambda l: l.camera and ((l.pineapple and l.ischunky) or l.CanPhase())),
        LocationLogic(Locations.KremKap_AztecMainEnemy_VaseRoom2, lambda l: l.camera and ((l.pineapple and l.ischunky) or l.CanPhase())),
        LocationLogic(Locations.KremKap_AztecMainEnemy_StartingTunnel0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecMainEnemy_StartingTunnel1, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecMainEnemy_StartingTunnel2, lambda l: l.camera),
    ], [
        Event(Events.AztecW1aTagged, lambda _: True),
    ], [
        TransitionFront(Regions.AngryAztecStart, lambda l: l.can_use_vines or (l.istiny and l.twirl) or l.CanPhase()),
        TransitionFront(Regions.AztecTunnelBeforeOasis, lambda l: l.assumeAztecEntry or l.can_use_vines or (l.istiny and l.twirl) or l.CanPhase()),
    ]),

    Regions.AztecTunnelBeforeOasis: Region("Angry Aztec Tunnel Before Oasis", HintRegion.AztecTunnels, Levels.AngryAztec, False, -1, [
        LocationLogic(Locations.AztecKasplatSandyBridge, lambda l: not l.settings.kasplat_rando and (l.CanPhase() or (l.hasMoveSwitchsanity(Switches.AztecBlueprintDoor, False) and ((l.strongKong and l.isdonkey) or (l.twirl and l.istiny))))),
        LocationLogic(Locations.AztecMainEnemy_StartingTunnel3, lambda _: True),
        LocationLogic(Locations.KremKap_AztecMainEnemy_StartingTunnel3, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.BetweenVinesByPortal, lambda l: l.can_use_vines or (l.istiny and l.twirl) or l.CanPhase()),
        TransitionFront(Regions.AngryAztecOasis, lambda _: True),
    ]),

    Regions.AngryAztecOasis: Region("Angry Aztec Oasis", HintRegion.OasisAndTotem, Levels.AngryAztec, True, -1, [
        LocationLogic(Locations.AztecDonkeyFreeLlama, lambda l: Events.LlamaFreed in l.Events),
        LocationLogic(Locations.AztecKasplatOnTinyTemple, lambda l: not l.settings.kasplat_rando and l.jetpack and l.isdiddy and l.climbing),
        LocationLogic(Locations.RainbowCoin_Location06, lambda _: True),
        LocationLogic(Locations.AztecMainEnemy_NearCandy, lambda _: True),
        LocationLogic(Locations.AztecMainEnemy_OasisDoor, lambda _: True),
        LocationLogic(Locations.KremKap_AztecMainEnemy_NearCandy, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecMainEnemy_OasisDoor, lambda l: l.camera),
    ], [
        Event(Events.AztecGuitarPad, lambda l: ((l.can_use_vines and l.climbing) or (l.jetpack and l.isdiddy and l.climbing) or (l.monkey_maneuvers and (l.istiny or l.isdiddy))) and l.hasMoveSwitchsanity(Switches.AztecGuitar, True)),
        Event(Events.AztecW1bTagged, lambda _: True),
        Event(Events.AztecW2aTagged, lambda _: True),
    ], [
        TransitionFront(Regions.AztecTunnelBeforeOasis, lambda _: True),
        TransitionFront(Regions.TempleStart, lambda l: ((l.peanut and l.isdiddy) or (l.grape and l.islanky)
                        or (l.feather and l.istiny) or (l.pineapple and l.ischunky)) or l.CanPhase(), Transitions.AztecStartToTemple),
        TransitionFront(Regions.AngryAztecConnectorTunnel, lambda l: l.checkBarrier(RemovedBarriersSelected.aztec_tunnel_door) or Events.AztecGuitarPad in l.Events or l.CanPhase() or l.generalclips),
        TransitionFront(Regions.CandyAztec, lambda l: l.candyAccess),
        TransitionFront(Regions.AztecBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.TempleStart: Region("Temple Start", HintRegion.TinyTemple, Levels.AngryAztec, False, -1, [
        LocationLogic(Locations.AztecChunkyKlaptrapRoom, lambda l: (l.triangle or (l.CanPhaseswim() and Events.AztecIceMelted in l.Events) or l.CanPhase()) and l.ischunky),
        LocationLogic(Locations.AztecTempleEnemy_GuardRotating0, lambda _: True),
        LocationLogic(Locations.AztecTempleEnemy_GuardRotating1, lambda _: True),
        LocationLogic(Locations.AztecTempleEnemy_MainRoom0, lambda _: True),
        LocationLogic(Locations.AztecTempleEnemy_MainRoom1, lambda _: True),
        LocationLogic(Locations.AztecTempleEnemy_MainRoom2, lambda _: True),
        LocationLogic(Locations.KremKap_AztecTempleEnemy_GuardRotating0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecTempleEnemy_GuardRotating1, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecTempleEnemy_MainRoom0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecTempleEnemy_MainRoom1, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecTempleEnemy_MainRoom2, lambda l: l.camera),
    ], [
    ], [
        TransitionFront(Regions.AngryAztecOasis, lambda _: True, Transitions.AztecTempleToStart),
        TransitionFront(Regions.TempleGuitarPad, lambda l: l.CanSlamSwitch(Levels.AngryAztec, 1) and l.peanut and l.isdiddy),
        TransitionFront(Regions.TempleUnderwater, lambda l: l.swim and Events.AztecIceMelted in l.Events),
    ]),

    Regions.TempleGuitarPad: Region("Temple Guitar Pad", HintRegion.TinyTemple, Levels.AngryAztec, False, -1, [], [
        Event(Events.AztecIceMelted, lambda l: l.guitar and l.isdiddy),
    ], [
        TransitionFront(Regions.TempleStart, lambda _: True),
    ]),

    Regions.TempleUnderwater: Region("Temple Underwater", HintRegion.TinyTemple, Levels.AngryAztec, False, -1, [
        LocationLogic(Locations.AztecTinyKlaptrapRoom, lambda l: ((l.mini and l.istiny) or l.CanPhase() or l.generalclips or l.CanPhaseswim())),
        LocationLogic(Locations.KremKap_AztecTempleEnemy_Underwater, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.TempleStart, lambda l: Events.AztecIceMelted in l.Events),
        TransitionFront(Regions.TempleVultureRoom, lambda _: True),
        TransitionFront(Regions.TempleKONGRoom, lambda _: True),
    ]),

    Regions.TempleVultureRoom: Region("Temple Vulture Room", HintRegion.TinyTemple, Levels.AngryAztec, False, -1, [
        LocationLogic(Locations.AztecLankyVulture, lambda l: l.CanSlamSwitch(Levels.AngryAztec, 1) and l.grape and l.islanky),
        LocationLogic(Locations.AztecBattleArena, lambda l: not l.settings.crown_placement_rando and l.CanSlamSwitch(Levels.AngryAztec, 1) and l.grape and l.lanky),
    ], [], [
        TransitionFront(Regions.TempleUnderwater, lambda l: l.swim),
    ]),

    Regions.TempleKONGRoom: Region("Temple KONG Room", HintRegion.TinyTemple, Levels.AngryAztec, False, -1, [
        LocationLogic(Locations.TinyKong, lambda l: l.CanFreeTiny()),
        LocationLogic(Locations.AztecDiddyFreeTiny, lambda l: l.CanFreeTiny() or l.CanPhase() or l.ledgeclip or l.CanPhaseswim()),
        LocationLogic(Locations.AztecTempleEnemy_KongRoom0, lambda _: True),
        LocationLogic(Locations.AztecTempleEnemy_KongRoom1, lambda _: True),
        LocationLogic(Locations.AztecTempleEnemy_KongRoom2, lambda _: True),
        LocationLogic(Locations.AztecTempleEnemy_KongRoom3, lambda _: True),
        LocationLogic(Locations.AztecTempleEnemy_KongRoom4, lambda _: True),
        LocationLogic(Locations.KremKap_AztecTempleEnemy_KongRoom0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecTempleEnemy_KongRoom1, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecTempleEnemy_KongRoom2, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecTempleEnemy_KongRoom3, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecTempleEnemy_KongRoom4, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.TempleUnderwater, lambda l: l.swim),
    ]),

    Regions.AngryAztecConnectorTunnel: Region("Angry Aztec Connector Tunnel", HintRegion.AztecTunnels, Levels.AngryAztec, False, -1, [
        LocationLogic(Locations.AztecChunkyCagedBarrel, lambda l: l.ischunky and ((l.hunkyChunky and (l.barrels or l.generalclips)) or l.CanPhase()), MinigameType.BonusBarrel),
        LocationLogic(Locations.AztecKasplatNearLab, lambda l: not l.settings.kasplat_rando),
        LocationLogic(Locations.AztecMainEnemy_TunnelPad0, lambda _: True),
        LocationLogic(Locations.AztecMainEnemy_TunnelCage0, lambda _: True),
        LocationLogic(Locations.AztecMainEnemy_TunnelCage1, lambda _: True),
        LocationLogic(Locations.AztecMainEnemy_TunnelCage2, lambda _: True),
        LocationLogic(Locations.AztecMainEnemy_TunnelCage3, lambda _: True),
        LocationLogic(Locations.AztecMainEnemy_TunnelPad1, lambda _: True),
        LocationLogic(Locations.KremKap_AztecMainEnemy_TunnelPad0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecMainEnemy_TunnelCage0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecMainEnemy_TunnelCage1, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecMainEnemy_TunnelCage2, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecMainEnemy_TunnelCage3, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecMainEnemy_TunnelPad1, lambda l: l.camera),
        LocationLogic(Locations.HoldableBoulderAztec, lambda l: l.barrels and l.hunkyChunky and l.ischunky),
    ], [
        Event(Events.AztecW3bTagged, lambda _: True),
    ], [
        TransitionFront(Regions.AngryAztecOasis, lambda _: True),
        TransitionFront(Regions.AngryAztecMain, lambda _: True),
        TransitionFront(Regions.CrankyAztec, lambda l: l.crankyAccess),
    ]),

    Regions.AngryAztecMain: Region("Angry Aztec Main", HintRegion.OasisAndTotem, Levels.AngryAztec, True, -1, [
        LocationLogic(Locations.AztecDiddyRamGongs, lambda l: l.charge and l.jetpack and l.diddy),
        LocationLogic(Locations.AztecDiddyVultureRace, lambda l: l.jetpack and l.diddy),
        LocationLogic(Locations.MelonCrate_Location06, lambda l: (l.jetpack and l.isdiddy) or l.CanMoonkick()),
        LocationLogic(Locations.MelonCrate_Location07, lambda _: True),
        LocationLogic(Locations.AztecMainEnemy_OutsideLlama, lambda _: True),
        LocationLogic(Locations.AztecMainEnemy_OutsideTower, lambda _: True),
        LocationLogic(Locations.AztecMainEnemy_AroundTotem, lambda _: True),
        LocationLogic(Locations.AztecMainEnemy_Outside5DT, lambda _: True),
        LocationLogic(Locations.AztecMainEnemy_OutsideSnide, lambda _: True),
        LocationLogic(Locations.AztecMainEnemy_NearSnoopTunnel, lambda _: True),
        LocationLogic(Locations.KremKap_AztecMainEnemy_OutsideLlama, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecMainEnemy_OutsideTower, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecMainEnemy_AroundTotem, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecMainEnemy_Outside5DT, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecMainEnemy_OutsideSnide, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecMainEnemy_NearSnoopTunnel, lambda l: l.camera),
    ], [
        Event(Events.FedTotem, lambda l: l.checkBarrier(RemovedBarriersSelected.aztec_5dtemple_switches) or (l.jetpack and l.CanSlamSwitch(Levels.AngryAztec, 1) and l.peanut and l.diddy)),
        Event(Events.AztecW2bTagged, lambda _: True),
        Event(Events.AztecW3aTagged, lambda _: True),
        Event(Events.AztecW4aTagged, lambda _: True),
        Event(Events.AztecW4bTagged, lambda _: True),
        Event(Events.AztecW5aTagged, lambda _: True),
    ], [
        TransitionFront(Regions.AngryAztecConnectorTunnel, lambda _: True),
        TransitionFront(Regions.DonkeyTemple, lambda l: (Events.FedTotem in l.Events and l.coconut and l.isdonkey) or l.CanPhase() or l.generalclips, Transitions.AztecMainToDonkey),
        TransitionFront(Regions.DiddyTemple, lambda l: (Events.FedTotem in l.Events and l.peanut and l.isdiddy) or (l.generalclips and l.charge and l.isdiddy) or l.CanPhase(), Transitions.AztecMainToDiddy),
        TransitionFront(Regions.LankyTempleEntrance, lambda l: (Events.FedTotem in l.Events and l.grape and l.islanky) or l.CanPhase(), Transitions.AztecMainToLanky),
        TransitionFront(Regions.TinyTempleEntrance, lambda l: (Events.FedTotem in l.Events and l.feather and l.istiny) or l.CanPhase(), Transitions.AztecMainToTiny),
        TransitionFront(Regions.ChunkyTempleEntrance, lambda l: (Events.FedTotem in l.Events and l.pineapple and l.ischunky) or l.CanPhase() or (l.generalclips and l.ischunky and l.hunkyChunky), Transitions.AztecMainToChunky),
        TransitionFront(Regions.AztecTinyRace, lambda l: l.charge and l.jetpack and l.diddy and l.mini and l.saxophone and l.istiny, Transitions.AztecMainToRace),
        TransitionFront(Regions.LlamaTemple, lambda l: l.canOpenLlamaTemple() or l.CanPhase() or (l.generalclips and not l.islanky), Transitions.AztecMainToLlama),
        TransitionFront(Regions.AztecBaboonBlast, lambda l: l.blast and l.isdonkey),  # , Transitions.AztecMainToBBlast),
        TransitionFront(Regions.Snide, lambda l: l.snideAccess),
        TransitionFront(Regions.FunkyAztec, lambda l: l.funkyAccess),
        TransitionFront(Regions.AztecDonkeyQuicksandCave, lambda l: (((Events.AztecDonkeySwitch in l.Events and l.strongKong) or ((not l.settings.shuffle_shops) and l.generalclips)) and l.isdonkey) or l.CanPhase()),
        TransitionFront(Regions.AztecBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.AztecDonkeyQuicksandCave: Region("Aztec Donkey Sand Tunnel", HintRegion.AztecTunnels, Levels.AngryAztec, False, -1, [
        LocationLogic(Locations.AztecDonkeyQuicksandCave, lambda l: l.isdonkey or l.settings.free_trade_items, MinigameType.BonusBarrel),
    ], [
        Event(Events.AztecW5bTagged, lambda l: Locations.AztecDonkeyQuicksandCave in l.SpecialLocationsReached),
    ], [
        TransitionFront(Regions.AngryAztecMain, lambda l: (l.isdonkey and l.strongKong) or l.CanPhase())
    ]),

    Regions.AztecBaboonBlast: Region("Aztec Baboon Blast", HintRegion.OasisAndTotem, Levels.AngryAztec, False, None, [], [
        Event(Events.LlamaFreed, lambda l: l.isdonkey)
    ], [
        TransitionFront(Regions.AngryAztecMain, lambda _: True)
    ]),

    # All the 5 door temple require their respective gun to die
    Regions.DonkeyTemple: Region("Donkey Temple", HintRegion.FiveDoorTemple, Levels.AngryAztec, False, TransitionFront(Regions.AngryAztecEntryHandler, lambda l: (l.coconut and l.isdonkey) or l.CanPhase()), [
        LocationLogic(Locations.AztecDonkey5DoorTemple, lambda l: (l.coconut or l.CanPhase()) and (l.isdonkey or l.settings.free_trade_items)),
        LocationLogic(Locations.AztecDK5DTEnemy_EndTrap0, lambda l: (l.coconut and l.isdonkey) or l.CanPhase()),
        LocationLogic(Locations.AztecDK5DTEnemy_EndTrap1, lambda l: (l.coconut and l.isdonkey) or l.CanPhase()),
        LocationLogic(Locations.AztecDK5DTEnemy_EndTrap2, lambda l: (l.coconut and l.isdonkey) or l.CanPhase()),
        LocationLogic(Locations.AztecDK5DTEnemy_EndPath0, lambda l: (l.coconut and l.isdonkey) or l.CanPhase()),
        LocationLogic(Locations.AztecDK5DTEnemy_EndPath1, lambda l: (l.coconut and l.isdonkey) or l.CanPhase()),
        LocationLogic(Locations.AztecDK5DTEnemy_StartPath, lambda l: (l.coconut and l.isdonkey) or l.CanPhase()),
        LocationLogic(Locations.KremKap_AztecDK5DTEnemy_EndTrap0, lambda l: l.camera and ((l.coconut and l.isdonkey) or l.CanPhase())),
        LocationLogic(Locations.KremKap_AztecDK5DTEnemy_EndTrap1, lambda l: l.camera and ((l.coconut and l.isdonkey) or l.CanPhase())),
        LocationLogic(Locations.KremKap_AztecDK5DTEnemy_EndTrap2, lambda l: l.camera and ((l.coconut and l.isdonkey) or l.CanPhase())),
        LocationLogic(Locations.KremKap_AztecDK5DTEnemy_EndPath0, lambda l: l.camera and ((l.coconut and l.isdonkey) or l.CanPhase())),
        LocationLogic(Locations.KremKap_AztecDK5DTEnemy_EndPath1, lambda l: l.camera and ((l.coconut and l.isdonkey) or l.CanPhase())),
        LocationLogic(Locations.KremKap_AztecDK5DTEnemy_StartPath, lambda l: l.camera and ((l.coconut and l.isdonkey) or l.CanPhase())),
    ], [], [
        TransitionFront(Regions.AngryAztecMain, lambda _: True, Transitions.AztecDonkeyToMain),
        TransitionFront(Regions.DonkeyTempleDeadEndRight, lambda l: (l.coconut and l.isdonkey) or l.CanPhase()),
    ]),

    Regions.DonkeyTempleDeadEndRight: Region("Donkey Temple Dead End Right", HintRegion.FiveDoorTemple, Levels.AngryAztec, False, -1, [
        LocationLogic(Locations.AztecDK5DTEnemy_StartTrap0, lambda _: True),
        LocationLogic(Locations.AztecDK5DTEnemy_StartTrap1, lambda _: True),
        LocationLogic(Locations.AztecDK5DTEnemy_StartTrap2, lambda _: True),
        LocationLogic(Locations.KremKap_AztecDK5DTEnemy_StartTrap0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecDK5DTEnemy_StartTrap1, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecDK5DTEnemy_StartTrap2, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.DonkeyTemple, lambda _: True),
    ]),

    Regions.DiddyTemple: Region("Diddy Temple", HintRegion.FiveDoorTemple, Levels.AngryAztec, False, TransitionFront(Regions.AngryAztecEntryHandler, lambda l: (l.peanut and l.isdiddy) or l.CanPhase()), [
        LocationLogic(Locations.AztecDiddy5DoorTemple, lambda l: (l.peanut or l.CanPhase()) and (l.isdiddy or l.settings.free_trade_items)),
        LocationLogic(Locations.AztecDiddy5DTEnemy_StartLeft0, lambda l: (l.peanut and l.isdiddy) or l.CanPhase()),
        LocationLogic(Locations.AztecDiddy5DTEnemy_StartLeft1, lambda l: (l.peanut and l.isdiddy) or l.CanPhase()),
        LocationLogic(Locations.AztecDiddy5DTEnemy_Reward, lambda l: (l.peanut and l.isdiddy) or l.CanPhase()),
        LocationLogic(Locations.AztecDiddy5DTEnemy_SecondSwitch, lambda l: (l.peanut and l.isdiddy) or l.CanPhase()),
        LocationLogic(Locations.KremKap_AztecDiddy5DTEnemy_StartLeft0, lambda l: l.camera and ((l.peanut and l.isdiddy) or l.CanPhase())),
        LocationLogic(Locations.KremKap_AztecDiddy5DTEnemy_StartLeft1, lambda l: l.camera and ((l.peanut and l.isdiddy) or l.CanPhase())),
        LocationLogic(Locations.KremKap_AztecDiddy5DTEnemy_Reward, lambda l: l.camera and ((l.peanut and l.isdiddy) or l.CanPhase())),
        LocationLogic(Locations.KremKap_AztecDiddy5DTEnemy_SecondSwitch, lambda l: l.camera and ((l.peanut and l.isdiddy) or l.CanPhase())),
    ], [], [
        TransitionFront(Regions.AngryAztecMain, lambda _: True, Transitions.AztecDiddyToMain),
        TransitionFront(Regions.DiddyTempleDeadEndRight, lambda l: (l.peanut and l.isdiddy) or l.CanPhase()),
    ]),

    Regions.DiddyTempleDeadEndRight: Region("Diddy Temple Dead End Right", HintRegion.FiveDoorTemple, Levels.AngryAztec, False, -1, [
        LocationLogic(Locations.AztecDiddy5DTEnemy_EndTrap0, lambda _: True),
        LocationLogic(Locations.AztecDiddy5DTEnemy_EndTrap1, lambda _: True),
        LocationLogic(Locations.AztecDiddy5DTEnemy_EndTrap2, lambda _: True),
        LocationLogic(Locations.KremKap_AztecDiddy5DTEnemy_EndTrap0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecDiddy5DTEnemy_EndTrap1, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecDiddy5DTEnemy_EndTrap2, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.DiddyTemple, lambda _: True),
    ]),

    Regions.LankyTempleEntrance: Region("Lanky Temple Entrance", HintRegion.FiveDoorTemple, Levels.AngryAztec, False, None, [
    ], [], [
        TransitionFront(Regions.AngryAztecMain, lambda _: True, Transitions.AztecLankyToMain),
        TransitionFront(Regions.LankyTemple, lambda l: (l.grape and l.islanky) or l.CanPhase()),
    ]),

    Regions.LankyTemple: Region("Lanky Temple", HintRegion.FiveDoorTemple, Levels.AngryAztec, False, -1, [
        LocationLogic(Locations.AztecLanky5DoorTemple, lambda l: (l.grape or l.CanPhase()) and (l.islanky or l.settings.free_trade_items), MinigameType.BonusBarrel),
        LocationLogic(Locations.AztecLanky5DTEnemy_JoiningPaths, lambda _: True),
        LocationLogic(Locations.AztecLanky5DTEnemy_EndTrap, lambda l: (l.grape and l.islanky) or l.CanPhase()),
        LocationLogic(Locations.AztecLanky5DTEnemy_Reward, lambda l: (l.grape and l.islanky) or l.CanPhase()),
        LocationLogic(Locations.KremKap_AztecLanky5DTEnemy_JoiningPaths, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecLanky5DTEnemy_EndTrap, lambda l: l.camera and ((l.grape and l.islanky) or l.CanPhase())),
        LocationLogic(Locations.KremKap_AztecLanky5DTEnemy_Reward, lambda l: l.camera and ((l.grape and l.islanky) or l.CanPhase())),
    ], [], [
        TransitionFront(Regions.LankyTempleEntrance, lambda _: True),
    ]),

    Regions.TinyTempleEntrance: Region("Tiny Temple Entrance", HintRegion.FiveDoorTemple, Levels.AngryAztec, False, None, [], [], [
        TransitionFront(Regions.AngryAztecMain, lambda _: True, Transitions.AztecTinyToMain),
        TransitionFront(Regions.TinyTemple, lambda l: (l.feather and l.istiny) or l.CanPhase()),
    ]),

    Regions.TinyTemple: Region("Tiny Temple", HintRegion.FiveDoorTemple, Levels.AngryAztec, False, -1, [
        LocationLogic(Locations.AztecTiny5DoorTemple, lambda l: (l.feather or l.CanPhase()) and (l.istiny or l.settings.free_trade_items)),
        LocationLogic(Locations.AztecBananaFairyTinyTemple, lambda l: l.camera and ((l.mini and l.istiny) or l.CanPhase())),
        LocationLogic(Locations.AztecTiny5DTEnemy_StartRightFront, lambda _: True),
        LocationLogic(Locations.AztecTiny5DTEnemy_StartLeftBack, lambda _: True),
        LocationLogic(Locations.AztecTiny5DTEnemy_StartRightBack, lambda _: True),
        LocationLogic(Locations.AztecTiny5DTEnemy_StartLeftFront, lambda _: True),
        LocationLogic(Locations.AztecTiny5DTEnemy_Reward0, lambda l: (l.feather and l.istiny) or l.CanPhase()),
        LocationLogic(Locations.AztecTiny5DTEnemy_Reward1, lambda l: (l.feather and l.istiny) or l.CanPhase()),
        LocationLogic(Locations.AztecTiny5DTEnemy_DeadEnd0, lambda l: (l.feather and l.istiny) or l.CanPhase()),
        LocationLogic(Locations.AztecTiny5DTEnemy_DeadEnd1, lambda l: (l.feather and l.istiny) or l.CanPhase()),
        LocationLogic(Locations.KremKap_AztecTiny5DTEnemy_StartRightFront, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecTiny5DTEnemy_StartLeftBack, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecTiny5DTEnemy_StartRightBack, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecTiny5DTEnemy_StartLeftFront, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecTiny5DTEnemy_Reward0, lambda l: l.camera and ((l.feather and l.istiny) or l.CanPhase())),
        LocationLogic(Locations.KremKap_AztecTiny5DTEnemy_Reward1, lambda l: l.camera and ((l.feather and l.istiny) or l.CanPhase())),
        LocationLogic(Locations.KremKap_AztecTiny5DTEnemy_DeadEnd0, lambda l: l.camera and ((l.feather and l.istiny) or l.CanPhase())),
        LocationLogic(Locations.KremKap_AztecTiny5DTEnemy_DeadEnd1, lambda l: l.camera and ((l.feather and l.istiny) or l.CanPhase())),
    ], [], [
        TransitionFront(Regions.TinyTempleEntrance, lambda _: True),
    ]),

    Regions.ChunkyTempleEntrance: Region("Chunky Temple Entrance", HintRegion.FiveDoorTemple, Levels.AngryAztec, False, None, [], [], [
        TransitionFront(Regions.AngryAztecMain, lambda _: True, Transitions.AztecChunkyToMain),
        TransitionFront(Regions.ChunkyTemple, lambda l: (l.pineapple and l.ischunky) or l.CanPhase()),
    ]),

    Regions.ChunkyTemple: Region("Chunky Temple", HintRegion.FiveDoorTemple, Levels.AngryAztec, False, -1, [
        LocationLogic(Locations.AztecChunky5DoorTemple, lambda l: (l.pineapple or l.CanPhase()) and (l.ischunky or l.settings.free_trade_items), MinigameType.BonusBarrel),
        LocationLogic(Locations.AztecKasplatChunky5DT, lambda l: not l.settings.kasplat_rando and ((l.pineapple and l.ischunky) or l.CanPhase())),
        LocationLogic(Locations.RainbowCoin_Location01, lambda _: True),
        LocationLogic(Locations.AztecChunky5DTEnemy_StartRight, lambda _: True),
        LocationLogic(Locations.AztecChunky5DTEnemy_StartLeft, lambda _: True),
        LocationLogic(Locations.AztecChunky5DTEnemy_SecondRight, lambda _: True),
        LocationLogic(Locations.AztecChunky5DTEnemy_SecondLeft, lambda _: True),
        LocationLogic(Locations.AztecChunky5DTEnemy_Reward, lambda l: (l.pineapple and l.ischunky) or l.CanPhase()),
        LocationLogic(Locations.KremKap_AztecChunky5DTEnemy_StartRight, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecChunky5DTEnemy_StartLeft, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecChunky5DTEnemy_SecondRight, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecChunky5DTEnemy_SecondLeft, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecChunky5DTEnemy_Reward, lambda l: l.camera and ((l.pineapple and l.ischunky) or l.CanPhase())),
    ], [], [
        TransitionFront(Regions.ChunkyTempleEntrance, lambda _: True),
    ]),

    Regions.AztecTinyRace: Region("Aztec Tiny Race", HintRegion.OasisAndTotem, Levels.AngryAztec, False, None, [
        LocationLogic(Locations.AztecTinyBeetleRace, lambda l: l.HasEnoughRaceCoins(Maps.AztecTinyRace, Kongs.tiny, not l.settings.free_trade_items)),
    ], [], [
        TransitionFront(Regions.AngryAztecMain, lambda _: True, Transitions.AztecRaceToMain),
    ], Transitions.AztecMainToRace
    ),

    Regions.LlamaTemple: Region("Llama Temple", HintRegion.LlamaTemple, Levels.AngryAztec, True, -1, [
        LocationLogic(Locations.LankyKong, lambda l: l.CanFreeLanky()),
        LocationLogic(Locations.AztecDonkeyFreeLanky, lambda l: l.CanFreeLanky()),
        LocationLogic(Locations.AztecLankyLlamaTempleBarrel, lambda l: l.trombone and ((l.handstand and l.islanky) or (l.settings.free_trade_items and ((l.istiny and ((l.twirl and l.monkey_maneuvers) or l.slope_resets)) or l.CanMoonkick()))), MinigameType.BonusBarrel),
        LocationLogic(Locations.AztecBananaFairyLlamaTemple, lambda l: l.camera),
        LocationLogic(Locations.MelonCrate_Location02, lambda _: True),
        LocationLogic(Locations.AztecLlamaEnemy_KongFreeInstrument, lambda _: True),
        LocationLogic(Locations.AztecLlamaEnemy_DinoInstrument, lambda _: True),
        LocationLogic(Locations.AztecLlamaEnemy_Right, lambda _: True),
        LocationLogic(Locations.AztecLlamaEnemy_Left, lambda _: True),
        LocationLogic(Locations.AztecLlamaEnemy_MelonCrate, lambda _: True),
        LocationLogic(Locations.AztecLlamaEnemy_SlamSwitch, lambda _: True),
        LocationLogic(Locations.KremKap_AztecLlamaEnemy_KongFreeInstrument, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecLlamaEnemy_DinoInstrument, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecLlamaEnemy_Right, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecLlamaEnemy_Left, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecLlamaEnemy_MelonCrate, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecLlamaEnemy_SlamSwitch, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecNPC_Llama, lambda l: l.camera),
    ], [
        Event(Events.AztecDonkeySwitch, lambda l: l.hasMoveSwitchsanity(Switches.AztecQuicksandSwitch, False, Levels.AngryAztec, 1)),
        Event(Events.AztecLlamaSpit, lambda l: l.CanLlamaSpit()),
        Event(Events.LlamaW1aTagged, lambda _: True),
        Event(Events.LlamaW1bTagged, lambda _: True),
        Event(Events.LlamaW2aTagged, lambda _: True),
    ], [
        TransitionFront(Regions.AngryAztecMain, lambda _: True, Transitions.AztecLlamaToMain),
        TransitionFront(Regions.LlamaTempleMatching, lambda l: (l.grape and l.islanky) or l.CanPhase()),
        TransitionFront(Regions.LlamaTempleBack, lambda l: (l.mini and l.istiny) or l.CanPhase() or l.ledgeclip or l.CanOStandTBSNoclip()),
    ]),

    Regions.LlamaTempleMatching: Region("Llama Temple Matching", HintRegion.LlamaTemple, Levels.AngryAztec, False, -1, [
        LocationLogic(Locations.AztecLankyMatchingGame, lambda l: l.grape and l.CanSlamSwitch(Levels.AngryAztec, 1) and l.lanky),
        LocationLogic(Locations.AztecLlamaEnemy_Matching0, lambda _: True),
        LocationLogic(Locations.AztecLlamaEnemy_Matching1, lambda _: True),
        LocationLogic(Locations.KremKap_AztecLlamaEnemy_Matching0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_AztecLlamaEnemy_Matching1, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.LlamaTemple, lambda _: True),
    ]),

    Regions.LlamaTempleBack: Region("Llama Temple Back", HintRegion.LlamaTemple, Levels.AngryAztec, False, -1, [
        LocationLogic(Locations.AztecTinyLlamaTemple, lambda l: l.CanSlamSwitch(Levels.AngryAztec, 1) and l.istiny),
        LocationLogic(Locations.AztecKasplatLlamaTemple, lambda l: not l.settings.kasplat_rando),
    ], [
        Event(Events.LlamaW2bTagged, lambda _: True),
    ], [
        TransitionFront(Regions.LlamaTemple, lambda _: True),
    ]),

    Regions.AztecBossLobby: Region("Aztec Boss Lobby", HintRegion.Bosses, Levels.AngryAztec, True, None, [], [], [
        TransitionFront(Regions.AztecBoss, lambda l: l.IsBossReachable(Levels.AngryAztec)),
    ]),

    Regions.AztecBoss: Region("Aztec Boss", HintRegion.Bosses, Levels.AngryAztec, False, None, [
        LocationLogic(Locations.AztecKey, lambda l: l.IsBossBeatable(Levels.AngryAztec)),
    ], [], []),
}
