import logging

from BaseClasses import ItemClassification, Location, Item
from .data import iname, rname
from .options import CV64Options, BackgroundMusic, Countdown, IceTrapAppearance, InvisibleItems, CharacterStages
from .stages import vanilla_stage_order, get_stage_info
from .locations import get_location_info, base_id
from .regions import get_region_info
from .items import get_item_info, item_info

from typing import TYPE_CHECKING, Dict, List, Tuple, Union, Iterable

if TYPE_CHECKING:
    from . import CV64World

rom_sub_weapon_offsets = {
    0x10C6EB: (b"\x10", rname.forest_of_silence),  # Forest
    0x10C6F3: (b"\x0F", rname.forest_of_silence),
    0x10C6FB: (b"\x0E", rname.forest_of_silence),
    0x10C703: (b"\x0D", rname.forest_of_silence),

    0x10C81F: (b"\x0F", rname.castle_wall),  # Castle Wall
    0x10C827: (b"\x10", rname.castle_wall),
    0x10C82F: (b"\x0E", rname.castle_wall),
    0x7F9A0F: (b"\x0D", rname.castle_wall),

    0x83A5D9: (b"\x0E", rname.villa),  # Villa
    0x83A5E5: (b"\x0D", rname.villa),
    0x83A5F1: (b"\x0F", rname.villa),
    0xBFC903: (b"\x10", rname.villa),
    0x10C987: (b"\x10", rname.villa),
    0x10C98F: (b"\x0D", rname.villa),
    0x10C997: (b"\x0F", rname.villa),
    0x10CF73: (b"\x10", rname.villa),

    0x10CA57: (b"\x0D", rname.tunnel),  # Tunnel
    0x10CA5F: (b"\x0E", rname.tunnel),
    0x10CA67: (b"\x10", rname.tunnel),
    0x10CA6F: (b"\x0D", rname.tunnel),
    0x10CA77: (b"\x0F", rname.tunnel),
    0x10CA7F: (b"\x0E", rname.tunnel),

    0x10CBC7: (b"\x0E", rname.castle_center),  # Castle Center
    0x10CC0F: (b"\x0D", rname.castle_center),
    0x10CC5B: (b"\x0F", rname.castle_center),

    0x10CD3F: (b"\x0E", rname.tower_of_execution),  # Character towers
    0x10CD65: (b"\x0D", rname.tower_of_execution),
    0x10CE2B: (b"\x0E", rname.tower_of_science),
    0x10CE83: (b"\x10", rname.duel_tower),

    0x10CF8B: (b"\x0F", rname.room_of_clocks),  # Room of Clocks
    0x10CF93: (b"\x0D", rname.room_of_clocks),

    0x99BC5A: (b"\x0D", rname.clock_tower),  # Clock Tower
    0x10CECB: (b"\x10", rname.clock_tower),
    0x10CED3: (b"\x0F", rname.clock_tower),
    0x10CEDB: (b"\x0E", rname.clock_tower),
    0x10CEE3: (b"\x0D", rname.clock_tower),
}

rom_sub_weapon_flags = {
    0x10C6EC: b"\x02\x00\xFF\x04",  # Forest of Silence
    0x10C6FC: b"\x04\x00\xFF\x04",
    0x10C6F4: b"\x08\x00\xFF\x04",
    0x10C704: b"\x40\x00\xFF\x04",

    0x10C831: b"\x08",  # Castle Wall
    0x10C829: b"\x10",
    0x10C821: b"\x20",
    0xBFCA97: b"\x04",

    # Villa
    0xBFC926: b"\xFF\x04",
    0xBFC93A: b"\x80",
    0xBFC93F: b"\x01",
    0xBFC943: b"\x40",
    0xBFC947: b"\x80",
    0x10C989: b"\x10",
    0x10C991: b"\x20",
    0x10C999: b"\x40",
    0x10CF77: b"\x80",

    0x10CA58: b"\x40\x00\xFF\x0E",  # Tunnel
    0x10CA6B: b"\x80",
    0x10CA60: b"\x10\x00\xFF\x05",
    0x10CA70: b"\x20\x00\xFF\x05",
    0x10CA78: b"\x40\x00\xFF\x05",
    0x10CA80: b"\x80\x00\xFF\x05",

    0x10CBCA: b"\x02",  # Castle Center
    0x10CC10: b"\x80",
    0x10CC5C: b"\x40",

    0x10CE86: b"\x01",  # Duel Tower
    0x10CD43: b"\x02",  # Tower of Execution
    0x10CE2E: b"\x20",  # Tower of Science

    0x10CF8E: b"\x04",  # Room of Clocks
    0x10CF96: b"\x08",

    0x10CECE: b"\x08",  # Clock Tower
    0x10CED6: b"\x10",
    0x10CEE6: b"\x20",
    0x10CEDE: b"\x80",
}

