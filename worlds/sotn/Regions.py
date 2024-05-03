from BaseClasses import MultiWorld, Region

from .Locations import SotnLocation, enemy_locations, drop_locations, castle_table, exploration_table


def create_regions(multiworld: MultiWorld, player: int) -> None:
    open_no4 = multiworld.opened_no4[player]
    open_are = multiworld.opened_are[player]
    open_no2 = multiworld.opened_no2[player]
    esanity = multiworld.enemysanity[player]
    dsanity = multiworld.dropsanity[player]

    regions_dict = {
        1: Region("Colosseum", player, multiworld),
        2: Region("Catacombs", player, multiworld),
        4: Region("Abandoned Mine", player, multiworld),
        5: Region("Royal Chapel", player, multiworld),
        7: Region("Long Library", player, multiworld),
        8: Region("Marble Gallery", player, multiworld),
        9: Region("Outer Wall", player, multiworld),
        10: Region("Olrox's Quarters", player, multiworld),
        11: Region("Castle Entrance", player, multiworld),
        13: Region("Underground Caverns", player, multiworld),
        14: Region("Alchemy Laboratory", player, multiworld),
        15: Region("Clock Tower", player, multiworld),
        16: Region("Castle Keep", player, multiworld),
        18: Region("Reverse Colosseum", player, multiworld),
        19: Region("Floating Catacombs", player, multiworld),
        20: Region("Reverse Center Cube", player, multiworld),
        21: Region("Cave", player, multiworld),
        22: Region("Anti-Chapel", player, multiworld),
        23: Region("Forbidden Library", player, multiworld),
        24: Region("Black Marble Gallery", player, multiworld),
        25: Region("Reverse Outer Wall", player, multiworld),
        26: Region("Death Wing's Lair", player, multiworld),
        27: Region("Reverse Entrance", player, multiworld),
        28: Region("Reverse Caverns", player, multiworld),
        29: Region("Necromancy Laboratory", player, multiworld),
        30: Region("Reverse Clock Tower", player, multiworld),
        31: Region("Reverse Castle Keep", player, multiworld),
    }

    menu = Region("Menu", player, multiworld)
    multiworld.regions.append(menu)

    name_to_region = {value.name: value for key, value in regions_dict.items()}
    for k, v in castle_table.items():
        region = name_to_region[v.zone]
        region.locations.append(SotnLocation(player, k, v.location_id, region))

    # Exploration locations
    no3 = name_to_region["Castle Entrance"]
    for k, v in exploration_table.items():
        no3.locations.append(SotnLocation(player, k, v.location_id, no3))


    if esanity:
        for k, v in enemy_locations.items():
            region = name_to_region[v.zone]
            region.locations.append(SotnLocation(player, k, v.location_id, region))
    if dsanity:
        for k, v in drop_locations.items():
            region = name_to_region[v.zone]
            region.locations.append(SotnLocation(player, k, v.location_id, region))

    for k, v in regions_dict.items():
        multiworld.regions.append(v)

    menu.connect(name_to_region["Castle Entrance"])
    # Colosseum
    if not open_are:
        name_to_region["Colosseum"].connect(name_to_region["Royal Chapel"], "ARE->DAI", lambda state: (state.has("Form of mist", player) and
                    state.has("Power of mist", player)) or state.has("Gravity boots", player) or
                    state.has("Leap stone", player) or state.has("Soul of bat", player))
    else:
        # Could access normally or thru back door coming from NZ1 or NZ0
        name_to_region["Colosseum"].connect(name_to_region["Royal Chapel"], "ARE->DAI", lambda state: (state.has("Form of mist", player) and
                    state.has("Power of mist", player)) or state.has("Gravity boots", player) or
                    state.has("Leap stone", player) or state.has("Soul of bat", player) or
                    state.has("Jewel of open", player))
    name_to_region["Colosseum"].connect(name_to_region["Olrox's Quarters"])
    # Catacombs
    name_to_region["Catacombs"].connect(name_to_region["Abandoned Mine"])
    # Abandoned Mine
    name_to_region["Abandoned Mine"].connect(name_to_region["Catacombs"])
    name_to_region["Abandoned Mine"].connect(name_to_region["Underground Caverns"])
    # Royal Chapel
    name_to_region["Royal Chapel"].connect(name_to_region["Alchemy Laboratory"], "DAI->NZ0", lambda state: state.has("Jewel of open", player) or
                state.has("Leap stone", player) or state.has("Soul of bat", player) or
                (state.has("Form of mist", player) and state.has("Power of mist", player)))
    if not open_are:
        name_to_region["Royal Chapel"].connect(name_to_region["Colosseum"], "DAI->ARE", lambda state: (state.has("Form of mist", player) and
                    state.has("Power of mist", player)) or state.has("Gravity boots", player) or
                    state.has("Leap stone", player) or state.has("Soul of bat", player))
    else:
        name_to_region["Royal Chapel"].connect(name_to_region["Colosseum"], "DAI->ARE", lambda state: (state.has("Form of mist", player) and
                    state.has("Power of mist", player)) or state.has("Gravity boots", player) or
                    state.has("Leap stone", player) or state.has("Soul of bat", player) or
                    state.has("Jewel of open", player))
    if not open_no2:
        name_to_region["Royal Chapel"].connect(name_to_region["Olrox's Quarters"], "DAI->NO2", lambda state: (state.has("Form of mist", player) and
                    state.has("Power of mist", player)) or state.has("Soul of bat", player) or
                    state.has("Leap stone", player) or state.has("Gravity boots", player))
    else:
        name_to_region["Royal Chapel"].connect(name_to_region["Olrox's Quarters"], "DAI->NO2", lambda state: (state.has("Form of mist", player) and
                    state.has("Power of mist", player)) or state.has("Soul of bat", player) or
                    state.has("Leap stone", player) or state.has("Gravity boots", player) or
                    state.has("Jewel of open", player))

    name_to_region["Royal Chapel"].connect(name_to_region["Castle Keep"])
    # Long Library
    name_to_region["Long Library"].connect(name_to_region["Outer Wall"])
    # Marble Gallery
    name_to_region["Marble Gallery"].connect(name_to_region["Outer Wall"])
    name_to_region["Marble Gallery"].connect(name_to_region["Olrox's Quarters"], "NO0->NO2", lambda state: state.has("Leap stone", player) or
                state.has("Soul of bat", player) or (state.has("Form of mist", player) and
                state.has("Power of mist", player)) or state.has("Gravity boots", player))
    name_to_region["Marble Gallery"].connect(name_to_region["Underground Caverns"], "NO0->NO4", lambda state: state.has("Jewel of open", player))
    name_to_region["Marble Gallery"].connect(name_to_region["Castle Entrance"])
    name_to_region["Marble Gallery"].connect(name_to_region["Alchemy Laboratory"])
    # Outer Wall
    name_to_region["Outer Wall"].connect(name_to_region["Long Library"])
    name_to_region["Outer Wall"].connect(name_to_region["Marble Gallery"])
    name_to_region["Outer Wall"].connect(name_to_region["Clock Tower"], "NO1->NZ1", lambda state: state.has("Leap stone", player) or
                state.has("Soul of bat", player) or
                (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                state.has("Gravity boots", player))
    # reinforce NZ1->TOP
    # Olrox's Quarters
    name_to_region["Olrox's Quarters"].connect(name_to_region["Royal Chapel"])
    if not open_no2:
        name_to_region["Olrox's Quarters"].connect(name_to_region["Colosseum"])
    else:
        (name_to_region["Olrox's Quarters"].connect(name_to_region["Colosseum"], "NO2->ARE"), lambda state: state.has("Soul of bat", player) or
                    (state.has("Gravity boots", player)) and (state.has("Leap stone", player) or
                                                               state.has("Soul of wolf", player) or
                                                               state.has("Form of mist", player)) or
                    (state.has("Form of mist", player) and state.has("Power of mist", player)))
    name_to_region["Olrox's Quarters"].connect(name_to_region["Marble Gallery"], "NO2->NO0", lambda state: state.has("Leap stone", player) or
                state.has("Soul of bat", player) or
                (state.has("Form of mist", player) and state.has("Power of mist", player)))
    # Castle Entrance
    if not open_no4:
        name_to_region["Castle Entrance"].connect(name_to_region["Underground Caverns"], "NO3->NO4", lambda state: (state.has("Jewel of open", player)))
    else:
        name_to_region["Castle Entrance"].connect(name_to_region["Underground Caverns"])
    name_to_region["Castle Entrance"].connect(name_to_region["Alchemy Laboratory"])
    name_to_region["Castle Entrance"].connect(name_to_region["Marble Gallery"])
    # Underground Caverns
    name_to_region["Underground Caverns"].connect(name_to_region["Marble Gallery"], "NO4->NO0", lambda state: state.has("Jewel of open", player))
    if not open_no4:
        name_to_region["Underground Caverns"].connect(name_to_region["Castle Entrance"], "NO4->NO3", lambda state: state.has("Jewel of open", player))
        name_to_region["Underground Caverns"].connect(name_to_region["Abandoned Mine"], "NO4->CHI", lambda state: state.has("Leap stone", player) or
                    state.has("Soul of bat", player) or (state.has("Form of mist", player) and
                                                         state.has("Power of mist", player)) or
                    (state.has("Gravity boots", player) and state.has("Leap stone", player)) or
                    (state.has("Soul of wolf", player) and state.has("Power of wolf", player)))
    else:
        name_to_region["Underground Caverns"].connect(name_to_region["Castle Entrance"])
        name_to_region["Underground Caverns"].connect(name_to_region["Abandoned Mine"], "NO4->CHI", lambda state: state.has("Soul of bat", player) or
                    (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                    (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                             state.has("Soul of wolf", player) or
                                                             state.has("Form of mist", player))))
    # Alchemy Laboratory
    name_to_region["Alchemy Laboratory"].connect(name_to_region["Marble Gallery"])
    name_to_region["Alchemy Laboratory"].connect(name_to_region["Castle Entrance"])
    name_to_region["Alchemy Laboratory"].connect(name_to_region["Royal Chapel"], "NZ0->DAI", lambda state: (state.has("Jewel of open", player)))
    # Clock Tower
    name_to_region["Clock Tower"].connect(name_to_region["Outer Wall"])
    name_to_region["Clock Tower"].connect(name_to_region["Castle Keep"], "NZ1->TOP", lambda state: state.has("Leap stone", player) or
                state.has("Soul of bat", player) or state.has("Gravity boots", player) or
                (state.has("Form of mist", player) and state.has("Power of mist", player)))
    # Castle Keep
    name_to_region["Castle Keep"].connect(name_to_region["Clock Tower"], "TOP->NZ1", lambda state: state.has("Soul of bat", player) or
                state.has("Gravity boots", player) or
                (state.has("Form of mist", player) and state.has("Power of mist", player)))
    name_to_region["Castle Keep"].connect(name_to_region["Royal Chapel"])
    name_to_region["Castle Keep"].connect(name_to_region["Reverse Castle Keep"], "TOP->RTOP", lambda state: state.has("Holy glasses", player) and
                (state.has("Soul of bat", player) or (state.has("Gravity boots", player) and
                (state.has("Soul of wolf", player) or state.has("Form of mist", player))) or
                (state.has("Form of mist", player) and state.has("Power of mist", player))))
    # Reverse Keep
    name_to_region["Reverse Castle Keep"].connect(name_to_region["Castle Keep"], "RTOP->TOP", lambda state: state.has("Holy glasses", player) and
                (state.has("Soul of bat", player) or (state.has("Gravity boots", player) and
                (state.has("Soul of wolf", player) or state.has("Form of mist", player))) or
                (state.has("Form of mist", player) and state.has("Power of mist", player))))
    name_to_region["Reverse Castle Keep"].connect(name_to_region["Anti-Chapel"])
    name_to_region["Reverse Castle Keep"].connect(name_to_region["Reverse Clock Tower"])
    # Anti-Chapel
    name_to_region["Anti-Chapel"].connect(name_to_region["Reverse Castle Keep"])
    name_to_region["Anti-Chapel"].connect(name_to_region["Death Wing's Lair"])
    name_to_region["Anti-Chapel"].connect(name_to_region["Reverse Colosseum"])
    name_to_region["Anti-Chapel"].connect(name_to_region["Necromancy Laboratory"])
    # Reverse Clock Tower
    name_to_region["Reverse Clock Tower"].connect(name_to_region["Reverse Castle Keep"])
    name_to_region["Reverse Clock Tower"].connect(name_to_region["Reverse Outer Wall"])
    # Death Wing's Lair
    name_to_region["Death Wing's Lair"].connect(name_to_region["Anti-Chapel"])
    name_to_region["Death Wing's Lair"].connect(name_to_region["Reverse Colosseum"])
    name_to_region["Death Wing's Lair"].connect(name_to_region["Black Marble Gallery"])
    # Reverse Colosseum
    name_to_region["Reverse Colosseum"].connect(name_to_region["Reverse Clock Tower"])
    name_to_region["Reverse Colosseum"].connect(name_to_region["Death Wing's Lair"])
    # Necromancy Laboratory
    name_to_region["Necromancy Laboratory"].connect(name_to_region["Anti-Chapel"])
    name_to_region["Necromancy Laboratory"].connect(name_to_region["Black Marble Gallery"])
    name_to_region["Necromancy Laboratory"].connect(name_to_region["Reverse Entrance"])
    # Reverse Outer Wall
    name_to_region["Reverse Outer Wall"].connect(name_to_region["Reverse Clock Tower"])
    name_to_region["Reverse Outer Wall"].connect(name_to_region["Forbidden Library"])
    name_to_region["Reverse Outer Wall"].connect(name_to_region["Black Marble Gallery"])
    # Black Marble Gallery
    name_to_region["Black Marble Gallery"].connect(name_to_region["Death Wing's Lair"])
    name_to_region["Black Marble Gallery"].connect(name_to_region["Reverse Outer Wall"])
    name_to_region["Black Marble Gallery"].connect(name_to_region["Reverse Caverns"])
    name_to_region["Black Marble Gallery"].connect(name_to_region["Reverse Entrance"])
    name_to_region["Black Marble Gallery"].connect(name_to_region["Necromancy Laboratory"])
    name_to_region["Black Marble Gallery"].connect(name_to_region["Reverse Center Cube"], "RNO0->RCEN", lambda state: state.has("Heart of vlad", player) and
                 state.has("Tooth of vlad", player) and state.has("Rib of vlad", player) and
                 state.has("Ring of vlad", player) and state.has("Eye of vlad", player))
    # Reverse Center Cube
    name_to_region["Reverse Center Cube"]. connect(name_to_region["Black Marble Gallery"])
    # Reverse Castle Entrance
    name_to_region["Reverse Entrance"].connect(name_to_region["Death Wing's Lair"])
    name_to_region["Reverse Entrance"].connect(name_to_region["Black Marble Gallery"])
    name_to_region["Reverse Entrance"].connect(name_to_region["Reverse Caverns"])
    # Forbidden Library
    name_to_region["Forbidden Library"].connect(name_to_region["Reverse Outer Wall"])
    # Reverse Caverns
    name_to_region["Reverse Caverns"].connect(name_to_region["Black Marble Gallery"])
    name_to_region["Reverse Caverns"].connect(name_to_region["Reverse Entrance"])
    name_to_region["Reverse Caverns"].connect(name_to_region["Cave"])
    # Cave
    name_to_region["Cave"].connect(name_to_region["Reverse Caverns"])
    name_to_region["Cave"].connect(name_to_region["Floating Catacombs"])
    # Floating Catacombs
    name_to_region["Floating Catacombs"].connect(name_to_region["Cave"])
