from BaseClasses import Location


# I'm assuming this its just to add uniqueness to ids with all worlds in a seed I have no idea how this number is
# calculate, so just threw some random numbers. 127{zone id}{game id}
base_location_id = 127000000


class ZoneData:
    def __init__(self, abrev: str, name: str, start: int, loot_flag: int = 0, loot_size: int = 0):
        self.abrev = abrev
        self.name = name
        self.start = start
        self.loot_flag = 0
        self.loot_size = 0
        if loot_flag != 0 and loot_size != 0:
            self.loot_flag = loot_flag
            self.loot_size = loot_size

    @staticmethod
    def get_zone_data(zone_start):
        for k, v in zones_dict.items():
            if v.start == zone_start:
                return k, v
        return 50, ZoneData("UNK", "UNKNOWN", 0x00)


zones_dict = {
    0: ZoneData("ST0", "Final Stage: Bloodlines", 0x189c),
    1: ZoneData("ARE", "Colosseum", 0x8704, 0x03bf06, 2),
    2: ZoneData("CAT", "Catacombs", 0xb6d4, 0x03befc, 3),
    3: ZoneData("CEN", "Center Cube", 0x0e7c, 0x03beec, 2),
    4: ZoneData("CHI", "Abandoned Mine", 0xdea4, 0x03bf02, 2),
    5: ZoneData("DAI", "Royal Chapel", 0x5fb8, 0x03beff, 3),
    6: ZoneData("DRE", "Nightmare", 0x6fc0),
    7: ZoneData("LIB", "Long Library", 0xf160, 0x03befa, 2),
    8: ZoneData("NO0", "Marble Gallery", 0x37b8, 0x03beec, 2),
    9: ZoneData("NO1", "Outer Wall", 0x1a20, 0x03beee, 2),
    10: ZoneData("NO2", "Olrox's Quarters", 0x8744, 0x03bef0, 2),
    11: ZoneData("NO3", "Castle Entrance", 0x187c, 0x03bef2, 2),
    12: ZoneData("NO3", "Castle Entrance", 0x90ec, 0x03bef2, 2),
    # 12: ZoneData("NP3", "Castle Entrance (after visiting Alchemy Laboratory)", 0x90ec, 0x03bef2, 2),
    13: ZoneData("NO4", "Underground Caverns", 0xa620, 0x03bef4, 5),
    14: ZoneData("NZ0", "Alchemy Laboratory", 0x9504, 0x03bf0b, 2),
    15: ZoneData("NZ1", "Clock Tower", 0xc710, 0x03bf0d, 2),
    16: ZoneData("TOP", "Castle Keep", 0xd660, 0x03bf08, 3),
    17: ZoneData("WRP", "Warp rooms", 0x8218),
    18: ZoneData("RARE", "Reverse Colosseum", 0x6b70, 0x03bf3b, 2),
    19: ZoneData("RCAT", "Floating Catacombs", 0x3f80, 0x03bf2b, 4),
    20: ZoneData("RCEN", "Reverse Center Cube", 0x049c),
    21: ZoneData("RCHI", "Cave", 0xac24, 0x03bf33, 2),
    22: ZoneData("RDAI", "Anti-Chapel", 0x465c, 0x03bf2f, 3),
    23: ZoneData("RLIB", "Forbidden Library", 0x2b90, 0x03bf27, 2),
    24: ZoneData("RNO0", "Black Marble Gallery", 0x7354, 0x03bf13, 2),
    25: ZoneData("RNO1", "Reverse Outer Wall", 0x9ccc, 0x03bf17, 2),
    26: ZoneData("RNO2", "Death Wing's Lair", 0x6d20, 0x03bf1b, 2),
    27: ZoneData("RNO3", "Reverse Entrance", 0x3ee0, 0x03bf1f, 2),
    28: ZoneData("RNO4", "Reverse Caverns", 0xa214, 0x03bf23, 4),
    29: ZoneData("RNZ0", "Necromancy Laboratory", 0xcc34, 0x03bf43, 2),
    30: ZoneData("RNZ1", "Reverse Clock Tower", 0xced0, 0x03bf47, 2),
    31: ZoneData("RTOP", "Reverse Castle Keep", 0x2524, 0x03bf3f, 4),
    32: ZoneData("RWRP", "Reverse Warp rooms", 0xa198),
    33: ZoneData("BO0", "Olrox", 0xc10c, 0x03bef0, 2),
    34: ZoneData("BO1", "Legion", 0x55d0, 0x03befc, 3),  # or Granfaloon
    35: ZoneData("BO2", "Werewolf & Minotaur", 0x76a0, 0x03bf06, 2),
    36: ZoneData("BO3", "Scylla", 0x6734, 0x03bef4, 5),
    37: ZoneData("BO4", "Doppleganger10", 0x69ec, 0x03beee, 2),
    38: ZoneData("BO5", "Hippogryph", 0x6be4, 0x03beff, 2),
    39: ZoneData("BO6", "Richter", 0x9b84),
    40: ZoneData("BO7", "Cerberus", 0x6678, 0x03bf02, 2),
    41: ZoneData("RBO0", "Trio", 0xa094, 0x03bf3b, 2),
    42: ZoneData("RBO1", "Beezlebub", 0x5174, 0x03bf43, 2),
    43: ZoneData("RBO2", "Death", 0x1ab0, 0x03bf33, 2),
    44: ZoneData("RBO3", "Medusa", 0x31c8, 0x03bf2f, 3),
    45: ZoneData("RBO4", "Creature", 0x8e3c, 0x03bf17, 2),
    46: ZoneData("RBO5", "Doppleganger40", 0x5920, 0x03bf23, 4),
    47: ZoneData("RBO6", "Shaft/Dracula", 0x54ec),
    48: ZoneData("RBO7", "Akmodan II", 0x5f04, 0x03bf1b, 2),
    49: ZoneData("RBO8", "Galamoth", 0x9dc8, 0x03bf2b, 4),
}


def get_zone_id(zone_name: str) -> int:
    for k, v in zones_dict.items():
        if v.name == zone_name:
            return k * 10000


class SotnLocation(Location):
    game = "Symphony of the Night"
    # parent_region = Optional[Region] add zones


class LocationData:
    def __init__(self, zone: str, game_id, rom_address: list = None, no_offset=False, can_be_relic=False, delete=0, relic_index=0, item_address=None):
        self.zone = zone
        self.game_id = game_id
        self.rom_address = [] if rom_address is None else rom_address
        self.can_be_relic = can_be_relic
        self.no_offset = no_offset
        self.delete = delete
        self.relic_index = relic_index
        self.item_address = [] if item_address is None else item_address
        if game_id is None:
            self.game_id: int = None
            self.location_id: int = None
        else:
            self.game_id: int = game_id
            self.location_id: int = base_location_id + get_zone_id(zone) + game_id

    def get_delete(self):
        return self.delete

    def get_zone(self):
        return self.zone

    def get_location_id(self):
        return self.location_id

    @staticmethod
    def get_location_name(id: int) -> str:
        for k, v in location_table.items():
            if v.location_id == id:
                return k


# Bosses, Relics and despawn item 3{zone}{n++}
no3_locations = {
    "NO3 - Heart Vessel (Above Death)": LocationData("Castle Entrance", 0, [0x4b68604, 0x53f5f80]),
    "NO3 - Life Vessel (Bellow shield potion)": LocationData("Castle Entrance", 1,
                                                             [0x4b68606, 0x53f5f82]),
    "NO3 - Life Apple (Hidden room)": LocationData("Castle Entrance", 2, [0x4b68608, 0x53f5f84]),
    "NO3 - Shield Potion": LocationData("Castle Entrance", 4, [0x4b6860c, 0x53f5f88]),
    "NO3 - Holy mail": LocationData("Castle Entrance", 5,[0x4b6860e, 0x53f5f8a]),
    "NO3 - Life Vessel (UC exit)": LocationData("Castle Entrance", 6,[0x4b68610, 0x53f5f8c]),
    "NO3 - Heart Vessel (Teleport exit)": LocationData("Castle Entrance", 7,
                                                       [0x4b68612, 0x53f5f8e]),
    "NO3 - Life Vessel (Above entry)": LocationData("Castle Entrance", 8,[0x4b68614, 0x53f5f90]),
    "NO3 - Jewel sword": LocationData("Castle Entrance", 9, [0x53f5f92]),
    "NO3 - Pot Roast": LocationData("Castle Entrance", 3110, [0x4ba9774, 0x5431554],
                                    True, False),
    "NO3 - Turkey": LocationData("Castle Entrance", 3111, [0x4baa2b0, 0x5431f60],
                                 True, False),
    "Cube of Zoe": LocationData("Castle Entrance", 3112,
                                [0x4b6b082+8, 0x4b6b93e+8, 0x53f8e26+8, 0x53f9692+8],
                                False, True, 0x000e00b0, 10, [0x4b68618, 0x53f5f94]),
    "Power of Wolf": LocationData("Castle Entrance", 3113,
                                  [0x4b6b14a+8, 0x4b6b9ac+8, 0x53f8f16+8, 0x53f9714+8],
                                  False,True, 0x000e00b1, 11, [0x4b6861a, 0x53f5f96])
}

nz0_locations = {
    "NZ0 - Hide cuirass": LocationData("Alchemy Laboratory", 0, [0x54b2298]),
    "NZ0 - Heart Vessel": LocationData("Alchemy Laboratory", 1, [0x54b229a]),
    "NZ0 - Cloth cape": LocationData("Alchemy Laboratory", 2, [0x54b229c]),
    "NZ0 - Life Vessel": LocationData("Alchemy Laboratory", 3, [0x54b229e]),
    "NZ0 - Sunglasses": LocationData("Alchemy Laboratory", 6, [0x54b22a4]),
    "NZ0 - Resist thunder": LocationData("Alchemy Laboratory", 7, [0x54b22a6]),
    "NZ0 - Leather shield": LocationData("Alchemy Laboratory", 8, [0x54b22a8]),
    "NZ0 - Basilard": LocationData("Alchemy Laboratory", 9, [0x54b22aa]),
    "NZ0 - Potion": LocationData("Alchemy Laboratory", 10, [0x54b22ac]),
    "NZ0 - Slogra and Gaibon kill": LocationData("Alchemy Laboratory", 3140),
    "Skill of Wolf": LocationData("Alchemy Laboratory", 3141, [0x054b1d5a],
                                  False, True),
    "Bat Card": LocationData("Alchemy Laboratory", 3142, [0x054b1d58],
                             False, True)
}

