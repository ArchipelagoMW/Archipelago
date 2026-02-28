"""Apply Door Locations."""

from randomizer.Enums.Levels import Levels
from randomizer.Enums.DoorType import DoorType
from randomizer.Enums.ScriptTypes import ScriptTypes
from randomizer.Enums.Settings import MiscChangesSelected, ProgressiveHintItem, HelmSetting, DKPortalRando
from randomizer.Enums.Transitions import Transitions
from randomizer.Enums.Types import Types
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Maps import Maps
from randomizer.Lists.DoorLocations import door_locations
from randomizer.Lists.MapsAndExits import GetExitId, GetMapId
from randomizer.Patching.Library.Generic import addNewScript, getNextFreeID, IsDDMSSelected
from randomizer.Patching.Library.DataTypes import float_to_hex
from randomizer.Patching.Library.Assets import getPointerLocation, TableNames
from randomizer.Patching.Patcher import LocalROM

LEVEL_MAIN_MAPS = (
    Maps.JungleJapes,
    Maps.AngryAztec,
    Maps.FranticFactory,
    Maps.GloomyGalleon,
    Maps.FungiForest,
    Maps.CrystalCaves,
    Maps.CreepyCastle,
)

MAP_LEVEL_PAIRING = {
    Maps.JungleJapes: Levels.JungleJapes,
    Maps.AngryAztec: Levels.AngryAztec,
    Maps.FranticFactory: Levels.FranticFactory,
    Maps.GloomyGalleon: Levels.GloomyGalleon,
    Maps.FungiForest: Levels.FungiForest,
    Maps.CrystalCaves: Levels.CrystalCaves,
    Maps.CreepyCastle: Levels.CreepyCastle,
}

PORTAL_MAP_ID_PAIRING = {
    Maps.JungleJapes: 0x11B,
    Maps.AngryAztec: 0x1A0,
    Maps.FranticFactory: 0x1C2,
    Maps.GloomyGalleon: 0x57,
    Maps.FungiForest: 0x5C,
    Maps.CrystalCaves: 0x54,
    Maps.CreepyCastle: 0xB8,
}

PORTAL_MAP_EXIT_PAIRING = {
    Maps.JungleJapes: [0, 15],
    Maps.AngryAztec: [0],
    Maps.FranticFactory: [0],
    Maps.GloomyGalleon: [0],
    Maps.FungiForest: [0, 27],
    Maps.CrystalCaves: [0],
    Maps.CreepyCastle: [0, 21],
}


class FunctionData:
    """Function information regarding an instance script."""

    def __init__(self, conditions: list, executions: list):
        """Initialize with given parameters."""
        self.conditions = conditions.copy()
        self.executions = executions.copy()


class InstanceInstruction:
    """Information about an instruction regarding an instance script."""

    def __init__(self, function: int, parameters: list, inverted: bool = False):
        """Initialize with given parameters."""
        self.function = function
        self.parameters = parameters.copy()
        self.inverted = inverted


