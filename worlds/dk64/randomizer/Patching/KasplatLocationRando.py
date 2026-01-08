"""Apply Kasplat Locations."""

from randomizer.Enums.Enemies import Enemies
from randomizer.Lists.KasplatLocations import KasplatLocationList
from randomizer.Enums.Maps import Maps
from randomizer.Patching.Patcher import LocalROM
from randomizer.Patching.Library.Assets import getPointerLocation, TableNames


def randomize_kasplat_locations(spoiler, ROM_COPY: LocalROM):
    """Write replaced enemies to ROM."""
    kasplat_types = [
        Enemies.KasplatDK,
        Enemies.KasplatDiddy,
        Enemies.KasplatLanky,
        Enemies.KasplatTiny,
        Enemies.KasplatChunky,
    ]
    vanilla_kasplat_maps = [
        Maps.JungleJapes,
        Maps.JapesUnderGround,
        Maps.AngryAztec,
        Maps.AztecChunky5DTemple,
        Maps.AztecLlamaTemple,
        Maps.FranticFactory,
        Maps.GloomyGalleon,
        Maps.FungiForest,
        Maps.ForestGiantMushroom,
        Maps.CrystalCaves,
        Maps.CreepyCastle,
        Maps.CastleUpperCave,
        Maps.CastleLowerCave,
        Maps.CastleTree,
        Maps.HideoutHelmLobby,
        Maps.CreepyCastleLobby,
        Maps.CrystalCavesLobby,
        Maps.FranticFactoryLobby,
        Maps.GloomyGalleonLobby,
    ]
    if spoiler.settings.kasplat_rando:
        selected_kasplat_names = [name for name in spoiler.shuffled_kasplat_map.keys()]
        for cont_map_id in range(216):
            cont_map_spawner_address = getPointerLocation(TableNames.Spawners, cont_map_id)
            ROM_COPY.seek(cont_map_spawner_address)
            fence_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
            offset = 2
            fence_bytes = []
            used_fence_ids = []
            if fence_count > 0:
                for x in range(fence_count):
                    fence = []
                    fence_start = cont_map_spawner_address + offset
                    ROM_COPY.seek(cont_map_spawner_address + offset)
                    point_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
                    offset += (point_count * 6) + 2
                    ROM_COPY.seek(cont_map_spawner_address + offset)
                    point0_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
                    offset += (point0_count * 10) + 6
                    fence_finish = cont_map_spawner_address + offset
                    fence_size = fence_finish - fence_start
                    ROM_COPY.seek(fence_finish - 4)
                    used_fence_ids.append(int.from_bytes(ROM_COPY.readBytes(2), "big"))
                    ROM_COPY.seek(fence_start)
                    for y in range(int(fence_size / 2)):
                        fence.append(int.from_bytes(ROM_COPY.readBytes(2), "big"))
                    fence_bytes.append(fence)
                    ROM_COPY.seek(fence_finish)
            spawner_count_location = cont_map_spawner_address + offset
            ROM_COPY.seek(spawner_count_location)
            spawner_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
            offset += 2
            spawner_bytes = []
            used_enemy_indexes = []
            for x in range(spawner_count):
                ROM_COPY.seek(cont_map_spawner_address + offset)
                enemy_id = int.from_bytes(ROM_COPY.readBytes(1), "big")
                ROM_COPY.seek(cont_map_spawner_address + offset + 0x4)
                enemy_coords = []
                for y in range(3):
                    coord = int.from_bytes(ROM_COPY.readBytes(2), "big")
                    if coord > 32767:
                        coord -= 65536
                    enemy_coords.append(coord)
                ROM_COPY.seek(cont_map_spawner_address + offset + 0x13)
                enemy_index = int.from_bytes(ROM_COPY.readBytes(1), "big")
                used_enemy_indexes.append(enemy_index)
                init_offset = offset
                ROM_COPY.seek(cont_map_spawner_address + offset + 0x11)
                extra_count = int.from_bytes(ROM_COPY.readBytes(1), "big")
                offset += 0x16 + (extra_count * 2)
                end_offset = offset
                is_vanilla = False
                new_id = 0
                for level in KasplatLocationList:
                    kasplats = KasplatLocationList[level]
                    for kasplat in kasplats:
                        if kasplat.vanilla and kasplat.name in selected_kasplat_names and kasplat.map == cont_map_id:
                            coord_match_count = 0
                            for y in range(3):
                                if enemy_coords[y] == kasplat.coords[y]:
                                    coord_match_count += 1
                            if coord_match_count == 3:
                                is_vanilla = True
                                kong_idx = spoiler.shuffled_kasplat_map[kasplat.name]
                                new_id = kasplat_types[kong_idx]

                if enemy_id not in kasplat_types or is_vanilla or cont_map_id not in vanilla_kasplat_maps:
                    data_bytes = []
                    spawner_size = end_offset - init_offset
                    ROM_COPY.seek(cont_map_spawner_address + init_offset)
                    for x in range(spawner_size):
                        if x == 0 and is_vanilla:
                            data_bytes.append(new_id)
                            ROM_COPY.seek(cont_map_spawner_address + init_offset + 1)
                        else:
                            data_bytes.append(int.from_bytes(ROM_COPY.readBytes(1), "big"))
                    spawner_bytes.append(data_bytes)
            spawn_index = 1
            fence_index = 1
            for level in KasplatLocationList:
                kasplats = KasplatLocationList[level]
                for kasplat in kasplats:
                    if cont_map_id == kasplat.map and kasplat.name in selected_kasplat_names and not kasplat.vanilla:
                        if spawn_index in used_enemy_indexes:
                            while spawn_index in used_enemy_indexes:
                                spawn_index += 1
                            used_enemy_indexes.append(spawn_index)
                        if fence_index in used_fence_ids:
                            while fence_index in used_fence_ids:
                                fence_index += 1
                            used_fence_ids.append(fence_index)
                        scale = int(kasplat.scale * 0x32) & 0xFF
                        # Spawner
                        data_bytes = []
                        kong_idx = spoiler.shuffled_kasplat_map[kasplat.name]
                        data_bytes.append(kasplat_types[kong_idx])
                        data_bytes.append(0x7A)
                        for x in range(2):
                            data_bytes.append(0)
                        for x in kasplat.coords:
                            if x < 0:
                                x += 65536  # Convert to unsigned
                            data_bytes.append(int(x / 256))
                            data_bytes.append(int(x % 256))
                        for x in range(2):
                            data_bytes.append(0)
                        data_bytes.append(0x23)  # Idle Speed
                        data_bytes.append(0x3C)  # Aggro Speed
                        data_bytes.append(fence_index)  # Fence ID
                        data_bytes.append(scale)  # Scale
                        data_bytes.append(1)  # Init Control State
                        data_bytes.append(0)  # Extra Data Count
                        data_bytes.append(2)  # Init Spawn State
                        data_bytes.append(spawn_index)  # Spawn Index
                        data_bytes.append(0x1E)  # Init Respawn Timer
                        data_bytes.append(0)
                        spawner_bytes.append(data_bytes)
                        # Fence
                        new_fence_bytes = []
                        a_0 = [kasplat.bounds[0], 0, kasplat.bounds[2]]
                        a_1 = [kasplat.bounds[1], 0, kasplat.bounds[2]]
                        a_2 = [kasplat.bounds[1], 0, kasplat.bounds[3]]
                        a_3 = [kasplat.bounds[0], 0, kasplat.bounds[3]]
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
            ROM_COPY.seek(cont_map_spawner_address)
            ROM_COPY.writeMultipleBytes(len(fence_bytes), 2)
            for x in fence_bytes:
                for y in x:
                    ROM_COPY.writeMultipleBytes(y, 2)
            ROM_COPY.writeMultipleBytes(len(spawner_bytes), 2)
            for x in spawner_bytes:
                for y in x:
                    ROM_COPY.writeMultipleBytes(y, 1)
