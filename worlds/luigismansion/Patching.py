from random import randrange, choice


# Converts AP readable name to in-game name
def __get_item_name(item_data):
    if item_data["door_id"] != 0:
        return "key_" + str(item_data["door_id"])

    match item_data["name"]:
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

        case "Gold Diamond":
            return "rdiamond"
        case "Money Bundle": #TODO support gems as well
            return "money"
        case "Poison Mushroom":
            return "mkinoko"
        case "Small Heart":
            return "sheart"
        case "Large Heart":
            return "lheart"
        case "Bomb":
            return "itembomb"
        case "Ice Trap":
            return "ice"

    return "nothing"


def update_event_info(event_info):
    # Removes events that we don't want to trigger at all in the mansion, such as some E. Gadd calls, warps after
    # boss battles / grabbing boss keys, and various cutscenes etc.
    events_to_remove = [15, 11, 42, 80, 96, 16, 70, 69, 35, 85, 73, 47, 54, 91, 92, 93, 94]
    event_info.info_file_field_entries = list(filter(
        lambda info_entry: not info_entry["EventNo"] in events_to_remove, event_info.info_file_field_entries))

    for x in event_info.info_file_field_entries:
        # Allows the Ring of Boos on the 3F Balcony to only appear when the Ice Medal has been collected.
        # This prevents being soft locked in Boolossus and having to reset the game without saving.
        if x["EventNo"] == 71:
            x["EventFlag"] = 22

        # Since we have a custom blackout event, we need to update event 44's trigger condition to be A-pressed based.
        # We also update the area ad trigger location to be the same as event45
        if x["EventNo"] == 44:
            x["pos_x"] = 3500.277000
            x["pos_y"] = -550.000000
            x["pos_z"] = -2164.792000
            x["EventFlag"] = 25
            x["EventArea"] = 400
            x["EventIf"] = 1
            x["EventLock"] = 0
            x["PlayerStop"] = 0
            x["EventLoad"] = 0

        # Update the blackout off event trigger to be A-pressed based
        if x["EventNo"] == 45:
            x["EventIf"] = 1
            x["EventArea"] = 400
            x["EventLock"] = 0
            x["PlayerStop"] = 0
            x["EventLoad"] = 0

        if x["EventNo"] == 65:
            x["disappear_flag"] = 10

def update_character_info(character_info, output_data):
    # Removes useless cutscene objects and the vacuum in the Parlor under the closet.
    bad_actors_to_remove = ["vhead", "vbody", "dhakase", "demobak1", "dluige01"]
    character_info.info_file_field_entries = list(filter(
        lambda info_entry: not info_entry["name"] in bad_actors_to_remove, character_info.info_file_field_entries))

    for x in character_info.info_file_field_entries:
        # Replace the mstar Observatory item with its randomized item.
        if x["name"] == "mstar":
            x["name"] = __get_item_name(output_data["Locations"]["Observatory Mario Star"])

        # Allow Chauncey, Lydia, and the Twins to spawn as soon as a new game is created.
        if x["name"] in ["baby", "mother", "dboy", "dboy2"]:
            x["appear_flag"] = 0

        # Fix a Nintendo mistake where the Cellar chest has a room ID of 0 instead of 63.
        if x["create_name"] == "63_2":
            x["room_no"] = 63


def update_observer_info(observer_info):
    for x in observer_info.info_file_field_entries:
        # Allows the Foyer Toad to spawn by default.
        if x["name"] == "kinopio":
            x["cond_arg0"] = 0
            x["appear_flag"] = 0
            x["cond_type"] = 13

        # Allows the Master Bedroom to be lit after clearing it, even if Neville hasn't been caught.
        if x["room_no"] == 33:
            x["appear_flag"] = 0

        # Allows Twins Room to be lit after clearing it, even if Chauncey hasn't been caught.
        if x["room_no"] == 25:
            x["appear_flag"] = 0

        # Remove locking doors behind Luigi in dark rooms to prevent soft locks
        if x["do_type"] == 11:
            x["do_type"] = 0

        # Ignore me, I am the observers that spawn ghosts for Vincent
        # if x["string_arg0"] in ["57_1", "57_2", "57_3", "57_4", "57_5", "57_6", "57_7"]:
        #    x["string_arg0"] = "(null)"


def update_generator_info(generator_info):
    for x in generator_info.info_file_field_entries:
        # Allows the Ring of Boos on the 3F Balcony to only appear when the Ice Medal has been collected.
        # This prevents being softlocked in Boolossus and having to reset the game without saving.
        if x["type"] == "demotel2":
            x["appear_flag"] = 22
            x["disappear_flag"] = 11


