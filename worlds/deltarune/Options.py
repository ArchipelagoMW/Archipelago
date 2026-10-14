from enum import StrEnum

from Options import Choice, FreeText, Toggle, Range, PerGameCommonOptions, NamedRange, OptionGroup
from dataclasses import dataclass


# region No Group
class ProgressionBalancing(NamedRange):
    """
    ATTEMPTS TO BALANCE THE PROGRESSION OF YOUR ITEMS.

    SETTING THE VALUE LOWER WILL RESULT IN MORE WAITING TO RECIEVE ITEMS.

    SETTING THE VALUE HIGHER WILL RESULT IN LESS WAITING TO RECIEVE ITEMS.
    """

    default = 50
    range_start = 0
    range_end = 99
    display_name = "Progression Balancing"
    rich_text_doc = True
    special_range_names = {
        "disabled": 0,
        "normal": 50,
        "extreme": 99,
    }


class Accessibility(Choice):
    """
    SETS THE RULES FOR THE ABILITY TO REACH ALL ITEMS.

    - **Full** *GUARANTEES THAT ALL ITEMS CAN BE OBTAINED.*

    - **Minimal** *GUARANTEES ONLY WHAT IS NECESSARY, BUT NO MORE.*
    """

    display_name = "Accessibility"
    rich_text_doc = True
    option_full = 0
    option_minimal = 2
    alias_none = 2
    alias_locations = 0
    alias_items = 0
    default = 0

class OptionsCreatorReminder(Choice): # Yeah, I can't believe we need this either...
    """
    EACH OPTION WILL BE DESCRIPTIVE AS TO WHAT IT MODIFIES.

    WITH YOUR CURSOR POINTER, HOVER OVER THE NAME OF EACH OPTION TO VIEW ITS DESCRIPTION.
    
    CONTEMPLATE THE TEXT ACCORDINGLY AND MAKE YOUR CHOICE.

    (If you editing this with notepad or something instead of Options Creator, you can ignore this.)
    """

    display_name = "(Hover Over to) Read Option Description"
    option_understood = 0


class HaveStarwalker(Toggle):
    """
    THE ORIGINAL ONE BE PRESENT UPON STARTING A NEW SAVE.

    **star              walker :D**
    """

    display_name = "Always Have Starwalker"
    default = 1


class ShuffleOST(Toggle):
    """
    THE BACKGROUND MUSIC WILL BE UNLIKE HOW YOU RECALL IT.

    (Just a basic music randomizer.)
    (Will likely not include things like the rhythm games or the Sweet Cap'n Cakes fight.)
    (Also, expect things like multiple soundtracks overlapping. This isn't a bug, it's just how the game is programmed.)
    """

    display_name = "[BETA] Shuffle OST"
    default = 0


# endregion

# region Gameplay


class UnnerfPinkTwinRibbon(Toggle):
    """
    THE PINK AND THE TWIN RIBBONS WILL NOT BE DOWNGRADED PAST THE SECOND CHAPTER.

    (If you don't know, the pink/twin ribbon gets nerfed hard if you equip a second one in chapter 3+.)
    (Though, keep in mind it was definitely nerfed for a reason. Equipping these ribbons all at once make some battles a cakewalk.)
    """

    display_name = "Un-nerf Pink/Twin Ribbon"
    default = 1


class BetterOdds(Toggle):
    """
    SHOULD EVENTS RELIANT ON LUCK HAVE BETTER ODDS TO HAPPEN?

    - **Chapter 1&2 Eggs**
    """

    display_name = "Better Odds"
    default = 1


class RockVideoSanity(Choice):
    """
    YOUR RANK IN CONCERTS WILL COUNT AS LOCATIONS.

    *(Also named Lightners Live concerts, Rhythm minigames, etc)*
    *(This is separate Chapter 3's Board 2 ranks)*
    """

    display_name = "Rock Video Sanity"
    option_false = 0
    option_normal_only = 1
    option_true = 2


class ExcludeTRankRockVideo(Toggle):
    """
    THE HIGHEST RANK OF THE CONCERTS WILL BE EXCLUDED FROM CONTAINING AN IMPORTANT ITEM.

    (Of course, this only applies if you set Rocky Video Sanity to true.)
    """

    display_name = "Exclude T Rank for rock video"
    default = 1


