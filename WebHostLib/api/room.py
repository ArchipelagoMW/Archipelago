from typing import Any, Dict
from uuid import UUID

from flask import abort, url_for

from WebHostLib import to_url
from worlds.Files import is_ap_player_container
from . import api_endpoints, get_players
from ..models import Room


@api_endpoints.route('/room_status/<suuid:room_id>')
def room_info(room_id: UUID) -> Dict[str, Any]:
    room = Room.get(id=room_id)
    if room is None:
        return abort(404)

    def supports_patch_download(game: str, data: bytes, player_id: int) -> bool:
        if game == "Factorio":
            return False
        return is_ap_player_container(game, data, player_id)

    downloads = []
    for slot in sorted(room.seed.slots):
        if slot.data and not supports_patch_download(slot.game, slot.data, slot.player_id):
            slot_download = {
                "slot": slot.player_id,
                "download": url_for("download_slot_file", room_id=room.id, player_id=slot.player_id)
            }
            downloads.append(slot_download)
        elif slot.data:
            slot_download = {
                "slot": slot.player_id,
                "download": url_for("download_patch", patch_id=slot.id, room_id=room.id)
            }
            downloads.append(slot_download)

    return {
        "tracker": to_url(room.tracker),
        "players": get_players(room.seed),
        "last_port": room.last_port,
        "last_activity": room.last_activity,
        "timeout": room.timeout,
        "downloads": downloads,
    }
