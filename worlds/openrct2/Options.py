from enum import IntEnum
from typing import TypedDict
from Options import DefaultOnToggle, Toggle, Range, Choice, OptionSet

class LocationBalancingMode(IntEnum):
    disabled = 0
    compromise = 1
    full = 2


class DeathLinkMode(IntEnum):
    disabled = 0
    enabled = 1

class Difficulty(IntEnum):
    very_easy = 0
    easy = 1
    medium = 2
    hard = 3
    extreme = 4

class Randomization_Range(IntEnum):
    low = 0
    medium = 1
    high = 2
    extreme = 3

class Scenario_Length(IntEnum):
    speedrun = 0
    normal = 1
    lengthy = 2
    marathon = 3
    
class Stat_ReRolls(IntEnum):
    never = 0
    infrequent = 1
    semi_frequent = 2
    frequent = 3
    very_frequent = 4
    extremely_frequent = 5


class OpenRCT2OnToggle(DefaultOnToggle):
    @property
    def result(self) -> bool:
        return bool(self.value)


class OpenRCT2Toggle(Toggle):
    @property
    def result(self) -> bool:
        return bool(self.value)


class LocationBalancing(Choice):
    """Location balancing affects the density of progression items found in your world relative to other worlds. This setting changes nothing for solo games.

    - Disabled: Location density in your world can fluctuate greatly depending on the settings of other players. In extreme cases, your world may be entirely populated with filler items

    - Compromise: Locations are balanced to a midpoint between "fair" and "natural"

    - Full: Locations are balanced in an attempt to make the number of progression items sent out and received equal over the entire game"""
    auto_display_name = True
    display_name = "Location Balancing"
    option_disabled = LocationBalancingMode.disabled.value
    option_compromise = LocationBalancingMode.compromise.value
    option_full = LocationBalancingMode.full.value
    default = LocationBalancingMode.compromise.value

    

class DeathLink(Choice):
    """DeathLink is an opt-in feature for Multiworlds where individual death events are propagated to all games with DeathLink enabled.

    - Disabled: No changes to base game.

    - Enabled: When any ride crashes, the signal will be sent out, killing any player in the game. Inversely, any received deathlink will instantly cause a random ride to crash.

    When enabled, there is a 20 second rest period between any deathlink event. Fix that coaster quickly!
    """
    auto_display_name = True
    display_name = "DeathLink"
    option_disabled = DeathLinkMode.disabled.value
    option_enabled = DeathLinkMode.enabled.value
    default = DeathLinkMode.enabled.value

class Difficulty(Choice):
    """Choose a difficulty for the randomization. This will affect things such as ride multipliers and interest rates for loans.
    """
    auto_display_name = True
    display_name = "Difficulty"
    option_very_easy = Difficulty.very_easy.value
    option_easy = Difficulty.easy.value
    option_medium = Difficulty.medium.value
    option_hard = Difficulty.hard.value
    option_extreme = Difficulty.extreme.value
    default = Difficulty.medium.value

class Randomization_Range(Choice):
    """Choose a difficulty for the randomization. This will affect things such as ride multipliers and interest rates for loans.
    """
    auto_display_name = True
    display_name = "Randomization Range"
    option_low = Randomization_Range.low.value
    option_medium = Randomization_Range.medium.value
    option_high = Randomization_Range.high.value
    option_extreme = Randomization_Range.extreme.value
    default = Randomization_Range.medium.value

class Scenario_Length(Choice):
    """Choose how long this game will last. It's reccomended to choose based on how long other worlds in the multi-world take to complete.
    """
    auto_display_name = True
    display_name = "Scenario Length"
    option_speedrun = Scenario_Length.speedrun.value
    option_normal = Scenario_Length.normal.value
    option_lengthy = Scenario_Length.lengthy.value
    option_marathon = Scenario_Length.marathon.value
    default = Scenario_Length.normal.value

class Stat_ReRolls(Choice):
    """How often to rerandomize the stats for ride types. Build the Theme Park of Theseus!
    """
    auto_display_name = True
    display_name = "Stat Re-Rolls"
    option_never = Stat_ReRolls.never.value
    option_infrequent = Stat_ReRolls.infrequent.value
    option_semi_frequent = Stat_ReRolls.semi_frequent.value
    option_frequent = Stat_ReRolls.frequent.value
    option_very_frequent = Stat_ReRolls.very_frequent.value
    option_extremely_frequent = Stat_ReRolls.extremely_frequent.value
    default = Stat_ReRolls.infrequent.value

