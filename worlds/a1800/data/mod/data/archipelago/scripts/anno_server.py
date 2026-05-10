from contextlib import contextmanager
import json
from pathlib import Path
from typing import Any, Dict, Generator

from rcon.rcon_mmap_server import RCONMMapServer
from rcon.rcon_packet import RCONPacket


class AnnoServer(RCONMMapServer):
    def __init__(self, env: Dict[str, Any], file_path: Path, script_path: Path, slot_name: str, seed_name: str) -> None:
        super().__init__(file_path)
        self.env = env
        self.script_path = script_path
        self.slot_name = slot_name
        self.seed_name = seed_name

        self.register_handler("/ap-rcon-info", _handle_ap_rcon_info)
        self.register_handler("/ap-sync", _handle_ap_sync)
        self.register_handler("/ap-receive-item", _handle_ap_receive_item)


def _handle_ap_rcon_info(server: RCONMMapServer, packet: RCONPacket, _body: str) -> None:
    assert isinstance(server, AnnoServer)

    info = {
        "slot_name": server.slot_name,
        "seed_name": server.seed_name,
    }

    server.send_message(packet.id, RCONPacket.SERVERDATA_RESPONSE_VALUE, json.dumps(info))


def _handle_ap_sync(server: RCONMMapServer, packet: RCONPacket, _body: str) -> None:
    assert isinstance(server, AnnoServer)

    locations_checked = set()  # type: set[int] # pyright: ignore[reportTypeCommentUsage]

    server.env["console"].startScript(str(server.script_path / "ap_sync.lua"))

    for _, (location_id, is_unlocked) in server.env["g_location_guid_data"].items():
        if is_unlocked:
            locations_checked.add(location_id)

    data = {
        "slot_name": server.slot_name,
        "seed_name": server.seed_name,
        "locations_checked": list(locations_checked),
        "victory": server.env["g_victory"],
    }  # type: dict[str, Any] # pyright: ignore[reportTypeCommentUsage]

    server.send_message(packet.id, RCONPacket.SERVERDATA_RESPONSE_VALUE, json.dumps(data))


def _handle_ap_receive_item(server: RCONMMapServer, _packet: RCONPacket, body: str) -> None:
    assert isinstance(server, AnnoServer)

    item_id = int(body)
    if item_id in server.env["ITEM_ID_TO_GUIDS"]:
        server.env["console"].startScript(
            str(server.script_path / "ap_receive_item" / "ap_receive_item_{}.lua".format(item_id)))


@contextmanager
def open_anno_server(env: Dict[str, Any], file_path: Path, script_path: Path, slot_name: str, seed_name: str) -> Generator[AnnoServer, Any, None]:
    anno_server = AnnoServer(env, file_path, script_path, slot_name, seed_name)
    try:
        yield anno_server
    finally:
        anno_server.close()
