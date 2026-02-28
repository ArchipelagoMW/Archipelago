# fmt: off
"""Logic file for Hideout Helm."""

from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.MinigameType import MinigameType
from randomizer.Enums.Regions import Regions
from randomizer.Enums.HintRegion import HintRegion
from randomizer.Enums.Settings import HelmSetting, RemovedBarriersSelected
from randomizer.Enums.Transitions import Transitions
from randomizer.LogicClasses import (Event, LocationLogic, Region,
                                     TransitionFront)

LogicRegions = {
    # This region serves to set up Helm and send the player to the right location based on the settings
    Regions.HideoutHelmEntry: Region("Hideout Helm Entry Redirect", HintRegion.Helm, Levels.HideoutHelm, False, None, [
        LocationLogic(Locations.HelmDonkey1, lambda l: not l.settings.helm_donkey or l.settings.helm_setting == HelmSetting.skip_all),
        LocationLogic(Locations.HelmDonkey2, lambda l: not l.settings.helm_donkey or l.settings.helm_setting == HelmSetting.skip_all),
        LocationLogic(Locations.HelmChunky1, lambda l: not l.settings.helm_chunky or l.settings.helm_setting == HelmSetting.skip_all),
        LocationLogic(Locations.HelmChunky2, lambda l: not l.settings.helm_chunky or l.settings.helm_setting == HelmSetting.skip_all),
        LocationLogic(Locations.HelmTiny1, lambda l: not l.settings.helm_tiny or l.settings.helm_setting == HelmSetting.skip_all),
        LocationLogic(Locations.HelmTiny2, lambda l: not l.settings.helm_tiny or l.settings.helm_setting == HelmSetting.skip_all),
        LocationLogic(Locations.HelmLanky1, lambda l: not l.settings.helm_lanky or l.settings.helm_setting == HelmSetting.skip_all),
        LocationLogic(Locations.HelmLanky2, lambda l: not l.settings.helm_lanky or l.settings.helm_setting == HelmSetting.skip_all),
        LocationLogic(Locations.HelmDiddy1, lambda l: not l.settings.helm_diddy or l.settings.helm_setting == HelmSetting.skip_all),
        LocationLogic(Locations.HelmDiddy2, lambda l: not l.settings.helm_diddy or l.settings.helm_setting == HelmSetting.skip_all),
    ], [
        Event(Events.HelmDoorsOpened, lambda l: l.checkBarrier(RemovedBarriersSelected.helm_star_gates)),
        Event(Events.HelmGatesPunched, lambda l: l.checkBarrier(RemovedBarriersSelected.helm_punch_gates) and Events.HelmDoorsOpened in l.Events),
        Event(Events.HelmFinished, lambda l: l.settings.helm_setting == HelmSetting.skip_all),
    ], [
        # These transitions route you to where the loading zone entering Helm will take you
        # If we must turn off the Blast-O-Matic, also prevent the fill from entering Helm without Snide
        TransitionFront(Regions.HideoutHelmStart, lambda l: l.settings.helm_setting == HelmSetting.default and l.canAccessHelm()),
        TransitionFront(Regions.HideoutHelmMain, lambda l: l.settings.helm_setting == HelmSetting.skip_start and l.canAccessHelm()),
        TransitionFront(Regions.HideoutHelmAfterBoM, lambda l: l.settings.helm_setting == HelmSetting.skip_all),
        TransitionFront(Regions.HideoutHelmLobbyPastVines, lambda l: Events.HelmFinished in l.Events, Transitions.HelmToIsles),
    ]),

    Regions.HideoutHelmStart: Region("Hideout Helm Start", HintRegion.Helm, Levels.HideoutHelm, True, None, [
        LocationLogic(Locations.HelmMainEnemy_Start0, lambda _: True),
        LocationLogic(Locations.HelmMainEnemy_Start1, lambda _: True),
        LocationLogic(Locations.KremKap_HelmMainEnemy_Start0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_HelmMainEnemy_Start1, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.HideoutHelmSwitchRoom, lambda l: (l.handstand and l.islanky) or l.slope_resets),
        TransitionFront(Regions.HideoutHelmAfterBoM, lambda l: l.settings.helm_setting == HelmSetting.skip_all or Events.HelmFinished in l.Events),  # W1
    ]),

    Regions.HideoutHelmSwitchRoom: Region("Hideout Helm Start", HintRegion.Helm, Levels.HideoutHelm, True, -1, [
        LocationLogic(Locations.HelmMainEnemy_Hill, lambda _: True),
        LocationLogic(Locations.HelmMainEnemy_SwitchRoom0, lambda _: True),
        LocationLogic(Locations.HelmMainEnemy_SwitchRoom1, lambda _: True),
        LocationLogic(Locations.KremKap_HelmMainEnemy_Hill, lambda l: l.camera),
        LocationLogic(Locations.KremKap_HelmMainEnemy_SwitchRoom0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_HelmMainEnemy_SwitchRoom1, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.HideoutHelmStart, lambda _: True),
        TransitionFront(Regions.HideoutHelmMiniRoom, lambda l: l.pineapple and l.chunky and l.can_use_vines),
        TransitionFront(Regions.HideoutHelmOOBChunky, lambda l: l.CanMoonkick() or l.CanPhase() or l.CanOStandTBSNoclip())
    ]),

    Regions.HideoutHelmMiniRoom: Region("Hideout Helm Start", HintRegion.Helm, Levels.HideoutHelm, True, -1, [
        LocationLogic(Locations.HelmMainEnemy_MiniRoom0, lambda _: True),
        LocationLogic(Locations.HelmMainEnemy_MiniRoom1, lambda _: True),
        LocationLogic(Locations.HelmMainEnemy_MiniRoom2, lambda _: True),
        LocationLogic(Locations.HelmMainEnemy_MiniRoom3, lambda _: True),
        LocationLogic(Locations.KremKap_HelmMainEnemy_MiniRoom0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_HelmMainEnemy_MiniRoom1, lambda l: l.camera),
        LocationLogic(Locations.KremKap_HelmMainEnemy_MiniRoom2, lambda l: l.camera),
        LocationLogic(Locations.KremKap_HelmMainEnemy_MiniRoom3, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.HideoutHelmMain, lambda l: l.istiny and l.mini),
        TransitionFront(Regions.HideoutHelmOOBChunky, lambda l: (l.generalclips and l.ischunky) or l.CanPhase() or l.CanOStandTBSNoclip()),
    ]),

    Regions.HideoutHelmMain: Region("Hideout Helm Main", HintRegion.Helm, Levels.HideoutHelm, True, -1, [
        LocationLogic(Locations.HelmBattleArena, lambda l: not l.settings.crown_placement_rando and l.jetpack and l.isdiddy and Events.HelmFinished in l.Events),
    ], [
        Event(Events.HelmDoorsOpened, lambda l: l.grab and l.donkey and l.jetpack and l.diddy),
        Event(Events.HelmGatesPunched, lambda l: Events.HelmDoorsOpened in l.Events and l.chunky and l.punch),
        Event(Events.HelmDonkeyDone, lambda l: l.HelmDonkey1 and l.HelmDonkey2),
        Event(Events.HelmChunkyDone, lambda l: l.HelmChunky1 and l.HelmChunky2),
        Event(Events.HelmTinyDone, lambda l: l.HelmTiny1 and l.HelmTiny2),
        Event(Events.HelmLankyDone, lambda l: l.HelmLanky1 and l.HelmLanky2),
        Event(Events.HelmDiddyDone, lambda l: l.HelmDiddy1 and l.HelmDiddy2),
        Event(Events.HelmFinished, lambda l: Events.HelmDonkeyDone in l.Events and Events.HelmChunkyDone in l.Events and Events.HelmTinyDone in l.Events and Events.HelmLankyDone in l.Events and Events.HelmDiddyDone in l.Events),
    ], [
        TransitionFront(Regions.HideoutHelmDonkeyRoom, lambda l: l.bongos and l.isdonkey and l.isPriorHelmComplete(Kongs.donkey) and Events.HelmGatesPunched in l.Events),
        TransitionFront(Regions.HideoutHelmChunkyRoom, lambda l: l.triangle and l.ischunky and l.isPriorHelmComplete(Kongs.chunky) and Events.HelmGatesPunched in l.Events),
        TransitionFront(Regions.HideoutHelmTinyRoom, lambda l: l.saxophone and l.istiny and l.isPriorHelmComplete(Kongs.tiny) and Events.HelmGatesPunched in l.Events),
        TransitionFront(Regions.HideoutHelmLankyRoom, lambda l: l.trombone and l.islanky and l.isPriorHelmComplete(Kongs.lanky) and Events.HelmGatesPunched in l.Events),
        TransitionFront(Regions.HideoutHelmDiddyRoom, lambda l: l.guitar and l.jetpack and l.isdiddy and l.isPriorHelmComplete(Kongs.diddy) and Events.HelmDoorsOpened in l.Events),
        TransitionFront(Regions.HideoutHelmAfterBoM, lambda l: Events.HelmFinished in l.Events),
        TransitionFront(Regions.HideoutHelmOOBChunky, lambda l: l.CanPhase() or l.CanOStandTBSNoclip()),
        TransitionFront(Regions.HideoutHelmOOBLanky, lambda l: l.CanPhase()),
    ]),

    Regions.HideoutHelmDonkeyRoom: Region("Hideout Helm Main", HintRegion.Helm, Levels.HideoutHelm, False, -1, [
        LocationLogic(Locations.HelmDonkey1, lambda _: True, MinigameType.HelmBarrelSecond),
        LocationLogic(Locations.HelmDonkey2, lambda _: True, MinigameType.HelmBarrelFirst),
        LocationLogic(Locations.HelmDonkeyMedal, lambda l: Events.HelmDonkeyDone in l.Events and l.isdonkey),
        LocationLogic(Locations.HelmMainEnemy_DKRoom, lambda _: True),
        LocationLogic(Locations.KremKap_HelmMainEnemy_DKRoom, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.HideoutHelmMain, lambda _: True),
        TransitionFront(Regions.HideoutHelmOOBChunky, lambda l: l.CanPhase() or (l.isdonkey and l.generalclips)),
    ]),

    Regions.HideoutHelmChunkyRoom: Region("Hideout Helm Main", HintRegion.Helm, Levels.HideoutHelm, False, -1, [
        LocationLogic(Locations.HelmChunky1, lambda _: True, MinigameType.HelmBarrelFirst),
        LocationLogic(Locations.HelmChunky2, lambda _: True, MinigameType.HelmBarrelSecond),
        LocationLogic(Locations.HelmChunkyMedal, lambda l: Events.HelmChunkyDone in l.Events and l.ischunky),
        LocationLogic(Locations.HelmMainEnemy_ChunkyRoom0, lambda _: True),
        LocationLogic(Locations.HelmMainEnemy_ChunkyRoom1, lambda _: True),
        LocationLogic(Locations.KremKap_HelmMainEnemy_ChunkyRoom0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_HelmMainEnemy_ChunkyRoom1, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.HideoutHelmMain, lambda _: True),
        TransitionFront(Regions.HideoutHelmOOBChunky, lambda l: l.CanPhase()),
    ]),

    Regions.HideoutHelmTinyRoom: Region("Hideout Helm Main", HintRegion.Helm, Levels.HideoutHelm, False, -1, [
        LocationLogic(Locations.HelmTiny1, lambda _: True, MinigameType.HelmBarrelSecond),
        LocationLogic(Locations.HelmTiny2, lambda _: True, MinigameType.HelmBarrelFirst),
        LocationLogic(Locations.HelmTinyMedal, lambda l: Events.HelmTinyDone in l.Events and l.istiny),
        LocationLogic(Locations.HelmMainEnemy_TinyRoom, lambda _: True),
        LocationLogic(Locations.KremKap_HelmMainEnemy_TinyRoom, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.HideoutHelmMain, lambda _: True),
        TransitionFront(Regions.HideoutHelmOOBChunky, lambda l: l.CanPhase()),
    ]),

    Regions.HideoutHelmLankyRoom: Region("Hideout Helm Main", HintRegion.Helm, Levels.HideoutHelm, False, -1, [
        LocationLogic(Locations.HelmLanky1, lambda _: True, MinigameType.HelmBarrelFirst),
        LocationLogic(Locations.HelmLanky2, lambda _: True, MinigameType.HelmBarrelSecond),
        LocationLogic(Locations.HelmLankyMedal, lambda l: Events.HelmLankyDone in l.Events and l.islanky),
        LocationLogic(Locations.HelmMainEnemy_LankyRoom0, lambda _: True),
        LocationLogic(Locations.HelmMainEnemy_LankyRoom1, lambda _: True),
        LocationLogic(Locations.KremKap_HelmMainEnemy_LankyRoom0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_HelmMainEnemy_LankyRoom1, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.HideoutHelmMain, lambda _: True),
        TransitionFront(Regions.HideoutHelmOOBLanky, lambda l: l.CanPhase()),
    ]),

    Regions.HideoutHelmDiddyRoom: Region("Hideout Helm Main", HintRegion.Helm, Levels.HideoutHelm, False, -1, [
        LocationLogic(Locations.HelmDiddy1, lambda _: True, MinigameType.HelmBarrelFirst),
        LocationLogic(Locations.HelmDiddy2, lambda _: True, MinigameType.HelmBarrelSecond),
        LocationLogic(Locations.HelmDiddyMedal, lambda l: Events.HelmDiddyDone in l.Events and l.isdiddy),
        LocationLogic(Locations.HelmMainEnemy_DiddyRoom0, lambda _: True),
        LocationLogic(Locations.HelmMainEnemy_DiddyRoom1, lambda _: True),
        LocationLogic(Locations.KremKap_HelmMainEnemy_DiddyRoom0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_HelmMainEnemy_DiddyRoom1, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.HideoutHelmMain, lambda _: True),
        TransitionFront(Regions.HideoutHelmOOBLanky, lambda l: l.CanPhase()),
    ]),

    Regions.HideoutHelmAfterBoM: Region("Hideout Helm Navigation Room", HintRegion.Helm, Levels.HideoutHelm, False, -1, [
        LocationLogic(Locations.HelmMainEnemy_NavRight, lambda l: Events.HelmFinished in l.Events),
        LocationLogic(Locations.HelmMainEnemy_NavLeft, lambda l: Events.HelmFinished in l.Events),
        LocationLogic(Locations.KremKap_HelmMainEnemy_NavRight, lambda l: l.camera and Events.HelmFinished in l.Events),
        LocationLogic(Locations.KremKap_HelmMainEnemy_NavLeft, lambda l: l.camera and Events.HelmFinished in l.Events),
    ], [], [
        TransitionFront(Regions.HideoutHelmStart, lambda _: True),  # W1 is always pre-activated
        TransitionFront(Regions.HideoutHelmMain, lambda l: Events.HelmFinished in l.Events),
        TransitionFront(Regions.HideoutHelmThroneRoom, lambda l: l.CrownDoorOpened()),
        TransitionFront(Regions.HideoutHelmOOBLanky, lambda l: l.generalclips or l.CanPhase()),
    ]),

    Regions.HideoutHelmThroneRoom: Region("Hideout Helm Throne Room", HintRegion.Helm, Levels.HideoutHelm, False, None, [], [], [
        TransitionFront(Regions.HideoutHelmAfterBoM, lambda l: l.CrownDoorOpened()),
        TransitionFront(Regions.HideoutHelmKeyRoom, lambda l: l.CoinDoorOpened()),
        TransitionFront(Regions.HideoutHelmOOBLanky, lambda l: l.CanPhase()),
    ]),

    Regions.HideoutHelmKeyRoom: Region("Hideout Helm Key Room", HintRegion.Helm, Levels.HideoutHelm, False, None, [
        LocationLogic(Locations.HelmKey, lambda _: True),
        LocationLogic(Locations.HelmBananaFairy1, lambda l: l.camera),
        LocationLogic(Locations.HelmBananaFairy2, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.HideoutHelmOOBLanky, lambda l: l.CanPhase()),
    ]),

    Regions.HideoutHelmOOBChunky: Region("Hideout Helm OOB (Chunky Room Elevation)", HintRegion.Helm, Levels.HideoutHelm, False, -1, [], [], [
        TransitionFront(Regions.HideoutHelmStart, lambda _: True),
        TransitionFront(Regions.HideoutHelmSwitchRoom, lambda _: True),
        TransitionFront(Regions.HideoutHelmMiniRoom, lambda _: True),
        TransitionFront(Regions.HideoutHelmMain, lambda _: True),
        TransitionFront(Regions.HideoutHelmDonkeyRoom, lambda _: True),
        TransitionFront(Regions.HideoutHelmChunkyRoom, lambda _: True),
        TransitionFront(Regions.HideoutHelmTinyRoom, lambda _: True),
        TransitionFront(Regions.HideoutHelmAfterBoM, lambda _: True),
        TransitionFront(Regions.HideoutHelmThroneRoom, lambda _: True),
        TransitionFront(Regions.HideoutHelmOOBLanky, lambda l: l.isdiddy or l.istiny),
    ]),

    Regions.HideoutHelmOOBLanky: Region("Hideout Helm OOB (Lanky Room Elevation)", HintRegion.Helm, Levels.HideoutHelm, False, -1, [], [], [
        TransitionFront(Regions.HideoutHelmOOBChunky, lambda _: True),
        TransitionFront(Regions.HideoutHelmLankyRoom, lambda _: True),
        TransitionFront(Regions.HideoutHelmDiddyRoom, lambda l: l.isdiddy or l.istiny),
        TransitionFront(Regions.HideoutHelmAfterBoM, lambda _: True),
        TransitionFront(Regions.HideoutHelmThroneRoom, lambda _: True),
        TransitionFront(Regions.HideoutHelmKeyRoom, lambda _: True),
    ]),
}
