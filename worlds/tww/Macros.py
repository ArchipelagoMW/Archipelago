from BaseClasses import CollectionState


def can_play_winds_requiem(state: CollectionState, player: int) -> bool:
    return state.has_all(["Wind Waker", "Wind's Requiem"], player)


def can_play_ballad_of_gales(state: CollectionState, player: int) -> bool:
    return state.has_all(["Wind Waker", "Ballad of Gales"], player)


def can_play_command_melody(state: CollectionState, player: int) -> bool:
    return state.has_all(["Wind Waker", "Command Melody"], player)


def can_play_earth_gods_lyric(state: CollectionState, player: int) -> bool:
    return state.has_all(["Wind Waker", "Earth God's Lyric"], player)


def can_play_wind_gods_aria(state: CollectionState, player: int) -> bool:
    return state.has_all(["Wind Waker", "Wind God's Aria"], player)


def can_play_song_of_passing(state: CollectionState, player: int) -> bool:
    return state.has_all(["Wind Waker", "Song of Passing"], player)


def can_fan_with_deku_leaf(state: CollectionState, player: int) -> bool:
    return state.has("Deku Leaf", player)


def can_fly_with_deku_leaf_indoors(state: CollectionState, player: int) -> bool:
    return state.has("Deku Leaf", player) and has_magic_meter(state, player)


def can_fly_with_deku_leaf_outdoors(state: CollectionState, player: int) -> bool:
    return state.has("Deku Leaf", player) and has_magic_meter(state, player) and can_play_winds_requiem(state, player)


def can_use_magic_armor(state: CollectionState, player: int) -> bool:
    return state.has("Magic Armor", player) and has_magic_meter(state, player)


