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
                world.multiworld.get_location(location.name, world.player),
                lambda state: StateLogic.canDig(state, world.player),
            )
        if "Beanstone" in location.name:
            add_rule(
                world.multiworld.get_location(location.name, world.player),
                lambda state: StateLogic.canDig(state, world.player),
            )
        if "Shop" in location.name and "Coffee" not in location.name and location.name not in excluded:
            forbid_item(world.multiworld.get_location(location.name, world.player), "Hammers", world.player)
            if "Badge" in location.name or "Pants" in location.name:
                add_rule(
                    world.multiworld.get_location(location.name, world.player),
                    lambda state: StateLogic.brooch(state, world.player) or StateLogic.rose(state, world.player),
                )
        if location.itemType != 0 and location.name not in excluded:
            if "Bowser" in location.name and world.options.castle_skip:
                continue
            forbid_item(world.multiworld.get_location(location.name, world.player), "5 Coins", world.player)

    if world.options.chuckle_beans == 2:
        add_rule(
            world.multiworld.get_location(LocationName.HoohooVillageSuperHammerCaveDigspot, world.player),
            lambda state: StateLogic.canCrash(state, world.player) or StateLogic.super(state, world.player),
        )
        add_rule(
            world.multiworld.get_location(LocationName.BeanbeanOutskirtsFarmRoomDigspot2, world.player),
            lambda state: StateLogic.thunder(state, world.player),
        )
        add_rule(
            world.multiworld.get_location(LocationName.BeanbeanOutskirtsFarmRoomDigspot3, world.player),
            lambda state: StateLogic.thunder(state, world.player),
        )
        add_rule(
            world.multiworld.get_location(LocationName.ChucklehuckWoodsWhiteFruitRoomDigspot3, world.player),
            lambda state: StateLogic.canMini(state, world.player),
        )
        add_rule(
            world.multiworld.get_location(LocationName.JokesEndJojoraRoomDigspot, world.player),
            lambda state: StateLogic.canDash(state, world.player),
        )

    if world.options.chuckle_beans == 1 or world.options.chuckle_beans == 2:
        add_rule(
            world.multiworld.get_location(LocationName.HoohooMountainBaseBoostatueRoomDigspot2, world.player),
            lambda state: StateLogic.canCrash(state, world.player) or StateLogic.super(state, world.player),
        )
        add_rule(
            world.multiworld.get_location(LocationName.BeanbeanOutskirtsFarmRoomDigspot1, world.player),
            lambda state: StateLogic.thunder(state, world.player),
        )
        add_rule(
            world.multiworld.get_location(LocationName.ChucklehuckWoodsWhiteFruitRoomDigspot2, world.player),
            lambda state: StateLogic.canMini(state, world.player),
        )
        add_rule(
            world.multiworld.get_location(LocationName.TeeheeValleyPastUltraHammersDigspot1, world.player),
            lambda state: StateLogic.ultra(state, world.player),
        )
        add_rule(
            world.multiworld.get_location(LocationName.TeeheeValleyPastUltraHammersDigspot3, world.player),
            lambda state: StateLogic.ultra(state, world.player),
        )
        add_rule(
            world.multiworld.get_location(LocationName.BeanbeanOutskirtsNorthBeachDigspot3, world.player),
            lambda state: StateLogic.canDash(state, world.player) or StateLogic.super(state, world.player),
        )
        add_rule(
            world.multiworld.get_location(LocationName.BeanbeanOutskirtsEDigspot2, world.player),
            lambda state: StateLogic.thunder(state, world.player),
        )
        add_rule(
            world.multiworld.get_location(LocationName.BeanbeanOutskirtsNEDigspot1, world.player),
            lambda state: StateLogic.thunder(state, world.player),
        )
        add_rule(
            world.multiworld.get_location(LocationName.BeanbeanOutskirtsSRoom1Digspot2, world.player),
            lambda state: StateLogic.ultra(state, world.player) and StateLogic.thunder(state, world.player),
        )

    forbid_item(
        world.multiworld.get_location(LocationName.SSChuckolaMembershipCard, world.player), "Nuts", world.player
    )  # Bandaid Fix

    add_rule(
        world.multiworld.get_location(LocationName.HoohooVillageHammerHouseBlock, world.player),
        lambda state: StateLogic.hammers(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.HoohooMountainBaseBoostatueRoomBlock2, world.player),
        lambda state: StateLogic.canCrash(state, world.player) or StateLogic.super(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.BeanbeanOutskirtsBooStatueMole, world.player),
        lambda state: StateLogic.canMini(state, world.player) and StateLogic.canDig(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.HoohooVillageSuperHammerCaveBlock, world.player),
        lambda state: StateLogic.canCrash(state, world.player) or StateLogic.super(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.BeanbeanOutskirtsFarmRoomMoleReward1, world.player),
        lambda state: StateLogic.thunder(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.BeanbeanOutskirtsFarmRoomMoleReward2, world.player),
        lambda state: StateLogic.thunder(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.BeanbeanOutskirtsThunderHandMole, world.player),
        lambda state: StateLogic.thunder(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.BeanbeanOutskirtsNWBlock, world.player),
        lambda state: StateLogic.super(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.BeanbeanOutskirtsBeanFruit1, world.player),
        lambda state: StateLogic.canDig(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.BeanbeanOutskirtsBeanFruit2, world.player),
        lambda state: StateLogic.canDig(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.BeanbeanOutskirtsBeanFruit3, world.player),
        lambda state: StateLogic.canDig(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.BeanbeanOutskirtsBeanFruit4, world.player),
        lambda state: StateLogic.super(state, world.player) and StateLogic.canDig(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.BeanbeanOutskirtsBeanFruit5, world.player),
        lambda state: StateLogic.super(state, world.player) and StateLogic.canDig(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.BeanbeanOutskirtsBeanFruit6, world.player),
        lambda state: StateLogic.canDig(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.BeanbeanOutskirtsBeanFruit7, world.player),
        lambda state: StateLogic.teehee(state, world.player) and StateLogic.canDig(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.BeanbeanOutskirtsSRoom1Block, world.player),
        lambda state: StateLogic.ultra(state, world.player) and StateLogic.thunder(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.BeanbeanOutskirtsSRoom2Block1, world.player),
        lambda state: StateLogic.canDig(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.WoohooHooniversityMiniMarioPuzzleSecretAreaBlock1, world.player),
        lambda state: StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.WoohooHooniversityMiniMarioPuzzleSecretAreaBlock2, world.player),
        lambda state: StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.WoohooHooniversityMiniMarioPuzzleSecretAreaBlock3, world.player),
        lambda state: StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.WoohooHooniversityMiniMarioPuzzleSecretAreaBlock4, world.player),
        lambda state: StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.WoohooHooniversityMiniMarioPuzzleBlock, world.player),
        lambda state: StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.BeanbeanOutskirtsSecretScroll1, world.player),
        lambda state: StateLogic.thunder(state, world.player) and StateLogic.super(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.BeanbeanOutskirtsSecretScroll2, world.player),
        lambda state: StateLogic.thunder(state, world.player) and StateLogic.ultra(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.HoohooVillageMoleBehindTurtle, world.player),
        lambda state: StateLogic.canDash(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.BeanbeanOutskirtsNESoloMarioMole1, world.player),
        lambda state: StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.BeanbeanOutskirtsNESoloMarioMole2, world.player),
        lambda state: StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.BeanbeanOutskirtsSuperHammerUpgrade, world.player),
        lambda state: StateLogic.thunder(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.BeanbeanOutskirtsUltraHammerUpgrade, world.player),
        lambda state: StateLogic.thunder(state, world.player)
        and StateLogic.pieces(state, world.player)
        and StateLogic.castleTown(state, world.player)
        and StateLogic.rose(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.BeanbeanOutskirtsSoloLuigiCaveMole, world.player),
        lambda state: StateLogic.canDig(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.ChucklehuckWoodsRedChuckolaFruit, world.player),
        lambda state: StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.ChucklehuckWoodsWhiteChuckolaFruit, world.player),
        lambda state: StateLogic.canDig(state, world.player) and StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.ChucklehuckWoodsAfterChucklerootBlock1, world.player),
        lambda state: StateLogic.fruits(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.ChucklehuckWoodsAfterChucklerootBlock2, world.player),
        lambda state: StateLogic.fruits(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.ChucklehuckWoodsAfterChucklerootBlock3, world.player),
        lambda state: StateLogic.fruits(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.ChucklehuckWoodsAfterChucklerootBlock4, world.player),
        lambda state: StateLogic.fruits(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.ChucklehuckWoodsAfterChucklerootBlock5, world.player),
        lambda state: StateLogic.fruits(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.ChucklehuckWoodsAfterChucklerootBlock6, world.player),
        lambda state: StateLogic.fruits(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.ChucklehuckWoodsRoom7Block1, world.player),
        lambda state: StateLogic.hammers(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.ChucklehuckWoodsRoom7Block2, world.player),
        lambda state: StateLogic.hammers(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.ChucklehuckWoodsRoom4Block1, world.player),
        lambda state: StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.ChucklehuckWoodsRoom4Block2, world.player),
        lambda state: StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.ChucklehuckWoodsRoom4Block3, world.player),
        lambda state: StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.ChucklehuckWoodsPipeRoomBlock1, world.player),
        lambda state: StateLogic.hammers(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.ChucklehuckWoodsPipeRoomBlock2, world.player),
        lambda state: StateLogic.hammers(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.BeanbeanCastleTownMiniMarioBlock1, world.player),
        lambda state: StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.BeanbeanCastleTownMiniMarioBlock2, world.player),
        lambda state: StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.BeanbeanCastleTownMiniMarioBlock3, world.player),
        lambda state: StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.BeanbeanCastleTownMiniMarioBlock4, world.player),
        lambda state: StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.BeanbeanCastleTownMiniMarioBlock5, world.player),
        lambda state: StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.BeanbeanCastleFakeBeastar, world.player),
        lambda state: StateLogic.pieces(state, world.player) and StateLogic.rose(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.BeanbeanCastlePeachsExtraDress, world.player),
        lambda state: StateLogic.pieces(state, world.player) and StateLogic.rose(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.SewersRoom5Block1, world.player),
        lambda state: StateLogic.hammers(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.SewersRoom5Block2, world.player),
        lambda state: StateLogic.hammers(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.GwarharLagoonFirstUnderwaterAreaRoom1Block, world.player),
        lambda state: StateLogic.canDash(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.GwarharLagoonFirstUnderwaterAreaRoom2Block1, world.player),
        lambda state: StateLogic.canDash(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.GwarharLagoonFirstUnderwaterAreaRoom2Block2, world.player),
        lambda state: StateLogic.canDash(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.GwarharLagoonRedPearlBean, world.player),
        lambda state: StateLogic.fire(state, world.player) and StateLogic.thunder(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.GwarharLagoonGreenPearlBean, world.player),
        lambda state: StateLogic.fire(state, world.player) and StateLogic.thunder(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.TeeheeValleyPastUltraHammersBlock1, world.player),
        lambda state: StateLogic.ultra(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.TeeheeValleyPastUltraHammersBlock2, world.player),
        lambda state: StateLogic.ultra(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.TeeheeValleySoloLuigiMazeRoom1Block, world.player),
        lambda state: StateLogic.ultra(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.OhoOasisFirebrand, world.player),
        lambda state: StateLogic.canMini(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.OhoOasisThunderhand, world.player),
        lambda state: StateLogic.canDig(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.BeanstarPieceYoshiTheater, world.player),
        lambda state: StateLogic.neon(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.YoshiTheaterAzureYoshi, world.player),
        lambda state: StateLogic.beanFruit(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.YoshiTheaterBlueYoshi, world.player),
        lambda state: StateLogic.beanFruit(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.YoshiTheaterGreenYoshi, world.player),
        lambda state: StateLogic.beanFruit(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.YoshiTheaterOrangeYoshi, world.player),
        lambda state: StateLogic.beanFruit(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.YoshiTheaterPurpleYoshi, world.player),
        lambda state: StateLogic.beanFruit(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.YoshiTheaterRedYoshi, world.player),
        lambda state: StateLogic.beanFruit(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.YoshiTheaterYellowYoshi, world.player),
        lambda state: StateLogic.beanFruit(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.WinkleAreaBeanstarRoomBlock, world.player),
        lambda state: StateLogic.winkle(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.BeanstarPieceWinkleArea, world.player),
        lambda state: StateLogic.winkle(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.GwarharLagoonSpangleReward, world.player),
        lambda state: StateLogic.spangle(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.PantsShopMomPiranhaFlag1, world.player),
        lambda state: StateLogic.brooch(state, world.player) or StateLogic.rose(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.PantsShopMomPiranhaFlag2, world.player),
        lambda state: StateLogic.brooch(state, world.player) or StateLogic.rose(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.PantsShopMomPiranhaFlag3, world.player),
        lambda state: StateLogic.brooch(state, world.player) or StateLogic.rose(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.BadgeShopMomPiranhaFlag1, world.player),
        lambda state: StateLogic.brooch(state, world.player) or StateLogic.rose(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.BadgeShopMomPiranhaFlag2, world.player),
        lambda state: StateLogic.brooch(state, world.player) or StateLogic.rose(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.BadgeShopMomPiranhaFlag3, world.player),
        lambda state: StateLogic.brooch(state, world.player) or StateLogic.rose(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.ChateauGreenGoblet, world.player),
        lambda state: StateLogic.brooch(state, world.player) and StateLogic.canDig(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.ChateauRedGoblet, world.player),
        lambda state: StateLogic.brooch(state, world.player) and StateLogic.canMini(state, world.player),
    )

    add_rule(
        world.multiworld.get_location(LocationName.GwarharLagoonSpangle, world.player),
        lambda state: StateLogic.ultra(state, world.player),
    )
    add_rule(
        world.multiworld.get_location(LocationName.GwarharLagoonSpangleRoomBlock, world.player),
        lambda state: StateLogic.ultra(state, world.player),
    )
    if world.options.difficult_logic:
        add_rule(
            world.multiworld.get_location(LocationName.GwarharLagoonSpangleReward, world.player),
            lambda state: StateLogic.canCrash(state, world.player),
        )
        add_rule(
            world.multiworld.get_location(LocationName.BeanstarPieceHermie, world.player),
            lambda state: StateLogic.canCrash(state, world.player),
        )
        if world.options.chuckle_beans != 0:
            add_rule(
                world.multiworld.get_location(LocationName.GwarharLagoonPastHermieDigspot, world.player),
                lambda state: StateLogic.canCrash(state, world.player),
            )

    if world.options.coins:
        add_rule(
            world.multiworld.get_location(LocationName.HoohooMountainBaseBooStatueCaveCoinBlock1, world.player),
            lambda state: StateLogic.canCrash(state, world.player) or StateLogic.super(state, world.player),
        )
        add_rule(
            world.multiworld.get_location("Hoohoo Mountain Base Boo Statue Cave Coin Block 2", world.player),
            lambda state: StateLogic.canCrash(state, world.player) or StateLogic.super(state, world.player),
        )
        add_rule(
            world.multiworld.get_location("Hoohoo Mountain Base Boo Statue Cave Coin Block 3", world.player),
            lambda state: StateLogic.canCrash(state, world.player) or StateLogic.super(state, world.player),
        )
        add_rule(
            world.multiworld.get_location("Beanbean Outskirts NW Coin Block", world.player),
            lambda state: StateLogic.super(state, world.player),
        )
        add_rule(
            world.multiworld.get_location("Beanbean Outskirts S Room 1 Coin Block", world.player),
            lambda state: StateLogic.ultra(state, world.player) and StateLogic.thunder(state, world.player),
        )
        add_rule(
            world.multiworld.get_location("Beanbean Outskirts S Room 2 Coin Block", world.player),
            lambda state: StateLogic.canCrash(state, world.player),
        )
        add_rule(
            world.multiworld.get_location("Chateau Popple Room Coin Block 1", world.player),
            lambda state: StateLogic.brooch(state, world.player),
        )
        add_rule(
            world.multiworld.get_location("Chateau Popple Room Coin Block 2", world.player),
            lambda state: StateLogic.brooch(state, world.player),
        )
        add_rule(
            world.multiworld.get_location("Chucklehuck Woods Cave Room 1 Coin Block", world.player),
            lambda state: StateLogic.brooch(state, world.player),
        )
        add_rule(
            world.multiworld.get_location("Chucklehuck Woods Cave Room 2 Coin Block", world.player),
            lambda state: StateLogic.brooch(state, world.player),
        )
        add_rule(
            world.multiworld.get_location("Chucklehuck Woods Cave Room 3 Coin Block", world.player),
            lambda state: StateLogic.brooch(state, world.player),
        )
        add_rule(
            world.multiworld.get_location("Chucklehuck Woods Pipe 5 Room Coin Block", world.player),
            lambda state: StateLogic.brooch(state, world.player) and StateLogic.hammers(state, world.player),
        )
        add_rule(
            world.multiworld.get_location("Chucklehuck Woods Room 7 Coin Block", world.player),
            lambda state: StateLogic.brooch(state, world.player) and StateLogic.hammers(state, world.player),
        )
        add_rule(
            world.multiworld.get_location("Chucklehuck Woods After Chuckleroot Coin Block", world.player),
            lambda state: StateLogic.brooch(state, world.player) and StateLogic.fruits(state, world.player),
        )
        add_rule(
            world.multiworld.get_location("Chucklehuck Woods Koopa Room Coin Block", world.player),
            lambda state: StateLogic.brooch(state, world.player),
        )
        add_rule(
            world.multiworld.get_location("Chucklehuck Woods Winkle Area Cave Coin Block", world.player),
            lambda state: StateLogic.brooch(state, world.player) and StateLogic.canDash(state, world.player),
        )
        add_rule(
            world.multiworld.get_location("Sewers Prison Room Coin Block", world.player),
            lambda state: StateLogic.rose(state, world.player),
        )
        add_rule(
            world.multiworld.get_location("Teehee Valley Past Ultra Hammer Rocks Coin Block", world.player),
            lambda state: StateLogic.ultra(state, world.player),
        )
        add_rule(
            world.multiworld.get_location("S.S. Chuckola Storage Room Coin Block 1", world.player),
            lambda state: StateLogic.super(state, world.player) or StateLogic.canDash(state, world.player),
        )
        add_rule(
            world.multiworld.get_location("Gwarhar Lagoon First Underwater Area Room 2 Coin Block", world.player),
            lambda state: StateLogic.canDash(state, world.player)
            and (StateLogic.membership(state, world.player) or StateLogic.surfable(state, world.player)),
        )
        add_rule(
            world.multiworld.get_location("S.S. Chuckola Storage Room Coin Block 2", world.player),
            lambda state: StateLogic.super(state, world.player) or StateLogic.canDash(state, world.player),
        )
        add_rule(
            world.multiworld.get_location("Joke's End Second Floor West Room Coin Block", world.player),
            lambda state: StateLogic.ultra(state, world.player)
            and StateLogic.fire(state, world.player)
            and (
                StateLogic.membership(state, world.player)
                or (StateLogic.canDig(state, world.player) and StateLogic.canMini(state, world.player))
            ),
        )
        add_rule(
            world.multiworld.get_location("Joke's End North of Bridge Room Coin Block", world.player),
            lambda state: StateLogic.ultra(state, world.player)
            and StateLogic.fire(state, world.player)
            and StateLogic.canDig(state, world.player)
            and (StateLogic.membership(state, world.player) or StateLogic.canMini(state, world.player)),
        )
        if not world.options.difficult_logic:
            add_rule(
                world.multiworld.get_location("Joke's End North of Bridge Room Coin Block", world.player),
                lambda state: StateLogic.canCrash(state, world.player),
            )
