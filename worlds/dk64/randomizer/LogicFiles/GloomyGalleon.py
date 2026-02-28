# fmt: off
"""Logic file for Gloomy Galleon."""

from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Maps import Maps
from randomizer.Enums.MinigameType import MinigameType
from randomizer.Enums.Regions import Regions
from randomizer.Enums.HintRegion import HintRegion
from randomizer.Enums.Settings import GalleonWaterSetting, RemovedBarriersSelected
from randomizer.Enums.Switches import Switches
from randomizer.Enums.Transitions import Transitions
from randomizer.LogicClasses import (Event, LocationLogic, Region,
                                     TransitionFront)

LogicRegions = {
    Regions.GloomyGalleonMedals: Region("Gloomy Galleon Medals", HintRegion.GalleonCBs, Levels.GloomyGalleon, False, None, [
        LocationLogic(Locations.GalleonDonkeyMedal, lambda l: l.ColoredBananas[Levels.GloomyGalleon][Kongs.donkey] >= l.settings.medal_cb_req_level[3]),
        LocationLogic(Locations.GalleonDiddyMedal, lambda l: l.ColoredBananas[Levels.GloomyGalleon][Kongs.diddy] >= l.settings.medal_cb_req_level[3]),
        LocationLogic(Locations.GalleonLankyMedal, lambda l: l.ColoredBananas[Levels.GloomyGalleon][Kongs.lanky] >= l.settings.medal_cb_req_level[3]),
        LocationLogic(Locations.GalleonTinyMedal, lambda l: l.ColoredBananas[Levels.GloomyGalleon][Kongs.tiny] >= l.settings.medal_cb_req_level[3]),
        LocationLogic(Locations.GalleonChunkyMedal, lambda l: l.ColoredBananas[Levels.GloomyGalleon][Kongs.chunky] >= l.settings.medal_cb_req_level[3]),
        LocationLogic(Locations.GalleonDonkeyHalfMedal, lambda l: l.ColoredBananas[Levels.GloomyGalleon][Kongs.donkey] >= max(1, int(l.settings.medal_cb_req_level[3] >> 1))),
        LocationLogic(Locations.GalleonDiddyHalfMedal, lambda l: l.ColoredBananas[Levels.GloomyGalleon][Kongs.diddy] >= max(1, int(l.settings.medal_cb_req_level[3] >> 1))),
        LocationLogic(Locations.GalleonLankyHalfMedal, lambda l: l.ColoredBananas[Levels.GloomyGalleon][Kongs.lanky] >= max(1, int(l.settings.medal_cb_req_level[3] >> 1))),
        LocationLogic(Locations.GalleonTinyHalfMedal, lambda l: l.ColoredBananas[Levels.GloomyGalleon][Kongs.tiny] >= max(1, int(l.settings.medal_cb_req_level[3] >> 1))),
        LocationLogic(Locations.GalleonChunkyHalfMedal, lambda l: l.ColoredBananas[Levels.GloomyGalleon][Kongs.chunky] >= max(1, int(l.settings.medal_cb_req_level[3] >> 1))),
    ], [], [], restart=-1),

    # This region serves to set up the entry for the level based on the DK Portal Location
    Regions.GloomyGalleonEntryHandler: Region("Gloomy Galleon Entry Handler", HintRegion.Error, Levels.GloomyGalleon, False, None, [], [
        Event(Events.GalleonEntered, lambda _: True),
    ], [
        TransitionFront(Regions.GloomyGalleonLobby, lambda _: True, Transitions.GalleonToIsles),
        TransitionFront(Regions.GloomyGalleonStart, lambda _: True),  # Don't move this away from index 1 (ShuffleDoors.py relies on this being index 1)
    ], restart=-1),

    Regions.GloomyGalleonStart: Region("Gloomy Galleon Start", HintRegion.GalleonCaverns, Levels.GloomyGalleon, True, None, [
        LocationLogic(Locations.GalleonChunkyChest, lambda l: l.punch and l.chunky),
        LocationLogic(Locations.GalleonBattleArena, lambda l: (not l.settings.crown_placement_rando and ((l.punch and l.chunky) or l.CanPhase() or l.CanSkew(False, False)))),
        LocationLogic(Locations.GalleonBananaFairybyCranky, lambda l: l.camera and l.punch and l.chunky),
        LocationLogic(Locations.GalleonMainEnemy_ChestRoom0, lambda _: True),
        LocationLogic(Locations.GalleonMainEnemy_ChestRoom1, lambda _: True),
        LocationLogic(Locations.GalleonMainEnemy_NearVineCannon, lambda _: True),
        LocationLogic(Locations.GalleonMainEnemy_CrankyCannon, lambda _: True),
        LocationLogic(Locations.GalleonMainEnemy_PeanutTunnel, lambda _: True),
        LocationLogic(Locations.GalleonMainEnemy_CoconutTunnel, lambda _: True),
        LocationLogic(Locations.KremKap_GalleonMainEnemy_ChestRoom0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_GalleonMainEnemy_ChestRoom1, lambda l: l.camera),
        LocationLogic(Locations.KremKap_GalleonMainEnemy_NearVineCannon, lambda l: l.camera),
        LocationLogic(Locations.KremKap_GalleonMainEnemy_CrankyCannon, lambda l: l.camera),
        LocationLogic(Locations.KremKap_GalleonMainEnemy_PeanutTunnel, lambda l: l.camera),
        LocationLogic(Locations.KremKap_GalleonMainEnemy_CoconutTunnel, lambda l: l.camera),
    ], [
        Event(Events.GalleonLankySwitch, lambda l: l.CanSlamSwitch(Levels.GloomyGalleon, 1) and l.lanky and (l.swim or l.galleonGatesStayOpen())),
        Event(Events.GalleonTinySwitch, lambda l: l.CanSlamSwitch(Levels.GloomyGalleon, 1) and l.tiny and (l.swim or l.galleonGatesStayOpen())),
        Event(Events.LighthouseGateOpened, lambda l: l.hasMoveSwitchsanity(Switches.GalleonLighthouse, False)),
        Event(Events.ShipyardGateOpened, lambda l: l.hasMoveSwitchsanity(Switches.GalleonShipwreck, False)),
        Event(Events.GalleonCannonRoomOpened, lambda l: l.hasMoveSwitchsanity(Switches.GalleonCannonGame, False)),
        Event(Events.GalleonW1aTagged, lambda _: True),
        Event(Events.GalleonW2aTagged, lambda _: True),
        Event(Events.WaterLowered, lambda l: l.settings.galleon_water_internal == GalleonWaterSetting.lowered),
        Event(Events.WaterRaised, lambda l: l.settings.galleon_water_internal == GalleonWaterSetting.raised),
    ], [
        TransitionFront(Regions.GalleonPastVines, lambda l: l.can_use_vines or l.CanMoonkick()),
        TransitionFront(Regions.GalleonBeyondPineappleGate, lambda l: Events.GalleonCannonRoomOpened in l.Events or l.CanPhase() or l.CanSkew(False, False) or (l.CanPhaseswim() and Events.WaterRaised in l.Events)),
        TransitionFront(Regions.LighthouseSurface, lambda l: l.checkBarrier(RemovedBarriersSelected.galleon_lighthouse_gate) or Events.LighthouseGateOpened in l.Events or l.CanPhase() or l.CanSkew(False, False)),
        TransitionFront(Regions.Shipyard, lambda l: (l.checkBarrier(RemovedBarriersSelected.galleon_shipyard_area_gate) or Events.ShipyardGateOpened in l.Events or l.CanPhase() or l.CanSkew(False, False) or (l.CanPhaseswim() and Events.WaterRaised in l.Events)) and (not l.IsLavaWater() or l.Melons >= 2)),
        TransitionFront(Regions.CrankyGalleon, lambda l: l.crankyAccess),
    ]),

    Regions.GalleonPastVines: Region("Galleon Past Vines", HintRegion.GalleonCaverns, Levels.GloomyGalleon, False, None, [
        LocationLogic(Locations.GalleonKasplatNearLab, lambda l: not l.settings.kasplat_rando),
    ], [
        Event(Events.GalleonW3aTagged, lambda _: True),
    ], [
        TransitionFront(Regions.GloomyGalleonStart, lambda _: True),
        TransitionFront(Regions.GalleonBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.GalleonBeyondPineappleGate: Region("Galleon Beyond Pineapple Gate", HintRegion.GalleonCaverns, Levels.GloomyGalleon, False, None, [
        LocationLogic(Locations.GalleonChunkyCannonGame, lambda l: l.CanGetOnCannonGamePlatform() and l.ischunky and l.barrels),
        LocationLogic(Locations.GalleonKasplatCannons, lambda l: not l.settings.kasplat_rando and l.CanGetOnCannonGamePlatform()),
    ], [], [
        TransitionFront(Regions.GloomyGalleonStart, lambda l: Events.GalleonCannonRoomOpened in l.Events or l.CanPhaseswim() or (l.CanPhase() and l.CanGetOnCannonGamePlatform())),
        TransitionFront(Regions.Shipyard, lambda l: (l.CanPhaseswim() or (l.CanPhase() and l.CanGetOnCannonGamePlatform())) and (not l.IsLavaWater() or l.Melons >= 2)),
    ]),

    Regions.LighthouseSurface: Region("Lighthouse Surface", HintRegion.Lighthouse, Levels.GloomyGalleon, False, None, [
        LocationLogic(Locations.GalleonKasplatLighthouseArea, lambda l: not l.settings.kasplat_rando),
    ], [
        Event(Events.GalleonChunkyPad, lambda l: (l.triangle and l.chunky) and (l.swim or l.galleonGatesStayOpen()) and Events.WaterLowered in l.Events),
        Event(Events.WaterLowered, lambda l: l.settings.galleon_water_internal == GalleonWaterSetting.lowered),
        Event(Events.WaterRaised, lambda l: l.settings.galleon_water_internal == GalleonWaterSetting.raised),
    ], [
        TransitionFront(Regions.GloomyGalleonStart, lambda l: Events.LighthouseGateOpened in l.Events),
        TransitionFront(Regions.LighthouseUnderwater, lambda l: l.swim and (not l.IsLavaWater() or l.Melons >= 3)),
        TransitionFront(Regions.LighthousePlatform, lambda l: Events.WaterRaised in l.Events or (l.monkey_maneuvers and (l.islanky or l.ischunky))),
        TransitionFront(Regions.LighthouseSnideAlcove, lambda l: Events.WaterRaised in l.Events or (l.monkey_maneuvers and (l.islanky or l.ischunky))),
        TransitionFront(Regions.GalleonBeyondPineappleGate, lambda l: l.CanPhaseswim()),
    ]),

    Regions.LighthousePlatform: Region("Lighthouse Platform", HintRegion.Lighthouse, Levels.GloomyGalleon, False, None, [
        LocationLogic(Locations.GalleonDiddyShipSwitch, lambda l: Events.ActivatedLighthouse in l.Events and l.jetpack and l.CanSlamSwitch(Levels.GloomyGalleon, 1) and l.isdiddy),
    ], [
        Event(Events.MechafishSummoned, lambda l: l.jetpack and l.guitar and l.canTravelToMechFish() and l.isdiddy),
        Event(Events.GalleonW1bTagged, lambda _: True),
        Event(Events.GalleonW5aTagged, lambda _: True),
    ], [
        TransitionFront(Regions.LighthouseSurface, lambda _: True),
        # Rare case of needing to open gate before being able to go through backwards
        TransitionFront(Regions.Lighthouse, lambda l: ((l.CanSlamSwitch(Levels.GloomyGalleon, 1) and l.isdonkey) or l.generalclips) and l.climbing, Transitions.GalleonLighthouseAreaToLighthouse),
        TransitionFront(Regions.SickBay, lambda l: Events.ActivatedLighthouse in l.Events and l.Slam and l.ischunky, Transitions.GalleonLighthouseAreaToSickBay),
        TransitionFront(Regions.GalleonBaboonBlast, lambda l: l.blast and l.isdonkey)  # , Transitions.GalleonMainToBBlast)
    ]),

    Regions.LighthouseUnderwater: Region("Lighthouse Underwater", HintRegion.Lighthouse, Levels.GloomyGalleon, True, None, [
        LocationLogic(Locations.GalleonLankyEnguardeChest, lambda l: Events.LighthouseEnguarde in l.Events and l.lanky),
    ], [
        Event(Events.WaterLowered, lambda _: True),
        Event(Events.WaterRaised, lambda _: True),
        Event(Events.LighthouseEnguarde, lambda l: l.lanky),
    ], [
        TransitionFront(Regions.LighthouseSurface, lambda _: True),
        TransitionFront(Regions.LighthouseEnguardeDoor, lambda l: Events.LighthouseEnguarde in l.Events or l.CanPhaseswim()),
        TransitionFront(Regions.MermaidRoom, lambda l: (l.mini and l.istiny) or l.CanPhaseswim(), Transitions.GalleonLighthouseAreaToMermaid),
        TransitionFront(Regions.GalleonBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.LighthouseEnguardeDoor: Region("Lighthouse Enguarde Door", HintRegion.Lighthouse, Levels.GloomyGalleon, False, None, [], [], [
        TransitionFront(Regions.LighthouseUnderwater, lambda _: True),
        TransitionFront(Regions.GalleonBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.LighthouseSnideAlcove: Region("Lighthouse Snide Alcove", HintRegion.Lighthouse, Levels.GloomyGalleon, True, None, [], [
        Event(Events.GalleonW3bTagged, lambda _: True),
    ], [
        TransitionFront(Regions.LighthouseSurface, lambda _: True),
        TransitionFront(Regions.Snide, lambda l: l.snideAccess),
    ]),

    Regions.GalleonBaboonBlast: Region("Galleon Baboon Blast", HintRegion.Lighthouse, Levels.GloomyGalleon, False, None, [], [
        Event(Events.SealReleased, lambda l: l.isdonkey)
    ], [
        TransitionFront(Regions.LighthousePlatform, lambda _: True)
    ]),

    Regions.Lighthouse: Region("Lighthouse", HintRegion.Lighthouse, Levels.GloomyGalleon, False, -1, [
        LocationLogic(Locations.RainbowCoin_Location09, lambda _: True),
        LocationLogic(Locations.GalleonLighthouseEnemy_Enemy0, lambda _: True),
        LocationLogic(Locations.GalleonLighthouseEnemy_Enemy1, lambda _: True),
        LocationLogic(Locations.KremKap_GalleonLighthouseEnemy_Enemy0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_GalleonLighthouseEnemy_Enemy1, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.LighthousePlatform, lambda _: True, Transitions.GalleonLighthouseToLighthouseArea),
        TransitionFront(Regions.LighthouseAboveLadder, lambda l: l.climbing),
    ]),

    Regions.LighthouseAboveLadder: Region("Lighthouse Above Ladder", HintRegion.Lighthouse, Levels.GloomyGalleon, False, None, [
        LocationLogic(Locations.GalleonDonkeyLighthouse, lambda l: Events.ActivatedLighthouse in l.Events and (l.isdonkey or l.settings.free_trade_items)),
    ], [
        Event(Events.ActivatedLighthouse, lambda l: l.grab and l.isdonkey),
    ], [
        TransitionFront(Regions.Lighthouse, lambda _: True),
    ]),

    Regions.MermaidRoom: Region("Mermaid Room", HintRegion.Lighthouse, Levels.GloomyGalleon, False, None, [
        LocationLogic(Locations.GalleonTinyPearls, lambda l: (l.Pearls >= l.settings.mermaid_gb_pearls) and (l.istiny or l.settings.free_trade_items)),
        LocationLogic(Locations.KremKap_GalleonNPC_Mermaid, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.LighthouseUnderwater, lambda _: True, Transitions.GalleonMermaidToLighthouseArea),
    ]),

    Regions.SickBay: Region("Sick Bay", HintRegion.Lighthouse, Levels.GloomyGalleon, False, -1, [
        LocationLogic(Locations.GalleonChunkySeasick, lambda l: (l.punch and l.ischunky)),
    ], [], [
        TransitionFront(Regions.LighthousePlatform, lambda _: True, Transitions.GalleonSickBayToLighthouseArea),
    ]),

    Regions.Shipyard: Region("Shipyard", HintRegion.ShipyardOutskirts, Levels.GloomyGalleon, True, None, [
        LocationLogic(Locations.GalleonDonkeyFreetheSeal, lambda l: Events.SealReleased in l.Events and (l.isdonkey or l.settings.free_trade_items)),
        LocationLogic(Locations.GalleonKasplatNearSub, lambda l: not l.settings.kasplat_rando),
        LocationLogic(Locations.MelonCrate_Location05, lambda _: True),
        LocationLogic(Locations.KremKap_GalleonNPC_Seal, lambda l: l.camera and Events.SealReleased in l.Events),
    ], [
        Event(Events.ShipyardTreasureRoomOpened, lambda l: (Events.ShipyardEnguarde in l.Events and (Events.WaterRaised in l.Events or l.monkey_maneuvers)) or l.checkBarrier(RemovedBarriersSelected.galleon_treasure_room)),
        Event(Events.GalleonDonkeyPad, lambda l: l.bongos and l.isdonkey and (l.swim or l.galleonGatesStayOpen())),
        Event(Events.GalleonDiddyPad, lambda l: l.guitar and l.isdiddy and (l.swim or l.galleonGatesStayOpen()) and Events.WaterLowered in l.Events),
        Event(Events.GalleonLankyPad, lambda l: l.trombone and l.islanky and (l.swim or l.galleonGatesStayOpen()) and Events.WaterLowered in l.Events),
        Event(Events.GalleonTinyPad, lambda l: l.saxophone and l.istiny and (l.swim or l.galleonGatesStayOpen())),
        Event(Events.GalleonW2bTagged, lambda _: True),
        Event(Events.GalleonW4bTagged, lambda _: True),
        Event(Events.GalleonW5bTagged, lambda _: True),
        Event(Events.WaterLowered, lambda l: l.settings.galleon_water_internal == GalleonWaterSetting.lowered),
        Event(Events.WaterRaised, lambda l: l.settings.galleon_water_internal == GalleonWaterSetting.raised),
    ], [
        TransitionFront(Regions.GloomyGalleonStart, lambda l: Events.ShipyardGateOpened in l.Events),
        TransitionFront(Regions.ShipyardUnderwater, lambda l: l.swim and (not l.IsLavaWater() or l.Melons >= 3)),
        TransitionFront(Regions.SealRace, lambda l: (Events.SealReleased in l.Events and Events.WaterRaised in l.Events and l.isdonkey) or l.CanPhaseswim(), Transitions.GalleonShipyardToSeal),
        TransitionFront(Regions.CandyGalleon, lambda l: l.candyAccess),
        TransitionFront(Regions.FunkyGalleon, lambda l: l.funkyAccess),
    ]),

    Regions.ShipyardUnderwater: Region("Shipyard Underwater", HintRegion.ShipyardOutskirts, Levels.GloomyGalleon, True, None, [
        LocationLogic(Locations.KremKap_GalleonMainEnemy_Submarine, lambda l: l.camera),
        LocationLogic(Locations.KremKap_GalleonMainEnemy_5DS0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_GalleonMainEnemy_5DS1, lambda l: l.camera),
        LocationLogic(Locations.KremKap_GalleonNPC_Mechfish, lambda l: l.camera and Events.MechafishSummoned in l.Events and l.isdiddy),
    ], [
        Event(Events.ShipyardEnguarde, lambda l: l.lanky),
    ], [
        TransitionFront(Regions.Shipyard, lambda l: not l.IsLavaWater() or l.Melons >= 2),
        TransitionFront(Regions.TreasureRoom, lambda l: Events.ShipyardTreasureRoomOpened in l.Events or l.CanPhaseswim()),
        TransitionFront(Regions.Submarine, lambda l: ((l.mini or l.CanSTS()) and l.istiny) or l.CanPhaseswim(), Transitions.GalleonShipyardToSubmarine),
        TransitionFront(Regions.Mechafish, lambda l: Events.MechafishSummoned in l.Events and l.isdiddy, Transitions.GalleonShipyardToMechFish),
        TransitionFront(Regions.LankyShip, lambda l: (Events.GalleonLankySwitch in l.Events and l.islanky) or l.CanPhaseswim(), Transitions.GalleonShipyardToLanky),
        TransitionFront(Regions.TinyShip, lambda l: (Events.GalleonTinySwitch in l.Events and l.istiny) or l.CanPhaseswim(), Transitions.GalleonShipyardToTiny),
        TransitionFront(Regions.BongosShip, lambda l: (Events.GalleonDonkeyPad in l.Events and l.isdonkey) or l.CanPhaseswim(), Transitions.GalleonShipyardToBongos),
        TransitionFront(Regions.GuitarShip, lambda l: (Events.GalleonDiddyPad in l.Events and l.isdiddy) or l.CanPhaseswim(), Transitions.GalleonShipyardToGuitar),
        TransitionFront(Regions.TromboneShip, lambda l: (Events.GalleonLankyPad in l.Events and l.islanky) or l.CanPhaseswim(), Transitions.GalleonShipyardToTrombone),
        TransitionFront(Regions.SaxophoneShip, lambda l: (Events.GalleonTinyPad in l.Events and l.istiny) or l.CanPhaseswim(), Transitions.GalleonShipyardToSaxophone),
        TransitionFront(Regions.TriangleShip, lambda l: (Events.GalleonChunkyPad in l.Events and l.ischunky) or l.CanPhaseswim(), Transitions.GalleonShipyardToTriangle),
        TransitionFront(Regions.GalleonBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.SealRace: Region("Seal Race", HintRegion.ShipyardOutskirts, Levels.GloomyGalleon, False, None, [
        LocationLogic(Locations.GalleonDonkeySealRace, lambda l: l.HasEnoughRaceCoins(Maps.GalleonSealRace, Kongs.donkey, not l.settings.free_trade_items)),
    ], [], [
        TransitionFront(Regions.Shipyard, lambda l: not l.IsLavaWater() or l.Melons >= 2, Transitions.GalleonSealToShipyard),
    ], Transitions.GalleonShipyardToSeal
    ),

    Regions.TreasureRoom: Region("Treasure Room", HintRegion.TreasureRoom, Levels.GloomyGalleon, True, None, [
        LocationLogic(Locations.GalleonLankyGoldTower, lambda l: ((Events.WaterRaised in l.Events or (Events.ShipyardEnguarde in l.Events and Events.ShipyardTreasureRoomOpened in l.Events and l.monkey_maneuvers)) and l.balloon and l.islanky) or (l.CanMoonkick() and l.settings.free_trade_items), MinigameType.BonusBarrel),
    ], [
        Event(Events.WaterLowered, lambda l: l.settings.galleon_water_internal == GalleonWaterSetting.lowered),
        Event(Events.WaterRaised, lambda l: l.settings.galleon_water_internal == GalleonWaterSetting.raised),
        Event(Events.ShipyardTreasureRoomOpened, lambda l: l.checkBarrier(RemovedBarriersSelected.galleon_treasure_room)),
    ], [
        TransitionFront(Regions.ShipyardUnderwater, lambda l: (Events.ShipyardTreasureRoomOpened in l.Events or l.CanPhaseswim()) and l.swim),
        TransitionFront(Regions.TinyChest, lambda l: (l.mini and l.istiny and l.swim) or l.CanPhaseswim(), Transitions.GalleonTreasureToChest),
        TransitionFront(Regions.TreasureRoomDiddyGoldTower, lambda l: (Events.WaterRaised in l.Events and l.spring and l.diddy) or l.CanMoonkick() or (Events.ShipyardEnguarde in l.Events and Events.ShipyardTreasureRoomOpened in l.Events and l.monkey_maneuvers and l.balloon and l.islanky)),
    ]),

    Regions.TreasureRoomDiddyGoldTower: Region("Treasure Room Diddy Gold Tower", HintRegion.TreasureRoom, Levels.GloomyGalleon, False, None, [  # Deathwarp is possible without the kasplat, but you can only take fall damage once
        LocationLogic(Locations.GalleonDiddyGoldTower, lambda l: (l.spring and l.isdiddy) or (l.CanMoonkick() and l.settings.free_trade_items), MinigameType.BonusBarrel),
        LocationLogic(Locations.GalleonKasplatGoldTower, lambda l: not l.settings.kasplat_rando),
    ], [
        Event(Events.GalleonW4aTagged, lambda l: Locations.GalleonDiddyGoldTower in l.SpecialLocationsReached),
    ], [
        TransitionFront(Regions.TreasureRoom, lambda _: True)
    ]),

    Regions.TinyChest: Region("Tiny Chest", HintRegion.TreasureRoom, Levels.GloomyGalleon, False, -1, [
        LocationLogic(Locations.GalleonPearl0, lambda _: True),
        LocationLogic(Locations.GalleonPearl1, lambda _: True),
        LocationLogic(Locations.GalleonPearl2, lambda _: True),
        LocationLogic(Locations.GalleonPearl3, lambda _: True),
        LocationLogic(Locations.GalleonPearl4, lambda _: True),
    ], [], [
        TransitionFront(Regions.TreasureRoom, lambda _: True, Transitions.GalleonChestToTreasure),
    ]),

    Regions.Submarine: Region("Submarine", HintRegion.ShipyardOutskirts, Levels.GloomyGalleon, False, None, [
        LocationLogic(Locations.GalleonTinySubmarine, lambda l: l.istiny or l.settings.free_trade_items, MinigameType.BonusBarrel),
        LocationLogic(Locations.KremKap_GalleonSubEnemy_Enemy0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_GalleonSubEnemy_Enemy1, lambda l: l.camera),
        LocationLogic(Locations.KremKap_GalleonSubEnemy_Enemy2, lambda l: l.camera),
        LocationLogic(Locations.KremKap_GalleonSubEnemy_Enemy3, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.ShipyardUnderwater, lambda _: True, Transitions.GalleonSubmarineToShipyard),
    ]),

    Regions.Mechafish: Region("Mechafish", HintRegion.ShipyardOutskirts, Levels.GloomyGalleon, False, -1, [
        LocationLogic(Locations.GalleonDiddyMechafish, lambda l: l.HasGun(Kongs.diddy) or (l.settings.free_trade_items and l.HasGun(Kongs.any))),
    ], [], [
        TransitionFront(Regions.ShipyardUnderwater, lambda _: True, Transitions.GalleonMechFishToShipyard)
    ]),

    Regions.LankyShip: Region("Lanky Ship", HintRegion.ShipyardOutskirts, Levels.GloomyGalleon, False, None, [
        LocationLogic(Locations.GalleonLanky2DoorShip, lambda l: l.islanky or (l.settings.free_trade_items and l.CanPhaseswim())),
    ], [], [
        TransitionFront(Regions.ShipyardUnderwater, lambda _: True, Transitions.GalleonLankyToShipyard),
        TransitionFront(Regions.TinyShip, lambda l: l.CanPhaseswim()),
    ]),

    Regions.TinyShip: Region("Tiny Ship", HintRegion.ShipyardOutskirts, Levels.GloomyGalleon, False, None, [
        LocationLogic(Locations.GalleonTiny2DoorShip, lambda l: l.istiny or l.settings.free_trade_items, MinigameType.BonusBarrel),
        LocationLogic(Locations.KremKap_Galleon2DSEnemy_Tiny0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_Galleon2DSEnemy_Tiny1, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.ShipyardUnderwater, lambda _: True, Transitions.GalleonTinyToShipyard),
        TransitionFront(Regions.LankyShip, lambda l: l.CanPhaseswim()),
    ]),

    Regions.BongosShip: Region("Bongos Ship", HintRegion.FiveDoorShip, Levels.GloomyGalleon, False, None, [
        LocationLogic(Locations.GalleonDonkey5DoorShip, lambda l: l.isdonkey or l.settings.free_trade_items, MinigameType.BonusBarrel),
        LocationLogic(Locations.KremKap_Galleon5DSDTEnemy_DK0, lambda l: l.camera),
        LocationLogic(Locations.KremKap_Galleon5DSDTEnemy_DK1, lambda l: l.camera),
        LocationLogic(Locations.KremKap_Galleon5DSDTEnemy_DK2, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.ShipyardUnderwater, lambda _: True, Transitions.GalleonBongosToShipyard),
        TransitionFront(Regions.SaxophoneShip, lambda l: l.CanPhaseswim()),
    ]),

    Regions.GuitarShip: Region("Guitar Ship", HintRegion.FiveDoorShip, Levels.GloomyGalleon, False, None, [
        LocationLogic(Locations.GalleonDiddy5DoorShip, lambda l: l.isdiddy or l.settings.free_trade_items, MinigameType.BonusBarrel),
        LocationLogic(Locations.KremKap_Galleon5DSDLCEnemy_Diddy, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.ShipyardUnderwater, lambda _: True, Transitions.GalleonGuitarToShipyard),
        TransitionFront(Regions.TriangleShip, lambda l: l.CanPhaseswim()),
        TransitionFront(Regions.TromboneShip, lambda l: l.CanPhaseswim()),
    ]),

    Regions.TromboneShip: Region("Trombone Ship", HintRegion.FiveDoorShip, Levels.GloomyGalleon, False, None, [
        LocationLogic(Locations.GalleonLanky5DoorShip, lambda l: l.islanky or l.settings.free_trade_items),
        LocationLogic(Locations.KremKap_Galleon5DSDLCEnemy_Lanky, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.ShipyardUnderwater, lambda _: True, Transitions.GalleonTromboneToShipyard),
        TransitionFront(Regions.GuitarShip, lambda l: l.CanPhaseswim()),
        TransitionFront(Regions.TriangleShip, lambda l: l.CanPhaseswim()),
    ]),

    Regions.SaxophoneShip: Region("Saxophone Ship", HintRegion.FiveDoorShip, Levels.GloomyGalleon, False, None, [
        LocationLogic(Locations.GalleonTiny5DoorShip, lambda l: l.istiny or l.settings.free_trade_items),
        LocationLogic(Locations.GalleonBananaFairy5DoorShip, lambda l: l.camera),
        LocationLogic(Locations.KremKap_Galleon5DSDTEnemy_TinyCage, lambda l: l.camera),
        LocationLogic(Locations.KremKap_Galleon5DSDTEnemy_TinyBed, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.ShipyardUnderwater, lambda _: True, Transitions.GalleonSaxophoneToShipyard),
        TransitionFront(Regions.BongosShip, lambda l: l.CanPhaseswim()),
    ]),

    Regions.TriangleShip: Region("Triangle Ship", HintRegion.FiveDoorShip, Levels.GloomyGalleon, False, None, [
        LocationLogic(Locations.GalleonChunky5DoorShip, lambda l: l.ischunky or l.settings.free_trade_items, MinigameType.BonusBarrel),
        LocationLogic(Locations.KremKap_Galleon5DSDLCEnemy_Chunky, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.ShipyardUnderwater, lambda _: True, Transitions.GalleonTriangleToShipyard),
        TransitionFront(Regions.GuitarShip, lambda l: l.CanPhaseswim()),
        TransitionFront(Regions.TromboneShip, lambda l: l.CanPhaseswim()),
    ]),

    Regions.GalleonBossLobby: Region("Galleon Boss Lobby", HintRegion.Bosses, Levels.GloomyGalleon, True, None, [], [], [
        TransitionFront(Regions.GalleonBoss, lambda l: l.IsBossReachable(Levels.GloomyGalleon)),
    ]),

    Regions.GalleonBoss: Region("Galleon Boss", HintRegion.Bosses, Levels.GloomyGalleon, False, None, [
        LocationLogic(Locations.GalleonKey, lambda l: l.IsBossBeatable(Levels.GloomyGalleon)),
    ], [], []),
}
