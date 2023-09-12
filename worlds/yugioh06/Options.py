import typing
from Options import Option, Choice, Range, Toggle


class StructureDeck(Choice):
    """Which Structure Deck you start with"""
    display_name = "Structure Deck"
    option_dragons_roar = 0
    option_zombie_madness = 1
    option_blazing_destruction = 2
    option_fury_from_the_deep = 3
    option_warriors_triumph = 4
    option_spellcasters_judgement = 5
    default = "random"


class Banlist(Choice):
    """Which Banlist you start with"""
    display_name = "Banlist"
    option_no_banlist = 0
    option_September_2003 = 1
    option_March_2004 = 2
    option_September_2004 = 3
    option_March_2005 = 4
    option_September_2005 = 5
    default = option_September_2005


class FinalCampaignBossChallenges(Range):
    """Number of Limited/Theme Duels completed for the Final Campaign Boss to appear"""
    display_name = "Final Campaign Boss unlock amount"
    range_start = 0
    range_end = 91
    default = 20


class FourthTier5CampaignBossChallenges(Range):
    """Number of Limited/Theme Duels completed for the Forth Level 5 Campaign Opponent to appear"""
    display_name = "Fourth Tier 5 Campaign Boss unlock amount"
    range_start = 0
    range_end = 91
    default = 15


class ThirdTier5CampaignBossChallenges(Range):
    """Number of Limited/Theme Duels completed for the Third Level 5 Campaign Opponent to appear"""
    display_name = "Third Tier 5 Campaign Boss unlock amount"
    range_start = 0
    range_end = 91
    default = 10


class StartingMoney(Range):
    """The amount of money you start with"""
    display_name = "Starting Money"
    range_start = 0
    range_end = 99999999
    default = 3000


class MoneyRewardMultiplier(Range):
    """By which amount the campaign reward money is multiplied"""
    display_name = "Money Reward Multiplier"
    range_start = 1
    range_end = 255
    default = 10


class NormalizeBoostersPacks(Toggle):
    """If enabled every booster pack costs the same otherwise vanilla cost is used"""
    display_name = "Normalize Booster Packs"


class BoosterPackPrices(Range):
    """
    Only Works if normalize booster packs is enabled.
    Sets the amount that what every booster pack costs.
    """
    display_name = "Booster Pack Prices"
    range_start = 1
    range_end = 3000
    default = 300


ygo06_options: typing.Dict[str, type(Option)] = {
    "StructureDeck": StructureDeck,
    "Banlist": Banlist,
    "FinalCampaignBossChallenges": FinalCampaignBossChallenges,
    "FourthTier5CampaignBossChallenges": FourthTier5CampaignBossChallenges,
    "ThirdTier5CampaignBossChallenges": ThirdTier5CampaignBossChallenges,
    "StartingMoney": StartingMoney,
    "MoneyRewardMultiplier": MoneyRewardMultiplier,
    "NormalizeBoostersPacks": NormalizeBoostersPacks,
    "BoosterPackPrices": BoosterPackPrices
}