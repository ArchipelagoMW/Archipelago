import argparse
import zipfile
from io import BytesIO

import bsdiff4
from datetime import datetime
import hashlib
import json
import logging
import os
import requests
import secrets
import shutil
import subprocess
from tkinter import messagebox
from typing import Any, Dict, Set
import urllib
import urllib.parse

import Utils
from .Constants import *
from . import SavingPrincessWorld

files_to_clean: Set[str] = {
    "D3DX9_43.dll",
    "data.win",
    "m_boss.ogg",
    "m_brainos.ogg",
    "m_coldarea.ogg",
    "m_escape.ogg",
    "m_hotarea.ogg",
    "m_hsis_dark.ogg",
    "m_hsis_power.ogg",
    "m_introarea.ogg",
    "m_malakhov.ogg",
    "m_miniboss.ogg",
    "m_ninja.ogg",
    "m_purple.ogg",
    "m_space_idle.ogg",
    "m_stonearea.ogg",
    "m_swamp.ogg",
    "m_zzz.ogg",
    "options.ini",
    "Saving Princess v0_8.exe",
    "splash.png",
    "gm-apclientpp.dll",
    "LICENSE",
    "original_data.win",
    "versions.json",
}

file_hashes: Dict[str, str] = {
    "D3DX9_43.dll": "86e39e9161c3d930d93822f1563c280d",
    "Saving Princess v0_8.exe": "cc3ad10c782e115d93c5b9fbc5675eaf",
    "original_data.win": "f97b80204bd9ae535faa5a8d1e5eb6ca",
}


class UrlResponse:
    def __init__(self, response_code: int, data: Any):
        self.response_code = response_code
        self.data = data


def get_date(target_asset: str) -> str:
    """Provided the name of an asset, fetches its update date"""
    try:
        with open("versions.json", "r") as versions_json:
            return json.load(versions_json)[target_asset]
    except (FileNotFoundError, KeyError, json.decoder.JSONDecodeError):
        return "2000-01-01T00:00:00Z"  # arbitrary old date


def set_date(target_asset: str, date: str) -> None:
    """Provided the name of an asset and a date, sets it update date"""
    try:
        with open("versions.json", "r") as versions_json:
            versions = json.load(versions_json)
            versions[target_asset] = date
    except (FileNotFoundError, KeyError, json.decoder.JSONDecodeError):
        versions = {target_asset: date}
    with open("versions.json", "w") as versions_json:
        json.dump(versions, versions_json)


def get_timestamp(date: str) -> float:
    """Parses a GitHub REST API date into a timestamp"""
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").timestamp()


def send_request(request_url: str) -> UrlResponse:
    """Fetches status code and json response from given url"""
    response = requests.get(request_url)
    if response.status_code == 200:  # success
        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            raise RuntimeError(f"Unable to fetch data. (status code {response.status_code}).")
    else:
        data = {}
    return UrlResponse(response.status_code, data)


def update(target_asset: str, url: str) -> bool:
    """
    Returns True if the data was fetched and installed
        (or it was already on the latest version, or the user refused the update)
    Returns False if rate limit was exceeded
    """
    try:
        logging.info(f"Checking for {target_asset} updates.")
        response = send_request(url)
        if response.response_code == 403:  # rate limit exceeded
            return False
        assets = response.data[0]["assets"]
        for asset in assets:
            if target_asset in asset["name"]:
                newest_date: str = asset["updated_at"]
                release_url: str = asset["browser_download_url"]
                break
        else:
            raise RuntimeError(f"Failed to locate {target_asset} amongst the assets.")
    except (KeyError, IndexError, TypeError, RuntimeError):
        update_error = f"Failed to fetch latest {target_asset}."
        messagebox.showerror("Failure", update_error)
        raise RuntimeError(update_error)
    try:
        update_available = get_timestamp(newest_date) > get_timestamp(get_date(target_asset))
        if update_available and messagebox.askyesnocancel(f"New {target_asset}",
                                                          "Would you like to install the new version now?"):
            # unzip and patch
            with urllib.request.urlopen(release_url) as download:
                with zipfile.ZipFile(BytesIO(download.read())) as zf:
                    zf.extractall()
            patch_game()
            set_date(target_asset, newest_date)
    except (ValueError, RuntimeError, urllib.error.HTTPError):
        update_error = f"Failed to apply update."
        messagebox.showerror("Failure", update_error)
        raise RuntimeError(update_error)
    return True


def patch_game() -> None:
    """Applies the patch to data.win"""
    logging.info("Proceeding to patch.")
    with open(PATCH_NAME, "rb") as patch:
        with open("original_data.win", "rb") as data:
            patched_data = bsdiff4.patch(data.read(), patch.read())
        with open("data.win", "wb") as data:
            data.write(patched_data)
        logging.info("Done!")


