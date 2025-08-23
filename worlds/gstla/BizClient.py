from __future__ import annotations

import base64
from collections import defaultdict
import logging
from enum import IntEnum, Enum
from typing import Dict, List, TYPE_CHECKING, Set, Tuple, Mapping, Optional, Any

from BaseClasses import ItemClassification
from NetUtils import ClientStatus, NetworkItem
from worlds._bizhawk.client import BizHawkClient
from worlds._bizhawk import read, write, guarded_write, display_message
from . import items_by_id, ItemType, remote_blacklist
from .gen.LocationNames import loc_names_by_id, LocationName, option_name_to_goal_name
from .gen.ItemData import djinn_items, mimics, ItemData, events
from .gen.LocationData import all_locations, LocationType, djinn_locations, LocationData, location_name_to_data, \
    event_name_to_data, location_id_to_data, event_id_to_name

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext, BizHawkClientCommandProcessor

logger = logging.getLogger("Client")

FLAG_START = 0x40
FORCE_ENCOUNTER_ADDR = 0x30164
PREVENT_FLEEING_ADDR = 0x48B
IN_BATTLE_ADDR = 0x60

class _MemDomain(str, Enum):
    EWRAM = 'EWRAM'
    ROM = 'ROM'

class _DataLocations(IntEnum):
    IN_GAME = (0x428, 0x2, 0x0, _MemDomain.EWRAM)
    DJINN_FLAGS = (FLAG_START + (0x30 >> 3), 0x0A, 0x30, _MemDomain.EWRAM)
    AP_ITEM_SLOT = (0xA96, 0x2, 0x0, _MemDomain.EWRAM)
    # two unused bytes in save data
    AP_ITEMS_RECEIVED = (0xA72, 0x2, 0x0, _MemDomain.EWRAM)
    INITIAL_INVENTORY = (FLAG_START + 0x0, 0x1, 0x0, _MemDomain.EWRAM)
    SUMMONS = (FLAG_START + (0x10 >> 3), 0x2, 0x10, _MemDomain.EWRAM)
    TREASURE_8_FLAGS = (FLAG_START + (0x800 >> 3), 0x20, 0x800, _MemDomain.EWRAM)
    TREASURE_9_FLAGS = (FLAG_START + (0x900 >> 3), 0x20, 0x900, _MemDomain.EWRAM)
    TREASURE_A_FLAGS = (FLAG_START + (0xA00 >> 3), 0x20, 0xA00, _MemDomain.EWRAM)
    TREASURE_B_FLAGS = (FLAG_START + (0xB00 >> 3), 0x20, 0xB00, _MemDomain.EWRAM)
    TREASURE_C_FLAGS = (FLAG_START + (0xC00 >> 3), 0x20, 0xC00, _MemDomain.EWRAM)
    TREASURE_D_FLAGS = (FLAG_START + (0xD00 >> 3), 0x20, 0xD00, _MemDomain.EWRAM)
    TREASURE_E_FLAGS = (FLAG_START + (0xE00 >> 3), 0x20, 0xE00, _MemDomain.EWRAM)
    TREASURE_F_FLAGS = (FLAG_START + (0xF00 >> 3), 0x20, 0xF00, _MemDomain.EWRAM)
    ENEMY_FLAGS = (FLAG_START + (0x600 >> 3), 0x40, 0x600, _MemDomain.EWRAM)
    STORY_FLAGS = (FLAG_START + (0x800 >> 3), 0x40, 0x800, _MemDomain.EWRAM)
    # DOOM_DRAGON = (FLAG_START + (0x778 >> 3), 0x1, 0x778, _MemDomain.EWRAM)

    def __new__(cls, addr: int, length: int, initial_flag: int, domain: _MemDomain):
        value = len(cls.__members__)
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.addr = addr
        obj.length = length
        obj.initial_flag = initial_flag
        obj.domain = domain
        return obj

    def to_request(self) -> Tuple[int, int, _MemDomain]:
        return self.addr, self.length, self.domain