no0_locations = {
    "NO0 - Life Vessel(Left clock)": LocationData("Marble Gallery", 0, [0x48fad98]),
    "NO0 - Alucart shield": LocationData("Marble Gallery", 1, [0x48fad9a]),
    "NO0 - Heart Vessel(Right clock)": LocationData("Marble Gallery", 2,[0x48fad9c]),
    "NO0 - Life apple(Middle clock)": LocationData("Marble Gallery", 3, [0x48fad9e]),
    "NO0 - Hammer(Middle clock)": LocationData("Marble Gallery", 4, [0x48fada0]),
    "NO0 - Potion(Middle clock)": LocationData("Marble Gallery", 5, [0x48fada2]),
    "NO0 - Alucart mail": LocationData("Marble Gallery", 6, [0x48fada4]),
    "NO0 - Alucart sword": LocationData("Marble Gallery", 7, [0x48fada6]),
    "NO0 - Life Vessel(Inside)": LocationData("Marble Gallery", 8, [0x48fada8]),
    "NO0 - Heart Vessel(Inside)": LocationData("Marble Gallery", 9, [0x48fadaa]),
    "NO0 - Library card(Jewel)": LocationData("Marble Gallery", 10, [0x48fadac]),
    "NO0 - Attack potion(Jewel)": LocationData("Marble Gallery", 11, [0x48fadae]),
    "NO0 - Hammer(Spirit)": LocationData("Marble Gallery", 12, [0x48fadb0]),
    "NO0 - Str. potion": LocationData("Marble Gallery", 13, [0x48fadb2]),
    "NO0 - Holy glasses": LocationData("Marble Gallery", 3080, [0x456e368], True),
    "Spirit Orb": LocationData("Marble Gallery", 3081, [0x48fd1f6+8, 0x48fe278+8],
                               False, True, 0x001700b0, 14, [0x48fadb4]),
    "Gravity Boots": LocationData("Marble Gallery", 3082, [0x48fc9b2+8, 0x48fd944+8],
                                  False, True, 0x001700b1, 15, [0x48fadb6])
}

no1_locations = {
    "NO1 - Jewel knuckles": LocationData("Outer Wall", 0, [0x49d3674]),
    "NO1 - Mirror cuirass": LocationData("Outer Wall", 1, [0x49d3676]),
    "NO1 - Heart Vessel": LocationData("Outer Wall", 2, [0x49d3678]),
    "NO1 - Garnet": LocationData("Outer Wall", 3, [0x49d367a]),
    "NO1 - Gladius": LocationData("Outer Wall", 4, [0x49d367c]),
    "NO1 - Life Vessel": LocationData("Outer Wall", 5, [0x49d367e]),
    "NO1 - Zircon": LocationData("Outer Wall", 6, [0x49d3680]),
    "NO1 - Pot Roast": LocationData("Outer Wall", 3090, [0x4a197d8], True),
    "NO1 - Doppleganger 10 kill": LocationData("Outer Wall", 3091),
    "Soul of Wolf": LocationData("Outer Wall", 3092, [0x49d5d36+8, 0x49d658e+8],
                                 False, True, 0x002e00b0, 7, [0x49d3682])
}

lib_locations = {
    "LIB - Stone mask": LocationData("Long Library", 1, [0x47a390a]),
    "LIB - Holy rod": LocationData("Long Library", 2, [0x47a390c]),
    "LIB - Bronze cuirass": LocationData("Long Library", 4, [0x47a3910]),
    "LIB - Takemitsu": LocationData("Long Library", 5, [0x47a3912]),
    "LIB - Onyx": LocationData("Long Library", 6, [0x47a3914]),
    "LIB - Frankfurter": LocationData("Long Library", 7, [0x47a3916]),
    "LIB - Potion": LocationData("Long Library", 8, [0x47a3918]),
    "LIB - Antivenom": LocationData("Long Library", 9, [0x47a391a]),
    "LIB - Topaz circlet": LocationData("Long Library", 10, [0x47a391c]),
    "LIB - Lesser Demon kill": LocationData("Long Library", 3070),
    "Soul of Bat": LocationData("Long Library", 3072, [0x47a5b5e+8, 0x47a623e+8],
                                False, True, 0x002600b2, 11, [0x47a391e]),
    "Faerie Scroll": LocationData("Long Library", 3073, [0x47a5718+8, 0x47a5dca+8],
                                  False, True, 0x00f400b1, 12, [0x47a3920]),
    "Jewel of Open": LocationData("Long Library", 3074, [0x047a321c], False,
                                  True),
    "Faerie Card": LocationData("Long Library", 3075, [0x47a577c+8, 0x47a5f64+8],
                                False,True, 0x002600b0, 13, [0x47a3922]),
}

# IMPORTANT: Writing on item index 12 make Karasuman door not interactable, trying Fire of Bat on index 2
nz1_locations = {
    "NZ1 - Magic missile": LocationData("Clock Tower", 0, [0x5573834]),
    "NZ1 - Pentagram": LocationData("Clock Tower", 1, [0x5573836]),
    "NZ1 - Star flail": LocationData("Clock Tower", 3, [0x557383a]),
    "NZ1 - Gold plate": LocationData("Clock Tower", 4, [0x557383c]),
    "NZ1 - Steel helm": LocationData("Clock Tower", 5, [0x557383e]),
    "NZ1 - Healing mail": LocationData("Clock Tower", 6, [0x5573840]),
    "NZ1 - Bekatowa": LocationData("Clock Tower", 7, [0x5573842]),
    "NZ1 - Shaman shield": LocationData("Clock Tower", 8, [0x5573844]),
    "NZ1 - Ice mail": LocationData("Clock Tower", 9, [0x5573846]),
    "NZ1 - Life Vessel(Gear train)": LocationData("Clock Tower", 10, [0x5573848]),
    "NZ1 - Heart Vessel(Gear train)": LocationData("Clock Tower", 11, [0x557384a]),
    "NZ1 - Bwaka knife": LocationData("Clock Tower", 3150, [0x55737a4], True),
    "NZ1 - Pot roast": LocationData("Clock Tower", 3151, [0x557379c], True),
    "NZ1 - Shuriken": LocationData("Clock Tower", 3152, [0x55737a0], True),
    "NZ1 - TNT": LocationData("Clock Tower", 3153, [0x55737a8], True),
    "NZ1 - Karasuman kill": LocationData("Clock Tower", 3154),
    "Fire of Bat": LocationData("Clock Tower", 3155, [0x5575356+8, 0x5575e92+8], False,
                                True, 0x002300b0, 2, [0x5573838])
}

top_locations = {
    "TOP - Turquoise": LocationData("Castle Keep", 0, [0x560f5f8]),
    "TOP - Turkey(Behind wall)": LocationData("Castle Keep", 1, [0x560f5fa]),
    "TOP - Fire mail(Behind wall)": LocationData("Castle Keep", 2, [0x560f5fc]),
    "TOP - Tyrfing": LocationData("Castle Keep", 3, [0x560f5fe]),
    "TOP - Sirloin(Above Richter)": LocationData("Castle Keep", 4, [0x560f600]),
    "TOP - Turkey(Above Richter)": LocationData("Castle Keep", 5, [0x560f602]),
    "TOP - Pot roast(Above Richter)": LocationData("Castle Keep", 6, [0x560f604]),
    "TOP - Frankfurter(Above Richter)": LocationData("Castle Keep", 7, [0x560f606]),
    "TOP - Resist stone(Above Richter)": LocationData("Castle Keep", 8, [0x560f608]),
    "TOP - Resist dark(Above Richter)": LocationData("Castle Keep", 9, [0x560f60a]),
    "TOP - Resist holy(Above Richter)": LocationData("Castle Keep", 10, [0x560f60c]),
    "TOP - Platinum mail(Above Richter)": LocationData("Castle Keep", 11, [0x560f60e]),
    "TOP - Falchion": LocationData("Castle Keep", 12, [0x560f610]),
    "TOP - Life Vessel 1(Viewing room)": LocationData("Castle Keep", 13, [0x560f612]),
    "TOP - Life Vessel 2(Viewing room)": LocationData("Castle Keep", 14, [0x560f614]),
    "TOP - Heart Vessel 1(Viewing room)": LocationData("Castle Keep", 15, [0x560f616]),
    "TOP - Heart Vessel 2(Viewing room)": LocationData("Castle Keep", 16, [0x560f618]),
    "TOP - Heart Vessel(Before Richter)": LocationData("Castle Keep", 18, [0x560f61c]),
    "Leap Stone": LocationData("Castle Keep", 3160, [0x5610dba+8, 0x5611612+8], False,
                               True, 0x002400b0, 19, [0x560f61e]),
    "Power of Mist": LocationData("Castle Keep", 3161, [0x5610db0+8, 0x5611424+8], False,
                                  True, 0x002400b1, 20, [0x560f620]),
    "Ghost Card": LocationData("Castle Keep", 3162, [0x5611274+8, 0x5611950+8], False,
                               True, 0x002400b2, 21, [0x560f622]),
}

dai_locations = {
    "DAI - Ankh of life(Stairs)": LocationData("Royal Chapel", 0, [0x4676ef8]),
    "DAI - Morningstar": LocationData("Royal Chapel", 1, [0x4676efa]),
    "DAI - Silver ring": LocationData("Royal Chapel", 2, [0x4676efc]),
    "DAI - Aquamarine(Stairs)": LocationData("Royal Chapel", 3, [0x4676efe]),
    "DAI - Mystic pendant": LocationData("Royal Chapel", 4, [0x4676f00]),
    "DAI - Magic missile(Stairs)": LocationData("Royal Chapel", 5, [0x4676f02]),
    "DAI - Shuriken(Stairs)": LocationData("Royal Chapel", 6, [0x4676f04]),
    "DAI - TNT(Stairs)": LocationData("Royal Chapel", 7, [0x4676f06]),
    "DAI - Boomerang(Stairs)": LocationData("Royal Chapel", 8, [0x4676f08]),
    "DAI - Goggles": LocationData("Royal Chapel", 9, [0x4676f0a]),
    "DAI - Silver plate": LocationData("Royal Chapel", 10, [0x4676f0c]),
    "DAI - Str. potion(Bell)": LocationData("Royal Chapel", 11, [0x4676f0e]),
    "DAI - Life Vessel(Bell)": LocationData("Royal Chapel", 12, [0x4676f10]),
    "DAI - Zircon": LocationData("Royal Chapel", 13, [0x4676f12]),
    "DAI - Cutlass": LocationData("Royal Chapel", 14, [0x4676f14]),
    "DAI - Potion": LocationData("Royal Chapel", 15, [0x4676f16]),
    "DAI - Hippogryph kill": LocationData("Royal Chapel", 3050),
}

