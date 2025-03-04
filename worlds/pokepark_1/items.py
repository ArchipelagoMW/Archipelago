from BaseClasses import Item

class PokeparkItem(Item):
    game: str = "PokéPark"

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
    "Empoleon":76

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

    #Ice Zone
    "Delibird Unlock": 31000,
    "Squirtle Unlock": 32000,
    "Smoochum Unlock": 33000,
    "Sneasel Unlock": 34000,
    "Mamoswine Unlock": 35000,
    "Glalie Unlock": 36000,
    "Primeape Unlock": 37000,
    "Ursaring Unlock":38000

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
    "Empoleon Prisma": 5000000

}

POWERS: dict[str,int] = {
    "Progressive Thunderbolt": 10000000,
    "Progressive Dash": 20000000,
    "Progressive Health": 30000000,
    "Progressive Iron Tail": 40000000
}

REGION_UNLOCK: dict[str,int] = {
    # Beach Zone Unlock
    "Beach Zone Unlock": 99999,
    "Ice Zone Unlock": 88888
}

ALL_ITEMS_TABLE: dict[str, int] = {
    **FRIENDSHIP_ITEMS,
    **UNLOCK_ITEMS,
    **BERRIES,
    **PRISM_ITEM,
    **POWERS,
    **REGION_UNLOCK
}