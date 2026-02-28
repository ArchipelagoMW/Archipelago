"""Randomize puzzles."""

import math
from enum import IntEnum, auto
from randomizer.Enums.Maps import Maps
from randomizer.Patching.Patcher import LocalROM
from randomizer.Patching.Library.Generic import IsDDMSSelected
from randomizer.Patching.Library.DataTypes import float_to_hex
from randomizer.Patching.Library.Assets import getPointerLocation, TableNames
from randomizer.Patching.Library.ASM import getROMAddress, populateOverlayOffsets, getSym, Overlay
from randomizer.Enums.Settings import FasterChecksSelected, PuzzleRando


def chooseSFX(rando):
    """Choose random SFX from bank of acceptable SFX."""
    banks = [[98, 138], [166, 247], [249, 252], [398, 411], [471, 476], [519, 535], [547, 575], [614, 631], [644, 650]]
    bank = rando.choice(banks)
    return rando.randint(bank[0], bank[1])


def shiftCastleMinecartRewardZones(ROM_COPY: LocalROM):
    """Shifts the triggers for the reward point in castle minecart."""
    cont_map_lzs_address = getPointerLocation(TableNames.Triggers, Maps.CastleMinecarts)
    ROM_COPY.seek(cont_map_lzs_address)
    lz_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
    for lz_id in range(lz_count):
        start = (lz_id * 0x38) + 2
        ROM_COPY.seek(cont_map_lzs_address + start + 0x10)
        lz_type = int.from_bytes(ROM_COPY.readBytes(2), "big")
        lz_extra_data = int.from_bytes(ROM_COPY.readBytes(2), "big")
        if lz_type == 0xA and lz_extra_data == 4:
            # Turn around zone
            offsets = [2, 6, 8]
            for offset in offsets:
                ROM_COPY.seek(cont_map_lzs_address + start + offset)
                ROM_COPY.writeMultipleBytes(0, 2)
        elif lz_type == 0x0 and lz_extra_data == 5:
            new_location = (3232, 482, 693)
            for c in range(3):
                ROM_COPY.seek(cont_map_lzs_address + start + (c * 2))
                ROM_COPY.writeMultipleBytes(new_location[c], 2)
            ROM_COPY.seek(cont_map_lzs_address + start + 6)
            ROM_COPY.writeMultipleBytes(40, 2)


class CarRaceArea(IntEnum):
    """Car Race Area enum."""

    null = auto()
    # Castle Car Race
    castle_car_start_finish = auto()
    ramp_up = auto()
    ramp_down = auto()
    tunnel_in = auto()
    tunnel_out = auto()
    around_dartboard_boxes = auto()  # Used for enemy AI pathing
    around_arcade_stairs = auto()  # Used for enemy AI pathing
    high_turn_around = auto()  # Used for enemy AI Pathing


