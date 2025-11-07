from __future__ import annotations

import abc
import collections
import functools
import logging
import math
import numbers
import random
import typing
import enum
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass

from schema import And, Optional, Or, Schema
from typing_extensions import Self

from Utils import get_file_safe_name, get_fuzzy_results, is_iterable_except_str, output_path

if typing.TYPE_CHECKING:
    from BaseClasses import MultiWorld, PlandoOptions
    from worlds.AutoWorld import World
    import pathlib


def roll_percentage(percentage: int | float) -> bool:
    """Roll a percentage chance.
    percentage is expected to be in range [0, 100]"""
    return random.random() < (float(percentage) / 100)


class OptionError(ValueError):
    pass


class Visibility(enum.IntFlag):
    none = 0b0000
    template = 0b0001
    simple_ui = 0b0010  # show option in simple menus, such as player-options
    complex_ui = 0b0100  # show option in complex menus, such as weighted-options
    spoiler = 0b1000
    all = 0b1111


class AssembleOptions(abc.ABCMeta):
    def __new__(mcs, name, bases, attrs):
        options = attrs["options"] = {}
        name_lookup = attrs["name_lookup"] = {}
        # merge parent class options
        for base in bases:
            if getattr(base, "options", None):
                options.update(base.options)
                name_lookup.update(base.name_lookup)
        new_options = {name[7:].lower(): option_id for name, option_id in attrs.items() if
                       name.startswith("option_")}

        assert "random" not in new_options, "Choice option 'random' cannot be manually assigned."
        assert len(new_options) == len(set(new_options.values())), "same ID cannot be used twice. Try alias?"

        attrs["name_lookup"].update({option_id: name for name, option_id in new_options.items()})
        options.update(new_options)
        # apply aliases, without name_lookup
        aliases = attrs["aliases"] = {name[6:].lower(): option_id for name, option_id in attrs.items() if
                                      name.startswith("alias_")}

        assert (
            name in {"Option", "VerifyKeys"} or  # base abstract classes don't need default
            "default" in attrs or
            any(hasattr(base, "default") for base in bases)
        ), f"Option class {name} needs default value"
        assert "random" not in aliases, "Choice option 'random' cannot be manually assigned."

        # auto-alias Off and On being parsed as True and False
        if "off" in options:
            options["false"] = options["off"]
        if "on" in options:
            options["true"] = options["on"]

        options.update(aliases)

        if "verify" not in attrs:
            # not overridden by class -> look up bases
            verifiers = [f for f in (getattr(base, "verify", None) for base in bases) if f]
            if len(verifiers) > 1:  # verify multiple bases/mixins
                def verify(self, *args, **kwargs) -> None:
                    for f in verifiers:
                        f(self, *args, **kwargs)

                attrs["verify"] = verify
            else:
                assert verifiers, "class Option is supposed to implement def verify"

        # auto-validate schema on __init__
        if "schema" in attrs.keys():

            if "__init__" in attrs:
                def validate_decorator(func):
                    def validate(self, *args, **kwargs):
                        ret = func(self, *args, **kwargs)
                        self.value = self.schema.validate(self.value)
                        return ret

                    return validate

                attrs["__init__"] = validate_decorator(attrs["__init__"])
            else:
                # construct an __init__ that calls parent __init__

                cls = super(AssembleOptions, mcs).__new__(mcs, name, bases, attrs)

                def meta__init__(self, *args, **kwargs):
                    super(cls, self).__init__(*args, **kwargs)
                    self.value = self.schema.validate(self.value)

                cls.__init__ = meta__init__
                return cls

        return super(AssembleOptions, mcs).__new__(mcs, name, bases, attrs)


T = typing.TypeVar('T')


class Option(typing.Generic[T], metaclass=AssembleOptions):
    value: T
    default: typing.ClassVar[typing.Any]  # something that __init__ will be able to convert to the correct type
    visibility = Visibility.all

    # convert option_name_long into Name Long as display_name, otherwise name_long is the result.
    # Handled in get_option_name()
    auto_display_name = False

    # can be weighted between selections
    supports_weighting = True

    rich_text_doc: typing.Optional[bool] = None
    """Whether the WebHost should render the Option's docstring as rich text.

    If this is True, the Option's docstring is interpreted as reStructuredText_,
    the standard Python markup format. In the WebHost, it's rendered to HTML so
    that lists, emphasis, and other rich text features are displayed properly.

    If this is False, the docstring is instead interpreted as plain text, and
    displayed as-is on the WebHost with whitespace preserved.

    If this is None, it inherits the value of `WebWorld.rich_text_options_doc`. For
    backwards compatibility, this defaults to False, but worlds are encouraged to
    set it to True and use reStructuredText for their Option documentation.

    .. _reStructuredText: https://docutils.sourceforge.io/rst.html
    """

    # filled by AssembleOptions:
    name_lookup: typing.ClassVar[typing.Dict[T, str]]  # type: ignore
    # https://github.com/python/typing/discussions/1460 the reason for this type: ignore
    options: typing.ClassVar[typing.Dict[str, int]]
    aliases: typing.ClassVar[typing.Dict[str, int]]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.current_option_name})"

    def __hash__(self) -> int:
        return hash(self.value)

    @property
    def current_key(self) -> str:
        return self.name_lookup[self.value]

    @property
    def current_option_name(self) -> str:
        """For display purposes. Worlds should be using current_key."""
        return self.get_option_name(self.value)

    @classmethod
    def get_option_name(cls, value: T) -> str:
        if cls.auto_display_name:
            return cls.name_lookup[value].replace("_", " ").title()
        else:
            return cls.name_lookup[value]

    def __int__(self) -> T:
        return self.value

    def __bool__(self) -> bool:
        return bool(self.value)

    @classmethod
    @abc.abstractmethod
    def from_any(cls, data: typing.Any) -> Option[T]:
        ...

    if typing.TYPE_CHECKING:
        def verify(self, world: typing.Type[World], player_name: str, plando_options: PlandoOptions) -> None:
            pass
    else:
        def verify(self, *args, **kwargs) -> None:
            pass


class FreeText(Option[str]):
    """Text option that allows users to enter strings.
    Needs to be validated by the world or option definition."""

    default = ""

    def __init__(self, value: str):
        assert isinstance(value, str), "value of FreeText must be a string"
        self.value = value

    @property
    def current_key(self) -> str:
        return self.value

    @classmethod
    def from_text(cls, text: str) -> FreeText:
        return cls(text)

    @classmethod
    def from_any(cls, data: typing.Any) -> FreeText:
        return cls.from_text(str(data))

    @classmethod
    def get_option_name(cls, value: str) -> str:
        return value

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return other.value == self.value
        elif isinstance(other, str):
            return other == self.value
        else:
            raise TypeError(f"Can't compare {self.__class__.__name__} with {other.__class__.__name__}")


