import logging
import time
from enum import IntEnum
from base64 import b64encode
from typing import TYPE_CHECKING, Any
from NetUtils import ClientStatus, color, NetworkItem
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext, BizHawkClientCommandProcessor

nes_logger = logging.getLogger("NES")
logger = logging.getLogger("Client")

MM3_CURRENT_STAGE = 0x22
MM3_MEGAMAN_STATE = 0x30
MM3_PROG_STATE = 0x60
MM3_ROBOT_MASTERS_DEFEATED = 0x61
MM3_DOC_STATUS = 0x62
MM3_HEALTH = 0xA2
MM3_WEAPON_ENERGY = 0xA3
MM3_WEAPONS = {
    1: 1,
    2: 3,
    3: 0,
    4: 2,
    5: 4,
    6: 5,
    7: 7,
    8: 9,
    0x11: 6,
    0x12: 8,
    0x13: 10,
}

MM3_DOC_REMAP = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: 6,
    5: 7,
    6: 4,
    7: 5
}
MM3_LIVES = 0xAE
MM3_E_TANKS = 0xAF
MM3_ENERGY_BAR = 0xB2
MM3_CONSUMABLES = 0x150
MM3_ROBOT_MASTERS_UNLOCKED = 0x680
MM3_DOC_ROBOT_UNLOCKED = 0x681
MM3_ENERGYLINK = 0x682
MM3_LAST_WILY = 0x683
MM3_RBM_STROBE = 0x684
MM3_SFX_QUEUE = 0x685
MM3_DOC_ROBOT_DEFEATED = 0x686
MM3_COMPLETED_STAGES = 0x687
MM3_RECEIVED_ITEMS = 0x688
MM3_RUSH_RECEIVED = 0x689

MM3_CONSUMABLE_TABLE: dict[int, dict[int, tuple[int, int]]] = {
    # Stage:
    #   Item: (byte offset, bit mask)
    0: {
        0x0200: (0, 5),
        0x0201: (3, 2),
    },
    1: {
        0x0202: (2, 6),
        0x0203: (2, 5),
        0x0204: (2, 4),
        0x0205: (2, 3),
        0x0206: (3, 6),
        0x0207: (3, 5),
        0x0208: (3, 7),
        0x0209: (4, 0)
    },
    2: {
        0x020A: (2, 7),
        0x020B: (3, 0),
        0x020C: (3, 1),
        0x020D: (3, 2),
        0x020E: (4, 2),
        0x020F: (4, 3),
        0x0210: (4, 7),
        0x0211: (5, 1),
        0x0212: (6, 1),
        0x0213: (7, 0)
    },
    3: {
        0x0214: (0, 6),
        0x0215: (1, 5),
        0x0216: (2, 3),
        0x0217: (2, 7),
        0x0218: (2, 6),
        0x0219: (2, 5),
        0x021A: (4, 5),
    },
    4: {
        0x021B: (1, 3),
        0x021C: (1, 5),
        0x021D: (1, 7),
        0x021E: (2, 0),
        0x021F: (1, 6),
        0x0220: (2, 4),
        0x0221: (2, 5),
        0x0222: (4, 5)
    },
    5: {
        0x0223: (3, 0),
        0x0224: (3, 2),
        0x0225: (4, 5),
        0x0226: (4, 6),
        0x0227: (6, 4),
    },
    6: {
        0x0228: (2, 0),
        0x0229: (2, 1),
        0x022A: (3, 1),
        0x022B: (3, 2),
        0x022C: (3, 3),
        0x022D: (3, 4),
    },
    7: {
        0x022E: (3, 5),
        0x022F: (3, 4),
        0x0230: (3, 3),
        0x0231: (3, 2),
    },
    8: {
        0x0232: (1, 4),
        0x0233: (2, 1),
        0x0234: (2, 2),
        0x0235: (2, 5),
        0x0236: (3, 5),
        0x0237: (4, 2),
        0x0238: (4, 4),
        0x0239: (5, 3),
        0x023A: (6, 0),
        0x023B: (6, 1),
        0x023C: (7, 5),

    },
    9: {
        0x023D: (3, 2),
        0x023E: (3, 6),
        0x023F: (4, 5),
        0x0240: (5, 4),
    },
    10: {
        0x0241: (0, 2),
        0x0242: (2, 4)
    },
    11: {
        0x0243: (4, 1),
        0x0244: (6, 0),
        0x0245: (6, 1),
        0x0246: (6, 2),
        0x0247: (6, 3),
    },
    12: {
        0x0248: (0, 0),
        0x0249: (0, 3),
        0x024A: (0, 5),
        0x024B: (1, 6),
        0x024C: (2, 7),
        0x024D: (2, 3),
        0x024E: (2, 1),
        0x024F: (2, 2),
        0x0250: (3, 5),
        0x0251: (3, 4),
        0x0252: (3, 6),
        0x0253: (3, 7)
    },
    13: {
        0x0254: (0, 3),
        0x0255: (0, 6),
        0x0256: (1, 0),
        0x0257: (3, 0),
        0x0258: (3, 2),
        0x0259: (3, 3),
        0x025A: (3, 4),
        0x025B: (3, 5),
        0x025C: (3, 6),
        0x025D: (4, 0),
        0x025E: (3, 7),
        0x025F: (4, 1),
        0x0260: (4, 2),
    },
    14: {
        0x0261: (0, 3),
        0x0262: (0, 2),
        0x0263: (0, 6),
        0x0264: (1, 2),
        0x0265: (1, 7),
        0x0266: (2, 0),
        0x0267: (2, 1),
        0x0268: (2, 2),
        0x0269: (2, 3),
        0x026A: (5, 2),
        0x026B: (5, 3),
    },
    15: {
        0x026C: (0, 0),
        0x026D: (0, 1),
        0x026E: (0, 2),
        0x026F: (0, 3),
        0x0270: (0, 4),
        0x0271: (0, 6),
        0x0272: (1, 0),
        0x0273: (1, 2),
        0x0274: (1, 3),
        0x0275: (1, 1),
        0x0276: (0, 7),
        0x0277: (3, 2),
        0x0278: (2, 2),
        0x0279: (2, 3),
        0x027A: (2, 4),
        0x027B: (2, 5),
        0x027C: (3, 1),
        0x027D: (3, 0),
        0x027E: (2, 7),
        0x027F: (2, 6),
    },
    16: {
        0x0280: (0, 0),
        0x0281: (0, 3),
        0x0282: (0, 1),
        0x0283: (0, 2),
    },
    17: {
        0x0284: (0, 2),
        0x0285: (0, 6),
        0x0286: (0, 1),
        0x0287: (0, 5),
        0x0288: (0, 3),
        0x0289: (0, 0),
        0x028A: (0, 4)
    }
}


