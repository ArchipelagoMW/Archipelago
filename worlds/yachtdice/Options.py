from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range


class GameDifficulty(Choice):
    """
    Difficulty. This option determines how difficult the scores are to achieve.
    Easy: for beginners. No luck required, just roll the dice and have fun. Lower final goal.
    Medium: intended difficulty. If you play smart, you will finish the game without any trouble.
    Hard: you will need to play smart and be lucky.
    Extreme: really hard mode, which requires many brain wrinkles and insane luck. NOT RECOMMENDED FOR MULTIWORLDS.
    """

    display_name = "Game difficulty"
    option_easy = 1
    option_medium = 2
    option_hard = 3
    option_extreme = 4
    default = 2


class ScoreForLastCheck(Range):
    """
    The items in the item pool will always allow you to reach a score of 1000.
    By default, the last check is also at a score of 1000.
    However, you can set the score for the last check to be lower. This will make the game shorter and easier.
    """

    display_name = "Score for last check"
    range_start = 500
    range_end = 1000
    default = 1000


class ScoreForGoal(Range):
    """
    This option determines what score you need to reach to finish the game.
    It cannot be higher than the score for the last check (if it is, this option is changed automatically).
    """

    display_name = "Score for goal"
    range_start = 500
    range_end = 1000
    default = 777


class MinimalNumberOfDiceAndRolls(Choice):
    """
    The minimal number of dice and rolls in the pool.
    These are guaranteed, unlike the later items.
    You can never get more than 8 dice and 5 rolls.
    You start with one dice and one roll.
    """

    display_name = "Minimal number of dice and rolls in pool"
    option_5_dice_and_3_rolls = 2
    option_5_dice_and_5_rolls = 3
    option_6_dice_and_4_rolls = 4
    option_7_dice_and_3_rolls = 5
    option_8_dice_and_2_rolls = 6
    default = 2


class NumberDiceFragmentsPerDice(Range):
    """
    Dice can be split into fragments, gathering enough will give you an extra dice.
    You start with one dice, and there will always be one full dice in the pool.
    The other dice are split into fragments, according to this option.
    Setting this to 1 fragment per dice just puts "Dice" objects in the pool.
    """

    display_name = "Number of dice fragments per dice"
    range_start = 1
    range_end = 5
    default = 4


class NumberRollFragmentsPerRoll(Range):
    """
    Rolls can be split into fragments, gathering enough will give you an extra roll.
    You start with one roll, and there will always be one full roll in the pool.
    The other rolls are split into fragments, according to this option.
    Setting this to 1 fragment per roll just puts "Roll" objects in the pool.
    """

    display_name = "Number of roll fragments per roll"
    range_start = 1
    range_end = 5
    default = 4


class AlternativeCategories(Range):
    """
    There are 16 default categories, but there are also 16 alternative categories.
    These alternative categories can be randomly selected to replace the default categories.
    They are a little strange, but can give a fun new experience.
    In the game, you can hover over categories to check what they do.
    This option determines the number of alternative categories in your game.
    """

    display_name = "Number of alternative categories"
    range_start = 0
    range_end = 16
    default = 0


class ChanceOfDice(Range):
    """
    The item pool is always filled in such a way that you can reach a score of 1000.
    Extra progression items are added that will help you on your quest.
    You can set the weight for each extra progressive item in the following options.

    Of course, more dice = more points!
    """

    display_name = "Weight of adding Dice"
    range_start = 0
    range_end = 100
    default = 5


class ChanceOfRoll(Range):
    """
    With more rolls, you will be able to reach higher scores.
    """

    display_name = "Weight of adding Roll"
    range_start = 0
    range_end = 100
    default = 20


class ChanceOfFixedScoreMultiplier(Range):
    """
    Getting a Fixed Score Multiplier will boost all future scores by 10%.
    """

    display_name = "Weight of adding Fixed Score Multiplier"
    range_start = 0
    range_end = 100
    default = 30


class ChanceOfStepScoreMultiplier(Range):
    """
    The Step Score Multiplier boosts your multiplier after every roll by 1%, and resets on sheet reset.
    So, keep high scoring categories for later to get the most out of them.
    By default, this item is not included. It is fun however, you just need to know the above strategy.
    """

    display_name = "Weight of adding Step Score Multiplier"
    range_start = 0
    range_end = 100
    default = 0


class ChanceOfDoubleCategory(Range):
    """
    This option allows categories to appear multiple times.
    Each time you get a category after the first, its score value gets doubled.
    """

    display_name = "Weight of adding Category copy"
    range_start = 0
    range_end = 100
    default = 50