class GoalManager:

    supported_flags: dict[str, int] = {
        x: event_name_to_data[x].flag for x in [
            LocationName.Kandorean_Temple_Chestbeaters,
            LocationName.Yampi_Desert_King_Scorpion,
            LocationName.Alhafra_Briggs,
            LocationName.Lemurian_Ship_Aqua_Hydra,
            LocationName.Sea_of_Time_Poseidon,
            LocationName.Gaia_Rock_Serpent,
            LocationName.Champa_Avimander,
            LocationName.Shaman_Village_Moapa,
            LocationName.Contigo_Reunion,
            LocationName.Mars_Lighthouse_Flame_Dragons,
            LocationName.Mars_Lighthouse_Doom_Dragon,
            LocationName.Treasure_Isle_Star_Magician,
            LocationName.Islet_Cave_Sentinel,
            LocationName.Yampi_Desert_Cave_Valukar,
            LocationName.Anemos_Inner_Sanctum_Dullahan,
        ]
    }
    flag_to_name: dict[int, str] = {
        v: k for k,v in supported_flags.items()
    }

    def __init__(self):
        self.flag_requirements: Set[str] = set()
        self.count_requirements: dict[str, int] = dict()
        self.desired_flags: dict[int, int] = dict()
        self.current: defaultdict[str, defaultdict[str, bool]] = defaultdict(lambda: defaultdict(lambda: False))
        self.initialized = False

    def init_reqs_from_slotdata(self, slot_data: dict[str, Any]) -> None:
        reqs: dict[str, Any] = slot_data['goal']
        if reqs is None:
            reqs = dict()

        if 'flags' in reqs:
            self.flag_requirements: Set[str] = reqs['flags']
        if 'counts' in reqs:
            self.count_requirements: dict[str, int] = reqs['counts']

        if len(self.flag_requirements) == 0 and len(self.count_requirements) == 0:
            self.flag_requirements.add("Doom Dragon")

        for key in self.flag_requirements:
            location_name = option_name_to_goal_name[key]
            enemy_flag = GoalManager.supported_flags[location_name]
            location_data = event_name_to_data[location_name]
            self.desired_flags[enemy_flag] = location_data.ap_id
        # logger.info(f"Desired flags: {self.desired_flags}")
        # logger.info(f"Desired counts: {self.count_requirements}")


    async def check_goals(self, client: 'GSTLAClient', ctx: 'BizHawkClientContext') -> None:
        server_flags: Optional[List[int]] = ctx.stored_data.get(client.get_goal_flags_key(ctx), None)
        if server_flags is None:
            server_flags = []
        updated_flags: Set[int] = set()
        for flag, is_set in client.goal_map.items():
            ap_id = self.desired_flags.get(flag, None)
            if ap_id is not None:
                if is_set and ap_id not in server_flags:
                    await display_message(ctx.bizhawk_ctx, GoalManager.flag_to_name.get(flag, "Unknown") + " Completed")
                    updated_flags.add(ap_id)

        server_djinn = ctx.stored_data.get(client.get_djinn_location_key(ctx), [])
        if server_djinn is None:
            server_djinn: List[int] = []

        # Always compute difference for pop tracker
        difference = client.checked_djinn.difference(server_djinn)

        if difference:
            await display_message(ctx.bizhawk_ctx,
                                  f"Number of Djinn Obtained: {len(client.checked_djinn)}" +
                                  ("" if 'djinn' not in client.goals.count_requirements else "/" + str(client.goals.count_requirements.get("djinn",0))))

        if updated_flags or difference:
            # logger.info(f"Flags updated: {updated_flags}")
            # logger.info(f"Difference: {difference}")
            await client.update_goal_flags(updated_flags, ctx, include_djinn=len(difference)>0)

    def is_done(self, client: 'GSTLAClient', ctx: 'BizHawkClientContext'):
        if not self.initialized:
            return
        goal_flags: List[int] = ctx.stored_data.get(client.get_goal_flags_key(ctx), [])
        if goal_flags is None:
            goal_flags = []
        # logger.info(f"Goal flags: {goal_flags}")
        for ap_id in self.desired_flags.values():
            if ap_id not in goal_flags:
                return False

        if "djinn" in self.count_requirements:
            required_count = self.count_requirements["djinn"]
            server_count = ctx.stored_data.get(client.get_djinn_location_key(ctx), None)
            if server_count is None:
                server_count = dict()
            if required_count > len(server_count):
                return False

        if "summons" in self.count_requirements:
            required_count = self.count_requirements["summons"]
            server_count = len(client.summons)
            if required_count > server_count:
                return False

        return True


