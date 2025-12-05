import base64
import logging
import time

from NetUtils import ClientStatus
from worlds._bizhawk.client import BizHawkClient
from worlds._bizhawk import read, write, guarded_write

from .locations import location_data

logger = logging.getLogger("Client")

BANK_EXCHANGE_RATE = 50000000

DATA_LOCATIONS = {
    "ItemIndex": (0x1A6E, 0x02),
    "Deathlink": (0x00FD, 0x01),
    "APItem": (0x00FF, 0x01),
    "EventFlag": (0x1735, 0x140),
    "Missable": (0x161A, 0x20),
    "Hidden": (0x16DE, 0x0E),
    "Rod": (0x1716, 0x01),
    "DexSanityFlag": (0x1A71, 19),
    "GameStatus": (0x1A84, 0x01),
    "Money": (0x141F, 3),
    "CurrentMap": (0x1436, 1),
    "ResetCheck": (0x0100, 4),
    # First and second Vermilion Gym trash can selection. Second is not used, so should always be 0.
    # First should never be above 0x0F. This is just before Event Flags.
    "CrashCheck1": (0x1731, 2),
    # Unused, should always be 0. This is just before Missables flags.
    "CrashCheck2": (0x1617, 1),
    # Progressive keys, should never be above 10. Just before Dexsanity flags.
    "CrashCheck3": (0x1A70, 1),
    # Route 18 Gate script value. Should never be above 3. Just before Hidden items flags.
    "CrashCheck4": (0x16DD, 1),
}

TRACKER_EVENT_FLAGS = [
    0x77, # EVENT_BEAT_BROCK
    0xbf, # EVENT_BEAT_MISTY
    0x167, # EVENT_BEAT_LT_SURGE
    0x1a9, # EVENT_BEAT_ERIKA
    0x259, # EVENT_BEAT_KOGA
    0x361, # EVENT_BEAT_SABRINA
    0x299, # EVENT_BEAT_BLAINE
    0x51, # EVENT_BEAT_VIRIDIAN_GYM_GIOVANNI

    0x38, # EVENT_OAK_GOT_PARCEL
    0x525, # EVENT_BEAT_ROUTE22_RIVAL_1ST_BATTLE
    0x117, # EVENT_RESCUED_MR_FUJI
    0x55c, # EVENT_GOT_SS_TICKET
    0x78f, # EVENT_BEAT_SILPH_CO_GIOVANNI
    0x901, # EVENT_BEAT_CHAMPION_RIVAL
]

assert len(TRACKER_EVENT_FLAGS) <= 32

location_map = {"Rod": {}, "EventFlag": {}, "Missable": {}, "Hidden": {}, "list": {}, "DexSanityFlag": {}}
location_bytes_bits = {}
for location in location_data:
    if location.ram_address is not None:
        if type(location.ram_address) == list:
            location_map[type(location.ram_address).__name__][(location.ram_address[0].flag, location.ram_address[1].flag)] = location.address
            location_bytes_bits[location.address] = [{'byte': location.ram_address[0].byte, 'bit': location.ram_address[0].bit},
                                                     {'byte': location.ram_address[1].byte, 'bit': location.ram_address[1].bit}]
        else:
            location_map[type(location.ram_address).__name__][location.ram_address.flag] = location.address
            location_bytes_bits[location.address] = {'byte': location.ram_address.byte, 'bit': location.ram_address.bit}

location_name_to_id = {location.name: location.address for location in location_data if location.type == "Item"
                       and location.address is not None}


