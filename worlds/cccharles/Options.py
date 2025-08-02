from dataclasses import dataclass
from Options import DefaultOnToggle, Range, Toggle, DeathLink, Choice, PerGameCommonOptions, Visibility
from .Items import useless_items


class ScrapsAmountAsCheck(Range):
    """
    What number of scraps are necessary to get an item as a check.
    The collected scraps are not added to the inventory.
    You must collect this number of scraps to get 1 randomized item.
    '0' means the option is disabled and no scraps will be randomized (except mission rewards).
    """
    display_name = "Scraps amount"
    range_start = 0
    range_end = 5
    default = 1
    visibility = Visibility.none


class KeyFragments(Range):
    """
    Change keys into fragments of keys, instead of directly get a key.
    Collecting this amount of fragments will craft the associated key.
    '1' means the option is disabled, because 1 fragment = 1 key.
    Remember there are 7 keys in the game, 8 in total if the key to access the train is included.
    If the 'Train access' option is enabled, the key to access the train is affected (40 fragments).
    If 'Train access' is disabled, there are at most 7x5 = 35 fragments, 8x5 = 40 fragments otherwise.
    """
    display_name = "Key fragments amount"
    range_start = 1
    range_end = 5
    default = 1
    visibility = Visibility.none


class AddCompass(Choice):
    """
    Add a compass in the game, that allows a UI showing the closest check to do.
    This item does not exist in the original game.
    The following options are provided :
    - **No compass** : Disabled, the game stays vanilla.
    - **Compass at start** : The compass is given at the start of the game.
    - **Compass as check** : The compass is added to the item pool, meaning it must first be found.
    """
    display_name = "Add compass"
    option_no_compass = 0
    option_compass_at_start = 1
    option_compass_as_check = 2
    default = 1
    visibility = Visibility.none


class ScrapsTracker(DefaultOnToggle):
    """
    If allowed, the amount of collected scraps will be shown on the map.
    """
    display_name = "Allow scraps tracker"
    visibility = Visibility.none


class TrainUpgradeFragments(Toggle):
    """
    If allowed, none of the 3 upgrades of the train can be done without collecting a blueprint fragment.
    These fragments will be added to the item pool : Speed Upgrade ; Damage Upgrade ; Armor Upgrade.
    The 'Repair' option on the blueprint will remain unchanged.
    """
    display_name = "Allow train upgrade fragments"
    visibility = Visibility.none


class RandomStartingWeapon(DefaultOnToggle):
    """
    If allowed, the starting weapon will be randomized among the 4 possible guns.
    """
    display_name = "Random starting weapon"
    visibility = Visibility.none


class TrainAccess(Toggle):
    """
    If allowed, the key allowing the access to the train will be added to the item pool.
    Meaning the player cannot use the train while the key is not found.
    Note this option is affected by the "Key fragments amount" option only if enabled.
    """
    display_name = "Train access"
    visibility = Visibility.none


class PaintCanRule(Choice):
    """
    Add a rule when a paint can is collected.
    The following options are provided :
    - **No rule** : Disabled, the game stays vanilla.
    - **Randomized** : The paint cans are added to the item pool.
    - **Vanilla with hints** : The paint cans are not randomized and give hints when collected.
    - **Random with hints** : The paint cans are randomized and give hints when collected.
    """
    display_name = "Paint can rule"
    option_no_rule = 0
    option_randomized = 1
    option_vanilla_with_hints = 2
    option_random_with_hints = 3
    default = 1
    visibility = Visibility.none


class SplitRemoteExplosive(Choice):
    """
    Split the 8 explosives to make up to 8 more checks.
    The following options are provided :
    - **Stack of 1** : Split the explosives to 8 stacks of 1.
    - **Stack of 2** : Split the explosives to 4 stacks of 2.
    - **Stack of 4** : Split the explosives to 2 stacks of 4.
    - **Stack of 8** : Split the explosives to 1 stacks of 8 (vanilla).
    """
    display_name = "Paint can rule"
    option_stack_of_1 = 1
    option_stack_of_2 = 2
    option_stack_of_4 = 4
    option_stack_of_8 = 8
    default = 1
    visibility = Visibility.none


class UnscrapTrap(Range):
    """
    What percent of traps removing 5 scraps from the inventory will be added to the item pool.
    """
    display_name = "Unscrap-trap %"
    range_start = 0
    range_end = 20
    default = 0
    visibility = Visibility.all


class DerailedTrap(Range):
    """
    What percent of traps reducing the train HP by 40 will be added to the item pool.
    """
    display_name = "Derailed-trap %"
    range_start = 0
    range_end = 20
    default = 0
    visibility = Visibility.none


class GuruTrap(Range):
    """
    What percent of traps spawning a cultist near the player for a short while will be added to the item pool.
    """
    display_name = "Guru-trap %"
    range_start = 0
    range_end = 20
    default = 0
    visibility = Visibility.none


@dataclass
class CCCharlesOptions(PerGameCommonOptions):
    scraps_amount_as_check: ScrapsAmountAsCheck
    key_fragments: KeyFragments
    add_compass: AddCompass
    scraps_tracker: ScrapsTracker
    train_upgrade_fragments: TrainUpgradeFragments
    random_starting_weapon: RandomStartingWeapon
    train_access: TrainAccess
    paint_can_rule: PaintCanRule
    split_remote_explosive: SplitRemoteExplosive
    unscrap_trap: UnscrapTrap
    derailed_trap: DerailedTrap
    guru_trap: GuruTrap
    death_link: DeathLink
