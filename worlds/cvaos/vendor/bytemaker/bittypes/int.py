from __future__ import annotations

import operator
from math import ceil, log2
from typing import TYPE_CHECKING, Any

from bytemaker.bittypes.bittype import BitType, StructPackedBitType
from bytemaker.bitvector import BitsConstructible, BitVector
from bytemaker.typing_redirect import Final, Literal, Optional, TypeVar
from bytemaker.utils import is_instance_of_union

if TYPE_CHECKING:
    IntSelf = TypeVar("IntSelf", bound="Int")
else:
    try:
        from typing_redirect import Self as IntSelf
    except ImportError:
        IntSelf = TypeVar("IntSelf", bound="Int")


class Int(BitType[int]):
    """
    A `BitType` that represents an integer.

    Is further subclassed into `SInt` and `UInt` for signed and unsigned integers,

    Class Attributes:
    ---------------
    num_bits : int
       The number of bits in the BitType.
    base_bit_type : Type[BitType]
       The base `BitType` this class derives from.
    py_type : Type[T]
       The Pythonic type that this Int can be converted to/from. It is int.
    is_signed : bool
       Whether the integer type is signed.

    Instance Attributes
    -------------------
    bits : BitVector
       The underlying sequence of bits of this `Int` object.
    value : int
       The `int` value of this `Int` object.
    endianness : Literal["big", "little"]
       The endianness of this `Int` object.
    """

    py_type = int
    is_signed: Final[bool]
    """Whether the integer type is signed."""

    def __int__(self):
        return self.value

    def to_pyint(
        self: BitType | BitsConstructible,
        signed: Optional[bool] = None,
        bin_format: Literal[
            "twos_complement", "signed_magnitude", "ones_complement"
        ] = "twos_complement",
    ):
        """
        Convert a bitstring to an integer.

        Parameters:
        - bitstring (str): The bitstring to convert.
        - signed (Optional[bool], optional) Whether the bitstring represents
            a signed integer (vs unsigned). Default is `cls.is_signed` or `True`.
        - bin_format (Optional[str], optional): The format for signed integers.
            Can be "twos_complement", "signed_magnitude", or "ones_complement".
            Default is "twos_complement".

        Returns:
        - int: The integer representation of the bitstring.
        """

        if signed is None:
            bin_format_default = getattr(self, "is_signed", True)
            assert isinstance(bin_format_default, bool)
            signed = bin_format_default

        if isinstance(self, BitType):
            self = self.bits.to01()
        elif isinstance(self, BitVector):
            self = self.to01()
        elif is_instance_of_union(self, BitsConstructible):
            self = BitVector(self).to01()
        else:
            raise TypeError(f"Unsupported type: {type(self)}")

        bitstring: str = self

        if not bitstring:
            raise ValueError("bitstring cannot be empty")

        bit_length = len(bitstring)

        if not signed:
            # Unsigned integer
            return int(bitstring, 2)

        # Signed integer handling
        if bin_format == "twos_complement":
            # Handle two's complement for signed integers
            if bitstring[0] == "1":  # Negative number
                int_value = -(2**bit_length) + int(bitstring, 2)
            else:  # Positive number
                int_value = int(bitstring, 2)

        elif bin_format == "signed_magnitude" or bin_format == "sign_magnitude":
            # Handle sign-magnitude for signed integers
            if bitstring[0] == "1":  # Negative number
                int_value = -int(bitstring[1:], 2)
            else:  # Positive number
                int_value = int(bitstring[1:], 2)

        elif bin_format == "ones_complement":
            # Handle one's complement for signed integers
            if bitstring[0] == "1":  # Negative number
                int_value = -((2 ** (bit_length - 1)) - int(bitstring[1:], 2) - 1)
            else:  # Positive number
                int_value = int(bitstring, 2)
        else:
            raise ValueError(f"Unsupported format: {bin_format}")

        return int_value

    @staticmethod
    def min_bit_length(
        value: int,
        signed: bool = True,
        bin_format: Optional[
            Literal["twos_complement", "signed_magnitude", "ones_complement"]
        ] = None,
    ) -> int:
        """
        Calculate the minimum number of bits required to represent an integer.
        Note that this is not the same as len(bin(value)), which assumes an unsigned
        representation (possibly with - in front).

        Parameters:
           value (int): The integer to represent.
           signed (bool, optional): Whether the representation format should be signed.
                Default is True.
           bin_format (Optional[str], optional): The format for signed integers.
                Can be "twos_complement", "signed_magnitude", or "ones_complement".
                Default is "twos_complement".
        """
        n = value

        if not signed:
            if n == 0:
                return 1
            return ceil(log2(n + 1))
        else:
            if bin_format is None:
                bin_format = "twos_complement"

            if bin_format == "twos_complement":
                if n == 0:
                    return 1  # Technically can represent 0 with 0 bits in
                    # two's complement, but this is not useful

                is_greq_than_zero = n >= 0
                abs_val = abs(n)
                is_power_of_two = (abs_val & (abs_val - 1)) == 0

                if is_greq_than_zero or not is_power_of_two:
                    return ceil(log2(abs_val + 1)) + 1  # Account for extra
                    # at negative extreme
                else:
                    return int(log2(abs_val)) + 1
            elif bin_format == "signed_magnitude" or bin_format == "sign_magnitude":
                if n == 0:
                    return 1
                return ceil(log2(abs(n) + 1)) + 1
            elif bin_format == "ones_complement":
                if n == 0:
                    return 1  # Technically can represent 0 with 0 bits in
                    # one's complement, but this is not useful
                return ceil(log2(abs(n) + 1)) + 1

    def to_bitstring(
        self: Int | int,
        signed: bool = True,
        bit_length: Optional[int] = None,
        rep_format: Optional[
            Literal["twos_complement", "signed_magnitude", "ones_complement"]
        ] = None,
    ) -> str:
        """
        Convert an integer to a bitstring.

        Parameters:
        - integer (int): The integer to convert.
        - signed (bool, optional): Whether the integer should be treated as signed.
            Default is True.
        - bit_length (int, optional): The length of the bitstring.
        - rep_format (Optional[str], optional): The format for signed integers.
            Can be "twos_complement", "signed_magnitude", or "ones_complement".
            Default is "twos_complement".

        Returns:
        - str: The bitstring representation of the integer.
        """

        def unsigned_int_to_bitstring(n: int, bit_length: int):
            if n < 0 or n >= 2**bit_length:
                raise ValueError("Value out of range for the specified bit_length")
            return bin(n)[2:].zfill(bit_length)

        def int_to_twos_complement(n: int, bit_length: int):
            """
            Convert a signed integer to its two's complement binary string
                representation.

            Args:
            z (int): The signed integer to convert.
            bit_length (int): The bit length of the two's complement representation.

            Returns:
            str: The two's complement binary string representation of the integer.
            """

            if n < -(2 ** (bit_length - 1)) or n >= 2 ** (bit_length - 1):
                raise ValueError(
                    "Value out of range for the specified bit_length"
                    " for two's-complement notation."
                )

            if n < 0:
                # Calculate two's complement for negative numbers
                n = 2**bit_length + n
            return format(n, f"0{bit_length}b")

        def int_to_ones_complement(n: int, bit_length: int):
            if abs(n) > 2 ** (bit_length - 1) - 1:
                raise ValueError(
                    "Value out of range for the specified bit_length"
                    " for one's-complement notation."
                )

            magnitude_string = unsigned_int_to_bitstring(abs(n), bit_length)
            if n >= 0:
                return magnitude_string
            else:
                return "".join(
                    "0" if digit == "1" else "1" for digit in magnitude_string
                )

        def int_to_signed_magnitude(n: int, bit_length: int):
            if abs(n) > 2 ** (bit_length - 1) - 1:
                raise ValueError(
                    "Value out of range for the specified bit_length"
                    " for sign-magnitude notation."
                )

            if n >= 0:
                return "0" + unsigned_int_to_bitstring(n, bit_length - 1)
            else:
                return "1" + unsigned_int_to_bitstring(-n, bit_length - 1)

        if isinstance(self, Int):
            value = self.value
        elif isinstance(self, int):
            value = int(self)

        if signed and rep_format is None:
            rep_format = "twos_complement"

        if bit_length is None:
            bit_length = Int.min_bit_length(value, signed=signed, bin_format=rep_format)

        if bit_length <= 0:
            raise ValueError("bit_length must be a positive integer")

        if not signed:
            return unsigned_int_to_bitstring(value, bit_length)

        if signed:
            if rep_format == "twos_complement":
                return int_to_twos_complement(value, bit_length)
            elif rep_format == "signed_magnitude" or rep_format == "sign_magnitude":
                return int_to_signed_magnitude(value, bit_length)
            elif rep_format == "ones_complement":
                return int_to_ones_complement(value, bit_length)
            else:
                raise ValueError(f"Unsupported format: {rep_format}")

    # Integer value magic methods
    def __add__(self: IntSelf, other: Any) -> IntSelf:
        return self._binary_value_op(other, operator.add)

    def __radd__(self: IntSelf, other: Any) -> IntSelf:
        return self._binary_value_op(other, lambda x, y: operator.add(y, x))

    def __sub__(self: IntSelf, other: Any) -> IntSelf:
        return self._binary_value_op(other, operator.sub)

    def __rsub__(self: IntSelf, other: Any) -> IntSelf:
        return self._binary_value_op(other, lambda x, y: operator.sub(y, x))

    def __mul__(self: IntSelf, other: Any) -> IntSelf:
        return self._binary_value_op(other, operator.mul)

    def __rmul__(self: IntSelf, other: Any) -> IntSelf:
        return self._binary_value_op(other, lambda x, y: operator.mul(y, x))

    def __truediv__(self: IntSelf, other: Any) -> IntSelf:
        return self._binary_value_op(other, operator.truediv)

    def __rtruediv__(self: IntSelf, other: Any) -> IntSelf:
        return self._binary_value_op(other, lambda x, y: operator.truediv(y, x))

    def __floordiv__(self: IntSelf, other: Any) -> IntSelf:
        return self._binary_value_op(other, operator.floordiv)

    def __rfloordiv__(self: IntSelf, other: Any) -> IntSelf:
        return self._binary_value_op(other, lambda x, y: operator.floordiv(y, x))

    def __mod__(self: IntSelf, other: Any) -> IntSelf:
        return self._binary_value_op(other, operator.mod)

    def __rmod__(self: IntSelf, other: Any) -> IntSelf:
        return self._binary_value_op(other, lambda x, y: operator.mod(y, x))

    def __pow__(self: IntSelf, other: Any) -> IntSelf:
        return self._binary_value_op(other, operator.pow)

    def __rpow__(self: IntSelf, other: Any) -> IntSelf:
        return self._binary_value_op(other, lambda x, y: operator.pow(y, x))

    # Integer bits magic methods
    def __lshift__(self: IntSelf, other: Any) -> IntSelf:
        return self._binary_bits_op(other, operator.lshift)

    def __rlshift__(self: IntSelf, other: Any) -> IntSelf:
        return self._binary_bits_op(other, lambda x, y: operator.lshift(y, x))

    def __rshift__(self: IntSelf, other: Any) -> IntSelf:
        return self._binary_bits_op(other, operator.rshift)

    def __and__(self: IntSelf, other: Any) -> IntSelf:
        return self._binary_bits_op(other, operator.and_)

    # def __add__(self: IntSelf, other: Any) -> IntSelf:
    #     return self._binary_value_op(other, operator.add)

    # def __mul__(self: IntSelf, other: Any) -> IntSelf:
    #     return self._binary_value_op(other, operator.mul)

    # def __sub__(self: IntSelf, other: Any) -> IntSelf:
    #     return self._binary_value_op(other, operator.sub)

    # def __truediv__(self: IntSelf, other: Any) -> IntSelf:
    #     return self._binary_value_op(other, operator.truediv)

    # def __floordiv__(self: IntSelf, other: Any) -> IntSelf:
    #     return self._binary_value_op(other, operator.floordiv)

    # def __mod__(self: IntSelf, other: Any) -> IntSelf:
    #     return self._binary_value_op(other, operator.mod)

    # def __pow__(self: IntSelf, other: Any) -> IntSelf:
    #     return self._binary_value_op(other, operator.pow)

    # def __lshift__(self: IntSelf, other: Any) -> IntSelf:
    #     return self._binary_bits_op(other, operator.lshift)

    # def __rshift__(self: IntSelf, other: Any) -> IntSelf:
    #     return self._binary_bits_op(other, operator.rshift)

    # def __and__(self: IntSelf, other: Any) -> IntSelf:
    #     return self._binary_bits_op(other, operator.and_)

    # def __or__(self: IntSelf, other: Any) -> IntSelf:
    #     return self._binary_bits_op(other, operator.or_)

    # def __xor__(self: IntSelf, other: Any) -> IntSelf:
    #     return self._binary_bits_op(other, operator.xor)


