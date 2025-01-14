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
    default = 0
    option_survival = 0
    option_bosses_any = 1
    option_bosses_all = 2

class DaysToSurvive(NamedRange):
    """
    Only applies for the survival goal. The number of days your character must survive for the survival goal.

    Each day would last 8 real life minutes on default settings. Being a ghost pauses your timer. Regenerating the world or dying in Wilderness mode resets your timer.
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

    "Random" chooses a random boss. If bosses are chosen along with it, it'll choose a random boss within your selection.

    Valid Bosses:
    Deerclops - Winter
    Moose/Goose - Spring
    Bearger - Autumn
    Ancient Guardian - Cave (Full)
    Antlion - Summer
    Dragonfly
    Bee Queen
    Klaus - Winter
    Toadstool - Cave
    Malbatross - Ocean
    Crab King - Ocean
    Frostjaw - Ocean
    Eye Of Terror - Night
    Retinazor - Night
    Spazmatism - Night
    Nightmare Werepig - Cave (Full)
    Scrappy Werepig - Cave (Full)
    Ancient Fuelweaver - Cave (Full), Night
    Celestial Champion - Ocean (Full)
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

class CraftingMode(Choice):
    """
    Change the crafting behavior?

    Vanilla: Crafting behavior is vanilla.

    Journey: Once you craft an item once, you can craft it again freely.

    Free Samples: Once you unlock a recipe, you can craft one for free.

    Free-Build: Once you unlock a recipe, you can always craft it.

    Locked Ingredients: You cannot craft items that use one of your missing items as an ingredient.

    """
    display_name = "Crafting Mode"
    default = 2
    option_vanilla = 0
    option_journey = 1
    option_free_samples = 2
    option_free_build = 3
    option_locked_ingredients = 4

class CaveRegions(Choice):
    """
    How far into the cave will your items and locations be shuffled?

    None: No cave. Choose this if you're making a no-cave world!

    Auto: Choose minimum regions based on your goal. (Survival goal will default to None. For boss goals, check the tooltip for "Boss Defeat Requirement".)

    Light: Shuffle caves without ruins and archive.

    Full: Shuffle caves, ruins, and archive.
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

    None: No ocean checks.

    Auto: Choose minimum regions based on your goal. (Survival goal will default to None. For boss goals, check the tooltip for "Boss Defeat Requirement".)

    Light: Shuffle ocean without moonstorm.

    Full: Shuffle ocean and moonstorm. Requires either Boss Locations to be "all" or Celestial Champion as your goal.
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

    This is not automatic. If changed from default, seasons will need to be set manually in your world settings!
    """
    display_name = "Seasons"
    default =    {SEASON.AUTUMN, SEASON.WINTER, SEASON.SPRING, SEASON.SUMMER}
    valid_keys = {SEASON.AUTUMN, SEASON.WINTER, SEASON.SPRING, SEASON.SUMMER}

class StartingSeason(Choice):
    """
    Which season do you start with in your world?

    This is not automatic. If not autumn, starting season will need to be set manually in your world settings!
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

    This is not automatic. If changed from default, day phases will need to be set manually in your world settings!

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

    All: Includes raid bosses. These are intended for multiplayer sessions, but can still be soloed with enough damage bonuses or creative strategies.
    """
    display_name = "Boss Locations"
    default = 1
    option_none = 0
    option_easy = 1
    option_all = 2

class CookingLocations(Choice):
    """
    Find items when cooking different foods in the crock pot? There's a good chance you'll need the wiki to get all of these: https://dontstarve.wiki.gg/wiki/Dishes

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

    This is exponential. With 10 stacks, this turns into x2.6 and x9.3 damage multipiers respectively. Multipliers can be configured in the mod configuration in the game's menu.

    This amount is separate from any prefilled through "Boss Fill Items" setting.
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
        "overkill": 20,
    }

class DamageBonuses(NamedRange):
    """
    This adds "Damage Bonus" buffs as Archipelago items.

    Each stack of this buff gives the player a permanent +10% damage against all mobs.

    This is exponential. With 10 stacks, this turns into a x2.6 multipier. Multiplier can be configured in the mod configuration in the game's menu.

    This amount is separate from any prefilled through "Boss Fill Items" setting.
    """
    display_name = "Damage Bonuses"
    range_start = 0
    range_end = 20
    default = 6

    special_range_names = {
        "none": 0,
        "low": 3,
        "medium": 6,
        "high": 10,
        "overkill": 20,
    }

