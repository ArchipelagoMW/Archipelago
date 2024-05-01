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
                    world.options.castle_skip and "Bowser" in location.name):
                continue
            if world.options.chuckle_beans == 0 or world.options.chuckle_beans == 1 and location.id in hidden:
                continue
            add_rule(world.multiworld.get_location(location.name, world.player),
                     StateLogic.canDig(world.player))
        if "Beanstone" in location.name:
            add_rule(world.multiworld.get_location(location.name, world.player),
                     StateLogic.canDig(world.player))
        if "Shop" in location.name and "Coffee" not in location.name and location.name not in excluded:
            forbid_item(world.multiworld.get_location(location.name, world.player), "Hammers", world.player)
        if location.itemType != 0 and location.name not in excluded:
            if "Bowser" in location.name and world.options.castle_skip:
                continue
            forbid_item(world.multiworld.get_location(location.name, world.player), "5 Coins", world.player)

    if world.options.chuckle_beans == 2:
        add_rule(world.multiworld.get_location(LocationName.HoohooVillageSuperHammerCaveDigspot, world.player),
                 StateLogic.canCrash(world.player) or StateLogic.super(world.player))
        add_rule(world.multiworld.get_location(LocationName.BeanbeanOutskirtsFarmRoomDigspot2, world.player),
                 StateLogic.thunder(world.player))
        add_rule(world.multiworld.get_location(LocationName.BeanbeanOutskirtsFarmRoomDigspot3, world.player),
                 StateLogic.thunder(world.player))
        add_rule(world.multiworld.get_location(LocationName.ChucklehuckWoodsWhiteFruitRoomDigspot3, world.player),
                 StateLogic.canMini(world.player))
        add_rule(world.multiworld.get_location(LocationName.JokesEndJojoraRoomDigspot, world.player),
                 StateLogic.canDash(world.player))

    if world.options.chuckle_beans == 1 or world.options.chuckle_beans == 2:
        add_rule(world.multiworld.get_location(LocationName.HoohooMountainBaseBoostatueRoomDigspot2, world.player),
                 StateLogic.canCrash(world.player) or StateLogic.super(world.player))
        add_rule(world.multiworld.get_location(LocationName.BeanbeanOutskirtsFarmRoomDigspot1, world.player),
                 StateLogic.thunder(world.player))
        add_rule(world.multiworld.get_location(LocationName.ChucklehuckWoodsWhiteFruitRoomDigspot2, world.player),
                 StateLogic.canMini(world.player))
        add_rule(world.multiworld.get_location(LocationName.TeeheeValleyPastUltraHammersDigspot1, world.player),
                 StateLogic.ultra(world.player))
        add_rule(world.multiworld.get_location(LocationName.TeeheeValleyPastUltraHammersDigspot3, world.player),
                 StateLogic.ultra(world.player))
        add_rule(world.multiworld.get_location(LocationName.BeanbeanOutskirtsNorthBeachDigspot3, world.player),
                 StateLogic.canDash(world.player) or StateLogic.super(world.player))
        add_rule(world.multiworld.get_location(LocationName.BeanbeanOutskirtsEDigspot2, world.player),
                 StateLogic.thunder(world.player))
        add_rule(world.multiworld.get_location(LocationName.BeanbeanOutskirtsNEDigspot1, world.player),
                 StateLogic.thunder(world.player))
        add_rule(world.multiworld.get_location(LocationName.BeanbeanOutskirtsSRoom1Digspot2, world.player),
                 StateLogic.ultra(world.player) and StateLogic.thunder(world.player))

    forbid_item(world.multiworld.get_location(LocationName.SSChuckolaMembershipCard, world.player), "Nuts",
                world.player)  # Bandaid Fix

    add_rule(world.multiworld.get_location(LocationName.HoohooVillageHammerHouseBlock, world.player),
             StateLogic.hammers(world.player))
    add_rule(world.multiworld.get_location(LocationName.HoohooMountainBaseBoostatueRoomBlock2, world.player),
             StateLogic.canCrash(world.player) or StateLogic.super(world.player))
    add_rule(world.multiworld.get_location(LocationName.BeanbeanOutskirtsBooStatueMole, world.player),
             StateLogic.canMini(world.player) and StateLogic.canDig(world.player))
    add_rule(world.multiworld.get_location(LocationName.HoohooVillageSuperHammerCaveBlock, world.player),
             StateLogic.canCrash(world.player) or StateLogic.super(world.player))
    add_rule(world.multiworld.get_location(LocationName.BeanbeanOutskirtsFarmRoomMoleReward1, world.player),
             StateLogic.thunder(world.player))
    add_rule(world.multiworld.get_location(LocationName.BeanbeanOutskirtsFarmRoomMoleReward2, world.player),
             StateLogic.thunder(world.player))
    add_rule(world.multiworld.get_location(LocationName.BeanbeanOutskirtsThunderHandMole, world.player),
             StateLogic.thunder(world.player))
    add_rule(world.multiworld.get_location(LocationName.BeanbeanOutskirtsNWBlock, world.player),
             StateLogic.super(world.player))
    add_rule(world.multiworld.get_location(LocationName.BeanbeanOutskirtsBeanFruit1, world.player),
             StateLogic.canDig(world.player))
    add_rule(world.multiworld.get_location(LocationName.BeanbeanOutskirtsBeanFruit2, world.player),
             StateLogic.canDig(world.player))
    add_rule(world.multiworld.get_location(LocationName.BeanbeanOutskirtsBeanFruit3, world.player),
             StateLogic.canDig(world.player))
    add_rule(world.multiworld.get_location(LocationName.BeanbeanOutskirtsBeanFruit4, world.player),
             StateLogic.super(world.player) and StateLogic.canDig(world.player))
    add_rule(world.multiworld.get_location(LocationName.BeanbeanOutskirtsBeanFruit5, world.player),
             StateLogic.super(world.player) and StateLogic.canDig(world.player))
    add_rule(world.multiworld.get_location(LocationName.BeanbeanOutskirtsBeanFruit6, world.player),
             StateLogic.canDig(world.player))
    add_rule(world.multiworld.get_location(LocationName.BeanbeanOutskirtsBeanFruit7, world.player),
             StateLogic.teehee(world.player) and StateLogic.canDig(world.player))
    add_rule(world.multiworld.get_location(LocationName.BeanbeanOutskirtsSRoom1Block, world.player),
             StateLogic.ultra(world.player) and StateLogic.thunder(world.player))
    add_rule(world.multiworld.get_location(LocationName.BeanbeanOutskirtsSRoom2Block1, world.player),
             StateLogic.canDig(world.player))
    add_rule(
        world.multiworld.get_location(LocationName.WoohooHooniversityMiniMarioPuzzleSecretAreaBlock1, world.player),
        StateLogic.canMini(world.player))
    add_rule(
        world.multiworld.get_location(LocationName.WoohooHooniversityMiniMarioPuzzleSecretAreaBlock2, world.player),
        StateLogic.canMini(world.player))
    add_rule(
        world.multiworld.get_location(LocationName.WoohooHooniversityMiniMarioPuzzleSecretAreaBlock3, world.player),
        StateLogic.canMini(world.player))
    add_rule(
        world.multiworld.get_location(LocationName.WoohooHooniversityMiniMarioPuzzleSecretAreaBlock4, world.player),
        StateLogic.canMini(world.player))
    add_rule(world.multiworld.get_location(LocationName.WoohooHooniversityMiniMarioPuzzleBlock, world.player),
             StateLogic.canMini(world.player))
    add_rule(world.multiworld.get_location(LocationName.BeanbeanOutskirtsSecretScroll1, world.player),
             StateLogic.thunder(world.player) and StateLogic.super(world.player))
    add_rule(world.multiworld.get_location(LocationName.BeanbeanOutskirtsSecretScroll2, world.player),
             StateLogic.thunder(world.player) and StateLogic.ultra(world.player))
    add_rule(world.multiworld.get_location(LocationName.HoohooVillageMoleBehindTurtle, world.player),
             StateLogic.canDash(world.player))
    add_rule(world.multiworld.get_location(LocationName.BeanbeanOutskirtsNESoloMarioMole1, world.player),
             StateLogic.canMini(world.player))
    add_rule(world.multiworld.get_location(LocationName.BeanbeanOutskirtsNESoloMarioMole2, world.player),
             StateLogic.canMini(world.player))
    add_rule(world.multiworld.get_location(LocationName.BeanbeanOutskirtsSuperHammerUpgrade, world.player),
             StateLogic.thunder(world.player))
    add_rule(world.multiworld.get_location(LocationName.BeanbeanOutskirtsUltraHammerUpgrade, world.player),
             StateLogic.thunder(world.player) and StateLogic.pieces(world.player) and StateLogic.castleTown(world.player) and StateLogic.rose(world.player))
    add_rule(world.multiworld.get_location(LocationName.BeanbeanOutskirtsSoloLuigiCaveMole, world.player),
             StateLogic.canDig(world.player))
    add_rule(world.multiworld.get_location(LocationName.ChucklehuckWoodsRedChuckolaFruit, world.player),
             StateLogic.canMini(world.player))
    add_rule(world.multiworld.get_location(LocationName.ChucklehuckWoodsWhiteChuckolaFruit, world.player),
             StateLogic.canDig(world.player) and StateLogic.canMini(world.player))
    add_rule(world.multiworld.get_location(LocationName.ChucklehuckWoodsAfterChucklerootBlock1, world.player),
             StateLogic.fruits(world.player))
    add_rule(world.multiworld.get_location(LocationName.ChucklehuckWoodsAfterChucklerootBlock2, world.player),
             StateLogic.fruits(world.player))
    add_rule(world.multiworld.get_location(LocationName.ChucklehuckWoodsAfterChucklerootBlock3, world.player),
             StateLogic.fruits(world.player))
    add_rule(world.multiworld.get_location(LocationName.ChucklehuckWoodsAfterChucklerootBlock4, world.player),
             StateLogic.fruits(world.player))
    add_rule(world.multiworld.get_location(LocationName.ChucklehuckWoodsAfterChucklerootBlock5, world.player),
             StateLogic.fruits(world.player))
    add_rule(world.multiworld.get_location(LocationName.ChucklehuckWoodsAfterChucklerootBlock6, world.player),
             StateLogic.fruits(world.player))
    add_rule(world.multiworld.get_location(LocationName.ChucklehuckWoodsRoom7Block1, world.player),
             StateLogic.hammers(world.player))
    add_rule(world.multiworld.get_location(LocationName.ChucklehuckWoodsRoom7Block2, world.player),
             StateLogic.hammers(world.player))
    add_rule(world.multiworld.get_location(LocationName.ChucklehuckWoodsRoom4Block1, world.player),
             StateLogic.canMini(world.player))
    add_rule(world.multiworld.get_location(LocationName.ChucklehuckWoodsRoom4Block2, world.player),
             StateLogic.canMini(world.player))
    add_rule(world.multiworld.get_location(LocationName.ChucklehuckWoodsRoom4Block3, world.player),
             StateLogic.canMini(world.player))
    add_rule(world.multiworld.get_location(LocationName.ChucklehuckWoodsPipeRoomBlock1, world.player),
             StateLogic.hammers(world.player))
    add_rule(world.multiworld.get_location(LocationName.ChucklehuckWoodsPipeRoomBlock2, world.player),
             StateLogic.hammers(world.player))
    add_rule(world.multiworld.get_location(LocationName.BeanbeanCastleTownMiniMarioBlock1, world.player),
             StateLogic.canMini(world.player))
    add_rule(world.multiworld.get_location(LocationName.BeanbeanCastleTownMiniMarioBlock2, world.player),
             StateLogic.canMini(world.player))
    add_rule(world.multiworld.get_location(LocationName.BeanbeanCastleTownMiniMarioBlock3, world.player),
             StateLogic.canMini(world.player))
    add_rule(world.multiworld.get_location(LocationName.BeanbeanCastleTownMiniMarioBlock4, world.player),
             StateLogic.canMini(world.player))
    add_rule(world.multiworld.get_location(LocationName.BeanbeanCastleTownMiniMarioBlock5, world.player),
             StateLogic.canMini(world.player))
    add_rule(world.multiworld.get_location(LocationName.BeanbeanCastleFakeBeastar, world.player),
             StateLogic.pieces(world.player) and StateLogic.rose(world.player))
    add_rule(world.multiworld.get_location(LocationName.BeanbeanCastlePeachsExtraDress, world.player),
             StateLogic.pieces(world.player) and StateLogic.rose(world.player))
    add_rule(world.multiworld.get_location(LocationName.SewersRoom5Block1, world.player),
             StateLogic.hammers(world.player))
    add_rule(world.multiworld.get_location(LocationName.SewersRoom5Block2, world.player),
             StateLogic.hammers(world.player))
    add_rule(world.multiworld.get_location(LocationName.GwarharLagoonFirstUnderwaterAreaRoom1Block, world.player),
             StateLogic.canDash(world.player))
    add_rule(world.multiworld.get_location(LocationName.GwarharLagoonFirstUnderwaterAreaRoom2Block1, world.player),
             StateLogic.canDash(world.player))
    add_rule(world.multiworld.get_location(LocationName.GwarharLagoonFirstUnderwaterAreaRoom2Block2, world.player),
             StateLogic.canDash(world.player))
    add_rule(world.multiworld.get_location(LocationName.GwarharLagoonRedPearlBean, world.player),
             StateLogic.fire(world.player) and StateLogic.thunder(world.player))
    add_rule(world.multiworld.get_location(LocationName.GwarharLagoonGreenPearlBean, world.player),
             StateLogic.fire(world.player) and StateLogic.thunder(world.player))
    add_rule(world.multiworld.get_location(LocationName.TeeheeValleyPastUltraHammersBlock1, world.player),
             StateLogic.ultra(world.player))
    add_rule(world.multiworld.get_location(LocationName.TeeheeValleyPastUltraHammersBlock2, world.player),
             StateLogic.ultra(world.player))
    add_rule(world.multiworld.get_location(LocationName.TeeheeValleySoloLuigiMazeRoom1Block, world.player),
             StateLogic.ultra(world.player))
    add_rule(world.multiworld.get_location(LocationName.OhoOasisFirebrand, world.player),
             StateLogic.canMini(world.player))
    add_rule(world.multiworld.get_location(LocationName.OhoOasisThunderhand, world.player),
             StateLogic.canDig(world.player))
    add_rule(world.multiworld.get_location(LocationName.BeanstarPieceYoshiTheater, world.player),
             StateLogic.neon(world.player))
    add_rule(world.multiworld.get_location(LocationName.YoshiTheaterAzureYoshi, world.player),
             StateLogic.beanFruit(world.player))
    add_rule(world.multiworld.get_location(LocationName.YoshiTheaterBlueYoshi, world.player),
             StateLogic.beanFruit(world.player))
    add_rule(world.multiworld.get_location(LocationName.YoshiTheaterGreenYoshi, world.player),
             StateLogic.beanFruit(world.player))
    add_rule(world.multiworld.get_location(LocationName.YoshiTheaterOrangeYoshi, world.player),
             StateLogic.beanFruit(world.player))
    add_rule(world.multiworld.get_location(LocationName.YoshiTheaterPurpleYoshi, world.player),
             StateLogic.beanFruit(world.player))
    add_rule(world.multiworld.get_location(LocationName.YoshiTheaterRedYoshi, world.player),
             StateLogic.beanFruit(world.player))
    add_rule(world.multiworld.get_location(LocationName.YoshiTheaterYellowYoshi, world.player),
             StateLogic.beanFruit(world.player))
    add_rule(world.multiworld.get_location(LocationName.WinkleAreaBeanstarRoomBlock, world.player),
             StateLogic.winkle(world.player))
    add_rule(world.multiworld.get_location(LocationName.BeanstarPieceWinkleArea, world.player),
             StateLogic.winkle(world.player))
    add_rule(world.multiworld.get_location(LocationName.GwarharLagoonSpangleReward, world.player),
             StateLogic.spangle(world.player))
    add_rule(world.multiworld.get_location(LocationName.PantsShopMomPiranhaFlag1, world.player),
             StateLogic.brooch(world.player) or StateLogic.rose(world.player))
    add_rule(world.multiworld.get_location(LocationName.PantsShopMomPiranhaFlag2, world.player),
             StateLogic.brooch(world.player) or StateLogic.rose(world.player))
    add_rule(world.multiworld.get_location(LocationName.PantsShopMomPiranhaFlag3, world.player),
             StateLogic.brooch(world.player) or StateLogic.rose(world.player))
    add_rule(world.multiworld.get_location(LocationName.BadgeShopMomPiranhaFlag1, world.player),
             StateLogic.brooch(world.player) or StateLogic.rose(world.player))
    add_rule(world.multiworld.get_location(LocationName.BadgeShopMomPiranhaFlag2, world.player),
             StateLogic.brooch(world.player) or StateLogic.rose(world.player))
    add_rule(world.multiworld.get_location(LocationName.BadgeShopMomPiranhaFlag3, world.player),
             StateLogic.brooch(world.player) or StateLogic.rose(world.player))
    add_rule(world.multiworld.get_location(LocationName.ChateauGreenGoblet, world.player),
             StateLogic.brooch(world.player) and StateLogic.canDig(world.player))
    add_rule(world.multiworld.get_location(LocationName.ChateauRedGoblet, world.player),
             StateLogic.brooch(world.player) and StateLogic.canMini(world.player))

    add_rule(world.multiworld.get_location(LocationName.GwarharLagoonSpangle, world.player),
             StateLogic.ultra(world.player))
    add_rule(world.multiworld.get_location(LocationName.GwarharLagoonSpangleRoomBlock, world.player),
             StateLogic.ultra(world.player))
    if world.options.difficult_logic:
        add_rule(world.multiworld.get_location(LocationName.GwarharLagoonSpangleReward, world.player),
                 StateLogic.canCrash(world.player))
        add_rule(world.multiworld.get_location(LocationName.BeanstarPieceHermie, world.player),
                 StateLogic.canCrash(world.player))
        if world.options.chuckle_beans != 0:
            add_rule(world.multiworld.get_location(LocationName.GwarharLagoonPastHermieDigspot, world.player),
                    StateLogic.canCrash(world.player))

    if world.options.coins:
        add_rule(world.multiworld.get_location(LocationName.HoohooMountainBaseBooStatueCaveCoinBlock1, world.player),
                 StateLogic.canCrash(world.player) or StateLogic.super(world.player))
        add_rule(world.multiworld.get_location("Hoohoo Mountain Base Boo Statue Cave Coin Block 2", world.player),
                 StateLogic.canCrash(world.player) or StateLogic.super(world.player))
        add_rule(world.multiworld.get_location("Hoohoo Mountain Base Boo Statue Cave Coin Block 3", world.player),
                 StateLogic.canCrash(world.player) or StateLogic.super(world.player))
        add_rule(world.multiworld.get_location("Beanbean Outskirts NW Coin Block", world.player),
                 StateLogic.super(world.player))
        add_rule(world.multiworld.get_location("Beanbean Outskirts S Room 1 Coin Block", world.player),
                 StateLogic.ultra(world.player) and StateLogic.thunder(world.player))
        add_rule(world.multiworld.get_location("Beanbean Outskirts S Room 2 Coin Block", world.player),
                 StateLogic.canCrash(world.player))
        add_rule(world.multiworld.get_location("Chateau Popple Room Coin Block 1", world.player),
                 StateLogic.brooch(world.player))
        add_rule(world.multiworld.get_location("Chateau Popple Room Coin Block 2", world.player),
                 StateLogic.brooch(world.player))
        add_rule(world.multiworld.get_location("Chucklehuck Woods Cave Room 1 Coin Block", world.player),
                 StateLogic.brooch(world.player))
        add_rule(world.multiworld.get_location("Chucklehuck Woods Cave Room 2 Coin Block", world.player),
                 StateLogic.brooch(world.player))
        add_rule(world.multiworld.get_location("Chucklehuck Woods Cave Room 3 Coin Block", world.player),
                 StateLogic.brooch(world.player))
        add_rule(world.multiworld.get_location("Chucklehuck Woods Pipe 5 Room Coin Block", world.player),
                 StateLogic.brooch(world.player) and StateLogic.hammers(world.player))
        add_rule(world.multiworld.get_location("Chucklehuck Woods Room 7 Coin Block", world.player),
                 StateLogic.brooch(world.player) and StateLogic.hammers(world.player))
        add_rule(world.multiworld.get_location("Chucklehuck Woods After Chuckleroot Coin Block", world.player),
                 StateLogic.brooch(world.player) and StateLogic.fruits(world.player))
        add_rule(world.multiworld.get_location("Chucklehuck Woods Koopa Room Coin Block", world.player),
                 StateLogic.brooch(world.player))
        add_rule(world.multiworld.get_location("Chucklehuck Woods Winkle Area Cave Coin Block", world.player),
                 StateLogic.brooch(world.player) and StateLogic.canDash(world.player))
        add_rule(world.multiworld.get_location("Sewers Prison Room Coin Block", world.player),
                 StateLogic.rose(world.player))
        add_rule(world.multiworld.get_location("Teehee Valley Past Ultra Hammer Rocks Coin Block", world.player),
                 StateLogic.ultra(world.player))
        add_rule(world.multiworld.get_location("S.S. Chuckola Storage Room Coin Block 1", world.player),
                 StateLogic.super(world.player) or StateLogic.canDash(world.player))
        add_rule(world.multiworld.get_location("Gwarhar Lagoon First Underwater Area Room 2 Coin Block", world.player),
                 StateLogic.canDash(world.player) and (StateLogic.membership(world.player) or StateLogic.surfable(world.player)))
        add_rule(world.multiworld.get_location("S.S. Chuckola Storage Room Coin Block 2", world.player),
                 StateLogic.super(world.player) or StateLogic.canDash(world.player))
        add_rule(world.multiworld.get_location("Joke's End Second Floor West Room Coin Block", world.player),
                 StateLogic.ultra(world.player) and StateLogic.fire(world.player)
                 and (StateLogic.membership(world.player)
                 or (StateLogic.canDig(world.player) and StateLogic.canMini(world.player))))
        add_rule(world.multiworld.get_location("Joke's End North of Bridge Room Coin Block", world.player),
                 StateLogic.ultra(world.player) and StateLogic.fire(world.player)
                 and StateLogic.canDig(world.player)
                 and (
                    StateLogic.membership(world.player)
                    or StateLogic.canMini(world.player)
                 ))
        if not world.options.difficult_logic:
            add_rule(world.multiworld.get_location("Joke's End North of Bridge Room Coin Block", world.player),
                     StateLogic.canCrash(world.player))
