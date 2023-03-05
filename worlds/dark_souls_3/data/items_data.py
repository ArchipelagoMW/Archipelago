"""
Tools used to create this list :
List of all items https://docs.google.com/spreadsheets/d/1nK2g7g6XJ-qphFAk1tjP3jZtlXWDQY-ItKLa_sniawo/edit#gid=1551945791
Regular expression parser https://regex101.com/r/XdtiLR/2
List of locations https://darksouls3.wiki.fextralife.com/Locations
"""

weapons_upgrade_5_table = {
    "Irithyll Straight Sword": 0x0020A760,
    "Chaos Blade": 0x004C9960,
    "Dragonrider Bow": 0x00D6B0F0,
    "White Hair Talisman": 0x00CAF120,
    "Izalith Staff": 0x00C96A80,
    "Fume Ultra Greatsword": 0x0060E4B0,
    "Black Knight Sword": 0x005F5E10,
    "Yorshka's Spear": 0x008C3A70,
    "Smough's Great Hammer": 0x007E30B0,
    "Dragonslayer Greatbow": 0x00CF8500,
    "Golden Ritual Spear": 0x00C83200,
    "Eleonora": 0x006CCB90,
    "Witch's Locks": 0x00B7B740,
    "Crystal Chime": 0x00CA2DD0,
    "Black Knight Glaive": 0x009AE070,
    "Dragonslayer Spear": 0x008CAFA0,
    "Caitha's Chime": 0x00CA06C0,
    "Sunlight Straight Sword": 0x00203230,
    "Firelink Greatsword": 0x0060BDA0,
    "Hollowslayer Greatsword": 0x00604870,
    "Arstor's Spear": 0x008BEC50,
    "Vordt's Great Hammer": 0x007CD120,
    "Crystal Sage's Rapier": 0x002E6300,
    "Farron Greatsword": 0x005E9AC0,
    "Wolf Knight's Greatsword": 0x00602160,
    "Dancer's Enchanted Swords": 0x00F4C040,
    "Wolnir's Holy Sword": 0x005FFA50,
    "Demon's Greataxe": 0x006CA480,
    "Demon's Fist": 0x00A84DF0,
    "Old King's Great Hammer": 0x007CF830,
    "Greatsword of Judgment": 0x005E2590,
    "Profaned Greatsword": 0x005E4CA0,
    "Yhorm's Great Machete": 0x005F0FF0,
    "Cleric's Candlestick": 0x0020F580,
    "Dragonslayer Greataxe": 0x006C7D70,
    "Moonlight Greatsword": 0x00606F80,
    "Gundyr's Halberd": 0x009A1D20,
    "Lothric's Holy Sword": 0x005FD340,
    "Lorian's Greatsword": 0x005F8520,
    "Twin Princes' Greatsword": 0x005FAC30,
    "Storm Curved Sword": 0x003E4180,
    "Dragonslayer Swordspear": 0x008BC540,
    "Sage's Crystal Staff": 0x00C8CE40,
    "Irithyll Rapier": 0x002E8A10
}

dlc_weapons_upgrade_5_table = {
    "Friede's Great Scythe": 0x009B55A0,
    "Rose of Ariandel": 0x00B82C70,
    "Demon's Scar": 0x003F04D0, # Assigned to "RC: Church Guardian Shiv"
    "Frayed Blade": 0x004D35A0, # Assigned to "RC: Ritual Spear Fragment"
    "Gael's Greatsword": 0x00227C20, # Assigned to "RC: Violet Wrappings"
    "Repeating Crossbow": 0x00D885B0, # Assigned to "RC: Blood of the Dark Souls"
    "Onyx Blade": 0x00222E00, # VILHELM FIGHT
    "Earth Seeker": 0x006D8EE0,
    "Quakestone Hammer": 0x007ECCF0,
    "Millwood Greatbow": 0x00D85EA0,
    "Valorheart": 0x00F646E0,
    "Aquamarine Dagger": 0x00116520,
    "Ringed Knight Straight Sword": 0x00225510,
    "Ledo's Great Hammer": 0x007EF400, # INVADER FIGHT
    "Ringed Knight Spear": 0x008CFDC0,
    "Crucifix of the Mad King": 0x008D4BE0,
    "Sacred Chime of Filianore": 0x00CCECF0,
    "Preacher's Right Arm": 0x00CD1400,
    "White Birch Bow": 0x00D77440,
    "Ringed Knight Paired Greatswords": 0x00F69500
}

