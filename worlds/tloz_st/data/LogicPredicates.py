from BaseClasses import CollectionState
from Options import Accessibility
from .Constants import *


# =========== Item States ============= TODO another big change

def st_has_stamp_book(state, player):
    return state.has("Stamp Book", player)

def st_has_sword(state: CollectionState, player: int):
    return state.has("Sword (Progressive)", player)


def st_has_stantom_sword(state: CollectionState, player: int):
    return state.has("Sword (Progressive)", player, 2)


def st_has_shield(state: CollectionState, player: int):
    # Shield can be bought from shop
    return True


def st_has_shovel(state: CollectionState, player: int):
    return state.has("Shovel", player)


def st_has_bow(state: CollectionState, player: int):
    return state.has("Bow (Progressive)", player)


def st_has_bombs(state: CollectionState, player: int):
    return state.has("Bombs (Progressive)", player)


def st_has_chus(state: CollectionState, player: int):
    return state.has("Bombchus (Progressive)", player)


def st_has_grapple(state: CollectionState, player: int):
    return state.has("Grappling Hook", player)


def st_has_hammer(state: CollectionState, player: int):
    return state.has("Hammer", player)


def st_has_boomerang(state: CollectionState, player: int):
    return state.has("Boomerang", player)


def st_has_spirit(state: CollectionState, player: int, spirit: str, count: int = 1):
    return state.has(f"Spirit of {spirit} (Progressive)", player, count)


def st_has_spirit_gems(state: CollectionState, player: int, spirit: str, count: int = 1):
    return all([state.has(f"{spirit} Gem", player, count),
                st_has_spirit(state, player, spirit)])


def st_has_sun_key(state: CollectionState, player: int):
    return state.has("Sun Key", player)


def st_has_ghost_key(state: CollectionState, player: int):
    return state.has("Ghost Key", player)


def st_has_kings_key(state: CollectionState, player: int):
    return state.has("King's Key", player)


def st_has_regal_necklace(state: CollectionState, player: int):
    return state.has("Regal Necklace", player)


def st_has_stantom_blade(state: CollectionState, player: int):
    return state.has("Phantom Blade", player)


def st_has_heros_new_clothes(state: CollectionState, player: int):
    return state.has("Hero's New Clothes", player)


def st_has_guard_notebook(state: CollectionState, player: int):
    return state.has("Guard Notebook", player)


def st_has_kaleidoscope(state: CollectionState, player: int):
    return state.has("Kaleidoscope", player)


def st_has_wood_heart(state: CollectionState, player: int):
    return state.has("Wood Heart", player)


def st_has_triforce_crest(state: CollectionState, player: int):
    return any([state.has("Triforce Crest", player),
                not st_option_triforce_crest(state, player)])


# ========= Sea Items =============

def st_has_sea_chart(state: CollectionState, player: int, quadrant: str):
    return state.has(f"{quadrant} Sea Chart", player)


def st_has_courage_crest(state: CollectionState, player: int):
    return state.has("Courage Crest", player)


def st_has_cannon(state: CollectionState, player: int):
    return state.has("Cannon", player)


def st_has_salvage(state: CollectionState, player: int):
    return state.has("Salvage Arm", player)


# ============== Frogs =======================

def st_has_cyclone_slate(state: CollectionState, player: int):
    return state.has("Cyclone Slate", player)


# Does not mean you can logically get back, use the other frogs
def st_has_frog(state: CollectionState, player: int, glyst: str, quadrant: str):
    return all([
        st_has_sea_chart(state, player, quadrant),
        st_has_cyclone_slate(state, player),
        any([
            state.has(f"Frog Glyst {glyst}", player),
            st_option_start_with_frogs(state, player)
        ])
    ])


def st_has_frog_x(state: CollectionState, player: int):
    return st_has_frog(state, player, "X", "SW")


def st_has_frog_sti(state: CollectionState, player: int):
    return all([
        st_has_frog(state, player, "Phi", "SW"),
        any([
            st_has_cannon(state, player),
            st_has_frog_x(state, player),
            st_has_sea_chart(state, player, "NW")
        ])
    ])


def st_has_frog_n(state: CollectionState, player: int):
    return st_has_frog(state, player, "N", "NW")


