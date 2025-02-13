import asyncio
import logging
# import os
import typing
# import sys

# sys.path.remove(os.path.dirname(__file__))
# polyemu_root = os.path.normpath(os.path.join(os.path.dirname(__file__)))
# os.chdir(polyemu_root)
# sys.path.append(polyemu_root)

from .core.requests import RequestChain, RequestType, RequestChainHeader, ListDevicesRequest
from .core.responses import ResponseChain, ResponseType, ResponseChainHeader, Response, NoOpResponse, ListDevicesResponse, ErrorResponse
from .core.errors import ErrorType


CLIENT_PORT = 43030
DEVICE_PORT = 43031
_INACTIVITY_TIMEOUT = 10


class PolyEmuDeviceConnection:
    id: bytes | None
    name: str
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter
    close_cb: typing.Callable[[], None] | None
    logger: logging.Logger

    def __init__(self, name: str, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, logger: logging.Logger):
        self.logger = logger
        self.id = None
        self.name = name
        self.reader = reader
        self.writer = writer
        self.close_cb = None

    async def request_id(self) -> bytes | None:
        msg = RequestChain(RequestChainHeader(bytes([0] * 8)), [ListDevicesRequest()]).to_bytes()

        received = await self.send_msg(msg)
        response = ResponseChain.from_bytes(received).responses[0]

        if response.type != ResponseType.LIST_DEVICES:
            return None
        assert isinstance(response, ListDevicesResponse)

        self.id = response.devices[0]
        return self.id

    def set_on_close(self, cb: typing.Callable[[], None] | None) -> None:
        self.close_cb = cb

    async def send_msg(self, msg: bytes) -> bytes:
        """Do not include message size"""
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
            self.logger.info(f"({self.name}) Device timeout")
        except (asyncio.CancelledError, ConnectionResetError, BrokenPipeError):
            self.logger.info(f"({self.name}) Device closed connection")

        self.logger.info(f"({self.name}) Device disconnected")
        self.writer.close()
        try:
            await self.writer.wait_closed()
        except (ConnectionResetError, ConnectionAbortedError):
            pass
        finally:
            if self.close_cb is not None:
                self.close_cb()

            return ErrorResponse(ErrorType.DEVICE_CLOSED_CONNECTION).to_bytes()


class Broker:
    clients: dict[str, tuple[asyncio.StreamReader, asyncio.StreamWriter]]
    devices: dict[bytes, PolyEmuDeviceConnection]
    activity_event: asyncio.Event
    client_server: asyncio.Server | None
    device_server: asyncio.Server | None
    logger: logging.Logger

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.clients = {}
        self.devices = {}
        self.activity_event = asyncio.Event()
        self.client_server = None
        self.device_server = None

    def process_requests(self, data: bytes) -> bytes:
        request_chain = RequestChain.from_bytes(data)
        responses: list[Response] = []
        for request in request_chain.requests:
            if request.type == RequestType.NO_OP:
                response = NoOpResponse()
            elif request.type == RequestType.LIST_DEVICES:
                response = ListDevicesResponse(list(self.devices.keys()))
            else:
                response = ErrorResponse(ErrorType.UNSUPPORTED_OPERATION, bytes([request.type]))

            responses.append(response)

        return ResponseChain(ResponseChainHeader(), responses).to_bytes()

    async def handle_client_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        address = writer.get_extra_info("peername")
        client_name = f"{address[0]}:{address[1]}"
        self.logger.info(f"({client_name}) Client connected")
        self.clients[client_name] = (reader, writer)

        try:
            while True:
                data_size = await reader.read(2)
                if len(data_size) == 0:
                    raise Exception("ASdf")

                data_size = int.from_bytes(data_size, "big")
                incoming_msg = await reader.read(data_size)
                if len(incoming_msg) == 0:
                    raise Exception("ASdf")

                self.activity_event.set()
                self.logger.info(f"({client_name}) Message received: {incoming_msg}")

                device_id = incoming_msg[0:8]
                if device_id == b"\x00\x00\x00\x00\x00\x00\x00\x00":
                    msg_to_client = self.process_requests(incoming_msg)
                elif device_id in self.devices:
                    msg_to_client = await self.devices[device_id].send_msg(incoming_msg)
                else:
                    msg_to_client = ErrorResponse(ErrorType.NO_SUCH_DEVICE, device_id).to_bytes()

                msg_to_client = len(msg_to_client).to_bytes(2, "big") + msg_to_client
                writer.write(msg_to_client)
                await writer.drain()
        except asyncio.TimeoutError:
            self.logger.info(f"({client_name}) Client timeout")
        except (asyncio.CancelledError, ConnectionResetError, BrokenPipeError):
            self.logger.info(f"({client_name}) Client closed connection")
        finally:
            self.logger.info(f"({client_name}) Client disconnected")
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
        self.logger.info(f"({device_name}) New device connected")

        device = PolyEmuDeviceConnection(device_name, reader, writer, self.logger)
        device_id = await device.request_id()
        if device_id is None:
            return

        device.set_on_close(self.get_unregister_device_cb(device_id))
        self.devices[device_id] = device
        self.logger.info(f"({device_name}) Device identity set: {device_id}")

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
                self.logger.info("No activity. Shutting down.")
                self.client_server.close()
                self.device_server.close()
                await self.client_server.wait_closed()
                await self.device_server.wait_closed()
                break

    async def start(self):
        self.logger.info("Starting servers")
        self.client_server = await asyncio.start_server(self.handle_client_connection, "127.0.0.1", CLIENT_PORT)
        self.device_server = await asyncio.start_server(self.handle_device_connection, "127.0.0.1", DEVICE_PORT)
        self.logger.info("Servers running")

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


def start_broker(*args):
    logger = logging.getLogger("Broker")
    broker = Broker(logger)
    try:
        asyncio.run(broker.start())
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt. Exiting.")


# def init_logging(log_directory: str):
#     import datetime

#     # Log uncaught exceptions
#     original_excepthook = sys.excepthook
#     def wrapped_excepthook(exc_type, exc_value, exc_traceback):
#         if issubclass(exc_type, KeyboardInterrupt):
#             sys.__excepthook__(exc_type, exc_value, exc_traceback)
#             return
#         logging.getLogger().exception("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback), extra={"NoStream": True})
#         return original_excepthook(exc_type, exc_value, exc_traceback)
#     sys.excepthook = wrapped_excepthook

#     # Create logfile
#     os.makedirs(log_directory, exist_ok=True)
#     logger = logging.getLogger()
#     logger.setLevel(logging.INFO)
#     file_handler = logging.FileHandler(os.path.join(log_directory, f"PolyEmuBroker_{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.txt"), "w", encoding="utf-8-sig")
#     file_handler.setFormatter(logging.Formatter("[%(name)s at %(asctime)s]: %(message)s"))
#     logger.addHandler(file_handler)


# if __name__ == "__main__":
#     import argparse
#     parser = argparse.ArgumentParser(description="a connection broker for PolyEmu Client")
#     parser.add_argument("--log_directory", type=str, help="the directory to store log files")
#     args = parser.parse_args()

#     init_logging(args.log_directory)
#     logging.info("Logging initialized")
#     start_broker(logging.getLogger())
