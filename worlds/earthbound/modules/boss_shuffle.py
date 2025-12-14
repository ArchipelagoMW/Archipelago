from typing import NamedTuple, TYPE_CHECKING
from logging import warning
import struct
if TYPE_CHECKING:
    from .. import EarthBoundWorld
    from ..Rom import LocalRom
import struct

boss_sprite_pointers = {
    "Frank": 0xEF2B69,
    "Frankystein Mark II": 0xEF43F9,
    "Titanic Ant": 0xEF3B57,
    "Captain Strong": 0xEF23A9,
    "Everdred": 0xEF2BCD,
    "Mr. Carpainter": 0xEF2BFF,
    "Mondo Mole": 0xEF4557,
    "Boogey Tent": 0xEF3748,
    "Mini Barf": 0xEF3B89,
    "Master Belch": 0xEF3CD6,
    "Trillionage Sprout": 0xEF3BBB,
    "Guardian Digger": 0xEF45BB,
    "Dept. Store Spook": 0xEF495F,
    "Evil Mani-Mani": 0xEF395F,
    "Clumsy Robot": 0xEF45A2,
    "Shrooom!": 0xEF392B,
    "Plague Rat of Doom": 0xEF4570,
    "Thunder and Storm": 0xEF3C70,
    "Kraken": 0xEF3991,
    "Guardian General": 0xEF3C3C,
    "Master Barf": 0xEF39F5,
    "Starman Deluxe": 0xEF3A59,
    "Electro Specter": 0xEF45ED,
    "Carbon Dog": 0xEF3D08,
    "Ness's Nightmare": 0xEF395F,
    "Heavily Armed Pokey": 0xEF49AA,
    "Starman Junior": 0xEF3A59,
    "Diamond Dog": 0xEF3D08,
    "Giygas": 0xEF40F2

}

boss_plando_keys = {
    "Frank",
    "Frankystein Mark II",
    "Frankystein",
    "Captain Strong",
    "Strong",
    "Everdred",
    "Mr. Carpainter",
    "Mr Carpainter",
    "Carpainter",
    "Mondo Mole",
    "Boogey Tent",
    "Mini Barf",
    "Master Belch",
    "Belch",
    "Trillionage Sprout",
    "Guardian Digger",
    "Dept. Store Spook",
    "Dept Store Spook",
    "Evil Mani Mani",
    "Mani Mani",
    "Clumsy Robot",
    "Shrooom!",
    "Shrooom",
    "Shroom!",
    "Shroooooom!",
    "Shroom",
    "Plague Rat of Doom",
    "Thunder and Storm",
    "Kraken",
    "The Kraken",
    "Guardian General",
    "Master Barf",
    "Starman Deluxe",
    "Starman DX",
    "Electro Specter",
    "Carbon Dog",
    "Ness's Nightmare",
    "Nesss Nightmare",
    "Heavily Armed Pokey",
    "Pokey"
    "Starman Junior",
    "Diamond Dog",
    "Giygas"
}

boss_typo_key = {
    "Frankystein": "Frankystein Mark II",
    "Strong": "Captain Strong",
    "Mr Carpainter": "Mr. Carpainter",
    "Carpainter": "Mr. Carpainter",
    "Belch": "Master Belch",
    "Dept Store Spook": "Dept. Store Spook",
    "Evil Mani Mani": "Evil Mani-Mani",
    "Mani Mani": "Evil Mani-Mani",
    "Shroom": "Shrooom!",
    "Shrooom": "Shrooom!",
    "Shroom!": "Shrooom!",
    "Shroooooom!": "Shrooom!",
    "The Kraken": "Kraken",
    "Starman DX": "Starman Deluxe",
    "Nesss Nightmare": "Ness's Nightmare",
    "Pokey": "Heavily Armed Pokey"
}

banned_transformations = ["Master Belch", "Master Barf", "Kraken", "Heavily Armed Pokey"]
hard_final_bosses = ["Carbon Dog", "Kraken", "Clumsy Robot", "Starman Junior", "Starman Deluxe", "Giygas", "Thunder and Storm", "Electro Specter",
                     "Evil Mani-Mani", "Ness's Nightmare", "Shrooom!", "Master Belch"]


