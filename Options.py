from __future__ import annotations

import abc
import logging
from copy import deepcopy
from dataclasses import dataclass
import functools
import math
import numbers
import random
import typing
from copy import deepcopy

from schema import And, Optional, Or, Schema

from Utils import get_fuzzy_results

if typing.TYPE_CHECKING:
    from BaseClasses import PlandoOptions
    from worlds.AutoWorld import World
    import pathlib


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
        aliases = {name[6:].lower(): option_id for name, option_id in attrs.items() if
                   name.startswith("alias_")}

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
    default = 0

    # convert option_name_long into Name Long as display_name, otherwise name_long is the result.
    # Handled in get_option_name()
    auto_display_name = False

    # can be weighted between selections
    supports_weighting = True

    # filled by AssembleOptions:
    name_lookup: typing.Dict[T, str]
    options: typing.Dict[str, int]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.current_option_name})"

    def __hash__(self) -> int:
        return hash(self.value)

    @property
    def current_key(self) -> str:
        return self.name_lookup[self.value]

    def get_current_option_name(self) -> str:
        """Deprecated. use current_option_name instead. TODO remove around 0.4"""
        logging.warning(DeprecationWarning(f"get_current_option_name for {self.__class__.__name__} is deprecated."
                                           f" use current_option_name instead. Worlds should use {self}.current_key"))
        return self.current_option_name

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
        assert value == 0 or value == 1, "value of Toggle can only be 0 or 1"
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

    __hash__ = Option.__hash__  # see https://docs.python.org/3/reference/datamodel.html#object.__hash__


class TextChoice(Choice):
    """Allows custom string input and offers choices. Choices will resolve to int and text will resolve to string"""
    value: typing.Union[str, int]

    def __init__(self, value: typing.Union[str, int]):
        assert isinstance(value, str) or isinstance(value, int), \
            f"{value} is not a valid option for {self.__class__.__name__}"
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
                    raise ValueError(f"{boss.title()} is not a valid boss name.")
                if not cls.valid_location_name(location):
                    raise ValueError(f"{location.title()} is not a valid boss location name.")
                if not cls.can_place_boss(boss, location):
                    raise ValueError(f"{location.title()} is not a valid location for {boss.title()} to be placed.")
            else:
                if cls.duplicate_bosses:
                    if not cls.valid_boss_name(option):
                        raise ValueError(f"{option} is not a valid boss name.")
                else:
                    raise ValueError(f"{option.title()} is not formatted correctly.")

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
        if not(PlandoOptions.bosses & plando_options):
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
            return cls(cls.triangular(cls.range_start, cls.range_end, cls.range_start))
        elif text == "random-high":
            return cls(cls.triangular(cls.range_start, cls.range_end, cls.range_end))
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
            return cls(cls.triangular(random_range[0], random_range[1], random_range[0]))
        elif text.startswith("random-range-middle"):
            return cls(cls.triangular(random_range[0], random_range[1]))
        elif text.startswith("random-range-high"):
            return cls(cls.triangular(random_range[0], random_range[1], random_range[1]))
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
    def triangular(lower: int, end: int, tri: typing.Optional[int] = None) -> int:
        return int(round(random.triangular(lower, end, tri), 0))


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
        self.value = value

    @classmethod
    def from_text(cls, text: str) -> Range:
        text = text.lower()
        if text in cls.special_range_names:
            return cls(cls.special_range_names[text])
        return super().from_text(text)


class SpecialRange(NamedRange):
    special_range_cutoff = 0

    # TODO: remove class SpecialRange, earliest 3 releases after 0.4.3
    def __new__(cls, value: int) -> SpecialRange:
        from Utils import deprecate
        deprecate(f"Option type {cls.__name__} is a subclass of SpecialRange, which is deprecated and pending removal. "
                  "Consider switching to NamedRange, which supports all use-cases of SpecialRange, and more. In "
                  "NamedRange, range_start specifies the lower end of the regular range, while special values can be "
                  "placed anywhere (below, inside, or above the regular range).")
        return super().__new__(cls, value)

    @classmethod
    def weighted_range(cls, text) -> Range:
        if text == "random-low":
            return cls(cls.triangular(cls.special_range_cutoff, cls.range_end, cls.special_range_cutoff))
        elif text == "random-high":
            return cls(cls.triangular(cls.special_range_cutoff, cls.range_end, cls.range_end))
        elif text == "random-middle":
            return cls(cls.triangular(cls.special_range_cutoff, cls.range_end))
        elif text.startswith("random-range-"):
            return cls.custom_range(text)
        elif text == "random":
            return cls(random.randint(cls.special_range_cutoff, cls.range_end))
        else:
            raise Exception(f"random text \"{text}\" did not resolve to a recognized pattern. "
                            f"Acceptable values are: random, random-high, random-middle, random-low, "
                            f"random-range-low-<min>-<max>, random-range-middle-<min>-<max>, "
                            f"random-range-high-<min>-<max>, or random-range-<min>-<max>.")


