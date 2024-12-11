import logging

import Options as ap_options
from . import options

logger = logging.getLogger(__name__)


def force_change_options_if_incompatible(world_options: options.StardewValleyOptions, player: int, player_name: str) -> None:
    force_ginger_island_inclusion_when_goal_is_ginger_island_related(world_options, player, player_name)
    force_walnutsanity_deactivation_when_ginger_island_is_excluded(world_options, player, player_name)
    force_qi_special_orders_deactivation_when_ginger_island_is_excluded(world_options, player, player_name)
    force_accessibility_to_full_when_goal_requires_all_locations(player, player_name, world_options)


def force_ginger_island_inclusion_when_goal_is_ginger_island_related(world_options: options.StardewValleyOptions, player: int, player_name: str) -> None:
    goal_is_walnut_hunter = world_options.goal == options.Goal.option_greatest_walnut_hunter
    goal_is_perfection = world_options.goal == options.Goal.option_perfection
    goal_is_island_related = goal_is_walnut_hunter or goal_is_perfection
    ginger_island_is_excluded = world_options.exclude_ginger_island == options.ExcludeGingerIsland.option_true

    if goal_is_island_related and ginger_island_is_excluded:
        world_options.exclude_ginger_island.value = options.ExcludeGingerIsland.option_false
        goal_name = world_options.goal.current_option_name
        logger.warning(f"Goal '{goal_name}' requires Ginger Island. "
                       f"Exclude Ginger Island option forced to 'False' for player {player} ({player_name})")


def force_walnutsanity_deactivation_when_ginger_island_is_excluded(world_options: options.StardewValleyOptions, player: int, player_name: str):
    ginger_island_is_excluded = world_options.exclude_ginger_island == options.ExcludeGingerIsland.option_true
    walnutsanity_is_active = world_options.walnutsanity != options.Walnutsanity.preset_none

    if ginger_island_is_excluded and walnutsanity_is_active:
        world_options.walnutsanity.value = options.Walnutsanity.preset_none
        logger.warning(f"Walnutsanity requires Ginger Island. "
                       f"Ginger Island was excluded from {player} ({player_name})'s world, so walnutsanity was force disabled")


def force_qi_special_orders_deactivation_when_ginger_island_is_excluded(world_options: options.StardewValleyOptions, player: int, player_name: str):
    ginger_island_is_excluded = world_options.exclude_ginger_island == options.ExcludeGingerIsland.option_true
    qi_board_is_active = world_options.special_order_locations.value & options.SpecialOrderLocations.value_qi

    if ginger_island_is_excluded and qi_board_is_active:
        original_option_name = world_options.special_order_locations.current_option_name
        world_options.special_order_locations.value -= options.SpecialOrderLocations.value_qi
        logger.warning(f"Mr. Qi's Special Orders requires Ginger Island. "
                       f"Ginger Island was excluded from {player} ({player_name})'s world, so Special Order Locations was changed from {original_option_name} to {world_options.special_order_locations.current_option_name}")


def force_accessibility_to_full_when_goal_requires_all_locations(player, player_name, world_options):
    goal_is_allsanity = world_options.goal == options.Goal.option_allsanity
    goal_is_perfection = world_options.goal == options.Goal.option_perfection
    goal_requires_all_locations = goal_is_allsanity or goal_is_perfection
    accessibility_is_minimal = world_options.accessibility == ap_options.Accessibility.option_minimal

    if goal_requires_all_locations and accessibility_is_minimal:
        world_options.accessibility.value = ap_options.Accessibility.option_full
        goal_name = world_options.goal.current_option_name
        logger.warning(f"Goal '{goal_name}' requires full accessibility. "
                       f"Accessibility option forced to 'Full' for player {player} ({player_name})")