class ExcludeZRankRockVideo(Toggle):
    """
    THE LOWEST RANK OF THE CONCERTS WILL BE EXCLUDED FROM CONTAINING AN IMPORTANT ITEM.

    (Of course, this only applies if you set Rocky Video Sanity to true.)
    """

    display_name = "Exclude Z Rank for rock video"
    default = 1


# endregion

# region Chapter 3


class IncludeChapter3(Toggle):
    """
    DO YOU WISH TO PLAY CHAPTER 3?

    *(Items from this chapter will also be included)*
    """

    display_name = "Include Chapter 3"
    default = 1


class MacGuffinChapter3(Range):
    """
    A NEW ROADBLOCK WILL APPEAR BEFORE THE FINAL BOSS OF CHAPTER 3.

    THIS OPTION DETERMINES HOW MANY OF THESE ITEMS WILL BE REQUIRED TO PROGRESS.

    (Remote Batteries)
    """

    display_name = "Macguffin Chapter 3 Amount"
    default = 0
    range_start = 0
    range_end = 10


class RandomizeSWORDRoute(Toggle):
    """
    LOCATIONS RECEIVED IN THE ORIGINAL GAME OF THE THIRD CHAPTER WILL BE RANDOMIZED.
    """

    display_name = "Randomize SWORD route"
    default = 0


class ShadowMantleHolderAsSecretBoss(Toggle):
    """
    SHOULD THE FINAL ENEMY OF THE ORIGINAL GAME BE TREATED AS A SHADOW CRYSTAL BOSS?

    (This option makes Chapter 3's Shadow Mantle Holder Fight mandatory if you turn Secret Bosses to Mandatory.)
    """

    display_name = "Shadow Mantle Holder as secret boss"
    default = 0


class IncludeShadowMantle(Toggle):
    """
    THE SHADOW MANTLE WILL BE IN THE RANDOM ITEM POOL OF THE THIRD CHAPTER.

    - **False** *The Shadow Mantle is the reward for the Shadow Mantle Holder/ERAM fight, but isn't in logic for the knight*
    - **True** *The Shadow Mantle will be in the itempool in logic before Knight fight*
    """

    display_name = "Include Shadow Mantle in itempool"
    default = 1


class AllowDoomBoardWithoutAllCharacters(Toggle):
    """
    UNLOCKING ALL THREE HEROES WILL NOT BE REQUIRED TO ACCESS THE FINAL BOARD OF THE THIRD CHAPTER.

    *(Usually, all three characters would need to be unlocked to access Doom Board in chapter 3)*
    *(This is because the board has an ACT that requires everyone in order to progress.)*
    *(If you want to disable this requirement, set this option to true.)*
    *(However, this will make it so that you might have to do fights such as the Knight with only one or two characters unlocked.)*

    *(Of course, this only applies if you set Randomize Characters to true.)*
    """

    display_name = "Doom Board in logic without all characters"
    default = 0


class ExcludeTRankBoard(Toggle):
    """
    THE HIGHEST RANK OF THE THIRD CHAPTER FOR BOARDS WILL BE EXCLUDED FROM CONTAINING AN IMPORTANT ITEM.
    """

    display_name = "Exclude T Rank for boards"
    default = 1


class ExcludeZRankBoard(Toggle):
    """
    THE LOWEST RANK OF THE THIRD CHAPTER FOR BOARDS WILL BE EXCLUDED FROM CONTAINING AN IMPORTANT ITEM.
    """

    display_name = "Exclude Z Rank for boards"
    default = 1


class PhysicalChallengeRankSanity(Toggle):
    """
    THE RANKS ACQUIRED ON THE LORD OF SCREEN'S CHALLENGES WILL BE COUNTED AS LOCATIONS.
    """

    display_name = "Physical Challenge Sanity"
    default = 0


class ExcludeTRankPhysicalChallenge(Toggle):
    """
    THE HIGHEST RANK OF THE THIRD CHAPTER FOR CHALLENGES WILL BE EXCLUDED FROM CONTAINING AN IMPORTANT ITEM.
    """

    display_name = "Exclude T Rank for physical challenges"
    default = 1


class ExcludeZRankPhysicalChallenge(Toggle):
    """
    THE LOWEST RANK OF THE THIRD CHAPTER FOR CHALLENGES WILL BE EXCLUDED FROM CONTAINING AN IMPORTANT ITEM.
    """

    display_name = "Exclude Z Rank for physical challenges"
    default = 1


# endregion