DK_PORTAL_NEW_PICKUP_RADIUS = 60
DK_PORTAL_SCRIPT = [
    FunctionData(
        [InstanceInstruction(1, [0, 0, 0])],
        [
            InstanceInstruction(22, [1, 0, 0]),
            InstanceInstruction(22, [2, 0, 0]),
            InstanceInstruction(20, [1, 160, 0]),
            InstanceInstruction(20, [2, 115, 0]),
        ],
    ),
    FunctionData(
        [
            InstanceInstruction(1, [0, 0, 0]),
        ],
        [
            InstanceInstruction(17, [1, 65535, 0]),
            InstanceInstruction(17, [2, 65535, 0]),
            InstanceInstruction(1, [1, 0, 0]),
        ],
    ),
    FunctionData(
        [
            InstanceInstruction(1, [1, 0, 0]),
            InstanceInstruction(19, [DK_PORTAL_NEW_PICKUP_RADIUS, 0, 0]),
            InstanceInstruction(35, [0, 0, 0], True),
        ],
        [
            InstanceInstruction(3, [0, 60, 0]),
            InstanceInstruction(7, [116, 0, 1]),
        ],
    ),
    FunctionData(
        [
            InstanceInstruction(1, [1, 0, 0]),
            InstanceInstruction(19, [DK_PORTAL_NEW_PICKUP_RADIUS, 0, 0]),
            InstanceInstruction(35, [0, 0, 0], True),
        ],
        [
            InstanceInstruction(110, [1, 0, 0]),
            InstanceInstruction(37, [29, 0, 15]),
            InstanceInstruction(25, [90, 0, 0]),
            InstanceInstruction(1, [100, 0, 0]),
        ],
    ),
    FunctionData(
        [
            InstanceInstruction(1, [100, 0, 0]),
            InstanceInstruction(4, [0, 0, 0]),
        ],
        [
            InstanceInstruction(1, [2, 0, 0]),
        ],
    ),
    FunctionData(
        [
            InstanceInstruction(1, [1, 0, 0]),
            InstanceInstruction(19, [DK_PORTAL_NEW_PICKUP_RADIUS, 0, 0], True),
        ],
        [
            InstanceInstruction(1, [2, 0, 0]),
        ],
    ),
    FunctionData(
        [
            InstanceInstruction(1, [1, 0, 0]),
            InstanceInstruction(35, [0, 0, 0]),
        ],
        [
            InstanceInstruction(1, [2, 0, 0]),
        ],
    ),
    FunctionData(
        [
            InstanceInstruction(1, [2, 0, 0]),
            InstanceInstruction(4, [0, 0, 0]),
        ],
        [
            InstanceInstruction(90, [60, 60, 60]),
            InstanceInstruction(61, [3, 0, 0]),
            InstanceInstruction(1, [3, 0, 0]),
        ],
    ),
    FunctionData(
        [
            InstanceInstruction(1, [3, 0, 0]),
            InstanceInstruction(16, [1, 1, 0]),
        ],
        [
            InstanceInstruction(3, [0, 40, 0]),
            InstanceInstruction(7, [116, 0, 0]),
            InstanceInstruction(110, [1, 0, 0]),
            InstanceInstruction(37, [30, 0, 15]),
        ],
    ),
    FunctionData(
        [
            InstanceInstruction(1, [3, 0, 0]),
            InstanceInstruction(16, [1, 1, 0]),
        ],
        [
            InstanceInstruction(25, [89, 0, 0]),
            InstanceInstruction(1, [4, 0, 0]),
        ],
    ),
    FunctionData(
        [
            InstanceInstruction(1, [4, 0, 0]),
            InstanceInstruction(4, [0, 0, 0]),
        ],
        [
            InstanceInstruction(141, [0, 0, 0]),
            InstanceInstruction(1, [5, 0, 0]),
        ],
    ),
]


def pushNewDKPortalScript(cont_map_id: Maps, portal_id_dict: dict, ROM_COPY: LocalROM):
    """Write new dk portal script to ROM."""
    id_pairings = {
        Maps.JungleJapes: 0x11B,
        Maps.AngryAztec: 0x1A0,
        Maps.FranticFactory: 0x1C2,
        Maps.GloomyGalleon: 0x57,
        Maps.FungiForest: 0x5C,
        Maps.CrystalCaves: 0x54,
        Maps.CreepyCastle: 0xB8,
    }
    obj_id = portal_id_dict[cont_map_id]
    if obj_id is None:
        raise Exception("Invalid Portal ID.")
    script_table = getPointerLocation(TableNames.InstanceScripts, cont_map_id)
    ROM_COPY.seek(script_table)
    script_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
    good_scripts = []
    # Construct good pre-existing scripts
    file_offset = 2
    for script_item in range(script_count):
        ROM_COPY.seek(script_table + file_offset)
        script_start = script_table + file_offset
        script_id = int.from_bytes(ROM_COPY.readBytes(2), "big")
        block_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
        file_offset += 6
        for block_item in range(block_count):
            ROM_COPY.seek(script_table + file_offset)
            cond_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
            file_offset += 2 + (8 * cond_count)
            ROM_COPY.seek(script_table + file_offset)
            exec_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
            file_offset += 2 + (8 * exec_count)
        script_end = script_table + file_offset
        if script_id != obj_id:
            script_data = []
            ROM_COPY.seek(script_start)
            for x in range(int((script_end - script_start) / 2)):
                script_data.append(int.from_bytes(ROM_COPY.readBytes(2), "big"))
            good_scripts.append(script_data)
    # Get new script data
    script_arr = [
        obj_id,
        len(DK_PORTAL_SCRIPT),
        0,
    ]
    for block in DK_PORTAL_SCRIPT:
        script_arr.append(len(block.conditions))
        for cond in block.conditions:
            func = cond.function
            if cond.inverted:
                func |= 0x8000
            script_arr.append(func)
            script_arr.extend(cond.parameters)
        script_arr.append(len(block.executions))
        for ex in block.executions:
            script_arr.append(ex.function)
            script_arr.extend(ex.parameters)
    good_scripts.append(script_arr)
    # Reconstruct File
    ROM_COPY.seek(script_table)
    ROM_COPY.writeMultipleBytes(len(good_scripts), 2)
    for script in good_scripts:
        for x in script:
            ROM_COPY.writeMultipleBytes(x, 2)


