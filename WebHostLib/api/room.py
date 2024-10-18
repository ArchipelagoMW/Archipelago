from typing import Any, Dict
from uuid import UUID

from flask import abort, url_for

import worlds.Files
from . import api_endpoints, get_players
from ..models import Room


@api_endpoints.route('/room_status/<suuid:room_id>')
def room_info(room_id: UUID) -> Dict[str, Any]:
    room = Room.get(id=room_id)
    if room is None:
        return abort(404)

    def supports_apdeltapatch(game: str) -> bool:
        return game in worlds.Files.AutoPatchRegister.patch_types

    downloads = []
    for slot in sorted(room.seed.slots):
        if slot.data and not supports_apdeltapatch(slot.game):
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
        "tracker": room.tracker,
        "players": get_players(room.seed),
        "last_port": room.last_port,
        "last_activity": room.last_activity,
        "timeout": room.timeout,
        "downloads": downloads,
    }
