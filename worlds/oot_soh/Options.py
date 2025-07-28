from dataclasses import dataclass
from Options import Choice, Toggle, Range, PerGameCommonOptions, StartInventoryPool

class ClosedForest(Choice):
    """
    
    """
    display_name = "Closed Forest"
    option_on = 0
    option_deku_only = 1
    option_off = 2
    default = 2

class KakarikoGate(Choice):
    """
    
    """
    display_name = "Kakariko Gate"
    option_closed = 0
    option_open = 1
    default = 1

class DoorOfTime(Choice):
    """
    
    """
    display_name = "Door of Time"
    option_closed = 0
    option_song_only = 1
    option_open = 2
    default = 2

class ZorasFountain(Choice):
    """
    
    """
    display_name = "Zora's Domain"
    option_closed = 0
    option_closed_as_child = 1
    option_open = 2
    default = 1

class SleepingWaterfall(Choice):
    """
    
    """
    display_name = "Sleeping Waterfall"
    option_closed = 0
    option_open = 1
    default = 0

class JabuJabu(Choice):
    """
    
    """
    display_name = "Jabu-Jabu"
    option_closed = 0
    option_open = 1
    default = 0

class LockOverworldDoors(Toggle):
    """
    
    """
    display_name = "Lock Overworld Doors"

class FortressCarpenters(Choice):
    """
    
    """
    display_name = "Fortress Carpenters"
    option_normal = 0
    option_fast = 1
    option_free = 2
    default = 1

class RainbowBridge(Choice):
    """
    
    """
    display_name = "Rainbow Bridge"
    option_vanilla = 0
    option_always_open = 1
    option_stones = 2
    option_medallions = 3
    option_dungeon_rewards = 4
    option_dungeons = 5
    option_tokens = 6
    option_greg = 7
    default = 7

class RainbowBridgeStonesRequired(Range):
    """
    If Rainbow Bridge is set to stones, this is how many Spiritual Stones are required to open it.
    """
    display_name = "Rainbow Bridge Stones Required"
    range_start = 1
    range_end = 3
    default = 3

class RainbowBridgeMedallionsRequired(Range):
    """
    
    """
    display_name = "Rainbow Bridge Medallions Required"
    range_start = 1
    range_end = 6
    default = 6

class RainbowBridgeDungeonRewardsRequired(Range):
    """
    
    """
    display_name = "Rainbow Bridge Dungeon Rewards Required"
    range_start = 1
    range_end = 9
    default = 9

class RainbowBridgeDungeonsRequired(Range):
    """
    
    """
    display_name = "Rainbow Bridge Dungeons Required"
    range_start = 1
    range_end = 8
    default = 8

class RainbowBridgeSkullTokensRequired(Range):
    """
    
    """
    display_name = "Rainbow Bridge Skull Tokens Required"
    range_start = 1
    range_end = 100
    default = 50

class GanonsTrialsRequired(Range):
    """
    
    """
    display_name = "Ganon's Trials Required"
    range_start = 0
    range_end = 6
    default = 0

class TriforceHunt(Toggle):
    """
    
    """
    display_name = "Triforce Hunt"

class TriforceHuntRequiredPieces(Range):
    """
    
    """
    display_name = "Triforce Hunt Required Pieces"
    range_start = 1
    range_end = 100
    default = 20

class TriforceHuntExtraPiecesPercentage(Range):
    """
    
    """
    display_name = "Triforce Hunt Extra Pieces Percentage"
    range_start = 0
    range_end = 100
    default = 50

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

class ShuffleMasterSword(Toggle):
    """
    
    """
    display_name = "Shuffle Master Sword"

class ShuffleChildsWallet(Toggle):
    """
    
    """
    display_name = "Shuffle Child's Wallet"

class ShuffleOcarinaButtons(Toggle):
    """
    
    """
    display_name = "Shuffle Ocarina Buttons"

class ShuffleSwim(Toggle):
    """
    
    """
    display_name = "Shuffle Swim"

class ShuffleWeirdEgg(Toggle):
    """
    
    """
    display_name = "Shuffle Weird Egg"

class ShuffleFishingPole(Toggle):
    """
    
    """
    display_name = "Shuffle Fishing Pole"

class ShuffleDekuStickBag(Toggle):
    """
    
    """
    display_name = "Shuffle Deku Stick Bag"

class ShuffleDekuNutBag(Toggle):
    """
    
    """
    display_name = "Shuffle Deku Nut Bag"

class ShuffleFreestandingItems(Choice):
    """
    Shuffle freestanding items. IF this is turned off, freestanding pieces of heart are still randomized.
    """
    display_name = "Shuffle Freestanding Items"
    option_off = 0
    option_dungeon = 1
    option_overworld = 2
    option_all = 3
    default = 0

