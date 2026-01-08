from BaseClasses import CollectionState

############ MACRO NAMING ############
#  has item:        "has_"           #
#  defeat enemies:  "can_defeat_"    #
#  defeat bosses:   "can_beat_"      #
#  beat dungeon:    "can_beat_"      #
#  access region:   "can_access_"    #
#  reach area:      "can_reach_"     #
#  get past area:   "can_pass_"      #
# -------------- misc -------------- #
#  "can_afford_"                     #
#  "can_obtain_"                     #
#  "can_reach_dungeon_entrance_in_"  #
######################################


# Items
def has_practice_sword(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Sword", player, 1)


def has_goddess_sword(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Sword", player, 2)


def has_goddess_longsword(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Sword", player, 3)


def has_goddess_white_sword(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Sword", player, 4)


def has_master_sword(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Sword", player, 5)


def has_true_master_sword(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Sword", player, 6)


def has_beetle(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Beetle", player, 1)


def has_hook_beetle(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Beetle", player, 2)

def has_quick_beetle(state: CollectionState, player: int) -> bool:
    return (
        (state.has("Progressive Beetle", player, 3) and state._ss_option_gondo_upgrades(player))
        or (can_upgrade_to_quick_beetle(state, player) and not state._ss_option_gondo_upgrades(player))
    )

def has_tough_beetle(state: CollectionState, player: int) -> bool:
    return (
        (state.has("Progressive Beetle", player, 4) and state._ss_option_gondo_upgrades(player))
        or (can_upgrade_to_tough_beetle(state, player) and not state._ss_option_gondo_upgrades(player))
    )

def has_bow(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Bow", player, 1)


def has_slingshot(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Slingshot", player, 1)


def has_bug_net(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Bug Net", player, 1)


def has_digging_mitts(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Mitts", player, 1)


def has_mogma_mitts(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Mitts", player, 2)


def has_pouch(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Pouch", player, 1)


def has_medium_wallet(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Wallet", player, 1)


def has_big_wallet(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Wallet", player, 2)


def has_giant_wallet(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Wallet", player, 3)


def has_tycoon_wallet(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Wallet", player, 4)


def has_one_extra_wallet(state: CollectionState, player: int) -> bool:
    return state.has("Extra Wallet", player, 1)


def has_two_extra_wallets(state: CollectionState, player: int) -> bool:
    return state.has("Extra Wallet", player, 2)


def has_three_extra_wallets(state: CollectionState, player: int) -> bool:
    return state.has("Extra Wallet", player, 3)


def has_song_of_the_hero(state: CollectionState, player: int) -> bool:
    return (
        state.has("Faron Song of the Hero Part", player)
        and state.has("Eldin Song of the Hero Part", player)
        and state.has("Lanayru Song of the Hero Part", player)
    )


def has_bottle(state: CollectionState, player: int) -> bool:
    return has_pouch(state, player) and state.has("Empty Bottle", player)


def has_completed_triforce(state: CollectionState, player: int) -> bool:
    return (
        state.has("Triforce of Courage", player)
        and state.has("Triforce of Power", player)
        and state.has("Triforce of Wisdom", player)
    )


# Misc
def upgraded_skyward_strike(state: CollectionState, player: int) -> bool:
    return has_true_master_sword(state, player) or (
        state._ss_option_upgraded_skyward_strike(player)
        and has_goddess_sword(state, player)
    )


def unlocked_endurance_potion(state: CollectionState, player: int) -> bool:
    return can_raise_lmf(state, player)


def damaging_item(state: CollectionState, player: int) -> bool:
    return (
        has_practice_sword(state, player)
        or has_bow(state, player)
        or state.has("Bomb Bag", player)
    )


def projectile_item(state: CollectionState, player: int) -> bool:
    return (
        has_slingshot(state, player)
        or has_beetle(state, player)
        or has_bow(state, player)
    )


def distance_activator(state: CollectionState, player: int) -> bool:
    return projectile_item(state, player) or state.has("Clawshots", player)


def can_cut_trees(state: CollectionState, player: int) -> bool:
    return has_practice_sword(state, player) or state.has("Bomb Bag", player)


def can_unlock_combination_lock(state: CollectionState, player: int) -> bool:
    return (
        has_practice_sword(state, player)
        or has_bow(state, player)
        or state.has("Whip", player)
        or state.has("Clawshots", player)
    )


def can_hit_timeshift_stone(state: CollectionState, player: int) -> bool:
    return (
        distance_activator(state, player)
        or has_practice_sword(state, player)
        or state.has("Whip", player)
        or state.has("Bomb Bag", player)
    )

def can_upgrade_to_quick_beetle(state: CollectionState, player: int) -> bool:
    return(
        has_hook_beetle(state, player)
        and can_access_deep_woods(state, player) # Larvae farming
        and (
            lanayru_mine_ancient_flower_farming(state, player)
            or lanayru_desert_ancient_flower_farming(state, player)
            or lanayru_desert_ancient_flower_farming_near_main_node(state, player)
            or pirate_stronghold_ancient_flower_farming(state, player)
            or lanayru_gorge_ancient_flower_farming(state, player)
        ) # Ancient flower farming
        and clean_cut_minigame(state, player) # Gold Skull farming
    )

def can_upgrade_to_tough_beetle(state: CollectionState, player: int) -> bool:
    return(
        can_upgrade_to_quick_beetle(state, player)
        and can_reach_most_of_faron_woods(state, player) # Amber relic farming
        and (
            lanayru_mine_ancient_flower_farming(state, player)
            or lanayru_desert_ancient_flower_farming(state, player)
            or lanayru_desert_ancient_flower_farming_near_main_node(state, player)
            or pirate_stronghold_ancient_flower_farming(state, player)
            or lanayru_gorge_ancient_flower_farming(state, player)
        ) # Ancient flower farming
        and clean_cut_minigame(state, player) # Plume/Blue feather farming
    )


# Can Defeat
def can_defeat_bokoblins(state: CollectionState, player: int) -> bool:
    return damaging_item(state, player)


def can_defeat_moblins(state: CollectionState, player: int) -> bool:
    return damaging_item(state, player)


def can_defeat_keeses(state: CollectionState, player: int) -> bool:
    return (
        damaging_item(state, player)
        or has_slingshot(state, player)
        or has_beetle(state, player)
        or state.has("Whip", player)
        or state.has("Clawshots", player)
    )


def can_defeat_lezalfos(state: CollectionState, player: int) -> bool:
    return has_practice_sword(state, player) or state.has("Bomb Bag", player)


def can_defeat_ampilus(state: CollectionState, player: int) -> bool:
    return damaging_item(state, player)


def can_defeat_moldarachs(state: CollectionState, player: int) -> bool:
    return state.has("Gust Bellows", player) and has_practice_sword(state, player)


def can_defeat_armos(state: CollectionState, player: int) -> bool:
    return state.has("Gust Bellows", player) and has_practice_sword(state, player)


def can_defeat_beamos(state: CollectionState, player: int) -> bool:
    return has_practice_sword(state, player) or has_bow(state, player)


def can_defeat_cursed_bokoblins(state: CollectionState, player: int) -> bool:
    return has_practice_sword(state, player) or state.has("Bomb Bag", player)


def can_defeat_stalfos(state: CollectionState, player: int) -> bool:
    return has_practice_sword(state, player)


def can_defeat_stalmaster(state: CollectionState, player: int) -> bool:
    return has_practice_sword(state, player)


# Crystals
def can_access_batreauxs_house(state: CollectionState, player: int) -> bool:
    return can_access_skyloft_village(state, player)


def can_obtain_5_loose_crystals(state: CollectionState, player: int) -> bool:
    return can_access_central_skyloft(state, player)


def can_obtain_10_loose_crystals(state: CollectionState, player: int) -> bool:
    return (
        can_access_central_skyloft(state, player)
        and can_access_sky(state, player)
        and (
            can_cut_trees(state, player)  # 2 crystals past waterfall cave
            or state.has("Clawshots", player)  # Zelda's room, atop waterfall
            or has_beetle(state, player)
        )  # Sparring hall, beedle's island
    )


def can_obtain_15_loose_crystals(state: CollectionState, player: int) -> bool:
    return (
        can_access_central_skyloft(state, player)
        and can_access_sky(state, player)
        and (can_cut_trees(state, player) or has_beetle(state, player))
        and state.has("Clawshots", player)
        and has_beetle(state, player)
    )


def five_gratitude_crystals(state: CollectionState, player: int) -> bool:
    return can_obtain_5_loose_crystals(state, player) or state.has(
        "Gratitude Crystal Pack", player, 1
    )


def ten_gratitude_crystals(state: CollectionState, player: int) -> bool:
    return (
        can_obtain_10_loose_crystals(state, player)
        or (
            can_obtain_5_loose_crystals(state, player)
            and state.has("Gratitude Crystal Pack", player, 1)
        )
        or state.has("Gratitude Crystal Pack", player)
    )


def thirty_gratitude_crystals(state: CollectionState, player: int) -> bool:
    return (
        (
            can_obtain_15_loose_crystals(state, player)
            and state.has("Gratitude Crystal Pack", player, 3)
        )
        or (
            can_obtain_10_loose_crystals(state, player)
            and state.has("Gratitude Crystal Pack", player, 4)
        )
        or (
            can_obtain_5_loose_crystals(state, player)
            and state.has("Gratitude Crystal Pack", player, 5)
        )
        or state.has("Gratitude Crystal Pack", player, 6)
    )


def forty_gratitude_crystals(state: CollectionState, player: int) -> bool:
    return (
        (
            can_obtain_15_loose_crystals(state, player)
            and state.has("Gratitude Crystal Pack", player, 5)
        )
        or (
            can_obtain_10_loose_crystals(state, player)
            and state.has("Gratitude Crystal Pack", player, 6)
        )
        or (
            can_obtain_5_loose_crystals(state, player)
            and state.has("Gratitude Crystal Pack", player, 7)
        )
        or state.has("Gratitude Crystal Pack", player, 8)
    )


def fifty_gratitude_crystals(state: CollectionState, player: int) -> bool:
    return (
        (
            can_obtain_15_loose_crystals(state, player)
            and state.has("Gratitude Crystal Pack", player, 7)
        )
        or (
            can_obtain_10_loose_crystals(state, player)
            and state.has("Gratitude Crystal Pack", player, 8)
        )
        or (
            can_obtain_5_loose_crystals(state, player)
            and state.has("Gratitude Crystal Pack", player, 9)
        )
        or state.has("Gratitude Crystal Pack", player, 10)
    )


def seventy_gratitude_crystals(state: CollectionState, player: int) -> bool:
    return (
        (
            can_obtain_15_loose_crystals(state, player)
            and state.has("Gratitude Crystal Pack", player, 11)
        )
        or (
            can_obtain_10_loose_crystals(state, player)
            and state.has("Gratitude Crystal Pack", player, 12)
        )
        or (
            can_obtain_5_loose_crystals(state, player)
            and state.has("Gratitude Crystal Pack", player, 13)
        )
    )


def eighty_gratitude_crystals(state: CollectionState, player: int) -> bool:
    return can_obtain_15_loose_crystals(state, player) and state.has(
        "Gratitude Crystal Pack", player, 13
    )


# Rupees
def can_access_beedles_shop(state: CollectionState, player: int) -> bool:
    return distance_activator(state, player)


def can_afford_300_rupees(state: CollectionState, player: int) -> bool:
    return can_medium_rupee_farm(state, player)


def can_afford_600_rupees(state: CollectionState, player: int) -> bool:
    return can_high_rupee_farm(state, player) and (
        has_big_wallet(state, player) or has_one_extra_wallet(state, player)
    )


def can_afford_800_rupees(state: CollectionState, player: int) -> bool:
    return can_high_rupee_farm(state, player) and (
        has_big_wallet(state, player)
        or has_two_extra_wallets(state, player)
        or (has_medium_wallet(state, player) and has_one_extra_wallet(state, player))
    )


def can_afford_1000_rupees(state: CollectionState, player: int) -> bool:
    return can_high_rupee_farm(state, player) and (
        has_big_wallet(state, player)
        or has_three_extra_wallets(state, player)
        or (has_medium_wallet(state, player) and has_two_extra_wallets(state, player))
    )


def can_afford_1200_rupees(state: CollectionState, player: int) -> bool:
    return can_high_rupee_farm(state, player) and (
        has_giant_wallet(state, player)
        or has_three_extra_wallets(state, player)
        or (has_big_wallet(state, player) and has_one_extra_wallet(state, player))
        or (has_medium_wallet(state, player) and has_three_extra_wallets(state, player))
    )


def can_afford_1600_rupees(state: CollectionState, player: int) -> bool:
    return can_high_rupee_farm(state, player) and (
        has_giant_wallet(state, player)
        or (has_big_wallet(state, player) and has_two_extra_wallets(state, player))
    )


def can_medium_rupee_farm(state: CollectionState, player: int) -> bool:
    return (
        clean_cut_minigame(state, player) and can_access_skyloft_village(state, player)
    ) or can_high_rupee_farm(state, player)


def can_high_rupee_farm(state: CollectionState, player: int) -> bool:
    return fun_fun_minigame(state, player) or thrill_digger_minigame(state, player)


def clean_cut_minigame(state: CollectionState, player: int) -> bool:
    return can_access_sky(state, player) and has_practice_sword(state, player)


def fun_fun_minigame(state: CollectionState, player: int) -> bool:
    return can_access_sky(state, player) and can_retrieve_party_wheel(state, player)


def thrill_digger_minigame(state: CollectionState, player: int) -> bool:
    return can_reach_second_part_of_eldin_volcano(state, player) and has_digging_mitts(
        state, player
    )


### SKY REGION
# Skyloft
def can_access_upper_skyloft(state: CollectionState, player: int) -> bool:
    return True


def can_access_central_skyloft(state: CollectionState, player: int) -> bool:
    return True


def can_access_skyloft_village(state: CollectionState, player: int) -> bool:
    return True


def can_reach_dungeon_entrance_on_skyloft(state: CollectionState, player: int) -> bool:
    return (
        can_access_central_skyloft(state, player)
        and state.has("Stone of Trials", player)
        and state.has("Clawshots", player)
    )


def can_open_trial_gate_on_skyloft(state: CollectionState, player: int) -> bool:
    return (
        can_access_central_skyloft(state, player)
        and has_song_of_the_hero(state, player)
        and state.has("Goddess's Harp", player)
    )


# Sky
def can_access_sky(state: CollectionState, player: int) -> bool:
    return True


def can_save_orielle(state: CollectionState, player: int) -> bool:
    return has_bottle(state, player)


# Thunderhead
def can_access_thunderhead(state: CollectionState, player: int) -> bool:
    return (
        state._ss_option_thunderhead_ballad(player)
        and state.has("Ballad of the Goddess", player)
    ) or state._ss_option_thunderhead_open(player)


### Faron
# Sealed Grounds
def can_access_sealed_grounds(state: CollectionState, player: int) -> bool:
    return can_access_sky(state, player) and state.has("Emerald Tablet", player)


def can_reach_sealed_temple(state: CollectionState, player: int) -> bool:
    return can_access_sealed_grounds(state, player)


def can_raise_gate_of_time(state: CollectionState, player: int) -> bool:
    return state.has("Goddess's Harp", player)


# Past
def can_reach_past(state: CollectionState, player: int) -> bool:
    return (
        can_reach_sealed_temple(state, player)
        and can_raise_gate_of_time(state, player)
        and state._ss_sword_requirement_met(player)
        and (state._ss_can_beat_required_dungeons(player) or state._ss_option_unrequired_dungeons(player))
    )


def can_access_hylias_realm(state: CollectionState, player: int) -> bool:
    return can_reach_past(state, player) and (
        state._ss_option_no_triforce(player) or has_completed_triforce(state, player)
    )


def can_reach_and_defeat_demise(state: CollectionState, player: int) -> bool:
    return can_access_hylias_realm(state, player)


# Faron Woods
def can_access_faron_woods(state: CollectionState, player: int) -> bool:
    return can_reach_sealed_temple(state, player)


def can_reach_most_of_faron_woods(state: CollectionState, player: int) -> bool:
    return (
        can_access_faron_woods(state, player)
        and (
            can_cut_trees(state, player)
            or state.has("Clawshots", player)
        )
    )


def can_reach_oolo(state: CollectionState, player: int) -> bool:
    return (
        (
            can_access_faron_woods(state, player)
            or can_access_flooded_faron_woods(state, player)
        )
        and can_reach_most_of_faron_woods(state, player)
        and state.has("Bomb Bag", player)
    )


def can_reach_great_tree(state: CollectionState, player: int) -> bool:
    return can_reach_most_of_faron_woods(state, player) and state.has(
        "Water Dragon's Scale", player
    )


def can_reach_top_of_great_tree(state: CollectionState, player: int) -> bool:
    return (
        can_reach_most_of_faron_woods(state, player) and state.has("Clawshots", player)
    ) or (can_reach_great_tree(state, player) and state.has("Gust Bellows", player))


def can_talk_to_yerbal(state: CollectionState, player: int) -> bool:
    return can_reach_top_of_great_tree(state, player) and (
        has_slingshot(state, player) or has_beetle(state, player)
    )


def can_open_trial_gate_in_faron_woods(state: CollectionState, player: int) -> bool:
    return (
        can_reach_most_of_faron_woods(state, player)
        and state.has("Farore's Courage", player)
        and state.has("Goddess's Harp", player)
    )


def goddess_cube_on_east_great_tree_with_clawshot_target(
    state: CollectionState, player: int
) -> bool:
    return (
        can_reach_most_of_faron_woods(state, player)
        and (
            state.has("Clawshots", player) or can_reach_top_of_great_tree(state, player)
        )
        and has_goddess_sword(state, player)
    )


def goddess_cube_on_east_great_tree_with_rope(
    state: CollectionState, player: int
) -> bool:
    return can_reach_top_of_great_tree(state, player) and has_goddess_sword(
        state, player
    )


def goddess_cube_on_west_great_tree_near_exit(
    state: CollectionState, player: int
) -> bool:
    return can_reach_top_of_great_tree(state, player) and has_goddess_sword(
        state, player
    )


# Deep Woods
def can_access_deep_woods(state: CollectionState, player: int) -> bool:
    return can_reach_most_of_faron_woods(state, player) and (
        distance_activator(state, player) or state.has("Bomb Bag", player)
    )


def can_reach_deep_woods_after_beehive(state: CollectionState, player: int) -> bool:
    return can_access_deep_woods(state, player) and (
        distance_activator(state, player)
        or has_goddess_sword(state, player)
        or state.has("Bomb Bag", player)
    )


def can_reach_dungeon_entrance_in_deep_woods(
    state: CollectionState, player: int
) -> bool:
    return can_reach_deep_woods_after_beehive(state, player) and distance_activator(
        state, player
    )


def initial_goddess_cube(state: CollectionState, player: int) -> bool:
    return can_reach_deep_woods_after_beehive(state, player) and has_goddess_sword(
        state, player
    )


def goddess_cube_in_deep_woods(state: CollectionState, player: int) -> bool:
    return can_reach_deep_woods_after_beehive(state, player) and has_goddess_sword(
        state, player
    )


def goddess_cube_on_top_on_skyview(state: CollectionState, player: int) -> bool:
    return (
        can_reach_dungeon_entrance_in_deep_woods(state, player)
        and state.has("Clawshots", player)
        and has_goddess_sword(state, player)
    )


# Lake Floria
def can_access_lake_floria(state: CollectionState, player: int) -> bool:
    return (
        can_reach_most_of_faron_woods(state, player)
        and state.has("Water Dragon's Scale", player)
        and (
            (can_talk_to_yerbal(state, player) and has_goddess_sword(state, player))
            or (
                can_talk_to_yerbal(state, player)
                and state._ss_option_lake_floria_yerbal(player)
            )
            or state._ss_option_lake_floria_open(player)
        )
    )


def can_reach_floria_waterfall(state: CollectionState, player: int) -> bool:
    return can_access_lake_floria(state, player)


def can_reach_dungeon_entrance_in_lake_floria(
    state: CollectionState, player: int
) -> bool:
    return can_reach_floria_waterfall(state, player) and state.has(
        "Water Dragon's Scale", player
    )


def goddess_cube_in_lake_floria(state: CollectionState, player: int) -> bool:
    return can_access_lake_floria(state, player) and has_goddess_sword(state, player)


def goddess_cube_in_floria_waterfall(state: CollectionState, player: int) -> bool:
    return (
        can_reach_floria_waterfall(state, player)
        and state.has("Clawshots", player)
        and has_goddess_sword(state, player)
    )


# Flooded Faron Woods
def can_access_flooded_faron_woods(state: CollectionState, player: int) -> bool:
    return can_reach_top_of_great_tree(state, player)


### Eldin
# Eldin Volcano
def can_access_eldin_volcano(state: CollectionState, player: int) -> bool:
    return can_access_sky(state, player) and state.has("Ruby Tablet", player)


def can_reach_second_part_of_eldin_volcano(state: CollectionState, player: int) -> bool:
    return can_access_eldin_volcano(state, player) and (
        can_reach_second_part_of_mogma_turf(state, player)
        or (state.has("Bomb Bag", player) or has_hook_beetle(state, player))
    )


def can_survive_eldin_hot_cave(state: CollectionState, player: int) -> bool:
    return state.has(
        "Fireshield Earrings", player
    ) or state._ss_option_damage_multiplier_under_12(player)


def can_open_trial_gate_in_eldin_volcano(state: CollectionState, player: int) -> bool:
    return (
        can_reach_second_part_of_eldin_volcano(state, player)
        and state.has("Din's Power", player)
        and state.has("Goddess's Harp", player)
    )


def can_reach_dungeon_entrance_in_eldin_volcano(
    state: CollectionState, player: int
) -> bool:
    return can_reach_second_part_of_eldin_volcano(state, player) and state.has(
        "Key Piece", player, 5
    )


def goddess_cube_at_eldin_entrance(state: CollectionState, player: int) -> bool:
    return can_access_eldin_volcano(state, player) and has_goddess_sword(state, player)


def goddess_cube_near_mogma_turf_entrance(state: CollectionState, player: int) -> bool:
    return (
        can_access_eldin_volcano(state, player)
        or (can_access_bokoblin_base(state, player) and has_mogma_mitts(state, player))
    ) and has_goddess_sword(state, player)


def goddess_cube_on_sand_slide(state: CollectionState, player: int) -> bool:
    return (
        can_reach_second_part_of_eldin_volcano(state, player)
        and can_survive_eldin_hot_cave(state, player)
        and has_goddess_sword(state, player)
    )


def goddess_cube_east_of_earth_temple_entrance(
    state: CollectionState, player: int
) -> bool:
    return (
        can_reach_second_part_of_eldin_volcano(state, player)
        or (
            can_access_bokoblin_base(state, player)
            and has_mogma_mitts(state, player)
            and state.has("Clawshots", player)
            and (
                state.has("Bomb Bag", player)
                or (
                    can_bypass_boko_base_watchtower(state, player)
                    and state.has("Whip", player)
                )
            )
        )
    ) and has_goddess_sword(state, player)


def goddess_cube_west_of_earth_temple_entrance(
    state: CollectionState, player: int
) -> bool:
    return (
        (
            can_reach_second_part_of_eldin_volcano(state, player)
            and has_digging_mitts(state, player)
        )
        or (
            can_access_bokoblin_base(state, player)
            and has_mogma_mitts(state, player)
            and state.has("Clawshots", player)
            and (
                state.has("Bomb Bag", player)
                or can_bypass_boko_base_watchtower(state, player)
                and state.has("Whip", player)
            )
        )
    ) and has_goddess_sword(state, player)


# Mogma Turf
def can_access_mogma_turf(state: CollectionState, player: int) -> bool:
    return can_access_eldin_volcano(state, player)


def can_reach_second_part_of_mogma_turf(state: CollectionState, player: int) -> bool:
    return can_access_mogma_turf(state, player) and has_digging_mitts(state, player)


def goddess_cube_in_mogma_turf(state: CollectionState, player: int) -> bool:
    return can_access_mogma_turf(state, player) and has_goddess_sword(state, player)


# Volcano Summit
def can_access_volcano_summit(state: CollectionState, player: int) -> bool:
    return can_reach_second_part_of_eldin_volcano(state, player) and state.has(
        "Fireshield Earrings", player
    )


def can_pass_volcano_summit_first_frog(state: CollectionState, player: int) -> bool:
    return can_access_volcano_summit(state, player) and has_bottle(state, player)


def can_pass_volcano_summit_second_frog(state: CollectionState, player: int) -> bool:
    return can_pass_volcano_summit_first_frog(state, player) and state.has(
        "Clawshots", player
    )


def can_reach_dungeon_entrance_in_volcano_summit(
    state: CollectionState, player: int
) -> bool:
    return can_pass_volcano_summit_second_frog(state, player)


def goddess_cube_inside_volcano_summit(state: CollectionState, player: int) -> bool:
    return (
        can_access_volcano_summit(state, player)
        and (
            upgraded_skyward_strike(state, player)
            or (
                can_access_bokoblin_base(state, player)
                and has_mogma_mitts(state, player)
                and state.has("Clawshots", player)
                and state.has("Bomb Bag", player)
                and state.has("Fireshield Earrings", player)
            )
        )
        and has_goddess_sword(state, player)
    )


def goddess_cube_in_summit_waterfall(state: CollectionState, player: int) -> bool:
    return can_access_volcano_summit(state, player) and has_goddess_sword(state, player)


def goddess_cube_near_fire_sanctuary_entrance(
    state: CollectionState, player: int
) -> bool:
    return (
        can_pass_volcano_summit_second_frog(state, player)
        and state.has("Clawshots", player)
        and has_goddess_sword(state, player)
    )


# Boko Base
def can_access_bokoblin_base(state: CollectionState, player: int) -> bool:
    return can_access_eldin_volcano(state, player)


def can_bypass_boko_base_watchtower(state: CollectionState, player: int) -> bool:
    return (
        state.has("Bomb Bag", player)
        or has_slingshot(state, player)
        or has_bow(state, player)
    )


### LANAYRU


# Lanayru Mine
def can_access_lanayru_mine(state: CollectionState, player: int) -> bool:
    return state.has("Amber Tablet", player)


def can_reach_second_part_of_lanayru_mine(state: CollectionState, player: int) -> bool:
    return (
        can_access_lanayru_mine(state, player)
        and can_hit_timeshift_stone(state, player)
        and (
            state.has("Bomb Bag", player)
            or has_hook_beetle(state, player)
            or False  # (unlocked_endurance_potion(state, player) and has_bottle(state, player))
        )  # Line above is recursive, AP doesn't like that :c
    )


def goddess_cube_at_lanayru_mine_entrance(state: CollectionState, player: int) -> bool:
    return can_access_lanayru_mine(state, player) and has_goddess_sword(state, player)


# Lanayru Desert
def can_access_lanayru_desert(state: CollectionState, player: int) -> bool:
    return can_reach_second_part_of_lanayru_mine(state, player) or (
        can_access_lanayru_mine(state, player) and state.has("Clawshots", player)
    )


def can_retrieve_party_wheel(state: CollectionState, player: int) -> bool:
    return (
        can_access_lanayru_desert(state, player)
        and state.has("Scrapper", player)
        and state.has("Bomb Bag", player)
    )


def can_reach_temple_of_time(state: CollectionState, player: int) -> bool:
    return can_access_lanayru_desert(state, player) and (
        state.has("Clawshots", player) or has_hook_beetle(state, player)
    )


def can_reach_second_part_of_lanayru_desert(
    state: CollectionState, player: int
) -> bool:
    return can_access_lanayru_desert(state, player) and (
        state.has("Clawshots", player)
        or can_reach_temple_of_time(state, player)
        or state._ss_option_lmf_open(player)
    )


def can_activate_nodes(state: CollectionState, player: int) -> bool:
    return (
        can_reach_second_part_of_lanayru_desert(state, player)
        and state.has("Bomb Bag", player)
        and has_practice_sword(state, player)
        and can_defeat_ampilus(state, player)
        and has_hook_beetle(state, player)
    )


def can_raise_lmf(state: CollectionState, player: int) -> bool:
    return can_access_lanayru_desert(state, player) and (
        state._ss_option_lmf_open(player)
        or (
            state._ss_option_lmf_main_node(player)
            and can_reach_second_part_of_lanayru_desert(state, player)
        )
        or can_activate_nodes(state, player)
    )


def can_open_trial_gate_in_lanayru_desert(state: CollectionState, player: int) -> bool:
    return (
        can_reach_second_part_of_lanayru_desert(state, player)
        and state.has("Nayru's Wisdom", player)
        and state.has("Goddess's Harp", player)
    )


def can_reach_dungeon_entrance_in_lanayru_desert(
    state: CollectionState, player: int
) -> bool:
    return can_raise_lmf(state, player)


def goddess_cube_near_caged_robot(state: CollectionState, player: int) -> bool:
    return (
        can_access_lanayru_desert(state, player)
        and state.has("Clawshots", player)
        and has_goddess_sword(state, player)
    )


def goddess_cube_in_secret_passageway(state: CollectionState, player: int) -> bool:
    return (
        can_reach_second_part_of_lanayru_desert(state, player)
        and state.has("Clawshots", player)
        and state.has("Bomb Bag", player)
        and has_goddess_sword(state, player)
    )


def goddess_cube_in_sand_oasis(state: CollectionState, player: int) -> bool:
    return can_reach_temple_of_time(state, player) and has_goddess_sword(state, player)


def goddess_cube_at_ride_near_temple_of_time(
    state: CollectionState, player: int
) -> bool:
    return can_reach_temple_of_time(state, player) and has_goddess_sword(state, player)


# Lanayru Caves
def can_access_lanayru_caves(state: CollectionState, player: int) -> bool:
    return can_access_lanayru_mine(state, player) and state.has("Clawshots", player)


# Lanayru Gorge
def can_access_lanayru_gorge(state: CollectionState, player: int) -> bool:
    return can_access_lanayru_caves(state, player)


def goddess_cube_in_lanayru_gorge(state: CollectionState, player: int) -> bool:
    return (
        can_access_lanayru_gorge(state, player)
        and can_hit_timeshift_stone(state, player)
        and has_goddess_sword(state, player)
    )


# Lanayru Sand Sea
def can_access_lanayru_sand_sea(state: CollectionState, player: int) -> bool:
    return (
        can_access_lanayru_caves(state, player)
        and state.has("Lanayru Caves Small Key", player)
        and state.has("Clawshots", player)
    )


def can_reach_dungeon_entrance_in_lanayru_sand_sea(
    state: CollectionState, player: int
) -> bool:
    return (
        can_access_lanayru_sand_sea(state, player)
        and state.has("Sea Chart", player)
        and has_practice_sword(state, player)
    )


def goddess_cube_in_ancient_harbour(state: CollectionState, player: int) -> bool:
    return (
        can_access_lanayru_sand_sea(state, player)
        and state.has("Clawshots", player)
        and has_goddess_sword(state, player)
    )


def goddess_cube_in_skippers_retreat(state: CollectionState, player: int) -> bool:
    return (
        can_access_lanayru_sand_sea(state, player)
        and (state.has("Bomb Bag", player) or has_hook_beetle(state, player))
        and state.has("Clawshots", player)
        and has_goddess_sword(state, player)
    )


def goddess_cube_in_pirate_stronghold(state: CollectionState, player: int) -> bool:
    return (
        can_access_lanayru_sand_sea(state, player)
        and can_defeat_beamos(state, player)
        and can_defeat_armos(state, player)
        and has_goddess_sword(state, player)
    )


# Ancient Flowers
def lanayru_mine_ancient_flower_farming(state: CollectionState, player: int) -> bool:
    return can_access_lanayru_mine(state, player) and can_hit_timeshift_stone(
        state, player
    )


def lanayru_desert_ancient_flower_farming(state: CollectionState, player: int) -> bool:
    return can_access_lanayru_desert(state, player) and state.has("Bomb Bag", player)


def lanayru_desert_ancient_flower_farming_near_main_node(
    state: CollectionState, player: int
) -> bool:
    return can_reach_second_part_of_lanayru_desert(state, player) and (
        has_hook_beetle(state, player) or state.has("Bomb Bag", player)
    )


def pirate_stronghold_ancient_flower_farming(
    state: CollectionState, player: int
) -> bool:
    return can_access_lanayru_sand_sea(state, player)


def lanayru_gorge_ancient_flower_farming(state: CollectionState, player: int) -> bool:
    return (
        can_access_lanayru_gorge(state, player)
        and state.has("Gust Bellows", player)
        and can_hit_timeshift_stone(state, player)
    )


### DUNGEONS

# Skyview


def can_reach_SV_second_room(state: CollectionState, player: int) -> bool:
    return (
        state.can_reach_region("Skyview", player)
        and can_cut_trees(state, player)
        and (
            state.has("Water Dragon's Scale", player)  # Skyview 2
            or state.has("Bomb Bag", player)  # Bomb the barricade
            or (
                distance_activator(state, player) and has_practice_sword(state, player)
            )  # One eye room
        )
    )


def can_reach_SV_main_room(state: CollectionState, player: int) -> bool:
    return (
        can_reach_SV_second_room(state, player)
        and state.has("Skyview Small Key", player)
        and (
            distance_activator(state, player)
            or has_goddess_sword(state, player)  # Only have to raise water level once
            or state.has(
                "Whip", player
            )  # Whip and goddess sword can hit vines in left room
        )
    )


def can_reach_SV_boss_door(state: CollectionState, player: int) -> bool:
    return (
        can_reach_SV_second_room(state, player)
        and state.has("Skyview Small Key", player, 2)
        and (
            has_practice_sword(state, player) or state.has("Bomb Bag", player)
        )  # Staldra fight
        and (
            has_goddess_sword(state, player)  # Hanging Skulltula
            or has_beetle(state, player)  # Break web with beetle or bow
            or has_bow(state, player)  # Knock away with skyward strike or bombs
            or state.has("Water Dragon's Scale", player)  # Doesn't exist in skyview 2
            or state.has("Bomb Bag", player)
        )
        and (
            upgraded_skyward_strike(state, player)
            or has_hook_beetle(state, player)
            or has_bow(state, player)  # Archers in last room in skyview 2
        )
    )


def can_beat_ghirahim_1(state: CollectionState, player: int) -> bool:
    return (
        can_reach_SV_boss_door(state, player)
        and state.has("Skyview Boss Key", player)
        and has_practice_sword(state, player)
    )


def can_beat_SV(state: CollectionState, player: int) -> bool:
    return can_beat_ghirahim_1(state, player) and has_goddess_sword(state, player)


def goddess_cube_in_skyview_spring(state: CollectionState, player: int) -> bool:
    return can_beat_ghirahim_1(state, player) and has_goddess_sword(state, player)


# Earth Temple
def can_lower_ET_drawbridge(state: CollectionState, player: int) -> bool:
    return has_bow(state, player) or has_beetle(state, player)


def can_dislodge_ET_boulder(state: CollectionState, player: int) -> bool:
    return (
        has_slingshot(state, player)
        or has_bow(state, player)
        or upgraded_skyward_strike(state, player)
        or state.has("Clawshots", player)
        or (has_beetle(state, player) and can_defeat_lezalfos(state, player))
    )


def can_reach_ET_main_room(state: CollectionState, player: int) -> bool:
    return (
        state.can_reach_region("Earth Temple", player)
        and can_lower_ET_drawbridge(state, player)
        and can_dislodge_ET_boulder(state, player)
    )


def can_pass_ET_boulder_section(state: CollectionState, player: int) -> bool:
    return (
        can_reach_ET_main_room(state, player)
        and has_beetle(state, player)
        and (has_hook_beetle(state, player) or state.has("Bomb Bag", player))
    )


def can_reach_ET_boss_door(state: CollectionState, player: int) -> bool:
    return can_pass_ET_boulder_section(state, player) and (
        has_hook_beetle(state, player)
        or (has_digging_mitts(state, player) and state.has("Bomb Bag", player))
    )


def can_beat_scaldera(state: CollectionState, player: int) -> bool:
    return (
        can_reach_ET_boss_door(state, player)
        and state.has("Earth Temple Boss Key", player)
        and state.has("Bomb Bag", player)
        and has_practice_sword(state, player)
    )


def can_beat_ET(state: CollectionState, player: int) -> bool:
    return can_beat_scaldera(state, player) and has_goddess_sword(state, player)


# Lanayru Mining Facility
def can_reach_LMF_second_room(state: CollectionState, player: int) -> bool:
    return state.can_reach_region(
        "Lanayru Mining Facility", player
    ) and has_hook_beetle(state, player)


def can_reach_LMF_key_locked_room_in_past(state: CollectionState, player: int) -> bool:
    return (
        can_reach_LMF_second_room(state, player)
        and state.has("Lanayru Mining Facility Small Key", player)
        and has_hook_beetle(state, player)
    )


def can_reach_LMF_hub_room(state: CollectionState, player: int) -> bool:
    return can_reach_LMF_second_room(state, player)


def can_reach_LMF_hub_room_west(state: CollectionState, player: int) -> bool:
    return (
        can_reach_LMF_second_room(state, player)
        and state.has("Gust Bellows", player)
        and can_defeat_beamos(state, player)
        and can_defeat_armos(state, player)
        and (
            has_goddess_sword(state, player)
            or has_slingshot(state, player)
            or has_bow(state, player)
            or state.has("Whip", player)  # to hit timeshift stone
        )
    )


def can_reach_LMF_boss_door(state: CollectionState, player: int) -> bool:
    return can_reach_LMF_hub_room_west(state, player) and state.has(
        "Gust Bellows", player
    )


def can_pass_LMF_boss_key_room(state: CollectionState, player: int) -> bool:
    return (
        can_reach_LMF_boss_door(state, player)
        and state.has("Gust Bellows", player)
        and state.has("Bomb Bag", player)  # Bombs uncover statues
        and can_defeat_beamos(state, player)
        and can_defeat_armos(state, player)
        and (
            has_practice_sword(state, player) or distance_activator(state, player)
        )  # Hit crystals
    )


def can_beat_moldarach(state: CollectionState, player: int) -> bool:
    return (
        can_reach_LMF_boss_door(state, player)
        and state.has("Lanayru Mining Facility Boss Key", player)
        and can_defeat_moldarachs(state, player)
    )


def can_beat_LMF(state: CollectionState, player: int) -> bool:
    return can_beat_moldarach(state, player) and (
        has_beetle(state, player) or has_bow(state, player)
    )  # To hit the timeshift stone


# Ancient Cistern
def can_enter_AC_statue(state: CollectionState, player: int) -> bool:
    return state.can_reach_region("Ancient Cistern", player) and (
        state.has("Ancient Cistern Small Key", player, 2)
        or can_lower_AC_statue(state, player)
    )


def can_lower_AC_statue(state: CollectionState, player: int) -> bool:
    return can_reach_AC_vines(state, player) and state.has("Whip", player)


def can_pass_AC_waterfall(state: CollectionState, player: int) -> bool:
    return (
        state.can_reach_region("Ancient Cistern", player)
        and state.has("Water Dragon's Scale", player)
        and state.has("Whip", player)
    )


def can_reach_AC_boko_key_door(state: CollectionState, player: int) -> bool:
    return (
        can_pass_AC_waterfall(state, player)
        and state.has("Whip", player)
        and state.has("Water Dragon's Scale", player)
        and (has_beetle(state, player) or has_bow(state, player))
    )


def can_reach_AC_vines(state: CollectionState, player: int) -> bool:
    return state.can_reach_region("Ancient Cistern", player) and (
        (state.has("Clawshots", player) and state.has("Whip", player))
        or (
            can_reach_AC_boko_key_door(state, player)
            and state.has("Ancient Cistern Small Key", player, 2)
        )
    )


def can_reach_AC_thread(state: CollectionState, player: int) -> bool:
    return can_lower_AC_statue(state, player) and (
        state.has("Clawshots", player) or has_hook_beetle(state, player)
    )


def can_reach_AC_boss_door(state: CollectionState, player: int) -> bool:
    return (  # This means can reach the very TOP of the dungeon after the boss key is put in
        can_enter_AC_statue(state, player)
        and state.has("Whip", player)  # Whip valves
        and state.has("Ancient Cistern Boss Key", player)
    )


def can_beat_koloktos(state: CollectionState, player: int) -> bool:
    return (
        can_reach_AC_boss_door(state, player)
        and state.has("Whip", player)
        and (
            has_practice_sword(state, player)
            or has_bow(state, player)
            or state.has("Bomb Bag", player)
        )
    )


def can_beat_AC(state: CollectionState, player: int) -> bool:
    return can_beat_koloktos(state, player) and has_goddess_sword(state, player)


# Sandship
def can_change_SSH_temporality(state: CollectionState, player: int) -> bool:
    return (
        state.can_reach_region("Sandship", player)
        and has_bow(state, player)
        and (
            has_practice_sword(state, player)
            or state.has("Sandship Small Key", player, 2)
        )
    )


def can_reach_SSH_4_door_corridor(state: CollectionState, player: int) -> bool:
    return state.can_reach_region("Sandship", player) and (
        can_change_SSH_temporality(state, player)
        or has_goddess_sword(state, player)
        or has_bow(state, player)
        or has_slingshot(state, player)
        or state.has("Bomb Bag", player)
    )


def can_reach_SSH_brig(state: CollectionState, player: int) -> bool:
    return (
        can_change_SSH_temporality(state, player)
        and has_practice_sword(state, player)
        and has_bow(state, player)
        and state.has("Whip", player)
    )


def can_reach_SSH_boss_door(state: CollectionState, player: int) -> bool:
    return can_change_SSH_temporality(state, player)


def can_beat_tentalus(state: CollectionState, player: int) -> bool:
    return (
        can_reach_SSH_boss_door(state, player)
        and state.has("Sandship Boss Key", player)
        and has_bow(state, player)
    )


def can_beat_SSH(state: CollectionState, player: int) -> bool:
    return can_beat_tentalus(state, player) and has_goddess_sword(state, player)


# Fire Sanctuary
def can_reach_FS_first_magmanos_room(state: CollectionState, player: int) -> bool:
    return (
        state.can_reach_region("Fire Sanctuary", player)
        and state.has("Fire Sanctuary Small Key", player)
        and (distance_activator(state, player) or state.has("Bomb Bag", player))
    )


def can_reach_FS_water_pod_room(state: CollectionState, player: int) -> bool:
    return (
        can_reach_FS_first_magmanos_room(state, player)
        and can_defeat_lezalfos(state, player)
        and has_hook_beetle(state, player)
        and state.has("Fire Sanctuary Small Key", player, 2)
    )


def can_reach_FS_second_bridge(state: CollectionState, player: int) -> bool:
    return (
        can_reach_FS_water_pod_room(state, player)
        and has_practice_sword(state, player)
        and has_mogma_mitts(state, player)
        and state.has("Gust Bellows", player)
    )


def can_reach_FS_plats_room(state: CollectionState, player: int) -> bool:
    return (
        can_reach_FS_water_pod_room(state, player)
        and has_practice_sword(state, player)
        and has_mogma_mitts(state, player)
        and state.has("Fire Sanctuary Small Key", player, 3)
        and (
            distance_activator(state, player) or state.has("Bomb Bag", player)
        )  # for water pod
    )


def can_reach_FS_boss_door(state: CollectionState, player: int) -> bool:
    return can_reach_FS_plats_room(state, player) and has_mogma_mitts(state, player)


def can_reach_top_of_FS_staircase(state: CollectionState, player: int) -> bool:
    return (
        can_reach_FS_boss_door(state, player)
        and can_defeat_lezalfos(state, player)
        and state.has("Clawshots", player)
    )


def can_beat_ghirahim_2(state: CollectionState, player: int) -> bool:
    return (
        can_reach_FS_boss_door(state, player)
        and state.has("Fire Sanctuary Boss Key", player)
        and has_practice_sword(state, player)
    )


def can_beat_FS(state: CollectionState, player: int) -> bool:
    return can_beat_ghirahim_2(state, player) and has_goddess_sword(state, player)


# Sky Keep
def can_pass_SK_sv_room(state: CollectionState, player: int) -> bool:
    return (
        state.can_reach_region("Sky Keep", player)
        and (has_beetle(state, player) or has_bow(state, player))
        and state.has("Whip", player)
        and state.has("Clawshots", player)
        and (
            state.has("Bomb Bag", player)
            or has_hook_beetle(state, player)
            or has_bow(state, player)
        )
        and state.has("Gust Bellows", player)
    )


def can_pass_SK_lmf_room(state: CollectionState, player: int) -> bool:
    return (
        can_pass_SK_sv_room(state, player)
        and has_bow(state, player)
        and state.has("Gust Bellows", player)
    )


def can_pass_SK_et_room(state: CollectionState, player: int) -> bool:
    return (
        can_pass_SK_lmf_room(state, player)
        and has_mogma_mitts(state, player)
        and has_hook_beetle(state, player)
        and state.has("Bomb Bag", player)
        and upgraded_skyward_strike(state, player)
    )


def can_pass_SK_mini_boss_room(state: CollectionState, player: int) -> bool:
    return (
        (can_pass_SK_et_room(state, player) or can_pass_SK_fs_room(state, player))
        and has_practice_sword(state, player)
        and state.has("Clawshots", player)
    )


def can_pass_SK_ac_room(state: CollectionState, player: int) -> bool:
    return can_pass_SK_lmf_room(state, player)


def can_get_triforce_of_courage(state: CollectionState, player: int) -> bool:
    return (
        can_pass_SK_ac_room(state, player)
        and state.has("Sky Keep Small Key", player)
        and can_defeat_moblins(state, player)
        and can_defeat_bokoblins(state, player)
        and can_defeat_stalfos(state, player)
        and has_bow(state, player)
        and can_defeat_cursed_bokoblins(state, player)
        and can_defeat_stalmaster(state, player)
    )


def can_pass_SK_fs_room(state: CollectionState, player: int) -> bool:
    return (
        can_pass_SK_ac_room(state, player)
        and has_beetle(state, player)
        and state.has("Clawshots", player)
    )


def can_get_triforce_of_power(state: CollectionState, player: int) -> bool:
    return can_pass_SK_fs_room(state, player)


def can_pass_SK_ssh_room(state: CollectionState, player: int) -> bool:
    return (
        can_pass_SK_fs_room(state, player)
        and has_bow(state, player)
        and state.has("Clawshots", player)
    )


def can_get_triforce_of_wisdom(state: CollectionState, player: int) -> bool:
    return can_pass_SK_ssh_room(state, player)


def can_beat_SK(state: CollectionState, player: int) -> bool:
    return (
        state.can_reach_region("Sky Keep", player)
        and can_get_triforce_of_courage(state, player)
        and can_get_triforce_of_power(state, player)
        and can_get_triforce_of_wisdom(state, player)
    )


# Silent Realms
def can_access_skyloft_silent_realm(state: CollectionState, player: int) -> bool:
    return state.can_reach_region("Skyloft Silent Realm", player)


def can_access_faron_silent_realm(state: CollectionState, player: int) -> bool:
    return state.can_reach_region("Faron Silent Realm", player)


def can_access_eldin_silent_realm(state: CollectionState, player: int) -> bool:
    return state.can_reach_region("Eldin Silent Realm", player)


def can_access_lanayru_silent_realm(state: CollectionState, player: int) -> bool:
    return state.can_reach_region("Lanayru Silent Realm", player)
