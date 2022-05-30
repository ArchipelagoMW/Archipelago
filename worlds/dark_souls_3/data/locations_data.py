
class LocationData:

    @staticmethod
    def create_dictionary_table():
        pass


# Regular expression to parse the Python list https://regex101.com/r/XdtiLR/2
# List of location https://darksouls3.wiki.fextralife.com/Locations

cemetery_of_ash_table = {
    "Broken Straight Sword": 0x001EF9B0,  # Multiple
    "East-West Shield": 0x0142B930,
    "Ashen Estus Flask": 0x400000BF,  # Flask
}

fire_link_shrine_table = {
    "Fire Keeper Robe": 0x140D9CE8,
    "Fire Keeper Gloves": 0x140DA0D0,
    "Fire Keeper Skirt": 0x140DA4B8,
    "Estus Ring": 0x200050DC,
    "Fire Keeper Soul": 0x40000186,
    "Covetous Silver Serpent Ring": 0x20004FB0,
    "Seed of a Giant Tree #1": 0x400001B8,  # Multiple
    "Estus Flask Shard #1": 0x4000085D,  # Multiple #Flask
}

high_wall_of_lothric = {
    "Deep Battle Axe": 0x0006AFA54,
    "Club": 0x007A1200,
    "Deserter Trousers": 0x126265B8,
    "Claymore": 0x005BDBA0,
    "Binoculars": 0x40000173,
    "Longbow": 0x00D689E0,
    "Mail Breaker": 0x002DEDD0,
    "Broadsword": 0x001ED2A0,
    "Silver Eagle Kite Shield": 0x014418C0,
    "Astora's Straight Sword": 0x002191C0,
    "Cell Key": 0x400007DA,
    "Rapier": 0x002E14E0,
    "Ring of Sacrifice #1": 0x20004EF2,  # Multiple
    "Lucerne": 0x0098BD90,
    "Estus Flask Shard #2": 0x4000085D,  # Multiple #Flask
    "Refined Gem #1": 0x40000460,       # Shop #Multiple
}

undead_settlement_table = {
    "Small Leather Shield": 0x01315410,
    "Whip": 0x00B71B00,
    "Reinforced Club": 0x007A8730,
    "Blue Wooden Shield": 0x0143F1B0,

    "Cleric Hat": 0x11D905C0,
    "Cleric Blue Robe": 0x11D909A8,
    "Cleric Gloves": 0x11D90D90,
    "Cleric Trousers": 0x11D91178,

    "Mortician's Ashes": 0x4000083B,  # Shop
    "Caestus": 0x00A7FFD0,
    "Plank Shield": 0x01346150,
    "Flame Stoneplate Ring": 0x20004E52,
    "Caduceus Round Shield": 0x01341330,
    "Fire Clutch Ring": 0x2000501E,
    "Partizan": 0x0089C970,


    "Red Hilted Halberd": 0x009AB960,
    "Saint's Talisman": 0x00CACA10,
    "Irithyll Straight Sword": 0x0020A760,
    "Fire Gem #1": 0x4000047E,  # Shop #Multiple
    "Large Club": 0x007AFC60,
    "Northern Helm": 0x116E3600,
    "Northern Armor": 0x116E39E8,
    "Northern Gloves": 0x116E3DD0,
    "Northern Trousers": 0x116E41B8,
    "Flynn's Ring": 0x2000503C,
    "Mirrah Chain Mail": 0x14B575A8,
    "Mirrah Chain Gloves": 0x14B57990,
    "Mirrah Chain Leggings": 0x14B57D78,
    "Chloranthy Ring": 0x20004E2A,
    "Loincloth": 0x148F57D8,
    "Wargod Wooden Shield": 0x0144DC10,

    "Loretta's Bone": 0x40000846,
    "Estus Flask Shard #3": 0x4000085D,  # Multiple #Flask
    "Undead Bone Shard #1": 0x4000085F,  # Multiple #Flask
}

