from random import randrange, choice

def update_event_info(event_info):
    for x in event_info.info_file_field_entries[:]:
        # Removes events that we don't want to trigger at all in the mansion, such as some E. Gadd calls, warps after
        # boss battles / grabbing boss keys, and various cutscenes etc.
        if x["EventNo"] in {15, 11, 42, 80, 96, 16, 70, 69, 35, 85, 73, 47, 54, 91}:
            event_info.info_file_field_entries.remove(x)

        # Allows the Ring of Boos on the 3F Balcony to only appear when the Ice Medal has been collected.
        # This prevents being softlocked in Boolossus and having to reset the game without saving.
        if x["EventNo"] == 71:
            x["EventFlag"] = 22

def update_character_info(character_info, output_data):
    for x in character_info.info_file_field_entries[:]:
        # Removes useless cutscene objects and the vacuum in the Parlor under the closet.
        if x["name"] in {"vhead", "vbody", "dhakase", "demobak1", "dluige01"}:
            character_info.info_file_field_entries.remove(x)

        # Replace the mstar Observatory item with its randomized item.
        if x["name"] == "mstar":
            for item_name, item_data in output_data["Locations"].items():
                if item_name == "Observatory Mario Star":
                    if item_data["door_id"] == 0:
                        item_name = get_item_name(item_data["name"], item_data)
                    else:
                        item_name = "key_" + str(item_data["door_id"])
                    x["name"] = item_name
                    break

        # Allow Chauncey, Lydia, and the Twins to spawn as soon as a new game is created.
        if x["name"] in {"baby", "mother", "dboy", "dboy2"}:
            x["appear_flag"] = 0

        # Fix a Nintendo mistake where the Cellar chest has a room ID of 0 instead of 63.
        if x["create_name"] == "63_2":
            x["room_no"] = 63

def update_observer_info(observer_info):
    for x in observer_info.info_file_field_entries[:]:
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

        # Remove locking doors behind Luigi in dark rooms to prevent softlocks
        if x["do_type"] == 11:
            x["do_type"] = 0

        # Ignore me, I am the observers that spawn ghosts for Vincent
        # if x["string_arg0"] in ["57_1", "57_2", "57_3", "57_4", "57_5", "57_6", "57_7"]:
        #    x["string_arg0"] = "(null)"

def update_generator_info(generator_info):
    for x in generator_info.info_file_field_entries[:]:
        # Allows the Ring of Boos on the 3F Balcony to only appear when the Ice Medal has been collected.
        # This prevents being softlocked in Boolossus and having to reset the game without saving.
        if x["type"] == "demotel2":
            x["appear_flag"] = 22

def update_obj_info(obj_info):
    for x in obj_info.info_file_field_entries[:]:
        # Removes the vines on Area doors, as those require the Area Number of the game to be changed
        # to have them disappear.
        if x["name"] in {"eldoor07", "eldoor08", "eldoor09", "eldoor10"}:
            obj_info.info_file_field_entries.remove(x)

def __get_chest_size_from_item(item_name):
    match item_name:
        case "Mario's Hat" | "Mario's Letter" | "Mario's Shoe" | "Mario's Glove" | "Mario's Star":
            return 0

        case "Small Heart":
            return 0
        case "Large Heart":
            return 1

        case "Poison Mushroom" | "Bomb" | "Gold Diamond":
            return 2

        case "Fire Element Medal" | "Water Element Medal" | "Ice Element Medal":
            return 2

        case "Money Bundle":
            return 1

    return 0

