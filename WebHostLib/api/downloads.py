from flask import redirect, Response
from pony.orm import commit, db_session, select

from Utils import __version__
from WebHostLib import cache
from WebHostLib.models import ArchipelagoDownload
from . import api_endpoints


@cache.cached
@api_endpoints.route("/downloads/<string:build>")
def get_download(build: str) -> Response:
    download_data = select(download for download in ArchipelagoDownload
                           if download.platform == build).first()
    if download_data and download_data.version >= __version__:
        with db_session:
            download_data.downloads += 1
            commit()
        return redirect(download_data.url)
    return get_latest_release(build)


def get_latest_release(build: str) -> Response:
    """Pulls the latest release from the Archipelago GitHub and saves them to the db."""
    import requests

    response = requests.get("https://api.github.com/repos/ArchipelagoMW/Archipelago/releases/latest", timeout=5)
    response.raise_for_status()
    data = response.json()

    entry_to_send: ArchipelagoDownload
    with db_session:
        for asset in data["assets"]:
            filename = name = asset["name"]
            if "AppImage" in filename:
                name = "appimage"
            elif "tar" in filename:
                name = "tar"
            elif "exe" in filename:
                name = "windows"
            download_url = asset["browser_download_url"]
            db_entry = ArchipelagoDownload(platform=name, version=data["tag_name"],
                                           url=download_url, downloads=0)
            if name == build:
                db_entry.downloads += 1
                entry_to_send = db_entry
        commit()
    return redirect(entry_to_send.url)
