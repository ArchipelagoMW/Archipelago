from dataclasses import dataclass
from Options import Toggle, DefaultOnToggle, Range, NamedRange, Choice, OptionSet, DeathLink, PerGameCommonOptions, OptionGroup
from .Constants import PHASE, SEASON

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
    If "Random" is chosen and nothing else, a random valid boss is selected.
    If "Random" is chosen with bosses, it chooses a single boss within the selection.

    Valid Bosses:             Difficulty        Regions
        "Random"
        "Deerclops"           - Easy            Winter
        "Moose/Goose"         - Easy            Spring
        "Bearger"             - Easy            Autumn
        "Ancient Guardian"    - Medium          Cave, Ruins
        "Antlion"             - Easy            Summer
        "Dragonfly"           - Medium
        "Bee Queen"           - Hard
        "Klaus"               - Medium          Winter
        "Toadstool"           - Hard            Cave
        "Malbatross"          - Medium          Ocean
        "Crab King"           - Hard            Ocean
        "Frostjaw"            - Medium          Ocean
        "Eye Of Terror"       - Easy            Night
        "Retinazor"           - Hard            Night
        "Spazmatism"          - Hard            Night
        "Nightmare Werepig"   - Medium          Cave
        "Scrappy Werepig"     - Medium          Cave
        "Ancient Fuelweaver"  - Hard            Cave, Ruins, Night
        "Celestial Champion"  - Hard            Ocean, Moonstorm

    Example: ['Deerclops', 'Moose/Goose', 'Bearger']
    """
    display_name = "Boss Defeat Requirement"
    default = {"Ancient Guardian"}
    valid_keys = {
        "Random",
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

# class CraftWithLockedItems(DefaultOnToggle):
#     """
#     Should you be able to craft if any of the ingredients are one of your missing items?
#     """
#     display_name = "Craft With Locked Items"

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

class Seasons(OptionSet):
    """
    Which seasons will be enabled in your world?
    (This is not automatic. If changed from default, seasons will need to be set manually in your world settings!)
    """
    display_name = "Seasons"
    default =    {SEASON.AUTUMN, SEASON.WINTER, SEASON.SPRING, SEASON.SUMMER}
    valid_keys = {SEASON.AUTUMN, SEASON.WINTER, SEASON.SPRING, SEASON.SUMMER}
    
class StartingSeason(Choice):
    """
    Which season do you start with in your world?
    (This is not automatic. If not autumn, starting season will need to be set manually in your world settings!)
    """
    display_name = "Starting Season"
    default = 0
    option_autumn = 0
    option_winter = 1
    option_spring = 2
    option_summer = 3
    
class DayPhases(OptionSet):
    """
    Which day phases will be enabled in your world?
    (This is not automatic. If changed from default, day phases will need to be set manually in your world settings!)
    Set to Night only if you plan to play on a Lights Out world.
    """
    display_name = "Day Phases"
    default =    {PHASE.DAY, PHASE.DUSK, PHASE.NIGHT}
    valid_keys = {PHASE.DAY, PHASE.DUSK, PHASE.NIGHT}

class CreatureLocations(Choice):
    """
    Are non-boss creatures item locations, by killing or non-violent interactions?
    None: Creatures are not checks. (Disabling will remove a lot of locations. Excess items will be moved into your start inventory.)
    All: All creatures are checks.
    Peaceful: Only creatures that have a peaceful interaction are checks. Killing still also grants the check.
    """
    display_name = "Creature Locations"
    default = 1
    option_none = 0
    option_all = 1
    option_peaceful = 2

class BossLocations(Choice):
    """
    Are boss defeats item locations, other than ones listed in your goal condition?

    None: No boss checks other than ones on your goal path.
    Easy: Only easier bosses. These can be defeated even if playing solo with default difficulty. 
    All: Includes raid bosses. These are intended for multiplayer sessions, but can still be soloed with Extra Damage Against Bosses or creative strategies.
    Prioritized: All bosses will have either useful or progression items.
    """
    display_name = "Boss Locations"
    default = 1
    option_none = 0
    option_easy = 1
    option_all = 2
    option_prioritized = 3