class SignedConfig:
    """
    A class to change the default representation and conversion
        for all non-user-implemented or non-user-specified signed integers
            simultaneously.
        If this is unadjusted, the default signed integer format is two's complement.
    """

    signed_int_format: Literal[
        "signed_magnitude", "ones_complement", "twos_complement"
    ] = "twos_complement"


class SInt(Int):
    """
    A BitType that represents a signed integer.

    Use the `specialize` method to create a subclass with the desired number of bits
        or use one of the pre-defined subclasses.

    To change the signed integer format, use the `Config` class
        (or set the `int_format` parameter in the constructor).
        The default signed integer format is two's complement.

    Class Attributes:
        base_bit_type : Type[BitType]
            The base class (this is `SInt` for `SInt` children).
        num_bits : int
            The number of bits in the integer.
        is_signed : bool
            Whether the integer is signed (this is True for SInts).

    Instance Attributes:
        int_format : Optional[str]
            The format for this signed integer.
            Can be "twos_complement", "signed_magnitude", or "ones_complement".
            If this is left as `None`, the format will be taken from the `Config` class.
            Default is "twos_complement.
        value : int
            The `int` value of the `SInt`.
        bits : BitVector
            The bits representing the value.
    """

    is_signed = True

    def __init__(
        self,
        source: Optional[(int | BitVector | BitType)] = None,
        value: Optional[int] = None,
        bits: Optional[BitVector] = None,
        endianness: Literal["big", "little", "source_else_big"] = "source_else_big",
        int_format: Optional[
            Literal["twos_complement", "signed_magnitude", "ones_complement"]
        ] = None,
    ):
        if int_format is None:
            int_format = SignedConfig.signed_int_format

        self.int_format: Literal[
            "twos_complement", "signed_magnitude", "ones_complement"
        ] = int_format
        super().__init__(source=source, value=value, bits=bits, endianness=endianness)

    # @classproperty
    # @classmethod
    # def int_format(cls) -> str:
    #     return Config.signed_int_format

    @property
    def value(self):
        return Int.to_pyint(self.bits.to01(), signed=True, bin_format=self.int_format)

    @value.setter
    def value(self, value):
        str_bits = Int.to_bitstring(
            value, signed=True, bit_length=self.num_bits, rep_format=self.int_format
        )

        self.bits = BitVector(str_bits)

    @classmethod
    def specialize(
        cls,
        num_bits_: int,
        packing_format_letter_: Optional[str] = None,
        name_: Optional[str] = None,
    ):
        """
        Produce a subclass of SInt with the specified number of bits.

        If a packing format letter is provided, the subclass will also be a
            StructPackedBitType
            and use struct's packing/unpacking functions with the provided letter.

        If name_ is provided, the subclass will have that name internally after class
            creation. Otherwise, the subclass will be named _SInt.

        Args:
            num_bits_ (int): The number of bits in integers of this type.
            packing_format_letter_ (Optional[str], optional): The struct packing format
                letter to use, if any. Defaults to None, meaning no struct (un)packing.
            name_ (Optional[str], optional): What to rename the subclass, if anything.
                Defaults to None, meaning the subclass's name will be _SInt.

        Returns:
            type[SInt]: The subclass of SInt with the specified number of bits.
        """
        if packing_format_letter_ is not None:

            class _SInt(StructPackedBitType[int], cls):
                _num_bits = num_bits_
                packing_format_letter = packing_format_letter_

                @property
                def skip_struct_packing(self):
                    return self.int_format != "twos_complement"

        else:

            class _SInt(cls):
                _num_bits = num_bits_

        if name_ is not None:
            _SInt.__name__ = name_

        return _SInt


