from typing import TYPE_CHECKING

from BaseClasses import CollectionState

from ..generic.Rules import add_rule, set_rule

if TYPE_CHECKING:
    from .world import APQuestWorld


def set_all_rules(world: "APQuestWorld") -> None:
    # In order for AP to be able to randomize into an item layout that is actually possible to complete,
    # We need to define rules for our Entrances and Locations.
    # Note: Regions do not have rules, the Entrances connecting them do!
    # We'll do entrances first, then locations, and then finally we set our victory condition.

    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_victory_condition(world)


def set_all_entrance_rules(world: "APQuestWorld") -> None:
    # First, we need to actually grab our entrances. Luckily, there is a helper method for this.
    overworld_to_bottom_right_room = world.get_entrance("Overworld to Bottom Right Room")
    overworld_to_top_left_room = world.get_entrance("Overworld to Top Left Room")
    right_room_to_final_boss_room = world.get_entrance("Right Room to Final Boss Room")

    # An access rule is a function. We can define this function like any other function.
    # This function must accept exactly one parameter: A "CollectionState".
    # A CollectionState describes the current progress of the players in the multiworld, i.e. what items they have,
    # which regions they've reached, etc.
    # In an access rule, we can ask whether the player has a collected a certain item.
    # We can do this via the state.has(...) function.
    # This function takes an item name, a player number, and an optional count parameter (more on that below)
    # Since a rule only takes a CollectionState parameter, but we also need the player number in the state.has call,
    # our function needs to be locally defined so that it has access to the player number from the outer scope.
    # In our case, we are inside a function that has access to the "world" parameter, so we can use world.player.
    def can_destroy_bush(state: CollectionState) -> bool:
        return state.has("Sword", world.player)

    # Now we can set our "can_destroy_bush" rule to our entrance which requires slashing a bush to clear the path.
    # One way to set rules is via the set_rule() function, which works on both Entrances and Locations.
    set_rule(overworld_to_bottom_right_room, can_destroy_bush)

    # Because the function has to be defined locally, most worlds prefer the lambda syntax.
    set_rule(overworld_to_top_left_room, lambda state: state.has("Key", world.player))

    # Conditions can depend on events items.
    set_rule(right_room_to_final_boss_room, lambda state: state.has("Top Left Room Button Pressed", world.player))


def set_all_location_rules(world: "APQuestWorld") -> None:
    # Location rules work no differently from Entrance rules.
    # Most of our locations are chests that can simply be opened by walking up to them.
    # Thus, their logical requirements are covered by the Entrance rules of the Entrances that were required to
    # reach the region that the chest sits in.
    # However, our two enemies work differently.
    # Entering the room with the enemy is not enough, you also need to have enough combat items to be able to defeat it.
    # So, we need to set requirements on the Locations themselves.
    # Since combat is a bit more complicated, we'll use this chance to cover some advanced access rule concepts.

    # Sometimes, you may want to have different rules depending on the player's chosen options.
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

    # Another way to chain multiple conditions is via the add_rule function.
    # This is generally somewhat slow though, so it should only be used if your structure justifies it.
    # In our case, it's pretty useful because hard mode and easy mode have different requirements.
    final_boss = world.get_location("Final Boss Defeated")
    add_rule(final_boss, lambda state: state.has("Sword", world.player))
    add_rule(final_boss, lambda state: state.has("Shield", world.player))

    if world.options.hard_mode:
        # You can check for multiple copies of an item by using the optional count parameter of state.has().
        add_rule(final_boss, lambda state: state.has("Health Upgrade", world.player, 2))


def set_victory_condition(world: "APQuestWorld") -> None:
    # Finally, we need to set a victory condition.
    # You can just set a victory condition directly like any other condition, referencing items the player receives:
    world.multiworld.completion_condition[world.player] = lambda state: state.has_all(("Sword", "Shield"), world.player)

    # In our case, we went for the Victory event design pattern (see regions.py).
    # So lets undo what we just did, and instead set the victory condition to:
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)
