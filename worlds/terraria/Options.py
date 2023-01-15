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

options: typing.Dict[str, type(Option)] = {
    "goal": Goal,
}
