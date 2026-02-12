import dataclasses
import importlib
from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast, overload

from typing_extensions import override

from Options import Option

if TYPE_CHECKING:
    from worlds.AutoWorld import World


@dataclasses.dataclass()
class FieldResolver(ABC):
    @abstractmethod
    def resolve(self, world: "World") -> Any: ...

    def to_dict(self) -> dict[str, Any]:
        fields = {field.name: getattr(self, field.name, None) for field in dataclasses.fields(self)}
        return {
            "resolver": self.__class__.__name__,
            **fields,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        resolver = data.pop("resolver", None)
        assert resolver == cls.__name__
        return cls(**data)

    @override
    def __str__(self) -> str:
        return self.__class__.__name__


@dataclasses.dataclass()
class FromOption(FieldResolver):
    option: type[Option[Any]]
    field: str = "value"

    @override
    def resolve(self, world: "World") -> Any:
        option_name = next(
            (name for name, cls in world.options.__class__.type_hints.items() if cls is self.option),
            None,
        )

        if option_name is None:
            raise ValueError(
                f"Cannot find option {self.option.__name__} in options class {world.options.__class__.__name__}"
            )
        opt = cast(Option[Any] | None, getattr(world.options, option_name, None))
        if opt is None:
            raise ValueError(f"Invalid option: {option_name}")
        return getattr(opt, self.field)

    @override
    def to_dict(self) -> dict[str, Any]:
        return {
            "resolver": "FromOption",
            "option": f"{self.option.__module__}.{self.option.__name__}",
            "field": self.field,
        }

    @override
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        if "option" not in data:
            raise ValueError("Missing required option")

        option_path = data["option"]
        try:
            option_mod_name, option_cls_name = option_path.rsplit(".", 1)
            option_module = importlib.import_module(option_mod_name)
            option = getattr(option_module, option_cls_name, None)
        except (ValueError, ImportError) as e:
            raise ValueError(f"Cannot parse option '{option_path}'") from e
        if option is None or not issubclass(option, Option):
            raise ValueError(f"Invalid option '{option_path}' returns type '{option}' instead of Option subclass")

        return cls(cast(type[Option[Any]], option), data.get("field", "value"))

    @override
    def __str__(self) -> str:
        return f"FromOption({self.option.__name__}.{self.field})"


@dataclasses.dataclass()
class FromWorldAttr(FieldResolver):
    name: str

    @override
    def resolve(self, world: "World") -> Any:
        obj: Any = world
        for field in self.name.split("."):
            if obj is None:
                return None
            if isinstance(obj, Mapping):
                obj = obj.get(field, None)  # pyright: ignore[reportUnknownMemberType]
            else:
                obj = getattr(obj, field, None)
        return obj

    @override
    def __str__(self) -> str:
        return f"FromWorldAttr({self.name})"


T = TypeVar("T")


@overload
def resolve_field(field: Any, world: "World", expected_type: type[T]) -> T: ...
@overload
def resolve_field(field: Any, world: "World", expected_type: None = None) -> Any: ...
def resolve_field(field: Any, world: "World", expected_type: type[T] | None = None) -> T | Any:
    if isinstance(field, FieldResolver):
        field = field.resolve(world)
    if expected_type:
        assert isinstance(field, expected_type), f"Expected type {expected_type} but got {type(field)}"
    return field
