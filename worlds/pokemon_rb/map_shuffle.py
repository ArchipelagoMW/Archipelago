#from .rom_addresses import rom_addresses


map_ids = {
    "Pallet Town": 0x00,
    "Viridian City": 0x01,
    "Pewter City": 0x02,
    "Cerulean City": 0x03,
    "Lavender Town": 0x04,
    "Vermilion City": 0x05,
    "Celadon City": 0x06,
    "Fuchsia City": 0x07,
    "Cinnabar Island": 0x08,
    "Indigo Plateau": 0x09,
    "Saffron City": 0x0A,
    # "Unused Map 0B": 0x0B,
    "Route 1": 0x0C,
    "Route 2": 0x0D,
    "Route 3": 0x0E,
    "Route 4": 0x0F,
    "Route 5": 0x10,
    "Route 6": 0x11,
    "Route 7": 0x12,
    "Route 8": 0x13,
    "Route 9": 0x14,
    "Route 10": 0x15,
    "Route 11": 0x16,
    "Route 12": 0x17,
    "Route 13": 0x18,
    "Route 14": 0x19,
    "Route 15": 0x1A,
    "Route 16": 0x1B,
    "Route 17": 0x1C,
    "Route 18": 0x1D,
    "Route 19": 0x1E,
    "Route 20": 0x1F,
    "Route 21": 0x20,
    "Route 22": 0x21,
    "Route 23": 0x22,
    "Route 24": 0x23,
    "Route 25": 0x24,
    "Player's House 1F": 0x25,
    "Player's House 2F": 0x26,
    "Rival's House": 0x27,
    "Oak's Lab": 0x28,
    "Viridian Pokemon Center": 0x29,
    "Viridian Pokemart": 0x2A,
    "Viridian School House": 0x2B,
    "Viridian Nickname House": 0x2C,
    "Viridian Gym": 0x2D,
    "Diglett's Cave Route 2": 0x2E,
    "Viridian Forest North Gate": 0x2F,
    "Route 2 Trade House": 0x30,
    "Route 2 Gate": 0x31,
    "Viridian Forest South Gate": 0x32,
    "Viridian Forest": 0x33,
    "Pewter Museum 1F": 0x34,
    "Pewter Museum 2F": 0x35,
    "Pewter Gym": 0x36,
    "Pewter Nidoran House": 0x37,
    "Pewter Pokemart": 0x38,
    "Pewter Speech House": 0x39,
    "Pewter Pokemon Center": 0x3A,
    "Mt Moon 1F": 0x3B,
    "Mt Moon B1F": 0x3C,
    "Mt Moon B2F": 0x3D,
    "Cerulean Trashed House": 0x3E,
    "Cerulean Trade House": 0x3F,
    "Cerulean Pokemon Center": 0x40,
    "Cerulean Gym": 0x41,
    "Bike Shop": 0x42,
    "Cerulean Pokemart": 0x43,
    "Route 4 Pokemon Center": 0x44,
    # "Cerulean Trashed House Copy": 0x45,
    "Route 5 Gate": 0x46,
    "Underground Path Route 5": 0x47,
    "Daycare": 0x48,
    "Route 6 Gate": 0x49,
    "Underground Path Route 6": 0x4A,
    # "Underground Path Route 6 Copy": 0x4B,
    "Route 7 Gate": 0x4C,
    "Underground Path Route 7": 0x4D,
    # "Underground Path Route 7 Copy": 0x4E,
    "Route 8 Gate": 0x4F,
    "Underground Path Route 8": 0x50,
    "Rock Tunnel Pokemon Center": 0x51,
    "Rock Tunnel 1F": 0x52,
    "Power Plant": 0x53,
    "Route 11 Gate 1F": 0x54,
    "Diglett's Cave Route 11": 0x55,
    "Route 11 Gate 2F": 0x56,
    "Route 12 Gate 1F": 0x57,
    "Bill's House": 0x58,
    "Vermilion Pokemon Center": 0x59,
    "Pokemon Fan Club": 0x5A,
    "Vermilion Pokemart": 0x5B,
    "Vermilion Gym": 0x5C,
    "Vermilion Pidgey House": 0x5D,
    "Vermilion Dock": 0x5E,
    "S.S. Anne 1F": 0x5F,
    "S.S. Anne 2F": 0x60,
    "S.S. Anne 3F": 0x61,
    "S.S. Anne B1F": 0x62,
    "S.S. Anne Bow": 0x63,
    "S.S. Anne Kitchen": 0x64,
    "S.S. Anne Captain's Room": 0x65,
    "S.S. Anne 1F Rooms": 0x66,
    "S.S. Anne 2F Rooms": 0x67,
    "S.S. Anne B1F Rooms": 0x68,
    # "Unused Map 69": 0x69,
    # "Unused Map 6A": 0x6A,
    # "Unused Map 6B": 0x6B,
    "Victory Road 1F": 0x6C,
    # "Unused Map 6D": 0x6D,
    # "Unused Map 6E": 0x6E,
    # "Unused Map 6F": 0x6F,
    # "Unused Map 70": 0x70,
    "Lance's Room": 0x71,
    # "Unused Map 72": 0x72,
    # "Unused Map 73": 0x73,
    # "Unused Map 74": 0x74,
    # "Unused Map 75": 0x75,
    "Hall Of Fame": 0x76,
    "Underground Path North South": 0x77,
    "Indigo Plateau Champion's Room": 0x78,
    "Underground Path West East": 0x79,
    "Celadon Pokemart 1F": 0x7A,
    "Celadon Pokemart 2F": 0x7B,
    "Celadon Pokemart 3F": 0x7C,
    "Celadon Pokemart 4F": 0x7D,
    "Celadon Pokemart Roof": 0x7E,
    "Celadon Pokemart Elevator": 0x7F,
    "Celadon Mansion 1F": 0x80,
    "Celadon Mansion 2F": 0x81,
    "Celadon Mansion 3F": 0x82,
    "Celadon Mansion Roof": 0x83,
    "Celadon Mansion Roof House": 0x84,
    "Celadon Pokemon Center": 0x85,
    "Celadon Gym": 0x86,
    "Celadon Game Corner": 0x87,
    "Celadon Pokemart 5F": 0x88,
    "Celadon Prize Corner": 0x89,
    "Celadon Diner": 0x8A,
    "Celadon Chief House": 0x8B,
    "Celadon Hotel": 0x8C,
    "Lavender Pokemon Center": 0x8D,
    "Pokemon Tower 1F": 0x8E,
    "Pokemon Tower 2F": 0x8F,
    "Pokemon Tower 3F": 0x90,
    "Pokemon Tower 4F": 0x91,
    "Pokemon Tower 5F": 0x92,
    "Pokemon Tower 6F": 0x93,
    "Pokemon Tower 7F": 0x94,
    "Lavender Mr Fuji's House": 0x95,
    "Lavender Pokemart": 0x96,
    "Lavender Cubone House": 0x97,
    "Fuchsia Pokemart": 0x98,
    "Fuchsia Bill's Grandpa's House": 0x99,
    "Fuchsia Pokemon Center": 0x9A,
    "Fuchsia Warden's House": 0x9B,
    "Safari Zone Gate": 0x9C,
    "Fuchsia Gym": 0x9D,
    "Fuchsia Meeting Room": 0x9E,
    "Seafoam Islands B1F": 0x9F,
    "Seafoam Islands B2F": 0xA0,
    "Seafoam Islands B3F": 0xA1,
    "Seafoam Islands B4F": 0xA2,
    "Vermilion Old Rod House": 0xA3,
    "Fuchsia Good Rod House": 0xA4,
    "Pokemon Mansion 1F": 0xA5,
    "Cinnabar Gym": 0xA6,
    "Cinnabar Lab": 0xA7,
    "Cinnabar Lab Trade Room": 0xA8,
    "Cinnabar Lab Metronome Room": 0xA9,
    "Cinnabar Lab Fossil Room": 0xAA,
    "Cinnabar Pokemon Center": 0xAB,
    "Cinnabar Pokemart": 0xAC,
    # "Cinnabar Pokemart Copy": 0xAD,
    "Indigo Plateau Lobby": 0xAE,
    "Saffron Copycat's House 1F": 0xAF,
    "Saffron Copycat's House 2F": 0xB0,
    "Saffron Fighting Dojo": 0xB1,
    "Saffron Gym": 0xB2,
    "Saffron Pidgey House": 0xB3,
    "Saffron Pokemart": 0xB4,
    "Silph Co 1F": 0xB5,
    "Saffron Pokemon Center": 0xB6,
    "Mr. Psychic's House": 0xB7,
    "Route 15 Gate 1F": 0xB8,
    "Route 15 Gate 2F": 0xB9,
    "Route 16 Gate 1F": 0xBA,
    "Route 16 Gate 2F": 0xBB,
    "Route 16 Fly House": 0xBC,
    "Route 12 Super Rod House": 0xBD,
    "Route 18 Gate 1F": 0xBE,
    "Route 18 Gate 2F": 0xBF,
    "Seafoam Islands 1F": 0xC0,
    "Route 22 Gate": 0xC1,
    "Victory Road 2F": 0xC2,
    "Route 12 Gate 2F": 0xC3,
    "Vermilion Trade House": 0xC4,
    "Diglett's Cave": 0xC5,
    "Victory Road 3F": 0xC6,
    "Rocket Hideout B1F": 0xC7,
    "Rocket Hideout B2F": 0xC8,
    "Rocket Hideout B3F": 0xC9,
    "Rocket Hideout B4F": 0xCA,
    "Rocket Hideout Elevator": 0xCB,
    # "Unused Map Cc": 0xCC,
    # "Unused Map Cd": 0xCD,
    # "Unused Map Ce": 0xCE,
    "Silph Co 2F": 0xCF,
    "Silph Co 3F": 0xD0,
    "Silph Co 4F": 0xD1,
    "Silph Co 5F": 0xD2,
    "Silph Co 6F": 0xD3,
    "Silph Co 7F": 0xD4,
    "Silph Co 8F": 0xD5,
    "Pokemon Mansion 2F": 0xD6,
    "Pokemon Mansion 3F": 0xD7,
    "Pokemon Mansion B1F": 0xD8,
    "Safari Zone East": 0xD9,
    "Safari Zone North": 0xDA,
    "Safari Zone West": 0xDB,
    "Safari Zone Center": 0xDC,
    "Safari Zone Center Rest House": 0xDD,
    "Safari Zone Secret House": 0xDE,
    "Safari Zone West Rest House": 0xDF,
    "Safari Zone East Rest House": 0xE0,
    "Safari Zone North Rest House": 0xE1,
    "Cerulean Cave 2F": 0xE2,
    "Cerulean Cave B1F": 0xE3,
    "Cerulean Cave 1F": 0xE4,
    "Lavender Name Rater's House": 0xE5,
    "Cerulean Badge House": 0xE6,
    # "Unused Map E7": 0xE7,
    "Rock Tunnel B1F": 0xE8,
    "Silph Co 9F": 0xE9,
    "Silph Co 10F": 0xEA,
    "Silph Co 11F": 0xEB,
    "Silph Co Elevator": 0xEC,
    # "Unused Map Ed": 0xED,
    # "Unused Map Ee": 0xEE,
    "Trade Center": 0xEF,
    "Colosseum": 0xF0,
    # "Unused Map F1": 0xF1,
    # "Unused Map F2": 0xF2,
    # "Unused Map F3": 0xF3,
    # "Unused Map F4": 0xF4,
    "Indigo Plateau Lorelei's Room": 0xF5,
    "Indigo Plateau Bruno's Room": 0xF6,
    "Indigo Plateau Agatha's Room": 0xF7,

}

# map_ids = {x: y for y,x in map_ids.items()}

