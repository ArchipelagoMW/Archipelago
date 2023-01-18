from Options import Choice, Range, DeathLink


class EpisodesToClear(Choice):
    """Sets which specific episodes must be cleared to flag the world as complete. If episodes from an excluded season
    are required, then only the episodes from the season that actually is included will be required instead."""
    display_name = "Episode(s) To Clear"
    option_season_1_episode_4 = 0
    option_season_2_episode_8 = 1
    option_s1e4_and_s2e8 = 2
    option_all_season_1 = 3
    option_all_season_2 = 4
    option_specific_number = 5
    default = 2


class NumberToClear(Range):
    """Sets how many episodes to clear. Only applies if Episodes To Clear is set to Specific Number. Will be reduced if
    higher than the total number of episodes included."""
    range_start = 1
    range_end = 12
    default = 12
    display_name = "Number To Clear"


arcane_options = {
    "episodes_to_clear": EpisodesToClear,
    "number_to_clear": NumberToClear,
    "death_link": DeathLink,
}
