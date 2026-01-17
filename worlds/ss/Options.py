from dataclasses import dataclass

from Options import (
    Choice,
    DeathLink,
    DefaultOnToggle,
    OptionGroup,
    OptionSet,
    PerGameCommonOptions,
    Range,
    StartInventoryPool,
    ProgressionBalancing,
    Toggle,
    Removed,
)


# Completion Requirements
class RequiredDungeonCount(Range):
    """
    Determines the number of dungeons required to beat the seed.
    Beating Sky Keep is **NOT** required.
    Lanayru Mining Facility is beaten when exiting to the Temple of Time at the end of the dungeon.
    The other dungeons are only beaten when the Goddess Crest at the end is struck with a Skyward Strike.
    """

    display_name = "Required Dungeon Count"
    range_start = 0
    range_end = 6
    default = 2


class TriforceRequired(DefaultOnToggle):
    """
    If enabled, the three Triforces will be required to open the door to Hylia's Realm at the end of the game.
    """

    display_name = "Triforce Required"


class TriforceShuffle(Choice):
    """
    Choose where Triforces will appear in the game.
    **Vanilla**: Triforces are placed in their vanilla locations in Sky Keep.
    **Sky Keep**: Triforces are shuffled only within Sky Keep.
    **Anywhere**: Triforces are shuffled with all other valid locations in the game.
    """

    display_name = "Triforce Shuffle"
    option_vanilla = 0
    option_sky_keep = 1
    option_anywhere = 2
    default = 2


class GateOfTimeSwordRequirement(Choice):
    """
    Determines the sword needed to open the Gate of Time.
    """

    display_name = "Gate of Time Sword Requirement"
    option_goddess_sword = 0
    option_goddess_longsword = 1
    option_goddess_white_sword = 2
    option_master_sword = 3
    option_true_master_sword = 4
    default = 4


class GateOfTimeDungeonRequirements(Choice):
    """
    Enables dungeon requirements for opening the Gate of Time.
    **Required**: beating the required dungeons is necessary to open the Gate of Time.
    **Unrequired**: the Gate of Time can be opened without beating the required dungeons.
    """

    display_name = "Gate of Time Dungeon Requirements"
    option_required = 0
    option_unrequired = 1
    default = 0


class Imp2Skip(DefaultOnToggle):
    """
    If enabled, the requirement to defeat Imprisoned 2 at the end of the game is skipped.
    """

    display_name = "Imp 2 Skip"


class SkipHorde(Toggle):
    """
    If enabled, the requirement to defeat The Horde at the end of the game is skipped.
    """

    display_name = "Skip Horde"


class SkipGhirahim3(Toggle):
    """
    If enabled, the requirement to defeat Ghirahim 3 at the end of the game is skipped.
    """

    display_name = "Skip Ghirahim 3"


class SkipDemise(Toggle):
    """
    If enabled, the requirement to defeat Demise at the end of the game is skipped.
    """

    display_name = "Skip Demise"


# Open Options
class GateOfTimeStartingState(Choice):
    """
    Determines whether the Gate of Time starts raised or lowered.
    **Lowered**: the Goddess's Harp is needed to raise the Gate of Time.
    **Raised**: the Gate of Time is raised from the start of the game.
    """

    display_name = "Gate of Time Starting State"
    option_lowered = 0
    option_raised = 1
    default = 0


class OpenThunderhead(Choice):
    """
    Determines how the Thunderhead is unlocked.
    **Ballad**: the Thunderhead opens when the Ballad of the Goddess song is found.
    **Open**: the Thunderhead is open from the start of the game.
    """

    display_name = "Open Thunderhead"
    option_ballad = 0
    option_open = 1
    default = 0


class OpenEarthTemple(Toggle):
    """
    If enabled, the Earth Temple door (requiring 5 key pieces to unlock) is opened at the start of the game.
    """

    display_name = "Open Earth Temple"


class OpenLanayruMiningFacility(Choice):
    """
    Determines the conditions for opening the Lanayru Mining Facility dungeon.
    **Nodes**: requires activating the 3 nodes (vanilla).
    **Main Node**: requires only the main generator to be activated.
    **Open**: the Lanayru Mining Facility is open at the start of the game.
    """

    display_name = "Open Lanayru Mining Facility"
    option_nodes = 0
    option_main_node = 1
    option_open = 2
    default = 2