class NumericOption(Option[int], numbers.Integral, abc.ABC):
    default = 0

    # note: some of the `typing.Any`` here is a result of unresolved issue in python standards
    # `int` is not a `numbers.Integral` according to the official typestubs
    # (even though isinstance(5, numbers.Integral) == True)
    # https://github.com/python/typing/issues/272
    # https://github.com/python/mypy/issues/3186
    # https://github.com/microsoft/pyright/issues/1575

    def __eq__(self, other: typing.Any) -> bool:
        if isinstance(other, NumericOption):
            return self.value == other.value
        else:
            return typing.cast(bool, self.value == other)

    def __lt__(self, other: typing.Union[int, NumericOption]) -> bool:
        if isinstance(other, NumericOption):
            return self.value < other.value
        else:
            return self.value < other

    def __le__(self, other: typing.Union[int, NumericOption]) -> bool:
        if isinstance(other, NumericOption):
            return self.value <= other.value
        else:
            return self.value <= other

    def __gt__(self, other: typing.Union[int, NumericOption]) -> bool:
        if isinstance(other, NumericOption):
            return self.value > other.value
        else:
            return self.value > other

    def __ge__(self, other: typing.Union[int, NumericOption]) -> bool:
        if isinstance(other, NumericOption):
            return self.value >= other.value
        else:
            return self.value >= other

    def __bool__(self) -> bool:
        return bool(self.value)

    def __int__(self) -> int:
        return self.value

    def __mul__(self, other: typing.Any) -> typing.Any:
        if isinstance(other, NumericOption):
            return self.value * other.value
        else:
            return self.value * other

    def __rmul__(self, other: typing.Any) -> typing.Any:
        if isinstance(other, NumericOption):
            return other.value * self.value
        else:
            return other * self.value

    def __sub__(self, other: typing.Any) -> typing.Any:
        if isinstance(other, NumericOption):
            return self.value - other.value
        else:
            return self.value - other

    def __rsub__(self, left: typing.Any) -> typing.Any:
        if isinstance(left, NumericOption):
            return left.value - self.value
        else:
            return left - self.value

    def __add__(self, other: typing.Any) -> typing.Any:
        if isinstance(other, NumericOption):
            return self.value + other.value
        else:
            return self.value + other

    def __radd__(self, left: typing.Any) -> typing.Any:
        if isinstance(left, NumericOption):
            return left.value + self.value
        else:
            return left + self.value

    def __truediv__(self, other: typing.Any) -> typing.Any:
        if isinstance(other, NumericOption):
            return self.value / other.value
        else:
            return self.value / other

    def __rtruediv__(self, left: typing.Any) -> typing.Any:
        if isinstance(left, NumericOption):
            return left.value / self.value
        else:
            return left / self.value

    def __abs__(self) -> typing.Any:
        return abs(self.value)

    def __and__(self, other: typing.Any) -> int:
        return self.value & int(other)

    def __ceil__(self) -> int:
        return math.ceil(self.value)

    def __floor__(self) -> int:
        return math.floor(self.value)

    def __floordiv__(self, other: typing.Any) -> int:
        return self.value // int(other)

    def __invert__(self) -> int:
        return ~(self.value)

    def __lshift__(self, other: typing.Any) -> int:
        return self.value << int(other)

    def __mod__(self, other: typing.Any) -> int:
        return self.value % int(other)

    def __neg__(self) -> int:
        return -(self.value)

    def __or__(self, other: typing.Any) -> int:
        return self.value | int(other)

    def __pos__(self) -> int:
        return +(self.value)

    def __pow__(self, exponent: numbers.Complex, modulus: typing.Optional[numbers.Integral] = None) -> int:
        if not (modulus is None):
            assert isinstance(exponent, numbers.Integral)
            return pow(self.value, exponent, modulus)  # type: ignore
        return self.value ** exponent  # type: ignore

    def __rand__(self, other: typing.Any) -> int:
        return int(other) & self.value

    def __rfloordiv__(self, other: typing.Any) -> int:
        return int(other) // self.value

    def __rlshift__(self, other: typing.Any) -> int:
        return int(other) << self.value

    def __rmod__(self, other: typing.Any) -> int:
        return int(other) % self.value

    def __ror__(self, other: typing.Any) -> int:
        return int(other) | self.value

    def __round__(self, ndigits: typing.Optional[int] = None) -> int:
        return round(self.value, ndigits)

    def __rpow__(self, base: typing.Any) -> typing.Any:
        return base ** self.value

    def __rrshift__(self, other: typing.Any) -> int:
        return int(other) >> self.value

    def __rshift__(self, other: typing.Any) -> int:
        return self.value >> int(other)

    def __rxor__(self, other: typing.Any) -> int:
        return int(other) ^ self.value

    def __trunc__(self) -> int:
        return math.trunc(self.value)

    def __xor__(self, other: typing.Any) -> int:
        return self.value ^ int(other)


class Toggle(NumericOption):
    option_false = 0
    option_true = 1
    default = 0

    def __init__(self, value: int):
        # if user puts in an invalid value, make it valid
        value = int(bool(value))
        self.value = value

    @classmethod
    def from_text(cls, text: str) -> Toggle:
        if text == "random":
            return cls(random.choice(list(cls.name_lookup)))
        elif text.lower() in {"off", "0", "false", "none", "null", "no"}:
            return cls(0)
        else:
            return cls(1)

    @classmethod
    def from_any(cls, data: typing.Any):
        if type(data) == str:
            return cls.from_text(data)
        else:
            return cls(int(data))

    @classmethod
    def get_option_name(cls, value):
        return ["No", "Yes"][int(value)]

    __hash__ = Option.__hash__  # see https://docs.python.org/3/reference/datamodel.html#object.__hash__


class DefaultOnToggle(Toggle):
    default = 1


class Choice(NumericOption):
    auto_display_name = True

    def __init__(self, value: int):
        self.value: int = value

    @classmethod
    def from_text(cls, text: str) -> Choice:
        text = text.lower()
        if text == "random":
            return cls(random.choice(list(cls.name_lookup)))
        for option_name, value in cls.options.items():
            if option_name == text:
                return cls(value)
        raise KeyError(
            f'Could not find option "{text}" for "{cls.__name__}", '
            f'known options are {", ".join(f"{option}" for option in cls.name_lookup.values())}')

    @classmethod
    def from_any(cls, data: typing.Any) -> Choice:
        if type(data) == int and data in cls.options.values():
            return cls(data)
        return cls.from_text(str(data))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return other.value == self.value
        elif isinstance(other, str):
            assert other in self.options, f"compared against a str that could never be equal. {self} == {other}"
            return other == self.current_key
        elif isinstance(other, int):
            assert other in self.name_lookup, f"compared against an int that could never be equal. {self} == {other}"
            return other == self.value
        elif isinstance(other, bool):
            return other == bool(self.value)
        else:
            raise TypeError(f"Can't compare {self.__class__.__name__} with {other.__class__.__name__}")

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return other.value != self.value
        elif isinstance(other, str):
            assert other in self.options, f"compared against a str that could never be equal. {self} != {other}"
            return other != self.current_key
        elif isinstance(other, int):
            assert other in self.name_lookup, f"compared against am int that could never be equal. {self} != {other}"
            return other != self.value
        elif isinstance(other, bool):
            return other != bool(self.value)
        elif other is None:
            return False
        else:
            raise TypeError(f"Can't compare {self.__class__.__name__} with {other.__class__.__name__}")

    def __lt__(self, other: typing.Union[Choice, int, str]):
        if isinstance(other, str):
            assert other in self.options, f"compared against an unknown string. {self} < {other}"
            other = self.options[other]
        return super(Choice, self).__lt__(other)

    def __gt__(self, other: typing.Union[Choice, int, str]):
        if isinstance(other, str):
            assert other in self.options, f"compared against an unknown string. {self} > {other}"
            other = self.options[other]
        return super(Choice, self).__gt__(other)

    def __le__(self, other: typing.Union[Choice, int, str]):
        if isinstance(other, str):
            assert other in self.options, f"compared against an unknown string. {self} <= {other}"
            other = self.options[other]
        return super(Choice, self).__le__(other)

    def __ge__(self, other: typing.Union[Choice, int, str]):
        if isinstance(other, str):
            assert other in self.options, f"compared against an unknown string. {self} >= {other}"
            other = self.options[other]
        return super(Choice, self).__ge__(other)

    __hash__ = Option.__hash__  # see https://docs.python.org/3/reference/datamodel.html#object.__hash__


