from .connection_data import area_doors_unpackable
from .door_logic import canOpen
from .item_data import items_unpackable
from .logicCommon import can_bomb, can_use_pbs, lava_run
from .logic_area_shortcuts import SandLand, ServiceSector, LifeTemple, \
    SkyWorld, FireHive, PirateLab, Verdite, Geothermal, Early
from .logicInterface import AreaLogicType
from .logic_shortcut_data import (
    shootThroughWalls, breakIce, pinkDoor, missileBarrier, icePod,
    electricHyper, killGreenOrRedPirates, underwaterSuperSink
)
from .trick_data import Tricks

(
    CraterR, SunkenNestL, RuinedConcourseBL, RuinedConcourseTR, CausewayR,
    SporeFieldTR, SporeFieldBR, OceanShoreR, EleToTurbidPassageR, PileAnchorL,
    ExcavationSiteL, WestCorridorR, FoyerR, ConstructionSiteL, AlluringCenoteR,
    FieldAccessL, TransferStationR, CellarR, SubbasementFissureL,
    WestTerminalAccessL, MezzanineConcourseL, VulnarCanyonL, CanyonPassageR,
    ElevatorToCondenserL, LoadingDockSecurityAreaL, ElevatorToWellspringL,
    NorakBrookL, NorakPerimeterTR, NorakPerimeterBL, VulnarDepthsElevatorEL,
    VulnarDepthsElevatorER, HiveBurrowL, SequesteredInfernoL,
    CollapsedPassageR, MagmaPumpL, ReservoirMaintenanceTunnelR, IntakePumpR,
    ThermalReservoir1R, GeneratorAccessTunnelL, ElevatorToMagmaLakeR,
    MagmaPumpAccessR, FieryGalleryL, RagingPitL, HollowChamberR, PlacidPoolR,
    SporousNookL, RockyRidgeTrailL, TramToSuziIslandR
) = area_doors_unpackable

(
    Missile, Super, PowerBomb, Morph, GravityBoots, Speedball, Bombs, HiJump,
    Aqua, DarkVisor, Wave, SpeedBooster, Spazer, Varia, Ice, Grapple,
    MetroidSuit, Plasma, Screw, Hypercharge, Charge, Xray, SpaceJump, Energy,
    Refuel, SmallAmmo, LargeAmmo, DamageAmp, AccelCharge, SpaceJumpBoost,
    spaceDrop
) = items_unpackable


