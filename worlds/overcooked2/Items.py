from BaseClasses import Item
from typing import NamedTuple, Dict
from .Overcooked2Levels import Overcooked2Dlc

class ItemData(NamedTuple):
    code: int


class Overcooked2Item(Item):
    game: str = "Overcooked! 2"


oc2_base_id = 213700

item_table: Dict[str, ItemData] = {
    "Wood"                          : ItemData(oc2_base_id + 1 ),
    "Coal Bucket"                   : ItemData(oc2_base_id + 2 ),
    "Spare Plate"                   : ItemData(oc2_base_id + 3 ),
    "Fire Extinguisher"             : ItemData(oc2_base_id + 4 ),
    "Bellows"                       : ItemData(oc2_base_id + 5 ),
    "Clean Dishes"                  : ItemData(oc2_base_id + 6 ),
    "Larger Tip Jar"                : ItemData(oc2_base_id + 7 ),
    "Progressive Dash"              : ItemData(oc2_base_id + 8 ),
    "Progressive Throw/Catch"       : ItemData(oc2_base_id + 9 ),
    "Coin Purse"                    : ItemData(oc2_base_id + 10),
    "Control Stick Batteries"       : ItemData(oc2_base_id + 11),
    "Wok Wheels"                    : ItemData(oc2_base_id + 12),
    "Dish Scrubber"                 : ItemData(oc2_base_id + 13),
    "Burn Leniency"                 : ItemData(oc2_base_id + 14),
    "Sharp Knife"                   : ItemData(oc2_base_id + 15),
    "Order Lookahead"               : ItemData(oc2_base_id + 16),
    "Lightweight Backpack"          : ItemData(oc2_base_id + 17),
    "Faster Respawn Time"           : ItemData(oc2_base_id + 18),
    "Faster Condiment/Drink Switch" : ItemData(oc2_base_id + 19),
    "Guest Patience"                : ItemData(oc2_base_id + 20),
    "Kevin-1"                       : ItemData(oc2_base_id + 21),
    "Kevin-2"                       : ItemData(oc2_base_id + 22),
    "Kevin-3"                       : ItemData(oc2_base_id + 23),
    "Kevin-4"                       : ItemData(oc2_base_id + 24),
    "Kevin-5"                       : ItemData(oc2_base_id + 25),
    "Kevin-6"                       : ItemData(oc2_base_id + 26),
    "Kevin-7"                       : ItemData(oc2_base_id + 27),
    "Kevin-8"                       : ItemData(oc2_base_id + 28),
    "Cooking Emote"                 : ItemData(oc2_base_id + 29),
    "Curse Emote"                   : ItemData(oc2_base_id + 30),
    "Serving Emote"                 : ItemData(oc2_base_id + 31),
    "Preparing Emote"               : ItemData(oc2_base_id + 32),
    "Washing Up Emote"              : ItemData(oc2_base_id + 33),
    "Ok Emote"                      : ItemData(oc2_base_id + 34),
    "Ramp Button"                   : ItemData(oc2_base_id + 35),
    "Bonus Star"                    : ItemData(oc2_base_id + 36),
    "Calmer Unbread"                : ItemData(oc2_base_id + 37),
    "Green Ramp"                    : ItemData(oc2_base_id + 38),
    "Yellow Ramp"                   : ItemData(oc2_base_id + 39),
    "Blue Ramp"                     : ItemData(oc2_base_id + 40),
    "Pink Ramp"                     : ItemData(oc2_base_id + 41),
    "Dark Green Ramp"               : ItemData(oc2_base_id + 42),
    "Red Ramp"                      : ItemData(oc2_base_id + 43),
    "Purple Ramp"                   : ItemData(oc2_base_id + 44),
    "Emote Wheel"                   : ItemData(oc2_base_id + 45),
}

item_frequencies = {
    "Progressive Throw/Catch": 2,
    "Larger Tip Jar": 2,
    "Order Lookahead": 2,
    "Progressive Dash": 2,
    "Bonus Star": 0,  # Filler Item

    # Unused items
    "Ramp Button": 0,
    "Cooking Emote" : 0,
    "Curse Emote" : 0,
    "Serving Emote" : 0,
    "Preparing Emote" : 0,
    "Washing Up Emote": 0,
    "Ok Emote": 0,
}

dlc_exclusives = {
    "Wood"                          : {Overcooked2Dlc.CAMPFIRE_COOK_OFF},
    "Coal Bucket"                   : {Overcooked2Dlc.NIGHT_OF_THE_HANGRY_HORDE},
    "Bellows"                       : {Overcooked2Dlc.SURF_N_TURF},
    "Control Stick Batteries"       : {Overcooked2Dlc.STORY, Overcooked2Dlc.SURF_N_TURF, Overcooked2Dlc.NIGHT_OF_THE_HANGRY_HORDE, Overcooked2Dlc.CARNIVAL_OF_CHAOS, Overcooked2Dlc.SEASONAL},
    "Wok Wheels"                    : {Overcooked2Dlc.SEASONAL},
    "Lightweight Backpack"          : {Overcooked2Dlc.CAMPFIRE_COOK_OFF},
    "Faster Condiment/Drink Switch" : {Overcooked2Dlc.SEASONAL, Overcooked2Dlc.CARNIVAL_OF_CHAOS},
    "Calmer Unbread"                : {Overcooked2Dlc.SEASONAL, Overcooked2Dlc.NIGHT_OF_THE_HANGRY_HORDE},
    "Coin Purse"                    : {Overcooked2Dlc.SEASONAL, Overcooked2Dlc.NIGHT_OF_THE_HANGRY_HORDE},
}

