from dataclasses import dataclass
from Options import Choice, Toggle, DefaultOnToggle, Range, PerGameCommonOptions, StartInventoryPool, Visibility, OptionGroup


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
    Closed:
    Sleeping Waterfall obstructs the entrance to Zora's Domain. Zelda's Lullaby must be played in order to open
    it (but only once; then it stays open in both time periods).

    Open: 
    Sleeping Waterfall is always open. Link may always enter Zora's Domain.
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


class RainbowBridgeGregModifier(Choice):
    """
    If Rainbow Bridge is enabled, Greg will count toward the bridge requirement goal.
    Off - Greg won't change the Rainbow Bridge Requirements.
    Reward - Greg will count toward the bridge requirement and be considered in the logic.
    Wildcard - Greg will count toward the bridge requirement but not be considered in logic.
    """
    display_name = "Rainbow Bridge Greg Modifier"
    option_off = 0
    option_reward = 1
    option_wildcard = 2


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


class SkipGanonsTrials(DefaultOnToggle):
    """
    Choose wether or not Ganon's Trials are completed from the start.
    """
    display_name = "Skip Ganon's Trials"


class TriforceHunt(Toggle):
    """
    Pieces of the Triforce of Courage have been scattered across the world. Find them all to finish the game! 
    If this option is enabled, Ganon's Boss Key will not be shuffled and Light Arrow Cutscene (LACS) will revert to its vanilla behavior.
    When the required amount of pieces have been found, the game is saved and Ganon's Boss key is
    given to you when you load back into the game if you desire to beat Ganon afterwards.
    """
    display_name = "Triforce Hunt"


class TriforceHuntPiecesTotal(Range):
    """
    Specify an exact number of Triforce Pieces to add to the item pool. If the item pool is out of space, no more will be added.
    """
    display_name = "Triforce Hunt Pieces Total"
    range_start = 1
    range_end = 100
    default = 30


class TriforceHuntPiecesRequiredPercentage(Range):
    """
    The percentage of Triforce pieces that will be required to complete the game.
    """
    display_name = "Triforce Hunt Pieces Required Percentage"
    range_start = 1
    range_end = 100
    default = 60


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


class SkullsSunSong(Toggle):
    """
    All Golden Skulltulas that require nighttime to appear will only be expected to be collected after getting Sun's Song.
    """
    display_name = "Night Skulltulas Expect Sun's Song"


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
    Shuffle shop items amongst the different shops.
    """
    display_name = "Shuffle Shops"


class ShuffleShopsItemAmount(Range):
    """
    If Shuffle Shops is on, set how many shop items in each shop will be replaced by an entirely random item with a random price.
    """
    display_name = "Shuffle Shops Item Amount"
    range_start = 0
    range_end = 7
    default = 4


class ShuffleShopsMinimumPrice(Range):
    """
    If Shuffle Shops is on, set the minimum price of randomized shop items. Final price will be rounded down to multiples of 5.
    Shuffled vanilla shop items will keep their vanilla price regardless of what's chosen here.
    """
    display_name = "Shuffle Shops Minimum Price"
    range_start = 0
    range_end = 999
    default = 10


class ShuffleShopsMaximumPrice(Range):
    """
    If Shuffle Shops is on, set the maximum price of randomized shop items. Final price will be rounded down to multiples of 5.
    If this is set below the minimum, this option will be set to whatever the minimum is set to.
    Shuffled vanilla shop items will keep their vanilla price regardless of what's chosen here.
    """
    display_name = "Shuffle Shops Maximum Price"
    range_start = 0
    range_end = 999
    default = 250


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
    Shuffles all Deku Scrub merchants in the game.
    """
    display_name = "Shuffle Scrubs"


class ShuffleScrubsMinimumPrice(Range):
    """
    If Shuffle Scrubs is on, set their minimum price. Final price will be rounded down to multiples of 5.
    """
    display_name = "Shuffle Scrubs Minimum Price"
    range_start = 0
    range_end = 999
    default = 10


class ShuffleScrubsMaximumPrice(Range):
    """
    If Shuffle Scrubs is on, set their maximum price. Final price will be rounded down to multiples of 5.
    If this is set below the minimum, this option will be set to whatever the minimum is set to.
    """
    display_name = "Shuffle Scrubs Maximum Price"
    range_start = 0
    range_end = 999
    default = 90


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


class ShuffleTrees(Toggle):
    """
    Trees will contain randomized items which are dropped the first time the player rolls into one.
    Trees will have a special appearance when carrying randomized items.

    Some trees are dependent on Link's age, such as some trees in Hyrule Field.
    Two trees at Hyrule Castle are only shuffle with No Logic.
    """
    display_name = "Shuffle Trees"


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


