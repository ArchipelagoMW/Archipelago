import sys

from BaseClasses import Location
from worlds.dark_souls_3.data.locations_data import location_tables, painted_world_table, dreg_heap_table, \
    ringed_city_table, key_location_list, dlc_key_location_list


class DarkSouls3Location(Location):
    game: str = "Dark Souls III"

    weapon_location = (
        "US: Irithyll Straight Sword",
        "UG: Chaos Blade",
        "SL: Dragonrider Bow",
        "SL: White Hair Talisman",
        "SL: Izalith Staff",
        "SL: Fume Ultra Greatsword",
        "SL: Black Knight Sword",
        "IBV: Yorshka's Spear",
        "IBV: Smough's Great Hammer",
        "IBV: Dragonslayer Greatbow",
        "IBV: Golden Ritual Spear",
        "PC: Eleonora",
        "GA: Witch's Locks",
        "GA: Crystal Chime",
        "UG: Black Knight Glaive",
        "AP: Dragonslayer Spear",
        "LC: Caitha's Chime",
        "LC: Sunlight Straight Sword",
        "FS: Uchigatana",
        "FS: Master's Attire",
        "FS: Master's Gloves",
        "US: Bloodbite Ring",
        "US: Mirrah Vest",
        "US: Mirrah Gloves",
        "US: Mirrah Trousers",
        "US: Loretta's Bone",
        "US: Hand Axe",
        "US: Great Scythe",
        "US: Hawk Ring",
        "US: Warrior of Sunlight Covenant",
        "RS: Great Swamp Ring",
        "CD: Rosaria's Fingers Covenant",
        "FK: Nameless Knight Helm",
        "FK: Nameless Knight Armor",
        "FK: Nameless Knight Gauntlets",
        "FK: Nameless Knight Leggings",
        "FK: Wolf's Blood Swordgrass",
        "FK: Watchdogs of Farron Covenant",
        "IBV: Roster of Knights",
        "IBV: Aldrich Faithful Covenant",
        "LC: Gotthard Twinswords",
        "LC: Irithyll Rapier",
        "AP: Dragon Tooth",
        "GA: Sage's Crystal Staff",
        "AP: Havel's Greatshield",
        "FS: Broken Straight Sword",
        "HWL: Deep Battle Axe",
        "HWL: Club",
        "HWL: Claymore",
        "HWL: Longbow",
        "HWL: Mail Breaker",
        "HWL: Broadsword",
        "HWL: Astora's Straight Sword",
        "HWL: Rapier",
        "HWL: Lucerne",
        "US: Whip",
        "US: Reinforced Club",
        "US: Caestus",
        "US: Partizan",
        "US: Red Hilted Halberd",
        "US: Saint's Talisman",
        "US: Large Club",
        "RS: Brigand Twindaggers",
        "RS: Butcher Knife",
        "RS: Brigand Axe",
        "RS: Heretic's Staff",
        "RS: Great Club",
        "RS: Exile Greatsword",
        "RS: Sellsword Twinblades",
        "CD: Notched Whip",
        "CD: Astora Greatsword",
        "CD: Executioner's Greatsword",
        "CD: Saint-tree Bellvine",
        "CD: Saint Bident",
        "CD: Drang Hammers",
        "CD: Arbalest",
        "FK: Sunlight Talisman",
        "FK: Greatsword",
        "FK: Black Bow of Pharis",
        "FK: Great Axe",
        "CC: Black Blade",
        "UG: Blacksmith Hammer",
        "IBV: Witchtree Branch",
        "IBV: Painting Guardian's Curved Sword",
        "ID: Pickaxe",
        "PC: Court Sorcerer's Staff",
        "GA: Avelyn",
        "GA: Onikiri and Ubadachi",
        "AP: Ricard's Rapier",
        "AP: Drakeblood Greatsword",
        "LC: Greatlance",
        "LC: Sniper Crossbow",
        "CKG: Claw",
        "IBV: Drang Twinspears")
    
    dlc_weapon_location = (
        "PW: Champions Bones",
        "PW: Titanite Slab",
        "DH: Loincloth",
        "RC: Church Guardian Shiv",
        "RC: Titanite Slab",
        "RC: Violet Wrappings",
        "PW: Onyx Blade",
        "PW: Earth Seeker",
        "PW: Quakestone Hammer",
        "PW: Millwood Greatbow",
        "PW: Valorheart",
        "DH: Aquamarine Dagger",
        "RC: Ringed Knight Straight Sword",
        "RC: Blood of the Dark Souls",
        "RC: Ringed Knight Spear",
        "RC: Crucifix of the Mad King",
        "RC: Sacred Chime of Filianore",
        "RC: Preacher's Right Arm",
        "RC: White Birch Bow",
        "RC: Ringed Knight Paired Greatswords",
        "PW: Follower Sabre",
        "PW: Millwood Battle Axe",
        "PW: Follower Javelin",
        "PW: Crow Talons",
        "PW: Pyromancer's Parting Flame",
        "PW: Crow Quills",
        "PW: Follower Torch",
        "DH: Murky Hand Scythe",
        "DH: Herald Curved Greatsword",
        "DH: Lothric War Banner",
        "RC: Ritual Spear Fragment",
        "DH: Murky Longstaff"
    )

    shield_location = (
        "FS: East-West Shield",
        "HWL: Silver Eagle Kite Shield",
        "US: Small Leather Shield",
        "US: Blue Wooden Shield",
        "US: Plank Shield",
        "US: Caduceus Round Shield",
        "US: Wargod Wooden Shield",
        "RS: Grass Crest Shield",
        "RS: Golden Falcon Shield",
        "RS: Twin Dragon Greatshield",
        "CD: Spider Shield",
        "CD: Crest Shield",
        "CD: Curse Ward Greatshield",
        "FK: Stone Parma",
        "FK: Dragon Crest Shield",
        "SL: Shield of Want",
        "SL: Black Iron Greatshield",
        "PC: Greatshield of Glory",
        "LC: Sacred Bloom Shield",
        "GA: Golden Wing Crest Shield",
        "AP: Ancient Dragon Greatshield",
        "LC: Spirit Tree Crest Shield",
        "US: Blessed Red and White Shield"
    )

    dlc_shield_location = (
        "PW: Follower Shield",
        "PW: Ethereal Oak Shield",
        "DH: Giant Door Shield",
        "RC: Dragonhead Shield",
        "RC: Dragonhead Greatshield"
    )

    armor_location = (
        "FSBT: Fire Keeper Robe",
        "FSBT: Fire Keeper Gloves",
        "FSBT: Fire Keeper Skirt",
        "FSBT: Fire Keeper Soul",
        "US: Cleric Hat",
        "US: Cleric Blue Robe",
        "US: Cleric Gloves",
        "US: Cleric Trousers",
        "US: Northern Helm",
        "US: Northern Armor",
        "US: Northern Gloves",
        "US: Northern Trousers",
        "US: Loincloth",
        "RS: Brigand Hood",
        "RS: Brigand Armor",
        "RS: Brigand Gauntlets",
        "RS: Brigand Trousers",
        "RS: Sorcerer Hood",
        "RS: Sorcerer Robe",
        "RS: Sorcerer Gloves",
        "RS: Sorcerer Trousers",
        "RS: Fallen Knight Helm",
        "RS: Fallen Knight Armor",
        "RS: Fallen Knight Gauntlets",
        "RS: Fallen Knight Trousers",
        "RS: Conjurator Hood",
        "RS: Conjurator Robe",
        "RS: Conjurator Manchettes",
        "RS: Conjurator Boots",
        "RS: Sellsword Helm",
        "RS: Sellsword Armor",
        "RS: Sellsword Gauntlet",
        "RS: Sellsword Trousers",
        "RS: Herald Helm",
        "RS: Herald Armor",
        "RS: Herald Gloves",
        "RS: Herald Trousers",
        "CD: Maiden Hood",
        "CD: Maiden Robe",
        "CD: Maiden Gloves",
        "CD: Maiden Skirt",
        "CD: Drang Armor",
        "CD: Drang Gauntlets",
        "CD: Drang Shoes",
        "CD: Archdeacon White Crown",
        "CD: Archdeacon Holy Garb",
        "CD: Archdeacon Skirt",
        "FK: Antiquated Dress",
        "FK: Antiquated Gloves",
        "FK: Antiquated Skirt",
        "FK: Ragged Mask",
        "FK: Crown of Dusk",
        "FK: Pharis's Hat",
        "CC: Old Sage's Blindfold",
        "IBV: Painting Guardian Hood",
        "IBV: Painting Guardian Gown",
        "IBV: Painting Guardian Gloves",
        "IBV: Painting Guardian Waistcloth",
        "IBV: Brass Helm",
        "IBV: Brass Armor",
        "IBV: Brass Gauntlets",
        "IBV: Brass Leggings",
        "ID: Old Sorcerer Hat",
        "ID: Old Sorcerer Coat",
        "ID: Old Sorcerer Gauntlets",
        "ID: Old Sorcerer Boots",
        "PC: Court Sorcerer Hood",
        "PC: Court Sorcerer Robe",
        "PC: Court Sorcerer Gloves",
        "PC: Court Sorcerer Trousers",
        "AP: Dragonslayer Helm",
        "AP: Dragonslayer Armor",
        "AP: Dragonslayer Gauntlets",
        "AP: Dragonslayer Leggings",
        "LC: Hood of Prayer",
        "LC: Robe of Prayer",
        "LC: Skirt of Prayer",
        "LC: Winged Knight Helm",
        "LC: Winged Knight Armor",
        "LC: Winged Knight Gauntlets",
        "LC: Winged Knight Leggings",
        "CKG: Shadow Mask",
        "CKG: Shadow Garb",
        "CKG: Shadow Gauntlets",
        "CKG: Shadow Leggings",
        "GA: Outrider Knight Helm",
        "GA: Outrider Knight Armor",
        "GA: Outrider Knight Gauntlets",
        "GA: Outrider Knight Leggings"
    )

    dlc_armor_location = (
        "PW: Slave Knight Hood",
        "PW: Slave Knight Armor",
        "PW: Slave Knight Gauntlets",
        "PW: Slave Knight Leggings",
        "PW: Vilhelm's Helm",
        "PW: Vilhelm's Armor",
        "PW: Vilhelm's Gauntlets",
        "PW: Vilhelm's Leggings",
        "RC: Shira's Crown",
        "RC: Shira's Armor",
        "RC: Shira's Gloves",
        "RC: Shira's Trousers",
        "RC: Iron Dragonslayer Helm",
        "RC: Iron Dragonslayer Armor",
        "RC: Iron Dragonslayer Gauntlets",
        "RC: Iron Dragonslayer Leggings",
        "RC: Ruin Sentinel Helm",
        "RC: Ruin Sentinel Armor",
        "RC: Ruin Sentinel Gauntlets",
        "RC: Ruin Sentinel Leggings",
        "DH: Desert Pyromancer Hood",
        "DH: Desert Pyromancer Garb",
        "DH: Desert Pyromancer Gloves",
        "DH: Desert Pyromancer Skirt",
        "RC: Black Witch Veil",
        "RC: Black Witch Hat",
        "RC: Black Witch Garb",
        "RC: Black Witch Wrappings",
        "RC: Black Witch Trousers",
        "RC: White Preacher Head",
        "RC: Antiquated Plain Garb"
    )

    ring_location = (
        "FSBT: Estus Ring",
        "FSBT: Covetous Silver Serpent Ring",
        "US: Fire Clutch Ring",
        "US: Flame Stoneplate Ring",
        "US: Flynn's Ring",
        "US: Chloranthy Ring",
        "RS: Morne's Ring",
        "RS: Sage Ring",
        "CD: Aldrich's Sapphire",
        "CD: Lloyd's Sword Ring",
        "CD: Poisonbite Ring",
        "CD: Deep Ring",
        "FK: Lingering Dragoncrest Ring",
        "CC: Carthus Milkring",
        "CC: Witch's Ring",
        "CC: Carthus Bloodring",
        "SL: Speckled Stoneplate Ring",
        "IBV: Magic Clutch Ring",
        "IBV: Ring of the Sun's First Born",
        "IBV: Pontiff's Right Eye",
        "IBV: Leo Ring",
        "IBV: Dark Stoneplate Ring",
        "IBV: Reversal Ring",
        "IBV: Ring of Favor",
        "ID: Bellowing Dragoncrest Ring",
        "ID: Covetous Gold Serpent Ring",
        "ID: Dusk Crown Ring",
        "ID: Dark Clutch Ring",
        "PC: Cursebite Ring",
        "AL: Sun Princess Ring",
        "AL: Aldrich's Ruby",
        "GA: Scholar Ring",
        "GA: Fleshbite Ring",
        "GA: Hunter's Ring",
        "UG: Ashen Estus Ring",
        "UG: Hornet Ring",
        "AP: Lightning Clutch Ring",
        "AP: Ring of Steel Protection",
        "AP: Calamity Ring",
        "AP: Thunder Stoneplate Ring",
        "LC: Knight's Ring",
        "LC: Red Tearstone Ring",
        "CKG: Dragonscale Ring",
        "SL: Knight Slayer's Ring",
        "CKG: Magic Stoneplate Ring",
        "HWL: Blue Tearstone Ring"
    )

    dlc_ring_location = (
        "RC: Havel's Ring",
        "PW: Chillbite Ring"
    )

    spell_location = (
        "CD: Seek Guidance",
        "FK: Lightning Spear",
        "FK: Atonement",
        "FK: Great Magic Weapon",
        "FK: Iron Flesh",
        "SL: Lightning Stake",
        "SL: Toxic Mist",
        "SL: Sacred Flame",
        "IBV: Dorhys' Gnawing",
        "IBV: Great Heal",
        "ID: Lightning Blade",
        "ID: Profaned Flame",
        "PC: Wrath of the Gods",
        "GA: Power Within",
        "GA: Soul Stream",
        "GA: Divine Pillars of Light",
        "AP: Great Magic Barrier",
        "ID: Great Magic Shield",
        "GA: Crystal Scroll"
    )

    dlc_spell_location = (
        "PW: Frozen Weapon",
        "PW: Snap Freeze",
        "DH: Great Soul Dregs",
        "DH: Flame Fan",
        "RC: Lightning Arrow",
        "PW: Way of White Corona",
        "DH: Projected Heal",
        "PW: Floating Chaos"
    )

    misc_location = (
        "RS: Braille Divine Tome of Carim",
        "RS: Great Swamp Pyromancy Tome",
        "RS: Farron Coal",
        "CD: Paladin's Ashes",
        "CD: Deep Braille Divine Tome",
        "FK: Golden Scroll",
        "FK: Sage's Coal",
        "FK: Sage's Scroll",
        "FK: Dreamchaser's Ashes",
        "CC: Carthus Pyromancy Tome",
        "CC: Grave Warden's Ashes",
        "CC: Grave Warden Pyromancy Tome",
        "SL: Quelana Pyromancy Tome",
        "SL: Izalith Pyromancy Tome",
        "HWL: Greirat's Ashes",
        "IBV: Excrement-covered Ashes",
        "IBV: Easterner's Ashes",
        "ID: Dragon Torso Stone",
        "ID: Profaned Coal",
        "ID: Xanthous Ashes",
        "PC: Logan's Scroll",
        "AL: Giant's Coal",
        "UG: Coiled Sword Fragment",
        "AP: Dragon Chaser's Ashes",
        "AP: Twinkling Dragon Torso Stone",
        "LC: Braille Divine Tome of Lothric",
        "US: Fire Gem",
        "HWL: Binoculars"
    )

    dlc_misc_location = ("PW: Captains Ashes")

    npc_location = (
        "US: Irina's Ashes",
        "US: Tower Key (Irina Drop)",
        "ID: Karla's Ashes",
        "ID: Karla's Pointed Hat",
        "ID: Karla's Coat",
        "ID: Karla's Gloves",
        "ID: Karla's Trousers",
        "US: Cornyx's Ashes",
        "US: Pyromancy Flame",
        "US: Cornyx's Wrap",
        "US: Cornyx's Garb",
        "US: Cornyx's Skirt",
        "RS: Orbeck's Ashes"
    )

    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 100000
        table_offset = 100

        output = {}
        for i, table in enumerate(location_tables):
            if len(table) > table_offset:
                raise Exception("A location table has {} entries, that is more than {} entries (table #{})".format(len(table), table_offset, i))
            output.update({name: id for id, name in enumerate(table, base_id + (table_offset * i))})

        return output
    
    @staticmethod
    def is_weapon_location(name) -> bool:
        return name in DarkSouls3Location.weapon_location
    
    @staticmethod
    def is_dlc_weapon_location(name) -> bool:
        return name in DarkSouls3Location.dlc_weapon_location
    
    @staticmethod
    def is_shield_location(name) -> bool:
        return name in DarkSouls3Location.shield_location
    
    @staticmethod
    def is_dlc_shield_location(name) -> bool:
        return name in DarkSouls3Location.dlc_shield_location
    
    @staticmethod
    def is_armor_location(name) -> bool:
        return name in DarkSouls3Location.armor_location
    
    @staticmethod
    def is_dlc_armor_location(name) -> bool:
        return name in DarkSouls3Location.dlc_armor_location
    
    @staticmethod
    def is_ring_location(name) -> bool:
        return name in DarkSouls3Location.ring_location
    
    @staticmethod
    def is_dlc_ring_location(name) -> bool:
        return name in DarkSouls3Location.dlc_ring_location
    
    @staticmethod
    def is_spell_location(name) -> bool:
        return name in DarkSouls3Location.spell_location
    
    @staticmethod
    def is_dlc_spell_location(name) -> bool:
        return name in DarkSouls3Location.dlc_spell_location
    
    @staticmethod
    def is_misc_location(name) -> bool:
        return name in DarkSouls3Location.misc_location
    
    @staticmethod
    def is_dlc_misc_location(name) -> bool:
        return name in DarkSouls3Location.dlc_misc_location
    
    @staticmethod
    def is_npc_location(name) -> bool:
        return name in DarkSouls3Location.npc_location
    
            