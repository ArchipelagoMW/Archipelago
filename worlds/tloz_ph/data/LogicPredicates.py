from math import floor, ceil

from BaseClasses import CollectionState
from Options import Accessibility
from .Constants import *


# =========== Item States =============

def ph_has_sword(state: CollectionState, player: int):
    return any([
        state.has("Sword (Progressive)", player),
        state.has("Oshus' Sword", player)
    ])


def ph_has_phantom_sword(state: CollectionState, player: int):
    return any([
        state.has("Sword (Progressive)", player, 2),
        all([
            ph_has_sword(state, player),
            state.has("Phantom Sword", player)
        ])
    ])


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
    pack_size = state.multiworld.worlds[player].options.spirit_gem_packs
    return all([
        ph_has_spirit(state, player, spirit),
        any([
            state.has(f"{spirit} Gem", player, count),
            state.has(f"{spirit} Gem Pack", player, ceil(count / pack_size)),
        ])

    ])


def ph_has_phantom_hourglass(state, player):
    return state.has("Phantom Hourglass", player)


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


def ph_has_fishing_rod(state, player):
    return state.has("Fishing Rod", player)


def ph_has_big_catch_lure(state, player):
    return state.has("Big Catch Lure", player)


def ph_has_swordfish_shadows(state, player):
    return state.has("Swordfish Shadows", player)


def ph_can_catch_rsf(state, player):
    return any([
        ph_has_big_catch_lure(state, player),
        ph_has_swordfish_shadows(state, player)
    ])


def ph_ut_can_stowfish(state, player):
    return all([
        ph_has_swordfish_shadows(state, player),
        any([
            ph_UT_glitched_logic(state, player),
            ph_has_big_catch_lure(state, player)
        ])
    ])


def ph_has_loovar(state, player):
    return state.has("Fish: Loovar", player)


def ph_has_rsf(state, player):
    return state.has("Fish: Rusty Swordfish", player)


def ph_has_neptoona(state, player):
    return state.has("Fish: Legendary Neptoona", player)


def ph_has_stowfish(state, player):
    return state.has("Fish: Stowfish", player)


def ph_has_jolene_letter(state, player):
    return state.has("Jolene's Letter", player)


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


def ph_has_treasure_map(state, player, number):
    map_name = ITEM_GROUPS["Treasure Maps"][number - 1]
    return state.has(map_name, player)


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


def ph_can_kill_blue_chu(state: CollectionState, player: int):
    return any([
        ph_has_bombs(state, player),  # Only place this is relevant is in "cave"
        ph_has_bow(state, player),
        ph_has_grapple(state, player),
        ph_has_hammer(state, player),
        ph_has_beam_sword(state, player),
        all([
            ph_has_sword(state, player),
            any([
                ph_has_boomerang(state, player),
                ph_has_super_shield(state, player),
            ])
        ])
    ])


def ph_can_kill_phantom_eyes(state, player):
    return any([
        ph_clever_pots(state, player),
        ph_has_hammer(state, player),
        ph_has_phantom_sword(state, player),
        ph_has_explosives(state, player),
        ph_has_bow(state, player),
        ph_has_grapple(state, player)
    ])


