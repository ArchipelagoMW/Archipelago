"""
Tools used to create this list :
List of all items https://docs.google.com/spreadsheets/d/1nK2g7g6XJ-qphFAk1tjP3jZtlXWDQY-ItKLa_sniawo/edit#gid=1551945791
Regular expression parser https://regex101.com/r/XdtiLR/2
List of locations https://darksouls3.wiki.fextralife.com/Locations
"""

cemetery_of_ash_table = {
}

fire_link_shrine_table = {
    # "FS: Coiled Sword": 0x40000859, You can still light the Firelink Shrine fire whether you have it or not, useless
    "FS: Broken Straight Sword": 0x001EF9B0,
    "FS: East-West Shield": 0x0142B930,
    "FS: Uchigatana": 0x004C4B40,
    "FS: Master's Attire": 0x148F5008,
    "FS: Master's Gloves": 0x148F53F0,
}

firelink_shrine_bell_tower_table = {
    "FSBT: Covetous Silver Serpent Ring": 0x20004FB0,
    "FSBT: Fire Keeper Robe": 0x140D9CE8,
    "FSBT: Fire Keeper Gloves": 0x140DA0D0,
    "FSBT: Fire Keeper Skirt": 0x140DA4B8,
    "FSBT: Estus Ring": 0x200050DC,
    "FSBT: Fire Keeper Soul": 0x40000186
}

high_wall_of_lothric = {
    "HWL: Deep Battle Axe": 0x0006AFA54,
    "HWL: Club": 0x007A1200,
    "HWL: Claymore": 0x005BDBA0,
    "HWL: Binoculars": 0x40000173,
    "HWL: Longbow": 0x00D689E0,
    "HWL: Mail Breaker": 0x002DEDD0,
    "HWL: Broadsword": 0x001ED2A0,
    "HWL: Silver Eagle Kite Shield": 0x014418C0,
    "HWL: Astora's Straight Sword": 0x002191C0,
    "HWL: Cell Key": 0x400007DA,
    "HWL: Rapier": 0x002E14E0,
    "HWL: Lucerne": 0x0098BD90,
    "HWL: Small Lothric Banner": 0x40000836,
    "HWL: Basin of Vows": 0x40000845,
    "HWL: Soul of Boreal Valley Vordt": 0x400002CF,
    "HWL: Soul of the Dancer": 0x400002CA,
    "HWL: Way of Blue Covenant": 0x2000274C,
    "HWL: Greirat's Ashes": 0x4000083F,
}

undead_settlement_table = {
    "US: Small Leather Shield": 0x01315410,
    "US: Whip": 0x00B71B00,
    "US: Reinforced Club": 0x007A8730,
    "US: Blue Wooden Shield": 0x0143F1B0,

    "US: Cleric Hat": 0x11D905C0,
    "US: Cleric Blue Robe": 0x11D909A8,
    "US: Cleric Gloves": 0x11D90D90,
    "US: Cleric Trousers": 0x11D91178,

    "US: Mortician's Ashes": 0x4000083B,
    "US: Caestus": 0x00A7FFD0,
    "US: Plank Shield": 0x01346150,
    "US: Flame Stoneplate Ring": 0x20004E52,
    "US: Caduceus Round Shield": 0x01341330,
    "US: Fire Clutch Ring": 0x2000501E,
    "US: Partizan": 0x0089C970,
    "US: Bloodbite Ring": 0x20004E84,

    "US: Red Hilted Halberd": 0x009AB960,
    "US: Saint's Talisman": 0x00CACA10,
    "US: Irithyll Straight Sword": 0x0020A760,
    "US: Large Club": 0x007AFC60,
    "US: Northern Helm": 0x116E3600,
    "US: Northern Armor": 0x116E39E8,
    "US: Northern Gloves": 0x116E3DD0,
    "US: Northern Trousers": 0x116E41B8,
    "US: Flynn's Ring": 0x2000503C,

    "US: Mirrah Vest": 0x15204568,
    "US: Mirrah Gloves": 0x15204950,
    "US: Mirrah Trousers": 0x15204D38,

    "US: Chloranthy Ring": 0x20004E2A,
    "US: Loincloth": 0x148F57D8,
    "US: Wargod Wooden Shield": 0x0144DC10,

    "US: Loretta's Bone": 0x40000846,

    "US: Hand Axe": 0x006ACFC0,
    "US: Great Scythe": 0x00989680,
    "US: Soul of the Rotted Greatwood": 0x400002D7,
    "US: Hawk Ring": 0x20004F92,
    "US: Warrior of Sunlight Covenant": 0x20002738,
}

