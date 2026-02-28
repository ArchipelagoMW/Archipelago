"""Apply cosmetic elements of Kong Rando."""

from randomizer.Enums.Maps import Maps
from randomizer.Enums.Enemies import Enemies
from randomizer.Patching.Patcher import LocalROM
from randomizer.Patching.Library.Assets import getPointerLocation, TableNames


def apply_kongrando_cosmetic(ROM_COPY: LocalROM):
    """Write kong cage changes for kong rando."""
    for cont_map_id in [Maps.JungleJapes, Maps.AztecLlamaTemple, Maps.AztecTinyTemple, Maps.FranticFactory]:
        # Character Spawners
        cont_map_spawner_address = getPointerLocation(TableNames.Spawners, cont_map_id)
        ROM_COPY.seek(cont_map_spawner_address)
        fence_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
        offset = 2
        if fence_count > 0:
            for x in range(fence_count):
                ROM_COPY.seek(cont_map_spawner_address + offset)
                point_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
                offset += (point_count * 6) + 2
                ROM_COPY.seek(cont_map_spawner_address + offset)
                point0_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
                offset += (point0_count * 10) + 6
        ROM_COPY.seek(cont_map_spawner_address + offset)
        spawner_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
        offset += 2
        for x in range(spawner_count):
            ROM_COPY.seek(cont_map_spawner_address + offset)
            enemy_id = int.from_bytes(ROM_COPY.readBytes(1), "big")
            init_offset = offset
            ROM_COPY.seek(cont_map_spawner_address + offset + 0x11)
            extra_count = int.from_bytes(ROM_COPY.readBytes(1), "big")
            offset += 0x16 + (extra_count * 2)
            has_id = False
            new_type = 0
            if enemy_id in (Enemies.CutsceneDiddy, Enemies.CutsceneLanky, Enemies.CutsceneTiny, Enemies.CutsceneChunky):
                has_id = True
                new_type = Enemies.CharSpawnerItem
            if has_id:
                ROM_COPY.seek(cont_map_spawner_address + init_offset)
                ROM_COPY.writeMultipleBytes(new_type, 1)
