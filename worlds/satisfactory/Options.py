from dataclasses import dataclass
from typing import Dict, List, Any, Tuple, ClassVar, cast
from enum import IntEnum
from Options import PerGameCommonOptions, DeathLink, AssembleOptions, Visibility
from Options import Range, Toggle, OptionSet, StartInventoryPool, NamedRange, Choice

class Placement(IntEnum):
    starting_inventory = 0
    early = 1
    somewhere = 2

class PlacementLogicMeta(AssembleOptions):
    def __new__(mcs, name: str, bases: Tuple[type], attrs: Dict[Any, Any]) -> "PlacementLogicMeta":
        if "default" in attrs and isinstance(attrs["default"], Placement):
            attrs["default"] = int(attrs["default"])

        cls = super(PlacementLogicMeta, mcs).__new__(mcs, name, bases, attrs)
        return cast(PlacementLogicMeta, cls)

class PlacementLogic(Choice, metaclass=PlacementLogicMeta):
    option_unlocked_from_start = Placement.starting_inventory
    option_early_game = Placement.early
    option_somewhere = Placement.somewhere

class ChoiceMapMeta(AssembleOptions):
    def __new__(mcs, name: str, bases: Tuple[type], attrs: Dict[Any, Any]) -> "ChoiceMapMeta":
        if "choices" in attrs:
            for index, choice in enumerate(attrs["choices"].keys()):
                option_name = "option_" + choice.replace(' ', '_')
                attrs[option_name] = index

        cls = super(ChoiceMapMeta, mcs).__new__(mcs, name, bases, attrs)
        return cast(ChoiceMapMeta, cls)

class ChoiceMap(Choice, metaclass=ChoiceMapMeta):
    # TODO `default` doesn't do anything, default is always the first `choices` value. if uncommented it messes up the template file generation (caps mismatch)
    choices: ClassVar[Dict[str, List[str]]]

    def get_selected_list(self) -> List[str]:
        for index, choice in enumerate(self.choices.keys()):
            if index == self.value:
                return self.choices[choice]


class ElevatorTier(NamedRange):
    """
    Ship these Space Elevator packages to finish.
    Does nothing if *Space Elevator Tier* goal is not enabled.
    """
    display_name = "Goal: Space Elevator shipment"
    default = 2
    range_start = 1
    range_end = 4
    special_range_names = {
        "one package (tiers 1-2)": 1,
        "two packages (tiers 1-4)": 2,
        "three packages (tiers 1-6)": 3,
        "four packages (tiers 7-8)": 4,
        "five packages (tier 9)": 5,
    }

class ResourceSinkPoints(NamedRange):
    """
    Sink an amount of items totalling this amount of points to finish.
    This setting is a *point count*, not a *coupon* count!
    Does nothing if *AWESOME Sink Points* goal is not enabled.

    In the base game, it takes 347 coupons to unlock every non-repeatable purchase, or 1895 coupons to purchase every non-producible item.

    Use the **TFIT - Ficsit Information Tool** mod or the Satisfactory wiki to find out how many points items are worth.

    If you have *Free Samples* enabled, consider setting this higher so that you can't reach the goal just by sinking your Free Samples.
    """
    # Coupon data for above comment from https://satisfactory.wiki.gg/wiki/AWESOME_Shop
    display_name = "Goal: AWESOME Sink points"
    default = 2166000
    range_start = 2166000
    range_end = 18436379500
    special_range_names = {
        "50 coupons (~2m points)": 2166000,
        "100 coupons (~18m points)": 17804500,
        "150 coupons (~61m points)": 60787500,
        "200 coupons (~145m points)": 145053500,
        "250 coupons (~284m points)": 284442000,
        "300 coupons (~493m points)": 492825000,
        "350 coupons (~784m points)": 784191000,
        "400 coupons (~1,2b points)": 1172329500,
        "450 coupons (~1,7b points)": 1671112500,
        "500 coupons (~2b points)": 2294578500,
        "550 coupons (~3b points)": 3056467000,
        "600 coupons (~4b points)": 3970650000,
        "650 coupons (~5b points)": 5051216000,
        "700 coupons (~6b points)": 6311854500,
        "750 coupons (~8b points)": 7766437500,
        "800 coupons (~9b points)": 9429103500,
        "850 coupons (~11b points)": 11313492000,
        "900 coupons (~13b points)": 13433475000,
        "950 coupons (~16b points)": 15803241000,
        "1000 coupons (~18b points)": 18436379500
    }