class RaceBound:
    """Class to store information regarding a race bound."""

    def __init__(
        self,
        start_x: int,
        start_z: int,
        end_x: int,
        end_z: int,
        direction_is_x: bool,
        checkpoint_count: int,
        area: CarRaceArea = CarRaceArea.null,
    ):
        """Initialize with given parameters."""
        self.start_x = start_x
        self.end_x = end_x
        self.start_z = start_z
        self.end_z = end_z
        self.direction_is_x = direction_is_x
        self.checkpoint_count = checkpoint_count
        self.area = area
        self.placement_radius = 80

    def getPoints(self, random, y_level: int, placement_bubbles: list) -> list:
        """Get list of points."""
        if self.area == CarRaceArea.null:
            arr = []
            i = 0
            lower_x = min(self.start_x, self.end_x)
            upper_x = max(self.start_x, self.end_x)
            lower_z = min(self.start_z, self.end_z)
            upper_z = max(self.start_z, self.end_z)
            while i < self.checkpoint_count:
                x = random.randint(lower_x, upper_x)
                z = random.randint(lower_z, upper_z)
                allowed = True
                for bubble in placement_bubbles:
                    dx = bubble[0] - x
                    dz = bubble[1] - z
                    dxz2 = (dx * dx) + (dz * dz)
                    if dxz2 < (bubble[2] * bubble[2]):
                        allowed = False
                        break
                if allowed:
                    arr.append((x, y_level, z))
                    placement_bubbles.append([x, z, self.placement_radius])
                    i += 1
            return arr.copy()
        elif self.area == CarRaceArea.ramp_up:
            return [(2106, 1026, 1122), (1685, 1113, 735)]
        elif self.area == CarRaceArea.ramp_down:
            return [(1738, 1113, 731), (2128, 1026, 1119)]
        elif self.area == CarRaceArea.tunnel_in:
            return [(2779, 1026, 1138), (3045, 1026, 1085)]
        elif self.area == CarRaceArea.tunnel_out:
            return [(3045, 1026, 1085), (2779, 1026, 1138)]
        elif self.area == CarRaceArea.castle_car_start_finish:
            return [(2733, 1026, 1308)]
        elif self.area == CarRaceArea.around_dartboard_boxes:
            return [(2431, 1026, 1166), (2567, 1026, 1157)]
        elif self.area == CarRaceArea.around_arcade_stairs:
            return [(2061, 1026, 1446), (2095, 1026, 1299)]
        elif self.area == CarRaceArea.high_turn_around:
            return [(1565, 1113, 625)]
        return []

    def getAngle(self, random) -> int:
        """Get angle for a checkpoint."""
        if self.area == CarRaceArea.castle_car_start_finish:
            return 0
        angle_offset = random.randint(-300, 300)
        if self.direction_is_x:
            if self.start_x > self.end_x:
                return angle_offset + 3072
            else:
                return angle_offset + 1024
        else:
            if self.start_z > self.end_z:
                return angle_offset + 2048
            else:
                new_angle = angle_offset
                if new_angle < 0:
                    new_angle += 4096
                return new_angle


