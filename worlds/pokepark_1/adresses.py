from worlds.pokepark_1 import FRIENDSHIP_ITEMS, UNLOCK_ITEMS, BERRIES
from worlds.pokepark_1.items import PRISM_ITEM, POWERS, REGION_UNLOCK

prisma_location_checks = [
    # Prismas
    # Bulbasaur Prisma
    (0x80377e1c + 0x7fff + 0x0003, 0x03, PRISM_ITEM["Bulbasaur Prisma"]),
    # Venusaur Prisma
    (0x80376DA8 + 0x7fff + 0x0003, 0x03, PRISM_ITEM["Venusaur Prisma"]),
    # Pelipper Prisma
    (0x803772B8 + 0x7fff + 0x0003, 0x03, PRISM_ITEM["Pelipper Prisma"]),
    # Gyarados Prisma
    (0x80377174 + 0x7fff + 0x0003, 0x03, PRISM_ITEM["Gyarados Prisma"]),
]
beach_zone_friendship_checks = [
# Beach Zone
    # Buizel
    (0x803755d0+ 0x0001,0x80, FRIENDSHIP_ITEMS["Buizel"]),
    (0x803755d0 + 0x000c, 0x80, FRIENDSHIP_ITEMS["Buizel"]),

    #Psyduck
    (0x803755F8 + 0x0001, 0x80, FRIENDSHIP_ITEMS["Psyduck"]),
    (0x803755F8 + 0x000c, 0x80, FRIENDSHIP_ITEMS["Psyduck"]),

    # Slowpoke
    (0x803755BC + 0x0001, 0x80, FRIENDSHIP_ITEMS["Slowpoke"]),
    (0x803755BC + 0x000c, 0x80, FRIENDSHIP_ITEMS["Slowpoke"]),

    # Azurill
    (0x80375558 + 0x0001, 0x80, FRIENDSHIP_ITEMS["Azurill"]),
    (0x80375558 + 0x000c, 0x80, FRIENDSHIP_ITEMS["Azurill"]),

    # Totodile
    (0x80375670 + 0x0001, 0x80, FRIENDSHIP_ITEMS["Totodile"]),
    (0x80375670 + 0x000c, 0x80, FRIENDSHIP_ITEMS["Totodile"]),

    # Mudkip
    (0x8037556C + 0x0001, 0x80, FRIENDSHIP_ITEMS["Mudkip"]),
    (0x8037556C + 0x000c, 0x80, FRIENDSHIP_ITEMS["Mudkip"]),
    # Pidgeotto
    (0x80375634 + 0x0001, 0x80, FRIENDSHIP_ITEMS["Pidgeotto"]),
    (0x80375634 + 0x000c, 0x80, FRIENDSHIP_ITEMS["Pidgeotto"]),
    # Taillow
    (0x80375620 + 0x0001, 0x80, FRIENDSHIP_ITEMS["Taillow"]),
    (0x80375620 + 0x000c, 0x80, FRIENDSHIP_ITEMS["Taillow"]),
    # Wingull
    (0x803756ac + 0x0001, 0x80, FRIENDSHIP_ITEMS["Wingull"]),
    (0x803756ac + 0x000c, 0x80, FRIENDSHIP_ITEMS["Wingull"]),
    # Starly
    (0x80375364 + 0x0001, 0x80, FRIENDSHIP_ITEMS["Starly"]+1000),
    (0x80375364 + 0x000c, 0x80, FRIENDSHIP_ITEMS["Starly"]+1000),
    # Staravia
    (0x80375378 + 0x0001, 0x80, FRIENDSHIP_ITEMS["Staravia"]),
    (0x80375378 + 0x000c, 0x80, FRIENDSHIP_ITEMS["Staravia"]),

    # Corsola
    (0x803755A8 + 0x0001, 0x80, FRIENDSHIP_ITEMS["Corsola"]),
    (0x803755A8 + 0x000c, 0x80, FRIENDSHIP_ITEMS["Corsola"]),
    # Floatzel
    (0x803755E4 + 0x0001, 0x80, FRIENDSHIP_ITEMS["Floatzel"]),
    (0x803755E4 + 0x000c, 0x80, FRIENDSHIP_ITEMS["Floatzel"]),
    # Vaporeon
    (0x803754E0 + 0x0001, 0x80, FRIENDSHIP_ITEMS["Vaporeon"]),
    (0x803754E0 + 0x000c, 0x80, FRIENDSHIP_ITEMS["Vaporeon"]),
    # Golduck
    (0x8037560C + 0x0001, 0x80, FRIENDSHIP_ITEMS["Golduck"]),
    (0x8037560C + 0x000c, 0x80, FRIENDSHIP_ITEMS["Golduck"]),
    # Pelipper
    (0x803756C0 + 0x0001, 0x80, FRIENDSHIP_ITEMS["Pelipper"]),
    (0x803756C0 + 0x000c, 0x80, FRIENDSHIP_ITEMS["Pelipper"]),

    # Krabby
    (0x80375580 + 0x0001, 0x80, FRIENDSHIP_ITEMS["Krabby"]),
    (0x80375580 + 0x000c, 0x80, FRIENDSHIP_ITEMS["Krabby"]),
    # Wailord
    (0x803760ac + 0x0001, 0x80, FRIENDSHIP_ITEMS["Wailord"]),
    (0x803760ac + 0x000c, 0x80, FRIENDSHIP_ITEMS["Wailord"]),

    # Corphish
    (0x80375594 + 0x0001, 0x80, FRIENDSHIP_ITEMS["Corphish"]),
    (0x80375594 + 0x000c, 0x80, FRIENDSHIP_ITEMS["Corphish"]),

    # Gyarados
    (0x803756E8 + 0x0001, 0x80, FRIENDSHIP_ITEMS["Gyarados"]),
    (0x803756E8 + 0x000c, 0x80, FRIENDSHIP_ITEMS["Gyarados"]),

    # Feraligatr
    (0x80375684 + 0x0001, 0x80, FRIENDSHIP_ITEMS["Feraligatr"]),
    (0x80375684 + 0x000c, 0x80, FRIENDSHIP_ITEMS["Feraligatr"]),
]
meadow_zone_friendship_location_checks = [

    #Friendships  #+c is best friend address in future maybe used for seperate locations/items
    # Chikorita
    (0x80375C74+0x0001, 0x80, FRIENDSHIP_ITEMS["Chikorita"]),
    (0x80375C74+0x000c, 0x80, FRIENDSHIP_ITEMS["Chikorita"]),

    # Pachirisu
    (0x80375210+0x0001, 0x80, FRIENDSHIP_ITEMS["Pachirisu"]),
    (0x80375210+0x000c, 0x80, FRIENDSHIP_ITEMS["Pachirisu"]),

    # Bulbasaur
    (0x80375490+0x0001, 0x80, FRIENDSHIP_ITEMS["Bulbasaur"]),
    (0x80375490+0x000c, 0x80, FRIENDSHIP_ITEMS["Bulbasaur"]),

    # Munchlax
    (0x8037529C+0x0001, 0x80, FRIENDSHIP_ITEMS["Munchlax"]),
    (0x8037529C+0x000c, 0x80, FRIENDSHIP_ITEMS["Munchlax"]),

    # Tropius
    (0x803753DC+0x0001, 0x80, FRIENDSHIP_ITEMS["Tropius"]),
    (0x803753DC+0x000c, 0x80, FRIENDSHIP_ITEMS["Tropius"]),

    # Turtwig
    (0x803751D4+0x0001, 0x80, FRIENDSHIP_ITEMS["Turtwig"]),
    (0x803751D4+0x000c, 0x80, FRIENDSHIP_ITEMS["Turtwig"]),

    # Bonsly
    (0x803752C4+0x0001, 0x80, FRIENDSHIP_ITEMS["Bonsly"]),
    (0x803752C4+0x000c, 0x80, FRIENDSHIP_ITEMS["Bonsly"]),

    # Sudowoodo
    (0x803752D8+0x0001, 0x80, FRIENDSHIP_ITEMS["Sudowoodo"]),
    (0x803752D8+0x000c, 0x80, FRIENDSHIP_ITEMS["Sudowoodo"]),

    # Buneary
    (0x8037533C+0x0001, 0x80, FRIENDSHIP_ITEMS["Buneary"]),
    (0x8037533C+0x000c, 0x80, FRIENDSHIP_ITEMS["Buneary"]),

    # Shinx
    (0x803753F0+0x0001, 0x80, FRIENDSHIP_ITEMS["Shinx"]),
    (0x803753F0+0x000c, 0x80, FRIENDSHIP_ITEMS["Shinx"]),

    # Mankey
    # (0x80375314+0x0001,0x80, FRIENDSHIP_ITEMS["Mankey"]),

    # Spearow
    (0x803753C8+0x0001, 0x80, FRIENDSHIP_ITEMS["Spearow"]),
    (0x803753C8+0x000c, 0x80, FRIENDSHIP_ITEMS["Spearow"]),

    # Croagunk
    (0x8037547C+0x0001, 0x80, FRIENDSHIP_ITEMS["Croagunk"]),
    (0x8037547C+0x000c, 0x80, FRIENDSHIP_ITEMS["Croagunk"]),

    # Chatot
    (0x80376034+0x0001, 0x80, FRIENDSHIP_ITEMS["Chatot"]),
    (0x80376034+0x000c, 0x80, FRIENDSHIP_ITEMS["Chatot"]),

    # Lotad
    (0x80375224+0x0001, 0x80, FRIENDSHIP_ITEMS["Lotad"]),
    (0x80375224+0x000c, 0x80, FRIENDSHIP_ITEMS["Lotad"]),

    # Treecko
    (0x803751FC+0x0001, 0x80, FRIENDSHIP_ITEMS["Treecko"]),
    (0x803751FC+0x000c, 0x80, FRIENDSHIP_ITEMS["Treecko"]),

    # Caterpie
    (0x80375274+0x0001, 0x80, FRIENDSHIP_ITEMS["Caterpie"]),
    (0x80375274+0x000c, 0x80, FRIENDSHIP_ITEMS["Caterpie"]),

    # Butterfree
    (0x80375288+0x0001, 0x80, FRIENDSHIP_ITEMS["Butterfree"]),
    (0x80375288+0x000c, 0x80, FRIENDSHIP_ITEMS["Butterfree"]),

    # Chimchar
    (0x80375A94+0x0001, 0x80, FRIENDSHIP_ITEMS["Chimchar"]),
    (0x80375A94+0x000c, 0x80, FRIENDSHIP_ITEMS["Chimchar"]),

    # Aipom
    (0x8037542C+0x0001, 0x80, FRIENDSHIP_ITEMS["Aipom"]),
    (0x8037542C+0x000c, 0x80, FRIENDSHIP_ITEMS["Aipom"]),

    # Ambipom
    (0x80375440+0x0001, 0x80, FRIENDSHIP_ITEMS["Ambipom"]),
    (0x80375440+0x000c, 0x80, FRIENDSHIP_ITEMS["Ambipom"]),

    # Weedle
    (0x80375260+0x0001, 0x80, FRIENDSHIP_ITEMS["Weedle"]),
    (0x80375260+0x000c, 0x80, FRIENDSHIP_ITEMS["Weedle"]),

    # Shroomish
    (0x803752EC+0x0001, 0x80, FRIENDSHIP_ITEMS["Shroomish"]),
    (0x803752EC+0x000c, 0x80, FRIENDSHIP_ITEMS["Shroomish"]),

    # Magikarp
    (0x803756D4+0x0001, 0x80, FRIENDSHIP_ITEMS["Magikarp"]),
    (0x803756D4+0x000c, 0x80, FRIENDSHIP_ITEMS["Magikarp"]),

    # Oddish
    (0x803753A0+0x0001, 0x80, FRIENDSHIP_ITEMS["Oddish"]),
    (0x803753A0+0x000c, 0x80, FRIENDSHIP_ITEMS["Oddish"]),

    # Leafeon
    (0x803754CC+0x0001, 0x80, FRIENDSHIP_ITEMS["Leafeon"]),
    (0x803754CC+0x000c, 0x80, FRIENDSHIP_ITEMS["Leafeon"]),

    # Bidoof
    (0x80375238+0x0001, 0x80, FRIENDSHIP_ITEMS["Bidoof"]),
    (0x80375238+0x000c, 0x80, FRIENDSHIP_ITEMS["Bidoof"]),

    # Starly
    (0x80375364+0x0001,0x80, FRIENDSHIP_ITEMS["Starly"]),
    (0x80375364 + 0x000c, 0x80, FRIENDSHIP_ITEMS["Starly"]),
    #Torterra
    (0x803751E8 + 0x0001, 0x80, FRIENDSHIP_ITEMS["Torterra"]),
    (0x803751E8 + 0x000c, 0x80, FRIENDSHIP_ITEMS["Torterra"]),
    # Bibarel
    (0x8037524C + 0x0001, 0x80, FRIENDSHIP_ITEMS["Bibarel"]),
    (0x8037524C + 0x000c, 0x80, FRIENDSHIP_ITEMS["Bibarel"]),
    # Scyther
    (0x80375454 + 0x0001, 0x80, FRIENDSHIP_ITEMS["Scyther"]),
    (0x80375454 + 0x000c, 0x80, FRIENDSHIP_ITEMS["Scyther"]),

]
quests_location_checks = [

    # quests
    # Meadow Zone
    (0x8037500F, 0x66, BERRIES.get("10 Berries") + 1),
    (0x8037500F, 0x6A, BERRIES.get("10 Berries") + 2),
    (0x8037500F, 0x6E, BERRIES.get("10 Berries") + 3),
    (0x8037500F, 0x72, BERRIES.get("10 Berries") + 4),

    # Beach Zone
    (0x80375011, 0x10, BERRIES.get("10 Berries") + 5),
    (0x80375011, 0x20, BERRIES.get("10 Berries") + 6),
    (0x80375011, 0x30, BERRIES.get("10 Berries") + 7),
    (0x80375011, 0x40, BERRIES.get("10 Berries") + 8),
    (0x80375011, 0x50, BERRIES.get("10 Berries") + 9),
    (0x80375011, 0x60, BERRIES.get("10 Berries") + 10),
]
unlocks_location_checks = [
    #unlocks
    #
    # Tropius
    (0x80376ad0 + 0x7FFF + 0x0001, 0x40, UNLOCK_ITEMS["Tropius Unlock"]),
    # Pachirisu
    (0x80376ad0 + 0x7FFF + 0x0003, 0x08, UNLOCK_ITEMS["Pachirisu Unlock"]),
    (0x80376ad0 + 0x7FFF + 0x0002, 0x40, UNLOCK_ITEMS["Pachirisu Unlock"]),
    # Sudowoodo
    (0x80376ad8 + 0x7FFF +0x0001, 0x40, UNLOCK_ITEMS["Sudowoodo Unlock"]),
    # Lotad
    (0x80376ad0+ 0x7FFF +0x0002, 0x80, UNLOCK_ITEMS["Lotad Unlock"]),
    # Scyther
    (0x80376ad0 + 0x7FFF+0x0000, 0x04, UNLOCK_ITEMS["Scyther Unlock"]),
    # Caterpie
    (0x80376ad0 + 0x7FFF+0x0002, 0x02, UNLOCK_ITEMS["Caterpie Unlock"]),
    # Butterfree
    (0x80376ad0 + 0x7FFF +0x0001, 0x20, UNLOCK_ITEMS["Butterfree Unlock"]),
    # Chimchar
    (0x80376ad0 + 0x7FFF +0x0003, 0x40, UNLOCK_ITEMS["Chimchar Unlock"]),
    # Ambipom
    (0x80376ad0 + 0x7FFF+0x0000, 0x01, UNLOCK_ITEMS["Ambipom Unlock"]),
    # Weedle
    (0x80376ad0 + 0x7FFF+0x0002, 0x04, UNLOCK_ITEMS["Weedle Unlock"]),
    # Shroomish
    (0x80376ad0 + 0x7FFF+0x0002, 0x20, UNLOCK_ITEMS["Shroomish Unlock"]),
    # Magikarp
    (0x80376ad0 + 0x7FFF+ 0x0003, 0x80, UNLOCK_ITEMS["Magikarp Unlock"]),
    # Bidoof1
    (0x80376ad0 + 0x7FFF+0x0000, 0x80, UNLOCK_ITEMS["Bidoof1 Unlock"]),
    # Bidoof2
    (0x80376ad4 + 0x7FFF+0x0003, 0x01, UNLOCK_ITEMS["Bidoof2 Unlock"]),
    # Bidoof3
    (0x80376ad4 + 0x7FFF+0x0003, 0x02, UNLOCK_ITEMS["Bidoof3 Unlock"]),
    # Bibarel
    (0x80376ad0 + 0x7FFF+0x0001, 0x80, UNLOCK_ITEMS["Bibarel Unlock"]),
    # Starly
    (0x80376ad0 + 0x7FFF+0x0001, 0x10, UNLOCK_ITEMS["Starly Unlock"]),
    # Torterra
    (0x80376ad0 + 0x7FFF+0x0001, 0x08, UNLOCK_ITEMS["Torterra Unlock"]),

    #Beach Zone
    #
    (0x80376AD4 + 0x7FFF + 0x0000, 0x02, UNLOCK_ITEMS["Floatzel Unlock"]),
    (0x80376AD4 + 0x7FFF + 0x0000, 0x01, UNLOCK_ITEMS["Golduck Unlock"]),
    (0x80376AD4 + 0x7FFF + 0x0001, 0x04, UNLOCK_ITEMS["Mudkip Unlock"]),
    (0x80376AD4 + 0x7FFF + 0x0001, 0x02, UNLOCK_ITEMS["Totodile Unlock"]),
    (0x80376AD4 + 0x7FFF + 0x0001, 0x01, UNLOCK_ITEMS["Krabby Unlock"]),
    (0x80376AD4 + 0x7FFF + 0x0001, 0x08, UNLOCK_ITEMS["Corphish Unlock"]),
]

