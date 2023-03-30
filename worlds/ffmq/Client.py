
from NetUtils import ClientStatus, color
from worlds.AutoSNIClient import SNIClient
from .Regions import offset
import logging

snes_logger = logging.getLogger("SNES")

ROM_NAME = (0x7FC0, 0x7FD4 + 1 - 0x7FC0)
GAME_FLAGS = (0xF50EA8, 0xF50EE7 + 1 - 0xF50EA8)
COMPLETED_GAME = (0xF50F22, 1)
BATTLEFIELD_DATA = (0xF50FD4, 0xF50FE7 + 1 - 0xF50FD4)
RECEIVED_DATA = (0xF50FD0, 3)

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


# def get_bit(data, bit):
#     byte = int(bit / 8)
#     return (data[byte] & (1 << (bit - (byte * 8)))) > 0

def get_flag(data, flag):
    byte = int(flag / 8)
    bit = int(0x80 / (2 ** (flag % 8)))
    return (data[byte] & bit) > 0


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
        ctx.items_handling = 0b101
        return True

    async def game_watcher(self, ctx):

        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        #container_flags = await snes_read(ctx, *CONTAINER_FLAGS)
        received = await snes_read(ctx, *RECEIVED_DATA)
        completed_game = await snes_read(ctx, *COMPLETED_GAME)
        battlefield_data = await snes_read(ctx, *BATTLEFIELD_DATA)
        game_flags = await snes_read(ctx, *GAME_FLAGS)
        if game_flags is None:
            return
        if not get_flag(game_flags, IN_GAME_FLAG):
            return

        if not ctx.finished_game:
                if completed_game[0] & 0x80:
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    ctx.finished_game = True

        old_locations_checked = ctx.locations_checked.copy()

        for container in range(248):
            if get_flag(game_flags, (0x20 * 8) + container): #game_flags[byte] & bit:
                ctx.locations_checked.add(offset["Chest"] + container)

        for location, data in NPC_CHECKS.items():
            if get_flag(game_flags, data[0]) is data[1]:
                ctx.locations_checked.add(location)

        for battlefield in range(20):
            if battlefield_data[battlefield] == 0:
                ctx.locations_checked.add(offset["Battlefield"] + battlefield + 1)


        # for box in range(201):
        #     byte = int(box/8) + 5
        #     bit = int(0x80/(2 ** (box % 8)))
        #     if game_flags[byte] & bit:
        #         ctx.locations_checked.add(offset["Box"] + box)

        if old_locations_checked != ctx.locations_checked:
            await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": ctx.locations_checked}])

        if received[0] == 0:
            received_index = (received[2] * 256) + received[1]
            if received_index < len(ctx.items_received):
                item = ctx.items_received[received_index]
                received_index += 1
                # logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                #     color(ctx.item_names[item.item], 'red', 'bold'),
                #     color(ctx.player_names[item.player], 'yellow'),
                #     ctx.location_names[item.location], received_index, len(ctx.items_received)))
                code = (item.item - ITEM_CODE_START) + 1
                if code > 256:
                    code -= 256
                snes_buffered_write(ctx, RECEIVED_DATA[0], bytes([code]))
        await snes_flush_writes(ctx)

    # async def server_auth(self, password_requested: bool = False) -> None:
    #     if password_requested and not self.password:
    #         await ctx.server_auth(password_requested)
    #     if self.rom is None:
    #         self.awaiting_rom = True
    #         snes_logger.info(
    #             "No ROM detected, awaiting snes connection to authenticate to the multiworld server (/snes)")
    #         return
    #     self.awaiting_rom = False
    #     # TODO: This looks kind of hacky...
    #     # Context.auth is meant to be the "name" parameter in send_connect,
    #     # which has to be a str (bytes is not json serializable).
    #     # But here, Context.auth is being used for something else
    #     # (where it has to be bytes because it is compared with rom elsewhere).
    #     # If we need to save something to compare with rom elsewhere,
    #     # it should probably be in a different variable,
    #     # and let auth be used for what it's meant for.
    #     #self.auth = self.rom
    #     #auth = base64.b64encode(self.rom).decode()
    #     await self.send_connect(name="FFMQPlayer")
