from dataclasses import dataclass

from Options import (
    Choice, DefaultOnToggle, ExcludeLocations, LocalItems, NonLocalItems, OptionGroup, PerGameCommonOptions,
    PriorityLocations, Range, StartHints, StartInventory, StartLocationHints, Toggle,
)
from . import ItemType, item_table
from .Constants import location_info


class IxupiCapturesNeeded(Range):
    """
    Number of Ixupi Captures needed for goal condition.
    """
    display_name = "Number of Ixupi Captures Needed"
    range_start = 1
    range_end = 10
    default = 10


class LobbyAccess(Choice):
    """
    Chooses how keys needed to reach the lobby are placed.
    - Normal: Keys are placed anywhere
    - Early: Keys are placed early 
    - Local: Keys are placed locally and early
    """
    display_name = "Lobby Access"
    option_normal = 0
    option_early = 1
    option_local = 2
    default = 1


class PuzzleHintsRequired(DefaultOnToggle):
    """
    If turned on puzzle hints/solutions will be available before the corresponding puzzle is required.

    For example: The Red Door puzzle will be logically required only after obtaining access to Beth's Address Book
    which gives you the solution.

    Turning this off allows for greater randomization.
    """
    display_name = "Puzzle Hints Required"


class InformationPlaques(Toggle):
    """
    Adds Information Plaques as checks.
    (40 Locations)
    """
    display_name = "Include Information Plaques"


class FrontDoorUsable(Toggle):
    """
    Adds a key to unlock the front door of the museum.
    """
    display_name = "Front Door Usable"


class ElevatorsStaySolved(DefaultOnToggle):
    """
    Adds elevators as checks and will remain open upon solving them.
    (3 Locations)
    """
    display_name = "Elevators Stay Solved"


class EarlyBeth(DefaultOnToggle):
    """
    Beth's body is open at the start of the game.
    This allows any pot piece to be placed in the slide and early checks on the second half of the final riddle.
    """
    display_name = "Early Beth"


class EarlyLightning(Toggle):
    """
    Allows lightning to be captured at any point in the game. You will still need to capture all ten Ixupi for victory.
    (1 Location)
    """
    display_name = "Early Lightning"


class LocationPotPieces(Choice):
    """
    Chooses where pot pieces will be located within the multiworld.
    - Own World: Pot pieces will be located within your own world
    - Different World: Pot pieces will be located in another world
    - Any World: Pot pieces will be located in any world
    """
    display_name = "Location of Pot Pieces"
    option_own_world = 0
    option_different_world = 1
    option_any_world = 2
    default = 2


class FullPots(Choice):
    """
    Chooses if pots will be in pieces or already completed
    - Pieces: Only pot pieces will be added to the item pool
    - Complete: Only completed pots will be added to the item pool
    - Mixed: Each pot will be randomly chosen to be pieces or already completed.
    """
    display_name = "Full Pots"
    option_pieces = 0
    option_complete = 1
    option_mixed = 2


class IxupiCapturesPriority(DefaultOnToggle):
    """
    Ixupi captures are set to priority locations. This forces a progression item into these locations if possible.
    """
    display_name = "Ixupi Captures are Priority"


class PuzzleCollectBehavior(Choice):
    """
    Defines what happens to puzzles on collect.
    - Solve None: No puzzles will be solved when collected.
    - Prevent Out Of Logic Access: All puzzles, except Red Door and Skull Door, will be solved when collected.
    This prevents out of logic access to Gods Room and Slide.
    - Solve All: All puzzles will be solved when collected. (original behavior)
    """
    display_name = "Puzzle Collect Behavior"
    option_solve_none = 0
    option_prevent_out_of_logic_access = 1
    option_solve_all = 2
    default = 1


# Need to override the default options to remove the goal items and goal locations so that they do not show on web.
valid_item_keys = [name for name, data in item_table.items() if data.type != ItemType.GOAL and data.code is not None]
valid_location_keys = [name for name in location_info["all_locations"] if name != "Mystery Solved"]


class ShiversLocalItems(LocalItems):
    __doc__ = LocalItems.__doc__
    valid_keys = valid_item_keys


class ShiversNonLocalItems(NonLocalItems):
    __doc__ = NonLocalItems.__doc__
    valid_keys = valid_item_keys


class ShiversStartInventory(StartInventory):
    __doc__ = StartInventory.__doc__
    valid_keys = valid_item_keys


class ShiversStartHints(StartHints):
    __doc__ = StartHints.__doc__
    valid_keys = valid_item_keys


class ShiversStartLocationHints(StartLocationHints):
    __doc__ = StartLocationHints.__doc__
    valid_keys = valid_location_keys


class ShiversExcludeLocations(ExcludeLocations):
    __doc__ = ExcludeLocations.__doc__
    valid_keys = valid_location_keys


class ShiversPriorityLocations(PriorityLocations):
    __doc__ = PriorityLocations.__doc__
    valid_keys = valid_location_keys


@dataclass
class ShiversOptions(PerGameCommonOptions):
    ixupi_captures_needed: IxupiCapturesNeeded
    lobby_access: LobbyAccess
    puzzle_hints_required: PuzzleHintsRequired
    include_information_plaques: InformationPlaques
    front_door_usable: FrontDoorUsable
    elevators_stay_solved: ElevatorsStaySolved
    early_beth: EarlyBeth
    early_lightning: EarlyLightning
    location_pot_pieces: LocationPotPieces
    full_pots: FullPots
    ixupi_captures_priority: IxupiCapturesPriority
    puzzle_collect_behavior: PuzzleCollectBehavior
    local_items: ShiversLocalItems
    non_local_items: ShiversNonLocalItems
    start_inventory: ShiversStartInventory
    start_hints: ShiversStartHints
    start_location_hints: ShiversStartLocationHints
    exclude_locations: ShiversExcludeLocations
    priority_locations: ShiversPriorityLocations


shivers_option_groups = [
    OptionGroup(
        "Item & Location Options", [
            ShiversLocalItems,
            ShiversNonLocalItems,
            ShiversStartInventory,
            ShiversStartHints,
            ShiversStartLocationHints,
            ShiversExcludeLocations,
            ShiversPriorityLocations
        ], True,
    ),
]
