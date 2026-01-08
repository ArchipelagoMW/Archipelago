import typing
from dataclasses import dataclass
from typing import Dict, Any
from Options import Option, Choice, DeathLink, Range, Toggle, PerGameCommonOptions, OptionGroup, OptionSet

class Goal(Choice):
    """The main victory condition for your run"""
    display_name = "Goal"
    option_high_dragun = 0
    option_lich = 1
    default = 0

class AdditionalGoals(OptionSet):
    """Select additional bosses to be required to complete your run'"""
    display_name = "Additional Goals"
    default = {}
    valid_keys = ["Blobulord", "Old King", "Resourceful Rat", "Agunim", "Advanced Dragun"]

class RandomGunTierD(Range):
    """Amount of D tier guns in the item pool"""
    display_name = "D Tier Guns"
    range_start = 0
    range_end = 20
    default = 5

class RandomGunTierC(Range):
    """Amount of C tier guns in the item pool"""
    display_name = "C Tier Guns"
    range_start = 0
    range_end = 20
    default = 3

class RandomGunTierB(Range):
    """Amount of B tier guns in the item pool"""
    display_name = "B Tier Guns"
    range_start = 0
    range_end = 20
    default = 3

class RandomGunTierA(Range):
    """Amount of A tier guns in the item pool"""
    display_name = "A Tier Guns"
    range_start = 0
    range_end = 20
    default = 2

class RandomGunTierS(Range):
    """Amount of S tier guns in the item pool"""
    display_name = "S Tier Guns"
    range_start = 0
    range_end = 20
    default = 2

class RandomItemTierD(Range):
    """Amount of D tier items in the item pool"""
    display_name = "D Tier Items"
    range_start = 0
    range_end = 20
    default = 5

class RandomItemTierC(Range):
    """Amount of C tier items in the item pool"""
    display_name = "C Tier Items"
    range_start = 0
    range_end = 20
    default = 3

class RandomItemTierB(Range):
    """Amount of B tier items in the item pool"""
    display_name = "B Tier Items"
    range_start = 0
    range_end = 20
    default = 3

class RandomItemTierA(Range):
    """Amount of A tier items in the item pool"""
    display_name = "A Tier Items"
    range_start = 0
    range_end = 20
    default = 2

class RandomItemTierS(Range):
    """Amount of S tier items in the item pool"""
    display_name = "S Tier Items"
    range_start = 0
    range_end = 20
    default = 2

class PickupAmount(Range):
    """Amount of item pickups in the item pool"""
    display_name = "Pickup Amount"
    range_start = 0
    range_end = 50
    default = 10

class TrapAmount(Range):
    """Amount of traps in the item pool"""
    display_name = "Trap Amount"
    range_start = 0
    range_end = 50
    default = 10

gungeon_option_groups = [
    OptionGroup("Item Amount Options", [
        RandomGunTierD,
        RandomGunTierC,
        RandomGunTierB,
        RandomGunTierA,
        RandomGunTierS,
        RandomItemTierD,
        RandomItemTierC,
        RandomItemTierB,
        RandomItemTierA,
        RandomItemTierS,
        PickupAmount,
        TrapAmount,
    ])
]

gungeon_options_presets: Dict[str, Dict[str, Any]] = {
    "All Bosses": {
        "goal":                  Goal.option_lich,
        "additional_goals":      AdditionalGoals.valid_keys,
    },
    "D Tier": {
        "random_gun_tier_d":     RandomGunTierD.range_end,
        "random_gun_tier_c":     0,
        "random_gun_tier_b":     0,
        "random_gun_tier_a":     0,
        "random_gun_tier_s":     0,
        "random_item_tier_d":    RandomItemTierD.range_end,
        "random_item_tier_c":    0,
        "random_item_tier_b":    0,
        "random_item_tier_a":    0,
        "random_item_tier_s":    0,
    },
    "Random": {
        "pickup_amount":         "random",
        "random_gun_tier_d":     "random",
        "random_gun_tier_c":     "random",
        "random_gun_tier_b":     "random",
        "random_gun_tier_a":     "random",
        "random_gun_tier_s":     "random",
        "trap_amount":           "random",
        "random_item_tier_d":    "random",
        "random_item_tier_c":    "random",
        "random_item_tier_b":    "random",
        "random_item_tier_a":    "random",
        "random_item_tier_s":    "random",
    },
}

@dataclass
class GungeonOptions(PerGameCommonOptions):
    death_link: DeathLink
    goal: Goal
    pickup_amount: PickupAmount
    random_gun_tier_d: RandomGunTierD
    random_gun_tier_c: RandomGunTierC
    random_gun_tier_b: RandomGunTierB
    random_gun_tier_a: RandomGunTierA
    random_gun_tier_s: RandomGunTierS
    trap_amount: TrapAmount
    random_item_tier_d: RandomItemTierD
    random_item_tier_c: RandomItemTierC
    random_item_tier_b: RandomItemTierB
    random_item_tier_a: RandomItemTierA
    random_item_tier_s: RandomItemTierS
    additional_goals: AdditionalGoals