class ChosenRoute(Choice):
    """
    CHOOSE THE ROUTE THAT YOU PREFER.

    - **Normal Route** *Progress through the story normally.*
    - **Weird Route** *Proceed through the "Weird Route" storyline. Can we rename this to Side B yet*
    - **All Recruits** *Progress through the story normally, but you have to recruit everyone to complete the chapter.*
    - **Both Routes** *Beat each chapter with All Recruits, as well as chapter 2 and 5 a second time for their Side B ending.*
    """

    display_name = "Chosen Route"
    option_all_recruits = 0
    option_weird_route = 1
    option_both_all_recruits_and_weird_route = 2
    option_normal_route = 3
    default = option_normal_route


class RecruitsSanity(Toggle):
    """
    WILL GAINING RECRUITS COUNT AS LOCATIONS?

    (Forced enabled if All recruits is selected.)
    (If you choose Weird Route, specifically the recruits in Cyber City will be force disabled.)
    """

    display_name = "Recruits Sanity"
    default = False


class LoseRecruitsSanity(Toggle):
    """
    WILL LOSING RECRUITS COUNT AS LOCATIONS?

    (If you choose Weird Route, specifically the recruits you lose in Cyber City will be force enabled to avoid a generation fail.)
    """

    display_name = "Lose recruits Sanity"
    default = False


class RandomizeChapters(Choice):
    """
    HOW WILL YOU PROGRESS THROUGH THE CHAPTERS?

    - **In Order** *The next chapter will be unlocked once you complete the one you're in.*
    - **Randomized** *Chapters are unlocked through getting items. You'll be expected to move in-between chapters a lot.*
    - **All Unlocked** *All chapters are unlocked from the start. You will be expected to play through another chapter once stuck.*

    (The goal is closing the final fountain of each chapter enabled.)
    """

    display_name = "Randomize Chapters"
    option_in_order = 0
    option_randomized = 1
    option_all_unlocked = 2
    default = option_all_unlocked


class StartingChapter(Choice):
    """
    WHICH CHAPTER WILL BEGIN THE JOURNEY?

    (This only applies if you set Randomize Chapters to random.)
    """

    display_name = "Starting Random Chapter"
    option_random_chapter = 0
    option_chapter_1 = 1
    option_chapter_2 = 2
    option_chapter_3 = 3
    option_chapter_4 = 4
    option_chapter_5 = 5
    default = option_random_chapter


class RandomSafetyChapterIncluded(Toggle):
    """
    SHOULD NO CHAPTERS BE ENABLED, A RANDOM ONE WILL BE GRANTED.

    (Should be enabled if you choose to randomly enable chapters, i.e. through weights)
    """

    display_name = "RANDOM SAFETY : Chapter inclusion"
    default = False


class RandomizeSecretBosses(Choice):
    """
    LOCATIONS GIVEN BY SHADOW CRYSTAL BOSSES WILL BE RANDOMIZED OR EVEN REQUIRED.

    - **Mandatory** *Secret Boss rewards will be randomized, and they will be required to beat to access the fountain.*

    *Secret bosses are: Jevil, Spamton Neo, Chapter 3 Knight, Hammer of Justice, Pink*

    (Yeah yeah I know the knight fight isn't technically secret. SHUT IT!!!!)
    """

    display_name = "Randomize Secret Bosses"
    option_false = 0
    option_true = 1
    option_mandatory = 2
    default = option_false


class ItemBalancing(Toggle):
    """
    IF AN ITEM IS OBTAINED EARLY, ITS POWER WILL BE SCALED DOWN.

    (Getting Chapter 5 items in Chapter 1 can make enemies die in a single hit and make you take less than 10 damage each hit.)
    (If you don't want the game to be THAT easy, then set this option to true.)

    (Can be toggled in-game)
    """

    display_name = "ItemBalancing"
    default = 0


class IncludeHiddenItems(Toggle):
    """
    RANDOMIZES ITEMS THAT ARE CONSIDERABLY MORE DIFFICULT TO FIND OR TEDIOUS TO OBTAIN.

    - **Golden Prizes**
    - **Eggs**
    - **Dog Dollars**
    - **Moss**
    - **Bromide F**
    """

    display_name = "Randomize Grindy/Hidden Items"
    default = 0


class IncludeSecretBossesItemsRequirement(Toggle):
    """
    RANDOMIZES ITEMS THAT ARE NECESSARY TO ACCESS SECRET BOSSES.

    - **Broken Keys**
    - **Door Key**
    - **KeyGen**
    - **Empty Disk**
    - **Pink Coins**
    - **Pink Key**

    *(For MANTLE items, see the Randomize SWORD Route option)*
    """

    display_name = "Randomize Items required for Secret Bosses"
    default = 0