weapons_upgrade_10_table = {
    "Broken Straight Sword": 0x001EF9B0,
    "Deep Battle Axe": 0x0006AFA54,
    "Club": 0x007A1200,
    "Claymore": 0x005BDBA0,
    "Longbow": 0x00D689E0,
    "Mail Breaker": 0x002DEDD0,
    "Broadsword": 0x001ED2A0,
    "Astora's Straight Sword": 0x002191C0,
    "Rapier": 0x002E14E0,
    "Lucerne": 0x0098BD90,
    "Whip": 0x00B71B00,
    "Reinforced Club": 0x007A8730,
    "Caestus": 0x00A7FFD0,
    "Partizan": 0x0089C970,
    "Red Hilted Halberd": 0x009AB960,
    "Saint's Talisman": 0x00CACA10,
    "Large Club": 0x007AFC60,
    "Brigand Twindaggers": 0x00F50E60,
    "Butcher Knife": 0x006BE130,
    "Brigand Axe": 0x006B1DE0,
    "Heretic's Staff": 0x00C8F550,
    "Great Club": 0x007B4A80,
    "Exile Greatsword": 0x005DD770,
    "Sellsword Twinblades": 0x00F42400,
    "Notched Whip": 0x00B7DE50,
    "Astora Greatsword": 0x005C9EF0,
    "Executioner's Greatsword": 0x0021DFE0,
    "Saint-tree Bellvine": 0x00C9DFB0,
    "Saint Bident": 0x008C1360,
    "Drang Hammers": 0x00F61FD0,
    "Arbalest": 0x00D662D0,
    "Sunlight Talisman": 0x00CA54E0,
    "Greatsword": 0x005C50D0,
    "Black Bow of Pharis": 0x00D7E970,
    "Great Axe": 0x006B9310,
    "Black Blade": 0x004CC070,
    "Blacksmith Hammer": 0x007E57C0,
    "Witchtree Branch": 0x00C94370,
    "Painting Guardian's Curved Sword": 0x003E6890,
    "Pickaxe": 0x007DE290,
    "Court Sorcerer's Staff": 0x00C91C60,
    "Avelyn": 0x00D6FF10,
    "Onikiri and Ubadachi": 0x00F58390,
    "Ricard's Rapier": 0x002E3BF0,
    "Drakeblood Greatsword": 0x00609690,
    "Greatlance": 0x008A8CC0,
    "Sniper Crossbow": 0x00D83790,
    "Claw": 0x00A7D8C0,
    "Drang Twinspears": 0x00F5AAA0,
    "Pyromancy Flame": 0x00CC77C0 #given/dropped by Cornyx
}

dlc_weapons_upgrade_10_table = {
    "Follower Sabre": 0x003EDDC0,
    "Millwood Battle Axe": 0x006D67D0,
    "Follower Javelin": 0x008CD6B0,
    "Crow Talons": 0x00A89C10,
    "Pyromancer's Parting Flame": 0x00CC9ED0,
    "Crow Quills": 0x00F66DF0,
    "Follower Torch": 0x015F1AD0,
    "Murky Hand Scythe": 0x00118C30,
    "Herald Curved Greatsword": 0x006159E0,
    "Lothric War Banner": 0x008D24D0,
    "Splitleaf Greatsword": 0x009B2E90, # SHOP ITEM
    "Murky Longstaff": 0x00CCC5E0,
}

