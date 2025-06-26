from BaseClasses import CollectionState
from Options import Accessibility
from .Constants import *


# =========== Item States =============

def ph_has_sword(state: CollectionState, player: int):
    return state.has("Sword (Progressive)", player)


def ph_has_phantom_sword(state: CollectionState, player: int):
    return state.has("Sword (Progressive)", player, 2)


def ph_has_shield(state: CollectionState, player: int):
    # Shield can be bought from shop
    return True


def ph_has_shovel(state: CollectionState, player: int):
    return state.has("Shovel", player)


def ph_has_bow(state: CollectionState, player: int):
    return state.has("Bow (Progressive)", player)


def ph_has_bombs(state: CollectionState, player: int):
    return state.has("Bombs (Progressive)", player)


def ph_has_chus(state: CollectionState, player: int):
    return state.has("Bombchus (Progressive)", player)


def ph_has_grapple(state: CollectionState, player: int):
    return state.has("Grappling Hook", player)


def ph_has_hammer(state: CollectionState, player: int):
    return state.has("Hammer", player)


def ph_has_boomerang(state: CollectionState, player: int):
    return state.has("Boomerang", player)


def ph_has_spirit(state: CollectionState, player: int, spirit: str, count: int = 1):
    return state.has(f"Spirit of {spirit} (Progressive)", player, count)


def ph_has_spirit_gems(state: CollectionState, player: int, spirit: str, count: int = 1):
    return all([state.has(f"{spirit} Gem", player, count),
                ph_has_spirit(state, player, spirit)])


def ph_has_sun_key(state: CollectionState, player: int):
    return state.has("Sun Key", player)


def ph_has_ghost_key(state: CollectionState, player: int):
    return state.has("Ghost Key", player)


def ph_has_kings_key(state: CollectionState, player: int):
    return state.has("King's Key", player)


def ph_has_regal_necklace(state: CollectionState, player: int):
    return state.has("Regal Necklace", player)


def ph_has_phantom_blade(state: CollectionState, player: int):
    return state.has("Phantom Blade", player)


def ph_has_heros_new_clothes(state: CollectionState, player: int):
    return state.has("Hero's New Clothes", player)


def ph_has_guard_notebook(state: CollectionState, player: int):
    return state.has("Guard Notebook", player)


def ph_has_kaleidoscope(state: CollectionState, player: int):
    return state.has("Kaleidoscope", player)


def ph_has_wood_heart(state: CollectionState, player: int):
    return state.has("Wood Heart", player)


def ph_has_triforce_crest(state: CollectionState, player: int):
    return any([state.has("Triforce Crest", player),
                not ph_option_triforce_crest(state, player)])


# ========= Sea Items =============

def ph_has_sea_chart(state: CollectionState, player: int, quadrant: str):
    return state.has(f"{quadrant} Sea Chart", player)


def ph_has_courage_crest(state: CollectionState, player: int):
    return state.has("Courage Crest", player)


def ph_has_cannon(state: CollectionState, player: int):
    return state.has("Cannon", player)


def ph_has_salvage(state: CollectionState, player: int):
    return state.has("Salvage Arm", player)


# ============== Frogs =======================

def ph_has_cyclone_slate(state: CollectionState, player: int):
    return state.has("Cyclone Slate", player)


# Does not mean you can logically get back, use the other frogs
def ph_has_frog(state: CollectionState, player: int, glyph: str, quadrant: str):
    return all([
        ph_has_sea_chart(state, player, quadrant),
        ph_has_cyclone_slate(state, player),
        any([
            state.has(f"Frog Glyph {glyph}", player),
            ph_option_start_with_frogs(state, player)
        ])
    ])


def ph_has_frog_x(state: CollectionState, player: int):
    return ph_has_frog(state, player, "X", "SW")


def ph_has_frog_phi(state: CollectionState, player: int):
    return all([
        ph_has_frog(state, player, "Phi", "SW"),
        any([
            ph_has_cannon(state, player),
            ph_has_frog_x(state, player),
            ph_has_sea_chart(state, player, "NW")
        ])
    ])


