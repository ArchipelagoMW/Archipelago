"""Apply Coin Rando changes."""

import math
from randomizer.Patching.Library.DataTypes import float_to_hex
from randomizer.Patching.Library.Assets import getPointerLocation, TableNames
from randomizer.Patching.Patcher import LocalROM
from randomizer.Enums.Maps import Maps

MINIGAME_MAPS = [
    Maps.StashSnatchEasy,
    Maps.StashSnatchNormal,
    Maps.StashSnatchHard,
    Maps.StashSnatchInsane,
    Maps.SplishSplashSalvageEasy,
    Maps.SplishSplashSalvageNormal,
    Maps.SplishSplashSalvageHard,
    Maps.SpeedySwingSortieEasy,
    Maps.SpeedySwingSortieNormal,
    Maps.SpeedySwingSortieHard,
    Maps.DiveBarrel,
    Maps.VineBarrel,
    Maps.MinecartMayhemEasy,
    Maps.MinecartMayhemNormal,
    Maps.MinecartMayhemHard,
]


def randomize_coins(spoiler, ROM_COPY: LocalROM):
    """Place Coins into ROM."""
    if spoiler.settings.coin_rando or spoiler.settings.race_coin_rando:
        for cont_map_id in range(216):
            # Wipe setup and paths of Coin information
            if cont_map_id in MINIGAME_MAPS:
                continue
            # SETUP
            items_to_remove = []
            coin_items = [0x1D, 0x24, 0x23, 0x1C, 0x27]  # Has to remain in this order
            if spoiler.settings.coin_rando:
                items_to_remove.extend(coin_items)  # Banana Coins
            if spoiler.settings.race_coin_rando:
                items_to_remove.append(236)  # Race Coins
            setup_table = getPointerLocation(TableNames.Setups, cont_map_id)
            ROM_COPY.seek(setup_table)
            model2_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
            # Model Two Coins
            persisted_m2_data = []
            used_m2_ids = []
            for item in range(model2_count):
                item_start = setup_table + 4 + (item * 0x30)
                ROM_COPY.seek(item_start + 0x28)
                item_type = int.from_bytes(ROM_COPY.readBytes(2), "big")
                if item_type not in items_to_remove:  # Not Coin
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
            for item in range(actor_count):
                actor_start = actor_block + 4 + (item * 0x38)
                ROM_COPY.seek(actor_start + 0x34)
                used_actor_ids.append(int.from_bytes(ROM_COPY.readBytes(2), "big"))
                ROM_COPY.seek(actor_start)
                item_data = []
                for x in range(int(0x38 / 4)):
                    item_data.append(int.from_bytes(ROM_COPY.readBytes(4), "big"))
                persisted_act_data.append(item_data)
            # Place all new coins
            new_id = 0
            placement_data = [
                {
                    "enabled": spoiler.settings.coin_rando,
                    "placements": spoiler.coin_placements,
                    "kong_arr_check": True,
                    "arr": coin_items,
                },
                {
                    "enabled": spoiler.settings.race_coin_rando,
                    "placements": spoiler.race_coin_placements,
                    "kong_arr_check": False,
                    "arr": [236],
                },
            ]
            for data in placement_data:
                if data["enabled"]:
                    for new_coin in data["placements"]:
                        if new_coin["map"] == cont_map_id:
                            # Model Two Coins
                            for loc in new_coin["locations"]:
                                item_data = []
                                item_data.extend(
                                    [
                                        int(float_to_hex(loc[1]), 16),
                                        int(float_to_hex(loc[2]), 16),
                                        int(float_to_hex(loc[3]), 16),
                                        int(float_to_hex(loc[0]), 16),
                                    ]
                                )
                                item_data.append(2)
                                item_data.append(0x01C7FFFF)
                                for x in range(int((0x24 - 0x18) / 4)):
                                    item_data.append(0)
                                item_data.append(0x40400000)
                                if data["kong_arr_check"]:
                                    coin_item_type = data["arr"][new_coin["kong"]]
                                else:
                                    coin_item_type = data["arr"][0]
                                found_vacant = False
                                found_id = 0
                                while not found_vacant:
                                    if new_id not in used_m2_ids:
                                        used_m2_ids.append(new_id)
                                        found_id = new_id
                                        found_vacant = True
                                    new_id += 1
                                item_data.append((coin_item_type << 16) + found_id)
                                item_data.append((2 << 16) + 1)
                                persisted_m2_data.append(item_data)
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