road_of_sacrifice_table = {
    "Shriving Stone": 0x400004E2,  # Shop #Multiple
    "Brigand Twindaggers": 0x00F50E60,

    "Brigand Hood": 0x148009E0,
    "Brigand Armor": 0x14800DC8,
    "Brigand Gauntlets": 0x148011B0,
    "Brigand Trousers": 0x14801598,

    "Butcher Knife": 0x006BE130,
    "Brigand Axe": 0x006B1DE0,
    "Braille Divine Tome of Carim": 0x40000847,  # Shop
    "Morne's Ring": 0x20004F1A,
    "Twin Dragon Greatshield": 0x01513820,
    "Heretic's Staff": 0x00C8F550,

    "Sorcerer Hood": 0x11C9C380,
    "Sorcerer Robe": 0x11C9C768,
    "Sorcerer Gloves": 0x11C9CB50,
    "Sorcerer Trousers": 0x11C9CF38,

    "Sage Ring": 0x20004F38,

    "Fallen Knight Helm": 0x1121EAC0,
    "Fallen Knight Armor": 0x1121EEA8,
    "Fallen Knight Gauntlets": 0x1121F290,
    "Fallen Knight Trousers": 0x1121F678,

    "Conjurator Hood": 0x149E8E60,
    "Conjurator Robe": 0x149E9248,
    "Conjurator Manchettes": 0x149E9630,
    "Conjurator Boots": 0x149E9A18,

    "Great Swamp Pyromancy Tome": 0x4000084F,  # Shop

    "Great Club": 0x007B4A80,
    "Exile Greatsword": 0x005DD770,

    "Farron Coal ": 0x40000837,  # Shop

    "Sellsword Twinblades": 0x00F42400,
    "Sellsword Helm": 0x11481060,
    "Sellsword Armor": 0x11481448,
    "Sellsword Gauntlet": 0x11481830,
    "Sellsword Trousers": 0x11481C18,

    "Golden Falcon Shield": 0x01354BB0,
    "Ring of Sacrifice #2": 0x20004EF2,  # Multiple

    "Herald Helm": 0x114FB180,
    "Herald Armor": 0x114FB568,
    "Herald Gloves": 0x114FB950,
    "Herald Trousers": 0x114FBD38,

    "Grass Crest Shield": 0x01437C80,
    "Estus Flask Shard #4": 0x4000085D,  # Multiple #Flask
}

cathedral_of_the_deep_table = {
    "Paladin's Ashes": 0x4000083D,      #Shop
    "Spider Shield": 0x01435570,
    "Crest Shield": 0x01430750,
    "Notched Whip": 0x00B7DE50,
    "Astora Greatsword": 0x005C9EF0,
    "Executioner's Greatsword": 0x0021DFE0,
    "Curse Ward Greatshield": 0x01518640,
    "Saint-tree Bellvine": 0x00C9DFB0,
    "Poisonbite Ring": 0x20004E8E,

    "Deep Gem #1": 0x4000049C,              #Shop #Multiple
    "Lloyd's Sword Ring": 0x200050B4,
    "Seek Guidance": 0x40360420,

    "Aldrich's Sapphire": 0x20005096,
    "Deep Braille Divine Tome": 0x40000860,  # Shop

    "Saint Bident": 0x008C1360,
    "Maiden Hood": 0x14BD12E0,
    "Maiden Robe": 0x14BD16C8,
    "Maiden Gloves": 0x14BD1AB0,
    "Maiden Skirt": 0x14BD1E98,
    "Drang Armor": 0x154E0C28,
    "Drang Gauntlets": 0x154E1010,
    "Drang Shoes": 0x154E13F8,
    "Pale Tongue #1": 0x40000175,
    "Drang Hammers": 0x00F61FD0,
    "Deep Ring": 0x20004F60,

    "Archdeacon White Crown": 0x13EF1480,
    "Archdeacon Holy Garb": 0x13EF1868,
    "Archdeacon Skirt": 0x13EF2038,
    "Spiked Shield": 0x01426B10,
    "Barbed Straight Sword": 0x0021B8D0,

    "Arbalest": 0x00D662D0,
    "Pale Tongue #2": 0x40000175,
    "Blessed Gem #1": 0x400004CE,
    "Helm of Thorns": 0x15B8D800,
    "Armor of Thorns": 0x15B8DBE8,
    "Gauntlets of Thorns": 0x15B8DFD0,
    "Leggings of Thorns": 0x15B8E3B8,

    "Estus Flask Shard #5": 0x4000085D,  # Multiple #Flask
    "Undead Bone Shard #2": 0x4000085F,  # Multiple #Flask
}