#halfword
minigame_location_checks = [
    # Meadow Zone - Bulbasaur's Daring Dash Minigame
    #
    # Pikachu
    (0x80377E30, 0x0001, BERRIES.get("100 Berries")+1),
    #Turtwig
    (0x80377EE4, 0x0001, BERRIES.get("100 Berries") + 2),
    # Munchlax
    (0x80377F20, 0x0001, BERRIES.get("100 Berries") + 3),
    # Chimchar
    (0x80377EC0, 0x0001, BERRIES.get("100 Berries") + 4),
    # Treecko
    (0x80377ECC, 0x0001, BERRIES.get("100 Berries") + 5),
    # Bibarel
    (0x80377ED8, 0x0001, BERRIES.get("100 Berries") + 6),
    # Bulbasaur
    (0x80377EF0, 0x0001, BERRIES.get("100 Berries") + 7),
    # Bidoof
    (0x80377EFC, 0x0001, BERRIES.get("100 Berries") + 8),
    # Oddish
    (0x80377F08, 0x0001, BERRIES.get("100 Berries") + 9),
    # Shroomish
    (0x80377F14, 0x0001, BERRIES.get("100 Berries") + 10),
    # Bonsly
    (0x80377F2C, 0x0001, BERRIES.get("100 Berries") + 11),
    # Lotad
    (0x80377F38, 0x0001, BERRIES.get("100 Berries") + 12),
    # Weedle
    (0x80377F44, 0x0001, BERRIES.get("100 Berries") + 13),
    # Caterpie
    (0x80377F50, 0x0001, BERRIES.get("100 Berries") + 14),
    # Magikarp
    (0x80377F5C, 0x0001, BERRIES.get("100 Berries") + 15),
    # Jolteon
    #(0x0, 0x0001, BERRIES.get("100 Berries") + 16),
    # Arcanine
    # (0x0, 0x0001, BERRIES.get("100 Berries") + 17),
    # Leafeon
    (0x80377E60, 0x0001, BERRIES.get("100 Berries") + 18),
    # Scyther
    (0x80377e6c, 0x0001, BERRIES.get("100 Berries") + 19),
    # Ponyta
    # (0x0, 0x0001, BERRIES.get("100 Berries") + 20),
    # Shinx
    (0x80377E84, 0x0001, BERRIES.get("100 Berries") + 21),
    # Eevee
    # (0x0, 0x0001, BERRIES.get("100 Berries") + 22),
    # Pachirisu
    (0x80377E9C, 0x0001, BERRIES.get("100 Berries") + 23),
    # Buneary
    (0x80377EA8, 0x0001, BERRIES.get("100 Berries") + 24),
    # Croagunk
    (0x80377EB4, 0x0001, BERRIES.get("100 Berries") + 25),


    #Pikachu
    (0x80376DBC, 0x0001, BERRIES.get("100 Berries") + 26),
    # Munchlax
    (0x80376e64, 0x0001, BERRIES.get("100 Berries") + 27),
    #Magikarp
    (0x80376e70, 0x0001, BERRIES.get("100 Berries") + 28),
    #Blaziken
    #(0x, 0x0001, BERRIES.get("100 Berries") + 29),
    # Infernape
    # (0x, 0x0001, BERRIES.get("100 Berries") + 30),
    # Lucario
    # (0x, 0x0001, BERRIES.get("100 Berries") + 31),
    # Primeape
    # (0x, 0x0001, BERRIES.get("100 Berries") + 32),
    # Tangrowth
    # (0x, 0x0001, BERRIES.get("100 Berries") + 33),
    # Ambipom
    (0x80376e10, 0x0001, BERRIES.get("100 Berries") + 34),
    # Croagunk
    (0x80376e4c, 0x0001, BERRIES.get("100 Berries") + 35),
    # Mankey
    (0x80376e1c, 0x0001, BERRIES.get("100 Berries") + 36),
    # Aipom
    (0x80376e28, 0x0001, BERRIES.get("100 Berries") + 37),
    # Chimchar
    (0x80376e34, 0x0001, BERRIES.get("100 Berries") + 38),
    # Treecko
    (0x80376e40, 0x0001, BERRIES.get("100 Berries") + 39),
    # Pachirisu
    (0x80376e58, 0x0001, BERRIES.get("100 Berries") + 40),

    # Beach Zone Pelipper's Circle Circuit
    # Pikachu
    (0x80377380, 0x0001, BERRIES.get("100 Berries") + 41),
    # Staraptor
    # (0x, 0x0001, BERRIES.get("100 Berries") + 42),
    # Togekiss
    # (0x, 0x0001, BERRIES.get("100 Berries") + 43),
    # Honchkrow
    # (0x, 0x0001, BERRIES.get("100 Berries") + 44),
    # Gliscor
    # (0x, 0x0001, BERRIES.get("100 Berries") + 45),
    # Pelipper
    (0x80377338, 0x0001, BERRIES.get("100 Berries") + 46),
    # Staravia
    (0x803772FC, 0x0001, BERRIES.get("100 Berries") + 47),
    # Pidgeotto
    (0x80377308, 0x0001, BERRIES.get("100 Berries") + 48),
    # Butterfree
    (0x80377374, 0x0001, BERRIES.get("100 Berries") + 49),
    # Tropius
    (0x80377368, 0x0001, BERRIES.get("100 Berries") + 50),
    # Murkrow
    # (0x, 0x0001, BERRIES.get("100 Berries") + 51),
    # Taillow
    (0x80377320, 0x0001, BERRIES.get("100 Berries") + 52),
    # Spearow
    (0x8037732C, 0x0001, BERRIES.get("100 Berries") + 53),
    # Starly
    (0x80377344, 0x0001, BERRIES.get("100 Berries") + 54),
    #Wingull
    (0x8037735c, 0x0001, BERRIES.get("100 Berries") + 55),

    # Beach Zone Gyarados' Aqua Dash
    # Pikachu
    (0x80377218, 0x0001, BERRIES.get("100 Berries") + 56),
    # Psyduck
    (0x80377224, 0x0001, BERRIES.get("100 Berries") + 57),
    # Azurill
    (0x80377230, 0x0001, BERRIES.get("100 Berries") + 58),
    # Slowpoke
    (0x8037723c, 0x0001, BERRIES.get("100 Berries") + 59),
    # Empoleon
    #(0x, 0x0001, BERRIES.get("100 Berries") + 60),
    # Floatzel
    (0x803771a0, 0x0001, BERRIES.get("100 Berries") + 61),
    # Feraligatr
    (0x803771ac, 0x0001, BERRIES.get("100 Berries") + 62),
    # Golduck
    (0x803771b8, 0x0001, BERRIES.get("100 Berries") + 63),
    # Vaporeon
    (0x803771c4, 0x0001, BERRIES.get("100 Berries") + 64),
    # Prinplup
    #(0x, 0x0001, BERRIES.get("100 Berries") + 65),
    # Bibarel
    (0x803771dc, 0x0001, BERRIES.get("100 Berries") + 66),
    # Buizel
    (0x803771f4, 0x0001, BERRIES.get("100 Berries") + 67),
    # Corsola
    (0x803771e8, 0x0001, BERRIES.get("100 Berries") + 68),
    # Piplup
    (0x80377200, 0x0001, BERRIES.get("100 Berries") + 69),
    # Lotad
    (0x8037720c, 0x0001, BERRIES.get("100 Berries") + 70),

]

