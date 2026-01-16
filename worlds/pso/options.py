from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle

# In this file, we define the options the player can pick.
# The most common types of options are Toggle, Range and Choice.

# Options will be in the game's template yaml.
# They will be represented by checkboxes, sliders etc. on the game's options page on the website.
# (Note: Options can also be made invisible from either of these places by overriding Option.visibility.
#  APQuest doesn't have an example of this, but this can be used for secret / hidden / advanced options.)

# For further reading on options, you can also read the Options API Document:
# https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/options%20api.md

class StartWithLavisBlade(Toggle):
    """
    You know you want one.
    """
    display_name = "Start with Lavis Blade"

class Goal(Choice):
    """
    Completing this objective tells Archipelago you've completed your seed
    """
    display_name = "Goal"

    option_defeat_dark_falz = 0
    option_defeat_the_dragon = 1
    option_defeat_olga_flow = 2
    option_quest_completion = 3
    default = 0


class QuestsRequired(Range):
    """
    How many quests must be successfully completed to beat the seed, if Quest Completion is selected as the Goal
    Has no effect if another goal is chosen
    """
    display_name = "QuestsRequired"

    range_start = 1
    range_end = 26
    default = 9

class TrapChance(Range):
    """
    Percentage chance that any given filler item will be replaced by a random trap
    """

    display_name = "Trap Chance"

    range_start = 0
    range_end = 100
    default = 0


# We must now define a dataclass inheriting from PerGameCommonOptions that we put all our options in.
# This is in the format "option_name_in_snake_case: OptionClassName".
@dataclass
class PSOOptions(PerGameCommonOptions):
    goal: Goal
    quests_required: QuestsRequired
    start_with_lavis_blade: StartWithLavisBlade
    trap_chance: TrapChance


# If we want to group our options by similar type, we can do so as well. This looks nice on the website.
option_groups = [
    OptionGroup(
        "Goal Options",
        [Goal, QuestsRequired],
    ),
    OptionGroup(
        "Starting Items",
        [StartWithLavisBlade],
    ),
    OptionGroup(
        "Misc. Options",
        [TrapChance]
    )
]

# Finally, we can define some option presets if we want the player to be able to quickly choose a specific "mode".
option_presets = {
    "normal": {
        "goal": Goal.option_defeat_dark_falz,
        "quests_required": 9,
        "start_with_lavis_blade": False,
        "trap_chance": 5
    },
    "debug": {
        "goal": Goal.option_defeat_the_dragon,
        "quests_required": 9,
        "start_with_lavis_blade": True,
        "trap_chance": 50
    },
}