farron_keep_table = {
    "Ragged Mask": 0x148F4C20,
    "Iron Flesh": 0x40251430,
    "Golden Scroll": 0x4000085C,

    "Antiquated Dress": 0x15D76068,
    "Antiquated Gloves": 0x15D76450,
    "Antiquated Skirt": 0x15D76838,

    "Nameless Knight Helm": 0x143B5FC0,
    "Nameless Knight Armor": 0x143B63A8,
    "Nameless Knight Gauntlets": 0x143B6790,
    "Nameless Knight Leggings": 0x143B6B78,

    "Sunlight Talisman": 0x00CA54E0,
    "Wolf's Blood Swordgrass": 0x4000016E,
    "Greatsword": 0x005C50D0,

    "Sage's Coal": 0x40000838,  # Shop #Unique
    "Stone Parma": 0x01443FD0,
    "Poison Gem #1": 0x400004B0,  # Shop #Multiple
    "Sage's Scroll": 0x40000854,
    "Crown of Dusk": 0x15D75C80,

    "Lingering Dragoncrest Ring": 0x20004F2E,
    "Pharis's Hat": 0x1487AB00,
    "Black Bow of Pharis": 0x00D7E970,

    "Dreamchaser's Ashes": 0x4000083C,  # Shop #Unique
    "Great Axe": 0x006B9310,  # Multiple
    "Dragon Crest Shield": 0x01432E60,
    "Lightning Spear": 0x40362B30,
    "Shriving Stone #2": 0x400004E2,  # Shop #Multiple
    "Atonement": 0x4039ADA0,
    "Hollow Gem #1": 0x400004D8,  # Shop #Multiple
    "Great Magic Weapon": 0x40140118,

    "Estus Flask Shard #6": 0x4000085D,  # Multiple #Flask
    "Undead Bone Shard #3": 0x4000085F,  # Multiple #Flask
}

catacombs_of_carthus_table = {
    "Sharp Gem": 0x40000456,
    "Carthus Pyromancy Tome": 0x40000850,
    "Carthus Milkring": 0x20004FE2,
    "Grave Warden's Ashes": 0x4000083E,
    "Deep Gem": 0x4000049C,
    "Knight Slayer's Ring": 0x20005000,
    "Carthus Bloodring": 0x200050FA,
    "Grave Warden Pyromancy Tome": 0x40000853,
    "Old Sage's Blindfold": 0x11945BA0,
    "Witch's Ring": 0x20004F11,
    "Black Blade": 0x004CC070,
    "Undead Bone Shard #4": 0x4000085F,
}

smouldering_lake_table = {
    "Shield of Want": 0x0144B500,
    "Speckled Stoneplate Ring": 0x20004E7A,
    "Chaos Gem #1": 0x40000488,
    "Dragonrider Bow": 0x00D6B0F0,
    "Lightning Stake": 0x40389C30,
    "Fire Gem #2": 0x4000047E,
    "Izalith Pyromancy Tome": 0x40000851,
    "Black Knight Sword": 0x005F5E10,
    "Quelana Pyromancy Tome": 0x40000852,
    "Toxic Mist": 0x4024F108,
    "White Hair Talisman": 0x00CAF120,
    "Izalith Staff": 0x00C96A80,
    "Sacred Flame": 0x40284880,
    "Fume Ultra Greatsword": 0x0060E4B0,
    "Black Iron Greatshield": 0x0150EA00,

    "Estus Flask Shard #7": 0x4000085D,
    "Undead Bone Shard #5": 0x4000085F,
    "Undead Bone Shard #6": 0x4000085F,
}