class OpenLakeFloria(Choice):
    """
    Choose how to access Lake Floria.
    **Vanilla**: logically requires you to talk to Yerbal and draw on the Floria Gates to enter Lake Floria.
    **Talk to Yerbal**: logically requires you to talk to Yerbal to enter Lake Floria.
    **Open**: the Floria Gates are opened from the start of the game.
    """

    display_name = "Open Lake Floria"
    option_vanilla = 0
    option_talk_to_yerbal = 1
    option_open = 2
    default = 0


# Progression Groups for AP
# These options only exist for AP
class ProgressionGoddessChests(DefaultOnToggle):
    """
    If enabled, Goddess Chests can contain progression items.
    If not enabled, all Goddess Chests will contain junk (filler) items.
    """

    display_name = "Progression in Goddess Chests"

class ProgressionMinigames(DefaultOnToggle):
    """
    If enabled, Minigames can contain progression items.
    If not enabled, all Minigames will contain junk (filler) items.
    """

    display_name = "Progression in Minigames"

class ProgressionCrystals(DefaultOnToggle):
    """
    If enabled, Crystal Quests can contain progression items.
    If not enabled, all Crystals Quests will contain junk (filler) items.
    """

    display_name = "Progression in Gratitude Crystal Quests"

class ProgressionScrapper(DefaultOnToggle):
    """
    If enabled, Scrapper Quests can contain progression items.
    If not enabled, all Scrapper Quests will contain junk (filler) items.
    """

    display_name = "Progression in Scrapper Quests"

class ProgressionBatreaux(Range):
    """
    Controls the maximum Batreaux's reward that can contain progression items.
    Progression locations will begin with Batreaux's first rewards. Any locations
    after this number will contain junk (filler) items.
    0 means no rewards may contain progression, 7 means all rewards may contain progression.

    NOTE: Batreaux's chest falls under the third reward, and the seventh reward falls under the sixth reward,
    since they are given at the same time.
    """

    display_name = "Progression in Batreaux's Rewards"
    range_start = 0
    range_end = 7
    default = 7


# Dungeons
class EmptyUnrequiredDungeons(DefaultOnToggle):
    """
    If enabled, only the required dungeons will contain progression items.
    If not enabled, all dungeons and Sky Keep can potentially contain progression items.
    """

    display_name = "Empty Unrequired Dungeons"


class MapMode(Choice):
    """
    Determines the placement of maps.
    **Start With**: start with all maps.
    **Vanilla**: maps appear in their vanilla locations.
    **Own Dungeon - Restricted**: dungeon maps cannot appear on boss heart containers or the ending checks of dungeons.
    **Own Dungeon - Unrestricted**: dungeon maps appear anywhere within their own dungeon.
    **Anywhere**: maps can appear outside of dungeons in any world.
    """

    display_name = "Map Mode"
    option_start_with = 0
    option_vanilla = 1
    option_own_dungeon_restricted = 2
    option_own_dungeon_unrestricted = 3
    # option_own_dungeon_any_world = 0
    option_anywhere = 4
    default = 2


class SmallKeyMode(Choice):
    """
    Determines the placement of small keys.
    **Vanilla**: keys will be in their vanilla locations (The Skyview Digging Spot will not contain a key).
    **Own Dungeon**: keys will be within their own dungeons in your own world.
    **Anywhere**: keys can appear outside of dungeons in any world.
    """

    display_name = "Small Key Mode"
    option_vanilla = 0
    option_own_dungeon = 1
    # option_own_dungeon_any_world = 0
    option_anywhere = 2
    default = 1


class LanayruCavesSmallKey(Choice):
    """
    Determines the placement of the Lanayru Caves small key.
    **Start With**: start with the key in your inventory.
    **Caves**: places the key within the caves.
    **Lanayru**: places the key in the Lanayru surface region. The key will only be in an accessible area of Lanayru.
    **Anywhere**: key can appear outside of lanayru in any world.
    """

    display_name = "Lanayru Caves Small Key"
    option_start_with = 0
    option_caves = 1
    option_lanayru = 2
    option_anywhere = 3
    default = 2