class FreezeValidKeys(AssembleOptions):
    def __new__(mcs, name, bases, attrs):
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

    @classmethod
    def verify_keys(cls, data: typing.List[str]):
        if cls.valid_keys:
            data = set(data)
            dataset = set(word.casefold() for word in data) if cls.valid_keys_casefold else set(data)
            extra = dataset - cls._valid_keys
            if extra:
                raise Exception(f"Found unexpected key {', '.join(extra)} in {cls}. "
                                f"Allowed keys: {cls._valid_keys}.")

    def verify(self, world: typing.Type[World], player_name: str, plando_options: "PlandoOptions") -> None:
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
                    raise Exception(f"Item {item_name} from option {self} "
                                    f"is not a valid item name from {world.game}. "
                                    f"Did you mean '{picks[0][0]}' ({picks[0][1]}% sure)")
        elif self.verify_location_name:
            for location_name in self.value:
                if location_name not in world.location_names:
                    picks = get_fuzzy_results(location_name, world.location_names, limit=1)
                    raise Exception(f"Location {location_name} from option {self} "
                                    f"is not a valid location name from {world.game}. "
                                    f"Did you mean '{picks[0][0]}' ({picks[0][1]}% sure)")


class OptionDict(Option[typing.Dict[str, typing.Any]], VerifyKeys, typing.Mapping[str, typing.Any]):
    default: typing.Dict[str, typing.Any] = {}
    supports_weighting = False

    def __init__(self, value: typing.Dict[str, typing.Any]):
        self.value = deepcopy(value)

    @classmethod
    def from_any(cls, data: typing.Dict[str, typing.Any]) -> OptionDict:
        if type(data) == dict:
            cls.verify_keys(data)
            return cls(data)
        else:
            raise NotImplementedError(f"Cannot Convert from non-dictionary, got {type(data)}")

    def get_option_name(self, value):
        return ", ".join(f"{key}: {v}" for key, v in value.items())

    def __getitem__(self, item: str) -> typing.Any:
        return self.value.__getitem__(item)

    def __iter__(self) -> typing.Iterator[str]:
        return self.value.__iter__()

    def __len__(self) -> int:
        return self.value.__len__()


class ItemDict(OptionDict):
    verify_item_name = True

    def __init__(self, value: typing.Dict[str, int]):
        if any(item_count < 1 for item_count in value.values()):
            raise Exception("Cannot have non-positive item counts.")
        super(ItemDict, self).__init__(value)


class OptionList(Option[typing.List[typing.Any]], VerifyKeys):
    # Supports duplicate entries and ordering.
    # If only unique entries are needed and input order of elements does not matter, OptionSet should be used instead.
    # Not a docstring so it doesn't get grabbed by the options system.

    default: typing.List[typing.Any] = []
    supports_weighting = False

    def __init__(self, value: typing.List[typing.Any]):
        self.value = deepcopy(value)
        super(OptionList, self).__init__()

    @classmethod
    def from_text(cls, text: str):
        return cls([option.strip() for option in text.split(",")])

    @classmethod
    def from_any(cls, data: typing.Any):
        if type(data) == list:
            cls.verify_keys(data)
            return cls(data)
        return cls.from_text(str(data))

    def get_option_name(self, value):
        return ", ".join(map(str, value))

    def __contains__(self, item):
        return item in self.value


class OptionSet(Option[typing.Set[str]], VerifyKeys):
    default: typing.Union[typing.Set[str], typing.FrozenSet[str]] = frozenset()
    supports_weighting = False

    def __init__(self, value: typing.Iterable[str]):
        self.value = set(deepcopy(value))
        super(OptionSet, self).__init__()

    @classmethod
    def from_text(cls, text: str):
        return cls([option.strip() for option in text.split(",")])

    @classmethod
    def from_any(cls, data: typing.Any):
        if isinstance(data, (list, set, frozenset)):
            cls.verify_keys(data)
            return cls(data)
        return cls.from_text(str(data))

    def get_option_name(self, value):
        return ", ".join(sorted(value))

    def __contains__(self, item):
        return item in self.value


class ItemSet(OptionSet):
    verify_item_name = True
    convert_name_groups = True


class Accessibility(Choice):
    """Set rules for reachability of your items/locations.
    Locations: ensure everything can be reached and acquired.
    Items: ensure all logically relevant items can be acquired.
    Minimal: ensure what is needed to reach your goal can be acquired."""
    display_name = "Accessibility"
    option_locations = 0
    option_items = 1
    option_minimal = 2
    alias_none = 2
    default = 1