unlock_item_checks = {
    #Meadow Zone
  UNLOCK_ITEMS["Tropius Unlock"]: (0x80376AE1, 0x40),
  UNLOCK_ITEMS["Pachirisu Unlock"]: (0x80376AE3, 0x08),
  UNLOCK_ITEMS["Bonsly Unlock"]: (0x80376AE2, 0x40),
  UNLOCK_ITEMS["Sudowoodo Unlock"]: (0x80376AE9, 0x40),
  UNLOCK_ITEMS["Lotad Unlock"]: (0x80376AE2, 0x01),
  UNLOCK_ITEMS["Shinx Unlock"]: (0x80376AE2, 0x80),
  UNLOCK_ITEMS["Scyther Unlock"]: (0x80376AE0 , 0x04),
  UNLOCK_ITEMS["Caterpie Unlock"]: (0x80376AE2 , 0x02),
  UNLOCK_ITEMS["Butterfree Unlock"]: (0x80376AE1 , 0x20),
  UNLOCK_ITEMS["Chimchar Unlock"]: (0x80376AE3 , 0x40),
  UNLOCK_ITEMS["Ambipom Unlock"]: (0x80376AE0 , 0x01),
  UNLOCK_ITEMS["Weedle Unlock"]: (0x80376AE2 , 0x04),
  UNLOCK_ITEMS["Shroomish Unlock"]: (0x80376AE2 , 0x20),
  UNLOCK_ITEMS["Magikarp Unlock"]: (0x80376AE3 , 0x80),
  UNLOCK_ITEMS["Bidoof1 Unlock"]: (0x80376AE0 , 0x80),
  UNLOCK_ITEMS["Bidoof2 Unlock"]: (0x80376AE7 , 0x01),
  UNLOCK_ITEMS["Bidoof3 Unlock"]: (0x80376AE7 , 0x02),
  UNLOCK_ITEMS["Bibarel Unlock"]: (0x80376AE1 , 0x80),
  UNLOCK_ITEMS["Starly Unlock"]: (0x80376AE1 , 0x10),
UNLOCK_ITEMS["Starly Unlock 2"]: (0x80376AE7, 0x10),
UNLOCK_ITEMS["Torterra Unlock"]: (0x80376AE1 , 0x08),

    #Beach Zone
    UNLOCK_ITEMS["Floatzel Unlock"]: (0x80376AE4,0x02),
    UNLOCK_ITEMS["Golduck Unlock"]: (0x80376AE4, 0x01),
    UNLOCK_ITEMS["Mudkip Unlock"]: (0x80376AE5, 0x04),
    UNLOCK_ITEMS["Totodile Unlock"]: (0x80376AE5, 0x02),
    UNLOCK_ITEMS["Krabby Unlock"]: (0x80376AE5, 0x01),
    UNLOCK_ITEMS["Corphish Unlock"]: (0x80376AE5, 0x08),

    #Misc
    UNLOCK_ITEMS["Pikachu Balloon"]: (0x8037AEC3, 0x08), #+0x08
    UNLOCK_ITEMS["Pikachu Surfboard"]: (0x8037AEC3, 0x01), #+0x01

}

