import logging
import time
from enum import IntEnum
from base64 import b64encode
from typing import TYPE_CHECKING, Dict, Tuple, List, Optional, Any
from NetUtils import ClientStatus, color, NetworkItem
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext, BizHawkClientCommandProcessor

nes_logger = logging.getLogger("NES")
logger = logging.getLogger("Client")

MM2_ROBOT_MASTERS_UNLOCKED = 0x8A
MM2_ROBOT_MASTERS_DEFEATED = 0x8B
MM2_ITEMS_ACQUIRED = 0x8C
MM2_LAST_WILY = 0x8D
MM2_RECEIVED_ITEMS = 0x8E
MM2_DEATHLINK = 0x8F
MM2_ENERGYLINK = 0x90
MM2_RBM_STROBE = 0x91
MM2_WEAPONS_UNLOCKED = 0x9A
MM2_ITEMS_UNLOCKED = 0x9B
MM2_WEAPON_ENERGY = 0x9C
MM2_E_TANKS = 0xA7
MM2_LIVES = 0xA8
MM2_DIFFICULTY = 0xCB
MM2_HEALTH = 0x6C0
MM2_COMPLETED_STAGES = 0x770
MM2_CONSUMABLES = 0x780

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
    0x880227: (38, 4),
    0x880228: (38, 32),
    0x880229: (38, 128),
    0x88022A: (39, 4),
    0x88022B: (39, 2),
    0x88022C: (39, 1),
    0x88022D: (38, 64),
    0x88022E: (38, 16),
    0x88022F: (38, 8),
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


class MM2EnergyLinkType(IntEnum):
    Life = 0
    AtomicFire = 1
    AirShooter = 2
    LeafShield = 3
    BubbleLead = 4
    QuickBoomerang = 5
    TimeStopper = 6
    MetalBlade = 7
    CrashBomber = 8
    Item1 = 9
    Item2 = 10
    Item3 = 11
    OneUP = 12


request_to_name: Dict[str, str] = {
    "HP": "health",
    "AF": "Atomic Fire energy",
    "AS": "Air Shooter energy",
    "LS": "Leaf Shield energy",
    "BL": "Bubble Lead energy",
    "QB": "Quick Boomerang energy",
    "TS": "Time Stopper energy",
    "MB": "Metal Blade energy",
    "CB": "Crash Bomber energy",
    "I1": "Item 1 energy",
    "I2": "Item 2 energy",
    "I3": "Item 3 energy",
    "1U": "lives"
}

HP_EXCHANGE_RATE = 500000000
WEAPON_EXCHANGE_RATE = 250000000
ONEUP_EXCHANGE_RATE = 14000000000


def cmd_pool(self: "BizHawkClientCommandProcessor") -> None:
    """Check the current pool of EnergyLink, and requestable refills from it."""
    if self.ctx.game != "Mega Man 2":
        logger.warning("This command can only be used when playing Mega Man 2.")
        return
    if not self.ctx.server or not self.ctx.slot:
        logger.warning("You must be connected to a server to use this command.")
        return
    energylink = self.ctx.stored_data.get(f"EnergyLink{self.ctx.team}", 0)
    health_points = energylink // HP_EXCHANGE_RATE
    weapon_points = energylink // WEAPON_EXCHANGE_RATE
    lives = energylink // ONEUP_EXCHANGE_RATE
    logger.info(f"Healing available: {health_points}\n"
                f"Weapon refill available: {weapon_points}\n"
                f"Lives available: {lives}")


def cmd_request(self: "BizHawkClientCommandProcessor", amount: str, target: str) -> None:
    from worlds._bizhawk.context import BizHawkClientContext
    """Request a refill from EnergyLink."""
    if self.ctx.game != "Mega Man 2":
        logger.warning("This command can only be used when playing Mega Man 2.")
        return
    if not self.ctx.server or not self.ctx.slot:
        logger.warning("You must be connected to a server to use this command.")
        return
    valid_targets: Dict[str, MM2EnergyLinkType] = {
        "HP": MM2EnergyLinkType.Life,
        "AF": MM2EnergyLinkType.AtomicFire,
        "AS": MM2EnergyLinkType.AirShooter,
        "LS": MM2EnergyLinkType.LeafShield,
        "BL": MM2EnergyLinkType.BubbleLead,
        "QB": MM2EnergyLinkType.QuickBoomerang,
        "TS": MM2EnergyLinkType.TimeStopper,
        "MB": MM2EnergyLinkType.MetalBlade,
        "CB": MM2EnergyLinkType.CrashBomber,
        "I1": MM2EnergyLinkType.Item1,
        "I2": MM2EnergyLinkType.Item2,
        "I3": MM2EnergyLinkType.Item3,
        "1U": MM2EnergyLinkType.OneUP
    }
    if target.upper() not in valid_targets:
        logger.warning(f"Unrecognized target {target.upper()}. Available targets: {', '.join(valid_targets.keys())}")
        return
    ctx = self.ctx
    assert isinstance(ctx, BizHawkClientContext)
    client = ctx.client_handler
    assert isinstance(client, MegaMan2Client)
    client.refill_queue.append((valid_targets[target.upper()], int(amount)))
    logger.info(f"Restoring {amount} {request_to_name[target.upper()]}.")