def update_obj_info(obj_info):
    # Removes the vines on Area doors, as those require the Area Number of the game to be changed
    # to have them disappear.
    bad_objects_to_remove = ["eldoor07", "eldoor08", "eldoor09", "eldoor10"]
    obj_info.info_file_field_entries = list(filter(
        lambda info_entry: not info_entry["name"] in bad_objects_to_remove, obj_info.info_file_field_entries))


# Indicates the chest size that will be loaded in game based on item provided. 0 = small, 1 = medium, 2 = large
def __get_chest_size_from_item(item_name):
    match item_name:
        case "Mario's Hat" | "Mario's Letter" | "Mario's Shoe" | "Mario's Glove" | "Mario's Star":
            return 0

        case "Small Heart":
            return 0
        case "Large Heart":
            return 1

        case "Poison Mushroom" | "Bomb" | "Ice Trap" | "Gold Diamond":
            return 2

        case "Fire Element Medal" | "Water Element Medal" | "Ice Element Medal":
            return 2

        case "Money Bundle": #Todo change to support gems as well
            return 1

    return 0

# For every key found in the generation output, add an entry for it in "iteminfotable".
def update_item_info_table(item_info, output_data):
    # Adds the special items so they can spawn in furniture or chests.
    items_to_add = ["rdiamond", "itembomb", "ice", "mstar"]
    for new_item in items_to_add:
        __add_info_item(item_info, None, info_item_name=new_item)

    # Gets the list of keys already added in the item info table
    already_added_keys = [item_entry["name"] for item_entry in item_info.info_file_field_entries if
            str(item_entry["name"]).startswith("key_")]

    for item_name, item_data in output_data["Locations"].items():
        current_item = __get_item_name(item_data)
        if item_data["door_id"] > 0 and current_item not in already_added_keys:
            __add_info_item(item_info, item_data)


def __add_info_item(item_info, item_data, open_door_no = 0, hp_amount = 0, is_escape = 0, info_item_name=None):
    if info_item_name is None:
        info_name = __get_item_name(item_data)
        char_name = __get_item_name(item_data) if not item_data["door_id"] > 0 else (
            __get_key_name(item_data["door_id"]))
        open_no = 0 if not item_data["door_id"] > 0 else item_data["door_id"]
    else:
        info_name = info_item_name
        char_name = info_item_name
        open_no = open_door_no

    item_info.info_file_field_entries.append({
        "name": info_name,
        "character_name": char_name,
        "open_door_no": open_no,
        "hp_amount": hp_amount,
        "is_escape": is_escape
    })


# Indicates the key model to use when spawning the item.
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


def update_item_appear_table(item_appear_info, output_data):
    # Add the special items, so they can be spawned from treasure chests or furniture in game.
    items_to_add = ["mkinoko", "itembomb", "ice", "elffst", "elwfst", "elifst", "mstar", "mglove", "mshoes",
                    "rdiamond", "mheart", "lheart", "move_mheart"]
    for new_item in items_to_add:
        __add_appear_item(item_appear_info, new_item)

    # Gets the list of keys already added in the item appear table
    already_added_keys = [item_entry["item0"] for item_entry in item_appear_info.info_file_field_entries if
                          str(item_entry["item0"]).startswith("key_")]

    # For every key found in the generation output, add an entry for it in "itemappeartable".
    for item_name, item_data in output_data["Locations"].items():
        current_item = __get_item_name(item_data)
        if item_data["door_id"] > 0 and current_item not in already_added_keys:
            __add_appear_item(item_appear_info, current_item)


def __add_appear_item(item_appear_table_entry, item_name):
    new_item = {}
    for itemid in range(20):
        new_item["item" + str(itemid)] = item_name
    item_appear_table_entry.info_file_field_entries.append(new_item)


def update_treasure_table(treasure_info, character_info, output_data):
    # Clear out the vanilla treasuretable from everything.
    treasure_info.info_file_field_entries.clear()

    for x in character_info.info_file_field_entries:
        for item_name, item_data in output_data["Locations"].items():
            # Ignore output data not related to chests that are not chests.
            if not item_data["type"] == "Chest":
                continue

            # Find the proper chest in the proper room by looking comparing the Room ID.
            if x["name"].find("takara") != -1 and x["room_no"] == item_data["room_no"]:
                # Replace the Chest visuals with something that matches the item name in "characterinfo".
                x["name"] = __get_item_chest_visual(item_data["name"])

                # Define the actor name to use from the Location in the generation output.
                # Act differently if it's a key.
                # Also define the size of the chest from the item name.
                treasure_item_name = __get_item_name(item_data)
                if item_data["door_id"] == 0:
                    chest_size = __get_chest_size_from_item(item_data["name"])
                else:
                    chest_size = __get_chest_size_from_key(item_data["door_id"])

                coin_amount = 0
                bill_amount = 0
                gold_bar_amount = 0

                # Generate a random amount of money if the item is supposed to be a money bundle.
                if treasure_item_name == "money": #TODO support gems as well
                    coin_amount = randrange(5, 20)
                    bill_amount = randrange(10, 30)
                    gold_bar_amount = randrange(1, 5)

                # Add the entry for the chest in "treasuretable". Also includes the chest size.
                treasure_info.info_file_field_entries.append({
                    "other": treasure_item_name,
                    "room": item_data["room_no"],
                    "size": chest_size,
                    "coin": coin_amount,
                    "bill": bill_amount,
                    "gold": gold_bar_amount,
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
                    "camera": 0
                    })


