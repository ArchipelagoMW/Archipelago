"""API endpoints package."""
from typing import List, Tuple
from uuid import UUID

from flask import Blueprint, abort

from MultiServer import Context
from Utils import restricted_loads
from .. import cache
from ..models import GameDataPackage, Room, Seed

api_endpoints = Blueprint('api', __name__, url_prefix="/api")

# unsorted/misc endpoints


def get_players(seed: Seed) -> List[Tuple[str, str]]:
    return [(slot.player_name, slot.game) for slot in seed.slots]


@api_endpoints.route("/room_status/<suuid:room>")
def room_info(room: UUID):
    room = Room.get(id=room)
    if room is None:
        return abort(404)
    from base64 import urlsafe_b64encode
    multidata = Context.decompress(room.seed.multidata)
    return {
        "tracker": urlsafe_b64encode(room.tracker.bytes).rstrip(b'=').decode('ascii'),
        "players": get_players(room.seed),
        "last_port": room.last_port,
        "last_activity": room.last_activity,
        "timeout": room.timeout,
        "datapackage": multidata["datapackage"],
    }


@api_endpoints.route('/datapackage')
@cache.cached()
def get_datapackage():
    from worlds import network_data_package
    return network_data_package


@api_endpoints.route('/datapackage_version')
@cache.cached()
def get_datapackage_versions():
    from worlds import AutoWorldRegister

    version_package = {game: world.data_version for game, world in AutoWorldRegister.world_types.items()}
    return version_package


@api_endpoints.route('/datapackage_checksum')
@cache.cached()
def get_datapackage_checksums():
    from worlds import network_data_package
    version_package = {
        game: game_data["checksum"] for game, game_data in network_data_package["games"].items()
    }
    return version_package


@api_endpoints.route("/datapackage/<suuid:room>/<string:game>")
@cache.cached()
def get_gamepackage(room: UUID, game: str):
    room = Room.get(id=room)
    if room is None:
        return abort(404)
    multidata = Context.decompress(room.seed.multidata)
    return restricted_loads(GameDataPackage.get(checksum=multidata["datapackage"][game]["checksum"]).data)


from . import generate, user, tracker  # trigger registration