class BossKeyMode(Choice):
    """
    Determines the placement of boss keys.
    **Vanilla**: boss keys appear in their vanilla locations.
    **Own Dungeon**: boss keys appear within their own dungeon in your own world.
    **Anywhere**: boss keys can appear outside of dungeons in any world.
    """

    display_name = "Boss Key Mode"
    option_vanilla = 0
    option_own_dungeon = 1
    # option_own_dungeon_any_world = 0
    option_anywhere = 2
    default = 1


class FSLastRoomLavaFlow(Toggle):
    """
    If enabled, the lava in the last room of Fire Sanctuary will be flowing by default (without needing to
    blow up the underground boulder).
    """

    display_name = "FS Last Room Lava Flow"


# Silent Realms
class ShuffleTrialObjects(Choice):
    """
    Shuffles obtainable items in Silent Realms (within the same Silent Realm).
    **None**: trial objects appear in their vanilla locations.
    **Simple**: only shuffles tears and light fruits.
    **Advanced**: also shuffles dusk relics.
    **Full**: also shuffles stamina fruits.
    """

    display_name = "Shuffle Trial Objects"
    option_none = 0
    option_simple = 1
    option_advanced = 2
    option_full = 3
    default = 0


class TreasuresanityInSilentRealms(Toggle):
    """
    Randomizes treasures in Silent Realms to items. Items other than relics will glow in Silent Realms
    (Yellow in Faron, Blue in Eldin, Green in Lanayru, and Red on Skyloft)
    """

    display_name = "Treasuresanity in Silent Realms"


class TrialTreasureAmount(Range):
    """
    How many treasures per Silent Realm you want to randomize.
    """

    display_name = "Trial Treasure Amount"
    range_start = 1
    range_end = 10
    default = 5


# Entrances
class RandomizeEntrances(Choice):
    """
    Shuffles entrances with one another.
    **None**: entrances are vanilla.
    **Required Dungeons Separately**: required dungeons entrances are only shuffled with each other.
    **All Surface Dungeons**: all surface dungeons entrances are shuffled with each other.
    **All Surface Dungeons + Sky Keep** - all surface dungeon entrances AND the Sky Keep entrance are shuffled with each other.
    """

    display_name = "Randomize Entrances"
    option_none = 0
    option_required_dungeons_separately = 1
    option_all_surface_dungeons = 2
    option_all_surface_dungeons_and_sky_keep = 3
    default = 0


class RandomizeSilentRealms(Toggle):
    """
    If enabled, the Silent Realm that a Trial Gate entrance leads to is shuffled.
    """

    display_name = "Randomize Silent Realms"


class RandomStartingSpawn(Choice):
    """
    Determines where you will spawn you start the game.
    **Vanilla**: You will spawn in Link's bedroom.
    **Bird Statues**: You will spawn at a random Bird Statue or Link's bedroom.
    **Any Surface Region**: You will spawn at any valid surface entrance or Link's bedroom.
    **Any**: You will spawn at any valid entrance.
    **TIP**: You can ask Fi to warp you back to the starting point.
    """

    display_name = "Random Starting Spawn"
    option_vanilla = 0
    option_bird_statues = 1
    option_any_surface_region = 2
    option_any = 3
    default = 0


# class LimitStartingLocation(Toggle):
#     """
#     If enabled, you will only start at a location in a region unlocked by the tablets you start with.
#     E.g. Starting with Ruby Tablet and Amber Tablet will mean you cannot start in Faron.
#     """

#     display_name = "Limit Starting Location"


class RandomStartingStatues(Toggle):
    """
    If enabled, the starting statue for each surface region will be randomized. All overworld statues
    except Inside the Volcano and Inside Fire Sanctuary may be chosen.
    """

    display_name = "Random Starting Statues"


# Additional Randomization
class Shopsanity(DefaultOnToggle):
    """
    Determines if shops are randomized. When enabled, shop items and locations will be shuffled like normal items,
    and the shop locations will get a randomized item. When disabled, shops will always contain their vanilla items,
    however those items may still be required for progression. **Currently shuffled shops**: Beedle's Airshop
    """

    display_name = "Shopsanity"


