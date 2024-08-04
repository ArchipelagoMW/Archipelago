from BaseClasses import CollectionState

SINGLE_PUPPIES = ["Puppy " + str(i).rjust(2,"0") for i in range(1,100)]
TRIPLE_PUPPIES = ["Puppies " + str(3*(i-1)+1).rjust(2, "0") + "-" + str(3*(i-1)+3).rjust(2, "0") for i in range(1,34)]
TORN_PAGES = ["Torn Page " + str(i) for i in range(1,6)]
WORLDS =    ["Wonderland", "Olympus Coliseum", "Deep Jungle", "Agrabah",      "Monstro",      "Atlantica", "Halloween Town", "Neverland",  "Hollow Bastion", "End of the World"]
KEYBLADES = ["Lady Luck",  "Olympia",          "Jungle King", "Three Wishes", "Wishing Star", "Crabclaw",  "Pumpkinhead",    "Fairy Harp", "Divine Rose",    "Oblivion"]

def has_x_worlds(state: CollectionState, player: int, num_of_worlds: int, keyblades_unlock_chests: bool) -> bool:
    worlds_acquired = 0.0
    for i in range(len(WORLDS)):
        if state.has(WORLDS[i], player):
            worlds_acquired = worlds_acquired + 0.5
        if (state.has(WORLDS[i], player) and has_keyblade(state, player, keyblades_unlock_chests, KEYBLADES[i])) or (state.has(WORLDS[i], player) and WORLDS[i] == "Atlantica"):
            worlds_acquired = worlds_acquired + 0.5
    return worlds_acquired >= num_of_worlds

def has_emblems(state: CollectionState, player: int, keyblades_unlock_chests: bool) -> bool:
    return state.has_all({
        "Emblem Piece (Flame)",
        "Emblem Piece (Chest)",
        "Emblem Piece (Statue)",
        "Emblem Piece (Fountain)",
        "Hollow Bastion"}, player) and has_x_worlds(state, player, 5, keyblades_unlock_chests)

def has_puppies(state: CollectionState, player: int, puppies_required: int) -> bool:
    puppies_available = state.count_from_list_unique(SINGLE_PUPPIES, player)
    puppies_available = puppies_available + (state.count_from_list_unique(TRIPLE_PUPPIES, player) * 3)
    return (puppies_available >= puppies_required) or state.has("All Puppies", player)

def has_torn_pages(state: CollectionState, player: int, pages_required: int) -> bool:
    return state.count_from_list_unique(TORN_PAGES, player) >= pages_required

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

def has_reports(state: CollectionState, player: int, eotw_required_reports: int) -> bool:
    return state.has_group_unique("Reports", player, eotw_required_reports)

def has_final_rest_door(state: CollectionState, player: int, final_rest_door_requirement: str, final_rest_door_required_reports: int, keyblades_unlock_chests: bool):
    if final_rest_door_requirement == "reports":
        return state.has_group_unique("Reports", player, final_rest_door_required_reports)
    if final_rest_door_requirement == "puppies":
        return has_puppies(state, player, 99)
    if final_rest_door_requirement == "postcards":
        return state.has("Postcard", player, 10)
    if final_rest_door_requirement == "superbosses":
        return (
                state.has_all({"Olympus Coliseum", "Neverland", "Agrabah", "Hollow Bastion", "Green Trinity", "Phil Cup", "Pegasus Cup", "Hercules Cup", "Entry Pass"}, player)
                and has_emblems(state, player, keyblades_unlock_chests)
                and has_all_magic_lvx(state, player, 2)
                and has_defensive_tools(state, player)
                and has_x_worlds(state, player, 7, keyblades_unlock_chests)
            )

def has_defensive_tools(state: CollectionState, player: int) -> bool:
    return (
            (
                state.has("Progressive Cure", player, 2)
                and state.has("Leaf Bracer", player)
                and state.has("Dodge Roll", player)
            )
            and (
                state.has("Second Chance", player)
                or state.has("MP Rage", player)
                or state.has("Progressive Aero", player, 2)
            )
        )

