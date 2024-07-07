from BaseClasses import CollectionState, MultiWorld


def has_x_worlds(state: CollectionState, player: int, num_of_worlds: int, keyblades_unlock_chests: bool) -> bool:
    worlds_acquired = 0.0
    worlds =    ["Wonderland", "Olympus Coliseum", "Deep Jungle", "Agrabah",      "Monstro",      "Atlantica", "Halloween Town", "Neverland",  "Hollow Bastion", "End of the World"]
    keyblades = ["Lady Luck",  "Olympia",          "Jungle King", "Three Wishes", "Wishing Star", "Crabclaw",  "Pumpkinhead",    "Fairy Harp", "Divine Rose",    "Oblivion"]
    for i in range(len(worlds)):
        if state.has(worlds[i], player):
            worlds_acquired = worlds_acquired + 0.5
        if (state.has(worlds[i], player) and has_keyblade(state, player, keyblades_unlock_chests, keyblades[i])) or (state.has(worlds[i], player) and worlds[i] == "Atlantica"):
            worlds_acquired = worlds_acquired + 0.5
    return worlds_acquired >= num_of_worlds

def has_slides(state: CollectionState, player: int) -> bool:
    return state.has("Slides", player)

def has_evidence(state: CollectionState, player: int) -> bool:
    return state.has("Footprints", player) #or state.has("Stench", player) or state.has("Claw Marks", player) or state.has("Antenna", player)

