from typing import Dict

from Options import Range, DefaultOnToggle, FreeText, Option


class EnableTimeLimit(DefaultOnToggle):
    """
    If the time limit is enabled, when time is up, any remaining items are forever encrypted, potentially making the
    seed unbeatable without cheating.
    """
    display_name = "Enable Time Limit"


class TimeLimitInMinutes(Range):
    """
    If the time limit is enabled, the number of minutes until any remaining items are forever encrypted. Has no effect
    if "Enable Time Limit" is disabled.
    """
    display_name = "Time Limit in Minutes"
    range_start = 30
    range_end = 43200  # 30 Days
    default = 240  # 4 Hours


class MaximumPharcoinCost(Range):
    """Maximum number of Pharcoins that are needed to decrypt any given item."""
    display_name = "Maximum Pharcoin Cost"
    range_start = 2
    range_end = 5
    default = 3


class ExtraPharcoinsPerPlayer(Range):
    """Extra Pharcoins in the item pool per player."""
    display_name = "Extra Pharcoins per Player"
    range_start = 0
    range_end = 25
    default = 5


class NumberOfItemsPerBlock(Range):
    """Number of items to encrypt in each block."""
    display_name = "Number of Items per Block"
    range_start = 5
    range_end = 100
    default = 15


class NumberOfItemBlocks(Range):
    """
    Number of blocks of items there are. Any items encrypted in a block require a certain percentage of items to be
    decrypted in the previous block to be eligible for decrypting.
    """
    display_name = "Number of Item Blocks"
    range_start = 5
    range_end = 25
    default = 5


class RequiredPercentageOfItemsDecryptedForBlockUnlock(Range):
    """The percentage of items that need to be decrypted in an earlier block to decrypt items in the next block."""
    display_name = "Required Percentage of Items Decrypted for Blocks to Unlock"
    range_start = 0
    range_end = 100
    default = 75


class StartingPassword(FreeText):
    """A password that's required to start Pharcryption. Useful for game hosts that want to start it instead."""
    display_name = "Starting Password"
    default = ""


PharcryptionOptions: Dict[str, type(Option)] = {
    "enable_time_limit": EnableTimeLimit,
    "time_limit_in_minutes": TimeLimitInMinutes,
    "maximum_pharcoin_cost": MaximumPharcoinCost,
    "extra_pharcoins_per_player": ExtraPharcoinsPerPlayer,
    "number_of_items_per_block": NumberOfItemsPerBlock,
    "number_of_item_blocks": NumberOfItemBlocks,
    "required_percentage_of_items_decrypted_for_block_unlock": RequiredPercentageOfItemsDecryptedForBlockUnlock,
    "starting_password": StartingPassword,
}
