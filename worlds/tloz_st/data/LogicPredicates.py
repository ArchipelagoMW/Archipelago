from BaseClasses import CollectionState
from Options import Accessibility
from .Constants import *


# =========== Item States ============= TODO another big change

def st_has_stamp_book(state, player):
    return state.has("Stamp Book", player)

def st_has_sword(state: CollectionState, player: int):
    return state.has("Sword (Progressive)", player)

def st_has_shield(state: CollectionState, player: int):
    # Shield can be bought from shop
    return True

def st_has_bow(state: CollectionState, player: int):
    return state.has("Bow (Progressive)", player)

def st_has_bombs(state: CollectionState, player: int):
    return state.has("Bombs (Progressive)", player)


def st_has_whip(state: CollectionState, player: int):
    return state.has("Whip", player)

def st_has_boomerang(state: CollectionState, player: int):
    return state.has("Boomerang", player)

def st_has_sword_beam_scroll(state: CollectionState, player: int):
    return state.has("Sword Beam Swordsman's Scroll", player)

# def st_has_spirit_gems(state: CollectionState, player: int, spirit: str, count: int = 1):
#     return all([state.has(f"{spirit} Gem", player, count),
#                 st_has_spirit(state, player, spirit)])


def st_has_regal_necklace(state: CollectionState, player: int):
    return state.has("Regal Necklace", player)


def st_has_stantom_blade(state: CollectionState, player: int):
    return state.has("Phantom Blade", player)


def st_has_wood_heart(state: CollectionState, player: int):
    return state.has("Wood Heart", player)


# ========= Rail Items =============

def st_has_glyph(state: CollectionState, player: int, realm: str):
    return state.has(f"{realm} Glyph", player)


def st_has_cannon(state: CollectionState, player: int):
    return state.has("Cannon", player)


# ============== Frogs =======================

# Does not mean you can logically get back, use the other frogs
# def st_has_frog(state: CollectionState, player: int, glyst: str, quadrant: str):
#     return all([
#         st_has_sea_chart(state, player, quadrant),
#         st_has_cyclone_slate(state, player),
#         any([
#             state.has(f"Frog Glyst {glyst}", player),
#             st_option_start_with_frogs(state, player)
#         ])
#     ])
#
#
# def st_has_frog_x(state: CollectionState, player: int):
#     return st_has_frog(state, player, "X", "SW")
#
#
# def st_has_frog_sti(state: CollectionState, player: int):
#     return all([
#         st_has_frog(state, player, "Phi", "SW"),
#         any([
#             st_has_cannon(state, player),
#             st_has_frog_x(state, player),
#             st_has_sea_chart(state, player, "NW")
#         ])
#     ])
#
#
# def st_has_frog_n(state: CollectionState, player: int):
#     return st_has_frog(state, player, "N", "NW")
#
#
# def st_has_frog_omega(state: CollectionState, player: int):
#     return st_has_frog(state, player, "Omega", "SE")
#
#
# def st_has_frog_w(state: CollectionState, player: int):
#     return st_has_frog(state, player, "W", "SE")
#
#
# def st_has_frog_square(state: CollectionState, player: int):
#     return all([
#         st_has_frog(state, player, "Square", "NE"),
#         any([
#             st_has_sea_chart(state, player, "SE"),
#             st_has_frog_sti(state, player),
#             st_has_frog_n(state, player),
#             st_has_frog_x(state, player)
#         ])
#     ])


# =========== Combined item states ================

def st_has_bomb(state: CollectionState, player: int):
    return state.has_any(["Bombs (Progressive)"], player)


def st_has_damage(state: CollectionState, player: int):
    return any([
        state.has("Sword (Progressive)", player),
        st_has_bombs(state, player),
        state.has("Bow (Progressive)", player),
        state.has("Whip", player),
        state.has("Hammer", player)
    ])


def st_has_cave_damage(state: CollectionState, player: int):
    return any([
        state.has("Sword (Progressive)", player),
        st_has_bombs(state, player),
        state.has("Bow (Progressive)", player),
        state.has("Whip", player),
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
        st_has_whip(state, player),
        st_has_beam_sword(state, player),
        all([
            st_has_sword(state, player),
            any([
                st_has_boomerang(state, player),
            ])
        ])
    ])


def st_can_kill_eye_brute(state: CollectionState, player: int):
    return any([
        st_option_hard_logic(state, player),
        st_has_bow(state, player),
    ])


def st_can_kill_bubble(state: CollectionState, player: int):
    return any([
        st_has_bombs(state, player),
        st_has_bow(state, player),
        st_has_whip(state, player),
        all([
            st_has_sword(state, player), any([
                st_has_boomerang(state, player),
            ])
        ])
    ])


def st_totok_stantom_steal_object(state, player):
    return any([
        st_clever_pots(state, player),
        st_can_kill_bat(state, player)
    ])


def st_has_range(state: CollectionState, player: int):
    return state.has_any(["Boomerang", "Bow (Progressive)", "Whip"], player)


def st_has_short_range(state: CollectionState, player: int):
    return any([st_has_mid_range(state, player),
                st_clever_bombs(state, player), ])


def st_has_mid_range(state: CollectionState, player: int):
    return any([st_has_range(state, player),
                st_has_beam_sword(state, player)])


def st_has_beam_sword(state: CollectionState, player: int):
    return all([
        st_has_sword(state, player),
        st_has_sword_beam_scroll(state, player)
    ])


def st_can_hit_spin_switches(state: CollectionState, player: int):
    return any([
        st_has_sword(state, player),
        all([
            st_option_hard_logic(state, player),
            any([
                st_has_bombs(state, player),
                st_has_boomerang(state, player)
            ])
        ])
    ])


