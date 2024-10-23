import typing

from typing import TYPE_CHECKING
from NetUtils import ClientStatus
from random import Random
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from .utils import Constants
from .locations import get_location_id_for_duelist, duelist_from_location_id, is_duelist_location_id
from .duelists import Duelist, all_duelists, name_to_duelist
from .version import __version__

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
    from NetUtils import JSONMessagePart

COMBINED_WRAM: typing.Final[str] = "Combined WRAM"

def get_wins_from_bytes(b: bytes) -> int:
    return int.from_bytes(b, "little")

class YGODDMClient(BizHawkClient):
    game: str = Constants.GAME_NAME
    system: str = "GBA"
    patch_suffix: str = ".apygoddm"
    local_checked_locations: typing.Set[int]
    checked_version_string: bool
    random: Random

    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = set()

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:

        try:
            # this import down here to prevent circular import issue
            from CommonClient import logger
            # Check ROM name/patch version
            rom_name_bytes = ((await bizhawk.read(ctx.bizhawk_ctx, [(0xA0, 12, "ROM")]))[0])
            rom_name = bytes([byte for byte in rom_name_bytes if byte != 0]).decode("ascii")
            logger.info(rom_name + " rom_name")
            if not rom_name.startswith("YU-GI-OH DDM"):
                return False
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False  # Should verify on the next pass

        ctx.game = self.game
        ctx.items_handling = 0b111 # Has this been set correctly? A little confusion
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125
        logger.info(f"YGO Dungeon Dice Monsters Client v{__version__}.")
        # Add updates section to logger info
        return True

    async def read_dice_collection(self, ctx: "BizHawkClientContext") -> bytes:
        return (await bizhawk.read(
            ctx.bizhawk_ctx, [(Constants.DICE_COLLECTION_OFFSET, 124, COMBINED_WRAM)]
        ))[0]

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if not ctx.finished_game and any(item.item == Constants.VICTORY_ITEM_ID for item in ctx.items_received):
            await ctx.send_msgs([{
                "cmd": "StatusUpdate",
                "status": ClientStatus.CLIENT_GOAL
            }])
            ctx.finished_game = True

        if ctx.slot_data is not None:
            # in YGO FM this is a version mismatch check between user vs generated world

            # Unlock duelists based on who has been received

            unlocked_duelist_bitflags: int = 0
            for item in ctx.items_received:
                if is_duelist_location_id(item.item):
                    unlocked_duelist_bitflags |= duelist_from_location_id(item.item).bitflag
                    print (unlocked_duelist_bitflags)

            if unlocked_duelist_bitflags != 0:
                await bizhawk.write(ctx.bizhawk_ctx, [(
                    Constants.DUELIST_UNLOCK_OFFSET,
                    [unlocked_duelist_bitflags],
                    COMBINED_WRAM
                )])


            # Read number of wins over each duelist for 'duelist defeated' locations

            read_list: typing.List[typing.Tuple[int, int, str]] = [
                (d.wins_address, 2, COMBINED_WRAM) for d in all_duelists
            ]
            wins_bytes: typing.List[bytes] = await bizhawk.read(ctx.bizhawk_ctx, read_list)
            duelists_to_wins: typing.Dict[Duelist, int] = {
                d: get_wins_from_bytes(w) for d, w in zip(all_duelists, wins_bytes)
            }
            new_local_check_locations: typing.Set[int] = set([
                get_location_id_for_duelist(key) for key, value in duelists_to_wins.items() if value != 0
            ])

            #print("Win Mem check")
            #for duelist, wins in duelists_to_wins.items():
            #    if duelist is Duelist.YUGI_MOTO:
            #        print("Yugi Moto Wins")
            #        print (wins)

            #    print(all_duelists[i].name)
            #    print(all_duelists[i].wins_address)
            #    print(read_list[i])
            #    print(wins_bytes[i])
            #    print(new_local_check_locations)



            # Here YGO FM does a check for card checks then does a union of the two sets

            if new_local_check_locations != self.local_checked_locations:
                self.local_checked_locations = new_local_check_locations
                if new_local_check_locations is not None:
                    print ("send check!")
                    await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": list(new_local_check_locations)
                    }])