class BossFillItems(Choice):
    """
    Choose what type of items a boss location can grant. Requires Boss Locations to be enabled.
    """
    display_name = "Boss Fill Items"
    default = 0
    option_normal = 0
    option_filler = 1
    option_priority = 2
    option_extra_damage_against_bosses = 11
    option_damage_bonus = 12

class ShuffleStartingRecipes(Toggle):
    """
    Turn your basic starting recipes into Archipelago items?

    This may leave you vulnerable to darkness on your first night! If you're not okay with this, you may want to add Torch to your starting items.

    Sphere 1 will also be small, making generation more restrictive when generating alone, and is prone to fail if "Creature Locations" are off!
    """
    display_name = "Shuffle Starting Recipes"

class ShuffleNoUnlockRecipes(Toggle):
    """
    Turn crafting recipes from the Ancient Pseudoscience Station and Celestial Altars into Archipelago items?
    """
    display_name = "Shuffle Ancient and Celestial Recipes"

class SeedItems(DefaultOnToggle):
    """
    Turn farm plant seeds into Archipelago items? When enabled, generic seeds can only grow weeds.
    """
    display_name = "Farm Plant Seed Items"

class SeasonFlow(Choice):
    """
    How do seasons progress in your world?

    Normal: Seasons progress as default. Logic attempts to prepare you for seasons in time, but not guaranteed. Seasonal checks may not have progression items.

    Unlockable: Season-changing items are progression. Seasonal checks may have progression items. Can optionally play with long seasons.

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

@dataclass
class DSTOptions(PerGameCommonOptions):
    goal: Goal
    days_to_survive: DaysToSurvive
    required_bosses: RequiredBosses
    crafting_mode: CraftingMode
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

    # Item options
    shuffle_starting_recipes: ShuffleStartingRecipes
    shuffle_no_unlock_recipes: ShuffleNoUnlockRecipes
    chesspiece_sketch_items: ChessPieceSketchItems
    seed_items: SeedItems
    extra_damage_against_bosses: ExtraDamageAgainstBosses
    damage_bonuses: DamageBonuses
    boss_fill_items: BossFillItems
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

dontstarvetogether_option_groups = [
    OptionGroup("Season and Day Phase Options", [
        Seasons,
        StartingSeason,
        SeasonFlow,
        DayPhases,
    ]),
    OptionGroup("Location Options", [
        CaveRegions,
        OceanRegions,
        CreatureLocations,
        BossLocations,
        CookingLocations,
        FarmingLocations,
    ]),
    OptionGroup("Item Options", [
        ShuffleStartingRecipes,
        ShuffleNoUnlockRecipes,
        ChessPieceSketchItems,
        SeedItems,
        JunkItemAmount,
        TrapItems,
        SeasonTrapItems,
    ]),
    OptionGroup("Buff Options", [
        ExtraDamageAgainstBosses,
        DamageBonuses,
    ]),
    OptionGroup("Logic Options", [
        PlayerSkillLevel,
        LightingLogic,
        WeaponLogic,
        SeasonGearLogic,
        BaseMakingLogic,
        BackpackLogic,
        HealingLogic,
    ]),
]

dontstarvetogether_option_presets = {
    "Year Survival (Easy)": {
        "goal": "survival",
        "days_to_survive": 70,
        "season_flow": "normal",
        "season_gear_logic": "enabled",
        "seed_items": False,
    },
    "Season Giants (Easy)": {
        "goal": "bosses_all",
        "required_bosses": {"Deerclops", "Moose/Goose", "Antlion", "Bearger"},
        "season_flow": "unlockable_shuffled",
    },
    "Ancient Guardian (Easy)": {
        "goal": "bosses_any",
        "required_bosses": {"Ancient Guardian"},
        "cave_regions": "full",
        "season_flow": "unlockable",
    },
    "RPG Mode (Advanced)": {
        "goal": "bosses_any",
        "required_bosses": {"Random", "Ancient Fuelweaver", "Celestial Champion"},
        "cave_regions": "full",
        "ocean_regions": "full",
        "boss_locations": "all",
        "starting_season": "random",
        "season_flow": "unlockable_shuffled",
        "crafting_mode": "journey",
        "boss_fill_items": "extra_damage_against_bosses",
        "shuffle_starting_recipes": True,
        "shuffle_no_unlock_recipes": True,
        "chesspiece_sketch_items": True,
        "extra_damage_against_bosses": 0,
        "damage_bonuses": 20,
        "skill_level": "advanced",
        "weapon_logic": "none",
        "healing_logic": "none",
        "start_inventory": {"Torch": 1, "Booster Shot": 1}
    },
}