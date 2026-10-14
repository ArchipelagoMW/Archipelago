import csv
from importlib.resources import files
from typing import Dict, List, NamedTuple, Optional


class SpellLevel(NamedTuple):
    index: int
    name: str
    sysmsg_index: int


def load_rows(file_name: str, encoding: Optional[str] = None) -> List[Dict[str, str]]:
    with files(__name__).joinpath(file_name).open(encoding=encoding) as file:
        return list(csv.DictReader(file))


def group_spell_levels_by_spell(rows: List[Dict[str, str]]) -> Dict[str, List[SpellLevel]]:
    levels_by_spell: Dict[str, List[SpellLevel]] = {}
    for index, row in enumerate(rows):
        level = SpellLevel(index, row["level"], int(row["sysmsg_index"]))
        levels_by_spell.setdefault(row["item"], []).append(level)
    return levels_by_spell


items = load_rows("items.csv")
event_items = load_rows("event_items.csv")
locations = load_rows("locations.csv")
event_locations = load_rows("event_locations.csv")

keyblade_stats = load_rows("keyblade_stats.csv")
ability_ap_costs = load_rows("ability_ap_costs.csv", "utf-8")
spells = load_rows("spells.csv")
level_up_stats = load_rows("level_up_stats.csv")

char_to_kh = load_rows("char_to_kh.csv", "utf-8")
item_help = load_rows("item_help.csv", "utf-8")
words = load_rows("words.csv", "utf-8")
system_messages = load_rows("system_messages.csv", "utf-8")

CHAR_TO_KH = {row["char"]: int(row["byte"], 16) for row in char_to_kh}
MP_COST_LABELS = {15: "0.5 CP", 30: "1 CP", 100: "1 MP", 200: "2 MP", 300: "3 MP"}
POSSIBLE_SPELL_COSTS = list(MP_COST_LABELS)

WORD = [row["text"] for row in words]
ITEMHELP = [row["text"] for row in item_help]
SYSMSG = [row["text"] for row in system_messages]

SPELL_LEVELS_BY_SPELL = group_spell_levels_by_spell(spells)
VANILLA_SPELL_LEVEL_COSTS = [int(row["vanilla_cost"]) for row in spells]
VANILLA_SPELL_COSTS = [30, 30, 100, 100, 100, 200, 200]
VANILLA_SPELL_EFFECTIVENESS = [int(row["vanilla_effectiveness"]) for row in spells]
VANILLA_LEVEL_UP_STATS = {int(row["level"]): row["item"] for row in level_up_stats}

CHEST_KEYBLADES = {
    "Destiny Islands": "Oathkeeper",
    "Traverse Town": "Lionheart",
    "Wonderland": "Lady Luck",
    "Olympus Coliseum": "Olympia",
    "Deep Jungle": "Jungle King",
    "Agrabah": "Three Wishes",
    "Monstro": "Wishing Star",
    "Atlantica": "Crabclaw",
    "Halloween Town": "Pumpkinhead",
    "Neverland": "Fairy Harp",
    "Hollow Bastion": "Divine Rose",
    "End of the World": "Oblivion",
    "100 Acre Wood": "Spellbinder",
}

WORLD_KEY_ITEMS = {
    "Footprints": "Wonderland",
    "Entry Pass": "Olympus Coliseum",
    "Slide 1": "Deep Jungle",
    "Crystal Trident": "Atlantica",
    "Forget-Me-Not": "Halloween Town",
    "Jack-In-The-Box": "Halloween Town",
    "Theon Vol. 6": "Hollow Bastion",
}
