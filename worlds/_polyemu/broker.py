import asyncio
import logging
import typing


CLIENT_PORT = 43030
DEVICE_PORT = 43031
_INACTIVITY_TIMEOUT = 10


def create_error():
    msg = bytearray([0xFF])
    return len(msg).to_bytes(2, "big") + msg


class PolyEmuDeviceConnection:
    name: str
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter
    close_cb: typing.Callable[[], None] | None

    def __init__(self, name: str, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, close_cb: typing.Callable[[], None] | None = None):
        self.name = name
        self.reader = reader
        self.writer = writer
        self.close_cb = close_cb

    async def send_request(self, msg: bytes) -> bytes:
        try:
            self.writer.write(msg)
            await self.writer.drain()
            return await self.reader.read(1024)
        except asyncio.TimeoutError:
            logging.info(f"({self.name}) Device timeout")
        except (asyncio.CancelledError, ConnectionResetError, BrokenPipeError):
            logging.info(f"({self.name}) Device closed connection")

        logging.info(f"({self.name}) Device disconnected")
        self.writer.close()
        try:
            await self.writer.wait_closed()
        except ConnectionResetError:
            pass
        finally:
            if self.close_cb is not None:
                self.close_cb()


class PolyEmuBroker:
    clients: dict[str, tuple[asyncio.StreamReader, asyncio.StreamWriter]]
    devices: dict[str, PolyEmuDeviceConnection]
    activity_event: asyncio.Event
    client_server: asyncio.Server | None
    device_server: asyncio.Server | None

    def __init__(self):
        self.clients = {}
        self.devices = {}
        self.activity_event = asyncio.Event()
        self.client_server = None
        self.device_server = None

    async def handle_client_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        address = writer.get_extra_info("peername")
        client_name = f"{address[0]}:{address[1]}"
        logging.info(f"({client_name}) Client connected")
        self.clients[client_name] = (reader, writer)

        try:
            while data := await reader.read(1024):
                self.activity_event.set()
                logging.debug(f"({client_name}) Message received: {data}")
                if len(self.devices):
                    res = await list(self.devices.values())[0].send_request(data)
                    writer.write(res)
                else:
                    writer.write(create_error())
                await writer.drain()
        except asyncio.TimeoutError:
            logging.info(f"({client_name}) Client timeout")
        except (asyncio.CancelledError, ConnectionResetError, BrokenPipeError):
            logging.info(f"({client_name}) Client closed connection")
        finally:
            logging.info(f"({client_name}) Client disconnected")
            del self.clients[client_name]
            writer.close()
            try:
                await writer.wait_closed()
            except ConnectionResetError:
                pass

    async def handle_device_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self.activity_event.set()
        device_name = writer.get_extra_info("peername")
        device_name = f"{device_name[0]}:{device_name[1]}"
        logging.info(f"({device_name}) Device connected")
        self.devices[device_name] = PolyEmuDeviceConnection(device_name, reader, writer, self.get_unregister_device_cb(device_name))
        while True:
            await asyncio.sleep(1)

    def get_unregister_device_cb(self, device_name: str):
        def cb():
            del self.devices[device_name]
        return cb

    async def monitor_inactivity(self):
        while True:
            try:
                await asyncio.wait_for(self.activity_event.wait(), timeout=_INACTIVITY_TIMEOUT)
                self.activity_event.clear()  # Activity occurred, reset timer
            except asyncio.TimeoutError:
                logging.info("No activity. Shutting down.")
                self.client_server.close()
                self.device_server.close()
                await self.client_server.wait_closed()
                await self.device_server.wait_closed()
                break

    async def start(self):
        logging.info("Starting servers")
        self.client_server = await asyncio.start_server(self.handle_client_connection, "127.0.0.1", CLIENT_PORT)
        self.device_server = await asyncio.start_server(self.handle_device_connection, "127.0.0.1", DEVICE_PORT)
        logging.info("Servers running")

        try:
            await asyncio.gather(
                self.client_server.serve_forever(),
                self.device_server.serve_forever(),
                self.monitor_inactivity()
            )
        except asyncio.CancelledError:
            pass
        finally:
            self.client_server.close()
            self.device_server.close()
            await self.client_server.wait_closed()
            await self.device_server.wait_closed()


def init_logging(log_directory: str):
    import datetime
    import os
    import sys

    # Log uncaught exceptions
    original_excepthook = sys.excepthook
    def wrapped_excepthook(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logging.getLogger().exception("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback), extra={"NoStream": True})
        return original_excepthook(exc_type, exc_value, exc_traceback)
    sys.excepthook = wrapped_excepthook

    # Create logfile
    os.makedirs(log_directory, exist_ok=True)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(os.path.join(log_directory, f"PolyEmuBroker_{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.txt"), "w", encoding="utf-8-sig")
    file_handler.setFormatter(logging.Formatter("[%(name)s at %(asctime)s]: %(message)s"))
    logger.addHandler(file_handler)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="a connection broker for PolyEmu Client")
    parser.add_argument("--log_directory", type=str, help="the directory to store log files")
    args = parser.parse_args()

    init_logging(args.log_directory)
    logging.info("Logging initialized")

    broker = PolyEmuBroker()
    try:
        asyncio.run(broker.start())
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt. Exiting.")
