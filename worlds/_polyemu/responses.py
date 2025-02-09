from __future__ import annotations

import abc
from typing import Any, ClassVar, Self, Sequence, Type  # Self py 3.11+

from .enums import PLATFORMS, PlatformEnum, RequestType, ResponseType


RESPONSE_HEADER_SIZE = 1


class ResponseBuffer(bytes):
    cursor: int

    def __init__(self):
        super().__init__()
        self.cursor = 0

    def reached_end(self):
        return self.cursor >= len(self)

    def consume_bytes(self, size: int) -> bytes:
        ret = self[self.cursor:self.cursor + size]
        self.cursor = self.cursor + size
        return ret

    def consume_int(self, size: int) -> int:
        ret = int.from_bytes(self[self.cursor:self.cursor + size], "big")
        self.cursor = self.cursor + size
        return ret


class AutoResponseRegister(abc.ABCMeta):
    response_types: ClassVar[dict[int, Response]] = {}

    def __new__(cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> AutoResponseRegister:
        new_class = super().__new__(cls, name, bases, namespace)

        # Register response type
        if "type" in namespace:
            AutoResponseRegister.response_types[namespace["type"]] = new_class

        return new_class

    @staticmethod
    def get_response_type(code: int) -> Type[Response]:
        try:
            return AutoResponseRegister.response_types[code]
        except KeyError:
            raise KeyError(f"Response code [{hex(code)}] does not have a corresponding response type")

    @staticmethod
    def convert_message_chain(msg: bytes) -> list[Response]:
        buffer = ResponseBuffer(msg)
        responses: list[Response] = []
        while not buffer.reached_end():
            response_header = buffer.consume_bytes(RESPONSE_HEADER_SIZE)
            response = AutoResponseRegister.get_response_type(response_header[0]).consume_response_body(response_header, buffer)
            responses.append(response)
        return responses


class Response(abc.ABC, metaclass=AutoResponseRegister):
    type: ClassVar[int]

    @staticmethod
    @abc.abstractmethod
    def consume_response_body(header: bytes, buffer: ResponseBuffer) -> Self:
        ...


class NoOpResponse(Response):
    type = ResponseType.NO_OP

    @staticmethod
    def consume_response_body(header, buffer: ResponseBuffer) -> NoOpResponse:
        assert header[0] == NoOpResponse.type
        return NoOpResponse()


class SupportedOperationsResponse(Response):
    type = ResponseType.PLATFORM

    supported_operations: list[int]

    def __init__(self, supported_operations: Sequence[int]):
        self.supported_operations = list(supported_operations)

    @staticmethod
    def consume_response_body(header, buffer: ResponseBuffer) -> SupportedOperationsResponse:
        assert header[0] == SupportedOperationsResponse.type
        return SupportedOperationsResponse(buffer.consume_bytes(buffer.consume_int(1)))


class PlatformResponse(Response):
    type = ResponseType.PLATFORM

    platform_id: PlatformEnum

    def __init__(self, platform_id: int):
        self.platform_id = PLATFORMS.get_by_id(platform_id)

    @staticmethod
    def consume_response_body(header, buffer: ResponseBuffer) -> PlatformResponse:
        assert header[0] == PlatformResponse.type
        return PlatformResponse(buffer.consume_int(1))


class GameIdResponse(Response):
    type = ResponseType.GAME_ID

    game_id: bytes

    def __init__(self, game_id: bytes):
        self.game_id = game_id

    @staticmethod
    def consume_response_body(header, buffer: ResponseBuffer) -> GameIdResponse:
        assert header[0] == PlatformResponse.type
        return PlatformResponse(buffer.consume_bytes(8))


class MemorySizeResponse(Response):
    type = ResponseType.MEMORY_SIZE

    memory_sizes: dict[int, int]

    def __init__(self, memory_sizes: dict[int, int]):
        self.memory_sizes = memory_sizes

    @staticmethod
    def consume_response_body(header, buffer: ResponseBuffer) -> MemorySizeResponse:
        assert header[0] == PlatformResponse.type
        num_entries = buffer.consume_int(1)
        sizes = {}
        for i in range(num_entries):
            sizes[buffer.consume_int(1)] = buffer.consume_int(8)
        return MemorySizeResponse(sizes)


class ReadResponse(Response):
    type = ResponseType.READ

    data: bytes

    def __init__(self, data: bytes):
        self.data = data

    @staticmethod
    def consume_response_body(header, buffer: ResponseBuffer) -> ReadResponse:
        assert header[0] == ReadResponse.type
        return ReadResponse(buffer.consume_bytes(buffer.consume_int(2)))


class WriteResponse(Response):
    type = ResponseType.WRITE

    @staticmethod
    def consume_response_body(header, buffer: ResponseBuffer) -> WriteResponse:
        assert header[0] == WriteResponse.type
        return WriteResponse()


class GuardResponse(Response):
    type = ResponseType.GUARD

    validated: bool

    def __init__(self, validated: bool):
        self.validated = validated

    @staticmethod
    def consume_response_body(header, buffer: ResponseBuffer) -> GuardResponse:
        assert header[0] == GuardResponse.type
        return GuardResponse(buffer.consume_int(1) != 0)


class LockResponse(Response):
    type = ResponseType.LOCK

    @staticmethod
    def consume_response_body(header, buffer: ResponseBuffer) -> LockResponse:
        assert header[0] == LockResponse.type
        return LockResponse()


class UnlockResponse(Response):
    type = ResponseType.LOCK

    @staticmethod
    def consume_response_body(header, buffer: ResponseBuffer) -> UnlockResponse:
        assert header[0] == UnlockResponse.type
        return UnlockResponse()


class DisplayMessageResponse(Response):
    type = ResponseType.LOCK

    @staticmethod
    def consume_response_body(header, buffer: ResponseBuffer) -> DisplayMessageResponse:
        assert header[0] == DisplayMessageResponse.type
        return DisplayMessageResponse()


class ErrorResponse(Response):
    type = ResponseType.ERROR

    error_code: int
    error_context: bytes

    def __init__(self, code: int, context: bytes):
        self.error_code = code
        self.error_context = context

    @staticmethod
    def consume_response_body(header, buffer: ResponseBuffer) -> ErrorResponse:
        assert header[0] == ErrorResponse.type
        return ErrorResponse(buffer.consume_int(1), buffer.consume_bytes(buffer.consume_int(2)))
