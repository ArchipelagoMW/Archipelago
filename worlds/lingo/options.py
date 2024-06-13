from dataclasses import dataclass

from schema import And, Schema

from Options import Toggle, Choice, DefaultOnToggle, Range, PerGameCommonOptions, StartInventoryPool, OptionDict, \
    OptionGroup
from .items import TRAP_ITEMS


class ShuffleDoors(Choice):
    """If on, opening doors will require their respective "keys".
    In "simple", doors are sorted into logical groups, which are all opened by receiving an item.
    In "complex", the items are much more granular, and will usually only open a single door each."""
    display_name = "Shuffle Doors"
    option_none = 0
    option_simple = 1
    option_complex = 2


class ProgressiveOrangeTower(DefaultOnToggle):
    """When "Shuffle Doors" is on, this setting governs the manner in which the Orange Tower floors open up.
    If off, there is an item for each floor of the tower, and each floor's item is the only one needed to access that floor.
    If on, there are six progressive items, which open up the tower from the bottom floor upward.
    """
    display_name = "Progressive Orange Tower"


class ProgressiveColorful(DefaultOnToggle):
    """When "Shuffle Doors" is on "complex", this setting governs the manner in which The Colorful opens up.
    If off, there is an item for each room of The Colorful, meaning that random rooms in the middle of the sequence can open up without giving you access to them.
    If on, there are ten progressive items, which open up the sequence from White forward."""
    display_name = "Progressive Colorful"


class LocationChecks(Choice):
    """Determines what locations are available.
    On "normal", there will be a location check for each panel set that would ordinarily open a door, as well as for achievement panels and a small handful of other panels.
    On "reduced", many of the locations that are associated with opening doors are removed.
    On "insanity", every individual panel in the game is a location check."""
    display_name = "Location Checks"
    option_normal = 0
    option_reduced = 1
    option_insanity = 2


class ShuffleColors(DefaultOnToggle):
    """
    If on, an item is added to the pool for every puzzle color (besides White).
    You will need to unlock the requisite colors in order to be able to solve puzzles of that color.
    """
    display_name = "Shuffle Colors"


class ShufflePanels(Choice):
    """If on, the puzzles on each panel are randomized.
    On "rearrange", the puzzles are the same as the ones in the base game, but are placed in different areas."""
    display_name = "Shuffle Panels"
    option_none = 0
    option_rearrange = 1


class ShufflePaintings(Toggle):
    """If on, the destination, location, and appearance of the painting warps in the game will be randomized."""
    display_name = "Shuffle Paintings"


class EnablePilgrimage(Toggle):
    """Determines how the pilgrimage works.
    If on, you are required to complete a pilgrimage in order to access the Pilgrim Antechamber.
    If off, the pilgrimage will be deactivated, and the sun painting will be added to the pool, even if door shuffle is off."""
    display_name = "Enable Pilgrimage"


class PilgrimageAllowsRoofAccess(DefaultOnToggle):
    """
    If on, you may use the Crossroads roof access during a pilgrimage (and you may be expected to do so).
    Otherwise, pilgrimage will be deactivated when going up the stairs.
    """
    display_name = "Allow Roof Access for Pilgrimage"


class PilgrimageAllowsPaintings(DefaultOnToggle):
    """
    If on, you may use paintings during a pilgrimage (and you may be expected to do so).
    Otherwise, pilgrimage will be deactivated when going through a painting.
    """
    display_name = "Allow Paintings for Pilgrimage"


class SunwarpAccess(Choice):
    """Determines how access to sunwarps works.
    On "normal", all sunwarps are enabled from the start.
    On "disabled", all sunwarps are disabled. Pilgrimage must be disabled when this is used.
    On "unlock", sunwarps start off disabled, and all six activate once you receive an item.
    On "individual", sunwarps start off disabled, and each has a corresponding item that unlocks it.
    On "progressive", sunwarps start off disabled, and they unlock in order using a progressive item."""
    display_name = "Sunwarp Access"
    option_normal = 0
    option_disabled = 1
    option_unlock = 2
    option_individual = 3
    option_progressive = 4


class ShuffleSunwarps(Toggle):
    """If on, the pairing and ordering of the sunwarps in the game will be randomized."""
    display_name = "Shuffle Sunwarps"


