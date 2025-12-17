from dataclasses import dataclass

from schema import And, Optional, Schema
from Options import ExcludeLocations, OptionCounter, OptionDict, Toggle, PerGameCommonOptions, StartInventoryPool, Choice, DefaultOnToggle, Range, DeathLinkMixin, Visibility

level_prefixes = tuple(["Atl", "Crn", "Prt", "Pht", "FoF", "Otw"])
level_suffixes = tuple(["1", "2", "3", "!", "?"])

class VictoryCondition(Choice):
    """The condition needed to beat Glover.
    Endscreen: Get to the endscreen.
    Crystal Count: Get the number of crystals required."""
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Victory Condition"
    option_endscreen = 0
    option_crystal_count = 1
    option_golden_garibs = 2

class RequiredCrystals(Range):
    """The number of crystals needed to beat Glover while Victory Condition is Crystal Count. Default 4."""
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Required Crystals"
    range_start = 2
    range_end = 7
    default = 4

class GoldenGaribCount(Range):
    """The number of Golden Garibs in the world pool while Victory Condition is Golden Garibs. Default 12."""
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Golden Garib Count"
    range_start = 1
    range_end = 100
    default = 12

class GoldenGaribRequirement(Range):
    """The number of Golden Garibs required to win while Victory Condition is Golden Garibs. Default 6."""
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Golden Garibs Requirement"
    range_start = 1
    range_end = 100
    default = 6

class DifficultyLogic(Choice):
    """What tricks are allowed. Default Intended.
    Intended: No clips, no skips, no glitches. Things that are reasonable for a player to do.
    Easy Tricks: Jumping through the garib completion marks is expected. Things that are hard to do that don't require glitches, and minor skips are allowed.
    Hard Tricks: Any glitches and clips are expected.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Logic Difficulty"
    option_intended = 0
    option_easy_tricks = 1
    option_hard_tricks = 2

class StartingBall(Choice):
    """Set the ball you start with. Default Crystal.
    Any Random and Power Ball require Power Ball Transformation to be enabled.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Starting Ball"
    option_rubber_ball = 0
    option_bowling_ball = 1
    option_ball_bearing = 2
    option_crystal_ball = 3
    option_power_ball = 4
    option_random_no_power_ball = 5
    option_random_any = 6
    default = 3

class GaribLogic(Choice):
    """How the garibs are placed in logic. Default Garib Groups.
    Level Garibs: You get a check for getting all garibs in a level. You aren't sent garibs.
    Garib Groups: Each group of garibs in a level is a check. You are sent bundles of garibs.
    Garibsanity: Each garib is a check. You can be sent individual garibs.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Garib Logic"
    option_level_garibs = 0
    option_garib_groups = 1
    option_garibsanity = 2
    default = 1

class GaribSorting(Choice):
    """Where Garibs are sent to. Default In Order. Ignored if Garib Logic is Level Garibs.
    By Level: Garibs sent to you are from specific levels, and all garibs from that level must be gotten to get a completion mark.
    In Order: Garibs are sent to levels in world order.
    Random: Garibs are sent to levels in a random order.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Garib Sorting"
    option_by_level = 0
    option_in_order = 1
    option_random_order = 2
    default = 1

class GaribOrderOverrides(OptionCounter):
    """The postions of checkpoints when Garib Sorting is set to Random Order.
    Structured World Name[Level Number] : Array Positon
    Example "Atl3" : 0 (Starts the game's garib order with Atl3)"""
    visibility = Visibility.template | Visibility.spoiler | Visibility.complex_ui
    min = 0
    max = 23
    default = {}
    display_name = "Garib Order Overrides"

class RandomGaribSounds(Toggle):
    """Makes garib sounds use random sounds instead."""
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Random Garib Sounds"

class EntranceRandomizer(DefaultOnToggle):
    """Loading zones are randomized. Default on.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Entrance Randomizer"

class EntranceOverrides(OptionDict):
    """The postions of levels when Spawn Randomizer is on.
    Structured {"Level" : "Original Door"}
    Example [{"Atl1" : "FoF!"}, {"Atl?" : "Otw?"}]"""
    visibility = Visibility.template | Visibility.spoiler | Visibility.complex_ui
    schema = Schema({
        Optional(And(str, lambda level_name : level_name.startswith(level_prefixes)
            and level_name.endswith(level_suffixes) and len(level_name) == 4))
        :And(str, lambda door_name : door_name.startswith(level_prefixes)
            and door_name.endswith(level_suffixes) and len(door_name) == 4)
        })
    default = {}
    display_name = "Entrance Overrides"

class Portalsanity(Toggle):
    """Goals and All Garibs in Level are checks. Portals and garib completion marks are items. Default off.
    !! UNIMPLIMENTED !!
    """
    visibility = Visibility.spoiler
    display_name = "Portalsanity"

class GeneratePuml(Toggle):
    """Generates a .puml file of the world for debugging use with the AP Logic Builder. Default off.
    !! DEBUG !!
    """
    visibility = Visibility.none
    display_name = "Generate Puml"

class SpawningCheckpointRandomizer(Toggle):
    """Spawning checkpoints are randomized. Default off.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Spawn Randomizer"

