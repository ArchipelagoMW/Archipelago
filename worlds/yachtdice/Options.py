from Options import Choice, Range, PerGameCommonOptions
from dataclasses import dataclass

class gameDifficulty(Choice):
    """
    Difficulty. This setting determines how difficult the scores are to achieve. 
    Easy: for beginners. No luck required, just roll the dice and have fun. Lower final goal.
    Medium: intended difficulty. If you play smart, you'll finish the game without any trouble.
    Hard: you'll need to play smart and be lucky.
    Extreme: really hard mode, which requires many brain wrinkles and insane luck. NOT RECOMMENDED FOR MULTIWORLDS.
    """
    display_name = "Game difficulty"
    option_easy = 1
    option_medium = 2
    option_hard = 3
    option_extreme = 4
    default = 2
        
class scoreForLastCheck(Range):
    """
    The items in the item pool will always allow you to reach a score of 1000.
    By default, the last check is also at a score of 1000. 
    However, you can set the score for the last check to be lower. This will make the game shorter and easier.
    """
    display_name = "Score for last check"
    range_start = 500
    range_end = 1000
    default = 1000
    
class scoreForGoal(Range):
    """
    This setting determines what score you need to reach to finish the game.
    It cannot be higher than the score for the last check (if it is, it is changed automatically).
    """
    display_name = "Score for goal"
    range_start = 500
    range_end = 1000
    default = 777

class minimalNumberOfDiceAndRolls(Choice):
    """
    The minimal number of dice and rolls in the pool.
    These are guaranteed, unlike the later items.
    You can never get more than 8 dice and 5 rolls.
    You start with one dice and one roll.
    """
    display_name = "Minimal number of dice and rolls in pool"
    option_2_dice_and_2_rolls = 1
    option_5_dice_and_3_rolls = 2
    option_5_dice_and_5_rolls = 3
    option_6_dice_and_4_rolls = 4
    option_7_dice_and_3_rolls = 5
    option_8_dice_and_2_rolls = 6
    default = 2

class numberDiceFragmentsPerDice(Range):
    """
    Dice can be split into fragments, gathering enough will give you an extra dice. 
    You start with one dice, and there will always be one full dice in the pool. 
    The other dice are split into fragments, according to this setting. 
    Setting this to 1 fragment per dice just puts 'Dice' objects in the pool.
    """
    display_name = "Number of dice fragments per dice"
    range_start = 1
    range_end = 5
    default = 4
    
class numberRollFragmentsPerRoll(Range):
    """
    Rolls can be split into fragments, gathering enough will give you an extra roll. 
    You start with one roll, and there will always be one full roll in the pool. 
    The other three rolls are split into fragments, according to this setting.
    Setting this to 1 fragment per roll just puts 'Roll' objects in the pool.
    """
    display_name = "Number of roll fragments per roll"
    range_start = 1
    range_end = 5
    default = 4
    
"""
Test 1 2 3
"""
    
class alternativeCategories(Range):
    """
    There are 16 default categories, but there are also 16 alternative categories.
    These alternative categories can be randomly selected to replace the default categories.
    They are a little strange, but can give a fun new experience.
    In the game, you can hover over categories to check what they do.
    How many alternative categories would you like to see in your game?
    """
    display_name = "Number of alternative categories"
    range_start = 0
    range_end = 16
    default = 0    
    
    
class chanceOfDice(Range):
    """
    The item pool is always filled in such a way that you can reach a score of 1000.
    Extra progressive items are added that will help you on your quest.
    You can set the weight for each extra progressive item in the following options.
    
    Of course, more dice = more points!
    """
    display_name = "Weight of adding Dice"
    range_start = 0
    range_end = 100
    default = 5 
    
class chanceOfRoll(Range):
    """
    With more rolls, you'll be able to reach higher scores.
    """
    display_name = "Weight of adding Roll"
    range_start = 0
    range_end = 100
    default = 20     

class chanceOfFixedScoreMultiplier(Range):
    """
    Getting a Fixed Score Multiplier will boost all future scores by 10%.
    """
    display_name = "Weight of adding Fixed Score Multiplier"
    range_start = 0
    range_end = 100
    default = 30 
    