def can_aim_mirror_shield(state: CollectionState, player: int) -> bool:
    return has_mirror_shield(state, player) and (
        state.has_any(["Wind Waker", "Grappling Hook", "Boomerang", "Deku Leaf", "Hookshot"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_move_boulders(state: CollectionState, player: int) -> bool:
    return state.has_any(["Bombs", "Power Bracelets"], player)


def can_defeat_door_flowers(state: CollectionState, player: int) -> bool:
    return state.has_any(["Boomerang", "Bombs", "Hookshot"], player) or has_heros_bow(state, player)


def can_hit_diamond_switches_at_range(state: CollectionState, player: int) -> bool:
    return state.has_any(["Boomerang", "Hookshot"], player) or has_heros_bow(state, player)


def can_destroy_seeds_hanging_by_vines(state: CollectionState, player: int) -> bool:
    return state.has_any(["Boomerang", "Bombs", "Hookshot"], player) or has_heros_bow(state, player)


def has_heros_sword(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Sword", player, 1)


def has_any_master_sword(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Sword", player, 2)


def has_full_power_master_sword(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Sword", player, 4)


def has_heros_shield(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Shield", player, 1)


def has_mirror_shield(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Shield", player, 2)


def has_heros_bow(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Bow", player, 1)


def has_fire_arrows(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Bow", player, 2) and has_magic_meter(state, player)


def has_ice_arrows(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Bow", player, 2) and has_magic_meter(state, player)


def has_light_arrows(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Bow", player, 3) and has_magic_meter(state, player)


def has_any_wallet_upgrade(state: CollectionState, player: int) -> bool:
    return state.has("Wallet Capacity Upgrade", player, 1)


def has_picto_box(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Picto Box", player, 1)


def has_deluxe_picto_box(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Picto Box", player, 2)


def has_any_quiver_upgrade(state: CollectionState, player: int) -> bool:
    return state.has("Quiver Capacity Upgrade", player, 1)


def has_magic_meter(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Magic Meter", player, 1)


def has_magic_meter_upgrade(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Magic Meter", player, 2)


def has_all_8_triforce_shards(state: CollectionState, player: int) -> bool:
    return state.has_group_unique("Shards", player, 8)


def has_tingle_bombs(state: CollectionState, player: int) -> bool:
    return state.has("Bombs", player) or (state._tww_tuner_logic_enabled(player) and state.has("Tingle Tuner", player))


def can_reach_outset_island_upper_level(state: CollectionState, player: int) -> bool:
    return can_cut_down_outset_trees(state, player) or (
        can_fly_with_deku_leaf_outdoors(state, player) and state._tww_obscure_1(player)
    )


def can_access_forest_of_fairies(state: CollectionState, player: int) -> bool:
    return can_reach_outset_island_upper_level(state, player) and can_fly_with_deku_leaf_outdoors(state, player)


def can_reach_dragon_roost_cavern_gaping_maw(state: CollectionState, player: int) -> bool:
    return state.has("DRC Small Key", player, 1) and (
        (state.has("DRC Small Key", player, 4) and can_cut_down_hanging_drc_platform(state, player))
        or (can_fly_with_deku_leaf_indoors(state, player) and state._tww_obscure_2(player))
        or (has_ice_arrows(state, player) and state._tww_obscure_2(player) and state._tww_precise_1(player))
    )


def can_reach_dragon_roost_cavern_boss_stairs(state: CollectionState, player: int) -> bool:
    return state.has("DRC Small Key", player, 4) and (
        state.has_any(["Grappling Hook", "Hookshot"], player)
        or can_fly_with_deku_leaf_indoors(state, player)
        or has_ice_arrows(state, player)
    )


def can_reach_tower_of_the_gods_second_floor(state: CollectionState, player: int) -> bool:
    return state.has_all(["Bombs", "TotG Small Key"], player) and can_defeat_yellow_chuchus(state, player)


def can_reach_tower_of_the_gods_third_floor(state: CollectionState, player: int) -> bool:
    return (
        can_reach_tower_of_the_gods_second_floor(state, player)
        and can_bring_west_servant_of_the_tower(state, player)
        and can_bring_north_servant_of_the_tower(state, player)
        and state.has("Wind Waker", player)
    )


def can_bring_west_servant_of_the_tower(state: CollectionState, player: int) -> bool:
    return (
        (state.has("Grappling Hook", player) or can_fly_with_deku_leaf_indoors(state, player))
        and can_play_command_melody(state, player)
        and has_heros_bow(state, player)
    )


def can_bring_north_servant_of_the_tower(state: CollectionState, player: int) -> bool:
    return (
        state.has("TotG Small Key", player, 2)
        and (can_fly_with_deku_leaf_indoors(state, player) or state._tww_obscure_1(player))
        and can_play_command_melody(state, player)
    )


def can_reach_earth_temple_sun_statue_room(state: CollectionState, player: int) -> bool:
    return (
        can_play_command_melody(state, player)
        and can_defeat_red_chuchus(state, player)
        and can_defeat_green_chuchus(state, player)
    )


def can_reach_earth_temple_right_path(state: CollectionState, player: int) -> bool:
    return (
        can_reach_earth_temple_sun_statue_room(state, player)
        and can_play_command_melody(state, player)
        and state.has("Skull Hammer", player)
    )


def can_reach_earth_temple_left_path(state: CollectionState, player: int) -> bool:
    return can_reach_earth_temple_sun_statue_room(state, player) and state.has("ET Small Key", player, 2)


def can_reach_earth_temple_moblins_and_poes_room(state: CollectionState, player: int) -> bool:
    return (
        can_reach_earth_temple_left_path(state, player)
        and has_fire_arrows(state, player)
        and state.has("Power Bracelets", player)
        and can_defeat_floormasters(state, player)
        and (can_play_command_melody(state, player) or has_mirror_shield(state, player))
    )


def can_reach_earth_temple_basement(state: CollectionState, player: int) -> bool:
    return (
        can_reach_earth_temple_sun_statue_room(state, player)
        and can_play_command_melody(state, player)
        and can_aim_mirror_shield(state, player)
    )


def can_reach_earth_temple_redead_hub_room(state: CollectionState, player: int) -> bool:
    return can_reach_earth_temple_basement(state, player) and can_play_earth_gods_lyric(state, player)


def can_reach_earth_temple_third_crypt(state: CollectionState, player: int) -> bool:
    return (
        can_reach_earth_temple_redead_hub_room(state, player)
        and (can_play_command_melody(state, player) or can_aim_mirror_shield(state, player))
        and state.has_all_counts({"Power Bracelets": 1, "Skull Hammer": 1, "ET Small Key": 3}, player)
        and (can_defeat_red_bubbles(state, player) or state._tww_precise_2(player))
        and can_play_command_melody(state, player)
        and can_aim_mirror_shield(state, player)
    )


def can_reach_earth_temple_tall_vine_room(state: CollectionState, player: int) -> bool:
    return can_reach_earth_temple_third_crypt(state, player) and can_play_earth_gods_lyric(state, player)


def can_reach_earth_temple_many_mirrors_room(state: CollectionState, player: int) -> bool:
    return can_reach_earth_temple_tall_vine_room(state, player)


def can_reach_wind_temple_kidnapping_room(state: CollectionState, player: int) -> bool:
    return (
        can_play_command_melody(state, player)
        and state.has("Iron Boots", player)
        and can_fly_with_deku_leaf_indoors(state, player)
    )


def can_reach_end_of_wind_temple_many_cyclones_room(state: CollectionState, player: int) -> bool:
    return can_reach_wind_temple_kidnapping_room(state, player) and (
        (
            state.has("Iron Boots", player)
            and can_fan_with_deku_leaf(state, player)
            and can_fly_with_deku_leaf_indoors(state, player)
            and can_cut_grass(state, player)
        )
        or (
            state.has("Hookshot", player)
            and can_defeat_blue_bubbles(state, player)
            and can_fly_with_deku_leaf_indoors(state, player)
        )
        or (
            state.has("Hookshot", player)
            and can_fly_with_deku_leaf_indoors(state, player)
            and state._tww_obscure_1(player)
            and state._tww_precise_2(player)
        )
    )


def can_open_wind_temple_upper_giant_grate(state: CollectionState, player: int) -> bool:
    return can_reach_end_of_wind_temple_many_cyclones_room(state, player) and state.has("Iron Boots", player)


def can_activate_wind_temple_giant_fan(state: CollectionState, player: int) -> bool:
    return can_open_wind_temple_upper_giant_grate(state, player) and can_play_command_melody(state, player)


def can_open_wind_temple_lower_giant_grate(state: CollectionState, player: int) -> bool:
    return (
        can_reach_wind_temple_kidnapping_room(state, player)
        and state.has("Hookshot", player)
        and can_defeat_blue_bubbles(state, player)
    )


def can_reach_wind_temple_tall_basement_room(state: CollectionState, player: int) -> bool:
    return (
        can_open_wind_temple_upper_giant_grate(state, player)
        and can_open_wind_temple_lower_giant_grate(state, player)
        and state.has("WT Small Key", player, 2)
    )


def can_access_dungeon_entrance_on_dragon_roost_island(state: CollectionState, player: int) -> bool:
    return True


def can_access_forest_haven(state: CollectionState, player: int) -> bool:
    return state.has("Grappling Hook", player) or can_fly_with_deku_leaf_outdoors(state, player)


def can_access_dungeon_entrance_in_forest_haven_sector(state: CollectionState, player: int) -> bool:
    return (
        can_access_forest_haven(state, player)
        and (
            state.has("Grappling Hook", player)
            or (
                can_fly_with_deku_leaf_indoors(state, player)
                and can_fly_with_deku_leaf_outdoors(state, player)
                and state._tww_obscure_1(player)
                and state._tww_precise_1(player)
            )
        )
        and can_fly_with_deku_leaf_outdoors(state, player)
        and (can_cut_grass(state, player) or has_magic_meter_upgrade(state, player))
    )


def can_access_dungeon_entrance_in_tower_of_the_gods_sector(state: CollectionState, player: int) -> bool:
    return state.has_group_unique("Pearls", player, 3)


def can_access_dungeon_entrance_in_forsaken_fortress_sector(state: CollectionState, player: int) -> bool:
    return False


def can_access_dungeon_entrance_on_headstone_island(state: CollectionState, player: int) -> bool:
    return state.has("Power Bracelets", player)


def can_access_dungeon_entrance_on_gale_isle(state: CollectionState, player: int) -> bool:
    return state.has_all(["Iron Boots", "Skull Hammer"], player)


def can_access_miniboss_entrance_in_forbidden_woods(state: CollectionState, player: int) -> bool:
    return (
        can_fly_with_deku_leaf_indoors(state, player)
        and can_defeat_boko_babas(state, player)
        and state.has_all(["Grappling Hook", "FW Small Key"], player)
    )


def can_access_miniboss_entrance_in_tower_of_the_gods(state: CollectionState, player: int) -> bool:
    return (
        can_reach_tower_of_the_gods_second_floor(state, player)
        and (state.has("Grappling Hook", player) or can_fly_with_deku_leaf_indoors(state, player))
        and (can_play_command_melody(state, player) or has_heros_bow(state, player))
    )


def can_access_miniboss_entrance_in_earth_temple(state: CollectionState, player: int) -> bool:
    return can_reach_earth_temple_moblins_and_poes_room(state, player) and state.has("ET Small Key", player, 3)


def can_access_miniboss_entrance_in_wind_temple(state: CollectionState, player: int) -> bool:
    return can_open_wind_temple_upper_giant_grate(state, player) and state.has("WT Small Key", player, 2)


def can_access_miniboss_entrance_in_hyrule_castle(state: CollectionState, player: int) -> bool:
    return can_access_hyrule(state, player)


def can_access_boss_entrance_in_dragon_roost_cavern(state: CollectionState, player: int) -> bool:
    return can_reach_dragon_roost_cavern_boss_stairs(state, player) and state.has("DRC Big Key", player)


def can_access_boss_entrance_in_forbidden_woods(state: CollectionState, player: int) -> bool:
    return (
        can_fly_with_deku_leaf_indoors(state, player)
        and can_defeat_boko_babas(state, player)
        and (can_defeat_door_flowers(state, player) or state.has("Grappling Hook", player))
        and can_defeat_mothulas(state, player)
        and state.has("FW Big Key", player)
    )


def can_access_boss_entrance_in_tower_of_the_gods(state: CollectionState, player: int) -> bool:
    return (
        can_reach_tower_of_the_gods_third_floor(state, player)
        and can_defeat_armos(state, player)
        and state.has("TotG Big Key", player)
    )


def can_access_boss_entrance_in_forsaken_fortress(state: CollectionState, player: int) -> bool:
    return (
        can_get_inside_forsaken_fortress(state, player)
        and state.has("Skull Hammer", player)
        and (
            can_fly_with_deku_leaf_indoors(state, player)
            or state.has("Hookshot", player)
            or (state._tww_obscure_2(player) and state._tww_precise_2(player))
        )
        and (
            can_defeat_bokoblins(state, player)
            or can_fly_with_deku_leaf_outdoors(state, player)
            or state.has("Grappling Hook", player)
        )
    )


def can_access_boss_entrance_in_earth_temple(state: CollectionState, player: int) -> bool:
    return can_reach_earth_temple_tall_vine_room(state, player) and state.has("ET Big Key", player)


def can_access_boss_entrance_in_wind_temple(state: CollectionState, player: int) -> bool:
    return (
        can_reach_wind_temple_tall_basement_room(state, player)
        and state.has_all(["Hookshot", "Iron Boots", "WT Big Key"], player)
        and can_play_command_melody(state, player)
        and can_play_wind_gods_aria(state, player)
    )


def can_access_secret_cave_entrance_on_outset_island(state: CollectionState, player: int) -> bool:
    return (
        (can_reach_outset_island_upper_level(state, player) and can_fly_with_deku_leaf_outdoors(state, player))
        or state.has("Hookshot", player)
    ) and state.has("Power Bracelets", player)


def can_access_secret_cave_entrance_on_dragon_roost_island(state: CollectionState, player: int) -> bool:
    return can_move_boulders(state, player)


def can_access_secret_cave_entrance_on_fire_mountain(state: CollectionState, player: int) -> bool:
    return has_ice_arrows(state, player)


def can_access_secret_cave_entrance_on_ice_ring_isle(state: CollectionState, player: int) -> bool:
    return has_fire_arrows(state, player)


def can_access_secret_cave_entrance_on_private_oasis(state: CollectionState, player: int) -> bool:
    return state.has_all(["Delivery Bag", "Cabana Deed", "Grappling Hook"], player)


def can_access_secret_cave_entrance_on_needle_rock_isle(state: CollectionState, player: int) -> bool:
    return has_fire_arrows(state, player)


def can_access_secret_cave_entrance_on_angular_isles(state: CollectionState, player: int) -> bool:
    return can_fly_with_deku_leaf_outdoors(state, player) or state.has("Hookshot", player)


def can_access_secret_cave_entrance_on_boating_course(state: CollectionState, player: int) -> bool:
    return can_fly_with_deku_leaf_outdoors(state, player) or state.has("Hookshot", player)


def can_access_secret_cave_entrance_on_stone_watcher_island(state: CollectionState, player: int) -> bool:
    return state.has("Power Bracelets", player)


def can_access_secret_cave_entrance_on_overlook_island(state: CollectionState, player: int) -> bool:
    return state.has("Hookshot", player)


def can_access_secret_cave_entrance_on_birds_peak_rock(state: CollectionState, player: int) -> bool:
    return state.has("Bait Bag", player)


def can_access_secret_cave_entrance_on_pawprint_isle(state: CollectionState, player: int) -> bool:
    return True


def can_access_secret_cave_entrance_on_pawprint_isle_side_isle(state: CollectionState, player: int) -> bool:
    return state.has("Hookshot", player)


def can_access_secret_cave_entrance_on_diamond_steppe_island(state: CollectionState, player: int) -> bool:
    return state.has("Hookshot", player)


def can_access_secret_cave_entrance_on_bomb_island(state: CollectionState, player: int) -> bool:
    return can_move_boulders(state, player)


def can_access_secret_cave_entrance_on_rock_spire_isle(state: CollectionState, player: int) -> bool:
    return state.has("Bombs", player)


def can_access_secret_cave_entrance_on_shark_island(state: CollectionState, player: int) -> bool:
    return state.has_all(["Iron Boots", "Skull Hammer"], player)


def can_access_secret_cave_entrance_on_cliff_plateau_isles(state: CollectionState, player: int) -> bool:
    return True


def can_access_secret_cave_entrance_on_horseshoe_island(state: CollectionState, player: int) -> bool:
    return can_fan_with_deku_leaf(state, player)


def can_access_secret_cave_entrance_on_star_island(state: CollectionState, player: int) -> bool:
    return can_move_boulders(state, player)


def can_access_inner_entrance_in_ice_ring_isle_secret_cave(state: CollectionState, player: int) -> bool:
    return state.has("Iron Boots", player)


def can_access_inner_entrance_in_cliff_plateau_isles_secret_cave(state: CollectionState, player: int) -> bool:
    return can_defeat_boko_babas(state, player) and can_fly_with_deku_leaf_indoors(state, player)


def can_access_fairy_fountain_entrance_on_outset_island(state: CollectionState, player: int) -> bool:
    return can_access_forest_of_fairies(state, player) and can_move_boulders(state, player)


def can_access_fairy_fountain_entrance_on_thorned_fairy_island(state: CollectionState, player: int) -> bool:
    return state.has("Skull Hammer", player)


def can_access_fairy_fountain_entrance_on_eastern_fairy_island(state: CollectionState, player: int) -> bool:
    return can_move_boulders(state, player)


def can_access_fairy_fountain_entrance_on_western_fairy_island(state: CollectionState, player: int) -> bool:
    return state.has("Skull Hammer", player)


def can_access_fairy_fountain_entrance_on_southern_fairy_island(state: CollectionState, player: int) -> bool:
    return state.has("Bombs", player) or has_fire_arrows(state, player)


def can_access_fairy_fountain_entrance_on_northern_fairy_island(state: CollectionState, player: int) -> bool:
    return True


def can_get_past_forsaken_fortress_gate(state: CollectionState, player: int) -> bool:
    return (
        state.has("Bombs", player)
        or (state._tww_obscure_1(player) and state._tww_precise_1(player))
        or (can_open_ganons_tower_dark_portal(state, player) and state._tww_obscure_1(player))
    )


def can_get_inside_forsaken_fortress(state: CollectionState, player: int) -> bool:
    return can_get_past_forsaken_fortress_gate(state, player) and state.has("Skull Hammer", player)


def can_reach_and_defeat_phantom_ganon(state: CollectionState, player: int) -> bool:
    return can_get_past_forsaken_fortress_gate(state, player) and can_defeat_phantom_ganon(state, player)


def can_defeat_phantom_ganon(state: CollectionState, player: int) -> bool:
    return (state._tww_outside_swordless_mode(player) and has_any_master_sword(state, player)) or (
        state._tww_in_swordless_mode(player) and state.has("Skull Hammer", player)
    )


def can_access_hyrule(state: CollectionState, player: int) -> bool:
    return has_all_8_triforce_shards(state, player)


def can_get_past_hyrule_barrier(state: CollectionState, player: int) -> bool:
    return can_access_hyrule(state, player) and (
        has_full_power_master_sword(state, player) or state._tww_in_swordless_mode(player)
    )


def can_access_ganons_tower(state: CollectionState, player: int) -> bool:
    return can_get_past_hyrule_barrier(state, player) and (
        state.has("Hookshot", player) or can_fly_with_deku_leaf_indoors(state, player)
    )


def can_complete_memory_dragon_roost_cavern_and_gohma(state: CollectionState, player: int) -> bool:
    return (
        state.has("Grappling Hook", player)
        and can_fly_with_deku_leaf_indoors(state, player)
        and can_defeat_gohma(state, player)
    )


def can_complete_memory_forbidden_woods_and_kalle_demos(state: CollectionState, player: int) -> bool:
    return (
        can_fan_with_deku_leaf(state, player)
        and can_fly_with_deku_leaf_indoors(state, player)
        and can_defeat_kalle_demos(state, player)
    )


def can_complete_memory_earth_temple_and_jalhalla(state: CollectionState, player: int) -> bool:
    return can_defeat_jalhalla(state, player)


def can_complete_memory_wind_temple_and_molgera(state: CollectionState, player: int) -> bool:
    return can_fly_with_deku_leaf_indoors(state, player) and can_defeat_molgera(state, player)


def can_complete_all_memory_dungeons_and_bosses(state: CollectionState, player: int) -> bool:
    return (
        can_complete_memory_dragon_roost_cavern_and_gohma(state, player)
        and can_complete_memory_forbidden_woods_and_kalle_demos(state, player)
        and can_complete_memory_earth_temple_and_jalhalla(state, player)
        and can_complete_memory_wind_temple_and_molgera(state, player)
    )


def can_unlock_ganons_tower_four_boss_door(state: CollectionState, player: int) -> bool:
    return can_complete_all_memory_dungeons_and_bosses(state, player) or state._tww_rematch_bosses_skipped(player)


def can_reach_ganons_tower_phantom_ganon_room(state: CollectionState, player: int) -> bool:
    return can_access_ganons_tower(state, player) and can_unlock_ganons_tower_four_boss_door(state, player)


def can_open_ganons_tower_dark_portal(state: CollectionState, player: int) -> bool:
    return can_reach_ganons_tower_phantom_ganon_room(state, player) and state.has("Boomerang", player)


def can_reach_and_defeat_puppet_ganon(state: CollectionState, player: int) -> bool:
    return (
        can_reach_ganons_tower_phantom_ganon_room(state, player)
        and has_light_arrows(state, player)
        and can_unlock_puppet_ganon_door(state, player)
        and can_defeat_puppet_ganon(state, player)
    )


def can_unlock_puppet_ganon_door(state: CollectionState, player: int) -> bool:
    return (
        can_defeat_moblins(state, player)
        and can_defeat_mighty_darknuts(state, player)
        and (
            state._tww_outside_required_bosses_mode(player)
            or (state._tww_in_required_bosses_mode(player) and state._tww_can_defeat_all_required_bosses(player))
        )
    )


def can_defeat_puppet_ganon(state: CollectionState, player: int) -> bool:
    return has_light_arrows(state, player) and (state.has("Boomerang", player) or state._tww_precise_2(player))


def can_reach_and_defeat_ganondorf(state: CollectionState, player: int) -> bool:
    return (
        can_reach_and_defeat_puppet_ganon(state, player)
        and state.has_all(["Grappling Hook", "Hookshot"], player)
        and can_defeat_ganondorf(state, player)
    )


def can_defeat_ganondorf(state: CollectionState, player: int) -> bool:
    return (has_heros_sword(state, player) or state._tww_in_swordless_mode(player)) and (
        has_heros_shield(state, player) or (state.has("Skull Hammer", player) and state._tww_obscure_2(player))
    )


def can_farm_knights_crests(state: CollectionState, player: int) -> bool:
    return state.has_all(["Grappling Hook", "Spoils Bag"], player) and (
        # (Can Access Item Location "Ice Ring Isle - Inner Cave - Chest")
        (state.can_reach_region("Ice Ring Isle Inner Cave", player) and has_fire_arrows(state, player))
        # | (Can Access Item Location "Outset Island - Savage Labyrinth - Floor 30")
        or (
            state.can_reach_region("Savage Labyrinth", player)
            and can_defeat_keese(state, player)
            and can_defeat_miniblins(state, player)
            and can_defeat_red_chuchus(state, player)
            and can_defeat_magtails(state, player)
            and can_defeat_fire_keese(state, player)
            and can_defeat_peahats(state, player)
            and can_defeat_green_chuchus(state, player)
            and can_defeat_boko_babas(state, player)
            and can_defeat_mothulas(state, player)
            and can_defeat_winged_mothulas(state, player)
            and can_defeat_wizzrobes(state, player)
            and can_defeat_armos(state, player)
            and can_defeat_yellow_chuchus(state, player)
            and can_defeat_red_bubbles(state, player)
            and can_defeat_darknuts(state, player)
            and can_play_winds_requiem(state, player)
            and (state.has_any(["Grappling Hook", "Skull Hammer"], player) or has_heros_sword(state, player))
        )
        # | (Can Access Item Location "Earth Temple - Big Key Chest" & Can Defeat Darknuts Easily)
        or (
            state.can_reach_region("Earth Temple", player)
            and can_reach_earth_temple_many_mirrors_room(state, player)
            and state.has("Power Bracelets", player)
            and can_play_command_melody(state, player)
            and can_aim_mirror_shield(state, player)
            and (
                can_defeat_blue_bubbles(state, player)
                or (has_heros_bow(state, player) and state._tww_obscure_1(player))
                or (
                    (
                        has_heros_sword(state, player)
                        or has_any_master_sword(state, player)
                        or state.has("Skull Hammer", player)
                    )
                    and state._tww_obscure_1(player)
                    and state._tww_precise_1(player)
                )
            )
            and can_defeat_darknuts_easily(state, player)
        )
        # | (Can Access Item Location "Wind Temple - Big Key Chest" & Can Defeat Darknuts Easily)
        or (
            state.can_reach_region("Wind Temple", player)
            and can_reach_wind_temple_kidnapping_room(state, player)
            and state.has("Iron Boots", player)
            and can_fan_with_deku_leaf(state, player)
            and can_play_wind_gods_aria(state, player)
            and can_defeat_darknuts_easily(state, player)
        )
        # | (Can Access Item Location "Shark Island - Cave")
        or (state.can_reach_region("Shark Island Secret Cave", player) and can_defeat_miniblins(state, player))
        # | (Can Access Item Location "Stone Watcher Island - Cave" & Can Defeat Darknuts Easily)
        or (
            state.can_reach_region("Stone Watcher Island Secret Cave", player)
            and can_defeat_armos(state, player)
            and can_defeat_wizzrobes(state, player)
            and can_play_winds_requiem(state, player)
            and can_defeat_darknuts_easily(state, player)
        )
        # | (Can Access Item Location "Overlook Island - Cave" & Can Defeat Darknuts Easily)
        or (
            state.can_reach_region("Overlook Island Secret Cave", player)
            and can_defeat_stalfos(state, player)
            and can_defeat_wizzrobes(state, player)
            and can_defeat_red_chuchus(state, player)
            and can_defeat_green_chuchus(state, player)
            and can_defeat_keese(state, player)
            and can_defeat_fire_keese(state, player)
            and can_defeat_morths(state, player)
            and can_defeat_kargarocs(state, player)
            and can_play_winds_requiem(state, player)
            and can_defeat_darknuts_easily(state, player)
        )
        # | (Can Access Hyrule)
        or can_access_hyrule(state, player)
    )


def can_farm_joy_pendants(state: CollectionState, player: int) -> bool:
    return state.has_all(["Grappling Hook", "Spoils Bag"], player)


def can_farm_skull_necklaces(state: CollectionState, player: int) -> bool:
    return state.has_all(["Grappling Hook", "Spoils Bag"], player)


def can_farm_golden_feathers(state: CollectionState, player: int) -> bool:
    return state.has_all(["Grappling Hook", "Spoils Bag"], player)


def can_farm_green_chu_jelly(state: CollectionState, player: int) -> bool:
    return state.has_all(["Grappling Hook", "Spoils Bag"], player)


def can_obtain_15_blue_chu_jelly(state: CollectionState, player: int) -> bool:
    return (
        can_get_blue_chu_jelly_from_blue_chuchus(state, player)
        and (
            state.has_any(["Hookshot", "Bombs", "Grappling Hook"], player)
            or can_move_boulders(state, player)
            or (
                can_access_secret_cave_entrance_on_shark_island(state, player)
                and can_fly_with_deku_leaf_outdoors(state, player)
            )
            or state.can_reach_region("Cliff Plateau Isles Inner Cave", player)
            or can_fan_with_deku_leaf(state, player)
            or can_access_secret_cave_entrance_on_boating_course(state, player)
        )
        and state.has("Spoils Bag", player)
    )


def can_defeat_bokoblins(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Bombs", "Skull Hammer"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_defeat_moblins(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Bombs", "Skull Hammer"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_defeat_darknuts(state: CollectionState, player: int) -> bool:
    return has_heros_sword(state, player) or has_light_arrows(state, player) or state.has("Skull Hammer", player)


def can_defeat_darknuts_easily(state: CollectionState, player: int) -> bool:
    return has_heros_sword(state, player) or has_light_arrows(state, player)


def can_defeat_mighty_darknuts(state: CollectionState, player: int) -> bool:
    return can_defeat_darknuts_easily(state, player) or (
        state.has("Skull Hammer", player) and state._tww_precise_3(player)
    )


def can_defeat_miniblins(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Grappling Hook", "Boomerang", "Bombs", "Skull Hammer"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_defeat_miniblins_easily(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Boomerang", "Bombs", "Skull Hammer"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_defeat_red_chuchus(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Skull Hammer", "Bombs"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_defeat_green_chuchus(state: CollectionState, player: int) -> bool:
    return can_defeat_red_chuchus(state, player)


def can_defeat_yellow_chuchus(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Bombs", "Skull Hammer"], player)
        or (state.has("Boomerang", player) and has_heros_sword(state, player))
        or has_heros_bow(state, player)
        or (can_fan_with_deku_leaf(state, player) and has_heros_sword(state, player))
        or (
            state.has("Grappling Hook", player)
            and has_heros_sword(state, player)
            and state._tww_obscure_1(player)
            and state._tww_precise_2(player)
        )
    )


def can_defeat_blue_chuchus(state: CollectionState, player: int) -> bool:
    return can_defeat_yellow_chuchus(state, player)


def can_get_blue_chu_jelly_from_blue_chuchus(state: CollectionState, player: int) -> bool:
    return can_defeat_blue_chuchus(state, player) or state.has("Grappling Hook", player)


def can_defeat_keese(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Hookshot", "Grappling Hook", "Boomerang", "Bombs", "Skull Hammer"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_defeat_fire_keese(state: CollectionState, player: int) -> bool:
    return can_defeat_keese(state, player)


def can_defeat_magtails(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Skull Hammer", "Boomerang", "Hookshot", "Bombs", "Grappling Hook"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_stun_magtails(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Skull Hammer", "Boomerang", "Hookshot", "Bombs", "Grappling Hook"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_defeat_kargarocs(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Boomerang", "Skull Hammer", "Bombs"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_defeat_peahats(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Boomerang", "Skull Hammer", "Bombs"], player)
        or (state.has("Hookshot", player) and has_heros_sword(state, player))
        or (can_fan_with_deku_leaf(state, player) and has_heros_sword(state, player))
        or has_heros_bow(state, player)
    )


def can_remove_peahat_armor(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Boomerang", "Hookshot", "Skull Hammer", "Bombs"], player)
        or can_fan_with_deku_leaf(state, player)
        or has_heros_bow(state, player)
    )


def can_defeat_seahats(state: CollectionState, player: int) -> bool:
    return state.has_any(["Boomerang", "Hookshot", "Bombs"], player) or has_heros_bow(state, player)


def can_defeat_boko_babas(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Boomerang", "Skull Hammer", "Hookshot", "Bombs"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
        or (can_fan_with_deku_leaf(state, player) and state.has("Grappling Hook", player))
    )


def can_defeat_mothulas(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Bombs", "Skull Hammer"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_defeat_winged_mothulas(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Bombs", "Skull Hammer"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_defeat_wizzrobes(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Hookshot", "Bombs", "Skull Hammer"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_defeat_wizzrobes_at_range(state: CollectionState, player: int) -> bool:
    return has_heros_bow(state, player) or (state.has("Hookshot", player) and state._tww_precise_1(player))


def can_defeat_armos(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Bombs", "Skull Hammer", "Hookshot"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_defeat_big_octos(state: CollectionState, player: int) -> bool:
    return state.has_any(["Bombs", "Boomerang"], player) or has_heros_bow(state, player)


def can_defeat_12_eye_big_octos(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Bombs", "Boomerang"], player)
        or (has_heros_bow(state, player) and has_any_quiver_upgrade(state, player))
        or has_light_arrows(state, player)
    )


def can_defeat_red_bubbles(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Skull Hammer", "Bombs"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
        or (
            (can_fan_with_deku_leaf(state, player) or state.has("Hookshot", player))
            and state.has("Grappling Hook", player)
        )
    )


def can_defeat_blue_bubbles(state: CollectionState, player: int) -> bool:
    return (
        has_ice_arrows(state, player)
        or state.has("Bombs", player)
        or (
            (can_fan_with_deku_leaf(state, player) or state.has("Hookshot", player))
            and (
                state.has_any(["Grappling Hook", "Skull Hammer"], player)
                or has_heros_sword(state, player)
                or has_heros_bow(state, player)
            )
        )
    )


def can_defeat_redeads(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Skull Hammer", "Bombs"], player)
        or has_heros_sword(state, player)
        or has_light_arrows(state, player)
    )


def can_defeat_jalhalla_poes(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Bombs", "Skull Hammer"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_defeat_stalfos(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Bombs", "Skull Hammer"], player)
        or has_heros_sword(state, player)
        or has_light_arrows(state, player)
    )


def can_defeat_floormasters(state: CollectionState, player: int) -> bool:
    return (
        has_heros_sword(state, player)
        or has_heros_bow(state, player)
        or (state.has("Skull Hammer", player) and state._tww_precise_1(player))
    )


def can_defeat_morths(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Boomerang", "Hookshot"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_defeat_bombchus(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Boomerang", "Skull Hammer", "Grappling Hook"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_defeat_gohma(state: CollectionState, player: int) -> bool:
    return state.has("Grappling Hook", player)


def can_defeat_kalle_demos(state: CollectionState, player: int) -> bool:
    return state.has("Boomerang", player)


def can_defeat_gohdan(state: CollectionState, player: int) -> bool:
    return (
        has_heros_bow(state, player)
        or (state.has("Hookshot", player) and state._tww_obscure_1(player) and state._tww_precise_2(player))
    ) and state.has("Bombs", player)


def can_defeat_helmaroc_king(state: CollectionState, player: int) -> bool:
    return state.has("Skull Hammer", player)


def can_defeat_jalhalla(state: CollectionState, player: int) -> bool:
    return (
        (can_aim_mirror_shield(state, player) or has_light_arrows(state, player))
        and state.has("Power Bracelets", player)
        and can_defeat_jalhalla_poes(state, player)
    )


def can_defeat_molgera(state: CollectionState, player: int) -> bool:
    return state.has("Hookshot", player) and (
        state.has_any(["Boomerang", "Grappling Hook", "Skull Hammer", "Bombs"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_destroy_cannons(state: CollectionState, player: int) -> bool:
    return state.has_any(["Bombs", "Boomerang"], player)


def can_cut_down_outset_trees(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Boomerang", "Skull Hammer"], player)
        or has_heros_sword(state, player)
        or (state.has("Power Bracelets", player) and state._tww_obscure_3(player))
    )


def can_cut_down_hanging_drc_platform(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Bombs", "Skull Hammer"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
        or (state.has("Hookshot", player) and state._tww_precise_1(player))
        or (state.has("Grappling Hook", player) and state._tww_precise_1(player))
    )


def can_cut_grass(state: CollectionState, player: int) -> bool:
    return state.has_any(["Skull Hammer", "Boomerang", "Bombs"], player) or has_heros_sword(state, player)


def can_sword_fight_with_orca(state: CollectionState, player: int) -> bool:
    return has_heros_sword(state, player) or state._tww_in_swordless_mode(player)