are_locations = {
    "ARE - Heart Vessel": LocationData("Colosseum", 0, [0x43c3130]),
    "ARE - Shield rod": LocationData("Colosseum", 1, [0x43c3132]),
    "ARE - Blood cloak": LocationData("Colosseum", 3, [0x43c3136]),
    "ARE - Knight shield(Chapel passage)": LocationData("Colosseum", 4, [0x43c3138]),
    "ARE - Library card": LocationData("Colosseum", 5, [0x43c313a]),
    "ARE - Green tea": LocationData("Colosseum", 6, [0x43c313c]),
    "ARE - Holy sword(Hidden attic)": LocationData("Colosseum", 7, [0x43c313e]),
    "ARE - Minotaurus/Werewolf kill": LocationData("Colosseum", 3010),
    "Form of Mist": LocationData("Colosseum", 3011, [0x43c5782+8, 0x43c5e00+8], False,
                                 True, 0x003300b0, 8, [0x43c3140])
}

no2_locations = {
    "NO2 - Heart Vessel": LocationData("Olrox's Quarters", 1, [0x4aa1556]),
    "NO2 - Broadsword": LocationData("Olrox's Quarters", 4, [0x4aa155c]),
    "NO2 - Onyx": LocationData("Olrox's Quarters", 5, [0x4aa155e]),
    "NO2 - Cheese": LocationData("Olrox's Quarters", 6, [0x4aa1560]),
    "NO2 - Manna prism": LocationData("Olrox's Quarters", 7, [0x4aa1562]),
    "NO2 - Resist fire": LocationData("Olrox's Quarters", 8, [0x4aa1564]),
    "NO2 - Luck potion": LocationData("Olrox's Quarters", 9, [0x4aa1566]),
    "NO2 - Estoc": LocationData("Olrox's Quarters", 10, [0x4aa1698]),
    "NO2 - Iron ball": LocationData("Olrox's Quarters", 11, [0x4aa169a]),
    "NO2 - Garnet": LocationData("Olrox's Quarters", 12, [0x4aa169c]),
    "NO2 - Olrox kill": LocationData("Olrox's Quarters", 3100),
    "Echo of Bat": LocationData("Olrox's Quarters", 3101, [0x4aa414e+8, 0x4aa49a6+8],
                                False, True, 0x001a00b0, 13, [0x4aa169e]),
    "Sword Card": LocationData("Olrox's Quarters", 3102, [0x4aa3f6e+8, 0x4aa47c6+8],
                               False, True, 0x001a00b1, 14, [0x4aa16a0]),
}

no4_locations = {
    "NO4 - Heart Vessel(0)": LocationData("Underground Caverns", 0,[0x4c324a0]),
    "NO4 - Life Vessel(1)": LocationData("Underground Caverns", 1, [0x4c324a2]),
    "NO4 - Crystal cloak": LocationData("Underground Caverns", 2,[0x4c324a4, 0x61a73a8]),
    "NO4 - Antivenom(Underwater)": LocationData("Underground Caverns", 4, [0x4c324a8]),
    "NO4 - Life Vessel(Underwater)": LocationData("Underground Caverns", 5, [0x4c324aa]),
    "NO4 - Life Vessel(Behind waterfall)": LocationData("Underground Caverns", 6,[0x4c324ac]),
    "NO4 - Herald Shield": LocationData("Underground Caverns", 7, [0x4c324ae]),
    "NO4 - Zircon": LocationData("Underground Caverns", 9, [0x4c324b2]),
    "NO4 - Gold Ring": LocationData("Underground Caverns", 10, [0x4c324b4]),
    "NO4 - Bandanna": LocationData("Underground Caverns", 11, [0x4c324b6]),
    "NO4 - Shiitake(12)": LocationData("Underground Caverns", 12, [0x4c324b8]),
    "NO4 - Claymore": LocationData("Underground Caverns", 13, [0x4c324ba]),
    "NO4 - Meal ticket 1(Succubus)": LocationData("Underground Caverns", 14, [0x4c324bc]),
    "NO4 - Meal ticket 2(Succubus)": LocationData("Underground Caverns", 15, [0x4c324be]),
    "NO4 - Meal ticket 3(Succubus)": LocationData("Underground Caverns", 16, [0x4c324c0]),
    "NO4 - Meal ticket 4(Succubus)": LocationData("Underground Caverns", 17, [0x4c324c2]),
    "NO4 - Moonstone": LocationData("Underground Caverns", 18, [0x4c324c4]),
    "NO4 - Scimitar": LocationData("Underground Caverns", 19, [0x4c324c6, 0x61a73ca]),
    "NO4 - Resist ice": LocationData("Underground Caverns", 20, [0x4c324c8, 0x61a73cc]),
    "NO4 - Pot roast": LocationData("Underground Caverns", 21, [0x4c324ca, 0x61a73ce]),
    "NO4 - Onyx(Holy)": LocationData("Underground Caverns", 22, [0x4c324cc]),
    "NO4 - Knuckle duster(Holy)": LocationData("Underground Caverns", 23, [0x4c324ce]),
    "NO4 - Life Vessel(Holy)": LocationData("Underground Caverns", 24, [0x4c324d0]),
    "NO4 - Elixir(Holy)": LocationData("Underground Caverns", 25, [0x4c324d2]),
    "NO4 - Toadstool(26)": LocationData("Underground Caverns", 26, [0x4c324d4]),
    "NO4 - Shiitake(27)": LocationData("Underground Caverns", 27, [0x4c324d6]),
    "NO4 - Life Vessel(Bellow bridge)": LocationData("Underground Caverns", 28, [0x4c324d8]),
    "NO4 - Heart Vessel(Bellow bridge)": LocationData("Underground Caverns", 29, [0x4c324da]),
    "NO4 - Pentagram": LocationData("Underground Caverns", 30, [0x4c324dc]),
    "NO4 - Secret boots": LocationData("Underground Caverns", 31, [0x4c324de]),
    "NO4 - Shiitake(Waterfall)": LocationData("Underground Caverns", 32, [0x4c324e0]),
    "NO4 - Toadstool(Waterfall)": LocationData("Underground Caverns", 33, [0x4c324e2]),
    "NO4 - Shiitake(Near entrance passage)": LocationData("Underground Caverns", 35, [0x4c324e6]),
    "NO4 - Nunchaku": LocationData("Underground Caverns", 36, [0x4c324e8]),
    "NO4 - Scylla kill": LocationData("Underground Caverns", 3130),
    "NO4 - Succubus kill": LocationData("Underground Caverns", 3131),
    "Holy Symbol": LocationData("Underground Caverns", 3132, [0x4c34ede+8, 0x4c361d0+8],
                                False, True, 0x003f00b0, 37, [0x4c324ea]),
    "Merman Statue": LocationData("Underground Caverns", 3133, [0x4c3516c+8, 0x4c36472+8],
                                  False, True, 0x003f00b1, 38, [0x4c324ec])
}

chi_locations = {
    "CHI - Power of sire(Demon)": LocationData("Abandoned Mine", 0, [0x45e95fc]),
    "CHI - Karma coin": LocationData("Abandoned Mine", 1, [0x45e95fe]),
    "CHI - Ring of ares": LocationData("Abandoned Mine", 4, [0x45e9604]),
    "CHI - Combat knife": LocationData("Abandoned Mine", 5, [0x45e9606]),
    "CHI - Shiitake 1": LocationData("Abandoned Mine", 6, [0x45e9608]),
    "CHI - Shiitake 2": LocationData("Abandoned Mine", 7, [0x45e960a]),
    "CHI - Barley tea(Demon)": LocationData("Abandoned Mine", 8, [0x45e960c]),
    "CHI - Peanuts 1(Demon)": LocationData("Abandoned Mine", 9, [0x45e960e]),
    "CHI - Peanuts 2(Demon)": LocationData("Abandoned Mine", 10, [0x45e9610]),
    "CHI - Peanuts 3(Demon)": LocationData("Abandoned Mine", 11, [0x45e9612]),
    "CHI - Peanuts 4(Demon)": LocationData("Abandoned Mine", 12, [0x45e9614]),
    "CHI - Turkey(Demon)": LocationData("Abandoned Mine", 3040, [0x45e9602]),
    "CHI - Cerberos kill": LocationData("Abandoned Mine", 3041),
    "Demon Card": LocationData("Abandoned Mine", 3042, [0x45ea956+8, 0x45eacda+8], False,
                               True, 0x001600b0, 13, [0x45e9616]),
}

cat_locations = {
    "CAT - Cat-eye circl.": LocationData("Catacombs", 0, [0x44912e4]),
    "CAT - Icebrand": LocationData("Catacombs", 1, [0x44912e6]),
    "CAT - Walk armor": LocationData("Catacombs", 2, [0x44912e8]),
    "CAT - Mormegil": LocationData("Catacombs", 3, [0x44912ea]),
    "CAT - Library card(Spike breaker)": LocationData("Catacombs", 4, [0x44912ec]),
    "CAT - Heart Vessel(Ballroom mask)": LocationData("Catacombs", 6, [0x44912f0]),
    "CAT - Ballroom mask": LocationData("Catacombs", 7, [0x44912f2]),
    "CAT - Bloodstone": LocationData("Catacombs", 8, [0x44912f4]),
    "CAT - Life Vessel(Crypt)": LocationData("Catacombs", 9, [0x44912f6]),
    "CAT - Heart Vessel(Crypt)": LocationData("Catacombs", 10, [0x44912f8]),
    "CAT - Cross shuriken 1(Spike breaker)": LocationData("Catacombs", 11, [0x44912fa]),
    "CAT - Cross shuriken 2(Spike breaker)": LocationData("Catacombs", 12, [0x44912fc]),
    "CAT - Karma coin 1(Spike breaker)": LocationData("Catacombs", 13, [0x44912fe]),
    "CAT - Karma coin 2(Spike breaker)": LocationData("Catacombs", 14, [0x4491300]),
    "CAT - Pork bun": LocationData("Catacombs", 15, [0x4491302]),
    "CAT - Spike breaker": LocationData("Catacombs", 16, [0x4491304]),
    "CAT - Monster vial 3 1(Sarcophagus)": LocationData("Catacombs", 17, [0x4491306]),
    "CAT - Monster vial 3 2(Sarcophagus)": LocationData("Catacombs", 18, [0x4491308]),
    "CAT - Monster vial 3 3(Sarcophagus)": LocationData("Catacombs", 19, [0x449130a]),
    "CAT - Monster vial 3 4(Sarcophagus)": LocationData("Catacombs", 20, [0x449130c]),
    "CAT - Legion kill": LocationData("Catacombs", 3020),
}

