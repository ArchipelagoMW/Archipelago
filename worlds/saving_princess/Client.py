import hashlib
import json
import logging
import os
import secrets
import shutil
import subprocess
from datetime import datetime
from tkinter import messagebox
from typing import Any, Dict
import urllib

import bsdiff4
import requests

import Utils
from .Constants import *
from . import SavingPrincessWorld

file_hashes: Dict[str, str] = {
    "D3DX9_43.dll": "86e39e9161c3d930d93822f1563c280d",
    "Saving Princess v0_8.exe": "cc3ad10c782e115d93c5b9fbc5675eaf",
    "original_data.win": "f97b80204bd9ae535faa5a8d1e5eb6ca",
}

download_urls: Dict[str, str] = {
    DLL_NAME: DLL_URL,
    PATCH_NAME: PATCH_URL,
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
        versions: json = {target_asset: date}
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
        if update_available and messagebox.askyesnocancel(f"New version of {target_asset} found",
                                                          "Would you like to install the new version now?"):
            if target_asset == DLL_NAME:
                download_dll(release_url)
            else:
                patch_game(release_url)
            set_date(target_asset, newest_date)
    except (ValueError, RuntimeError, urllib.error.HTTPError):
        update_error = f"Failed to apply update to {target_asset}."
        messagebox.showerror("Failure", update_error)
        raise RuntimeError(update_error)
    return True


def download_dll(url: str) -> None:
    """Downloads the dll from the provided url and saves it to the installation folder"""
    logging.info("Downloading dll.")
    with urllib.request.urlopen(url) as download:
        with open(DLL_NAME, "wb") as dll:
            dll.write(download.read())
        logging.info("Done!")


def patch_game(url: str) -> None:
    """Downloads the patch from the provided url and applies it to data.win"""
    logging.info("Proceeding to patch.")
    with urllib.request.urlopen(url) as download:
        with open("original_data.win", "rb") as data:
            patched_data = bsdiff4.patch(data.read(), download.read())
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
    if os.path.exists("versions.json"):
        os.remove("versions.json")  # to force reinstall of the assets
    logging.info("Done!")


def launch() -> None:
    """Check the mod installation, then launch it"""
    os.chdir(SavingPrincessWorld.settings.install_folder)

    # check that the mod installation is valid
    valid_install = is_install_valid()
    if not valid_install:
        if messagebox.askyesnocancel(f"Mod installation missing or corrupted!",
                                     "Would you like to reinstall now?"):
            install()
        # if there is no mod installation, and we are not installing it, then there's not much to do
        else:
            return

    # check for updates
    for asset_name, download_url in download_urls.items():
        if not update(asset_name, download_url):
            messagebox.showinfo("Rate limit exceeded",
                                "GitHub REST API limit exceeded, could not check for updates.\n\n"
                                "This will not prevent the game from being played if it was already playable.")
            break

    # and try to launch the game
    if SavingPrincessWorld.settings.launch_game:
        logging.info("Launching game.")
        if Utils.is_windows:
            subprocess.run([os.path.join(os.path.curdir, "Saving Princess v0_8.exe")])
        else:
            if shutil.which("wine") is not None:
                subprocess.run(["wine", os.path.join(os.path.curdir, "Saving Princess v0_8.exe")])
            else:
                messagebox.showerror("Missing package!",
                                     "Could not find wine.\n\nPlease install wine or run the game manually.")
