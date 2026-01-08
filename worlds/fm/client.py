import typing

from typing import TYPE_CHECKING
from random import Random
from NetUtils import ClientStatus
from collections import Counter
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from .utils import Constants
from .duelists import (Duelist, map_ids_to_duelists, ids_to_duelists, UNLOCK_OFFSET,
                       LATEGAME_DUELIST_UNLOCK_OFFSET)
from .items import starchip_item_ids_to_starchip_values, is_card_item, convert_item_id_to_card_id
from .locations import get_location_id_for_duelist, get_location_id_for_card_id
from .logic import get_unlocked_duelists
from .version import __version__

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
    from NetUtils import JSONMessagePart

CARDS_IN_CHESTS_OFFSET: typing.Final[int] = 0x1D0250
MAIN_RAM: typing.Final[str] = "MainRAM"
STARCHIPS_AWARDED_COMANDEERED_BYTE_OFFSET: typing.Final[int] = LATEGAME_DUELIST_UNLOCK_OFFSET + 0x04
LAST_ITEM_AWARDED_INDEX_BYTE_OFFSET: typing.Final[int] = STARCHIPS_AWARDED_COMANDEERED_BYTE_OFFSET + 0x04
# There are 7*4 more unused bytes in this area for more values
STARCHIP_RAM_OFFSET: typing.Final[int] = 0x1D07E0
MAGIC_DUEL_BYTE_OFFSET: typing.Final[int] = 0x09B238
"""This byte is FF during an active, ready duel (all duel-specific memory values are set), 01 after a loss"""
AI_LIFE_POINTS_SHORT_OFFSET: typing.Final[int] = 0x0EA024
PLAYER_LIFE_POINTS_SHORT_OFFSET: typing.Final[int] = 0x0EA004
AI_DUELIST_ID_OFFSET: typing.Final[int] = 0x09B361

SILLY_DEATH_STRINGS: typing.Tuple[str, ...] = (
    "{o} NEEDED precisely those two cards to win against {p}.",
    "{p}'s deck couldn't win against a deck like {o}'s.",
    "{o} topdecked the only card that could beat {p}."
    "{o} had the perfect cards against {p}.",
    "There was nothing {p} could do against {o}.",
    "{p} played that perfectly against {o} and still lost.",
    "{o}'s deck had no pathetic cards against {p}.",
    "{p}'s time to d-d-d-d-d-d-d-duel is over against {o}."
)


def get_wins_and_losses_from_bytes(b: bytes) -> typing.Tuple[int, int]:
    """Wins is the first value; losses is the second."""
    return int.from_bytes(b[:2], "little"), int.from_bytes(b[2:], "little")


