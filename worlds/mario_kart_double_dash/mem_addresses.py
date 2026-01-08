class MkddMemAddresses():
    """
    Collection of memory addresses of relevant data.
    Inherit this class to specify addresses for different versions.

    Property suffixes tell the data type (b = byte, h = half word, w = word, s = string, f = float, x = table).
    Pointers are always words.
    """
    # Vanilla addresses:
    mode_w: int
    """Current game mode. Updated after select character screen. See game_data.Modes for values."""
    cup_w: int
    """Cup selection. 0 Mushroom Cup - 4 All Cup Tour."""
    menu_course_w: int
    """Currently selected course inside a cup. Doesn't update in midst of a gp. 0-3."""
    vehicle_class_w: int
    """Currently selected class. Updated after select character screen. 0 = 50cc, 3 = Mirror."""
    current_course_w: int
    """Currently loaded course. For values see game_data.COURSES"""
    current_lap_wx: int
    """Table of players' current lap from 1st player to 4th. 0 = 1st lap."""
    in_race_placement_wx: int
    """Table of player placements from 1st player to 4th. 1 = 1st place. -1 for unused player slots."""
    current_course_ranking_w: int
    total_ranking_w: int
    """Player's placement in the current cup. 0 = 1st place."""
    total_points_wx: int
    """Players' and cpus' points in a table."""
    game_ticks_w: int
    """Frames since game startup. 60 per second."""
    kart_stats_pointer: int
    """Pointer to kart stat table."""
    gp_race_no_w: int
    """Current race # inside a cup. 0 = first race, 16 = all cup tour awards."""
    speed_multiplier_150cc_f: int
    """Speed multiplier when playing on 150cc or Mirror. Default 1.15."""
    max_speed_f: int
    """Max kart speed which cannot be exceeded even with mushrooms. Default 200."""
    all_cup_tour_contents_wx: int
    """All cup tour course ids - uses ids 0 (Luigi Circuit) - 16 (Rainbow Road). Lenght 16, first value is unused."""
    cup_contents_wx: int
    """Table of cup course ids, name and preview images in cup order (ie. from Luigi Circuit to Rainbow Road).
    Example: Mushroom cup course 3: course id = 2*12, name = 2*12+4, preview = 2*12+8."""
    course_names_s: list[int]
    """List of course name image files for the menu."""
    course_previews_s: list[int]
    """List of course preview image files for the menu."""

    # Vanilla offsets:
    menu_character_w_offset: int
    """Offset from menu_pointer, cursor position."""
    menu_kart_w_offset: int
    """Offset from menu_pointer, selected kart."""
    menu_driver_w_offset: int
    """Offset from menu_pointer, confirmed driver."""
    menu_rider_w_offset: int
    """Offset from menu_pointer, confirmed rider."""
    menu_player_struct_size: int
    """Size of player menu struct. Add this to menu offsets to get different players' selections."""
    kart_struct_size: int
    """Use this in combination with kart_stats_pointer and stat offsets to modify karts."""
    kart_speed_on_road_f_offset: int
    kart_speed_off_road_sand_f_offset: int
    kart_speed_off_road_grass_f_offset: int
    kart_speed_off_road_mud_f_offset: int
    kart_acceleration_1_f_offset: int
    kart_acceleration_2_f_offset: int
    kart_mini_turbo_f_offset: int
    kart_mass_f_offset: int
    kart_roll_f_offset: int
    kart_steer_f_offset: int

    # Custom addresses:
    menu_pointer: int
    """Pointer to menu object. Use with character/kart offsets."""
    available_characters_bx: int
    """Table of available characters from Mario to King Boo (size 20). 1 = unlocked."""
    available_karts_bx: int
    """Table of available karts from Goo-Goo Buggy to Parade Kart (size 21). 1 = unlocked."""
    race_counter_w: int
    """Increased each time the player finishes."""
    race_timer_w: int
    """Increased each frame during the race (inc. countdown of 185 frames)."""
    lap_count_bx: int
    """Lap count for each course. Offsets from course ids."""
    max_vehicle_class_w: int
    """0 = 50cc, 3 = Mirror"""
    available_cups_bx: int
    """Table of available cups (size 5). 1 = unlocked."""
    tt_items_bx: int
    """Items for driver and rider in time trials (size 2)."""
    gp_next_items_bx: int
    """Item for player in grand prix. Offset by character's special item id (size 22)."""
    text_sx: int
    """Text to print."""
    text_size: int
    """Max lenght of the text."""
    text_x_offset_h: int
    """Offset from text, x coordinate for the text."""
    text_y_offset_h: int
    """Offset from text, y coordinate for the text."""
    text_amount: int
    """Size of the text table."""

