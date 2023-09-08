from argparse import Namespace
import asyncio
import json
import os
import subprocess
from typing import Any, Dict, Optional, Tuple
import zipfile

from asyncio import StreamReader, StreamWriter
from pathlib import Path

import bsdiff4

from CommonClient import CommonContext, server_loop, gui_enabled, \
    ClientCommandProcessor, logger, get_base_parser
import Utils
from worlds import network_data_package

from .rom import get_base_rom_path
from .locations import get_level_locations, location_table


SYSTEM_MESSAGE_ID = 0

CONNECTION_TIMING_OUT_STATUS = 'Connection timing out. Please restart your emulator, then restart connector_wl4.lua'
CONNECTION_REFUSED_STATUS = \
    'Connection refused. Please start your emulator and make sure connector_wl4.lua is running'
CONNECTION_RESET_STATUS = 'Connection was reset. Please restart your emulator, then restart connector_wl4.lua'
CONNECTION_TENTATIVE_STATUS = 'Initial Connection Made'
CONNECTION_CONNECTED_STATUS = 'Connected'
CONNECTION_INITIAL_STATUS = 'Connection has not been initiated'

'''
Payload: lua -> client
{
    playerName: string,
    locations: dict,
    deathlinkActive: bool,
    isDead: bool,
    gameComplete: bool
}

Payload: client -> lua
{
    items: list,
    playerNames: list,
    triggerDeath: bool
}

Deathlink logic:
"Dead" is true <-> Wario is at 0 hp.

deathlink_pending: we need to kill the player
deathlink_sent_this_death: we interacted with the multiworld on this death,
    waiting to reset with living link

'''

wl4_loc_name_to_id = network_data_package['games']['Wario Land 4']['location_name_to_id']

script_version: int = 0

def get_item_value(ap_id):
    return ap_id - 0xEC00


class WL4CommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx):
        super().__init__(ctx)

    def _cmd_gba(self):
        '''Check GBA Connection State'''
        if isinstance(self.ctx, WL4Context):
            logger.info(f'GBA Status: {self.ctx.gba_status}')

    def _cmd_deathlink(self):
        '''Toggle deathlink from client. Overrides default setting.'''
        if isinstance(self.ctx, WL4Context):
            self.ctx.deathlink_client_override = True
            self.ctx.deathlink_enabled = not self.ctx.deathlink_enabled
            Utils.async_start(
                self.ctx.update_death_link(self.ctx.deathlink_enabled),
                name='Update Deathlink'
            )


class WL4Context(CommonContext):
    command_processor = WL4CommandProcessor
    game = 'Wario Land 4'
    items_handling = 0b001  # All local

    def __init__(self, server_address, password):
        super().__init__(server_address, password)

        self.gba_streams: Tuple[StreamReader, StreamWriter] = None
        self.gba_sync_task = None
        self.gba_status = CONNECTION_INITIAL_STATUS
        self.awaiting_rom = False

        self.location_list = []

        self.deathlink_enabled = False
        self.deathlink_pending = False
        self.deathlink_sent_this_death = False
        self.deathlink_client_override = False

        self.version_warning = False

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(WL4Context, self).server_auth(password_requested)

        if not self.auth:
            self.awaiting_rom = True
            logger.info(
                'No ROM detected, awaiting conection to Bizhawk to '
                'authenticate to the multiworld server'
            )
            return

        await self.send_connect()

    def on_deathlink(self, data: Dict[str, Any]):
        self.deathlink_pending = True
        super().on_deathlink(data)

    def run_gui(self):
        from kvui import GameManager

        class WL4Manager(GameManager):
            logging_pairs = [
                ('Client', 'Archipelago')
            ]
            base_title = 'Archipelago Wario Land 4 Client'

        self.ui = WL4Manager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name='UI')


