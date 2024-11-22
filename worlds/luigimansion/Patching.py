from .Regions import REGION_LIST
import random

def update_event_info(event_info):
    for x in event_info.info_file_field_entries:
        if x["EventNo"] in {15, 11, 42, 80, 96, 16, 70, 69, 35, 85, 73, 47, 29, 54}: # Removes events that we don't want to trigger at all in the mansion, such as some Egadd calls.
            event_info.info_file_field_entries.remove(x)


def update_character_info(character_info):
    for x in character_info.info_file_field_entries:
        if x["name"] in { "vhead", "vbody", "dhakase", "demobak1", "dluige01" }: # Removes useless cutscene objects and the vacuum in the Parlor under the closet.
            character_info.info_file_field_entries.remove(x)


def update_observer_info(observer_info):
    for x in observer_info.info_file_field_entries:
        if x["name"] == "kinopio": # Allows the Foyer Toad to spawn by default.
            x["cond_arg0"] = 0
            x["appear_flag"] = 0
            x["cond_type"] = 13

        if x["room_no"] in { 25, 33 }: # Allows the Master Bedroom to be lit after clearing it, even if Neville hasn't been caught, and allows The Twins Room to be lit after clearing it, even if Chauncey hasn't been caught.
            x["appear_flag"] = 0


def update_generator_info(generator_info):
    for x in generator_info.info_file_field_entries:
        if x["name"] == "demotel2": # Allows the Ring of Boos on the 3F Balcony to only appear when the Ice Medal has been collected. This prevents being softlocked in Boolossus and having to reset the game without saving.
            x["appear_flag"] = 22


def update_obj_info(obj_info):
    for x in obj_info.info_file_field_entries:
        if x["name"] in { "eldoor07", "eldoor08", "eldoor09", "eldoor10" }: # Removes the vines on Area doors, as those require the Area Number of the game to be changed to have them disappear.
            obj_info.info_file_field_entries.remove(x)


def get_chest_size(key_id):
    match key_id:
        case 3:
            return 2
        case 42:
            return 2
        case 59:
            return 2
        case 72:
            return 2
        case _:
            return 0


def get_key_name(door_id):
    match door_id:
        case 3:
            return "key02"
        case 42:
            return "key03"
        case 59:
            return "key04"
        case 72:
            return "key05"
        case _:
            return "key01"


def update_item_info_table(item_info_table_entry, output_data):
    for x in item_info_table_entry.info_file_field_entries[:]:
        if x["name"].startswith("key_"):
            item_info_table_entry.info_file_field_entries.remove(x)

    for item_name, item_data in output_data["Locations"].items():
        if item_data["door_id"] != 0:
            item_name = "key_" + str(item_data["door_id"])

            new_item = {
                "name": item_name,
                "character_name": get_key_name(item_data["door_id"]),
                "open_door_no": item_data["door_id"],
                "hp_amount": 0,
                "is_escape": 0
            }
            item_info_table_entry.info_file_field_entries.append(new_item)
            # [dict(t) for t in {tuple(d.items()) for d in treasure_table_entry.info_file_field_entries}]


def update_item_appear_table(item_appear_table_entry, output_data):
    for x in item_appear_table_entry.info_file_field_entries[:]:
        if x["item0"].startswith("key_"):
            item_appear_table_entry.info_file_field_entries.remove(x)

    for item_name, item_data in output_data["Locations"].items():
        if item_data["door_id"] != 0:
            item_name = "key_" + str(item_data["door_id"])

            new_item = {
                "item0": item_name,
                "item1": item_name,
                "item2": item_name,
                "item3": item_name,
                "item4": item_name,
                "item5": item_name,
                "item6": item_name,
                "item7": item_name,
                "item8": item_name,
                "item9": item_name,
                "item10": item_name,
                "item11": item_name,
                "item12": item_name,
                "item13": item_name,
                "item14": item_name,
                "item15": item_name,
                "item16": item_name,
                "item17": item_name,
                "item18": item_name,
                "item19": item_name
            }
            item_appear_table_entry.info_file_field_entries.append(new_item)
            # [dict(t) for t in {tuple(d.items()) for d in treasure_table_entry.info_file_field_entries}]


def update_treasure_table(treasure_table_entry, output_data):
    for x in treasure_table_entry.info_file_field_entries[:]:
        treasure_table_entry.info_file_field_entries.remove(x)

    for item_name, item_data in output_data["Locations"].items():
        chest_size = 0
        item_name = ""

        if item_data["door_id"] == 0:
            item_name = get_item_name(item_name, item_data)
            chest_size = 2
        else:
            item_name = "key_" + str(item_data["door_id"])
            chest_size = get_chest_size(item_data["door_id"])

        if item_name != "":
            new_item = {
                "other": item_name,
                "room": item_data["room_no"],
                "size": chest_size,
                "coin": 0,
                "bill": 0,
                "gold": 0,
                "spearl": 0,
                "mpearl": 0,
                "lpearl": 0,
                "sapphire": 0,
                "emerald": 0,
                "ruby": 0,
                "diamond": 0,
                "cdiamond": 0,
                "rdiamond": 0,
                "effect": 1 if chest_size == 2 else 0,
                "camera": 1
            }
            treasure_table_entry.info_file_field_entries.append(new_item)
            # [dict(t) for t in {tuple(d.items()) for d in treasure_table_entry.info_file_field_entries}]


def get_item_name(item_name, item_data):
    if item_data["door_id"] != 0:
        return get_key_name(item_data["door_id"])

    match item_name:
        case "Fire Element Medal":
            return "elffst"
        case "Water Element Medal":
            return "elwfst"
        case "Ice Element Medal":
            return "elifst"
        case "Mario's Hat":
            return "mcap"
        case "Mario's Letter":
            return "mletter"
        case "Mario's Shoe":
            return "mshoes"
        case "Mario's Glove":
            return "mglove"
        case "Mario's Star":
            return "mstar"

    return "----"


def update_key_info(key_info_entry, output_data):
    for item_name, item_data in output_data["Locations"].items():
        if item_name == "Ghost Foyer Key":
            for x in key_info_entry.info_file_field_entries[:]:
                    x["name"] = get_item_name(item_name, item_data)
                    x["open_door_no"] = item_data["door_id"]
                    x["appear_flag"] = 0
                    x["disappear_flag"] = 0
                    x["appear_type"] = 4
                    x["invisible"] = 0
                    break
        for x in key_info_entry.info_file_field_entries[:]:
            if item_data["type"] == "Freestanding":
                x["name"] = get_item_name(item_name, item_data)
                x["open_door_no"] = item_data["door_id"]
                break