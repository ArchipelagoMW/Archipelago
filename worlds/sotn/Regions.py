from BaseClasses import MultiWorld, Region

from .Locations import are_locations, cat_locations, chi_locations, dai_locations, lib_locations, no0_locations, \
                        no1_locations, no2_locations, no3_locations, no4_locations, nz0_locations, nz1_locations, \
                        top_locations, SotnLocation, rare_locations, rcat_locations, rcen_locations, rchi_locations, \
                        rdai_locations, rlib_locations, rno0_locations, rno1_locations, rno2_locations, \
                        rno3_locations, rno4_locations, rnz0_locations, rnz1_locations, rtop_locations, \
                        exp_locations_item, exp_locations_token


def create_regions(multiworld: MultiWorld, player: int) -> None:
    open_no4 = multiworld.opened_no4[player]
    open_are = multiworld.opened_are[player]
    open_no2 = multiworld.opened_no2[player]

    menu = Region("Menu", player, multiworld)
    multiworld.regions.append(menu)
    # TODO: Google a better way of doing this in python iterate over dicts with similar names and different sizes
    are = Region("Colosseum", player,multiworld)
    for k, v in are_locations.items():
        are.locations.append(SotnLocation(player, k, v.location_id, are))
    cat = Region("Catacombs", player, multiworld)
    for k, v in cat_locations.items():
        cat.locations.append(SotnLocation(player, k, v.location_id, cat))
    chi = Region("Abandoned Mine", player, multiworld)
    for k, v in chi_locations.items():
        chi.locations.append(SotnLocation(player, k, v.location_id, chi))
    dai = Region("Royal Chapel", player, multiworld)
    for k, v in dai_locations.items():
        dai.locations.append(SotnLocation(player, k, v.location_id, dai))
    lib = Region("Long Library", player, multiworld)
    for k, v in lib_locations.items():
        lib.locations.append(SotnLocation(player, k, v.location_id, lib))
    no0 = Region("Marble Gallery", player, multiworld)
    for k, v in no0_locations.items():
        no0.locations.append(SotnLocation(player, k, v.location_id, no0))
    no1 = Region("Outer Wall", player, multiworld)
    for k, v in no1_locations.items():
        no1.locations.append(SotnLocation(player, k, v.location_id, no1))
    no2 = Region("Olrox's Quarters", player, multiworld)
    for k, v in no2_locations.items():
        no2.locations.append(SotnLocation(player, k, v.location_id, no2))
    no3 = Region("Castle Entrance", player, multiworld)
    for k, v in no3_locations.items():
        no3.locations.append(SotnLocation(player, k, v.location_id, no3))
    for k, v in exp_locations_token.items():
        no3.locations.append(SotnLocation(player, k, v.location_id, no3))
    for k, v in exp_locations_item.items():
        no3.locations.append(SotnLocation(player, k, v.location_id, no3))
    no4 = Region("Underground Caverns", player, multiworld)
    for k, v in no4_locations.items():
        no4.locations.append(SotnLocation(player, k, v.location_id, no4))
    nz0 = Region("Alchemy Laboratory", player, multiworld)
    for k, v in nz0_locations.items():
        nz0.locations.append(SotnLocation(player, k, v.location_id, nz0))
    nz1 = Region("Clock Tower", player, multiworld)
    for k, v in nz1_locations.items():
        nz1.locations.append(SotnLocation(player, k, v.location_id, nz1))
    top = Region("Castle Keep", player, multiworld)
    for k, v in top_locations.items():
        top.locations.append(SotnLocation(player, k, v.location_id, top))
    # Reverse Castle
    rare = Region("Reverse Colosseum", player, multiworld)
    for k, v in rare_locations.items():
        rare.locations.append(SotnLocation(player, k, v.location_id, rare))
    rcat = Region("Floating Catacombs", player, multiworld)
    for k, v in rcat_locations.items():
        rcat.locations.append(SotnLocation(player, k, v.location_id, rcat))
    rcen = Region("Reverse Center Cube", player, multiworld)
    for k, v in rcen_locations.items():
        rcen.locations.append(SotnLocation(player, k, v.location_id, rcen))
    rchi = Region("Cave", player, multiworld)
    for k, v in rchi_locations.items():
        rchi.locations.append(SotnLocation(player, k, v.location_id, rchi))
    rdai = Region("Anti-Chapel", player, multiworld)
    for k, v in rdai_locations.items():
        rdai.locations.append(SotnLocation(player, k, v.location_id, rdai))
    rlib = Region("Forbidden Library", player, multiworld)
    for k, v in rlib_locations.items():
        rlib.locations.append(SotnLocation(player, k, v.location_id, rlib))
    rno0 = Region("Black Marble Gallery", player, multiworld)
    for k, v in rno0_locations.items():
        rno0.locations.append(SotnLocation(player, k, v.location_id, rno0))
    rno1 = Region("Reverse Outer Wall", player, multiworld)
    for k, v in rno1_locations.items():
        rno1.locations.append(SotnLocation(player, k, v.location_id, rno1))
    rno2 = Region("Death Wing's Lair", player, multiworld)
    for k, v in rno2_locations.items():
        rno2.locations.append(SotnLocation(player, k, v.location_id, rno2))
    rno3 = Region("Reverse Entrance", player, multiworld)
    for k, v in rno3_locations.items():
        rno3.locations.append(SotnLocation(player, k, v.location_id, rno3))
    rno4 = Region("Reverse Caverns", player, multiworld)
    for k, v in rno4_locations.items():
        rno4.locations.append(SotnLocation(player, k, v.location_id, rno4))
    rnz0 = Region("Necromancy Laboratory", player, multiworld)
    for k, v in rnz0_locations.items():
        rnz0.locations.append(SotnLocation(player, k, v.location_id, rnz0))
    rnz1 = Region("Reverse Clock Tower", player, multiworld)
    for k, v in rnz1_locations.items():
        rnz1.locations.append(SotnLocation(player, k, v.location_id, rnz1))
    rtop = Region("Reverse Catle Keep", player, multiworld)
    for k, v in rtop_locations.items():
        rtop.locations.append(SotnLocation(player, k, v.location_id, rtop))

    multiworld.regions.append(are)
    multiworld.regions.append(cat)
    multiworld.regions.append(chi)
    multiworld.regions.append(dai)
    multiworld.regions.append(lib)
    multiworld.regions.append(no0)
    multiworld.regions.append(no1)
    multiworld.regions.append(no2)
    multiworld.regions.append(no3)
    multiworld.regions.append(no4)
    multiworld.regions.append(nz0)
    multiworld.regions.append(nz1)
    multiworld.regions.append(top)
    # Reverse Castle
    multiworld.regions.append(rare)
    multiworld.regions.append(rcat)
    multiworld.regions.append(rchi)
    multiworld.regions.append(rdai)
    multiworld.regions.append(rlib)
    multiworld.regions.append(rno0)
    multiworld.regions.append(rno1)
    multiworld.regions.append(rno2)
    multiworld.regions.append(rno3)
    multiworld.regions.append(rno4)
    multiworld.regions.append(rnz0)
    multiworld.regions.append(rnz1)
    multiworld.regions.append(rtop)

    menu.connect(no3)
    # Colosseum
    if not open_are:
        are.connect(dai, "ARE->DAI", lambda state: (state.has("Form of mist", player) and
                    state.has("Power of mist", player)) or state.has("Gravity boots", player) or
                    state.has("Leap stone", player) or state.has("Soul of bat", player))
    else:
        # Could access normally or thru back door coming from NZ1 or NZ0
        are.connect(dai, "ARE->DAI", lambda state: (state.has("Form of mist", player) and
                    state.has("Power of mist", player)) or state.has("Gravity boots", player) or
                    state.has("Leap stone", player) or state.has("Soul of bat", player) or
                    state.has("Jewel of open", player))
    are.connect(no2)
    # Catacombs
    cat.connect(chi)
    # Abandoned Mine
    chi.connect(cat)
    chi.connect(no4)
    # Royal Chapel
    dai.connect(nz0, "DAI->NZ0", lambda state: state.has("Jewel of open", player) or
                state.has("Leap stone", player) or state.has("Soul of bat", player) or
                (state.has("Form of mist", player) and state.has("Power of mist", player)))
    if not open_are:
        dai.connect(are, "DAI->ARE", lambda state: (state.has("Form of mist", player) and
                    state.has("Power of mist", player)) or state.has("Gravity boots", player) or
                    state.has("Leap stone", player) or state.has("Soul of bat", player))
    else:
        dai.connect(are, "ARE->DAI", lambda state: (state.has("Form of mist", player) and
                    state.has("Power of mist", player)) or state.has("Gravity boots", player) or
                    state.has("Leap stone", player) or state.has("Soul of bat", player) or
                    state.has("Jewel of open", player))
    if not open_no2:
        dai.connect(no2, "DAI->NO2", lambda state: (state.has("Form of mist", player) and
                    state.has("Power of mist", player)) or state.has("Soul of bat", player) or
                    state.has("Leap stone", player) or state.has("Gravity boots", player))
    else:
        dai.connect(no2, "DAI->NO2", lambda state: (state.has("Form of mist", player) and
                    state.has("Power of mist", player)) or state.has("Soul of bat", player) or
                    state.has("Leap stone", player) or state.has("Gravity boots", player) or
                    state.has("Jewel of open", player))

    dai.connect(top)
    # Long Library
    lib.connect(no1)
    # Marble Gallery
    no0.connect(no1)
    no0.connect(no2, "NO0->NO2", lambda state: state.has("Leap stone", player) or
                state.has("Soul of bat", player) or (state.has("Form of mist", player) and
                state.has("Power of mist", player)))
    no0.connect(no4, "NO0->NO4", lambda state: state.has("Jewel of open", player))
    no0.connect(no3)
    no0.connect(nz0)
    # Outer Wall
    no1.connect(lib)
    no1.connect(no0)
    no1.connect(nz1)  # NO1 connect to NZ1 with only 2 items available, better leave the rules to items and
    # reinforce NZ1->TOP
    # Olrox's Quarters
    no2.connect(dai)
    no2.connect(are)
    no2.connect(no0, "NO2->NO0", lambda state: state.has("Leap stone", player) or
                state.has("Soul of bat", player) or
                (state.has("Form of mist", player) and state.has("Power of mist", player)))
    # Castle Entrance
    if not open_no4:
        no3.connect(no4, "NO3->NO4", lambda state: (state.has("Jewel of open", player)))
    else:
        no3.connect(no4)
    no3.connect(nz0)
    no3.connect(no0)
    # Underground Caverns
    no4.connect(no0, "NO4->NO0", lambda state: state.has("Jewel of open", player))
    if not open_no4:
        no4.connect(no3, "NO4->NO3", lambda state: (state.has("Jewel of open", player)))
        no4.connect(chi, "NO4->CHI", lambda state: state.has("Leap stone", player) or
                    state.has("Soul of bat", player) or (state.has("Form of mist", player) and
                                                         state.has("Power of mist", player)) or
                    (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                             state.has("Soul of wolf", player) or
                     state.has("Form of mist", player))) or (state.has("Soul of wolf", player) and
                                                             state.has("Power of wolf", player)))
    else:
        no4.connect(no3)
        no4.connect(chi, "NO4->CHI", lambda state: state.has("Soul of bat", player) or
                    (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                    (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                             state.has("Soul of wolf", player) or
                                                             state.has("Form of mist", player))))
    # Alchemy Laboratory
    nz0.connect(no0)
    nz0.connect(no3)
    nz0.connect(dai, "NZ0->DAI", lambda state: (state.has("Jewel of open", player)))
    # Clock Tower
    nz1.connect(no1)
    nz1.connect(top, "NZ1->TOP", lambda state: state.has("Leap stone", player) or
                state.has("Soul of bat", player) or state.has("Gravity boots", player) or
                (state.has("Form of mist", player) and state.has("Power of mist", player)))
    # Castle Keep
    top.connect(nz1, "TOP->NZ1", lambda state: state.has("Leap stone", player) or
                state.has("Soul of bat", player) or state.has("Gravity boots", player) or
                (state.has("Form of mist", player) and state.has("Power of mist", player)))
    top.connect(dai)
    top.connect(rtop, "TOP->RTOP", lambda state: state.has("Holy glasses", player) and
                (state.has("Soul of bat", player) or (state.has("Gravity boots", player) and
                (state.has("Soul of wolf", player) or state.has("Form of mist", player))) or
                (state.has("Form of mist", player) and state.has("Power of mist", player))))
    # Reverse Keep
    # TODO: Research if connections are reciprocal
    rtop.connect(top, "RTOP->TOP", lambda state: state.has("Holy glasses", player) and
                (state.has("Soul of bat", player) or (state.has("Gravity boots", player) and
                (state.has("Soul of wolf", player) or state.has("Form of mist", player))) or
                (state.has("Form of mist", player) and state.has("Power of mist", player))))
    rtop.connect(rdai)
    rtop.connect(rnz1)
    # Anti-Chapel
    rnz1.connect(rtop)
    rnz1.connect(rno2)
    rnz1.connect(rare)
    rnz1.connect(rnz0)
    # Reverse Clock Tower
    rnz1.connect(rtop)
    rnz1.connect(rno1)
    # Death Wing's Lair
    rno2.connect(rdai)
    rno2.connect(rare)
    rno2.connect(rno0)
    # Reverse Colosseum
    rare.connect(rnz1)
    rare.connect(rno2)
    # Necromancy Laboratory
    rnz0.connect(rdai)
    rnz0.connect(rno0)
    rnz0.connect(rno3)
    # Reverse Outer Wall
    rno1.connect(rnz1)
    rno1.connect(rlib)
    rno1.connect(rno0)
    # Black Marble Gallery
    rno0.connect(rno2)
    rno0.connect(rno1)
    rno0.connect(rno4)
    rno0.connect(rno3)
    rno0.connect(rnz1)
    rno0.connect(rcen, "RNO0->RCEN", lambda state: state.has("Heart of vlad", player) and
                 state.has("Tooth of vlad", player) and state.has("Rib of vlad", player) and
                 state.has("Ring of vlad", player) and state.has("Eye of vlad", player))
    # Reverse Center Cube
    rcen. connect(rno0)
    # Reverse Castle Entrance
    rno3.connect(rnz0)
    rno3.connect(rno0)
    rno3.connect(rno4)
    # Forbidden Library
    rlib.connect(rno1)
    # Reverse Caverns
    rno4.connect(rno0)
    rno4.connect(rno3)
    rno4.connect(rchi)
    # Cave
    rchi.connect(rno4)
    rchi.connect(rcat)
    # Floating Catacombs
    rcat.connect(rchi)
