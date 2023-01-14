from Options import Choice, Option
import typing

class Goal(Choice):
    """The victory condition for your run. Stuff after the goal will not be shuffled."""
    display_name = "Goal"
    option_wall_of_flesh = 0
    option_mechanical_bosses = 1
    option_plantera = 2
    option_moon_lord = 3
    option_zenith = 4
    default = 3

options: typing.Dict[str, type(Option)] = {
    # "goal": Goal,
}
