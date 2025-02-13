import abc
import asyncio

from .errors import NotConnectedError, ConnectionLostError


__all__ = (
    "Connector", "BrokerConnector",
)


BROKER_CLIENT_PORT = 43030


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


class BrokerConnector(Connector):
    _streams: tuple[asyncio.StreamReader, asyncio.StreamWriter] | None
    _lock: asyncio.Lock

    def __init__(self):
        super().__init__()
        self._streams = None
        self._lock = asyncio.Lock()

    def is_connected(self):
        return self._streams is not None

    async def connect(self):
        try:
            self._streams = await asyncio.open_connection("127.0.0.1", BROKER_CLIENT_PORT)
            return True
        except (TimeoutError, ConnectionRefusedError):
            self._streams = None
            return False

    async def disconnect(self):
        if self._streams is not None:
            self._streams[1].close()

            try:
                await self._streams[1].wait_closed()
            except:
                pass
            finally:
                self._streams = None

    async def send_message(self, message) -> bytes:
        message = len(message).to_bytes(2, "big") + message

        async with self._lock:
            if self._streams is None:
                raise NotConnectedError()

            try:
                reader, writer = self._streams
                writer.write(message)
                await asyncio.wait_for(writer.drain(), timeout=5)

                response_size = await asyncio.wait_for(reader.read(2), timeout=5)
                if response_size == b"":
                    await self.disconnect()
                    raise ConnectionLostError("Connection closed")

                data = await asyncio.wait_for(reader.read(int.from_bytes(response_size, "big")), timeout=5)
                if data == b"":
                    await self.disconnect()
                    raise ConnectionLostError("Connection closed")

                return data
            except asyncio.TimeoutError as exc:
                await self.disconnect()
                raise ConnectionLostError("Connection timed out") from exc
            except ConnectionResetError as exc:
                await self.disconnect()
                raise ConnectionLostError("Connection reset") from exc
