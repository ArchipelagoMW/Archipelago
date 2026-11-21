from dataclasses import dataclass
from typing import ClassVar, Any, cast
from enum import IntEnum
from schema import Schema, And
from Options import PerGameCommonOptions, DeathLinkMixin, AssembleOptions, OptionGroup
from Options import Range, NamedRange, Toggle, DefaultOnToggle, OptionSet, StartInventoryPool, Choice


class Placement(IntEnum):
    starting_inventory = 0
    early = 1
    somewhere = 2


class PlacementLogicMeta(AssembleOptions):
    def __new__(mcs, name: str, bases: tuple[type], attrs: dict[Any, Any]) -> "PlacementLogicMeta":
        if "default" in attrs and isinstance(attrs["default"], Placement):
            attrs["default"] = int(attrs["default"])

        cls = super(PlacementLogicMeta, mcs).__new__(mcs, name, bases, attrs)
        return cast(PlacementLogicMeta, cls)


class PlacementLogic(Choice, metaclass=PlacementLogicMeta):
    option_unlocked_from_start = Placement.starting_inventory.value
    option_early_game = Placement.early.value
    option_somewhere = Placement.somewhere.value


class ChoiceMapMeta(AssembleOptions):
    def __new__(mcs, name: str, bases: tuple[type], attrs: dict[Any, Any]) -> "ChoiceMapMeta":
        if "choices" in attrs:
            for index, choice in enumerate(attrs["choices"]):
                option_name = "option_" + choice.replace(' ', '_')
                attrs[option_name] = index

                if "default" in attrs and attrs["default"] == choice:
                    attrs["default"] = index

        cls = super(ChoiceMapMeta, mcs).__new__(mcs, name, bases, attrs)
        return cast(ChoiceMapMeta, cls)


class ChoiceMap(Choice, metaclass=ChoiceMapMeta):
    choices: ClassVar[dict[str, list[str]]]
    default: str

    def get_selected_list(self) -> list[str]:
        for index, choice in enumerate(self.choices):
            if index == self.value:
                return self.choices[choice]
            
        raise Exception(f"ChoiceMap: selected choice {self.value} is not valid, valid choices are: {self.choices.keys()}")


class ElevatorPhase(NamedRange):
    """
    Put the milestones accessible BEFORE this Space Elevator Phase in logic.
    Milestones after the selected Phase are empty and contain nothing.
    If your goal selection contains *Space Elevator Phase* then submitting this Phase's elevator package completes that goal.
    If the goal is not enabled, this setting simply limits the included HUB and MAM content.
    
    Estimated in-game completion times:

    - **Phase 1 (Tiers 1-2)**: ~3 Hours
    - **Phase 2 (Tiers 1-4)**: ~8 Hours
    - **Phase 3 (Tiers 1-6)**: ~50 Hours
    - **Phase 4 (Tiers 1-8)**: ~100 Hours
    - **Phase 5 (Tiers 1-9)**: ~140 Hours
    """
    display_name = "Final Space Elevator Phase in logic"
    default = 2
    range_start = 1
    range_end = 5
    special_range_names = {
        "phase 1 (tiers 1-2)": 1,
        "phase 2 (tiers 1-4)": 2,
        "phase 3 (tiers 1-6)": 3,
        "phase 4 (tiers 1-8)": 4,
        "phase 5 (tiers 1-9)": 5,
    }


class ResourceSinkPointsTotal(NamedRange):
    """
    Does nothing if *AWESOME Sink Points (total)* goal is not enabled.

    Sink an amount of items totalling this amount of points to finish.
    This setting is a *point count*, not a *coupon* count!

    In the base game, it takes 347 coupons to unlock every non-repeatable purchase, or 1895 coupons to purchase every non-producible item.

    Use the **TFIT - Ficsit Information Tool** mod or the Satisfactory wiki to find out how many points items are worth.

    If you have *Free Samples* enabled, consider setting this higher so that you can't reach the goal just by sinking your Free Samples.
    """
    # Coupon data for above comment from https://satisfactory.wiki.gg/wiki/AWESOME_Shop
    display_name = "AWESOME Sink points total"
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


