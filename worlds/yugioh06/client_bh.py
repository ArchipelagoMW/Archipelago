import logging
import math
from typing import TYPE_CHECKING, List, Optional, Set, Dict

import Utils
from MultiServer import mark_raw
from NetUtils import ClientStatus, NetworkItem

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from . import item_to_index, cards, collection_id_to_name
from .boosterpack_contents import BoosterCard
from .boosterpacks_data import booster_pack_data, booster_card_id_to_name, rarities

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

logger = logging.getLogger("Client")

rarity_sort_order = {
    "Secret Rare Alt 1": 0,
    "Secret Rare Alt 2": 1,
    "Secret Rare Alt 3": 2,
    "Secret Rare": 3,
    "Ultra Rare Alt 1": 4,
    "Ultra Rare Alt 2": 5,
    "Ultra Rare Alt 3": 6,
    "Ultra Rare": 7,
    "Super Rare Alt 1": 8,
    "Super Rare ALt 2": 9,
    "Super Rare Alt 3": 10,
    "Super Rare": 11,
    "Rare Alt 1": 12,
    "Rare Alt 2": 13,
    "Rare Alt 3": 14,
    "Rare": 15,
    "Common Alt 1": 16,
    "Common Alt 2": 17,
    "Common Alt 3": 18,
    "Common": 19,
}

@mark_raw
def cmd_booster_pack(self, booster_name: str = ""):
    """Print Booster Contents"""
    if self.ctx.game != "Yu-Gi-Oh! 2006":
        logger.warning("This command can only be used when playing Yu-Gi-Oh! 2006.")
        return
    found_name, usable, response = Utils.get_intended_text(booster_name, booster_pack_data.keys())
    if usable:
        booster_name = found_name
    else:
        self.output(response)
        return
    client = self.ctx.client_handler
    assert isinstance(client, YuGiOh2006Client)
    logger.info("Send request for " + booster_name)
    client.print_pack = booster_name


@mark_raw
def cmd_search_card(self, card_name: str = ""):
    """What packs can this card be found in"""
    if self.ctx.game != "Yu-Gi-Oh! 2006":
        logger.warning("This command can only be used when playing Yu-Gi-Oh! 2006.")
        return
    found_name, usable, response = Utils.get_intended_text(card_name, cards.keys())
    if usable:
        card_name = found_name
    else:
        self.output(response)
        return
    client = self.ctx.client_handler
    assert isinstance(client, YuGiOh2006Client)
    logger.info("Send request for " + card_name)
    client.card_search = card_name


