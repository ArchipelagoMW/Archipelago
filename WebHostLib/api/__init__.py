"""API endpoints package."""
import urllib.request
from io import BytesIO
from typing import List, Tuple
from uuid import UUID

from flask import Blueprint, abort, send_file, url_for
from pony.orm import flush

import worlds.Files
from .. import cache
from ..models import ArchipelagoInstaller, Room, Seed

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


@api_endpoints.route("/downloads/<string:build>")
def get_download(build: str):
    download_data = ArchipelagoInstaller.get(id=build)
    if download_data is None:
        get_latest_release()
        download_data = ArchipelagoInstaller.get(id=build)
    return send_file(BytesIO(download_data.data), as_attachment=True, download_name=download_data.name)


def get_latest_release() -> None:
    """Pulls the latest release from the Archipelago GitHub and saves them to the db."""
    import requests
    response = requests.get("https://api.github.com/repos/ArchipelagoMW/Archipelago/releases/latest")
    response.raise_for_status()
    data = response.json()
    for asset in data["assets"]:
        filename = asset["name"]
        if "AppImage" in filename:
            name = "appimage"
        elif "tar" in filename:
            name = "tar"
        elif "Win7" in filename:
            name = "windows7"
        elif "exe" in filename:
            name = "windows"
        else:
            break
        ArchipelagoInstaller(id=name, name=filename, data=urllib.request.urlopen(asset["browser_download_url"]).read())
        flush()


from . import generate, user  # trigger registration