def has_keyblade(state: CollectionState, player: int, keyblade_required: bool, item: str) -> bool:
    return not keyblade_required or state.has(item, player)

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
    multiworld                       = kh1world.multiworld
    player                           = kh1world.player
    options                          = kh1world.options
    eotw_required_reports            = kh1world.determine_reports_required_to_open_end_of_the_world()
    final_rest_door_required_reports = kh1world.determine_reports_required_to_open_final_rest_door()
    final_rest_door_requirement      = kh1world.options.final_rest_door.current_key
   
    multiworld.get_location("Traverse Town 1st District Candle Puzzle Chest"                               , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lionheart")
            and state.has("Progressive Blizzard", player)
        )
    multiworld.get_location("Traverse Town 1st District Accessory Shop Roof Chest"                         , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lionheart")
        )
    multiworld.get_location("Traverse Town 2nd District Boots and Shoes Awning Chest"                      , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lionheart")
        )
    multiworld.get_location("Traverse Town 2nd District Rooftop Chest"                                     , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lionheart")
        )
    multiworld.get_location("Traverse Town 2nd District Gizmo Shop Facade Chest"                           , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lionheart")
        )
    multiworld.get_location("Traverse Town Alleyway Balcony Chest"                                         , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lionheart")
        )
    multiworld.get_location("Traverse Town Alleyway Blue Room Awning Chest"                                , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lionheart")
        )
    multiworld.get_location("Traverse Town Alleyway Corner Chest"                                          , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lionheart")
        )
    multiworld.get_location("Traverse Town Green Room Clock Puzzle Chest"                                  , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lionheart")
        )
    multiworld.get_location("Traverse Town Green Room Table Chest"                                         , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lionheart")
        )
    multiworld.get_location("Traverse Town Red Room Chest"                                                 , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lionheart")
        )
    multiworld.get_location("Traverse Town Mystical House Yellow Trinity Chest"                            , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lionheart")
            and state.has("Progressive Fire", player)
            and
            (
                state.has("Yellow Trinity", player)
                or (options.advanced_logic and state.has("High Jump", player))
                or state.has("High Jump", player, 2)
            )
        )
    multiworld.get_location("Traverse Town Accessory Shop Chest"                                           , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lionheart")
        )
    multiworld.get_location("Traverse Town Secret Waterway White Trinity Chest"                            , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lionheart")
            and state.has("White Trinity", player)
        )
    multiworld.get_location("Traverse Town Geppetto's House Chest"                                         , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lionheart")
            and state.has("Monstro", player)
            and
            (
                state.has("High Jump", player)
                or (options.advanced_logic and state.has("Progressive Glide", player))
            )
            and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Traverse Town Item Workshop Right Chest"                                      , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lionheart")
            and
            (
                state.has("Green Trinity", player)
                or state.has("High Jump", player, 3)
            )
        )
    multiworld.get_location("Traverse Town 1st District Blue Trinity Balcony Chest"                        , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lionheart")
            and
            (
                (state.has("Blue Trinity", player) and state.has("Progressive Glide", player))
                or (options.advanced_logic and state.has("Progressive Glide", player))
            )
        )
    multiworld.get_location("Traverse Town Mystical House Glide Chest"                                     , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lionheart")
            and
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
        )
    multiworld.get_location("Traverse Town Alleyway Behind Crates Chest"                                   , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lionheart")
            and state.has("Red Trinity", player)
        )
    multiworld.get_location("Traverse Town Item Workshop Left Chest"                                       , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lionheart")
            and
            (
                state.has("Green Trinity", player)
                or state.has("High Jump", player, 3)
            )
        )
    multiworld.get_location("Traverse Town Secret Waterway Near Stairs Chest"                              , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lionheart")
        )
    multiworld.get_location("Wonderland Rabbit Hole Green Trinity Chest"                                   , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lady Luck")
            and state.has("Green Trinity", player)
        )
    multiworld.get_location("Wonderland Rabbit Hole Defeat Heartless 1 Chest"                              , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lady Luck")
        )
    multiworld.get_location("Wonderland Rabbit Hole Defeat Heartless 2 Chest"                              , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lady Luck")
        )
    multiworld.get_location("Wonderland Rabbit Hole Defeat Heartless 3 Chest"                              , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lady Luck")
            and has_x_worlds(state, player, 5, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Wonderland Bizarre Room Green Trinity Chest"                                  , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lady Luck")
            and state.has("Green Trinity", player)
        )
    multiworld.get_location("Wonderland Queen's Castle Hedge Left Red Chest"                               , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lady Luck")
            and
            (
                state.has("Footprints", player)
                or state.has("High Jump", player)
                or state.has("Progressive Glide", player)
            )
        )
    multiworld.get_location("Wonderland Queen's Castle Hedge Right Blue Chest"                             , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lady Luck")
            and
            (
                state.has("Footprints", player)
                or state.has("High Jump", player)
                or state.has("Progressive Glide", player)
            )
        )
    multiworld.get_location("Wonderland Queen's Castle Hedge Right Red Chest"                              , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lady Luck")
            and
            (
                state.has("Footprints", player)
                or state.has("High Jump", player)
                or state.has("Progressive Glide", player)
            )
        )
    multiworld.get_location("Wonderland Lotus Forest Thunder Plant Chest"                                  , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lady Luck")
            and state.has("Progressive Thunder", player)
            and state.has("Footprints", player)
        )
    multiworld.get_location("Wonderland Lotus Forest Through the Painting Thunder Plant Chest"             , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lady Luck")
            and state.has("Progressive Thunder", player)
            and state.has("Footprints", player)
        )
    multiworld.get_location("Wonderland Lotus Forest Glide Chest"                                          , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lady Luck")
            and
            (
                state.has("Progressive Glide", player)
                or
                (
                    options.advanced_logic
                    and (state.has("High Jump", player) or can_dumbo_skip(state, player))
                    and state.has("Footprints", player)
                )
            )
        )
    multiworld.get_location("Wonderland Lotus Forest Nut Chest"                                            , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lady Luck")
        )
    multiworld.get_location("Wonderland Lotus Forest Corner Chest"                                         , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lady Luck")
            and
            (
                (
                    state.has("High Jump", player)
                    or state.has("Progressive Glide", player)
                )
                or options.advanced_logic
            )
        )
    multiworld.get_location("Wonderland Bizarre Room Lamp Chest"                                           , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lady Luck")
            and state.has("Footprints", player)
        )
    multiworld.get_location("Wonderland Tea Party Garden Above Lotus Forest Entrance 2nd Chest"            , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lady Luck")
            and
            (
                state.has("Progressive Glide", player)
                or
                (
                    options.advanced_logic
                    and state.has("High Jump", player)
                    and state.has("Footprints", player)
                )
            )
        )
    multiworld.get_location("Wonderland Tea Party Garden Above Lotus Forest Entrance 1st Chest"            , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lady Luck")
            and
            (
                state.has("Progressive Glide", player)
                or
                (
                    options.advanced_logic
                    and state.has("High Jump", player)
                    and state.has("Footprints", player)
                )
            )
        )
    multiworld.get_location("Wonderland Tea Party Garden Bear and Clock Puzzle Chest"                      , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lady Luck")
            and
            (
                state.has("Footprints", player)
                or (options.advanced_logic and state.has("Progressive Glide", player))
                or state.has("High Jump", player, 2)
            )
        )
    multiworld.get_location("Wonderland Tea Party Garden Across From Bizarre Room Entrance Chest"          , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lady Luck")
            and
            (
                state.has("Progressive Glide", player)
                or
                (
                    state.has("High Jump", player, 3)
                    and state.has("Footprints", player)
                )
                or
                (
                    options.advanced_logic
                    and state.has("High Jump", player)
                    and state.has("Footprints", player)
                    and state.has("Combo Master", player)
                )
            )
        )
    multiworld.get_location("Wonderland Lotus Forest Through the Painting White Trinity Chest"             , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Lady Luck")
            and state.has("White Trinity", player)
            and state.has("Footprints", player)
        )
    multiworld.get_location("Deep Jungle Tree House Beneath Tree House Chest"                              , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Jungle King")
        )
    multiworld.get_location("Deep Jungle Tree House Rooftop Chest"                                         , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Jungle King")
        )
    multiworld.get_location("Deep Jungle Hippo's Lagoon Center Chest"                                      , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Jungle King")
        )
    multiworld.get_location("Deep Jungle Hippo's Lagoon Left Chest"                                        , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Jungle King")
        )
    multiworld.get_location("Deep Jungle Hippo's Lagoon Right Chest"                                       , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Jungle King")
            and
            (
                state.has("High Jump", player)
                or state.has("Progressive Glide", player)
                or options.advanced_logic
            )
        )
    multiworld.get_location("Deep Jungle Vines Chest"                                                      , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Jungle King")
        )
    multiworld.get_location("Deep Jungle Vines 2 Chest"                                                    , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Jungle King")
        )
    multiworld.get_location("Deep Jungle Climbing Trees Blue Trinity Chest"                                , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Jungle King")
            and state.has("Blue Trinity", player)
        )
    multiworld.get_location("Deep Jungle Tunnel Chest"                                                     , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Jungle King")
        )
    multiworld.get_location("Deep Jungle Cavern of Hearts White Trinity Chest"                             , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Jungle King")
            and state.has("White Trinity", player)
            and state.has("Slides", player)
        )
    multiworld.get_location("Deep Jungle Camp Blue Trinity Chest"                                          , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Jungle King")
            and state.has("Blue Trinity", player)
        )
    multiworld.get_location("Deep Jungle Tent Chest"                                                       , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Jungle King")
        )
    multiworld.get_location("Deep Jungle Waterfall Cavern Low Chest"                                       , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Jungle King")
            and state.has("Slides", player)
        )
    multiworld.get_location("Deep Jungle Waterfall Cavern Middle Chest"                                    , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Jungle King")
            and state.has("Slides", player)
        )
    multiworld.get_location("Deep Jungle Waterfall Cavern High Wall Chest"                                 , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Jungle King")
            and state.has("Slides", player)
        )
    multiworld.get_location("Deep Jungle Waterfall Cavern High Middle Chest"                               , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Jungle King")
            and state.has("Slides", player)
        )
    multiworld.get_location("Deep Jungle Cliff Right Cliff Left Chest"                                     , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Jungle King")
        )
    multiworld.get_location("Deep Jungle Cliff Right Cliff Right Chest"                                    , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Jungle King")
        )
    multiworld.get_location("Deep Jungle Tree House Suspended Boat Chest"                                  , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Jungle King")
            and
            (
                state.has("Progressive Glide", player)
                or options.advanced_logic
            )
        )
    multiworld.get_location("Agrabah Plaza By Storage Chest"                                               , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
        )
    multiworld.get_location("Agrabah Plaza Raised Terrace Chest"                                           , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
        )
    multiworld.get_location("Agrabah Plaza Top Corner Chest"                                               , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
        )
    multiworld.get_location("Agrabah Alley Chest"                                                          , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
        )
    multiworld.get_location("Agrabah Bazaar Across Windows Chest"                                          , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
        )
    multiworld.get_location("Agrabah Bazaar High Corner Chest"                                             , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
        )
    multiworld.get_location("Agrabah Main Street Right Palace Entrance Chest"                              , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
        )
    multiworld.get_location("Agrabah Main Street High Above Alley Entrance Chest"                          , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
        )
    multiworld.get_location("Agrabah Main Street High Above Palace Gates Entrance Chest"                   , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
            and
            (
                state.has("High Jump", player)
                or state.has("Progressive Glide", player)
                or (options.advanced_logic and can_dumbo_skip(state, player))
            )
        )
    multiworld.get_location("Agrabah Palace Gates Low Chest"                                               , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
        )
    multiworld.get_location("Agrabah Palace Gates High Opposite Palace Chest"                              , player).access_rule = lambda state: (
             has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
             and
             (
                state.has("High Jump", player)
                or options.advanced_logic
             )
        )
    multiworld.get_location("Agrabah Palace Gates High Close to Palace Chest"                              , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
            and
            (
                (
                    state.has("High Jump", player)
                    and state.has("Progressive Glide", player)
                    or
                    (
                        options.advanced_logic
                        and
                        (
                            state.has("Combo Master", player)
                            or can_dumbo_skip(state, player)
                        )
                    )
                )
                or state.has("High Jump", player, 3)
                or (options.advanced_logic and state.has("Progressive Glide", player))
            )
        )
    multiworld.get_location("Agrabah Storage Green Trinity Chest"                                          , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
            and state.has("Green Trinity", player)
        )
    multiworld.get_location("Agrabah Storage Behind Barrel Chest"                                          , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
        )
    multiworld.get_location("Agrabah Cave of Wonders Entrance Left Chest"                                  , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
        )
    multiworld.get_location("Agrabah Cave of Wonders Entrance Tall Tower Chest"                            , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
            and
            (
                state.has("Progressive Glide", player)
                or (options.advanced_logic and state.has("Combo Master", player))
                or (options.advanced_logic and can_dumbo_skip(state, player))
                or state.has("High Jump", player, 2)
            )
        )
    multiworld.get_location("Agrabah Cave of Wonders Hall High Left Chest"                                 , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
        )
    multiworld.get_location("Agrabah Cave of Wonders Hall Near Bottomless Hall Chest"                      , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
        )
    multiworld.get_location("Agrabah Cave of Wonders Bottomless Hall Raised Platform Chest"                , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
        )
    multiworld.get_location("Agrabah Cave of Wonders Bottomless Hall Pillar Chest"                         , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
            and
            (
                state.has("High Jump", player)
                or state.has("Progressive Glide", player)
                or options.advanced_logic
            )
        )
    multiworld.get_location("Agrabah Cave of Wonders Bottomless Hall Across Chasm Chest"                   , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
        )
    multiworld.get_location("Agrabah Cave of Wonders Treasure Room Across Platforms Chest"                 , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
        )
    multiworld.get_location("Agrabah Cave of Wonders Treasure Room Small Treasure Pile Chest"              , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
        )
    multiworld.get_location("Agrabah Cave of Wonders Treasure Room Large Treasure Pile Chest"              , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
        )
    multiworld.get_location("Agrabah Cave of Wonders Treasure Room Above Fire Chest"                       , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
        )
    multiworld.get_location("Agrabah Cave of Wonders Relic Chamber Jump from Stairs Chest"                 , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
        )
    multiworld.get_location("Agrabah Cave of Wonders Relic Chamber Stairs Chest"                           , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
        )
    multiworld.get_location("Agrabah Cave of Wonders Dark Chamber Abu Gem Chest"                           , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
        )
    multiworld.get_location("Agrabah Cave of Wonders Dark Chamber Across from Relic Chamber Entrance Chest", player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
        )
    multiworld.get_location("Agrabah Cave of Wonders Dark Chamber Bridge Chest"                            , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
        )
    multiworld.get_location("Agrabah Cave of Wonders Dark Chamber Near Save Chest"                         , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
        )
    multiworld.get_location("Agrabah Cave of Wonders Silent Chamber Blue Trinity Chest"                    , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
            and state.has("Blue Trinity", player)
        )
    multiworld.get_location("Agrabah Cave of Wonders Hidden Room Right Chest"                              , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
            and
            (
                state.has("Yellow Trinity", player)
                or state.has("High Jump", player)
                or (options.advanced_logic and state.has("Progressive Glide", player))
            )
        )
    multiworld.get_location("Agrabah Cave of Wonders Hidden Room Left Chest"                               , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
            and
            (
                state.has("Yellow Trinity", player)
                or state.has("High Jump", player)
                or (options.advanced_logic and state.has("Progressive Glide", player))
            )
        )
    multiworld.get_location("Agrabah Aladdin's House Main Street Entrance Chest"                           , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
        )
    multiworld.get_location("Agrabah Aladdin's House Plaza Entrance Chest"                                 , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
        )
    multiworld.get_location("Agrabah Cave of Wonders Entrance White Trinity Chest"                         , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes")
            and state.has("White Trinity", player)
        )
    multiworld.get_location("Monstro Chamber 6 Other Platform Chest"                                       , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star")
            and
            (
                state.has("High Jump", player)
                or (options.advanced_logic and state.has("Combo Master", player))
            )
        )
    multiworld.get_location("Monstro Chamber 6 Platform Near Chamber 5 Entrance Chest"                     , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star")
            and
            (
                state.has("High Jump", player)
                or options.advanced_logic
            )
        )
    multiworld.get_location("Monstro Chamber 6 Raised Area Near Chamber 1 Entrance Chest"                  , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star")
            and
            (
                state.has("High Jump", player)
                or (options.advanced_logic and state.has("Combo Master", player))
            )
        )
    multiworld.get_location("Monstro Chamber 6 Low Chest"                                                  , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star")
        )
    multiworld.get_location("Halloween Town Moonlight Hill White Trinity Chest"                            , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead")
            and state.has("White Trinity", player)
            and state.has("Forget-Me-Not", player)
        )
    multiworld.get_location("Halloween Town Bridge Under Bridge"                                           , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead")
            and state.has("Jack-In-The-Box", player)
            and state.has("Forget-Me-Not", player)
        )
    multiworld.get_location("Halloween Town Boneyard Tombstone Puzzle Chest"                               , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead")
            and state.has("Forget-Me-Not", player)
        )
    multiworld.get_location("Halloween Town Bridge Right of Gate Chest"                                    , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead")
            and state.has("Jack-In-The-Box", player)
            and state.has("Forget-Me-Not", player)
            and
            (
                state.has("Progressive Glide", player)
                or options.advanced_logic
            )
        )
    multiworld.get_location("Halloween Town Cemetery Behind Grave Chest"                                   , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead")
            and state.has("Jack-In-The-Box", player)
            and state.has("Forget-Me-Not", player)
            and has_oogie_manor(state, player, options.advanced_logic)
        )
    multiworld.get_location("Halloween Town Cemetery By Cat Shape Chest"                                   , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead")
            and state.has("Jack-In-The-Box", player)
            and state.has("Forget-Me-Not", player)
            and has_oogie_manor(state, player, options.advanced_logic)
        )
    multiworld.get_location("Halloween Town Cemetery Between Graves Chest"                                 , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead")
            and state.has("Jack-In-The-Box", player)
            and state.has("Forget-Me-Not", player)
            and has_oogie_manor(state, player, options.advanced_logic)
        )
    multiworld.get_location("Halloween Town Oogie's Manor Lower Iron Cage Chest"                           , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead")
            and state.has("Jack-In-The-Box", player)
            and state.has("Forget-Me-Not", player)
            and has_oogie_manor(state, player, options.advanced_logic)
        )
    multiworld.get_location("Halloween Town Oogie's Manor Upper Iron Cage Chest"                           , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead")
            and state.has("Jack-In-The-Box", player)
            and state.has("Forget-Me-Not", player)
            and has_oogie_manor(state, player, options.advanced_logic)
        )
    multiworld.get_location("Halloween Town Oogie's Manor Hollow Chest"                                    , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead")
            and state.has("Jack-In-The-Box", player)
            and state.has("Forget-Me-Not", player)
            and has_oogie_manor(state, player, options.advanced_logic)
        )
    multiworld.get_location("Halloween Town Oogie's Manor Grounds Red Trinity Chest"                       , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead")
            and state.has("Jack-In-The-Box", player)
            and state.has("Forget-Me-Not", player)
            and state.has("Red Trinity", player)
        )
    multiworld.get_location("Halloween Town Guillotine Square High Tower Chest"                            , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead")
            and
            (
                state.has("High Jump", player)
                or (options.advanced_logic and can_dumbo_skip(state, player))
                or (options.advanced_logic and state.has("Progressive Glide", player))
            )
        )
    multiworld.get_location("Halloween Town Guillotine Square Pumpkin Structure Left Chest"                , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead")
            and
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
        )
    multiworld.get_location("Halloween Town Oogie's Manor Entrance Steps Chest"                            , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead")
            and state.has("Jack-In-The-Box", player)
            and state.has("Forget-Me-Not", player)
        )
    multiworld.get_location("Halloween Town Oogie's Manor Inside Entrance Chest"                           , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead")
            and state.has("Jack-In-The-Box", player)
            and state.has("Forget-Me-Not", player)
        )
    multiworld.get_location("Halloween Town Bridge Left of Gate Chest"                                     , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead")
            and state.has("Jack-In-The-Box", player)
            and state.has("Forget-Me-Not", player)
            and
            (
                state.has("Progressive Glide", player)
                or state.has("High Jump", player)
                or options.advanced_logic
            )
        )
    multiworld.get_location("Halloween Town Cemetery By Striped Grave Chest"                               , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead")
            and state.has("Jack-In-The-Box", player)
            and state.has("Forget-Me-Not", player)
            and has_oogie_manor(state, player, options.advanced_logic)
        )
    multiworld.get_location("Halloween Town Guillotine Square Under Jack's House Stairs Chest"             , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead")
        )
    multiworld.get_location("Halloween Town Guillotine Square Pumpkin Structure Right Chest"               , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead")
            and
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
        )
    multiworld.get_location("Olympus Coliseum Coliseum Gates Left Behind Columns Chest"                    , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Olympia")
        )
    multiworld.get_location("Olympus Coliseum Coliseum Gates Right Blue Trinity Chest"                     , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Olympia")
            and state.has("Blue Trinity", player)
        )
    multiworld.get_location("Olympus Coliseum Coliseum Gates Left Blue Trinity Chest"                      , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Olympia")
            and state.has("Blue Trinity", player)
        )
    multiworld.get_location("Olympus Coliseum Coliseum Gates White Trinity Chest"                          , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Olympia")
            and state.has("White Trinity", player)
        )
    multiworld.get_location("Olympus Coliseum Coliseum Gates Blizzara Chest"                               , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Olympia")
            and state.has("Progressive Blizzard", player, 2)
        )
    multiworld.get_location("Olympus Coliseum Coliseum Gates Blizzaga Chest"                               , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Olympia")
            and state.has("Progressive Blizzard", player, 3)
        )
    multiworld.get_location("Monstro Mouth Boat Deck Chest"                                                , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star")
        )
    multiworld.get_location("Monstro Mouth High Platform Boat Side Chest"                                  , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star")
            and
            (
                state.has("High Jump", player)
                or state.has("Progressive Glide", player)
            )
        )
    multiworld.get_location("Monstro Mouth High Platform Across from Boat Chest"                           , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star")
            and
            (
                state.has("High Jump", player)
                or state.has("Progressive Glide", player)
            )
        )
    multiworld.get_location("Monstro Mouth Near Ship Chest"                                                , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star")
        )
    multiworld.get_location("Monstro Mouth Green Trinity Top of Boat Chest"                                , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star")
            and
            (
                state.has("High Jump", player)
                or state.has("Progressive Glide", player)
            )
            and state.has("Green Trinity", player)
        )
    multiworld.get_location("Monstro Chamber 2 Ground Chest"                                               , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star")
        )
    multiworld.get_location("Monstro Chamber 2 Platform Chest"                                             , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star")
        )
    multiworld.get_location("Monstro Chamber 5 Platform Chest"                                             , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star")
            and state.has("High Jump", player)
        )
    multiworld.get_location("Monstro Chamber 3 Ground Chest"                                               , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star")
        )
    multiworld.get_location("Monstro Chamber 3 Platform Above Chamber 2 Entrance Chest"                    , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star")
            and
            (
                state.has("High Jump", player)
                or options.advanced_logic
            )
        )
    multiworld.get_location("Monstro Chamber 3 Near Chamber 6 Entrance Chest"                              , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star")
        )
    multiworld.get_location("Monstro Chamber 3 Platform Near Chamber 6 Entrance Chest"                     , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star")
            and
            (
                state.has("High Jump", player)
                or options.advanced_logic
            )
        )
    multiworld.get_location("Monstro Mouth High Platform Near Teeth Chest"                                 , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star")
        )
    multiworld.get_location("Monstro Chamber 5 Atop Barrel Chest"                                          , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star")
            and
            (
                state.has("High Jump", player)
                or options.advanced_logic
            )
        )
    multiworld.get_location("Monstro Chamber 5 Low 2nd Chest"                                              , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star")
        )
    multiworld.get_location("Monstro Chamber 5 Low 1st Chest"                                              , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star")
        )
    multiworld.get_location("Neverland Pirate Ship Deck White Trinity Chest"                               , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Fairy Harp")
            and state.has("White Trinity", player)
            and state.has("Green Trinity", player)
        )
    multiworld.get_location("Neverland Pirate Ship Crows Nest Chest"                                       , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Fairy Harp")
            and state.has("Green Trinity", player)
        )
    multiworld.get_location("Neverland Hold Yellow Trinity Right Blue Chest"                               , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Fairy Harp")
            and state.has("Yellow Trinity", player)
        )
    multiworld.get_location("Neverland Hold Yellow Trinity Left Blue Chest"                                , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Fairy Harp")
            and state.has("Yellow Trinity", player)
        )
    multiworld.get_location("Neverland Galley Chest"                                                       , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Fairy Harp")
        )
    multiworld.get_location("Neverland Cabin Chest"                                                        , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Fairy Harp")
            and state.has("Green Trinity", player)
        )
    multiworld.get_location("Neverland Hold Flight 1st Chest "                                             , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Fairy Harp")
            and
            (
                state.has("Green Trinity", player)
                or state.has("Progressive Glide", player)
                or state.has("High Jump", player, 3)
            )
        )
    multiworld.get_location("Neverland Clock Tower Chest"                                                  , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Fairy Harp")
            and state.has("Green Trinity", player)
            and has_all_magic_lvx(state, player, 2)
        )
    multiworld.get_location("Neverland Hold Flight 2nd Chest"                                              , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Fairy Harp")
            and
            (
                state.has("Green Trinity", player)
                or state.has("Progressive Glide", player)
                or state.has("High Jump", player, 3)
            )
        )
    multiworld.get_location("Neverland Hold Yellow Trinity Green Chest"                                    , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Fairy Harp")
            and state.has("Yellow Trinity", player)
        )
    multiworld.get_location("Neverland Captain's Cabin Chest"                                              , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Fairy Harp")
            and state.has("Green Trinity", player)
        )
    multiworld.get_location("Hollow Bastion Rising Falls Water's Surface Chest"                            , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose")
        )
    multiworld.get_location("Hollow Bastion Rising Falls Under Water 1st Chest"                            , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose")
        )
    multiworld.get_location("Hollow Bastion Rising Falls Under Water 2nd Chest"                            , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose")
            and has_emblems(state, player, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Hollow Bastion Rising Falls Floating Platform Near Save Chest"                , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose")
            and
            (
                state.has("High Jump", player)
                or state.has("Progressive Glide", player)
                or state.has("Progressive Blizzard", player)
            )
         )
    multiworld.get_location("Hollow Bastion Rising Falls Floating Platform Near Bubble Chest"              , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose")
            and
            (
                state.has("High Jump", player)
                or state.has("Progressive Glide", player)
                or state.has("Progressive Blizzard", player)
            )
        )
    multiworld.get_location("Hollow Bastion Rising Falls High Platform Chest"                              , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose")
            and
            (
                state.has("Progressive Glide", player)
                or (state.has("Progressive Blizzard", player) and has_emblems(state, player, options.keyblades_unlock_chests))
                or (options.advanced_logic and state.has("Combo Master", player))
            )
        )
    multiworld.get_location("Hollow Bastion Castle Gates Gravity Chest"                                    , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose")
            and state.has("Progressive Gravity", player)
            and
            (
                has_emblems(state, player, options.keyblades_unlock_chests)
                or (options.advanced_logic and state.has("High Jump", player, 2) and state.has("Progressive Glide", player))
                or (options.advanced_logic and can_dumbo_skip(state, player) and state.has("Progressive Glide", player))
            )
        )
    multiworld.get_location("Hollow Bastion Castle Gates Freestanding Pillar Chest"                        , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose")
            and
            (
                has_emblems(state, player, options.keyblades_unlock_chests)
                or state.has("High Jump", player, 2)
                or (options.advanced_logic and can_dumbo_skip(state, player))
            )
        )
    multiworld.get_location("Hollow Bastion Castle Gates High Pillar Chest"                                , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose")
            and
            (
                has_emblems(state, player, options.keyblades_unlock_chests)
                or state.has("High Jump", player, 2)
                or (options.advanced_logic and can_dumbo_skip(state, player))
            )
        )
    multiworld.get_location("Hollow Bastion Great Crest Lower Chest"                                       , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose")
            and has_emblems(state, player, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Hollow Bastion Great Crest After Battle Platform Chest"                       , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose")
            and has_emblems(state, player, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Hollow Bastion High Tower 2nd Gravity Chest"                                  , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose")
            and state.has("Progressive Gravity", player)
            and has_emblems(state, player, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Hollow Bastion High Tower 1st Gravity Chest"                                  , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose")
            and state.has("Progressive Gravity", player)
            and has_emblems(state, player, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Hollow Bastion High Tower Above Sliding Blocks Chest"                         , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose")
            and has_emblems(state, player, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Hollow Bastion Library Top of Bookshelf Chest"                                , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose")
        )
    multiworld.get_location("Hollow Bastion Lift Stop Library Node After High Tower Switch Gravity Chest"  , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose")
            and state.has("Progressive Gravity", player)
            and has_emblems(state, player, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Hollow Bastion Lift Stop Library Node Gravity Chest"                          , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose")
            and state.has("Progressive Gravity", player)
        )
    multiworld.get_location("Hollow Bastion Lift Stop Under High Tower Sliding Blocks Chest"               , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose")
            and has_emblems(state, player, options.keyblades_unlock_chests)
            and state.has("Progressive Glide", player)
            and state.has("Progressive Gravity", player)
        )
    multiworld.get_location("Hollow Bastion Lift Stop Outside Library Gravity Chest"                       , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose")
            and state.has("Progressive Gravity", player)
        )
    multiworld.get_location("Hollow Bastion Lift Stop Heartless Sigil Door Gravity Chest"                  , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose")
            and state.has("Progressive Gravity", player)
            and has_emblems(state, player, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Hollow Bastion Base Level Bubble Under the Wall Platform Chest"               , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose")
        )
    multiworld.get_location("Hollow Bastion Base Level Platform Near Entrance Chest"                       , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose")
        )
    multiworld.get_location("Hollow Bastion Base Level Near Crystal Switch Chest"                          , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose")
        )
    multiworld.get_location("Hollow Bastion Waterway Near Save Chest"                                      , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose")
        )
    multiworld.get_location("Hollow Bastion Waterway Blizzard on Bubble Chest"                             , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose")
            and
            (
                (state.has("Progressive Blizzard", player) and state.has("High Jump", player))
                or state.has("High Jump", player, 3)
            )
        )
    multiworld.get_location("Hollow Bastion Waterway Unlock Passage from Base Level Chest"                 , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose")
        )
    multiworld.get_location("Hollow Bastion Dungeon By Candles Chest"                                      , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose")
        )
    multiworld.get_location("Hollow Bastion Dungeon Corner Chest"                                          , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose")
        )
    multiworld.get_location("Hollow Bastion Grand Hall Steps Right Side Chest"                             , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose")
            and has_emblems(state, player, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Hollow Bastion Grand Hall Oblivion Chest"                                     , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose")
            and has_emblems(state, player, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Hollow Bastion Grand Hall Left of Gate Chest"                                 , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose")
            and has_emblems(state, player, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Hollow Bastion Entrance Hall Left of Emblem Door Chest"                       , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose")
            and
            (
                state.has("High Jump", player)
                or
                (
                    options.advanced_logic
                    and can_dumbo_skip(state, player)
                    and has_emblems(state, player, options.keyblades_unlock_chests)
                )
            )
        )
    multiworld.get_location("Hollow Bastion Rising Falls White Trinity Chest"                              , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose")
            and state.has("White Trinity", player)
        )
    multiworld.get_location("End of the World Final Dimension 1st Chest"                                   , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Oblivion")
        )
    multiworld.get_location("End of the World Final Dimension 2nd Chest"                                   , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Oblivion")
        )
    multiworld.get_location("End of the World Final Dimension 3rd Chest"                                   , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Oblivion")
        )
    multiworld.get_location("End of the World Final Dimension 4th Chest"                                   , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Oblivion")
        )
    multiworld.get_location("End of the World Final Dimension 5th Chest"                                   , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Oblivion")
        )
    multiworld.get_location("End of the World Final Dimension 6th Chest"                                   , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Oblivion")
        )
    multiworld.get_location("End of the World Final Dimension 10th Chest"                                  , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Oblivion")
        )
    multiworld.get_location("End of the World Final Dimension 9th Chest"                                   , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Oblivion")
        )
    multiworld.get_location("End of the World Final Dimension 8th Chest"                                   , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Oblivion")
        )
    multiworld.get_location("End of the World Final Dimension 7th Chest"                                   , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Oblivion")
        )
    multiworld.get_location("End of the World Giant Crevasse 3rd Chest"                                    , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Oblivion")
        )
    multiworld.get_location("End of the World Giant Crevasse 5th Chest"                                    , player).access_rule = lambda state: (
            state.has("High Jump", player) or state.has("Progressive Glide", player)
            and has_keyblade(state, player, options.keyblades_unlock_chests, "Oblivion")
        )
    multiworld.get_location("End of the World Giant Crevasse 1st Chest"                                    , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Oblivion")
            and
            (
                state.has("High Jump", player)
                or state.has("Progressive Glide", player)
            )
        )
    multiworld.get_location("End of the World Giant Crevasse 4th Chest"                                    , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Oblivion")
            and
            (
                (
                    options.advanced_logic
                    and state.has("High Jump", player)
                    and state.has("Combo Master", player)
                )
                or state.has("Progressive Glide", player)
            )
        )
    multiworld.get_location("End of the World Giant Crevasse 2nd Chest"                                    , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Oblivion")
        )
    multiworld.get_location("End of the World World Terminus Traverse Town Chest"                          , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Oblivion")
        )
    multiworld.get_location("End of the World World Terminus Wonderland Chest"                             , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Oblivion")
        )
    multiworld.get_location("End of the World World Terminus Olympus Coliseum Chest"                       , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Oblivion")
        )
    multiworld.get_location("End of the World World Terminus Deep Jungle Chest"                            , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Oblivion")
        )
    multiworld.get_location("End of the World World Terminus Agrabah Chest"                                , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Oblivion")
            and
            (
                state.has("High Jump", player)
                or
                (
                    options.advanced_logic
                    and can_dumbo_skip(state, player)
                    and state.has("Progressive Glide", player)
                )
            )
        )
    multiworld.get_location("End of the World World Terminus Halloween Town Chest"                         , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Oblivion")
        )
    multiworld.get_location("End of the World World Terminus Neverland Chest"                              , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Oblivion")
        )
    multiworld.get_location("End of the World World Terminus 100 Acre Wood Chest"                          , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Oblivion")
        )
    multiworld.get_location("End of the World Final Rest Chest"                                            , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Oblivion")
        )
    multiworld.get_location("Monstro Chamber 6 White Trinity Chest"                                        , player).access_rule = lambda state: (
            has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star")
            and state.has("White Trinity", player)
        )
    multiworld.get_location("Traverse Town Kairi Secret Waterway Oathkeeper Event"                         , player).access_rule = lambda state: (
            has_emblems(state, player, options.keyblades_unlock_chests)
            and state.has("Hollow Bastion", player)
            and has_x_worlds(state, player, 5, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Deep Jungle Defeat Sabor White Fang Event"                                    , player).access_rule = lambda state: (
            state.has("Slides", player)
        )
    multiworld.get_location("Deep Jungle Defeat Clayton Cure Event"                                        , player).access_rule = lambda state: (
            state.has("Slides", player)
        )
    multiworld.get_location("Deep Jungle Seal Keyhole Jungle King Event"                                   , player).access_rule = lambda state: (
            state.has("Slides", player)
        )
    multiworld.get_location("Deep Jungle Seal Keyhole Red Trinity Event"                                   , player).access_rule = lambda state: (
            state.has("Slides", player)
        )
    multiworld.get_location("Olympus Coliseum Defeat Cerberus Inferno Band Event"                          , player).access_rule = lambda state: (
            state.has("Entry Pass", player)
        )
    multiworld.get_location("Olympus Coliseum Cloud Sonic Blade Event"                                     , player).access_rule = lambda state: (
            state.has("Entry Pass", player)
        )
    multiworld.get_location("Wonderland Defeat Trickmaster Blizzard Event"                                 , player).access_rule = lambda state: (
            state.has("Footprints", player)
        )
    multiworld.get_location("Wonderland Defeat Trickmaster Ifrit's Horn Event"                             , player).access_rule = lambda state: (
            state.has("Footprints", player)
        )
    multiworld.get_location("Monstro Defeat Parasite Cage II Stop Event"                                   , player).access_rule = lambda state: (
            state.has("High Jump", player)
            or
            (
                options.advanced_logic
                and state.has("Progressive Glide", player)
            )
        )
    multiworld.get_location("Halloween Town Defeat Oogie Boogie Holy Circlet Event"                        , player).access_rule = lambda state: (
            state.has("Jack-In-The-Box", player)
            and state.has("Forget-Me-Not", player)
            and has_oogie_manor(state, player, options.advanced_logic)
        )
    multiworld.get_location("Halloween Town Defeat Oogie's Manor Gravity Event"                            , player).access_rule = lambda state: (
            state.has("Jack-In-The-Box", player)
            and state.has("Forget-Me-Not", player)
            and has_oogie_manor(state, player, options.advanced_logic)
        )
    multiworld.get_location("Halloween Town Seal Keyhole Pumpkinhead Event"                                , player).access_rule = lambda state: (
            state.has("Jack-In-The-Box", player)
            and state.has("Forget-Me-Not", player)
            and has_oogie_manor(state, player, options.advanced_logic)
        )
    multiworld.get_location("Neverland Defeat Anti Sora Raven's Claw Event"                                , player).access_rule = lambda state: (
            state.has("Green Trinity", player)
        )
    multiworld.get_location("Neverland Encounter Hook Cure Event"                                          , player).access_rule = lambda state: (
            state.has("Green Trinity", player)
        )
    multiworld.get_location("Neverland Seal Keyhole Fairy Harp Event"                                      , player).access_rule = lambda state: (
            state.has("Green Trinity", player)
        )
    multiworld.get_location("Neverland Seal Keyhole Tinker Bell Event"                                     , player).access_rule = lambda state: (
            state.has("Green Trinity", player)
        )
    multiworld.get_location("Neverland Seal Keyhole Glide Event"                                           , player).access_rule = lambda state: (
            state.has("Green Trinity", player)
        )
    multiworld.get_location("Neverland Defeat Captain Hook Ars Arcanum Event"                              , player).access_rule = lambda state: (
            state.has("Green Trinity", player)
        )
    multiworld.get_location("Hollow Bastion Defeat Maleficent Donald Cheer Event"                          , player).access_rule = lambda state: (
            has_emblems(state, player, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Hollow Bastion Defeat Dragon Maleficent Fireglow Event"                       , player).access_rule = lambda state: (
            has_emblems(state, player, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Hollow Bastion Defeat Riku II Ragnarok Event"                                 , player).access_rule = lambda state: (
            has_emblems(state, player, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Hollow Bastion Defeat Behemoth Omega Arts Event"                              , player).access_rule = lambda state: (
            has_emblems(state, player, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Hollow Bastion Speak to Princesses Fire Event"                                , player).access_rule = lambda state: (
            has_emblems(state, player, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Traverse Town Mail Postcard 01 Event"                                         , player).access_rule = lambda state: (
            state.has("Postcard", player)
        )
    multiworld.get_location("Traverse Town Mail Postcard 02 Event"                                         , player).access_rule = lambda state: (
            state.has("Postcard", player, 2)
        )
    multiworld.get_location("Traverse Town Mail Postcard 03 Event"                                         , player).access_rule = lambda state: (
            state.has("Postcard", player, 3)
        )
    multiworld.get_location("Traverse Town Mail Postcard 04 Event"                                         , player).access_rule = lambda state: (
            state.has("Postcard", player, 4)
        )
    multiworld.get_location("Traverse Town Mail Postcard 05 Event"                                         , player).access_rule = lambda state: (
            state.has("Postcard", player, 5)
        )
    multiworld.get_location("Traverse Town Mail Postcard 06 Event"                                         , player).access_rule = lambda state: (
            state.has("Postcard", player, 6)
        )
    multiworld.get_location("Traverse Town Mail Postcard 07 Event"                                         , player).access_rule = lambda state: (
            state.has("Postcard", player, 7)
        )
    multiworld.get_location("Traverse Town Mail Postcard 08 Event"                                         , player).access_rule = lambda state: (
            state.has("Postcard", player, 8)
        )
    multiworld.get_location("Traverse Town Mail Postcard 09 Event"                                         , player).access_rule = lambda state: (
            state.has("Postcard", player, 9)
        )
    multiworld.get_location("Traverse Town Mail Postcard 10 Event"                                         , player).access_rule = lambda state: (
            state.has("Postcard", player, 10)
        )
    multiworld.get_location("Traverse Town Defeat Opposite Armor Aero Event"                               , player).access_rule = lambda state: (
            state.has("Red Trinity", player)
        )
    multiworld.get_location("Hollow Bastion Speak with Aerith Ansem's Report 2"                            , player).access_rule = lambda state: (
            has_emblems(state, player, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Hollow Bastion Speak with Aerith Ansem's Report 4"                            , player).access_rule = lambda state: (
            has_emblems(state, player, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Hollow Bastion Defeat Maleficent Ansem's Report 5"                            , player).access_rule = lambda state: (
            has_emblems(state, player, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Hollow Bastion Speak with Aerith Ansem's Report 6"                            , player).access_rule = lambda state: (
            has_emblems(state, player, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Halloween Town Defeat Oogie Boogie Ansem's Report 7"                          , player).access_rule = lambda state: (
            state.has("Jack-In-The-Box", player)
            and state.has("Forget-Me-Not", player)
            and state.has("Progressive Fire", player)
        )
    multiworld.get_location("Neverland Defeat Hook Ansem's Report 9"                                       , player).access_rule = lambda state: (
            state.has("Green Trinity", player)
        )
    multiworld.get_location("Hollow Bastion Speak with Aerith Ansem's Report 10"                           , player).access_rule = lambda state: (
            has_emblems(state, player, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Traverse Town Geppetto's House Geppetto Reward 1"                             , player).access_rule = lambda state: (
            state.has("Monstro", player)
            and
            (
                state.has("High Jump", player)
                or (options.advanced_logic and state.has("Progressive Glide", player))
            )
            and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Traverse Town Geppetto's House Geppetto Reward 2"                             , player).access_rule = lambda state: (
            state.has("Monstro", player)
            and
            (
                state.has("High Jump", player)
                or (options.advanced_logic and state.has("Progressive Glide", player))
            )
            and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Traverse Town Geppetto's House Geppetto Reward 3"                             , player).access_rule = lambda state: (
            state.has("Monstro", player)
            and
            (
                state.has("High Jump", player)
                or (options.advanced_logic and state.has("Progressive Glide", player))
            )
            and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Traverse Town Geppetto's House Geppetto Reward 4"                             , player).access_rule = lambda state: (
            state.has("Monstro", player)
            and
            (
                state.has("High Jump", player)
                or (options.advanced_logic and state.has("Progressive Glide", player))
            )
            and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Traverse Town Geppetto's House Geppetto Reward 5"                             , player).access_rule = lambda state: (
            state.has("Monstro", player)
            and
            (
                state.has("High Jump", player)
                or (options.advanced_logic and state.has("Progressive Glide", player))
            )
            and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Traverse Town Geppetto's House Geppetto All Summons Reward"                   , player).access_rule = lambda state: (
            state.has("Monstro", player)
            and
            (
                state.has("High Jump", player)
                or (options.advanced_logic and state.has("Progressive Glide", player))
            )
            and has_all_summons(state, player)
            and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Traverse Town Geppetto's House Talk to Pinocchio"                             , player).access_rule = lambda state: (
            state.has("Monstro", player)
            and
            (
                state.has("High Jump", player)
                or (options.advanced_logic and state.has("Progressive Glide", player))
            )
            and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Traverse Town Magician's Study Obtained All Arts Items"                       , player).access_rule = lambda state: (
            has_all_magic_lvx(state, player, 1)
            and has_all_arts(state, player)
            and has_x_worlds(state, player, 7, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Traverse Town Magician's Study Obtained All LV1 Magic"                        , player).access_rule = lambda state: (
            has_all_magic_lvx(state, player, 1)
        )
    multiworld.get_location("Traverse Town Magician's Study Obtained All LV3 Magic"                        , player).access_rule = lambda state: (
            has_all_magic_lvx(state, player, 3)
        )
    multiworld.get_location("Traverse Town Piano Room Return 10 Puppies"                                   , player).access_rule = lambda state: (
            has_puppies(state, player, 10)
        )
    multiworld.get_location("Traverse Town Piano Room Return 20 Puppies"                                   , player).access_rule = lambda state: (
            has_puppies(state, player, 20)
        )
    multiworld.get_location("Traverse Town Piano Room Return 30 Puppies"                                   , player).access_rule = lambda state: (
            has_puppies(state, player, 30)
        )
    multiworld.get_location("Traverse Town Piano Room Return 40 Puppies"                                   , player).access_rule = lambda state: (
            has_puppies(state, player, 40)
        )
    multiworld.get_location("Traverse Town Piano Room Return 50 Puppies Reward 1"                          , player).access_rule = lambda state: (
            has_puppies(state, player, 50)
        )
    multiworld.get_location("Traverse Town Piano Room Return 50 Puppies Reward 2"                          , player).access_rule = lambda state: (
            has_puppies(state, player, 50)
        )
    multiworld.get_location("Traverse Town Piano Room Return 60 Puppies"                                   , player).access_rule = lambda state: (
            has_puppies(state, player, 60)
        )
    multiworld.get_location("Traverse Town Piano Room Return 70 Puppies"                                   , player).access_rule = lambda state: (
            has_puppies(state, player, 70)
        )
    multiworld.get_location("Traverse Town Piano Room Return 80 Puppies"                                   , player).access_rule = lambda state: (
            has_puppies(state, player, 80)
        )
    multiworld.get_location("Traverse Town Piano Room Return 90 Puppies"                                   , player).access_rule = lambda state: (
            has_puppies(state, player, 90)
        )
    multiworld.get_location("Traverse Town Piano Room Return 99 Puppies Reward 1"                          , player).access_rule = lambda state: (
            has_puppies(state, player, 99)
        )
    multiworld.get_location("Traverse Town Piano Room Return 99 Puppies Reward 2"                          , player).access_rule = lambda state: (
            has_puppies(state, player, 99)
        )
    multiworld.get_location("Neverland Hold Aero Chest"                                                    , player).access_rule = lambda state: (
            state.has("Yellow Trinity", player)
        )
    multiworld.get_location("Deep Jungle Camp Hi-Potion Experiment"                                        , player).access_rule = lambda state: (
            state.has("Progressive Fire", player)
        )
    multiworld.get_location("Deep Jungle Camp Ether Experiment"                                            , player).access_rule = lambda state: (
            state.has("Progressive Blizzard", player)
        )
    multiworld.get_location("Deep Jungle Camp Replication Experiment"                                      , player).access_rule = lambda state: (
            state.has("Progressive Blizzard", player)
        )
    multiworld.get_location("Deep Jungle Cliff Save Gorillas"                                              , player).access_rule = lambda state: (
            state.has("Slides", player)
        )
    multiworld.get_location("Deep Jungle Tree House Save Gorillas"                                         , player).access_rule = lambda state: (
            state.has("Slides", player)
        )
    multiworld.get_location("Deep Jungle Camp Save Gorillas"                                               , player).access_rule = lambda state: (
            state.has("Slides", player)
        )
    multiworld.get_location("Deep Jungle Bamboo Thicket Save Gorillas"                                     , player).access_rule = lambda state: (
            state.has("Slides", player)
        )
    multiworld.get_location("Deep Jungle Climbing Trees Save Gorillas"                                     , player).access_rule = lambda state: (
            state.has("Slides", player)
        )
    multiworld.get_location("Deep Jungle Jungle Slider 10 Fruits"                                          , player).access_rule = lambda state: (
            state.has("Slides", player)
        )
    multiworld.get_location("Deep Jungle Jungle Slider 20 Fruits"                                          , player).access_rule = lambda state: (
            state.has("Slides", player)
        )
    multiworld.get_location("Deep Jungle Jungle Slider 30 Fruits"                                          , player).access_rule = lambda state: (
            state.has("Slides", player)
        )
    multiworld.get_location("Deep Jungle Jungle Slider 40 Fruits"                                          , player).access_rule = lambda state: (
            state.has("Slides", player)
        )
    multiworld.get_location("Deep Jungle Jungle Slider 50 Fruits"                                          , player).access_rule = lambda state: (
            state.has("Slides", player)
        )
    multiworld.get_location("Wonderland Bizarre Room Read Book"                                            , player).access_rule = lambda state: (
            state.has("Footprints", player)
        )
    multiworld.get_location("Olympus Coliseum Coliseum Gates Green Trinity"                                , player).access_rule = lambda state: (
            state.has("Green Trinity", player)
        )
    multiworld.get_location("Olympus Coliseum Coliseum Gates Hero's License Event"                         , player).access_rule = lambda state: (
            state.has("Entry Pass", player)
        )
    multiworld.get_location("Deep Jungle Cavern of Hearts Navi-G Piece Event"                              , player).access_rule = lambda state: (
            state.has("Slides", player)
        )
    multiworld.get_location("Wonderland Bizarre Room Navi-G Piece Event"                                   , player).access_rule = lambda state: (
            state.has("Footprints", player)
        )
    multiworld.get_location("Traverse Town Synth Log"                                                      , player).access_rule = lambda state: (
            state.has("Empty Bottle", player, 6)
            and
            (
                state.has("Green Trinity", player)
                or state.has("High Jump", player, 3)
            )
        )
    multiworld.get_location("Traverse Town Synth Cloth"                                                    , player).access_rule = lambda state: (
            state.has("Empty Bottle", player, 6)
            and
            (
                state.has("Green Trinity", player)
                or state.has("High Jump", player, 3)
            )
        )
    multiworld.get_location("Traverse Town Synth Rope"                                                     , player).access_rule = lambda state: (
            state.has("Empty Bottle", player, 6)
            and
            (
                state.has("Green Trinity", player)
                or state.has("High Jump", player, 3)
            )
        )
    multiworld.get_location("Traverse Town Synth Seagull Egg"                                              , player).access_rule = lambda state: (
            state.has("Empty Bottle", player, 6)
            and
            (
                state.has("Green Trinity", player)
                or state.has("High Jump", player, 3)
            )
        )
    multiworld.get_location("Traverse Town Synth Fish"                                                     , player).access_rule = lambda state: (
            state.has("Empty Bottle", player, 6)
            and
            (
                state.has("Green Trinity", player)
                or state.has("High Jump", player, 3)
            )
        )
    multiworld.get_location("Traverse Town Synth Mushroom"                                                 , player).access_rule = lambda state: (
            state.has("Empty Bottle", player, 6)
            and
            (
                state.has("Green Trinity", player)
                or state.has("High Jump", player, 3)
            )
        )
    multiworld.get_location("Traverse Town Gizmo Shop Postcard 1"                                          , player).access_rule = lambda state: (
            state.has("Progressive Thunder", player)
        )
    multiworld.get_location("Traverse Town Gizmo Shop Postcard 2"                                          , player).access_rule = lambda state: (
            state.has("Progressive Thunder", player)
        )
    multiworld.get_location("Traverse Town Item Workshop Postcard"                                         , player).access_rule = lambda state: (
            state.has("Green Trinity", player)
            or state.has("High Jump", player, 3)
        )
    multiworld.get_location("Traverse Town Geppetto's House Postcard"                                      , player).access_rule = lambda state: (
            state.has("Monstro", player)
            and
            (
                state.has("High Jump", player)
                or (options.advanced_logic and state.has("Progressive Glide", player))
            )
            and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Hollow Bastion Entrance Hall Emblem Piece (Flame)"                            , player).access_rule = lambda state: (
            (
                state.has("Theon Vol. 6", player)
                or state.has("High Jump", player, 3)
                or has_emblems(state, player, options.keyblades_unlock_chests)
            )
            and state.has("Progressive Fire", player)
            and
            (
                state.has("High Jump", player)
                or state.has("Progressive Glide", player)
                or state.has("Progressive Thunder", player)
                or options.advanced_logic
            )
        )
    multiworld.get_location("Hollow Bastion Entrance Hall Emblem Piece (Chest)"                            , player).access_rule = lambda state: (
            state.has("Theon Vol. 6", player)
            or state.has("High Jump", player, 3)
            or has_emblems(state, player, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Hollow Bastion Entrance Hall Emblem Piece (Statue)"                           , player).access_rule = lambda state: (
            (
                state.has("Theon Vol. 6", player)
                or state.has("High Jump", player, 3)
                or has_emblems(state, player, options.keyblades_unlock_chests)
            )
            and state.has("Red Trinity", player)
        )
    multiworld.get_location("Hollow Bastion Entrance Hall Emblem Piece (Fountain)"                         , player).access_rule = lambda state: (
            state.has("Theon Vol. 6", player)
            or state.has("High Jump", player, 3)
            or has_emblems(state, player, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Hollow Bastion Library Speak to Belle Divine Rose"                            , player).access_rule = lambda state: (
            has_emblems(state, player, options.keyblades_unlock_chests)
        )
    multiworld.get_location("Hollow Bastion Library Speak to Aerith Cure"                                  , player).access_rule = lambda state: (
            has_emblems(state, player, options.keyblades_unlock_chests)
        )
    if options.hundred_acre_wood:
        multiworld.get_location("100 Acre Wood Meadow Inside Log Chest"                                    , player).access_rule = lambda state: (
                has_keyblade(state, player, options.keyblades_unlock_chests, "Oathkeeper")
            )
        multiworld.get_location("100 Acre Wood Bouncing Spot Left Cliff Chest"                             , player).access_rule = lambda state: (
                has_torn_pages(state, player, 4)
                and
                (
                    state.has("High Jump", player)
                    or state.has("Progressive Glide", player)
                )
                and has_keyblade(state, player, options.keyblades_unlock_chests, "Oathkeeper")
            )
        multiworld.get_location("100 Acre Wood Bouncing Spot Right Tree Alcove Chest"                      , player).access_rule = lambda state: (
                has_torn_pages(state, player, 4)
                and
                (
                    state.has("High Jump", player)
                    or state.has("Progressive Glide", player)
                )
                and has_keyblade(state, player, options.keyblades_unlock_chests, "Oathkeeper")
            )
        multiworld.get_location("100 Acre Wood Bouncing Spot Under Giant Pot Chest"                        , player).access_rule = lambda state: (
                has_torn_pages(state, player, 4)
                and has_keyblade(state, player, options.keyblades_unlock_chests, "Oathkeeper")
            )
        multiworld.get_location("100 Acre Wood Bouncing Spot Turn in Rare Nut 1"                           , player).access_rule = lambda state: (
                has_torn_pages(state, player, 4)
            )
        multiworld.get_location("100 Acre Wood Bouncing Spot Turn in Rare Nut 2"                           , player).access_rule = lambda state: (
                has_torn_pages(state, player, 4)
                and
                (
                    state.has("High Jump", player)
                    or state.has("Progressive Glide", player)
                )
            )
        multiworld.get_location("100 Acre Wood Bouncing Spot Turn in Rare Nut 3"                           , player).access_rule = lambda state: (
                has_torn_pages(state, player, 4)
                and
                (
                    state.has("High Jump", player)
                    or state.has("Progressive Glide", player)
                )
            )
        multiworld.get_location("100 Acre Wood Bouncing Spot Turn in Rare Nut 4"                           , player).access_rule = lambda state: (
                has_torn_pages(state, player, 4)
                and
                (
                    state.has("High Jump", player)
                    or state.has("Progressive Glide", player)
                )
            )
        multiworld.get_location("100 Acre Wood Bouncing Spot Turn in Rare Nut 5"                           , player).access_rule = lambda state: (
                has_torn_pages(state, player, 4)
                and
                (
                    state.has("High Jump", player)
                    or state.has("Progressive Glide", player)
                )
            )
        multiworld.get_location("100 Acre Wood Pooh's House Owl Cheer"                                     , player).access_rule = lambda state: (
                has_torn_pages(state, player, 5)
            )
        multiworld.get_location("100 Acre Wood Convert Torn Page 1"                                        , player).access_rule = lambda state: (
                has_torn_pages(state, player, 1)
            )
        multiworld.get_location("100 Acre Wood Convert Torn Page 2"                                        , player).access_rule = lambda state: (
                has_torn_pages(state, player, 2)
            )
        multiworld.get_location("100 Acre Wood Convert Torn Page 3"                                        , player).access_rule = lambda state: (
                has_torn_pages(state, player, 3)
            )
        multiworld.get_location("100 Acre Wood Convert Torn Page 4"                                        , player).access_rule = lambda state: (
                has_torn_pages(state, player, 4)
            )
        multiworld.get_location("100 Acre Wood Convert Torn Page 5"                                        , player).access_rule = lambda state: (
                has_torn_pages(state, player, 5)
            )
        multiworld.get_location("100 Acre Wood Pooh's House Start Fire"                                    , player).access_rule = lambda state: (
                has_torn_pages(state, player, 3)
            )
        multiworld.get_location("100 Acre Wood Bouncing Spot Break Log"                                    , player).access_rule = lambda state: (
                has_torn_pages(state, player, 4)
            )
        multiworld.get_location("100 Acre Wood Bouncing Spot Fall Through Top of Tree Next to Pooh"        , player).access_rule = lambda state: (
                has_torn_pages(state, player, 4)
                and
                (
                    state.has("High Jump", player)
                    or state.has("Progressive Glide", player)
                )
            )
    if options.atlantica:
        multiworld.get_location("Atlantica Ursula's Lair Use Fire on Urchin Chest"                         , player).access_rule = lambda state: (
                state.has("Progressive Fire", player)
                and state.has("Crystal Trident", player)
            )
        multiworld.get_location("Atlantica Triton's Palace White Trinity Chest"                            , player).access_rule = lambda state: (
                state.has("White Trinity", player)
            )
        multiworld.get_location("Atlantica Defeat Ursula I Mermaid Kick Event"                             , player).access_rule = lambda state: (
                has_offensive_magic(state, player)
                and state.has("Crystal Trident", player)
            )
        multiworld.get_location("Atlantica Defeat Ursula II Thunder Event"                                 , player).access_rule = lambda state: (
                state.has("Mermaid Kick", player)
                and has_offensive_magic(state, player)
                and state.has("Crystal Trident", player)
            )
        multiworld.get_location("Atlantica Seal Keyhole Crabclaw Event"                                    , player).access_rule = lambda state: (
                state.has("Mermaid Kick", player)
                and has_offensive_magic(state, player)
                and state.has("Crystal Trident", player)
            )
        multiworld.get_location("Atlantica Undersea Gorge Blizzard Clam"                                   , player).access_rule = lambda state: (
                state.has("Progressive Blizzard", player)
            )
        multiworld.get_location("Atlantica Undersea Valley Fire Clam"                                      , player).access_rule = lambda state: (
                state.has("Progressive Fire", player)
            )
        multiworld.get_location("Atlantica Triton's Palace Thunder Clam"                                   , player).access_rule = lambda state: (
                state.has("Progressive Thunder", player)
            )
        multiworld.get_location("Atlantica Cavern Nook Clam"                                               , player).access_rule = lambda state: (
                state.has("Crystal Trident", player)
            )
        multiworld.get_location("Atlantica Defeat Ursula II Ansem's Report 3"                              , player).access_rule = lambda state: (
                state.has("Mermaid Kick", player)
                and has_offensive_magic(state, player)
                and state.has("Crystal Trident", player)
            )
    if options.cups:
        multiworld.get_location("Olympus Coliseum Defeat Hades Ansem's Report 8"                           , player).access_rule = lambda state: (
                state.has("Phil Cup", player)
                and state.has("Pegasus Cup", player)
                and state.has("Hercules Cup", player)
                and has_x_worlds(state, player, 7, options.keyblades_unlock_chests)
                and has_defensive_tools(state, player)
                and state.has("Entry Pass", player)
            )
        multiworld.get_location("Complete Phil Cup"                                                        , player).access_rule = lambda state: (
                state.has("Phil Cup", player)
                and state.has("Entry Pass", player)
            )
        multiworld.get_location("Complete Phil Cup Solo"                                                   , player).access_rule = lambda state: (
                state.has("Phil Cup", player)
                and state.has("Entry Pass", player)
            )
        multiworld.get_location("Complete Phil Cup Time Trial"                                             , player).access_rule = lambda state: (
                state.has("Phil Cup", player)
                and state.has("Entry Pass", player)
            )
        multiworld.get_location("Complete Pegasus Cup"                                                     , player).access_rule = lambda state: (
                state.has("Pegasus Cup", player)
                and state.has("Entry Pass", player)
            )
        multiworld.get_location("Complete Pegasus Cup Solo"                                                , player).access_rule = lambda state: (
                state.has("Pegasus Cup", player)
                and state.has("Entry Pass", player)
            )
        multiworld.get_location("Complete Pegasus Cup Time Trial"                                          , player).access_rule = lambda state: (
                state.has("Pegasus Cup", player)
                and state.has("Entry Pass", player)
            )
        multiworld.get_location("Complete Hercules Cup"                                                    , player).access_rule = lambda state: (
                state.has("Hercules Cup", player)
                and has_x_worlds(state, player, 4, options.keyblades_unlock_chests)
                and state.has("Entry Pass", player)
            )
        multiworld.get_location("Complete Hercules Cup Solo"                                               , player).access_rule = lambda state: (
                state.has("Hercules Cup", player)
                and has_x_worlds(state, player, 4, options.keyblades_unlock_chests)
                and state.has("Entry Pass", player)
            )
        multiworld.get_location("Complete Hercules Cup Time Trial"                                         , player).access_rule = lambda state: (
                state.has("Hercules Cup", player)
                and has_x_worlds(state, player, 4, options.keyblades_unlock_chests)
                and state.has("Entry Pass", player)
            )
        multiworld.get_location("Complete Hades Cup"                                                       , player).access_rule = lambda state: (
                state.has("Phil Cup", player)
                and state.has("Pegasus Cup", player)
                and state.has("Hercules Cup", player)
                and has_x_worlds(state, player, 7, options.keyblades_unlock_chests)
                and has_defensive_tools(state, player)
                and state.has("Entry Pass", player)
            )
        multiworld.get_location("Complete Hades Cup Solo"                                                  , player).access_rule = lambda state: (
                state.has("Phil Cup", player)
                and state.has("Pegasus Cup", player)
                and state.has("Hercules Cup", player)
                and has_x_worlds(state, player, 7, options.keyblades_unlock_chests)
                and has_defensive_tools(state, player)
                and state.has("Entry Pass", player)
            )
        multiworld.get_location("Complete Hades Cup Time Trial"                                            , player).access_rule = lambda state: (
                state.has("Phil Cup", player)
                and state.has("Pegasus Cup", player)
                and state.has("Hercules Cup", player)
                and has_x_worlds(state, player, 7, options.keyblades_unlock_chests)
                and has_defensive_tools(state, player)
                and state.has("Entry Pass", player)
            )
        multiworld.get_location("Hades Cup Defeat Cloud and Leon Event"                                    , player).access_rule = lambda state: (
                state.has("Phil Cup", player)
                and state.has("Pegasus Cup", player)
                and state.has("Hercules Cup", player)
                and has_x_worlds(state, player, 7, options.keyblades_unlock_chests)
                and has_defensive_tools(state, player)
                and state.has("Entry Pass", player)
            )
        multiworld.get_location("Hades Cup Defeat Yuffie Event"                                            , player).access_rule = lambda state: (
                state.has("Phil Cup", player)
                and state.has("Pegasus Cup", player)
                and state.has("Hercules Cup", player)
                and has_x_worlds(state, player, 7, options.keyblades_unlock_chests)
                and has_defensive_tools(state, player)
                and state.has("Entry Pass", player)
            )
        multiworld.get_location("Hades Cup Defeat Cerberus Event"                                          , player).access_rule = lambda state: (
                state.has("Phil Cup", player)
                and state.has("Pegasus Cup", player)
                and state.has("Hercules Cup", player)
                and has_x_worlds(state, player, 7, options.keyblades_unlock_chests)
                and has_defensive_tools(state, player)
                and state.has("Entry Pass", player)
            )
        multiworld.get_location("Hades Cup Defeat Behemoth Event"                                          , player).access_rule = lambda state: (
                state.has("Phil Cup", player)
                and state.has("Pegasus Cup", player)
                and state.has("Hercules Cup", player)
                and has_x_worlds(state, player, 7, options.keyblades_unlock_chests)
                and has_defensive_tools(state, player)
                and state.has("Entry Pass", player)
            )
        multiworld.get_location("Hades Cup Defeat Hades Event"                                             , player).access_rule = lambda state: (
                state.has("Phil Cup", player)
                and state.has("Pegasus Cup", player)
                and state.has("Hercules Cup", player)
                and has_x_worlds(state, player, 7, options.keyblades_unlock_chests)
                and has_defensive_tools(state, player)
                and state.has("Entry Pass", player)
            )
        multiworld.get_location("Hercules Cup Defeat Cloud Event"                                          , player).access_rule = lambda state: (
                state.has("Hercules Cup", player)
                and has_x_worlds(state, player, 4, options.keyblades_unlock_chests)
                and state.has("Entry Pass", player)
            )
        multiworld.get_location("Hercules Cup Yellow Trinity Event"                                        , player).access_rule = lambda state: (
                state.has("Hercules Cup", player)
                and has_x_worlds(state, player, 4, options.keyblades_unlock_chests)
                and state.has("Entry Pass", player)
            )
        multiworld.get_location("Olympus Coliseum Defeat Ice Titan Diamond Dust Event"                     , player).access_rule = lambda state: (
                state.has("Phil Cup", player)
                and state.has("Pegasus Cup", player)
                and state.has("Hercules Cup", player)
                and has_x_worlds(state, player, 7, options.keyblades_unlock_chests)
                and state.has("Guard", player)
                and has_defensive_tools(state, player)
                and state.has("Entry Pass", player)
            )
        multiworld.get_location("Olympus Coliseum Gates Purple Jar After Defeating Hades"                  , player).access_rule = lambda state: (
                state.has("Phil Cup", player)
                and state.has("Pegasus Cup", player)
                and state.has("Hercules Cup", player)
                and has_x_worlds(state, player, 7, options.keyblades_unlock_chests)
                and has_defensive_tools(state, player)
                and state.has("Entry Pass", player)
            )
        multiworld.get_location("Olympus Coliseum Olympia Chest"                                           , player).access_rule = lambda state: (
                state.has("Phil Cup", player)
                and state.has("Pegasus Cup", player)
                and state.has("Hercules Cup", player)
                and has_x_worlds(state, player, 4, options.keyblades_unlock_chests)
                and state.has("Entry Pass", player)
            )
    if options.super_bosses:
        multiworld.get_location("Neverland Defeat Phantom Stop Event"                                      , player).access_rule = lambda state: (
                state.has("Green Trinity", player)
                and has_all_magic_lvx(state, player, 2)
                and has_defensive_tools(state, player)
                and has_emblems(state, player, options.keyblades_unlock_chests)
            )
        multiworld.get_location("Agrabah Defeat Kurt Zisa Ansem's Report 11"                               , player).access_rule = lambda state: (
                has_emblems(state, player, options.keyblades_unlock_chests)
                and has_x_worlds(state, player, 7, options.keyblades_unlock_chests)
                and has_defensive_tools(state, player)
            )
        multiworld.get_location("Agrabah Defeat Kurt Zisa Zantetsuken Event"                               , player).access_rule = lambda state: (
                has_emblems(state, player, options.keyblades_unlock_chests) and has_x_worlds(state, player, 7, options.keyblades_unlock_chests) and has_defensive_tools(state, player)
            )
    if options.super_bosses or options.goal.current_key == "sephiroth":
        multiworld.get_location("Olympus Coliseum Defeat Sephiroth Ansem's Report 12"                      , player).access_rule = lambda state: (
                state.has("Phil Cup", player)
                and state.has("Pegasus Cup", player)
                and state.has("Hercules Cup", player)
                and has_x_worlds(state, player, 7, options.keyblades_unlock_chests)
                and has_defensive_tools(state, player)
                and state.has("Entry Pass", player)
            )
        multiworld.get_location("Olympus Coliseum Defeat Sephiroth One-Winged Angel Event"                 , player).access_rule = lambda state: (
                state.has("Phil Cup", player)
                and state.has("Pegasus Cup", player)
                and state.has("Hercules Cup", player)
                and has_x_worlds(state, player, 7, options.keyblades_unlock_chests)
                and has_defensive_tools(state, player)
                and state.has("Entry Pass", player)
            )
    if options.super_bosses or options.goal.current_key == "unknown":
        multiworld.get_location("Hollow Bastion Defeat Unknown Ansem's Report 13"                          , player).access_rule = lambda state: (
                has_emblems(state, player, options.keyblades_unlock_chests)
                and has_x_worlds(state, player, 7, options.keyblades_unlock_chests)
                and has_defensive_tools(state, player)
            )
        multiworld.get_location("Hollow Bastion Defeat Unknown EXP Necklace Event"                         , player).access_rule = lambda state: (
                has_emblems(state, player, options.keyblades_unlock_chests) and has_x_worlds(state, player, 7, options.keyblades_unlock_chests)
                and has_defensive_tools(state, player)
            )
    for i in range(options.level_checks):
        multiworld.get_location("Level " + str(i+1).rjust(3,'0')                                           , player).access_rule = lambda state, level_num=i: (
                has_x_worlds(state, player, min(((level_num//10)*2), 8), options.keyblades_unlock_chests)
            )
    if options.goal.current_key == "final_ansem":
        multiworld.get_location("Final Ansem"                                                              , player).access_rule = lambda state: (
                has_final_rest_door(state, player, final_rest_door_requirement, final_rest_door_required_reports, options.keyblades_unlock_chests)
            )

    multiworld.get_entrance("Wonderland"                                                                   , player).access_rule = lambda state: state.has("Wonderland", player)       and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
    multiworld.get_entrance("Olympus Coliseum"                                                             , player).access_rule = lambda state: state.has("Olympus Coliseum", player) and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
    multiworld.get_entrance("Deep Jungle"                                                                  , player).access_rule = lambda state: state.has("Deep Jungle", player)      and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
    multiworld.get_entrance("Agrabah"                                                                      , player).access_rule = lambda state: state.has("Agrabah", player)          and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
    multiworld.get_entrance("Monstro"                                                                      , player).access_rule = lambda state: state.has("Monstro", player)          and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
    if options.atlantica:
        multiworld.get_entrance("Atlantica"                                                                , player).access_rule = lambda state: state.has("Atlantica", player)        and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
    multiworld.get_entrance("Halloween Town"                                                               , player).access_rule = lambda state: state.has("Halloween Town", player)   and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
    multiworld.get_entrance("Neverland"                                                                    , player).access_rule = lambda state: state.has("Neverland", player)        and has_x_worlds(state, player, 3, options.keyblades_unlock_chests)
    multiworld.get_entrance("Hollow Bastion"                                                               , player).access_rule = lambda state: state.has("Hollow Bastion", player)   and has_x_worlds(state, player, 5, options.keyblades_unlock_chests)
    multiworld.get_entrance("End of the World"                                                             , player).access_rule = lambda state: has_x_worlds(state, player, 7, options.keyblades_unlock_chests) and (has_reports(state, player, eotw_required_reports) or state.has("End of the World", player))
    multiworld.get_entrance("100 Acre Wood"                                                                , player).access_rule = lambda state: state.has("Progressive Fire", player)

    multiworld.completion_condition[player] = lambda state: state.has("Victory", player)
