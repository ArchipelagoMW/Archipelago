import asyncio
import colorama

from CommonClient import get_base_parser, handle_url_arg

from .. import constants


def launch_tomba_client(*args) -> None:
    from TombaClient import main

    parser = get_base_parser(description=f"{constants.GAME} Client.")
    parser.add_argument("--name", default=None, help="Slot Name to connect as.")
    parser.add_argument("--loglevel", default="info", choices=["debug", "info", "warning", "error"], help="Log level.")
    parser.add_argument("url", nargs="?", help="Archipelago connection url")

    launch_args = handle_url_arg(parser.parse_args(args))

    colorama.just_fix_windows_console()

    asyncio.run(main(launch_args))
    colorama.deinit()