class TextChoice(Choice):
    """Allows custom string input and offers choices. Choices will resolve to int and text will resolve to string"""
    value: typing.Union[str, int]

    def __init__(self, value: typing.Union[str, int]):
        assert isinstance(value, str) or isinstance(value, int), \
            f"'{value}' is not a valid option for '{self.__class__.__name__}'"
        self.value = value

    @property
    def current_key(self) -> str:
        if isinstance(self.value, str):
            return self.value
        return super().current_key

    @classmethod
    def from_text(cls, text: str) -> TextChoice:
        if text.lower() == "random":  # chooses a random defined option but won't use any free text options
            return cls(random.choice(list(cls.name_lookup)))
        for option_name, value in cls.options.items():
            if option_name.lower() == text.lower():
                return cls(value)
        return cls(text)

    @classmethod
    def get_option_name(cls, value: T) -> str:
        if isinstance(value, str):
            return value
        return super().get_option_name(value)

    def __eq__(self, other: typing.Any):
        if isinstance(other, self.__class__):
            return other.value == self.value
        elif isinstance(other, str):
            if other in self.options:
                return other == self.current_key
            return other == self.value
        elif isinstance(other, int):
            assert other in self.name_lookup, f"compared against an int that could never be equal. {self} == {other}"
            return other == self.value
        elif isinstance(other, bool):
            return other == bool(self.value)
        else:
            raise TypeError(f"Can't compare {self.__class__.__name__} with {other.__class__.__name__}")


class BossMeta(AssembleOptions):
    def __new__(mcs, name, bases, attrs):
        if name != "PlandoBosses":
            assert "bosses" in attrs, f"Please define valid bosses for {name}"
            attrs["bosses"] = frozenset((boss.lower() for boss in attrs["bosses"]))
            assert "locations" in attrs, f"Please define valid locations for {name}"
            attrs["locations"] = frozenset((location.lower() for location in attrs["locations"]))
        cls = super().__new__(mcs, name, bases, attrs)
        assert not cls.duplicate_bosses or "singularity" in cls.options, f"Please define option_singularity for {name}"
        return cls


class PlandoBosses(TextChoice, metaclass=BossMeta):
    """Generic boss shuffle option that supports plando. Format expected is
    'location1-boss1;location2-boss2;shuffle_mode'.
    If shuffle_mode is not provided in the string, this will be the default shuffle mode. Must override can_place_boss,
    which passes a plando boss and location. Check if the placement is valid for your game here."""
    bosses: typing.ClassVar[typing.Union[typing.Set[str], typing.FrozenSet[str]]]
    locations: typing.ClassVar[typing.Union[typing.Set[str], typing.FrozenSet[str]]]

    duplicate_bosses: bool = False

    @classmethod
    def from_text(cls, text: str):
        # set all of our text to lower case for name checking
        text = text.lower()
        if text == "random":
            return cls(random.choice(list(cls.options.values())))
        for option_name, value in cls.options.items():
            if option_name == text:
                return cls(value)
        options = text.split(";")

        # since plando exists in the option verify the plando values given are valid
        cls.validate_plando_bosses(options)
        return cls.get_shuffle_mode(options)

    @classmethod
    def get_shuffle_mode(cls, option_list: typing.List[str]):
        # find out what mode of boss shuffle we should use for placing bosses after plando
        # and add as a string to look nice in the spoiler
        if "random" in option_list:
            shuffle = random.choice(list(cls.options))
            option_list.remove("random")
            options = ";".join(option_list) + f";{shuffle}"
            boss_class = cls(options)
        else:
            for option in option_list:
                if option in cls.options:
                    options = ";".join(option_list)
                    break
            else:
                if cls.duplicate_bosses and len(option_list) == 1:
                    if cls.valid_boss_name(option_list[0]):
                        # this doesn't exist in this class but it's a forced option for classes where this is called
                        options = option_list[0] + ";singularity"
                    else:
                        options = option_list[0] + f";{cls.name_lookup[cls.default]}"
                else:
                    options = ";".join(option_list) + f";{cls.name_lookup[cls.default]}"
            boss_class = cls(options)
        return boss_class

    @classmethod
    def validate_plando_bosses(cls, options: typing.List[str]) -> None:
        used_locations = []
        used_bosses = []
        for option in options:
            # check if a shuffle mode was provided in the incorrect location
            if option == "random" or option in cls.options:
                if option != options[-1]:
                    raise ValueError(f"{option} option must be at the end of the boss_shuffle options!")
            elif "-" in option:
                location, boss = option.split("-")
                if location in used_locations:
                    raise ValueError(f"Duplicate Boss Location {location} not allowed.")
                if not cls.duplicate_bosses and boss in used_bosses:
                    raise ValueError(f"Duplicate Boss {boss} not allowed.")
                used_locations.append(location)
                used_bosses.append(boss)
                if not cls.valid_boss_name(boss):
                    raise ValueError(f"'{boss.title()}' is not a valid boss name.")
                if not cls.valid_location_name(location):
                    raise ValueError(f"'{location.title()}' is not a valid boss location name.")
                if not cls.can_place_boss(boss, location):
                    raise ValueError(f"'{location.title()}' is not a valid location for {boss.title()} to be placed.")
            else:
                if cls.duplicate_bosses:
                    if not cls.valid_boss_name(option):
                        raise ValueError(f"'{option}' is not a valid boss name.")
                else:
                    raise ValueError(f"'{option.title()}' is not formatted correctly.")

    @classmethod
    def can_place_boss(cls, boss: str, location: str) -> bool:
        raise NotImplementedError

    @classmethod
    def valid_boss_name(cls, value: str) -> bool:
        return value in cls.bosses

    @classmethod
    def valid_location_name(cls, value: str) -> bool:
        return value in cls.locations

    def verify(self, world: typing.Type[World], player_name: str, plando_options: "PlandoOptions") -> None:
        if isinstance(self.value, int):
            return
        from BaseClasses import PlandoOptions
        if not (PlandoOptions.bosses & plando_options):
            # plando is disabled but plando options were given so pull the option and change it to an int
            option = self.value.split(";")[-1]
            self.value = self.options[option]
            logging.warning(f"The plando bosses module is turned off, so {self.name_lookup[self.value].title()} "
                            f"boss shuffle will be used for player {player_name}.")