def _handle_common_cmd(self: 'BizHawkClientCommandProcessor') -> Optional[GSTLAClient]:
    from worlds._bizhawk.context import BizHawkClientContext
    if self.ctx.game != "Golden Sun The Lost Age":
        logger.warning("This command can only be used when playing GSTLA")
        return None

    if not self.ctx.server or not self.ctx.slot:
        logger.warning("You must be connected to a server to use this command")
        return None
    ctx = self.ctx
    assert isinstance(ctx, BizHawkClientContext)
    client = ctx.client_handler
    assert isinstance(client, GSTLAClient)
    return client


def cmd_unchecked_djinn(self: 'BizHawkClientCommandProcessor') -> None:
    """Prints djinn locations that have not yet been checked"""
    client = _handle_common_cmd(self)
    if client is None:
        return
    for djinn in djinn_locations:
        djinn_name = loc_names_by_id[djinn.id]
        if djinn.flag not in client.checked_djinn:
            logger.info(djinn_name)


def cmd_checked_djinn(self: 'BizHawkClientCommandProcessor') -> None:
    """Prints djinn locations that have been checked"""
    client = _handle_common_cmd(self)
    if client is None:
        return
    for djinn_id in client.checked_djinn:
        djinn = loc_names_by_id[client.djinn_flag_to_loc_id[djinn_id]]
        logger.info(djinn)

def cmd_print_goals(self: 'BizHawkClientCommandProcessor') -> None:
    """Prints the goals for this seed"""
    client = _handle_common_cmd(self)
    if client is None:
        return
    flags = client.goals.flag_requirements
    if flags:
        logger.info("Must clear the following: ")
        for flag in flags:
            logger.info(flag)
    counters = client.goals.count_requirements
    if counters:
        logger.info("Obtain the following: ")
        for thing, num in counters.items():
            logger.info(f"{thing.capitalize()} count: {num}")

def cmd_print_progress(self: 'BizHawkClientCommandProcessor') -> None:
    """Prints the current progress towards the goal"""
    client = _handle_common_cmd(self)
    if client is None:
        return
    flags: List[int] = self.ctx.stored_data.get(client.get_goal_flags_key(self.ctx))
    if flags is not None and len(flags) != 0:
        logger.info("Objectives Completed: ")
        for ap_id in flags:
            event_name = event_id_to_name[ap_id]
            logger.info(event_name)

    djinn_count: List[int] = self.ctx.stored_data.get(client.get_djinn_location_key(self.ctx))
    if "djinn" in client.goals.count_requirements and djinn_count is not None:
        logger.info(f"Djinn count: {len(djinn_count)}")
        # logger.info("Objectives Not Completed: ")
        # for flag, cleared in flags.items():
        #     if not cleared:
        #         logger.info(flag)
    if "summons" in client.goals.count_requirements:
        logger.info(f"Summon count: {len(client.summons)}")


commands = [
    ("unchecked_djinn", cmd_unchecked_djinn),
    ("djinn", cmd_checked_djinn),
    ("goals", cmd_print_goals),
    ("goals_completed", cmd_print_progress)
]

