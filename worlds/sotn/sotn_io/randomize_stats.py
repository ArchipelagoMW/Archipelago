import constants, item_stats, util


weaponHandTypes = [
    constants.HAND_TYPE["SHORT_SWORD"],
    constants.HAND_TYPE["SWORD"],
    constants.HAND_TYPE["THROWING_SWORD"],
    constants.HAND_TYPE["FIST"],
    constants.HAND_TYPE["CLUB"],
    constants.HAND_TYPE["TWO_HANDED_SWORD"],
]


def shuffle_stats(rng, data: dict, stats: [dict], stat: str, offset: int, func: str) -> None:
    shuffled = util.shuffled("", stats)
    for index, item in enumerate(shuffled):
        addr = util.rom_offset(constants.exe, stats[index]["offset"] + offset)
        if func == "short":
            util.write_short(data, addr, item[stat])
        elif func == "char":
            util.write_char(data, addr, item[stat])
        else:
            raise Exception(f"No function {func} in shuffle_stats")


def shuffle_hand_stats(rng, data: dict, new_names: list, stats: [dict], hand_type: str) -> None:
    # Randomize names.
    items = list(filter(lambda item: item["handType"] not in {constants.HAND_TYPE["FOOD"],
                                                              constants.HAND_TYPE["PROJECTILE_CONSUMABLE"],
                                                              constants.HAND_TYPE["OTHER"]} and
                        item["name"] not in ['Firebrand', 'Thunderbrand', 'Icebrand', 'Stone sword', 'Holy sword',
                                             'Dark Blade', 'Sword Familiar', 'Harper', 'Gram', 'Yasutsuna',
                                             'Monster vial 1', 'Monster vial 2', 'Monster vial 3', 'Pentagram',
                                             'Bat Pentagram', 'Neutron bomb', 'Power of Sire', 'Jewel sword',
                                             'Shield rod', 'Mace', 'Morningstar', 'Holy rod', 'Star flail', 'Moon rod',
                                             'Were Bane', 'Rapier'], stats))
    shuffled = util.shuffled("", items)
    for index, item in enumerate(shuffled):
        new_names.append({"id": stats[index]["id"], "name": item["name"]})
        addr = util.rom_offset(constants.exe, items[index]["offset"] + 0x00)  # Why add???
        util.write_word(data, addr, item["nameAddress"])
    if hand_type != 'SHIELD':
        # Randomize stats.
        if hand_type not in weaponHandTypes:
            shuffled = util.shuffled("", stats)
            for index, item in enumerate(shuffled):
                addr = util.rom_offset(constants.exe, stats[index]["offset"] + 0x08)
                addr = util.write_short(data, addr, item["attack"])
                addr = util.write_short(data, addr, item["defense"])
            shuffle_stats("", data, stats, "stunFrames", 0x26, "short")
            shuffle_stats("", data, stats, "range", 0x28, "short")
        else:
            shuffle_stats("", data, stats, "range", 0x28, "short")
        items = []
        for item in stats:
            """There is no filter over here: no true is ever returned
            if ([
            'Mourneblade',
            'Jewel sword',
            ].indexOf(item.name) !== -1) {
            return false
            }
            """
            pass

        shuffle_stats("", data, items, "extra", 0x2a, "char")
        # Randomize icons and sprite.
        items = list(filter(lambda item: item["handType"] not in [constants.HAND_TYPE["FOOD"],
                                                                  constants.HAND_TYPE["DAMAGE_CONSUMABLE"],
                                                                  constants.HAND_TYPE["PROJECTILE_CONSUMABLE"]]
                            and item["name"] not in ["Library card", "Meal ticket", "Life apple", "Hammer"], stats))
        shuffle_stats("", data, items, "icon", 0x2c, "short")
    # Randomize palettes.
    items = list(filter(lambda item: item["name"] not in ["Meal ticket", "Library card"], stats))
    shuffle_stats("", data, items, "palette", 0x2e, "short")


