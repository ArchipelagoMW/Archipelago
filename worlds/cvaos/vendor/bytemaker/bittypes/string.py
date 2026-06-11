from __future__ import annotations

import re
from abc import abstractmethod
from typing import TYPE_CHECKING

from bytemaker.bittypes.bittype import BitType
from bytemaker.bitvector import BitVector
from bytemaker.typing_redirect import Optional, Tuple, TypeVar
from bytemaker.utils import FrozenDict, HashableMapping, classproperty

if TYPE_CHECKING:
    StrSelf = TypeVar("StrSelf", bound="String")
else:
    try:
        from typing_redirect import Self as StrSelf
    except ImportError:
        StrSelf = TypeVar("StrSelf", bound="String")


class String(BitType[str]):
    py_type = str
    _codepoint_changes: Optional[
        HashableMapping[BitVector, BitVector] | HashableMapping[str, str]
    ] = None
    _codepoint_changes_cache: Optional[Tuple[int, HashableMapping[str, str]]] = None
    _reverse_codepoint_changes_cache: Optional[
        Tuple[int, HashableMapping[str, str]]
    ] = None
    _codepoint_change_regex_cache: Optional[Tuple[int, re.Pattern[str]]] = None
    _reverse_codepoint_changes_regex_cache: Optional[Tuple[int, re.Pattern[str]]] = None

    @classmethod
    @abstractmethod
    def encoding(cls, value: str) -> BitVector:
        """
        The method used to encode a string into a BitVector.

        Args:
            value (str): The string to encode into a BitVector

        Returns:
            BitVector: The encoded BitVector representation of the input string
        """

    @classmethod
    @abstractmethod
    def decoding(cls, bits: BitVector) -> str:
        """
        The method used to decode a BitVector into a string.

        Args:
            bits (BitVector): The BitVector to decode into a string

        Returns:
            str: The decoded string representation of the input BitVector
        """

    @classproperty
    @classmethod
    def codepoint_changes(cls) -> Optional[HashableMapping[str, str]]:
        """
        A classproperty that gives this class's optional codepoint changes.
        Set this with a str->str mapping or a BitVector -> BitVector mapping
        to have substitutions applied when converting between the
        underlying BitVector bits and str value representations of this class.

        TODO: Add support for sub-byte codepoint changes

        Returns:
            Optional[HashableMapping[str, str]]: The codepoint changes mapping
        """
        if cls._codepoint_changes is None:
            return None
        if cls._codepoint_changes_cache and cls._codepoint_changes_cache[0] == hash(
            cls._codepoint_changes
        ):
            return cls._codepoint_changes_cache[1]

        codepoint_changes_field = cls._codepoint_changes
        if len(codepoint_changes_field) > 0:
            if isinstance(
                codepoint_changes_field.items().__iter__().__next__()[0], BitVector
            ):
                codepoint_changes_field = FrozenDict(
                    {
                        cls.decoding(k): cls.decoding(v)
                        for k, v in codepoint_changes_field.items()
                    }
                )

        cls._codepoint_changes_cache = (
            hash(cls._codepoint_changes),
            codepoint_changes_field,
        )  # type: ignore[reportAttributeAccessIssue]
        return cls._codepoint_changes_cache[1]

    @classproperty
    @classmethod
    def _reverse_codepoint_changes(cls) -> Optional[HashableMapping[str, str]]:
        if cls._codepoint_changes is None:
            return None
        if cls._reverse_codepoint_changes_cache and (
            cls._reverse_codepoint_changes_cache[0] == hash(cls._codepoint_changes)
        ):
            return cls._reverse_codepoint_changes_cache[1]

        codepoint_changes = cls.codepoint_changes
        reverse_codepoint_changes = FrozenDict(
            {v: k for k, v in codepoint_changes.items()}
        )
        cls._reverse_codepoint_changes_cache = (
            hash(cls._codepoint_changes),
            reverse_codepoint_changes,
        )
        return cls._reverse_codepoint_changes_cache[1]

    @classproperty
    @classmethod
    def _codepoint_change_regex(cls) -> Optional[re.Pattern]:
        if cls.codepoint_changes:
            if cls._codepoint_change_regex_cache and cls._codepoint_change_regex_cache[
                0
            ] == hash(cls.codepoint_changes):
                return cls._codepoint_change_regex_cache[1]
            else:
                cls._codepoint_change_regex_cache = (
                    hash(cls.codepoint_changes),
                    re.compile(
                        "|".join(re.escape(key) for key in cls.codepoint_changes.keys())
                    ),
                )
            return cls._codepoint_change_regex_cache[1]
        return None

    @classproperty
    @classmethod
    def _reverse_codepoint_change_regex(cls) -> Optional[re.Pattern]:
        if cls.codepoint_changes:
            if cls._reverse_codepoint_changes_regex_cache and (
                cls._reverse_codepoint_changes_regex_cache[0]
                == hash(cls.codepoint_changes)
            ):
                return cls._reverse_codepoint_changes_regex_cache[1]
            else:
                cls._reverse_codepoint_changes_regex_cache = (
                    hash(cls.codepoint_changes),
                    re.compile(
                        "|".join(
                            re.escape(key) for key in cls.codepoint_changes.values()
                        )
                    ),
                )
            return cls._reverse_codepoint_changes_regex_cache[1]
        return None

    @codepoint_changes.setter
    @classmethod
    def codepoint_changes(
        cls, value: HashableMapping[BitVector, BitVector] | HashableMapping[str, str]
    ):
        if len(value) > 0:
            if isinstance(value.items().__iter__().__next__()[0], BitVector):
                value = FrozenDict(
                    {cls.decoding(k): cls.decoding(v) for k, v in value.items()}
                )

        cls._codepoint_changes = value

    @classmethod
    def perform_codepoint_substitution(
        cls,
        input_string,
        codepoint_changes: HashableMapping[str, str],
        changes_regex: re.Pattern[str],
    ):
        """
        Performs codepoint substitutions on the input string.

        Args:
            input_string (str): The input string to perform substitutions on
            codepoint_changes (HashableMapping[str, str]): The codepoint changes mapping
            changes_regex (re.Pattern[str]): The compiled
                regex pattern for the codepoint changes

        Returns:
            str: The input string with codepoint substitutions applied
        """
        return changes_regex.sub(
            lambda match: codepoint_changes[match.group(0)], input_string
        )

    @property
    def value(self):
        temp_value = self.decoding(self.bits)
        codepoint_changes = self.codepoint_changes
        if codepoint_changes is not None:
            codepoint_changes_regex: re.Pattern[str] = self._codepoint_change_regex
            temp_value = self.perform_codepoint_substitution(
                temp_value, codepoint_changes, codepoint_changes_regex
            )
        return temp_value

    @value.setter
    def value(self, value):
        temp_value = value
        reverse_codepoint_changes = self._reverse_codepoint_changes
        if reverse_codepoint_changes is not None:
            reverse_codepoint_changes_regex: re.Pattern[str] = (
                self._reverse_codepoint_change_regex
            )
            temp_value = self.perform_codepoint_substitution(
                temp_value, reverse_codepoint_changes, reverse_codepoint_changes_regex
            )
        self.bits = self.encoding(temp_value)

    @classmethod
    def specialize(cls, num_bits_: int, name_: Optional[str] = None):
        class _String(cls):
            _num_bits = num_bits_

        if name_:
            _String.__name__ = name_

        return _String


