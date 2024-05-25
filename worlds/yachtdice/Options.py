from Options import Choice, Range, PerGameCommonOptions
from dataclasses import dataclass

class numberOfDiceAndRolls(Choice):
    """
    Total number of dice and rolls in the pool.
    You start with one dice and one roll.
    This option does not change the final goal.
    """
    display_name = "Number of dice and rolls in pool"
    option_5_dice_and_5_rolls = 5
    option_6_dice_and_4_rolls = 6
    option_7_dice_and_3_rolls = 7
    option_8_dice_and_2_rolls = 8
    default = 5

# class numberOfExtraRolls(Range):
#     """Total number of extra rolls you can add to your collection.
#     Wait this is always 4? Yes, I removed other options, but they might return."""
#     display_name = "Number of extra rolls"
#     range_start = 4
#     range_end = 4
#     default = 4

class numberDiceFragmentsPerDice(Range):
    """
    Dice can be split into fragments, gathering enough will give you an extra dice. 
    You start with one dice, and there will always be one full dice in the pool. 
    The other dice are split into fragments, according to this setting. 
    Setting this to 1 fragment per dice, just puts 'Dice' objects in the pool.
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
    Setting this to 1 fragment per roll, just puts 'Roll' objects in the pool.
    """
    display_name = "Number of roll fragments per roll"
    range_start = 1
    range_end = 5
    default = 4
    

class numberExtraDiceFragments(Range):
    """
    Number of extra dice fragments in the pool. 
    The number cannot exceed the number of dice fragments per dice,
    if it does, the generation will lower this setting automatically.
    The option will never give an extra full dice, but makes it easier to collect all dice.
    """
    display_name = "Number of extra dice fragments in the pool"
    range_start = 0
    range_end = 4
    default = 3
    
    

class numberExtraRollFragments(Range):
    """
    Number of extra roll fragments in the pool. 
    The number cannot exceed the number of roll fragments per roll
    if it does, the generation will lower this setting automatically.
    The option will never give an extra full roll, but makes it easier to collect all roll.
    """
    display_name = "Number of extra roll fragments in the pool"
    range_start = 0
    range_end = 4
    default = 3


class gameDifficulty(Choice):
    """
    Difficulty. This setting determines how difficult the scores are to achieve. 
    Easy: for beginners. No luck required, just roll the dice and have fun. Lower final goal.
    Medium: intended difficulty. If you play smart, you'll finish the game without any trouble.
    Hard: you may need to play smart, be lucky and understand the score multiplier mechanic. Higher final goal.
    Extreme: more strict logic, higher final goal. ONLY FOR EXPERIENCES PLAYERS IN MULTIWORLDS.
    """
    display_name = "Game difficulty"
    option_easy = 1
    option_medium = 2
    option_hard = 3
    option_extreme = 4
    #option_nightmare = 5
    
    default = 2
    
    
class goalLocationPercentage(Range):
    """
    What percentage of checks you need to get, to 'finish' the game.
    Low percentage means you can probably 'finish' the game with some of the dice/rolls/categories.
    High percentage means you need most of the useful items, and on higher difficulties you might need them all.
    """
    display_name = "Goal percentage location"
    range_start = 70
    range_end = 100
    default = 90
    
class alternativeCategories(Range):
    """
    There are 16 default categories, but there are also 16 alternative categories.
    These alternative categories can replace the default categories.
    How many alternative categories would you like to see in your game?
    """
    display_name = "Number of alternative categories"
    range_start = 0
    range_end = 16
    default = 0
      
    
    
class scoreMultiplierType(Choice):
    """
    There are 10 Score Multiplier items available.
    This options decides how the Score Multipliers work.
    Both options are of similar difficulty.
    
    fixed_multiplier: every multiplier item gives you +10%. 
    Every score gets multiplied with the multiplier.
    So with all score multipliers, all scores get +100%.
    
    step_multiplier: every multiplier item gives you +1%. 
    Your multiplier increases with this percentage after every turn. 
    So in the first turn you have no multiplier, but in turn 16, you can have a +150% multiplier. 
    So, save your high-scoring categories for last. This option allow for more strategic games. 
    """
    display_name = "Score multiplier type"
    option_fixed_multiplier = 1
    option_step_multiplier = 2
    default = 1 
    
class gameMode(Choice):
    """
    Yacht Dice has three main game modes:
    
    Standard. Get to 500 points on medium difficulty (and a bit lower/higher on other difficulties).
    
    Points mode: a bunch of "10 Points" items are shuffled through the item pool. Get to 1000 points.
    The amount of "10 Points" items in the pool depends on your selected difficulty.
    
    I'll add a new category soon™
    """
    # Extra categories: categories may appear multiple times. 
    # Getting a category again gives a x2 multiplier for that category. Get to 1000 points.
    # The amount of "10 Points" items in the pool depends on your selected difficulty.
    
    display_name = "Game mode"
    option_standard = 1
    option_points_mode = 2
    option_extra_categories = 3
    default = 1
    
class pointsGameMode(Choice):
    """
    If points mode is selected, this option determines the value of the points items.
    
    yes_1_per_item: hundreds of "1 Point" items are shuffled into the pool.
    NOT recommended in multiplayer, unless everyone is aware of the hundred of points items
    
    yes_10_per_item: puts tens of "10 Points" (and a few 1 Points) into the item pool.
    
    yes_100_per_item: puts a few "100 Points" (and a few 1 and 10 Points) into the item pool. 
    Warning: will unlock many checks if an 100 Points item is collected.
    """
    display_name = "Value of points item"
    option_1_per_item = 2
    option_10_per_item = 3
    option_100_per_item = 4
    default = 3

    
class minimizeExtraItems(Choice):
    """
    Would you like to minimize the number of extra items in the pool?
    Note that if you put this on, categories Fives, Sixes and Pair are put early into the playthrough.
    """
    display_name = "Minimize extra items"
    option_no_dont = 1
    option_yes_please = 2
    default = 1    
    
class addExtraPoints(Choice):
    """
    Yacht Dice typically has space for more items.
    Would you like extra points shuffled in the item pool?
    They make the game a little bit easier, as they are not considered in the logic.
    all_of_it: put as many extra points in locations as possible
    sure: put some extra points in
    never: don't but any extra points
    """
    display_name = "Extra points in the pool"
    option_all_of_it = 1
    option_sure = 2
    option_never = 3
    default = 2
      
class addStoryChapters(Choice):
    """
    Yacht Dice typically has space for more items.
    Would you like story chapters shuffled in the item pool?
    Note: if you have extra points on "all_of_it" there won't be story chapters.
    """
    display_name = "Extra story chapters in the pool"
    option_all_of_it = 1
    option_sure = 2
    option_never = 3
    default = 2
    
class whichStory(Choice):
    """
    The most important part of Yacht Dice is the narrative. 
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
    number_of_dice_and_rolls: numberOfDiceAndRolls
    number_of_dice_fragments_per_dice: numberDiceFragmentsPerDice
    number_of_extra_dice_fragments: numberExtraDiceFragments
    number_of_roll_fragments_per_roll: numberRollFragmentsPerRoll
    number_of_extra_roll_fragments: numberExtraRollFragments
    game_difficulty: gameDifficulty
    goal_location_percentage: goalLocationPercentage
    alternative_categories: alternativeCategories
    score_multiplier_type: scoreMultiplierType
    game_mode: gameMode
    points_game_mode: pointsGameMode
    minimize_extra_items: minimizeExtraItems
    add_extra_points: addExtraPoints
    add_story_chapters: addStoryChapters
    which_story: whichStory