import logging
import time
import typing
from logging import Logger
from typing import Dict

from NetUtils import ClientStatus, NetworkItem
from worlds.AutoSNIClient import SNIClient
from .Items import start_id as items_start_id
from .Locations import start_id as locations_start_id

if typing.TYPE_CHECKING:
    from SNIClient import SNIContext
else:
    SNIContext = typing.Any

snes_logger: Logger = logging.getLogger("SNES")

SRAM_START: int = 0xE00000
L2AC_ROMNAME_START: int = 0x007FC0
L2AC_SIGN_ADDR: int = SRAM_START + 0x2000
L2AC_GOAL_ADDR: int = SRAM_START + 0x2030
L2AC_DEATH_ADDR: int = SRAM_START + 0x203D
L2AC_TX_ADDR: int = SRAM_START + 0x2040
L2AC_RX_ADDR: int = SRAM_START + 0x2800

enemy_names: Dict[int, str] = {
    0x00: "a Goblin",
    0x01: "an Armor goblin",
    0x02: "a Regal Goblin",
    0x03: "a Goblin Mage",
    0x04: "a Troll",
    0x05: "an Ork",
    0x06: "a Fighter ork",
    0x07: "an Ork Mage",
    0x08: "a Lizardman",
    0x09: "a Skull Lizard",
    0x0A: "an Armour Dait",
    0x0B: "a Dragonian",
    0x0C: "a Cyclops",
    0x0D: "a Mega Cyclops",
    0x0E: "a Flame genie",
    0x0F: "a Well Genie",
    0x10: "a Wind Genie",
    0x11: "an Earth Genie",
    0x12: "a Cobalt",
    0x13: "a Merman",
    0x14: "an Aqualoi",
    0x15: "an Imp",
    0x16: "a Fiend",
    0x17: "an Archfiend",
    0x18: "a Hound",
    0x19: "a Doben",
    0x1A: "a Winger",
    0x1B: "a Serfaco",
    0x1C: "a Pug",
    0x1D: "a Salamander",
    0x1E: "a Brinz Lizard",
    0x1F: "a Seahorse",
    0x20: "a Seirein",
    0x21: "an Earth Viper",
    0x22: "a Gnome",
    0x23: "a Wispy",
    0x24: "a Thunderbeast",
    0x25: "a Lunar bear",
    0x26: "a Shadowfly",
    0x27: "a Shadow",
    0x28: "a Lion",
    0x29: "a Sphinx",
    0x2A: "a Mad horse",
    0x2B: "an Armor horse",
    0x2C: "a Buffalo",
    0x2D: "a Bruse",
    0x2E: "a Bat",
    0x2F: "a Big Bat",
    0x30: "a Red Bat",
    0x31: "an Eagle",
    0x32: "a Hawk",
    0x33: "a Crow",
    0x34: "a Baby Frog",
    0x35: "a King Frog",
    0x36: "a Lizard",
    0x37: "a Newt",
    0x38: "a Needle Lizard",
    0x39: "a Poison Lizard",
    0x3A: "a Medusa",
    0x3B: "a Ramia",
    0x3C: "a Basilisk",
    0x3D: "a Cokatoris",
    0x3E: "a Scorpion",
    0x3F: "an Antares",
    0x40: "a Small Crab",
    0x41: "a Big Crab",
    0x42: "a Red Lobster",
    0x43: "a Spider",
    0x44: "a Web Spider",
    0x45: "a Beetle",
    0x46: "a Poison Beetle",
    0x47: "a Mosquito",
    0x48: "a Coridras",
    0x49: "a Spinner",
    0x4A: "a Tartona",
    0x4B: "an Armour Nail",
    0x4C: "a Moth",
    0x4D: "a Mega  Moth",
    0x4E: "a Big Bee",
    0x4F: "a Dark Fly",
    0x50: "a Stinger",
    0x51: "an Armor Bee",
    0x52: "a Sentopez",
    0x53: "a Cancer",
    0x54: "a Garbost",
    0x55: "a Bolt Fish",
    0x56: "a Moray",
    0x57: "a She Viper",
    0x58: "an Angler fish",
    0x59: "a Unicorn",
    0x5A: "an Evil Shell",
    0x5B: "a Drill Shell",
    0x5C: "a Snell",
    0x5D: "an Ammonite",
    0x5E: "an Evil Fish",
    0x5F: "a Squid",
    0x60: "a Kraken",
    0x61: "a Killer Whale",
    0x62: "a White Whale",
    0x63: "a Grianos",
    0x64: "a Behemoth",
    0x65: "a Perch",
    0x66: "a Current",
    0x67: "a Vampire Rose",
    0x68: "a Desert Rose",
    0x69: "a Venus Fly",
    0x6A: "a Moray Vine",
    0x6B: "a Torrent",
    0x6C: "a Mad Ent",
    0x6D: "a Crow Kelp",
    0x6E: "a Red Plant",
    0x6F: "La Fleshia",
    0x70: "a Wheel Eel",
    0x71: "a Skeleton",
    0x72: "a Ghoul",
    0x73: "a Zombie",
    0x74: "a Specter",
    0x75: "a Dark Spirit",
    0x76: "a Snatcher",
    0x77: "a Jurahan",
    0x78: "a Demise",
    0x79: "a Leech",
    0x7A: "a Necromancer",
    0x7B: "a Hade Chariot",
    0x7C: "a Hades",
    0x7D: "a Dark Skull",
    0x7E: "a Hades Skull",
    0x7F: "a Mummy",
    0x80: "a Vampire",
    0x81: "a Nosferato",
    0x82: "a Ghost Ship",
    0x83: "a Deadly Sword",
    0x84: "a Deadly Armor",
    0x85: "a T Rex",
    0x86: "a Brokion",
    0x87: "a Pumpkin Head",
    0x88: "a Mad Head",
    0x89: "a Snow Gas",
    0x8A: "a Great Coca",
    0x8B: "a Gargoyle",
    0x8C: "a Rogue Shape",
    0x8D: "a Bone Gorem",
    0x8E: "a Nuborg",
    0x8F: "a Wood Gorem",
    0x90: "a Mad Gorem",
    0x91: "a Green Clay",
    0x92: "a Sand Gorem",
    0x93: "a Magma Gorem",
    0x94: "an Iron Gorem",
    0x95: "a Gold Gorem",
    0x96: "a Hidora",
    0x97: "a Sea Hidora",
    0x98: "a High Hidora",
    0x99: "a King Hidora",
    0x9A: "an Orky",
    0x9B: "a Waiban",
    0x9C: "a White Dragon",
    0x9D: "a Red Dragon",
    0x9E: "a Blue Dragon",
    0x9F: "a Green Dragon",
    0xA0: "a Black Dragon",
    0xA1: "a Copper Dragon",
    0xA2: "a Silver Dragon",
    0xA3: "a Gold Dragon",
    0xA4: "a Red Jelly",
    0xA5: "a Blue Jelly",
    0xA6: "a Bili Jelly",
    0xA7: "a Red Core",
    0xA8: "a Blue Core",
    0xA9: "a Green Core",
    0xAA: "a No Core",
    0xAB: "a Mimic",
    0xAC: "a Blue Mimic",
    0xAD: "an Ice Roge",
    0xAE: "a Mushroom",
    0xAF: "a Big Mushr'm",
    0xB0: "a Minataurus",
    0xB1: "a Gorgon",
    0xB2: "a Ninja",
    0xB3: "an Asashin",
    0xB4: "a Samurai",
    0xB5: "a Dark Warrior",
    0xB6: "an Ochi Warrior",
    0xB7: "a Sly Fox",
    0xB8: "a Tengu",
    0xB9: "a Warm Eye",
    0xBA: "a Wizard",
    0xBB: "a Dark Sum'ner",
    0xBC: "the Big Catfish",
    0xBD: "a Follower",
    0xBE: "the Tarantula",
    0xBF: "Pierre",
    0xC0: "Daniele",
    0xC1: "the Venge Ghost",
    0xC2: "the Fire Dragon",
    0xC3: "the Tank",
    0xC4: "Idura",
    0xC5: "Camu",
    0xC6: "Gades",
    0xC7: "Amon",
    0xC8: "Erim",
    0xC9: "Daos",
    0xCA: "a Lizard Man",
    0xCB: "a Goblin",
    0xCC: "a Skeleton",
    0xCD: "a Regal Goblin",
    0xCE: "a Goblin",
    0xCF: "a Goblin Mage",
    0xD0: "a Slave",
    0xD1: "a Follower",
    0xD2: "a Groupie",
    0xD3: "the Egg Dragon",
    0xD4: "a Mummy",
    0xD5: "a Troll",
    0xD6: "Gades",
    0xD7: "Idura",
    0xD8: "a Lion",
    0xD9: "the Rogue Flower",
    0xDA: "a Gargoyle",
    0xDB: "a Ghost Ship",
    0xDC: "Idura",
    0xDD: "a Soldier",
    0xDE: "Gades",
    0xDF: "the Master",
}


