import logging
import time
import typing
from base64 import b64encode
from typing import TYPE_CHECKING, Dict, Tuple
from NetUtils import ClientStatus, color
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

nes_logger = logging.getLogger("NES")

MM2_ROBOT_MASTERS_UNLOCKED = 0x8A
MM2_ROBOT_MASTERS_DEFEATED = 0x8B
MM2_ITEMS_ACQUIRED = 0x8C
MM2_WEAPONS_UNLOCKED = 0x9A
MM2_ITEMS_UNLOCKED = 0x9B
MM2_RECEIVED_ITEMS = 0x8E
MM2_COMPLETED_STAGES = 0x770
MM2_CONSUMABLES = 0x780
MM2_E_TANKS = 0xA7
MM2_LIVES = 0xA8
MM2_WEAPON_ENERGY = 0x9C
MM2_HEALTH = 0x6C0
MM2_DEATHLINK = 0x8F
MM2_DIFFICULTY = 0xCB

MM2_SFX_QUEUE = 0x580
MM2_SFX_STROBE = 0x66

MM2_CONSUMABLE_TABLE: Dict[int, Tuple[int, int]] = {
    # Item: (byte offset, bit mask)
    0x880201: (0, 8),
    0x880202: (16, 1),
    0x880203: (16, 2),
    0x880204: (16, 4),
    0x880205: (16, 8),
    0x880206: (16, 16),
    0x880207: (16, 32),
    0x880208: (16, 64),
    0x880209: (16, 128),
    0x88020A: (20, 1),
    0x88020B: (20, 4),
    0x88020C: (20, 64),
    0x88020D: (21, 1),
    0x88020E: (21, 2),
    0x88020F: (21, 4),
    0x880210: (24, 1),
    0x880211: (24, 2),
    0x880212: (24, 4),
    0x880213: (28, 1),
    0x880214: (28, 2),
    0x880215: (28, 4),
    0x880216: (33, 4),
    0x880217: (33, 8),
    0x880218: (37, 8),
    0x880219: (37, 16),
    0x88021A: (38, 1),
    0x88021B: (38, 2),
    0x88021C: (39, 32),
    0x88021D: (39, 64),
    0x88021E: (39, 128),
    0x88021F: (41, 16),
    0x880220: (42, 2),
    0x880221: (42, 4),
    0x880222: (42, 8),
    0x880223: (46, 1),
    0x880224: (46, 2),
    0x880225: (46, 4),
    0x880226: (46, 8),
}


def get_sfx_writes(sfx: int):
    return (MM2_SFX_QUEUE, sfx.to_bytes(1, 'little'), "RAM"), (MM2_SFX_STROBE, 0x01.to_bytes(1, "little"), "RAM")


