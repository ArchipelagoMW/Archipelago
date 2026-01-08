from copy import deepcopy
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Literal, Mapping, Optional, Union, cast

from .area_rando_types import AreaDoor, DoorPairs
from .daphne_gate_types import DaphneBlocks
from .door_logic import vanilla_doors
from .goals import Event, Goals
from .hint_types import Hint, from_jsonable as hint_from_jsonable, to_jsonable as hint_to_jsonable
from .item_data import Item, all_items
from .item_marker import (
    ItemMarkersOption, LocationToMarker, make_item_markers, markers_from_jsonable, markers_to_jsonable
)
from .location_data import Location
from .logic_shortcut import LogicShortcut
from .trick import Trick
from .trick_data import tricks_from_names, tricks_to_jsonable


def door_factory() -> "dict[AreaDoor, Union[Item, LogicShortcut]]":
    return vanilla_doors


def daphne_factory() -> DaphneBlocks:
    return DaphneBlocks("Screw", "Screw")


def markers_factory() -> LocationToMarker:
    return make_item_markers(ItemMarkersOption.Simple, [])


class CypherItems(Enum):
    Anything = "Anything"
    NotRequired = "Something Not Required"
    SmallAmmo = "Small Ammo Tanks"
    """ also restricts Suzi map stations from being required in objective rando """


@dataclass
class GameOptions:
    logic: "frozenset[Trick]"
    area_rando: bool
    fill_choice: Literal["M", "MM", "D", "S", "B"]
    small_spaceport: bool
    escape_shortcuts: bool = False
    cypher_items: CypherItems = CypherItems.NotRequired
    daphne_gate: bool = False
    item_markers: ItemMarkersOption = ItemMarkersOption.Simple
    objective_rando: int = 0
    _skip_crash_option_set: bool = False
    """ protected because objective rando auto-enables this """

    def skip_crash(self) -> bool:
        """ objective rando automatically includes skip crash space port """
        return self._skip_crash_option_set or self.objective_rando > 0

    def to_jsonable(self) -> dict[str, Any]:
        dct = asdict(self)
        dct["logic"] = tricks_to_jsonable(dct["logic"])
        dct["cypher_items"] = self.cypher_items.name
        dct["item_markers"] = self.item_markers.name
        return dct

    @staticmethod
    def from_jsonable(d: dict[str, Any]) -> "GameOptions":
        options = GameOptions(**d)
        options.logic = tricks_from_names(d["logic"])
        options.cypher_items = getattr(CypherItems, d["cypher_items"])
        options.item_markers = getattr(ItemMarkersOption, d["item_markers"])
        return options


@dataclass
class Game:
    """ a composition of all the components that make up the generated seed """
    options: GameOptions
    all_locations: dict[str, Location]
    door_pairs: DoorPairs
    seed: int
    door_data: "Mapping[AreaDoor, Union[Item, LogicShortcut]]" = field(default_factory=door_factory)
    item_markers: LocationToMarker = field(default_factory=markers_factory)
    item_placement_spoiler: str = ""
    hint_data: Optional[Hint] = None
    daphne_blocks: DaphneBlocks = field(default_factory=daphne_factory)
    goals: Goals = field(default_factory=Goals)

    def to_jsonable(self) -> dict[str, Any]:
        dct = asdict(self)
        dct["options"] = self.options.to_jsonable()
        dct["door_pairs"] = self.door_pairs.to_jsonable()
        dct["door_data"] = ""  # always vanilla after serialization - If door-cap rando is ever implemented...
        # TODO: I think door_data should be stored differently.
        # (same with DaphneBlocks - I don't like storing LogicShortcut in Game.
        #  It should store a key to a LogicShortcut stored somewhere else.)
        dct["item_markers"] = markers_to_jsonable(self.item_markers)
        dct["hint_data"] = hint_to_jsonable(self.hint_data)
        dct["daphne_blocks"] = asdict(self.daphne_blocks)
        dct["goals"] = asdict(self.goals)

        locations_copy = deepcopy(self.all_locations)
        dct["all_locations"] = locations_copy
        for loc in locations_copy.values():
            assert isinstance(loc, dict)
            item = loc["item"]
            if item:
                item_name = item.name
                assert isinstance(item_name, str)
                non_loc = cast(dict[str, Any], loc)
                non_loc["item"] = item_name

        return dct

    @staticmethod
    def from_jsonable(dct: dict[str, Any]) -> "Game":
        game = Game(**dct)
        game.options = GameOptions.from_jsonable(dct["options"])
        game.door_pairs = DoorPairs.from_jsonable(dct["door_pairs"])
        game.door_data = door_factory()
        game.item_markers = markers_from_jsonable(dct["item_markers"])
        game.hint_data = hint_from_jsonable(dct["hint_data"])
        game.daphne_blocks = DaphneBlocks(**(dct["daphne_blocks"]))
        game.goals = Goals(**(dct["goals"]))

        # change event list to tuples
        game.goals.objectives = list(
            cast(Event, tuple(event))
            for event in game.goals.objectives
        )

        for loc in game.all_locations.values():
            item = loc["item"]
            item_name = cast(Optional[str], item)
            if item_name:
                loc["item"] = all_items[item_name]

        return game