def __get_chest_size_from_key(key_id):
    match key_id:
        case 3 | 42 | 59 | 72:
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
    #item_info_table_entry.info_file_field_entries.clear()

    #__add_info_item(item_info_table_entry, "nothing")

    # For every key found in the generation output, add an entry for it in "iteminfotable".
    for item_name, item_data in output_data["Locations"].items():
        if item_data["door_id"] != 0:
            item_name = "key_" + str(item_data["door_id"])
            item_info_table_entry.info_file_field_entries.append({
                "name": item_name,
                "character_name": __get_key_name(item_data["door_id"]) if item_data["door_id"] != 0 else item_name,
                "open_door_no": item_data["door_id"],
                "hp_amount": 0,
                "is_escape": 0
            })

    # Add the rest of the items that can spawn in the game, so they can be spawned from treasure chests or furniture.
    #__add_info_item(item_info_table_entry, "money")
    __add_info_item(item_info_table_entry, "rdiamond")

    #__add_info_item(item_info_table_entry, "sheart", 10, 0)
    #__add_info_item(item_info_table_entry, "mheart", 20, 0)
    #__add_info_item(item_info_table_entry, "lheart", 50, 0)

    #__add_info_item(item_info_table_entry, "move_sheart", 10, 1)
    #__add_info_item(item_info_table_entry, "move_mheart", 20, 1)
    #__add_info_item(item_info_table_entry, "move_lheart", 50, 1)

    #__add_info_item(item_info_table_entry, "mkinoko")
    __add_info_item(item_info_table_entry, "itembomb")

    #__add_info_item(item_info_table_entry, "elffst")
    #__add_info_item(item_info_table_entry, "elwfst")
    #__add_info_item(item_info_table_entry, "elifst")

    #__add_info_item(item_info_table_entry, "mcap")
    #__add_info_item(item_info_table_entry, "mletter")
    #__add_info_item(item_info_table_entry, "mshoes")
    #__add_info_item(item_info_table_entry, "mglove")
    __add_info_item(item_info_table_entry, "mstar")

def __add_info_item(item_info_table_entry, item_name, hp_amount = 0, is_escape = 0):
    item_info_table_entry.info_file_field_entries.append({
        "name": item_name,
        "character_name": item_name,
        "open_door_no": 0,
        "hp_amount": hp_amount,
        "is_escape": is_escape
    })

def __add_appear_item(item_appear_table_entry, item_name):
    new_item = {}
    for itemid in range(20):
        new_item["item" + str(itemid)] = item_name
    item_appear_table_entry.info_file_field_entries.append(new_item)

def update_item_appear_table(item_appear_table_entry, output_data):
    # Replace all original entries of "itemappeartable" to be filled with "nothing".
    # This prevents vanilla actors to spawn things, without breaking them.
    #for x in item_appear_table_entry.info_file_field_entries[:]:
    #    for itemid in range(20):
    #        x["item" + str(itemid)] = "nothing"

    # For every key found in the generation output, add an entry for it in "itemappeartable".
    for item_name, item_data in output_data["Locations"].items():
        if item_data["door_id"] != 0:
            item_name = "key_" + str(item_data["door_id"])
            __add_appear_item(item_appear_table_entry, item_name)

    # Add the rest of the items that can spawn in the game, so they can be spawned from treasure chests or furniture.
    __add_appear_item(item_appear_table_entry, "rdiamond")

    __add_appear_item(item_appear_table_entry, "mkinoko")
    __add_appear_item(item_appear_table_entry, "itembomb")

    __add_appear_item(item_appear_table_entry, "elffst")
    __add_appear_item(item_appear_table_entry, "elwfst")
    __add_appear_item(item_appear_table_entry, "elifst")

    __add_appear_item(item_appear_table_entry, "mshoes")
    __add_appear_item(item_appear_table_entry, "mglove")
    __add_appear_item(item_appear_table_entry, "mstar")

def update_treasure_table(treasure_table_entry, character_info, output_data):
    # Clear out the vanilla treasuretable from everything.
    treasure_table_entry.info_file_field_entries.clear()

    for x in character_info.info_file_field_entries[:]:
        for item_name, item_data in output_data["Locations"].items():
            # Define the actor name to use from the Location in the generation output.
            # Act differently if it's a key.
            # Also define the size of the chest from the item name.
            if item_data["door_id"] == 0:
                item_name = get_item_name(item_data["name"], item_data)
                chest_size = __get_chest_size_from_item(item_data["name"])
            else:
                item_name = "key_" + str(item_data["door_id"])
                chest_size = __get_chest_size_from_key(item_data["door_id"])

            # If the item in the generation output we're looking at right now is supposed to be in a chest:
            if item_data["type"] == "Chest":
                # Find the proper chest in the proper room by looking comparing the Room ID.
                if x["name"].find("takara") != -1 and item_data["type"] == "Chest" and x["room_no"] == item_data["room_no"]:
                    # Replace the Chest visuals with something that matches the item name in "characterinfo".
                    x["name"] = __get_item_chest_visual(item_data["name"])

                    coin_amount = 0
                    bill_amount = 0
                    gold_bar_amount = 0

                    # Generate a random amount of money if the item is supposed to be a money bundle.
                    if item_name == "money":
                        coin_amount = randrange(10, 30)
                        bill_amount = randrange(10, 30)
                        gold_bar_amount = randrange(0, 1)

                    # Add the entry for the chest in "treasuretable". Also includes the chest size.
                    treasure_table_entry.info_file_field_entries.append({
                        "other": item_name,
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
                        "camera": 1
                    })
                    break