power_item_location_checks = [
    (0x8037501c, 0x01, POWERS["Progressive Thunderbolt"]+1, 0x0F),
    (0x8037501c, 0x02, POWERS["Progressive Thunderbolt"]+2, 0x0F),
    (0x8037501c, 0x03, POWERS["Progressive Thunderbolt"]+3, 0x0F),
    (0x8037501d, 0x10, POWERS["Progressive Dash"]+1, 0xF0),
    (0x8037501d, 0x20, POWERS["Progressive Dash"]+2, 0xF0),
    (0x8037501d, 0x30, POWERS["Progressive Dash"]+3, 0xF0),
    (0x8037501d, 0x01, POWERS["Progressive Health"] + 1, 0x0F),
    (0x8037501d, 0x02, POWERS["Progressive Health"] + 2, 0x0F),
    (0x8037501d, 0x03, POWERS["Progressive Health"] + 3, 0x0F)
]
POWER_INCREMENTS = {
    "thunderbolt": {
        "base": 0x11,
        "increments": [0x20, 0x40, 0x80],      # +20, +40, +80
    },
    "dash": {
        "base": 0x11,
        "increments": [0x04, 0x08, 0x4000],    # +4, +8, +4000
    },
    "health": {
        "base": 0x11,
        "increments": [0x100,0x200,0x400]
    }
}

