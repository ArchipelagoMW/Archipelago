from __future__ import annotations

import abc
from enum import IntEnum
from typing import TYPE_CHECKING, Any, ClassVar, Self  # Self py 3.11+

if TYPE_CHECKING:
    from .responses import ErrorResponse


__all__ = [
    "ErrorType", "PolyEmuBaseError", "NotConnectedError",
    "ConnectionLostError", "MalformedResponseError", "MalformedRequestError",
    "AutoPolyEmuErrorRegister", "PolyEmuError", "UnsupportedOperationError",
    "MismatchedDeviceError", "NoSuchDeviceError", "DeviceClosedConnectionError",
]


class ErrorType(IntEnum):
    DEVICE_ERROR = 0x00
    UNSUPPORTED_OPERATION = 0x01
    MISMATCHED_DEVICE = 0x02
    NO_SUCH_DEVICE = 0x80
    DEVICE_CLOSED_CONNECTION = 0x81
    UNKNOWN = 0xFF


class PolyEmuBaseError(Exception):
    pass


class NotConnectedError(PolyEmuBaseError):
    pass


class ConnectionLostError(PolyEmuBaseError):
    pass


class MalformedResponseError(PolyEmuBaseError):
    pass


class MalformedRequestError(PolyEmuBaseError):
    pass


class AutoPolyEmuErrorRegister(abc.ABCMeta):
    exception_types: ClassVar[dict[int, PolyEmuError]] = {}

    def __new__(cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> AutoPolyEmuErrorRegister:
        new_class = super().__new__(cls, name, bases, namespace)

        # Register error type
        if "code" in namespace:
            AutoPolyEmuErrorRegister.exception_types[namespace["code"]] = new_class

        return new_class

    @staticmethod
    def get_error_type(code: int) -> type[PolyEmuError]:
        try:
            return AutoPolyEmuErrorRegister.exception_types[code]
        except KeyError:
            return AutoPolyEmuErrorRegister.exception_types[ErrorType.UNKNOWN]


class PolyEmuError(PolyEmuBaseError, abc.ABC, metaclass=AutoPolyEmuErrorRegister):
    code: ClassVar[int]

    @classmethod
    @abc.abstractmethod
    def from_response(cls, response: "ErrorResponse") -> Self:
        ...


class UnsupportedOperationError(PolyEmuError):
    code = ErrorType.UNSUPPORTED_OPERATION

    @classmethod
    def from_response(cls, response) -> Self:
        context = f"0x{hex(response.error_context[0])}" if response.error_context else "Unknown"
        return cls(f"Device does not support request type: {context}")


class MismatchedDeviceError(PolyEmuError):
    code = ErrorType.MISMATCHED_DEVICE

    @classmethod
    def from_response(cls, response) -> Self:
        return cls(f"Requests sent to wrong device. Expected [{response.error_context[:8]}] but got [{response.error_context[8:]}]")


class NoSuchDeviceError(PolyEmuError):
    code = ErrorType.NO_SUCH_DEVICE

    @classmethod
    def from_response(cls, response) -> Self:
        return cls(f"Device does not appear to exist: {response.error_context}")


class DeviceClosedConnectionError(PolyEmuError):
    code = ErrorType.DEVICE_CLOSED_CONNECTION

    @classmethod
    def from_response(cls, response) -> Self:
        return cls(f"Device closed the connection without sending response")
