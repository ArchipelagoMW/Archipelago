import constants

location_list = [
    {
        "name": constants.LOCATION["CRYSTAL_CLOAK"],
        "extension": constants.EXTENSION["GUARDED"],
        "itemId": 221,
        "tileIndex": 0,
        "asRelic": {"y": 0x00a0,}
    }, {
        "name": constants.LOCATION["MORMEGIL"],
        "extension": constants.EXTENSION["GUARDED"],
        "itemId": 110,
        "tileIndex": 0,
        "asRelic": {"y": 0x0098,}
    }, {
        "name": constants.LOCATION["DARK_BLADE"],
        "extension": constants.EXTENSION["GUARDED"],
        "itemId": 118,
        "tileIndex": 0,
        "asRelic": {"y": 0x0080,}
    }, {
        "name": constants.LOCATION["RING_OF_ARCANA"],
        "extension": constants.EXTENSION["GUARDED"],
        "itemId": 244,
        "tileIndex": 0,
        "x": 0x0082,
        "asRelic": {"y": 0x0080,}
    }, {
        "name": constants.LOCATION["HOLY_MAIL"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 187,
        "tileIndex": 0,
        "asRelic": {"y": 0x0050,}
    }, {
        "name": constants.LOCATION["TRIO"],
        "extension": constants.EXTENSION["GUARDED"],
        "entity": {
            "zones": [constants.ZONE["RARE"]],
            "entities": [0x23ba, 0x293c, ],
        },
        "reward": {"zone": constants.ZONE["RBO0"], "index": 0x02,},
        "erase": {"instructions": [{"addresses": [0x06487bd4], "instruction": 0x34020000,}]},
        "replaceWithItem": {"boss": [constants.ZONE["RBO0"]], "entry": 0x026e64, "inj": 0x038a00,},
        "asItem": {"y": 0x00d9},
    }, {
        "name": constants.LOCATION["JEWEL_SWORD"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 146,  # Actually life apple because it's on the pedestal.
        "tileIndex": 0,
        "asRelic": {"y": 0x0090,}
    }, {
        "name": constants.LOCATION["BASILARD"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 18,
        "tileIndex": 0,
        "asRelic": {"y": 0x0090,}
    }, {
        "name": constants.LOCATION["SUNGLASSES"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 196,
        "tileIndex": 0,
        "asRelic": {"y": 0x0080,}
    }, {
        "name": constants.LOCATION["CLOTH_CAPE"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 218,
        "tileIndex": 0,
        "asRelic": {"y": 0x0080,}
    }, {
        "name": constants.LOCATION["MYSTIC_PENDANT"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 245,
        "tileIndex": 0,
    }, {
        "name": constants.LOCATION["ANKH_OF_LIFE"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 249,
        "tileIndex": 0,
    }, {
        "name": constants.LOCATION["MORNING_STAR"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 129,
        "tileIndex": 0,
    }, {
        "name": constants.LOCATION["GOGGLES"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 201,
        "tileIndex": 0,
        "asRelic": {"y": 0x0120,}
    }, {
        "name": constants.LOCATION["SILVER_PLATE"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 175,
        "tileIndex": 0,
        "asRelic": {"y": 0x00f0,}
    }, {
        "name": constants.LOCATION["CUTLASS"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 88,
        "tileIndex": 0,
        "asRelic": {"y": 0x00ef,}
    }, {
        "name": constants.LOCATION["PLATINUM_MAIL"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 177,
        "tileIndex": 0,
        "asRelic": {"y": 0x00be,}
    }, {
        "name": constants.LOCATION["FALCHION"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 90,
        "tileIndex": 0,
        "asRelic": {"y": 0x0090,}
    }, {
        "name": constants.LOCATION["GOLD_PLATE"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 176,
        "tileIndex": 0,
        "asRelic": {"y": 0x0090,}
    }, {
        "name": constants.LOCATION["BEKATOWA"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 92,
        "tileIndex": 0,
        "asRelic": {"y": 0x0280,}
    }, {
        "name": constants.LOCATION["GLADIUS"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 86,
        "tileIndex": 0,
        "asRelic": {"y": 0x00b0,}
    }, {
        "name": constants.LOCATION["JEWEL_KNUCKLES"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 97,
        "tileIndex": 0,
        "asRelic": {"y": 0x0090,}
    }, {
        "name": constants.LOCATION["HOLY_ROD"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 130,
        "tileIndex": 0,
        "asRelic": {"y": 0x00b0,}
    }, {
        "name": constants.LOCATION["LIBRARY_ONYX"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 235,
        "tileIndex": 0,
    }, {
        "name": constants.LOCATION["BRONZE_CUIRASS"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 172,
        "tileIndex": 0,
        "asRelic": {"y": 0x01b0,}
    }, {
        "name": constants.LOCATION["ALUCART_SWORD"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 168,
        "tileIndex": 0,
        "asRelic": {"y": 0x00b0,}
    }, {
        "name": constants.LOCATION["BROADSWORD"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 91,
        "tileIndex": 0,
    }, {
        "name": constants.LOCATION["ESTOC"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 95,
        "tileIndex": 0,
    }, {
        "name": constants.LOCATION["OLROX_GARNET"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 236,
        "tileIndex": 1,
        "asRelic": {"y": 0x0090,}
    }, {
        "name": constants.LOCATION["BLOOD_CLOAK"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 223,
        "tileIndex": 0,
        "asRelic": {"y": 0x00b0,}
    }, {
        "name": constants.LOCATION["SHIELD_ROD"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 4,
        "tileIndex": 0,
        "asRelic": {"y": 0x0078,}
    }, {
        "name": constants.LOCATION["KNIGHT_SHIELD"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 6,
        "tileIndex": 0,
        "asRelic": {"y": 0x00b0,}
    }, {
        "name": constants.LOCATION["BANDANNA"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 198,
        "tileIndex": 0,
        "asRelic": {"y": 0x00a0,}
    }, {
        "name": constants.LOCATION["NUNCHAKU"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 21,
        "tileIndex": 0,
        "asRelic": {"y": 0x00f2,}
    }, {
        "name": constants.LOCATION["KNUCKLE_DUSTER"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 85,
        "tileIndex": 0,
        "asRelic": {"y": 0x00f5,}
    }, {
        "name": constants.LOCATION["CAVERNS_ONYX"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 235,
        "tileIndex": 1,
        "x": 0x053f,
        "asRelic": {"y": 0x0052,}
    }, {
        "name": constants.LOCATION["SECRET_BOOTS"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 257,
        "tileIndex": 0,
        "asRelic": {"y": 0x021f,}
    }, {
        "name": constants.LOCATION["COMBAT_KNIFE"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 20,
        "tileIndex": 0,
        "asRelic": {"y": 0x005f,}
    }, {
        "name": constants.LOCATION["RING_OF_ARES"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 240,
        "tileIndex": 0,
        "asRelic": {"y": 0x0190,}
    }, {
        "name": constants.LOCATION["BLOODSTONE"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 229,
        "tileIndex": 0,
        "asRelic": {"y": 0x0090,}
    }, {
        "name": constants.LOCATION["ICEBRAND"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 113,
        "tileIndex": 0,
        "asRelic": {"y": 0x0098,}
    }, {
        "name": constants.LOCATION["WALK_ARMOR"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 188,
        "tileIndex": 0,
        "asRelic": {"y": 0x00b0,}
    }, {
        "name": constants.LOCATION["BERYL_CIRCLET"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 211,
        "tileIndex": 0,
        "asRelic": {"y": 0x0090,}
    }, {
        "name": constants.LOCATION["TALISMAN"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 252,
        "tileIndex": 0,
        "asRelic": {"y": 0x0080,}
    }, {
        "name": constants.LOCATION["KATANA"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 100,
        "tileIndex": 0,
        "x": 0x0080,
        "asRelic": {"y": 0x0070,}
    }, {
        "name": constants.LOCATION["GODDESS_SHIELD"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 11,
        "tileIndex": 0,
        "x": 0x0080,
        "asRelic": {"y": 0x0080,}
    }, {
        "name": constants.LOCATION["TWILIGHT_CLOAK"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 225,
        "tileIndex": 0,
        "asRelic": {"y": 0x0080,}
    }, {
        "name": constants.LOCATION["TALWAR"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 99,
        "tileIndex": 0,
    }, {
        "name": constants.LOCATION["SWORD_OF_DAWN"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 236,  # Actually the garnet because sword is in breakable wall.
        "tileIndex": 2,
        "asRelic": {"y": 0x0110,}
    }, {
        "name": constants.LOCATION["BASTARD_SWORD"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 96,
        "tileIndex": 0,
        "asRelic": {"y": 0x0080,}
    }, {
        "name": constants.LOCATION["ROYAL_CLOAK"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 222,
        "tileIndex": 0,
        "asRelic": {"y": 0x0080,}
    }, {
        "name": constants.LOCATION["LIGHTNING_MAIL"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 180,
        "tileIndex": 0,
        "asRelic": {"y": 0x0080,}
    }, {
        "name": constants.LOCATION["MOON_ROD"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 132,
        "tileIndex": 0,
        "asRelic": {"y": 0x0080,}
    }, {
        "name": constants.LOCATION["SUNSTONE"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 228,
        "tileIndex": 0,
        "asRelic": {"y": 0x0080,}
    }, {
        "name": constants.LOCATION["LUMINUS"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 105,
        "tileIndex": 0,
    }, {
        "name": constants.LOCATION["DRAGON_HELM"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 214,
        "tileIndex": 0,
        "asRelic": {"y": 0x0060,}
    }, {
        "name": constants.LOCATION["SHOTEL"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 147,  # Actually the hammer.
        "tileIndex": 2,
        "asRelic": {"y": 0x00b0,}
    }, {
        "name": constants.LOCATION["STAUROLITE"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 230,
        "tileIndex": 0,
        "asRelic": {"y": 0x00b0,}
    }, {
        "name": constants.LOCATION["BADELAIRE"],
        "extension": constants.EXTENSION["SPREAD"],
        "itemId": 125,
        "tileIndex": 0,
        "asRelic": {"y": 0x00c0,}
    }, {
        "name": constants.LOCATION["FORBIDDEN_LIBRARY_OPAL"],
        "extension": constants.EXTENSION["SPREAD"],
        "itemId": 237,
        "tileIndex": 0,
        "asRelic": {"y": 0x0080,}
    }, {
        "name": constants.LOCATION["REVERSE_CAVERNS_DIAMOND"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 238,
        "tileIndex": 1,
        "x": 0x0080,
        "asRelic": {"y": 0x0080,}
    }, {
        "name": constants.LOCATION["REVERSE_CAVERNS_OPAL"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 237,
        "tileIndex": 1,
        "asRelic": {"y": 0x0090,}
    }, {
        "name": constants.LOCATION["REVERSE_CAVERNS_GARNET"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 236,
        "tileIndex": 4,
        "asRelic": {"y": 0x0080,}
    }, {
        "name": constants.LOCATION["OSAFUNE_KATANA"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 139,
        "tileIndex": 0,
        "x": 0x0080,
        "asRelic": {"y": 0x0080,}
    }, {
        "name": constants.LOCATION["ALUCARD_SHIELD"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 16,
        "tileIndex": 0,
        "x": 0x0080,
        "asRelic": {"y": 0x0080,}
    }, {
        "name": constants.LOCATION["ALUCARD_SWORD"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 123,
        "tileIndex": 0,
        "asRelic": {"y": 0x0080,}
    }, {
        "name": constants.LOCATION["NECKLACE_OF_J"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 247,
        "tileIndex": 0,
        "asRelic": {"y": 0x0080,}
    }, {
        "name": constants.LOCATION["FLOATING_CATACOMBS_DIAMOND"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 238,
        "tileIndex": 2,
        "asRelic": {"y": 0x0080,}
    }, {
        "name": constants.LOCATION["SWORD_OF_HADOR"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 237,  # Actually the Opal.
        "tileIndex": 3,
        "asRelic": {"y": 0x0080,}
    }, {
        "name": constants.LOCATION["ALUCARD_MAIL"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 184,
        "tileIndex": 0,
        "asRelic": {"y": 0x0080,}
    }, {
        "name": constants.LOCATION["GRAM"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 108,
        "tileIndex": 0,
        "asRelic": {"y": 0x00b0,}
    }, {
        "name": constants.LOCATION["FURY_PLATE"],
        "extension": constants.EXTENSION["EQUIPMENT"],
        "itemId": 191,
        "tileIndex": 0,
        "asRelic": {"y": 0x0080,}
    }, {
        "name": constants.LOCATION["CONFESSIONAL"],
        "extension": constants.EXTENSION["TOURIST"],
        "entity": {"zones": [constants.ZONE["DAI"]], "entities": [0x27f2, 0x3184, ],},
    }, {
        "name": constants.LOCATION["TELESCOPE"],
        "extension": constants.EXTENSION["TOURIST"],
        "entity": {"zones": [constants.ZONE["NO1"]], "entities": [0x3904, 0x4108, ],},
    }, {
        "name": constants.LOCATION["COLOSSEUM_GREEN_TEA"],
        "extension": constants.EXTENSION["TOURIST"],
        "itemId": 58,
        "tileIndex": 0,
        "asRelic": {"y": 0x00a9,}
    }, {
        "name": constants.LOCATION["CLOCK_TOWER_CLOAKED_KNIGHT"],
        "extension": constants.EXTENSION["TOURIST"],
        "entity": {"zones": [constants.ZONE["NZ1"]], "entities": [0x2444, 0x2e50, ],}
    }, {
        "name": constants.LOCATION["WATERFALL_CAVE"],
        "extension": constants.EXTENSION["TOURIST"],
        "entity": {"zones": [constants.ZONE["NO4"]], "entities": [0x3f6e, 0x5000, ],}
    }, {
        "name": constants.LOCATION["FLOATING_CATACOMBS_ELIXIR"],
        "extension": constants.EXTENSION["TOURIST"],
        "itemId": 161,
        "tileIndex": 2,
        "asRelic": {"y": 0x0077,}
    }, {
        "name": constants.LOCATION["REVERSE_ENTRANCE_ANTIVENOM"],
        "extension": constants.EXTENSION["TOURIST"],
        "itemId": 144,
        "tileIndex": 3,
        "asRelic": {"y": 0x0279,}
    }, {
        "name": constants.LOCATION["REVERSE_FORBIDDEN_ROUTE"],
        "extension": constants.EXTENSION["TOURIST"],
        "itemId": 166,
        "tileIndex": 5,
        "asRelic": {"y": 0x02b5,}
    }, {
        "name": constants.LOCATION["CAVE_LIFE_APPLE"],
        "extension": constants.EXTENSION["TOURIST"],
        "itemId": 146,
        "tileIndex": 3,
        "asRelic": {"y": 0x00a0,}
    }, {
        "name": constants.LOCATION["REVERSE_COLOSSEUM_ZIRCON"],
        "extension": constants.EXTENSION["TOURIST"],
        "itemId": 232,
        "tileIndex": 8,
        "asRelic": {"y": 0x00ad,}
    }, {
        "name": constants.LOCATION["BLACK_MARBLE_GALLERY_VAT"],
        "extension": constants.EXTENSION["TOURIST"],
        "entity": {"zones": [constants.ZONE["RNO0"]], "entities": [0x3bea, 0x4c54, ],}
    }, {
        "name": constants.LOCATION["BLACK_MARBLE_MEAL_TICKET"],
        "extension": constants.EXTENSION["TOURIST"],
        "itemId": 70,
        "tileIndex": 4,
        "x": 0x0088,
        "asRelic": {"y": 0x00a5,}
    }, {
        "name": constants.LOCATION["REVERSE_KEEP_HIGH_POTION"],
        "extension": constants.EXTENSION["TOURIST"],
        "itemId": 160,
        "tileIndex": 0,
        "asRelic": {"y": 0x0180,}
    }, {
        "name": constants.LOCATION["CONFESSIONAL"],
        "extension": constants.EXTENSION["WANDERER"],
        "entity": {"zones": [constants.ZONE["DAI"]], "entities": [0x27f2, 0x3184, ],}
    }, {
        "name": constants.LOCATION["TELESCOPE"],
        "extension": constants.EXTENSION["WANDERER"],
        "entity": {"zones": [constants.ZONE["NO1"]], "entities": [0x3904, 0x4108, ],}
    }, {
        "name": constants.LOCATION["COLOSSEUM_GREEN_TEA"],
        "extension": constants.EXTENSION["WANDERER"],
        "itemId": 58,
        "tileIndex": 0,
        "asRelic": {"y": 0x00a9,}
    }, {
        "name": constants.LOCATION["CLOCK_TOWER_CLOAKED_KNIGHT"],
        "extension": constants.EXTENSION["WANDERER"],
        "entity": {"zones": [constants.ZONE["NZ1"]], "entities": [0x2444, 0x2e50, ],}
    }, {
        "name": constants.LOCATION["WATERFALL_CAVE"],
        "extension": constants.EXTENSION["WANDERER"],
        "entity": {"zones": [constants.ZONE["NO4"]], "entities": [0x3f6e, 0x5000, ],}
    }, {
        "name": constants.LOCATION["FLOATING_CATACOMBS_ELIXIR"],
        "extension": constants.EXTENSION["WANDERER"],
        "itemId": 161,
        "tileIndex": 2,
        "asRelic": {"y": 0x0077,}
    }, {
        "name": constants.LOCATION["REVERSE_ENTRANCE_ANTIVENOM"],
        "extension": constants.EXTENSION["WANDERER"],
        "itemId": 144,
        "tileIndex": 3,
        "asRelic": {"y": 0x0279,}
    }, {
        "name": constants.LOCATION["REVERSE_FORBIDDEN_ROUTE"],
        "extension": constants.EXTENSION["WANDERER"],
        "itemId": 166,
        "tileIndex": 5,
        "asRelic": {"y": 0x02b5,}
    }, {
        "name": constants.LOCATION["CAVE_LIFE_APPLE"],
        "extension": constants.EXTENSION["WANDERER"],
        "itemId": 146,
        "tileIndex": 3,
        "asRelic": {"y": 0x00a0,}
    }, {
        "name": constants.LOCATION["REVERSE_COLOSSEUM_ZIRCON"],
        "extension": constants.EXTENSION["WANDERER"],
        "itemId": 232,
        "tileIndex": 8,
        "asRelic": {"y": 0x00ad,}
    }, {
        "name": constants.LOCATION["BLACK_MARBLE_GALLERY_VAT"],
        "extension": constants.EXTENSION["WANDERER"],
        "entity": {"zones": [constants.ZONE["RNO0"]], "entities": [0x3bea, 0x4c54, ],}
    }, {
        "name": constants.LOCATION["BLACK_MARBLE_MEAL_TICKET"],
        "extension": constants.EXTENSION["WANDERER"],
        "itemId": 70,
        "tileIndex": 4,
        "asRelic": {"x": 0x0088, "y": 0x00a5,}
    }, {
        "name": constants.LOCATION["REVERSE_KEEP_HIGH_POTION"],
        "extension": constants.EXTENSION["WANDERER"],
        "itemId": 160,
        "tileIndex": 0,
        "asRelic": {"y": 0x0180,}
    }, {
        "name": constants.LOCATION["BASILARD"],
        "extension": constants.EXTENSION["WANDERER"],
        "itemId": 18,
        "tileIndex": 0,
        "asRelic": {"y": 0x0090,}
    }, {
        "name": constants.LOCATION["GOGGLES"],
        "extension": constants.EXTENSION["WANDERER"],
        "itemId": 201,
        "tileIndex": 0,
        "asRelic": {"y": 0x0120,}
    }, {
        "name": constants.LOCATION["GOLD_PLATE"],
        "extension": constants.EXTENSION["WANDERER"],
        "itemId": 176,
        "tileIndex": 0,
        "asRelic": {"y": 0x0090,}
    }, {
        "name": constants.LOCATION["BEKATOWA"],
        "extension": constants.EXTENSION["WANDERER"],
        "itemId": 92,
        "tileIndex": 0,
        "asRelic": {"y": 0x0280,}
    }, {
        "name": constants.LOCATION["MYSTIC_PENDANT"],
        "extension": constants.EXTENSION["WANDERER"],
        "itemId": 245,
        "tileIndex": 0,
    }, {
        "name": constants.LOCATION["JEWEL_KNUCKLES"],
        "extension": constants.EXTENSION["WANDERER"],
        "itemId": 97,
        "tileIndex": 0,
        "asRelic": {"y": 0x0090,}
    }, {
        "name": constants.LOCATION["ALUCART_SWORD"],
        "extension": constants.EXTENSION["WANDERER"],
        "itemId": 168,
        "tileIndex": 0,
        "asRelic": {"y": 0x00b0,}
    }, {
        "name": constants.LOCATION["NUNCHAKU"],
        "extension": constants.EXTENSION["WANDERER"],
        "itemId": 21,
        "tileIndex": 0,
        "asRelic": {"y": 0x00f2,}
    }, {
        "name": constants.LOCATION["RING_OF_ARES"],
        "extension": constants.EXTENSION["WANDERER"],
        "itemId": 240,
        "tileIndex": 0,
        "asRelic": {"y": 0x0190,}
    }, {
        "name": constants.LOCATION["BERYL_CIRCLET"],
        "extension": constants.EXTENSION["WANDERER"],
        "itemId": 211,
        "tileIndex": 0,
        "asRelic": {"y": 0x0090,}
    }, {
        "name": constants.LOCATION["KATANA"],
        "extension": constants.EXTENSION["WANDERER"],
        "itemId": 100,
        "tileIndex": 0,
        "asRelic": {"x": 0x0080, "y": 0x0070,}
    }, {
        "name": constants.LOCATION["TWILIGHT_CLOAK"],
        "extension": constants.EXTENSION["WANDERER"],
        "itemId": 225,
        "tileIndex": 0,
        "asRelic": {"y": 0x0080,}
    }, {
        "name": constants.LOCATION["PLATINUM_MAIL"],
        "extension": constants.EXTENSION["WANDERER"],
        "itemId": 177,
        "tileIndex": 0,
        "asRelic": {"y": 0x00be,}
    }, {
        "name": constants.LOCATION["MOON_ROD"],
        "extension": constants.EXTENSION["WANDERER"],
        "itemId": 132,
        "tileIndex": 0,
        "asRelic": {"y": 0x0080,}
    }, {
        "name": constants.LOCATION["LUMINUS"],
        "extension": constants.EXTENSION["WANDERER"],
        "itemId": 105,
        "tileIndex": 0,
    }, {
        "name": constants.LOCATION["REVERSE_CAVERNS_OPAL"],
        "extension": constants.EXTENSION["WANDERER"],
        "itemId": 237,
        "tileIndex": 1,
        "asRelic": {"y": 0x0090,}
    }, {
        "name": constants.LOCATION["OSAFUNE_KATANA"],
        "extension": constants.EXTENSION["WANDERER"],
        "itemId": 139,
        "tileIndex": 0,
        "x": 0x0080,
        "asRelic": {"y": 0x0080,}
    }, {
        "name": constants.LOCATION["GRAM"],
        "extension": constants.EXTENSION["WANDERER"],
        "itemId": 108,
        "tileIndex": 0,
        "asRelic": {"y": 0x00b0,}
    }
]