from dataclasses import dataclass

from schema import And, Schema

from Options import Toggle, Choice, DefaultOnToggle, Range, PerGameCommonOptions, StartInventoryPool, OptionCounter, \
    OptionGroup
from .items import TRAP_ITEMS


class ShuffleDoors(Choice):
    """This option specifies how doors open.

    - **None:** Doors in the game will open the way they do in vanilla.
    - **Panels:** Doors still open as in vanilla, but the panels that open the
      doors will be locked, and an item will be required to unlock the panels.
    - **Doors:** the doors themselves are locked behind items, and will open
      automatically without needing to solve a panel once the key is obtained.
    """
    display_name = "Shuffle Doors"
    option_none = 0
    option_panels = 1
    option_doors = 2
    alias_simple = 2
    alias_complex = 2


class GroupDoors(Toggle):
    """By default, door shuffle in either panels or doors mode will create individual keys for every panel or door to be locked.
    
    When group doors is on, some panels and doors are sorted into logical groups, which are opened together by receiving an item."""
    display_name = "Group Doors"


class ProgressiveOrangeTower(DefaultOnToggle):
    """When "Shuffle Doors" is on doors mode, this setting governs the manner in which the Orange Tower floors open up.

    - **Off:** There is an item for each floor of the tower, and each floor's
      item is the only one needed to access that floor.
    - **On:** There are six progressive items, which open up the tower from the
      bottom floor upward.
    """
    display_name = "Progressive Orange Tower"


class ProgressiveColorful(DefaultOnToggle):
    """When "Shuffle Doors" is on either panels or doors mode and "Group Doors" is off, this setting governs the manner in which The Colorful opens up.

    - **Off:** There is an item for each room of The Colorful, meaning that
      random rooms in the middle of the sequence can open up without giving you
      access to them.
    - **On:** There are ten progressive items, which open up the sequence from
      White forward.
    """
    display_name = "Progressive Colorful"


class LocationChecks(Choice):
    """Determines what locations are available.

    - **Normal:** There will be a location check for each panel set that would
      ordinarily open a door, as well as for achievement panels and a small
      handful of other panels.
    - **Reduced:** Many of the locations that are associated with opening doors
      are removed.
    - **Insanity:** Every individual panel in the game is a location check.
    """
    display_name = "Location Checks"
    option_normal = 0
    option_reduced = 1
    option_insanity = 2


class ShuffleColors(DefaultOnToggle):
    """If on, an item is added to the pool for every puzzle color (besides White).

    You will need to unlock the requisite colors in order to be able to solve
    puzzles of that color.
    """
    display_name = "Shuffle Colors"


class ShufflePanels(Choice):
    """Determines how panel puzzles are randomized.

    - **None:** Most panels remain the same as in the base game. Note that there are
      some panels (in particular, in Starting Room and Second Room) that are changed
      by the randomizer even when panel shuffle is disabled.
    - **Rearrange:** The puzzles are the same as the ones in the base game, but are
      placed in different areas.

    More options for puzzle randomization are planned in the future.
    """
    display_name = "Shuffle Panels"
    option_none = 0
    option_rearrange = 1


class ShufflePaintings(Toggle):
    """If on, the destination, location, and appearance of the painting warps in the game will be randomized."""
    display_name = "Shuffle Paintings"


class EnablePilgrimage(Toggle):
    """Determines how the pilgrimage works.

    - **On:** You are required to complete a pilgrimage in order to access the
      Pilgrim Antechamber.
    - **Off:** The pilgrimage will be deactivated, and the sun painting will be
      added to the pool, even if door shuffle is off.
    """
    display_name = "Enable Pilgrimage"


class PilgrimageAllowsRoofAccess(DefaultOnToggle):
    """If on, you may use the Crossroads roof access during a pilgrimage (and you may be expected to do so).

    Otherwise, pilgrimage will be deactivated when going up the stairs.
    """
    display_name = "Allow Roof Access for Pilgrimage"