class PokemonRBClient(BizHawkClient):
    system = ("GB", "SGB")
    patch_suffix = (".apred", ".apblue")
    game = "Pokemon Red and Blue"

    def __init__(self):
        super().__init__()
        self.auto_hints = set()
        self.locations_array = None
        self.tracker_bitfield = 0
        self.disconnect_pending = False
        self.set_deathlink = False
        self.banking_command = None
        self.game_state = False
        self.last_death_link = 0
        self.current_map = 0

    async def validate_rom(self, ctx):
        game_name = await read(ctx.bizhawk_ctx, [(0x134, 12, "ROM")])
        game_name = game_name[0].decode("ascii")
        if game_name in ("POKEMON RED\00", "POKEMON BLUE"):
            ctx.game = self.game
            ctx.items_handling = 0b001
            ctx.command_processor.commands["bank"] = cmd_bank
            seed_name = await read(ctx.bizhawk_ctx, [(0xFFDB, 21, "ROM")])
            ctx.seed_name = seed_name[0].split(b"\0")[0].decode("ascii")
            self.set_deathlink = False
            self.banking_command = None
            self.locations_array = None
            self.disconnect_pending = False
            return True
        return False

    async def set_auth(self, ctx):
        auth_name = await read(ctx.bizhawk_ctx, [(0xFFC6, 21, "ROM")])
        if auth_name[0] == bytes([0] * 21):
            # rom was patched before rom names implemented, use player name
            auth_name = await read(ctx.bizhawk_ctx, [(0xFFF0, 16, "ROM")])
            auth_name = auth_name[0].decode("ascii").split("\x00")[0]
        else:
            auth_name = base64.b64encode(auth_name[0]).decode()
        ctx.auth = auth_name

    async def game_watcher(self, ctx):
        if not ctx.server or not ctx.server.socket.open or ctx.server.socket.closed:
            return

        data = await read(ctx.bizhawk_ctx, [(loc_data[0], loc_data[1], "WRAM")
                                            for loc_data in DATA_LOCATIONS.values()])
        data = {data_set_name: data_name for data_set_name, data_name in zip(DATA_LOCATIONS.keys(), data)}

        if self.set_deathlink:
            self.set_deathlink = False
            await ctx.update_death_link(True)

        if self.disconnect_pending:
            self.disconnect_pending = False
            await ctx.disconnect()

        if data["GameStatus"][0] == 0 or data["ResetCheck"] == b'\xff\xff\xff\x7f':
            # Do not handle anything before game save is loaded
            self.game_state = False
            return
        elif (data["GameStatus"][0] not in (0x2A, 0xAC)
              or data["CrashCheck1"][0] & 0xF0 or data["CrashCheck1"][1] & 0xFF
              or data["CrashCheck2"][0]
              or data["CrashCheck3"][0] > 10
              or data["CrashCheck4"][0] > 3):
            # Should mean game crashed
            logger.warning("Pokémon Red/Blue game may have crashed. Disconnecting from server.")
            self.game_state = False
            await ctx.disconnect()
            return
        self.game_state = True

        # SEND ITEMS TO CLIENT

        if data["APItem"][0] == 0:
            item_index = int.from_bytes(data["ItemIndex"], "little")
            if len(ctx.items_received) > item_index:
                item_code = ctx.items_received[item_index].item
                if item_code > 255:
                    item_code -= 256
                await write(ctx.bizhawk_ctx, [(DATA_LOCATIONS["APItem"][0],
                                               [item_code], "WRAM")])

        # LOCATION CHECKS

        locations = set()

        for flag_type, loc_map in location_map.items():
            for flag, loc_id in loc_map.items():
                if flag_type == "list":
                    if (data["EventFlag"][location_bytes_bits[loc_id][0]['byte']] & 1 <<
                            location_bytes_bits[loc_id][0]['bit']
                            and data["Missable"][location_bytes_bits[loc_id][1]['byte']] & 1 <<
                            location_bytes_bits[loc_id][1]['bit']):
                        locations.add(loc_id)
                elif data[flag_type][location_bytes_bits[loc_id]['byte']] & 1 << location_bytes_bits[loc_id]['bit']:
                    locations.add(loc_id)

        if locations != self.locations_array:
            if locations:
                self.locations_array = locations
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": list(locations)}])

        # AUTO HINTS

        hints = []
        if data["EventFlag"][280] & 16:
            hints.append("Cerulean Bicycle Shop")
        if data["EventFlag"][280] & 32:
            hints.append("Route 2 Gate - Oak's Aide")
        if data["EventFlag"][280] & 64:
            hints.append("Route 11 Gate 2F - Oak's Aide")
        if data["EventFlag"][280] & 128:
            hints.append("Route 15 Gate 2F - Oak's Aide")
        if data["EventFlag"][281] & 1:
            hints += ["Celadon Prize Corner - Item Prize 1", "Celadon Prize Corner - Item Prize 2",
                      "Celadon Prize Corner - Item Prize 3"]
        if (location_name_to_id["Fossil - Choice A"] in ctx.checked_locations and location_name_to_id[
            "Fossil - Choice B"]
                not in ctx.checked_locations):
            hints.append("Fossil - Choice B")
        elif (location_name_to_id["Fossil - Choice B"] in ctx.checked_locations and location_name_to_id[
            "Fossil - Choice A"]
              not in ctx.checked_locations):
            hints.append("Fossil - Choice A")
        hints = [
            location_name_to_id[loc] for loc in hints if location_name_to_id[loc] not in self.auto_hints and
                                                         location_name_to_id[loc] in ctx.missing_locations and
                                                         location_name_to_id[loc] not in ctx.locations_checked
        ]
        if hints:
            await ctx.send_msgs([{"cmd": "LocationScouts", "locations": hints, "create_as_hint": 2}])
        self.auto_hints.update(hints)

        # DEATHLINK

        if "DeathLink" in ctx.tags:
            if data["Deathlink"][0] == 3:
                await ctx.send_death(ctx.player_names[ctx.slot] + " is out of usable Pokémon! "
                                     + ctx.player_names[ctx.slot] + " blacked out!")
                await write(ctx.bizhawk_ctx, [(DATA_LOCATIONS["Deathlink"][0], [0], "WRAM")])
                self.last_death_link = ctx.last_death_link
            elif ctx.last_death_link > self.last_death_link:
                self.last_death_link = ctx.last_death_link
                await write(ctx.bizhawk_ctx, [(DATA_LOCATIONS["Deathlink"][0], [1], "WRAM")])

        # BANK

        if self.banking_command:
            original_money = data["Money"]
            # Money is stored as binary-coded decimal.
            money = int(original_money.hex())
            if self.banking_command > money:
                logger.warning(f"You do not have ${self.banking_command} to deposit!")
            elif (-self.banking_command * BANK_EXCHANGE_RATE) > (ctx.stored_data[f"EnergyLink{ctx.team}"] or 0):
                logger.warning("Not enough money in the EnergyLink storage!")
            else:
                if self.banking_command + money > 999999:
                    self.banking_command = 999999 - money
                money = str(money - self.banking_command).zfill(6)
                money = [int(money[:2], 16), int(money[2:4], 16), int(money[4:], 16)]
                money_written = await guarded_write(ctx.bizhawk_ctx, [(0x141F, money, "WRAM")],
                                                    [(0x141F, original_money, "WRAM")])
                if money_written:
                    if self.banking_command >= 0:
                        deposit = self.banking_command - int(self.banking_command / 4)
                        tax = self.banking_command - deposit
                        logger.info(f"Deposited ${deposit}, and charged a tax of ${tax}.")
                        self.banking_command = deposit
                    else:
                        logger.info(f"Withdrew ${-self.banking_command}.")
                    await ctx.send_msgs([{
                        "cmd": "Set", "key": f"EnergyLink{ctx.team}", "operations":
                            [{"operation": "add", "value": self.banking_command * BANK_EXCHANGE_RATE},
                             {"operation": "max", "value": 0}],
                    }])
            self.banking_command = None

        if data["CurrentMap"][0] != self.current_map:
            await ctx.send_msgs([{"cmd": "Bounce", "slots": [ctx.slot], "data": {"currentMap": data["CurrentMap"][0]}}])
            self.current_map = data["CurrentMap"][0]

        # TRACKER
        tracker_bitfield = 0
        for i, flag in enumerate(TRACKER_EVENT_FLAGS):
            if data["EventFlag"][flag // 8] & (1 << (flag % 8)):
                tracker_bitfield |= 1 << i

        if tracker_bitfield != self.tracker_bitfield:
            await ctx.send_msgs([{
                "cmd": "Set",
                "key": f"pokemon_rb_events_{ctx.team}_{ctx.slot}",
                "default": 0,
                "want_reply": False,
                "operations": [{"operation": "or", "value": tracker_bitfield}],
            }])
            self.tracker_bitfield = tracker_bitfield

        # VICTORY

        if data["EventFlag"][280] & 1 and not ctx.finished_game:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True

    def on_package(self, ctx, cmd, args):
        if cmd == 'Connected':
            if 'death_link' in args['slot_data'] and args['slot_data']['death_link']:
                self.set_deathlink = True
                self.last_death_link = time.time()
            ctx.set_notify(f"EnergyLink{ctx.team}")
        elif cmd == 'RoomInfo':
            if ctx.seed_name and ctx.seed_name != args["seed_name"]:
                # CommonClient's on_package displays an error to the user in this case, but connection is not cancelled.
                self.game_state = False
                self.disconnect_pending = True
        super().on_package(ctx, cmd, args)


def cmd_bank(self, cmd: str = "", amount: str = ""):
    """Deposit or withdraw money with the server's EnergyLink storage.
    /bank - check server balance.
    /bank deposit # - deposit money. One quarter of the amount will be lost to taxation.
    /bank withdraw # - withdraw money."""
    if self.ctx.game != "Pokemon Red and Blue":
        logger.warning("This command can only be used while playing Pokémon Red and Blue")
        return
    if (not self.ctx.server) or self.ctx.server.socket.closed or not self.ctx.client_handler.game_state:
        logger.info(f"Must be connected to server and in game.")
        return
    elif not cmd:
        logger.info(f"Money available: {int((self.ctx.stored_data[f'EnergyLink{self.ctx.team}'] or 0) / BANK_EXCHANGE_RATE)}")
        return
    elif not amount:
        logger.warning("You must specify an amount.")
    elif cmd == "withdraw":
        self.ctx.client_handler.banking_command = -int(amount)
    elif cmd == "deposit":
        if int(amount) < 4:
            logger.warning("You must deposit at least $4, for tax purposes.")
            return
        self.ctx.client_handler.banking_command = int(amount)
    else:
        logger.warning(f"Invalid bank command {cmd}")
        return