def st_spiral_wall_switches(state: CollectionState, player: int):
    return any([
        st_has_boomerang(state, player),
        st_has_bombs(state, player)
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
    return any([st_has_sword(state, player), st_has_bombs(state, player)])


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

    # # Sell Treasure for safe average 150 (can be 50, 150, 800 or 1500)
    # if st_has_courage_crest(state, player):
    #     rupees += state.count_group("Treasure Items", player) * 150

    return rupees >= cost


def st_can_farm_rupees(state: CollectionState, player: int):
    return any([
        all([
            #st_has_courage_crest(state, player),  # Can Sell Treasure
            any([
            ])
        ]),
    ])

# def st_beedle_shop(state, player, price):
#     other_costs = 550
#     if st_has_bow(state, player):
#         other_costs += 1000
#         if st_has_chus(state, player):
#             other_costs += 3000
#     if st_has_bombs(state, player):
#         other_costs += 1000
#     if st_option_randomize_masked_beedle(state, player):
#         other_costs += 1500
#     return st_has_rupees(state, player, price + other_costs)

#
# def st_can_buy_quiver(state: CollectionState, player: int):
#     return all([st_has_bow(state, player), st_island_shop(state, player, 1500)])


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


# def st_option_stantoms_hard(state: CollectionState, player: int):
#     return all([state.multiworld.worlds[player].options.stantom_combat_difficulty in ["require_weapon"],
#                 st_has_whip(state, player)])


# def st_option_stantoms_med(state: CollectionState, player: int):
#     return all([state.multiworld.worlds[player].options.stantom_combat_difficulty in ["require_weapon", "require_stun"],
#                 any([
#                     st_has_bow(state, player),
#                     st_has_hammer(state, player),
#                     st_has_fire_sword(state, player)
#                 ])])
#
#
# def st_option_stantoms_easy(state: CollectionState, player: int):
#     return (state.multiworld.worlds[player].options.stantom_combat_difficulty in
#             ["require_weapon", "require_stun", "require_traps"])

#
# def st_option_stantoms_sword_only(state: CollectionState, player: int):
#     return all([state.multiworld.worlds[player].options.stantom_combat_difficulty in
#                 ["require_weapon", "require_stun", "require_traps", "require_stantom_sword"],
#                 st_has_stantom_sword(state, player)])


def st_clever_pots(state: CollectionState, player: int):
    return st_option_hard_logic(state, player)


def st_can_hit_switches(state: CollectionState, player: int):
    return any([st_option_hard_logic(state, player), st_can_kill_bat(state, player)])


def st_clever_bombs(state: CollectionState, player: int):
    return all([st_has_bombs(state, player),
                st_option_hard_logic(state, player)])

#
# def st_option_randomize_frogs(state: CollectionState, player: int):
#     return state.multiworld.worlds[player].options.randomize_frogs == "randomize"
#
#
# def st_option_start_with_frogs(state: CollectionState, player: int):
#     return state.multiworld.worlds[player].options.randomize_frogs == "start_with"


# def st_beat_required_dungeons(state: CollectionState, player: int):
#     # print(f"Dungeons required: {state.count_group('Current Metals', player)}/{state.multiworld.worlds[player].options.dungeons_required} {state.has_group("Current Metals", player,
#     #                       state.multiworld.worlds[player].options.dungeons_required)}")
#     return state.has_group("Current Metals", player,
#                            state.multiworld.worlds[player].options.dungeons_required)


def st_option_train_requires_forest_glyph(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.train_requires_forest_glyph


def st_option_goal_ToS_section_1(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.goal == "beat_ToS_section_1"


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

# def st_can_kill_stantoms(state: CollectionState, player: int):
#     return any([
#         st_option_stantoms_hard(state, player),
#         st_option_stantoms_med(state, player),
#         st_option_stantoms_sword_only(state, player)
#     ])


# def st_can_kill_stantoms_traps(state: CollectionState, player: int):
#     return any([
#         st_option_stantoms_hard(state, player),
#         st_option_stantoms_med(state, player),
#         st_option_stantoms_easy(state, player),
#         st_option_stantoms_sword_only(state, player)
#     ])


def st_can_hit_tricky_switches(state: CollectionState, player: int):
    return any([
        st_clever_pots(state, player),
        st_has_short_range(state, player)
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
# def st_totok_b1_all_checks_ut(state, player):
#     return all([
#         st_ut_small_key_own_dungeon(state, player),
#         st_has_spirit(state, player, "Power"),
#         st_has_bow(state, player),
#         st_has_whip(state, player),
#         st_can_kill_stantoms(state, player),
#     ])


# Overworld

def st_train_access(state, player):
    return any([
        not st_option_train_requires_forest_glyph(state, player),
        st_has_glyph(state, player, "Forest")
    ])


# Handles keylocking due to lack of locations
# def st_can_reach_MP2(state: CollectionState, player: int):
#     return any([
#         all([
#             st_option_keysanity(state, player),
#             st_has_small_keys(state, player, "Mountain Passage", 2)
#         ]),
#         all([
#             st_option_keys_in_own_dungeon(state, player),
#             any([
#                 st_can_cut_small_trees(state, player),
#                 st_option_glitched_logic(state, player)  # SW in back entrance / reversse cuccoo jump
#             ]),
#             any([
#                 st_has_small_keys(state, player, "Mountain Passage"),
#                 st_is_ut(state, player)
#             ])
#         ])
#     ])


# Goal Stuff

def st_temp_goal(state, player):
    return all([st_has_glyph(state, player, "Forest"),
                st_has_sword(state, player)])
