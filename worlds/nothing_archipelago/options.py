from dataclasses import dataclass
from Options import Choice, OptionGroup, PerGameCommonOptions, Range, DefaultOnToggle, Toggle



class Goal(Choice):
    """
    Decide how long you would like to do nothing for (in seconds)
    Note this game is expected to take (goal/(2*time_cap_interval))*(time_cap_interval+goal) seconds to complete
    """

    display_name = "Goal"

    option_1_second = 1
    option_2_seconds = 2
    option_3_seconds = 3
    option_4_seconds = 4
    option_5_seconds = 5
    option_6_seconds = 6
    option_10_seconds = 10
    option_12_seconds = 12
    option_15_seconds = 15
    option_20_seconds = 20
    option_30_seconds = 30
    option_1_minute = 60
    option_2_minutes = 120
    option_3_minutes = 180
    option_4_minutes = 240
    option_5_minutes = 300
    option_6_minutes = 360
    option_10_minutes = 600
    option_12_minutes = 720
    option_15_minutes = 900
    option_20_minutes = 1200
    option_30_minutes = 1800
    option_1_hour = 3600
    option_2_hours = 7200
    option_3_hours = 10800
    option_4_hours = 14400
    option_6_hours = 21600
    option_8_hours = 28800
    option_12_hours = 43200
    option_24_hours = 86400

    default = option_20_minutes


class shopupgrades(DefaultOnToggle):
    """
    Add the upgrade shop into randomization
    Note Goal needs to be greater than 1200 seconds for all shop upgrades to be in logic
    """

    display_name = "Randomize Shop Upgrades"

class shopcolors(DefaultOnToggle):
    """
    Add the color shop into randomization
    Note Goal needs to be greater than 1200 seconds for any shop colors to be in logic
    """

    display_name = "Randomize Shop Colors"

class shopmusic(DefaultOnToggle):
    """
    Add the music shop into randomization
    Note Goal needs to be greater than 1200 seconds for any shop music to be in logic
    """

    display_name = "Randomize Shop Music"

class shopsounds(DefaultOnToggle):
    """
    Add the sound shop into randomization
    Note Goal needs to be greater than 1200 seconds for any shop sound to be in logic
    """

    display_name = "Randomize Shop Sounds"

class giftcoins(Toggle):
    """
    Enable recieving coins at game start
    """

    display_name = "Enable Starting Coins"

class milestoneinterval(Choice):
    """
    Decide how far apart each milestone location is (in seconds)
    Note Milestone Interval should be less than the goal
    """

    display_name = "Milestone Interval"

    option_1_second = 1
    option_2_seconds = 2
    option_3_seconds = 3
    option_4_seconds = 4
    option_5_seconds = 5
    option_6_seconds = 6
    option_10_seconds = 10
    option_12_seconds = 12
    option_15_seconds = 15
    option_20_seconds = 20
    option_30_seconds = 30
    option_1_minute = 60
    option_2_minutes = 120
    option_3_minutes = 180
    option_4_minutes = 240
    option_5_minutes = 300
    option_6_minutes = 360
    option_10_minutes = 600
    option_12_minutes = 720
    option_15_minutes = 900
    option_20_minutes = 1200
    option_30_minutes = 1800
    option_1_hour = 3600
    option_2_hours = 7200
    option_3_hours = 10800
    option_4_hours = 14400
    option_6_hours = 21600
    option_8_hours = 28800
    option_12_hours = 43200
    option_24_hours = 86400

    default = option_2_minutes

class timecapinterval(Choice):
    """
    Decide how much the timer cap should increase for each item recieved (in seconds)
    Note the time cap interval must be greater than or equal to the milestone interval
        if the time cap interval is greater the extra checks will be gifted coins
    """

    display_name = "Time Cap Increment"

    option_1_second = 1
    option_2_seconds = 2
    option_3_seconds = 3
    option_4_seconds = 4
    option_5_seconds = 5
    option_6_seconds = 6
    option_10_seconds = 10
    option_12_seconds = 12
    option_15_seconds = 15
    option_20_seconds = 20
    option_30_seconds = 30
    option_1_minute = 60
    option_2_minutes = 120
    option_3_minutes = 180
    option_4_minutes = 240
    option_5_minutes = 300
    option_6_minutes = 360
    option_10_minutes = 600
    option_12_minutes = 720
    option_15_minutes = 900
    option_20_minutes = 1200
    option_30_minutes = 1800
    option_1_hour = 3600
    option_2_hours = 7200
    option_3_hours = 10800
    option_4_hours = 14400
    option_6_hours = 21600
    option_8_hours = 28800
    option_12_hours = 43200
    option_24_hours = 86400

    default = option_2_minutes

class Startingcoincount(Range):
    """
    Decide how many coins you want to start with
    """

    display_name = "Starting Coins"

    range_start = 1
    range_end = 100
    default = 10

class Deathlink(Toggle):
    """
    Because why shouldn't your every move hurt everyone else
    """

    display_name = "Death Link"

class Deathlinkmercy(Range):
    """
    Because you only hate fun a little bit
    """

    display_name = "Timer Resets to send a death"

    range_start = 1
    range_end = 100
    default = 10

class TimeDilation(Range):
    """
    Because if i didn't provide this options the game could take > 120 years
    """

    display_name = "Time Dilation"

    range_start = 1
    range_end = 600
    default = 1


@dataclass
class NothingOptions(PerGameCommonOptions):
    goal: Goal
    shop_upgrades: shopupgrades
    shop_colors: shopcolors
    shop_music: shopmusic
    shop_sounds: shopsounds
    gift_coins: giftcoins
    milestone_interval: milestoneinterval
    timecap_interval: timecapinterval
    Starting_coin_count: Startingcoincount
    Death_link: Deathlink
    Death_link_mercy: Deathlinkmercy
    Time_dilation: TimeDilation

option_groups = [
    OptionGroup(
        "Randomizer Options",
        [shopupgrades, shopcolors, shopmusic, shopsounds],
    ),
    OptionGroup(
        "Game Duration Options",
        [Goal, milestoneinterval, timecapinterval, TimeDilation],
    ),
    OptionGroup(
        "Other",
        [giftcoins, Startingcoincount, Deathlink, Deathlinkmercy],
    ),
]


option_presets = {
    "4-hour game": {
        "goal": 1800,
        "shop_upgrades": True,
        "shop_colors": True,
        "shop_music": True,
        "shop_sounds": True,
        "gift_coins": True,
        "milestone_interval": 120,
        "timecap_interval": 120,
        "Starting_coin_count": 10,
        "Death_link": False,
        "Death_link_mercy": 100,
        "Time_dilation": 1
    },
    "Everyone else should suffer": {
        "goal": 86400,
        "shop_upgrades": True,
        "shop_colors": True,
        "shop_music": True,
        "shop_sounds": True,
        "gift_coins": True,
        "milestone_interval": 1,
        "timecap_interval": 1,
        "Starting_coin_count": 0,
        "Death_link": True,
        "Death_link_mercy": 1,
        "Time_dilation": 1
    }
}