def __get_item_chest_visual(item_name):
    match item_name:
        case "Heart Key" | "Club Key" |  "Diamond Key" | "Spade Key":
            return "ytakara1"

        case "Small Heart" | "Large Heart":
            return "ytakara1"

        case "Poison Mushroom" | "Bomb":
            return "ytakara1"

        case "Fire Element Medal":
            return "rtakara1"
        case "Water Element Medal":
            return "btakara1"
        case "Ice Element Medal":
            return "wtakara1"

        case "Mario's Hat" | "Mario's Letter" | "Mario's Shoe" | "Mario's Glove" | "Mario's Star":
            return "rtakara1"

        case "Money Bundle" | "Gold Diamond":
            return "gtakara1"

    return "btakara1"

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
        case "Gold Diamond":
            return "rdiamond"
        case "Money Bundle":
            return "money"
        case "Poison Mushroom":
            return "mkinoko"
        case "Small Heart":
            return "sheart"
        case "Large Heart":
            return "lheart"
        case "Bomb":
            return "itembomb"

    return "nothing"

def set_key_info_entry(key_entry, item_data, item_name):
    new_item_name = get_item_name(item_data["name"], item_data)

    # Disable the item's invisible status by default.
    # This is needed since we change the appear_type to 0, which makes items other than keys not spawn out of bounds.
    # IIRC, the default appear_type for keys in keyinfo makes them visible, even if invisible is set to 1.
    key_entry["name"] = new_item_name
    key_entry["open_door_no"] = item_data["door_id"]
    key_entry["appear_type"] = 0
    key_entry["invisible"] = 0

    # Allow the Ghost Foyer Key to be spawned at the beginning of the game and work properly.
    if item_name == "Ghost Foyer Key":
        key_entry["appear_flag"] = 0
        key_entry["disappear_flag"] = 0

# List of Location names and their index in keyinfo.
LOCATION_TO_INDEX = {
    "The Well Key": 0,
    "Ghost Foyer Key": 1,
    "1F Bathroom Shelf Key": 3,
    "Fortune Teller Candles": 4,
    "Wardrobe Shelf Key": 5,
}

def update_key_info(key_info_entry, output_data):
    # For every Freestanding Key in the game, replace its entry with the proper item from the generation output.
    for item_name, item_data in output_data["Locations"].items():
        for location_name, keyinfo_index in LOCATION_TO_INDEX.items():
            if location_name == item_name:
                set_key_info_entry(key_info_entry.info_file_field_entries[keyinfo_index], item_data, item_name)
                break

    # Remove the cutscene HD key from the Foyer, which only appears in the cutscene.
    key_info_entry.info_file_field_entries.remove(key_info_entry.info_file_field_entries[2])

# List of furniture names that tend to spawn items up high or potentially out of bounds.
higher_up_furniture = ["Painting", "Fan", "Mirror", "Picture"]

