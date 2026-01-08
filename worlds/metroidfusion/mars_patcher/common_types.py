from typing import Annotated, TypeAlias

from .mf import auto_generated_types as types_mf
from .zm import auto_generated_types as types_zm

TypeU8: TypeAlias = types_mf.Typeu8 | types_zm.TypeU8

AreaId: TypeAlias = types_mf.Areaid | types_zm.AreaId
RoomId: TypeAlias = TypeU8

AreaRoomPair = tuple[AreaId, RoomId]

MinimapId: TypeAlias = Annotated[int, "0 <= value < 10"]
