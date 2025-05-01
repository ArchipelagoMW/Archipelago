import traceback

import dolphin_memory_engine as dme
import asyncio

from worlds.pokepark.adresses import logic_adresses
from CommonClient import logger

delay_seconds = 0.1


async def logic_watcher(ctx):
    def _sub():
        if not dme.is_hooked():
            return
        for address, value in logic_adresses:
            if dme.read_word(address) != value:
                dme.write_word(address, value)

    while not ctx.exit_event.is_set():
        try:
            if not dme.is_hooked():
                dme.hook()
            else:
                _sub()
        except Exception as e:
            logger.error(f"Error in logic_watcher: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            dme.un_hook()

        await asyncio.sleep(delay_seconds)
