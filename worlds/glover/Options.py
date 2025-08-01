from dataclasses import dataclass
from Options import ExcludeLocations, Toggle, DeathLink, PerGameCommonOptions, StartInventoryPool, Choice, DefaultOnToggle, Range

class DifficultyLogic(Choice):
    """What tricks are allowed. Default Intended.
    Intended: No clips, no skips, no glitches. Things that are reasonable for a player to do.
    Easy Tricks: Jumping through the garib completion marks is expected. Things that are hard to do that don't require glitches, and minor skips are allowed.
    Hard Tricks: Any glitches and clips are expected.
    """
    display_name = "Logic Difficulty"
    option_intended = 0
    option_easy_tricks = 1
    option_hard_tricks = 2

class StartingBall(Choice):
    """Set the ball you start with. Default Crystal.
    Any Random and Power Ball require Power Ball Transformation to be enabled.
    """
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
    display_name = "Garib Sorting"
    option_by_level = 0
    option_in_order = 1
    option_random = 2
    default = 1

class EntranceRandomizer(DefaultOnToggle):
    """Loading zones are randomized. Default on.
    """
    display_name = "Entrance Randomizer"

class SpawningCheckpointRandomizer(Toggle):
    """Spawning checkpoints are randomized. Default off.
    """
    display_name = "Spawn Randomizer"

class EnableBonuses(DefaultOnToggle):
    """Makes Bonus Levels contain checks. Default on.
    """
    display_name = "Include Bonus Levels"

class GloverExcludeLocations(ExcludeLocations):
    """Prevent these locations from having important item."""
    default = frozenset({"Atlantis_Bonus"})

class TagLink(Toggle):
    """When you transform the ball, everyone who enabled swap link changes character or the ball. Of course, the reverse is true too. Default off.
    """
    display_name = "Tag Link"



class RandomizeJump(Toggle):
    """Start without jump. Default off.
    """
    display_name = "Randomize Jump"

class IncludePowerBall(Toggle):
    """Adds the Power Ball to the items. Default off.
    """
    display_name = "Randomize Jump"

class CheckpointsChecks(Toggle):
    """Checkpoints are checks and items. Default off.
    """
    display_name = "Randomize Checkpoints"

class SwitchesChecks(DefaultOnToggle):
    """Switches are checks and level events are items. Default on.
    """
    display_name = "Randomize Switches"

class MrTipChecks(DefaultOnToggle):
    """Mr. Tips are checks. Default on.
    """
    display_name = "Mr. Tip Checks"



class MrHints(Choice):
    """Mr. Tips give AP hints. Default 1.
    """
    display_name = "Mr. Tip Hints"
    option_off = 0
    option_balanced = 1
    option_catagory_only = 2
    option_chaos = 3
    option_traps = 4
    option_useful = 5
    option_progression = 6
    default = 1

class ChickenHints(Choice):
    """Cheat Chicken gives AP hints. Default 3.
    """
    display_name = "Cheat Chicken Hints"
    option_off = 0
    option_balanced = 1
    option_catagory_only = 2
    option_chaos = 3
    option_traps = 4
    option_useful = 5
    option_progression = 6
    default = 3



class FillerExtraGaribsWeight(Range):
    """What percentage of filler items are extra Garibs. Default is 0.
    """
    display_name = "Extra Garibs Weight"
    range_start = 0
    range_end = 100
    default = 0

class FillerChickenSoundWeight(Range):
    """What percentage of filler items are nothing. Default is 10.
    """
    display_name = "Chicken Sound (Nothing) Weight"
    range_start = 0
    range_end = 100
    default = 10

class FillerLifeWeight(Range):
    """What percentage of filler items are Extra Lives. Default is 50.
    """
    display_name = "Life Weight"
    range_start = 0
    range_end = 100
    default = 50

class FillerBoomerangBallWeight(Range):
    """What percentage of filler items are Boomerang Balls. Default is 5.
    """
    display_name = "Boomerang Ball Weight"
    range_start = 0
    range_end = 100
    default = 5

class FillerBeachballWeight(Range):
    """What percentage of filler items are Beach Balls. Default is 5.
    """
    display_name = "Beach Ball Weight"
    range_start = 0
    range_end = 100
    default = 5

class FillerHerculesPotionWeight(Range):
    """What percentage of filler items are Hercules Potions. Default is 5.
    """
    display_name = "Hercules Potion Weight"
    range_start = 0
    range_end = 100
    default = 5

class FillerHelicopterPotionWeight(Range):
    """What percentage of filler items are Helicopter Potions. Default is 5.
    """
    display_name = "Helicopter Potion Weight"
    range_start = 0
    range_end = 100
    default = 5

class FillerSpeedPotionWeight(Range):
    """What percentage of filler items are Speed Potions. Default is 5.
    """
    display_name = "Speed Potion Weight"
    range_start = 0
    range_end = 100
    default = 5

class FillerFrogPotionWeight(Range):
    """What percentage of filler items are Frog Potions. Default is 5.
    """
    display_name = "Frog Potion Weight"
    range_start = 0
    range_end = 100
    default = 5

class FillerDeathPotionWeight(Range):
    """What percentage of filler items are Death Potions. Default is 5.
    """
    display_name = "Death Potion Weight"
    range_start = 0
    range_end = 100
    default = 5

class FillerStickyPotionWeight(Range):
    """What percentage of filler items are Sticky Potions. Default is 5.
    """
    display_name = "Sticky Potion Weight"
    range_start = 0
    range_end = 100
    default = 5



class TrapPercentage(Range):
    """What percentage of checks that would be filler are replaced with traps. Default is 20.
    """
    display_name = "Trap Weight"
    range_start = 0
    range_end = 100
    default = 20

class TrapFrogWeight(Range):
    """What percentage of traps are Frog Traps. Default is 20.
    """
    display_name = "Frog Trap Weight"
    range_start = 0
    range_end = 100
    default = 20

class TrapCursedBallWeight(Range):
    """What percentage of traps are Cursed Ball. Default is 20.
    """
    display_name = "Cursed Ball Trap Weight"
    range_start = 0
    range_end = 100
    default = 20

class TrapBecomesCrystalWeight(Range):
    """What percentage of traps are Crystal Transformations. Default is 15.
    """
    display_name = "Instant Crystal Trap Weight"
    range_start = 0
    range_end = 100
    default = 15

class TrapCameraRotateWeight(Range):
    """What percentage of traps are Camera Tilts. Default is 15.
    """
    display_name = "Camera Tilt Trap Weight"
    range_start = 0
    range_end = 100
    default = 15

class TrapTipWeight(Range):
    """What percentage of traps are Tips. Default is 30.
    """
    display_name = "Tip Trap Weight"
    range_start = 0
    range_end = 100
    default = 30

class GloverOptions(PerGameCommonOptions):
    difficulty_logic : DifficultyLogic
    starting_ball : StartingBall
    garib_logic : GaribLogic
    garib_sorting : GaribSorting
    entrance_randomizer : EntranceRandomizer
    spawning_checkpoint_randomizer : SpawningCheckpointRandomizer
    bonus_levels : EnableBonuses
    death_link : DeathLink
    tag_link : TagLink

    randomize_jump : RandomizeJump
    include_power_ball : IncludePowerBall
    checkpoint_checks : CheckpointsChecks
    switches_checks : SwitchesChecks
    mr_tip_checks : MrTipChecks

    mr_hints : MrHints
    chicken_hints : ChickenHints

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
    exclude_locations : GloverExcludeLocations