rare_locations = {
    "RARE - Fury plate(Hidden floor)": LocationData("Reverse Colosseum", 0, [0x5751554]),
    "RARE - Zircon": LocationData("Reverse Colosseum", 1, [0x5751556]),
    "RARE - Buffalo star": LocationData("Reverse Colosseum", 2, [0x5751558]),
    "RARE - Gram": LocationData("Reverse Colosseum", 3, [0x575155a]),
    "RARE - Aquamarine": LocationData("Reverse Colosseum", 4, [0x575155c]),
    "RARE - Heart Vessel(5)": LocationData("Reverse Colosseum", 5, [0x575155e]),
    "RARE - Life Vessel": LocationData("Reverse Colosseum", 6, [0x5751560]),
    "RARE - Heart Vessel(7)": LocationData("Reverse Colosseum", 7, [0x5751562]),
    "RARE - Fake Trevor/Grant/Sypha kill": LocationData("Reverse Colosseum", 3180),
}

rcat_locations = {
    "RCAT - Magic missile": LocationData("Floating Catacombs", 0, [0x4cfb6e0]),
    "RCAT - Buffalo star": LocationData("Floating Catacombs", 1, [0x4cfb6e2]),
    "RCAT - Resist thunder": LocationData("Floating Catacombs", 2, [0x4cfb6e4]),
    "RCAT - Resist fire": LocationData("Floating Catacombs", 3, [0x4cfb6e6]),
    "RCAT - Karma coin(4)(Spike breaker)": LocationData("Floating Catacombs", 4, [0x4cfb6e8]),
    "RCAT - Karma coin(5)(Spike breaker)": LocationData("Floating Catacombs", 5, [0x4cfb6ea]),
    "RCAT - Red bean bun": LocationData("Floating Catacombs", 6, [0x4cfb6ec]),
    "RCAT - Elixir": LocationData("Floating Catacombs", 7, [0x4cfb6ee]),
    "RCAT - Library card": LocationData("Floating Catacombs", 8, [0x4cfb6f0]),
    "RCAT - Life Vessel(9)": LocationData("Floating Catacombs", 9, [0x4cfb6f2]),
    "RCAT - Heart Vessel(10)": LocationData("Floating Catacombs", 10, [0x4cfb6f4]),
    "RCAT - Shield potion": LocationData("Floating Catacombs", 11, [0x4cfb6f6]),
    "RCAT - Attack potion": LocationData("Floating Catacombs", 12, [0x4cfb6f8]),
    "RCAT - Necklace of j": LocationData("Floating Catacombs", 13, [0x4cfb6fa]),
    "RCAT - Diamond": LocationData("Floating Catacombs", 14, [0x4cfb6fc]),
    "RCAT - Heart Vessel(After Galamoth)": LocationData("Floating Catacombs", 15, [0x4cfb6fe]),
    "RCAT - Life Vessel(After Galamoth)": LocationData("Floating Catacombs", 16,  [0x4cfb700]),
    "RCAT - Ruby circlet": LocationData("Floating Catacombs", 17, [0x4cfb702]),
    "RCAT - Galamoth kill": LocationData("Floating Catacombs", 3190),
    "Gas Cloud": LocationData("Floating Catacombs", 3191, [0x4cfcb0e+8, 0x4cfd892+8],
                              False, True, 0x00ff00b0, 18, [0x4cfb704])
}

rcen_locations = {
    "RCEN - Kill Dracula": LocationData("Reverse Center Cube", None)
}

rchi_locations = {
    "RCHI - Power of Sire(Demon)": LocationData("Cave", 0, [0x4da5134]),
    "RCHI - Life apple(Demon)": LocationData("Cave", 1, [0x4da5136]),
    "RCHI - Alucard sword": LocationData("Cave", 2, [0x4da5138]),
    "RCHI - Green tea(Demon)": LocationData("Cave", 3, [0x4da513a]),
    "RCHI - Power of Sire": LocationData("Cave", 4, [0x4da513c]),
    "RCHI - Shiitake 1(6)": LocationData("Cave", 6, [0x4da5140]),
    "RCHI - Shiitake 2(7)": LocationData("Cave", 7, [0x4da5142]),
    "RCHI - Death kill": LocationData("Cave", 3210),
    "Eye of Vlad": LocationData("Cave", 3211, [0x4da65ea+8, 0x4da6a4a+8, 0x662263a],
                                False, True, 0x0016)
}

rdai_locations = {
    "RDAI - Fire boomerang": LocationData("Anti-Chapel", 2, [0x4e322b8]),
    "RDAI - Diamond": LocationData("Anti-Chapel", 3, [0x4e322ba]),
    "RDAI - Zircon": LocationData("Anti-Chapel", 4, [0x4e322bc]),
    "RDAI - Heart Vessel(5)": LocationData("Anti-Chapel", 5, [0x4e322be]),
    "RDAI - Shuriken": LocationData("Anti-Chapel", 6, [0x4e322c0]),
    "RDAI - TNT": LocationData("Anti-Chapel", 7, [0x4e322c2]),
    "RDAI - Boomerang": LocationData("Anti-Chapel", 8, [0x4e322c4]),
    "RDAI - Javelin": LocationData("Anti-Chapel", 9, [0x4e322c6]),
    "RDAI - Manna prism": LocationData("Anti-Chapel", 10, [0x4e322c8]),
    "RDAI - Smart potion": LocationData("Anti-Chapel", 11, [0x4e322ca]),
    "RDAI - Life Vessel": LocationData("Anti-Chapel", 12, [0x4e322cc]),
    "RDAI - Talwar": LocationData("Anti-Chapel", 13, [0x4e322ce]),
    "RDAI - Bwaka knife": LocationData("Anti-Chapel", 14, [0x4e322d0]),
    "RDAI - Magic missile": LocationData("Anti-Chapel", 15, [0x4e322d2]),
    "RDAI - Twilight cloak": LocationData("Anti-Chapel", 16, [0x4e322d4]),
    "RDAI - Heart Vessel(17)": LocationData("Anti-Chapel", 17, [0x4e322d6]),
    "RDAI - Medusa kill": LocationData("Anti-Chapel", 3220),
    "Heart of Vlad": LocationData("Anti-Chapel", 3221, [0x4e335ac+8, 0x4e34048+8, 0x67437d2],
                                  False, True, 0x0016),
}

rlib_locations = {
    "RLIB - Turquoise": LocationData("Forbidden Library", 0, [0x4ee2f10]),
    "RLIB - Opal": LocationData("Forbidden Library", 1, [0x4ee2f12]),
    "RLIB - Library card": LocationData("Forbidden Library", 2, [0x4ee2f14]),
    "RLIB - Resist fire": LocationData("Forbidden Library", 3, [0x4ee2f16]),
    "RLIB - Resist ice": LocationData("Forbidden Library", 4, [0x4ee2f18]),
    "RLIB - Resist stone": LocationData("Forbidden Library", 5, [0x4ee2f1a]),
    "RLIB - Neutron bomb": LocationData("Forbidden Library", 6, [0x4ee2f1c]),
    "RLIB - Badelaire": LocationData("Forbidden Library", 7, [0x4ee2f1e]),
    "RLIB - Staurolite": LocationData("Forbidden Library", 8, [0x4ee2f20]),
}

rno0_locations = {
    "RNO0 - Library card": LocationData("Black Marble Gallery", 0, [0x4f85ae4]),
    "RNO0 - Potion": LocationData("Black Marble Gallery", 1, [0x4f85ae6]),
    "RNO0 - Antivenom": LocationData("Black Marble Gallery", 2, [0x4f85ae8]),
    "RNO0 - Life Vessel(Middle clock)": LocationData("Black Marble Gallery", 3, [0x4f85aea]),
    "RNO0 - Heart Vessel(Middle clock)": LocationData("Black Marble Gallery", 4, [0x4f85aec]),
    "RNO0 - Resist dark(Left clock)": LocationData("Black Marble Gallery", 5, [0x4f85aee]),
    "RNO0 - Resist holy(Left clock)": LocationData("Black Marble Gallery", 6, [0x4f85af0]),
    "RNO0 - Resist thunder(Left clock)": LocationData("Black Marble Gallery", 7, [0x4f85af2]),
    "RNO0 - Resist fire(Left clock)": LocationData("Black Marble Gallery", 8, [0x4f85af4]),
    "RNO0 - Meal ticket": LocationData("Black Marble Gallery", 9, [0x4f85af6]),
    "RNO0 - Iron ball": LocationData("Black Marble Gallery", 10, [0x4f85af8]),
    "RNO0 - Heart Refresh(Inside clock)": LocationData("Black Marble Gallery", 11, [0x4f85afa]),
}

rno1_locations = {
    "RNO1 - Heart Vessel": LocationData("Reverse Outer Wall", 0, [0x505016c]),
    "RNO1 - Shotel": LocationData("Reverse Outer Wall", 1, [0x505016e]),
    "RNO1 - Hammer": LocationData("Reverse Outer Wall", 2, [0x5050170]),
    "RNO1 - Life Vessel": LocationData("Reverse Outer Wall", 3, [0x5050172]),
    "RNO1 - Luck potion": LocationData("Reverse Outer Wall", 4, [0x5050174]),
    "RNO1 - Shield potion": LocationData("Reverse Outer Wall", 5, [0x5050176]),
    "RNO1 - High potion": LocationData("Reverse Outer Wall", 6, [0x5050178]),
    "RNO1 - Garnet": LocationData("Reverse Outer Wall", 7, [0x505017a]),
    "RNO1 - Dim Sum set": LocationData("Reverse Outer Wall", 3250, [0x507d08c], True),
    "RNO1 - Creature kill": LocationData("Reverse Outer Wall", 3251),
    "Tooth of Vlad": LocationData("Reverse Outer Wall", 3252,
                                  [0x5051d4a+8, 0x5052566+8, 0x67d1630], False, True,
                                  0x0016),
}

