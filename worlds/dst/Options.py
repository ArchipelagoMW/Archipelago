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
    
    Valid Bosses:
        "Deerclops"
        "Moose/Goose"
        "Bearger"
        "Ancient Guardian"
        "Antlion"
        "Dragonfly"
        "Bee Queen"
        "Klaus"
        "Toadstool"
        "Malbatross"
        "Crab King"
        "Frostjaw"
        "Eye Of Terror"
        "Retinazor"
        "Spazmatism"
        "Nightmare Werepig"
        "Scrappy Werepig"
        "Ancient Fuelweaver"
        "Celestial Champion"

    Example: ['Deerclops', 'Moose/Goose', 'Bearger']
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
        "Malbatross",
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
    Are non-boss creatures item locations, by killing or non-violent interactions? 
    (Disabling will remove a lot of locations and potentially leave unplaced items!)
    """
    display_name = "Creature Locations"

    
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
    Regular: Get items for cooking in the crock pot, excluding Warly's exclusives.
    Include Warly Exclusives: All crock pot recipes are item locations. Logic will expect you to have the ability to use the Portable Crock Pot.
    Veggie Only: All recipes except meat and Warly exclusives.
    Meat Only: All recipes except veggie and Warly exclusives.
    """
    display_name = "Cooking Locations"
    default = 1
    option_none = 0
    option_regular = 1
    option_warly_enabled = 2
    option_veggie_only = 3
    option_meat_only = 4

class FarmingLocations(Toggle):
    """
    Find items when you harvest giant crops?
    """
    display_name = "Farming Locations"

class SeasonalLocations(Toggle):
    """
    Should season-specific locations have important items?

    False: Season-specific locations will only have filler items.
    True: Season-specific locations may have useful items.
    """
    display_name = "Seasonal Locations"
    
class SeasonChangeHelperItems(Toggle):
    """
    Include a way to change seasons and moon phases to help with location checks?
    These will be added as Archipelago items, and cost sanity and purple gems to use.
    """
    display_name = "Season Change Helper Items"

class ExtraDamageAgainstBosses(NamedRange):
    """
    This adds "Extra Damage Against Bosses" buffs as Archipelago items.
    Each stack of this buff gives the player a permanent +10% damage against easier bosses and +25% damage against tougher ones.
    """
    display_name = "Extra Damage Against Bosses"
    range_start = 0
    range_end = 10
    default = 0

    special_range_names = {
        "none": 0,
        "low": 3,
        "medium": 6,
        "high": 10,
    }
  
class ShuffleStartingRecipes(Toggle):
    """
    Turn your basic starting recipes into Archipelago items?
    """
    display_name = "Shuffle Starting Recipes"

class ShuffleNoUnlockRecipes(Toggle):
    """
    Turn crafting recipes in the Ancient Pseudoscience Station and Celestial Altars into Archipelago items?
    """
    display_name = "Shuffle Ancient and Celestial Recipes"

# class CraftWithLockedItems(DefaultOnToggle):
#     """
#     Should you be able to craft if any of the ingredients are one of your missing items?
#     """
#     display_name = "Craft With Locked Items"

class PlayerSkillLevel(Choice):
    """
    What skill level should be considered for randomizer logic?

    Easy: Ensure items that would be helpful for progression are accessible
    Advanced: Expects you to know the game well and to survive seasons under-equipped
    Expert: Expects you to survive in riskier conditions, such as entering the ruins without light, etc
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
    season_change_helper_items: SeasonChangeHelperItems
    extra_damage_against_bosses: ExtraDamageAgainstBosses
    shuffle_starting_recipes: ShuffleStartingRecipes
    shuffle_no_unlock_recipes: ShuffleNoUnlockRecipes
    # craft_with_locked_items: CraftWithLockedItems
    skill_level: PlayerSkillLevel
    trap_items: TrapItems
    season_trap_items: SeasonTrapItems
    death_link: DeathLink