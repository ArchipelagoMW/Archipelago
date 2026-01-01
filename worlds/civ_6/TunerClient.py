import asyncio
from logging import Logger
import socket
from typing import Any

ADDRESS = "127.0.0.1"
PORT = 4318

CLIENT_PREFIX = "APSTART:"
CLIENT_POSTFIX = ":APEND"


def decode_mixed_string(data: bytes) -> str:
    return "".join(chr(b) if 32 <= b < 127 else "?" for b in data)


class TunerException(Exception):
    pass


class TunerTimeoutException(TunerException):
    pass


class TunerErrorException(TunerException):
    pass


class TunerConnectionException(TunerException):
    pass


class TunerClient:
    """Interfaces with Civilization via the tuner socket"""
    logger: Logger

    def __init__(self, logger: Logger):
        self.logger = logger

    def __parse_response(self, response: str) -> str:
        """Parses the response from the tuner socket"""
        split = response.split(CLIENT_PREFIX)
        if len(split) > 1:
            start = split[1]
            end = start.split(CLIENT_POSTFIX)[0]
            return end
        elif "ERR:" in response:
            raise TunerErrorException(response.replace("?", ""))
        else:
            return ""

    async def send_game_command(self, command_string: str, size: int = 64):
        """Small helper that prefixes a command with GameCore.Game."""
        return await self.send_command("GameCore.Game." + command_string, size)

    async def send_command(self, command_string: str, size: int = 64):
        """Send a raw commannd"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)

        b_command_string = command_string.encode("utf-8")

        # Send data to the server
        command_prefix = b"CMD:0:"
        delimiter = b"\x00"
        full_command = b_command_string
        message = command_prefix + full_command + delimiter
        message_length = len(message).to_bytes(1, byteorder="little")

        # game expects this to be added before any command that is sent, indicates payload size
        message_header = message_length + b"\x00\x00\x00\x03\x00\x00\x00"
        data = message_header + command_prefix + full_command + delimiter

        server_address = (ADDRESS, PORT)
        loop = asyncio.get_event_loop()
        try:
            await loop.sock_connect(sock, server_address)
            await loop.sock_sendall(sock, data)

            # Add a delay before receiving data
            await asyncio.sleep(.02)

            received_data = await self.async_recv(sock)
            response = decode_mixed_string(received_data)
            return self.__parse_response(response)

        except socket.timeout:
            self.logger.debug("Timeout occurred while receiving data")
            raise TunerTimeoutException()
        except Exception as e:
            self.logger.debug(f"Error occurred while receiving data: {str(e)}")
            # check if No connection could be made is present in the error message
            connection_errors = [
                "The remote computer refused the network connection",
            ]
            if any(error in str(e) for error in connection_errors):
                raise TunerConnectionException(e)
            else:
                raise TunerErrorException(e)
        finally:
            sock.close()

    async def async_recv(self, sock: Any, timeout: float = 2.0, size: int = 4096):
        response = await asyncio.wait_for(asyncio.get_event_loop().sock_recv(sock, size), timeout)
        return response
