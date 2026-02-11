import asyncio
import json
import logging
import pkgutil
from typing import TYPE_CHECKING

from NetUtils import ClientStatus
from Options import Toggle
from Utils import async_start

from .._bizhawk import ConnectorError, RequestFailedError, guarded_write, read, write
from .._bizhawk.client import BizHawkClient
from .locations import LocationData, all_locations, events

if TYPE_CHECKING:
    from .._bizhawk.context import BizHawkClientContext, BizHawkClientCommandProcessor

logger = logging.getLogger("Client")


def get_version() -> str:
    return json.loads(pkgutil.get_data(__name__, "archipelago.json").decode())["world_version"]



def _cmd_deathlink(self: "BizHawkClientCommandProcessor"):
    """Toggles death_link from client. Temporarily overrides yaml setting, resets after closing client."""
    from worlds._bizhawk.context import BizHawkClientContext
    if self.ctx.game != "The Minish Cap":
        logger.info("You cannot run this command from outside The Minish Cap")

    assert isinstance(self.ctx, BizHawkClientContext)
    client = self.ctx.client_handler
    assert isinstance(client, MinishCapClient)
    client.death_link_mode = 1 if client.death_link_mode != 1 else 0
    if client.death_link_mode:
        client.previous_death_link = self.ctx.last_death_link
    async_start(self.ctx.update_death_link(client.death_link_mode != 0), name="Update Deathlink")
    logger.info("Deathlink Mode: %s", get_deathlink_mode_name(client.death_link_mode))


def _cmd_deathlink_gameover(self: "BizHawkClientCommandProcessor"):
    """Toggles death_link_gameover from client. Temporarily overrides yaml setting, resets after closing client."""
    from worlds._bizhawk.context import BizHawkClientContext
    if self.ctx.game != "The Minish Cap":
        logger.info("You cannot run this command from outside The Minish Cap")

    assert isinstance(self.ctx, BizHawkClientContext)
    client = self.ctx.client_handler
    assert isinstance(client, MinishCapClient)
    client.death_link_mode = 2 if client.death_link_mode != 2 else 0
    if client.death_link_mode:
        client.previous_death_link = self.ctx.last_death_link
    async_start(self.ctx.update_death_link(client.death_link_mode != 0), name="Update Deathlink")
    logger.info("Deathlink Mode: %s", get_deathlink_mode_name(client.death_link_mode))


def get_deathlink_mode_name(mode: int) -> str:
    return "Disabled" if mode == 0 else "Fairy" if mode == 1 else "Game Over"


ROM_ADDRS = {"game_identifier": (0xA0, 8, "ROM")}

RAM_ADDRS = {
    # 0x00: Gameplay
    # 0x01: File creation
    # 0x02: Language menu
    # 0x03: File options
    # 0x04: File select
    # 0x05: File copy
    # 0x06: File delete
    # 0x07: File load
    "game_task": (0x1002, 1, "IWRAM"),
    # 0x00 = Initialise Room
    # 0x01 = Change Room
    # 0x02 = Update
    # 0x03 = Change Area
    # 0x04 = Minish Portal
    # 0x05 = Barrel Update
    # 0x06 = Reserved
    # 0x07 = Subtask
    "task_substate": (0x1004, 1, "IWRAM"),
    # The room id in the 1st byte, area id in the 2nd
    "room_area_id": (0x0BF4, 2, "IWRAM"),
    # 0x00 Denotes whether the player can input, 0x01 cannot input. Not to be confused with can move/interact.
    # Can still be set to 0x00 when the player is in confusing situations such as reading textboxes
    "action_state": (0x116C, 1, "IWRAM"),
    # 0x11: Standard gameplay
    # 0x12: Reading dialog?
    # 0x13: Growing (yes, there's a separate state for growing from minish and none for shrinking)
    # 0x16: Watching Cutscene
    "link_priority": (0x1171, 1, "IWRAM"),
    # An arbitrary address that isn't used strictly by the game
    # We'll use it to store the index of the last processed remote item
    "received_index": (0x2A44, 2, "EWRAM"),
    "vaati_address": (0x2CA6, 1, "EWRAM"),
    "pedestal_address": (0x2D0B, 1, "EWRAM"),
    "link_health": (0x11A5, 1, "IWRAM"),
    "gameover": (0x10A5, 1, "IWRAM"),
}


