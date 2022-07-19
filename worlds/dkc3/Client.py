from __future__ import annotations

import sys
import threading
import time
import multiprocessing
import os
import subprocess
import base64
import shutil
import logging
import asyncio
import enum
import typing

from json import loads, dumps

#import ModuleUpdate
#ModuleUpdate.update()

from Utils import init_logging

if __name__ == "__main__":
    init_logging("DKC3Client", exception_logger="Client")

import colorama
import websockets

from NetUtils import ClientStatus, color
from .Rom import ROM_PLAYER_LIMIT
import Utils
from CommonClient import CommonContext, server_loop, ClientCommandProcessor, gui_enabled, get_base_parser
from SNIClient import Context, snes_buffered_write, snes_flush_writes, SNESState, snes_connect, snes_read
from Patch import GAME_DKC3

snes_logger = logging.getLogger("SNES")

from MultiServer import mark_raw


class DKC3Context(Context):

    def on_deathlink(self, data: dict):
        if not self.killing_player_task or self.killing_player_task.done():
            # This could be an "If game is ___, import deathlink_kill_player from world._____.Client"
            # Doing so would potentially remove the need to have this subclass entirely
            self.killing_player_task = asyncio.create_task(deathlink_kill_player(self))
        super(DKC3Context, self).on_deathlink(data)
        
    def run_gui(self):
        from kvui import GameManager

        class SNIManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago"),
                ("SNES", "SNES"),
            ]
            base_title = "Archipelago DKC3 Client"

        self.ui = SNIManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


async def deathlink_kill_player(ctx: DKC3Context):
    ctx.death_state = DeathState.killing_player
    while ctx.death_state == DeathState.killing_player and \
            ctx.snes_state == SNESState.SNES_ATTACHED:
        await snes_flush_writes(ctx)
        await asyncio.sleep(1)

        #if ctx.game == GAME_DKC3:
            # DKC3_TODO: Handle Receiving Deathlink
        ctx.last_death_link = time.time()


# DKC3 - DKC3_TODO: Check these values
ROM_START = 0x000000
WRAM_START = 0xF50000
WRAM_SIZE = 0x20000
SRAM_START = 0xE00000

SAVEDATA_START = WRAM_START + 0xF000
SAVEDATA_SIZE = 0x500

DKC3_ROMNAME_START = 0x00FFC0
DKC3_ROMHASH_START = 0x7FC0
ROMNAME_SIZE = 0x15
ROMHASH_SIZE = 0x15

DKC3_RECV_PROGRESS_ADDR = WRAM_START + 0x632     # DKC3_TODO: Find a permanent home for this
DKC3_FILE_NAME_ADDR = WRAM_START + 0x5D9
DEATH_LINK_ACTIVE_ADDR = DKC3_ROMNAME_START + 0x15     # DKC3_TODO: Find a permanent home for this


