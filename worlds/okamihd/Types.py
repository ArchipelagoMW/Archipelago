import typing
from typing import NamedTuple, List, Callable, TYPE_CHECKING, TypeVar

from BaseClasses import Location, Item, ItemClassification, LocationProgressType
from rule_builder.rules import Rule, True_, False_
from .Enums import RegionNames
from .Enums.BrushTechniques import BrushTechniques
from .Enums.LocationType import LocationType
from .Enums.OkamiEnemies import OkamiEnemies
from .Enums.WarpType import WarpType
from .Options import OkamiOptions

if TYPE_CHECKING:
    from .. import OkamiWorld


class OkamiLocation(Location):
    game = "Okami HD"


class OkamiItem(Item):
    game = "Okami HD"


class ItemData(NamedTuple):
    code: int
    classification: ItemClassification
    # Number in pool, set this to 0 to exclude the item from the pool
    count_in_pool: Callable[[OkamiOptions], int] | int = 1


class LocData(NamedTuple):
    id: int
    type: LocationType = LocationType.NORMAL_CHEST
    required_brush_techniques: List[BrushTechniques] = []
    power_slash_level: int = 0
    cherry_bomb_level: int = 0
    required_items_events: [str] = []
    mandatory_enemies: List[OkamiEnemies] = []
    needs_long_swim: bool = False
    praise_sanity: int = 0
    progress_type: LocationProgressType | typing.Callable[
        [OkamiOptions], LocationProgressType] = LocationProgressType.DEFAULT
    # This rule overrides all other access rules
    special_rule: Rule | None = None


class EventData(NamedTuple):
    id: int | None = None
    type: LocationType = LocationType.EVENT
    required_brush_techniques: List[BrushTechniques] = []
    power_slash_level: int = 0
    cherry_bomb_level: int = 0
    event_item_name: str | None = None
    required_items_events: [str] = []
    mandatory_enemies: List[OkamiEnemies] = []
    needs_long_swim: bool = False
    precollected: bool | typing.Callable[[OkamiOptions], bool] = False
    is_event_item: bool | typing.Callable[[OkamiOptions], bool] = False
    progress_type: LocationProgressType | typing.Callable[
        [OkamiOptions], LocationProgressType] = LocationProgressType.DEFAULT
    # This rule is added with all other access rules
    special_rule: Rule | None = None


class ExitData(NamedTuple):
    destination: str
    required_items_events: [str] = []
    needs_long_swim: bool = False
    one_way: bool = False
    loading_screen: bool = True


class WarpData(NamedTuple):
    # Type of warp
    type: WarpType
    ## Both of these don't need to specify the "common" requirements (Mist warp,Merdmaid coin or Foutanin)
    # The logical rule to warp from this place to anywhere else
    trigger_warp_from: Rule | True_ | False_
    # The logical rule to warp from anywhere else to this place
    trigger_warp_to: Rule | True_ | False_

# Defines the way an item should be ranomized locally ("To a limited set of locations")
class LocalItem(NamedTuple):
    items:List[str]
    allowed_regions: List[RegionNames]
    is_biteable: bool
    # For debug; name of the prefill phase. Will default to the first item name if set to None.
    prefill_name:str|None = None
    exclude_locations: List[str] = []
    additional_locations: List[str] = []
    # Is this a "bitable" item ? (will exclude location types that directly put the item in the players inventory)



T = TypeVar('T', str, int, bool)


# Generic function to return the value or the resolved value of a callable that depends of options.
def resolve_option_callable(value: T | Callable[[OkamiOptions], T], world: "OkamiWorld") -> T:
    if isinstance(value, Callable):
        return value(world.options)
    else:
        return value