road_of_sacrifice_table = {
    "RS: Brigand Twindaggers": 0x00F50E60,

    "RS: Brigand Hood": 0x148009E0,
    "RS: Brigand Armor": 0x14800DC8,
    "RS: Brigand Gauntlets": 0x148011B0,
    "RS: Brigand Trousers": 0x14801598,

    "RS: Butcher Knife": 0x006BE130,
    "RS: Brigand Axe": 0x006B1DE0,
    "RS: Braille Divine Tome of Carim": 0x40000847,
    "RS: Morne's Ring": 0x20004F1A,
    "RS: Twin Dragon Greatshield": 0x01513820,
    "RS: Heretic's Staff": 0x00C8F550,

    "RS: Sorcerer Hood": 0x11C9C380,
    "RS: Sorcerer Robe": 0x11C9C768,
    "RS: Sorcerer Gloves": 0x11C9CB50,
    "RS: Sorcerer Trousers": 0x11C9CF38,

    "RS: Sage Ring": 0x20004F38,

    "RS: Fallen Knight Helm": 0x1121EAC0,
    "RS: Fallen Knight Armor": 0x1121EEA8,
    "RS: Fallen Knight Gauntlets": 0x1121F290,
    "RS: Fallen Knight Trousers": 0x1121F678,

    "RS: Conjurator Hood": 0x149E8E60,
    "RS: Conjurator Robe": 0x149E9248,
    "RS: Conjurator Manchettes": 0x149E9630,
    "RS: Conjurator Boots": 0x149E9A18,

    "RS: Great Swamp Pyromancy Tome": 0x4000084F,

    "RS: Great Club": 0x007B4A80,
    "RS: Exile Greatsword": 0x005DD770,

    "RS: Farron Coal ": 0x40000837,

    "RS: Sellsword Twinblades": 0x00F42400,
    "RS: Sellsword Helm": 0x11481060,
    "RS: Sellsword Armor": 0x11481448,
    "RS: Sellsword Gauntlet": 0x11481830,
    "RS: Sellsword Trousers": 0x11481C18,

    "RS: Golden Falcon Shield": 0x01354BB0,

    "RS: Herald Helm": 0x114FB180,
    "RS: Herald Armor": 0x114FB568,
    "RS: Herald Gloves": 0x114FB950,
    "RS: Herald Trousers": 0x114FBD38,

    "RS: Grass Crest Shield": 0x01437C80,
    "RS: Soul of a Crystal Sage": 0x400002CB,
    "RS: Great Swamp Ring": 0x20004F10,
}

cathedral_of_the_deep_table = {
    "CD: Paladin's Ashes": 0x4000083D,
    "CD: Spider Shield": 0x01435570,
    "CD: Crest Shield": 0x01430750,
    "CD: Notched Whip": 0x00B7DE50,
    "CD: Astora Greatsword": 0x005C9EF0,
    "CD: Executioner's Greatsword": 0x0021DFE0,
    "CD: Curse Ward Greatshield": 0x01518640,
    "CD: Saint-tree Bellvine": 0x00C9DFB0,
    "CD: Poisonbite Ring": 0x20004E8E,

    "CD: Lloyd's Sword Ring": 0x200050B4,
    "CD: Seek Guidance": 0x40360420,

    "CD: Aldrich's Sapphire": 0x20005096,
    "CD: Deep Braille Divine Tome": 0x40000860,

    "CD: Saint Bident": 0x008C1360,
    "CD: Maiden Hood": 0x14BD12E0,
    "CD: Maiden Robe": 0x14BD16C8,
    "CD: Maiden Gloves": 0x14BD1AB0,
    "CD: Maiden Skirt": 0x14BD1E98,
    "CD: Drang Armor": 0x154E0C28,
    "CD: Drang Gauntlets": 0x154E1010,
    "CD: Drang Shoes": 0x154E13F8,
    "CD: Drang Hammers": 0x00F61FD0,
    "CD: Deep Ring": 0x20004F60,

    "CD: Archdeacon White Crown": 0x13EF1480,
    "CD: Archdeacon Holy Garb": 0x13EF1868,
    "CD: Archdeacon Skirt": 0x13EF2038,

    "CD: Arbalest": 0x00D662D0,
    "CD: Small Doll": 0x400007D5,
    "CD: Soul of the Deacons of the Deep": 0x400002D9,
    "CD: Rosaria's Fingers Covenant": 0x20002760,
}