warp_data = {'Menu': [], 'Anywhere': [], 'Pokedex': [], 'Fossil': [], 'Celadon City': [
    {'address': 'Warps_CeladonCity', 'id': 0, 'to': {'map': 'Celadon Pokemart 1F', 'id': (0, 1)}},
    {'address': 'Warps_CeladonCity', 'id': 1, 'to': {'map': 'Celadon Pokemart 1F', 'id': (2, 3)}},
    {'address': 'Warps_CeladonCity', 'id': 2, 'to': {'map': 'Celadon Mansion 1F', 'id': (0, 1)}},
    {'address': 'Warps_CeladonCity', 'id': (3, 4), 'to': {'map': 'Celadon Mansion 1F', 'id': 2}},
    {'address': 'Warps_CeladonCity', 'id': 5, 'to': {'map': 'Celadon Pokemon Center', 'id': 0}},
    {'address': 'Warps_CeladonCity', 'id': 7, 'to': {'map': 'Celadon Game Corner', 'id': (0, 1)}},
    {'address': 'Warps_CeladonCity', 'id': 9, 'to': {'map': 'Celadon Prize Corner', 'id': (0, 1)}},
    {'address': 'Warps_CeladonCity', 'id': 10, 'to': {'map': 'Celadon Diner', 'id': (0, 1)}},
    {'address': 'Warps_CeladonCity', 'id': 11, 'to': {'map': 'Celadon Chief House', 'id': (0, 1)}},
    {'address': 'Warps_CeladonCity', 'id': 12, 'to': {'map': 'Celadon Hotel', 'id': (0, 1)}}],
             'Celadon City-G': [{'address': 'Warps_CeladonCity', 'id': 6, 'to': {'map': 'Celadon Gym', 'id': (0, 1)}}],
             'Pallet Town': [{'address': 'Warps_PalletTown', 'id': 0, 'to': {'map': "Player's House 1F", 'id': (0, 1)}},
                             {'address': 'Warps_PalletTown', 'id': 1, 'to': {'map': "Rival's House", 'id': (0, 1)}},
                             {'address': 'Warps_PalletTown', 'id': 2, 'to': {'map': "Oak's Lab", 'id': (1, 0)}}],
             'Viridian City': [
                 {'address': 'Warps_ViridianCity', 'id': 0, 'to': {'map': 'Viridian Pokemon Center', 'id': (0, 1)}},
                 {'address': 'Warps_ViridianCity', 'id': 1, 'to': {'map': 'Viridian Pokemart', 'id': (0, 1)}},
                 {'address': 'Warps_ViridianCity', 'id': 2, 'to': {'map': 'Viridian School House', 'id': (0, 1)}},
                 {'address': 'Warps_ViridianCity', 'id': 3, 'to': {'map': 'Viridian Nickname House', 'id': (0, 1)}}],
             'Viridian City-N': [], 'Viridian City-G': [
        {'address': 'Warps_ViridianCity', 'id': 4, 'to': {'map': 'Viridian Gym', 'id': (0, 1)}}],
             'Pewter City': [{'address': 'Warps_PewterCity', 'id': 0, 'to': {'map': 'Pewter Museum 1F', 'id': (0, 1)}},
                             {'address': 'Warps_PewterCity', 'id': 1, 'to': {'map': 'Pewter Museum 1F', 'id': (2, 3)}},
                             {'address': 'Warps_PewterCity', 'id': 2, 'to': {'map': 'Pewter Gym', 'id': (0, 1)}},
                             {'address': 'Warps_PewterCity', 'id': 3,
                              'to': {'map': 'Pewter Nidoran House', 'id': (0, 1)}},
                             {'address': 'Warps_PewterCity', 'id': 4, 'to': {'map': 'Pewter Pokemart', 'id': (0, 1)}},
                             {'address': 'Warps_PewterCity', 'id': 5,
                              'to': {'map': 'Pewter Speech House', 'id': (0, 1)}},
                             {'address': 'Warps_PewterCity', 'id': 6,
                              'to': {'map': 'Pewter Pokemon Center', 'id': (0, 1)}}], 'Cerulean City': [
        {'address': 'Warps_CeruleanCity', 'id': 0, 'to': {'map': 'Cerulean Trashed House', 'id': (0, 1)}},
        {'address': 'Warps_CeruleanCity', 'id': 1, 'to': {'map': 'Cerulean Trade House', 'id': (0, 1)}},
        {'address': 'Warps_CeruleanCity', 'id': 2, 'to': {'map': 'Cerulean Pokemon Center', 'id': (0, 1)}},
        {'address': 'Warps_CeruleanCity', 'id': 3, 'to': {'map': 'Cerulean Gym', 'id': (0, 1)}},
        {'address': 'Warps_CeruleanCity', 'id': 4, 'to': {'map': 'Bike Shop', 'id': (0, 1)}},
        {'address': 'Warps_CeruleanCity', 'id': 5, 'to': {'map': 'Cerulean Pokemart', 'id': (0, 1)}},
        {'address': 'Warps_CeruleanCity', 'id': 8, 'to': {'map': 'Cerulean Badge House', 'id': (1, 2)}}],
             'Cerulean City-Badge House Backyard': [
        {'address': 'Warps_CeruleanCity', 'id': 9, 'to': {'map': 'Cerulean Badge House', 'id': 0}}],
             'Cerulean City-Water': [], 'Cerulean City-Cave': [
        {'address': 'Warps_CeruleanCity', 'id': 6, 'to': {'map': 'Cerulean Cave 1F', 'id': (0, 1)}}],
             'Cerulean City-Outskirts': [
                 {'address': 'Warps_CeruleanCity', 'id': 7, 'to': {'map': 'Cerulean Trashed House', 'id': 2}}],
             'Vermilion City': [
                 {'address': 'Warps_VermilionCity', 'id': 0, 'to': {'map': 'Vermilion Pokemon Center', 'id': (0, 1)}},
                 {'address': 'Warps_VermilionCity', 'id': 1, 'to': {'map': 'Pokemon Fan Club', 'id': (0, 1)}},
                 {'address': 'Warps_VermilionCity', 'id': 2, 'to': {'map': 'Vermilion Pokemart', 'id': (0, 1)}},
                 {'address': 'Warps_VermilionCity', 'id': 4, 'to': {'map': 'Vermilion Pidgey House', 'id': 0}},
                 {'address': 'Warps_VermilionCity', 'id': 7, 'to': {'map': 'Vermilion Trade House', 'id': 0}},
                 {'address': 'Warps_VermilionCity', 'id': 8, 'to': {'map': 'Vermilion Old Rod House', 'id': 0}}],
             'Vermilion City-G': [
                 {'address': 'Warps_VermilionCity', 'id': 3, 'to': {'map': 'Vermilion Gym', 'id': (0, 1)}}],
             'Vermilion City-Dock': [
                 {'address': 'Warps_VermilionCity', 'id': (5, 6), 'to': {'map': 'Vermilion Dock', 'id': 0}}],
             'Fuchsia City': [
                 {'address': 'Warps_FuchsiaCity', 'id': 0, 'to': {'map': 'Fuchsia Pokemart', 'id': (0, 1)}},
                 {'address': 'Warps_FuchsiaCity', 'id': 1, 'to': {'map': "Fuchsia Bill's Grandpa's House", 'id': 0}},
                 {'address': 'Warps_FuchsiaCity', 'id': 2, 'to': {'map': 'Fuchsia Pokemon Center', 'id': 0}},
                 {'address': 'Warps_FuchsiaCity', 'id': 3, 'to': {'map': "Fuchsia Warden's House", 'id': 0}},
                 {'address': 'Warps_FuchsiaCity', 'id': 4, 'to': {'map': 'Safari Zone Gate-S', 'id': (0, 1)}},
                 {'address': 'Warps_FuchsiaCity', 'id': 5, 'to': {'map': 'Fuchsia Gym', 'id': 0}},
                 {'address': 'Warps_FuchsiaCity', 'id': 6, 'to': {'map': 'Fuchsia Meeting Room', 'id': 0}},
                 {'address': 'Warps_FuchsiaCity', 'id': 7, 'to': {'map': 'Fuchsia Good Rod House', 'id': 1}}],
             'Fuchsia City-Good Rod House Backyard': [
                 {'address': 'Warps_FuchsiaCity', 'id': 8, 'to': {'map': 'Fuchsia Good Rod House', 'id': 0}}],
             "Rival's House": [{'address': 'Warps_BluesHouse', 'id': (0, 1), 'to': {'map': 'Pallet Town', 'id': 1}}],
             'Vermilion Trade House': [
                 {'address': 'Warps_VermilionTradeHouse', 'id': (0, 1), 'to': {'map': 'Vermilion City', 'id': 7}}],
             'Indigo Plateau Lobby': [
                 {'address': 'Warps_IndigoPlateauLobby', 'id': (0, 1), 'to': {'map': 'Indigo Plateau', 'id': (0, 1)}},
                 {'address': 'Warps_IndigoPlateauLobby', 'id': 2,
                  'to': {'map': "Indigo Plateau Lorelei's Room", 'id': 0}}],
             'Silph Co 4F': [{'address': 'Warps_SilphCo4F', 'id': 0, 'to': {'map': 'Silph Co 3F', 'id': 1}},
                             {'address': 'Warps_SilphCo4F', 'id': 1, 'to': {'map': 'Silph Co 5F', 'id': 1}},
                             {'address': 'Warps_SilphCo4F', 'id': 2, 'to': {'map': 'Silph Co Elevator', 'id': 3}},
                             {'address': 'Warps_SilphCo4F', 'id': 5, 'to': {'map': 'Silph Co 10F-SE', 'id': 4}},
                             {'address': 'Warps_SilphCo4F', 'id': 6, 'to': {'map': 'Silph Co 10F', 'id': 5}}],
             'Silph Co 4F-N': [{'address': 'Warps_SilphCo4F', 'id': 4, 'to': {'map': 'Silph Co 6F', 'id': 3}},
                               {'address': 'Warps_SilphCo4F', 'id': 3, 'to': {'map': 'Silph Co 10F-SE', 'id': 3}}],
             'Silph Co 4F-W': [], 'Silph Co 5F-NW': [], 'Silph Co 6F-SW': [],
             'Silph Co 5F': [{'address': 'Warps_SilphCo5F', 'id': 0, 'to': {'map': 'Silph Co 6F', 'id': 1}},
                             {'address': 'Warps_SilphCo5F', 'id': 1, 'to': {'map': 'Silph Co 4F', 'id': 1}},
                             {'address': 'Warps_SilphCo5F', 'id': 2, 'to': {'map': 'Silph Co Elevator', 'id': 4}},
                             {'address': 'Warps_SilphCo5F', 'id': 3, 'to': {'map': 'Silph Co 7F-SE', 'id': 5}},
                             {'address': 'Warps_SilphCo5F', 'id': 4, 'to': {'map': 'Silph Co 9F', 'id': 4}},
                             {'address': 'Warps_SilphCo5F', 'id': 5, 'to': {'map': 'Silph Co 3F', 'id': 4}}],
             'Silph Co 5F-SW': [{'address': 'Warps_SilphCo5F', 'id': 6, 'to': {'map': 'Silph Co 3F', 'id': 5}}],
             'Silph Co 6F': [{'address': 'Warps_SilphCo6F', 'id': 0, 'to': {'map': 'Silph Co 7F', 'id': 1}},
                             {'address': 'Warps_SilphCo6F', 'id': 1, 'to': {'map': 'Silph Co 5F', 'id': 0}},
                             {'address': 'Warps_SilphCo6F', 'id': 2, 'to': {'map': 'Silph Co Elevator', 'id': 6}},
                             {'address': 'Warps_SilphCo6F', 'id': 3, 'to': {'map': 'Silph Co 4F-N', 'id': 4}},
                             {'address': 'Warps_SilphCo6F', 'id': 4, 'to': {'map': 'Silph Co 2F-SW', 'id': 6}}],
             'Cinnabar Island-M': [
                 {'address': 'Warps_CinnabarIsland', 'id': 0, 'to': {'map': 'Pokemon Mansion 1F', 'id': 1}}],
             'Cinnabar Island-G': [
                 {'address': 'Warps_CinnabarIsland', 'id': 1, 'to': {'map': 'Cinnabar Gym', 'id': 0}}],
             'Cinnabar Island': [{'address': 'Warps_CinnabarIsland', 'id': 2, 'to': {'map': 'Cinnabar Lab', 'id': 0}},
                                 {'address': 'Warps_CinnabarIsland', 'id': 3,
                                  'to': {'map': 'Cinnabar Pokemon Center', 'id': 0}},
                                 {'address': 'Warps_CinnabarIsland', 'id': 4,
                                  'to': {'map': 'Cinnabar Pokemart', 'id': (0, 1)}}], 'Route 1': [],
             "Oak's Lab": [{'address': 'Warps_OaksLab', 'id': (1, 0), 'to': {'map': 'Pallet Town', 'id': 2}}],
             'Viridian Pokemart': [
                 {'address': 'Warps_ViridianMart', 'id': (0, 1), 'to': {'map': 'Viridian City', 'id': 1}}],
             'Viridian School House': [
                 {'address': 'Warps_ViridianSchoolHouse', 'id': (0, 1), 'to': {'map': 'Viridian City', 'id': 2}}],
             'Viridian Nickname House': [
                 {'address': 'Warps_ViridianNicknameHouse', 'id': (0, 1), 'to': {'map': 'Viridian City', 'id': 3}}],
             'Pewter Nidoran House': [
                 {'address': 'Warps_PewterNidoranHouse', 'id': (0, 1), 'to': {'map': 'Pewter City', 'id': 3}}],
             'Pewter Speech House': [
                 {'address': 'Warps_PewterSpeechHouse', 'id': (0, 1), 'to': {'map': 'Pewter City', 'id': 5}}],
             'Cerulean Trashed House': [
                 {'address': 'Warps_CeruleanTrashedHouse', 'id': (0, 1), 'to': {'map': 'Cerulean City', 'id': 0}},
                 {'address': 'Warps_CeruleanTrashedHouse', 'id': 2, 'to': {'map': 'Cerulean City-Outskirts', 'id': 7}}],
             'Cerulean Trade House': [
                 {'address': 'Warps_CeruleanTradeHouse', 'id': (0, 1), 'to': {'map': 'Cerulean City', 'id': 1}}],
             'Bike Shop': [{'address': 'Warps_BikeShop', 'id': (0, 1), 'to': {'map': 'Cerulean City', 'id': 4}}],
             "Lavender Mr Fuji's House": [
                 {'address': 'Warps_MrFujisHouse', 'id': (0, 1), 'to': {'map': 'Lavender Town', 'id': 2}}],
             'Lavender Cubone House': [
                 {'address': 'Warps_LavenderCuboneHouse', 'id': (0, 1), 'to': {'map': 'Lavender Town', 'id': 4}}],
             "Lavender Name Rater's House": [
                 {'address': 'Warps_NameRatersHouse', 'id': (0, 1), 'to': {'map': 'Lavender Town', 'id': 5}}],
             'Vermilion Pidgey House': [
                 {'address': 'Warps_VermilionPidgeyHouse', 'id': (0, 1), 'to': {'map': 'Vermilion City', 'id': 4}}],
             'Vermilion Dock': [{'address': 'Warps_VermilionDock', 'id': 0, 'to': {'map': 'Vermilion City', 'id': 5}},
                                {'address': 'Warps_VermilionDock', 'id': 1, 'to': {'map': 'S.S. Anne 1F', 'id': 1}}],
             'Celadon Mansion Roof House': [{'address': 'Warps_CeladonMansionRoofHouse', 'id': (0, 1),
                                             'to': {'map': 'Celadon Mansion Roof', 'id': 2}}], 'Fuchsia Pokemart': [
        {'address': 'Warps_FuchsiaMart', 'id': (0, 1), 'to': {'map': 'Fuchsia City', 'id': 0}}],
             'Saffron Pidgey House': [
                 {'address': 'Warps_SaffronPidgeyHouse', 'id': (0, 1), 'to': {'map': 'Saffron City', 'id': 3}}],
             "Mr. Psychic's House": [
                 {'address': 'Warps_MrPsychicsHouse', 'id': (0, 1), 'to': {'map': 'Saffron City', 'id': 7}}],
             "Diglett's Cave Route 2": [
                 {'address': 'Warps_DiglettsCaveRoute2', 'id': (0, 1), 'to': {'map': 'Route 2-NE', 'id': 0}},
                 {'address': 'Warps_DiglettsCaveRoute2', 'id': 2, 'to': {'map': "Diglett's Cave", 'id': 0}}],
             'Route 2 Trade House': [
                 {'address': 'Warps_Route2TradeHouse', 'id': (0, 1), 'to': {'map': 'Route 2-NE', 'id': 2}}],
             'Route 5 Gate-S': [{'address': 'Warps_Route5Gate', 'id': (0, 1), 'to': {'map': 'Route 5-S', 'id': 2}}],
             'Route 5 Gate-N': [{'address': 'Warps_Route5Gate', 'id': (3, 2), 'to': {'map': 'Route 5', 'id': (1, 0)}}],
             'Route 6 Gate-S': [{'address': 'Warps_Route6Gate', 'id': (0, 1), 'to': {'map': 'Route 6', 'id': 2}}],
             'Route 6 Gate-N': [{'address': 'Warps_Route6Gate', 'id': (2, 3), 'to': {'map': 'Route 6-N', 'id': 1}}],
             'Route 7 Gate-W': [{'address': 'Warps_Route7Gate', 'id': (0, 1), 'to': {'map': 'Route 7', 'id': 3}}],
             'Route 7 Gate-E': [{'address': 'Warps_Route7Gate', 'id': (2, 3), 'to': {'map': 'Route 7-E', 'id': (0, 1)}}],
             'Route 8 Gate-W': [{'address': 'Warps_Route8Gate', 'id': (0, 1), 'to': {'map': 'Route 8-W', 'id': (0, 1)}}],
             'Route 8 Gate-E': [{'address': 'Warps_Route8Gate', 'id': (2, 3), 'to': {'map': 'Route 8', 'id': (2, 3)}}],
             'Underground Path Route 8': [
                 {'address': 'Warps_UndergroundPathRoute8', 'id': (0, 1), 'to': {'map': 'Route 8', 'id': 4}},
                 {'address': 'Warps_UndergroundPathRoute8', 'id': 2,
                  'to': {'map': 'Underground Path West East', 'id': 1}}],
             'Power Plant': [{'address': 'Warps_PowerPlant', 'id': (0, 1), 'to': {'map': 'Route 10-P', 'id': 3}},
                             {'address': 'Warps_PowerPlant', 'id': 2, 'to': {'map': 'Route 10-P', 'id': 3}}],
             "Diglett's Cave Route 11": [
                 {'address': 'Warps_DiglettsCaveRoute11', 'id': (0, 1), 'to': {'map': 'Route 11', 'id': 4}},
                 {'address': 'Warps_DiglettsCaveRoute11', 'id': 2, 'to': {'map': "Diglett's Cave", 'id': 1}}],
             'Route 16 Fly House': [
                 {'address': 'Warps_Route16FlyHouse', 'id': (0, 1), 'to': {'map': 'Route 16-NW', 'id': 8}}],
             'Route 22 Gate-S': [{'address': 'Warps_Route22Gate', 'id': (0, 1), 'to': {'map': 'Route 22', 'id': 0}}],
             'Route 22 Gate-N': [
                 {'address': 'Warps_Route22Gate', 'id': (2, 3), 'to': {'map': 'Route 23-S', 'id': (0, 1)}}],
             "Bill's House": [{'address': 'Warps_BillsHouse', 'id': (0, 1), 'to': {'map': 'Route 25', 'id': 0}}],
             'Lavender Town': [
                 {'address': 'Warps_LavenderTown', 'id': 0, 'to': {'map': 'Lavender Pokemon Center', 'id': 0}},
                 {'address': 'Warps_LavenderTown', 'id': 1, 'to': {'map': 'Pokemon Tower 1F', 'id': 0}},
                 {'address': 'Warps_LavenderTown', 'id': 2, 'to': {'map': "Lavender Mr Fuji's House", 'id': 0}},
                 {'address': 'Warps_LavenderTown', 'id': 3, 'to': {'map': 'Lavender Pokemart', 'id': 0}},
                 {'address': 'Warps_LavenderTown', 'id': 4, 'to': {'map': 'Lavender Cubone House', 'id': 0}},
                 {'address': 'Warps_LavenderTown', 'id': 5, 'to': {'map': "Lavender Name Rater's House", 'id': 0}}],
             'Viridian Pokemon Center': [
                 {'address': 'Warps_ViridianPokecenter', 'id': (0, 1), 'to': {'map': 'Viridian City', 'id': 0}}],
             'Pokemon Mansion 1F': [
                 {'address': 'Warps_PokemonMansion1F', 'id': 4, 'to': {'map': 'Pokemon Mansion 2F', 'id': 0}},
                 {'address': 'Warps_PokemonMansion1F', 'id': (0, 1, 2, 3),
                  'to': {'map': 'Cinnabar Island-M', 'id': 0}}], 'Pokemon Mansion 1F-SE': [
        {'address': 'Warps_PokemonMansion1F', 'id': 5, 'to': {'map': 'Pokemon Mansion B1F', 'id': 0}},
        {'address': 'Warps_PokemonMansion1F', 'id': (6, 7), 'to': {'map': 'Cinnabar Island-M', 'id': 0}}],
             'Pokemon Mansion 2F': [
                 {'address': 'Warps_PokemonMansion2F', 'id': 0, 'to': {'map': 'Pokemon Mansion 1F', 'id': 4}},
                 {'address': 'Warps_PokemonMansion2F', 'id': 1, 'to': {'map': 'Pokemon Mansion 3F-SW', 'id': 0}}],
             'Pokemon Mansion 2F-NW': [
                 {'address': 'Warps_PokemonMansion2F', 'id': 3, 'to': {'map': 'Pokemon Mansion 3F', 'id': 1}}],
             'Pokemon Mansion 2F-E': [
                 {'address': 'Warps_PokemonMansion2F', 'id': 2, 'to': {'map': 'Pokemon Mansion 3F-SE', 'id': 2}}], 'Pokemon Mansion 3F': [
        {'address': 'Warps_PokemonMansion3F', 'id': 1, 'to': {'map': 'Pokemon Mansion 2F-NW', 'id': 3}}],
             'Pokemon Mansion 3F-SE': [
                 {'address': 'Warps_PokemonMansion3F', 'id': 2, 'to': {'map': 'Pokemon Mansion 2F-E', 'id': 2}}],
             'Pokemon Mansion 3F-SW': [
                 {'address': 'Warps_PokemonMansion3F', 'id': 0, 'to': {'map': 'Pokemon Mansion 2F', 'id': 1}}],
             'Pokemon Mansion B1F': [
                 {'address': 'Warps_PokemonMansionB1F', 'id': 0, 'to': {'map': 'Pokemon Mansion 1F-SE', 'id': 5}}],
             'Rock Tunnel 1F': [{'address': 'Warps_RockTunnel1F', 'id': (0, 1), 'to': {'map': 'Route 10-N', 'id': 1}},
                                {'address': 'Warps_RockTunnel1F', 'id': (2, 3), 'to': {'map': 'Route 10-S', 'id': 2}},
                                {'address': 'Warps_RockTunnel1F', 'id': 4, 'to': {'map': 'Rock Tunnel B1F', 'id': 0}},
                                {'address': 'Warps_RockTunnel1F', 'id': 5, 'to': {'map': 'Rock Tunnel B1F', 'id': 1}},
                                {'address': 'Warps_RockTunnel1F', 'id': 6, 'to': {'map': 'Rock Tunnel B1F', 'id': 2}},
                                {'address': 'Warps_RockTunnel1F', 'id': 7, 'to': {'map': 'Rock Tunnel B1F', 'id': 3}}],
             'Seafoam Islands 1F': [
                 {'address': 'Warps_SeafoamIslands1F', 'id': (2, 3), 'to': {'map': 'Route 20-IE', 'id': 1}},
                 {'address': 'Warps_SeafoamIslands1F', 'id': 4, 'to': {'map': 'Seafoam Islands B1F', 'id': 1}},
                 {'address': 'Warps_SeafoamIslands1F', 'id': 5, 'to': {'map': 'Seafoam Islands B1F-NE', 'id': 6}}],
             'Seafoam Islands 1F-SE': [
                 {'address': 'Warps_SeafoamIslands1F', 'id': (0, 1), 'to': {'map': 'Route 20-IW', 'id': 0}},
                 {'address': 'Warps_SeafoamIslands1F', 'id': 6, 'to': {'map': 'Seafoam Islands B1F-SE', 'id': 4}}],
             'S.S. Anne 3F': [{'address': 'Warps_SSAnne3F', 'id': 0, 'to': {'map': 'S.S. Anne Bow', 'id': 0}},
                              {'address': 'Warps_SSAnne3F', 'id': 1, 'to': {'map': 'S.S. Anne 2F', 'id': 7}}],
             'Victory Road 3F': [{'address': 'Warps_VictoryRoad3F', 'id': 0, 'to': {'map': 'Victory Road 2F', 'id': 3}},
                                 {'address': 'Warps_VictoryRoad3F', 'id': 3,
                                  'to': {'map': 'Victory Road 2F', 'id': 6}}], 'Victory Road 3F-SE': [
        {'address': 'Warps_VictoryRoad3F', 'id': 1, 'to': {'map': 'Victory Road 2F', 'id': 5}},
        {'address': 'Warps_VictoryRoad3F', 'id': 2, 'to': {'map': 'Victory Road 2F', 'id': 4}}],
             'Victory Road 3F-S': [], 'Rocket Hideout B1F': [
        {'address': 'Warps_RocketHideoutB1F', 'id': 0, 'to': {'map': 'Rocket Hideout B2F', 'id': 0}},
        {'address': 'Warps_RocketHideoutB1F', 'id': 1, 'to': {'map': 'Celadon Game Corner', 'id': 2}}],
             'Rocket Hideout B1F-SE': [{'address': 'Warps_RocketHideoutB1F', 'id': (2, 4),
                                        'to': {'map': 'Rocket Hideout Elevator', 'id': 0}}], 'Rocket Hideout B1F-S': [
        {'address': 'Warps_RocketHideoutB1F', 'id': 3, 'to': {'map': 'Rocket Hideout B2F', 'id': 3}}],
             'Rocket Hideout B2F': [
                 {'address': 'Warps_RocketHideoutB2F', 'id': 0, 'to': {'map': 'Rocket Hideout B1F', 'id': 0}},
                 {'address': 'Warps_RocketHideoutB2F', 'id': 1, 'to': {'map': 'Rocket Hideout B3F', 'id': 0}},
                 {'address': 'Warps_RocketHideoutB2F', 'id': (2, 4), 'to': {'map': 'Rocket Hideout Elevator', 'id': 1}},
                 {'address': 'Warps_RocketHideoutB2F', 'id': 3, 'to': {'map': 'Rocket Hideout B1F-S', 'id': 3}}],
             'Rocket Hideout B3F': [
                 {'address': 'Warps_RocketHideoutB3F', 'id': 0, 'to': {'map': 'Rocket Hideout B2F', 'id': 1}},
                 {'address': 'Warps_RocketHideoutB3F', 'id': 1, 'to': {'map': 'Rocket Hideout B4F-NW', 'id': 0}}],
             'Rocket Hideout B4F': [{'address': 'Warps_RocketHideoutB4F', 'id': (1, 2),
                                     'to': {'map': 'Rocket Hideout Elevator', 'id': 2}}], 'Rocket Hideout B4F-NW': [
        {'address': 'Warps_RocketHideoutB4F', 'id': 0, 'to': {'map': 'Rocket Hideout B3F', 'id': 1}}],
             'Rocket Hideout Elevator': [
                 {'address': 'RocketHideoutElevatorWarpMaps', 'id': 0, 'to': {'map': 'Rocket Hideout B1F', 'id': 4}},
                 {'address': 'RocketHideoutElevatorWarpMaps', 'id': 1, 'to': {'map': 'Rocket Hideout B2F', 'id': 4}},
                 {'address': 'RocketHideoutElevatorWarpMaps', 'id': 2, 'to': {'map': 'Rocket Hideout B4F', 'id': 2}}],
             'Silph Co Elevator': [
                 {'address': 'SilphCoElevatorWarpMaps', 'id': 0, 'to': {'map': 'Silph Co 1F', 'id': 3}},
                 {'address': 'SilphCoElevatorWarpMaps', 'id': 1, 'to': {'map': 'Silph Co 2F', 'id': 2}},
                 {'address': 'SilphCoElevatorWarpMaps', 'id': 2, 'to': {'map': 'Silph Co 3F', 'id': 2}},
                 {'address': 'SilphCoElevatorWarpMaps', 'id': 3, 'to': {'map': 'Silph Co 4F', 'id': 2}},
                 {'address': 'SilphCoElevatorWarpMaps', 'id': 4, 'to': {'map': 'Silph Co 5F', 'id': 2}},
                 {'address': 'SilphCoElevatorWarpMaps', 'id': 5, 'to': {'map': 'Silph Co 6F', 'id': 2}},
                 {'address': 'SilphCoElevatorWarpMaps', 'id': 6, 'to': {'map': 'Silph Co 7F', 'id': 2}},
                 {'address': 'SilphCoElevatorWarpMaps', 'id': 7, 'to': {'map': 'Silph Co 8F', 'id': 2}},
                 {'address': 'SilphCoElevatorWarpMaps', 'id': 8, 'to': {'map': 'Silph Co 9F', 'id': 2}},
                 {'address': 'SilphCoElevatorWarpMaps', 'id': 9, 'to': {'map': 'Silph Co 10F', 'id': 2}},
                 {'address': 'SilphCoElevatorWarpMaps', 'id': 10, 'to': {'map': 'Silph Co 11F', 'id': 1}}],
             'Safari Zone East': [
                 {'address': 'Warps_SafariZoneEast', 'id': (0, 1), 'to': {'map': 'Safari Zone North', 'id': (6, 7)}},
                 {'address': 'Warps_SafariZoneEast', 'id': (2, 3), 'to': {'map': 'Safari Zone Center', 'id': (6, 7)}},
                 {'address': 'Warps_SafariZoneEast', 'id': 4, 'to': {'map': 'Safari Zone East Rest House', 'id': 0}}],
             'Safari Zone North': [
                 {'address': 'Warps_SafariZoneNorth', 'id': (0, 1), 'to': {'map': 'Safari Zone West', 'id': (0, 1)}},
                 {'address': 'Warps_SafariZoneNorth', 'id': (2, 3), 'to': {'map': 'Safari Zone West', 'id': (2, 3)}},
                 {'address': 'Warps_SafariZoneNorth', 'id': (4, 5), 'to': {'map': 'Safari Zone Center', 'id': (4, 5)}},
                 {'address': 'Warps_SafariZoneNorth', 'id': (6, 7), 'to': {'map': 'Safari Zone East', 'id': (0, 1)}},
                 {'address': 'Warps_SafariZoneNorth', 'id': 8, 'to': {'map': 'Safari Zone North Rest House', 'id': 0}}],
             'Safari Zone Center': [
                 {'address': 'Warps_SafariZoneCenter', 'id': (0, 1), 'to': {'map': 'Safari Zone Gate-N', 'id': (2, 3)}},
                 {'address': 'Warps_SafariZoneCenter', 'id': (2, 3), 'to': {'map': 'Safari Zone West', 'id': (4, 5)}},
                 {'address': 'Warps_SafariZoneCenter', 'id': (4, 5), 'to': {'map': 'Safari Zone North', 'id': (4, 5)}},
                 {'address': 'Warps_SafariZoneCenter', 'id': (6, 7), 'to': {'map': 'Safari Zone East', 'id': (2, 3)}},
                 {'address': 'Warps_SafariZoneCenter', 'id': 8,
                  'to': {'map': 'Safari Zone Center Rest House', 'id': 0}}], 'Safari Zone Center Rest House': [
        {'address': 'Warps_SafariZoneCenterRestHouse', 'id': (0, 1), 'to': {'map': 'Safari Zone Center', 'id': 8}}],
             'Safari Zone West Rest House': [{'address': 'Warps_SafariZoneWestRestHouse', 'id': (0, 1),
                                              'to': {'map': 'Safari Zone West', 'id': 7}}],
             'Safari Zone East Rest House': [{'address': 'Warps_SafariZoneEastRestHouse', 'id': (0, 1),
                                              'to': {'map': 'Safari Zone East', 'id': 4}}],
             'Safari Zone North Rest House': [{'address': 'Warps_SafariZoneNorthRestHouse', 'id': (0, 1),
                                               'to': {'map': 'Safari Zone North', 'id': 8}}], 'Cerulean Cave 2F-E': [
        {'address': 'Warps_CeruleanCave2F', 'id': 0, 'to': {'map': 'Cerulean Cave 1F', 'id': 2}},
        {'address': 'Warps_CeruleanCave2F', 'id': 1, 'to': {'map': 'Cerulean Cave 1F', 'id': 3}}],
             'Cerulean Cave 2F-Wild': [],
             'Cerulean Cave 2F-W': [
                 {'address': 'Warps_CeruleanCave2F', 'id': 4, 'to': {'map': 'Cerulean Cave 1F', 'id': 6}},
                 {'address': 'Warps_CeruleanCave2F', 'id': 5, 'to': {'map': 'Cerulean Cave 1F', 'id': 7}}],
             'Cerulean Cave 2F-N': [
                 {'address': 'Warps_CeruleanCave2F', 'id': 2, 'to': {'map': 'Cerulean Cave 1F', 'id': 4}},
                 {'address': 'Warps_CeruleanCave2F', 'id': 3, 'to': {'map': 'Cerulean Cave 1F', 'id': 5}}],
             'Cerulean Cave B1F': [
                 {'address': 'Warps_CeruleanCaveB1F', 'id': 0, 'to': {'map': 'Cerulean Cave 1F', 'id': 8}}],
             'Rock Tunnel B1F': [{'address': 'Warps_RockTunnelB1F', 'id': 0, 'to': {'map': 'Rock Tunnel 1F', 'id': 4}},
                                 {'address': 'Warps_RockTunnelB1F', 'id': 1, 'to': {'map': 'Rock Tunnel 1F', 'id': 5}},
                                 {'address': 'Warps_RockTunnelB1F', 'id': 2, 'to': {'map': 'Rock Tunnel 1F', 'id': 6}},
                                 {'address': 'Warps_RockTunnelB1F', 'id': 3, 'to': {'map': 'Rock Tunnel 1F', 'id': 7}}],
             'Seafoam Islands B1F': [
                 {'address': 'Warps_SeafoamIslandsB1F', 'id': 0, 'to': {'map': 'Seafoam Islands B2F-NW', 'id': 0}},
                 {'address': 'Warps_SeafoamIslandsB1F', 'id': 1, 'to': {'map': 'Seafoam Islands 1F', 'id': 4}},
                 {'address': 'Warps_SeafoamIslandsB1F', 'id': 2, 'to': {'map': 'Seafoam Islands B2F-SW', 'id': 2}},
                 {'address': 'Warps_SeafoamIslandsB1F', 'id': 3, 'to': {'map': 'Seafoam Islands B2F-SW', 'id': 3}}],
             'Seafoam Islands B1F-SE': [
                 {'address': 'Warps_SeafoamIslandsB1F', 'id': 4, 'to': {'map': 'Seafoam Islands 1F-SE', 'id': 6}},
                 {'address': 'Warps_SeafoamIslandsB1F', 'id': 5, 'to': {'map': 'Seafoam Islands B2F-SE', 'id': 5}}],
             'Seafoam Islands B1F-NE': [
                 {'address': 'Warps_SeafoamIslandsB1F', 'id': 6, 'to': {'map': 'Seafoam Islands 1F', 'id': 5}}],
             'Seafoam Islands B2F-Wild': [],
             'Seafoam Islands B2F-SE': [
                 {'address': 'Warps_SeafoamIslandsB2F', 'id': 5, 'to': {'map': 'Seafoam Islands B1F-SE', 'id': 5}},
                 {'address': 'Warps_SeafoamIslandsB2F', 'id': 6, 'to': {'map': 'Seafoam Islands B3F-SE', 'id': 4}}],
             'Seafoam Islands B2F-NE': [
                 {'address': 'Warps_SeafoamIslandsB2F', 'id': 4, 'to': {'map': 'Seafoam Islands B3F-NE', 'id': 3}}],
             'Seafoam Islands B2F-SW': [
                 {'address': 'Warps_SeafoamIslandsB2F', 'id': 3, 'to': {'map': 'Seafoam Islands B1F', 'id': 3}},
                 {'address': 'Warps_SeafoamIslandsB2F', 'id': 1, 'to': {'map': 'Seafoam Islands B3F', 'id': 0}},
                 {'address': 'Warps_SeafoamIslandsB2F', 'id': 2, 'to': {'map': 'Seafoam Islands B1F', 'id': 2}}],
             'Seafoam Islands B2F-NW': [
                 {'address': 'Warps_SeafoamIslandsB2F', 'id': 0, 'to': {'map': 'Seafoam Islands B1F', 'id': 0}}],
             'Seafoam Islands B3F': [
                 {'address': 'Warps_SeafoamIslandsB3F', 'id': 0, 'to': {'map': 'Seafoam Islands B2F-SW', 'id': 1}},
                 {'address': 'Warps_SeafoamIslandsB3F', 'id': 1, 'to': {'map': 'Seafoam Islands B4F', 'id': 2}},
                 {'address': 'Warps_SeafoamIslandsB3F', 'id': 5, 'to': {'map': 'Seafoam Islands B4F', 'id': 0}},
                 {'address': 'Warps_SeafoamIslandsB3F', 'id': 6, 'to': {'map': 'Seafoam Islands B4F', 'id': 1}}],
             'Seafoam Islands B3F-SE': [
                 {'address': 'Warps_SeafoamIslandsB3F', 'id': 4, 'to': {'map': 'Seafoam Islands B2F-SE', 'id': 6}}],
             'Seafoam Islands B3F-NE': [
                 {'address': 'Warps_SeafoamIslandsB3F', 'id': 2, 'to': {'map': 'Seafoam Islands B4F', 'id': 3}},
                 {'address': 'Warps_SeafoamIslandsB3F', 'id': 3, 'to': {'map': 'Seafoam Islands B2F-NE', 'id': 4}}],
             'Seafoam Islands B4F': [
                 {'address': 'Warps_SeafoamIslandsB4F', 'id': 0, 'to': {'map': 'Seafoam Islands B3F', 'id': 5}},
                 {'address': 'Warps_SeafoamIslandsB4F', 'id': 1, 'to': {'map': 'Seafoam Islands B3F', 'id': 6}},
                 {'address': 'Warps_SeafoamIslandsB4F', 'id': 2, 'to': {'map': 'Seafoam Islands B3F', 'id': 1}},
                 {'address': 'Warps_SeafoamIslandsB4F', 'id': 3, 'to': {'map': 'Seafoam Islands B3F-NE', 'id': 2}}],
             'Route 7': [{'address': 'Warps_Route7', 'id': 3, 'to': {'map': 'Route 7 Gate', 'id': (0, 1)}},
                         {'address': 'Warps_Route7', 'id': 4, 'to': {'map': 'Underground Path Route 7', 'id': 0}}],
             'Route 7-E': [{'address': 'Warps_Route7', 'id': (0, 1), 'to': {'map': 'Route 7 Gate', 'id': (2, 3)}}],
             "Player's House 1F": [
                 {'address': 'Warps_RedsHouse1F', 'id': (0, 1), 'to': {'map': 'Pallet Town', 'id': 0}},
                 {'address': 'Warps_RedsHouse1F', 'id': 2, 'to': {'map': "Player's House 2F", 'id': 0}}],
             'Celadon Pokemart 3F': [
                 {'address': 'Warps_CeladonMart3F', 'id': 0, 'to': {'map': 'Celadon Pokemart 4F', 'id': 0}},
                 {'address': 'Warps_CeladonMart3F', 'id': 1, 'to': {'map': 'Celadon Pokemart 2F', 'id': 1}},
                 {'address': 'Warps_CeladonMart3F', 'id': 2, 'to': {'map': 'Celadon Pokemart Elevator', 'id': 0}}],
             'Celadon Pokemart 4F': [
                 {'address': 'Warps_CeladonMart4F', 'id': 0, 'to': {'map': 'Celadon Pokemart 3F', 'id': 0}},
                 {'address': 'Warps_CeladonMart4F', 'id': 1, 'to': {'map': 'Celadon Pokemart 5F', 'id': 1}},
                 {'address': 'Warps_CeladonMart4F', 'id': 2, 'to': {'map': 'Celadon Pokemart Elevator', 'id': 0}}],
             'Celadon Pokemart Roof': [
                 {'address': 'Warps_CeladonMartRoof', 'id': 0, 'to': {'map': 'Celadon Pokemart 5F', 'id': 0}}],
             'Celadon Pokemart Elevator': [
                 {'address': 'CeladonMartElevatorWarpMaps', 'id': 0, 'to': {'map': 'Celadon Pokemart 1F', 'id': 5}},
                 {'address': 'CeladonMartElevatorWarpMaps', 'id': 1, 'to': {'map': 'Celadon Pokemart 2F', 'id': 2}},
                 {'address': 'CeladonMartElevatorWarpMaps', 'id': 2, 'to': {'map': 'Celadon Pokemart 3F', 'id': 2}},
                 {'address': 'CeladonMartElevatorWarpMaps', 'id': 3, 'to': {'map': 'Celadon Pokemart 4F', 'id': 2}},
                 {'address': 'CeladonMartElevatorWarpMaps', 'id': 4, 'to': {'map': 'Celadon Pokemart 5F', 'id': 2}}],
             'Celadon Mansion 1F': [
                 {'address': 'Warps_CeladonMansion1F', 'id': (0, 1), 'to': {'map': 'Celadon City', 'id': 2}},
                 {'address': 'Warps_CeladonMansion1F', 'id': 2, 'to': {'map': 'Celadon City', 'id': 4}},
                 {'address': 'Warps_CeladonMansion1F', 'id': 3, 'to': {'map': 'Celadon Mansion 2F', 'id': 1}},
                 {'address': 'Warps_CeladonMansion1F', 'id': 4, 'to': {'map': 'Celadon Mansion 2F', 'id': 2}}],
             'Celadon Mansion 2F': [
                 {'address': 'Warps_CeladonMansion2F', 'id': 0, 'to': {'map': 'Celadon Mansion 3F', 'id': 0}},
                 {'address': 'Warps_CeladonMansion2F', 'id': 1, 'to': {'map': 'Celadon Mansion 1F', 'id': 3}},
                 {'address': 'Warps_CeladonMansion2F', 'id': 2, 'to': {'map': 'Celadon Mansion 1F', 'id': 4}},
                 {'address': 'Warps_CeladonMansion2F', 'id': 3, 'to': {'map': 'Celadon Mansion 3F', 'id': 3}}],
             'Celadon Mansion 3F': [
                 {'address': 'Warps_CeladonMansion3F', 'id': 0, 'to': {'map': 'Celadon Mansion 2F', 'id': 0}},
                 {'address': 'Warps_CeladonMansion3F', 'id': 1, 'to': {'map': 'Celadon Mansion Roof', 'id': 0}},
                 {'address': 'Warps_CeladonMansion3F', 'id': 2, 'to': {'map': 'Celadon Mansion Roof', 'id': 1}},
                 {'address': 'Warps_CeladonMansion3F', 'id': 3, 'to': {'map': 'Celadon Mansion 2F', 'id': 3}}],
             'Celadon Mansion Roof': [
                 {'address': 'Warps_CeladonMansionRoof', 'id': 0, 'to': {'map': 'Celadon Mansion 3F', 'id': 1}},
                 {'address': 'Warps_CeladonMansionRoof', 'id': 1, 'to': {'map': 'Celadon Mansion 3F', 'id': 2}},
                 {'address': 'Warps_CeladonMansionRoof', 'id': 2,
                  'to': {'map': 'Celadon Mansion Roof House', 'id': 0}}], 'Celadon Pokemon Center': [
        {'address': 'Warps_CeladonPokecenter', 'id': (0, 1), 'to': {'map': 'Celadon City', 'id': 5}}],
             'Celadon Gym': [{'address': 'Warps_CeladonGym', 'id': (0, 1), 'to': {'map': 'Celadon City-G', 'id': 6}}],
             'Celadon Game Corner': [
                 {'address': 'Warps_GameCorner', 'id': (0, 1), 'to': {'map': 'Celadon City', 'id': 7}},
                 {'address': 'Warps_GameCorner', 'id': 2, 'to': {'map': 'Rocket Hideout B1F', 'id': 1}}],
             'Celadon Pokemart 5F': [
                 {'address': 'Warps_CeladonMart5F', 'id': 0, 'to': {'map': 'Celadon Pokemart Roof', 'id': 0}},
                 {'address': 'Warps_CeladonMart5F', 'id': 1, 'to': {'map': 'Celadon Pokemart 4F', 'id': 1}},
                 {'address': 'Warps_CeladonMart5F', 'id': 2, 'to': {'map': 'Celadon Pokemart Elevator', 'id': 0}}],
             'Celadon Prize Corner': [
                 {'address': 'Warps_GameCornerPrizeRoom', 'id': (0, 1), 'to': {'map': 'Celadon City', 'id': 9}}],
             'Celadon Diner': [
                 {'address': 'Warps_CeladonDiner', 'id': (0, 1), 'to': {'map': 'Celadon City', 'id': 10}}],
             'Celadon Chief House': [
                 {'address': 'Warps_CeladonChiefHouse', 'id': (0, 1), 'to': {'map': 'Celadon City', 'id': 11}}],
             'Celadon Hotel': [
                 {'address': 'Warps_CeladonHotel', 'id': (0, 1), 'to': {'map': 'Celadon City', 'id': 12}}],
             'Route 4 Pokemon Center': [
                 {'address': 'Warps_MtMoonPokecenter', 'id': (0, 1), 'to': {'map': 'Route 4-W', 'id': 0}}],
             'Rock Tunnel Pokemon Center': [
                 {'address': 'Warps_RockTunnelPokecenter', 'id': (0, 1), 'to': {'map': 'Route 10-N', 'id': 0}}],
             'Route 11 Gate 1F': [
                 {'address': 'Warps_Route11Gate1F', 'id': (0, 1), 'to': {'map': 'Route 11', 'id': (0, 1)}},
                 {'address': 'Warps_Route11Gate1F', 'id': (2, 3), 'to': {'map': 'Route 11', 'id': (2, 3)}},
                 {'address': 'Warps_Route11Gate1F', 'id': 4, 'to': {'map': 'Route 11 Gate 2F', 'id': 0}}],
             'Route 11 Gate 2F': [
                 {'address': 'Warps_Route11Gate2F', 'id': 0, 'to': {'map': 'Route 11 Gate 1F', 'id': 4}}],
             'Route 12 Gate 1F': [
                 {'address': 'Warps_Route12Gate1F', 'id': (0, 1), 'to': {'map': 'Route 12-L', 'id': (0, 1)}},
                 {'address': 'Warps_Route12Gate1F', 'id': (2, 3), 'to': {'map': 'Route 12-N', 'id': 2}},
                 {'address': 'Warps_Route12Gate1F', 'id': 4, 'to': {'map': 'Route 12 Gate 2F', 'id': 0}}],
             'Route 12 Gate 2F': [
                 {'address': 'Warps_Route12Gate2F', 'id': 0, 'to': {'map': 'Route 12 Gate 1F', 'id': 4}}],
             'Route 15 Gate 1F': [
                 {'address': 'Warps_Route15Gate1F', 'id': (0, 1), 'to': {'map': 'Route 15-W', 'id': (0, 1)}},
                 {'address': 'Warps_Route15Gate1F', 'id': (2, 3), 'to': {'map': 'Route 15', 'id': (2, 3)}},
                 {'address': 'Warps_Route15Gate1F', 'id': 4, 'to': {'map': 'Route 15 Gate 2F', 'id': 0}}],
             'Route 15 Gate 2F': [
                 {'address': 'Warps_Route15Gate2F', 'id': 0, 'to': {'map': 'Route 15 Gate 1F', 'id': 4}}],
             'Route 16 Gate 1F': [
                 {'address': 'Warps_Route16Gate1F', 'id': (0, 1), 'to': {'map': 'Route 16-SW', 'id': (0, 1)}},
                 {'address': 'Warps_Route16Gate1F', 'id': (2, 3), 'to': {'map': 'Route 16-C', 'id': 2}},
                 {'address': 'Warps_Route16Gate1F', 'id': 8, 'to': {'map': 'Route 16 Gate 2F', 'id': 0}}],
             'Route 16 Gate 1F-N': [
                 {'address': 'Warps_Route16Gate1F', 'id': (4, 5), 'to': {'map': 'Route 16-NW', 'id': (4, 5)}},
                 {'address': 'Warps_Route16Gate1F', 'id': (6, 7), 'to': {'map': 'Route 16-NE', 'id': (6, 7)}}],
             'Route 16 Gate 2F': [
                 {'address': 'Warps_Route16Gate2F', 'id': 0, 'to': {'map': 'Route 16 Gate 1F', 'id': 8}}],
             'Route 18 Gate 1F': [
                 {'address': 'Warps_Route18Gate1F', 'id': (0, 1), 'to': {'map': 'Route 18-W', 'id': (0, 1)}},
                 {'address': 'Warps_Route18Gate1F', 'id': (2, 3), 'to': {'map': 'Route 18-E', 'id': (2, 3)}},
                 {'address': 'Warps_Route18Gate1F', 'id': 4, 'to': {'map': 'Route 18 Gate 2F', 'id': 0}}],
             'Route 18 Gate 2F': [
                 {'address': 'Warps_Route18Gate2F', 'id': 0, 'to': {'map': 'Route 18 Gate 1F', 'id': 4}}],
             'Mt Moon 1F': [{'address': 'Warps_MtMoon1F', 'id': (0, 1), 'to': {'map': 'Route 4-W', 'id': 1}},
                            {'address': 'Warps_MtMoon1F', 'id': 2, 'to': {'map': 'Mt Moon B1F', 'id': 0}},
                            {'address': 'Warps_MtMoon1F', 'id': 3, 'to': {'map': 'Mt Moon B1F', 'id': 2}},
                            {'address': 'Warps_MtMoon1F', 'id': 4, 'to': {'map': 'Mt Moon B1F', 'id': 3}}],
             'Mt Moon B2F': [{'address': 'Warps_MtMoonB2F', 'id': 1, 'to': {'map': 'Mt Moon B1F', 'id': 4}},
                             {'address': 'Warps_MtMoonB2F', 'id': 3, 'to': {'map': 'Mt Moon B1F', 'id': 6}}],
             'Mt Moon B2F-NE': [{'address': 'Warps_MtMoonB2F', 'id': 0, 'to': {'map': 'Mt Moon B1F', 'id': 1}}],
             'Mt Moon B2F-C': [{'address': 'Warps_MtMoonB2F', 'id': 2, 'to': {'map': 'Mt Moon B1F', 'id': 5}}],
             'Safari Zone West': [
                 {'address': 'Warps_SafariZoneWest', 'id': 0, 'to': {'map': 'Safari Zone North', 'id': 0}},
                 {'address': 'Warps_SafariZoneWest', 'id': 1, 'to': {'map': 'Safari Zone North', 'id': 1}},
                 {'address': 'Warps_SafariZoneWest', 'id': 2, 'to': {'map': 'Safari Zone North', 'id': 2}},
                 {'address': 'Warps_SafariZoneWest', 'id': 3, 'to': {'map': 'Safari Zone North', 'id': 3}},
                 {'address': 'Warps_SafariZoneWest', 'id': 4, 'to': {'map': 'Safari Zone Center', 'id': 2}},
                 {'address': 'Warps_SafariZoneWest', 'id': 5, 'to': {'map': 'Safari Zone Center', 'id': 3}},
                 {'address': 'Warps_SafariZoneWest', 'id': 6, 'to': {'map': 'Safari Zone Secret House', 'id': 0}},
                 {'address': 'Warps_SafariZoneWest', 'id': 7, 'to': {'map': 'Safari Zone West Rest House', 'id': 0}}],
             'Safari Zone Secret House': [
                 {'address': 'Warps_SafariZoneSecretHouse', 'id': (0, 1), 'to': {'map': 'Safari Zone West', 'id': 6}}],
             'Trade Center': [], 'Colosseum': [],
             'Route 22': [{'address': 'Warps_Route22', 'id': 0, 'to': {'map': 'Route 22 Gate-S', 'id': (0, 1)}}],
             'Route 20-IW': [{'address': 'Warps_Route20', 'id': 0, 'to': {'map': 'Seafoam Islands 1F', 'id': 0}}],
             'Route 20-IE': [{'address': 'Warps_Route20', 'id': 1, 'to': {'map': 'Seafoam Islands 1F', 'id': 2}}],
             'Route 20-E': [], 'Route 20-W': [], 'Route 20-Water': [],
             'Route 23-S': [{'address': 'Warps_Route23', 'id': (0, 1), 'to': {'map': 'Route 22 Gate-N', 'id': (2, 3)}}],
             'Route 23-C': [{'address': 'Warps_Route23', 'id': 2, 'to': {'map': 'Victory Road 1F', 'id': 0}}],
             'Route 23-N': [{'address': 'Warps_Route23', 'id': 3, 'to': {'map': 'Victory Road 2F', 'id': 1}}],
             'Route 24': [],
             'Route 25': [{'address': 'Warps_Route25', 'id': 0, 'to': {'map': "Bill's House", 'id': 0}}],
             'Indigo Plateau': [
                 {'address': 'Warps_IndigoPlateau', 'id': (0, 1), 'to': {'map': 'Indigo Plateau Lobby', 'id': (0, 1)}}],
             'Saffron City': [
                 {'address': 'Warps_SaffronCity', 'id': 1, 'to': {'map': 'Saffron Fighting Dojo', 'id': 0}},
                 {'address': 'Warps_SaffronCity', 'id': 3, 'to': {'map': 'Saffron Pidgey House', 'id': 0}},
                 {'address': 'Warps_SaffronCity', 'id': 4, 'to': {'map': 'Saffron Pokemart', 'id': 0}},
                 {'address': 'Warps_SaffronCity', 'id': 6, 'to': {'map': 'Saffron Pokemon Center', 'id': 0}},
                 {'address': 'Warps_SaffronCity', 'id': 7, 'to': {'map': "Mr. Psychic's House", 'id': 0}}],
             'Saffron City-Copycat': [
                 {'address': 'Warps_SaffronCity', 'id': 0, 'to': {'map': "Saffron Copycat's House 1F", 'id': 0}}],
             'Saffron City-G': [{'address': 'Warps_SaffronCity', 'id': 2, 'to': {'map': 'Saffron Gym', 'id': 0}}],
             'Saffron City-Silph': [{'address': 'Warps_SaffronCity', 'id': 5, 'to': {'map': 'Silph Co 1F', 'id': 0}}],
             'Victory Road 2F': [{'address': 'Warps_VictoryRoad2F', 'id': 0, 'to': {'map': 'Victory Road 1F', 'id': 2}},
                                 {'address': 'Warps_VictoryRoad2F', 'id': (1, 2), 'to': {'map': 'Route 23-N', 'id': 3}},
                                 {'address': 'Warps_VictoryRoad2F', 'id': 3, 'to': {'map': 'Victory Road 3F', 'id': 0}},
                                 {'address': 'Warps_VictoryRoad2F', 'id': 4,
                                  'to': {'map': 'Victory Road 3F-SE', 'id': 2}},
                                 {'address': 'Warps_VictoryRoad2F', 'id': 5,
                                  'to': {'map': 'Victory Road 3F-SE', 'id': 1}},
                                 {'address': 'Warps_VictoryRoad2F', 'id': 6,
                                  'to': {'map': 'Victory Road 3F', 'id': 3}}],
             'Mt Moon B1F-W': [{'address': 'Warps_MtMoonB1F', 'id': 0, 'to': {'map': 'Mt Moon 1F', 'id': 2}},
                               {'address': 'Warps_MtMoonB1F', 'id': 4, 'to': {'map': 'Mt Moon B2F', 'id': 1}}],
             'Mt Moon B1F-C': [{'address': 'Warps_MtMoonB1F', 'id': 1, 'to': {'map': 'Mt Moon B2F-NE', 'id': 0}},
                             {'address': 'Warps_MtMoonB1F', 'id': 2, 'to': {'map': 'Mt Moon 1F', 'id': 3}}],
             'Mt Moon B1F-NE': [
                             {'address': 'Warps_MtMoonB1F', 'id': 6, 'to': {'map': 'Mt Moon B2F', 'id': 3}},
                             {'address': 'Warps_MtMoonB1F', 'id': 7, 'to': {'map': 'Route 4-E', 'id': 2}}],
             'Mt Moon B1F-SE': [
                             {'address': 'Warps_MtMoonB1F', 'id': 3, 'to': {'map': 'Mt Moon 1F', 'id': 4}},
                             {'address': 'Warps_MtMoonB1F', 'id': 5, 'to': {'map': 'Mt Moon B2F-C', 'id': 2}}],
             'Mt Moon B1F-Wild': [],
             'Silph Co 7F': [{'address': 'Warps_SilphCo7F', 'id': 0, 'to': {'map': 'Silph Co 8F', 'id': 1}},
                             {'address': 'Warps_SilphCo7F', 'id': 1, 'to': {'map': 'Silph Co 6F', 'id': 0}},
                             {'address': 'Warps_SilphCo7F', 'id': 2, 'to': {'map': 'Silph Co Elevator', 'id': 6}}],
             'Silph Co 7F-NW': [{'address': 'Warps_SilphCo7F', 'id': 4, 'to': {'map': 'Silph Co 3F-C', 'id': 8}},
                                {'address': 'Warps_SilphCo7F', 'id': 3, 'to': {'map': 'Silph Co 11F-W', 'id': 3}}],
             'Silph Co 7F-SE': [{'address': 'Warps_SilphCo7F', 'id': 5, 'to': {'map': 'Silph Co 5F', 'id': 3}}],
             'Silph Co 7F-E': [],
             'Silph Co 11F-C': [],
             'Route 2-NW': [{'address': 'Warps_Route2', 'id': 1, 'to': {'map': 'Viridian Forest North Gate', 'id': 1}}],
             'Route 2-SW': [{'address': 'Warps_Route2', 'id': 5, 'to': {'map': 'Viridian Forest South Gate', 'id': 2}}],
             'Route 2-NE': [{'address': 'Warps_Route2', 'id': 0, 'to': {'map': "Diglett's Cave Route 2", 'id': 0}},
                            {'address': 'Warps_Route2', 'id': 2, 'to': {'map': 'Route 2 Trade House', 'id': 0}}],
             'Route 2-E': [{'address': 'Warps_Route2', 'id': 3, 'to': {'map': 'Route 2 Gate', 'id': 1}}],
             'Route 2-SE': [{'address': 'Warps_Route2', 'id': 4, 'to': {'map': 'Route 2 Gate', 'id': 2}}],
             'Route 2-Grass': [], 'Route 3': [],
             'Route 4-W': [{'address': 'Warps_Route4', 'id': 0, 'to': {'map': 'Route 4 Pokemon Center', 'id': 0}},
                           {'address': 'Warps_Route4', 'id': 1, 'to': {'map': 'Mt Moon 1F', 'id': 0}}],
             'Route 4-E': [{'address': 'Warps_Route4', 'id': 2, 'to': {'map': 'Mt Moon B1F', 'id': 7}}],
             'Route 4-Lass': [],
             'Route 5': [{'address': 'Warps_Route5', 'id': (1, 0), 'to': {'map': 'Route 5 Gate-N', 'id': (3, 2)}},
                         {'address': 'Warps_Route5', 'id': 3, 'to': {'map': 'Underground Path Route 5', 'id': 0}},
                         {'address': 'Warps_Route5', 'id': 4, 'to': {'map': 'Daycare', 'id': 0}}], 'Route 9': [],
             'Route 5-S': [
                         {'address': 'Warps_Route5', 'id': 2, 'to': {'map': 'Route 5 Gate', 'id': 0}},],
             'Route 13': [], 'Route 13-E': [], 'Route 14': [], 'Route 14-Grass': [], 'Route 17': [], 'Route 19-S': [],
             'Route 19-N': [], 'Route 21': [],
             'Vermilion Old Rod House': [
                 {'address': 'Warps_VermilionOldRodHouse', 'id': (0, 1), 'to': {'map': 'Vermilion City', 'id': 8}}],
             'Celadon Pokemart 2F': [
                 {'address': 'Warps_CeladonMart2F', 'id': 0, 'to': {'map': 'Celadon Pokemart 1F', 'id': 4}},
                 {'address': 'Warps_CeladonMart2F', 'id': 1, 'to': {'map': 'Celadon Pokemart 3F', 'id': 1}},
                 {'address': 'Warps_CeladonMart2F', 'id': 2, 'to': {'map': 'Celadon Pokemart Elevator', 'id': 0}}],
             'Fuchsia Good Rod House': [{'address': 'Warps_FuchsiaGoodRodHouse', 'id': 0,
                                         'to': {'map': 'Fuchsia City-Good Rod House Backyard', 'id': 8}},
                                        {'address': 'Warps_FuchsiaGoodRodHouse', 'id': (1, 2),
                                         'to': {'map': 'Fuchsia City', 'id': 7}}],
             'Daycare': [{'address': 'Warps_Daycare', 'id': (0, 1), 'to': {'map': 'Route 5', 'id': 4}}],
             'Route 12 Super Rod House': [
                 {'address': 'Warps_Route12SuperRodHouse', 'id': (0, 1), 'to': {'map': 'Route 12-S', 'id': 3}}],
             'Silph Co 8F': [{'address': 'Warps_SilphCo8F', 'id': 0, 'to': {'map': 'Silph Co 9F', 'id': 1}},
                             {'address': 'Warps_SilphCo8F', 'id': 1, 'to': {'map': 'Silph Co 7F', 'id': 0}},
                             {'address': 'Warps_SilphCo8F', 'id': 2, 'to': {'map': 'Silph Co Elevator', 'id': 7}},
                             {'address': 'Warps_SilphCo8F', 'id': 4, 'to': {'map': 'Silph Co 2F', 'id': 4}},
                             {'address': 'Warps_SilphCo8F', 'id': 5, 'to': {'map': 'Silph Co 2F', 'id': 5}},
                             {'address': 'Warps_SilphCo8F', 'id': 6, 'to': {'map': 'Silph Co 8F-W', 'id': 3}}],
             'Silph Co 8F-W': [{'address': 'Warps_SilphCo8F', 'id': 3, 'to': {'map': 'Silph Co 8F', 'id': 6}}],
             'Route 6': [
                         {'address': 'Warps_Route6', 'id': 2, 'to': {'map': 'Route 6 Gate', 'id': 0}},
                         {'address': 'Warps_Route6', 'id': 3, 'to': {'map': 'Underground Path Route 6', 'id': 0}}],
             'Route 6-N': [{'address': 'Warps_Route6', 'id': 1, 'to': {'map': 'Route 6 Gate', 'id': 2}},],
             'Route 8-W': [{'address': 'Warps_Route8', 'id': (0, 1), 'to': {'map': 'Route 8 Gate', 'id': (0, 1)}}],
             'Route 8': [
                         {'address': 'Warps_Route8', 'id': (2, 3), 'to': {'map': 'Route 8 Gate', 'id': (2, 3)}},
                         {'address': 'Warps_Route8', 'id': 4, 'to': {'map': 'Underground Path Route 8', 'id': 0}}],
             'Route 8-Grass': [],
             'Route 10-N': [{'address': 'Warps_Route10', 'id': 0, 'to': {'map': 'Rock Tunnel Pokemon Center', 'id': 0}},
                            {'address': 'Warps_Route10', 'id': 1, 'to': {'map': 'Rock Tunnel 1F', 'id': 0}}],
             'Route 10-S': [{'address': 'Warps_Route10', 'id': 2, 'to': {'map': 'Rock Tunnel 1F', 'id': 2}}],
             'Route 10-P': [{'address': 'Warps_Route10', 'id': 3, 'to': {'map': 'Power Plant', 'id': 0}}],
             'Route 10-C': [],
             'Route 11': [
                          {'address': 'Warps_Route11', 'id': 4, 'to': {'map': "Diglett's Cave Route 11", 'id': 0}}],
             'Route 11-E': [
                          {'address': 'Warps_Route11', 'id': (2, 3), 'to': {'map': 'Route 11 Gate 1F', 'id': (2, 3)}}],
             'Route 11-C': [{'address': 'Warps_Route11', 'id': (0, 1), 'to': {'map': 'Route 11 Gate 1F', 'id': (0, 1)}}],
             'Route 12-L': [
                 {'address': 'Warps_Route12', 'id': (0, 1), 'to': {'map': 'Route 12 Gate 1F', 'id': (0, 1)}}],
             'Route 12-N': [{'address': 'Warps_Route12', 'id': 2, 'to': {'map': 'Route 12 Gate 1F', 'id': 2}}],
             'Route 12-S': [{'address': 'Warps_Route12', 'id': 3, 'to': {'map': 'Route 12 Super Rod House', 'id': 0}}],
             'Route 12-W': [],
             'Route 12-Grass': [],
             'Route 15-W': [
                 {'address': 'Warps_Route15', 'id': (0, 1), 'to': {'map': 'Route 15 Gate 1F', 'id': (0, 1)}}],
             'Route 15': [{'address': 'Warps_Route15', 'id': (2, 3), 'to': {'map': 'Route 15 Gate 1F', 'id': (2, 3)}}],
             'Route 16-E': [],
             'Route 16-C': [{'address': 'Warps_Route16', 'id': 2, 'to': {'map': 'Route 16 Gate 1F', 'id': (2, 3)}}],
             'Route 16-SW': [
                 {'address': 'Warps_Route16', 'id': (0, 1), 'to': {'map': 'Route 16 Gate 1F', 'id': (0, 1)}}],
             'Route 16-NW': [
                 {'address': 'Warps_Route16', 'id': (4, 5), 'to': {'map': 'Route 16 Gate 1F-N', 'id': (4, 5)}},
                 {'address': 'Warps_Route16', 'id': 8, 'to': {'map': 'Route 16 Fly House', 'id': 0}}], 'Route 16-NE': [
        {'address': 'Warps_Route16', 'id': (6, 7), 'to': {'map': 'Route 16 Gate 1F-N', 'id': (6, 7)}}], 'Route 18-W': [
        {'address': 'Warps_Route18', 'id': (0, 1), 'to': {'map': 'Route 18 Gate 1F', 'id': (0, 1)}}], 'Route 18-E': [
        {'address': 'Warps_Route18', 'id': (2, 3), 'to': {'map': 'Route 18 Gate 1F', 'id': (2, 3)}}],
             'Pokemon Fan Club': [
                 {'address': 'Warps_PokemonFanClub', 'id': (0, 1), 'to': {'map': 'Vermilion City', 'id': 1}}],
             'Silph Co 2F-NW': [{'address': 'Warps_SilphCo2F', 'id': 3, 'to': {'map': 'Silph Co 3F', 'id': 6}}],
             'Silph Co 2F': [{'address': 'Warps_SilphCo2F', 'id': 0, 'to': {'map': 'Silph Co 1F', 'id': 2}},
                             {'address': 'Warps_SilphCo2F', 'id': 1, 'to': {'map': 'Silph Co 3F', 'id': 0}},
                             {'address': 'Warps_SilphCo2F', 'id': 2, 'to': {'map': 'Silph Co Elevator', 'id': 1}},
                             {'address': 'Warps_SilphCo2F', 'id': 4, 'to': {'map': 'Silph Co 8F', 'id': 4}},
                             {'address': 'Warps_SilphCo2F', 'id': 5, 'to': {'map': 'Silph Co 8F', 'id': 5}}],
             'Silph Co 2F-SW': [{'address': 'Warps_SilphCo2F', 'id': 6, 'to': {'map': 'Silph Co 6F', 'id': 4}}],
             'Silph Co 3F': [{'address': 'Warps_SilphCo3F', 'id': 0, 'to': {'map': 'Silph Co 2F', 'id': 1}},
                             {'address': 'Warps_SilphCo3F', 'id': 1, 'to': {'map': 'Silph Co 4F', 'id': 0}},
                             {'address': 'Warps_SilphCo3F', 'id': 2, 'to': {'map': 'Silph Co Elevator', 'id': 2}},
                             {'address': 'Warps_SilphCo3F', 'id': 3, 'to': {'map': 'Silph Co 3F', 'id': 9}},
                             {'address': 'Warps_SilphCo3F', 'id': 4, 'to': {'map': 'Silph Co 5F', 'id': 5}},
                             {'address': 'Warps_SilphCo3F', 'id': 5, 'to': {'map': 'Silph Co 5F-SW', 'id': 6}},
                             {'address': 'Warps_SilphCo3F', 'id': 6, 'to': {'map': 'Silph Co 2F-NW', 'id': 3}},
                             {'address': 'Warps_SilphCo3F', 'id': 9, 'to': {'map': 'Silph Co 3F', 'id': 3}}],
             'Silph Co 3F-C': [{'address': 'Warps_SilphCo3F', 'id': 8, 'to': {'map': 'Silph Co 7F-NW', 'id': 4}}],
             'Silph Co 3F-W': [{'address': 'Warps_SilphCo3F', 'id': 7, 'to': {'map': 'Silph Co 9F-NW', 'id': 3}}],
             'Silph Co 10F': [{'address': 'Warps_SilphCo10F', 'id': 0, 'to': {'map': 'Silph Co 9F', 'id': 0}},
                              {'address': 'Warps_SilphCo10F', 'id': 1, 'to': {'map': 'Silph Co 11F', 'id': 0}},
                              {'address': 'Warps_SilphCo10F', 'id': 2, 'to': {'map': 'Silph Co Elevator', 'id': 9}},
                              {'address': 'Warps_SilphCo10F', 'id': 5, 'to': {'map': 'Silph Co 4F', 'id': 6}}],
             'Silph Co 10F-SE': [{'address': 'Warps_SilphCo10F', 'id': 3, 'to': {'map': 'Silph Co 4F-N', 'id': 3}},
                                 {'address': 'Warps_SilphCo10F', 'id': 4, 'to': {'map': 'Silph Co 4F', 'id': 5}}],
             "Lance's Room": [
                 {'address': 'Warps_LancesRoom', 'id': 0, 'to': {'map': "Indigo Plateau Agatha's Room", 'id': 2}},
                 {'address': 'Warps_LancesRoom', 'id': (1, 2),
                  'to': {'map': "Indigo Plateau Champion's Room", 'id': 0}}], 'Hall Of Fame': [
        {'address': 'Warps_HallOfFame', 'id': 0, 'to': {'map': "Indigo Plateau Champion's Room", 'id': 2}},
        {'address': 'Warps_HallOfFame', 'id': 1, 'to': {'map': "Indigo Plateau Champion's Room", 'id': 3}}],
             "Player's House 2F": [
                 {'address': 'Warps_RedsHouse2F', 'id': 0, 'to': {'map': "Player's House 1F", 'id': 2}}],
             'Pewter Museum 1F': [{'address': 'Warps_Museum1F', 'id': (0, 1), 'to': {'map': 'Pewter City', 'id': 0}},
                                  {'address': 'Warps_Museum1F', 'id': (2, 3), 'to': {'map': 'Pewter City', 'id': 1}},
                                  {'address': 'Warps_Museum1F', 'id': 4, 'to': {'map': 'Pewter Museum 2F', 'id': 0}}],
             'Pewter Museum 2F': [{'address': 'Warps_Museum2F', 'id': 0, 'to': {'map': 'Pewter Museum 1F', 'id': 4}}],
             'Pewter Gym': [{'address': 'Warps_PewterGym', 'id': (0, 1), 'to': {'map': 'Pewter City', 'id': 2}}],
             'Pewter Pokemon Center': [
                 {'address': 'Warps_PewterPokecenter', 'id': (0, 1), 'to': {'map': 'Pewter City', 'id': 6}}],
             'Cerulean Pokemon Center': [
                 {'address': 'Warps_CeruleanPokecenter', 'id': (0, 1), 'to': {'map': 'Cerulean City', 'id': 2}}],
             'Cerulean Gym': [{'address': 'Warps_CeruleanGym', 'id': (0, 1), 'to': {'map': 'Cerulean City', 'id': 3}}],
             'Cerulean Pokemart': [
                 {'address': 'Warps_CeruleanMart', 'id': (0, 1), 'to': {'map': 'Cerulean City', 'id': 5}}],
             'Lavender Pokemon Center': [
                 {'address': 'Warps_LavenderPokecenter', 'id': (0, 1), 'to': {'map': 'Lavender Town', 'id': 0}}],
             'Lavender Pokemart': [
                 {'address': 'Warps_LavenderMart', 'id': (0, 1), 'to': {'map': 'Lavender Town', 'id': 3}}],
             'Vermilion Pokemon Center': [
                 {'address': 'Warps_VermilionPokecenter', 'id': (0, 1), 'to': {'map': 'Vermilion City', 'id': 0}}],
             'Vermilion Pokemart': [
                 {'address': 'Warps_VermilionMart', 'id': (0, 1), 'to': {'map': 'Vermilion City', 'id': 2}}],
             'Vermilion Gym': [
                 {'address': 'Warps_VermilionGym', 'id': (0, 1), 'to': {'map': 'Vermilion City-G', 'id': 3}}],
             "Saffron Copycat's House 2F": [
                 {'address': 'Warps_CopycatsHouse2F', 'id': 0, 'to': {'map': "Saffron Copycat's House 1F", 'id': 2}}],
             'Saffron Fighting Dojo': [
                 {'address': 'Warps_FightingDojo', 'id': (0, 1), 'to': {'map': 'Saffron City', 'id': 1}}],
             'Saffron Gym-NW': [{'address': 'Warps_SaffronGym', 'id': 2, 'to': {'map': 'Saffron Gym-NE', 'id': 22}},
                                {'address': 'Warps_SaffronGym', 'id': 3, 'to': {'map': 'Saffron Gym-N', 'id': 15}},
                                {'address': 'Warps_SaffronGym', 'id': 4, 'to': {'map': 'Saffron Gym-C', 'id': 18}},
                                {'address': 'Warps_SaffronGym', 'id': 5, 'to': {'map': 'Saffron Gym-W', 'id': 8}}],
             'Saffron Gym-W': [{'address': 'Warps_SaffronGym', 'id': 6, 'to': {'map': 'Saffron Gym-E', 'id': 27}},
                               {'address': 'Warps_SaffronGym', 'id': 7, 'to': {'map': 'Saffron Gym-N', 'id': 16}},
                               {'address': 'Warps_SaffronGym', 'id': 8, 'to': {'map': 'Saffron Gym-NW', 'id': 5}},
                               {'address': 'Warps_SaffronGym', 'id': 9, 'to': {'map': 'Saffron Gym-SW', 'id': 13}}],
             'Saffron Gym-SW': [{'address': 'Warps_SaffronGym', 'id': 10, 'to': {'map': 'Saffron Gym-NE', 'id': 23}},
                                {'address': 'Warps_SaffronGym', 'id': 11, 'to': {'map': 'Saffron Gym-SE', 'id': 30}},
                                {'address': 'Warps_SaffronGym', 'id': 12, 'to': {'map': 'Saffron Gym-N', 'id': 17}},
                                {'address': 'Warps_SaffronGym', 'id': 13, 'to': {'map': 'Saffron Gym-W', 'id': 9}}],
             'Saffron Gym-N': [{'address': 'Warps_SaffronGym', 'id': 14, 'to': {'map': 'Saffron Gym-E', 'id': 26}},
                               {'address': 'Warps_SaffronGym', 'id': 15, 'to': {'map': 'Saffron Gym-NW', 'id': 3}},
                               {'address': 'Warps_SaffronGym', 'id': 16, 'to': {'map': 'Saffron Gym-W', 'id': 7}},
                               {'address': 'Warps_SaffronGym', 'id': 17, 'to': {'map': 'Saffron Gym-SW', 'id': 12}}],
             'Saffron Gym-C': [{'address': 'Warps_SaffronGym', 'id': 18, 'to': {'map': 'Saffron Gym-NW', 'id': 4}}],
             'Saffron Gym-S': [{'address': 'Warps_SaffronGym', 'id': 19, 'to': {'map': 'Saffron Gym-SE', 'id': 31}},
                               {'address': 'Warps_SaffronGym', 'id': (0, 1), 'to': {'map': 'Saffron City-G', 'id': 2}}],
             'Saffron Gym-NE': [{'address': 'Warps_SaffronGym', 'id': 20, 'to': {'map': 'Saffron Gym-E', 'id': 24}},
                                {'address': 'Warps_SaffronGym', 'id': 21, 'to': {'map': 'Saffron Gym-SE', 'id': 28}},
                                {'address': 'Warps_SaffronGym', 'id': 22, 'to': {'map': 'Saffron Gym-NW', 'id': 2}},
                                {'address': 'Warps_SaffronGym', 'id': 23, 'to': {'map': 'Saffron Gym-SW', 'id': 10}}],
             'Saffron Gym-E': [{'address': 'Warps_SaffronGym', 'id': 24, 'to': {'map': 'Saffron Gym-NE', 'id': 20}},
                               {'address': 'Warps_SaffronGym', 'id': 25, 'to': {'map': 'Saffron Gym-SE', 'id': 29}},
                               {'address': 'Warps_SaffronGym', 'id': 26, 'to': {'map': 'Saffron Gym-N', 'id': 14}},
                               {'address': 'Warps_SaffronGym', 'id': 27, 'to': {'map': 'Saffron Gym-W', 'id': 6}}],
             'Saffron Gym-SE': [{'address': 'Warps_SaffronGym', 'id': 28, 'to': {'map': 'Saffron Gym-NE', 'id': 21}},
                                {'address': 'Warps_SaffronGym', 'id': 29, 'to': {'map': 'Saffron Gym-E', 'id': 25}},
                                {'address': 'Warps_SaffronGym', 'id': 30, 'to': {'map': 'Saffron Gym-SW', 'id': 11}},
                                {'address': 'Warps_SaffronGym', 'id': 31, 'to': {'map': 'Saffron Gym-S', 'id': 19}}],
             'Saffron Pokemart': [
                 {'address': 'Warps_SaffronMart', 'id': (0, 1), 'to': {'map': 'Saffron City', 'id': 4}}],
             'Silph Co 1F': [{'address': 'Warps_SilphCo1F', 'id': (0, 1), 'to': {'map': 'Silph Co Elevator', 'id': 5}},
                             {'address': 'Warps_SilphCo1F', 'id': 2, 'to': {'map': 'Silph Co 2F', 'id': 0}},
                             {'address': 'Warps_SilphCo1F', 'id': 3, 'to': {'map': 'Silph Co Elevator', 'id': 0}},
                             {'address': 'Warps_SilphCo1F', 'id': 4, 'to': {'map': 'Silph Co 3F', 'id': 6}}],
             'Saffron Pokemon Center': [
                 {'address': 'Warps_SaffronPokecenter', 'id': (0, 1), 'to': {'map': 'Saffron City', 'id': 6}}],
             'Viridian Forest North Gate': [
                 {'address': 'Warps_ViridianForestNorthGate', 'id': 1, 'to': {'map': 'Route 2-NW', 'id': 1}},
                 {'address': 'Warps_ViridianForestNorthGate', 'id': (2, 3), 'to': {'map': 'Viridian Forest', 'id': 0}}],
             'Route 2 Gate': [{'address': 'Warps_Route2Gate', 'id': (0, 1), 'to': {'map': 'Route 2-E', 'id': 3}},
                              {'address': 'Warps_Route2Gate', 'id': (2, 3), 'to': {'map': 'Route 2-SE', 'id': 4}}],
             'Viridian Forest South Gate': [
                 {'address': 'Warps_ViridianForestSouthGate', 'id': 1, 'to': {'map': 'Viridian Forest', 'id': 4}},
                 {'address': 'Warps_ViridianForestSouthGate', 'id': (2, 3), 'to': {'map': 'Route 2-SW', 'id': 5}}],
             'Underground Path Route 5': [
                 {'address': 'Warps_UndergroundPathRoute5', 'id': (0, 1), 'to': {'map': 'Route 5', 'id': 3}},
                 {'address': 'Warps_UndergroundPathRoute5', 'id': 2,
                  'to': {'map': 'Underground Path North South', 'id': 0}}], 'Underground Path Route 6': [
        {'address': 'Warps_UndergroundPathRoute6', 'id': (0, 1), 'to': {'map': 'Route 6', 'id': 3}},
        {'address': 'Warps_UndergroundPathRoute6', 'id': 2, 'to': {'map': 'Underground Path North South', 'id': 1}}],
             'Underground Path Route 7': [
                 {'address': 'Warps_UndergroundPathRoute7', 'id': (0, 1), 'to': {'map': 'Route 7', 'id': 4}},
                 {'address': 'Warps_UndergroundPathRoute7', 'id': 2,
                  'to': {'map': 'Underground Path West East', 'id': 0}}],
             'Silph Co 9F-SW': [],
             'Silph Co 9F': [{'address': 'Warps_SilphCo9F', 'id': 0, 'to': {'map': 'Silph Co 10F', 'id': 0}},
                             {'address': 'Warps_SilphCo9F', 'id': 1, 'to': {'map': 'Silph Co 8F', 'id': 0}},
                             {'address': 'Warps_SilphCo9F', 'id': 2, 'to': {'map': 'Silph Co Elevator', 'id': 8}},
                             {'address': 'Warps_SilphCo9F', 'id': 4, 'to': {'map': 'Silph Co 5F', 'id': 4}}],
             'Silph Co 9F-NW': [{'address': 'Warps_SilphCo9F', 'id': 3, 'to': {'map': 'Silph Co 3F-W', 'id': 7}}],
             'Victory Road 1F': [{'address': 'Warps_VictoryRoad1F', 'id': (0, 1), 'to': {'map': 'Route 23-C', 'id': 2}},
                                 {'address': 'Warps_VictoryRoad1F', 'id': 2,
                                  'to': {'map': 'Victory Road 2F', 'id': 0}}], 'Pokemon Tower 1F': [
        {'address': 'Warps_PokemonTower1F', 'id': (0, 1), 'to': {'map': 'Lavender Town', 'id': 1}},
        {'address': 'Warps_PokemonTower1F', 'id': 2, 'to': {'map': 'Pokemon Tower 2F', 'id': 1}}], 'Pokemon Tower 2F': [
        {'address': 'Warps_PokemonTower2F', 'id': 0, 'to': {'map': 'Pokemon Tower 3F', 'id': 0}},
        {'address': 'Warps_PokemonTower2F', 'id': 1, 'to': {'map': 'Pokemon Tower 1F', 'id': 2}}], 'Pokemon Tower 3F': [
        {'address': 'Warps_PokemonTower3F', 'id': 0, 'to': {'map': 'Pokemon Tower 2F', 'id': 0}},
        {'address': 'Warps_PokemonTower3F', 'id': 1, 'to': {'map': 'Pokemon Tower 4F', 'id': 1}}], 'Pokemon Tower 4F': [
        {'address': 'Warps_PokemonTower4F', 'id': 0, 'to': {'map': 'Pokemon Tower 5F', 'id': 0}},
        {'address': 'Warps_PokemonTower4F', 'id': 1, 'to': {'map': 'Pokemon Tower 3F', 'id': 1}}], 'Pokemon Tower 5F': [
        {'address': 'Warps_PokemonTower5F', 'id': 0, 'to': {'map': 'Pokemon Tower 4F', 'id': 0}},
        {'address': 'Warps_PokemonTower5F', 'id': 1, 'to': {'map': 'Pokemon Tower 6F', 'id': 0}}], 'Pokemon Tower 6F': [
        {'address': 'Warps_PokemonTower6F', 'id': 0, 'to': {'map': 'Pokemon Tower 5F', 'id': 1}},
        {'address': 'Warps_PokemonTower6F', 'id': 1, 'to': {'map': 'Pokemon Tower 7F', 'id': 0}}], 'Pokemon Tower 7F': [
        {'address': 'Warps_PokemonTower7F', 'id': 0, 'to': {'map': 'Pokemon Tower 6F', 'id': 1}}],
             'Celadon Pokemart 1F': [
                 {'address': 'Warps_CeladonMart1F', 'id': (0, 1), 'to': {'map': 'Celadon City', 'id': 0}},
                 {'address': 'Warps_CeladonMart1F', 'id': (2, 3), 'to': {'map': 'Celadon City', 'id': 1}},
                 {'address': 'Warps_CeladonMart1F', 'id': 4, 'to': {'map': 'Celadon Pokemart 2F', 'id': 0}},
                 {'address': 'Warps_CeladonMart1F', 'id': 5, 'to': {'map': 'Celadon Pokemart Elevator', 'id': 0}}],
             'Viridian Forest': [{'address': 'Warps_ViridianForest', 'id': (0, 1),
                                  'to': {'map': 'Viridian Forest North Gate', 'id': (2, 3)}},
                                 {'address': 'Warps_ViridianForest', 'id': (2, 3, 4, 5),
                                  'to': {'map': 'Viridian Forest South Gate', 'id': 1}}],
             'S.S. Anne 1F': [{'address': 'Warps_SSAnne1F', 'id': (0, 1), 'to': {'map': 'Vermilion Dock', 'id': 1}},
                              {'address': 'Warps_SSAnne1F', 'id': 2, 'to': {'map': 'S.S. Anne 1F Rooms', 'id': 0}},
                              {'address': 'Warps_SSAnne1F', 'id': 3, 'to': {'map': 'S.S. Anne 1F Rooms', 'id': 1}},
                              {'address': 'Warps_SSAnne1F', 'id': 4, 'to': {'map': 'S.S. Anne 1F Rooms', 'id': 2}},
                              {'address': 'Warps_SSAnne1F', 'id': 5, 'to': {'map': 'S.S. Anne 1F Rooms', 'id': 3}},
                              {'address': 'Warps_SSAnne1F', 'id': 6, 'to': {'map': 'S.S. Anne 1F Rooms', 'id': 4}},
                              {'address': 'Warps_SSAnne1F', 'id': 7, 'to': {'map': 'S.S. Anne 1F Rooms', 'id': 5}},
                              {'address': 'Warps_SSAnne1F', 'id': 8, 'to': {'map': 'S.S. Anne 2F', 'id': 6}},
                              {'address': 'Warps_SSAnne1F', 'id': 9, 'to': {'map': 'S.S. Anne B1F', 'id': 5}},
                              {'address': 'Warps_SSAnne1F', 'id': 10, 'to': {'map': 'S.S. Anne Kitchen', 'id': 0}}],
             'S.S. Anne 2F': [{'address': 'Warps_SSAnne2F', 'id': 0, 'to': {'map': 'S.S. Anne 2F Rooms', 'id': 0}},
                              {'address': 'Warps_SSAnne2F', 'id': 1, 'to': {'map': 'S.S. Anne 2F Rooms', 'id': 2}},
                              {'address': 'Warps_SSAnne2F', 'id': 2, 'to': {'map': 'S.S. Anne 2F Rooms', 'id': 4}},
                              {'address': 'Warps_SSAnne2F', 'id': 3, 'to': {'map': 'S.S. Anne 2F Rooms', 'id': 6}},
                              {'address': 'Warps_SSAnne2F', 'id': 4, 'to': {'map': 'S.S. Anne 2F Rooms', 'id': 8}},
                              {'address': 'Warps_SSAnne2F', 'id': 5, 'to': {'map': 'S.S. Anne 2F Rooms', 'id': 10}},
                              {'address': 'Warps_SSAnne2F', 'id': 6, 'to': {'map': 'S.S. Anne 1F', 'id': 8}},
                              {'address': 'Warps_SSAnne2F', 'id': 7, 'to': {'map': 'S.S. Anne 3F', 'id': 1}},
                              {'address': 'Warps_SSAnne2F', 'id': 8,
                               'to': {'map': "S.S. Anne Captain's Room", 'id': 0}}],
             'S.S. Anne B1F': [{'address': 'Warps_SSAnneB1F', 'id': 0, 'to': {'map': 'S.S. Anne B1F Rooms', 'id': 8}},
                               {'address': 'Warps_SSAnneB1F', 'id': 1, 'to': {'map': 'S.S. Anne B1F Rooms', 'id': 6}},
                               {'address': 'Warps_SSAnneB1F', 'id': 2, 'to': {'map': 'S.S. Anne B1F Rooms', 'id': 4}},
                               {'address': 'Warps_SSAnneB1F', 'id': 3, 'to': {'map': 'S.S. Anne B1F Rooms', 'id': 2}},
                               {'address': 'Warps_SSAnneB1F', 'id': 4, 'to': {'map': 'S.S. Anne B1F Rooms', 'id': 0}},
                               {'address': 'Warps_SSAnneB1F', 'id': 5, 'to': {'map': 'S.S. Anne 1F', 'id': 9}}],
             'S.S. Anne Bow': [{'address': 'Warps_SSAnneBow', 'id': (0, 1), 'to': {'map': 'S.S. Anne 3F', 'id': 0}}],
             'S.S. Anne Kitchen': [
                 {'address': 'Warps_SSAnneKitchen', 'id': 0, 'to': {'map': 'S.S. Anne 1F', 'id': 10}}],
             "S.S. Anne Captain's Room": [
                 {'address': 'Warps_SSAnneCaptainsRoom', 'id': 0, 'to': {'map': 'S.S. Anne 2F', 'id': 8}}],
             'S.S. Anne 1F Rooms': [{'address': 'Warps_SSAnne1FRooms', 'id': 0, 'to': {'map': 'S.S. Anne 1F', 'id': 2}},
                                    {'address': 'Warps_SSAnne1FRooms', 'id': 1, 'to': {'map': 'S.S. Anne 1F', 'id': 3}},
                                    {'address': 'Warps_SSAnne1FRooms', 'id': 2, 'to': {'map': 'S.S. Anne 1F', 'id': 4}},
                                    {'address': 'Warps_SSAnne1FRooms', 'id': 3, 'to': {'map': 'S.S. Anne 1F', 'id': 5}},
                                    {'address': 'Warps_SSAnne1FRooms', 'id': 4, 'to': {'map': 'S.S. Anne 1F', 'id': 6}},
                                    {'address': 'Warps_SSAnne1FRooms', 'id': 5,
                                     'to': {'map': 'S.S. Anne 1F', 'id': 7}}], 'S.S. Anne 2F Rooms': [
        {'address': 'Warps_SSAnne2FRooms', 'id': (0, 1), 'to': {'map': 'S.S. Anne 2F', 'id': 0}},
        {'address': 'Warps_SSAnne2FRooms', 'id': (2, 3), 'to': {'map': 'S.S. Anne 2F', 'id': 1}},
        {'address': 'Warps_SSAnne2FRooms', 'id': (4, 5), 'to': {'map': 'S.S. Anne 2F', 'id': 2}},
        {'address': 'Warps_SSAnne2FRooms', 'id': (6, 7), 'to': {'map': 'S.S. Anne 2F', 'id': 3}},
        {'address': 'Warps_SSAnne2FRooms', 'id': (8, 9), 'to': {'map': 'S.S. Anne 2F', 'id': 4}},
        {'address': 'Warps_SSAnne2FRooms', 'id': (10, 11), 'to': {'map': 'S.S. Anne 2F', 'id': 5}}],
             'S.S. Anne B1F Rooms': [
                 {'address': 'Warps_SSAnneB1FRooms', 'id': (0, 1), 'to': {'map': 'S.S. Anne B1F', 'id': 4}},
                 {'address': 'Warps_SSAnneB1FRooms', 'id': (2, 3), 'to': {'map': 'S.S. Anne B1F', 'id': 3}},
                 {'address': 'Warps_SSAnneB1FRooms', 'id': (4, 5), 'to': {'map': 'S.S. Anne B1F', 'id': 2}},
                 {'address': 'Warps_SSAnneB1FRooms', 'id': (6, 7), 'to': {'map': 'S.S. Anne B1F', 'id': 1}},
                 {'address': 'Warps_SSAnneB1FRooms', 'id': (8, 9), 'to': {'map': 'S.S. Anne B1F', 'id': 0}}],
             'Underground Path North South': [{'address': 'Warps_UndergroundPathNorthSouth', 'id': 0,
                                               'to': {'map': 'Underground Path Route 5', 'id': 2}},
                                              {'address': 'Warps_UndergroundPathNorthSouth', 'id': 1,
                                               'to': {'map': 'Underground Path Route 6', 'id': 2}}],
             'Underground Path West East': [{'address': 'Warps_UndergroundPathWestEast', 'id': 0,
                                             'to': {'map': 'Underground Path Route 7', 'id': 2}},
                                            {'address': 'Warps_UndergroundPathWestEast', 'id': 1,
                                             'to': {'map': 'Underground Path Route 8', 'id': 2}}], "Diglett's Cave": [
        {'address': 'Warps_DiglettsCave', 'id': 0, 'to': {'map': "Diglett's Cave Route 2", 'id': 2}},
        {'address': 'Warps_DiglettsCave', 'id': 1, 'to': {'map': "Diglett's Cave Route 11", 'id': 2}}],
             'Silph Co 11F': [{'address': 'Warps_SilphCo11F', 'id': 0, 'to': {'map': 'Silph Co 10F', 'id': 1}},
                              {'address': 'Warps_SilphCo11F', 'id': 1, 'to': {'map': 'Silph Co Elevator', 'id': 10}}],
             'Silph Co 11F-W': [{'address': 'Warps_SilphCo11F', 'id': 3, 'to': {'map': 'Silph Co 7F-NW', 'id': 3}}],
             'Viridian Gym': [
                 {'address': 'Warps_ViridianGym', 'id': (0, 1), 'to': {'map': 'Viridian City-Gym', 'id': 4}}],
             'Pewter Pokemart': [{'address': 'Warps_PewterMart', 'id': (0, 1), 'to': {'map': 'Pewter City', 'id': 4}}],
             'Cerulean Cave 1F': [
                 {'address': 'Warps_CeruleanCave1F', 'id': (0, 1), 'to': {'map': 'Cerulean City-Cave', 'id': 6}},
                 {'address': 'Warps_CeruleanCave1F', 'id': 2, 'to': {'map': 'Cerulean Cave 2F-E', 'id': 0}},
                 {'address': 'Warps_CeruleanCave1F', 'id': 3, 'to': {'map': 'Cerulean Cave 2F-E', 'id': 1}},
                 {'address': 'Warps_CeruleanCave1F', 'id': 4, 'to': {'map': 'Cerulean Cave 2F-N', 'id': 2}},
                 {'address': 'Warps_CeruleanCave1F', 'id': 5, 'to': {'map': 'Cerulean Cave 2F-N', 'id': 3}},
                 {'address': 'Warps_CeruleanCave1F', 'id': 6, 'to': {'map': 'Cerulean Cave 2F-W', 'id': 4}},
                 {'address': 'Warps_CeruleanCave1F', 'id': 7, 'to': {'map': 'Cerulean Cave 2F-W', 'id': 5}},
                 {'address': 'Warps_CeruleanCave1F', 'id': 8, 'to': {'map': 'Cerulean Cave B1F', 'id': 0}}],
             'Cerulean Badge House': [
                 {'address': 'Warps_CeruleanBadgeHouse', 'id': 0, 'to': {'map': 'Cerulean City-Badge House Backyard', 'id': 9}},
                 {'address': 'Warps_CeruleanBadgeHouse', 'id': (1, 2), 'to': {'map': 'Cerulean City', 'id': 8}}],
             "Fuchsia Bill's Grandpa's House": [
                 {'address': 'Warps_FuchsiaBillsGrandpasHouse', 'id': (0, 1), 'to': {'map': 'Fuchsia City', 'id': 1}}],
             'Fuchsia Pokemon Center': [
                 {'address': 'Warps_FuchsiaPokecenter', 'id': (0, 1), 'to': {'map': 'Fuchsia City', 'id': 2}}],
             "Fuchsia Warden's House": [
                 {'address': 'Warps_WardensHouse', 'id': (0, 1), 'to': {'map': 'Fuchsia City', 'id': 3}}],
             'Safari Zone Gate-S': [
                 {'address': 'Warps_SafariZoneGate', 'id': (0, 1), 'to': {'map': 'Fuchsia City', 'id': 4}}],
             'Safari Zone Gate-N': [
                 {'address': 'Warps_SafariZoneGate', 'id': (2, 3), 'to': {'map': 'Safari Zone Center', 'id': (0, 1)}}],
             'Fuchsia Gym': [{'address': 'Warps_FuchsiaGym', 'id': (0, 1), 'to': {'map': 'Fuchsia City', 'id': 5}}],
             'Fuchsia Meeting Room': [
                 {'address': 'Warps_FuchsiaMeetingRoom', 'id': (0, 1), 'to': {'map': 'Fuchsia City', 'id': 6}}],
             'Cinnabar Gym': [
                 {'address': 'Warps_CinnabarGym', 'id': (0, 1), 'to': {'map': 'Cinnabar Island-G', 'id': 1}}],
             'Cinnabar Lab': [{'address': 'Warps_CinnabarLab', 'id': (0, 1), 'to': {'map': 'Cinnabar Island', 'id': 2}},
                              {'address': 'Warps_CinnabarLab', 'id': 2,
                               'to': {'map': 'Cinnabar Lab Trade Room', 'id': 0}},
                              {'address': 'Warps_CinnabarLab', 'id': 3,
                               'to': {'map': 'Cinnabar Lab Metronome Room', 'id': 0}},
                              {'address': 'Warps_CinnabarLab', 'id': 4,
                               'to': {'map': 'Cinnabar Lab Fossil Room', 'id': 0}}], 'Cinnabar Lab Trade Room': [
        {'address': 'Warps_CinnabarLabTradeRoom', 'id': (0, 1), 'to': {'map': 'Cinnabar Lab', 'id': 2}}],
             'Cinnabar Lab Metronome Room': [
                 {'address': 'Warps_CinnabarLabMetronomeRoom', 'id': (0, 1), 'to': {'map': 'Cinnabar Lab', 'id': 3}}],
             'Cinnabar Lab Fossil Room': [
                 {'address': 'Warps_CinnabarLabFossilRoom', 'id': (0, 1), 'to': {'map': 'Cinnabar Lab', 'id': 4}}],
             'Cinnabar Pokemon Center': [
                 {'address': 'Warps_CinnabarPokecenter', 'id': (0, 1), 'to': {'map': 'Cinnabar Island', 'id': 3}}],
             'Cinnabar Pokemart': [
                 {'address': 'Warps_CinnabarMart', 'id': (0, 1), 'to': {'map': 'Cinnabar Island', 'id': 4}}],
             "Saffron Copycat's House 1F": [
                 {'address': 'Warps_CopycatsHouse1F', 'id': (0, 1), 'to': {'map': 'Saffron City-Copycat', 'id': 0}},
                 {'address': 'Warps_CopycatsHouse1F', 'id': 2, 'to': {'map': "Saffron Copycat's House 2F", 'id': 0}}],
             "Indigo Plateau Champion's Room": [
                 {'address': 'Warps_ChampionsRoom', 'id': (0, 1), 'to': {'map': "Lance's Room", 'id': (1, 2)}},
                 {'address': 'Warps_ChampionsRoom', 'id': (2, 3), 'to': {'map': 'Hall Of Fame', 'id': 0}}],
             "Indigo Plateau Lorelei's Room": [
                 {'address': 'Warps_LoreleisRoom', 'id': (0, 1), 'to': {'map': 'Indigo Plateau Lobby', 'id': 2}},
                 {'address': 'Warps_LoreleisRoom', 'id': (2, 3),
                  'to': {'map': "Indigo Plateau Bruno's Room", 'id': (0, 1)}}], "Indigo Plateau Bruno's Room": [
        {'address': 'Warps_BrunosRoom', 'id': (0, 1), 'to': {'map': "Indigo Plateau Lorelei's Room", 'id': (2, 3)}},
        {'address': 'Warps_BrunosRoom', 'id': (2, 3), 'to': {'map': "Indigo Plateau Agatha's Room", 'id': (0, 1)}}],
             "Indigo Plateau Agatha's Room": [{'address': 'Warps_AgathasRoom', 'id': (0, 1),
                                               'to': {'map': "Indigo Plateau Bruno's Room", 'id': (2, 3)}},
                                              {'address': 'Warps_AgathasRoom', 'id': (2, 3),
                                               'to': {'map': "Lance's Room", 'id': 0}}]}



