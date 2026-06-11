from typing import TYPE_CHECKING

from bytemaker.bittypes.bittype import BitType
from bytemaker.bitvector import BitVector
from bytemaker.typing_redirect import Optional, Type, TypeVar

if TYPE_CHECKING:
    BufferSelf = TypeVar("BufferSelf", bound="Buffer")
else:
    try:
        from typing_redirect import Self as BufferSelf
    except ImportError:
        BufferSelf = TypeVar("BufferSelf", bound="Buffer")


class Buffer(BitType[BitVector]):
    """
    A BitType that represents a buffer of bits.

    Use the `specialize` method to create a subclass with the desired number of bits
        or use one of the pre-defined subclasses.

    Class Attributes:
    -----------------
    num_bits : int
        The number of bits in instances of this `Buffer` subclass.
    base_bit_type : Type[Buffer]
        The base `BitType` this class derives from. It will be `Buffer`.
    py_type : Type[BitVector]
        The type that this `BitType` represents. It is `BitVector`.

    Instance Attributes
    -------------------
    bits : BitVector
       The underlying sequence of bits of this `Buffer` object. Identical to `value`.
    value : BitVector
       The `BitVector` value of this `Buffer` object. Identical to `bits`.
    """

    """
    A BitType that represents a buffer of bits.

    Use the `specialize` method to create a subclass with the desired number of bits
        or use one of the pre-defined subclasses.
    """

    py_type = BitVector

    @property
    def value(self):
        return self.bits

    @value.setter
    def value(self, value):
        self._bits = BitVector(value)

    @classmethod
    def specialize(cls: Type[BufferSelf], num_bits_: int, name_: Optional[str] = None):
        """
        Returns a subclass of Buffer with the specified number of bits.

        Args:
            num_bits_ (int): The number of bits the buffer should have.
            name_ (Optional[str], optional): The name of the subclass. Defaults to None,
                meaning the name will be _Buffer.

        Returns:
            Type[BufferSelf]: A subclass of Buffer with the specified number of bits.
        """

        class _Buffer(cls):
            _num_bits = num_bits_

        if name_:
            _Buffer.__name__ = name_

        return _Buffer


Buffer.base_bit_type = Buffer


class Buffer1(Buffer):
    _num_bits = 1


class Buffer2(Buffer):
    _num_bits = 2


class Buffer3(Buffer):
    _num_bits = 3


class Buffer4(Buffer):
    _num_bits = 4


class Buffer5(Buffer):
    _num_bits = 5


class Buffer6(Buffer):
    _num_bits = 6


class Buffer7(Buffer):
    _num_bits = 7


class Buffer8(Buffer):
    _num_bits = 8


class Buffer9(Buffer):
    _num_bits = 9


class Buffer10(Buffer):
    _num_bits = 10


class Buffer11(Buffer):
    _num_bits = 11


class Buffer12(Buffer):
    _num_bits = 12


class Buffer13(Buffer):
    _num_bits = 13


class Buffer14(Buffer):
    _num_bits = 14


class Buffer15(Buffer):
    _num_bits = 15


class Buffer16(Buffer):
    _num_bits = 16


class Buffer17(Buffer):
    _num_bits = 17


class Buffer18(Buffer):
    _num_bits = 18


class Buffer19(Buffer):
    _num_bits = 19


class Buffer20(Buffer):
    _num_bits = 20


class Buffer21(Buffer):
    _num_bits = 21


class Buffer22(Buffer):
    _num_bits = 22


class Buffer23(Buffer):
    _num_bits = 23


class Buffer24(Buffer):
    _num_bits = 24


class Buffer25(Buffer):
    _num_bits = 25


class Buffer26(Buffer):
    _num_bits = 26


class Buffer27(Buffer):
    _num_bits = 27


class Buffer28(Buffer):
    _num_bits = 28


class Buffer29(Buffer):
    _num_bits = 29


class Buffer30(Buffer):
    _num_bits = 30


class Buffer31(Buffer):
    _num_bits = 31


class Buffer32(Buffer):
    _num_bits = 32


class Buffer50(Buffer):
    _num_bits = 50


class Buffer64(Buffer):
    _num_bits = 64


class Buffer100(Buffer):
    _num_bits = 100


class Buffer128(Buffer):
    _num_bits = 128


class Buffer200(Buffer):
    _num_bits = 200


class Buffer250(Buffer):
    _num_bits = 250


class Buffer256(Buffer):
    _num_bits = 256


class Buffer500(Buffer):
    _num_bits = 500


class Buffer512(Buffer):
    _num_bits = 512


class Buffer1000(Buffer):
    _num_bits = 1000


class Buffer1024(Buffer):
    _num_bits = 1024


__all__ = [
    "Buffer",
    "Buffer1",
    "Buffer2",
    "Buffer3",
    "Buffer4",
    "Buffer5",
    "Buffer6",
    "Buffer7",
    "Buffer8",
    "Buffer9",
    "Buffer10",
    "Buffer11",
    "Buffer12",
    "Buffer13",
    "Buffer14",
    "Buffer15",
    "Buffer16",
    "Buffer17",
    "Buffer18",
    "Buffer19",
    "Buffer20",
    "Buffer21",
    "Buffer22",
    "Buffer23",
    "Buffer24",
    "Buffer25",
    "Buffer26",
    "Buffer27",
    "Buffer28",
    "Buffer29",
    "Buffer30",
    "Buffer31",
    "Buffer32",
    "Buffer50",
    "Buffer64",
    "Buffer100",
    "Buffer128",
    "Buffer200",
    "Buffer250",
    "Buffer256",
    "Buffer500",
    "Buffer512",
    "Buffer1000",
    "Buffer1024",
]