class CookingLocations(Choice):
    """
    Find items when cooking different foods in the crock pot?
    There's a good chance you'll need the wiki to get all of these: https://dontstarve.wiki.gg/wiki/Dishes

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

# class ExtraDamageAgainstBossesWhenDefeatingBosses(Toggle):
#     """
#     This adds "Extra Damage Against Bosses" as rewards for defeating bosses. Recommended if playing solo.
#     This requires Boss Locations to be enabled. Does not apply to bosses that count for your victory condition.
#     Can also be functionally used to make boss items local-only and not required in logic.
#     """
#     display_name = "Extra Damage Against Bosses When Defeating Bosses"

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
    Turn crafting recipes from the Ancient Pseudoscience Station and Celestial Altars into Archipelago items?
    """
    display_name = "Shuffle Ancient and Celestial Recipes"

class SeedItems(Toggle):
    """
    Turn farm plant seeds into Archipelago items?
    When enabled, generic seeds can only grow weeds.
    """
    display_name = "Farm Plant Seed Items"

class SeasonFlow(Choice):
    """
    How do seasons progress in your world?
    
    Normal: Seasons progress as default. Logic attempts to prepare you for seasons, but not guaranteed. Seasonal checks may not have progression items.
    Unlockable: Season-changing items are progression. Seasonal checks may have progresion items. Can optionally play with long seasons.
    Unlockable Shuffled: Same as unlockable, except seasons are logically shuffled within the spheres. Can optionally play with long seasons.
    """
    display_name = "Season Flow"
    default = 2
    option_normal = 0
    option_unlockable = 2
    option_unlockable_shuffled = 3

class PlayerSkillLevel(Choice):
    """
    What skill level should be considered for randomizer logic?

    Easy: Adds useful items in logic and avoids harder solutions.
    Advanced: Expects the player to be familiar with game mechanics.
    Expert: Expects the player survive in riskier conditions, have minimal items, and know advanced tricks.

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
    
    If set too high, junk will leave no space for regular items, and overflow them into your starting inventory.
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
    Chance percentage junk items can be season-changing traps. These can only be seasons that are enabled. If combined with Traps Items, the percentage is split.
    Can present a challenge when playing with normal season flow, otherwise can act as an annoyance or out-of-logic opportunity for unlockable season flow.
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

dontstarvetogether_option_groups = [
    OptionGroup("Location Options", [
        CaveRegions,
        OceanRegions,
        Seasons,
        StartingSeason,
        DayPhases,
        CreatureLocations,
        BossLocations,
        CookingLocations,
        FarmingLocations,
        # SeasonalLocations,
    ]),
    OptionGroup("Item Options", [
        ShuffleStartingRecipes,
        ShuffleNoUnlockRecipes,
        ChessPieceSketchItems,
        SeedItems,
        ExtraDamageAgainstBosses,
        JunkItemAmount,
        TrapItems,
        SeasonTrapItems,
    ]),
    OptionGroup("Logic Options", [
        SeasonFlow,
        PlayerSkillLevel,
        LightingLogic,
        WeaponLogic,
        SeasonGearLogic,
        BaseMakingLogic,
        BackpackLogic,
        HealingLogic,
    ]),
]

@dataclass
class DSTOptions(PerGameCommonOptions):
    goal: Goal
    days_to_survive: DaysToSurvive
    required_bosses: RequiredBosses
    # craft_with_locked_items: CraftWithLockedItems
    death_link: DeathLink

    # Shuffling options
    cave_regions: CaveRegions
    ocean_regions: OceanRegions
    seasons: Seasons
    starting_season: StartingSeason
    day_phases: DayPhases
    creature_locations: CreatureLocations
    boss_locations: BossLocations
    cooking_locations: CookingLocations
    farming_locations: FarmingLocations
    # seasonal_locations: SeasonalLocations
    # season_change_helper_items: SeasonChangeHelperItems

    # Item options
    shuffle_starting_recipes: ShuffleStartingRecipes
    shuffle_no_unlock_recipes: ShuffleNoUnlockRecipes
    chesspiece_sketch_items: ChessPieceSketchItems
    seed_items: SeedItems
    extra_damage_against_bosses: ExtraDamageAgainstBosses
    junk_item_amount: JunkItemAmount
    trap_items: TrapItems
    season_trap_items: SeasonTrapItems

    # Logic options
    season_flow: SeasonFlow
    skill_level: PlayerSkillLevel
    lighting_logic: LightingLogic
    weapon_logic: WeaponLogic
    season_gear_logic: SeasonGearLogic
    base_making_logic: BaseMakingLogic
    backpack_logic: BackpackLogic
    healing_logic: HealingLogic