from typing import TYPE_CHECKING, Dict, Set
import sys

# NOTE: This code is not necessary if the bizhawk client code is merged
if "worlds._bizhawk" not in sys.modules:
    import importlib
    import os
    import zipimport

    bh_apworld_path = os.path.join(os.path.dirname(
        sys.modules["worlds"].__file__), "_bizhawk.apworld")
    if os.path.isfile(bh_apworld_path):
        importer = zipimport.zipimporter(bh_apworld_path)
        spec = importer.find_spec(os.path.basename(
            bh_apworld_path).rsplit(".", 1)[0])
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

from .data import BASE_OFFSET, data

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
else:
    BizHawkClientContext = object

# Add .apemerald suffix to bizhawk client
from worlds.LauncherComponents import SuffixIdentifier, components
for component in components:
    if component.script_name == "BizHawkClient":
        component.file_identifier = SuffixIdentifier(
            *(*component.file_identifier.suffixes, ".apcrystal"))
        break


EXPECTED_ROM_NAME = "CGB-APV0-00pokemon_crystal"


class PokemonCrystalClient(BizHawkClient):
    game = "Pokemon Crystal"
    system = "GBC"
    local_checked_locations: Set[int]
    # patch_suffix = ".apcrystal"
    local_checked_locations: Set[int]

    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = set()
        self.goal_flag = data.event_flags["EVENT_BEAT_ELITE_FOUR"]

    async def validate_rom(self, ctx: BizHawkClientContext) -> bool:
        from CommonClient import logger

        try:
            # Check ROM name/patch version
            rom_name_bytes = ((await bizhawk.read(ctx.bizhawk_ctx, [(data.rom_addresses["AP_ROM_Version"], 27, "ROM")]))[0])
            rom_name = bytes(
                [byte for byte in rom_name_bytes if byte != 0]).decode("ascii")
            if not rom_name.startswith("CGB"):
                return False
            if rom_name == "CGB-BXTJ-00pokemon_crystal":
                logger.info("ERROR: You appear to be running an unpatched version of Pokemon Crystal. "
                            "You need to generate a patch file and use it to create a patched ROM.")
                return False
            if rom_name != EXPECTED_ROM_NAME:
                logger.info("ERROR: The patch file used to create this ROM is not compatible with "
                            "this client. Double check your client version against the version being "
                            "used by the generator.")
                return False
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False  # Should verify on the next pass

        ctx.game = self.game
        ctx.items_handling = 0b001
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125
        return True

    async def set_auth(self, ctx: BizHawkClientContext) -> None:
        slot_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(data.rom_addresses["AP_Seed_Name"], 64, "ROM")]))[0]
        ctx.auth = bytes(
            [byte for byte in slot_name_bytes if byte != 0]).decode("utf-8")

    async def game_watcher(self, ctx: BizHawkClientContext) -> None:
        # if ctx.slot_data is not None:
        #     if ctx.slot_data["goal"] == Goal.option_champion:
        #         self.goal_flag = IS_CHAMPION_FLAG
        #     elif ctx.slot_data["goal"] == Goal.option_steven:
        #         self.goal_flag = DEFEATED_STEVEN_FLAG
        #     elif ctx.slot_data["goal"] == Goal.option_norman:
        #         self.goal_flag = DEFEATED_NORMAN_FLAG
        try:
            overworld_guard = (
                data.ram_addresses["wArchipelagoSafeWrite"], [1], "WRAM")

            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx, [(data.ram_addresses["wArchipelagoItemReceived"], 4, "WRAM")], [overworld_guard])

            if read_result is None:  # Not in overworld
                return

            num_received_items = int.from_bytes(
                [read_result[0][1], read_result[0][2]], "little")
            received_item_is_empty = read_result[0][0] == 0

            if num_received_items < len(ctx.items_received) and received_item_is_empty:
                next_item = ctx.items_received[num_received_items]
                print("writing next item value: " +
                      str(next_item.item - BASE_OFFSET))
                await bizhawk.write(ctx.bizhawk_ctx, [
                    (data.ram_addresses["wArchipelagoItemReceived"],
                     (next_item.item - BASE_OFFSET).to_bytes(1, "little"), "WRAM")
                ])

            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx,
                [(data.ram_addresses["wEventFlags"], 0x100, "WRAM")],  # Flags
                [overworld_guard]
            )

            if read_result is None:  # Not in overworld, or save block moved
                return

            game_clear = False
            local_checked_locations = set()

            flag_bytes = read_result[0]
            for byte_i, byte in enumerate(flag_bytes):
                for i in range(8):
                    if byte & (1 << i) != 0:
                        flag_id = byte_i * 8 + i

                        location_id = flag_id + BASE_OFFSET
                        if location_id in ctx.server_locations:
                            local_checked_locations.add(location_id)

                        if flag_id == self.goal_flag:
                            game_clear = True

            if local_checked_locations != self.local_checked_locations:
                self.local_checked_locations = local_checked_locations

                if local_checked_locations is not None:
                    await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": list(local_checked_locations)
                    }])

                # Send game clear
            if not ctx.finished_game and game_clear:
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])
        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect
            pass