class RupoorMode(Choice):
    """
    Adds or replaces junk items with Rupoors.
    **Off**: no Rupoors are added as junk items.
    **Added**: adds 15 rupoors as junk items.
    **Rupoor Mayhem**: replaces half of the junk items with Rupoors.
    **Rupoor Insanity**: replaces all junk items with Rupoors.
    Note, Rupoors may also be added if there are not enough junk items for the game to randomize.
    """

    display_name = "Rupoor Mode"
    option_off = 0
    option_added = 1
    option_rupoor_mayhem = 2
    option_rupoor_insanity = 3
    default = 0


class Rupeesanity(DefaultOnToggle): # Toggle
    """
    Shuffles freestanding rupees. When unshuffled, all freestanding rupees will remain vanilla.
    Note, it is not possible to shuffle some freestanding rupees yet (e.g. the rupees on the Lumpy Pumpkin
    chandelier).
    """

    display_name = "Rupeesanity"


class Tadtonesanity(Toggle):
    """
    If enabled, 17 \"Group of Tadtones\" items will be shuffled throughout the world and each of the tadtone
    groups in Flooded Faron Woods will give an item when collected. Get all 17 \"Group of Tadtones\" items to
    complete the music scroll and receive an item from the Water Dragon in Flooded Faron Woods."
    """

    display_name = "Tadtonesanity"


class PlaceScrapShopUpgrades(DefaultOnToggle):
    """
    If enabled, the extra progressive items upgradeable in the Scrap Shop in vanilla will be shuffled.
    Includes: Quick Beetle, Tough Beetle, Iron Bow, Sacred Bow, Big Bug Net and Scattershot.
    Note, there are no random items obtainable by talking to Gondo at the Scrap Shop.
    """

    display_name = "Place Scrap Shop Upgrades"


class ForceSwordDungeonReward(Choice):
    """
    Determines if swords should be rewarded for beating required dungeons.
    **None**: swords are shuffled anywhere.
    **Heart Container**: end of required dungeon heart containers are swords.
    **Final Check**: the final check of required dungeons are swords.
    Note, if there aren't enough swords to place, some required dungeons will not force a sword at the end.
    """

    display_name = "Force Sword Dungeon Reward"
    option_none = 0
    option_heart_container = 1
    option_final_check = 2
    default = 0


class ShuffleBatreauxCounts(Choice):
    """
    Determines the amount of crystals Batreaux will require for each of his rewards.
    **Vanilla**: The normal required crystal counts (5, 10, 30, 40, 50, 70, 80).
    **Half**: Half of the normal required crystal counts (2, 5, 15, 20, 25, 35, 40).
    **Shuffled**: Completely random required crystal counts (min 1, max 80).
    **Shuffled - High**: Higher random required crystal counts (min 30, max 80).
    **Shuffled - Low**: Lower random required crystal counts (min 1, max 50).
    """
    
    display_name = "Shuffle Batreaux Counts"
    option_vanilla = 0
    option_half = 1
    option_shuffled = 2
    option_shuffled_high = 3
    option_shuffled_low = 4
    default = 0


class RandomizeBossKeyPuzzles(Toggle):
    """
    If enabled, the starting position of the boss keys will be randomized.
    """

    display_name = "Randomize Boss Key Puzzles"


class RandomPuzzles(Toggle):
    """
    Randomizes the Isle of Songs puzzle, the Ancient Cistern/Sandship directional door puzzles,
    and the Lanayru Mining Facility switches puzzle.
    """

    display_name = "Random Puzzles"


class PeatriceConversations(Range):
    """
    How many times you need to talk to Peatrice before she calls you \"darling\" and you can start Peater's quest.
    """

    display_name = "Peatrice Conversations"
    range_start = 0
    range_end = 6
    default = 6


class DemiseCount(Range):
    """
    Determines how many demises appear in the final fight of the game.
    **WARNING**: Enabling more than one makes the fight very difficult.
    **DOUBLE WARNING**: Enabling more than 3 demises produces a lot of lag and can make the game unplayable.
    """

    display_name = "Demise Count"
    range_start = 1
    range_end = 10
    default = 1