class MinishCapClient(BizHawkClient):
    game = "The Minish Cap"
    system = "GBA"
    patch_suffix = ".aptmc"
    location_by_id: dict[int, LocationData]
    room: int
    death_link_mode = -1
    previous_death_link = 0
    """Timestamp of when the last deathlink was processed"""
    death_link_ready = False
    """Whether the player is expected to be in a death state"""
    event_data = list(map(lambda e: (e[0], 1, "EWRAM"), events.keys()))
    events_sent = set()
    player_name: str | None
    seed_verify = False
    version_checked = False

    def __init__(self) -> None:
        super().__init__()
        self.location_by_id = {loc_data.id: loc_data for loc_data in all_locations}
        self.room = 0x0000

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            # Check ROM name/patch version
            rom_name_bytes = (await read(ctx.bizhawk_ctx, [ROM_ADDRS["game_identifier"]]))[0]
            rom_name = bytes([byte for byte in rom_name_bytes if byte != 0]).decode("ascii")
            if rom_name != "GBAZELDA":
                return False

            if "deathlink" in ctx.command_processor.commands:
                ctx.command_processor.commands.pop("deathlink")
            if "deathlink_gameover" in ctx.command_processor.commands:
                ctx.command_processor.commands.pop("deathlink_gameover")
        except UnicodeDecodeError:
            return False
        except RequestFailedError:
            return False

        ctx.game = self.game
        ctx.items_handling = 0b101
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.5
        name_bytes = (await read(ctx.bizhawk_ctx, [(0x000600, 16, "ROM")]))[0]
        name = bytes([byte for byte in name_bytes if byte != 0]).decode("UTF-8")
        self.player_name = name

        ctx.command_processor.commands["deathlink"] = _cmd_deathlink
        ctx.command_processor.commands["deathlink_gameover"] = _cmd_deathlink_gameover

        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        ctx.auth = self.player_name

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ctx.server is None or ctx.server.socket.closed or ctx.slot_data is None:
            return

        if ctx.slot_data["remote_items"] == Toggle.option_true and not ctx.items_handling & 0b010:
            ctx.items_handling = 0b111
            async_start(ctx.send_msgs([{
                "cmd": "ConnectUpdate",
                "items_handling": ctx.items_handling
            }]))

            # Need to make sure items handling updates and we get the correct list of received items
            # before continuing. Otherwise we might give some duplicate items and skip others.
            # Should patch remote_items option value into the ROM in the future to guarantee we get the
            # right item list before entering this part of the code
            await asyncio.sleep(0.75)
            return

        try:
            if ctx.server_seed_name is None:
                return
            if not self.seed_verify:
                seed = await read(ctx.bizhawk_ctx, [(0x000620, len(ctx.server_seed_name), "ROM")])
                seed = seed[0].decode("UTF-8")
                if seed not in ctx.server_seed_name:
                    logger.info("ERROR: The ROM you loaded is for a different game of AP. "
                                "Please make sure the host has sent you the correct patch file,"
                                "and that you have opened the correct ROM.")
                    raise ConnectorError("Loaded ROM is for Incorrect lobby.")
                logger.info("Seed verified")
                self.seed_verify = True

            if self.death_link_mode < 0:
                if ctx.slot_data.get("death_link", 0) == 0:
                    self.death_link_mode = 0
                    await ctx.update_death_link(False)
                elif ctx.slot_data.get("death_link_gameover", 0) == 0:
                    self.death_link_mode = 1
                    self.previous_death_link = ctx.last_death_link
                    await ctx.update_death_link(True)
                else:
                    self.death_link_mode = 2
                    self.previous_death_link = ctx.last_death_link
                    await ctx.update_death_link(True)
                logger.info("Deathlink Mode: %s", get_deathlink_mode_name(self.death_link_mode))

            if not self.version_checked:
                self.version_checked = True
                multiworld_version = ctx.slot_data["version"]
                client_version = get_version()
                if multiworld_version != client_version:
                    logger.warn(f"The multiworld was generated on v{multiworld_version} but the client is using "
                                f"v{client_version}. Consult the apworld releases page to ensure the versions are "
                                "compatible.")

            # Handle giving the player items
            read_result = await read(ctx.bizhawk_ctx, [
                RAM_ADDRS["game_task"],  # Current state of game (is the player actually in-game?)
                RAM_ADDRS["task_substate"],  # Is there any room transitions or anything similar
                RAM_ADDRS["room_area_id"],
                RAM_ADDRS["action_state"],
                RAM_ADDRS["received_index"],
                RAM_ADDRS["link_health"],
                RAM_ADDRS["gameover"],
            ])
            if read_result is None:
                return

            game_task = read_result[0][0]
            task_substate = read_result[1][0]
            room_area_id = int.from_bytes(read_result[2], "little")
            action_state = read_result[3][0]
            received_index = (read_result[4][0] << 8) + read_result[4][1]
            link_health = int.from_bytes(read_result[5], "little")
            gameover = bool.from_bytes(read_result[6])

            # Check for goal, since vaati's defeat triggers a cutscene this has to be checked before the next if
            # specifically because it sets the game_task to 0x04
            if not ctx.finished_game and game_task == 0x04:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

            # Only process items/locations if the player is in "normal" gameplay
            if game_task == 0x02 or task_substate == 0x02:
                await self.handle_item_receiving(ctx, received_index)
                await self.handle_location_sending(ctx)
                await self.handle_event_setting(ctx)

            # Death link handling only if in normal gameplay (0x02) or gameover (0x03)
            if game_task in range(0x02, 0x04) and self.death_link_mode > 0:
                await self.handle_death_link(ctx, link_health, gameover, action_state)

            # Player moved to a new room that isn't the pause menu. Pause menu `room_area_id` == 0x0000
            if task_substate == 0x02 and self.room != room_area_id:
                await self.handle_room_change(ctx, room_area_id)

        except RequestFailedError:
            # The connector didn't respond. Exit handler and return to main loop to reconnect
            pass

    @staticmethod
    async def handle_item_receiving(ctx: "BizHawkClientContext", received_index: int) -> None:
        # Read all pending receive items and dump into game ram
        for i in range(len(ctx.items_received) - received_index):
            write_result = False
            item_id = ctx.items_received[received_index + i].item
            pid, sid = item_id >> 8, item_id & 0xFF
            total = 0
            while not write_result:
                # Write to the address if it hasn't changed
                write_result = await guarded_write(ctx.bizhawk_ctx,
                                                   [(0x3FF10, [pid, sid], "EWRAM")],
                                                   [(0x3FF10, [0x0, 0x0], "EWRAM"), (0x2A4A, [1], "EWRAM")])

                await asyncio.sleep(0.05)
                total += 0.05
                if write_result:
                    total = 1
                if total > 1:
                    break
            if not write_result:
                break
            await write(ctx.bizhawk_ctx, [(
                RAM_ADDRS["received_index"][0],
                [(received_index + i + 1) // 0x100, (received_index + i + 1) % 0x100],
                "EWRAM",
            )])

    async def handle_location_sending(self, ctx: "BizHawkClientContext") -> None:
        # Read all location flags in area and add to pending location checks if updates
        locations_to_read = [self.location_by_id[loc_id] for loc_id in ctx.missing_locations
                             if self.location_by_id[loc_id].ram_addr is not None]
        location_reads = [(loc.ram_addr[0], 1, "EWRAM") for loc in locations_to_read]
        loc_bytes = await read(ctx.bizhawk_ctx, location_reads)
        locs_to_send = [locations_to_read[i].id for i, loc_ram in enumerate(loc_bytes)
                        if loc_ram[0] | locations_to_read[i].ram_addr[1] == loc_ram[0]]
        await self.handle_special_sending(ctx, locs_to_send)
        # Send location checks
        if len(locs_to_send) > 0:
            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": locs_to_send}])

    async def handle_special_sending(self, ctx: "BizHawkClientContext", locs_to_send: list[int]) -> None:
        """Goron Merchant and Cucco Rounds require special handling since they store their bit flags differently"""
        if len(ctx.missing_locations.intersection(SPECIAL_ADDRESSES)) == 0:
            return
        special_read = await read(ctx.bizhawk_ctx, [(0x2CA3, 3, "EWRAM")])
        goron_restocks = (special_read[0][0] & 0xC0).bit_count() + (special_read[0][1] & 0x03).bit_count()
        goron_slot_purchases = (special_read[0][1] & 0x1C) >> 2
        goron_stock = SPECIAL_ADDRESSES[goron_restocks * 3:goron_restocks*3 + 3]
        new_locs = [goron_stock[i] for i in range(3) if goron_slot_purchases & (1 << i)]

        cucco_rounds = special_read[0][2] >> 3  # Reads for rounds 1-9
        final_cucco_round = special_read[0][2] | 0x80 == special_read[0][2]  # Round 10
        new_locs.extend(SPECIAL_ADDRESSES[15:15+cucco_rounds+int(final_cucco_round)])

        locs_to_send.extend(ctx.missing_locations.intersection(new_locs))

    async def handle_death_link(self, ctx: "BizHawkClientContext", link_health: int, game_over: bool,
                                action_state: int) -> None:
        # If we processed a death on a previous loop
        if not self.death_link_ready:
            # Wait until player is not in a game_over state
            if link_health > 0 and not game_over:
                self.death_link_ready = True
            # And/or return out of processing
            return

        gameover_mode = self.death_link_mode == 2

        # If a new death link has come in  different from the last
        if self.previous_death_link != ctx.last_death_link:
            if gameover_mode:
                write_list = [(RAM_ADDRS["gameover"][0], [1], "IWRAM")]
            else:
                write_list = [(RAM_ADDRS["link_health"][0], [0], "IWRAM")]

            # Attempt to kill them if they're safe
            if await guarded_write(ctx.bizhawk_ctx, write_list, [(0x2A4A, [1], "EWRAM")]):
                # Custom "Player safe" address
                # The kill was successful, record the player is dead for the next loop
                self.death_link_ready = False
                # and save the fact that we successfully killed for that deathlink
                self.previous_death_link = ctx.last_death_link
            else:
                # The player wasn't safe, do nothing and wait for the next death
                pass

        # Not receiving death, decide if we send death
        if action_state != 0x0A:
            return
        if gameover_mode and game_over:
            await ctx.send_death(f"{ctx.player_names[ctx.slot]} ran out of fairies!")
            self.previous_death_link = ctx.last_death_link
            self.death_link_ready = False
        elif not gameover_mode and link_health == 0:
            await ctx.send_death(f"{ctx.player_names[ctx.slot]} ran out of hearts!")
            self.previous_death_link = ctx.last_death_link
            self.death_link_ready = False

    async def handle_room_change(self, ctx: "BizHawkClientContext", room_area_id) -> None:
        # Location Scouting
        location_scouts = [loc_id for loc_id in ctx.missing_locations
                           if self.location_by_id[loc_id].room_area == self.room
                           and self.location_by_id[loc_id].scoutable]
        if len(location_scouts) > 0:
            await ctx.send_msgs([{"cmd": "LocationScouts", "locations": location_scouts, "create_as_hint": 2}])

        self.room = room_area_id
        # Room sync for poptracker tab tracking
        await ctx.send_msgs([{
            "cmd": "Set",
            "key": f"tmc_room_{ctx.team}_{ctx.slot}",
            "default": 0,
            "want_reply": False,
            "operations": [{"operation": "replace", "value": room_area_id}]
        }])

    async def handle_event_setting(self, ctx: "BizHawkClientContext") -> None:
        # Batch all events together into one read
        read_events = await read(ctx.bizhawk_ctx, self.event_data)

        if read_events is None:
            return

        for i, (address_pair, event_name) in enumerate(events.items()):
            if event_name in self.events_sent or read_events[i][0] | address_pair[1] != read_events[i][0]:
                continue
            self.events_sent.add(event_name)
            await ctx.send_msgs([{
                "cmd": "Set",
                "key": f"tmc_{event_name}_{ctx.team}_{ctx.slot}",
                "default": 0,
                "want_reply": False,
                "operations": [{"operation": "replace", "value": 1}]
            }])


SPECIAL_ADDRESSES = [
    6029034, 6029035, 6029036,  # Goron Set 1
    6029037, 6029038, 6029039,  # Goron Set 2
    6029040, 6029041, 6029042,  # Goron Set 3
    6029043, 6029044, 6029045,  # Goron Set 4
    6029046, 6029047, 6029048,  # Goron Set 5
    6029068, 6029069, 6029070, 6029071, 6029072, 6029073, 6029074, 6029075, 6029076, 6029077,  # Cucco Rounds 1-10
]