rom_empty_breakables_flags = {
    0x10C74D: b"\x40\xFF\x05",  # Forest of Silence
    0x10C765: b"\x20\xFF\x0E",
    0x10C774: b"\x08\x00\xFF\x0E",
    0x10C755: b"\x80\xFF\x05",
    0x10C784: b"\x01\x00\xFF\x0E",
    0x10C73C: b"\x02\x00\xFF\x0E",

    0x10C8D0: b"\x04\x00\xFF\x0E",  # Villa foyer

    0x10CF9F: b"\x08",  # Room of Clocks flags
    0x10CFA7: b"\x01",
    0xBFCB6F: b"\x04",  # Room of Clocks candle property IDs
    0xBFCB73: b"\x05",
}

rom_axe_cross_lower_values = {
    0x6: [0x7C7F97, 0x07],  # Forest
    0x8: [0x7C7FA6, 0xF9],

    0x30: [0x83A60A, 0x71],  # Villa hallway
    0x27: [0x83A617, 0x26],
    0x2C: [0x83A624, 0x6E],

    0x16C: [0x850FE6, 0x07],  # Villa maze

    0x10A: [0x8C44D3, 0x08],  # CC factory floor
    0x109: [0x8C44E1, 0x08],

    0x74: [0x8DF77C, 0x07],  # CC invention area
    0x60: [0x90FD37, 0x43],
    0x55: [0xBFCC2B, 0x43],
    0x65: [0x90FBA1, 0x51],
    0x64: [0x90FBAD, 0x50],
    0x61: [0x90FE56, 0x43]
}

rom_looping_music_fade_ins = {
    0x10: None,
    0x11: None,
    0x12: None,
    0x13: None,
    0x14: None,
    0x15: None,
    0x16: 0x17,
    0x18: 0x19,
    0x1A: 0x1B,
    0x21: 0x75,
    0x27: None,
    0x2E: 0x23,
    0x39: None,
    0x45: 0x63,
    0x56: None,
    0x57: 0x58,
    0x59: None,
    0x5A: None,
    0x5B: 0x5C,
    0x5D: None,
    0x5E: None,
    0x5F: None,
    0x60: 0x61,
    0x62: None,
    0x64: None,
    0x65: None,
    0x66: None,
    0x68: None,
    0x69: None,
    0x6D: 0x78,
    0x6E: None,
    0x6F: None,
    0x73: None,
    0x74: None,
    0x77: None,
    0x79: None
}

music_sfx_ids = [0x1C, 0x4B, 0x4C, 0x4D, 0x4E, 0x55, 0x6C, 0x76]