class VictoryCondition(Choice):
    """Change the victory condition.
    On "the_end", the goal is to solve THE END at the top of the tower.
    On "the_master", the goal is to solve THE MASTER at the top of the tower, after getting the number of achievements specified in the Mastery Achievements option.
    On "level_2", the goal is to solve LEVEL 2 in the second room, after solving the number of panels specified in the Level 2 Requirement option.
    On "pilgrimage", the goal is to solve PILGRIM in the Pilgrim Antechamber, typically after performing a Pilgrimage."""
    display_name = "Victory Condition"
    option_the_end = 0
    option_the_master = 1
    option_level_2 = 2
    option_pilgrimage = 3


class MasteryAchievements(Range):
    """The number of achievements required to unlock THE MASTER.
    In the base game, 21 achievements are needed.
    If you include The Scientific and The Unchallenged, which are in the base game but are not counted for mastery, 23 would be required.
    If you include the custom achievement (The Wanderer), 24 would be required.
    """
    display_name = "Mastery Achievements"
    range_start = 1
    range_end = 24
    default = 21


class Level2Requirement(Range):
    """The number of panel solves required to unlock LEVEL 2.
    In the base game, 223 are needed.
    Note that this count includes ANOTHER TRY.
    When set to 1, the panel hunt is disabled, and you can access LEVEL 2 for free.
    """
    display_name = "Level 2 Requirement"
    range_start = 1
    range_end = 800
    default = 223


class EarlyColorHallways(Toggle):
    """
    When on, a painting warp to the color hallways area will appear in the starting room.
    This lets you avoid being trapped in the starting room for long periods of time when door shuffle is on.
    """
    display_name = "Early Color Hallways"


class TrapPercentage(Range):
    """Replaces junk items with traps, at the specified rate."""
    display_name = "Trap Percentage"
    range_start = 0
    range_end = 100
    default = 20


class TrapWeights(OptionDict):
    """
    Specify the distribution of traps that should be placed into the pool.
    If you don't want a specific type of trap, set the weight to zero.
    """
    display_name = "Trap Weights"
    schema = Schema({trap_name: And(int, lambda n: n >= 0) for trap_name in TRAP_ITEMS})
    default = {trap_name: 1 for trap_name in TRAP_ITEMS}


class PuzzleSkipPercentage(Range):
    """Replaces junk items with puzzle skips, at the specified rate."""
    display_name = "Puzzle Skip Percentage"
    range_start = 0
    range_end = 100
    default = 20


class DeathLink(Toggle):
    """If on: Whenever another player on death link dies, you will be returned to the starting room."""
    display_name = "Death Link"


lingo_option_groups = [
    OptionGroup("Pilgrimage", [
        EnablePilgrimage,
        PilgrimageAllowsRoofAccess,
        PilgrimageAllowsPaintings,
        SunwarpAccess,
        ShuffleSunwarps,
    ]),
    OptionGroup("Fine-tuning", [
        ProgressiveOrangeTower,
        ProgressiveColorful,
        MasteryAchievements,
        Level2Requirement,
        TrapPercentage,
        TrapWeights,
        PuzzleSkipPercentage,
    ])
]


@dataclass
class LingoOptions(PerGameCommonOptions):
    shuffle_doors: ShuffleDoors
    progressive_orange_tower: ProgressiveOrangeTower
    progressive_colorful: ProgressiveColorful
    location_checks: LocationChecks
    shuffle_colors: ShuffleColors
    shuffle_panels: ShufflePanels
    shuffle_paintings: ShufflePaintings
    enable_pilgrimage: EnablePilgrimage
    pilgrimage_allows_roof_access: PilgrimageAllowsRoofAccess
    pilgrimage_allows_paintings: PilgrimageAllowsPaintings
    sunwarp_access: SunwarpAccess
    shuffle_sunwarps: ShuffleSunwarps
    victory_condition: VictoryCondition
    mastery_achievements: MasteryAchievements
    level_2_requirement: Level2Requirement
    early_color_hallways: EarlyColorHallways
    trap_percentage: TrapPercentage
    trap_weights: TrapWeights
    puzzle_skip_percentage: PuzzleSkipPercentage
    death_link: DeathLink
    start_inventory_from_pool: StartInventoryPool
