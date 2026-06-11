from __future__ import annotations

import copy
import logging
import math
import sys
from typing import TYPE_CHECKING, overload

logger = logging.getLogger(__name__)

try:
    from bytemaker.typing_redirect import (
        Buffer,
        Iterable,
        Iterator,
        Literal,
        MutableSequence,
        Optional,
        Protocol,
        Sequence,
        TypeVar,
        Union,
        runtime_checkable,
    )
    from bytemaker.utils import is_instance_of_union, twos_complement_bit_length
except ImportError:
    from typing_redirect import (  # type: ignore
        Buffer,
        Iterable,
        Iterator,
        Literal,
        MutableSequence,
        Optional,
        Protocol,
        Sequence,
        TypeVar,
        Union,
        runtime_checkable,
    )
    from utils import is_instance_of_union, twos_complement_bit_length

LaxLiteral01 = Union[Literal[0, 1], int]
LaxLiteral01Str = Union[Sequence[Literal["0", "1"]], str]

if TYPE_CHECKING:
    Self = TypeVar("Self", bound="BitVector")
else:
    try:
        from typing_redirect import Self
    except ImportError:
        Self = TypeVar("Self", bound="BitVector")
T = TypeVar("T")


@runtime_checkable
class BitsCastable(Protocol):
    """
    Protocol for objects that can be cast to a BitVector.

    If provided object is not itself a BitVector, this protocol will be
       prioritized when BitVectorSubtype(object) is called
       over any other possible behavior.

    __Bits__ returns a BitVector representation of the object
        that should not be a shallow copy (unless you want)
        the cast object to share memory with the original object).
    """

    def __Bits__(
        self,
    ) -> BitVector:
        """
        Returns a deep BitVector representation of the object.

        This method is prioritized when BitVectorSubtype(object) is called.

        Returns:
            BitVector: The BitVector representation of the object
        """
        ...


_SEPARATOR_TABLE = str.maketrans("", "", "_- :")
_CHAR_TO_BIT = {"0": 0, "1": 1}
_BITS_TO_01_TABLE = bytes.maketrans(b"\x00\x01", b"01")

_BITS_PER_CHAR = {2: 1, 4: 2, 8: 3, 16: 4, 32: 5, 64: 6}
_STD_DIGITS = "0123456789abcdef"
_BASE32_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
_BASE64_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

# Each byte value expanded into its 8 constituent bits (most-significant first)
_BYTE_TO_BITS = [
    bytes((byte >> shift) & 1 for shift in range(7, -1, -1)) for byte in range(256)
]


def _coerce_bit(value: LaxLiteral01) -> int:
    """Validates that `value` is a 0 or 1 (or equal to one of them,
    e.g. booleans) and returns it as a plain int."""
    if value == 0:
        return 0
    if value == 1:
        return 1
    raise ValueError(f"bit must be 0 or 1, got {value!r}")


def _bytes_to_bits(data: bytes) -> bytearray:
    """Expands bytes into a bytearray of 0/1 values, 8 bits per input byte,
    most-significant bit first."""
    bits = bytearray()
    for byte in data:
        bits += _BYTE_TO_BITS[byte]
    return bits


def _char_to_value(char: str, base: int) -> int:
    """Converts a single digit character to its value in the given base
    (a power of two no greater than 64)."""
    if base <= 16:
        value = int(char, base)  # case-insensitive, raises ValueError when invalid
    elif base == 32:
        value = _BASE32_ALPHABET.find(char)
    else:
        value = _BASE64_ALPHABET.find(char)
    if value < 0:
        raise ValueError(f"invalid digit for base {base}: {char!r}")
    return value


def _base_str_to_bits(string: str, base: int) -> bytearray:
    """Converts a string of digits in the given base (a power of two
    no greater than 64) to a bytearray of 0/1 values."""
    bits_per_char = _BITS_PER_CHAR[base]
    bits = bytearray()
    for char in string:
        value = _char_to_value(char, base)
        bits.extend((value >> shift) & 1 for shift in range(bits_per_char - 1, -1, -1))
    return bits