# Indicates the chest size that will be loaded in game based on key type. 0 = small, 1 = medium, 2 = large
def __get_chest_size_from_key(key_id):
    match key_id:
        case 3 | 42 | 59 | 72:
            return 2
        case _:
            return 0


# Changes the type of chest loaded in game based on the type of item that is hidden inside
def __get_item_chest_visual(item_name):
    match item_name:
        case "Heart Key" | "Club Key" |  "Diamond Key" | "Spade Key":
            return "ytakara1"

        case "Small Heart" | "Large Heart":
            return "ytakara1"

        case "Fire Element Medal" | "Bomb":
            return "rtakara1"
        case "Water Element Medal" | "Poison Mushroom":
            return "btakara1"
        case "Ice Element Medal" | "Ice Trap":
            return "wtakara1"

        case "Mario's Hat" | "Mario's Letter" | "Mario's Shoe" | "Mario's Glove" | "Mario's Star":
            return "rtakara1"

        case "Money Bundle" | "Gold Diamond": #Todo support gems as well
            return "gtakara1"

    return "btakara1"


# Dictionary of Location names and their index in keyinfo.
LOCATION_TO_INDEX = {
    "The Well Key": 0,
    "Ghost Foyer Key": 1,
    "1F Bathroom Shelf Key": 3,
    "Fortune Teller Candles": 4,
    "Wardrobe Shelf Key": 5,
}


def update_key_info(key_info, output_data):
    # For every Freestanding Key in the game, replace its entry with the proper item from the generation output.
    for item_name, item_data in output_data["Locations"].items():
        if not item_data["type"] == "Freestanding":
            continue

        __set_key_info_entry(key_info.info_file_field_entries[LOCATION_TO_INDEX[item_name]], item_data)

        # if item_name == "Ghost Foyer Key":
            # key_info.info_file_field_entries[LOCATION_TO_INDEX[item_name]]["name"] = "vbody"
            # Todo remove this line after testing. Proper name is above.

    # Remove the cutscene HD key from the Foyer, which only appears in the cutscene.
    key_info.info_file_field_entries.remove(key_info.info_file_field_entries[2])


def __set_key_info_entry(key_info_single_entry, item_data):
    # Disable the item's invisible status by default.
    # This is needed since we change the appear_type to 0, which makes items other than keys not spawn out of bounds.
    key_info_single_entry["name"] = __get_item_name(item_data) if not item_data["door_id"] > 0 else (
            __get_key_name(item_data["door_id"]))
    key_info_single_entry["open_door_no"] = item_data["door_id"]
    key_info_single_entry["appear_type"] = 0
    key_info_single_entry["invisible"] = 0
    key_info_single_entry["appear_flag"] = 0
    key_info_single_entry["disappear_flag"] = 0


def update_furniture_info(furniture_info, item_appear_info, output_data):
    for x in furniture_info.info_file_field_entries:
        # If any of the arguments are used in the Study bookshelves / reading books, disable this.
        if x["arg0"] in [101, 102, 103, 104, 105, 106]:
            x["arg0"] = 0.0

        # If this is a book/bookshelf, set it to just shake, no book interaction.
        if x["move"] == 16:
            x["move"] = 0

        # If one of Vincent's painting, update the flag to disable zoom instead.
        # if furniture_info_entry.info_file_field_entries.index(x) in {692, 693, 694, 695, 696, 697}:
            # x["move"] = 0

    # List of furniture names that tend to spawn items up high or potentially out of bounds.
    higher_up_furniture = ["Painting", "Fan", "Mirror", "Picture"]

    for item_name, item_data in output_data["Locations"].items():
        if not item_data["type"] == "Furniture":
            continue

        # Update any furniture up high to spawn items at a lower y offset
        # Otherwise items are sent into the floor above or out of bounds, which makes it almost impossible to get.
        if any(high_furniture in item_name for high_furniture in higher_up_furniture):
            current_y_offset = furniture_info.info_file_field_entries[item_data["loc_enum"]]["item_offset_y"]
            furniture_info.info_file_field_entries[item_data["loc_enum"]]["item_offset_y"]= current_y_offset-50.0

        actor_item_name = __get_item_name(item_data)

        # Replace the furnitureinfo entry to spawn an item from the "itemappeartable".
        # If the entry is supposed to be money, then generate a random amount of coins and/or bills from it.
        item_appear_entry_idx = next(item_appear_entry for item_appear_entry in
            item_appear_info.info_file_field_entries if item_appear_entry["item0"] == actor_item_name)

        furniture_info.info_file_field_entries[item_data["loc_enum"]]["item_table"] = (
            item_appear_info.info_file_field_entries.index(item_appear_entry_idx))

        if actor_item_name == "money":  # TODO change once more money types are implement to force AP to change.
            furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate"] = (
                randrange(1, 3))
            furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate_num"] = (
                randrange(10, 40))


