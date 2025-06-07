from dataclasses import dataclass
from Options import Choice, Toggle, Range, PerGameCommonOptions, StartInventoryPool


class DeathLink(Toggle):
    """
    You die, others die. Others die, you die!
    """
    display_name = "Death Link"

class ShuffleDungeonRewards(Choice):
    """
    Shuffle dungeon rewards to be vanilla, shuffled between dungeons, or anywhere. If not turned on, dungeon rewards will be on their vanilla location.
    """
    display_name = "Shuffle Dungeon Rewards"
    option_off = 0
    option_dungeons = 1
    option_anywhere = 2
    default = 0

class GanonsCastleBossKeySetting(Choice):
    """
    Choose wether Ganon's Castle Boss key is placed anywhere, or upon reaching a requirement. Once the requirements are reached, it'll be granted in the Temple of Time.
    """
    display_name = "Ganons Castle Boss Key Setting"
    option_dungeon_rewards = 0
    option_anywhere = 1
    default = 0

class GanonsCastleBossKeyRewardsRequired(Range):
    """
    Choose how many dungeon rewards are required to receive GCBK when set to require dungeon rewards.
    """
    display_name = "Ganons Castle Boss Key Dungeons Required"
    range_start = 1
    range_end = 9
    default = 6

class ShuffleTokens(Choice):
    """
    Shuffle Gold Skulltula tokens.
    """
    display_name = "Shuffle Tokens"
    option_off = 0
    option_dungeon = 1
    option_overworld = 2
    option_all = 3
    default = 0

class ShuffleShops(Toggle):
    """
    Shuffle the 4 left items in every shop. Randomized items are free. The other 4 shop items stay vanilla.
    """
    display_name = "Shuffle Shops"

class ShuffleScrubs(Toggle):
    """
    Shuffles all Deku Scrub merchants in the game. Randomized items are free.
    """
    display_name = "Shuffle Scrubs"

class ShuffleTradeItems(Toggle):
    """
    Adds all trade quest items to the pool. If this is turned off, only the Claim Check is in the pool.
    """
    display_name = "Shuffle Trade Items"

class ShuffleMerchants(Toggle):
    """
    Randomize what the bean merchant, Granny's shop, Medigoron and the Wasteland Carpet Merchant sell.
    """
    display_name = "Shuffle Merchants"

class ShuffleCows(Toggle):
    """
    Randomize what cows will give when playing Epona's Song for them for the first time.
    """
    display_name = "Shuffle Cows"

class ShuffleFrogs(Toggle):
    """
    Shuffle the purple rupee rewards from the frogs in Zora's River. If this is turned off, only the Song of Storms and Frog Minigame rewards are shuffled.
    """
    display_name = "Shuffle Frogs"

class ShuffleBeehives(Toggle):
    """
    Shuffle all beehives.
    """
    display_name = "Shuffle Beehives"

class ShufflePots(Choice):
    """
    Shuffle pot drops.
    """
    display_name = "Shuffle Pots"
    option_off = 0
    option_dungeon = 1
    option_overworld = 2
    option_all = 3
    default = 0

class ShuffleCrates(Choice):
    """
    Shuffle small and large crate drops.
    """
    display_name = "Shuffle Crates"
    option_off = 0
    option_dungeon = 1
    option_overworld = 2
    option_all = 3
    default = 0

class ShuffleFreestanding(Choice):
    """
    Shuffle freestanding items. IF this is turned off, freestanding pieces of heart are still randomized.
    """
    display_name = "Shuffle Freestanding"
    option_off = 0
    option_dungeon = 1
    option_overworld = 2
    option_all = 3
    default = 0

class ShuffleFairies(Toggle):
    """
    Shuffle fairies from wonder spots, playing Song of Storms and other regular songs for Gossip Stones and in Fairy Fountains.
    """
    display_name = "Shuffle Fairies"

class ShuffleGrass(Choice):
    """
    Shuffle grass drops.
    """
    display_name = "Shuffle Grass"
    option_off = 0
    option_dungeon = 1
    option_overworld = 2
    option_all = 3
    default = 0

class ShuffleFish(Choice):
    """
    Shuffle fish. Fishing pond fish will have 15 fish for each age. Overworld fish need a bottle to scoop up.
    """
    display_name = "Shuffle Fish"
    option_off = 0
    option_pond = 1
    option_overworld = 2
    option_all = 3
    default = 0

@dataclass
class SohOptions(PerGameCommonOptions):
    death_link: DeathLink
    shuffle_dungeon_rewards: ShuffleDungeonRewards
    gcbk_setting: GanonsCastleBossKeySetting
    gcbk_rewards_required: GanonsCastleBossKeyRewardsRequired
    shuffle_tokens: ShuffleTokens
    shuffle_shops: ShuffleShops
    shuffle_scrubs: ShuffleScrubs
    shuffle_trade_items: ShuffleTradeItems
    shuffle_merchants: ShuffleMerchants
    shuffle_cows: ShuffleCows
    shuffle_frogs: ShuffleFrogs
    shuffle_beehives: ShuffleBeehives
    shuffle_pots: ShufflePots
    shuffle_crates: ShuffleCrates
    shuffle_freestanding: ShuffleFreestanding
    shuffle_fairies: ShuffleFairies
    shuffle_grass: ShuffleGrass
    shuffle_fish: ShuffleFish