class SlotInfo(NamedTuple):
    sprite_addrs: list[int]
    short_names: list[int]
    long_names: list[int]
    battle_data: list[int]


class BossData(NamedTuple):
    sprite_pointer: int
    short_name_pointer: int
    long_name_pointer: int
    battle_group: int
    enemy_id: int
    music: int


def initialize_bosses(world: "EarthBoundWorld") -> None:
    from ..Options import BossShuffle
     
    world.boss_list = [
        "Frank",
        "Frankystein Mark II",
        "Titanic Ant",
        "Captain Strong",
        "Everdred",
        "Mr. Carpainter",
        "Mondo Mole",
        "Boogey Tent",
        "Mini Barf",
        "Master Belch",
        "Trillionage Sprout",
        "Guardian Digger",
        "Dept. Store Spook",
        "Evil Mani-Mani",
        "Clumsy Robot",
        "Shrooom!",
        "Plague Rat of Doom",
        "Thunder and Storm",
        "Kraken",
        "Guardian General",
        "Master Barf",
        "Starman Deluxe",
        "Electro Specter",
        "Carbon Dog",
        "Ness's Nightmare",
        "Heavily Armed Pokey",
        "Starman Junior",
        "Diamond Dog",
        "Giygas"
    ]

    world.boss_slots = {
        "Frank": SlotInfo([0x0F9338],
                          [0x066111, 0x066198, 0x0661AC],
                          [0x065F11, 0x065F20, 0x066482, 0x0660C5, 0x0746E2, 0x074BC1, 0x074E1D],
                          [0x0683FF]),
        "Frankystein Mark II": SlotInfo([0x0F96F0], [], [0x066146, 0x06648B, 0x0664FC], [0x068406]),
        "Titanic Ant": SlotInfo([], [], [], [0x06840D]),
        "Captain Strong": SlotInfo([], [0x5FC2B, 0x05FCF7, 0x065F88, 0x066085],
                                   [0x05FC59, 0x3317DB], [0x068468]),
        "Everdred": SlotInfo([0x0F9A64, 0x0F9FB4], [0x2EEEEA], [0x095C70], [0x06846F]),
        "Mr. Carpainter": SlotInfo([0x0FA27E, 0x0FA5D0],
                                   [0x0990DA, 0x0684D0],
                                   [0x0993DB, 0x09945E, 0x099311, 0x099364, 0x098EF6, 0x099143, 0x099028,
                                    0x0983BB, 0x09840C, 0x09835B, 0x09056F, 0x0794EC],
                                   [0x0684FD]),
        "Mondo Mole": SlotInfo([], [], [], [0x068414]),
        "Boogey Tent": SlotInfo([0x0FACEB], [], [], [0x06853C]),
        "Mini Barf": SlotInfo([0x0FB0B4], [], [], [0x2F9515]),
        "Master Belch": SlotInfo([0x0FB7CF],
                                 [0x09E64D, 0x09E690, 0x2EEED7, 0x08EF21, 0x08EF38],
                                 [0x2F6297, 0x2F62B3, 0x2F6910, 0x2F6973],
                                 [0x068558]),
        "Trillionage Sprout": SlotInfo([], [], [], [0x068422]),
        "Guardian Digger": SlotInfo([0x0FC11B, 0x0FC0B5, 0x0FC12C, 0x0FC0D7, 0x0FC0C6],
                                    [],
                                    [],
                                    [0x06858E, 0x068595, 0x06859C, 0x0685A3, 0x0685AA]),
        "Dept. Store Spook": SlotInfo([0x0FC803], [], [], [0x06855F]),
        "Evil Mani-Mani": SlotInfo([0x0FE6E4], [], [0x0978AD, 0x09782D, 0x097998], [0x068587]),
        "Clumsy Robot": SlotInfo([0x0FC429], [], [], [0x06856D]),
        "Shrooom!": SlotInfo([], [], [], [0x06841B]),
        "Plague Rat of Doom": SlotInfo([], [], [], [0x068429]),
        "Thunder and Storm": SlotInfo([], [], [], [0x068430]),
        "Kraken": SlotInfo([0x092CD0, 0x0FE370, 0x0FE381, 0x0FE392, 0x092D13],
                           [0x092D4D],
                           [0x086061, 0x086139, 0x08B430, 0x08B6FC, 0x08B8B4, 0x08B591, 0x09AB2B],
                           [0x0685B1, 0x2F9472, 0x2F9491, 0x2F94B0]),
        "Guardian General": SlotInfo([0x0FD7E2], [], [], [0x2F9453]),
        "Master Barf": SlotInfo([0x0FDB23], [], [], [0x068574]),
        "Starman Deluxe": SlotInfo([0x0FB626], [], [0x092C29], [0x2F942F]),
        "Electro Specter": SlotInfo([], [], [], [0x068437]),
        "Carbon Dog": SlotInfo([], [], [], [0x06843E]),
        "Ness's Nightmare": SlotInfo([0x0FE3B4], [], [], [0x068580]),
        "Heavily Armed Pokey": SlotInfo([0x09C2EC], [0x2EEEC3, 0x2EEECC], [], []),
        "Starman Junior": SlotInfo([], [], [], []),
        "Diamond Dog": SlotInfo([], [], [], []),
        "Giygas": SlotInfo([0x09C2BF, 0x09C2E5], [0x2EF0A9], [0x2EF09F], [])
    }

    world.boss_info = {
        "Frank": BossData(0x0099, 0xEEEEBC, 0xEEEEBC, 0x01C0, 0x83, 0x64),
        "Frankystein Mark II": BossData(0x0191, 0xEEEF0A, 0xEEEEF6, 0x01C1, 0x82, 0x66),
        "Titanic Ant": BossData(0x0139, 0xEEEF1E, 0xEEEF16, 0x01C2, 0x25, 0x67),
        "Captain Strong": BossData(0x004B, 0xEEEF2A, 0xEEEF22, 0x01C4, 0xE4, 0x66),
        "Everdred": BossData(0x009D, 0xEEEF31, 0xEEEF31, 0x01C5, 0x6E, 0x62),
        "Mr. Carpainter": BossData(0x009F, 0xEEEF3E, 0xEEEF3A, 0x01C6, 0x1A, 0x94),
        "Mondo Mole": BossData(0x019F, 0xEEEF4F, 0xEEEF49, 0x01C7, 0x29, 0x67),
        "Boogey Tent": BossData(0x0110, 0xEEEF5B, 0xEEEF54, 0x01CA, 0x66, 0x66),
        "Mini Barf": BossData(0x013B, 0xEEEF65, 0xEEEF60, 0x01E2, 0xE2, 0x63),
        "Master Belch": BossData(0x0148, 0xEEEF71, 0xEEEF6A, 0x01C8, 0x5D, 0x63),
        "Trillionage Sprout": BossData(0x013D, 0xEEEF83, 0xEEEF77, 0x01C9, 0x5A, 0x67),
        "Guardian Digger": BossData(0x01A3, 0xEEEF93, 0xEEEF8A, 0x01CB, 0x2A, 0x67),
        "Dept. Store Spook": BossData(0x01C7, 0xEEEFA6, 0xEEEF9A, 0x01CC, 0x02, 0x66),
        "Evil Mani-Mani": BossData(0x0125, 0xEEEFC1, 0xEEEFAC, 0x01CD, 0x89, 0x94),
        "Clumsy Robot": BossData(0x01A2, 0xEEEFD2, 0xEEEFCB, 0x01CE, 0x92, 0x94),
        "Shrooom!": BossData(0x0123, 0xEEEFD8, 0xEEEFD8, 0x01D1, 0x27, 0x67),
        "Plague Rat of Doom": BossData(0x01A0, 0xEEEFEE, 0xEEEFE0, 0x01CF, 0x28, 0x67),
        "Thunder and Storm": BossData(0x0144, 0xEEEFFF, 0xEEEFF3, 0x01D0, 0x80, 0x68),
        "Kraken": BossData(0x0127, 0xEEF005, 0xEEF005, 0x01D3, 0x31, 0x68),
        "Guardian General": BossData(0x0142, 0xEEF015, 0xEEF00C, 0x01D4, 0x49, 0x67),
        "Master Barf": BossData(0x012B, 0xEEEF65, 0xEEF01D, 0x01D5, 0x5F, 0x63),
        "Starman Deluxe": BossData(0x012F, 0xEEF034, 0xEEF029, 0x01D2, 0x4A, 0x61),
        "Electro Specter": BossData(0x01A5, 0xEEF043, 0xEEF03B, 0x01D6, 0x74, 0x68),
        "Carbon Dog": BossData(0x014A, 0xEEF052, 0xEEF04B, 0x01D7, 0x1B, 0x67),
        "Ness's Nightmare": BossData(0x0125, 0xEEF070, 0xEEF06A, 0x01D8, 0x15, 0x94),
        "Heavily Armed Pokey": BossData(0x01CA, 0xEEF064, 0xEEF056, 0x000E, 0xD8, 0x69),
        "Starman Junior": BossData(0x012F, 0xEEF082, 0xEEF07A, 0x01DA, 0xD6, 0x94),
        "Diamond Dog": BossData(0x014A, 0xEEF052, 0xEEF089, 0x01D9, 0x53, 0x61),
        "Giygas": BossData(0x0172, 0xEEF095, 0xEEF095, 0x01DD, 0xDC, 0x49)
    }

    if world.options.skip_prayer_sequences:
        # Boss shuffle sprites needs to apply to the skip prayer cleanup too
        world.boss_slots["Giygas"].sprite_addrs.append(0x07B9AC)
        world.boss_slots["Heavily Armed Pokey"].sprite_addrs.append(0x07B9A7)

    # mole/rat text
    # todo; Giygas sprites/text

    world.boss_slot_order = world.boss_list.copy()
    if type(world.options.boss_shuffle.value) == str:
        boss_plando = world.options.boss_shuffle.value.split(";")
        shuffle_result = boss_plando.pop()
    else:
        boss_plando = []
        shuffle_result = world.options.boss_shuffle.value

    if shuffle_result == "true" or shuffle_result == 1:
        world.random.shuffle(world.boss_list)

        if not world.options.decouple_diamond_dog:
            world.boss_list.remove("Diamond Dog")
            insert_index = 28 if not world.options.boss_shuffle_add_giygas else 27
            world.boss_list.insert(insert_index, "Diamond Dog")

        if not world.options.boss_shuffle_add_giygas:
            world.boss_list.remove("Giygas")
            world.boss_list.insert(29, "Giygas")

    if world.options.safe_final_boss:
        while world.boss_list[25] in hard_final_bosses:
            i = world.random.randrange(len(world.boss_list))
            if (world.boss_list[i] == "Diamond Dog" and not world.options.decouple_diamond_dog) or (
                world.boss_list[i] == "Giygas" and not world.options.boss_shuffle_add_giygas
            ):
                continue
            world.boss_list[25], world.boss_list[i] = world.boss_list[i], world.boss_list[25]

    did_plando_diam_dog = False
    diamond_dog_plando_slot = None

    for item in boss_plando:
        boss_block = item.split("-")
        boss = boss_block[0].title()  # Boss is what's being placed
        slot = boss_block[1].title()  # SLot is where the boss is going.
        if boss in boss_typo_key:
            boss = boss_typo_key[boss]

        if slot in boss_typo_key:
            slot = boss_typo_key[boss]

        if slot == "Diamond Dog":
            did_plando_diam_dog = True
            diamond_dog_plando_slot = boss

        old_index = world.boss_list.index(boss)  # This should be the slot where the chosen boss currently is
        new_index = world.boss_slot_order.index(slot)  # Boss slots should use the original position

        world.boss_list[old_index] = world.boss_list[new_index]  # We want to replace the boss that was originally there with the boss we're swapping with
        world.boss_list[new_index] = boss

    if world.boss_list[25] == "Carbon Dog" and world.boss_list[27] in banned_transformations:
        if did_plando_diam_dog:
            warning(f"""Unable to plando {diamond_dog_plando_slot} for {world.multiworld.get_player_name(world.player)}'s EarthBound world.
This boss cannot be placed onto Diamond Dog's slot if Carbon Dog is on Heavily Armed Pokey's slot.
This message is likely the result of randomization and can be safely ignored.""")  # Why is this spacing the only way to get the message to render legibly
        original_boss = world.boss_list[27]
        transformation_replacement = world.random.randint(0, 24)
        while world.boss_list[transformation_replacement] in banned_transformations:
            transformation_replacement = world.random.randint(0, 24)
        world.boss_list[27] = world.boss_list[transformation_replacement]
        world.boss_list[transformation_replacement] = original_boss