String.base_bit_type = String


class StandardEncodingString(String):
    """
    A class for strings that use a standard Python encoding (str.encode/decode)
    """

    py_type = str
    encoding_name: str
    """The name of the Python-supported encoding to use for encoding/decoding."""

    @classmethod
    def encoding(cls, value: str) -> BitVector:
        return BitVector(value.encode(cls.encoding_name))

    @classmethod
    def decoding(cls, bits: BitVector) -> str:
        return bytes(bits).decode(cls.encoding_name)


class UTF8String(StandardEncodingString):
    encoding_name = "utf-8"


class Str1(UTF8String):
    _num_bits = 1


class Str2(UTF8String):
    _num_bits = 2


class Str3(UTF8String):
    _num_bits = 3


class Str4(UTF8String):
    _num_bits = 4


class Str5(UTF8String):
    _num_bits = 5


class Str6(UTF8String):
    _num_bits = 6


class Str7(UTF8String):
    _num_bits = 7


class Str8(UTF8String):
    _num_bits = 8


class Str9(UTF8String):
    _num_bits = 9


class Str10(UTF8String):
    _num_bits = 10


class Str11(UTF8String):
    _num_bits = 11


class Str12(UTF8String):
    _num_bits = 12


class Str13(UTF8String):
    _num_bits = 13


class Str14(UTF8String):
    _num_bits = 14


class Str15(UTF8String):
    _num_bits = 15


class Str16(UTF8String):
    _num_bits = 16


class Str32(UTF8String):
    _num_bits = 32


class Str64(UTF8String):
    _num_bits = 64


class Str128(UTF8String):
    _num_bits = 128


class Str256(UTF8String):
    _num_bits = 256


class Str512(UTF8String):
    _num_bits = 512


__all__ = [
    "String",
    "StandardEncodingString",
    "UTF8String",
    "Str1",
    "Str2",
    "Str3",
    "Str4",
    "Str5",
    "Str6",
    "Str7",
    "Str8",
    "Str9",
    "Str10",
    "Str11",
    "Str12",
    "Str13",
    "Str14",
    "Str15",
    "Str16",
    "Str32",
    "Str64",
    "Str128",
    "Str256",
    "Str512",
]