SInt.base_bit_type = SInt


class SInt1(SInt):
    _num_bits = 1


class SInt2(SInt):
    _num_bits = 2


class SInt3(SInt):
    _num_bits = 3


class SInt4(SInt):
    _num_bits = 4


class SInt5(SInt):
    _num_bits = 5


class SInt6(SInt):
    _num_bits = 6


class SInt7(SInt):
    _num_bits = 7


class SInt8(StructPackedBitType, SInt):
    _num_bits = 8
    packing_format_letter = "b"

    @property
    def skip_struct_packing(self):
        return SignedConfig.signed_int_format != "twos_complement"


class SInt9(SInt):
    _num_bits = 9


class SInt10(SInt):
    _num_bits = 10


class SInt11(SInt):
    _num_bits = 11


class SInt12(SInt):
    _num_bits = 12


class SInt13(SInt):
    _num_bits = 13


class SInt14(SInt):
    _num_bits = 14


class SInt15(SInt):
    _num_bits = 15


class SInt16(StructPackedBitType, SInt):
    _num_bits = 16
    packing_format_letter = "h"

    @property
    def skip_struct_packing(self):
        return SignedConfig.signed_int_format != "twos_complement"


class SInt32(StructPackedBitType, SInt):
    _num_bits = 32
    packing_format_letter = "i"

    @property
    def skip_struct_packing(self):
        return SignedConfig.signed_int_format != "twos_complement"


