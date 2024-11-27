import argparse
import io
import logging
import os.path
import subprocess
import urllib.request
from shutil import which
from typing import Any
from zipfile import ZipFile
from Utils import open_file

import requests

from Utils import is_windows, messagebox, tuplize_version


MOD_URL = "https://api.github.com/repos/alwaysintreble/TheMessengerRandomizerModAP/releases/latest"


def ask_yes_no_cancel(title: str, text: str) -> bool | None:
    """
    Wrapper for tkinter.messagebox.askyesnocancel, that creates a popup dialog box with yes, no, and cancel buttons.

    :param title: Title to be displayed at the top of the message box.
    :param text: Text to be displayed inside the message box.
    :return: Returns True if yes, False if no, None if cancel.
    """
    from tkinter import Tk, messagebox
    root = Tk()
    root.withdraw()
    ret = messagebox.askyesnocancel(title, text)
    root.update()
    return ret


def launch_game(*args) -> None:
    """Check the game installation, then launch it"""
    def courier_installed() -> bool:
        """Check if Courier is installed"""
        assembly_path = os.path.join(game_folder, "TheMessenger_Data", "Managed", "Assembly-CSharp.dll")
        with open(assembly_path, "rb") as assembly:
            for line in assembly:
                if b"Courier" in line:
                    return True
        return False

    def mod_installed() -> bool:
        """Check if the mod is installed"""
        return os.path.exists(os.path.join(game_folder, "Mods", "TheMessengerRandomizerAP", "courier.toml"))

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
                for member in zf.infolist():
                    zf.extract(member, path=game_folder)
    
        os.chdir(game_folder)
        # linux and mac handling
        if not is_windows:
            mono_exe = which("mono")
            if not mono_exe:
                # download and use mono kickstart
                # this allows steam deck support
                mono_kick_url = "https://github.com/flibitijibibo/MonoKickstart/archive/716f0a2bd5d75138969090494a76328f39a6dd78.zip"
                files = []
                with urllib.request.urlopen(mono_kick_url) as download:
                    with ZipFile(io.BytesIO(download.read()), "r") as zf:
                        for member in zf.infolist():
                            if "precompiled/" not in member.filename or member.filename.endswith("/"):
                                continue
                            member.filename = member.filename.split("/")[-1]
                            if member.filename.endswith("bin.x86_64"):
                                member.filename = "MiniInstaller.bin.x86_64"
                            zf.extract(member, path=game_folder)
                            files.append(member.filename)
                mono_installer = os.path.join(game_folder, "MiniInstaller.bin.x86_64")
                os.chmod(mono_installer, 0o755)
                installer = subprocess.Popen(mono_installer, shell=False)
                failure = installer.wait()
                for file in files:
                    os.remove(file)
            else:
                installer = subprocess.Popen([mono_exe, os.path.join(game_folder, "MiniInstaller.exe")], shell=True)
                failure = installer.wait()
        else:
            installer = subprocess.Popen(os.path.join(game_folder, "MiniInstaller.exe"), shell=True)
            failure = installer.wait()

        print(failure)
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
        assets = request_data(MOD_URL)["assets"]
        if len(assets) == 1:
            release_url = assets[0]["browser_download_url"]
        else:
            for asset in assets:
                if "TheMessengerRandomizerAP" in asset["name"]:
                    release_url = asset["browser_download_url"]
                    break
            else:
                messagebox("Failure", "Failed to find latest mod download", True)
                raise RuntimeError("Failed to install Mod")

        mod_folder = os.path.join(game_folder, "Mods")
        os.makedirs(mod_folder, exist_ok=True)
        with urllib.request.urlopen(release_url) as download:
            with ZipFile(io.BytesIO(download.read()), "r") as zf:
                for member in zf.infolist():
                    zf.extract(member, path=mod_folder)

        messagebox("Success!", "Latest mod successfully installed!")

    def available_mod_update(latest_version: str) -> bool:
        """Check if there's an available update"""
        latest_version = latest_version.lstrip("v")
        toml_path = os.path.join(game_folder, "Mods", "TheMessengerRandomizerAP", "courier.toml")
        with open(toml_path, "r") as f:
            installed_version = f.read().splitlines()[1].strip("version = \"")

        logging.info(f"Installed version: {installed_version}. Latest version: {latest_version}")
        # one of the alpha builds
        return "alpha" in latest_version or tuplize_version(latest_version) > tuplize_version(installed_version)

    from . import MessengerWorld
    try:
        game_folder = os.path.dirname(MessengerWorld.settings.game_path)
    except ValueError as e:
        logging.error(e)
        messagebox("Invalid File", "Selected file did not match expected hash. "
                   "Please try again and ensure you select The Messenger.exe.")
        return
    working_directory = os.getcwd()
    # setup ssl context
    try:
        import certifi
        import ssl
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=certifi.where())
        context.set_alpn_protocols(["http/1.1"])
        https_handler = urllib.request.HTTPSHandler(context=context)
        opener = urllib.request.build_opener(https_handler)
        urllib.request.install_opener(opener)
    except ImportError:
        pass
    if not courier_installed():
        should_install = ask_yes_no_cancel("Install Courier",
                                           "No Courier installation detected. Would you like to install now?")
        if not should_install:
            return
        logging.info("Installing Courier")
        install_courier()
    if not mod_installed():
        should_install = ask_yes_no_cancel("Install Mod",
                                           "No randomizer mod detected. Would you like to install now?")
        if not should_install:
            return
        logging.info("Installing Mod")
        install_mod()
    else:
        latest = request_data(MOD_URL)["tag_name"]
        if available_mod_update(latest):
            should_update = ask_yes_no_cancel("Update Mod",
                                              f"New mod version detected. Would you like to update to {latest} now?")
            if should_update:
                logging.info("Updating mod")
                install_mod()
            elif should_update is None:
                return

    if not args:
        should_launch = ask_yes_no_cancel("Launch Game",
                                          "Mod installed and up to date. Would you like to launch the game now?")
        if not should_launch:
            return

    parser = argparse.ArgumentParser(description="Messenger Client Launcher")
    parser.add_argument("url", type=str, nargs="?", help="Archipelago Webhost uri to auto connect to.")
    args = parser.parse_args(args)

    if not is_windows:
        if args.url:
            open_file(f"steam://rungameid/764790//{args.url}/")
        else:
            open_file("steam://rungameid/764790")
    else:
        os.chdir(game_folder)
        if args.url:
            subprocess.Popen([MessengerWorld.settings.game_path, str(args.url)])
        else:
            subprocess.Popen(MessengerWorld.settings.game_path)
        os.chdir(working_directory)
