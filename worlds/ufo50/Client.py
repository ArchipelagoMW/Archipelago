import argparse
import hashlib
import json
import logging
import os
import secrets
import shlex
import shutil
import subprocess
import urllib
import urllib.parse
import zipfile
from datetime import datetime
from enum import Enum
from io import BytesIO
from tkinter import messagebox
from typing import Any

import bsdiff4
import requests

import Utils
from Utils import open_filename
from . import UFO50World


class UpdateResult(Enum):
    SUCCESS = 1
    API_LIMIT = 2
    VERSION_MISMATCH = 3
    ERROR = 4


class UrlResponse:
    def __init__(self, response_code: int, data: Any):
        self.response_code = response_code
        self.data = data


def find_steam_app_path(app_id: str, app_title: str) -> str:
    """
    Attempts to find a Steam game's install folder given its app id.
    If not found, an empty string is returned.
    """
    try:
        import vdf
        # fetch the vdf file path
        if Utils.is_windows:
            vdf_path = find_windows_vdf()
        else:
            vdf_path = "~/.steam/root/steamapps/libraryfolders.vdf"
        if not vdf_path:
            return ""
        # check each library folder (these can be in different drives)
        with open(vdf_path, "r") as lib:
            steam_dict = vdf.parse(lib)
            for index in (steam_dict["libraryfolders"].keys()):
                # to see if it contains the target app
                if app_id in steam_dict["libraryfolders"][index]["apps"].keys():
                    return fr"{steam_dict['libraryfolders'][index]['path']}\steamapps\common\{app_title}"
    except Exception as ex:
        logging.info(f"Error finding game's Steam installation: {ex}")
    return ""


def find_windows_vdf() -> str:
    """
    Attempts to find Steam's libraryfolders.vdf on Windows.
    If not found, an empty string is returned.
    """
    try:
        # fetch the steam registry key
        import winreg
        reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        steam_key = winreg.OpenKey(reg, r"SOFTWARE\Wow6432Node\Valve\Steam")
        # and comb it for the steam installation path
        for i in range(winreg.QueryInfoKey(steam_key)[1]):
            value = winreg.EnumValue(steam_key, i)
            if value[0] == "InstallPath":
                return fr"{value[1]}\steamapps\libraryfolders.vdf"
    except Exception as ex:
        logging.info(f"Error finding Steam installation through Windows registry: {ex}")
    return ""


def get_version() -> str:
    """Returns the game version that the patch targets"""
    try:
        with open("verify.json", "r") as verify:
            return json.load(verify)["version"]
    except (FileNotFoundError, KeyError, json.decoder.JSONDecodeError):
        return ""


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


def download_patch() -> UpdateResult:
    """
    Returns UpdateResult.UP_TO_DATE if the newest patch is the same as the one that is applied
    Returns UpdateResult.VERSION_MISMATCH if the downloaded patch is for a different version of the game
    Returns UpdateResult.API_LIMIT if rate limit was exceeded
    Returns UpdateResult.ERROR if downloading otherwise failed
    """
    target_asset = "ufo_50_archipelago.zip"
    try:
        logging.info(f"Checking for {target_asset} updates.")
        response = send_request("https://api.github.com/repos/UFO-50-Archipelago/Patch/releases")
        if response.response_code == 403:  # rate limit exceeded
            return UpdateResult.API_LIMIT
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
        return UpdateResult.ERROR
    try:
        # unzip
        with urllib.request.urlopen(release_url) as download:
            with zipfile.ZipFile(BytesIO(download.read())) as zf:
                zf.extractall()
        if not verify_game_version():
            return UpdateResult.VERSION_MISMATCH
        set_date(target_asset, newest_date)
    except (ValueError, RuntimeError, urllib.error.HTTPError):
        update_error = f"Failed to download update."
        messagebox.showerror("Failure", update_error)
        return UpdateResult.ERROR
    return UpdateResult.SUCCESS


def verify_game_version() -> bool:
    """Checks that the current version of the game matches that in the verify file"""
    try:
        with open("verify.json", "r") as verify:
            targets = json.load(verify)["files"]
        for target_name in ["original_data.win", "ufo50.exe"]:
            with open(target_name, "rb") as target:
                current_hash = hashlib.md5(target.read()).hexdigest()
                if not secrets.compare_digest(current_hash, targets[target_name]):
                    return False
    except (FileNotFoundError, KeyError, json.decoder.JSONDecodeError):
        return False
    return True


def patch_game() -> None:
    """Applies the patch to data.win"""
    logging.info("Proceeding to patch.")
    with open("ufo_50_basepatch.bsdiff4", "rb") as patch:
        with open("original_data.win", "rb") as data:
            patched_data = bsdiff4.patch(data.read(), patch.read())
        with open("data.win", "wb") as data:
            data.write(patched_data)
        logging.info("Done!")
    set_date("ufo50.exe", get_date("ufo_50_archipelago.zip"))


def is_install_valid() -> bool:
    """
    Checks the hash of files listed in the verify file, if it exists
    Returns true if it can fetch and verify the targets
    """
    try:
        with open("verify.json", "r") as verify:
            targets = json.load(verify)["files"]
        for file_name, expected_hash in targets.items():
            with open(file_name, "rb") as target:
                current_hash = hashlib.md5(target.read()).hexdigest()
            if not secrets.compare_digest(current_hash, expected_hash):
                return False
    except (FileNotFoundError, KeyError, json.decoder.JSONDecodeError):
        return False
    return True


