# Common utilities for outputting binary data for the patches, and shuffling stat values.

import inspect
import random
import re

# Amount to boost very small values when shuffling to give a bit more range for very small values.
SMALL_BOOST_AMOUNT = 2.0


def isclass_or_instance(obj_or_cls, classinfo):
    """Helper function to check if an object is an instance of a class, or the class itself."""
    return isinstance(obj_or_cls, classinfo) or (inspect.isclass(obj_or_cls) and issubclass(obj_or_cls, classinfo))


class BitMapSet(set):
    """A class representing a bitmap of a certain length using the set built-in type to track which bits are set."""

    def __init__(self, num_bytes=1, *args, **kwargs):
        """
        :type num_bytes: int
        """
        super().__init__(*args, **kwargs)
        self._num_bytes = num_bytes

    def as_bytes(self):
        """Return bitmap in little endian byte format for ROM patching.

        :rtype: bytearray
        """
        result = 0
        for value in self:
            result |= (1 << value)
        return result.to_bytes(self._num_bytes, 'little')

    def __str__(self):
        return "BitMapSet({})".format(super().__str__())


class ByteField:
    """Base class for an integer value field spanning one or more bytes."""

    def __init__(self, value, num_bytes=1):
        """
        :type value: int
        :type num_bytes: int
        """
        self._value = value
        self._num_bytes = num_bytes

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = int(value)

    def as_bytes(self):
        """Return current value of this stat as a little-endian byte array for the patch.  If the value is less than
        zero, convert this to a signed int in byte format.

        :rtype: bytearray
        """
        if self._value < 0:
            val = self._value + (2 ** (self._num_bytes * 8))
        else:
            val = self._value
        return val.to_bytes(self._num_bytes, 'little')

    def __str__(self):
        return "ByteField(current value: {}, number of bytes: {}".format(self.value, self._num_bytes)


class Mutator:
    """Mutator class that shuffles stat attributes based on min/max values and a difficulty setting."""

    def __init__(self, difficulty=None):
        # Placeholder for future difficulty option.
        self.difficulty = difficulty

    def mutate_normal(self, value, minimum=0, maximum=0xff):
        """Mutate a value with a given range.
        This is roughly simulating a normal distribution with mean <value>, std deviation approx 1/5 <value>.
        """
        # The actual value we're shuffling is the difference between the default value and the minimum or maximum,
        # whichever is smaller.  Shuffle this distance value, then recompute the new actual value below.
        value = max(minimum, min(value, maximum))
        if value > (minimum + maximum) / 2:
            reverse = True
        else:
            reverse = False

        if reverse:
            value = maximum - value
        else:
            value = value - minimum

        # For very small values, give a small boost amount to allow for a bit more variance.  Subtract this later.
        boosted = False
        if value < SMALL_BOOST_AMOUNT:
            value += SMALL_BOOST_AMOUNT
            if value > 0:
                boosted = True
            else:
                value = 0

        # Make new random value.
        if value > 0:
            half = value / 2.0
            a, b = random.random(), random.random()
            value = half + (half * a) + (half * b)

        # If we boosted the value, bring it back down now.
        if boosted:
            value -= SMALL_BOOST_AMOUNT

        # Compute actual final value with new distance from minimum/maximum.
        if reverse:
            value = maximum - value
        else:
            value = value + minimum

        # 1/10 chance to chain mutate for more variance.
        if random.randint(1, 10) == 10:
            return self.mutate_normal(value, minimum=minimum, maximum=maximum)
        else:
            value = max(minimum, min(value, maximum))
            value = int(round(value))
            return value


class _GlobalMutator:
    """Container class for the global mutator instance so we can control the difficulty."""
    mutator = Mutator()

    @classmethod
    def get_mutator(cls):
        return cls.mutator

    @classmethod
    def set_difficulty(cls, difficulty):
        cls.mutator.difficulty = difficulty


def mutate_normal(value, minimum=0, maximum=0xff):
    """Mutate a stat value using the global mutator."""
    return _GlobalMutator.get_mutator().mutate_normal(value, minimum, maximum)


def set_difficulty(difficulty):
    """Set the difficulty level for the global mutator that shuffles stats."""
    _GlobalMutator.set_difficulty(difficulty)


def coin_flip(odds=0.5):
    """Weighted coin flip with odds."""
    return random.random() < odds


def add_desc_fields(fields):
    d = ''
    for chars, flag, attr in fields:
        if isinstance(attr, (list, tuple)):
            if flag in attr:
                d += chars
            else:
                d += '\x20'
        elif isinstance(attr, bool):
            if attr:
                d += chars
            else:
                d += '\x20'
    return d


def split_camel_case(string):
    """

    Args:
        string: String to split.

    Returns:
        str: Camel case string split out with spaces in between words.

    """
    return re.sub(r'(?!^)([A-Z0-9][a-z]*)', r' \1', string)
