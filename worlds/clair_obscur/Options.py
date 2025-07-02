from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions, StartInventory, OptionGroup


class Goal(Choice):
    """
    The victory condition for your run
    """

    display_name = "Goal"
    option_paintress = 0
    option_curator = 1
    option_painted_love = 2
    option_simon = 3

    default = 1

class ClairObscurStartInventory(StartInventory):
    """
    Start with these items
    """

@dataclass
class ClairObscurOptions(PerGameCommonOptions):
    goal: Goal

    start_inventory: ClairObscurStartInventory

OPTIONS_GROUP = [
    OptionGroup(
        "Item & Location Options", [
            ClairObscurStartInventory,
        ], False,
    ),
]