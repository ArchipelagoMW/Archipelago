from Options import Choice, Option
import typing

class Goal(Choice):
    """The victory condition for your run. Stuff after the goal will not be shuffled."""
    display_name = "Goal"
    option_wall_of_flesh = 0
    option_plantera = 1
    option_moon_lord = 2
    option_zenith = 3
    default = 2

class Achievements(Choice):
    """
    Adds checks upon collecting achievements. Achievements for clearing bosses and events are excluded.
    "Exclude Grindy" also excludes fishing achievements.
    """
    display_name = "Achievements"
    option_none = 0
    option_exclude_grindy = 1
    option_exclude_fishing = 2
    option_all = 3
    default = 1

class FillExtraChecksWith(Choice):
    """
    Applies if you have achievements enabled. "Useful Items" helps to make the early game less grindy.
    Items are rewarded to all players in your Terraria world.
    """
    display_name = "Fill Extra Checks With"
    option_filler_items = 0
    option_useful_items = 1
    default = 1

options: typing.Dict[str, type(Option)] = {
    "goal": Goal,
    "achievements": Achievements,
    "fill_extra_checks_with": FillExtraChecksWith,
}