item_name_to_config_name = {
    "Wood"                          : "DisableWood"                    ,
    "Coal Bucket"                   : "DisableCoal"                    ,
    "Spare Plate"                   : "DisableOnePlate"                ,
    "Fire Extinguisher"             : "DisableFireExtinguisher"        ,
    "Bellows"                       : "DisableBellows"                 ,
    "Clean Dishes"                  : "PlatesStartDirty"               ,
    "Control Stick Batteries"       : "DisableControlStick"            ,
    "Wok Wheels"                    : "DisableWokDrag"                 ,
    "Dish Scrubber"                 : "WashTimeMultiplier"             ,
    "Burn Leniency"                 : "BurnSpeedMultiplier"            ,
    "Sharp Knife"                   : "ChoppingTimeScale"              ,
    "Lightweight Backpack"          : "BackpackMovementScale"          ,
    "Faster Respawn Time"           : "RespawnTime"                    ,
    "Faster Condiment/Drink Switch" : "CarnivalDispenserRefactoryTime" ,
    "Guest Patience"                : "CustomOrderLifetime"            ,
    "Ramp Button"                   : "DisableRampButton"              ,
    "Green Ramp"                    : "DisableGreenRampButton"         ,
    "Yellow Ramp"                   : "DisableYellowRampButton"        ,
    "Blue Ramp"                     : "DisableBlueRampButton"          ,
    "Pink Ramp"                     : "DisablePinkRampButton"          ,
    "Dark Green Ramp"               : "DisableGreyRampButton"          ,
    "Red Ramp"                      : "DisableRedRampButton"           ,
    "Purple Ramp"                   : "DisablePurpleRampButton"        ,
    "Calmer Unbread"                : "AggressiveHorde"                ,
    "Coin Purse"                    : "DisableEarnHordeMoney"          ,
}

vanilla_values = {
    "DisableWood": False,
    "DisableCoal": False,
    "DisableOnePlate": False,
    "DisableFireExtinguisher": False,
    "DisableBellows": False,
    "PlatesStartDirty": False,
    "DisableControlStick": False,
    "DisableWokDrag": False,
    "DisableRampButton": False,
    "WashTimeMultiplier": 1.0,
    "BurnSpeedMultiplier": 1.0,
    "ChoppingTimeScale": 1.0,
    "BackpackMovementScale": 1.0,
    "RespawnTime": 5.0,
    "CarnivalDispenserRefactoryTime": 0.0,
    "CustomOrderLifetime": 100.0,
    "AggressiveHorde": False,
    "DisableEarnHordeMoney": False,
    "DisableGreenRampButton" : False,
    "DisableYellowRampButton" : False,
    "DisableBlueRampButton" : False,
    "DisablePinkRampButton" : False,
    "DisableGreyRampButton" : False,
    "DisableRedRampButton" : False,
    "DisablePurpleRampButton" : False,
}

item_id_to_name: Dict[int, str] = {
    data.code: item_name for item_name, data in item_table.items() if data.code
}

item_name_to_id: Dict[str, int] = {
    item_name: data.code for item_name, data in item_table.items() if data.code
}


def is_progression(item_name: str) -> bool:
    return not item_name.endswith("Emote")


def item_to_unlock_event(item_name: str) -> Dict[str, str]:
    message = f"{item_name} Acquired!"
    action = ""
    payload = ""
    if item_name.startswith("Kevin"):
        kevin_num = int(item_name.split("-")[-1])
        action = "UNLOCK_LEVEL"
        payload = str(kevin_num + 36)
    elif item_name == "Emote Wheel":
        action = "UNLOCK_EMOTES"
    elif "Emote" in item_name:
        action = "UNLOCK_EMOTE"
        payload = str(item_table[item_name].code - item_table["Cooking Emote"].code)
    elif item_name == "Larger Tip Jar":
        action = "INC_TIP_COMBO"
    elif item_name == "Order Lookahead":
        action = "INC_ORDERS_ON_SCREEN"
    elif item_name == "Bonus Star":
        action = "INC_STAR_COUNT"
        payload = "1"
    elif item_name == "Progressive Dash":
        action = "INC_DASH"
    elif item_name == "Progressive Throw/Catch":
        action = "INC_THROW"
    else:
        config_name = item_name_to_config_name[item_name]
        vanilla_value = vanilla_values[config_name]

        action = "SET_VALUE"
        payload = f"{config_name}={vanilla_value}"

    return {
        "message": message,
        "action": action,
        "payload": payload,
    }
