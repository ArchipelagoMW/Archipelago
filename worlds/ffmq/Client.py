
from NetUtils import ClientStatus, color
from worlds.AutoSNIClient import SNIClient
from .Regions import offset
import logging

snes_logger = logging.getLogger("SNES")

ROM_NAME = (0x7FC0, 0x7FD4 + 1 - 0x7FC0)

READ_DATA_START = 0xF50EA8
READ_DATA_END = 0xF50FE7 + 1

GAME_FLAGS = (0xF50EA8, 64)
COMPLETED_GAME = (0xF50F22, 1)
BATTLEFIELD_DATA = (0xF50FD4, 20)

RECEIVED_DATA = (0xE01FF0, 3)

ITEM_CODE_START = 0x420000

IN_GAME_FLAG = (4 * 8) + 2

NPC_CHECKS = {
    4325676: ((6 * 8) + 4, False),  # Old Man Level Forest
    4325677: ((3 * 8) + 6, True),  # Kaeli Level Forest
    4325678: ((25 * 8) + 1, True),  # Tristam
    4325680: ((26 * 8) + 0, True),  # Aquaria Vendor Girl
    4325681: ((29 * 8) + 2, True),  # Phoebe Wintry Cave
    4325682: ((25 * 8) + 6, False),  # Mysterious Man (Life Temple)
    4325683: ((29 * 8) + 3, True),  # Reuben Mine
    4325684: ((29 * 8) + 7, True),  # Spencer
    4325685: ((29 * 8) + 6, False),  # Venus Chest
    4325686: ((29 * 8) + 1, True),  # Fireburg Tristam
    4325687: ((26 * 8) + 1, True),  # Fireburg Vendor Girl
    4325688: ((14 * 8) + 4, True),  # MegaGrenade Dude
    4325689: ((29 * 8) + 5, False),  # Tristam's Chest
    4325690: ((29 * 8) + 4, True),  # Arion
    4325691: ((29 * 8) + 0, True),  # Windia Kaeli
    4325692: ((26 * 8) + 2, True),  # Windia Vendor Girl

}


def get_flag(data, flag):
    byte = int(flag / 8)
    bit = int(0x80 / (2 ** (flag % 8)))
    return (data[byte] & bit) > 0

def validate_read_state(data1, data2):
    validation_array = bytes([0x01, 0x46, 0x46, 0x4D, 0x51, 0x52])

    if data1 is None or data2 is None:
        return False
    for i in range(6):
        if data1[i] != validation_array[i] or data2[i] != validation_array[i]:
            return False;
    return True
    
   

class FFMQClient(SNIClient):
    game = "Final Fantasy Mystic Quest"

    async def validate_rom(self, ctx):
        from SNIClient import snes_read
        rom_name = await snes_read(ctx, *ROM_NAME)
        if rom_name is None:
            return False
        if rom_name[:2] != b"MQ":
            return False

        ctx.rom = rom_name
        ctx.game = self.game
        ctx.items_handling = 0b001
        return True

    async def game_watcher(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        check_1 = await snes_read(ctx, 0xF53749, 6)
        received = await snes_read(ctx, RECEIVED_DATA[0], RECEIVED_DATA[1])
        data = await snes_read(ctx, READ_DATA_START, READ_DATA_END - READ_DATA_START)
        check_2 = await snes_read(ctx, 0xF53749, 6)
        if not validate_read_state(check_1, check_2):
            return

        def get_range(data_range):
            return data[data_range[0] - READ_DATA_START:data_range[0] + data_range[1] - READ_DATA_START]
        completed_game = get_range(COMPLETED_GAME)
        battlefield_data = get_range(BATTLEFIELD_DATA)
        game_flags = get_range(GAME_FLAGS)

        if game_flags is None:
            return
        if not get_flag(game_flags, IN_GAME_FLAG):
            return

        if not ctx.finished_game:
            if completed_game[0] & 0x80 and game_flags[30] & 0x18:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                ctx.finished_game = True

        old_locations_checked = ctx.locations_checked.copy()

        for container in range(256):
            if get_flag(game_flags, (0x20 * 8) + container):
                ctx.locations_checked.add(offset["Chest"] + container)

        for location, data in NPC_CHECKS.items():
            if get_flag(game_flags, data[0]) is data[1]:
                ctx.locations_checked.add(location)

        for battlefield in range(20):
            if battlefield_data[battlefield] == 0:
                ctx.locations_checked.add(offset["BattlefieldItem"] + battlefield + 1)

        if old_locations_checked != ctx.locations_checked:
            await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": ctx.locations_checked}])

        if received[0] == 0:
            received_index = int.from_bytes(received[1:], "big")
            if received_index < len(ctx.items_received):
                item = ctx.items_received[received_index]
                received_index += 1
                code = (item.item - ITEM_CODE_START) + 1
                if code > 256:
                    code -= 256
                snes_buffered_write(ctx, RECEIVED_DATA[0], bytes([code, *received_index.to_bytes(2, "big")]))
        await snes_flush_writes(ctx)