class DoorKeyFromBrokenKeys(Toggle):
    """
    THE JOKER'S DOOR KEY WILL BE ACQUIRED BY FUSING THE THREE BROKEN KEY PIECES.

    *(Plando "Door Key" to "CH1: Bake Sale - Repair Door Key")*
    *(Otherwise, it could be anywhere. This option only matters if you randomize secret boss requirement items.)*
    *(Of course, this only applies if you play Chapter 1.)*
    """

    display_name = "Door Key from Broken Keys"
    default = 1


class MysteryKeyFromPinkCoins(Toggle):
    """
    THE MYSTERIOUS PINK KEY WILL BE PURCHASED FOR TEN PINK COINS.

    *(Plando "MysteryKey" to "CH5: Cliffs Shop Item #4")*
    *(Otherwise, it could be anywhere. This option only matters if you randomize secret boss requirement items.)*
    *(Of course, this only applies if you play Chapter 5.)*
    """

    display_name = "MysteryKey from Pink Coins"
    default = 1


class RemoveStartingEquipment(Toggle):
    """
    SHOULD STARTING FROM A CHAPTER MAKE THE HEROES HAVE NOTHING?

    *(Normally if you start a save file on a chapter, you'll start with some equipment from the previous two chapters.)*
    *(If this option is set to true, you'll start every chapter like chapter 1, with no armors and only the starting weapons.)*
    """

    display_name = "Remove Starting Equipment"
    default = 0


class IncludeChapter1(Toggle):
    """
    DO YOU WISH TO PLAY CHAPTER 1?

    *(Items from this chapter will also be included)*
    """

    display_name = "Include Chapter 1"
    default = 1


class Chapter1Recruit(Toggle):
    """
    THE SYSTEM TO RECRUIT ENEMIES WILL BE PRESENT IN THE FIRST CHAPTER.
    """

    display_name = "Recruits/Lost for chapter 1"
    default = 1


class IncludeChapter2(Toggle):
    """
    DO YOU WISH TO PLAY CHAPTER 2?

    *(Items from this chapter will also be included)*
    """

    display_name = "Include Chapter 2"
    default = 1


class IncludeChapter4(Toggle):
    """
    DO YOU WISH TO PLAY CHAPTER 4?

    *(Items from this chapter will also be included)*
    """

    display_name = "Include Chapter 4"
    default = 1


class IncludeChapter5(Toggle):
    """
    DO YOU WISH TO PLAY CHAPTER 5?

    *(Items from this chapter will also be included)*
    """

    display_name = "Include Chapter 5"
    default = 1


class MacGuffinChapter1(Range):
    """
    A NEW ROADBLOCK WILL APPEAR BEFORE THE FINAL BOSS OF CHAPTER 1.

    THIS OPTION DETERMINES HOW MANY OF THESE ITEMS WILL BE REQUIRED TO PROGRESS.

    (King-Shaped Key Pieces)
    """

    display_name = "Macguffin Chapter 1 Amount"
    default = 0
    range_start = 0
    range_end = 10


class MacGuffinChapter2(Range):
    """
    A NEW ROADBLOCK WILL APPEAR BEFORE THE FINAL BOSS OF CHAPTER 2.

    THIS OPTION DETERMINES HOW MANY OF THESE ITEMS WILL BE REQUIRED TO PROGRESS.

    (KeyGen 2 Segments)
    """

    display_name = "Macguffin Chapter 2 Amount"
    default = 0
    range_start = 0
    range_end = 10


class MacGuffinChapter4(Range):
    """
    A NEW ROADBLOCK WILL APPEAR BEFORE THE FINAL BOSS OF CHAPTER 4.

    THIS OPTION DETERMINES HOW MANY OF THESE ITEMS WILL BE REQUIRED TO PROGRESS.

    (Combination Lock Digits)
    """

    display_name = "Macguffin Chapter 4 Amount"
    default = 0
    range_start = 0
    range_end = 10


class MacGuffinChapter5(Range):
    """
    A NEW ROADBLOCK WILL APPEAR BEFORE THE FINAL BOSS OF CHAPTER 5.

    THIS OPTION DETERMINES HOW MANY OF THESE ITEMS WILL BE REQUIRED TO PROGRESS.

    (Jarona Lessons)
    """

    display_name = "Macguffin Chapter 5 Amount"
    default = 3
    range_start = 0
    range_end = 10