def writeRandomCastleCarRace(random, ROM_COPY: LocalROM):
    """Write random castle car race pathing."""
    # Castle Car Race
    placement_bubbles = []
    bounds = [
        RaceBound(2641, 1419, 2517, 1581, True, 1),
        # RaceBound(2517, 1581, 2352, 1402, True, 1),
        RaceBound(2346, 1450, 2003, 1554, True, 1),
        RaceBound(0, 0, 0, 0, False, 0, CarRaceArea.around_arcade_stairs),
        RaceBound(2073, 1307, 2307, 1194, False, 1),
        RaceBound(0, 0, 0, 0, False, 0, CarRaceArea.ramp_up),  # Ramp Up
        RaceBound(1698, 778, 1625, 579, True, 1),  # Forward
        RaceBound(0, 0, 0, 0, False, 0, CarRaceArea.high_turn_around),
        RaceBound(1625, 579, 1698, 778, True, 1),  # Back
        RaceBound(0, 0, 0, 0, False, 0, CarRaceArea.ramp_down),  # Ramp Down
        RaceBound(2189, 1111, 2380, 1010, True, 1),
        RaceBound(0, 0, 0, 0, False, 0, CarRaceArea.around_dartboard_boxes),
        RaceBound(2560, 990, 2692, 1183, True, 1),
        RaceBound(0, 0, 0, 0, False, 0, CarRaceArea.tunnel_in),  # Tunnel In
        RaceBound(3070, 1090, 3205, 987, True, 1),
        RaceBound(3205, 1090, 3070, 1162, True, 1),
        RaceBound(0, 0, 0, 0, False, 0, CarRaceArea.tunnel_out),  # Tunnel Out
        RaceBound(0, 0, 0, 0, False, 1, CarRaceArea.castle_car_start_finish),  # Start/Finish Line
    ]
    enemy_car_checkpoints = []
    y_level = 1026
    checkpoint_bytes_order = []
    for bound in bounds:
        if bound.area == CarRaceArea.ramp_up:
            y_level = 1113
        elif bound.area == CarRaceArea.ramp_down:
            y_level = 1026
        new_points = bound.getPoints(random, y_level, placement_bubbles)
        if bound.area in (CarRaceArea.null, CarRaceArea.castle_car_start_finish):
            for i in range(bound.checkpoint_count):
                local_bytes = []
                for j in range(3):
                    local_bytes.extend([(new_points[i][j] & 0xFF00) >> 8, new_points[i][j] & 0xFF])
                angle = bound.getAngle(random)
                angle_rad = (angle / 2048) * math.pi
                local_bytes.extend([(angle & 0xFF00) >> 8, angle & 0xFF])
                s_angle = int(float_to_hex(math.sin(angle_rad)), 16)
                c_angle = int(float_to_hex(math.cos(angle_rad)), 16)
                for strength in [s_angle, c_angle]:
                    strength_arr = [0, 0, 0, 0]
                    val = strength
                    for j in range(4):
                        strength_arr[3 - j] = val & 0xFF
                        val >>= 8
                    local_bytes.extend(strength_arr)
                local_bytes.append(2)  # Goal
                local_bytes.append(0)  # unk11 - always 0
                local_bytes.extend([0, 0])  # unk12 - always 0
                if bound.area == CarRaceArea.castle_car_start_finish:
                    local_bytes.extend([0x00, 0x00, 0x00, 0x00])  # Scale
                else:
                    local_bytes.extend([0x3F, 0x80, 0x00, 0x00])  # Scale
                local_bytes.extend([2, 0])  # Always 512
                check_type = 0x27 if bound.area == CarRaceArea.null else 0x1A
                local_bytes.extend([0, check_type])  # Seen values of 26,39,42,43,44,47,48,49,50,53,55,65,89,90,110,124
                checkpoint_bytes_order.append(local_bytes)
        enemy_car_checkpoints.extend(new_points)
    will_reverse = random.randint(0, 3) == 0
    if will_reverse and False:
        temp_checkpoints = enemy_car_checkpoints[:-1]
        temp_check_bytes = checkpoint_bytes_order[:-1]
        sf_checkpoint = enemy_car_checkpoints[-1]
        sf_check_bytes = checkpoint_bytes_order[-1]
        temp_checkpoints.reverse()
        temp_check_bytes.reverse()
        temp_checkpoints.append(sf_checkpoint)
        temp_check_bytes.append(sf_check_bytes)
        enemy_car_checkpoints = temp_checkpoints.copy()
        checkpoint_bytes_order = temp_check_bytes.copy()
    # Write Enemy Car AI
    checkpoint_ai_mapping = [
        0xF,
        0x0,
        0x01,
        0x1D,
        0x02,
        0x19,
        0x03,
        0x18,
        0x04,
        0x06,
        0x07,
        0x08,
        0x09,
        0x15,
        0x1C,
        0x12,
        0x10,
        0x05,
        0x0A,
        0x0B,
        0x0C,
        0x0D,
        0x13,
        0x0E,
        0x14,
        0x1B,
        0x1A,
        0x11,
    ]
    map_spawners = getPointerLocation(TableNames.Spawners, Maps.CastleTinyRace)
    for point in range(len(checkpoint_ai_mapping)):
        slot = checkpoint_ai_mapping[point]
        ROM_COPY.seek(map_spawners + 36 + (slot * 0xA))
        point_filtered = point
        if point_filtered >= len(enemy_car_checkpoints):
            point_filtered = len(enemy_car_checkpoints) - 1
        coords = enemy_car_checkpoints[point_filtered]
        if len(coords) != 3:
            raise Exception("Invalid tuple size for Castle Car Race.")
        if slot in (22, 23):  # Positions used for the end of Castle Car Race
            raise Exception("Invalid slot for Castle Car Race.")
        for item in coords:
            ROM_COPY.writeMultipleBytes(item, 2)
    # Write checkpoint file
    checkpoint_raw_bytes = []
    for check in checkpoint_bytes_order:
        checkpoint_raw_bytes.extend(check)
    start_bytes = [1, 0, len(checkpoint_bytes_order), 0, len(checkpoint_bytes_order)]
    for x in range(len(checkpoint_bytes_order)):
        start_bytes.extend([0, x])  # Add Checkpoint mapping
    start_bytes.extend(checkpoint_raw_bytes)
    if (len(start_bytes) & 0xF) != 0:
        diff = 0x10 - (len(start_bytes) & 0xF)
        for _ in range(diff):
            start_bytes.append(0)
    map_checkpoints = getPointerLocation(TableNames.RaceCheckpoints, Maps.CastleTinyRace)
    ROM_COPY.seek(map_checkpoints)
    ROM_COPY.writeBytes(bytearray(start_bytes))


