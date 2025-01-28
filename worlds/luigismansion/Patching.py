import re
from random import choice

from .Items import filler_items


# Converts AP readable name to in-game name
def __get_item_name(item_data):
    if item_data["door_id"] != 0:
        return "key_" + str(item_data["door_id"])
    elif "Bills" in item_data["name"] or "Coins" in item_data["name"] or "Gold Bars" in item_data["name"]:
        return "money"

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
        case "Sapphire":
            return "sapphire"
        case "Emerald":
            return "emerald"
        case "Ruby":
            return "ruby"
        case "Diamond":
            return "diamond"

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
        case "Banana Trap":
            return "banana"

    return "nothing"


def update_event_info(event_info, boo_checks: bool):
    # Removes events that we don't want to trigger at all in the mansion, such as some E. Gadd calls, warps after
    # boss battles / grabbing boss keys, and various cutscenes etc.
    events_to_remove = [11, 15, 42, 54, 69, 70, 73, 80, 81, 85, 91, 92, 93, 94]

    # Only remove the boo checks if the player does not want them.
    if not boo_checks:
        events_to_remove = events_to_remove + [16, 47, 96]

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

        # Removes the zoom on Bogmire's tombstone
        if x["EventNo"] == 65:
            x["disappear_flag"] = 10

        # Removes the Mr. Bones requirement. He will spawn instantly
        if x["EventNo"] == 23:
            x["EventFlag"] = 0
            x["disappear_flag"] = 74

        # Update the Washroom event trigger to be area entry based
        # Also updates the event disappear trigger to be flag 28
        # Also updates the EventFlag to 0, so this event always plays
        if boo_checks and x["EventNo"] == 47:
            x["pos_x"] = -1625.000000
            x["pos_y"] = 100.000000
            x["pos_z"] = -4150.000000
            x["EventFlag"] = 0
            x["disappear_flag"] = 28
            x["EventIf"] = 5
            x["EventArea"] = 380
            x["EventLock"] = 1
            x["PlayerStop"] = 1
            x["EventLoad"] = 0

        # Update the King Boo event trigger to be area entry based
        if boo_checks and x["EventNo"] == 16:
            x["pos_x"] = 2260.000000
            x["pos_y"] = -450.000000
            x["pos_z"] = -5300.000000
            x["EventIf"] = 5
            x["EventArea"] = 200
            x["EventLock"] = 1
            x["PlayerStop"] = 1
            x["EventLoad"] = 0

        # Update the Balcony Boo event trigger to be area entry based
        if boo_checks and x["EventNo"] == 96:
            x["pos_x"] = 1800.000000
            x["pos_y"] = 1200.000000
            x["pos_z"] = -2600.000000
            x["EventIf"] = 5
            x["EventArea"] = 200
            x["EventLock"] = 1
            x["PlayerStop"] = 1
            x["EventLoad"] = 0


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

        # Remove King Boo in the hallway, since his event was removed.
        if x["name"] == "dltelesa" and x["room_no"] == 68:
            character_info.info_file_field_entries.remove(x)

        # Remove Miss Petunia to never disappear, unless captured.
        if x["name"] == "fat" and x["room_no"] == 45:
            x["disappear_flag"] = 0


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

    # Add our new custom events for turning on hallway lights
    # This one enables the hallway after beating Chauncey
    observer_info.info_file_field_entries.append({
        "name": "observer",
        "code_name": "(null)",
        "string_arg0": "(null)",
        "cond_string_arg0": "(null)",
        "pos_x": -3000.000000,
        "pos_y": 550.000000,
        "pos_z": -815.000000,
        "dir_x": 0.000000,
        "dir_y": 0.000000,
        "dir_z": 0.000000,
        "scale_x": 0.000000,
        "scale_y": 0.000000,
        "scale_z": 0.000000,
        "room_no": 29,
        "cond_arg0": 46,
        "arg0": 0,
        "arg1": 0,
        "arg2": 0,
        "arg3": 0,
        "arg4": 0,
        "arg5": 0,
        "appear_flag": 46,
        "disappear_flag": 0,
        "cond_type": 18,
        "do_type": 1,
        "invisible": 1,
        "(Undocumented)": 0,
    })
    # This one enables the Dinning 1F hallway after beating Bogmire
    observer_info.info_file_field_entries.append({
        "name": "observer",
        "code_name": "(null)",
        "string_arg0": "(null)",
        "cond_string_arg0": "(null)",
        "pos_x": 1200.000000,
        "pos_y": 0.000000,
        "pos_z": -1800.000000,
        "dir_x": 0.000000,
        "dir_y": 0.000000,
        "dir_z": 0.000000,
        "scale_x": 0.000000,
        "scale_y": 0.000000,
        "scale_z": 0.000000,
        "room_no": 53,
        "cond_arg0": 67,
        "arg0": 0,
        "arg1": 0,
        "arg2": 0,
        "arg3": 0,
        "arg4": 0,
        "arg5": 0,
        "appear_flag": 67,
        "disappear_flag": 0,
        "cond_type": 18,
        "do_type": 1,
        "invisible": 1,
        "(Undocumented)": 0,
    })
    # This one enables the Conservatory 1F hallway after beating Bogmire
    observer_info.info_file_field_entries.append({
        "name": "observer",
        "code_name": "(null)",
        "string_arg0": "(null)",
        "cond_string_arg0": "(null)",
        "pos_x": 1400.000000,
        "pos_y": 0.000000,
        "pos_z": -4100.000000,
        "dir_x": 0.000000,
        "dir_y": 0.000000,
        "dir_z": 0.000000,
        "scale_x": 0.000000,
        "scale_y": 0.000000,
        "scale_z": 0.000000,
        "room_no": 18,
        "cond_arg0": 67,
        "arg0": 0,
        "arg1": 0,
        "arg2": 0,
        "arg3": 0,
        "arg4": 0,
        "arg5": 0,
        "appear_flag": 67,
        "disappear_flag": 0,
        "cond_type": 18,
        "do_type": 1,
        "invisible": 1,
        "(Undocumented)": 0,
    })
    # This one enables the 1F Washroom/Bathroom hallway after beating Bogmire
    observer_info.info_file_field_entries.append({
        "name": "observer",
        "code_name": "(null)",
        "string_arg0": "(null)",
        "cond_string_arg0": "(null)",
        "pos_x": -1250.000000,
        "pos_y": 0.000000,
        "pos_z": -4900.000000,
        "dir_x": 0.000000,
        "dir_y": 0.000000,
        "dir_z": 0.000000,
        "scale_x": 0.000000,
        "scale_y": 0.000000,
        "scale_z": 0.000000,
        "room_no": 7,
        "cond_arg0": 67,
        "arg0": 0,
        "arg1": 0,
        "arg2": 0,
        "arg3": 0,
        "arg4": 0,
        "arg5": 0,
        "appear_flag": 67,
        "disappear_flag": 0,
        "cond_type": 18,
        "do_type": 1,
        "invisible": 1,
        "(Undocumented)": 0,
    })
    # This one enables the Laundry 1F hallway after beating Bogmire
    observer_info.info_file_field_entries.append({
        "name": "observer",
        "code_name": "(null)",
        "string_arg0": "(null)",
        "cond_string_arg0": "(null)",
        "pos_x": -1300.000000,
        "pos_y": 0.000000,
        "pos_z": -1000.000000,
        "dir_x": 0.000000,
        "dir_y": 0.000000,
        "dir_z": 0.000000,
        "scale_x": 0.000000,
        "scale_y": 0.000000,
        "scale_z": 0.000000,
        "room_no": 6,
        "cond_arg0": 67,
        "arg0": 0,
        "arg1": 0,
        "arg2": 0,
        "arg3": 0,
        "arg4": 0,
        "arg5": 0,
        "appear_flag": 67,
        "disappear_flag": 0,
        "cond_type": 18,
        "do_type": 1,
        "invisible": 1,
        "(Undocumented)": 0,
    })
    # This one enables the 1F/2F Stairwell after beating Boolossus
    observer_info.info_file_field_entries.append({
        "name": "observer",
        "code_name": "(null)",
        "string_arg0": "(null)",
        "cond_string_arg0": "(null)",
        "pos_x": 3000.000000,
        "pos_y": 0.000000,
        "pos_z": -4100.000000,
        "dir_x": 0.000000,
        "dir_y": 0.000000,
        "dir_z": 0.000000,
        "scale_x": 0.000000,
        "scale_y": 0.000000,
        "scale_z": 0.000000,
        "room_no": 6,
        "cond_arg0": 81,
        "arg0": 0,
        "arg1": 0,
        "arg2": 0,
        "arg3": 0,
        "arg4": 0,
        "arg5": 0,
        "appear_flag": 81,
        "disappear_flag": 0,
        "cond_type": 18,
        "do_type": 1,
        "invisible": 1,
        "(Undocumented)": 0,
    })
    # This one enables the Astral 2F hallway after beating Boolossus
    observer_info.info_file_field_entries.append({
        "name": "observer",
        "code_name": "(null)",
        "string_arg0": "(null)",
        "cond_string_arg0": "(null)",
        "pos_x": 1250.000000,
        "pos_y": 550.000000,
        "pos_z": -3600.000000,
        "dir_x": 0.000000,
        "dir_y": 0.000000,
        "dir_z": 0.000000,
        "scale_x": 0.000000,
        "scale_y": 0.000000,
        "scale_z": 0.000000,
        "room_no": 26,
        "cond_arg0": 81,
        "arg0": 0,
        "arg1": 0,
        "arg2": 0,
        "arg3": 0,
        "arg4": 0,
        "arg5": 0,
        "appear_flag": 81,
        "disappear_flag": 0,
        "cond_type": 18,
        "do_type": 1,
        "invisible": 1,
        "(Undocumented)": 0,
    })
    # This one enables the Sitting Room 2F hallway after beating Boolossus
    observer_info.info_file_field_entries.append({
        "name": "observer",
        "code_name": "(null)",
        "string_arg0": "(null)",
        "cond_string_arg0": "(null)",
        "pos_x": 2250.000000,
        "pos_y": 550.000000,
        "pos_z": -980.000000,
        "dir_x": 0.000000,
        "dir_y": 0.000000,
        "dir_z": 0.000000,
        "scale_x": 0.000000,
        "scale_y": 0.000000,
        "scale_z": 0.000000,
        "room_no": 31,
        "cond_arg0": 81,
        "arg0": 0,
        "arg1": 0,
        "arg2": 0,
        "arg3": 0,
        "arg4": 0,
        "arg5": 0,
        "appear_flag": 81,
        "disappear_flag": 0,
        "cond_type": 18,
        "do_type": 1,
        "invisible": 1,
        "(Undocumented)": 0,
    })
    # This one enables the Sealed Room 2F hallway after beating Boolossus
    observer_info.info_file_field_entries.append({
        "name": "observer",
        "code_name": "(null)",
        "string_arg0": "(null)",
        "cond_string_arg0": "(null)",
        "pos_x": 1350.000000,
        "pos_y": 550.000000,
        "pos_z": -2000.000000,
        "dir_x": 0.000000,
        "dir_y": 0.000000,
        "dir_z": 0.000000,
        "scale_x": 0.000000,
        "scale_y": 0.000000,
        "scale_z": 0.000000,
        "room_no": 64,
        "cond_arg0": 81,
        "arg0": 0,
        "arg1": 0,
        "arg2": 0,
        "arg3": 0,
        "arg4": 0,
        "arg5": 0,
        "appear_flag": 81,
        "disappear_flag": 0,
        "cond_type": 18,
        "do_type": 1,
        "invisible": 1,
        "(Undocumented)": 0,
    })
    # This one enables the Area 3 Entrance 2F hallway after beating Boolossus
    observer_info.info_file_field_entries.append({
        "name": "observer",
        "code_name": "(null)",
        "string_arg0": "(null)",
        "cond_string_arg0": "(null)",
        "pos_x": 1750.000000,
        "pos_y": 550.000000,
        "pos_z": -4000.000000,
        "dir_x": 0.000000,
        "dir_y": 0.000000,
        "dir_z": 0.000000,
        "scale_x": 0.000000,
        "scale_y": 0.000000,
        "scale_z": 0.000000,
        "room_no": 43,
        "cond_arg0": 81,
        "arg0": 0,
        "arg1": 0,
        "arg2": 0,
        "arg3": 0,
        "arg4": 0,
        "arg5": 0,
        "appear_flag": 81,
        "disappear_flag": 0,
        "cond_type": 18,
        "do_type": 1,
        "invisible": 1,
        "(Undocumented)": 0,
    })
    # This one enables the Nana's 2F hallway after beating Boolossus
    observer_info.info_file_field_entries.append({
        "name": "observer",
        "code_name": "(null)",
        "string_arg0": "(null)",
        "cond_string_arg0": "(null)",
        "pos_x": -1300.000000,
        "pos_y": 550.000000,
        "pos_z": -5000.000000,
        "dir_x": 0.000000,
        "dir_y": 0.000000,
        "dir_z": 0.000000,
        "scale_x": 0.000000,
        "scale_y": 0.000000,
        "scale_z": 0.000000,
        "room_no": 44,
        "cond_arg0": 81,
        "arg0": 0,
        "arg1": 0,
        "arg2": 0,
        "arg3": 0,
        "arg4": 0,
        "arg5": 0,
        "appear_flag": 81,
        "disappear_flag": 0,
        "cond_type": 18,
        "do_type": 1,
        "invisible": 1,
        "(Undocumented)": 0,
    })
    # This one enables the 2F to Attic Stairwell after beating Boolossus
    observer_info.info_file_field_entries.append({
        "name": "observer",
        "code_name": "(null)",
        "string_arg0": "(null)",
        "cond_string_arg0": "(null)",
        "pos_x": 3900.000000,
        "pos_y": 880.000000,
        "pos_z": -980.000000,
        "dir_x": 0.000000,
        "dir_y": 0.000000,
        "dir_z": 0.000000,
        "scale_x": 0.000000,
        "scale_y": 0.000000,
        "scale_z": 0.000000,
        "room_no": 32,
        "cond_arg0": 81,
        "arg0": 0,
        "arg1": 0,
        "arg2": 0,
        "arg3": 0,
        "arg4": 0,
        "arg5": 0,
        "appear_flag": 81,
        "disappear_flag": 0,
        "cond_type": 18,
        "do_type": 1,
        "invisible": 1,
        "(Undocumented)": 0,
    })
    # This one enables the Safari's North hallway after beating Boolossus
    observer_info.info_file_field_entries.append({
        "name": "observer",
        "code_name": "(null)",
        "string_arg0": "(null)",
        "cond_string_arg0": "(null)",
        "pos_x": 2500.000000,
        "pos_y": 1200.000000,
        "pos_z": -900.000000,
        "dir_x": 0.000000,
        "dir_y": 0.000000,
        "dir_z": 0.000000,
        "scale_x": 0.000000,
        "scale_y": 0.000000,
        "scale_z": 0.000000,
        "room_no": 15,
        "cond_arg0": 81,
        "arg0": 0,
        "arg1": 0,
        "arg2": 0,
        "arg3": 0,
        "arg4": 0,
        "arg5": 0,
        "appear_flag": 81,
        "disappear_flag": 0,
        "cond_type": 18,
        "do_type": 1,
        "invisible": 1,
        "(Undocumented)": 0,
    })
    # This one enables the Safari's West hallway after beating Boolossus
    observer_info.info_file_field_entries.append({
        "name": "observer",
        "code_name": "(null)",
        "string_arg0": "(null)",
        "cond_string_arg0": "(null)",
        "pos_x": 1800.000000,
        "pos_y": 1200.000000,
        "pos_z": -300.000000,
        "dir_x": 0.000000,
        "dir_y": 0.000000,
        "dir_z": 0.000000,
        "scale_x": 0.000000,
        "scale_y": 0.000000,
        "scale_z": 0.000000,
        "room_no": 51,
        "cond_arg0": 81,
        "arg0": 0,
        "arg1": 0,
        "arg2": 0,
        "arg3": 0,
        "arg4": 0,
        "arg5": 0,
        "appear_flag": 81,
        "disappear_flag": 0,
        "cond_type": 18,
        "do_type": 1,
        "invisible": 1,
        "(Undocumented)": 0,
    })
    # This one enables the Artist's hallway after beating Boolossus
    observer_info.info_file_field_entries.append({
        "name": "observer",
        "code_name": "(null)",
        "string_arg0": "(null)",
        "cond_string_arg0": "(null)",
        "pos_x": 1800.000000,
        "pos_y": 1200.000000,
        "pos_z": -2600.000000,
        "dir_x": 0.000000,
        "dir_y": 0.000000,
        "dir_z": 0.000000,
        "scale_x": 0.000000,
        "scale_y": 0.000000,
        "scale_z": 0.000000,
        "room_no": 58,
        "cond_arg0": 1,  # 81
        "arg0": 0,
        "arg1": 0,
        "arg2": 0,
        "arg3": 0,
        "arg4": 0,
        "arg5": 0,
        "appear_flag": 1,  # 81
        "disappear_flag": 0,
        "cond_type": 18,
        "do_type": 1,
        "invisible": 1,
        "(Undocumented)": 0,
    })
    # This one enables the Ceramics hallway after beating Boolossus
    observer_info.info_file_field_entries.append({
        "name": "observer",
        "code_name": "(null)",
        "string_arg0": "(null)",
        "cond_string_arg0": "(null)",
        "pos_x": -1800.000000,
        "pos_y": 1200.000000,
        "pos_z": -2600.000000,
        "dir_x": 0.000000,
        "dir_y": 0.000000,
        "dir_z": 0.000000,
        "scale_x": 0.000000,
        "scale_y": 0.000000,
        "scale_z": 0.000000,
        "room_no": 54,
        "cond_arg0": 81,
        "arg0": 0,
        "arg1": 0,
        "arg2": 0,
        "arg3": 0,
        "arg4": 0,
        "arg5": 0,
        "appear_flag": 81,
        "disappear_flag": 0,
        "cond_type": 18,
        "do_type": 1,
        "invisible": 1,
        "(Undocumented)": 0,
    })
    # This one enables the Armory/Telephone hallway after beating Boolossus
    observer_info.info_file_field_entries.append({
        "name": "observer",
        "code_name": "(null)",
        "string_arg0": "(null)",
        "cond_string_arg0": "(null)",
        "pos_x": -1800.000000,
        "pos_y": 1200.000000,
        "pos_z": -300.000000,
        "dir_x": 0.000000,
        "dir_y": 0.000000,
        "dir_z": 0.000000,
        "scale_x": 0.000000,
        "scale_y": 0.000000,
        "scale_z": 0.000000,
        "room_no": 49,
        "cond_arg0": 81,
        "arg0": 0,
        "arg1": 0,
        "arg2": 0,
        "arg3": 0,
        "arg4": 0,
        "arg5": 0,
        "appear_flag": 81,
        "disappear_flag": 0,
        "cond_type": 18,
        "do_type": 1,
        "invisible": 1,
        "(Undocumented)": 0,
    })


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
    if "Bills" in item_name or "Coins" in item_name or "Gold Bars" in item_name:
        item_name = "Money"
    match item_name:
        case "Mario's Hat" | "Mario's Letter" | "Mario's Shoe" | "Mario's Glove" | "Mario's Star":
            return 0

        case "Small Heart" | "Money" :
            return 0
        case "Large Heart":
            return 1

        case "Poison Mushroom" | "Bomb" | "Ice Trap" | "Gold Diamond" | "Banana Trap":
            return 2

        case "Fire Element Medal" | "Water Element Medal" | "Ice Element Medal":
            return 2

        case "Sapphire" | "Emerald" | "Ruby" | "Diamond":
            return 1

    return 0

