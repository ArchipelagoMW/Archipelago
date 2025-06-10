from BaseClasses import CollectionState
from Options import Accessibility
from .Constants import *


# =========== Item States =============

def ph_has_sword(state: CollectionState, player: int):
    return state.has("Sword", player)


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


def ph_has_explosives(state: CollectionState, player: int):
    return state.has_any(["Bombs (Progressive)", "Bombchus (Progressive)"], player)


def ph_has_damage(state: CollectionState, player: int):
    return any([
        state.has("Sword", player),
        ph_has_explosives(state, player),
        state.has("Bow (Progressive)", player),
        state.has("Grappling Hook", player),
        state.has("Hammer", player)
    ])


def ph_has_range(state: CollectionState, player: int):
    return state.has_any(["Boomerang", "Bow (Progressive)", "Grappling Hook"], player)


def ph_has_sw_sea_chart(state: CollectionState, player: int):
    return state.has("SW Sea Chart", player)


# ================ Rupee States ==================
def ph_has_rupees(state: CollectionState, player: int, cost: int):
    # TODO code rupee logic
    return True


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

def ph_option_keysanity(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.keysanity == "anywhere"


# ============= Key logic ==============

def ph_has_small_keys(state: CollectionState, player: int, dung_name: str, amount: int = 1):
    return state.has(f"Small Key ({dung_name})", player, amount)


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


