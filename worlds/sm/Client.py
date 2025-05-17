import logging
import time
from typing import NamedTuple

from NetUtils import ClientStatus, color
import worlds._polyemu as polyemu

from .Rom import SM_ROM_MAX_PLAYERID


snes_logger = logging.getLogger("SNES")

DOMAINS = polyemu.PLATFORMS.SNES


class SMAddress(NamedTuple):
    address: int
    size: int | None
    domain: int


SM_ROMNAME = SMAddress(0x007FC0, 0x15, DOMAINS.ROM)

# SM_INGAME_MODES = {0x07, 0x09, 0x0b}  # Currently unused
SM_ENDGAME_MODES = {0x26, 0x27}
SM_DEATH_MODES = {0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A}

# RECV and SEND are from the gameplay's perspective: this client writes to RECV queue and reads from SEND queue
SM_RECV_QUEUE_START  = SMAddress(0x2000, None, DOMAINS.SRAM)
SM_RECV_QUEUE_WCOUNT = SMAddress(0x2602, 2, DOMAINS.SRAM)
SM_SEND_QUEUE_START  = SMAddress(0x2700, None, DOMAINS.SRAM)
SM_SEND_QUEUE_RCOUNT = SMAddress(0x2680, 2, DOMAINS.SRAM)
SM_SEND_QUEUE_WCOUNT = SMAddress(0x2682, 2, DOMAINS.SRAM)

SM_DEATH_LINK_ACTIVE_ADDR = SMAddress(0x277F04, 1, DOMAINS.ROM)
SM_REMOTE_ITEM_FLAG_ADDR = SMAddress(0x277F06, 1, DOMAINS.ROM)


class SuperMetroidClient(polyemu.PolyEmuClient):
    game = "Super Metroid"
    platform = polyemu.PLATFORMS.SNES
    patch_suffix = (".apsm", ".apm3")

    async def validate_rom(self, ctx):
        rom_name = (await polyemu.read(ctx.polyemu_ctx, [SM_ROMNAME]))[0]
        if rom_name == bytes([0] * SM_ROMNAME.size) or rom_name[:2] != b"SM" or rom_name[2] not in b"1234567890":
            return False

        ctx.game = self.game

        # versions lower than 0.3.0 dont have item handling flag nor remote item support
        rom_version = int(rom_name[2:5].decode("UTF-8"))
        if rom_version < 30:
            ctx.items_handling = 0b001 # full local
        else:
            ctx.items_handling = (await polyemu.read(ctx.polyemu_ctx, [SM_REMOTE_ITEM_FLAG_ADDR]))[0][0]

        death_link = (await polyemu.read(ctx.polyemu_ctx, [SM_DEATH_LINK_ACTIVE_ADDR]))[0][0]

        if death_link:
            # ctx.allow_collect = bool(death_link[0] & 0b100)
            # ctx.death_link_allow_survive = bool(death_link[0] & 0b10)
            await ctx.update_death_link(bool(death_link[0] & 0b1))
        
        return True

    async def game_watcher(self, ctx):
        if ctx.server is None or ctx.slot is None:
            # not successfully connected to a multiworld server, cannot process the game sending items
            return

        write_list = []

        try:
            game_mode = (await polyemu.read(ctx.polyemu_ctx, [(0x0998, 1, DOMAINS.WRAM)]))[0][0]
            if "DeathLink" in ctx.tags and game_mode and ctx.last_death_link + 1 < time.time():
                currently_dead = game_mode in SM_DEATH_MODES
                # await ctx.handle_deathlink_state(currently_dead)
            if game_mode in SM_ENDGAME_MODES:
                if not ctx.finished_game:
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    ctx.finished_game = True
                return
            print("asdfff")

            data = (await polyemu.read(ctx.polyemu_ctx, [SM_SEND_QUEUE_RCOUNT, SM_SEND_QUEUE_WCOUNT]))

            recv_index = int.from_bytes(data[0], "little")
            recv_item = int.from_bytes(data[1], "little")

            while recv_index < recv_item:
                print("a")
                item_address = recv_index * 8
                message = (await polyemu.read(ctx.polyemu_ctx, [(SM_SEND_QUEUE_START.address + item_address, 8, SM_SEND_QUEUE_START.domain)]))[0]
                item_index = (message[4] | (message[5] << 8)) >> 3

                recv_index += 1
                write_list.append((
                    SM_SEND_QUEUE_RCOUNT.address,
                    bytes([recv_index & 0xFF, (recv_index >> 8) & 0xFF]),
                    SM_SEND_QUEUE_RCOUNT.domain,
                ))

                from . import locations_start_id
                location_id = locations_start_id + item_index

                ctx.locations_checked.add(location_id)
                location = ctx.location_names.lookup_in_game(location_id)
                snes_logger.info(f"New Check: {location} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})")
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}])

            data = (await polyemu.read(ctx.polyemu_ctx, [SM_RECV_QUEUE_WCOUNT]))[0]

            item_out_ptr = data[0] | (data[1] << 8)
            print(item_out_ptr)

            from . import items_start_id
            from . import locations_start_id
            if item_out_ptr < len(ctx.items_received):
                print("b")
                item = ctx.items_received[item_out_ptr]
                item_id = item.item - items_start_id
                if bool(ctx.items_handling & 0b010) or item.location < 0:  # item.location < 0 for !getitem to work
                    location_id = (item.location - locations_start_id) if (item.location >= 0 and item.player == ctx.slot) else 0xFF
                else:
                    location_id = 0x00  #backward compat

                player_id = item.player if item.player <= SM_ROM_MAX_PLAYERID else 0
                write_list.append((
                    SM_RECV_QUEUE_START.address + (item_out_ptr * 4),
                    bytes([player_id & 0xFF, (player_id >> 8) & 0xFF, item_id & 0xFF, location_id & 0xFF]),
                    SM_RECV_QUEUE_START.domain
                ))
                item_out_ptr += 1
                write_list.append((
                    SM_RECV_QUEUE_WCOUNT.address,
                    bytes([item_out_ptr & 0xFF, (item_out_ptr >> 8) & 0xFF]),
                    SM_RECV_QUEUE_WCOUNT.domain
                ))
                logging.info("Received %s from %s (%s) (%d/%d in list)" % (
                    color(ctx.item_names.lookup_in_game(item.item), "red", "bold"),
                    color(ctx.player_names[item.player], "yellow"),
                    ctx.location_names.lookup_in_slot(item.location, item.player), item_out_ptr, len(ctx.items_received)))

            await polyemu.write(ctx.polyemu_ctx, write_list)
        except polyemu.ConnectionLostError:
            pass
