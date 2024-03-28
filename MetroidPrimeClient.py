import asyncio
import traceback

import dolphin_memory_engine
from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, logger, server_loop, gui_enabled
import Utils
from worlds.metroidprime.DolphinClient import DolphinException
from worlds.metroidprime.MetroidPrimeInterface import MetroidPrimeInterface
from enum import Enum
class MetroidPrimeCommandProcessor(ClientCommandProcessor):
  def __init__(self, ctx: CommonContext):
    super().__init__(ctx)

class MetroidPrimeContext(CommonContext):
  command_processor = MetroidPrimeCommandProcessor
  game_interface: MetroidPrimeInterface
  game = "Metroid Prime"
  items_handling = 0b111
  dolphin_sync_task = None

  def __init__(self, server_address, password):
    super().__init__(server_address, password)
    self.game_interface = MetroidPrimeInterface(logger)

  def on_deathlink(self, data: Utils.Dict[str, Utils.Any]) -> None:
    super().on_deathlink(data)
    logger.info()

  async def server_auth(self, password_requested: bool = False):
    if password_requested and not self.password:
        await super(MetroidPrimeContext, self).server_auth(password_requested)
    await self.get_username()
    await self.send_connect()

async def dolphin_sync_task(ctx: MetroidPrimeContext):
  logger.info("Starting Dolphin connector")
  while not ctx.exit_event.is_set():
    try:
      if ctx.game_interface.is_connected() and ctx.game_interface.is_in_playable_state():
        await _handle_game_ready(ctx)
      else:
        await _handle_game_not_ready(ctx)
    except Exception as e:
      if isinstance(e, DolphinException):
        logger.error(str(e))
      else:
        logger.error(traceback.format_exc())

      logger.info("Attempting to reconnect to Dolphin")
      await ctx.disconnect()
      await asyncio.sleep(3)
      continue

async def _handle_game_ready(ctx: MetroidPrimeContext):
  if ctx.server and ctx.slot:
    if "DeathLink" in ctx.tags:
      logger.warn("DeathLink not implemented")
    # await give_items(ctx)
    # await check_locations(ctx)
  await asyncio.sleep(0.5)

async def _handle_game_not_ready(ctx: MetroidPrimeContext):
  """If the game is not connected or not in a playable state, this will attempt to retry connecting to the game."""
  if not ctx.game_interface.is_connected():
    logger.info("Attempting to connect to Dolphin")
    ctx.game_interface.connect_to_game()
  elif not ctx.game_interface.is_in_playable_state():
    logger.info("Waiting for player to load a save file or start a new game")
    await asyncio.sleep(3)

def main(connect=None, password=None):
  Utils.init_logging("Metroid Prime Client")

  async def _main(connect, password):
    ctx = MetroidPrimeContext(connect, password)
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
    if gui_enabled:
      ctx.run_gui()
    await asyncio.sleep(1)

    ctx.dolphin_sync_task = asyncio.create_task(dolphin_sync_task(ctx), name="DolphinSync")

    await ctx.exit_event.wait()
    ctx.server_address = None

    await ctx.shutdown()

    if ctx.dolphin_sync_task:
        await asyncio.sleep(3)
        await ctx.dolphin_sync_task

  import colorama

  colorama.init()
  asyncio.run(_main(connect, password))
  colorama.deinit()

if __name__ == "__main__":
    parser = get_base_parser()
    args = parser.parse_args()
    main(args.connect, args.password)