def remove_existing_indicators(spoiler, ROM_COPY: LocalROM):
    """Remove all existing indicators."""
    if spoiler.settings.portal_numbers:
        return
    for cont_map_id in range(216):
        setup_table = getPointerLocation(TableNames.Setups, cont_map_id)
        # Filter Setup
        ROM_COPY.seek(setup_table)
        model2_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
        retained_model2 = []
        for item in range(model2_count):
            item_start = setup_table + 4 + (item * 0x30)
            ROM_COPY.seek(item_start + 0x28)
            item_type = int.from_bytes(ROM_COPY.readBytes(2), "big")
            if cont_map_id == 0x2A or item_type != 0x2AB:
                ROM_COPY.seek(item_start)
                item_data = []
                for x in range(int(0x30 / 4)):
                    item_data.append(int.from_bytes(ROM_COPY.readBytes(4), "big"))
                retained_model2.append(item_data)
        mys_start = setup_table + 4 + (model2_count * 0x30)
        ROM_COPY.seek(mys_start)
        mys_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
        act_start = mys_start + 4 + (mys_count * 0x24)
        ROM_COPY.seek(act_start)
        act_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
        act_end = act_start + 4 + (act_count * 0x38)
        other_retained_data = []
        ROM_COPY.seek(mys_start)
        for x in range(int((act_end - mys_start) / 4)):
            other_retained_data.append(int.from_bytes(ROM_COPY.readBytes(4), "big"))
        # Reconstruct setup file
        ROM_COPY.seek(setup_table)
        ROM_COPY.writeMultipleBytes(len(retained_model2), 4)
        for item in retained_model2:
            for data in item:
                ROM_COPY.writeMultipleBytes(data, 4)
        for data in other_retained_data:
            ROM_COPY.writeMultipleBytes(data, 4)


