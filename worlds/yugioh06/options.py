import typing
from dataclasses import dataclass

from Options import Choice, DefaultOnToggle, PerGameCommonOptions, Range, Toggle, OptionDict
from worlds.yugioh06.card_data import get_all_valid_cards_set


class StructureDeck(Choice):
    """
    Which Structure Deck you start with.
    The first 6 are regular Structure Decks
    Worst: Start you of with basically nothing
    Random Deck: Chooses one of the Regular SDs at random.
    Random Singles: Your deck contains 40 completely random cards with no duplicates.
    Random Playsets: Your deck contains 14 completely random playsets of 3.
    Custom: Create your own starting deck see Custom Structure Deck for more details.
    """

    display_name = "Structure Deck"
    option_dragons_roar = 0
    option_zombie_madness = 1
    option_blazing_destruction = 2
    option_fury_from_the_deep = 3
    option_warriors_triumph = 4
    option_spellcasters_judgement = 5
    option_worst = 6
    option_random_deck = 7
    option_random_singles = 8
    option_random_playsets = 9
    option_custom = 10
    default = 7


class CustomStructureDeck(OptionDict):
    """
    Create your own Structure Deck to start with
    Only works if structure deck is set to custom
    Has to be below 80 cards in total.
    Fusion monsters don't work properly you have to add them to your Trunk and then back into the deck.
    """
    display_name = "Custom Structure Deck"
    valid_keys = get_all_valid_cards_set()

    def __init__(self, value: typing.Dict[str, int]):
        if any(amount is None for amount in value.values()):
            raise Exception("Cards must have amounts associated with them. Please provide positive integer values in the format \"card\": amount .")
        if any(amount < 1 for amount in value.values()):
            raise Exception("Cannot have non-positive card amounts.")
        if any(amount > 3 for amount in value.values()):
            raise Exception("Cannot have more than 3 of the same card.")
        if sum(value.values()) > 80:
            raise Exception("The Structure Deck cannot have more than 80 cards.")
        super(CustomStructureDeck, self).__init__(value)


class StarterDeck(Choice):
    """
    What are the cards you start with in the Trunk
    Vanilla: Default starting cards.
    Remove: Start with no cards in Trunk.
    Random Singles: Start with 40 random cards with no duplicates.
    Random Playsets: Start with 13 random playsets of 3.
    Custom: Choose your own cards. For more details see Custom Starter Deck.
    """
    display_name = "Starter Deck"
    option_vanilla = 0
    option_remove = 1
    option_random_singles = 2
    option_random_playsets = 3
    option_custom = 4
    default = 0


class CustomStarterDeck(OptionDict):
    """
    Choose the cards that you have in your trunk at the start of the game
    Only works if starter deck is set to custom.
    Must be below 40 cards in total.
    """
    display_name = "Custom Starter Deck"
    valid_keys = get_all_valid_cards_set()

    def __init__(self, value: typing.Dict[str, int]):
        if any(amount is None for amount in value.values()):
            raise Exception("Cards must have amounts associated with them. Please provide positive integer values in the format \"card\": amount .")
        if any(amount < 1 for amount in value.values()):
            raise Exception("Cannot have non-positive card amounts.")
        if any(amount > 3 for amount in value.values()):
            raise Exception("Cannot have more than 3 of the same card.")
        if sum(value.values()) > 40:
            raise Exception("The Starter Deck cannot have more than 40 cards.")
        super(CustomStarterDeck, self).__init__(value)


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


class FinalCampaignBossChallenges(Range):
    """Number of Limited/Theme Duels completed for the Final Campaign Boss to appear"""

    display_name = "Final Campaign Boss challenges unlock amount"
    range_start = 0
    range_end = 91
    default = 3


class FourthTier5CampaignBossChallenges(Range):
    """Number of Limited/Theme Duels completed for the Fourth Level 5 Campaign Opponent to appear"""

    display_name = "Fourth Tier 5 Campaign Boss unlock amount"
    range_start = 0
    range_end = 91
    default = 2


class ThirdTier5CampaignBossChallenges(Range):
    """Number of Limited/Theme Duels completed for the Third Level 5 Campaign Opponent to appear"""

    display_name = "Third Tier 5 Campaign Boss unlock amount"
    range_start = 0
    range_end = 91
    default = 1


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


class NormalizeBoosterPackPrices(DefaultOnToggle):
    """If enabled every booster pack costs the same and has 5 cards per pack otherwise vanilla cost is used"""

    display_name = "Normalize Booster Pack Prices"


class BoosterPackPrices(Range):
    """
    Only Works if normalize booster packs is enabled.
    Sets the amount that what every booster pack costs.
    """

    display_name = "Booster Pack Prices"
    range_start = 1
    range_end = 3000
    default = 100


class NormalizeBoosterPackRarities(Toggle):
    """All cards in packs are commons"""
    display_name = "Normalize Booster Pack Rarities"


class RandomizePackContents(Choice):
    """Randomize the contents of the Booster Packs"""
    display_name = "Randomize Pack Contents"
    option_vanilla = 0
    option_shuffle = 1
    option_chaos = 2


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
    starter_deck: StarterDeck
    banlist: Banlist
    final_campaign_boss_challenges: FinalCampaignBossChallenges
    fourth_tier_5_campaign_boss_challenges: FourthTier5CampaignBossChallenges
    third_tier_5_campaign_boss_challenges: ThirdTier5CampaignBossChallenges
    final_campaign_boss_campaign_opponents: FinalCampaignBossCampaignOpponents
    fourth_tier_5_campaign_boss_campaign_opponents: FourthTier5CampaignBossCampaignOpponents
    third_tier_5_campaign_boss_campaign_opponents: ThirdTier5CampaignBossCampaignOpponents
    number_of_challenges: NumberOfChallenges
    starting_money: StartingMoney
    money_reward_multiplier: MoneyRewardMultiplier
    normalize_booster_pack_prices: NormalizeBoosterPackPrices
    booster_pack_prices: BoosterPackPrices
    normalize_booster_pack_rarities: NormalizeBoosterPackRarities
    randomize_pack_contents: RandomizePackContents
    add_empty_banlist: AddEmptyBanList
    campaign_opponents_shuffle: CampaignOpponentsShuffle
    ocg_arts: OCGArts
    custom_structure_deck: CustomStructureDeck
    custom_starter_deck: CustomStarterDeck