class YuGiOh2006Client(BizHawkClient):
    game = "Yu-Gi-Oh! 2006"
    system = "GBA"
    patch_suffix = ".apygo06"
    local_checked_locations: Set[int]
    goal_flag: int
    rom_slot_name: Optional[str]
    print_pack: str = ""
    card_search: str = ""
    all_progression_cards: List[int] = []
    progression_in_booster: List[int] = []
    collection_state: Dict[int, int] = {}
    collection_changed = False

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
        ctx.want_slot_data = True
        if "boosterpack" not in ctx.command_processor.commands:
            ctx.command_processor.commands["boosterpack"] = cmd_booster_pack
        if "search_card" not in ctx.command_processor.commands:
            ctx.command_processor.commands["search_card"] = cmd_search_card
        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        ctx.auth = self.rom_slot_name

    def on_package(self, ctx, cmd, args):
        if cmd == 'Connected':
            if 'all_progression_cards' in args['slot_data'] and args['slot_data']['all_progression_cards']:
                self.all_progression_cards = args['slot_data']['all_progression_cards']
            if 'progression_cards_in_booster' in args['slot_data'] and args['slot_data']['progression_cards_in_booster']:
                self.progression_in_booster = args['slot_data']['progression_cards_in_booster']
        super().on_package(ctx, cmd, args)

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
                    (0x8, 0x1042, "EWRAM")
                ],
            )
            game_state = read_state[0].decode("utf-8")
            locations = read_state[1]
            items = read_state[2]
            amount_items = int.from_bytes(read_state[3], "little")
            money = int.from_bytes(read_state[4], "little")
            collection = read_state[5]

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
                if location not in self.local_checked_locations and 5730037 < location < 5730129:
                    cid = location - 5730038
                    old_score = await bizhawk.read(
                        ctx.bizhawk_ctx, [
                            (cid * 4 + 0x6CC8, 1, "EWRAM")]
                    )
                    # set last 2 bits to 01
                    old_score = old_score[0][0]
                    new_score = old_score & 252 | 1
                    await bizhawk.guarded_write(
                        ctx.bizhawk_ctx, [
                            (cid * 4 + 0x6CC8, new_score.to_bytes(1, "little"), "EWRAM"),
                        ],
                        [
                            (cid * 4 + 0x6CC8, old_score.to_bytes(1, "little"), "EWRAM"),
                        ]
                    )

            # Send game clear if the fifth tier 5 campaign opponent was beaten.
            if not ctx.finished_game and locations[18] & (1 << 5) != 0:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

            # prepare collection tracking
            for card_id in self.progression_in_booster:
                amount = collection[(card_id - 1) * 2] & 0xF
                if amount > 0 and (card_id not in self.collection_state or not self.collection_state[card_id]):
                    self.collection_state[card_id] = amount
                    self.collection_changed = True

            # send collection tracking
            if self.collection_changed:
                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": f"ygo06_collection_{ctx.team}_{ctx.slot}",
                    "default": {},
                    "want_reply": False,
                    "operations": [{"operation": "update", "value": self.collection_state}],
                }])
                self.collection_changed = False

            # print booster contents command
            if self.print_pack != "":
                logger.info("Printing Pack: " + self.print_pack)
                pack_data = booster_pack_data[self.print_pack]
                pointer = pack_data.pointer
                # two separate bizhawk read cause I got buggy results otherwise
                raw_data = await bizhawk.read(
                    ctx.bizhawk_ctx, [
                        (pointer, pack_data.cards_in_set * 4, "ROM")
                    ]
                )
                boosterpack_data = raw_data[0]
                raw_data = await bizhawk.read(
                    ctx.bizhawk_ctx, [
                        (0x8, 0x1042, "EWRAM")
                    ]
                )
                collection_data = raw_data[0]
                booster_cards: List[BoosterCard] = []
                for i in range(0, pack_data.cards_in_set):
                    cid = int.from_bytes(boosterpack_data[i * 4: i * 4 + 2], "little")
                    if cid in booster_card_id_to_name.keys():
                        name = booster_card_id_to_name[cid]
                    else:
                        name = str(hex(cid))
                    rarity = rarities[int.from_bytes(boosterpack_data[i * 4 + 2: i * 4 + 4], "little")]
                    if rarity.endswith(" Alt 1"):
                        name += " Alt 1"
                    elif rarity.endswith(" Alt 2"):
                        name += " Alt 2"
                    elif rarity.endswith(" Alt 3"):
                        name += " Alt 3"

                    if name in cards:
                        card_id = cards[name].id
                    else:
                        card_id = 0
                        name = "ERROR: " + name
                    amount = collection_data[(card_id - 1) * 2] & 0xF
                    if card_id in self.all_progression_cards:
                        color = "blue"
                    elif name.startswith("ERROR"):
                        color = "red"
                    else:
                        color = "white"
                    booster_cards.append(BoosterCard(i, name, rarity, amount, color))
                for card in sorted(booster_cards, key=lambda card: (rarity_sort_order[card.rarity], card.name)):
                    ctx.ui.print_json([{"text": f"{card.amount}x {card.name}: {card.rarity}",
                                        "type": "color", "color": card.color}])
                self.print_pack = ""

            # cards search command
            if self.card_search:
                logger.info("Searching for Card: " + self.card_search)
                card_data = cards[self.card_search]
                found_in_pack: List[str] = []
                for name, booster in booster_pack_data.items():
                    pointer = booster.pointer
                    raw_data = await bizhawk.read(
                        ctx.bizhawk_ctx, [
                            (pointer, booster.cards_in_set * 4, "ROM")
                        ]
                    )
                    boosterpack_data = raw_data[0]
                    for i in range(0, booster.cards_in_set):
                        cid = int.from_bytes(boosterpack_data[i * 4: i * 4 + 2], "little")
                        rarity = rarities[int.from_bytes(boosterpack_data[i * 4 + 2: i * 4 + 4], "little")]
                        artwork = 0
                        if rarity.endswith(" Alt 1"):
                            artwork = 1
                        elif rarity.endswith(" Alt 2"):
                            artwork = 2
                        elif rarity.endswith(" Alt 3"):
                            artwork = 3
                        if cid == card_data.starter_id and artwork == card_data.art:
                            found_in_pack.append(f"{name}: {rarity}")
                if len(found_in_pack) > 0:
                    logger.info("Can be found in:")
                    for found_pack in found_in_pack:
                        logger.info(found_pack)
                    raw_data = await bizhawk.read(
                        ctx.bizhawk_ctx, [
                            (0x8, 0x1042, "EWRAM")
                        ]
                    )
                    collection_data = raw_data[0]
                    amount = collection_data[(card_data.id - 1) * 2] & 0xF
                    logger.info(f"You have {amount} copies of this card")
                else:
                    logger.info("Cannot be found in any pack")
                self.card_search = ""
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
