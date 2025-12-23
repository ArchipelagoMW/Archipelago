import asyncio
from collections.abc import Sequence

import colorama

from CommonClient import get_base_parser, handle_url_arg

# !!! IMPORTANT !!!
# The client implementation is *not* meant for teaching.
# Obviously, it is written to the best of its author's abilities,
# but it is not to the same standard as the rest of the apworld.
# Copy things from here at your own risk.


def launch_ap_quest_client(*args: Sequence[str]) -> None:
    from .ap_quest_client import main

    parser = get_base_parser()
    parser.add_argument("--name", default=None, help="Slot Name to connect as.")
    parser.add_argument("url", nargs="?", help="Archipelago connection url")

    launch_args = handle_url_arg(parser.parse_args(args))

    colorama.just_fix_windows_console()

    asyncio.run(main(launch_args))
    colorama.deinit()
