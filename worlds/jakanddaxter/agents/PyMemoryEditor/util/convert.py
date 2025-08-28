# -*- coding: utf-8 -*-

from typing import Type, TypeVar
import ctypes


T = TypeVar("T")


def convert_from_byte_array(byte_array: ctypes.Array, pytype: Type[T], length: int) -> T:
    """
    Convert a byte array to a Python type.
    """
    if pytype is bytes: return bytes(byte_array)
    if pytype is str: return bytes(byte_array).decode()

    c_value = get_c_type_of(pytype, length)

    return c_value.__class__.from_buffer(byte_array).value


def get_c_type_of(pytype: Type, length) -> ctypes._SimpleCData:
    """
    Return a C type of a primitive type of the Python language.
    """
    if pytype is str or pytype is bytes: return ctypes.create_string_buffer(length)

    elif pytype is int:

        if length == 1: return ctypes.c_int8()      # 1 Byte
        if length == 2: return ctypes.c_int16()     # 2 Bytes
        if length <= 4: return ctypes.c_int32()     # 4 Bytes
        return ctypes.c_int64()                     # 8 Bytes

    elif pytype is float:

        if length == 4: return ctypes.c_float()     # 4 Bytes
        return ctypes.c_double()                    # 8 Bytes

    elif pytype is bool: return ctypes.c_bool()

    else: raise ValueError("The type must be bool, int, float, str or bytes.")