class ProgressionBalancing(NamedRange):
    """A system that can move progression earlier, to try and prevent the player from getting stuck and bored early.
    A lower setting means more getting stuck. A higher setting means less getting stuck."""
    default = 50
    range_start = 0
    range_end = 99
    display_name = "Progression Balancing"
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
            assert not isinstance(attr_type, AssembleOptions),\
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

    def as_dict(self, *option_names: str, casing: str = "snake") -> typing.Dict[str, typing.Any]:
        """
        Returns a dictionary of [str, Option.value]
        
        :param option_names: names of the options to return
        :param casing: case of the keys to return. Supports `snake`, `camel`, `pascal`, `kebab`
        """
        option_results = {}
        for option_name in option_names:
            if option_name in type(self).type_hints:
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
                option_results[display_name] = value
            else:
                raise ValueError(f"{option_name} not found in {tuple(type(self).type_hints)}")
        return option_results


class LocalItems(ItemSet):
    """Forces these items to be in their native world."""
    display_name = "Local Items"


class NonLocalItems(ItemSet):
    """Forces these items to be outside their native world."""
    display_name = "Not Local Items"


class StartInventory(ItemDict):
    """Start with these items."""
    verify_item_name = True
    display_name = "Start Inventory"


class StartInventoryPool(StartInventory):
    """Start with these items and don't place them in the world.
    The game decides what the replacement items will be."""
    verify_item_name = True
    display_name = "Start Inventory from Pool"


class StartHints(ItemSet):
    """Start with these item's locations prefilled into the !hint command."""
    display_name = "Start Hints"


class LocationSet(OptionSet):
    verify_location_name = True
    convert_name_groups = True


class StartLocationHints(LocationSet):
    """Start with these locations and their item prefilled into the !hint command"""
    display_name = "Start Location Hints"


class ExcludeLocations(LocationSet):
    """Prevent these locations from having an important item"""
    display_name = "Excluded Locations"


class PriorityLocations(LocationSet):
    """Prevent these locations from having an unimportant item"""
    display_name = "Priority Locations"


class DeathLink(Toggle):
    """When you die, everyone dies. Of course the reverse is true too."""
    display_name = "Death Link"


class ItemLinks(OptionList):
    """Share part of your item pool with other players."""
    display_name = "Item Links"
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
        }
    ])

    @staticmethod
    def verify_items(items: typing.List[str], item_link: str, pool_name: str, world, allow_item_groups: bool = True) -> typing.Set:
        pool = set()
        for item_name in items:
            if item_name not in world.item_names and (not allow_item_groups or item_name not in world.item_name_groups):
                picks = get_fuzzy_results(item_name, world.item_names, limit=1)
                picks_group = get_fuzzy_results(item_name, world.item_name_groups.keys(), limit=1)
                picks_group = f" or '{picks_group[0][0]}' ({picks_group[0][1]}% sure)" if allow_item_groups else ""

                raise Exception(f"Item {item_name} from item link {item_link} "
                                f"is not a valid item from {world.game} for {pool_name}. "
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
            if link["name"] in existing_links:
                raise Exception(f"You cannot have more than one link named {link['name']}.")
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


def generate_yaml_templates(target_folder: typing.Union[str, "pathlib.Path"], generate_hidden: bool = True):
    import os

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

    for game_name, world in AutoWorldRegister.world_types.items():
        if not world.hidden or generate_hidden:
            all_options: typing.Dict[str, AssembleOptions] = world.options_dataclass.type_hints

            with open(local_path("data", "options.yaml")) as f:
                file_data = f.read()
            res = Template(file_data).render(
                options=all_options,
                __version__=__version__, game=game_name, yaml_dump=yaml.dump,
                dictify_range=dictify_range,
            )

            del file_data

            with open(os.path.join(target_folder, game_name + ".yaml"), "w", encoding="utf-8-sig") as f:
                f.write(res)


if __name__ == "__main__":

    from worlds.alttp.Options import Logic
    import argparse

    map_shuffle = Toggle
    compass_shuffle = Toggle
    key_shuffle = Toggle
    big_key_shuffle = Toggle
    hints = Toggle
    test = argparse.Namespace()
    test.logic = Logic.from_text("no_logic")
    test.map_shuffle = map_shuffle.from_text("ON")
    test.hints = hints.from_text('OFF')
    try:
        test.logic = Logic.from_text("overworld_glitches_typo")
    except KeyError as e:
        print(e)
    try:
        test.logic_owg = Logic.from_text("owg")
    except KeyError as e:
        print(e)
    if test.map_shuffle:
        print("map_shuffle is on")
    print(f"Hints are {bool(test.hints)}")
    print(test)