class HardDriveProgressionLimit(Range):
    """
    How many Hard Drives can contain progression items.
    Hard Drives above this count cannot contain progression, but can still be Useful.
    
    There are 118 total hard drives in the world and the current implementation supports up to 100 progression hard drives.
    """
    display_name = "Hard Drive Progression Items"
    default = 20
    range_start = 0
    range_end = 100

class FreeSampleEquipment(Range):
    """
    How many free sample items of Equipment items should be given when they are unlocked.
    
    (ex. Jetpack, Rifle)
    """
    display_name = "Free Samples: Equipment"
    default = 1
    range_start = 0
    range_end = 10

class FreeSampleBuildings(Range):
    """
    How many copies of a Building's construction cost to give as a free sample when they are unlocked.
    Space Elevator is always excluded.
    
    (ex. Packager, Constructor, Smelter)
    """
    display_name = "Free Samples: Buildings"
    default = 5
    range_start = 0
    range_end = 10

class FreeSampleParts(NamedRange):
    """
    How free sample items of general crafting components should be given when a recipe for them is unlocked.
    Space Elevator Project Parts are always excluded.
    
    Negative numbers mean that fraction of a full stack.
    
    (ex. Iron Plate, Packaged Turbofuel, Reinforced Modular Frame)
    """
    display_name = "Free Samples: Parts"
    default = -2
    range_start = -5
    range_end = 500
    special_range_names = {
        "disabled": 0,
        "half_stack": -2,
        "one_stack": -1,
        "1": 1,
        "50": 50,
        "100": 100,
        "200": 200,
        "500": 500,
    }

class FreeSampleRadioactive(Toggle):
    """
    Allow free samples to include radioactive parts.
    Remember, they are delivered directly to your player inventory.
    """
    display_name = "Free Samples: Radioactive"

class TrapChance(Range):
    """
    Chance of traps in the item pool.
    Traps will only replace filler items such as parts and resources.
    
    - **0:** No traps will be present
    - **100:** Every filler item will be a trap.
    """
    display_name = "Trap Chance"
    range_start = 0
    range_end = 100
    default = 10

_trap_types = {
        "Trap: Doggo with Pulse Nobelisk", 
        "Trap: Doggo with Nuke Nobelisk", 
        "Trap: Doggo with Gas Nobelisk", 
        "Trap: Hog",
        "Trap: Alpha Hog",
        "Trap: Cliff Hog",
        "Trap: Nuclear Hog",
        "Trap: Johnny",
        "Trap: Hatcher",
        "Trap: Elite Hatcher",
        "Trap: Small Stinger",
        "Trap: Stinger",
        "Trap: Gas Stinger",
        "Trap: Spore Flower",
        "Trap: Spitter",
        "Trap: Alpha Spitter",
        "Trap: Not the Bees",
        "Trap: Nuclear Waste Drop",
        "Trap: Plutonium Waste Drop",
        "Trap: Can of Beans",
        "Trap: Fart Cloud",

        # Radioactive parts delivered via portal
        "Bundle: Uranium",
        "Bundle: Uranium Fuel Rod",
        "Bundle: Uranium Waste",
        "Bundle: Plutonium Fuel Rod",
        "Bundle: Plutonium Pellet",
        "Bundle: Plutonium Waste",
        "Bundle: Non-fissile Uranium",
        "Bundle: Ficsonium",
        "Bundle: Ficsonium Fuel Rod"
    }

