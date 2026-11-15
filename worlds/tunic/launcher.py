import argparse
import logging
import os
import subprocess

from Utils import messagebox
from worlds.LauncherComponents import Component, Type, components


logger = logging.getLogger(__name__)


def launch_game(*args: str) -> None:
    from . import TunicWorld

    try:
        game_folder = os.path.dirname(TunicWorld.settings.game_path)
    except ValueError as e:
        logger.error(e)
        messagebox(
            "Invalid File",
            "Please try again and ensure you select Tunic.exe or Secret Legend.exe.",
        )
        return

    working_directory = os.getcwd()
    parser = argparse.ArgumentParser(description="TUNIC Launcher")
    parser.add_argument("url", type=str, nargs="?", help="Archipelago Webhost URI to auto connect to.")
    parsed_args = parser.parse_args(args)
    os.chdir(game_folder)
    if parsed_args.url:
        subprocess.Popen([TunicWorld.settings.game_path, str(parsed_args.url)])
    else:
        subprocess.Popen(TunicWorld.settings.game_path)
    os.chdir(working_directory)


def attempt_launch_ut(*args: str) -> None:
    try:
        from worlds.tracker import launch_client

        launch_client(*args)
    except ImportError as e:
        logger.error(e)
        messagebox(
            "Cannot Load UT",
            "There was an error loading Universal Tracker. Please ensure it is installed and up to date.",
        )


components.extend(
    (
        Component(
            "TUNIC",
            func=launch_game,
            game_name="TUNIC",
            component_type=Type.HIDDEN,
            supports_uri=True,
        ),
        Component(
            "Universal Tracker for TUNIC",
            func=attempt_launch_ut,
            game_name="TUNIC",
            component_type=Type.HIDDEN,
            supports_uri=True,
        ),
    )
)
