import ctypes
import dataclasses

from bytemaker.bittypes import BitType, bytes_to_bittype
from bytemaker.bitvector import BitVector
from bytemaker.conversions.ctypes_ import (
    CType,
    bits_to_ctype,
    bytes_to_ctype,
    ctype_to_bits,
    ctype_to_bytes,
)
from bytemaker.conversions.pytypes import (
    ConversionConfig,
    PyType,
    bits_to_pytype,
    bytes_to_pytype,
    pytype_to_bits,
    pytype_to_bytes,
)
from bytemaker.typing_redirect import Dict, Iterable, Literal, Union, get_type_hints
from bytemaker.utils import DataClassType, is_instance_of_union, is_subclass_of_union

UnitType = Union[CType, BitType, PyType]

# CType is a Union of _SimpleCData, Structure, Union, and Array
# YType is a Union of YInt, YFloat, YString, YBytes, YBool, YEnum, YArray, and YStruct
# PyType is a Union of int, float, str, bytes, bool, and Enum


def resolve_field_types(dataclass_type: type) -> Dict[str, type]:
    """
    Resolve a dataclass's field annotations to concrete types.

    Field annotations are strings rather than types whenever the defining
    module uses ``from __future__ import annotations`` (PEP 563) or otherwise
    stringizes its annotations. ``typing.get_type_hints`` evaluates those
    strings in the namespace of the module that defined the dataclass, so
    concrete types such as ``SInt16`` resolve correctly. A bare ``eval`` would
    instead resolve them in bytemaker's own namespace and raise ``NameError``.

    For non-stringized annotations the field types are already real objects and
    are returned unchanged, so this is safe to use unconditionally.

    Returns:
        Dict[str, type]: A mapping from field name to its resolved type.
    """
    return get_type_hints(dataclass_type)


def count_bits_in_unit_type(unit_type: UnitType) -> int:
    """
    Function to count the number of bits in a UnitType-\
        a Python, type, ctype, or BitType (bytemaker type).
    """

    # print("Counting bits in unit type", unit_type)
    if is_subclass_of_union(unit_type, CType):
        return ctypes.sizeof(unit_type) * 8
    elif is_subclass_of_union(unit_type, BitType):
        return unit_type.num_bits
    elif is_subclass_of_union(unit_type, PyType):
        # print(ConversionConfig.get_conversion_info(unit_type).num_bits)
        return ConversionConfig.get_conversion_info(unit_type).num_bits("")
    elif is_subclass_of_union(unit_type, DataClassType):
        size_in_bits = 0
        field_types = resolve_field_types(unit_type)
        for field in dataclasses.fields(unit_type):
            size_in_bits += count_bits_in_unit_type(field_types[field.name])
        return size_in_bits


def count_bits_in_aggregate_type(aggregate_type: type) -> int:
    """
    Function to count the number of bits in an aggregate type-\
        a Python, type, ctype, BitType (bytemaker type), or
        a dataclass annotated with those.
    """
    if is_subclass_of_union(aggregate_type, UnitType):
        return count_bits_in_unit_type(aggregate_type)
    else:
        size_in_bits = 0
        field_types = resolve_field_types(aggregate_type)
        for field in dataclasses.fields(aggregate_type):
            size_in_bits += count_bits_in_unit_type(field_types[field.name])
        return size_in_bits


def count_bytes_in_unit_type(unit_type: UnitType) -> int:
    """
    Function to count the number of bytes in a UnitType-
        a Python numeric/binary/string type, ctype, or BitType (bytemaker type).
    """
    return (count_bits_in_unit_type(unit_type) + 7) // 8


def to_bits_individual(unit: UnitType) -> BitVector:
    """
    Function to convert a single Python primitive or ctypes object into BitVector.
    """
    if is_instance_of_union(unit, CType):
        return ctype_to_bits(unit)
    elif isinstance(unit, BitType):
        return unit.to_bits()
    elif is_instance_of_union(unit, PyType):
        return pytype_to_bits(unit)
    else:
        raise Exception(
            f"Cannot convert {unit} to bits because"
            f" the unit type is not a CType, YType, or PyType"
        )


def to_bytes_individual(
    unit: UnitType, endianness: Literal["big", "little"] = "big"
) -> bytes:
    """
    Function to convert a single Python primitive or ctypes object into bytes.
    """

    if is_instance_of_union(unit, CType):
        return ctype_to_bytes(unit, endianness=endianness)
    elif isinstance(unit, BitType):
        unit_bytes = bytes(unit)
        if endianness == "little":
            unit_bytes = unit_bytes[::-1]
        return unit_bytes
    elif is_instance_of_union(unit, PyType):
        return pytype_to_bytes(unit, endianness=endianness)
    else:
        raise Exception(
            f"Cannot convert {unit} to bytes because"
            f" the unit type is not a CType, YType, or PyType"
        )