class Range(NumericOption):
    range_start = 0
    range_end = 1

    def __init__(self, value: int):
        if value < self.range_start:
            raise Exception(f"{value} is lower than minimum {self.range_start} for option {self.__class__.__name__}")
        elif value > self.range_end:
            raise Exception(f"{value} is higher than maximum {self.range_end} for option {self.__class__.__name__}")
        self.value = value

    @classmethod
    def from_text(cls, text: str) -> Range:
        text = text.lower()
        if text.startswith("random"):
            return cls.weighted_range(text)
        elif text == "default" and hasattr(cls, "default"):
            return cls.from_any(cls.default)
        elif text == "high":
            return cls(cls.range_end)
        elif text == "low":
            return cls(cls.range_start)
        elif cls.range_start == 0 \
                and hasattr(cls, "default") \
                and cls.default != 0 \
                and text in ("true", "false"):
            # these are the conditions where "true" and "false" make sense
            if text == "true":
                return cls.from_any(cls.default)
            else:  # "false"
                return cls(0)
        return cls(int(text))

    @classmethod
    def weighted_range(cls, text) -> Range:
        if text == "random-low":
            return cls(cls.triangular(cls.range_start, cls.range_end, 0.0))
        elif text == "random-high":
            return cls(cls.triangular(cls.range_start, cls.range_end, 1.0))
        elif text == "random-middle":
            return cls(cls.triangular(cls.range_start, cls.range_end))
        elif text.startswith("random-range-"):
            return cls.custom_range(text)
        elif text == "random":
            return cls(random.randint(cls.range_start, cls.range_end))
        else:
            raise Exception(f"random text \"{text}\" did not resolve to a recognized pattern. "
                            f"Acceptable values are: random, random-high, random-middle, random-low, "
                            f"random-range-low-<min>-<max>, random-range-middle-<min>-<max>, "
                            f"random-range-high-<min>-<max>, or random-range-<min>-<max>.")

    @classmethod
    def custom_range(cls, text) -> Range:
        textsplit = text.split("-")
        try:
            random_range = [int(textsplit[len(textsplit) - 2]), int(textsplit[len(textsplit) - 1])]
        except ValueError:
            raise ValueError(f"Invalid random range {text} for option {cls.__name__}")
        random_range.sort()
        if random_range[0] < cls.range_start or random_range[1] > cls.range_end:
            raise Exception(
                f"{random_range[0]}-{random_range[1]} is outside allowed range "
                f"{cls.range_start}-{cls.range_end} for option {cls.__name__}")
        if text.startswith("random-range-low"):
            return cls(cls.triangular(random_range[0], random_range[1], 0.0))
        elif text.startswith("random-range-middle"):
            return cls(cls.triangular(random_range[0], random_range[1]))
        elif text.startswith("random-range-high"):
            return cls(cls.triangular(random_range[0], random_range[1], 1.0))
        else:
            return cls(random.randint(random_range[0], random_range[1]))

    @classmethod
    def from_any(cls, data: typing.Any) -> Range:
        if type(data) == int:
            return cls(data)
        return cls.from_text(str(data))

    @classmethod
    def get_option_name(cls, value: int) -> str:
        return str(value)

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    def triangular(lower: int, end: int, tri: float = 0.5) -> int:
        """
        Integer triangular distribution for `lower` inclusive to `end` inclusive.

        Expects `lower <= end` and `0.0 <= tri <= 1.0`. The result of other inputs is undefined.
        """
        # Use the continuous range [lower, end + 1) to produce an integer result in [lower, end].
        # random.triangular is actually [a, b] and not [a, b), so there is a very small chance of getting exactly b even
        # when a != b, so ensure the result is never more than `end`.
        return min(end, math.floor(random.triangular(0.0, 1.0, tri) * (end - lower + 1) + lower))


class NamedRange(Range):
    special_range_names: typing.Dict[str, int] = {}
    """Special Range names have to be all lowercase as matching is done with text.lower()"""

    def __init__(self, value: int) -> None:
        if value < self.range_start and value not in self.special_range_names.values():
            raise Exception(f"{value} is lower than minimum {self.range_start} for option {self.__class__.__name__} " +
                            f"and is also not one of the supported named special values: {self.special_range_names}")
        elif value > self.range_end and value not in self.special_range_names.values():
            raise Exception(f"{value} is higher than maximum {self.range_end} for option {self.__class__.__name__} " +
                            f"and is also not one of the supported named special values: {self.special_range_names}")

        # See docstring
        for key in self.special_range_names:
            if key != key.lower():
                raise Exception(f"{self.__class__.__name__} has an invalid special_range_names key: {key}. "
                                f"NamedRange keys must use only lowercase letters, and ideally should be snake_case.")
        self.value = value

    @classmethod
    def from_text(cls, text: str) -> Range:
        text = text.lower()
        if text in cls.special_range_names:
            return cls(cls.special_range_names[text])
        return super().from_text(text)


class FreezeValidKeys(AssembleOptions):
    def __new__(mcs, name, bases, attrs):
        assert not "_valid_keys" in attrs, "'_valid_keys' gets set by FreezeValidKeys, define 'valid_keys' instead."
        if "valid_keys" in attrs:
            attrs["_valid_keys"] = frozenset(attrs["valid_keys"])
        return super(FreezeValidKeys, mcs).__new__(mcs, name, bases, attrs)


class VerifyKeys(metaclass=FreezeValidKeys):
    valid_keys: typing.Iterable = []
    _valid_keys: frozenset  # gets created by AssembleOptions from valid_keys
    valid_keys_casefold: bool = False
    convert_name_groups: bool = False
    verify_item_name: bool = False
    verify_location_name: bool = False
    value: typing.Any

    def verify_keys(self) -> None:
        if self.valid_keys:
            data = set(self.value)
            dataset = set(word.casefold() for word in data) if self.valid_keys_casefold else set(data)
            extra = dataset - self._valid_keys
            if extra:
                raise OptionError(
                    f"Found unexpected key {', '.join(extra)} in {getattr(self, 'display_name', self)}. "
                    f"Allowed keys: {self._valid_keys}."
                )

    def verify(self, world: typing.Type[World], player_name: str, plando_options: "PlandoOptions") -> None:
        try:
            self.verify_keys()
        except OptionError as validation_error:
            raise OptionError(f"Player {player_name} has invalid option keys:\n{validation_error}")
        if self.convert_name_groups and self.verify_item_name:
            new_value = type(self.value)()  # empty container of whatever value is
            for item_name in self.value:
                new_value |= world.item_name_groups.get(item_name, {item_name})
            self.value = new_value
        elif self.convert_name_groups and self.verify_location_name:
            new_value = type(self.value)()
            for loc_name in self.value:
                new_value |= world.location_name_groups.get(loc_name, {loc_name})
            self.value = new_value
        if self.verify_item_name:
            for item_name in self.value:
                if item_name not in world.item_names:
                    picks = get_fuzzy_results(item_name, world.item_names, limit=1)
                    raise Exception(f"Item '{item_name}' from option '{self}' "
                                    f"is not a valid item name from '{world.game}'. "
                                    f"Did you mean '{picks[0][0]}' ({picks[0][1]}% sure)")
        elif self.verify_location_name:
            for location_name in self.value:
                if location_name not in world.location_names:
                    picks = get_fuzzy_results(location_name, world.location_names, limit=1)
                    raise Exception(f"Location '{location_name}' from option '{self}' "
                                    f"is not a valid location name from '{world.game}'. "
                                    f"Did you mean '{picks[0][0]}' ({picks[0][1]}% sure)")

    def __iter__(self) -> typing.Iterator[typing.Any]:
        return self.value.__iter__()

    
class OptionDict(Option[typing.Dict[str, typing.Any]], VerifyKeys, typing.Mapping[str, typing.Any]):
    default = {}
    supports_weighting = False

    def __init__(self, value: typing.Dict[str, typing.Any]):
        self.value = deepcopy(value)

    @classmethod
    def from_any(cls, data: typing.Dict[str, typing.Any]) -> OptionDict:
        if type(data) == dict:
            return cls(data)
        else:
            raise NotImplementedError(f"Cannot Convert from non-dictionary, got {type(data)}")

    def get_option_name(self, value):
        return ", ".join(f"{key}: {v}" for key, v in value.items())

    def __getitem__(self, item: str) -> typing.Any:
        return self.value[item]

    def __iter__(self) -> typing.Iterator[str]:
        return iter(self.value)

    def __len__(self) -> int:
        return len(self.value)

    # __getitem__ fallback fails for Counters, so we define this explicitly
    def __contains__(self, item) -> bool:
        return item in self.value