def place_door_locations(spoiler, ROM_COPY: LocalROM):
    """Place Wrinkly Doors, and eventually T&S Doors."""
    enabled = False
    settings_enable = [
        spoiler.settings.wrinkly_location_rando,
        spoiler.settings.tns_location_rando,
        spoiler.settings.remove_wrinkly_puzzles,
        spoiler.settings.progressive_hint_item != ProgressiveHintItem.off,
        spoiler.settings.dk_portal_location_rando_v2 != DKPortalRando.off,
    ]
    for boolean in settings_enable:
        if boolean:
            enabled = True
    if enabled:
        wrinkly_doors = [0xF0, 0xF2, 0xEF, 0x67, 0xF1]
        # Also remove
        #   0x23C: Spinning Door (Az Lobby)
        #   0x18: Metal Pad (Az Lobby)
        #   0x23D: Wrinkly Wheel (Fungi Lobby)
        #   0x28: Lever (Fungi Lobby)
        #   0x35: Ice Block (Caves Lobby)
        #   0xCE: Grey Switch (Caves Lobby)
        dk_portal_locations = {}
        dk_portal_ids = {}
        # Handle Setup
        for cont_map_id in range(216):
            setup_table = getPointerLocation(TableNames.Setups, cont_map_id)
            # Filter Setup
            ROM_COPY.seek(setup_table)
            model2_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
            retained_model2 = []
            for item in range(model2_count):
                item_start = setup_table + 4 + (item * 0x30)
                ROM_COPY.seek(item_start + 0x28)
                item_type = int.from_bytes(ROM_COPY.readBytes(2), "big")
                retain = True
                if spoiler.settings.wrinkly_location_rando or spoiler.settings.remove_wrinkly_puzzles or spoiler.settings.progressive_hint_item != ProgressiveHintItem.off:
                    if item_type in wrinkly_doors:
                        retain = False
                    if cont_map_id == Maps.AngryAztecLobby and item_type in (0x23C, 0x18):
                        retain = False
                    if cont_map_id == Maps.FungiForestLobby and item_type in (0x23D, 0x28):
                        retain = False
                    if cont_map_id == Maps.CrystalCavesLobby and item_type in (0x35, 0xCE):
                        retain = False
                if spoiler.settings.tns_location_rando:
                    if cont_map_id != 0x2A:
                        if item_type in (0x2AB, 0x2AC):
                            retain = False
                if spoiler.settings.dk_portal_location_rando_v2 != DKPortalRando.off:
                    if cont_map_id in LEVEL_MAIN_MAPS:
                        if item_type == 0x2AD:
                            retain = False
                            level = MAP_LEVEL_PAIRING[cont_map_id]
                            for data in spoiler.shuffled_door_data[level]:
                                if data[1] == DoorType.dk_portal:
                                    if door_locations[level][data[0]].default_placed == DoorType.dk_portal:
                                        retain = True

                if retain:
                    ROM_COPY.seek(item_start)
                    item_data = []
                    for x in range(int(0x30 / 4)):
                        item_data.append(int.from_bytes(ROM_COPY.readBytes(4), "big"))
                    retained_model2.append(item_data)
            mys_start = setup_table + 4 + (model2_count * 0x30)
            ROM_COPY.seek(mys_start)
            mys_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
            act_start = mys_start + 4 + (mys_count * 0x24)
            ROM_COPY.seek(act_start)
            act_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
            act_end = act_start + 4 + (act_count * 0x38)
            other_retained_data = []
            ROM_COPY.seek(mys_start)
            for x in range(int((act_end - mys_start) / 4)):
                other_retained_data.append(int.from_bytes(ROM_COPY.readBytes(4), "big"))
            # Construct placed wrinkly doors
            door_ids = []
            map_wrinkly_ids = []
            portal_indicator_ids = []
            portal_ids = []
            indicator_ids = []
            for level in spoiler.shuffled_door_data:
                for data in spoiler.shuffled_door_data[level]:
                    door = door_locations[level][data[0]]
                    door_type = data[1]
                    if door.map == cont_map_id:
                        # If any wrinkly doors have had their location changed or randomized
                        if door_type == DoorType.wrinkly and (
                            IsDDMSSelected(
                                spoiler.settings.misc_changes_selected,
                                MiscChangesSelected.remove_wrinkly_puzzles,
                            )
                            or spoiler.settings.wrinkly_location_rando
                        ):
                            # If hint doors should exist (no progressive hints unless hints are in the pool, or the edge case of wrinkly puzzles
                            # being removed without wrinkly location rando AND progressive hints being set to off)
                            if (
                                (spoiler.settings.progressive_hint_item == ProgressiveHintItem.off)
                                or Types.Hint in spoiler.settings.shuffled_location_types
                                or (
                                    IsDDMSSelected(
                                        spoiler.settings.misc_changes_selected,
                                        MiscChangesSelected.remove_wrinkly_puzzles,
                                    )
                                    and not spoiler.settings.wrinkly_location_rando
                                    and spoiler.settings.progressive_hint_item == ProgressiveHintItem.off
                                )
                            ):
                                kong = data[2]
                                item_data = []
                                for coord_index in range(3):
                                    item_data.append(int(float_to_hex(door.location[coord_index]), 16))  # x y z
                                default_scale = door.scale
                                if door.default_placed == DoorType.dk_portal:
                                    default_scale = 2
                                item_data.append(int(float_to_hex(default_scale), 16))  # Scale
                                item_data.append(0x5F0)
                                item_data.append(0x80121B00)
                                item_data.append(int(float_to_hex(door.rx), 16))  # rx
                                item_data.append(int(float_to_hex(door.location[3]), 16))  # ry
                                item_data.append(int(float_to_hex(door.rz), 16))  # rz
                                item_data.append(0)
                                id = getNextFreeID(ROM_COPY, cont_map_id, door_ids)
                                map_wrinkly_ids.append(id)
                                door_ids.append(id)
                                item_data.append((wrinkly_doors[kong] << 16) | id)
                                item_data.append(1 << 16)
                                retained_model2.append(item_data)
                        elif door_type == DoorType.boss and spoiler.settings.tns_location_rando:
                            lim = 2
                            if not spoiler.settings.portal_numbers:
                                lim = 1
                            for k in range(lim):
                                item_data = []
                                default_scale = door.scale
                                if door.default_placed == DoorType.dk_portal:
                                    default_scale = 2
                                for coord_index in range(3):
                                    if k == 1 and coord_index == 1:
                                        y_offset = 30 * default_scale
                                        item_data.append(int(float_to_hex(door.location[coord_index] - y_offset), 16))  # y
                                    else:
                                        item_data.append(int(float_to_hex(door.location[coord_index]), 16))  # x y z
                                item_data.append(int(float_to_hex([default_scale, 0.35 * default_scale][k]), 16))  # Scale
                                item_data.append(0xFFFEFEFF)
                                item_data.append(0x001BFFE1)
                                item_data.append(int(float_to_hex(door.rx), 16))  # rx
                                item_data.append(int(float_to_hex(door.location[3]), 16))  # ry
                                item_data.append(int(float_to_hex(door.rz), 16))  # rz
                                item_data.append(0)
                                id = getNextFreeID(ROM_COPY, cont_map_id, door_ids)
                                portal_indicator_ids.append(id)
                                door_ids.append(id)
                                if k == 0:
                                    portal_ids.append(id)
                                else:
                                    indicator_ids.append(id)
                                item_data.append(([0x2AC, 0x2AB][k] << 16) | id)
                                item_data.append(1 << 16)
                                retained_model2.append(item_data)
                        elif door_type == DoorType.dk_portal and spoiler.settings.dk_portal_location_rando_v2 != DKPortalRando.off and door.default_placed != DoorType.dk_portal:
                            item_data = []
                            for coord_index in range(3):
                                item_data.append(int(float_to_hex(door.location[coord_index]), 16))  # x y z
                            if cont_map_id not in dk_portal_locations:
                                dk_portal_locations[cont_map_id] = [0, 0, 0, 0]
                            for coord_index in range(4):
                                dk_portal_locations[cont_map_id][coord_index] = door.location[coord_index]
                            default_scale = 1
                            if door.default_placed != DoorType.dk_portal:
                                default_scale = door.scale / 2
                            item_data.append(int(float_to_hex(default_scale), 16))  # Scale
                            item_data.append(0xFFFFFEFF)
                            item_data.append(0x0101F03E)
                            item_data.append(int(float_to_hex(door.rx), 16))  # rx
                            item_data.append(int(float_to_hex(door.location[3]), 16))  # ry
                            item_data.append(int(float_to_hex(door.rz), 16))  # rz
                            item_data.append(0)
                            if cont_map_id in PORTAL_MAP_ID_PAIRING:
                                dk_portal_ids[cont_map_id] = PORTAL_MAP_ID_PAIRING[cont_map_id]
                            else:
                                dk_portal_ids[cont_map_id] = getNextFreeID(ROM_COPY, cont_map_id, door_ids)
                            item_data.append((0x2AD << 16) | dk_portal_ids[cont_map_id])
                            item_data.append(1 << 16)
                            retained_model2.append(item_data)
            if len(map_wrinkly_ids) > 0:
                addNewScript(ROM_COPY, cont_map_id, map_wrinkly_ids, ScriptTypes.Wrinkly)
            if len(portal_ids) > 0:
                addNewScript(ROM_COPY, cont_map_id, portal_ids, ScriptTypes.TnsPortal)
            if len(indicator_ids) > 0:
                addNewScript(ROM_COPY, cont_map_id, indicator_ids, ScriptTypes.TnsIndicator)
            # Reconstruct setup file
            ROM_COPY.seek(setup_table)
            ROM_COPY.writeMultipleBytes(len(retained_model2), 4)
            for item in retained_model2:
                for data in item:
                    ROM_COPY.writeMultipleBytes(data, 4)
            for data in other_retained_data:
                ROM_COPY.writeMultipleBytes(data, 4)
        if spoiler.settings.dk_portal_location_rando_v2 != DKPortalRando.off:
            for portal_map in dk_portal_locations:
                if dk_portal_locations[portal_map][0] + dk_portal_locations[portal_map][1] + dk_portal_locations[portal_map][2] + dk_portal_locations[portal_map][3] != 0:
                    pushNewDKPortalScript(portal_map, dk_portal_ids, ROM_COPY)
                    exit_start = getPointerLocation(TableNames.Exits, portal_map)
                    exits_to_alter = [-1]
                    if portal_map in LEVEL_MAIN_MAPS:
                        exits_to_alter = [-1] + PORTAL_MAP_EXIT_PAIRING[portal_map]
                    for exit_index in exits_to_alter:
                        if exit_index >= 0:
                            ROM_COPY.seek(exit_start + 12 + (exit_index * 10))
                        else:
                            ROM_COPY.seek(exit_start)
                        for coord_index in range(3):
                            coord_value = dk_portal_locations[portal_map][coord_index]
                            coord_int = int(coord_value)
                            if coord_int < 0:
                                coord_int += 0x10000
                            ROM_COPY.writeMultipleBytes(coord_int, 2)
                        angle = int(255 * (dk_portal_locations[portal_map][3] / 360))
                        cam_raw_angle = dk_portal_locations[portal_map][3]
                        if cam_raw_angle >= 180:
                            cam_raw_angle -= 180
                        else:
                            cam_raw_angle += 180
                        cam_angle = int(255 * (cam_raw_angle / 360))
                        ROM_COPY.writeMultipleBytes(angle, 1)
                        ROM_COPY.writeMultipleBytes(cam_angle, 1)