rno2_locations = {
    "RNO2 - Opal": LocationData("Death Wing's Lair", 0, [0x50f87b8]),
    "RNO2 - Sword of hador": LocationData("Death Wing's Lair", 1, [0x50f87ba]),
    "RNO2 - High potion": LocationData("Death Wing's Lair", 2, [0x50f87bc]),
    "RNO2 - Shield potion": LocationData("Death Wing's Lair", 3, [0x50f87be]),
    "RNO2 - Luck potion": LocationData("Death Wing's Lair", 4, [0x50f87c0]),
    "RNO2 - Manna prism": LocationData("Death Wing's Lair", 5, [0x50f87c2]),
    "RNO2 - Aquamarine": LocationData("Death Wing's Lair", 6, [0x50f87c4]),
    "RNO2 - Alucard mail": LocationData("Death Wing's Lair", 7, [0x50f87c6]),
    "RNO2 - Life Vessel": LocationData("Death Wing's Lair", 8, [0x50f87c8]),
    "RNO2 - Heart Refresh": LocationData("Death Wing's Lair", 9, [0x50f87ca]),
    "RNO2 - Shuriken": LocationData("Death Wing's Lair", 10, [0x50f87cc]),
    "RNO2 - Heart Vessel": LocationData("Death Wing's Lair", 11, [0x50f87ce]),
    "RNO2 - Akmodan II kill": LocationData("Death Wing's Lair", 3260),
    "Rib of Vlad": LocationData("Death Wing's Lair", 3261,
                                [0x50fa90c+8, 0x50fb220+8, 0x69d2b1e], False, True,
                                0x0016),
}

rno3_locations = {
    "RNO3 - Hammer": LocationData("Reverse Entrance", 0, [0x51ad798]),
    "RNO3 - Antivenom": LocationData("Reverse Entrance", 1, [0x51ad79a]),
    "RNO3 - High potion": LocationData("Reverse Entrance", 2, [0x51ad79c]),
    "RNO3 - Heart Vessel": LocationData("Reverse Entrance", 3, [0x51ad79e]),
    "RNO3 - Zircon": LocationData("Reverse Entrance", 4, [0x51ad7a0]),
    "RNO3 - Opal": LocationData("Reverse Entrance", 5, [0x51ad7a2]),
    "RNO3 - Beryl circlet": LocationData("Reverse Entrance", 6, [0x51ad7a4]),
    "RNO3 - Fire boomerang": LocationData("Reverse Entrance", 7, [0x51ad7a6]),
    "RNO3 - Life Vessel": LocationData("Reverse Entrance", 8, [0x51ad7a8]),
    "RNO3 - Talisman": LocationData("Reverse Entrance", 9, [0x51ad7aa]),
    "RNO3 - Pot roast": LocationData("Reverse Entrance", 3270, [0x51e6e4c], True),
}

rno4_locations = {
    "RNO4 - Alucard shield": LocationData("Reverse Caverns", 0, [0x526c0e8]),
    "RNO4 - Shiitake 1(Near entrance passage)": LocationData("Reverse Caverns", 1, [0x526c0ea]),
    "RNO4 - Toadstool(Waterfall)": LocationData("Reverse Caverns", 2, [0x526c0ec]),
    "RNO4 - Shiitake 2(Waterfall)": LocationData("Reverse Caverns", 3, [0x526c0ee]),
    "RNO4 - Garnet": LocationData("Reverse Caverns", 4, [0x526c0f0]),
    "RNO4 - Bat Pentagram": LocationData("Reverse Caverns", 5, [0x526c0f2]),
    "RNO4 - Life Vessel(Underwater)": LocationData("Reverse Caverns", 6, [0x526c0f4]),
    "RNO4 - Heart Vessel(Air pocket)": LocationData("Reverse Caverns", 7, [0x526c0f6]),
    "RNO4 - Potion(Underwater)": LocationData("Reverse Caverns", 8, [0x526c0f8]),
    "RNO4 - Shiitake 3(Near air pocket)": LocationData("Reverse Caverns", 9, [0x526c0fa]),
    "RNO4 - Shiitake 4(Near air pocket)": LocationData("Reverse Caverns", 10, [0x526c0fc]),
    "RNO4 - Opal": LocationData("Reverse Caverns", 11, [0x526c0fe]),
    "RNO4 - Life Vessel": LocationData("Reverse Caverns", 12, [0x526c100]),
    "RNO4 - Diamond": LocationData("Reverse Caverns", 13, [0x526c102]),
    "RNO4 - Zircon(Vase)": LocationData("Reverse Caverns", 14, [0x526c104]),
    "RNO4 - Heart Vessel(Succubus side)": LocationData("Reverse Caverns", 15, [0x526c106]),
    "RNO4 - Meal ticket 1(Succubus side)": LocationData("Reverse Caverns", 16, [0x526c108]),
    "RNO4 - Meal ticket 2(Succubus side)": LocationData("Reverse Caverns", 17, [0x526c10a]),
    "RNO4 - Meal ticket 3(Succubus side)": LocationData("Reverse Caverns", 18, [0x526c10c]),
    "RNO4 - Meal ticket 4(Succubus side)": LocationData("Reverse Caverns", 19, [0x526c10e]),
    "RNO4 - Meal ticket 5(Succubus side)": LocationData("Reverse Caverns", 20, [0x526c110]),
    "RNO4 - Zircon(Doppleganger)": LocationData("Reverse Caverns", 21, [0x526c112]),
    "RNO4 - Pot roast(Doppleganger)": LocationData("Reverse Caverns", 22, [0x526c114]),
    "RNO4 - Dark Blade": LocationData("Reverse Caverns", 23, [0x526c116]),
    "RNO4 - Manna prism": LocationData("Reverse Caverns", 24, [0x526c118]),
    "RNO4 - Elixir": LocationData("Reverse Caverns", 25, [0x526c11a]),
    "RNO4 - Osafune katana": LocationData("Reverse Caverns", 26, [0x526c11c]),
    "RNO4 - Doppleganger40 kill": LocationData("Reverse Caverns", 3280),
    "Force of Echo": LocationData("Reverse Caverns", 3281, [0x526e6a0+8, 0x526f86e+8],
                                  False, True, 0x00da00b0, 27, [0x526c11e])
}

rnz0_locations = {
    "RNZ0 - Heart Vessel": LocationData("Necromancy Laboratory", 1, [0x5903072]),
    "RNZ0 - Life Vessel": LocationData("Necromancy Laboratory", 2, [0x5903074]),
    "RNZ0 - Goddess shield": LocationData("Necromancy Laboratory", 3, [0x5903076]),
    "RNZ0 - Manna prism": LocationData("Necromancy Laboratory", 4, [0x5903078]),
    "RNZ0 - Katana": LocationData("Necromancy Laboratory", 5, [0x590307a]),
    "RNZ0 - High potion": LocationData("Necromancy Laboratory", 6, [0x590307c]),
    "RNZ0 - Turquoise": LocationData("Necromancy Laboratory", 7, [0x590307e]),
    "RNZ0 - Ring of Arcana": LocationData("Necromancy Laboratory", 8, [0x5903080]),
    "RNZ0 - Resist dark": LocationData("Necromancy Laboratory", 9, [0x5903082]),
    "RNZ0 - Beezelbub kill": LocationData("Necromancy Laboratory", 3290),
}

rnz1_locations = {
    "RNZ1 - Magic missile": LocationData("Reverse Clock Tower", 0, [0x59bc0d0]),
    "RNZ1 - Karma coin": LocationData("Reverse Clock Tower", 1, [0x59bc0d2]),
    "RNZ1 - Str. potion": LocationData("Reverse Clock Tower", 2, [0x59bc0d4]),
    "RNZ1 - Luminus": LocationData("Reverse Clock Tower", 3, [0x59bc0d6]),
    "RNZ1 - Smart potion": LocationData("Reverse Clock Tower", 4, [0x59bc0d8]),
    "RNZ1 - Dragon helm": LocationData("Reverse Clock Tower", 5, [0x59bc0da]),
    "RNZ1 - Diamond(Hidden room)": LocationData("Reverse Clock Tower", 6, [0x59bc0dc]),
    "RNZ1 - Life apple(Hidden room)": LocationData("Reverse Clock Tower", 7, [0x59bc0de]),
    "RNZ1 - Sunstone(Hidden room)": LocationData("Reverse Clock Tower", 8, [0x59bc0e0]),
    "RNZ1 - Life Vessel": LocationData("Reverse Clock Tower", 9, [0x59bc0e2]),
    "RNZ1 - Heart Vessel": LocationData("Reverse Clock Tower", 10, [0x59bc0e4]),
    "RNZ1 - Moon rod": LocationData("Reverse Clock Tower", 11, [0x59bc0e6]),
    "RNZ1 - Bwaka knife": LocationData("Reverse Clock Tower", 3300, [0x59bc354], True),
    "RNZ1 - Turkey": LocationData("Reverse Clock Tower", 3301, [0x59bc34c], True),
    "RNZ1 - Shuriken": LocationData("Reverse Clock Tower", 3302, [0x59bc350], True),
    "RNZ1 - TNT": LocationData("Reverse Clock Tower", 3303, [0x59bc358], True),
    "RNZ1 - Darkwing bat kill": LocationData("Reverse Clock Tower", 3304),
    "Ring of Vlad": LocationData("Reverse Clock Tower", 3305,
                                 [0x059e8074, 0x059ee2e4, 0x059bdb30], False, True,
                                 0x0016),
}

