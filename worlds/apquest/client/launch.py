import asyncio
from collections.abc import Sequence

import colorama
from CommonClient import get_base_parser, handle_url_arg

from worlds.LauncherComponents import Component, Type, components, launch_subprocess

# !!! IMPORTANT !!!
# The client implementation is *not* meant for teaching.
# Obviously, it is written to the best of its author's abilities,
# but it is not to the same standard as the rest of the apworld.
# Copy things from here at your own risk.


def launch_client(*args: Sequence[str]) -> None:
    from .ap_quest_client import main

    parser = get_base_parser()
    parser.add_argument("--name", default=None, help="Slot Name to connect as.")
    parser.add_argument("url", nargs="?", help="Archipelago connection url")

    launch_args = handle_url_arg(parser.parse_args(args))

    colorama.just_fix_windows_console()

    asyncio.run(main(launch_args))
    colorama.deinit()


def run_client(*args) -> None:
    launch_subprocess(launch_client, name="APQuest Client", args=args)


components.append(
    Component(
        "APQuest Client",
        func=run_client,
        game_name="APQuest",
        component_type=Type.CLIENT,
        supports_uri=True,
    )
)
