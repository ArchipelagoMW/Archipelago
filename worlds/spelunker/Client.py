import logging
import struct
import time
from struct import pack
from .Rom import location_table, hidden_table
from typing import TYPE_CHECKING, Dict, Set

# TODO:  Remove this when Archipelago 0.4.4 gets released
import sys

if "worlds._bizhawk" not in sys.modules:
    import importlib
    import os
    import zipimport

    bh_apworld_path = os.path.join(
        os.path.dirname(sys.modules["worlds"].__file__), "_bizhawk.apworld"
    )
    if os.path.isfile(bh_apworld_path):
        importer = zipimport.zipimporter(bh_apworld_path)
        spec = importer.find_spec(os.path.basename(bh_apworld_path).rsplit(".", 1)[0])
        mod = importlib.util.module_from_spec(spec)
        mod.__package__ = f"worlds.{mod.__package__}"
        mod.__name__ = f"worlds.{mod.__name__}"
        sys.modules[mod.__name__] = mod
        importer.exec_module(mod)
    elif not os.path.isdir(os.path.splitext(bh_apworld_path)[0]):
        raise AssertionError("Could not import worlds._bizhawk")

from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
import time

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
else:
    BizHawkClientContext = object

# Add .apwl suffix to bizhawk client
from worlds.LauncherComponents import SuffixIdentifier, components

for component in components:
    if component.script_name == "BizHawkClient":
        component.file_identifier = SuffixIdentifier(
            *(*component.file_identifier.suffixes, ".apsplunker")
        )
        break

EXPECTED_ROM_NAME = "SPELUNKERAP"


class SpelunkerClient(BizHawkClient):
    game = "Spelunker"
    system = ("NES")
    location_map = location_table
    received_deathlinks = 0
    deathlink_all_clear = False

    def __init__(self) -> None:
        super().__init__()

    async def validate_rom(self, ctx: BizHawkClientContext) -> bool:
        from CommonClient import logger

        try:
            # Check ROM name/patch version
            rom_name_bytes = (
                await bizhawk.read(ctx.bizhawk_ctx, [(0x7030, 11, "PRG ROM")])
            )[0]
            rom_name = bytes([byte for byte in rom_name_bytes if byte != 0]).decode(
                "ascii"
            )
            if not rom_name.startswith(EXPECTED_ROM_NAME):
                logger.info(
                    "ERROR: Rom is not valid!"
                )
                return False
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False  # Should verify on the next pass

        ctx.game = self.game
        ctx.items_handling = 0b111

        death_link = await bizhawk.read(ctx.bizhawk_ctx, [(0x7052, 1, "PRG ROM")])
        if death_link:
            await ctx.update_death_link(bool(death_link[0]))
        return True

    async def set_auth(self, ctx: BizHawkClientContext) -> None:
        from CommonClient import logger

        slot_name_length = await bizhawk.read(ctx.bizhawk_ctx, [(0x7040, 1, "PRG ROM")])
        slot_name_bytes = await bizhawk.read(
            ctx.bizhawk_ctx, [(0x7041, slot_name_length[0][0], "PRG ROM")]
        )
        ctx.auth = bytes([byte for byte in slot_name_bytes[0] if byte != 0]).decode(
            "utf-8"
        )

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict) -> None:
        if cmd != "Bounced":
            return
        if "tags" not in args:
            return
        if "DeathLink" in args["tags"] and args["data"]["source"] != ctx.slot_info[ctx.slot].name:
            self.received_deathlinks += 1

    async def game_watcher(self, ctx: BizHawkClientContext) -> None:
        from CommonClient import logger

        if ctx.server_version.build > 0:
            ctx.connected = True
        else:
            ctx.connected = False
            ctx.refresh_connect = True

        if ctx.slot_data != None:
            ctx.data_present = True
        else:
            ctx.data_present = False

        if ctx.server is None or ctx.server.socket.closed or ctx.slot_data is None:
            return

        from .Rom import item_ids

        #if goal_flag[0] != 0x00:
            #await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            #ctx.finished_game = True

        read_state = await bizhawk.read(ctx.bizhawk_ctx, [(0x229, 1, "RAM"),
                                                            (0x0500, 0xFF, "RAM"),
                                                            (0x0780, 1, "RAM"),
                                                            (0x7051, 1, "PRG ROM"),
                                                            (0x022C, 1, "RAM"),
                                                            (0x022D, 1, "RAM"),
                                                            (0x0783, 1, "RAM"),
                                                            (0x0781, 1, "RAM")])

        demo_mode = int.from_bytes(read_state[0], "little")
        loc_array = bytearray(read_state[1])
        item_pause = int.from_bytes(read_state[2], "little")
        hidden_checks = int.from_bytes(read_state[3], "little")
        is_dead = int.from_bytes(read_state[4], "little")
        is_paused = int.from_bytes(read_state[5], "little")
        goal_trigger = int.from_bytes(read_state[6], "little")
        recv_count = int.from_bytes(read_state[7], "big")

        if hidden_checks == 0x01:
            self.location_map.update(hidden_table)

        if demo_mode != 0x00:
            return

        if item_pause != 0x00:
            return

        if is_dead == 0x00:
            self.deathlink_all_clear = True

        if "DeathLink" in ctx.tags and ctx.last_death_link + 1 < time.time():
            if is_dead in range(0x01,0x80) and self.received_deathlinks == 0x00 and is_paused != 0xFF and self.deathlink_all_clear == True:
                self.deathlink_all_clear = False
                await ctx.send_death(f"{ctx.player_names[ctx.slot]} died!")

        #The death animation is long enough to send 2 deathlinks per death
        if self.received_deathlinks != 0:
            await bizhawk.write(ctx.bizhawk_ctx, [(0x780, bytes([0x0D]), "RAM")])
            self.received_deathlinks -= 1

        new_checks = []

        for loc_id, loc_pointer in self.location_map.items():
            if loc_id not in ctx.locations_checked:
                location = loc_array[loc_pointer]
                if location == 0:
                    new_checks.append(loc_id)

            if loc_id in ctx.checked_locations:
                loc_array[loc_pointer] = 0 

        await bizhawk.write(ctx.bizhawk_ctx, [(0x0500, loc_array, "RAM")])
                
        for new_check_id in new_checks:
            ctx.locations_checked.add(new_check_id)
            location = ctx.location_names[new_check_id]
            await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [new_check_id]}])

        if recv_count < len(ctx.items_received):
            item = ctx.items_received[recv_count]
            recv_count += 1

            if item.item in item_ids:
                ram_item = item_ids[item.item]
                await bizhawk.write(ctx.bizhawk_ctx, [(0x780, bytes([ram_item]), "RAM")])
                await bizhawk.write(ctx.bizhawk_ctx, [(0x781, bytes([recv_count]), "RAM")])

        if not ctx.finished_game and goal_trigger == 0x01:
            await ctx.send_msgs([{
                "cmd": "StatusUpdate",
                "status": ClientStatus.CLIENT_GOAL
            }])


