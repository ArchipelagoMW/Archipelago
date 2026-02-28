"""Place Shuffled Shops."""

from randomizer.Enums.Regions import Regions
from randomizer.Enums.Maps import Maps
from randomizer.Enums.VendorType import VendorType
from randomizer.Patching.Library.DataTypes import intf_to_float
from randomizer.Patching.Library.Assets import getPointerLocation, TableNames
from randomizer.Patching.Library.ItemRando import CustomActors
from randomizer.Patching.Patcher import LocalROM
from randomizer.ShuffleShopLocations import available_shops


class FunctionData:
    """Function Data Class."""

    def __init__(
        self,
        function: int,
        parameters: list,
        inverted: bool = False,
        exist_vendors: list = [VendorType.Candy, VendorType.Cranky, VendorType.Funky, VendorType.Snide],
    ):
        """Initialize with given parameters."""
        self.function = function
        self.parameters = parameters.copy()
        self.inverted = inverted
        self.exist_vendors = exist_vendors.copy()


class ScriptBlock:
    """Script Block Class."""

    def __init__(
        self,
        conditions: list,
        executions: list,
        exist_vendors: list = [VendorType.Candy, VendorType.Cranky, VendorType.Funky, VendorType.Snide],
    ):
        """Initialize with given parameters."""
        self.conditions = conditions.copy()
        self.executions = executions.copy()
        self.exist_vendors = exist_vendors.copy()


