from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, add_item_rule
from math import ceil
from BaseClasses import ItemClassification

from .Locations import KH1Location, location_table
from .Items import KH1Item, item_table, get_items_by_type

WORLDS =    ["Wonderland", "Olympus Coliseum", "Deep Jungle", "Agrabah",      "Monstro",      "Atlantica", "Halloween Town", "Neverland",  "Hollow Bastion", "End of the World"]
KEYBLADES = ["Lady Luck",  "Olympia",          "Jungle King", "Three Wishes", "Wishing Star", "Crabclaw",  "Pumpkinhead",    "Fairy Harp", "Divine Rose",    "Oblivion"]

def has_x_worlds(state: CollectionState, player: int, num_of_worlds: int, keyblades_unlock_chests: bool) -> bool:
    worlds_acquired = 0.0
    for i in range(len(WORLDS)):
        if state.has(WORLDS[i], player):
            worlds_acquired = worlds_acquired + 0.5
        if (state.has(WORLDS[i], player) and (not keyblades_unlock_chests or state.has(KEYBLADES[i], player))) or (state.has(WORLDS[i], player) and WORLDS[i] == "Atlantica"):
            worlds_acquired = worlds_acquired + 0.5
    return worlds_acquired >= num_of_worlds

def has_emblems(state: CollectionState, player: int, keyblades_unlock_chests: bool) -> bool:
    return state.has_all({
        "Emblem Piece (Flame)",
        "Emblem Piece (Chest)",
        "Emblem Piece (Statue)",
        "Emblem Piece (Fountain)",
        "Hollow Bastion"}, player) and has_x_worlds(state, player, 5, keyblades_unlock_chests)

def has_puppies(state: CollectionState, player: int, puppies_required: int, puppy_value: int) -> bool:
    return (state.count("Puppy", player) * puppy_value) >= puppies_required

def has_all_arts(state: CollectionState, player: int) -> bool:
    return state.has_all({"Fire Arts", "Blizzard Arts", "Thunder Arts", "Cure Arts", "Gravity Arts", "Stop Arts", "Aero Arts"}, player)

def has_all_summons(state: CollectionState, player: int) -> bool:
    return state.has_all({"Simba", "Bambi", "Genie", "Dumbo", "Mushu", "Tinker Bell"}, player)

def has_all_magic_lvx(state: CollectionState, player: int, level) -> bool:
    return state.has_all_counts({
        "Progressive Fire": level,
        "Progressive Blizzard": level,
        "Progressive Thunder": level,
        "Progressive Cure": level,
        "Progressive Gravity": level,
        "Progressive Aero": level,
        "Progressive Stop": level}, player)

def has_offensive_magic(state: CollectionState, player: int) -> bool:
    return state.has_any({"Progressive Fire", "Progressive Blizzard", "Progressive Thunder", "Progressive Gravity", "Progressive Stop"}, player)

def has_lucky_emblems(state: CollectionState, player: int, required_amt: int) -> bool:
    return state.has("Lucky Emblem", player, required_amt)

def has_final_rest_door(state: CollectionState, player: int, final_rest_door_requirement: str, final_rest_door_required_lucky_emblems: int):
    if final_rest_door_requirement == "lucky_emblems":
        return state.has("Lucky Emblem", player, final_rest_door_required_lucky_emblems)
    else:
        return state.has("Final Door Key", player)

def has_defensive_tools(state: CollectionState, player: int) -> bool:
    return (
            state.has_all_counts({"Progressive Cure": 2, "Leaf Bracer": 1, "Dodge Roll": 1}, player)
            and state.has_any_count({"Second Chance": 1, "MP Rage": 1, "Progressive Aero": 2}, player)
        )

def can_dumbo_skip(state: CollectionState, player: int) -> bool:
    return (
            state.has("Dumbo", player)
            and state.has_group("Magic", player)
        )

def has_oogie_manor(state: CollectionState, player: int, advanced_logic: bool) -> bool:
    return (
                state.has("Progressive Fire", player)
                or (advanced_logic and state.has("High Jump", player, 2))
                or (advanced_logic and state.has("High Jump", player) and state.has("Progressive Glide", player))
        )