class OptionCounter(OptionDict):
    min: int | None = None
    max: int | None = None

    def __init__(self, value: dict[str, int]) -> None:
        super(OptionCounter, self).__init__(collections.Counter(value))

    def verify(self, world: type[World], player_name: str, plando_options: PlandoOptions) -> None:
        super(OptionCounter, self).verify(world, player_name, plando_options)

        range_errors = []

        if self.max is not None:
            range_errors += [
                f"\"{key}: {value}\" is higher than maximum allowed value {self.max}."
                for key, value in self.value.items() if value > self.max
            ]

        if self.min is not None:
            range_errors += [
                f"\"{key}: {value}\" is lower than minimum allowed value {self.min}."
                for key, value in self.value.items() if value < self.min
            ]

        if range_errors:
            range_errors = [f"For option {getattr(self, 'display_name', self)}:"] + range_errors
            raise OptionError("\n".join(range_errors))


class ItemDict(OptionCounter):
    verify_item_name = True

    min = 0

    def __init__(self, value: dict[str, int]) -> None:
        # Backwards compatibility: Cull 0s to make "in" checks behave the same as when this wasn't a OptionCounter
        value = {item_name: amount for item_name, amount in value.items() if amount != 0}

        super(ItemDict, self).__init__(value)


class OptionList(Option[typing.List[typing.Any]], VerifyKeys):
    # Supports duplicate entries and ordering.
    # If only unique entries are needed and input order of elements does not matter, OptionSet should be used instead.
    # Not a docstring so it doesn't get grabbed by the options system.

    default = ()
    supports_weighting = False

    def __init__(self, value: typing.Iterable[typing.Any]):
        self.value = list(deepcopy(value))
        super(OptionList, self).__init__()

    @classmethod
    def from_text(cls, text: str):
        return cls([option.strip() for option in text.split(",")])

    @classmethod
    def from_any(cls, data: typing.Any):
        if is_iterable_except_str(data):
            return cls(data)
        return cls.from_text(str(data))

    def get_option_name(self, value):
        return ", ".join(map(str, value))

    def __contains__(self, item):
        return item in self.value


class OptionSet(Option[typing.Set[str]], VerifyKeys):
    default = frozenset()
    supports_weighting = False

    def __init__(self, value: typing.Iterable[str]):
        self.value = set(deepcopy(value))
        super(OptionSet, self).__init__()

    @classmethod
    def from_text(cls, text: str):
        return cls([option.strip() for option in text.split(",")])

    @classmethod
    def from_any(cls, data: typing.Any):
        if is_iterable_except_str(data):
            return cls(data)
        return cls.from_text(str(data))

    def get_option_name(self, value):
        return ", ".join(sorted(value))

    def __contains__(self, item):
        return item in self.value


class ItemSet(OptionSet):
    verify_item_name = True
    convert_name_groups = True


class PlandoText(typing.NamedTuple):
    at: str
    text: typing.List[str]
    percentage: int = 100


PlandoTextsFromAnyType = typing.Union[
    typing.Iterable[typing.Union[typing.Mapping[str, typing.Any], PlandoText, typing.Any]], typing.Any
]


class PlandoTexts(Option[typing.List[PlandoText]], VerifyKeys):
    default = ()
    supports_weighting = False
    display_name = "Plando Texts"

    def __init__(self, value: typing.Iterable[PlandoText]) -> None:
        self.value = list(deepcopy(value))
        super().__init__()

    def verify(self, world: typing.Type[World], player_name: str, plando_options: "PlandoOptions") -> None:
        from BaseClasses import PlandoOptions
        if self.value and not (PlandoOptions.texts & plando_options):
            # plando is disabled but plando options were given so overwrite the options
            self.value = []
            logging.warning(f"The plando texts module is turned off, "
                            f"so text for {player_name} will be ignored.")
        else:
            super().verify(world, player_name, plando_options)

    def verify_keys(self) -> None:
        if self.valid_keys:
            data = set(text.at for text in self)
            dataset = set(word.casefold() for word in data) if self.valid_keys_casefold else set(data)
            extra = dataset - self._valid_keys
            if extra:
                raise OptionError(
                    f"Invalid \"at\" placement {', '.join(extra)} in {getattr(self, 'display_name', self)}. "
                    f"Allowed placements: {self._valid_keys}."
                )

    @classmethod
    def from_any(cls, data: PlandoTextsFromAnyType) -> Self:
        texts: typing.List[PlandoText] = []
        if isinstance(data, typing.Iterable):
            for text in data:
                if isinstance(text, typing.Mapping):
                    if roll_percentage(text.get("percentage", 100)):
                        at = text.get("at", None)
                        if at is not None:
                            if isinstance(at, dict):
                                if at:
                                    at = random.choices(list(at.keys()),
                                                        weights=list(at.values()), k=1)[0]
                                else:
                                    raise OptionError("\"at\" must be a valid string or weighted list of strings!")
                            given_text = text.get("text", [])
                            if isinstance(given_text, dict):
                                if not given_text:
                                    given_text = []
                                else:
                                    given_text = random.choices(list(given_text.keys()),
                                                                weights=list(given_text.values()), k=1)
                            if isinstance(given_text, str):
                                given_text = [given_text]
                            texts.append(PlandoText(
                                at,
                                given_text,
                                text.get("percentage", 100)
                            ))
                        else:
                            raise OptionError("\"at\" must be a valid string or weighted list of strings!")
                elif isinstance(text, PlandoText):
                    if roll_percentage(text.percentage):
                        texts.append(text)
                else:
                    raise Exception(f"Cannot create plando text from non-dictionary type, got {type(text)}")
            return cls(texts)
        else:
            raise NotImplementedError(f"Cannot Convert from non-list, got {type(data)}")

    @classmethod
    def get_option_name(cls, value: typing.List[PlandoText]) -> str:
        return str({text.at: " ".join(text.text) for text in value})

    def __iter__(self) -> typing.Iterator[PlandoText]:
        yield from self.value

    def __getitem__(self, index: typing.SupportsIndex) -> PlandoText:
        return self.value[index]

    def __len__(self) -> int:
        return len(self.value)


class ConnectionsMeta(AssembleOptions):
    def __new__(mcs, name: str, bases: tuple[type, ...], attrs: dict[str, typing.Any]):
        if name != "PlandoConnections":
            assert "entrances" in attrs, f"Please define valid entrances for {name}"
            attrs["entrances"] = frozenset((connection.lower() for connection in attrs["entrances"]))
            assert "exits" in attrs, f"Please define valid exits for {name}"
            attrs["exits"] = frozenset((connection.lower() for connection in attrs["exits"]))
        if "__doc__" not in attrs:
            attrs["__doc__"] = PlandoConnections.__doc__
        cls = super().__new__(mcs, name, bases, attrs)
        return cls


class PlandoConnection(typing.NamedTuple):
    class Direction:
        entrance = "entrance"
        exit = "exit"
        both = "both"

    entrance: str
    exit: str
    direction: typing.Literal["entrance", "exit", "both"]  # TODO: convert Direction to StrEnum once 3.10 is dropped
    percentage: int = 100


PlandoConFromAnyType = typing.Union[
    typing.Iterable[typing.Union[typing.Mapping[str, typing.Any], PlandoConnection, typing.Any]], typing.Any
]


