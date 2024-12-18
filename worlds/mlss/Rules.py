import typing

from worlds.generic.Rules import add_rule, forbid_item
from .Names.LocationName import LocationName
from .Locations import all_locations, hidden
from . import StateLogic

if typing.TYPE_CHECKING:
    from . import MLSSWorld


def set_rules(world: "MLSSWorld", excluded):
    for location in all_locations:
        if "Digspot" in location.name:
            if (world.options.skip_minecart and "Minecart" in location.name) or (
                    world.options.castle_skip and "Bowser" in location.name
            ):
                continue
            if world.options.chuckle_beans == 0 or world.options.chuckle_beans == 1 and location.id in hidden:
                continue
            add_rule(
                world.get_location(location.name),
                lambda state: StateLogic.canDig(state, world.player),
            )
        if "Beanstone" in location.name:
            add_rule(
                world.get_location(location.name),
                lambda state: StateLogic.canDig(state, world.player),
            )
        if "Shop" in location.name and "Coffee" not in location.name and location.name not in excluded:
            forbid_item(world.get_location(location.name), "Hammers", world.player)
            if "Badge" in location.name or "Pants" in location.name:
                add_rule(
                    world.get_location(location.name),
                    lambda state: StateLogic.brooch(state, world.player) or StateLogic.rose(state, world.player),
                )
        if location.itemType != 0 and location.name not in excluded:
            if "Bowser" in location.name and world.options.castle_skip:
                continue
            forbid_item(world.get_location(location.name), "5 Coins", world.player)

    if world.options.chuckle_beans == 2:
        add_rule(
            world.get_location(LocationName.HoohooVillageSuperHammerCaveDigspot),
            lambda state: StateLogic.canCrash(state, world.player) or StateLogic.super(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.BeanbeanOutskirtsFarmRoomDigspot2),
            lambda state: StateLogic.thunder(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.BeanbeanOutskirtsFarmRoomDigspot3),
            lambda state: StateLogic.thunder(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.ChucklehuckWoodsWhiteFruitRoomDigspot3),
            lambda state: StateLogic.canMini(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.JokesEndJojoraRoomDigspot),
            lambda state: StateLogic.canDash(state, world.player),
        )

    if world.options.chuckle_beans != 0:
        add_rule(
            world.get_location(LocationName.HoohooMountainBaseBoostatueRoomDigspot2),
            lambda state: StateLogic.canCrash(state, world.player) or StateLogic.super(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.BeanbeanOutskirtsFarmRoomDigspot1),
            lambda state: StateLogic.thunder(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.ChucklehuckWoodsWhiteFruitRoomDigspot2),
            lambda state: StateLogic.canMini(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.TeeheeValleyPastUltraHammersDigspot1),
            lambda state: StateLogic.ultra(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.TeeheeValleyPastUltraHammersDigspot3),
            lambda state: StateLogic.ultra(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.BeanbeanOutskirtsNorthBeachDigspot3),
            lambda state: StateLogic.canDash(state, world.player) or StateLogic.super(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.BeanbeanOutskirtsEDigspot2),
            lambda state: StateLogic.thunder(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.BeanbeanOutskirtsNEDigspot1),
            lambda state: StateLogic.thunder(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.BeanbeanOutskirtsSRoom1Digspot2),
            lambda state: StateLogic.ultra(state, world.player) and StateLogic.thunder(state, world.player),
        )

    forbid_item(
        world.get_location(LocationName.SSChuckolaMembershipCard), "Nuts", world.player
    )  # Bandaid Fix

    add_rule(
        world.get_location(LocationName.HoohooVillageHammerHouseBlock),
        lambda state: StateLogic.hammers(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.HoohooMountainBaseBoostatueRoomBlock2),
        lambda state: StateLogic.canCrash(state, world.player) or StateLogic.super(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.BeanbeanOutskirtsBooStatueMole),
        lambda state: StateLogic.canMini(state, world.player) and StateLogic.canDig(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.HoohooVillageSuperHammerCaveBlock),
        lambda state: StateLogic.canCrash(state, world.player) or StateLogic.super(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.BeanbeanOutskirtsFarmRoomMoleReward1),
        lambda state: StateLogic.thunder(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.BeanbeanOutskirtsFarmRoomMoleReward2),
        lambda state: StateLogic.thunder(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.BeanbeanOutskirtsThunderHandMole),
        lambda state: StateLogic.thunder(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.BeanbeanOutskirtsNWBlock),
        lambda state: StateLogic.super(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.BeanbeanOutskirtsBeanFruit1),
        lambda state: StateLogic.canDig(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.BeanbeanOutskirtsBeanFruit2),
        lambda state: StateLogic.canDig(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.BeanbeanOutskirtsBeanFruit3),
        lambda state: StateLogic.canDig(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.BeanbeanOutskirtsBeanFruit4),
        lambda state: StateLogic.super(state, world.player) and StateLogic.canDig(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.BeanbeanOutskirtsBeanFruit5),
        lambda state: StateLogic.super(state, world.player) and StateLogic.canDig(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.BeanbeanOutskirtsBeanFruit6),
        lambda state: StateLogic.canDig(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.BeanbeanOutskirtsBeanFruit7),
        lambda state: StateLogic.teehee(state, world.player) and StateLogic.canDig(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.BeanbeanOutskirtsSRoom1Block),
        lambda state: StateLogic.ultra(state, world.player) and StateLogic.thunder(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.BeanbeanOutskirtsSRoom2Block1),
        lambda state: StateLogic.canDig(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.WoohooHooniversityMiniMarioPuzzleSecretAreaBlock1),
        lambda state: StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.WoohooHooniversityMiniMarioPuzzleSecretAreaBlock2),
        lambda state: StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.WoohooHooniversityMiniMarioPuzzleSecretAreaBlock3),
        lambda state: StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.WoohooHooniversityMiniMarioPuzzleSecretAreaBlock4),
        lambda state: StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.WoohooHooniversityMiniMarioPuzzleBlock),
        lambda state: StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.BeanbeanOutskirtsSecretScroll1),
        lambda state: StateLogic.thunder(state, world.player) and StateLogic.super(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.BeanbeanOutskirtsSecretScroll2),
        lambda state: StateLogic.thunder(state, world.player) and StateLogic.ultra(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.HoohooVillageMoleBehindTurtle),
        lambda state: StateLogic.canDash(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.BeanbeanOutskirtsNESoloMarioMole1),
        lambda state: StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.BeanbeanOutskirtsNESoloMarioMole2),
        lambda state: StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.BeanbeanOutskirtsSuperHammerUpgrade),
        lambda state: StateLogic.thunder(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.BeanbeanOutskirtsUltraHammerUpgrade),
        lambda state: StateLogic.thunder(state, world.player)
                      and StateLogic.pieces(state, world.player)
                      and StateLogic.castleTown(state, world.player)
                      and StateLogic.rose(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.BeanbeanOutskirtsSoloLuigiCaveMole),
        lambda state: StateLogic.canDig(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.ChucklehuckWoodsRedChuckolaFruit),
        lambda state: StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.ChucklehuckWoodsWhiteChuckolaFruit),
        lambda state: StateLogic.canDig(state, world.player) and StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.ChucklehuckWoodsPastChucklerootBlock1),
        lambda state: StateLogic.fruits(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.ChucklehuckWoodsPastChucklerootBlock2),
        lambda state: StateLogic.fruits(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.ChucklehuckWoodsPastChucklerootBlock3),
        lambda state: StateLogic.fruits(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.ChucklehuckWoodsPastChucklerootBlock4),
        lambda state: StateLogic.fruits(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.ChucklehuckWoodsPastChucklerootBlock5),
        lambda state: StateLogic.fruits(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.ChucklehuckWoodsPastChucklerootBlock6),
        lambda state: StateLogic.fruits(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.ChucklehuckWoodsRoom7Block1),
        lambda state: StateLogic.hammers(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.ChucklehuckWoodsRoom7Block2),
        lambda state: StateLogic.hammers(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.ChucklehuckWoodsRoom4Block1),
        lambda state: StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.ChucklehuckWoodsRoom4Block2),
        lambda state: StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.ChucklehuckWoodsRoom4Block3),
        lambda state: StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.ChucklehuckWoodsPipeRoomBlock1),
        lambda state: StateLogic.hammers(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.ChucklehuckWoodsPipeRoomBlock2),
        lambda state: StateLogic.hammers(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.BeanbeanCastleTownMiniMarioBlock1),
        lambda state: StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.BeanbeanCastleTownMiniMarioBlock2),
        lambda state: StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.BeanbeanCastleTownMiniMarioBlock3),
        lambda state: StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.BeanbeanCastleTownMiniMarioBlock4),
        lambda state: StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.BeanbeanCastleTownMiniMarioBlock5),
        lambda state: StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.BeanbeanCastleFakeBeastar),
        lambda state: StateLogic.pieces(state, world.player) and StateLogic.rose(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.BeanbeanCastlePeachsExtraDress),
        lambda state: StateLogic.pieces(state, world.player) and StateLogic.rose(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.SewersRoom5Block1),
        lambda state: StateLogic.hammers(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.SewersRoom5Block2),
        lambda state: StateLogic.hammers(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.GwarharLagoonFirstUnderwaterAreaRoom1Block),
        lambda state: StateLogic.canDash(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.GwarharLagoonFirstUnderwaterAreaRoom2Block1),
        lambda state: StateLogic.canDash(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.GwarharLagoonFirstUnderwaterAreaRoom2Block2),
        lambda state: StateLogic.canDash(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.GwarharLagoonRedPearlBean),
        lambda state: StateLogic.fire(state, world.player) and StateLogic.thunder(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.GwarharLagoonGreenPearlBean),
        lambda state: StateLogic.fire(state, world.player) and StateLogic.thunder(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.TeeheeValleyPastUltraHammersBlock1),
        lambda state: StateLogic.ultra(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.TeeheeValleyPastUltraHammersBlock2),
        lambda state: StateLogic.ultra(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.OhoOasisFirebrand),
        lambda state: StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.OhoOasisThunderhand),
        lambda state: StateLogic.canDig(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.BeanstarPieceYoshiTheater),
        lambda state: StateLogic.neon(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.YoshiTheaterAzureYoshi),
        lambda state: StateLogic.beanFruit(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.YoshiTheaterBlueYoshi),
        lambda state: StateLogic.beanFruit(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.YoshiTheaterGreenYoshi),
        lambda state: StateLogic.beanFruit(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.YoshiTheaterOrangeYoshi),
        lambda state: StateLogic.beanFruit(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.YoshiTheaterPurpleYoshi),
        lambda state: StateLogic.beanFruit(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.YoshiTheaterRedYoshi),
        lambda state: StateLogic.beanFruit(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.YoshiTheaterYellowYoshi),
        lambda state: StateLogic.beanFruit(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.WinkleAreaBeanstarRoomBlock),
        lambda state: StateLogic.winkle(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.BeanstarPieceWinkleArea),
        lambda state: StateLogic.winkle(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.GwarharLagoonSpangleReward),
        lambda state: StateLogic.spangle(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.PantsShopMomPiranhaFlag1),
        lambda state: StateLogic.brooch(state, world.player) or StateLogic.rose(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.PantsShopMomPiranhaFlag2),
        lambda state: StateLogic.brooch(state, world.player) or StateLogic.rose(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.PantsShopMomPiranhaFlag3),
        lambda state: StateLogic.brooch(state, world.player) or StateLogic.rose(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.BadgeShopMomPiranhaFlag1),
        lambda state: StateLogic.brooch(state, world.player) or StateLogic.rose(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.BadgeShopMomPiranhaFlag2),
        lambda state: StateLogic.brooch(state, world.player) or StateLogic.rose(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.BadgeShopMomPiranhaFlag3),
        lambda state: StateLogic.brooch(state, world.player) or StateLogic.rose(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.ChateauGreenGoblet),
        lambda state: StateLogic.brooch(state, world.player) and StateLogic.canDig(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.ChateauRedGoblet),
        lambda state: StateLogic.brooch(state, world.player) and StateLogic.canMini(state, world.player),
    )

    add_rule(
        world.get_location(LocationName.GwarharLagoonSpangle),
        lambda state: StateLogic.ultra(state, world.player),
    )
    add_rule(
        world.get_location(LocationName.GwarharLagoonSpangleRoomBlock),
        lambda state: StateLogic.ultra(state, world.player),
    )
    if world.options.difficult_logic:
        add_rule(
            world.get_location(LocationName.GwarharLagoonSpangleReward),
            lambda state: StateLogic.canCrash(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.BeanstarPieceHermie),
            lambda state: StateLogic.canCrash(state, world.player),
        )
        if world.options.chuckle_beans != 0:
            add_rule(
                world.get_location(LocationName.GwarharLagoonPastHermieDigspot),
                lambda state: StateLogic.canCrash(state, world.player),
            )

    if world.options.randomize_bosses.value != 0:
        if world.options.chuckle_beans != 0:
            add_rule(
                world.get_location(LocationName.HoohooMountainHoohoorosRoomDigspot1),
                lambda state: StateLogic.hammers(state, world.player)
                              or StateLogic.fire(state, world.player)
                              or StateLogic.thunder(state, world.player),
            )
            add_rule(
                world.get_location(LocationName.HoohooMountainPastHoohoorosDigspot),
                lambda state: StateLogic.hammers(state, world.player)
                              or StateLogic.fire(state, world.player)
                              or StateLogic.thunder(state, world.player),
            )
            add_rule(
                world.get_location(LocationName.HoohooMountainPastHoohoorosConnectorRoomDigspot1),
                lambda state: StateLogic.hammers(state, world.player)
                              or StateLogic.fire(state, world.player)
                              or StateLogic.thunder(state, world.player),
            )
            add_rule(
                world.get_location(LocationName.HoohooMountainBelowSummitDigspot),
                lambda state: StateLogic.hammers(state, world.player)
                              or StateLogic.fire(state, world.player)
                              or StateLogic.thunder(state, world.player),
            )
            add_rule(
                world.get_location(LocationName.HoohooMountainSummitDigspot),
                lambda state: StateLogic.hammers(state, world.player)
                              or StateLogic.fire(state, world.player)
                              or StateLogic.thunder(state, world.player),
            )
            if world.options.chuckle_beans == 2:
                add_rule(
                    world.get_location(LocationName.HoohooMountainHoohoorosRoomDigspot2),
                    lambda state: StateLogic.hammers(state, world.player)
                                  or StateLogic.fire(state, world.player)
                                  or StateLogic.thunder(state, world.player),
                )
                add_rule(
                    world.get_location(LocationName.HoohooMountainPastHoohoorosConnectorRoomDigspot2),
                    lambda state: StateLogic.hammers(state, world.player)
                                  or StateLogic.fire(state, world.player)
                                  or StateLogic.thunder(state, world.player),
                )
        add_rule(
            world.get_location(LocationName.HoohooVillageHammers),
            lambda state: StateLogic.hammers(state, world.player)
                          or StateLogic.fire(state, world.player)
                          or StateLogic.thunder(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.HoohooMountainPeasleysRose),
            lambda state: StateLogic.hammers(state, world.player)
                          or StateLogic.fire(state, world.player)
                          or StateLogic.thunder(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.HoohooMountainHoohoorosRoomBlock1),
            lambda state: StateLogic.hammers(state, world.player)
                          or StateLogic.fire(state, world.player)
                          or StateLogic.thunder(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.HoohooMountainHoohoorosRoomBlock2),
            lambda state: StateLogic.hammers(state, world.player)
                          or StateLogic.fire(state, world.player)
                          or StateLogic.thunder(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.HoohooMountainBelowSummitBlock1),
            lambda state: StateLogic.hammers(state, world.player)
                          or StateLogic.fire(state, world.player)
                          or StateLogic.thunder(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.HoohooMountainBelowSummitBlock2),
            lambda state: StateLogic.hammers(state, world.player)
                          or StateLogic.fire(state, world.player)
                          or StateLogic.thunder(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.HoohooMountainBelowSummitBlock3),
            lambda state: StateLogic.hammers(state, world.player)
                          or StateLogic.fire(state, world.player)
                          or StateLogic.thunder(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.HoohooMountainPastHoohoorosBlock1),
            lambda state: StateLogic.hammers(state, world.player)
                          or StateLogic.fire(state, world.player)
                          or StateLogic.thunder(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.HoohooMountainPastHoohoorosBlock2),
            lambda state: StateLogic.hammers(state, world.player)
                          or StateLogic.fire(state, world.player)
                          or StateLogic.thunder(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.HoohooMountainPastHoohoorosConnectorRoomBlock),
            lambda state: StateLogic.hammers(state, world.player)
                          or StateLogic.fire(state, world.player)
                          or StateLogic.thunder(state, world.player),
        )

    if not world.options.difficult_logic:
        if world.options.chuckle_beans != 0:
            add_rule(
                world.get_location(LocationName.JokesEndNortheastOfBoilerRoom2Digspot),
                lambda state: StateLogic.canCrash(state, world.player),
            )
            add_rule(
                world.get_location(LocationName.JokesEndNortheastOfBoilerRoom3Digspot),
                lambda state: StateLogic.canCrash(state, world.player),
            )
        add_rule(
            world.get_location(LocationName.JokesEndNortheastOfBoilerRoom1Block),
            lambda state: StateLogic.canCrash(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.JokesEndNortheastOfBoilerRoom2Block1),
            lambda state: StateLogic.canCrash(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.JokesEndFurnaceRoom1Block1),
            lambda state: StateLogic.canCrash(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.JokesEndFurnaceRoom1Block2),
            lambda state: StateLogic.canCrash(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.JokesEndFurnaceRoom1Block3),
            lambda state: StateLogic.canCrash(state, world.player),
        )

    if world.options.coins:
        add_rule(
            world.get_location(LocationName.HoohooMountainBaseBooStatueCaveCoinBlock1),
            lambda state: StateLogic.canCrash(state, world.player) or StateLogic.super(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.HoohooMountainBaseBooStatueCaveCoinBlock2),
            lambda state: StateLogic.canCrash(state, world.player) or StateLogic.super(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.HoohooMountainBaseBooStatueCaveCoinBlock3),
            lambda state: StateLogic.canCrash(state, world.player) or StateLogic.super(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.BeanbeanOutskirtsNWCoinBlock),
            lambda state: StateLogic.super(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.BeanbeanOutskirtsSRoom1CoinBlock),
            lambda state: StateLogic.ultra(state, world.player) and StateLogic.thunder(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.BeanbeanOutskirtsSRoom2CoinBlock),
            lambda state: StateLogic.canCrash(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.ChateauPoppleRoomCoinBlock1),
            lambda state: StateLogic.brooch(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.ChateauPoppleRoomCoinBlock2),
            lambda state: StateLogic.brooch(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.ChucklehuckWoodsCaveRoom1CoinBlock),
            lambda state: StateLogic.brooch(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.ChucklehuckWoodsCaveRoom2CoinBlock),
            lambda state: StateLogic.brooch(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.ChucklehuckWoodsCaveRoom3CoinBlock),
            lambda state: StateLogic.brooch(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.ChucklehuckWoodsPipe5RoomCoinBlock),
            lambda state: StateLogic.brooch(state, world.player) and StateLogic.hammers(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.ChucklehuckWoodsRoom7CoinBlock),
            lambda state: StateLogic.brooch(state, world.player) and StateLogic.hammers(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.ChucklehuckWoodsPastChucklerootCoinBlock),
            lambda state: StateLogic.brooch(state, world.player) and StateLogic.fruits(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.ChucklehuckWoodsKoopaRoomCoinBlock),
            lambda state: StateLogic.brooch(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.ChucklehuckWoodsWinkleAreaCaveCoinBlock),
            lambda state: StateLogic.brooch(state, world.player) and StateLogic.canDash(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.SewersPrisonRoomCoinBlock),
            lambda state: StateLogic.rose(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.TeeheeValleyPastUltraHammerRocksCoinBlock),
            lambda state: StateLogic.ultra(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.SSChuckolaStorageRoomCoinBlock1),
            lambda state: StateLogic.super(state, world.player) or StateLogic.canDash(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.SSChuckolaStorageRoomCoinBlock2),
            lambda state: StateLogic.super(state, world.player) or StateLogic.canDash(state, world.player),
        )
        add_rule(
            world.get_location(LocationName.GwarharLagoonFirstUnderwaterAreaRoom2CoinBlock),
            lambda state: StateLogic.canDash(state, world.player)
                            and (StateLogic.membership(state, world.player) or StateLogic.surfable(state, world.player)),
        )
        add_rule(
            world.get_location(LocationName.JokesEndSecondFloorWestRoomCoinBlock),
            lambda state: StateLogic.ultra(state, world.player)
                          and StateLogic.fire(state, world.player)
                          and (StateLogic.membership(state, world.player)
                          or (StateLogic.canDig(state, world.player)
                          and StateLogic.canMini(state, world.player))),
        )
        add_rule(
            world.get_location(LocationName.JokesEndNorthofBridgeRoomCoinBlock),
            lambda state: StateLogic.ultra(state, world.player)
                          and StateLogic.fire(state, world.player)
                          and StateLogic.canDig(state, world.player)
                          and (StateLogic.membership(state, world.player)
                          or StateLogic.canMini(state, world.player)),
        )
        if not world.options.difficult_logic:
            add_rule(
                world.get_location(LocationName.JokesEndNorthofBridgeRoomCoinBlock),
                lambda state: StateLogic.canCrash(state, world.player),
            )
