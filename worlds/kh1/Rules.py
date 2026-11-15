from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, add_item_rule
from math import ceil
from BaseClasses import ItemClassification
from .Data import WORLD_KEY_ITEMS, LOGIC_BEGINNER, LOGIC_NORMAL, LOGIC_PROUD, LOGIC_MINIMAL

from .Locations import KH1Location, location_table
from .Items import KH1Item, item_table

WORLDS =    ["Destiny Islands", "Traverse Town", "Wonderland", "Olympus Coliseum", "Deep Jungle", "Agrabah",      "Monstro",      "Atlantica", "Halloween Town", "Neverland",  "Hollow Bastion", "End of the World", "100 Acre Wood"]
KEYBLADES = ["Oathkeeper",      "Lionheart",     "Lady Luck",  "Olympia",          "Jungle King", "Three Wishes", "Wishing Star", "Crabclaw",  "Pumpkinhead",    "Fairy Harp", "Divine Rose",    "Oblivion",         "Spellbinder"]
BROKEN_KEYBLADE_LOCKING_LOCATIONS = [
    "End of the World Final Dimension 2nd Chest",
    "End of the World Final Dimension 4th Chest",
    "End of the World Final Dimension 7th Chest",
    "End of the World Final Dimension 8th Chest",
    "End of the World Final Dimension 10th Chest",
    "Neverland Hold Aero Chest",
    "Hollow Bastion Library 1st Floor Turn the Carousel Chest", 
    "Hollow Bastion Library Top of Bookshelf Turn the Carousel Chest",
    "Hollow Bastion Library 2nd Floor Turn the Carousel 1st Chest",
    "Hollow Bastion Library 2nd Floor Turn the Carousel 2nd Chest",
    "Hollow Bastion Entrance Hall Emblem Piece (Chest)",
    "Atlantica Sunken Ship In Flipped Boat Chest",
    "Atlantica Sunken Ship Seabed Chest",
    "Atlantica Sunken Ship Inside Ship Chest",
    "Atlantica Ariel's Grotto High Chest",
    "Atlantica Ariel's Grotto Middle Chest",
    "Atlantica Ariel's Grotto Low Chest",
    "Atlantica Ursula's Lair Use Fire on Urchin Chest",
    "Atlantica Undersea Gorge Jammed by Ariel's Grotto Chest",
    "Atlantica Triton's Palace White Trinity Chest",
    "Atlantica Sunken Ship Crystal Trident Event"
]

def has_x_worlds(state: CollectionState, player: int, num_of_worlds: int, keyblades_unlock_chests: bool, logic_difficulty: int, hundred_acre_wood: bool) -> bool:
    if logic_difficulty >= LOGIC_MINIMAL:
        return True
    else:
        worlds_acquired = 0.0
        for i in range(len(WORLDS)):
            if WORLDS[i] == "Traverse Town":
                worlds_acquired = worlds_acquired + 0.5
                if not keyblades_unlock_chests or state.has(KEYBLADES[i], player):
                    worlds_acquired = worlds_acquired + 0.5
            elif WORLDS[i] == "100 Acre Wood" and hundred_acre_wood:
                if state.has("Progressive Fire", player):
                    worlds_acquired = worlds_acquired + 0.5
                    if not keyblades_unlock_chests or state.has(KEYBLADES[i], player):
                        worlds_acquired = worlds_acquired + 0.5
            elif state.has(WORLDS[i], player):
                worlds_acquired = worlds_acquired + 0.5
                if not keyblades_unlock_chests or state.has(KEYBLADES[i], player):
                    worlds_acquired = worlds_acquired + 0.5
        return worlds_acquired >= num_of_worlds

def has_emblems(state: CollectionState, player: int, keyblades_unlock_chests: bool, logic_difficulty: int, hundred_acre_wood: bool) -> bool:
    return state.has_all({
        "Emblem Piece (Flame)",
        "Emblem Piece (Chest)",
        "Emblem Piece (Statue)",
        "Emblem Piece (Fountain)",
        "Hollow Bastion"}, player) and has_x_worlds(state, player, 6, keyblades_unlock_chests, logic_difficulty, hundred_acre_wood)

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

def has_offensive_magic(state: CollectionState, player: int, logic_difficulty: int) -> bool:
    return (
        state.has_any({"Progressive Fire", "Progressive Blizzard"}, player)
        or (logic_difficulty > LOGIC_NORMAL and state.has_any({"Progressive Thunder", "Progressive Gravity"}, player))
        or (logic_difficulty > LOGIC_PROUD and state.has("Progressive Stop", player))
    )

def has_lucky_emblems(state: CollectionState, player: int, required_amt: int) -> bool:
    return state.has("Lucky Emblem", player, required_amt)

def has_final_rest_door(state: CollectionState, player: int, final_rest_door_requirement: str, final_rest_door_required_lucky_emblems: int):
    if final_rest_door_requirement == "lucky_emblems":
        return state.has("Lucky Emblem", player, final_rest_door_required_lucky_emblems)
    else:
        return state.has("Final Door Key", player)

def has_defensive_tools(state: CollectionState, player: int, logic_difficulty: int) -> bool:
    if logic_difficulty >= LOGIC_MINIMAL:
        return True
    else:
        return (
            state.has_all_counts({"Progressive Cure": 2, "Leaf Bracer": 1, "Dodge Roll": 1}, player)
            and state.has_any_count({"Second Chance": 1, "MP Rage": 1, "Progressive Aero": 2}, player)
        )

def has_basic_tools(state: CollectionState, player: int) -> bool:
    return (
            state.has_all({"Dodge Roll", "Progressive Cure"}, player)
            and state.has_any({"Combo Master", "Strike Raid", "Sonic Blade", "Counterattack"}, player)
            and state.has_any({"Leaf Bracer", "Second Chance", "Guard"}, player)
            and has_offensive_magic(state, player, 6)
        )

def can_dumbo_skip(state: CollectionState, player: int) -> bool:
    return (
            state.has("Dumbo", player)
            and state.has_group("Magic", player)
        )

def has_oogie_manor(state: CollectionState, player: int, logic_difficulty: int) -> bool:
    return (
            state.has("Progressive Fire", player)
            or (logic_difficulty > LOGIC_BEGINNER and state.has("High Jump", player, 3))
            or (logic_difficulty > LOGIC_NORMAL and state.has("High Jump", player, 2) or (state.has_all({"High Jump", "Progressive Glide"}, player)))
            or (logic_difficulty > LOGIC_PROUD and state.has_any({"High Jump", "Progressive Glide"}, player))
        )

def has_item_workshop(state: CollectionState, player: int, logic_difficulty: int) -> bool:
    return (
            state.has("Green Trinity", player)
            or (logic_difficulty > LOGIC_NORMAL and state.has("High Jump", player, 2))
        )

def has_parasite_cage(state: CollectionState, player: int, logic_difficulty: int, worlds: bool) -> bool:
    return (
            state.has("Monstro", player)
            and
            (
                state.has("High Jump", player)
                or (logic_difficulty > LOGIC_BEGINNER and state.has("Progressive Glide", player))
            )
            and worlds
    )

def has_key_item(state: CollectionState, player: int, key_item: str, stacking_world_items: bool, halloween_town_key_item_bundle: bool, difficulty: int, keyblades_unlock_chests: bool):
    return (
        (
            state.has(key_item, player)
            or (stacking_world_items and state.has(WORLD_KEY_ITEMS[key_item], player, 2))
            or (key_item == "Jack-In-The-Box" and state.has("Forget-Me-Not", player) and halloween_town_key_item_bundle)
        )
        # Adding this to make sure that if a beginner logic player is playing with keyblade locking, 
        # anything that would require the Crystal Trident should expect the player to be able to 
        # open the Crystal Trident chest.
        and (key_item != "Crystal Trident" or difficulty > LOGIC_BEGINNER or not keyblades_unlock_chests or state.has("Crabclaw", player))
    )

