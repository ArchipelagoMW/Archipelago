from typing import Optional

from ..RomData import RomData
from . import char_table, kanji_table, text_offset_1_table_address_seasons, text_offset_2_table_address_seasons, text_table_eng_address_seasons, \
    text_offset_split_index_seasons, text_offset_1_table_address_ages, text_offset_2_table_address_ages, text_table_eng_address_ages, \
    text_offset_split_index_ages
from ..Util import simple_hex
from ..z80asm.Assembler import GameboyAddress


def parse_dict_seasons(rom: RomData, seasons: bool):
    if seasons:
        base_address = text_table_eng_address_seasons
        text_offset_1 = GameboyAddress(rom.read_byte(text_offset_1_table_address_seasons), rom.read_word(text_offset_1_table_address_seasons + 1))
    else:
        base_address = text_table_eng_address_ages
        text_offset_1 = GameboyAddress(rom.read_byte(text_offset_1_table_address_ages), rom.read_word(text_offset_1_table_address_seasons + 1))
    dict_entries_offset = rom.read_word(base_address)

    base_address += dict_entries_offset
    text_offset_1_address = text_offset_1.address_in_rom()

    dict_seasons = {}
    for i in range(0x400):
        entry_address = text_offset_1_address + rom.read_word(base_address)
        base_address += 2

        dict_seasons[f"DICT{i // 0x100}_{simple_hex(i % 0x100)}"] = decode_text(rom, entry_address)

    return dict_seasons


def parse_all_texts(rom: RomData, dictionary: dict[str, str], seasons: bool):
    if seasons:
        text_offset_1 = GameboyAddress(rom.read_byte(text_offset_1_table_address_seasons), rom.read_word(text_offset_1_table_address_seasons + 1))
        text_offset_2 = GameboyAddress(rom.read_byte(text_offset_2_table_address_seasons), rom.read_word(text_offset_2_table_address_seasons + 1))
        base_address = text_table_eng_address_seasons
        text_offset_split_index = text_offset_split_index_seasons
    else:
        text_offset_1 = GameboyAddress(rom.read_byte(text_offset_1_table_address_ages), rom.read_word(text_offset_1_table_address_seasons + 1))
        text_offset_2 = GameboyAddress(rom.read_byte(text_offset_2_table_address_ages), rom.read_word(text_offset_2_table_address_seasons + 1))
        base_address = text_table_eng_address_ages
        text_offset_split_index = text_offset_split_index_ages

    text_offset_1_address = text_offset_1.address_in_rom()
    text_offset_2_address = text_offset_2.address_in_rom()
    current_offset_address = base_address + 8
    prev_offset = rom.read_word(current_offset_address)
    current_offset_address += 2
    prev_index = 4
    texts_season = {}
    for i in range(5, 0x61):
        if i == 0x60:
            offset = text_offset_1_address - base_address
        else:
            offset = rom.read_word(current_offset_address)
            current_offset_address += 2
        if offset <= prev_offset:
            continue
        if prev_index < text_offset_split_index:
            base_text_offset = text_offset_1_address
        else:
            base_text_offset = text_offset_2_address
        for j in range(0, (offset - prev_offset) // 2):
            text_offset = rom.read_word(base_address + prev_offset + j * 2)
            texts_season[f"TX_{simple_hex(prev_index - 4)}{simple_hex(j)}"] = (
                decode_text(rom, base_text_offset + text_offset, dictionary))
        prev_offset = offset
        prev_index = i
    return texts_season


def decode_text(rom: RomData, entry_address: int, dictionary: Optional[dict[str, str]] = None) -> str:
    text = ""
    while True:
        character = rom.read_byte(entry_address)
        entry_address += 1
        converted = char_table[character]
        if converted != "🚫":
            text += converted
        else:
            if character == 0x00:
                break
            character2 = rom.read_byte(entry_address)
            entry_address += 1
            if character < 0x06:
                text += dictionary[f"DICT{character - 2}_{simple_hex(character2)}"]
            elif character == 0x06:
                text += kanji_table[character2]  # Only the music note, triforce icon and trade items are used in EN in the kanji part
            elif character == 0x07:
                text += f"\\jump({simple_hex(character2)})"
                break
            elif character == 0x08:
                text += f"\\cmd({simple_hex(character2)})"
            elif character == 0x09:
                if character2 == 0:
                    text += "⬜"
                elif character2 == 1:
                    text += "🟥"
                elif character2 == 2:
                    text += "🟧"
                elif character2 == 3:
                    text += "🟦"
                elif character2 == 4:
                    text += "🟩"
                else:
                    text += f"\\col({simple_hex(character2)})"
            elif character == 0x0a:
                if character2 == 0:
                    text += "\\link_name"
                elif character2 == 1:
                    text += "\\child_name"
                elif character2 == 2:
                    text += "\\w7SecretBuffer1"
                elif character2 == 3:
                    text += "\\w7SecretBuffer2"
            elif character == 0x0b:
                text += f"\\charsfx({simple_hex(character2)})"
            elif character == 0x0c:
                argument = character2 & 3
                command = character2 >> 3
                if command == 0:
                    text += f"\\speed({simple_hex(argument)})"
                elif command == 1:
                    text += "\\num1"
                elif command == 2:
                    text += "\\opt"
                elif command == 3:
                    text += "\\stop"
                elif command == 4:
                    text += f"\\pos({simple_hex(argument)})"
                elif command == 5:
                    text += "\\heartpiece"
                elif command == 6:
                    text += "\\num2"
                elif command == 7:
                    text += "\\slow"
            elif character == 0x0d:
                text += f"\\wait({simple_hex(character2)})"
            elif character == 0x0e:
                text += f"\\sfx({simple_hex(character2)})"
            elif character == 0x0f:
                # A bit too complex to parse rn
                # if character2 >= 0xfc:
                #    argument = (~character2) & 3
                #    text += f"\\call(wTextSubstitutions+{argument})"
                # else:
                text += f"\\call({simple_hex(character2)})"
            elif character == 0xb8:
                # Two parts A button
                assert character2 == 0xb9
                text += "Ⓐ"
            elif character == 0xba:
                assert character2 == 0xbb
                text += "Ⓑ"
    return text


def fetch_data(rom: RomData, category_id: int, text_id: int, length: int, text_offset_1_address: int, text_offset_2_address: int) -> list[int]:
    address = text_table_eng_address_seasons + category_id * 2
    address = rom.read_word(address) + text_table_eng_address_seasons + text_id * 2
    address = rom.read_word(address)
    if category_id < text_offset_split_index_seasons:
        address += text_offset_1_address
    else:
        address += text_offset_2_address
    return list(rom.read_bytes(address, length))