shields_table = {
    "East-West Shield": 0x0142B930,
    "Silver Eagle Kite Shield": 0x014418C0,
    "Small Leather Shield": 0x01315410,
    "Blue Wooden Shield": 0x0143F1B0,
    "Plank Shield": 0x01346150,
    "Caduceus Round Shield": 0x01341330,
    "Wargod Wooden Shield": 0x0144DC10,
    "Grass Crest Shield": 0x01437C80,
    "Golden Falcon Shield": 0x01354BB0,
    "Twin Dragon Greatshield": 0x01513820,
    "Spider Shield": 0x01435570,
    "Crest Shield": 0x01430750,
    "Curse Ward Greatshield": 0x01518640,
    "Stone Parma": 0x01443FD0,
    "Dragon Crest Shield": 0x01432E60,
    "Shield of Want": 0x0144B500,
    "Black Iron Greatshield": 0x0150EA00,
    "Greatshield of Glory": 0x01515F30,
    "Sacred Bloom Shield": 0x013572C0,
    "Golden Wing Crest Shield": 0x0143CAA0,
    "Ancient Dragon Greatshield": 0x013599D0,
    "Spirit Tree Crest Shield": 0x014466E0,
    "Blessed Red and White Shield": 0x01343FB9
}

dlc_shields_table = {
    "Followers Shield": 0x0135C0E0,
    "Ethereal Oak Shield": 0x01450320,
    "Giant Door Shield": 0x00F5F8C0,
    "Dragonhead Shield": 0x0135E7F0,
    "Dragonhead Greatshield": 0x01452A30
}

goods_table = {
    "Soul of an Intrepid Hero": 0x4000019D,
    "Soul of the Nameless King": 0x400002D2,
    "Soul of Champion Gundyr": 0x400002C8,
    "Soul of the Twin Princes": 0x400002DB,
    "Soul of Consumed Oceiros": 0x400002CE,
    "Soul of Aldrich": 0x400002D5,
    "Soul of Yhorm the Giant": 0x400002DC,
    "Soul of Pontiff Sulyvahn": 0x400002D4,
    "Soul of the Old Demon King": 0x400002D0,
    "Soul of High Lord Wolnir": 0x400002D6,
    "Soul of the Blood of the Wolf": 0x400002CD,
    "Soul of the Deacons of the Deep": 0x400002D9,
    "Soul of a Crystal Sage": 0x400002CB,
    "Soul of Boreal Valley Vordt": 0x400002CF,
    "Soul of a Stray Demon": 0x400002E7,
    "Soul of a Demon": 0x400002E3,

    # Upgrade materials
    **{"Titanite Shard #"+str(i): 0x400003E8 for i in range(1, 11)},
    **{"Large Titanite Shard #"+str(i): 0x400003E9 for i in range(1, 11)},
    **{"Titanite Chunk #"+str(i): 0x400003EA for i in range(1, 6)},
    **{"Titanite Slab #"+str(i): 0x400003EB for i in range(1, 4)},

    # Healing
    **{"Estus Shard #"+str(i): 0x4000085D for i in range(1, 16)},
    **{"Undead Bone Shard #"+str(i): 0x4000085F for i in range(1, 6)},

    # Souls
    **{"Soul of a Great Champion #"+str(i): 0x400001A4 for i in range(1, 3)},
    **{"Soul of a Champion #"+str(i): 0x400001A3 for i in range(1, 5)},
    **{"Soul of a Venerable Old Hand #"+str(i): 0x400001A2 for i in range(1, 5)},
    **{"Soul of a Crestfallen Knight #"+str(i): 0x40000199 for i in range(1, 11)}
}

goods_2_table = { # Added by Br00ty
    "HWL: Gold Pine Resin #": 0x4000014B,
    "US: Charcoal Pine Resin #": 0x4000014A,
    "FK: Gold Pine Bundle #": 0x40000155,
    "CC: Carthus Rouge #": 0x4000014F,
    "ID: Pale Pine Resin #": 0x40000150,
    **{"Ember #"+str(i): 0x400001F4 for i in range(1, 45)},
    **{"Titanite Shard #"+str(i): 0x400003E8 for i in range(11, 16)},
    **{"Large Titanite Shard #"+str(i): 0x400003E9 for i in range(11, 16)},
    **{"Titanite Scale #" + str(i): 0x400003FC for i in range(1, 25)}
}