def from_bits_individual(unitbits: BitVector, unittype: type) -> PyType:
    """
    Function to convert BitVector into a single UnitType-
        a Python numeric/binary/string type, ctype, or YType (bytemaker type).

    Args:
        unitbits (BitVector): The BitVector object to convert to a UnitType
        unittype (type): The type of the UnitType to convert to.
            Must be a member of UnitType
    """

    size_in_bits = count_bits_in_unit_type(unittype)

    if len(unitbits) != size_in_bits:
        raise Exception(
            f"Cannot convert {unitbits} to {unittype}"
            f" because the number of bits in the bits object ({unitbits.num_bits})"
            f" does not match the number of bits in the unit type ({size_in_bits})"
        )
    if is_subclass_of_union(unittype, CType):
        return bits_to_ctype(unitbits, unittype)
    elif is_subclass_of_union(unittype, BitType):
        return unittype.from_bits(unitbits)
    elif is_subclass_of_union(unittype, PyType):
        return bits_to_pytype(unitbits, unittype)
    else:
        raise Exception(
            f"Cannot convert {unitbits} to {unittype}"
            f" because the unit type is not a CType, YType, or PyType"
        )


def from_bytes_individual(
    unitbytes: bytes,
    unittype: type,
    endianness: Literal["big", "little"] = "big",
) -> PyType:
    """
    Function to convert bytes into a single UnitType-
        a Python numeric/binary/string type, ctype, or YType (bytemaker type).

    Args:
        unitbytes (bytes): The bytes object to convert to a UnitType
        unittype (type): The type of the UnitType to convert to.
            Must be a member of UnitType
        endianness: The byte order of the input bytes.
            Defaults to "big".
    """

    size_in_bits = count_bits_in_unit_type(unittype)
    if len(unitbytes) * 8 != size_in_bits:
        raise Exception(
            f"Cannot convert {unitbytes} to {unittype}"
            f" because the number of bits in the bytes object ({len(unitbytes) * 8})"
            f" does not match the number of bits in the unit type ({size_in_bits})"
        )
    if is_subclass_of_union(unittype, CType):
        return bytes_to_ctype(unitbytes, unittype, endianness=endianness)
    elif is_subclass_of_union(unittype, BitType):
        return bytes_to_bittype(unitbytes, unittype, endianness=endianness)
    elif is_subclass_of_union(unittype, PyType):
        return bytes_to_pytype(unitbytes, unittype, endianness=endianness)
    else:
        raise Exception(
            f"Cannot convert {unitbytes} to {unittype}"
            f" because the unit type is not a CType, YType, or PyType"
        )


AggregateTypeByteConvertible = Union[DataClassType, BitType, CType, PyType, Iterable]


def trycast(obj, type_):
    if not isinstance(obj, type_):
        obj = type_(obj)
    return obj


def to_bits_aggregate(convertible_object: AggregateTypeByteConvertible) -> BitVector:
    """
    Function to convert a BitType, Python primitive, ctypes object, or dataclass\
        of those types into a BitVector.

    Essentially a bitfield serializer.

    Args:
        units (DataClassType | YType | CType | PyType | Iterable):\
            The object to convert to BitVector

    Returns:
        BitVector: The BitVector representation of the object
    """

    ret_bits = BitVector()

    # print("to_bits_aggregate", convertible_object)
    # print("type(units)", type(convertible_object))
    # print("isinstance(units, DataClassType)",
    # isinstance(convertible_object, DataClassType))

    # try:
    if is_instance_of_union(convertible_object, UnitType) and not (
        isinstance(convertible_object, str) and len(convertible_object) > 1
    ):
        ret_bits = to_bits_individual(convertible_object)
    elif isinstance(convertible_object, DataClassType):
        fields = dataclasses.fields(convertible_object)
        resolved_types = resolve_field_types(type(convertible_object))
        field_values = [getattr(convertible_object, field.name) for field in fields]
        field_types = [resolved_types[field.name] for field in fields]
        # print("types", field_types)
        # print("type_is_dataclass", [isinstance(field_type, DataClassType)
        # for field_type in field_types])
        field_values = [
            trycast(field_value, field_type)
            for field_type, field_value in zip(field_types, field_values)
        ]
        field_value_bits = []
        for field_value in field_values:
            bitsified = to_bits_aggregate(field_value)
            field_value_bits.append(bitsified)
        # field_value_bits = [to_bits_aggregate(field_value)
        # for field_value in field_values]
        ret_bits = BitVector().join(field_value_bits)
    elif isinstance(convertible_object, Iterable):
        for unit in convertible_object:
            ret_bits.extend(to_bits_aggregate(unit))
    else:
        raise Exception(
            f"Cannot convert {convertible_object} to bits because the unit type"
            f" is not a CType, YType, or PyType"
        )
    # except Exception as e:
    #     raise Exception(f"Cannot convert {convertible_object} to bits.\n
    #                     f"Next-level error: {e}") from e

    return ret_bits