class PlandoConnections(Option[typing.List[PlandoConnection]], metaclass=ConnectionsMeta):
    """Generic connections plando. Format is:
    - entrance: "Entrance Name"
      exit: "Exit Name"
      direction: "Direction"
      percentage: 100
    Direction must be one of 'entrance', 'exit', or 'both', and defaults to 'both' if omitted.
    Percentage is an integer from 1 to 100, and defaults to 100 when omitted."""

    display_name = "Plando Connections"

    default = ()
    supports_weighting = False

    entrances: typing.ClassVar[typing.AbstractSet[str]]
    exits: typing.ClassVar[typing.AbstractSet[str]]

    duplicate_exits: bool = False
    """Whether or not exits should be allowed to be duplicate."""

    def __init__(self, value: typing.Iterable[PlandoConnection]):
        self.value = list(deepcopy(value))
        super(PlandoConnections, self).__init__()

    @classmethod
    def validate_entrance_name(cls, entrance: str) -> bool:
        return entrance.lower() in cls.entrances

    @classmethod
    def validate_exit_name(cls, exit: str) -> bool:
        return exit.lower() in cls.exits

    @classmethod
    def can_connect(cls, entrance: str, exit: str) -> bool:
        """Checks that a given entrance can connect to a given exit.
        By default, this will always return true unless overridden."""
        return True

    @classmethod
    def validate_plando_connections(cls, connections: typing.Iterable[PlandoConnection]) -> None:
        used_entrances: typing.List[str] = []
        used_exits: typing.List[str] = []
        for connection in connections:
            entrance = connection.entrance
            exit = connection.exit
            direction = connection.direction
            if direction not in (PlandoConnection.Direction.entrance,
                                 PlandoConnection.Direction.exit,
                                 PlandoConnection.Direction.both):
                raise ValueError(f"Unknown direction: {direction}")
            if entrance in used_entrances:
                raise ValueError(f"Duplicate Entrance {entrance} not allowed.")
            if not cls.duplicate_exits and exit in used_exits:
                raise ValueError(f"Duplicate Exit {exit} not allowed.")
            used_entrances.append(entrance)
            used_exits.append(exit)
            if not cls.validate_entrance_name(entrance):
                raise ValueError(f"'{entrance.title()}' is not a valid entrance.")
            if not cls.validate_exit_name(exit):
                raise ValueError(f"'{exit.title()}' is not a valid exit.")
            if not cls.can_connect(entrance, exit):
                raise ValueError(f"Connection between '{entrance.title()}' and '{exit.title()}' is invalid.")

    @classmethod
    def from_any(cls, data: PlandoConFromAnyType) -> Self:
        if not isinstance(data, typing.Iterable):
            raise Exception(f"Cannot create plando connections from non-List value, got {type(data)}.")

        value: typing.List[PlandoConnection] = []
        for connection in data:
            if isinstance(connection, typing.Mapping):
                percentage = connection.get("percentage", 100)
                if roll_percentage(percentage):
                    entrance = connection.get("entrance", None)
                    if is_iterable_except_str(entrance):
                        entrance = random.choice(sorted(entrance))
                    exit = connection.get("exit", None)
                    if is_iterable_except_str(exit):
                        exit = random.choice(sorted(exit))
                    direction = connection.get("direction", "both")

                    if not entrance or not exit:
                        raise Exception("Plando connection must have an entrance and an exit.")
                    value.append(PlandoConnection(
                        entrance,
                        exit,
                        direction,
                        percentage
                    ))
            elif isinstance(connection, PlandoConnection):
                if roll_percentage(connection.percentage):
                    value.append(connection)
            else:
                raise Exception(f"Cannot create connection from non-Dict type, got {type(connection)}.")
        cls.validate_plando_connections(value)
        return cls(value)

    def verify(self, world: typing.Type[World], player_name: str, plando_options: "PlandoOptions") -> None:
        from BaseClasses import PlandoOptions
        if self.value and not (PlandoOptions.connections & plando_options):
            # plando is disabled but plando options were given so overwrite the options
            self.value = []
            logging.warning(f"The plando connections module is turned off, "
                            f"so connections for {player_name} will be ignored.")

    @classmethod
    def get_option_name(cls, value: typing.List[PlandoConnection]) -> str:
        return ", ".join(["%s %s %s" % (connection.entrance,
                                        "<=>" if connection.direction == PlandoConnection.Direction.both else
                                        "<=" if connection.direction == PlandoConnection.Direction.exit else
                                        "=>",
                                        connection.exit) for connection in value])

    def __getitem__(self, index: typing.SupportsIndex) -> PlandoConnection:
        return self.value[index]

    def __iter__(self) -> typing.Iterator[PlandoConnection]:
        yield from self.value

    def __len__(self) -> int:
        return len(self.value)


class Accessibility(Choice):
    """
    Set rules for reachability of your items/locations.

    **Full:** ensure everything can be reached and acquired.

    **Minimal:** ensure what is needed to reach your goal can be acquired.
    """
    display_name = "Accessibility"
    rich_text_doc = True
    option_full = 0
    option_minimal = 2
    alias_none = 2
    alias_locations = 0
    alias_items = 0
    default = 0


class ItemsAccessibility(Accessibility):
    """
    Set rules for reachability of your items/locations.

    **Full:** ensure everything can be reached and acquired.

    **Minimal:** ensure what is needed to reach your goal can be acquired.

    **Items:** ensure all logically relevant items can be acquired. Some items, such as keys, may be self-locking, and
    some locations may be inaccessible.
    """
    option_items = 1
    default = 1


class ProgressionBalancing(NamedRange):
    """A system that can move progression earlier, to try and prevent the player from getting stuck and bored early.

    A lower setting means more getting stuck. A higher setting means less getting stuck.
    """
    default = 50
    range_start = 0
    range_end = 99
    display_name = "Progression Balancing"
    rich_text_doc = True
    special_range_names = {
        "disabled": 0,
        "normal": 50,
        "extreme": 99,
    }


class OptionsMetaProperty(type):
    def __new__(mcs,
                name: str,
                bases: typing.Tuple[type, ...],
                attrs: typing.Dict[str, typing.Any]) -> "OptionsMetaProperty":
        for attr_type in attrs.values():
            assert not isinstance(attr_type, AssembleOptions), \
                f"Options for {name} should be type hinted on the class, not assigned"
        return super().__new__(mcs, name, bases, attrs)

    @property
    @functools.lru_cache(maxsize=None)
    def type_hints(cls) -> typing.Dict[str, typing.Type[Option[typing.Any]]]:
        """Returns type hints of the class as a dictionary."""
        return typing.get_type_hints(cls)


@dataclass
class CommonOptions(metaclass=OptionsMetaProperty):
    progression_balancing: ProgressionBalancing
    accessibility: Accessibility

    def as_dict(
            self,
            *option_names: str,
            casing: typing.Literal["snake", "camel", "pascal", "kebab"] = "snake",
            toggles_as_bools: bool = False,
    ) -> dict[str, typing.Any]:
        """
        Returns a dictionary of [str, Option.value]

        :param option_names: Names of the options to get the values of.
        :param casing: Casing of the keys to return. Supports `snake`, `camel`, `pascal`, `kebab`.
        :param toggles_as_bools: Whether toggle options should be returned as bools instead of ints.

        :return: A dictionary of each option name to the value of its Option. If the option is an OptionSet, the value
        will be returned as a sorted list.
        """
        assert option_names, "options.as_dict() was used without any option names."
        assert len(option_names) < len(self.__class__.type_hints), "Specify only options you need."
        option_results = {}
        for option_name in option_names:
            if option_name not in type(self).type_hints:
                raise ValueError(f"{option_name} not found in {tuple(type(self).type_hints)}")

            if casing == "snake":
                display_name = option_name
            elif casing == "camel":
                split_name = [name.title() for name in option_name.split("_")]
                split_name[0] = split_name[0].lower()
                display_name = "".join(split_name)
            elif casing == "pascal":
                display_name = "".join([name.title() for name in option_name.split("_")])
            elif casing == "kebab":
                display_name = option_name.replace("_", "-")
            else:
                raise ValueError(f"{casing} is invalid casing for as_dict. "
                                 "Valid names are 'snake', 'camel', 'pascal', 'kebab'.")
            value = getattr(self, option_name).value
            if isinstance(value, set):
                value = sorted(value)
            elif toggles_as_bools and issubclass(type(self).type_hints[option_name], Toggle):
                value = bool(value)
            option_results[display_name] = value
        return option_results