def getShopkeeperInstanceScript(vendor: VendorType, water_id: int = None, lz_id: int = None) -> list:
    """Get the instance script associated with a shopkeeper."""
    script = []
    # Generate Script
    data_arg_0 = {
        VendorType.Candy: 2,
        VendorType.Cranky: 3,
        VendorType.Funky: 2,
        VendorType.Snide: 4,
    }
    data_arg_1 = {
        VendorType.Candy: 0,
        VendorType.Cranky: 1,
        VendorType.Funky: 2,
        VendorType.Snide: 3,
    }
    data_arg_2 = {
        VendorType.Candy: 80,
        VendorType.Cranky: 120,
        VendorType.Funky: 80,
        VendorType.Snide: 50,
    }
    data_arg_3 = {
        VendorType.Candy: 101,
        VendorType.Cranky: 100,
        VendorType.Funky: 102,
    }
    data_arg_4 = {
        VendorType.Cranky: 4,
        VendorType.Funky: 3,
    }
    data_arg_5 = {
        VendorType.Candy: 815,
        VendorType.Funky: 814,
    }
    data_arg_6 = {
        VendorType.Candy: 8,
        VendorType.Funky: 12,
    }
    data_arg_7 = {
        VendorType.Candy: 816,
        VendorType.Funky: 814,
    }
    data_arg_8 = {
        VendorType.Candy: 20,
        VendorType.Funky: 20,
        VendorType.Cranky: 20,
        VendorType.Snide: 15,
    }
    data_arg_9 = {
        VendorType.Cranky: 50,
        VendorType.Snide: 28,
    }
    data_arg_10 = {
        VendorType.Candy: 2,
        VendorType.Funky: 2,
        VendorType.Cranky: 4,
        VendorType.Snide: 4,
    }
    bone_id = {
        VendorType.Candy: 1,
        VendorType.Funky: 3,
        VendorType.Cranky: 10,
        VendorType.Snide: 10,
    }

    range_val = 100
    if water_id is not None:
        script.append(
            ScriptBlock(
                [
                    FunctionData(0, [0, 0, 0]),
                ],
                [
                    FunctionData(27, [water_id, 1, 0]),
                    FunctionData(123, [lz_id, bone_id.get(vendor, 0), 0]),
                ],
            )
        )
        range_val = 120
    else:
        script.append(
            ScriptBlock(
                [
                    FunctionData(1, [0, 0, 0]),
                ],
                [
                    FunctionData(20, [data_arg_4.get(vendor, 0), data_arg_8.get(vendor, 0), 0]),
                    FunctionData(24, [data_arg_4.get(vendor, 0), 1, 0]),
                ],
                [VendorType.Cranky, VendorType.Funky],
            )
        )

    script.extend(
        [
            ScriptBlock(
                [
                    FunctionData(1, [0, 0, 0]),
                ],
                [
                    FunctionData(90, [range_val, range_val, range_val]),
                    FunctionData(61, [4, 0, 0]),
                    FunctionData(20, [data_arg_0.get(vendor, 0), data_arg_8.get(vendor, 0), 0]),
                    FunctionData(24, [data_arg_0.get(vendor, 0), 1, 0]),
                ],
            ),
            ScriptBlock(
                [
                    FunctionData(1, [0, 0, 0]),
                ],
                [
                    FunctionData(20, [2, 80, 0], False, [VendorType.Cranky]),
                    FunctionData(24, [1, 1, 0]),
                    FunctionData(22, [1, 1, 0]),
                    FunctionData(20, [1, 0, 0]),
                ],
            ),
        ]
    )
    if vendor in (VendorType.Candy, VendorType.Funky):
        script.extend(
            [
                ScriptBlock(
                    [
                        FunctionData(1, [0, 0, 0]),
                        FunctionData(32, [400, 0, 0]),
                    ],
                    [
                        FunctionData(17, [3, 65535, 0]),
                    ],
                    [VendorType.Funky],
                ),
                ScriptBlock(
                    [
                        FunctionData(1, [0, 0, 0]),
                        FunctionData(32, [400, 0, 0]),
                    ],
                    [
                        FunctionData(17, [2, 65535, 0]),
                        FunctionData(26, [1, 41, 100]),
                        FunctionData(17, [1, 1, 0]),
                        FunctionData(1, [1, 0, 0]),
                    ],
                ),
            ]
        )
    elif vendor in (VendorType.Cranky, VendorType.Snide):
        script.extend(
            [
                ScriptBlock(
                    [
                        FunctionData(1, [0, 0, 0]),
                        FunctionData(32, [400, 0, 0]),
                    ],
                    [
                        FunctionData(17, [4, 65535, 0]),
                    ],
                    [VendorType.Cranky],
                ),
                ScriptBlock(
                    [
                        FunctionData(1, [0, 0, 0]),
                        FunctionData(32, [400, 0, 0]),
                    ],
                    [
                        FunctionData(17, [4, 65535, 0], False, [VendorType.Snide]),
                        FunctionData(38, [1, 0, 0], False, [VendorType.Cranky]),
                        FunctionData(26, [1, data_arg_9.get(vendor, 0), 100]),
                        FunctionData(17, [1, 1, 0]),
                        FunctionData(1, [1, 0, 0]),
                    ],
                ),
                ScriptBlock(
                    [
                        FunctionData(1, [0, 0, 0]),
                        FunctionData(32, [400, 0, 0]),
                    ],
                    [
                        FunctionData(38, [1, 0, 0]),
                        FunctionData(124, [1, 0, 0]),
                        FunctionData(125, [295, 0, 6480]),
                    ],
                    [VendorType.Snide],
                ),
            ]
        )
    script.extend(
        [
            ScriptBlock(
                [
                    FunctionData(1, [1, 0, 0]),
                ],
                [
                    FunctionData(38, [1, 0, 0], False, [VendorType.Candy, VendorType.Funky]),
                    FunctionData(18, [1, 0, 0]),
                    FunctionData(1, [12, 0, 0]),
                ],
            ),
            ScriptBlock(
                [
                    FunctionData(1, [0, 0, 0]),
                    FunctionData(32, [400, 0, 0], True),
                ],
                [
                    FunctionData(69, [1, 0, 255]),
                    FunctionData(26, [1, 0, 0]),
                    FunctionData(17, [1, 1, 0]),
                    FunctionData(1, [5, 0, 0]),
                ],
            ),
            ScriptBlock(
                [
                    FunctionData(1, [5, 0, 0]),
                ],
                [
                    FunctionData(18, [1, 0, 0]),
                    FunctionData(1, [10, 0, 0]),
                ],
            ),
            ScriptBlock(
                [
                    FunctionData(1, [10, 0, 0]),
                    FunctionData(32, [1000, 0, 0]),
                ],
                [
                    FunctionData(7, [94, data_arg_1.get(vendor, 0), 0]),
                ],
            ),
            ScriptBlock(
                [
                    FunctionData(1, [10, 0, 0]),
                    FunctionData(32, [400, 0, 0]),
                ],
                [
                    FunctionData(69, [0, 0, 255]),
                    FunctionData(20, [1, data_arg_2.get(vendor, 0), 0]),
                    FunctionData(17, [1, 1, 0]),
                    FunctionData(1, [11, 0, 0], False, [VendorType.Candy, VendorType.Cranky, VendorType.Snide]),
                ],
            ),
            ScriptBlock(
                [
                    FunctionData(1, [10, 0, 0]),
                    FunctionData(32, [400, 0, 0]),
                ],
                [
                    FunctionData(17, [4, 65535, 0], False, [VendorType.Cranky]),
                    FunctionData(15, [74, 12160, 40], False, [VendorType.Snide]),
                    FunctionData(38, [1, 0, 0], False, [VendorType.Cranky, VendorType.Candy, VendorType.Funky]),
                    FunctionData(15, [data_arg_5.get(vendor, 0), 0, 40], False, [VendorType.Candy, VendorType.Funky]),
                    FunctionData(124, [1, 0, 0], False, [VendorType.Snide]),
                    FunctionData(125, [295, 0, 6480], False, [VendorType.Snide]),
                    FunctionData(17, [2, 65535, 0], False, [VendorType.Candy, VendorType.Funky]),
                    FunctionData(17, [3, 65535, 0], False, [VendorType.Funky]),
                    FunctionData(17, [4, 65535, 0], False, [VendorType.Snide]),
                    FunctionData(14, [256, 0, 40], False, [VendorType.Cranky]),
                    FunctionData(72, [0, 9000, 20], False, [VendorType.Cranky]),
                ],
            ),
            ScriptBlock(
                [
                    FunctionData(1, [10, 0, 0]),
                    FunctionData(32, [400, 0, 0]),
                ],
                [
                    FunctionData(3, [0, 18, 0], False, [VendorType.Funky, VendorType.Candy, VendorType.Cranky]),
                    FunctionData(38, [1, 0, 0], False, [VendorType.Snide]),
                    FunctionData(1, [11, 0, 0], False, [VendorType.Funky]),
                ],
                [VendorType.Funky, VendorType.Snide],
            ),
            ScriptBlock(
                [
                    FunctionData(1, [11, 0, 0]),
                    FunctionData(4, [1, 0, 0]),
                ],
                [
                    FunctionData(15, [91, 0, 40]),
                ],
                [VendorType.Funky],
            ),
            ScriptBlock(
                [
                    FunctionData(1, [11, 0, 0]),
                    FunctionData(21, [1, 0, 0], True),
                ],
                [
                    FunctionData(16, [0, 0, 0], False, [VendorType.Cranky]),
                    FunctionData(1, [12, 0, 0]),
                ],
            ),
            ScriptBlock(
                [
                    FunctionData(1, [12, 0, 0]),
                ],
                [
                    FunctionData(7, [data_arg_3.get(vendor, 0), 1, 0]),
                ],
                [VendorType.Cranky, VendorType.Funky, VendorType.Candy],
            ),
            ScriptBlock(
                [
                    FunctionData(1, [12, 0, 0]),
                    FunctionData(4, [0, 0, 0]),
                    FunctionData(21, [2, 0, 0], True),
                ],
                [
                    FunctionData(26, [2, 0, 0]),
                    FunctionData(17, [2, 1, 0]),
                    FunctionData(3, [0, 100, 0]),
                ],
                [VendorType.Cranky],
            ),
            ScriptBlock(
                [
                    FunctionData(1, [12, 0, 0]),
                    FunctionData(4, [0, 1, 0]),
                    FunctionData(21, [3, 0, 0], True),
                ],
                [
                    FunctionData(26, [3, 0, 0]),
                    FunctionData(17, [3, 1, 0]),
                    FunctionData(3, [0, 150, 1]),
                ],
                [VendorType.Cranky],
            ),
            ScriptBlock(
                [
                    FunctionData(1, [12, 0, 0]),
                    FunctionData(32, [500, 0, 0], True),
                ],
                [
                    FunctionData(18, [data_arg_10.get(vendor, 0), 0, 0]),
                    FunctionData(20, [1, data_arg_2.get(vendor, 0), 0]),
                    FunctionData(17, [1, 1, 0]),
                    FunctionData(1, [13, 0, 0]),
                ],
            ),
            ScriptBlock(
                [
                    FunctionData(1, [12, 0, 0]),
                    FunctionData(32, [500, 0, 0], True),
                ],
                [
                    FunctionData(14, [256, 0, 40], False, [VendorType.Cranky]),
                    FunctionData(72, [0, 7000, 20], False, [VendorType.Cranky]),
                    FunctionData(18, [3, 0, 0], False, [VendorType.Funky]),
                    FunctionData(16, [0, 0, 0], False, [VendorType.Snide]),
                    FunctionData(3, [0, 18, 0]),
                ],
            ),
            ScriptBlock(
                [
                    FunctionData(1, [13, 0, 0]),
                    FunctionData(4, [data_arg_6.get(vendor, 0), 0, 0]),
                ],
                [
                    FunctionData(15, [data_arg_7.get(vendor, 0), 0, 40]),
                ],
                [VendorType.Candy, VendorType.Funky],
            ),
            ScriptBlock(
                [
                    FunctionData(1, [13, 0, 0]),
                    FunctionData(4, [0, 0, 0]),
                ],
                [
                    FunctionData(15, [661, 0, 40]),
                    FunctionData(1, [14, 0, 0]),
                ],
            ),
            ScriptBlock(
                [
                    FunctionData(1, [14, 0, 0]),
                    FunctionData(21, [1, 0, 0], True),
                ],
                [
                    FunctionData(16, [0, 0, 0], False, [VendorType.Cranky]),
                    FunctionData(38, [0, 0, 0], False, [VendorType.Snide]),
                    FunctionData(69, [1, 0, 255]),
                    FunctionData(38, [0, 0, 0], False, [VendorType.Cranky, VendorType.Candy, VendorType.Funky]),
                    FunctionData(1, [10, 0, 0]),
                ],
            ),
        ]
    )
    # Parse Script to remove anything unused
    script = [x for x in script if vendor in x.exist_vendors]
    for block in script:
        block.conditions = [x for x in block.conditions if vendor in x.exist_vendors]
        block.executions = [x for x in block.executions if vendor in x.exist_vendors]
    return script