class CheckpointOverrides(OptionCounter):
    """The postions of checkpoints when Spawn Randomizer is on.
    Structured World Name[Level Number] : [Checkpoint Number]
    Example "Atl3" : 2 (Spawns you at the top of the stairs in Atlantis 3)"""
    visibility = Visibility.template | Visibility.spoiler | Visibility.complex_ui
    min = 1
    max = 5
    default = {}
    display_name = "Checkpoint Overrides"

class EnableBonuses(DefaultOnToggle):
    """Makes Bonus Levels contain checks. Default on.
    """
    display_name = "Include Bonus Levels"
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui

class GloverExcludeLocations(ExcludeLocations):
    """Prevent these locations from having important item."""
    default = frozenset({"Atl? Goal"})

class TagLink(Toggle):
    """When you transform the ball, everyone who enabled tag link changes character or the ball. Of course, the reverse is true too. Default off.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Tag Link"

class TrapLink(Toggle):
    """When you get a trap, sends a similar trap to everyone else with trap link enabled. Of course, the reverse is true too. Default off.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Trap Link"


class RandomizeJump(Toggle):
    """Start without jump. Default off.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Randomize Jump"

class IncludePowerBall(Toggle):
    """Adds the Power Ball to the items. Default off.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Randomize Power Ball"

class CheckpointsChecks(Toggle):
    """Checkpoints are checks and items. Default off.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Randomize Checkpoints"

class SwitchesChecks(DefaultOnToggle):
    """Switches are checks and level events are items. Default on.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Randomize Switches"

class MrTipChecks(DefaultOnToggle):
    """Mr. Tips are checks. Default on.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Mr. Tip Checks"

class Enemysanity(Toggle):
    """Enemies that can normally be defeated are checks.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Enemysanity"

class Insectity(Toggle):
    """Defeating insects are checks.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Insectity"

class EasyBallWalk(Toggle):
    """Forces the game to de-invert ball controls.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Easy Ball Walk"

class MrHints(Choice):
    """Mr. Tips give AP hints. Default 1.
    Catagory only will tell you a vauge hint in regards to the quality, but not the item.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Mr. Tip Hints"
    option_off = 0
    option_balanced = 1
    option_catagory_only = 2
    option_chaos = 3
    option_traps = 4
    option_useful = 5
    option_progression = 6
    default = 1


class MrTipTextDisplay(Choice):
    """Sets the text of Mr. Tip Textboxes. Default Hints and Custom.
    Off: Ingame Mr. Tips do not display text.
    Hints and Custom: Displays hint text until there are no more hints, and then falls back to custom.
    Custom Only: Only displays custom text. Multiworld hints can still be given.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Mr. Tip Text Display"
    option_off = 0
    option_hints_and_custom = 1
    option_custom_only = 2
    default = 1

class MrTipScouts(DefaultOnToggle):
    """Makes Mr. Tip's hints show up as multiworld hints.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Mr. Hint Scouts"

class ChickenHints(Choice):
    """Cheat Chicken gives AP hints. Default 3.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Cheat Chicken Hints"
    option_off = 0
    option_balanced = 1
    option_catagory_only = 2
    option_chaos = 3
    option_traps = 4
    option_useful = 5
    option_progression = 6
    default = 3

class ExtraGaribsValue(Range):
    """How many Garibs 'Extra Garibs' are worth. Only applies if Garib Sorting is not By Level.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Bonus Garib"
    range_start = 1
    range_end = 20
    default = 4


class FillerExtraGaribsWeight(Range):
    """The weight of filler items that are Extra Garibs. Default is 0.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Extra Garibs Weight"
    range_start = 0
    range_end = 100
    default = 0

class FillerChickenSoundWeight(Range):
    """The weight of filler items that play a chicken noise. That's it. Default is 10.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Chicken Sound (Nothing) Weight"
    range_start = 0
    range_end = 100
    default = 10

class FillerLifeWeight(Range):
    """The weight of filler items that are Extra Lives. Default is 50.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Life Weight"
    range_start = 0
    range_end = 100
    default = 50

class FillerBoomerangBallWeight(Range):
    """The weight of filler items that are Boomerang Balls. Default is 5.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Boomerang Ball Weight"
    range_start = 0
    range_end = 100
    default = 5

class FillerBeachballWeight(Range):
    """The weight of filler items that are Beach Balls. Default is 5.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Beach Ball Weight"
    range_start = 0
    range_end = 100
    default = 5