class ShuffleShops(Toggle):
    """
    Shuffle the 4 left items in every shop. Randomized items cost 10 rupees. The other 4 shop items stay vanilla.
    """
    display_name = "Shuffle Shops"

class ShuffleFish(Choice):
    """
    Shuffle fish. Fishing pond fish will have 15 fish for each age. Overworld fish need a bottle to scoop up. Hylian Loach is not included.
    """
    display_name = "Shuffle Fish"
    option_off = 0
    option_pond = 1
    option_overworld = 2
    option_all = 3
    default = 0

class ShuffleScrubs(Toggle):
    """
    Shuffles all Deku Scrub merchants in the game. Randomized items cost 10 rupees.
    """
    display_name = "Shuffle Scrubs"

class ShuffleBeehives(Toggle):
    """
    Shuffle all beehives.
    """
    display_name = "Shuffle Beehives"

class ShuffleCows(Toggle):
    """
    Randomize what cows will give when playing Epona's Song for them for the first time.
    """
    display_name = "Shuffle Cows"

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

class ShuffleMerchants(Choice):
    """
    
    """
    display_name = "Shuffle Merchants"
    option_off = 0
    option_bean_merchant_only = 1
    option_all_but_beans = 2
    option_all = 3
    default = 0

class ShuffleFrogSongRupees(Toggle):
    """
    Shuffle the purple rupee rewards from the frogs in Zora's River. If this is turned off, only the Song of Storms and Frog Minigame rewards are shuffled.
    """
    display_name = "Shuffle Frog Song Rupees"

class ShuffleAdultTradeItems(Toggle):
    """
    Adds all adult trade quest items to the pool. If this is turned off, only the Claim Check is in the pool.
    """
    display_name = "Shuffle Adult Trade Items"

class ShuffleBossSouls(Choice):
    """
    
    """
    display_name = "Shuffle Boss Souls"
    option_off = 0
    option_on = 1
    option_on_plus_ganons = 2
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

class ShuffleDungeonRewards(Choice):
    """
    Shuffle dungeon rewards to be vanilla, shuffled between dungeons, or anywhere. If not turned on, dungeon rewards will be on their vanilla location.
    """
    display_name = "Shuffle Dungeon Rewards"
    option_off = 0
    option_dungeons = 1
    option_anywhere = 2
    default = 0

class MapsAndCompasses(Choice):
    """
    
    """
    display_name = "Maps and Compasses"
    option_start_with = 0
    option_shuffle = 1
    default = 0

class GanonsCastleBossKey(Choice):
    """
    
    """
    display_name = "Ganons Castle Boss Key"
    option_vanilla = 0
    option_anywhere = 1
    option_lacs_vanilla = 2
    option_lacs_stones = 3
    option_lacs_medallions = 4
    option_lacs_dungeon_rewards = 5
    option_lacs_dungeons = 6
    option_lacs_skull_tokens = 7
    default = 5

class GanonsCastleBossKeyStonesRequired(Range):
    """
    If Ganon's Boss Key is set to stones, this is how many Spiritual Stones are required to open it.
    Once the required amount is reached, the boss key will be granted through the Light Arrow cutscene in the Temple of Time.
    """
    display_name = "Ganons Castle Boss Key Stones Required"
    range_start = 1
    range_end = 3
    default = 3

class GanonsCastleBossKeyMedallionsRequired(Range):
    """
    
    """
    display_name = "Ganons Castle Boss Key Medallions Required"
    range_start = 1
    range_end = 6
    default = 6

class GanonsCastleBossKeyDungeonRewardsRequired(Range):
    """
    
    """
    display_name = "Ganons Castle Boss Key Dungeon Rewards Required"
    range_start = 1
    range_end = 9
    default = 6

class GanonsCastleBossKeyDungeonsRequired(Range):
    """
    
    """
    display_name = "Ganons Castle Boss Key Dungeons Required"
    range_start = 1
    range_end = 8
    default = 8

class GanonsCastleBossKeySkullTokensRequired(Range):
    """
    
    """
    display_name = "Ganons Castle Boss Key Skull Tokens Required"
    range_start = 1
    range_end = 100
    default = 50

class KeyRings(Toggle):
    """
    
    """
    display_name = "Key Rings"

class BigPoeTargetCount(Range):
    """
    
    """
    display_name = "Big Poe Target Count"
    range_start = 0
    range_end = 10
    default = 1

class SkipChildZelda(Toggle):
    """
    
    """
    display_name = "Skip Child Zelda"
    default = 1

class SkipEponaRace(Toggle):
    """
    
    """
    display_name = "Skip Epona Zelda"
    default = 1

class CompleteMaskQuest(Toggle):
    """
    
    """
    display_name = "Complete Mask Quest"
    default = 1

