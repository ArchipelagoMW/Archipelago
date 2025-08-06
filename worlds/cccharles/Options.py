from dataclasses import dataclass
from Options import DefaultOnToggle, Range, Toggle, DeathLink, Choice, PerGameCommonOptions, Visibility
from .Items import useless_items


class ScrapsAmountAsCheck(Range):
    """
    What number of scraps are required to get an item as a check.
    The collected scraps are not added to the inventory.
    You must collect this number of scraps to send 1 randomized item.

    '0' means the option is disabled and no scraps is randomized (except mission rewards).
    """
    display_name = "Scraps amount as check"
    range_start = 0
    range_end = 5
    default = 1
    visibility = Visibility.all


class ScrapsDetector(Choice):
    """
    Add a detector in the game, showing the closest scraps in a UI.

    **No:** Disabled.

    **Start:** The detector is enabled from the start of the game.

    **Randomized:** The detector is randomized.
    """
    display_name = "Scraps detector"
    option_no = 0
    option_start = 1
    option_randomized = 2
    default = 1
    visibility = Visibility.all


class ScrapsTracker(DefaultOnToggle):
    """
    The number of collected scraps in the region is shown on the map and the UI.
    """
    display_name = "Scraps tracker"
    visibility = Visibility.all


class BlueprintFragments(Toggle):
    """
    Blueprint fragments must be received to access the 3 upgrades of the train.
    These fragments are randomized:

    Speed Upgrade ; Damage Upgrade ; Armor Upgrade

    The 'Repair' option on the blueprint is not affected.
    """
    display_name = "Blueprint fragments"
    visibility = Visibility.all


class KeyFragments(Range):
    """
    Break keys into key fragments.
    Collecting enough fragments crafts the associated key.

    '1' means the option is disabled (1 fragment = 1 key).

    If the 'Train access' option is disabled, there are at most:

    **7x5 = 35 fragments**

    **8x5 = 40 fragments otherwise**
    """
    display_name = "Key fragments"
    range_start = 1
    range_end = 5
    default = 1
    visibility = Visibility.all


class TrainAccess(Toggle):
    """
    The key to access the train is randomized.
    This option is affected by the "Key fragments" option if enabled.
    """
    display_name = "Train access"
    visibility = Visibility.all


class TrainRepairCost(Range):
    """
    Set the number of required scraps to repair the train.
    """
    display_name = "Repair cost"
    range_start = 0
    range_end = 5
    default = 1
    visibility = Visibility.all


class RandomStartingWeapon(DefaultOnToggle):
    """
    Randomize the starting weapon among the 4 possible guns.
    """
    display_name = "Random starting weapon"
    visibility = Visibility.all


class PaintCansRule(Choice):
    """
    Add a rule for the paint cans.

    **No:** Disabled.

    **Randomized:** The paint cans are randomized.

    **Hints:** The paint cans are randomized and give hints when received.

    **Potions:** The paint cans are randomized and confer passive effects when received.
    """
    display_name = "Paint Cans rule"
    option_no = 0
    option_randomized = 1
    option_hints = 2
    option_potions = 3
    default = 1
    visibility = Visibility.all


class SplitRemoteExplosives(Choice):
    """
    Split the explosives to make up to 8 packs to randomize.

    **1 pack:** 1 pack of 8 (vanilla).

    **2 packs:** 2 packs of 4.

    **4 packs:** 4 packs of 2.

    **8 packs:** 8 packs of 1.
    """
    display_name = "Split Remote Explosives"
    option_1_pack = 1
    option_2_packs = 2
    option_4_packs = 4
    option_8_packs = 8
    default = 1
    visibility = Visibility.all


class UnscrapTrap(Range):
    """
    What percent of traps removing 5 scraps from the inventory are randomized.
    """
    display_name = "Unscrap-trap %"
    range_start = 0
    range_end = 10
    default = 0
    visibility = Visibility.all


class DerailedTrap(Range):
    """
    What percent of traps reducing the train HP by 30 are randomized.
    """
    display_name = "Derailed-trap %"
    range_start = 0
    range_end = 10
    default = 0
    visibility = Visibility.all


@dataclass
class CCCharlesOptions(PerGameCommonOptions):
    scraps_amount_as_check: ScrapsAmountAsCheck
    scraps_detector: ScrapsDetector
    scraps_tracker: ScrapsTracker
    blueprint_fragments: BlueprintFragments
    key_fragments: KeyFragments
    train_access: TrainAccess
    train_repair_cost: TrainRepairCost
    random_starting_weapon: RandomStartingWeapon
    paint_cans_rule: PaintCansRule
    split_remote_explosives: SplitRemoteExplosives
    unscrap_trap: UnscrapTrap
    derailed_trap: DerailedTrap
    death_link: DeathLink