def write_bosses(world: "EarthBoundWorld", rom: "LocalRom") -> None:
    rom.write_bytes(0x15E527, bytearray([0x00, 0x00]))  # Blank out Pokey's end battle action
    rom.write_bytes(0x15B8B9, bytearray([0x00, 0x00]))
    rom.write_bytes(0x15DD13, bytearray([0x00, 0x00]))  # Blank out barf's end battle script
    rom.write_bytes(0x15E69F, bytearray([0x00, 0x00]))  # Blank giygas
    if world.boss_list[25] == "Carbon Dog":  # Heavily armed Pokey
        pokey_adjust = 27
    else:
        pokey_adjust = 25

    rom.write_bytes(world.enemies[world.boss_list[pokey_adjust]].address + 78, bytearray([0x13, 0x01]))
    for i in range(1, world.enemies[world.boss_list[pokey_adjust]].attack_extensions):
        enemy_new = f"{world.enemies[world.boss_list[pokey_adjust]].name} ({i + 1})"
        rom.write_bytes(world.enemies[enemy_new].address + 78, bytearray([0x13, 0x01]))

    if world.boss_list[20] == "Carbon Dog":  # Master Barf
        barf_adjust = 27
    else:
        barf_adjust = 20
        
    rom.write_bytes(world.enemies[world.boss_list[barf_adjust]].address + 78, bytearray([0xF4, 0x00]))
    for i in range(1, world.enemies[world.boss_list[barf_adjust]].attack_extensions):
        enemy_new = f"{world.enemies[world.boss_list[barf_adjust]].name} ({i + 1})"
        rom.write_bytes(world.enemies[enemy_new].address + 78, bytearray([0xF4, 0x00]))

    if world.boss_list[28] == "Carbon Dog":  # Giygas 2
        # I should probably just hard stop Carbon Dog from being here
        giygas_2_adjust = 27  # Set to the diamond dog slot
    else:

        giygas_2_adjust = 28

    rom.write_bytes(world.enemies[world.boss_list[giygas_2_adjust]].address + 78, bytearray([0x16, 0x01]))
    for i in range(1, world.enemies[world.boss_list[giygas_2_adjust]].attack_extensions):
        enemy_new = f"{world.enemies[world.boss_list[giygas_2_adjust]].name} ({i + 1})"
        rom.write_bytes(world.enemies[enemy_new].address + 78, bytearray([0x16, 0x01]))

    if world.boss_list[25] != "Heavily Armed Pokey":
        rom.write_bytes(0x15E50A, bytearray([0x19, 0x6E, 0xEF]))
        rom.write_bytes(0x15E4FE, bytearray([0x70, 0x11, 0x01]))  # Add to the scaling list?

    for slot, boss in enumerate(world.boss_slot_order):
        for address in world.boss_slots[boss].sprite_addrs:  # sprite
            rom.write_bytes(address, struct.pack("H", world.boss_info[world.boss_list[slot]].sprite_pointer))

        for address in world.boss_slots[boss].short_names:  # short name
            rom.write_bytes(address, struct.pack("I", world.boss_info[world.boss_list[slot]].short_name_pointer))

        for address in world.boss_slots[boss].long_names:  # long name
            rom.write_bytes(address, struct.pack("I", world.boss_info[world.boss_list[slot]].long_name_pointer))

        for address in world.boss_slots[boss].battle_data:  # battle
            rom.write_bytes(address, struct.pack("H", world.boss_info[world.boss_list[slot]].battle_group))

    rom.write_bytes(0x10DF7F, struct.pack("H", world.boss_info[world.boss_list[25]].enemy_id))
    rom.write_bytes(0x10DF86, struct.pack("H", world.boss_info[world.boss_list[25]].enemy_id))
    # rom.write_bytes(0x10DF8D, struct.pack("H", world.boss_info[world.boss_list[25]].enemy_id))
    rom.write_bytes(0x10DFA2, struct.pack("H", world.boss_info[world.boss_list[25]].enemy_id))
    rom.write_bytes(0x10D563, struct.pack("H", world.boss_info[world.boss_list[25]].enemy_id))
    rom.write_bytes(world.enemies[world.boss_list[25]].address + 91, bytearray([0x00]))  # Row of the enemy

    rom.write_bytes(0x10DF83, struct.pack("H", world.boss_info[world.boss_list[28]].enemy_id))
    rom.write_bytes(0x02C4FD, struct.pack("H", world.boss_info[world.boss_list[28]].enemy_id))
    rom.write_bytes(0x10D560, struct.pack("H", world.boss_info[world.boss_list[28]].enemy_id))

    rom.write_bytes(0x159FC7, struct.pack("H", world.boss_info[world.boss_list[27]].enemy_id))
    rom.write_bytes(0x15D5C1, struct.pack("H", world.boss_info[world.boss_list[27]].enemy_id))
    # carbon dog's transformation
    rom.write_bytes(0x10DF69, struct.pack("H", world.boss_info[world.boss_list[27]].enemy_id))
    rom.write_bytes(0x02C503, bytearray([world.boss_info[world.boss_list[28]].music]))  # music

    rom.write_bytes(0x2F188F, struct.pack("I", boss_sprite_pointers[world.boss_list[3]]))

    rom.write_bytes(0x0302CE, struct.pack("H", 0x0154))
    rom.write_bytes(0x05F870, struct.pack("H", 0x0154))
    rom.write_bytes(0x0F8E3D, struct.pack("H", 0x0154))
    rom.write_bytes(0x05F886, struct.pack("H", 0x0154))
    rom.write_bytes(0x05F8A1, struct.pack("H", 0x0154))
    rom.write_bytes(0x05F8E3, struct.pack("H", 0x0154))
    rom.write_bytes(0x05FB0E, struct.pack("H", 0x0154))
    rom.write_bytes(0x05FBFC, struct.pack("H", 0x0154))
    rom.write_bytes(0x05FD08, struct.pack("H", 0x0154))
    rom.write_bytes(0x05FD5C, struct.pack("H", 0x0154))
    rom.copy_bytes(0x10DF7B, 6, 0x2FFF10)
    if world.boss_list[25] == "Carbon Dog":
        rom.write_bytes(0x2FFF16, bytearray([0x00]))  # Count of enemies
        rom.write_bytes(0x2FFF17, struct.pack("H", world.boss_info[world.boss_list[27]].enemy_id))  # Add diamond dog
        rom.write_bytes(0x2FFF19, bytearray([0xFF]))
        rom.write_bytes(world.enemies[world.boss_list[27]].address + 91, bytearray([0x00]))  # Force to front row
    elif world.boss_list[25] == "Giygas":
        rom.write_bytes(0x0121DF, bytearray([0x00]))
        rom.write_bytes(0x2FFF16, bytearray([0xFF]))
    else:
        rom.write_bytes(0x2FFF16, bytearray([0xFF]))
    
    # c2c505 sets the song