cs_advancements = {
    1: 10,
    2: 12,
    3: 16,
    10: 18,
    15: 18,
    16: 18,
    12: 6,
}

modifications = {
    0x1C: {
        753: Levels.JungleJapes,
        754: Levels.AngryAztec,
        755: Levels.FranticFactory,
        756: Levels.GloomyGalleon,
        884: Levels.FungiForest,
        885: Levels.CrystalCaves,
        886: Levels.CreepyCastle,
    },
    Maps.Snide: {
        44: Levels.HideoutHelm,
    },
}


def getStoryDestination(spoiler, level: Levels) -> dict:
    """Get the destination dict for a story warp."""
    if level != Levels.HideoutHelm:
        return spoiler.settings.level_portal_destinations[level]
    map_id = Maps.HideoutHelm
    exit_id = 0
    if Transitions.IslesToHelm in spoiler.shuffled_exit_data:
        shuffledBack = spoiler.shuffled_exit_data[Transitions.IslesToHelm]
        map_id = GetMapId(spoiler.settings, shuffledBack.regionId)
        exit_id = GetExitId(shuffledBack)
    if map_id == Maps.HideoutHelm:
        helm_start = spoiler.settings.helm_setting
        if helm_start == HelmSetting.default:
            exit_id = 0
        elif helm_start == HelmSetting.skip_start:
            exit_id = 3
        elif helm_start == HelmSetting.skip_all:
            exit_id = 4
    return {
        "map": map_id,
        "exit": exit_id,
    }