def get_payload(ctx: WL4Context):
    if ctx.deathlink_enabled and ctx.deathlink_pending:
        trigger_death = True
        ctx.deathlink_sent_this_death = True
    else:
        trigger_death = False

    payload = json.dumps({
        'items': [get_item_value(item.item) for item in ctx.items_received],
        'senders': [item.player for item in ctx.items_received],
        'playerNames': [name for (i, name) in ctx.player_names.items() if i != 0],
        'triggerDeath': trigger_death,
    })
    return payload


async def parse_payload(payload: dict, ctx: WL4Context, force: bool):
    # Refuse to do anything if ROM is detected as changed
    if ctx.auth and payload['playerName'] != ctx.auth:
        logger.warning('ROM change detected. Disconnecting and reconnecting...')
        ctx.deathlink_enabled = False
        ctx.deathlink_client_override = False
        ctx.finished_game = False
        ctx.location_list = []
        ctx.deathlink_pending = False
        ctx.deathlink_sent_this_death = False
        ctx.auth = payload['playerName']
        await ctx.send_connect()
        return

    # Turn on deathlink if it is on, and if the client hasn't overriden it
    if (payload['deathlinkActive']
            and not ctx.deathlink_enabled
            and not ctx.deathlink_client_override):
        await ctx.update_death_link(True)
        ctx.deathlink_enabled = True

    # Game completion handling
    if payload['gameComplete'] and not ctx.finished_game:
        await ctx.send_msgs([{
            'cmd': 'StatusUpdate',
            'status': 30
        }])
        ctx.finished_game = True

    # Parse item status bits
    item_status = payload['itemStatus']
    locations = []
    for passage in range(6):
        for level in range(6):
            status_bits = item_status[passage * 6 + level] >> 8
            for location in get_level_locations(passage, level):
                _, (_, _, bit), *_ = location_table[location]
                if status_bits & bit:
                    locations.append(location)

    # Locations handling
    if ctx.location_list != locations:
        ctx.location_list = locations
        await ctx.send_msgs([{
            'cmd': 'LocationChecks',
            'locations': [wl4_loc_name_to_id[loc] for loc in ctx.location_list]
        }])

    # Deathlink handling
    if ctx.deathlink_enabled:
        if payload['isDead']:  # Wario is dead
            ctx.deathlink_pending = False
            if not ctx.deathlink_sent_this_death:
                ctx.deathlink_sent_this_death = True
                await ctx.send_death()
        else:  # Wario is alive
            ctx.deathlink_sent_this_death = False


