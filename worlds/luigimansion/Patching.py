def update_event_info(event_info):
    for x in event_info.info_file_field_entries:
        # Removes events that we don't want to trigger at all in the mansion, such as some E. Gadd calls.
        if x["EventNo"] in {15, 11, 42, 80, 96, 16, 70, 69, 35, 85, 73, 47, 29, 54}:
            event_info.info_file_field_entries.remove(x)

def update_character_info(character_info):
    for x in character_info.info_file_field_entries:
        # Removes useless cutscene objects and the vacuum in the Parlor under the closet.
        if x["name"] in { "vhead", "vbody", "dhakase", "demobak1", "dluige01" }:
            character_info.info_file_field_entries.remove(x)

def update_observer_info(observer_info):
    for x in observer_info.info_file_field_entries:
        # Allows the Foyer Toad to spawn by default.
        if x["name"] == "kinopio":
            x["cond_arg0"] = 0
            x["appear_flag"] = 0
            x["cond_type"] = 13

        # Allows the Master Bedroom to be lit after clearing it, even if Neville hasn't been caught, and allows The
        # Twins Room to be lit after clearing it, even if Chauncey hasn't been caught.
        if x["room_no"] in { 33 }:
            x["appear_flag"] = 0

def update_generator_info(generator_info):
    for x in generator_info.info_file_field_entries:
        # Allows the Ring of Boos on the 3F Balcony to only appear when the Ice Medal has been collected.
        # This prevents being softlocked in Boolossus and having to reset the game without saving.
        if x["name"] == "demotel2":
            x["appear_flag"] = 22

def update_obj_info(obj_info):
    for x in obj_info.info_file_field_entries:
        # Removes the vines on Area doors, as those require the Area Number of the game to be changed
        # to have them disappear.
        if x["name"] in { "eldoor07", "eldoor08", "eldoor09", "eldoor10" }:
            obj_info.info_file_field_entries.remove(x)

def __get_chest_size(key_id):
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

def __get_key_name(door_id):
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
                "character_name": __get_key_name(item_data["door_id"]),
                "open_door_no": item_data["door_id"],
                "hp_amount": 0,
                "is_escape": 0
            }
            item_info_table_entry.info_file_field_entries.append(new_item)

def add_appear_item(item_appear_table_entry, item_name):
    new_item = {}
    for itemid in range(20):
        new_item["item" + str(itemid)] = item_name
    item_appear_table_entry.info_file_field_entries.append(new_item)

def update_item_appear_table(item_appear_table_entry, output_data):
    for x in item_appear_table_entry.info_file_field_entries[:]:
        if x["item0"].startswith("key_"):
            item_appear_table_entry.info_file_field_entries.remove(x)

    for item_name, item_data in output_data["Locations"].items():
        if item_data["door_id"] != 0:
            item_name = "key_" + str(item_data["door_id"])

            new_item = {}
            for item_id in range(20):
                new_item["item" + str(item_id)] = item_name

            item_appear_table_entry.info_file_field_entries.append(new_item)

    add_appear_item(item_appear_table_entry, "nothing")
    add_appear_item(item_appear_table_entry, "mkinoko")
    add_appear_item(item_appear_table_entry, "move_sheart")
    add_appear_item(item_appear_table_entry, "move_lheart")
    add_appear_item(item_appear_table_entry, "itembomb")

    add_appear_item(item_appear_table_entry, "elffst")
    add_appear_item(item_appear_table_entry, "elwfst")
    add_appear_item(item_appear_table_entry, "elifst")

    add_appear_item(item_appear_table_entry, "mcap")
    add_appear_item(item_appear_table_entry, "mletter")
    add_appear_item(item_appear_table_entry, "mshoes")
    add_appear_item(item_appear_table_entry, "mglove")
    add_appear_item(item_appear_table_entry, "mstar")

def update_treasure_table(treasure_table_entry, output_data):
    for x in treasure_table_entry.info_file_field_entries[:]:
        treasure_table_entry.info_file_field_entries.remove(x)

    for item_name, item_data in output_data["Locations"].items():
        if item_data["door_id"] == 0:
            item_name = get_item_name(item_data["name"], item_data)
            chest_size = 2
        else:
            item_name = "key_" + str(item_data["door_id"])
            chest_size = __get_chest_size(item_data["door_id"])

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

def get_item_name(item_name, item_data):
    if item_data is not None and item_data["door_id"] != 0:
        return __get_key_name(item_data["door_id"])

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

        case "Nothing":
            return "nothing"
        case "Poison Mushroom":
            return "mkinoko"
        case "Small Heart":
            return "move_sheart"
        case "Large Heart":
            return "move_lheart"
        case "Bomb":
            return "itembomb"

    return "----"

def update_key_info(key_info_entry, output_data):
    for item_name, item_data in output_data["Locations"].items():
        if item_name == "Ghost Foyer Key":
            for x in key_info_entry.info_file_field_entries[:]:
                    x["name"] = get_item_name(item_data["name"], item_data)
                    x["open_door_no"] = item_data["door_id"]
                    x["appear_flag"] = 0
                    x["disappear_flag"] = 0
                    x["appear_type"] = 4
                    x["invisible"] = 0
                    break
        for x in key_info_entry.info_file_field_entries[:]:
            if item_data["type"] == "Freestanding":
                x["name"] = get_item_name(item_data["name"], item_data)
                x["open_door_no"] = item_data["door_id"]
                break

def update_furniture_info(furniture_info_entry, item_appear_table_entry, output_data):
    for item_name, item_data in output_data["Locations"].items():
        if item_data["type"] == "Furniture":
            for y in item_appear_table_entry.info_file_field_entries:
                if y["item0"].startswith("key_"):
                    if y["item0"] == "key_" + str(item_data["door_id"]):
                        furniture_info_entry.info_file_field_entries[item_data["loc_enum"]]["item_table"] = (
                            item_appear_table_entry.info_file_field_entries.index(y))
                        break
                elif y["item0"] == get_item_name(item_data["name"], None):
                    furniture_info_entry.info_file_field_entries[item_data["loc_enum"]]["item_table"] = (
                        item_appear_table_entry.info_file_field_entries.index(y))
                    break