def shortenCastleMinecart(spoiler, ROM_COPY: LocalROM):
    """Shorten Castle Minecart to end at the u-turn point."""
    if not IsDDMSSelected(
        spoiler.settings.faster_checks_selected,
        FasterChecksSelected.castle_minecart,
    ):
        return
    if spoiler.settings.race_coin_rando:
        return
    shiftCastleMinecartRewardZones(ROM_COPY)
    new_squawks_coords = (3232, 482, 693)
    old_squawks_coords = (619, 690, 4134)
    cont_map_spawner_address = getPointerLocation(TableNames.Spawners, Maps.CastleMinecarts)
    ROM_COPY.seek(cont_map_spawner_address)
    fence_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
    offset = 2
    fence_bytes = []
    used_fence_ids = []
    fence_4_data = {"fence_6": [], "fence_A": [], "footer": 1}
    if fence_count > 0:
        for x in range(fence_count):
            fence = []
            fence_start = cont_map_spawner_address + offset
            ROM_COPY.seek(cont_map_spawner_address + offset)
            point_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
            point_6_offset = offset + 2
            offset += (point_count * 6) + 2
            ROM_COPY.seek(cont_map_spawner_address + offset)
            point0_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
            offset + 2
            offset += (point0_count * 10) + 6
            fence_finish = cont_map_spawner_address + offset
            fence_size = fence_finish - fence_start
            ROM_COPY.seek(fence_finish - 4)
            fence_id = int.from_bytes(ROM_COPY.readBytes(2), "big")
            used_fence_ids.append(fence_id)
            ROM_COPY.seek(fence_start)
            for y in range(int(fence_size / 2)):
                fence.append(int.from_bytes(ROM_COPY.readBytes(2), "big"))
            fence_bytes.append(fence)
            if fence_id == 4:
                # Vanilla Squawks Fence
                for p in range(point_count):
                    ROM_COPY.seek(cont_map_spawner_address + point_6_offset + (p * 6))
                    local_coords = []
                    for c in range(3):
                        local_coords.append(int.from_bytes(ROM_COPY.readBytes(2), "big"))
                    fence_4_data["fence_6"].append(local_coords)
                # for p in range(point0_count):
                #     ROM_COPY.seek(cont_map_spawner_address + point_A_offset + (p * 10))
                #     local_coords = []
                #     for c in range(5):
                #         local_coords.append(int.from_bytes(ROM_COPY.readBytes(2), "big"))
                #     fence_4_data["fence_A"].append(local_coords)
            ROM_COPY.seek(fence_finish)
    spawner_count_location = cont_map_spawner_address + offset
    ROM_COPY.seek(spawner_count_location)
    spawner_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
    offset += 2
    spawner_bytes = []
    used_enemy_indexes = []
    # Get new fence index
    fence_index = 1
    if fence_index in used_fence_ids:
        while fence_index in used_fence_ids:
            fence_index += 1
        used_fence_ids.append(fence_index)
    # Read Spawners
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
        # Get New Spawner Bytes
        data_bytes = []
        spawner_size = end_offset - init_offset
        ROM_COPY.seek(cont_map_spawner_address + init_offset)
        for x in range(spawner_size):
            value = int.from_bytes(ROM_COPY.readBytes(1), "big")
            if enemy_id == 0x35 and enemy_index == 5:
                if x >= 4 and x < 10:
                    coord_slot = int((x - 4) / 2)
                    coord_top = (x - 4) % 2
                    coord_val = new_squawks_coords[coord_slot]
                    write_val = coord_val & 0xFF
                    if coord_top == 0:
                        write_val = (coord_val >> 8) & 0xFF
                    value = write_val
                elif x == 0xE:
                    value = fence_index
            data_bytes.append(value)
        spawner_bytes.append(data_bytes)
    # Create new fence
    new_fence_bytes = []
    new_fence_bytes.append(len(fence_4_data["fence_6"]))  # 0: Fence Block 0x6 Count, 1: Fence Block 0xA Count
    for point in fence_4_data["fence_6"]:
        for yi, y in enumerate(point):
            diff = y - old_squawks_coords[yi]
            new_fence_bytes.append(new_squawks_coords[yi] + diff)
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


