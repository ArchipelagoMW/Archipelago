from dataclasses import dataclass
from Options import Toggle, DefaultOnToggle, Range, NamedRange, Choice, OptionSet, DeathLink, PerGameCommonOptions, OptionGroup
from .Items import item_data_table

class Goal(Choice):
    """
    What must you accomplish to win the game?
    Survival: Survive a number of days to win. Chose the amount in "Days to Survive" option.
    Bosses (Any): Defeat any boss selected in "Boss Defeat Requirement" to win.
    Bosses (All): Defeat all bosses selected in "Boss Defeat Requirement" to win.
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
    Being a ghost pauses your timer. Regenerating the world or dying in Wilderness mode resets your timer.
    """
    display_name = "Days to Survive"
    default = 70
    range_start = 0
    range_end = 1000

    special_range_names = {
        "through autumn": 20,
        "through winter": 35,
        "one year": 70,
        "two years": 140,
    }

class RequiredBosses(OptionSet):
    """
    Only applies for boss goal types. Which boss(es) are required to be defeated to beat the game?

    Valid Bosses:             Difficulty                Regions
        "Deerclops"           - Easy / Seasonal
        "Moose/Goose"         - Easy / Seasonal
        "Bearger"             - Easy / Seasonal
        "Ancient Guardian"    - Medium                  Cave, Ruins
        "Antlion"             - Easy / Seasonal
        "Dragonfly"           - Medium
        "Bee Queen"           - Hard
        "Klaus"               - Medium / Seasonal
        "Toadstool"           - Hard                    Cave
        "Malbatross"          - Medium                  Ocean
        "Crab King"           - Hard                    Ocean
        "Frostjaw"            - Medium                  Ocean
        "Eye Of Terror"       - Easy
        "Retinazor"           - Hard
        "Spazmatism"          - Hard
        "Nightmare Werepig"   - Medium                  Cave
        "Scrappy Werepig"     - Medium                  Cave
        "Ancient Fuelweaver"  - Hard                    Cave, Ruins
        "Celestial Champion"  - Hard                    Ocean, Moonstorm

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

class CaveRegions(Choice):
    """
    How far into the cave will your items and locations be shuffled?

    None: No cave. Choose this if you're making a no-cave world!
    Auto: Choose minimum regions based on your goal. (Survival goal will default to None. For boss goals, check the tooltip for "Boss Defeat Requirement")
    Light: Shuffle caves without ruins and archive
    Full: Shuffle caves, ruins, and archive
    """
    display_name = "Cave Regions"
    default = 1
    option_none = 0
    option_auto = 1
    option_light = 2
    option_full = 3
    
class OceanRegions(Choice):
    """
    How far into the ocean will your items and locations be shuffled?

    None: No ocean checks
    Auto: Choose minimum regions based on your goal. (Survival goal will default to None. For boss goals, check the tooltip for "Boss Defeat Requirement")
    Light: Shuffle ocean without moonstorm
    Full: Shuffle ocean and moonstorm
    """
    display_name = "Ocean Regions"
    default = 1
    option_none = 0
    option_auto = 1
    option_light = 2
    option_full = 3

class CreatureLocations(DefaultOnToggle):
    """
    Are non-boss creatures item locations, by killing or non-violent interactions?
    (Disabling will remove a lot of locations. Excess items will be moved into your start inventory.)
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
    There's a good chance you'll need the wiki to get all of these: https://dontstarve.fandom.com/wiki/Crock_Pot

    None: No items from cooking. (This will remove a lot of locations. Excess items will be moved into your start inventory.)
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

class ChessPieceSketchItems(DefaultOnToggle):
    """
    Include Knight, Bishop, and Rook Figure Sketches as items?
    This bypasses the need to assemble the marble sculptures for Shadow Pieces, while preventing specific progression-locking scenarios.
    """
    display_name = "Chess Piece Sketch Items"

class ExtraDamageAgainstBosses(NamedRange):
    """
    This adds "Extra Damage Against Bosses" buffs as Archipelago items. Recommended if playing solo.
    Each stack of this buff gives the player a permanent +10% damage against easier bosses and +25% damage against tougher ones.
    This is exponential. With 10 stacks, this turns into x2.6 and x9.3 damage multipiers respectively.
    """
    display_name = "Extra Damage Against Bosses"
    range_start = 0
    range_end = 20
    default = 6

    special_range_names = {
        "none": 0,
        "low": 3,
        "medium": 6,
        "high": 10,
    }

class ShuffleStartingRecipes(Toggle):
    """
    Turn your basic starting recipes into Archipelago items?

    This may leave you vulnerable to darkness on your first night!
    If you're not okay with this, you may want to add Torch to your starting items.

    Sphere 1 will also be small, making generation more restrictive when generating alone, and is prone to fail if "Creature Locations" are off!
    """
    display_name = "Shuffle Starting Recipes"

class ShuffleNoUnlockRecipes(Toggle):
    """
    Turn crafting recipes in the Ancient Pseudoscience Station and Celestial Altars into Archipelago items?
    """
    display_name = "Shuffle Ancient and Celestial Recipes"

class SeedItems(Toggle):
    """
    Turn farm plant seeds into Archipelago items?
    When enabled, generic seeds can only grow weeds.
    """
    display_name = "Farm Plant Seed Items"

