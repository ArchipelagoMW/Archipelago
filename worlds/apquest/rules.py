from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule

from .options import HardMode

if TYPE_CHECKING:
    from .world import APQuestWorld


def set_all_rules(world: APQuestWorld) -> None:
    # In order for AP to generate an item layout that is actually possible for the player to complete,
    # we need to define rules for our Entrances and Locations.
    # Note: Regions do not have rules, the Entrances connecting them do!
    # We'll do entrances first, then locations, and then finally we set our victory condition.

    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: APQuestWorld) -> None:
    # First, we need to actually grab our entrances. Luckily, there is a helper method for this.
    overworld_to_bottom_right_room = world.get_entrance("Overworld to Bottom Right Room")
    overworld_to_top_left_room = world.get_entrance("Overworld to Top Left Room")
    right_room_to_final_boss_room = world.get_entrance("Right Room to Final Boss Room")

    # Now, let's make some rules!
    # First, let's handle the transition from the overworld to the bottom right room,
    # which requires slashing a bush with the Sword.
    # For this, we need a rule that says "player has a Sword".
    # We can use a "Has"-type rule from the rule_builder module for this.
    can_destroy_bush = Has("Sword")

    # Now we can set our "can_destroy_bush" rule to the entrance which requires slashing a bush to clear the path.
    # The easiest way to do this is by calling world.set_rule, which works for both Locations and Entrances.
    world.set_rule(overworld_to_bottom_right_room, can_destroy_bush)

    # Conditions can also depend on event items.
    button_pressed = Has("Top Left Room Button Pressed")
    world.set_rule(right_room_to_final_boss_room, button_pressed)

    # Some entrance rules may only apply if the player enabled certain options.
    # In our case, if the hammer option is enabled, we need to add the Hammer requirement to the Entrance from
    # Overworld to the Top Middle Room.
    if world.options.hammer:
        overworld_to_top_middle_room = world.get_entrance("Overworld to Top Middle Room")
        can_smash_brick = Has("Hammer")
        world.set_rule(overworld_to_top_middle_room, can_smash_brick)

    # So far, we've been using "Has" from the Rule Builder to make our rules.
    # There is another way to make rules that you will see in a lot of older worlds.
    # A rule can just be  a function that takes a "state" argument and returns a bool.
    # As a demonstration of what that looks like, let's do it with our final Entrance rule:
    world.set_rule(overworld_to_top_left_room, lambda state: state.has("Key", world.player))
    # This style is not really recommended anymore, though.
    # Using Rule Builder allows the core AP code to do a lot of under-the-hood optimizations.
    # Rule Builder is quite comprehensive, and even if you have really esoteric rules,
    # you can make custom rules by subclassing CustomRule.
    # Since Rule Builder is preferred, we'll re-set this rule to also use "Has" from the Rule Builder.
    world.set_rule(overworld_to_top_left_room, Has("Key"))


def set_all_location_rules(world: APQuestWorld) -> None:
    # Location rules work no differently from Entrance rules.
    # Most of our locations are chests that can simply be opened by walking up to them.
    # Thus, their logical requirements are covered by the Entrance rules of the Entrances that were required to
    # reach the region that the chest sits in.
    # However, our two enemies work differently.
    # Entering the room with the enemy is not enough, you also need to have enough combat items to be able to defeat it.
    # So, we need to set requirements on the Locations themselves.
    # Since combat is a bit more complicated, we'll use this chance to cover some advanced access rule concepts.

    # In "set_all_entrance_rules", we had a rule for a location that doesn't always exist.
    # In this case, we had to check for its existence (by checking the player's chosen options) before setting the rule.
    # Other times, you may have a situation where a location can have two different rules depending on the options.
    # In our case, the enemy in the right room has more health if hard mode is selected,
    # so ontop of the Sword, the player will either need one more health or a Shield in hard mode.
    # First, let's make our sword condition.
    can_defeat_basic_enemy: Rule = Has("Sword")

    # Next, we'll check whether hard mode has been chosen in the player options.
    if world.options.hard_mode:
        # We'll make the condition for "Has a Shield or a Health Upgrade".
        # We can chain two "Has" conditions together with the | operator to make "Has Shield or has Health Upgrade".
        can_withstand_a_hit = Has("Shield") | Has("Health Upgrade")

        # Now, we chain this rule to our Sword rule.
        # Since we want both conditions to be true, in this case, we have to chain them in an "and" way.
        # For this, we can use the & operator.
        can_defeat_basic_enemy = can_defeat_basic_enemy & can_withstand_a_hit

    # Finally, we set our rule onto the Right Room Eney Drop location.
    right_room_enemy = world.get_location("Right Room Enemy Drop")
    world.set_rule(right_room_enemy, can_defeat_basic_enemy)

    # For the final boss, we also need to chain multiple conditions.
    # First of all, you always need a Sword and a Shield.
    # So far, we used the | and & operators to chain "Has" rules.
    # Instead, we can also use HasAny for an or-chain of items, or HasAll for an and-chain of items.
    has_sword_and_shield: Rule = HasAll("Sword", "Shield")

    # In hard mode, the player also needs both Health Upgrades to survive long enough to defeat the boss.
    # For this, we can use the optional "count" parameter for "Has".
    has_both_health_upgrades = Has("Health Upgrade", count=2)

    # Previously, we used an "if world.options.hard_mode" condition to check if we should apply the extra requirement.
    # However, if you're comfortable with boolean logic, there is another way.
    # OptionFilter is a rule which just resolves to True if the option has the specified value, or False otherwise.
    hard_mode_is_off = OptionFilter(HardMode, False)

    # Now we can combine our rule as follows.
    can_defeat_final_boss = has_sword_and_shield & (hard_mode_is_off | has_both_health_upgrades)
    # If you're not as comfortable with boolean logic, it might be somewhat confusing why this is correct.
    # There is nothing wrong with using "if" conditions to check for options, if you find that easier to understand.

    # Finally, we apply the rule to our "Final Boss Defeated" event location.
    final_boss = world.get_location("Final Boss Defeated")
    world.set_rule(final_boss, can_defeat_final_boss)


def set_completion_condition(world: APQuestWorld) -> None:
    # Finally, we need to set a completion condition for our world, defining what the player needs to win the game.
    # For this, we can use world.set_completion_rule.
    # You can just set a completion condition directly like any other condition, referencing items the player receives:
    world.set_completion_rule(HasAll("Sword", "Shield"))

    # In our case, we went for the Victory event design pattern (see create_events() in locations.py).
    # So lets undo what we just did, and instead set the completion condition to:
    world.set_completion_rule(Has("Victory"))


# One final comment about rules:
# If your world exclusively uses Rule Builder rules (like APQuest), it's worth trying CachedRuleBuilderWorld.
# CachedRuleBuilderWorld is a subclass of World that has a bunch of caching magic to make rules faster.
# Just have your world class subclass CachedRuleBuilderWorld instead of World:
#   class APQuestWorld(CachedRuleBuilderWorld): ...
# This may speed up your world, or it may make it slower.
# The exact factors are complex and not well understood, but there is no harm in trying it.
# Generate a few seeds and see if there is a noticable difference!
# If you're wondering, author has checked: APQuest is too simple to see any benefits, so we'll stick with "World".
