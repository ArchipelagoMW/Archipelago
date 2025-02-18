import asyncio

import dolphin_memory_engine as dme

import ModuleUpdate
from worlds.pokepark_1 import POWERS, BERRIES
from worlds.pokepark_1.adresses import friend_item_checks, \
    unlock_item_checks, \
    berry_item_checks, prisma_item_checks, tmp_addresses_disabled_friendship_overwrite, \
    region_unlock_item_checks, POWER_INCREMENTS, POWER_SHARED_ADDR, blocked_unlocks, prisma_overwrites, \
    driffzeppeli_address, driffzeppeli_value
from worlds.pokepark_1.watcher.location_state_watcher import location_state_watcher
from worlds.pokepark_1.watcher.location_watcher import location_watcher
from worlds.pokepark_1.watcher.logic_watcher import logic_watcher
from worlds.pokepark_1.watcher.state_watcher import state_watcher

ModuleUpdate.update()

import Utils

from NetUtils import ClientStatus
from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, \
    CommonContext, server_loop


old_berry_count = 0
first_berry_check = True


class PokeparkCommandProcessor(ClientCommandProcessor):

    def _cmd_connect(self, address: str = "") -> bool:
        temp = super()._cmd_connect()
        if dme.is_hooked():
            logger.info("Already connected to Dolphin!")
            self._cmd_resync()
        else:
            logger.info("Please connect to Dolphin (may have issues, default is to start game before opening client).")
        if temp:
            return True
        else:
            return False

    def _cmd_resync(self):
        """Manually trigger a resync."""
        self.output(f"Syncing items.")
        self.ctx.syncing = True
        refresh_items(self.ctx)


class PokeparkContext(CommonContext):
    command_processor = PokeparkCommandProcessor
    game = "PokéPark Wii: Pikachu's Adventure"
    items_handling = 0b111  # full remote
    hook_check = False
    hook_nagged = False

    believe_hooked = False
    victory = False

    def __init__(self, server_address, password):
        super(PokeparkContext, self).__init__(server_address, password)
        self.send_index: int = 0
        self.syncing = False
        self.awaiting_bridge = False

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(PokeparkContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()




    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []

    def run_gui(self):
        """Import kivy UI system and start running it as self.ui_task."""
        from kvui import GameManager

        class PokeparkManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Pokepark Client"

        self.ui = PokeparkManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")



def game_start():
    dme.hook()
    return dme.is_hooked()

async def game_watcher(ctx: PokeparkContext):

    while not ctx.exit_event.is_set():

        sync_msg = [{'cmd': 'Sync'}]
        if ctx.locations_checked:
            sync_msg.append({"cmd": "LocationChecks", "locations": list(ctx.locations_checked)})
        await ctx.send_msgs(sync_msg)
        refresh_items(ctx)

        ctx.lives_switch = True

        if ctx.victory and not ctx.finished_game:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True
        if not ctx.hook_check:
            if not ctx.hook_nagged:
                logger.info("Checking Dolphin hookup...")
            dme.hook()
            if dme.is_hooked():
                logger.info("Hooked to Dolphin!")
                ctx.hook_check = True
            elif not ctx.hook_nagged:
                logger.info(
                    "Please connect to Dolphin (may have issues, default is to start game before opening client).")
                ctx.hook_nagged = True

        await asyncio.sleep(0.08)
        ctx.lives_switch = False


def refresh_items(ctx):
    global old_berry_count, first_berry_check
    sums = {}
    for item in ctx.items_received:
        if item.item in unlock_item_checks and not item.item in blocked_unlocks:
            addr, val = unlock_item_checks[item.item]
            sums[addr] = sums.get(addr, 0) + val
    sums[driffzeppeli_address] = sums.get(driffzeppeli_address,0)+driffzeppeli_value
    for address,value in sums.items():
        dme.write_byte(address,value)

    for received_item in ctx.items_received:
        if received_item.item in friend_item_checks:
            for address, value in friend_item_checks[received_item.item]:
                if address not in tmp_addresses_disabled_friendship_overwrite:
                    dme.write_byte(address, value)


    for received_item in ctx.items_received:
        if received_item.item in prisma_item_checks and not received_item.item in prisma_overwrites:
            for address, value in prisma_item_checks[received_item.item]:
                dme.write_word(address, value)

    berry_count_new = sum(1 for item in ctx.items_received if item.item in BERRIES.values())
    if first_berry_check and old_berry_count != berry_count_new:
        old_berry_count = berry_count_new
        first_berry_check = False
        return

    new_berry_items = [item for item in ctx.items_received
                      if item.item in BERRIES.values()][old_berry_count:berry_count_new]
    for received_item in new_berry_items:
        if received_item.item in berry_item_checks:
            for address, value in berry_item_checks[received_item.item]:
                current_berries = int.from_bytes(dme.read_bytes(address, 2), byteorder='big', signed=False)
                if current_berries < 0xFFFF:
                    new_value = min(current_berries + value, 0x270F)
                    dme.write_bytes(address, new_value.to_bytes(2, byteorder='big'))


    old_berry_count = berry_count_new

    thunderbolt_count = sum(1 for item in ctx.items_received
                           if item.item == POWERS["Progressive Thunderbolt"])

    dash_count = sum(1 for item in ctx.items_received
                    if item.item == POWERS["Progressive Dash"])
    health_count = sum(1 for item in ctx.items_received
                    if item.item == POWERS["Progressive Health"])
    if thunderbolt_count > 0 or dash_count > 0 or health_count:
        new_value = POWER_INCREMENTS["thunderbolt"]["base"]
        if thunderbolt_count > 0:
            new_value += sum(POWER_INCREMENTS["thunderbolt"]["increments"][:thunderbolt_count])
        if dash_count > 0:
            new_value += sum(POWER_INCREMENTS["dash"]["increments"][:dash_count])
        if dash_count > 0:
            new_value += sum(POWER_INCREMENTS["health"]["increments"][:health_count])
        dme.write_bytes(POWER_SHARED_ADDR, new_value.to_bytes(2, byteorder='big'))



def send_victory(ctx: PokeparkContext):
    if ctx.victory:
        return

    ctx.victory = True
    ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
    logger.info("Congratulations")
    return

def main(connect= None, password= None):
    Utils.init_logging("PokeparkClient", exception_logger="Client")

    async def _main(connect, password):
        ctx = PokeparkContext(connect, password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        await asyncio.sleep(1)

        game_start()
        if dme.is_hooked():
            logger.info("Hooked to Dolphin!")

        progression_watcher = asyncio.create_task(
            game_watcher(ctx), name="PokeparkProgressionWatcher")
        loc_watch = asyncio.create_task(location_watcher(ctx))
        logic_watch = asyncio.create_task(logic_watcher(ctx))
        state_watch = asyncio.create_task(state_watcher(ctx))
        location_state_watch = asyncio.create_task(location_state_watcher(ctx))

        await progression_watcher
        await loc_watch
        await logic_watch
        await state_watch
        await location_state_watch
        await asyncio.sleep(.25)

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        await asyncio.sleep(.5)

    import colorama
    colorama.init()
    asyncio.run(_main(connect, password))
    colorama.deinit()


if __name__ == "__main__":
    parser = get_base_parser(description="Pokepark Client, for text interfacing.")
    args, rest = parser.parse_known_args()
    main(args.connect, args.password)

