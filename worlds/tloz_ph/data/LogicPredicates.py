from BaseClasses import CollectionState
from Options import Accessibility
from .Constants import *


def ph_has_sword(state: CollectionState, player: int):
    return state.has("Sword", player)


def ph_has_shovel(state: CollectionState, player: int):
    return state.has("Shovel", player)


def ph_has_bow(state: CollectionState, player: int):
    return state.has("Bow", player)


def ph_has_bombs(state: CollectionState, player: int):
    return state.has("Bombs", player)


def ph_has_chus(state: CollectionState, player: int):
    return state.has("Bombchus", player)


def ph_has_grapple(state: CollectionState, player: int):
    return state.has("Grappling Hook", player)


def ph_has_hammer(state: CollectionState, player: int):
    return state.has("Hammer", player)


def ph_has_boomerang(state: CollectionState, player: int):
    return state.has("Boomerang", player)


def ph_has_explosives(state: CollectionState, player: int):
    return any([
        state.has("Bombs", player),
        state.has("Bombchus", player)
    ])


def ph_has_damage(state: CollectionState, player: int):
    return any([
        state.has("Sword", player),
        ph_has_explosives(state, player),
        state.has("Bow", player),
        state.has("Grappling Hook", player),
        state.has("Hammer", player)
    ])


def ph_has_range(state: CollectionState, player: int):
    return any([
        state.has("Boomerang", player),
        state.has("Bow", player),
        state.has("Grappling Hook", player)
    ])


def ph_has_sw_sea_chart(state: CollectionState, player: int):
    return state.has("SW Sea Chart", player)