def pushNewShopLocationWrite(ROM_COPY: LocalROM, cont_map_id: Maps, obj_id: int, old_vendor: VendorType, new_vendor: VendorType):
    """Write new shop location script to ROM."""
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
    water_ids = [None, None]
    if cont_map_id == Maps.GloomyGalleon:
        if old_vendor == VendorType.Candy:
            water_ids = [94, 17]
        elif old_vendor == VendorType.Funky:
            water_ids = [501, 24]
    new_script_data = getShopkeeperInstanceScript(new_vendor, water_ids[0], water_ids[1])
    script_arr = [
        obj_id,
        len(new_script_data),
        0,
    ]
    for block in new_script_data:
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


def ApplyShopRandomizer(spoiler, ROM_COPY: LocalROM):
    """Write shop locations to ROM."""
    if spoiler.settings.shuffle_shops:
        shop_assortment = spoiler.shuffled_shop_locations
        shop_placement_maps = []
        for level in available_shops:
            shop_array = available_shops[level]
            for shop in shop_array:
                if shop.map not in shop_placement_maps:
                    shop_placement_maps.append(shop.map)
        for map in shop_placement_maps:
            setup_address = getPointerLocation(TableNames.Setups, map)
            lz_address = getPointerLocation(TableNames.Triggers, map)
            shops_in_map = []
            map_level = 0
            for level in available_shops:
                shop_array = available_shops[level]
                for shop in shop_array:
                    if shop.map == map and not shop.locked:
                        shops_in_map.append(shop.shop)
                        map_level = level
            placement_data = []
            for shop in shops_in_map:
                if map_level not in shop_assortment.keys():
                    continue
                shop_data = {}
                new_shop = shop_assortment[map_level][shop]
                new_model = -1
                new_lz = -1
                new_rot = -1
                new_scale = -1
                search_model = -1
                search_lz = -1
                search_rot = -1
                search_scale = -1
                obj_id = None
                search_vars = [shop, new_shop]
                for x_i, x in enumerate(search_vars):
                    if x == Regions.CrankyGeneric:
                        if x_i == 0:
                            search_model = 0x73
                            search_lz = Maps.Cranky
                            search_rot = 180
                            search_scale = 0.95
                        else:
                            new_model = 0x73
                            new_lz = Maps.Cranky
                            new_rot = 180
                            new_scale = 0.95
                    elif x == Regions.CandyGeneric:
                        if x_i == 0:
                            search_model = 0x124
                            search_lz = Maps.Candy
                            search_rot = 0
                            search_scale = 0.95
                        else:
                            new_model = 0x124
                            new_lz = Maps.Candy
                            new_rot = 0
                            new_scale = 0.95
                    elif x == Regions.FunkyGeneric:
                        if x_i == 0:
                            search_model = 0x7A
                            search_lz = Maps.Funky
                            search_rot = 90
                            search_scale = 1.045
                        else:
                            new_model = 0x7A
                            new_lz = Maps.Funky
                            new_rot = 90
                            new_scale = 1.045
                    elif x == Regions.Snide:
                        if x_i == 0:
                            search_model = 0x79
                            search_lz = Maps.Snide
                            search_rot = 270
                            search_scale = 3
                        else:
                            new_model = 0x79
                            new_lz = Maps.Snide
                            new_rot = 270
                            new_scale = 3
                if new_model > -1 and new_lz > -1 and search_model > -1 and search_lz > -1:
                    model_index = -1
                    zone_index = -1
                    ROM_COPY.seek(setup_address)
                    shop_coords = []
                    # Modify Object
                    model2_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
                    for model2_index in range(model2_count):
                        if model_index == -1:
                            obj_start = setup_address + 4 + (model2_index * 0x30)
                            ROM_COPY.seek(obj_start + 0x28)
                            obj_type = int.from_bytes(ROM_COPY.readBytes(2), "big")
                            if obj_type == search_model:
                                model_index = model2_index
                                obj_id = int.from_bytes(ROM_COPY.readBytes(2), "big")
                                ROM_COPY.seek(obj_start)
                                for x in range(3):
                                    shop_coords.append(intf_to_float(int.from_bytes(ROM_COPY.readBytes(4), "big")))
                    # Modify indicator
                    closest_indicator_index = None
                    closest_indicator_dist = 9999999
                    ROM_COPY.seek(setup_address + 4 + (0x30 * model2_count))
                    mys_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
                    actor_block_start = setup_address + 8 + (0x30 * model2_count) + (0x24 * mys_count)
                    ROM_COPY.seek(actor_block_start)
                    act_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
                    for actor_index in range(act_count):
                        act_start = actor_block_start + (actor_index * 0x38) + 4
                        delta_sum = 0
                        ROM_COPY.seek(act_start)
                        for x in range(3):
                            coord_value = intf_to_float(int.from_bytes(ROM_COPY.readBytes(4), "big"))
                            delta = shop_coords[x] - coord_value
                            delta_sum += delta * delta
                        if closest_indicator_index is None or delta_sum < closest_indicator_dist:
                            closest_indicator_index = actor_index
                            closest_indicator_dist = delta_sum
                    closest_start = actor_block_start + 4 + (closest_indicator_index * 0x38)
                    ROM_COPY.seek(closest_start + 0x32)
                    closest_new_type = CustomActors.SpreadCounter if new_model == 0x79 else 70
                    ROM_COPY.writeMultipleBytes(closest_new_type - 0x10, 2)
                    # Modify LZ
                    ROM_COPY.seek(lz_address)
                    lz_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
                    for lz_index in range(lz_count):
                        if zone_index == -1:
                            lz_start = lz_address + 2 + (lz_index * 0x38)
                            ROM_COPY.seek(lz_start + 0x10)
                            lz_type = int.from_bytes(ROM_COPY.readBytes(2), "big")
                            if lz_type == 16:
                                ROM_COPY.seek(lz_start + 0x12)
                                lz_map = int.from_bytes(ROM_COPY.readBytes(2), "big")
                                if lz_map == search_lz:
                                    zone_index = lz_index
                    if model_index > -1 and zone_index > -1:
                        shop_data["model_index"] = model_index
                        shop_data["zone_index"] = zone_index
                        shop_data["replace_model"] = new_model
                        shop_data["original_model"] = search_model
                        shop_data["replace_zone"] = new_lz
                        shop_data["angle_change"] = search_rot - new_rot
                        shop_data["scale_factor"] = search_scale / new_scale
                        shop_data["object_id"] = obj_id
                        placement_data.append(shop_data)
                    else:
                        print(f"ERROR: Couldn't find LZ or Model attributed to shop ({model_index} | {zone_index})")
                else:
                    print("ERROR: Couldn't find shop in assortment")
            for placement in placement_data:
                setup_item = setup_address + 4 + (placement["model_index"] * 0x30)
                zone_item = lz_address + 2 + (placement["zone_index"] * 0x38)
                # Type
                ROM_COPY.seek(setup_item + 0x28)
                ROM_COPY.writeMultipleBytes(placement["replace_model"], 2)
                # Angle
                if placement["angle_change"] != 0:
                    ROM_COPY.seek(setup_item + 0x1C)
                    original_angle = intf_to_float(int.from_bytes(ROM_COPY.readBytes(4), "big"))
                    new_angle = original_angle + placement["angle_change"]
                    if new_angle < 0:
                        new_angle += 360
                    elif new_angle >= 360:
                        new_angle -= 360
                    ROM_COPY.seek(setup_item + 0x1C)
                    ROM_COPY.writeFloat(new_angle)
                # Scale
                ROM_COPY.seek(setup_item + 0xC)
                original_scale = intf_to_float(int.from_bytes(ROM_COPY.readBytes(4), "big"))
                new_scale = original_scale * placement["scale_factor"]
                ROM_COPY.seek(setup_item + 0xC)
                ROM_COPY.writeFloat(new_scale)
                # Get Model X and Z
                ROM_COPY.seek(setup_item)
                model_x = intf_to_float(int.from_bytes(ROM_COPY.readBytes(4), "big"))
                ROM_COPY.seek(setup_item + 0x8)
                model_z = intf_to_float(int.from_bytes(ROM_COPY.readBytes(4), "big"))
                # Get Base Zone X and Z
                if model_x < 0:
                    model_x = int(model_x) + 65536
                else:
                    model_x = int(model_x)
                if model_z < 0:
                    model_z = int(model_z) + 65536
                else:
                    model_z = int(model_z)
                ROM_COPY.seek(zone_item + 0xA)
                lz_id = int.from_bytes(ROM_COPY.readBytes(2), "big")
                if map != Maps.GloomyGalleon or lz_id not in (17, 24):
                    ROM_COPY.seek(zone_item)
                    ROM_COPY.writeMultipleBytes(model_x, 2)
                    ROM_COPY.seek(zone_item + 0x4)
                    ROM_COPY.writeMultipleBytes(model_z, 2)
                # Overwrite new radius
                model_to_vendor_table = {
                    0x73: VendorType.Cranky,
                    0x7A: VendorType.Funky,
                    0x124: VendorType.Candy,
                    0x79: VendorType.Snide,
                }

                base_model_scale = [88, 88]
                if placement["replace_model"] == 0x73:
                    # Cranky
                    base_model_scale = [50, 30]
                elif placement["replace_model"] == 0x7A:
                    # Funky
                    base_model_scale = [55, 25]
                elif placement["replace_model"] == 0x124:
                    # Candy
                    base_model_scale = [40.1, 14]
                elif placement["replace_model"] == 0x79:
                    # Snide
                    base_model_scale = [87.5, 59.5]

                base_model_idx = 0
                if map == Maps.GloomyGalleon and lz_id in (17, 24):
                    base_model_idx = 1
                ROM_COPY.seek(zone_item + 0x6)
                ROM_COPY.writeMultipleBytes(int(base_model_scale[base_model_idx] * new_scale), 2)
                # Loading Zone
                ROM_COPY.seek(zone_item + 0x12)
                ROM_COPY.writeMultipleBytes(placement["replace_zone"], 2)
                original_vendor = model_to_vendor_table.get(placement["original_model"], None)
                new_vendor = model_to_vendor_table.get(placement["replace_model"], None)
                if original_vendor is None:
                    raise Exception(f"Original vendor could not be found (Model: {placement['original_model']})")
                if new_vendor is None:
                    raise Exception(f"New vendor could not be found (Model: {placement['replace_model']})")
                pushNewShopLocationWrite(ROM_COPY, map, placement["object_id"], original_vendor, new_vendor)