class MacGuffinExtra(Range):
    """
    THE AMOUNT OF EXTRA ITEMS IN THE ITEMPOOL TO UNBLOCK THE ROAD TO FINAL BOSSES.

    *(So, if you choose to have 3 macguffin items in Chapter 1 and set this option to 1,)*
    *(you'll have 4 macguffin items in the pool, but you'll still only need 3 to progress.)*
    """

    display_name = "Extra MacGuffin Amount"
    default = 1
    range_start = 0
    range_end = 5


class DeathLink(Toggle):
    """
    YOUR FAILURE CAUSES THE FAILURE OF EVERYONE WHO HAS ENABLED THIS OPTION.

    TO COMPLIMENT, THE REVERSE IS TRUE AS WELL.

    (Can be toggled in-game)
    """

    display_name = "Death Link"
    default = 0


class DeathLinkGroup(FreeText):
    """
    ONLY THOSE IN THIS GROUP WILL BE PART OF YOUR DEATH LINK.

    *(Games that don't support this option are part of the empty group.)*
    """


class DamageLink(Toggle):
    """
    GETTING HARMED WILL CAUSE THE HARM OF EVERYONE WHO HAS ENABLED THIS OPTION.

    TO COMPLIMENT, THE REVERSE IS TRUE AS WELL.

    (Can be toggled in-game)
    """

    display_name = "Damage Link"
    default = 0


class DamageLinkGroup(FreeText):
    """
    ONLY THOSE IN THIS GROUP WILL BE A PART OF YOUR DAMAGE LINK.

    *(Games that don't support this option are part of the empty group.)*
    """

    display_name = "Damage Link Group"
    default = ""


filler_weight_range_names = {"common": 50, "uncommon": 25, "rare": 10, "very rare": 5, "extremely rare": 1, "none": 0}


class FillerHealingWeight(NamedRange):
    """
    DETERMINES HOW OFTEN HEALING ITEMS WILL APPEAR COMPARED TO OTHERS ITEMS.
    """

    display_name = "Healing Items Weights"
    range_start = 0
    range_end = 99
    default = filler_weight_range_names["common"]
    rich_text_doc = True
    special_range_names = filler_weight_range_names


class FillerCurrencyWeight(NamedRange):
    """
    DETERMINES HOW OFTEN ALL CURRENCIES WILL APPEAR COMPARED TO OTHERS ITEMS.
    """

    display_name = "Currency Weights"
    range_start = 0
    range_end = 99
    default = filler_weight_range_names["uncommon"]
    rich_text_doc = True
    special_range_names = filler_weight_range_names


class TrapWeight(NamedRange):
    """
    DETERMINES HOW OFTEN TRAPS WILL APPEAR COMPARED TO OTHERS ITEMS.
    """

    display_name = "Trap Weights"
    range_start = 0
    range_end = 99
    default = filler_weight_range_names["rare"]
    rich_text_doc = True
    special_range_names = filler_weight_range_names


class FillerArmorWeight(NamedRange):
    """
    DETERMINES HOW OFTEN ARMOR ITEMS WILL APPEAR COMPARED TO OTHERS ITEMS.
    """

    display_name = "Armors Weights"
    range_start = 0
    range_end = 99
    default = filler_weight_range_names["rare"]
    rich_text_doc = True
    special_range_names = filler_weight_range_names


class FillerTensionWeight(NamedRange):
    """
    DETERMINES HOW OFTEN TENSION ITEMS WILL APPEAR COMPARED TO OTHERS ITEMS.
    """

    display_name = "Tension Items Weights"
    range_start = 0
    range_end = 99
    default = filler_weight_range_names["very rare"]
    rich_text_doc = True
    special_range_names = filler_weight_range_names


class FillerSMILEWeight(NamedRange):
    """
    DETERMINES HOW OFTEN IT WILL SMILE.

    *(SMILE only sends a silly message.)*
    *(...Right?)*
    """

    display_name = "SMILE Weight"
    range_start = 0
    range_end = 99
    default = filler_weight_range_names["extremely rare"]
    rich_text_doc = True
    special_range_names = filler_weight_range_names


class ProgressiveKrisWeapons(Toggle):
    """
    THE WEAPONS RECEIVED FOR THE CAGE WILL BE IN SEQUENTIAL ORDER OF RISING POWER.
    """

    display_name = "Progressive Kris Weapons"
    default = 0