class ShuffleFountainFairies(Toggle):
    """
    Shuffle fairies in fountain locations.
    This includes the sets of fairies found in Ganon's Castle and the Desert Oasis.
    """
    display_name = "Shuffle Fairies in Fountains"


class ShuffleStoneFairies(Toggle):
    """
    Shuffle fairies from gossip stone locations.
    """
    display_name = "Shuffle Gossip Stone Fairies"


class ShuffleBeanFairies(Toggle):
    """
    Shuffle fairies from magic bean locations.
    """
    display_name = "Shuffle Bean Fairies"


class ShuffleSongFairies(Toggle):
    """
    Shuffle fairy spots. These are spots where a big fairy is revealed by a song.

    This excludes gossip stones and magic bean locations.
    """
    display_name = "Shuffle Fairy Spots"


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
    Shuffle - Maps & Compasses can appear anywhere.
    """
    display_name = "Maps and Compasses"
    option_start_with = 0
    option_shuffle = 1
    default = 0


class GanonsCastleBossKey(Choice):
    """
    Vanilla - Ganon's Boss Key will appear in the vanilla location.
    Anywhere - Ganon's Boss Key can appear anywhere.
    LACS - These settings put the boss key on the Light Arrow Cutscene location, from Zelda in Temple of Time as adult, with differing requirements:
    - Vanilla: Obtain the Shadow Medallion and Spirit Medallion.
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


class GanonsCastleBossKeyGregModifier(Choice):
    """
    If Ganons Castle Boss Key is enabled, Greg will count toward the LACS goal.
    Off - Greg won't change the LACS goal requirement.
    Reward - Greg will count toward the LACS goal and be considered in the logic.
    Wildcard - Greg will count toward the LACS goal but not be considered in logic.
    """
    display_name = "Ganons Castle Boss Key Greg Wildcard"
    option_off = 0
    option_reward = 1
    option_wildcard = 2


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


class SkipChildZelda(DefaultOnToggle):
    """
    Start with Zelda's Letter and the item Impa would normally give you and skip the sequence up until after meeting Zelda. Disables the ability to shuffle Weird Egg.
    """
    display_name = "Skip Child Zelda"


class SkipEponaRace(DefaultOnToggle):
    """
    Epona can be summoned with Epona's Song without needing to race Ingo.
    """
    display_name = "Skip Epona Race"


class CompleteMaskQuest(DefaultOnToggle):
    """
    Once the Happy Mask Shop is opened, all masks will be available to be borrowed.
    """
    display_name = "Complete Mask Quest"


class SkipScarecrowsSong(DefaultOnToggle):
    """
    Start with the ability to summon Pierre the Scarecrow. Pulling out an Ocarina in the usual locations will automatically summon him.
    With Shuffle Ocarina Buttons enabled, you'll need at least two Ocarina buttons to summon him.
    """
    display_name = "Skip Scarecrow's Song"


class FullWallets(DefaultOnToggle):
    """
    Start with a full wallet. All wallet upgrades come filled with rupees.
    """
    display_name = "Full Wallets"


class BombchuBag(DefaultOnToggle):
    """
    Bombchus require their own bag to be found before use. Without this setting, any Bombchu requirement is filled by Bomb Bag + a renewable source of Bombchus.
    The first Bombchu you find be a Bag containing 20 chus, and subsequent packs will have 10.
    Once found, they can be replenished at shops selling refills, Bombchu Bowling and the carpet merchant.
    Bombchu Bowling is opened by obtaining the Bombchu Bag.
    """
    display_name = "Bombchu Bag"


class BombchuDrops(DefaultOnToggle):
    """
    Once you obtain a Bombchu Bag, refills will sometimes replace Bomb drops that would spawn.
    If you have Bombchu Bag disabled, you will need a Bomb Bag and existing Bombchus for Bombchus to drop.
    """
    display_name = "Bombchu Drops"


class BlueFireArrows(DefaultOnToggle):
    """
    Ice Arrows act like Blue Fire, making them able to melt red ice. 
    """
    display_name = "Blue Fire Arrows"


