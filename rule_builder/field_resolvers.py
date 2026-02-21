import dataclasses
import importlib
from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, ClassVar, Self, TypeVar, cast, overload

from typing_extensions import override

from Options import Option

if TYPE_CHECKING:
    from worlds.AutoWorld import World


class FieldResolverRegister:
    """A container class to contain world custom resolvers"""

    custom_resolvers: ClassVar[dict[str, dict[str, type["FieldResolver"]]]] = {}
    """
    A mapping of game name to mapping of resolver name to resolver class
    to hold custom resolvers implemented by worlds
    """

    @classmethod
    def get_resolver_cls(cls, game_name: str, resolver_name: str) -> type["FieldResolver"]:
        """Returns the world-registered or default resolver with the given name"""
        custom_resolver_classes = cls.custom_resolvers.get(game_name, {})
        if resolver_name not in DEFAULT_RESOLVERS and resolver_name not in custom_resolver_classes:
            raise ValueError(f"Resolver '{resolver_name}' for game '{game_name}' not found")
        return custom_resolver_classes.get(resolver_name) or DEFAULT_RESOLVERS[resolver_name]


@dataclasses.dataclass(frozen=True)
class FieldResolver(ABC):
    @abstractmethod
    def resolve(self, world: "World") -> Any: ...

    def to_dict(self) -> dict[str, Any]:
        """Returns a JSON compatible dict representation of this resolver"""
        fields = {field.name: getattr(self, field.name, None) for field in dataclasses.fields(self)}
        return {
            "resolver": self.__class__.__name__,
            **fields,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """Returns a new instance of this resolver from a serialized dict representation"""
        assert data.get("resolver", None) == cls.__name__
        return cls(**{k: v for k, v in data.items() if k != "resolver"})

    @override
    def __str__(self) -> str:
        return self.__class__.__name__

    @classmethod
    def __init_subclass__(cls, /, game: str) -> None:
        if game != "Archipelago":
            custom_resolvers = FieldResolverRegister.custom_resolvers.setdefault(game, {})
            if cls.__qualname__ in custom_resolvers:
                raise TypeError(f"Resolver {cls.__qualname__} has already been registered for game {game}")
            custom_resolvers[cls.__qualname__] = cls
        elif cls.__module__ != "rule_builder.field_resolvers":
            raise TypeError("You cannot define custom resolvers for the base Archipelago world")


@dataclasses.dataclass(frozen=True)
class FromOption(FieldResolver, game="Archipelago"):
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
        field = f".{self.field}" if self.field != "value" else ""
        return f"FromOption({self.option.__name__}{field})"


@dataclasses.dataclass(frozen=True)
class FromWorldAttr(FieldResolver, game="Archipelago"):
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


DEFAULT_RESOLVERS = {
    resolver_name: resolver_class
    for resolver_name, resolver_class in locals().items()
    if isinstance(resolver_class, type)
    and issubclass(resolver_class, FieldResolver)
    and resolver_class is not FieldResolver
}
