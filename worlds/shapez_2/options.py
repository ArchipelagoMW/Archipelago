import random
import typing
from dataclasses import dataclass

from BaseClasses import PlandoOptions
from Options import Choice, PerGameCommonOptions, OptionSet, OptionError, OptionCounter, StartInventoryPool

if typing.TYPE_CHECKING:
    from worlds.AutoWorld import World
    from . import Shapez2World


class CasefoldOptionSet(OptionSet):
    valid_keys_casefold = True

    def __init__(self, value: typing.Iterable[str]):
        self.value: set[str] = set(val.casefold() for val in value)
        super(OptionSet, self).__init__()

    def __contains__(self, item: str):
        return item.casefold() in self.value

    def verify_keys(self) -> None:
        if self.valid_keys:
            dataset = set(word.casefold() for word in self.value)
            extra = dataset - set(key.casefold() for key in self._valid_keys)
            if extra:
                raise OptionError(
                    f"Found unexpected key {', '.join(extra)} in {getattr(self, 'display_name', self)}. "
                    f"Allowed keys: {self._valid_keys}."
                )


class ExtendedOptionCounter(OptionCounter):
    value: dict[str, int]
    individual_min_max: dict[str, tuple[int, int]] = {}
    min_max_pairs: list[tuple[str, str]] = []

    @classmethod
    def from_any(cls, data: typing.Dict[str, typing.Any]):
        data = data.copy()
        if not isinstance(data, dict):
            raise NotImplementedError(f"Cannot Convert from non-dictionary, got {type(data)}")
        for key in cls.valid_keys:
            if key not in data:
                if key in cls.default:
                    data[key] = cls.default[key]
                else:
                    data[key] = 0
            data[key] = cls.resolve_value(data[key], key)
        return cls(data)

    def verify(self, world: type["World"], player_name: str, plando_options: PlandoOptions) -> None:
        super().verify(world, player_name, plando_options)

        errors = []

        for key in self.value:
            if key in self.individual_min_max:
                _min, _max = self.individual_min_max[key]
                if not _min <= self.value[key] <= _max:
                    errors.append(f"{key}: {self.value[key]} not in range {_min} to {_max}")

        for min_key, max_key in self.min_max_pairs:
            if min_key in self.value and max_key in self.value:
                if self.value[min_key] > self.value[max_key]:
                    errors.append(f"{min_key} is higher than {max_key}")

        if len(errors) != 0:
            errors = [f"For option {getattr(self, 'display_name', self)} of player {player_name}:"] + errors
            raise OptionError("\n".join(errors))

    @classmethod
    def resolve_value(cls, val: int | dict[typing.Any, int] | list | str, key: str) -> int:
        if isinstance(val, int):
            return val
        elif isinstance(val, list):
            return cls.resolve_value(random.choice(val), key)
        elif isinstance(val, dict):
            return cls.resolve_value(random.choices(list(val.keys()), list(val.values())), key)
        elif isinstance(val, str) and val.startswith("random"):
            if val == "random":
                return random.randint(*(cls.individual_min_max[key]))
            elif val.startswith("random-range-"):
                parts = val.split("-")
                if parts[-2].isnumeric() and parts[-1].isnumeric():
                    start = int(parts[-2])
                    end = int(parts[-1])
                    _min, _max = cls.individual_min_max[key]
                    if _min <= start <= _max and _min <= end <= _max and start <= end:
                        return random.randint(start, end)
        raise OptionError(
            f"Invalid value \"{val}\" for key \"{key}\" in option \"{getattr(cls, 'display_name', cls)}\"."
        )

    def __getitem__(self, item: str) -> int:
        return super().__getitem__(item)


class Goal(Choice):
    """
    Select your goal.

    - **Milestones** - Complete all milestones.
    - **Operator levels** - Reach the operator level that contains your last operator level check. Requires an operator level checks number higher than 0.
    """
    display_name = "Goal"
    option_milestones = 0
    option_operator_levels = 1
    default = 0


class LocationModifiers(CasefoldOptionSet):
    """
    Modifies Various aspects about location generation. You can add as many modifiers as you want.

    - **Lock task lines** - Makes task lines require an item to be unlocked. Task lines #1-3 are always unlocked.
    - **Lock operator lines** - Makes operator lines require an item to be unlocked.
    - **Lock operator levels tab** - Makes the operator levels tab require an item to be unlocked.
    """
    # - **Add sandbox buildings** - Adds the sandbox item and fluid producers to the itempool.
    display_name = "Location Modifiers"
    valid_keys = [
        "Lock task lines",
        "Lock operator lines",
        "Lock operator levels tab",
    ]
    default = ["Lock operator lines"]


