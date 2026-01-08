import json
from typing import Any, Literal, Mapping, Sequence, TypedDict
from typing_extensions import NotRequired
import websockets

from subversion_rando.tracker_logic import TrackerLogic

from Utils import async_start


INFO_PACKET = info = {
    "cmd": "Info",
    "protocol": 0,
    "name": "SubversionLogic",
    "version": "0.1.0"
}


class ClientPacket(TypedDict):
    cmd: Literal["Sync"]
    slot: NotRequired[str]


class VarPacket(TypedDict):
    cmd: Literal["Var"]
    name: str
    value: Any
    slot: NotRequired[str]


class UATServer:
    """ https://github.com/black-sliver/UAT/blob/master/PROTOCOL.md """

    _clients: set[websockets.WebSocketCommonProtocol]
    _locations: list[str]
    _server: websockets.serve | None = None
    _tr_logic: TrackerLogic
    # TODO: be able to change logic mid game

    def __init__(self, logic_str: str) -> None:
        self._clients = set()
        self._locations = []
        self._tr_logic = TrackerLogic(logic_str)

    def get_variable_data(self) -> list[VarPacket]:
        return [{
            "cmd": "Var",
            "name": "locations",
            "value": self._locations
        }]

    async def send_data(self, client: websockets.WebSocketCommonProtocol) -> None:
        data = json.dumps(self.get_variable_data())
        print(f"sending {data=}")
        await client.send(data)

    async def server_loop(self, client: websockets.WebSocketCommonProtocol, path: str) -> None:
        async def error(cmd_name: str,
                        reason: Literal["unknown cmd", "missing argument", "bad value", "unknown"]) -> None:
            data = [{"cmd": "ErrorReply", "name": cmd_name, "reason": reason}]
            print(f"error {data=}")
            await client.send(json.dumps(data))

        self._clients.add(client)
        try:
            await client.send(json.dumps([info]))
            async for data in client:
                packet: Sequence[ClientPacket | Any] | Any = json.loads(data)
                print(f"received {json.dumps(packet, indent=4)}")
                if not isinstance(packet, Sequence):
                    await error("?", "unknown")
                    continue
                for command in packet:
                    if not isinstance(command, dict):
                        await error("?", "unknown")
                        continue
                    cmd_str = command.get("cmd")
                    if cmd_str != "Sync":
                        await error(cmd_str, "unknown cmd")
                        continue
                    await self.send_data(client)
        finally:
            self._clients.remove(client)

    def set_items(self, items: Mapping[str, int]) -> None:
        self._locations = self._tr_logic.item_names_to_location_names(items)
        # print(f"{self._locations=}")

        async def send() -> None:
            for client in self._clients:
                await self.send_data(client)

        async_start(send())

    def get_locations(self) -> list[str]:
        return self._locations.copy()

    async def start(self) -> None:
        async def handler(client: websockets.WebSocketCommonProtocol, path: str) -> None:
            await self.server_loop(client, path)

        assert self._server is None
        self._server = websockets.serve(handler, "localhost", 65399)
        await self._server

    async def close(self) -> None:
        for client in self._clients:
            await client.close()
        if self._server:
            self._server.ws_server.close()
        self._server = None
