import dataclasses
import importlib
import operator
from collections.abc import Callable, Iterable
from typing import Any, Final, Literal, Self, cast

from typing_extensions import override

from Options import CommonOptions, Option

Operator = Literal["eq", "ne", "gt", "lt", "ge", "le", "contains", "in"]

OPERATORS: Final[dict[Operator, Callable[..., bool]]] = {
    "eq": operator.eq,
    "ne": operator.ne,
    "gt": operator.gt,
    "lt": operator.lt,
    "ge": operator.ge,
    "le": operator.le,
    "contains": operator.contains,
    "in": operator.contains,
}
OPERATOR_STRINGS: Final[dict[Operator, str]] = {
    "eq": "==",
    "ne": "!=",
    "gt": ">",
    "lt": "<",
    "ge": ">=",
    "le": "<=",
}
REVERSE_OPERATORS: Final[tuple[Operator, ...]] = ("in",)


@dataclasses.dataclass(frozen=True)
class OptionFilter:
    option: type[Option[Any]]
    value: Any
    operator: Operator = "eq"

    def to_dict(self) -> dict[str, Any]:
        """Returns a JSON compatible dict representation of this option filter"""
        return {
            "option": f"{self.option.__module__}.{self.option.__name__}",
            "value": self.value,
            "operator": self.operator,
        }

    def check(self, options: CommonOptions) -> bool:
        """Tests the given options dataclass to see if it passes this option filter"""
        option_name = next(
            (name for name, cls in options.__class__.type_hints.items() if cls is self.option),
            None,
        )
        if option_name is None:
            raise ValueError(f"Cannot find option {self.option.__name__} in options class {options.__class__.__name__}")
        opt = cast(Option[Any] | None, getattr(options, option_name, None))
        if opt is None:
            raise ValueError(f"Invalid option: {option_name}")

        fn = OPERATORS[self.operator]
        return fn(self.value, opt) if self.operator in REVERSE_OPERATORS else fn(opt, self.value)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """Returns a new OptionFilter instance from a dict representation"""
        if "option" not in data or "value" not in data:
            raise ValueError("Missing required value and/or option")

        option_path = data["option"]
        try:
            option_mod_name, option_cls_name = option_path.rsplit(".", 1)
            option_module = importlib.import_module(option_mod_name)
            option = getattr(option_module, option_cls_name, None)
        except (ValueError, ImportError) as e:
            raise ValueError(f"Cannot parse option '{option_path}'") from e
        if option is None or not issubclass(option, Option):
            raise ValueError(f"Invalid option '{option_path}' returns type '{option}' instead of Option subclass")

        value = data["value"]
        operator = data.get("operator", "eq")
        return cls(option=cast(type[Option[Any]], option), value=value, operator=operator)

    @classmethod
    def multiple_from_dict(cls, data: Iterable[dict[str, Any]]) -> tuple[Self, ...]:
        """Returns a tuple of OptionFilters instances from an iterable of dict representations"""
        return tuple(cls.from_dict(o) for o in data)

    @override
    def __str__(self) -> str:
        op = OPERATOR_STRINGS.get(self.operator, self.operator)
        return f"{self.option.__name__} {op} {self.value}"