farron_keep_table = {
    "FK: Ragged Mask": 0x148F4C20,
    "FK: Iron Flesh": 0x40251430,
    "FK: Golden Scroll": 0x4000085C,

    "FK: Antiquated Dress": 0x15D76068,
    "FK: Antiquated Gloves": 0x15D76450,
    "FK: Antiquated Skirt": 0x15D76838,

    "FK: Nameless Knight Helm": 0x143B5FC0,
    "FK: Nameless Knight Armor": 0x143B63A8,
    "FK: Nameless Knight Gauntlets": 0x143B6790,
    "FK: Nameless Knight Leggings": 0x143B6B78,

    "FK: Sunlight Talisman": 0x00CA54E0,
    "FK: Wolf's Blood Swordgrass": 0x4000016E,
    "FK: Greatsword": 0x005C50D0,

    "FK: Sage's Coal": 0x40000838,
    "FK: Stone Parma": 0x01443FD0,
    "FK: Sage's Scroll": 0x40000854,
    "FK: Crown of Dusk": 0x15D75C80,

    "FK: Lingering Dragoncrest Ring": 0x20004F2E,
    "FK: Pharis's Hat": 0x1487AB00,
    "FK: Black Bow of Pharis": 0x00D7E970,

    "FK: Dreamchaser's Ashes": 0x4000083C,
    "FK: Great Axe": 0x006B9310,
    "FK: Dragon Crest Shield": 0x01432E60,
    "FK: Lightning Spear": 0x40362B30,
    "FK: Atonement": 0x4039ADA0,
    "FK: Great Magic Weapon": 0x40140118,
    "FK: Cinders of a Lord - Abyss Watcher": 0x4000084B,
    "FK: Soul of the Blood of the Wolf": 0x400002CD,
    "FK: Soul of a Stray Demon": 0x400002E7,
    "FK: Watchdogs of Farron Covenant": 0x20002724,
}

catacombs_of_carthus_table = {
    "CC: Carthus Pyromancy Tome": 0x40000850,
    "CC: Carthus Milkring": 0x20004FE2,
    "CC: Grave Warden's Ashes": 0x4000083E,
    "CC: Carthus Bloodring": 0x200050FA,
    "CC: Grave Warden Pyromancy Tome": 0x40000853,
    "CC: Old Sage's Blindfold": 0x11945BA0,
    "CC: Witch's Ring": 0x20004F11,
    "CC: Black Blade": 0x004CC070,
    "CC: Soul of High Lord Wolnir": 0x400002D6,
    "CC: Soul of a Demon": 0x400002E3,
}

smouldering_lake_table = {
    "SL: Shield of Want": 0x0144B500,
    "SL: Speckled Stoneplate Ring": 0x20004E7A,
    "SL: Dragonrider Bow": 0x00D6B0F0,
    "SL: Lightning Stake": 0x40389C30,
    "SL: Izalith Pyromancy Tome": 0x40000851,
    "SL: Black Knight Sword": 0x005F5E10,
    "SL: Quelana Pyromancy Tome": 0x40000852,
    "SL: Toxic Mist": 0x4024F108,
    "SL: White Hair Talisman": 0x00CAF120,
    "SL: Izalith Staff": 0x00C96A80,
    "SL: Sacred Flame": 0x40284880,
    "SL: Fume Ultra Greatsword": 0x0060E4B0,
    "SL: Black Iron Greatshield": 0x0150EA00,
    "SL: Soul of the Old Demon King": 0x400002D0,
    "SL: Knight Slayer's Ring": 0x20005000,
}