goods_3_table = { # Added by Br00ty
    **{"Fading Soul #" + str(i): 0x40000190 for i in range(1, 4)},
    **{"Ring of Sacrifice #"+str(i): 0x20004EF2 for i in range(1, 5)},
    **{"Homeward Bone #"+str(i): 0x4000015E for i in range(1, 17)},
    **{"Green Blossom #"+str(i): 0x40000104 for i in range(1, 7)},
    **{"Human Pine Resin #"+str(i): 0x4000014E for i in range(1, 3)},
    **{"Charcoal Pine Bundle #"+str(i): 0x40000154 for i in range(1, 3)},
    **{"Rotten Pine Resin #"+str(i): 0x40000157 for i in range(1, 3)},
    **{"Alluring Skull #"+str(i): 0x40000126 for i in range(1, 9)},
    **{"Rusted Coin #"+str(i): 0x400001C7 for i in range(1, 3)},
    **{"Rusted Gold Coin #"+str(i): 0x400001C9 for i in range(1, 3)},
    **{"Titanite Chunk #"+str(i): 0x400003EA for i in range(1, 17)},
    **{"Twinkling Titanite #"+str(i): 0x40000406 for i in range(1, 8)}
}

dlc_goods_table = {
    "Soul of Sister Friede": 0x400002E8,
    "Soul of the Demon Prince": 0x400002EA,
    "Soul of Darkeater Midir": 0x400002EB,
    "Soul of Slave Knight Gael": 0x400002E9
}

dlc_goods_2_table = { #71
    **{"Large Soul of an Unknown Traveler $"+str(i): 0x40000194 for i in range(1, 10)},
    **{"Soul of a Weary Warrior $"+str(i): 0x40000197 for i in range(1, 6)},
    **{"Large Soul of a Weary Warrior $"+str(i): 0x40000198 for i in range(1, 7)},
    **{"Soul of a Crestfallen Knight $"+str(i): 0x40000199 for i in range(1, 7)},
    **{"Large Soul of a Crestfallen Knight $"+str(i): 0x4000019A for i in range(1, 4)},
    **{"Homeward Bone $"+str(i): 0x4000015E for i in range(1, 7)},
    **{"Large Titanite Shard $"+str(i): 0x400003E9 for i in range(1, 4)},
    **{"Titanite Chunk $"+str(i): 0x400003EA for i in range(1, 16)},
    **{"Twinkling Titanite $"+str(i): 0x40000406 for i in range(1, 6)},
    **{"Rusted Coin $"+str(i): 0x400001C7 for i in range(1, 4)},
    **{"Ember $"+str(i): 0x400001F4 for i in range(1, 11)}
}

