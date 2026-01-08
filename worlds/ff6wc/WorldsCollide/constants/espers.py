ESPER_COUNT = 27
RAMUH, IFRIT, SHIVA, SIREN, TERRATO, SHOAT, MADUIN, BISMARK, STRAY, PALIDOR, TRITOCH, ODIN, RAIDEN,\
BAHAMUT, ALEXANDR, CRUSADER, RAGNAROK, KIRIN, ZONESEEK, CARBUNKL, PHANTOM, SRAPHIM, GOLEM, UNICORN,\
FENRIR, STARLET, PHOENIX = range(ESPER_COUNT)

id_esper = {
    0   : "Ramuh",
    1   : "Ifrit",
    2   : "Shiva",
    3   : "Siren",
    4   : "Terrato",
    5   : "Shoat",
    6   : "Maduin",
    7   : "Bismark",
    8   : "Stray",
    9   : "Palidor",
    10  : "Tritoch",
    11  : "Odin",
    12  : "Raiden",
    13  : "Bahamut",
    14  : "Alexandr",
    15  : "Crusader",
    16  : "Ragnarok",
    17  : "Kirin",
    18  : "ZoneSeek",
    19  : "Carbunkl",
    20  : "Phantom",
    21  : "Sraphim",
    22  : "Golem",
    23  : "Unicorn",
    24  : "Fenrir",
    25  : "Starlet",
    26  : "Phoenix",
}
esper_id = {v: k for k, v in id_esper.items()}

# order espers appear in menu going left to right, top to bottom
esper_menu_order = [0, 17, 3, 8, 1, 2, 23, 6, 5, 20, 19, 7, 22, 18, 21, 9, 24, 10, 4, 25, 14, 26, 11, 13, 16, 15, 12]