def shuffle_equipment_stats(rng, data: dict, new_names: list, stats: [dict]) -> None:
    # Randomize names.
    def randomize_names() -> None:
        nonlocal new_names, shuffled, items, data
        for index, item in enumerate(shuffled):
            new_names.append({"id": items[index]["id"], "name": item["name"]})
            addr = util.rom_offset(constants.exe, items[index]["offset"] + 0x00)
            addr = util.write_word(data, addr, item["nameAddress"])

    items = list(filter(lambda item: item["name"] not in ["Cloth tunic", "Hide cuirass", "Bronze cuirass",
                                                          "Iron cuirass", "Steel cuirass", "Silver plate", "Gold plate",
                                                          "Platinum mail", "Diamond plate", "Fire mail",
                                                          "Lightning mail", "Ice mail", "Mirror cuirass",
                                                          "Spike Breaker", "Dark armor", "Holy mail", "Moonstone",
                                                          "Sunstone", "Bloodstone", "Gauntlet", "Duplicator",
                                                          "Secret boots", "Sunglasses", "Holy glasses", "Goggles",
                                                          "Ballroom mask", "Stone mask", "Felt hat", "Leather hat",
                                                          "Velvet hat", "Wizard hat", "Ring of Pales", "Ring of Ares",
                                                          "Gold ring", "Silver ring", "Ring of Varda", "Ring of Arcana",
                                                          "Ring of Feanor", "Necklace of J"], stats))
    shuffled = util.shuffled("", items)
    randomize_names()
    items = list(filter(lambda item: item["name"] in ["Sunglasses", "Holy glasses", "Goggles", "Ballroom mask",
                                                      "Stone mask"], stats))
    shuffled = util.shuffled("", items)
    randomize_names()
    items = list(filter(lambda item: item["name"] in ["Felt hat", "Leather hat", "Velvet hat", "Wizard hat"], stats))
    shuffled = util.shuffled("", items)
    randomize_names()
    items = list(filter(lambda item: item["name"] in ["Ring of Pales", "Ring of Ares", "Gold ring", "Silver ring",
                                                      "Ring of Varda", "Ring of Arcana", "Ring of Feanor"], stats))
    shuffled = util.shuffled("", items)
    randomize_names()
    # Randomize stats

    def randomize_stats() -> None:
        nonlocal shuffled, items, data
        for index, item in enumerate(shuffled):
            addr = util.rom_offset(constants.exe, items[index]["offset"] + 0x08)
            addr = util.write_short(data, addr, item["attack"])
            addr = util.write_short(data, addr, item["defense"])
            addr = util.write_char(data, addr, item["strength"])
            addr = util.write_char(data, addr, item["constitution"])
            addr = util.write_char(data, addr, item["intelligence"])
            addr = util.write_char(data, addr, item["luck"])

    # Ignore Duplicator, salable gems, gold & silver rings, and items that
    # have stats in their descriptions
    items = list(filter(lambda item: item["name"] not in ["God\'s Garb", "Silver crown", "Zircon", "Aquamarine",
                                                          "Turquoise", "Onyx", "Garnet", "Opal", "Diamond",
                                                          "Lapis lazuli", "Ring of Ares", "Gold ring", "Silver ring",
                                                          "Necklace of J", "Gauntlet", "Ring of Feanor", "Medal",
                                                          "Duplicator", "King\'s stone", "Covenant stone", "Nauglamir",
                                                          "Circlet", "Gold circlet", "Ruby circlet", "Opal circlet",
                                                          "Topaz circlet", "Beryl circlet", "Cat-eye circl.",
                                                          "Coral circlet"], stats))
    shuffled = util.shuffled("", items)
    randomize_stats()
    items = list(filter(lambda item: item["name"] in ["Circlet", "Gold circlet", "Ruby circlet", "Opal circlet",
                                                      "Topaz circlet", "Beryl circlet", "Cat-eye circl.",
                                                      "Coral circlet"], stats))
    shuffled = util.shuffled("", items)
    randomize_stats()
    # Randomize icons.
    items = list(filter(lambda item: item["name"] not in ["Gauntlet", "Duplicator", "Secret boots", "Sunglasses",
                                                          "Holy glasses", "Goggles", "Ballroom mask", "Stone mask",
                                                          "Felt hat", "Leather hat", "Velvet hat", "Wizard hat",
                                                          "Circlet", "Gold circlet", "Ruby circlet", "Opal circlet",
                                                          "Topaz circlet", "Beryl circlet", "Cat-eye circl.",
                                                          "Coral circlet", "Ring of Pales", "Zircon", "Aquamarine",
                                                          "Turquoise", "Onyx", "Garnet", "Opal", "Diamond",
                                                          "Lapis lazuli", "Ring of Ares", "Gold ring", "Silver ring",
                                                          "Ring of Varda", "Ring of Arcana", "Ring of Feanor",
                                                          "Necklace of J", "Nauglamir", "Mystic pendant"], stats))
    shuffle_stats("", data, items, "icon", 0x18, "short")
    items = list(filter(lambda item: item["name"] in ["Sunglasses", "Holy glasses", "Goggles", "Ballroom mask",
                                                      "Stone mask"], stats))
    shuffle_stats("", data, items, "icon", 0x18, "short")
    items = list(filter(lambda item: item["name"] in ["Felt hat", "Leather hat", "Velvet hat", "Wizard hat"], stats))
    shuffle_stats("", data, items, "icon", 0x18, "short")
    items = list(filter(lambda item: item["name"] in ["Circlet", "Gold circlet", "Ruby circlet", "Opal circlet",
                                                      "Topaz circlet", "Beryl circlet", "Cat-eye circl.",
                                                      "Coral circlet"], stats))
    shuffle_stats("", data, items, "icon", 0x18, "short")
    items = list(filter(lambda item: item["name"] in ["Zircon", "Aquamarine", "Turquoise", "Onyx", "Garnet", "Opal",
                                                      "Diamond", "Lapis lazuli", "Gold ring", "Silver ring",
                                                      "Ring of Varda", "Ring of Arcana", "Ring of Feanor"], stats))
    shuffle_stats("", data, items, "icon", 0x18, "short")
    items = list(filter(lambda item: item["name"] in ["Necklace of J", "Nauglamir", "Mystic pendant"], stats))
    shuffle_stats("", data, items, "icon", 0x18, "short")
    # Randomize palettes.
    shuffle_stats("", data, stats, "palette", 0x1a, "short")


