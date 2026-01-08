from typing import List, Any

from .Constants import NUM_CUSTOM

NUM_CUSTOM = NUM_CUSTOM

character_list: List[str] = [
    "Ironclad",
    "Silent",
    "Defect",
    "Watcher",
    "Hermit",
    "SlimeBoss",
    "Guardian",
    "Hexaghost",
    "Champ",
    "Gremlins",
    "Automaton",
    "Snecko",
    "Collector",
]

official_names: List[str] = [
    "IRONCLAD",
    "THE_SILENT",
    "DEFECT",
    "WATCHER",
    "HERMIT",
    "SLIMEBOUND",
    "GUARDIAN",
    "THE_SPIRIT",
    "THE_CHAMP",
    "GREMLIN",
    "THE_AUTOMATON",
    "THE_SNECKO",
    "THE_COLLECTOR",
]

# character_option_map = {
#     value: key.lower()
#     for key, value in Character.options.items()
# }

character_offset_map = {
    name.lower(): i
    for i, name in enumerate(character_list)
}

for i, name in enumerate(official_names):
    character_offset_map[name.lower()] = i

class CharacterConfig:
    # name: str
    # option_name: str
    # official_name: str
    # char_offset: int
    # mod_num: int
    # ascension: int
    # final_act: bool
    # downfall: bool

    def __init__(self, name: str, option_name: str, char_offset: int, mod_num: int, seed: str, locked: bool, **kwargs):
        self.name: str = name
        self.option_name: str = option_name
        self.char_offset: int = char_offset
        self.mod_num: int = mod_num
        if self.mod_num > 0:
            self.official_name: str = self.option_name
        else:
            self.official_name: str = official_names[char_offset]
        self.seed: str = seed
        self.locked = locked
        self.ascension: int = kwargs['ascension']
        self.final_act: int = kwargs['final_act']
        self.downfall: int = kwargs['downfall']
        self.ascension_down: int = kwargs['ascension_down']

    def to_dict(self) -> dict[str, Any]:
        return {
            'name': self.name,
            'option_name': self.option_name,
            'char_offset': self.char_offset,
            'official_name': self.official_name,
            'seed': self.seed,
            'locked': self.locked,
            'mod_num': self.mod_num,
            'ascension': self.ascension,
            'final_act': self.final_act != 0,
            'downfall': self.downfall != 0,
            'ascension_down': self.ascension_down,
        }

    def __repr__(self):
        return self.to_dict().__repr__()
