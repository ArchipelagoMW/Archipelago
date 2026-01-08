from random import Random
from typing import Iterator, List, Tuple

from BaseClasses import CollectionState
from .item import name_to_id as item_name_to_id, id_to_sv_item

from subversion_rando.connection_data import area_doors
from subversion_rando.game import Game
from subversion_rando.item_data import Items
from subversion_rando.loadout import Loadout
from subversion_rando.logic_updater import update_area_logic
from subversion_rando.trick_data import Tricks

_excluded_after_torpedo_bay = {
    "Missile": ["Gantry", "Weapon Locker"],
    "Super Missile": ["Gantry", "Weapon Locker", "Ready Room"],
    "Morph Ball": ["Aft Battery"],
    "Grapple Beam": ["Docking Port 3", "Docking Port 4"],
}

_casual_area = {
    Items.Missile: 1,
}

_casual_early = {
    Items.Missile: 12,
    Items.Morph: 6,
    Items.Super: 1,
}

_casual_extra = {
    Items.Wave: 1,
}

_expert_area = {
    Items.Missile: 6,
    Items.GravityBoots: 3,
}

_expert_early = {
    Items.Missile: 10,
    Items.GravityBoots: 5,
    Items.Morph: 3,
    Items.Super: 1,
    Items.Bombs: 2,
    Items.PowerBomb: 1,
}


def choose_torpedo_bay(sv_game: Game, auto_hints: bool, rand: Random) -> Tuple[str, List[str]]:
    """
    The beginning logic is very restrictive,
    so we place the first item in the first location manually before the fill algorithm.

    This function returns the name of the item to place,
    and the names of the locations that will be excluded from progression with this placement.
    """
    if Tricks.wave_gate_glitch in sv_game.options.logic:  # not casual logic
        if sv_game.options.area_rando:
            dist = _expert_area.copy()
        else:
            dist = _expert_early.copy()
            if not auto_hints:
                for _item_name, item_id in item_name_to_id.items():
                    item = id_to_sv_item[item_id]
                    if item not in dist:
                        dist[item] = 1
    else:  # casual, no gate glitch
        if sv_game.options.area_rando:
            dist = _casual_area.copy()
        else:
            dist = _casual_early.copy()
            if not auto_hints:
                dist.update(_casual_extra)
    dist_items = tuple(dist.keys())
    dist_weights = tuple(dist.values())
    item_choice = rand.choices(dist_items, dist_weights)[0].name
    excluded_locations = _excluded_after_torpedo_bay.get(item_choice, [])

    return item_choice, excluded_locations


def item_counts(cs: CollectionState, p: int) -> Iterator[Tuple[str, int]]:
    """
    the items that player p has collected

    ((item_name, count), (item_name, count), ...)
    """
    return ((item_name, cs.count(item_name, p)) for item_name in item_name_to_id)


def cs_to_loadout(sv_game: Game, collection_state: CollectionState, player: int) -> Loadout:
    """ convert Archipelago CollectionState to subversion_rando collection state """
    loadout = Loadout(sv_game)
    for item_name, count in item_counts(collection_state, player):
        loadout.contents[id_to_sv_item[item_name_to_id[item_name]]] += count
    loadout.append(Items.spaceDrop)
    loadout.append(area_doors["SunkenNestL"])
    update_area_logic(loadout)
    return loadout
