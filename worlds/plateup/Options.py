from dataclasses import dataclass
from Options import Choice, PerGameCommonOptions, Range, Toggle

class Goal(Choice):
    """Set the goal for completion."""
    display_name = "Goal"
    option_franchise_x_times = 0
    option_complete_x_days = 1
    default = 0

class FranchiseCount(Range):
    """Select how many franchises are required for completion.(Only used if Goal=complete_x_franchises)"""
    display_name = "Required Franchise Count"
    range_start = 1
    range_end = 50
    default = 1

class DayCount(Range):
    """Select how many days are required for completion. (Only used if Goal=complete_x_days)"""
    display_name = "Required Day Count"
    range_start = 10
    range_end = 1000
    default = 10

class DayLeaseInterval(Range):
    """How many in-game days between each required Day Lease (min 1)."""
    display_name = "Day Lease Interval"
    range_start = 1
    range_end = 30
    default = 5

class DishCount(Range):
    """How many dishes the player starts with (1-17) or 0 for disabled."""
    display_name = "Starting Dish Count"
    range_start = 0
    range_end = 17
    default = 1

class ItemsKept(Range):
    """How many appliances the player keeps each run."""
    display_name = "Starting Appliance Count"
    range_start = 1
    range_end = 5
    default = 1

class DeathLink(Toggle):
    """Enable death link mode, affecting all linked players."""
    display_name = "Death Link"
    default = 0

class DeathLinkBehavior(Choice):
    """Choose what happens when DeathLink triggers."""
    display_name = "Death Link Behavior"
    option_reset_run = 0
    option_reset_to_last_star = 1
    default = 0

class ApplianceSpeedMode(Choice):
    """
    Choose whether all Speed Upgrade Appliances are "grouped" (single item),
    or "separate" (Cook, Chop, Clean).
    """
    display_name = "Appliance Speed Upgrade Mode"
    option_grouped = 0
    option_separate = 1
    default = 0

class PlayerSpeedUpgradeCount(Range):
    """How many Player Speed Upgrade items to place (0-10)."""
    display_name = "Player Speed Upgrade Count"
    range_start = 0
    range_end = 10
    default = 5

class ApplianceSpeedUpgradeCount(Range):
    """How many Appliance Speed Upgrade items to place (0-10)."""
    display_name = "Appliance Speed Upgrade Count"
    range_start = 0
    range_end = 10
    default = 5

class StartingMoneyCap(Range):
    """Starting total money cap (in gold). You cannot hold more than this amount at any time until increased by items."""
    display_name = "Starting Money Cap"
    range_start = 10
    range_end = 40
    default = 20



@dataclass
class PlateUpOptions(PerGameCommonOptions):
    goal: Goal
    franchise_count: FranchiseCount
    day_count: DayCount
    dish: DishCount
    appliances_kept: ItemsKept
    death_link: DeathLink
    death_link_behavior: DeathLinkBehavior
    appliance_speed_mode: ApplianceSpeedMode
    day_lease_interval: DayLeaseInterval
    player_speed_upgrade_count: PlayerSpeedUpgradeCount
    appliance_speed_upgrade_count: ApplianceSpeedUpgradeCount
    starting_money_cap: StartingMoneyCap
    # removed item count; items are generated automatically from total days