irithyll_of_the_boreal_valley_table = {
    "Dorhys' Gnawing": 0x40363EB8,
    "Witchtree Branch": 0x00C94370,
    "Magic Clutch Ring": 0x2000500A,
    "Lightning Gem #1": 0x40000492,
    "Ring of the Sun's First Born": 0x20004F1B,
    "Proof of a Concord Kept #1": 0x40000174,
    "Roster of Knights": 0x4000006C,
    "Undead Bone Shard #7": 0x4000085F,
    "Chameleon": 0x4014ACF8,
    "Pontiff's Right Eye": 0x2000510E,

    "Shriving Stone": 0x400004E2,
    "Yorshka's Spear": 0x008C3A70,
    "Blood Gem #1": 0x400004BA,
    "Ring of Sacrifice #3": 0x20004EF2,
    "Great Heal": 0x40356FB0,

    "Smough's Great Hammer": 0x007E30B0,
    "Leo Ring": 0x20004EE8,
    "Greirat's Ashes": 0x4000083F,
    "Excrement-covered Ashes": 0x40000862,

    "Dark Stoneplate Ring": 0x20004E70,
    "Deep Gem #3": 0x4000049C,
    "Easterner's Ashes": 0x40000868,
    "Painting Guardian's Curved Sword": 0x003E6890,
    "Painting Guardian Hood": 0x156C8CC0,
    "Painting Guardian Gown": 0x156C90A8,
    "Painting Guardian Gloves": 0x156C9490,
    "Painting Guardian Waistcloth": 0x156C9878,
    "Dragonslayer Greatbow": 0x00CF8500,
    "Reversal Ring": 0x20005104,
    "Brass Helm": 0x1501BD00,
    "Brass Armor": 0x1501C0E8,
    "Brass Gauntlets": 0x1501C4D0,
    "Brass Leggings": 0x1501C8B8,
    "Ring of Favor": 0x20004E3E,
    "Golden Ritual Spear": 0x00C83200,
}

irithyll_dungeon_table = {
    "Bellowing Dragoncrest Ring": 0x20004F07,
    "Jailbreaker's Key": 0x400007D7,
    "Prisoner Chief's Ashes": 0x40000863,
    "Old Sorcerer Hat": 0x1496ED40,
    "Old Sorcerer Coat": 0x1496F128,
    "Old Sorcerer Gauntlets": 0x1496F510,
    "Old Sorcerer Boots": 0x1496F8F8,
    "Great Magic Shield": 0x40144F38,
    "Estus Flask Shard #8": 0x4000085D,

    "Dragon Torso Stone": 0x4000017A,
    "Lightning Blade": 0x4036C770,
    "Profaned Coal": 0x4000083A,
    "Xanthous Ashes": 0x40000864,
    "Old Cell Key": 0x400007DC,
    "Pickaxe": 0x007DE290,
    "Profaned Flame": 0x402575D8,
    "Covetous Gold Serpent Ring": 0x20004FA6,
    "Jailer's Key Ring": 0x400007D8,
    "Dusk Crown Ring": 0x20004F4C,
    "Dark Clutch Ring": 0x20005028,
}

profaned_capital_table = {
    "Cursebite Ring": 0x20004E98,
    "Poison Gem #2": 0x400004B0,
    "Shriving Stone #4": 0x400004E2,
    "Court Sorcerer Hood": 0x11BA8140,
    "Court Sorcerer Robe": 0x11BA8528,
    "Court Sorcerer Gloves": 0x11BA8910,
    "Court Sorcerer Trousers": 0x11BA8CF8,
    "Wrath of the Gods": 0x4035E0F8,
    "Covetous Gold Serpent Ring": 0x20004FA6,
    "Jailer's Key Ring": 0x400007D8,
    "Logan's Scroll": 0x40000855,
    "Eleonora": 0x006CCB90,
    "Court Sorcerer's Staff": 0x00C91C60,
    "Undead Bone Shard #8": 0x4000085F,
    "Greatshield of Glory": 0x01515F30,
}

anor_londo_table = {
    "Giant's Coal": 0x40000839,
    "Proof of a Concord Kept": 0x40000174,
    "Sun Princess Ring": 0x20004FBA,
    "Estus Flask Shard #9": 0x4000085D,
    "Aldrich's Ruby": 0x2000508C,
}

lothric_castle_table = {
    "Hood of Prayer": 0x13AA6A60,
    "Robe of Prayer": 0x13AA6E48,
    "Skirt of Prayer": 0x13AA7618,

    "Sacred Bloom Shield": 0x013572C0,
    "Winged Knight Helm": 0x12EBAE40,
    "Winged Knight Armor": 0x12EBB228,
    "Winged Knight Gauntlets": 0x12EBB610,
    "Winged Knight Leggings": 0x12EBB9F8,
    "Estus Flask Shard #10": 0x4000085D,

    "Greatlance": 0x008A8CC0,
    "Sniper Crossbow": 0x00D83790,
    "Raw Gem #1": 0x400004C4,
    "Spirit Tree Crest Shield": 0x014466E0,
    "Refined Gem #2": 0x40000460,
    "Red Tearstone Ring": 0x20004ECA,
    "Caitha's Chime": 0x00CA06C0,
    "Braille Divine Tome of Lothric": 0x40000848,
    "Knight's Ring": 0x20004FEC,
    "Sunlight Straight Sword": 0x00203230,
}

