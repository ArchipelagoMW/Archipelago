from random import randrange, choice

def update_event_info(event_info):
    # Removes events that we don't want to trigger at all in the mansion, such as some E. Gadd calls, warps after
    # boss battles / grabbing boss keys, and various cutscenes etc.
    events_to_remove = [15, 11, 42, 80, 96, 16, 70, 69, 35, 85, 73, 47, 54, 91]
    event_info.info_file_field_entries = list(filter(
        lambda info_entry: not info_entry["EventNo"] in events_to_remove, event_info.info_file_field_entries))

    for x in event_info.info_file_field_entries:
        # Allows the Ring of Boos on the 3F Balcony to only appear when the Ice Medal has been collected.
        # This prevents being soft locked in Boolossus and having to reset the game without saving.
        if x["EventNo"] == 71:
            x["EventFlag"] = 22


def update_character_info(character_info, output_data):
    # Removes useless cutscene objects and the vacuum in the Parlor under the closet.
    bad_actors_to_remove = ["vhead", "vbody", "dhakase", "demobak1", "dluige01"]
    character_info.info_file_field_entries = list(filter(
        lambda info_entry: not info_entry["name"] in bad_actors_to_remove, character_info.info_file_field_entries))

    for x in character_info.info_file_field_entries:
        # Replace the mstar Observatory item with its randomized item.
        if x["name"] == "mstar":
            mario_dict = output_data["Locations"]["Observatory Mario Star"]
            if mario_dict["door_id"] == 0:
                item_name = get_item_name(mario_dict["name"], mario_dict)
            else:
                item_name = "key_" + str(mario_dict["door_id"])
            x["name"] = item_name

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

        case "Money Bundle":
            return 1

    return 0


def update_item_info_table(item_info_table_entry, output_data):
    # Todo remove duplicate entries from keys here
    # TODO Update to use a filtered list
    # For every key found in the generation output, add an entry for it in "iteminfotable".
    for item_name, item_data in output_data["Locations"].items():
        if item_data["door_id"] != 0:
            item_name = "key_" + str(item_data["door_id"])
            item_info_table_entry.info_file_field_entries.append({
                "name": item_name,
                "character_name": __get_key_name(item_data["door_id"]),
                "open_door_no": item_data["door_id"],
                "hp_amount": 0,
                "is_escape": 0
            })

    # Adds the rest of the special items so they can spawn in furniture or chests.
    items_to_add = ["rdiamond", "mkinoko", "itembomb", "ice", "mstar"]
    for new_item in items_to_add:
        __add_info_item(item_info_table_entry, new_item)


