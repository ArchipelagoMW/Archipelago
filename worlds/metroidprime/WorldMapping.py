from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Dict, Type, TypeVar, Generic, TypedDict

T = TypeVar("T")


class AreaMappingDict(TypedDict):
    area: str
    type_mapping: Any


@dataclass
class AreaMapping(Generic[T]):
    area: str
    type_mapping: T

    def to_dict(self) -> AreaMappingDict:
        return {
            "area": self.area,
            "type_mapping": dict(self.type_mapping),  # type: ignore
        }

    @classmethod
    def from_dict(cls, data: AreaMappingDict) -> "AreaMapping[T]":
        return cls(area=data["area"], type_mapping=data["type_mapping"])


class WorldMapping(Dict[str, AreaMapping[T]], Generic[T]):
    def to_option_value(self) -> Dict[str, AreaMappingDict]:
        return deepcopy({area: mapping.to_dict() for area, mapping in self.items()})

    @classmethod
    def from_option_value_generic(
        cls, data: Dict[str, Any], area_cls: Type[AreaMapping[T]]
    ) -> "WorldMapping[T]":
        return WorldMapping(
            {area: area_cls.from_dict(mapping) for area, mapping in data.items()}
        )
