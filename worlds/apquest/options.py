from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle

# In this file, we define the options the player can pick.
# The most common types of options are Toggle, Range and Choice.


# A toggle is an option that can either be on or off. This will be represented by a checkbox on the website.
class HardMode(Toggle):
    """
    In hard mode, the basic enemy and the final boss will have more health.
    The Health Upgrades become progression, as they are now required to beat the final boss.
    """

    display_name = "Hard Mode"


# A range is a numeric option with a min and max value. This will be represented by a slider on the website.
class ConfettiExplosiveness(Range):
    """
    How much confetti each use of a confetti cannon will fire.
    """

    display_name = "Confetti Explosiveness"

    range_start = 0
    range_end = 10
    default = 3


# A choice is an option with multiple discrete choices. This will be represented by a dropdown on the website.
class PlayerSprite(Choice):
    """
    The sprite that the player will have.
    """

    display_name = "Player Sprite"

    option_human = 0
    option_duck = 1
    option_horse = 2
    option_cat = 3

    default = option_human


# We must now define a dataclass inheriting from PerGameCommonOptions that we put all our options in.
@dataclass
class APQuestOptions(PerGameCommonOptions):
    hard_mode: HardMode
    confetti_explosiveness: ConfettiExplosiveness
    player_sprite: PlayerSprite


# If we want to group our options by similar type, we can do so as well. This looks nice on the website.
option_groups = [
    OptionGroup(
        "Gameplay Options",
        [HardMode],
    ),
    OptionGroup(
        "Aesthetic Options",
        [ConfettiExplosiveness, PlayerSprite],
    ),
]

# Finally, we can define some option presets if we want the player to be able to quickly choose a specific "mode".
option_presets = {
    "boring": {
        "hard_mode": False,
        "confetti_explosiveness": ConfettiExplosiveness.range_start,
        "player_sprite": PlayerSprite.option_human,
    },
    "the true way to play": {
        "hard_mode": True,
        "confetti_explosiveness": ConfettiExplosiveness.range_end,
        "player_sprite": PlayerSprite.option_duck,
    },
}
