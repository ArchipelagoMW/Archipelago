import logging

from typing import TYPE_CHECKING

from NetUtils import ClientStatus

import worlds._bizhawk as bizhawk

from worlds._bizhawk.client import BizHawkClient

from .data import memory
from .data.items import item_data_lookup, gear_item_names, gil_item_names, gil_item_sizes, zodiac_stone_names, \
    jp_item_names, jp_item_sizes, job_names, special_character_names, world_map_pass_names, earned_job_names
from .data.locations import linked_reward_names
from .data.logic.JobUnlocks import unlock_dict
from .data.memory import stones_lookup, seed_hash_length, pass_paths, finale_path

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

logger = logging.getLogger("Client")

guard_list = [
    (memory.world_loaded_address, [memory.world_loaded_value[3]], "MainRAM"),
    (memory.world_loaded_address + 1, [memory.world_loaded_value[2]], "MainRAM"),
    (memory.world_loaded_address + 2, [memory.world_loaded_value[1]], "MainRAM"),
    (memory.world_loaded_address + 3, [memory.world_loaded_value[0]], "MainRAM"),
]

def get_byte_bit_from_index(index):
    return index // 8, 2 ** (index % 8)

def get_bit_value_from_position(position):
    return 2 ** position

class FinalFantasyTacticsIvaliceIslandClient(BizHawkClient):
    game = "Final Fantasy Tactics Ivalice Island"
    system = "PSX"
    patch_suffix = ".apfftii"

    def __init__(self) -> None:
        self.ram = "MainRAM"
        self.location_name_to_id: dict[str, int] | None = None
        self.item_name_to_id: dict[str, int] | None = None
        self.logged_version = False

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            # Check ROM name/patch version
            rom_name = ((await bizhawk.read(
                ctx.bizhawk_ctx,
                [(memory.cd_name_location, len(memory.cd_name), self.ram)]))[0])
            try:
                rom_name = rom_name.decode("utf-8")
            except UnicodeDecodeError:
                return False
            if rom_name != memory.cd_name:
                return False
        except bizhawk.RequestFailedError:
            return False  # Not able to get a response, say no for now

        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        import base64
        auth_raw = (await bizhawk.read(
            ctx.bizhawk_ctx,
            [(memory.rom_name_location_in_ram, memory.rom_name_length, self.ram)]))[0]
        ctx.auth = base64.b64encode(auth_raw).decode()

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ctx.server is None:
            return

        if ctx.slot is None:
            return
        try:
            if self.location_name_to_id is None:
                from . import FinalFantasyTacticsIvaliceIslandWorld
                self.location_name_to_id = FinalFantasyTacticsIvaliceIslandWorld.location_name_to_id
                self.item_name_to_id = FinalFantasyTacticsIvaliceIslandWorld.item_name_to_id
            if await self.check_valid_game(ctx):
                await self.check_victory(ctx)
                await self.location_check(ctx)
                await self.received_items_check(ctx)
                await self.write_pass_paths(ctx)

        except bizhawk.RequestFailedError:
            # The connector didn't respond. Exit handler and return to main loop to reconnect
            pass

    async def check_valid_game(self, ctx: "BizHawkClientContext") -> bool:
        game_started_address, game_started_bit = get_byte_bit_from_index(memory.game_started_flag_address)
        game_started_data = await self.read_ram_value_guarded(ctx, memory.event_flags_location + game_started_address)
        if game_started_data is None:
            return False
        if game_started_data & game_started_bit == 0:
            return False
        return True

    async def location_check(self, ctx: "BizHawkClientContext"):
        locations_checked = []
        locations_checked.extend(await self.check_major_locations(ctx))
        locations_checked.extend(await self.check_poaches(ctx))
        locations_checked.extend(await self.check_job_unlocks(ctx))

        found_locations = await ctx.check_locations(locations_checked)
        for location in found_locations:
            ctx.locations_checked.add(location)

    async def check_major_locations(self, ctx: "BizHawkClientContext") -> list[int]:
        locations_checked = []
        major_locations_data = await self.read_ram_values_guarded(
            ctx,
            memory.event_flags_location,
            memory.event_flags_length)
        if major_locations_data is None:
            return locations_checked
        for location, flag in memory.locations_to_read.items():
            offset, bit = get_byte_bit_from_index(flag)
            if major_locations_data[offset] & bit:
                locations_checked.append(self.location_name_to_id[location])
                if location in linked_reward_names.keys():
                    for linked_location in linked_reward_names[location]:
                        locations_checked.append(self.location_name_to_id[linked_location])
        return locations_checked

    async def check_poaches(self, ctx: "BizHawkClientContext") -> list[int]:
        locations_checked = []
        poach_data = await self.read_ram_values_guarded(
            ctx,
            memory.poaching_flags_location,
            memory.poaching_flags_length)
        if poach_data is None:
            return locations_checked
        for location, flag in memory.poaching_addresses.items():
            offset, bit = get_byte_bit_from_index(flag)
            if poach_data[offset] & bit:
                locations_checked.append(self.location_name_to_id[location])
        return locations_checked

    async def check_job_unlocks(self, ctx: "BizHawkClientContext") -> list[int]:
        locations_checked = []
        formation_data = await self.read_ram_values_guarded(ctx, memory.unit_stats_address, memory.unit_stats_length)
        if formation_data is None:
            return locations_checked
        unlocked_jobs = set()
        for unit_number in range(memory.unit_count):
            current_unit_jobs = {}
            base_address = unit_number * memory.unit_stat_size
            party_id_location = base_address + memory.party_id_offset
            unit_party_id_data = formation_data[party_id_location]
            if unit_party_id_data == 0xFF:
                continue
            for index, job in enumerate(memory.job_level_order):
                job_byte_location = base_address + memory.job_level_offset + (index // 2)
                if index % 2 == 0:
                    job_nybble = (formation_data[job_byte_location] & 0xF0) >> 4
                else:
                    job_nybble = formation_data[job_byte_location] & 0x0F
                current_unit_jobs[job] = job_nybble
            for job, requirements in unlock_dict.items():
                job_ids = []
                for earned_job in earned_job_names:
                    job_ids.append(self.item_name_to_id[earned_job])
                all_jobs_obtained = [item.item for item in ctx.items_received if item.item in job_ids]
                jobs_obtained_names = [ctx.item_names.lookup_in_game(pass_id) for pass_id in all_jobs_obtained]
                jobs_obtained_names.extend(["Squire"])
                unlock_job = self.check_job_unlock_condition(current_unit_jobs, requirements, jobs_obtained_names)
                if unlock_job:
                    unlocked_jobs.add(f"{job} Unlock")
        for job in unlocked_jobs:
            locations_checked.append(self.location_name_to_id[job])
        return locations_checked

    def check_job_unlock_condition(self, job_levels, unlock_requirements, current_jobs):
        unlock = True
        for requirement_job, required_level in unlock_requirements.items():
            current_level = job_levels[requirement_job]
            if requirement_job not in current_jobs:
                return False
            if current_level < required_level:
                unlock = False
            if requirement_job == "Bard":
                if job_levels["Bard"] == 0:
                    unlock = False
            if requirement_job == "Dancer":
                if job_levels["Dancer"] == 0:
                    unlock = False
            if unlock == False:
                return False
        return True

    async def received_items_check(self, ctx: "BizHawkClientContext"):
        write_list: list[tuple[int, list[int], str]] = []

        items_received_count_low = await self.read_ram_value_guarded(ctx, memory.items_received_low)
        items_received_count_high = await self.read_ram_value_guarded(ctx, memory.items_received_high)
        if items_received_count_low is None or items_received_count_high is None:
            return
        items_received_count = int.from_bytes([items_received_count_low, items_received_count_high], "little")
        if items_received_count < len(ctx.items_received):
            current_item = ctx.items_received[items_received_count]
            current_item_id = current_item.item
            current_item_name = ctx.item_names.lookup_in_game(current_item_id, ctx.game)
            if current_item_name in gear_item_names:
                write_list_candidate = await self.write_inventory_item(ctx, current_item_name)
                if write_list_candidate is None:
                    return
                write_list.append(write_list_candidate)
            elif current_item_name == "Progressive Shop Level":
                write_list_candidate = await self.increment_shop_progression(ctx)
                if write_list_candidate is None:
                    return
                write_list.append(write_list_candidate)
            elif current_item_name in gil_item_names:
                write_list_candidate = await self.write_gil_item(ctx, current_item_name)
                if write_list_candidate is None:
                    return
                write_list.extend(write_list_candidate)
            elif current_item_name in zodiac_stone_names:
                write_list_candidate = await self.write_zodiac_stones(ctx, current_item_name)
                if write_list_candidate is None:
                    return
                write_list.append(write_list_candidate)
            elif current_item_name in jp_item_names:
                write_list_candidate = await self.write_jp_items(ctx, current_item_name)
                if write_list_candidate is None:
                    return
                write_list.extend(write_list_candidate)
                write_list_candidate = await self.write_cumulative_boon(ctx, current_item_name)
                if write_list_candidate is None:
                    return
                write_list.extend(write_list_candidate)
            elif current_item_name in special_character_names:
                write_list_candidate = await self.write_character_recruit(ctx, current_item_name)
                if write_list_candidate is None:
                    return
                write_list.append(write_list_candidate)
            elif current_item_name == "Progressive Ramza Job Form":
                write_list_candidate = await self.write_ramza_form(ctx)
                if write_list_candidate is None:
                    return
                write_list.append(write_list_candidate)
            elif current_item_name in job_names:
                write_list_candidate = await self.write_job_unlocks(ctx, current_item_name)
                if write_list_candidate is None:
                    return
                write_list.append(write_list_candidate)
            items_received_count += 1
            write_list.append((memory.items_received_low, [items_received_count % 256], self.ram))
            write_list.append((memory.items_received_high, [items_received_count // 256], self.ram))
            write_successful = await self.write_ram_values_guarded(ctx, write_list)
            if write_successful:
                await bizhawk.display_message(ctx.bizhawk_ctx, f"Received {current_item_name}")

    async def check_victory(self, ctx):
        value = None
        if ctx.finished_game:
            return
        else:
            if self.location_name_to_id["Graveyard of Airships 2 Story Battle"] in ctx.locations_checked:
                await ctx.send_msgs([
                    {"cmd": "StatusUpdate",
                     "status": ClientStatus.CLIENT_GOAL}
                ])
                ctx.finished_game = True

    async def set_options_flags(self, ctx):
        write_list = []
        sidequest_address, sidequest_bit = get_byte_bit_from_index(memory.yaml_options["Sidequests"])
        sidequest_data = await self.read_ram_value_guarded(ctx, memory.event_flags_location + sidequest_address)
        if sidequest_data is None:
            return
        new_sidequest_data = sidequest_data | sidequest_bit
        write_list.append((memory.event_flags_location + sidequest_address, [new_sidequest_data], self.ram))
        await self.write_ram_values_guarded(ctx, write_list)

    async def write_inventory_item(self, ctx: "BizHawkClientContext", item: str) -> tuple[int, list[int], str] | None:
        item_index = item_data_lookup[item].game_id
        current_item_data = await self.read_ram_value_guarded(ctx, memory.inventory_start_address + item_index)
        if current_item_data is None:
            return
        current_item_quantity = current_item_data
        new_item_quantity = min(99, current_item_quantity + 1)
        return memory.inventory_start_address + item_index, [new_item_quantity], self.ram

    async def increment_shop_progression(self, ctx: "BizHawkClientContext") -> tuple[int, list[int], str] | None:
        current_shop_data = await self.read_ram_value_guarded(ctx, memory.shop_progression_address)
        if current_shop_data is None:
            return
        new_shop_progression = min(15, current_shop_data + 1)
        return memory.shop_progression_address, [new_shop_progression], self.ram

    async def write_gil_item(self, ctx: "BizHawkClientContext", gil_item: str) -> list[tuple[int, list[int], str]] | None:
        current_gil_data = await self.read_ram_values_guarded(ctx, memory.war_funds_address, memory.war_funds_length)
        if current_gil_data is None:
            return None
        current_gil = int.from_bytes(current_gil_data, "little")
        gil_item_size = int(ctx.slot_data["bonus_gil_item_size"])
        gil_quantity = gil_item_sizes[gil_item_size][gil_item]
        new_gil = min(99999999, current_gil + gil_quantity)
        return [
            (memory.war_funds_address, [new_gil % 256], self.ram),
            (memory.war_funds_address + 1, [new_gil // 256 % 256], self.ram),
            (memory.war_funds_address + 2, [new_gil // (2**16) % 256], self.ram),
            (memory.war_funds_address + 3, [new_gil // (2**24)], self.ram),
        ]

    async def write_jp_items(self, ctx: "BizHawkClientContext", jp_item: str) -> list[tuple[int, list[int], str]] | None:
        jp_item_size = int(ctx.slot_data["jp_boon_size"])
        jp_quantity = jp_item_sizes[jp_item_size][jp_item]

        formation_data = await self.read_ram_values_guarded(ctx, memory.unit_stats_address, memory.unit_stats_length)
        if formation_data is None:
            return None
        new_formation_data = bytearray(formation_data)
        for unit_number in range(memory.unit_count):
            base_address = unit_number * memory.unit_stat_size
            party_id_location = base_address + memory.party_id_offset
            unit_party_id_data = formation_data[party_id_location]
            if unit_party_id_data == 0xFF:
                continue
            for job_number in range(memory.job_amount):
                jp_address = base_address + memory.jp_offset + (job_number * 2)
                current_jp = int.from_bytes(formation_data[jp_address:jp_address + 2], "little")
                new_jp = min(current_jp + jp_quantity, 9999)
                new_jp_lower_byte = new_jp % 256
                new_jp_upper_byte = new_jp // 256
                new_formation_data[jp_address] = new_jp_lower_byte
                new_formation_data[jp_address + 1] = new_jp_upper_byte

        temp_formation_data = await self.read_ram_values_guarded(ctx, memory.temp_unit_stats_address, memory.temp_unit_stats_length)
        if temp_formation_data is None:
            return None
        temp_new_formation_data = bytearray(temp_formation_data)
        for unit_number in range(memory.temp_unit_count):
            base_address = unit_number * memory.temp_unit_stat_size
            for job_number in range(memory.temp_job_amount):
                jp_address = base_address + memory.temp_jp_offset + (job_number * 2)
                current_jp = int.from_bytes(temp_formation_data[jp_address:jp_address + 2], "little")
                new_jp = min(current_jp + jp_quantity, 9999)
                new_jp_lower_byte = new_jp % 256
                new_jp_upper_byte = new_jp // 256
                temp_new_formation_data[jp_address] = new_jp_lower_byte
                temp_new_formation_data[jp_address + 1] = new_jp_upper_byte
        return [
            (memory.unit_stats_address, list(new_formation_data), self.ram),
            (memory.temp_unit_stats_address, list(temp_new_formation_data), self.ram)
        ]

    async def write_cumulative_boon(self, ctx: "BizHawkClientContext", jp_item: str) -> list[tuple[int, list[int], str]] | None:
        jp_item_size = int(ctx.slot_data["jp_boon_size"])
        jp_quantity = jp_item_sizes[jp_item_size][jp_item]
        current_jp_data = await self.read_ram_values_guarded(
            ctx,
            memory.total_jp_boon_gained,
            memory.total_jp_boon_gained_length)
        if current_jp_data is None:
            return
        current_jp_amount = int.from_bytes(current_jp_data, "little")
        new_jp_amount = min(9999, current_jp_amount + jp_quantity)
        return [
            (memory.total_jp_boon_gained, [new_jp_amount % 256], self.ram),
            (memory.total_jp_boon_gained + 1, [new_jp_amount // 256 % 256], self.ram)
        ]


    async def write_zodiac_stones(self, ctx: "BizHawkClientContext", stone_name: str) -> tuple[int, list[int], str] | None:
        address, bit = stones_lookup[stone_name]
        current_stone_data = await self.read_ram_value_guarded(ctx, address)
        if current_stone_data is None:
            return None
        new_stone_data = current_stone_data | get_bit_value_from_position(bit)
        return address, [new_stone_data], self.ram

    async def write_character_recruit(self, ctx: "BizHawkClientContext", character_name: str) -> tuple[int, list[int], str] | None:
        address, bit = get_byte_bit_from_index(memory.character_recruit_addresses[character_name])
        recruit_location = memory.event_flags_location + address
        current_recruit_data = await self.read_ram_value_guarded(ctx, recruit_location)
        if current_recruit_data is None:
            return None
        new_recruit_data = current_recruit_data | bit
        return recruit_location, [new_recruit_data], self.ram

    async def write_ramza_form(self, ctx: "BizHawkClientContext") -> tuple[int, list[int], str] | None:
        chapter_2_address, chapter_2_bit = get_byte_bit_from_index(
            memory.ramza_job_unlock_addresses["Chapter 2 Ramza Squire Job Unlock"])
        chapter_4_address, chapter_4_bit = get_byte_bit_from_index(
            memory.ramza_job_unlock_addresses["Chapter 4 Ramza Squire Job Unlock"])
        chapter_2_location = memory.event_flags_location + chapter_2_address
        chapter_4_location = memory.event_flags_location + chapter_4_address
        chapter_2_data = await self.read_ram_value_guarded(ctx, chapter_2_location)
        chapter_4_data = await self.read_ram_value_guarded(ctx, chapter_4_location)
        if chapter_2_data is None or chapter_4_data is None:
            return None
        if chapter_2_data & chapter_2_bit > 0:
            new_data = chapter_4_data | chapter_4_bit
            return chapter_4_location, [new_data], self.ram
        else:
            new_data = chapter_2_data | chapter_2_bit
            return chapter_2_location, [new_data], self.ram

    async def write_job_unlocks(self, ctx: "BizHawkClientContext", job_name: str) -> tuple[int, list[int], str] | None:
        address, bit = get_byte_bit_from_index(memory.available_jobs_addresses[job_name])
        job_location = memory.event_flags_location + address
        job_data = await self.read_ram_value_guarded(ctx, job_location)
        if job_data is None:
            return None
        new_job_data = job_data | bit
        return job_location, [new_job_data], self.ram

    async def write_pass_paths(self, ctx: "BizHawkClientContext"):
        pass_ids = []
        for world_map_pass in world_map_pass_names:
            pass_ids.append(self.item_name_to_id[world_map_pass])
        all_passes_obtained = [item.item for item in ctx.items_received if item.item in pass_ids]
        pass_obtained_names = [ctx.item_names.lookup_in_game(pass_id) for pass_id in all_passes_obtained]
        flags_to_write = []
        for pass_name in pass_obtained_names:
            if pass_name in pass_paths:
                for companion_pass in pass_paths[pass_name]:
                    if companion_pass in pass_obtained_names:
                        flags_to_write.extend(pass_paths[pass_name][companion_pass])

        stone_ids = []
        for stone in zodiac_stone_names:
            stone_ids.append(self.item_name_to_id[stone])
        all_stones_obtained = [item.item for item in ctx.items_received if item.item in stone_ids]
        if len(all_stones_obtained) >= ctx.slot_data["zodiac_stones_required"]:
            flags_to_write.append(finale_path)
        write_list = []
        for flag in flags_to_write:
            address, bit = get_byte_bit_from_index(flag)
            flag_address = memory.event_flags_location + address
            flag_data = await self.read_ram_value_guarded(ctx, flag_address)
            if flag_data is None:
                return
            new_flag_data = flag_data | bit
            write_list.append((flag_address, [new_flag_data], self.ram))
            await self.write_ram_values_guarded(ctx, write_list)

    async def read_ram_values_guarded(self, ctx: "BizHawkClientContext", location: int, size: int):
        value = await bizhawk.guarded_read(ctx.bizhawk_ctx, [(location, size, self.ram)], guard_list)
        if value is None:
            return None
        return value[0]

    async def read_ram_value_guarded(self, ctx: "BizHawkClientContext", location: int):
        value = await bizhawk.guarded_read(ctx.bizhawk_ctx, [(location, 1, self.ram)], guard_list)
        if value is None:
            return None
        return int.from_bytes(value[0], "little")

    async def write_ram_values_guarded(self, ctx: "BizHawkClientContext", write_list: list[tuple[int, list[int], str]]):
        return await bizhawk.guarded_write(ctx.bizhawk_ctx, write_list, guard_list)
