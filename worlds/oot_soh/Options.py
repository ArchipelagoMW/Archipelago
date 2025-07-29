from dataclasses import dataclass
from Options import Choice, Toggle, Range, PerGameCommonOptions, StartInventoryPool

class ClosedForest(Choice):
    """
    On - Kokiri Sword & Deku Shield are required to access the Deku Tree, and completing the Deku Tree is required to access the Lost Woods Bridge Exit.
    Deku Only - Kokiri boy no longer blocks the path to the Bridge but Mido still requires the Kokiri Sword and Deku Shield to access the tree.
    Off - Mido no longer blocks the path to the Deku Tree. Kokiri boy no longer blocks the path out of the forest.
    """
    display_name = "Closed Forest"
    option_on = 0
    option_deku_only = 1
    option_off = 2
    default = 2

class KakarikoGate(Choice):
    """
    Closed - The gate will remain closed until Zelda's Letter is shown to the guard.
    Open - The gate is always open. The Happy Mask Shop will open immediately after obtaining Zelda's Letter.
    """
    display_name = "Kakariko Gate"
    option_closed = 0
    option_open = 1
    default = 1

class DoorOfTime(Choice):
    """
    Closed - The Ocarina of Time, the Song of Time and all three Spiritual Stones are required to open the Door of Time.
    Song only - Play the Song of Time in front of the Door of Time to open it.
    Open - The Door of Time is permanently open with no requirements.
    """
    display_name = "Door of Time"
    option_closed = 0
    option_song_only = 1
    option_open = 2
    default = 2

class ZorasFountain(Choice):
    """
    Closed - King Zora obstructs the way to Zora's Fountain. Ruto's Letter must be shown as child Link in order to move him in both time periods.
    Closed as child - Ruto's Letter is only required to move King Zora as child Link. Zora's Fountain starts open as adult.
    Open - King Zora has already mweeped out of the way in both time periods. Ruto's Letter is removed from the item pool.
    """
    display_name = "Zora's Domain"
    option_closed = 0
    option_closed_as_child = 1
    option_open = 2
    default = 1

class SleepingWaterfall(Choice):
    """
    Closed - Sleeping Waterfall obstructs the entrance to Zora's Domain. Zelda's Lullaby must be played in order to open it (but only once; then it stays open in both time periods).
    Open - Sleeping Waterfall is always open. Link may always enter Zora's Domain.
    """
    display_name = "Sleeping Waterfall"
    option_closed = 0
    option_open = 1
    default = 0

class JabuJabu(Choice):
    """
    Closed - A fish is required to open Jabu-Jabu's mouth.
    Open - Jabu-Jabu's mouth opens without the need for a fish.
    """
    display_name = "Jabu-Jabu"
    option_closed = 0
    option_open = 1
    default = 0

class LockOverworldDoors(Toggle):
    """
    Add locks to all wooden overworld doors, requiring specific small keys to open them.
    """
    display_name = "Lock Overworld Doors"

class FortressCarpenters(Choice):
    """
    Sets the state of the carpenters captured by Gerudo in Gerudo Fortress, and with it the number of guards that spawn.
    Normal - All 4 carpenters are required to be saved.
    Fast - Only the bottom left carpenter requires rescuing.
    Free - The bridge is repaired from the start, and Nabooru cannot spawn. If the Gerudo Membership Card isn't shuffled, you start with it.
    Only Normal is compatible with Gerudo Fortress Key Rings.
    """
    display_name = "Fortress Carpenters"
    option_normal = 0
    option_fast = 1
    option_free = 2
    default = 1

class RainbowBridge(Choice):
    """
    Alters the requirements to open the bridge to Ganon's Castle.
    Vanilla - Obtain the Shadow Medallion, Spirit Medallion and Light Arrows.
    Always open - No requirements.
    Stones - Obtain the specified amount of Spiritual Stones.
    Medallions - Obtain the specified amount of medallions.
    Dungeon rewards - Obtain the specified total sum of Spiritual Stones or medallions.
    Dungeons - Complete the specified amount of dungeons. Dungeons are considered complete after stepping in to the blue warp after the boss.
    Tokens - Obtain the specified amount of Skulltula tokens.
    Greg - Find Greg the Green Rupee.
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
    If Rainbow Bridge is set to medallions, this is how many medallions are required to open it.
    """
    display_name = "Rainbow Bridge Medallions Required"
    range_start = 1
    range_end = 6
    default = 6

class RainbowBridgeDungeonRewardsRequired(Range):
    """
    If Rainbow Bridge is set to dungeon rewards, this is how many dungeon rewards are required to open it.
    """
    display_name = "Rainbow Bridge Dungeon Rewards Required"
    range_start = 1
    range_end = 9
    default = 9