class FMClient(BizHawkClient):
    game: str = Constants.GAME_NAME
    system: str = "PSX"
    patch_suffix: str = ".apfm"
    local_checked_locations: typing.Set[int]
    duelist_unlock_order: typing.Tuple[typing.Tuple[Duelist, ...], ...]
    final_6_order: typing.Tuple[Duelist, ...]
    local_last_deathlink: float
    awaiting_deathlink_death: bool
    checked_version_string: bool
    random: Random

    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = set()
        self.local_last_deathlink = float("-inf")
        self.awaiting_deathlink_death = False
        self.checked_version_string = False

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        # Forbidden Memories has a very active romhacking community. Although not all mods will be compatible with AP
        # since AP assumes specific card distributions (card drop tables), I see no reason to limit players to only a
        # small subset of mods when all the revelant memory addresses for the AP interface don't change. We could even
        # support modded drop tables in the future.
        #
        # I searched for a means to validate the ROM in a mod-agnostic way. PSX discs contain filesystems; some mods
        # extract the files, modify the relevant parts, then rebuild the ISO (FM card mod does this process). This can
        # cause files to move around inside the binary so offsets for strings may not be reliable. Some mods also update
        # the game's checksum so that they run on real consoles.
        #
        # I've found that the most reliable way is to search the RAM instead of the ROM. When the BIOS boots up, as soon
        # as the PlayStation "P" logo appears, a certain section of memory is initialized with the game's NTSC
        # identifier: BASLUS-01411-YUGIOH. This stays in memory at least through the game's main menu (as deep as I
        # checked) and probably for as long as the game is running. Most mods base themselves on the NTSC release, and
        # the speedrunning community uses it as well since it's faster than PAL and JP, although I'd like to validate
        # the others releases if there's demand to play them.
        fm_identifier_ram_address: int = 0x10384

        # = BASLUS-01411-YUGIOH in ASCII
        bytes_expected: bytes = bytes.fromhex("4241534C55532D30313431312D595547494F4800")
        try:
            bytes_actual: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                fm_identifier_ram_address, len(bytes_expected), MAIN_RAM
            )]))[0]
            if bytes_actual != bytes_expected:
                return False
        except Exception:
            return False

        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125  # value taken from Pokemon Emerald's client
        self.random = Random()  # used for silly random deathlink messages
        from CommonClient import logger
        logger.info(f"Forbidden Memories Client v{__version__}. For updates:")
        logger.info("https://github.com/sg4e/Archipelago/releases/latest")
        return True

    async def kill_player(self, ctx: "BizHawkClientContext") -> bool:
        """Return True if this method thinks it actually killed the player, False otherwise"""
        # # Check that the magic duel byte is FF and opponent's LP is not 0
        # magic_byte, ai_lp_bytes = await bizhawk.read(ctx.bizhawk_ctx, [
        #     (MAGIC_DUEL_BYTE_OFFSET, 1, MAIN_RAM),
        #     (AI_LIFE_POINTS_SHORT_OFFSET, 2, MAIN_RAM)
        # ])
        # ai_lp: int = int.from_bytes(ai_lp_bytes, "little")
        # if magic_byte == b"\xFF" and ai_lp > 0:
        #     # Player is in a duel and eligible to be killed (probably)
        #     await bizhawk.write
        return await bizhawk.guarded_write(
            ctx.bizhawk_ctx,
            [(PLAYER_LIFE_POINTS_SHORT_OFFSET, (0).to_bytes(2, "little"), MAIN_RAM)],
            [(MAGIC_DUEL_BYTE_OFFSET, (0xFF).to_bytes(1, "little"), MAIN_RAM)]
        )

    async def is_player_dead(self, ctx: "BizHawkClientContext") -> bool:
        "Checks if player is dead and resets the RAM death info byte"
        return await bizhawk.guarded_write(
            ctx.bizhawk_ctx,
            [(MAGIC_DUEL_BYTE_OFFSET, (0x00).to_bytes(1, "little"), MAIN_RAM)],  # write
            [(MAGIC_DUEL_BYTE_OFFSET, (0x01).to_bytes(1, "little"), MAIN_RAM)]   # read
        )

    async def read_chest_memory(self, ctx: "BizHawkClientContext") -> bytes:
        return (await bizhawk.read(
            ctx.bizhawk_ctx, [(CARDS_IN_CHESTS_OFFSET, 722, MAIN_RAM)]
        ))[0]

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        # Example of the chest RAM (raw, set Bizhawk memory viewer to big-endian):
        # 0x00000000 0x00000000 0x02000000 0x00000001
        # 2 Shadow Specters (card ID: 9) in the chest and 1 Time Wizard (card ID: 16)
        # Cards in chest DO NOT include what's in the deck
        # Chest memory is updated after the player leaves the Build Deck screen

        if not ctx.finished_game and any(item.item == Constants.VICTORY_ITEM_ID for item in ctx.items_received):
            await ctx.send_msgs([{
                "cmd": "StatusUpdate",
                "status": ClientStatus.CLIENT_GOAL
            }])
            ctx.finished_game = True
        # Pokemon Emerald checks the slot data here
        # Can this be evaluated only once?
        if ctx.slot_data is not None:
            if not self.checked_version_string:
                self.checked_version_string = True
                generated_version: str = (ctx.slot_data[Constants.GENERATED_WITH_KEY] if Constants.GENERATED_WITH_KEY
                                          in ctx.slot_data else "undefined")
                if __version__ != generated_version:
                    parts: typing.List[JSONMessagePart] = []
                    from NetUtils import add_json_text
                    add_json_text(parts, "WARNING:", type="color", color="red")
                    add_json_text(parts, " generator/client apworld mismatch.")
                    ctx.on_print_json({"data": parts})
                    from CommonClient import logger
                    logger.warning(
                        "The multiworld was generated with a different "
                        "version of the apworld file. Please install the same apworld version for "
                        "maximum compatibility."
                    )
                    logger.warning(f"Multiworld generated with apworld: {generated_version}")
                    logger.warning(f"Installed apworld: {__version__}")
            self.duelist_unlock_order = map_ids_to_duelists(
                ctx.slot_data[Constants.DUELIST_UNLOCK_ORDER_KEY]
            )
            self.final_6_order = tuple(
                ids_to_duelists[id] for id in ctx.slot_data[Constants.FINAL_6_ORDER_KEY]
            )
            if ctx.slot_data[Constants.DEATHLINK_OPTION_KEY]:
                await ctx.update_death_link(True)

            try:
                # Deathlink
                if "DeathLink" in ctx.tags:
                    if ctx.last_death_link > self.local_last_deathlink:
                        # Someone died on the link
                        self.local_last_deathlink = ctx.last_death_link
                        self.awaiting_deathlink_death = await self.kill_player(ctx)
                    if await self.is_player_dead(ctx):
                        if not self.awaiting_deathlink_death:
                            username: str = "the Pharaoh"
                            try:
                                username = ctx.player_names[typing.cast(int, ctx.slot)]
                            except KeyError:
                                pass
                            opponent_name: str = "the opposing duelist"
                            try:
                                duelist_id: int = int.from_bytes((await bizhawk.read(
                                    ctx.bizhawk_ctx, [(AI_DUELIST_ID_OFFSET, 1, MAIN_RAM)]
                                ))[0], "little")
                                opponent_name = str(ids_to_duelists[duelist_id])
                            except Exception:
                                pass
                            death_str: str = self.random.choice(SILLY_DEATH_STRINGS).format(o=opponent_name, p=username)
                            death_str = death_str[0].upper() + death_str[1:]
                            await ctx.send_death(death_text=death_str)
                        self.awaiting_deathlink_death = False
                if self.duelist_unlock_order is not None and self.final_6_order is not None:
                    # Unlock duelists for Progressive Duelist item count
                    progressive_duelist_item_count: int = sum(
                        1 for item in ctx.items_received if item.item == Constants.PROGRESSIVE_DUELIST_ITEM_ID
                    )
                    unlocked_duelists: typing.List[Duelist] = get_unlocked_duelists(
                        progressive_duelist_item_count,
                        self.duelist_unlock_order,
                        self.final_6_order,
                    )
                    first_bit_field: int = 0
                    second_bit_field: int = 0
                    for duelist in unlocked_duelists:
                        if not duelist.is_5th_byte:
                            first_bit_field |= duelist.bitflag
                        else:
                            second_bit_field |= duelist.bitflag
                    if Duelist.HEISHIN_2ND in unlocked_duelists:
                        first_bit_field |= Duelist.HEISHIN.bitflag
                    await bizhawk.write(ctx.bizhawk_ctx, [(
                        UNLOCK_OFFSET,
                        first_bit_field.to_bytes(4, "little") + second_bit_field.to_bytes(1, "little"),
                        MAIN_RAM
                    )])
                # Read number of wins and losses over each duelist for "Duelist defeated" locations
                all_duelists: typing.List[Duelist] = [d for d in Duelist]
                read_list: typing.List[typing.Tuple[int, int, str]] = [
                    (d.wins_address, 4, MAIN_RAM) for d in all_duelists
                ]
                wins_bytes: typing.List[bytes] = await bizhawk.read(ctx.bizhawk_ctx, read_list)
                duelists_to_wins: typing.Dict[Duelist, int] = {
                    d: get_wins_and_losses_from_bytes(w)[0] for d, w in zip(all_duelists, wins_bytes)
                }
                new_local_checked_locations: typing.Set[int] = set([
                    get_location_id_for_duelist(key) for key, value in duelists_to_wins.items() if value != 0
                ])
                chest_memory: bytes = await self.read_chest_memory(ctx)
                owned_ids: set[int] = set(
                    [get_location_id_for_card_id(i+1) for i in range(722) if chest_memory[i] != 0]
                )
                new_local_checked_locations |= owned_ids

                if new_local_checked_locations != self.local_checked_locations:
                    self.local_checked_locations = new_local_checked_locations
                    if new_local_checked_locations is not None:
                        await ctx.send_msgs([{
                            "cmd": "LocationChecks",
                            "locations": list(new_local_checked_locations)
                        }])

                # Starchip handling
                starchips_awarded_bytes: bytes = (await bizhawk.read(
                    ctx.bizhawk_ctx, [(STARCHIPS_AWARDED_COMANDEERED_BYTE_OFFSET, 4, MAIN_RAM)]
                ))[0]
                # In the spirit of the PlayStation, we encode the integer in little-endian
                starchips_awarded: int = int.from_bytes(starchips_awarded_bytes, "little")
                starchips_on_server: int = sum(
                    starchip_item_ids_to_starchip_values[item.item] for item in ctx.items_received
                    if item.item in starchip_item_ids_to_starchip_values
                )
                if starchips_on_server > starchips_awarded:
                    amount_to_award: int = starchips_on_server - starchips_awarded
                    starchip_ram_bytes: bytes = (
                        await bizhawk.read(ctx.bizhawk_ctx, [(STARCHIP_RAM_OFFSET, 4, MAIN_RAM)])
                    )[0]
                    starchips_in_ram: int = int.from_bytes(starchip_ram_bytes, "little")
                    new_starchip_count: int = starchips_in_ram + amount_to_award
                    new_starchip_bytes: bytes = new_starchip_count.to_bytes(4, "little")
                    new_total_awarded: bytes = starchips_on_server.to_bytes(4, "little")
                    # Use guarded write to avoid the race condition where the player spends their starchips
                    # or acquires more starchips before the adjusted amount is awarded
                    await bizhawk.guarded_write(ctx.bizhawk_ctx, [
                        (STARCHIP_RAM_OFFSET, new_starchip_bytes, MAIN_RAM),  # new value
                        (STARCHIPS_AWARDED_COMANDEERED_BYTE_OFFSET, new_total_awarded, MAIN_RAM)
                    ], [
                        (STARCHIP_RAM_OFFSET, starchip_ram_bytes, MAIN_RAM)  # guarded value
                    ])
                # Granting cards into memory
                last_awarded_item_index: int = int.from_bytes(
                    (await bizhawk.read(ctx.bizhawk_ctx, [(LAST_ITEM_AWARDED_INDEX_BYTE_OFFSET, 4, MAIN_RAM)]))[0],
                    "little"
                )
                item_count: int = len(ctx.items_received)
                if last_awarded_item_index < item_count:
                    from CommonClient import logger
                    logger.debug("Item count exceeds previous index: %s > %s", item_count, last_awarded_item_index)
                    new_item_ids: typing.List[int] = [
                        item.item for item in ctx.items_received[last_awarded_item_index:]
                    ]
                    logger.debug("New item ids: %s", new_item_ids)
                    new_card_item_ids: typing.List[int] = [id for id in new_item_ids if is_card_item(id)]
                    if new_card_item_ids:
                        logger.debug("Granting cards")
                        card_ids: typing.List[int] = [convert_item_id_to_card_id(i) for i in new_card_item_ids]
                        from .cards import id_to_card
                        for id in card_ids:
                            card_name: str = id_to_card[id].name if id in id_to_card else "Not a valid card id"
                            logger.debug("New card: %s = %s", id, card_name)
                        new_card_counter = Counter(card_ids)
                        logger.debug("Totals: %s", new_card_counter)
                        chest_memory = await self.read_chest_memory(ctx)
                        logger.debug("Chest memory: %s", chest_memory)
                        writes: typing.List[typing.Tuple[int, typing.Iterable[int], str]] = [(
                            CARDS_IN_CHESTS_OFFSET + card_id - 1,
                            (chest_memory[card_id-1] + new_count).to_bytes(1, "little"),
                            MAIN_RAM
                        ) for card_id, new_count in new_card_counter.items()]
                        logger.debug("Impending writes: %s", writes)
                        # Technically there's a race condition if they win the new card at the same time,
                        # but why bother since they get the card anyway
                        await bizhawk.write(ctx.bizhawk_ctx, writes)
                        logger.debug("Finished writes")
                    await bizhawk.write(ctx.bizhawk_ctx, [(
                        LAST_ITEM_AWARDED_INDEX_BYTE_OFFSET,
                        item_count.to_bytes(4, "little"),
                        MAIN_RAM
                    )])
            except bizhawk.RequestFailedError:
                pass