irithyll_of_the_boreal_valley_table = {
    "IBV: Dorhys' Gnawing": 0x40363EB8,
    "IBV: Witchtree Branch": 0x00C94370,
    "IBV: Magic Clutch Ring": 0x2000500A,
    "IBV: Ring of the Sun's First Born": 0x20004F1B,
    "IBV: Roster of Knights": 0x4000006C,
    "IBV: Pontiff's Right Eye": 0x2000510E,

    "IBV: Yorshka's Spear": 0x008C3A70,
    "IBV: Great Heal": 0x40356FB0,

    "IBV: Smough's Great Hammer": 0x007E30B0,
    "IBV: Leo Ring": 0x20004EE8,
    "IBV: Excrement-covered Ashes": 0x40000862,

    "IBV: Dark Stoneplate Ring": 0x20004E70,
    "IBV: Easterner's Ashes": 0x40000868,
    "IBV: Painting Guardian's Curved Sword": 0x003E6890,
    "IBV: Painting Guardian Hood": 0x156C8CC0,
    "IBV: Painting Guardian Gown": 0x156C90A8,
    "IBV: Painting Guardian Gloves": 0x156C9490,
    "IBV: Painting Guardian Waistcloth": 0x156C9878,
    "IBV: Dragonslayer Greatbow": 0x00CF8500,
    "IBV: Reversal Ring": 0x20005104,
    "IBV: Brass Helm": 0x1501BD00,
    "IBV: Brass Armor": 0x1501C0E8,
    "IBV: Brass Gauntlets": 0x1501C4D0,
    "IBV: Brass Leggings": 0x1501C8B8,
    "IBV: Ring of Favor": 0x20004E3E,
    "IBV: Golden Ritual Spear": 0x00C83200,
    "IBV: Soul of Pontiff Sulyvahn": 0x400002D4,
    "IBV: Aldrich Faithful Covenant": 0x2000272E,
    "IBV: Drang Twinspears": 0x00F5AAA0,
}

irithyll_dungeon_table = {
    "ID: Bellowing Dragoncrest Ring": 0x20004F07,
    "ID: Jailbreaker's Key": 0x400007D7,
    "ID: Prisoner Chief's Ashes": 0x40000863,
    "ID: Old Sorcerer Hat": 0x1496ED40,
    "ID: Old Sorcerer Coat": 0x1496F128,
    "ID: Old Sorcerer Gauntlets": 0x1496F510,
    "ID: Old Sorcerer Boots": 0x1496F8F8,
    "ID: Great Magic Shield": 0x40144F38,

    "ID: Dragon Torso Stone": 0x4000017A,
    "ID: Lightning Blade": 0x4036C770,
    "ID: Profaned Coal": 0x4000083A,
    "ID: Xanthous Ashes": 0x40000864,
    "ID: Old Cell Key": 0x400007DC,
    "ID: Pickaxe": 0x007DE290,
    "ID: Profaned Flame": 0x402575D8,
    "ID: Covetous Gold Serpent Ring": 0x20004FA6,
    "ID: Jailer's Key Ring": 0x400007D8,
    "ID: Dusk Crown Ring": 0x20004F4C,
    "ID: Dark Clutch Ring": 0x20005028,
}

profaned_capital_table = {
    "PC: Cursebite Ring": 0x20004E98,
    "PC: Court Sorcerer Hood": 0x11BA8140,
    "PC: Court Sorcerer Robe": 0x11BA8528,
    "PC: Court Sorcerer Gloves": 0x11BA8910,
    "PC: Court Sorcerer Trousers": 0x11BA8CF8,
    "PC: Wrath of the Gods": 0x4035E0F8,
    "PC: Logan's Scroll": 0x40000855,
    "PC: Eleonora": 0x006CCB90,
    "PC: Court Sorcerer's Staff": 0x00C91C60,
    "PC: Greatshield of Glory": 0x01515F30,
    "PC: Storm Ruler": 0x006132D0,
    "PC: Cinders of a Lord - Yhorm the Giant": 0x4000084D,
    "PC: Soul of Yhorm the Giant": 0x400002DC,
}

anor_londo_table = {
    "AL: Giant's Coal": 0x40000839,
    "AL: Sun Princess Ring": 0x20004FBA,
    "AL: Aldrich's Ruby": 0x2000508C,
    "AL: Cinders of a Lord - Aldrich": 0x4000084C,
    "AL: Soul of Aldrich": 0x400002D5,
}

lothric_castle_table = {
    "LC: Hood of Prayer": 0x13AA6A60,
    "LC: Robe of Prayer": 0x13AA6E48,
    "LC: Skirt of Prayer": 0x13AA7618,

    "LC: Sacred Bloom Shield": 0x013572C0,
    "LC: Winged Knight Helm": 0x12EBAE40,
    "LC: Winged Knight Armor": 0x12EBB228,
    "LC: Winged Knight Gauntlets": 0x12EBB610,
    "LC: Winged Knight Leggings": 0x12EBB9F8,

    "LC: Greatlance": 0x008A8CC0,
    "LC: Sniper Crossbow": 0x00D83790,
    "LC: Spirit Tree Crest Shield": 0x014466E0,
    "LC: Red Tearstone Ring": 0x20004ECA,
    "LC: Caitha's Chime": 0x00CA06C0,
    "LC: Braille Divine Tome of Lothric": 0x40000848,
    "LC: Knight's Ring": 0x20004FEC,
    "LC: Sunlight Straight Sword": 0x00203230,
    "LC: Soul of Dragonslayer Armour": 0x400002D1,

    # The Black Hand Gotthard corpse appears when you have defeated Yhorm and Aldrich and triggered the cutscene
    "LC: Grand Archives Key": 0x400007DE,       # On Black Hand Gotthard corpse
    "LC: Gotthard Twinswords": 0x00F53570       # On Black Hand Gotthard corpse
}