def set_rules(kh1world):
    multiworld                             = kh1world.multiworld
    player                                 = kh1world.player
    options                                = kh1world.options
    eotw_required_lucky_emblems            = kh1world.determine_lucky_emblems_required_to_open_end_of_the_world()
    final_rest_door_required_lucky_emblems = kh1world.determine_lucky_emblems_required_to_open_final_rest_door()
    final_rest_door_requirement            = kh1world.options.final_rest_door_key.current_key
    
    add_rule(kh1world.get_location("Traverse Town 1st District Candle Puzzle Chest"),
        lambda state: state.has("Progressive Blizzard", player))
    add_rule(kh1world.get_location("Traverse Town Mystical House Yellow Trinity Chest"),
        lambda state: (
            state.has("Progressive Fire", player)
            and
            (
                state.has("Yellow Trinity", player)
                or (options.advanced_logic and state.has("High Jump", player))
                or state.has("High Jump", player, 2)
            )
        ))
    add_rule(kh1world.get_location("Traverse Town Secret Waterway White Trinity Chest"),
        lambda state: state.has("White Trinity", player))
    add_rule(kh1world.get_location("Traverse Town Geppetto's House Chest"),
        lambda state: (
            state.has("Monstro", player)
            and
            (
                state.has("High Jump", player)
                or (options.advanced_logic and state.has("Progressive Glide", player))
            )
            and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
        ))
    add_rule(kh1world.get_location("Traverse Town Item Workshop Right Chest"),
        lambda state: (
            state.has("Green Trinity", player)
            or state.has("High Jump", player, 3)
            or (options.advanced_logic and state.has("High Jump", player, 2))
        ))
    add_rule(kh1world.get_location("Traverse Town 1st District Blue Trinity Balcony Chest"),
        lambda state: (
            (state.has("Blue Trinity", player) and state.has("Progressive Glide", player))
            or (options.advanced_logic and state.has("Progressive Glide", player))
        ))
    add_rule(kh1world.get_location("Traverse Town Mystical House Glide Chest"),
        lambda state: (
            (
                state.has("Progressive Glide", player)
                or
                (
                    options.advanced_logic
                    and
                    (
                        (state.has("High Jump", player) and state.has("Yellow Trinity", player))
                        or state.has("High Jump", player, 2)
                    )
                    and state.has("Combo Master", player)
                )
                or
                (
                    options.advanced_logic
                    and state.has("Mermaid Kick", player)
                )
            )
            and state.has("Progressive Fire", player)
        ))
    add_rule(kh1world.get_location("Traverse Town Alleyway Behind Crates Chest"),
        lambda state: state.has("Red Trinity", player))
    add_rule(kh1world.get_location("Traverse Town Item Workshop Left Chest"),
        lambda state: (
            state.has("Green Trinity", player)
            or state.has("High Jump", player, 3)
            or (options.advanced_logic and state.has("High Jump", player, 2))
        ))
    add_rule(kh1world.get_location("Wonderland Rabbit Hole Green Trinity Chest"),
        lambda state: state.has("Green Trinity", player))
    add_rule(kh1world.get_location("Wonderland Rabbit Hole Defeat Heartless 3 Chest"),
        lambda state: has_x_worlds(state, player, 5, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Wonderland Bizarre Room Green Trinity Chest"),
        lambda state: state.has("Green Trinity", player))
    add_rule(kh1world.get_location("Wonderland Queen's Castle Hedge Left Red Chest"),
        lambda state: (
            state.has("Footprints", player)
            or state.has("High Jump", player)
            or state.has("Progressive Glide", player)
        ))
    add_rule(kh1world.get_location("Wonderland Queen's Castle Hedge Right Blue Chest"),
        lambda state: (
            state.has("Footprints", player)
            or state.has("High Jump", player)
            or state.has("Progressive Glide", player)
        ))
    add_rule(kh1world.get_location("Wonderland Queen's Castle Hedge Right Red Chest"),
        lambda state: (
            state.has("Footprints", player)
            or state.has("High Jump", player)
            or state.has("Progressive Glide", player)
        ))
    add_rule(kh1world.get_location("Wonderland Lotus Forest Thunder Plant Chest"),
        lambda state: (
            state.has_all({
                "Progressive Thunder",
                "Footprints"}, player)
        ))
    add_rule(kh1world.get_location("Wonderland Lotus Forest Through the Painting Thunder Plant Chest"),
        lambda state: (
            state.has_all({
                "Progressive Thunder",
                "Footprints"}, player)
        ))
    add_rule(kh1world.get_location("Wonderland Lotus Forest Glide Chest"),
        lambda state: (
            state.has("Progressive Glide", player)
            or
            (
                options.advanced_logic
                and (state.has("High Jump", player) or can_dumbo_skip(state, player))
                and state.has("Footprints", player)
            )
        ))
    add_rule(kh1world.get_location("Wonderland Lotus Forest Corner Chest"),
        lambda state: (
            (
                state.has("High Jump", player)
                or state.has("Progressive Glide", player)
            )
            or options.advanced_logic
        ))
    add_rule(kh1world.get_location("Wonderland Bizarre Room Lamp Chest"),
        lambda state: state.has("Footprints", player))
    add_rule(kh1world.get_location("Wonderland Tea Party Garden Above Lotus Forest Entrance 2nd Chest"),
        lambda state: (
            state.has("Progressive Glide", player)
            or
            (
                state.has("High Jump", player, 2)
                and state.has("Footprints", player)
            )
            or
            (
                options.advanced_logic
                and state.has_all({
                    "High Jump",
                    "Footprints"}, player)
            )
        ))
    add_rule(kh1world.get_location("Wonderland Tea Party Garden Above Lotus Forest Entrance 1st Chest"),
        lambda state: (
            state.has("Progressive Glide", player)
            or
            (
                state.has("High Jump", player, 2)
                and state.has("Footprints", player)
            )
            or
            (
                options.advanced_logic
                and state.has_all({
                    "High Jump",
                    "Footprints"}, player)
            )
        ))
    add_rule(kh1world.get_location("Wonderland Tea Party Garden Bear and Clock Puzzle Chest"),
        lambda state: (
        
           state.has("Footprints", player)
           or (options.advanced_logic and state.has("Progressive Glide", player))
        ))
    add_rule(kh1world.get_location("Wonderland Tea Party Garden Across From Bizarre Room Entrance Chest"),
        lambda state: (
            state.has("Progressive Glide", player)
            or
            (
                state.has("High Jump", player, 3)
                and state.has("Footprints", player)
            )
            or
            (
                options.advanced_logic
                and 
                (
                    state.has_all({"High Jump", "Footprints", "Combo Master"}, player)
                    or (state.has("High Jump", player, 2) and state.has("Footprints", player))
                )
            )
        ))
    add_rule(kh1world.get_location("Wonderland Lotus Forest Through the Painting White Trinity Chest"),
        lambda state: (
            state.has_all({
                "White Trinity",
                "Footprints"}, player)
        ))
    add_rule(kh1world.get_location("Deep Jungle Hippo's Lagoon Right Chest"),
        lambda state: (
           state.has("High Jump", player)
           or state.has("Progressive Glide", player)
           or options.advanced_logic
        ))
    add_rule(kh1world.get_location("Deep Jungle Climbing Trees Blue Trinity Chest"),
        lambda state: state.has("Blue Trinity", player))
    add_rule(kh1world.get_location("Deep Jungle Cavern of Hearts White Trinity Chest"),
        lambda state: (
            state.has_all({
            "White Trinity",
            "Slides"}, player)
        ))
    add_rule(kh1world.get_location("Deep Jungle Camp Blue Trinity Chest"),
        lambda state: state.has("Blue Trinity", player))
    add_rule(kh1world.get_location("Deep Jungle Waterfall Cavern Low Chest"),
        lambda state: state.has("Slides", player))
    add_rule(kh1world.get_location("Deep Jungle Waterfall Cavern Middle Chest"),
        lambda state: state.has("Slides", player))
    add_rule(kh1world.get_location("Deep Jungle Waterfall Cavern High Wall Chest"),
        lambda state: state.has("Slides", player))
    add_rule(kh1world.get_location("Deep Jungle Waterfall Cavern High Middle Chest"),
        lambda state: state.has("Slides", player))
    add_rule(kh1world.get_location("Deep Jungle Tree House Suspended Boat Chest"),
        lambda state: (
           state.has("Progressive Glide", player)
           or options.advanced_logic
        ))
    add_rule(kh1world.get_location("Agrabah Main Street High Above Palace Gates Entrance Chest"),
        lambda state: (
            state.has("High Jump", player)
            or state.has("Progressive Glide", player)
            or (options.advanced_logic and can_dumbo_skip(state, player))
        ))
    add_rule(kh1world.get_location("Agrabah Palace Gates High Opposite Palace Chest"),
        lambda state: (
            state.has("High Jump", player)
            or options.advanced_logic
        ))
    add_rule(kh1world.get_location("Agrabah Palace Gates High Close to Palace Chest"),
        lambda state: (
            state.has_all({
                "High Jump",
                "Progressive Glide"}, player)
            or
            (
                options.advanced_logic
                and
                (
                    state.has("Combo Master", player)
                    or can_dumbo_skip(state, player)
                    or state.has("High Jump", player, 2)
                    or state.has("Progressive Glide", player)
                )
            )
            or state.has("High Jump", player, 3)
        ))
    add_rule(kh1world.get_location("Agrabah Storage Green Trinity Chest"),
        lambda state: state.has("Green Trinity", player))
    add_rule(kh1world.get_location("Agrabah Cave of Wonders Entrance Tall Tower Chest"),
        lambda state: (
            state.has("Progressive Glide", player)
            or (options.advanced_logic and state.has("Combo Master", player))
            or (options.advanced_logic and can_dumbo_skip(state, player))
            or state.has("High Jump", player, 2)
        ))
    add_rule(kh1world.get_location("Agrabah Cave of Wonders Bottomless Hall Pillar Chest"),
        lambda state: (
           state.has("High Jump", player)
           or state.has("Progressive Glide", player)
           or options.advanced_logic
        ))
    add_rule(kh1world.get_location("Agrabah Cave of Wonders Silent Chamber Blue Trinity Chest"),
        lambda state: state.has("Blue Trinity", player))
    add_rule(kh1world.get_location("Agrabah Cave of Wonders Hidden Room Right Chest"),
        lambda state: (
            state.has("Yellow Trinity", player)
            or state.has("High Jump", player)
            or (options.advanced_logic and state.has("Progressive Glide", player))
        ))
    add_rule(kh1world.get_location("Agrabah Cave of Wonders Hidden Room Left Chest"),
        lambda state: (
            state.has("Yellow Trinity", player)
            or state.has("High Jump", player)
            or (options.advanced_logic and state.has("Progressive Glide", player))
        ))
    add_rule(kh1world.get_location("Agrabah Cave of Wonders Entrance White Trinity Chest"),
        lambda state: state.has("White Trinity", player))
    add_rule(kh1world.get_location("Monstro Chamber 6 Other Platform Chest"),
        lambda state: (
            state.has_all({
                "High Jump",
                "Progressive Glide"}, player)
            or (options.advanced_logic and state.has("Combo Master", player))
        ))
    add_rule(kh1world.get_location("Monstro Chamber 6 Platform Near Chamber 5 Entrance Chest"),
        lambda state: (
            state.has("High Jump", player)
            or options.advanced_logic
        ))
    add_rule(kh1world.get_location("Monstro Chamber 6 Raised Area Near Chamber 1 Entrance Chest"),
        lambda state: (
            state.has_all({
                "High Jump",
                "Progressive Glide"}, player)
            or (options.advanced_logic and state.has("Combo Master", player))
        ))
    add_rule(kh1world.get_location("Halloween Town Moonlight Hill White Trinity Chest"),
        lambda state: (
            state.has_all({
                "White Trinity",
                "Forget-Me-Not"}, player)
        ))
    add_rule(kh1world.get_location("Halloween Town Bridge Under Bridge"),
        lambda state: (
            state.has_all({
                "Jack-In-The-Box",
                "Forget-Me-Not"}, player)
        ))
    add_rule(kh1world.get_location("Halloween Town Boneyard Tombstone Puzzle Chest"),
        lambda state: state.has("Forget-Me-Not", player))
    add_rule(kh1world.get_location("Halloween Town Bridge Right of Gate Chest"),
        lambda state: (
            state.has_all({
                "Jack-In-The-Box",
                "Forget-Me-Not"}, player)
            and
            (
                state.has("Progressive Glide", player)
                or options.advanced_logic
            )
        ))
    add_rule(kh1world.get_location("Halloween Town Cemetery Behind Grave Chest"),
        lambda state: (
            state.has_all({
                "Jack-In-The-Box",
                "Forget-Me-Not"}, player)
            and has_oogie_manor(state, player, options.advanced_logic)
        ))
    add_rule(kh1world.get_location("Halloween Town Cemetery By Cat Shape Chest"),
        lambda state: (
            state.has_all({
                "Jack-In-The-Box",
                "Forget-Me-Not"}, player)
            and has_oogie_manor(state, player, options.advanced_logic)
        ))
    add_rule(kh1world.get_location("Halloween Town Cemetery Between Graves Chest"),
        lambda state: (
            state.has_all({
                "Jack-In-The-Box",
                "Forget-Me-Not"}, player)
            and has_oogie_manor(state, player, options.advanced_logic)
        ))
    add_rule(kh1world.get_location("Halloween Town Oogie's Manor Lower Iron Cage Chest"),
        lambda state: (
            state.has_all({
                "Jack-In-The-Box",
                "Forget-Me-Not"}, player)
            and has_oogie_manor(state, player, options.advanced_logic)
        ))
    add_rule(kh1world.get_location("Halloween Town Oogie's Manor Upper Iron Cage Chest"),
        lambda state: (
            state.has_all({
                "Jack-In-The-Box",
                "Forget-Me-Not"}, player)
            and has_oogie_manor(state, player, options.advanced_logic)
        ))
    add_rule(kh1world.get_location("Halloween Town Oogie's Manor Hollow Chest"),
        lambda state: (
            state.has_all({
                "Jack-In-The-Box",
                "Forget-Me-Not"}, player)
            and has_oogie_manor(state, player, options.advanced_logic)
        ))
    add_rule(kh1world.get_location("Halloween Town Oogie's Manor Grounds Red Trinity Chest"),
        lambda state: (
            state.has_all({
                "Jack-In-The-Box",
                "Forget-Me-Not",
                "Red Trinity"}, player)
        ))
    add_rule(kh1world.get_location("Halloween Town Guillotine Square High Tower Chest"),
        lambda state: (
           state.has("High Jump", player)
           or (options.advanced_logic and can_dumbo_skip(state, player))
           or (options.advanced_logic and state.has("Progressive Glide", player))
        ))
    add_rule(kh1world.get_location("Halloween Town Guillotine Square Pumpkin Structure Left Chest"),
        lambda state: (
            (
                state.has("High Jump", player)
                or (options.advanced_logic and state.has("Progressive Glide", player))
            )
            and
            (
                state.has("Progressive Glide", player)
                or (options.advanced_logic and state.has("Combo Master", player))
                or state.has("High Jump", player, 2)
            )
        ))
    add_rule(kh1world.get_location("Halloween Town Oogie's Manor Entrance Steps Chest"),
        lambda state: (
            state.has_all({
                "Jack-In-The-Box",
                "Forget-Me-Not"}, player)
        ))
    add_rule(kh1world.get_location("Halloween Town Oogie's Manor Inside Entrance Chest"),
        lambda state: (
            state.has_all({
                "Jack-In-The-Box",
                "Forget-Me-Not"}, player)
        ))
    add_rule(kh1world.get_location("Halloween Town Bridge Left of Gate Chest"),
        lambda state: (
            state.has_all({
                "Jack-In-The-Box",
                "Forget-Me-Not"}, player)
            and
            (
                state.has("Progressive Glide", player)
                or state.has("High Jump", player)
                or options.advanced_logic
            )
        ))
    add_rule(kh1world.get_location("Halloween Town Cemetery By Striped Grave Chest"),
        lambda state: (
            state.has_all({
                "Jack-In-The-Box",
                "Forget-Me-Not"}, player)
            and has_oogie_manor(state, player, options.advanced_logic)
        ))
    add_rule(kh1world.get_location("Halloween Town Guillotine Square Pumpkin Structure Right Chest"),
        lambda state: (
            (
                state.has("High Jump", player)
                or (options.advanced_logic and state.has("Progressive Glide", player))
            )
            and
            (
                state.has("Progressive Glide", player)
                or (options.advanced_logic and state.has("Combo Master", player))
                or state.has("High Jump", player, 2)
            )
        ))
    add_rule(kh1world.get_location("Olympus Coliseum Coliseum Gates Right Blue Trinity Chest"),
        lambda state: state.has("Blue Trinity", player))
    add_rule(kh1world.get_location("Olympus Coliseum Coliseum Gates Left Blue Trinity Chest"),
        lambda state: state.has("Blue Trinity", player))
    add_rule(kh1world.get_location("Olympus Coliseum Coliseum Gates White Trinity Chest"),
        lambda state: state.has("White Trinity", player))
    add_rule(kh1world.get_location("Olympus Coliseum Coliseum Gates Blizzara Chest"),
        lambda state: state.has("Progressive Blizzard", player, 2))
    add_rule(kh1world.get_location("Olympus Coliseum Coliseum Gates Blizzaga Chest"),
        lambda state: state.has("Progressive Blizzard", player, 3))
    add_rule(kh1world.get_location("Monstro Mouth High Platform Boat Side Chest"),
        lambda state: (
            state.has("High Jump", player)
            or state.has("Progressive Glide", player)
        ))
    add_rule(kh1world.get_location("Monstro Mouth High Platform Across from Boat Chest"),
        lambda state: (
            state.has("High Jump", player)
            or state.has("Progressive Glide", player)
        ))
    add_rule(kh1world.get_location("Monstro Mouth Green Trinity Top of Boat Chest"),
        lambda state: (
            (
                state.has("High Jump", player)
                or state.has("Progressive Glide", player)
            )
            and state.has("Green Trinity", player)
        ))
    add_rule(kh1world.get_location("Monstro Chamber 5 Platform Chest"),
        lambda state: state.has("High Jump", player))
    add_rule(kh1world.get_location("Monstro Chamber 3 Platform Above Chamber 2 Entrance Chest"),
        lambda state: (
            state.has("High Jump", player)
            or options.advanced_logic
        ))
    add_rule(kh1world.get_location("Monstro Chamber 3 Platform Near Chamber 6 Entrance Chest"),
        lambda state: (
            state.has("High Jump", player)
            or options.advanced_logic
        ))
    add_rule(kh1world.get_location("Monstro Chamber 5 Atop Barrel Chest"),
        lambda state: (
           state.has("High Jump", player)
           or options.advanced_logic
        ))
    add_rule(kh1world.get_location("Neverland Pirate Ship Deck White Trinity Chest"),
        lambda state: (
            state.has_all({
                "White Trinity",
                "Green Trinity"}, player)
        ))
    add_rule(kh1world.get_location("Neverland Pirate Ship Crows Nest Chest"),
        lambda state: state.has("Green Trinity", player))
    add_rule(kh1world.get_location("Neverland Hold Yellow Trinity Right Blue Chest"),
        lambda state: state.has("Yellow Trinity", player))
    add_rule(kh1world.get_location("Neverland Hold Yellow Trinity Left Blue Chest"),
        lambda state: state.has("Yellow Trinity", player))
    add_rule(kh1world.get_location("Neverland Cabin Chest"),
        lambda state: state.has("Green Trinity", player))
    add_rule(kh1world.get_location("Neverland Hold Flight 1st Chest"),
        lambda state: (
           state.has("Green Trinity", player)
           or state.has("Progressive Glide", player)
           or state.has("High Jump", player, 3)
        ))
    add_rule(kh1world.get_location("Neverland Clock Tower Chest"),
        lambda state: (
            state.has("Green Trinity", player)
            and has_all_magic_lvx(state, player, 2)
            and has_defensive_tools(state, player)
        ))
    add_rule(kh1world.get_location("Neverland Hold Flight 2nd Chest"),
        lambda state: (
           state.has("Green Trinity", player)
           or state.has("Progressive Glide", player)
           or state.has("High Jump", player, 3)
        ))
    add_rule(kh1world.get_location("Neverland Hold Yellow Trinity Green Chest"),
        lambda state: state.has("Yellow Trinity", player))
    add_rule(kh1world.get_location("Neverland Captain's Cabin Chest"),
        lambda state: state.has("Green Trinity", player))
    add_rule(kh1world.get_location("Hollow Bastion Rising Falls Under Water 2nd Chest"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Hollow Bastion Rising Falls Floating Platform Near Save Chest"),
        lambda state: (
           state.has("High Jump", player)
           or state.has("Progressive Glide", player)
           or state.has("Progressive Blizzard", player)
         ))
    add_rule(kh1world.get_location("Hollow Bastion Rising Falls Floating Platform Near Bubble Chest"),
        lambda state: (
            state.has("High Jump", player)
            or state.has("Progressive Glide", player)
            or state.has("Progressive Blizzard", player)
        ))
    add_rule(kh1world.get_location("Hollow Bastion Rising Falls High Platform Chest"),
        lambda state: (
            state.has("Progressive Glide", player)
            or (state.has("Progressive Blizzard", player) and has_emblems(state, player, options.keyblades_unlock_chests))
            or (options.advanced_logic and state.has("Combo Master", player))
        ))
    add_rule(kh1world.get_location("Hollow Bastion Castle Gates Gravity Chest"),
        lambda state: (
            state.has("Progressive Gravity", player)
            and
            (
                has_emblems(state, player, options.keyblades_unlock_chests)
                or (options.advanced_logic and state.has("High Jump", player, 2) and state.has("Progressive Glide", player))
                or (options.advanced_logic and can_dumbo_skip(state, player) and state.has("Progressive Glide", player))
            )
        ))
    add_rule(kh1world.get_location("Hollow Bastion Castle Gates Freestanding Pillar Chest"),
        lambda state: (
            has_emblems(state, player, options.keyblades_unlock_chests)
            or state.has("High Jump", player, 2)
            or (options.advanced_logic and can_dumbo_skip(state, player))
        ))
    add_rule(kh1world.get_location("Hollow Bastion Castle Gates High Pillar Chest"),
        lambda state: (
            has_emblems(state, player, options.keyblades_unlock_chests)
            or state.has("High Jump", player, 2)
            or (options.advanced_logic and can_dumbo_skip(state, player))
        ))
    add_rule(kh1world.get_location("Hollow Bastion Great Crest Lower Chest"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Hollow Bastion Great Crest After Battle Platform Chest"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Hollow Bastion High Tower 2nd Gravity Chest"),
        lambda state: (
            state.has("Progressive Gravity", player)
            and has_emblems(state, player, options.keyblades_unlock_chests)
        ))
    add_rule(kh1world.get_location("Hollow Bastion High Tower 1st Gravity Chest"),
        lambda state: (
            state.has("Progressive Gravity", player)
            and has_emblems(state, player, options.keyblades_unlock_chests)
        ))
    add_rule(kh1world.get_location("Hollow Bastion High Tower Above Sliding Blocks Chest"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Hollow Bastion Lift Stop Library Node After High Tower Switch Gravity Chest"),
        lambda state: (
            state.has("Progressive Gravity", player)
            and has_emblems(state, player, options.keyblades_unlock_chests)
        ))
    add_rule(kh1world.get_location("Hollow Bastion Lift Stop Library Node Gravity Chest"),
        lambda state: state.has("Progressive Gravity", player))
    add_rule(kh1world.get_location("Hollow Bastion Lift Stop Under High Tower Sliding Blocks Chest"),
        lambda state: (
            has_emblems(state, player, options.keyblades_unlock_chests)
            and state.has_all({
                "Progressive Glide",
                "Progressive Gravity"}, player)
        ))
    add_rule(kh1world.get_location("Hollow Bastion Lift Stop Outside Library Gravity Chest"),
        lambda state: state.has("Progressive Gravity", player))
    add_rule(kh1world.get_location("Hollow Bastion Lift Stop Heartless Sigil Door Gravity Chest"),
        lambda state: (
            state.has("Progressive Gravity", player)
            and has_emblems(state, player, options.keyblades_unlock_chests)
        ))
    add_rule(kh1world.get_location("Hollow Bastion Waterway Blizzard on Bubble Chest"),
        lambda state: (
            (state.has("Progressive Blizzard", player) and state.has("High Jump", player))
            or state.has("High Jump", player, 3)
        ))
    add_rule(kh1world.get_location("Hollow Bastion Grand Hall Steps Right Side Chest"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Hollow Bastion Grand Hall Oblivion Chest"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Hollow Bastion Grand Hall Left of Gate Chest"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Hollow Bastion Entrance Hall Left of Emblem Door Chest"),
        lambda state: (
            state.has("High Jump", player)
            or
            (
                options.advanced_logic
                and can_dumbo_skip(state, player)
                and has_emblems(state, player, options.keyblades_unlock_chests)
            )
        ))
    add_rule(kh1world.get_location("Hollow Bastion Rising Falls White Trinity Chest"),
        lambda state: state.has("White Trinity", player))
    add_rule(kh1world.get_location("End of the World Giant Crevasse 5th Chest"),
        lambda state: (
            state.has("Progressive Glide", player)
            or options.advanced_logic
        ))
    add_rule(kh1world.get_location("End of the World Giant Crevasse 1st Chest"),
        lambda state: (
            state.has("High Jump", player)
            or state.has("Progressive Glide", player)
        ))
    add_rule(kh1world.get_location("End of the World Giant Crevasse 4th Chest"),
        lambda state: (
            (
                options.advanced_logic
                and 
                (
                    state.has_all({"High Jump", "Combo Master"}, player)
                    or state.has("High Jump", player, 2)
                )
            )
            or state.has("Progressive Glide", player)
        ))
    add_rule(kh1world.get_location("End of the World World Terminus Agrabah Chest"),
        lambda state: (
            state.has("High Jump", player)
            or
            (
                options.advanced_logic
                and can_dumbo_skip(state, player)
                and state.has("Progressive Glide", player)
            )
        ))
    add_rule(kh1world.get_location("Monstro Chamber 6 White Trinity Chest"),
        lambda state: state.has("White Trinity", player))
    add_rule(kh1world.get_location("Traverse Town Kairi Secret Waterway Oathkeeper Event"),
        lambda state: (
            has_emblems(state, player, options.keyblades_unlock_chests)
            and state.has("Hollow Bastion", player)
            and has_x_worlds(state, player, 5, options.keyblades_unlock_chests)
        ))
    add_rule(kh1world.get_location("Traverse Town Secret Waterway Navi Gummi Event"),
        lambda state: (
            has_emblems(state, player, options.keyblades_unlock_chests)
            and state.has("Hollow Bastion", player)
            and has_x_worlds(state, player, 5, options.keyblades_unlock_chests)
        ))
    add_rule(kh1world.get_location("Deep Jungle Defeat Sabor White Fang Event"),
        lambda state: state.has("Slides", player))
    add_rule(kh1world.get_location("Deep Jungle Defeat Clayton Cure Event"),
        lambda state: state.has("Slides", player))
    add_rule(kh1world.get_location("Deep Jungle Seal Keyhole Jungle King Event"),
        lambda state: state.has("Slides", player))
    add_rule(kh1world.get_location("Deep Jungle Seal Keyhole Red Trinity Event"),
        lambda state: state.has("Slides", player))
    add_rule(kh1world.get_location("Olympus Coliseum Defeat Cerberus Inferno Band Event"),
        lambda state: state.has("Entry Pass", player))
    add_rule(kh1world.get_location("Olympus Coliseum Cloud Sonic Blade Event"),
        lambda state: state.has("Entry Pass", player))
    add_rule(kh1world.get_location("Wonderland Defeat Trickmaster Blizzard Event"),
        lambda state: state.has("Footprints", player))
    add_rule(kh1world.get_location("Wonderland Defeat Trickmaster Ifrit's Horn Event"),
        lambda state: state.has("Footprints", player))
    add_rule(kh1world.get_location("Monstro Defeat Parasite Cage II Stop Event"),
        lambda state: (
            state.has("High Jump", player)
            or
            (
                options.advanced_logic
                and state.has("Progressive Glide", player)
            )
        ))
    add_rule(kh1world.get_location("Halloween Town Defeat Oogie Boogie Holy Circlet Event"),
        lambda state: (
            state.has_all({
                "Jack-In-The-Box",
                "Forget-Me-Not"}, player)
            and has_oogie_manor(state, player, options.advanced_logic)
        ))
    add_rule(kh1world.get_location("Halloween Town Defeat Oogie's Manor Gravity Event"),
        lambda state: (
            state.has_all({
                "Jack-In-The-Box",
                "Forget-Me-Not"}, player)
            and has_oogie_manor(state, player, options.advanced_logic)
        ))
    add_rule(kh1world.get_location("Halloween Town Seal Keyhole Pumpkinhead Event"),
        lambda state: (
            state.has_all({
                "Jack-In-The-Box",
                "Forget-Me-Not"}, player)
            and has_oogie_manor(state, player, options.advanced_logic)
        ))
    add_rule(kh1world.get_location("Neverland Defeat Anti Sora Raven's Claw Event"),
        lambda state: state.has("Green Trinity", player))
    add_rule(kh1world.get_location("Neverland Encounter Hook Cure Event"),
        lambda state: state.has("Green Trinity", player))
    add_rule(kh1world.get_location("Neverland Seal Keyhole Fairy Harp Event"),
        lambda state: state.has("Green Trinity", player))
    add_rule(kh1world.get_location("Neverland Seal Keyhole Tinker Bell Event"),
        lambda state: state.has("Green Trinity", player))
    add_rule(kh1world.get_location("Neverland Seal Keyhole Glide Event"),
        lambda state: state.has("Green Trinity", player))
    add_rule(kh1world.get_location("Neverland Seal Keyhole Navi-G Piece Event"),
        lambda state: state.has("Green Trinity", player))
    add_rule(kh1world.get_location("Neverland Defeat Captain Hook Ars Arcanum Event"),
        lambda state: state.has("Green Trinity", player))
    add_rule(kh1world.get_location("Hollow Bastion Defeat Maleficent Donald Cheer Event"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Hollow Bastion Defeat Dragon Maleficent Fireglow Event"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Hollow Bastion Defeat Riku II Ragnarok Event"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Hollow Bastion Defeat Behemoth Omega Arts Event"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Hollow Bastion Speak to Princesses Fire Event"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Traverse Town Mail Postcard 01 Event"),
        lambda state: state.has("Postcard", player))
    add_rule(kh1world.get_location("Traverse Town Mail Postcard 02 Event"),
        lambda state: state.has("Postcard", player, 2))
    add_rule(kh1world.get_location("Traverse Town Mail Postcard 03 Event"),
        lambda state: state.has("Postcard", player, 3))
    add_rule(kh1world.get_location("Traverse Town Mail Postcard 04 Event"),
        lambda state: state.has("Postcard", player, 4))
    add_rule(kh1world.get_location("Traverse Town Mail Postcard 05 Event"),
        lambda state: state.has("Postcard", player, 5))
    add_rule(kh1world.get_location("Traverse Town Mail Postcard 06 Event"),
        lambda state: state.has("Postcard", player, 6))
    add_rule(kh1world.get_location("Traverse Town Mail Postcard 07 Event"),
        lambda state: state.has("Postcard", player, 7))
    add_rule(kh1world.get_location("Traverse Town Mail Postcard 08 Event"),
        lambda state: state.has("Postcard", player, 8))
    add_rule(kh1world.get_location("Traverse Town Mail Postcard 09 Event"),
        lambda state: state.has("Postcard", player, 9))
    add_rule(kh1world.get_location("Traverse Town Mail Postcard 10 Event"),
        lambda state: state.has("Postcard", player, 10))
    add_rule(kh1world.get_location("Traverse Town Defeat Opposite Armor Aero Event"),
        lambda state: state.has("Red Trinity", player))
    add_rule(kh1world.get_location("Traverse Town Defeat Opposite Armor Navi-G Piece Event"),
        lambda state: state.has("Red Trinity", player))
    add_rule(kh1world.get_location("Hollow Bastion Speak with Aerith Ansem's Report 2"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Hollow Bastion Speak with Aerith Ansem's Report 4"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Hollow Bastion Defeat Maleficent Ansem's Report 5"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Hollow Bastion Speak with Aerith Ansem's Report 6"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Halloween Town Defeat Oogie Boogie Ansem's Report 7"),
        lambda state: (
            state.has_all({
                "Jack-In-The-Box",
                "Forget-Me-Not",
                "Progressive Fire"}, player)
        ))
    add_rule(kh1world.get_location("Neverland Defeat Hook Ansem's Report 9"),
        lambda state: state.has("Green Trinity", player))
    add_rule(kh1world.get_location("Hollow Bastion Speak with Aerith Ansem's Report 10"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Traverse Town Geppetto's House Geppetto Reward 1"),
        lambda state: (
            state.has("Monstro", player)
            and
            (
                state.has("High Jump", player)
                or (options.advanced_logic and state.has("Progressive Glide", player))
            )
            and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
        ))
    add_rule(kh1world.get_location("Traverse Town Geppetto's House Geppetto Reward 2"),
        lambda state: (
            state.has("Monstro", player)
            and
            (
                state.has("High Jump", player)
                or (options.advanced_logic and state.has("Progressive Glide", player))
            )
            and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
        ))
    add_rule(kh1world.get_location("Traverse Town Geppetto's House Geppetto Reward 3"),
        lambda state: (
            state.has("Monstro", player)
            and
            (
                state.has("High Jump", player)
                or (options.advanced_logic and state.has("Progressive Glide", player))
            )
            and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
        ))
    add_rule(kh1world.get_location("Traverse Town Geppetto's House Geppetto Reward 4"),
        lambda state: (
            state.has("Monstro", player)
            and
            (
                state.has("High Jump", player)
                or (options.advanced_logic and state.has("Progressive Glide", player))
            )
            and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
        ))
    add_rule(kh1world.get_location("Traverse Town Geppetto's House Geppetto Reward 5"),
        lambda state: (
            state.has("Monstro", player)
            and
            (
                state.has("High Jump", player)
                or (options.advanced_logic and state.has("Progressive Glide", player))
            )
            and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
        ))
    add_rule(kh1world.get_location("Traverse Town Geppetto's House Geppetto All Summons Reward"),
        lambda state: (
            state.has("Monstro", player)
            and
            (
                state.has("High Jump", player)
                or (options.advanced_logic and state.has("Progressive Glide", player))
            )
            and has_all_summons(state, player)
            and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
        ))
    add_rule(kh1world.get_location("Traverse Town Geppetto's House Talk to Pinocchio"),
        lambda state: (
            state.has("Monstro", player)
            and
            (
                state.has("High Jump", player)
                or (options.advanced_logic and state.has("Progressive Glide", player))
            )
            and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
        ))
    add_rule(kh1world.get_location("Traverse Town Magician's Study Obtained All Arts Items"),
        lambda state: (
            has_all_magic_lvx(state, player, 1)
            and has_all_arts(state, player)
            and has_x_worlds(state, player, 7, options.keyblades_unlock_chests)
        ))
    add_rule(kh1world.get_location("Traverse Town Magician's Study Obtained All LV1 Magic"),
        lambda state: has_all_magic_lvx(state, player, 1))
    add_rule(kh1world.get_location("Traverse Town Magician's Study Obtained All LV3 Magic"),
        lambda state: has_all_magic_lvx(state, player, 3))
    add_rule(kh1world.get_location("Traverse Town Piano Room Return 10 Puppies"),
        lambda state: has_puppies(state, player, 10, options.puppy_value.value))
    add_rule(kh1world.get_location("Traverse Town Piano Room Return 20 Puppies"),
        lambda state: has_puppies(state, player, 20, options.puppy_value.value))
    add_rule(kh1world.get_location("Traverse Town Piano Room Return 30 Puppies"),
        lambda state: has_puppies(state, player, 30, options.puppy_value.value))
    add_rule(kh1world.get_location("Traverse Town Piano Room Return 40 Puppies"),
        lambda state: has_puppies(state, player, 40, options.puppy_value.value))
    add_rule(kh1world.get_location("Traverse Town Piano Room Return 50 Puppies Reward 1"),
        lambda state: has_puppies(state, player, 50, options.puppy_value.value))
    add_rule(kh1world.get_location("Traverse Town Piano Room Return 50 Puppies Reward 2"),
        lambda state: has_puppies(state, player, 50, options.puppy_value.value))
    add_rule(kh1world.get_location("Traverse Town Piano Room Return 60 Puppies"),
        lambda state: has_puppies(state, player, 60, options.puppy_value.value))
    add_rule(kh1world.get_location("Traverse Town Piano Room Return 70 Puppies"),
        lambda state: has_puppies(state, player, 70, options.puppy_value.value))
    add_rule(kh1world.get_location("Traverse Town Piano Room Return 80 Puppies"),
        lambda state: has_puppies(state, player, 80, options.puppy_value.value))
    add_rule(kh1world.get_location("Traverse Town Piano Room Return 90 Puppies"),
        lambda state: has_puppies(state, player, 90, options.puppy_value.value))
    add_rule(kh1world.get_location("Traverse Town Piano Room Return 99 Puppies Reward 1"),
        lambda state: has_puppies(state, player, 99, options.puppy_value.value))
    add_rule(kh1world.get_location("Traverse Town Piano Room Return 99 Puppies Reward 2"),
        lambda state: has_puppies(state, player, 99, options.puppy_value.value))
    add_rule(kh1world.get_location("Neverland Hold Aero Chest"),
        lambda state: state.has("Yellow Trinity", player))
    add_rule(kh1world.get_location("Deep Jungle Camp Hi-Potion Experiment"),
        lambda state: state.has("Progressive Fire", player))
    add_rule(kh1world.get_location("Deep Jungle Camp Ether Experiment"),
        lambda state: state.has("Progressive Blizzard", player))
    add_rule(kh1world.get_location("Deep Jungle Camp Replication Experiment"),
        lambda state: state.has("Progressive Blizzard", player))
    add_rule(kh1world.get_location("Deep Jungle Cliff Save Gorillas"),
        lambda state: state.has("Slides", player))
    add_rule(kh1world.get_location("Deep Jungle Tree House Save Gorillas"),
        lambda state: state.has("Slides", player))
    add_rule(kh1world.get_location("Deep Jungle Camp Save Gorillas"),
        lambda state: state.has("Slides", player))
    add_rule(kh1world.get_location("Deep Jungle Bamboo Thicket Save Gorillas"),
        lambda state: state.has("Slides", player))
    add_rule(kh1world.get_location("Deep Jungle Climbing Trees Save Gorillas"),
        lambda state: state.has("Slides", player))
    add_rule(kh1world.get_location("Wonderland Bizarre Room Read Book"),
        lambda state: state.has("Footprints", player))
    add_rule(kh1world.get_location("Olympus Coliseum Coliseum Gates Green Trinity"),
        lambda state: state.has("Green Trinity", player))
    add_rule(kh1world.get_location("Olympus Coliseum Coliseum Gates Hero's License Event"),
        lambda state: state.has("Entry Pass", player))
    add_rule(kh1world.get_location("Deep Jungle Cavern of Hearts Navi-G Piece Event"),
        lambda state: state.has("Slides", player))
    add_rule(kh1world.get_location("Wonderland Bizarre Room Navi-G Piece Event"),
        lambda state: state.has("Footprints", player))
    add_rule(kh1world.get_location("Traverse Town Synth 15 Items"),
        lambda state: (
            max(state.count("Orichalcum", player),9) + max(state.count("Mythril", player),9) >= 15
            and
            (
                state.has("Green Trinity", player)
                or state.has("High Jump", player, 3)
                or (options.advanced_logic and state.has("High Jump", player, 2))
            )
        ))
    for i in range(33):
        add_rule(kh1world.get_location("Traverse Town Synth Item " + str(i+1).rjust(2,'0')),
            lambda state: (
                state.has("Orichalcum", player, 17)
                and state.has("Mythril", player, 16)
                and
                (
                    state.has("Green Trinity", player)
                    or state.has("High Jump", player, 3)
                    or (options.advanced_logic and state.has("High Jump", player, 2))
                )
            ))
    add_rule(kh1world.get_location("Traverse Town Gizmo Shop Postcard 1"),
        lambda state: state.has("Progressive Thunder", player))
    add_rule(kh1world.get_location("Traverse Town Gizmo Shop Postcard 2"),
        lambda state: state.has("Progressive Thunder", player))
    add_rule(kh1world.get_location("Traverse Town Item Workshop Postcard"),
        lambda state: (
            state.has("Green Trinity", player)
            or state.has("High Jump", player, 3)
            or (options.advanced_logic and state.has("High Jump", player, 2))
        ))
    add_rule(kh1world.get_location("Traverse Town Geppetto's House Postcard"),
        lambda state: (
            state.has("Monstro", player)
            and
            (
                state.has("High Jump", player)
                or (options.advanced_logic and state.has("Progressive Glide", player))
            )
            and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
        ))
    add_rule(kh1world.get_location("Hollow Bastion Entrance Hall Emblem Piece (Flame)"),
        lambda state: (
            (
                state.has("Theon Vol. 6", player)
                or state.has("High Jump", player, 3)
                or has_emblems(state, player, options.keyblades_unlock_chests)
                or (options.advanced_logic and state.has("High Jump", player, 2))
            )
            and state.has("Progressive Fire", player)
            and
            (
                state.has("High Jump", player)
                or state.has("Progressive Glide", player)
                or state.has("Progressive Thunder", player)
                or options.advanced_logic
            )
        ))
    add_rule(kh1world.get_location("Hollow Bastion Entrance Hall Emblem Piece (Chest)"),
        lambda state: (
            state.has("Theon Vol. 6", player)
            or state.has("High Jump", player, 3)
            or has_emblems(state, player, options.keyblades_unlock_chests)
            or (options.advanced_logic and state.has("High Jump", player, 2))
        ))
    add_rule(kh1world.get_location("Hollow Bastion Entrance Hall Emblem Piece (Statue)"),
        lambda state: (
            (
                state.has("Theon Vol. 6", player)
                or state.has("High Jump", player, 3)
                or has_emblems(state, player, options.keyblades_unlock_chests)
                or (options.advanced_logic and state.has("High Jump", player, 2))
            )
            and state.has("Red Trinity", player)
        ))
    add_rule(kh1world.get_location("Hollow Bastion Entrance Hall Emblem Piece (Fountain)"),
        lambda state: (
            state.has("Theon Vol. 6", player)
            or state.has("High Jump", player, 3)
            or has_emblems(state, player, options.keyblades_unlock_chests)
            or (options.advanced_logic and state.has("High Jump", player, 2))
        ))
    add_rule(kh1world.get_location("Hollow Bastion Library Speak to Belle Divine Rose"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Hollow Bastion Library Speak to Aerith Cure"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Traverse Town 1st District Blue Trinity by Exit Door"),
        lambda state: state.has("Blue Trinity", player))
    add_rule(kh1world.get_location("Traverse Town 3rd District Blue Trinity"),
        lambda state: state.has("Blue Trinity", player))
    add_rule(kh1world.get_location("Traverse Town Magician's Study Blue Trinity"),
        lambda state: (
            state.has_all({
                "Blue Trinity",
                "Progressive Fire"}, player)
            ))
    add_rule(kh1world.get_location("Wonderland Lotus Forest Blue Trinity in Alcove"),
        lambda state: state.has("Blue Trinity", player))
    add_rule(kh1world.get_location("Wonderland Lotus Forest Blue Trinity by Moving Boulder"),
        lambda state: (
            state.has("Blue Trinity", player)
            and state.has("Footprints", player)
            ))
    add_rule(kh1world.get_location("Agrabah Bazaar Blue Trinity"),
        lambda state: state.has("Blue Trinity", player))
    add_rule(kh1world.get_location("Monstro Mouth Blue Trinity"),
        lambda state: state.has("Blue Trinity", player))
    add_rule(kh1world.get_location("Monstro Chamber 5 Blue Trinity"),
        lambda state: state.has("Blue Trinity", player))
    add_rule(kh1world.get_location("Hollow Bastion Great Crest Blue Trinity"),
        lambda state: (
            state.has("Blue Trinity", player)
            and has_emblems(state, player, options.keyblades_unlock_chests)
        ))
    add_rule(kh1world.get_location("Hollow Bastion Dungeon Blue Trinity"),
        lambda state: state.has("Blue Trinity", player))
    add_rule(kh1world.get_location("Deep Jungle Treetop Green Trinity"),
        lambda state: state.has("Green Trinity", player))
    add_rule(kh1world.get_location("Agrabah Cave of Wonders Treasure Room Red Trinity"),
        lambda state: state.has("Red Trinity", player))
    if options.hundred_acre_wood:
        add_rule(kh1world.get_location("100 Acre Wood Bouncing Spot Left Cliff Chest"),
            lambda state: (
                state.has("Torn Page", player, 4)
                and
                (
                    state.has("High Jump", player)
                    or state.has("Progressive Glide", player)
                )
            ))
        add_rule(kh1world.get_location("100 Acre Wood Bouncing Spot Right Tree Alcove Chest"),
            lambda state: (
                state.has("Torn Page", player, 4)
                and
                (
                    state.has("High Jump", player)
                    or state.has("Progressive Glide", player)
                )
            ))
        add_rule(kh1world.get_location("100 Acre Wood Bouncing Spot Under Giant Pot Chest"),
            lambda state: state.has("Torn Page", player, 4))
        add_rule(kh1world.get_location("100 Acre Wood Bouncing Spot Turn in Rare Nut 1"),
            lambda state: state.has("Torn Page", player, 4))
        add_rule(kh1world.get_location("100 Acre Wood Bouncing Spot Turn in Rare Nut 2"),
            lambda state: (
                state.has("Torn Page", player, 4)
                and
                (
                    state.has("High Jump", player)
                    or state.has("Progressive Glide", player)
                )
            ))
        add_rule(kh1world.get_location("100 Acre Wood Bouncing Spot Turn in Rare Nut 3"),
            lambda state: (
                state.has("Torn Page", player, 4)
                and
                (
                    state.has("High Jump", player)
                    or state.has("Progressive Glide", player)
                )
            ))
        add_rule(kh1world.get_location("100 Acre Wood Bouncing Spot Turn in Rare Nut 4"),
            lambda state: (
                state.has("Torn Page", player, 4)
                and
                (
                    state.has("High Jump", player)
                    or state.has("Progressive Glide", player)
                )
            ))
        add_rule(kh1world.get_location("100 Acre Wood Bouncing Spot Turn in Rare Nut 5"),
            lambda state: (
                state.has("Torn Page", player, 4)
                and
                (
                    state.has("High Jump", player)
                    or state.has("Progressive Glide", player)
                )
            ))
        add_rule(kh1world.get_location("100 Acre Wood Pooh's House Owl Cheer"),
            lambda state: state.has("Torn Page", player, 5))
        add_rule(kh1world.get_location("100 Acre Wood Convert Torn Page 1"),
            lambda state: state.has("Torn Page", player, 1))
        add_rule(kh1world.get_location("100 Acre Wood Convert Torn Page 2"),
            lambda state: state.has("Torn Page", player, 2))
        add_rule(kh1world.get_location("100 Acre Wood Convert Torn Page 3"),
            lambda state: state.has("Torn Page", player, 3))
        add_rule(kh1world.get_location("100 Acre Wood Convert Torn Page 4"),
            lambda state: state.has("Torn Page", player, 4))
        add_rule(kh1world.get_location("100 Acre Wood Convert Torn Page 5"),
            lambda state: state.has("Torn Page", player, 5))
        add_rule(kh1world.get_location("100 Acre Wood Pooh's House Start Fire"),
            lambda state: state.has("Torn Page", player, 3))
        add_rule(kh1world.get_location("100 Acre Wood Bouncing Spot Break Log"),
            lambda state: state.has("Torn Page", player, 4))
        add_rule(kh1world.get_location("100 Acre Wood Bouncing Spot Fall Through Top of Tree Next to Pooh"),
            lambda state: (
                state.has("Torn Page", player, 4)
                and
                (
                    state.has("High Jump", player)
                    or state.has("Progressive Glide", player)
                )
            ))
    if options.atlantica:
        add_rule(kh1world.get_location("Atlantica Ursula's Lair Use Fire on Urchin Chest"),
            lambda state: (
                state.has_all({
                    "Progressive Fire",
                    "Crystal Trident"}, player)
            ))
        add_rule(kh1world.get_location("Atlantica Triton's Palace White Trinity Chest"),
            lambda state: state.has("White Trinity", player))
        add_rule(kh1world.get_location("Atlantica Defeat Ursula I Mermaid Kick Event"),
            lambda state: (
                has_offensive_magic(state, player)
                and state.has("Crystal Trident", player)
            ))
        add_rule(kh1world.get_location("Atlantica Defeat Ursula II Thunder Event"),
            lambda state: (
                state.has("Mermaid Kick", player)
                and has_offensive_magic(state, player)
                and state.has("Crystal Trident", player)
            ))
        add_rule(kh1world.get_location("Atlantica Seal Keyhole Crabclaw Event"),
            lambda state: (
                state.has("Mermaid Kick", player)
                and has_offensive_magic(state, player)
                and state.has("Crystal Trident", player)
            ))
        add_rule(kh1world.get_location("Atlantica Undersea Gorge Blizzard Clam"),
            lambda state: state.has("Progressive Blizzard", player))
        add_rule(kh1world.get_location("Atlantica Undersea Valley Fire Clam"),
            lambda state: state.has("Progressive Fire", player))
        add_rule(kh1world.get_location("Atlantica Triton's Palace Thunder Clam"),
            lambda state: state.has("Progressive Thunder", player))
        add_rule(kh1world.get_location("Atlantica Cavern Nook Clam"),
            lambda state: state.has("Crystal Trident", player))
        add_rule(kh1world.get_location("Atlantica Defeat Ursula II Ansem's Report 3"),
            lambda state: (
                state.has_all({
                    "Mermaid Kick",
                    "Crystal Trident"}, player)
                and has_offensive_magic(state, player)
            ))
    if options.cups.current_key != "off":
        if options.cups.current_key == "hades_cup":
            add_rule(kh1world.get_location("Olympus Coliseum Defeat Hades Ansem's Report 8"),
                lambda state: (
                    state.has_all({
                        "Phil Cup",
                        "Pegasus Cup",
                        "Hercules Cup",
                        "Entry Pass"}, player)
                    and has_x_worlds(state, player, 7, options.keyblades_unlock_chests)
                    and has_defensive_tools(state, player)
                ))
        add_rule(kh1world.get_location("Complete Phil Cup"),
            lambda state: (
                state.has_all({
                    "Phil Cup",
                    "Entry Pass"}, player)
            ))
        add_rule(kh1world.get_location("Complete Phil Cup Solo"),
            lambda state: (
                state.has_all({
                    "Phil Cup",
                    "Entry Pass"}, player)
            ))
        add_rule(kh1world.get_location("Complete Phil Cup Time Trial"),
            lambda state: (
                state.has_all({
                    "Phil Cup",
                    "Entry Pass"}, player)
            ))
        add_rule(kh1world.get_location("Complete Pegasus Cup"),
            lambda state: (
                state.has_all({
                    "Pegasus Cup",
                    "Entry Pass"}, player)
            ))
        add_rule(kh1world.get_location("Complete Pegasus Cup Solo"),
            lambda state: (
                state.has_all({
                    "Pegasus Cup",
                    "Entry Pass"}, player)
            ))
        add_rule(kh1world.get_location("Complete Pegasus Cup Time Trial"),
            lambda state: (
                state.has_all({
                    "Pegasus Cup",
                    "Entry Pass"}, player)
            ))
        add_rule(kh1world.get_location("Complete Hercules Cup"),
            lambda state: (
                state.has_all({
                    "Hercules Cup",
                    "Entry Pass"}, player)
                and has_x_worlds(state, player, 4, options.keyblades_unlock_chests)
            ))
        add_rule(kh1world.get_location("Complete Hercules Cup Solo"),
            lambda state: (
                state.has_all({
                    "Hercules Cup",
                    "Entry Pass"}, player)
                and has_x_worlds(state, player, 4, options.keyblades_unlock_chests)
            ))
        add_rule(kh1world.get_location("Complete Hercules Cup Time Trial"),
            lambda state: (
                state.has_all({
                    "Hercules Cup",
                    "Entry Pass"}, player)
                and has_x_worlds(state, player, 4, options.keyblades_unlock_chests)
            ))
        if options.cups.current_key == "hades_cup":
            add_rule(kh1world.get_location("Complete Hades Cup"),
                lambda state: (
                    state.has_all({
                        "Phil Cup",
                        "Pegasus Cup",
                        "Hercules Cup",
                        "Entry Pass"}, player)
                    and has_x_worlds(state, player, 7, options.keyblades_unlock_chests)
                    and has_defensive_tools(state, player)
                ))
            add_rule(kh1world.get_location("Complete Hades Cup Solo"),
                lambda state: (
                    state.has_all({
                        "Phil Cup",
                        "Pegasus Cup",
                        "Hercules Cup",
                        "Entry Pass"}, player)
                    and has_x_worlds(state, player, 7, options.keyblades_unlock_chests)
                    and has_defensive_tools(state, player)
                ))
            add_rule(kh1world.get_location("Complete Hades Cup Time Trial"),
                lambda state: (
                    state.has_all({
                        "Phil Cup",
                        "Pegasus Cup",
                        "Hercules Cup",
                        "Entry Pass"}, player)
                    and has_x_worlds(state, player, 7, options.keyblades_unlock_chests)
                    and has_defensive_tools(state, player)
                ))
            add_rule(kh1world.get_location("Hades Cup Defeat Cloud and Leon Event"),
                lambda state: (
                    state.has_all({
                        "Phil Cup",
                        "Pegasus Cup",
                        "Hercules Cup",
                        "Entry Pass"}, player)
                    and has_x_worlds(state, player, 7, options.keyblades_unlock_chests)
                    and has_defensive_tools(state, player)
                ))
            add_rule(kh1world.get_location("Hades Cup Defeat Yuffie Event"),
                lambda state: (
                    state.has_all({
                        "Phil Cup",
                        "Pegasus Cup",
                        "Hercules Cup",
                        "Entry Pass"}, player)
                    and has_x_worlds(state, player, 7, options.keyblades_unlock_chests)
                    and has_defensive_tools(state, player)
                ))
            add_rule(kh1world.get_location("Hades Cup Defeat Cerberus Event"),
                lambda state: (
                    state.has_all({
                        "Phil Cup",
                        "Pegasus Cup",
                        "Hercules Cup",
                        "Entry Pass"}, player)
                    and has_x_worlds(state, player, 7, options.keyblades_unlock_chests)
                    and has_defensive_tools(state, player)
                ))
            add_rule(kh1world.get_location("Hades Cup Defeat Behemoth Event"),
                lambda state: (
                    state.has_all({
                        "Phil Cup",
                        "Pegasus Cup",
                        "Hercules Cup",
                        "Entry Pass"}, player)
                    and has_x_worlds(state, player, 7, options.keyblades_unlock_chests)
                    and has_defensive_tools(state, player)
                ))
            add_rule(kh1world.get_location("Hades Cup Defeat Hades Event"),
                lambda state: (
                    state.has_all({
                        "Phil Cup",
                        "Pegasus Cup",
                        "Hercules Cup",
                        "Entry Pass"}, player)
                    and has_x_worlds(state, player, 7, options.keyblades_unlock_chests)
                    and has_defensive_tools(state, player)
                ))
        add_rule(kh1world.get_location("Hercules Cup Defeat Cloud Event"),
            lambda state: (
                state.has_all({
                    "Hercules Cup",
                    "Entry Pass"}, player)
                and has_x_worlds(state, player, 4, options.keyblades_unlock_chests)
            ))
        add_rule(kh1world.get_location("Hercules Cup Yellow Trinity Event"),
            lambda state: (
                state.has_all({
                    "Hercules Cup",
                    "Entry Pass"}, player)
                and has_x_worlds(state, player, 4, options.keyblades_unlock_chests)
            ))
        if options.cups.current_key == "hades_cup":
            add_rule(kh1world.get_location("Olympus Coliseum Defeat Ice Titan Diamond Dust Event"),
                lambda state: (
                    state.has_all({
                        "Phil Cup",
                        "Pegasus Cup",
                        "Hercules Cup",
                        "Entry Pass",
                        "Guard"}, player)
                    and has_x_worlds(state, player, 7, options.keyblades_unlock_chests)
                    and has_defensive_tools(state, player)
                ))
            add_rule(kh1world.get_location("Olympus Coliseum Gates Purple Jar After Defeating Hades"),
                lambda state: (
                    state.has_all({
                        "Phil Cup",
                        "Pegasus Cup",
                        "Hercules Cup",
                        "Entry Pass"}, player)
                    and has_x_worlds(state, player, 7, options.keyblades_unlock_chests)
                    and has_defensive_tools(state, player)
                ))
        add_rule(kh1world.get_location("Olympus Coliseum Olympia Chest"),
            lambda state: (
                state.has_all({
                    "Phil Cup",
                    "Pegasus Cup",
                    "Hercules Cup",
                    "Entry Pass"}, player)
                and has_x_worlds(state, player, 4, options.keyblades_unlock_chests)
            ))
    if options.super_bosses:
        add_rule(kh1world.get_location("Neverland Defeat Phantom Stop Event"),
            lambda state: (
                state.has("Green Trinity", player)
                and has_all_magic_lvx(state, player, 2)
                and has_defensive_tools(state, player)
                and has_emblems(state, player, options.keyblades_unlock_chests)
            ))
        add_rule(kh1world.get_location("Agrabah Defeat Kurt Zisa Ansem's Report 11"),
            lambda state: (
                has_emblems(state, player, options.keyblades_unlock_chests)
                and has_x_worlds(state, player, 7, options.keyblades_unlock_chests)
                and has_defensive_tools(state, player)
                and state.has("Progressive Blizzard", player, 3)
            ))
        add_rule(kh1world.get_location("Agrabah Defeat Kurt Zisa Zantetsuken Event"),
            lambda state: (
                has_emblems(state, player, options.keyblades_unlock_chests) and has_x_worlds(state, player, 7, options.keyblades_unlock_chests) and has_defensive_tools(state, player) and state.has("Progressive Blizzard", player, 3)
            ))
    if options.super_bosses or options.final_rest_door_key.current_key == "sephiroth":
        add_rule(kh1world.get_location("Olympus Coliseum Defeat Sephiroth Ansem's Report 12"),
            lambda state: (
                state.has_all({
                    "Phil Cup",
                    "Pegasus Cup",
                    "Hercules Cup",
                    "Entry Pass"}, player)
                and has_x_worlds(state, player, 7, options.keyblades_unlock_chests)
                and has_defensive_tools(state, player)
            ))
        add_rule(kh1world.get_location("Olympus Coliseum Defeat Sephiroth One-Winged Angel Event"),
            lambda state: (
                state.has_all({
                    "Phil Cup",
                    "Pegasus Cup",
                    "Hercules Cup",
                    "Entry Pass"}, player)
                and has_x_worlds(state, player, 7, options.keyblades_unlock_chests)
                and has_defensive_tools(state, player)
            ))
    if options.super_bosses or options.final_rest_door_key.current_key == "unknown":
        add_rule(kh1world.get_location("Hollow Bastion Defeat Unknown Ansem's Report 13"),
            lambda state: (
                has_emblems(state, player, options.keyblades_unlock_chests)
                and has_x_worlds(state, player, 7, options.keyblades_unlock_chests)
                and has_defensive_tools(state, player)
            ))
        add_rule(kh1world.get_location("Hollow Bastion Defeat Unknown EXP Necklace Event"),
            lambda state: (
                has_emblems(state, player, options.keyblades_unlock_chests) and has_x_worlds(state, player, 7, options.keyblades_unlock_chests)
                and has_defensive_tools(state, player)
            ))
    if options.jungle_slider:
        add_rule(kh1world.get_location("Deep Jungle Jungle Slider 10 Fruits"),
            lambda state: state.has("Slides", player))
        add_rule(kh1world.get_location("Deep Jungle Jungle Slider 20 Fruits"),
            lambda state: state.has("Slides", player))
        add_rule(kh1world.get_location("Deep Jungle Jungle Slider 30 Fruits"),
            lambda state: state.has("Slides", player))
        add_rule(kh1world.get_location("Deep Jungle Jungle Slider 40 Fruits"),
            lambda state: state.has("Slides", player))
        add_rule(kh1world.get_location("Deep Jungle Jungle Slider 50 Fruits"),
            lambda state: state.has("Slides", player))
    for i in range(1,options.level_checks+1):
        add_rule(kh1world.get_location("Level " + str(i+1).rjust(3,'0') + " (Slot 1)"),
            lambda state, level_num=i: (
                has_x_worlds(state, player, min(((level_num//10)*2), 8), options.keyblades_unlock_chests)
            ))
        if i+1 in kh1world.get_slot_2_levels():
            add_rule(kh1world.get_location("Level " + str(i+1).rjust(3,'0') + " (Slot 2)"),
                lambda state, level_num=i: (
                    has_x_worlds(state, player, min(((level_num//10)*2), 8), options.keyblades_unlock_chests)
                ))
            if i+1 >= options.force_stats_and_abilities_on_levels.value:
                add_item_rule(kh1world.get_location("Level " + str(i+1).rjust(3,'0') + " (Slot 2)"),
                    lambda i: (i.player == player and (i.name not in get_items_by_type("Item").keys() and i.name not in get_items_by_type("Shared Ability").keys())))
    add_rule(kh1world.get_location("Final Ansem"),
        lambda state: (
            has_final_rest_door(state, player, final_rest_door_requirement, final_rest_door_required_lucky_emblems)
        ))
    if options.keyblades_unlock_chests:
        add_rule(kh1world.get_location("Traverse Town 1st District Candle Puzzle Chest"),
            lambda state: state.has("Lionheart", player))
        add_rule(kh1world.get_location("Traverse Town 1st District Accessory Shop Roof Chest"),
            lambda state: state.has("Lionheart", player))
        add_rule(kh1world.get_location("Traverse Town 2nd District Boots and Shoes Awning Chest"),
            lambda state: state.has("Lionheart", player))
        add_rule(kh1world.get_location("Traverse Town 2nd District Rooftop Chest"),
            lambda state: state.has("Lionheart", player))
        add_rule(kh1world.get_location("Traverse Town 2nd District Gizmo Shop Facade Chest"),
            lambda state: state.has("Lionheart", player))
        add_rule(kh1world.get_location("Traverse Town Alleyway Balcony Chest"),
            lambda state: state.has("Lionheart", player))
        add_rule(kh1world.get_location("Traverse Town Alleyway Blue Room Awning Chest"),
            lambda state: state.has("Lionheart", player))
        add_rule(kh1world.get_location("Traverse Town Alleyway Corner Chest"),
            lambda state: state.has("Lionheart", player))
        add_rule(kh1world.get_location("Traverse Town Green Room Clock Puzzle Chest"),
            lambda state: state.has("Lionheart", player))
        add_rule(kh1world.get_location("Traverse Town Green Room Table Chest"),
            lambda state: state.has("Lionheart", player))
        add_rule(kh1world.get_location("Traverse Town Red Room Chest"),
            lambda state: state.has("Lionheart", player))
        add_rule(kh1world.get_location("Traverse Town Mystical House Yellow Trinity Chest"),
            lambda state: state.has("Lionheart", player))
        add_rule(kh1world.get_location("Traverse Town Accessory Shop Chest"),
            lambda state: state.has("Lionheart", player))
        add_rule(kh1world.get_location("Traverse Town Secret Waterway White Trinity Chest"),
            lambda state: state.has("Lionheart", player))
        add_rule(kh1world.get_location("Traverse Town Geppetto's House Chest"),
            lambda state: state.has("Lionheart", player))
        add_rule(kh1world.get_location("Traverse Town Item Workshop Right Chest"),
            lambda state: state.has("Lionheart", player))
        add_rule(kh1world.get_location("Traverse Town 1st District Blue Trinity Balcony Chest"),
            lambda state: state.has("Lionheart", player))
        add_rule(kh1world.get_location("Traverse Town Mystical House Glide Chest"),
            lambda state: state.has("Lionheart", player))
        add_rule(kh1world.get_location("Traverse Town Alleyway Behind Crates Chest"),
            lambda state: state.has("Lionheart", player))
        add_rule(kh1world.get_location("Traverse Town Item Workshop Left Chest"),
            lambda state: state.has("Lionheart", player))
        add_rule(kh1world.get_location("Traverse Town Secret Waterway Near Stairs Chest"),
            lambda state: state.has("Lionheart", player))
        add_rule(kh1world.get_location("Wonderland Rabbit Hole Green Trinity Chest"),
            lambda state: state.has("Lady Luck", player))
        add_rule(kh1world.get_location("Wonderland Rabbit Hole Defeat Heartless 1 Chest"),
            lambda state: state.has("Lady Luck", player))
        add_rule(kh1world.get_location("Wonderland Rabbit Hole Defeat Heartless 2 Chest"),
            lambda state: state.has("Lady Luck", player))
        add_rule(kh1world.get_location("Wonderland Rabbit Hole Defeat Heartless 3 Chest"),
            lambda state: state.has("Lady Luck", player))
        add_rule(kh1world.get_location("Wonderland Bizarre Room Green Trinity Chest"),
            lambda state: state.has("Lady Luck", player))
        add_rule(kh1world.get_location("Wonderland Queen's Castle Hedge Left Red Chest"),
            lambda state: state.has("Lady Luck", player))
        add_rule(kh1world.get_location("Wonderland Queen's Castle Hedge Right Blue Chest"),
            lambda state: state.has("Lady Luck", player))
        add_rule(kh1world.get_location("Wonderland Queen's Castle Hedge Right Red Chest"),
            lambda state: state.has("Lady Luck", player))
        add_rule(kh1world.get_location("Wonderland Lotus Forest Thunder Plant Chest"),
            lambda state: state.has("Lady Luck", player))
        add_rule(kh1world.get_location("Wonderland Lotus Forest Through the Painting Thunder Plant Chest"),
            lambda state: state.has("Lady Luck", player))
        add_rule(kh1world.get_location("Wonderland Lotus Forest Glide Chest"),
            lambda state: state.has("Lady Luck", player))
        add_rule(kh1world.get_location("Wonderland Lotus Forest Nut Chest"),
            lambda state: state.has("Lady Luck", player))
        add_rule(kh1world.get_location("Wonderland Lotus Forest Corner Chest"),
            lambda state: state.has("Lady Luck", player))
        add_rule(kh1world.get_location("Wonderland Bizarre Room Lamp Chest"),
            lambda state: state.has("Lady Luck", player))
        add_rule(kh1world.get_location("Wonderland Tea Party Garden Above Lotus Forest Entrance 2nd Chest"),
            lambda state: state.has("Lady Luck", player))
        add_rule(kh1world.get_location("Wonderland Tea Party Garden Above Lotus Forest Entrance 1st Chest"),
            lambda state: state.has("Lady Luck", player))
        add_rule(kh1world.get_location("Wonderland Tea Party Garden Bear and Clock Puzzle Chest"),
            lambda state: state.has("Lady Luck", player))
        add_rule(kh1world.get_location("Wonderland Tea Party Garden Across From Bizarre Room Entrance Chest"),
            lambda state: state.has("Lady Luck", player))
        add_rule(kh1world.get_location("Wonderland Lotus Forest Through the Painting White Trinity Chest"),
            lambda state: state.has("Lady Luck", player))
        add_rule(kh1world.get_location("Deep Jungle Tree House Beneath Tree House Chest"),
            lambda state: state.has("Jungle King", player))
        add_rule(kh1world.get_location("Deep Jungle Tree House Rooftop Chest"),
            lambda state: state.has("Jungle King", player))
        add_rule(kh1world.get_location("Deep Jungle Hippo's Lagoon Center Chest"),
            lambda state: state.has("Jungle King", player))
        add_rule(kh1world.get_location("Deep Jungle Hippo's Lagoon Left Chest"),
            lambda state: state.has("Jungle King", player))
        add_rule(kh1world.get_location("Deep Jungle Hippo's Lagoon Right Chest"),
            lambda state: state.has("Jungle King", player))
        add_rule(kh1world.get_location("Deep Jungle Vines Chest"),
            lambda state: state.has("Jungle King", player))
        add_rule(kh1world.get_location("Deep Jungle Vines 2 Chest"),
            lambda state: state.has("Jungle King", player))
        add_rule(kh1world.get_location("Deep Jungle Climbing Trees Blue Trinity Chest"),
            lambda state: state.has("Jungle King", player))
        add_rule(kh1world.get_location("Deep Jungle Tunnel Chest"),
            lambda state: state.has("Jungle King", player))
        add_rule(kh1world.get_location("Deep Jungle Cavern of Hearts White Trinity Chest"),
            lambda state: state.has("Jungle King", player))
        add_rule(kh1world.get_location("Deep Jungle Camp Blue Trinity Chest"),
            lambda state: state.has("Jungle King", player))
        add_rule(kh1world.get_location("Deep Jungle Tent Chest"),
            lambda state: state.has("Jungle King", player))
        add_rule(kh1world.get_location("Deep Jungle Waterfall Cavern Low Chest"),
            lambda state: state.has("Jungle King", player))
        add_rule(kh1world.get_location("Deep Jungle Waterfall Cavern Middle Chest"),
            lambda state: state.has("Jungle King", player))
        add_rule(kh1world.get_location("Deep Jungle Waterfall Cavern High Wall Chest"),
            lambda state: state.has("Jungle King", player))
        add_rule(kh1world.get_location("Deep Jungle Waterfall Cavern High Middle Chest"),
            lambda state: state.has("Jungle King", player))
        add_rule(kh1world.get_location("Deep Jungle Cliff Right Cliff Left Chest"),
            lambda state: state.has("Jungle King", player))
        add_rule(kh1world.get_location("Deep Jungle Cliff Right Cliff Right Chest"),
            lambda state: state.has("Jungle King", player))
        add_rule(kh1world.get_location("Deep Jungle Tree House Suspended Boat Chest"),
            lambda state: state.has("Jungle King", player))
        add_rule(kh1world.get_location("Agrabah Plaza By Storage Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Plaza Raised Terrace Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Plaza Top Corner Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Alley Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Bazaar Across Windows Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Bazaar High Corner Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Main Street Right Palace Entrance Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Main Street High Above Alley Entrance Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Main Street High Above Palace Gates Entrance Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Palace Gates Low Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Palace Gates High Opposite Palace Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Palace Gates High Close to Palace Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Storage Green Trinity Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Storage Behind Barrel Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Cave of Wonders Entrance Left Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Cave of Wonders Entrance Tall Tower Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Cave of Wonders Hall High Left Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Cave of Wonders Hall Near Bottomless Hall Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Cave of Wonders Bottomless Hall Raised Platform Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Cave of Wonders Bottomless Hall Pillar Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Cave of Wonders Bottomless Hall Across Chasm Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Cave of Wonders Treasure Room Across Platforms Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Cave of Wonders Treasure Room Small Treasure Pile Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Cave of Wonders Treasure Room Large Treasure Pile Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Cave of Wonders Treasure Room Above Fire Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Cave of Wonders Relic Chamber Jump from Stairs Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Cave of Wonders Relic Chamber Stairs Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Cave of Wonders Dark Chamber Abu Gem Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Cave of Wonders Dark Chamber Across from Relic Chamber Entrance Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Cave of Wonders Dark Chamber Bridge Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Cave of Wonders Dark Chamber Near Save Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Cave of Wonders Silent Chamber Blue Trinity Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Cave of Wonders Hidden Room Right Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Cave of Wonders Hidden Room Left Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Aladdin's House Main Street Entrance Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Aladdin's House Plaza Entrance Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Agrabah Cave of Wonders Entrance White Trinity Chest"),
            lambda state: state.has("Three Wishes", player))
        add_rule(kh1world.get_location("Monstro Chamber 6 Other Platform Chest"),
            lambda state: state.has("Wishing Star", player))
        add_rule(kh1world.get_location("Monstro Chamber 6 Platform Near Chamber 5 Entrance Chest"),
            lambda state: state.has("Wishing Star", player))
        add_rule(kh1world.get_location("Monstro Chamber 6 Raised Area Near Chamber 1 Entrance Chest"),
            lambda state: state.has("Wishing Star", player))
        add_rule(kh1world.get_location("Monstro Chamber 6 Low Chest"),
            lambda state: state.has("Wishing Star", player))
        add_rule(kh1world.get_location("Halloween Town Moonlight Hill White Trinity Chest"),
            lambda state: state.has("Pumpkinhead", player))
        add_rule(kh1world.get_location("Halloween Town Bridge Under Bridge"),
            lambda state: state.has("Pumpkinhead", player))
        add_rule(kh1world.get_location("Halloween Town Boneyard Tombstone Puzzle Chest"),
            lambda state: state.has("Pumpkinhead", player))
        add_rule(kh1world.get_location("Halloween Town Bridge Right of Gate Chest"),
            lambda state: state.has("Pumpkinhead", player))
        add_rule(kh1world.get_location("Halloween Town Cemetery Behind Grave Chest"),
            lambda state: state.has("Pumpkinhead", player))
        add_rule(kh1world.get_location("Halloween Town Cemetery By Cat Shape Chest"),
            lambda state: state.has("Pumpkinhead", player))
        add_rule(kh1world.get_location("Halloween Town Cemetery Between Graves Chest"),
            lambda state: state.has("Pumpkinhead", player))
        add_rule(kh1world.get_location("Halloween Town Oogie's Manor Lower Iron Cage Chest"),
            lambda state: state.has("Pumpkinhead", player))
        add_rule(kh1world.get_location("Halloween Town Oogie's Manor Upper Iron Cage Chest"),
            lambda state: state.has("Pumpkinhead", player))
        add_rule(kh1world.get_location("Halloween Town Oogie's Manor Hollow Chest"),
            lambda state: state.has("Pumpkinhead", player))
        add_rule(kh1world.get_location("Halloween Town Oogie's Manor Grounds Red Trinity Chest"),
            lambda state: state.has("Pumpkinhead", player))
        add_rule(kh1world.get_location("Halloween Town Guillotine Square High Tower Chest"),
            lambda state: state.has("Pumpkinhead", player))
        add_rule(kh1world.get_location("Halloween Town Guillotine Square Pumpkin Structure Left Chest"),
            lambda state: state.has("Pumpkinhead", player))
        add_rule(kh1world.get_location("Halloween Town Oogie's Manor Entrance Steps Chest"),
            lambda state: state.has("Pumpkinhead", player))
        add_rule(kh1world.get_location("Halloween Town Oogie's Manor Inside Entrance Chest"),
            lambda state: state.has("Pumpkinhead", player))
        add_rule(kh1world.get_location("Halloween Town Bridge Left of Gate Chest"),
            lambda state: state.has("Pumpkinhead", player))
        add_rule(kh1world.get_location("Halloween Town Cemetery By Striped Grave Chest"),
            lambda state: state.has("Pumpkinhead", player))
        add_rule(kh1world.get_location("Halloween Town Guillotine Square Under Jack's House Stairs Chest"),
            lambda state: state.has("Pumpkinhead", player))
        add_rule(kh1world.get_location("Halloween Town Guillotine Square Pumpkin Structure Right Chest"),
            lambda state: state.has("Pumpkinhead", player))
        add_rule(kh1world.get_location("Olympus Coliseum Coliseum Gates Left Behind Columns Chest"),
            lambda state: state.has("Olympia", player))
        add_rule(kh1world.get_location("Olympus Coliseum Coliseum Gates Right Blue Trinity Chest"),
            lambda state: state.has("Olympia", player))
        add_rule(kh1world.get_location("Olympus Coliseum Coliseum Gates Left Blue Trinity Chest"),
            lambda state: state.has("Olympia", player))
        add_rule(kh1world.get_location("Olympus Coliseum Coliseum Gates White Trinity Chest"),
            lambda state: state.has("Olympia", player))
        add_rule(kh1world.get_location("Olympus Coliseum Coliseum Gates Blizzara Chest"),
            lambda state: state.has("Olympia", player))
        add_rule(kh1world.get_location("Olympus Coliseum Coliseum Gates Blizzaga Chest"),
            lambda state: state.has("Olympia", player))
        add_rule(kh1world.get_location("Monstro Mouth Boat Deck Chest"),
            lambda state: state.has("Wishing Star", player))
        add_rule(kh1world.get_location("Monstro Mouth High Platform Boat Side Chest"),
            lambda state: state.has("Wishing Star", player))
        add_rule(kh1world.get_location("Monstro Mouth High Platform Across from Boat Chest"),
            lambda state: state.has("Wishing Star", player))
        add_rule(kh1world.get_location("Monstro Mouth Near Ship Chest"),
            lambda state: state.has("Wishing Star", player))
        add_rule(kh1world.get_location("Monstro Mouth Green Trinity Top of Boat Chest"),
            lambda state: state.has("Wishing Star", player))
        add_rule(kh1world.get_location("Monstro Chamber 2 Ground Chest"),
            lambda state: state.has("Wishing Star", player))
        add_rule(kh1world.get_location("Monstro Chamber 2 Platform Chest"),
            lambda state: state.has("Wishing Star", player))
        add_rule(kh1world.get_location("Monstro Chamber 5 Platform Chest"),
            lambda state: state.has("Wishing Star", player))
        add_rule(kh1world.get_location("Monstro Chamber 3 Ground Chest"),
            lambda state: state.has("Wishing Star", player))
        add_rule(kh1world.get_location("Monstro Chamber 3 Platform Above Chamber 2 Entrance Chest"),
            lambda state: state.has("Wishing Star", player))
        add_rule(kh1world.get_location("Monstro Chamber 3 Near Chamber 6 Entrance Chest"),
            lambda state: state.has("Wishing Star", player))
        add_rule(kh1world.get_location("Monstro Chamber 3 Platform Near Chamber 6 Entrance Chest"),
            lambda state: state.has("Wishing Star", player))
        add_rule(kh1world.get_location("Monstro Mouth High Platform Near Teeth Chest"),
            lambda state: state.has("Wishing Star", player))
        add_rule(kh1world.get_location("Monstro Chamber 5 Atop Barrel Chest"),
            lambda state: state.has("Wishing Star", player))
        add_rule(kh1world.get_location("Monstro Chamber 5 Low 2nd Chest"),
            lambda state: state.has("Wishing Star", player))
        add_rule(kh1world.get_location("Monstro Chamber 5 Low 1st Chest"),
            lambda state: state.has("Wishing Star", player))
        add_rule(kh1world.get_location("Neverland Pirate Ship Deck White Trinity Chest"),
            lambda state: state.has("Fairy Harp", player))
        add_rule(kh1world.get_location("Neverland Pirate Ship Crows Nest Chest"),
            lambda state: state.has("Fairy Harp", player))
        add_rule(kh1world.get_location("Neverland Hold Yellow Trinity Right Blue Chest"),
            lambda state: state.has("Fairy Harp", player))
        add_rule(kh1world.get_location("Neverland Hold Yellow Trinity Left Blue Chest"),
            lambda state: state.has("Fairy Harp", player))
        add_rule(kh1world.get_location("Neverland Galley Chest"),
            lambda state: state.has("Fairy Harp", player))
        add_rule(kh1world.get_location("Neverland Cabin Chest"),
            lambda state: state.has("Fairy Harp", player))
        add_rule(kh1world.get_location("Neverland Hold Flight 1st Chest"),
            lambda state: state.has("Fairy Harp", player))
        add_rule(kh1world.get_location("Neverland Clock Tower Chest"),
            lambda state: state.has("Fairy Harp", player))
        add_rule(kh1world.get_location("Neverland Hold Flight 2nd Chest"),
            lambda state: state.has("Fairy Harp", player))
        add_rule(kh1world.get_location("Neverland Hold Yellow Trinity Green Chest"),
            lambda state: state.has("Fairy Harp", player))
        add_rule(kh1world.get_location("Neverland Captain's Cabin Chest"),
            lambda state: state.has("Fairy Harp", player))
        add_rule(kh1world.get_location("Hollow Bastion Rising Falls Water's Surface Chest"),
            lambda state: state.has("Divine Rose", player))
        add_rule(kh1world.get_location("Hollow Bastion Rising Falls Under Water 1st Chest"),
            lambda state: state.has("Divine Rose", player))
        add_rule(kh1world.get_location("Hollow Bastion Rising Falls Under Water 2nd Chest"),
            lambda state: state.has("Divine Rose", player))
        add_rule(kh1world.get_location("Hollow Bastion Rising Falls Floating Platform Near Save Chest"),
            lambda state: state.has("Divine Rose", player))
        add_rule(kh1world.get_location("Hollow Bastion Rising Falls Floating Platform Near Bubble Chest"),
            lambda state: state.has("Divine Rose", player))
        add_rule(kh1world.get_location("Hollow Bastion Rising Falls High Platform Chest"),
            lambda state: state.has("Divine Rose", player))
        add_rule(kh1world.get_location("Hollow Bastion Castle Gates Gravity Chest"),
            lambda state: state.has("Divine Rose", player))
        add_rule(kh1world.get_location("Hollow Bastion Castle Gates Freestanding Pillar Chest"),
            lambda state: state.has("Divine Rose", player))
        add_rule(kh1world.get_location("Hollow Bastion Castle Gates High Pillar Chest"),
            lambda state: state.has("Divine Rose", player))
        add_rule(kh1world.get_location("Hollow Bastion Great Crest Lower Chest"),
            lambda state: state.has("Divine Rose", player))
        add_rule(kh1world.get_location("Hollow Bastion Great Crest After Battle Platform Chest"),
            lambda state: state.has("Divine Rose", player))
        add_rule(kh1world.get_location("Hollow Bastion High Tower 2nd Gravity Chest"),
            lambda state: state.has("Divine Rose", player))
        add_rule(kh1world.get_location("Hollow Bastion High Tower 1st Gravity Chest"),
            lambda state: state.has("Divine Rose", player))
        add_rule(kh1world.get_location("Hollow Bastion High Tower Above Sliding Blocks Chest"),
            lambda state: state.has("Divine Rose", player))
        add_rule(kh1world.get_location("Hollow Bastion Library Top of Bookshelf Chest"),
            lambda state: state.has("Divine Rose", player))
        add_rule(kh1world.get_location("Hollow Bastion Lift Stop Library Node After High Tower Switch Gravity Chest"),
            lambda state: state.has("Divine Rose", player))
        add_rule(kh1world.get_location("Hollow Bastion Lift Stop Library Node Gravity Chest"),
            lambda state: state.has("Divine Rose", player))
        add_rule(kh1world.get_location("Hollow Bastion Lift Stop Under High Tower Sliding Blocks Chest"),
            lambda state: state.has("Divine Rose", player))
        add_rule(kh1world.get_location("Hollow Bastion Lift Stop Outside Library Gravity Chest"),
            lambda state: state.has("Divine Rose", player))
        add_rule(kh1world.get_location("Hollow Bastion Lift Stop Heartless Sigil Door Gravity Chest"),
            lambda state: state.has("Divine Rose", player))
        add_rule(kh1world.get_location("Hollow Bastion Base Level Bubble Under the Wall Platform Chest"),
            lambda state: state.has("Divine Rose", player))
        add_rule(kh1world.get_location("Hollow Bastion Base Level Platform Near Entrance Chest"),
            lambda state: state.has("Divine Rose", player))
        add_rule(kh1world.get_location("Hollow Bastion Base Level Near Crystal Switch Chest"),
            lambda state: state.has("Divine Rose", player))
        add_rule(kh1world.get_location("Hollow Bastion Waterway Near Save Chest"),
            lambda state: state.has("Divine Rose", player))
        add_rule(kh1world.get_location("Hollow Bastion Waterway Blizzard on Bubble Chest"),
            lambda state: state.has("Divine Rose", player))
        add_rule(kh1world.get_location("Hollow Bastion Waterway Unlock Passage from Base Level Chest"),
            lambda state: state.has("Divine Rose", player))
        add_rule(kh1world.get_location("Hollow Bastion Dungeon By Candles Chest"),
            lambda state: state.has("Divine Rose", player))
        add_rule(kh1world.get_location("Hollow Bastion Dungeon Corner Chest"),
            lambda state: state.has("Divine Rose", player))
        add_rule(kh1world.get_location("Hollow Bastion Grand Hall Steps Right Side Chest"),
            lambda state: state.has("Divine Rose", player))
        add_rule(kh1world.get_location("Hollow Bastion Grand Hall Oblivion Chest"),
            lambda state: state.has("Divine Rose", player))
        add_rule(kh1world.get_location("Hollow Bastion Grand Hall Left of Gate Chest"),
            lambda state: state.has("Divine Rose", player))
        add_rule(kh1world.get_location("Hollow Bastion Entrance Hall Left of Emblem Door Chest"),
            lambda state: state.has("Divine Rose", player))
        add_rule(kh1world.get_location("Hollow Bastion Rising Falls White Trinity Chest"),
            lambda state: state.has("Divine Rose", player))
        add_rule(kh1world.get_location("End of the World Final Dimension 1st Chest"),
            lambda state: state.has("Oblivion", player))
        add_rule(kh1world.get_location("End of the World Final Dimension 2nd Chest"),
            lambda state: state.has("Oblivion", player) or options.advanced_logic)
        add_rule(kh1world.get_location("End of the World Final Dimension 3rd Chest"),
            lambda state: state.has("Oblivion", player))
        add_rule(kh1world.get_location("End of the World Final Dimension 4th Chest"),
            lambda state: state.has("Oblivion", player) or options.advanced_logic)
        add_rule(kh1world.get_location("End of the World Final Dimension 5th Chest"),
            lambda state: state.has("Oblivion", player))
        add_rule(kh1world.get_location("End of the World Final Dimension 6th Chest"),
            lambda state: state.has("Oblivion", player))
        add_rule(kh1world.get_location("End of the World Final Dimension 10th Chest"),
            lambda state: state.has("Oblivion", player) or options.advanced_logic)
        add_rule(kh1world.get_location("End of the World Final Dimension 9th Chest"),
            lambda state: state.has("Oblivion", player))
        add_rule(kh1world.get_location("End of the World Final Dimension 8th Chest"),
            lambda state: state.has("Oblivion", player) or options.advanced_logic)
        add_rule(kh1world.get_location("End of the World Final Dimension 7th Chest"),
            lambda state: state.has("Oblivion", player) or options.advanced_logic)
        add_rule(kh1world.get_location("End of the World Giant Crevasse 3rd Chest"),
            lambda state: state.has("Oblivion", player))
        add_rule(kh1world.get_location("End of the World Giant Crevasse 5th Chest"),
            lambda state: state.has("Oblivion", player))
        add_rule(kh1world.get_location("End of the World Giant Crevasse 1st Chest"),
            lambda state: state.has("Oblivion", player))
        add_rule(kh1world.get_location("End of the World Giant Crevasse 4th Chest"),
            lambda state: state.has("Oblivion", player))
        add_rule(kh1world.get_location("End of the World Giant Crevasse 2nd Chest"),
            lambda state: state.has("Oblivion", player))
        add_rule(kh1world.get_location("End of the World World Terminus Traverse Town Chest"),
            lambda state: state.has("Oblivion", player))
        add_rule(kh1world.get_location("End of the World World Terminus Wonderland Chest"),
            lambda state: state.has("Oblivion", player))
        add_rule(kh1world.get_location("End of the World World Terminus Olympus Coliseum Chest"),
            lambda state: state.has("Oblivion", player))
        add_rule(kh1world.get_location("End of the World World Terminus Deep Jungle Chest"),
            lambda state: state.has("Oblivion", player))
        add_rule(kh1world.get_location("End of the World World Terminus Agrabah Chest"),
            lambda state: state.has("Oblivion", player))
        add_rule(kh1world.get_location("End of the World World Terminus Halloween Town Chest"),
            lambda state: state.has("Oblivion", player))
        add_rule(kh1world.get_location("End of the World World Terminus Neverland Chest"),
            lambda state: state.has("Oblivion", player))
        add_rule(kh1world.get_location("End of the World World Terminus 100 Acre Wood Chest"),
            lambda state: state.has("Oblivion", player))
        add_rule(kh1world.get_location("End of the World Final Rest Chest"),
            lambda state: state.has("Oblivion", player))
        add_rule(kh1world.get_location("Monstro Chamber 6 White Trinity Chest"),
            lambda state: state.has("Wishing Star", player))
        add_rule(kh1world.get_location("Neverland Hold Aero Chest"),
            lambda state: state.has("Fairy Harp", player) or options.advanced_logic)
        add_rule(kh1world.get_location("Hollow Bastion Library 1st Floor Turn the Carousel Chest"),
            lambda state: state.has("Divine Rose", player) or options.advanced_logic)
        add_rule(kh1world.get_location("Hollow Bastion Library Top of Bookshelf Turn the Carousel Chest"),
            lambda state: state.has("Divine Rose", player) or options.advanced_logic)
        add_rule(kh1world.get_location("Hollow Bastion Library 2nd Floor Turn the Carousel 1st Chest"),
            lambda state: state.has("Divine Rose", player) or options.advanced_logic)
        add_rule(kh1world.get_location("Hollow Bastion Library 2nd Floor Turn the Carousel 2nd Chest"),
            lambda state: state.has("Divine Rose", player) or options.advanced_logic)
        add_rule(kh1world.get_location("Hollow Bastion Entrance Hall Emblem Piece (Chest)"),
            lambda state: state.has("Divine Rose", player) or options.advanced_logic)
        if options.hundred_acre_wood:
            add_rule(kh1world.get_location("100 Acre Wood Meadow Inside Log Chest"),
                lambda state: state.has("Oathkeeper", player))
            add_rule(kh1world.get_location("100 Acre Wood Bouncing Spot Left Cliff Chest"),
                lambda state: state.has("Oathkeeper", player))
            add_rule(kh1world.get_location("100 Acre Wood Bouncing Spot Right Tree Alcove Chest"),
                lambda state: state.has("Oathkeeper", player))
            add_rule(kh1world.get_location("100 Acre Wood Bouncing Spot Under Giant Pot Chest"),
                lambda state: state.has("Oathkeeper", player))
    
    
    for location in location_table.keys():
        try:
            kh1world.get_location(location)
        except KeyError:
            continue
        if options.remote_items.current_key == "off":
            if location_table[location].type == "Chest":
                add_item_rule(kh1world.get_location(location),
                    lambda i: (i.player != player or i.name not in get_items_by_type("Stats").keys()))
            if location_table[location].type == "Reward":
                add_item_rule(kh1world.get_location(location),
                    lambda i: (i.player != player or i.name not in get_items_by_type("Stats").keys()))
            if location_table[location].type == "Static":
                add_item_rule(kh1world.get_location(location),
                    lambda i: (i.player != player or i.name in get_items_by_type("Item").keys()))
            if location_table[location].type == "Level Slot 1":
                add_item_rule(kh1world.get_location(location),
                    lambda i: (i.player != player or i.name in get_items_by_type("Stats").keys()))
            if location_table[location].type == "Level Slot 2":
                add_item_rule(kh1world.get_location(location),
                    lambda i: (i.player != player or (i.name not in get_items_by_type("Item").keys() and i.name not in get_items_by_type("Shared Ability").keys())))
            if location_table[location].type == "Synth":
                add_item_rule(kh1world.get_location(location),
                    lambda i: (i.player != player or (i.name in get_items_by_type("Item").keys())))
        if location_table[location].type == "Prize":
            add_item_rule(kh1world.get_location(location),
                lambda i: (
                    i.player == player 
                    and i.name in get_items_by_type("Item").keys()
                    and i.name not in ["Puppy", "Lucky Emblem"]
                    and
                    (
                        (
                            item_table[i.name].max_quantity == 1
                            and item_table[i.name].classification != ItemClassification.filler
                        )
                        or item_table[i.name].classification == ItemClassification.filler
                    )
                ))

    
    add_rule(kh1world.get_entrance("Wonderland"),
        lambda state: state.has("Wonderland", player) and has_x_worlds(state, player, 2, options.keyblades_unlock_chests))
    add_rule(kh1world.get_entrance("Olympus Coliseum"),
        lambda state: state.has("Olympus Coliseum", player) and has_x_worlds(state, player, 2, options.keyblades_unlock_chests))
    add_rule(kh1world.get_entrance("Deep Jungle"),
        lambda state: state.has("Deep Jungle", player) and has_x_worlds(state, player, 2, options.keyblades_unlock_chests))
    add_rule(kh1world.get_entrance("Agrabah"),
        lambda state: state.has("Agrabah", player) and has_x_worlds(state, player, 2, options.keyblades_unlock_chests))
    add_rule(kh1world.get_entrance("Monstro"),
        lambda state: state.has("Monstro", player) and has_x_worlds(state, player, 2, options.keyblades_unlock_chests))
    if options.atlantica:
        add_rule(kh1world.get_entrance("Atlantica"),
            lambda state: state.has("Atlantica", player) and has_x_worlds(state, player, 2, options.keyblades_unlock_chests))
    add_rule(kh1world.get_entrance("Halloween Town"),
        lambda state: state.has("Halloween Town", player) and has_x_worlds(state, player, 2, options.keyblades_unlock_chests))
    add_rule(kh1world.get_entrance("Neverland"),
        lambda state: state.has("Neverland", player) and has_x_worlds(state, player, 3, options.keyblades_unlock_chests))
    add_rule(kh1world.get_entrance("Hollow Bastion"),
        lambda state: state.has("Hollow Bastion", player) and has_x_worlds(state, player, 5, options.keyblades_unlock_chests))
    add_rule(kh1world.get_entrance("End of the World"),
        lambda state: has_x_worlds(state, player, 7, options.keyblades_unlock_chests) and (has_lucky_emblems(state, player, eotw_required_lucky_emblems) or state.has("End of the World", player)))
    add_rule(kh1world.get_entrance("100 Acre Wood"),
        lambda state: state.has("Progressive Fire", player))

    multiworld.completion_condition[player] = lambda state: state.has("Victory", player)