renon_item_dialogue = {
    0x02: "More Sub-weapon uses!\n"
          "Just what you need!",
    0x03: "Galamoth told me it's\n"
          "a heart in other times.",
    0x04: "Who needs Warp Rooms\n"
          "when you have these?",
    0x05: "I was told to safeguard\n"
          "this, but I dunno why.",
    0x06: "Fresh off a Behemoth!\n"
          "Those cows are weird.",
    0x07: "Preserved with special\n"
          " wall-based methods.",
    0x08: "Don't tell Geneva\n"
          "about this...",
    0x09: "If this existed in 1094,\n"
          "that whip wouldn't...",
    0x0A: "For when some lizard\n"
          "brain spits on your ego.",
    0x0C: "It'd be a shame if you\n"
          "lost it immediately...",
    0x10C: "No consequences should\n"
           "you perish with this!",
    0x0D: "Arthur was far better\n"
          "with it than you!",
    0x0E: "Night Creatures handle\n"
          "with care!",
    0x0F: "Some may call it a\n"
          "\"Banshee Boomerang.\"",
    0x10: "No weapon triangle\n"
          "advantages with this.",
    0x12: "It looks sus? Trust me,"
          "my wares are genuine.",
    0x15: "This non-volatile kind\n"
          "is safe to handle.",
    0x16: "If you can soul-wield,\n"
          "they have a good one!",
    0x17: "Calls the morning sun\n"
          "to vanquish the night.",
    0x18: "1 on-demand horrible\n"
          "night. Devils love it!",
    0x1A: "Want to study here?\n"
          "It will cost you.",
    0x1B: "\"Let them eat cake!\"\n"
          "Said no princess ever.",
    0x1C: "Why do I suspect this\n"
          "was a toilet room?",
    0x1D: "When you see Coller,\n"
          "tell him I said hi!",
    0x1E: "Atomic number is 29\n"
          "and weight is 63.546.",
    0x1F: "One torture per pay!\n"
          "Who will it be?",
    0x20: "Being here feels like\n"
          "time is slowing down.",
    0x21: "Only one thing beind\n"
          "this. Do you dare?",
    0x22: "The key 2 Science!\n"
          "Both halves of it!",
    0x23: "This warehouse can\n"
          "be yours for a fee.",
    0x24: "Long road ahead if you\n"
          "don't have the others.",
    0x25: "Will you get the curse\n"
          "of eternal burning?",
    0x26: "What's beyond time?\n"
          "Find out your",
    0x27: "Want to take out a\n"
          "loan? By all means!",
    0x28: "The bag is green,\n"
          "so it must be lucky!",
    0x29: "(Does this fool realize?)\n"
          "Oh, sorry.",
    "prog": "They will absolutely\n"
            "need it in time!",
    "useful": "Now, this would be\n"
              "useful to send...",
    "common": "Every last little bit\n"
              "helps, right?",
    "trap": "I'll teach this fool\n"
            " a lesson for a price!",
    "dlc coin": "1 coin out of... wha!?\n"
                "You imp, why I oughta!"
}


def randomize_lighting(world: "CV64World") -> Dict[int, bytes]:
    """Generates randomized data for the map lighting table."""
    randomized_lighting = {}
    for entry in range(67):
        for sub_entry in range(19):
            if sub_entry not in [3, 7, 11, 15] and entry != 4:
                # The fourth entry in the lighting table affects the lighting on some item pickups; skip it
                randomized_lighting[0x1091A0 + (entry * 28) + sub_entry] = bytes([world.random.randint(0, 255)])
    return randomized_lighting


def shuffle_sub_weapons(world: "CV64World") -> Dict[int, bytes]:
    """Shuffles the sub-weapons amongst themselves."""
    sub_weapon_dict = {offset: rom_sub_weapon_offsets[offset][0] for offset in rom_sub_weapon_offsets if
                       rom_sub_weapon_offsets[offset][1] in world.active_stage_exits}

    # Remove the one 3HB sub-weapon in Tower of Execution if 3HBs are not shuffled.
    if not world.options.multi_hit_breakables and 0x10CD65 in sub_weapon_dict:
        del (sub_weapon_dict[0x10CD65])

    sub_bytes = list(sub_weapon_dict.values())
    world.random.shuffle(sub_bytes)
    return dict(zip(sub_weapon_dict, sub_bytes))


