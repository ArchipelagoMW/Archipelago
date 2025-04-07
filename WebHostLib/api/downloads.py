import os
import urllib.request
from io import BytesIO

from flask import redirect, Response, send_file, send_from_directory
from pony.orm import flush

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
    response = requests.get("https://api.github.com/repos/ArchipelagoMW/Archipelago/releases/latest", timeout=5)
    response.raise_for_status()
    data = response.json()
    from pony.orm import db_session
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
                ArchipelagoInstaller(id=name, name=filename, data=urllib.request.urlopen(download_url).read(), url=download_url, downloads=0)
            else:
                # we have the latest file so no need to download it again
                if filename == db_entry.name:
                    continue
                # TODO write current downloads number somewhere?
                with urllib.request.urlopen(download_url) as response:
                    data = response.read()
                db_entry.set(name=filename, data=data, url=download_url, downloads=0)
                with open(os.path.join(os.getcwd(), "WebHostLib", "static", "builds", name), "wb") as file:
                    file.write(data)

    flush()

def send_from_static(build: str) -> Response:
    return send_from_directory("static", f"builds/{build}")
