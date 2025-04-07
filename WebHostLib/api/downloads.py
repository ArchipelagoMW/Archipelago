from flask import redirect, Response, send_from_directory
from pony.orm import flush

from Utils import download_file, local_path
from WebHostLib import cache
from WebHostLib.models import ArchipelagoInstaller
from . import api_endpoints


@api_endpoints.route("/downloads/<string:build>")
def get_download(build: str) -> Response:
    from requests import HTTPError
    download_data = ArchipelagoInstaller.get(id=build)
    try:
        # ping GitHub API to make sure it's alive and cache the latest data
        get_latest_release()
        return redirect(download_data.url)
    except HTTPError:
        # GitHub request failed so return the last cached mirror
        download_data.downloads += 1
        return send_from_static(build)


@cache.cached(timeout=300)
def get_latest_release() -> None:
    """Pulls the latest release from the Archipelago GitHub and saves them to the db."""
    import requests
    import tempfile

    response = requests.get("https://api.github.com/repos/ArchipelagoMW/Archipelago/releases/latest", timeout=5)
    response.raise_for_status()
    data = response.json()
    from pony.orm import db_session
    build_path = local_path("WebHostLib", "static", "builds")
    with db_session:
        for asset in data["assets"]:
            filename = asset["name"]
            if "AppImage" in filename:
                name = "appimage"
            elif "tar" in filename:
                name = "tar"
            elif "exe" in filename:
                name = "windows"
            else:
                break
            download_url = asset["browser_download_url"]
            db_entry = ArchipelagoInstaller.get(id=name)
            if db_entry is None:
                ArchipelagoInstaller(id=name, name=filename, url=download_url, downloads=0)
            else:
                # we have the latest file so no need to download it again
                if filename == db_entry.name:
                    continue
                # TODO write current downloads number somewhere?
                db_entry.set(name=filename, url=download_url, downloads=0)
                download_file(download_url, build_path, filename)

    flush()

def send_from_static(build: str) -> Response:
    return send_from_directory("static/builds", build)