def randomize_music(world: "CV64World") -> Dict[int, bytes]:
    """Generates randomized or disabled data for all the music in the game."""
    music_array = bytearray(0x7A)
    for number in music_sfx_ids:
        music_array[number] = number
    if world.options.background_music == BackgroundMusic.option_randomized:
        looping_songs = []
        non_looping_songs = []
        fade_in_songs = {}
        # Create shuffle-able lists of all the looping, non-looping, and fade-in track IDs
        for i in range(0x10, len(music_array)):
            if i not in rom_looping_music_fade_ins.keys() and i not in rom_looping_music_fade_ins.values() and \
                    i != 0x72:  # Credits song is blacklisted
                non_looping_songs.append(i)
            elif i in rom_looping_music_fade_ins.keys():
                looping_songs.append(i)
            elif i in rom_looping_music_fade_ins.values():
                fade_in_songs[i] = i
        # Shuffle the looping songs
        rando_looping_songs = looping_songs.copy()
        world.random.shuffle(rando_looping_songs)
        looping_songs = dict(zip(looping_songs, rando_looping_songs))
        # Shuffle the non-looping songs
        rando_non_looping_songs = non_looping_songs.copy()
        world.random.shuffle(rando_non_looping_songs)
        non_looping_songs = dict(zip(non_looping_songs, rando_non_looping_songs))
        non_looping_songs[0x72] = 0x72
        # Figure out the new fade-in songs if applicable
        for vanilla_song in looping_songs:
            if rom_looping_music_fade_ins[vanilla_song]:
                if rom_looping_music_fade_ins[looping_songs[vanilla_song]]:
                    fade_in_songs[rom_looping_music_fade_ins[vanilla_song]] = rom_looping_music_fade_ins[
                        looping_songs[vanilla_song]]
                else:
                    fade_in_songs[rom_looping_music_fade_ins[vanilla_song]] = looping_songs[vanilla_song]
        # Build the new music array
        for i in range(0x10, len(music_array)):
            if i in looping_songs.keys():
                music_array[i] = looping_songs[i]
            elif i in non_looping_songs.keys():
                music_array[i] = non_looping_songs[i]
            else:
                music_array[i] = fade_in_songs[i]
    del (music_array[0x00: 0x10])

    return {0xBFCD30: bytes(music_array)}


def randomize_shop_prices(world: "CV64World") -> Dict[int, bytes]:
    """Randomize the shop prices based on the minimum and maximum values chosen.
    The minimum price will adjust if it's higher than the max."""
    min_price = world.options.minimum_gold_price.value
    max_price = world.options.maximum_gold_price.value

    if min_price > max_price:
        min_price = world.random.randint(0, max_price)
        logging.warning(f"[{world.multiworld.player_name[world.player]}] The Minimum Gold Price "
                        f"({world.options.minimum_gold_price.value * 100}) is higher than the "
                        f"Maximum Gold Price ({max_price * 100}). Lowering the minimum to: {min_price * 100}")
        world.options.minimum_gold_price.value = min_price

    shop_price_list = [world.random.randint(min_price * 100, max_price * 100) for _ in range(7)]

    # Convert the price list into a data dict.
    price_dict = {}
    for i in range(len(shop_price_list)):
        price_dict[0x103D6C + (i * 12)] = int.to_bytes(shop_price_list[i], 4, "big")

    return price_dict


def get_countdown_numbers(options: CV64Options, active_locations: Iterable[Location]) -> Dict[int, bytes]:
    """Figures out which Countdown numbers to increase for each Location after verifying the Item on the Location should
    increase a number.

    First, check the location's info to see if it has a countdown number override.
    If not, then figure it out based on the parent region's stage's position in the vanilla stage order.
    If the parent region is not part of any stage (as is the case for Renon's shop), skip the location entirely."""
    countdown_list = [0 for _ in range(15)]
    for loc in active_locations:
        if loc.address is not None and (options.countdown == Countdown.option_all_locations or
                                        (options.countdown == Countdown.option_majors
                                         and loc.item.advancement)):

            countdown_number = get_location_info(loc.name, "countdown")

            if countdown_number is None:
                stage = get_region_info(loc.parent_region.name, "stage")
                if stage is not None:
                    countdown_number = vanilla_stage_order.index(stage)

            if countdown_number is not None:
                countdown_list[countdown_number] += 1

    return {0xBFD818: bytes(countdown_list)}


