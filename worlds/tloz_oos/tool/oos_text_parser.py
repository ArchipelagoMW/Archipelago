import json
import os

from settings import get_settings
from worlds.tloz_oos.patching.RomData import RomData
from worlds.tloz_oos.patching.text.decoding import parse_dict_seasons, parse_all_texts, decode_text
from worlds.tloz_oos.patching.text.encoding import write_text_data, encode_dict

if __name__ == "__main__":
    if not os.path.isdir("output"):
        os.mkdir("output")
    file_name = get_settings()["tloz_oos_options"]["rom_file"]
    rom = RomData(bytes(open(file_name, "rb").read()))
    dict_seasons = parse_dict_seasons(rom, True)
    text = parse_all_texts(rom, dict_seasons, True)

    with open("output/seasons_text_dict.json", "w+", encoding="utf-8") as f:
        json.dump(dict_seasons, f, ensure_ascii=False, indent=4)

    with open("output/seasons_text.json", "w+", encoding="utf-8") as f:
        json.dump(text, f, ensure_ascii=False, indent=4)

    encoded_dict1 = encode_dict(dict_seasons)
    for key in dict_seasons:
        fake_rom = RomData(encoded_dict1[key])
        assert decode_text(fake_rom, 0) == dict_seasons[key], (decode_text(fake_rom, 0), dict_seasons[0])

    encoded_dict2 = encode_dict(text, dict_seasons)
    for key in text:
        fake_rom = RomData(encoded_dict2[key])
        assert decode_text(fake_rom, 0, dict_seasons) == text[key], (decode_text(fake_rom, 0, dict_seasons), text[key])

    write_text_data(rom, dict_seasons, text)

    dict_seasons2 = parse_dict_seasons(rom)

    for key in dict_seasons:
        assert dict_seasons2[key] == dict_seasons[key], (dict_seasons2[key], dict_seasons[key])

    text2 = parse_all_texts(rom, dict_seasons2)

    for key in text2:
        assert text2[key] == text[key], (text2[key], text[key])