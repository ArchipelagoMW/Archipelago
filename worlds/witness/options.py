from dataclasses import dataclass
from Options import Toggle, DefaultOnToggle, Range, Choice, PerGameCommonOptions


class DisableNonRandomizedPuzzles(Toggle):
    """Disables puzzles that cannot be randomized.
    This includes many puzzles that heavily involve the environment, such as Shadows, Monastery or Orchard.
    The lasers for those areas will activate as you solve optional puzzles, such as Discarded Panels.
    Additionally, the panels activating Monastery Laser and Jungle Popup Wall will be on from the start."""
    display_name = "Disable non randomized puzzles"


class EarlyCaves(Choice):
    """Adds an item that opens the Caves Shortcuts to Swamp and Mountain,
    allowing early access to the Caves even if you are not playing a remote Door Shuffle mode.
    You can either add this item to the pool to be found on one of your randomized checks,
    or you can outright start with it and have immediate access to the Caves.
    If you choose "add_to_pool" and you are already playing a remote Door Shuffle mode, this setting will do nothing."""
    display_name = "Early Caves"
    option_off = 0
    option_add_to_pool = 1
    option_starting_inventory = 2


class ShuffleSymbols(DefaultOnToggle):
    """You will need to unlock puzzle symbols as items to be able to solve the panels that contain those symbols.
    If you turn this off, there will be no progression items in the game unless you turn on door shuffle."""
    display_name = "Shuffle Symbols"


class ShuffleLasers(Toggle):
    """If on, the 11 lasers are turned into items and will activate on their own upon receiving them.
    Note: There is a visual bug that can occur with the Desert Laser. It does not affect gameplay - The Laser can still
    be redirected as normal, for both applications of redirection."""
    display_name = "Shuffle Lasers"


class ShuffleDoors(Choice):
    """If on, opening doors, moving bridges etc. will require a "key".
    If set to "panels", the panel on the door will be locked until receiving its corresponding key.
    If set to "doors", the door will open immediately upon receiving its key. Door panels are added as location checks.
    "Mixed" includes all doors from "doors", and all control panels (bridges, elevators etc.) from "panels"."""
    display_name = "Shuffle Doors"
    option_off = 0
    option_panels = 1
    option_doors = 2
    option_mixed = 3


class DoorGroupings(Choice):
    """If set to "none", there will be one key for every door, resulting in up to 120 keys being added to the item pool.
    If set to "regional", all doors in the same general region will open at once with a single key,
    reducing the amount of door items and complexity."""
    display_name = "Door Groupings"
    option_off = 0
    option_regional = 1


class ShuffleBoat(DefaultOnToggle):
    """If set, adds a "Boat" item to the item pool. Before receiving this item, you will not be able to use the boat."""
    display_name = "Shuffle Boat"


class ShuffleDiscardedPanels(Toggle):
    """Add Discarded Panels into the location pool.
    Solving certain Discarded Panels may still be necessary to beat the game, even if this is off - The main example
    of this being the alternate activation triggers in disable_non_randomized."""

    display_name = "Shuffle Discarded Panels"


class ShuffleVaultBoxes(Toggle):
    """Add Vault Boxes to the location pool."""
    display_name = "Shuffle Vault Boxes"


class ShuffleEnvironmentalPuzzles(Choice):
    """
    Add Environmental/Obelisk Puzzles into the location pool.
    In "individual", every Environmental Puzzle sends an item.
    In "obelisk_sides", completing every puzzle on one side of an Obelisk sends an item.
    Note: In Obelisk Sides, any EPs excluded through another setting will be counted as pre-completed on their Obelisk.
    """
    display_name = "Shuffle Environmental Puzzles"
    option_off = 0
    option_individual = 1
    option_obelisk_sides = 2


class ShuffleDog(Toggle):
    """Add petting the Town dog into the location pool."""

    display_name = "Pet the Dog"


class EnvironmentalPuzzlesDifficulty(Choice):
    """
    When "Shuffle Environmental Puzzles" is on, this setting governs which EPs are eligible for the location pool.
    On "eclipse", every EP in the game is eligible, including the 1-hour-long "Theater Eclipse EP".
    On "tedious", Theater Eclipse EP is excluded from the location pool.
    On "normal", several other difficult or long EPs are excluded as well.
    """
    display_name = "Environmental Puzzles Difficulty"
    option_normal = 0
    option_tedious = 1
    option_eclipse = 2