def get_location_data(world: "CV64World", active_locations: Iterable[Location]) \
        -> Tuple[Dict[int, bytes], List[str], List[bytearray], List[List[Union[int, str, None]]]]:
    """Gets ALL the item data to go into the ROM. Item data consists of two bytes: the first dictates the appearance of
    the item, the second determines what the item actually is when picked up. All items from other worlds will be AP
    items that do nothing when picked up other than set their flag, and their appearance will depend on whether it's
    another CV64 player's item and, if so, what item it is in their game. Ice Traps can assume the form of any item that
    is progression, non-progression, or either depending on the player's settings.

    Appearance does not matter if it's one of the two NPC-given items (from either Vincent or Heinrich Meyer). For
    Renon's shop items, a list containing the shop item names, descriptions, and colors will be returned alongside the
    regular data."""

    # Figure out the list of possible Ice Trap appearances to use based on the settings, first and foremost.
    if world.options.ice_trap_appearance == IceTrapAppearance.option_major_only:
        allowed_classifications = ["progression", "progression skip balancing"]
    elif world.options.ice_trap_appearance == IceTrapAppearance.option_junk_only:
        allowed_classifications = ["filler", "useful"]
    else:
        allowed_classifications = ["progression", "progression skip balancing", "filler", "useful"]

    trap_appearances = []
    for item in item_info:
        if item_info[item]["default classification"] in allowed_classifications and item != "Ice Trap" and \
                get_item_info(item, "code") is not None:
            trap_appearances.append(item)

    shop_name_list = []
    shop_desc_list = []
    shop_colors_list = []

    location_bytes = {}

    for loc in active_locations:
        # If the Location is an event, skip it.
        if loc.address is None:
            continue

        loc_type = get_location_info(loc.name, "type")

        # Figure out the item ID bytes to put in each Location here. Write the item itself if either it's the player's
        # very own, or it belongs to an Item Link that the player is a part of.
        if loc.item.player == world.player:
            if loc_type not in ["npc", "shop"] and get_item_info(loc.item.name, "pickup actor id") is not None:
                location_bytes[get_location_info(loc.name, "offset")] = get_item_info(loc.item.name, "pickup actor id")
            else:
                location_bytes[get_location_info(loc.name, "offset")] = get_item_info(loc.item.name, "code") & 0xFF
        else:
            # Make the item the unused Wooden Stake - our multiworld item.
            location_bytes[get_location_info(loc.name, "offset")] = 0x11

        # Figure out the item's appearance. If it's a CV64 player's item, change the multiworld item's model to
        # match what it is. Otherwise, change it to an Archipelago progress or not progress icon. The model "change"
        # has to be applied to even local items because this is how the game knows to count it on the Countdown.
        if loc.item.game == "Castlevania 64":
            location_bytes[get_location_info(loc.name, "offset") - 1] = get_item_info(loc.item.name, "code")
        elif loc.item.advancement:
            location_bytes[get_location_info(loc.name, "offset") - 1] = 0x11  # Wooden Stakes are majors
        else:
            location_bytes[get_location_info(loc.name, "offset") - 1] = 0x12  # Roses are minors

        # If it's a PermaUp, change the item's model to a big PowerUp no matter what.
        if loc.item.game == "Castlevania 64" and loc.item.code == 0x10C + base_id:
            location_bytes[get_location_info(loc.name, "offset") - 1] = 0x0B

        # If it's an Ice Trap, change its model to one of the appearances we determined before.
        # Unless it's an NPC item, in which case use the Ice Trap's regular ID so that it won't decrement the majors
        # Countdown due to how I set up the NPC items to work.
        if loc.item.game == "Castlevania 64" and loc.item.code == 0x12 + base_id:
            if loc_type == "npc":
                location_bytes[get_location_info(loc.name, "offset") - 1] = 0x12
            else:
                location_bytes[get_location_info(loc.name, "offset") - 1] = \
                    get_item_info(world.random.choice(trap_appearances), "code")
                # If we chose a PermaUp as our trap appearance, change it to its actual in-game ID of 0x0B.
                if location_bytes[get_location_info(loc.name, "offset") - 1] == 0x10C:
                    location_bytes[get_location_info(loc.name, "offset") - 1] = 0x0B

        # Apply the invisibility variable depending on the "invisible items" setting.
        if (world.options.invisible_items == InvisibleItems.option_vanilla and loc_type == "inv") or \
                (world.options.invisible_items == InvisibleItems.option_hide_all and loc_type not in ["npc", "shop"]):
            location_bytes[get_location_info(loc.name, "offset") - 1] += 0x80
        elif world.options.invisible_items == InvisibleItems.option_chance and loc_type not in ["npc", "shop"]:
            invisible = world.random.randint(0, 1)
            if invisible:
                location_bytes[get_location_info(loc.name, "offset") - 1] += 0x80

        # If it's an Axe or Cross in a higher freestanding location, lower it into grab range.
        # KCEK made these spawn 3.2 units higher for some reason.
        if loc.address & 0xFFF in rom_axe_cross_lower_values and loc.item.code & 0xFF in [0x0F, 0x10]:
            location_bytes[rom_axe_cross_lower_values[loc.address & 0xFFF][0]] = \
                rom_axe_cross_lower_values[loc.address & 0xFFF][1]

        # Figure out the list of shop names, descriptions, and text colors here.
        if loc.parent_region.name != rname.renon:
            continue

        shop_name = loc.item.name
        if len(shop_name) > 18:
            shop_name = shop_name[0:18]
        shop_name_list.append(shop_name)

        if loc.item.player == world.player:
            shop_desc_list.append([get_item_info(loc.item.name, "code"), None])
        elif loc.item.game == "Castlevania 64":
            shop_desc_list.append([get_item_info(loc.item.name, "code"),
                                   world.multiworld.get_player_name(loc.item.player)])
        else:
            if loc.item.game == "DLCQuest" and loc.item.name in ["DLC Quest: Coin Bundle",
                                                                 "Live Freemium or Die: Coin Bundle"]:
                if getattr(world.multiworld.worlds[loc.item.player].options, "coinbundlequantity") == 1:
                    shop_desc_list.append(["dlc coin", world.multiworld.get_player_name(loc.item.player)])
                    shop_colors_list.append(get_item_text_color(loc))
                    continue

            if loc.item.advancement:
                shop_desc_list.append(["prog", world.multiworld.get_player_name(loc.item.player)])
            elif loc.item.classification == ItemClassification.useful:
                shop_desc_list.append(["useful", world.multiworld.get_player_name(loc.item.player)])
            elif loc.item.classification == ItemClassification.trap:
                shop_desc_list.append(["trap", world.multiworld.get_player_name(loc.item.player)])
            else:
                shop_desc_list.append(["common", world.multiworld.get_player_name(loc.item.player)])

        shop_colors_list.append(get_item_text_color(loc))

    return {offset: int.to_bytes(byte, 1, "big") for offset, byte in location_bytes.items()}, shop_name_list,\
        shop_colors_list, shop_desc_list


