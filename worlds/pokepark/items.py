from BaseClasses import Item

class PokeparkItem(Item):
    game: str = "PokePark"

FRIENDSHIP_ITEMS: dict[str, int] = {
    #Meadow Zone
    "Chikorita": 1,
    "Pachirisu": 2,
    "Bulbasaur": 3,
    "Munchlax": 4,
    "Tropius": 5,
    "Turtwig": 6,
    "Bonsly": 7,
    "Sudowoodo": 8,
    "Buneary": 9,
    "Shinx": 10,
    "Mankey": 11,
    "Spearow": 12,
    "Croagunk": 13,
    "Chatot": 14,
    "Lotad": 15,
    "Treecko": 16,
    "Caterpie": 17,
    "Butterfree": 18,
    "Chimchar": 19,
    "Aipom": 20,
    "Ambipom": 21,
    "Weedle": 22,
    "Shroomish": 23,
    "Magikarp": 24,
    "Oddish": 25,
    "Leafeon": 26,
    "Bidoof": 27,
    "Bibarel": 28,
    "Torterra": 29,
    "Starly": 30,
    "Scyther":31,

    # Beach Zone
    "Buizel":32,
    "Psyduck":33,
    "Slowpoke":34,
    "Azurill": 35,
    "Totodile":36,
    "Mudkip":37,
    "Pidgeotto":38,
    "Taillow":39,
    "Wingull":40,
    "Staravia":41,
    "Corsola":42,
    "Floatzel":43,
    "Vaporeon":44,
    "Golduck":45,
    "Pelipper":46,
    "Sharpedo":47,
    "Wynaut": 48,
    "Carvanha": 49,
    "Krabby":50,
    "Wailord":51,
    "Corphish":52,
    "Gyarados":53,
    "Feraligatr":54,
    "Piplup": 55,

    #Treehouse
    "Burmy": 56,
    "Drifblim":57,

    # Ice Zone
    "Lapras": 58,
    "Spheal":59,
    "Octillery":60,
    "Teddiursa": 61,
    "Delibird": 62,
    "Smoochum":63,
    "Squirtle":64,
    "Glaceon":65,
    "Prinplup":66,
    "Sneasel":67,
    "Piloswine":68,
    "Glalie":69,
    "Froslass":70,
    "Primeape":71,
    "Ursaring":72,
    "Mamoswine":73,
    "Kirlia":74,
    "Quagsire":75,
    "Empoleon":76,

    # Cavern Zone
    "Magnemite":77,
    "Geodude": 78,
    "Torchic":79,
    "Machamp":80,
    "Meowth":81,
    "Zubat":82,
    "Cranidos":83,
    "Scizor":84,
    "Mawile":85,
    "Marowak":86,
    "Mr. Mime":87,
    "Aron":88,
    "Dugtrio":89,
    "Gible":90,
    "Magnezone": 91,
    "Diglett": 92,
    "Phanpy":93,
    "Raichu":94,
    "Golbat":95,
    "Bastiodon":96,

    # Magma Zone
    "Camerupt": 97,
    "Magby": 98,
    "Vulpix":99,
    "Ninetales": 100,
    "Quilava": 101,
    "Flareon": 102,
    "Meditite" : 103,
    "Infernape": 104,
    "Farfetch'd": 105,
    "Magcargo": 106,
    "Charmander": 107,
    "Ponyta": 108,
    "Torkoal": 109,
    "Golem": 110,
    "Rhyperior": 111,
    "Baltoy": 112,
    "Claydol": 113,
    "Hitmonchan": 114,
    "Hitmontop": 115,

    # Meadow Zone
    "Venusaur": 116,

    # Treehouse
    "Mime Jr.": 117,

    # Cavern Zone
    "Hitmonlee": 118,

    # Haunted Zone
    "Drifloon": 119,
    "Murkrow": 120,
    "Honchkrow":121,
    "Gliscor": 122,
    "Metapod": 123,
    "Kakuna": 124,

    # Haunted Zone Mansion
    "Duskull": 125,
    "Sableye": 126,
    "Misdreavus": 127,
    "Pichu": 128,
    "Umbreon": 129,
    "Spinarak": 130,
    "Abra": 131,
    "Riolu": 132,
    "Voltorb": 133,
    "Elekid": 134,
    "Electabuzz": 135,
    "Luxray": 136,
    "Stunky": 137,
    "Skuntank": 138,
    "Breloom": 139,
    "Mismagius": 140,
    "Electrode": 141,
    "Haunter": 142,
    "Gastly":143,
    "Dusknoir": 144,
    "Espeon":145,
    #Haunted Zone
    "Tangrowth": 146,

    # Haunted Zone Mansion
    "Gengar": 147,
}