MAYHEM_Y_POSITION = 170
MAYHEM_BANDS = [
    # Ring 0 (Outer)
    [
        (602, 517),  # TL
        (54, 529),  # TR
        (46, 56),  # BR
    ],
    # Ring 1
    [
        (548, 477),  # TL
        (103, 487),  # TR
        (95, 86),  # BR
        (554, 108),  # BL
    ],
    # Ring 2
    [
        (503, 443),  # TL
        (145, 427),  # TR
        (145, 141),  # BR
        (517, 135),  # BL
    ],
    # Ring 3 (Inner)
    [
        (461, 386),  # TL
        (189, 385),  # TR
        (181, 184),  # BR
        (468, 179),  # BL
    ],
]


def gen_mayhem_coins(settings, random):
    """Generate the list of coin locations."""
    settings.mayhem_coins = [[], [], []]
    if not settings.alt_minecart_mayhem:
        return
    for y in range(3):
        bubbles = []
        placement_count = 15
        while placement_count > 0:
            band = random.randint(0, 3)
            band_lst = MAYHEM_BANDS[band]
            if band == 0:
                start = random.randint(0, 1)
            else:
                start = random.randint(0, len(band_lst) - 1)
            end = start + 1
            if end == len(band_lst):
                end = 0
            delta_x = band_lst[end][0] - band_lst[start][0]
            delta_z = band_lst[end][1] - band_lst[start][1]
            prog = random.uniform(0, 1)
            x = band_lst[start][0] + (prog * delta_x)
            z = band_lst[start][1] + (prog * delta_z)
            close_to_a_bubble = False
            for bubble in bubbles:
                dx = bubble[0] - x
                dz = bubble[1] - z
                if ((dx * dx) + (dz * dz)) < (20 * 20):  # Within 20 units
                    close_to_a_bubble = True
            if not close_to_a_bubble:
                settings.mayhem_coins[y].append((x, MAYHEM_Y_POSITION, z))
                bubbles.append((x, z))
                placement_count -= 1


def place_mayhem_coins(spoiler, ROM_COPY: LocalROM):
    """Place the minecart mayhem coins in the setup."""
    if not spoiler.settings.alt_minecart_mayhem:
        return
    minecart_maps = (Maps.MinecartMayhemEasy, Maps.MinecartMayhemNormal, Maps.MinecartMayhemHard)
    for index, map_id in enumerate(minecart_maps):
        setup_table = getPointerLocation(TableNames.Setups, map_id)
        ROM_COPY.seek(setup_table)
        file_data = b""
        model2_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
        file_data += ROM_COPY.readBytes(model2_count * 0x30)
        # Add in extra coins
        new_id = 0
        for coin in spoiler.settings.mayhem_coins[index]:
            coin_data = [
                int(float_to_hex(coin[0]), 16),  # 00
                int(float_to_hex(coin[1]), 16),  # 04
                int(float_to_hex(coin[2]), 16),  # 08
                int(float_to_hex(2), 16),  # 0C
                2,  # 10
                0x01C7FFFF,  # 14
                0,  # 18
                0,  # 1C
                0,  # 20
                0x40400000,  # 24
            ]
            # ID calculation
            found_vacant = False
            found_id = 0
            used_m2_ids = []
            while not found_vacant:
                if new_id not in used_m2_ids:
                    used_m2_ids.append(new_id)
                    found_id = new_id
                    found_vacant = True
                new_id += 1
            coin_data.append((236 << 16) + found_id)  # 28
            coin_data.append((2 << 16) + 1)  # 2C
            for item in coin_data:
                file_data += item.to_bytes(4, "big")
            model2_count += 1
        # Mystery
        mys_bytes = ROM_COPY.readBytes(4)
        mys_count = int.from_bytes(mys_bytes, "big")
        file_data += mys_bytes
        file_data += ROM_COPY.readBytes(mys_count * 0x24)
        # Actors
        act_bytes = ROM_COPY.readBytes(4)
        act_count = int.from_bytes(act_bytes, "big")
        file_data += act_bytes
        file_data += ROM_COPY.readBytes(act_count * 0x38)
        # Write it back
        ROM_COPY.seek(setup_table)
        ROM_COPY.writeMultipleBytes(model2_count, 4)
        ROM_COPY.writeBytes(file_data)