POWER_SHARED_ADDR = 0x8037AEEE # at least dash and thunderbolt


friend_item_checks = {
    #Meadow Zone
   FRIENDSHIP_ITEMS["Chikorita"]: [(0x80375C74,0x80)],
   FRIENDSHIP_ITEMS["Pachirisu"]: [(0x80375210,0x80)],
   FRIENDSHIP_ITEMS["Bulbasaur"]: [(0x80375490,0x80)],
   FRIENDSHIP_ITEMS["Munchlax"]: [(0x8037529C,0x80)],
   FRIENDSHIP_ITEMS["Tropius"]: [(0x803753DC,0x80)], #00400000
   FRIENDSHIP_ITEMS["Turtwig"]: [(0x803751D4,0x80)],
   FRIENDSHIP_ITEMS["Bonsly"]: [(0x803752C4,0x80)],
   FRIENDSHIP_ITEMS["Sudowoodo"]: [(0x803752D8,0x80)],
   FRIENDSHIP_ITEMS["Buneary"]: [(0x8037533C,0x80)],
   FRIENDSHIP_ITEMS["Shinx"]: [(0x803753F0,0x80)],
   FRIENDSHIP_ITEMS["Mankey"]: [(0x80375314,0x80)],
   FRIENDSHIP_ITEMS["Spearow"]: [(0x803753C8,0x80)],
   FRIENDSHIP_ITEMS["Croagunk"]: [(0x8037547C,0x80)],
   FRIENDSHIP_ITEMS["Chatot"]: [(0x80376034,0x80)],
   FRIENDSHIP_ITEMS["Lotad"]: [(0x80375224,0x80)],
   FRIENDSHIP_ITEMS["Treecko"]: [(0x803751FC,0x80)],
   FRIENDSHIP_ITEMS["Caterpie"]: [(0x80375274,0x80)],
   FRIENDSHIP_ITEMS["Butterfree"]: [(0x80375288,0x80)],
   FRIENDSHIP_ITEMS["Chimchar"]: [(0x80375A94,0x80)],
   FRIENDSHIP_ITEMS["Aipom"]: [(0x8037542C,0x80)],
   FRIENDSHIP_ITEMS["Ambipom"]: [(0x80375440,0x80)],
   FRIENDSHIP_ITEMS["Weedle"]: [(0x80375260,0x80)],
   FRIENDSHIP_ITEMS["Shroomish"]: [(0x803752EC,0x80)],
   FRIENDSHIP_ITEMS["Magikarp"]: [(0x803756D4,0x80)],
   FRIENDSHIP_ITEMS["Oddish"]: [(0x803753A0,0x80)],
   FRIENDSHIP_ITEMS["Leafeon"]: [(0x803754CC,0x80)],
   FRIENDSHIP_ITEMS["Bidoof"]: [(0x80375238,0x80)],
   FRIENDSHIP_ITEMS["Bibarel"]: [(0x8037524C, 0x80)],
   FRIENDSHIP_ITEMS["Torterra"]: [(0x803751E8, 0x80)],
   FRIENDSHIP_ITEMS["Starly"]: [(0x80375364,0x80)],
    FRIENDSHIP_ITEMS["Scyther"]: [(0x80375454,0x80)],
    # Beach Zone
   FRIENDSHIP_ITEMS["Buizel"]: [(0x803755d0, 0x80)],
    FRIENDSHIP_ITEMS["Psyduck"]: [(0x803755F8, 0x80)],
    FRIENDSHIP_ITEMS["Slowpoke"]: [(0x803755BC, 0x80)],
    FRIENDSHIP_ITEMS["Azurill"]: [(0x80375558, 0x80)],
    FRIENDSHIP_ITEMS["Totodile"]: [(0x80375670, 0x80)],
    FRIENDSHIP_ITEMS["Mudkip"]: [(0x8037556C, 0x80)],
    FRIENDSHIP_ITEMS["Pidgeotto"]: [(0x80375634, 0x80)],
    FRIENDSHIP_ITEMS["Taillow"]: [(0x80375620, 0x80)],
    FRIENDSHIP_ITEMS["Wingull"]: [(0x803756ac, 0x80)],
    FRIENDSHIP_ITEMS["Staravia"]: [(0x80375378, 0x80)],
    FRIENDSHIP_ITEMS["Corsola"]: [(0x803755a8, 0x80)],
    FRIENDSHIP_ITEMS["Floatzel"]: [(0x803755E4, 0x80)],
    FRIENDSHIP_ITEMS["Vaporeon"]: [(0x803754E0, 0x80)],
    FRIENDSHIP_ITEMS["Golduck"]: [(0x8037560C, 0x80)],
    FRIENDSHIP_ITEMS["Pelipper"]: [(0x803756C0, 0x80)],
    FRIENDSHIP_ITEMS["Sharpedo"]: [(0x80376048, 0x80)],
    FRIENDSHIP_ITEMS["Wynaut"]: [(0x80375C88, 0x80)],
    FRIENDSHIP_ITEMS["Carvanha"]: [(0x80375FE4, 0x80)],
    FRIENDSHIP_ITEMS["Krabby"]: [(0x80375580, 0x80)],
    FRIENDSHIP_ITEMS["Wailord"]: [(0x803760ac, 0x80)],
    FRIENDSHIP_ITEMS["Corphish"]: [(0x80375594, 0x80)],
    FRIENDSHIP_ITEMS["Gyarados"]: [(0x803756E8, 0x80)],
    FRIENDSHIP_ITEMS["Feraligatr"]: [(0x80375684, 0x80)],
    FRIENDSHIP_ITEMS["Piplup"]: [(0x803757EC, 0x80)],

}