armor_table = {
    "Fire Keeper Robe": 0x140D9CE8,
    "Fire Keeper Gloves": 0x140DA0D0,
    "Fire Keeper Skirt": 0x140DA4B8,
    "Deserter Trousers": 0x126265B8,
    "Cleric Hat": 0x11D905C0,
    "Cleric Blue Robe": 0x11D909A8,
    "Cleric Gloves": 0x11D90D90,
    "Cleric Trousers": 0x11D91178,
    "Northern Helm": 0x116E3600,
    "Northern Armor": 0x116E39E8,
    "Northern Gloves": 0x116E3DD0,
    "Northern Trousers": 0x116E41B8,
    "Loincloth": 0x148F57D8,

    "Brigand Hood": 0x148009E0,
    "Brigand Armor": 0x14800DC8,
    "Brigand Gauntlets": 0x148011B0,
    "Brigand Trousers": 0x14801598,
    "Sorcerer Hood": 0x11C9C380,
    "Sorcerer Robe": 0x11C9C768,
    "Sorcerer Gloves": 0x11C9CB50,
    "Sorcerer Trousers": 0x11C9CF38,
    "Fallen Knight Helm": 0x1121EAC0,
    "Fallen Knight Armor": 0x1121EEA8,
    "Fallen Knight Gauntlets": 0x1121F290,
    "Fallen Knight Trousers": 0x1121F678,
    "Conjurator Hood": 0x149E8E60,
    "Conjurator Robe": 0x149E9248,
    "Conjurator Manchettes": 0x149E9630,
    "Conjurator Boots": 0x149E9A18,

    "Sellsword Helm": 0x11481060,
    "Sellsword Armor": 0x11481448,
    "Sellsword Gauntlet": 0x11481830,
    "Sellsword Trousers": 0x11481C18,
    "Herald Helm": 0x114FB180,
    "Herald Armor": 0x114FB568,
    "Herald Gloves": 0x114FB950,
    "Herald Trousers": 0x114FBD38,

    "Maiden Hood": 0x14BD12E0,
    "Maiden Robe": 0x14BD16C8,
    "Maiden Gloves": 0x14BD1AB0,
    "Maiden Skirt": 0x14BD1E98,
    "Drang Armor": 0x154E0C28,
    "Drang Gauntlets": 0x154E1010,
    "Drang Shoes": 0x154E13F8,
    "Archdeacon White Crown": 0x13EF1480,
    "Archdeacon Holy Garb": 0x13EF1868,
    "Archdeacon Skirt": 0x13EF2038,
    "Antiquated Dress": 0x15D76068,
    "Antiquated Gloves": 0x15D76450,
    "Antiquated Skirt": 0x15D76838,
    "Ragged Mask": 0x148F4C20,
    "Crown of Dusk": 0x15D75C80,
    "Pharis's Hat": 0x1487AB00,
    "Old Sage's Blindfold": 0x11945BA0,

    "Painting Guardian Hood": 0x156C8CC0,
    "Painting Guardian Gown": 0x156C90A8,
    "Painting Guardian Gloves": 0x156C9490,
    "Painting Guardian Waistcloth": 0x156C9878,
    "Brass Helm": 0x1501BD00,
    "Brass Armor": 0x1501C0E8,
    "Brass Gauntlets": 0x1501C4D0,
    "Brass Leggings": 0x1501C8B8,
    "Old Sorcerer Hat": 0x1496ED40,
    "Old Sorcerer Coat": 0x1496F128,
    "Old Sorcerer Gauntlets": 0x1496F510,
    "Old Sorcerer Boots": 0x1496F8F8,
    "Court Sorcerer Hood": 0x11BA8140,
    "Court Sorcerer Robe": 0x11BA8528,
    "Court Sorcerer Gloves": 0x11BA8910,
    "Court Sorcerer Trousers": 0x11BA8CF8,
    "Dragonslayer Helm": 0x158B1140,
    "Dragonslayer Armor": 0x158B1528,
    "Dragonslayer Gauntlets": 0x158B1910,
    "Dragonslayer Leggings": 0x158B1CF8,

    "Hood of Prayer": 0x13AA6A60,
    "Robe of Prayer": 0x13AA6E48,
    "Skirt of Prayer": 0x13AA7618,
    "Winged Knight Helm": 0x12EBAE40,
    "Winged Knight Armor": 0x12EBB228,
    "Winged Knight Gauntlets": 0x12EBB610,
    "Winged Knight Leggings": 0x12EBB9F8,
    "Shadow Mask": 0x14D3F640,
    "Shadow Garb": 0x14D3FA28,
    "Shadow Gauntlets": 0x14D3FE10,
    "Shadow Leggings": 0x14D401F8,
    "Outrider Knight Helm": 0x1328B740,
    "Outrider Knight Armor": 0x1328BB28,
    "Outrider Knight Gauntlets": 0x1328BF10,
    "Outrider Knight Leggings": 0x1328C2F8,

    "Cornyx's Wrap": 0x11946370,
    "Cornyx's Garb": 0x11945F88,
    "Cornyx's Skirt": 0x11946758
}