class ResourceSinkPointsPerMinute(NamedRange):
    """
    Does nothing if *AWESOME Sink Points (per minute)* goal is not enabled.

    Sink items to maintain a sink points per minute of the chosen amount for 10 minutes to finish.
    This setting is in *points per minute* on the orange track, so DNA Capsules don't count.
    This option's presets are example production thresholds - you don't have to sink exactly those specific items.

    Use the **TFIT - Ficsit Information Tool** mod or the Satisfactory wiki to find out how many points items are worth.
    """
    display_name = "AWESOME Sink points per minute"
    default = 50000
    range_start = 1000
    range_end = 10000000
    special_range_names = {
        "~500 screw/min": 1000,
        "~100 reinforced iron plate/min": 12000,
        "~100 stator/min": 24000,
        "~100 modular frame/min": 40000,
        "~100 smart plating/min": 50000,
        "~20 crystal oscillator/min": 60000,
        "~50 motor/min": 76000,
        "~10 heavy modular frame/min": 100000,
        "~10 radio control unit/min": 300000,
        "~10 fused modular frame/min": 625000,
        "~10 supercomputer/min": 1000000,
        "~10 pressure conversion cube/min": 2500000,
        "~10 nuclear pasta/min": 5000000,
        "~4 ballistic warp drive/min": 10000000,
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
    How many free sample Equipment items are given when they are unlocked.
    
    (ex. Jetpack, Rifle)
    """
    display_name = "Free Samples: Equipment"
    default = 1
    range_start = 0
    range_end = 10


class FreeSampleBuildings(Range):
    """
    How many copies of a Building's construction cost are given as a free sample when they are unlocked.
    Space Elevator is always excluded.
    
    (ex. Packager, Constructor, Smelter)
    """
    display_name = "Free Samples: Buildings"
    default = 5
    range_start = 0
    range_end = 10


class FreeSampleParts(NamedRange):
    """
    How many general crafting component free samples are given when their recipe is unlocked.
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
        "Gentle": ["Trap: Doggo with Pulse Nobelisk", "Trap: Hog", "Trap: Spitter", "Trap: Can of Beans"],
        "Normal": ["Trap: Doggo with Pulse Nobelisk", "Trap: Doggo with Gas Nobelisk", "Trap: Hog", "Trap: Alpha Hog", "Trap: Hatcher", "Trap: Elite Hatcher", "Trap: Small Stinger", "Trap: Stinger", "Trap: Spitter", "Trap: Alpha Spitter", "Trap: Not the Bees", "Trap: Nuclear Waste Drop", "Bundle: Uranium", "Bundle: Non-fissile Uranium", "Trap: Can of Beans", "Trap: Fart Cloud"],
        "Harder": ["Trap: Doggo with Pulse Nobelisk", "Trap: Doggo with Nuke Nobelisk", "Trap: Doggo with Gas Nobelisk", "Trap: Alpha Hog", "Trap: Cliff Hog", "Trap: Spore Flower", "Trap: Hatcher", "Trap: Elite Hatcher", "Trap: Stinger", "Trap: Alpha Spitter", "Trap: Not the Bees", "Trap: Fart Cloud", "Trap: Nuclear Waste Drop", "Trap: Plutonium Waste Drop", "Bundle: Uranium", "Bundle: Uranium Fuel Rod", "Bundle: Uranium Waste", "Bundle: Plutonium Fuel Rod", "Bundle: Plutonium Pellet", "Bundle: Plutonium Waste", "Bundle: Non-fissile Uranium"],
        "All": list(_trap_types),
        "Ruthless": ["Trap: Doggo with Nuke Nobelisk", "Trap: Nuclear Hog", "Trap: Cliff Hog", "Trap: Elite Hatcher", "Trap: Spore Flower", "Trap: Gas Stinger", "Trap: Nuclear Waste Drop", "Trap: Plutonium Waste Drop", "Bundle: Uranium Fuel Rod", "Bundle: Uranium Waste", "Bundle: Plutonium Fuel Rod", "Bundle: Plutonium Pellet", "Bundle: Plutonium Waste", "Bundle: Non-fissile Uranium", "Bundle: Ficsonium", "Bundle: Ficsonium Fuel Rod"],
        "All Arachnids All the Time": ["Trap: Small Stinger", "Trap: Stinger", "Trap: Gas Stinger"],
        "Whole Hog": ["Trap: Hog", "Trap: Alpha Hog", "Trap: Cliff Hog", "Trap: Nuclear Hog", "Trap: Johnny"],
        "Nicholas Cage": ["Trap: Hatcher", "Trap: Elite Hatcher", "Trap: Not the Bees"],
        "Fallout": ["Trap: Doggo with Nuke Nobelisk", "Trap: Nuclear Hog", "Trap: Nuclear Waste Drop", "Trap: Plutonium Waste Drop", "Bundle: Uranium", "Bundle: Uranium Fuel Rod", "Bundle: Uranium Waste", "Bundle: Plutonium Fuel Rod", "Bundle: Plutonium Waste", "Bundle: Ficsonium", "Bundle: Ficsonium Fuel Rod"],
    }
    default = "Normal"