class ShufflePostgame(Toggle):
    """Adds locations into the pool that are guaranteed to become accessible after or at the same time as your goal.
    Use this if you don't play with release on victory. IMPORTANT NOTE: The possibility of your second
    "Progressive Dots" showing up in the Caves is ignored, they will still be considered "postgame" in base settings."""
    display_name = "Shuffle Postgame"


class VictoryCondition(Choice):
    """Change the victory condition from the original game's ending (elevator) to beating the Challenge
    or solving the mountaintop box, either using the short solution
    (7 lasers or whatever you've changed it to) or the long solution (11 lasers or whatever you've changed it to)."""
    display_name = "Victory Condition"
    option_elevator = 0
    option_challenge = 1
    option_mountain_box_short = 2
    option_mountain_box_long = 3


class PuzzleRandomization(Choice):
    """Puzzles in this randomizer are randomly generated. This setting changes the difficulty/types of puzzles."""
    display_name = "Puzzle Randomization"
    option_sigma_normal = 0
    option_sigma_expert = 1
    option_none = 2


class MountainLasers(Range):
    """Sets the amount of beams required to enter the final area."""
    display_name = "Required Lasers for Mountain Entry"
    range_start = 1
    range_end = 7
    default = 7


class ChallengeLasers(Range):
    """Sets the amount of beams required to enter the Caves through the Mountain Bottom Floor Discard."""
    display_name = "Required Lasers for Challenge"
    range_start = 1
    range_end = 11
    default = 11


class ElevatorsComeToYou(Toggle):
    """If true, the Quarry Elevator, Bunker Elevator and Swamp Long Bridge will "come to you" if you approach them.
    This does actually affect logic as it allows unintended backwards / early access into these areas."""
    display_name = "All Bridges & Elevators come to you"


class TrapPercentage(Range):
    """Replaces junk items with traps, at the specified rate."""
    display_name = "Trap Percentage"
    range_start = 0
    range_end = 100
    default = 20


class PuzzleSkipAmount(Range):
    """Adds this number of Puzzle Skips into the pool, if there is room. Puzzle Skips let you skip one panel.
    Works on most panels in the game - The only big exception is The Challenge."""
    display_name = "Puzzle Skips"
    range_start = 0
    range_end = 30
    default = 10


class HintAmount(Range):
    """Adds hints to Audio Logs. If set to a low amount, up to 2 additional duplicates of each hint will be added.
    Remaining Audio Logs will have junk hints."""
    display_name = "Hints on Audio Logs"
    range_start = 0
    range_end = 49
    default = 10


class DeathLink(Toggle):
    """If on: Whenever you fail a puzzle (with some exceptions), everyone who is also on Death Link dies.
    The effect of a "death" in The Witness is a Power Surge."""
    display_name = "Death Link"


@dataclass
class TheWitnessOptions(PerGameCommonOptions):
    puzzle_randomization: PuzzleRandomization
    shuffle_symbols: ShuffleSymbols
    shuffle_doors: ShuffleDoors
    door_groupings: DoorGroupings
    shuffle_boat: ShuffleBoat
    shuffle_lasers: ShuffleLasers
    disable_non_randomized_puzzles: DisableNonRandomizedPuzzles
    shuffle_discarded_panels: ShuffleDiscardedPanels
    shuffle_vault_boxes: ShuffleVaultBoxes
    shuffle_EPs: ShuffleEnvironmentalPuzzles
    EP_difficulty: EnvironmentalPuzzlesDifficulty
    shuffle_postgame: ShufflePostgame
    victory_condition: VictoryCondition
    mountain_lasers: MountainLasers
    challenge_lasers: ChallengeLasers
    early_caves: EarlyCaves
    elevators_come_to_you: ElevatorsComeToYou
    trap_percentage: TrapPercentage
    puzzle_skip_amount: PuzzleSkipAmount
    hint_amount: HintAmount
    death_link: DeathLink