class FillerHerculesPotionWeight(Range):
    """The weight of filler items that are Hercules Potions. Default is 5.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Hercules Potion Weight"
    range_start = 0
    range_end = 100
    default = 5

class FillerHelicopterPotionWeight(Range):
    """The weight of filler items that are Helicopter Potions. Default is 5.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Helicopter Potion Weight"
    range_start = 0
    range_end = 100
    default = 5

class FillerSpeedPotionWeight(Range):
    """The weight of filler items that are Speed Potions. Default is 5.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Speed Potion Weight"
    range_start = 0
    range_end = 100
    default = 5

class FillerFrogPotionWeight(Range):
    """The weight of filler items that are Frog Potions. Default is 5.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Frog Potion Weight"
    range_start = 0
    range_end = 100
    default = 5

class FillerDeathPotionWeight(Range):
    """The weight of filler items that are Death Potions. Default is 5.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Death Potion Weight"
    range_start = 0
    range_end = 100
    default = 5

class FillerStickyPotionWeight(Range):
    """The weight of filler items that are Sticky Potions. Default is 5.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Sticky Potion Weight"
    range_start = 0
    range_end = 100
    default = 5



class TrapPercentage(Range):
    """What percentage of checks that would be filler are replaced with traps. Default is 20.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Trap Weight"
    range_start = 0
    range_end = 100
    default = 20

class TrapFrogWeight(Range):
    """The weight of traps that are Frog Traps. Default is 20.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Frog Trap Weight"
    range_start = 0
    range_end = 100
    default = 20

class TrapCursedBallWeight(Range):
    """The weight of traps that are Cursed Ball. Default is 20.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Cursed Ball Trap Weight"
    range_start = 0
    range_end = 100
    default = 20

class TrapBecomesCrystalWeight(Range):
    """The weight of traps that are Crystal Transformations. Default is 15.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Instant Crystal Trap Weight"
    range_start = 0
    range_end = 100
    default = 15

class TrapCameraRotateWeight(Range):
    """The weight of traps that are Camera Tilts. Default is 15.
    """
    visibility = Visibility.template | Visibility.spoiler | Visibility.simple_ui
    display_name = "Camera Tilt Trap Weight"
    range_start = 0
    range_end = 100
    default = 15

class TrapTipWeight(Range):
    """The weight of traps that are Tips.
    !! UNIMPLIMENTED !!
    """
    visibility = Visibility.spoiler
    display_name = "Tip Trap Weight"
    range_start = 0
    range_end = 100
    default = 0

@dataclass
class GloverOptions(DeathLinkMixin, PerGameCommonOptions):
    victory_condition : VictoryCondition
    required_crystals : RequiredCrystals
    golden_garib_count : GoldenGaribCount
    required_golden_garibs : GoldenGaribRequirement
    difficulty_logic : DifficultyLogic
    starting_ball : StartingBall
    garib_logic : GaribLogic
    garib_sorting : GaribSorting
    garib_order_overrides : GaribOrderOverrides
    random_garib_sounds : RandomGaribSounds
    entrance_randomizer : EntranceRandomizer
    entrance_overrides : EntranceOverrides
    portalsanity : Portalsanity
    spawning_checkpoint_randomizer : SpawningCheckpointRandomizer
    checkpoint_overrides : CheckpointOverrides
    bonus_levels : EnableBonuses
    tag_link : TagLink
    trap_link : TrapLink

    randomize_jump : RandomizeJump
    include_power_ball : IncludePowerBall
    checkpoint_checks : CheckpointsChecks
    switches_checks : SwitchesChecks
    mr_tip_checks : MrTipChecks
    enemysanity : Enemysanity
    insectity : Insectity

    easy_ball_walk : EasyBallWalk

    mr_hints : MrHints
    chicken_hints : ChickenHints
    extra_garibs_value : ExtraGaribsValue
    mr_tip_text_display : MrTipTextDisplay
    mr_hints_scouts : MrTipScouts

    filler_extra_garibs_weight : FillerExtraGaribsWeight
    filler_chicken_sound_weight : FillerChickenSoundWeight
    filler_life_weight : FillerLifeWeight
    filler_boomerang_weight : FillerBoomerangBallWeight
    filler_beachball_weight : FillerBeachballWeight
    filler_hercules_weight : FillerHerculesPotionWeight
    filler_helicopter_weight : FillerHelicopterPotionWeight
    filler_speed_weight : FillerSpeedPotionWeight
    filler_frog_weight : FillerFrogPotionWeight
    filler_death_weight : FillerDeathPotionWeight
    filler_sticky_weight : FillerStickyPotionWeight

    trap_percentage : TrapPercentage
    frog_trap_weight : TrapFrogWeight
    cursed_ball_trap_weight : TrapCursedBallWeight
    instant_crystal_trap_weight : TrapBecomesCrystalWeight
    camera_rotate_trap_weight : TrapCameraRotateWeight
    tip_trap_weight : TrapTipWeight

    start_inventory_from_pool : StartInventoryPool
    #exclude_locations : GloverExcludeLocations
    generate_puml : GeneratePuml