class TrapSelectionPreset(ChoiceMap):
    """
    Themed presets of trap types to enable.

    If you want more control, use *Trap Override* or visit the Weighted Options page.
    """
    display_name = "Trap Presets"
    choices = {
        "Normal": ["Trap: Doggo with Pulse Nobelisk", "Trap: Doggo with Gas Nobelisk", "Trap: Hog", "Trap: Alpha Hog", "Trap: Hatcher", "Trap: Elite Hatcher", "Trap: Small Stinger", "Trap: Stinger", "Trap: Spitter", "Trap: Alpha Spitter", "Trap: Not the Bees", "Trap: Nuclear Waste Drop", "Bundle: Uranium", "Bundle: Non-fissile Uranium", "Trap: Can of Beans", "Trap: Fart Cloud"],
        "Gentle": ["Trap: Doggo with Pulse Nobelisk", "Trap: Hog", "Trap: Spitter", "Trap: Can of Beans"],
        "Harder": ["Trap: Doggo with Pulse Nobelisk", "Trap: Doggo with Nuke Nobelisk", "Trap: Doggo with Gas Nobelisk", "Trap: Alpha Hog", "Trap: Cliff Hog", "Trap: Spore Flower", "Trap: Hatcher", "Trap: Elite Hatcher", "Trap: Stinger", "Trap: Alpha Spitter", "Trap: Not the Bees", "Trap: Fart Cloud", "Trap: Nuclear Waste Drop", "Trap: Plutonium Waste Drop", "Bundle: Uranium", "Bundle: Uranium Fuel Rod", "Bundle: Uranium Waste", "Bundle: Plutonium Fuel Rod", "Bundle: Plutonium Pellet", "Bundle: Plutonium Waste", "Bundle: Non-fissile Uranium"],
        "All": list(_trap_types),
        "Ruthless": ["Trap: Doggo with Nuke Nobelisk", "Trap: Nuclear Hog", "Trap: Cliff Hog", "Trap: Elite Hatcher", "Trap: Spore Flower", "Trap: Gas Stinger", "Trap: Nuclear Waste Drop", "Trap: Plutonium Waste Drop", "Bundle: Uranium Fuel Rod", "Bundle: Uranium Waste", "Bundle: Plutonium Fuel Rod", "Bundle: Plutonium Pellet", "Bundle: Plutonium Waste", "Bundle: Non-fissile Uranium", "Bundle: Ficsonium", "Bundle: Ficsonium Fuel Rod"],
        "All Arachnids All the Time": ["Trap: Small Stinger", "Trap: Stinger", "Trap: Gas Stinger"],
        "Whole Hog": ["Trap: Hog", "Trap: Alpha Hog", "Trap: Cliff Hog", "Trap: Nuclear Hog", "Trap: Johnny"],
        "Nicholas Cage": ["Trap: Hatcher", "Trap: Elite Hatcher", "Trap: Not the Bees"],
        "Fallout": ["Trap: Doggo with Nuke Nobelisk", "Trap: Nuclear Hog", "Trap: Nuclear Waste Drop", "Trap: Plutonium Waste Drop", "Bundle: Uranium", "Bundle: Uranium Fuel Rod", "Bundle: Uranium Waste", "Bundle: Plutonium Fuel Rod", "Bundle: Plutonium Waste", "Bundle: Ficsonium", "Bundle: Ficsonium Fuel Rod"],
    }
    # default="Normal" # TODO `default` doesn't do anything, default is always the first `choices` value. if uncommented it messes up the template file generation (caps mismatch)

class TrapSelectionOverride(OptionSet):
    """
    Precise list of traps that may be in the item pool to find.
    If you select anything with this option it will be used instead of the *Trap Presets* setting.
    """
    display_name = "Trap Override"
    valid_keys = _trap_types
    default = {}

class EnergyLink(Toggle):
    """
    Allow transferring energy to and from other worlds using the Power Storage building.
    No energy is lost in the transfer on Satisfactory's side, but other worlds may have other settings.
    """
    display_name = "EnergyLink"

class MamLogic(PlacementLogic):
    """
    Where to place the MAM building in logic.
    Earlier means it will be more likely you need to interact with it for progression purposes.
    """
    display_name = "MAM Placement"
    default = Placement.early

class AwesomeLogic(PlacementLogic):
    """
    Where to place the AWESOME Shop and Sink buildings in logic.
    Earlier means it will be more likely you need to interact with it for progression purposes.
    """
    display_name = "AWESOME Stuff Placement"
    default = Placement.early

class EnergyLinkLogic(PlacementLogic):
    """
    Where to place the EnergyLink building (or Power Storage if EnergyLink is disabled) in logic.
    Earlier means it will be more likely to get access to it early into your game.
    """
    display_name = "EnergyLink Placement"
    default = Placement.early