# Convenience Tweaks
class BiTPatches(Choice):
    """
    Changes how the Back in Time (BiT) glitch works.
    **Disable BiT**: Makes it impossible to activate BiT.
    **Vanilla**: Keeps the vanilla game behaviour where BiT is possible but Eldin BiT (and others) will still crash.
    **Fix BiT Crashes**: Does not load some arcs to make all areas accessible in BiT.
    **WARNING**: All 3 files must be filled BEFORE activating BiT otherwise this will not work.
    """

    display_name = "BiT Patches"
    option_disable = 0
    option_vanilla = 1
    option_fix_crashes = 2
    default = 0 # 1


class FillDowsingOnWhiteSword(DefaultOnToggle):
    """
    If enabled, obtaining the Goddess White Sword will unlock rupee, crystal, treasure and goddess cube dowsing.
    """

    display_name = "Fill Dowsing on White Sword"


class FullWalletUpgrades(Toggle):
    """
    If enabled, wallets you find throughout the game will already be filled with Rupees.
    E.g. Finding the Giant Wallet will add 4000 Rupees to your Rupee counter.
    """

    display_name = "Full Wallet Upgrades"


class AmmoAvailability(Choice):
    """
    Determines the number of locations where ammo refills can be found.
    **Scarce**: Ammo will only be available from chance-based drops and Rupin's Gear shop.
    **Vanilla**: Ammo will appear when breaking pots and barrels in the same way as the vanilla game.
    **Useful**: Ammo pots will be added in key places near checks requiring a specific ammo to reduce back-tracking.
    **Plentiful**: Ammo pots will be added next to all Bird Statues.
    """

    display_name = "Ammo Availability"
    option_scarce = 0
    option_vanilla = 1
    option_useful = 2
    option_plentiful = 3
    default = 3


# Hero Mode
class UpgradedSkywardStrike(DefaultOnToggle):
    """
    If enabled, the Skyward Strike will be fully upgraded for all swords (excluding Practice Sword).
    This increases the reach and the charge speed of the Skyward Strike.
    """

    display_name = "Upgraded Skyward Strike"


class FasterAirMeterDrain(Toggle):
    """
    If enabled, the air meter depletes twice as fast when under water.
    """

    display_name = "Faster Air Meter Drain"


class HeartDrops(Toggle):
    """
    If enabled, heart flowers will spawn and hearts may drop from defeated enemies, broken pots, broken barrels,
    cut grass, and digging spots.
    """

    display_name = "Heart Drops"


class DamageMultiplier(Range):
    """
    Determines the overall damage multiplier.
    **Normal Mode** (default) damage is x1.
    **Hero Hode** (new game +) damage is x2.
    At x12 or higher, the hot cave in Eldin Volcano logically requires Fireshield Earrings to traverse."
    """

    display_name = "Damage Multiplier"
    range_start = 1
    range_end = 255
    default = 1


# Starting Items
class StartingSword(Choice):
    """
    Select which sword to start with.
    The remaining upgrades will be shuffled into the item pool.
    """

    display_name = "Starting Sword"
    option_swordless = 0
    option_practice_sword = 1
    option_goddess_sword = 2
    option_goddess_longsword = 3
    option_goddess_white_sword = 4
    option_master_sword = 5
    option_true_master_sword = 6
    default = 2


class StartingTabletCount(Range):
    """
    The number of tablets to start with.
    Tablets are selected randomly and the remainder are randomized as progress items.
    """

    display_name = "Starting Tablet Count"
    range_start = 0
    range_end = 3
    default = 1


class StartingGratitudeCrystalPacks(Range):
    """
    How many gratitude crystal packs to start with.
    """

    display_name = "Starting Gratitude Crystal Packs"
    range_start = 0
    range_end = 13
    default = 0


class StartingEmptyBottles(Range):
    """
    Determines how many empty bottles start in your pouch.
    **WARNING**: If you start with more pouch items than pouch slots, the extra items will become usable after
    finding additional pouches.
    """

    display_name = "Starting Empty Bottles"
    range_start = 0
    range_end = 5
    default = 0


