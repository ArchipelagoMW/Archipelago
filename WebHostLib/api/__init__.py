"""API endpoints package."""
from uuid import UUID
from typing import List, Tuple

from flask import Blueprint, abort

from ..models import Room, Seed
from .. import cache

api_endpoints = Blueprint('api', __name__, url_prefix="/api")

# unsorted/misc endpoints


def get_players(seed: Seed) -> List[Tuple[str, str]]:
    return [(slot.player_name, slot.game) for slot in seed.slots]


@api_endpoints.route('/room_status/<suuid:room>')
def room_info(room: UUID):
    room = Room.get(id=room)
    if room is None:
        return abort(404)
    return {
        "tracker": room.tracker,
        "players": get_players(room.seed),
        "last_port": room.last_port,
        "last_activity": room.last_activity,
        "timeout": room.timeout
    }


@api_endpoints.route('/datapackage')
@cache.cached()
def get_datapackage():
    from worlds import network_data_package
    return network_data_package


@api_endpoints.route('/datapackage_version')
@cache.cached()
def get_datapackage_versions():
    from worlds import network_data_package, AutoWorldRegister
    version_package = {game: world.data_version for game, world in AutoWorldRegister.world_types.items()}
    version_package["version"] = network_data_package["version"]
    return version_package


from . import generate, user  # trigger registration