def get_loading_zone_bytes(options: CV64Options, starting_stage: str,
                           active_stage_exits: Dict[str, Dict[str, Union[str, int, None]]]) -> Dict[int, bytes]:
    """Figure out all the bytes for loading zones and map transitions based on which stages are where in the exit data.
    The same data was used earlier in figuring out the logic. Map transitions consist of two major components: which map
    to send the player to, and which spot within the map to spawn the player at."""

    # Write the byte for the starting stage to send the player to after the intro narration.
    loading_zone_bytes = {0xB73308: get_stage_info(starting_stage, "start map id")}

    for stage in active_stage_exits:

        # Start loading zones
        # If the start zone is the start of the line, have it simply refresh the map.
        if active_stage_exits[stage]["prev"] == "Menu":
            loading_zone_bytes[get_stage_info(stage, "startzone map offset")] = b"\xFF"
            loading_zone_bytes[get_stage_info(stage, "startzone spawn offset")] = b"\x00"
        elif active_stage_exits[stage]["prev"]:
            loading_zone_bytes[get_stage_info(stage, "startzone map offset")] = \
                get_stage_info(active_stage_exits[stage]["prev"], "end map id")
            loading_zone_bytes[get_stage_info(stage, "startzone spawn offset")] = \
                get_stage_info(active_stage_exits[stage]["prev"], "end spawn id")

            # Change CC's end-spawn ID to put you at Carrie's exit if appropriate
            if active_stage_exits[stage]["prev"] == rname.castle_center:
                if options.character_stages == CharacterStages.option_carrie_only or \
                        active_stage_exits[rname.castle_center]["alt"] == stage:
                    loading_zone_bytes[get_stage_info(stage, "startzone spawn offset")] = b"\x03"

        # End loading zones
        if active_stage_exits[stage]["next"]:
            loading_zone_bytes[get_stage_info(stage, "endzone map offset")] = \
                get_stage_info(active_stage_exits[stage]["next"], "start map id")
            loading_zone_bytes[get_stage_info(stage, "endzone spawn offset")] = \
                get_stage_info(active_stage_exits[stage]["next"], "start spawn id")

        # Alternate end loading zones
        if active_stage_exits[stage]["alt"]:
            loading_zone_bytes[get_stage_info(stage, "altzone map offset")] = \
                get_stage_info(active_stage_exits[stage]["alt"], "start map id")
            loading_zone_bytes[get_stage_info(stage, "altzone spawn offset")] = \
                get_stage_info(active_stage_exits[stage]["alt"], "start spawn id")

    return loading_zone_bytes


