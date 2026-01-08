"""Common classes and functions for the N64 client for DK64."""

import asyncio
import urllib.request
import os
import json
import sys
from ap_version import version as ap_version
from Utils import get_settings


class DK64MemoryMap:
    """DK64MemoryMap is a class that contains memory addresses and offsets used in the game Donkey Kong 64."""

    name_location = 0xD0A0A6F8
    memory_pointer = 0x807FFF1C
    counter_offset = 0x000
    start_flag = 0x002
    arch_items = 0x004
    fed_string = 0x008
    connection = 0x029
    fed_subtitle = 0x02B
    EEPROM = 0x807ECEA8
    CurrentGamemode = 0x80755314
    NextGamemode = 0x80755318
    current_map = 0x8076A0A8
    safety_text_timer = 0x02A
    end_credits = 0x1B0
    send_death = 0x05C  # If donk player dies. Set this back to 0 upon receiving that the donk player has died
    receive_death = 0x05D  # If someone else dies, this will kill the donk player
    can_die = 0x05E  # If death is received, the game will queue the death until this is 1. It is generally a good idea to not send a death to the donk player if this is zero
    text_timer = 0x05F  # can be any value between 50 and 255, Under 50 gets weird, Defaults to 130 at boot, which is the standard speed
    # Ammo addresses (all 2 byte values)
    ammo_base = 0x807FCC40  # Base ammo address
    homing_ammo = 0x807FCC42  # Homing ammo
    oranges = 0x807FCC44  # Oranges
    crystal_coconuts = 0x807FCC46  # Crystal coconuts
    film = 0x807FCC48  # Film (for fairy camera)
    ammo_belt = 0x807FC953  # (0, 1 or 2) 1 byte
    banana_fairies = 0x0000000
    tag_kong = 0x060  # Byte to set the current kong to this. Check can_tag before setting this if you want safety. Resets back to -1 upon successful tag
    # 0 = DK
    # 1 = Diddy
    # 2 = Lanky
    # 3 = Tiny
    # 4 = Chunky
    # 5 = Random

    can_tag = 0x061
    current_kong = 0x8074E77C


all_tasks = set()


def create_task_log_exception(awaitable) -> asyncio.Task:
    """Create an asyncio task that logs any exceptions raised during its execution.

    Args:
        awaitable: An awaitable object (e.g., coroutine) to be executed.
    Returns:
        asyncio.Task: The created asyncio task.
    The task will log any exceptions raised during its execution using the logger.
    It will also remove itself from the `all_tasks` set upon completion.
    """
    from CommonClient import logger

    async def _log_exception(awaitable):
        try:
            return await awaitable
        except Exception as e:
            logger.exception(e)
            pass
        finally:
            all_tasks.remove(task)
        return

    task = asyncio.create_task(_log_exception(awaitable))
    all_tasks.add(task)
    return task