prisma_item_checks = {
    PRISM_ITEM["Bulbasaur Prisma"]: [(0x80377E1C,0x00000003)],
    PRISM_ITEM["Venusaur Prisma"]: [(0x80376DA8,0x00000003)],
    PRISM_ITEM["Pelipper Prisma"]: [(0x803772B8, 0x00000003)],
    PRISM_ITEM["Gyarados Prisma"]: [(0x80377174, 0x00000003)],

}
MEADOW_ZONE_SPECIAL_EXCEPTION_POKEMON = [
    (FRIENDSHIP_ITEMS["Tropius"], friend_item_checks[FRIENDSHIP_ITEMS["Tropius"]]),
    (FRIENDSHIP_ITEMS["Munchlax"], friend_item_checks[FRIENDSHIP_ITEMS["Munchlax"]]),
    (FRIENDSHIP_ITEMS["Leafeon"], friend_item_checks[FRIENDSHIP_ITEMS["Leafeon"]]),
]
meadow_zone_unlock_pokemon_addresses_for_location = {
    0x0000002f: [UNLOCK_ITEMS.get("Tropius Unlock")],
    0x0000000f: [UNLOCK_ITEMS.get("Sudowoodo Unlock")],
    0x0000002d: [UNLOCK_ITEMS.get("Bonsly Unlock"),UNLOCK_ITEMS.get("Pachirisu Unlock")],
    0x00000002: [UNLOCK_ITEMS.get("Bonsly Unlock"), UNLOCK_ITEMS.get("Pachirisu Unlock")],
    0x00000003: [UNLOCK_ITEMS.get("Lotad Unlock"), UNLOCK_ITEMS.get("Shinx Unlock")],
    0x0000002b: [UNLOCK_ITEMS.get("Lotad Unlock"), UNLOCK_ITEMS.get("Shinx Unlock")],
0x0000001d: [UNLOCK_ITEMS.get("Scyther Unlock")],
0x0000000a: [UNLOCK_ITEMS.get("Butterfree Unlock")],
0x00000025: [UNLOCK_ITEMS.get("Ambipom Unlock")],
0x00000012: [UNLOCK_ITEMS.get("Ambipom Unlock")],
0x0000000c: [UNLOCK_ITEMS.get("Bidoof1 Unlock"),UNLOCK_ITEMS.get("Bidoof2 Unlock"),UNLOCK_ITEMS.get("Bidoof3 Unlock"),UNLOCK_ITEMS.get("Bibarel Unlock")]
}
beach_zone_unlock_pokemon_addresses_for_location = {
0x00000002: [UNLOCK_ITEMS.get("Floatzel Unlock")],
0x00000003: [UNLOCK_ITEMS.get("Golduck Unlock")],
0x00000004: [UNLOCK_ITEMS.get("Mudkip Unlock")],
0x00000005: [UNLOCK_ITEMS.get("Totodile Unlock")]
}


UNCHECKED_MEADOW_ZONE_LOCATION_POKEMON_IDS = [
   # Meadow Zone
   # (pokemon_id, friend_item_checks, location_id)
    # (0x00000001, friend_item_checks[FRIENDSHIP_ITEMS["Chatot"]]), not neccessary for now
    # (0x00000032, friend_item_checks[FRIENDSHIP_ITEMS["Chikorita"]]), #not neccessary for now
   (0x0000002f, friend_item_checks[FRIENDSHIP_ITEMS["Munchlax"]], FRIENDSHIP_ITEMS["Munchlax"]), #event munchlax
   (0x00000005, friend_item_checks[FRIENDSHIP_ITEMS["Munchlax"]], FRIENDSHIP_ITEMS["Munchlax"]), # overworld munchlax
   (0x0000002d, friend_item_checks[FRIENDSHIP_ITEMS["Turtwig"]], FRIENDSHIP_ITEMS["Turtwig"]), # static overworld blocked from event
   (0x00000002, friend_item_checks[FRIENDSHIP_ITEMS["Turtwig"]], FRIENDSHIP_ITEMS["Turtwig"]), # free walking overworld
   (0x00000003, friend_item_checks[FRIENDSHIP_ITEMS["Buneary"]], FRIENDSHIP_ITEMS["Buneary"]), # free walking overworld
   (0x0000002b, friend_item_checks[FRIENDSHIP_ITEMS["Buneary"]], FRIENDSHIP_ITEMS["Buneary"]), # standing beside bulbasaur after minigame
   (0x00000027, friend_item_checks[FRIENDSHIP_ITEMS["Spearow"]], FRIENDSHIP_ITEMS["Spearow"]), # before minigame
   (0x00000013, friend_item_checks[FRIENDSHIP_ITEMS["Spearow"]], FRIENDSHIP_ITEMS["Spearow"]), #overworld spearow
   (0x0000001C, friend_item_checks[FRIENDSHIP_ITEMS["Leafeon"]], FRIENDSHIP_ITEMS["Leafeon"]), # overworld leafeon
   (0x0000000c, friend_item_checks[FRIENDSHIP_ITEMS["Bidoof"]], FRIENDSHIP_ITEMS["Bidoof"]), # quest bidoof
    (0x0000001e, friend_item_checks[FRIENDSHIP_ITEMS["Bulbasaur"]],FRIENDSHIP_ITEMS["Bulbasaur"]), #prob not needed
    (0x00000031, friend_item_checks[FRIENDSHIP_ITEMS["Pachirisu"]], FRIENDSHIP_ITEMS["Pachirisu"]), #pachirisu 1
   (0x00000004, friend_item_checks[FRIENDSHIP_ITEMS["Pachirisu"]], FRIENDSHIP_ITEMS["Pachirisu"]), # pachirisu 2
   (0x0000000f, friend_item_checks[FRIENDSHIP_ITEMS["Bonsly"]], FRIENDSHIP_ITEMS["Bonsly"]), # overworld bonsly
   (0x00000010, friend_item_checks[FRIENDSHIP_ITEMS["Shinx"]], FRIENDSHIP_ITEMS["Shinx"]), #shinx 1 overworld
   (0x0000002c, friend_item_checks[FRIENDSHIP_ITEMS["Shinx"]], FRIENDSHIP_ITEMS["Shinx"]), # shinx 2 overworld
   (0x00000017, friend_item_checks[FRIENDSHIP_ITEMS["Tropius"]], FRIENDSHIP_ITEMS["Tropius"]), #tropius overworld
   (0x00000021, friend_item_checks[FRIENDSHIP_ITEMS["Lotad"]], FRIENDSHIP_ITEMS["Lotad"]), #Lotad 1 overworld
   (0x00000009, friend_item_checks[FRIENDSHIP_ITEMS["Lotad"]], FRIENDSHIP_ITEMS["Lotad"]), # Lotad 2 overworld
   (0x00000028, friend_item_checks[FRIENDSHIP_ITEMS["Lotad"]], FRIENDSHIP_ITEMS["Lotad"]), # Lotad 3 overworld
   (0x00000029, friend_item_checks[FRIENDSHIP_ITEMS["Lotad"]], FRIENDSHIP_ITEMS["Lotad"]), # Lotad 4 overworld
   (0x00000006, friend_item_checks[FRIENDSHIP_ITEMS["Treecko"]], FRIENDSHIP_ITEMS["Treecko"]), # Treecko overworld
   (0x0000001a, friend_item_checks[FRIENDSHIP_ITEMS["Sudowoodo"]], FRIENDSHIP_ITEMS["Sudowoodo"]), # Sudowoodo overworld
   (0x0000000a, friend_item_checks[FRIENDSHIP_ITEMS["Caterpie"]], FRIENDSHIP_ITEMS["Caterpie"]), # overworld caterpie
   (0x0000000d, friend_item_checks[FRIENDSHIP_ITEMS["Oddish"]], FRIENDSHIP_ITEMS["Oddish"]), # overworld oddish
    # (0x00000011, friend_item_checks[FRIENDSHIP_ITEMS["Mankey"]]), # overworld mankey probably not neccessary for now since locations are event based
    (0x00000025, friend_item_checks[FRIENDSHIP_ITEMS["Aipom"]], FRIENDSHIP_ITEMS["Aipom"]), #overworld walking aipom
   (0x00000012, friend_item_checks[FRIENDSHIP_ITEMS["Aipom"]], FRIENDSHIP_ITEMS["Aipom"]), # explainer aipom beside tree
   (0x0000000e, friend_item_checks[FRIENDSHIP_ITEMS["Shroomish"]], FRIENDSHIP_ITEMS["Shroomish"]), #overworld Shroomish
   (0x0000000b, friend_item_checks[FRIENDSHIP_ITEMS["Weedle"]], FRIENDSHIP_ITEMS["Weedle"]), #overworld weedle
   (0x00000008, friend_item_checks[FRIENDSHIP_ITEMS["Magikarp"]], FRIENDSHIP_ITEMS["Magikarp"]), #overworld magikarp
   (0x00000019, friend_item_checks[FRIENDSHIP_ITEMS["Ambipom"]], FRIENDSHIP_ITEMS["Ambipom"]), #overworld Ambipom
   (0x00000007, friend_item_checks[FRIENDSHIP_ITEMS["Chimchar"]], FRIENDSHIP_ITEMS["Chimchar"]), #overworld Chimchar
   (0x0000002e, friend_item_checks[FRIENDSHIP_ITEMS["Butterfree"]], FRIENDSHIP_ITEMS["Butterfree"]), #overworld flying Butterfree
    (0x00000016, friend_item_checks[FRIENDSHIP_ITEMS["Butterfree"]], FRIENDSHIP_ITEMS["Butterfree"]), # overworld flying Butterfree 2

    (0x0000001d, friend_item_checks[FRIENDSHIP_ITEMS["Croagunk"]], FRIENDSHIP_ITEMS["Croagunk"]), # standing before gate
   (0x00000014, friend_item_checks[FRIENDSHIP_ITEMS["Torterra"]], FRIENDSHIP_ITEMS["Torterra"]), # walking in overworld Torterra
   (0x00000023, friend_item_checks[FRIENDSHIP_ITEMS["Starly"]], FRIENDSHIP_ITEMS["Starly"]), # flying Starly 1
   (0x00000024, friend_item_checks[FRIENDSHIP_ITEMS["Starly"]], FRIENDSHIP_ITEMS["Starly"]), # flying Starly 2
   (0x0000002a, friend_item_checks[FRIENDSHIP_ITEMS["Starly"]], FRIENDSHIP_ITEMS["Starly"]), # flying Starly 3
   (0x00000015, friend_item_checks[FRIENDSHIP_ITEMS["Starly"]], FRIENDSHIP_ITEMS["Starly"]), # flying Starly 4
   (0x00000026, friend_item_checks[FRIENDSHIP_ITEMS["Starly"]], FRIENDSHIP_ITEMS["Starly"]), # flying Starly 5
   (0x00000018, friend_item_checks[FRIENDSHIP_ITEMS["Bibarel"]], FRIENDSHIP_ITEMS["Bibarel"]), # overworld Bibarel
    (0x0000001b, friend_item_checks[FRIENDSHIP_ITEMS["Scyther"]], FRIENDSHIP_ITEMS["Scyther"]),

]

