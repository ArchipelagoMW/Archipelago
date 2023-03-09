import logging
import asyncio
import time

from NetUtils import ClientStatus, color
from worlds.AutoSNIClient import SNIClient

snes_logger = logging.getLogger("SNES")

# FXPAK Pro protocol memory mapping used by SNI
ROM_START = 0x000000
WRAM_START = 0xF50000
WRAM_SIZE = 0x20000
SRAM_START = 0xE00000

# KDL3
KDL3_GAME_STATE = SRAM_START + 0x36D0
KDL3_KIRBY_HP = SRAM_START + 0x39D1
KDL3_ABILITY_ARRAY = SRAM_START + 0x3800
KDL3_WORLD_1_HEARTS = SRAM_START + 0x53A7

class KDL3SNIClient(SNIClient):
    game = "Kirby's Dream Land 3"

    async def deathlink_kill_player(self, ctx) -> None:
        from SNIClient import DeathState, snes_buffered_write, snes_flush_writes, snes_read
        game_state = await snes_read
