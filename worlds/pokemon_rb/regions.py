from copy import deepcopy
from BaseClasses import MultiWorld, Region, Entrance, LocationProgressType, ItemClassification
from .items import item_table, item_groups
from .locations import location_data, PokemonRBLocation
from . import logic
from . import poke_data

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
    "Cerulean Bicycle Shop": 0x42,
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
    "Vermilion Pokemon Fan Club": 0x5A,
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
    "Indigo Plateau Lance's Room": 0x71,
    # "Unused Map 72": 0x72,
    # "Unused Map 73": 0x73,
    # "Unused Map 74": 0x74,
    # "Unused Map 75": 0x75,
    "Indigo Plateau Hall of Fame": 0x76,
    "Underground Path North South": 0x77,
    "Indigo Plateau Champion's Room": 0x78,
    "Underground Path West East": 0x79,
    "Celadon Department Store 1F": 0x7A,
    "Celadon Department Store 2F": 0x7B,
    "Celadon Department Store 3F": 0x7C,
    "Celadon Department Store 4F": 0x7D,
    "Celadon Department Store Roof": 0x7E,
    "Celadon Department Store Elevator": 0x7F,
    "Celadon Mansion 1F": 0x80,
    "Celadon Mansion 2F": 0x81,
    "Celadon Mansion 3F": 0x82,
    "Celadon Mansion Roof": 0x83,
    "Celadon Mansion Roof House": 0x84,
    "Celadon Pokemon Center": 0x85,
    "Celadon Gym": 0x86,
    "Celadon Game Corner": 0x87,
    "Celadon Department Store 5F": 0x88,
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
    "Lavender Mr. Fuji's House": 0x95,
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
    "Cinnabar Lab R&D Room": 0xA9,
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
    "Saffron Mr. Psychic's House": 0xB7,
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