for region in warp_data:
    for entrance in warp_data[region]:
        m = entrance['to']["map"].split("-")[0]
        i = entrance['to']["id"]
        for region2 in warp_data:
            if region2.split("-")[0] == m:
                for entrance2 in warp_data[region2]:
                    if (entrance2["id"] == i or (isinstance(entrance2["id"], tuple) and i in entrance2["id"])) and region2 != m:
                        # print(f"change {entrance} to {region2}")
                        entrance["to"]["map"] = region2
print(warp_data)
# print(len([region for region in warp_data if len(warp_data[region]) == 1]))
# print(len([region for region in warp_data if len(warp_data[region]) == 2]))
# print(len([region for region in warp_data if len(warp_data[region]) > 2]))
# for region in warp_data:
#     for entrance in warp_data[region]:
#         c = entrance["to"]["map"]
#         i = entrance["to"]["id"]
#         for e in warp_data[c]:
#             if e["id"] == i:
#                 break
#             if isinstance(e["id"], tuple):
#                 if i in e["id"]:
#                     # print(f"{region} connecting to {c} {i} - should be {e['id']}")
#                     break
#         else:
#             print(f"{region} connecting to {c} {i}")



# for region in warp_data:
#     if region not in map_ids:
#         print(region)

# for region in warp_data:
#     for entrance in warp_data[region]:
#         entrance["address"] = "".join(entrance["address"].split(" "))
#         if entrance["to"]["map"] == 255:
#             for region_2 in warp_data:
#                 for entrance_2 in warp_data[region_2]:
#                     if entrance_2["to"]["map"] == region and (entrance_2["to"]["id"] == entrance["id"] or (isinstance(entrance["id"], tuple) and entrance_2["to"]["id"] in entrance["id"])):
#                         entrance["to"]["map"] = region_2
#                         break
#                 else:
#                     continue
#                 break
#             else:
#                 print("failed")
#                 print(entrance)
#
# print(warp_data)
#
# def process(word):
#     result = ""
#     last_letter = ""
#     for i in word:
#         if (i.isupper() and not last_letter.isnumeric()) or (i.isnumeric() and last_letter != "B"):
#             if last_letter == "s":
#                 result = result[:-1] + "'" + result[-1:]
#             result=result+" "+i.upper()
#
#         else:
#             result=result+i
#         last_letter = i
#     return result[1:]
#
# new_warp_data = {}
# for region in warp_data:
#     warps = []
#     new_warp_data[process(region)] = warps
#     for i, warp in enumerate(warp_data[region]):
#         id = warp["id"]
#         # warps.append({"address": f"*rom_addresses[\"Warps_{region}\"] + {id * 4}*", "map": map_ids[warp["map"]] if warp["map"] in map_ids else warp["map"], "id": warp["to"]})
#         warps.append({"address": "Warps_" + region, "id": id, "to": {"map": map_ids[warp["map"]] if warp["map"] in map_ids else warp["map"], "id": warp["to"]}})
#     #new_warp_data[f"Warps_{region}"] = warps
# print(new_warp_data)