class SunlightArrows(DefaultOnToggle):
    """
    Light Arrows can be used to light up the sun switches instead of using the Mirror Shield.
    """
    display_name = "Sunlight Arrows"


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
    Adds a new item called the Skeleton Key, it unlocks every door locked by a small key.
    """
    display_name = "Skeleton Key"


class SlingbowBreakBeehives(DefaultOnToggle):
    """
    Allows Slingshot and Bow to break beehives when Beehive Shuffle is turned on.
    """
    display_name = "Slingshot and Bow Can Break Beehives"


class StartingAge(Choice):
    """
    Decide whether to start as child Link or adult Link.
    Child Link starts in Link's House in Kokiri Forest.
    Adult Link starts in the Temple of Time.
    CAUTION: When Door of Time is set to closed, and Shuffle Dungeon Rewards set to off, this option will be forced to child.
    """
    display_name = "Starting Age"
    option_child = 0
    option_adult = 1
    default = 0


class Shuffle100GSReward(Toggle):
    """
    Shuffle the item the cursed rich man in the House of Skulltula gives you when you have collected all 100 Gold Skulltula Tokens.
    You can still talk to him multiple times to get Huge Rupees.
    """
    display_name = "Shuffle 100 GS Reward"


class IceTrapCount(Range):
    """
    Specify an exact number of Ice Traps to add to the item pool. If the item pool is out of space, no more will be added.
    """
    display_name = "Ice Trap Count"
    range_start = 0
    range_end = 100
    default = 6


class IceTrapFillerReplacement(Range):
    """
    Specify a percentage of filler items to replace with Ice Traps.
    """
    display_name = "Ice Trap Filler Replacement Count"
    range_start = 0
    range_end = 100
    default = 0


class TrueNoLogic(Toggle):
    """
    Turn off logic completely.
    Generation will fail if this is enabled and allow_true_no_logic is not set to true in the host.yaml.
    """
    display_name = "True No Logic"
    visibility = Visibility.spoiler


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
    rainbow_bridge_greg_modifier: RainbowBridgeGregModifier
    skip_ganons_trials: SkipGanonsTrials
    triforce_hunt: TriforceHunt
    triforce_hunt_pieces_total: TriforceHuntPiecesTotal
    triforce_hunt_pieces_required_percentage: TriforceHuntPiecesRequiredPercentage
    shuffle_skull_tokens: ShuffleTokens
    skulls_sun_song: SkullsSunSong
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
    shuffle_shops_item_amount: ShuffleShopsItemAmount
    shuffle_shops_minimum_price: ShuffleShopsMinimumPrice
    shuffle_shops_maximum_price: ShuffleShopsMaximumPrice
    shuffle_fish: ShuffleFish
    shuffle_scrubs: ShuffleScrubs
    shuffle_scrubs_minimum_price: ShuffleScrubsMinimumPrice
    shuffle_scrubs_maximum_price: ShuffleScrubsMaximumPrice
    shuffle_beehives: ShuffleBeehives
    shuffle_cows: ShuffleCows
    shuffle_pots: ShufflePots
    shuffle_crates: ShuffleCrates
    shuffle_trees: ShuffleTrees
    shuffle_merchants: ShuffleMerchants
    shuffle_frog_song_rupees: ShuffleFrogSongRupees
    shuffle_adult_trade_items: ShuffleAdultTradeItems
    shuffle_boss_souls: ShuffleBossSouls
    shuffle_fountain_fairies: ShuffleFountainFairies
    shuffle_stone_fairies: ShuffleStoneFairies
    shuffle_bean_fairies: ShuffleBeanFairies
    shuffle_song_fairies: ShuffleSongFairies
    shuffle_grass: ShuffleGrass
    shuffle_dungeon_rewards: ShuffleDungeonRewards
    maps_and_compasses: MapsAndCompasses
    ganons_castle_boss_key: GanonsCastleBossKey
    ganons_castle_boss_key_stones_required: GanonsCastleBossKeyStonesRequired
    ganons_castle_boss_key_medallions_required: GanonsCastleBossKeyMedallionsRequired
    ganons_castle_boss_key_dungeon_rewards_required: GanonsCastleBossKeyDungeonRewardsRequired
    ganons_castle_boss_key_dungeons_required: GanonsCastleBossKeyDungeonsRequired
    ganons_castle_boss_key_skull_tokens_required: GanonsCastleBossKeySkullTokensRequired
    ganons_castle_boss_key_greg_modifier: GanonsCastleBossKeyGregModifier
    key_rings: KeyRings
    big_poe_target_count: BigPoeTargetCount
    skip_child_zelda: SkipChildZelda
    skip_epona_race: SkipEponaRace
    complete_mask_quest: CompleteMaskQuest
    skip_scarecrows_song: SkipScarecrowsSong
    full_wallets: FullWallets
    bombchu_bag: BombchuBag
    bombchu_drops: BombchuDrops
    start_inventory_from_pool: StartInventoryPool
    blue_fire_arrows: BlueFireArrows
    sunlight_arrows: SunlightArrows
    infinite_upgrades: InfiniteUpgrades
    skeleton_key: SkeletonKey
    slingbow_break_beehives: SlingbowBreakBeehives
    starting_age: StartingAge
    shuffle_100_gs_reward: Shuffle100GSReward
    ice_trap_count: IceTrapCount
    ice_trap_filler_replacement: IceTrapFillerReplacement
    true_no_logic: TrueNoLogic


soh_option_groups = [
    OptionGroup("Area Access", [
        ClosedForest,
        KakarikoGate,
        DoorOfTime,
        ZorasFountain,
        SleepingWaterfall,
        JabuJabu,
        LockOverworldDoors,
    ]),
    OptionGroup("World Settings", [
        StartingAge,
        FortressCarpenters,
        RainbowBridge,
        RainbowBridgeStonesRequired,
        RainbowBridgeMedallionsRequired,
        RainbowBridgeDungeonRewardsRequired,
        RainbowBridgeDungeonsRequired,
        RainbowBridgeSkullTokensRequired,
        RainbowBridgeGregModifier,
        SkipGanonsTrials,
        TriforceHunt,
        TriforceHuntPiecesTotal,
        TriforceHuntPiecesRequiredPercentage,
    ]),
    # OptionGroup("Shuffle Entrances", [
    #     # Dungeon Entrances
    #     # Boss Entrances
    #     # Overworld Entrances
    #     # Interior Entrances
    #     # Grotto Entrances
    #     # Owl Drops
    #     # Warp Songs
    #     # Overworld Spawns
    #     # Decouple Entrances
    # ]),
    OptionGroup("Shuffle Items", [
        # Shuffle Songs -- idk if this or the other ones here will be an actual option here, delete if not
        ShuffleTokens,
        SkullsSunSong,
        # Shuffle Kokiri Sword
        ShuffleMasterSword,
        ShuffleChildsWallet,
        # Include Tycoon Wallet
        # Shuffle Ocarinas
        ShuffleOcarinaButtons,
        ShuffleSwim,
        ShuffleWeirdEgg,
        # Shuffle Gerudu Membership Card
        ShuffleFishingPole,
        ShuffleDekuStickBag,
        ShuffleDekuNutBag,
        ShuffleFreestandingItems,
    ]),
    OptionGroup("Shuffle NPCs & Merchants", [
        ShuffleShops,
        ShuffleShopsItemAmount,
        ShuffleShopsMinimumPrice,
        ShuffleShopsMaximumPrice,
        # Other shop weight stuff
        ShuffleFish,
        ShuffleScrubs,
        ShuffleScrubsMinimumPrice,
        ShuffleScrubsMaximumPrice,
        ShuffleBeehives,
        ShuffleCows,
        ShufflePots,
        ShuffleCrates,
        ShuffleTrees,
        ShuffleMerchants,
        # Merchant prices
        ShuffleFrogSongRupees,
        ShuffleAdultTradeItems,
        Shuffle100GSReward,
        ShuffleBossSouls,
        ShuffleFountainFairies,
        ShuffleStoneFairies,
        ShuffleBeanFairies,
        ShuffleSongFairies,
        ShuffleGrass,
    ]),
    OptionGroup("Shuffle Dungeon Items", [
        ShuffleDungeonRewards,
        MapsAndCompasses,
        # Small Key Shuffle
        # Gerudo Fortress Keys
        # Boss Key Shuffle
        GanonsCastleBossKey,
        GanonsCastleBossKeyStonesRequired,
        GanonsCastleBossKeyMedallionsRequired,
        GanonsCastleBossKeyDungeonRewardsRequired,
        GanonsCastleBossKeyDungeonsRequired,
        GanonsCastleBossKeySkullTokensRequired,
        GanonsCastleBossKeyGregModifier,
        KeyRings,
        # Key Ring Dungeon Count
    ]),
    # todo: decide whether these should be in the yaml or just let you change them locally on the fly
    OptionGroup("Timesavers", [
        BigPoeTargetCount,
        SkipChildZelda,
        SkipEponaRace,
        CompleteMaskQuest,
        SkipScarecrowsSong,
    ]),
    # OptionGroup("Item Pool & Hints", [
    # none of these are implemented, so just leaving this placeholder
    # ]),
    OptionGroup("Additional Features", [
        FullWallets,  # another one that should maybe just be a locally changeable setting instead of in the yaml
        BombchuBag,
        BombchuDrops,
        BlueFireArrows,
        SunlightArrows,
        InfiniteUpgrades,
        SkeletonKey,
        SlingbowBreakBeehives,
        IceTrapCount,
        IceTrapFillerReplacement
    ])
]