class RainbowBridgeDungeonsRequired(Range):
    """
    If Rainbow Bridge is set to dungeons, this is how many completed dungeons are required to open it.
    """
    display_name = "Rainbow Bridge Dungeons Required"
    range_start = 1
    range_end = 8
    default = 8

class RainbowBridgeSkullTokensRequired(Range):
    """
    If Rainbow Bridge is set to tokens, this is how many Gold Skulltula Tokens are required to open it.
    """
    display_name = "Rainbow Bridge Skull Tokens Required"
    range_start = 1
    range_end = 100
    default = 50

class GanonsTrialsRequired(Range):
    """
    Sets the number of Ganon's Trials required to dispel the barrier.
    """
    display_name = "Ganon's Trials Required"
    range_start = 0
    range_end = 6
    default = 0

class TriforceHunt(Toggle):
    """
    Pieces of the Triforce of Courage have been scattered across the world. Find them all to finish the game! 
    If this option is enabled, Ganon's Boss Key will not be shuffled and Light Arrow Cutscene (LACS) will revert to its vanilla behavior.
    When the required amount of pieces have been found, the game is saved and Ganon's Boss key is given to you when you load back into the game if you desire to beat Ganon afterwards.
    """
    display_name = "Triforce Hunt"

class TriforceHuntRequiredPieces(Range):
    """
    The amount of Triforce pieces required to win the game.
    """
    display_name = "Triforce Hunt Required Pieces"
    range_start = 1
    range_end = 100
    default = 20

class TriforceHuntExtraPiecesPercentage(Range):
    """
    The percentage of extra Triforce pieces that will be added to the pool. The maximum total Triforce pieces is 100.
    For example:
    If 10 pieces are required, and this option is set to 50%, 5 extra pieces will be added.
    If 20 pieces are required, and this option is set to 100%, 20 extra pieces will be added.
    """
    display_name = "Triforce Hunt Extra Pieces Percentage"
    range_start = 0
    range_end = 100
    default = 50

class ShuffleTokens(Choice):
    """
    Shuffles Golden Skulltula Tokens into the item pool. This means Golden Skulltulas can contain other items as well.
    Off - GS tokens will not be shuffled.
    Dungeons - Only shuffle GS tokens that are within dungeons.
    Overworld - Only shuffle GS tokens that are outside of dungeons.
    All Tokens - Shuffle all 100 GS tokens.
    """
    display_name = "Shuffle Tokens"
    option_off = 0
    option_dungeon = 1
    option_overworld = 2
    option_all = 3
    default = 0

class ShuffleMasterSword(Toggle):
    """
    Shuffles the Master Sword into the item pool.
    If you haven't found the Master Sword before facing Ganon, you won't receive it during the fight.
    """
    display_name = "Shuffle Master Sword"

class ShuffleChildsWallet(Toggle):
    """
    Enabling this shuffles the Child's Wallet into the item pool.
    You will not be able to carry any rupees until you find a wallet.
    """
    display_name = "Shuffle Child's Wallet"

class ShuffleOcarinaButtons(Toggle):
    """
    Enabling this shuffles the Ocarina buttons into the item pool.
    This will require finding the buttons before being able to use them in songs.
    """
    display_name = "Shuffle Ocarina Buttons"

class ShuffleSwim(Toggle):
    """
    Shuffles the ability to Swim into the item pool.
    The ability to swim has to be found as an item (you can still be underwater if you use iron boots).
    If you enter a water entrance without swim you will be respawned on land to prevent infinite death loops.
    If you void out in Water Temple you will immediately be kicked out to prevent a softlock.
    """
    display_name = "Shuffle Swim"

class ShuffleWeirdEgg(Toggle):
    """
    Shuffles the Weird Egg from Malon in to the item pool. Enabling Skip Child Zelda disables this feature.
    The Weird Egg is required to unlock several events:
      - Zelda's Lullaby from Impa
      - Saria's Song in Sacred Forest Meadow
      - Epona's Song and chicken minigame at Lon Lon Ranch
      - Zelda's Letter for Kakariko gate (if set to closed)
      - Happy Mask Shop sidequest
    """
    display_name = "Shuffle Weird Egg"

class ShuffleFishingPole(Toggle):
    """
    Shuffles the fishing pole into the item pool. The fishing pole is required to play the fishing pond minigame.
    """
    display_name = "Shuffle Fishing Pole"

class ShuffleDekuStickBag(Toggle):
    """
    Shuffles the Deku Stick bag into the item pool. The Deku Stick bag is required to hold Deku Sticks.
    """
    display_name = "Shuffle Deku Stick Bag"

