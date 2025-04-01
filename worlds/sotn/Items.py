from BaseClasses import ItemClassification, Item

tile_id_offset = 0X80


class SotnItem(Item):
    game: str = "Symphony of the Night"


# Thanks M. for useful items
items = {
    "Monster vial 1":
        {
            "id": 1,
            "type": "USABLE",
            "address": 0x09798b,
            "classification": ItemClassification.filler
        },
    "Monster vial 2":
        {
            "id": 2,
            "type": "USABLE",
            "address": 0x09798c,
            "classification": ItemClassification.filler
        },
    "Monster vial 3":
        {
            "id": 3,
            "type": "USABLE",
            "address": 0x09798d,
            "classification": ItemClassification.filler
        },
    "Shield rod":
        {
            "id": 4,
            "type": "WEAPON1",
            "address": 0x09798e,
            "classification": ItemClassification.useful
        },
    "Leather shield":
        {
            "id": 5,
            "type": "SHIELD",
            "address": 0x09798f,
            "classification": ItemClassification.useful
        },
    "Knight shield":
        {
            "id": 6,
            "type": "SHIELD",
            "address": 0x097990,
            "classification": ItemClassification.useful
        },
    "Iron shield":
        {
            "id": 7,
            "type": "SHIELD",
            "address": 0x097991,
            "classification": ItemClassification.useful
        },
    "AxeLord shield":
        {
            "id": 8,
            "type": "SHIELD",
            "address": 0x097992,
            "classification": ItemClassification.useful
        },
    "Herald shield":
        {
            "id": 9,
            "type": "SHIELD",
            "address": 0x097993,
            "classification": ItemClassification.useful
        },
    "Dark shield":
        {
            "id": 10,
            "type": "SHIELD",
            "address": 0x097994,
            "classification": ItemClassification.useful
        },
    "Goddess shield":
        {
            "id": 11,
            "type": "SHIELD",
            "address": 0x097995,
            "classification": ItemClassification.useful
        },
    "Shaman shield":
        {
            "id": 12,
            "type": "SHIELD",
            "address": 0x097996,
            "classification": ItemClassification.useful
        },
    "Medusa shield":
        {
            "id": 13,
            "type": "SHIELD",
            "address": 0x097997,
            "classification": ItemClassification.useful
        },
    "Skull shield":
        {
            "id": 14,
            "type": "SHIELD",
            "address": 0x097998,
            "classification": ItemClassification.useful
        },
    "Fire shield":
        {
            "id": 15,
            "type": "SHIELD",
            "address": 0x097999,
            "classification": ItemClassification.useful
        },
    "Alucard shield":
        {
            "id": 16,
            "type": "SHIELD",
            "address": 0x09799a,
            "classification": ItemClassification.useful
        },
    "Sword of dawn":
        {
            "id": 17,
            "type": "WEAPON2",
            "address": 0x09799b,
            "classification": ItemClassification.useful
        },
    "Basilard":
        {
            "id": 18,
            "type": "WEAPON1",
            "address": 0x09799c,
            "classification": ItemClassification.useful
        },
    "Short sword":
        {
            "id": 19,
            "type": "WEAPON1",
            "address": 0x09799d,
            "classification": ItemClassification.useful
        },
    "Combat knife":
        {
            "id": 20,
            "type": "WEAPON1",
            "address": 0x09799e,
            "classification": ItemClassification.useful
        },
    "Nunchaku":
        {
            "id": 21,
            "type": "WEAPON2",
            "address": 0x09799f,
            "classification": ItemClassification.useful
        },
    "Were bane":
        {
            "id": 22,
            "type": "WEAPON1",
            "address": 0x0979a0,
            "classification": ItemClassification.useful
        },
    "Rapier":
        {
            "id": 23,
            "type": "WEAPON1",
            "address": 0x0979a1,
            "classification": ItemClassification.useful
        },
    "Karma coin":
        {
            "id": 24,
            "type": "USABLE",
            "address": 0x0979a2,
            "classification": ItemClassification.filler
        },
    "Magic missile":
        {
            "id": 25,
            "type": "USABLE",
            "address": 0x0979a3,
            "classification": ItemClassification.filler
        },
    "Red rust":
        {
            "id": 26,
            "type": "WEAPON2",
            "address": 0x0979a4,
            "classification": ItemClassification.filler
        },
    "Takemitsu":
        {
            "id": 27,
            "type": "WEAPON2",
            "address": 0x0979a5,
            "classification": ItemClassification.useful
        },
    "Shotel":
        {
            "id": 28,
            "type": "WEAPON1",
            "address": 0x0979a6,
            "classification": ItemClassification.useful
        },
    "Orange":
        {
            "id": 29,
            "type": "USABLE",
            "address": 0x0979a7,
            "classification": ItemClassification.filler
        },
    "Apple":
        {
            "id": 30,
            "type": "USABLE",
            "address": 0x0979a8,
            "classification": ItemClassification.filler
        },
    "Banana":
        {
            "id": 31,
            "type": "USABLE",
            "address": 0x0979a9,
            "classification": ItemClassification.filler
        },
    "Grapes":
        {
            "id": 32,
            "type": "USABLE",
            "address": 0x0979aa,
            "classification": ItemClassification.filler
        },
    "Strawberry":
        {
            "id": 33,
            "type": "USABLE",
            "address": 0x0979ab,
            "classification": ItemClassification.filler
        },
    "Pineapple":
        {
            "id": 34,
            "type": "USABLE",
            "address": 0x0979ac,
            "classification": ItemClassification.filler
        },
    "Peanuts":
        {
            "id": 35,
            "type": "USABLE",
            "address": 0x0979ad,
            "classification": ItemClassification.filler
        },
    "Toadstool":
        {
            "id": 36,
            "type": "USABLE",
            "address": 0x0979ae,
            "classification": ItemClassification.filler
        },
    "Shiitake":
        {
            "id": 37,
            "type": "USABLE",
            "address": 0x0979af,
            "classification": ItemClassification.filler
        },
    "Cheesecake":
        {
            "id": 38,
            "type": "USABLE",
            "address": 0x0979b0,
            "classification": ItemClassification.filler
        },
    "Shortcake":
        {
            "id": 39,
            "type": "USABLE",
            "address": 0x0979b1,
            "classification": ItemClassification.filler
        },
    "Tart":
        {
            "id": 40,
            "type": "USABLE",
            "address": 0x0979b2,
            "classification": ItemClassification.filler
        },
    "Parfait":
        {
            "id": 41,
            "type": "USABLE",
            "address": 0x0979b3,
            "classification": ItemClassification.filler
        },
    "Pudding":
        {
            "id": 42,
            "type": "USABLE",
            "address": 0x0979b4,
            "classification": ItemClassification.filler
        },
    "Ice cream":
        {
            "id": 43,
            "type": "USABLE",
            "address": 0x0979b5,
            "classification": ItemClassification.filler
        },
    "Frankfurter":
        {
            "id": 44,
            "type": "USABLE",
            "address": 0x0979b6,
            "classification": ItemClassification.filler
        },
    "Hamburger":
        {
            "id": 45,
            "type": "USABLE",
            "address": 0x0979b7,
            "classification": ItemClassification.filler
        },
    "Pizza":
        {
            "id": 46,
            "type": "USABLE",
            "address": 0x0979b8,
            "classification": ItemClassification.filler
        },
    "Cheese":
        {
            "id": 47,
            "type": "USABLE",
            "address": 0x0979b9,
            "classification": ItemClassification.filler
        },
    "Ham and eggs":
        {
            "id": 48,
            "type": "USABLE",
            "address": 0x0979ba,
            "classification": ItemClassification.filler
        },
    "Omelette":
        {
            "id": 49,
            "type": "USABLE",
            "address": 0x0979bb,
            "classification": ItemClassification.filler
        },
    "Morning set":
        {
            "id": 50,
            "type": "USABLE",
            "address": 0x0979bc,
            "classification": ItemClassification.filler
        },
    "Lunch A":
        {
            "id": 51,
            "type": "USABLE",
            "address": 0x0979bd,
            "classification": ItemClassification.filler
        },
    "Lunch B":
        {
            "id": 52,
            "type": "USABLE",
            "address": 0x0979be,
            "classification": ItemClassification.filler
        },
    "Curry rice":
        {
            "id": 53,
            "type": "USABLE",
            "address": 0x0979bf,
            "classification": ItemClassification.filler
        },
    "Gyros plate":
        {
            "id": 54,
            "type": "USABLE",
            "address": 0x0979c0,
            "classification": ItemClassification.filler
        },
    "Spaghetti":
        {
            "id": 55,
            "type": "USABLE",
            "address": 0x0979c1,
            "classification": ItemClassification.filler
        },
    "Grape juice":
        {
            "id": 56,
            "type": "USABLE",
            "address": 0x0979c2,
            "classification": ItemClassification.filler
        },
    "Barley tea":
        {
            "id": 57,
            "type": "USABLE",
            "address": 0x0979c3,
            "classification": ItemClassification.filler
        },
    "Green tea":
        {
            "id": 58,
            "type": "USABLE",
            "address": 0x0979c4,
            "classification": ItemClassification.filler
        },
    "Natou":
        {
            "id": 59,
            "type": "USABLE",
            "address": 0x0979c5,
            "classification": ItemClassification.filler
        },
    "Ramen":
        {
            "id": 60,
            "type": "USABLE",
            "address": 0x0979c6,
            "classification": ItemClassification.filler
        },
    "Miso soup":
        {
            "id": 61,
            "type": "USABLE",
            "address": 0x0979c7,
            "classification": ItemClassification.filler
        },
    "Sushi":
        {
            "id": 62,
            "type": "USABLE",
            "address": 0x0979c8,
            "classification": ItemClassification.filler
        },
    "Pork bun":
        {
            "id": 63,
            "type": "USABLE",
            "address": 0x0979c9,
            "classification": ItemClassification.filler
        },
    "Red bean bun":
        {
            "id": 64,
            "type": "USABLE",
            "address": 0x0979ca,
            "classification": ItemClassification.filler
        },
    "Chinese bun":
        {
            "id": 65,
            "type": "USABLE",
            "address": 0x0979cb,
            "classification": ItemClassification.filler
        },
    "Dim sum set":
        {
            "id": 66,
            "type": "USABLE",
            "address": 0x0979cc,
            "classification": ItemClassification.filler
        },
    "Pot roast":
        {
            "id": 67,
            "type": "USABLE",
            "address": 0x0979cd,
            "classification": ItemClassification.filler
        },
    "Sirloin":
        {
            "id": 68,
            "type": "USABLE",
            "address": 0x0979ce,
            "classification": ItemClassification.filler
        },
    "Turkey":
        {
            "id": 69,
            "type": "USABLE",
            "address": 0x0979cf,
            "classification": ItemClassification.filler
        },
    "Meal ticket":
        {
            "id": 70,
            "type": "USABLE",
            "address": 0x0979d0,
            "classification": ItemClassification.filler
        },
    "Neutron bomb":
        {
            "id": 71,
            "type": "USABLE",
            "address": 0x0979d1,
            "classification": ItemClassification.filler
        },
    "Power of sire":
        {
            "id": 72,
            "type": "USABLE",
            "address": 0x0979d2,
            "classification": ItemClassification.filler
        },
    "Pentagram":
        {
            "id": 73,
            "type": "USABLE",
            "address": 0x0979d3,
            "classification": ItemClassification.filler
        },
    "Bat pentagram":
        {
            "id": 74,
            "type": "USABLE",
            "address": 0x0979d4,
            "classification": ItemClassification.filler
        },
    "Shuriken":
        {
            "id": 75,
            "type": "USABLE",
            "address": 0x0979d5,
            "classification": ItemClassification.filler
        },
    "Cross shuriken":
        {
            "id": 76,
            "type": "USABLE",
            "address": 0x0979d6,
            "classification": ItemClassification.filler
        },
    "Buffalo star":
        {
            "id": 77,
            "type": "USABLE",
            "address": 0x0979d7,
            "classification": ItemClassification.filler
        },
    "Flame star":
        {
            "id": 78,
            "type": "USABLE",
            "address": 0x0979d8,
            "classification": ItemClassification.filler
        },
    "TNT":
        {
            "id": 79,
            "type": "USABLE",
            "address": 0x0979d9,
            "classification": ItemClassification.filler
        },
    "Bwaka knife":
        {
            "id": 80,
            "type": "USABLE",
            "address": 0x0979da,
            "classification": ItemClassification.filler
        },
    "Boomerang":
        {
            "id": 81,
            "type": "USABLE",
            "address": 0x0979db,
            "classification": ItemClassification.filler
        },
    "Javelin":
        {
            "id": 82,
            "type": "USABLE",
            "address": 0x0979dc,
            "classification": ItemClassification.filler
        },
    "Tyrfing":
        {
            "id": 83,
            "type": "WEAPON1",
            "address": 0x0979dd,
            "classification": ItemClassification.useful
        },
    "Namakura":
        {
            "id": 84,
            "type": "WEAPON2",
            "address": 0x0979de,
            "classification": ItemClassification.useful
        },
    "Knuckle duster":
        {
            "id": 85,
            "type": "WEAPON1",
            "address": 0x0979df,
            "classification": ItemClassification.useful
        },
    "Gladius":
        {
            "id": 86,
            "type": "WEAPON1",
            "address": 0x0979e0,
            "classification": ItemClassification.useful
        },
    "Scimitar":
        {
            "id": 87,
            "type": "WEAPON1",
            "address": 0x0979e1,
            "classification": ItemClassification.useful
        },
    "Cutlass":
        {
            "id": 88,
            "type": "WEAPON1",
            "address": 0x0979e2,
            "classification": ItemClassification.useful
        },
    "Saber":
        {
            "id": 89,
            "type": "WEAPON1",
            "address": 0x0979e3,
            "classification": ItemClassification.useful
        },
    "Falchion":
        {
            "id": 90,
            "type": "WEAPON1",
            "address": 0x0979e4,
            "classification": ItemClassification.useful
        },
    "Broadsword":
        {
            "id": 91,
            "type": "WEAPON1",
            "address": 0x0979e5,
            "classification": ItemClassification.useful
        },
    "Bekatowa":
        {
            "id": 92,
            "type": "WEAPON1",
            "address": 0x0979e6,
            "classification": ItemClassification.useful
        },
    "Damascus sword":
        {
            "id": 93,
            "type": "WEAPON1",
            "address": 0x0979e7,
            "classification": ItemClassification.useful
        },
    "Hunter sword":
        {
            "id": 94,
            "type": "WEAPON1",
            "address": 0x0979e8,
            "classification": ItemClassification.useful
        },
    "Estoc":
        {
            "id": 95,
            "type": "WEAPON2",
            "address": 0x0979e9,
            "classification": ItemClassification.useful
        },
    "Bastard sword":
        {
            "id": 96,
            "type": "WEAPON1",
            "address": 0x0979ea,
            "classification": ItemClassification.useful
        },
    "Jewel knuckles":
        {
            "id": 97,
            "type": "WEAPON1",
            "address": 0x0979eb,
            "classification": ItemClassification.useful
        },
    "Claymore":
        {
            "id": 98,
            "type": "WEAPON2",
            "address": 0x0979ec,
            "classification": ItemClassification.useful
        },
    "Talwar":
        {
            "id": 99,
            "type": "WEAPON1",
            "address": 0x0979ed,
            "classification": ItemClassification.useful
        },
    "Katana":
        {
            "id": 100,
            "type": "WEAPON2",
            "address": 0x0979ee,
            "classification": ItemClassification.useful
        },
    "Flamberge":
        {
            "id": 101,
            "type": "WEAPON2",
            "address": 0x0979ef,
            "classification": ItemClassification.useful
        },
    "Iron fist":
        {
            "id": 102,
            "type": "WEAPON1",
            "address": 0x0979f0,
            "classification": ItemClassification.useful
        },
    "Zwei hander":
        {
            "id": 103,
            "type": "WEAPON2",
            "address": 0x0979f1,
            "classification": ItemClassification.useful
        },
    "Sword of hador":
        {
            "id": 104,
            "type": "WEAPON1",
            "address": 0x0979f2,
            "classification": ItemClassification.useful
        },
    "Luminus":
        {
            "id": 105,
            "type": "WEAPON1",
            "address": 0x0979f3,
            "classification": ItemClassification.useful
        },
    "Harper":
        {
            "id": 106,
            "type": "WEAPON1",
            "address": 0x0979f4,
            "classification": ItemClassification.useful
        },
    "Obsidian sword":
        {
            "id": 107,
            "type": "WEAPON2",
            "address": 0x0979f5,
            "classification": ItemClassification.useful
        },
    "Gram":
        {
            "id": 108,
            "type": "WEAPON1",
            "address": 0x0979f6,
            "classification": ItemClassification.useful
        },
    "Jewel sword":
        {
            "id": 109,
            "type": "WEAPON1",
            "address": 0x0979f7,
            "classification": ItemClassification.useful
        },
    "Mormegil":
        {
            "id": 110,
            "type": "WEAPON1",
            "address": 0x0979f8,
            "classification": ItemClassification.useful
        },
    "Firebrand":
        {
            "id": 111,
            "type": "WEAPON1",
            "address": 0x0979f9,
            "classification": ItemClassification.useful
        },
    "Thunderbrand":
        {
            "id": 112,
            "type": "WEAPON1",
            "address": 0x0979fa,
            "classification": ItemClassification.useful
        },
    "Icebrand":
        {
            "id": 113,
            "type": "WEAPON1",
            "address": 0x0979fb,
            "classification": ItemClassification.useful
        },
    "Stone sword":
        {
            "id": 114,
            "type": "WEAPON1",
            "address": 0x0979fc,
            "classification": ItemClassification.useful
        },
    "Holy sword":
        {
            "id": 115,
            "type": "WEAPON1",
            "address": 0x0979fd,
            "classification": ItemClassification.useful
        },
    "Terminus est":
        {
            "id": 116,
            "type": "WEAPON1",
            "address": 0x0979fe,
            "classification": ItemClassification.useful
        },
    "Marsil":
        {
            "id": 117,
            "type": "WEAPON1",
            "address": 0x0979ff,
            "classification": ItemClassification.useful
        },
    "Dark blade":
        {
            "id": 118,
            "type": "WEAPON1",
            "address": 0x097a00,
            "classification": ItemClassification.useful
        },
    "Heaven sword":
        {
            "id": 119,
            "type": "WEAPON1",
            "address": 0x097a01,
            "classification": ItemClassification.useful
        },
    "Fist of tulkas":
        {
            "id": 120,
            "type": "WEAPON1",
            "address": 0x097a02,
            "classification": ItemClassification.useful
        },
    "Gurthang":
        {
            "id": 121,
            "type": "WEAPON1",
            "address": 0x097a03,
            "classification": ItemClassification.useful
        },
    "Mourneblade":
        {
            "id": 122,
            "type": "WEAPON1",
            "address": 0x097a04,
            "classification": ItemClassification.useful
        },
    "Alucard sword":
        {
            "id": 123,
            "type": "WEAPON1",
            "address": 0x097a05,
            "classification": ItemClassification.useful
        },
    "Mablung sword":
        {
            "id": 124,
            "type": "WEAPON1",
            "address": 0x097a06,
            "classification": ItemClassification.useful
        },
    "Badelaire":
        {
            "id": 125,
            "type": "WEAPON1",
            "address": 0x097a07,
            "classification": ItemClassification.useful
        },
    "Sword familiar":
        {
            "id": 126,
            "type": "WEAPON1",
            "address": 0x097a08,
            "classification": ItemClassification.useful
        },
    "Great sword":
        {
            "id": 127,
            "type": "WEAPON2",
            "address": 0x097a09,
            "classification": ItemClassification.useful
        },
    "Mace":
        {
            "id": 128,
            "type": "WEAPON1",
            "address": 0x097a0a,
            "classification": ItemClassification.useful
        },
    "Morningstar":
        {
            "id": 129,
            "type": "WEAPON1",
            "address": 0x097a0b,
            "classification": ItemClassification.useful
        },
    "Holy rod":
        {
            "id": 130,
            "type": "WEAPON1",
            "address": 0x097a0c,
            "classification": ItemClassification.useful
        },
    "Star flail":
        {
            "id": 131,
            "type": "WEAPON1",
            "address": 0x097a0d,
            "classification": ItemClassification.useful
        },
    "Moon rod":
        {
            "id": 132,
            "type": "WEAPON1",
            "address": 0x097a0e,
            "classification": ItemClassification.useful
        },
    "Chakram":
        {
            "id": 133,
            "type": "WEAPON1",
            "address": 0x097a0f,
            "classification": ItemClassification.useful
        },
    "Fire boomerang":
        {
            "id": 134,
            "type": "USABLE",
            "address": 0x097a10,
            "classification": ItemClassification.filler
        },
    "Iron ball":
        {
            "id": 135,
            "type": "USABLE",
            "address": 0x097a11,
            "classification": ItemClassification.filler
        },
    "Holbein dagger":
        {
            "id": 136,
            "type": "WEAPON1",
            "address": 0x097a12,
            "classification": ItemClassification.useful
        },
    "Blue knuckles":
        {
            "id": 137,
            "type": "WEAPON1",
            "address": 0x097a13,
            "classification": ItemClassification.useful
        },
    "Dynamite":
        {
            "id": 138,
            "type": "USABLE",
            "address": 0x097a14,
            "classification": ItemClassification.filler
        },
    "Osafune katana":
        {
            "id": 139,
            "type": "WEAPON2",
            "address": 0x097a15,
            "classification": ItemClassification.useful
        },
    "Masamune":
        {
            "id": 140,
            "type": "WEAPON2",
            "address": 0x097a16,
            "classification": ItemClassification.useful
        },
    "Muramasa":
        {
            "id": 141,
            "type": "WEAPON2",
            "address": 0x097a17,
            "classification": ItemClassification.useful
        },
    "Heart refresh":
        {
            "id": 142,
            "type": "USABLE",
            "address": 0x097a18,
            "classification": ItemClassification.filler
        },
    "Runesword":
        {
            "id": 143,
            "type": "WEAPON1",
            "address": 0x097a19,
            "classification": ItemClassification.useful
        },
    "Antivenom":
        {
            "id": 144,
            "type": "USABLE",
            "address": 0x097a1a,
            "classification": ItemClassification.filler
        },
    "Uncurse":
        {
            "id": 145,
            "type": "USABLE",
            "address": 0x097a1b,
            "classification": ItemClassification.filler
        },
    "Life apple":
        {
            "id": 146,
            "type": "USABLE",
            "address": 0x097a1c,
            "classification": ItemClassification.filler
        },
    "Hammer":
        {
            "id": 147,
            "type": "USABLE",
            "address": 0x097a1d,
            "classification": ItemClassification.filler
        },
    "Str. potion":
        {
            "id": 148,
            "type": "USABLE",
            "address": 0x097a1e,
            "classification": ItemClassification.filler
        },
    "Luck potion":
        {
            "id": 149,
            "type": "USABLE",
            "address": 0x097a1f,
            "classification": ItemClassification.filler
        },
    "Smart potion":
        {
            "id": 150,
            "type": "USABLE",
            "address": 0x097a20,
            "classification": ItemClassification.filler
        },
    "Attack potion":
        {
            "id": 151,
            "type": "USABLE",
            "address": 0x097a21,
            "classification": ItemClassification.filler
        },
    "Shield potion":
        {
            "id": 152,
            "type": "USABLE",
            "address": 0x097a22,
            "classification": ItemClassification.filler
        },
    "Resist fire":
        {
            "id": 153,
            "type": "USABLE",
            "address": 0x097a23,
            "classification": ItemClassification.filler
        },
    "Resist thunder":
        {
            "id": 154,
            "type": "USABLE",
            "address": 0x097a24,
            "classification": ItemClassification.filler
        },
    "Resist ice":
        {
            "id": 155,
            "type": "USABLE",
            "address": 0x097a25,
            "classification": ItemClassification.filler
        },
    "Resist stone":
        {
            "id": 156,
            "type": "USABLE",
            "address": 0x097a26,
            "classification": ItemClassification.filler
        },
    "Resist holy":
        {
            "id": 157,
            "type": "USABLE",
            "address": 0x097a27,
            "classification": ItemClassification.filler
        },
    "Resist dark":
        {
            "id": 158,
            "type": "USABLE",
            "address": 0x097a28,
            "classification": ItemClassification.filler
        },
    "Potion":
        {
            "id": 159,
            "type": "USABLE",
            "address": 0x097a29,
            "classification": ItemClassification.filler
        },
    "High potion":
        {
            "id": 160,
            "type": "USABLE",
            "address": 0x097a2a,
            "classification": ItemClassification.filler
        },
    "Elixir":
        {
            "id": 161,
            "type": "USABLE",
            "address": 0x097a2b,
            "classification": ItemClassification.filler
        },
    "Manna prism":
        {
            "id": 162,
            "type": "USABLE",
            "address": 0x097a2c,
            "classification": ItemClassification.filler
        },
    "Vorpal blade":
        {
            "id": 163,
            "type": "WEAPON1",
            "address": 0x097a2d,
            "classification": ItemClassification.useful
        },
    "Crissaegrim":
        {
            "id": 164,
            "type": "WEAPON1",
            "address": 0x097a2e,
            "classification": ItemClassification.useful
        },
    "Yasutsuna":
        {
            "id": 165,
            "type": "WEAPON2",
            "address": 0x097a2f,
            "classification": ItemClassification.useful
        },
    "Library card":
        {
            "id": 166,
            "type": "USABLE",
            "address": 0x097a30,
            "classification": ItemClassification.filler
        },
    "Alucart shield":
        {
            "id": 167,
            "type": "SHIELD",
            "address": 0x097a31,
            "classification": ItemClassification.useful
        },
    "Alucart sword":
        {
            "id": 168,
            "type": "WEAPON1",
            "address": 0x097a32,
            "classification": ItemClassification.useful
        },
    "Cloth tunic":
        {
            "id": 170,
            "type": "ARMOR",
            "address": 0x097a34,
            "classification": ItemClassification.useful
        },
    "Hide cuirass":
        {
            "id": 171,
            "type": "ARMOR",
            "address": 0x097a35,
            "classification": ItemClassification.useful
        },
    "Bronze cuirass":
        {
            "id": 172,
            "type": "ARMOR",
            "address": 0x097a36,
            "classification": ItemClassification.useful
        },
    "Iron cuirass":
        {
            "id": 173,
            "type": "ARMOR",
            "address": 0x097a37,
            "classification": ItemClassification.useful
        },
    "Steel cuirass":
        {
            "id": 174,
            "type": "ARMOR",
            "address": 0x097a38,
            "classification": ItemClassification.useful
        },
    "Silver plate":
        {
            "id": 175,
            "type": "ARMOR",
            "address": 0x097a39,
            "classification": ItemClassification.useful
        },
    "Gold plate":
        {
            "id": 176,
            "type": "ARMOR",
            "address": 0x097a3a,
            "classification": ItemClassification.useful
        },
    "Platinum mail":
        {
            "id": 177,
            "type": "ARMOR",
            "address": 0x097a3b,
            "classification": ItemClassification.useful
        },
    "Diamond plate":
        {
            "id": 178,
            "type": "ARMOR",
            "address": 0x097a3c,
            "classification": ItemClassification.useful
        },
    "Fire mail":
        {
            "id": 179,
            "type": "ARMOR",
            "address": 0x097a3d,
            "classification": ItemClassification.useful
        },
    "Lightning mail":
        {
            "id": 180,
            "type": "ARMOR",
            "address": 0x097a3e,
            "classification": ItemClassification.useful
        },
    "Ice mail":
        {
            "id": 181,
            "type": "ARMOR",
            "address": 0x097a3f,
            "classification": ItemClassification.useful
        },
    "Mirror cuirass":
        {
            "id": 182,
            "type": "ARMOR",
            "address": 0x097a40,
            "classification": ItemClassification.useful
        },
    "Spike breaker":
        {
            "id": 183,
            "type": "ARMOR",
            "address": 0x097a41,
            "classification": ItemClassification.progression
        },
    "Alucard mail":
        {
            "id": 184,
            "type": "ARMOR",
            "address": 0x097a42,
            "classification": ItemClassification.useful
        },
    "Dark armor":
        {
            "id": 185,
            "type": "ARMOR",
            "address": 0x097a43,
            "classification": ItemClassification.useful
        },
    "Healing mail":
        {
            "id": 186,
            "type": "ARMOR",
            "address": 0x097a44,
            "classification": ItemClassification.useful
        },
    "Holy mail":
        {
            "id": 187,
            "type": "ARMOR",
            "address": 0x097a45,
            "classification": ItemClassification.useful
        },
    "Walk armor":
        {
            "id": 188,
            "type": "ARMOR",
            "address": 0x097a46,
            "classification": ItemClassification.useful
        },
    "Brilliant mail":
        {
            "id": 189,
            "type": "ARMOR",
            "address": 0x097a47,
            "classification": ItemClassification.useful
        },
    "Mojo mail":
        {
            "id": 190,
            "type": "ARMOR",
            "address": 0x097a48,
            "classification": ItemClassification.useful
        },
    "Fury plate":
        {
            "id": 191,
            "type": "ARMOR",
            "address": 0x097a49,
            "classification": ItemClassification.useful
        },
    "Dracula tunic":
        {
            "id": 192,
            "type": "ARMOR",
            "address": 0x097a4a,
            "classification": ItemClassification.useful
        },
    "God's Garb":
        {
            "id": 193,
            "type": "ARMOR",
            "address": 0x097a4b,
            "classification": ItemClassification.useful
        },
    "Axe Lord armor":
        {
            "id": 194,
            "type": "ARMOR",
            "address": 0x097a4c,
            "classification": ItemClassification.filler
        },
    "Alucart mail":
        {
            "id": 258,
            "type": "ARMOR",
            "address": 0x097a8c,
            "classification": ItemClassification.useful
        },
    "Sunglasses":
        {
            "id": 196,
            "type": "HELMET",
            "address": 0x097a4e,
            "classification": ItemClassification.useful
        },
    "Ballroom mask":
        {
            "id": 197,
            "type": "HELMET",
            "address": 0x097a4f,
            "classification": ItemClassification.useful
        },
    "Bandanna":
        {
            "id": 198,
            "type": "HELMET",
            "address": 0x097a50,
            "classification": ItemClassification.useful
        },
    "Felt hat":
        {
            "id": 199,
            "type": "HELMET",
            "address": 0x097a51,
            "classification": ItemClassification.useful
        },
    "Velvet hat":
        {
            "id": 200,
            "type": "HELMET",
            "address": 0x097a52,
            "classification": ItemClassification.useful
        },
    "Goggles":
        {
            "id": 201,
            "type": "HELMET",
            "address": 0x097a53,
            "classification": ItemClassification.useful
        },
    "Leather hat":
        {
            "id": 202,
            "type": "HELMET",
            "address": 0x097a54,
            "classification": ItemClassification.useful
        },
    "Holy glasses":
        {
            "id": 203,
            "type": "HELMET",
            "address": 0x097a55,
            "classification": ItemClassification.progression
        },
    "Steel helm":
        {
            "id": 204,
            "type": "HELMET",
            "address": 0x097a56,
            "classification": ItemClassification.useful
        },
    "Stone mask":
        {
            "id": 205,
            "type": "HELMET",
            "address": 0x097a57,
            "classification": ItemClassification.useful
        },
    "Circlet":
        {
            "id": 206,
            "type": "HELMET",
            "address": 0x097a58,
            "classification": ItemClassification.useful
        },
    "Gold circlet":
        {
            "id": 207,
            "type": "HELMET",
            "address": 0x097a59,
            "classification": ItemClassification.useful
        },
    "Ruby circlet":
        {
            "id": 208,
            "type": "HELMET",
            "address": 0x097a5a,
            "classification": ItemClassification.useful
        },
    "Opal circlet":
        {
            "id": 209,
            "type": "HELMET",
            "address": 0x097a5b,
            "classification": ItemClassification.useful
        },
    "Topaz circlet":
        {
            "id": 210,
            "type": "HELMET",
            "address": 0x097a5c,
            "classification": ItemClassification.useful
        },
    "Beryl circlet":
        {
            "id": 211,
            "type": "HELMET",
            "address": 0x097a5d,
            "classification": ItemClassification.useful
        },
    "Cat-eye circl.":
        {
            "id": 212,
            "type": "HELMET",
            "address": 0x097a5e,
            "classification": ItemClassification.useful
        },
    "Coral circlet":
        {
            "id": 213,
            "type": "HELMET",
            "address": 0x097a5f,
            "classification": ItemClassification.useful
        },
    "Dragon helm":
        {
            "id": 214,
            "type": "HELMET",
            "address": 0x097a60,
            "classification": ItemClassification.useful
        },
    "Silver crown":
        {
            "id": 215,
            "type": "HELMET",
            "address": 0x097a61,
            "classification": ItemClassification.useful
        },
    "Wizard hat":
        {
            "id": 216,
            "type": "HELMET",
            "address": 0x097a62,
            "classification": ItemClassification.useful
        },
    "Cloth cape":
        {
            "id": 218,
            "type": "CLOAK",
            "address": 0x097a64,
            "classification": ItemClassification.useful
        },
    "Reverse cloak":
        {
            "id": 219,
            "type": "CLOAK",
            "address": 0x097a65,
            "classification": ItemClassification.useful
        },
    "Elven cloak":
        {
            "id": 220,
            "type": "CLOAK",
            "address": 0x097a66,
            "classification": ItemClassification.useful
        },
    "Crystal cloak":
        {
            "id": 221,
            "type": "CLOAK",
            "address": 0x097a67,
            "classification": ItemClassification.useful
        },
    "Royal cloak":
        {
            "id": 222,
            "type": "CLOAK",
            "address": 0x097a68,
            "classification": ItemClassification.useful
        },
    "Blood cloak":
        {
            "id": 223,
            "type": "CLOAK",
            "address": 0x097a69,
            "classification": ItemClassification.useful
        },
    "Joseph's cloak":
        {
            "id": 224,
            "type": "CLOAK",
            "address": 0x097a6a,
            "classification": ItemClassification.useful
        },
    "Twilight cloak":
        {
            "id": 225,
            "type": "CLOAK",
            "address": 0x097a6b,
            "classification": ItemClassification.useful
        },
    "Moonstone":
        {
            "id": 227,
            "type": "ACCESSORY",
            "address": 0x097a6d,
            "classification": ItemClassification.useful
        },
    "Sunstone":
        {
            "id": 228,
            "type": "ACCESSORY",
            "address": 0x097a6e,
            "classification": ItemClassification.useful
        },
    "Bloodstone":
        {
            "id": 229,
            "type": "ACCESSORY",
            "address": 0x097a6f,
            "classification": ItemClassification.useful
        },
    "Staurolite":
        {
            "id": 230,
            "type": "ACCESSORY",
            "address": 0x097a70,
            "classification": ItemClassification.useful
        },
    "Ring of pales":
        {
            "id": 231,
            "type": "ACCESSORY",
            "address": 0x097a71,
            "classification": ItemClassification.useful
        },
    "Zircon":
        {
            "id": 232,
            "type": "ACCESSORY",
            "address": 0x097a72,
            "classification": ItemClassification.filler
        },
    "Aquamarine":
        {
            "id": 233,
            "type": "ACCESSORY",
            "address": 0x097a73,
            "classification": ItemClassification.filler
        },
    "Turquoise":
        {
            "id": 234,
            "type": "ACCESSORY",
            "address": 0x097a74,
            "classification": ItemClassification.filler
        },
    "Onyx":
        {
            "id": 235,
            "type": "ACCESSORY",
            "address": 0x097a75,
            "classification": ItemClassification.filler
        },
    "Garnet":
        {
            "id": 236,
            "type": "ACCESSORY",
            "address": 0x097a76,
            "classification": ItemClassification.filler
        },
    "Opal":
        {
            "id": 237,
            "type": "ACCESSORY",
            "address": 0x097a77,
            "classification": ItemClassification.filler
        },
    "Diamond":
        {
            "id": 238,
            "type": "ACCESSORY",
            "address": 0x097a78,
            "classification": ItemClassification.filler
        },
    "Lapis lazuli":
        {
            "id": 239,
            "type": "ACCESSORY",
            "address": 0x097a79,
            "classification": ItemClassification.useful
        },
    "Ring of ares":
        {
            "id": 240,
            "type": "ACCESSORY",
            "address": 0x097a7a,
            "classification": ItemClassification.useful
        },
    "Gold ring":
        {
            "id": 241,
            "type": "ACCESSORY",
            "address": 0x097a7b,
            "classification": ItemClassification.progression
        },
    "Silver ring":
        {
            "id": 242,
            "type": "ACCESSORY",
            "address": 0x097a7c,
            "classification": ItemClassification.progression
        },
    "Ring of varda":
        {
            "id": 243,
            "type": "ACCESSORY",
            "address": 0x097a7d,
            "classification": ItemClassification.useful
        },
    "Ring of arcana":
        {
            "id": 244,
            "type": "ACCESSORY",
            "address": 0x097a7e,
            "classification": ItemClassification.useful
        },
    "Mystic pendant":
        {
            "id": 245,
            "type": "ACCESSORY",
            "address": 0x097a7f,
            "classification": ItemClassification.useful
        },
    "Heart broach":
        {
            "id": 246,
            "type": "ACCESSORY",
            "address": 0x097a80,
            "classification": ItemClassification.useful
        },
    "Necklace of j":
        {
            "id": 247,
            "type": "ACCESSORY",
            "address": 0x097a81,
            "classification": ItemClassification.useful
        },
    "Gauntlet":
        {
            "id": 248,
            "type": "ACCESSORY",
            "address": 0x097a82,
            "classification": ItemClassification.useful
        },
    "Ankh of life":
        {
            "id": 249,
            "type": "ACCESSORY",
            "address": 0x097a83,
            "classification": ItemClassification.useful
        },
    "Ring of feanor":
        {
            "id": 250,
            "type": "ACCESSORY",
            "address": 0x097a84,
            "classification": ItemClassification.useful
        },
    "Medal":
        {
            "id": 251,
            "type": "ACCESSORY",
            "address": 0x097a85,
            "classification": ItemClassification.useful
        },
    "Talisman":
        {
            "id": 252,
            "type": "ACCESSORY",
            "address": 0x097a86,
            "classification": ItemClassification.useful
        },
    "Duplicator":
        {
            "id": 253,
            "type": "ACCESSORY",
            "address": 0x097a87,
            "classification": ItemClassification.useful
        },
    "King's stone":
        {
            "id": 254,
            "type": "ACCESSORY",
            "address": 0x097a88,
            "classification": ItemClassification.useful
        },
    "Covenant stone":
        {
            "id": 255,
            "type": "ACCESSORY",
            "address": 0x097a89,
            "classification": ItemClassification.useful
        },
    "Nauglamir":
        {
            "id": 256,
            "type": "ACCESSORY",
            "address": 0x097a8a,
            "classification": ItemClassification.useful
        },
    "Secret boots":
        {
            "id": 257,
            "type": "ACCESSORY",
            "address": 0x097a8b,
            "classification": ItemClassification.filler
        },
    "Soul of bat":
        {
            "id": 300,
            "type": "RELIC",
            "address": 0x097964,
            "classification": ItemClassification.progression
        },
    "Fire of bat":
        {
            "id": 301,
            "type": "RELIC",
            "address": 0x097965,
            "classification": ItemClassification.useful
        },
    "Echo of bat":
        {
            "id": 302,
            "type": "RELIC",
            "address": 0x097966,
            "classification": ItemClassification.progression
        },
    "Force of echo":
        {
            "id": 303,
            "type": "RELIC",
            "address": 0x097967,
            "classification": ItemClassification.useful
        },
    "Soul of wolf":
        {
            "id": 304,
            "type": "RELIC",
            "address": 0x097968,
            "classification": ItemClassification.progression
        },
    "Power of wolf":
        {
            "id": 305,
            "type": "RELIC",
            "address": 0x097969,
            "classification": ItemClassification.useful
        },
    "Skill of wolf":
        {
            "id": 306,
            "type": "RELIC",
            "address": 0x09796a,
            "classification": ItemClassification.useful
        },
    "Form of mist":
        {
            "id": 307,
            "type": "RELIC",
            "address": 0x09796b,
            "classification": ItemClassification.progression
        },
    "Power of mist":
        {
            "id": 308,
            "type": "RELIC",
            "address": 0x09796c,
            "classification": ItemClassification.progression
        },
    "Gas cloud":
        {
            "id": 309,
            "type": "RELIC",
            "address": 0x09796d,
            "classification": ItemClassification.useful
        },
    "Cube of zoe":
        {
            "id": 310,
            "type": "RELIC",
            "address": 0x09796e,
            "classification": ItemClassification.progression
        },
    "Spirit orb":
        {
            "id": 311,
            "type": "RELIC",
            "address": 0x09796f,
            "classification": ItemClassification.useful
        },
    "Gravity boots":
        {
            "id": 312,
            "type": "RELIC",
            "address": 0x097970,
            "classification": ItemClassification.progression
        },
    "Leap stone":
        {
            "id": 313,
            "type": "RELIC",
            "address": 0x097971,
            "classification": ItemClassification.progression
        },
    "Holy symbol":
        {
            "id": 314,
            "type": "RELIC",
            "address": 0x097972,
            "classification": ItemClassification.progression
        },
    "Faerie scroll":
        {
            "id": 315,
            "type": "RELIC",
            "address": 0x097973,
            "classification": ItemClassification.useful
        },
    "Jewel of open":
        {
            "id": 316,
            "type": "RELIC",
            "address": 0x097974,
            "classification": ItemClassification.progression
        },
    "Merman statue":
        {
            "id": 317,
            "type": "RELIC",
            "address": 0x097975,
            "classification": ItemClassification.progression
        },
    "Bat card":
        {
            "id": 318,
            "type": "RELIC",
            "address": 0x097976,
            "classification": ItemClassification.useful
        },
    "Ghost card":
        {
            "id": 319,
            "type": "RELIC",
            "address": 0x097977,
            "classification": ItemClassification.useful
        },
    "Faerie card":
        {
            "id": 320,
            "type": "RELIC",
            "address": 0x097978,
            "classification": ItemClassification.useful
        },
    "Demon card":
        {
            "id": 321,
            "type": "RELIC",
            "address": 0x097979,
            "classification": ItemClassification.progression
        },
    "Sword card":
        {
            "id": 322,
            "type": "RELIC",
            "address": 0x09797a,
            "classification": ItemClassification.useful
        },
    "Heart of vlad":
        {
            "id": 325,
            "type": "RELIC",
            "address": 0x09797d,
            "classification": ItemClassification.progression
        },
    "Tooth of vlad":
        {
            "id": 326,
            "type": "RELIC",
            "address": 0x09797e,
            "classification": ItemClassification.progression
        },
    "Rib of vlad":
        {
            "id": 327,
            "type": "RELIC",
            "address": 0x09797f,
            "classification": ItemClassification.progression
        },
    "Ring of vlad":
        {
            "id": 328,
            "type": "RELIC",
            "address": 0x097980,
            "classification": ItemClassification.progression
        },
    "Eye of vlad":
        {
            "id": 329,
            "type": "RELIC",
            "address": 0x097981,
            "classification": ItemClassification.progression
        },
    "Victory":
        {
            "id": 400,
            "type": "EVENT",
            "address": 0x000000,
            "classification": ItemClassification.progression
        },
    "Boss token":
        {
            "id": 401,
            "type": "EVENT",
            "address": 0x000000,
            "classification": ItemClassification.progression
        },
    "Exploration token":
        {
            "id": 402,
            "type": "EVENT",
            "address": 0x000000,
            "classification": ItemClassification.progression
        },
    "Heart Vessel":
        {
            "id": 412,
            "type": "POWERUP",
            "address": 0x097ba8,
            "classification": ItemClassification.useful
        },
    "Life Vessel":
        {
            "id": 423,
            "type": "POWERUP",
            "address": 0x097ba0,
            "classification": ItemClassification.useful
        },
}

relic_id_to_name = {v["id"]: k for k, v in items.items() if v["type"] == "RELIC"}
relic_table = {k: v for k, v in items.items() if v["type"] == "RELIC"}
progression_items = {k: v for k, v in items.items() if v["classification"] == ItemClassification.progression}
id_to_item = {v["id"]: v for k, v in items.items()}
item_id_to_name = {value["id"]: key for key, value in items.items()}
weapon1 = {k: v for k, v in items.items() if v["type"] == "WEAPON1"}
shield = {k: v for k, v in items.items() if v["type"] == "SHIELD"}
armor = {k: v for k, v in items.items() if v["type"] == "ARMOR"}
helmet = {k: v for k, v in items.items() if v["type"] == "HELMET"}
cloak = {k: v for k, v in items.items() if v["type"] == "CLOAK"}
accessory = {k: v for k, v in items.items() if v["type"] == "ACCESSORY"}
