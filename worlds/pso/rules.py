from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule

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
    # TODO: Fill this in with real things once we actually have items
    right_room_enemy = world.get_location("Right Room Enemy Drop")

    if world.options.hard_mode:
        # If you have multiple conditions, you can obviously chain them via "or" or "and".
        # However, there are also the nice helper functions "state.has_any" and "state.has_all".
        set_rule(
            right_room_enemy,
            lambda state: (
                state.has("Sword", world.player) and state.has_any(("Shield", "Health Upgrade"), world.player)
            ),
        )
    else:
        set_rule(right_room_enemy, lambda state: state.has("Sword", world.player))

def set_completion_condition(world: PSOWorld) -> None:
    # For now, we're just going to check for the Victory condition
    # We might set more complex conditions here later, or just simplify this further and handle in by
    # handing out the "Victory" item in different ways
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)