dlc_armor_table = { 
    "Slave Knight Hood": 0x134EDCE0,
    "Slave Knight Armor": 0x134EE0C8,
    "Slave Knight Gauntlets": 0x134EE4B0,
    "Slave Knight Leggings": 0x134EE898,
    "Vilhelm's Helm": 0x11312D00,
    "Vilhelm's Armor": 0x113130E8,
    "Vilhelm's Gauntlets": 0x113134D0,
    "Vilhelm's Leggings": 0x113138B8,
    #"Millwood Knight Helm": 0x139B2820, # SHOP ITEM
    #"Millwood Knight Armor": 0x139B2C08, # SHOP ITEM
    #"Millwood Knight Gauntlets": 0x139B2FF0, # SHOP ITEM
    #"Millwood Knight Leggings": 0x139B33D8, # SHOP ITEM

    "Shira's Crown": 0x11C22260,
    "Shira's Armor": 0x11C22648,
    "Shira's Gloves": 0x11C22A30,
    "Shira's Trousers": 0x11C22E18,
    #"Lapp's Helm": 0x11E84800, # SHOP ITEM
    #"Lapp's Armor": 0x11E84BE8, # SHOP ITEM
    #"Lapp's Gauntlets": 0x11E84FD0, # SHOP ITEM
    #"Lapp's Leggings": 0x11E853B8, # SHOP ITEM
    #"Ringed Knight Hood": 0x13C8EEE0, # RANDOM ENEMY DROP
    #"Ringed Knight Armor": 0x13C8F2C8, # RANDOM ENEMY DROP
    #"Ringed Knight Gauntlets": 0x13C8F6B0, # RANDOM ENEMY DROP
    #"Ringed Knight Leggings": 0x13C8FA98, # RANDOM ENEMY DROP
    #"Harald Legion Armor": 0x13D83508, # RANDOM ENEMY DROP
    #"Harald Legion Gauntlets": 0x13D838F0, # RANDOM ENEMY DROP
    #"Harald Legion Leggings": 0x13D83CD8, # RANDOM ENEMY DROP
    "Iron Dragonslayer Helm": 0x1405F7E0,
    "Iron Dragonslayer Armor": 0x1405FBC8,
    "Iron Dragonslayer Gauntlets": 0x1405FFB0,
    "Iron Dragonslayer Leggings": 0x14060398,

    "Ruin Sentinel Helm": 0x14CC5520,
    "Ruin Sentinel Armor": 0x14CC5908,
    "Ruin Sentinel Gauntlets": 0x14CC5CF0,
    "Ruin Sentinel Leggings": 0x14CC60D8,
    "Desert Pyromancer Hood": 0x14DB9760,
    "Desert Pyromancer Garb": 0x14DB9B48,
    "Desert Pyromancer Gloves": 0x14DB9F30,
    "Desert Pyromancer Skirt": 0x14DBA318,

    #"Follower Helm": 0x137CA3A0, # RANDOM ENEMY DROP
    #"Follower Armor": 0x137CA788, # RANDOM ENEMY DROP
    #"Follower Gloves": 0x137CAB70, # RANDOM ENEMY DROP
    #"Follower Boots": 0x137CAF58, # RANDOM ENEMY DROP
    #"Ordained Hood": 0x135E1F20, # SHOP ITEM
    #"Ordained Dress": 0x135E2308, # SHOP ITEM
    #"Ordained Trousers": 0x135E2AD8, # SHOP ITEM
    "Black Witch Veil": 0x14FA1BE0,
    "Black Witch Hat": 0x14EAD9A0,
    "Black Witch Garb": 0x14EADD88,
    "Black Witch Wrappings": 0x14EAE170,
    "Black Witch Trousers": 0x14EAE558,
    "White Preacher Head": 0x14153A20,
    "Antiquated Plain Garb": 0x11B2E408
}