def update_furniture_info(furniture_info_entry, item_appear_table_entry, output_data):
    for x in furniture_info_entry.info_file_field_entries:
        # If any of the arguments are used in the Study bookshelves / reading books, disable this.
        if x["arg0"] in {101, 102, 103, 104, 105, 106}:
            x["arg0"] = 0.0

        # If this is a book/bookshelf, set it to just shake, no book interaction. Only modify in the Study.
        if x["move"] == 16 and x["room_no"] == 34:
            x["move"] = 0

        # If one of Vincent's painting, update the flag to disable zoom instead.
        # if furniture_info_entry.info_file_field_entries.index(x) in {692, 693, 694, 695, 696, 697}:
            # x["move"] = 0

    for item_name, item_data in output_data["Locations"].items():
        if not item_data["type"] == "Furniture":
            continue

        # Update any furniture up high to spawn items at a lower y offset
        # Otherwise items are sent into the floor above or out of bounds, which makes it almost impossible to get.
        if any(high_furniture in item_name for high_furniture in higher_up_furniture):
            current_y_offset = furniture_info_entry.info_file_field_entries[item_data["loc_enum"]]["item_offset_y"]
            furniture_info_entry.info_file_field_entries[item_data["loc_enum"]]["item_offset_y"]= current_y_offset-50.0

        # Replace the furnitureinfo entry to spawn an item from the "itemappeartable".
        # If the entry is supposed to be money, then generate a random amount of coins and/or bills from it.
        for x in item_appear_table_entry.info_file_field_entries:
            actor_item_name = get_item_name(item_data["name"], item_data)
            if x["item0"] == "key_" + str(item_data["door_id"]) or x["item0"] == actor_item_name:
                if x["item19"] == "key_" + str(item_data["door_id"]) or x["item19"] == actor_item_name:
                    furniture_info_entry.info_file_field_entries[item_data["loc_enum"]]["item_table"] = (
                        item_appear_table_entry.info_file_field_entries.index(x))
                    if actor_item_name == "money": # TODO change once more money types are implement to force AP to change.
                        furniture_info_entry.info_file_field_entries[item_data["loc_enum"]]["generate"] = randrange(1, 3)
                        furniture_info_entry.info_file_field_entries[item_data["loc_enum"]]["generate_num"] = randrange(10, 40)
                    break

# List of Room names and their ID. Used for the Enemizer.
ROOM_TO_ID = {
    "Wardrobe": 38,
    "Laundry Room": 5,
    "Hidden Room": 1,
    "Storage Room": 14,
    "Kitchen": 8,
    "1F Bathroom": 20,
    "Courtyard": 23,
    "Tea Room": 47,
    "2F Washroom": 42,
    "Projection Room": 13,
    "Safari Room": 52,
    "Cellar": 63,
    "Telephone Room": 50,
    "Roof": 60,
    "Sealed Room": 36,
    "Armory": 48,
    "Pipe Room": 66,
    "Ballroom": 10,
    "Artist's Studio": 57
}

def apply_new_ghost(x, element):
    # The list of ghosts that can replace the vanilla ones. Only includes the ones without elements.
    random_ghosts_to_patch = [["yapoo1"], ["mapoo1"], ["mopoo1"], ["banaoba"],
                              ["topoo1", "topoo2", "topoo3", "topoo4"],
                              ["heypo1", "heypo2", "heypo3", "heypo4", "heypo5", "heypo6", "heypo7", "heypo8"],
                              ["putcher1"], ["tenjyo", "tenjyo2"]]

    # If the vanilla ghost is a Ceiling Ghost, reduce its spawning Y position so the new ghost spawns on the floor.
    if "tenjyo" in x["name"]:
        x["pos_y"] -= 200.000

    # If a room is supposed to have an element, replace all the ghosts in it to be only ghosts with that element.
    # Otherwise, randomize the ghosts between the non-element ones from the list.
    match element:
        case "Ice":
            x["name"] = "mapoo2"
        case "Water":
            x["name"] = "mopoo2"
        case "Fire":
            x["name"] = "yapoo2"
        case "No Element":
            x["name"] = choice(choice(random_ghosts_to_patch))

    # If the new ghost is a Ceiling Ghost, increase its spawning Y position so it spawns in the air.
    if "tenjyo" in x["name"]:
        x["pos_y"] += 200.000

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

    for x in enemy_info.info_file_field_entries[:]:
        # Randomize Ghosts
        if output_data["Options"]["enemizer"] > 0:
            for room_name, element in output_data["Room Enemies"].items():
                # Only replace ghosts in rooms that are defined in the ROOM_TO_ID list.
                if x["room_no"] == ROOM_TO_ID[room_name] and x["name"] in ghost_list:
                    apply_new_ghost(x, element)
                    break