class SInt64(StructPackedBitType, SInt):
    _num_bits = 64
    packing_format_letter = "q"

    @property
    def skip_struct_packing(self):
        return SignedConfig.signed_int_format != "twos_complement"


class SInt128(SInt):
    _num_bits = 128


class SInt256(SInt):
    _num_bits = 256


class UInt(Int):
    """
    A BitType that represents an unsigned integer.

    Use the `specialize` method to create a subclass with the desired number of bits
        or use one of the pre-defined subclasses.

    Class Attributes:
        base_bit_type (Type[BitType]): The base class (this is UInt).
        num_bits (int): The number of bits in the integer.
        is_signed (bool): Whether the integer is signed. (This is False)

    Properties:
        value (int): The integer value of the bits.
        bits (BitVector): The bits representing the integer value.
    """

    is_signed = False

    @property
    def value(self):
        return int(self.bits.to01(), 2)

    @value.setter
    def value(self, value):
        self._bits = BitVector(bin(value)[2:])

    @classmethod
    def specialize(
        cls,
        num_bits_: int,
        packing_format_letter_: Optional[str] = None,
        name_: Optional[str] = None,
    ):
        """
        Produce a subclass of UInt with the specified number of bits.

        If a packing format letter is provided, the subclass will also be a
            StructPackedBitType
            and use struct's packing/unpacking functions with the provided letter.

        If name_ is provided, the subclass will have that name internally after class
            creation. Otherwise, the subclass will be named _UInt.

        Args:
            num_bits_ (int): The number of bits in integers of this type.
            packing_format_letter_ (Optional[str], optional): The struct packing format
                letter to use, if any. Defaults to None, meaning no struct (un)packing.
            name_ (Optional[str], optional): What to rename the subclass, if anything.
                Defaults to None, meaning the subclass's name will be _UInt.

        Returns:
            type[UInt]: The subclass of UInt with the specified number of bits.
        """
        if packing_format_letter_ is not None:

            class _UInt(StructPackedBitType[int], cls):
                _num_bits = num_bits_
                packing_format_letter = packing_format_letter_

        else:

            class _UInt(cls):
                _num_bits = num_bits_

        if name_ is not None:
            _UInt.__name__ = name_

        return _UInt