def is_install_valid() -> bool:
    """Checks that the mandatory files that we cannot replace do exist in the current folder"""
    for file_name, expected_hash in file_hashes.items():
        if not os.path.exists(file_name):
            return False
        with open(file_name, "rb") as clean:
            current_hash = hashlib.md5(clean.read()).hexdigest()
        if not secrets.compare_digest(current_hash, expected_hash):
            return False
    return True


def install() -> None:
    """Extracts all the game files into the mod installation folder"""
    logging.info("Mod installation missing or corrupted, proceeding to reinstall.")
    # get the cab file and extract it into the installation folder
    with open(SavingPrincessWorld.settings.exe_path, "rb") as exe:
        # find the cab header
        logging.info("Looking for cab archive inside exe.")
        cab_found: bool = False
        while not cab_found:
            cab_found = exe.read(1) == b'M' and exe.read(1) == b'S' and exe.read(1) == b'C' and exe.read(1) == b'F'
        exe.read(4)  # skip reserved1, always 0
        cab_size: int = int.from_bytes(exe.read(4), "little")  # read size in bytes
        exe.seek(-12, 1)  # move the cursor back to the start of the cab file
        logging.info(f"Archive found at offset {hex(exe.seek(0, 1))}, size: {hex(cab_size)}.")
        logging.info("Extracting cab archive from exe.")
        with open("saving_princess.cab", "wb") as cab:
            cab.write(exe.read(cab_size))

    # clean up files from previous installations
    for file_name in files_to_clean:
        if os.path.exists(file_name):
            os.remove(file_name)

    logging.info("Extracting files from cab archive.")
    if Utils.is_windows:
        subprocess.run(["Extrac32", "/Y", "/E", "saving_princess.cab"])
    else:
        if shutil.which("wine") is not None:
            subprocess.run(["wine", "Extrac32", "/Y", "/E", "saving_princess.cab"])
        elif shutil.which("7z") is not None:
            subprocess.run(["7z", "e", "saving_princess.cab"])
        else:
            error = "Could not find neither wine nor 7z.\n\nPlease install either the wine or the p7zip package."
            messagebox.showerror("Missing package!", f"Error: {error}")
            raise RuntimeError(error)
    os.remove("saving_princess.cab")  # delete the cab file

    shutil.copyfile("data.win", "original_data.win")  # and make a copy of data.win
    logging.info("Done!")


def launch(*args: str) -> Any:
    """Check args, then the mod installation, then launch the game"""
    name: str = ""
    password: str = ""
    server: str = ""
    if args:
        parser = argparse.ArgumentParser(description=f"{GAME_NAME} Client Launcher")
        parser.add_argument("url", type=str, nargs="?", help="Archipelago Webhost uri to auto connect to.")
        args = parser.parse_args(args)

        # handle if text client is launched using the "archipelago://name:pass@host:port" url from webhost
        if args.url:
            url = urllib.parse.urlparse(args.url)
            if url.scheme == "archipelago":
                server = f'--server="{url.hostname}:{url.port}"'
                if url.username:
                    name = f'--name="{urllib.parse.unquote(url.username)}"'
                if url.password:
                    password = f'--password="{urllib.parse.unquote(url.password)}"'
            else:
                parser.error(f"bad url, found {args.url}, expected url in form of archipelago://archipelago.gg:38281")

    Utils.init_logging(CLIENT_NAME, exception_logger="Client")

    os.chdir(SavingPrincessWorld.settings.install_folder)

    # check that the mod installation is valid
    if not is_install_valid():
        if messagebox.askyesnocancel(f"Mod installation missing or corrupted!",
                                     "Would you like to reinstall now?"):
            install()
        # if there is no mod installation, and we are not installing it, then there isn't much to do
        else:
            return

    # check for updates
    if not update(DOWNLOAD_NAME, DOWNLOAD_URL):
        messagebox.showinfo("Rate limit exceeded",
                            "GitHub REST API limit exceeded, could not check for updates.\n\n"
                            "This will not prevent the game from being played if it was already playable.")

    # and try to launch the game
    if SavingPrincessWorld.settings.launch_game:
        logging.info("Launching game.")
        try:
            subprocess.Popen(f"{SavingPrincessWorld.settings.launch_command} {name} {password} {server}")
        except FileNotFoundError:
            error = ("Could not run the game!\n\n"
                     "Please check that launch_command in options.yaml or host.yaml is set up correctly.")
            messagebox.showerror("Command error!", f"Error: {error}")
            raise RuntimeError(error)