def ph_can_kill_eye_brute(state: CollectionState, player: int):
    return any([
        ph_option_hard_logic(state, player),
        ph_has_hammer(state, player),
        ph_has_chus(state, player),
        all([
            ph_has_bow(state, player),
            ph_has_sword(state, player)
        ]),
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


def ph_totok_phantom_steal_object(state, player):
    return any([
        ph_clever_pots(state, player),
        ph_can_kill_bat(state, player)
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


def ph_has_mid_range_pots(state, player):
    return any([
        ph_has_mid_range(state, player),
        ph_clever_pots(state, player)
    ])


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
            ph_option_hard_logic(state, player),
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


def ph_quick_switches(state, player):
    return any([
        ph_has_boomerang(state, player),
        all([
            ph_has_bow(state, player),
            ph_option_hard_logic(state, player)
        ])
    ])


def ph_can_cut_small_trees(state: CollectionState, player: int):
    return any([ph_has_sword(state, player), ph_has_explosives(state, player)])


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
                all([  # Can Farm Minigames
                    ph_option_randomize_minigames(state, player),
                    any([
                        state.has("_beat_toc", player),  # Archery Game
                        state.has("_can_play_cannon_game", player),
                        state.has("_can_play_goron_race", player),
                    ])
                ])
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
        other_costs += 1550
        if ph_option_randomize_masked_beedle(state, player):
            other_costs += 1500
        other_costs *= 0.7  # Cost multiplier, cause the chance of all checks being useful is low
    return ph_has_rupees(state, player, price + other_costs)


def ph_has_freebie_card(state, player):
    return state.has("Freebie Card", player)


def ph_beedle_shop(state, player, price):
    # Multiplier only applies to non-linear items
    multiplier = 0.7 if ph_option_shop_hints(state, player) else 1
    other_costs = 500 * multiplier + 50
    discount = ph_count_beedle_discount(state, player)  # Discount from points
    # Island shop items
    if ph_has_bow(state, player):
        other_costs += 1000
        if ph_has_chus(state, player):
            other_costs += 3000
    if ph_has_bombs(state, player):
        other_costs += 1000 * discount * multiplier  # Bomb bag is effected by discount
    if ph_option_randomize_masked_beedle(state, player):
        other_costs += 1500 * multiplier
    if ph_has_freebie_card(state, player):
        other_costs -= 500 * discount  # Freebie card assumed to be used for the 500r wisdom gem.
    return ph_has_rupees(state, player, price * discount + other_costs)


def ph_count_beedle_points(state, player):
    return (state.count("Beedle Points (10)", player) * 10 +
            state.count("Beedle Points (20)", player) * 20 +
            state.count("Beedle Points (50)", player) * 50)


def ph_count_beedle_discount(state, player):
    thresholds = {20: 0.9, 50: 0.8, 100: 0.7}
    res = 1
    points = ph_count_beedle_points(state, player)
    for threshold, discount in thresholds.items():
        if points >= threshold:
            res = discount
    return res

def ph_option_shop_hints(state, player):
    return state.multiworld.worlds[player].options.shop_hints

def ph_has_beedle_points_buyable(state, player, points):
    points_res = points - ph_count_beedle_points(state, player)
    if points_res > 0:
        cost = points_res * 100
    else:
        return True
    if ph_has_bombs(state, player):
        cost -= 1000 * ph_count_beedle_discount(state, player)
    return ph_beedle_shop(state, player, cost)


def ph_has_beedle_points(state: CollectionState, player, points):
    option = state.multiworld.worlds[player].options.randomize_beedle_membership
    if option == "randomize":
        if points <= 20:  # Buying 20 points is always in logic
            return ph_has_beedle_points_buyable(state, player, points)
        return ph_count_beedle_points(state, player) >= points
    elif option == "randomize_with_grinding":
        return ph_has_beedle_points_buyable(state, player, points)
    return False


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
    return state.multiworld.worlds[player].options.logic == "glitched" or state.has("_UT_Glitched_logic", player)


def ph_option_normal_logic(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.logic == "normal"


def ph_option_hard_logic(state: CollectionState, player: int):
    return (state.multiworld.worlds[player].options.logic in ["hard", "glitched"]
            or state.has("_UT_Glitched_logic", player))


def ph_option_not_glitched_logic(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.logic in ["hard", "normal"]


def ph_option_keysanity(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.keysanity == "anywhere"


def ph_option_keys_vanilla(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.keysanity == "vanilla"


def ph_option_keys_in_own_dungeon(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.keysanity in ["in_own_dungeon", "vanilla"]


def ph_option_phantoms_hard(state: CollectionState, player: int):
    return all([
        any([
            state.multiworld.worlds[player].options.phantom_combat_difficulty in ["require_weapon"],
            ph_UT_glitched_logic(state, player)
        ]),
        ph_has_grapple(state, player)
    ])


def ph_option_phantoms_med(state: CollectionState, player: int):
    return all([
        any([
            state.multiworld.worlds[player].options.phantom_combat_difficulty in ["require_weapon", "require_stun"],
            ph_UT_glitched_logic(state, player)
        ]),
        any([
            ph_has_bow(state, player),
            ph_has_hammer(state, player),
            ph_has_fire_sword(state, player)
        ])
    ])


def ph_option_phantoms_easy(state: CollectionState, player: int):
    return any([state.multiworld.worlds[player].options.phantom_combat_difficulty in
                ["require_weapon", "require_stun", "require_traps"],
                ph_UT_glitched_logic(state, player)])


def ph_option_phantoms_sword_only(state: CollectionState, player: int):
    return ph_has_phantom_sword(state, player)


def ph_clever_pots(state: CollectionState, player: int):
    return ph_option_hard_logic(state, player)


def ph_can_hit_switches(state: CollectionState, player: int):
    return any([ph_option_hard_logic(state, player), ph_can_kill_bat(state, player)])


def ph_clever_bombs(state: CollectionState, player: int):
    return all([ph_has_bombs(state, player),
                ph_option_hard_logic(state, player)])


def ph_option_randomize_minigames(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.randomize_minigames


def ph_option_randomize_frogs(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.randomize_frogs == "randomize"


def ph_option_start_with_frogs(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.randomize_frogs == "start_with"


def ph_option_triforce_crest(state, player):
    return state.multiworld.worlds[player].options.randomize_triforce_crest


def ph_has_required_metals(state: CollectionState, player: int):
    current_metals = state.count_from_list(ITEM_GROUPS["Metals"], player)
    return any([
        all([
            ph_option_goal_metal_hunt(state, player),
            current_metals >= state.multiworld.worlds[player].options.metal_hunt_required
        ]),
        all([
            ph_option_goal_dungeons(state, player),
            current_metals >= state.multiworld.worlds[player].options.dungeons_required
        ])
    ])


def ph_zauz_required_metals(state: CollectionState, player: int):
    current_metals = ITEM_GROUPS["Metals"]
    # print(f"Zauz {state.multiworld.worlds[player].options.zauz_required_metals} have {state.count_from_list(
    # current_metals, player)}")
    return state.has_from_list(current_metals, player,
                               state.multiworld.worlds[player].options.zauz_required_metals)


def ph_option_randomize_masked_beedle(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.randomize_masked_beedle


def ph_goal_option_phantom_door(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.bellum_access == "spawn_phantoms_on_b13"


def ph_goal_option_staircase(state: CollectionState, player: int):
    return True  # All goal options unlock staircase on goal req...


def ph_goal_option_warp(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.bellum_access == "warp_to_bellum"


def ph_goal_option_spawn_bellumbeck(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.bellum_access == "spawn_bellumbeck"


def ph_goal_option_instant_goal(state, player):
    return state.multiworld.worlds[player].options.bellum_access == "win"


def ph_option_boat_requires_sea_chart(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.boat_requires_sea_chart


def ph_option_fog_vanilla(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.fog_settings in ["vanilla_fog", "no_fog"]


def ph_option_fog_open(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.fog_settings == "open_ghost_ship"


def ph_option_randomize_harrow(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.randomize_harrow


def ph_option_goal_dungeons(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.goal_requirements == "complete_dungeons"


def ph_option_goal_metal_hunt(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.goal_requirements == "metal_hunt"


def ph_option_goal_midway(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.goal_requirements == "triforce_door"


def ph_can_pass_sea_monsters(state, player):
    return any([
        ph_has_cannon(state, player),
        state.multiworld.worlds[player].options.skip_ocean_fights
    ])


def ph_option_time_no_logic(state, player):
    time_option = state.multiworld.worlds[player].options.ph_time_logic
    return any([
        time_option == "no_logic",
        ph_UT_glitched_logic(state, player),
    ])


def ph_option_ph_required(state, player):
    return state.multiworld.worlds[player].options.ph_required


def ph_option_floor_time(state, player, room):
    time_option = state.multiworld.worlds[player].options.ph_time_logic
    if time_option.value not in [3, 4]:
        return False
    elif (time_option == "ph_only_b1" and room > 0) or (time_option == "ph_only_b4" and room > 3):
        return ph_has_phantom_hourglass(state, player)
    return True


def ph_option_time_divider(state, player):
    time_option = state.multiworld.worlds[player].options.ph_time_logic.value
    # print(f"Time option {time_option}")
    time_lookup = {0: 1, 1: 2, 2: 4}
    return time_lookup.get(time_option, 1)


def ph_has_time(state: CollectionState, player, time, room=4):
    # No time logic of floor + ph based time logic
    if ph_option_time_no_logic(state, player):
        return True

    time_option = state.multiworld.worlds[player].options.ph_time_logic.value
    if time_option > 2:
        return ph_option_floor_time(state, player, room)
    else:

        # Heart logic for if ph is required
        heart_time = state.multiworld.worlds[player].options.ph_heart_time.value
        heart_total = heart_time * (state.count("Heart Containers", player) + 2)
        multiplier = ph_option_time_divider(state, player)
        if ph_option_ph_required(state, player) and not ph_has_phantom_hourglass(state, player):
            return heart_total >= time // multiplier

        # Time calculations for proper time logic
        ph_time = state.multiworld.worlds[player].options.ph_starting_time.value
        sand_time = state.multiworld.worlds[player].options.ph_time_increment.value
        total_time = (ph_time * state.count("Phantom Hourglass", player) +
                      sand_time * state.count("Sand of Hours", player) +
                      60 * state.count("Sand of Hours (Small)", player) +
                      120 * state.count("Sand of Hours (Boss)", player) +
                      heart_total)

        return total_time >= time // multiplier


# For doing sneaky stuff with universal tracker UT
def ph_is_ut(state: CollectionState, player: int):
    return getattr(state.multiworld, "generation_is_fake", False)


def ph_UT_glitched_logic(state, player):
    return state.has("_UT_Glitched_logic", player)


# ============= Key logic ==============

def ph_has_small_keys(state: CollectionState, player: int, dung_name: str, amount: int = 1):
    return state.has(f"Small Key ({dung_name})", player, amount)


def ph_has_boss_key(state: CollectionState, player: int, dung_name: str):
    return state.has(f"Boss Key ({dung_name})", player)


def ph_has_boss_key_simple(state: CollectionState, player: int, dung_name: str):
    return any([
        ph_has_boss_key(state, player, dung_name),
        ph_is_ut(state, player)
    ])


def ph_has_force_gems(state, player, floor=3, count=3):
    return state.has(f"Force Gem (B{floor})", player, count)


def ph_has_shape_crystal(state: CollectionState, player: int, dung_name: str, shape: str):
    return state.has(f"{shape} Crystal ({dung_name})", player)


def ph_ut_small_key_vanilla_location(state, player):
    return all([
        ph_is_ut(state, player),
        ph_option_keys_vanilla(state, player)
    ])


def ph_ut_small_key_own_dungeon(state, player):
    return all([
        ph_is_ut(state, player),
        ph_option_keys_in_own_dungeon(state, player)
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


def ph_can_bcl(state, player):
    # Bombchu Camera Lock
    return all([
        ph_has_chus(state, player),
        ph_option_glitched_logic(state, player)
    ])


def ph_can_sword_glitch(state, player):
    return all([
        ph_has_sword(state, player),
        ph_option_glitched_logic(state, player)
    ])


def ph_can_sword_scroll_clip(state, player):
    return all([
        ph_has_sword(state, player),
        state.has("Swordsman's Scroll", player),
        ph_option_glitched_logic(state, player)
    ])


# ====== Specific locations =============

# TotOK
def ph_totok_b1_all_checks_ut(state, player):
    return all([
        ph_ut_small_key_own_dungeon(state, player),
        ph_has_spirit(state, player, "Power"),
        ph_totok_b1_bow(state, player),
        ph_totok_b1_key(state, player),
        ph_totok_b1_phantom(state, player),
    ])


def ph_totok_b2_all_checks_ut(state, player):
    return all([
        ph_totok_b1_all_checks_ut(state, player),
        ph_totok_b2_phantom(state, player),
        ph_totok_b2_key(state, player),
        ph_totok_b2_chu(state, player),
    ])


def ph_totok_b4_all_checks_ut(state, player):
    return all([
        ph_totok_b2_all_checks_ut(state, player),
        ph_has_spirit(state, player, "Wisdom"),
        # B3
        ph_totok_b3_phantom(state, player),
        ph_totok_b3_bow(state, player),
        # B4
        ph_totok_b4_phantom(state, player),
        ph_totok_b4_eyes(state, player),
        ph_totok_b4_key(state, player),
    ])


def ph_totok_b10_all_checks_ut(state, player):
    return all([
        ph_totok_b4_all_checks_ut(state, player),
        ph_has_triforce_crest(state, player),
        ph_has_sea_chart(state, player, "SW"),
        ph_has_hammer(state, player),
        ph_has_explosives(state, player),
        ph_has_shovel(state, player)
    ])


def ph_totok_b13_door(state: CollectionState, player: int):
    # Required to enter the phantom door
    return all([
        ph_has_phantom_sword(state, player),
        ph_totok_has_floor_time(state, player, 13, 30),
        any([
            all([ph_goal_option_phantom_door(state, player),
                 ph_has_required_metals(state, player)]),
            ph_goal_option_staircase(state, player)
        ])
    ])


# Overworld

def ph_boat_access(state, player):
    return any([
        not ph_option_boat_requires_sea_chart(state, player),
        ph_has_sea_chart(state, player, "SW")
    ])


# Handles keylocking due to lack of locations
def ph_can_reach_MP2(state: CollectionState, player: int):
    return any([
        all([
            ph_option_keysanity(state, player),
            ph_has_small_keys(state, player, "Mountain Passage", 2)
        ]),
        all([
            ph_option_keys_in_own_dungeon(state, player),
            any([
                ph_can_cut_small_trees(state, player),
                ph_option_glitched_logic(state, player)  # SW in back entrance / reversse cuccoo jump
            ]),
            any([
                ph_has_small_keys(state, player, "Mountain Passage"),
                ph_is_ut(state, player)
            ])
        ])
    ])


def ph_mercay_passage_rat(state, player):
    return any([
        ph_can_kill_bat(state, player),
        ph_clever_pots(state, player)
    ])


def ph_bannan_scroll(state, player):
    return all([
        ph_has_wood_heart(state, player),
        ph_can_pass_sea_monsters(state, player),
        ph_has_sea_chart(state, player, "SE"),
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


# Tof

def ph_tof_1f_key_ut(state, player):
    return all([
        ph_ut_small_key_own_dungeon(state, player),
        ph_can_kill_bat(state, player)
    ])


def ph_tof_3f(state, player):
    return all([
        any([
            ph_has_small_keys(state, player, "Temple of Fire", 2),
            ph_ut_small_key_own_dungeon(state, player)]),
        any([
            ph_has_boomerang(state, player),
            ph_has_hammer(state, player),
            ph_clever_bombs(state, player)
        ])
    ])


# Wind

def ph_wind_temple_key_ut(state, player):
    return all([
        ph_has_shovel(state, player),
        any([
            all([
                ph_has_bombs(state, player),
                ph_ut_small_key_own_dungeon(state, player)]),
            ph_ut_small_key_own_dungeon(state, player)
        ])
    ])


# Toc

def ph_can_enter_toc(state, player):
    return all([
        ph_has_damage(state, player),
        any([
            ph_has_boomerang(state, player),
            ph_has_bow(state, player)
        ])
    ])


def ph_toc_key_door_1(state, player):
    return any([
        ph_toc_key_doors(state, player, 3, 1),
        # UT Keys
        all([
            ph_option_not_glitched_logic(state, player),
            ph_ut_small_key_own_dungeon(state, player),
            any([
                ph_has_explosives(state, player),
                ph_option_keys_vanilla(state, player)
            ])
        ]),
    ])


def ph_toc_key_door_2(state, player):
    return any([
        ph_toc_key_doors(state, player, 3, 2),
        # UT stuff
        all([
            ph_option_not_glitched_logic(state, player),
            any([
                # Keys in own dungeon
                all([
                    ph_ut_small_key_own_dungeon(state, player),
                    ph_has_explosives(state, player),
                    ph_has_grapple(state, player),
                    ph_has_bow(state, player)
                ]),
                # Keys vanilla
                all([
                    ph_ut_small_key_vanilla_location(state, player),
                    any([
                        ph_has_explosives(state, player),
                        all([
                            ph_has_bow(state, player),
                            ph_has_grapple(state, player)
                        ])
                    ])
                ])
            ])
        ])
    ])


def ph_toc_key_door_3(state, player):
    return any([
        ph_has_small_keys(state, player, "Temple of Courage", 3),
        # UT
        all([
            ph_ut_small_key_own_dungeon(state, player),
            ph_has_bow(state, player),
            ph_has_explosives(state, player)
        ]),
        all([
            ph_ut_small_key_vanilla_location(state, player),
            any([
                ph_can_hammer_clip(state, player),
                all([
                    ph_has_bow(state, player),
                    any([
                        ph_has_grapple(state, player),
                        ph_has_explosives(state, player),
                    ])
                ])
            ])
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


def ph_toc_final_switch_state(state, player):
    return any([
        ph_has_bow(state, player),
        ph_toc_key_doors(state, player, 2, 1)
    ])


# Ghost Ship

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


def ph_beat_ghost_ship(state: CollectionState, player):
    return state.has("_beat_ghost_ship", player)


# Goron

def ph_goron_chus(state, player):
    return all([
        ph_has_shovel(state, player),
        any([
            ph_has_hammer(state, player),
            ph_has_bow(state, player),
            ph_has_grapple(state, player),
        ])
    ])


# Toi

def ph_toi_3f_boomerang(state, player):
    return all([
        ph_quick_switches(state, player),
        any([
            ph_has_boomerang(state, player),
            ph_has_grapple(state, player)
        ])
    ])


def ph_toi_b2(state, player):
    return all([
        ph_has_bow(state, player),
        ph_quick_switches(state, player),
        any([
            ph_toi_key_doors(state, player, 3, 2),
            ph_can_hammer_clip(state, player),
            ph_can_bcl(state, player)
        ])
    ])


def ph_toi_key_door_1_ut(state, player):
    return any([
        ph_toi_all_key_doors_ut(state, player),
        all([
            ph_option_not_glitched_logic(state, player),
            any([
                ph_ut_small_key_vanilla_location(state, player),
                all([
                    ph_ut_small_key_own_dungeon(state, player),
                    ph_has_explosives(state, player)
                ])
            ]),
        ])
    ])


def ph_toi_all_key_doors_ut(state, player):
    return all([
        ph_ut_small_key_own_dungeon(state, player),
        ph_has_grapple(state, player),
        ph_has_explosives(state, player),
        ph_has_bow(state, player),
        ph_quick_switches(state, player)
    ])


def ph_toi_key_doors(state, player, glitched: int, not_glitched: int = None):
    not_glitched = glitched if not_glitched is None else not_glitched
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


def ph_toi_key_door_2(state, player):
    return any([
        ph_toi_key_doors(state, player, 3, 2),
        # UT
        ph_toi_all_key_doors_ut(state, player),
        all([
            ph_option_not_glitched_logic(state, player),
            ph_ut_small_key_own_dungeon(state, player),
            ph_quick_switches(state, player)
        ])
    ])


def ph_toi_key_door_3(state, player):
    return any([
        ph_toi_key_doors(state, player, 3),
        # UT
        ph_toi_all_key_doors_ut(state, player),
    ])


# Mutoh's

def ph_mutoh_water(state, player):
    return any([
        all([
            any([
                ph_mutoh_key_doors(state, player, 2, 1),
                ph_ut_small_key_own_dungeon(state, player)  # This should account for all chests
            ]),
            ph_has_bow(state, player),
            any([
                ph_has_boomerang(state, player),
                ph_has_beam_sword(state, player)
            ])
        ]),
        ph_can_arrow_despawn(state, player),
        all([
            ph_has_beam_sword(state, player),
            ph_has_explosives(state, player),
            ph_option_glitched_logic(state, player)
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


# Goal Stuff

def ph_totok_blue_warp(state: CollectionState, player: int):
    return all([
        ph_goal_option_warp(state, player),
        ph_has_required_metals(state, player)
    ])


def ph_totok_bellum_staircase(state, player):
    return ph_has_required_metals(state, player)


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
        ph_has_required_metals(state, player),
        ph_goal_option_spawn_bellumbeck(state, player)
    ])


def ph_win_on_metals(state, player):
    return all([
        ph_has_required_metals(state, player),
        ph_goal_option_instant_goal(state, player)
    ])


def ph_temp_goal(state, player):
    return all([ph_has_sea_chart(state, player, "SW"),
                ph_has_phantom_sword(state, player),
                ph_has_courage_crest(state, player)])


# TotOK New Time Logic

def ph_time_1f(state, player):
    return 0


def ph_time_b1(state, player):
    return ph_time_1f(state, player) + 1


def ph_time_b2(state, player):
    return ph_time_b1(state, player) + 6


def ph_time_b3(state, player):
    if ph_can_hit_switches(state, player):
        return ph_time_b2(state, player) + 10
    elif ph_clever_pots(state, player):
        return ph_time_b2(state, player) + 30
    return 6000


def ph_time_b4(state, player):
    if ph_has_grapple(state, player):
        return ph_time_b3(state, player) + 8
    elif any([
        ph_has_force_gems(state, player, 3, 3),
        all([
            ph_is_ut(state, player),
            ph_has_small_keys(state, player, "Temple of the Ocean King", 4)
        ])
    ]):
        return ph_time_b3(state, player) + 60
    return 6000


def ph_time_b5(state, player):
    if ph_has_bow(state, player):
        return ph_time_b4(state, player) + 12
    elif ph_has_mid_range_pots(state, player):
        return ph_time_b4(state, player) + 25
    return 6000


def ph_time_b6(state, player):
    # Alt path
    if ph_can_hit_bombchu_switches(state, player):
        return ph_time_b5(state, player) + 15
    # normal path
    elif all([
        ph_can_kill_bubble(state, player),
        any([
            ph_has_mid_range(state, player),
            ph_clever_bombs(state, player)])
    ]):
        return ph_time_b5(state, player) + 25
    return 6000


def ph_time_b7(state, player):
    return ph_time_b6(state, player) + 10


def ph_time_b7_g(state, player):
    # Needs logic because of min statement later
    if ph_has_grapple(state, player):
        return ph_time_b7(state, player) + 10
    return 6000


def ph_time_b8(state, player):
    return min(ph_time_b7(state, player) + 20,
               ph_time_b8_shortcut(state, player))


def ph_time_b8_shortcut(state, player):
    comp = [6000]
    if ph_has_small_keys(state, player, "Temple of the Ocean King", 6):
        comp += [ph_time_b7_g(state, player) + 5]
        # comp += [ph_time_b7_e(state, player) + 20] Invalid, causes loop
    return min(comp)


def ph_time_b9_shortcut(state, player):
    return ph_time_b8_shortcut(state, player) + 2


def ph_time_b9(state, player):
    return min(ph_time_b8(state, player) + 10,
               ph_time_b9_shortcut(state, player))


def ph_time_b7_e(state, player):
    return ph_time_b8(state, player) + 7


def ph_time_b8_1c(state, player):
    comp = [ph_time_b7_g(state, player) + 20]
    if ph_can_hit_switches(state, player):
        comp.append(ph_time_b7_e(state, player) + 35)
    return min(comp)


def ph_time_b8_2c(state, player):
    return ph_time_b8_1c(state, player) + 20


def ph_time_b9_1c(state, player):
    comp = [6000]
    if ph_can_hit_bombchu_switches(state, player):
        comp += [ph_time_b8_1c(state, player) + 10]
        comp += [ph_time_b9_shortcut(state, player)]
    if ph_has_explosives(state, player) or ph_can_hit_bombchu_switches(state, player):
        comp += [ph_time_b8_2c(state, player) + 40]
    return min(comp)


def ph_time_b9_2c(state, player):
    comp = [6000]
    if ph_has_explosives(state, player) or ph_can_hit_bombchu_switches(state, player):
        comp.append(ph_time_b8_2c(state, player) + 70),
    if ph_totok_phantom_steal_object(state, player):
        comp.append(ph_time_b9_1c(state, player) + 25)
    return min(comp)


def ph_time_b10(state, player):
    return min([
        ph_time_b9_2c(state, player) + 35,
        ph_time_b9_1c(state, player) + 50 if ph_totok_phantom_steal_object(state, player) else 6000
    ])


def ph_time_b11(state, player):
    time = 25 if ph_has_chus(state, player) else 40
    return ph_time_b10(state, player) + time


def ph_time_b12(state, player):
    if ph_has_shovel(state, player):
        return ph_time_b11(state, player) + 55
    return 6000


def ph_time_b12_h(state, player):
    if ph_has_hammer(state, player):
        return ph_time_b11(state, player) + 2
    return 6000


def ph_time_b13(state, player):
    return min(
        ph_time_b12(state, player) + 60,
        ph_time_b12_h(state, player) + 50,
    )


floor_lookup = {0: ph_time_1f,
                1: ph_time_b1,
                2: ph_time_b2,
                3: ph_time_b3,
                4: ph_time_b4,
                5: ph_time_b5,
                6: ph_time_b6,
                7: ph_time_b7,
                8: ph_time_b8,
                9: ph_time_b9,
                '7_g': ph_time_b7_g,
                '7_e': ph_time_b7_e,
                '8_1c': ph_time_b8_1c,
                '8_2c': ph_time_b8_2c,
                '9_1c': ph_time_b9_1c,
                '9_2c': ph_time_b9_2c,
                10: ph_time_b10,
                11: ph_time_b11,
                12: ph_time_b12,
                '12_h': ph_time_b12_h,
                13: ph_time_b13}


def ph_totok_has_floor_time(state, player, room, time=0):
    floor_time = floor_lookup[room](state, player)
    # print(f"Floor time {room} {time}")
    if floor_time >= 6000:
        return False
    room = 7 if type(room) is str else room
    return ph_has_time(state, player, floor_lookup[room](state, player) + time, room)


# Totok Floor logic

def ph_totok_1f(state, player):
    return ph_totok_has_floor_time(state, player, 0)


def ph_totok_1f_chest(state, player):
    return ph_totok_has_floor_time(state, player, 0, 5)


def ph_totok_1f_chart(state, player):
    return all([
        ph_totok_has_floor_time(state, player, 0, 15),
        any([
            ph_has_small_keys(state, player, "Temple of the Ocean King", 1),
            ph_totok_b1_all_checks_ut(state, player)  # UT Bypass
        ])

    ])


# B1
def ph_totok_b1(state, player):
    return all([
        ph_totok_has_floor_time(state, player, 1),
        ph_has_spirit(state, player, "Power")
    ])


def ph_totok_b1_key(state, player):
    if ph_has_explosives(state, player) or ph_has_grapple(state, player):
        time = 15
    elif ph_has_boomerang(state, player):
        time = 25
    else:
        return False
    return ph_totok_has_floor_time(state, player, 1, time)


def ph_totok_b1_phantom(state, player):
    return any([
        all([
            ph_has_phantom_sword(state, player),
            ph_totok_has_floor_time(state, player, 1, 10)
        ]),
        all([
            ph_can_kill_phantoms(state, player),
            ph_totok_has_floor_time(state, player, 1, 30)
        ])
    ])


def ph_totok_b1_bow(state, player):
    return all([
        ph_totok_has_floor_time(state, player, 1, 12),
        ph_has_bow(state, player),
        ph_has_grapple(state, player)
    ])


# B2
def ph_totok_b2(state, player):
    return all([
        ph_totok_has_floor_time(state, player, 2),
        any([
            ph_has_small_keys(state, player, "Temple of the Ocean King", 2),
            ph_totok_b1_all_checks_ut(state, player)
        ])
    ])


def ph_totok_b2_key(state, player):
    if ph_has_explosives(state, player):
        time = 15
    elif ph_can_boomerang_return(state, player):
        time = 20
    elif ph_clever_pots(state, player):
        time = 70
    else:
        return False
    return ph_totok_has_floor_time(state, player, 2, time)


def ph_totok_b2_phantom(state, player):
    return all([
        ph_has_phantom_sword(state, player),
        any([ph_has_mid_range(state, player),
             ph_has_explosives(state, player)]),
        ph_totok_has_floor_time(state, player, 2, 20)
    ])


def ph_totok_b2_chu(state, player):
    return all([
        ph_can_hit_bombchu_switches(state, player),
        ph_totok_has_floor_time(state, player, 2, 20)
    ])


def ph_totok_b3(state, player):
    return all([
        ph_totok_has_floor_time(state, player, 3),  # Includes switch logic
        any([
            ph_has_small_keys(state, player, "Temple of the Ocean King", 3),
            ph_totok_b2_all_checks_ut(state, player)
        ])

    ])


def ph_totok_b3_nw(state, player):
    return ph_totok_has_floor_time(state, player, 3, 5)


def ph_totok_b3_sw(state, player):
    return ph_totok_has_floor_time(state, player, 3, 10)


def ph_totok_b3_se(state, player):
    return all([
        ph_totok_has_floor_time(state, player, 3, 7),
        any([
            ph_has_small_keys(state, player, "Temple of the Ocean King", 4),
            ph_totok_b4_all_checks_ut(state, player)
        ])
    ])


def ph_totok_b3_bow(state, player):
    if ph_has_bow(state, player):
        if ph_has_shovel(state, player):
            time = 20
        else:
            time = 25
        return ph_totok_has_floor_time(state, player, 3, time)
    return False


def ph_totok_b3_key(state, player):
    return all([
        ph_totok_has_floor_time(state, player, 3, 5),
        ph_totok_phantom_steal_object(state, player)])


def ph_totok_b3_phantom(state, player):
    if ph_has_grapple(state, player):
        if ph_has_phantom_sword(state, player):
            if ph_has_shovel(state, player):
                time = 15
            else:
                time = 20
        elif ph_can_kill_phantoms_traps(state, player):
            time = 35
        else:
            return False
        return ph_totok_has_floor_time(state, player, 3, time)
    return False


def ph_totok_b35(state, player):
    return ph_totok_has_floor_time(state, player, 4)


def ph_totok_b4(state, player):
    return all([
        ph_totok_has_floor_time(state, player, 4),
        ph_has_spirit(state, player, "Wisdom")
    ])


def ph_totok_b4_key(state, player):
    time = 0
    if ph_can_boomerang_return(state, player):
        time = 6
    elif ph_can_hit_bombchu_switches(state, player):
        if ph_has_bow(state, player):
            time = 12
        elif ph_has_mid_range_pots(state, player):
            time = 20
    elif ph_has_bombs(state, player):
        if ph_has_bow(state, player):
            time = 20
        elif ph_has_mid_range_pots(state, player):
            time = 40
    if not time:
        return False
    return ph_totok_has_floor_time(state, player, 4, time)


def ph_totok_b4_eyes(state, player):
    time = 0
    if ph_can_kill_phantom_eyes(state, player):
        if ph_has_bow(state, player):
            time = 25
        elif ph_has_mid_range_pots(state, player):
            time = 40
    if not time:
        return False
    return ph_totok_has_floor_time(state, player, 4, time)


def ph_totok_b4_phantom(state, player):
    time = 0
    if ph_has_phantom_sword(state, player):
        if ph_has_bow(state, player):
            time = 15
        elif ph_has_mid_range_pots(state, player):
            time = 25
    if not time:
        return False
    return ph_totok_has_floor_time(state, player, 4, time)


def ph_totok_b5(state, player):
    return all([
        ph_totok_has_floor_time(state, player, 5),
        any([
            ph_totok_b4_all_checks_ut(state, player),
            ph_has_small_keys(state, player, "Temple of the Ocean King", 5),
            all([
                ph_has_grapple(state, player),
                ph_has_small_keys(state, player, "Temple of the Ocean King", 4)
            ])
        ])
    ])


def ph_totok_b5_alt(state, player):
    return all([
        ph_totok_has_floor_time(state, player, 5),
        ph_can_hit_bombchu_switches(state, player),
        ph_has_small_keys(state, player, "Temple of the Ocean King", 5)
    ])


def ph_totok_b5_chest(state, player):
    return all([
        ph_can_kill_bubble(state, player),
        any([
            ph_has_mid_range_pots(state, player),
            ph_clever_bombs(state, player)
        ]),
        ph_totok_has_floor_time(state, player, 5, 25)
    ])


def ph_totok_b5_alt_chest(state, player):
    return all([
        any([
            ph_has_shovel(state, player),
            ph_has_grapple(state, player)
        ]),
        ph_totok_has_floor_time(state, player, 5, 7),
    ])


def ph_totok_b6(state, player):
    return ph_totok_has_floor_time(state, player, 6)


def ph_totok_b6_bow(state, player):
    return all([
        ph_has_bow(state, player),
        ph_totok_has_floor_time(state, player, 6, 10)
    ])


def ph_totok_b6_phantom(state, player):
    return all([
        ph_has_phantom_sword(state, player),
        ph_totok_has_floor_time(state, player, 6, 15)
    ])


def ph_totok_b6_crest(state, player):
    return all([
        ph_has_sea_chart(state, player, "SW"),
        ph_totok_has_floor_time(state, player, 6, 10)
    ])


def ph_totok_b7(state, player):
    return all([
        ph_has_triforce_crest(state, player),
        ph_totok_has_floor_time(state, player, 7)
    ])


def ph_totok_b7_crystal(state, player):
    return any([
        all([
            ph_has_grapple(state, player),
            ph_totok_has_floor_time(state, player, '7_g')
        ]),
        all([
            ph_can_hit_switches(state, player),
            ph_totok_has_floor_time(state, player, '7_e', 15)
        ])
    ])


def ph_totok_b7_switch_chest(state, player):
    return all([
        ph_has_range(state, player),
        any([
            ph_totok_has_floor_time(state, player, '7_g', 15),
            ph_totok_has_floor_time(state, player, '7_e', 30)
        ])
    ])


def ph_totok_b8(state, player):
    return ph_totok_has_floor_time(state, player, 8)


def ph_totok_b8_phantom(state, player):
    return any([
        all([
            ph_has_phantom_sword(state, player),
            ph_totok_has_floor_time(state, player, 8, 25)
        ]),
        all([
            ph_can_kill_phantoms(state, player),
            ph_totok_has_floor_time(state, player, 8, 45)
        ])
    ])


def ph_totok_b9(state, player):
    return any([
        all([
            ph_can_hit_bombchu_switches(state, player),
            ph_totok_has_floor_time(state, player, '9_1c')
        ]),
        all([
            ph_has_explosives(state, player),
            any([
                ph_has_shape_crystal(state, player, "Temple of the Ocean King", "Triangle"),
                ph_is_ut(state, player)
            ])
        ])
    ])


def ph_totok_b7_phantom(state, player):
    return any([
        all([
            ph_has_phantom_sword(state, player),
            ph_totok_has_floor_time(state, player, '7_e', 20)

        ]),
        all([
            ph_can_kill_phantoms(state, player),
            ph_totok_has_floor_time(state, player, '7_e', 70)
        ])
    ])


def ph_totok_b9_phantom(state, player):
    room = 9 if ph_can_hit_bombchu_switches(state, player) else '9_1c'
    return any([
        all([
            ph_has_phantom_sword(state, player),
            ph_totok_has_floor_time(state, player, room, 12)
        ]),
        all([
            ph_can_kill_phantoms_traps(state, player),
            ph_has_hammer(state, player),
            ph_totok_has_floor_time(state, player, room, 17)
        ]),
        all([
            ph_can_kill_phantoms_traps(state, player),
            ph_has_bow(state, player),
            ph_has_boomerang(state, player),
            ph_totok_has_floor_time(state, player, room, 20)
        ]),
    ])


def ph_totok_b9_ghosts(state, player):
    room = 9 if ph_can_hit_bombchu_switches(state, player) else '9_1c'
    return ph_totok_has_floor_time(state, player, room, 30)


def ph_totok_b9_corner_chest(state, player):
    # print(f"corner 8_2c {ph_time_b8_2c(state, player)} "
    #      f"9_2c {ph_time_b9_2c(state, player)} "
    #      f"9 {ph_time_b9(state, player) + 25}")
    return any([
        all([
            ph_totok_has_floor_time(state, player, '8_2c'),
            any([
                ph_has_shape_crystal(state, player, "Temple of the Ocean King", "Round"),
                ph_is_ut(state, player)
            ])
        ]),
        all([
            any([
                ph_totok_has_floor_time(state, player, 9, 25),
                ph_totok_has_floor_time(state, player, '9_2c'),
            ]),
            ph_totok_phantom_steal_object(state, player)
        ])
    ])


def ph_totok_b8_2_crystal_chest(state, player):
    return all([
        ph_has_explosives(state, player),
        ph_totok_has_floor_time(state, player, '8_2c', 30),
        any([
            ph_is_ut(state, player),
            all([
                ph_has_shape_crystal(state, player, "Temple of the Ocean King", "Round"),
                ph_has_shape_crystal(state, player, "Temple of the Ocean King", "Triangle"),
            ])
        ])
    ])


def ph_totok_b10(state, player):
    return all([
        ph_totok_has_floor_time(state, player, 10),
        any([
            ph_is_ut(state, player),
            all([
                ph_has_shape_crystal(state, player, "Temple of the Ocean King", "Round"),
                ph_has_shape_crystal(state, player, "Temple of the Ocean King", "Triangle"),
            ])
        ])
    ])


def ph_totok_b10_key(state, player):
    return all([
        ph_totok_has_floor_time(state, player, 10, 10),
        ph_totok_phantom_steal_object(state, player)
    ])


def ph_totok_b10_phantom(state, player):
    time = 15
    if ph_has_phantom_sword(state, player):
        time += 15
    elif ph_can_kill_phantoms_traps(state, player):
        time += 30
    else:
        return False
    return all([
        ph_has_explosives(state, player),
        ph_totok_has_floor_time(state, player, 10, time)
    ])


def ph_totok_b10_eye(state, player):
    if ph_has_explosives(state, player) and ph_has_grapple(state, player):
        if ph_has_chus(state, player):
            return ph_totok_has_floor_time(state, player, 10, 40)
        return ph_totok_has_floor_time(state, player, 10, 45)
    return False


def ph_totok_b10_hammer(state, player):
    if ph_has_explosives(state, player) and ph_has_hammer(state, player):
        if ph_has_chus(state, player):
            return ph_totok_has_floor_time(state, player, 10, 20)
        return ph_totok_has_floor_time(state, player, 10, 35)


def ph_totok_b11(state, player):
    return all([
        ph_has_explosives(state, player),
        ph_totok_has_floor_time(state, player, 11),
        any([
            all([
                ph_is_ut(state, player),
                ph_totok_b10_all_checks_ut(state, player)  # Assume that time is enough
            ]),
            ph_has_small_keys(state, player, "Temple of the Ocean King", 6),
            all([
                ph_has_small_keys(state, player, "Temple of the Ocean King", 5),
                ph_has_grapple(state, player)
            ])
        ])
    ])


def ph_totok_b11_phantom(state, player):
    return all([
        ph_has_phantom_sword(state, player),
        ph_totok_has_floor_time(state, player, 11, 10)
    ])


def ph_totok_b11_eyes(state, player):
    return ph_totok_has_floor_time(state, player, 11, 25)


def ph_totok_b12(state, player):
    return any([
        ph_totok_has_floor_time(state, player, 12),
        ph_totok_has_floor_time(state, player, '12_h')
    ])


def ph_totok_b12_nw(state, player):
    return any([
        ph_totok_has_floor_time(state, player, 12, 12),
        ph_totok_has_floor_time(state, player, '12_h', 15)
    ])


def ph_totok_b12_ne(state, player):
    return any([
        ph_totok_has_floor_time(state, player, 12, 35),
        ph_totok_has_floor_time(state, player, '12_h', 15)
    ])


def ph_totok_b12_phantom(state, player):
    return all([
        ph_has_phantom_sword(state, player),
        any([
            ph_totok_has_floor_time(state, player, 12, 55),
            ph_totok_has_floor_time(state, player, '12_h', 40)
        ])
    ])


def ph_totok_b12_ghost(state, player):
    return any([
        ph_totok_has_floor_time(state, player, 12, 70),
        ph_totok_has_floor_time(state, player, '12_h', 50)
    ])


def ph_totok_b12_hammer(state, player):
    return ph_totok_has_floor_time(state, player, '12_h', 10)


def ph_totok_b13(state, player):
    return all([
        ph_totok_has_floor_time(state, player, 13),
        any([
            all([
                ph_has_force_gems(state, player, 12, 2),
                ph_totok_phantom_steal_object(state, player)  # Redundant since bombs are needed to get here
            ]),
            ph_is_ut(state, player)
        ])
    ])


def ph_totok_b13_chest(state, player):
    return ph_totok_has_floor_time(state, player, 13, 5)
