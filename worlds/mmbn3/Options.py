from Options import Choice, Range, DefaultOnToggle


class ExtraRanks(Range):
    """
    How many extra Undernet Ranks to add to the pool in place of filler items.
    The more ranks there are, the faster the game will go.
    Depending on your other options, you might not have enough filler items to replace.
    If generation errors occur, consider reducing this value.
    """
    display_name = "Extra Undernet Ranks"
    range_start = 0
    range_end = 16
    default = 0


class IncludeJobs(DefaultOnToggle):
    """
    Whether Jobs can be included in logic.
    """
    display_name = "Include Jobs"

# Possible logic options:
# - Include Number Trader
# - Include Secret Area
# - Overworld Item Restrictions
# - Cybermetro Locked Shortcuts


class TradeQuestHinting(Choice):
    """
    Whether NPCs offering Chip Trades should show what item they provide.
    None - NPCs will not provide any information on what item they will give
    Partial - NPCs will state if an item is progression or not, but not the specific item
    Full - NPCs will state what item they will give, providing an Archipelago Hint when doing so
    """
    display_name = "Trade Quest Hinting"
    option_none = 0
    option_partial = 1
    option_full = 2
    default = 2


MMBN3Options = {
    "extra_ranks": ExtraRanks,
    "include_jobs": IncludeJobs,
    "trade_quest_hinting": TradeQuestHinting,
}
