"""Rando write bananaport locations."""

import math
from randomizer.Enums.Settings import BananaportRando, ShufflePortLocations
from randomizer.Lists.Warps import BananaportVanilla
from randomizer.Patching.Patcher import LocalROM
from randomizer.Enums.Maps import Maps
from randomizer.Lists.Warps import BananaportVanilla
from randomizer.Lists.CustomLocations import CustomLocations
from randomizer.Enums.Levels import Levels
from randomizer.Patching.Library.Assets import getPointerLocation, TableNames


def randomize_bananaport(spoiler, ROM_COPY: LocalROM):
    """Rando write bananaport locations."""
    pad_types = [0x214, 0x213, 0x211, 0x212, 0x210]

    if spoiler.settings.bananaport_rando in (BananaportRando.crossmap_coupled, BananaportRando.crossmap_decoupled):
        data_start = 0x1FF0000
        visual_warp_changes = []
        maps_used = []
        for port_index, port_new in enumerate(spoiler.bananaport_replacements):
            ROM_COPY.seek(data_start + (port_index * 0xA))
            map_id = int.from_bytes(ROM_COPY.readBytes(1), "big")
            ROM_COPY.writeMultipleBytes(port_new[0], 1)
            obj_id = int.from_bytes(ROM_COPY.readBytes(2), "big")
            if map_id not in maps_used:
                maps_used.append(map_id)
            visual_warp_changes.append([map_id, obj_id, port_new[1]])
        for cont_map_id in maps_used:
            cont_map_setup_address = getPointerLocation(TableNames.Setups, cont_map_id)
            ROM_COPY.seek(cont_map_setup_address)
            model2_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
            for x in range(model2_count):
                start = cont_map_setup_address + 4 + (x * 0x30)
                ROM_COPY.seek(start + 0x2A)
                obj_id = int.from_bytes(ROM_COPY.readBytes(2), "big")
                for warp_change in visual_warp_changes:
                    if warp_change[0] == cont_map_id and warp_change[1] == obj_id:
                        ROM_COPY.seek(start + 0x28)
                        ROM_COPY.writeMultipleBytes(pad_types[warp_change[2]], 2)


CAMERA_DISTANCE = 100