def randomize_stats(data: dict, rng, options) -> list:
    new_names = []
    # Randomize hand item stats by type.
    for hand_type in constants.HAND_TYPE:
        items = list(filter(lambda item: item["handType"] == constants.HAND_TYPE[hand_type], item_stats.hand_list))
        shuffle_hand_stats("", data, new_names, items, hand_type)
    # Randomize attack, defense, and stunFrames of all weapons.
    weapons = list(filter(lambda item: item["handType"] in weaponHandTypes, item_stats.hand_list))
    shuffled = util.shuffled("", weapons)
    for index, item in enumerate(shuffled):
        addr = util.rom_offset(constants.exe, weapons[index]["offset"] + 0x08)
        addr = util.write_short(data, addr, item["attack"])
        addr = util.write_short(data, addr, item["defense"])
    shuffle_stats("", data, weapons, "stunFrames", 0x26, "short")
    # Choose random item's palette for cards.
    rand = util.shuffled("", item_stats.hand_list).pop()
    items = list(filter(lambda item: item["name"] in ["Meal ticket", "Library card"], item_stats.hand_list))
    for item in items:
        addr = util.rom_offset(constants.exe, item["offset"] + 0x2e)
        addr = util.write_short(data, addr, rand["palette"])
    # Randomize equipment item stats.
    for hand_type in constants.TYPE:
        items = list(filter(lambda item: item["type"] == constants.TYPE[hand_type], item_stats.equipment_list))
        shuffle_equipment_stats("", data, new_names, items)

    return new_names








"""
data_test = {}

new_names = randomize_stats(data_test, "", "")
print(data_test)
print(len(data_test))
print(new_names)

with open("o.bin", "rb") as in_file:
    original_bin = list(in_file.read())


for addr, data in data_test.items():
    size = data["len"]
    if size == 1:
        original_bin[addr] = data["val"] & 0xff
    elif size == 2:
        bytes_object = [
            data["val"] & 0xff,
            (data["val"] >> 8) & 0xff
        ]
        for i in range(2):
            original_bin[addr + i] = bytes_object[i]
    elif size == 4:
        bytes_object = [
            data["val"] & 0xff,
            (data["val"] >> 8) & 0xff,
            (data["val"] >> 16) & 0xff,
            (data["val"] >> 24) & 0xff,
        ]
        for i in range(4):
            pass
            original_bin[addr + i] = bytes_object[i]
    else:
        print(f"{size} no function for {data}")

with open("Castlevania - Symphony of the Night (USA) (Track 1).bin", "wb") as out_file:
    out_file.write(bytearray(original_bin))"""