class MkddMemAddressesUsa(MkddMemAddresses):
    # Vanilla addresses:
    mode_w = 0x803b1464
    cup_w = 0x803cb7a8
    menu_course_w = 0x803cb7ac
    vehicle_class_w = 0x803b146c
    current_course_w = 0x803cbd44
    current_lap_wx = 0x8037ff60
    in_race_placement_wx = 0x8037ffa0
    current_course_ranking_w = 0x803b0f3b
    total_ranking_w = 0x803b1260
    total_points_wx = 0x803b11cc
    game_ticks_w = 0x803b0754
    kart_stats_pointer = 0x80bd5000
    gp_race_no_w = 0x803b0fc8
    speed_multiplier_150cc_f = 0x80361d4c
    max_speed_f = 0x803d1894
    all_cup_tour_contents_wx = 0x803b1300
    cup_contents_wx = 0x803322e8
    course_names_s = [
        0x80331fd0, # Luigi Circuit
        0x80332004, # Peach Beach
        0x80332030, # Baby Park
        0x8033205c, # Dry Dry Desert
        0x80332094, # Mushroom Bridge
        0x803320c8, # Mario Circuit
        0x803320fc, # Daisy Cruiser
        0x80332128, # Waluigi Stadium
        0x8033215c, # Sherbet Land
        0x8033218c, # Mushroom City
        0x803321b8, # Yoshi Circuit
        0x803321ec, # DK Mountain
        0x80332218, # Wario Colosseum
        0x8033224c, # Dino Dino Jungle
        0x80332284, # Bowser's Castle
        0x803322b8, # Rainbow Road
    ]
    course_previews_s = [
        0x80331fec, # Luigi Circuit
        0x8033201c, # Peach Beach
        0x80332048, # Baby Park
        0x80332078, # Dry Dry Desert
        0x803320b0, # Mushroom Bridge
        0x803320e4, # Mario Circuit
        0x80332114, # Daisy Cruiser
        0x80332144, # Waluigi Stadium
        0x80332174, # Sherbet Land
        0x803321a4, # Mushroom City
        0x803321d4, # Yoshi Circuit
        0x80332204, # DK Mountain
        0x80332234, # Wario Colosseum
        0x80332268, # Dino Dino Jungle
        0x803322a0, # Bowser's Castle
        0x803322d0, # Rainbow Road
    ]

    # Vanilla offsets:
    menu_character_w_offset = 0x212c
    menu_kart_w_offset = 0x2140
    menu_driver_w_offset = 0x2138
    menu_rider_w_offset = 0x213c
    menu_player_struct_size = 28

    kart_struct_size = 0x100
    kart_speed_on_road_f_offset = 0x50
    kart_speed_off_road_sand_f_offset = 0x54
    kart_speed_off_road_grass_f_offset = 0x58
    kart_speed_off_road_mud_f_offset = 0x5c
    kart_acceleration_1_f_offset = 0x64
    kart_acceleration_2_f_offset = 0x74
    kart_mini_turbo_f_offset = 0x80
    kart_mass_f_offset = 0x84
    kart_roll_f_offset = 0xa0
    kart_steer_f_offset = 0xb4

    # Custom addresses:
    menu_pointer = 0x80001030
    available_characters_bx = 0x80001000
    available_karts_bx = 0x80001014
    race_counter_w = 0x8000102c
    race_timer_w = 0x80001034
    lap_count_bx = 0x80005460 - 0x21 # First course has id of 0x21
    max_vehicle_class_w = 0x80001038
    available_cups_bx = 0x8000103c
    tt_items_bx = 0x80001041
    gp_next_items_bx = 0x80001043

    text_sx = 0x80000da4
    text_size = 0x30
    text_x_offset_h = -4
    text_y_offset_h = -2
    text_amount = 5
