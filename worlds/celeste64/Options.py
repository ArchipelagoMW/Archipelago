from dataclasses import dataclass

from Options import Choice, Range, Toggle, DeathLink, OptionGroup, PerGameCommonOptions


class DeathLinkAmnesty(Range):
    """
    How many deaths it takes to send a DeathLink
    """
    display_name = "Death Link Amnesty"
    range_start = 1
    range_end = 30
    default = 10

class TotalStrawberries(Range):
    """
    How many Strawberries exist
    """
    display_name = "Total Strawberries"
    range_start = 0
    range_end = 46
    default = 20

class StrawberriesRequiredPercentage(Range):
    """
    Percentage of existing Strawberries you must receive to finish
    """
    display_name = "Strawberries Required Percentage"
    range_start = 0
    range_end = 100
    default = 80


class LogicDifficulty(Choice):
    """
    Whether the logic expects you to play the intended way, or to be able to use advanced tricks and skips
    """
    display_name = "Logic Difficulty"
    option_standard = 0
    option_hard = 1
    default = 0

class MoveShuffle(Toggle):
    """
    Whether the following base movement abilities are shuffled into the item pool:
    - Ground Dash
    - Air Dash
    - Skid Jump
    - Climb

    NOTE: Having Move Shuffle and Standard Logic Difficulty will guarantee that one of the four Move items will be immediately accessible

    WARNING: Combining Move Shuffle and Hard Logic Difficulty can require very difficult tricks
    """
    display_name = "Move Shuffle"


class Friendsanity(Toggle):
    """
    Whether chatting with your friends grants location checks
    """
    display_name = "Friendsanity"

class Signsanity(Toggle):
    """
    Whether reading signs grants location checks
    """
    display_name = "Signsanity"

class Carsanity(Toggle):
    """
    Whether riding on cars grants location checks
    """
    display_name = "Carsanity"


class BadelineChaserSource(Choice):
    """
    What type of action causes more Badeline Chasers to start spawning

    Locations: The number of locations you've checked contributes to Badeline Chasers

    Strawberries: The number of Strawberry items you've received contributes to Badeline Chasers
    """
    display_name = "Badeline Chaser Source"
    option_locations = 0
    option_strawberries = 1
    default = 0

class BadelineChaserFrequency(Range):
    """
    How many of the `Badeline Chaser Source` actions must occur to make each Badeline Chaser start spawning

    NOTE: Choosing `0` disables Badeline Chasers entirely

    WARNING: Turning on Badeline Chasers alongside Move Shuffle could result in extremely difficult situations
    """
    display_name = "Badeline Chaser Frequency"
    range_start = 0
    range_end = 10
    default = 0

class BadelineChaserSpeed(Range):
    """
    How many seconds behind you each Badeline Chaser will be
    """
    display_name = "Badeline Chaser Speed"
    range_start = 2
    range_end = 10
    default = 3


celeste_64_option_groups = [
    OptionGroup("Goal Options", [
        TotalStrawberries,
        StrawberriesRequiredPercentage,
    ]),
    OptionGroup("Sanity Options", [
        Friendsanity,
        Signsanity,
        Carsanity,
    ]),
    OptionGroup("Badeline Chasers", [
        BadelineChaserSource,
        BadelineChaserFrequency,
        BadelineChaserSpeed,
    ]),
]


@dataclass
class Celeste64Options(PerGameCommonOptions):
    death_link: DeathLink
    death_link_amnesty: DeathLinkAmnesty

    total_strawberries: TotalStrawberries
    strawberries_required_percentage: StrawberriesRequiredPercentage

    logic_difficulty: LogicDifficulty
    move_shuffle: MoveShuffle

    friendsanity: Friendsanity
    signsanity: Signsanity
    carsanity: Carsanity

    badeline_chaser_source: BadelineChaserSource
    badeline_chaser_frequency: BadelineChaserFrequency
    badeline_chaser_speed: BadelineChaserSpeed