class MegaMan2Client(BizHawkClient):
    game = "Mega Man 2"
    system = "NES"
    patch_suffix = ".apmm2"
    item_queue: typing.List = []
    pending_death_link: bool = False
    # default to true, as we don't want to send a deathlink until Mega Man's HP is initialized once
    sending_death_link: bool = True
    death_link: bool = False
    rom: typing.Optional[bytes] = None
    weapon_energy: int = 0
    health_energy: int = 0

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from worlds._bizhawk import RequestFailedError, read

        try:
            game_name = ((await read(ctx.bizhawk_ctx, [(0x3FFB0, 21, "PRG ROM")]))[0])
            if game_name[:3] != b"MM2":
                return False
        except UnicodeDecodeError:
            return False
        except RequestFailedError:
            return False  # Should verify on the next pass

        ctx.game = self.game
        self.rom = game_name
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        if self.rom:
            ctx.auth = b64encode(self.rom).decode()

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict) -> None:
        if cmd == "Bounced":
            if "tags" in args:
                if "DeathLink" in args["tags"] and args["data"]["source"] != ctx.slot_info[ctx.slot].name:
                    self.on_deathlink(ctx)

    async def send_deathlink(self, ctx: "BizHawkClientContext"):
        self.sending_death_link = True
        ctx.last_death_link = time.time()
        await ctx.send_death("Mega Man was defeated.")

    def on_deathlink(self, ctx: "BizHawkClientContext"):
        ctx.last_death_link = time.time()
        self.pending_death_link = True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        from worlds._bizhawk import read, write

        if ctx.server is None:
            return

        if ctx.slot is None:
            await ctx.send_connect(name=ctx.auth)

        if ctx.slot_data is None:
            return

        # get our relevant bytes
        robot_masters_unlocked, robot_masters_defeated, items_acquired, \
            weapons_unlocked, items_unlocked, items_received, \
            completed_stages, consumable_checks,\
            e_tanks, lives, weapon_energy, health, difficulty, death_link_status = await read(ctx.bizhawk_ctx, [
                (MM2_ROBOT_MASTERS_UNLOCKED, 1, "RAM"),
                (MM2_ROBOT_MASTERS_DEFEATED, 1, "RAM"),
                (MM2_ITEMS_ACQUIRED, 1, "RAM"),
                (MM2_WEAPONS_UNLOCKED, 1, "RAM"),
                (MM2_ITEMS_UNLOCKED, 1, "RAM"),
                (MM2_RECEIVED_ITEMS, 1, "RAM"),
                (MM2_COMPLETED_STAGES, 0xE, "RAM"),
                (MM2_CONSUMABLES, 52, "RAM"),
                (MM2_E_TANKS, 1, "RAM"),
                (MM2_LIVES, 1, "RAM"),
                (MM2_WEAPON_ENERGY, 11, "RAM"),
                (MM2_HEALTH, 1, "RAM"),
                (MM2_DIFFICULTY, 1, "RAM"),
                (MM2_DEATHLINK, 1, "RAM")
            ])

        if difficulty[0] not in (0, 1):
            return  # Game is not initialized

        if not ctx.finished_game and completed_stages[0xD] != 0:
            # this sets on credits fade, no real better way to do this
            await ctx.send_msgs([{
                "cmd": "StatusUpdate",
                "status": ClientStatus.CLIENT_GOAL
            }])
        writes = []

        # deathlink
        if ctx.slot_data["death_link"]:
            if not self.death_link:
                self.death_link = True
                await ctx.update_death_link(self.death_link)
        if self.pending_death_link:
            writes.append((MM2_DEATHLINK, bytes([0x01]), "RAM"))
            self.pending_death_link = False
            self.sending_death_link = True
        if "DeathLink" in ctx.tags and ctx.last_death_link + 1 < time.time():
            if health[0] == 0x00 and not self.sending_death_link:
                await self.send_deathlink(ctx)
            elif health[0] != 0x00 and not death_link_status[0]:
                self.sending_death_link = False

        # handle receiving items
        recv_amount = items_received[0]
        if recv_amount < len(ctx.items_received):
            item = ctx.items_received[recv_amount]
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(ctx.item_names[item.item], 'red', 'bold'),
                color(ctx.player_names[item.player], 'yellow'),
                ctx.location_names[item.location], recv_amount, len(ctx.items_received)))

            if item.item & 0x130 == 0:
                # Robot Master Weapon
                new_weapons = weapons_unlocked[0] | (1 << ((item.item & 0xF) - 1))
                writes.append((MM2_WEAPONS_UNLOCKED, new_weapons.to_bytes(1, 'little'), "RAM"))
                writes.extend(get_sfx_writes(0x21))
            elif item.item & 0x30 == 0:
                # Robot Master Stage Access
                # print(robot_masters_unlocked[0])
                new_stages = robot_masters_unlocked[0] ^ (1 << ((item.item & 0xF) - 1))
                # print(new_stages)
                writes.append((MM2_ROBOT_MASTERS_UNLOCKED, new_stages.to_bytes(1, 'little'), "RAM"))
                writes.extend(get_sfx_writes(0x3a))
            elif item.item & 0x20 == 0:
                # Items
                new_items = items_unlocked[0] | (1 << ((item.item & 0xF) - 1))
                writes.append((MM2_ITEMS_UNLOCKED, new_items.to_bytes(1, 'little'), "RAM"))
                writes.extend(get_sfx_writes(0x21))
            else:
                # append to the queue, so we handle it later
                self.item_queue.append(item)
            recv_amount += 1
            writes.append((MM2_RECEIVED_ITEMS, recv_amount.to_bytes(1, 'little'), "RAM"))

        if self.weapon_energy:
            # Weapon Energy
            # We parse the whole thing to spread it as thin as possible
            current_energy = self.weapon_energy
            weapon_energy = bytearray(weapon_energy)
            for i, weapon in zip(range(len(weapon_energy)), weapon_energy):
                if weapon < 0x1C:
                    missing = 0x1C - weapon
                    if missing > self.weapon_energy:
                        missing = self.weapon_energy
                    self.weapon_energy -= missing
                    weapon_energy[i] = weapon + missing
                    if not self.weapon_energy:
                        writes.append((MM2_WEAPON_ENERGY, weapon_energy, "RAM"))
                        break
            else:
                if current_energy != self.weapon_energy:
                    writes.append((MM2_WEAPON_ENERGY, weapon_energy, "RAM"))

        if self.health_energy:
            # Health Energy
            # We save this if the player has not taken any damage
            current_health = health[0]
            if current_health < 0x1C:
                health_diff = 0x1C - current_health
                if health_diff > self.health_energy:
                    health_diff = self.health_energy
                self.health_energy -= health_diff
                current_health += health_diff
                writes.append((MM2_HEALTH, current_health.to_bytes(1, 'little'), "RAM"))

        if len(self.item_queue):
            item = self.item_queue.pop(0)
            idx = item.item & 0xF
            if idx == 0:
                # 1-Up
                current_lives = lives[0]
                if current_lives > 99:
                    self.item_queue.append(item)
                else:
                    current_lives += 1
                    writes.append((MM2_LIVES, current_lives.to_bytes(1, 'little'), "RAM"))
                    writes.extend(get_sfx_writes(0x42))
            elif idx == 1:
                self.weapon_energy += 0xE
                writes.extend(get_sfx_writes(0x28))
            elif idx == 2:
                self.health_energy += 0xE
                writes.extend(get_sfx_writes(0x28))
            elif idx == 3:
                # E-Tank
                # visuals only allow 4, but we're gonna go up to 9 anyway? May change
                current_tanks = e_tanks[0]
                if current_tanks < 9:
                    current_tanks += 1
                    writes.append((MM2_E_TANKS, current_tanks.to_bytes(1, 'little'), "RAM"))
                    writes.extend(get_sfx_writes(0x42))
                else:
                    self.item_queue.append(item)

        await write(ctx.bizhawk_ctx, writes)

        new_checks = []
        # check for locations
        for i in range(8):
            flag = 1 << i
            if robot_masters_defeated[0] & flag:
                wep_id = 0x880101 + i
                if wep_id not in ctx.checked_locations:
                    new_checks.append(wep_id)

        for i in range(3):
            flag = 1 << i
            if items_acquired[0] & flag:
                itm_id = 0x880111 + i
                if itm_id not in ctx.checked_locations:
                    new_checks.append(itm_id)

        for i in range(0xD):
            rbm_id = 0x880001 + i
            if completed_stages[i] != 0:
                if rbm_id not in ctx.checked_locations:
                    new_checks.append(rbm_id)

        for consumable in MM2_CONSUMABLE_TABLE:
            if consumable not in ctx.checked_locations:
                is_checked = consumable_checks[MM2_CONSUMABLE_TABLE[consumable][0]] & MM2_CONSUMABLE_TABLE[consumable][1]
                if is_checked:
                    new_checks.append(consumable)

        for new_check_id in new_checks:
            ctx.locations_checked.add(new_check_id)
            location = ctx.location_names[new_check_id]
            nes_logger.info(
                f'New Check: {location} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
            await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [new_check_id]}])