class PuzzleRandoBound:
    """Class to store information regarding the bounds of a puzzle requirement."""

    def __init__(self, lower: int, upper: int):
        """Initialize with given parameters."""
        self.lower = lower
        self.upper = upper
        self.selected = None

    def generateRequirement(self, spoiler) -> int:
        """Generate random requirement between the upper and lower bounds."""
        lower = self.lower
        lower_mid = int((((self.upper - self.lower) / 3) * 1) + self.lower)
        upper_mid = int((((self.upper - self.lower) / 3) * 2) + self.lower)
        upper = self.upper
        selected_upper = upper
        selected_lower = lower
        puzzle_setting = spoiler.settings.puzzle_rando_difficulty
        if puzzle_setting == PuzzleRando.easy:
            selected_lower = lower
            selected_upper = lower_mid
        elif puzzle_setting == PuzzleRando.medium:
            selected_lower = lower_mid
            selected_upper = upper_mid
        elif puzzle_setting == PuzzleRando.hard:
            selected_lower = upper_mid
            selected_upper = upper
        self.selected = spoiler.settings.random.randint(selected_lower, selected_upper)
        return self.selected


class PuzzleItem:
    """Class to store information regarding a puzzle requirement."""

    def __init__(
        self,
        name: str,
        tied_map: Maps,
        offset: int,
        normal_bound: PuzzleRandoBound,
        fast_bound: PuzzleRandoBound = None,
        fast_check_setting: FasterChecksSelected = None,
    ):
        """Initialize with given parameters."""
        self.name = name
        self.tied_map = tied_map
        self.offset = offset
        self.normal_bound = normal_bound
        self.fast_bound = fast_bound
        self.fast_check_setting = fast_check_setting
        self.selected_bound = self.normal_bound

    def updateBoundSetting(self, spoiler):
        """Update the settings regarding bounds depending on selected settings."""
        self.selected_bound = self.normal_bound
        if self.fast_check_setting is not None and self.fast_bound is not None:
            if IsDDMSSelected(spoiler.settings.faster_checks_selected, self.fast_check_setting):
                self.selected_bound = self.fast_bound


coin_req_info = [
    PuzzleItem("Caves Beetle Race", Maps.CavesLankyRace, 3, PuzzleRandoBound(10, 60)),
    PuzzleItem("Aztec Beetle Race", Maps.AztecTinyRace, 0, PuzzleRandoBound(20, 60)),
    PuzzleItem(
        "Factory Car Race",
        Maps.FactoryTinyRace,
        4,
        PuzzleRandoBound(5, 18),
        PuzzleRandoBound(3, 12),
        FasterChecksSelected.factory_car_race,
    ),
    PuzzleItem(
        "Galleon Seal Race",
        Maps.GalleonSealRace,
        6,
        PuzzleRandoBound(5, 12),
        PuzzleRandoBound(5, 10),
        FasterChecksSelected.galleon_seal_race,
    ),
    PuzzleItem(
        "Castle Car Race",
        Maps.CastleTinyRace,
        5,
        PuzzleRandoBound(5, 15),
        PuzzleRandoBound(5, 12),
        FasterChecksSelected.castle_car_race,
    ),
    PuzzleItem("Japes Minecart", Maps.JapesMinecarts, 1, PuzzleRandoBound(40, 70)),
    PuzzleItem("Forest Minecart", Maps.ForestMinecarts, 2, PuzzleRandoBound(25, 60)),
    PuzzleItem(
        "Castle Minecart",
        Maps.CastleMinecarts,
        7,
        PuzzleRandoBound(10, 45),
        PuzzleRandoBound(5, 30),
        FasterChecksSelected.castle_minecart,
    ),
]


