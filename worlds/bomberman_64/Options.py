from dataclasses import dataclass
from Options import Choice, Range, Toggle, PerGameCommonOptions, StartInventoryPool, DeathLink

class Goal(Choice):
    """
    Required Goal to complete the seed
    Altair - Clear the game by defeating the final boss
    Gold Cards - Clear the game by getting enough gold cards for shorter seeds
    Bosses - Clear the game by beating the 4 main world bosses
    """
    #display_name = "Goal"
    option_altair = 0
    option_goalcards = 1
    option_mainbosses = 2
    default = 0

class OpenStages(Toggle):
    """If Selected The first 3 stages of the main 4 worlds will be open from the start
    You will still require a key to access the Boss Stage"""

class HardMode(Choice):
    """Determines The Logic Used for Gold Card Checks, 
    This should be Set to the in game difficulty you want to use"""
    display_name = "Game Difficulty"
    option_normal = 0
    option_hard = 1
    default = 0

class GoldCards(Range):
    """Number of Gold Cards required to access Black Fortress
    Keep in mind 3 black keys will also be required to reach the goal
    if Final Boss is Selected
    If Gold Card Goal is Selected then this determines the number of Cards 
    Needed to hit your goal"""
    display_name = "Required Gold Cards"
    range_start = 8
    range_end = 100
    default = 45

class MaxCards(Range):
    """Max number of Gold Cards in the pool"""
    display_name = "Max Gold Cards"
    range_start = 8
    range_end = 100
    default = 50

class IncludePalace(Toggle):
    """Includes Locations for Rainbow Palace stages, 
    When this option is disabled, filler items will be placed in Rainbow Palace's locations but the stages will still unlock
    Stages are unlocked for every 25% of required gold cards."""

class RandomMusic(Toggle):
    """Shuffles the game music"""

class RandomSound(Toggle):
    """Shuffles the game sounds"""

class RandomEnemyModel(Choice):
    """If enabled will randomize enemies
    This option will require the use of the companion bomberman_64.lua script to function
    Shuffle: Suffles the enemy models consistently
    Chaotic: Randomizes enemy model every load"""
    option_off = 0
    option_shuffle = 1
    option_chaos = 2
    default = 0

class RandomEnemyAI(Choice):
    """If enabled will randomize enemies
    This option will require the use of the companion bomberman_64.lua script to function
    Shuffle: Suffles the enemy AI consistently
    Chaotic: Randomizes enemy AI every load"""
    option_off = 0
    option_shuffle = 1
    option_chaos = 2
    default = 0

class BombermanColor(Choice):
    """Changes Bomberman's model color"""
    option_white = 0
    option_black = 1
    #option_red = 2
    #option_blue = 3
    default = 0

@dataclass
class Bomb64Options(PerGameCommonOptions):
    #start_inventory_from_pool: StartInventoryPool
    open_stages: OpenStages
    gold_cards: GoldCards
    max_cards: MaxCards
    game_goal: Goal
    difficulty: HardMode
    random_music: RandomMusic
    random_sound: RandomSound
    enemy_model : RandomEnemyModel
    color: BombermanColor
    palace_on: IncludePalace
    enemy_ai: RandomEnemyAI
    death_link: DeathLink