class ShuffleDekuNutBag(Toggle):
    """
    Shuffles the Deku Nut bag into the item pool. The Deku Nut bag is required to hold Deku Nuts.
    """
    display_name = "Shuffle Deku Nut Bag"

class ShuffleFreestandingItems(Choice):
    """
    Freestanding rupees & hearts are shuffles to random items. Freestanding heart pieces and small keys are already shuffled by default.
    Off - freestanding rupees & hearts will not be shuffled.
    Dungeons - Only freestanding rupees & hearts that are within dungeons.
    Overworld - Only freestanding rupees & hearts that are outside of dungeons.
    All - Shuffle all freestanding rupees & hearts.
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
    Pots will drop a randomized item the first time they're broken and collected. This does not include the flying pots.
    With this option enabled, Ganon's boss key door is moved further up the stairs to allow access to the pots before obtaining Ganon's Boss Key.
    Off - Pots will not be shuffled.
    Dungeons - Only shuffle pots that are within dungeons.
    Overworld - Only shuffle pots that are outside of dungeons.
    All pots - Shuffle all pots.
    """
    display_name = "Shuffle Pots"
    option_off = 0
    option_dungeon = 1
    option_overworld = 2
    option_all = 3
    default = 0

class ShuffleCrates(Choice):
    """
    Large and small crates will drop a randomized item the first time they're broken and collected.
    Off - Crates will not be shuffled.
    Dungeons - Only shuffle crates that are within dungeons.
    Overworld - Only shuffle crates that are outside of dungeons.
    All Crates - Shuffle all crates.
    """
    display_name = "Shuffle Crates"
    option_off = 0
    option_dungeon = 1
    option_overworld = 2
    option_all = 3
    default = 0

class ShuffleMerchants(Choice):
    """
    This setting governs if the Bean Salesman, Medigoron, Granny and the Carpet Salesman sell a random item.
    Beans Merchant Only - Only the Bean Salesman will have a check, and a pack of Magic Beans will be added to the item pool.
    All But Beans - Medigoron, Granny and the Carpet Salesman will have checks.
    All - Apply both effects.
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
    Shuffles 8 boss souls (one for each blue warp dungeon). A boss will not appear until you collect its respective soul.
    On + Ganon will also hide Ganon and Ganondorf behind a boss soul.
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
    Grass/Bushes will drop a randomized item the first time they're cut and collected.
    Off - Grass/Bushes will not be shuffled.
    Dungeons - Only shuffle grass/bushes that are within dungeons.
    Overworld - Only shuffle grass/bushes that are outside of dungeons.
    All Grass/Bushes - Shuffle all grass/bushes.
    """
    display_name = "Shuffle Grass"
    option_off = 0
    option_dungeon = 1
    option_overworld = 2
    option_all = 3
    default = 0

class ShuffleDungeonRewards(Choice):
    """
    Shuffles the location of Spiritual Stones and medallions.
    Off - Spiritual Stones and medallions will be given in their vanilla location from their respective boss.
    Dungeons - Spiritual Stones and medallions will be given as rewards for beating major dungeons. Link will always start with one stone or medallion.
    Anywhere - Spiritual Stones and medallions can appear anywhere.
    """
    display_name = "Shuffle Dungeon Rewards"
    option_off = 0
    option_dungeons = 1
    option_anywhere = 2
    default = 0

class MapsAndCompasses(Choice):
    """
    Start with - You will start with Maps & Compasses from all dungeons.
    Shuffle - Maps & Compasses can appear anywhere in the world.
    """
    display_name = "Maps and Compasses"
    option_start_with = 0
    option_shuffle = 1
    default = 0

class GanonsCastleBossKey(Choice):
    """
    Vanilla - Ganon's Boss Key will appear in the vanilla location.
    Anywhere - Ganon's Boss Key Key can appear anywhere in the world.
    LACS - These settings put the boss key on the Light Arrow Cutscene location, from Zelda in Temple of Time as adult, with differing requirements:
    - Vanilla: Obtain the Shadow Medallion and Spirit Medallion
    - Stones: Obtain the specified amount of Spiritual Stones.
    - Medallions: Obtain the specified amount of medallions.
    - Dungeon rewards: Obtain the specified total sum of Spiritual Stones or medallions.
    - Dungeons: Complete the specified amount of dungeons. Dungeons are considered complete after stepping in to the blue warp after the boss.
    - Tokens: Obtain the specified amount of Skulltula tokens.
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
    If Ganon's Boss Key is set to medallions, this is how many medallions are required to open it.
    Once the required amount is reached, the boss key will be granted through the Light Arrow cutscene in the Temple of Time.
    """
    display_name = "Ganons Castle Boss Key Medallions Required"
    range_start = 1
    range_end = 6
    default = 6