async def game_watcher(ctx: DKC3Context):
    prev_game_timer = 0
    perf_counter = time.perf_counter()
    while not ctx.exit_event.is_set():
        try:
            await asyncio.wait_for(ctx.watcher_event.wait(), 0.125)
        except asyncio.TimeoutError:
            pass
        ctx.watcher_event.clear()

        if not ctx.rom:
            ctx.finished_game = False
            ctx.death_link_allow_survive = False
            game_name = await snes_read(ctx, DKC3_ROMNAME_START, 0x15)
            if game_name is None or game_name != b"DONKEY KONG COUNTRY 3":
                continue
            else:
                ctx.game = GAME_DKC3
                print("GAME: ", ctx.game)
                ctx.items_handling = 0b111  # remote items

            rom = await snes_read(ctx, DKC3_ROMHASH_START, ROMHASH_SIZE)
            if rom is None or rom == bytes([0] * ROMHASH_SIZE):
                continue

            ctx.rom = rom
            print("ROM: ", ctx.rom)
            #death_link = await snes_read(ctx, DEATH_LINK_ACTIVE_ADDR, 1)
            ## DKC3_TODO: Handle Deathlink
            #if death_link:
            #    ctx.allow_collect = bool(death_link[0] & 0b100)
            #    await ctx.update_death_link(bool(death_link[0] & 0b1))
            if not ctx.prev_rom or ctx.prev_rom != ctx.rom:
                ctx.locations_checked = set()
                ctx.locations_scouted = set()
                ctx.locations_info = {}
            ctx.prev_rom = ctx.rom

            if ctx.awaiting_rom:
                await ctx.server_auth(False)

        if ctx.auth and ctx.auth != ctx.rom:
            # Maybe nuke the ctx.rom and ctx.game to prevent further reads?
            snes_logger.warning("ROM change detected, please reconnect to the multiworld server")
            await ctx.disconnect()

        if ctx.game == GAME_DKC3:
            # DKC3_TODO: Handle Progress and Deathlink
            
            save_file_name = await snes_read(ctx, DKC3_FILE_NAME_ADDR, 0x5)

            if save_file_name is None or save_file_name[0] == 0x00:
                # We haven't loaded a save file
                continue

            from worlds.dkc3.Rom import location_rom_data, item_rom_data
            for loc_id, loc_data in location_rom_data.items():
                if loc_id not in ctx.locations_checked:
                    data = await snes_read(ctx, WRAM_START + loc_data[0], 1)
                    masked_data = data[0] & (1 << loc_data[1])
                    bit_set = (masked_data != 0)
                    invert_bit = ((len(loc_data) >= 3) and loc_data[2])
                    if bit_set != invert_bit:
                        # DKC3_TODO: Handle non-included checks
                        ctx.locations_checked.add(loc_id)
                        location = ctx.location_names[loc_id]
                        print("New Location Check: ", location)
                        snes_logger.info(
                            f'New Check: {location} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
                        await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [loc_id]}])

            # DKC3_TODO: Make this actually visually display new things received (ASM Hook required)
            recv_count = await snes_read(ctx, DKC3_RECV_PROGRESS_ADDR, 1)
            recv_index = recv_count[0]
            #print("Game Index: ", recv_count, " | ctx Index: ", ctx.items_received)
            if recv_index < len(ctx.items_received):
                item = ctx.items_received[recv_index]
                recv_index += 1
                logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                    color(ctx.item_names[item.item], 'red', 'bold'),
                    color(ctx.player_names[item.player], 'yellow'),
                    ctx.location_names[item.location], recv_index, len(ctx.items_received)))

                snes_buffered_write(ctx, DKC3_RECV_PROGRESS_ADDR, bytes([recv_index]))
                if item.item in item_rom_data:
                    item_count = await snes_read(ctx, WRAM_START + item_rom_data[item.item][0], 0x1)
                    new_item_count = item_count[0] + 1
                    for address in item_rom_data[item.item]:
                        snes_buffered_write(ctx, WRAM_START + address, bytes([new_item_count]))

                    # Handle Coin Displays
                    current_level = await snes_read(ctx, WRAM_START + 0x5E3, 0x5)
                    if item.item == 0xDC3002 and (current_level[0] == 0x0A and current_level[2] == 0x00 and current_level[4] == 0x03):
                        # Bazaar and Barter
                        item_count = await snes_read(ctx, WRAM_START + 0xB02, 0x1)
                        new_item_count = item_count[0] + 1
                        snes_buffered_write(ctx, WRAM_START + 0xB02, bytes([new_item_count]))
                    elif item.item == 0xDC3002 and current_level[0] == 0x04:
                        # Swanky
                        item_count = await snes_read(ctx, WRAM_START + 0xA26, 0x1)
                        new_item_count = item_count[0] + 1
                        snes_buffered_write(ctx, WRAM_START + 0xA26, bytes([new_item_count]))
                    elif item.item == 0xDC3003 and (current_level[0] == 0x0A and current_level[2] == 0x08 and current_level[4] == 0x01):
                        # Boomer
                        item_count = await snes_read(ctx, WRAM_START + 0xB02, 0x1)
                        new_item_count = item_count[0] + 1
                        snes_buffered_write(ctx, WRAM_START + 0xB02, bytes([new_item_count]))
                else:
                    # Handle Patch and Skis
                    if item.item == 0xDC3007:
                        num_upgrades = 1
                        inventory = await snes_read(ctx, WRAM_START + 0x605, 0xF)

                        if (inventory[0] & 0x02):
                            num_upgrades = 3
                        elif (inventory[13] & 0x08) or (inventory[0] & 0x01):
                            num_upgrades = 2

                        if num_upgrades == 1:
                            snes_buffered_write(ctx, WRAM_START + 0x605, bytes([inventory[0] | 0x01]))
                            if inventory[4] == 0:
                                snes_buffered_write(ctx, WRAM_START + 0x609, bytes([0x01]))
                            elif inventory[6] == 0:
                                snes_buffered_write(ctx, WRAM_START + 0x60B, bytes([0x01]))
                            elif inventory[8] == 0:
                                snes_buffered_write(ctx, WRAM_START + 0x60D, bytes([0x01]))
                            elif inventory[10] == 0:
                                snes_buffered_write(ctx, WRAM_START + 0x60F, bytes([0x01]))

                            cove_mekanos_progress = await snes_read(ctx, WRAM_START + 0x691, 0x2)
                            snes_buffered_write(ctx, WRAM_START + 0x691, bytes([cove_mekanos_progress[0] | 0x01]))
                            snes_buffered_write(ctx, WRAM_START + 0x692, bytes([cove_mekanos_progress[1] | 0x01]))
                        elif num_upgrades == 2:
                            snes_buffered_write(ctx, WRAM_START + 0x605, bytes([inventory[0] | 0x02]))
                            if inventory[4] == 0:
                                snes_buffered_write(ctx, WRAM_START + 0x609, bytes([0x02]))
                            elif inventory[6] == 0:
                                snes_buffered_write(ctx, WRAM_START + 0x60B, bytes([0x02]))
                            elif inventory[8] == 0:
                                snes_buffered_write(ctx, WRAM_START + 0x60D, bytes([0x02]))
                            elif inventory[10] == 0:
                                snes_buffered_write(ctx, WRAM_START + 0x60F, bytes([0x02]))
                        elif num_upgrades == 3:
                            snes_buffered_write(ctx, WRAM_START + 0x606, bytes([inventory[1] | 0x20]))

                            k3_ridge_progress = await snes_read(ctx, WRAM_START + 0x693, 0x2)
                            snes_buffered_write(ctx, WRAM_START + 0x693, bytes([k3_ridge_progress[0] | 0x01]))
                            snes_buffered_write(ctx, WRAM_START + 0x694, bytes([k3_ridge_progress[1] | 0x01]))
                    elif item.item == 0xDC3000:
                        # Handle Victory
                        if not ctx.finished_game:
                            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                            ctx.finished_game = True
                    else:
                        print("Item Not Recognized: ", item.item)
                    pass

                await snes_flush_writes(ctx)

            # DKC3_TODO: This method of collect should work, however it does not unlock the next level correctly when previous is flagged
            # Handle Collected Locations
            #for loc_id in ctx.checked_locations:
            #    if loc_id not in ctx.locations_checked:
            #        loc_data = location_rom_data[loc_id]
            #        data = await snes_read(ctx, WRAM_START + loc_data[0], 1)
            #        invert_bit = ((len(loc_data) >= 3) and loc_data[2])
            #        if not invert_bit:
            #            masked_data = data[0] | (1 << loc_data[1])
            #            print("Collected Location: ", hex(loc_data[0]), " | ", loc_data[1])
            #            snes_buffered_write(ctx, WRAM_START + loc_data[0], bytes([masked_data]))
            #            await snes_flush_writes(ctx)
            #        else:
            #            masked_data = data[0] & ~(1 << loc_data[1])
            #            print("Collected Inverted Location: ", hex(loc_data[0]), " | ", loc_data[1])
            #            snes_buffered_write(ctx, WRAM_START + loc_data[0], bytes([masked_data]))
            #            await snes_flush_writes(ctx)
            #        ctx.locations_checked.add(loc_id)

            # Calculate Boomer Cost Text
            boomer_cost_text = await snes_read(ctx, 0xF5AAFD, 2)
            if boomer_cost_text[0] == 0x31 and boomer_cost_text[1] == 0x35:
                boomer_cost = await snes_read(ctx, ROM_START + 0xB49857, 1)
                boomer_cost_tens = int(boomer_cost[0]) // 10
                boomer_cost_ones = int(boomer_cost[0]) % 10
                snes_buffered_write(ctx, 0xF5AAFD, bytes([0x30 + boomer_cost_tens, 0x30 + boomer_cost_ones]))
                await snes_flush_writes(ctx)

            boomer_final_cost_text = await snes_read(ctx, 0xF5AB9B, 2)
            if boomer_final_cost_text[0] == 0x32 and boomer_final_cost_text[1] == 0x35:
                boomer_cost = await snes_read(ctx, ROM_START + 0xB49857, 1)
                boomer_cost_tens = boomer_cost[0] // 10
                boomer_cost_ones = boomer_cost[0] % 10
                snes_buffered_write(ctx, 0xF5AB9B, bytes([0x30 + boomer_cost_tens, 0x30 + boomer_cost_ones]))
                await snes_flush_writes(ctx)



