from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule
from .strings.item_names import Item

if TYPE_CHECKING:
    from .world import PSOWorld


def set_all_rules(world: PSOWorld) -> None:
    # In order for AP to generate an item layout that is actually possible for the player to complete,
    # we need to define rules for our Entrances and Locations.
    # Note: Regions do not have rules, the Entrances connecting them do!
    # We'll do entrances first, then locations, and then finally we set our victory condition.

    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: PSOWorld) -> None:
    # We assigned all the relevant entrance rules to our current batch of entrances in regions.py
    # We might need to add some additional rules later, especially if we get more granular with
    # things like switches, but for now, we'll just return
    return


def set_all_location_rules(world: PSOWorld) -> None:

    def set_rule_if_exists(location_name: str, rule: Callable[[CollectionState], bool]) -> None:
        if location_name in world.progress_locations:
            set_rule(world.get_location(location_name), rule)

    player = world.player

    forest_locations = ["Red Ring Rico Message 1", "Enter Forest 1", "Defeat Dragon", "Unlock Caves"]
    caves_locations = ["Scientist 1 - After Dragon", "Defeat De Rol Le", "Unlock Mines"]
    mines_locations = ["Mines 2 Pillar", "Defeat Vol Opt"]
    ruins_locations = ["Unlock Ruins", "Defeat Dark Falz"]

    for location in forest_locations:
        set_rule_if_exists(location, lambda state: state.has(Item.UNLOCK_FOREST_1, player))

    for location in caves_locations:
        set_rule_if_exists(location, lambda state: state.has(Item.UNLOCK_CAVES_1, player))

    for location in mines_locations:
        set_rule_if_exists(location, lambda state: state.has(Item.UNLOCK_MINES_1, player))

    for location in ruins_locations:
        set_rule_if_exists(
            location, lambda state: state.has_all([Item.FOREST_PILLAR, Item.CAVES_PILLAR, Item.MINES_PILLAR], player)
        )

def set_completion_condition(world: PSOWorld) -> None:
    # For now, we're just going to check for the Victory condition
    # We might set more complex conditions here later, or just simplify this further and handle in by
    # handing out the "Victory" item in different ways
    world.multiworld.completion_condition[world.player] = lambda state: state.has(Item.VICTORY, world.player)