area_logic: AreaLogicType = {
    "Early": {
        # using SunkenNestL as the hub for this area, so we don't need a path from every door to every other door
        # just need at least a path with sunken nest to and from every other door in the area
        ("CraterR", "SunkenNestL"): lambda loadout: (
            (GravityBoots in loadout) and
            ((
                (SpaceJump in loadout) and (
                    (HiJump in loadout) or (SpaceJumpBoost in loadout)
                )  # 1 SJ boost enough with no hjb
            ) or (SpeedBooster in loadout) or (
                (Tricks.infinite_bomb_jump in loadout)
            ))
        ),
        ("SunkenNestL", "CraterR"): lambda loadout: (
            (GravityBoots in loadout) and
            (canOpen(CraterR) in loadout) and
            ((
                (SpaceJump in loadout) and (
                    (HiJump in loadout) or (SpaceJumpBoost in loadout)
                )  # 1 SJ boost enough with no hjb
            ) or (SpeedBooster in loadout) or (
                (Tricks.infinite_bomb_jump in loadout)
            ))
        ),
        ("SunkenNestL", "RuinedConcourseBL"): lambda loadout: (
            (GravityBoots in loadout) and
            (pinkDoor in loadout) and  # multiple
            (missileBarrier in loadout) and
            (Early.cisternAccessTunnel in loadout)
        ),
        ("SunkenNestL", "RuinedConcourseTR"): lambda loadout: (
            loadout.has_all(
                GravityBoots, pinkDoor, missileBarrier, Early.cisternAccessTunnel, Early.concourseShinespark
            )
        ),
        ("SunkenNestL", "CausewayR"): lambda loadout: (
            (GravityBoots in loadout) and
            (pinkDoor in loadout) and  # multiple
            (missileBarrier in loadout) and
            (Early.cisternAccessTunnel in loadout) and
            (Early.causeway in loadout)
        ),
        ("SunkenNestL", "SporeFieldTR"): lambda loadout: (
            (GravityBoots in loadout) and
            (pinkDoor in loadout) and  # multiple
            (missileBarrier in loadout) and
            (Early.sporeFieldEntrance in loadout)
        ),
        ("SunkenNestL", "SporeFieldBR"): lambda loadout: (
            (GravityBoots in loadout) and
            (pinkDoor in loadout) and  # multiple
            (missileBarrier in loadout) and
            ((shootThroughWalls in loadout) or (Tricks.wave_gate_glitch in loadout)) and
            (Early.sporeFieldEntrance in loadout)
        ),
        ("RuinedConcourseBL", "SunkenNestL"): lambda loadout: (
            (GravityBoots in loadout) and
            (pinkDoor in loadout) and  # multiple
            (missileBarrier in loadout) and
            (Early.cisternAccessTunnel in loadout)
        ),
        ("RuinedConcourseBL", "RuinedConcourseTR"): lambda loadout: (
            (GravityBoots in loadout) and
            (Early.concourseShinespark in loadout)
        ),
        ("RuinedConcourseBL", "CausewayR"): lambda loadout: (
            (GravityBoots in loadout) and
            (Early.causeway in loadout)
        ),
        ("RuinedConcourseTR", "SunkenNestL"): lambda loadout: (
            loadout.has_all(
                GravityBoots, pinkDoor, missileBarrier, Early.cisternAccessTunnel, Early.concourseShinespark
            )
        ),
        ("RuinedConcourseTR", "RuinedConcourseBL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Early.concourseShinespark in loadout)
        ),
        ("RuinedConcourseTR", "CausewayR"): lambda loadout: (
            (GravityBoots in loadout) and
            (Early.causeway in loadout) and
            (Early.concourseShinespark in loadout)
        ),
        ("CausewayR", "SunkenNestL"): lambda loadout: (
            (GravityBoots in loadout) and
            (pinkDoor in loadout) and  # multiple
            (missileBarrier in loadout) and
            (Early.cisternAccessTunnel in loadout) and
            (Early.causeway in loadout)
        ),
        ("CausewayR", "RuinedConcourseBL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Early.causeway in loadout)
        ),
        ("CausewayR", "RuinedConcourseTR"): lambda loadout: (
            (GravityBoots in loadout) and
            (Early.causeway in loadout) and
            (Early.concourseShinespark in loadout)
        ),
        ("SporeFieldTR", "SunkenNestL"): lambda loadout: (
            (GravityBoots in loadout) and
            (pinkDoor in loadout) and  # multiple
            (missileBarrier in loadout) and
            (Early.sporeFieldEntrance in loadout)
        ),
        ("SporeFieldTR", "RuinedConcourseBL"): lambda loadout: (
            (GravityBoots in loadout) and
            (pinkDoor in loadout) and
            (Early.sporeFieldEntrance in loadout) and
            (Early.cisternAccessTunnel in loadout)
        ),
        ("SporeFieldTR", "RuinedConcourseTR"): lambda loadout: (
            (GravityBoots in loadout) and
            (pinkDoor in loadout) and
            (Early.sporeFieldEntrance in loadout) and
            (Early.cisternAccessTunnel in loadout) and
            (Early.concourseShinespark in loadout)
        ),
        ("SporeFieldTR", "SporeFieldBR"): lambda loadout: (
            (GravityBoots in loadout) and
            ((shootThroughWalls in loadout) or (Tricks.wave_gate_glitch in loadout))
        ),
        ("SporeFieldTR", "CausewayR"): lambda loadout: (
            (GravityBoots in loadout) and
            (pinkDoor in loadout) and
            (Early.sporeFieldEntrance in loadout) and
            (Early.cisternAccessTunnel in loadout) and
            (Early.causeway in loadout)
        ),
        ("SporeFieldBR", "SunkenNestL"): lambda loadout: (
            (GravityBoots in loadout) and
            (pinkDoor in loadout) and  # multiple
            (missileBarrier in loadout) and
            ((shootThroughWalls in loadout) or (Tricks.wave_gate_glitch in loadout)) and
            (Early.sporeFieldEntrance in loadout)
        ),
        ("SporeFieldBR", "RuinedConcourseBL"): lambda loadout: (
            (GravityBoots in loadout) and
            ((shootThroughWalls in loadout) or (Tricks.wave_gate_glitch in loadout)) and
            (pinkDoor in loadout) and
            (Early.sporeFieldEntrance in loadout) and
            (Early.cisternAccessTunnel in loadout)
        ),
        ("SporeFieldBR", "RuinedConcourseTR"): lambda loadout: (
            ((shootThroughWalls in loadout) or (Tricks.wave_gate_glitch in loadout)) and
            (GravityBoots in loadout) and
            (pinkDoor in loadout) and
            (Early.sporeFieldEntrance in loadout) and
            (Early.cisternAccessTunnel in loadout) and
            (Early.concourseShinespark in loadout)
        ),
        ("SporeFieldBR", "SporeFieldTR"): lambda loadout: (
            (GravityBoots in loadout) and
            ((shootThroughWalls in loadout) or (Tricks.wave_gate_glitch in loadout))
        ),
        ("SporeFieldBR", "CausewayR"): lambda loadout: (
            ((shootThroughWalls in loadout) or (Tricks.wave_gate_glitch in loadout)) and
            (GravityBoots in loadout) and
            (pinkDoor in loadout) and
            (Early.sporeFieldEntrance in loadout) and
            (Early.cisternAccessTunnel in loadout) and
            (Early.causeway in loadout)
        ),
    },
    "SandLand": {
        ("OceanShoreR", "EleToTurbidPassageR"): lambda loadout: (
            # same as "EleToTurbidPassageR", "OceanShoreR" except door colors changed for direction
            (SandLand.turbidToSedFloor in loadout) and
            (  # door from sediment floor to turbid passage
                (Super in loadout) or
                ((underwaterSuperSink in loadout) and (pinkDoor in loadout))  # pink door to return
            ) and
            ((
                (SandLand.sedFloorToCanyon in loadout) and
                (SandLand.canyonToGreenMoon in loadout) and
                (SandLand.GreenMoonDown in loadout)  # door from shallows to canyon
            ) or (
                (SandLand.sedFloorToCanyon in loadout) and
                (SandLand.canyonToShaft in loadout) and
                (SandLand.shaftToGreenMoon in loadout)
            ) or (
                (SandLand.lowerLowerToSubCrevice in loadout) and
                (SandLand.subCreviceToSedFloor in loadout) and
                (Super in loadout) and  # door from meandering to sediment floor
                (SandLand.shaftToLowerLower in loadout) and
                ((
                    (SandLand.canyonToShaft in loadout) and
                    (SandLand.canyonToGreenMoon in loadout) and
                    (SandLand.GreenMoonDown in loadout)  # door from shallows to canyon
                ) or (
                    (SandLand.shaftToGreenMoon in loadout)
                ))
            ))
        ),
        ("EleToTurbidPassageR", "OceanShoreR"): lambda loadout: (
            # same as "OceanShoreR", "EleToTurbidPassageR" except door colors changed for direction
            (SandLand.turbidToSedFloor in loadout) and
            (pinkDoor in loadout) and  # turbid passage to sediment floor
            ((
                (SandLand.sedFloorToCanyon in loadout) and
                (SandLand.canyonToGreenMoon in loadout) and
                (can_use_pbs(1) in loadout)  # door to shallows
            ) or (
                (SandLand.sedFloorToCanyon in loadout) and
                (SandLand.canyonToShaft in loadout) and
                (SandLand.shaftToGreenMoon in loadout)
            ) or (
                (SandLand.lowerLowerToSubCrevice in loadout) and
                (SandLand.subCreviceToSedFloor in loadout) and
                (pinkDoor in loadout) and  # sediment floor to meandering
                (SandLand.shaftToLowerLower in loadout) and
                ((
                    (SandLand.canyonToShaft in loadout) and
                    (SandLand.canyonToGreenMoon in loadout) and
                    (can_use_pbs(1) in loadout)  # door to shallows
                ) or (
                    (SandLand.shaftToGreenMoon in loadout)
                ))
            ))
        ),
        ("OceanShoreR", "PileAnchorL"): lambda loadout: (
            loadout.has_all(Super, GravityBoots, Aqua, can_use_pbs(2), SpeedBooster, Grapple) and
            ((DarkVisor in loadout) or (Tricks.dark_medium in loadout))
        ),
        ("EleToTurbidPassageR", "PileAnchorL"): lambda loadout: (
            loadout.has_all(Super, GravityBoots, Aqua, can_use_pbs(2), SpeedBooster, Grapple) and
            ((DarkVisor in loadout) or (Tricks.dark_medium in loadout))
        ),
        ("PileAnchorL", "OceanShoreR"): lambda loadout: (
            loadout.has_all(Super, GravityBoots, Aqua, can_use_pbs(2), SpeedBooster, Grapple) and
            ((DarkVisor in loadout) or (Tricks.dark_medium in loadout))
        ),
        ("PileAnchorL", "EleToTurbidPassageR"): lambda loadout: (
            loadout.has_all(Super, GravityBoots, Aqua, can_use_pbs(2), SpeedBooster, Grapple) and
            ((DarkVisor in loadout) or (Tricks.dark_medium in loadout))
        ),
    },
    "PirateLab": {
        ("ExcavationSiteL", "WestCorridorR"): lambda loadout: (
            (GravityBoots in loadout) and (killGreenOrRedPirates(5) in loadout)
        ),
        ("ExcavationSiteL", "FoyerR"): lambda loadout: (
            (GravityBoots in loadout) and
            (canOpen(FoyerR) in loadout) and
            ((  # high
                (killGreenOrRedPirates(5) in loadout) and
                (PirateLab.westCorridorToCentralTop in loadout) and
                (PirateLab.centralTopToMid in loadout) and
                (PirateLab.eastCorridor in loadout)
            ) or (  # low
                (can_use_pbs(1) in loadout) and
                (PirateLab.epiphreaticIsobaric in loadout) and
                (PirateLab.centralCorridorWater in loadout) and
                (PirateLab.eastCorridor in loadout)
            ))
        ),
        ("ExcavationSiteL", "ConstructionSiteL"): lambda loadout: (
            (GravityBoots in loadout) and
            (can_use_pbs(1) in loadout) and
            (PirateLab.constructionLToElevator in loadout)
        ),
        ("ExcavationSiteL", "AlluringCenoteR"): lambda loadout: (
            (GravityBoots in loadout) and
            ((  # high
                (killGreenOrRedPirates(5) in loadout) and
                (PirateLab.westCorridorToCentralTop in loadout) and
                (PirateLab.centralTopToMid in loadout) and
                ((Screw in loadout) or (MetroidSuit in loadout)) and
                (PirateLab.cenote in loadout)
            ) or (  # low
                (can_use_pbs(1) in loadout) and
                (PirateLab.epiphreaticIsobaric in loadout) and
                (PirateLab.centralCorridorWater in loadout) and
                ((Screw in loadout) or (MetroidSuit in loadout)) and
                (PirateLab.cenote in loadout)
            ))
        ),
        ("WestCorridorR", "ExcavationSiteL"): lambda loadout: (
            (GravityBoots in loadout) and (killGreenOrRedPirates(5) in loadout)
        ),
        ("WestCorridorR", "FoyerR"): lambda loadout: (
            (GravityBoots in loadout) and
            (canOpen(FoyerR) in loadout) and
            (PirateLab.westCorridorToCentralTop in loadout) and
            (PirateLab.centralTopToMid in loadout) and
            (PirateLab.eastCorridor in loadout)
        ),
        ("WestCorridorR", "ConstructionSiteL"): lambda loadout: (
            (GravityBoots in loadout) and
            ((
                (killGreenOrRedPirates(5) in loadout) and  # needed to go right if start from corridor
                (can_use_pbs(1) in loadout)
            ) or (
                (PirateLab.westCorridorToCentralTop in loadout) and
                (PirateLab.centralTopToMid in loadout) and
                (PirateLab.centralCorridorWater in loadout) and
                (PirateLab.epiphreaticIsobaric in loadout)
            )) and
            (PirateLab.constructionLToElevator in loadout)
        ),
        ("WestCorridorR", "AlluringCenoteR"): lambda loadout: (
            (GravityBoots in loadout) and
            (PirateLab.westCorridorToCentralTop in loadout) and
            (PirateLab.centralTopToMid in loadout) and
            ((Screw in loadout) or (MetroidSuit in loadout)) and
            (PirateLab.cenote in loadout)
        ),
        ("FoyerR", "ExcavationSiteL"): lambda loadout: (
            (GravityBoots in loadout) and
            ((  # high
                (PirateLab.eastCorridor in loadout) and
                (PirateLab.centralTopToMid in loadout) and
                (PirateLab.westCorridorToCentralTop in loadout) and
                (killGreenOrRedPirates(5) in loadout)  # needed to return right even if you start from corridor
            ) or (  # low
                (can_use_pbs(1) in loadout) and
                (PirateLab.epiphreaticIsobaric in loadout) and
                (PirateLab.centralCorridorWater in loadout) and
                (PirateLab.eastCorridor in loadout)
            ))
        ),
        ("FoyerR", "WestCorridorR"): lambda loadout: (
            (GravityBoots in loadout) and
            (PirateLab.westCorridorToCentralTop in loadout) and
            (PirateLab.centralTopToMid in loadout) and
            (PirateLab.eastCorridor in loadout)
        ),
        ("FoyerR", "ConstructionSiteL"): lambda loadout: (
            (GravityBoots in loadout) and
            (PirateLab.constructionLToElevator in loadout) and
            (PirateLab.epiphreaticIsobaric in loadout) and
            (PirateLab.centralCorridorWater in loadout) and
            (PirateLab.eastCorridor in loadout)
        ),
        ("FoyerR", "AlluringCenoteR"): lambda loadout: (
            (GravityBoots in loadout) and
            (PirateLab.eastCorridor in loadout) and
            ((Screw in loadout) or (MetroidSuit in loadout)) and
            (PirateLab.cenote in loadout)
        ),
        ("ConstructionSiteL", "ExcavationSiteL"): lambda loadout: (
            (GravityBoots in loadout) and
            (PirateLab.constructionLToElevator in loadout) and
            ((  # outside
                (can_use_pbs(1) in loadout)
            ) or (  # inside
                (PirateLab.epiphreaticIsobaric in loadout) and
                (PirateLab.centralCorridorWater in loadout) and
                (PirateLab.centralTopToMid in loadout) and
                (PirateLab.westCorridorToCentralTop in loadout) and
                (killGreenOrRedPirates(5) in loadout)
            ))
        ),
        ("ConstructionSiteL", "WestCorridorR"): lambda loadout: (
            (GravityBoots in loadout) and
            (killGreenOrRedPirates(5) in loadout) and
            (can_use_pbs(1) in loadout) and
            (PirateLab.constructionLToElevator in loadout)
        ),
        ("ConstructionSiteL", "FoyerR"): lambda loadout: (
            (GravityBoots in loadout) and
            (canOpen(FoyerR) in loadout) and
            (PirateLab.eastCorridor in loadout) and
            (PirateLab.centralCorridorWater in loadout) and
            (PirateLab.epiphreaticIsobaric in loadout) and
            (PirateLab.constructionLToElevator in loadout)
        ),
        ("ConstructionSiteL", "AlluringCenoteR"): lambda loadout: (
            (GravityBoots in loadout) and
            (PirateLab.constructionLToElevator in loadout) and
            ((  # top
                (can_use_pbs(1) in loadout) and
                (killGreenOrRedPirates(5) in loadout) and
                (PirateLab.westCorridorToCentralTop in loadout) and
                (PirateLab.centralTopToMid in loadout)
            ) or (  # bottom
                (PirateLab.epiphreaticIsobaric in loadout) and
                (PirateLab.centralCorridorWater in loadout)
            )) and
            ((Screw in loadout) or (MetroidSuit in loadout)) and
            (PirateLab.cenote in loadout)
        ),
        ("AlluringCenoteR", "ExcavationSiteL"): lambda loadout: (
            (GravityBoots in loadout) and
            ((  # top
                (killGreenOrRedPirates(5) in loadout) and
                (PirateLab.westCorridorToCentralTop in loadout) and
                (PirateLab.centralTopToMid in loadout)
            ) or (  # bottom
                (can_use_pbs(1) in loadout) and
                (PirateLab.epiphreaticIsobaric in loadout) and
                (PirateLab.centralCorridorWater in loadout)
            )) and
            ((Screw in loadout) or (MetroidSuit in loadout)) and
            (PirateLab.cenote in loadout)
        ),
        ("AlluringCenoteR", "WestCorridorR"): lambda loadout: (
            (GravityBoots in loadout) and
            (PirateLab.cenote in loadout) and
            ((Screw in loadout) or (MetroidSuit in loadout)) and
            ((
                (PirateLab.centralTopToMid in loadout) and
                (PirateLab.westCorridorToCentralTop in loadout)
            ) or (
                (PirateLab.centralCorridorWater in loadout) and
                (PirateLab.epiphreaticIsobaric in loadout) and
                (can_use_pbs(1) in loadout) and
                (killGreenOrRedPirates(5) in loadout)
            ))
        ),
        ("AlluringCenoteR", "FoyerR"): lambda loadout: (
            (GravityBoots in loadout) and
            (canOpen(FoyerR) in loadout) and
            (PirateLab.eastCorridor in loadout) and
            (PirateLab.cenote in loadout) and
            ((Screw in loadout) or (MetroidSuit in loadout))
        ),
        ("AlluringCenoteR", "ConstructionSiteL"): lambda loadout: (
            (GravityBoots in loadout) and
            (PirateLab.cenote in loadout) and
            ((Screw in loadout) or (MetroidSuit in loadout)) and
            ((  # top
                (PirateLab.centralTopToMid in loadout) and
                (PirateLab.westCorridorToCentralTop in loadout) and
                (killGreenOrRedPirates(5) in loadout) and
                (can_use_pbs(1) in loadout)
            ) or (  # bottom
                (PirateLab.centralCorridorWater in loadout) and
                (PirateLab.epiphreaticIsobaric in loadout)
            )) and
            (PirateLab.constructionLToElevator in loadout)
        ),
    },
    "ServiceSector": {
        ("FieldAccessL", "TransferStationR"): lambda loadout: (
            loadout.has_all(GravityBoots,
                            ServiceSector.westSpore,
                            ServiceSector.eastSpore,
                            ServiceSector.transfer,
                            ServiceSector.transferGateRight)
        ),
        ("FieldAccessL", "CellarR"): lambda loadout: (
            (GravityBoots in loadout) and
            (ServiceSector.westSpore in loadout) and
            (ServiceSector.eastSpore in loadout) and
            (ServiceSector.crumblingBasement in loadout) and
            (Super in loadout) and  # door from crumbling basement to cellar
            (ServiceSector.cellar in loadout)
        ),
        ("FieldAccessL", "SubbasementFissureL"): lambda loadout: (
            (GravityBoots in loadout) and
            (ServiceSector.eastSpore in loadout) and
            (ServiceSector.crumblingBasement in loadout) and
            (ServiceSector.wasteProcessingTraverse in loadout) and
            (Super in loadout)
        ),
        ("TransferStationR", "FieldAccessL"): lambda loadout: (
            loadout.has_all(GravityBoots, ServiceSector.transfer, ServiceSector.eastSpore, ServiceSector.westSpore)
            # not putting shootThroughWalls in hard requirements here, don't close the door behind you
        ),
        ("TransferStationR", "CellarR"): lambda loadout: (
            (GravityBoots in loadout) and
            (ServiceSector.transfer in loadout) and
            (ServiceSector.crumblingBasement in loadout) and
            (Super in loadout) and  # door to cellar
            (ServiceSector.cellar in loadout)
        ),
        ("TransferStationR", "SubbasementFissureL"): lambda loadout: (
            (GravityBoots in loadout) and
            (ServiceSector.transfer in loadout) and
            (ServiceSector.crumblingBasement in loadout) and
            (ServiceSector.wasteProcessingTraverse in loadout) and
            (Super in loadout)  # door to exhaust vent
        ),
        ("CellarR", "FieldAccessL"): lambda loadout: (
            (GravityBoots in loadout) and
            (ServiceSector.cellar in loadout) and
            (pinkDoor in loadout) and  # cellar to crumbling
            (ServiceSector.crumblingBasement in loadout) and
            (ServiceSector.eastSpore in loadout) and
            (ServiceSector.westSpore in loadout)
        ),
        ("CellarR", "TransferStationR"): lambda loadout: (
            (GravityBoots in loadout) and
            (ServiceSector.cellar in loadout) and
            (pinkDoor in loadout) and  # cellar to crumbling
            (ServiceSector.crumblingBasement in loadout) and
            (ServiceSector.transfer in loadout) and
            (ServiceSector.transferGateRight in loadout)
        ),
        ("CellarR", "SubbasementFissureL"): lambda loadout: (
            (GravityBoots in loadout) and
            (ServiceSector.cellar in loadout) and
            (pinkDoor in loadout) and  # cellar to crumbling
            (ServiceSector.wasteProcessingTraverse in loadout) and
            (Super in loadout)  # door into exhaust vent
        ),
        ("SubbasementFissureL", "FieldAccessL"): lambda loadout: (
            (GravityBoots in loadout) and
            (can_use_pbs(1) in loadout) and  # door to waste
            (ServiceSector.wasteProcessingTraverse in loadout) and
            (ServiceSector.crumblingBasement in loadout) and
            (ServiceSector.eastSpore in loadout) and
            (ServiceSector.westSpore in loadout)
        ),
        ("SubbasementFissureL", "TransferStationR"): lambda loadout: (
            (GravityBoots in loadout) and
            (can_use_pbs(1) in loadout) and  # door to waste
            (ServiceSector.wasteProcessingTraverse in loadout) and
            (ServiceSector.crumblingBasement in loadout) and
            (ServiceSector.transfer in loadout) and
            (ServiceSector.transferGateRight in loadout)
        ),
        ("SubbasementFissureL", "CellarR"): lambda loadout: (
            (GravityBoots in loadout) and
            (can_use_pbs(1) in loadout) and  # door to waste
            (ServiceSector.wasteProcessingTraverse in loadout) and
            (Super in loadout) and  # door into cellar access
            (ServiceSector.cellar in loadout)
        ),
    },
    "SkyWorld": {
        ("WestTerminalAccessL", "MezzanineConcourseL"): lambda loadout: (
            (GravityBoots in loadout) and
            (SkyWorld.westTerminal in loadout) and
            (SkyWorld.mezzanineShaft in loadout)
        ),
        ("WestTerminalAccessL", "VulnarCanyonL"): lambda loadout: (
            (GravityBoots in loadout) and
            (SkyWorld.westTerminal in loadout) and
            (SpeedBooster in loadout) and
            (canOpen(VulnarCanyonL) in loadout) and
            (SkyWorld.crackedCliffsideCave in loadout)
        ),
        ("WestTerminalAccessL", "CanyonPassageR"): lambda loadout: (
            (GravityBoots in loadout) and
            (SkyWorld.westTerminal in loadout) and
            (SpeedBooster in loadout) and
            (SkyWorld.crackedCliffsideCave in loadout)
        ),
        ("WestTerminalAccessL", "ElevatorToCondenserL"): lambda loadout: (
            (GravityBoots in loadout) and
            (SkyWorld.westTerminal in loadout) and
            (Morph in loadout) and
            (breakIce in loadout) and
            (SkyWorld.condenser in loadout)
        ),
        ("MezzanineConcourseL", "WestTerminalAccessL"): lambda loadout: (
            (canOpen(WestTerminalAccessL) in loadout) and
            (GravityBoots in loadout) and
            (SkyWorld.mezzanineShaft in loadout) and
            (SkyWorld.westTerminal in loadout)
        ),
        ("MezzanineConcourseL", "VulnarCanyonL"): lambda loadout: (
            (GravityBoots in loadout) and
            (canOpen(VulnarCanyonL) in loadout) and
            (SkyWorld.crackedCliffsideCave in loadout) and
            (SpeedBooster in loadout)
        ),
        ("MezzanineConcourseL", "CanyonPassageR"): lambda loadout: (
            (GravityBoots in loadout) and
            (SkyWorld.crackedCliffsideCave in loadout) and
            (SpeedBooster in loadout)
        ),
        ("MezzanineConcourseL", "ElevatorToCondenserL"): lambda loadout: (
            (GravityBoots in loadout) and
            (SkyWorld.mezzanineShaft in loadout) and
            (Morph in loadout) and
            (breakIce in loadout) and
            (SkyWorld.condenser in loadout)
        ),
        ("VulnarCanyonL", "WestTerminalAccessL"): lambda loadout: (
            (GravityBoots in loadout) and
            (canOpen(WestTerminalAccessL) in loadout) and
            (SkyWorld.crackedCliffsideCave in loadout) and
            (SpeedBooster in loadout) and
            (SkyWorld.westTerminal in loadout)
        ),
        ("VulnarCanyonL", "MezzanineConcourseL"): lambda loadout: (
            (GravityBoots in loadout) and
            (SkyWorld.crackedCliffsideCave in loadout) and
            (SpeedBooster in loadout) and
            (SkyWorld.mezzanineShaft in loadout)
        ),
        ("VulnarCanyonL", "CanyonPassageR"): lambda loadout: (
            GravityBoots in loadout
        ),
        ("VulnarCanyonL", "ElevatorToCondenserL"): lambda loadout: (
            (GravityBoots in loadout) and
            (SpeedBooster in loadout) and
            (SkyWorld.crackedCliffsideCave in loadout) and
            (Morph in loadout) and
            (breakIce in loadout) and
            (SkyWorld.condenser in loadout)
        ),
        ("CanyonPassageR", "WestTerminalAccessL"): lambda loadout: (
            (GravityBoots in loadout) and
            (canOpen(WestTerminalAccessL) in loadout) and
            ((can_bomb(1) in loadout) or (Screw in loadout)) and
            (SpeedBooster in loadout) and
            (SkyWorld.westTerminal in loadout)
        ),
        ("CanyonPassageR", "MezzanineConcourseL"): lambda loadout: (
            (GravityBoots in loadout) and
            (SpeedBooster in loadout) and
            ((can_bomb(1) in loadout) or (Screw in loadout)) and
            (SkyWorld.mezzanineShaft in loadout)
        ),
        ("CanyonPassageR", "VulnarCanyonL"): lambda loadout: (
            (GravityBoots in loadout) and
            (canOpen(VulnarCanyonL) in loadout)
        ),
        ("CanyonPassageR", "ElevatorToCondenserL"): lambda loadout: (
            (GravityBoots in loadout) and
            (SpeedBooster in loadout) and
            ((can_bomb(1) in loadout) or (Screw in loadout)) and
            (Morph in loadout) and
            (breakIce in loadout) and
            (SkyWorld.condenser in loadout)
        ),
        ("ElevatorToCondenserL", "WestTerminalAccessL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Morph in loadout) and
            (breakIce in loadout) and
            (SkyWorld.condenser in loadout) and
            (canOpen(WestTerminalAccessL) in loadout) and
            (SkyWorld.westTerminal in loadout)
        ),
        ("ElevatorToCondenserL", "MezzanineConcourseL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Morph in loadout) and
            (breakIce in loadout) and
            (SkyWorld.condenser in loadout) and
            (SkyWorld.mezzanineShaft in loadout)
        ),
        ("ElevatorToCondenserL", "VulnarCanyonL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Morph in loadout) and
            (breakIce in loadout) and
            (SkyWorld.condenser in loadout) and
            ((can_bomb(1) in loadout) or (Screw in loadout)) and
            (SpeedBooster in loadout) and
            (canOpen(VulnarCanyonL) in loadout)
        ),
        ("ElevatorToCondenserL", "CanyonPassageR"): lambda loadout: (
            (GravityBoots in loadout) and
            (Morph in loadout) and
            (breakIce in loadout) and
            (SkyWorld.condenser in loadout) and
            ((can_bomb(1) in loadout) or (Screw in loadout)) and
            (SpeedBooster in loadout)
        ),
    },
    "LifeTemple": {
        ("ElevatorToWellspringL", "NorakBrookL"): lambda loadout: (
            (GravityBoots in loadout) and
            (LifeTemple.brook in loadout) and
            (LifeTemple.veranda in loadout) and
            (LifeTemple.waterToVeranda in loadout) and
            (LifeTemple.waterGardenBottom in loadout)
        ),
        ("ElevatorToWellspringL", "NorakPerimeterTR"): lambda loadout: (
            (GravityBoots in loadout) and
            (LifeTemple.veranda in loadout) and
            (LifeTemple.waterToVeranda in loadout) and
            (LifeTemple.waterGardenBottom in loadout) and
            (MetroidSuit in loadout)
        ),
        ("ElevatorToWellspringL", "NorakPerimeterBL"): lambda loadout: (
            (GravityBoots in loadout) and
            (LifeTemple.perimBL in loadout) and
            (LifeTemple.veranda in loadout) and
            (LifeTemple.waterToVeranda in loadout) and
            (LifeTemple.waterGardenBottom in loadout)
        ),
        ("NorakBrookL", "ElevatorToWellspringL"): lambda loadout: (
            (GravityBoots in loadout) and
            (LifeTemple.brook in loadout) and
            (LifeTemple.veranda in loadout) and
            (LifeTemple.waterToVeranda in loadout) and
            (LifeTemple.waterGardenBottom in loadout)
        ),
        ("NorakBrookL", "NorakPerimeterTR"): lambda loadout: (
            (GravityBoots in loadout) and
            (MetroidSuit in loadout) and
            (LifeTemple.brook in loadout)
        ),
        ("NorakBrookL", "NorakPerimeterBL"): lambda loadout: (
            (GravityBoots in loadout) and
            (LifeTemple.brook in loadout) and
            (LifeTemple.perimBL in loadout)
        ),
        ("NorakPerimeterTR", "ElevatorToWellspringL"): lambda loadout: (
            (GravityBoots in loadout) and
            (MetroidSuit in loadout) and
            (LifeTemple.veranda in loadout) and
            (LifeTemple.waterToVeranda in loadout) and
            (LifeTemple.waterGardenBottom in loadout)
        ),
        ("NorakPerimeterTR", "NorakBrookL"): lambda loadout: (
            (GravityBoots in loadout) and
            (MetroidSuit in loadout) and
            (LifeTemple.brook in loadout)
        ),
        ("NorakPerimeterTR", "NorakPerimeterBL"): lambda loadout: (
            (GravityBoots in loadout) and
            (MetroidSuit in loadout) and
            (LifeTemple.perimBL in loadout)
        ),
        ("NorakPerimeterBL", "ElevatorToWellspringL"): lambda loadout: (
            (GravityBoots in loadout) and
            (LifeTemple.perimBL in loadout) and
            (LifeTemple.veranda in loadout) and
            (LifeTemple.waterToVeranda in loadout) and
            (LifeTemple.waterGardenBottom in loadout)
        ),
        ("NorakPerimeterBL", "NorakBrookL"): lambda loadout: (
            (GravityBoots in loadout) and
            (LifeTemple.perimBL in loadout) and
            (LifeTemple.brook in loadout)
        ),
        ("NorakPerimeterBL", "NorakPerimeterTR"): lambda loadout: (
            (GravityBoots in loadout) and
            (LifeTemple.perimBL in loadout) and
            (MetroidSuit in loadout)
        ),
    },
    "FireHive": {
        ("VulnarDepthsElevatorEL", "VulnarDepthsElevatorER"): lambda loadout: (
            True  # flat hallway to walk across
        ),
        ("VulnarDepthsElevatorER", "VulnarDepthsElevatorEL"): lambda loadout: (
            True  # flat hallway to walk across
        ),
        ("VulnarDepthsElevatorER", "HiveBurrowL"): lambda loadout: (
            (GravityBoots in loadout) and
            (FireHive.hiveEntrance in loadout) and
            (FireHive.hiveBurrow in loadout)
        ),
        ("VulnarDepthsElevatorER", "SequesteredInfernoL"): lambda loadout: (
            (GravityBoots in loadout) and
            (FireHive.hiveEntrance in loadout) and
            ((icePod in loadout) or (FireHive.westHiveTunnel in loadout)) and
            (FireHive.crossways in loadout) and
            (FireHive.infernalSequestration in loadout)
        ),
        ("VulnarDepthsElevatorER", "CollapsedPassageR"): lambda loadout: (
            (GravityBoots in loadout) and
            (FireHive.hiveEntrance in loadout) and
            ((icePod in loadout) or (FireHive.westHiveTunnel in loadout)) and
            (FireHive.crossways in loadout) and
            (FireHive.crosswaysToCourtyard in loadout) and
            (Super in loadout) and  # door to ancient basin access
            (FireHive.courtyardToCollapsed in loadout)
        ),
        ("HiveBurrowL", "VulnarDepthsElevatorER"): lambda loadout: (
            (GravityBoots in loadout) and
            (FireHive.hiveEntrance in loadout) and
            (FireHive.hiveBurrow in loadout)
        ),
        ("HiveBurrowL", "SequesteredInfernoL"): lambda loadout: (
            (GravityBoots in loadout) and
            (FireHive.hiveBurrow in loadout) and
            ((icePod in loadout) or (FireHive.westHiveTunnel in loadout)) and
            (FireHive.crossways in loadout) and
            (FireHive.infernalSequestration in loadout)
        ),
        ("HiveBurrowL", "CollapsedPassageR"): lambda loadout: (
            (GravityBoots in loadout) and
            (FireHive.hiveBurrow in loadout) and
            ((icePod in loadout) or (FireHive.westHiveTunnel in loadout)) and
            (FireHive.crossways in loadout) and
            (FireHive.crosswaysToCourtyard in loadout) and
            (Super in loadout) and  # door to ancient basin access
            (FireHive.courtyardToCollapsed in loadout)
        ),
        ("SequesteredInfernoL", "VulnarDepthsElevatorER"): lambda loadout: (
            (GravityBoots in loadout) and
            (FireHive.infernalSequestration in loadout) and
            (FireHive.crossways in loadout) and
            ((icePod in loadout) or (FireHive.westHiveTunnel in loadout)) and
            (FireHive.hiveEntrance in loadout)
        ),
        ("SequesteredInfernoL", "HiveBurrowL"): lambda loadout: (
            (GravityBoots in loadout) and
            (FireHive.hiveBurrow in loadout) and
            ((icePod in loadout) or (FireHive.westHiveTunnel in loadout)) and
            (FireHive.crossways in loadout) and
            (FireHive.infernalSequestration in loadout)
        ),
        ("SequesteredInfernoL", "CollapsedPassageR"): lambda loadout: (
            (GravityBoots in loadout) and
            (FireHive.infernalSequestration in loadout) and
            (FireHive.crosswaysToCourtyard in loadout) and
            (Super in loadout) and  # door to ancient basin access
            (FireHive.courtyardToCollapsed in loadout)
        ),
        ("CollapsedPassageR", "VulnarDepthsElevatorER"): lambda loadout: (
            (GravityBoots in loadout) and
            (FireHive.courtyardToCollapsed in loadout) and
            (pinkDoor in loadout) and  # into ancient basin
            (FireHive.crosswaysToCourtyard in loadout) and
            (FireHive.crossways in loadout) and
            ((icePod in loadout) or (FireHive.westHiveTunnel in loadout)) and
            (FireHive.hiveEntrance in loadout)
        ),
        ("CollapsedPassageR", "HiveBurrowL"): lambda loadout: (
            (GravityBoots in loadout) and
            (FireHive.hiveBurrow in loadout) and
            ((icePod in loadout) or (FireHive.westHiveTunnel in loadout)) and
            (FireHive.crossways in loadout) and
            (FireHive.crosswaysToCourtyard in loadout) and
            (Super in loadout) and  # door to ancient basin access
            (FireHive.courtyardToCollapsed in loadout)
        ),
        ("CollapsedPassageR", "SequesteredInfernoL"): lambda loadout: (
            (GravityBoots in loadout) and
            (FireHive.courtyardToCollapsed in loadout) and
            (pinkDoor in loadout) and  # into ancient basin
            (FireHive.crosswaysToCourtyard in loadout) and
            (FireHive.infernalSequestration in loadout)
        ),
    },
    "Geothermal": {
        ("MagmaPumpL", "ReservoirMaintenanceTunnelR"): lambda loadout: (
            (GravityBoots in loadout) and
            (Geothermal.thermalResGamma in loadout) and
            (can_bomb(1) in loadout)
        ),
        ("MagmaPumpL", "IntakePumpR"): lambda loadout: (
            (GravityBoots in loadout) and
            (Geothermal.thermalResGamma in loadout) and
            (Geothermal.intakePump in loadout)
        ),
        ("MagmaPumpL", "ThermalReservoir1R"): lambda loadout: (
            (GravityBoots in loadout) and
            (Geothermal.thermalResGamma in loadout) and
            (Geothermal.thermalResBeta in loadout) and
            (Geothermal.control in loadout) and
            (MetroidSuit in loadout) and
            (Geothermal.thermalResAlpha in loadout)
        ),
        ("MagmaPumpL", "GeneratorAccessTunnelL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Geothermal.thermalResGamma in loadout) and
            (Geothermal.thermalResBeta in loadout) and
            (Geothermal.control in loadout) and
            (MetroidSuit in loadout) and
            (can_use_pbs(2) in loadout)
        ),
        ("ReservoirMaintenanceTunnelR", "MagmaPumpL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Geothermal.thermalResGamma in loadout) and
            (can_bomb(1) in loadout)
        ),
        ("ReservoirMaintenanceTunnelR", "IntakePumpR"): lambda loadout: (
            (GravityBoots in loadout) and
            (can_bomb(1) in loadout) and
            (Geothermal.intakePump in loadout)
        ),
        ("ReservoirMaintenanceTunnelR", "ThermalReservoir1R"): lambda loadout: (
            (GravityBoots in loadout) and
            (can_bomb(1) in loadout) and
            (Geothermal.thermalResBeta in loadout) and
            (Geothermal.control in loadout) and
            (MetroidSuit in loadout) and
            (Geothermal.thermalResAlpha in loadout)
        ),
        ("ReservoirMaintenanceTunnelR", "GeneratorAccessTunnelL"): lambda loadout: (
            (GravityBoots in loadout) and
            (can_bomb(1) in loadout) and
            (Geothermal.thermalResBeta in loadout) and
            (Geothermal.control in loadout) and
            (MetroidSuit in loadout) and
            (can_use_pbs(2) in loadout)
        ),
        ("IntakePumpR", "MagmaPumpL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Geothermal.intakePump in loadout) and
            (Geothermal.thermalResGamma in loadout)
        ),
        ("IntakePumpR", "ReservoirMaintenanceTunnelR"): lambda loadout: (
            (GravityBoots in loadout) and
            (Geothermal.intakePump in loadout) and
            (can_bomb(1) in loadout)
        ),
        ("IntakePumpR", "ThermalReservoir1R"): lambda loadout: (
            (GravityBoots in loadout) and
            (Geothermal.intakePump in loadout) and
            (Geothermal.control in loadout) and
            (MetroidSuit in loadout) and
            (Geothermal.thermalResAlpha in loadout)
        ),
        ("IntakePumpR", "GeneratorAccessTunnelL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Geothermal.intakePump in loadout) and
            (Geothermal.control in loadout) and
            (MetroidSuit in loadout) and
            (can_use_pbs(2) in loadout)
        ),
        ("ThermalReservoir1R", "MagmaPumpL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Geothermal.thermalResAlpha in loadout) and
            (MetroidSuit in loadout) and
            (Geothermal.control in loadout) and
            (Geothermal.thermalResBeta in loadout) and
            (Geothermal.thermalResGamma in loadout)
        ),
        ("ThermalReservoir1R", "ReservoirMaintenanceTunnelR"): lambda loadout: (
            (GravityBoots in loadout) and
            (Geothermal.thermalResAlpha in loadout) and
            (MetroidSuit in loadout) and
            (Geothermal.control in loadout) and
            (Geothermal.thermalResBeta in loadout) and
            (can_bomb(1) in loadout)
        ),
        ("ThermalReservoir1R", "IntakePumpR"): lambda loadout: (
            (GravityBoots in loadout) and
            (Geothermal.thermalResAlpha in loadout) and
            (MetroidSuit in loadout) and
            (Geothermal.control in loadout) and
            (Geothermal.intakePump in loadout)
        ),
        ("ThermalReservoir1R", "GeneratorAccessTunnelL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Geothermal.thermalResAlpha in loadout) and
            (can_use_pbs(2) in loadout)
        ),
        ("GeneratorAccessTunnelL", "MagmaPumpL"): lambda loadout: (
            (GravityBoots in loadout) and
            (can_use_pbs(2) in loadout) and
            (MetroidSuit in loadout) and
            (Geothermal.control in loadout) and
            (Geothermal.thermalResBeta in loadout) and
            (Geothermal.thermalResGamma in loadout)
        ),
        ("GeneratorAccessTunnelL", "ReservoirMaintenanceTunnelR"): lambda loadout: (
            (GravityBoots in loadout) and
            (can_use_pbs(2) in loadout) and
            (MetroidSuit in loadout) and
            (Geothermal.control in loadout) and
            (Geothermal.thermalResBeta in loadout) and
            (can_bomb(1) in loadout)
        ),
        ("GeneratorAccessTunnelL", "IntakePumpR"): lambda loadout: (
            (GravityBoots in loadout) and
            (can_use_pbs(2) in loadout) and
            (MetroidSuit in loadout) and
            (Geothermal.control in loadout) and
            (Geothermal.intakePump in loadout)
        ),
        ("GeneratorAccessTunnelL", "ThermalReservoir1R"): lambda loadout: (
            (GravityBoots in loadout) and
            (can_use_pbs(2) in loadout) and
            (Geothermal.thermalResAlpha in loadout)
        ),
    },
    "DrayLand": {
        ("ElevatorToMagmaLakeR", "MagmaPumpAccessR"): lambda loadout: (
            (GravityBoots in loadout) and
            (
                (
                    (Aqua in loadout) and
                    (Screw in loadout)
                ) or
                (electricHyper in loadout)
            ) and
            (lava_run(446, 950) in loadout) and  # TODO: measure lava run w/o aqua (950 is estimate)
            # TODO: killDragons or higher numbers for lava run
            (MetroidSuit in loadout) and
            (can_use_pbs(1) in loadout)
        ),
        ("MagmaPumpAccessR", "ElevatorToMagmaLakeR"): lambda loadout: (
            (GravityBoots in loadout) and
            (
                (
                    (Aqua in loadout) and
                    (Screw in loadout)
                ) or
                (electricHyper in loadout)
            ) and
            (lava_run(446, 950) in loadout) and  # TODO: measure lava run w/o aqua (950 is estimate)
            # TODO: killDragons or higher numbers for lava run
            (MetroidSuit in loadout) and
            (can_use_pbs(1) in loadout)
        ),
    },
    "Verdite": {
        ("FieryGalleryL", "RagingPitL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Verdite.fieryTrail in loadout) and
            ((can_bomb(1) in loadout) or (Screw in loadout)) and  # middle of verdite mines main shaft
            (Super in loadout) and  # door to raging pit access
            (Verdite.pit in loadout)
        ),
        ("FieryGalleryL", "HollowChamberR"): lambda loadout: (
            (GravityBoots in loadout) and
            (Verdite.fieryTrail in loadout) and
            (Verdite.beta in loadout) and
            (Super in loadout) and  # door out of lava pool
            (Verdite.hollow in loadout)
        ),
        ("FieryGalleryL", "PlacidPoolR"): lambda loadout: (
            (GravityBoots in loadout) and
            (Verdite.fieryTrail in loadout) and
            (Verdite.beta in loadout) and
            (Super in loadout) and  # door out of lava pool
            (Verdite.placid in loadout)
        ),
        ("FieryGalleryL", "SporousNookL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Verdite.fieryTrail in loadout) and
            (Verdite.hotSpring in loadout)
        ),
        ("RagingPitL", "FieryGalleryL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Verdite.pit in loadout) and
            (can_use_pbs(1) in loadout) and  # door to verdite mines
            ((can_bomb(1) in loadout) or (Screw in loadout)) and  # middle of verdite mines main shaft
            (Verdite.fieryTrail in loadout)
        ),
        ("RagingPitL", "HollowChamberR"): lambda loadout: (
            (GravityBoots in loadout) and
            (Verdite.pit in loadout) and
            (can_use_pbs(1) in loadout) and  # door to verdite mines
            ((can_bomb(1) in loadout) or (Screw in loadout)) and  # middle of verdite mines main shaft
            (Verdite.beta in loadout) and
            (Super in loadout) and  # door out of lava pool
            (Verdite.hollow in loadout)
        ),
        ("RagingPitL", "PlacidPoolR"): lambda loadout: (
            (GravityBoots in loadout) and
            (Verdite.pit in loadout) and
            (can_use_pbs(1) in loadout) and  # door to verdite mines
            ((can_bomb(1) in loadout) or (Screw in loadout)) and  # middle of verdite mines main shaft
            (Verdite.beta in loadout) and
            (Super in loadout) and  # door out of lava pool
            (Verdite.placid in loadout)
        ),
        ("RagingPitL", "SporousNookL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Verdite.pit in loadout) and
            (can_use_pbs(1) in loadout) and  # door to verdite mines
            ((can_bomb(1) in loadout) or (Screw in loadout)) and  # middle of verdite mines main shaft
            (Verdite.hotSpring in loadout)
        ),
        ("HollowChamberR", "FieryGalleryL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Verdite.hollow in loadout) and
            (pinkDoor in loadout) and  # door into lava pool
            (Verdite.beta in loadout) and
            (Verdite.fieryTrail in loadout)
        ),
        ("HollowChamberR", "RagingPitL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Verdite.hollow in loadout) and
            (pinkDoor in loadout) and  # door into lava pool
            (Verdite.beta in loadout) and
            ((can_bomb(1) in loadout) or (Screw in loadout)) and  # middle of verdite mines main shaft
            (Super in loadout) and  # door raging pit access
            (Verdite.pit in loadout)
        ),
        ("HollowChamberR", "PlacidPoolR"): lambda loadout: (
            (GravityBoots in loadout) and
            (Verdite.hollow in loadout) and
            (Verdite.placid in loadout)
        ),
        ("HollowChamberR", "SporousNookL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Verdite.hollow in loadout) and
            (pinkDoor in loadout) and  # door into lava pool
            (Verdite.beta in loadout) and
            (Verdite.hotSpring in loadout)
        ),
        ("PlacidPoolR", "FieryGalleryL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Verdite.placid in loadout) and
            (pinkDoor in loadout) and  # door into lava pool
            (Verdite.beta in loadout) and
            (Verdite.fieryTrail in loadout)
        ),
        ("PlacidPoolR", "RagingPitL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Verdite.placid in loadout) and
            (pinkDoor in loadout) and  # door into lava pool
            (Verdite.beta in loadout) and
            ((can_bomb(1) in loadout) or (Screw in loadout)) and  # middle of verdite mines main shaft
            (Super in loadout) and  # door to raging pit access
            (Verdite.pit in loadout)
        ),
        ("PlacidPoolR", "HollowChamberR"): lambda loadout: (
            (GravityBoots in loadout) and
            (Verdite.placid in loadout) and
            (Verdite.hollow in loadout)
        ),
        ("PlacidPoolR", "SporousNookL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Verdite.placid in loadout) and
            (pinkDoor in loadout) and  # door into lava pool
            (Verdite.beta in loadout) and
            (Verdite.hotSpring in loadout)
        ),
        ("SporousNookL", "FieryGalleryL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Verdite.hotSpring in loadout) and
            (Verdite.fieryTrail in loadout)
        ),
        ("SporousNookL", "RagingPitL"): lambda loadout: (
            (GravityBoots in loadout) and
            (Verdite.hotSpring in loadout) and
            ((can_bomb(1) in loadout) or (Screw in loadout)) and  # middle of verdite mines main shaft
            (Super in loadout) and  # door to raging pit access
            (Verdite.pit in loadout)
        ),
        ("SporousNookL", "HollowChamberR"): lambda loadout: (
            (GravityBoots in loadout) and
            (Verdite.hotSpring in loadout) and
            (Verdite.beta in loadout) and
            (Super in loadout) and  # door out of lava pool
            (Verdite.hollow in loadout)
        ),
        ("SporousNookL", "PlacidPoolR"): lambda loadout: (
            (GravityBoots in loadout) and
            (Verdite.hotSpring in loadout) and
            (Verdite.beta in loadout) and
            (Super in loadout) and  # door out of lava pool
            (Verdite.placid in loadout)
        ),
    },
}
