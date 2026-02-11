import dataclasses
import importlib
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Self, cast

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
        return opt.value

    @override
    def to_dict(self) -> dict[str, Any]:
        return {
            "resolver": "FromOption",
            "option": f"{self.option.__module__}.{self.option.__name__}",
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

        return cls(cast(type[Option[Any]], option))

    @override
    def __str__(self) -> str:
        return f"(FromOption {self.option.__name__})"


@dataclasses.dataclass()
class FromWorldAttr(FieldResolver):
    name: str

    @override
    def resolve(self, world: "World") -> Any:
        return getattr(world, self.name, None)

    @override
    def __str__(self) -> str:
        return f"FromWorldAttr({self.name})"