def move_bananaports(spoiler, ROM_COPY: LocalROM):
    """Move bananaports around in conjunction with custom bananaport location rando."""
    MAPS_WITH_WARPS = {
        Maps.JungleJapes: Levels.JungleJapes,
        Maps.AngryAztec: Levels.AngryAztec,
        Maps.FranticFactory: Levels.FranticFactory,
        Maps.GloomyGalleon: Levels.GloomyGalleon,
        Maps.FungiForest: Levels.FungiForest,
        Maps.CrystalCaves: Levels.CrystalCaves,
        Maps.CreepyCastle: Levels.CreepyCastle,
        Maps.Isles: Levels.DKIsles,
        Maps.AztecLlamaTemple: Levels.AngryAztec,
        Maps.CastleCrypt: Levels.CreepyCastle,
    }

    if spoiler.settings.bananaport_placement_rando != ShufflePortLocations.off:
        for cont_map_id in MAPS_WITH_WARPS:
            level_id = MAPS_WITH_WARPS[cont_map_id]
            cutscene_table = getPointerLocation(TableNames.Cutscenes, cont_map_id)
            setup_table = getPointerLocation(TableNames.Setups, cont_map_id)
            exit_table = getPointerLocation(TableNames.Exits, cont_map_id)
            modification_table = []
            for warp_id in spoiler.warp_locations:
                if BananaportVanilla[warp_id].map_id == cont_map_id:
                    custom_location_id = spoiler.warp_locations[warp_id]
                    obj_id = BananaportVanilla[warp_id].obj_id_vanilla
                    exit_id = BananaportVanilla[warp_id].tied_exit
                    new_coords = CustomLocations[level_id][custom_location_id].coords
                    cam_lock_id = BananaportVanilla[warp_id].camera
                    warp_angle = (CustomLocations[level_id][custom_location_id].rot_y / 4096) * 360
                    modification_table.append(
                        {
                            "obj_id": obj_id,
                            "coords": new_coords,
                            "scale": min(CustomLocations[level_id][custom_location_id].max_size / (56 * 4), 0.25),  # Make 0.25 the max size
                            "rot_x": CustomLocations[level_id][custom_location_id].rot_x,
                            "rot_y": warp_angle,
                            "rot_z": CustomLocations[level_id][custom_location_id].rot_z,
                        }
                    )
                    # Modify Exit Table
                    ROM_COPY.seek(exit_table + (10 * exit_id) + 12)
                    ROM_COPY.writeMultipleBytes(int(new_coords[0]), 2)
                    ROM_COPY.writeMultipleBytes(int(new_coords[1] + 4.25), 2)
                    ROM_COPY.writeMultipleBytes(int(new_coords[2]), 2)
                    # Modify Camera Lock Table
                    if cam_lock_id is not None:
                        ROM_COPY.seek(cutscene_table)
                        header_end = 0x30
                        for x in range(0x18):
                            count = int.from_bytes(ROM_COPY.readBytes(2), "big")
                            header_end += 0x12 * count
                        ROM_COPY.seek(cutscene_table + header_end)
                        count = int.from_bytes(ROM_COPY.readBytes(2), "big")
                        if cam_lock_id >= count:
                            continue
                            # raise Exception(f"Invalid ID for camera lock. Map {cont_map_id}. Cam Lock ID {cam_lock_id}. Cap {count}. Header End {hex(header_end)}")
                        # Update Prox Trigger Coordinates
                        ROM_COPY.seek(cutscene_table + header_end + 2 + (0x1C * cam_lock_id) + 0x10)
                        ROM_COPY.writeMultipleBytes(int(new_coords[0]), 2)
                        ROM_COPY.writeMultipleBytes(int(new_coords[1] + 4.25), 2)
                        ROM_COPY.writeMultipleBytes(int(new_coords[2]), 2)
                        # Focal X Z
                        ROM_COPY.seek(cutscene_table + header_end + 2 + (0x1C * cam_lock_id) + 0x06)
                        ROM_COPY.writeMultipleBytes(int(new_coords[0]), 2)
                        ROM_COPY.writeMultipleBytes(int(new_coords[2]), 2)
                        # Update Distance
                        ROM_COPY.seek(cutscene_table + header_end + 2 + (0x1C * cam_lock_id) + 0x19)
                        ROM_COPY.writeMultipleBytes(0xA, 1)
                        # Update camera position
                        angle_rad = (CustomLocations[level_id][custom_location_id].rot_y / 4096) * math.pi * 2
                        new_angle = 0
                        if angle_rad >= math.pi:
                            new_angle = angle_rad - math.pi
                        else:
                            new_angle = angle_rad + math.pi
                        dz = math.cos(new_angle) * CAMERA_DISTANCE
                        dx = math.sin(new_angle) * CAMERA_DISTANCE
                        ROM_COPY.seek(cutscene_table + header_end + 2 + (0x1C * cam_lock_id) + 0x0)
                        ROM_COPY.writeMultipleBytes(int(new_coords[0] + dx), 2)
                        ROM_COPY.writeMultipleBytes(int(new_coords[1] + 30), 2)
                        ROM_COPY.writeMultipleBytes(int(new_coords[2] - dz), 2)
            # Modify setup table
            obj_id_list = [x["obj_id"] for x in modification_table]
            ROM_COPY.seek(setup_table)
            model2_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
            for model2_item in range(model2_count):
                item_start = setup_table + 4 + (model2_item * 0x30)
                ROM_COPY.seek(item_start + 0x2A)
                item_id = int.from_bytes(ROM_COPY.readBytes(2), "big")
                if item_id in obj_id_list:
                    ROM_COPY.seek(item_start)
                    for k in modification_table:
                        if k["obj_id"] == item_id:
                            for c in k["coords"]:
                                ROM_COPY.writeFloat(c)
                            ROM_COPY.writeFloat(k["scale"])
                            ROM_COPY.seek(item_start + 0x18)
                            ROM_COPY.writeFloat(k["rot_x"])
                            ROM_COPY.writeFloat(k["rot_y"])
                            ROM_COPY.writeFloat(k["rot_z"])
