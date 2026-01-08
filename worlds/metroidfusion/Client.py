import logging
import time
from typing import TYPE_CHECKING

from NetUtils import ClientStatus

import worlds._bizhawk as bizhawk
from settings import get_settings
from worlds._bizhawk.client import BizHawkClient

from .data import memory
from .data.minor_locations import location_order as minor_location_order
from .data.major_locations import location_order as major_location_order
from .data.room_names import room_names

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

logger = logging.getLogger("Client")


def get_byte_bit_from_index(index):
    return index // 8, 2 ** (index % 8)

def get_bit_value_from_position(position):
    return 2 ** position

class MetroidFusionClient(BizHawkClient):
    game = "Metroid Fusion"
    system = "GBA"
    patch_suffix = ".apmetfus"
    current_sector: int = 0

    def __init__(self) -> None:
        self.ewram = "EWRAM"
        self.iwram = "IWRAM"
        self.sram = "SRAM"
        self.bus = "System Bus"
        self.rom = "ROM"
        self.location_name_to_id: dict[str, int] | None = None
        self.logged_version = False
        self.display_location_found_messages = True
        self.current_sectpr = 0
        self.locations_hinted: list[str] = list()
        self.deathlink_enabled = False
        self.sent_deathlink = False
        self.received_deathlink = False
        self.recently_received_deathlink = False
        self.set_tags = False
        self.current_room_name = "Docking Bay"

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            # Check ROM name/patch version
            rom_name = ((await bizhawk.read(ctx.bizhawk_ctx, [(memory.rom_name_location, 20, self.rom)]))[0])
            try:
                rom_name = rom_name.decode("utf-8")
            except UnicodeDecodeError:
                return False
            if rom_name[:3] != "MFU":
                return False  # Not a Metroid Fusion ROM
        except bizhawk.RequestFailedError:
            return False  # Not able to get a response, say no for now

        ctx.game = self.game
        ctx.items_handling = 0b011
        ctx.want_slot_data = True
        if not self.logged_version:
            from . import MetroidFusionWorld
            generation_version = (await bizhawk.read(
                ctx.bizhawk_ctx,
        [(memory.generation_version_location, 1, self.rom)]))[0]
            patch_version = (await bizhawk.read(
                ctx.bizhawk_ctx,
                [(memory.patching_version_location, 1, self.rom)]))[0]
            logger.info(f"Metroid Fusion APWorld v{int.from_bytes(generation_version)} was used for generation.")
            logger.info(f"Metroid Fusion APWorld v{int.from_bytes(patch_version)} was used for patching.")
            logger.info(f"Metroid Fusion APWorld v{MetroidFusionWorld.version} used for playing.")
            self.logged_version = True
            self.display_location_found_messages = (get_settings()["metroidfusion_options"]
                                                    .get("display_location_found_messages", True))
        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        import base64
        auth_raw = (await bizhawk.read(
            ctx.bizhawk_ctx,
            [(memory.rom_name_location, 20, self.rom)]))[0]
        ctx.auth = base64.b64encode(auth_raw).decode()

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ctx.server is None:
            return

        if ctx.slot is None:
            return
        try:
            if self.set_tags == False:
                self.set_tags = True
                if ctx.slot_data.get("DeathLink", 0) == 1:
                    self.deathlink_enabled = True
                    await ctx.update_death_link(True)
            if self.location_name_to_id is None:
                from . import MetroidFusionWorld
                self.location_name_to_id = MetroidFusionWorld.location_name_to_id
            await self.check_victory(ctx)
            await self.location_check(ctx)
            await self.received_items_check(ctx)
            await self.sync_upgrades(ctx)
            await self.check_hints(ctx)
            await self.update_map(ctx)
            if self.deathlink_enabled:
                await self.check_deathlink(ctx)
        except bizhawk.RequestFailedError:
            # The connector didn't respond. Exit handler and return to main loop to reconnect
            pass

    async def location_check(self, ctx: "BizHawkClientContext"):
        locations_checked = []


        # Minor locations
        locations_data = await self.read_ram_values_guarded(ctx, memory.minor_locations_start, 16, self.ewram)
        if locations_data is None:
            return
        for index, location in enumerate(minor_location_order):
            location_byte, location_bit = get_byte_bit_from_index(index)
            if (int(locations_data[location_byte]) & location_bit) > 0:
                locations_checked.append(self.location_name_to_id[location])

        # Major locations
        locations_data = await self.read_ram_values_guarded(ctx, memory.major_locations_start, 4, self.iwram)
        if locations_data is None:
            return
        for index, location in enumerate(major_location_order):
            if location == "ARC Data Room 2 -- Unused":
                continue
            location_byte, location_bit = get_byte_bit_from_index(index)
            if (int(locations_data[location_byte]) & location_bit) > 0:
                locations_checked.append(self.location_name_to_id[location])

        found_locations = await ctx.check_locations(locations_checked)
        for location in found_locations:
            ctx.locations_checked.add(location)
            location_name = ctx.location_names.lookup_in_game(location)
            if self.display_location_found_messages:
                logger.info(
                    f'New Check: {location_name} ({len(ctx.locations_checked)}/'
                    f'{len(ctx.missing_locations) + len(ctx.checked_locations)})')

    async def received_items_check(self, ctx: "BizHawkClientContext"):
        write_list: list[tuple[int, list[int], str]] = []

        items_received_count_low = await self.read_ram_value_guarded(ctx, memory.items_received_low, self.bus)
        items_received_count_high = await self.read_ram_value_guarded(ctx, memory.items_received_high, self.bus)
        if items_received_count_low is None or items_received_count_high is None:
            return
        items_received_count = int.from_bytes([items_received_count_low, items_received_count_high], "little")
        if items_received_count == 0xFFFF:
            items_received_count = 0
        if items_received_count < len(ctx.items_received):
            current_item = ctx.items_received[items_received_count]
            current_item_id = current_item.item
            current_item_name = ctx.item_names.lookup_in_game(current_item_id, ctx.game)
            if current_item.player == ctx.slot and current_item.location >= 0:
                pass
            elif current_item_name == "Infant Metroid":
                metroid_count_data = await self.read_ram_value_guarded(ctx,
                                                                       memory.FusionInfantMetroid.current_address,
                                                                       self.iwram)
                if metroid_count_data is None:
                    return
                new_count = metroid_count_data + 1
                write_list.append((memory.FusionInfantMetroid.current_address, [new_count], self.iwram))
            elif current_item_name in memory.keycards.keys():
                keycard = memory.keycards[current_item_name]
                current_keycard_data = await self.read_ram_value_guarded(ctx, keycard.address, self.iwram)
                if current_keycard_data is None:
                    return
                new_keycard_value = current_keycard_data | get_bit_value_from_position(keycard.bit)
                write_list.append((keycard.address, [new_keycard_value], self.iwram))
            elif current_item_name in memory.upgrades.keys():
                upgrade = memory.upgrades[current_item_name]
                current_upgrade_obtained_data = await self.read_ram_value_guarded(ctx, upgrade.inventory_address, self.iwram)
                current_upgrade_toggled_data = await self.read_ram_value_guarded(ctx, upgrade.toggled_address, self.iwram)
                if current_upgrade_obtained_data is None or current_upgrade_toggled_data is None:
                    return
                inv_bit = get_bit_value_from_position(upgrade.inventory_bit)
                new_obtained_value = current_upgrade_obtained_data | inv_bit
                write_list.append((upgrade.inventory_address, [new_obtained_value], self.iwram))
                up_bit = get_bit_value_from_position(upgrade.toggled_bit)
                new_toggled_value = current_upgrade_toggled_data | up_bit
                write_list.append((upgrade.toggled_address, [new_toggled_value], self.iwram))
                if "Beam" in current_item_name:
                    write_list.append((memory.graphics_reload_flag, [1], self.iwram))
                if current_item_name == "Missile Data":
                    missile_max_address = memory.tanks["Missile Tank"].max_address
                    missile_current_address = memory.tanks["Missile Tank"].current_address
                    missile_max_amount = await self.read_ram_value_guarded(ctx, missile_max_address, self.iwram)
                    missile_current_amount = await self.read_ram_value_guarded(ctx, missile_current_address, self.iwram)
                    if missile_max_amount is None or missile_current_amount is None:
                        return
                    missile_data_ammo = ctx.slot_data["MissileDataAmmo"]
                    new_max_value = missile_max_amount + missile_data_ammo
                    new_current_value = missile_current_amount + missile_data_ammo
                    write_list.append((missile_current_address, [(new_current_value) % 256], self.iwram))
                    write_list.append((missile_max_address, [(new_max_value) % 256], self.iwram))
                    write_list.append((missile_current_address + 1, [(new_current_value) // 256], self.iwram))
                    write_list.append((missile_max_address + 1, [(new_max_value) // 256], self.iwram))
                if current_item_name == "Power Bomb Data":
                    power_bomb_max_amount = await self.read_ram_value_guarded(
                        ctx,
                        memory.tanks["Power Bomb Tank"].max_address,
                        self.iwram
                    )
                    power_bomb_current_amount = await self.read_ram_value_guarded(
                        ctx,
                        memory.tanks["Power Bomb Tank"].current_address,
                        self.iwram
                    )
                    if power_bomb_max_amount is None or power_bomb_current_amount is None:
                        return
                    power_bomb_data_ammo = ctx.slot_data["PowerBombDataAmmo"]
                    new_max_value = power_bomb_max_amount + power_bomb_data_ammo
                    new_current_value = power_bomb_current_amount + power_bomb_data_ammo
                    write_list.append((memory.tanks["Power Bomb Tank"].current_address, [min(new_current_value, 255)], self.iwram))
                    write_list.append((memory.tanks["Power Bomb Tank"].max_address, [min(new_max_value, 255)], self.iwram))
            elif current_item_name in memory.tanks.keys():
                tank = memory.tanks[current_item_name]
                if current_item_name == "Power Bomb Tank":
                    current_amount_data = await self.read_ram_value_guarded(ctx, tank.current_address, self.iwram)
                    max_amount_data = await self.read_ram_value_guarded(ctx, tank.max_address, self.iwram)
                    if current_amount_data is None or max_amount_data is None:
                        return
                    current_amount = current_amount_data
                    max_amount = max_amount_data
                    additional_amount = ctx.slot_data["PowerBombTankAmmo"]
                    write_list.append((tank.current_address, [min(current_amount + additional_amount, 99)], self.iwram))
                    write_list.append((tank.max_address, [min(max_amount + additional_amount, 99)], self.iwram))
                elif current_item_name == "Energy Tank":
                    current_amount_data = await self.read_ram_values_guarded(ctx, tank.current_address, 2, self.iwram)
                    max_amount_data = await self.read_ram_values_guarded(ctx, tank.max_address, 2, self.iwram)
                    if current_amount_data is None or max_amount_data is None:
                        return
                    max_amount = int.from_bytes(max_amount_data, "little")
                    write_list.append((tank.current_address, [(max_amount + tank.tank_size) % 256], self.iwram))
                    write_list.append((tank.max_address, [(max_amount + tank.tank_size) % 256], self.iwram))
                    write_list.append((tank.current_address + 1, [(max_amount + tank.tank_size) // 256], self.iwram))
                    write_list.append((tank.max_address + 1, [(max_amount + tank.tank_size) // 256], self.iwram))
                else:
                    current_amount_data = await self.read_ram_values_guarded(ctx, tank.current_address, 2, self.iwram)
                    max_amount_data = await self.read_ram_values_guarded(ctx, tank.max_address, 2, self.iwram)
                    if current_amount_data is None or max_amount_data is None:
                        return
                    current_amount = int.from_bytes(current_amount_data, "little")
                    new_current = min(current_amount, 999)
                    max_amount = int.from_bytes(max_amount_data, "little")
                    new_max = min(max_amount, 999)
                    additional_amount = ctx.slot_data["MissileTankAmmo"]
                    write_list.append((tank.current_address, [new_current % 256], self.iwram))
                    write_list.append((tank.max_address, [new_max % 256], self.iwram))
                    write_list.append((tank.current_address + 1, [new_current // 256], self.iwram))
                    write_list.append((tank.max_address + 1, [new_max // 256], self.iwram))

            items_received_count += 1
            write_list.append((memory.items_received_low, [items_received_count % 256], self.bus))
            write_list.append((memory.items_received_high, [items_received_count // 256], self.bus))
            write_successful = await self.write_ram_values_guarded(ctx, write_list)
            if write_successful:
                if current_item.player != ctx.slot or current_item.location < 1:
                    await bizhawk.display_message(ctx.bizhawk_ctx, f"Received {current_item_name}")


    async def check_victory(self, ctx):
        value = await bizhawk.read(ctx.bizhawk_ctx, [(memory.game_mode, 1, self.iwram)])
        if value is None or ctx.finished_game:
            return
        else:
            if int.from_bytes(value[0]) == memory.credits_mode:
                await ctx.send_msgs([
                    {"cmd": "StatusUpdate",
                     "status": ClientStatus.CLIENT_GOAL}
                ])
                ctx.finished_game = True

    async def sync_upgrades(self, ctx: "BizHawkClientContext"):
        missile_max = ctx.slot_data["MissileDataAmmo"]
        energy_max = 99
        power_bomb_max = ctx.slot_data["PowerBombDataAmmo"]
        infant_metroid_count = 0
        write_list: list[tuple[int, list[int], str]] = []
        upgrade_addresses = {}
        toggle_addresses = {}
        keycard_value = 0x01
        items_received_count_low = await self.read_ram_value_guarded(ctx, memory.items_received_low, self.bus)
        items_received_count_high = await self.read_ram_value_guarded(ctx, memory.items_received_high, self.bus)
        if items_received_count_low is None or items_received_count_high is None:
            return
        items_received_count = int.from_bytes([items_received_count_low, items_received_count_high], "little")
        if items_received_count == 0xFFFF:
            items_received_count = 0
        if items_received_count >= len(ctx.items_received):
            items_received = ctx.slot_data["StartInventory"].copy()
            for item in ctx.items_received:
                item_id = item.item
                item_name = ctx.item_names.lookup_in_game(item_id, ctx.game)
                items_received.append(item_name)
            for item in items_received:
                current_item_name = item
                if "Beam" in current_item_name:
                    write_list.append((memory.graphics_reload_flag, [1], self.iwram))
                if current_item_name == "Infant Metroid":
                    infant_metroid_count += 1
                elif current_item_name in memory.upgrades.keys():
                    upgrade = memory.upgrades[current_item_name]
                    inv_bit = get_bit_value_from_position(upgrade.inventory_bit)
                    if upgrade.inventory_address in upgrade_addresses.keys():
                        current_upgrade_data = upgrade_addresses[upgrade.inventory_address]
                        if current_upgrade_data & inv_bit == 0:
                            toggle_bit = get_bit_value_from_position(upgrade.toggled_bit)
                            if upgrade.toggled_address in toggle_addresses.keys():
                                current_toggle_data = toggle_addresses[upgrade.toggled_address]
                                new_toggle_value = current_toggle_data | toggle_bit
                                toggle_addresses[upgrade.toggled_address] = new_toggle_value
                            else:
                                current_toggle_data = await self.read_ram_value_guarded(ctx, upgrade.toggled_address, self.iwram)
                                if current_toggle_data is None:
                                    return
                                new_toggle_value = current_toggle_data | toggle_bit
                                toggle_addresses[upgrade.toggled_address] = new_toggle_value
                        new_upgrade_value = current_upgrade_data | inv_bit
                        upgrade_addresses[upgrade.inventory_address] = new_upgrade_value
                    else:
                        current_upgrade_data = await self.read_ram_value_guarded(ctx, upgrade.inventory_address, self.iwram)
                        if current_upgrade_data is None:
                            return
                        if current_upgrade_data & inv_bit == 0:
                            toggle_bit = get_bit_value_from_position(upgrade.toggled_bit)
                            if upgrade.toggled_address in toggle_addresses.keys():
                                current_toggle_data = toggle_addresses[upgrade.toggled_address]
                                new_toggle_value = current_toggle_data | toggle_bit
                                toggle_addresses[upgrade.toggled_address] = new_toggle_value
                            else:
                                current_toggle_data = await self.read_ram_value_guarded(ctx, upgrade.toggled_address, self.iwram)
                                if current_toggle_data is None:
                                    return
                                new_toggle_value = current_toggle_data | toggle_bit
                                toggle_addresses[upgrade.toggled_address] = new_toggle_value
                        new_upgrade_value = current_upgrade_data | inv_bit
                        upgrade_addresses[upgrade.inventory_address] = new_upgrade_value
                elif current_item_name in memory.tanks.keys():
                    if current_item_name == "Missile Tank":
                        missile_max += ctx.slot_data["MissileTankAmmo"]
                    elif current_item_name == "Energy Tank":
                        energy_max += memory.tanks[current_item_name].tank_size
                    elif current_item_name == "Power Bomb Tank":
                        power_bomb_max += ctx.slot_data["PowerBombTankAmmo"]
                elif current_item_name in memory.keycards.keys():
                    keycard = memory.keycards[current_item_name]
                    current_keycard_data = await self.read_ram_value_guarded(ctx, keycard.address, self.iwram)
                    if current_keycard_data is None:
                        return
                    keycard_value = keycard_value | get_bit_value_from_position(keycard.bit)
                    write_list.append((keycard.address, [keycard_value], self.iwram))
                    write_list.append((memory.keycard_flash_address, [keycard_value], self.iwram))
            for address, value in upgrade_addresses.items():
                write_list.append((address, [value], self.iwram))
            for address, value in toggle_addresses.items():
                write_list.append((address, [value], self.iwram))
            missile_max = min(missile_max, 999)
            energy_max = min(energy_max, 2099)
            write_list.append((memory.FusionInfantMetroid.current_address, [infant_metroid_count], self.iwram))
            write_list.append((memory.tanks["Missile Tank"].max_address, [missile_max % 256], self.iwram))
            write_list.append((memory.tanks["Missile Tank"].max_address + 1, [missile_max // 256], self.iwram))
            write_list.append((memory.tanks["Energy Tank"].max_address, [energy_max % 256], self.iwram))
            write_list.append((memory.tanks["Energy Tank"].max_address + 1, [energy_max // 256], self.iwram))
            write_list.append((memory.tanks["Power Bomb Tank"].max_address, [min(power_bomb_max, 99)], self.iwram))
            await self.write_ram_values_guarded(ctx, write_list)

    async def check_hints(self, ctx: "BizHawkClientContext"):
        game_mode_data = await bizhawk.read(ctx.bizhawk_ctx, [(memory.game_mode, 1, self.iwram)])
        if game_mode_data is None:
            return
        samus_pose_data = await bizhawk.read(ctx.bizhawk_ctx, [(memory.samus_pose, 1, self.iwram)])
        if samus_pose_data is None:
            return
        game_mode = int.from_bytes(game_mode_data[0])
        samus_pose = int.from_bytes(samus_pose_data[0])
        if game_mode == memory.map_mode and samus_pose == memory.navigation_pose:
            area_data = await bizhawk.read(ctx.bizhawk_ctx, [(memory.current_area, 1, self.iwram)])
            if area_data is None:
                return
            room_data = await bizhawk.read(ctx.bizhawk_ctx, [(memory.current_room, 1, self.iwram)])
            if room_data is None:
                return
            area = int.from_bytes(area_data[0])
            room = int.from_bytes(room_data[0])
            room_key = None
            for key, value in memory.navigation_rooms.items():
                if value.area == area and value.room == room:
                    room_key = key
            if "Hints" in ctx.slot_data.keys():
                hints = ctx.slot_data["Hints"]
                if room_key in hints and room_key not in self.locations_hinted:
                    location_id = hints[room_key]["Location"]
                    player_id = hints[room_key]["Player"]
                    self.locations_hinted.append(room_key)
                    await ctx.send_msgs([{
                        "cmd": "CreateHints",
                        "locations": [location_id],
                        "player": player_id}])

    async def update_map(self, ctx: "BizHawkClientContext"):
        current_sector = await self.read_ram_value_guarded(ctx, memory.current_area, self.iwram)
        current_room = await self.read_ram_value_guarded(ctx, memory.current_room, self.iwram)
        current_room_list = [room for room in room_names if room["Area"] == current_sector and room["Room"] == current_room]
        if len(current_room_list) > 0:
            self.current_room_name = current_room_list.pop()["Name"]
        if current_sector is None:
            return
        if current_sector != self.current_sector:
            self.current_sector = current_sector
            await ctx.send_msgs([{
                "cmd": "Set",
                "key": f"fusion_current_sector_{ctx.slot}_{ctx.team}",
                "default": 0,
                "want_reply": False,
                "operations": [{"operation": "replace", "value": self.current_sector}],
            }])

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict) -> None:
        if cmd == "Bounced":
            if "tags" in args:
                if "DeathLink" in args["tags"]:
                    if args["data"]["source"] != ctx.player_names[ctx.slot]:
                        if ctx.last_death_link <= args["data"]["time"] and not self.received_deathlink:
                            self.received_deathlink = True
                            ctx.on_deathlink(args["data"])

    async def check_deathlink(self, ctx: "BizHawkClientContext"):
        current_game_mode_data = await bizhawk.read(ctx.bizhawk_ctx, [(memory.game_mode, 1, self.iwram)])
        if current_game_mode_data is None:
            return
        else:
            current_game_mode = int.from_bytes(current_game_mode_data[0])
            tank = memory.tanks["Energy Tank"]
            current_energy_data = await self.read_ram_values_guarded(ctx, tank.current_address, 2, self.iwram)
            if current_energy_data is None:
                return
            current_energy = int.from_bytes(current_energy_data, "little")
            if current_game_mode == memory.ingame_mode:
                if not self.sent_deathlink and current_energy == 0:
                    if ctx.last_death_link + 10 < time.time():
                        self.sent_deathlink = True
                        sector_message = "Main Deck" if self.current_sector == 0 else f"Sector {self.current_sector}"
                        death_message = (f"{ctx.player_names[ctx.slot]} was defeated in {sector_message}'s "
                                         f"{self.current_room_name}")
                        await ctx.send_death(death_message)
            if (self.received_deathlink
                    and (current_game_mode == memory.ingame_mode or current_game_mode == memory.map_mode)):
                tank = memory.tanks["Energy Tank"]
                write_list = []
                write_list.append((tank.current_address, [0], self.iwram))
                write_list.append((tank.current_address + 1, [0], self.iwram))
                write_successful = await self.write_ram_values_guarded(ctx, write_list)
                if write_successful:
                    self.received_deathlink = False
            if self.sent_deathlink or self.received_deathlink:
                if (current_game_mode == memory.game_over_mode
                        or (current_game_mode == memory.ingame_mode and current_energy > 0)):
                    self.sent_deathlink = False
                    self.received_deathlink = False

    async def read_ram_values_guarded(self, ctx: "BizHawkClientContext", location: int, size: int, domain: str):
        value = await bizhawk.guarded_read(ctx.bizhawk_ctx,
                                           [(location, size, domain)],
                                           [(memory.game_mode, [memory.ingame_mode], self.iwram)])
        if value is None:
            return None
        return value[0]

    async def read_ram_value_guarded(self, ctx: "BizHawkClientContext", location: int, domain: str):
        value = await bizhawk.guarded_read(ctx.bizhawk_ctx,
                                           [(location, 1, domain)],
                                           [(memory.game_mode, [memory.ingame_mode], self.iwram)])
        if value is None:
            return None
        return int.from_bytes(value[0], "little")


    async def write_ram_values_guarded(self, ctx: "BizHawkClientContext", write_list):
        return await bizhawk.guarded_write(ctx.bizhawk_ctx,
                                           write_list,
                                           [(memory.game_mode, [memory.ingame_mode], self.iwram)])
