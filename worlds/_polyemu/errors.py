from __future__ import annotations

import abc
from typing import Any, ClassVar, Self, Type  # Self py 3.11+

from .enums import PolyEmuErrorType
from .responses import ErrorResponse


class PolyEmuBaseError(Exception):
    pass


class NotConnectedError(PolyEmuBaseError):
    pass


class RequestFailedError(PolyEmuBaseError):
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
    def get_error_type(code: int) -> Type[PolyEmuError]:
        try:
            return AutoPolyEmuErrorRegister.exception_types[code]
        except KeyError:
            return AutoPolyEmuErrorRegister.exception_types[PolyEmuErrorType.UNKNOWN]


class PolyEmuError(PolyEmuBaseError, abc.ABC, metaclass=AutoPolyEmuErrorRegister):
    code: ClassVar[int]

    @classmethod
    @abc.abstractmethod
    def from_response(cls, response: ErrorResponse) -> Self:
        ...


class UnsupportedOperationError(PolyEmuError):
    code = PolyEmuErrorType.UNSUPPORTED_OPERATION

    @classmethod
    def from_response(cls, response) -> Self:
        context = f"0x{hex(response.error_context[0])}" if response.error_context else "Unknown"
        return cls(f"Device does not support request type: {context}")
