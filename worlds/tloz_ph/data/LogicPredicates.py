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


def ph_has_sw_sea_chart(state: CollectionState, player: int):
    return state.has("SW Sea Chart", player)


def ph_has_se_sea_chart(state: CollectionState, player: int):
    return state.has("SE Sea Chart", player)


def ph_has_courage_crest(state, player):
    return state.has("Courage Crest", player)


def ph_has_cannon(state, player):
    return state.has("Cannon", player)


def ph_has_salvage(state, player):
    return state.has("Salvage Arm", player)


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
    return any([ph_has_range(state, player),
                ph_clever_bombs(state, player),
                ph_has_hammer(state, player),
                ph_has_beam_sword(state, player)])


def ph_has_mid_range(state: CollectionState, player: int):
    return any([ph_has_range(state, player),
                ph_has_hammer(state, player),
                ph_has_beam_sword(state, player),
                ph_option_clever_pots(state, player)])


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
    # TODO code rupee logic
    return state.has("Pre-Alpha Rupee (5000)", player)


def ph_can_buy_quiver(state: CollectionState, player: int):
    return all([ph_has_bow(state, player), ph_has_rupees(state, player, 1500)])


def ph_can_buy_chu_bag(state: CollectionState, player: int):
    return all([ph_has_chus(state, player), ph_has_bow(state, player), ph_has_rupees(state, player, 2500)])


def ph_can_buy_heart(state: CollectionState, player: int):
    return all([ph_has_chus(state, player), ph_has_bow(state, player), ph_has_rupees(state, player, 4500)])


# ============ Option states =============

def ph_option_glitched_logic(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.logic == "glitched"


def ph_option_normal_logic(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.logic == "normal"


def ph_option_med_logic(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.logic in ["medium", "glitched"]


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


def ph_option_clever_pots(state: CollectionState, player: int):
    return ph_option_med_logic(state, player)


def ph_clever_bombs(state: CollectionState, player: int):
    return all([ph_has_bombs(state, player),
                ph_option_med_logic(state, player)])


# ============= Key logic ==============

def ph_has_small_keys(state: CollectionState, player: int, dung_name: str, amount: int = 1):
    return state.has(f"Small Key ({dung_name})", player, amount)


def ph_has_boss_key(state: CollectionState, player: int, dung_name: str):
    return state.has(f"Boss Key ({dung_name})", player)


def ph_has_force_gems(state, player, floor=3):
    # TODO: Differentiate between B3 and B12
    return state.has(f"Force Gem (B{floor})", player, 3)

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


def ph_totok_b6(state: CollectionState, player: int):
    return all([
        ph_totok_b5_key_logic(state, player),
        any([
            ph_can_hit_bombchu_switches(state, player),
            all([
                ph_can_kill_bubble(state, player),
                ph_has_mid_range(state, player)
            ])
        ])
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
        ph_option_clever_pots(state, player),
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


def ph_totok_b5_key_logic(state: CollectionState, player: int):
    # TODO: Does not take into account force gem shuffling
    return any([
        all([ph_has_small_keys(state, player, "Temple of the Ocean King", 4), ph_has_grapple(state, player)]),
        ph_has_small_keys(state, player, "Temple of the Ocean King", 5),
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
        ph_has_cannon(state, player)
    ])


def ph_temp_goal(state, player):
    return all([ph_has_sw_sea_chart(state, player),
                ph_has_phantom_sword(state, player),
                ph_has_courage_crest(state, player)])
