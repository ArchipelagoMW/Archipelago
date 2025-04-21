from urllib.error import HTTPError

from flask import redirect, Response
from pony.orm import commit, db_session, select

from Utils import __version__, tuplize_version
from WebHostLib import cache
from WebHostLib.models import ArchipelagoDownload
from . import api_endpoints


@api_endpoints.route("/downloads/<string:build>")
def get_download(build: str) -> Response:
    # download_data = ArchipelagoDownload.select(platform=build).sort_by(A)
    download_data = select(download for download in ArchipelagoDownload
                           if download.platform == build).sort_by(ArchipelagoDownload.version).first()
    try:
        # ping GitHub API to make sure it's alive and cache the latest data
        if get_latest_release():
            download_data = select(download for download in ArchipelagoDownload
                                   if download.platform == build).sort_by(ArchipelagoDownload.version).first()
    except HTTPError:
        # failed to hit the api endpoint, just send the latest known link anyway
        pass
    download_data.downloads += 1
    return redirect(download_data.url)


@cache.cached(timeout=300)
def get_latest_release() -> bool:
    """
    Pulls the latest release from the Archipelago GitHub and saves new releases to the db.

    :return: Whether a new version was found.
    """
    import requests

    response = requests.get("https://api.github.com/repos/ArchipelagoMW/Archipelago/releases/latest", timeout=1)
    response.raise_for_status()
    data = response.json()

    entry_to_send: ArchipelagoDownload

    latest_downloads = select(download for download in ArchipelagoDownload if download.version == data["tag_name"])

    new_download = False
    with db_session:
        for asset in data["assets"]:
            filename = name = asset["name"]
            if "AppImage" in filename:
                name = "appimage"
            elif "tar" in filename:
                name = "tar"
            elif "exe" in filename:
                name = "windows"
            # not currently supported but maybe one day
            elif "arm64" in filename:
                name = "arm64"
            elif "amd64" in filename or "x86_64" in filename:
                name = "x86_64"
            download_url = asset["browser_download_url"]
            ArchipelagoDownload(platform=name, version=data["tag_name"], url=download_url, downloads=0)
        commit()
    return True