def ph_has_frog_n(state: CollectionState, player: int):
    return ph_has_frog(state, player, "N", "NW")


def ph_has_frog_omega(state: CollectionState, player: int):
    return ph_has_frog(state, player, "Omega", "SE")


def ph_has_frog_w(state: CollectionState, player: int):
    return ph_has_frog(state, player, "W", "SE")


def ph_has_frog_square(state: CollectionState, player: int):
    return all([
        ph_has_frog(state, player, "Square", "NE"),
        any([
            ph_has_sea_chart(state, player, "SE"),
            ph_has_frog_phi(state, player),
            ph_has_frog_n(state, player),
            ph_has_frog_x(state, player)
        ])
    ])


# =========== Combined item states ================

def ph_has_explosives(state: CollectionState, player: int):
    return state.has_any(["Bombs (Progressive)", "Bombchus (Progressive)"], player)


def ph_has_damage(state: CollectionState, player: int):
    return any([
        state.has("Sword (Progressive)", player),
        ph_has_explosives(state, player),
        state.has("Bow (Progressive)", player),
        state.has("Grappling Hook", player),
        state.has("Hammer", player)
    ])


def ph_has_cave_damage(state: CollectionState, player: int):
    return any([
        state.has("Sword (Progressive)", player),
        ph_has_bombs(state, player),
        state.has("Bow (Progressive)", player),
        state.has("Grappling Hook", player),
        state.has("Hammer", player)
    ])


def ph_can_kill_bat(state: CollectionState, player: int):
    return any([
        ph_has_damage(state, player),
        ph_has_boomerang(state, player)
    ])


def ph_can_kill_bubble(state: CollectionState, player: int):
    return any([
        ph_has_hammer(state, player),
        ph_has_explosives(state, player),
        ph_has_bow(state, player),
        ph_has_grapple(state, player),
        ph_has_fire_sword(state, player),
        all([
            ph_has_sword(state, player), any([
                ph_has_boomerang(state, player),
                ph_has_super_shield(state, player)  # This is the one logical use for shield!!!
            ])
        ])
    ])


def ph_has_range(state: CollectionState, player: int):
    return state.has_any(["Boomerang", "Bow (Progressive)", "Grappling Hook"], player)


def ph_has_short_range(state: CollectionState, player: int):
    return any([ph_has_mid_range(state, player),
                ph_clever_bombs(state, player), ])


def ph_has_mid_range(state: CollectionState, player: int):
    return any([ph_has_range(state, player),
                ph_has_hammer(state, player),
                ph_has_beam_sword(state, player)])


def ph_has_fire_sword(state: CollectionState, player: int):
    return all([
        ph_has_sword(state, player),
        ph_has_spirit(state, player, "Power", 2)
    ])


def ph_has_super_shield(state: CollectionState, player: int):
    return all([
        ph_has_shield(state, player),
        ph_has_spirit(state, player, "Wisdom", 2)
    ])


def ph_has_beam_sword(state: CollectionState, player: int):
    return all([
        ph_has_sword(state, player),
        ph_has_spirit(state, player, "Courage", 2)
    ])


def ph_can_hit_spin_switches(state: CollectionState, player: int):
    return any([
        ph_has_sword(state, player),
        all([
            ph_option_med_logic(state, player),
            any([
                ph_has_explosives(state, player),
                ph_has_boomerang(state, player)
            ])
        ])
    ])


def ph_spiral_wall_switches(state: CollectionState, player: int):
    return any([
        ph_has_boomerang(state, player),
        ph_has_hammer(state, player),
        ph_has_explosives(state, player)
    ])


# ================ Rupee States ==================


