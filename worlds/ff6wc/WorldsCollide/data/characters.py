from ..data.character import Character
from ..data.natural_magic import NaturalMagic
from ..data.commands import Commands
from ..data.menu_character_sprites import MenuCharacterSprites
from ..data.character_sprites import CharacterSprites
from ..data.character_palettes import CharacterPalettes
from ..data.party_battle_scripts import PartyBattleScripts
from ..data.structures import DataArray

from ..data import characters_asm as characters_asm

class Characters():
    CHARACTER_COUNT = 14   # 14 playable characters
    TERRA, LOCKE, CYAN, SHADOW, EDGAR, SABIN, CELES, STRAGO, RELM, SETZER, MOG, GAU, GOGO, UMARO = range(CHARACTER_COUNT)
    SOLDIER, IMP, GENERAL_LEO, BANON_DUNCAN, ESPER_TERRA, MERCHANT, GHOST, KEFKA = range(CHARACTER_COUNT, 22)

    # Moogle character indexes
    FIRST_MOOGLE = 0x12
    LAST_MOOGLE = 0x1B

    DEFAULT_NAME = ["TERRA", "LOCKE", "CYAN", "SHADOW", "EDGAR", "SABIN", "CELES", "STRAGO", "RELM", "SETZER", "MOG", "GAU", "GOGO", "UMARO"]

    INIT_DATA_START = 0x2d7ca0
    INIT_DATA_END = 0x2d821f
    INIT_DATA_SIZE = 22

    NAMES_START = 0x478c0
    NAMES_END = 0x47a3f
    NAME_SIZE = 6

    def __init__(self, rom, args, spells):
        self.rom = rom
        self.args = args

        self.init_data = DataArray(self.rom, self.INIT_DATA_START, self.INIT_DATA_END, self.INIT_DATA_SIZE)
        self.name_data = DataArray(self.rom, self.NAMES_START, self.NAMES_END, self.NAME_SIZE)

        self.characters = []
        for character_index in range(len(self.name_data)):
            character = Character(character_index, self.init_data[character_index], self.name_data[character_index])
            self.characters.append(character)

        self.playable = self.characters[:self.CHARACTER_COUNT]

        self.natural_magic = NaturalMagic(self.rom, self.args, self, spells)
        self.commands = Commands(self.characters)

        self.menu_character_sprites = MenuCharacterSprites(self.rom, self.args)
        self.character_sprites = CharacterSprites(self.rom, self.args)
        self.character_palettes = CharacterPalettes(self.rom, self.args, self.menu_character_sprites)

        self.battle_scripts = PartyBattleScripts(self.rom, self.args, self)

        self.available_characters = list(range(self.CHARACTER_COUNT))

        # path of characters required to unlock each character
        # e.g. self.character_paths[self.TERRA] = all characters required for terra (in order)
        self.character_paths = [[] for char_index in range(self.CHARACTER_COUNT)]

    def get_available_count(self):
        return len(self.available_characters)

    def set_unavailable(self, character):
        self.available_characters.remove(character)

    def get_random_available(self, exclude = None):
        if exclude is None:
            exclude = []

        import random
        possible_characters = [character_id for character_id in self.available_characters if character_id not in exclude]
        random_character = random.choice(possible_characters)
        self.set_unavailable(random_character)
        return random_character
    
    def get_specific_character(self, name):
        character = int(self.get_by_name(name).id)
        self.set_unavailable(character)
        return character

    def set_character_path(self, character, required_character):
        if required_character is not None:
            self.character_paths[character].extend(self.character_paths[required_character])
            self.character_paths[character].append(required_character)

    def get_character_path(self, character):
        return self.character_paths[character]

    def mod_init_levels(self):
        # remove all variation in leveling, since we're controlling level directly
        for character in self.characters:
            character.init_level_factor = 0

        characters_asm.set_starting_level(self.args.start_level)

    def stats_random_percent(self):
        import random
        stats = ["init_extra_hp", "init_extra_mp", "init_vigor", "init_speed", "init_stamina", "init_magic",
                 "init_attack", "init_defense", "init_magic_defense", "init_evasion", "init_magic_evasion"]
        for character in self.characters:
            for stat in stats:
                stat_value = getattr(character, stat)
                if stat_value != 0:
                    character_stat_percent = random.randint(self.args.character_stat_random_percent_min,
                                                            self.args.character_stat_random_percent_max) / 100.0
                    value = int(stat_value * character_stat_percent)
                    setattr(character, stat, max(min(value, 255), 0))

    def get_characters_with_command(self, command_name):
        from ..constants.commands import name_id
        command_id = name_id[command_name]

        result = []
        for character in self.characters:
            if command_id in character.commands:
                result.append(character.id)
        return result

    def mod_names(self):
        for character_id, name in enumerate(self.args.names):
            self.characters[character_id].name = name

    def mod(self):
        if self.args.start_naked:
            for char in self.characters:
                char.clear_init_equip()

        if self.args.equipable_umaro:
            characters_asm.equipable_umaro(self.CHARACTER_COUNT)

        self.mod_init_levels()

        if self.args.character_stat_random_percent:
            self.stats_random_percent()

        self.commands.mod()

        if self.args.character_names:
            self.mod_names()

        if self.args.original_name_display:
            characters_asm.show_original_names()

        self.natural_magic.mod()
        self.character_sprites.mod()
        self.character_palettes.mod()
        self.battle_scripts.mod()

    def write(self):
        if self.args.spoiler_log:
            self.commands.log()

        for character_index in range(len(self.characters)):
            self.init_data[character_index] = self.characters[character_index].init_data()
            self.name_data[character_index] = self.characters[character_index].name_data()

        self.init_data.write()
        self.name_data.write()

        self.natural_magic.write()

        self.menu_character_sprites.write()
        self.character_sprites.write()
        self.character_palettes.write()
        self.battle_scripts.write()

    def print_character_paths(self):
        for char_index in range(self.CHARACTER_COUNT):
            path = self.get_character_path(char_index)
            for req_char_index in path:
                print(f"{self.DEFAULT_NAME[req_char_index]} -> ", end = '')
            print(f"{self.DEFAULT_NAME[char_index]}")

    def print(self):
        for char in self.characters:
            char.print()

    def get(self, character):
        for char in self.characters:
            if char.id == character:
                return char

    def get_by_name(self, name):
        for char in self.characters:
            if self.DEFAULT_NAME[char.id].lower() == name.lower():
                return char

    def get_name(self, character):
        return self.characters[character].name.rstrip('\0')

    def get_default_name(self, character):
        return self.DEFAULT_NAME[character]

    def get_sprite(self, character):
        return self.character_sprites.character_sprites[character].id

    def get_random_esper_item_sprite(self):
        sprites = [self.SOLDIER, self.IMP, self.MERCHANT, self.GHOST]

        import random
        return sprites[random.randrange(len(sprites))]

    def get_palette(self, character):
        return self.character_palettes.get(character)