class GanonsCastleBossKeyDungeonRewardsRequired(Range):
    """
    If Ganon's Boss Key is set to dungeon rewards, this is how many dungeon rewards are required to open it.
    Once the required amount is reached, the boss key will be granted through the Light Arrow cutscene in the Temple of Time.
    """
    display_name = "Ganons Castle Boss Key Dungeon Rewards Required"
    range_start = 1
    range_end = 9
    default = 6

class GanonsCastleBossKeyDungeonsRequired(Range):
    """
    If Ganon's Boss Key is set to dungeons, this is how many dungeon completions are required to open it.
    Once the required amount is reached, the boss key will be granted through the Light Arrow cutscene in the Temple of Time.
    """
    display_name = "Ganons Castle Boss Key Dungeons Required"
    range_start = 1
    range_end = 8
    default = 8

class GanonsCastleBossKeySkullTokensRequired(Range):
    """
    If Ganon's Boss Key is set to tokens, this is how many Gold Skulltula Tokens are required to open it.
    Once the required amount is reached, the boss key will be granted through the Light Arrow cutscene in the Temple of Time.
    """
    display_name = "Ganons Castle Boss Key Skull Tokens Required"
    range_start = 1
    range_end = 100
    default = 50

class KeyRings(Toggle):
    """
    Keyrings will replace all small keys from a particular dungeon with a single keyring that awards all keys for its associated dungeon.
    """
    display_name = "Key Rings"

class BigPoeTargetCount(Range):
    """
    The Poe collector will give a reward for turning in this many Big Poes.
    """
    display_name = "Big Poe Target Count"
    range_start = 0
    range_end = 10
    default = 1

class SkipChildZelda(Toggle):
    """
    Start with Zelda's Letter and the item Impa would normally give you and skip the sequence up until after meeting Zelda. Disables the ability to shuffle Weird Egg.
    """
    display_name = "Skip Child Zelda"
    default = 1

class SkipEponaRace(Toggle):
    """
    Epona can be summoned with Epona's Song without needing to race Ingo.
    """
    display_name = "Skip Epona Zelda"
    default = 1

class CompleteMaskQuest(Toggle):
    """
    Once the Happy Mask Shop is opened, all masks will be available to be borrowed.
    """
    display_name = "Complete Mask Quest"
    default = 1

class SkipScarecrowsSong(Toggle):
    """
    Start with the ability to summon Pierre the Scarecrow. Pulling out an Ocarina in the usual locations will automatically summon him.
    With Shuffle Ocarina Buttons enabled, you'll need at least two Ocarina buttons to summon him.
    """
    display_name = "Skip Scarecrow's Song"
    default = 1

class FullWallets(Toggle):
    """
    Start with a full wallet. All wallet upgrades come filled with rupees.
    """
    display_name = "Full Wallets"
    default = 1

class BombchuBag(Toggle):
    """
    Bombchus require their own bag to be found before use. Without this setting, any Bombchu requirement is filled by Bomb Bag + a renewable source of Bombchus.
    The first Bombchu you find be a Bag containing 20 chus, and subsequent packs will have 10.
    Once found, they can be replenished at shops selling refills, Bombchu Bowling and the carpet merchant.
    Bombchu Bowling is opened by obtaining the Bombchu Bag.
    """
    display_name = "Bombchu Bag"

class BombchuDrops(Toggle):
    """
    Once you obtain a Bombchu Bag, refills will sometimes replace Bomb drops that would spawn.
    If you have Bombchu Bag disabled, you will need a Bomb Bag and existing Bombchus for Bombchus to drop.
    """
    display_name = "Bombchu Drops"
    default = 1

class BlueFireArrows(Toggle):
    """
    Ice Arrows act like Blue Fire, making them able to melt red ice. 
    """
    display_name = "Blue Fire Arrows"
    default = 1

class SunlightArrows(Toggle):
    """
    Light Arrows can be used to light up the sun switches instead of using the Mirror Shield.
    """
    display_name = "Sunlight Arrows"
    default = 1

class InfiniteUpgrades(Choice):
    """
    Adds upgrades that hold infinite quantities of items (bombs, arrows, etc.).
    Progressive - The infinite upgrades are obtained after getting the last normal capacity upgrade.
    Condensed Progressive - The infinite upgrades are obtained as the first capacity upgrade (doesn't apply to the infinite wallet or to infinite magic).
    """
    display_name = "Infinite Upgrades"
    option_off = 0
    option_progressive = 1
    option_condensed_progressive = 2
    default = 0

class SkeletonKey(Toggle):
    """
    Adds a new item called the Skeleton Key, it unlocks every dungeon door locked by a small key.
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
