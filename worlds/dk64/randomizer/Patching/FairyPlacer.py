"""Place fairies into the world."""

from randomizer.Enums.Enemies import Enemies
from randomizer.Lists.FairyLocations import fairy_locations, relocated_5ds_fairy
from randomizer.Enums.Maps import Maps
from randomizer.Patching.Patcher import LocalROM
from randomizer.Patching.Library.Assets import getPointerLocation, TableNames


def ReplaceShipFairy(ROM_COPY: LocalROM):
    """Replace the fairy inside 5DS with an easier to get fairy."""
    file_start = getPointerLocation(TableNames.Spawners, Maps.Galleon5DShipDKTiny)
    ROM_COPY.seek(file_start)
    fence_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
    offset = 2
    fence_bytes = []
    used_fence_ids = []
    if fence_count > 0:
        for x in range(fence_count):
            fence = []
            fence_start = file_start + offset
            ROM_COPY.seek(file_start + offset)
            point_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
            offset += (point_count * 6) + 2
            ROM_COPY.seek(file_start + offset)
            point0_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
            offset += (point0_count * 10) + 6
            fence_finish = file_start + offset
            fence_size = fence_finish - fence_start
            ROM_COPY.seek(fence_finish - 4)
            used_fence_ids.append(int.from_bytes(ROM_COPY.readBytes(2), "big"))
            ROM_COPY.seek(fence_start)
            for y in range(int(fence_size / 2)):
                fence.append(int.from_bytes(ROM_COPY.readBytes(2), "big"))
            fence_bytes.append(fence)
            ROM_COPY.seek(fence_finish)
    spawner_count_location = file_start + offset
    ROM_COPY.seek(spawner_count_location)
    spawner_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
    offset += 2
    spawner_bytes = []
    fairy_spawner_id = None
    for x in range(spawner_count):
        # Parse spawners
        ROM_COPY.seek(file_start + offset)
        enemy_id = int.from_bytes(ROM_COPY.readBytes(1), "big")
        ROM_COPY.seek(file_start + offset + 0x13)
        enemy_index = int.from_bytes(ROM_COPY.readBytes(1), "big")
        init_offset = offset
        ROM_COPY.seek(file_start + offset + 0x11)
        extra_count = int.from_bytes(ROM_COPY.readBytes(1), "big")
        offset += 0x16 + (extra_count * 2)
        end_offset = offset
        if enemy_id != Enemies.Fairy:
            # Keep enemy if not fairy
            data_bytes = []
            spawner_size = end_offset - init_offset
            ROM_COPY.seek(file_start + init_offset)
            for x in range(spawner_size):
                data_bytes.append(int.from_bytes(ROM_COPY.readBytes(1), "big"))
            spawner_bytes.append(data_bytes)
        else:
            # Is fairy
            fairy_spawner_id = enemy_index
    fence_index = 1
    if fence_index in used_fence_ids:
        while fence_index in used_fence_ids:
            fence_index += 1
    used_fence_ids.append(fence_index)
    # Spawner
    data_bytes = []
    data_bytes.append(Enemies.Fairy)
    data_bytes.append(0)
    for x in range(2):
        data_bytes.append(0)
    for x in [relocated_5ds_fairy.fence.center_x, relocated_5ds_fairy.spawn_y, relocated_5ds_fairy.fence.center_z]:
        if x < 0:
            x += 65536  # Convert to unsigned
        data_bytes.append(int(x / 256))
        data_bytes.append(int(x % 256))
    for x in range(2):
        data_bytes.append(0)
    data_bytes.append(0x23)  # Idle Speed
    data_bytes.append(0x3C)  # Aggro Speed
    data_bytes.append(fence_index)  # Fence ID
    data_bytes.append(0x32)  # Scale
    data_bytes.append(1)  # Init Control State
    data_bytes.append(0)  # Extra Data Count
    data_bytes.append(2)  # Init Spawn State
    data_bytes.append(fairy_spawner_id)  # Spawn Index
    data_bytes.append(0)  # Init Respawn Timer
    data_bytes.append(0)
    spawner_bytes.append(data_bytes)
    # Fence
    new_fence_bytes = []
    a_0 = [relocated_5ds_fairy.fence.min_x, 0, relocated_5ds_fairy.fence.min_z]
    a_1 = [relocated_5ds_fairy.fence.max_x, 0, relocated_5ds_fairy.fence.min_z]
    a_2 = [relocated_5ds_fairy.fence.max_x, 0, relocated_5ds_fairy.fence.max_z]
    a_3 = [relocated_5ds_fairy.fence.min_x, 0, relocated_5ds_fairy.fence.max_z]
    a_01 = []
    a_12 = []
    a_23 = []
    a_30 = []
    for x in range(3):
        a_01.append(int((a_0[x] + a_1[x]) / 2))
        a_12.append(int((a_1[x] + a_2[x]) / 2))
        a_23.append(int((a_2[x] + a_3[x]) / 2))
        a_30.append(int((a_3[x] + a_0[x]) / 2))
    fence_coords = [a_0, a_01, a_1, a_12, a_2, a_23, a_3, a_30]
    new_fence_bytes.append(len(fence_coords))  # 0: Fence Block 0x6 Count, 1: Fence Block 0xA Count
    for x in fence_coords:
        for y in x:
            if y < 0:
                y += 65536  # Signed to unsigned conversion
            new_fence_bytes.append(y)
    new_fence_bytes.append(0)
    new_fence_bytes.append(fence_index)
    new_fence_bytes.append(1)
    fence_bytes.append(new_fence_bytes)
    # Repack
    ROM_COPY.seek(file_start)
    ROM_COPY.writeMultipleBytes(len(fence_bytes), 2)
    for x in fence_bytes:
        for y in x:
            ROM_COPY.writeMultipleBytes(y, 2)
    ROM_COPY.writeMultipleBytes(len(spawner_bytes), 2)
    for x in spawner_bytes:
        for y in x:
            ROM_COPY.writeMultipleBytes(y, 1)