class TrapSelectionOverride(OptionSet):
    """
    Precise list of traps that may be in the item pool to find.
    If you select anything with this option it will be used instead of the *Trap Presets* setting.
    """
    display_name = "Trap Override"
    valid_keys = _trap_types


class EnergyLink(DefaultOnToggle):
    """
    Allow transferring energy to and from other worlds using the Power Storage building.
    Some energy is lost when depositing it in the multiworld network.
    """
    display_name = "EnergyLink"


class MamLogic(PlacementLogic):
    """
    Where to place the MAM building in logic.
    Earlier means it will be more likely that you will need to interact with it for progression purposes.
    """
    display_name = "MAM Placement"
    default = Placement.early.value


class AwesomeLogic(PlacementLogic):
    """
    Where to place the AWESOME Shop and Sink buildings in logic.
    Earlier means it will be more likely that you will need to interact with it for progression purposes.
    """
    display_name = "AWESOME Stuff Placement"
    default = Placement.early.value


class EnergyLinkLogic(PlacementLogic):
    """
    Where to place the EnergyLink building (or Power Storage if EnergyLink is disabled) in logic.
    Earlier means it will be more likely that you will need to interact with it for progression purposes.
    """
    display_name = "EnergyLink Placement"
    default = Placement.early.value


class SplitterLogic(PlacementLogic):
    """
    Where to place the Conveyor Splitter and Merger buildings in logic.
    Earlier means it will be more likely that you will need to interact with it for progression purposes.
    """
    display_name = "Splitter and Merger Placement"
    default = Placement.starting_inventory.value


_skip_tutorial_starting_items = [
    # https://satisfactory.wiki.gg/wiki/Onboarding
    "Single: Portable Miner",
    "Single: Portable Miner",
    "Single: Portable Miner",
    "Single: Portable Miner",
    "Bundle: Iron Plate",
    "Bundle: Concrete",
    "Bundle: Iron Rod",
    "Bundle: Wire",
    "Single: Reinforced Iron Plate",
    "Single: Reinforced Iron Plate",
    "Single: Reinforced Iron Plate",
    "Single: Reinforced Iron Plate",
    "Single: Reinforced Iron Plate",
    "Single: Reinforced Iron Plate",
    "Single: Reinforced Iron Plate",
    "Single: Reinforced Iron Plate",
    "Single: Reinforced Iron Plate",
    "Single: Reinforced Iron Plate",
    "Bundle: Cable",
    "Bundle: Iron Ore"
]