def __add_info_item(item_info_table_entry, item_name, hp_amount = 0, is_escape = 0):
    item_info_table_entry.info_file_field_entries.append({
        "name": item_name,
        "character_name": item_name,
        "open_door_no": 0,
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


def update_item_appear_table(item_appear_table_entry, output_data):
    # Add the special items, so they can be spawned from treasure chests or furniture in game.
    items_to_add = ["mkinoko", "itembomb", "ice", "elffst", "elwfst", "elifst", "mstar", "mglove", "mshoes",
                    "rdiamond"]

    for new_item in items_to_add:
        __add_appear_item(item_appear_table_entry, new_item)

    # For every key found in the generation output, add an entry for it in "itemappeartable".
    for item_name, item_data in output_data["Locations"].items():
        if item_data["door_id"] != 0:
            item_name = "key_" + str(item_data["door_id"])
            __add_appear_item(item_appear_table_entry, item_name)


def __add_appear_item(item_appear_table_entry, item_name):
    new_item = {}
    for itemid in range(20):
        new_item["item" + str(itemid)] = item_name
    item_appear_table_entry.info_file_field_entries.append(new_item)


def update_treasure_table(treasure_table_entry, character_info, output_data):
    # Clear out the vanilla treasuretable from everything.
    treasure_table_entry.info_file_field_entries.clear()

    # TODO Update to use a filtered list
    for x in character_info.info_file_field_entries:
        for item_name, item_data in output_data["Locations"].items():
            # Ignore actors that are not chests.
            if not item_data["type"] == "Chest":
                continue

            # Find the proper chest in the proper room by looking comparing the Room ID.
            if (x["name"].find("takara") != -1 and item_data["type"] == "Chest" and
                    x["room_no"] == item_data["room_no"]):
                # Replace the Chest visuals with something that matches the item name in "characterinfo".
                x["name"] = __get_item_chest_visual(item_data["name"])

                # Define the actor name to use from the Location in the generation output.
                # Act differently if it's a key.
                # Also define the size of the chest from the item name.
                if item_data["door_id"] == 0:
                    item_name = get_item_name(item_data["name"], item_data)
                    chest_size = __get_chest_size_from_item(item_data["name"])
                else:
                    item_name = "key_" + str(item_data["door_id"])
                    chest_size = __get_chest_size_from_key(item_data["door_id"])

                coin_amount = 0
                bill_amount = 0
                gold_bar_amount = 0

                # Generate a random amount of money if the item is supposed to be a money bundle.
                if item_name == "money":
                    coin_amount = randrange(5, 20)
                    bill_amount = randrange(10, 30)
                    gold_bar_amount = randrange(1, 5)

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

        case "Money Bundle" | "Gold Diamond":
            return "gtakara1"

    return "btakara1"


# Converts AP readable name to in-game name
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
        case "Ice Trap":
            return "ice"

    return "nothing"


def set_key_info_entry(key_entry, item_data, item_name):
    # Disable the item's invisible status by default.
    # This is needed since we change the appear_type to 0, which makes items other than keys not spawn out of bounds.
    key_entry["name"] = get_item_name(item_data["name"], item_data)
    key_entry["open_door_no"] = item_data["door_id"]
    key_entry["appear_type"] = 0
    key_entry["invisible"] = 0
    key_entry["appear_flag"] = 0
    key_entry["disappear_flag"] = 0

    # Allow the Ghost Foyer Key to be spawned at the beginning of the game and work properly.
    # if item_name == "Ghost Foyer Key":
        # key_entry["name"] = "gameboy" #Todo remove this line after testing. Proper name is above.


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
        if x["arg0"] in [101, 102, 103, 104, 105, 106]:
            x["arg0"] = 0.0

        # If this is a book/bookshelf, set it to just shake, no book interaction.
        if x["move"] == 16:
            x["move"] = 0

        # If one of Vincent's painting, update the flag to disable zoom instead.
        # if furniture_info_entry.info_file_field_entries.index(x) in {692, 693, 694, 695, 696, 697}:
            # x["move"] = 0

    # TODO Update to use a filtered list
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
                furniture_info_entry.info_file_field_entries[item_data["loc_enum"]]["item_table"] = (
                    item_appear_table_entry.info_file_field_entries.index(x))
                if actor_item_name == "money": # TODO change once more money types are implement to force AP to change.
                    furniture_info_entry.info_file_field_entries[item_data["loc_enum"]]["generate"] = (
                        randrange(1, 3))
                    furniture_info_entry.info_file_field_entries[item_data["loc_enum"]]["generate_num"] = (
                        randrange(10, 40))
                break


# List of Room names and their ID. Used for the Enemizer.
ROOM_TO_ID = {
    "Mirror Room": 4,
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

    for x in enemy_info.info_file_field_entries:
        # Randomize Ghosts
        if output_data["Options"]["enemizer"] > 0:
            # TODO make this a next function so this will grab the first item and return instead of a for loop/break
            for room_name, element in output_data["Room Enemies"].items():
                # Only replace ghosts in rooms that are defined in the ROOM_TO_ID list.
                if x["room_no"] == ROOM_TO_ID[room_name] and x["name"] in ghost_list:
                    apply_new_ghost(x, element)
                    break

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