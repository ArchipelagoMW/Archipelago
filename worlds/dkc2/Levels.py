
from worlds.AutoWorld import World
from .Names import RegionName

level_list = [
    [RegionName.pirate_panic_level, 0x03],
    [RegionName.mainbrace_mayhem_level, 0x0C],
    [RegionName.gangplank_galley_level, 0x04],
    [RegionName.lockjaws_locker_level, 0x15],
    [RegionName.topsail_trouble_level, 0x0B],
    [RegionName.hot_head_hop_level, 0x07],
    [RegionName.kannons_klaim_level, 0x25],
    [RegionName.lava_lagoon_level, 0x14],
    [RegionName.red_hot_ride_level, 0x08],
    [RegionName.squawks_shaft_level, 0x24],
    [RegionName.barrel_bayou_level, 0x28],
    [RegionName.glimmers_galleon_level, 0x01],
    [RegionName.krockhead_klamber_level, 0x29],
    [RegionName.rattle_battle_level, 0x05],
    [RegionName.slime_climb_level, 0x0A],
    [RegionName.bramble_blast_level, 0x2D],
    [RegionName.hornet_hole_level, 0x11],
    [RegionName.target_terror_level, 0x0E],
    [RegionName.bramble_scramble_level, 0x2E],
    [RegionName.rickety_race_level, 0x0F],
    [RegionName.mudhole_marsh_level, 0x2C],
    [RegionName.rambi_rumble_level, 0x02],
    [RegionName.ghostly_grove_level, 0x19],
    [RegionName.haunted_hall_level, 0x10],
    [RegionName.gusty_glade_level, 0x18],
    [RegionName.parrot_chute_panic_level, 0x13],
    [RegionName.web_woods_level, 0x17],
    [RegionName.arctic_abyss_level, 0x6C],
    [RegionName.windy_well_level, 0x23],
    [RegionName.castle_crush_level, 0x62],
    [RegionName.clappers_cavern_level, 0x8F],
    [RegionName.chain_link_chamber_level, 0x6D],
    [RegionName.toxic_tower_level, 0x6E],
    [RegionName.screechs_sprint_level, 0x2F],
    [RegionName.jungle_jinx_level, 0x99],
    [RegionName.black_ice_battle_level, 0x96],
    [RegionName.klobber_karnage_level, 0x80],
    [RegionName.fiery_furnace_level, 0x16],
    [RegionName.animal_antics_level, 0x9A],
]

boss_list = [
    [RegionName.krows_nest_level, 0x09],
    [RegionName.kleevers_kiln_level, 0x21],
    [RegionName.kudgels_kontest_level, 0x63],
    [RegionName.king_zing_sting_level, 0x60],
    [RegionName.kreepy_krow_level, 0x0D],
    [RegionName.stronghold_showdown_level, 0xB9],
]

level_connections = {
    RegionName.pirate_panic_map: RegionName.pirate_panic_level,
    RegionName.mainbrace_mayhem_map: RegionName.mainbrace_mayhem_level,
    RegionName.gangplank_galley_map: RegionName.gangplank_galley_level,
    RegionName.lockjaws_locker_map: RegionName.lockjaws_locker_level,
    RegionName.topsail_trouble_map: RegionName.topsail_trouble_level,
    RegionName.hot_head_hop_map: RegionName.hot_head_hop_level,
    RegionName.kannons_klaim_map: RegionName.kannons_klaim_level,
    RegionName.lava_lagoon_map: RegionName.lava_lagoon_level,
    RegionName.red_hot_ride_map: RegionName.red_hot_ride_level,
    RegionName.squawks_shaft_map: RegionName.squawks_shaft_level,
    RegionName.barrel_bayou_map: RegionName.barrel_bayou_level,
    RegionName.glimmers_galleon_map: RegionName.glimmers_galleon_level,
    RegionName.krockhead_klamber_map: RegionName.krockhead_klamber_level,
    RegionName.rattle_battle_map: RegionName.rattle_battle_level,
    RegionName.slime_climb_map: RegionName.slime_climb_level,
    RegionName.bramble_blast_map: RegionName.bramble_blast_level,
    RegionName.hornet_hole_map: RegionName.hornet_hole_level,
    RegionName.target_terror_map: RegionName.target_terror_level,
    RegionName.bramble_scramble_map: RegionName.bramble_scramble_level,
    RegionName.rickety_race_map: RegionName.rickety_race_level,
    RegionName.mudhole_marsh_map: RegionName.mudhole_marsh_level,
    RegionName.rambi_rumble_map: RegionName.rambi_rumble_level,
    RegionName.ghostly_grove_map: RegionName.ghostly_grove_level,
    RegionName.haunted_hall_map: RegionName.haunted_hall_level,
    RegionName.gusty_glade_map: RegionName.gusty_glade_level,
    RegionName.parrot_chute_panic_map: RegionName.parrot_chute_panic_level,
    RegionName.web_woods_map: RegionName.web_woods_level,
    RegionName.arctic_abyss_map: RegionName.arctic_abyss_level,
    RegionName.windy_well_map: RegionName.windy_well_level,
    RegionName.castle_crush_map: RegionName.castle_crush_level,
    RegionName.clappers_cavern_map: RegionName.clappers_cavern_level,
    RegionName.chain_link_chamber_map: RegionName.chain_link_chamber_level,
    RegionName.toxic_tower_map: RegionName.toxic_tower_level,
    RegionName.screechs_sprint_map: RegionName.screechs_sprint_level,
    RegionName.jungle_jinx_map: RegionName.jungle_jinx_level,
    RegionName.black_ice_battle_map: RegionName.black_ice_battle_level,
    RegionName.klobber_karnage_map: RegionName.klobber_karnage_level,
    RegionName.fiery_furnace_map: RegionName.fiery_furnace_level,
    RegionName.animal_antics_map: RegionName.animal_antics_level,
}

