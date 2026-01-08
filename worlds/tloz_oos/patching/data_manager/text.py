import json
from pathlib import Path

from typing_extensions import Any

import Utils
from worlds.tloz_oos.patching.RomData import RomData
from worlds.tloz_oos.patching.text import normalize_text
from worlds.tloz_oos.patching.text.decoding import parse_dict_seasons, parse_all_texts


def load_modded_seasons_text_data() -> None | tuple[dict[str, str], dict[str, str]]:
    from worlds.tloz_oos import OracleOfSeasonsWorld
    text_dir = Path(Utils.cache_path("oos_ooa/text"))
    dict_file = text_dir.joinpath(f"seasons_dict.json")
    if not dict_file.is_file():
        return None

    text_file = text_dir.joinpath(f"seasons_texts.json")
    if text_file.is_file():
        texts: dict[str, Any] = json.load(open(text_file, encoding="utf-8"))
        version = texts.pop("version")
        if version == OracleOfSeasonsWorld.version():
            return json.load(open(dict_file, encoding="utf-8")), texts

    vanilla_text_file = text_dir.joinpath(f"seasons_texts_vanilla.json")
    if not vanilla_text_file.is_file():
        return None
    texts = json.load(open(vanilla_text_file, encoding="utf-8"))
    apply_text_edits(texts)
    save_edited_text_data(texts)
    return json.load(open(dict_file, encoding="utf-8")), texts


def save_vanilla_text_data(dictionary: dict[str, str],
                           texts: dict[str, str],
                           seasons: bool = True) -> None:
    text_dir = Path(Utils.cache_path("oos_ooa/text"))
    text_dir.mkdir(parents=True, exist_ok=True)

    game_name = "seasons" if seasons else "ages"
    dict_file = text_dir.joinpath(f"{game_name}_dict.json")
    text_file = text_dir.joinpath(f"{game_name}_texts_vanilla.json")

    with dict_file.open("w", encoding="utf-8") as f:
        json.dump(dictionary, f, ensure_ascii=False)

    with text_file.open("w", encoding="utf-8") as f:
        json.dump(texts, f, ensure_ascii=False)


def save_edited_text_data(texts: dict[str, str]) -> None:
    from worlds.tloz_oos import OracleOfSeasonsWorld
    texts["version"] = OracleOfSeasonsWorld.version()

    text_dir = Path(Utils.cache_path("oos_ooa/text"))
    text_file = text_dir.joinpath(f"seasons_texts.json")

    with text_file.open("w", encoding="utf-8") as f:
        json.dump(texts, f, ensure_ascii=False)

    del texts["version"]


