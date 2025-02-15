import abc


__all__ = (
    "Connector",
)


class Connector(abc.ABC):
    @abc.abstractmethod
    def is_connected(self) -> bool:
        ...

    @abc.abstractmethod
    async def connect(self) -> bool:
        ...

    @abc.abstractmethod
    async def disconnect(self) -> None:
        ...

    @abc.abstractmethod
    async def send_message(self, message: bytes) -> bytes:
        ...
