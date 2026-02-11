from ..DSZeldaClient.subclasses import Address, Pointer, SRAM

addr_null = Address(0, 0)

class PHAddr:
    null = addr_null

    # Basic Reads
    game_identifier = Address(0, 0, 16, "ROM")
    game_state = Address(0x060C48)
    save_slot = Address(0x1B8124)
    
    boat_health = Address(0x1FA036, name="boat_health")
    salvage_health = Address(0x1F5720, name="salvage_health")
    
    received_item_index = Address(0x1BA64C, size=2)
    slot_id = Address(0x1BA64A, size=2)
    
    stage = Address(0x1B2E94, size=4)
    room = Address(0x1B2EA6)
    floor = Address(0x1B2E98, size=4)  # unused
    entrance = Address(0x1B2EA7)
    
    transition_x = Address(0x1B2EC8, size=4)
    transition_y = Address(0x1B2ECC, size=4)
    transition_z = Address(0x1B2ED0, size=4)
    boat_respawn = Address(0x1B2F12, size=2)
    
    link_x = Address(0x1B6FEC, size=4, name="link_x")
    link_y = Address(0x1B6FF0, size=4, name="link_y")
    link_z = Address(0x1B6FF4, size=4, name="link_z")
    boat_x = Address(0x1B8518, size=4, name="boat_x")
    boat_z = Address(0x1B8520, size=4, name="boat_y")
    
    # Technical Reads
    getting_location = Address(0x1B6F44)
    shot_frog = Address(0x1B7038)
    getting_ship_part = Address(0x11F5E4)
    getting_salvage = Address(0x1BA654)
    getting_salvage_1 = Address(0x1ba655)
    getting_salvage_2 = Address(0x1ba656)
    getting_salvage_3 = Address(0x1ba657)
    
    stage_small = Address(0x1B2E94, size=1)  # Used for precision rads
    
    saving = Address(0x19B7CF)
    changing_map_scene = Address(0x1BA700)
    pen_mode_pointer = Address(0x1CCCEC, size=4)
    lower_water = Address(0x1B5582)
    
    text_speed = Address(0x0EC754)  # Sus
    treasure_price_index = Address(0x0EC7D8, size=4)
    
    using_item = Address(0x1BA71C)
    drawing_sea_route = Address(0x207C4C)
    equipped_item = Address(0x1BA520, size=4)
    got_item_menu = Address(0x19A5B0)
    opened_clog = Address(0x0FC5BC)
    flipped_clog = Address(0x0FA37B)
    in_map = Address(0x1B2D60)
    using_cyclone_slate = Address(0x1B636C)
    
    loading_stage = Address(0x1B2E78)  # 0 when loading stage, some sorta pointer
    loading_room = Address(0x10BD6F) # 0 when not loading room
    in_cutscene = Address(0x1BBCF4)
    in_short_cs = Address(0x1B6FE8)
    started_save_file = Address(0x1B7FB8)  # Used to trigger precision stuff from menu

    link_held_item_goron = Address(0x1CD770, size=2)
    link_held_item_2 = Address(0x1CDAE0, size=2)
    link_held_item = Address(0x1CD510, size=2)

    actor_table_pointer = Address(0x1BA8C4, size=4)

    # Pointers
    gItemManager = Pointer(0x0fb4)
    gPlayerManager = Pointer(0x0fbc)
    gAdventureFlags = Pointer(0x0f74)
    gPlayer = Pointer(0x0f90)
    # gOverlayManager_mLoadedOverlays_4 = Pointer(0x0910)
    gMapManager = Pointer(0x0e60)
    
    # Adventure flags
    adv_flags = Address(0x1B557C, size=52)
    adv_flags_0 = Address(0x1b557c)
    adv_flags_1 = Address(0x1b557d)
    adv_flags_2 = flags_fog_spirits = Address(0x1b557e)
    adv_flags_3 = flags_bosses_0 = Address(0x1b557f)
    adv_flags_4 = Address(0x1b5580)
    adv_flags_5 = Address(0x1b5581)
    adv_flags_6 = flags_clear_fog = flags_cannon = Address(0x1b5582)
    adv_flags_7 = Address(0x1b5583)
    adv_flags_8 = Address(0x1b5584)
    adv_flags_9 = Address(0x1b5585)
    adv_flags_10 = Address(0x1b5586)
    adv_flags_11 = Address(0x1b5587)
    adv_flags_12 = Address(0x1b5588)
    adv_flags_13 = flags_shops = Address(0x1b5589)
    adv_flags_14 = Address(0x1b558a)
    adv_flags_15 = flags_metals = Address(0x1b558b)
    adv_flags_16 = Address(0x1b558c)
    adv_flags_17 = Address(0x1b558d)
    adv_flags_18 = Address(0x1b558e)
    adv_flags_19 = Address(0x1b558f)
    adv_flags_20 = flags_trade_quest = Address(0x1b5590)
    adv_flags_21 = Address(0x1b5591)
    adv_flags_22 = Address(0x1b5592)
    adv_flags_23 = Address(0x1b5593)
    adv_flags_24 = Address(0x1b5594)
    adv_flags_25 = Address(0x1b5595)
    adv_flags_26 = Address(0x1b5596)
    adv_flags_27 = Address(0x1b5597)
    adv_flags_28 = Address(0x1b5598)
    adv_flags_29 = Address(0x1b5599)
    adv_flags_30 = Address(0x1b559a)
    adv_flags_31 = Address(0x1b559b)
    adv_flags_32 = Address(0x1b559c)
    adv_flags_33 = Address(0x1b559d)
    adv_flags_34 = Address(0x1b559e)
    adv_flags_35 = Address(0x1b559f)
    adv_flags_36 = Address(0x1b55a0)
    adv_flags_37 = Address(0x1b55a1)
    adv_flags_38 = Address(0x1b55a2)
    adv_flags_39 = frog_glyphs = Address(0x1b55a3)
    adv_flags_40 = Address(0x1b55a4)
    adv_flags_41 = Address(0x1b55a5)
    adv_flags_42 = Address(0x1b55a6)
    adv_flags_43 = Address(0x1b55a7)
    adv_flags_44 = watched_intro = Address(0x1b55a8)  # intro is 0x2
    adv_flags_45 = Address(0x1b55a9)
    adv_flags_46 = Address(0x1b55aa)
    adv_flags_47 = flags_fog_done = Address(0x1b55ab)
    adv_flags_48 = Address(0x1b55ac)
    adv_flags_49 = Address(0x1b55ad)
    adv_flags_50 = Address(0x1b55ae)
    adv_flags_51 = Address(0x1b55af)
    
    
    
    small_key_storage_1 = Address(0x1BA64E)
    small_key_storage_2 = Address(0x1BA64F)
    custom_storage = Address(0x1BA661)
    
    tof_doors = Address(0x258D20)
    tow_doors = Address(0x24D740, size=2)
    toc_boss_door = Address(0x252360)
    gt_boss_door = Address(0x25D9B0)
    toi_doors = Address(0x259CA0)
    mt_doors = Address(0x24DED0)
    
    color_switch_toi = Address(0x20DBE0)
    color_switch_toc = Address(0x207CA8)
    
    wayfarer_chest = Address(0x20DAA1)
    
    cannon_bomb_blocks = Address(0x2562F0)
    goron_bomb_blocks = Address(0x262888)
    molida_bomb_blocks = Address(0x258B6C)
    
    tow_warp = Address(0x25A224)
    toc_warp = Address(0x25AF1C)
    toi_warp = Address(0x264FE4)
    
    totok_b3_state = Address(0x2572EC, size=2)
    totok_b3_state_1 = Address(0x2572ED)
    totok_b8_state = Address(0x25762C)
    totok_b9_state = Address(0x257694)
    totok_b12_state = Address(0x257834, size=2)
    totok_b12_state_1 = Address(0x257835)
    totok_b12_pedestal_left = Address(0x257EA4)
    totok_b12_pedestal_right = Address(0x257FE4)
    toc_crystal_state = Address(0x252264)
    global_salvage_health = Address(0x1BA390)
    
    totok_b9_elevator = Address(0x20C5F0)
    
    # Inventory Data
    inventory_1 = Address(0x1ba644)
    inventory_2 = Address(0x1ba645)  # Just hammer and potions lol
    inventory_3 = fairies_0 = Address(0x1ba646)  # Fairies 0
    inventory_4 = fairies_1 = Address(0x1ba647)  # Fairies 1
    inventory_5 = Address(0x1ba648)
    inventory_6 = Address(0x1ba649)
    
    rupee_count = Address(0x1ba53e, size=2)
    
    show_ship_prices = Address(0x1BA658, size=9)
    show_treasure_prices = Address(0x1BA664)
    ship_part_counts = Address(0x1BA564, size=72)
    
    all_treasure_count = Address(0x1BA5AC, size=8)
    pink_coral_count = Address(0x1BA5AC)
    wpl_count = Address(0x1BA5AD)
    dpl_count = Address(0x1BA5AE)
    zora_scale_count = Address(0x1BA5AF)
    goron_amber_count = Address(0x1BA5B0)
    ruto_crown_count = Address(0x1BA5B1)
    roc_feather_count = Address(0x1BA5B2)
    regal_ring_count = Address(0x1BA5B3)
    
    phantom_hourglass_max = Address(0x1BA528, size=4)
    phantom_hourglass_current = Address(0x1E2A48, size=4)
    
    treasure_maps_0 = Address(0x1BA650)
    treasure_maps_1 = Address(0x1BA651)
    treasure_maps_2 = Address(0x1BA652)
    treasure_maps_3 = Address(0x1BA653)
    
    sword_count = Address(0x1ba6b8)
    boomerang_bit = Address(0x1BA6BC)
    shovel_bit = Address(0x1BA6BE)
    bomb_count = Address(0x1BA6C0, size=2)
    arrow_count = Address(0x1BA6C2, size=2)
    grapple_bit = Address(0x1BA6C4)
    chu_count = Address(0x1BA6C6, size=2)
    hammer_bit = Address(0x1BA6C8)
    
    bomb_upgrades = Address(0x1ba5d2)
    quiver_upgrades = Address(0x1ba5d0)
    chu_upgrades = Address(0x1ba5d4)
    
    power_gem_count = Address(0x1BA541)
    wisdom_gem_count = Address(0x1BA542)
    courage_gem_count = Address(0x1BA540)
    
    skippyjack_count = Address(0x1BA5B4)
    toona_count = Address(0x1BA5B5)
    loovar_count = Address(0x1BA5B6)
    rsf_count = Address(0x1BA5B7)
    neptoona_count = Address(0x1BA5B8)
    stowfish_count = Address(0x1BA5B9)
    
    heart_containers = Address(0x1ba388, size=2)
    beedle_points = Address(0x1B2773)
    
    potion_left = Address(0x1BA5D8)
    potion_right = Address(0x1BA5D9)
    
    island_visible_mercay = Address(0x1b4b8c)
    island_visible_molida = Address(0x1b4bb4)
    island_visible_ember = Address(0x1B4BDC)
    island_visible_cannon = Address(0x1B4C04)
    island_visible_spirit = Address(0x1B4C2C)
    island_visible_gust = Address(0x1B4C54)
    island_visible_bannan = Address(0x1B4C7C)
    island_visible_zauz = Address(0x1B4CA4)
    island_visible_uncharted = Address(0x1B4CCC)
    island_visible_goron = Address(0x1B4CF4)
    island_visible_frost = Address(0x1B4D1C)
    island_visible_harrow = Address(0x1B4D44)
    island_visible_ds = Address(0x1B4D6C)
    island_visible_ruins = Address(0x1B4D94)
    island_visible_iotd = Address(0x1B4DBC)
    island_visible_maze = Address(0x1B4DE4)

    equipped_ship_parts_0 = Address(0x1ba544, size=4)
    equipped_ship_parts_1 = Address(0x1ba548, size=4)
    equipped_ship_parts_2 = Address(0x1ba54c, size=4)
    equipped_ship_parts_3 = Address(0x1ba550, size=4)
    equipped_ship_parts_4 = Address(0x1ba554, size=4)
    equipped_ship_parts_5 = Address(0x1ba558, size=4)
    equipped_ship_parts_6 = Address(0x1ba55c, size=4)
    equipped_ship_parts_7 = Address(0x1ba560, size=4)
    
    # island_visible_ = Address()
    # island_visible_ = Address()
    # island_visible_ = Address()
    # island_visible_ = Address()
    # island_visible_ = Address()
    # island_visible_ = Address()

class PHSRAM:
    # SRAM
    mercay_se_chests = SRAM(0x3c4)
    mountain_passage_chests = SRAM(0xae4)
    mountain_passage = SRAM(0x230)
    bannan = SRAM(0x198)
    gs = SRAM(0xb14)
    frost = SRAM(0x544)
    iotd = SRAM(0x73c)
    maze = SRAM(0x1c1)