def ph_has_rupees(state: CollectionState, player: int, cost: int):
    # If has a farmable minigame and the means to sell, expensive things are in logic.
    if ph_can_farm_rupees(state, player):
        return True

    # Count up regular rupee items
    rupees = state.count("Green Rupee (1)", player)
    rupees += state.count("Blue Rupee (5)", player) * 5
    rupees += state.count("Red Rupee (20)", player) * 20
    rupees += state.count("Big Green Rupee (100)", player) * 100
    rupees += state.count("Big Red Rupee (200)", player) * 200
    rupees += state.count("Gold Rupee (300)", player) * 300

    # Sell Treasure for safe average 150 (can be 50, 150, 800 or 1500)
    if ph_has_courage_crest(state, player):
        rupees += state.count_group("Treasure Items", player) * 150

    return rupees >= cost


def ph_can_farm_rupees(state: CollectionState, player: int):
    return any([
        all([
            ph_has_courage_crest(state, player),  # Can Sell Treasure
            any([
                all([  # Can Farm Phantoms in TotOK
                    ph_has_phantom_sword(state, player),
                    ph_has_spirit(state, player, "Power")
                ]),
                state.has("_beat_toc", player),
                state.has("_can_play_cannon_game", player),
            ])
        ]),
        all([  # Can farm harrow (and chooses to play with harrow)
            state.has("_can_play_harrow", player),
            ph_option_randomize_harrow(state, player)
        ])
    ])


def ph_island_shop(state, player, price):
    other_costs = 0
    if ph_has_sea_chart(state, player, "SW"):
        # Includes cannon island, but not salvage arm cause that also unlocks treasure shop
        other_costs += 1550  # TODO this might break generation
    return ph_has_rupees(state, player, price + other_costs)


def ph_beedle_shop(state, player, price):
    other_costs = 550
    if ph_has_bow(state, player):
        other_costs += 1000
        if ph_has_chus(state, player):
            other_costs += 3000
    if ph_has_bombs(state, player):
        other_costs += 1000
    return ph_has_rupees(state, player, price + other_costs)


def ph_can_buy_gem(state: CollectionState, player: int):
    return all([ph_has_bow(state, player), ph_island_shop(state, player, 500)])


def ph_can_buy_quiver(state: CollectionState, player: int):
    return all([ph_has_bow(state, player), ph_island_shop(state, player, 1500)])


def ph_can_buy_chu_bag(state: CollectionState, player: int):
    return all([ph_has_chus(state, player), ph_has_bow(state, player), ph_island_shop(state, player, 2500)])


def ph_can_buy_heart(state: CollectionState, player: int):
    return all([ph_has_chus(state, player), ph_has_bow(state, player), ph_island_shop(state, player, 4500)])


# ============ Option states =============