boss_connections = {
    RegionName.krows_nest_map: RegionName.krows_nest_level,
    RegionName.kleevers_kiln_map: RegionName.kleevers_kiln_level,
    RegionName.kudgels_kontest_map: RegionName.kudgels_kontest_level,
    RegionName.king_zing_sting_map: RegionName.king_zing_sting_level,
    RegionName.kreepy_krow_map: RegionName.kreepy_krow_level,
    RegionName.stronghold_showdown_map: RegionName.stronghold_showdown_level,
}

level_rom_data = {
    RegionName.pirate_panic_level:          [0x34DD6F+9, 0x34DD7E],
    RegionName.mainbrace_mayhem_level:      [0x34DD9C+9, 0x34DDB3],
    RegionName.gangplank_galley_level:      [0x34D24D+9, 0x34D260],
    RegionName.lockjaws_locker_level:       [0x34D2BA+9, 0x34D2CD],
    RegionName.topsail_trouble_level:       [0x34D2F2+9, 0x34D305],
    RegionName.hot_head_hop_level:          [0x34D3CF+9, 0x34D3E2],
    RegionName.kannons_klaim_level:         [0x34D481+9, 0x34D498],
    RegionName.lava_lagoon_level:           [0x34D4F0+9, 0x34D507],
    RegionName.red_hot_ride_level:          [0x34D54E+9, 0x34D565],
    RegionName.squawks_shaft_level:         [0x34D5B5+9, 0x34D5C8],
    RegionName.barrel_bayou_level:          [0x34D620+9, 0x34D62F],
    RegionName.glimmers_galleon_level:      [0x34D64D+9, 0x34D664],
    RegionName.krockhead_klamber_level:     [0x34D68A+9, 0x34D6A1],
    RegionName.rattle_battle_level:         [0x34D6CD+9, 0x34D6E4],
    RegionName.slime_climb_level:           [0x34D738+9, 0x34D74F],
    RegionName.bramble_blast_level:         [0x34D771+9, 0x34D784],
    RegionName.hornet_hole_level:           [0x34E032+9, 0x34E045],
    RegionName.target_terror_level:         [0x34DEEB+9, 0x34DEFE],
    RegionName.bramble_scramble_level:      [0x34DF21+9, 0x34DF38],
    RegionName.rickety_race_level:          [0x34DF5F+9, 0x34DF72],
    RegionName.mudhole_marsh_level:         [0x34DE21+9, 0x34DE38],
    RegionName.rambi_rumble_level:          [0x34DE57+9, 0x34DE6A],
    RegionName.ghostly_grove_level:         [0x34D8C1+9, 0x34D8D0],
    RegionName.haunted_hall_level:          [0x34D921+9, 0x34D934],
    RegionName.gusty_glade_level:           [0x34D97A+9, 0x34D991],
    RegionName.parrot_chute_panic_level:    [0x34D9EC+9, 0x34DA07],
    RegionName.web_woods_level:             [0x34DA96+9, 0x34DAA9],
    RegionName.arctic_abyss_level:          [0x34DAF2+9, 0x34DB09],
    RegionName.windy_well_level:            [0x34DB58+9, 0x34DB6B],
    RegionName.castle_crush_level:          [0x34DBE9+9, 0x34DBFC],
    RegionName.clappers_cavern_level:       [0x34DC1B+9, 0x34DC2E],
    RegionName.chain_link_chamber_level:    [0x34DC54+9, 0x34DC6B],
    RegionName.toxic_tower_level:           [0x34DD06+9, 0x34DD19],
    RegionName.screechs_sprint_level:       [0x34E15B+9, 0x34E172],
    RegionName.jungle_jinx_level:           [0x34E26C+9, 0x34E27F],
    RegionName.black_ice_battle_level:      [0x34E33A+9, 0x34E34D],
    RegionName.klobber_karnage_level:       [0x34E41F+9, 0x34E432],
    RegionName.fiery_furnace_level:         [0x34E4F9+9, 0x34E50C],
    RegionName.animal_antics_level:         [0x34E5D5+9, 0x34E5E8],
}

boss_rom_data = {
    RegionName.krows_nest_level:            [0x34D363+9, 0x34D372],
    RegionName.kleevers_kiln_level:         [0x34D5ED+9, 0x34D5FC],
    RegionName.kudgels_kontest_level:       [0x34D7A3+9, 0x34D7B2],
    RegionName.king_zing_sting_level:       [0x34DEBB+9, 0x34DECA],
    RegionName.kreepy_krow_level:           [0x34DAC4+9, 0x34DAD3],
    RegionName.stronghold_showdown_level:   [0x34DD34+9, 0x34DD43],
}

def generate_level_list(world: World):
    shuffled_level_list = level_list.copy()
    shuffled_boss_list = boss_list.copy()
    if world.options.shuffle_levels:
        world.random.shuffle(shuffled_level_list)
        world.random.shuffle(shuffled_boss_list)

    for map_level, level in level_connections.items():
        selected_level = shuffled_level_list.pop(0)
        world.level_connections[map_level] = selected_level[0]
        world.rom_connections[level] = selected_level[1]

    for map_boss, boss in boss_connections.items():
        selected_boss = shuffled_boss_list.pop(0)
        world.level_connections[map_boss] = selected_boss[0]
        world.rom_connections[boss] = selected_boss[1]

location_id_to_level_id = {
}