UNCHECKED_BEACH_ZONE_LOCATION_POKEMON_IDS = [
   # Beach Zone
   # (pokemon_id, friend_item_checks, location_id)
   (0x00000002, friend_item_checks[FRIENDSHIP_ITEMS["Buizel"]], FRIENDSHIP_ITEMS["Buizel"]), # overworld Buizel
    (0x00000016, friend_item_checks[FRIENDSHIP_ITEMS["Floatzel"]], FRIENDSHIP_ITEMS["Floatzel"]),  # overworld Floatzel

    (0x00000003, friend_item_checks[FRIENDSHIP_ITEMS["Psyduck"]], FRIENDSHIP_ITEMS["Psyduck"]),  # overworld Psyduck
    (0x00000004, friend_item_checks[FRIENDSHIP_ITEMS["Slowpoke"]], FRIENDSHIP_ITEMS["Slowpoke"]),  # overworld Slowpoke
    (0x00000005, friend_item_checks[FRIENDSHIP_ITEMS["Azurill"]], FRIENDSHIP_ITEMS["Azurill"]),  # overworld Azurill
    (0x00000006, friend_item_checks[FRIENDSHIP_ITEMS["Corsola"]], FRIENDSHIP_ITEMS["Corsola"]),  # overworld Corsola quest on bridge
    (0x00000021, friend_item_checks[FRIENDSHIP_ITEMS["Corsola"]], FRIENDSHIP_ITEMS["Corsola"]),  # overworld Corsola free
    (0x00000022, friend_item_checks[FRIENDSHIP_ITEMS["Corsola"]], FRIENDSHIP_ITEMS["Corsola"]),  # overworld Corsola free

    (0x00000007, friend_item_checks[FRIENDSHIP_ITEMS["Taillow"]], FRIENDSHIP_ITEMS["Taillow"]),  # overworld Taillow 1 todo:search all
    (0x00000029, friend_item_checks[FRIENDSHIP_ITEMS["Taillow"]], FRIENDSHIP_ITEMS["Taillow"]), # overworld Taillow 2
    (0x00000024, friend_item_checks[FRIENDSHIP_ITEMS["Wingull"]], FRIENDSHIP_ITEMS["Wingull"]),  # overworld Wingull 1 todo:search all
    (0x0000002b, friend_item_checks[FRIENDSHIP_ITEMS["Wingull"]], FRIENDSHIP_ITEMS["Wingull"]), # overworld Wingull 2 todo:search all
    (0x0000000a, friend_item_checks[FRIENDSHIP_ITEMS["Wingull"]], FRIENDSHIP_ITEMS["Wingull"]),
    # overworld Wingull 3 todo:search all
    (0x00000026, friend_item_checks[FRIENDSHIP_ITEMS["Starly"]], FRIENDSHIP_ITEMS["Starly"] +1000),  # overworld Starly 1 todo:search all
    (0x00000008, friend_item_checks[FRIENDSHIP_ITEMS["Starly"]], FRIENDSHIP_ITEMS["Starly"]+1000),
    # overworld Starly 2 todo:search all

    (0x0000000c, friend_item_checks[FRIENDSHIP_ITEMS["Totodile"]], FRIENDSHIP_ITEMS["Totodile"]),  # overworld Totodile
    (0x0000000d, friend_item_checks[FRIENDSHIP_ITEMS["Mudkip"]], FRIENDSHIP_ITEMS["Mudkip"]),  # overworld Mudkip
    (0x00000017, friend_item_checks[FRIENDSHIP_ITEMS["Staravia"]], FRIENDSHIP_ITEMS["Staravia"]),# overworld Staravia
    (0x00000018, friend_item_checks[FRIENDSHIP_ITEMS["Pidgeotto"]], FRIENDSHIP_ITEMS["Pidgeotto"]),  # overworld Pidgeotto
    (0x00000014, friend_item_checks[FRIENDSHIP_ITEMS["Vaporeon"]], FRIENDSHIP_ITEMS["Vaporeon"]), # overworld Vaporeon
    (0x00000015, friend_item_checks[FRIENDSHIP_ITEMS["Golduck"]], FRIENDSHIP_ITEMS["Golduck"]), #overworld Golduck
    (0x0000001d, friend_item_checks[FRIENDSHIP_ITEMS["Pelipper"]], FRIENDSHIP_ITEMS["Pelipper"]),  # minigame Pelipper
    (0x0000002c, friend_item_checks[FRIENDSHIP_ITEMS["Krabby"]], FRIENDSHIP_ITEMS["Krabby"]),  # overworld Krabby 1
    (0x0000002d, friend_item_checks[FRIENDSHIP_ITEMS["Krabby"]], FRIENDSHIP_ITEMS["Krabby"]),  # overworld Krabby 2
    (0x0000000b, friend_item_checks[FRIENDSHIP_ITEMS["Krabby"]], FRIENDSHIP_ITEMS["Krabby"]),  # overworld Krabby 3
    (0x00000020, friend_item_checks[FRIENDSHIP_ITEMS["Krabby"]], FRIENDSHIP_ITEMS["Krabby"]),  # overworld Krabby 4
    (0x00000013, friend_item_checks[FRIENDSHIP_ITEMS["Wailord"]], FRIENDSHIP_ITEMS["Wailord"]),  # overworld Wailord bottle quest
    (0x0000002f, friend_item_checks[FRIENDSHIP_ITEMS["Corphish"]], FRIENDSHIP_ITEMS["Corphish"]), #Overworld Corphish
    (0x0000002e, friend_item_checks[FRIENDSHIP_ITEMS["Corphish"]], FRIENDSHIP_ITEMS["Corphish"]),  # Overworld Corphish 2
    (0x0000000e, friend_item_checks[FRIENDSHIP_ITEMS["Corphish"]], FRIENDSHIP_ITEMS["Corphish"]), # Overworld Corphish 3

    (0x0000001e, friend_item_checks[FRIENDSHIP_ITEMS["Gyarados"]], FRIENDSHIP_ITEMS["Gyarados"]),  # minigame Gyarados
    (0x0000001b, friend_item_checks[FRIENDSHIP_ITEMS["Feraligatr"]], FRIENDSHIP_ITEMS["Feraligatr"]),  # minigame Gyarados

]