def ph_option_glitched_logic(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.logic == "glitched"


def ph_option_normal_logic(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.logic == "normal"


def ph_option_med_logic(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.logic in ["medium", "glitched"]


def ph_option_not_glitched_logic(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.logic in ["medium", "normal"]


def ph_option_keysanity(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.keysanity == "anywhere"


def ph_option_phantoms_hard(state: CollectionState, player: int):
    return all([state.multiworld.worlds[player].options.phantom_combat_difficulty in ["require_weapon"],
                ph_has_grapple(state, player)])


def ph_option_phantoms_med(state: CollectionState, player: int):
    return all([state.multiworld.worlds[player].options.phantom_combat_difficulty in ["require_weapon", "require_stun"],
                any([
                    ph_has_bow(state, player),
                    ph_has_hammer(state, player),
                    ph_has_fire_sword(state, player)
                ])])


def ph_option_phantoms_easy(state: CollectionState, player: int):
    return (state.multiworld.worlds[player].options.phantom_combat_difficulty in
            ["require_weapon", "require_stun", "require_traps"])


def ph_option_phantoms_sword_only(state: CollectionState, player: int):
    return all([state.multiworld.worlds[player].options.phantom_combat_difficulty in
                ["require_weapon", "require_stun", "require_traps", "require_phantom_sword"],
                ph_has_phantom_sword(state, player)])


def ph_clever_pots(state: CollectionState, player: int):
    return ph_option_med_logic(state, player)


def ph_can_hit_switches(state: CollectionState, player: int):
    return any([ph_option_med_logic(state, player), ph_can_kill_bat(state, player)])


def ph_clever_bombs(state: CollectionState, player: int):
    return all([ph_has_bombs(state, player),
                ph_option_med_logic(state, player)])


def ph_option_randomize_frogs(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.randomize_frogs == "randomize"


def ph_option_start_with_frogs(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.randomize_frogs == "start_with"


def ph_option_triforce_crest(state, player):
    return state.multiworld.worlds[player].options.randomize_triforce_crest


def ph_beat_required_dungeons(state: CollectionState, player: int):
    # print(f"Dungeons required: {state.count_group("Current Metals", player)}/{state.multiworld.worlds[player].options.dungeons_required} {state.has_group("Current Metals", player,
    #                       state.multiworld.worlds[player].options.dungeons_required)}")
    return state.has_group("Current Metals", player,
                           state.multiworld.worlds[player].options.dungeons_required)


def ph_goal_option_phantom_door(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.bellum_access == "spawn_phantoms_on_b13"


def ph_goal_option_staircase(state: CollectionState, player: int):
    return (state.multiworld.worlds[player].options.bellum_access in
            ["spawn_phantoms_on_b13", "spawn_phantoms_on_b13", "warp_to_bellum"])


def ph_goal_option_warp(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.bellum_access == "warp_to_bellum"


def ph_goal_option_spawn_bellumbeck(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.bellum_access == "spawn_bellumbeck"


def ph_option_boat_requires_sea_chart(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.boat_requires_sea_chart


def ph_option_fog_vanilla(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.fog_settings in ["vanilla_fog", "no_fog"]


def ph_option_fog_open(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.fog_settings == "open_ghost_ship"


def ph_option_randomize_harrow(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.randomize_harrow


# ============= Key logic ==============

def ph_has_small_keys(state: CollectionState, player: int, dung_name: str, amount: int = 1):
    return state.has(f"Small Key ({dung_name})", player, amount)


def ph_has_boss_key(state: CollectionState, player: int, dung_name: str):
    return state.has(f"Boss Key ({dung_name})", player)


def ph_has_force_gems(state, player, floor=3, count=3):
    return state.has(f"Force Gem (B{floor})", player, count)


def ph_has_shape_crystal(state: CollectionState, player: int, dung_name: str, shape: str):
    return state.has(f"{shape} Crystal ({dung_name})", player)


# ============= Location states ========

def ph_can_cut_small_trees(state: CollectionState, player: int):
    return any([ph_has_sword(state, player), ph_has_explosives(state, player)])


# Handles keylocking due to lack of locations
def ph_can_reach_MP2(state: CollectionState, player: int):
    return any([
        all([
            ph_option_keysanity(state, player),
            ph_has_small_keys(state, player, "Mountain Passage", 2)
        ]),
        all([
            not ph_option_keysanity(state, player),
            ph_has_small_keys(state, player, "Mountain Passage")
        ])
    ])


def ph_totok_b5(state: CollectionState, player: int):
    return all([
        ph_can_kill_bubble(state, player),
        any([
            ph_has_mid_range(state, player),
            ph_clever_bombs(state, player)])
    ])


# ======== Harder Logic ===========

def ph_can_kill_phantoms(state: CollectionState, player: int):
    return any([
        ph_option_phantoms_hard(state, player),
        ph_option_phantoms_med(state, player),
        ph_option_phantoms_sword_only(state, player)
    ])


def ph_can_kill_phantoms_traps(state: CollectionState, player: int):
    return any([
        ph_option_phantoms_hard(state, player),
        ph_option_phantoms_med(state, player),
        ph_option_phantoms_easy(state, player),
        ph_option_phantoms_sword_only(state, player)
    ])


def ph_can_hit_tricky_switches(state: CollectionState, player: int):
    return any([
        ph_clever_pots(state, player),
        ph_has_short_range(state, player)
    ])


def ph_can_hammer_clip(state: CollectionState, player: int):
    return all([ph_has_hammer(state, player), ph_option_glitched_logic(state, player)])


def ph_can_hit_bombchu_switches(state: CollectionState, player: int):
    return any([
        ph_can_hammer_clip(state, player),
        ph_has_chus(state, player)
    ])


def ph_can_boomerang_return(state: CollectionState, player: int):
    return all([
        ph_has_boomerang(state, player),
        ph_option_glitched_logic(state, player)
    ])


def ph_can_arrow_despawn(state: CollectionState, player: int):
    return all([
        ph_has_bow(state, player),
        ph_option_glitched_logic(state, player)
    ])


def ph_totok_b2_key(state: CollectionState, player: int):
    return any([ph_can_boomerang_return(state, player),
                all([ph_can_hit_switches(state, player),
                     any([ph_option_med_logic(state, player),
                          ph_has_explosives(state, player),
                          ph_can_hit_tricky_switches(state, player)
                          ])
                     ])
                ])


def ph_boat_access(state, player):
    return any([
        not ph_option_boat_requires_sea_chart(state, player),
        ph_has_sea_chart(state, player, "SW")
    ])


def ph_totok_b5_key_logic(state: CollectionState, player: int):
    # TODO: Does not take into account force gem shuffling
    return any([
        all([ph_has_small_keys(state, player, "Temple of the Ocean King", 4), ph_has_grapple(state, player)]),
        ph_has_small_keys(state, player, "Temple of the Ocean King", 5),
    ])


def ph_has_totok_crystal(state: CollectionState, player: int, shape: str):
    return state.has(f"{shape} Crystal ({"Temple of the Ocean King"})", player)


def ph_totok_b8_2_crystals(state, player):
    return all([
        ph_has_explosives(state, player),
        ph_has_totok_crystal(state, player, "Round"),
        ph_has_totok_crystal(state, player, "Triangle")
    ])


def ph_totok_b9(state, player):
    return any([
        ph_can_hit_bombchu_switches(state, player),
        all([
            ph_has_explosives(state, player),
            ph_has_totok_crystal(state, player, "Triangle")])
    ])


def ph_totok_b9_phantom_kill(state, player):
    return any([
        ph_has_phantom_sword(state, player),
        all([
            ph_can_kill_phantoms_traps(state, player),
            any([
                ph_has_hammer(state, player),
                all([ph_has_bow(state, player), ph_has_boomerang(state, player)])
            ])])
    ])


def ph_totok_b10_key_logic(state: CollectionState, player: int):
    # TODO: Does not take into account force gem shuffling
    return any([
        all([ph_has_small_keys(state, player, "Temple of the Ocean King", 5), ph_has_grapple(state, player)]),
        ph_has_small_keys(state, player, "Temple of the Ocean King", 6),
    ])


def ph_totok_b12(state: CollectionState, player: int):
    return any([
        ph_has_hammer(state, player),
        ph_has_shovel(state, player)
    ])


def ph_totok_b13_door(state: CollectionState, player: int):
    # Required to enter the phantom door
    return all([
        ph_has_phantom_sword(state, player),
        any([
            all([ph_goal_option_phantom_door(state, player),
                 ph_beat_required_dungeons(state, player)]),
            ph_goal_option_staircase(state, player)
        ])
    ])


def ph_totok_blue_warp(state: CollectionState, player: int):
    return all([
        ph_goal_option_warp(state, player),
        ph_beat_required_dungeons(state, player)
    ])


def ph_totok_bellum_staircase(state, player):
    return ph_beat_required_dungeons(state, player)



def ph_can_beat_bellum(state, player):
    return all([
        ph_has_grapple(state, player),
        ph_has_phantom_sword(state, player),
        ph_has_bow(state, player),
        ph_has_spirit(state, player, "Courage")
    ])


def ph_can_beat_ghost_ship_fight(state, player):
    return ph_has_cannon(state, player)


def ph_can_beat_bellumbeck(state, player):
    return all([
        ph_has_phantom_sword(state, player),
        ph_has_spirit(state, player, "Courage")
    ])

def ph_bellumbeck_quick_finish(state, player):
    return all([
        ph_can_beat_bellumbeck(state, player),
        ph_beat_required_dungeons(state, player),
        ph_goal_option_spawn_bellumbeck(state, player)
    ])

def ph_tof_3f(state, player):
    return all([
        ph_has_small_keys(state, player, "Temple of Fire", 2),
        any([
            ph_has_boomerang(state, player),
            ph_has_hammer(state, player),
            ph_clever_bombs(state, player)
        ])
    ])


def ph_salvage_courage_crest(state: CollectionState, player: int):
    return all([
        ph_has_courage_crest(state, player),
        ph_has_salvage(state, player),
        # The sea monster is disabled, otherwise add cannon to reqs
    ])


def ph_can_enter_ocean_sw_west(state, player):
    return any([
        ph_has_cannon(state, player),
        ph_has_frog_phi(state, player),  # Includes return data, and NW way back
    ])


def ph_can_enter_toc(state, player):
    return all([
        ph_has_damage(state, player),
        any([
            ph_has_boomerang(state, player),
            ph_has_bow(state, player)
        ])
    ])


def ph_toc_key_doors(state, player, glitched: int, not_glitched: int):
    return any([
        all([
            ph_option_glitched_logic(state, player),
            ph_has_small_keys(state, player, "Temple of Courage", glitched)
        ]),
        all([
            ph_option_not_glitched_logic(state, player),
            ph_has_small_keys(state, player, "Temple of Courage", not_glitched)
        ])
    ])


def ph_toi_key_doors(state, player, glitched: int, not_glitched: int):
    return any([
        all([
            ph_option_glitched_logic(state, player),
            ph_has_small_keys(state, player, "Temple of Ice", glitched)
        ]),
        all([
            ph_option_not_glitched_logic(state, player),
            ph_has_small_keys(state, player, "Temple of Ice", not_glitched)
        ])
    ])


def ph_mutoh_key_doors(state, player, glitched: int, not_glitched: int):
    return any([
        all([
            ph_option_glitched_logic(state, player),
            ph_has_small_keys(state, player, "Mutoh's Temple", glitched)
        ]),
        all([
            ph_option_not_glitched_logic(state, player),
            ph_has_small_keys(state, player, "Mutoh's Temple", not_glitched)
        ])
    ])


def ph_has_ghost_ship_access(state, player):
    return any([
        all([
            ph_has_spirit(state, player, "Power"),
            ph_has_spirit(state, player, "Wisdom"),
            ph_has_spirit(state, player, "Courage"),
            ph_option_fog_vanilla(state, player)
        ]),
        ph_option_fog_open(state, player)
    ])


def ph_ghost_ship_barrel(state, player):
    return any([
        ph_has_bombs(state, player),
        ph_has_hammer(state, player),
        ph_has_boomerang(state, player),
        ph_has_grapple(state, player)
    ])


def ph_toc_final_switch_state(state, player):
    return any([
        ph_has_bow(state, player),
        ph_toc_key_doors(state, player, 2, 1)
    ])


def ph_goron_chus(state, player):
    return all([
        ph_has_shovel(state, player),
        ph_has_mid_range(state, player)
    ])


def ph_bannan_scroll(state, player):
    return all([
        ph_has_wood_heart(state, player),
        ph_has_cannon(state, player),
        ph_has_sea_chart(state, player, "SE"),
    ])


def ph_mutoh_water(state, player):
    return any([
        all([
            ph_mutoh_key_doors(state, player, 2, 1),
            ph_has_bow(state, player),
        ]),
        ph_can_arrow_despawn(state, player)
    ])


def ph_beat_ghost_ship(state: CollectionState, player):
    return state.has("_beat_ghost_ship", player)


def ph_temp_goal(state, player):
    return all([ph_has_sea_chart(state, player, "SW"),
                ph_has_phantom_sword(state, player),
                ph_has_courage_crest(state, player)])