class ProgressiveSusieWeapons(Toggle):
    """
    THE WEAPONS RECEIVED FOR THE GIRL WILL BE IN SEQUENTIAL ORDER OF RISING POWER.
    """

    display_name = "Progressive Susie Weapons"
    default = 0


class ProgressiveRalseiWeapons(Toggle):
    """
    THE WEAPONS RECEIVED FOR THE PRINCE WILL BE IN SEQUENTIAL ORDER OF RISING POWER.
    """

    display_name = "Progressive Ralsei Weapons"
    default = 0


class ProgressiveNoelleWeapons(Toggle):
    """
    THE FORBIDDEN RINGS WILL BE IN SEQUENTIAL ORDER OF RISING POWER.
    """

    display_name = "Progressive Noelle Weapons"
    default = 0


class UnlockCharacters(Choice):
    """
    THE ABILITY TO USE HEROES IN COMBAT SEQUENCIES WILL NEED TO BE UNLOCKED.

    *(If someone isn't unlocked, they'll be at -666HP, and you can't use them in battle.)*
    *(If nobody is unlocked, then it will immediately be the enemy's turn, but you still get one hit to live.)*

    **(Of course, missing any number of characters makes battles exponentially more difficult.)**
    **(Expect things like battles taking 10 or more turns if you only have one character unlocked!)**
    **(ONLY TURN THIS TO TRUE IF YOU ARE SKILLED AT THE GAME.)**
    """

    display_name = "[HARD MODE] Unlock Characters"
    option_false = 0
    option_true = 1
    option_except_kris = 2
    default = option_false


class StartWithRandomCharacter(Toggle):
    """
    IF THE ABILITY TO USE HEROES NEEDS TO BE UNLOCKED, WILL YOU BEGIN WITH ONE OR NONE?

    *(Only if you chose true on unlock character option. If you chose "Except Kris" this doesn't apply either.)*
    *(Cannot be Noelle.)*
    """

    display_name = "Start with a random character"
    default = 1


class IncludeUnusedItems(Choice):
    """
    CERTAIN ITEMS ARE NOT NORMALLY PRESENT.
    WILL THEY NOW BE WITH THE REST?

    - **True without EveryBodyWeapon** *(Include Unused items except for EverybodyWeapon.)*
    *(It's pretty clear EverybodyWeapon was only meant for debug purposes, as it's pretty overpowered.)*
    *(Turn on True Without Everybody weapon if you don't want it in the item pool.)*
    """

    display_name = "Include Unused Items"
    option_false = 0
    option_true = 1
    option_true_without_everybodyweapon = 2
    default = option_false


class IncludeUnusedItemsOptions(StrEnum):
    false = "false"
    true = "true"
    true_without_everybodyweapon = "true_without_everybodyweapon"


class IncludeMike(Choice):
    """
    WILL THE DEFEAT OF THE MICROPHONE IMITATORS AS WELL AS THEIR GAMES COUNT AS CHECK LOCATIONS?

    (Reminder that Mike needs a mouse to be played to its fullest.)
    (Feel free to disable this if you don't plan on having one, i.e. Steam Deck users.)
    """

    display_name = "Include Mike"
    option_false = 0
    option_battle_only = 1
    option_battle_and_games = 2
    default = option_false


class ExcludeMikePlatinum(Toggle):
    """
    WILL THE PLATINUM TROPHY IN THE MICROPHONE IMITATORS' GAMES BE KEPT AWAY FROM HOLDING AN IMPORTANT ITEM?
    """

    display_name = "Exclude Platinum trophy"
    default = 0


class IncludeMikeOptions(StrEnum):
    false = "false"
    battle_only = "battle_only"
    battle_and_games = "battle_and_games"


class UnlockFunGangActions(Toggle):
    """
    THE ABILITY TO USE THE ACTIONS OF THE GIRL, THE PRINCE, AND THE WHITE CLOAK WILL BE AN ITEM.
    """

    display_name = "Unlock S/R/N-Actions"
    default = 0


# region Logic Difficulty


