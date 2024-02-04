import io
import logging
import os.path
import subprocess
import urllib.request
from pathlib import Path
from shutil import which
from tkinter.messagebox import askyesnocancel
from typing import Any, Optional
from zipfile import ZipFile
from Utils import open_file

import requests

from Utils import is_linux, is_windows, messagebox, tuplize_version


def launch_game(url: Optional[str] = None) -> None:
    """Check the game installation, then launch it"""
    if not (is_linux or is_windows):
        return

    def courier_installed() -> bool:
        """Check if Courier is installed"""
        return os.path.exists(os.path.join(folder, "miniinstaller-log.txt"))

    def mod_installed() -> bool:
        """Check if the mod is installed"""
        return os.path.exists(os.path.join(folder, "Mods", "TheMessengerRandomizerAP", "courier.toml"))

    def request_data(request_url: str) -> Any:
        """Fetches json response from given url"""
        logging.info(f"requesting {request_url}")
        response = requests.get(request_url)
        if response.status_code == 200:  # success
            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError:
                raise RuntimeError(f"Unable to fetch data. (status code {response.status_code})")
        else:
            raise RuntimeError(f"Unable to fetch data. (status code {response.status_code})")
        return data

    def install_courier() -> None:
        """Installs latest version of Courier"""
        # can't use latest since courier uses pre-release tags
        courier_url = "https://api.github.com/repos/Brokemia/Courier/releases"
        latest_download = request_data(courier_url)[0]["assets"][-1]["browser_download_url"]
    
        with urllib.request.urlopen(latest_download) as download:
            with ZipFile(io.BytesIO(download.read()), "r") as zf:
                zf.extractall(folder)
    
        working_directory = os.getcwd()
        os.chdir(folder)
        # linux handling
        if is_linux:
            mono_exe = which("mono")
            if not mono_exe:
                # download and use mono kickstart
                # this allows steam deck support
                mono_kick_url = "https://github.com/flibitijibibo/MonoKickstart/archive/refs/heads/main.zip"
                target = os.path.join(folder, "monoKickstart")
                with urllib.request.urlopen(mono_kick_url) as download:
                    with ZipFile(io.BytesIO(download.read()), "r") as zf:
                        os.makedirs(target, exist_ok=True)
                        zf.extractall(target)
                installer = subprocess.Popen([os.path.join(target, "precompiled"),
                                              os.path.join(folder, "MiniInstaller.exe")], shell=False)
            else:
                installer = subprocess.Popen([mono_exe, os.path.join(folder, "MiniInstaller.exe")], shell=False)
        else:
            installer = subprocess.Popen(os.path.join(folder, "MiniInstaller.exe"), shell=False)

        failure = installer.wait()
        if failure:
            messagebox("Failure", "Failed to install Courier", True)
            os.chdir(working_directory)
            raise RuntimeError("Failed to install Courier")
        os.chdir(working_directory)
    
        if courier_installed():
            messagebox("Success!", "Courier successfully installed!")
            return
        messagebox("Failure", "Failed to install Courier", True)
        raise RuntimeError("Failed to install Courier")

    def install_mod() -> None:
        """Installs latest version of the mod"""
        # TODO: add /latest before actual PR since i want pre-releases for now
        get_url = "https://api.github.com/repos/alwaysintreble/TheMessengerRandomizerModAP/releases"
        assets = request_data(get_url)[0]["assets"]
        for asset in assets:
            if "TheMessengerRandomizerAP" in asset["name"]:
                release_url = asset["browser_download_url"]
                break
        else:
            messagebox("Failure!", "something went wrong while trying to get latest mod version")
            logging.error(assets)
            return

        with urllib.request.urlopen(release_url) as download:
            with ZipFile(io.BytesIO(download.read()), "r") as zf:
                zf.extractall(folder)

        messagebox("Success!", "Latest mod successfully installed!")

    def available_mod_update() -> bool:
        """Check if there's an available update"""
        get_url = "https://api.github.com/repos/alwaysintreble/TheMessengerRandomizerModAP/releases"
        assets = request_data(get_url)[0]["assets"]
        # TODO simplify once we're done with 0.13.0 alpha
        for asset in assets:
            if "TheMessengerRandomizerAP" in asset["name"]:
                if asset["label"]:
                    latest_version = asset["label"]
                    break
                names = asset["name"].strip(".zip").split("-")
                if len(names) > 2:
                    if names[-1].isnumeric():
                        latest_version = names[-1]
                        break
                    latest_version = 1
                    break
                latest_version = names[1]
                break
        else:
            return False

        toml_path = os.path.join(folder, "Mods", "TheMessengerRandomizerAP", "courier.toml")
        with open(toml_path, "r") as f:
            installed_version = f.read().splitlines()[1].strip("version = \"")

        logging.info(f"Installed version: {installed_version}. Latest version: {latest_version}")
        if not installed_version.isnumeric():
            if installed_version[-1].isnumeric():
                installed_version = installed_version[-1]
            else:
                installed_version = 1
            return int(latest_version) > int(installed_version)
        elif int(latest_version) >= 1:
            return True
        return tuplize_version(latest_version) > tuplize_version(installed_version)

    from . import MessengerWorld
    folder = os.path.dirname(MessengerWorld.settings.game_path)
    if not courier_installed():
        should_install = askyesnocancel("Install Courier",
                                        "No Courier installation detected. Would you like to install now?")
        if not should_install:
            return
        logging.info("Installing Courier")
        install_courier()
    if not mod_installed():
        should_install = askyesnocancel("Install Mod",
                                        "No randomizer mod detected. Would you like to install now?")
        if not should_install:
            return
        logging.info("Installing Mod")
        install_mod()
    else:
        if available_mod_update():
            should_update = askyesnocancel("Update Mod",
                                           "Old mod version detected. Would you like to update now?")
            if should_update:
                logging.info("Updating mod")
                install_mod()
    if is_linux:
        if url:
            open_file(f"steam://rungameid/764790//{url}/")
        else:
            open_file("steam://rungameid/764790")
    else:
        os.chdir(Path(MessengerWorld.settings.game_path).parent)
        if url:
            subprocess.Popen([MessengerWorld.settings.game_path, str(url)])
        else:
            subprocess.Popen(MessengerWorld.settings.game_path)