consumed_king_garden_table = {
    "CKG: Dragonscale Ring": 0x2000515E,
    "CKG: Shadow Mask": 0x14D3F640,
    "CKG: Shadow Garb": 0x14D3FA28,
    "CKG: Shadow Gauntlets": 0x14D3FE10,
    "CKG: Shadow Leggings": 0x14D401F8,
    "CKG: Claw": 0x00A7D8C0,
    "CKG: Soul of Consumed Oceiros": 0x400002CE,
    # "CKG: Path of the Dragon Gesture": 0x40002346, I can't technically randomize it as it is a gesture and not an item
}

grand_archives_table = {
    "GA: Avelyn": 0x00D6FF10,
    "GA: Witch's Locks": 0x00B7B740,
    "GA: Power Within": 0x40253B40,
    "GA: Scholar Ring": 0x20004EB6,
    "GA: Soul Stream": 0x4018B820,
    "GA: Fleshbite Ring": 0x20004EA2,
    "GA: Crystal Chime": 0x00CA2DD0,
    "GA: Golden Wing Crest Shield": 0x0143CAA0,
    "GA: Onikiri and Ubadachi": 0x00F58390,
    "GA: Hunter's Ring": 0x20004FF6,
    "GA: Divine Pillars of Light": 0x4038C340,
    "GA: Cinders of a Lord - Lothric Prince": 0x4000084E,
    "GA: Soul of the Twin Princes": 0x400002DB,
    "GA: Sage's Crystal Staff": 0x00C8CE40,
}

untended_graves_table = {
    "UG: Ashen Estus Ring": 0x200050E6,
    "UG: Black Knight Glaive": 0x009AE070,
    "UG: Hornet Ring": 0x20004F9C,
    "UG: Chaos Blade": 0x004C9960,
    "UG: Blacksmith Hammer": 0x007E57C0,
    "UG: Eyes of a Fire Keeper": 0x4000085A,
    "UG: Coiled Sword Fragment": 0x4000015F,
    "UG: Soul of Champion Gundyr": 0x400002C8,
}

archdragon_peak_table = {
    "AP: Lightning Clutch Ring": 0x20005014,
    "AP: Ancient Dragon Greatshield": 0x013599D0,
    "AP: Ring of Steel Protection": 0x20004E48,
    "AP: Calamity Ring": 0x20005078,
    "AP: Drakeblood Greatsword": 0x00609690,
    "AP: Dragonslayer Spear": 0x008CAFA0,

    "AP: Thunder Stoneplate Ring": 0x20004E5C,
    "AP: Great Magic Barrier": 0x40365628,
    "AP: Dragon Chaser's Ashes": 0x40000867,
    "AP: Twinkling Dragon Torso Stone": 0x40000184,
    "AP: Dragonslayer Helm": 0x158B1140,
    "AP: Dragonslayer Armor": 0x158B1528,
    "AP: Dragonslayer Gauntlets": 0x158B1910,
    "AP: Dragonslayer Leggings": 0x158B1CF8,
    "AP: Ricard's Rapier": 0x002E3BF0,
    "AP: Soul of the Nameless King": 0x400002D2,
    "AP: Dragon Tooth": 0x007E09A0,
    "AP: Havel's Greatshield": 0x013376F0,
}

location_dictionary_table = {**cemetery_of_ash_table, **fire_link_shrine_table, **firelink_shrine_bell_tower_table, **high_wall_of_lothric, **undead_settlement_table, **road_of_sacrifice_table,
                             **cathedral_of_the_deep_table, **farron_keep_table, **catacombs_of_carthus_table, **smouldering_lake_table, **irithyll_of_the_boreal_valley_table,
                             **irithyll_dungeon_table, **profaned_capital_table, **anor_londo_table, **lothric_castle_table, **consumed_king_garden_table,
                             **grand_archives_table, **untended_graves_table, **archdragon_peak_table}