rings_table = {
    "Estus Ring": 0x200050DC,
    "Covetous Silver Serpent Ring": 0x20004FB0,
    "Fire Clutch Ring": 0x2000501E,
    "Flame Stoneplate Ring": 0x20004E52,
    "Flynn's Ring": 0x2000503C,
    "Chloranthy Ring": 0x20004E2A,

    "Morne's Ring": 0x20004F1A,
    "Sage Ring": 0x20004F38,
    "Aldrich's Sapphire": 0x20005096,
    "Lloyd's Sword Ring": 0x200050B4,
    "Poisonbite Ring": 0x20004E8E,
    "Deep Ring": 0x20004F60,
    "Lingering Dragoncrest Ring": 0x20004F2E,
    "Carthus Milkring": 0x20004FE2,
    "Witch's Ring": 0x20004F11,
    "Carthus Bloodring": 0x200050FA,

    "Speckled Stoneplate Ring": 0x20004E7A,
    "Magic Clutch Ring": 0x2000500A,
    "Ring of the Sun's First Born": 0x20004F1B,
    "Pontiff's Right Eye": 0x2000510E, "Leo Ring": 0x20004EE8,
    "Dark Stoneplate Ring": 0x20004E70,
    "Reversal Ring": 0x20005104,
    "Ring of Favor": 0x20004E3E,
    "Bellowing Dragoncrest Ring": 0x20004F07,
    "Covetous Gold Serpent Ring": 0x20004FA6,
    "Dusk Crown Ring": 0x20004F4C,
    "Dark Clutch Ring": 0x20005028,
    "Cursebite Ring": 0x20004E98,
    "Sun Princess Ring": 0x20004FBA,
    "Aldrich's Ruby": 0x2000508C,
    "Scholar Ring": 0x20004EB6,
    "Fleshbite Ring": 0x20004EA2,
    "Hunter's Ring": 0x20004FF6,
    "Ashen Estus Ring": 0x200050E6,
    "Hornet Ring": 0x20004F9C,
    "Lightning Clutch Ring": 0x20005014,
    "Ring of Steel Protection": 0x20004E48,
    "Calamity Ring": 0x20005078,
    "Thunder Stoneplate Ring": 0x20004E5C,
    "Knight's Ring": 0x20004FEC,
    "Red Tearstone Ring": 0x20004ECA,
    "Dragonscale Ring": 0x2000515E,
    "Knight Slayer's Ring": 0x20005000,
    "Magic Stoneplate Ring": 0x20004E66,
    "Blue Tearstone Ring": 0x20004ED4 #given/dropped by Greirat
}

dlc_ring_table = {
    "Havel's Ring": 0x20004E34,
    "Chillbite Ring": 0x20005208
}

spells_table = {
    "Seek Guidance": 0x40360420,
    "Lightning Spear": 0x40362B30,
    "Atonement": 0x4039ADA0,
    "Great Magic Weapon": 0x40140118,
    "Iron Flesh": 0x40251430,
    "Lightning Stake": 0x40389C30,
    "Toxic Mist": 0x4024F108,
    "Sacred Flame": 0x40284880,
    "Dorhys' Gnawing": 0x40363EB8,
    "Great Heal": 0x40356FB0,
    "Lightning Blade": 0x4036C770,
    "Profaned Flame": 0x402575D8,
    "Wrath of the Gods": 0x4035E0F8,
    "Power Within": 0x40253B40,
    "Soul Stream": 0x4018B820,
    "Divine Pillars of Light": 0x4038C340,
    "Great Magic Barrier": 0x40365628,
    "Great Magic Shield": 0x40144F38,
    "Crystal Scroll": 0x40000856
}

dlc_spells_table = { 
    #"Boulder Heave": 0x40282170, # KILN STRAY DEMON
    #"Seething Chaos": 0x402896A0, # KILN DEMON PRINCES
    #"Old Moonlight": 0x4014FF00, # KILN MIDIR
    "Frozen Weapon": 0x401408E8,
    "Snap Freeze": 0x401A90C8,
    "Great Soul Dregs": 0x401879A0,
    "Flame Fan": 0x40258190,
    "Lightning Arrow": 0x40358B08,
    "Way of White Corona": 0x403642A0,
    "Projected Heal": 0x40364688,
    "Floating Chaos": 0x40257DA8
}