def st_has_frog_omega(state: CollectionState, player: int):
    return st_has_frog(state, player, "Omega", "SE")


def st_has_frog_w(state: CollectionState, player: int):
    return st_has_frog(state, player, "W", "SE")


def st_has_frog_square(state: CollectionState, player: int):
    return all([
        st_has_frog(state, player, "Square", "NE"),
        any([
            st_has_sea_chart(state, player, "SE"),
            st_has_frog_sti(state, player),
            st_has_frog_n(state, player),
            st_has_frog_x(state, player)
        ])
    ])


# =========== Combined item states ================

def st_has_explosives(state: CollectionState, player: int):
    return state.has_any(["Bombs (Progressive)", "Bombchus (Progressive)"], player)


def st_has_damage(state: CollectionState, player: int):
    return any([
        state.has("Sword (Progressive)", player),
        st_has_explosives(state, player),
        state.has("Bow (Progressive)", player),
        state.has("Grappling Hook", player),
        state.has("Hammer", player)
    ])


def st_has_cave_damage(state: CollectionState, player: int):
    return any([
        state.has("Sword (Progressive)", player),
        st_has_bombs(state, player),
        state.has("Bow (Progressive)", player),
        state.has("Grappling Hook", player),
        state.has("Hammer", player)
    ])


def st_can_kill_bat(state: CollectionState, player: int):
    return any([
        st_has_damage(state, player),
        st_has_boomerang(state, player)
    ])


def st_can_kill_blue_chu(state: CollectionState, player: int):
    return any([
        st_has_bombs(state, player),  # Only place this is relevant is in "cave"
        st_has_bow(state, player),
        st_has_grapple(state, player),
        st_has_hammer(state, player),
        st_has_beam_sword(state, player),
        all([
            st_has_sword(state, player),
            any([
                st_has_boomerang(state, player),
                st_has_super_shield(state, player),
            ])
        ])
    ])


def st_can_kill_eye_brute(state: CollectionState, player: int):
    return any([
        st_option_hard_logic(state, player),
        st_has_hammer(state, player),
        st_has_bow(state, player),
        st_has_chus(state, player)
    ])


def st_can_kill_bubble(state: CollectionState, player: int):
    return any([
        st_has_hammer(state, player),
        st_has_explosives(state, player),
        st_has_bow(state, player),
        st_has_grapple(state, player),
        st_has_fire_sword(state, player),
        all([
            st_has_sword(state, player), any([
                st_has_boomerang(state, player),
                st_has_super_shield(state, player)  # This is the one logical use for shield!!!
            ])
        ])
    ])


def st_totok_stantom_steal_object(state, player):
    return any([
        st_clever_pots(state, player),
        st_can_kill_bat(state, player)
    ])


def st_has_range(state: CollectionState, player: int):
    return state.has_any(["Boomerang", "Bow (Progressive)", "Grappling Hook"], player)


def st_has_short_range(state: CollectionState, player: int):
    return any([st_has_mid_range(state, player),
                st_clever_bombs(state, player), ])


def st_has_mid_range(state: CollectionState, player: int):
    return any([st_has_range(state, player),
                st_has_hammer(state, player),
                st_has_beam_sword(state, player)])


def st_has_fire_sword(state: CollectionState, player: int):
    return all([
        st_has_sword(state, player),
        st_has_spirit(state, player, "Power", 2)
    ])


def st_has_super_shield(state: CollectionState, player: int):
    return all([
        st_has_shield(state, player),
        st_has_spirit(state, player, "Wisdom", 2)
    ])


def st_has_beam_sword(state: CollectionState, player: int):
    return all([
        st_has_sword(state, player),
        st_has_spirit(state, player, "Courage", 2)
    ])


def st_can_hit_spin_switches(state: CollectionState, player: int):
    return any([
        st_has_sword(state, player),
        all([
            st_option_hard_logic(state, player),
            any([
                st_has_explosives(state, player),
                st_has_boomerang(state, player)
            ])
        ])
    ])


def st_spiral_wall_switches(state: CollectionState, player: int):
    return any([
        st_has_boomerang(state, player),
        st_has_hammer(state, player),
        st_has_explosives(state, player)
    ])


