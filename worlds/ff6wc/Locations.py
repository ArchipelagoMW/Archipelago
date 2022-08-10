terra_checks = {
    'Whelk': 1,
    'Lete River': 2,
    'Sealed Gate': 3,
    'Zozo': 4,
    'Mobliz': 5
}

locke_checks = {
    'South Figaro Cave': 6,
    'Narshe Weapon Shop 1': 7,
    "Narshe Weapon Shop 2": 8,
    'Phoenix Cave': 9,
    'Red Dragon': 10,
    "Red Dragon Status": 11
}

cyan_checks = {
    'Doma Castle Siege': 12,
    'Dream Stooges': 13,
    'Wrexsoul': 14,
    'Doma Castle Throne': 15,
    'Mt. Zozo': 16,
    'Storm Dragon': 17,
    "Storm Dragon Status": 18
}

shadow_checks = {
    'Gau Father House': 19,
    'Imperial Air Force': 20,
    'AtmaWeapon': 21,
    'Nerapa': 22,
    'Veldt Cave': 23
}

edgar_checks = {
    'Figaro Castle Throne': 24,
    'Figaro Castle Basement': 25,
    'Ancient Castle': 26,
    'Blue Dragon': 27,
    "Blue Dragon Status": 28
}

sabin_checks = {
    'Mt. Kolts': 29,
    'Collapsing House': 30,
    'Baren Falls': 31,
    'Imperial Camp': 32,
    'Phantom Train': 33
}

celes_checks = {
    'South Figaro': 34,
    'Ifrit and Shiva': 35,
    'Number 024': 36,
    'Cranes': 37,
    'Opera House': 38
}

strago_checks = {
    'Burning House': 39,
    "Ebot's Rock": 40,
    'MagiMaster': 41,
    'Gem Box': 42
}

relm_checks = {
    'Esper Mountain': 43,
    "Owzer Mansion": 44
}

setzer_checks = {
    'Kohlingen': 45,
    "Daryl's Tomb": 46
}

mog_checks = {
    'Lone Wolf 1': 47,
    "Lone Wolf 2": 48
}

gau_checks = {
    'Veldt': 49,
    'Serpent Trench': 50
}

gogo_checks = {
    "Gogo's Cave": 51
}

umaro_checks = {
    "Umaro's Cave": 52
}

generic_checks = {
    'Kefka at Narshe': 53,
    'Tzen Thief': 54,
    'Doom Gaze': 55,
    'Tritoch': 56,
    'Auction House 10kGP': 57,
    'Auction House 20kGP': 58,
    'Dirt Dragon': 59,
    'White Dragon': 60,
    'Ice Dragon': 61,
    "Dirt Dragon Status": 62,
    "White Dragon Status": 63,
    "Ice Dragon Status": 64
}

kefka_checks = {
    'Atma': 65,
    "Skull Dragon": 66,
    "Gold Dragon": 67,
    "Skull Dragon Status": 68,
    "Gold Dragon Status": 69
}

accomplishment_data = {
    "Kefka's Tower": 70,
    'Beat Final Kefka': 71

}

dragon_events = [
    "Red Dragon Status",
    "Storm Dragon Status",
    "Blue Dragon Status",
    "Dirt Dragon Status",
    "White Dragon Status",
    "Ice Dragon Status",
    "Skull Dragon Status",
    "Gold Dragon Status"
]

dragon_events_link = {
    "Red Dragon": "Red Dragon Status",
    "Storm Dragon": "Storm Dragon Status",
    "Blue Dragon": "Blue Dragon Status",
    "Dirt Dragon": "Dirt Dragon Status",
    "White Dragon": "White Dragon Status",
    "Ice Dragon": "Ice Dragon Status",
    "Skull Dragon": "Skull Dragon Status",
    "Gold Dragon": "Gold Dragon Status"
}

location_table = {
    **terra_checks, **locke_checks, **cyan_checks, **shadow_checks, **edgar_checks, **sabin_checks, **celes_checks,
    **strago_checks, **relm_checks, **setzer_checks, **mog_checks, **gau_checks, **gogo_checks, **umaro_checks,
    **kefka_checks, **generic_checks, **accomplishment_data
}

dragons = ["Red Dragon", "Storm Dragon", "Blue Dragon", "Dirt Dragon",
           "White Dragon", "Ice Dragon", "Skull Dragon", "Gold Dragon"]
# Most checks are either character/esper/item, esper/item, or item.
# Except for Cranes, Magimaster, Imperial Air Force, AtmaWeapon, Veldt
# Most are the first one, so we only need to note the exceptions
item_only_checks = list(dragons)
item_only_checks.extend(("Narshe Weapon Shop 2", "Gem Box", "Atma"))
no_item_checks = ["Cranes", "MagiMaster", "Imperial Air Force", "AtmaWeapon", "Veldt"]
no_character_checks = ["Auction House 10kGP", "Auction House 20kGP", "Wrexsoul", "Doma Castle Throne",
                       "Doom Gaze", "Nerapa", "Ifrit and Shiva", "Number 024", "Narshe Weapon Shop 1",
                       "Tritoch", "Tzen Thief"]