# class CraftWithLockedItems(DefaultOnToggle):
#     """
#     Should you be able to craft if any of the ingredients are one of your missing items?
#     """
#     display_name = "Craft With Locked Items"

class PlayerSkillLevel(Choice):
    """
    What skill level should be considered for randomizer logic?

    Easy: Ensure items that would be helpful for progression are accessible
    Advanced: Expects you to know the game well. Season gear logic defaults to none.
    Expert: Expects you to survive in riskier conditions, have minimal items, and know advanced tricks. All helpful logic defaults to none.

    Easier difficulties may make generation more restrictive.
    """
    display_name = "Logic Difficulty"
    default = 0
    option_easy = 0
    option_advanced = 1
    option_expert = 2

class LightingLogic(Choice):
    """
    Make portable light sources progression and include in logic?
    """
    display_name = "Lighting Logic"
    default = 1
    option_none = 0
    option_auto = 1
    option_enabled = 2

class WeaponLogic(Choice):
    """
    Make weapons and armor progression and include in logic?
    """
    display_name = "Weapon Logic"
    default = 1
    option_none = 0
    option_auto = 1
    option_enabled = 2

class SeasonGearLogic(Choice):
    """
    Make protective seasonal gear progression and include in logic?
    """
    display_name = "Season Gear Logic"
    default = 1
    option_none = 0
    option_auto = 1
    option_enabled = 2

class BaseMakingLogic(Choice):
    """
    Make quality-of-life structures such as Chest, Ice Box, and flooring progression and include in logic?
    """
    display_name = "Base Making Logic"
    default = 1
    option_none = 0
    option_auto = 1
    option_enabled = 2

class BackpackLogic(Choice):
    """
    Make backpacks progression and include in logic?
    """
    display_name = "Backpack Logic"
    default = 1
    option_none = 0
    option_auto = 1
    option_enabled = 2

class HealingLogic(Choice):
    """
    Make healing items progression and include in logic?
    """
    display_name = "Healing Logic"
    default = 1
    option_none = 0
    option_auto = 1
    option_enabled = 2

class JunkItemAmount(Range):
    """
    Number of junk (stat change) and trap items to add to the item pool
    """
    display_name = "Junk Item Amount"
    default = 20
    range_start = 0
    range_end = 100

class TrapItems(NamedRange):
    """
    Chance percentage junk items can be regular traps. These do not change the season. If combined with Season Traps Items, the percentage is split.
    """
    display_name = "Trap Item Chance (Percentage)"
    default = 20
    range_start = 0
    range_end = 100
    
    special_range_names = {
        "none": 0,
        "low": 20,
        "medium": 50,
        "high": 80,
        "always": 100,
    }

class SeasonTrapItems(NamedRange):
    """
    Chance percentage junk items can be season-changing traps. If combined with Traps Items, the percentage is split.
    """
    display_name = "Season Trap Item Chance (Percentage)"
    default = 0
    range_start = 0
    range_end = 100

    special_range_names = {
        "none": 0,
        "low": 20,
        "medium": 50,
        "high": 80,
        "always": 100,
    }

class NonshuffledItems(OptionSet):
    """
    Items that will not be shuffled. 
    This differs from adding these as starting items since these will only be available at their respective prototype station, etc.
    """
    display_name = "Nonshuffled Items"
    valid_keys = {name for name, item in item_data_table.items() if not len(item.tags.intersection({
        "nonshuffled",
        "progressive",
        "deprecated"
    }))}

dontstarvetogether_option_groups = [
    OptionGroup("Logic Options", [
        PlayerSkillLevel,
        LightingLogic,
        WeaponLogic,
        SeasonGearLogic,
        BaseMakingLogic,
        BackpackLogic,
        HealingLogic,
    ]),
    OptionGroup("Item & Location Options", [
        NonshuffledItems,
    ]),
]

@dataclass
class DSTOptions(PerGameCommonOptions):
    goal: Goal
    days_to_survive: DaysToSurvive
    required_bosses: RequiredBosses
    cave_regions: CaveRegions
    ocean_regions: OceanRegions
    creature_locations: CreatureLocations
    boss_locations: BossLocations
    cooking_locations: CookingLocations
    farming_locations: FarmingLocations
    seasonal_locations: SeasonalLocations
    season_change_helper_items: SeasonChangeHelperItems
    chesspiece_sketch_items: ChessPieceSketchItems
    extra_damage_against_bosses: ExtraDamageAgainstBosses
    shuffle_starting_recipes: ShuffleStartingRecipes
    shuffle_no_unlock_recipes: ShuffleNoUnlockRecipes
    seed_items: SeedItems
    # craft_with_locked_items: CraftWithLockedItems
    skill_level: PlayerSkillLevel
    lighting_logic: LightingLogic
    weapon_logic: WeaponLogic
    season_gear_logic: SeasonGearLogic
    base_making_logic: BaseMakingLogic
    backpack_logic: BackpackLogic
    healing_logic: HealingLogic
    junk_item_amount: JunkItemAmount
    trap_items: TrapItems
    season_trap_items: SeasonTrapItems
    nonshuffled_items: NonshuffledItems
    death_link: DeathLink