misc_items_table = {
    "Tower Key": 0x400007DF,
    "Grave Key": 0x400007D9,
    "Cell Key": 0x400007DA,
    "Small Lothric Banner": 0x40000836,
    "Mortician's Ashes": 0x4000083B,
    "Braille Divine Tome of Carim": 0x40000847,  # Shop
    "Great Swamp Pyromancy Tome": 0x4000084F,  # Shop
    "Farron Coal ": 0x40000837,  # Shop
    "Paladin's Ashes": 0x4000083D,  # Shop
    "Deep Braille Divine Tome": 0x40000860,  # Shop
    "Small Doll": 0x400007D5,
    "Golden Scroll": 0x4000085C,
    "Sage's Coal": 0x40000838,  # Shop #Unique
    "Sage's Scroll": 0x40000854,
    "Dreamchaser's Ashes": 0x4000083C,  # Shop #Unique
    "Cinders of a Lord - Abyss Watcher": 0x4000084B,
    "Cinders of a Lord - Yhorm the Giant": 0x4000084D,
    "Cinders of a Lord - Aldrich": 0x4000084C,
    "Grand Archives Key": 0x400007DE,
    "Basin of Vows": 0x40000845,
    "Cinders of a Lord - Lothric Prince": 0x4000084E,
    "Carthus Pyromancy Tome": 0x40000850,
    "Grave Warden's Ashes": 0x4000083E,
    "Grave Warden Pyromancy Tome": 0x40000853,
    "Quelana Pyromancy Tome": 0x40000852,
    "Izalith Pyromancy Tome": 0x40000851,
    "Greirat's Ashes": 0x4000083F,
    "Excrement-covered Ashes": 0x40000862,
    "Easterner's Ashes": 0x40000868,
    "Prisoner Chief's Ashes": 0x40000863,
    "Jailbreaker's Key": 0x400007D7,
    "Dragon Torso Stone": 0x4000017A,
    "Profaned Coal": 0x4000083A,
    "Xanthous Ashes": 0x40000864,
    "Old Cell Key": 0x400007DC,
    "Jailer's Key Ring": 0x400007D8,
    "Logan's Scroll": 0x40000855,
    "Storm Ruler": 0x006132D0,
    "Giant's Coal": 0x40000839,
    "Coiled Sword Fragment": 0x4000015F,
    "Dragon Chaser's Ashes": 0x40000867,
    "Twinkling Dragon Torso Stone": 0x40000184,
    "Braille Divine Tome of Lothric": 0x40000848,
    "Irina's Ashes": 0x40000843,
    "Karla's Ashes": 0x40000842,
    "Cornyx's Ashes": 0x40000841,
    "Orbeck's Ashes": 0x40000840
}

dlc_misc_table = {
    "Captains Ashes": 0x4000086A,
    "Contraption Key": 0x4000086B, # Needed for Painted World
    "Small Envoy Banner": 0x4000086C # Needed to get to Ringed City from Dreg Heap
}

key_items_list = {
    "Small Lothric Banner",
    "Basin of Vows",
    "Small Doll",
    "Storm Ruler",
    "Grand Archives Key",
    "Cinders of a Lord - Abyss Watcher",
    "Cinders of a Lord - Yhorm the Giant",
    "Cinders of a Lord - Aldrich",
    "Cinders of a Lord - Lothric Prince",
    "Mortician's Ashes",
    "Cell Key",
    "Tower Key",
    "Jailbreaker's Key",
    "Prisoner Chief's Ashes",
    "Old Cell Key",
    "Jailer's Key Ring",
    "Contraption Key",
    "Small Envoy Banner"
}

item_tables = [weapons_upgrade_5_table, weapons_upgrade_10_table, shields_table,
               armor_table, rings_table, spells_table, misc_items_table, goods_table, goods_2_table, goods_3_table,
               dlc_weapons_upgrade_5_table, dlc_weapons_upgrade_10_table, dlc_shields_table, dlc_goods_table,
               dlc_armor_table, dlc_spells_table, dlc_ring_table, dlc_misc_table, dlc_goods_2_table]

item_dictionary = {**weapons_upgrade_5_table, **weapons_upgrade_10_table, **shields_table,
                   **armor_table, **rings_table, **spells_table, **misc_items_table, **goods_table, **goods_2_table,
                   **goods_3_table, **dlc_weapons_upgrade_5_table, **dlc_weapons_upgrade_10_table, **dlc_shields_table,
                   **dlc_goods_table, **dlc_armor_table, **dlc_spells_table, **dlc_ring_table, **dlc_misc_table, **dlc_goods_2_table}