class SplitterLogic(PlacementLogic):
    """
    Where to place the Conveyor Splitter and Merger buildings in logic.
    Earlier means it will be more likely to get access to it early into your game.
    """
    display_name = "Splitter and Merger Placement"
    default = Placement.starting_inventory

_skip_tutorial_starting_items = [
    # https://satisfactory.wiki.gg/wiki/Onboarding
    "Bundle: Portable Miner",
    "Bundle: Iron Plate",
    "Bundle: Concrete",
    "Bundle: Iron Rod",
    "Bundle: Wire",
    "Bundle: Reinforced Iron Plate",
    "Bundle: Cable"
]

_default_starting_items = _skip_tutorial_starting_items + [
    "Bundle: Iron Ingot",
    "Bundle: Copper Ingot",
    "Bundle: Concrete",
    "Building: Blueprint Designer",
    "Expanded Toolbelt",
    "Inflated Pocket Dimension",
    "Building: Personal Storage Box"
]

_default_plus_foundations_starting_items = _default_starting_items + [
    "Building: Foundation",
    "Building: Half Foundation"
]

_foundation_lover_starting_items = _default_plus_foundations_starting_items + [
    "Bundle: Iron Plate", "Bundle: Iron Plate", "Bundle: Iron Plate",
    "Bundle: Concrete", "Bundle: Concrete", "Bundle: Concrete"
]

class StartingInventoryPreset(ChoiceMap):
    """
    What resources (and buildings) the player should start with in their inventory.
    If you want more control, visit the Weighted Options page or edit the YAML directly.

    - **Barebones**: Nothing but the default xeno zapper and buildings.
    - **Skip Tutorial Inspired**: Inspired by the items you would have if you skipped the base game's tutorial.
    - **Archipelago**: The starting items we think will lead to a fun experience.
    - **Foundations**: 'Archipelago' option, but also guaranteeing that you have foundations unlocked at the start.
    - **Foundation Lover**: You really like foundations.
    """
    display_name = "Starting Goodies Presets"
    choices = {
        "Archipelago": _default_starting_items,
        "Barebones": [], # Nothing but the xeno zapper
        "Skip Tutorial Inspired": _skip_tutorial_starting_items,
        "Foundations": _default_plus_foundations_starting_items,
        "Foundation Lover": _foundation_lover_starting_items
    }
    # default = "Archipelago" # TODO `default` doesn't do anything, default is always the first `choices` value. if uncommented it messes up the template file generation (caps mismatch)

class GoalSelection(OptionSet):
    """
    What will be your goal(s)?
    Configure them further with other options.
    """
    display_name = "Select your Goals"
    valid_keys = {
        "Space Elevator Tier",
        "AWESOME Sink Points",
        # "Exploration",
        # "FICSMAS Tree",
    }
    default = {"Space Elevator Tier"}

class GoalRequirement(Choice):
    """
    Of the goals selected in *Select your Goals*, how many must be reached to complete your slot?
    """
    display_name = "Goal Requirements"
    option_require_any_one_goal = 0
    option_require_all_goals = 1
    default = 0

class ExperimentalGeneration(Toggle):
    """
    Attempts to only mark recipes as progression if they are on your path to victory.
    WARNING: has a very high change of generation failure and should therefore only be used in single player games.
    """
    display_name = "Experimental Generation"
    visibility = Visibility.none

@dataclass
class SatisfactoryOptions(PerGameCommonOptions):
    goal_selection: GoalSelection
    goal_requirement: GoalRequirement
    final_elevator_package: ElevatorTier
    final_awesome_sink_points: ResourceSinkPoints
    hard_drive_progression_limit: HardDriveProgressionLimit
    free_sample_equipment: FreeSampleEquipment
    free_sample_buildings: FreeSampleBuildings
    free_sample_parts: FreeSampleParts
    free_sample_radioactive: FreeSampleRadioactive
    starting_inventory_preset: StartingInventoryPreset
    mam_logic_placement: MamLogic
    awesome_logic_placement: AwesomeLogic
    energy_link_logic_placement: EnergyLinkLogic
    splitter_placement: SplitterLogic
    trap_chance: TrapChance
    trap_selection_preset: TrapSelectionPreset
    trap_selection_override: TrapSelectionOverride
    death_link: DeathLink
    energy_link: EnergyLink
    start_inventory_from_pool: StartInventoryPool
    experimental_generation: ExperimentalGeneration