class StartingHeartContainers(Range):
    """
    Determines how many heart containers to start with.
    """

    display_name = "Starting Heart Containers"
    range_start = 0
    range_end = 6
    default = 0


class StartingHeartPieces(Range):
    """
    Determines how many heart pieces to start with.
    """

    display_name = "Starting Heart Pieces"
    range_start = 0
    range_end = 24
    default = 0


class StartingTadtoneCount(Range):
    """
    How many groups of Tadtones to start with.
    """

    display_name = "Starting Tadtone Count"
    range_start = 0
    range_end = 17
    default = 0


class RandomStartingItem(Toggle):
    """
    Gives you a random progression item at the start of the game in addition to any starting items.
    This includes: Bow, Beetle, Slingshot, Digging Mitts, Pouch, Bomb Bag, Clawshots, Whip, Gust Bellows,
    Water Dragon's Scale, Fireshield Earrings, Goddess's Harp and Spiral Charge.
    """

    display_name = "Random Starting Item"


class StartWithHylianShield(DefaultOnToggle):
    """
    If enabled, you will start with the Hylian Shield in your pouch.
    **WARNING**: If you start with more pouch items than pouch slots, the extra items will become usable after
    finding additional pouches.
    Hylian Shield will always be placed in the first pouch slot.
    """

    display_name = "Start with Hylian Shield"


class StartWithFullWallet(Toggle):
    """
    If enabled, you will start with a full wallet.
    This changes based on the number of starting wallets and extra wallets.
    """

    display_name = "Start with Full Wallet"


class StartWithMaxBugs(Toggle):
    """
    If enabled, you will start with 99 of each type of bug.
    """

    display_name = "Start with Max Bugs"


class StartWithMaxTreasures(Toggle):
    """
    If enabled, you will start with 99 of each type of treasure.
    """

    display_name = "Start with Max Treasures"


# Hints
class HintDistribution(Choice):
    """
    Determines what hints are placed throughout the world.
    **Standard**: The standard hint distribution.
    **Junk**: 0 Fi hints, and only junk hints on gossip stones.

    Note that this distribution is different from the original randomizer's hint distribution option.
    Archipelago hints in game are placed differently than the original randomizer's hints.
    """

    display_name = "Archipelago Hint Distribution"
    option_standard = 0
    option_junk = 1
    default = 0

class SongHints(Choice):
    """
    Determines how hints appear on songs.
    **None**: Silent Realm rewards will be hinted on Gossip Stones.
    **Basic**: the song text indicates if beating the trial rewards a progress item.
    **Advanced**: the song text indicates if beating the trial rewards a SotS, junk or potientially required item.
    **Direct**: the song text states the reward for beating the trial directly.
    """

    display_name = "Song Hints"
    option_none = 0
    option_basic = 1
    option_advanced = 2
    option_direct = 3
    default = 0


class ChestDowsing(Choice):
    """
    Determines the main quest (top) dowsing option.
    **Vanilla**: dowsing points to Trial Gates and the Sandship
        (after obtaining the necessary song or Sea Chart first).
    **All Chests**: dowsing points to all chests (regardless of their contents).
    **Progress Items**: dowsing only points to chests containing progress items
        (Goddess Chests must be activated by their respective Goddess Cube before being dowsable)).
    """

    display_name = "Chest Dowsing"
    option_vanilla = 0
    option_all_chests = 1
    option_progress_items = 2
    default = 0


class AllowDowsingInDungeons(Toggle):
    """
    If enabled, dowsing will be re-enabled in dungeons and other dungeon-like areas like the Great Tree and
    Waterfall Cave.
    """

    display_name = "Allow Dowsing in Dungeons"


class PastImpaStoneOfTrialsHint(Toggle): # DefaultOnToggle
    """
    If enabled, Impa in Hylia's Temple to give a hint to the location of the Stone of Trials.
    Does not appear if the Stone of Trials is a starting item.
    """

    display_name = "Past Impa Stone of Trials Hint"


class SeparateCubeSotS(Toggle):
    """
    If enabled, when a SotS hint points to a Goddess Chest, the hint will change to indicate this and display
    which of the cube progress regions is SotS.
    """

    display_name = "Separate Cube SotS"