async def gba_sync_task(ctx: WL4Context):
    logger.info('Starting GBA connector. Use /gba for status information.')
    while not ctx.exit_event.is_set():
        error_status = None
        if ctx.gba_streams:
            (reader, writer) = ctx.gba_streams
            msg = get_payload(ctx).encode()
            writer.write(msg)
            writer.write(b'\n')
            try:
                await asyncio.wait_for(writer.drain(), timeout=1.5)
                try:
                    # Data will return a dict with up to four fields
                    # 1. str: player name (always)
                    # 2. int: script version (always)
                    # 3. dict[str, byte]: value of location's memory byte
                    # 4. bool: whether the game currently registers as complete
                    data = await asyncio.wait_for(reader.readline(), timeout=10)
                    data_decoded = json.loads(data.decode())
                    reported_version = data_decoded.get('scriptVersion', 0)
                    if reported_version >= script_version:
                        if ctx.game is not None and 'itemStatus' in data_decoded:
                            # Not just a keep alive ping, parse
                            asyncio.create_task((parse_payload(data_decoded, ctx, False)))
                        if not ctx.auth:
                            ctx.auth = data_decoded['playerName']

                            if ctx.awaiting_rom:
                                logger.info('Awaiting data from ROM...')
                                await ctx.server_auth(False)
                    else:
                        if not ctx.version_warning:
                            logger.warning(f'Your Lua script is version {reported_version}, expected {script_version}.'
                                           'Please update to the latest version.'
                                           'Your connection to the Archipelago server will not be accepted.')
                            ctx.version_warning = True
                except asyncio.TimeoutError:
                    logger.debug('Read Timed Out, Reconnecting')
                    error_status = CONNECTION_TIMING_OUT_STATUS
                    writer.close()
                    ctx.gba_streams = None
                except ConnectionResetError:
                    logger.debug('Read failed due to Connection Lost, Reconnecting')
                    error_status = CONNECTION_RESET_STATUS
                    writer.close()
                    ctx.gba_streams = None
            except TimeoutError:
                logger.debug('Connection Timed Out, Reconnecting')
                error_status = CONNECTION_TIMING_OUT_STATUS
                writer.close()
                ctx.gba_streams = None
            except ConnectionResetError:
                logger.debug('Connection Lost, Reconnecting')
                error_status = CONNECTION_RESET_STATUS
                writer.close()
                ctx.gba_streams = None
            if ctx.gba_status == CONNECTION_TENTATIVE_STATUS:
                if not error_status:
                    logger.info('Successfully Connected to GBA')
                    ctx.gba_status = CONNECTION_CONNECTED_STATUS
                else:
                    ctx.gba_status = f'Was tentatively connected but error occurred: {error_status}'
            elif error_status:
                ctx.gba_status = error_status
                logger.info('Lost connection to GBA and attempting to reconnect. Use /gba for status updates')
        else:
            try:
                logger.debug('Attempting to connect to GBA')
                ctx.gba_streams = await asyncio.wait_for(asyncio.open_connection('localhost', 28922), timeout=10)
                ctx.gba_status = CONNECTION_TENTATIVE_STATUS
            except TimeoutError:
                logger.debug('Connection Timed Out, Trying Again')
                ctx.gba_status = CONNECTION_TIMING_OUT_STATUS
                continue
            except ConnectionRefusedError:
                logger.debug('Connection Refused, Trying Again')
                ctx.gba_status = CONNECTION_REFUSED_STATUS
                continue


async def run_game(romfile):
    options = Utils.get_options().get('wl4_options', None)
    if options is None:
        auto_start = True
    else:
        auto_start = options.get('rom_start', True)
    if auto_start:
        import webbrowser
        webbrowser.open(romfile)
    elif os.path.isfile(auto_start):
        subprocess.Popen([auto_start, romfile],
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


async def patch_and_run_game(wl4_path: Path):
    with zipfile.ZipFile(wl4_path, 'r') as patch_archive:
        try:
            with patch_archive.open('delta.bsdiff4', 'r') as stream:
                patch_data = stream.read()
        except KeyError:
            raise FileNotFoundError('Patch file missing from archive.')
    rom_file = get_base_rom_path()

    with open(rom_file, 'rb') as rom:
        rom_bytes = rom.read()
    patched_bytes = bsdiff4.patch(rom_bytes, patch_data)
    patched_rom_file = wl4_path.with_suffix('.gba')
    with open(patched_rom_file,'wb') as patched_rom:
        patched_rom.write(patched_bytes)

    asyncio.create_task(run_game(patched_rom_file))


parser = get_base_parser()
parser.add_argument('apwl4_file', default=None, type=Path, nargs='?',
                    help='Path to an APWL4 file')

async def run_client(args: Namespace):
    ctx = WL4Context(args.connect, args.password)
    ctx.server_task = asyncio.create_task(server_loop(ctx), name='Server Loop')

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    if args.apwl4_file is not None:
        Utils.async_start(patch_and_run_game(args.apwl4_file))

    ctx.gba_sync_task = asyncio.create_task(gba_sync_task(ctx), name='GBA Sync')

    await ctx.exit_event.wait()
    await ctx.shutdown()


def launch():
    import colorama
    colorama.init()
    asyncio.run(run_client(parser.parse_args()))
    colorama.deinit()
