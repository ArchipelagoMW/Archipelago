import asyncio

from ...core.adapter import Adapter
from ...core.errors import NotConnectedError, ConnectionLostError
from .broker import CLIENT_PORT


__all__ = [
    "DefaultAdapter",
]


async def launch_broker():
    import subprocess
    from Launcher import get_exe
    import Utils
    launcher = get_exe("Launcher")
    await asyncio.create_subprocess_exec(
        launcher[0], *launcher[1:], "PolyEmu Connection Broker",
        start_new_session=True,
        creationflags=subprocess.DETACHED_PROCESS if Utils.is_windows else 0,
    )


class DefaultAdapter(Adapter):
    name = "Default Adapter"

    _streams: tuple[asyncio.StreamReader, asyncio.StreamWriter] | None
    _lock: asyncio.Lock

    def __init__(self):
        super().__init__()
        self._streams = None
        self._lock = asyncio.Lock()

    def is_connected(self):
        return self._streams is not None

    async def try_connect(self) -> tuple[asyncio.StreamReader, asyncio.StreamWriter] | None:
        try:
            reader, writer = await asyncio.open_connection("127.0.0.1", CLIENT_PORT)
            return reader, writer
        except (ConnectionRefusedError, ConnectionResetError, OSError):
            return None

    async def connect(self):
        streams = await self.try_connect()

        # Try starting the connection broker process and connect again
        if streams is None:
            await launch_broker()
            await asyncio.sleep(5)  # Give the broker time to start up
            streams = await self.try_connect()
            if streams is None:
                return False

        self._streams = streams
        return True

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
