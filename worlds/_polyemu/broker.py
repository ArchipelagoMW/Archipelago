import asyncio
import logging
import typing


CLIENT_PORT = 43030
DEVICE_PORT = 43031
_INACTIVITY_TIMEOUT = 10


class PolyEmuDeviceConnection:
    id: bytes | None
    name: str
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter
    close_cb: typing.Callable[[], None] | None

    def __init__(self, name: str, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self.id = None
        self.name = name
        self.reader = reader
        self.writer = writer
        self.close_cb = None

    async def request_id(self) -> bytes | None:
        msg = bytes([0] * 8) + b"\x04"

        res = await self.send_request(msg)
        if res[0] != 0x84:
            return None

        assert res[1] == 1

        self.id = res[2:10]
        return self.id

    def set_on_close(self, cb: typing.Callable[[], None] | None) -> None:
        self.close_cb = cb

    async def send_request(self, msg: bytes) -> bytes:
        """Do not include message size header"""
        msg = len(msg).to_bytes(2, "big") + msg
        try:
            self.writer.write(msg)
            await self.writer.drain()

            data_size = await self.reader.read(2)
            if len(data_size) == 0:
                raise ConnectionResetError()  # TODO: Figure this out

            data_size = int.from_bytes(data_size, "big")
            data = await self.reader.read(data_size)
            if len(data) == 0:
                raise ConnectionResetError()  # TODO: Figure this out

            return data
        except asyncio.TimeoutError:
            logging.info(f"({self.name}) Device timeout")
        except (asyncio.CancelledError, ConnectionResetError, BrokenPipeError):
            logging.info(f"({self.name}) Device closed connection")

        logging.info(f"({self.name}) Device disconnected")
        self.writer.close()
        try:
            await self.writer.wait_closed()
        except (ConnectionResetError, ConnectionAbortedError):
            pass
        finally:
            if self.close_cb is not None:
                self.close_cb()

            return bytes([0xFF, 0x81, 0x00, 0x00])  # Error, device did not respond

class PolyEmuBroker:
    clients: dict[str, tuple[asyncio.StreamReader, asyncio.StreamWriter]]
    devices: dict[bytes, PolyEmuDeviceConnection]
    activity_event: asyncio.Event
    client_server: asyncio.Server | None
    device_server: asyncio.Server | None

    def __init__(self):
        self.clients = {}
        self.devices = {}
        self.activity_event = asyncio.Event()
        self.client_server = None
        self.device_server = None

    def process_requests(self, data: bytes) -> bytes:
        if data[8] == 0x00:
            res = bytes([0x80])
            return res
        elif data[8] == 0x04:
            res = bytes([0x84]) + len(self.devices).to_bytes(1, "big")
            for device_id in self.devices.keys():
                res += device_id
            return res
        raise Exception(f"Can't handle request: {' '.join(hex(d) for d in data)}")

    async def handle_client_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        address = writer.get_extra_info("peername")
        client_name = f"{address[0]}:{address[1]}"
        logging.info(f"({client_name}) Client connected")
        self.clients[client_name] = (reader, writer)

        try:
            while True:
                data_size = await reader.read(2)
                if len(data_size) == 0:
                    raise Exception("ASdf")

                data_size = int.from_bytes(data_size, "big")
                data = await reader.read(data_size)
                if len(data) == 0:
                    raise Exception("ASdf")

                self.activity_event.set()
                logging.debug(f"({client_name}) Message received: {data}")

                device_id = data[0:8]
                if device_id == b"\x00\x00\x00\x00\x00\x00\x00\x00":
                    res = self.process_requests(data)
                elif device_id in self.devices:
                    res = await self.devices[device_id].send_request(data)
                else:
                    res = bytes([0xFF, 0x80]) + len(device_id).to_bytes(2, "big") + device_id

                res = len(res).to_bytes(2, "big") + res
                writer.write(res)
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
        logging.info(f"({device_name}) New device connected")

        device = PolyEmuDeviceConnection(device_name, reader, writer)
        device_id = await device.request_id()
        if device_id is None:
            return

        device.set_on_close(self.get_unregister_device_cb(device_id))
        self.devices[device_id] = device
        logging.info(f"({device_name}) Device identity set: {device_id}")

    def get_unregister_device_cb(self, device_id: bytes):
        def cb():
            del self.devices[device_id]
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