def to_oneup_format(val: int) -> int:
    return ((val // 10) * 0x10) + val % 10


def from_oneup_format(val: int) -> int:
    return ((val // 0x10) * 10) + val % 0x10


class MM3EnergyLinkType(IntEnum):
    Life = 0
    NeedleCannon = 1
    MagnetMissile = 2
    GeminiLaser = 3
    HardKnuckle = 4
    TopSpin = 5
    SearchSnake = 6
    SparkShot = 7
    ShadowBlade = 8
    OneUP = 12
    RushCoil = 0x11
    RushMarine = 0x12
    RushJet = 0x13


request_to_name: dict[str, str] = {
    "HP": "health",
    "NE": "Needle Cannon energy",
    "MA": "Magnet Missile energy",
    "GE": "Gemini Laser energy",
    "HA": "Hard Knuckle energy",
    "TO": "Top Spin energy",
    "SN": "Search Snake energy",
    "SP": "Spark Shot energy",
    "SH": "Shadow Blade energy",
    "RC": "Rush Coil energy",
    "RM": "Rush Marine energy",
    "RJ": "Rush Jet energy",
    "1U": "lives"
}

HP_EXCHANGE_RATE = 500000000
WEAPON_EXCHANGE_RATE = 250000000
ONEUP_EXCHANGE_RATE = 14000000000


def cmd_pool(self: "BizHawkClientCommandProcessor") -> None:
    """Check the current pool of EnergyLink, and requestable refills from it."""
    if self.ctx.game != "Mega Man 3":
        logger.warning("This command can only be used when playing Mega Man 3.")
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
    """Request a refill from EnergyLink."""
    from worlds._bizhawk.context import BizHawkClientContext
    if self.ctx.game != "Mega Man 3":
        logger.warning("This command can only be used when playing Mega Man 3.")
        return
    if not self.ctx.server or not self.ctx.slot:
        logger.warning("You must be connected to a server to use this command.")
        return
    valid_targets: dict[str, MM3EnergyLinkType] = {
        "HP": MM3EnergyLinkType.Life,
        "NE": MM3EnergyLinkType.NeedleCannon,
        "MA": MM3EnergyLinkType.MagnetMissile,
        "GE": MM3EnergyLinkType.GeminiLaser,
        "HA": MM3EnergyLinkType.HardKnuckle,
        "TO": MM3EnergyLinkType.TopSpin,
        "SN": MM3EnergyLinkType.SearchSnake,
        "SP": MM3EnergyLinkType.SparkShot,
        "SH": MM3EnergyLinkType.ShadowBlade,
        "RC": MM3EnergyLinkType.RushCoil,
        "RM": MM3EnergyLinkType.RushMarine,
        "RJ": MM3EnergyLinkType.RushJet,
        "1U": MM3EnergyLinkType.OneUP
    }
    if target.upper() not in valid_targets:
        logger.warning(f"Unrecognized target {target.upper()}. Available targets: {', '.join(valid_targets.keys())}")
        return
    ctx = self.ctx
    assert isinstance(ctx, BizHawkClientContext)
    client = ctx.client_handler
    assert isinstance(client, MegaMan3Client)
    client.refill_queue.append((valid_targets[target.upper()], int(amount)))
    logger.info(f"Restoring {amount} {request_to_name[target.upper()]}.")


def cmd_autoheal(self: "BizHawkClientCommandProcessor") -> None:
    """Enable auto heal from EnergyLink."""
    if self.ctx.game != "Mega Man 3":
        logger.warning("This command can only be used when playing Mega Man 3.")
        return
    if not self.ctx.server or not self.ctx.slot:
        logger.warning("You must be connected to a server to use this command.")
        return
    else:
        assert isinstance(self.ctx.client_handler, MegaMan3Client)
        if self.ctx.client_handler.auto_heal:
            self.ctx.client_handler.auto_heal = False
            logger.info(f"Auto healing disabled.")
        else:
            self.ctx.client_handler.auto_heal = True
            logger.info(f"Auto healing enabled.")


def get_sfx_writes(sfx: int) -> tuple[int, bytes, str]:
    return MM3_SFX_QUEUE, sfx.to_bytes(1, 'little'), "RAM"


class MegaMan3Client(BizHawkClient):
    game = "Mega Man 3"
    system = "NES"
    patch_suffix = ".apmm3"
    item_queue: list[NetworkItem] = []
    pending_death_link: bool = False
    # default to true, as we don't want to send a deathlink until Mega Man's HP is initialized once
    sending_death_link: bool = True
    death_link: bool = False
    energy_link: bool = False
    rom: bytes | None = None
    weapon_energy: int = 0
    health_energy: int = 0
    auto_heal: bool = False
    refill_queue: list[tuple[MM3EnergyLinkType, int]] = []
    last_wily: int | None = None  # default to wily 1
    doc_status: int | None = None  # default to no doc progress

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from worlds._bizhawk import RequestFailedError, read, get_memory_size
        from . import MM3World

        try:

            if (await get_memory_size(ctx.bizhawk_ctx, "PRG ROM")) < 0x3FFB0:
                # not the entire size, but enough to check validation
                if "pool" in ctx.command_processor.commands:
                    ctx.command_processor.commands.pop("pool")
                if "request" in ctx.command_processor.commands:
                    ctx.command_processor.commands.pop("request")
                if "autoheal" in ctx.command_processor.commands:
                    ctx.command_processor.commands.pop("autoheal")
                return False

            game_name, version = (await read(ctx.bizhawk_ctx, [(0x3F320, 21, "PRG ROM"),
                                                               (0x3F33C, 3, "PRG ROM")]))
            if game_name[:3] != b"MM3" or version != bytes(MM3World.world_version):
                if game_name[:3] == b"MM3":
                    # I think this is an easier check than the other?
                    older_version = f"{version[0]}.{version[1]}.{version[2]}"
                    logger.warning(f"This Mega Man 3 patch was generated for an different version of the apworld. "
                                   f"Please use that version to connect instead.\n"
                                   f"Patch version: ({older_version})\n"
                                   f"Client version: ({'.'.join([str(i) for i in MM3World.world_version])})")
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
        deathlink = (await read(ctx.bizhawk_ctx, [(0x3F336, 1, "PRG ROM")]))[0][0]
        if deathlink & 0x01:
            self.death_link = True
            await ctx.update_death_link(self.death_link)
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

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict[str, Any]) -> None:
        if cmd == "Bounced":
            if "tags" in args:
                assert ctx.slot is not None
                if "DeathLink" in args["tags"] and args["data"]["source"] != ctx.slot_info[ctx.slot].name:
                    self.on_deathlink(ctx)
        elif cmd == "Retrieved":
            if f"MM3_LAST_WILY_{ctx.team}_{ctx.slot}" in args["keys"]:
                self.last_wily = args["keys"][f"MM3_LAST_WILY_{ctx.team}_{ctx.slot}"]
            if f"MM3_DOC_STATUS_{ctx.team}_{ctx.slot}" in args["keys"]:
                self.doc_status = args["keys"][f"MM3_DOC_STATUS_{ctx.team}_{ctx.slot}"]
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
        (prog_state, robot_masters_unlocked, robot_masters_defeated, doc_status, doc_robo_unlocked, doc_robo_defeated,
         rush_acquired, received_items, completed_stages, consumable_checks,
            e_tanks, lives, weapon_energy, health, state, bar_state, current_stage,
            energy_link_packet, last_wily) = await read(ctx.bizhawk_ctx, [
                (MM3_PROG_STATE, 1, "RAM"),
                (MM3_ROBOT_MASTERS_UNLOCKED, 1, "RAM"),
                (MM3_ROBOT_MASTERS_DEFEATED, 1, "RAM"),
                (MM3_DOC_STATUS, 1, "RAM"),
                (MM3_DOC_ROBOT_UNLOCKED, 1, "RAM"),
                (MM3_DOC_ROBOT_DEFEATED, 1, "RAM"),
                (MM3_RUSH_RECEIVED, 1, "RAM"),
                (MM3_RECEIVED_ITEMS, 1, "RAM"),
                (MM3_COMPLETED_STAGES, 0x1, "RAM"),
                (MM3_CONSUMABLES, 16, "RAM"),  # Could be more but 16 definitely catches all current
                (MM3_E_TANKS, 1, "RAM"),
                (MM3_LIVES, 1, "RAM"),
                (MM3_WEAPON_ENERGY, 11, "RAM"),
                (MM3_HEALTH, 1, "RAM"),
                (MM3_MEGAMAN_STATE, 1, "RAM"),
                (MM3_ENERGY_BAR, 2, "RAM"),
                (MM3_CURRENT_STAGE, 1, "RAM"),
                (MM3_ENERGYLINK, 1, "RAM"),
                (MM3_LAST_WILY, 1, "RAM"),
            ])

        if bar_state[0] not in (0x00, 0x80):
            return  # Game is not initialized
            # Bit of a trick here, bar state can only be 0x00 or 0x80 (display health bar, or don't)
            # This means it can double as init guard and in-stage tracker

        if not ctx.finished_game and completed_stages[0] & 0x20:
            await ctx.send_msgs([{
                "cmd": "StatusUpdate",
                "status": ClientStatus.CLIENT_GOAL
            }])
        writes = []

        # deathlink
        # only handle deathlink in bar state 0x80 (in stage)
        if bar_state[0] == 0x80:
            if self.pending_death_link:
                writes.append((MM3_MEGAMAN_STATE, bytes([0x0E]), "RAM"))
                self.pending_death_link = False
                self.sending_death_link = True
            if "DeathLink" in ctx.tags and ctx.last_death_link + 1 < time.time():
                if state[0] == 0x0E and not self.sending_death_link:
                    await self.send_deathlink(ctx)
                elif state[0] != 0x0E:
                    self.sending_death_link = False

        if self.last_wily != last_wily[0]:
            if self.last_wily is None:
                # revalidate last wily from data storage
                await ctx.send_msgs([{"cmd": "Set", "key": f"MM3_LAST_WILY_{ctx.team}_{ctx.slot}", "operations": [
                    {"operation": "default", "value": 0xC}
                ]}])
                await ctx.send_msgs([{"cmd": "Get", "keys": [f"MM3_LAST_WILY_{ctx.team}_{ctx.slot}"]}])
            elif last_wily[0] == 0:
                writes.append((MM3_LAST_WILY, self.last_wily.to_bytes(1, "little"), "RAM"))
            else:
                # correct our setting
                self.last_wily = last_wily[0]
                await ctx.send_msgs([{"cmd": "Set", "key": f"MM3_LAST_WILY_{ctx.team}_{ctx.slot}", "operations": [
                    {"operation": "replace", "value": self.last_wily}
                ]}])

        if self.doc_status != doc_status[0]:
            if self.doc_status is None:
                # revalidate doc status from data storage
                await ctx.send_msgs([{"cmd": "Set", "key": f"MM3_DOC_STATUS_{ctx.team}_{ctx.slot}", "operations": [
                    {"operation": "default", "value": 0}
                ]}])
                await ctx.send_msgs([{"cmd": "Get", "keys": [f"MM3_DOC_STATUS_{ctx.team}_{ctx.slot}"]}])
            elif doc_status[0] == 0:
                writes.append((MM3_DOC_STATUS, self.doc_status.to_bytes(1, "little"), "RAM"))
            else:
                # correct our setting
                # shouldn't be possible to desync, but we'll account for it anyways
                self.doc_status |= doc_status[0]
                await ctx.send_msgs([{"cmd": "Set", "key": f"MM3_DOC_STATUS_{ctx.team}_{ctx.slot}", "operations": [
                    {"operation": "replace", "value": self.doc_status}
                ]}])

        weapon_energy = bytearray(weapon_energy)
        # handle receiving items
        recv_amount = received_items[0]
        if recv_amount < len(ctx.items_received):
            item = ctx.items_received[recv_amount]
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(ctx.item_names.lookup_in_slot(item.item), 'red', 'bold'),
                color(ctx.player_names[item.player], 'yellow'),
                ctx.location_names.lookup_in_slot(item.location, item.player), recv_amount, len(ctx.items_received)))

            if item.item & 0x120 == 0:
                # Robot Master Weapon, or Rush
                new_weapons = item.item & 0xFF
                weapon_energy[MM3_WEAPONS[new_weapons]] |= 0x9C
                writes.append((MM3_WEAPON_ENERGY, weapon_energy, "RAM"))
                writes.append(get_sfx_writes(0x32))
            elif item.item & 0x20 == 0:
                # Robot Master Stage Access
                # Catch the Doc Robo here
                if item.item & 0x10:
                    ptr = MM3_DOC_ROBOT_UNLOCKED
                    unlocked = doc_robo_unlocked
                else:
                    ptr = MM3_ROBOT_MASTERS_UNLOCKED
                    unlocked = robot_masters_unlocked
                new_stages = unlocked[0] | (1 << ((item.item & 0xF) - 1))
                print(new_stages)
                writes.append((ptr, new_stages.to_bytes(1, 'little'), "RAM"))
                writes.append(get_sfx_writes(0x34))
                writes.append((MM3_RBM_STROBE, b"\x01", "RAM"))
            else:
                # append to the queue, so we handle it later
                self.item_queue.append(item)
            recv_amount += 1
            writes.append((MM3_RECEIVED_ITEMS, recv_amount.to_bytes(1, 'little'), "RAM"))

        if energy_link_packet[0]:
            pickup = energy_link_packet[0]
            if pickup in (0x64, 0x65):
                # Health pickups
                if pickup == 0x65:
                    value = 2
                else:
                    value = 10
                exchange_rate = HP_EXCHANGE_RATE
            elif pickup in (0x66, 0x67):
                # Weapon Energy
                if pickup == 0x67:
                    value = 2
                else:
                    value = 10
                exchange_rate = WEAPON_EXCHANGE_RATE
            elif pickup == 0x69:
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
            writes.append((MM3_ENERGYLINK, 0x00.to_bytes(1, "little"), "RAM"))

        if self.weapon_energy:
            # Weapon Energy
            # We parse the whole thing to spread it as thin as possible
            current_energy = self.weapon_energy
            for i, weapon in zip(range(len(weapon_energy)), weapon_energy):
                if weapon & 0x80 and (weapon & 0x7F) < 0x1C:
                    missing = 0x1C - (weapon & 0x7F)
                    if missing > self.weapon_energy:
                        missing = self.weapon_energy
                    self.weapon_energy -= missing
                    weapon_energy[i] = weapon + missing
                    if not self.weapon_energy:
                        writes.append((MM3_WEAPON_ENERGY, weapon_energy, "RAM"))
                        break
            else:
                if current_energy != self.weapon_energy:
                    writes.append((MM3_WEAPON_ENERGY, weapon_energy, "RAM"))

        if self.health_energy or self.auto_heal:
            # Health Energy
            # We save this if the player has not taken any damage
            current_health = health[0]
            if 0 < (current_health & 0x7F) < 0x1C:
                health_diff = 0x1C - (current_health & 0x7F)
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
                writes.append((MM3_HEALTH, current_health.to_bytes(1, 'little'), "RAM"))

        if self.refill_queue:
            refill_type, refill_amount = self.refill_queue.pop()
            if refill_type == MM3EnergyLinkType.Life:
                exchange_rate = HP_EXCHANGE_RATE
            elif refill_type == MM3EnergyLinkType.OneUP:
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
                if refill_type == MM3EnergyLinkType.Life:
                    refill_ptr = MM3_HEALTH
                elif refill_type == MM3EnergyLinkType.OneUP:
                    refill_ptr = MM3_LIVES
                else:
                    refill_ptr = MM3_WEAPON_ENERGY + MM3_WEAPONS[refill_type]
                current_value = (await read(ctx.bizhawk_ctx, [(refill_ptr, 1, "RAM")]))[0][0]
                if refill_type == MM3EnergyLinkType.OneUP:
                    current_value = from_oneup_format(current_value)
                new_value = min(0x9C if refill_type != MM3EnergyLinkType.OneUP else 99, current_value + refill_amount)
                if refill_type == MM3EnergyLinkType.OneUP:
                    new_value = to_oneup_format(new_value)
                writes.append((refill_ptr, new_value.to_bytes(1, "little"), "RAM"))

        if len(self.item_queue):
            item = self.item_queue.pop(0)
            idx = item.item & 0xF
            if idx == 0:
                # 1-Up
                current_lives = from_oneup_format(lives[0])
                if current_lives > 99:
                    self.item_queue.append(item)
                else:
                    current_lives += 1
                    current_lives = to_oneup_format(current_lives)
                    writes.append((MM3_LIVES, current_lives.to_bytes(1, 'little'), "RAM"))
                    writes.append(get_sfx_writes(0x14))
            elif idx == 1:
                self.weapon_energy += 0xE
                writes.append(get_sfx_writes(0x1C))
            elif idx == 2:
                self.health_energy += 0xE
                writes.append(get_sfx_writes(0x1C))
            elif idx == 3:
                current_tanks = from_oneup_format(e_tanks[0])
                if current_tanks > 99:
                    self.item_queue.append(item)
                else:
                    current_tanks += 1
                    current_tanks = to_oneup_format(current_tanks)
                    writes.append((MM3_E_TANKS, current_tanks.to_bytes(1, 'little'), "RAM"))
                    writes.append(get_sfx_writes(0x14))

        await write(ctx.bizhawk_ctx, writes)

        new_checks = []
        # check for locations
        for i in range(8):
            flag = 1 << i
            if robot_masters_defeated[0] & flag:
                rbm_id = 0x0001 + i
                if rbm_id not in ctx.checked_locations:
                    new_checks.append(rbm_id)
                wep_id = 0x0101 + i
                if wep_id not in ctx.checked_locations:
                    new_checks.append(wep_id)
            if doc_robo_defeated[0] & flag:
                doc_id = 0x0010 + MM3_DOC_REMAP[i]
                if doc_id not in ctx.checked_locations:
                    new_checks.append(doc_id)

        for i in range(2):
            flag = 1 << i
            if rush_acquired[0] & flag:
                itm_id = 0x0111 + i
                if itm_id not in ctx.checked_locations:
                    new_checks.append(itm_id)

        for i in (0, 1, 2, 4):
            # Wily 4 does not have a boss check
            boss_id = 0x0009 + i
            if completed_stages[0] & (1 << i) != 0:
                if boss_id not in ctx.checked_locations:
                    new_checks.append(boss_id)
        
        if completed_stages[0] & 0x80 and 0x000F not in ctx.checked_locations:
            new_checks.append(0x000F)

        if bar_state[0] == 0x80:  # currently in stage
            if (prog_state[0] > 0x00 and current_stage[0] >= 8) or prog_state[0] == 0x00:
                # need to block the specific state of Break Man prog=0x12 stage=0x5
                # it doesn't clean the consumable table and he doesn't have any anyways
                for consumable in MM3_CONSUMABLE_TABLE[current_stage[0]]:
                    consumable_info = MM3_CONSUMABLE_TABLE[current_stage[0]][consumable]
                    if consumable not in ctx.checked_locations:
                        is_checked = consumable_checks[consumable_info[0]] & (1 << consumable_info[1])
                        if is_checked:
                            new_checks.append(consumable)

        for new_check_id in new_checks:
            ctx.locations_checked.add(new_check_id)
            location = ctx.location_names.lookup_in_game(new_check_id)
            nes_logger.info(
                f'New Check: {location} ({len(ctx.locations_checked)}/'
                f'{len(ctx.missing_locations) + len(ctx.checked_locations)})')
            await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [new_check_id]}])