def st_quick_switches(state, player):
    return any([
        st_has_boomerang(state, player),
        all([
            st_has_bow(state, player),
            st_option_hard_logic(state, player)
        ])
    ])


def st_can_cut_small_trees(state: CollectionState, player: int):
    return any([st_has_sword(state, player), st_has_explosives(state, player)])


# ================ Rupee States ==================


def st_has_rupees(state: CollectionState, player: int, cost: int):
    # If has a farmable minigame and the means to sell, expensive things are in logic.
    if st_can_farm_rupees(state, player):
        return True

    # Count up regular rupee items
    rupees = state.count("Green Rupee (1)", player)
    rupees += state.count("Blue Rupee (5)", player) * 5
    rupees += state.count("Red Rupee (20)", player) * 20
    rupees += state.count("Big Green Rupee (100)", player) * 100
    rupees += state.count("Big Red Rupee (200)", player) * 200
    rupees += state.count("Gold Rupee (300)", player) * 300

    # Sell Treasure for safe average 150 (can be 50, 150, 800 or 1500)
    if st_has_courage_crest(state, player):
        rupees += state.count_group("Treasure Items", player) * 150

    return rupees >= cost


def st_can_farm_rupees(state: CollectionState, player: int):
    return any([
        all([
            st_has_courage_crest(state, player),  # Can Sell Treasure
            any([
                all([  # Can Farm Phantoms in TotOK
                    st_has_stantom_sword(state, player),
                    st_has_spirit(state, player, "Power")
                ]),
                state.has("_beat_toc", player),
                state.has("_can_play_cannon_game", player),
                state.has("_can_play_goron_race", player),
            ])
        ]),
        all([  # Can farm harrow (and chooses to play with harrow)
            state.has("_can_play_harrow", player),
            st_option_randomize_harrow(state, player)
        ])
    ])


def st_island_shop(state, player, price):
    other_costs = 0
    if st_has_sea_chart(state, player, "SW"):
        # Includes cannon island, but not salvage arm cause that also unlocks treasure shop
        other_costs += 1550  # TODO this might break generation
    return st_has_rupees(state, player, price + other_costs)


def st_beedle_shop(state, player, price):
    other_costs = 550
    if st_has_bow(state, player):
        other_costs += 1000
        if st_has_chus(state, player):
            other_costs += 3000
    if st_has_bombs(state, player):
        other_costs += 1000
    if st_option_randomize_masked_beedle(state, player):
        other_costs += 1500
    return st_has_rupees(state, player, price + other_costs)


def st_can_buy_gem(state: CollectionState, player: int):
    return all([st_has_bow(state, player), st_island_shop(state, player, 500)])


def st_can_buy_quiver(state: CollectionState, player: int):
    return all([st_has_bow(state, player), st_island_shop(state, player, 1500)])


def st_can_buy_chu_bag(state: CollectionState, player: int):
    return all([st_has_chus(state, player), st_has_bow(state, player), st_island_shop(state, player, 2500)])


def st_can_buy_heart(state: CollectionState, player: int):
    return all([st_has_chus(state, player), st_has_bow(state, player), st_island_shop(state, player, 4500)])


# ============ Option states =============