class PilgrimageAllowsPaintings(DefaultOnToggle):
    """If on, you may use paintings during a pilgrimage (and you may be expected to do so).

    Otherwise, pilgrimage will be deactivated when going through a painting.
    """
    display_name = "Allow Paintings for Pilgrimage"


class SunwarpAccess(Choice):
    """Determines how access to sunwarps works.

    - **Normal:** All sunwarps are enabled from the start.
    - **Disabled:** All sunwarps are disabled. Pilgrimage must be disabled when
      this is used.
    - **Unlock:** Sunwarps start off disabled, and all six activate once you
      receive an item.
    - **Individual:** Sunwarps start off disabled, and each has a corresponding
      item that unlocks it.
    - **Progressive:** Sunwarps start off disabled, and they unlock in order
      using a progressive item.
    """
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

    - **The End:** the goal is to solve THE END at the top of the tower.
    - **The Master:** The goal is to solve THE MASTER at the top of the tower,
      after getting the number of achievements specified in the Mastery
      Achievements option.
    - **Level 2:** The goal is to solve LEVEL 2 in the second room, after
      solving the number of panels specified in the Level 2 Requirement option.
    - **Pilgrimage:** The goal is to solve PILGRIM in the Pilgrim Antechamber,
      typically after performing a Pilgrimage.
    """
    display_name = "Victory Condition"
    option_the_end = 0
    option_the_master = 1
    option_level_2 = 2
    option_pilgrimage = 3


class MasteryAchievements(Range):
    """The number of achievements required to unlock THE MASTER.

    - In the base game, 21 achievements are needed.
    - If you include The Scientific and The Unchallenged, which are in the base
      game but are not counted for mastery, 23 would be required.
    - If you include the custom achievement (The Wanderer), 24 would be
      required.
    """
    display_name = "Mastery Achievements"
    range_start = 1
    range_end = 24
    default = 21


class Level2Requirement(Range):
    """The number of panel solves required to unlock LEVEL 2.

    In the base game, 223 are needed. Note that this count includes ANOTHER TRY.
    When set to 1, the panel hunt is disabled, and you can access LEVEL 2 for
    free.
    """
    display_name = "Level 2 Requirement"
    range_start = 1
    range_end = 800
    default = 223


class EarlyColorHallways(Toggle):
    """When on, a painting warp to the color hallways area will appear in the starting room.

    This lets you avoid being trapped in the starting room for long periods of
    time when door shuffle is on.
    """
    display_name = "Early Color Hallways"


class ShufflePostgame(Toggle):
    """When off, locations that could not be reached without also reaching your victory condition are removed."""
    display_name = "Shuffle Postgame"


class TrapPercentage(Range):
    """Replaces junk items with traps, at the specified rate."""
    display_name = "Trap Percentage"
    range_start = 0
    range_end = 100
    default = 20


class TrapWeights(OptionCounter):
    """Specify the distribution of traps that should be placed into the pool.

    If you don't want a specific type of trap, set the weight to zero.
    """
    display_name = "Trap Weights"
    valid_keys = TRAP_ITEMS
    min = 0
    default = {trap_name: 1 for trap_name in TRAP_ITEMS}


class SpeedBoostMode(Toggle):
    """
    If on, the player's default speed is halved, as if affected by a Slowness Trap. Speed Boosts are added to
    the item pool, which temporarily return the player to normal speed. Slowness Traps are removed from the pool.
    """
    display_name = "Speed Boost Mode"


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
        SpeedBoostMode,
        PuzzleSkipPercentage,
    ])
]


@dataclass
class LingoOptions(PerGameCommonOptions):
    shuffle_doors: ShuffleDoors
    group_doors: GroupDoors
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
    shuffle_postgame: ShufflePostgame
    trap_percentage: TrapPercentage
    trap_weights: TrapWeights
    speed_boost_mode: SpeedBoostMode
    puzzle_skip_percentage: PuzzleSkipPercentage
    death_link: DeathLink
    start_inventory_from_pool: StartInventoryPool