rtop_locations = {
    "RTOP - Sword of dawn": LocationData("Reverse Castle Keep", 0, [0x57e0160]),
    "RTOP - Iron ball(Above Richter)": LocationData("Reverse Castle Keep", 1, [0x57e0162]),
    "RTOP - Zircon": LocationData("Reverse Castle Keep", 2, [0x57e0164]),
    "RTOP - Bastard sword": LocationData("Reverse Castle Keep", 4, [0x57e0168]),
    "RTOP - Life Vessel 1": LocationData("Reverse Castle Keep", 5, [0x57e016a]),
    "RTOP - Heart Vessel 1": LocationData("Reverse Castle Keep", 6, [0x57e016c]),
    "RTOP - Life Vessel 2": LocationData("Reverse Castle Keep", 7, [0x57e016e]),
    "RTOP - Heart Vessel 2": LocationData("Reverse Castle Keep", 8, [0x57e0170]),
    "RTOP - Life Vessel 3": LocationData("Reverse Castle Keep", 9, [0x57e0172]),
    "RTOP - Heart Vessel 4": LocationData("Reverse Castle Keep", 10, [0x57e0174]),
    "RTOP - Royal cloak": LocationData("Reverse Castle Keep", 11, [0x57e0176]),
    "RTOP - Resist fire(Viewing room)": LocationData("Reverse Castle Keep", 17, [0x57e0182]),
    "RTOP - Resist ice(Viewing room)": LocationData("Reverse Castle Keep", 18, [0x57e0184]),
    "RTOP - Resist thunder(Viewing room)": LocationData("Reverse Castle Keep", 19, [0x57e0186]),
    "RTOP - Resist stone(Viewing room)": LocationData("Reverse Castle Keep", 20, [0x57e0188]),
    "RTOP - High potion(Viewing room)": LocationData("Reverse Castle Keep", 21, [0x57e018a]),
    "RTOP - Garnet": LocationData("Reverse Castle Keep", 22, [0x57e018c]),
    "RTOP - Lightning mail": LocationData("Reverse Castle Keep", 23, [0x57e018e]),
    "RTOP - Library card": LocationData("Reverse Castle Keep", 24, [0x57e0190]),
}

exp_locations_item = {
    "Exploration 10 item": LocationData("Castle Entrance", 31, []),
    "Exploration 20 item": LocationData("Castle Entrance", 32, []),
    "Exploration 30 item": LocationData("Castle Entrance", 33, []),
    "Exploration 40 item": LocationData("Castle Entrance", 34, []),
    "Exploration 50 item": LocationData("Castle Entrance", 35, []),
    "Exploration 60 item": LocationData("Castle Entrance", 36, []),
    "Exploration 70 item": LocationData("Castle Entrance", 37, []),
    "Exploration 80 item": LocationData("Castle Entrance", 38, []),
    "Exploration 90 item": LocationData("Castle Entrance", 39, []),
    "Exploration 100 item": LocationData("Castle Entrance", 40, []),
    "Exploration 110 item": LocationData("Castle Entrance", 41, []),
    "Exploration 120 item": LocationData("Castle Entrance", 42, []),
    "Exploration 130 item": LocationData("Castle Entrance", 43, []),
    "Exploration 140 item": LocationData("Castle Entrance", 44, []),
    "Exploration 150 item": LocationData("Castle Entrance", 45, []),
    "Exploration 160 item": LocationData("Castle Entrance", 46, []),
    "Exploration 170 item": LocationData("Castle Entrance", 47, []),
    "Exploration 180 item": LocationData("Castle Entrance", 48, []),
    "Exploration 190 item": LocationData("Castle Entrance", 49, []),
    "Exploration 200 item": LocationData("Castle Entrance", 50, []),
}

exp_locations_token = {
    "Exploration 10": LocationData("Castle Entrance", 11, []),
    "Exploration 20": LocationData("Castle Entrance", 12, []),
    "Exploration 30": LocationData("Castle Entrance", 13, []),
    "Exploration 40": LocationData("Castle Entrance", 14, []),
    "Exploration 50": LocationData("Castle Entrance", 15, []),
    "Exploration 60": LocationData("Castle Entrance", 16, []),
    "Exploration 70": LocationData("Castle Entrance", 17, []),
    "Exploration 80": LocationData("Castle Entrance", 18, []),
    "Exploration 90": LocationData("Castle Entrance", 19, []),
    "Exploration 100": LocationData("Castle Entrance", 20, []),
    "Exploration 110": LocationData("Castle Entrance", 21, []),
    "Exploration 120": LocationData("Castle Entrance", 22, []),
    "Exploration 130": LocationData("Castle Entrance", 23, []),
    "Exploration 140": LocationData("Castle Entrance", 24, []),
    "Exploration 150": LocationData("Castle Entrance", 25, []),
    "Exploration 160": LocationData("Castle Entrance", 26, []),
    "Exploration 170": LocationData("Castle Entrance", 27, []),
    "Exploration 180": LocationData("Castle Entrance", 28, []),
    "Exploration 190": LocationData("Castle Entrance", 29, []),
    "Exploration 200": LocationData("Castle Entrance", 30, []),
}

are_enemies = {
    "Enemysanity: 25 - Blade soldier": LocationData("Colosseum", 125),
    "Enemysanity: 67 - Paranthropus": LocationData("Colosseum", 167),
    "Enemysanity: 69 - Blade master": LocationData("Colosseum", 169),
    "Enemysanity: 71 - Grave keeper": LocationData("Colosseum", 171),
    "Enemysanity: 74 - Minotaurus": LocationData("Colosseum", 174),
    "Enemysanity: 75 - Werewolf": LocationData("Colosseum", 175),
    "Enemysanity: 77 - Valhalla knight": LocationData("Colosseum", 177),
}

are_drops = {
    "Dropsanity: 25 - Blade soldier": LocationData("Colosseum", 325),
    "Dropsanity: 67 - Paranthropus": LocationData("Colosseum", 367),
    "Dropsanity: 69 - Blade master": LocationData("Colosseum", 369),
    "Dropsanity: 71 - Grave keeper": LocationData("Colosseum", 371),
    "Dropsanity: 77 - Valhalla knight": LocationData("Colosseum", 377),
}

cat_enemies = {
    "Enemysanity: 68 - Slime": LocationData("Catacombs", 168),
    "Enemysanity: 70 - Wereskeleton": LocationData("Catacombs", 170),
    "Enemysanity: 72 - Gremlin": LocationData("Catacombs", 172),
    "Enemysanity: 76 - Bone ark": LocationData("Catacombs", 176),
    "Enemysanity: 81 - Lossoth": LocationData("Catacombs", 181),
    "Enemysanity: 86 - Discus lord": LocationData("Catacombs", 186),
    "Enemysanity: 88 - Large slime": LocationData("Catacombs", 188),
    "Enemysanity: 89 - Hellfire beast": LocationData("Catacombs", 189),
    "Enemysanity: 98 - Legion": LocationData("Catacombs", 198),
}

cat_drops = {
    "Dropsanity: 70 - Wereskeleton": LocationData("Catacombs", 370),
    "Dropsanity: 72 - Gremlin": LocationData("Catacombs", 372),
    "Dropsanity: 76 - Bone ark": LocationData("Catacombs", 376),
    "Dropsanity: 81 - Lossoth": LocationData("Catacombs", 381),
    "Dropsanity: 86 - Discus lord": LocationData("Catacombs", 386),
    "Dropsanity: 89 - Hellfire beast": LocationData("Catacombs", 389),
}

chi_enemies = {
    "Enemysanity: 82 - Salem witch": LocationData("Abandoned Mine", 182),
    "Enemysanity: 90 - Cerberos": LocationData("Abandoned Mine", 190),
    "Enemysanity: 95 - Venus weed": LocationData("Abandoned Mine", 195),
}

chi_drops = {
    "Dropsanity: 82 - Salem witch": LocationData("Abandoned Mine", 382),
    "Dropsanity: 95 - Venus weed": LocationData("Abandoned Mine", 395),
}

# Mudman only appears on Lesser Demon fight keep it out
lib_enemies = {
    "Enemysanity: 17 - Thornweed": LocationData("Long Library", 117),
    "Enemysanity: 40 - Spellbook": LocationData("Long Library", 140),
    "Enemysanity: 42 - Ectoplasm": LocationData("Long Library", 142),
    "Enemysanity: 47 - Dhuron": LocationData("Long Library", 147),
    "Enemysanity: 50 - Magic tome": LocationData("Long Library", 150),
    "Enemysanity: 54 - Corpseweed": LocationData("Long Library", 154),
    "Enemysanity: 65 - Flea armor": LocationData("Long Library", 165),
    "Enemysanity: 80 - Lesser demon": LocationData("Long Library", 180),
}

lib_drops = {
    "Dropsanity: 17 - Thornweed": LocationData("Long Library", 317),
    "Dropsanity: 40 - Spellbook": LocationData("Long Library", 340),
    "Dropsanity: 42 - Ectoplasm": LocationData("Long Library", 342),
    "Dropsanity: 47 - Dhuron": LocationData("Long Library", 347),
    "Dropsanity: 50 - Magic tome": LocationData("Long Library", 350),
    "Dropsanity: 54 - Corpseweed": LocationData("Long Library", 354),
    "Dropsanity: 65 - Flea armor": LocationData("Long Library", 365),
}

dai_enemies = {
    "Enemysanity: 33 - Bone Pillar": LocationData("Royal Chapel", 133),
    "Enemysanity: 41 - Winged guard": LocationData("Royal Chapel", 141),
    "Enemysanity: 46 - Corner guard": LocationData("Royal Chapel", 146),
    "Enemysanity: 52 - Black crow": LocationData("Royal Chapel", 152),
    "Enemysanity: 53 - Blue raven": LocationData("Royal Chapel", 153),
    "Enemysanity: 58 - Bone halberd": LocationData("Royal Chapel", 158),
    "Enemysanity: 60 - Hunting girl": LocationData("Royal Chapel", 160),
    "Enemysanity: 63 - Spectral sword(swords)": LocationData("Royal Chapel", 163),
    "Enemysanity: 66 - Hippogryph": LocationData("Royal Chapel", 166),
}

dai_drops = {
    "Dropsanity: 33 - Bone Pillar": LocationData("Royal Chapel", 333),
    "Dropsanity: 41 - Winged guard": LocationData("Royal Chapel", 341),
    "Dropsanity: 46 - Corner guard": LocationData("Royal Chapel", 346),
    "Dropsanity: 52 - Black crow": LocationData("Royal Chapel", 352),
    "Dropsanity: 53 - Blue raven": LocationData("Royal Chapel", 353),
    "Dropsanity: 58 - Bone halberd": LocationData("Royal Chapel", 358),
    "Dropsanity: 60 - Hunting girl": LocationData("Royal Chapel", 360),
    "Dropsanity: 63 - Spectral sword(swords)": LocationData("Royal Chapel", 363),
}

