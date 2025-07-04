import random
import typing

from Options import FreeText, NumericOption


class FloatRangeText(FreeText, NumericOption):
    """FreeText option optimized for entering float numbers.
    Supports everything that Range supports.
    range_start and range_end have to be floats, while default has to be a string."""

    default = "0.0"
    value: float
    range_start: float = 0.0
    range_end: float = 1.0

    def __init__(self, value: str):
        super().__init__(value)
        value = value.lower()
        if value.startswith("random"):
            self.value = self.weighted_range(value)
        elif value == "default" and hasattr(self, "default"):
            self.value = float(self.default)
        elif value == "high":
            self.value = self.range_end
        elif value == "low":
            self.value = self.range_start
        elif self.range_start == 0.0 \
                and hasattr(self, "default") \
                and self.default != "0.0" \
                and value in ("true", "false"):
            # these are the conditions where "true" and "false" make sense
            if value == "true":
                self.value = float(self.default)
            else:  # "false"
                self.value = 0.0
        else:
            try:
                self.value = float(value)
            except ValueError:
                raise Exception(f"Invalid value for option {self.__class__.__name__}: {value}")
            except OverflowError:
                raise Exception(f"Out of range floating value for option {self.__class__.__name__}: {value}")
            if self.value < self.range_start:
                raise Exception(f"{value} is lower than minimum {self.range_start} for option {self.__class__.__name__}")
            if self.value > self.range_end:
                raise Exception(f"{value} is higher than maximum {self.range_end} for option {self.__class__.__name__}")

    @classmethod
    def from_text(cls, text: str) -> typing.Any:
        return cls(text)

    @classmethod
    def weighted_range(cls, text: str) -> float:
        if text == "random-low":
            return random.triangular(cls.range_start, cls.range_end, cls.range_start)
        elif text == "random-high":
            return random.triangular(cls.range_start, cls.range_end, cls.range_end)
        elif text == "random-middle":
            return random.triangular(cls.range_start, cls.range_end)
        elif text.startswith("random-range-"):
            return cls.custom_range(text)
        elif text == "random":
            return random.uniform(cls.range_start, cls.range_end)
        else:
            raise Exception(f"random text \"{text}\" did not resolve to a recognized pattern. "
                            f"Acceptable values are: random, random-high, random-middle, random-low, "
                            f"random-range-low-<min>-<max>, random-range-middle-<min>-<max>, "
                            f"random-range-high-<min>-<max>, or random-range-<min>-<max>.")

    @classmethod
    def custom_range(cls, text: str) -> float:
        textsplit = text.split("-")
        try:
            random_range = [float(textsplit[len(textsplit) - 2]), float(textsplit[len(textsplit) - 1])]
        except ValueError:
            raise ValueError(f"Invalid random range {text} for option {cls.__name__}")
        except OverflowError:
            raise Exception(f"Out of range floating value for option {cls.__name__}: {text}")
        random_range.sort()
        if random_range[0] < cls.range_start or random_range[1] > cls.range_end:
            raise Exception(
                f"{random_range[0]}-{random_range[1]} is outside allowed range "
                f"{cls.range_start}-{cls.range_end} for option {cls.__name__}")
        if text.startswith("random-range-low"):
            return random.triangular(random_range[0], random_range[1], random_range[0])
        elif text.startswith("random-range-middle"):
            return random.triangular(random_range[0], random_range[1])
        elif text.startswith("random-range-high"):
            return random.triangular(random_range[0], random_range[1], random_range[1])
        else:
            return random.uniform(random_range[0], random_range[1])

    @property
    def current_key(self) -> str:
        return str(self.value)

    @classmethod
    def get_option_name(cls, value: float) -> str:
        return str(value)

    def __eq__(self, other: typing.Any):
        if isinstance(other, NumericOption):
            return self.value == other.value
        else:
            return typing.cast(bool, self.value == other)

    def __lt__(self, other: typing.Union[int, float, NumericOption]) -> bool:
        if isinstance(other, NumericOption):
            return self.value < other.value
        else:
            return self.value < other

    def __le__(self, other: typing.Union[int, float, NumericOption]) -> bool:
        if isinstance(other, NumericOption):
            return self.value <= other.value
        else:
            return self.value <= other

    def __gt__(self, other: typing.Union[int, float, NumericOption]) -> bool:
        if isinstance(other, NumericOption):
            return self.value > other.value
        else:
            return self.value > other

    def __ge__(self, other: typing.Union[int, float, NumericOption]) -> bool:
        if isinstance(other, NumericOption):
            return self.value >= other.value
        else:
            return self.value >= other

    def __int__(self) -> int:
        return int(self.value)

    def __and__(self, other: typing.Any) -> int:
        raise TypeError("& operator not supported for float values")

    def __floordiv__(self, other: typing.Any) -> int:
        return int(self.value // float(other))

    def __invert__(self) -> int:
        raise TypeError("~ operator not supported for float values")

    def __lshift__(self, other: typing.Any) -> int:
        raise TypeError("<< operator not supported for float values")

    def __mod__(self, other: typing.Any) -> float:
        return self.value % float(other)

    def __neg__(self) -> float:
        return -self.value

    def __or__(self, other: typing.Any) -> int:
        raise TypeError("| operator not supported for float values")

    def __pos__(self) -> float:
        return +self.value

    def __rand__(self, other: typing.Any) -> int:
        raise TypeError("& operator not supported for float values")

    def __rfloordiv__(self, other: typing.Any) -> int:
        return int(float(other) // self.value)

    def __rlshift__(self, other: typing.Any) -> int:
        raise TypeError("<< operator not supported for float values")

    def __rmod__(self, other: typing.Any) -> float:
        return float(other) % self.value

    def __ror__(self, other: typing.Any) -> int:
        raise TypeError("| operator not supported for float values")

    def __round__(self, ndigits: typing.Optional[int] = None) -> float:
        return round(self.value, ndigits)

    def __rpow__(self, base: typing.Any) -> typing.Any:
        return base ** self.value

    def __rrshift__(self, other: typing.Any) -> int:
        raise TypeError(">> operator not supported for float values")

    def __rshift__(self, other: typing.Any) -> int:
        raise TypeError(">> operator not supported for float values")

    def __rxor__(self, other: typing.Any) -> int:
        raise TypeError("^ operator not supported for float values")

    def __xor__(self, other: typing.Any) -> int:
        raise TypeError("^ operator not supported for float values")
