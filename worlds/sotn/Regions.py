from BaseClasses import MultiWorld, Region

from .Locations import SotnLocation, locations, ZONE, LOCATION_TO_ABREV
from .Rules import sotn_has_flying, sotn_has_any, sotn_has_wolf, sotn_has_reverse, sotn_has_dracula
from .Options import SOTNOptions
from .data.Constants import BASE_LOCATION_ID, EXTENSIONS


def create_regions(multiworld: MultiWorld, player: int, options: SOTNOptions) -> None:
    open_no4 = options.open_no4.value
    open_are = options.open_are.value
    extension = options.extension.value

    regions_dict = {
        1: Region("Colosseum", player, multiworld),
        2: Region("Catacombs", player, multiworld),
        3: Region("Center Cube", player, multiworld),
        4: Region("Abandoned Mine", player, multiworld),
        5: Region("Royal Chapel", player, multiworld),
        7: Region("Long Library", player, multiworld),
        8: Region("Marble Gallery", player, multiworld),
        9: Region("Outer Wall", player, multiworld),
        10: Region("Olrox\'s Quarters", player, multiworld),
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
        26: Region("Death Wing\'s Lair", player, multiworld),
        27: Region("Reverse Entrance", player, multiworld),
        28: Region("Reverse Caverns", player, multiworld),
        29: Region("Necromancy Laboratory", player, multiworld),
        30: Region("Reverse Clock Tower", player, multiworld),
        31: Region("Reverse Castle Keep", player, multiworld),
        32: Region("Lower Underground Caverns", player, multiworld),
        33: Region("Upper Underground Caverns", player, multiworld),
        34: Region("Succubus Underground Caverns", player, multiworld),
        35: Region("Lower Olrox\'s Quarters", player, multiworld),
        36: Region("Upper Olrox\'s Quarters", player, multiworld),
        37: Region("Lower Clock Tower", player, multiworld),
        38: Region("Upper Clock Tower", player, multiworld),
        39: Region("Lower Castle Keep", player, multiworld),
        40: Region("Upper Castle Keep", player, multiworld)
    }

    name_to_region = {value.name: value for key, value in regions_dict.items()}

    menu = Region("Menu", player, multiworld)
    multiworld.regions.append(menu)
    no3 = name_to_region["Castle Entrance"]
    menu.connect(no3)

    # Entrance
    lno4 = name_to_region["Lower Underground Caverns"]
    nz0 = name_to_region["Alchemy Laboratory"]
    no3.connect(nz0)
    if open_no4:
        no3.connect(lno4)

    # Entrance -> Alchemy Laboratory
    no0 = name_to_region["Marble Gallery"]
    dai = name_to_region["Royal Chapel"]
    nz0.connect(no0)
    nz0.connect(dai, rule=lambda state: state.has("Jewel of open", player))

    # Alchemy Laboratory -> Marble Galley
    lno2 = name_to_region["Lower Olrox\'s Quarters"]
    cen = name_to_region["Center Cube"]
    uno4 = name_to_region["Upper Underground Caverns"]
    no1 = name_to_region["Outer Wall"]
    no0.connect(lno2, rule=lambda state: sotn_has_any(state, player))
    no0.connect(cen, rule=lambda state: state.has("Gold ring", player) and state.has("Silver ring", player))
    no0.connect(uno4, rule=lambda state: state.has("Jewel of open", player))
    no0.connect(no1)

    # Marble Gallery -> Outer Wall
    lib = name_to_region["Long Library"]
    lnz1 = name_to_region["Lower Clock Tower"]
    no1.connect(lib)
    no1.connect(lnz1)

    # Outer Wall -> Lower Clock Tower
    unz1 = name_to_region["Upper Clock Tower"]
    lnz1.connect(unz1, rule=lambda state: sotn_has_any(state, player))

    # Lower Clock Tower -> Upper Clock Tower
    ltop = name_to_region["Lower Castle Keep"]
    unz1.connect(ltop)

    # Upper Clock Tower -> Lower Castle Keep
    utop = name_to_region["Upper Castle Keep"]
    ltop.connect(utop, rule=lambda state: sotn_has_flying(state, player))

    # Upper Castle Keep -> Reverse Castle Keep
    rtop = name_to_region["Reverse Castle Keep"]
    utop.connect(rtop, rule=lambda state: sotn_has_reverse(state, player))

    # Lower Castle Keep -> Royal Chapel
    ltop.connect(dai)

    # Royal Chapel -> Colosseum
    are = name_to_region["Colosseum"]
    if open_are:
        dai.connect(are)

    # Royal Chapel -> Lower Castle Keep
    dai.connect(ltop)

    # Entrance -> Lower Underground Caverns
    lno4.connect(uno4, rule=lambda state: sotn_has_flying(state, player))

    # Marble Gallery -> Lower Olrox's Quarters
    uno2 = name_to_region["Upper Olrox\'s Quarters"]
    lno2.connect(are)
    lno2.connect(dai)
    lno2.connect(uno2, rule=lambda state: sotn_has_flying(state, player))

    # Colosseum
    are.connect(dai)
    are.connect(lno2)

    # Upper Olrox's Quarters
    uno2.connect(lno2)

    # Upper Underground Caverns -> Lower Underground Caverns
    uno4.connect(lno4)
    # Upper Underground Caverns -> Succubus Underground Caverns
    sno4 = name_to_region["Succubus Underground Caverns"]
    uno4.connect(sno4, rule=lambda state: sotn_has_flying(state, player))

    # Upper Underground Caverns -> Abandoned Mine
    chi = name_to_region["Abandoned Mine"]
    if open_no4:
        uno4.connect(chi, rule=lambda state: sotn_has_flying(state, player) or ((state.has("Leap stone", player) or
                                                                                 sotn_has_wolf(state, player))))
    else:
        uno4.connect(chi, rule=lambda state: (sotn_has_flying(state, player) or sotn_has_wolf(state, player) or
                                              state.has("Leap stone", player)))

    # Abandoned Mine -> Catacombs
    cat = name_to_region["Catacombs"]
    chi.connect(cat)

    # Connect every reverse region to RTOP
    for k, v in regions_dict.items():
        if k == 20:
            rtop.connect(v, rule=lambda state: sotn_has_dracula(state, player))
        elif (17 < k < 32) and k != 31:
            rtop.connect(v)

    added_locations = []
    # Add locations
    for k, v in locations.items():
        for zone in v["zones"]:
            loc = LOCATION_TO_ABREV[k]
            if zone == ZONE["NO2"]:
                # Olrox's Quarters
                if loc == "" or loc == "" or loc == "":
                    region = name_to_region["Lower Olrox\'s Quarters"]
                else:
                    region = name_to_region["Upper Olrox\'s Quarters"]
            elif zone == ZONE["NO4"]:
                # Underground Caverns
                if loc == "NO4_Shiitake_35" or loc == "NO4_Life Vessel_6" or loc == "Merman statue":
                    region = name_to_region["Lower Underground Caverns"]
                elif "Succubus" in k:
                    region = name_to_region["Succubus Underground Caverns"]
                else:
                    region = name_to_region["Upper Underground Caverns"]
            elif zone == ZONE["NZ1"]:
                # Clock Tower
                if loc == "NZ1_Pentagram_1" or loc == "NZ1_Magic missile_0":
                    region = name_to_region["Lower Clock Tower"]
                else:
                    region = name_to_region["Upper Clock Tower"]
            elif zone == ZONE["TOP"]:
                # Castle Keep
                if loc == "TOP_Tyrfing_3" or loc == "TOP_Turquoise_0" or loc == "TOP_Turkey_1" or loc == "Leap stone":
                    region = name_to_region["Lower Castle Keep"]
                else:
                    region = name_to_region["Upper Castle Keep"]
            elif zone == ZONE["NP3"]:
                # Castle Entrance (after visiting Alchemy Laboratory)
                region = name_to_region["Castle Entrance"]
            else:
                region = regions_dict[zone]

            if k not in added_locations:
                if loc in EXTENSIONS[extension]:
                    region.locations.append(SotnLocation(player, k, v["ap_id"] + BASE_LOCATION_ID, region))
                added_locations.append(k)

    # Add kill Dracula
    region = name_to_region["Reverse Center Cube"]
    region.locations.append(SotnLocation(player, "Reverse Center Cube - Kill Dracula", None, region))