consumed_king_garden_table = {
    "Estus Flask Shard #11": 0x4000085D,
    "Ring of Sacrifice #4": 0x20004EF2,
    "Dark Gem": 0x400004A6,
    "Dragonscale Ring": 0x2000515E,
    "Shadow Mask": 0x14D3F640,
    "Shadow Garb": 0x14D3FA28,
    "Shadow Gauntlets": 0x14D3FE10,
    "Shadow Leggings": 0x14D401F8,
    "Claw": 0x00A7D8C0,
}

grand_archives_table = {
    "Avelyn": 0x00D6FF10,
    "Witch's Locks": 0x00B7B740,
    "Power Within": 0x40253B40,
    "Scholar Ring": 0x20004EB6,
    "Soul Stream": 0x4018B820,
    "Fleshbite Ring": 0x20004EA2,
    "Crystal Chime": 0x00CA2DD0,
    "Shriving Stone #5": 0x400004E2,
    "Hollow Gem #2": 0x400004D8,
    "Undead Bone Shard #9": 0x4000085F,
    "Golden Wing Crest Shield": 0x0143CAA0,
    "Sage's Crystal Staff": 0x00C8CE40,
    "Onikiri and Ubadachi": 0x00F58390,
    "Hunter's Ring": 0x20004FF6,
    "Divine Pillars of Light": 0x4038C340,
    "Blessed Gem #2": 0x400004CE,
    "Estus Flask Shard #12": 0x4000085D,
}

untended_graves_table = {
    "Ashen Estus Ring": 0x200050E6,
    "Black Knight Glaive": 0x009AE070,
    "Hornet Ring": 0x20004F9C,
    "Chaos Blade": 0x004C9960,
    "Seed of a Giant Tree #2": 0x400001B8,
    "Blacksmith Hammer": 0x007E57C0,
    "Eyes of a Fire Keeper": 0x4000085A,
    "Coiled Sword Fragment": 0x4000015F,
}

archdragon_peak_table = {
    "Lightning Gem #2": 0x40000492,
    "Lightning Clutch Ring": 0x20005014,
    "Ancient Dragon Greatshield": 0x013599D0,
    "Ring of Steel Protection": 0x20004E48,
    "Calamity Ring": 0x20005078,
    "Drakeblood Greatsword": 0x00609690,
    "Dragonslayer Spear": 0x008CAFA0,

    "Thunder Stoneplate Ring": 0x20004E5C,
    "Great Magic Barrier": 0x40365628,
    "Dragon Chaser's Ashes": 0x40000867,
    "Twinkling Dragon Torso Stone": 0x40000184,
    "Dragonslayer Helm": 0x158B1140,
    "Dragonslayer Armor": 0x158B1528,
    "Dragonslayer Gauntlets": 0x158B1910,
    "Dragonslayer Leggings": 0x158B1CF8,
    "Ricard's Rapier": 0x002E3BF0,
}


key_items_table = {
    "Grand Archives Key": 0x400007DE,
    "Storm Ruler": 0x006132D0,
    "Small Doll": 0x400007D5,
    "Path of the Dragon Gesture": 0x40002346,
    # "Coiled Sword": 0x40000859,            #Useless item, it can be used if looted or not
}

dictionary_table = {**cemetery_of_ash_table, ** fire_link_shrine_table, **high_wall_of_lothric, **undead_settlement_table, **road_of_sacrifice_table,
                    **cathedral_of_the_deep_table, **farron_keep_table, **catacombs_of_carthus_table, **smouldering_lake_table, **irithyll_of_the_boreal_valley_table,
                    **irithyll_dungeon_table, **profaned_capital_table, **anor_londo_table, **lothric_castle_table, **consumed_king_garden_table,
                    **grand_archives_table, **untended_graves_table, **archdragon_peak_table}