def apply_text_edits(texts: dict[str, str]) -> None:
    # New items
    # Replace ring box 1
    texts["TX_0034"] = ("You got 🟥Ember\n"
                        "Seeds⬜! Open\n"
                        "your 🟥Seed\n"
                        "Satchel⬜ to use\n"
                        "them.")
    # Replace ring box 1 unused text
    texts["TX_0057"] = ("You found an\n"
                        "item for another\n"
                        "world!")
    # Replace ring box 2 unused text
    texts["TX_0058"] = ("You got 🟥25\n"
                        "Ore Chunks⬜!")

    # Brand-new texts, for 20 bombs
    texts["TX_0094"] = texts["TX_004d"].replace("ten", "twenty")

    # Trade items
    # Cuccodex is fine
    texts["TX_005b"] = ("You got a\n"
                        "\\col(84)🥚🟥 Lon Lon Egg⬜!\n"
                        "It's a\n"
                        "beauty aid?!?")
    texts["TX_005c"] = ("You got a\n"
                        "\\col(84)🎎🟥 Ghastly Doll⬜!\n"
                        "Looking at it\n"
                        "gives you\n"
                        "chills!")
    texts["TX_005d"] = ("You got an\n"
                        "\\col(84)⚗🟥 Iron Pot⬜.\n"
                        "It looks...\n"
                        "well-seasoned.")
    # Soup is fine
    texts["TX_005f"] = ("You got the\n"
                        "\\col(84)🏺🟥 Goron Vase⬜!\n"
                        "It's a very\n"
                        "nice vase...")
    texts["TX_0060"] = ("You got a\n"
                        "\\col(84)🐟🟥 Fish⬜! It's\n"
                        "market fresh!")
    texts["TX_0061"] = ("You got a\n"
                        "\\col(84)📢🟥 Megaphone⬜!\n"
                        "Give a shout!")
    texts["TX_0062"] = ("You got a\n"
                        "\\col(84)🍄🟥 Mushroom⬜!\n"
                        "It smells weird.")
    texts["TX_0063"] = ("You got a\n"
                        "\\col(84)🐦🟥 Wooden Bird⬜!\n"
                        "It looks real!")
    texts["TX_0064"] = ("You got\n"
                        "\\col(84)🛢🟥 Engine Grease⬜.")
    texts["TX_0065"] = ("You got a\n"
                        "\\col(84)📻🟥 Phonograph⬜!\n"
                        "What a tune!")

    # Appraisal text
    texts["TX_301c"] = ("You got the\n"
                        "\\call(fd)!")

    # Cross items
    # Obtain text
    texts["TX_003b"] = ("You got the\n"
                        "🟥Switch Hook⬜!\n"
                        "Shoot at an\n"
                        "object to switch\n"
                        "places with it.\n")  # Strange flute
    texts["TX_0051"] = ("You got the 🟥Long\n"
                        "Switch⬜! Switch\n"
                        "places with\n"
                        "objects from a\n"
                        "distance.")  # Warrior child heart
    texts["TX_0053"] = ("You got the\n"
                        "🟥Cane of Somaria⬜!\n"
                        "Use it to create\n"
                        "blocks.")  # Warrior child heart refill
    texts["TX_0054"] = ("You got the\n"
                        "🟥Seed Shooter⬜!\n"
                        "Pick your 🟥seeds⬜,\n"
                        "fire, then watch\n"
                        "them ricochet.")  # Unappraised ring
    texts["TX_091d"] = ("Cane of Somaria\n"
                        "Used to create\n"
                        "blocks.")  # Replaces ring box 1
    texts["TX_091e"] = ("Switch Hook\n"
                        "User and target\n"
                        "trade places.")  # Replaces ring box 2
    texts["TX_0917"] = ("Long Hook\n"
                        "Switches places\n"
                        "from a distance.")  # Replaces unappraised ring
    texts["TX_092e"] = ("Seed Shooter\n"
                        "Used to bounce\n"
                        "seeds around.")  # Replaces strange flute
    # Note: 3 other seemingly unused seeds follow

    # Map stuff, replaces the group 05 since it's all linked game dialogues
    texts["TX_0500"] = "Unknown Portal"
    texts["TX_0501"] = normalize_text("Portal to Eastern Suburbs")
    texts["TX_0502"] = normalize_text("Portal to Spool Swamp")
    texts["TX_0503"] = normalize_text("Portal to Mt. Cucco")
    texts["TX_0504"] = normalize_text("Portal to Eyeglass Lake")
    texts["TX_0505"] = normalize_text("Portal to Horon Village")
    texts["TX_0506"] = normalize_text("Portal to Temple Remains")
    texts["TX_0507"] = normalize_text("Portal to Temple Summit")
    texts["TX_0508"] = normalize_text("Portal to Subrosian Village")
    texts["TX_0509"] = normalize_text("Portal to Subrosian Market")
    texts["TX_050a"] = normalize_text("Portal to Subrosian Wilds")
    texts["TX_050b"] = normalize_text("Portal to Great Furnace")
    texts["TX_050c"] = normalize_text("Portal to House of Pirates")
    texts["TX_050d"] = normalize_text("Portal to Subrosian Volcanoes")
    texts["TX_050e"] = normalize_text("Portal to Subrosian Dungeon")

    # Reword the natzu deku to omit the secret and the full satchel
    texts["TX_4c43"] = ("\\sfx(c6)Come back\n"
                        "with all five\n"
                        "kinds of 🟥seeds⬜!")

    # Remove the mention of 777 ore chunks
    unlucky_text: str = texts["TX_3a2f"]
    index_777 = unlucky_text.index(" Get")
    texts["TX_3a2f"] = unlucky_text[:index_777]

    # Replace the shield selling part of dekus which will never be used
    texts["TX_450a"] = ("\\sfx(c6)Greetings!\n"
                        "I can refill\n"
                        "your bag for\n"
                        "🟩30 Rupees⬜ only.\n"
                        "  \\optOK \\optNo thanks")

    # Impa refills
    texts["TX_2503"] = ("Come see me if\n"
                        "you need a\n"
                        "refill!")
    # Change D8 introduction text to “Sword & Shield Dungeon” from “Sword & Shield Maze”,
    # since every other mention of it was using “Dungeon” naming
    texts["TX_0208"] = texts["TX_0208"].replace("Maze", "Dungeon")

    # Now unused text from Maku talking
    texts["TX_1700"] = texts["TX_1701"] = ""

    texts["TX_0602"] = "Unknown Dungeon"


def get_text_data(rom_data: RomData, seasons: bool = True) -> tuple[dict[str, str], dict[str, str]]:
    result = load_modded_seasons_text_data()
    if result is not None:
        return result

    dictionary = parse_dict_seasons(rom_data, seasons)
    texts = parse_all_texts(rom_data, dictionary, seasons)
    save_vanilla_text_data(dictionary, texts, texts)
    apply_text_edits(texts)
    save_edited_text_data(texts)
    return dictionary, texts