class ChanceOfPoints(Range):
    """
    Are you tired of rolling dice countless times and tallying up points one by one, all by yourself? 
    Worry not, as this option will simply add some points items to the item pool! 
    And getting one of these points items gives you... points!
    Imagine how nice it would be to find tons of them. Or even better, having others find them FOR you!
    """

    display_name = "Weight of adding Points"
    range_start = 0
    range_end = 100
    default = 20


class PointsSize(Choice):
    """
    If you choose to add points to the item pool, you can choose to have many small points,
    medium-size points, a few larger points, or a mix of them.
    """

    display_name = "Size of points"
    option_small = 1
    option_medium = 2
    option_large = 3
    option_mix = 4
    default = 2


class MinimizeExtraItems(Choice):
    """
    Besides necessary items, Yacht Dice has extra useful/filler items in the item pool.
    It is possible however to decrease the number of locations and extra items.
    This option will:
    - decrease the number of locations at the start (you'll start with 2 dice and 2 rolls).
    - will limit the number of dice/roll fragments per dice/roll to 2.
    - in multiplayer games, it will reduce the number of filler items.
    """

    display_name = "Minimize extra items"
    option_no_dont = 1
    option_yes_please = 2
    default = 1


class AddExtraPoints(Choice):
    """
    Yacht Dice typically has space for extra items.
    This option determines if bonus points are put into the item pool.
    They make the game a little bit easier, as they are not considered in the logic.

    All Of It: fill all locations with extra points
    Sure: put some bonus points in
    Never: do not put any bonus points
    """

    display_name = "Extra bonus in the pool"
    option_all_of_it = 1
    option_sure = 2
    option_never = 3
    default = 2


class AddStoryChapters(Choice):
    """
    Yacht Dice typically has space for more items.
    This option determines if extra story chapters are put into the item pool.
    Note: if you have extra points on "all_of_it", there will not be story chapters.

    All Of It: fill all locations with story chapters
    Sure: if there is space left, put in 10 story chapters.
    Never: do not put any story chapters in, I do not like reading (but I am glad you are reading THIS!)
    """

    display_name = "Extra story chapters in the pool"
    option_all_of_it = 1
    option_sure = 2
    option_never = 3
    default = 3


class WhichStory(Choice):
    """
    The most important part of Yacht Dice is the narrative.
    Of course you will need to add story chapters to the item pool.
    You can read story chapters in the feed on the website and there are several stories to choose from.
    """

    display_name = "Story"
    option_the_quest_of_the_dice_warrior = 1
    option_the_tragedy_of_fortunas_gambit = 2
    option_the_dicey_animal_dice_game = 3
    option_whispers_of_fate = 4
    option_a_yacht_dice_odyssey = 5
    option_a_rollin_rhyme_adventure = 6
    option_random_story = -1
    default = -1


class AllowManual(Choice):
    """
    If allowed, players can roll IRL dice and input them manually into the game.
    By sending "manual" in the chat, an input field appears where you can type your dice rolls.
    Of course, we cannot check anymore if the player is playing fair.
    """

    display_name = "Allow manual inputs"
    option_yes_allow = 1
    option_no_dont_allow = 2
    default = 1


@dataclass
class YachtDiceOptions(PerGameCommonOptions):
    game_difficulty: GameDifficulty
    score_for_last_check: ScoreForLastCheck
    score_for_goal: ScoreForGoal

    minimal_number_of_dice_and_rolls: MinimalNumberOfDiceAndRolls
    number_of_dice_fragments_per_dice: NumberDiceFragmentsPerDice
    number_of_roll_fragments_per_roll: NumberRollFragmentsPerRoll

    alternative_categories: AlternativeCategories

    allow_manual_input: AllowManual

    # the following options determine what extra items are shuffled into the pool:
    weight_of_dice: ChanceOfDice
    weight_of_roll: ChanceOfRoll
    weight_of_fixed_score_multiplier: ChanceOfFixedScoreMultiplier
    weight_of_step_score_multiplier: ChanceOfStepScoreMultiplier
    weight_of_double_category: ChanceOfDoubleCategory
    weight_of_points: ChanceOfPoints
    points_size: PointsSize

    minimize_extra_items: MinimizeExtraItems
    add_bonus_points: AddExtraPoints
    add_story_chapters: AddStoryChapters
    which_story: WhichStory


yd_option_groups = [
    OptionGroup(
        "Extra progression items",
        [
            ChanceOfDice,
            ChanceOfRoll,
            ChanceOfFixedScoreMultiplier,
            ChanceOfStepScoreMultiplier,
            ChanceOfDoubleCategory,
            ChanceOfPoints,
            PointsSize,
        ],
    ),
    OptionGroup(
        "Other items", 
        [
            MinimizeExtraItems, 
            AddExtraPoints, 
            AddStoryChapters, 
            WhichStory
        ],
    ),
]
