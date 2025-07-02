import typing
from typing import NamedTuple, Optional, List
from BaseClasses import Location, Item, ItemClassification
from .Enums.BrushTechniques import BrushTechniques
from .Enums.OkamiEnnemies import OkamiEnnemies
from .Options import OkamiOptions

class OkamiLocation(Location):
    game = "Okami HD"


class OkamiItem(Item):
    game = "Okami HD"


class ItemData(NamedTuple):
    code: int
    classification: ItemClassification

class LocData(NamedTuple):
    id: int
    required_brush_techniques: List[BrushTechniques] = []
    power_slash_level: int = 0
    cherry_bomb_level: int = 0
    # 0 => No, 1=> Yes, 2=> Iron Claws
    buried: int = 0
    required_items_events: [str] = []
    mandatory_enemies: List[OkamiEnnemies] = []
    needs_swim: bool = False
    praise_sanity:int=0

class EventData(NamedTuple):
    id: int | None = None
    required_brush_techniques: List[BrushTechniques] = []
    power_slash_level: int = 0
    cherry_bomb_level: int = 0
    # 0 => No, 1=> Yes, 2=> Iron Claws
    buried: int = 0
    override_event_item_name: str | None = None
    required_items_events: [str] = []
    mandatory_enemies: List[OkamiEnnemies] = []
    needs_swim: bool = False
    is_event_item: bool | typing.Callable[[OkamiOptions], bool] = False
    precollected: bool | typing.Callable[[OkamiOptions], bool] = False

class ExitData(NamedTuple):
    name: str
    destination: str
    has_events: [str] = []
    needs_swim: bool = False
