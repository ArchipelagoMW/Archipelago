"""API endpoints package."""
from typing import List, Tuple
from uuid import UUID

from flask import Blueprint, abort, url_for

import worlds.Files
from .. import cache
from ..models import Room, Seed

api_endpoints = Blueprint('api', __name__, url_prefix="/api")

# unsorted/misc endpoints


def get_players(seed: Seed) -> List[Tuple[str, str]]:
    return [(slot.player_name, slot.game) for slot in seed.slots]


@api_endpoints.route('/room_status/<suuid:room>')
def room_info(room: UUID):
    room = Room.get(id=room)
    if room is None:
        return abort(404)
    
    def supports_apdeltapatch(game: str):
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


@api_endpoints.route('/datapackage')
@cache.cached()
def get_datapackage():
    from worlds import network_data_package
    return network_data_package


@api_endpoints.route('/datapackage_checksum')
@cache.cached()
def get_datapackage_checksums():
    from worlds import network_data_package
    version_package = {
        game: game_data["checksum"] for game, game_data in network_data_package["games"].items()
    }
    return version_package


from . import generate, user  # trigger registration
