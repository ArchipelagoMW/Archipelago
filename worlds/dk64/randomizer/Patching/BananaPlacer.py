"""Apply CB Rando changes."""

import randomizer.Lists.CBLocations.AngryAztecCBLocations
import randomizer.Lists.CBLocations.CreepyCastleCBLocations
import randomizer.Lists.CBLocations.CrystalCavesCBLocations
import randomizer.Lists.CBLocations.FranticFactoryCBLocations
import randomizer.Lists.CBLocations.FungiForestCBLocations
import randomizer.Lists.CBLocations.GloomyGalleonCBLocations
import randomizer.Lists.CBLocations.JungleJapesCBLocations
import randomizer.Lists.CBLocations.DKIslesCBLocations
from randomizer.Enums.Levels import Levels
from randomizer.Patching.Library.Generic import IsItemSelected
from randomizer.Patching.Library.Assets import getPointerLocation, TableNames
from randomizer.Patching.Library.DataTypes import float_to_hex, short_to_ushort
from randomizer.Patching.Patcher import LocalROM
from randomizer.Lists.MapsAndExits import LevelMapTable

level_data = {
    Levels.JungleJapes: {
        "cb": randomizer.Lists.CBLocations.JungleJapesCBLocations.ColoredBananaGroupList,
        "balloons": randomizer.Lists.CBLocations.JungleJapesCBLocations.BalloonList,
    },
    Levels.AngryAztec: {
        "cb": randomizer.Lists.CBLocations.AngryAztecCBLocations.ColoredBananaGroupList,
        "balloons": randomizer.Lists.CBLocations.AngryAztecCBLocations.BalloonList,
    },
    Levels.FranticFactory: {
        "cb": randomizer.Lists.CBLocations.FranticFactoryCBLocations.ColoredBananaGroupList,
        "balloons": randomizer.Lists.CBLocations.FranticFactoryCBLocations.BalloonList,
    },
    Levels.GloomyGalleon: {
        "cb": randomizer.Lists.CBLocations.GloomyGalleonCBLocations.ColoredBananaGroupList,
        "balloons": randomizer.Lists.CBLocations.GloomyGalleonCBLocations.BalloonList,
    },
    Levels.FungiForest: {
        "cb": randomizer.Lists.CBLocations.FungiForestCBLocations.ColoredBananaGroupList,
        "balloons": randomizer.Lists.CBLocations.FungiForestCBLocations.BalloonList,
    },
    Levels.CrystalCaves: {
        "cb": randomizer.Lists.CBLocations.CrystalCavesCBLocations.ColoredBananaGroupList,
        "balloons": randomizer.Lists.CBLocations.CrystalCavesCBLocations.BalloonList,
    },
    Levels.CreepyCastle: {
        "cb": randomizer.Lists.CBLocations.CreepyCastleCBLocations.ColoredBananaGroupList,
        "balloons": randomizer.Lists.CBLocations.CreepyCastleCBLocations.BalloonList,
    },
    Levels.CreepyCastle: {
        "cb": randomizer.Lists.CBLocations.CreepyCastleCBLocations.ColoredBananaGroupList,
        "balloons": randomizer.Lists.CBLocations.CreepyCastleCBLocations.BalloonList,
    },
    Levels.DKIsles: {
        "cb": randomizer.Lists.CBLocations.DKIslesCBLocations.ColoredBananaGroupList,
        "balloons": randomizer.Lists.CBLocations.DKIslesCBLocations.BalloonList,
    },
}

PATH_CAP = 64