def alterStoryCutsceneWarps(spoiler, ROM_COPY: LocalROM):
    """Alter the story cutscene warp destinations."""
    for map_id in modifications:
        cutscene_start = getPointerLocation(TableNames.Cutscenes, map_id)
        info_l = 0x30
        ROM_COPY.seek(cutscene_start)
        for _ in range(0x18):
            count = int.from_bytes(ROM_COPY.readBytes(2), "big")
            info_l += count * 0x12
        ROM_COPY.seek(cutscene_start + info_l)
        base_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
        info_l += 2
        info_l += base_count * 0x1C
        ROM_COPY.seek(cutscene_start + info_l)
        cutscene_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
        info_l += 2
        for _ in range(cutscene_count):
            ROM_COPY.seek(cutscene_start + info_l)
            subcount = int.from_bytes(ROM_COPY.readBytes(2), "big")
            info_l += 2
            info_l += 4 * subcount
        ROM_COPY.seek(cutscene_start + info_l)
        point_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
        point_count_copy = point_count
        info_l += 2
        seg_idx = 0
        while point_count_copy != 0:
            ROM_COPY.seek(cutscene_start + info_l + 1)
            command = int.from_bytes(ROM_COPY.readBytes(1), "big")
            point_count_copy -= 1
            if command in cs_advancements:
                info_l += cs_advancements[command]
            elif command == 4:
                ROM_COPY.seek(cutscene_start + info_l + 4)
                cmd_4_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
                info_l += 0x20
                info_l += 0xE * cmd_4_count
            elif command == 5:
                ROM_COPY.seek(cutscene_start + info_l + 4)
                cmd_5_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
                info_l += 0x14
                info_l += 0x8 * cmd_5_count
            elif command == 13:
                info_l += 4
                ROM_COPY.seek(cutscene_start + info_l)
                subcommand = int.from_bytes(ROM_COPY.readBytes(4), "big")
                if seg_idx in modifications[map_id]:
                    level = modifications[map_id][seg_idx]
                    dest = getStoryDestination(spoiler, level)
                    if subcommand == 0x22:
                        # Init Map Change
                        ROM_COPY.seek(cutscene_start + info_l + 4)
                        ROM_COPY.writeMultipleBytes(dest["map"], 2)
                        ROM_COPY.writeMultipleBytes(dest["exit"], 2)
                info_l += 12
            else:
                point_count_copy += 1
                info_l += 4
            seg_idx += 1
