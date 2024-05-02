import io
import json
import random

from . import Data
from typing import TYPE_CHECKING, Optional
from BaseClasses import Item, Location
from settings import get_settings
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension
from .Items import item_table
from .Locations import shop, badge, pants, location_table, hidden, all_locations

if TYPE_CHECKING:
    from . import MLSSWorld

colors = [
    Data.redHat,
    Data.greenHat,
    Data.blueHat,
    Data.azureHat,
    Data.yellowHat,
    Data.orangeHat,
    Data.purpleHat,
    Data.pinkHat,
    Data.blackHat,
    Data.whiteHat,
    Data.silhouetteHat,
    Data.chaosHat,
    Data.truechaosHat
]

pants = [
    Data.vanilla,
    Data.redPants,
    Data.greenPants,
    Data.bluePants,
    Data.azurePants,
    Data.yellowPants,
    Data.orangePants,
    Data.purplePants,
    Data.pinkPants,
    Data.blackPants,
    Data.whitePants,
    Data.chaosPants
]


def get_base_rom_as_bytes() -> bytes:
    with open(get_settings().mlss_options.rom_file, "rb") as infile:
        base_rom_bytes = bytes(infile.read())
    return base_rom_bytes


class MLSSPatchExtension(APPatchExtension):
    game = "Mario & Luigi Superstar Saga"

    @staticmethod
    def randomize_music(caller: APProcedurePatch, rom: bytes):
        options = json.loads(caller.get_file("options.json").decode("UTF-8"))
        if options["music_options"] != 1:
            return rom
        stream = io.BytesIO(rom)
        random.seed(options["seed"] + options["player"])

        songs = []
        stream.seek(0x21CB74)
        for _ in range(50):
            if stream.tell() == 0x21CBD8:
                stream.seek(4, 1)
                continue
            temp = stream.read(4)
            songs.append(temp)

        random.shuffle(songs)
        stream.seek(0x21CB74)
        for _ in range(50):
            if stream.tell() == 0x21CBD8:
                stream.seek(4, 1)
                continue
            stream.write(songs.pop())

        return stream.getvalue()

    @staticmethod
    def hidden_visible(caller: APProcedurePatch, rom: bytes):
        options = json.loads(caller.get_file("options.json").decode("UTF-8"))
        if options["block_visibility"] == 0:
            return rom
        stream = io.BytesIO(rom)

        for location in all_locations:
            stream.seek(location.id - 6)
            b = stream.read(1)
            if b[0] == 0x10 and options["block_visibility"] == 1:
                stream.seek(location.id - 6)
                stream.write(bytes([0x0]))
            if b[0] == 0x0 and options["block_visibility"] == 2:
                stream.seek(location.id - 6)
                stream.write(bytes([0x10]))

        return stream.getvalue()

    @staticmethod
    def randomize_sounds(caller: APProcedurePatch, rom: bytes):
        options = json.loads(caller.get_file("options.json").decode("UTF-8"))
        if options["randomize_sounds"] != 1:
            return rom
        stream = io.BytesIO(rom)
        random.seed(options["seed"] + options["player"])
        fresh_pointers = Data.sounds
        pointers = Data.sounds

        random.shuffle(pointers)
        stream.seek(0x21CC44, 0)
        for i in range(354):
            current_position = stream.tell()
            value = int.from_bytes(stream.read(3), "little")
            if value in fresh_pointers:
                stream.seek(current_position)
                stream.write(pointers.pop().to_bytes(3, "little"))
            stream.seek(1, 1)

        return stream.getvalue()

    @staticmethod
    def enemy_randomize(caller: APProcedurePatch, rom: bytes):
        options = json.loads(caller.get_file("options.json").decode("UTF-8"))
        if options["randomize_bosses"] == 0 and options["randomize_enemies"] == 0:
            return rom

        enemies = [pos for pos in Data.enemies if pos not in Data.bowsers] if options["castle_skip"] else Data.enemies
        bosses = [pos for pos in Data.bosses if pos not in Data.bowsers] if options["castle_skip"] else Data.bosses
        stream = io.BytesIO(rom)
        random.seed(options["seed"] + options["player"])

        if options["randomize_bosses"] == 1 or (options["randomize_bosses"] == 2) and options["randomize_enemies"] == 0:
            raw = []
            for pos in bosses:
                stream.seek(pos + 1)
                raw += [stream.read(0x1F)]
            random.shuffle(raw)
            for pos in bosses:
                stream.seek(pos + 1)
                stream.write(raw.pop())

        if options["randomize_enemies"] == 1:
            raw = []
            for pos in enemies:
                stream.seek(pos + 1)
                raw += [stream.read(0x1F)]
            if options["randomize_bosses"] == 2:
                for pos in bosses:
                    stream.seek(pos + 1)
                    raw += [stream.read(0x1F)]
            random.shuffle(raw)
            for pos in enemies:
                stream.seek(pos + 1)
                stream.write(raw.pop())
            if options["randomize_bosses"] == 2:
                for pos in bosses:
                    stream.seek(pos + 1)
                    stream.write(raw.pop())
            return stream.getvalue()

        enemies_raw = []
        groups = []

        if options["randomize_enemies"] == 0:
            return stream.getvalue()

        if options["randomize_bosses"] == 2:
            for pos in bosses:
                stream.seek(pos + 1)
                groups += [stream.read(0x1F)]

        for pos in enemies:
            stream.seek(pos + 8)
            for _ in range(6):
                enemy = int.from_bytes(stream.read(1))
                if enemy > 0:
                    stream.seek(1, 1)
                    flag = int.from_bytes(stream.read(1))
                    if flag == 0x7:
                        break
                    if flag in [0x0, 0x2, 0x4]:
                        if enemy not in Data.pestnut and enemy not in Data.flying:
                            enemies_raw += [enemy]
                    stream.seek(1, 1)
                else:
                    stream.seek(3, 1)

        random.shuffle(enemies_raw)
        chomp = False
        for pos in enemies:
            stream.seek(pos + 8)

            for _ in range(6):
                enemy = int.from_bytes(stream.read(1))
                if enemy > 0 and enemy not in Data.flying and enemy not in Data.pestnut:
                    if enemy == 0x52:
                        chomp = True
                    stream.seek(1, 1)
                    flag = int.from_bytes(stream.read(1))
                    if flag not in [0x0, 0x2, 0x4]:
                        stream.seek(1, 1)
                        continue
                    stream.seek(-3, 1)
                    stream.write(bytes([enemies_raw.pop()]))
                    stream.seek(1, 1)
                    stream.write(bytes([0x6]))
                    stream.seek(1, 1)
                else:
                    stream.seek(3, 1)

            stream.seek(pos + 1)
            raw = stream.read(0x1F)
            if chomp:
                raw = raw[0:3] + bytes([0x67, 0xAB, 0x28, 0x08]) + raw[7:]
            else:
                raw = raw[0:3] + bytes([0xEE, 0x2C, 0x28, 0x08]) + raw[7:]
            groups += [raw]
            chomp = False

        random.shuffle(groups)
        arr = enemies
        if options["randomize_bosses"] == 2:
            arr += bosses

        for pos in arr:
            stream.seek(pos + 1)
            stream.write(groups.pop())

        return stream.getvalue()


class MLSSProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Mario & Luigi Superstar Saga"
    hash = "4b1a5897d89d9e74ec7f630eefdfd435"
    patch_file_ending = ".apmlss"
    result_file_ending = ".gba"

    procedure = [
        ("apply_bsdiff4", ["base_patch.bsdiff4"]),
        ("apply_tokens", ["token_data.bin"]),
        ("enemy_randomize", []),
        ("hidden_visible", []),
        ("randomize_sounds", []),
        ("randomize_music", []),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()


def write_tokens(world: "MLSSWorld", patch: MLSSProcedurePatch) -> None:
    options_dict = {
        "randomize_enemies": world.options.randomize_enemies.value,
        "randomize_bosses": world.options.randomize_bosses.value,
        "castle_skip": world.options.castle_skip.value,
        "randomize_sounds": world.options.randomize_sounds.value,
        "music_options": world.options.music_options.value,
        "block_visibility": world.options.block_visibility.value,
        "seed": world.multiworld.seed,
        "player": world.player,
    }
    patch.write_file("options.json", json.dumps(options_dict).encode("UTF-8"))

    # Bake player name into ROM
    patch.write_token(APTokenTypes.WRITE, 0xDF0000, world.multiworld.player_name[world.player].encode("UTF-8"))

    # Bake seed name into ROM
    patch.write_token(APTokenTypes.WRITE, 0xDF00A0, world.multiworld.seed_name.encode("UTF-8"))

    # Bake patch into header
    patch.write_token(APTokenTypes.WRITE, 0xAD, "P".encode("UTF-8"))

    # Intro Skip
    patch.write_token(
        APTokenTypes.WRITE,
        0x244D08,
        bytes([0x88, 0x0, 0x19, 0x91, 0x1, 0x20, 0x58, 0x1, 0xF, 0xA0, 0x3, 0x15, 0x27, 0x8]),
    )

    # Patch S.S Chuckola Loading Zones
    patch.write_token(APTokenTypes.WRITE, 0x25FD4E, bytes([0x48, 0x30, 0x80, 0x60, 0x50, 0x2, 0xF]))

    patch.write_token(APTokenTypes.WRITE, 0x25FD83, bytes([0x48, 0x30, 0x80, 0x60, 0xC0, 0x2, 0xF]))

    patch.write_token(APTokenTypes.WRITE, 0x25FDB8, bytes([0x48, 0x30, 0x05, 0x80, 0xE4, 0x0, 0xF]))

    patch.write_token(APTokenTypes.WRITE, 0x25FDED, bytes([0x48, 0x30, 0x06, 0x80, 0xE4, 0x0, 0xF]))

    patch.write_token(APTokenTypes.WRITE, 0x25FE22, bytes([0x48, 0x30, 0x07, 0x80, 0xE4, 0x0, 0xF]))

    patch.write_token(APTokenTypes.WRITE, 0x25FE57, bytes([0x48, 0x30, 0x08, 0x80, 0xE4, 0x0, 0xF]))

    if world.options.extra_pipes:
        patch.write_token(APTokenTypes.WRITE, 0xD00001, bytes([0x1]))

    if world.options.castle_skip:
        patch.write_token(APTokenTypes.WRITE, 0x3AEAB0, bytes([0xC1, 0x67, 0x0, 0x6, 0x1C, 0x08, 0x3]))
        patch.write_token(APTokenTypes.WRITE, 0x3AEC18, bytes([0x89, 0x65, 0x0, 0xE, 0xA, 0x08, 0x1]))

    if world.options.skip_minecart:
        patch.write_token(APTokenTypes.WRITE, 0x3AC728, bytes([0x89, 0x13, 0x0, 0x10, 0xF, 0x08, 0x1]))
        patch.write_token(APTokenTypes.WRITE, 0x3AC56C, bytes([0x49, 0x16, 0x0, 0x8, 0x8, 0x08, 0x1]))

    if world.options.scale_stats:
        patch.write_token(APTokenTypes.WRITE, 0xD00002, bytes([0x1]))

    if world.options.xp_multiplier:
        patch.write_token(APTokenTypes.WRITE, 0xD00003, bytes([world.options.xp_multiplier.value]))

    if world.options.tattle_hp:
        patch.write_token(APTokenTypes.WRITE, 0xD00000, bytes([0x1]))

    if world.options.music_options == 2:
        patch.write_token(APTokenTypes.WRITE, 0x19B118, bytes([0x0, 0x25]))

    if world.options.randomize_backgrounds:
        all_enemies = Data.enemies + Data.bosses
        for address in all_enemies:
            patch.write_token(APTokenTypes.WRITE, address + 3, bytes([world.random.randint(0x0, 0x26)]))

    for location_name in location_table.keys():
        if (
            (world.options.skip_minecart and "Minecart" in location_name and "After" not in location_name)
            or (world.options.castle_skip and "Bowser" in location_name)
            or (world.options.disable_surf and "Surf Minigame" in location_name)
            or (world.options.harhalls_pants and "Harhall's" in location_name)
        ):
            continue
        if (world.options.chuckle_beans == 0 and "Digspot" in location_name) or (
            world.options.chuckle_beans == 1 and location_table[location_name] in hidden
        ):
            continue
        if not world.options.coins and "Coin" in location_name:
            continue
        location = world.multiworld.get_location(location_name, world.player)
        item = location.item
        address = [address for address in all_locations if address.name == location.name]
        item_inject(world, patch, location.address, address[0].itemType, item)
        if "Shop" in location_name and "Coffee" not in location_name and item.player != world.player:
            desc_inject(world, patch, location, item)

    swap_colors(world, patch, world.options.mario_pants.value, 0, True)
    swap_colors(world, patch, world.options.luigi_pants.value, 1, True)
    swap_colors(world, patch, world.options.mario_color.value, 0)
    swap_colors(world, patch, world.options.luigi_color.value, 1)

    patch.write_file("token_data.bin", patch.get_token_binary())


def swap_colors(world: "MLSSWorld", patch: MLSSProcedurePatch, color: int, bro: int,
                pants_option: Optional[bool] = False):
    if not pants_option and color == bro:
        return
    chaos = False
    if not pants_option and color == 11 or color == 12:
        chaos = True
    if pants_option and color == 11:
        chaos = True
    for c in [c for c in (pants[color] if pants_option else colors[color])
              if (c[3] == bro if not chaos else c[1] == bro)]:
        if chaos:
            patch.write_token(APTokenTypes.WRITE, c[0],
                              bytes([world.random.randint(0, 255), world.random.randint(0, 127)]))
        else:
            patch.write_token(APTokenTypes.WRITE, c[0], bytes([c[1], c[2]]))


def item_inject(world: "MLSSWorld", patch: MLSSProcedurePatch, location: int, item_type: int, item: Item):
    if item.player == world.player:
        code = item_table[item.name].itemID
    else:
        code = 0x3F
    if item_type == 0:
        patch.write_token(APTokenTypes.WRITE, location, bytes([code]))
    elif item_type == 1:
        if code == 0x1D or code == 0x1E:
            code += 0xE
        if 0x20 <= code <= 0x26:
            code -= 0x4
        insert = int(code)
        insert2 = insert % 0x10
        insert2 *= 0x10
        insert //= 0x10
        insert += 0x20
        patch.write_token(APTokenTypes.WRITE, location, bytes([insert, insert2]))
    elif item_type == 2:
        if code == 0x1D or code == 0x1E:
            code += 0xE
        if 0x20 <= code <= 0x26:
            code -= 0x4
        patch.write_token(APTokenTypes.WRITE, location, bytes([code]))
    elif item_type == 3:
        if code == 0x1D or code == 0x1E:
            code += 0xE
        if code < 0x1D:
            code -= 0xA
        if 0x20 <= code <= 0x26:
            code -= 0xE
        patch.write_token(APTokenTypes.WRITE, location, bytes([code]))
    else:
        patch.write_token(APTokenTypes.WRITE, location, bytes([0x18]))


def desc_inject(world: "MLSSWorld", patch: MLSSProcedurePatch, location: Location, item: Item):
    index = -1
    for key, value in shop.items():
        if location.address in value:
            if key == 0x3C05F0:
                index = value.index(location.address)
            else:
                index = value.index(location.address) + 14

    for key, value in badge.items():
        if index != -1:
            break
        if location.address in value:
            if key == 0x3C0618:
                index = value.index(location.address) + 24
            else:
                index = value.index(location.address) + 41

    for key, value in pants.items():
        if index != -1:
            break
        if location.address in value:
            if key == 0x3C0618:
                index = value.index(location.address) + 48
            else:
                index = value.index(location.address) + 66

    dstring = f"{world.multiworld.player_name[item.player]}: {item.name}"
    patch.write_token(APTokenTypes.WRITE, 0xD11000 + (index * 0x40), dstring.encode("UTF8"))