class SpeedrunGlitchesAsLogic(Toggle):
    """
    THE FAST LITTLE BOYS WAY TO PROGRESS MAY BE THE EXPECTED WAY TO PROGRESS.

    (All reasonable glitches will now be in logic.)
    (This includes: Wrong Warp, Bagel Overflow, interaction slide, etc.)
    (This doesn't includes: ARMS)
    (This will also add locations that can be obtained with Singapore Wrong Warp in chapter 2 Weird Route.)
    (Do not forget to save on multiple slot to still have access on earlier event that might not happen anymore if you play with the plot value.)
    (Reminder that Bagel Overflow was re-implemented.)
    **(ONLY TURN THIS TO TRUE IF YOU ARE KNOWLEDGEABLE.)**
    """

    display_name = "[HARD MODE] Speedrun glitches as Logic"
    default = 0


class NoHitAsLogic(Toggle):
    """
    SHOULD YOU HAVE NO CHARACTERS, TAKING NO DAMAGE WILL BE EXPECTED.

    (Fights or sections that require you no no-hit them will now be in logic.)
    (This includes: Mike fight, Knight Climb, Gerson.)
    (Reminder that Chapter 1 Lancer fight is always in logic no-hit.)
    **(ONLY TURN THIS TO TRUE IF YOU ARE EXTREMELY SKILLED AT THE GAME.)**

    *(Of course, this only applies if you set Unlock Characters to true.)*
    """

    display_name = "[HARD MODE] No Hit as Logic"
    default = 0


class AnnoyingFarmingAsLogic(Toggle):
    """
    TASKS TAKING A GREAT AMOUNT OF TIME TO ACCOMPLISH WILL BE EXPECTED.

    (Annoying farming will now be in logic.)
    (This include replaying Chapter 3 Board 1 multiple times for recruiting 25 shadowguys or spamming spare to recruit enemies if you don't have any other way to spare them.)
    """

    display_name = "[HARD MODE] Annoying farming as Logic"
    default = 0

# endregion

deltarune_option_groups = [
    OptionGroup(
        "Goal",
        [
            ChosenRoute,
            RecruitsSanity,
            LoseRecruitsSanity,
            RandomizeSecretBosses,
            MacGuffinExtra,
        ],
    ),
    OptionGroup(
        "Chapters",
        [
            RandomizeChapters,
            RandomSafetyChapterIncluded,
            StartingChapter,
        ],
    ),
    OptionGroup("Chapter 1", [IncludeChapter1, MacGuffinChapter1, Chapter1Recruit]),
    OptionGroup("Chapter 2", [IncludeChapter2, MacGuffinChapter2]),
    OptionGroup(
        "Chapter 3",
        [
            IncludeChapter3,
            MacGuffinChapter3,
            RandomizeSWORDRoute,
            ShadowMantleHolderAsSecretBoss,
            IncludeShadowMantle,
            ExcludeTRankBoard,
            ExcludeZRankBoard,
            AllowDoomBoardWithoutAllCharacters,
            PhysicalChallengeRankSanity,
            ExcludeTRankPhysicalChallenge,
            ExcludeZRankPhysicalChallenge,
        ],
    ),
    OptionGroup("Chapter 4", [IncludeChapter4, MacGuffinChapter4, IncludeMike, ExcludeMikePlatinum]),
    OptionGroup("Chapter 5", [IncludeChapter5, MacGuffinChapter5]),
    OptionGroup(
        "Items",
        [
            IncludeHiddenItems,
            IncludeSecretBossesItemsRequirement,
            DoorKeyFromBrokenKeys,
            MysteryKeyFromPinkCoins,
            IncludeUnusedItems,
            ProgressiveKrisWeapons,
            ProgressiveSusieWeapons,
            ProgressiveRalseiWeapons,
            ProgressiveNoelleWeapons,
            UnlockCharacters,
            StartWithRandomCharacter,
            UnlockFunGangActions,
        ],
    ),
    OptionGroup(
        "Gameplay",
        [
            BetterOdds,
            ItemBalancing,
            RemoveStartingEquipment,
            UnnerfPinkTwinRibbon,
            RockVideoSanity,
            ExcludeZRankRockVideo,
            ExcludeTRankRockVideo,
        ],
    ),
    OptionGroup(
        "Logic Difficulty",
        [SpeedrunGlitchesAsLogic, NoHitAsLogic, AnnoyingFarmingAsLogic],
    ),
    OptionGroup("Links", [DeathLink, DeathLinkGroup, DamageLink, DamageLinkGroup]),
    OptionGroup(
        "Fillers Weight",
        [
            FillerHealingWeight,
            FillerCurrencyWeight,
            TrapWeight,
            FillerArmorWeight,
            FillerTensionWeight,
            FillerSMILEWeight,
        ],
    ),
]