class Include_Park_Rules(OpenRCT2OnToggle):
    """Enables all park restrictions (No building above tree height, no marketing campains, harder guest generation, etc.) and includes items that will automatically disable them when found."""
    display_name = "Include Park Rules"


class Randomize_Park_Values(OpenRCT2OnToggle):
    """Randomizes values such as starting cash, starting bank loan amount, and the max bank loan"""
    display_name = "Randomize Park Values"

class Include_Guest_Objective(OpenRCT2OnToggle):
    """Include an objective to reach a certain number of guests. Multiple objectives can be enabled!"""
    display_name = "Include Guest Objective"

class Guest_Objective(Range):
    """If enabled, choose how many guests are required to win the scenario"""
    display_name = "Guest Objective"
    range_start = 1
    range_end = 7500
    default = 3000

class Include_Park_Value_Objective(OpenRCT2OnToggle):
    """Include an objective to achive a certain park value in Dollars (The game will adjust to your local currency). Multiple objectives can be enabled!"""
    display_name = "Include Park Value Objective"

class Park_Value_Objective(Range):
    """If enabled, choose what park value is required to win the scenario."""
    display_name = "Park Value Objective"
    range_start = 1
    range_end = 1000000
    default = 300000

class Include_Roller_Coaster_Objective(OpenRCT2OnToggle):
    """Include an objective to build a certain number of Roller Coasters with optional Paramaters. Multiple objectives can be enabled!"""
    display_name = "Include Roller Coaster Objective"

class Roller_Coaster_Objective(Range):
    """If enabled, choose how many coasters, and what prerequisites they need to beat the scenario."""
    display_name = "Roller Coaster Objective"
    range_start = 1
    range_end = 20
    default = 10

class Roller_Coaster_Excitement(Range):
    """Select the minimum excitement 😀 for a coaster to count towards your objective. 0 will disable a minimum excitement rating."""
    display_name = "Excitement Requirement"
    range_start = 0
    range_end = 10
    default = 6

class Roller_Coaster_Intensity(Range):
    """Select the minimum intensity 😬 for a coaster to count towards your objective. 0 will disable a minimum intensity rating."""
    display_name = "Intensity Requirement"
    range_start = 0
    range_end = 10
    default = 6

class Roller_Coaster_Nausea(Range):
    """Select the minimum nausea 🤢 for a coaster to count towards your objective. 0 will disable a minimum nausea rating."""
    display_name = "Nausea Requirement"
    range_start = 0
    range_end = 10
    default = 5

class Include_Park_Rating_Objective(OpenRCT2OnToggle):
    """Include an objective to require a minimum park rating for completion. Multiple objectives can be enabled!"""
    display_name = "Include Park Rating Objective"

class Park_Rating_Objective(Range):
    """If enabled, choose the minimum park rating needed to beat the scenario."""
    display_name = "Park Rating Objective"
    range_start = 0
    range_end = 999
    default = 800

class Pay_Off_Loan(OpenRCT2OnToggle):
    """Require Loan to be paid off before scenario completion is awarded"""
    display_name = "Pay Off Loan"



openRCT2_options = {
    # generator options
    "location_balancing": LocationBalancing,
    "difficulty": Difficulty,

    # deathlink
    "deathlink": DeathLink,

    # in-game options. All Archipelago needs to do with these is pass them to OpenRCT2. The game will handle the rest
    "randomization_range": Randomization_Range,
    "scenario_length": Scenario_Length,
    "stat_rerolls": Stat_ReRolls,
    "include_park_rules": Include_Park_Rules,
    "randomize_park_values": Randomize_Park_Values,
    "include_guest_objective": Include_Guest_Objective,
    "gust_objective": Guest_Objective,
    "include_park_value_objective": Include_Park_Value_Objective,
    "park_value_objective": Park_Value_Objective,
    "include_roller_coaster_objective": Include_Roller_Coaster_Objective,
    "roller_coaster_objective": Roller_Coaster_Objective,
    "roller_coaster_excitement": Roller_Coaster_Excitement,
    "roller_coaster_intensity": Roller_Coaster_Intensity,
    "roller_coaster_nausea": Roller_Coaster_Nausea,
    "include_park_rating_objective": Include_Park_Rating_Objective,
    "park_rating_objective": Park_Rating_Objective,
    "pay_off_loan": Pay_Off_Loan
}

OpenRCT2Options = TypedDict("OpenRCT2Options", {option.__name__: option for option in openRCT2_options.values()})
