from worlds.generic.Rules import add_rule, forbid_item
from BaseClasses import MultiWorld
from .Names.LocationName import LocationName
from .Locations import all_locations, hidden
from . import StateLogic


def set_rules(world: MultiWorld, player: int, excluded):
    for location in all_locations:
        if "Digspot" in location.name:
            if (world.skip_minecart[player] and "Minecart" in location.name) or (world.castle_skip[player] and "Bowser" in location.name):
                continue
            if world.chuckle_beans[player] == 0 or world.chuckle_beans[player] == 1 and location.id in hidden:
                continue
            add_rule(world.get_location(location.name, player), lambda state: StateLogic.canDig(state, player))
        if "Beanstone" in location.name:
            add_rule(world.get_location(location.name, player), lambda state: StateLogic.canDig(state, player))
        if "Shop" in location.name and "Coffee" not in location.name and location.name not in excluded:
            forbid_item(world.get_location(location.name, player), "Hammers", player)
        if location.itemType != 0 and location.name not in excluded:
            if "Bowser" in location.name and world.castle_skip[player]:
                continue
            forbid_item(world.get_location(location.name, player), "5 Coins", player)

    if world.chuckle_beans[player] == 2:
        add_rule(world.get_location(LocationName.HoohooVillageSuperHammerCaveDigspot, player),
                 lambda state: StateLogic.canCrash(state, player) or StateLogic.super(state, player))
        add_rule(world.get_location(LocationName.BeanbeanOutskirtsFarmRoomDigspot2, player),
                 lambda state: StateLogic.thunder(state, player))
        add_rule(world.get_location(LocationName.BeanbeanOutskirtsFarmRoomDigspot3, player),
                 lambda state: StateLogic.thunder(state, player))
        add_rule(world.get_location(LocationName.ChucklehuckWoodsWhiteFruitRoomDigspot3, player),
                 lambda state: StateLogic.canMini(state, player))
        add_rule(world.get_location(LocationName.JokesEndJojoraRoomDigspot, player),
                 lambda state: StateLogic.canDash(state, player))

    if world.chuckle_beans[player] == 1 or world.chuckle_beans[player] == 2:
        add_rule(world.get_location(LocationName.HoohooMountainBaseBoostatueRoomDigspot2, player),
                 lambda state: StateLogic.canCrash(state, player) or StateLogic.super(state, player))
        add_rule(world.get_location(LocationName.BeanbeanOutskirtsFarmRoomDigspot1, player),
                 lambda state: StateLogic.thunder(state, player))
        add_rule(world.get_location(LocationName.ChucklehuckWoodsWhiteFruitRoomDigspot2, player),
                 lambda state: StateLogic.canMini(state, player))
        add_rule(world.get_location(LocationName.TeeheeValleyPastUltraHammersDigspot1, player),
                 lambda state: StateLogic.ultra(state, player))
        add_rule(world.get_location(LocationName.TeeheeValleyPastUltraHammersDigspot3, player),
                 lambda state: StateLogic.ultra(state, player))
        add_rule(world.get_location(LocationName.BeanbeanOutskirtsNorthBeachDigspot3, player),
                 lambda state: StateLogic.canDash(state, player) or StateLogic.super(state, player))
        add_rule(world.get_location(LocationName.BeanbeanOutskirtsEDigspot2, player),
                 lambda state: StateLogic.thunder(state, player))
        add_rule(world.get_location(LocationName.BeanbeanOutskirtsNEDigspot1, player),
                 lambda state: StateLogic.thunder(state, player))
        add_rule(world.get_location(LocationName.BeanbeanOutskirtsSRoom1Digspot2, player),
                 lambda state: StateLogic.ultra(state, player) and StateLogic.thunder(state, player))

    forbid_item(world.get_location(LocationName.SSChuckolaMembershipCard, player), "Nuts", player)  # Bandaid Fix

    add_rule(world.get_location(LocationName.HoohooVillageHammerHouseBlock, player),
             lambda state: StateLogic.hammers(state, player))
    add_rule(world.get_location(LocationName.HoohooMountainBaseBoostatueRoomBlock2, player),
             lambda state: StateLogic.canCrash(state, player) or StateLogic.super(state, player))
    add_rule(world.get_location(LocationName.BeanbeanOutskirtsBooStatueMole, player),
             lambda state: StateLogic.canMini(state, player) and StateLogic.canDig(state, player))
    add_rule(world.get_location(LocationName.HoohooVillageSuperHammerCaveBlock, player),
             lambda state: StateLogic.canCrash(state, player) or StateLogic.super(state, player))
    add_rule(world.get_location(LocationName.BeanbeanOutskirtsFarmRoomMoleReward1, player),
             lambda state: StateLogic.thunder(state, player))
    add_rule(world.get_location(LocationName.BeanbeanOutskirtsFarmRoomMoleReward2, player),
             lambda state: StateLogic.thunder(state, player))
    add_rule(world.get_location(LocationName.BeanbeanOutskirtsThunderHandMole, player),
             lambda state: StateLogic.thunder(state, player))
    add_rule(world.get_location(LocationName.BeanbeanOutskirtsNWBlock, player),
             lambda state: StateLogic.super(state, player))
    add_rule(world.get_location(LocationName.BeanbeanOutskirtsBeanFruit1, player),
             lambda state: StateLogic.canDig(state, player))
    add_rule(world.get_location(LocationName.BeanbeanOutskirtsBeanFruit2, player),
             lambda state: StateLogic.canDig(state, player))
    add_rule(world.get_location(LocationName.BeanbeanOutskirtsBeanFruit3, player),
             lambda state: StateLogic.canDig(state, player))
    add_rule(world.get_location(LocationName.BeanbeanOutskirtsBeanFruit4, player),
             lambda state: StateLogic.super(state, player) and StateLogic.canDig(state, player))
    add_rule(world.get_location(LocationName.BeanbeanOutskirtsBeanFruit5, player),
             lambda state: StateLogic.super(state, player) and StateLogic.canDig(state, player))
    add_rule(world.get_location(LocationName.BeanbeanOutskirtsBeanFruit6, player),
             lambda state: StateLogic.canDig(state, player))
    add_rule(world.get_location(LocationName.BeanbeanOutskirtsBeanFruit7, player),
             lambda state: StateLogic.teehee(state, player) and StateLogic.canDig(state, player))
    add_rule(world.get_location(LocationName.BeanbeanOutskirtsSRoom1Block, player),
             lambda state: StateLogic.ultra(state, player) and StateLogic.thunder(state, player))
    add_rule(world.get_location(LocationName.BeanbeanOutskirtsSRoom2Block1, player),
             lambda state: StateLogic.canDig(state, player))
    add_rule(world.get_location(LocationName.WoohooHooniversityMiniMarioPuzzleSecretAreaBlock1, player),
             lambda state: StateLogic.canMini(state, player))
    add_rule(world.get_location(LocationName.WoohooHooniversityMiniMarioPuzzleSecretAreaBlock2, player),
             lambda state: StateLogic.canMini(state, player))
    add_rule(world.get_location(LocationName.WoohooHooniversityMiniMarioPuzzleSecretAreaBlock3, player),
             lambda state: StateLogic.canMini(state, player))
    add_rule(world.get_location(LocationName.WoohooHooniversityMiniMarioPuzzleSecretAreaBlock4, player),
             lambda state: StateLogic.canMini(state, player))
    add_rule(world.get_location(LocationName.WoohooHooniversityMiniMarioPuzzleBlock, player),
             lambda state: StateLogic.canMini(state, player))
    add_rule(world.get_location(LocationName.BeanbeanOutskirtsSecretScroll1, player),
             lambda state: StateLogic.thunder(state, player) and StateLogic.super(state, player))
    add_rule(world.get_location(LocationName.BeanbeanOutskirtsSecretScroll2, player),
             lambda state: StateLogic.thunder(state, player) and StateLogic.ultra(state, player))
    add_rule(world.get_location(LocationName.HoohooVillageMoleBehindTurtle, player),
             lambda state: StateLogic.canDash(state, player))
    add_rule(world.get_location(LocationName.BeanbeanOutskirtsNESoloMarioMole1, player),
             lambda state: StateLogic.canMini(state, player))
    add_rule(world.get_location(LocationName.BeanbeanOutskirtsNESoloMarioMole2, player),
             lambda state: StateLogic.canMini(state, player))
    add_rule(world.get_location(LocationName.HoohooVillageMoleBehindTurtle, player),
             lambda state: StateLogic.thunder(state, player))
    add_rule(world.get_location(LocationName.BeanbeanOutskirtsSuperHammerUpgrade, player),
             lambda state: StateLogic.thunder(state, player))
    add_rule(world.get_location(LocationName.BeanbeanOutskirtsUltraHammerUpgrade, player),
             lambda state: StateLogic.thunder(state, player) and StateLogic.pieces(state, player) and StateLogic.castleTown(state, player) and StateLogic.rose(state, player))
    add_rule(world.get_location(LocationName.BeanbeanOutskirtsSoloLuigiCaveMole, player),
             lambda state: StateLogic.canDig(state, player))
    add_rule(world.get_location(LocationName.ChucklehuckWoodsRedChuckolaFruit, player),
             lambda state: StateLogic.canMini(state, player))
    add_rule(world.get_location(LocationName.ChucklehuckWoodsWhiteChuckolaFruit, player),
             lambda state: StateLogic.canDig(state, player) and StateLogic.canMini(state, player))
    add_rule(world.get_location(LocationName.ChucklehuckWoodsAfterChucklerootBlock1, player),
             lambda state: StateLogic.fruits(state, player))
    add_rule(world.get_location(LocationName.ChucklehuckWoodsAfterChucklerootBlock2, player),
             lambda state: StateLogic.fruits(state, player))
    add_rule(world.get_location(LocationName.ChucklehuckWoodsAfterChucklerootBlock3, player),
             lambda state: StateLogic.fruits(state, player))
    add_rule(world.get_location(LocationName.ChucklehuckWoodsAfterChucklerootBlock4, player),
             lambda state: StateLogic.fruits(state, player))
    add_rule(world.get_location(LocationName.ChucklehuckWoodsAfterChucklerootBlock5, player),
             lambda state: StateLogic.fruits(state, player))
    add_rule(world.get_location(LocationName.ChucklehuckWoodsAfterChucklerootBlock6, player),
             lambda state: StateLogic.fruits(state, player))
    add_rule(world.get_location(LocationName.ChucklehuckWoodsRoom7Block1, player),
             lambda state: StateLogic.hammers(state, player))
    add_rule(world.get_location(LocationName.ChucklehuckWoodsRoom7Block2, player),
             lambda state: StateLogic.hammers(state, player))
    add_rule(world.get_location(LocationName.ChucklehuckWoodsRoom4Block1, player),
             lambda state: StateLogic.canMini(state, player))
    add_rule(world.get_location(LocationName.ChucklehuckWoodsRoom4Block2, player),
             lambda state: StateLogic.canMini(state, player))
    add_rule(world.get_location(LocationName.ChucklehuckWoodsRoom4Block3, player),
             lambda state: StateLogic.canMini(state, player))
    add_rule(world.get_location(LocationName.ChucklehuckWoodsPipeRoomBlock1, player),
             lambda state: StateLogic.hammers(state, player))
    add_rule(world.get_location(LocationName.ChucklehuckWoodsPipeRoomBlock2, player),
             lambda state: StateLogic.hammers(state, player))
    add_rule(world.get_location(LocationName.BeanbeanCastleTownMiniMarioBlock1, player),
             lambda state: StateLogic.canMini(state, player))
    add_rule(world.get_location(LocationName.BeanbeanCastleTownMiniMarioBlock2, player),
             lambda state: StateLogic.canMini(state, player))
    add_rule(world.get_location(LocationName.BeanbeanCastleTownMiniMarioBlock3, player),
             lambda state: StateLogic.canMini(state, player))
    add_rule(world.get_location(LocationName.BeanbeanCastleTownMiniMarioBlock4, player),
             lambda state: StateLogic.canMini(state, player))
    add_rule(world.get_location(LocationName.BeanbeanCastleTownMiniMarioBlock5, player),
             lambda state: StateLogic.canMini(state, player))
    add_rule(world.get_location(LocationName.BeanbeanCastleFakeBeastar, player),
             lambda state: StateLogic.pieces(state, player) and StateLogic.rose(state, player))
    add_rule(world.get_location(LocationName.BeanbeanCastlePeachsExtraDress, player),
             lambda state: StateLogic.pieces(state, player) and StateLogic.rose(state, player))
    add_rule(world.get_location(LocationName.SewersRoom5Block1, player),
             lambda state: StateLogic.hammers(state, player))
    add_rule(world.get_location(LocationName.SewersRoom5Block2, player),
             lambda state: StateLogic.hammers(state, player))
    add_rule(world.get_location(LocationName.GwarharLagoonFirstUnderwaterAreaRoom1Block, player),
             lambda state: StateLogic.canDash(state, player))
    add_rule(world.get_location(LocationName.GwarharLagoonFirstUnderwaterAreaRoom2Block1, player),
             lambda state: StateLogic.canDash(state, player))
    add_rule(world.get_location(LocationName.GwarharLagoonFirstUnderwaterAreaRoom2Block2, player),
             lambda state: StateLogic.canDash(state, player))
    add_rule(world.get_location(LocationName.GwarharLagoonRedPearlBean, player),
             lambda state: StateLogic.fire(state, player) and StateLogic.thunder(state, player))
    add_rule(world.get_location(LocationName.GwarharLagoonGreenPearlBean, player),
             lambda state: StateLogic.fire(state, player) and StateLogic.thunder(state, player))
    add_rule(world.get_location(LocationName.TeeheeValleyPastUltraHammersBlock1, player),
             lambda state: StateLogic.ultra(state, player))
    add_rule(world.get_location(LocationName.TeeheeValleyPastUltraHammersBlock2, player),
             lambda state: StateLogic.ultra(state, player))
    add_rule(world.get_location(LocationName.TeeheeValleySoloLuigiMazeRoom1Block, player),
             lambda state: StateLogic.ultra(state, player))
    add_rule(world.get_location(LocationName.OhoOasisFirebrand, player),
             lambda state: StateLogic.canMini(state, player))
    add_rule(world.get_location(LocationName.OhoOasisThunderhand, player),
             lambda state: StateLogic.canDig(state, player))
    add_rule(world.get_location(LocationName.BeanstarPieceYoshiTheater, player),
             lambda state: StateLogic.neon(state, player))
    add_rule(world.get_location(LocationName.YoshiTheaterAzureYoshi, player),
             lambda state: StateLogic.beanFruit(state, player))
    add_rule(world.get_location(LocationName.YoshiTheaterBlueYoshi, player),
             lambda state: StateLogic.beanFruit(state, player))
    add_rule(world.get_location(LocationName.YoshiTheaterGreenYoshi, player),
             lambda state: StateLogic.beanFruit(state, player))
    add_rule(world.get_location(LocationName.YoshiTheaterOrangeYoshi, player),
             lambda state: StateLogic.beanFruit(state, player))
    add_rule(world.get_location(LocationName.YoshiTheaterPurpleYoshi, player),
             lambda state: StateLogic.beanFruit(state, player))
    add_rule(world.get_location(LocationName.YoshiTheaterRedYoshi, player),
             lambda state: StateLogic.beanFruit(state, player))
    add_rule(world.get_location(LocationName.YoshiTheaterYellowYoshi, player),
             lambda state: StateLogic.beanFruit(state, player))
    add_rule(world.get_location(LocationName.WinkleAreaBeanstarRoomBlock, player),
             lambda state: StateLogic.winkle(state, player))
    add_rule(world.get_location(LocationName.BeanstarPieceWinkleArea, player),
             lambda state: StateLogic.winkle(state, player))
    add_rule(world.get_location(LocationName.GwarharLagoonSpangleReward, player),
             lambda state: StateLogic.spangle(state, player))
    add_rule(world.get_location(LocationName.PantsShopMomPiranhaFlag1, player),
             lambda state: StateLogic.brooch(state, player) or StateLogic.rose(state, player))
    add_rule(world.get_location(LocationName.PantsShopMomPiranhaFlag2, player),
             lambda state: StateLogic.brooch(state, player) or StateLogic.rose(state, player))
    add_rule(world.get_location(LocationName.PantsShopMomPiranhaFlag3, player),
             lambda state: StateLogic.brooch(state, player) or StateLogic.rose(state, player))
    add_rule(world.get_location(LocationName.BadgeShopMomPiranhaFlag1, player),
             lambda state: StateLogic.brooch(state, player) or StateLogic.rose(state, player))
    add_rule(world.get_location(LocationName.BadgeShopMomPiranhaFlag2, player),
             lambda state: StateLogic.brooch(state, player) or StateLogic.rose(state, player))
    add_rule(world.get_location(LocationName.BadgeShopMomPiranhaFlag3, player),
             lambda state: StateLogic.brooch(state, player) or StateLogic.rose(state, player))
    add_rule(world.get_location(LocationName.ChateauGreenGoblet, player),
             lambda state: StateLogic.brooch(state, player) and StateLogic.canDig(state, player))
    add_rule(world.get_location(LocationName.ChateauRedGoblet, player),
             lambda state: StateLogic.brooch(state, player) and StateLogic.canMini(state, player))
    if world.difficult_logic[player]:
        add_rule(world.get_location(LocationName.GwarharLagoonSpangleReward, player),
                 lambda state: StateLogic.canCrash(state, player))
        add_rule(world.get_location(LocationName.BeanstarPieceHermie, player),
                 lambda state: StateLogic.canCrash(state, player))
        add_rule(world.get_location(LocationName.GwarharLagoonPastHermieDigspot, player),
                 lambda state: StateLogic.canCrash(state, player))

    if world.coins[player]:
        add_rule(world.get_location(LocationName.HoohooMountainBaseBooStatueCaveCoinBlock1, player),
                 lambda state: StateLogic.canCrash(state, player) or StateLogic.super(state, player))
        add_rule(world.get_location("Hoohoo Mountain Base Boo Statue Cave Coin Block 2", player),
                 lambda state: StateLogic.canCrash(state, player) or StateLogic.super(state, player))
        add_rule(world.get_location("Hoohoo Mountain Base Boo Statue Cave Coin Block 3", player),
                 lambda state: StateLogic.canCrash(state, player) or StateLogic.super(state, player))
        add_rule(world.get_location("Beanbean Outskirts NW Coin Block", player),
                 lambda state: StateLogic.super(state, player))
        add_rule(world.get_location("Beanbean Outskirts S Room 1 Coin Block", player),
                 lambda state: StateLogic.ultra(state, player) and StateLogic.thunder(state, player))
        add_rule(world.get_location("Beanbean Outskirts S Room 2 Coin Block", player),
                 lambda state: StateLogic.canCrash(state, player))
        add_rule(world.get_location("Chateau Popple Room Coin Block 1", player),
                 lambda state: StateLogic.brooch(state, player))
        add_rule(world.get_location("Chateau Popple Room Coin Block 2", player),
                 lambda state: StateLogic.brooch(state, player))
        add_rule(world.get_location("Chucklehuck Woods Cave Room 1 Coin Block", player),
                 lambda state: StateLogic.brooch(state, player))
        add_rule(world.get_location("Chucklehuck Woods Cave Room 2 Coin Block", player),
                 lambda state: StateLogic.brooch(state, player))
        add_rule(world.get_location("Chucklehuck Woods Cave Room 3 Coin Block", player),
                 lambda state: StateLogic.brooch(state, player))
        add_rule(world.get_location("Chucklehuck Woods Pipe 5 Room Coin Block", player),
                 lambda state: StateLogic.brooch(state, player) and StateLogic.hammers(state, player))
        add_rule(world.get_location("Chucklehuck Woods Room 7 Coin Block", player),
                 lambda state: StateLogic.brooch(state, player) and StateLogic.hammers(state, player))
        add_rule(world.get_location("Chucklehuck Woods After Chuckleroot Coin Block", player),
                 lambda state: StateLogic.brooch(state, player) and StateLogic.fruits(state, player))
        add_rule(world.get_location("Chucklehuck Woods Koopa Room Coin Block", player),
                 lambda state: StateLogic.brooch(state, player))
        add_rule(world.get_location("Chucklehuck Woods Winkle Area Cave Coin Block", player),
                 lambda state: StateLogic.brooch(state, player) and StateLogic.canDash(state, player))
        add_rule(world.get_location("Sewers Prison Room Coin Block", player),
                 lambda state: StateLogic.rose(state, player))
        add_rule(world.get_location("Teehee Valley Past Ultra Hammer Rocks Coin Block", player),
                 lambda state: StateLogic.ultra(state, player))
        add_rule(world.get_location("S.S Chuckola Storage Room Coin Block 1", player),
                 lambda state: StateLogic.super(state, player) or StateLogic.canDash(state, player))
        add_rule(world.get_location("S.S Chuckola Storage Room Coin Block 2", player),
                 lambda state: StateLogic.super(state, player) or StateLogic.canDash(state, player))
        add_rule(world.get_location("Jokes End Second Floor West Room Coin Block", player),
                 lambda state: StateLogic.ultra(state, player) and StateLogic.fire(state, player) and (StateLogic.membership(state, player) or (StateLogic.canDig(state, player) and StateLogic.canMini(state, player))))

