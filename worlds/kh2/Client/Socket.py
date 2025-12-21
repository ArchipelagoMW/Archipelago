from enum import IntEnum
import asyncio
import socket
from CommonClient import logger
from typing import TYPE_CHECKING

# I don't know what is going on here, but it works.
if TYPE_CHECKING:
    from . import KH2Context
else:
    KH2Context = object

class MessageType(IntEnum):
    Invalid = -1
    Test = 0
    WorldLocationChecked = 1
    LevelChecked = 2
    KeybladeChecked = 3
    BountyList = 4
    SlotData = 5
    Deathlink = 6
    SoldItems = 7
    NotificationType = 8
    NotificationMessage = 9
    ChestsOpened = 10
    ReceiveItem = 11
    RequestAllItems = 12
    Handshake = 13
    Victory = 19
    Closed = 20

class KH2Socket:
    def __init__(self, client: KH2Context, host: str = "127.0.0.1", port:int = 13137):
        self.client: KH2Context = client
        self.host: str = host
        self.port: int = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = None
        self.accept_task = None
        self.listen_task = None
        self.is_connected = False
        self.closing = False

    async def start_server(self) -> None:
        self.loop = asyncio.get_running_loop()
        self.server_socket.setblocking(False)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        self.accept_task = self.loop.create_task(self._accept_client())

    async def _accept_client(self) -> None:
        """Wait for a client to connect and start a listener task."""
        logger.info("Waiting for KH2 game connection...")
        while not self.closing:
            try:
                self.client_socket, addr = await asyncio.wait_for(self.loop.sock_accept(self.server_socket), timeout=1.0)
                self.is_connected = True
                self.client_socket.setblocking(False)
                self.listen_task = self.loop.create_task(self.listen())
                return
            except asyncio.TimeoutError:
                continue
            except asyncio.CancelledError:
                raise
            except Exception as e:
                if self.closing:
                    return
                logger.info(f"Socket accept failed ({e}); retrying in 5s")
                self.is_connected = False
                await asyncio.sleep(5)

    def _safe_close_client(self) -> None:
        """Close the current client socket without killing the server socket."""
        try:
            if self.client_socket:
                self.client_socket.close()
        finally:
            self.client_socket = None
            self.is_connected = False

    async def listen(self) -> None:
        buffer = b""
        while not self.closing and self.client_socket:
            try:
                message = await asyncio.wait_for(self.loop.sock_recv(self.client_socket, 1024), timeout=1.0)
                if not message:
                    raise ConnectionResetError("Client disconnected")

                buffer += message

                while b"\n" in buffer:
                    raw_msg, buffer = buffer.split(b"\n", 1)
                    msgStr = raw_msg.decode("utf-8")

                    values = msgStr.split(";")
                    print("Received message: "+msgStr)
                    self.handle_message(values)
            except asyncio.TimeoutError:
                continue
            except asyncio.CancelledError:
                return
            except (ConnectionResetError, OSError) as e:
                if not self.closing:
                    logger.info("Connection to game lost, reconnecting...")
                    self._safe_close_client()
                    self.loop.create_task(self._accept_client())
                    return

    def send(self, msg_id: int, values: list[str]) -> None:
        if not self.is_connected or self.client_socket is None:
            return
        try:
            msg = str(msg_id)
            for val in values:
                msg += ";" + str(val)
            CHUNK_SIZE = 30
            i = 0
            if len(msg) >= 30:
                while i < len(msg):
                    part = msg[i: i + CHUNK_SIZE]
                    if i + CHUNK_SIZE < len(msg):
                        part += ";MOR\n"
                        print("Sending message in parts due to length: " + part)
                    else:
                        part += ";FIN\n"
                        print("Finished sending message in parts due to length: " + part)

                    self.client_socket.sendall(part.encode("utf-8"))
                    i += CHUNK_SIZE
            else:
                msg += "\n"
                self.client_socket.sendall(msg.encode("utf-8"))
                print("Sent message: "+msg)
        except (OSError, ConnectionResetError, BrokenPipeError) as e:
            print(f"Error sending message {msg_id}: {e}; connection may be lost")
            self.is_connected = False
        except Exception as e:
            print(f"Error sending message {msg_id}: {e}")

    def handle_message(self, message: list[str]) -> None:
        if message[0] == '':
            return

        print("Handling message: "+str(message))
        msg_type = MessageType(int(message[0]))

        if msg_type == MessageType.WorldLocationChecked:
            self.client.world_locations_checked.append(message[1])

        elif msg_type == MessageType.LevelChecked:
            self.client.sora_form_levels[message[2]] = int(message[1])

        elif msg_type == MessageType.KeybladeChecked:
            self.client.keyblade_ability_checked.append(message[1])

        elif msg_type == MessageType.SlotData:
            self.client.current_world_int = int(message[1])

        elif msg_type == MessageType.Deathlink:
            self.client.Room = int(message[1])
            self.client.Event = int(message[2])
            self.client.World = int(message[3])
            self.client.SoraDied = True

        elif msg_type == MessageType.SoldItems:
            self.client.kh2_seed_save["SoldEquipment"][message[1]] = message[2]

        elif msg_type == MessageType.Victory:
            self.client.kh2_finished_game = True
            self.send(MessageType.Victory, ["Victory Received"])

        elif msg_type == MessageType.RequestAllItems:
            self.client.get_items()

        elif msg_type == MessageType.Handshake:
            self.client.kh2connectionconfirmed = True
            self.send(MessageType.Handshake, [str(self.client.serverconnected)])
            print("Responded to Handshake")


    def send_item(self, msg: list) -> None:
        self.send(MessageType.ReceiveItem, msg)

    def send_slot_data(self, data: str) -> None:
        self.send(MessageType.SlotData, [data])

    def shutdown_server(self) -> None:
        self.closing = True
        if self.accept_task:
            try:
                self.accept_task.cancel()
            except Exception:
                pass
        if self.listen_task:
            try:
                self.listen_task.cancel()
            except Exception:
                pass
        self._safe_close_client()
        try:
            if self.server_socket:
                self.server_socket.close()
        except Exception:
            pass