class PreciseItemHints(Toggle):
    """
    If enabled, item hints will indicate the exact location within a region that is being hinted.
    If disabled, only the region will be hinted.
    """

    display_name = "Precise Item Hints"

class SSProgressionBalancing(ProgressionBalancing):
    """
    Algorithm for moving progression items into earlier spheres to make the gameplay experience a bit smoother.
    The higher the value, the more frontloaded the world is.
    """
    default = 70


@dataclass
class SSOptions(PerGameCommonOptions):
    """
    Dataclass containing all randomization options for the Skyward Sword Randomizer.
    """

    required_dungeon_count: RequiredDungeonCount
    triforce_required: TriforceRequired
    triforce_shuffle: TriforceShuffle
    got_sword_requirement: GateOfTimeSwordRequirement
    got_dungeon_requirement: GateOfTimeDungeonRequirements
    imp2_skip: Imp2Skip
    skip_horde: SkipHorde
    skip_g3: SkipGhirahim3
    skip_demise: SkipDemise
    got_start: GateOfTimeStartingState
    open_thunderhead: OpenThunderhead
    open_et: OpenEarthTemple
    open_lmf: OpenLanayruMiningFacility
    open_lake_floria: OpenLakeFloria
    progression_goddess_chests: ProgressionGoddessChests
    progression_minigames: ProgressionMinigames
    progression_crystals: ProgressionCrystals
    progression_scrapper: ProgressionScrapper
    progression_batreaux: ProgressionBatreaux
    empty_unrequired_dungeons: EmptyUnrequiredDungeons
    map_mode: MapMode
    small_key_mode: SmallKeyMode
    lanayru_caves_small_key: LanayruCavesSmallKey
    boss_key_mode: BossKeyMode
    fs_lava_flow: FSLastRoomLavaFlow
    shuffle_trial_objects: ShuffleTrialObjects
    treasuresanity_in_silent_realms: TreasuresanityInSilentRealms
    trial_treasure_amount: TrialTreasureAmount
    randomize_entrances: RandomizeEntrances
    randomize_trials: RandomizeSilentRealms
    random_start_entrance: RandomStartingSpawn
    #limit_start_entrance: LimitStartingLocation
    random_start_statues: RandomStartingStatues
    shopsanity: Shopsanity
    rupoor_mode: RupoorMode
    rupeesanity: Rupeesanity
    tadtonesanity: Tadtonesanity
    gondo_upgrades: PlaceScrapShopUpgrades
    sword_dungeon_reward: ForceSwordDungeonReward
    batreaux_counts: ShuffleBatreauxCounts
    randomize_boss_key_puzzles: RandomizeBossKeyPuzzles
    random_puzzles: RandomPuzzles
    peatrice_conversations: PeatriceConversations
    demise_count: DemiseCount
    bit_patches: BiTPatches
    dowsing_after_whitesword: FillDowsingOnWhiteSword
    full_wallet_upgrades: FullWalletUpgrades
    ammo_availability: AmmoAvailability
    upgraded_skyward_strike: UpgradedSkywardStrike
    fast_air_meter: FasterAirMeterDrain
    enable_heart_drops: HeartDrops
    damage_multiplier: DamageMultiplier
    starting_sword: StartingSword
    starting_tablet_count: StartingTabletCount
    starting_crystal_packs: StartingGratitudeCrystalPacks
    starting_bottles: StartingEmptyBottles
    starting_heart_containers: StartingHeartContainers
    starting_heart_pieces: StartingHeartPieces
    starting_tadtones: StartingTadtoneCount
    random_starting_item: RandomStartingItem
    start_with_hylian_shield: StartWithHylianShield
    full_starting_wallet: StartWithFullWallet
    max_starting_bugs: StartWithMaxBugs
    max_starting_treasures: StartWithMaxTreasures
    hint_distribution: HintDistribution
    song_hints: SongHints
    chest_dowsing: ChestDowsing
    dungeon_dowsing: AllowDowsingInDungeons
    impa_sot_hint: PastImpaStoneOfTrialsHint
    #cube_sots: SeparateCubeSotS
    #precise_item: PreciseItemHints
    starting_items: StartInventoryPool
    death_link: DeathLink
    progression_balancing: SSProgressionBalancing