class L2ACSNIClient(SNIClient):
    game: str = "Lufia II Ancient Cave"

    async def validate_rom(self, ctx: SNIContext) -> bool:
        from SNIClient import snes_read

        rom_name: bytes = await snes_read(ctx, L2AC_ROMNAME_START, 0x15)
        if rom_name is None or rom_name[:4] != b"L2AC":
            return False

        ctx.game = self.game
        ctx.items_handling = 0b111  # fully remote

        ctx.rom = rom_name

        return True

    async def game_watcher(self, ctx: SNIContext) -> None:
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        rom: bytes = await snes_read(ctx, L2AC_ROMNAME_START, 0x15)
        if rom != ctx.rom:
            ctx.rom = None
            return

        if ctx.server is None or ctx.slot is None:
            # not successfully connected to a multiworld server, cannot process the game sending items
            return

        signature: bytes = await snes_read(ctx, L2AC_SIGN_ADDR, 16)
        if signature != b"ArchipelagoLufia":
            return

        # Goal
        if not ctx.finished_game:
            goal_data: bytes = await snes_read(ctx, L2AC_GOAL_ADDR, 10)
            if goal_data is not None and goal_data[goal_data[0]] == 0x01:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                ctx.finished_game = True

        # DeathLink TX
        death_data: bytes = await snes_read(ctx, L2AC_DEATH_ADDR, 3)
        if death_data is not None:
            await ctx.update_death_link(bool(death_data[0]))
            if death_data[1] != 0x00:
                snes_buffered_write(ctx, L2AC_DEATH_ADDR + 1, b"\x00")
                if "DeathLink" in ctx.tags and ctx.last_death_link + 1 < time.time():
                    player_name: str = ctx.player_names.get(ctx.slot, str(ctx.slot))
                    enemy_name: str = enemy_names.get(death_data[1] - 1, hex(death_data[1] - 1))
                    await ctx.send_death(f"{player_name} was totally defeated by {enemy_name}.")

        # TX
        tx_data: bytes = await snes_read(ctx, L2AC_TX_ADDR, 8)
        if tx_data is not None:
            snes_items_sent = int.from_bytes(tx_data[:2], "little")
            client_items_sent = int.from_bytes(tx_data[2:4], "little")
            client_ap_items_found = int.from_bytes(tx_data[4:6], "little")

            if client_items_sent < snes_items_sent:
                location_id: int = locations_start_id + client_items_sent
                location: str = ctx.location_names[location_id]
                client_items_sent += 1

                ctx.locations_checked.add(location_id)
                await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [location_id]}])

                snes_logger.info("New Check: %s (%d/%d)" % (
                    location,
                    len(ctx.locations_checked),
                    len(ctx.missing_locations) + len(ctx.checked_locations)))
                snes_buffered_write(ctx, L2AC_TX_ADDR + 2, client_items_sent.to_bytes(2, "little"))

            ap_items_found: int = sum(net_item.player != ctx.slot for net_item in ctx.locations_info.values())
            if client_ap_items_found < ap_items_found:
                snes_buffered_write(ctx, L2AC_TX_ADDR + 4, ap_items_found.to_bytes(2, "little"))

        # RX
        rx_data: bytes = await snes_read(ctx, L2AC_RX_ADDR, 4)
        if rx_data is not None:
            snes_items_received = int.from_bytes(rx_data[:2], "little")

            if snes_items_received < len(ctx.items_received):
                item: NetworkItem = ctx.items_received[snes_items_received]
                item_code: int = item.item - items_start_id
                snes_items_received += 1

                snes_logger.info("Received %s from %s (%s) (%d/%d in list)" % (
                    ctx.item_names[item.item],
                    ctx.player_names[item.player],
                    ctx.location_names[item.location],
                    snes_items_received, len(ctx.items_received)))
                snes_buffered_write(ctx, L2AC_RX_ADDR + 2 * (snes_items_received + 1), item_code.to_bytes(2, 'little'))
                snes_buffered_write(ctx, L2AC_RX_ADDR, snes_items_received.to_bytes(2, "little"))

        await snes_flush_writes(ctx)

    async def deathlink_kill_player(self, ctx: SNIContext) -> None:
        from SNIClient import DeathState, snes_buffered_write, snes_flush_writes

        # DeathLink RX
        if "DeathLink" in ctx.tags and ctx.last_death_link + 1 < time.time():
            snes_buffered_write(ctx, L2AC_DEATH_ADDR + 2, b"\x01")
        else:
            snes_buffered_write(ctx, L2AC_DEATH_ADDR + 2, b"\x00")
        await snes_flush_writes(ctx)
        ctx.death_state = DeathState.dead
