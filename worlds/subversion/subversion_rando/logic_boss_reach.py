from typing import Literal
from .connection_data import area_doors
from .item_data import Items
from .logicCommon import can_bomb, can_use_pbs, lava_run, varia_or_hell_run
from .logic_area_shortcuts import Early, FireHive, LifeTemple, SandLand, ServiceSector, SkyWorld,  Suzi
from .logic_boss_kill import BossKill
from .logic_shortcut import LogicShortcut
from .logic_shortcut_data import breakIce, can_crash_spaceport, icePod, missileDamage, pinkDoor, shootThroughWalls
from .trick_data import Tricks


class BossReach:
    kraid = LogicShortcut(lambda loadout: (
        (area_doors["OceanShoreR"] in loadout) and
        (Items.GravityBoots in loadout) and
        (SandLand.shaftToGreenMoon in loadout) and
        (SandLand.shaftToSubmarineNest in loadout) and
        (missileDamage in loadout)  # eye door
    ))

    spore_spawn = LogicShortcut(lambda loadout: (
        ((
            (area_doors["FieldAccessL"] in loadout) and
            (ServiceSector.westSpore in loadout)
        ) or (
            (area_doors["TransferStationR"] in loadout) and
            (ServiceSector.transfer in loadout) and
            (ServiceSector.eastSpore in loadout)
        )) and
        ((Items.DarkVisor in loadout) or (Tricks.dark_easy in loadout)) and
        (can_bomb(2) in loadout) and
        (Items.Morph in loadout) and
        (Items.GravityBoots in loadout) and
        # 5-tile morph jump
        (pinkDoor in loadout)  # between spore collection and spore generator access
    ))

    bomb_torizo = LogicShortcut(lambda loadout: (
        (area_doors["RuinedConcourseBL"] in loadout) and
        (Early.eldersTop in loadout)
    ))

    draygon = LogicShortcut(lambda loadout: (
        (area_doors["MagmaPumpAccessR"] in loadout) and
        (Items.GravityBoots in loadout) and
        (can_use_pbs(1) in loadout) and  # door
        (Items.Super in loadout) and
        # getting through the heat
        (lava_run(850, 1850) in loadout) and
        # hell run without aqua will require crystal flash
        (Items.MetroidSuit in loadout) and
        # open gate
        ((  # with switch
            (
                (Items.Aqua in loadout) and
                (can_bomb(2) in loadout)
            ) or (
                # no aqua
                (Items.Speedball in loadout) and
                (can_bomb(2) in loadout)  # for getting stuck in crumbles
            )
        ) or (  # shoot through gate
            (Tricks.wave_gate_glitch in loadout) and
            # This is not the normal usage of this trick, but I don't want to make a trick just for this.
            (shootThroughWalls in loadout)
        )) and
        # exit
        ((Items.Aqua in loadout) or (Items.Speedball in loadout) or (Tricks.morph_jump_3_tile_water in loadout))
    ))

    dust_torizo = LogicShortcut(lambda loadout: (
        (FireHive.twisted in loadout) and
        (FireHive.magmaFurnace in loadout) and

        ((
            (area_doors["VulnarDepthsElevatorEL"] in loadout) and
            (FireHive.hiveEntrance in loadout) and
            ((icePod in loadout) or (FireHive.westHiveTunnel in loadout)) and
            (FireHive.crossways in loadout)
        ) or (
            (area_doors["SequesteredInfernoL"] in loadout) and
            (FireHive.infernalSequestration in loadout)
        ) or (
            (area_doors["CollapsedPassageR"] in loadout) and
            (pinkDoor in loadout) and
            (FireHive.courtyardToCollapsed in loadout)
        )) and

        # corrupted hall is not in logic anywhere else

        (varia_or_hell_run(1010) in loadout) and

        # 2 ways to Fire's Bane Shrine access
        (
            (  # kill metal pirates
                loadout.has_any(Items.Spazer, Items.Plasma, Items.Charge, missileDamage) or
                (loadout.has_all(Items.SpeedBooster, Tricks.movement_moderate))
            ) or
            (  # down the middle of path of fire
                (can_bomb(1) in loadout)
            )
        ) and

        (Items.Morph in loadout)
        # TODO: take damage from ki hunters
    ))

    gold_torizo = LogicShortcut(lambda loadout: (
        (area_doors["ElevatorToMagmaLakeR"] in loadout) and
        (Items.GravityBoots in loadout) and
        (varia_or_hell_run(350) in loadout)  # hell run not measured (because always combined with kill)
    ))

    crocomire = LogicShortcut(lambda loadout: (
        ((
            (area_doors["NorakBrookL"] in loadout) and
            (LifeTemple.brook in loadout)
        ) or (
            (area_doors["NorakPerimeterBL"] in loadout) and
            (LifeTemple.perimBL in loadout)
        ) or (
            (area_doors["NorakPerimeterTR"] in loadout) and
            (Items.MetroidSuit in loadout) and
            (Items.GravityBoots in loadout)
        )) and

        (Items.GravityBoots in loadout) and
        (LifeTemple.veranda in loadout) and
        (LifeTemple.waterToVeranda in loadout) and
        (Items.SpeedBooster in loadout) and
        (Items.Super in loadout)  # door to elevator to jungle's heart
    ))

    ridley = LogicShortcut(lambda loadout: (
        # copy paste rail access
        (Items.GravityBoots in loadout) and
        (
            (
                (area_doors["WestTerminalAccessL"] in loadout) and
                (SkyWorld.westTerminal in loadout)
            ) or (
                (area_doors["MezzanineConcourseL"] in loadout) and
                (SkyWorld.mezzanineShaft in loadout)
            ) or (
                (area_doors["ElevatorToCondenserL"] in loadout) and
                (Items.Morph in loadout) and
                (breakIce in loadout) and
                (SkyWorld.condenser in loadout)
            )
        ) and

        (Items.Super in loadout) and
        (SkyWorld.anticipation in loadout)
    ))

    phantoon = LogicShortcut(lambda loadout: (
        # copy paste rail access
        (Items.GravityBoots in loadout) and
        (
            (
                (area_doors["WestTerminalAccessL"] in loadout) and
                (SkyWorld.westTerminal in loadout)
            ) or (
                (area_doors["MezzanineConcourseL"] in loadout) and
                (SkyWorld.mezzanineShaft in loadout)
            ) or (
                (area_doors["ElevatorToCondenserL"] in loadout) and
                (Items.Morph in loadout) and
                (breakIce in loadout) and
                (SkyWorld.condenser in loadout)
            )
        ) and

        # get to the item
        (Items.Super in loadout) and
        (SkyWorld.anticipation in loadout) and
        (Items.GravityBoots in loadout) and
        ((BossKill.ridley in loadout) or (
            (can_bomb(1) in loadout) and
            (loadout.has_any(Items.Bombs, Items.Speedball, Tricks.morph_jump_3_tile, Tricks.morph_jump_4_tile))
        )) and
        # get out
        ((
            (BossKill.ridley in loadout)
        ) or (
            (BossKill.phantoon in loadout) and
            (can_bomb(3) in loadout) and
            (SkyWorld.meetingHallToLeft in loadout)
        ))
    ))

    hyper_torizo = LogicShortcut(lambda loadout: (
        (area_doors["TramToSuziIslandR"] in loadout) and
        (Suzi.enter in loadout) and
        (Suzi.cyphers in loadout)
    ))

    botwoon = LogicShortcut(lambda loadout: (
        (can_crash_spaceport in loadout) and
        (area_doors["OceanShoreR"] in loadout) and
        (Items.GravityBoots in loadout) and
        (Items.Aqua in loadout)  # TODO: I haven't looked at logic closely here
    ))


_BossName = Literal[
    "kraid", "spore_spawn", "bomb_torizo", "draygon", "dust_torizo",
    "gold_torizo", "crocomire", "ridley", "phantoon", "hyper_torizo", "botwoon"
]


def reach_and_kill(b: _BossName) -> LogicShortcut:
    return LogicShortcut(lambda loadout: (
        loadout.has_all(getattr(BossReach, b), getattr(BossKill, b))
    ))