UNLOCK_ITEMS: dict[str,int] = {
    "Tropius Unlock": 1000,
    "Pachirisu Unlock": 2000,
    "Bonsly Unlock": 3000,
    "Sudowoodo Unlock": 4000,
    "Lotad Unlock": 5000,
    "Shinx Unlock": 6000,
    "Scyther Unlock": 7000,
    "Caterpie Unlock": 8000,
    "Butterfree Unlock": 9000,
    "Chimchar Unlock": 10000,
    "Ambipom Unlock": 11000,
    "Weedle Unlock": 12000,
    "Shroomish Unlock": 13000,
    "Magikarp Unlock": 14000,
    "Bidoof Unlock": 15000,
    "Bidoof Unlock 2": 16000,
    "Bidoof Unlock 3": 17000,
    "Bibarel Unlock": 18000,
    "Starly Unlock": 19000,
    "Starly Unlock 2": 20000,
    "Torterra Unlock": 21000,

    # Beach Zone
    "Floatzel Unlock": 22000,
    "Mudkip Unlock": 23000,
    "Totodile Unlock": 24000,
    "Golduck Unlock": 25000,
    "Krabby Unlock": 26000,
    "Corphish Unlock": 27000,

    #Misc
    "Pikachu Balloon": 28000,
    "Pikachu Surfboard": 29000,
    "Pikachu Snowboard": 30000,
    "Drifblim Unlock": 31000,

    #Ice Zone
    "Delibird Unlock": 32000,
    "Squirtle Unlock": 33000,
    "Smoochum Unlock": 34000,
    "Sneasel Unlock": 35000,
    "Mamoswine Unlock": 36000,
    "Glalie Unlock": 37000,
    "Primeape Unlock": 38000,
    "Ursaring Unlock":39000,

    # Cavern Zone
    "Magnemite Unlock": 40000,
    "Machamp Unlock": 41000,
    "Magnemite Unlock 2": 42000,
    "Diglett Unlock": 43000,
    "Magnemite Unlock 3": 44000,
    "Magnezone Unlock": 45000,
    "Phanpy Unlock": 46000,
    "Raichu Unlock": 47000,

    # Magma Zone
    "Infernape Unlock": 48000,
    "Ninetales Unlock": 49000,
    "Ponyta Unlock": 50000,
    "Torkoal Unlock": 51000,
    "Golem Unlock": 52000,
    "Baltoy Unlock": 53000,
    "Claydol Unlock": 54000,
    "Hitmonchan Unlock": 55000,
    "Hitmonlee Unlock": 56000,

    # Haunted Zone
    "Honchkrow Unlock": 57000,
    "Metapod Unlock": 58000,
    "Kakuna Unlock": 59000,

    # Haunted Zone Mansion
    "Voltorb Unlock": 60000,
    "Elekid Unlock": 61000,
    "Electabuzz Unlock": 62000,
    "Luxray Unlock": 63000,
    "Stunky Unlock": 64000,
    "Skuntank Unlock": 65000,
    "Breloom Unlock": 66000,
    "Mismagius Unlock": 67000,
    "Electrode Unlock": 68000,
    "Haunter Unlock": 69000,
    "Gastly Unlock": 70000,
    "Gastly Unlock 2": 71000,
    "Dusknoir Unlock": 72000,
    "Espeon Unlock": 73000,
    "Gengar Unlock": 74000
}

BERRIES: dict[str,int] = {
    "10 Berries": 100000, #Location usage for quests
    "20 Berries": 200000,
    "50 Berries": 300000,
    "100 Berries": 400000 # Location usage for minigames
}

PRISM_ITEM: dict[str,int] = {
    "Bulbasaur Prisma": 1000000,
    "Venusaur Prisma": 2000000,
    "Pelipper Prisma": 3000000,
    "Gyarados Prisma": 4000000,
    "Empoleon Prisma": 5000000,
    "Bastiodon Prisma": 6000000,
    "Rhyperior Prisma": 7000000,
    "Blaziken Prisma": 8000000,
    "Tangrowth Prisma": 9000000,
    "Dusknoir Prisma": 9000001,
    "Rotom Prisma": 9000002

}

POWERS: dict[str,int] = {
    "Progressive Thunderbolt": 10000000,
    "Progressive Dash": 20000000,
    "Progressive Health": 30000000,
    "Progressive Iron Tail": 40000000
}

REGION_UNLOCK: dict[str,int] = {
    "Meadow Zone Unlock": 99999,
    "Beach Zone Unlock": 99998,
    "Ice Zone Unlock": 99997,
    "Cavern Zone & Magma Zone Unlock": 99996,
    "Haunted Zone Unlock": 99995,


}

ALL_ITEMS_TABLE: dict[str, int] = {
    **FRIENDSHIP_ITEMS,
    **UNLOCK_ITEMS,
    **BERRIES,
    **PRISM_ITEM,
    **POWERS,
    **REGION_UNLOCK
}