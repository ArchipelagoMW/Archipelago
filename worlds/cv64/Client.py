import logging
import asyncio

from NetUtils import ClientStatus, color
from worlds.AutoSNIClient import SNIClient

CV64_ROMNAME_START = 0x000020
CV64_ROMHASH_START = 0x0010
ROMNAME_SIZE = 0x0B
ROMHASH_SIZE = 0x08


class CV64SNIClient(SNIClient):
    game = "CASTLEVANIA"

    async def deathlink_kill_player(self, ctx):
        pass

    async def validate_rom(self, ctx):
        return False
        # TODO: Wait for SNI to finally get its planned N64 support, I guess!

    async def game_watcher(self, ctx):
        pass