class LocationAdjustments(ExtendedOptionCounter):
    """
    Adjust various parameters of milestones, task lines, operator lines, etc.
    Any minimum parameter cannot be higher than its corresponding maximum parameter.
    Weighting for each parameter individually, "random", and "random-range-x-y" are supported.

    Most names are self-explanatory. However, do note that...
    - **Random operator lines** means "X out of all operator lines are random".
    - **Required shapes multiplier** is in percent, i.e. 100 is default amount of shapes.
    Also, default amounts are based on the (vanilla) regular scenario.

    Do note that you have to add enough (minimum) locations to fit all non-filler items
    (filler items are research/platform/blueprint points).
    Excluding task line and operator line keys, there are ~70 items.

    Allowed values (in range) are...
    - **Milestones** - 3-20
    - **Minimum checks per milestone** - 2-12
    - **Maximum checks per milestone** - 5-12
    - **Starting platform points** - 250-2000
    - **Starting research points** - 0-50
    - **Starting blueprint points** - 0-10000
    - **Task lines** - 3-200
    - **Minimum checks per task line** - 1-5
    - **Maximum checks per task line** - 1-5
    - **Operator lines** - 1-100
    - **Random operator lines** - 0-3
    - **Operator level checks** - 0-200
    - **Required shapes multiplier** - 1-1000
    """
    display_name = "Location Adjustments"
    valid_keys = [
        "Milestones",
        "Minimum checks per milestone",
        "Maximum checks per milestone",
        "Starting platform points",
        "Starting research points",
        "Starting blueprint points",
        "Task lines",
        "Minimum checks per task line",
        "Maximum checks per task line",
        "Operator lines",
        "Random operator lines",
        "Operator level checks",
        "Required shapes multiplier",
    ]
    default = {
        "Milestones": 8,
        "Minimum checks per milestone": 8,
        "Maximum checks per milestone": 12,
        "Starting platform points": 250,
        "Starting research points": 0,
        "Starting blueprint points": 0,
        "Task lines": 20,
        "Minimum checks per task line": 3,
        "Maximum checks per task line": 5,
        "Operator lines": 8,
        "Random operator lines": 2,
        "Operator level checks": 0,
        "Required shapes multiplier": 100,
    }
    individual_min_max = {
        "Milestones": (3, 20),
        "Minimum checks per milestone": (2, 12),
        "Maximum checks per milestone": (5, 12),
        "Starting platform points": (250, 2000),
        "Starting research points": (0, 50),
        "Starting blueprint points": (0, 10000),
        "Task lines": (3, 200),
        "Minimum checks per task line": (1, 5),
        "Maximum checks per task line": (1, 5),
        "Operator lines": (1, 100),
        "Random operator lines": (0, 3),
        "Operator level checks": (0, 200),
        "Required shapes multiplier": (1, 1000),
    }
    min_max_pairs = [
        ("Minimum checks per milestone", "Maximum checks per milestone"),
        ("Minimum checks per task line", "Maximum checks per task line"),
        ("Random operator lines", "Operator lines"),
    ]

    def count_min_locations(self) -> int:
        return (self["Milestones"] * self["Minimum checks per milestone"] +
                self["Task lines"] * self["Minimum checks per task line"] + self["Operator level checks"])


class ShapeConfiguration(Choice):
    """
    Choose how many corners all shapes have.

    - **Tetragonal** - 4 corners (standard).
    - **Hexagonal** (not implemented) - 6 corners.
    """
    display_name = "Shape Configuration"
    option_tetragonal = 4
    # option_hexagonal = 6
    default = 4


class ShapeGenerationModifiers(CasefoldOptionSet):
    """
    Modifies what shapes are generated as requirements for milestones, tasks, and operator levels.
    You can add as many modifiers as you want.

    - **Milestone operator lines** - Takes the final shapes of (some) milestones and reuses them as operator lines.
    """
    display_name = "Shape Generation Modifiers"
    valid_keys = [
        "Milestone operator lines",
    ]
    default = ["Milestone operator lines"]


class ShapeGenerationAdjustments(ExtendedOptionCounter):
    """
    Adjust various parameters about how shape requirements for milestones, tasks, and operator levels are generated.
    Weighting for each parameter individually, "random", and "random-range-x-y" are supported.

    - **Maximum layers** - The maximum number of layers any shape can have.
    - **Maximum processors per milestone** - The maximum number of certain buildings that are required to produce the final shapes of milestones.
    """
    display_name = "Shape Generation Adjustments"
    valid_keys = [
        "Maximum layers",
        "Maximum processors per milestone",
    ]
    default = {
        "Maximum layers": 4,
        "Maximum processors per milestone": 4,
    }
    individual_min_max = {
        "Maximum layers": (2, 10),
        "Maximum processors per milestone": (3, 8),
    }


