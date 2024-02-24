from BaseClasses import Location


# I'm assuming this its just to add uniqueness to ids with all worlds in a seed I have no idea how this number is
# calculate, so just threw some random numbers. 127{zone id}{game id}
base_location_id = 127000000


class ZoneData:
    def __init__(self, abrev: str, name: str):
        self.abrev = abrev
        self.name = name


zones_dict = {
    0: ZoneData("ST0", "Final Stage: Bloodlines"),
    1: ZoneData("ARE", "Colosseum"),
    2: ZoneData("CAT", "Catacombs"),
    3: ZoneData("CEN", "Center Cube"),
    4: ZoneData("CHI", "Abandoned Mine"),
    5: ZoneData("DAI", "Royal Chapel"),
    6: ZoneData("DRE", "Nightmare"),
    7: ZoneData("LIB", "Long Library"),
    8: ZoneData("NO0", "Marble Gallery"),
    9: ZoneData("NO1", "Outer Wall"),
    10: ZoneData("NO2", "Olrox's Quarters"),
    11: ZoneData("NO3", "Castle Entrance"),
    12: ZoneData("NP3", "Castle Entrance (after visiting Alchemy Laboratory)"),
    13: ZoneData("NO4", "Underground Caverns"),
    14: ZoneData("NZ0", "Alchemy Laboratory"),
    15: ZoneData("NZ1", "Clock Tower"),
    16: ZoneData("TOP", "Castle Keep"),
    17: ZoneData("WRP", "Warp rooms"),
    18: ZoneData("RARE", "Reverse Colosseum"),
    19: ZoneData("RCAT", "Floating Catacombs"),
    20: ZoneData("RCEN", "Reverse Center Cube"),
    21: ZoneData("RCHI", "Cave"),
    22: ZoneData("RDAI", "Anti-Chapel"),
    23: ZoneData("RLIB", "Forbidden Library"),
    24: ZoneData("RNO0", "Black Marble Gallery"),
    25: ZoneData("RNO1", "Reverse Outer Wall"),
    26: ZoneData("RNO2", "Death Wing's Lair"),
    27: ZoneData("RNO3", "Reverse Entrance"),
    28: ZoneData("RNO4", "Reverse Caverns"),
    29: ZoneData("RNZ0", "Necromancy Laboratory"),
    30: ZoneData("RNZ1", "Reverse Clock Tower"),
    31: ZoneData("RTOP", "Reverse Castle Keep"),
    32: ZoneData("RWRP", "Reverse Warp rooms"),
    33: ZoneData("BO0", "Olrox"),
    34: ZoneData("BO1", "Legion"),  # or Granfaloon
    35: ZoneData("BO2", "Werewolf & Minotaur"),
    36: ZoneData("BO3", "Scylla"),
    37: ZoneData("BO4", "Doppleganger10"),
    38: ZoneData("BO5", "Hippogryph"),
    39: ZoneData("BO6", "Richter"),
    40: ZoneData("BO7", "Cerberus"),
    41: ZoneData("RBO0", "Trio"),
    42: ZoneData("RBO1", "Beezlebub"),
    43: ZoneData("RBO2", "Death"),
    44: ZoneData("RBO3", "Medusa"),
    45: ZoneData("RBO4", "Creature"),
    46: ZoneData("RBO5", "Doppleganger40"),
    47: ZoneData("RBO6", "Shaft/Dracula"),
    48: ZoneData("RBO7", "Akmodan II"),
    49: ZoneData("RBO8", "Galamoth"),
}


def get_zone_id(zone_name: str) -> int:
    for k, v in zones_dict.items():
        if v.name == zone_name:
            return k * 10000


class SotnLocation(Location):
    game = "Symphony of the Night"
    # parent_region = Optional[Region] add zones


class LocationData:
    def __init__(self, zone: str, game_id, rom_address: list = None, no_offset=False, can_be_relic=False, delete=0):
        self.zone = zone
        self.game_id = game_id
        self.rom_address = [] if rom_address is None else rom_address
        self.can_be_relic = can_be_relic
        self.no_offset = no_offset
        self.delete = delete
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
                                False, True, 0x000e00b0),
    "Power of Wolf": LocationData("Castle Entrance", 3113,
                                  [0x4b6b14a+8, 0x4b6b9ac+8, 0x53f8f16+8, 0x53f9714+8],
                                  False,True, 0x000e00b1)
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
                               False, True, 0x001700b0),
    "Gravity Boots": LocationData("Marble Gallery", 3082, [0x48fc9b2+8, 0x48fd944+8],
                                  False, True, 0x001700b1)
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
                                 False, True, 0x002e00b0)
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
                                False, True, 0x002600b2),
    "Faerie Scroll": LocationData("Long Library", 3073, [0x47a5718+8, 0x47a5dca+8],
                                  False, True, 0x00f400b1),
    "Jewel of Open": LocationData("Long Library", 3074, [0x047a321c], False,
                                  True),
    "Faerie Card": LocationData("Long Library", 3075, [0x47a577c+8, 0x47a5f64+8],
                                False,True, 0x002600b0),
}

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
                                True, 0x002300b0)
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
                               True, 0x002400b0),
    "Power of Mist": LocationData("Castle Keep", 3161, [0x5610db0+8, 0x5611424+8], False,
                                  True, 0x002400b1),
    "Ghost Card": LocationData("Castle Keep", 3162, [0x5611274+8, 0x5611950+8], False,
                               True, 0x002400b2),
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
                                 True, 0x003300b0)
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
                                False, True, 0x001a00b0),
    "Sword Card": LocationData("Olrox's Quarters", 3102, [0x4aa3f6e+8, 0x4aa47c6+8],
                               False, True, 0x001a00b1),
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
                                False, True, 0x003f00b0),
    "Merman Statue": LocationData("Underground Caverns", 3133, [0x4c3516c+8, 0x4c36472+8],
                                  False, True, 0x003f00b1)
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
                               True, 0x001600b0),
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
                              False, True, 0x00ff00b0)
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
    "RNO1 - Dim Sum set": LocationData("Reverse Outer Wall", 3240, [0x507d08c], True),
    "RNO1 - Creature kill": LocationData("Reverse Outer Wall", 3241),
    "Tooth of Vlad": LocationData("Reverse Outer Wall", 3242,
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
                                  False, True, 0x00da00b0)
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

location_table = {
    **normal_locations,
    **reverse_locations
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