class LocalItems(ItemSet):
    """Forces these items to be in their native world."""
    display_name = "Local Items"
    rich_text_doc = True


class NonLocalItems(ItemSet):
    """Forces these items to be outside their native world."""
    display_name = "Non-local Items"
    rich_text_doc = True


class StartInventory(ItemDict):
    """Start with the specified amount of these items. Example: "Bomb: 1" """
    verify_item_name = True
    display_name = "Start Inventory"
    rich_text_doc = True
    max = 10000


class StartInventoryPool(StartInventory):
    """Start with the specified amount of these items and don't place them in the world. Example: "Bomb: 1"

    The game decides what the replacement items will be.
    """
    verify_item_name = True
    display_name = "Start Inventory from Pool"
    rich_text_doc = True


class StartHints(ItemSet):
    """Start with these item's locations prefilled into the ``!hint`` command."""
    display_name = "Start Hints"
    rich_text_doc = True


class LocationSet(OptionSet):
    verify_location_name = True
    convert_name_groups = True


class StartLocationHints(LocationSet):
    """Start with these locations and their item prefilled into the ``!hint`` command."""
    display_name = "Start Location Hints"
    rich_text_doc = True


class ExcludeLocations(LocationSet):
    """Prevent these locations from having an important item."""
    display_name = "Excluded Locations"
    rich_text_doc = True


class PriorityLocations(LocationSet):
    """Prevent these locations from having an unimportant item."""
    display_name = "Priority Locations"
    rich_text_doc = True


class DeathLink(Toggle):
    """When you die, everyone who enabled death link dies. Of course, the reverse is true too."""
    display_name = "Death Link"
    rich_text_doc = True


class ItemLinks(OptionList):
    """Share part of your item pool with other players."""
    display_name = "Item Links"
    rich_text_doc = True
    default = []
    schema = Schema([
        {
            "name": And(str, len),
            "item_pool": [And(str, len)],
            Optional("exclude"): [And(str, len)],
            "replacement_item": Or(And(str, len), None),
            Optional("local_items"): [And(str, len)],
            Optional("non_local_items"): [And(str, len)],
            Optional("link_replacement"): Or(None, bool),
            Optional("skip_if_solo"): Or(None, bool),
        }
    ])

    @staticmethod
    def verify_items(items: typing.List[str], item_link: str, pool_name: str, world,
                     allow_item_groups: bool = True) -> typing.Set:
        pool = set()
        for item_name in items:
            if item_name not in world.item_names and (not allow_item_groups or item_name not in world.item_name_groups):
                picks = get_fuzzy_results(item_name, world.item_names, limit=1)
                picks_group = get_fuzzy_results(item_name, world.item_name_groups.keys(), limit=1)
                picks_group = f" or '{picks_group[0][0]}' ({picks_group[0][1]}% sure)" if allow_item_groups else ""

                raise Exception(f"Item '{item_name}' from item link '{item_link}' "
                                f"is not a valid item from '{world.game}' for '{pool_name}'. "
                                f"Did you mean '{picks[0][0]}' ({picks[0][1]}% sure){picks_group}")
            if allow_item_groups:
                pool |= world.item_name_groups.get(item_name, {item_name})
            else:
                pool |= {item_name}
        return pool

    def verify(self, world: typing.Type[World], player_name: str, plando_options: "PlandoOptions") -> None:
        link: dict
        super(ItemLinks, self).verify(world, player_name, plando_options)
        existing_links = set()
        for link in self.value:
            link["name"] = link["name"].strip()[:16].strip()
            if link["name"] in existing_links:
                raise Exception(f"Item link names are limited to their first 16 characters and must be unique. "
                                f"You have more than one link named '{link['name']}'.")
            existing_links.add(link["name"])

            pool = self.verify_items(link["item_pool"], link["name"], "item_pool", world)
            local_items = set()
            non_local_items = set()

            if "exclude" in link:
                pool -= self.verify_items(link["exclude"], link["name"], "exclude", world)
            if link["replacement_item"]:
                self.verify_items([link["replacement_item"]], link["name"], "replacement_item", world, False)
            if "local_items" in link:
                local_items = self.verify_items(link["local_items"], link["name"], "local_items", world)
                local_items &= pool
            if "non_local_items" in link:
                non_local_items = self.verify_items(link["non_local_items"], link["name"], "non_local_items", world)
                non_local_items &= pool

            intersection = local_items.intersection(non_local_items)
            if intersection:
                raise Exception(f"item_link {link['name']} has {intersection} "
                                f"items in both its local_items and non_local_items pool.")
            link.setdefault("link_replacement", None)
            link["item_pool"] = list(pool)


@dataclass(frozen=True)
class PlandoItem:
    items: list[str] | dict[str, typing.Any]
    locations: list[str]
    world: int | str | bool | None | typing.Iterable[str] | set[int] = False
    from_pool: bool = True
    force: bool | typing.Literal["silent"] = "silent"
    count: int | bool | dict[str, int] = False
    percentage: int = 100


class PlandoItems(Option[typing.List[PlandoItem]]):
    """Generic items plando."""
    default = ()
    supports_weighting = False
    display_name = "Plando Items"

    def __init__(self, value: typing.Iterable[PlandoItem]) -> None:
        self.value = list(deepcopy(value))
        super().__init__()

    @classmethod
    def from_any(cls, data: typing.Any) -> Option[typing.List[PlandoItem]]:
        if not isinstance(data, typing.Iterable):
            raise OptionError(f"Cannot create plando items from non-Iterable type, got {type(data)}")

        value: typing.List[PlandoItem] = []
        for item in data:
            if isinstance(item, typing.Mapping):
                percentage = item.get("percentage", 100)
                if not isinstance(percentage, int):
                    raise OptionError(f"Plando `percentage` has to be int, not {type(percentage)}.")
                if not (0 <= percentage <= 100):
                    raise OptionError(f"Plando `percentage` has to be between 0 and 100 (inclusive) not {percentage}.")
                if roll_percentage(percentage):
                    count = item.get("count", False)
                    items = item.get("items", [])
                    if not items:
                        items = item.get("item", None)  # explicitly throw an error here if not present
                        if not items:
                            raise OptionError("You must specify at least one item to place items with plando.")
                        count = 1
                    if isinstance(items, str):
                        items = [items]
                    elif not isinstance(items, (dict, list)):
                        raise OptionError(f"Plando 'items' has to be string, list, or "
                                          f"dictionary, not {type(items)}")
                    locations = item.get("locations", [])
                    if not locations:
                        locations = item.get("location", [])
                        if locations:
                            count = 1
                        else:
                            locations = ["Everywhere"]
                        if isinstance(locations, str):
                            locations = [locations]
                        if not isinstance(locations, list):
                            raise OptionError(f"Plando `location` has to be string or list, not {type(locations)}")
                    world = item.get("world", False)
                    from_pool = item.get("from_pool", True)
                    force = item.get("force", "silent")
                    if not isinstance(from_pool, bool):
                        raise OptionError(f"Plando 'from_pool' has to be true or false, not {from_pool!r}.")
                    if not (isinstance(force, bool) or force == "silent"):
                        raise OptionError(f"Plando `force` has to be true or false or `silent`, not {force!r}.")
                    value.append(PlandoItem(items, locations, world, from_pool, force, count, percentage))
            elif isinstance(item, PlandoItem):
                if roll_percentage(item.percentage):
                    value.append(item)
            else:
                raise OptionError(f"Cannot create plando item from non-Dict type, got {type(item)}.")
        return cls(value)

    def verify(self, world: typing.Type[World], player_name: str, plando_options: "PlandoOptions") -> None:
        if not self.value:
            return
        from BaseClasses import PlandoOptions
        if not (PlandoOptions.items & plando_options):
            # plando is disabled but plando options were given so overwrite the options
            self.value = []
            logging.warning(f"The plando items module is turned off, "
                            f"so items for {player_name} will be ignored.")
        else:
            # filter down item groups
            for plando in self.value:
                # confirm a valid count
                if isinstance(plando.count, dict):
                    if "min" in plando.count and "max" in plando.count:
                        if plando.count["min"] > plando.count["max"]:
                            raise OptionError("Plando cannot have count `min` greater than `max`.")
                items_copy = plando.items.copy()
                if isinstance(plando.items, dict):
                    for item in items_copy:
                        if item in world.item_name_groups:
                            value = plando.items.pop(item)
                            group = world.item_name_groups[item]
                            filtered_items = sorted(group.difference(list(plando.items.keys())))
                            if not filtered_items:
                                raise OptionError(f"Plando `items` contains the group \"{item}\" "
                                                  f"and every item in it. This is not allowed.")
                            if value is True:
                                for key in filtered_items:
                                    plando.items[key] = True
                            else:
                                for key in random.choices(filtered_items, k=value):
                                    plando.items[key] = plando.items.get(key, 0) + 1
                else:
                    assert isinstance(plando.items, list)  # pycharm can't figure out the hinting without the hint
                    for item in items_copy:
                        if item in world.item_name_groups:
                            plando.items.remove(item)
                            plando.items.extend(sorted(world.item_name_groups[item]))

    @classmethod
    def get_option_name(cls, value: list[PlandoItem]) -> str:
        return ", ".join(["(%s: %s)" % (item.items, item.locations) for item in value])  #TODO: see what a better way to display would be

    def __getitem__(self, index: typing.SupportsIndex) -> PlandoItem:
        return self.value.__getitem__(index)

    def __iter__(self) -> typing.Iterator[PlandoItem]:
        yield from self.value

    def __len__(self) -> int:
        return len(self.value)

        