async def run_game(romfile):
    auto_start = Utils.get_options()["dkc3_options"].get("rom_start", True)
    if auto_start is True:
        # DKC3_TODO: Fix this hack
        dirname = os.path.dirname(__file__)
        new_dirname = os.path.join(dirname, "..\\..\\")
        os.startfile(os.path.join(new_dirname, romfile))
    elif os.path.isfile(auto_start):
        subprocess.Popen([auto_start, romfile],
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


async def main():
    multiprocessing.freeze_support()
    parser = get_base_parser()
    parser.add_argument('diff_file', default="", type=str, nargs="?",
                        help='Path to a Archipelago Binary Patch file')
    parser.add_argument('--snes', default='localhost:8080', help='Address of the SNI server.')
    parser.add_argument('--loglevel', default='info', choices=['debug', 'info', 'warning', 'error', 'critical'])
    args = parser.parse_args()

    if args.diff_file:
        import Patch
        logging.info("Patch file was supplied. Creating sfc rom..")
        meta, romfile = Patch.create_rom_file(args.diff_file)
        if "server" in meta:
            args.connect = meta["server"]
        logging.info(f"Wrote rom file to {romfile}")
        asyncio.create_task(run_game(romfile))

    ctx = DKC3Context(args.snes, args.connect, args.password)
    if ctx.server_task is None:
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    ctx.snes_connect_task = asyncio.create_task(snes_connect(ctx, ctx.snes_address), name="SNES Connect")
    watcher_task = asyncio.create_task(game_watcher(ctx), name="GameWatcher")

    await ctx.exit_event.wait()

    ctx.server_address = None
    ctx.snes_reconnect_address = None
    if ctx.snes_socket is not None and not ctx.snes_socket.closed:
        await ctx.snes_socket.close()
    await watcher_task
    await ctx.shutdown()


if __name__ == '__main__':
    colorama.init()
    asyncio.run(main())
    colorama.deinit()