def randomize_cbs(spoiler, ROM_COPY: LocalROM):
    """Place Colored Bananas into ROM."""
    if not spoiler.settings.cb_rando_enabled:
        return
    levels_to_place = []
    for level in level_data:
        is_level_placed = IsItemSelected(spoiler.settings.cb_rando_enabled, spoiler.settings.cb_rando_list_selected, level)
        if is_level_placed:
            levels_to_place.append(level)
    for cont_map_id in range(216):
        # Wipe setup and paths of CB information
        level_id = None
        for lvl, map_ids in LevelMapTable.items():
            if cont_map_id in map_ids:
                level_id = lvl
        if level_id is not None and level_id not in levels_to_place:
            continue
        # SETUP
        modeltwo_cbs = [0xA, 0xD, 0x16, 0x1E, 0x1F, 0x2B, 0x205, 0x206, 0x207, 0x208]
        actor_cbs = [91, 111, 112, 113, 114]
        setup_table = getPointerLocation(TableNames.Setups, cont_map_id)
        ROM_COPY.seek(setup_table)
        model2_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
        # Model Two CBs
        persisted_m2_data = []
        used_m2_ids = []
        for item in range(model2_count):
            item_start = setup_table + 4 + (item * 0x30)
            ROM_COPY.seek(item_start + 0x28)
            item_type = int.from_bytes(ROM_COPY.readBytes(2), "big")
            if item_type not in modeltwo_cbs:  # Not CB
                ROM_COPY.seek(item_start + 0x2A)
                used_m2_ids.append(int.from_bytes(ROM_COPY.readBytes(2), "big"))
                ROM_COPY.seek(item_start)
                item_data = []
                for x in range(int(0x30 / 4)):
                    item_data.append(int.from_bytes(ROM_COPY.readBytes(4), "big"))
                persisted_m2_data.append(item_data)
        ROM_COPY.seek(setup_table + 4 + (0x30 * model2_count))
        mystery_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
        # Mystery
        persisted_mys_data = []
        for item in range(mystery_count):
            ROM_COPY.seek(setup_table + 4 + (model2_count * 0x30) + 4 + (item * 0x24))
            item_data = []
            for x in range(int(0x24 / 4)):
                item_data.append(int.from_bytes(ROM_COPY.readBytes(4), "big"))
            persisted_mys_data.append(item_data)
        actor_block = setup_table + 4 + (0x30 * model2_count) + 4 + (0x24 * mystery_count)
        ROM_COPY.seek(actor_block)
        actor_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
        # Actors
        persisted_act_data = []
        used_actor_ids = []
        remove_paths = []
        for item in range(actor_count):
            actor_start = actor_block + 4 + (item * 0x38)
            ROM_COPY.seek(actor_start + 0x32)
            actor_type = int.from_bytes(ROM_COPY.readBytes(2), "big") + 0x10
            if actor_type not in actor_cbs:
                ROM_COPY.seek(actor_start + 0x34)
                used_actor_ids.append(int.from_bytes(ROM_COPY.readBytes(2), "big"))
                ROM_COPY.seek(actor_start)
                item_data = []
                for x in range(int(0x38 / 4)):
                    item_data.append(int.from_bytes(ROM_COPY.readBytes(4), "big"))
                persisted_act_data.append(item_data)
            else:
                ROM_COPY.seek(actor_start + 0x12)
                path_id = int.from_bytes(ROM_COPY.readBytes(2), "big")
                if path_id not in remove_paths:
                    remove_paths.append(path_id)
        # PATHS
        path_table = getPointerLocation(TableNames.Paths, cont_map_id)
        ROM_COPY.seek(path_table)
        path_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
        persisted_paths = []
        used_path_ids = []
        path_offset = 2
        for path_index in range(path_count):
            ROM_COPY.seek(path_table + path_offset)
            path_id = int.from_bytes(ROM_COPY.readBytes(2), "big")
            point_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
            if path_id not in remove_paths:
                path_size = 6 + (point_count * 10)
                item_data = []
                ROM_COPY.seek(path_table + path_offset)
                for x in range(int(path_size / 2)):
                    item_data.append(int.from_bytes(ROM_COPY.readBytes(2), "big"))
                persisted_paths.append(item_data)
                used_path_ids.append(path_id)
            path_offset += 6 + (10 * point_count)
        # Place all new colored bananas
        new_id = 0
        act_id = 0
        npath_id = 0
        for new_cb in spoiler.cb_placements:
            if new_cb["map"] == cont_map_id:
                cb_type = new_cb["type"]
                associated_list = level_data[new_cb["level"]][cb_type]
                if cb_type == "cb":
                    # Model Two CBs
                    singles = [0xD, 0xA, 0x1E, 0x16, 0x1F]
                    bunches = [0x2B, 0x208, 0x205, 0x207, 0x206]
                    for loc in new_cb["locations"]:
                        item_data = []
                        item_data.extend(
                            [
                                int(float_to_hex(loc[2]), 16),
                                int(float_to_hex(loc[3]), 16),
                                int(float_to_hex(loc[4]), 16),
                                int(float_to_hex(loc[1]), 16),
                            ]
                        )
                        item_data.append(2)
                        item_data.append(0x01C7FFFF)
                        for x in range(int((0x24 - 0x18) / 4)):
                            item_data.append(0)
                        item_data.append(0x40400000)
                        cb_item_type = 0
                        if loc[0] == 5:
                            cb_item_type = bunches[new_cb["kong"]]
                        else:
                            cb_item_type = singles[new_cb["kong"]]
                        found_vacant = False
                        found_id = 0
                        while not found_vacant:
                            if new_id not in used_m2_ids:
                                used_m2_ids.append(new_id)
                                found_id = new_id
                                found_vacant = True
                            new_id += 1
                        item_data.append((cb_item_type << 16) + found_id)
                        item_data.append((2 << 16) + 1)
                        persisted_m2_data.append(item_data)
                for list_item in associated_list:
                    if cb_type == "balloons" and list_item.id == new_cb["id"]:
                        # Found balloon
                        # Setup
                        balloons = [114, 91, 113, 112, 111]
                        item_data = []
                        for coord in list_item.setSpawnPoint(list_item.points):
                            item_data.append(int(float_to_hex(coord), 16))  # x y z
                        item_data.append(int(float_to_hex(1), 16))  # Scale
                        found_vacant_path = False
                        found_path_id = 0
                        found_vacant_actor = False
                        found_actor_id = 0
                        while not found_vacant_path:
                            if npath_id not in used_path_ids:
                                used_path_ids.append(npath_id)
                                found_path_id = npath_id
                                found_vacant_path = True
                            npath_id += 1
                        while not found_vacant_actor:
                            if act_id not in used_actor_ids:
                                used_actor_ids.append(act_id)
                                found_actor_id = act_id
                                found_vacant_actor = True
                            act_id += 1
                        if found_path_id < PATH_CAP:
                            item_data.append(found_path_id)
                        else:
                            item_data.append(0xFFFF)  # Fixes a crash from too many balloons - might have some side-effects
                        item_data.append(list_item.speed)
                        for x in range(int((0x30 - 0x18) / 4)):
                            item_data.append(0)
                        item_data.append(balloons[new_cb["kong"]] - 16)
                        item_data.append((found_actor_id << 16) + 0x6E08)
                        persisted_act_data.append(item_data)
                        # Path
                        if found_path_id < PATH_CAP:  # Crashing issues with more than PATH_CAP paths
                            item_data = []
                            item_data.append(found_path_id)
                            item_data.append(len(list_item.points))
                            item_data.append(0)
                            for pt in list_item.points:
                                item_data.append(20)
                                item_data.append(short_to_ushort(pt[0]))
                                item_data.append(short_to_ushort(pt[1]))
                                item_data.append(short_to_ushort(pt[2]))
                                item_data.append((1 << 8) + 0)
                            new_paths = []
                            for path in persisted_paths:
                                if path[0] < found_path_id:
                                    new_paths.append(path)
                            new_paths.append(item_data)
                            for path in persisted_paths:
                                if path[0] > found_path_id:
                                    new_paths.append(path)
                            persisted_paths = new_paths.copy()
        # Recompile Tables
        # SETUP
        ROM_COPY.seek(setup_table)
        ROM_COPY.writeMultipleBytes(len(persisted_m2_data), 4)
        for x in persisted_m2_data:
            for y in x:
                ROM_COPY.writeMultipleBytes(y, 4)
        ROM_COPY.writeMultipleBytes(len(persisted_mys_data), 4)
        for x in persisted_mys_data:
            for y in x:
                ROM_COPY.writeMultipleBytes(y, 4)
        ROM_COPY.writeMultipleBytes(len(persisted_act_data), 4)
        for x in persisted_act_data:
            for y in x:
                ROM_COPY.writeMultipleBytes(y, 4)
        # print(f"{hex(cont_map_id)}: {hex(path_table)}")
        ROM_COPY.seek(path_table)
        ROM_COPY.writeMultipleBytes(len(persisted_paths), 2)
        for x in persisted_paths:
            for y in x:
                ROM_COPY.writeMultipleBytes(y, 2)