def cmd_autoheal(self) -> None:
    """Enable auto heal from EnergyLink."""
    if self.ctx.game != "Mega Man 2":
        logger.warning("This command can only be used when playing Mega Man 2.")
        return
    if not self.ctx.server or not self.ctx.slot:
        logger.warning("You must be connected to a server to use this command.")
        return
    else:
        assert isinstance(self.ctx.client_handler, MegaMan2Client)
        if self.ctx.client_handler.auto_heal:
            self.ctx.client_handler.auto_heal = False
            logger.info(f"Auto healing disabled.")
        else:
            self.ctx.client_handler.auto_heal = True
            logger.info(f"Auto healing enabled.")


def get_sfx_writes(sfx: int) -> Tuple[Tuple[int, bytes, str], ...]:
    return (MM2_SFX_QUEUE, sfx.to_bytes(1, 'little'), "RAM"), (MM2_SFX_STROBE, 0x01.to_bytes(1, "little"), "RAM")


class MegaMan2Client(BizHawkClient):
    game = "Mega Man 2"
    system = "NES"
    patch_suffix = ".apmm2"
    item_queue: List[NetworkItem] = []
    pending_death_link: bool = False
    # default to true, as we don't want to send a deathlink until Mega Man's HP is initialized once
    sending_death_link: bool = True
    death_link: bool = False
    energy_link: bool = False
    rom: Optional[bytes] = None
    weapon_energy: int = 0
    health_energy: int = 0
    auto_heal: bool = False
    refill_queue: List[Tuple[MM2EnergyLinkType, int]] = []
    last_wily: Optional[int] = None  # default to wily 1

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from worlds._bizhawk import RequestFailedError, read, get_memory_size
        from . import MM2World

        try:
            if (await get_memory_size(ctx.bizhawk_ctx, "PRG ROM")) < 0x3FFB0:
                if "pool" in ctx.command_processor.commands:
                    ctx.command_processor.commands.pop("pool")
                if "request" in ctx.command_processor.commands:
                    ctx.command_processor.commands.pop("request")
                if "autoheal" in ctx.command_processor.commands:
                    ctx.command_processor.commands.pop("autoheal")
                return False

            game_name, version = (await read(ctx.bizhawk_ctx, [(0x3FFB0, 21, "PRG ROM"),
                                                               (0x3FFC8, 3, "PRG ROM")]))
            if game_name[:3] != b"MM2" or version != bytes(MM2World.world_version):
                if game_name[:3] == b"MM2":
                    # I think this is an easier check than the other?
                    older_version = "0.2.1" if version == b"\xFF\xFF\xFF" else f"{version[0]}.{version[1]}.{version[2]}"
                    logger.warning(f"This Mega Man 2 patch was generated for an different version of the apworld. "
                                   f"Please use that version to connect instead.\n"
                                   f"Patch version: ({older_version})\n"
                                   f"Client version: ({'.'.join([str(i) for i in MM2World.world_version])})")
                if "pool" in ctx.command_processor.commands:
                    ctx.command_processor.commands.pop("pool")
                if "request" in ctx.command_processor.commands:
                    ctx.command_processor.commands.pop("request")
                if "autoheal" in ctx.command_processor.commands:
                    ctx.command_processor.commands.pop("autoheal")
                return False
        except UnicodeDecodeError:
            return False
        except RequestFailedError:
            return False  # Should verify on the next pass

        ctx.game = self.game
        self.rom = game_name
        ctx.items_handling = 0b111
        ctx.want_slot_data = False
        deathlink = (await read(ctx.bizhawk_ctx, [(0x3FFC5, 1, "PRG ROM")]))[0][0]
        if deathlink & 0x01:
            self.death_link = True
        if deathlink & 0x02:
            self.energy_link = True

        if self.energy_link:
            if "pool" not in ctx.command_processor.commands:
                ctx.command_processor.commands["pool"] = cmd_pool
            if "request" not in ctx.command_processor.commands:
                ctx.command_processor.commands["request"] = cmd_request
            if "autoheal" not in ctx.command_processor.commands:
                ctx.command_processor.commands["autoheal"] = cmd_autoheal

        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        if self.rom:
            ctx.auth = b64encode(self.rom).decode()

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: Dict[str, Any]) -> None:
        if cmd == "Bounced":
            if "tags" in args:
                assert ctx.slot is not None
                if "DeathLink" in args["tags"] and args["data"]["source"] != ctx.slot_info[ctx.slot].name:
                    self.on_deathlink(ctx)
        elif cmd == "Retrieved":
            if f"MM2_LAST_WILY_{ctx.team}_{ctx.slot}" in args["keys"]:
                self.last_wily = args["keys"][f"MM2_LAST_WILY_{ctx.team}_{ctx.slot}"]
        elif cmd == "Connected":
            if self.energy_link:
                ctx.set_notify(f"EnergyLink{ctx.team}")
                if ctx.ui:
                    ctx.ui.enable_energy_link()

    async def send_deathlink(self, ctx: "BizHawkClientContext") -> None:
        self.sending_death_link = True
        ctx.last_death_link = time.time()
        await ctx.send_death("Mega Man was defeated.")

    def on_deathlink(self, ctx: "BizHawkClientContext") -> None:
        ctx.last_death_link = time.time()
        self.pending_death_link = True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        from worlds._bizhawk import read, write

        if ctx.server is None:
            return

        if ctx.slot is None:
            return

        # get our relevant bytes
        robot_masters_unlocked, robot_masters_defeated, items_acquired, \
            weapons_unlocked, items_unlocked, items_received, \
            completed_stages, consumable_checks, \
            e_tanks, lives, weapon_energy, health, difficulty, death_link_status, \
            energy_link_packet, last_wily = await read(ctx.bizhawk_ctx, [
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
                (MM2_DEATHLINK, 1, "RAM"),
                (MM2_ENERGYLINK, 1, "RAM"),
                (MM2_LAST_WILY, 1, "RAM"),
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
        if self.death_link:
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

        if self.last_wily != last_wily[0]:
            if self.last_wily is None:
                # revalidate last wily from data storage
                await ctx.send_msgs([{"cmd": "Set", "key": f"MM2_LAST_WILY_{ctx.team}_{ctx.slot}", "operations": [
                    {"operation": "default", "value": 8}
                ]}])
                await ctx.send_msgs([{"cmd": "Get", "keys": [f"MM2_LAST_WILY_{ctx.team}_{ctx.slot}"]}])
            elif last_wily[0] == 0:
                writes.append((MM2_LAST_WILY, self.last_wily.to_bytes(1, "little"), "RAM"))
            else:
                # correct our setting
                self.last_wily = last_wily[0]
                await ctx.send_msgs([{"cmd": "Set", "key": f"MM2_LAST_WILY_{ctx.team}_{ctx.slot}", "operations": [
                    {"operation": "replace", "value": self.last_wily}
                ]}])

        # handle receiving items
        recv_amount = items_received[0]
        if recv_amount < len(ctx.items_received):
            item = ctx.items_received[recv_amount]
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(ctx.item_names.lookup_in_game(item.item), 'red', 'bold'),
                color(ctx.player_names[item.player], 'yellow'),
                ctx.location_names.lookup_in_slot(item.location, item.player), recv_amount, len(ctx.items_received)))

            if item.item & 0x130 == 0:
                # Robot Master Weapon
                new_weapons = weapons_unlocked[0] | (1 << ((item.item & 0xF) - 1))
                writes.append((MM2_WEAPONS_UNLOCKED, new_weapons.to_bytes(1, 'little'), "RAM"))
                writes.extend(get_sfx_writes(0x21))
            elif item.item & 0x30 == 0:
                # Robot Master Stage Access
                new_stages = robot_masters_unlocked[0] & ~(1 << ((item.item & 0xF) - 1))
                writes.append((MM2_ROBOT_MASTERS_UNLOCKED, new_stages.to_bytes(1, 'little'), "RAM"))
                writes.extend(get_sfx_writes(0x3a))
                writes.append((MM2_RBM_STROBE, b"\x01", "RAM"))
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

        if energy_link_packet[0]:
            pickup = energy_link_packet[0]
            if pickup in (0x76, 0x77):
                # Health pickups
                if pickup == 0x77:
                    value = 2
                else:
                    value = 10
                exchange_rate = HP_EXCHANGE_RATE
            elif pickup in (0x78, 0x79):
                # Weapon Energy
                if pickup == 0x79:
                    value = 2
                else:
                    value = 10
                exchange_rate = WEAPON_EXCHANGE_RATE
            elif pickup == 0x7B:
                # 1-Up
                value = 1
                exchange_rate = ONEUP_EXCHANGE_RATE
            else:
                # if we managed to pickup something else, we should just fall through
                value = 0
                exchange_rate = 0
            contribution = (value * exchange_rate) >> 1
            if contribution:
                await ctx.send_msgs([{
                    "cmd": "Set", "key": f"EnergyLink{ctx.team}", "slot": ctx.slot, "operations":
                        [{"operation": "add", "value": contribution},
                         {"operation": "max", "value": 0}]}])
            logger.info(f"Deposited {contribution / HP_EXCHANGE_RATE} health into the pool.")
            writes.append((MM2_ENERGYLINK, 0x00.to_bytes(1, "little"), "RAM"))

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

        if self.health_energy or self.auto_heal:
            # Health Energy
            # We save this if the player has not taken any damage
            current_health = health[0]
            if 0 < current_health < 0x1C:
                health_diff = 0x1C - current_health
                if self.health_energy:
                    if health_diff > self.health_energy:
                        health_diff = self.health_energy
                    self.health_energy -= health_diff
                else:
                    pool = ctx.stored_data.get(f"EnergyLink{ctx.team}", 0)
                    if health_diff * HP_EXCHANGE_RATE > pool:
                        health_diff = int(pool // HP_EXCHANGE_RATE)
                    await ctx.send_msgs([{
                        "cmd": "Set", "key": f"EnergyLink{ctx.team}", "slot": ctx.slot, "operations":
                            [{"operation": "add", "value": -health_diff * HP_EXCHANGE_RATE},
                             {"operation": "max", "value": 0}]}])
                current_health += health_diff
                writes.append((MM2_HEALTH, current_health.to_bytes(1, 'little'), "RAM"))

        if self.refill_queue:
            refill_type, refill_amount = self.refill_queue.pop()
            if refill_type == MM2EnergyLinkType.Life:
                exchange_rate = HP_EXCHANGE_RATE
            elif refill_type == MM2EnergyLinkType.OneUP:
                exchange_rate = ONEUP_EXCHANGE_RATE
            else:
                exchange_rate = WEAPON_EXCHANGE_RATE
            pool = ctx.stored_data.get(f"EnergyLink{ctx.team}", 0)
            request = exchange_rate * refill_amount
            if request > pool:
                logger.warning(
                    f"Not enough energy to fulfill the request. Maximum request: {pool // exchange_rate}")
            else:
                await ctx.send_msgs([{
                    "cmd": "Set", "key": f"EnergyLink{ctx.team}", "slot": ctx.slot, "operations":
                        [{"operation": "add", "value": -request},
                         {"operation": "max", "value": 0}]}])
                if refill_type == MM2EnergyLinkType.Life:
                    refill_ptr = MM2_HEALTH
                elif refill_type == MM2EnergyLinkType.OneUP:
                    refill_ptr = MM2_LIVES
                else:
                    refill_ptr = MM2_WEAPON_ENERGY - 1 + refill_type
                current_value = (await read(ctx.bizhawk_ctx, [(refill_ptr, 1, "RAM")]))[0][0]
                new_value = min(0x1C if refill_type != MM2EnergyLinkType.OneUP else 99, current_value + refill_amount)
                writes.append((refill_ptr, new_value.to_bytes(1, "little"), "RAM"))

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
                is_checked = consumable_checks[MM2_CONSUMABLE_TABLE[consumable][0]] \
                             & MM2_CONSUMABLE_TABLE[consumable][1]
                if is_checked:
                    new_checks.append(consumable)

        for new_check_id in new_checks:
            ctx.locations_checked.add(new_check_id)
            location = ctx.location_names.lookup_in_game(new_check_id)
            nes_logger.info(
                f'New Check: {location} ({len(ctx.locations_checked)}/'
                f'{len(ctx.missing_locations) + len(ctx.checked_locations)})')
            await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [new_check_id]}])