_default_starting_items = _skip_tutorial_starting_items + [
    "Bundle: Iron Ingot",
    "Bundle: Copper Ingot",
    "Bundle: Concrete",
    "Bundle: Solid Biofuel",  # user's choice if they want to hold onto it for chainsaw or burn it right away
    "Building: Blueprint Designer",
    "Expanded Toolbelt",
    "Inflated Pocket Dimension",
    "Building: Personal Storage Box"
]

_default_plus_foundations_starting_items = _default_starting_items + [
    "Building: Foundation",
    "Building: Half Foundation"
]

_explorer_starting_items = _default_plus_foundations_starting_items + [
    "Single: Parachute",
    "Single: Blade Runners",
    "Single: Object Scanner",
    "Single: Boom Box",
    "Expanded Toolbelt",
    "Inflated Pocket Dimension"
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
    - **Explorer**: 'Foundations' option plus one set of early exploration equipment (Parachute, Blade Runners, Object Scanner, Boom Box).
    """
    display_name = "Starting Goodies Presets"
    choices = {
        "Barebones": [],  # Nothing but the xeno zapper
        "Skip Tutorial Inspired": _skip_tutorial_starting_items,
        "Archipelago": _default_starting_items,
        "Foundations": _default_plus_foundations_starting_items,
        "Foundation Lover": _foundation_lover_starting_items,
        "Explorer": _explorer_starting_items
    }
    default = "Archipelago"


class ExplorationCollectableCount(Range):
    """
    Does nothing if *Exploration Collectables* goal is not enabled.

    Collect this amount of Mercer Spheres, Somersloops, Hard Drives, Paleberries, Beryl Nuts, and Bacon Agarics each to finish.

    - The amount of **Mercer Spheres** is **2x** the selected amount
    - The amount of **Somersloops** is **1x** the selected amount
    - The amount of **Hard Drives** is **1/5th** the selected amount
    - The amount of **Paleberries** is **10x** the selected amount
    - The amount of **Beryl Nuts** is **20x** the selected amount
    - The amount of **Bacon Agarics** is **1x** the selected amount
    """
    display_name = "Exploration Collectables"
    default = 20
    range_start = 5
    range_end = 100


class MilestoneCostMultiplier(Range):
    """
    Multiplies the amount of resources needed to unlock a Milestone by this factor.

    The value is a percentage:

    - **50** = half cost
    - **100** = normal milestone cost
    - **200** = double the cost
    """
    display_name = "Milestone cost multiplier %"
    default = 100
    range_start = 1
    range_end = 500


class GoalSelection(OptionSet):
    """
    What will be your goal(s)?
    Configure them further with other options.

    Possible values are:
    - **Space Elevator Phase**
    - **AWESOME Sink Points (total)**
    - **AWESOME Sink Points (per minute)**
    - **Exploration Collectables**
    - **Erect a FICSMAS Tree**
    """
    display_name = "Select your Goals"
    valid_keys = {
        "Space Elevator Phase",
        "AWESOME Sink Points (total)",
        "AWESOME Sink Points (per minute)",
        "Exploration Collectables",
        "Erect a FICSMAS Tree",
    }
    default = {"Space Elevator Phase"}
    schema = Schema(And(set, len),
                    error="yaml does not specify a goal, the Satisfactory option `goal_selection` is empty")


class GoalRequirement(Choice):
    """
    Of the goals selected in *Select your Goals*, how many must be reached to complete your slot?
    """
    display_name = "Goal Requirements"
    option_require_any_one_goal = 0
    option_require_all_goals = 1
    default = 0


class RandomizeTier0(DefaultOnToggle):
    """
    Randomizes what recipes you use to craft the default unlocked parts:
    Iron Ingot, Iron Plate, Iron Rod, Copper Ingot, Wire, Concrete, Screw, Reinforced Iron Plate

    - Could require usage of Foundries or Assemblers (which get unlocked by default if needed, at reduced build costs)
    - Could require other ores to be mixed in via alt recipes (which will become hand-craftable if needed)
    """
    display_name = "Randomize Default Part Recipes"


@dataclass
class SatisfactoryOptions(PerGameCommonOptions, DeathLinkMixin):
    goal_selection: GoalSelection
    goal_requirement: GoalRequirement
    final_elevator_phase: ElevatorPhase
    goal_awesome_sink_points_total: ResourceSinkPointsTotal
    goal_awesome_sink_points_per_minute: ResourceSinkPointsPerMinute
    goal_exploration_collectables_amount: ExplorationCollectableCount
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
    milestone_cost_multiplier: MilestoneCostMultiplier
    trap_chance: TrapChance
    trap_selection_preset: TrapSelectionPreset
    trap_selection_override: TrapSelectionOverride
    energy_link: EnergyLink
    start_inventory_from_pool: StartInventoryPool
    randomize_starter_recipes: RandomizeTier0


option_groups = [
    OptionGroup("Game Scope", [
        ElevatorPhase,
        HardDriveProgressionLimit
    ]),
    OptionGroup("Goal Selection", [
        GoalSelection,
        GoalRequirement,
        ResourceSinkPointsTotal,
        ResourceSinkPointsPerMinute,
        ExplorationCollectableCount
    ]),
    OptionGroup("Placement logic", [
        StartingInventoryPreset,
        RandomizeTier0,
        MamLogic,
        AwesomeLogic,
        SplitterLogic,
        EnergyLinkLogic
    ], start_collapsed=True),
    OptionGroup("Free Samples", [
        FreeSampleEquipment,
        FreeSampleBuildings,
        FreeSampleParts,
        FreeSampleRadioactive
    ], start_collapsed=True),
    OptionGroup("Traps", [
        TrapChance,
        TrapSelectionPreset,
        TrapSelectionOverride
    ], start_collapsed=True)
]

option_presets: dict[str, dict[str, Any]] = {
    "Short": {
        "final_elevator_phase": 1,
        "goal_selection": {"Space Elevator Phase", "AWESOME Sink Points (total)"},
        "goal_requirement": GoalRequirement.option_require_any_one_goal,
        "goal_awesome_sink_points_total": 17804500,  # 100 coupons
        "hard_drive_progression_limit": 20,
        "starting_inventory_preset": 3,  # "Foundations"
        "randomize_starter_recipes": False,
        "mam_logic_placement": Placement.starting_inventory.value,
        "awesome_logic_placement": Placement.starting_inventory.value,
        "energy_link_logic_placement": Placement.starting_inventory.value,
        "splitter_placement": Placement.starting_inventory.value,
        "milestone_cost_multiplier": 50,
        "trap_selection_preset": 1  # Gentle
    },
    "Long": {
        "final_elevator_phase": 3,
        "goal_selection": {"Space Elevator Phase", "AWESOME Sink Points (per minute)"},
        "goal_requirement": GoalRequirement.option_require_all_goals,
        "goal_awesome_sink_points_per_minute": 100000,  # ~10 heavy modular frame/min
        "hard_drive_progression_limit": 60,
        "mam_logic_placement": Placement.somewhere.value,
        "awesome_logic_placement": Placement.somewhere.value,
        "energy_link_logic_placement": Placement.somewhere.value,
        "splitter_placement": Placement.somewhere.value,
        "trap_selection_preset": 3  # Harder
    },
    "Extra Long": {
        "final_elevator_phase": 5,
        "goal_selection": {"Space Elevator Phase", "AWESOME Sink Points (per minute)"},
        "goal_requirement": GoalRequirement.option_require_all_goals,
        "goal_awesome_sink_points_per_minute": 625000,  # ~10 fused modular frame/min
        "hard_drive_progression_limit": 100,
        "mam_logic_placement": Placement.somewhere.value,
        "awesome_logic_placement": Placement.somewhere.value,
        "energy_link_logic_placement": Placement.somewhere.value,
        "splitter_placement": Placement.somewhere.value,
        "milestone_cost_multiplier": 300,
        "trap_selection_preset": 4  # All
    }
} 