class chanceOfStepScoreMultiplier(Range):
    """
    The Step Score Multiplier boosts your multiplier after every roll by 1%, and resets on sheet reset.
    So, keep high scoring categories for later to get the most of them.
    By default, this item is not included. It is fun however, you just need to know the above strategy.
    """
    display_name = "Weight of adding Step Score Multiplier"
    range_start = 0
    range_end = 100
    default = 0 
    
class chanceOfDoubleCategory(Range):
    """
    This option allows categories to appear multiple times.
    Each time you get a category after the first, its score value gets doubled.
    """
    display_name = "Weight of adding Category copy"
    range_start = 0
    range_end = 100
    default = 50
    
class chanceOfPoints(Range):
    """
    Getting points gives you... points. You can get 1 point, 10 points, and even 100 points.
    """
    display_name = "Weight of adding Points"
    range_start = 0
    range_end = 100
    default = 20    
    
class pointsSize(Choice):
    """
    If you choose to add points to the item pool, do you prefer many small points, 
    medium size, a few larger points, or a mix of them?
    """
    display_name = "Size of points"
    option_small = 1
    option_medium = 2
    option_large = 3
    option_mix = 4
    default = 2
    
class minimizeExtraItems(Choice):
    """
    Besides necessary items, Yacht Dice has extra items in the item pool.
    It is possible however to decrease the number of extra items
    by putting categories Fives, Sixes and Pair early into the playthrough. Would you like to do this?
    """
    display_name = "Minimize extra items"
    option_no_dont = 1
    option_yes_please = 2
    default = 1    
    
class addExtraPoints(Choice):
    """
    Yacht Dice typically has space for extra items.
    If there is space, would you like bonus points shuffled in the item pool?
    They make the game a little bit easier, as they are not considered in the logic.
    
    all_of_it: fill all locations with extra points
    sure: put some bonus points in
    never: don't put any bonus points
    """
    display_name = "Extra bonus in the pool"
    option_all_of_it = 1
    option_sure = 2
    option_never = 3
    default = 2
      
class addStoryChapters(Choice):
    """
    Yacht Dice typically has space for more items.
    If there is space, would you like story chapters shuffled in the item pool?
    Note: if you have extra points on "all_of_it", there won't be story chapters.
    
    all_of_it: fill all locations with story chapters
    sure: if there is space left, put in 10 story chapters.
    never: don't put any story chapters, I don't like reading (but I'm glad you're reading THIS!)
    """
    display_name = "Extra story chapters in the pool"
    option_all_of_it = 1
    option_sure = 2
    option_never = 3
    default = 3
    
class whichStory(Choice):
    """
    The most important part of Yacht Dice is the narrative.
    If you choose to 
    10 story chapters are shuffled into the item pool. 
    You can read them in the feed on the website.
    Which story would you like to read?
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
    
@dataclass
class YachtDiceOptions(PerGameCommonOptions):
    game_difficulty: gameDifficulty
    score_for_last_check: scoreForLastCheck
    score_for_goal: scoreForGoal
    
    minimal_number_of_dice_and_rolls: minimalNumberOfDiceAndRolls
    number_of_dice_fragments_per_dice: numberDiceFragmentsPerDice
    number_of_roll_fragments_per_roll: numberRollFragmentsPerRoll
    
    alternative_categories: alternativeCategories
    
    #the following options determine what extra items are shuffled into the pool:
    weight_of_dice: chanceOfDice
    weight_of_roll: chanceOfRoll
    weight_of_fixed_score_multiplier: chanceOfFixedScoreMultiplier
    weight_of_step_score_multiplier: chanceOfStepScoreMultiplier
    weight_of_double_category: chanceOfDoubleCategory
    weight_of_points: chanceOfPoints
    points_size: pointsSize
    
    minimize_extra_items: minimizeExtraItems
    add_bonus_points: addExtraPoints
    add_story_chapters: addStoryChapters
    which_story: whichStory