def check_version():
    """Check for a new version of the DK64 Rando from GitHub releases."""
    try:
        from CommonClient import logger
    except Exception:
        # Create a logger if it doesn't exist
        import logging

        logger = logging.getLogger("DK64Client")
    try:
        from tkinter import Tk, messagebox

        # Read host config to determine release branch
        release_branch = "master"  # Default to master
        options = get_settings()
        # Use a 'dk64' section for DK64-specific settings
        dk64_options = options.get("dk64_options", {})
        release_branch = dk64_options.get("release_branch", "master")
        # Save back the release_branch if not present
        if "release_branch" not in dk64_options:
            dk64_options["release_branch"] = release_branch
            options["dk64_options"] = dk64_options
            options.save()

        # Determine repository and API endpoint based on release_branch
        if release_branch == "dev" or release_branch == "develop":
            repo = "2dos/DK64-Randomizer-dev"
            api_endpoint = f"https://api.github.com/repos/{repo}/releases/latest"
        elif release_branch.startswith("v"):
            # Specific version requested from dev repo
            repo = "2dos/DK64-Randomizer-dev"
            api_endpoint = f"https://api.github.com/repos/{repo}/releases/tags/{release_branch}"
        else:
            # Default to master branch from release repo
            repo = "2dos/DK64-Randomizer-Release"
            api_endpoint = f"https://api.github.com/repos/{repo}/releases/latest"

        request = urllib.request.Request(api_endpoint, headers={"User-Agent": "DK64Client/1.0"})
        with urllib.request.urlopen(request) as response:
            data = json.load(response)
            latest_tag = data.get("tag_name")
            if latest_tag and latest_tag.startswith("v"):
                # Remove the 'v' prefix to get the version number
                api_version = latest_tag[1:]
                api_major = api_version.split(".")[0]
                api_minor = api_version.split(".")[1]
                api_patch = api_version.split(".")[2]
                # Get the current version from the ap_version.py file
                ap_major = ap_version.split(".")[0]
                ap_minor = ap_version.split(".")[1]
                ap_patch = ap_version.split(".")[2]

                # Check if we should update based on release_branch setting
                should_update = False
                if release_branch.startswith("v"):
                    # Specific version requested - update if current version doesn't match
                    requested_version = release_branch[1:]  # Remove 'v' prefix
                    should_update = api_version != ap_version
                    if should_update:
                        logger.warning(f"Specific version requested: {requested_version} (current: {ap_version})")
                    # Get the latest dev version for informational purposes
                    try:
                        dev_request = urllib.request.Request("https://api.github.com/repos/2dos/DK64-Randomizer-dev/releases/latest", headers={"User-Agent": "DK64Client/1.0"})
                        with urllib.request.urlopen(dev_request) as dev_response:
                            dev_data = json.load(dev_response)
                            latest_dev_tag = dev_data.get("tag_name")
                            if latest_dev_tag and latest_dev_tag.startswith("v"):
                                latest_dev_version = latest_dev_tag[1:]
                                logger.info(f"Latest version available: {latest_dev_version}")
                    except Exception as e:
                        logger.warning(f"Could not check latest dev version: {e}")
                else:
                    # Latest version check - update if newer version available
                    should_update = (int(api_major), int(api_minor), int(api_patch)) > (int(ap_major), int(ap_minor), int(ap_patch))
                    if should_update:
                        logger.warning(f"Warning: New version of DK64 Rando available: {api_version} (current: {ap_version})")

                if should_update:
                    # Check if we're installed in an apworld in custom_worlds/dk64.apworld
                    # Check if the file exists
                    apworld_output = "./custom_worlds/dk64.apworld"
                    if os.path.exists(apworld_output):
                        should_install = ask_yes_no_cancel("Update Available", "A new version of DK64 Rando is available. Would you like to install it?")
                        if not should_install:
                            return

                        # Find the dk64.apworld asset in the release
                        assets = data.get("assets", [])
                        apworld_asset = None
                        for asset in assets:
                            if asset.get("name") == "dk64.apworld":
                                apworld_asset = asset
                                break

                        if not apworld_asset:
                            logger.warning("No dk64.apworld asset found in the latest release")
                            return

                        download_url = apworld_asset.get("browser_download_url")
                        if not download_url:
                            logger.warning("No download URL found for dk64.apworld asset")
                            return

                        try:
                            with urllib.request.urlopen(download_url) as response:
                                data = response.read()
                                # Delete the original AP World in the folder
                                os.remove(apworld_output)
                                # Save as .apworld
                                with open(apworld_output, "wb") as f:
                                    f.write(data)
                                print(f"APWorld file saved as {apworld_output}")
                                root = Tk()
                                root.withdraw()
                                messagebox.showinfo("Update Complete", f"New version of DK64 Rando installed as {apworld_output}")
                                root.update()
                                sys.exit(1)
                        except Exception as e:
                            logger.warning(f"Failed to download or save the new APWorld file: {e}")
                    else:
                        logger.warning("-" * 50)
                        logger.warning("New version of DK64 Rando available, but no APWorld file found. Please update manually.")
                        logger.warning("-" * 50)
                else:
                    logger.info("You are running the latest version of DK64 Rando.")
    except Exception as e:
        print(e)
        print("Failed to check for new version of DK64")


def ask_yes_no_cancel(title: str, text: str) -> bool | None:
    """Wrap for tkinter.messagebox.askyesnocancel, that creates a popup dialog box with yes, no, and cancel buttons.

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
