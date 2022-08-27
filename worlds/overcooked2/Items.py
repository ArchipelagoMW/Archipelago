from BaseClasses import Item
import typing


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]


class Overcooked2Item(Item):
    game: str = "Overcooked! 2"


item_table: dict[str, ItemData] = {
    "Wood": ItemData(36),  # python doesn't like this being 0
    "Coal Bucket": ItemData(1),
    "Spare Plate": ItemData(2),
    "Fire Extinguisher": ItemData(3),
    "Bellows": ItemData(4),
    "Clean Dishes": ItemData(5),
    "Progressive Tip Jar": ItemData(6),
    "Progressive Tip Jar": ItemData(7),
    "Dash": ItemData(8),
    "Throw": ItemData(9),
    "Catch": ItemData(10),
    "Remote Control Batteries": ItemData(11),
    "Wok Wheels": ItemData(12),
    "Dish Scrubber": ItemData(13),
    "Burn Leniency": ItemData(14),
    "Sharp Knife": ItemData(15),
    "Progressive Order Lookahead": ItemData(16),
    "Progressive Order Lookahead": ItemData(17),
    "Lightweight Backpack": ItemData(18),
    "Faster Respawn Time": ItemData(19),
    "Faster Condiment/Drink Switch": ItemData(20),
    "Guest Patience": ItemData(21),
    "Kevin-1": ItemData(22),
    "Kevin-2": ItemData(23),
    "Kevin-3": ItemData(24),
    "Kevin-4": ItemData(25),
    "Kevin-5": ItemData(26),
    "Kevin-6": ItemData(27),
    "Kevin-7": ItemData(29),
    "Kevin-8": ItemData(29),
    "Ok Emote": ItemData(30),
    "Cooking Emote": ItemData(31),
    "Curse Emote": ItemData(32),
    "Serving Emote": ItemData(33),
    "Preparing Emote": ItemData(34),
    "Washing Up Emote": ItemData(35),
}

item_name_to_config_name = {
    "Wood"                         : "DisableWood"                   ,
    "Coal Bucket"                  : "DisableCoal"                   ,
    "Spare Plate"                  : "DisableOnePlate"               ,
    "Fire Extinguisher"            : "DisableFireExtinguisher"       ,
    "Bellows"                      : "DisableBellows"                ,
    "Clean Dishes"                 : "PlatesStartDirty"              ,
    "Dash"                         : "DisableDash"                   ,
    "Throw"                        : "DisableThrow"                  ,
    "Catch"                        : "DisableCatch"                  ,
    "Remote Control Batteries"     : "DisableControlStick"           ,
    "Wok Wheels"                   : "DisableWokDrag"                ,
    "Dish Scrubber"                : "WashTimeMultiplier"            ,
    "Burn Leniency"                : "BurnSpeedMultiplier"           ,
    "Sharp Knife"                  : "ChoppingTimeScale"             ,
    "Lightweight Backpack"         : "BackpackMovementScale"         ,
    "Faster Respawn Time"          : "RespawnTime"                   ,
    "Faster Condiment/Drink Switch": "CarnivalDispenserRefactoryTime",
    "Guest Patience"               : "CustomOrderLifetime"           ,
}

vanilla_values = {
    "DisableWood": False,
    "DisableCoal": False,
    "DisableOnePlate": False,
    "DisableFireExtinguisher": False,
    "DisableBellows": False,
    "PlatesStartDirty": False,
    "DisableDash": False,
    "DisableThrow": False,
    "DisableCatch": False,
    "DisableControlStick": False,
    "DisableWokDrag": False,
    "WashTimeMultiplier": 1.0,
    "BurnSpeedMultiplier": 1.0,
    "ChoppingTimeScale": 1.0,
    "BackpackMovementScale": 1.0,
    "RespawnTime": 5.0,
    "CarnivalDispenserRefactoryTime": 0.0,
    "CustomOrderLifetime": 100.0,
}

item_id_to_name: typing.Dict[int, str] = {
    data.code: item_name for item_name, data in item_table.items() if data.code
}

item_name_to_id: typing.Dict[str, int] = {
    item_name: data.code for item_name, data in item_table.items() if data.code
}


def is_progression(item_name: str) -> bool:
    return "Emote" not in item_name


def item_to_unlock_event(item_name: str) -> dict[str, str]:
    message = f"{item_name} Acquired!"
    action = ""
    payload = ""
    if item_name.startswith("Kevin"):
        kevin_num = int(item_name.split("-")[-1])
        action = "UNLOCK_LEVEL"
        payload = str(kevin_num + 36)
    elif "Emote" in item_name:
        action = "UNLOCK_EMOTE"
        payload = str(item_table[item_name].code - 30)
    elif item_name == "Progressive Tip Jar":
        action = "INC_TIP_COMBO"
    elif item_name == "Progressive Order Lookahead":
        action = "INC_ORDERS_ON_SCREEN"
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