def st_option_glitched_logic(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.logic == "glitched"


def st_option_normal_logic(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.logic == "normal"


def st_option_hard_logic(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.logic in ["hard", "glitched"]


def st_option_not_glitched_logic(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.logic in ["hard", "normal"]


def st_option_keysanity(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.keysanity == "anywhere"


def st_option_keys_vanilla(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.keysanity == "vanilla"


def st_option_keys_in_own_dungeon(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.keysanity in ["in_own_dungeon", "vanilla"]


def st_option_stantoms_hard(state: CollectionState, player: int):
    return all([state.multiworld.worlds[player].options.stantom_combat_difficulty in ["require_weapon"],
                st_has_grapple(state, player)])


def st_option_stantoms_med(state: CollectionState, player: int):
    return all([state.multiworld.worlds[player].options.stantom_combat_difficulty in ["require_weapon", "require_stun"],
                any([
                    st_has_bow(state, player),
                    st_has_hammer(state, player),
                    st_has_fire_sword(state, player)
                ])])


def st_option_stantoms_easy(state: CollectionState, player: int):
    return (state.multiworld.worlds[player].options.stantom_combat_difficulty in
            ["require_weapon", "require_stun", "require_traps"])


def st_option_stantoms_sword_only(state: CollectionState, player: int):
    return all([state.multiworld.worlds[player].options.stantom_combat_difficulty in
                ["require_weapon", "require_stun", "require_traps", "require_stantom_sword"],
                st_has_stantom_sword(state, player)])


def st_clever_pots(state: CollectionState, player: int):
    return st_option_hard_logic(state, player)


def st_can_hit_switches(state: CollectionState, player: int):
    return any([st_option_hard_logic(state, player), st_can_kill_bat(state, player)])


def st_clever_bombs(state: CollectionState, player: int):
    return all([st_has_bombs(state, player),
                st_option_hard_logic(state, player)])


def st_option_randomize_frogs(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.randomize_frogs == "randomize"


def st_option_start_with_frogs(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.randomize_frogs == "start_with"


def st_option_triforce_crest(state, player):
    return state.multiworld.worlds[player].options.randomize_triforce_crest


def st_beat_required_dungeons(state: CollectionState, player: int):
    # print(f"Dungeons required: {state.count_group('Current Metals', player)}/{state.multiworld.worlds[player].options.dungeons_required} {state.has_group("Current Metals", player,
    #                       state.multiworld.worlds[player].options.dungeons_required)}")
    return state.has_group("Current Metals", player,
                           state.multiworld.worlds[player].options.dungeons_required)


def st_option_randomize_masked_beedle(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.randomize_masked_beedle


def st_goal_option_stantom_door(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.bellum_access == "spawn_stantoms_on_b13"


def st_goal_option_staircase(state: CollectionState, player: int):
    return (state.multiworld.worlds[player].options.bellum_access in
            ["spawn_stantoms_on_b13", "spawn_stantoms_on_b13", "warp_to_bellum"])


def st_goal_option_warp(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.bellum_access == "warp_to_bellum"


def st_goal_option_spawn_bellumbeck(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.bellum_access == "spawn_bellumbeck"


def st_option_boat_requires_sea_chart(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.boat_requires_sea_chart


def st_option_fog_vanilla(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.fog_settings in ["vanilla_fog", "no_fog"]


def st_option_fog_open(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.fog_settings == "open_ghost_ship"


def st_option_randomize_harrow(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.randomize_harrow


def st_option_goal_bellum(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.goal == "beat_bellumbeck"


def st_option_goal_midway(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.goal == "triforce_door"


# For doing sneaky stuff with universal tracker UT
def st_is_ut(state: CollectionState, player: int):
    return getattr(state.multiworld, "generation_is_fake", False)


# ============= Key logic ==============

def st_has_small_keys(state: CollectionState, player: int, dung_name: str, amount: int = 1):
    return state.has(f"Small Key ({dung_name})", player, amount)


def st_has_boss_key(state: CollectionState, player: int, dung_name: str):
    return state.has(f"Boss Key ({dung_name})", player)


def st_has_boss_key_simple(state: CollectionState, player: int, dung_name: str):
    return any([
        st_has_boss_key(state, player, dung_name),
        st_is_ut(state, player)
    ])


def st_has_force_gems(state, player, floor=3, count=3):
    return state.has(f"Force Gem (B{floor})", player, count)


def st_has_shape_crystal(state: CollectionState, player: int, dung_name: str, shape: str):
    return state.has(f"{shape} Crystal ({dung_name})", player)


def st_ut_small_key_vanilla_location(state, player):
    return all([
        st_is_ut(state, player),
        st_option_keys_vanilla(state, player)
    ])


def st_ut_small_key_own_dungeon(state, player):
    return all([
        st_is_ut(state, player),
        st_option_keys_in_own_dungeon(state, player)
    ])


# ======== Harder Logic ===========

def st_can_kill_stantoms(state: CollectionState, player: int):
    return any([
        st_option_stantoms_hard(state, player),
        st_option_stantoms_med(state, player),
        st_option_stantoms_sword_only(state, player)
    ])


def st_can_kill_stantoms_traps(state: CollectionState, player: int):
    return any([
        st_option_stantoms_hard(state, player),
        st_option_stantoms_med(state, player),
        st_option_stantoms_easy(state, player),
        st_option_stantoms_sword_only(state, player)
    ])


def st_can_hit_tricky_switches(state: CollectionState, player: int):
    return any([
        st_clever_pots(state, player),
        st_has_short_range(state, player)
    ])


def st_can_hammer_clip(state: CollectionState, player: int):
    return all([st_has_hammer(state, player), st_option_glitched_logic(state, player)])


def st_can_hit_bombchu_switches(state: CollectionState, player: int):
    return any([
        st_can_hammer_clip(state, player),
        st_has_chus(state, player)
    ])


def st_can_boomerang_return(state: CollectionState, player: int):
    return all([
        st_has_boomerang(state, player),
        st_option_glitched_logic(state, player)
    ])


def st_can_arrow_despawn(state: CollectionState, player: int):
    return all([
        st_has_bow(state, player),
        st_option_glitched_logic(state, player)
    ])

def st_can_bcl(state, player):
    # Bombchu Camera Lock
    return all([
        st_has_chus(state, player),
        st_option_glitched_logic(state, player)
    ])

def st_can_sword_glitch(state, player):
    return all([
        st_has_sword(state, player),
        st_option_glitched_logic(state, player)
    ])

def st_can_sword_scroll_clip(state, player):
    return all([
        st_has_sword(state, player),
        state.has("Swordsman's Scroll", player),
        st_option_glitched_logic(state, player)
    ])


# ====== Specific locations =============

# TotOK
def st_totok_b1_all_checks_ut(state, player):
    return all([
        st_ut_small_key_own_dungeon(state, player),
        st_has_spirit(state, player, "Power"),
        st_has_bow(state, player),
        st_has_grapple(state, player),
        st_can_kill_stantoms(state, player),
    ])


def st_totok_b2_key(state: CollectionState, player: int):
    return any([st_can_boomerang_return(state, player),
                all([st_can_hit_switches(state, player),
                     any([st_option_hard_logic(state, player),
                          st_has_explosives(state, player),
                          st_can_hit_tricky_switches(state, player)
                          ])
                     ])
                ])


def st_totok_b2_all_checks_ut(state, player):
    return all([
        st_totok_b1_all_checks_ut(state, player),
        st_has_stantom_sword(state, player)
    ])


def st_totok_b4_all_checks_ut(state, player):
    return all([
        st_totok_b2_all_checks_ut(state, player),
        st_has_spirit(state, player, "Wisdom"),
        any([
            st_has_explosives(state, player),
            st_can_hammer_clip(state, player),
            st_can_boomerang_return(state, player)
        ])
    ])


def st_totok_b4_access(state, player):
    return any([
        st_has_grapple(state, player),
        st_has_force_gems(state, player),
        all([
            st_is_ut(state, player),
            st_has_small_keys(state, player, "Temple of the Ocean King", 4)
        ])
    ])


def st_totok_b5(state: CollectionState, player: int):
    return all([
        st_can_kill_bubble(state, player),
        any([
            st_has_mid_range(state, player),
            st_clever_bombs(state, player)])
    ])


def st_totok_b5_key_logic(state: CollectionState, player: int):
    # TODO: Does not take into account force gem shuffling
    return any([
        # Grapple Shortcut
        all([
            st_has_small_keys(state, player, "Temple of the Ocean King", 4),
            st_has_grapple(state, player)
        ]),
        # Force Gems
        st_has_small_keys(state, player, "Temple of the Ocean King", 5),
        # UT
        st_totok_b4_all_checks_ut(state, player)
    ])


def st_has_totok_crystal(state: CollectionState, player: int, shape: str):
    return state.has(f"{shape} Crystal (Temple of the Ocean King)", player)


def st_totok_b8_2_crystals(state, player):
    return any([
        all([
            st_has_explosives(state, player),
            st_has_totok_crystal(state, player, "Round"),
            st_has_totok_crystal(state, player, "Triangle")
        ]),
        st_totok_b8_crystals_ut(state, player)
    ])


def st_totok_b8_crystals_ut(state, player):
    return all([
        st_is_ut(state, player),
        st_can_hit_switches(state, player),  # Covers Round Crystal, and also triangle,
        st_has_explosives(state, player)  # For placing triangle switch
    ])


def st_totok_b9(state, player):
    return any([
        st_can_hit_bombchu_switches(state, player),
        all([
            st_has_explosives(state, player),
            any([
                st_has_totok_crystal(state, player, "Triangle"),
                st_totok_b8_crystals_ut(state, player)
            ])])
    ])


def st_totok_b9_crystals_ut(state, player):
    return all([
        st_is_ut(state, player),
        st_can_hit_switches(state, player),  # Covers Round Crystal, and also triangle,
        st_totok_b9_stantom_square(state, player)  # For placing triangle switch
    ])


def st_totok_b9_stantom_square(state, player):
    return any([
        st_totok_b9_stantom_kill(state, player),
        st_totok_stantom_steal_object(state, player),
    ])


def st_totok_b9_stantom_kill(state, player):
    return any([
        st_has_stantom_sword(state, player),
        all([
            st_can_kill_stantoms_traps(state, player),
            any([
                st_has_hammer(state, player),
                all([
                    st_has_bow(state, player),
                    st_has_boomerang(state, player)])
            ])])
    ])


def st_totok_b95(state, player):
    return any([
        all([
            st_has_totok_crystal(state, player, "Round"),
            st_has_totok_crystal(state, player, "Triangle"),
            st_totok_b9_stantom_square(state, player)
        ]),
        st_totok_b9_crystals_ut(state, player)
    ])


def st_totok_b10_all_checks_ut(state, player):
    return all([
        st_totok_b4_all_checks_ut(state, player),
        st_has_triforce_crest(state, player),
        st_has_sea_chart(state, player, "SW"),
        st_has_hammer(state, player),
        st_has_explosives(state, player),
        st_has_shovel(state, player)
    ])


def st_totok_b10_key_logic(state: CollectionState, player: int):
    # TODO: Does not take into account force gem shuffling
    return any([
        all([
            st_has_small_keys(state, player, "Temple of the Ocean King", 5),
            st_has_grapple(state, player)
        ]),
        st_has_small_keys(state, player, "Temple of the Ocean King", 6),
        # UT
        st_totok_b10_all_checks_ut(state, player)
    ])


def st_totok_b12(state: CollectionState, player: int):
    return any([
        st_has_hammer(state, player),
        all([
            st_has_shovel(state, player),
            any([
                st_clever_pots(state, player),
                st_has_mid_range(state, player),
                st_has_explosives(state, player)
            ])
        ])
    ])


def st_totok_b12_force_gems(state, player):
    return any([
        all([
            st_has_force_gems(state, player, 12, 2),
            st_totok_stantom_steal_object(state, player)  # Redundant since bombs are needed to get here
        ]),
        st_is_ut(state, player)
    ])


def st_totok_b13_door(state: CollectionState, player: int):
    # Required to enter the stantom door
    return all([
        st_has_stantom_sword(state, player),
        any([
            all([st_goal_option_stantom_door(state, player),
                 st_beat_required_dungeons(state, player)]),
            st_goal_option_staircase(state, player)
        ])
    ])


# Overworld

def st_boat_access(state, player):
    return any([
        not st_option_boat_requires_sea_chart(state, player),
        st_has_sea_chart(state, player, "SW")
    ])


# Handles keylocking due to lack of locations
def st_can_reach_MP2(state: CollectionState, player: int):
    return any([
        all([
            st_option_keysanity(state, player),
            st_has_small_keys(state, player, "Mountain Passage", 2)
        ]),
        all([
            st_option_keys_in_own_dungeon(state, player),
            any([
                st_can_cut_small_trees(state, player),
                st_option_glitched_logic(state, player)  # SW in back entrance / reversse cuccoo jump
            ]),
            any([
                st_has_small_keys(state, player, "Mountain Passage"),
                st_is_ut(state, player)
            ])
        ])
    ])


def st_mercay_passage_rat(state, player):
    return any([
        st_can_kill_bat(state, player),
        st_clever_pots(state, player)
    ])


def st_bannan_scroll(state, player):
    return all([
        st_has_wood_heart(state, player),
        st_has_cannon(state, player),
        st_has_sea_chart(state, player, "SE"),
    ])


def st_salvage_courage_crest(state: CollectionState, player: int):
    return all([
        st_has_courage_crest(state, player),
        st_has_salvage(state, player),
        # The sea monster is disabled, otherwise add cannon to reqs
    ])


def st_can_enter_ocean_sw_west(state, player):
    return any([
        st_has_cannon(state, player),
        st_has_frog_sti(state, player),  # Includes return data, and NW way back
    ])


# Tof

def st_tof_1f_key_ut(state, player):
    return all([
        st_ut_small_key_own_dungeon(state, player),
        st_can_kill_bat(state, player)
    ])

def st_tof_3f(state, player):
    return all([
        any([
            st_has_small_keys(state, player, "Temple of Fire", 2),
            st_ut_small_key_own_dungeon(state, player)]),
        any([
            st_has_boomerang(state, player),
            st_has_hammer(state, player),
            st_clever_bombs(state, player)
        ])
    ])


# Wind

def st_wind_temple_key_ut(state, player):
    return all([
        st_has_shovel(state, player),
        any([
            all([
                st_has_bombs(state, player),
                st_ut_small_key_own_dungeon(state, player)]),
            st_ut_small_key_own_dungeon(state, player)
        ])
    ])


# Toc

def st_can_enter_toc(state, player):
    return all([
        st_has_damage(state, player),
        any([
            st_has_boomerang(state, player),
            st_has_bow(state, player)
        ])
    ])


def st_toc_key_door_1(state, player):
    return any([
        st_toc_key_doors(state, player, 3, 1),
        # UT Keys
        all([
            st_option_not_glitched_logic(state, player),
            st_ut_small_key_own_dungeon(state, player),
            any([
                st_has_explosives(state, player),
                st_option_keys_vanilla(state, player)
            ])
        ]),
    ])


def st_toc_key_door_2(state, player):
    return any([
        st_toc_key_doors(state, player, 3, 2),
        # UT stuff
        all([
            st_option_not_glitched_logic(state, player),
            any([
                # Keys in own dungeon
                all([
                    st_ut_small_key_own_dungeon(state, player),
                    st_has_explosives(state, player),
                    st_has_grapple(state, player),
                    st_has_bow(state, player)
                ]),
                # Keys vanilla
                all([
                    st_ut_small_key_vanilla_location(state, player),
                    any([
                        st_has_explosives(state, player),
                        all([
                            st_has_bow(state, player),
                            st_has_grapple(state, player)
                        ])
                    ])
                ])
            ])
        ])
    ])


def st_toc_key_door_3(state, player):
    return any([
        st_has_small_keys(state, player, "Temple of Courage", 3),
        # UT
        all([
            st_ut_small_key_own_dungeon(state, player),
            st_has_bow(state, player),
            st_has_explosives(state, player)
        ]),
        all([
            st_ut_small_key_vanilla_location(state, player),
            any([
                st_can_hammer_clip(state, player),
                all([
                    st_has_bow(state, player),
                    any([
                        st_has_grapple(state, player),
                        st_has_explosives(state, player),
                    ])
                ])
            ])
        ])
    ])


def st_toc_key_doors(state, player, glitched: int, not_glitched: int):
    return any([
        all([
            st_option_glitched_logic(state, player),
            st_has_small_keys(state, player, "Temple of Courage", glitched)
        ]),
        all([
            st_option_not_glitched_logic(state, player),
            st_has_small_keys(state, player, "Temple of Courage", not_glitched)
        ])
    ])


def st_toc_final_switch_state(state, player):
    return any([
        st_has_bow(state, player),
        st_toc_key_doors(state, player, 2, 1)
    ])


# Ghost Ship

def st_has_ghost_ship_access(state, player):
    return any([
        all([
            st_has_spirit(state, player, "Power"),
            st_has_spirit(state, player, "Wisdom"),
            st_has_spirit(state, player, "Courage"),
            st_option_fog_vanilla(state, player)
        ]),
        st_option_fog_open(state, player)
    ])


def st_ghost_ship_barrel(state, player):
    return any([
        st_has_bombs(state, player),
        st_has_hammer(state, player),
        st_has_boomerang(state, player),
        st_has_grapple(state, player)
    ])


def st_beat_ghost_ship(state: CollectionState, player):
    return state.has("_beat_ghost_ship", player)


# Goron

def st_goron_chus(state, player):
    return all([
        st_has_shovel(state, player),
        any([
            st_has_hammer(state, player),
            st_has_bow(state, player),
            st_has_grapple(state, player),
        ])
    ])


# Toi

def st_toi_3f_boomerang(state, player):
    return st_quick_switches(state, player)


def st_toi_b2(state, player):
    return all([
        st_has_bow(state, player),
        st_quick_switches(state, player),
        any([
            st_toi_key_doors(state, player, 3, 2),
            st_can_hammer_clip(state, player),
            st_can_bcl(state, player)
        ])
    ])


def st_toi_key_door_1_ut(state, player):
    return any([
        st_toi_all_key_doors_ut(state, player),
        all([
            st_option_not_glitched_logic(state, player),
            any([
                st_ut_small_key_vanilla_location(state, player),
                all([
                    st_ut_small_key_own_dungeon(state, player),
                    st_has_explosives(state, player)
                ])
            ]),
        ])
    ])


def st_toi_all_key_doors_ut(state, player):
    return all([
        st_ut_small_key_own_dungeon(state, player),
        st_has_grapple(state, player),
        st_has_explosives(state, player),
        st_has_bow(state, player),
        st_quick_switches(state, player)
    ])


def st_toi_key_doors(state, player, glitched: int, not_glitched: int = None):
    not_glitched = glitched if not_glitched is None else not_glitched
    return any([
        all([
            st_option_glitched_logic(state, player),
            st_has_small_keys(state, player, "Temple of Ice", glitched)
        ]),
        all([
            st_option_not_glitched_logic(state, player),
            st_has_small_keys(state, player, "Temple of Ice", not_glitched)
        ])
    ])


def st_toi_key_door_2(state, player):
    return any([
        st_toi_key_doors(state, player, 3, 2),
        # UT
        st_toi_all_key_doors_ut(state, player),
        all([
            st_option_not_glitched_logic(state, player),
            st_ut_small_key_own_dungeon(state, player),
            st_quick_switches(state, player)
        ])
    ])


def st_toi_key_door_3(state, player):
    return any([
        st_toi_key_doors(state, player, 3),
        # UT
        st_toi_all_key_doors_ut(state, player),
    ])


# Mutoh's

def st_mutoh_water(state, player):
    return any([
        all([
            any([
                st_mutoh_key_doors(state, player, 2, 1),
                st_ut_small_key_own_dungeon(state, player)  # This should account for all chests
            ]),
            st_has_bow(state, player),
        ]),
        st_can_arrow_despawn(state, player)
    ])


def st_mutoh_key_doors(state, player, glitched: int, not_glitched: int):
    return any([
        all([
            st_option_glitched_logic(state, player),
            st_has_small_keys(state, player, "Mutoh's Temple", glitched)
        ]),
        all([
            st_option_not_glitched_logic(state, player),
            st_has_small_keys(state, player, "Mutoh's Temple", not_glitched)
        ])
    ])


# Goal Stuff

def st_totok_blue_warp(state: CollectionState, player: int):
    return all([
        st_goal_option_warp(state, player),
        st_beat_required_dungeons(state, player)
    ])


def st_totok_bellum_staircase(state, player):
    return st_beat_required_dungeons(state, player)


def st_can_beat_bellum(state, player):
    return all([
        st_has_grapple(state, player),
        st_has_stantom_sword(state, player),
        st_has_bow(state, player),
        st_has_spirit(state, player, "Courage")
    ])


def st_can_beat_ghost_ship_fight(state, player):
    return st_has_cannon(state, player)


def st_can_beat_bellumbeck(state, player):
    return all([
        st_has_stantom_sword(state, player),
        st_has_spirit(state, player, "Courage")
    ])


def st_bellumbeck_quick_finish(state, player):
    return all([
        st_can_beat_bellumbeck(state, player),
        st_beat_required_dungeons(state, player),
        st_goal_option_spawn_bellumbeck(state, player)
    ])


def st_temp_goal(state, player):
    return all([st_has_sea_chart(state, player, "SW"),
                st_has_stantom_sword(state, player),
                st_has_courage_crest(state, player)])
