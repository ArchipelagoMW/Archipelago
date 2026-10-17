from BaseClasses import ItemClassification
from rule_builder.rules import Has, HasAllCounts
from worlds.tcg_card_shop_simulator.data.rules.state_rules import hasAllPacks


def set_goal(world):

    if world.options.goal.value == world.options.goal.option_reach_max_level:
        world.set_completion_rule(Has("Victory"))

    if world.options.goal.value == world.options.goal.option_collection_builder:
        world.set_completion_rule(hasAllPacks())

    if world.options.goal.value == world.options.goal.option_grade_ghost_cards:
        world.set_completion_rule(HasAllCounts(world.ghost_item_counts))