def PlaceFairies(spoiler, ROM_COPY: LocalROM):
    """Write Fairies to ROM."""
    ReplaceShipFairy(ROM_COPY)
    sav = spoiler.settings.rom_data
    ROM_COPY.seek(sav + 0xE0)
    ROM_COPY.writeMultipleBytes(0, 2)
    if spoiler.settings.random_fairies:
        action_maps = [
            Maps.JungleJapes,
            Maps.JapesLankyCave,
            Maps.AztecLlamaTemple,
            Maps.AztecTiny5DTemple,
            Maps.FranticFactory,
            Maps.GloomyGalleon,
            Maps.Galleon5DShipDKTiny,
            Maps.ForestThornvineBarn,
            Maps.ForestRafters,
            Maps.CavesTinyIgloo,
            Maps.CavesDiddyUpperCabin,
            Maps.CastleTree,
            Maps.CastleMuseum,
            Maps.Isles,
            Maps.FranticFactoryLobby,
            Maps.FungiForestLobby,
            Maps.HideoutHelm,
        ]
        # Append new maps to action map list
        for level in spoiler.fairy_locations:
            for item in spoiler.fairy_locations[level]:
                if fairy_locations[level][item].map not in action_maps:
                    action_maps.append(fairy_locations[level][item].map)
        # Pull all character spawner files that are part of the action map list
        for map in action_maps:
            file_start = getPointerLocation(TableNames.Spawners, map)
            ROM_COPY.seek(file_start)
            fence_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
            offset = 2
            fence_bytes = []
            used_fence_ids = []
            if fence_count > 0:
                for x in range(fence_count):
                    fence = []
                    fence_start = file_start + offset
                    ROM_COPY.seek(file_start + offset)
                    point_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
                    offset += (point_count * 6) + 2
                    ROM_COPY.seek(file_start + offset)
                    point0_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
                    offset += (point0_count * 10) + 6
                    fence_finish = file_start + offset
                    fence_size = fence_finish - fence_start
                    ROM_COPY.seek(fence_finish - 4)
                    used_fence_ids.append(int.from_bytes(ROM_COPY.readBytes(2), "big"))
                    ROM_COPY.seek(fence_start)
                    for y in range(int(fence_size / 2)):
                        fence.append(int.from_bytes(ROM_COPY.readBytes(2), "big"))
                    fence_bytes.append(fence)
                    ROM_COPY.seek(fence_finish)
            spawner_count_location = file_start + offset
            ROM_COPY.seek(spawner_count_location)
            spawner_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
            offset += 2
            spawner_bytes = []
            used_enemy_indexes = []
            for x in range(spawner_count):
                # Parse spawners
                ROM_COPY.seek(file_start + offset)
                enemy_id = int.from_bytes(ROM_COPY.readBytes(1), "big")
                ROM_COPY.seek(file_start + offset + 0x4)
                enemy_coords = []
                for y in range(3):
                    coord = int.from_bytes(ROM_COPY.readBytes(2), "big")
                    if coord > 32767:
                        coord -= 65536
                    enemy_coords.append(coord)
                ROM_COPY.seek(file_start + offset + 0x13)
                enemy_index = int.from_bytes(ROM_COPY.readBytes(1), "big")
                used_enemy_indexes.append(enemy_index)
                init_offset = offset
                ROM_COPY.seek(file_start + offset + 0x11)
                extra_count = int.from_bytes(ROM_COPY.readBytes(1), "big")
                offset += 0x16 + (extra_count * 2)
                end_offset = offset
                is_vanilla = False
                # Check if fairy is a vanilla fairy
                for level in spoiler.fairy_locations:
                    fairies = [fairy_locations[level][x] for x in spoiler.fairy_locations[level]]
                    for fairy in fairies:
                        if fairy.is_vanilla and fairy.map == map:
                            coord_match_count = 0
                            for y in range(3):
                                if enemy_coords[y] == fairy.spawn_xyz[y]:
                                    coord_match_count += 1
                            if coord_match_count == 3:
                                is_vanilla = True
                if enemy_id != Enemies.Fairy or is_vanilla:
                    # Keep enemy if not fairy or is a vanilla fairy that's going to be kept
                    data_bytes = []
                    spawner_size = end_offset - init_offset
                    ROM_COPY.seek(file_start + init_offset)
                    for x in range(spawner_size):
                        data_bytes.append(int.from_bytes(ROM_COPY.readBytes(1), "big"))
                    spawner_bytes.append(data_bytes)
            spawn_index = 1
            fence_index = 1
            for level in spoiler.fairy_locations:
                # Check for new fairies
                fairies = [fairy_locations[level][x] for x in spoiler.fairy_locations[level]]
                for sub_index, fairy in enumerate(fairies):
                    if map == fairy.map and not fairy.is_vanilla:
                        # Fairy is not vanilla
                        if spawn_index in used_enemy_indexes:
                            while spawn_index in used_enemy_indexes:
                                spawn_index += 1
                        used_enemy_indexes.append(spawn_index)
                        if fence_index in used_fence_ids:
                            while fence_index in used_fence_ids:
                                fence_index += 1
                        used_fence_ids.append(fence_index)
                        # Spawner
                        data_bytes = []
                        data_bytes.append(Enemies.Fairy)
                        data_bytes.append(0)
                        for x in range(2):
                            data_bytes.append(0)
                        for x in [fairy.fence.center_x, fairy.spawn_y, fairy.fence.center_z]:
                            if x < 0:
                                x += 65536  # Convert to unsigned
                            data_bytes.append(int(x / 256))
                            data_bytes.append(int(x % 256))
                        for x in range(2):
                            data_bytes.append(0)
                        data_bytes.append(0x23)  # Idle Speed
                        data_bytes.append(0x3C)  # Aggro Speed
                        data_bytes.append(fence_index)  # Fence ID
                        data_bytes.append(0x32)  # Scale
                        data_bytes.append(1)  # Init Control State
                        data_bytes.append(0)  # Extra Data Count
                        data_bytes.append(2)  # Init Spawn State
                        data_bytes.append(spawn_index)  # Spawn Index
                        data_bytes.append(0)  # Init Respawn Timer
                        data_bytes.append(0)
                        spawner_bytes.append(data_bytes)
                        # Set ID for array
                        for item in spoiler.fairy_data_table:
                            if item["level"] == level and spoiler.fairy_locations[level][sub_index] == item["fairy_index"]:
                                item["id"] = spawn_index
                        # Fence
                        new_fence_bytes = []
                        a_0 = [fairy.fence.min_x, 0, fairy.fence.min_z]
                        a_1 = [fairy.fence.max_x, 0, fairy.fence.min_z]
                        a_2 = [fairy.fence.max_x, 0, fairy.fence.max_z]
                        a_3 = [fairy.fence.min_x, 0, fairy.fence.max_z]
                        a_01 = []
                        a_12 = []
                        a_23 = []
                        a_30 = []
                        for x in range(3):
                            a_01.append(int((a_0[x] + a_1[x]) / 2))
                            a_12.append(int((a_1[x] + a_2[x]) / 2))
                            a_23.append(int((a_2[x] + a_3[x]) / 2))
                            a_30.append(int((a_3[x] + a_0[x]) / 2))
                        fence_coords = [a_0, a_01, a_1, a_12, a_2, a_23, a_3, a_30]
                        new_fence_bytes.append(len(fence_coords))  # 0: Fence Block 0x6 Count, 1: Fence Block 0xA Count
                        for x in fence_coords:
                            for y in x:
                                if y < 0:
                                    y += 65536  # Signed to unsigned conversion
                                new_fence_bytes.append(y)
                        new_fence_bytes.append(0)
                        new_fence_bytes.append(fence_index)
                        new_fence_bytes.append(1)
                        fence_bytes.append(new_fence_bytes)
            # Repack
            ROM_COPY.seek(file_start)
            ROM_COPY.writeMultipleBytes(len(fence_bytes), 2)
            for x in fence_bytes:
                for y in x:
                    ROM_COPY.writeMultipleBytes(y, 2)
            ROM_COPY.writeMultipleBytes(len(spawner_bytes), 2)
            for x in spawner_bytes:
                for y in x:
                    ROM_COPY.writeMultipleBytes(y, 1)
        # Non-Spawner files
        # Setting Enable
        ROM_COPY.seek(sav + 0x100)
        ROM_COPY.write(1)
        # Array construction
        write_data = [255, 255]
        for index, item in enumerate(spoiler.fairy_data_table):
            ROM_COPY.seek(0x1FFC000 + (4 * index))
            ROM_COPY.writeMultipleBytes(item["flag"], 2)
            item_level = item["level"]
            item_map = fairy_locations[item_level][item["fairy_index"]].map
            ROM_COPY.writeMultipleBytes(item_map, 1)
            ROM_COPY.writeMultipleBytes(item["id"], 1)  # Get Spawner ID
            if item["shift"] >= 0:
                offset = int(item["shift"] >> 3)
                check = int(item["shift"] % 8)
                write_data[offset] &= 0xFF - (0x80 >> check)
        ROM_COPY.seek(sav + 0xE0)
        for byte_data in write_data:
            ROM_COPY.writeMultipleBytes(byte_data, 1)
