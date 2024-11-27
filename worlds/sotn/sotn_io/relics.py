from constants import RELIC, ZONE, EXTENSION

relics_list = [
    {
        "name": "Soul of Bat",
        "ability": RELIC["SOUL_OF_BAT"],
        "relicId": 0,
        "entity": {"zones": [ZONE["LIB"]], "entities": [0x3826, 0x3f06], },
    }, {
        "name": "Fire of Bat",
        "ability": RELIC["FIRE_OF_BAT"],
        "relicId": 1,
        "entity": {"zones": [ZONE["NZ1"]], "entities": [0x28ae, 0x32ba], },
        "asItem": {"y": 0x00c9, },
    }, {
        "name": "Echo of Bat",
        "ability": RELIC["ECHO_OF_BAT"],
        "relicId": 2,
        "entity": {"zones": [ZONE["NO2"]], "entities": [0x35f6, 0x3d1e], },
        "asItem": {"y": 0x009d, },
    }, {
        "name": "Force of Echo",
        "ability": RELIC["FORCE_OF_ECHO"],
        "relicId": 3,
        "entity": {"zones": [ZONE["RNO4"]], "entities": [0x3718, 0x4686], },
        "asItem": {"y": 0x00b9, },
    }, {
        "name": "Soul of Wolf",
        "ability": RELIC["SOUL_OF_WOLF"],
        "relicId": 4,
        "entity": {"zones": [ZONE["NO1"]], "entities": [0x3c2e, 0x4356], },
        "asItem": {"y": 0x0331, },
    }, {
        "name": "Power of Wolf",
        "ability": RELIC["POWER_OF_WOLF"],
        "relicId": 5,
        "entity": {"zones": [ZONE["NO3"], ZONE["NP3"]], "entities": [0x41e2, 0x4914, 0x3fbe, 0x468c], },
        "asItem": {"y": 0x00c8, },
    }, {
        "name": "Skill of Wolf",
        "ability": RELIC["SKILL_OF_WOLF"],
        "relicId": 6,
        "entity": {"zones": [ZONE["NZ0"]], "entities": [0x3054, 0x3998], "replaceWithRelic": "false", },
        "ids": {"zone": [ZONE["NZ0"]], "addresses": [0x054b1d5a], },
        "asItem": {"x": 0x007e, "y": 0x00b9, },
    }, {
        "name": "Form of Mist",
        "ability": RELIC["FORM_OF_MIST"],
        "relicId": 7,
        "entity": {"zones": [ZONE["ARE"]], "entities": [0x304a, 0x36c8], },
        "asItem": {"y": 0x0099, },
    }, {
        "name": "Power of Mist",
        "ability": RELIC["POWER_OF_MIST"],
        "relicId": 8,
        "entity": {"zones": [ZONE["TOP"]], "entities": [0x2138, 0x27ac], },
        "asItem": {"y": 0x04c8, },
    }, {
        "name": "Gas Cloud",
        "ability": RELIC["GAS_CLOUD"],
        "relicId": 9,
        "entity": {"zones": [ZONE["RCAT"]], "entities": [0x2596, 0x30ba], },
        "asItem": {"x": 0x0016, "y": 0x00b1, },
    }, {
        "name": "Cube of Zoe",
        "ability": RELIC["CUBE_OF_ZOE"],
        "relicId": 10,
        "entity": {"zones": [ZONE["NO3"], ZONE["NP3"]], "entities": [0x411a, 0x48a6, 0x3ece, 0x460a], },
        "asItem": {"y": 0x007b, },
    }, {
        "name": "Spirit Orb",
        "ability": RELIC["SPIRIT_ORB"],
        "relicId": 11,
        "entity": {"zones": [ZONE["NO0"]], "entities": [0x309e, 0x3ff0], },
        "asItem": {"x": 0x0043, },
    }, {
        "name": "Gravity Boots",
        "ability": RELIC["GRAVITY_BOOTS"],
        "relicId": 12,
        "entity": {"zones": [ZONE["NO0"]], "entities": [0x298a, 0x37ec], },
        "asItem": {"y": 0x00b9, },
    }, {
        "name": "Leap Stone",
        "ability": RELIC["LEAP_STONE"],
        "relicId": 13,
        "entity": {"zones": [ZONE["TOP"]], "entities": [0x2142, 0x286a], },
        "asItem": {"y": 0x0729, },
    }, {
        "name": "Holy Symbol",
        "ability": RELIC["HOLY_SYMBOL"],
        "relicId": 14,
        "entity": {"zones": [ZONE["NO4"]], "entities": [0x3ea6, 0x4f38], },
        "asItem": {"y": 0x00b9, },
    }, {
        "name": "Faerie Scroll",
        "ability": RELIC["FAERIE_SCROLL"],
        "relicId": 15,
        "entity": {"zones": [ZONE["LIB"]], "entities": [0x3510, 0x3a92], },
        "asItem": {"y": 0x00b9, },
    }, {
        "name": "Jewel of Open",
        "ability": RELIC["JEWEL_OF_OPEN"],
        "relicId": 16,
        "ids": {"zone": [ZONE["LIB"]], "addresses": [0x047a321c], },
        "erase": {
            "instructions": [
                {"addresses": [0x047dbde0], "instruction": 0x34020001, },
            ],
        },
        "replaceWithRelic": "replaceShopRelicWithRelic",
        "replaceWithItem": "replaceShopRelicWithItem",
        "consumesItem": False,
    }, {
        "name": "Merman Statue",
        "ability": RELIC["MERMAN_STATUE"],
        "relicId": 17,
        "entity": {"zones": [ZONE["NO4"]], "entities": [0x4004, 0x50aa], },
        "asItem": {"y": 0x00b9, },
    }, {
        "name": "Bat Card",
        "ability": RELIC["BAT_CARD"],
        "relicId": 18,
        "entity": {"zones": [ZONE["NZ0"], ZONE["NZ0"]], "entities": [0x2a8c, 0x33d0, 0x2ad2, 0x343e],
                   "replaceWithRelic": "false", },
        "ids": {"zone": [ZONE["NZ0"]], "addresses": [0x054b1d58], },
        "asItem": {"x": 0x007e, "y": 0x00b9, },
    }, {
        "name": "Ghost Card",
        "ability": RELIC["GHOST_CARD"],
        "relicId": 19,
        "entity": {"zones": [ZONE["TOP"]], "entities": [0x25fc, 0x2ba8], },
        "asItem": {"y": 0x02a8, },
    }, {
        "name": "Faerie Card",
        "ability": RELIC["FAERIE_CARD"],
        "relicId": 20,
        "entity": {"zones": [ZONE["LIB"]], "entities": [0x3574, 0x3c2c], },
        "asItem": {"y": 0x00b9, },
    }, {
        "name": "Demon Card",
        "ability": RELIC["DEMON_CARD"],
        "relicId": 21,
        "entity": {"zones": [ZONE["CHI"]], "entities": [0x1ade, 0x1e62], },
        "asItem": {"y": 0x00b8, },
    }, {
        "name": "Sword Card",
        "ability": RELIC["SWORD_CARD"],
        "relicId": 22,
        "entity": {"zones": [ZONE["NO2"]], "entities": [0x3416, 0x3b3e], },
        "asItem": {"y": 0x009c, },
    }, {
        "name": "Sprite Card",
        "ability": RELIC["SPRITE_CARD"],
        "relicId": 23,
        "extension": EXTENSION["GUARDED"],
    }, {
        "name": "Nosedevil Card",
        "ability": RELIC["NOSEDEVIL_CARD"],
        "relicId": 24,
        "extension": EXTENSION["GUARDED"],
    }, {
        "name": "Heart of Vlad",
        "ability": RELIC["HEART_OF_VLAD"],
        "relicId": 25,
        "entity": {"zones": [ZONE["RDAI"]], "entities": [0x1dc4, 0x2730], },
        "reward": {"zone": [ZONE["RBO3"]], "index": 0x11, },
        "erase": {
            "instructions": [
                {"addresses": [0x06757b54], "instruction": 0x34020000, },
            ],
        },
        "replaceWithItem": {"boss": ZONE["RBO3"], "entry": 0x034950, "inj": 0x047900, },
        "asItem": {"y": 0x00c9, },
    }, {
        "name": "Tooth of Vlad",
        "ability": RELIC["TOOTH_OF_VLAD"],
        "relicId": 26,
        "entity": {"zones": [ZONE["RNO1"]], "entities": [0x2332, 0x2a1e], },
        "reward": {"zone": [ZONE["RBO4"]], "index": 0x12, },
        "erase": {
            "instructions": [
                {"addresses": [0x067ec398], "instruction": 0x34020000, }
            ]
        },
        "replaceWithItem": {"boss": ZONE["RBO4"], "entry": 0x029fc0, "inj": 0x037500, },
        "asItem": {"y": 0x00b9, },
    }, {
        "name": "Rib of Vlad",
        "ability": RELIC["RIB_OF_VLAD"],
        "relicId": 27,
        "entity": {"zones": [ZONE["RNO2"]], "entities": [0x29d4, 0x31b8], },
        "reward": {"zone": [ZONE["RBO7"]], "index": 0x13, },
        "erase": {
            "instructions": [
                {"addresses": [0x069e8524], "instruction": 0x34020000, },
            ]
        },
        "replaceWithItem": {"boss": ZONE["RBO7"], "entry": 0x037014, "inj": 0x04bf00, },
        "asItem": {"y": 0x01b9, },
    }, {
        "name": "Ring of Vlad",
        "ability": RELIC["RING_OF_VLAD"],
        "relicId": 28,
        "entity": {"zones": [ZONE["RNZ1"]], "entities": [0x2dce, 0x3640], "erase": False},
        "ids": {"zone": [ZONE["RNZ1"]], "addresses": [0x059e8074, 0x059ee2e4, 0x059bdb30], },
        "erase": {
            "instructions": [
                {"addresses": [0x059ee594], "instruction": 0x34020000, },
                {"addresses": [0x059ee2d0], "instruction": 0x34020000, },
                {"addresses": [0x059ee2d4], "instruction": 0x00000000, }
            ]
        },
        "replaceWithItem": "replaceRingOfVladWithItem",
        "asItem": {"y": 0x00c9},
    }, {
        "name": "Eye of Vlad",
        "ability": RELIC["EYE_OF_VLAD"],
        "relicId": 29,
        "entity": {"zones": [ZONE["RCHI"]], "entities": [0x18f2, 0x1d52]},
        "reward": {"zone": [ZONE["RBO2"]], "index": 0x15},
        "erase": {
            "instructions": [
                {"addresses": [0x06644cf0], "instruction": 0x34020000, },
            ]
        },
        "replaceWithItem": {"boss": ZONE["RBO2"], "entry": 0x01af18, "inj": 0x02a000, },
        "asItem": {"y": 0x0079},
    }, {
        "name": "Spike Breaker",
        "ability": RELIC["SPIKE_BREAKER"],
        "itemId": 183,
        "tileIndex": 0,
        "asRelic": {"y": 0x0094, },
    }, {
        "name": "Gold ring",
        "ability": RELIC["GOLD_RING"],
        "itemId": 241,
        "entity": {"zones": [ZONE["NO4"]], "entities": [0x4270, 0x52ee], },
        "ids": {"zone": [ZONE["NO4"]], "addresses": [0x04c324b4], "tileId": "True", },
        "replaceWithRelic": "replaceGoldRingWithRelic",
    }, {
        "name": "Silver ring",
        "ability": RELIC["SILVER_RING"],
        "itemId": 242,
        "tileIndex": 0,
        "asRelic": {"y": 0x009a, },
    }, {
        "name": "Holy glasses",
        "ability": RELIC["HOLY_GLASSES"],
        "itemId": 203,
        "ids": {"zone": [ZONE["CEN"]], "addresses": [0x0456e368], },
        "erase": {
            "instructions": [
                {"addresses": [0x0456e360], "instruction": 0x08063ff6, },
            ]
        },
        "replaceWithRelic": "replaceHolyGlassesWithRelic",
    }, {
        "name": "Thrust sword",
        "ability": RELIC["THRUST_SWORD"],
        "consumesItem": False,
    }
]