@dataclass
class DeltaruneOptions(PerGameCommonOptions):
    # No Group
    options_creator_reminder: OptionsCreatorReminder
    progression_balancing: ProgressionBalancing
    accessibility: Accessibility
    have_starwalker: HaveStarwalker
    shuffle_ost: ShuffleOST

    # Goal
    chosen_route: ChosenRoute
    recruits_sanity: RecruitsSanity
    lose_recruits_sanity: LoseRecruitsSanity
    randomize_secret_bosses: RandomizeSecretBosses
    macguffin_extra: MacGuffinExtra

    # Chapters
    randomize_chapters: RandomizeChapters
    random_safety_chapter_inclusion: RandomSafetyChapterIncluded
    starting_chapter: StartingChapter

    # Chapter 1
    include_chapter_1: IncludeChapter1
    macguffin_chapter_1: MacGuffinChapter1
    chapter_1_recruit: Chapter1Recruit

    # Chapter 2
    include_chapter_2: IncludeChapter2
    macguffin_chapter_2: MacGuffinChapter2

    # Chapter 3
    include_chapter_3: IncludeChapter3
    macguffin_chapter_3: MacGuffinChapter3
    randomize_sword_route: RandomizeSWORDRoute
    shadow_mantle_holder_as_secret_boss: ShadowMantleHolderAsSecretBoss
    include_shadow_mantle: IncludeShadowMantle
    exclude_t_rank_board: ExcludeTRankBoard
    exclude_z_rank_board: ExcludeZRankBoard
    physical_challenge_rank_sanity: PhysicalChallengeRankSanity
    exclude_t_rank_physical_challenge: ExcludeTRankPhysicalChallenge
    exclude_z_rank_physical_challenge: ExcludeZRankPhysicalChallenge
    allow_doom_board_without_all_characters: AllowDoomBoardWithoutAllCharacters

    # Chapter 4
    include_chapter_4: IncludeChapter4
    macguffin_chapter_4: MacGuffinChapter4
    include_mike: IncludeMike
    exclude_mike_platinum: ExcludeMikePlatinum

    # Chapter 5
    include_chapter_5: IncludeChapter5
    macguffin_chapter_5: MacGuffinChapter5

    # Items
    include_hidden_items: IncludeHiddenItems
    include_secret_bosses_items_requirement: IncludeSecretBossesItemsRequirement
    mysterykey_from_pink_coins: MysteryKeyFromPinkCoins
    door_key_from_broken_keys: DoorKeyFromBrokenKeys
    include_unused_items: IncludeUnusedItems
    progressive_kris_weapons: ProgressiveKrisWeapons
    progressive_susie_weapons: ProgressiveSusieWeapons
    progressive_ralsei_weapons: ProgressiveRalseiWeapons
    progressive_noelle_weapons: ProgressiveNoelleWeapons
    unlock_characters: UnlockCharacters
    start_with_random_character: StartWithRandomCharacter
    unlock_fun_gang_actions: UnlockFunGangActions

    # Gameplay
    better_odds: BetterOdds
    remove_starting_equipment: RemoveStartingEquipment
    item_balancing: ItemBalancing
    pink_twin_ribbon_unnerf: UnnerfPinkTwinRibbon
    rock_video_sanity: RockVideoSanity
    exclude_t_rank_rock_video: ExcludeTRankRockVideo
    exclude_z_rank_rock_video: ExcludeZRankRockVideo

    # Logic Difficulty
    speedrun_gliches_as_logic: SpeedrunGlitchesAsLogic
    nohit_as_logic: NoHitAsLogic
    annoying_farming_as_logic: AnnoyingFarmingAsLogic

    # Links
    death_link: DeathLink
    death_link_group: DeathLinkGroup
    damage_link: DamageLink
    damage_link_group: DamageLinkGroup

    # Fillers Weight
    filler_healing_weight: FillerHealingWeight
    filler_currency_weight: FillerCurrencyWeight
    trap_weight: TrapWeight
    filler_armor_weight: FillerArmorWeight
    filler_tension_weight: FillerTensionWeight
    filler_smile_weight: FillerSMILEWeight


options_presets = {
    "Classic All Recruits": {"chosen_route": "all_recruits", "recruits_sanity": True},
    "Classic Weird Route": {"chosen_route": "weird_route", "recruits_sanity": False, "lose_recruits_sanity": True},
}