warp_data = {'Menu': [], 'Evolution': [], 'Old Rod Fishing': [], 'Good Rod Fishing': [], 'Fossil Level': [],
             'Pokedex': [], 'Fossil': [], 'Celadon City': [
        {'name': 'Celadon City to Celadon Department Store 1F W', 'address': 'Warps_CeladonCity', 'id': 0,
         'to': {'map': 'Celadon Department Store 1F', 'id': (1, 0)}},
        {'name': 'Celadon City to Celadon Department Store 1F E', 'address': 'Warps_CeladonCity', 'id': 1,
         'to': {'map': 'Celadon Department Store 1F', 'id': (3, 2)}},
        {'address': 'Warps_CeladonCity', 'id': 2, 'to': {'map': 'Celadon Mansion 1F', 'id': (0, 1)}},
        {'address': 'Warps_CeladonCity', 'id': (3, 4), 'to': {'map': 'Celadon Mansion 1F-Back', 'id': 2}},
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
        {'address': 'Warps_ViridianCity', 'id': 4, 'to': {'map': 'Viridian Gym', 'id': (0, 1)}}], 'Pewter City-E': [],
             'Pewter City-M': [
                 {'address': 'Warps_PewterCity', 'id': 1, 'to': {'map': 'Pewter Museum 1F-E', 'id': (2, 3)}}],
             'Pewter City': [{'address': 'Warps_PewterCity', 'id': 0, 'to': {'map': 'Pewter Museum 1F', 'id': (0, 1)}},
                             {'address': 'Warps_PewterCity', 'id': 2, 'to': {'map': 'Pewter Gym', 'id': (0, 1)}},
                             {'address': 'Warps_PewterCity', 'id': 3,
                              'to': {'map': 'Pewter Nidoran House', 'id': (0, 1)}},
                             {'address': 'Warps_PewterCity', 'id': 4, 'to': {'map': 'Pewter Pokemart', 'id': (0, 1)}},
                             {'address': 'Warps_PewterCity', 'id': 5,
                              'to': {'map': 'Pewter Speech House', 'id': (0, 1)}},
                             {'address': 'Warps_PewterCity', 'id': 6,
                              'to': {'map': 'Pewter Pokemon Center', 'id': (0, 1)}}], 'Cerulean City-T': [
        {'address': 'Warps_CeruleanCity', 'id': 0, 'to': {'map': 'Cerulean Trashed House', 'id': (0, 1)}}],
             'Cerulean City': [
                 {'address': 'Warps_CeruleanCity', 'id': 1, 'to': {'map': 'Cerulean Trade House', 'id': (0, 1)}},
                 {'address': 'Warps_CeruleanCity', 'id': 2, 'to': {'map': 'Cerulean Pokemon Center', 'id': (0, 1)}},
                 {'address': 'Warps_CeruleanCity', 'id': 3, 'to': {'map': 'Cerulean Gym', 'id': (0, 1)}},
                 {'address': 'Warps_CeruleanCity', 'id': 4, 'to': {'map': 'Cerulean Bicycle Shop', 'id': (0, 1)}},
                 {'address': 'Warps_CeruleanCity', 'id': 5, 'to': {'map': 'Cerulean Pokemart', 'id': (0, 1)}},
                 {'address': 'Warps_CeruleanCity', 'id': 8, 'to': {'map': 'Cerulean Badge House', 'id': (1, 2)}}],
             'Cerulean City-Badge House Backyard': [
                 {'address': 'Warps_CeruleanCity', 'id': 9, 'to': {'map': 'Cerulean Badge House', 'id': 0}}],
             'Cerulean City-Water': [], 'Cerulean City-Cave': [
        {'address': 'Warps_CeruleanCity', 'id': 6, 'to': {'map': 'Cerulean Cave 1F-SE', 'id': (0, 1)}}],
             'Cerulean City-Outskirts': [
                 {'address': 'Warps_CeruleanCity', 'id': 7, 'to': {'map': 'Cerulean Trashed House', 'id': 2}}],
             'Vermilion City': [
                 {'address': 'Warps_VermilionCity', 'id': 0, 'to': {'map': 'Vermilion Pokemon Center', 'id': (0, 1)}},
                 {'address': 'Warps_VermilionCity', 'id': 1, 'to': {'map': 'Vermilion Pokemon Fan Club', 'id': (0, 1)}},
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
                 {'address': 'Warps_IndigoPlateauLobby', 'id': (0, 1), 'to': {'map': 'Indigo Plateau', 'id': (0, 1)}}],
             'Indigo Plateau Lobby-N': [{'address': 'Warps_IndigoPlateauLobby', 'id': 2,
                                         'to': {'map': "Indigo Plateau Lorelei's Room", 'id': 0}}],
             'Silph Co 4F': [{'address': 'Warps_SilphCo4F', 'id': 0, 'to': {'map': 'Silph Co 3F', 'id': 1}},
                             {'address': 'Warps_SilphCo4F', 'id': 1, 'to': {'map': 'Silph Co 5F', 'id': 1}},
                             {'address': 'Warps_SilphCo4F', 'id': 2, 'to': {'map': 'Silph Co Elevator-4F', 'id': 3}},
                             {'address': 'Warps_SilphCo4F', 'id': 5, 'to': {'map': 'Silph Co 10F-SE', 'id': 4}},
                             {'address': 'Warps_SilphCo4F', 'id': 6, 'to': {'map': 'Silph Co 10F', 'id': 5}}],
             'Silph Co 4F-N': [{'address': 'Warps_SilphCo4F', 'id': 4, 'to': {'map': 'Silph Co 6F', 'id': 3}},
                               {'address': 'Warps_SilphCo4F', 'id': 3, 'to': {'map': 'Silph Co 10F-SE', 'id': 3}}],
             'Silph Co 4F-W': [], 'Silph Co 5F-NW': [], 'Silph Co 6F-SW': [],
             'Silph Co 5F': [{'address': 'Warps_SilphCo5F', 'id': 0, 'to': {'map': 'Silph Co 6F', 'id': 1}},
                             {'address': 'Warps_SilphCo5F', 'id': 1, 'to': {'map': 'Silph Co 4F', 'id': 1}},
                             {'address': 'Warps_SilphCo5F', 'id': 2, 'to': {'map': 'Silph Co Elevator-5F', 'id': 4}},
                             {'address': 'Warps_SilphCo5F', 'id': 3, 'to': {'map': 'Silph Co 7F-SE', 'id': 5}},
                             {'address': 'Warps_SilphCo5F', 'id': 4, 'to': {'map': 'Silph Co 9F', 'id': 4}},
                             {'address': 'Warps_SilphCo5F', 'id': 5, 'to': {'map': 'Silph Co 3F', 'id': 4}}],
             'Silph Co 5F-SW': [{'address': 'Warps_SilphCo5F', 'id': 6, 'to': {'map': 'Silph Co 3F', 'id': 5}}],
             'Silph Co 6F': [{'address': 'Warps_SilphCo6F', 'id': 0, 'to': {'map': 'Silph Co 7F', 'id': 1}},
                             {'address': 'Warps_SilphCo6F', 'id': 1, 'to': {'map': 'Silph Co 5F', 'id': 0}},
                             {'address': 'Warps_SilphCo6F', 'id': 2, 'to': {'map': 'Silph Co Elevator-7F', 'id': 6}},
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
                 {'address': 'Warps_CeruleanTrashedHouse', 'id': (0, 1), 'to': {'map': 'Cerulean City-T', 'id': 0}},
                 {'address': 'Warps_CeruleanTrashedHouse', 'id': 2, 'to': {'map': 'Cerulean City-Outskirts', 'id': 7}}],
             'Cerulean Trade House': [
                 {'address': 'Warps_CeruleanTradeHouse', 'id': (0, 1), 'to': {'map': 'Cerulean City', 'id': 1}}],
             'Cerulean Bicycle Shop': [
                 {'address': 'Warps_BikeShop', 'id': (0, 1), 'to': {'map': 'Cerulean City', 'id': 4}}],
             "Lavender Mr. Fuji's House": [
                 {'address': 'Warps_MrFujisHouse', 'id': (0, 1), 'to': {'map': 'Lavender Town', 'id': 2}}],
             'Lavender Cubone House': [
                 {'address': 'Warps_LavenderCuboneHouse', 'id': (0, 1), 'to': {'map': 'Lavender Town', 'id': 4}}],
             "Lavender Name Rater's House": [
                 {'address': 'Warps_NameRatersHouse', 'id': (0, 1), 'to': {'map': 'Lavender Town', 'id': 5}}],
             'Vermilion Pidgey House': [
                 {'address': 'Warps_VermilionPidgeyHouse', 'id': (0, 1), 'to': {'map': 'Vermilion City', 'id': 4}}],
             'Vermilion Dock': [
                 {'address': 'Warps_VermilionDock', 'id': 0, 'to': {'map': 'Vermilion City-Dock', 'id': 5}},
                 {'address': 'Warps_VermilionDock', 'id': 1, 'to': {'map': 'S.S. Anne 1F', 'id': 1}}],
             'Celadon Mansion Roof House': [{'address': 'Warps_CeladonMansionRoofHouse', 'id': (0, 1),
                                             'to': {'map': 'Celadon Mansion Roof-Back', 'id': 2}}],
             'Fuchsia Pokemart': [
                 {'address': 'Warps_FuchsiaMart', 'id': (0, 1), 'to': {'map': 'Fuchsia City', 'id': 0}}],
             'Saffron Pidgey House': [
                 {'address': 'Warps_SaffronPidgeyHouse', 'id': (0, 1), 'to': {'map': 'Saffron City-Pidgey', 'id': 3}}],
             "Saffron Mr. Psychic's House": [
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
             'Route 7 Gate-E': [
                 {'address': 'Warps_Route7Gate', 'id': (2, 3), 'to': {'map': 'Route 7-E', 'id': (0, 1)}}],
             'Route 8 Gate-W': [
                 {'address': 'Warps_Route8Gate', 'id': (0, 1), 'to': {'map': 'Route 8-W', 'id': (0, 1)}}],
             'Route 8 Gate-E': [{'address': 'Warps_Route8Gate', 'id': (2, 3), 'to': {'map': 'Route 8', 'id': (2, 3)}}],
             'Underground Path Route 8': [
                 {'address': 'Warps_UndergroundPathRoute8', 'id': (0, 1), 'to': {'map': 'Route 8', 'id': 4}},
                 {'address': 'Warps_UndergroundPathRoute8', 'id': 2,
                  'to': {'map': 'Underground Path West East', 'id': 1}}],
             'Power Plant': [{'address': 'Warps_PowerPlant', 'id': (0, 1), 'to': {'map': 'Route 10-P', 'id': 3}},
                             {'name': 'Power Plant to Route 10-P Back Door', 'address': 'Warps_PowerPlant', 'id': 2,
                              'to': {'map': 'Route 10-P', 'id': 3}}], "Diglett's Cave Route 11": [
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
                 {'address': 'Warps_LavenderTown', 'id': 2, 'to': {'map': "Lavender Mr. Fuji's House", 'id': 0}},
                 {'address': 'Warps_LavenderTown', 'id': 3, 'to': {'map': 'Lavender Pokemart', 'id': 0}},
                 {'address': 'Warps_LavenderTown', 'id': 4, 'to': {'map': 'Lavender Cubone House', 'id': 0}},
                 {'address': 'Warps_LavenderTown', 'id': 5, 'to': {'map': "Lavender Name Rater's House", 'id': 0}}],
             'Viridian Pokemon Center': [
                 {'address': 'Warps_ViridianPokecenter', 'id': (0, 1), 'to': {'map': 'Viridian City', 'id': 0}}],
             'Pokemon Mansion 1F-Wild': [], 'Pokemon Mansion 1F': [
        {'address': 'Warps_PokemonMansion1F', 'id': 4, 'to': {'map': 'Pokemon Mansion 2F', 'id': 0}},
        {'address': 'Warps_PokemonMansion1F', 'id': (0, 1, 2, 3), 'to': {'map': 'Cinnabar Island-M', 'id': 0}}],
             'Pokemon Mansion 1F-SE': [
                 {'address': 'Warps_PokemonMansion1F', 'id': 5, 'to': {'map': 'Pokemon Mansion B1F', 'id': 0}},
                 {'name': "Pokemon Mansion 1F-SE to Cinnabar Island-M", 'address': 'Warps_PokemonMansion1F',
                  'id': (6, 7), 'to': {'map': 'Cinnabar Island-M', 'id': 0}}],
             'Pokemon Mansion 2F': [
                 {'address': 'Warps_PokemonMansion2F', 'id': 0, 'to': {'map': 'Pokemon Mansion 1F', 'id': 4}},
                 {'address': 'Warps_PokemonMansion2F', 'id': 1, 'to': {'map': 'Pokemon Mansion 3F-SW', 'id': 0}},
                 {'address': 'Warps_PokemonMansion2F', 'id': 3, 'to': {'map': 'Pokemon Mansion 3F', 'id': 1}}],
             'Pokemon Mansion 2F-E': [
                 {'address': 'Warps_PokemonMansion2F', 'id': 2, 'to': {'map': 'Pokemon Mansion 3F-SE', 'id': 2}}],
             'Pokemon Mansion 3F-Wild': [], 'Pokemon Mansion 2F-Wild': [], 'Pokemon Mansion 3F': [
        {'address': 'Warps_PokemonMansion3F', 'id': 1, 'to': {'map': 'Pokemon Mansion 2F', 'id': 3}}],
             'Pokemon Mansion 3F-SE': [
                 {'address': 'Warps_PokemonMansion3F', 'id': 2, 'to': {'map': 'Pokemon Mansion 2F-E', 'id': 2}},],
             'Pokemon Mansion 3F-SW': [
                 {'address': 'Warps_PokemonMansion3F', 'id': 0, 'to': {'map': 'Pokemon Mansion 2F', 'id': 1}}],
             'Pokemon Mansion B1F': [
                 {'address': 'Warps_PokemonMansionB1F', 'id': 0, 'to': {'map': 'Pokemon Mansion 1F-SE', 'id': 5}}],
             'Rock Tunnel 1F-NE': [{'address': 'Warps_RockTunnel1F', 'id': 0, 'to': {'map': 'Route 10-N', 'id': 1}},
                                   {'address': 'Warps_RockTunnel1F', 'id': 4,
                                    'to': {'map': 'Rock Tunnel B1F-E', 'id': 0}}], 'Rock Tunnel 1F-NW': [
        {'address': 'Warps_RockTunnel1F', 'id': 5, 'to': {'map': 'Rock Tunnel B1F-E', 'id': 1}},
        {'address': 'Warps_RockTunnel1F', 'id': 6, 'to': {'map': 'Rock Tunnel B1F-W', 'id': 2}}],
             'Rock Tunnel 1F-S': [{'address': 'Warps_RockTunnel1F', 'id': 2, 'to': {'map': 'Route 10-S', 'id': 2}},
                                  {'address': 'Warps_RockTunnel1F', 'id': 7,
                                   'to': {'map': 'Rock Tunnel B1F-W', 'id': 3}}], 'Rock Tunnel 1F-Wild': [],
             'Rock Tunnel B1F-Wild': [], 'Seafoam Islands 1F': [
        {'address': 'Warps_SeafoamIslands1F', 'id': (2, 3), 'to': {'map': 'Route 20-IE', 'id': 1}},
        {'address': 'Warps_SeafoamIslands1F', 'id': 4, 'to': {'map': 'Seafoam Islands B1F', 'id': 1}},
        {'address': 'Warps_SeafoamIslands1F', 'id': 5, 'to': {'map': 'Seafoam Islands B1F-NE', 'id': 6}}],
             'Seafoam Islands B1F-Wild': [], 'Seafoam Islands 1F-Wild': [], 'Seafoam Islands 1F-SE': [
        {'address': 'Warps_SeafoamIslands1F', 'id': (0, 1), 'to': {'map': 'Route 20-IW', 'id': 0}},
        {'address': 'Warps_SeafoamIslands1F', 'id': 6, 'to': {'map': 'Seafoam Islands B1F-SE', 'id': 4}}],
             'S.S. Anne 3F': [{'address': 'Warps_SSAnne3F', 'id': 0, 'to': {'map': 'S.S. Anne Bow', 'id': 0}},
                              {'address': 'Warps_SSAnne3F', 'id': 1, 'to': {'map': 'S.S. Anne 2F', 'id': 7}}],
             'Victory Road 3F': [
                 {'address': 'Warps_VictoryRoad3F', 'id': 0, 'to': {'map': 'Victory Road 2F-C', 'id': 3}},
                 {'address': 'Warps_VictoryRoad3F', 'id': 3, 'to': {'map': 'Victory Road 2F-NW', 'id': 6}}],
             'Victory Road 3F-SE': [
                 {'address': 'Warps_VictoryRoad3F', 'id': 1, 'to': {'map': 'Victory Road 2F-E', 'id': 5}},
                 {'address': 'Warps_VictoryRoad3F', 'id': 2, 'to': {'map': 'Victory Road 2F-SE', 'id': 4}}],
             'Victory Road 3F-S': [], 'Victory Road 3F-Wild': [], 'Rocket Hideout B1F': [
        {'address': 'Warps_RocketHideoutB1F', 'id': 0, 'to': {'map': 'Rocket Hideout B2F', 'id': 0}},
        {'address': 'Warps_RocketHideoutB1F', 'id': 1, 'to': {'map': 'Celadon Game Corner-Hidden Stairs', 'id': 2}}],
             'Rocket Hideout B1F-SE': [{'address': 'Warps_RocketHideoutB1F', 'id': (2, 4),
                                        'to': {'map': 'Rocket Hideout Elevator-B1F', 'id': 0}}],
             'Rocket Hideout B1F-S': [
                 {'address': 'Warps_RocketHideoutB1F', 'id': 3, 'to': {'map': 'Rocket Hideout B2F', 'id': 3}}],
             'Rocket Hideout B2F': [
                 {'address': 'Warps_RocketHideoutB2F', 'id': 0, 'to': {'map': 'Rocket Hideout B1F', 'id': 0}},
                 {'address': 'Warps_RocketHideoutB2F', 'id': 1, 'to': {'map': 'Rocket Hideout B3F', 'id': 0}},
                 {'address': 'Warps_RocketHideoutB2F', 'id': (2, 4),
                  'to': {'map': 'Rocket Hideout Elevator-B2F', 'id': 1}},
                 {'address': 'Warps_RocketHideoutB2F', 'id': 3, 'to': {'map': 'Rocket Hideout B1F-S', 'id': 3}}],
             'Rocket Hideout B3F': [
                 {'address': 'Warps_RocketHideoutB3F', 'id': 0, 'to': {'map': 'Rocket Hideout B2F', 'id': 1}},
                 {'address': 'Warps_RocketHideoutB3F', 'id': 1, 'to': {'map': 'Rocket Hideout B4F-NW', 'id': 0}}],
             'Rocket Hideout B4F': [{'address': 'Warps_RocketHideoutB4F', 'id': (1, 2),
                                     'to': {'map': 'Rocket Hideout Elevator-B4F', 'id': 2}}], 'Rocket Hideout B4F-NW': [
        {'address': 'Warps_RocketHideoutB4F', 'id': 0, 'to': {'map': 'Rocket Hideout B3F', 'id': 1}}],
             'Rocket Hideout Elevator': [], 'Silph Co Elevator': [], 'Celadon Department Store Elevator': [],
             'Rocket Hideout Elevator-B1F': [{'address': 'RocketHideoutElevatorWarpMaps', 'id': 0,
                                              'to': {'map': 'Rocket Hideout B1F-SE', 'id': 4}}],
             'Rocket Hideout Elevator-B2F': [
                 {'address': 'RocketHideoutElevatorWarpMaps', 'id': 1, 'to': {'map': 'Rocket Hideout B2F', 'id': 4}}],
             'Rocket Hideout Elevator-B4F': [
                 {'address': 'RocketHideoutElevatorWarpMaps', 'id': 2, 'to': {'map': 'Rocket Hideout B4F', 'id': 2}}],
             'Silph Co Elevator-1F': [
                 {'address': 'SilphCoElevatorWarpMaps', 'id': 0, 'to': {'map': 'Silph Co 1F', 'id': 3}}],
             'Silph Co Elevator-2F': [
                 {'address': 'SilphCoElevatorWarpMaps', 'id': 1, 'to': {'map': 'Silph Co 2F', 'id': 2}}],
             'Silph Co Elevator-3F': [
                 {'address': 'SilphCoElevatorWarpMaps', 'id': 2, 'to': {'map': 'Silph Co 3F', 'id': 2}}],
             'Silph Co Elevator-4F': [
                 {'address': 'SilphCoElevatorWarpMaps', 'id': 3, 'to': {'map': 'Silph Co 4F', 'id': 2}}],
             'Silph Co Elevator-5F': [
                 {'address': 'SilphCoElevatorWarpMaps', 'id': 4, 'to': {'map': 'Silph Co 5F', 'id': 2}}],
             'Silph Co Elevator-6F': [
                 {'address': 'SilphCoElevatorWarpMaps', 'id': 5, 'to': {'map': 'Silph Co 6F', 'id': 2}}],
             'Silph Co Elevator-7F': [
                 {'address': 'SilphCoElevatorWarpMaps', 'id': 6, 'to': {'map': 'Silph Co 7F', 'id': 2}}],
             'Silph Co Elevator-8F': [
                 {'address': 'SilphCoElevatorWarpMaps', 'id': 7, 'to': {'map': 'Silph Co 8F', 'id': 2}}],
             'Silph Co Elevator-9F': [
                 {'address': 'SilphCoElevatorWarpMaps', 'id': 8, 'to': {'map': 'Silph Co 9F', 'id': 2}}],
             'Silph Co Elevator-10F': [
                 {'address': 'SilphCoElevatorWarpMaps', 'id': 9, 'to': {'map': 'Silph Co 10F', 'id': 2}}],
             'Silph Co Elevator-11F': [
                 {'address': 'SilphCoElevatorWarpMaps', 'id': 10, 'to': {'map': 'Silph Co 11F', 'id': 1}}],
             'Safari Zone East': [
                 {'address': 'Warps_SafariZoneEast', 'id': (0, 1), 'to': {'map': 'Safari Zone North', 'id': (6, 7)}},
                 {'address': 'Warps_SafariZoneEast', 'id': (2, 3), 'to': {'map': 'Safari Zone Center-S', 'id': (6, 7)}},
                 {'address': 'Warps_SafariZoneEast', 'id': 4, 'to': {'map': 'Safari Zone East Rest House', 'id': 0}}],
             'Safari Zone North': [
                 {'address': 'Warps_SafariZoneNorth', 'id': (0, 1), 'to': {'map': 'Safari Zone West-NW', 'id': (0, 1)}},
                 {'address': 'Warps_SafariZoneNorth', 'id': (2, 3), 'to': {'map': 'Safari Zone West', 'id': (2, 3)}},
                 {'address': 'Warps_SafariZoneNorth', 'id': (4, 5),
                  'to': {'map': 'Safari Zone Center-NE', 'id': (4, 5)}},
                 {'address': 'Warps_SafariZoneNorth', 'id': (6, 7), 'to': {'map': 'Safari Zone East', 'id': (0, 1)}},
                 {'address': 'Warps_SafariZoneNorth', 'id': 8, 'to': {'map': 'Safari Zone North Rest House', 'id': 0}}],
             'Safari Zone Center-C': [], 'Safari Zone Center-Wild': [], 'Safari Zone Center-NW': [
        {'address': 'Warps_SafariZoneCenter', 'id': (2, 3), 'to': {'map': 'Safari Zone West', 'id': (4, 5)}}],
             'Safari Zone Center-NE': [
                 {'address': 'Warps_SafariZoneCenter', 'id': (4, 5), 'to': {'map': 'Safari Zone North', 'id': (4, 5)}}],
             'Safari Zone Center-S': [
                 {'address': 'Warps_SafariZoneCenter', 'id': (0, 1), 'to': {'map': 'Safari Zone Gate-N', 'id': (2, 3)}},
                 {'address': 'Warps_SafariZoneCenter', 'id': (6, 7), 'to': {'map': 'Safari Zone East', 'id': (2, 3)}},
                 {'address': 'Warps_SafariZoneCenter', 'id': 8,
                  'to': {'map': 'Safari Zone Center Rest House', 'id': 0}}], 'Safari Zone Center Rest House': [
        {'address': 'Warps_SafariZoneCenterRestHouse', 'id': (0, 1), 'to': {'map': 'Safari Zone Center-S', 'id': 8}}],
             'Safari Zone West Rest House': [{'address': 'Warps_SafariZoneWestRestHouse', 'id': (0, 1),
                                              'to': {'map': 'Safari Zone West', 'id': 7}}],
             'Safari Zone East Rest House': [{'address': 'Warps_SafariZoneEastRestHouse', 'id': (0, 1),
                                              'to': {'map': 'Safari Zone East', 'id': 4}}],
             'Safari Zone North Rest House': [{'address': 'Warps_SafariZoneNorthRestHouse', 'id': (0, 1),
                                               'to': {'map': 'Safari Zone North', 'id': 8}}], 'Cerulean Cave 2F-E': [
        {'address': 'Warps_CeruleanCave2F', 'id': 0, 'to': {'map': 'Cerulean Cave 1F-NE', 'id': 2}},
        {'address': 'Warps_CeruleanCave2F', 'id': 1, 'to': {'map': 'Cerulean Cave 1F-SE', 'id': 3}}],
             'Cerulean Cave 2F-Wild': [], 'Cerulean Cave 2F-W': [
        {'address': 'Warps_CeruleanCave2F', 'id': 4, 'to': {'map': 'Cerulean Cave 1F-NW', 'id': 6}},
        {'address': 'Warps_CeruleanCave2F', 'id': 5, 'to': {'map': 'Cerulean Cave 1F-SW', 'id': 7}}],
             'Cerulean Cave 2F-N': [
                 {'address': 'Warps_CeruleanCave2F', 'id': 2, 'to': {'map': 'Cerulean Cave 1F-SW', 'id': 4}},
                 {'address': 'Warps_CeruleanCave2F', 'id': 3, 'to': {'map': 'Cerulean Cave 1F-N', 'id': 5}}],
             'Cerulean Cave B1F': [
                 {'address': 'Warps_CeruleanCaveB1F', 'id': 0, 'to': {'map': 'Cerulean Cave 1F-NW', 'id': 8}}],
             'Cerulean Cave B1F-E': [], 'Rock Tunnel B1F-E': [
        {'address': 'Warps_RockTunnelB1F', 'id': 0, 'to': {'map': 'Rock Tunnel 1F-NE', 'id': 4}},
        {'address': 'Warps_RockTunnelB1F', 'id': 1, 'to': {'map': 'Rock Tunnel 1F-NW', 'id': 5}}],
             'Rock Tunnel B1F-W': [
                 {'address': 'Warps_RockTunnelB1F', 'id': 2, 'to': {'map': 'Rock Tunnel 1F-NW', 'id': 6}},
                 {'address': 'Warps_RockTunnelB1F', 'id': 3, 'to': {'map': 'Rock Tunnel 1F-S', 'id': 7}}],
             'Seafoam Islands B1F': [
                 {'address': 'Warps_SeafoamIslandsB1F', 'id': 0, 'to': {'map': 'Seafoam Islands B2F-NW', 'id': 0}},
                 {'address': 'Warps_SeafoamIslandsB1F', 'id': 1, 'to': {'map': 'Seafoam Islands 1F', 'id': 4}},
                 {'name': 'Seafoam Islands B1F to Seafoam Islands B2F-SW N', 'address': 'Warps_SeafoamIslandsB1F',
                  'id': 2, 'to': {'map': 'Seafoam Islands B2F-SW', 'id': 2}},
                 {'name': 'Seafoam Islands B1F to Seafoam Islands B2F-SW S', 'address': 'Warps_SeafoamIslandsB1F',
                  'id': 3, 'to': {'map': 'Seafoam Islands B2F-SW', 'id': 3}}], 'Seafoam Islands B1F-SE': [
        {'address': 'Warps_SeafoamIslandsB1F', 'id': 4, 'to': {'map': 'Seafoam Islands 1F-SE', 'id': 6}},
        {'address': 'Warps_SeafoamIslandsB1F', 'id': 5, 'to': {'map': 'Seafoam Islands B2F-SE', 'id': 5}}],
             'Seafoam Islands B1F-NE': [
                 {'address': 'Warps_SeafoamIslandsB1F', 'id': 6, 'to': {'map': 'Seafoam Islands 1F', 'id': 5}}],
             'Seafoam Islands B2F-Wild': [], 'Seafoam Islands B2F-SE': [
        {'address': 'Warps_SeafoamIslandsB2F', 'id': 5, 'to': {'map': 'Seafoam Islands B1F-SE', 'id': 5}},
        {'address': 'Warps_SeafoamIslandsB2F', 'id': 6, 'to': {'map': 'Seafoam Islands B3F-SE', 'id': 4}}],
             'Seafoam Islands B2F-NE': [
                 {'address': 'Warps_SeafoamIslandsB2F', 'id': 4, 'to': {'map': 'Seafoam Islands B3F-NE', 'id': 3}}],
             'Seafoam Islands B2F-SW': [
                 {'name': 'Seafoam Islands B2F-SW to Seafoam Islands 1F-SW S', 'address': 'Warps_SeafoamIslandsB2F',
                  'id': 3, 'to': {'map': 'Seafoam Islands B1F', 'id': 3}},
                 {'address': 'Warps_SeafoamIslandsB2F', 'id': 1, 'to': {'map': 'Seafoam Islands B3F', 'id': 0}},
                 {'name': 'Seafoam Islands B2F-SW to Seafoam Islands 1F-SW N', 'address': 'Warps_SeafoamIslandsB2F',
                  'id': 2, 'to': {'map': 'Seafoam Islands B1F', 'id': 2}}], 'Seafoam Islands B2F-NW': [
        {'address': 'Warps_SeafoamIslandsB2F', 'id': 0, 'to': {'map': 'Seafoam Islands B1F', 'id': 0}}],
             'Seafoam Islands B3F': [
                 {'address': 'Warps_SeafoamIslandsB3F', 'id': 0, 'to': {'map': 'Seafoam Islands B2F-SW', 'id': 1}},
                 {'address': 'Warps_SeafoamIslandsB3F', 'id': 1, 'to': {'map': 'Seafoam Islands B4F', 'id': 2}}
                 ], 'Seafoam Islands B3F-SE': [
        {'address': 'Warps_SeafoamIslandsB3F', 'id': 4, 'to': {'map': 'Seafoam Islands B2F-SE', 'id': 6}}],
             'Seafoam Islands B3F-Wild': [], 'Seafoam Islands B3F-NE': [
        {'address': 'Warps_SeafoamIslandsB3F', 'id': 2, 'to': {'map': 'Seafoam Islands B4F', 'id': 3}},
        {'address': 'Warps_SeafoamIslandsB3F', 'id': 3, 'to': {'map': 'Seafoam Islands B2F-NE', 'id': 4}}],
             'Seafoam Islands B4F-W': [],
             'Seafoam Islands B4F': [
                                     {'address': 'Warps_SeafoamIslandsB4F', 'id': 2,
                                      'to': {'map': 'Seafoam Islands B3F', 'id': 1}},
                                     {'address': 'Warps_SeafoamIslandsB4F', 'id': 3,
                                      'to': {'map': 'Seafoam Islands B3F-NE', 'id': 2}}],
             'Route 7': [{'address': 'Warps_Route7', 'id': 3, 'to': {'map': 'Route 7 Gate-W', 'id': (0, 1)}},
                         {'address': 'Warps_Route7', 'id': 4, 'to': {'map': 'Underground Path Route 7', 'id': 0}}],
             'Route 7-E': [{'address': 'Warps_Route7', 'id': (0, 1), 'to': {'map': 'Route 7 Gate-E', 'id': (2, 3)}}],
             "Player's House 1F": [
                 {'address': 'Warps_RedsHouse1F', 'id': (0, 1), 'to': {'map': 'Pallet Town', 'id': 0}},
                 {'address': 'Warps_RedsHouse1F', 'id': 2, 'to': {'map': "Player's House 2F", 'id': 0}}],
             'Celadon Department Store 3F': [
                 {'address': 'Warps_CeladonMart3F', 'id': 0, 'to': {'map': 'Celadon Department Store 4F', 'id': 0}},
                 {'address': 'Warps_CeladonMart3F', 'id': 1, 'to': {'map': 'Celadon Department Store 2F', 'id': 1}},
                 {'address': 'Warps_CeladonMart3F', 'id': 2,
                  'to': {'map': 'Celadon Department Store Elevator-3F', 'id': 2}}], 'Celadon Department Store 4F': [
        {'address': 'Warps_CeladonMart4F', 'id': 0, 'to': {'map': 'Celadon Department Store 3F', 'id': 0}},
        {'address': 'Warps_CeladonMart4F', 'id': 1, 'to': {'map': 'Celadon Department Store 5F', 'id': 1}},
        {'address': 'Warps_CeladonMart4F', 'id': 2, 'to': {'map': 'Celadon Department Store Elevator-4F', 'id': 3}}],
             'Celadon Department Store Roof': [
                 {'address': 'Warps_CeladonMartRoof', 'id': 0, 'to': {'map': 'Celadon Department Store 5F', 'id': 0}}],
             'Celadon Department Store Elevator-1F': [{'address': 'CeladonMartElevatorWarpMaps', 'id': 0,
                                                       'to': {'map': 'Celadon Department Store 1F', 'id': 5}}],
             'Celadon Department Store Elevator-2F': [{'address': 'CeladonMartElevatorWarpMaps', 'id': 1,
                                                       'to': {'map': 'Celadon Department Store 2F', 'id': 2}}],
             'Celadon Department Store Elevator-3F': [{'address': 'CeladonMartElevatorWarpMaps', 'id': 2,
                                                       'to': {'map': 'Celadon Department Store 3F', 'id': 2}}],
             'Celadon Department Store Elevator-4F': [{'address': 'CeladonMartElevatorWarpMaps', 'id': 3,
                                                       'to': {'map': 'Celadon Department Store 4F', 'id': 2}}],
             'Celadon Department Store Elevator-5F': [{'address': 'CeladonMartElevatorWarpMaps', 'id': 4,
                                                       'to': {'map': 'Celadon Department Store 5F', 'id': 2}}],
             'Celadon Mansion 1F': [
                 {'address': 'Warps_CeladonMansion1F', 'id': (0, 1), 'to': {'map': 'Celadon City', 'id': 2}},
                 {'address': 'Warps_CeladonMansion1F', 'id': 3, 'to': {'map': 'Celadon Mansion 2F', 'id': 1}}],
             'Celadon Mansion 1F-Back': [
                 {'address': 'Warps_CeladonMansion1F', 'id': 4, 'to': {'map': 'Celadon Mansion 2F-Back', 'id': 2}},
                 {'address': 'Warps_CeladonMansion1F', 'id': 2, 'to': {'map': 'Celadon City', 'id': 4}}],
             'Celadon Mansion 2F': [
                 {'address': 'Warps_CeladonMansion2F', 'id': 0, 'to': {'map': 'Celadon Mansion 3F', 'id': 0}},
                 {'address': 'Warps_CeladonMansion2F', 'id': 1, 'to': {'map': 'Celadon Mansion 1F', 'id': 3}}],
             'Celadon Mansion 2F-Back': [
                 {'address': 'Warps_CeladonMansion2F', 'id': 2, 'to': {'map': 'Celadon Mansion 1F-Back', 'id': 4}},
                 {'address': 'Warps_CeladonMansion2F', 'id': 3, 'to': {'map': 'Celadon Mansion 3F-Back', 'id': 3}}],
             'Celadon Mansion 3F': [
                 {'address': 'Warps_CeladonMansion3F', 'id': 0, 'to': {'map': 'Celadon Mansion 2F', 'id': 0}},
                 {'address': 'Warps_CeladonMansion3F', 'id': 1, 'to': {'map': 'Celadon Mansion Roof', 'id': 0}}],
             'Celadon Mansion 3F-Back': [
                 {'address': 'Warps_CeladonMansion3F', 'id': 2, 'to': {'map': 'Celadon Mansion Roof-Back', 'id': 1}},
                 {'address': 'Warps_CeladonMansion3F', 'id': 3, 'to': {'map': 'Celadon Mansion 2F-Back', 'id': 3}}],
             'Celadon Mansion Roof': [
                 {'address': 'Warps_CeladonMansionRoof', 'id': 0, 'to': {'map': 'Celadon Mansion 3F', 'id': 1}}],
             'Celadon Mansion Roof-Back': [
                 {'address': 'Warps_CeladonMansionRoof', 'id': 1, 'to': {'map': 'Celadon Mansion 3F-Back', 'id': 2}},
                 {'address': 'Warps_CeladonMansionRoof', 'id': 2,
                  'to': {'map': 'Celadon Mansion Roof House', 'id': 0}}], 'Celadon Pokemon Center': [
        {'address': 'Warps_CeladonPokecenter', 'id': (0, 1), 'to': {'map': 'Celadon City', 'id': 5}}],
             'Celadon Gym': [{'address': 'Warps_CeladonGym', 'id': (0, 1), 'to': {'map': 'Celadon City-G', 'id': 6}}],
             'Celadon Gym-C': [], 'Celadon Game Corner': [
        {'address': 'Warps_GameCorner', 'id': (0, 1), 'to': {'map': 'Celadon City', 'id': 7}}],
             'Celadon Game Corner-Hidden Stairs': [
                 {'address': 'Warps_GameCorner', 'id': 2, 'to': {'map': 'Rocket Hideout B1F', 'id': 1}}],
             'Celadon Department Store 5F': [
                 {'address': 'Warps_CeladonMart5F', 'id': 0, 'to': {'map': 'Celadon Department Store Roof', 'id': 0}},
                 {'address': 'Warps_CeladonMart5F', 'id': 1, 'to': {'map': 'Celadon Department Store 4F', 'id': 1}},
                 {'address': 'Warps_CeladonMart5F', 'id': 2,
                  'to': {'map': 'Celadon Department Store Elevator-5F', 'id': 4}}], 'Celadon Prize Corner': [
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
                 {'address': 'Warps_Route11Gate1F', 'id': (0, 1), 'to': {'map': 'Route 11-C', 'id': (0, 1)}},
                 {'address': 'Warps_Route11Gate1F', 'id': (2, 3), 'to': {'map': 'Route 11-E', 'id': (2, 3)}},
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
             'Route 16 Gate 1F-W': [
                 {'address': 'Warps_Route16Gate1F', 'id': (0, 1), 'to': {'map': 'Route 16-SW', 'id': (0, 1)}}],
             'Route 16 Gate 1F-E': [
                 {'address': 'Warps_Route16Gate1F', 'id': (2, 3), 'to': {'map': 'Route 16-C', 'id': 2}},
                 {'address': 'Warps_Route16Gate1F', 'id': 8, 'to': {'map': 'Route 16 Gate 2F', 'id': 0}}],
             'Route 16 Gate 1F-N': [
                 {'address': 'Warps_Route16Gate1F', 'id': (4, 5), 'to': {'map': 'Route 16-NW', 'id': (4, 5)}},
                 {'address': 'Warps_Route16Gate1F', 'id': (6, 7), 'to': {'map': 'Route 16-NE', 'id': (6, 7)}}],
             'Route 16 Gate 2F': [
                 {'address': 'Warps_Route16Gate2F', 'id': 0, 'to': {'map': 'Route 16 Gate 1F-E', 'id': 8}}],
             'Route 18 Gate 1F-W': [
                 {'address': 'Warps_Route18Gate1F', 'id': (0, 1), 'to': {'map': 'Route 18-W', 'id': (0, 1)}}],
             'Route 18 Gate 1F-E': [
                 {'address': 'Warps_Route18Gate1F', 'id': (2, 3), 'to': {'map': 'Route 18-E', 'id': (2, 3)}},
                 {'address': 'Warps_Route18Gate1F', 'id': 4, 'to': {'map': 'Route 18 Gate 2F', 'id': 0}}],
             'Route 18 Gate 2F': [
                 {'address': 'Warps_Route18Gate2F', 'id': 0, 'to': {'map': 'Route 18 Gate 1F-E', 'id': 4}}],
             'Mt Moon 1F': [{'address': 'Warps_MtMoon1F', 'id': (0, 1), 'to': {'map': 'Route 4-W', 'id': 1}},
                            {'address': 'Warps_MtMoon1F', 'id': 2, 'to': {'map': 'Mt Moon B1F-W', 'id': 0}},
                            {'address': 'Warps_MtMoon1F', 'id': 3, 'to': {'map': 'Mt Moon B1F-C', 'id': 2}},
                            {'address': 'Warps_MtMoon1F', 'id': 4, 'to': {'map': 'Mt Moon B1F-SE', 'id': 3}}],
             'Mt Moon B2F': [{'address': 'Warps_MtMoonB2F', 'id': 1, 'to': {'map': 'Mt Moon B1F-W', 'id': 4}},
                             {'address': 'Warps_MtMoonB2F', 'id': 3, 'to': {'map': 'Mt Moon B1F-NE', 'id': 6}}],
             'Mt Moon B2F-NE': [{'address': 'Warps_MtMoonB2F', 'id': 0, 'to': {'map': 'Mt Moon B1F-C', 'id': 1}}],
             'Mt Moon B2F-C': [{'address': 'Warps_MtMoonB2F', 'id': 2, 'to': {'map': 'Mt Moon B1F-SE', 'id': 5}}],
             'Mt Moon B2F-Wild': [], 'Victory Road 1F-Wild': [], 'Pallet/Viridian Fishing': [], 'Route 22 Fishing': [],
             'Route 24/25/Cerulean/Cerulean Gym Fishing': [], 'Route 6/11/Vermilion/Dock Fishing': [],
             'Route 10/Celadon Fishing': [], 'Safari Zone Fishing': [], 'Route 12/13/17/18 Fishing': [],
             'Sea Routes/Cinnabar/Seafoam Fishing': [], 'Route 23/Cerulean Cave Fishing': [], 'Fuchsia Fishing': [],
             'Safari Zone West': [
                 {'address': 'Warps_SafariZoneWest', 'id': (2, 3), 'to': {'map': 'Safari Zone North', 'id': (2, 3)}},
                 {'address': 'Warps_SafariZoneWest', 'id': (4, 5),
                  'to': {'map': 'Safari Zone Center-NW', 'id': (2, 3)}},
                 {'address': 'Warps_SafariZoneWest', 'id': 7, 'to': {'map': 'Safari Zone West Rest House', 'id': 0}}],
             'Safari Zone West-NW': [
                 {'address': 'Warps_SafariZoneWest', 'id': (0, 1), 'to': {'map': 'Safari Zone North', 'id': (0, 1)}},
                 {'address': 'Warps_SafariZoneWest', 'id': 6, 'to': {'map': 'Safari Zone Secret House', 'id': 0}}],
             'Safari Zone West-Wild': [], 'Safari Zone Secret House': [
        {'address': 'Warps_SafariZoneSecretHouse', 'id': (0, 1), 'to': {'map': 'Safari Zone West-NW', 'id': 6}}],
             'Route 22': [{'address': 'Warps_Route22', 'id': 0, 'to': {'map': 'Route 22 Gate-S', 'id': (0, 1)}}],
             'Route 22-F': [],
             'Route 20-IW': [{'address': 'Warps_Route20', 'id': 0, 'to': {'map': 'Seafoam Islands 1F-SE', 'id': 0}}],
             'Route 20-IE': [{'address': 'Warps_Route20', 'id': 1, 'to': {'map': 'Seafoam Islands 1F', 'id': 2}}],
             'Route 20-E': [], 'Route 20-W': [], 'Route 19/20-Water': [],
             'Route 23-S': [{'address': 'Warps_Route23', 'id': (0, 1), 'to': {'map': 'Route 22 Gate-N', 'id': (2, 3)}}],
             'Route 23-C': [{'address': 'Warps_Route23', 'id': 2, 'to': {'map': 'Victory Road 1F-S', 'id': 0}}],
             'Route 23-N': [{'address': 'Warps_Route23', 'id': 3, 'to': {'map': 'Victory Road 2F-E', 'id': 1}}],
             'Route 23-Grass': [], 'Route 24': [],
             'Route 25': [{'address': 'Warps_Route25', 'id': 0, 'to': {'map': "Bill's House", 'id': 0}}],
             'Indigo Plateau': [
                 {'address': 'Warps_IndigoPlateau', 'id': (0, 1), 'to': {'map': 'Indigo Plateau Lobby', 'id': (0, 1)}}],
             'Saffron City': [
                 {'address': 'Warps_SaffronCity', 'id': 1, 'to': {'map': 'Saffron Fighting Dojo', 'id': 0}},
                 {'address': 'Warps_SaffronCity', 'id': 4, 'to': {'map': 'Saffron Pokemart', 'id': 0}},
                 {'address': 'Warps_SaffronCity', 'id': 6, 'to': {'map': 'Saffron Pokemon Center', 'id': 0}},
                 {'address': 'Warps_SaffronCity', 'id': 7, 'to': {'map': "Saffron Mr. Psychic's House", 'id': 0}}],
             'Saffron City-Pidgey': [
                 {'address': 'Warps_SaffronCity', 'id': 3, 'to': {'map': 'Saffron Pidgey House', 'id': 0}}],
             'Saffron City-Copycat': [
                 {'address': 'Warps_SaffronCity', 'id': 0, 'to': {'map': "Saffron Copycat's House 1F", 'id': 0}}],
             'Saffron City-G': [{'address': 'Warps_SaffronCity', 'id': 2, 'to': {'map': 'Saffron Gym-S', 'id': 0}}],
             'Saffron City-Silph': [{'address': 'Warps_SaffronCity', 'id': 5, 'to': {'map': 'Silph Co 1F', 'id': 0}}],
             'Victory Road 2F-E': [
                 {'address': 'Warps_VictoryRoad2F', 'id': (1, 2), 'to': {'map': 'Route 23-N', 'id': 3}},
                 {'address': 'Warps_VictoryRoad2F', 'id': 5, 'to': {'map': 'Victory Road 3F-SE', 'id': 1}}],
             'Victory Road 2F-W': [
                 {'address': 'Warps_VictoryRoad2F', 'id': 0, 'to': {'map': 'Victory Road 1F', 'id': 2}}],
             'Victory Road 2F-NW': [
                 {'address': 'Warps_VictoryRoad2F', 'id': 6, 'to': {'map': 'Victory Road 3F', 'id': 3}}],
             'Victory Road 2F-C': [
                 {'address': 'Warps_VictoryRoad2F', 'id': 3, 'to': {'map': 'Victory Road 3F', 'id': 0}}],
             'Victory Road 2F-SE': [
                 {'address': 'Warps_VictoryRoad2F', 'id': 4, 'to': {'map': 'Victory Road 3F-SE', 'id': 2}}],
             'Victory Road 2F-Wild': [],
             'Mt Moon B1F-W': [{'address': 'Warps_MtMoonB1F', 'id': 0, 'to': {'map': 'Mt Moon 1F', 'id': 2}},
                               {'address': 'Warps_MtMoonB1F', 'id': 4, 'to': {'map': 'Mt Moon B2F', 'id': 1}}],
             'Mt Moon B1F-C': [{'address': 'Warps_MtMoonB1F', 'id': 1, 'to': {'map': 'Mt Moon B2F-NE', 'id': 0}},
                               {'address': 'Warps_MtMoonB1F', 'id': 2, 'to': {'map': 'Mt Moon 1F', 'id': 3}}],
             'Mt Moon B1F-NE': [{'address': 'Warps_MtMoonB1F', 'id': 6, 'to': {'map': 'Mt Moon B2F', 'id': 3}},
                                {'address': 'Warps_MtMoonB1F', 'id': 7, 'to': {'map': 'Route 4-C', 'id': 2}}],
             'Mt Moon B1F-SE': [{'address': 'Warps_MtMoonB1F', 'id': 3, 'to': {'map': 'Mt Moon 1F', 'id': 4}},
                                {'address': 'Warps_MtMoonB1F', 'id': 5, 'to': {'map': 'Mt Moon B2F-C', 'id': 2}}],
             'Mt Moon B1F-Wild': [],
             'Silph Co 7F': [{'address': 'Warps_SilphCo7F', 'id': 0, 'to': {'map': 'Silph Co 8F', 'id': 1}},
                             {'address': 'Warps_SilphCo7F', 'id': 1, 'to': {'map': 'Silph Co 6F', 'id': 0}},
                             {'address': 'Warps_SilphCo7F', 'id': 2, 'to': {'map': 'Silph Co Elevator-7F', 'id': 6}}],
             'Silph Co 7F-NW': [{'address': 'Warps_SilphCo7F', 'id': 4, 'to': {'map': 'Silph Co 3F-C', 'id': 8}},
                                {'address': 'Warps_SilphCo7F', 'id': 3, 'to': {'map': 'Silph Co 11F-W', 'id': 3}}],
             'Silph Co 7F-SE': [{'address': 'Warps_SilphCo7F', 'id': 5, 'to': {'map': 'Silph Co 5F', 'id': 3}}],
             'Silph Co 7F-E': [], 'Silph Co 11F-C': [],
             'Route 2-NW': [{'address': 'Warps_Route2', 'id': 1, 'to': {'map': 'Viridian Forest North Gate', 'id': 1}}],
             'Route 2-SW': [{'address': 'Warps_Route2', 'id': 5, 'to': {'map': 'Viridian Forest South Gate', 'id': 2}}],
             'Route 2-NE': [{'address': 'Warps_Route2', 'id': 0, 'to': {'map': "Diglett's Cave Route 2", 'id': 0}},
                            {'address': 'Warps_Route2', 'id': 2, 'to': {'map': 'Route 2 Trade House', 'id': 0}}],
             'Route 2-E': [{'address': 'Warps_Route2', 'id': 3, 'to': {'map': 'Route 2 Gate', 'id': 1}}],
             'Route 2-SE': [{'address': 'Warps_Route2', 'id': 4, 'to': {'map': 'Route 2 Gate', 'id': 2}}],
             'Route 2-Grass': [], 'Route 3': [],
             'Route 4-W': [{'address': 'Warps_Route4', 'id': 0, 'to': {'map': 'Route 4 Pokemon Center', 'id': 0}},
                           {'address': 'Warps_Route4', 'id': 1, 'to': {'map': 'Mt Moon 1F', 'id': 0}}],
             'Route 4-C': [{'address': 'Warps_Route4', 'id': 2, 'to': {'map': 'Mt Moon B1F-NE', 'id': 7}}],
             'Route 4-E': [], 'Route 4-Lass': [], 'Route 4-Grass': [],
             'Route 5': [{'address': 'Warps_Route5', 'id': (1, 0), 'to': {'map': 'Route 5 Gate-N', 'id': (3, 2)}},
                         {'address': 'Warps_Route5', 'id': 3, 'to': {'map': 'Underground Path Route 5', 'id': 0}},
                         {'address': 'Warps_Route5', 'id': 4, 'to': {'map': 'Daycare', 'id': 0}}], 'Route 9': [],
             'Route 5-S': [{'address': 'Warps_Route5', 'id': 2, 'to': {'map': 'Route 5 Gate-S', 'id': 0}}],
             'Route 13': [], 'Route 13-E': [], 'Route 13-Grass': [], 'Route 14': [], 'Route 14-Grass': [],
             'Route 17': [], 'Route 19-S': [], 'Route 19-N': [], 'Route 21': [], 'Vermilion Old Rod House': [
        {'address': 'Warps_VermilionOldRodHouse', 'id': (0, 1), 'to': {'map': 'Vermilion City', 'id': 8}}],
             'Celadon Department Store 2F': [
                 {'address': 'Warps_CeladonMart2F', 'id': 0, 'to': {'map': 'Celadon Department Store 1F', 'id': 4}},
                 {'address': 'Warps_CeladonMart2F', 'id': 1, 'to': {'map': 'Celadon Department Store 3F', 'id': 1}},
                 {'address': 'Warps_CeladonMart2F', 'id': 2,
                  'to': {'map': 'Celadon Department Store Elevator-2F', 'id': 1}}], 'Fuchsia Good Rod House': [
        {'address': 'Warps_FuchsiaGoodRodHouse', 'id': 0,
         'to': {'map': 'Fuchsia City-Good Rod House Backyard', 'id': 8}},
        {'address': 'Warps_FuchsiaGoodRodHouse', 'id': (1, 2), 'to': {'map': 'Fuchsia City', 'id': 7}}],
             'Daycare': [{'address': 'Warps_Daycare', 'id': (0, 1), 'to': {'map': 'Route 5', 'id': 4}}],
             'Route 12 Super Rod House': [
                 {'address': 'Warps_Route12SuperRodHouse', 'id': (0, 1), 'to': {'map': 'Route 12-S', 'id': 3}}],
             'Silph Co 8F': [{'address': 'Warps_SilphCo8F', 'id': 0, 'to': {'map': 'Silph Co 9F', 'id': 1}},
                             {'address': 'Warps_SilphCo8F', 'id': 1, 'to': {'map': 'Silph Co 7F', 'id': 0}},
                             {'address': 'Warps_SilphCo8F', 'id': 2, 'to': {'map': 'Silph Co Elevator-8F', 'id': 7}},
                             {'name': 'Silph Co 8F to Silph Co 2F S', 'address': 'Warps_SilphCo8F', 'id': 4,
                              'to': {'map': 'Silph Co 2F', 'id': 4}},
                             {'name': 'Silph Co 8F to Silph Co 2F N', 'address': 'Warps_SilphCo8F', 'id': 5,
                              'to': {'map': 'Silph Co 2F', 'id': 5}},
                             {'address': 'Warps_SilphCo8F', 'id': 6, 'to': {'map': 'Silph Co 8F-W', 'id': 3}}],
             'Silph Co 8F-W': [{'address': 'Warps_SilphCo8F', 'id': 3, 'to': {'map': 'Silph Co 8F', 'id': 6}}],
             'Route 6': [{'address': 'Warps_Route6', 'id': 2, 'to': {'map': 'Route 6 Gate-S', 'id': 0}},
                         {'address': 'Warps_Route6', 'id': 3, 'to': {'map': 'Underground Path Route 6', 'id': 0}}],
             'Route 6-N': [{'address': 'Warps_Route6', 'id': 1, 'to': {'map': 'Route 6 Gate-N', 'id': 2}}],
             'Route 8-W': [{'address': 'Warps_Route8', 'id': (0, 1), 'to': {'map': 'Route 8 Gate-W', 'id': (0, 1)}}],
             'Route 8': [{'address': 'Warps_Route8', 'id': (2, 3), 'to': {'map': 'Route 8 Gate-E', 'id': (2, 3)}},
                         {'address': 'Warps_Route8', 'id': 4, 'to': {'map': 'Underground Path Route 8', 'id': 0}}],
             'Route 8-Grass': [],
             'Route 10-N': [{'address': 'Warps_Route10', 'id': 0, 'to': {'map': 'Rock Tunnel Pokemon Center', 'id': 0}},
                            {'address': 'Warps_Route10', 'id': 1, 'to': {'map': 'Rock Tunnel 1F-NE', 'id': 0}}],
             'Route 10-S': [{'address': 'Warps_Route10', 'id': 2, 'to': {'map': 'Rock Tunnel 1F-S', 'id': 2}}],
             'Route 10-P': [{'address': 'Warps_Route10', 'id': 3, 'to': {'map': 'Power Plant', 'id': 0}}],
             'Route 10-C': [],
             'Route 11': [{'address': 'Warps_Route11', 'id': 4, 'to': {'map': "Diglett's Cave Route 11", 'id': 0}}],
             'Route 11-E': [
                 {'address': 'Warps_Route11', 'id': (2, 3), 'to': {'map': 'Route 11 Gate 1F', 'id': (2, 3)}}],
             'Route 11-C': [
                 {'address': 'Warps_Route11', 'id': (0, 1), 'to': {'map': 'Route 11 Gate 1F', 'id': (0, 1)}}],
             'Route 12-L': [
                 {'address': 'Warps_Route12', 'id': (0, 1), 'to': {'map': 'Route 12 Gate 1F', 'id': (0, 1)}}],
             'Route 12-N': [{'address': 'Warps_Route12', 'id': 2, 'to': {'map': 'Route 12 Gate 1F', 'id': 2}}],
             'Route 12-S': [{'address': 'Warps_Route12', 'id': 3, 'to': {'map': 'Route 12 Super Rod House', 'id': 0}}],
             'Route 12-W': [], 'Route 12-Grass': [], 'Route 15-N': [], 'Route 15-W': [
        {'address': 'Warps_Route15', 'id': (0, 1), 'to': {'map': 'Route 15 Gate 1F', 'id': (0, 1)}}],
             'Route 15': [{'address': 'Warps_Route15', 'id': (2, 3), 'to': {'map': 'Route 15 Gate 1F', 'id': (2, 3)}}],
             'Route 16-E': [],
             'Route 16-C': [{'address': 'Warps_Route16', 'id': 2, 'to': {'map': 'Route 16 Gate 1F-E', 'id': (2, 3)}}],
             'Route 16-SW': [
                 {'address': 'Warps_Route16', 'id': (0, 1), 'to': {'map': 'Route 16 Gate 1F-W', 'id': (0, 1)}}],
             'Route 16-NW': [
                 {'address': 'Warps_Route16', 'id': (4, 5), 'to': {'map': 'Route 16 Gate 1F-N', 'id': (4, 5)}},
                 {'address': 'Warps_Route16', 'id': 8, 'to': {'map': 'Route 16 Fly House', 'id': 0}}], 'Route 16-NE': [
        {'address': 'Warps_Route16', 'id': (6, 7), 'to': {'map': 'Route 16 Gate 1F-N', 'id': (6, 7)}}], 'Route 18-W': [
        {'address': 'Warps_Route18', 'id': (0, 1), 'to': {'map': 'Route 18 Gate 1F-W', 'id': (0, 1)}}], 'Route 18-E': [
        {'address': 'Warps_Route18', 'id': (2, 3), 'to': {'map': 'Route 18 Gate 1F-E', 'id': (2, 3)}}],
             'Vermilion Pokemon Fan Club': [
                 {'address': 'Warps_PokemonFanClub', 'id': (0, 1), 'to': {'map': 'Vermilion City', 'id': 1}}],
             'Silph Co 2F-NW': [{'address': 'Warps_SilphCo2F', 'id': 3, 'to': {'map': 'Silph Co 3F', 'id': 6}}],
             'Silph Co 2F': [{'address': 'Warps_SilphCo2F', 'id': 0, 'to': {'map': 'Silph Co 1F', 'id': 2}},
                             {'address': 'Warps_SilphCo2F', 'id': 1, 'to': {'map': 'Silph Co 3F', 'id': 0}},
                             {'address': 'Warps_SilphCo2F', 'id': 2, 'to': {'map': 'Silph Co Elevator-2F', 'id': 1}},
                             {'name': 'Silph Co 2F to Silph Co 8F N', 'address': 'Warps_SilphCo2F', 'id': 4,
                              'to': {'map': 'Silph Co 8F', 'id': 4}},
                             {'name': 'Silph Co 2F to Silph Co 8F S', 'address': 'Warps_SilphCo2F', 'id': 5,
                              'to': {'map': 'Silph Co 8F', 'id': 5}}],
             'Silph Co 2F-SW': [{'address': 'Warps_SilphCo2F', 'id': 6, 'to': {'map': 'Silph Co 6F', 'id': 4}}],
             'Silph Co 3F': [{'address': 'Warps_SilphCo3F', 'id': 0, 'to': {'map': 'Silph Co 2F', 'id': 1}},
                             {'address': 'Warps_SilphCo3F', 'id': 1, 'to': {'map': 'Silph Co 4F', 'id': 0}},
                             {'address': 'Warps_SilphCo3F', 'id': 2, 'to': {'map': 'Silph Co Elevator-3F', 'id': 2}},
                             {'name': 'Silph Co 3F to Silph Co 3F N', 'address': 'Warps_SilphCo3F', 'id': 3,
                              'to': {'map': 'Silph Co 3F', 'id': 9}},
                             {'address': 'Warps_SilphCo3F', 'id': 4, 'to': {'map': 'Silph Co 5F', 'id': 5}},
                             {'address': 'Warps_SilphCo3F', 'id': 5, 'to': {'map': 'Silph Co 5F-SW', 'id': 6}},
                             {'address': 'Warps_SilphCo3F', 'id': 6, 'to': {'map': 'Silph Co 2F-NW', 'id': 3}},
                             {'name': 'Silph Co 3F to Silph Co 3F S', 'address': 'Warps_SilphCo3F', 'id': 9,
                              'to': {'map': 'Silph Co 3F', 'id': 3}}],
             'Silph Co 3F-C': [{'address': 'Warps_SilphCo3F', 'id': 8, 'to': {'map': 'Silph Co 7F-NW', 'id': 4}}],
             'Silph Co 3F-W': [{'address': 'Warps_SilphCo3F', 'id': 7, 'to': {'map': 'Silph Co 9F-NW', 'id': 3}}],
             'Silph Co 10F': [{'address': 'Warps_SilphCo10F', 'id': 0, 'to': {'map': 'Silph Co 9F', 'id': 0}},
                              {'address': 'Warps_SilphCo10F', 'id': 1, 'to': {'map': 'Silph Co 11F', 'id': 0}},
                              {'address': 'Warps_SilphCo10F', 'id': 2, 'to': {'map': 'Silph Co Elevator-10F', 'id': 9}},
                              {'address': 'Warps_SilphCo10F', 'id': 5, 'to': {'map': 'Silph Co 4F', 'id': 6}}],
             'Silph Co 10F-SE': [{'address': 'Warps_SilphCo10F', 'id': 3, 'to': {'map': 'Silph Co 4F-N', 'id': 3}},
                                 {'address': 'Warps_SilphCo10F', 'id': 4, 'to': {'map': 'Silph Co 4F', 'id': 5}}],
             "Indigo Plateau Lance's Room": [
                 {'address': 'Warps_LancesRoom', 'id': 0, 'to': {'map': "Indigo Plateau Agatha's Room", 'id': 2}},
                 {'address': 'Warps_LancesRoom', 'id': (1, 2),
                  'to': {'map': "Indigo Plateau Champion's Room", 'id': 0}}], 'Indigo Plateau Hall of Fame': [
        {'address': 'Warps_HallOfFame', 'id': 0, 'to': {'map': "Indigo Plateau Champion's Room", 'id': (2, 3)}}],
             "Player's House 2F": [
                 {'address': 'Warps_RedsHouse2F', 'id': 0, 'to': {'map': "Player's House 1F", 'id': 2}}],
             'Pewter Museum 1F': [{'address': 'Warps_Museum1F', 'id': (0, 1), 'to': {'map': 'Pewter City', 'id': 0}},
                                  {'address': 'Warps_Museum1F', 'id': 4, 'to': {'map': 'Pewter Museum 2F', 'id': 0}}],
             'Pewter Museum 1F-E': [
                 {'address': 'Warps_Museum1F', 'id': (2, 3), 'to': {'map': 'Pewter City-M', 'id': 1}}],
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
             'Silph Co 1F': [{'address': 'Warps_SilphCo1F', 'id': (0, 1), 'to': {'map': 'Saffron City-Silph', 'id': 5}},
                             {'address': 'Warps_SilphCo1F', 'id': 2, 'to': {'map': 'Silph Co 2F', 'id': 0}},
                             {'address': 'Warps_SilphCo1F', 'id': 3, 'to': {'map': 'Silph Co Elevator-1F', 'id': 0}}],
             'Saffron Pokemon Center': [
                 {'address': 'Warps_SaffronPokecenter', 'id': (0, 1), 'to': {'map': 'Saffron City', 'id': 6}}],
             'Viridian Forest North Gate': [
                 {'address': 'Warps_ViridianForestNorthGate', 'id': 1, 'to': {'map': 'Route 2-NW', 'id': 1}},
                 {'address': 'Warps_ViridianForestNorthGate', 'id': (2, 3), 'to': {'map': 'Viridian Forest', 'id': 0}}],
             'Route 2 Gate': [{'address': 'Warps_Route2Gate', 'id': 1, 'to': {'map': 'Route 2-E', 'id': 3}},
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
                  'to': {'map': 'Underground Path West East', 'id': 0}}], 'Silph Co 9F-SW': [],
             'Silph Co 9F': [{'address': 'Warps_SilphCo9F', 'id': 0, 'to': {'map': 'Silph Co 10F', 'id': 0}},
                             {'address': 'Warps_SilphCo9F', 'id': 1, 'to': {'map': 'Silph Co 8F', 'id': 0}},
                             {'address': 'Warps_SilphCo9F', 'id': 2, 'to': {'map': 'Silph Co Elevator-9F', 'id': 8}},
                             {'address': 'Warps_SilphCo9F', 'id': 4, 'to': {'map': 'Silph Co 5F', 'id': 4}}],
             'Silph Co 9F-NW': [{'address': 'Warps_SilphCo9F', 'id': 3, 'to': {'map': 'Silph Co 3F-W', 'id': 7}}],
             'Victory Road 1F-S': [
                 {'address': 'Warps_VictoryRoad1F', 'id': (0, 1), 'to': {'map': 'Route 23-C', 'id': 2}}],
             'Victory Road 1F': [
                 {'address': 'Warps_VictoryRoad1F', 'id': 2, 'to': {'map': 'Victory Road 2F-W', 'id': 0}}],
             'Pokemon Tower 1F': [
                 {'address': 'Warps_PokemonTower1F', 'id': (0, 1), 'to': {'map': 'Lavender Town', 'id': 1}},
                 {'address': 'Warps_PokemonTower1F', 'id': 2, 'to': {'map': 'Pokemon Tower 2F', 'id': 1}}],
             'Pokemon Tower 2F': [
                 {'address': 'Warps_PokemonTower2F', 'id': 0, 'to': {'map': 'Pokemon Tower 3F', 'id': 0}},
                 {'address': 'Warps_PokemonTower2F', 'id': 1, 'to': {'map': 'Pokemon Tower 1F', 'id': 2}}],
             'Pokemon Tower 3F': [
                 {'address': 'Warps_PokemonTower3F', 'id': 0, 'to': {'map': 'Pokemon Tower 2F', 'id': 0}},
                 {'address': 'Warps_PokemonTower3F', 'id': 1, 'to': {'map': 'Pokemon Tower 4F', 'id': 1}}],
             'Pokemon Tower 4F': [
                 {'address': 'Warps_PokemonTower4F', 'id': 0, 'to': {'map': 'Pokemon Tower 5F', 'id': 0}},
                 {'address': 'Warps_PokemonTower4F', 'id': 1, 'to': {'map': 'Pokemon Tower 3F', 'id': 1}}],
             'Pokemon Tower 5F': [
                 {'address': 'Warps_PokemonTower5F', 'id': 0, 'to': {'map': 'Pokemon Tower 4F', 'id': 0}},
                 {'address': 'Warps_PokemonTower5F', 'id': 1, 'to': {'map': 'Pokemon Tower 6F', 'id': 0}}],
             'Pokemon Tower 6F': [
                 {'address': 'Warps_PokemonTower6F', 'id': 0, 'to': {'map': 'Pokemon Tower 5F', 'id': 1}}],
             'Pokemon Tower 6F-S': [
                 {'address': 'Warps_PokemonTower6F', 'id': 1, 'to': {'map': 'Pokemon Tower 7F', 'id': 0}}],
             'Pokemon Tower 7F': [
                 {'address': 'Warps_PokemonTower7F', 'id': 0, 'to': {'map': 'Pokemon Tower 6F-S', 'id': 1}}],
             'Celadon Department Store 1F': [
                 {'name': 'Celadon Department Store 1F to Celadon City W', 'address': 'Warps_CeladonMart1F',
                  'id': (1, 0), 'to': {'map': 'Celadon City', 'id': 0}},
                 {'name': 'Celadon Department Store 1F to Celadon City E', 'address': 'Warps_CeladonMart1F',
                  'id': (3, 2), 'to': {'map': 'Celadon City', 'id': 1}},
                 {'address': 'Warps_CeladonMart1F', 'id': 4, 'to': {'map': 'Celadon Department Store 2F', 'id': 0}},
                 {'address': 'Warps_CeladonMart1F', 'id': 5,
                  'to': {'map': 'Celadon Department Store Elevator-1F', 'id': 0}}], 'Viridian Forest': [
        {'address': 'Warps_ViridianForest', 'id': (0, 1), 'to': {'map': 'Viridian Forest North Gate', 'id': (2, 3)}},
        {'address': 'Warps_ViridianForest', 'id': (4, 2, 5, 3), 'to': {'map': 'Viridian Forest South Gate', 'id': 1}}],
             'S.S. Anne 1F': [{'address': 'Warps_SSAnne1F', 'id': (0, 1), 'to': {'map': 'Vermilion Dock', 'id': 1}},
                              {'address': 'Warps_SSAnne1F', 'id': 2,
                               'to': {'map': 'S.S. Anne 1F Rooms-East Gentleman Room', 'id': 0}},
                              {'address': 'Warps_SSAnne1F', 'id': 3,
                               'to': {'map': 'S.S. Anne 1F Rooms-West Gentleman Room', 'id': 1}},
                              {'address': 'Warps_SSAnne1F', 'id': 4,
                               'to': {'map': 'S.S. Anne 1F Rooms-Cherry Pie Room', 'id': 2}},
                              {'address': 'Warps_SSAnne1F', 'id': 5,
                               'to': {'map': 'S.S. Anne 1F Rooms-Wigglytuff Room', 'id': 3}},
                              {'address': 'Warps_SSAnne1F', 'id': 6,
                               'to': {'map': 'S.S. Anne 1F Rooms-Youngster and Lass Room', 'id': 4}},
                              {'address': 'Warps_SSAnne1F', 'id': 7,
                               'to': {'map': 'S.S. Anne 1F Rooms-Police Room', 'id': 5}},
                              {'address': 'Warps_SSAnne1F', 'id': 8, 'to': {'map': 'S.S. Anne 2F', 'id': 6}},
                              {'address': 'Warps_SSAnne1F', 'id': 9, 'to': {'map': 'S.S. Anne B1F', 'id': 5}},
                              {'address': 'Warps_SSAnne1F', 'id': 10, 'to': {'map': 'S.S. Anne Kitchen', 'id': 0}}],
             'S.S. Anne 2F': [
                 {'address': 'Warps_SSAnne2F', 'id': 0, 'to': {'map': 'S.S. Anne 2F Rooms-Snorlax Room', 'id': 0}},
                 {'address': 'Warps_SSAnne2F', 'id': 1,
                  'to': {'map': 'S.S. Anne 2F Rooms-Fisherman and Gentleman Room', 'id': 2}},
                 {'address': 'Warps_SSAnne2F', 'id': 2, 'to': {'map': 'S.S. Anne 2F Rooms-Surf and Cut Room', 'id': 4}},
                 {'address': 'Warps_SSAnne2F', 'id': 3,
                  'to': {'map': 'S.S. Anne 2F Rooms-Gentleman and Lass Room', 'id': 6}},
                 {'address': 'Warps_SSAnne2F', 'id': 4, 'to': {'map': 'S.S. Anne 2F Rooms-Safari Zone Room', 'id': 8}},
                 {'address': 'Warps_SSAnne2F', 'id': 5, 'to': {'map': 'S.S. Anne 2F Rooms-Seasickness Room', 'id': 10}},
                 {'address': 'Warps_SSAnne2F', 'id': 6, 'to': {'map': 'S.S. Anne 1F', 'id': 8}},
                 {'address': 'Warps_SSAnne2F', 'id': 7, 'to': {'map': 'S.S. Anne 3F', 'id': 1}},
                 {'address': 'Warps_SSAnne2F', 'id': 8, 'to': {'map': "S.S. Anne Captain's Room", 'id': 0}}],
             'S.S. Anne B1F': [
                 {'address': 'Warps_SSAnneB1F', 'id': 0, 'to': {'map': 'S.S. Anne B1F Rooms-Machoke Room', 'id': 8}},
                 {'address': 'Warps_SSAnneB1F', 'id': 1,
                  'to': {'map': 'S.S. Anne B1F Rooms-Two Sailors Room', 'id': 6}},
                 {'address': 'Warps_SSAnneB1F', 'id': 2,
                  'to': {'map': 'S.S. Anne B1F Rooms-East Single Sailor Room', 'id': 4}},
                 {'address': 'Warps_SSAnneB1F', 'id': 3,
                  'to': {'map': 'S.S. Anne B1F Rooms-West Single Sailor Room', 'id': 2}},
                 {'address': 'Warps_SSAnneB1F', 'id': 4, 'to': {'map': 'S.S. Anne B1F Rooms-Fisherman Room', 'id': 0}},
                 {'address': 'Warps_SSAnneB1F', 'id': 5, 'to': {'map': 'S.S. Anne 1F', 'id': 9}}],
             'S.S. Anne Bow': [{'address': 'Warps_SSAnneBow', 'id': (0, 1), 'to': {'map': 'S.S. Anne 3F', 'id': 0}}],
             'S.S. Anne Kitchen': [
                 {'address': 'Warps_SSAnneKitchen', 'id': 0, 'to': {'map': 'S.S. Anne 1F', 'id': 10}}],
             "S.S. Anne Captain's Room": [
                 {'address': 'Warps_SSAnneCaptainsRoom', 'id': 0, 'to': {'map': 'S.S. Anne 2F', 'id': 8}}],
             'S.S. Anne 1F Rooms-West Gentleman Room': [
                 {'address': 'Warps_SSAnne1FRooms', 'id': 1, 'to': {'map': 'S.S. Anne 1F', 'id': 3}}],
             'S.S. Anne 1F Rooms-East Gentleman Room': [
                 {'address': 'Warps_SSAnne1FRooms', 'id': 0, 'to': {'map': 'S.S. Anne 1F', 'id': 2}}],
             'S.S. Anne 1F Rooms-Police Room': [
                 {'address': 'Warps_SSAnne1FRooms', 'id': 5, 'to': {'map': 'S.S. Anne 1F', 'id': 7}}],
             'S.S. Anne 1F Rooms-Youngster and Lass Room': [
                 {'address': 'Warps_SSAnne1FRooms', 'id': 4, 'to': {'map': 'S.S. Anne 1F', 'id': 6}}],
             'S.S. Anne 1F Rooms-Wigglytuff Room': [
                 {'address': 'Warps_SSAnne1FRooms', 'id': 3, 'to': {'map': 'S.S. Anne 1F', 'id': 5}}],
             'S.S. Anne 1F Rooms-Cherry Pie Room': [
                 {'address': 'Warps_SSAnne1FRooms', 'id': 2, 'to': {'map': 'S.S. Anne 1F', 'id': 4}}],
             'S.S. Anne 2F Rooms-Snorlax Room': [
                 {'address': 'Warps_SSAnne2FRooms', 'id': (0, 1), 'to': {'map': 'S.S. Anne 2F', 'id': 0}}],
             'S.S. Anne 2F Rooms-Fisherman and Gentleman Room': [
                 {'address': 'Warps_SSAnne2FRooms', 'id': (2, 3), 'to': {'map': 'S.S. Anne 2F', 'id': 1}}],
             'S.S. Anne 2F Rooms-Surf and Cut Room': [
                 {'address': 'Warps_SSAnne2FRooms', 'id': (4, 5), 'to': {'map': 'S.S. Anne 2F', 'id': 2}}],
             'S.S. Anne 2F Rooms-Gentleman and Lass Room': [
                 {'address': 'Warps_SSAnne2FRooms', 'id': (6, 7), 'to': {'map': 'S.S. Anne 2F', 'id': 3}}],
             'S.S. Anne 2F Rooms-Safari Zone Room': [
                 {'address': 'Warps_SSAnne2FRooms', 'id': (8, 9), 'to': {'map': 'S.S. Anne 2F', 'id': 4}}],
             'S.S. Anne 2F Rooms-Seasickness Room': [
                 {'address': 'Warps_SSAnne2FRooms', 'id': (10, 11), 'to': {'map': 'S.S. Anne 2F', 'id': 5}}],
             'S.S. Anne B1F Rooms-Fisherman Room': [
                 {'address': 'Warps_SSAnneB1FRooms', 'id': (0, 1), 'to': {'map': 'S.S. Anne B1F', 'id': 4}}],
             'S.S. Anne B1F Rooms-West Single Sailor Room': [
                 {'address': 'Warps_SSAnneB1FRooms', 'id': (2, 3), 'to': {'map': 'S.S. Anne B1F', 'id': 3}}],
             'S.S. Anne B1F Rooms-East Single Sailor Room': [
                 {'address': 'Warps_SSAnneB1FRooms', 'id': (4, 5), 'to': {'map': 'S.S. Anne B1F', 'id': 2}}],
             'S.S. Anne B1F Rooms-Two Sailors Room': [
                 {'address': 'Warps_SSAnneB1FRooms', 'id': (6, 7), 'to': {'map': 'S.S. Anne B1F', 'id': 1}}],
             'S.S. Anne B1F Rooms-Machoke Room': [
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
                              {'address': 'Warps_SilphCo11F', 'id': 1,
                               'to': {'map': 'Silph Co Elevator-11F', 'id': 10}}],
             'Silph Co 11F-W': [{'address': 'Warps_SilphCo11F', 'id': 3, 'to': {'map': 'Silph Co 7F-NW', 'id': 3}}],
             'Viridian Gym': [
                 {'address': 'Warps_ViridianGym', 'id': (0, 1), 'to': {'map': 'Viridian City-G', 'id': 4}}],
             'Pewter Pokemart': [{'address': 'Warps_PewterMart', 'id': (0, 1), 'to': {'map': 'Pewter City', 'id': 4}}],
             'Cerulean Cave 1F-SE': [
                 {'address': 'Warps_CeruleanCave1F', 'id': (0, 1), 'to': {'map': 'Cerulean City-Cave', 'id': 6}},
                 {'address': 'Warps_CeruleanCave1F', 'id': 3, 'to': {'map': 'Cerulean Cave 2F-E', 'id': 1}}],
             'Cerulean Cave 1F-NE': [
                 {'address': 'Warps_CeruleanCave1F', 'id': 2, 'to': {'map': 'Cerulean Cave 2F-E', 'id': 0}}],
             'Cerulean Cave 1F-N': [
                 {'address': 'Warps_CeruleanCave1F', 'id': 5, 'to': {'map': 'Cerulean Cave 2F-N', 'id': 3}}],
             'Cerulean Cave 1F-SW': [
                 {'address': 'Warps_CeruleanCave1F', 'id': 4, 'to': {'map': 'Cerulean Cave 2F-N', 'id': 2}},
                 {'address': 'Warps_CeruleanCave1F', 'id': 7, 'to': {'map': 'Cerulean Cave 2F-W', 'id': 5}}],
             'Cerulean Cave 1F-NW': [
                 {'address': 'Warps_CeruleanCave1F', 'id': 6, 'to': {'map': 'Cerulean Cave 2F-W', 'id': 4}},
                 {'address': 'Warps_CeruleanCave1F', 'id': 8, 'to': {'map': 'Cerulean Cave B1F', 'id': 0}}],
             'Cerulean Cave 1F-Wild': [], 'Cerulean Cave 1F-Water': [], 'Cerulean Badge House': [
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
             'Safari Zone Gate-N': [{'address': 'Warps_SafariZoneGate', 'id': (2, 3),
                                     'to': {'map': 'Safari Zone Center-S', 'id': (0, 1)}}],
             'Fuchsia Gym': [{'address': 'Warps_FuchsiaGym', 'id': (0, 1), 'to': {'map': 'Fuchsia City', 'id': 5}}],
             'Fuchsia Meeting Room': [
                 {'address': 'Warps_FuchsiaMeetingRoom', 'id': (0, 1), 'to': {'map': 'Fuchsia City', 'id': 6}}],
             'Cinnabar Gym': [
                 {'address': 'Warps_CinnabarGym', 'id': (0, 1), 'to': {'map': 'Cinnabar Island-G', 'id': 1}}],
             'Cinnabar Lab': [{'address': 'Warps_CinnabarLab', 'id': (0, 1), 'to': {'map': 'Cinnabar Island', 'id': 2}},
                              {'address': 'Warps_CinnabarLab', 'id': 2,
                               'to': {'map': 'Cinnabar Lab Trade Room', 'id': 0}},
                              {'address': 'Warps_CinnabarLab', 'id': 3,
                               'to': {'map': 'Cinnabar Lab R&D Room', 'id': 0}},
                              {'address': 'Warps_CinnabarLab', 'id': 4,
                               'to': {'map': 'Cinnabar Lab Fossil Room', 'id': 0}}], 'Cinnabar Lab Trade Room': [
        {'address': 'Warps_CinnabarLabTradeRoom', 'id': (0, 1), 'to': {'map': 'Cinnabar Lab', 'id': 2}}],
             'Cinnabar Lab R&D Room': [
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
             "Indigo Plateau Champion's Room": [{'address': 'Warps_ChampionsRoom', 'id': (0, 1),
                                                 'to': {'map': "Indigo Plateau Lance's Room", 'id': (1, 2)}},
                                                {'address': 'Warps_ChampionsRoom', 'id': (2, 3),
                                                 'to': {'map': 'Indigo Plateau Hall of Fame', 'id': 0}}],
             "Indigo Plateau Lorelei's Room": [
                 {'address': 'Warps_LoreleisRoom', 'id': (0, 1), 'to': {'map': 'Indigo Plateau Lobby-N', 'id': 2}},
                 {'address': 'Warps_LoreleisRoom', 'id': (2, 3),
                  'to': {'map': "Indigo Plateau Bruno's Room", 'id': (0, 1)}}], "Indigo Plateau Bruno's Room": [
        {'address': 'Warps_BrunosRoom', 'id': (0, 1), 'to': {'map': "Indigo Plateau Lorelei's Room", 'id': (2, 3)}},
        {'address': 'Warps_BrunosRoom', 'id': (2, 3), 'to': {'map': "Indigo Plateau Agatha's Room", 'id': (0, 1)}}],
             "Indigo Plateau Agatha's Room": [{'address': 'Warps_AgathasRoom', 'id': (0, 1),
                                               'to': {'map': "Indigo Plateau Bruno's Room", 'id': (2, 3)}},
                                              {'address': 'Warps_AgathasRoom', 'id': (2, 3),
                                               'to': {'map': "Indigo Plateau Lance's Room", 'id': 0}}]}


silph_co_warps = [
    'Silph Co 4F to Silph Co 10F-SE', 'Silph Co 4F to Silph Co 10F', 'Silph Co 4F-N to Silph Co 6F',
    'Silph Co 4F-N to Silph Co 10F-SE', 'Silph Co 5F to Silph Co 7F-SE', 'Silph Co 5F to Silph Co 9F',
    'Silph Co 5F to Silph Co 3F', 'Silph Co 5F-SW to Silph Co 3F', 'Silph Co 6F to Silph Co 4F-N',
    'Silph Co 6F to Silph Co 2F-SW', 'Silph Co 7F-NW to Silph Co 3F-C', 'Silph Co 7F-NW to Silph Co 11F-W',
    'Silph Co 7F-SE to Silph Co 5F', 'Silph Co 8F to Silph Co 2F S', 'Silph Co 8F to Silph Co 2F N',
    'Silph Co 8F to Silph Co 8F-W', 'Silph Co 8F-W to Silph Co 8F', 'Silph Co 2F-NW to Silph Co 3F',
    'Silph Co 2F to Silph Co 8F N', 'Silph Co 2F to Silph Co 8F S', 'Silph Co 2F-SW to Silph Co 6F',
    'Silph Co 3F to Silph Co 3F N', 'Silph Co 3F to Silph Co 5F', 'Silph Co 3F to Silph Co 5F-SW',
    'Silph Co 3F to Silph Co 2F-NW', 'Silph Co 3F to Silph Co 3F S', 'Silph Co 3F-C to Silph Co 7F-NW',
    'Silph Co 3F-W to Silph Co 9F-NW', 'Silph Co 10F to Silph Co 4F', 'Silph Co 10F-SE to Silph Co 4F-N',
    'Silph Co 10F-SE to Silph Co 4F', 'Silph Co 9F to Silph Co 5F', 'Silph Co 9F-NW to Silph Co 3F-W',
    'Silph Co 11F-W to Silph Co 7F-NW'
]

saffron_gym_warps = [
    'Saffron Gym-NW to Saffron Gym-NE', 'Saffron Gym-NW to Saffron Gym-N', 'Saffron Gym-NW to Saffron Gym-C',
    'Saffron Gym-NW to Saffron Gym-W', 'Saffron Gym-W to Saffron Gym-E', 'Saffron Gym-W to Saffron Gym-N',
    'Saffron Gym-W to Saffron Gym-NW', 'Saffron Gym-W to Saffron Gym-SW', 'Saffron Gym-SW to Saffron Gym-NE',
    'Saffron Gym-SW to Saffron Gym-SE', 'Saffron Gym-SW to Saffron Gym-N', 'Saffron Gym-SW to Saffron Gym-W',
    'Saffron Gym-N to Saffron Gym-E', 'Saffron Gym-N to Saffron Gym-NW', 'Saffron Gym-N to Saffron Gym-W',
    'Saffron Gym-N to Saffron Gym-SW', 'Saffron Gym-C to Saffron Gym-NW', 'Saffron Gym-S to Saffron Gym-SE',
    'Saffron Gym-NE to Saffron Gym-E', 'Saffron Gym-NE to Saffron Gym-SE', 'Saffron Gym-NE to Saffron Gym-NW',
    'Saffron Gym-NE to Saffron Gym-SW', 'Saffron Gym-E to Saffron Gym-NE', 'Saffron Gym-E to Saffron Gym-SE',
    'Saffron Gym-E to Saffron Gym-N', 'Saffron Gym-E to Saffron Gym-W', 'Saffron Gym-SE to Saffron Gym-NE',
    'Saffron Gym-SE to Saffron Gym-E', 'Saffron Gym-SE to Saffron Gym-SW', 'Saffron Gym-SE to Saffron Gym-S'
]

entrance_only = [
    "Route 4-W to Mt Moon 1F", "Saffron City-G to Saffron Gym-S", "Saffron City-Copycat to Saffron Copycat's House 1F",
    "Saffron City-Pidgey to Saffron Pidgey House", "Celadon Game Corner-Hidden Stairs to Rocket Hideout B1F"
    "Cinnabar Island-M to Pokemon Mansion 1F", "Mt Moon B2F to Mt Moon B1F-W", "Silph Co 7F-NW to Silph Co 11F-W",
    "Viridian City-G", "Cerulean City-Cave to Cerulean Cave 1F-SE", "Cerulean City-T to Cerulean Trashed House",
    "Route 10-P to Power Plant", "S.S. Anne 2F to S.S. Anne Captain's Room", "Pewter City-M to Pewter Museum 1F-E",
    "Pokemon Mansion 1F-SE to Cinnabar Island-M", "Cinnabar Island-G to Cinnabar Gym",
    "Saffron City-Silph to Silph Co 1F",
]

pokemon_center_entrances = ['Viridian City to Viridian Pokemon Center', 'Celadon City to Celadon Pokemon Center',
                            'Route 4-W to Route 4 Pokemon Center', 'Route 10-N to Rock Tunnel Pokemon Center',
                            'Pewter City to Pewter Pokemon Center', 'Cerulean City to Cerulean Pokemon Center',
                            'Lavender Town to Lavender Pokemon Center', 'Vermilion City to Vermilion Pokemon Center',
                            'Saffron City to Saffron Pokemon Center', 'Fuchsia City to Fuchsia Pokemon Center',
                            'Cinnabar Island to Cinnabar Pokemon Center', 'Indigo Plateau to Indigo Plateau Lobby']
pokemon_centers = ['Celadon Pokemon Center to Celadon City', 'Viridian Pokemon Center to Viridian City',
                   'Pewter Pokemon Center to Pewter City', 'Cerulean Pokemon Center to Cerulean City',
                   'Vermilion Pokemon Center to Vermilion City', 'Fuchsia Pokemon Center to Fuchsia City',
                   'Cinnabar Pokemon Center to Cinnabar Island', 'Lavender Pokemon Center to Lavender Town',
                   'Saffron Pokemon Center to Saffron City', 'Route 4 Pokemon Center to Route 4-W',
                   'Rock Tunnel Pokemon Center to Route 10-N', 'Indigo Plateau Lobby to Indigo Plateau']

pokemart_entrances = ['Viridian City to Viridian Pokemart', 'Pewter City to Pewter Pokemart',
                      'Cerulean City to Cerulean Pokemart', 'Lavender Town to Lavender Pokemart',
                      'Vermilion City to Vermilion Pokemart', 'Saffron City to Saffron Pokemart',
                      'Fuchsia City to Fuchsia Pokemart', 'Cinnabar Island to Cinnabar Pokemart']

pokemarts = ['Viridian Pokemart to Viridian City', 'Pewter Pokemart to Pewter City',
             'Cerulean Pokemart to Cerulean City', 'Lavender Pokemart to Lavender Town',
             'Vermilion Pokemart to Vermilion City', 'Saffron Pokemart to Saffron City',
             'Fuchsia Pokemart to Fuchsia City', 'Cinnabar Pokemart to Cinnabar Island']


safe_rooms = ["Rival's House to Pallet Town",
              'Vermilion Trade House to Vermilion City',
              'Viridian School House to Viridian City', 'Viridian Nickname House to Viridian City',
              'Pewter Nidoran House to Pewter City', 'Pewter Speech House to Pewter City',
              'Cerulean Trade House to Cerulean City', 'Cerulean Bicycle Shop to Cerulean City',
              "Lavender Mr. Fuji's House to Lavender Town", 'Lavender Cubone House to Lavender Town',
              "Lavender Name Rater's House to Lavender Town", 'Vermilion Pidgey House to Vermilion City',
              'Saffron Pidgey House to Saffron City-Pidgey', "Saffron Mr. Psychic's House to Saffron City",
              'Route 2 Trade House to Route 2-NE', 'Route 16 Fly House to Route 16-NW', "Bill's House to Route 25",
              'Safari Zone Center Rest House to Safari Zone Center-S',
              'Safari Zone West Rest House to Safari Zone West', 'Safari Zone East Rest House to Safari Zone East',
              'Safari Zone North Rest House to Safari Zone North',
              'Celadon Prize Corner to Celadon City', 'Celadon Diner to Celadon City',
              'Celadon Chief House to Celadon City', 'Celadon Hotel to Celadon City',
              'Safari Zone Secret House to Safari Zone West-NW',
              'Vermilion Old Rod House to Vermilion City', 'Daycare to Route 5',
              'Route 12 Super Rod House to Route 12-S', 'Vermilion Pokemon Fan Club to Vermilion City',
              "Fuchsia Bill's Grandpa's House to Fuchsia City", "Fuchsia Warden's House to Fuchsia City",
              'Fuchsia Meeting Room to Fuchsia City',]

insanity_safe_rooms = [
    'Cinnabar Lab Trade Room to Cinnabar Lab',
    'Cinnabar Lab R&D Room to Cinnabar Lab', 'Cinnabar Lab Fossil Room to Cinnabar Lab',
    'Celadon Mansion Roof House to Celadon Mansion Roof-Back',
    "Saffron Copycat's House 2F to Saffron Copycat's House 1F",
    'Route 11 Gate 2F to Route 11 Gate 1F', 'Route 12 Gate 2F to Route 12 Gate 1F',
    'Route 15 Gate 2F to Route 15 Gate 1F', 'Route 16 Gate 2F to Route 16 Gate 1F-E',
    'Route 18 Gate 2F to Route 18 Gate 1F-E',
    'Celadon Department Store Roof to Celadon Department Store 5F',
    'Pewter Museum 2F to Pewter Museum 1F',
    "Cerulean City-Badge House Backyard to Cerulean Badge House",
    'Fuchsia City-Good Rod House Backyard to Fuchsia Good Rod House',
    'S.S. Anne Kitchen to S.S. Anne 1F', "S.S. Anne Captain's Room to S.S. Anne 2F",
    'S.S. Anne 1F Rooms-Police Room to S.S. Anne 1F',
    'S.S. Anne 1F Rooms-Wigglytuff Room to S.S. Anne 1F',
    'S.S. Anne 1F Rooms-Cherry Pie Room to S.S. Anne 1F',
    'S.S. Anne 2F Rooms-Snorlax Room to S.S. Anne 2F',
    'S.S. Anne 2F Rooms-Surf and Cut Room to S.S. Anne 2F',
    'S.S. Anne 2F Rooms-Safari Zone Room to S.S. Anne 2F',
    'S.S. Anne 2F Rooms-Seasickness Room to S.S. Anne 2F',
    'S.S. Anne B1F Rooms-Machoke Room to S.S. Anne B1F',
]


def pair(a, b):
    return (f"{a} to {b}", f"{b} to {a}")


mandatory_connections = {
    pair("Safari Zone Center-S", "Safari Zone Gate-N"),
    pair("Safari Zone East", "Safari Zone North"),
    pair("Safari Zone East", "Safari Zone Center-S"),
    pair("Safari Zone North", "Safari Zone Center-NE"),
    pair("Safari Zone North", "Safari Zone West"),
    pair("Safari Zone North", "Safari Zone West-NW"),
    pair("Safari Zone West", "Safari Zone Center-NW"),
}
insanity_mandatory_connections = {
    # pair("Seafoam Islands B1F-NE", "Seafoam Islands 1F"),
    # pair("Seafoam Islands 1F", "Seafoam Islands B1F"),
    # pair("Seafoam Islands B2F-NW", "Seafoam Islands B1F"),
    # pair("Seafoam Islands B3F-SE", "Seafoam Islands B2F-SE"),
    # pair("Seafoam Islands B3F-NE", "Seafoam Islands B2F-NE"),
    # pair("Seafoam Islands B4F", "Seafoam Islands B3F-NE"),
    # pair("Seafoam Islands B4F", "Seafoam Islands B3F"),
    pair("Player's House 1F", "Player's House 2F"),
    pair("Indigo Plateau Lorelei's Room", "Indigo Plateau Lobby-N"),
    pair("Indigo Plateau Bruno's Room", "Indigo Plateau Lorelei's Room"),
    pair("Indigo Plateau Bruno's Room", "Indigo Plateau Agatha's Room"),
    pair("Indigo Plateau Agatha's Room", "Indigo Plateau Lance's Room"),
    pair("Indigo Plateau Champion's Room", "Indigo Plateau Lance's Room"),
    pair("Indigo Plateau Hall of Fame", "Indigo Plateau Champion's Room")
}

simple_mandatory_connections = {
    pair("Fuchsia City", "Safari Zone Gate-S")

}

safari_zone_houses = ["Safari Zone Center-S to Safari Zone Center Rest House",
                      "Safari Zone West to Safari Zone West Rest House",
                      "Safari Zone West-NW to Safari Zone Secret House",
                      "Safari Zone East to Safari Zone East Rest House",
                      "Safari Zone North to Safari Zone North Rest House"]

safe_connecting_interior_dungeons = [
    ["Viridian Forest South Gate to Route 2-SW", "Viridian Forest North Gate to Route 2-NW"],
    ["Diglett's Cave Route 2 to Route 2-NE", "Diglett's Cave Route 11 to Route 11"],
    ["Mt Moon 1F to Route 4-W", "Mt Moon B1F-NE to Route 4-C"],
]

unsafe_connecting_interior_dungeons = [
    ["Seafoam Islands 1F to Route 20-IE", "Seafoam Islands 1F-SE to Route 20-IW"],
    ["Rock Tunnel 1F-NE to Route 10-N", "Rock Tunnel 1F-S to Route 10-S"],
    ["Victory Road 1F-S to Route 23-C", "Victory Road 2F-E to Route 23-N"],
]

multi_purpose_dungeons = [
    ["Pokemon Mansion 1F to Cinnabar Island-M", "Pokemon Mansion 1F-SE to Cinnabar Island-M"],
    ["Power Plant to Route 10-P", "Power Plant to Route 10-P Back Door"]
]

multi_purpose_dungeon_entrances = [
    'Cinnabar Island-M to Pokemon Mansion 1F',
    'Route 10-P to Power Plant'
]

connecting_interior_dungeon_entrances = [
    ['Route 2-SW to Viridian Forest South Gate', 'Route 2-NW to Viridian Forest North Gate'],
    ["Route 2-NE to Diglett's Cave Route 2", "Route 11 to Diglett's Cave Route 11"],
    ['Route 20-IE to Seafoam Islands 1F', 'Route 20-IW to Seafoam Islands 1F-SE'],
    ['Route 4-W to Mt Moon 1F', 'Route 4-C to Mt Moon B1F-NE'],
    ['Route 10-N to Rock Tunnel 1F-NE', 'Route 10-S to Rock Tunnel 1F-S'],
    ['Route 23-C to Victory Road 1F-S', 'Route 23-N to Victory Road 2F-E'],
]


connecting_interiors = [
    ["Underground Path Route 5 to Route 5", "Underground Path Route 6 to Route 6"],
    ["Underground Path Route 7 to Route 7", "Underground Path Route 8 to Route 8"],
    ["Celadon Department Store 1F to Celadon City W", "Celadon Department Store 1F to Celadon City E"],
    ["Route 2 Gate to Route 2-E", "Route 2 Gate to Route 2-SE"],
    ["Cerulean Badge House to Cerulean City-Badge House Backyard", "Cerulean Badge House to Cerulean City"],
    ["Cerulean Trashed House to Cerulean City-T", "Cerulean Trashed House to Cerulean City-Outskirts"],
    ["Fuchsia Good Rod House to Fuchsia City", "Fuchsia Good Rod House to Fuchsia City-Good Rod House Backyard"],
    ["Route 11 Gate 1F to Route 11-E", "Route 11 Gate 1F to Route 11-C"],
    ["Route 12 Gate 1F to Route 12-N", "Route 12 Gate 1F to Route 12-L"],
    ["Route 15 Gate 1F to Route 15", "Route 15 Gate 1F to Route 15-W"],
    ["Route 16 Gate 1F-N to Route 16-NE", "Route 16 Gate 1F-N to Route 16-NW"],
    ["Route 16 Gate 1F-W to Route 16-SW", "Route 16 Gate 1F-E to Route 16-C"],
    ["Route 18 Gate 1F-W to Route 18-W", "Route 18 Gate 1F-E to Route 18-E"],
    ["Route 5 Gate-N to Route 5", "Route 5 Gate-S to Route 5-S"],
    ["Route 6 Gate-S to Route 6", "Route 6 Gate-N to Route 6-N"],
    ["Route 7 Gate-W to Route 7", "Route 7 Gate-E to Route 7-E"],
    ["Route 8 Gate-E to Route 8", "Route 8 Gate-W to Route 8-W"],
    ["Route 22 Gate-S to Route 22", "Route 22 Gate-N to Route 23-S"],

]

connecting_interior_entrances = [
    ['Route 5 to Underground Path Route 5', 'Route 6 to Underground Path Route 6'],
    ['Route 7 to Underground Path Route 7', 'Route 8 to Underground Path Route 8'],
    ["Celadon City to Celadon Department Store 1F W", "Celadon City to Celadon Department Store 1F E"],
    ['Route 2-E to Route 2 Gate', 'Route 2-SE to Route 2 Gate'],
    ['Cerulean City-Badge House Backyard to Cerulean Badge House',
     'Cerulean City to Cerulean Badge House'],
    ['Cerulean City-T to Cerulean Trashed House',
     'Cerulean City-Outskirts to Cerulean Trashed House'],
    ['Fuchsia City to Fuchsia Good Rod House',
     'Fuchsia City-Good Rod House Backyard to Fuchsia Good Rod House'],
    ['Route 11-E to Route 11 Gate 1F', 'Route 11-C to Route 11 Gate 1F'],
    ['Route 12-N to Route 12 Gate 1F', 'Route 12-L to Route 12 Gate 1F'],
    ['Route 15 to Route 15 Gate 1F', 'Route 15-W to Route 15 Gate 1F'],
    ['Route 16-NE to Route 16 Gate 1F-N', 'Route 16-NW to Route 16 Gate 1F-N'],
    ['Route 16-SW to Route 16 Gate 1F-W', 'Route 16-C to Route 16 Gate 1F-E'],
    ['Route 18-W to Route 18 Gate 1F-W', 'Route 18-E to Route 18 Gate 1F-E'],
    ['Route 5 to Route 5 Gate-N', 'Route 5-S to Route 5 Gate-S'],
    ['Route 6 to Route 6 Gate-S', 'Route 6-N to Route 6 Gate-N'],
    ['Route 7 to Route 7 Gate-W', 'Route 7-E to Route 7 Gate-E'],
    ['Route 8 to Route 8 Gate-E', 'Route 8-W to Route 8 Gate-W'],
    ['Route 22 to Route 22 Gate-S', 'Route 23-S to Route 22 Gate-N']
]

dungeons = [
    "Silph Co 1F to Saffron City-Silph",
    "Rocket Hideout B1F to Celadon Game Corner-Hidden Stairs",
    "Cerulean Cave 1F-SE to Cerulean City-Cave",
    "Vermilion Dock to Vermilion City-Dock",
    "Pokemon Tower 1F to Lavender Town"
]

dungeon_entrances = [
    'Saffron City-Silph to Silph Co 1F', 'Celadon Game Corner-Hidden Stairs to Rocket Hideout B1F',
    'Cerulean City-Cave to Cerulean Cave 1F-SE', 'Vermilion City-Dock to Vermilion Dock',
    'Lavender Town to Pokemon Tower 1F'
]

gyms = [
    "Pewter Gym to Pewter City", "Cerulean Gym to Cerulean City", "Vermilion Gym to Vermilion City-G",
    "Celadon Gym to Celadon City-G", "Fuchsia Gym to Fuchsia City", "Saffron Gym-S to Saffron City-G",
    "Cinnabar Gym to Cinnabar Island-G", "Viridian Gym to Viridian City-G"
]

gym_entrances = [
    'Pewter City to Pewter Gym', 'Cerulean City to Cerulean Gym', 'Vermilion City-G to Vermilion Gym',
    'Celadon City-G to Celadon Gym', 'Fuchsia City to Fuchsia Gym', 'Saffron City-G to Saffron Gym-S',
    'Cinnabar Island-G to Cinnabar Gym', 'Viridian City-G to Viridian Gym'
]

initial_doors = [
    "Viridian City to Viridian Pokemart",
    "Viridian City to Viridian Nickname House",
    "Viridian City to Viridian School House",
    "Route 22 to Route 22 Gate-S"
]

mansion_dead_ends = [
    "Pokemon Mansion 2F-E to Pokemon Mansion 3F-SE",
    "Pokemon Mansion 3F-SW to Pokemon Mansion 2F",
]

mansion_stair_destinations = [
    "Pokemon Mansion 2F to Pokemon Mansion 1F",
    "Pokemon Mansion 2F to Pokemon Mansion 3F-SW",
    "Pokemon Mansion 3F to Pokemon Mansion 2F",
    "Pokemon Mansion 1F to Pokemon Mansion 2F"
]

unreachable_outdoor_entrances = [
    "Route 4-C to Mt Moon B1F-NE",
    "Fuchsia City-Good Rod House Backyard to Fuchsia Good Rod House",
    "Cerulean City-Badge House Backyard to Cerulean Badge House",
    # TODO: This doesn't need to be forced if fly location is Pokemon League?
    "Route 23-N to Victory Road 2F-E"
]


def create_region(multiworld: MultiWorld, player: int, name: str, locations_per_region=None, exits=None):
    ret = PokemonRBRegion(name, player, multiworld)
    for location in locations_per_region.get(name, []):
        location.parent_region = ret
        ret.locations.append(location)
        if multiworld.randomize_hidden_items[player] == "exclude" and "Hidden" in location.name:
            location.progress_type = LocationProgressType.EXCLUDED
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, exit, ret))
    locations_per_region[name] = []
    return ret


def outdoor_map(name):
    i = map_ids[name.split("-")[0]]
    if i <= 0x24 or 0xD9 <= i <= 0xDC:
        return True
    return False


def create_regions(self):
    multiworld = self.multiworld
    player = self.player
    locations_per_region = {}

    start_inventory = self.multiworld.start_inventory[self.player].value.copy()
    if self.multiworld.randomize_pokedex[self.player] == "start_with":
        start_inventory["Pokedex"] = 1
        self.multiworld.push_precollected(self.create_item("Pokedex"))
    if self.multiworld.exp_all[self.player] == "start_with":
        start_inventory["Exp. All"] = 1
        self.multiworld.push_precollected(self.create_item("Exp. All"))

    # locations = [location for location in location_data if location.type in ("Item", "Trainer Parties")]
    self.item_pool = []
    combined_traps = (self.multiworld.poison_trap_weight[self.player].value
                      + self.multiworld.fire_trap_weight[self.player].value
                      + self.multiworld.paralyze_trap_weight[self.player].value
                      + self.multiworld.ice_trap_weight[self.player].value)
    stones = ["Moon Stone", "Fire Stone", "Water Stone", "Thunder Stone", "Leaf Stone"]

    for location in location_data:
        locations_per_region.setdefault(location.region, [])
        # The check for list is so that we don't try to check the item table with a list as a key
        if location.inclusion(multiworld, player) and (isinstance(location.original_item, list) or
                not (self.multiworld.key_items_only[self.player] and item_table[location.original_item].classification
                not in (ItemClassification.progression, ItemClassification.progression_skip_balancing) and not
                location.event)):
            location_object = PokemonRBLocation(player, location.name, location.address, location.rom_address,
                                                location.type, location.level, location.level_address)
            locations_per_region[location.region].append(location_object)

            if location.type in ("Item", "Trainer Parties"):
                event = location.event

                if location.original_item is None:
                    item = self.create_filler()
                elif location.original_item == "Exp. All" and self.multiworld.exp_all[self.player] == "remove":
                    item = self.create_filler()
                elif location.original_item == "Pokedex":
                    if self.multiworld.randomize_pokedex[self.player] == "vanilla":
                        location_object.event = True
                        event = True
                    item = self.create_item("Pokedex")
                elif location.original_item == "Moon Stone" and self.multiworld.stonesanity[self.player]:
                    stone = stones.pop()
                    item = self.create_item(stone)
                elif location.original_item.startswith("TM"):
                    if self.multiworld.randomize_tm_moves[self.player]:
                        item = self.create_item(location.original_item.split(" ")[0])
                    else:
                        item = self.create_item(location.original_item)
                elif location.original_item == "Card Key" and self.multiworld.split_card_key[self.player] == "on":
                    item = self.create_item("Card Key 3F")
                elif "Card Key" in location.original_item and self.multiworld.split_card_key[self.player] == "progressive":
                    item = self.create_item("Progressive Card Key")
                else:
                    item = self.create_item(location.original_item)
                    if (item.classification == ItemClassification.filler and self.multiworld.random.randint(1, 100)
                            <= self.multiworld.trap_percentage[self.player].value and combined_traps != 0):
                        item = self.create_item(self.select_trap())

                if self.multiworld.key_items_only[self.player] and (not location.event) and (not item.advancement):
                    continue

                if item.name in start_inventory and start_inventory[item.name] > 0 and \
                        location.original_item in item_groups["Unique"]:
                    start_inventory[location.original_item] -= 1
                    item = self.create_filler()

                if event:
                    location_object.place_locked_item(item)
                    if location.type == "Trainer Parties":
                        # loc.item.classification = ItemClassification.filler
                        location_object.party_data = deepcopy(location.party_data)
                else:
                    self.item_pool.append(item)

    self.multiworld.random.shuffle(self.item_pool)
    advancement_items = [item.name for item in self.item_pool if item.advancement] \
                        + [item.name for item in self.multiworld.precollected_items[self.player] if
                           item.advancement]
    self.total_key_items = len(
        # The stonesanity items are not checekd for here and instead just always added as the `+ 4`
        # They will always exist, but if stonesanity is off, then only as events.
        # We don't want to just add 4 if stonesanity is off while still putting them in this list in case
        # the player puts stones in their start inventory, in which case they would be double-counted here.
        [item for item in ["Bicycle", "Silph Scope", "Item Finder", "Super Rod", "Good Rod",
                           "Old Rod", "Lift Key", "Card Key", "Town Map", "Coin Case", "S.S. Ticket",
                           "Secret Key", "Poke Flute", "Mansion Key", "Safari Pass", "Plant Key",
                           "Hideout Key", "Card Key 2F", "Card Key 3F", "Card Key 4F", "Card Key 5F",
                           "Card Key 6F", "Card Key 7F", "Card Key 8F", "Card Key 9F", "Card Key 10F",
                           "Card Key 11F", "Exp. All", "Moon Stone"] if item in advancement_items]) + 4
    if "Progressive Card Key" in advancement_items:
        self.total_key_items += 10

    self.multiworld.cerulean_cave_key_items_condition[self.player].total = \
        int((self.total_key_items / 100) * self.multiworld.cerulean_cave_key_items_condition[self.player].value)

    self.multiworld.elite_four_key_items_condition[self.player].total = \
        int((self.total_key_items / 100) * self.multiworld.elite_four_key_items_condition[self.player].value)

    regions = [create_region(multiworld, player, region, locations_per_region) for region in warp_data]
    multiworld.regions += regions
    if __debug__:
        for region in locations_per_region:
            assert not locations_per_region[region], f"locations not assigned to region {region}"

    connect(multiworld, player, "Menu", "Pallet Town", one_way=True)
    connect(multiworld, player, "Menu", "Pokedex", one_way=True)
    connect(multiworld, player, "Menu", "Evolution", one_way=True)
    connect(multiworld, player, "Menu", "Fossil", lambda state: logic.fossil_checks(state,
        state.multiworld.second_fossil_check_condition[player].value, player), one_way=True)
    connect(multiworld, player, "Pallet Town", "Route 1")
    connect(multiworld, player, "Route 1", "Viridian City")
    connect(multiworld, player, "Viridian City", "Route 22")
    connect(multiworld, player, "Route 22", "Route 22-F", lambda state: state.has("Defeat Viridian Gym Giovanni", player), one_way=True)
    connect(multiworld, player, "Route 2-SW", "Route 2-Grass", one_way=True)
    connect(multiworld, player, "Route 2-NW", "Route 2-Grass", one_way=True)
    connect(multiworld, player, "Route 22 Gate-S", "Route 22 Gate-N",
            lambda state: logic.has_badges(state, state.multiworld.route_22_gate_condition[player].value, player))
    connect(multiworld, player, "Route 23-Grass", "Route 23-C", lambda state: logic.has_badges(state, state.multiworld.victory_road_condition[player].value, player))
    connect(multiworld, player, "Route 23-Grass", "Route 23-S", lambda state: logic.can_surf(state, player))
    connect(multiworld, player, "Viridian City-N", "Viridian City-G", lambda state:
                     logic.has_badges(state, state.multiworld.viridian_gym_condition[player].value, player))
    connect(multiworld, player, "Route 2-SW", "Route 2-SE", lambda state: logic.can_cut(state, player))
    connect(multiworld, player, "Route 2-NW", "Route 2-NE", lambda state: logic.can_cut(state, player))
    connect(multiworld, player, "Route 2-E", "Route 2-NE", lambda state: logic.can_cut(state, player))
    connect(multiworld, player, "Route 2-SW", "Viridian City-N")
    connect(multiworld, player, "Route 2-NW", "Pewter City")
    connect(multiworld, player, "Pewter City", "Pewter City-E")
    connect(multiworld, player, "Pewter City-M", "Pewter City", one_way=True)
    connect(multiworld, player, "Pewter City", "Pewter City-M", lambda state: logic.can_cut(state, player), one_way=True)
    connect(multiworld, player, "Pewter City-E", "Route 3", lambda state: logic.route_3(state, player), one_way=True)
    connect(multiworld, player, "Route 3", "Pewter City-E", one_way=True)
    connect(multiworld, player, "Route 4-W", "Route 3")
    connect(multiworld, player, "Route 24", "Cerulean City-Water", one_way=True)
    connect(multiworld, player, "Cerulean City-Water", "Route 4-Lass", lambda state: logic.can_surf(state, player), one_way=True)
    connect(multiworld, player, "Mt Moon B2F", "Mt Moon B2F-Wild", one_way=True)
    connect(multiworld, player, "Mt Moon B2F-NE", "Mt Moon B2F-Wild", one_way=True)
    connect(multiworld, player, "Mt Moon B2F-C", "Mt Moon B2F-Wild", one_way=True)
    connect(multiworld, player, "Route 4-Lass", "Route 4-E", one_way=True)
    connect(multiworld, player, "Route 4-C", "Route 4-E", one_way=True)
    connect(multiworld, player, "Route 4-E", "Route 4-Grass", one_way=True)
    connect(multiworld, player, "Route 4-Grass", "Cerulean City", one_way=True)
    connect(multiworld, player, "Cerulean City", "Route 24", one_way=True)
    connect(multiworld, player, "Cerulean City", "Cerulean City-T", lambda state: state.has("Help Bill", player))
    connect(multiworld, player, "Cerulean City-Outskirts", "Cerulean City", one_way=True)
    connect(multiworld, player, "Cerulean City", "Cerulean City-Outskirts", lambda state: logic.can_cut(state, player), one_way=True)
    connect(multiworld, player, "Cerulean City-Outskirts", "Route 9", lambda state: logic.can_cut(state, player))
    connect(multiworld, player, "Cerulean City-Outskirts", "Route 5")
    connect(multiworld, player, "Cerulean Cave B1F", "Cerulean Cave B1F-E", lambda state: logic.can_surf(state, player), one_way=True)
    connect(multiworld, player, "Route 24", "Route 25")
    connect(multiworld, player, "Route 9", "Route 10-N")
    connect(multiworld, player, "Route 10-N", "Route 10-C", lambda state: logic.can_surf(state, player))
    connect(multiworld, player, "Route 10-C", "Route 10-P", lambda state: state.has("Plant Key", player) or not state.multiworld.extra_key_items[player].value)
    connect(multiworld, player, "Pallet Town", "Pallet/Viridian Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Viridian City", "Pallet/Viridian Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 22", "Route 22 Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 24", "Route 24/25/Cerulean/Cerulean Gym Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 25", "Route 24/25/Cerulean/Cerulean Gym Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Cerulean City", "Route 24/25/Cerulean/Cerulean Gym Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Cerulean Gym", "Route 24/25/Cerulean/Cerulean Gym Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 6", "Route 6/11/Vermilion/Dock Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 11", "Route 6/11/Vermilion/Dock Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Vermilion City", "Route 6/11/Vermilion/Dock Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Vermilion Dock", "Route 6/11/Vermilion/Dock Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 10-N", "Route 10/Celadon Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 10-C", "Route 10/Celadon Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Celadon City", "Route 10/Celadon Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Safari Zone Center-NW", "Safari Zone Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Safari Zone Center-NE", "Safari Zone Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Safari Zone Center-S", "Safari Zone Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Safari Zone West", "Safari Zone Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Safari Zone West-NW", "Safari Zone Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Safari Zone East", "Safari Zone Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Safari Zone North", "Safari Zone Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 12-N", "Route 12/13/17/18 Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 12-S", "Route 12/13/17/18 Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 13", "Route 12/13/17/18 Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 13-E", "Route 12/13/17/18 Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 17", "Route 12/13/17/18 Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 18-W", "Route 12/13/17/18 Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 21", "Sea Routes/Cinnabar/Seafoam Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Cinnabar Island", "Sea Routes/Cinnabar/Seafoam Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 20-IW", "Sea Routes/Cinnabar/Seafoam Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 20-IE", "Sea Routes/Cinnabar/Seafoam Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 19-N", "Sea Routes/Cinnabar/Seafoam Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Seafoam Islands B3F", "Sea Routes/Cinnabar/Seafoam Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Seafoam Islands B4F", "Sea Routes/Cinnabar/Seafoam Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 23-S", "Route 23/Cerulean Cave Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 23-Grass", "Route 23/Cerulean Cave Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Cerulean Cave 1F-SE", "Route 23/Cerulean Cave Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Cerulean Cave 1F-NE", "Route 23/Cerulean Cave Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Cerulean Cave 1F-N", "Route 23/Cerulean Cave Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Cerulean Cave 1F-SW", "Route 23/Cerulean Cave Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Cerulean Cave B1F", "Route 23/Cerulean Cave Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Fuchsia City", "Fuchsia Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Pallet Town", "Old Rod Fishing", lambda state: state.has("Old Rod", player), one_way=True)
    connect(multiworld, player, "Pallet Town", "Good Rod Fishing", lambda state: state.has("Good Rod", player), one_way=True)
    connect(multiworld, player, "Cinnabar Lab Fossil Room", "Fossil Level", lambda state: logic.fossil_checks(state, 1, player), one_way=True)
    connect(multiworld, player, "Route 5 Gate-N", "Route 5 Gate-S", lambda state: logic.can_pass_guards(state, player))
    connect(multiworld, player, "Route 6 Gate-N", "Route 6 Gate-S", lambda state: logic.can_pass_guards(state, player))
    connect(multiworld, player, "Route 7 Gate-W", "Route 7 Gate-E", lambda state: logic.can_pass_guards(state, player))
    connect(multiworld, player, "Route 8 Gate-W", "Route 8 Gate-E", lambda state: logic.can_pass_guards(state, player))
    connect(multiworld, player, "Saffron City", "Route 5-S")
    connect(multiworld, player, "Saffron City", "Route 6-N")
    connect(multiworld, player, "Saffron City", "Route 7-E")
    connect(multiworld, player, "Saffron City", "Route 8-W")
    connect(multiworld, player, "Saffron City", "Saffron City-Copycat", lambda state: state.has("Silph Co Liberated", player))
    connect(multiworld, player, "Saffron City", "Saffron City-Pidgey", lambda state: state.has("Silph Co Liberated", player))
    connect(multiworld, player, "Saffron City", "Saffron City-G", lambda state: state.has("Silph Co Liberated", player))
    connect(multiworld, player, "Saffron City", "Saffron City-Silph", lambda state: state.has("Fuji Saved", player))
    connect(multiworld, player, "Route 6", "Vermilion City")
    connect(multiworld, player, "Vermilion City", "Vermilion City-G", lambda state: logic.can_surf(state, player) or logic.can_cut(state, player))
    connect(multiworld, player, "Vermilion City", "Vermilion City-Dock", lambda state: state.has("S.S. Ticket", player))
    connect(multiworld, player, "Vermilion City", "Route 11")
    connect(multiworld, player, "Route 12-N", "Route 12-S", lambda state: logic.can_surf(state, player))
    connect(multiworld, player, "Route 12-W", "Route 11-E", lambda state: state.has("Poke Flute", player))
    connect(multiworld, player, "Route 12-W", "Route 12-N", lambda state: state.has("Poke Flute", player))
    connect(multiworld, player, "Route 12-W", "Route 12-S", lambda state: state.has("Poke Flute", player))
    connect(multiworld, player, "Route 12-S", "Route 12-Grass", lambda state: logic.can_cut(state, player), one_way=True)
    connect(multiworld, player, "Route 12-L", "Lavender Town")
    connect(multiworld, player, "Route 10-S", "Lavender Town")
    connect(multiworld, player, "Route 8", "Lavender Town")
    connect(multiworld, player, "Pokemon Tower 6F", "Pokemon Tower 6F-S", lambda state: state.has("Silph Scope", player) or (state.has("Buy Poke Doll", player) and state.multiworld.poke_doll_skip[player]))
    connect(multiworld, player, "Route 8", "Route 8-Grass", lambda state: logic.can_cut(state, player), one_way=True)
    connect(multiworld, player, "Route 7", "Celadon City")
    connect(multiworld, player, "Celadon City", "Celadon City-G", lambda state: logic.can_cut(state, player))
    connect(multiworld, player, "Celadon City", "Route 16-E")
    connect(multiworld, player, "Route 18 Gate 1F-W", "Route 18 Gate 1F-E", lambda state: state.has("Bicycle", player) or state.multiworld.bicycle_gate_skips[player] == "in_logic")
    connect(multiworld, player, "Route 16 Gate 1F-W", "Route 16 Gate 1F-E", lambda state: state.has("Bicycle", player) or state.multiworld.bicycle_gate_skips[player] == "in_logic")
    connect(multiworld, player, "Route 16-E", "Route 16-NE", lambda state: logic.can_cut(state, player))
    connect(multiworld, player, "Route 16-E", "Route 16-C", lambda state: state.has("Poke Flute", player))
    connect(multiworld, player, "Route 17", "Route 16-SW")
    connect(multiworld, player, "Route 17", "Route 18-W")
    # connect(multiworld, player, "Pokemon Mansion 2F", "Pokemon Mansion 2F-NW", one_way=True)
    connect(multiworld, player, "Safari Zone Gate-S", "Safari Zone Gate-N", lambda state: state.has("Safari Pass", player) or not state.multiworld.extra_key_items[player].value, one_way=True)
    connect(multiworld, player, "Fuchsia City", "Route 15-W")
    connect(multiworld, player, "Fuchsia City", "Route 18-E")
    connect(multiworld, player, "Route 15", "Route 14")
    connect(multiworld, player, "Route 14", "Route 15-N", lambda state: logic.can_cut(state, player), one_way=True)
    connect(multiworld, player, "Route 14", "Route 14-Grass", lambda state: logic.can_cut(state, player), one_way=True)
    connect(multiworld, player, "Route 13", "Route 13-Grass", lambda state: logic.can_cut(state, player), one_way=True)
    connect(multiworld, player, "Route 14", "Route 13")
    connect(multiworld, player, "Route 13", "Route 13-E", lambda state: logic.can_strength(state, player) or logic.can_surf(state, player) or not state.multiworld.extra_strength_boulders[player].value)
    connect(multiworld, player, "Route 12-S", "Route 13-E")
    connect(multiworld, player, "Fuchsia City", "Route 19-N")
    connect(multiworld, player, "Route 19-N", "Route 19-S", lambda state: logic.can_surf(state, player))
    connect(multiworld, player, "Route 20-E", "Route 20-IW", lambda state: logic.can_surf(state, player))
    connect(multiworld, player, "Route 20-E", "Route 19-S")
    connect(multiworld, player, "Route 20-W", "Cinnabar Island", lambda state: logic.can_surf(state, player))
    connect(multiworld, player, "Route 20-IE", "Route 20-W", lambda state: logic.can_surf(state, player))
    connect(multiworld, player, "Route 20-E", "Route 19/20-Water", one_way=True)
    connect(multiworld, player, "Route 20-W", "Route 19/20-Water", one_way=True)
    connect(multiworld, player, "Route 19-S", "Route 19/20-Water", one_way=True)
    connect(multiworld, player, "Safari Zone West-NW", "Safari Zone West", lambda state: logic.can_surf(state, player))
    connect(multiworld, player, "Safari Zone West", "Safari Zone West-Wild", one_way=True)
    connect(multiworld, player, "Safari Zone West-NW", "Safari Zone West-Wild", one_way=True)
    connect(multiworld, player, "Safari Zone Center-NW", "Safari Zone Center-C", lambda state: logic.can_surf(state, player))
    connect(multiworld, player, "Safari Zone Center-NE", "Safari Zone Center-C", lambda state: logic.can_surf(state, player))
    connect(multiworld, player, "Safari Zone Center-S", "Safari Zone Center-C", lambda state: logic.can_surf(state, player))
    connect(multiworld, player, "Safari Zone Center-S", "Safari Zone Center-Wild", one_way=True)
    connect(multiworld, player, "Safari Zone Center-NW", "Safari Zone Center-Wild", one_way=True)
    connect(multiworld, player, "Safari Zone Center-NE", "Safari Zone Center-Wild", one_way=True)
    connect(multiworld, player, "Victory Road 3F-S", "Victory Road 3F", lambda state: logic.can_strength(state, player))
    connect(multiworld, player, "Victory Road 3F-SE", "Victory Road 3F-S", lambda state: logic.can_strength(state, player), one_way=True)
    connect(multiworld, player, "Victory Road 3F", "Victory Road 3F-Wild", one_way=True)
    connect(multiworld, player, "Victory Road 3F-SE", "Victory Road 3F-Wild", one_way=True)
    connect(multiworld, player, "Victory Road 3F-S", "Victory Road 3F-Wild", one_way=True)
    connect(multiworld, player, "Victory Road 2F-W", "Victory Road 2F-Wild", one_way=True)
    connect(multiworld, player, "Victory Road 2F-NW", "Victory Road 2F-Wild", one_way=True)
    connect(multiworld, player, "Victory Road 2F-C", "Victory Road 2F-Wild", one_way=True)
    connect(multiworld, player, "Victory Road 2F-E", "Victory Road 2F-Wild", one_way=True)
    connect(multiworld, player, "Victory Road 2F-SE", "Victory Road 2F-Wild", one_way=True)
    connect(multiworld, player, "Victory Road 2F-W", "Victory Road 2F-C", lambda state: logic.can_strength(state, player), one_way=True)
    connect(multiworld, player, "Victory Road 2F-NW", "Victory Road 2F-W", lambda state: logic.can_strength(state, player), one_way=True)
    connect(multiworld, player, "Victory Road 2F-C", "Victory Road 2F-SE", lambda state: logic.can_strength(state, player) and state.has("Victory Road Boulder", player), one_way=True)
    connect(multiworld, player, "Victory Road 1F-S", "Victory Road 1F", lambda state: logic.can_strength(state, player))
    connect(multiworld, player, "Victory Road 1F", "Victory Road 1F-Wild", one_way=True)
    connect(multiworld, player, "Victory Road 1F-S", "Victory Road 1F-Wild", one_way=True)
    connect(multiworld, player, "Mt Moon B1F-W", "Mt Moon B1F-Wild", one_way=True)
    connect(multiworld, player, "Mt Moon B1F-C", "Mt Moon B1F-Wild", one_way=True)
    connect(multiworld, player, "Mt Moon B1F-NE", "Mt Moon B1F-Wild", one_way=True)
    connect(multiworld, player, "Mt Moon B1F-SE", "Mt Moon B1F-Wild", one_way=True)
    connect(multiworld, player, "Cerulean Cave 2F-N", "Cerulean Cave 2F-Wild", one_way=True)
    connect(multiworld, player, "Cerulean Cave 2F-E", "Cerulean Cave 2F-Wild", one_way=True)
    connect(multiworld, player, "Cerulean Cave 2F-W", "Cerulean Cave 2F-Wild", one_way=True)
    connect(multiworld, player, "Seafoam Islands 1F", "Seafoam Islands 1F-Wild", one_way=True)
    connect(multiworld, player, "Seafoam Islands 1F-SE", "Seafoam Islands 1F-Wild", one_way=True)
    connect(multiworld, player, "Seafoam Islands B1F", "Seafoam Islands B1F-Wild", one_way=True)
    connect(multiworld, player, "Seafoam Islands B1F-SE", "Seafoam Islands B1F-Wild", one_way=True)
    connect(multiworld, player, "Seafoam Islands B1F-NE", "Seafoam Islands B1F-Wild", one_way=True)
    connect(multiworld, player, "Seafoam Islands B2F-NW", "Seafoam Islands B2F-Wild", one_way=True)
    connect(multiworld, player, "Seafoam Islands B2F-NE", "Seafoam Islands B2F-Wild", one_way=True)
    connect(multiworld, player, "Seafoam Islands B2F-SW", "Seafoam Islands B2F-Wild", one_way=True)
    connect(multiworld, player, "Seafoam Islands B2F-SE", "Seafoam Islands B2F-Wild", one_way=True)
    connect(multiworld, player, "Seafoam Islands B3F", "Seafoam Islands B3F-Wild", one_way=True)
    connect(multiworld, player, "Seafoam Islands B3F-NE", "Seafoam Islands B3F-Wild", one_way=True)
    connect(multiworld, player, "Seafoam Islands B3F-SE", "Seafoam Islands B3F-Wild", one_way=True)
    connect(multiworld, player, "Seafoam Islands B4F", "Seafoam Islands B4F-W", lambda state: logic.can_surf(state, player), one_way=True)
    connect(multiworld, player, "Seafoam Islands B4F-W", "Seafoam Islands B4F", one_way=True)
    # This really shouldn't be necessary since if the boulders are reachable you can drop, but might as well be thorough
    connect(multiworld, player, "Seafoam Islands B3F", "Seafoam Islands B3F-SE", lambda state: logic.can_surf(state, player) and logic.can_strength(state, player) and state.has("Seafoam Exit Boulder", player, 6))
    connect(multiworld, player, "Viridian City", "Viridian City-N", lambda state: state.has("Oak's Parcel", player) or state.multiworld.old_man[player].value == 2 or logic.can_cut(state, player))
    connect(multiworld, player, "Route 11", "Route 11-C", lambda state: logic.can_strength(state, player) or not state.multiworld.extra_strength_boulders[player])
    connect(multiworld, player, "Cinnabar Island", "Cinnabar Island-G", lambda state: state.has("Secret Key", player))
    connect(multiworld, player, "Cinnabar Island", "Cinnabar Island-M", lambda state: state.has("Mansion Key", player) or not state.multiworld.extra_key_items[player].value)
    connect(multiworld, player, "Route 21", "Cinnabar Island", lambda state: logic.can_surf(state, player))
    connect(multiworld, player, "Pallet Town", "Route 21", lambda state: logic.can_surf(state, player))
    connect(multiworld, player, "Celadon Gym", "Celadon Gym-C", lambda state: logic.can_cut(state, player), one_way=True)
    connect(multiworld, player, "Celadon Game Corner", "Celadon Game Corner-Hidden Stairs", lambda state: (not state.multiworld.extra_key_items[player]) or state.has("Hideout Key", player), one_way=True)
    connect(multiworld, player, "Celadon Game Corner-Hidden Stairs", "Celadon Game Corner", one_way=True)
    connect(multiworld, player, "Rocket Hideout B1F-SE", "Rocket Hideout B1F", one_way=True)
    connect(multiworld, player, "Indigo Plateau Lobby", "Indigo Plateau Lobby-N", lambda state: logic.has_badges(state, state.multiworld.elite_four_badges_condition[player].value, player) and logic.has_pokemon(state, state.multiworld.elite_four_pokedex_condition[player].total, player) and logic.has_key_items(state, state.multiworld.elite_four_key_items_condition[player].total, player) and (state.has("Pokedex", player, int(state.multiworld.elite_four_pokedex_condition[player].total > 1) * state.multiworld.require_pokedex[player].value)))
    connect(multiworld, player, "Pokemon Mansion 3F", "Pokemon Mansion 3F-Wild", one_way=True)
    connect(multiworld, player, "Pokemon Mansion 3F-SW", "Pokemon Mansion 3F-Wild", one_way=True)
    connect(multiworld, player, "Pokemon Mansion 3F-SE", "Pokemon Mansion 3F-Wild", one_way=True)
    connect(multiworld, player, "Pokemon Mansion 2F-E", "Pokemon Mansion 2F-Wild", one_way=True)
    connect(multiworld, player, "Pokemon Mansion 1F-SE", "Pokemon Mansion 1F-Wild", one_way=True)
    connect(multiworld, player, "Pokemon Mansion 1F", "Pokemon Mansion 1F-Wild", one_way=True)
    connect(multiworld, player, "Rock Tunnel 1F-S", "Rock Tunnel 1F-Wild", lambda state: logic.rock_tunnel(state, player), one_way=True)
    connect(multiworld, player, "Rock Tunnel 1F-NW", "Rock Tunnel 1F-Wild", lambda state: logic.rock_tunnel(state, player), one_way=True)
    connect(multiworld, player, "Rock Tunnel 1F-NE", "Rock Tunnel 1F-Wild", lambda state: logic.rock_tunnel(state, player), one_way=True)
    connect(multiworld, player, "Rock Tunnel B1F-W", "Rock Tunnel B1F-Wild", lambda state: logic.rock_tunnel(state, player), one_way=True)
    connect(multiworld, player, "Rock Tunnel B1F-E", "Rock Tunnel B1F-Wild", lambda state: logic.rock_tunnel(state, player), one_way=True)
    connect(multiworld, player, "Cerulean Cave 1F-SE", "Cerulean Cave 1F-Wild", one_way=True)
    connect(multiworld, player, "Cerulean Cave 1F-SW", "Cerulean Cave 1F-Wild", one_way=True)
    connect(multiworld, player, "Cerulean Cave 1F-NE", "Cerulean Cave 1F-Wild", one_way=True)
    connect(multiworld, player, "Cerulean Cave 1F-N", "Cerulean Cave 1F-Wild", one_way=True)
    connect(multiworld, player, "Cerulean Cave 1F-NW", "Cerulean Cave 1F-Wild", one_way=True)
    connect(multiworld, player, "Cerulean Cave 1F-SE", "Cerulean Cave 1F-Water", lambda state: logic.can_surf(state, player))
    connect(multiworld, player, "Cerulean Cave 1F-SW", "Cerulean Cave 1F-Water", lambda state: logic.can_surf(state, player))
    connect(multiworld, player, "Cerulean Cave 1F-N", "Cerulean Cave 1F-Water", lambda state: logic.can_surf(state, player))
    connect(multiworld, player, "Cerulean Cave 1F-NE", "Cerulean Cave 1F-Water", lambda state: logic.can_surf(state, player))
    connect(multiworld, player, "Pokemon Mansion 3F", "Pokemon Mansion 3F-SE", one_way=True)
    connect(multiworld, player, "Silph Co 2F", "Silph Co 2F-NW", lambda state: logic.card_key(state, 2, player))
    connect(multiworld, player, "Silph Co 2F", "Silph Co 2F-SW", lambda state: logic.card_key(state, 2, player))
    connect(multiworld, player, "Silph Co 3F", "Silph Co 3F-C", lambda state: logic.card_key(state, 3, player))
    connect(multiworld, player, "Silph Co 3F-W", "Silph Co 3F-C", lambda state: logic.card_key(state, 3, player))
    connect(multiworld, player, "Silph Co 4F", "Silph Co 4F-N", lambda state: logic.card_key(state, 4, player))
    connect(multiworld, player, "Silph Co 4F", "Silph Co 4F-W", lambda state: logic.card_key(state, 4, player))
    connect(multiworld, player, "Silph Co 5F", "Silph Co 5F-NW", lambda state: logic.card_key(state, 5, player))
    connect(multiworld, player, "Silph Co 5F", "Silph Co 5F-SW", lambda state: logic.card_key(state, 5, player))
    connect(multiworld, player, "Silph Co 6F", "Silph Co 6F-SW", lambda state: logic.card_key(state, 6, player))
    connect(multiworld, player, "Silph Co 7F", "Silph Co 7F-E", lambda state: logic.card_key(state, 7, player))
    connect(multiworld, player, "Silph Co 7F-SE", "Silph Co 7F-E", lambda state: logic.card_key(state, 7, player))
    connect(multiworld, player, "Silph Co 8F", "Silph Co 8F-W", lambda state: logic.card_key(state, 8, player), one_way=True, name="Silph Co 8F to Silph Co 8F-W (Card Key)")
    connect(multiworld, player, "Silph Co 8F-W", "Silph Co 8F", lambda state: logic.card_key(state, 8, player), one_way=True, name="Silph Co 8F-W to Silph Co 8F (Card Key)")
    connect(multiworld, player, "Silph Co 9F", "Silph Co 9F-SW", lambda state: logic.card_key(state, 9, player))
    connect(multiworld, player, "Silph Co 9F-NW", "Silph Co 9F-SW", lambda state: logic.card_key(state, 9, player))
    connect(multiworld, player, "Silph Co 10F", "Silph Co 10F-SE", lambda state: logic.card_key(state, 10, player))
    connect(multiworld, player, "Silph Co 11F-W", "Silph Co 11F-C", lambda state: logic.card_key(state, 11, player))
    connect(multiworld, player, "Silph Co Elevator", "Silph Co Elevator-1F", lambda state: (not state.multiworld.all_elevators_locked[player]) or state.has("Lift Key", player)),
    connect(multiworld, player, "Silph Co Elevator", "Silph Co Elevator-2F", lambda state: (not state.multiworld.all_elevators_locked[player]) or state.has("Lift Key", player)),
    connect(multiworld, player, "Silph Co Elevator", "Silph Co Elevator-3F", lambda state: (not state.multiworld.all_elevators_locked[player]) or state.has("Lift Key", player)),
    connect(multiworld, player, "Silph Co Elevator", "Silph Co Elevator-4F", lambda state: (not state.multiworld.all_elevators_locked[player]) or state.has("Lift Key", player)),
    connect(multiworld, player, "Silph Co Elevator", "Silph Co Elevator-5F", lambda state: (not state.multiworld.all_elevators_locked[player]) or state.has("Lift Key", player)),
    connect(multiworld, player, "Silph Co Elevator", "Silph Co Elevator-6F", lambda state: (not state.multiworld.all_elevators_locked[player]) or state.has("Lift Key", player)),
    connect(multiworld, player, "Silph Co Elevator", "Silph Co Elevator-7F", lambda state: (not state.multiworld.all_elevators_locked[player]) or state.has("Lift Key", player)),
    connect(multiworld, player, "Silph Co Elevator", "Silph Co Elevator-8F", lambda state: (not state.multiworld.all_elevators_locked[player]) or state.has("Lift Key", player)),
    connect(multiworld, player, "Silph Co Elevator", "Silph Co Elevator-9F", lambda state: (not state.multiworld.all_elevators_locked[player]) or state.has("Lift Key", player)),
    connect(multiworld, player, "Silph Co Elevator", "Silph Co Elevator-10F", lambda state: (not state.multiworld.all_elevators_locked[player]) or state.has("Lift Key", player)),
    connect(multiworld, player, "Silph Co Elevator", "Silph Co Elevator-11F", lambda state: (not state.multiworld.all_elevators_locked[player]) or state.has("Lift Key", player)),
    connect(multiworld, player, "Rocket Hideout Elevator", "Rocket Hideout Elevator-B1F", lambda state: state.has("Lift Key", player))
    connect(multiworld, player, "Rocket Hideout Elevator", "Rocket Hideout Elevator-B2F", lambda state: state.has("Lift Key", player))
    connect(multiworld, player, "Rocket Hideout Elevator", "Rocket Hideout Elevator-B4F", lambda state: state.has("Lift Key", player))
    connect(multiworld, player, "Celadon Department Store Elevator", "Celadon Department Store Elevator-1F", lambda state: (not state.multiworld.all_elevators_locked[player]) or state.has("Lift Key", player)),
    connect(multiworld, player, "Celadon Department Store Elevator", "Celadon Department Store Elevator-2F", lambda state: (not state.multiworld.all_elevators_locked[player]) or state.has("Lift Key", player)),
    connect(multiworld, player, "Celadon Department Store Elevator", "Celadon Department Store Elevator-3F", lambda state: (not state.multiworld.all_elevators_locked[player]) or state.has("Lift Key", player)),
    connect(multiworld, player, "Celadon Department Store Elevator", "Celadon Department Store Elevator-4F", lambda state: (not state.multiworld.all_elevators_locked[player]) or state.has("Lift Key", player)),
    connect(multiworld, player, "Celadon Department Store Elevator", "Celadon Department Store Elevator-5F", lambda state: (not state.multiworld.all_elevators_locked[player]) or state.has("Lift Key", player)),
    connect(multiworld, player, "Route 23-N", "Indigo Plateau")
    connect(multiworld, player, "Cerulean City-Water", "Cerulean City-Cave", lambda state:
        logic.has_badges(state, self.multiworld.cerulean_cave_badges_condition[player].value, player) and
        logic.has_key_items(state, self.multiworld.cerulean_cave_key_items_condition[player].total, player) and logic.can_surf(state, player))


    # access to any part of a city will enable flying to the Pokemon Center
    connect(multiworld, player, "Cerulean City-Cave", "Cerulean City", lambda state: logic.can_fly(state, player), one_way=True)
    connect(multiworld, player, "Cerulean City-Badge House Backyard", "Cerulean City", lambda state: logic.can_fly(state, player), one_way=True)
    connect(multiworld, player, "Cerulean City-T", "Cerulean City", lambda state: logic.can_fly(state, player), one_way=True, name="Cerulean City-T to Cerulean City (Fly)")
    connect(multiworld, player, "Fuchsia City-Good Rod House Backyard", "Fuchsia City", lambda state: logic.can_fly(state, player), one_way=True)
    connect(multiworld, player, "Saffron City-G", "Saffron City", lambda state: logic.can_fly(state, player), one_way=True, name="Saffron City-G to Saffron City (Fly)")
    connect(multiworld, player, "Saffron City-Pidgey", "Saffron City", lambda state: logic.can_fly(state, player), one_way=True, name="Saffron City-Pidgey to Saffron City (Fly)")
    connect(multiworld, player, "Saffron City-Silph", "Saffron City", lambda state: logic.can_fly(state, player), one_way=True, name="Saffron City-Silph to Saffron City (Fly)")
    connect(multiworld, player, "Saffron City-Copycat", "Saffron City", lambda state: logic.can_fly(state, player), one_way=True, name="Saffron City-Copycat to Saffron City (Fly)")
    connect(multiworld, player, "Celadon City-G", "Celadon City", lambda state: logic.can_fly(state, player), one_way=True, name="Celadon City-G to Celadon City (Fly)")
    connect(multiworld, player, "Vermilion City-G", "Vermilion City", lambda state: logic.can_fly(state, player), one_way=True, name="Vermilion City-G to Vermilion City (Fly)")
    connect(multiworld, player, "Vermilion City-Dock", "Vermilion City", lambda state: logic.can_fly(state, player), one_way=True, name="Vermilion City-Dock to Vermilion City (Fly)")
    connect(multiworld, player, "Cinnabar Island-G", "Cinnabar Island", lambda state: logic.can_fly(state, player), one_way=True, name="Cinnabar Island-G to Cinnabar Island (Fly)")
    connect(multiworld, player, "Cinnabar Island-M", "Cinnabar Island", lambda state: logic.can_fly(state, player), one_way=True, name="Cinnabar Island-M to Cinnabar Island (Fly)")


    # drops
    connect(multiworld, player, "Seafoam Islands 1F", "Seafoam Islands B1F", one_way=True, name="Seafoam Islands 1F to Seafoam Islands B1F (Drop)")
    connect(multiworld, player, "Seafoam Islands 1F", "Seafoam Islands B1F-NE", one_way=True, name="Seafoam Islands 1F to Seafoam Islands B1F-NE (Drop)")
    connect(multiworld, player, "Seafoam Islands B1F", "Seafoam Islands B2F-NW", one_way=True, name="Seafoam Islands 1F to Seafoam Islands B2F-NW (Drop)")
    connect(multiworld, player, "Seafoam Islands B1F-NE", "Seafoam Islands B2F-NE", one_way=True)
    connect(multiworld, player, "Seafoam Islands B2F-NW", "Seafoam Islands B3F", lambda state: logic.can_strength(state, player) and state.has("Seafoam Exit Boulder", player, 6), one_way=True)
    connect(multiworld, player, "Seafoam Islands B2F-NE", "Seafoam Islands B3F", lambda state: logic.can_strength(state, player) and state.has("Seafoam Exit Boulder", player, 6), one_way=True)
    connect(multiworld, player, "Seafoam Islands B2F-NW", "Seafoam Islands B3F-SE", lambda state: logic.can_strength(state, player) and state.has("Seafoam Exit Boulder", player, 6), one_way=True)
    connect(multiworld, player, "Seafoam Islands B2F-NE", "Seafoam Islands B3F-SE", lambda state: logic.can_strength(state, player) and state.has("Seafoam Exit Boulder", player, 6), one_way=True)
    # If you haven't dropped the boulders, you'll go straight to B4F
    connect(multiworld, player, "Seafoam Islands B2F-NW", "Seafoam Islands B4F-W", one_way=True)
    connect(multiworld, player, "Seafoam Islands B2F-NE", "Seafoam Islands B4F-W", one_way=True)
    connect(multiworld, player, "Seafoam Islands B3F", "Seafoam Islands B4F", one_way=True, name="Seafoam Islands B1F to Seafoam Islands B4F (Drop)")
    connect(multiworld, player, "Seafoam Islands B3F", "Seafoam Islands B4F-W", lambda state: logic.can_surf(state, player), one_way=True)
    connect(multiworld, player, "Pokemon Mansion 3F-SE", "Pokemon Mansion 2F", one_way=True)
    connect(multiworld, player, "Pokemon Mansion 3F-SE", "Pokemon Mansion 1F-SE", one_way=True)
    connect(multiworld, player, "Victory Road 3F-S", "Victory Road 2F-C", one_way=True)

    if multiworld.worlds[player].fly_map != "Pallet Town":
        connect(multiworld, player, "Menu", multiworld.worlds[player].fly_map,
                lambda state: logic.can_fly(state, player), one_way=True, name="Free Fly Location")

    if multiworld.worlds[player].town_map_fly_map != "Pallet Town":
        connect(multiworld, player, "Menu", multiworld.worlds[player].town_map_fly_map,
                lambda state: logic.can_fly(state, player) and state.has("Town Map", player), one_way=True,
                name="Town Map Fly Location")

    entrances = []
    for region_name, region_entrances in warp_data.items():
        for entrance_data in region_entrances:
            region = multiworld.get_region(region_name, player)
            shuffle = True
            if not outdoor_map(region.name) and not outdoor_map(entrance_data['to']['map']) and \
                    multiworld.door_shuffle[player] not in ("insanity", "decoupled"):
                shuffle = False
            if multiworld.door_shuffle[player] == "simple":
                if sorted([entrance_data['to']['map'], region.name]) == ["Celadon Game Corner-Hidden Stairs",
                                                                         "Rocket Hideout B1F"]:
                    shuffle = True
                elif sorted([entrance_data['to']['map'], region.name]) == ["Celadon City", "Celadon Game Corner"]:
                    shuffle = False
            if (multiworld.randomize_rock_tunnel[player] and "Rock Tunnel" in region.name and "Rock Tunnel" in
                    entrance_data['to']['map']):
                shuffle = False
            if (f"{region.name} to {entrance_data['to']['map']}" if "name" not in entrance_data else
                    entrance_data["name"]) in silph_co_warps + saffron_gym_warps:
                if multiworld.warp_tile_shuffle[player] or multiworld.door_shuffle[player] in ("insanity",
                                                                                               "decoupled"):
                    shuffle = True
                else:
                    shuffle = False
            elif not multiworld.door_shuffle[player]:
                shuffle = False
            if shuffle:
                entrance = PokemonRBWarp(player, f"{region.name} to {entrance_data['to']['map']}" if "name" not in
                                         entrance_data else entrance_data["name"], region, entrance_data["id"],
                                         entrance_data["address"], entrance_data["flags"] if "flags" in
                                         entrance_data else "")
                # if "Rock Tunnel" in region_name:
                #     entrance.access_rule = lambda state: logic.rock_tunnel(state, player)
                entrances.append(entrance)
                region.exits.append(entrance)
            else:
                # connect(multiworld, player, region.name, entrance_data['to']['map'], one_way=True)
                if "Rock Tunnel" in region.name:
                    connect(multiworld, player, region.name, entrance_data["to"]["map"],
                            lambda state: logic.rock_tunnel(state, player), one_way=True)
                else:
                    connect(multiworld, player, region.name, entrance_data["to"]["map"], one_way=True,
                            name=entrance_data["name"] if "name" in entrance_data else None)

    forced_connections = set()

    if multiworld.door_shuffle[player]:
        forced_connections.update(mandatory_connections.copy())
        usable_safe_rooms = safe_rooms.copy()

        if multiworld.door_shuffle[player] == "simple":
            forced_connections.update(simple_mandatory_connections)
        else:
            usable_safe_rooms += pokemarts
            if self.multiworld.key_items_only[self.player]:
                usable_safe_rooms.remove("Viridian Pokemart to Viridian City")
        if multiworld.door_shuffle[player] in ("insanity", "decoupled"):
            forced_connections.update(insanity_mandatory_connections)
            r = multiworld.random.randint(0, 3)
            if r == 2:
                forced_connections.add(("Pokemon Mansion 1F-SE to Pokemon Mansion B1F",
                                        "Pokemon Mansion 3F-SE to Pokemon Mansion 2F-E"))
                forced_connections.add(("Pokemon Mansion 2F to Pokemon Mansion 3F",
                                        multiworld.random.choice(mansion_stair_destinations + mansion_dead_ends
                                                                 + ["Pokemon Mansion B1F to Pokemon Mansion 1F-SE"])))
            elif r == 3:
                dead_end = multiworld.random.randint(0, 1)
                forced_connections.add(("Pokemon Mansion 3F-SE to Pokemon Mansion 2F-E",
                                        mansion_dead_ends[dead_end]))
                forced_connections.add(("Pokemon Mansion 1F-SE to Pokemon Mansion B1F",
                                        "Pokemon Mansion B1F to Pokemon Mansion 1F-SE"))
                forced_connections.add(("Pokemon Mansion 2F to Pokemon Mansion 3F",
                                        multiworld.random.choice(mansion_stair_destinations
                                                                 + [mansion_dead_ends[dead_end ^ 1]])))
            else:
                forced_connections.add(("Pokemon Mansion 3F-SE to Pokemon Mansion 2F-E",
                                        mansion_dead_ends[r]))
                forced_connections.add(("Pokemon Mansion 1F-SE to Pokemon Mansion B1F",
                                        mansion_dead_ends[r ^ 1]))
                forced_connections.add(("Pokemon Mansion 2F to Pokemon Mansion 3F",
                                        multiworld.random.choice(mansion_stair_destinations
                                                                 + ["Pokemon Mansion B1F to Pokemon Mansion 1F-SE"])))

            usable_safe_rooms += insanity_safe_rooms

        safe_rooms_sample = multiworld.random.sample(usable_safe_rooms, 6)
        pallet_safe_room = safe_rooms_sample[-1]

        for a, b in zip(multiworld.random.sample(["Pallet Town to Player's House 1F", "Pallet Town to Oak's Lab",
                                                  "Pallet Town to Rival's House"], 3), ["Oak's Lab to Pallet Town",
                                                  "Player's House 1F to Pallet Town", pallet_safe_room]):
            forced_connections.add((a, b))
        for a, b in zip(safari_zone_houses, safe_rooms_sample):
            forced_connections.add((a, b))
        if multiworld.door_shuffle[player] == "simple":
            # force Indigo Plateau Lobby to vanilla location on simple, otherwise shuffle with Pokemon Centers.
            for a, b in zip(multiworld.random.sample(pokemon_center_entrances[0:-1], 11), pokemon_centers[0:-1]):
                forced_connections.add((a, b))
            forced_connections.add((pokemon_center_entrances[-1], pokemon_centers[-1]))
            forced_pokemarts = multiworld.random.sample(pokemart_entrances, 8)
            if self.multiworld.key_items_only[self.player]:
                forced_pokemarts.sort(key=lambda i: i[0] != "Viridian Pokemart to Viridian City")
            for a, b in zip(forced_pokemarts, pokemarts):
                forced_connections.add((a, b))
        else:
            # Pokemon Centers must be reached from the Cities and Routes that have programmed coordinates for
            # fly / blackout warps. Rather than mess with those coordinates (besides in Pallet Town) or have players
            # warping outside an entrance that isn't the Pokemon Center, just always put Pokemon Centers at Pokemon
            # Center entrances
            for a, b in zip(multiworld.random.sample(pokemon_center_entrances, 12), pokemon_centers):
                forced_connections.add((a, b))
            # Ensure a Pokemart is available at the beginning of the game
            if multiworld.key_items_only[player]:
                forced_connections.add((multiworld.random.choice(initial_doors), "Viridian Pokemart to Viridian City"))
            elif "Pokemart" not in pallet_safe_room:
                forced_connections.add((multiworld.random.choice(initial_doors), multiworld.random.choice(
                    [mart for mart in pokemarts if mart not in safe_rooms_sample])))

    if multiworld.warp_tile_shuffle[player]:
        warps = multiworld.random.sample(silph_co_warps, len(silph_co_warps))
        # The only warp tiles never reachable from the stairs/elevators are the two 7F-NW warps (where the rival is)
        # and the final 11F-W warp. As long as the two 7F-NW warps aren't connected to each other, everything should
        # always be reachable.
        warps.sort(key=lambda i: 0 if i == "Silph Co 7F-NW to Silph Co 3F-C" else
                   2 if i == "Silph Co 7F-NW to Silph Co 11F-W" else 1)
        while warps:
            forced_connections.add((warps.pop(), warps.pop(),))

        # Shuffle Saffron Gym sections, then connect one warp from each section to the next.
        # Then connect the rest at random.
        warps = multiworld.random.sample(saffron_gym_warps, len(saffron_gym_warps))
        solution = ["SW", "W", "NW", "N", "NE", "E", "SE"]
        multiworld.random.shuffle(solution)
        solution = ["S"] + solution + ["C"]
        for i in range(len(solution) - 1):
            f, t = solution[i], solution[i + 1]
            fw = None
            tw = None
            for warp in warps:
                if fw is None and warp.split(" to ")[0].endswith(f"-{f}"):
                    fw = warp
                if tw is None and warp.split(" to ")[0].endswith(f"-{t}"):
                    tw = warp
                if fw is not None and tw is not None:
                    break
            warps.remove(fw)
            warps.remove(tw)
            forced_connections.add((fw, tw))
        while warps:
            forced_connections.add((warps.pop(), warps.pop(),))

    for pair in forced_connections:
        entrance_a = multiworld.get_entrance(pair[0], player)
        entrance_b = multiworld.get_entrance(pair[1], player)
        entrance_a.connect(entrance_b)
        entrance_b.connect(entrance_a)
        entrances.remove(entrance_a)
        entrances.remove(entrance_b)

    if multiworld.door_shuffle[player] == "simple":
        def connect_connecting_interiors(interior_exits, exterior_entrances):
            for interior, exterior in zip(interior_exits, exterior_entrances):
                for a, b in zip(interior, exterior):
                    entrance_a = multiworld.get_entrance(a, player)
                    if b is None:
                        #entrance_b = multiworld.get_entrance(entrances[0], player)
                        # should just be able to use the entrance_b from the previous link?
                        pass
                    else:
                        entrance_b = multiworld.get_entrance(b, player)
                        entrance_b.connect(entrance_a)
                        entrances.remove(entrance_b)
                    entrance_a.connect(entrance_b)
                    entrances.remove(entrance_a)

        def connect_interiors(interior_exits, exterior_entrances):
            for a, b in zip(interior_exits, exterior_entrances):
                if isinstance(a, list):
                    entrance_a = multiworld.get_entrance(a[0], player)
                else:
                    entrance_a = multiworld.get_entrance(a, player)
                entrance_b = multiworld.get_entrance(b, player)
                entrance_a.connect(entrance_b)
                entrance_b.connect(entrance_a)
                entrances.remove(entrance_b)
                entrances.remove(entrance_a)
                if isinstance(a, list):
                    entrance_a = multiworld.get_entrance(a[1], player)
                    entrance_a.connect(entrance_b)
                    entrances.remove(entrance_a)

        placed_connecting_interior_dungeons = safe_connecting_interior_dungeons + unsafe_connecting_interior_dungeons
        interior_dungeon_entrances = connecting_interior_dungeon_entrances.copy()

        placed_single_entrance_dungeons = dungeons.copy()
        single_entrance_dungeon_entrances = dungeon_entrances.copy()

        for i in range(2):
            if True or not multiworld.random.randint(0, 2):
                placed_connecting_interior_dungeons.append(multi_purpose_dungeons[i])
                interior_dungeon_entrances.append([multi_purpose_dungeon_entrances[i], None])
            else:
                placed_single_entrance_dungeons.append(multi_purpose_dungeons[i])
                single_entrance_dungeon_entrances.append(multi_purpose_dungeon_entrances[i])

        multiworld.random.shuffle(placed_connecting_interior_dungeons)
        while placed_connecting_interior_dungeons[0] in unsafe_connecting_interior_dungeons:
            multiworld.random.shuffle(placed_connecting_interior_dungeons)
        connect_connecting_interiors(placed_connecting_interior_dungeons, interior_dungeon_entrances)

        interiors = connecting_interiors.copy()
        multiworld.random.shuffle(interiors)
        while ((connecting_interiors[2] in (interiors[2], interiors[10], interiors[11])  # Dept Store at Dept Store
                                                                                         # or Rt 16 Gate S or N
                and (interiors[11] in connecting_interiors[13:17]  # Saffron Gate at Rt 16 Gate S
                     or interiors[12] in connecting_interiors[13:17]))  # Saffron Gate at Rt 18 Gate
                and interiors[15] in connecting_interiors[13:17]  # Saffron Gate at Rt 7 Gate
                and interiors[1] in connecting_interiors[13:17]  # Saffron Gate at Rt 7-8 Underground Path
                and (not multiworld.tea[player]) and multiworld.worlds[player].fly_map != "Celadon City"
                and multiworld.worlds[player].town_map_fly_map != "Celadon City"):
            multiworld.random.shuffle(interiors)

        connect_connecting_interiors(interiors, connecting_interior_entrances)
        placed_gyms = gyms.copy()
        multiworld.random.shuffle(placed_gyms)

        # Celadon Gym requires Cut access to reach the Gym Leader. There are some scenarios where its placement
        # could make badge placement impossible
        def celadon_gym_problem():
            # Badgesanity or no badges needed for HM moves means gyms can go anywhere
            if multiworld.badgesanity[player] or not multiworld.badges_needed_for_hm_moves[player]:
                return False

            # Celadon Gym in Pewter City and need one or more badges for Viridian City gym.
            # No gym leaders would be reachable.
            if gyms[3] == placed_gyms[0] and multiworld.viridian_gym_condition[player] > 0:
                return True

            # Celadon Gym not on Cinnabar Island or can access Viridian City gym with one badge
            if not gyms[3] == placed_gyms[6] and multiworld.viridian_gym_condition[player] > 1:
                return False

            # At this point we need to see if we can get beyond Pewter/Cinnabar with just one badge

            # Can get Fly access from Pewter City gym and fly beyond Pewter/Cinnabar
            if multiworld.worlds[player].fly_map not in ("Pallet Town", "Viridian City", "Cinnabar Island",
                    "Indigo Plateau") and multiworld.worlds[player].town_map_fly_map not in ("Pallet Town",
                    "Viridian City", "Cinnabar Island", "Indigo Plateau"):
                return False

            # Route 3 condition is boulder badge but Mt Moon entrance leads to safe dungeons or Rock Tunnel
            if multiworld.route_3_condition[player] == "boulder_badge" and placed_connecting_interior_dungeons[2] not \
                    in (unsafe_connecting_interior_dungeons[0], unsafe_connecting_interior_dungeons[2]):
                return False

            # Route 3 condition is Defeat Brock and he is in Pewter City, or any other condition besides Boulder Badge.
            # Any badge can land in Pewter City, so the only problematic dungeon at Mt Moon is Seafoam Islands since
            # it requires two badges
            if (((multiworld.route_3_condition[player] == "defeat_brock" and gyms[0] == placed_gyms[0])
                    or multiworld.route_3_condition[player] not in ("defeat_brock", "boulder_badge"))
                    and placed_connecting_interior_dungeons[2] != unsafe_connecting_interior_dungeons[0]):
                return False

            # If dungeon at Diglett's Cave does not require a badge, we can get Cut access and make it through
            if placed_connecting_interior_dungeons[1] in safe_connecting_interior_dungeons:
                return False

            # If dungeon at Seafoam Islands does not require a badge, we can get Surf access and make it through
            if placed_connecting_interior_dungeons[3] in safe_connecting_interior_dungeons:
                return False

            # No apparent way to proceed, reshuffle
            return True

        # Also check for a very specific situation where Brock or vending machines are needed to access
        # Cerulean City, but they are placed in Cerulean City
        def cerulean_city_problem():
            if (gyms[0] == placed_gyms[1]  # Pewter Gym in Cerulean City
                    and interiors[0] in connecting_interiors[13:17]  # Saffron Gate at Underground Path North South
                    and interiors[13] in connecting_interiors[13:17]  # Saffron Gate at Route 5 Saffron Gate
                    and multi_purpose_dungeons[0] == placed_connecting_interior_dungeons[4]  # Pokémon Mansion at Rock Tunnel, which is
                    and (not multiworld.tea[player])                       # not traversable backwards
                    and multiworld.route_3_condition[player] == "defeat_brock"
                    and multiworld.worlds[player].fly_map != "Cerulean City"
                    and multiworld.worlds[player].town_map_fly_map != "Cerulean City"):
                return True

        while celadon_gym_problem() or cerulean_city_problem():
            multiworld.random.shuffle(placed_gyms)

        connect_interiors(placed_gyms, gym_entrances)

        multiworld.random.shuffle(placed_single_entrance_dungeons)
        while dungeons[4] == placed_single_entrance_dungeons[0]:  # Pokémon Tower at Silph Co
            multiworld.random.shuffle(placed_single_entrance_dungeons)
        connect_interiors(placed_single_entrance_dungeons, single_entrance_dungeon_entrances)

        remaining_entrances = [entrance for entrance in entrances if outdoor_map(entrance.parent_region.name)]
        multiworld.random.shuffle(remaining_entrances)
        remaining_interiors = [entrance for entrance in entrances if entrance not in remaining_entrances]
        for entrance_a, entrance_b in zip(remaining_entrances, remaining_interiors):
            entrance_a.connect(entrance_b)
            entrance_b.connect(entrance_a)
    elif multiworld.door_shuffle[player]:
        if multiworld.door_shuffle[player] == "full":
            loop_out_interiors = [[multiworld.get_entrance(e[0], player), multiworld.get_entrance(e[1], player)] for e
                                  in multiworld.random.sample(unsafe_connecting_interior_dungeons
                                                              + safe_connecting_interior_dungeons, 2)]
            entrances.remove(loop_out_interiors[0][1])
            entrances.remove(loop_out_interiors[1][1])
        if not multiworld.badgesanity[player]:
            badges = [item for item in self.item_pool if "Badge" in item.name]
            for badge in badges:
               self.item_pool.remove(badge)
            badge_locs = []
            for loc in ["Pewter Gym - Brock Prize", "Cerulean Gym - Misty Prize", "Vermilion Gym - Lt. Surge Prize",
                        "Celadon Gym - Erika Prize", "Fuchsia Gym - Koga Prize", "Saffron Gym - Sabrina Prize",
                        "Cinnabar Gym - Blaine Prize", "Viridian Gym - Giovanni Prize"]:
                badge_locs.append(multiworld.get_location(loc, player))
            multiworld.random.shuffle(badges)
            while badges[3].name == "Cascade Badge" and multiworld.badges_needed_for_hm_moves[player]:
                multiworld.random.shuffle(badges)
            for badge, loc in zip(badges, badge_locs):
                loc.place_locked_item(badge)

        state = multiworld.state.copy()
        for item, data in item_table.items():
            if (data.id or item in poke_data.pokemon_data) and data.classification == ItemClassification.progression \
                    and ("Badge" not in item or multiworld.badgesanity[player]):
                state.collect(self.create_item(item))

        multiworld.random.shuffle(entrances)
        reachable_entrances = []

        relevant_events = [
            "Boulder Badge",
            "Cascade Badge",
            "Thunder Badge",
            "Rainbow Badge",
            "Soul Badge",
            "Marsh Badge",
            "Volcano Badge",
            "Earth Badge",
            "Seafoam Exit Boulder",
            "Victory Road Boulder",
            "Silph Co Liberated",
        ]
        if multiworld.robbed_house_officer[player]:
            relevant_events.append("Help Bill")
        if multiworld.tea[player]:
            relevant_events.append("Vending Machine Drinks")
        if multiworld.route_3_condition[player] == "defeat_brock":
            relevant_events.append("Defeat Brock")
        elif multiworld.route_3_condition[player] == "defeat_any_gym":
            relevant_events += [
                "Defeat Brock",
                "Defeat Misty",
                "Defeat Lt. Surge",
                "Defeat Erika",
                "Defeat Koga",
                "Defeat Sabrina",
                "Defeat Blaine",
                "Defeat Viridian Gym Giovanni",
            ]

        event_locations = self.multiworld.get_filled_locations(player)

        def adds_reachable_entrances(entrances_copy, item, dead_end_cache):
            ret = dead_end_cache.get(item.name)
            if (ret != None):
                return ret

            state_copy = state.copy()
            state_copy.collect(item, True)
            state.sweep_for_events(locations=event_locations)
            ret = len([entrance for entrance in entrances_copy if entrance in reachable_entrances or
                      entrance.parent_region.can_reach(state_copy)]) > len(reachable_entrances)
            dead_end_cache[item.name] = ret
            return ret

        def dead_end(entrances_copy, e, dead_end_cache):
            region = e.parent_region
            check_warps = set()
            checked_regions = {region}
            check_warps.update(region.exits)
            check_warps.remove(e)
            for location in region.locations:
                if location.item and location.item.name in relevant_events and \
                                 adds_reachable_entrances(entrances_copy, location.item, dead_end_cache):
                    return False
            while check_warps:
                warp = check_warps.pop()
                warp = warp
                if warp not in reachable_entrances:
                    if "Rock Tunnel" not in warp.name or logic.rock_tunnel(state, player):
                        # confirm warp is in entrances list to ensure it's not a loop-out interior
                        if warp.connected_region is None and warp in entrances_copy:
                            return False
                        elif (isinstance(warp, PokemonRBWarp) and ("Rock Tunnel" not in warp.name or
                                logic.rock_tunnel(state, player))) or warp.access_rule(state):
                            if warp.connected_region and warp.connected_region not in checked_regions:
                                checked_regions.add(warp.connected_region)
                                check_warps.update(warp.connected_region.exits)
                                for location in warp.connected_region.locations:
                                    if (location.item and location.item.name in relevant_events and
                                            adds_reachable_entrances(entrances_copy, location.item, dead_end_cache)):
                                        return False
            return True

        starting_entrances = len(entrances)
        dc_connected = []
        rock_tunnel_entrances = [entrance for entrance in entrances if "Rock Tunnel" in entrance.name]
        entrances = [entrance for entrance in entrances if entrance not in rock_tunnel_entrances]
        while entrances:
            state.update_reachable_regions(player)
            state.sweep_for_events(locations=event_locations)

            if rock_tunnel_entrances and logic.rock_tunnel(state, player):
                entrances += rock_tunnel_entrances
                rock_tunnel_entrances = None

            reachable_entrances = [entrance for entrance in entrances if entrance in reachable_entrances or
                                   entrance.parent_region.can_reach(state)]
            assert reachable_entrances, \
                "Ran out of reachable entrances in Pokemon Red and Blue door shuffle"
            multiworld.random.shuffle(entrances)
            if multiworld.door_shuffle[player] == "decoupled" and len(entrances) == 1:
                entrances += dc_connected
                entrances[-1].connect(entrances[0])
                while len(entrances) > 1:
                    entrances.pop(0).connect(entrances[0])
                break
            if multiworld.door_shuffle[player] == "full" or len(entrances) != len(reachable_entrances):
                entrances.sort(key=lambda e: e.name not in entrance_only)

                dead_end_cache = {}

                # entrances list is empty while it's being sorted, must pass a copy to iterate through
                entrances_copy = entrances.copy()
                if multiworld.door_shuffle[player] == "decoupled":
                    entrances.sort(key=lambda e: 1 if e.connected_region is not None else 2 if e not in
                                   reachable_entrances else 0)
                    assert entrances[0].connected_region is None,\
                        "Ran out of valid reachable entrances in Pokemon Red and Blue door shuffle"
                elif len(reachable_entrances) > (1 if multiworld.door_shuffle[player] == "insanity" else 8) and len(
                        entrances) <= (starting_entrances - 3):
                    entrances.sort(key=lambda e: 0 if e in reachable_entrances else 2 if
                                   dead_end(entrances_copy, e, dead_end_cache) else 1)
                else:
                    entrances.sort(key=lambda e: 0 if e in reachable_entrances else 1 if
                                   dead_end(entrances_copy, e, dead_end_cache) else 2)
                if multiworld.door_shuffle[player] == "full":
                    outdoor = outdoor_map(entrances[0].parent_region.name)
                    if len(entrances) < 48 and not outdoor:
                        # Prevent a situation where the only remaining outdoor entrances are ones that cannot be reached
                        # except by connecting directly to it.
                        entrances.sort(key=lambda e: e.name in unreachable_outdoor_entrances)

                    entrances.sort(key=lambda e: outdoor_map(e.parent_region.name) != outdoor)
                assert entrances[0] in reachable_entrances, \
                    "Ran out of valid reachable entrances in Pokemon Red and Blue door shuffle"
            if (multiworld.door_shuffle[player] == "decoupled" and len(reachable_entrances) > 8 and len(entrances)
                    <= (starting_entrances - 3)):
                entrance_b = entrances.pop(1)
            else:
                entrance_b = entrances.pop()
            entrance_a = entrances.pop(0)
            entrance_a.connect(entrance_b)
            if multiworld.door_shuffle[player] == "decoupled":
                entrances.append(entrance_b)
                dc_connected.append(entrance_a)
            else:
                entrance_b.connect(entrance_a)

        if multiworld.door_shuffle[player] == "full":
            for pair in loop_out_interiors:
                pair[1].connected_region = pair[0].connected_region
                pair[1].parent_region.entrances.append(pair[0])
                pair[1].target = pair[0].target

    if multiworld.door_shuffle[player]:
        for region in multiworld.get_regions(player):
            checked_regions = {region}

            def check_region(region_to_check):
                if "Safari Zone" not in region_to_check.name and outdoor_map(region_to_check.name):
                    return True
                for entrance in region_to_check.entrances:
                    if entrance.parent_region not in checked_regions:
                        checked_regions.add(entrance.parent_region)
                        x = check_region(entrance.parent_region)
                        if x is True:
                            return entrance.name.split(" to ")[1].split("-")[0]
                        elif x is not None:
                            return x
                return None

            if region.name.split("-")[0] not in map_ids or ("Safari Zone" not in region.name and
                                                            outdoor_map(region.name)):
                region.entrance_hint = None
            else:
                region.entrance_hint = check_region(region)


def connect(world: MultiWorld, player: int, source: str, target: str, rule: callable = lambda state: True,
            one_way=False, name=None):
    source_region = world.get_region(source, player)
    target_region = world.get_region(target, player)

    if name is None:
        name = source + " to " + target

    connection = Entrance(
        player,
        name,
        source_region
    )

    connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)
    if not one_way:
        connect(world, player, target, source, rule, True)


class PokemonRBWarp(Entrance):
    def __init__(self, player, name, parent, warp_id, address, flags):
        super().__init__(player, name, parent)
        self.warp_id = warp_id
        self.address = address
        self.flags = flags

    def connect(self, entrance):
        super().connect(entrance.parent_region, None, target=entrance.warp_id)

    def access_rule(self, state):
        if self.connected_region is None:
            return False
        if "Rock Tunnel" in self.parent_region.name or "Rock Tunnel" in self.connected_region.name:
            return logic.rock_tunnel(state, self.player)
        return True


class PokemonRBRegion(Region):
    def __init__(self, name, player, multiworld):
        super().__init__(name, player, multiworld)
        self.distance = None