# Dictionary of Room names and their ID. Used for the Enemizer.
ROOM_ID_TO_NAME = {
    39: "Anteroom",
    35: "Parlor",
    27: "Sitting Room",
    16: "Graveyard",
    4: "Mirror Room",
    38: "Wardrobe",
    5: "Laundry Room",
    1: "Hidden Room",
    14: "Storage Room",
    8: "Kitchen",
    20: "1F Bathroom",
    23: "Courtyard",
    47: "Tea Room",
    42: "2F Washroom",
    13: "Projection Room",
    52: "Safari Room",
    63: "Cellar",
    50: "Telephone Room",
    60: "Roof",
    36: "Sealed Room",
    48: "Armory",
    66: "Pipe Room",
    10: "Ballroom",
    57: "Artist's Studio"
}


def update_enemy_info(enemy_info, output_data):
    # A list of all the ghost actors of the game we want to replace.
    # It excludes the "waiter" ghost as that is needed for Mr. Luggs to work properly.
    ghost_list = ["yapoo1", "mapoo1", "mopoo1",
                  "yapoo2", "mapoo2", "mopoo2",
                  "banaoba",
                  "topoo1", "topoo2", "topoo3", "topoo4",
                  "heypo1", "heypo2", "heypo3", "heypo4", "heypo5", "heypo6", "heypo7", "heypo8",
                  "skul",
                  "putcher1",
                  "tenjyo", "tenjyo2"]

    # If randomize ghosts options are enabled
    if output_data["Options"]["enemizer"] > 0:
        for x in enemy_info.info_file_field_entries:
            if not ROOM_ID_TO_NAME.keys().__contains__(x["room_no"]):
                continue
            room_enemy_entry = next(((key, val) for (key, val) in output_data["Room Enemies"].items() if
                ROOM_ID_TO_NAME[x["room_no"]] == key and x["name"] in ghost_list), None)
            if not room_enemy_entry is None or x["room_no"] == 35:
                apply_new_ghost(x, "No Element" if x["room_no"] == 35 else room_enemy_entry[1])

        # Disables enemies in furniture to allow them to spawn properly if an item is hidden inside said furniture.
        # if x["access_name"] != "(null)":
            # if "_99" in x["access_name"]:
                # TODO: Handle Speedy Ghosts for blackout
                # owo = True
            # else:
                # x["create_name"] = "(null)"
                # x["access_name"] = "(null)"
        # if x["cond_type"] == 17:
            # x["do_type"] = 6


def apply_new_ghost(enemy_info_entry, element):
    # The list of ghosts that can replace the vanilla ones. Only includes the ones without elements.
    # Excludes Skul ghosts as well unless the railinfo jmp table is updated.
    random_ghosts_to_patch = [["yapoo1"], ["mapoo1"], ["mopoo1"], ["banaoba"],
                              ["topoo1", "topoo2", "topoo3", "topoo4"],
                              ["heypo1", "heypo2", "heypo3", "heypo4", "heypo5", "heypo6", "heypo7", "heypo8"],
                              ["putcher1"], ["tenjyo", "tenjyo2"]]

    # If the vanilla ghost is a Ceiling Ghost, reduce its spawning Y position so the new ghost spawns on the floor.
    if "tenjyo" in enemy_info_entry["name"]:
        enemy_info_entry["pos_y"] -= 200.000

    # If a room is supposed to have an element, replace all the ghosts in it to be only ghosts with that element.
    # Otherwise, randomize the ghosts between the non-element ones from the list.
    match element:
        case "Ice":
            enemy_info_entry["name"] = "mapoo2"
        case "Water":
            enemy_info_entry["name"] = "mopoo2"
        case "Fire":
            enemy_info_entry["name"] = "yapoo2"
        case "No Element":
            enemy_info_entry["name"] = choice(choice(random_ghosts_to_patch))

    # If the new ghost is a Ceiling Ghost, increase its spawning Y position so it spawns in the air.
    if "tenjyo" in enemy_info_entry["name"]:
        enemy_info_entry["pos_y"] += 200.000