class GSTLAClient(BizHawkClient):
    game = 'Golden Sun The Lost Age'
    system = 'GBA'
    patch_suffix = '.apgstla'

    def __init__(self):
        super().__init__()
        self.slot_name = ''
        self.flag_map: defaultdict[int, Set[int]] = defaultdict(lambda: set())
        self.event_flag_map: defaultdict[int, Set[int]] = defaultdict(lambda: set())
        self.goal_map: dict[int, bool] = dict()
        self.djinn_ram_to_rom: Dict[int, int] = dict()
        self.djinn_flag_map: Dict[int, str] = dict()
        self.djinn_flag_to_loc_id: Dict[int, int] = {d.flag: d.id for d in djinn_locations}
        self.checked_djinn: Set[int] = set()
        self.possessed_djinn: Set[int] = set()
        self.djinn_last_count: int = 0
        self.mimics = {x.id: x for x in mimics}
        self.summons: Set[int] = set()
        self.summon_item_index: int = 0
        for loc in all_locations:
            if loc.loc_type == LocationType.Event:
                self.event_flag_map[loc.flag].add(loc.ap_id)
                continue
            self.flag_map[loc.flag].add(loc.ap_id)
            if loc.loc_type == LocationType.Djinn:
                self.djinn_flag_map[loc.flag] = loc_names_by_id[loc.addresses[0]]
        self.temp_locs: Set[int] = set()
        self.temp_events: Set[int] = set()
        self.local_events: Set[int] = set()
        self.local_locations: Set[int] = set()
        # self.starting_items: StartingItemHandler = StartingItemHandler(dict())
        self.was_in_game: bool = False
        self.coop: int = 0
        self.remote_blacklist: Set[int] = remote_blacklist
        self.goals = GoalManager()

    async def validate_rom(self, ctx: 'BizHawkClientContext'):
        from worlds._bizhawk.context import TextCategory
        game_name = await read(ctx.bizhawk_ctx, [(0xA0, 0x12, _MemDomain.ROM)])
        game_name = game_name[0].decode('ascii')
        logger.debug("Game loaded: %s", game_name)
        if game_name != 'GOLDEN_SUN_BAGFE01':
            for cmd, _ in commands:
                if cmd in ctx.command_processor.commands:
                    ctx.command_processor.commands.pop(cmd)
            return False
        ctx.game = self.game
        # TODO: would like to verify that the ROM is the correct one somehow
        # Possibly verify the seed; would also be nice to have the slot name encoded
        # in the rom somewhere, though not necessary
        slot_name = await read(ctx.bizhawk_ctx, [(0xFFF000, 64, _MemDomain.ROM)])
        if not slot_name:
            logger.warning("Could not find slot name in GSTLA ROM; please double check the ROM is correct")
        else:
            self.slot_name = base64.b64decode(slot_name[0].rstrip(b'\x00'), validate=True).decode('utf-8').strip()
        for cmd, func in commands:
            if cmd not in ctx.command_processor.commands:
                ctx.command_processor.commands[cmd] = func
        ctx.items_handling = 0b111
        ctx.watcher_timeout = 1  # not sure what a reasonable setting here is; passed to asyncio.wait_for
        ctx.text_passthrough_categories.add(TextCategory.OUTGOING)
        ctx.text_passthrough_categories.add(TextCategory.HINT)
        return True

    async def set_auth(self, ctx: 'BizHawkClientContext') -> None:
        if self.slot_name:
            ctx.auth = self.slot_name

    async def _load_djinn(self, ctx: 'BizHawkClientContext') -> None:
        if len(self.djinn_ram_to_rom) > 0:
            return
        # Don't put this in the data locations class; we don't want to check this regularly
        result = await read(ctx.bizhawk_ctx, [(0xFA0000, 0x2 * 18 * 4, _MemDomain.ROM)])
        for index in range(18 * 4):
            djinn_flag = (index // 18) * 20 + (index % 18) + _DataLocations.DJINN_FLAGS.initial_flag
            section = int.from_bytes(result[0][index * 2:(index * 2) + 2], 'little')
            rom_flag = (section >> 8) * 0x14 + (section & 0xFF) + 0x30
            self.djinn_ram_to_rom[rom_flag] = djinn_flag

    def _is_in_game(self, data: List[bytes]) -> bool:
        # What the emo tracker pack does; seems like it also verifies the player
        # has opened a save file
        flag = int.from_bytes(data[_DataLocations.IN_GAME], 'little')
        return flag > 1

    def get_goal_flags_key(self, ctx: 'BizHawkClientContext') -> str:
        return f"gstla_goal_flags_status_{ctx.slot}_{ctx.team}"

    def get_event_key(self, ctx: 'BizHawkClientContext') -> str:
        return f"gstla_events_status_{ctx.slot}_{ctx.team}"

    def get_djinn_location_key(self, ctx: 'BizHawkClientContext') -> str:
        return f"gstla_goal_djinn_status_{ctx.slot}_{ctx.team}"

    def get_djinn_possessed_key(self, ctx: 'BizHawkClientContext') -> str:
        return f"gstla_djinn_held_{ctx.slot}_{ctx.team}"

    def check_summon_count(self, ctx: "BizHawkClientContext") -> None:
        if self.summon_item_index >= len(ctx.items_received):
            return
        end = len(ctx.items_received)
        for i in range(self.summon_item_index, end):
            item = ctx.items_received[i]
            itemdata = items_by_id[item.item]
            if itemdata.type == ItemType.Summon:
                self.summons.add(itemdata.id)
        self.summon_item_index = end

    def _check_djinn_flags(self, data: List[bytes]) -> None:
        flag_bytes = data[_DataLocations.DJINN_FLAGS]
        for i in range(0, _DataLocations.DJINN_FLAGS.length, 2):
            part = flag_bytes[i:i + 2]
            part_int = int.from_bytes(part, "little")
            # logger.info(part_int)
            for bit in range(16):
                if part_int & 1 > 0:
                    flag = i * 8 + bit
                    original_flag = flag + _DataLocations.DJINN_FLAGS.initial_flag
                    if original_flag not in self.possessed_djinn:
                        self.possessed_djinn.add(original_flag)
                    shuffled_flag = self.djinn_ram_to_rom[original_flag]
                    # original_djinn = self.djinn_flag_map[original_flag]
                    # shuffled_djinn = self.djinn_flag_map[shuffled_flag]
                    # TODO: this may be wrong once djinn are events
                    # logger.debug("RAM Djinn: %s, Flag: %s -> ROM Djinn: %s, Flag: %s",
                    #              original_djinn, hex(original_flag), shuffled_djinn, hex(shuffled_flag))
                    self.checked_djinn.add(shuffled_flag)
                    # TODO: if djinn ever become proper items this code would be needed
                    # locs = self.flag_map.get(shuffled_flag, None)
                    # # logger.debug("orig_flag: %s, shuffle flag: %s, locs: %s", hex(flag), hex(shuffled_flag), locs)
                    # assert locs is not None, "Got null locations for flag: %s" % hex(shuffled_flag)
                    # self.temp_locs |= locs
                part_int >>= 1

    def _check_common_flags(self, data_loc: _DataLocations, data: List[bytes]) -> None:
        flag_bytes = data[data_loc]
        initial_flag = data_loc.initial_flag
        # logger.debug("Checking flags for %s" % data_loc.name)
        itr_step = 0x2 if data_loc.length > 0x1 else 0x1
        for i in range(0, data_loc.length, itr_step):
            part = flag_bytes[i:i + itr_step]
            part_int = int.from_bytes(part, 'little')
            # logger.debug("Data found: %s", hex(part_int))
            # logger.debug("Bytes: %s", part)
            for bit in range(itr_step * 8):
                # logger.debug("int %d", part_int)
                if part_int & 1 > 0:
                    flag = i * 8 + bit + initial_flag
                    locs = self.flag_map.get(flag, None)
                    # logger.debug("flag found: %s, locs: %s", hex(flag), locs)
                    if locs is not None:
                        self.temp_locs |= locs
                    events = self.event_flag_map.get(flag, None)
                    if events is not None:
                        self.temp_events |= events
                    # if 0x600 < flag < 0x800:
                    #     logger.info("flag found: %s", hex(flag))
                    if flag in self.goal_map:
                        self.goal_map[flag] = True
                part_int >>= 1
        # logger.debug(self.temp_locs)

    async def _receive_items(self, ctx: 'BizHawkClientContext', data: List[bytes]) -> None:
        item_in_slot = int.from_bytes(data[_DataLocations.AP_ITEM_SLOT], byteorder="little")
        if item_in_slot != 0:
            logger.debug("AP Item slot has data in it: %d", item_in_slot)
            return
        item_index = int.from_bytes(data[_DataLocations.AP_ITEMS_RECEIVED], 'little')
        cur_amount = len(ctx.items_received)
        if cur_amount <= item_index:
            return
        logger.debug("Items to give: %d, Current Item Index: %d", len(ctx.items_received), item_index)

        index_to_give = -1
        for i in range(item_index, cur_amount):
            item = ctx.items_received[i]
            if self._should_give_to_player(ctx, item):
                index_to_give = i
                break
            else:
                logger.debug(f"Should not give item {item.item} to player")

        if index_to_give == -1:
            logger.debug("None of the current items should be given")
            await write(ctx.bizhawk_ctx, [
                (_DataLocations.AP_ITEMS_RECEIVED.addr,
                 cur_amount.to_bytes(length=2, byteorder="little"),
                 _DataLocations.AP_ITEMS_RECEIVED.domain)
            ])
            return
        elif item_index != index_to_give:
            # Update the item index so as to skip ones we don't care about
            update_index = index_to_give
            await write(ctx.bizhawk_ctx, [
                (_DataLocations.AP_ITEMS_RECEIVED.addr,
                 update_index.to_bytes(length=2, byteorder="little"),
                 _DataLocations.AP_ITEMS_RECEIVED.domain)
            ])

        item = ctx.items_received[index_to_give]

        logger.debug("Writing Item %d to Slot", item.item)
        await write(ctx.bizhawk_ctx, [(_DataLocations.AP_ITEM_SLOT.addr,
                                       item.item.to_bytes(length=2, byteorder="little"),
                                       _DataLocations.AP_ITEM_SLOT.domain)])

    def _should_give_to_player(self, ctx: 'BizHawkClientContext', item: NetworkItem) -> bool:
        logger.debug("item: %s flags: %s location: %s coop: %s", item.item, item.flags, item.location, self.coop)
        if item.item in event_id_to_name:
            return False
        if ctx.slot != item.player:
            return True
        elif self.coop == 0:
            return False
        elif item.location in self.remote_blacklist:
            return False
        elif self.coop == 3:
            return True
        elif item.flags & (ItemClassification.progression | ItemClassification.trap) > 0:
            return True
        elif self.coop == 2 and (item.flags & ItemClassification.useful) > 0:
            return True
        return False

    async def update_goal_flags(self, updated: Set[int], ctx: 'BizHawkClientContext', include_djinn: bool = False) -> None:
        messages = []
        if len(updated) > 0:
            messages.append({
                "cmd": "Set",
                "operation": "update",
                "want_reply": True,
                "key": self.get_goal_flags_key(ctx),
                "default": [],
                "operations": [
                    {
                        "operation": "update",
                        "value": [x for x in updated],
                    }
                ]
            })
        if include_djinn:
            messages.append({
                "cmd": "Set",
                "operation": "update",
                "want_reply": True,
                "key": self.get_djinn_location_key(ctx),
                "default": [],
                "operations": [
                    {
                        "operation": "update",
                        "value": [x for x in self.checked_djinn],
                    }
                ]
            })
        if messages:
            await ctx.send_msgs(messages)

    async def game_watcher(self, ctx: 'BizHawkClientContext') -> None:

        if not ctx.server or not ctx.server.socket.open or ctx.server.socket.closed:
            logger.debug("Not connected to server...")
            return

        result = await read(ctx.bizhawk_ctx, [data_loc.to_request() for data_loc in _DataLocations])
        if not self._is_in_game(result):
            # TODO: if the player goes back into the save file should we reset some things?
            self.local_locations = set()
            self.was_in_game = False
            logger.debug("Not in game...")
            return

        if not self.was_in_game and ctx.slot_data is not None:
            # logger.info(f"Slot data: {ctx.slot_data}")
            # self.starting_items = StartingItemHandler(ctx.slot_data.get('start_inventory', dict()))
            self.goals.init_reqs_from_slotdata(ctx.slot_data)
            for desired_flag in self.goals.desired_flags.keys():
                self.goal_map[desired_flag] = False
            self.check_summon_count(ctx)
            self.coop = ctx.slot_data.get("options", dict()).get("coop", 0)
            ctx.set_notify(self.get_goal_flags_key(ctx), self.get_djinn_location_key(ctx))
            # logger.info(self.goals.flag_requirements)
            # logger.info(self.goals.count_requirements)
            self.was_in_game = True
            self.goals.initialized = True

        # logger.debug(
        #     f"Local locations checked: {len(self.local_locations)}; server locations checked: {len(ctx.checked_locations)}")

        self.temp_locs = set()
        self.temp_events = set()
        await self._load_djinn(ctx)

        self._check_djinn_flags(result)
        self._check_common_flags(_DataLocations.SUMMONS, result)
        for i in range(_DataLocations.TREASURE_8_FLAGS, _DataLocations.TREASURE_F_FLAGS.value + 1):
            self._check_common_flags(_DataLocations(i), result)
        self._check_common_flags(_DataLocations.INITIAL_INVENTORY, result)
        self._check_common_flags(_DataLocations.ENEMY_FLAGS, result)
        self._check_common_flags(_DataLocations.STORY_FLAGS, result)


        await self._receive_items(ctx, result)
        self.check_summon_count(ctx)

        if self.temp_locs != self.local_locations:
            if self.temp_locs:
                logger.debug("Sending locations to AP: %s", self.temp_locs)
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": list(self.temp_locs)}])
                self.local_locations = self.temp_locs

        if self.djinn_last_count != len(self.possessed_djinn):
            if self.possessed_djinn:
                logger.debug(f"Possesed djinn: {self.possessed_djinn}")
                await ctx.send_msgs([{
                    "cmd": "Set",
                    "operation": "update",
                    "want_reply": True,
                    "key": self.get_djinn_possessed_key(ctx),
                    "default": [],
                    "operations": [
                        {
                            "operation": "update",
                            "value": [x for x in self.possessed_djinn],
                        }
                    ]
                }])
                self.djinn_last_count = len(self.possessed_djinn)


        if self.temp_events != self.local_events:
            if self.temp_events:
                await ctx.send_msgs([{
                    "cmd": "Set",
                    "operation": "update",
                    "want_reply": True,
                    "key": self.get_event_key(ctx),
                    "default": [],
                    "operations": [
                        {
                            "operation": "update",
                            "value": [x for x in self.temp_events],
                        }
                    ]
                }])
                self.local_events = self.temp_events

        await self.goals.check_goals(self, ctx)

        if not ctx.finished_game and self.goals.is_done(self, ctx):
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True