class Removed(FreeText):
    """This Option has been Removed."""
    rich_text_doc = True
    default = ""
    visibility = Visibility.none

    def __init__(self, value: str):
        if value:
            raise Exception("Option removed, please update your options file.")
        super().__init__(value)


@dataclass
class PerGameCommonOptions(CommonOptions):
    local_items: LocalItems
    non_local_items: NonLocalItems
    start_inventory: StartInventory
    start_hints: StartHints
    start_location_hints: StartLocationHints
    exclude_locations: ExcludeLocations
    priority_locations: PriorityLocations
    item_links: ItemLinks
    plando_items: PlandoItems


@dataclass
class DeathLinkMixin:
    death_link: DeathLink


class OptionGroup(typing.NamedTuple):
    """Define a grouping of options."""
    name: str
    """Name of the group to categorize these options in for display on the WebHost and in generated YAMLS."""
    options: typing.List[typing.Type[Option[typing.Any]]]
    """Options to be in the defined group."""
    start_collapsed: bool = False
    """Whether the group will start collapsed on the WebHost options pages."""


item_and_loc_options = [LocalItems, NonLocalItems, StartInventory, StartInventoryPool, StartHints,
                        StartLocationHints, ExcludeLocations, PriorityLocations, ItemLinks, PlandoItems]
"""
Options that are always populated in "Item & Location Options" Option Group. Cannot be moved to another group.
If desired, a custom "Item & Location Options" Option Group can be defined, but only for adding additional options to
it.
"""


def get_option_groups(world: typing.Type[World], visibility_level: Visibility = Visibility.template) -> typing.Dict[
        str, typing.Dict[str, typing.Type[Option[typing.Any]]]]:
    """Generates and returns a dictionary for the option groups of a specified world."""
    option_to_name = {option: option_name for option_name, option in world.options_dataclass.type_hints.items()}

    ordered_groups = {group.name: group.options for group in world.web.option_groups}

    # add a default option group for uncategorized options to get thrown into
    if "Game Options" not in ordered_groups:
        grouped_options = set(option for group in ordered_groups.values() for option in group)
        ungrouped_options = [option for option in option_to_name if option not in grouped_options]
        # only add the game options group if we have ungrouped options
        if ungrouped_options:
            ordered_groups = {**{"Game Options": ungrouped_options}, **ordered_groups}

    return {
        group: {
            option_to_name[option]: option
            for option in group_options
            if (visibility_level in option.visibility and option in option_to_name)
        }
        for group, group_options in ordered_groups.items()
    }


def generate_yaml_templates(target_folder: typing.Union[str, "pathlib.Path"], generate_hidden: bool = True) -> None:
    import os
    from inspect import cleandoc

    import yaml
    from jinja2 import Template

    from worlds import AutoWorldRegister
    from Utils import local_path, __version__

    full_path: str

    os.makedirs(target_folder, exist_ok=True)

    # clean out old
    for file in os.listdir(target_folder):
        full_path = os.path.join(target_folder, file)
        if os.path.isfile(full_path) and full_path.endswith(".yaml"):
            os.unlink(full_path)

    def dictify_range(option: Range):
        data = {option.default: 50}
        for sub_option in ["random", "random-low", "random-high"]:
            if sub_option != option.default:
                data[sub_option] = 0

        notes = {}
        for name, number in getattr(option, "special_range_names", {}).items():
            notes[name] = f"equivalent to {number}"
            if number in data:
                data[name] = data[number]
                del data[number]
            else:
                data[name] = 0

        return data, notes

    def yaml_dump_scalar(scalar) -> str:
        # yaml dump may add end of document marker and newlines.
        return yaml.dump(scalar).replace("...\n", "").strip()

    with open(local_path("data", "options.yaml")) as f:
        file_data = f.read()
    template = Template(file_data)

    for game_name, world in AutoWorldRegister.world_types.items():
        if not world.hidden or generate_hidden:
            option_groups = get_option_groups(world)

            res = template.render(
                option_groups=option_groups,
                __version__=__version__,
                game=game_name,
                world_version=world.world_version.as_simple_string(),
                yaml_dump=yaml_dump_scalar,
                dictify_range=dictify_range,
                cleandoc=cleandoc,
            )

            with open(os.path.join(target_folder, get_file_safe_name(game_name) + ".yaml"), "w", encoding="utf-8-sig") as f:
                f.write(res)


def dump_player_options(multiworld: MultiWorld) -> None:
    from csv import DictWriter

    game_players = defaultdict(list)
    for player, game in multiworld.game.items():
        game_players[game].append(player)
    game_players = dict(sorted(game_players.items()))

    output = []
    per_game_option_names = [
        getattr(option, "display_name", option_key)
        for option_key, option in PerGameCommonOptions.type_hints.items()
    ]
    all_option_names = per_game_option_names.copy()
    for game, players in game_players.items():
        game_option_names = per_game_option_names.copy()
        for player in players:
            world = multiworld.worlds[player]
            player_output = {
                "Game": multiworld.game[player],
                "Name": multiworld.get_player_name(player),
                "ID": player,
            }
            output.append(player_output)
            for option_key, option in world.options_dataclass.type_hints.items():
                if option.visibility == Visibility.none:
                    continue
                display_name = getattr(option, "display_name", option_key)
                player_output[display_name] = getattr(world.options, option_key).current_option_name
                if display_name not in game_option_names:
                    all_option_names.append(display_name)
                    game_option_names.append(display_name)

    with open(output_path(f"generate_{multiworld.seed_name}.csv"), mode="w", newline="") as file:
        fields = ["ID", "Game", "Name", *all_option_names]
        writer = DictWriter(file, fields)
        writer.writeheader()
        writer.writerows(output)