def can_glide(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Glide", player) or state.has("Superglide", player)

def has_emblems(state: CollectionState, player: int, keyblades_unlock_chests: bool) -> bool:
    return (
                state.has("Emblem Piece (Flame)", player)
                and state.has("Emblem Piece (Chest)", player)
                and state.has("Emblem Piece (Statue)", player)
                and state.has("Emblem Piece (Fountain)", player)
                and state.has("Hollow Bastion", player)
                and has_x_worlds(state, player, 5, keyblades_unlock_chests)
           )

def has_item(state: CollectionState, player: int, item: str) -> bool:
    return state.has(item, player)

def has_at_least(state: CollectionState, player: int, item: str, x: int) -> bool:
    return state.has(item, player, x)

def has_postcards(state: CollectionState, player: int, postcards_required: int) -> bool:
    postcards_available = 0
    postcards_available = postcards_available + state.count("Postcard", player)
    return postcards_available >= postcards_required

def has_puppies(state: CollectionState, player: int, puppies_required: int) -> bool:
    puppies_available = 0
    for i in range(1,100):
        if state.has("Puppy " + str(i).rjust(2,"0"), player):
            puppies_available = puppies_available + 1
    for i in range(1,34):
        if state.has("Puppies " + str(3*(i-1)+1).rjust(2, "0") + "-" + str(3*(i-1)+3).rjust(2, "0"), player):
            puppies_available = puppies_available + 3
    if state.has("All Puppies", player):
        puppies_available = puppies_available + 99
    return puppies_available >= puppies_required

def has_torn_pages(state: CollectionState, player: int, pages_required: int) -> bool:
    pages_available = 0
    pages_available = pages_available + state.count("Torn Page 1", player)
    pages_available = pages_available + state.count("Torn Page 2", player)
    pages_available = pages_available + state.count("Torn Page 3", player)
    pages_available = pages_available + state.count("Torn Page 4", player)
    pages_available = pages_available + state.count("Torn Page 5", player)
    return pages_available >= pages_required

def has_all_arts(state: CollectionState, player: int) -> bool:
    return state.has_all({"Fire Arts", "Blizzard Arts", "Thunder Arts", "Cure Arts", "Gravity Arts", "Stop Arts", "Aero Arts"}, player)

def has_all_summons(state: CollectionState, player: int) -> bool:
    return state.has("Simba", player) and state.has("Bambi", player) and state.has("Genie", player) \
         and state.has("Dumbo", player) and state.has("Mushu", player) and state.has("Tinker Bell", player)

def has_all_magic_lvx(state: CollectionState, player: int, level) -> bool:
    return state.count("Progressive Fire", player) >= level and state.count("Progressive Blizzard", player) >= level and state.count("Progressive Thunder", player) >= level \
        and state.count("Progressive Cure", player) >= level and state.count("Progressive Gravity", player) >= level and state.count("Progressive Aero", player) >= level \
        and state.count("Progressive Stop", player) >= level

def has_offensive_magic(state: CollectionState, player: int) -> bool:
    return state.has_any({"Progressive Fire", "Progressive Blizzard", "Progressive Thunder", "Progressive Gravity", "Progressive Stop"}, player)

def has_reports(state: CollectionState, player: int, eotw_required_reports: int) -> bool:
    return state.has_group("Reports", player, eotw_required_reports)

def has_final_rest_door(state: CollectionState, player:int, final_rest_door_requirement: str, final_rest_door_required_reports: int, keyblades_unlock_chests: bool):
    if final_rest_door_requirement == "reports":
        return state.has_group("Reports", player, final_rest_door_required_reports)
    if final_rest_door_requirement == "puppies":
        return has_puppies(state, player, 99)
    if final_rest_door_requirement == "postcards":
        return has_postcards(state, player, 10)
    if final_rest_door_requirement == "superbosses":
        return (
                    state.has_all({"Olympus Coliseum", "Neverland", "Agrabah", "Hollow Bastion", "Green Trinity", "Phil Cup", "Pegasus Cup", "Hercules Cup", "Entry Pass"}, player) 
                    and has_emblems(state, player, keyblades_unlock_chests) 
                    and has_all_magic_lvx(state, player, 2) 
                    and has_defensive_tools(state, player) 
                    and has_x_worlds(state, player, 7, keyblades_unlock_chests) 
               )

def has_defensive_tools(state: CollectionState, player: int) -> bool:
    return (state.count("Progressive Cure", player) >= 2 and state.has("Leaf Bracer", player) and state.has("Dodge Roll", player)) and (state.has("Second Chance", player) or state.has("MP Rage", player) or state.count("Progressive Aero", player) >= 2)

def has_keyblade(state: CollectionState, player: int, keyblade_required: bool, item: str) -> bool:
    if keyblade_required:
        return state.has(item, player)
    else:
        return True

def can_dumbo_skip(state: CollectionState, player: int) -> bool:
    return state.has("Dumbo", player) and state.has_any({"Progressive Fire", "Progressive Blizzard", "Progressive Thunder", "Progressive Cure", "Progressive Gravity", "Progressive Stop", "Progressive Aero"}, player)

def has_oogie_manor(state: CollectionState, player: int, advanced_logic: bool) -> bool:
    return (
                has_item(state, player, "Progressive Fire") 
                or (advanced_logic and has_at_least(state, player, "High Jump", 2)) 
                or (advanced_logic and has_item(state, player, "High Jump") and can_glide(state, player))
           )

def set_rules(kh1world):
    multiworld                       = kh1world.multiworld
    player                           = kh1world.player
    options                          = kh1world.options
    eotw_required_reports            = kh1world.determine_reports_required_to_open_end_of_the_world()
    final_rest_door_required_reports = kh1world.determine_reports_required_to_open_final_rest_door()
    final_rest_door_requirement      = kh1world.options.final_rest_door.current_key
    
    #Location rules.
    #Keys
   #multiworld.get_location("Destiny Islands Chest"                                                        , player).access_rule = lambda state: has_item(state, player, "")
    multiworld.get_location("Traverse Town 1st District Candle Puzzle Chest"                               , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Lionheart")
                                                                                                                                                    and has_item(state, player, "Progressive Blizzard")
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
                                                                                                                                                    and has_item(state, player, "Progressive Fire")
                                                                                                                                                    and
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "Yellow Trinity")
                                                                                                                                                        or (options.advanced_logic and has_item(state, player, "High Jump"))
                                                                                                                                                        or has_at_least(state, player, "High Jump", 2)
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Traverse Town Accessory Shop Chest"                                           , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Lionheart")
                                                                                                                                                 )
    multiworld.get_location("Traverse Town Secret Waterway White Trinity Chest"                            , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Lionheart")
                                                                                                                                                    and has_item(state, player, "White Trinity")
                                                                                                                                                 )
    multiworld.get_location("Traverse Town Geppetto's House Chest"                                         , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Lionheart")
                                                                                                                                                    and has_item(state, player, "Monstro")
                                                                                                                                                    and
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "High Jump")
                                                                                                                                                        or (options.advanced_logic and can_glide(state, player))
                                                                                                                                                    )
                                                                                                                                                    and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
                                                                                                                                                 )
    multiworld.get_location("Traverse Town Item Workshop Right Chest"                                      , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Lionheart")
                                                                                                                                                    and
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "Green Trinity")
                                                                                                                                                        or has_at_least(state, player, "High Jump", 3)
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Traverse Town 1st District Blue Trinity Balcony Chest"                        , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Lionheart")
                                                                                                                                                    and
                                                                                                                                                    (
                                                                                                                                                        (has_item(state, player, "Blue Trinity") and can_glide(state, player))
                                                                                                                                                        or (options.advanced_logic and can_glide(state, player))
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Traverse Town Mystical House Glide Chest"                                     , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Lionheart")
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        can_glide(state, player)
                                                                                                                                                        or 
                                                                                                                                                        (
                                                                                                                                                            options.advanced_logic
                                                                                                                                                            and 
                                                                                                                                                            (
                                                                                                                                                                (has_item(state, player, "High Jump") and has_item(state, player, "Yellow Trinity"))
                                                                                                                                                                or has_at_least(state, player, "High Jump", 2)
                                                                                                                                                            )
                                                                                                                                                            and has_item(state, player, "Combo Master")
                                                                                                                                                        )
                                                                                                                                                        or
                                                                                                                                                        (
                                                                                                                                                            options.advanced_logic
                                                                                                                                                            and has_item(state, player, "Mermaid Kick")
                                                                                                                                                        )
                                                                                                                                                    )
                                                                                                                                                    and has_item(state, player, "Progressive Fire")
                                                                                                                                                 )
    multiworld.get_location("Traverse Town Alleyway Behind Crates Chest"                                   , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Lionheart")
                                                                                                                                                    and has_item(state, player, "Red Trinity")
                                                                                                                                                 )
    multiworld.get_location("Traverse Town Item Workshop Left Chest"                                       , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Lionheart")
                                                                                                                                                    and
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "Green Trinity")
                                                                                                                                                        or has_at_least(state, player, "High Jump", 3)
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Traverse Town Secret Waterway Near Stairs Chest"                              , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Lionheart")
                                                                                                                                                 )
    multiworld.get_location("Wonderland Rabbit Hole Green Trinity Chest"                                   , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Lady Luck")
                                                                                                                                                    and has_item(state, player, "Green Trinity")
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
                                                                                                                                                    and has_item(state, player, "Green Trinity")
                                                                                                                                                 )
    multiworld.get_location("Wonderland Queen's Castle Hedge Left Red Chest"                               , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Lady Luck")
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_evidence(state, player)
                                                                                                                                                        or has_item(state, player, "High Jump")
                                                                                                                                                        or can_glide(state, player)
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Wonderland Queen's Castle Hedge Right Blue Chest"                             , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Lady Luck")
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_evidence(state, player)
                                                                                                                                                        or has_item(state, player, "High Jump")
                                                                                                                                                        or can_glide(state, player)
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Wonderland Queen's Castle Hedge Right Red Chest"                              , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Lady Luck")
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_evidence(state, player)
                                                                                                                                                        or has_item(state, player, "High Jump")
                                                                                                                                                        or can_glide(state, player)
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Wonderland Lotus Forest Thunder Plant Chest"                                  , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Lady Luck") 
                                                                                                                                                    and has_item(state, player, "Progressive Thunder") 
                                                                                                                                                    and has_evidence(state, player)
                                                                                                                                                 )
    multiworld.get_location("Wonderland Lotus Forest Through the Painting Thunder Plant Chest"             , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Lady Luck") 
                                                                                                                                                    and has_item(state, player, "Progressive Thunder") 
                                                                                                                                                    and has_evidence(state, player)
                                                                                                                                                 )
    multiworld.get_location("Wonderland Lotus Forest Glide Chest"                                          , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Lady Luck") 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        can_glide(state, player)
                                                                                                                                                        or
                                                                                                                                                        (
                                                                                                                                                            options.advanced_logic
                                                                                                                                                            and (has_item(state, player, "High Jump") or can_dumbo_skip(state, player))
                                                                                                                                                            and has_evidence(state, player)
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
                                                                                                                                                            has_item(state, player, "High Jump") 
                                                                                                                                                            or can_glide(state, player)
                                                                                                                                                        )
                                                                                                                                                        or options.advanced_logic
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Wonderland Bizarre Room Lamp Chest"                                           , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Lady Luck") 
                                                                                                                                                    and has_evidence(state, player)
                                                                                                                                                 )
    multiworld.get_location("Wonderland Tea Party Garden Above Lotus Forest Entrance 2nd Chest"            , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Lady Luck") 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        can_glide(state, player)
                                                                                                                                                        or 
                                                                                                                                                        (
                                                                                                                                                            options.advanced_logic
                                                                                                                                                            and has_item(state, player, "High Jump")
                                                                                                                                                            and has_evidence(state, player)
                                                                                                                                                        )
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Wonderland Tea Party Garden Above Lotus Forest Entrance 1st Chest"            , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Lady Luck") 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        can_glide(state, player)
                                                                                                                                                        or 
                                                                                                                                                        (
                                                                                                                                                            options.advanced_logic
                                                                                                                                                            and has_item(state, player, "High Jump")
                                                                                                                                                            and has_evidence(state, player)
                                                                                                                                                        )
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Wonderland Tea Party Garden Bear and Clock Puzzle Chest"                      , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Lady Luck") 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_evidence(state, player)
                                                                                                                                                        or (options.advanced_logic and can_glide(state, player))
                                                                                                                                                        or has_at_least(state, player, "High Jump", 2)
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Wonderland Tea Party Garden Across From Bizarre Room Entrance Chest"          , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Lady Luck") 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        can_glide(state, player)
                                                                                                                                                        or 
                                                                                                                                                        (
                                                                                                                                                            has_at_least(state, player, "High Jump", 3) 
                                                                                                                                                            and has_evidence(state, player)
                                                                                                                                                        )
                                                                                                                                                        or 
                                                                                                                                                        (
                                                                                                                                                            options.advanced_logic
                                                                                                                                                            and has_item(state, player, "High Jump") 
                                                                                                                                                            and has_evidence(state, player)
                                                                                                                                                            and has_item(state, player, "Combo Master")
                                                                                                                                                        )
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Wonderland Lotus Forest Through the Painting White Trinity Chest"             , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Lady Luck") 
                                                                                                                                                    and has_item(state, player, "White Trinity") 
                                                                                                                                                    and has_evidence(state, player)
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
                                                                                                                                                        has_item(state, player, "High Jump") 
                                                                                                                                                        or can_glide(state, player)
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
                                                                                                                                                    and has_item(state, player, "Blue Trinity")
                                                                                                                                                 )
    multiworld.get_location("Deep Jungle Tunnel Chest"                                                     , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Jungle King")
                                                                                                                                                 )
    multiworld.get_location("Deep Jungle Cavern of Hearts White Trinity Chest"                             , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Jungle King") 
                                                                                                                                                    and has_item(state, player, "White Trinity") 
                                                                                                                                                    and has_slides(state, player)
                                                                                                                                                 )
    multiworld.get_location("Deep Jungle Camp Blue Trinity Chest"                                          , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Jungle King") 
                                                                                                                                                    and has_item(state, player, "Blue Trinity")
                                                                                                                                                 )
    multiworld.get_location("Deep Jungle Tent Chest"                                                       , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Jungle King")
                                                                                                                                                 )
    multiworld.get_location("Deep Jungle Waterfall Cavern Low Chest"                                       , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Jungle King") 
                                                                                                                                                    and has_slides(state, player)
                                                                                                                                                 )
    multiworld.get_location("Deep Jungle Waterfall Cavern Middle Chest"                                    , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Jungle King") 
                                                                                                                                                    and has_slides(state, player)
                                                                                                                                                 )
    multiworld.get_location("Deep Jungle Waterfall Cavern High Wall Chest"                                 , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Jungle King") 
                                                                                                                                                    and has_slides(state, player)
                                                                                                                                                 )
    multiworld.get_location("Deep Jungle Waterfall Cavern High Middle Chest"                               , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Jungle King") 
                                                                                                                                                    and has_slides(state, player)
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
                                                                                                                                                        can_glide(state, player)
                                                                                                                                                        or options.advanced_logic
                                                                                                                                                    )
                                                                                                                                                 )
    if options.hundred_acre_wood:
        multiworld.get_location("100 Acre Wood Meadow Inside Log Chest"                                    , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Oathkeeper")
                                                                                                                                                 )
        multiworld.get_location("100 Acre Wood Bouncing Spot Left Cliff Chest"                             , player).access_rule = lambda state: (
                                                                                                                                                    has_torn_pages(state, player, 4) 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "High Jump") 
                                                                                                                                                        or can_glide(state, player)
                                                                                                                                                    )
                                                                                                                                                    and has_keyblade(state, player, options.keyblades_unlock_chests, "Oathkeeper")
                                                                                                                                                 )
        multiworld.get_location("100 Acre Wood Bouncing Spot Right Tree Alcove Chest"                      , player).access_rule = lambda state: (
                                                                                                                                                    has_torn_pages(state, player, 4) 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "High Jump") 
                                                                                                                                                        or can_glide(state, player)
                                                                                                                                                    )
                                                                                                                                                    and has_keyblade(state, player, options.keyblades_unlock_chests, "Oathkeeper")
                                                                                                                                                 )
        multiworld.get_location("100 Acre Wood Bouncing Spot Under Giant Pot Chest"                        , player).access_rule = lambda state: (
                                                                                                                                                    has_torn_pages(state, player, 4)
                                                                                                                                                    and has_keyblade(state, player, options.keyblades_unlock_chests, "Oathkeeper")
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
                                                                                                                                                        has_item(state, player, "High Jump") 
                                                                                                                                                        or can_glide(state, player)
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
                                                                                                                                                        has_item(state, player, "High Jump")
                                                                                                                                                        or options.advanced_logic
                                                                                                                                                     )
                                                                                                                                                 )
    multiworld.get_location("Agrabah Palace Gates High Close to Palace Chest"                              , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes") 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        (
                                                                                                                                                            has_item(state, player, "High Jump") 
                                                                                                                                                            and can_glide(state, player)
                                                                                                                                                            or
                                                                                                                                                            (
                                                                                                                                                                options.advanced_logic
                                                                                                                                                                and 
                                                                                                                                                                (
                                                                                                                                                                    has_item(state, player, "Combo Master")
                                                                                                                                                                    or can_dumbo_skip(state, player)
                                                                                                                                                                )
                                                                                                                                                            )
                                                                                                                                                        )
                                                                                                                                                        or has_at_least(state, player, "High Jump", 3)
                                                                                                                                                        or (options.advanced_logic and can_glide(state, player))
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Agrabah Storage Green Trinity Chest"                                          , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes") 
                                                                                                                                                    and has_item(state, player, "Green Trinity")
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
                                                                                                                                                        can_glide(state, player)
                                                                                                                                                        or (options.advanced_logic and has_item(state, player, "Combo Master"))
                                                                                                                                                        or (options.advanced_logic and can_dumbo_skip(state, player))
                                                                                                                                                        or has_at_least(state, player, "High Jump", 2)
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
                                                                                                                                                        has_item(state, player, "High Jump") 
                                                                                                                                                        or can_glide(state, player)
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
                                                                                                                                                    and has_item(state, player, "Blue Trinity")
                                                                                                                                                 )
    multiworld.get_location("Agrabah Cave of Wonders Hidden Room Right Chest"                              , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes") 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "Yellow Trinity") 
                                                                                                                                                        or has_item(state, player, "High Jump")
                                                                                                                                                        or (options.advanced_logic and can_glide(state, player))
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Agrabah Cave of Wonders Hidden Room Left Chest"                               , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Three Wishes") 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "Yellow Trinity") 
                                                                                                                                                        or has_item(state, player, "High Jump")
                                                                                                                                                        or (options.advanced_logic and can_glide(state, player))
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
                                                                                                                                                    and has_item(state, player, "White Trinity")
                                                                                                                                                 )
    multiworld.get_location("Monstro Chamber 6 Other Platform Chest"                                       , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star") 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "High Jump")
                                                                                                                                                        or (options.advanced_logic and has_item(state, player, "Combo Master"))
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Monstro Chamber 6 Platform Near Chamber 5 Entrance Chest"                     , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star") 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "High Jump")
                                                                                                                                                        or options.advanced_logic
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Monstro Chamber 6 Raised Area Near Chamber 1 Entrance Chest"                  , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star") 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "High Jump")
                                                                                                                                                        or (options.advanced_logic and has_item(state, player, "Combo Master"))
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Monstro Chamber 6 Low Chest"                                                  , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star")
                                                                                                                                                 )
    if options.atlantica:
        multiworld.get_location("Atlantica Sunken Ship In Flipped Boat Chest"                              , player).access_rule = lambda state: (
                                                                                                                                                    True
                                                                                                                                                 )
        multiworld.get_location("Atlantica Sunken Ship Seabed Chest"                                       , player).access_rule = lambda state: (
                                                                                                                                                    True
                                                                                                                                                 )
        multiworld.get_location("Atlantica Sunken Ship Inside Ship Chest"                                  , player).access_rule = lambda state: (
                                                                                                                                                    True
                                                                                                                                                 )
        multiworld.get_location("Atlantica Ariel's Grotto High Chest"                                      , player).access_rule = lambda state: (
                                                                                                                                                    True
                                                                                                                                                 )
        multiworld.get_location("Atlantica Ariel's Grotto Middle Chest"                                    , player).access_rule = lambda state: (
                                                                                                                                                    True
                                                                                                                                                 )
        multiworld.get_location("Atlantica Ariel's Grotto Low Chest"                                       , player).access_rule = lambda state: (
                                                                                                                                                    True
                                                                                                                                                 )
        multiworld.get_location("Atlantica Ursula's Lair Use Fire on Urchin Chest"                         , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Progressive Fire")
                                                                                                                                                    and has_item(state, player, "Crystal Trident")
                                                                                                                                                 )
        multiworld.get_location("Atlantica Undersea Gorge Jammed by Ariel's Grotto Chest"                  , player).access_rule = lambda state: (
                                                                                                                                                    True
                                                                                                                                                 )
        multiworld.get_location("Atlantica Triton's Palace White Trinity Chest"                            , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "White Trinity")
                                                                                                                                                 )
    multiworld.get_location("Halloween Town Moonlight Hill White Trinity Chest"                            , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead") 
                                                                                                                                                    and has_item(state, player, "White Trinity")
                                                                                                                                                    and has_item(state, player, "Forget-Me-Not")
                                                                                                                                                 )
    multiworld.get_location("Halloween Town Bridge Under Bridge"                                           , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead") 
                                                                                                                                                    and has_item(state, player, "Jack-In-The-Box")
                                                                                                                                                    and has_item(state, player, "Forget-Me-Not")
                                                                                                                                                 )
    multiworld.get_location("Halloween Town Boneyard Tombstone Puzzle Chest"                               , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead")
                                                                                                                                                    and has_item(state, player, "Forget-Me-Not")
                                                                                                                                                 )
    multiworld.get_location("Halloween Town Bridge Right of Gate Chest"                                    , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead") 
                                                                                                                                                    and has_item(state, player, "Jack-In-The-Box") 
                                                                                                                                                    and has_item(state, player, "Forget-Me-Not")
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        can_glide(state, player)
                                                                                                                                                        or options.advanced_logic
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Halloween Town Cemetary Behind Grave Chest"                                   , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead") 
                                                                                                                                                    and has_item(state, player, "Jack-In-The-Box") 
                                                                                                                                                    and has_item(state, player, "Forget-Me-Not")
                                                                                                                                                    and has_oogie_manor(state, player, options)
                                                                                                                                                 )
    multiworld.get_location("Halloween Town Cemetary By Cat Shape Chest"                                   , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead") 
                                                                                                                                                    and has_item(state, player, "Jack-In-The-Box") 
                                                                                                                                                    and has_item(state, player, "Forget-Me-Not")
                                                                                                                                                    and has_oogie_manor(state, player, options.advanced_logic)
                                                                                                                                                 )
    multiworld.get_location("Halloween Town Cemetary Between Graves Chest"                                 , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead") 
                                                                                                                                                    and has_item(state, player, "Jack-In-The-Box") 
                                                                                                                                                    and has_item(state, player, "Forget-Me-Not")
                                                                                                                                                    and has_oogie_manor(state, player, options.advanced_logic)
                                                                                                                                                 )
    multiworld.get_location("Halloween Town Oogie's Manor Lower Iron Cage Chest"                           , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead") 
                                                                                                                                                    and has_item(state, player, "Jack-In-The-Box") 
                                                                                                                                                    and has_item(state, player, "Forget-Me-Not")
                                                                                                                                                    and has_oogie_manor(state, player, options.advanced_logic)
                                                                                                                                                 )
    multiworld.get_location("Halloween Town Oogie's Manor Upper Iron Cage Chest"                           , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead") 
                                                                                                                                                    and has_item(state, player, "Jack-In-The-Box") 
                                                                                                                                                    and has_item(state, player, "Forget-Me-Not")
                                                                                                                                                    and has_oogie_manor(state, player, options.advanced_logic)
                                                                                                                                                 )
    multiworld.get_location("Halloween Town Oogie's Manor Hollow Chest"                                    , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead") 
                                                                                                                                                    and has_item(state, player, "Jack-In-The-Box") 
                                                                                                                                                    and has_item(state, player, "Forget-Me-Not")
                                                                                                                                                    and has_oogie_manor(state, player, options.advanced_logic)
                                                                                                                                                 )
    multiworld.get_location("Halloween Town Oogie's Manor Grounds Red Trinity Chest"                       , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead") 
                                                                                                                                                    and has_item(state, player, "Jack-In-The-Box") 
                                                                                                                                                    and has_item(state, player, "Forget-Me-Not")
                                                                                                                                                    and has_item(state, player, "Red Trinity")
                                                                                                                                                 )
    multiworld.get_location("Halloween Town Guillotine Square High Tower Chest"                            , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead") 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "High Jump")
                                                                                                                                                        or (options.advanced_logic and can_dumbo_skip(state, player))
                                                                                                                                                        or (options.advanced_logic and can_glide(state, player))
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Halloween Town Guillotine Square Pumpkin Structure Left Chest"                , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead") 
                                                                                                                                                    and
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "High Jump")
                                                                                                                                                        or (options.advanced_logic and can_glide(state, player))
                                                                                                                                                    )
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        can_glide(state, player)
                                                                                                                                                        or (options.advanced_logic and has_item(state, player, "Combo Master"))
                                                                                                                                                        or has_at_least(state, player, "High Jump", 2)
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Halloween Town Oogie's Manor Entrance Steps Chest"                            , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead") 
                                                                                                                                                    and has_item(state, player, "Jack-In-The-Box")
                                                                                                                                                    and has_item(state, player, "Forget-Me-Not")
                                                                                                                                                 )
    multiworld.get_location("Halloween Town Oogie's Manor Inside Entrance Chest"                           , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead") 
                                                                                                                                                    and has_item(state, player, "Jack-In-The-Box")
                                                                                                                                                    and has_item(state, player, "Forget-Me-Not")
                                                                                                                                                 )
    multiworld.get_location("Halloween Town Bridge Left of Gate Chest"                                     , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead") 
                                                                                                                                                    and has_item(state, player, "Jack-In-The-Box") 
                                                                                                                                                    and has_item(state, player, "Forget-Me-Not")
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        can_glide(state, player) 
                                                                                                                                                        or has_item(state, player, "High Jump")
                                                                                                                                                        or options.advanced_logic
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Halloween Town Cemetary By Striped Grave Chest"                               , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead") 
                                                                                                                                                    and has_item(state, player, "Jack-In-The-Box") 
                                                                                                                                                    and has_item(state, player, "Forget-Me-Not")
                                                                                                                                                    and has_oogie_manor(state, player, options.advanced_logic)
                                                                                                                                                 )
    multiworld.get_location("Halloween Town Guillotine Square Under Jack's House Stairs Chest"             , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead")
                                                                                                                                                 )
    multiworld.get_location("Halloween Town Guillotine Square Pumpkin Structure Right Chest"               , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Pumpkinhead") 
                                                                                                                                                    and
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "High Jump")
                                                                                                                                                        or (options.advanced_logic and can_glide(state, player))
                                                                                                                                                    )
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        can_glide(state, player)
                                                                                                                                                        or (options.advanced_logic and has_item(state, player, "Combo Master"))
                                                                                                                                                        or has_at_least(state, player, "High Jump", 2)
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Olympus Coliseum Coliseum Gates Left Behind Columns Chest"                    , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Olympia")
                                                                                                                                                 )
    multiworld.get_location("Olympus Coliseum Coliseum Gates Right Blue Trinity Chest"                     , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Olympia") 
                                                                                                                                                    and has_item(state, player, "Blue Trinity")
                                                                                                                                                 )
    multiworld.get_location("Olympus Coliseum Coliseum Gates Left Blue Trinity Chest"                      , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Olympia") 
                                                                                                                                                    and has_item(state, player, "Blue Trinity")
                                                                                                                                                 )
    multiworld.get_location("Olympus Coliseum Coliseum Gates White Trinity Chest"                          , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Olympia") 
                                                                                                                                                    and has_item(state, player, "White Trinity")
                                                                                                                                                 )
    multiworld.get_location("Olympus Coliseum Coliseum Gates Blizzara Chest"                               , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Olympia") 
                                                                                                                                                    and has_at_least(state, player, "Progressive Blizzard", 2)
                                                                                                                                                 )
    multiworld.get_location("Olympus Coliseum Coliseum Gates Blizzaga Chest"                               , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Olympia") 
                                                                                                                                                    and has_at_least(state, player, "Progressive Blizzard", 3)
                                                                                                                                                 )
    multiworld.get_location("Monstro Mouth Boat Deck Chest"                                                , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star")
                                                                                                                                                 )
    multiworld.get_location("Monstro Mouth High Platform Boat Side Chest"                                  , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star") 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "High Jump") 
                                                                                                                                                        or can_glide(state, player)
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Monstro Mouth High Platform Across from Boat Chest"                           , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star") 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "High Jump") 
                                                                                                                                                        or can_glide(state, player)
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Monstro Mouth Near Ship Chest"                                                , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star")
                                                                                                                                                 )
    multiworld.get_location("Monstro Mouth Green Trinity Top of Boat Chest"                                , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star") 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "High Jump") 
                                                                                                                                                        or can_glide(state, player)
                                                                                                                                                    ) 
                                                                                                                                                    and has_item(state, player, "Green Trinity")
                                                                                                                                                 )
    multiworld.get_location("Monstro Chamber 2 Ground Chest"                                               , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star")
                                                                                                                                                 )
    multiworld.get_location("Monstro Chamber 2 Platform Chest"                                             , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star")
                                                                                                                                                 )
    multiworld.get_location("Monstro Chamber 5 Platform Chest"                                             , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star") 
                                                                                                                                                    and has_item(state, player, "High Jump")
                                                                                                                                                 )
    multiworld.get_location("Monstro Chamber 3 Ground Chest"                                               , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star")
                                                                                                                                                 )
    multiworld.get_location("Monstro Chamber 3 Platform Above Chamber 2 Entrance Chest"                    , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star") 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "High Jump")
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
                                                                                                                                                        has_item(state, player, "High Jump")
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
                                                                                                                                                        has_item(state, player, "High Jump")
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
                                                                                                                                                    and has_item(state, player, "White Trinity") 
                                                                                                                                                    and has_item(state, player, "Green Trinity")
                                                                                                                                                 )
    multiworld.get_location("Neverland Pirate Ship Crows Nest Chest"                                       , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Fairy Harp") 
                                                                                                                                                    and has_item(state, player, "Green Trinity")
                                                                                                                                                 )
    multiworld.get_location("Neverland Hold Yellow Trinity Right Blue Chest"                               , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Fairy Harp") 
                                                                                                                                                    and has_item(state, player, "Yellow Trinity")
                                                                                                                                                 )
    multiworld.get_location("Neverland Hold Yellow Trinity Left Blue Chest"                                , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Fairy Harp") 
                                                                                                                                                    and has_item(state, player, "Yellow Trinity")
                                                                                                                                                 )
    multiworld.get_location("Neverland Galley Chest"                                                       , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Fairy Harp")
                                                                                                                                                 )
    multiworld.get_location("Neverland Cabin Chest"                                                        , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Fairy Harp") 
                                                                                                                                                    and has_item(state, player, "Green Trinity")
                                                                                                                                                 )
    multiworld.get_location("Neverland Hold Flight 1st Chest "                                             , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Fairy Harp") 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "Green Trinity")
                                                                                                                                                        or can_glide(state, player)
                                                                                                                                                        or has_at_least(state, player, "High Jump", 3)
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Neverland Clock Tower Chest"                                                  , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Fairy Harp") 
                                                                                                                                                    and has_item(state, player, "Green Trinity") 
                                                                                                                                                    and has_all_magic_lvx(state, player, 2)
                                                                                                                                                 )
    multiworld.get_location("Neverland Hold Flight 2nd Chest"                                              , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Fairy Harp") 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "Green Trinity")
                                                                                                                                                        or can_glide(state, player)
                                                                                                                                                        or has_at_least(state, player, "High Jump", 3)
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Neverland Hold Yellow Trinity Green Chest"                                    , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Fairy Harp") 
                                                                                                                                                    and has_item(state, player, "Yellow Trinity")
                                                                                                                                                 )
    multiworld.get_location("Neverland Captain's Cabin Chest"                                              , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Fairy Harp") 
                                                                                                                                                    and has_item(state, player, "Green Trinity")
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
                                                                                                                                                        has_item(state, player, "High Jump") 
                                                                                                                                                        or can_glide(state, player) 
                                                                                                                                                        or has_item(state, player, "Progressive Blizzard")
                                                                                                                                                    )
                                                                                                                                                  )
    multiworld.get_location("Hollow Bastion Rising Falls Floating Platform Near Bubble Chest"              , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose") 
                                                                                                                                                    and
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "High Jump") 
                                                                                                                                                        or can_glide(state, player) 
                                                                                                                                                        or has_item(state, player, "Progressive Blizzard")
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Hollow Bastion Rising Falls High Platform Chest"                              , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose") 
                                                                                                                                                    and
                                                                                                                                                    (
                                                                                                                                                        can_glide(state, player)
                                                                                                                                                        or has_item(state, player, "Progressive Blizzard")
                                                                                                                                                        or (options.advanced_logic and has_item(state, player, "Combo Master"))
                                                                                                                                                    )
                                                                                                                                                    and has_emblems(state, player, options.keyblades_unlock_chests)
                                                                                                                                                 )
    multiworld.get_location("Hollow Bastion Castle Gates Gravity Chest"                                    , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose") 
                                                                                                                                                    and has_item(state, player, "Progressive Gravity") 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_emblems(state, player, options.keyblades_unlock_chests)
                                                                                                                                                        or (options.advanced_logic and has_at_least(state, player, "High Jump", 2) and can_glide(state,player))
                                                                                                                                                        or (options.advanced_logic and can_dumbo_skip(state, player) and can_glide(state,player))
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Hollow Bastion Castle Gates Freestanding Pillar Chest"                        , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose") 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_emblems(state, player, options.keyblades_unlock_chests)
                                                                                                                                                        or has_at_least(state, player, "High Jump", 2)
                                                                                                                                                        or (options.advanced_logic and can_dumbo_skip(state, player))
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Hollow Bastion Castle Gates High Pillar Chest"                                , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose") 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_emblems(state, player, options.keyblades_unlock_chests)
                                                                                                                                                        or has_at_least(state, player, "High Jump", 2)
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
                                                                                                                                                    and has_item(state, player, "Progressive Gravity") 
                                                                                                                                                    and has_emblems(state, player, options.keyblades_unlock_chests)
                                                                                                                                                 )
    multiworld.get_location("Hollow Bastion High Tower 1st Gravity Chest"                                  , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose") 
                                                                                                                                                    and has_item(state, player, "Progressive Gravity") 
                                                                                                                                                    and has_emblems(state, player, options.keyblades_unlock_chests)
                                                                                                                                                 )
    multiworld.get_location("Hollow Bastion High Tower Above Sliding Blocks Chest"                         , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose") 
                                                                                                                                                    and has_emblems(state, player, options.keyblades_unlock_chests)
                                                                                                                                                 )
    multiworld.get_location("Hollow Bastion Library Top of Bookshelf Chest"                                , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose")
                                                                                                                                                 )
   #multiworld.get_location("Hollow Bastion Library 1st Floor Turn the Carousel Chest"                     , player).access_rule = lambda state: ()
   #multiworld.get_location("Hollow Bastion Library Top of Bookshelf Turn the Carousel Chest"              , player).access_rule = lambda state: ()
   #multiworld.get_location("Hollow Bastion Library 2nd Floor Turn the Carousel 1st Chest"                 , player).access_rule = lambda state: ()
   #multiworld.get_location("Hollow Bastion Library 2nd Floor Turn the Carousel 2nd Chest"                 , player).access_rule = lambda state: ()
    multiworld.get_location("Hollow Bastion Lift Stop Library Node After High Tower Switch Gravity Chest"  , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose") 
                                                                                                                                                    and has_item(state, player, "Progressive Gravity") 
                                                                                                                                                    and has_emblems(state, player, options.keyblades_unlock_chests)
                                                                                                                                                 )
    multiworld.get_location("Hollow Bastion Lift Stop Library Node Gravity Chest"                          , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose") 
                                                                                                                                                    and has_item(state, player, "Progressive Gravity") 
                                                                                                                                                 )
    multiworld.get_location("Hollow Bastion Lift Stop Under High Tower Sliding Blocks Chest"               , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose") 
                                                                                                                                                    and has_emblems(state, player, options.keyblades_unlock_chests) 
                                                                                                                                                    and can_glide(state, player)
                                                                                                                                                    and has_item(state, player, "Progressive Gravity") 
                                                                                                                                                 )
    multiworld.get_location("Hollow Bastion Lift Stop Outside Library Gravity Chest"                       , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose") 
                                                                                                                                                    and has_item(state, player, "Progressive Gravity") 
                                                                                                                                                 )
    multiworld.get_location("Hollow Bastion Lift Stop Heartless Sigil Door Gravity Chest"                  , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose") 
                                                                                                                                                    and has_item(state, player, "Progressive Gravity") 
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
                                                                                                                                                        (has_item(state, player, "Progressive Blizzard") and has_item(state, player, "High Jump"))
                                                                                                                                                        or has_at_least(state, player, "High Jump", 3)
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
   #multiworld.get_location("Hollow Bastion Entrance Hall Push the Statue Chest"                           , player).access_rule = lambda state: ()
    multiworld.get_location("Hollow Bastion Entrance Hall Left of Emblem Door Chest"                       , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Divine Rose") 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "High Jump")
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
                                                                                                                                                    and has_item(state, player, "White Trinity")
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
                                                                                                                                                    has_item(state, player, "High Jump") or can_glide(state, player) 
                                                                                                                                                    and has_keyblade(state, player, options.keyblades_unlock_chests, "Oblivion")
                                                                                                                                                 )
    multiworld.get_location("End of the World Giant Crevasse 1st Chest"                                    , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Oblivion")
                                                                                                                                                    and
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "High Jump") 
                                                                                                                                                        or can_glide(state, player) 
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("End of the World Giant Crevasse 4th Chest"                                    , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Oblivion") 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        (
                                                                                                                                                            options.advanced_logic
                                                                                                                                                            and has_item(state, player, "High Jump") 
                                                                                                                                                            and has_item(state, player, "Combo Master")
                                                                                                                                                        )
                                                                                                                                                        or can_glide(state, player)
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
                                                                                                                                                        has_item(state, player, "High Jump")
                                                                                                                                                        or 
                                                                                                                                                        (
                                                                                                                                                            options.advanced_logic
                                                                                                                                                            and can_dumbo_skip(state, player)
                                                                                                                                                            and can_glide(state, player)
                                                                                                                                                        )
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("End of the World World Terminus Atlantica Chest"                              , player).access_rule = lambda state: (
                                                                                                                                                    True
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
    multiworld.get_location("End of the World World Terminus Hollow Bastion Chest"                         , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Oblivion")
                                                                                                                                                 )
    multiworld.get_location("End of the World Final Rest Chest"                                            , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Oblivion")
                                                                                                                                                 )
    multiworld.get_location("Monstro Chamber 6 White Trinity Chest"                                        , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Wishing Star") 
                                                                                                                                                    and has_item(state, player, "White Trinity")
                                                                                                                                                 )
   #multiworld.get_location("Awakening Chest"                                                              , player).access_rule = lambda state: has_item(state, player, "")

   #multiworld.get_location("Traverse Town Defeat Guard Armor Dodge Roll Event"                            , player).access_rule = lambda state: has_item(state, player, "")
   #multiworld.get_location("Traverse Town Defeat Guard Armor Fire Event"                                  , player).access_rule = lambda state: has_item(state, player, "")
   #multiworld.get_location("Traverse Town Defeat Guard Armor Blue Trinity Event"                          , player).access_rule = lambda state: has_item(state, player, "")
   #multiworld.get_location("Traverse Town Leon Secret Waterway Earthshine Event"                          , player).access_rule = lambda state: has_item(state, player, "")
    multiworld.get_location("Traverse Town Kairi Secret Waterway Oathkeeper Event"                         , player).access_rule = lambda state: (
                                                                                                                                                    has_emblems(state, player, options.keyblades_unlock_chests) 
                                                                                                                                                    and has_item(state, player,"Hollow Bastion") 
                                                                                                                                                    and has_x_worlds(state, player, 5, options.keyblades_unlock_chests)
                                                                                                                                                 )
   #multiworld.get_location("Traverse Town Defeat Guard Armor Brave Warrior Event"                         , player).access_rule = lambda state: has_item(state, player, "")
    multiworld.get_location("Deep Jungle Defeat Sabor White Fang Event"                                    , player).access_rule = lambda state: (
                                                                                                                                                    has_slides(state, player)
                                                                                                                                                 )
    multiworld.get_location("Deep Jungle Defeat Clayton Cure Event"                                        , player).access_rule = lambda state: (
                                                                                                                                                    has_slides(state, player)
                                                                                                                                                 )
    multiworld.get_location("Deep Jungle Seal Keyhole Jungle King Event"                                   , player).access_rule = lambda state: (
                                                                                                                                                    has_slides(state, player)
                                                                                                                                                 )
    multiworld.get_location("Deep Jungle Seal Keyhole Red Trinity Event"                                   , player).access_rule = lambda state: (
                                                                                                                                                    has_slides(state, player)
                                                                                                                                                 )
   #multiworld.get_location("Olympus Coliseum Clear Phil's Training Thunder Event"                         , player).access_rule = lambda state: has_item(state, player, "")
    multiworld.get_location("Olympus Coliseum Defeat Cerberus Inferno Band Event"                          , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Entry Pass")
                                                                                                                                                 )
    multiworld.get_location("Olympus Coliseum Cloud Sonic Blade Event"                                     , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Entry Pass")
                                                                                                                                                 )
    multiworld.get_location("Wonderland Defeat Trickmaster Blizzard Event"                                 , player).access_rule = lambda state: (
                                                                                                                                                    has_evidence(state, player)
                                                                                                                                                 )
    multiworld.get_location("Wonderland Defeat Trickmaster Ifrit's Horn Event"                             , player).access_rule = lambda state: (
                                                                                                                                                    has_evidence(state, player)
                                                                                                                                                 )
   #multiworld.get_location("Agrabah Defeat Pot Centipede Ray of Light Event"                              , player).access_rule = lambda state: has_item(state, player, "")
   #multiworld.get_location("Agrabah Defeat Jafar Blizzard Event"                                          , player).access_rule = lambda state: has_item(state, player, "")
   #multiworld.get_location("Agrabah Defeat Jafar Genie Fire Event"                                        , player).access_rule = lambda state: has_item(state, player, "")
   #multiworld.get_location("Agrabah Seal Keyhole Genie Event"                                             , player).access_rule = lambda state: has_item(state, player, "")
   #multiworld.get_location("Agrabah Seal Keyhole Three Wishes Event"                                      , player).access_rule = lambda state: has_item(state, player, "")
   #multiworld.get_location("Agrabah Seal Keyhole Green Trinity Event"                                     , player).access_rule = lambda state: has_item(state, player, "")
   #multiworld.get_location("Monstro Defeat Parasite Cage I Goofy Cheer Event"                             , player).access_rule = lambda state: has_item(state, player, "")
    multiworld.get_location("Monstro Defeat Parasite Cage II Stop Event"                                   , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "High Jump")
                                                                                                                                                    or
                                                                                                                                                    (
                                                                                                                                                        options.advanced_logic
                                                                                                                                                        and can_glide(state, player)
                                                                                                                                                    )
                                                                                                                                                 )
    if options.atlantica:
        multiworld.get_location("Atlantica Defeat Ursula I Mermaid Kick Event"                             , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Crabclaw") 
                                                                                                                                                    and has_offensive_magic(state, player)
                                                                                                                                                    and has_item(state, player, "Crystal Trident")
                                                                                                                                                 )
        multiworld.get_location("Atlantica Defeat Ursula II Thunder Event"                                 , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Crabclaw") 
                                                                                                                                                    and has_item(state, player, "Mermaid Kick") 
                                                                                                                                                    and has_offensive_magic(state, player)
                                                                                                                                                    and has_item(state, player, "Crystal Trident")
                                                                                                                                                 )
        multiworld.get_location("Atlantica Seal Keyhole Crabclaw Event"                                    , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Crabclaw") 
                                                                                                                                                    and has_item(state, player, "Mermaid Kick") 
                                                                                                                                                    and has_offensive_magic(state, player)
                                                                                                                                                    and has_item(state, player, "Crystal Trident")
                                                                                                                                                 )
    multiworld.get_location("Halloween Town Defeat Oogie Boogie Holy Circlet Event"                        , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Jack-In-The-Box") 
                                                                                                                                                    and has_item(state, player, "Forget-Me-Not")
                                                                                                                                                    and has_oogie_manor(state, player, options.advanced_logic)
                                                                                                                                                 )
    multiworld.get_location("Halloween Town Defeat Oogie's Manor Gravity Event"                            , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Jack-In-The-Box") 
                                                                                                                                                    and has_item(state, player, "Forget-Me-Not")
                                                                                                                                                    and has_oogie_manor(state, player, options.advanced_logic)
                                                                                                                                                 )
    multiworld.get_location("Halloween Town Seal Keyhole Pumpkinhead Event"                                , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Jack-In-The-Box") 
                                                                                                                                                    and has_item(state, player, "Forget-Me-Not")
                                                                                                                                                    and has_oogie_manor(state, player, options.advanced_logic)
                                                                                                                                                 )
    multiworld.get_location("Neverland Defeat Anti Sora Raven's Claw Event"                                , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Green Trinity")
                                                                                                                                                 )
    multiworld.get_location("Neverland Encounter Hook Cure Event"                                          , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Green Trinity")
                                                                                                                                                 )
    multiworld.get_location("Neverland Seal Keyhole Fairy Harp Event"                                      , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Green Trinity")
                                                                                                                                                 )
    multiworld.get_location("Neverland Seal Keyhole Tinker Bell Event"                                     , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Green Trinity")
                                                                                                                                                 )
    multiworld.get_location("Neverland Seal Keyhole Glide Event"                                           , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Green Trinity")
                                                                                                                                                 )
    if options.super_bosses:
        multiworld.get_location("Neverland Defeat Phantom Stop Event"                                      , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Green Trinity") 
                                                                                                                                                    and has_all_magic_lvx(state, player, 2) 
                                                                                                                                                    and has_defensive_tools(state, player) 
                                                                                                                                                    and has_emblems(state, player, options.keyblades_unlock_chests)
                                                                                                                                                 )
    multiworld.get_location("Neverland Defeat Captain Hook Ars Arcanum Event"                              , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Green Trinity")
                                                                                                                                                 )
   #multiworld.get_location("Hollow Bastion Defeat Riku I White Trinity Event"                             , player).access_rule = lambda state: has_item(state, player, "")
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
   #multiworld.get_location("End of the World Defeat Chernabog Superglide Event"                           , player).access_rule = lambda state: has_item(state, player, "")
    
    multiworld.get_location("Traverse Town Mail Postcard 01 Event"                                         , player).access_rule = lambda state: (
                                                                                                                                                    has_postcards(state, player, 1)
                                                                                                                                                 )
    multiworld.get_location("Traverse Town Mail Postcard 02 Event"                                         , player).access_rule = lambda state: (
                                                                                                                                                    has_postcards(state, player, 2)
                                                                                                                                                 )
    multiworld.get_location("Traverse Town Mail Postcard 03 Event"                                         , player).access_rule = lambda state: (
                                                                                                                                                    has_postcards(state, player, 3)
                                                                                                                                                 )
    multiworld.get_location("Traverse Town Mail Postcard 04 Event"                                         , player).access_rule = lambda state: (
                                                                                                                                                    has_postcards(state, player, 4)
                                                                                                                                                 )
    multiworld.get_location("Traverse Town Mail Postcard 05 Event"                                         , player).access_rule = lambda state: (
                                                                                                                                                    has_postcards(state, player, 5)
                                                                                                                                                 )
    multiworld.get_location("Traverse Town Mail Postcard 06 Event"                                         , player).access_rule = lambda state: (
                                                                                                                                                    has_postcards(state, player, 6)
                                                                                                                                                 )
    multiworld.get_location("Traverse Town Mail Postcard 07 Event"                                         , player).access_rule = lambda state: (
                                                                                                                                                    has_postcards(state, player, 7)
                                                                                                                                                 )
    multiworld.get_location("Traverse Town Mail Postcard 08 Event"                                         , player).access_rule = lambda state: (
                                                                                                                                                    has_postcards(state, player, 8)
                                                                                                                                                 )
    multiworld.get_location("Traverse Town Mail Postcard 09 Event"                                         , player).access_rule = lambda state: (
                                                                                                                                                    has_postcards(state, player, 9)
                                                                                                                                                 )
    multiworld.get_location("Traverse Town Mail Postcard 10 Event"                                         , player).access_rule = lambda state: (
                                                                                                                                                    has_postcards(state, player, 10)
                                                                                                                                                 )
    
    multiworld.get_location("Traverse Town Defeat Opposite Armor Aero Event"                               , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Red Trinity")
                                                                                                                                                 )
    
    if options.atlantica:
        multiworld.get_location("Atlantica Undersea Gorge Blizzard Clam"                                   , player).access_rule = lambda state: has_item(state, player, "Progressive Blizzard")
       #multiworld.get_location("Atlantica Undersea Gorge Ocean Floor Clam"                                , player).access_rule = lambda state: has_item(state, player, "")
       #multiworld.get_location("Atlantica Undersea Valley Higher Cave Clam"                               , player).access_rule = lambda state: has_item(state, player, "")
       #multiworld.get_location("Atlantica Undersea Valley Lower Cave Clam"                                , player).access_rule = lambda state: has_item(state, player, "")
        multiworld.get_location("Atlantica Undersea Valley Fire Clam"                                      , player).access_rule = lambda state: has_item(state, player, "Progressive Fire")
       #multiworld.get_location("Atlantica Undersea Valley Wall Clam"                                      , player).access_rule = lambda state: has_item(state, player, "")
       #multiworld.get_location("Atlantica Undersea Valley Pillar Clam"                                    , player).access_rule = lambda state: has_item(state, player, "")
       #multiworld.get_location("Atlantica Undersea Valley Ocean Floor Clam"                               , player).access_rule = lambda state: has_item(state, player, "")
        multiworld.get_location("Atlantica Triton's Palace Thunder Clam"                                   , player).access_rule = lambda state: has_item(state, player, "Progressive Thunder")
       #multiworld.get_location("Atlantica Triton's Palace Wall Right Clam"                                , player).access_rule = lambda state: has_item(state, player, "")
       #multiworld.get_location("Atlantica Triton's Palace Near Path Clam"                                 , player).access_rule = lambda state: has_item(state, player, "")
       #multiworld.get_location("Atlantica Triton's Palace Wall Left Clam"                                 , player).access_rule = lambda state: has_item(state, player, "")
        multiworld.get_location("Atlantica Cavern Nook Clam"                                               , player).access_rule = lambda state: has_item(state, player, "Crystal Trident")
       #multiworld.get_location("Atlantica Below Deck Clam"                                                , player).access_rule = lambda state: has_item(state, player, "")
       #multiworld.get_location("Atlantica Undersea Garden Clam"                                           , player).access_rule = lambda state: has_item(state, player, "")
       #multiworld.get_location("Atlantica Undersea Cave Clam"                                             , player).access_rule = lambda state: has_item(state, player, "")

   #multiworld.get_location("Agrabah Defeat Jafar Genie Ansem's Report 1"                                  , player).access_rule = lambda state: has_item(state, player, "")
    multiworld.get_location("Hollow Bastion Speak with Aerith Ansem's Report 2"                            , player).access_rule = lambda state: (
                                                                                                                                                    has_emblems(state, player, options.keyblades_unlock_chests)
                                                                                                                                                 )
    if options.atlantica:
        multiworld.get_location("Atlantica Defeat Ursula II Ansem's Report 3"                              , player).access_rule = lambda state: (
                                                                                                                                                    has_keyblade(state, player, options.keyblades_unlock_chests, "Crabclaw") 
                                                                                                                                                    and has_item(state, player, "Mermaid Kick") 
                                                                                                                                                    and has_offensive_magic(state, player)
                                                                                                                                                    and has_item(state, player, "Crystal Trident")
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
                                                                                                                                                    has_item(state, player, "Jack-In-The-Box") 
                                                                                                                                                    and has_item(state, player, "Forget-Me-Not")
                                                                                                                                                    and has_item(state, player, "Progressive Fire")
                                                                                                                                                 )
    if options.cups:
        multiworld.get_location("Olympus Coliseum Defeat Hades Ansem's Report 8"                           , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Phil Cup") 
                                                                                                                                                    and has_item(state, player, "Pegasus Cup") 
                                                                                                                                                    and has_item(state, player, "Hercules Cup") 
                                                                                                                                                    and has_x_worlds(state, player, 7, options.keyblades_unlock_chests) 
                                                                                                                                                    and has_defensive_tools(state, player)
                                                                                                                                                    and has_item(state, player, "Entry Pass")
                                                                                                                                                 )
    multiworld.get_location("Neverland Defeat Hook Ansem's Report 9"                                       , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Green Trinity")
                                                                                                                                                 )
    multiworld.get_location("Hollow Bastion Speak with Aerith Ansem's Report 10"                           , player).access_rule = lambda state: (
                                                                                                                                                    has_emblems(state, player, options.keyblades_unlock_chests)
                                                                                                                                                 )
    if options.super_bosses:
        multiworld.get_location("Agrabah Defeat Kurt Zisa Ansem's Report 11"                               , player).access_rule = lambda state: (
                                                                                                                                                    has_emblems(state, player, options.keyblades_unlock_chests) 
                                                                                                                                                    and has_x_worlds(state, player, 7, options.keyblades_unlock_chests) 
                                                                                                                                                    and has_defensive_tools(state, player)
                                                                                                                                                 )
    if options.super_bosses or options.goal.current_key == "sephiroth":
        multiworld.get_location("Olympus Coliseum Defeat Sephiroth Ansem's Report 12"                      , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Phil Cup") 
                                                                                                                                                    and has_item(state, player, "Pegasus Cup") 
                                                                                                                                                    and has_item(state, player, "Hercules Cup") 
                                                                                                                                                    and has_x_worlds(state, player, 7, options.keyblades_unlock_chests) 
                                                                                                                                                    and has_defensive_tools(state, player)
                                                                                                                                                    and has_item(state, player, "Entry Pass")
                                                                                                                                                 )
    if options.super_bosses or options.goal.current_key == "unknown":
        multiworld.get_location("Hollow Bastion Defeat Unknown Ansem's Report 13"                          , player).access_rule = lambda state: (
                                                                                                                                                    has_emblems(state, player, options.keyblades_unlock_chests) 
                                                                                                                                                    and has_x_worlds(state, player, 7, options.keyblades_unlock_chests) 
                                                                                                                                                    and has_defensive_tools(state, player)
                                                                                                                                                 )

    if options.cups:
        multiworld.get_location("Complete Phil Cup"                                                        , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Phil Cup")
                                                                                                                                                    and has_item(state, player, "Entry Pass")
                                                                                                                                                 )
        multiworld.get_location("Complete Phil Cup Solo"                                                   , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Phil Cup")
                                                                                                                                                    and has_item(state, player, "Entry Pass")
                                                                                                                                                 )
        multiworld.get_location("Complete Phil Cup Time Trial"                                             , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Phil Cup")
                                                                                                                                                    and has_item(state, player, "Entry Pass")
                                                                                                                                                 )
        multiworld.get_location("Complete Pegasus Cup"                                                     , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Pegasus Cup")
                                                                                                                                                    and has_item(state, player, "Entry Pass")
                                                                                                                                                 )
        multiworld.get_location("Complete Pegasus Cup Solo"                                                , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Pegasus Cup")
                                                                                                                                                    and has_item(state, player, "Entry Pass")
                                                                                                                                                 )
        multiworld.get_location("Complete Pegasus Cup Time Trial"                                          , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Pegasus Cup")
                                                                                                                                                    and has_item(state, player, "Entry Pass")
                                                                                                                                                 )
        multiworld.get_location("Complete Hercules Cup"                                                    , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Hercules Cup") 
                                                                                                                                                    and has_x_worlds(state, player, 4, options.keyblades_unlock_chests)
                                                                                                                                                    and has_item(state, player, "Entry Pass")
                                                                                                                                                 )
        multiworld.get_location("Complete Hercules Cup Solo"                                               , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Hercules Cup") 
                                                                                                                                                    and has_x_worlds(state, player, 4, options.keyblades_unlock_chests)
                                                                                                                                                    and has_item(state, player, "Entry Pass")
                                                                                                                                                 )
        multiworld.get_location("Complete Hercules Cup Time Trial"                                         , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Hercules Cup") 
                                                                                                                                                    and has_x_worlds(state, player, 4, options.keyblades_unlock_chests)
                                                                                                                                                    and has_item(state, player, "Entry Pass")
                                                                                                                                                 )
        multiworld.get_location("Complete Hades Cup"                                                       , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Phil Cup") 
                                                                                                                                                    and has_item(state, player, "Pegasus Cup") 
                                                                                                                                                    and has_item(state, player, "Hercules Cup") 
                                                                                                                                                    and has_x_worlds(state, player, 7, options.keyblades_unlock_chests) 
                                                                                                                                                    and has_defensive_tools(state, player)
                                                                                                                                                    and has_item(state, player, "Entry Pass")
                                                                                                                                                 )
        multiworld.get_location("Complete Hades Cup Solo"                                                  , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Phil Cup") 
                                                                                                                                                    and has_item(state, player, "Pegasus Cup") 
                                                                                                                                                    and has_item(state, player, "Hercules Cup") 
                                                                                                                                                    and has_x_worlds(state, player, 7, options.keyblades_unlock_chests) 
                                                                                                                                                    and has_defensive_tools(state, player)
                                                                                                                                                    and has_item(state, player, "Entry Pass")
                                                                                                                                                 )
        multiworld.get_location("Complete Hades Cup Time Trial"                                            , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Phil Cup") 
                                                                                                                                                    and has_item(state, player, "Pegasus Cup") 
                                                                                                                                                    and has_item(state, player, "Hercules Cup") 
                                                                                                                                                    and has_x_worlds(state, player, 7, options.keyblades_unlock_chests) 
                                                                                                                                                    and has_defensive_tools(state, player)
                                                                                                                                                    and has_item(state, player, "Entry Pass")
                                                                                                                                                 )
        multiworld.get_location("Hades Cup Defeat Cloud and Leon Event"                                    , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Phil Cup") 
                                                                                                                                                    and has_item(state, player, "Pegasus Cup") 
                                                                                                                                                    and has_item(state, player, "Hercules Cup") 
                                                                                                                                                    and has_x_worlds(state, player, 7, options.keyblades_unlock_chests) 
                                                                                                                                                    and has_defensive_tools(state, player)
                                                                                                                                                    and has_item(state, player, "Entry Pass")
                                                                                                                                                 )
        multiworld.get_location("Hades Cup Defeat Yuffie Event"                                            , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Phil Cup") 
                                                                                                                                                    and has_item(state, player, "Pegasus Cup") 
                                                                                                                                                    and has_item(state, player, "Hercules Cup") 
                                                                                                                                                    and has_x_worlds(state, player, 7, options.keyblades_unlock_chests) 
                                                                                                                                                    and has_defensive_tools(state, player)
                                                                                                                                                    and has_item(state, player, "Entry Pass")
                                                                                                                                                 )
        multiworld.get_location("Hades Cup Defeat Cerberus Event"                                          , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Phil Cup") 
                                                                                                                                                    and has_item(state, player, "Pegasus Cup") 
                                                                                                                                                    and has_item(state, player, "Hercules Cup") 
                                                                                                                                                    and has_x_worlds(state, player, 7, options.keyblades_unlock_chests) 
                                                                                                                                                    and has_defensive_tools(state, player)
                                                                                                                                                    and has_item(state, player, "Entry Pass")
                                                                                                                                                 )
        multiworld.get_location("Hades Cup Defeat Behemoth Event"                                          , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Phil Cup") 
                                                                                                                                                    and has_item(state, player, "Pegasus Cup") 
                                                                                                                                                    and has_item(state, player, "Hercules Cup") 
                                                                                                                                                    and has_x_worlds(state, player, 7, options.keyblades_unlock_chests) 
                                                                                                                                                    and has_defensive_tools(state, player)
                                                                                                                                                    and has_item(state, player, "Entry Pass")
                                                                                                                                                 )
        multiworld.get_location("Hades Cup Defeat Hades Event"                                             , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Phil Cup") 
                                                                                                                                                    and has_item(state, player, "Pegasus Cup") 
                                                                                                                                                    and has_item(state, player, "Hercules Cup") 
                                                                                                                                                    and has_x_worlds(state, player, 7, options.keyblades_unlock_chests) 
                                                                                                                                                    and has_defensive_tools(state, player)
                                                                                                                                                    and has_item(state, player, "Entry Pass")
                                                                                                                                                 )
        multiworld.get_location("Hercules Cup Defeat Cloud Event"                                          , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Hercules Cup") 
                                                                                                                                                    and has_x_worlds(state, player, 4, options.keyblades_unlock_chests)
                                                                                                                                                    and has_item(state, player, "Entry Pass")
                                                                                                                                                 )
        multiworld.get_location("Hercules Cup Yellow Trinity Event"                                        , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Hercules Cup") 
                                                                                                                                                    and has_x_worlds(state, player, 4, options.keyblades_unlock_chests)
                                                                                                                                                    and has_item(state, player, "Entry Pass")
                                                                                                                                                 )
        
   #multiworld.get_location("Traverse Town Magician's Study Turn in Naturespark"                           , player).access_rule = lambda state: has_item(state, player, "Naturespark") and has_item(state, player, "Progressive Fire")
   #multiworld.get_location("Traverse Town Magician's Study Turn in Watergleam"                            , player).access_rule = lambda state: has_item(state, player, "Watergleam") and has_item(state, player, "Progressive Fire")
   #multiworld.get_location("Traverse Town Magician's Study Turn in Fireglow"                              , player).access_rule = lambda state: has_item(state, player, "Fireglow") and has_item(state, player, "Progressive Fire")
   #multiworld.get_location("Traverse Town Magician's Study Turn in all Summon Gems"                       , player).access_rule = lambda state: has_item(state, player, "Naturespark") and has_item(state, player, "Watergleam") and has_item(state, player, "Fireglow") and has_item(state, player, "Progressive Fire")
    multiworld.get_location("Traverse Town Geppetto's House Geppetto Reward 1"                             , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Monstro") 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "High Jump")
                                                                                                                                                        or (options.advanced_logic and can_glide(state, player))
                                                                                                                                                    )
                                                                                                                                                    and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
                                                                                                                                                 )
    multiworld.get_location("Traverse Town Geppetto's House Geppetto Reward 2"                             , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Monstro") 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "High Jump")
                                                                                                                                                        or (options.advanced_logic and can_glide(state, player))
                                                                                                                                                    )
                                                                                                                                                    and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
                                                                                                                                                 )
    multiworld.get_location("Traverse Town Geppetto's House Geppetto Reward 3"                             , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Monstro") 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "High Jump")
                                                                                                                                                        or (options.advanced_logic and can_glide(state, player))
                                                                                                                                                    )
                                                                                                                                                    and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
                                                                                                                                                 )
    multiworld.get_location("Traverse Town Geppetto's House Geppetto Reward 4"                             , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Monstro") 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "High Jump")
                                                                                                                                                        or (options.advanced_logic and can_glide(state, player))
                                                                                                                                                    )
                                                                                                                                                    and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
                                                                                                                                                 )
    multiworld.get_location("Traverse Town Geppetto's House Geppetto Reward 5"                             , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Monstro") 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "High Jump")
                                                                                                                                                        or (options.advanced_logic and can_glide(state, player))
                                                                                                                                                    )
                                                                                                                                                    and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
                                                                                                                                                 )
    multiworld.get_location("Traverse Town Geppetto's House Geppetto All Summons Reward"                   , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Monstro") 
                                                                                                                                                    and
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "High Jump")
                                                                                                                                                        or (options.advanced_logic and can_glide(state, player))
                                                                                                                                                    )
                                                                                                                                                    and has_all_summons(state, player)
                                                                                                                                                    and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
                                                                                                                                                 )
    multiworld.get_location("Traverse Town Geppetto's House Talk to Pinocchio"                             , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Monstro") 
                                                                                                                                                    and
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "High Jump")
                                                                                                                                                        or (options.advanced_logic and can_glide(state, player))
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
    if options.super_bosses or options.goal.current_key == "sephiroth":
        multiworld.get_location("Olympus Coliseum Defeat Sephiroth One-Winged Angel Event"                 , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Phil Cup") 
                                                                                                                                                    and has_item(state, player, "Pegasus Cup") 
                                                                                                                                                    and has_item(state, player, "Hercules Cup") 
                                                                                                                                                    and has_x_worlds(state, player, 7, options.keyblades_unlock_chests) 
                                                                                                                                                    and has_defensive_tools(state, player)
                                                                                                                                                    and has_item(state, player, "Entry Pass")
                                                                                                                                                 )
    if options.cups:
        multiworld.get_location("Olympus Coliseum Defeat Ice Titan Diamond Dust Event"                     , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Phil Cup") 
                                                                                                                                                    and has_item(state, player, "Pegasus Cup") 
                                                                                                                                                    and has_item(state, player, "Hercules Cup") 
                                                                                                                                                    and has_x_worlds(state, player, 7, options.keyblades_unlock_chests) 
                                                                                                                                                    and has_item(state, player, "Guard") 
                                                                                                                                                    and has_defensive_tools(state, player)
                                                                                                                                                    and has_item(state, player, "Entry Pass")
                                                                                                                                                 )
        multiworld.get_location("Olympus Coliseum Gates Purple Jar After Defeating Hades"                  , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Phil Cup") 
                                                                                                                                                    and has_item(state, player, "Pegasus Cup") 
                                                                                                                                                    and has_item(state, player, "Hercules Cup") 
                                                                                                                                                    and has_x_worlds(state, player, 7, options.keyblades_unlock_chests) 
                                                                                                                                                    and has_defensive_tools(state, player)
                                                                                                                                                    and has_item(state, player, "Entry Pass")
                                                                                                                                                 )
   #multiworld.get_location("Halloween Town Guillotine Square Ring Jack's Doorbell 3 Times"                , player).access_rule = lambda state: has_item(state, player, "")
    multiworld.get_location("Neverland Clock Tower 01:00 Door"                                             , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Green Trinity")
                                                                                                                                                    and has_all_magic_lvx(state, player, 2) 
                                                                                                                                                    and has_defensive_tools(state, player) 
                                                                                                                                                    and has_emblems(state, player, options.keyblades_unlock_chests)
                                                                                                                                                 )
    multiworld.get_location("Neverland Clock Tower 02:00 Door"                                             , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Green Trinity")
                                                                                                                                                    and has_all_magic_lvx(state, player, 2) 
                                                                                                                                                    and has_defensive_tools(state, player) 
                                                                                                                                                    and has_emblems(state, player, options.keyblades_unlock_chests)
                                                                                                                                                 )
    multiworld.get_location("Neverland Clock Tower 03:00 Door"                                             , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Green Trinity")
                                                                                                                                                    and has_all_magic_lvx(state, player, 2) 
                                                                                                                                                    and has_defensive_tools(state, player) 
                                                                                                                                                    and has_emblems(state, player, options.keyblades_unlock_chests)
                                                                                                                                                 )
    multiworld.get_location("Neverland Clock Tower 04:00 Door"                                             , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Green Trinity")
                                                                                                                                                    and has_all_magic_lvx(state, player, 2) 
                                                                                                                                                    and has_defensive_tools(state, player) 
                                                                                                                                                    and has_emblems(state, player, options.keyblades_unlock_chests)
                                                                                                                                                 )
    multiworld.get_location("Neverland Clock Tower 05:00 Door"                                             , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Green Trinity")
                                                                                                                                                    and has_all_magic_lvx(state, player, 2) 
                                                                                                                                                    and has_defensive_tools(state, player) 
                                                                                                                                                    and has_emblems(state, player, options.keyblades_unlock_chests)
                                                                                                                                                 )
    multiworld.get_location("Neverland Clock Tower 06:00 Door"                                             , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Green Trinity")
                                                                                                                                                    and has_all_magic_lvx(state, player, 2) 
                                                                                                                                                    and has_defensive_tools(state, player) 
                                                                                                                                                    and has_emblems(state, player, options.keyblades_unlock_chests)
                                                                                                                                                 )
    multiworld.get_location("Neverland Clock Tower 07:00 Door"                                             , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Green Trinity")
                                                                                                                                                    and has_all_magic_lvx(state, player, 2) 
                                                                                                                                                    and has_defensive_tools(state, player) 
                                                                                                                                                    and has_emblems(state, player, options.keyblades_unlock_chests)
                                                                                                                                                 )
    multiworld.get_location("Neverland Clock Tower 08:00 Door"                                             , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Green Trinity")
                                                                                                                                                    and has_all_magic_lvx(state, player, 2) 
                                                                                                                                                    and has_defensive_tools(state, player) 
                                                                                                                                                    and has_emblems(state, player, options.keyblades_unlock_chests)
                                                                                                                                                 )
    multiworld.get_location("Neverland Clock Tower 09:00 Door"                                             , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Green Trinity")
                                                                                                                                                    and has_all_magic_lvx(state, player, 2) 
                                                                                                                                                    and has_defensive_tools(state, player) 
                                                                                                                                                    and has_emblems(state, player, options.keyblades_unlock_chests)
                                                                                                                                                 )
    multiworld.get_location("Neverland Clock Tower 10:00 Door"                                             , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Green Trinity")
                                                                                                                                                    and has_all_magic_lvx(state, player, 2) 
                                                                                                                                                    and has_defensive_tools(state, player) 
                                                                                                                                                    and has_emblems(state, player, options.keyblades_unlock_chests)
                                                                                                                                                 )
    multiworld.get_location("Neverland Clock Tower 11:00 Door"                                             , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Green Trinity")
                                                                                                                                                    and has_all_magic_lvx(state, player, 2) 
                                                                                                                                                    and has_defensive_tools(state, player) 
                                                                                                                                                    and has_emblems(state, player, options.keyblades_unlock_chests)
                                                                                                                                                 )
    multiworld.get_location("Neverland Clock Tower 12:00 Door"                                             , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Green Trinity")
                                                                                                                                                    and has_all_magic_lvx(state, player, 2) 
                                                                                                                                                    and has_defensive_tools(state, player) 
                                                                                                                                                    and has_emblems(state, player, options.keyblades_unlock_chests)
                                                                                                                                                 )
    multiworld.get_location("Neverland Hold Aero Chest"                                                    , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Yellow Trinity")
                                                                                                                                                 )
    if options.hundred_acre_wood:
        multiworld.get_location("100 Acre Wood Bouncing Spot Turn in Rare Nut 1"                           , player).access_rule = lambda state: (
                                                                                                                                                    has_torn_pages(state, player, 4)
                                                                                                                                                 )
        multiworld.get_location("100 Acre Wood Bouncing Spot Turn in Rare Nut 2"                           , player).access_rule = lambda state: (
                                                                                                                                                    has_torn_pages(state, player, 4) 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "High Jump") 
                                                                                                                                                        or can_glide(state, player)
                                                                                                                                                    )
                                                                                                                                                 )
        multiworld.get_location("100 Acre Wood Bouncing Spot Turn in Rare Nut 3"                           , player).access_rule = lambda state: (
                                                                                                                                                    has_torn_pages(state, player, 4) 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "High Jump") 
                                                                                                                                                        or can_glide(state, player)
                                                                                                                                                    )
                                                                                                                                                 )
        multiworld.get_location("100 Acre Wood Bouncing Spot Turn in Rare Nut 4"                           , player).access_rule = lambda state: (
                                                                                                                                                    has_torn_pages(state, player, 4) 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "High Jump") 
                                                                                                                                                        or can_glide(state, player)
                                                                                                                                                    )
                                                                                                                                                 )
        multiworld.get_location("100 Acre Wood Bouncing Spot Turn in Rare Nut 5"                           , player).access_rule = lambda state: (
                                                                                                                                                    has_torn_pages(state, player, 4) 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "High Jump") 
                                                                                                                                                        or can_glide(state, player)
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
       #multiworld.get_location("100 Acre Wood Pooh's Room Cabinet"                                        , player).access_rule = lambda state: has_item(state, player, "")
       #multiworld.get_location("100 Acre Wood Pooh's Room Chimney"                                        , player).access_rule = lambda state: has_item(state, player, "")
        multiworld.get_location("100 Acre Wood Bouncing Spot Break Log"                                    , player).access_rule = lambda state: (
                                                                                                                                                    has_torn_pages(state, player, 4)
                                                                                                                                                 )
        multiworld.get_location("100 Acre Wood Bouncing Spot Fall Through Top of Tree Next to Pooh"        , player).access_rule = lambda state: (
                                                                                                                                                    has_torn_pages(state, player, 4) 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "High Jump") 
                                                                                                                                                        or can_glide(state, player)
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Deep Jungle Camp Hi-Potion Experiment"                                        , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Progressive Fire")
                                                                                                                                                 )
    multiworld.get_location("Deep Jungle Camp Ether Experiment"                                            , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Progressive Blizzard")
                                                                                                                                                 )
    multiworld.get_location("Deep Jungle Camp Replication Experiment"                                      , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Progressive Blizzard")
                                                                                                                                                 )
    multiworld.get_location("Deep Jungle Cliff Save Gorillas"                                              , player).access_rule = lambda state: (
                                                                                                                                                    has_slides(state, player)
                                                                                                                                                 )
    multiworld.get_location("Deep Jungle Tree House Save Gorillas"                                         , player).access_rule = lambda state: (
                                                                                                                                                    has_slides(state, player)
                                                                                                                                                 )
    multiworld.get_location("Deep Jungle Camp Save Gorillas"                                               , player).access_rule = lambda state: (
                                                                                                                                                    has_slides(state, player)
                                                                                                                                                 )
    multiworld.get_location("Deep Jungle Bamboo Thicket Save Gorillas"                                     , player).access_rule = lambda state: (
                                                                                                                                                    has_slides(state, player)
                                                                                                                                                 )
    multiworld.get_location("Deep Jungle Climbing Trees Save Gorillas"                                     , player).access_rule = lambda state: (
                                                                                                                                                    has_slides(state, player)
                                                                                                                                                 )
    if options.cups:
        multiworld.get_location("Olympus Coliseum Olympia Chest"                                           , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Phil Cup") 
                                                                                                                                                    and has_item(state, player, "Pegasus Cup") 
                                                                                                                                                    and has_item(state, player, "Hercules Cup") 
                                                                                                                                                    and has_x_worlds(state, player, 4, options.keyblades_unlock_chests)
                                                                                                                                                    and has_item(state, player, "Entry Pass")
                                                                                                                                                 )
    multiworld.get_location("Deep Jungle Jungle Slider 10 Fruits"                                          , player).access_rule = lambda state: (
                                                                                                                                                    has_slides(state, player)
                                                                                                                                                 )
    multiworld.get_location("Deep Jungle Jungle Slider 20 Fruits"                                          , player).access_rule = lambda state: (
                                                                                                                                                    has_slides(state, player)
                                                                                                                                                 )
    multiworld.get_location("Deep Jungle Jungle Slider 30 Fruits"                                          , player).access_rule = lambda state: (
                                                                                                                                                    has_slides(state, player)
                                                                                                                                                 )
    multiworld.get_location("Deep Jungle Jungle Slider 40 Fruits"                                          , player).access_rule = lambda state: (
                                                                                                                                                    has_slides(state, player)
                                                                                                                                                 )
    multiworld.get_location("Deep Jungle Jungle Slider 50 Fruits"                                          , player).access_rule = lambda state: (
                                                                                                                                                    has_slides(state, player)
                                                                                                                                                 )
   #multiworld.get_location("Traverse Town 1st District Speak with Cid Event"                              , player).access_rule = lambda state: ()
    multiworld.get_location("Wonderland Bizarre Room Read Book"                                            , player).access_rule = lambda state: (
                                                                                                                                                    has_evidence(state, player)
                                                                                                                                                 )
    multiworld.get_location("Olympus Coliseum Coliseum Gates Green Trinity"                                , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Green Trinity")
                                                                                                                                                 )
    if options.super_bosses:
        multiworld.get_location("Agrabah Defeat Kurt Zisa Zantetsuken Event"                               , player).access_rule = lambda state: has_emblems(state, player, options.keyblades_unlock_chests) and has_x_worlds(state, player, 7, options.keyblades_unlock_chests) and has_defensive_tools(state, player)
    if options.super_bosses or options.goal.current_key == "unknown":
        multiworld.get_location("Hollow Bastion Defeat Unknown EXP Necklace Event"                         , player).access_rule = lambda state: has_emblems(state, player, options.keyblades_unlock_chests) and has_x_worlds(state, player, 7, options.keyblades_unlock_chests) and has_defensive_tools(state, player)
    multiworld.get_location("Olympus Coliseum Coliseum Gates Hero's License Event"                         , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Entry Pass")
                                                                                                                                                 )
   #if options.atlantica:
       #multiworld.get_location("Atlantica Sunken Ship Crystal Trident Event"                              , player).access_rule = lambda state: ()
   #multiworld.get_location("Halloween Town Graveyard Forget-Me-Not Event"                                 , player).access_rule = lamdba state: ()
   #multiworld.get_location("Deep Jungle Tent Protect-G Event"                                             , player).access_rule = lambda state: ()
    multiworld.get_location("Deep Jungle Cavern of Hearts Navi-G Piece Event"                              , player).access_rule = lambda state: (
                                                                                                                                                    has_slides(state, player)
                                                                                                                                                 )
    multiworld.get_location("Wonderland Bizarre Room Navi-G Piece Event"                                   , player).access_rule = lambda state: (
                                                                                                                                                    has_evidence(state, player)
                                                                                                                                                 )
   #multiworld.get_location("Olympus Coliseum Coliseum Gates Entry Pass Event"                             , player).access_rule = lambda state: ()
    
    multiworld.get_location("Traverse Town Synth Log"                                                      , player).access_rule = lambda state: (
                                                                                                                                                    has_at_least(state, player, "Empty Bottle", 6) 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "Green Trinity")
                                                                                                                                                        or has_at_least(state, player, "High Jump", 3)
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Traverse Town Synth Cloth"                                                    , player).access_rule = lambda state: (
                                                                                                                                                    has_at_least(state, player, "Empty Bottle", 6) 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "Green Trinity")
                                                                                                                                                        or has_at_least(state, player, "High Jump", 3)
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Traverse Town Synth Rope"                                                     , player).access_rule = lambda state: (
                                                                                                                                                    has_at_least(state, player, "Empty Bottle", 6) 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "Green Trinity")
                                                                                                                                                        or has_at_least(state, player, "High Jump", 3)
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Traverse Town Synth Seagull Egg"                                              , player).access_rule = lambda state: (
                                                                                                                                                    has_at_least(state, player, "Empty Bottle", 6) 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "Green Trinity")
                                                                                                                                                        or has_at_least(state, player, "High Jump", 3)
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Traverse Town Synth Fish"                                                     , player).access_rule = lambda state: (
                                                                                                                                                    has_at_least(state, player, "Empty Bottle", 6) 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "Green Trinity")
                                                                                                                                                        or has_at_least(state, player, "High Jump", 3)
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Traverse Town Synth Mushroom"                                                 , player).access_rule = lambda state: (
                                                                                                                                                    has_at_least(state, player, "Empty Bottle", 6) 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "Green Trinity")
                                                                                                                                                        or has_at_least(state, player, "High Jump", 3)
                                                                                                                                                    )
                                                                                                                                                 )
    
   #multiworld.get_location("Traverse Town Item Shop Postcard"                                             , player).access_rule = lambda state: has_item(state, player, "")
   #multiworld.get_location("Traverse Town 1st District Safe Postcard"                                     , player).access_rule = lambda state: has_item(state, player, "")
    multiworld.get_location("Traverse Town Gizmo Shop Postcard 1"                                          , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Progressive Thunder")
                                                                                                                                                 )
    multiworld.get_location("Traverse Town Gizmo Shop Postcard 2"                                          , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Progressive Thunder")
                                                                                                                                                 )
    multiworld.get_location("Traverse Town Item Workshop Postcard"                                         , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Green Trinity") 
                                                                                                                                                    or has_at_least(state, player, "High Jump", 3)
                                                                                                                                                 )
   #multiworld.get_location("Traverse Town 3rd District Balcony Postcard"                                  , player).access_rule = lambda state: has_item(state, player, "")
    multiworld.get_location("Traverse Town Geppetto's House Postcard"                                      , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Monstro") 
                                                                                                                                                    and 
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "High Jump") 
                                                                                                                                                        or (options.advanced_logic and can_glide(state, player))
                                                                                                                                                    )
                                                                                                                                                 )
   #multiworld.get_location("Halloween Town Lab Torn Page"                                                 , player).access_rule = lambda state: has_item(state, player, "")
    multiworld.get_location("Hollow Bastion Entrance Hall Emblem Piece (Flame)"                            , player).access_rule = lambda state: (
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "Theon Vol. 6") 
                                                                                                                                                        or has_at_least(state, player, "High Jump", 3)
                                                                                                                                                        or has_emblems(state, player, options.keyblades_unlock_chests)
                                                                                                                                                    )
                                                                                                                                                    and has_item(state, player, "Progressive Fire")
                                                                                                                                                    and
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "High Jump")
                                                                                                                                                        or can_glide(state, player)
                                                                                                                                                        or has_item(state, player, "Progressive Thunder")
                                                                                                                                                        or options.advanced_logic
                                                                                                                                                    )
                                                                                                                                                 )
    multiworld.get_location("Hollow Bastion Entrance Hall Emblem Piece (Chest)"                            , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Theon Vol. 6") 
                                                                                                                                                    or has_at_least(state, player, "High Jump", 3)
                                                                                                                                                    or has_emblems(state, player, options.keyblades_unlock_chests)
                                                                                                                                                 )
    multiworld.get_location("Hollow Bastion Entrance Hall Emblem Piece (Statue)"                           , player).access_rule = lambda state: (
                                                                                                                                                    (
                                                                                                                                                        has_item(state, player, "Theon Vol. 6") 
                                                                                                                                                        or has_at_least(state, player, "High Jump", 3)
                                                                                                                                                        or has_emblems(state, player, options.keyblades_unlock_chests)
                                                                                                                                                    )
                                                                                                                                                    and has_item(state, player, "Red Trinity")
                                                                                                                                                 )
    multiworld.get_location("Hollow Bastion Entrance Hall Emblem Piece (Fountain)"                         , player).access_rule = lambda state: (
                                                                                                                                                    has_item(state, player, "Theon Vol. 6") 
                                                                                                                                                    or has_at_least(state, player, "High Jump", 3)
                                                                                                                                                    or has_emblems(state, player, options.keyblades_unlock_chests)
                                                                                                                                                 )
   #multiworld.get_location("Traverse Town 1st District Leon Gift"                                         , player).access_rule = lambda state: ()
   #multiworld.get_location("Traverse Town 1st District Aerith Gift"                                       , player).access_rule = lambda state: ()
    multiworld.get_location("Hollow Bastion Library Speak to Belle Divine Rose"                            , player).access_rule = lambda state: (
                                                                                                                                                    has_emblems(state, player, options.keyblades_unlock_chests)
                                                                                                                                                 )
    multiworld.get_location("Hollow Bastion Library Speak to Aerith Cure"                                  , player).access_rule = lambda state: (
                                                                                                                                                    has_emblems(state, player, options.keyblades_unlock_chests)
                                                                                                                                                 )
    
    
    if options.goal.current_key == "final_ansem":
        multiworld.get_location("Final Ansem"                                                              , player).access_rule = lambda state: (
                                                                                                                                                    has_final_rest_door(state, player, final_rest_door_requirement, final_rest_door_required_reports, options.keyblades_unlock_chests)
                                                                                                                                                 )
    for i in range(options.level_checks):
        multiworld.get_location("Level " + str(i+1).rjust(3,'0')                                           , player).access_rule = lambda state, level_num=i: has_x_worlds(state, player, min(((level_num//10)*2), 8), options.keyblades_unlock_chests)
    


    # Region rules.
    multiworld.get_entrance("Wonderland"                                                                   , player).access_rule = lambda state: has_item(state, player,"Wonderland") and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
    multiworld.get_entrance("Olympus Coliseum"                                                             , player).access_rule = lambda state: has_item(state, player,"Olympus Coliseum") and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
    multiworld.get_entrance("Deep Jungle"                                                                  , player).access_rule = lambda state: has_item(state, player,"Deep Jungle") and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
    multiworld.get_entrance("Agrabah"                                                                      , player).access_rule = lambda state: has_item(state, player,"Agrabah") and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
    multiworld.get_entrance("Monstro"                                                                      , player).access_rule = lambda state: has_item(state, player,"Monstro") and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
    if options.atlantica:
        multiworld.get_entrance("Atlantica"                                                                , player).access_rule = lambda state: has_item(state, player,"Atlantica") and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
    multiworld.get_entrance("Halloween Town"                                                               , player).access_rule = lambda state: has_item(state, player,"Halloween Town") and has_x_worlds(state, player, 2, options.keyblades_unlock_chests)
    multiworld.get_entrance("Neverland"                                                                    , player).access_rule = lambda state: has_item(state, player,"Neverland") and has_x_worlds(state, player, 3, options.keyblades_unlock_chests)
    multiworld.get_entrance("Hollow Bastion"                                                               , player).access_rule = lambda state: has_item(state, player,"Hollow Bastion") and has_x_worlds(state, player, 5, options.keyblades_unlock_chests)
    multiworld.get_entrance("End of the World"                                                             , player).access_rule = lambda state: has_x_worlds(state, player, 7, options.keyblades_unlock_chests) and (has_reports(state, player, eotw_required_reports) or has_item(state, player,"End of the World"))
    multiworld.get_entrance("100 Acre Wood"                                                                , player).access_rule = lambda state: has_item(state, player, "Progressive Fire")

    # Win condition.
    multiworld.completion_condition[player] = lambda state: state.has("Victory", player)
    