# For every key found in the generation output, add an entry for it in "iteminfotable".
def update_item_info_table(item_info, output_data):
    # Adds the special items so they can spawn in furniture or chests.
    items_to_add = ["rdiamond", "itembomb", "ice", "mstar", "banana", "diamond"]
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
                    "sheart", "lheart", "banana", "rdiamond", "diamond", "ruby", "emerald", "sapphire"]
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
                sapphire_amount = 0
                emerald_amount = 0
                ruby_amount = 0
                diamond_amount = 0



                # Generate a random amount of money if the item is supposed to be a money bundle.
                if treasure_item_name in ["money", "emerald", "sapphire", "ruby", "diamond"]:
                    if any((key, val) for (key, val) in filler_items.items() if
                           key == item_data["name"] and val.type == "Money"):
                        int_money_amt = 1
                        if re.search(r"^\d+", item_data["name"]):
                            int_money_amt = int(re.search(r"^\d+", item_data["name"]).group())
                        if "Coins" in item_data["name"]:
                            if "Bills" in item_data["name"]:
                                coin_amount = int_money_amt
                                bill_amount = int_money_amt
                            else:
                                coin_amount = int_money_amt
                        elif "Bills" in item_data["name"]:
                            bill_amount = int_money_amt
                        elif "Gold Bars" in item_data["name"]:
                            gold_bar_amount = int_money_amt
                        elif "Sapphire" in item_data["name"]:
                            sapphire_amount = int_money_amt
                        elif "Emerald" in item_data["name"]:
                            emerald_amount = int_money_amt
                        elif "Ruby" in item_data["name"]:
                            ruby_amount = int_money_amt
                        elif "Diamond" in item_data["name"]:
                            diamond_amount = int_money_amt



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
                    "sapphire": sapphire_amount,
                    "emerald": emerald_amount,
                    "ruby": ruby_amount,
                    "diamond": diamond_amount,
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
    if "Bills" in item_name or "Coins" in item_name or "Gold Bars" in item_name:
        item_name = "Money"
    match item_name:
        case "Heart Key" | "Club Key" | "Diamond Key" | "Spade Key":
            return "ytakara1"

        case "Small Heart" | "Large Heart":
            return "ytakara1"

        case "Fire Element Medal" | "Bomb" | "Ruby":
            return "rtakara1"
        case "Water Element Medal" | "Poison Mushroom" | "Banana Trap" | "Sapphire":
            return "btakara1"
        case "Ice Element Medal" | "Ice Trap" | "Diamond":
            return "wtakara1"

        case "Mario's Hat" | "Mario's Letter" | "Mario's Shoe" | "Mario's Glove" | "Mario's Star":
            return "rtakara1"

        case "Gold Diamond" | "Emerald" | "Money":
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
    # Adjust the item spawn height based on if the item spawns from the ceiling or high up on the wall.
    # Otherwise items are sent into the floor above or out of bounds, which makes it almost impossible to get.
    ceiling_furniture_list = [4, 43, 62, 63, 76, 77, 81, 84, 85, 91, 92, 101, 110, 111, 137, 156, 158, 159, 163,
        173, 174, 189, 190, 195, 199, 200, 228, 240, 266, 310, 342, 352, 354, 355, 356, 357, 358, 359, 373, 374,
        378, 379, 380, 381, 399, 423, 426, 445, 446, 454, 459, 460, 463, 467, 485, 547, 595, 596, 631, 632, 636,
        657, 671, 672]
    medium_height_furniture_list = [0, 1, 104, 112, 113, 114, 124, 125, 135, 136, 210, 232, 234, 235, 264, 265,
        270, 343, 344, 345, 346, 347, 353, 361, 362, 363, 368, 369, 370, 388, 397, 398, 411, 418, 438, 444, 520,
        526, 544, 552, 553, 554, 555, 602, 603, 634, 635]
    for furniture_jmp_id in (ceiling_furniture_list+medium_height_furniture_list):
        current_y_offset = furniture_info.info_file_field_entries[furniture_jmp_id]["item_offset_y"]
        adjust_y_offset = 125.0
        if furniture_jmp_id in ceiling_furniture_list:
            adjust_y_offset += 100.0
        furniture_info.info_file_field_entries[furniture_jmp_id]["item_offset_y"] = current_y_offset - adjust_y_offset

    for x in furniture_info.info_file_field_entries:
        # If this is a book/bookshelf, set it to just shake, no book interaction.
        # Make sure to exclude Nana's knit ball bowl so they can drop on the floor properly.
        if x["move"] == 16 and x["dmd_name"] != "o_tuku1":
            x["move"] = 0

        # If one of Vincent's painting, update the flag to disable zoom instead.
        # if furniture_info_entry.info_file_field_entries.index(x) in {692, 693, 694, 695, 696, 697}:
            # x["move"] = 0

    for item_name, item_data in output_data["Locations"].items():
        if not (item_data["type"] == "Furniture" or item_data["type"] == "Plant"):
            continue

        actor_item_name = __get_item_name(item_data)

        # Replace the furnitureinfo entry to spawn an item from the "itemappeartable".
        # If the entry is supposed to be money, then generate a random amount of coins and/or bills from it.
        filtered_item_appear = list(item_appear_entry for item_appear_entry in
            item_appear_info.info_file_field_entries if item_appear_entry["item0"] == actor_item_name)
        item_appear_entry_idx = filtered_item_appear[len(filtered_item_appear) - 1]

        furniture_info.info_file_field_entries[item_data["loc_enum"]]["item_table"] = (
            item_appear_info.info_file_field_entries.index(item_appear_entry_idx))

        if any((key, val) for (key, val) in filler_items.items() if
               key == item_data["name"] and key != "Diamond" and val.type == "Money"):
            furniture_info.info_file_field_entries[item_data["loc_enum"]]["item_table"] = 11
            int_money_amt = 1
            if re.search(r"^\d+", item_data["name"]):
                int_money_amt = int(re.search(r"^\d+", item_data["name"]).group())
            furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate_num"] = int_money_amt
            if "Coins" in item_data["name"]:
                if "Bills" in item_data["name"]:
                    furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate"] = 3
                else:
                    furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate"] = 1
            elif "Bills" in item_data["name"]:
                furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate"] = 2
            elif "Sapphire" in item_data["name"]:
                furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate"] = 4
            elif "Emerald" in item_data["name"]:
                furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate"] = 6
            elif "Ruby" in item_data["name"]:
                furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate"] = 5
            elif "Gold Bar" in item_data["name"]:
                furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate"] = 7
            else:
                furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate"] = 0
                furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate_num"] = 0
        else:
            furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate"] = 0
            furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate_num"] = 0


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

def update_boo_table(telesa_info):
    for x in telesa_info.info_file_field_entries:
        x["accel"] = 3.000000
        x["max_speed"] = 15.000000
        x["str_hp"] = 30
        x["move_time"] = 300
        x["attack"] = 0

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