class BitVector(MutableSequence[LaxLiteral01], BitsCastable):
    """
    A mutable sequence of bits.

    This class's behavior is largely a superset of that of bytearray.
       excepting certain methods that are not applicable to bits.

    This particular implementation is pure Python: the bits are stored
        in a bytearray, one byte per bit.

    Do note that the behavior documented in bitvector.pyi
        is what is guaranteed.
    """

    _bits: bytearray

    def __new__(
        cls: type[Self],
        source: Optional[Union[BitsConstructible, int]] = None,
        buffer: Optional[Buffer] = None,
        *args,
        **kwargs,
    ) -> Self:
        """
        Constructs a BitVector.
        * The bits are drawn from `buffer`, else `source`.

        If `buffer` is set, the BitVector's bits are read from the provided
            object. The buffer object must support the buffer protocol
            (https://docs.python.org/3/c-api/buffer.html).

        Otherwise, `source` determines the BitVector's bits.
        * If `source` is  None, the BitVector is empty.
        * If `source` is a str, the bits are obtained by prefix-determined classmethod\
           that allow `source` to be interspersed with "_", "-", " ", or ":" characters.
           * "" invokes `from01`
           * "0b" invokes `frombin`
           * "0o" invokes `fromoct`
           * "0x" invokes `fromhex`
        * If `source` is an int, the BitVector is created with that many bits\
            (set to 0).

        Args:
            source (Optional[Union[BitsConstructible, int]]): The bits of the BitVector
            * If None, a BitVector with no bits is created.
            * If a string, uses the prefix (none, 0b, 0o, or 0x) to call\
                    (`from01`, `frombin`, `fromoct`, `fromhex`).\
            * If an int, a BitVector with that many bits (set to 0) is created.\
            encoding (Optional[str]): The encoding to use (NOT IMPLEMENTED)
            errors (Optional[str]): The error handling to use for encoding \
                (not implemented)
            buffer (Buffer): The buffer to use

        """

        # Buffer constructor
        if buffer is not None:
            self: Self = super().__new__(cls)
            self._bits = _bytes_to_bits(bytes(memoryview(buffer)))
            return self
        # Default constructor
        elif source is None:
            self: Self = super().__new__(cls)
            self._bits = bytearray()
            return self
        # Copy constructor
        elif isinstance(source, BitVector):
            self: Self = super().__new__(cls)
            self._bits = bytearray(source._bits)
            return self
        # BitsCastable constructor
        elif isinstance(source, BitsCastable):
            curinstance = source.__Bits__()
            self: Self = super().__new__(cls)
            self._bits = bytearray(curinstance._bits)
            return self

        # String constructor
        if isinstance(source, str):
            if source.startswith("0b"):
                self: Self = cls.frombin(source)
            elif source.startswith("0o"):
                self: Self = cls.fromoct(source)
            elif source.startswith("0x"):
                self: Self = cls.fromhex(source)
            else:
                self: Self = cls.from01(source)
            return self

        # Int constructor
        if isinstance(source, int):
            self: Self = cls.fromsize(source)
            return self

        if isinstance(source, (bytes, bytearray)):
            self: Self = cls(buffer=source)
            return self

        if isinstance(source, Iterable):
            self: Self = super().__new__(cls)
            self._bits = bytearray(_coerce_bit(bit) for bit in source)
            assert isinstance(self, cls)
            return self

        raise ValueError(f"Invalid source type: {type(source)}")

    def __init__(
        self,
        source: Optional[Union[BitsConstructible, int]] = None,
        encoding: Optional[str] = None,
        errors: Optional[str] = None,  # TODO
        buffer: Buffer = None,  # type: ignore
    ) -> None:
        """
        If `buffer` is not None, the BitVector's bits are read from the
            provided buffer object. The buffer object must support the buffer
            protocol (https://docs.python.org/3/c-api/buffer.html).

        Otherwise, `source` determines the BitVector's bits.
        * If `source` is None, the BitVector is empty.
        * If `source` is a str, the bits are obtained by prefix-determined classmethod
           * "" invokes `from01`
           * "0b" invokes `frombin`
           * "0o" invokes `fromoct`
           * "0x" invokes `fromhex`
        * If `source` is an int, the BitVector is created with that many bits set to 0.

        Args:
            source (Optional[Union[BitsConstructible, int]]): The bits of the BitVector
               If None, a BitVector with no bits is created.\
               If a string, uses the prefix (none, 0b, 0o, or 0x) to call\
                    (`from01`, `frombin`, `fromoct`, `fromhex`).\
                If an int, a BitVector with that many bits (set to 0) is created.\
            encoding (Optional[str]): The encoding to use
            errors (Optional[str]): The error handling to use. TODO
            buffer (Buffer): The buffer to use

        """
        super().__init__()

    @classmethod
    def _with_bits(cls: type[Self], bits: Union[bytearray, Iterable[int]]) -> Self:
        """Creates a BitVector around an already-validated bytearray of
        0/1 values, without re-parsing or re-validating them."""
        instance = cls()
        instance._bits = bits if isinstance(bits, bytearray) else bytearray(bits)
        return instance

    # Transformations
    @classmethod
    def fromhex(
        cls: type[Self],
        string: str,
    ) -> Self:
        """
        Create a BitVector from a hexadecimal string.
        The string may contain any of '_', '-', ' ', or ':'.
        The string may start with "0x".

        Args:
            string (str): The hexadecimal string to convert

        Returns:
            BitVector: The BitVector created from the hexadecimal string
        """
        string = string.translate(_SEPARATOR_TABLE)
        if string.startswith("0x"):
            string = string[2:]
        return cls._with_bits(_base_str_to_bits(string, 16))

    @classmethod
    def fromoct(
        cls: type[Self],
        string: str,
    ) -> Self:
        """
        Create a BitVector from an octal string.
        The string may contain any of '_', '-', ' ', or ':'.
        The string may start with "0o".

        Args:
            string (str): The octal string to convert

        Returns:
            BitVector: The BitVector created from the octal string
        """
        string = string.translate(_SEPARATOR_TABLE)
        if string.startswith("0o"):
            string = string[2:]
        return cls._with_bits(_base_str_to_bits(string, 8))

    @classmethod
    def frombin(
        cls: type[Self],
        string: str,
    ) -> Self:
        """
        Create a BitVector from a binary string.
        The string may contain any of '_', '-', ' ', or ':'.
        The string may start with "0b".

        Args:
            string (str): The binary string to convert

        Returns:
            BitVector: The BitVector created from the binary string
        """
        if string.startswith("0b"):
            string = string[2:]
        return cls.from01(string)

    @classmethod
    def from01(
        cls: type[Self],
        string: LaxLiteral01Str,
    ) -> Self:
        """
        Create a BitVector from a binary string.
        The string may contain any of '_', '-', ' ', or ':'.
        The string must contain only 0s and 1s other than these.

        Args:
            string (str): The binary string to convert

        Returns:
            BitVector: The BitVector created from the binary string
        """
        if not isinstance(string, str):
            string = "".join(string)
        string = string.translate(_SEPARATOR_TABLE)
        try:
            bits = bytearray(_CHAR_TO_BIT[char] for char in string)
        except KeyError as exc:
            raise ValueError(
                f"expected only '0's and '1's, got {exc.args[0]!r}"
            ) from None
        return cls._with_bits(bits)

    @classmethod
    def fromsize(
        cls: type[Self],
        size: int,
        /,  # We do not know what the name in PEP 467 will be
    ) -> Self:
        """
        Create a BitVector with `size` bits, all set to 0.

        Args:
            size (int): The size of the BitVector to create

        Returns:
            BitVector: The BitVector created with the given size
        """
        return cls._with_bits(bytearray(max(size, 0)))

    @classmethod
    def frombase(
        cls: type[Self],
        string: str,
        base: int,
    ) -> Self:
        """
        Create a BitVector from a string in a given base.
        The string may contain any of '_', '-', ' ', or ':'.
        In the case of bases 2, 8, and 16,
            the string may start with "0b", "0o", or "0x" respectively.

        Args:
            string (str): The string to convert
            base (int): The base of the string

        Returns:
            BitVector: The BitVector created from the string
        """
        if base == 2:
            return cls.frombin(string)

        elif base == 8:
            return cls.fromoct(string)

        elif base == 16:
            return cls.fromhex(string)

        if base not in _BITS_PER_CHAR:
            raise ValueError(f"Invalid base: {base}")
        string = string.translate(_SEPARATOR_TABLE)
        return cls._with_bits(_base_str_to_bits(string, base))

    @classmethod
    def from_chararray(
        cls: type[Self],
        char_array: str,
        encoding: Union[str, dict[str, BitsConstructible]] = "utf-8",
    ) -> Self:
        """
        Create a BitVector from a `char_array` string where each character is a byte.
        The string is encoded using the given `encoding`. If this is a standard
           byte encoding, str.encode is used to convert the string to bytes.
        Otherwise, the string is converted to bytes using the given mapping,
            iterating over the `char_array` and building up substrings
            until a substring is found in the encoding mapping to convert to
            a BitVector. These converted BitVectors are concatenated together
            to form the final returned BitVector.

        Args:
            char_array (str): The string to convert
            encoding (Union[str, dict[str, BitsConstructible]]): The encoding to use

        Returns:
            BitVector: The BitVector created from the string
        """
        if isinstance(encoding, str):
            char_array_as_bytes: bytes = char_array.encode(encoding)

            retval = cls(buffer=char_array_as_bytes)

            logger.debug("using standard encoding...")
            logger.debug(f"retval {retval}")
            return retval
        else:
            bitarray_list: list[Self] = []
            substring = ""
            for char in char_array:
                substring += char
                if substring in encoding:
                    bitarray_list.append(cls(encoding[substring]))
                    substring = ""
            bitarray_catted = cls()
            for bitarray_single in bitarray_list:
                bitarray_catted += bitarray_single
            return bitarray_catted

    def _to_base_str(self, base: int) -> str:
        """Converts the bits to a string of digits in the given base
        (a power of two no greater than 64). The number of bits must be
        a multiple of the number of bits per digit."""
        bits_per_char = _BITS_PER_CHAR[base]
        if len(self._bits) % bits_per_char != 0:
            raise ValueError(
                f"BitVector length {len(self._bits)} not multiple of {bits_per_char}"
            )
        if base <= 16:
            alphabet = _STD_DIGITS
        elif base == 32:
            alphabet = _BASE32_ALPHABET
        else:
            alphabet = _BASE64_ALPHABET

        chars = []
        for i in range(0, len(self._bits), bits_per_char):
            value = 0
            for bit in self._bits[i : i + bits_per_char]:
                value = (value << 1) | bit
            chars.append(alphabet[value])
        return "".join(chars)

    def tobase(
        self, base: int, sep: Optional[str] = None, bytes_per_sep: int = 1
    ) -> str:
        """
        Convert the BitVector to a string in a given base.
        If `sep` is not None, the string is split into chunks of `bytes_per_sep` bytes
           punctuated by `sep`.

        Args:
            base (int): The base to convert to. Currently must be a power of 2 (< 64).
            sep (Optional[str]): The separator to use
            bytes_per_sep (int): The number of bytes per separator

        Returns:
            str: The BitVector converted to a string in the given base
        """
        # TODO support non-multiple-of-two bases
        if base not in {2, 4, 8, 16, 32, 64}:
            raise ValueError(f"Invalid base: {base}")
        retstring = self._to_base_str(base)
        bits_per_char = math.log2(base)
        chars_per_byte = int(8 / bits_per_char + 0.999999999)
        if sep is not None:
            chars_per_sep = int(chars_per_byte * bytes_per_sep)
            retstring = sep.join(
                retstring[i : i + chars_per_sep]
                for i in range(0, len(retstring), chars_per_sep)
            )
        return retstring

    def hex(self, sep: Optional[str] = None, bytes_per_sep: int = 1) -> str:
        """
        Convert the BitVector to a hexadecimal string prefixed by 0x.
        If `sep` is not None, the string is split into chunks of `bytes_per_sep` bytes
           punctuated by `sep`.

        Args:
            sep (Optional[str]): The separator to use
            bytes_per_sep (int): The number of bytes per separator

        Returns:
            str: The BitVector converted to a hexadecimal string
        """

        retval = "0x" + self.tobase(16, sep, bytes_per_sep)
        return retval

    def oct(self, sep: Optional[str] = None, bytes_per_sep: int = 1) -> str:
        """
        Convert the BitVector to an octal string prefixed by 0o.
        If `sep` is not None, the string is split into chunks of `bytes_per_sep` bytes
           punctuated by `sep`.

        Args:
            sep (Optional[str]): The separator to use
            bytes_per_sep (int): The number of bytes per separator

        Returns:
            str: The BitVector converted to an octal string
        """
        retval = "0o" + self.tobase(8, sep, bytes_per_sep)
        return retval

    def bin(self, sep: Optional[str] = None, bytes_per_sep: int = 1) -> str:
        """
        Convert the BitVector to a binary string prefixed by 0b.
        If `sep` is not None, the string is split into chunks of `bytes_per_sep` bytes
           punctuated by `sep`.

        Args:
            sep (Optional[str]): The separator to use
            bytes_per_sep (int): The number of bytes per separator

        Returns:
            str: The BitVector converted to a binary string
        """
        return "0b" + self.to01(sep, bytes_per_sep)

    def to01(self, sep: Optional[str] = None, bytes_per_sep: int = 1) -> str:
        """
        Convert the BitVector to an unprefixed binary string.
        If `sep` is not None, the string is split into chunks of `bytes_per_sep` bytes
           punctuated by `sep`.
        """

        to01_without_sep = self._bits.translate(_BITS_TO_01_TABLE).decode("ascii")
        bits_per_sep = 8 * bytes_per_sep
        if sep is not None:
            return sep.join(
                to01_without_sep[i : i + bits_per_sep]
                for i in range(0, len(to01_without_sep), bits_per_sep)
            )
        return to01_without_sep

    def to_chararray(
        self, encoding: Union[str, dict[BitsConstructible, str]] = "utf-8"
    ) -> str:
        """
        Convert the BitVector to a string where each byte is a character.
        The string is decoded using the given `encoding`. If this is a standard
           byte encoding, bytes.decode is used to convert the bytes to a string.
        Otherwise, the bytes are converted to strings using the given mapping.

        Args:
            encoding (Union[str, dict[BitsConstructible, str]]): The encoding to use

        Returns:
            str: The BitVector converted to a string
        """
        cls = type(self)
        if isinstance(encoding, str):
            assert len(self) % 8 == 0, "BitVector length must be a multiple of 8\
                to use a standard encoding"
            return bytes(self).decode(encoding)
        else:
            encoding = {
                cls(bits_constructible).to01(): valstr
                for bits_constructible, valstr in encoding.items()
            }
            str_list = []
            subbitarray = ""
            for bit in self.to01():
                subbitarray += bit
                if subbitarray in encoding:
                    str_list.append(encoding[subbitarray])
                    subbitarray = ""
            return "".join(str_list)

    # Magic Methods and Overloads
    def __eq__(self, other: object) -> bool:
        """
        Returns whether this BitVector's bits are equal to another object's bits.
        This will only really true if both objects are BitVectors.
        """
        if isinstance(other, BitVector):
            return self._bits == other._bits
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        """
        Returns whether this BitVector's bits are not equal to another object's bits.
        This will only really be false if both objects are BitVectors.
        """
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def __lt__(self, other: BitVector) -> bool:
        """
        Returns True if, proceeding left-to-right, the first bit that differs
            is 0 in this BitVector and 1 in the other BitVector.
        """
        if isinstance(other, BitVector):
            return self._bits < other._bits
        return NotImplemented

    def __le__(self, other: BitVector) -> bool:
        """
        Returns True if, proceeding left-to-right, the first bit that differs
            is 0 in this BitVector and 1 in the other BitVector.
            or no bits differ.
        """
        if isinstance(other, BitVector):
            return self._bits <= other._bits
        return NotImplemented

    def __gt__(self, other: BitVector) -> bool:
        """
        Returns True if, proceeding left-to-right, the first bit that differs
            is 1 in this BitVector and 0 in the other BitVector.
        """
        if isinstance(other, BitVector):
            return self._bits > other._bits
        return NotImplemented

    def __ge__(self, other: BitVector) -> bool:
        """
        Returns True if, proceeding left-to-right, the first bit that differs
            is 1 in this BitVector and 0 in the other BitVector.
            or no bits differ.
        """
        if isinstance(other, BitVector):
            return self._bits >= other._bits
        return NotImplemented

    def __add__(self: Self, other: BitsConstructible) -> Self:
        """
        Concatenation of a BitVector and something constructible to a BitVector.
           Non-commutative.
        """
        other = self.cast_if_not_bitvector(other)
        return type(self)._with_bits(self._bits + other._bits)

    def __radd__(self: Self, other: BitsConstructible) -> Self:
        """
        Concatenation of something constructible to a BitVector and a BitVector.
           Non-commutative.
        """
        return type(self)(other) + self

    def __iadd__(self: Self, other: BitsConstructible) -> Self:
        """
        Inplace concatenation of a BitVector and something constructible to a BitVector.
        """
        if not isinstance(other, BitVector):
            other = BitVector(other)
        self._bits += other._bits
        return self

    def __mul__(self: Self, count: int) -> Self:
        """
        Concatenation of `count` copies of the BitVector.
        """
        if not isinstance(count, int):
            return NotImplemented
        return type(self)._with_bits(self._bits * count)

    def __rmul__(self: Self, count: int) -> Self:
        """
        Concatenation of `count` copies of the BitVector.
        """
        product = self.__mul__(count)
        return product

    def __imul__(self: Self, count: int) -> Self:
        """
        In-place assignment of the concatenation of `count` copies of the BitVector.
        """
        if not isinstance(count, int):
            return NotImplemented
        self._bits *= count
        return self

    def _binary_bitwise_op(self: Self, other: BitsConstructible, op) -> Self:
        """Applies an equal-length elementwise binary operation
        against another BitsConstructible."""
        other = type(self)(other)
        if len(other._bits) != len(self._bits):
            raise ValueError("BitVectors of equal length expected")
        return type(self)._with_bits(
            bytearray(op(a, b) for a, b in zip(self._bits, other._bits))
        )

    def __and__(self: Self, other: BitsConstructible) -> Self:
        """
        Bitwise AND of the bits of a BitVector and something constructible\
           to a BitVector.
        """
        return self._binary_bitwise_op(other, lambda a, b: a & b)

    def __rand__(self: Self, other: BitsConstructible) -> Self:
        """
        Bitwise AND of the bits of something\
           constructible to a BitVector and a BitVector.
        """
        return self & other

    def __iand__(self: Self, other: BitsConstructible) -> Self:
        """
        In-place assignment of\
           the bitwise AND of the bits of a BitVector\
           and something constructible to a BitVector.
        """
        return self & other

    def __or__(self: Self, other: BitsConstructible) -> Self:
        """
        Bitwise OR of the bits of a BitVector and something constructible\
           to a BitVector.
        """
        return self._binary_bitwise_op(other, lambda a, b: a | b)

    def __ror__(self: Self, other: BitsConstructible) -> Self:
        """
        Bitwise OR of the bits of\
           something constructible to a BitVector and a BitVector.
        """
        return self | other

    def __ior__(self: Self, other: BitsConstructible) -> Self:
        """
        In-place assignment of
           the bitwise OR of the bits of a BitVector
           and something constructible to a BitVector.
        """
        return self | other

    def __xor__(self: Self, other: BitsConstructible) -> Self:
        """
        Bitwise XOR of the bits of a BitVector and something constructible\
           to a BitVector.
        """
        return self._binary_bitwise_op(other, lambda a, b: a ^ b)

    def __rxor__(self: Self, other: BitsConstructible) -> Self:
        """
        Bitwise XOR of the bits of something constructible to a BitVector\
           and a BitVector.
        """
        return self ^ other

    def __ixor__(self: Self, other: BitsConstructible) -> Self:
        """
        In-place assignment of\
           the bitwise XOR of the bits of a BitVector\
           and something constructible to a BitVector.
        """
        return self ^ other

    def __lshift__(self: Self, count: int) -> Self:
        """
        Left shift of the bits of a BitVector by `count` bits.
        The length is preserved; vacated positions on the right are
            filled with 0s.
        """
        if not isinstance(count, int):
            raise TypeError(f"count must be an int, not {type(count)}")
        if count < 0:
            raise ValueError("negative shift count")
        length = len(self._bits)
        return type(self)._with_bits(self._bits[count:] + bytearray(min(count, length)))

    def __ilshift__(self: Self, count: int) -> Self:
        """
        In-place assignment of
           the left shift of the bits of a BitVector by `count` bits.
        """
        return self << count

    def __rshift__(self: Self, count: int) -> Self:
        """
        Right shift of the bits of a BitVector by `count` bits.
        The length is preserved; vacated positions on the left are
            filled with 0s.
        """
        if not isinstance(count, int):
            raise TypeError(f"count must be an int, not {type(count)}")
        if count < 0:
            raise ValueError("negative shift count")
        length = len(self._bits)
        return type(self)._with_bits(
            bytearray(min(count, length)) + self._bits[: max(length - count, 0)]
        )

    def __irshift__(self: Self, count: int) -> Self:
        """
        In-place assignment of
           the right shift of the bits of a BitVector by `count` bits.
        """
        return self >> count

    def __invert__(self: Self) -> Self:
        """
        Bitwise inversion of the bits of the BitVector.
        """
        return type(self)._with_bits(bytearray(bit ^ 1 for bit in self._bits))

    def __iter__(self) -> Iterator[Literal[0, 1]]:
        """
        Iterate over the bits of the BitVector.
        """
        return iter(self._bits)  # type: ignore

    def __format__(self, format_spec: str) -> str:
        """
        Format the BitVector as a binary, octal, or hexadecimal string.
           "b" returns a binary string prefixed with "0b".
           "o" returns an octal string prefixed with "0o".
           "x" returns a hexadecimal string prefixed with "0x".
        Any other format specifier raises a ValueError.
        """
        if format_spec == "b":
            return self.bin()
        elif format_spec == "o":
            return self.oct()
        elif format_spec == "x":
            return self.hex()
        elif format_spec == "":
            return str(self)
        else:
            raise ValueError(f"Invalid format specifier: {format_spec}")

    def __contains__(self, item: object) -> bool:
        """
        Returns whether the BitVector contains
            a given bit, if the item is an int,
            a given BitVector, if the item is a BitVector,
            a given BitVector constructed from item, if the item is a non-int
               BitsConstructible,
            or False otherwise.
        """
        if isinstance(item, int):
            if item not in {0, 1}:
                return False
            item = BitVector([item])  # type: ignore
        elif not isinstance(item, BitVector):
            if is_instance_of_union(item, BitsConstructible):
                item = BitVector(item)  # type: ignore
            else:
                return False
        assert isinstance(item, BitVector)
        first_index = self.find(item)
        return first_index != -1

    @overload
    def __getitem__(self, key: int) -> Literal[0, 1]: ...

    @overload
    def __getitem__(self: Self, key: slice) -> Self: ...

    @overload
    def __getitem__(self: Self, key: Iterable[int]) -> Self: ...

    def __getitem__(self, key):  # type: ignore[override]
        if isinstance(key, int):
            return self._bits[key]
        elif isinstance(key, slice):
            return type(self)._with_bits(self._bits[key])
        elif isinstance(key, Iterable):
            retval = type(self)([self[i] for i in key])
            return retval
        else:
            raise TypeError(f"Invalid key type: {type(key)}")

    def __setitem__(  # type: ignore[override]
        self,
        key: Union[int, slice, Sequence[int]],
        value: Union[Literal[0, 1], BitsConstructible],
    ) -> None:
        """
        Set the bit at a given index
           or the bits across the indices given in slice or Sequence form.

        An individual bit can be set with a BitsConstructible of length 1.

        A slice or sequence of indices can be set either with a single bit
           (setting every indexed position to that bit) or with a
           BitsConstructible (matching positions elementwise; for non-unit
           slice steps and index sequences, the lengths must agree).
        """
        if isinstance(key, int):
            if not isinstance(value, int):
                value = BitVector(value)[0]
            self._bits[key] = _coerce_bit(value)
        elif isinstance(key, slice):
            if isinstance(value, int):
                bit = _coerce_bit(value)
                fill_length = len(range(*key.indices(len(self._bits))))
                self._bits[key] = bytes([bit]) * fill_length
            else:
                value = self.cast_if_not_bitvector(value)
                # bytearray handles resizing for unit-step slices and
                # enforces matching lengths for extended slices
                self._bits[key] = value._bits
        elif isinstance(key, Iterable):
            indices = list(key)
            if isinstance(value, int):
                bit = _coerce_bit(value)
                for index in indices:
                    self._bits[index] = bit
            else:
                value = self.cast_if_not_bitvector(value)
                if len(value._bits) != len(indices):
                    raise ValueError(
                        f"attempt to assign sequence of size {len(value._bits)}"
                        f" to {len(indices)} indices"
                    )
                for index, bit in zip(indices, value._bits):
                    self._bits[index] = bit
        else:
            raise TypeError(f"Invalid key type: {type(key)}")

    def __delitem__(self, key: Union[int, slice, Iterable[int]]) -> None:
        """
        Delete the bit at a given index
           or the bits across the indices given in slice or Iterable form.

        Args:
            key (Union[int, slice, Iterable[int]]): The index/indices of
                the bit(s) to delete.
        """
        if isinstance(key, (int, slice)):
            del self._bits[key]
        elif isinstance(key, Iterable):
            length = len(self._bits)
            indices = {index if index >= 0 else index + length for index in key}
            for index in sorted(indices, reverse=True):
                del self._bits[index]
        else:
            raise TypeError(f"Invalid key type: {type(key)}")

    def __len__(self) -> int:
        """
        Get the number of bits in the BitVector.
        """
        return len(self._bits)

    def __str__(self) -> str:
        """
        Get a string representation of the BitVector.
            This is e.g. "type(self)('010.....')".
        """
        zerosandones = self.to01()
        # chunk the list into 8-bit chunks
        zeroesandoneslist = [
            zerosandones[i : i + 8] for i in range(0, len(zerosandones), 8)
        ]
        # join the chunks with spaces
        return f"{type(self).__name__}" f"('{' '.join(zeroesandoneslist)}')"

    def __repr__(self) -> str:
        """
        Get a reconstructible representation of the BitVector.
            This is e.g. "type(self)('010.....')".
        """
        zerosandones = self.to01()
        # chunk the list into 8-bit chunks
        zeroesandoneslist = [
            zerosandones[i : i + 8] for i in range(0, len(zerosandones), 8)
        ]
        # join the chunks with spaces
        return f"{type(self).__name__}" f"('{' '.join(zeroesandoneslist)}'" f")"

    def __bytes__(self) -> bytes:
        """
        Convert the BitVector to a bytes object.
        If the length of the BitVector is not a multiple of 8,
            the BitVector is padded with 0s until the length is a multiple of 8.
        """
        return self.tobytes()

    def tobytes(self) -> bytes:
        """
        Convert the BitVector to a bytes object, with each group of 8 bits
            (most-significant first) becoming a byte.
        If the length of the BitVector is not a multiple of 8,
            the BitVector is padded with 0s until the length is a multiple of 8.
        """
        bits = self._bits
        byte_arr = bytearray()
        for i in range(0, len(bits), 8):
            chunk = bits[i : i + 8]
            byte = 0
            for bit in chunk:
                byte = (byte << 1) | bit
            byte <<= 8 - len(chunk)
            byte_arr.append(byte)
        return bytes(byte_arr)

    def __Bits__(
        self: Self,
    ) -> Self:
        """
        Implementation of the BitsCastable protocol.

        See the `BitsCastable` protocol for more information.

        Returns a BitVector version of the object.
        """
        return copy.copy(self)

    def __copy__(self: Self) -> Self:
        """
        Returns a shallow copy of the object
            with the same bits.
        """
        return type(self)._with_bits(bytearray(self._bits))

    def __deepcopy__(self: Self, memo: dict[int, object]) -> Self:
        """
        Returns a deep copy of the object
            with the same bits.
        """
        retval = type(self)()
        memo[id(self)] = retval
        retval._bits = bytearray(self._bits)
        return retval

    def __sizeof__(self) -> int:
        """
        Get the size of the BitVector in bytes.
        This will not be the same as the number of bits in the BitVector
           divided by 8 (and, in fact, will be larger). This is because
           the BitVector object itself has some overhead (and this
           pure-Python implementation incidentally stores each bit in
           a full byte of memory).
        """
        return super().__sizeof__() + sys.getsizeof(self._bits)

    # Basic Operations
    def append(self, value: LaxLiteral01) -> None:
        """Appends the provided bit to end (right) of the BitVector.

        Args:
            value (int): The bit to append
        """
        self._bits.append(_coerce_bit(value))

    def extend(  # type: ignore[reportIncompatibleMethodOverride]
        self, values: BitsConstructible
    ) -> None:
        """Extends the BitVector with the provided bits (appends them
            on the right).

        Args:
            values (BitsConstructible): The bits to append
        """
        if not isinstance(values, (Iterable)) or isinstance(values, str):
            values = BitVector(values)
        if isinstance(values, BitVector):
            self._bits += values._bits
        else:
            self._bits.extend(_coerce_bit(value) for value in values)

    def insert(  # type: ignore[reportIncompatibleMethodOverride]
        self, index: int, value: LaxLiteral01
    ) -> None:
        """Inserts the provided bit at the given index (zero-indexed).
        All bits at or to the right of the index are shifted right.

        Args:
            index (int): The index at which to insert the bit
            value (int): The bit to insert
        """
        self._bits.insert(index, _coerce_bit(value))

    def pop(  # type: ignore[reportIncompatibleMethodOverride]
        self, index: Optional[int] = None, default: Optional[T] = None
    ) -> Union[int, T]:
        """Removes and returns the bit at the given index (zero-indexed).
        All bits to the right of the index are shifted one left.
        If the provided index is None, the rightmost bit is popped.
        If a default is provided and the index is out of bounds,
        the default is returned.

        Args:
            index (Optional[int], optional): The position of the bit to pop.
                Defaults to None.
            default (Optional[T], optional): The default value to return if the
                index is out of bounds. Defaults to None.

        Raises:
            IndexError: If the index is out of bounds and no default is provided.

        Returns:
            Union[int, T]: The bit at the given index or the default value
        """
        if index is None:
            index = len(self) - 1
        if index >= len(self) or index < 0:
            if default is not None:
                return default
            raise IndexError("pop from empty BitVector")
        value = self._bits[index]
        del self._bits[index]
        return value

    def remove(self, value: LaxLiteral01) -> None:
        """Removes the first occurrence of the provided bit from the BitVector.

        Args:
            value (int): The bit to remove

        Raises:
            ValueError: If the bit is not found in the BitVector
        """
        index = self._bits.find(_coerce_bit(value))
        if index == -1:
            raise ValueError(f"{value} is not in BitVector")
        del self._bits[index]

    def clear(self) -> None:
        """Removes all bits from the BitVector."""
        self._bits.clear()

    def copy(self: Self) -> Self:
        """
        Returns a shallow copy of the BitVector
        """
        return self.__copy__()

    def reverse(self) -> None:
        """
        Reverses the bits in the BitVector.
        """
        self._bits.reverse()

    # Search and Analysis
    def count(  # type: ignore[reportIncompatibleMethodOverride]
        self,
        value: Union[BitsConstructible, int],
        start: int = 0,
        end: Optional[int] = None,
    ) -> int:
        """
        Counts the occurrences of the given bit in the BitVector
            between the given start (inclusive) and end (exclusive) indices.

        Args:
            value (Union[BitsConstructible, int]): The bit to count
            start (int, optional): The start index. Defaults to 0.
            end (Optional[int], optional): The end index. Defaults to None.

        Returns:
            int: The number of occurrences of the bit
                (within the provided index range, if any)
        """
        if end is None:
            end = len(self)
        if isinstance(value, int):
            return self._bits.count(_coerce_bit(value), start, end)

        if not isinstance(value, BitVector):
            value = BitVector(value)
        return self._bits.count(value._bits, start, end)

    def startswith(
        self,
        substrings: Union[
            BitsConstructible,
            BitVector,
            Literal[0, 1],
            Iterable[Union[BitsConstructible, BitVector]],
        ],
        start: int = 0,
        stop: Optional[int] = None,
    ) -> bool:
        """
        Checks if the BitVector starts with the given substring.
        If start and stop are provided, the check is performed only
            on the bits between the start (inclusive) and stop exclusive) indices.

        Args:
            substrings (Union[BitsConstructible, BitVector, Literal[0, 1],\
                Iterable[Union[BitsConstructible, BitVector]]]): The substring(s)
                to check
            start (int, optional): The start index. Defaults to 0.
            stop (Optional[int], optional): The stop index. Defaults to None.
        """
        conv_substrings = self._normalize_substrings(substrings)

        if stop is None:
            stop = len(self)

        # Ensure the start and stop indices are within the bounds of the BitVector
        start, stop = max(0, start), min(len(self), stop)

        if any(len(conv_substring) == 0 for conv_substring in conv_substrings):
            return True

        return any(
            len(conv_substring) <= stop - start
            and self._bits[start : start + len(conv_substring)] == conv_substring._bits
            for conv_substring in conv_substrings
        )

    def endswith(
        self,
        substrings: Union[
            BitsConstructible,
            BitVector,
            Literal[0, 1],
            Iterable[Union[BitsConstructible, BitVector]],
        ],
        start: int = 0,
        stop: Optional[int] = None,
    ) -> bool:
        """
        Checks if the BitVector ends with the given substring.
        If start and stop are provided, the check is performed only
            on the bits between the start (inclusive) and stop exclusive) indices.

        Args:
            substrings (Union[BitsConstructible, BitVector, Literal[0, 1],\
                Iterable[Union[BitsConstructible, BitVector]]]): The substring(s)
                to check
            start (int, optional): The start index. Defaults to 0.
            stop (Optional[int], optional): The stop index. Defaults to None.
        """
        conv_substrings = self._normalize_substrings(substrings)

        if stop is None:
            stop = len(self)

        # Ensure the start and stop indices are within the bounds of the BitVector
        start, stop = max(0, start), min(len(self), stop)

        if any(len(conv_substring) == 0 for conv_substring in conv_substrings):
            return True

        return any(
            len(conv_substring) <= stop - start
            and self._bits[stop - len(conv_substring) : stop] == conv_substring._bits
            for conv_substring in conv_substrings
        )

    @staticmethod
    def _normalize_substrings(
        substrings: Union[
            BitsConstructible,
            BitVector,
            Literal[0, 1],
            Iterable[Union[BitsConstructible, BitVector]],
        ],
    ) -> list[BitVector]:
        """Converts the substring(s) accepted by startswith/endswith into
        a list of BitVectors. A bare iterable of ints is interpreted as a
        single substring; other iterables are interpreted as collections
        of substrings."""
        if isinstance(substrings, BitVector):
            return [substrings]
        elif isinstance(substrings, int):
            return [BitVector([substrings])]
        elif isinstance(substrings, (str, bytes, BitsCastable)):
            return [BitVector(substrings)]
        elif isinstance(substrings, Iterable):
            list_of_substrings = list(substrings)
            if all(isinstance(substring, int) for substring in list_of_substrings):
                return [BitVector(list_of_substrings)]  # type: ignore
            elif all(
                is_instance_of_union(substring, BitsConstructible)
                for substring in list_of_substrings
            ):
                return [
                    BitVector(substring)  # type: ignore
                    for substring in list_of_substrings
                ]
            else:
                raise ValueError("Invalid type in provided iterable")
        else:
            raise TypeError(f"Invalid substrings type: {type(substrings)}")

    def find(  # type: ignore[reportIncompatibleMethodOverride]
        self,
        value: Union[BitsConstructible, int],
        start: int = 0,
        stop: Optional[int] = None,
    ) -> int:
        """Finds the first occurrence of the given bit in the BitVector,
        or of the subsequence of bits if provided.
        If the bit is not found, -1 is returned.

        Args:
            value (Union[BitsConstructible, int]): The bit to find
            start (int, optional): The initial index to search. Defaults to 0.
            stop (Optional[int], optional): The index to give up on. Defaults to None.

        Returns:
            int: The index of the first occurrence of the bit, or -1 if not found
        """
        if stop is None:
            stop = len(self)
        if isinstance(value, int):
            return self._bits.find(_coerce_bit(value), start, stop)
        if not isinstance(value, BitVector):
            value = BitVector(value)
        return self._bits.find(value._bits, start, stop)

    def rfind(  # type: ignore[reportIncompatibleMethodOverride]
        self,
        value: Union[BitsConstructible, int],
        start: int = 0,
        stop: Optional[int] = None,
    ) -> int:
        """Finds the last occurrence of the given bit in the BitVector,
        or of the subsequence of bits if provided.
        If the bit is not found, -1 is returned.

        Args:
            value (Union[BitsConstructible, int]): The bit to find
            start (int, optional): The last (leftmost) index to search. Defaults to 0.
            stop (Optional[int], optional): One over the index to start.
                Defaults to None.

        Returns:
            int: The index of the last occurrence of the bit, or -1 if not found
        """
        if stop is None:
            stop = len(self)
        if isinstance(value, int):
            return self._bits.rfind(_coerce_bit(value), start, stop)
        if not isinstance(value, BitVector):
            value = BitVector(value)
        return self._bits.rfind(value._bits, start, stop)

    def index(  # type: ignore[reportIncompatibleMethodOverride]
        self,
        value: Union[BitsConstructible, int],
        start: int = 0,
        stop: Optional[int] = None,
    ) -> int:
        """Finds the first occurrence of the given bit in the BitVector, or
        of the subsequence of bits if provided.
        If the bit is not found, a ValueError is raised.

        Args:
            value (Union[BitsConstructible, int]): The bit to find
            start (int, optional): The first (leftmost) index to check. Defaults to 0.
            stop (Optional[int], optional): The index to give up on.
                Defaults to None.

        Raises:
            ValueError: If the bit is not found

        Returns:
            int: The index of the first occurrence of the bit
        """
        index = self.find(value, start, stop)
        if index == -1:
            raise ValueError(f"{value} is not in BitVector")
        return index

    def rindex(
        self,
        value: Union[BitsConstructible, int],
        start: int = 0,
        stop: Optional[int] = None,
    ) -> int:
        """Finds the last occurrence of the given bit in the BitVector, or
        of the subsequence of bits if provided.
        If the bit is not found, a ValueError is raised.

        Args:
            value (Union[BitsConstructible, int]): The bit to find
            start (int, optional): The last (leftmost) index to check. Defaults to 0.
            stop (Optional[int], optional): One over the index to start on.
                Defaults to None.

        Raises:
            ValueError: If the bit is not found

        Returns:
            int: The index of the last occurrence of the bit
        """
        index = self.rfind(value, start, stop)
        if index == -1:
            raise ValueError(f"{value} is not in BitVector")
        return index

    # Modification and Translation
    def replace(
        self: Self,
        old: BitsConstructible,
        new: BitsConstructible,
        count: Optional[int] = None,
    ) -> Self:
        """
        Generates a new BitVector with occurrences of the sequences of
            old bits replaced by the new bits.
        If count is provided, only the first `count` occurrences are replaced.

        Args:
            old (BitsConstructible): The bits to replace
            new (BitsConstructible): The bits to replace with
            count (Optional[int], optional): The maximum number of replacements.
                Defaults to None (maximal replacement).

        Returns:
            Self: The new BitVector with the replacements made
        """
        if not isinstance(old, type(self)):
            old = type(self)(old)
        if not isinstance(new, type(self)):
            new = type(self)(new)

        if len(old) == 0:
            return self.copy()

        max_replacements = float("inf") if count is None else count
        num_replacements = 0

        index = 0
        accumulated_bits = bytearray()

        while float(num_replacements) < max_replacements:
            found_index = self._bits.find(old._bits, index)
            if found_index == -1:
                break

            accumulated_bits += self._bits[index:found_index] + new._bits
            index = found_index + len(old)  # Move index past the replaced bits
            num_replacements += 1

        accumulated_bits += self._bits[index:]
        return type(self)._with_bits(accumulated_bits)

    def join(self: Self, iterable: Iterable[BitsConstructible]) -> Self:
        """
        Concatenates the BitVectors in the iterable
            with self as the separator.

        Args:
            self (Self): The element-separating BitVector in the concatenation.
            iterable (Iterable[BitsConstructible]): The BitVectors to concatenate.

        Returns:
            Self: A concatenation of the BitVectors in the iterable with
                self between them.
        """
        items = [
            item if isinstance(item, type(self)) else type(self)(item)
            for item in iterable
        ]
        joined_bits = bytearray()
        for position, item in enumerate(items):
            if position > 0:
                joined_bits += self._bits
            joined_bits += item._bits
        return type(self)._with_bits(joined_bits)

    def partition(self: Self, sep: BitVector) -> tuple[Self, Self, Self]:
        """
        Partitions the BitVector into three parts:
            the part before the first occurrence of the separator,
            the separator itself, and the part after the separator.
        If the separator is not found, the first part is the entire BitVector,
            and the other two parts are empty BitVectors.

        Args:
            sep (BitVector): The separator BitVector

        Returns:
            tuple[Self, Self, Self]: The three parts of the partition
        """
        index = self.find(sep)
        if index == -1:
            return self, type(self)(), type(self)()

        self_to_index = self[:index]
        sep = type(self)(sep)
        self_after_offset = self[index + len(sep) :]
        return self_to_index, sep, self_after_offset

    def rpartition(self: Self, sep: BitVector) -> tuple[Self, Self, Self]:
        """
        Partitions the BitVector into three parts:
            the part before the last occurrence of the separator,
            the separator itself, and the part after the separator.
        If the separator is not found, the last part is the entire BitVector,
            and the other two parts are empty BitVectors.

        Args:
            sep (BitVector): The separator BitVector

        Returns:
            tuple[Self, Self, Self]: The three parts of the partition
        """
        index = self.rfind(sep)
        if index == -1:
            return type(self)(), type(self)(), self

        self_to_index = self[:index]
        sep = type(self)(sep)
        self_after_offset = self[index + len(sep) :]
        return self_to_index, sep, self_after_offset

    @staticmethod
    def _normalize_strip_bit(
        bits: Optional[Union[Literal[0], Literal[1]]],
    ) -> Optional[int]:
        """Reduces the `bits` argument of lstrip/rstrip/strip to
        None or a single int."""
        if not (bits is None or isinstance(bits, int)):
            if hasattr(bits, "__int__"):
                bits = int(bits)  # type: ignore
            elif isinstance(bits, Iterable):
                bits = int(next(iter(bits)))  # type: ignore
            else:
                bits = int(bits)  # type: ignore
        return bits

    def lstrip(
        self: Self, bits: Optional[Union[Literal[0], Literal[1]]] = None
    ) -> Self:
        """
        Returns a new BitVector with contiguous leading instances of the
            provided bit from the BitVector removed.
        Defaults to removing leading 0s.

        Args:
            self (Self): The bit to remove contiguous leading instances of.
            bits (Optional[Union[Literal[0], Literal[1]]], optional):
                The bit to remove. Defaults to None, removing leading 0s.

        Returns:
            Self: The BitVector with the leading bits removed.
        """
        bits = self._normalize_strip_bit(bits)

        if bits is None or bits == 0:
            retvalindex = self.find(1)
        else:
            retvalindex = self.find(0)

        if retvalindex == -1:
            return type(self)()

        retval = self[retvalindex:]
        return retval

    def rstrip(
        self: Self, bits: Optional[Union[Literal[0], Literal[1]]] = None
    ) -> Self:
        """
        Returns a new BitVector with contiguous trailing instances of the
            provided bit from the BitVector removed.
        Defaults to removing trailing 0s.

        Args:
            self (Self): The bit to remove contiguous trailing instances of.
            bits (Optional[Union[Literal[0], Literal[1]]], optional): The
                bit to remove. Defaults to None, removing trailing 0s.

        Returns:
            Self: The BitVector with the trailing bits removed.
        """
        bits = self._normalize_strip_bit(bits)

        if bits is None or bits == 0:
            retvalindex = self.rfind(1)
        else:
            retvalindex = self.rfind(0)

        if retvalindex == -1:
            return type(self)()

        retval = self[: retvalindex + 1]
        return retval

    def strip(self: Self, bits: Optional[Union[Literal[0], Literal[1]]] = None) -> Self:
        """
        Returns a new BitVector with contiguous leading and trailing instances of the
            provided bit from the BitVector removed.
        Defaults to removing leading and trailing 0s.

        Args:
            self (Self): The bit to remove contiguous leading and trailing instances of.
            bits (Optional[Union[Literal[0], Literal[1]]], optional): The
                bit to remove. Defaults to None, removing leading and trailing 0s.

        Returns:
            Self: A BitVector with the leading and trailing bits removed.
        """
        return self.lstrip(bits).rstrip(bits)

    def lpad(self: Self, width: int, fillbit: Literal[0, 1] = 0) -> Self:
        if len(self) >= width:
            return self
        return type(self)([fillbit] * (width - len(self))) + self

    def rpad(self: Self, width: int, fillbit: Literal[0, 1] = 0) -> Self:
        if len(self) >= width:
            return self
        return self + type(self)([fillbit] * (width - len(self)))

    @classmethod
    def cast_if_not_bitvector(
        cls: type[Self], obj: BitsConstructible
    ) -> Union[Self, BitVector]:
        """
        Casts the object to a BitVector if it is not already a BitVector.

        Args:
            cls (type[Self]): The class of the object
            obj (BitsConstructible): The object to cast

        Returns:
            Union[Self, BitVector]: The object as a BitVector
        """
        return cls(obj) if not isinstance(obj, BitVector) else obj

    # Temporary methods. For transition from bits to bitarray only
    @classmethod
    def from_int(cls, integer: int, size: Optional[int] = None):
        """
        Converts an integer to a Bits object.
         The size parameter determines the number of bits to use.\
         If size is not provided, the number of bits required to \
         represent the integer is used.
        """
        if size is None:
            size = twos_complement_bit_length(integer)
        if integer.bit_length() > size:
            raise ValueError(
                f"Cannot convert {integer} to Bits with size {size},"
                f" because it requires {integer.bit_length()} bits to represent."
            )

        bitlist = list()
        for index in range(size):
            bitlist.insert(0, (integer >> index) & 1)

        return cls(bitlist)

    @classmethod
    def from_bytes(cls, byte_arr: bytes, reverse_endianness=False):
        if reverse_endianness:
            byte_arr = bytes(reversed(byte_arr))

        return cls(byte_arr)

    def to_int(self, endianness: Literal["big", "little"] = "big", signed=True) -> int:
        """
        Converts a Bits object to an integer. It does this
            by casting the Bits to bytes, and then converting the bytes to an integer
            using the provided endianness and signedness.
        """
        copy = BitVector(list(self))
        if signed and len(copy) > 0 and copy[0] == 1:
            next_multiple_of_8 = math.ceil(len(self) / 8) * 8
            copy = copy.lpad(width=next_multiple_of_8, fillbit=1)

        return int.from_bytes(copy.to_bytes(), byteorder=endianness, signed=signed)

    def to_bytes(self, reverse_endianness=False) -> bytes:
        byte_arr = bytearray()
        for i in range(0, len(self), 8):
            byte = 0
            byte_end_index = min(i + 8, len(self))

            for bit in self[i:byte_end_index]:
                byte = (byte << 1) | bit
            byte_arr.append(byte)

        if reverse_endianness:
            byte_arr = reversed(byte_arr)
        return bytes(byte_arr)


BitsConstructible = Union[BitVector, bytes, str, Iterable[LaxLiteral01], BitsCastable]
"""
The types that can be used to construct a BitVector.
These include the BitVector class itself, bytes, str, iterables of 0s and 1s,
and objects that can be cast to a BitVector.

Please note that you can also use an int to construct a BitVector of that many
zeroes, but this is not included in the type hint because it is less implicitly
a series of bits.
"""