def patchRaceRequirements(spoiler, ROM_COPY: LocalROM):
    """Patches the randomized requirements for the races."""
    puzzle_rando_setting = spoiler.settings.puzzle_rando_difficulty
    race_coin_rando_on = spoiler.settings.race_coin_rando
    if puzzle_rando_setting == PuzzleRando.off and not race_coin_rando_on:
        return
    offset_dict = populateOverlayOffsets(ROM_COPY)
    ram_addr = getSym("CoinHUDElements")
    rom_addr = getROMAddress(ram_addr, Overlay.Custom, offset_dict)
    for coinreq in coin_req_info:
        ROM_COPY.seek(rom_addr + (4 * coinreq.offset) + 2)
        ROM_COPY.writeMultipleBytes(spoiler.coin_requirements[coinreq.tied_map], 2)


race_coin_rando_ratios = {PuzzleRando.off: 0.6, PuzzleRando.easy: 0.4, PuzzleRando.medium: 0.6, PuzzleRando.hard: 0.75}


def randomizeRaceRequirements(spoiler):
    """Randomize the requirements for the races."""
    puzzle_rando_setting = spoiler.settings.puzzle_rando_difficulty
    race_coin_rando_on = spoiler.settings.race_coin_rando
    spoiler.coin_requirements = {}
    if puzzle_rando_setting == PuzzleRando.off and not race_coin_rando_on:
        return
    max_requirement_ratio = 0.6
    if puzzle_rando_setting == PuzzleRando.chaos:
        max_requirement_ratio = spoiler.settings.random.uniform(0.4, 0.8)
    else:
        max_requirement_ratio = race_coin_rando_ratios.get(puzzle_rando_setting, 0.6)

    max_coins = int((97 + 71 + 25 + 19 + 87 + 77 + 68 + 17) * max_requirement_ratio)
    delineations = len(coin_req_info)
    requirements = []
    for index in range(delineations):
        min_bound = int(max_coins * ((index / delineations)))
        max_bound = int(max_coins * (((index + 1) / delineations)))
        if min_bound > max_coins:
            min_bound = max_coins
        elif min_bound < 1:
            min_bound = 1
        if max_bound > max_coins:
            max_bound = max_coins
        # Random range, with bias towards the higher values so that it's more likely to push the requirements higher than lower
        selected_requirement = int(spoiler.settings.random.triangular(min_bound, max_bound, int(0.75 * ((max_bound + min_bound) / 2))))
        requirements.append(selected_requirement)
    spoiler.settings.random.shuffle(requirements)  # Shuffle so it's not always Caves beetle getting a low req
    for index, coinreq in enumerate(coin_req_info):
        coinreq.updateBoundSetting(spoiler)
        selected_requirement = None
        if race_coin_rando_on:
            selected_requirement = requirements[index]
        else:
            selected_requirement = coinreq.selected_bound.generateRequirement(spoiler)
        spoiler.coin_requirements[coinreq.tied_map] = selected_requirement