def from_bits_aggregate(
    unitbits: BitVector, aggregate_type: type
) -> Union[UnitType, AggregateTypeByteConvertible]:
    """
    Function to convert a collection of BitVector objects into Python primitives,\
        ctypes objects, BitTypes, or a dataclass of those types.

    Essentially a bitfield deserializer.

    Args:
        unitbits (BitVector): The BitVector object to convert to a Python primitive,\
            ctypes object, BitType, or dataclass.
        aggregate_type (type): The type(s) of the object to convert to.
            Must be a member of UnitType or a dataclass annotated with UnitType members.

    Returns:
        Union[UnitType, AggregateTypeByteConvertible]: The object(s)
            represented by the bits.
    """
    if is_subclass_of_union(aggregate_type, UnitType):
        return from_bits_individual(unitbits, aggregate_type)
    else:
        size_in_bits = count_bits_in_aggregate_type(aggregate_type)
        # print("unitbits type", type(unitbits))
        # print(unitbits)
        if len(unitbits) != size_in_bits:
            raise Exception(
                f"Cannot convert {unitbits} to {aggregate_type}"
                f" because the number of bits in the bits object ({unitbits.num_bits})"
                f" does not match the number of bits in the unit type ({size_in_bits})"
            )

        read_fields = list()
        field_types = resolve_field_types(aggregate_type)
        for field in dataclasses.fields(aggregate_type):
            field_type = field_types[field.name]

            field_size_in_bits = count_bits_in_unit_type(field_type)
            field_bits = unitbits[:field_size_in_bits]
            field_value = from_bits_aggregate(field_bits, field_type)
            read_fields.append(field_value)
            unitbits = unitbits[field_size_in_bits:]
        retval = aggregate_type(*read_fields)

    return retval


def to_bytes_aggregate(
    units: AggregateTypeByteConvertible,
    endianness: Literal["big", "little"] = "big",
) -> bytes:
    """
    Function to convert a collection of Python primitives or ctypes objects into bytes.

    Essentially a bitfield serializer.

    Args:
        units [Iterable | DataClassType]): The objects to convert to bytes
        endianness: The byte order of the output.
            Defaults to "big".

    Returns:
        bytes: The bytes representation of the objects
    """
    ret_bytes = bytearray()

    if is_instance_of_union(units, UnitType):
        ret_bytes = to_bytes_individual(units, endianness=endianness)

    elif isinstance(units, DataClassType):
        field_types = resolve_field_types(type(units))
        for field in dataclasses.fields(units):
            field_type = field_types[field.name]
            field_value = getattr(units, field.name)
            field_value = trycast(field_value, field_type)
            field_value_bytes = to_bytes_aggregate(field_value, endianness=endianness)
            ret_bytes.extend(field_value_bytes)

    elif isinstance(units, Iterable):
        for unit in units:
            ret_bytes.extend(to_bytes_aggregate(unit, endianness=endianness))

    return bytes(ret_bytes)


def from_bytes_aggregate(
    bytes_obj: bytes,
    aggregate_type: type,
    is_array=False,
    endianness: Literal["big", "little"] = "big",
) -> Union[UnitType, AggregateTypeByteConvertible]:
    """
    Function to convert a collection of bytes into Python primitives, ctypes objects,\
        BitTypes, or a dataclass of those types.

    Essentially a bitfield deserializer.

    Args:
        bytes_obj (bytes): The bytes object to convert to a Python primitive,
            ctypes object, BitType, or dataclass.
        aggregate_type (type): The type(s) of the object to convert to.
            Must be a member of UnitType or a dataclass annotated with UnitType members.
        is_array (bool, optional): Whether the object is an array of the aggregate type.
            Defaults to False.
        endianness: The byte order of the input bytes.
            Defaults to "big".

    Returns:
        Union[UnitType, AggregateTypeByteConvertible]: The object(s) represented by
            the bytes.
    """
    if is_subclass_of_union(aggregate_type, UnitType):
        return from_bytes_individual(bytes_obj, aggregate_type, endianness=endianness)
    else:
        size_in_bits = count_bits_in_unit_type(aggregate_type)

        if not is_array:
            if len(bytes_obj) * 8 != size_in_bits:
                raise Exception(
                    f"Cannot convert {bytes_obj} to {aggregate_type}"
                    f" because the # of bits in the bytes object ({len(bytes_obj) * 8})"
                    f" does not match the # of bits in the unit type ({size_in_bits})"
                )

            read_fields = list()
            field_types = resolve_field_types(aggregate_type)
            for field in dataclasses.fields(aggregate_type):
                field_type = field_types[field.name]
                field_size_in_bytes = (count_bits_in_unit_type(field_type) + 7) // 8
                field_bytes = bytes_obj[:field_size_in_bytes]
                field_value = from_bytes_aggregate(
                    field_bytes, field_type, endianness=endianness
                )
                read_fields.append(field_value)
                bytes_obj = bytes_obj[field_size_in_bytes:]
            retval = aggregate_type(*read_fields)

        else:
            arr_entry_list = list()
            size_in_bytes = (size_in_bits + 7) // 8
            for i in range(0, len(bytes_obj), size_in_bytes):
                endindex = (
                    i + size_in_bytes
                    if i + size_in_bytes < len(bytes_obj)
                    else len(bytes_obj)
                )
                arr_entry_list.append(
                    from_bytes_aggregate(
                        bytes_obj[i:endindex],
                        aggregate_type,
                        endianness=endianness,
                    )
                )
            retval = aggregate_type(*arr_entry_list)

    return retval