UInt.base_bit_type = UInt


class UInt1(UInt):
    _num_bits = 1


class UInt2(UInt):
    _num_bits = 2


class UInt3(UInt):
    _num_bits = 3


class UInt4(UInt):
    _num_bits = 4


class UInt5(UInt):
    _num_bits = 5


class UInt6(UInt):
    _num_bits = 6


class UInt7(UInt):
    _num_bits = 7


class UInt8(StructPackedBitType, UInt):
    _num_bits = 8
    packing_format_letter = "B"


class UInt9(UInt):
    _num_bits = 9


class UInt10(UInt):
    _num_bits = 10


class UInt11(UInt):
    _num_bits = 11


class UInt12(UInt):
    _num_bits = 12


class UInt13(UInt):
    _num_bits = 13


class UInt14(UInt):
    _num_bits = 14


class UInt15(UInt):
    _num_bits = 15


class UInt16(StructPackedBitType, UInt):
    _num_bits = 16
    packing_format_letter = "H"


class UInt32(StructPackedBitType, UInt):
    _num_bits = 32
    packing_format_letter = "I"


class UInt64(StructPackedBitType, UInt):
    _num_bits = 64
    packing_format_letter = "Q"


class UInt128(UInt):
    _num_bits = 128


class UInt256(UInt):
    _num_bits = 256


__all__ = [
    "Int",
    "SInt",
    "UInt",
    "SignedConfig",
    "SInt1",
    "SInt2",
    "SInt3",
    "SInt4",
    "SInt5",
    "SInt6",
    "SInt7",
    "SInt8",
    "SInt9",
    "SInt10",
    "SInt11",
    "SInt12",
    "SInt13",
    "SInt14",
    "SInt15",
    "SInt16",
    "SInt32",
    "SInt64",
    "SInt128",
    "SInt256",
    "UInt1",
    "UInt2",
    "UInt3",
    "UInt4",
    "UInt5",
    "UInt6",
    "UInt7",
    "UInt8",
    "UInt9",
    "UInt10",
    "UInt11",
    "UInt12",
    "UInt13",
    "UInt14",
    "UInt15",
    "UInt16",
    "UInt32",
    "UInt64",
    "UInt128",
    "UInt256",
]