def install() -> bool:
    """Copies all game files into the mod installation folder"""
    logging.info("Mod installation missing or corrupted, proceeding to reinstall.")
    # find the source folder
    source_path = find_steam_app_path("1147860", "UFO 50")
    source_file = open_filename(
        f"Locate UFO 50 executable {get_version()}",
        (("ufo50.exe", (".exe",)),),
        os.path.join(source_path, "ufo50.exe") if source_path else "")
    source_path = os.path.dirname(source_file)
    if not source_path:
        return False

    # check that the provided file is what we needed, if we have verify available
    if not os.path.exists(os.path.join(source_path, "data.win")):
        return False
    if not os.path.exists(os.path.join(source_path, "ufo50.exe")):
        return False
    if os.path.isfile("verify.json"):
        try:
            with open("verify.json", "r") as verify:
                targets = json.load(verify)["files"]
            with open(os.path.join(source_path, "data.win"), "rb") as target:
                current_hash = hashlib.md5(target.read()).hexdigest()
                if not secrets.compare_digest(current_hash, targets["original_data.win"]):
                    return False
            with open(os.path.join(source_path, "ufo50.exe"), "rb") as target:
                current_hash = hashlib.md5(target.read()).hexdigest()
                if not secrets.compare_digest(current_hash, targets["ufo50.exe"]):
                    return False
        except (FileNotFoundError, KeyError, json.decoder.JSONDecodeError):
            return False

    # copy all files over
    logging.info("Copying game files to installation folder.")
    shutil.copytree(source_path, os.curdir, dirs_exist_ok=True)

    shutil.copyfile("data.win", "original_data.win")  # and make a copy of data.win
    for file_name in ["steam_api64.dll", "Steamworks_x64.dll"]:
        if os.path.isfile(file_name):
            os.remove(file_name)
    logging.info("Done!")
    return True


def launch(*args: str) -> Any:
    """Check args, then the mod installation, then launch the game"""
    Utils.init_logging("UFO 50", exception_logger="Client")

    name: str = ""
    password: str = ""
    server: str = ""
    if args:
        parser = argparse.ArgumentParser(description=f"UFO 50 Launcher")
        parser.add_argument("url", type=str, nargs="?", help="Archipelago Webhost uri to auto connect to.")
        args = parser.parse_args(args)

        # handle if text client is launched using the "archipelago://name:pass@host:port" url from webhost
        if args.url:
            url = urllib.parse.urlparse(args.url)
            if url.scheme == "archipelago":
                if url.hostname:
                    if url.port:
                        server = shlex.quote(f"--server={url.hostname}:{url.port}")
                    else:
                        server = shlex.quote(f"--server={url.hostname}")
                if url.username:
                    name = shlex.quote(f"--name={urllib.parse.unquote(url.username)}")
                if url.password:
                    password = shlex.quote(f"--password={urllib.parse.unquote(url.password)}")
            else:
                parser.error(f"bad url, found {args.url}, expected url in form of archipelago://archipelago.gg:38281")
    os.chdir(UFO50World.settings.install_folder)

    # check that the mod installation is valid
    is_reinstall = False
    if not is_install_valid():
        # if the user wants to reinstall, we simply remove the existing versions file, so it looks like a blank slate
        if messagebox.askyesnocancel(f"Mod installation missing or corrupted!",
                                     "Would you like to reinstall now?"):
            is_reinstall = True
            if os.path.isfile("versions.json"):
                os.remove("versions.json")
        # if there is no mod installation, and we are not installing it, then there isn't much to do
        else:
            return

    # check if there's a new version
    version_result = download_patch()
    if version_result == UpdateResult.ERROR:
        messagebox.showinfo("Unexpected error",
                            "Could not check for patch updates.\n\n"
                            "This will not prevent the game from being played if it was already playable")
    elif version_result == UpdateResult.API_LIMIT:
        messagebox.showinfo("Rate limit exceeded",
                            "GitHub REST API limit exceeded, could not check for updates.\n\n"
                            "This will not prevent the game from being played if it was already playable")
    elif version_result == UpdateResult.VERSION_MISMATCH:
        # ask if the player wants to update, unless it's a reinstall, in which case we update right away
        if (
                is_reinstall or
                messagebox.askyesnocancel(f"Update found!",
                                          "A new version of the mod has been found.\n"
                                          "Would you like to update now?")
        ):
            # find the right ufo 50 version and patch it
            while not is_install_valid():
                if install():
                    patch_game()
                else:
                    messagebox.showerror("Could not locate executable!",
                                         f"The provided file did not match UFO 50 {get_version()}\n"
                                         f"Please, select ufo50.exe matching version {get_version()}.")
                    # if the user gives up, stop trying to update
                    if not messagebox.askyesnocancel(f"Could not locate executable!",
                                                     "Would you like to try again?"):
                        return

    # and try to launch the game
    if UFO50World.settings.launch_game:
        logging.info("Launching game.")
        try:
            subprocess.Popen(f"{UFO50World.settings.launch_command} {name} {password} {server}", shell=True)
        except FileNotFoundError:
            error = ("Could not run the game!\n\n"
                     "Please check that launch_command in options.yaml or host.yaml is set up correctly")
            messagebox.showerror("Command error!", f"Error: {error}")
            raise RuntimeError(error)
