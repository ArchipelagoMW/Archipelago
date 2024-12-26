import logging
import math
from typing import TYPE_CHECKING, List, Optional, Set

from numpy.matlib import empty

from MultiServer import mark_raw
from NetUtils import ClientStatus, NetworkItem

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from . import item_to_index
from .boosterpack_contents import Booster_Card
from .boosterpacks_data import booster_pack_data, booster_card_id_to_name, rarities

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

logger = logging.getLogger("Client")

rarity_sort_order  = {
    "Secret Rare Alt 1": 0,
    "Secret Rare": 1,
    "Ultra Rare": 2,
    "Super Rare": 3,
    "Rare": 4,
    "Common": 5,
}

@mark_raw
def cmd_booster_pack(self, booster_name: str = ""):
    """Print Booster Contents"""
    if self.ctx.game != "Yu-Gi-Oh! 2006":
        logger.warning("This command can only be used when playing Yu-Gi-Oh! 2006.")
        return
    booster_name = booster_name.upper()
    booster_found = False
    for name in booster_pack_data.keys():
        if name.upper() == booster_name:
            booster_found = True
            booster_name = name
            break
    if not booster_found:
        logger.warning("Pack not found")
        return
    client = self.ctx.client_handler
    assert isinstance(client, YuGiOh2006Client)
    logger.info("Send request for " + booster_name)
    client.print_pack = booster_name


class YuGiOh2006Client(BizHawkClient):
    game = "Yu-Gi-Oh! 2006"
    system = "GBA"
    patch_suffix = ".apygo06"
    local_checked_locations: Set[int]
    goal_flag: int
    rom_slot_name: Optional[str]
    print_pack: str = ""

    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = set()
        self.rom_slot_name = None

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from CommonClient import logger

        try:
            # Check if ROM is some version of Yu-Gi-Oh! 2006
            game_name = ((await bizhawk.read(ctx.bizhawk_ctx, [(0xA0, 11, "ROM")]))[0]).decode("ascii")
            if game_name != "YUGIOHWCT06":
                return False

            # Check if we can read the slot name. Doing this here instead of set_auth as a protection against
            # validating a ROM where there's no slot name to read.
            try:
                slot_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(0x30, 32, "ROM")]))[0]
                self.rom_slot_name = bytes([byte for byte in slot_name_bytes if byte != 0]).decode("utf-8")
            except UnicodeDecodeError:
                logger.info("Could not read slot name from ROM. Are you sure this ROM matches this client version?")
                return False
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False  # Should verify on the next pass

        ctx.game = self.game
        ctx.items_handling = 0b001
        ctx.want_slot_data = False
        if "boosterpack" not in ctx.command_processor.commands:
            ctx.command_processor.commands["boosterpack"] = cmd_booster_pack
        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        ctx.auth = self.rom_slot_name

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        try:
            read_state = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    (0x0, 8, "EWRAM"),
                    (0x52E8, 32, "EWRAM"),
                    (0x5308, 32, "EWRAM"),
                    (0x5325, 1, "EWRAM"),
                    (0x6C38, 4, "EWRAM"),
                ],
            )
            game_state = read_state[0].decode("utf-8")
            locations = read_state[1]
            items = read_state[2]
            amount_items = int.from_bytes(read_state[3], "little")
            money = int.from_bytes(read_state[4], "little")

            # make sure save was created
            if game_state != "YWCT2006":
                return
            local_items = bytearray(items)
            await bizhawk.guarded_write(
                ctx.bizhawk_ctx,
                [(0x5308, parse_items(bytearray(items), ctx.items_received), "EWRAM")],
                [(0x5308, local_items, "EWRAM")],
            )
            money_received = 0
            for item in ctx.items_received:
                if item.item == item_to_index["5000DP"] + 5730000:
                    money_received += 1
            if money_received > amount_items:
                await bizhawk.guarded_write(
                    ctx.bizhawk_ctx,
                    [
                        (0x6C38, (money + (money_received - amount_items) * 5000).to_bytes(4, "little"), "EWRAM"),
                        (0x5325, money_received.to_bytes(2, "little"), "EWRAM"),
                    ],
                    [
                        (0x6C38, money.to_bytes(4, "little"), "EWRAM"),
                        (0x5325, amount_items.to_bytes(2, "little"), "EWRAM"),
                    ],
                )

            locs_to_send = set()

            # Check for set location flags.
            for byte_i, byte in enumerate(bytearray(locations)):
                for i in range(8):
                    and_value = 1 << i
                    if byte & and_value != 0:
                        flag_id = byte_i * 8 + i

                        location_id = flag_id + 5730001
                        if location_id in ctx.server_locations:
                            locs_to_send.add(location_id)

            # Send locations if there are any to send.
            if locs_to_send != self.local_checked_locations:
                self.local_checked_locations = locs_to_send

                if locs_to_send is not None:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": list(locs_to_send)}])

            # Set collected Challenges to complete
            for location in ctx.checked_locations:
                if location not in ctx.locations_checked:
                    cid = location - 5730038
                    old_score = await bizhawk.read(
                        ctx.bizhawk_ctx, [
                            (cid * 4 + 0x6CC8, 1, "EWRAM")]
                    )
                    # set last 2 bits to 01
                    old_score = old_score[0][0]
                    new_score = old_score & 252 | 1
                    await bizhawk.guarded_write(
                        ctx.bizhawk_ctx,[
                            (cid * 4 + 0x6CC8, new_score.to_bytes(1, "little"), "EWRAM"),
                        ],
                        [
                            (cid * 4 + 0x6CC8, old_score.to_bytes(1, "little"), "EWRAM"),
                        ]
                    )

            # Send game clear if the fifth tier 5 campaign opponent was beaten.
            if not ctx.finished_game and locations[18] & (1 << 5) != 0:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

            # print booster contents
            if self.print_pack != "":
                logger.info("Printing Pack: " + self.print_pack)
                for pack in booster_pack_data.keys():
                    self.print_pack = pack
                    pack_data = booster_pack_data[self.print_pack]
                    pointer = pack_data.pointer
                    raw_data = await bizhawk.read(
                        ctx.bizhawk_ctx, [
                            (pointer, pack_data.cards_in_set * 4, "ROM")]
                    )
                    raw_data = raw_data[0]
                    logger.info("   \"" + self.print_pack + "\": {")
                    cards: List[Booster_Card] = []
                    for i in range(0, pack_data.cards_in_set):
                        cid = int.from_bytes(raw_data[i * 4: i * 4 + 2], "little")
                        if cid in booster_card_id_to_name.keys():
                            name = booster_card_id_to_name[cid]
                        else:
                            name = str(hex(cid))
                        rarity = rarities[int.from_bytes(raw_data[i * 4 + 2: i * 4 + 4], "little")]
                        cards.append(Booster_Card(i , name, rarity))

                    for card in sorted(cards, key=lambda card: (rarity_sort_order[card.rarity], card.name)):
                        logger.info("       \"" + card.name +
                                        "\": \"" + card.rarity + "\",")

                    logger.info("   },")
                self.print_pack = ""

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect.
            pass


# Parses bit-map for local items and adds the received items to that bit-map
def parse_items(local_items: bytearray, items: List[NetworkItem]) -> bytearray:
    array = local_items
    for item in items:
        index = item.item - 5730001
        if index != 254:
            byte = math.floor(index / 8)
            bit = index % 8
            array[byte] = array[byte] | (1 << bit)
    return array