def set_rules(kh1world):
    multiworld                             = kh1world.multiworld
    player                                 = kh1world.player
    options                                = kh1world.options
    eotw_required_lucky_emblems            = kh1world.determine_lucky_emblems_required_to_open_end_of_the_world()
    final_rest_door_required_lucky_emblems = kh1world.determine_lucky_emblems_required_to_open_final_rest_door()
    final_rest_door_requirement            = kh1world.options.final_rest_door_key.current_key
    day_2_materials                        = kh1world.options.day_2_materials.value
    homecoming_materials                   = kh1world.options.homecoming_materials.value
    difficulty                             = kh1world.options.logic_difficulty.value # difficulty > 0 is Normal or higher; difficulty > 5 is Proud or higher; difficulty > 10 is Minimal and higher; others are for if another difficulty is added
    stacking_world_items                   = kh1world.options.stacking_world_items.value
    halloween_town_key_item_bundle         = kh1world.options.halloween_town_key_item_bundle.value
    end_of_the_world_unlock                = kh1world.options.end_of_the_world_unlock.current_key
    hundred_acre_wood                      = kh1world.options.hundred_acre_wood
    

    add_rule(kh1world.get_location("Traverse Town 1st District Candle Puzzle Chest"),
        lambda state: state.has("Progressive Blizzard", player))
    add_rule(kh1world.get_location("Traverse Town 1st District Accessory Shop Roof Chest"), # this check could justifiably require high jump for Beginners
            lambda state: state.has("High Jump", player)) or difficulty > LOGIC_BEGINNER
    add_rule(kh1world.get_location("Traverse Town Mystical House Yellow Trinity Chest"),
        lambda state: (
            state.has("Progressive Fire", player)
            and
            (
                state.has("Yellow Trinity", player)
                or (difficulty > LOGIC_BEGINNER and state.has("High Jump", player, 2))
                or (difficulty > LOGIC_NORMAL and state.has("High Jump", player))
            )
        ))
    add_rule(kh1world.get_location("Traverse Town Secret Waterway White Trinity Chest"),
        lambda state: state.has("White Trinity", player))
    add_rule(kh1world.get_location("Traverse Town Geppetto's House Chest"),
        lambda state: (has_parasite_cage(state, player, difficulty, has_x_worlds(state, player, 3, options.keyblades_unlock_chests, difficulty, hundred_acre_wood))))
    add_rule(kh1world.get_location("Traverse Town Item Workshop Right Chest"),
        lambda state: (has_item_workshop(state, player, difficulty)))
    add_rule(kh1world.get_location("Traverse Town Item Workshop Left Chest"),
        lambda state: (has_item_workshop(state, player, difficulty)))
    add_rule(kh1world.get_location("Traverse Town 1st District Blue Trinity Balcony Chest"),
        lambda state: (
            (state.has("Blue Trinity", player) and state.has("Progressive Glide", player))
            or (difficulty > LOGIC_NORMAL and state.has("Progressive Glide", player))
        ))
    add_rule(kh1world.get_location("Traverse Town Mystical House Glide Chest"),
        lambda state: (
            state.has("Progressive Fire", player)
            and
            (
                state.has("Progressive Glide", player)
                or
                (
                    difficulty > LOGIC_NORMAL
                    and
                    (
                        state.has("High Jump", player, 3)
                        or
                        (
                            state.has("Combo Master", player)
                            and
                            (
                                state.has("High Jump", player, 2)
                                or
                                (
                                    state.has("High Jump", player)
                                    and state.has("Air Combo Plus", player, 2)
                                    #or state.has("Yellow Trinity", player)
                                )
                            )
                        )
                    )
                )
                or
                (
                    difficulty > LOGIC_PROUD
                    and
                    (
                        state.has("Mermaid Kick", player)
                        or state.has("Combo Master", player) and (state.has("High Jump", player) or state.has("Air Combo Plus", player, 2))
                    )
                )
            )
        ))
    add_rule(kh1world.get_location("Traverse Town Alleyway Behind Crates Chest"),
        lambda state: state.has("Red Trinity", player))
    add_rule(kh1world.get_location("Wonderland Rabbit Hole Green Trinity Chest"),
        lambda state: state.has("Green Trinity", player))
    add_rule(kh1world.get_location("Wonderland Rabbit Hole Defeat Heartless 3 Chest"),
        lambda state: (
            has_x_worlds(state, player, 6, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
            or (difficulty > LOGIC_NORMAL and has_x_worlds(state, player, 3, options.keyblades_unlock_chests, difficulty, hundred_acre_wood))
            or difficulty > LOGIC_PROUD
        ))
        
    add_rule(kh1world.get_location("Wonderland Bizarre Room Green Trinity Chest"),
        lambda state: state.has("Green Trinity", player))
    add_rule(kh1world.get_location("Wonderland Queen's Castle Hedge Left Red Chest"),
        lambda state: (
            has_key_item(state, player, "Footprints", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            or state.has("High Jump", player)
            or (difficulty > LOGIC_BEGINNER and state.has("Progressive Glide", player))
        ))
    add_rule(kh1world.get_location("Wonderland Queen's Castle Hedge Right Blue Chest"),
        lambda state: (
            has_key_item(state, player, "Footprints", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            or state.has("High Jump", player)
            or (difficulty > LOGIC_BEGINNER and state.has("Progressive Glide", player))
        ))
    add_rule(kh1world.get_location("Wonderland Queen's Castle Hedge Right Red Chest"),
        lambda state: (
            has_key_item(state, player, "Footprints", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            or state.has("High Jump", player)
            or (difficulty > LOGIC_BEGINNER and state.has("Progressive Glide", player))
        ))
    add_rule(kh1world.get_location("Wonderland Lotus Forest Thunder Plant Chest"),
        lambda state: (
            state.has("Progressive Thunder", player)
            and has_key_item(state, player, "Footprints", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
        ))
    add_rule(kh1world.get_location("Wonderland Lotus Forest Through the Painting Thunder Plant Chest"),
        lambda state: (
            state.has("Progressive Thunder", player)
            and has_key_item(state, player, "Footprints", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
        ))
    add_rule(kh1world.get_location("Wonderland Lotus Forest Glide Chest"),
        lambda state: (
            state.has("Progressive Glide", player)
            or
            (
                difficulty > LOGIC_NORMAL
                and (state.has("High Jump", player) or can_dumbo_skip(state, player))
                and has_key_item(state, player, "Footprints", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            )
            or
            (
                difficulty > LOGIC_PROUD  
                and state.has_all_counts({"Combo Master": 1, "High Jump": 3, "Air Combo Plus": 2}, player)
            )
        ))
    add_rule(kh1world.get_location("Wonderland Lotus Forest Corner Chest"),
        lambda state: (
            state.has_all({"High Jump", "Progressive Glide"}, player)
            or difficulty > LOGIC_BEGINNER and state.has_any({"High Jump","Progressive Glide"}, player)
            or difficulty > LOGIC_NORMAL
        ))
    add_rule(kh1world.get_location("Wonderland Bizarre Room Lamp Chest"),
        lambda state: has_key_item(state, player, "Footprints", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Wonderland Tea Party Garden Above Lotus Forest Entrance 2nd Chest"),
        lambda state: (
            state.has("Progressive Glide", player)
            or
            (
                difficulty > LOGIC_BEGINNER
                and state.has("High Jump", player, 2)
                and has_key_item(state, player, "Footprints", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            )
            or
            (
                difficulty > LOGIC_NORMAL
                and (state.has("High Jump", player) or can_dumbo_skip(state, player))
                and has_key_item(state, player, "Footprints", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            )
            or
            (
                difficulty > LOGIC_PROUD 
                and state.has_all_counts({"Combo Master": 1, "High Jump": 3, "Air Combo Plus": 2}, player)
            )
        ))
    add_rule(kh1world.get_location("Wonderland Tea Party Garden Above Lotus Forest Entrance 1st Chest"),
        lambda state: (
            state.has("Progressive Glide", player)
            or
            (
                difficulty > LOGIC_BEGINNER
                and state.has("High Jump", player, 2)
                and has_key_item(state, player, "Footprints", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            )
            or
            (
                difficulty > LOGIC_NORMAL
                and (state.has("High Jump", player) or can_dumbo_skip(state, player))
                and has_key_item(state, player, "Footprints", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            )
            or
            (
                difficulty > LOGIC_PROUD 
                and state.has_all_counts({"Combo Master": 1, "High Jump": 3, "Air Combo Plus": 2}, player)
            )
        ))
    add_rule(kh1world.get_location("Wonderland Tea Party Garden Bear and Clock Puzzle Chest"),
        lambda state: (
            has_key_item(state, player, "Footprints", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            or state.has("Progressive Glide", player)
            or
            (
                difficulty > LOGIC_PROUD 
                and state.has_all_counts({"Combo Master": 1, "High Jump": 3, "Air Combo Plus": 2}, player)
            )
        ))
    add_rule(kh1world.get_location("Wonderland Tea Party Garden Across From Bizarre Room Entrance Chest"),
        lambda state: (
            state.has("Progressive Glide", player)
            or
            (
                difficulty > LOGIC_BEGINNER
                and state.has("High Jump", player, 3)
                and has_key_item(state, player, "Footprints", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            )
            or
            (
                difficulty > LOGIC_NORMAL
                and 
                (
                    (
                        state.has_all({"High Jump", "Combo Master"}, player)
                        and has_key_item(state, player, "Footprints", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
                    )
                    or (state.has("High Jump", player, 2) and has_key_item(state, player, "Footprints", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests))
                )
            )
            or
            (
                difficulty > LOGIC_PROUD 
                and state.has_all_counts({"Combo Master": 1, "High Jump": 3, "Air Combo Plus": 2}, player)
            )
        ))
    add_rule(kh1world.get_location("Wonderland Lotus Forest Through the Painting White Trinity Chest"),
        lambda state: (
            state.has("White Trinity", player)
            and has_key_item(state, player, "Footprints", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
        ))
    add_rule(kh1world.get_location("Deep Jungle Hippo's Lagoon Right Chest"),
        lambda state: (
            state.has_all({"High Jump", "Progressive Glide"}, player)
            or
            (
                difficulty > LOGIC_BEGINNER
                and (state.has("High Jump", player)
                or state.has("Progressive Glide", player))
            )
            or
            difficulty > LOGIC_NORMAL
        ))
    add_rule(kh1world.get_location("Deep Jungle Climbing Trees Blue Trinity Chest"),
        lambda state: state.has("Blue Trinity", player))
    add_rule(kh1world.get_location("Deep Jungle Cavern of Hearts White Trinity Chest"),
        lambda state: (
            state.has("White Trinity", player)
            and has_key_item(state, player, "Slides", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
        ))
    add_rule(kh1world.get_location("Deep Jungle Camp Blue Trinity Chest"),
        lambda state: state.has("Blue Trinity", player))
    add_rule(kh1world.get_location("Deep Jungle Waterfall Cavern Low Chest"),
        lambda state: has_key_item(state, player, "Slides", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Deep Jungle Waterfall Cavern Middle Chest"),
        lambda state: has_key_item(state, player, "Slides", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Deep Jungle Waterfall Cavern High Wall Chest"),
        lambda state: has_key_item(state, player, "Slides", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Deep Jungle Waterfall Cavern High Middle Chest"),
        lambda state: has_key_item(state, player, "Slides", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Deep Jungle Tree House Rooftop Chest"),
        lambda state: (
           state.has("High Jump", player)
           or difficulty > LOGIC_NORMAL
        ))
    add_rule(kh1world.get_location("Deep Jungle Tree House Suspended Boat Chest"),
        lambda state: (
           state.has("Progressive Glide", player)
           or difficulty > LOGIC_NORMAL
        ))
    add_rule(kh1world.get_location("Agrabah Main Street High Above Palace Gates Entrance Chest"),
        lambda state: (
            state.has("High Jump", player)
            or (difficulty > LOGIC_BEGINNER and state.has("Progressive Glide", player))
            or (difficulty > LOGIC_NORMAL and can_dumbo_skip(state, player))
        ))
    add_rule(kh1world.get_location("Agrabah Palace Gates High Opposite Palace Chest"),
        lambda state: (
            state.has("High Jump", player)
            or (difficulty > LOGIC_NORMAL and state.has("Progressive Glide", player))
            or difficulty > LOGIC_PROUD
        ))
    add_rule(kh1world.get_location("Agrabah Palace Gates High Close to Palace Chest"),
        lambda state: (
            state.has_all({"High Jump", "Progressive Glide"}, player)
            or (difficulty > LOGIC_BEGINNER and state.has("High Jump", player, 3))
            or
            (
                difficulty > LOGIC_NORMAL
                and
                (
                    state.has("High Jump", player, 2)
                    or state.has("Progressive Glide", player)
                    or state.has_all({"High Jump", "Combo Master"}, player)
                )
            )
            or (difficulty > LOGIC_PROUD and state.has("Combo Master", player)) # can_dumbo_skip(state, player)
        ))
    add_rule(kh1world.get_location("Agrabah Storage Green Trinity Chest"),
        lambda state: state.has("Green Trinity", player))
    add_rule(kh1world.get_location("Agrabah Cave of Wonders Entrance Tall Tower Chest"),
        lambda state: (
            state.has("Progressive Glide", player)
            or (difficulty > LOGIC_BEGINNER and state.has("High Jump", player, 2))
            or
            (
                difficulty > LOGIC_NORMAL
                and
                (
                    state.has("Combo Master", player)
                    or can_dumbo_skip(state, player)
                    or state.has("High Jump", player)
                )
            )
            or difficulty > LOGIC_PROUD
        ))
    add_rule(kh1world.get_location("Agrabah Cave of Wonders Bottomless Hall Pillar Chest"),
        lambda state: (
           state.has("Progressive Glide", player)
           or (difficulty > LOGIC_BEGINNER and state.has("High Jump", player))
           or difficulty > LOGIC_NORMAL
        ))
    add_rule(kh1world.get_location("Agrabah Cave of Wonders Silent Chamber Blue Trinity Chest"),
        lambda state: state.has("Blue Trinity", player))
    add_rule(kh1world.get_location("Agrabah Cave of Wonders Hidden Room Right Chest"),
        lambda state: (
            state.has("Yellow Trinity", player)
            or (difficulty > LOGIC_BEGINNER and state.has("High Jump", player))
            or (difficulty > LOGIC_NORMAL and state.has("Progressive Glide", player))
        ))
    add_rule(kh1world.get_location("Agrabah Cave of Wonders Hidden Room Left Chest"),
        lambda state: (
            state.has("Yellow Trinity", player)
            or (difficulty > LOGIC_BEGINNER and state.has("High Jump", player))
            or (difficulty > LOGIC_NORMAL and state.has("Progressive Glide", player))
        ))
    add_rule(kh1world.get_location("Agrabah Cave of Wonders Entrance White Trinity Chest"),
        lambda state: state.has("White Trinity", player))
    add_rule(kh1world.get_location("Monstro Chamber 6 Platform Near Chamber 5 Entrance Chest"),
        lambda state: (
            state.has("High Jump", player)
            or difficulty > LOGIC_NORMAL
        ))
    add_rule(kh1world.get_location("Agrabah Cave of Wonders Dark Chamber Near Save Chest"),
            lambda state: state.has_any({"High Jump", "Progressive Glide"}, player) or difficulty > LOGIC_BEGINNER)
    add_rule(kh1world.get_location("Monstro Chamber 6 Other Platform Chest"),
        lambda state: (
            state.has_all({"High Jump","Progressive Glide"}, player)
            or 
            (
                difficulty > LOGIC_NORMAL 
                and
                (
                    state.has("Combo Master", player)
                    or state.has("High Jump", player)
                    or state.has("Progressive Glide", player)
                )
            )
            or
            difficulty > LOGIC_PROUD
        ))
    add_rule(kh1world.get_location("Monstro Chamber 6 Raised Area Near Chamber 1 Entrance Chest"),
        lambda state: (
            state.has_all({"High Jump","Progressive Glide"}, player)
            or 
            (
                difficulty > LOGIC_NORMAL 
                and
                (
                    state.has("Combo Master", player)
                    or state.has("High Jump", player)
                    or state.has("Progressive Glide", player)
                )
            )
            or
            difficulty > LOGIC_PROUD
        ))
    add_rule(kh1world.get_location("Halloween Town Moonlight Hill White Trinity Chest"),
        lambda state: (
            state.has("White Trinity", player)
            and has_key_item(state, player, "Forget-Me-Not", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
        ))
    add_rule(kh1world.get_location("Halloween Town Bridge Under Bridge"),
        lambda state: (
            has_key_item(state, player, "Forget-Me-Not", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests) and has_key_item(state, player, "Jack-In-The-Box", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
        ))
    add_rule(kh1world.get_location("Halloween Town Boneyard Tombstone Puzzle Chest"),
        lambda state: has_key_item(state, player, "Forget-Me-Not", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Halloween Town Bridge Right of Gate Chest"),
        lambda state: (
            has_key_item(state, player, "Forget-Me-Not", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests) and has_key_item(state, player, "Jack-In-The-Box", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            and
            (
                state.has("Progressive Glide", player)
                or state.has("High Jump", player, 3)
                or (difficulty > LOGIC_BEGINNER and state.has("High Jump", player, 2))
                or (difficulty > LOGIC_NORMAL and state.has("High Jump", player))
                or difficulty > LOGIC_PROUD
            )
        ))
    add_rule(kh1world.get_location("Halloween Town Cemetery Behind Grave Chest"),
        lambda state: (
            has_key_item(state, player, "Forget-Me-Not", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests) and has_key_item(state, player, "Jack-In-The-Box", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            and has_oogie_manor(state, player, difficulty)
        ))
    add_rule(kh1world.get_location("Halloween Town Cemetery By Cat Shape Chest"),
        lambda state: (
            has_key_item(state, player, "Forget-Me-Not", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests) and has_key_item(state, player, "Jack-In-The-Box", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            and has_oogie_manor(state, player, difficulty)
        ))
    add_rule(kh1world.get_location("Halloween Town Cemetery Between Graves Chest"),
        lambda state: (
            has_key_item(state, player, "Forget-Me-Not", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests) and has_key_item(state, player, "Jack-In-The-Box", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            and has_oogie_manor(state, player, difficulty)
        ))
    add_rule(kh1world.get_location("Halloween Town Oogie's Manor Lower Iron Cage Chest"),
        lambda state: (
            has_key_item(state, player, "Forget-Me-Not", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests) and has_key_item(state, player, "Jack-In-The-Box", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            and has_oogie_manor(state, player, difficulty)
            and (difficulty > LOGIC_BEGINNER or has_basic_tools or state.has("Progressive Glide", player))
            # difficulty > LOGIC_BEGINNER and state.has("High Jump", player, 2)
            # difficulty > LOGIC_NORMAL and state.has("Combo Master", player) or state.has("High Jump", player)
            # difficulty > LOGIC_PROUD
        ))
    add_rule(kh1world.get_location("Halloween Town Oogie's Manor Upper Iron Cage Chest"),
        lambda state: (
            has_key_item(state, player, "Forget-Me-Not", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests) and has_key_item(state, player, "Jack-In-The-Box", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            and has_oogie_manor(state, player, difficulty)
            and (difficulty > LOGIC_BEGINNER or has_basic_tools or state.has_all({"High Jump", "Progressive Glide"}))
        ))
    add_rule(kh1world.get_location("Halloween Town Oogie's Manor Hollow Chest"),
        lambda state: (
            has_key_item(state, player, "Forget-Me-Not", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests) and has_key_item(state, player, "Jack-In-The-Box", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            and has_oogie_manor(state, player, difficulty)
        ))
    add_rule(kh1world.get_location("Halloween Town Oogie's Manor Grounds Red Trinity Chest"),
        lambda state: (
            has_key_item(state, player, "Forget-Me-Not", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests) and has_key_item(state, player, "Jack-In-The-Box", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            and state.has("Red Trinity", player)
        ))
    add_rule(kh1world.get_location("Halloween Town Guillotine Square High Tower Chest"),
        lambda state: (
            state.has_all({"High Jump", "Progressive Glide"}, player)
            or (difficulty > LOGIC_BEGINNER and (state.has("High Jump", player) or state.has("Progressive Glide", player)))
            or (difficulty > LOGIC_NORMAL and can_dumbo_skip(state, player))
        ))
    add_rule(kh1world.get_location("Halloween Town Guillotine Square Pumpkin Structure Left Chest"),
        lambda state: (
            (
                state.has("High Jump", player)
                or (difficulty > LOGIC_BEGINNER and state.has("Progressive Glide", player))
                or (difficulty > LOGIC_NORMAL and can_dumbo_skip(state, player))
            )
            and
            (
                state.has("Progressive Glide", player)
                or (difficulty > LOGIC_BEGINNER and state.has("High Jump", player, 2))
                or (difficulty > LOGIC_NORMAL and state.has("Combo Master", player))
            )
        ))
    add_rule(kh1world.get_location("Halloween Town Guillotine Square Pumpkin Structure Right Chest"),
        lambda state: (
            (
                state.has("High Jump", player)
                or (difficulty > LOGIC_BEGINNER and state.has("Progressive Glide", player))
                or (difficulty > LOGIC_NORMAL and can_dumbo_skip(state, player))
            )
            and
            (
                state.has("Progressive Glide", player)
                or (difficulty > LOGIC_BEGINNER and state.has("High Jump", player, 2))
                or (difficulty > LOGIC_NORMAL and state.has("Combo Master", player))
            )
        ))
    add_rule(kh1world.get_location("Halloween Town Oogie's Manor Entrance Steps Chest"),
        lambda state: (
            has_key_item(state, player, "Forget-Me-Not", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests) and has_key_item(state, player, "Jack-In-The-Box", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
        ))
    add_rule(kh1world.get_location("Halloween Town Oogie's Manor Inside Entrance Chest"),
        lambda state: (
            has_key_item(state, player, "Forget-Me-Not", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests) and has_key_item(state, player, "Jack-In-The-Box", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
        ))
    add_rule(kh1world.get_location("Halloween Town Bridge Left of Gate Chest"),
        lambda state: (
            has_key_item(state, player, "Forget-Me-Not", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests) and has_key_item(state, player, "Jack-In-The-Box", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            and
            (
                state.has("Progressive Glide", player)
                or state.has("High Jump", player)
                or difficulty > LOGIC_NORMAL
            )
        ))
    add_rule(kh1world.get_location("Halloween Town Cemetery By Striped Grave Chest"),
        lambda state: (
            has_key_item(state, player, "Forget-Me-Not", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests) and has_key_item(state, player, "Jack-In-The-Box", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            and has_oogie_manor(state, player, difficulty)
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
            or (difficulty > LOGIC_BEGINNER and state.has("Progressive Glide", player))
        ))
    add_rule(kh1world.get_location("Monstro Mouth High Platform Across from Boat Chest"),
        lambda state: (
            state.has("High Jump", player)
            or (difficulty > LOGIC_BEGINNER and state.has("Progressive Glide", player))
        ))
    add_rule(kh1world.get_location("Monstro Mouth Green Trinity Top of Boat Chest"),
        lambda state: (
            (
                state.has("High Jump", player)
                or (difficulty > LOGIC_BEGINNER and state.has("Progressive Glide", player))
            )
            and state.has("Green Trinity", player)
        ))
    add_rule(kh1world.get_location("Monstro Mouth Near Ship Chest"),
        lambda state: (difficulty > LOGIC_BEGINNER or state.has_any({"High Jump","Progressive Glide"}, player) or has_basic_tools))
    add_rule(kh1world.get_location("Monstro Chamber 2 Platform Chest"),
        lambda state: (
            state.has_any({"High Jump","Progressive Glide"}, player)
            or difficulty > LOGIC_BEGINNER
        ))
    add_rule(kh1world.get_location("Monstro Chamber 5 Platform Chest"),
        lambda state: (
            state.has("High Jump", player)
            or difficulty > LOGIC_NORMAL
        ))
    add_rule(kh1world.get_location("Monstro Chamber 3 Platform Above Chamber 2 Entrance Chest"),
        lambda state: (
            state.has("High Jump", player)
            or difficulty > LOGIC_BEGINNER
        ))
    add_rule(kh1world.get_location("Monstro Chamber 3 Platform Near Chamber 6 Entrance Chest"),
        lambda state: (
            state.has("High Jump", player)
            or difficulty > LOGIC_BEGINNER
        ))
    add_rule(kh1world.get_location("Monstro Chamber 5 Atop Barrel Chest"),
        lambda state: (
           state.has("High Jump", player)
           or difficulty > LOGIC_NORMAL
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
           or (difficulty > LOGIC_BEGINNER and state.has("High Jump", player, 3))
        ))
    add_rule(kh1world.get_location("Neverland Clock Tower Chest"),
        lambda state: state.has("Green Trinity", player))
    add_rule(kh1world.get_location("Neverland Hold Flight 2nd Chest"),
        lambda state: (
           state.has("Green Trinity", player)
           or state.has("Progressive Glide", player)
           or (difficulty > LOGIC_BEGINNER and state.has("High Jump", player, 3))
        ))
    add_rule(kh1world.get_location("Neverland Hold Yellow Trinity Green Chest"),
        lambda state: state.has("Yellow Trinity", player))
    add_rule(kh1world.get_location("Neverland Captain's Cabin Chest"),
        lambda state: state.has("Green Trinity", player))
    add_rule(kh1world.get_location("Hollow Bastion Rising Falls Under Water 2nd Chest"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood))
    add_rule(kh1world.get_location("Hollow Bastion Rising Falls Floating Platform Near Save Chest"), #might be possible with CM and 2ACP
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
            or (state.has("Progressive Blizzard", player) and has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood))
            or (difficulty > LOGIC_BEGINNER and state.has("High Jump", player, 3))
            or (difficulty > LOGIC_NORMAL and (state.has("High Jump", player) or state.has("Combo Master", player)))
            or difficulty > LOGIC_PROUD
        ))
    add_rule(kh1world.get_location("Hollow Bastion Castle Gates Gravity Chest"),
        lambda state: (
            state.has("Progressive Gravity", player)
            and
            (
                has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
                or (difficulty > LOGIC_BEGINNER and state.has("High Jump", player, 3) and state.has("Progressive Glide", player))
                or (difficulty > LOGIC_NORMAL and (state.has("High Jump", player, 2) or can_dumbo_skip(state, player)) and state.has("Progressive Glide", player))
                or (difficulty > LOGIC_PROUD and state.has_all({"High Jump", "Progressive Glide"},player))
            )
        ))
    add_rule(kh1world.get_location("Hollow Bastion Castle Gates Freestanding Pillar Chest"),
        lambda state: (
            has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
            or (difficulty > LOGIC_BEGINNER and state.has("High Jump", player, 3))
            or (difficulty > LOGIC_NORMAL and (state.has("High Jump", player, 2) or can_dumbo_skip(state, player)))
            or (difficulty > LOGIC_PROUD and state.has_all({"High Jump", "Progressive Glide"},player))
        ))
    add_rule(kh1world.get_location("Hollow Bastion Castle Gates High Pillar Chest"),
        lambda state: (
            has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
            or (difficulty > LOGIC_BEGINNER and state.has("High Jump", player, 3))
            or (difficulty > LOGIC_NORMAL and (state.has("High Jump", player, 2) or can_dumbo_skip(state, player)))
            or (difficulty > LOGIC_PROUD and state.has_all({"High Jump", "Progressive Glide"},player))
        ))
    add_rule(kh1world.get_location("Hollow Bastion Base Level Platform Near Entrance Chest"),
        lambda state: (difficulty > LOGIC_BEGINNER or state.has_any({"Progressive Glide", "High Jump"}, player)))
    add_rule(kh1world.get_location("Hollow Bastion Great Crest Lower Chest"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood))
    add_rule(kh1world.get_location("Hollow Bastion Great Crest After Battle Platform Chest"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood))
    add_rule(kh1world.get_location("Hollow Bastion High Tower 2nd Gravity Chest"),
        lambda state: (
            state.has("Progressive Gravity", player)
            and has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
        ))
    add_rule(kh1world.get_location("Hollow Bastion High Tower 1st Gravity Chest"),
        lambda state: (
            state.has("Progressive Gravity", player)
            and has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
        ))
    add_rule(kh1world.get_location("Hollow Bastion High Tower Above Sliding Blocks Chest"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood))
    add_rule(kh1world.get_location("Hollow Bastion Lift Stop Library Node After High Tower Switch Gravity Chest"),
        lambda state: (
            state.has("Progressive Gravity", player)
            and has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
        ))
    add_rule(kh1world.get_location("Hollow Bastion Lift Stop Library Node Gravity Chest"),
        lambda state: state.has("Progressive Gravity", player))
    add_rule(kh1world.get_location("Hollow Bastion Lift Stop Under High Tower Sliding Blocks Chest"),
        lambda state: (
            has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
            and state.has("Progressive Gravity", player)
            and (difficulty > LOGIC_BEGINNER or state.has("Progressive Glide", player))
        ))
    add_rule(kh1world.get_location("Hollow Bastion Lift Stop Outside Library Gravity Chest"),
        lambda state: state.has("Progressive Gravity", player))
    add_rule(kh1world.get_location("Hollow Bastion Lift Stop Heartless Sigil Door Gravity Chest"),
        lambda state: (
            state.has("Progressive Gravity", player)
            and
            (
                has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
                or (difficulty > LOGIC_BEGINNER and state.has("High Jump", player, 3) and state.has("Progressive Glide", player))
                or (difficulty > LOGIC_NORMAL and (state.has("High Jump", player, 2) or can_dumbo_skip(state, player)) and state.has("Progressive Glide", player))
                or (difficulty > LOGIC_PROUD and state.has_all({"High Jump", "Progressive Glide"},player))
            )
        ))
    add_rule(kh1world.get_location("Hollow Bastion Waterway Blizzard on Bubble Chest"),
        lambda state: (
            (state.has("Progressive Blizzard", player) and state.has("High Jump", player))
            or (difficulty > LOGIC_BEGINNER and state.has("High Jump", player, 3))
        ))
    add_rule(kh1world.get_location("Hollow Bastion Grand Hall Steps Right Side Chest"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood))
    add_rule(kh1world.get_location("Hollow Bastion Grand Hall Oblivion Chest"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood))
    add_rule(kh1world.get_location("Hollow Bastion Grand Hall Left of Gate Chest"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood))
    add_rule(kh1world.get_location("Hollow Bastion Entrance Hall Left of Emblem Door Chest"),
        lambda state: (
            state.has("High Jump", player)
            or
            (
                difficulty > LOGIC_NORMAL
                and can_dumbo_skip(state, player)
                and has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
            )
        ))
    add_rule(kh1world.get_location("Hollow Bastion Rising Falls White Trinity Chest"),
        lambda state: state.has("White Trinity", player))
    add_rule(kh1world.get_location("End of the World Giant Crevasse 5th Chest"),
        lambda state: (
            state.has("Progressive Glide", player)
            or difficulty > LOGIC_NORMAL
        ))
    add_rule(kh1world.get_location("End of the World Giant Crevasse 1st Chest"),
        lambda state: (
            state.has("High Jump", player)
            or state.has("Progressive Glide", player)
            or difficulty > LOGIC_PROUD
        ))
    add_rule(kh1world.get_location("End of the World Giant Crevasse 2nd Chest"),
        lambda state: (difficulty > LOGIC_BEGINNER or state.has_any({"High Jump", "Progressive Glide"}, player)))
    add_rule(kh1world.get_location("End of the World Giant Crevasse 3rd Chest"),
        lambda state: (difficulty > LOGIC_BEGINNER or state.has_any({"High Jump", "Progressive Glide"}, player)))
    add_rule(kh1world.get_location("End of the World Giant Crevasse 4th Chest"),
        lambda state: (
            state.has("Progressive Glide", player)
            or
            (
                difficulty > LOGIC_NORMAL
                and 
                (
                    state.has_all({"High Jump", "Combo Master"}, player)
                    or state.has("High Jump", player, 2)
                )
            )
        ))
    add_rule(kh1world.get_location("End of the World World Terminus Agrabah Chest"),
        lambda state: (
            state.has("High Jump", player)
            or
            (
                difficulty > LOGIC_NORMAL
                and can_dumbo_skip(state, player)
                and state.has("Progressive Glide", player)
            ) #difficulty > LOGIC_PROUD and (can_dumbo_skip(state, player) or state.has("Progressive Glide", player))
        ))
    add_rule(kh1world.get_location("Monstro Chamber 6 White Trinity Chest"),
        lambda state: state.has("White Trinity", player))
    add_rule(kh1world.get_location("Traverse Town Kairi Secret Waterway Oathkeeper Event"),
        lambda state: (
            has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
            and state.has("Hollow Bastion", player)
            and has_x_worlds(state, player, 6, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
        ))
    add_rule(kh1world.get_location("Traverse Town Secret Waterway Navi Gummi Event"),
        lambda state: (
            has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
            and state.has("Hollow Bastion", player)
            and has_x_worlds(state, player, 6, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
        ))
    add_rule(kh1world.get_location("Deep Jungle Defeat Sabor White Fang Event"),
        lambda state: has_key_item(state, player, "Slides", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Deep Jungle Defeat Clayton Cure Event"),
        lambda state: has_key_item(state, player, "Slides", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Deep Jungle Seal Keyhole Jungle King Event"),
        lambda state: has_key_item(state, player, "Slides", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Deep Jungle Seal Keyhole Red Trinity Event"),
        lambda state: has_key_item(state, player, "Slides", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Olympus Coliseum Defeat Cerberus Inferno Band Event"),
        lambda state: has_key_item(state, player, "Entry Pass", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Olympus Coliseum Cloud Sonic Blade Event"),
        lambda state: has_key_item(state, player, "Entry Pass", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Wonderland Defeat Trickmaster Blizzard Event"),
        lambda state: has_key_item(state, player, "Footprints", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Wonderland Defeat Trickmaster Ifrit's Horn Event"),
        lambda state: has_key_item(state, player, "Footprints", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Monstro Defeat Parasite Cage II Stop Event"),
        lambda state: (has_parasite_cage(state, player, difficulty, has_x_worlds(state, player, 3, options.keyblades_unlock_chests, difficulty, hundred_acre_wood))))
    add_rule(kh1world.get_location("Halloween Town Defeat Oogie Boogie Holy Circlet Event"),
        lambda state: (
            has_key_item(state, player, "Forget-Me-Not", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests) and has_key_item(state, player, "Jack-In-The-Box", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            and has_oogie_manor(state, player, difficulty)
        ))
    add_rule(kh1world.get_location("Halloween Town Defeat Oogie's Manor Gravity Event"),
        lambda state: (
            has_key_item(state, player, "Forget-Me-Not", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests) and has_key_item(state, player, "Jack-In-The-Box", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            and has_oogie_manor(state, player, difficulty)
        ))
    add_rule(kh1world.get_location("Halloween Town Seal Keyhole Pumpkinhead Event"),
        lambda state: (
            has_key_item(state, player, "Forget-Me-Not", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests) and has_key_item(state, player, "Jack-In-The-Box", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            and has_oogie_manor(state, player, difficulty)
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
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood))
    add_rule(kh1world.get_location("Hollow Bastion Defeat Dragon Maleficent Fireglow Event"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood))
    add_rule(kh1world.get_location("Hollow Bastion Defeat Riku II Ragnarok Event"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood))
    add_rule(kh1world.get_location("Hollow Bastion Defeat Behemoth Omega Arts Event"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood))
    add_rule(kh1world.get_location("Hollow Bastion Speak to Princesses Fire Event"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood))
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
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood))
    add_rule(kh1world.get_location("Hollow Bastion Speak with Aerith Ansem's Report 4"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood))
    add_rule(kh1world.get_location("Hollow Bastion Defeat Maleficent Ansem's Report 5"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood))
    add_rule(kh1world.get_location("Hollow Bastion Speak with Aerith Ansem's Report 6"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood))
    add_rule(kh1world.get_location("Halloween Town Defeat Oogie Boogie Ansem's Report 7"),
        lambda state: (
            has_key_item(state, player, "Forget-Me-Not", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests) and has_key_item(state, player, "Jack-In-The-Box", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            and has_oogie_manor(state, player, difficulty)
        ))
    add_rule(kh1world.get_location("Neverland Defeat Hook Ansem's Report 9"),
        lambda state: state.has("Green Trinity", player))
    add_rule(kh1world.get_location("Hollow Bastion Speak with Aerith Ansem's Report 10"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood))
    add_rule(kh1world.get_location("Traverse Town Geppetto's House Geppetto Reward 1"),
        lambda state: has_parasite_cage(state, player, difficulty, has_x_worlds(state, player, 3, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)))
    add_rule(kh1world.get_location("Traverse Town Geppetto's House Geppetto Reward 2"),
        lambda state: has_parasite_cage(state, player, difficulty, has_x_worlds(state, player, 3, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)))
    add_rule(kh1world.get_location("Traverse Town Geppetto's House Geppetto Reward 3"),
        lambda state: has_parasite_cage(state, player, difficulty, has_x_worlds(state, player, 3, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)))
    add_rule(kh1world.get_location("Traverse Town Geppetto's House Geppetto Reward 4"),
        lambda state: has_parasite_cage(state, player, difficulty, has_x_worlds(state, player, 3, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)))
    add_rule(kh1world.get_location("Traverse Town Geppetto's House Geppetto Reward 5"),
        lambda state: has_parasite_cage(state, player, difficulty, has_x_worlds(state, player, 3, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)))
    add_rule(kh1world.get_location("Traverse Town Geppetto's House Geppetto All Summons Reward"),
        lambda state: 
            has_parasite_cage(state, player, difficulty, has_x_worlds(state, player, 3, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
            and has_all_summons(state, player)
        ))
    add_rule(kh1world.get_location("Traverse Town Geppetto's House Talk to Pinocchio"),
        lambda state: has_parasite_cage(state, player, difficulty, has_x_worlds(state, player, 3, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)))
    add_rule(kh1world.get_location("Traverse Town Magician's Study Obtained All Arts Items"),
        lambda state: (
            has_all_magic_lvx(state, player, 1)
            and has_all_arts(state, player)
            and has_x_worlds(state, player, 8, options.keyblades_unlock_chests, 0, hundred_acre_wood) #due to the softlock potential, I'm forcing it to logic normally instead of allowing the bypass
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
        lambda state: has_key_item(state, player, "Slides", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Deep Jungle Tree House Save Gorillas"),
        lambda state: has_key_item(state, player, "Slides", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Deep Jungle Camp Save Gorillas"),
        lambda state: has_key_item(state, player, "Slides", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Deep Jungle Bamboo Thicket Save Gorillas"),
        lambda state: has_key_item(state, player, "Slides", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Deep Jungle Climbing Trees Save Gorillas"),
        lambda state: has_key_item(state, player, "Slides", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Wonderland Bizarre Room Read Book"),
        lambda state: has_key_item(state, player, "Footprints", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Olympus Coliseum Coliseum Gates Green Trinity"),
        lambda state: state.has("Green Trinity", player))
    add_rule(kh1world.get_location("Olympus Coliseum Coliseum Gates Hero's License Event"),
        lambda state: has_key_item(state, player, "Entry Pass", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Deep Jungle Cavern of Hearts Navi-G Piece Event"),
        lambda state: has_key_item(state, player, "Slides", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Wonderland Bizarre Room Navi-G Piece Event"),
        lambda state: has_key_item(state, player, "Footprints", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Traverse Town Synth 15 Items"),
        lambda state: (
            min(state.count("Orichalcum", player),9) + min(state.count("Mythril", player),9) >= 15
            and has_item_workshop(state, player, difficulty)
        ))
    for i in range(33):
        add_rule(kh1world.get_location("Traverse Town Synth Item " + str(i+1).rjust(2,'0')),
            lambda state: (
                state.has("Orichalcum", player, 17)
                and state.has("Mythril", player, 16)
                and has_item_workshop(state, player, difficulty)
            ))
        add_item_rule(kh1world.get_location("Traverse Town Synth Item " + str(i+1).rjust(2,'0')),
            lambda i: (i.player != player or i.name not in ["Orichalcum", "Mythril"]))
    add_rule(kh1world.get_location("Traverse Town Gizmo Shop Postcard 1"),
        lambda state: state.has("Progressive Thunder", player))
    add_rule(kh1world.get_location("Traverse Town Gizmo Shop Postcard 2"),
        lambda state: state.has("Progressive Thunder", player))
    add_rule(kh1world.get_location("Traverse Town Item Workshop Postcard"),
        lambda state: (has_item_workshop(state, player, difficulty)))
    add_rule(kh1world.get_location("Traverse Town Geppetto's House Postcard"),
        lambda state: has_parasite_cage(state, player, difficulty, has_x_worlds(state, player, 3, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)))
    add_rule(kh1world.get_location("Hollow Bastion Entrance Hall Emblem Piece (Flame)"),
        lambda state: (
            (
                has_key_item(state, player, "Theon Vol. 6", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
                or has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
                or (difficulty > LOGIC_BEGINNER and state.has("High Jump", player, 3))
                or (difficulty > LOGIC_NORMAL and state.has("High Jump", player, 2))
            )
            and state.has("Progressive Fire", player)
            and
            (
                state.has("Progressive Glide", player)
                or state.has("Progressive Thunder", player)
                or (difficulty > LOGIC_BEGINNER and state.has("High Jump", player))
                or difficulty > LOGIC_NORMAL
            )
        ))
    add_rule(kh1world.get_location("Hollow Bastion Entrance Hall Emblem Piece (Chest)"),
        lambda state: (
            has_key_item(state, player, "Theon Vol. 6", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            or has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
            or (difficulty > LOGIC_BEGINNER and state.has("High Jump", player, 3))
            or (difficulty > LOGIC_NORMAL and state.has("High Jump", player, 2))
        ))
    add_rule(kh1world.get_location("Hollow Bastion Entrance Hall Emblem Piece (Statue)"),
        lambda state: (
            (
                has_key_item(state, player, "Theon Vol. 6", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
                or has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
                or (difficulty > LOGIC_BEGINNER and state.has("High Jump", player, 3))
                or (difficulty > LOGIC_NORMAL and state.has("High Jump", player, 2))
            )
            and state.has("Red Trinity", player)
        ))
    add_rule(kh1world.get_location("Hollow Bastion Entrance Hall Emblem Piece (Fountain)"),
        lambda state: (
            has_key_item(state, player, "Theon Vol. 6", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            or has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
            or (difficulty > LOGIC_BEGINNER and state.has("High Jump", player, 3))
            or (difficulty > LOGIC_NORMAL and state.has("High Jump", player, 2))
        ))
    add_rule(kh1world.get_location("Hollow Bastion Library Speak to Belle Divine Rose"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood))
    add_rule(kh1world.get_location("Hollow Bastion Library Speak to Aerith Cure"),
        lambda state: has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood))
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
            and has_key_item(state, player, "Footprints", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            ))
    add_rule(kh1world.get_location("Agrabah Bazaar Blue Trinity"),
        lambda state: state.has("Blue Trinity", player))
    add_rule(kh1world.get_location("Monstro Mouth Blue Trinity"),
        lambda state: state.has("Blue Trinity", player))
    add_rule(kh1world.get_location("Monstro Throat Blue Trinity"),
        lambda state: (
            state.has("Blue Trinity", player)
            and has_parasite_cage(state, player, difficulty, has_x_worlds(state, player, 3, options.keyblades_unlock_chests, difficulty, hundred_acre_wood))
            ))
    add_rule(kh1world.get_location("Monstro Chamber 5 Blue Trinity"),
        lambda state: state.has("Blue Trinity", player))
    add_rule(kh1world.get_location("Hollow Bastion Great Crest Blue Trinity"),
        lambda state: (
            state.has("Blue Trinity", player)
            and has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
        ))
    add_rule(kh1world.get_location("Hollow Bastion Dungeon Blue Trinity"),
        lambda state: state.has("Blue Trinity", player))
    add_rule(kh1world.get_location("Deep Jungle Treetop Green Trinity"),
        lambda state: state.has("Green Trinity", player))
    add_rule(kh1world.get_location("Agrabah Cave of Wonders Treasure Room Red Trinity"),
        lambda state: state.has("Red Trinity", player))
    add_rule(kh1world.get_location("Wonderland Bizarre Room Examine Flower Pot"),
        lambda state: has_key_item(state, player, "Footprints", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Wonderland Lotus Forest Yellow Elixir Flower Through Painting"),
        lambda state: has_key_item(state, player, "Footprints", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Wonderland Lotus Forest Red Flower Raise Lily Pads"),
        lambda state: has_key_item(state, player, "Footprints", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests))
    add_rule(kh1world.get_location("Wonderland Tea Party Garden Left Cushioned Chair"),
        lambda state: (
            has_key_item(state, player, "Footprints", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            or state.has("Progressive Glide", player)
            or
            (
                difficulty > LOGIC_PROUD 
                and state.has_all_counts({"Combo Master": 1, "High Jump": 3, "Air Combo Plus": 2}, player)
            )
        ))
    add_rule(kh1world.get_location("Wonderland Tea Party Garden Left Pink Chair"),
        lambda state: (
            has_key_item(state, player, "Footprints", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            or state.has("Progressive Glide", player)
            or
            (
                difficulty > LOGIC_PROUD 
                and state.has_all_counts({"Combo Master": 1, "High Jump": 3, "Air Combo Plus": 2}, player)
            )
        ))
    add_rule(kh1world.get_location("Wonderland Tea Party Garden Right Yellow Chair"),
        lambda state: (
            has_key_item(state, player, "Footprints", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            or state.has("Progressive Glide", player)
            or
            (
                difficulty > LOGIC_PROUD 
                and state.has_all_counts({"Combo Master": 1, "High Jump": 3, "Air Combo Plus": 2}, player)
            )
        ))
    add_rule(kh1world.get_location("Wonderland Tea Party Garden Left Gray Chair"),
        lambda state: (
            has_key_item(state, player, "Footprints", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            or state.has("Progressive Glide", player)
            or
            (
                difficulty > LOGIC_PROUD 
                and state.has_all_counts({"Combo Master": 1, "High Jump": 3, "Air Combo Plus": 2}, player)
            )
        ))
    add_rule(kh1world.get_location("Wonderland Tea Party Garden Right Brown Chair"),
        lambda state: (
            has_key_item(state, player, "Footprints", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            or state.has("Progressive Glide", player)
            or
            (
                difficulty > LOGIC_PROUD 
                and state.has_all_counts({"Combo Master": 1, "High Jump": 3, "Air Combo Plus": 2}, player)
            )
        ))
    add_rule(kh1world.get_location("Hollow Bastion Lift Stop from Waterway Examine Node"),
        lambda state: (
                has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
                or (difficulty > LOGIC_BEGINNER and state.has("High Jump", player, 3) and state.has("Progressive Glide", player))
                or (difficulty > LOGIC_NORMAL and (state.has("High Jump", player, 2) or can_dumbo_skip(state, player)) and state.has("Progressive Glide", player))
                or (difficulty > LOGIC_PROUD and state.has_all({"High Jump", "Progressive Glide"},player))
        ))
    for i in range(1,13):
            add_rule(kh1world.get_location("Neverland Clock Tower " + str(i).rjust(2, "0") + ":00 Door"),
                lambda state: state.has("Green Trinity", player))
    if options.hundred_acre_wood:
        add_rule(kh1world.get_location("100 Acre Wood Bouncing Spot Left Cliff Chest"),
            lambda state: (
                state.has("Torn Page", player, 4)
                and
                (
                    state.has_all({"High Jump", "Progressive Glide"},player)
                    or (difficulty > LOGIC_BEGINNER and (state.has("Progressive Glide", player) or state.has("High Jump", player)))
                    or difficulty > LOGIC_NORMAL
                )
            ))
        add_rule(kh1world.get_location("100 Acre Wood Bouncing Spot Right Tree Alcove Chest"),
            lambda state: (
                state.has("Torn Page", player, 4)
                and
                (
                    state.has_all({"High Jump", "Progressive Glide"},player)
                    or (difficulty > LOGIC_BEGINNER and (state.has("Progressive Glide", player) or state.has("High Jump", player)))
                    or difficulty > LOGIC_NORMAL
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
                    state.has_all({"High Jump", "Progressive Glide"},player)
                    or (difficulty > LOGIC_BEGINNER and (state.has("Progressive Glide", player) or state.has("High Jump", player)))
                    or difficulty > LOGIC_NORMAL
                )
            ))
        add_rule(kh1world.get_location("100 Acre Wood Bouncing Spot Turn in Rare Nut 3"),
            lambda state: (
                state.has("Torn Page", player, 4)
                and
                (
                    state.has_all({"High Jump", "Progressive Glide"},player)
                    or (difficulty > LOGIC_BEGINNER and (state.has("Progressive Glide", player) or state.has("High Jump", player)))
                    or difficulty > LOGIC_NORMAL
                )
            ))
        add_rule(kh1world.get_location("100 Acre Wood Bouncing Spot Turn in Rare Nut 4"),
            lambda state: (
                state.has("Torn Page", player, 4)
                and
                (
                    state.has_all({"High Jump", "Progressive Glide"},player)
                    or (difficulty > LOGIC_BEGINNER and (state.has("Progressive Glide", player) or state.has("High Jump", player)))
                    or difficulty > LOGIC_NORMAL
                )
            ))
        add_rule(kh1world.get_location("100 Acre Wood Bouncing Spot Turn in Rare Nut 5"),
            lambda state: (
                state.has("Torn Page", player, 4)
                and
                (
                    state.has_all({"High Jump", "Progressive Glide"},player)
                    or (difficulty > LOGIC_BEGINNER and (state.has("Progressive Glide", player) or state.has("High Jump", player)))
                    or (difficulty > LOGIC_PROUD and state.has("Combo Master", player))
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
                    state.has_all({"High Jump", "Progressive Glide"},player)
                    or (difficulty > LOGIC_BEGINNER and (state.has("Progressive Glide", player) or state.has("High Jump", player)))
                    or difficulty > LOGIC_NORMAL
                )
            ))
    if options.atlantica:
        add_rule(kh1world.get_location("Atlantica Ursula's Lair Use Fire on Urchin Chest"),
            lambda state: (
                state.has("Progressive Fire", player)
                and has_key_item(state, player, "Crystal Trident", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            ))
        add_rule(kh1world.get_location("Atlantica Triton's Palace White Trinity Chest"),
            lambda state: state.has("White Trinity", player))
        add_rule(kh1world.get_location("Atlantica Defeat Ursula I Mermaid Kick Event"),
            lambda state: (
                has_offensive_magic(state, player, difficulty)
                and has_key_item(state, player, "Crystal Trident", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            ))
        add_rule(kh1world.get_location("Atlantica Defeat Ursula II Thunder Event"),
            lambda state: (
                state.has("Mermaid Kick", player)
                and has_offensive_magic(state, player, difficulty)
                and has_key_item(state, player, "Crystal Trident", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            ))
        add_rule(kh1world.get_location("Atlantica Seal Keyhole Crabclaw Event"),
            lambda state: (
                state.has("Mermaid Kick", player)
                and has_offensive_magic(state, player, difficulty)
                and has_key_item(state, player, "Crystal Trident", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            ))
        add_rule(kh1world.get_location("Atlantica Undersea Gorge Blizzard Clam"),
            lambda state: state.has("Progressive Blizzard", player))
        add_rule(kh1world.get_location("Atlantica Undersea Valley Fire Clam"),
            lambda state: state.has("Progressive Fire", player))
        add_rule(kh1world.get_location("Atlantica Triton's Palace Thunder Clam"),
            lambda state: state.has("Progressive Thunder", player))
        add_rule(kh1world.get_location("Atlantica Cavern Nook Clam"),
            lambda state: has_key_item(state, player, "Crystal Trident", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests))
        add_rule(kh1world.get_location("Atlantica Defeat Ursula II Ansem's Report 3"),
            lambda state: (
                state.has("Mermaid Kick", player)
                and has_key_item(state, player, "Crystal Trident", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
                and has_offensive_magic(state, player, difficulty)
            ))
    if options.cups.current_key != "off":
        if options.cups.current_key == "hades_cup":
            add_rule(kh1world.get_location("Olympus Coliseum Defeat Hades Ansem's Report 8"),
                lambda state: (
                    state.has_all({
                        "Phil Cup",
                        "Pegasus Cup",
                        "Hercules Cup"}, player)
                    and has_key_item(state, player, "Entry Pass", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
                    and has_x_worlds(state, player, 8, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
                    and has_defensive_tools(state, player, difficulty)
                ))
        add_rule(kh1world.get_location("Complete Phil Cup"),
            lambda state: (
                state.has("Phil Cup", player)
                and has_key_item(state, player, "Entry Pass", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            ))
        add_rule(kh1world.get_location("Complete Phil Cup Solo"),
            lambda state: (
                state.has("Phil Cup", player)
                and has_key_item(state, player, "Entry Pass", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            ))
        add_rule(kh1world.get_location("Complete Phil Cup Time Trial"),
            lambda state: (
                state.has("Phil Cup", player)
                and has_key_item(state, player, "Entry Pass", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            ))
        add_rule(kh1world.get_location("Complete Pegasus Cup"),
            lambda state: (
                state.has("Pegasus Cup", player)
                and has_key_item(state, player, "Entry Pass", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            ))
        add_rule(kh1world.get_location("Complete Pegasus Cup Solo"),
            lambda state: (
                state.has("Pegasus Cup", player)
                and has_key_item(state, player, "Entry Pass", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            ))
        add_rule(kh1world.get_location("Complete Pegasus Cup Time Trial"),
            lambda state: (
                state.has("Pegasus Cup", player)
                and has_key_item(state, player, "Entry Pass", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
            ))
        add_rule(kh1world.get_location("Complete Hercules Cup"),
            lambda state: (
                state.has("Hercules Cup", player)
                and has_key_item(state, player, "Entry Pass", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
                and has_x_worlds(state, player, 4, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
            ))
        add_rule(kh1world.get_location("Complete Hercules Cup Solo"),
            lambda state: (
                state.has("Hercules Cup", player)
                and has_key_item(state, player, "Entry Pass", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
                and has_x_worlds(state, player, 4, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
            ))
        add_rule(kh1world.get_location("Complete Hercules Cup Time Trial"),
            lambda state: (
                state.has("Hercules Cup", player)
                and has_key_item(state, player, "Entry Pass", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
                and has_x_worlds(state, player, 4, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
            ))
        add_rule(kh1world.get_location("Hercules Cup Defeat Cloud Event"),
            lambda state: (
                state.has("Hercules Cup", player)
                and has_key_item(state, player, "Entry Pass", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
                and has_x_worlds(state, player, 4, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
            ))
        add_rule(kh1world.get_location("Hercules Cup Yellow Trinity Event"),
            lambda state: (
                state.has("Hercules Cup", player)
                and has_key_item(state, player, "Entry Pass", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
                and has_x_worlds(state, player, 4, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
            ))
        if options.cups.current_key == "hades_cup":
            add_rule(kh1world.get_location("Complete Hades Cup"),
                lambda state: (
                    state.has_all({
                        "Phil Cup",
                        "Pegasus Cup",
                        "Hercules Cup"}, player)
                    and has_key_item(state, player, "Entry Pass", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
                    and has_x_worlds(state, player, 8, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
                    and has_defensive_tools(state, player, difficulty)
                ))
            add_rule(kh1world.get_location("Complete Hades Cup Solo"),
                lambda state: (
                    state.has_all({
                        "Phil Cup",
                        "Pegasus Cup",
                        "Hercules Cup"}, player)
                    and has_key_item(state, player, "Entry Pass", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
                    and has_x_worlds(state, player, 8, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
                    and has_defensive_tools(state, player, difficulty)
                ))
            add_rule(kh1world.get_location("Complete Hades Cup Time Trial"),
                lambda state: (
                    state.has_all({
                        "Phil Cup",
                        "Pegasus Cup",
                        "Hercules Cup"}, player)
                    and has_key_item(state, player, "Entry Pass", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
                    and has_x_worlds(state, player, 8, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
                    and has_defensive_tools(state, player, difficulty)
                ))
            add_rule(kh1world.get_location("Hades Cup Defeat Cloud and Leon Event"),
                lambda state: (
                    state.has_all({
                        "Phil Cup",
                        "Pegasus Cup",
                        "Hercules Cup"}, player)
                    and has_key_item(state, player, "Entry Pass", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
                    and has_x_worlds(state, player, 8, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
                    and has_defensive_tools(state, player, difficulty)
                ))
            add_rule(kh1world.get_location("Hades Cup Defeat Yuffie Event"),
                lambda state: (
                    state.has_all({
                        "Phil Cup",
                        "Pegasus Cup",
                        "Hercules Cup"}, player)
                    and has_key_item(state, player, "Entry Pass", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
                    and has_x_worlds(state, player, 8, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
                    and has_defensive_tools(state, player, difficulty)
                ))
            add_rule(kh1world.get_location("Hades Cup Defeat Cerberus Event"),
                lambda state: (
                    state.has_all({
                        "Phil Cup",
                        "Pegasus Cup",
                        "Hercules Cup"}, player)
                    and has_key_item(state, player, "Entry Pass", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
                    and has_x_worlds(state, player, 8, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
                    and has_defensive_tools(state, player, difficulty)
                ))
            add_rule(kh1world.get_location("Hades Cup Defeat Behemoth Event"),
                lambda state: (
                    state.has_all({
                        "Phil Cup",
                        "Pegasus Cup",
                        "Hercules Cup"}, player)
                    and has_key_item(state, player, "Entry Pass", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
                    and has_x_worlds(state, player, 8, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
                    and has_defensive_tools(state, player, difficulty)
                ))
            add_rule(kh1world.get_location("Hades Cup Defeat Hades Event"),
                lambda state: (
                    state.has_all({
                        "Phil Cup",
                        "Pegasus Cup",
                        "Hercules Cup"}, player)
                    and has_key_item(state, player, "Entry Pass", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
                    and has_x_worlds(state, player, 8, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
                    and has_defensive_tools(state, player, difficulty)
                ))            
            add_rule(kh1world.get_location("Olympus Coliseum Gates Purple Jar After Defeating Hades"),
                lambda state: (
                    state.has_all({
                        "Phil Cup",
                        "Pegasus Cup",
                        "Hercules Cup"}, player)
                    and has_key_item(state, player, "Entry Pass", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
                    and has_x_worlds(state, player, 8, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
                    and has_defensive_tools(state, player, difficulty)
                ))
        if options.cups.current_key == "hades_cup" and options.super_bosses:
            add_rule(kh1world.get_location("Olympus Coliseum Defeat Ice Titan Diamond Dust Event"),
                lambda state: (
                    state.has_all({
                        "Phil Cup",
                        "Pegasus Cup",
                        "Hercules Cup"}, player)
                    and has_key_item(state, player, "Entry Pass", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
                    and (state.has("Guard", player) or difficulty > LOGIC_PROUD)
                    and has_x_worlds(state, player, 8, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
                    and has_defensive_tools(state, player, difficulty)
                ))
        add_rule(kh1world.get_location("Olympus Coliseum Olympia Chest"),
            lambda state: (
                state.has_all({
                        "Phil Cup",
                        "Pegasus Cup",
                        "Hercules Cup"}, player)
                    and has_key_item(state, player, "Entry Pass", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
                and has_x_worlds(state, player, 4, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
            ))    
    if options.super_bosses:
        add_rule(kh1world.get_location("Neverland Defeat Phantom Stop Event"),
            lambda state: (
                state.has("Green Trinity", player)
                and has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
                and 
                (
                    has_all_magic_lvx(state, player, 3)
                    or (difficulty > LOGIC_BEGINNER and has_all_magic_lvx(state, player, 2))
                    or (difficulty > LOGIC_NORMAL and state.has_all({"Progressive Fire", "Progressive Blizzard", "Progressive Thunder", "Progressive Stop"}, player))
                    or
                    (
                        difficulty > LOGIC_PROUD
                        and state.has_any({"Progressive Fire","Progressive Blizzard"}, player)
                        and state.has_any({"Progressive Fire","Progressive Thunder"}, player)
                        and state.has_any({"Progressive Thunder","Progressive Blizzard"}, player)
                        and state.has("Progressive Stop", player)
                    )
                )
                and (state.has("Leaf Bracer", player) or difficulty > LOGIC_NORMAL)
            ))
        add_rule(kh1world.get_location("Agrabah Defeat Kurt Zisa Ansem's Report 11"),
            lambda state: (
                has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
                and has_x_worlds(state, player, 8, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
                and has_defensive_tools(state, player, difficulty)
                and
                (
                    state.has("Progressive Blizzard", player, 3)
                    or (difficulty > LOGIC_BEGINNER and state.has_any_count({"Progressive Blizzard": 2, "Progressive Fire": 3,"Progressive Thunder": 3, "Progressive Gravity": 3}, player))
                    or (difficulty > LOGIC_NORMAL and (state.has_any_count({"Progressive Blizzard": 1, "Progressive Fire": 2, "Progressive Thunder": 2, "Progressive Gravity": 2}, player)))
                    or (difficulty > LOGIC_PROUD and (state.has_any({"Progressive Fire", "Progressive Thunder", "Progressive Gravity"}, player) or (state.has_group("Magic", player) and state.has_all({"Mushu", "Genie", "Dumbo"}, player))))
                )
            ))
        add_rule(kh1world.get_location("Agrabah Defeat Kurt Zisa Zantetsuken Event"),
            lambda state: (
                has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
                and has_x_worlds(state, player, 8, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
                and has_defensive_tools(state, player, difficulty)
                and
                (
                    state.has("Progressive Blizzard", player, 3)
                    or (difficulty > LOGIC_BEGINNER and state.has_any_count({"Progressive Blizzard": 2, "Progressive Fire": 3,"Progressive Thunder": 3, "Progressive Gravity": 3}, player))
                    or (difficulty > LOGIC_NORMAL and (state.has_any_count({"Progressive Blizzard": 1, "Progressive Fire": 2, "Progressive Thunder": 2, "Progressive Gravity": 2}, player)))
                    or (difficulty > LOGIC_PROUD and (state.has_any({"Progressive Fire", "Progressive Thunder", "Progressive Gravity"}, player) or (state.has_group("Magic", player) and state.has_all({"Mushu", "Genie", "Dumbo"}, player))))
                ) 
            ))
    if options.super_bosses or options.final_rest_door_key.current_key == "sephiroth":
        add_rule(kh1world.get_location("Olympus Coliseum Defeat Sephiroth Ansem's Report 12"),
            lambda state: (
                state.has_all({
                        "Phil Cup",
                        "Pegasus Cup",
                        "Hercules Cup"}, player)
                    and has_key_item(state, player, "Entry Pass", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
                and has_x_worlds(state, player, 8, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
                and has_defensive_tools(state, player, difficulty)
            ))
        add_rule(kh1world.get_location("Olympus Coliseum Defeat Sephiroth One-Winged Angel Event"),
            lambda state: (
                state.has_all({
                        "Phil Cup",
                        "Pegasus Cup",
                        "Hercules Cup"}, player)
                    and has_key_item(state, player, "Entry Pass", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests)
                and has_x_worlds(state, player, 8, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
                and has_defensive_tools(state, player, difficulty)
            ))
    if options.super_bosses or options.final_rest_door_key.current_key == "unknown":
        add_rule(kh1world.get_location("Hollow Bastion Defeat Unknown Ansem's Report 13"),
            lambda state: (
                has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
                and has_x_worlds(state, player, 8, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
                and has_defensive_tools(state, player, difficulty)
                and (difficulty > LOGIC_BEGINNER or state.has("Progressive Gravity", player))
            ))
        add_rule(kh1world.get_location("Hollow Bastion Defeat Unknown EXP Necklace Event"),
            lambda state: (
                has_emblems(state, player, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
                and has_x_worlds(state, player, 8, options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
                and has_defensive_tools(state, player, difficulty)
                and (difficulty > LOGIC_BEGINNER or state.has("Progressive Gravity", player))
            ))
    if options.jungle_slider:
        add_rule(kh1world.get_location("Deep Jungle Jungle Slider 10 Fruits"),
            lambda state: has_key_item(state, player, "Slides", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests))
        add_rule(kh1world.get_location("Deep Jungle Jungle Slider 20 Fruits"),
            lambda state: has_key_item(state, player, "Slides", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests))
        add_rule(kh1world.get_location("Deep Jungle Jungle Slider 30 Fruits"),
            lambda state: has_key_item(state, player, "Slides", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests))
        add_rule(kh1world.get_location("Deep Jungle Jungle Slider 40 Fruits"),
            lambda state: has_key_item(state, player, "Slides", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests))
        add_rule(kh1world.get_location("Deep Jungle Jungle Slider 50 Fruits"),
            lambda state: has_key_item(state, player, "Slides", stacking_world_items, halloween_town_key_item_bundle, difficulty, options.keyblades_unlock_chests))
    if options.destiny_islands:
        add_rule(kh1world.get_location("Destiny Islands Seashore Capture Fish 1 (Day 2)"),
            lambda state: state.has("Raft Materials", player, day_2_materials))
        add_rule(kh1world.get_location("Destiny Islands Seashore Capture Fish 2 (Day 2)"),
            lambda state: state.has("Raft Materials", player, day_2_materials))
        add_rule(kh1world.get_location("Destiny Islands Seashore Capture Fish 3 (Day 2)"),
            lambda state: state.has("Raft Materials", player, day_2_materials))
        add_rule(kh1world.get_location("Destiny Islands Seashore Gather Seagull Egg (Day 2)"),
            lambda state: state.has("Raft Materials", player, day_2_materials))
        add_rule(kh1world.get_location("Destiny Islands Secret Place Gather Mushroom (Day 2)"),
            lambda state: state.has("Raft Materials", player, day_2_materials))
        add_rule(kh1world.get_location("Destiny Islands Cove Gather Mushroom Near Zip Line (Day 2)"),
            lambda state: state.has("Raft Materials", player, day_2_materials))
        add_rule(kh1world.get_location("Destiny Islands Cove Gather Mushroom in Small Cave (Day 2)"),
            lambda state: state.has("Raft Materials", player, day_2_materials))
        #add_rule(kh1world.get_location("Destiny Islands Seashore Deliver Kairi Items (Day 1)"),
        #    lambda state: state.has("Raft Materials", player, day_2_materials))
        add_rule(kh1world.get_location("Destiny Islands Secret Place Gather Mushroom (Day 2)"),
            lambda state: state.has("Raft Materials", player, day_2_materials))
        add_rule(kh1world.get_location("Destiny Islands Cove Talk to Kairi (Day 2)"),
            lambda state: state.has("Raft Materials", player, day_2_materials))
        add_rule(kh1world.get_location("Destiny Islands Gather Drinking Water (Day 2)"),
            lambda state: state.has("Raft Materials", player, day_2_materials))
        add_rule(kh1world.get_location("Destiny Islands Chest"),
            lambda state: state.has("Raft Materials", player, day_2_materials))
        #add_rule(kh1world.get_location("Destiny Islands Cove Deliver Kairi Items (Day 2)"),
        #    lambda state: state.has("Raft Materials", player, homecoming_materials))
    for i in range(1,options.level_checks+1):
        add_rule(kh1world.get_location("Level " + str(i+1).rjust(3,'0') + " (Slot 1)"),
            lambda state, level_num=i: (
                has_x_worlds(state, player, min(((level_num//10)*2), 8), options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
            ))
        if i+1 in kh1world.get_slot_2_levels():
            add_rule(kh1world.get_location("Level " + str(i+1).rjust(3,'0') + " (Slot 2)"),
                lambda state, level_num=i: (
                    has_x_worlds(state, player, min(((level_num//10)*2), 8), options.keyblades_unlock_chests, difficulty, hundred_acre_wood)
                ))
    add_rule(kh1world.get_location("Final Ansem"),
        lambda state: (
            has_x_worlds(state, player, 8, options.keyblades_unlock_chests, difficulty, hundred_acre_wood) # In logic, player is strong enough
            and 
            (
                ( # Can DI Finish
                    state.has("Destiny Islands", player)
                    and state.has("Raft Materials", player, homecoming_materials)
                )
                or 
                (
                    ( # Has access to EotW
                        (
                            has_lucky_emblems(state, player, eotw_required_lucky_emblems) 
                            and end_of_the_world_unlock == "lucky_emblems"
                        )
                        or state.has("End of the World", player)
                    )
                    and has_final_rest_door(state, player, final_rest_door_requirement, final_rest_door_required_lucky_emblems) # Can open the Door
                )
            )
            and has_defensive_tools(state, player, difficulty)
        ))
    
    for location in location_table.keys():
        try:
            kh1world.get_location(location)
        except KeyError:
            continue
        if difficulty == LOGIC_BEGINNER and location_table[location].behind_boss:
            add_rule(kh1world.get_location(location),
                lambda state: has_basic_tools(state, player))
        if options.remote_items.current_key == "off":
            if location_table[location].type == "Static":
                add_item_rule(kh1world.get_location(location),
                    lambda i: (i.player != player or item_table[i.name].type == "Item"))
            if location_table[location].type == "Level Slot 1":
                add_item_rule(kh1world.get_location(location),
                    lambda i: (i.player != player or item_table[i.name].category in ["Level Up", "Limited Level Up"]))
            if location_table[location].type == "Level Slot 2":
                add_item_rule(kh1world.get_location(location),
                    lambda i: (i.player != player or (item_table[i.name].category in ["Level Up", "Limited Level Up"] or item_table[i.name].type == "Ability")))
            if location_table[location].type == "Synth":
                add_item_rule(kh1world.get_location(location),
                    lambda i: (i.player != player or (item_table[i.name].type == "Item")))
            if location_table[location].type == "Prize":
                add_item_rule(kh1world.get_location(location),
                    lambda i: (i.player != player or (item_table[i.name].type == "Item")))
        if options.keyblades_unlock_chests:
            if location_table[location].type == "Chest" or location in BROKEN_KEYBLADE_LOCKING_LOCATIONS:
                location_world = location_table[location].category
                location_required_keyblade = KEYBLADES[WORLDS.index(location_world)]
                if location not in BROKEN_KEYBLADE_LOCKING_LOCATIONS:
                    add_rule(kh1world.get_location(location),
                        lambda state, location_required_keyblade = location_required_keyblade: state.has(location_required_keyblade, player))
                else:
                    add_rule(kh1world.get_location(location),
                        lambda state, location_required_keyblade = location_required_keyblade: state.has(location_required_keyblade, player) or difficulty > LOGIC_BEGINNER)

    if options.destiny_islands:
        add_rule(kh1world.get_entrance("Destiny Islands"),
            lambda state: state.has("Destiny Islands", player))
    add_rule(kh1world.get_entrance("Wonderland"),
        lambda state: state.has("Wonderland", player) and has_x_worlds(state, player, 3, options.keyblades_unlock_chests, difficulty, hundred_acre_wood))
    add_rule(kh1world.get_entrance("Olympus Coliseum"),
        lambda state: state.has("Olympus Coliseum", player) and has_x_worlds(state, player, 3, options.keyblades_unlock_chests, difficulty, hundred_acre_wood))
    add_rule(kh1world.get_entrance("Deep Jungle"),
        lambda state: state.has("Deep Jungle", player) and has_x_worlds(state, player, 3, options.keyblades_unlock_chests, difficulty, hundred_acre_wood))
    add_rule(kh1world.get_entrance("Agrabah"),
        lambda state: state.has("Agrabah", player) and has_x_worlds(state, player, 3, options.keyblades_unlock_chests, difficulty, hundred_acre_wood))
    add_rule(kh1world.get_entrance("Monstro"),
        lambda state: state.has("Monstro", player) and has_x_worlds(state, player, 3, options.keyblades_unlock_chests, difficulty, hundred_acre_wood))
    if options.atlantica:
        add_rule(kh1world.get_entrance("Atlantica"),
            lambda state: state.has("Atlantica", player) and has_x_worlds(state, player, 3, options.keyblades_unlock_chests, difficulty, hundred_acre_wood))
    add_rule(kh1world.get_entrance("Halloween Town"),
        lambda state: state.has("Halloween Town", player) and has_x_worlds(state, player, 3, options.keyblades_unlock_chests, difficulty, hundred_acre_wood))
    add_rule(kh1world.get_entrance("Neverland"),
        lambda state: state.has("Neverland", player) and has_x_worlds(state, player, 4, options.keyblades_unlock_chests, difficulty, hundred_acre_wood))
    add_rule(kh1world.get_entrance("Hollow Bastion"),
        lambda state: state.has("Hollow Bastion", player) and has_x_worlds(state, player, 6, options.keyblades_unlock_chests, difficulty, hundred_acre_wood))
    add_rule(kh1world.get_entrance("End of the World"),
        lambda state: has_x_worlds(state, player, 8, options.keyblades_unlock_chests, difficulty, hundred_acre_wood) and ((has_lucky_emblems(state, player, eotw_required_lucky_emblems) and end_of_the_world_unlock == "lucky_emblems") or state.has("End of the World", player)))
    add_rule(kh1world.get_entrance("100 Acre Wood"),
        lambda state: state.has("Progressive Fire", player))

    multiworld.completion_condition[player] = lambda state: state.has("Victory", player)
