import io
import os
import pkgutil
import typing
import bsdiff4

from BaseClasses import Item, Location
from worlds.AutoWorld import World
from settings import get_settings
from worlds.Files import APDeltaPatch
from .Enemies import enemies, bosses, EnemyRandomize, Enemy, EnemyGroup
from .Items import item_table
from .Locations import shop, badge, pants

if typing.TYPE_CHECKING:
    from . import MLSSWorld


class Color:
    def __init__(self, location, byte1, byte2, bro):
        self.location = location
        self.byte1 = byte1
        self.byte2 = byte2
        self.bro = bro


colors = [
    "Red",
    "Green",
    "Blue",
    "Cyan",
    "Yellow",
    "Orange",
    "Purple",
    "Pink",
    "Black",
    "White",
    "Silhouette",
    "Chaos",
    "TrueChaos"
]

cpants = [
    "Vanilla",
    "Red",
    "Green",
    "Blue",
    "Cyan",
    "Yellow",
    "Orange",
    "Purple",
    "Pink",
    "Black",
    "White",
    "Chaos"
]


def get_base_rom_as_bytes() -> bytes:
    with open(get_settings().mlss_options.rom_file, "rb") as infile:
        base_rom_bytes = bytes(infile.read())
    return base_rom_bytes


class MLSSDeltaPatch(APDeltaPatch):
    game = "Mario & Luigi Superstar Saga"
    hash = "4b1a5897d89d9e74ec7f630eefdfd435"
    patch_file_ending = ".apmlss"
    result_file_ending = ".gba"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()