berry_item_checks ={
    BERRIES["10 Berries"]: [(0x8037AEDE, 0xa)],
    BERRIES["20 Berries"]: [(0x8037AEDE, 0x14)],
    BERRIES["50 Berries"]: [(0x8037AEDE, 0x32)],
    BERRIES["100 Berries"]: [(0x8037AEDE, 0x64)],
}



logic_adresses = [
    # clean up pokemon id
    (0x8004faa0, 0x3d808037),
    (0x8004faa4, 0x38600000),
    (0x8004faa8, 0x906CDC20),
    (0x8004faac, 0x4e800020),

    # Friendship trigger logic
    (0x80126508,0x98030001),
    # unlock trigger logic
    (0x8018397c, 0x90047fff),
    (0x80183970, 0x38600000),
    # disable berries in friendship
    #(0x80180a3c, 0x60000000),
    # disable check is friend check for locations
    #(0x801812f8,0x60000000)
    #(0x801146f8,0x38600000),
    #(0x801812e0,0x38600000)

    #find out pokemon id
    (0x80026664,0x3ca08037),
    (0x80026668,0x9085dc20),
    (0x8002666c,0x4e800020),

    # prism trigger logic
    (0x801261e0,0x90037fff),

    # deactivate thunderbolt level up
    (0x801268f4,0x60000000)
]

tmp_addresses_disabled_friendship_overwrite= []
blocked_unlocks = [UNLOCK_ITEMS["Caterpie Unlock"],UNLOCK_ITEMS["Weedle Unlock"],UNLOCK_ITEMS["Shroomish Unlock"],UNLOCK_ITEMS["Magikarp Unlock"]]
prisma_overwrites = []

driffzeppeli_address = 0x80376AE0
driffzeppeli_value = 0x40
pokemon_id_address = 0x8036dc20
stage_id_address = 0x8036AEF0 # word
is_in_menu_address = 0x80482F04
meadow_zone_stage_id = 0x13002E8
beach_zone_stage_id = 0x1591C24
main_menu_stage_id = 0x6FC360
main_menu2_stage_id = 0x93BEA0
main_menu3_stage_id = 0x2A080
intro_stage_id= 0x940220
treehouse_stage_id=0x13282F8
bulbasaur_minigame_stage_id = 0x98F584
venusaur_minigame_stage_id = 0xA81938
pelliper_minigame_stage_id = 0xD92358
gyarados_minigame_stage_id = 0xC61408

green_zone_trigger_address = stage_id_address
green_zone_trigger_value = intro_stage_id
green_zone_states_word = [
    (0x8037500C,0x44C60), # set state before beach zone
    (0x80377E1C,0x2), # init prisma for minigame bulbasaur
    (0x80376DA8,0x2), # init prisma for minigame Venusaur
    (0x8037502E,0x5840) # skip munchlax tutorial
]
green_zone_states_byte = [
    (0x8037AEEF,0x11), #init thunderbolt and dash
    (0x8037AEC9,0x37), #init status menu
    (0x80376AF7,0x10), # activate Celebi
    (0x80375021,0x20) #skipping driffzepeli quest
]
green_zone_keep_state = [
    (0x8037501B,0x08) # blocking photo quest so beach zone is not unlocked
]

beach_zone_trigger_address = 0x8037500D
beach_zone_trigger_value = 0x7d0
beach_zone_states_word = [
    (0x803772B8,0x2), # init prisma Pelipper
    (0x80377174,0x2) # init prisma Gyarados
]
beach_zone_states_hword = [
(0x8037500D,0x870) #world state
]
beach_zone_states_byte = [
    (0x80376af0,0x08),# unlock bidoof in beach zone
    (0x80375026,0x03), #bidoof only first bridge unlocked setup
    (0x80375010,0x3b), #building all bridges
] #next stage unlock 0x80375012, 0x14

region_unlock_item_checks = {
    REGION_UNLOCK["Beach Zone Unlock"]: [(0x8037500D,0x7d0)]
}

# bidifas event going 66 6a ... but depends on base value | maybe masking