def get_start_inventory_data(player: int, options: CV64Options, precollected_items: List[Item]) -> Dict[int, bytes]:
    """Calculate and return the starting inventory values. Not every Item goes into the menu inventory, so everything
    has to be handled appropriately."""
    start_inventory_data = {}

    inventory_items_array = [0 for _ in range(35)]
    total_money = 0
    total_jewels = 0
    total_powerups = 0
    total_ice_traps = 0

    items_max = 10

    # Raise the items max if Increase Item Limit is enabled.
    if options.increase_item_limit:
        items_max = 99

    for item in precollected_items:
        if item.player != player:
            continue

        inventory_offset = get_item_info(item.name, "inventory offset")
        sub_equip_id = get_item_info(item.name, "sub equip id")
        # Starting inventory items
        if inventory_offset is not None:
            inventory_items_array[inventory_offset] += 1
            if inventory_items_array[inventory_offset] > items_max and "Special" not in item.name:
                inventory_items_array[inventory_offset] = items_max
            if item.name == iname.permaup:
                if inventory_items_array[inventory_offset] > 2:
                    inventory_items_array[inventory_offset] = 2
        # Starting sub-weapon
        elif sub_equip_id is not None:
            start_inventory_data[0xBFD883] = bytes(sub_equip_id)
        # Starting PowerUps
        elif item.name == iname.powerup:
            total_powerups += 1
            # Can't have more than 2 PowerUps.
            if total_powerups > 2:
                total_powerups = 2
        # Starting Gold
        elif "GOLD" in item.name:
            total_money += int(item.name[0:4])
            # Money cannot be higher than 99999.
            if total_money > 99999:
                total_money = 99999
        # Starting Jewels
        elif "jewel" in item.name:
            if "L" in item.name:
                total_jewels += 10
            else:
                total_jewels += 5
            # Jewels cannot be higher than 99.
            if total_jewels > 99:
                total_jewels = 99
        # Starting Ice Traps
        else:
            total_ice_traps += 1
            # Ice Traps cannot be higher than 255.
            if total_ice_traps > 0xFF:
                total_ice_traps = 0xFF

    # Convert the jewels into data.
    start_inventory_data[0xBFD867] = bytes([total_jewels])

    # Convert the Ice Traps into data.
    start_inventory_data[0xBFD88B] = bytes([total_ice_traps])

    # Convert the inventory items into data.
    start_inventory_data[0xBFE518] = bytes(inventory_items_array)

    # Convert the starting money into data.
    start_inventory_data[0xBFE514] = int.to_bytes(total_money, 4, "big")

    return start_inventory_data


def get_item_text_color(loc: Location) -> bytearray:
    if loc.item.advancement:
        return bytearray([0xA2, 0x0C])
    elif loc.item.classification == ItemClassification.useful:
        return bytearray([0xA2, 0x0A])
    elif loc.item.classification == ItemClassification.trap:
        return bytearray([0xA2, 0x0B])
    else:
        return bytearray([0xA2, 0x02])