no0_enemies = {
    "Enemysanity: 14 - Slinger": LocationData("Marble Gallery", 114),
    "Enemysanity: 15 - Ouija table": LocationData("Marble Gallery", 115),
    "Enemysanity: 16 - Skelerang": LocationData("Marble Gallery", 116),
    "Enemysanity: 19 - Ghost": LocationData("Marble Gallery", 119),
    "Enemysanity: 20 - Marionette": LocationData("Marble Gallery", 120),
    "Enemysanity: 22 - Diplocephalus": LocationData("Marble Gallery", 122),
    "Enemysanity: 23 - Flea man": LocationData("Marble Gallery", 123),
    "Enemysanity: 28 - Plate lord": LocationData("Marble Gallery", 128),
    "Enemysanity: 29 - Stone rose": LocationData("Marble Gallery", 129),
    "Enemysanity: 31 - Ctulhu": LocationData("Marble Gallery", 131),
}

no0_drops = {
    "Dropsanity: 14 - Slinger": LocationData("Marble Gallery", 314),
    "Dropsanity: 15 - Ouija table": LocationData("Marble Gallery", 315),
    "Dropsanity: 16 - Skelerang": LocationData("Marble Gallery", 316),
    "Dropsanity: 19 - Ghost": LocationData("Marble Gallery", 319),
    "Dropsanity: 20 - Marionette": LocationData("Marble Gallery", 320),
    "Dropsanity: 22 - Diplocephalus": LocationData("Marble Gallery", 322),
    "Dropsanity: 23 - Flea man": LocationData("Marble Gallery", 323),
    "Dropsanity: 28 - Plate lord": LocationData("Marble Gallery", 328),
    "Dropsanity: 29 - Stone rose": LocationData("Marble Gallery", 329),
    "Dropsanity: 31 - Ctulhu": LocationData("Marble Gallery", 331),
}

no1_enemies = {
    "Enemysanity: 24 - Medusa head": LocationData("Outer Wall", 124),
    "Enemysanity: 26 - Bone musket": LocationData("Outer Wall", 126),
    "Enemysanity: 27 - Medusa head(yellow)": LocationData("Outer Wall", 127),
    "Enemysanity: 30 - Axe knight(armored)": LocationData("Outer Wall", 130),
    "Enemysanity: 32 - Bone archer": LocationData("Outer Wall", 132),
    "Enemysanity: 34 - Doppleganger10": LocationData("Outer Wall", 134),
    "Enemysanity: 38 - Skeleton ape": LocationData("Outer Wall", 138),
    "Enemysanity: 39 - Spear guard": LocationData("Outer Wall", 139),
    "Enemysanity: 43 - Sword lord": LocationData("Outer Wall", 143),
    "Enemysanity: 45 - Armor lord": LocationData("Outer Wall", 145),
}

no1_drops = {
    "Dropsanity: 24 - Medusa head": LocationData("Outer Wall", 324),
    "Dropsanity: 26 - Bone musket": LocationData("Outer Wall", 326),
    "Dropsanity: 27 - Medusa head(yellow)": LocationData("Outer Wall", 327),
    "Dropsanity: 30 - Axe knight(armored)": LocationData("Outer Wall", 330),
    "Dropsanity: 32 - Bone archer": LocationData("Outer Wall", 332),
    "Dropsanity: 34 - Doppleganger10": LocationData("Outer Wall", 334),
    "Dropsanity: 38 - Skeleton ape": LocationData("Outer Wall", 338),
    "Dropsanity: 39 - Spear guard": LocationData("Outer Wall", 339),
    "Dropsanity: 43 - Sword lord": LocationData("Outer Wall", 343),
    "Dropsanity: 45 - Armor lord": LocationData("Outer Wall", 345),
}

no2_enemies = {
    "Enemysanity: 57 - Spectral sword": LocationData("Olrox's Quarters", 157),
    "Enemysanity: 83 - Blade": LocationData("Olrox's Quarters", 183),
    "Enemysanity: 85 - Hammer": LocationData("Olrox's Quarters", 185),
    "Enemysanity: 92 - Olrox": LocationData("Olrox's Quarters", 192),
}

no2_drops = {
    "Dropsanity: 57 - Spectral sword": LocationData("Olrox's Quarters", 357),
    "Dropsanity: 83 - Blade": LocationData("Olrox's Quarters", 383),
    "Dropsanity: 85 - Hammer": LocationData("Olrox's Quarters", 385),
}

no3_enemies = {
    "Enemysanity: 3 - Bat": LocationData("Castle Entrance", 103),
    "Enemysanity: 5 - Zombie": LocationData("Castle Entrance", 105),
    "Enemysanity: 6 - Merman": LocationData("Castle Entrance", 106),
    "Enemysanity: 8 - Warg": LocationData("Castle Entrance", 108),
    "Enemysanity: 10 - Merman(red)": LocationData("Castle Entrance", 110),
    "Enemysanity: 35 - Owl": LocationData("Castle Entrance", 135),
    "Enemysanity: 62 - Owl knight": LocationData("Castle Entrance", 162),
    "Enemysanity: 84 - Gurkha": LocationData("Castle Entrance", 184),
}

no3_drops = {
    "Dropsanity: 3 - Bat": LocationData("Castle Entrance", 303),
    "Dropsanity: 5 - Zombie": LocationData("Castle Entrance", 305),
    "Dropsanity: 6 - Merman": LocationData("Castle Entrance", 306),
    "Dropsanity: 10 - Merman(red)": LocationData("Castle Entrance", 310),
    "Dropsanity: 62 - Owl knight": LocationData("Castle Entrance", 362),
    "Dropsanity: 84 - Gurkha": LocationData("Castle Entrance", 384),
}

no4_enemies = {
    "Enemysanity: 37 - Scylla wyrm": LocationData("Underground Caverns", 137),
    "Enemysanity: 44 - Toad": LocationData("Underground Caverns", 144),
    "Enemysanity: 48 - Frog": LocationData("Underground Caverns", 148),
    "Enemysanity: 49 - Frozen shade": LocationData("Underground Caverns", 149),
    "Enemysanity: 59 - Scylla": LocationData("Underground Caverns", 159),
    "Enemysanity: 79 - Fishhead": LocationData("Underground Caverns", 179),
    "Enemysanity: 91 - Killer fish": LocationData("Underground Caverns", 191),
    "Enemysanity: 93 - Succubus": LocationData("Underground Caverns", 193),
}

no4_drops = {
    "Dropsanity: 44 - Toad": LocationData("Underground Caverns", 344),
    "Dropsanity: 48 - Frog": LocationData("Underground Caverns", 348),
    "Dropsanity: 49 - Frozen shade": LocationData("Underground Caverns", 349),
    "Dropsanity: 79 - Fishhead": LocationData("Underground Caverns", 379),
    "Dropsanity: 91 - Killer fish": LocationData("Underground Caverns", 391),
}

nz0_enemies = {
    "Enemysanity: 2 - Blood skeleton": LocationData("Alchemy Laboratory", 102),
    "Enemysanity: 7 - Skeleton": LocationData("Alchemy Laboratory", 107),
    "Enemysanity: 9 - Bone scimitar": LocationData("Alchemy Laboratory", 109),
    "Enemysanity: 11 - Spittle bone": LocationData("Alchemy Laboratory", 111),
    "Enemysanity: 12 - Axe knight": LocationData("Alchemy Laboratory", 112),
    "Enemysanity: 13 - Bloody zombie": LocationData("Alchemy Laboratory", 113),
    "Enemysanity: 18 - Gaibon": LocationData("Alchemy Laboratory", 118),
    "Enemysanity: 21 - Slogra": LocationData("Alchemy Laboratory", 121),
}

nz0_drops = {
    "Dropsanity: 7 - Skeleton": LocationData("Alchemy Laboratory", 307),
    "Dropsanity: 9 - Bone scimitar": LocationData("Alchemy Laboratory", 309),
    "Dropsanity: 12 - Axe knight": LocationData("Alchemy Laboratory", 312),
    "Dropsanity: 13 - Bloody zombie": LocationData("Alchemy Laboratory", 313),
}

nz1_enemies = {
    "Enemysanity: 36 - Phantom skull": LocationData("Clock Tower", 136),
    "Enemysanity: 51 - Skull lord": LocationData("Clock Tower", 151),
    "Enemysanity: 55 - Flail guard": LocationData("Clock Tower", 155),
    "Enemysanity: 64 - Vandal sword": LocationData("Clock Tower", 164),
    "Enemysanity: 73 - Harpy": LocationData("Clock Tower", 173),
    "Enemysanity: 78 - Cloaked knight": LocationData("Clock Tower", 178),
    "Enemysanity: 87 - Karasuman": LocationData("Clock Tower", 187),
}

nz1_drops = {
    "Dropsanity: 36 - Phantom skull": LocationData("Clock Tower", 336),
    "Dropsanity: 51 - Skull lord": LocationData("Clock Tower", 351),
    "Dropsanity: 55 - Flail guard": LocationData("Clock Tower", 355),
    "Dropsanity: 64 - Vandal sword": LocationData("Clock Tower", 364),
    "Dropsanity: 73 - Harpy": LocationData("Clock Tower", 373),
    "Dropsanity: 78 - Cloaked knight": LocationData("Clock Tower", 378),
}

top_enemies = {
    "Enemysanity: 56 - Flea rider": LocationData("Castle Keep", 156),
    # "Enemysanity: 140 - Richter belmont": LocationData("Castle Keep", 240),
}

top_drops = {
    "Dropsanity: 56 - Flea rider": LocationData("Castle Keep", 356),
}

rare_enemies = {
    "Enemysanity: 108 - Werewolf(reverse)": LocationData("Reverse Colosseum", 208),
    "Enemysanity: 112 - Minotaur": LocationData("Reverse Colosseum", 212),
    "Enemysanity: 115 - White dragon": LocationData("Reverse Colosseum", 215),
    "Enemysanity: 132 - Fake grant": LocationData("Reverse Colosseum", 232),
    "Enemysanity: 133 - Fake trevor": LocationData("Reverse Colosseum", 233),
    "Enemysanity: 135 - Fake sipha": LocationData("Reverse Colosseum", 235),
    "Enemysanity: 137 - Azaghal": LocationData("Reverse Colosseum", 237),
}

