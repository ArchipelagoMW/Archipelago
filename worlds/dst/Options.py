from dataclasses import dataclass
from Options import Toggle, DefaultOnToggle, Range, NamedRange, Choice, OptionSet, DeathLink, PerGameCommonOptions

class Goal(Choice):
    """
    What must you accomplish to win the game?
    Survival: Survive a number of days to win.
    Bosses (Any): Defeat any of the selected bosses to win.
    Bosses (All): Defeat all selected bosses to win.
    """
    display_name = "Goal Type"
    default = 1
    option_survival = 0
    option_bosses_any = 1
    option_bosses_all = 2
   
class DaysToSurvive(NamedRange):
    """
    Only applies for the survival goal. The number of days your character must survive for the survival goal. 
    Each day would last 8 real life minutes on default settings.
    """
    display_name = "Days to Survive"
    default = 70
    range_start = 0
    range_end = 200

    special_range_names = {
        "through autumn": 20,
        "through winter": 35,
        "one year": 70,
        "two years": 140,
    }

class RequiredBosses(OptionSet):
    """
    Which boss(es) are required to be defeated to beat the game?
    """
    display_name = "Boss Defeat Requirement"
    default = {"Ancient Guardian"}
    valid_keys = {
        "Deerclops",
        "Moose/Goose",
        "Bearger",
        "Ancient Guardian",
        "Antlion",
        "Dragonfly",
        "Bee Queen",
        "Klaus",
        "Toadstool",
        "Crab King",
        "Frostjaw",
        "Eye Of Terror",
        "Retinazor",
        "Spazmatism",
        "Nightmare Werepig",
        "Scrappy Werepig",
        "Ancient Fuelweaver",
        "Celestial Champion",
    }
    
class CreatureLocations(DefaultOnToggle):
    """
    Are non-boss creatures item locations? 
    (Disabling will remove a lot of locations and potentially leave unplaced items!)
    """
    display_name = "Creature Kill Locations"

    
class BossLocations(Choice):
    """
    Decide what type of items bosses may have.

    None: Bosses only drop filler items.
    Easy: Easier bosses may have useful items. Raid bosses will only have filler items except when required by your goal.
    All: All bosses may have useful items.
    Prioritized: All bosses are more likely to have progression items.
    """
    display_name = "Boss Kill Locations"
    default = 1
    option_none = 0
    option_easy = 1
    option_all = 2
    option_prioritized = 3

class CookingLocations(Choice):
    """
    Find items when cooking different foods in the crock pot?

    None: No items from cooking. (This will remove a lot of locations and potentially leave unplaced items!)
    Regular: There are locations for cooking in the crock pot, excluding Warly's exclusives.
    Include Warly Exclusives: All crock pot recipes are locations. Logic will expect you to have the ability to use the Portable Crock Pot.
    """
    display_name = "Cooking Locations"
    default = 1
    option_none = 0
    option_regular = 1
    option_warly_enabled = 2

class FarmingLocations(Choice):
    """
    Find items when you harvest giant crops?
    """
    display_name = "Farming Locations"
    default = 0
    option_none = 0
    option_enabled = 1

class SeasonalLocations(Toggle):
    """
    Should season-specific locations have important items?

    False: Season-specific locations will only have filler items.
    True: Season-specific locations may have useful items.
    """
    display_name = "Seasonal Locations"

class PlayerSkillLevel(Choice):
    """
    What skill level should be considered for randomizer logic?

    Easy: You're still learning to not starve.
    Advanced: You're good at not dying most of the time.
    Expert: You're too good at this game.
    """
    display_name = "Player Skill Level"
    default = 0
    option_easy = 0
    option_advanced = 1
    option_expert = 2

class TrapItems(Choice):
    """
    Include regular traps in the item pool? These do not change the season.
    """
    display_name = "Trap Items"
    default = 1
    option_none = 0
    option_low = 1
    option_medium = 2
    option_high = 3

class SeasonTrapItems(Choice):
    """
    Include season-changing traps in the item pool?
    """
    display_name = "Season Trap Items"
    default = 0
    option_none = 0
    option_low = 1
    option_medium = 2
    option_high = 3

    
@dataclass
class DSTOptions(PerGameCommonOptions):
    goal: Goal
    days_to_survive: DaysToSurvive
    required_bosses: RequiredBosses
    creature_locations: CreatureLocations
    boss_locations: BossLocations
    cooking_locations: CookingLocations
    farming_locations: FarmingLocations
    seasonal_locations: SeasonalLocations
    skill_level: PlayerSkillLevel
    trap_items: TrapItems
    season_trap_items: SeasonTrapItems
    death_link: DeathLink