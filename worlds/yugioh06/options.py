from dataclasses import dataclass

from Options import Choice, DefaultOnToggle, PerGameCommonOptions, Range, Toggle


class StructureDeck(Choice):
    """Which Structure Deck you start with"""

    display_name = "Structure Deck"
    option_dragons_roar = 0
    option_zombie_madness = 1
    option_blazing_destruction = 2
    option_fury_from_the_deep = 3
    option_warriors_triumph = 4
    option_spellcasters_judgement = 5
    option_none = 6
    option_random_deck = 7
    default = 7


class Banlist(Choice):
    """Which Banlist you start with"""

    display_name = "Banlist"
    option_no_banlist = 0
    option_september_2003 = 1
    option_march_2004 = 2
    option_september_2004 = 3
    option_march_2005 = 4
    option_september_2005 = 5
    default = option_september_2005


class FinalCampaignBossUnlockCondition(Choice):
    """How to unlock the final campaign boss and goal for the world"""

    display_name = "Final Campaign Boss unlock Condition"
    option_campaign_opponents = 0
    option_challenges = 1


class FourthTier5UnlockCondition(Choice):
    """How to unlock the fourth campaign boss"""

    display_name = "Fourth Tier 5 Campaign Boss unlock Condition"
    option_campaign_opponents = 0
    option_challenges = 1


class ThirdTier5UnlockCondition(Choice):
    """How to unlock the third campaign boss"""

    display_name = "Third Tier 5 Campaign Boss unlock Condition"
    option_campaign_opponents = 0
    option_challenges = 1


class FinalCampaignBossChallenges(Range):
    """Number of Limited/Theme Duels completed for the Final Campaign Boss to appear"""

    display_name = "Final Campaign Boss challenges unlock amount"
    range_start = 0
    range_end = 91
    default = 10


class FourthTier5CampaignBossChallenges(Range):
    """Number of Limited/Theme Duels completed for the Fourth Level 5 Campaign Opponent to appear"""

    display_name = "Fourth Tier 5 Campaign Boss unlock amount"
    range_start = 0
    range_end = 91
    default = 5


class ThirdTier5CampaignBossChallenges(Range):
    """Number of Limited/Theme Duels completed for the Third Level 5 Campaign Opponent to appear"""

    display_name = "Third Tier 5 Campaign Boss unlock amount"
    range_start = 0
    range_end = 91
    default = 2


class FinalCampaignBossCampaignOpponents(Range):
    """Number of Campaign Opponents Duels defeated for the Final Campaign Boss to appear"""

    display_name = "Final Campaign Boss campaign opponent unlock amount"
    range_start = 0
    range_end = 24
    default = 12


class FourthTier5CampaignBossCampaignOpponents(Range):
    """Number of Campaign Opponents Duels defeated for the Fourth Level 5 Campaign Opponent to appear"""

    display_name = "Fourth Tier 5 Campaign Boss campaign opponent unlock amount"
    range_start = 0
    range_end = 23
    default = 7


class ThirdTier5CampaignBossCampaignOpponents(Range):
    """Number of Campaign Opponents Duels defeated for the Third Level 5 Campaign Opponent to appear"""

    display_name = "Third Tier 5 Campaign Boss campaign opponent unlock amount"
    range_start = 0
    range_end = 22
    default = 3


class NumberOfChallenges(Range):
    """Number of random Limited/Theme Duels that are included. The rest will be inaccessible."""

    display_name = "Number of Challenges"
    range_start = 0
    range_end = 91
    default = 10


class StartingMoney(Range):
    """The amount of money you start with"""

    display_name = "Starting Money"
    range_start = 0
    range_end = 100000
    default = 3000


class MoneyRewardMultiplier(Range):
    """By which amount the campaign reward money is multiplied"""

    display_name = "Money Reward Multiplier"
    range_start = 1
    range_end = 255
    default = 20


class NormalizeBoostersPacks(DefaultOnToggle):
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
    default = 100


class AddEmptyBanList(Toggle):
    """Adds a Ban List where everything is at 3 to the item pool"""

    display_name = "Add Empty Ban List"


class CampaignOpponentsShuffle(Toggle):
    """Replaces the campaign with random opponents from the entire game"""

    display_name = "Campaign Opponents Shuffle"


class OCGArts(Toggle):
    """Always use the OCG artworks for cards"""

    display_name = "OCG Arts"


@dataclass
class Yugioh06Options(PerGameCommonOptions):
    structure_deck: StructureDeck
    banlist: Banlist
    final_campaign_boss_unlock_condition: FinalCampaignBossUnlockCondition
    fourth_tier_5_campaign_boss_unlock_condition: FourthTier5UnlockCondition
    third_tier_5_campaign_boss_unlock_condition: ThirdTier5UnlockCondition
    final_campaign_boss_challenges: FinalCampaignBossChallenges
    fourth_tier_5_campaign_boss_challenges: FourthTier5CampaignBossChallenges
    third_tier_5_campaign_boss_challenges: ThirdTier5CampaignBossChallenges
    final_campaign_boss_campaign_opponents: FinalCampaignBossCampaignOpponents
    fourth_tier_5_campaign_boss_campaign_opponents: FourthTier5CampaignBossCampaignOpponents
    third_tier_5_campaign_boss_campaign_opponents: ThirdTier5CampaignBossCampaignOpponents
    number_of_challenges: NumberOfChallenges
    starting_money: StartingMoney
    money_reward_multiplier: MoneyRewardMultiplier
    normalize_boosters_packs: NormalizeBoostersPacks
    booster_pack_prices: BoosterPackPrices
    add_empty_banlist: AddEmptyBanList
    campaign_opponents_shuffle: CampaignOpponentsShuffle
    ocg_arts: OCGArts