def randomize_puzzles(spoiler, ROM_COPY: LocalROM):
    """Shuffle elements of puzzles."""
    patchRaceRequirements(spoiler, ROM_COPY)
    sav = spoiler.settings.rom_data
    if spoiler.settings.puzzle_rando_difficulty != PuzzleRando.off:
        chosen_sounds = []
        for matching_head in range(8):
            ROM_COPY.seek(sav + 0x15C + (2 * matching_head))
            sfx = chooseSFX(spoiler.settings.random)
            while sfx in chosen_sounds:
                sfx = chooseSFX(spoiler.settings.random)
            chosen_sounds.append(sfx)
            ROM_COPY.writeMultipleBytes(sfx, 2)
        for piano_item in range(7):
            ROM_COPY.seek(sav + 0x16C + piano_item)
            key = spoiler.settings.random.randint(0, 5)
            ROM_COPY.writeMultipleBytes(key, 1)
        spoiler.dk_face_puzzle = [None] * 9
        spoiler.chunky_face_puzzle = [None] * 9
        for face_puzzle_square in range(9):
            value = spoiler.settings.random.randint(0, 3)
            if face_puzzle_square == 8:
                value = spoiler.settings.random.choice([0, 1, 3])  # Lanky for this square glitches out the puzzle. Nice going Loser kong
            spoiler.dk_face_puzzle[face_puzzle_square] = value
            value = spoiler.settings.random.randint(0, 3)
            if face_puzzle_square == 2:
                value = spoiler.settings.random.choice([0, 1, 3])  # Lanky for this square glitches out the puzzle. Nice going Loser kong again
            spoiler.chunky_face_puzzle[face_puzzle_square] = value
        # Arcade Level Order Rando
        arcade_levels = ["25m", "50m", "75m", "100m"]
        arcade_level_data = {
            "25m": 1,
            "50m": 4,
            "75m": 3,
            "100m": 2,
        }
        spoiler.settings.random.shuffle(arcade_levels)
        if False:  # Testing the feedback on just ditching this rule
            # Make sure 75m isn't in the first 2 levels if faster arcade is enabled because 75m is hard
            if IsDDMSSelected(spoiler.settings.faster_checks_selected, FasterChecksSelected.arcade):
                for x in range(2):
                    if arcade_levels[x] == "75m":
                        temp_level = arcade_levels[2]
                        arcade_levels[2] = arcade_levels[x]
                        arcade_levels[x] = temp_level
        spoiler.arcade_order = [0] * 4
        for lvl_index, lvl in enumerate(arcade_levels):
            spoiler.arcade_order[lvl_index] = arcade_level_data[lvl]
    if spoiler.settings.puzzle_rando_difficulty in (PuzzleRando.hard, PuzzleRando.chaos):
        # Random Race Paths
        race_data = {
            # Maps.AngryAztec: {
            #     "offset": 0x21E,
            #     "center_x": 3280,
            #     "center_z": 3829,
            #     "radius": [70, 719],
            #     "y": [190, 530],
            #     "count": 16,
            #     "size": 10,
            #     "start_angle": None,
            # },
            # Maps.FungiForest: {
            #     "offset": 0xC2,
            #     "center_x": 1276,
            #     "center_z": 3825,
            #     "radius": [246, 587],
            #     "y": [231, 650],
            #     "count": 32,
            #     "size": 10,
            #     "start_angle": 0,
            # },
        }
        for map_index in race_data:
            map_spawners = getPointerLocation(TableNames.Spawners, map_index)
            map_data = race_data[map_index]
            if map_data["start_angle"] is None:
                initial_angle = spoiler.settings.random.randint(0, 359)
            else:
                initial_angle = map_data["start_angle"]
            previous_offset = None
            for point in range(map_data["count"]):
                ROM_COPY.seek(map_spawners + map_data["offset"] + (point * 0xA))
                if previous_offset is None:
                    angle_offset = spoiler.settings.random.randint(-90, 90)
                else:
                    angle_magnitude = spoiler.settings.random.randint(0, 90)
                    direction = -1
                    if previous_offset > 0:
                        direction = 1
                    change_direction = spoiler.settings.random.randint(0, 3) == 0
                    if change_direction:
                        direction *= -1
                    angle_offset = direction * angle_magnitude
                previous_offset = angle_offset
                initial_angle += angle_offset
                radius = spoiler.settings.random.randint(map_data["radius"][0], map_data["radius"][1])
                angle_rad = (initial_angle / 180) * math.pi
                x = int(map_data["center_x"] + (radius * math.sin(angle_rad)))
                y = spoiler.settings.random.randint(map_data["y"][0], map_data["y"][1])
                z = int(map_data["center_z"] + (radius * math.cos(angle_rad)))
                ROM_COPY.writeMultipleBytes(x, 2)
                ROM_COPY.writeMultipleBytes(y, 2)
                ROM_COPY.writeMultipleBytes(z, 2)
        writeRandomCastleCarRace(spoiler.settings.random, ROM_COPY)
