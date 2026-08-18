from typing import Any, Dict
from uuid import UUID

from flask import abort, url_for

from WebHostLib import to_url
import worlds.Files
from . import api_endpoints, get_players
from ..models import Room
from ..misc import get_slot_download


@api_endpoints.route('/room_status/<suuid:room_id>')
def room_info(room_id: UUID) -> Dict[str, Any]:
    room = Room.get(id=room_id)
    if room is None:
        return abort(404)

    def supports_apdeltapatch(game: str) -> bool:
        return game in worlds.Files.AutoPatchRegister.patch_types

    downloads = []
    for slot in sorted(room.seed.slots):
        slot_download = get_slot_download(room, slot)
        if slot_download:
            downloads.append(slot_download)

    return {
        "tracker": to_url(room.tracker),
        "players": get_players(room.seed),
        "last_port": room.last_port,
        "last_activity": room.last_activity,
        "timeout": room.timeout,
        "downloads": downloads,
    }
