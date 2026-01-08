from typing import Callable

from .connection_data import area_doors_unpackable
from .item_data import items_unpackable
from .loadout import Loadout
from .logicCommon import ammo_req, can_bomb, can_use_pbs, crystal_flash, \
    energy_req, hell_run_energy, lava_run, varia_or_hell_run
from .logic_area_shortcuts import Early, SandLand, ServiceSector, SpacePort, LifeTemple, SkyWorld, \
    FireHive, PirateLab, Verdite, Geothermal, Suzi, DrayLand
from .logic_boss_kill import BossKill
from .logic_boss_reach import BossReach
from .logic_shortcut import LogicShortcut
from .logic_shortcut_data import (
    canFly, shootThroughWalls, breakIce, missileDamage, pinkDoor, pinkSwitch,
    missileBarrier, icePod, electricHyper, killRippers, killGreenOrRedPirates,
    bonkCeilingSuperSink, hiJumpSuperSink, iceSBA, plasmaSBA, spazerSBA
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

# above this should not include any shortcuts that reference doors
# so they can be used in the area door logic
# below this cannot be used in area door logic, only location logic

topOfSpaceport = LogicShortcut(lambda loadout: (
    ((
        (spaceDrop not in loadout)
    ) or (
        (spaceDrop in loadout) and
        (LoadingDockSecurityAreaL in loadout) and
        (SpacePort.loadingDock in loadout) and
        (SpacePort.spaceportTopFromElevator in loadout)
    ))
))
""" above the grapple gate """

sunkenNestToVulnar = LogicShortcut(lambda loadout: (
    (SunkenNestL in loadout) and
    (GravityBoots in loadout) and
    (pinkDoor in loadout) and  # impact crater bottom right
    (missileBarrier in loadout)
))
""" from sunken nest area door to entrance of vulnar caves """

sensorMaintenance = LogicShortcut(lambda loadout: (
    (sunkenNestToVulnar in loadout) and
    (pinkDoor in loadout) and  # into way of the watcher
    ((  # way of the watcher grey door
        (Missile in loadout) and
        (ammo_req(25) in loadout) and
        (Tricks.movement_moderate in loadout)
    ) or (
        (Super in loadout) and
        (ammo_req(45) in loadout)
    ) or (
        (Screw in loadout) and
        (missileBarrier in loadout)
    )) and
    # TODO: hypercharge and a number of accel charges for each skill level
    (Morph in loadout) and
    ((Tricks.mockball_hard in loadout) or (Speedball in loadout)) and
    ((Tricks.morph_jump_3_tile in loadout) or (Speedball in loadout) or (
        (can_bomb(4) in loadout) and
        ((Tricks.morph_jump_4_tile in loadout) or (Bombs in loadout))
    ))
))
""" logic is almost the same for the 2 sensor maintenance items """

norakToLifeTemple = LogicShortcut(lambda loadout: (
    (
        (NorakBrookL in loadout) and
        (LifeTemple.brook in loadout)
    ) or (
        (NorakPerimeterBL in loadout) and
        (LifeTemple.perimBL in loadout)
    ) or (
        (NorakPerimeterTR in loadout) and
        (MetroidSuit in loadout) and
        (GravityBoots in loadout)
    )
))
""" from any of the Norak area doors to Life Temple """

railAccess = LogicShortcut(lambda loadout: (
    (GravityBoots in loadout) and
    (
        (
            (WestTerminalAccessL in loadout) and
            (SkyWorld.westTerminal in loadout)
        ) or (
            (MezzanineConcourseL in loadout) and
            (SkyWorld.mezzanineShaft in loadout)
        ) or (
            (ElevatorToCondenserL in loadout) and
            (Morph in loadout) and
            (breakIce in loadout) and
            (SkyWorld.condenser in loadout)
        )
    )
))
""" access to the Sky Temple elevators at West Terminal and Transit Concourse """

collapsedHive = LogicShortcut(lambda loadout: (
    (CollapsedPassageR in loadout) and
    (pinkDoor in loadout) and
    (FireHive.courtyardToCollapsed in loadout)
))
""" collapsed passage door to anything beyond fire temple courtyard """

enterSuzi = LogicShortcut(lambda loadout: (
    (TramToSuziIslandR in loadout) and
    (Suzi.enter in loadout)
))
""" from suzi area door to inside with energy requirement """

meanderingPassage = LogicShortcut(lambda loadout: (
    ((
        (OceanShoreR in loadout) and
        (SandLand.shaftToGreenMoon in loadout) and
        (SandLand.shaftToLowerLower in loadout) and
        (SandLand.lowerLowerToSubCrevice in loadout) and
        (SandLand.subCreviceToSedFloor in loadout)  # used without the door into sediment floor
    ) or (
        (OceanShoreR in loadout) and
        (SandLand.GreenMoonDown in loadout) and
        (SandLand.canyonToGreenMoon in loadout) and
        (SandLand.sedFloorToCanyon in loadout) and
        (pinkDoor in loadout) and  # door to meandering passage
        # TODO: pinkDoor or (eddy and Super), in case super can't open pink door
        ((DarkVisor in loadout) or (Tricks.dark_medium in loadout))
    ) or (
        (EleToTurbidPassageR in loadout) and
        (SandLand.turbidToSedFloor in loadout) and
        (pinkDoor in loadout) and  # door to meandering passage
        ((DarkVisor in loadout) or (Tricks.dark_medium in loadout))
    )) and
    (loadout.has_any(Tricks.movement_moderate, energy_req(130)))  # puyos hurt
    # hint: snail will help you up meandering passage
))
""" from OceanShoreR or EleToTurbidPassageR to bottom of meandering passage"""

submarineCrevice = LogicShortcut(lambda loadout: (
    ((
        (OceanShoreR in loadout) and
        (SandLand.shaftToGreenMoon in loadout) and
        (SandLand.shaftToLowerLower in loadout) and
        (SandLand.lowerLowerToSubCrevice in loadout)
    ) or (
        (OceanShoreR in loadout) and
        (SandLand.GreenMoonDown in loadout) and
        (SandLand.canyonToGreenMoon in loadout) and
        (SandLand.sedFloorToCanyon in loadout) and
        (pinkDoor in loadout) and  # door to meandering passage
        # TODO: pinkDoor or (eddy and Super), in case super can't open pink door
        (SandLand.subCreviceToSedFloor in loadout) and
        ((DarkVisor in loadout) or (Tricks.dark_medium in loadout))
    ) or (
        (EleToTurbidPassageR in loadout) and
        (SandLand.turbidToSedFloor in loadout) and
        (pinkDoor in loadout) and  # door to meandering passage
        (SandLand.subCreviceToSedFloor in loadout) and
        ((DarkVisor in loadout) or (Tricks.dark_medium in loadout))
    ))
))
""" from OceanShoreR or EleToTurbidPassageR to middle of submarine crevice """

doorsToWestCorridorTop = LogicShortcut(lambda loadout: (
    # you don't need gravity boots from west corridor door,
    # but you won't be able to go anywhere else without them
    (GravityBoots in loadout) and
    (
        (WestCorridorR in loadout)
    ) or (
        (ExcavationSiteL in loadout) and
        (killGreenOrRedPirates(5) in loadout)
    ) or (
        (ConstructionSiteL in loadout) and
        (PirateLab.constructionLToElevator in loadout) and
        (can_use_pbs(1) in loadout) and
        (killGreenOrRedPirates(5) in loadout)
    )
))
""" pirate lab area doors to top of west corridor """

doorsToCentralCorridorBottom = LogicShortcut(lambda loadout: (
    # similar to Mid
    # the only difference is where I have to get out of the water
    (GravityBoots in loadout) and
    ((
        (WestCorridorR in loadout) and
        ((
            # through PB tube
            (killGreenOrRedPirates(5) in loadout) and
            (can_use_pbs(1) in loadout) and
            (PirateLab.epiphreaticIsobaric in loadout)
        ) or (
            # through hydrodynamic chamber
            (PirateLab.westCorridorToCentralTop in loadout) and
            (PirateLab.centralTopToMid in loadout) and
            (PirateLab.centralCorridorWater in loadout)
        ))
    ) or (
        (ExcavationSiteL in loadout) and
        (can_use_pbs(1) in loadout) and
        (PirateLab.epiphreaticIsobaric in loadout)
    ) or (
        (ConstructionSiteL in loadout) and
        (PirateLab.constructionLToElevator in loadout) and
        (PirateLab.epiphreaticIsobaric in loadout)
    ) or (
        (AlluringCenoteR in loadout) and
        (PirateLab.cenote in loadout) and
        ((Screw in loadout) or (MetroidSuit in loadout)) and
        (PirateLab.centralCorridorWater in loadout)
    ) or (
        (FoyerR in loadout) and
        (PirateLab.eastCorridor in loadout) and
        (PirateLab.centralCorridorWater in loadout)
    ))
))
""" pirate lab area doors to bottom of central corridor """

# TODO: without bombs or screw or super sink, I could
# enter pirate lab through isobaric vent,
# xray climb up central corridor,
# and circle back to wherever I came from through PB tube

# full circle:
# (isobaric - bombs), xray climb central, hydrodynamic, west corridor, lab workshop, PBs for pb tube

doorsToCentralCorridorMid = LogicShortcut(lambda loadout: (
    # similar to bottom
    # the only difference is where I have to get out of the water
    (GravityBoots in loadout) and
    ((
        (WestCorridorR in loadout) and
        ((
            # through PB tube
            (killGreenOrRedPirates(5) in loadout) and
            (can_use_pbs(1) in loadout) and
            (PirateLab.epiphreaticIsobaric in loadout) and
            (PirateLab.centralCorridorWater in loadout)
        ) or (
            # through hydrodynamic chamber
            (PirateLab.westCorridorToCentralTop in loadout) and
            (PirateLab.centralTopToMid in loadout)
        ))
    ) or (
        (ExcavationSiteL in loadout) and
        (can_use_pbs(1) in loadout) and
        (PirateLab.epiphreaticIsobaric in loadout) and
        (PirateLab.centralCorridorWater in loadout)
    ) or (
        (ConstructionSiteL in loadout) and
        (PirateLab.constructionLToElevator in loadout) and
        (PirateLab.epiphreaticIsobaric in loadout) and
        (PirateLab.centralCorridorWater in loadout)
    ) or (
        (AlluringCenoteR in loadout) and
        (PirateLab.cenote in loadout) and
        ((Screw in loadout) or (MetroidSuit in loadout))
    ) or (
        (FoyerR in loadout) and
        (PirateLab.eastCorridor in loadout)
    ))
))
""" pirate lab area doors to middle of central corridor """

location_logic: dict[str, Callable[[Loadout], bool]] = {
    "Impact Crater": lambda loadout: (  # under ship
        (SunkenNestL in loadout) and
        (GravityBoots in loadout) and
        (Morph in loadout) and
        ((Spazer in loadout) or (
            (hiJumpSuperSink in loadout) and
            ((bonkCeilingSuperSink in loadout) or (Tricks.super_sink_easy in loadout))
            # the position for the easy super sink to get out is right above where you pick up the item
            # spam jump (respin) while holding left on the d-pad
        )) and
        ((HiJump in loadout) or (SpeedBooster in loadout) or (canFly in loadout) or (
            loadout.has_all(Tricks.wall_jump_delayed, Tricks.movement_zoast)
            # the hard wall jump that I heard is used in low% - from the wall between the platforms
        ))
    ),
    "Subterranean Burrow": lambda loadout: (
        (SunkenNestL in loadout)
    ),
    "Sandy Cache": lambda loadout: (
        (OceanShoreR in loadout) and
        (SandLand.shaftToGreenMoon in loadout)
    ),
    "Submarine Nest": lambda loadout: (
        (OceanShoreR in loadout) and
        (GravityBoots in loadout) and
        (SandLand.shaftToGreenMoon in loadout) and
        (SandLand.shaftToSubmarineNest in loadout)
    ),
    "Shrine Of The Penumbra": lambda loadout: (
        (OceanShoreR in loadout) and
        (GravityBoots in loadout) and
        (missileDamage in loadout) and  # eye door
        (pinkDoor in loadout) and  # 2 pink doors if I don't have (morph and (hjb or aqua))

        (BossKill.kraid in loadout) and

        # up to door in kraid's lair
        ((
            (Aqua in loadout) and
            (loadout.has_any(canFly, HiJump, Tricks.gravity_jump, Tricks.short_charge_2, Tricks.sbj_no_hjb))
        ) or (
            # without aqua
            (Tricks.sbj_underwater_w_hjb in loadout)
        )) and

        ((
            (can_bomb(1) in loadout) and
            (DarkVisor in loadout)
        ) or (
            (can_use_pbs(2) in loadout)
        ) or (
            (DarkVisor in loadout) and
            (Morph in loadout) and
            ((
                # shoot the switch through the wall
                # (could hit with plasma special beam, but with that, you could just get through with PBs)
                (shootThroughWalls in loadout) and
                (
                    (Tricks.morph_jump_4_tile in loadout) or  # get on top of the switch
                    (Speedball in loadout)
                )
            ) or (
                # If I have dark visor, but no way to shoot through the wall to hit it:
                # super sink on top of the switch
                (Screw in loadout) and
                (Speedball in loadout) and
                (bonkCeilingSuperSink in loadout)
            ))
        ))
    ),
    "Benthic Cache Access": lambda loadout: (
        (submarineCrevice in loadout) and
        (SandLand.benthic in loadout) and
        # if you don't have bombs, you'll need 3 pbs
        (can_bomb(3) in loadout) and
        # and even if you do have bombs, you'll need 1 pb
        (can_use_pbs(1) in loadout) and
        ((
            (Aqua in loadout) and
            ((
                (HiJump in loadout)
            ) or (
                (Tricks.wall_jump_precise in loadout)
            ))
        ) or (
            # This is a harder SBJ because you can't see where you hit the ceiling
            (Tricks.sbj_underwater_w_hjb in loadout) and
            (Tricks.movement_moderate in loadout)
        ))
    ),
    "Benthic Cache": lambda loadout: (
        (submarineCrevice in loadout) and
        (SandLand.benthic in loadout)
    ),
    "Ocean Vent Supply Depot": lambda loadout: (
        (meanderingPassage in loadout) and
        (Morph in loadout) and  # inside the room with the item
        (  # down
            (Super in loadout) or
            ((Aqua in loadout) and (Screw in loadout)) or
            (  # right room intended way down
                ((can_bomb(1) in loadout) or (Screw in loadout)) and
                ((Tricks.movement_moderate in loadout) or (energy_req(150) in loadout) or (MetroidSuit in loadout))
            ) or
            (Tricks.super_sink_easy in loadout)  # door-stuck to start super sink
        ) and
        (  # up
            ((Super in loadout) and (
                (Tricks.morph_jump_3_tile_water in loadout) or
                (Speedball in loadout) or
                loadout.has_all(Aqua, can_bomb(1))
            )) or
            ((Aqua in loadout) and (Screw in loadout)) or

            # lava room
            ((can_use_pbs(1) in loadout) and (
                (MetroidSuit in loadout) or
                (energy_req(hell_run_energy(610, loadout)) in loadout) or
                ((Aqua in loadout) and (
                    (energy_req(hell_run_energy(310, loadout)) in loadout)
                )) or
                (loadout.has_all(Varia, Aqua, energy_req(hell_run_energy(210, loadout))))
            )) or

            (Tricks.xray_climb in loadout)
        )
    ),
    "Sediment Flow": lambda loadout: (
        # similar to sediment floor and part of eddy
        loadout.has_all(GravityBoots, Aqua) and
        ((
            (OceanShoreR in loadout) and
            ((  # from left
                (SandLand.shaftToGreenMoon in loadout) and
                (Super in loadout) and  # door from bottom of shallows into sediment tunnel

                # return
                (
                    (SandLand.directionalSedFloorToGreenMoonThroughSeaCaves in loadout) or
                    (
                        (SandLand.sedFloorToCanyon in loadout) and
                        (
                            (SandLand.canyonToShaft in loadout) or
                            (
                                (SandLand.canyonToGreenMoon in loadout) and

                                # since we came from ocean shore, we can open the canyon door from above
                                # (without going in it)
                                # before going around to the sediment tunnel entrance
                                ((can_use_pbs(1) in loadout) or (Super in loadout))
                            )
                        )
                    )
                )
            ) or (  # from right
                (SandLand.GreenMoonDown in loadout) and
                (SandLand.canyonToGreenMoon in loadout) and
                (SandLand.sedimentTunnel in loadout) and

                # return
                (
                    (SandLand.sedFloorToCanyon in loadout) or
                    (SandLand.directionalSedFloorToGreenMoonThroughSeaCaves in loadout)
                )
            ))
        ) or (
            (EleToTurbidPassageR in loadout) and
            (SandLand.turbidToSedFloor in loadout) and
            (pinkDoor in loadout) and  # turbid passage to sediment floor
            (SandLand.sedFloorToCanyon in loadout) and
            (SandLand.sedimentTunnel in loadout)
        ))
    ),
    "Harmonic Growth Enhancer": lambda loadout: (
        ((
            (FieldAccessL in loadout) and
            (ServiceSector.westSpore in loadout)
        ) or (
            (TransferStationR in loadout) and
            (ServiceSector.transfer in loadout) and
            (ServiceSector.eastSpore in loadout)
        )) and
        ((DarkVisor in loadout) or (Tricks.dark_easy in loadout)) and
        (can_bomb(2) in loadout) and
        (Morph in loadout) and
        (GravityBoots in loadout) and
        # 5-tile morph jump
        (pinkDoor in loadout) and  # between spore collection and spore generator access

        # kill spore spawn
        (loadout.has_any(Tricks.movement_moderate, HiJump, SpaceJump)) and
        (loadout.has_any(Tricks.movement_moderate, energy_req(130), Varia, MetroidSuit, Aqua)) and
        (loadout.has_any(missileDamage, Charge))
    ),
    "Upper Vulnar Power Node": lambda loadout: (
        (sunkenNestToVulnar in loadout) and
        # if you don't have (grapple or can fly), you can get up on the right wall with screw
        (Screw in loadout) and
        (can_use_pbs(2) in loadout) and  # if 20 ammo, you'll need to get drops from red balls
        (MetroidSuit in loadout)
    ),
    "Grand Vault": lambda loadout: (
        (sunkenNestToVulnar in loadout) and
        (Grapple in loadout)
    ),
    "Cistern": lambda loadout: (
        (RuinedConcourseBL in loadout) and (GravityBoots in loadout) and (can_bomb(1) in loadout)
    ),
    "Warrior Shrine: Middle": lambda loadout: (
        (RuinedConcourseBL in loadout) and
        (Early.eldersTop in loadout) and
        (Morph in loadout) and
        (pinkDoor in loadout) and  # to warrior shrine access
        (
            (can_bomb(1) in loadout) or  # PB placement is important if you only have 10 ammo
            (
                (Screw in loadout) and
                (Tricks.movement_moderate in loadout)  # just keep trying a few times, it's not hard
            )
        ) and
        ((Speedball in loadout) or (Tricks.mockball_hard in loadout)) and
        ((can_use_pbs(1) in loadout))  # or (bonkCeilingSuperSink in loadout))
        # TODO: find out if super sink is possible from inside
    ),
    "Vulnar Caves Entrance": lambda loadout: (
        (sunkenNestToVulnar in loadout)
    ),
    "Crypt": lambda loadout: (
        (RuinedConcourseBL in loadout) and
        (Early.eldersTop in loadout) and
        (can_bomb(3) in loadout) and
        (
            (shootThroughWalls in loadout) or
            (Bombs in loadout) or
            (
                (Speedball in loadout) and  # follow your bullet with speedball to hit the switch
                (Tricks.movement_moderate in loadout)
            ) or

            # a non-normal beam shot can clip through the platform from beneath to hit the top left switch
            (
                loadout.has_any(Ice, Plasma, Spazer, Charge) and
                (Tricks.wave_gate_glitch in loadout) and
                (Tricks.movement_moderate in loadout)
            )
            # I tried for a while with normal beam and couldn't get it.
            # (If it's possible, I think it's too hard to put in logic.)
            # TODO: do we want a different trick for this?
        )
    ),
    "Archives: Front": lambda loadout: (
        (sunkenNestToVulnar in loadout) and
        (pinkDoor in loadout) and  # into way of the watcher
        (Morph in loadout) and
        ((Speedball in loadout) or (
            (Tricks.super_sink_easy in loadout) and
            (Tricks.movement_moderate in loadout)
            # this 2-tile space is a little more difficult to get into than others
        ))
    ),
    "Archives: Back": lambda loadout: (
        (sunkenNestToVulnar in loadout) and
        (pinkDoor in loadout) and  # into way of the watcher
        (Morph in loadout) and
        (Speedball in loadout) and
        (SpeedBooster in loadout)
    ),
    "Sensor Maintenance: Top": lambda loadout: (  # front
        (sensorMaintenance in loadout)
    ),
    "Eribium Apparatus Room": lambda loadout: (
        (GravityBoots in loadout) and
        (can_bomb(1) in loadout) and  # required for getting out
        ((
            (FieldAccessL in loadout) and
            (ServiceSector.westSpore in loadout) and
            (ServiceSector.eastSpore in loadout)
        ) or (
            (TransferStationR in loadout) and
            (ServiceSector.transfer in loadout)
        ))
    ),
    "Hot Spring": lambda loadout: (
        (SporousNookL in loadout) and
        (GravityBoots in loadout) and
        (can_bomb(2) in loadout) and
        (Verdite.hotSpring in loadout) and
        ((Aqua in loadout) or (Speedball in loadout))  # 2-tile morph jump
        # TODO: this doesn't require as much from verdite
        # (hot spring to sporous nook can't be done with just HJB, but this can be done with just HJB)
    ),
    "Epiphreatic Crag": lambda loadout: (
        (GravityBoots in loadout) and
        ((
            (ConstructionSiteL in loadout) and
            (PirateLab.constructionLToElevator in loadout)
        ) or (
            (ExcavationSiteL in loadout) and
            (can_use_pbs(1) in loadout)
        )) and
        (Morph in loadout) and
        ((Aqua in loadout) or (
            (HiJump in loadout) and
            ((
                # crouch down grab into first small platform
                # ball jump up from there
                (Speedball in loadout) and
                (Tricks.crouch_or_downgrab in loadout)
            ) or (
                # I saw someone at a casual skill level do this:
                # space jump at surface to get up to the ledge on the right
                # and bomb jump or speedball jump to the left
                (SpaceJump in loadout) and
                (SpaceJumpBoost in loadout) and  # TODO: test for (sj boost or movement_moderate)
                ((can_bomb(1) in loadout) or (Speedball in loadout))  # TODO: what about wall jump into morph?
            ))
        ) or (
            # go up on the right side, then left above the water
            (PirateLab.epiphreatic in loadout) and
            ((can_use_pbs(1) in loadout) or (
                ((Screw in loadout) or (Tricks.super_sink_easy in loadout)) and
                (Bombs in loadout)
            ))
        ))
    ),
    "Mezzanine Concourse": lambda loadout: (
        (MezzanineConcourseL in loadout) and
        (GravityBoots in loadout) and
        (Morph in loadout) and
        (SkyWorld.mezzanineShaft in loadout) and
        ((Tricks.morph_jump_4_tile in loadout) or (Bombs in loadout) or (Speedball in loadout))
    ),
    "Greater Inferno": lambda loadout: (
        (BossReach.draygon in loadout) and
        (BossKill.draygon in loadout)
    ),
    "Burning Depths Cache": lambda loadout: (
        (MagmaPumpAccessR in loadout) and
        (GravityBoots in loadout) and
        (can_use_pbs(1) in loadout) and
        (lava_run(550, 1250) in loadout) and
        (MetroidSuit in loadout) and
        (Morph in loadout) and
        ((Spazer in loadout) or (
            (Tricks.searing_gate_tricks in loadout) and
            ((Wave in loadout) or ((Charge in loadout) and (Bombs in loadout)))
        )) and
        # under-lava 2-tile space below a bomb block to exit
        ((can_use_pbs(1) in loadout) or (
            (can_bomb(1) in loadout) and
            ((Aqua in loadout) or (Speedball in loadout))
        ))
    ),
    "Mining Cache": lambda loadout: (
        (GravityBoots in loadout) and
        (Super in loadout) and
        (
            # exit room
            (can_bomb(2) in loadout) or
            loadout.has_all(can_bomb(1), Speedball) or
            loadout.has_all(Morph, Speedball, shootThroughWalls)
            # wall morph or hi jump or space jump or ibj
        ) and
        ((
            (FieryGalleryL in loadout) and
            (Verdite.fieryTrail in loadout)
        ) or (
            (SporousNookL in loadout) and
            (Verdite.hotSpring in loadout)
        ))
    ),
    "Infested Passage": lambda loadout: (
        # copy and paste hive main passage
        (GravityBoots in loadout) and
        ((
            (VulnarDepthsElevatorEL in loadout) and
            (FireHive.hiveEntrance in loadout)
        ) or (
            (SequesteredInfernoL in loadout) and
            (FireHive.infernalSequestration in loadout) and
            (FireHive.crossways in loadout) and
            ((icePod in loadout) or (FireHive.westHiveTunnel in loadout))
        ) or (
            (HiveBurrowL in loadout) and
            (FireHive.hiveBurrow in loadout)
        ))
    ),
    "Fire's Boon Shrine": lambda loadout: (
        # TODO: hell run numbers for pit stop at fire temple courtyard
        # (because it's weird that ancient basin is in logic from firehive entrance, and not boon)
        ((shootThroughWalls in loadout) or (
            (Tricks.ggg in loadout) and
            (Varia in loadout) and  # hell run ggg over spikes not in logic
            (missileDamage in loadout)
            # TODO: another trick because this is harder than others? because of spikes
        )) and
        ((
            (VulnarDepthsElevatorEL in loadout) and
            (FireHive.hiveEntrance in loadout) and
            ((icePod in loadout) or (FireHive.westHiveTunnel in loadout)) and
            (FireHive.crossways in loadout) and
            (pinkDoor in loadout) and
            # TODO: something that can kill red pirates, in case door color changes
            # crossways to item and back to crossways
            (can_bomb(1) in loadout) and
            (varia_or_hell_run(850, heat_and_metroid_suit_not_required=True) in loadout)
        ) or (
            (SequesteredInfernoL in loadout) and
            (FireHive.infernalSequestration in loadout) and
            (pinkDoor in loadout) and
            # TODO: something that can kill red pirates, in case door color changes
            # crossways to item and back to crossways
            (can_bomb(1) in loadout) and
            (varia_or_hell_run(850, heat_and_metroid_suit_not_required=True) in loadout)
        ) or (
            (collapsedHive in loadout)
        )) and
        (GravityBoots in loadout)
    ),
    "Fire's Bane Shrine": lambda loadout: (
        (FireHive.twisted in loadout) and
        (FireHive.magmaFurnace in loadout) and

        ((
            (VulnarDepthsElevatorEL in loadout) and
            (FireHive.hiveEntrance in loadout) and
            ((icePod in loadout) or (FireHive.westHiveTunnel in loadout)) and
            (FireHive.crossways in loadout)
        ) or (
            (SequesteredInfernoL in loadout) and
            (FireHive.infernalSequestration in loadout)
        ) or (
            (collapsedHive in loadout)
        ))
    ),
    "Ancient Shaft": lambda loadout: (
        ((
            (MetroidSuit in loadout) and
            (varia_or_hell_run(450) in loadout)
        ) or (
            # no metroid suit
            ((
                (Varia in loadout) and
                (Aqua in loadout) and
                (
                    (energy_req(hell_run_energy(450, loadout)) in loadout) or
                    (
                        (Speedball in loadout) and
                        (can_use_pbs(4) in loadout) and
                        (energy_req(hell_run_energy(350, loadout)) in loadout)
                    )
                )
            ) or (
                (Varia in loadout) and
                # no aqua
                (energy_req(hell_run_energy(1250, loadout)) in loadout)
            ) or (
                (Aqua in loadout) and
                # no varia
                (energy_req(hell_run_energy(850, loadout)) in loadout)
            ))  # no suits not possible
        )) and
        (GravityBoots in loadout) and
        (
            (Aqua in loadout) or (Speedball in loadout) or (Tricks.morph_jump_3_tile_water in loadout)
        ) and
        (can_bomb(4) in loadout) and
        ((
            (VulnarDepthsElevatorEL in loadout) and
            (FireHive.hiveEntrance in loadout) and
            ((icePod in loadout) or (FireHive.westHiveTunnel in loadout)) and
            (FireHive.crossways in loadout) and
            (FireHive.crosswaysToCourtyard in loadout)
        ) or (
            (SequesteredInfernoL in loadout) and
            (FireHive.infernalSequestration in loadout) and
            (Morph in loadout) and
            (FireHive.crosswaysToCourtyard in loadout)
        ) or (
            (collapsedHive in loadout)
        ))
    ),
    "Gymnasium": lambda loadout: (  # similar to ancient basin
        (Grapple in loadout) and
        (GravityBoots in loadout) and
        ((  # from west
            ((
                (VulnarDepthsElevatorEL in loadout) and
                (FireHive.hiveEntrance in loadout) and
                ((icePod in loadout) or (FireHive.westHiveTunnel in loadout)) and
                (FireHive.crossways in loadout) and
                (FireHive.crosswaysToCourtyard in loadout)
            ) or (
                (SequesteredInfernoL in loadout) and
                (FireHive.infernalSequestration in loadout) and
                (FireHive.crosswaysToCourtyard in loadout)
            ) or (
                (collapsedHive in loadout)  # using fire temple courtyard as a pit stop
            )) and
            # from fire temple courtyard to gymnasium
            (loadout.has_any(killRippers, Varia, Tricks.movement_zoast)) and  # just outside courtyard
            ((  # through power bomb blocks
                (can_use_pbs(3) in loadout) and
                (varia_or_hell_run(507, heat_and_metroid_suit_not_required=True) in loadout)
            ) or (  # through ancient basin
                (can_bomb(3) in loadout) and
                (varia_or_hell_run(869, heat_and_metroid_suit_not_required=True) in loadout)
            ))
        ) or (  # from east, no fire temple courtyard
            (collapsedHive in loadout) and
            (varia_or_hell_run(1450, heat_and_metroid_suit_not_required=True) in loadout)
        ))
    ),
    "Electromechanical Engine": lambda loadout: (
        (Grapple in loadout) and
        (Morph in loadout) and
        (GravityBoots in loadout) and
        ((Tricks.morph_jump_3_tile_up_1 in loadout) or (Speedball in loadout) or (can_bomb(1) in loadout)) and
        # which area door to come from
        ((
            # from below
            ((
                (ReservoirMaintenanceTunnelR in loadout) and
                (can_bomb(1) in loadout)
            ) or (
                (MagmaPumpL in loadout) and
                (Geothermal.thermalResGamma in loadout)
            )) and
            (Geothermal.thermalResBeta in loadout) and
            (Geothermal.control in loadout) and
            ((  # security matrix
                loadout.has_all(MetroidSuit, DarkVisor, varia_or_hell_run(311))
                # Metroid suit allows you to shoot switches that would normally need shootThroughWalls
            ) or (
                (Geothermal.mainBoiler in loadout)
            ))
        ) or (
            # The ways that come in the top of central corridor require metroid suit
            (MetroidSuit in loadout) and
            ((  # security matrix
                loadout.has_all(DarkVisor, varia_or_hell_run(311))
                # Metroid suit allows you to shoot switches that would normally need shootThroughWalls
            ) or (  # main boiler
                (Geothermal.mainBoiler in loadout)
            )) and
            (
                (ThermalReservoir1R in loadout) and
                (MetroidSuit in loadout) and
                (Geothermal.thermalResAlpha in loadout)
            ) or (
                (GeneratorAccessTunnelL in loadout) and
                (MetroidSuit in loadout) and  # top laser puzzles are 1 way w/o metroid suit
                (can_use_pbs(3) in loadout)
            )
        ))
    ),
    "Depressurization Valve": lambda loadout: (
        (GravityBoots in loadout) and
        (loadout.has_any(Morph, Screw)) and  # TODO: or blue keep?
        # which area door to come from
        ((
            (ReservoirMaintenanceTunnelR in loadout) and
            (Geothermal.control in loadout) and
            (can_bomb(1) in loadout) and
            (Geothermal.thermalResBeta in loadout) and
            ((True))  # or (Grapple in loadout) or (MetroidSuit in loadout))
            # This `True` represents the ability to turn the power off and back on again (requiring Screw)
            # It's here in case we disable turning off the power.
        ) or (
            (ThermalReservoir1R in loadout) and
            (MetroidSuit in loadout) and
            (Geothermal.thermalResAlpha in loadout)
        ) or (
            (GeneratorAccessTunnelL in loadout) and
            (MetroidSuit in loadout) and  # top laser puzzles are 1 way w/o metroid suit
            (can_use_pbs(3) in loadout)
        ) or (
            (MagmaPumpL in loadout) and
            (Geothermal.thermalResGamma in loadout) and
            (Geothermal.thermalResBeta in loadout) and
            (Geothermal.control in loadout) and
            ((True))  # or (Grapple in loadout) or (MetroidSuit in loadout))
            # This `True` represents the ability to turn the power off and back on again (requiring Screw)
            # It's here in case we disable turning off the power.
        ))
    ),
    "Loading Dock Storage Area": lambda loadout: (
        (LoadingDockSecurityAreaL in loadout)  # no gravity boots needed
    ),
    "Containment Area": lambda loadout: (
        (GravityBoots in loadout) and
        ((
            (doorsToCentralCorridorMid in loadout) and
            ((MetroidSuit in loadout) or (Screw in loadout))
        ) or (
            (AlluringCenoteR in loadout) and
            (PirateLab.cenote in loadout)
        ))
    ),
    "Briar: Top": lambda loadout: (  # PB tube
        (norakToLifeTemple in loadout) and
        (GravityBoots in loadout) and
        ((
            (can_use_pbs(1) in loadout)
        ) or (
            (bonkCeilingSuperSink in loadout) and
            (
                (can_bomb(1) in loadout) or

                loadout.has_all(bonkCeilingSuperSink, Tricks.morphless_tunnel_crawl)
                # get slopekiller above the right tile of the bomb blocks or the left tile of the bomb blocks
                # (for a 4-tile or 5-tile vertical space respectively)
                # then use turn around cancel to move slope killer to the 1st tile right of the bomb blocks
                # (don't move too far right, there's terrain that will mess up the super sink
                #  - keep a few pixels over the bomb blocks)
            )
        ))
    ),
    "Shrine Of Fervor": lambda loadout: (
        (GravityBoots in loadout) and
        (norakToLifeTemple in loadout) and
        (LifeTemple.veranda in loadout)
    ),
    "Chamber Of Wind": lambda loadout: (
        (GravityBoots in loadout) and
        (norakToLifeTemple in loadout) and
        (LifeTemple.veranda in loadout) and
        (pinkDoor in loadout) and
        ((can_bomb(2) in loadout) or (Screw in loadout)) and  # wall outside the door
        # Chamber of Wind Access both ways
        (SpeedBooster in loadout) and
        ((can_bomb(2) in loadout) or (
            (Speedball in loadout) and
            (Morph in loadout)
        ) or (
            (Tricks.short_charge_2 in loadout) and
            (HiJump in loadout) and
            (SpaceJump in loadout) and
            (Tricks.movement_moderate in loadout)
        )) and
        # get out of chamber of wind
        (
            (Tricks.short_charge_2 in loadout) or
            (canFly in loadout) or  # combine with wall jumps if no SJB

            ((HiJump in loadout) and (Tricks.wall_jump_precise in loadout))
            # with speedbooster, jump high enough to wall jump on top ledges
        )
        # TODO: Azder did this with no bombs, pbs, nor screw
        # This might be higher than expert level logic - Tricks.bob?
        # getting in, shinespark in is easy
        # getting out, he had (and needed) space jump and wave beam
        # charge shinespark at bottom of chamber of wind,
        # fast wall jump and space jump to get through door into chamber of wind access,
        # shoot left door (wave beam through wall, no time for hypercharge) of chamber of wind access
        # and use shinespark through it
        # He had no space jump boost, nor hi jump boots. Those would make it easier
        # https://clips.twitch.tv/AntsyVivaciousFriesNotLikeThis-SW5bAw7fOAyQnJfP
    ),
    "Water Garden": lambda loadout: (
        (GravityBoots in loadout) and
        (norakToLifeTemple in loadout) and
        (LifeTemple.veranda in loadout) and
        (LifeTemple.waterToVeranda in loadout) and
        (SpeedBooster in loadout) and
        (energy_req(163) in loadout)
        # TODO: Might there be a reason to add logic from ElevatorToWellspringL ?
    ),
    "Crocomire's Energy Station": lambda loadout: (
        # similar to crocomire lair, except need to go through bomb blocks on left
        (GravityBoots in loadout) and
        (norakToLifeTemple in loadout) and
        (LifeTemple.veranda in loadout) and
        (LifeTemple.waterToVeranda in loadout) and
        (SpeedBooster in loadout) and
        (Super in loadout) and  # door to elevator to jungle's heart
        ((  # to get past the bomb blocks in the left side of Croc's room (can't use shinespark for exit)
            (Morph in loadout) and
            (Speedball in loadout)
        ) or (can_bomb(2) in loadout) or (Screw in loadout) or (Tricks.morph_jump_3_tile in loadout))
    ),  # TODO: Might there be a reason to add logic from ElevatorToWellspringL ?
    "Wellspring Cache": lambda loadout: (
        (ElevatorToWellspringL in loadout) and
        (GravityBoots in loadout) and
        (Super in loadout) and
        (Morph in loadout) and
        ((
            (Aqua in loadout)
        ) or (
            (HiJump in loadout) and
            (Tricks.crouch_or_downgrab in loadout)
        ) or (
            (Speedball in loadout) and
            (Tricks.sbj_underwater_no_hjb in loadout) and
            (Tricks.crouch_or_downgrab in loadout)
        ) or (
            (Ice in loadout) and
            (ammo_req(20) in loadout) and  # a few supers to knock worm off the wall
            (Tricks.freeze_hard in loadout)
        ))
    ),
    "Frozen Lake Wall": lambda loadout: (
        (ElevatorToCondenserL in loadout) and
        (GravityBoots in loadout) and
        (can_use_pbs(1) in loadout)
    ),
    "Grand Promenade": lambda loadout: (
        (railAccess in loadout) and (GravityBoots in loadout)
    ),
    "Summit Landing": lambda loadout: (
        (GravityBoots in loadout) and
        (Morph in loadout) and
        ((can_bomb(1) in loadout) or (Screw in loadout)) and
        (railAccess in loadout) and
        (varia_or_hell_run(69) in loadout) and
        (loadout.has_any(Speedball, Tricks.movement_moderate))  # jump through respawning crumble block
    ),
    "Snow Cache": lambda loadout: (
        (railAccess in loadout) and
        (GravityBoots in loadout) and
        (can_bomb(4) in loadout) and
        ((
            (varia_or_hell_run(151) in loadout)
        ) or (
            ((Screw in loadout) or (
                (Charge in loadout) and
                (Hypercharge in loadout)
            )) and  # easier to farm health
            (varia_or_hell_run(98) in loadout)
        ))
    ),
    "Reliquary Access": lambda loadout: (
        # get to the item
        (Super in loadout) and
        (railAccess in loadout) and
        (SkyWorld.anticipation in loadout) and
        (GravityBoots in loadout) and
        ((BossKill.ridley in loadout) or (
            (can_bomb(1) in loadout) and
            (loadout.has_any(Bombs, Speedball, Tricks.morph_jump_3_tile, Tricks.morph_jump_4_tile))
        )) and
        # get out
        ((
            (BossKill.ridley in loadout) and
            (SkyWorld.anticipation in loadout)
        ) or (
            (BossKill.phantoon in loadout) and
            (can_bomb(3) in loadout) and
            (SkyWorld.meetingHallToLeft in loadout)
        ))
    ),
    "Syzygy Observatorium": lambda loadout: (
        (railAccess in loadout) and
        (GravityBoots in loadout) and
        ((
            (Screw in loadout) and
            ((  # stair of dawn
                (Morph in loadout) and
                (pinkDoor in loadout)
            ) or (  # anticipation chamber
                (SkyWorld.anticipation in loadout)
            )) and
            (varia_or_hell_run(90) in loadout)
        ) or (
            (SkyWorld.anticipation in loadout) and
            (Super in loadout) and
            (BossKill.ridley in loadout)
        ))
    ),
    "Armory Cache 2": lambda loadout: (
        # copy and paste armory cache 3
        (railAccess in loadout) and
        (GravityBoots in loadout) and
        ((
            (SkyWorld.meetingHall in loadout)  # both enter and exit
        ) or (
            (Super in loadout) and
            (can_bomb(2) in loadout) and
            (BossKill.phantoon in loadout) and
            loadout.has_any(
                Bombs, Speedball, Tricks.morph_jump_3_tile, Tricks.morph_jump_4_tile, BossKill.ridley
            ) and
            (SkyWorld.meetingHallToLeft in loadout)  # exit
        ))
    ),
    "Armory Cache 3": lambda loadout: (
        # copy and paste armory cache 2
        (railAccess in loadout) and
        (GravityBoots in loadout) and
        ((
            (SkyWorld.meetingHall in loadout)  # both enter and exit
        ) or (
            (Super in loadout) and
            (can_bomb(2) in loadout) and
            (BossKill.phantoon in loadout) and
            loadout.has_any(
                Bombs, Speedball, Tricks.morph_jump_3_tile, Tricks.morph_jump_4_tile, BossKill.ridley
            ) and
            (SkyWorld.meetingHallToLeft in loadout)  # exit
        ))
    ),
    "Drawing Room": lambda loadout: (
        (Super in loadout) and
        (GravityBoots in loadout) and
        (railAccess in loadout) and
        (SkyWorld.anticipation in loadout) and
        (varia_or_hell_run(90) in loadout)  # This might require getting i-frames from enemies to avoid spike damage
    ),
    "Impact Crater Overlook": lambda loadout: (
        (SunkenNestL in loadout) and
        (GravityBoots in loadout) and
        (can_bomb(2) in loadout) and
        ((
            (can_use_pbs(1) in loadout)
        ) or (
            (Super in loadout) and
            # getting in and out with supers is not trivial
            # right after super tunnel:
            (
                (Speedball in loadout) or
                (can_bomb(1) in loadout) or
                (Tricks.morph_jump_3_tile in loadout)
            ) and

            # exit
            ((
                (Tricks.super_sink_easy in loadout)
            ) or (
                (
                    (Speedball in loadout) or
                    (Bombs in loadout) or
                    (Tricks.morph_jump_4_tile in loadout)
                )
            ))
        ) or (
            # from the door to impact crater alcove
            (Tricks.xray_climb in loadout) and  # up
            (Tricks.super_sink_easy in loadout) and  # down
            (Tricks.movement_moderate in loadout)
            # movement_moderate because you can't see when you're done xray climbing,
            # just have to morph and hope you're not soft-locked
        )) and
        (Early.craterLedge in loadout)
    ),
    "Magma Lake Cache": lambda loadout: (
        (ElevatorToMagmaLakeR in loadout) and
        (GravityBoots in loadout) and
        (icePod in loadout) and
        (Morph in loadout) and
        ((Tricks.movement_moderate in loadout) or (HiJump in loadout) or (Speedball in loadout))
    ),
    "Shrine Of The Animate Spark": lambda loadout: (
        (enterSuzi in loadout) and
        (Suzi.cyphers in loadout) and
        ((
            (Hypercharge in loadout) and
            (Charge in loadout)
        ) or (
            (Charge in loadout) and
            (energy_req(
                750
                if (Tricks.movement_zoast in loadout)
                else (
                    1050
                    if (Tricks.movement_moderate in loadout)
                    else 1350
                )
            ) in loadout)
        )) and
        # exit
        (Hypercharge in loadout) and
        (Charge in loadout)
    ),
    "Docking Port 4": lambda loadout: (  # (4 = letter Omega)
        # copy and paste docking port 3
        (
            (spaceDrop not in loadout) and
            (Grapple in loadout)
        ) or (
            (spaceDrop in loadout) and
            (LoadingDockSecurityAreaL in loadout) and
            (SpacePort.loadingDock in loadout)
        )
    ),
    "Ready Room": lambda loadout: (
        (Super in loadout) and
        (topOfSpaceport in loadout)
    ),
    "Torpedo Bay": lambda loadout: (
        (topOfSpaceport in loadout)
    ),
    "Extract Storage": lambda loadout: (
        (can_use_pbs(1) in loadout) and
        (
            (electricHyper in loadout) or
            (
                ((energy_req(250) in loadout) or (Tricks.movement_zoast in loadout)) and
                (can_use_pbs(3) in loadout)
            )
        ) and
        (topOfSpaceport in loadout)
    ),
    "Impact Crater Alcove": lambda loadout: (
        (SunkenNestL in loadout) and
        (GravityBoots in loadout) and
        (can_bomb(2) in loadout) and
        (Early.craterLedge in loadout)
    ),
    "Ocean Shore: Bottom": lambda loadout: (
        (OceanShoreR in loadout)
    ),
    "Ocean Shore: Top": lambda loadout: (
        (OceanShoreR in loadout) and
        (SandLand.oceanShoreTop in loadout)
    ),
    "Sandy Burrow: Top": lambda loadout: (  # ETank
        (OceanShoreR in loadout) and
        (SandLand.sandy_burrow in loadout) and

        # the number of PBs in can_bomb is because the blocks respawn pretty fast
        ((
            (Aqua in loadout) and
            ((Screw in loadout) or (
                (can_bomb(1) in loadout) and
                (Tricks.movement_moderate in loadout)
            ) or (
                (can_bomb(2) in loadout)
            ))
        ) or (
            ((Tricks.sbj_underwater_no_hjb in loadout) or (HiJump in loadout)) and
            (
                (can_bomb(1) in loadout) and
                (Tricks.movement_zoast in loadout)  # water slows you down
            ) or (
                (can_bomb(2) in loadout)
            )
        )) and

        # from first morph tunnel up to door
        ((
            (Aqua in loadout)
        ) or (
            (Tricks.sbj_underwater_w_hjb in loadout)
        ) or (
            (Bombs in loadout) and (HiJump in loadout) and (Tricks.freeze_hard in loadout)
            # note: freezing enemies requires not killing the enemies with power bomb to get top item
            # so this section has to be duplicated in SandLand area shortcuts
        ))
    ),
    "Submarine Alcove": lambda loadout: (
        (meanderingPassage in loadout) and
        (Morph in loadout) and
        (
            # casual wall morph or hjb or space or ibj
            (Aqua in loadout) or
            (Tricks.sbj_underwater_w_hjb in loadout) or
            loadout.has_all(Tricks.sbj_underwater_no_hjb, Tricks.freeze_hard) or
            (HiJump in loadout) or
            (Tricks.crouch_or_downgrab in loadout)  # TODO: this with Tricks.snail_climb ?
        )
    ),
    "Sediment Floor": lambda loadout: (
        # similar to sediment flow and part of eddy
        (GravityBoots in loadout) and
        ((
            (OceanShoreR in loadout) and
            ((  # from left
                (SandLand.shaftToGreenMoon in loadout) and
                (SandLand.canyonToShaft in loadout) and

                # return
                (
                    (SandLand.directionalSedFloorToGreenMoonThroughSeaCaves in loadout) or
                    (SandLand.sedFloorToCanyon in loadout)
                )
            ) or (  # from right
                (SandLand.GreenMoonDown in loadout) and
                (SandLand.canyonToGreenMoon in loadout) and

                # return
                (
                    (SandLand.sedFloorToCanyon in loadout) or
                    (SandLand.directionalSedFloorToGreenMoonThroughSeaCaves in loadout)
                )
            ))
        ) or (
            (EleToTurbidPassageR in loadout) and
            (SandLand.turbidToSedFloor in loadout) and
            (pinkDoor in loadout) and  # turbid passage to sediment floor
            (SandLand.sedFloorToCanyon in loadout)
        ))
    ),
    "Sandy Gully": lambda loadout: (
        (OceanShoreR in loadout) and
        (Super in loadout) and  # green moon simplified because of super gate
        (GravityBoots in loadout) and
        (Aqua in loadout) and
        ((HiJump in loadout) or (
            (SpaceJump in loadout) and
            (SpaceJumpBoost in loadout)
            # TODO:logic shortcut for how many space jump boost
        ) or (
            (Tricks.movement_zoast in loadout)
        ) or (
            # gravity jump off disappearing blocks
            (Tricks.movement_moderate in loadout) and
            (Tricks.gravity_jump in loadout)
        ))
        # TODO: rusty said an expert can do this with just gravity boots and hi jump boots
        # I don't see how.
        # joonie said he thinks it's possible with double sbj (w hjb), but he gave up trying
    ),
    "Hall Of The Elders": lambda loadout: (
        (RuinedConcourseBL in loadout) and
        (Early.eldersBottom in loadout) and
        (
            (missileDamage in loadout) or
            (Aqua in loadout) or
            (HiJump in loadout) or
            (
                (Ice in loadout) and
                (Tricks.freeze_hard in loadout)
            ) or
            (SpaceJump in loadout) or  # no SJ boost needed
            (Tricks.sbj_underwater_no_hjb in loadout)
        )
    ),
    "Warrior Shrine: Bottom": lambda loadout: (
        (RuinedConcourseBL in loadout) and
        (Early.eldersTop in loadout) and
        (Morph in loadout) and
        (pinkDoor in loadout)
    ),
    "Warrior Shrine: Top": lambda loadout: (
        (RuinedConcourseBL in loadout) and
        (Early.eldersTop in loadout) and
        (Morph in loadout) and
        (pinkDoor in loadout) and  # to warrior shrine access
        (
            (can_bomb(1) in loadout) or  # PB placement is important if you only have 10 ammo
            (
                (Screw in loadout) and
                (Tricks.movement_moderate in loadout)  # just keep trying a few times, it's not hard
            )
        ) and
        ((Speedball in loadout) or (Tricks.mockball_hard in loadout))
    ),
    "Path Of Swords": lambda loadout: (
        (sunkenNestToVulnar in loadout) and
        ((can_bomb(1) in loadout) or (
            (Morph in loadout) and (Screw in loadout)
        ))
    ),
    "Auxiliary Pump Room": lambda loadout: (
        (sunkenNestToVulnar in loadout) and (can_bomb(1) in loadout)
    ),
    "Monitoring Station": lambda loadout: (
        (sunkenNestToVulnar in loadout) and
        (Morph in loadout) and
        ((Speedball in loadout) or (can_bomb(1) in loadout) or (Tricks.movement_zoast in loadout))
    ),
    "Sensor Maintenance: Bottom": lambda loadout: (  # back
        (sensorMaintenance in loadout) and
        (can_bomb(2) in loadout)  # TODO: confirm this is the only difference from the other sensor maintenance item
    ),
    "Causeway Overlook": lambda loadout: (
        (CausewayR in loadout) and (GravityBoots in loadout) and (can_bomb(1) in loadout)
    ),
    "Placid Pool": lambda loadout: (
        (PlacidPoolR in loadout) and
        (GravityBoots in loadout) and
        (can_use_pbs(1) in loadout) and
        ((icePod in loadout) or (
            (Aqua in loadout) and
            (hiJumpSuperSink in loadout) and
            (Tricks.clip_crouch in loadout)
        )) and
        ((Aqua in loadout) or (
            (HiJump in loadout) and (Tricks.crouch_or_downgrab in loadout)
        ) or (
            (Tricks.sbj_underwater_no_hjb in loadout)
        ))
    ),
    "Blazing Chasm": lambda loadout: (
        (ElevatorToMagmaLakeR in loadout) and
        (GravityBoots in loadout) and
        (can_use_pbs(1) in loadout) and
        # no aqua will require crystal flash
        (lava_run(850, 1650) in loadout) and
        (MetroidSuit in loadout) and
        # something to do damage here
        (loadout.has_any(Screw, Plasma, Spazer, shootThroughWalls, Super, Tricks.movement_zoast)) and
        # a non-simple jump to get up blazing chasm
        ((
            (Aqua in loadout) and
            ((canFly in loadout) or (Tricks.gravity_jump in loadout))
        ) or (
            (HiJump in loadout)
        ) or (
            (Tricks.wall_jump_precise in loadout)
        ))
    ),
    "Generator Manifold": lambda loadout: (
        (Super in loadout) and
        (GravityBoots in loadout) and
        (can_bomb(4) in loadout) and
        ((
            (ReservoirMaintenanceTunnelR in loadout) and
            (can_bomb(1) in loadout) and
            (Geothermal.thermalResBeta in loadout)
        ) or (
            (GeneratorAccessTunnelL in loadout) and
            (MetroidSuit in loadout) and  # top laser puzzles are 1 way w/o metroid suit
            (Geothermal.control in loadout) and
            (can_use_pbs(3) in loadout)
        ) or (
            (ThermalReservoir1R in loadout) and
            (MetroidSuit in loadout) and
            (Geothermal.control in loadout) and
            (Geothermal.thermalResAlpha in loadout)
        ))
    ),
    "Fiery Crossing Cache": lambda loadout: (
        (RagingPitL in loadout) and
        (GravityBoots in loadout) and
        (varia_or_hell_run(420) in loadout) and
        (can_use_pbs(1) in loadout)
    ),
    "Dark Crevice Cache": lambda loadout: (
        (ElevatorToMagmaLakeR in loadout) and
        (GravityBoots in loadout) and
        (can_bomb(1) in loadout) and
        (
            (canFly in loadout) or
            (SpeedBooster in loadout) or
            ((HiJump in loadout) and (Tricks.wall_jump_precise in loadout) and (DarkVisor in loadout))
        ) and
        # or wall_jump_insane (same as worst room with no hjb) - and doing it in the dark would be stupid
        ((DarkVisor in loadout) or (Tricks.dark_hard in loadout))
        # TODO: should wall jump in the dark be different from canFly or speedbooster in the dark?
    ),
    "Ancient Basin": lambda loadout: (  # similar to gymnasium
        (GravityBoots in loadout) and
        ((  # from west
            ((
                (VulnarDepthsElevatorEL in loadout) and
                (FireHive.hiveEntrance in loadout) and
                ((icePod in loadout) or (FireHive.westHiveTunnel in loadout)) and
                (FireHive.crossways in loadout) and
                (FireHive.crosswaysToCourtyard in loadout)
            ) or (
                (SequesteredInfernoL in loadout) and
                (FireHive.infernalSequestration in loadout) and
                (FireHive.crosswaysToCourtyard in loadout)
            ) or (
                (collapsedHive in loadout)  # using fire temple courtyard as a pit stop
            )) and
            # from fire temple courtyard to item in ancient basin
            (loadout.has_any(killRippers, Varia, Tricks.movement_zoast)) and  # just outside courtyard
            ((  # through power bomb blocks
                (can_use_pbs(3) in loadout) and
                (varia_or_hell_run(444, heat_and_metroid_suit_not_required=True) in loadout)
            ) or (  # through ancient basin
                (can_bomb(3) in loadout) and
                (loadout.has_any(Tricks.crumble_jump, SpaceJump, Speedball, Grapple)) and
                (varia_or_hell_run(661, heat_and_metroid_suit_not_required=True) in loadout)
            ))
        ) or (  # from east, no fire temple courtyard
            (collapsedHive in loadout) and
            (loadout.has_any(Tricks.crumble_jump, SpaceJump, Speedball, Grapple)) and
            (varia_or_hell_run(1216, heat_and_metroid_suit_not_required=True) in loadout)
        ))
    ),
    "Central Corridor: Right": lambda loadout: (
        (GravityBoots in loadout) and
        (can_bomb(1) in loadout) and

        # lowest jump in central corridor (below "bottom")
        (loadout.has_any(Aqua, HiJump, Tricks.crouch_or_downgrab, Ice, Tricks.sbj_underwater_no_hjb)) and

        (doorsToCentralCorridorBottom in loadout)
    ),
    "Briar: Bottom": lambda loadout: (  # AmmoTank
        (norakToLifeTemple in loadout) and
        (Morph in loadout) and
        (GravityBoots in loadout)
    ),
    "Icy Flow": lambda loadout: (
        (railAccess in loadout) and
        (GravityBoots in loadout) and
        (SpeedBooster in loadout) and
        (breakIce in loadout) and
        ((
            (varia_or_hell_run(111) in loadout)
        ) or (
            ((Screw in loadout) or (
                (Charge in loadout) and
                (Hypercharge in loadout)
            )) and  # easier to farm health
            (varia_or_hell_run(88) in loadout)
        ))
    ),
    "Ice Cave": lambda loadout: (
        (railAccess in loadout) and
        (GravityBoots in loadout) and
        (breakIce in loadout) and
        ((
            (varia_or_hell_run(111) in loadout)
        ) or (
            ((Screw in loadout) or (
                (Charge in loadout) and
                (Hypercharge in loadout)
            )) and  # easier to farm health
            (varia_or_hell_run(88) in loadout)
        ))
    ),
    "Antechamber": lambda loadout: (
        (railAccess in loadout) and
        (GravityBoots in loadout) and
        (
            (can_use_pbs(1) in loadout) or

            # xray up from left door, super sink down from right side, joonie used about 7 etanks with aqua
            # hard energy req because you get hit by ghost while xray climbing and super sinking
            loadout.has_all(Tricks.xray_climb, Tricks.super_sink_easy, varia_or_hell_run(1050), energy_req(220))
        )
    ),
    "Eddy Channels": lambda loadout: (
        (meanderingPassage in loadout) and  # exit
        (
            # all the ways to get to the eddy entrance
            # this section similar to sediment flow and sediment floor
            ((
                (OceanShoreR in loadout) and
                ((  # from left
                    (SandLand.shaftToGreenMoon in loadout) and
                    (Super in loadout)
                ) or (  # from right
                    (SandLand.GreenMoonDown in loadout)
                ))
            ) or (
                (EleToTurbidPassageR in loadout) and
                (SandLand.turbidToSedFloor in loadout) and
                (pinkDoor in loadout)  # turbid passage to sediment floor
            ) or (
                (Super in loadout)  # from meandering
            ))
        ) and
        (Morph in loadout) and
        (SandLand.eddy in loadout) and
        (GravityBoots in loadout) and
        (loadout.has_any(DarkVisor, Tricks.dark_medium))
    ),
    "Tram To Suzi Island": lambda loadout: (
        (TramToSuziIslandR in loadout) and (GravityBoots in loadout) and (Spazer in loadout) and (Morph in loadout)
    ),
    "Portico": lambda loadout: (
        (enterSuzi in loadout) and
        (Super in loadout)
    ),
    "Tower Rock Lookout": lambda loadout: (
        (enterSuzi in loadout) and
        (pinkDoor in loadout) and
        (Aqua in loadout) and
        ((
            (SpaceJump in loadout) and
            (HiJump in loadout) and
            (SpaceJumpBoost in loadout)
            # TODO: how many sjb required?
        ) or (
            (Tricks.infinite_bomb_jump in loadout) and
            (Tricks.movement_moderate in loadout)
        ) or (
            (SpeedBooster in loadout) and
            (Tricks.movement_moderate in loadout)
        ))
    ),
    "Reef Nook": lambda loadout: (
        (enterSuzi in loadout) and
        (pinkDoor in loadout) and
        (Aqua in loadout) and
        (Morph in loadout) and
        (Suzi.crossOceans in loadout)
    ),
    "Saline Cache": lambda loadout: (
        (enterSuzi in loadout) and
        (Super in loadout) and
        (
            ((Aqua in loadout) and (canFly in loadout)) or
            (Tricks.gravity_jump in loadout) or
            (Tricks.sbj_underwater_w_hjb in loadout)
        )
    ),
    "Enervation Chamber": lambda loadout: (
        (enterSuzi in loadout) and
        (Suzi.cyphers in loadout) and
        (Hypercharge in loadout) and
        (Charge in loadout)
    ),
    "Weapon Locker": lambda loadout: (
        (pinkDoor in loadout) and
        (topOfSpaceport in loadout)
    ),
    "Aft Battery": lambda loadout: (
        (Morph in loadout) and
        (topOfSpaceport in loadout)
    ),
    "Forward Battery": lambda loadout: (
        loadout.has_all(Morph, pinkDoor, missileDamage, topOfSpaceport)
    ),
    "Gantry": lambda loadout: (
        (pinkDoor in loadout) and
        (topOfSpaceport in loadout)
    ),
    "Garden Canal": lambda loadout: (
        (NorakPerimeterBL in loadout) and
        (GravityBoots in loadout) and
        (can_use_pbs(1) in loadout) and
        (Spazer in loadout) and
        (LifeTemple.veranda in loadout) and
        (LifeTemple.waterToVeranda in loadout)
        # TODO: Might there be a reason to add logic from ElevatorToWellspringL ?
    ),
    "Sandy Burrow: Bottom": lambda loadout: (  # AmmoTank
        (OceanShoreR in loadout) and
        (SandLand.sandy_burrow in loadout) and

        (  # to get back in hole after getting this item
            (Speedball in loadout) or
            loadout.has_all(Aqua, Bombs) or
            loadout.has_all(Aqua, PowerBomb) or
            (Tricks.morph_jump_3_tile_water in loadout)
        )
    ),
    "Trophobiotic Chamber": lambda loadout: (
        (sunkenNestToVulnar in loadout) and
        (Morph in loadout) and
        ((Speedball in loadout) or (hiJumpSuperSink in loadout))
    ),
    "Waste Processing": lambda loadout: (
        (SpeedBooster in loadout) and
        ((
            # get out through intended exit hole
            (Morph in loadout) and
            ((can_bomb(1) in loadout) or (Screw in loadout))
        ) or (
            # get out through the speedbooster blocks
            (Tricks.short_charge_3 in loadout)
        ) or (
            (Tricks.super_sink_easy in loadout)
        )) and
        ((
            (SubbasementFissureL in loadout) and
            (can_use_pbs(1) in loadout) and  # door into waste processing
            # If I didn't have speedbooster, then I would want either 2 pbs
            # or something else to kill green pirates with, because it would
            # be difficult to get up exhaust vent without killing them.
            (ServiceSector.wasteProcessingTraverse in loadout)
        ) or (
            (CellarR in loadout) and
            (pinkDoor in loadout) and  # door from cellar access to crumbling basement
            (ServiceSector.cellar in loadout)
        ) or (
            (FieldAccessL in loadout) and
            (ServiceSector.westSpore in loadout) and
            (ServiceSector.eastSpore in loadout) and
            (ServiceSector.crumblingBasement in loadout)
        ) or (
            (TransferStationR in loadout) and
            (ServiceSector.transfer in loadout) and
            (ServiceSector.crumblingBasement in loadout)
        ))
    ),
    "Grand Chasm": lambda loadout: (
        (railAccess in loadout) and (GravityBoots in loadout) and (Screw in loadout) and
        (
            # from left
            (can_bomb(6) in loadout) or
            ((can_bomb(4) in loadout) and (Speedball in loadout)) or
            # from right
            (
                (can_bomb(2) in loadout) and
                ((
                    (SpaceJump in loadout)
                ) or (
                    # without space jump you have to run a bit on spikes
                    (energy_req(121) in loadout)
                ))
            )
        )
    ),
    "Mining Site 1": lambda loadout: (  # (1 = letter Alpha)
        (GravityBoots in loadout) and
        (can_bomb(1) in loadout) and
        ((Speedball in loadout) or (Bombs in loadout) or (Tricks.morph_jump_4_tile in loadout)) and
        (pinkDoor in loadout) and
        (loadout.has_any(Ice, killRippers, Tricks.movement_moderate)) and
        ((
            (FieryGalleryL in loadout) and
            (Verdite.fieryTrail in loadout)
        ) or (
            (SporousNookL in loadout) and
            (Verdite.hotSpring in loadout)
        ))
    ),
    "Colosseum": lambda loadout: (  # GT
        (ElevatorToMagmaLakeR in loadout) and (GravityBoots in loadout) and (BossKill.gold_torizo in loadout)
    ),
    "Lava Pool": lambda loadout: (
        loadout.has_all(GravityBoots, can_bomb(1)) and
        ((
            (lava_run(664, 1258) in loadout) and (MetroidSuit in loadout)
        ) or (
            # no metroid suit
            (Varia in loadout) and (Aqua in loadout) and (energy_req(hell_run_energy(650, loadout)) in loadout)
        )) and
        ((
            (FieryGalleryL in loadout) and
            (Verdite.fieryTrail in loadout)
        ) or (
            (SporousNookL in loadout) and
            (Verdite.hotSpring in loadout)
        ))
        # TODO: logic from Hollow Chamber and Placid Pool (don't have to go through mining site beta)
    ),
    "Hive Main Chamber": lambda loadout: (
        # copy and paste infested passage
        (GravityBoots in loadout) and
        ((
            (VulnarDepthsElevatorEL in loadout) and
            (FireHive.hiveEntrance in loadout)
        ) or (
            (SequesteredInfernoL in loadout) and
            (FireHive.infernalSequestration in loadout) and
            (FireHive.crossways in loadout) and
            ((icePod in loadout) or (FireHive.westHiveTunnel in loadout))
        ) or (
            (HiveBurrowL in loadout) and
            (FireHive.hiveBurrow in loadout)
        ))
    ),
    "Crossway Cache": lambda loadout: (
        ((
            (VulnarDepthsElevatorEL in loadout) and
            (FireHive.hiveEntrance in loadout) and
            ((icePod in loadout) or (FireHive.westHiveTunnel in loadout))
        ) or (
            (SequesteredInfernoL in loadout) and
            (FireHive.infernalSequestration in loadout) and
            (FireHive.crossways in loadout)
        ) or (
            (HiveBurrowL in loadout) and
            (FireHive.hiveBurrow in loadout) and
            ((icePod in loadout) or (FireHive.westHiveTunnel in loadout))
        ) or (
            (collapsedHive in loadout) and
            (FireHive.crossways in loadout)
        ))
    ),
    "Slag Heap": lambda loadout: (
        # TODO: unit test for the requirements from different area doors
        ((
            (VulnarDepthsElevatorEL in loadout) and
            (FireHive.hiveEntrance in loadout) and
            ((icePod in loadout) or (FireHive.westHiveTunnel in loadout)) and
            (FireHive.crossways in loadout)
        ) or (
            (SequesteredInfernoL in loadout) and
            (FireHive.infernalSequestration in loadout)
        ) or (
            (collapsedHive in loadout)
        )) and
        (
            (Aqua in loadout) or (Speedball in loadout) or (Tricks.morph_jump_3_tile_water in loadout)
        ) and
        (FireHive.twisted in loadout) and
        (can_bomb(3) in loadout) and
        ((
            (MetroidSuit in loadout) and
            (lava_run(450, 640) in loadout)  # TODO: remeasure this with aqua suit
        ) or (
            loadout.has_all(Aqua, Varia, energy_req(hell_run_energy(930, loadout))) and
            loadout.has_any(Screw, Super)
        ) or (
            loadout.has_all(Aqua, Varia, can_use_pbs(1), Speedball, energy_req(hell_run_energy(705, loadout))) and
            loadout.has_any(Screw, Super)
        ))
    ),
    "Hydrodynamic Chamber": lambda loadout: (
        (GravityBoots in loadout) and
        (Spazer in loadout) and
        (Morph in loadout) and
        ((
            (doorsToWestCorridorTop in loadout) and
            (PirateLab.westCorridorToCentralTop in loadout)
        ) or (
            (doorsToCentralCorridorMid in loadout) and
            (PirateLab.centralTopToMid in loadout)
        ))
    ),
    "Central Corridor: Left": lambda loadout: (
        # don't need other area doors if everything here will get through east corridor
        (Aqua in loadout) and
        (Speedball in loadout) and
        (SpeedBooster in loadout) and
        (GravityBoots in loadout) and
        (Morph in loadout) and
        (can_bomb(1) in loadout) and
        (doorsToCentralCorridorBottom in loadout)
    ),
    "Restricted Area": lambda loadout: (
        (
            (MetroidSuit in loadout) or
            (
                (bonkCeilingSuperSink in loadout) and
                (
                    (energy_req(201) in loadout) or
                    (
                        (energy_req(151) in loadout) and
                        loadout.has_any(Varia, Aqua)
                    ) or
                    (
                        (Tricks.movement_zoast in loadout)
                        # possible to get out without taking any damage by morph rolling into pixel-perfect position
                        # then up to crouch and jump
                    )
                ) and
                (Tricks.clip_crouch in loadout)  # not a typical clip_crouch
                # How to get up through laser:
                #  1. run up the slope into the laser (with dash button)
                #  2. release everything
                #  3. tap left
                #  4. press and hold jump
                #  5. tap right
                #  6. release jump
                #  7. tap down
                #  8. jump
            )
        ) and
        (doorsToCentralCorridorMid in loadout)
    ),
    "Foundry": lambda loadout: (
        (GravityBoots in loadout) and

        (Morph in loadout) and
        # even with super sink getting through the first small passage, I couldn't get to the item without morph

        (doorsToCentralCorridorMid in loadout) and
        (
            (energy_req(129) in loadout) or
            ((MetroidSuit in loadout) and (Speedball in loadout)) or
            (Tricks.movement_zoast in loadout)
        )
    ),
    "Norak Escarpment": lambda loadout: (
        (NorakBrookL in loadout) and
        (GravityBoots in loadout) and
        (
            (canFly in loadout) or
            (
                (SpeedBooster in loadout) and
                (
                    # This shinespark is easy if vanilla area doors.
                    (loadout.game.door_pairs.other(CanyonPassageR) == NorakBrookL) or
                    # If area rando, we'll have to assume that we don't have the space to charge shinespark.
                    ((Tricks.short_charge_4 in loadout) and (Tricks.movement_zoast in loadout))  # stutter 4 tap
                    # TODO: hi jump + a short charge from bottom left that might not be as hard
                )
            )
        )
    ),
    "Glacier's Reach": lambda loadout: (
        (railAccess in loadout) and
        (GravityBoots in loadout) and
        # top of frozen trail
        ((can_bomb(1) in loadout) or (breakIce in loadout) or (
            loadout.has_all(Screw, Tricks.morphless_tunnel_crawl) and
            ((Tricks.movement_zoast in loadout) or (varia_or_hell_run(150) in loadout))
        )) and
        # bottom of frozen trail
        ((Morph in loadout) or (breakIce in loadout)) and
        ((  # hell run health can vary a lot depending on gear
            (varia_or_hell_run(386) in loadout)
        ) or (
            # don't have to climb the right wall of glacier's reach
            loadout.has_any(HiJump, SpaceJump) and
            (varia_or_hell_run(331) in loadout)  # TODO: remeasure
        ) or (
            # Wave makes a big difference to avoid getting hit by one enemy that you can shoot through the wall
            (Wave in loadout) and
            loadout.has_any(Spazer, DamageAmp) and
            (varia_or_hell_run(280) in loadout)  # TODO: remeasure
        ) or (
            # can kill blue rippers (without using ammo) for high drop rate on health
            # can farm to full health at the door between Icy Flow and Frozen Trail
            ((Screw in loadout) or (
                (Charge in loadout) and (Hypercharge in loadout)
            )) and
            (varia_or_hell_run(88) in loadout)
        ) or (
            (breakIce in loadout) and
            (varia_or_hell_run(338) in loadout)
        ))
    ),
    "Sitting Room": lambda loadout: (
        (can_use_pbs(1) in loadout) and  # might have to farm after opening door
        (GravityBoots in loadout) and
        (railAccess in loadout) and
        (SkyWorld.anticipation in loadout) and
        (varia_or_hell_run(98) in loadout) and
        ((Speedball in loadout) or (Tricks.infinite_bomb_jump in loadout) or (
            loadout.has_all(Tricks.morph_jump_3_tile, Tricks.morph_jump_4_tile)
        ) or (
            loadout.has_all(Tricks.morph_jump_4_tile, can_bomb(6))
        ))
    ),
    "Suzi Ruins Map Station Access": lambda loadout: (
        (enterSuzi in loadout) and
        (can_use_pbs(1) in loadout) and
        (Super in loadout)
    ),
    "Obscured Vestibule": lambda loadout: (
        (enterSuzi in loadout) and
        (can_bomb(1) in loadout)
    ),
    "Docking Port 3": lambda loadout: (  # (3 = letter Gamma)
        # copy and paste docking port 4
        (
            (spaceDrop not in loadout) and
            (Grapple in loadout)
        ) or (
            (spaceDrop in loadout) and
            (LoadingDockSecurityAreaL in loadout) and
            (SpacePort.loadingDock in loadout)
        )
    ),
    "Arena": lambda loadout: (
        (RuinedConcourseBL in loadout) and
        (Early.eldersTop in loadout)
    ),
    "West Spore Field": lambda loadout: (
        ((
            (sunkenNestToVulnar in loadout) and
            (Morph in loadout) and
            (loadout.has_any(Tricks.morph_jump_3_tile_up_1, can_bomb(1), Speedball)) and
            (pinkDoor in loadout)  # into west spore field
        ) or (
            (SporeFieldTR in loadout) and
            (GravityBoots in loadout)
        ) or (
            (SporeFieldBR in loadout) and
            (GravityBoots in loadout) and
            ((shootThroughWalls in loadout) or (Tricks.wave_gate_glitch in loadout))
        )) and
        ((DarkVisor in loadout) or (Tricks.dark_easy in loadout)) and
        ((
            # no super sink
            (Super in loadout) and  # door into great spore hall
            ((shootThroughWalls in loadout) or (Tricks.ggg in loadout) or (Tricks.wave_gate_glitch in loadout)) and
            ((can_bomb(1) in loadout) or ((Morph in loadout) and (Screw in loadout))) and  # great spore hall
            (pinkSwitch in loadout) and  # return through great spore hall
            # get in to item
            (
                (Speedball in loadout) or
                loadout.has_all(Aqua, SpaceJump, SpaceJumpBoost, Tricks.movement_moderate)
            ) and
            # get out (of water)
            ((Aqua in loadout) or (HiJump in loadout) or (Tricks.sbj_underwater_no_hjb in loadout))
        ) or (
            # super sink
            # enter
            (
                # For this super sink, unequip hi jump boots and press left to stand against door.
                ((bonkCeilingSuperSink in loadout) and (Speedball in loadout)) or

                (crystal_flash in loadout) or
                ((Tricks.super_sink_easy in loadout) and (Super in loadout))  # get stuck in door to Great Spore Hall
            ) and
            # exit
            (Tricks.super_sink_easy in loadout) and
            (Morph in loadout)
        ))
    ),
    "Magma Chamber": lambda loadout: (
        (ElevatorToMagmaLakeR in loadout) and
        (GravityBoots in loadout) and
        (  # one of the jumps near the entrance
            (HiJump in loadout) or
            (canFly in loadout) or
            (Tricks.wall_jump_precise in loadout) or
            (Tricks.freeze_hard in loadout)
        ) and
        (can_use_pbs(1) in loadout) and  # (return logic)
        ((
            # lower lava
            (BossKill.gold_torizo in loadout) and
            (DrayLand.lakeMonitoringStation in loadout) and
            # This is the hell run if GT is already dead. Killing GT will be a different hell run.
            (varia_or_hell_run(851, heat_and_metroid_suit_not_required=True) in loadout)
        ) or (
            # lava dive
            (MetroidSuit in loadout) and
            (lava_run(349, 750) in loadout)
            # TODO: measure number with aqua (and lava not lowered) - 750 is a guess
        ))
        # TODO: moonfall? lava dive without metroid suit?
    ),
    "Equipment Locker": lambda loadout: (
        (doorsToWestCorridorTop in loadout) and
        (GravityBoots in loadout) and
        (pinkDoor in loadout) and
        (
            (Aqua in loadout) or
            (HiJump in loadout) or
            (can_bomb(1) in loadout) or
            (Tricks.sbj_underwater_no_hjb in loadout)
        ) and
        (
            (Morph in loadout) or
            (MetroidSuit in loadout) or
            ((Tricks.morphless_tunnel_crawl in loadout) and (Tricks.super_sink_easy in loadout))
        )
    ),
    "Antelier": lambda loadout: (  # spelled "Antilier" in subversion 1.1
        (GravityBoots in loadout) and
        ((
            (doorsToWestCorridorTop in loadout) and
            (PirateLab.westCorridorToCentralTop in loadout) and
            ((PirateLab.waterGauntlet_oneWay in loadout) or (
                # backdoor main hydrology research
                loadout.has_any(Aqua, HiJump, Tricks.sbj_underwater_no_hjb, Tricks.xray_climb)
            ))
        ) or (
            (doorsToCentralCorridorMid in loadout) and
            (PirateLab.centralTopToMid in loadout) and
            # backdoor main hydrology research
            loadout.has_any(Aqua, HiJump, Tricks.sbj_underwater_no_hjb, Tricks.xray_climb)
        )) and
        (PirateLab.exitMainHydrologyResearch in loadout)
        # can gravity jump (no Aqua Suit)
        # through hydrodynamic chamber door into main hydrology research from central corridor
    ),
    "Weapon Research": lambda loadout: (
        (GravityBoots in loadout) and
        (
            loadout.has_any(shootThroughWalls, plasmaSBA, spazerSBA, MetroidSuit, bonkCeilingSuperSink) or

            ((iceSBA in loadout) and (Tricks.movement_moderate in loadout))
            # Stand in the middle of the last tile of the ledge, above the laser.
            # The sound of the Ice SBA, has an oscillating pitch.
            # Consider the highest pitch to be the beat. Start counting with 1.
            # On beat 19 (beat 3 of the 5th measure of 4/4), jump,
            # and morph or aim down before hitting the ceiling.
        ) and
        (
            (can_bomb(5) in loadout) or
            ((can_bomb(4) in loadout) and (Tricks.movement_moderate in loadout)) or
            ((can_bomb(3) in loadout) and (Tricks.movement_zoast in loadout)) or
            ((Spazer in loadout) and (Morph in loadout))
        ) and
        (doorsToCentralCorridorMid in loadout)
        # TODO: energy or movement or something to kill red pirates?
    ),
    "Crocomire's Lair": lambda loadout: (
        # similar to crocomire energy station, except don't need to go through bomb blocks on left
        (GravityBoots in loadout) and
        (norakToLifeTemple in loadout) and
        (LifeTemple.veranda in loadout) and
        (LifeTemple.waterToVeranda in loadout) and
        (SpeedBooster in loadout) and
        (Super in loadout)  # door to elevator to jungle's heart
    ),
}
