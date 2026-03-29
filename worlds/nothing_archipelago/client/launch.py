import asyncio
from collections.abc import Sequence
import colorama
from CommonClient import get_base_parser,handle_url_arg

def launch_nothing_archipelago()-> None:
    from .nothing_archipelago_client import main
    from ..Game.main import Game

    APnothing = Game()
    asyncio.run(APnothing.run())
    asyncio.run(main(APnothing))
    colorama.deinit()