class BlueprintShapes(Choice):
    """
    Choose which set of shapes rewards the player with blueprint points.

    If tetragonal shapes are chosen, **Regular**, **Hard**, and **Insane** use the corresponding scenario's set.
    If hexagonal shapes are chosen, all of those three options use the hexagonal scenario's set.
    **Randomized** generates a random set of 3 to 5 different blueprint shapes.

    You can also put in a list of custom blueprint shapes. See this game's option guides for more information.
    """
    display_name = "Blueprint Shapes"
    option_regular = 0
    option_hard = 1
    option_insane = 2
    option_randomized = 3
    default = 0

    def __init__(self, value: int, plando: list[str] | None = None):
        if "plando" not in self.options:
            self.options["plando"] = 99
        if "plando" not in self.name_lookup:
            self.name_lookup[99] = "plando"
        super().__init__(value)
        self.plando = plando

    def is_plando(self) -> bool:
        return self.plando is not None

    @classmethod
    def from_any(cls, data: typing.Any) -> typing.Self:
        if isinstance(data, list):
            return cls(99, data)
        return super().from_any(data)

    def verify(self, world: typing.Type["World"], player_name: str, plando_options: PlandoOptions) -> None:
        super().verify(world, player_name, plando_options)
        if self.is_plando():
            reasons: list[str] = []
            for val in self.plando:
                if not isinstance(val, str):
                    reasons.append(f"Shapes list must only contain strings, but found {type(val)}")
            if not (0 < len(self.plando) <= 5):
                reasons.append(f"Number of blueprint shapes must be in range 1-5, but found {len(self.plando)}")
            if reasons:
                raise OptionError(f"Player {player_name}: Bad plando formatting for blueprint_shapes option:\n" + ", ".join(reasons))

    def verify_plando(self, world: "Shapez2World"):
        if self.is_plando():
            from .generate.shapes.verify import is_valid_shape
            parts = 4 if world.options.shape_configuration == "tetragonal" else 6
            layers = world.options.shape_generation_adjustments["Maximum layers"]
            if any(not is_valid_shape(shape, parts, layers) for shape in self.plando):
                raise OptionError(f"Player {world.player_name}: Invalid plando shapes in option blueprint_shapes.\n"
                                  f"See this option's plando guide for more information.")

    def to_slot_data(self) -> str | list[str]:
        if self.is_plando():
            return self.plando
        else:
            return self.current_key


class ItemPoolModifiers(CasefoldOptionSet):
    """
    Modifies what items your world puts into the item pool. You can add as many modifiers as you want.

    - **Random starting processor** - Adds a random processor building that doesn't require other buildings to the starting milestone.
    - **Include blueprint points** - Allows blueprint points to be added as filler items. If blueprint costs are disabled ingame, blueprint point rewards will be invisible ingame.
    - **Arbitrary research points** - Allows research points items to give any amount in range of 1-100 instead of snapping them to nice numbers.
    - **Arbitrary platform items** - Allows platform items to give any amount in range of 1-500 instead of snapping them to nice numbers.
    - **Arbitrary blueprint points** - Allows blueprint points to give amounts in range of 1000-10000 snapped to 100-step numbers instead of 1000-step numbers.
    - **Unlock extensions with miners** - Makes shape and fluid miners also unlock their extensions with them.
    """
    # - **Add sandbox buildings** - Adds the sandbox item and fluid producers to the itempool.
    display_name = "Item Pool Modifiers"
    valid_keys = [
        # "Add sandbox buildings",
        "Random starting processor",
        "Include blueprint points",
        "Arbitrary research points",
        "Arbitrary platform items",
        "Arbitrary blueprint points",
        "Unlock extensions with miners",
    ]
    default = ["Random starting processor", "Unlock extensions with miners"]


class ShowOtherPlayersItems(Choice):
    """
    Shows the names of items in-game that do not belong to your own world.

    - **No** - Labels all of those items as "AP Item".
    - **Item** - Shows the name of each of those items.
    - **Player** - Additionally appends the player's name to the item's name.
    - **Classification** - Additionally appends the item's classification (progression, filler, ...) to its name.
    - **Item** - Appends bot the player's name and the classification to the item's name.
    """
    display_name = "Show other players' items"
    option_no = 0
    option_item = 1
    option_player = 2
    option_classification = 3
    option_player_classification = 4
    default = 1


@dataclass
class Shapez2Options(PerGameCommonOptions):
    goal: Goal
    location_modifiers: LocationModifiers
    location_adjustments: LocationAdjustments
    shape_configuration: ShapeConfiguration
    shape_generation_modifiers: ShapeGenerationModifiers
    shape_generation_adjustments: ShapeGenerationAdjustments
    blueprint_shapes: BlueprintShapes
    item_pool_modifiers: ItemPoolModifiers
    show_other_players_items: ShowOtherPlayersItems
    start_inventory_from_pool: StartInventoryPool
