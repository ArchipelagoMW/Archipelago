from typing import NamedTuple, TYPE_CHECKING, Any, Callable

from BaseClasses import ItemClassification, CollectionState, LocationProgressType

if not TYPE_CHECKING:
    AccessRule: type = Any
    ExtendedRule: type = Any
    ClassificationMethod: type = Any
    ProgressTypeMethod: type = Any
else:
    from .. import Shapez2World
    AccessRule: type = Callable[[CollectionState], bool]
    ExtendedRule: type = Callable[[CollectionState, Shapez2World], bool]
    ClassificationMethod: type = Callable[[Shapez2World], ItemClassification]
    ProgressTypeMethod: type = Callable[[Shapez2World], LocationProgressType]


class ItemData(NamedTuple):
    item_id: int
    classification: ClassificationMethod
    # The following attribute names originate from how certain things are named in the game's code
    # and thereby might be confusing without context
    remote_id: str
    reward_ids: tuple[str, ...]
    reward_type: int


class PointsItemData(NamedTuple):
    item_id: int
    classification: ClassificationMethod
    amount: int
    reward_type: int


class RegionConnectionData(NamedTuple):
    exiting_region: str
    entering_region: str
    rule: ExtendedRule | None


class LocationData(NamedTuple):
    location_id: int
    progress_type: ProgressTypeMethod