rare_drops = {
    "Dropsanity: 108 - Werewolf(reverse)": LocationData("Reverse Colosseum", 408),
    "Dropsanity: 112 - Minotaur": LocationData("Reverse Colosseum", 412),
    "Dropsanity: 137 - Azaghal": LocationData("Reverse Colosseum", 437),
}

rcat_enemies = {
    "Enemysanity: 138 - Frozen half": LocationData("Floating Catacombs", 238),
    "Enemysanity: 139 - Salome": LocationData("Floating Catacombs", 239),
    "Enemysanity: 142 - Galamoth": LocationData("Floating Catacombs", 242),
}

rcat_drops = {
    "Dropsanity: 138 - Frozen half": LocationData("Floating Catacombs", 438),
    "Dropsanity: 139 - Salome": LocationData("Floating Catacombs", 439),
}

rchi_enemies = {
    "Enemysanity: 144 - Death": LocationData("Floating Catacombs", 244),
}

rdai_enemies = {
    "Enemysanity: 101 - Ballon pod": LocationData("Anti-Chapel", 201),
    "Enemysanity: 107 - Archer": LocationData("Anti-Chapel", 207),
    "Enemysanity: 109 - Black panther": LocationData("Anti-Chapel", 209),
    "Enemysanity: 118 - Sniper of goth": LocationData("Anti-Chapel", 218),
    "Enemysanity: 119 - Spectral sword(shields)": LocationData("Anti-Chapel", 219),
    "Enemysanity: 130 - Medusa": LocationData("Anti-Chapel", 230),
    "Enemysanity: 134 - Imp": LocationData("Anti-Chapel", 234),
}

rdai_drops = {
    "Dropsanity: 107 - Archer": LocationData("Anti-Chapel", 407),
    "Dropsanity: 109 - Black panther": LocationData("Anti-Chapel", 409),
    "Dropsanity: 118 - Sniper of goth": LocationData("Anti-Chapel", 418),
    "Dropsanity: 119 - Spectral sword(shields)": LocationData("Anti-Chapel", 419),
    "Dropsanity: 134 - Imp": LocationData("Anti-Chapel", 434),
}

rlib_enemies = {
    "Enemysanity: 96 - Lion": LocationData("Forbidden Library", 196),
    "Enemysanity: 97 - Scarecrow": LocationData("Forbidden Library", 197),
    "Enemysanity: 99 - Schmoo": LocationData("Forbidden Library", 199),
    "Enemysanity: 100 - Tin man": LocationData("Forbidden Library", 200),
}

rlib_drops = {
    "Dropsanity: 96 - Lion": LocationData("Forbidden Library", 396),
    "Dropsanity: 97 - Scarecrow": LocationData("Forbidden Library", 397),
    "Dropsanity: 99 - Schmoo": LocationData("Forbidden Library", 399),
    "Dropsanity: 100 - Tin man": LocationData("Forbidden Library", 400),
}

rno0_enemies = {
    "Enemysanity: 4 - Stone skill": LocationData("Black Marble Gallery", 104),
    "Enemysanity: 106 - Jack O'bones": LocationData("Black Marble Gallery", 206),
    "Enemysanity: 113 - Nova skeleton": LocationData("Black Marble Gallery", 213),
    "Enemysanity: 125 - Gorgon": LocationData("Black Marble Gallery", 225),
    "Enemysanity: 143 - Guardian": LocationData("Black Marble Gallery", 243),
}

rno0_drops = {
    "Dropsanity: 106 - Jack O'bones": LocationData("Black Marble Gallery", 406),
    "Dropsanity: 113 - Nova skeleton": LocationData("Black Marble Gallery", 413),
    "Dropsanity: 125 - Gorgon": LocationData("Black Marble Gallery", 425),
    "Dropsanity: 143 - Guardian": LocationData("Black Marble Gallery", 443),
}

rno1_enemies = {
    "Enemysanity: 131 - The creature": LocationData("Reverse Outer Wall", 231),
}

rno2_enemies = {
    "Enemysanity: 104 - Flying zombie": LocationData("Death Wing's Lair", 204),
    "Enemysanity: 120 - Ghost dancer": LocationData("Death Wing's Lair", 220),
    "Enemysanity: 126 - Malachi": LocationData("Death Wing's Lair", 226),
    "Enemysanity: 127 - Akmodan II": LocationData("Death Wing's Lair", 227),
}

rno2_drops = {
    "Dropsanity: 104 - Flying zombie": LocationData("Death Wing's Lair", 404),
    "Dropsanity: 120 - Ghost dancer": LocationData("Death Wing's Lair", 420),
    "Dropsanity: 126 - Malachi": LocationData("Death Wing's Lair", 426),
    "Dropsanity: 87 - Karasuman": LocationData("Death Wing's Lair", 387),
}

rno3_enemies = {
    "Enemysanity: 111 - Dragon rider": LocationData("Reverse Entrance", 211),
    "Enemysanity: 114 - Orobourous": LocationData("Reverse Entrance", 214),
    "Enemysanity: 116 - Fire warg": LocationData("Reverse Entrance", 216),
    "Enemysanity: 141 - Dodo bird": LocationData("Reverse Entrance", 241),
}

rno3_drops = {
    "Dropsanity: 114 - Orobourous": LocationData("Reverse Entrance", 414),
    "Dropsanity: 116 - Fire warg": LocationData("Reverse Entrance", 416),
    "Dropsanity: 121 - Warg rider": LocationData("Reverse Entrance", 421),
    "Dropsanity: 141 - Dodo bird": LocationData("Reverse Entrance", 441),
}

rno4_enemies = {
    "Enemysanity: 117 - Rock knight": LocationData("Reverse Caverns", 217),
    "Enemysanity: 122 - Cave troll": LocationData("Reverse Caverns", 222),
    "Enemysanity: 123 - Dark octopus": LocationData("Reverse Caverns", 223),
    "Enemysanity: 128 - Blue venus weed": LocationData("Reverse Caverns", 228),
    "Enemysanity: 129 - Doppleganger40": LocationData("Reverse Caverns", 229),
}

rno4_drops = {
    "Dropsanity: 117 - Rock knight": LocationData("Reverse Caverns", 417),
    "Dropsanity: 122 - Cave troll": LocationData("Reverse Caverns", 422),
    "Dropsanity: 123 - Dark octopus": LocationData("Reverse Caverns", 423),
    "Dropsanity: 128 - Blue venus weed": LocationData("Reverse Caverns", 428),
}

rnz0_enemies = {
    "Enemysanity: 105 - Bitterfly": LocationData("Necromancy Laboratory", 205),
    "Enemysanity: 124 - Fire demon": LocationData("Necromancy Laboratory", 224),
    "Enemysanity: 136 - Beezelbub": LocationData("Necromancy Laboratory", 236),
}

rnz0_drops = {
    "Dropsanity: 105 - Bitterfly": LocationData("Necromancy Laboratory", 405),
    "Dropsanity: 124 - Fire demon": LocationData("Necromancy Laboratory", 424),
}

rnz1_enemies = {
    "Enemysanity: 103 - Bomb knight": LocationData("Reverse Clock Tower", 203),
    "Enemysanity: 110 - Darkwing bat": LocationData("Reverse Clock Tower", 210),
}

rnz1_drops = {
    "Dropsanity: 103 - Bomb knight": LocationData("Reverse Clock Tower", 403),
    "Dropsanity: 80 - Lesser demon": LocationData("Necromancy Laboratory", 380),
}

rtop_enemies = {
    "Enemysanity: 94 - Tombstone": LocationData("Reverse Castle Keep", 194),
    "Enemysanity: 102 - Yorick": LocationData("Reverse Castle Keep", 202),
}

rtop_drops = {
    "Dropsanity: 94 - Tombstone": LocationData("Reverse Castle Keep", 394),
    "Dropsanity: 102 - Yorick": LocationData("Reverse Castle Keep", 402),
}

normal_locations = {
    **are_locations,
    **cat_locations,
    **chi_locations,
    **dai_locations,
    **lib_locations,
    **no0_locations,
    **no1_locations,
    **no2_locations,
    **no3_locations,
    **no4_locations,
    **nz0_locations,
    **nz1_locations,
    **top_locations
}

reverse_locations = {
    **rare_locations,
    **rcat_locations,
    **rcen_locations,
    **rchi_locations,
    **rdai_locations,
    **rlib_locations,
    **rno0_locations,
    **rno1_locations,
    **rno2_locations,
    **rno3_locations,
    **rno4_locations,
    **rnz0_locations,
    **rnz1_locations,
    **rtop_locations
}

enemy_locations = {
    **are_enemies,
    **cat_enemies,
    **chi_enemies,
    **lib_enemies,
    **dai_enemies,
    **no0_enemies,
    **no1_enemies,
    **no2_enemies,
    **no3_enemies,
    **no4_enemies,
    **nz0_enemies,
    **nz1_enemies,
    **top_enemies,
    **rare_enemies,
    **rcat_enemies,
    **rchi_enemies,
    **rdai_enemies,
    **rlib_enemies,
    **rno0_enemies,
    **rno1_enemies,
    **rno2_enemies,
    **rno3_enemies,
    **rno4_enemies,
    **rnz0_enemies,
    **rnz1_enemies,
    **rtop_enemies
}

drop_locations = {
    **are_drops,
    **cat_drops,
    **chi_drops,
    **lib_drops,
    **dai_drops,
    **no0_drops,
    **no1_drops,
    **no2_drops,
    **no3_drops,
    **no4_drops,
    **nz0_drops,
    **nz1_drops,
    **top_drops,
    **rare_drops,
    **rcat_drops,
    **rdai_drops,
    **rlib_drops,
    **rno0_drops,
    **rno2_drops,
    **rno3_drops,
    **rno4_drops,
    **rnz0_drops,
    **rnz1_drops,
    **rtop_drops
}

location_table = {
    **normal_locations,
    **reverse_locations,
    **exp_locations_item,
    **exp_locations_token,
    **enemy_locations,
    **drop_locations
}


def get_location_data(location_id: int) -> LocationData:
    """ Try that
    try:
        l_id = int(str(location_id)[5:])
    except:
        return None
    """
    l_id = int(str(location_id)[5:])
    for k, v in location_table.items():
        data: LocationData = v
        if data.game_id == l_id:
            return data