class Rom:
    hash = "4b1a5897d89d9e74ec7f630eefdfd435"

    def __init__(self, world: "MLSSWorld"):
        content = get_base_rom_as_bytes()
        patched = self.apply_delta(content)
        self.random = world.multiworld.per_slot_randoms[world.player]
        self.stream = io.BytesIO(patched)
        self.world = world
        self.player = world.player

    def swap_colors(self, color, bro):
        temp = pkgutil.get_data(__name__, "colors/" + color + ".txt")
        temp_io = io.BytesIO(temp)
        color_arr = []

        for lines in temp_io.readlines():

            arr = lines.decode('utf-8').strip().split(',')
            if color != "Chaos" and color != "TrueChaos":
                color_arr.append(Color(int(arr[0], 16), int(arr[1], 16), int(arr[2], 16), int(arr[3], 16)))
            else:
                color_arr.append(
                    Color(int(arr[0], 16), self.random.randint(0, 255), self.random.randint(0, 127), int(arr[1], 16)))

        colors_ = [c for c in color_arr if c.bro == bro]

        for c in colors_:
            self.stream.seek(c.location, io.SEEK_SET)
            self.stream.write(bytes([c.byte1, c.byte2]))

    def swap_pants(self, color, bro):
        mario_color = self.world.options.mario_color
        luigi_color = self.world.options.luigi_color
        if bro == 0 and (colors[mario_color] == "TrueChaos" or colors[mario_color] == "Silhouette"):
            return
        if bro == 1 and (colors[luigi_color] == "TrueChaos" or colors[luigi_color] == "Silhouette"):
            return
        if color == "Vanilla":
            return
        temp = pkgutil.get_data(__name__, "colors/pants/" + color + ".txt")
        temp_io = io.BytesIO(temp)
        color_arr = []

        for lines in temp_io.readlines():
            arr = lines.decode('utf-8').strip().split(',')
            if color != "Chaos" and color != "TrueChaos":
                color_arr.append(Color(int(arr[0], 16), int(arr[1], 16), int(arr[2], 16), int(arr[3], 16)))
            else:
                color_arr.append(
                    Color(int(arr[0], 16), self.random.randint(0, 255), self.random.randint(0, 127), int(arr[1], 16)))

        colors_ = [c for c in color_arr if c.bro == bro]

        for c in colors_:
            self.stream.seek(c.location, io.SEEK_SET)
            self.stream.write(bytes([c.byte1, c.byte2]))

    def item_inject(self, location: int, item_type: int, item: Item):
        if item.player == self.player:
            code = item_table[item.name].itemID
        else:
            code = 0x3F
        if item_type == 0:
            self.stream.seek(location, 0)
            self.stream.write(bytes([code]))
            self.stream.seek(location - 6, 0)
            b = self.stream.read(1)
            if b[0] == 0x10 and self.world.options.hidden_visible:
                self.stream.seek(location - 6, 0)
                self.stream.write(bytes([0x0]))
            if b[0] == 0x0 and self.world.options.blocks_invisible:
                self.stream.seek(location - 6, 0)
                self.stream.write(bytes([0x10]))
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
            self.stream.seek(location, 0)
            self.stream.write(bytes([insert, insert2]))
        elif item_type == 2:
            if code == 0x1D or code == 0x1E:
                code += 0xE
            if 0x20 <= code <= 0x26:
                code -= 0x4
            self.stream.seek(location, 0)
            self.stream.write(bytes([code]))
        elif item_type == 3:
            if code == 0x1D or code == 0x1E:
                code += 0xE
            if code < 0x1D:
                code -= 0xA
            if 0x20 <= code <= 0x26:
                code -= 0xE
            self.stream.seek(location, 0)
            self.stream.write(bytes([code]))
        else:
            self.stream.seek(location, 0)
            self.stream.write(bytes([0x18]))

    def patch_options(self):
        name = self.world.multiworld.player_name[self.player].encode("UTF-8")
        self.stream.seek(0xDF0000, 0)
        self.stream.write(name)
        self.stream.seek(0xDF00A0, 0)
        self.stream.write(self.world.multiworld.seed_name.encode("UTF-8"))

        if self.world.options.skip_intro:
            # Enable Skip Intro in ROM
            self.stream.seek(0x244D08, 0)
            self.stream.write(bytes([0x88, 0x0, 0x19, 0x91, 0x1, 0x20, 0x58, 0x1, 0xF, 0xA0, 0x3, 0x15, 0x27, 0x8]))

        if self.world.options.extra_pipes:
            # Spawn in extra pipes in ROM
            self.stream.seek(0xD00001, 0)
            self.stream.write(bytes([0x1]))

        if self.world.options.castle_skip:
            # Enable Bowser's castle skip in ROM
            self.stream.seek(0x3AEAB0, 0)
            self.stream.write(bytes([0xC1, 0x67, 0x0, 0x6, 0x1C, 0x08, 0x3]))
            self.stream.seek(0x3AEC18, 0)
            self.stream.write(bytes([0x89, 0x65, 0x0, 0xE, 0xA, 0x08, 0x1]))

        if self.world.options.skip_minecart:
            # Enable minecart skip in ROM
            self.stream.seek(0x3AC728, 0)
            self.stream.write(bytes([0x89, 0x13, 0x0, 0x10, 0xF, 0x08, 0x1]))
            self.stream.seek(0x3AC56C, 0)
            self.stream.write(bytes([0x49, 0x16, 0x0, 0x8, 0x8, 0x08, 0x1]))

        if self.world.options.randomize_sounds:
            self.randomize_sounds()

        if self.world.options.music_options == 1:
            self.randomize_music()

        if self.world.options.music_options == 2:
            self.disable_music()

        if self.world.options.randomize_backgrounds:
            self.randomize_backgrounds()

        if self.world.options.randomize_enemies or self.world.options.randomize_bosses:
            self.enemy_randomize()

        if self.world.options.scale_stats:
            self.stream.seek(0x1E9418, 0)
            self.stream.write(bytes([0x1]))

        if self.world.options.scale_pow:
            self.stream.seek(0x1E9419, 0)
            self.stream.write(bytes([0x1]))

        if self.world.options.tattle_hp:
            self.stream.seek(0xD00000, 0)
            self.stream.write(bytes([0x1]))

        self.stream.seek(0x25FD4E, 0)
        self.stream.write(bytes([0x48, 0x30, 0x80, 0x60, 0x50, 0x2, 0xF]))
        self.stream.seek(0x25FD83, 0)
        self.stream.write(bytes([0x48, 0x30, 0x80, 0x60, 0xC0, 0x2, 0xF]))
        self.stream.seek(0x25FDB8, 0)
        self.stream.write(bytes([0x48, 0x30, 0x05, 0x80, 0xE4, 0x0, 0xF]))
        self.stream.seek(0x25FDED, 0)
        self.stream.write(bytes([0x48, 0x30, 0x06, 0x80, 0xE4, 0x0, 0xF]))
        self.stream.seek(0x25FE22, 0)
        self.stream.write(bytes([0x48, 0x30, 0x07, 0x80, 0xE4, 0x0, 0xF]))
        self.stream.seek(0x25FE57, 0)
        self.stream.write(bytes([0x48, 0x30, 0x08, 0x80, 0xE4, 0x0, 0xF]))

        self.swap_colors(colors[self.world.options.mario_color], 0)
        self.swap_colors(colors[self.world.options.luigi_color], 1)
        self.swap_pants(cpants[self.world.options.mario_pants], 0)
        self.swap_pants(cpants[self.world.options.luigi_pants], 1)

    def enemy_randomize(self):
        enemy_data = EnemyRandomize()
        if self.world.options.randomize_enemies:
            enemy_data = self.populate_enemy_array(enemy_data)
            enemy_data = self.generate_groups(enemy_data)

        if self.world.options.randomize_bosses:
            enemy_data = self.generate_boss_groups(enemy_data)

        self.insert_groups(enemy_data)

    def randomize_backgrounds(self):
        all_enemies = enemies + bosses
        for address in all_enemies:
            self.stream.seek(address + 3, io.SEEK_SET)
            self.stream.write(bytes([self.random.randint(0x0, 0x26)]))

    def randomize_sounds(self):
        temp = pkgutil.get_data(__name__, "data/sounds.txt")
        temp_io = io.BytesIO(temp)
        fresh_pointers = []

        for line in temp_io.readlines():
            fresh_pointers += [int(line.decode('utf-8').strip(), 16)]
        pointers = list(fresh_pointers)

        self.world.random.shuffle(pointers)
        self.stream.seek(0x21cc44, 0)
        for i in range(354):
            current_position = self.stream.tell()
            print(format(current_position, 'x'))
            value = int.from_bytes(self.stream.read(3), 'little')
            if value in fresh_pointers:
                print(format(value, 'x'))
                self.stream.seek(current_position)
                self.stream.write(pointers.pop().to_bytes(3, 'little'))
            self.stream.seek(1, 1)


    def disable_music(self):
        self.stream.seek(0x19B118)
        self.stream.write(bytes([0x0, 0x25]))

    def randomize_music(self):
        songs = []
        self.stream.seek(0x21CB74)
        while True:
            if self.stream.tell() == 0x21CBD8:
                self.stream.seek(4, io.SEEK_CUR)
                continue
            if self.stream.tell() == 0x21CC3C:
                break
            temp = self.stream.read(4)
            songs.append(temp)

        self.random.shuffle(songs)
        self.stream.seek(0x21CB74)
        for i in range(len(songs) - 1, -1, -1):
            if self.stream.tell() == 0x21CBD8:
                self.stream.seek(4, io.SEEK_CUR)
                continue
            self.stream.write(songs[i])

    def populate_enemy_array(self, enemy_data_) -> EnemyRandomize:
        enemy_data = enemy_data_

        for e in enemies:
            i = 0
            count = 0
            while True:
                if 0x50402C < e < 0x50434C and self.world.options.castle_skip:
                    break
                stream_seek_position = e + 10 + (i * 4)
                self.stream.seek(stream_seek_position, os.SEEK_SET)
                type_val = self.stream.read(1)[0]
                if type_val == 0x0:
                    type_val = 0x4
                if type_val == 0x7:
                    break
                self.stream.seek(-3, os.SEEK_CUR)
                id_val = self.stream.read(1)[0]
                if id_val in [int(hex_value) for hex_value in [0x18, 0x53, 0x4B]] or (
                        0x2D <= id_val <= 0x30) or id_val == 0x3C:
                    type_val = 0x4
                if id_val == 0xF and type_val == 0x3:
                    i += 1
                    if i == 6:
                        break
                    continue
                if id_val in [int(hex_value) for hex_value in [0x16, 0x1E, 0x20, 0x34, 0x35, 0x36, 0x37, 0x38, 0x46]]:
                    enemy_data.spikedEnemies.append(Enemy(id_val, type_val))
                else:
                    enemy_data.enemies.append(Enemy(id_val, type_val))
                count += 1

                i += 1
                if i == 6:
                    break

            if count > 4:
                count = 4
            if count != 0:
                enemy_data.groupSizes.append(count)

        return enemy_data

    def generate_groups(self, enemy_data_) -> EnemyRandomize:
        enemy_data = enemy_data_
        no_spike = False
        enemies_copy = enemy_data.enemies
        spiked_copy = enemy_data.spikedEnemies
        self.random.shuffle(enemies_copy)
        self.random.shuffle(spiked_copy)
        total = 0
        for sizes in enemy_data.groupSizes:
            total += min(sizes, 4)

        for size in enemy_data.groupSizes:
            temp_size = min(size, 4)
            if temp_size == 0:
                continue

            id_list = []
            type_list = []
            pestnuts = []
            temp_enemies = []
            script = bytes([0xEE, 0x2C, 0x28, 0x08])
            nut = 0
            special = 0

            for _ in range(temp_size):
                enemy = enemies_copy.pop(0)
                if enemy.id in [0x20, 0x34]:
                    nut += 1
                    pestnuts.append(enemy)
                else:
                    temp_enemies.append(enemy)
                if enemy.id in [0x52, 0x2C, 0x4A]:
                    special = 1
                if enemy.id == 0x52:
                    script = bytes([0x67, 0xAB, 0x28, 0x08])

            if len(pestnuts) == 3 and size == 4:
                for enemy in pestnuts:
                    id_list.append(enemy.id)
                    type_list.append(enemy.type)
                for _ in range(3):
                    id_list.append(0xF)
                    type_list.append(0x3)
            else:
                if size == 1 and pestnuts:
                    id_list.append(pestnuts[0].id)
                    type_list.append(pestnuts[0].type)

                for enemy in pestnuts:
                    id_list.append(enemy.id)
                    type_list.append(enemy.type)
                for enemy in temp_enemies:
                    id_list.append(enemy.id)
                    type_list.append(enemy.type)

                if size == 4:
                    for _ in range(nut):
                        id_list.append(0xF)
                        type_list.append(0x3)
                else:
                    if pestnuts:
                        for _ in range(4 - len(pestnuts + temp_enemies)):
                            id_list.append(0x0)
                            type_list.append(0x7)
                        for _ in range(nut):
                            id_list.append(0xF)
                            type_list.append(0x3)

            if len(enemy_data.stardustGroups) < 3:
                enemy_data.stardustGroups.append(EnemyGroup(bytes(id_list), bytes(type_list), temp_size, script, special))
            else:
                enemy_data.groups.append(EnemyGroup(bytes(id_list), bytes(type_list), temp_size, script, special))

            if len(enemy_data.stardustGroups) == 3 and not no_spike:
                enemies_copy.extend(spiked_copy)
                self.random.shuffle(enemies_copy)
                no_spike = True

        return enemy_data

    def generate_boss_groups(self, enemy_data_) -> EnemyRandomize:
        enemy_data = enemy_data_
        for boss_val in bosses:

            if 0x50402C < boss_val < 0x50434C and self.world.options.castle_skip:
                continue
            stream_seek_position = boss_val + 2
            self.stream.seek(stream_seek_position, os.SEEK_SET)
            boss = self.stream.read(1)[0]
            stream_seek_position = boss_val + 4
            self.stream.seek(stream_seek_position, os.SEEK_SET)
            data = self.stream.read(4)
            id = []
            types = []
            iterate = True
            i = 0
            while iterate:
                stream_seek_position = boss_val + 10 + (i * 4)
                self.stream.seek(stream_seek_position, os.SEEK_SET)
                type_val = self.stream.read(1)[0]
                types.append(type_val)
                self.stream.seek(-3, os.SEEK_CUR)
                id_val = self.stream.read(1)[0]
                id.append(id_val)
                i += 1
                if i == 6:
                    break
            stream_seek_position = boss_val + 1
            self.stream.seek(stream_seek_position, os.SEEK_SET)
            enemy_data.bossGroups.append(EnemyGroup(bytes(id), bytes(types), self.stream.read(1)[0], data, boss))

        return enemy_data

    def insert_groups(self, enemy_data):
        do_boss = self.world.options.randomize_bosses

        if do_boss != 1:
            enemy_data.groups.extend(enemy_data.bossGroups)
        self.random.shuffle(enemy_data.groups)
        enemy_data.groups = enemy_data.stardustGroups + enemy_data.groups
        locations = enemies
        boss_locations = bosses

        if do_boss == 2:
            locations += boss_locations
        locations.sort()
        count = 0

        for location in locations:
            if len(enemy_data.groups) > 0:
                if self.world.options.castle_skip and 0x50402C < location < 0x50434C:
                    continue
                count += 1
                temp_group = enemy_data.groups[0]
                enemy_data.groups = enemy_data.groups[1:]
                self.stream.seek(location + 1, 0)
                b = temp_group.position.to_bytes(1, byteorder='big')
                self.stream.write(b)
                for i in range(6):
                    if i < len(temp_group.id):
                        self.stream.seek(location + 8 + (i * 4))
                        self.stream.write(bytes([temp_group.id[i]]))
                        self.stream.seek(1, os.SEEK_CUR)
                        self.stream.write(bytes([temp_group.type[i]]))
                    else:
                        self.stream.seek(location + 8 + (i * 4))
                        self.stream.write(bytes([0]))
                        self.stream.seek(1, os.SEEK_CUR)
                        self.stream.write(bytes([7]))
                self.stream.seek(location + 2)
                self.stream.write(bytes([temp_group.boss]))
                if len(temp_group.data) > 0:
                    self.stream.seek(location + 4)
                    self.stream.write(temp_group.data)

        if do_boss == 1:
            for location in bosses:
                if self.world.options.castle_skip and 0x50402C < location < 0x50434C:
                    continue
                self.random.shuffle(enemy_data.bossGroups)
                count += 1
                temp_group = enemy_data.bossGroups[0]
                enemy_data.bossGroups = enemy_data.bossGroups[1:]
                self.stream.seek(location + 1, 0)
                b = temp_group.position.to_bytes(1, byteorder='big')
                self.stream.write(b)
                for i in range(6):
                    if i < len(temp_group.id):
                        self.stream.seek(location + 8 + (i * 4))
                        self.stream.write(bytes([temp_group.id[i]]))
                        self.stream.seek(1, os.SEEK_CUR)
                        self.stream.write(bytes([temp_group.type[i]]))
                    else:
                        self.stream.seek(location + 8 + (i * 4))
                        self.stream.write(bytes([0]))
                        self.stream.seek(1, os.SEEK_CUR)
                        self.stream.write(bytes([7]))
                self.stream.seek(location + 2)
                self.stream.write(bytes([temp_group.boss]))
                if len(temp_group.data) > 0:
                    self.stream.seek(location + 4)
                    self.stream.write(temp_group.data)

    def desc_inject(self, location: Location, item: Item):
        index = -1
        for key, value in shop.items():
            if location.address in value:
                if key == 0x3C05f0:
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
                if key ==0x3C0618:
                    index = value.index(location.address) + 48
                else:
                    index = value.index(location.address) + 66

        dstring = f"{self.world.multiworld.player_name[item.player]}: {item.name}"
        self.stream.seek(0xD11000 + (index * 0x40), 0)
        self.stream.write(dstring.encode("UTF8"))


    def close(self, path):
        output_path = os.path.join(path, f"AP_{self.world.multiworld.seed_name}_P{self.player}_{self.world.multiworld.player_name[self.player]}.gba")
        with open(output_path, 'wb') as outfile:
            outfile.write(self.stream.getvalue())
        patch = MLSSDeltaPatch(os.path.splitext(output_path)[0] + ".apmlss", player=self.player,
                               player_name=self.world.multiworld.player_name[self.player], patched_path=output_path)
        patch.write()
        os.unlink(output_path)
        self.stream.close()

    def apply_delta(self, b: bytes) -> bytes:
        """
        Gets the patched ROM data generated from applying the ap-patch diff file to the provided ROM.
        Which should contain all changed text banks and assembly code
        """
        import pkgutil
        patch_bytes = pkgutil.get_data(__name__, "data/basepatch.bsdiff")
        patched_rom = bsdiff4.patch(b, patch_bytes)
        return patched_rom