class SkipScarecrowsSong(Toggle):
    """
    
    """
    display_name = "Skip Scarecrow's Song"
    default = 1

class FullWallets(Toggle):
    """
    
    """
    display_name = "Full Wallets"
    default = 1

class BombchuBag(Toggle):
    """
    
    """
    display_name = "Bombchu Bag"

class BombchuDrops(Toggle):
    """
    
    """
    display_name = "Bombchu Drops"
    default = 1

class BlueFireArrows(Toggle):
    """
    
    """
    display_name = "Blue Fire Arrows"
    default = 1

class SunlightArrows(Toggle):
    """
    
    """
    display_name = "Sunlight Arrows"
    default = 1

class InfiniteUpgrades(Choice):
    """
    
    """
    display_name = "Infinite Upgrades"
    option_off = 0
    option_progressive = 1
    option_condensed_progressive = 2
    default = 0

class SkeletonKey(Toggle):
    """
    
    """
    display_name = "Skeleton Key"

@dataclass
class SohOptions(PerGameCommonOptions):
    closed_forest: ClosedForest
    kakariko_gate: KakarikoGate
    door_of_time: DoorOfTime
    zoras_fountain: ZorasFountain
    sleeping_waterfall: SleepingWaterfall
    jabu_jabu: JabuJabu
    lock_overworld_doors: LockOverworldDoors
    fortress_carpenters: FortressCarpenters
    rainbow_bridge: RainbowBridge
    rainbow_bridge_stones_required: RainbowBridgeStonesRequired
    rainbow_bridge_medallions_required: RainbowBridgeMedallionsRequired
    rainbow_bridge_dungeon_rewards_required: RainbowBridgeDungeonRewardsRequired
    rainbow_bridge_dungeons_required: RainbowBridgeDungeonsRequired
    rainbow_bridge_skull_tokens_required: RainbowBridgeSkullTokensRequired
    ganons_trials_required: GanonsTrialsRequired
    triforce_hunt: TriforceHunt
    triforce_hunt_required_pieces: TriforceHuntRequiredPieces
    triforce_hunt_extra_pieces_percentage: TriforceHuntExtraPiecesPercentage
    shuffle_skull_tokens: ShuffleTokens
    shuffle_master_sword: ShuffleMasterSword
    shuffle_childs_wallet: ShuffleChildsWallet
    shuffle_ocarina_buttons: ShuffleOcarinaButtons
    shuffle_swim: ShuffleSwim
    shuffle_weird_egg: ShuffleWeirdEgg
    shuffle_fishing_pole: ShuffleFishingPole
    shuffle_deku_stick_bag: ShuffleDekuStickBag
    shuffle_deku_nut_bag: ShuffleDekuNutBag
    shuffle_freestanding_items: ShuffleFreestandingItems
    shuffle_shops: ShuffleShops
    shuffle_fish: ShuffleFish
    shuffle_scrubs: ShuffleScrubs
    shuffle_beehives: ShuffleBeehives
    shuffle_cows: ShuffleCows
    shuffle_pots: ShufflePots
    shuffle_crates: ShuffleCrates
    shuffle_merchants: ShuffleMerchants
    shuffle_frog_song_rupees: ShuffleFrogSongRupees
    shuffle_adult_trade_items: ShuffleAdultTradeItems
    shuffle_boss_souls: ShuffleBossSouls
    shuffle_fairies: ShuffleFairies
    shuffle_grass: ShuffleGrass
    shuffle_dungeon_rewards: ShuffleDungeonRewards
    maps_and_compasses: MapsAndCompasses
    ganons_castle_boss_key: GanonsCastleBossKey
    ganons_castle_boss_key_stones_required: GanonsCastleBossKeyStonesRequired
    ganons_castle_boss_key_medallions_required: GanonsCastleBossKeyMedallionsRequired
    ganons_castle_boss_key_dungeon_rewards_required: GanonsCastleBossKeyDungeonRewardsRequired
    ganons_castle_boss_key_dungeons_required: GanonsCastleBossKeyDungeonsRequired
    ganons_castle_boss_key_skull_tokens_required: GanonsCastleBossKeySkullTokensRequired
    key_rings: KeyRings
    big_poe_target_count: BigPoeTargetCount
    skip_child_zelda: SkipChildZelda
    skip_epona_race: SkipEponaRace
    complete_mask_quest: CompleteMaskQuest
    skip_scarecrows_song: SkipScarecrowsSong
    full_wallets: FullWallets
    bombchu_bag: BombchuBag
    bombchu_drops: BombchuDrops
    blue_fire_arrows: BlueFireArrows
    sunlight_arrows: SunlightArrows
    infinite_upgrades: InfiniteUpgrades
    skeleton_key: SkeletonKey
