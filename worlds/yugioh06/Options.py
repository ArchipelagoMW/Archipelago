import typing
from Options import Option, Choice, Range


class StructureDeck(Choice):
    display_name = "Structure Deck"
    option_dragons_roar = 0
    option_zombie_madness = 1
    option_blazing_destruction = 2
    option_fury_from_the_deep = 3
    option_warriors_triumph = 4
    option_spellcasters_judgement = 5


class Banlist(Choice):
    display_name = "Banlist"
    option_no_banlist = 0
    option_September_2003 = 1
    option_March_2004 = 2
    option_September_2004 = 3
    option_March_2005 = 4
    option_September_2005 = 5


class FinalCampaignBossChallenges(Range):
    """Number of required Limited/Theme Duels completed for the Final Campaign Boss to appear"""
    display_name = "Final Campaign Boss unlock amount"
    range_start = 0
    range_end = 91
    default = 20


class FourthTier5CampaignBossChallenges(Range):
    display_name = "Fourth Tier 5 Campaign Boss unlock amount"
    range_start = 0
    range_end = 91
    default = 15


class ThirdTier5CampaignBossChallenges(Range):
    display_name = "Third Tier 5 Campaign Boss unlock amount"
    range_start = 0
    range_end = 91
    default = 10


ygo06_options: typing.Dict[str, type(Option)] = {
    "StructureDeck": StructureDeck,
    "Banlist": Banlist,
    "FinalCampaignBossChallenges": FinalCampaignBossChallenges,
    "FourthTier5CampaignBossChallenges": FourthTier5CampaignBossChallenges,
    "ThirdTier5CampaignBossChallenges": ThirdTier5CampaignBossChallenges
}