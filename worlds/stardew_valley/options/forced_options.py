import logging

import Options as ap_options
from . import options

logger = logging.getLogger(__name__)


def force_change_options_if_incompatible(world_options: options.StardewValleyOptions, player: int, player_name: str):
    goal_is_walnut_hunter = world_options.goal == options.Goal.option_greatest_walnut_hunter
    goal_is_perfection = world_options.goal == options.Goal.option_perfection
    goal_is_island_related = goal_is_walnut_hunter or goal_is_perfection
    exclude_ginger_island = world_options.exclude_ginger_island == options.ExcludeGingerIsland.option_true

    if goal_is_island_related and exclude_ginger_island:
        world_options.exclude_ginger_island.value = options.ExcludeGingerIsland.option_false
        goal_name = world_options.goal.current_key
        logger.warning(
            f"Goal '{goal_name}' requires Ginger Island. Exclude Ginger Island setting forced to 'False' for player {player} ({player_name})")

    if exclude_ginger_island and world_options.walnutsanity != options.Walnutsanity.preset_none:
        world_options.walnutsanity.value = options.Walnutsanity.preset_none
        logger.warning(
            f"Walnutsanity requires Ginger Island. Ginger Island was excluded from {player} ({player_name})'s world, so walnutsanity was force disabled")

    if goal_is_perfection and world_options.accessibility == ap_options.Accessibility.option_minimal:
        world_options.accessibility.value = ap_options.Accessibility.option_full
        logger.warning(
            f"Goal 'Perfection' requires full accessibility. Accessibility setting forced to 'Full' for player {player} ({player_name})")

    elif world_options.goal == options.Goal.option_allsanity and world_options.accessibility == ap_options.Accessibility.option_minimal:
        world_options.accessibility.value = ap_options.Accessibility.option_full
        logger.warning(
            f"Goal 'Allsanity' requires full accessibility. Accessibility setting forced to 'Full' for player {player} ({player_name})")
