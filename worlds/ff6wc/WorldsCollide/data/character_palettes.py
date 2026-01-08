from ..data.character_palette import CharacterPalette
from ..data.structures import DataArray
import pkgutil

SPRITE_PALETTE_COUNT = 7
DEFAULT_CHARACTER_PALETTES = list(range(SPRITE_PALETTE_COUNT))
DEFAULT_CHARACTER_SPRITE_PALETTES = [2, 1, 4, 4, 0, 0, 0, 3, 3, 4, 5, 3, 3, 5, 1, 0, 6, 1, 0, 3]


class CharacterPalettes:
    # field/battle palette color data
    FIELD_DATA_START = 0x268000
    FIELD_DATA_END = 0x2683ff
    FIELD_DATA_SIZE = 32

    BATTLE_DATA_START = 0x2d6300
    BATTLE_DATA_END = 0x2d63ff
    BATTLE_DATA_SIZE = 32

    # battle palette ids data
    BATTLE_ID_DATA_START = 0x2ce2b
    BATTLE_ID_DATA_END = 0x2ce40
    BATTLE_ID_DATA_SIZE = 1

    PORTRAIT_DATA_START = 0x2d5860
    PORTRAIT_DATA_END = 0x2d5abf
    PORTRAIT_DATA_SIZE = 32

    # default palette ids for sprites <= kefka (banon's palette for banon/duncan)
    DEFAULTS = [2, 1, 4, 4, 0, 0, 0, 3, 3, 4, 5, 3, 3, 5, 1, 0, 0, 3, 6, 1, 0, 3]

    def __init__(self, rom, args, menu_character_sprites):
        self.rom = rom
        self.args = args
        self.menu_character_sprites = menu_character_sprites

        self.field_palette_data = DataArray(self.rom, self.FIELD_DATA_START, self.FIELD_DATA_END, self.FIELD_DATA_SIZE)
        self.battle_palette_data = DataArray(self.rom, self.BATTLE_DATA_START, self.BATTLE_DATA_END,
                                             self.BATTLE_DATA_SIZE)
        self.portrait_palette_data = DataArray(self.rom, self.PORTRAIT_DATA_START, self.PORTRAIT_DATA_END,
                                               self.PORTRAIT_DATA_SIZE)

        self.field_palettes = []
        for field_palette_index in range(len(self.field_palette_data)):
            field_palette = CharacterPalette(field_palette_index, self.field_palette_data[field_palette_index])
            self.field_palettes.append(field_palette)

        self.battle_palettes = []
        for battle_palette_index in range(len(self.battle_palette_data)):
            battle_palette = CharacterPalette(battle_palette_index, self.battle_palette_data[battle_palette_index])
            self.battle_palettes.append(battle_palette)

        self.portrait_palettes = []
        for portrait_palette_index in range(len(self.portrait_palette_data)):
            portrait_palette = CharacterPalette(portrait_palette_index,
                                                self.portrait_palette_data[portrait_palette_index])
            self.portrait_palettes.append(portrait_palette)

        battle_palette_id_count = self.BATTLE_ID_DATA_END - self.BATTLE_ID_DATA_START + 1
        self.battle_palette_ids = self.rom.get_bytes(self.BATTLE_ID_DATA_START, battle_palette_id_count)

    def get(self, character_id):
        return self.battle_palette_ids[character_id]

    def mod_palette_colors(self):
        modified = [False] * len(self.args.palette_files)
        for palette_index, palette_id, in enumerate(self.args.palette_ids):
            if palette_id != DEFAULT_CHARACTER_PALETTES[palette_index]:
                modified[palette_index] = True

        # palette 6 is different between field and battles (field palette 8 corresponds to battle palette 6)
        # npcs only have 3 bits for palettes so cannot set their palette >= 8 (except maybe individually in event code)
        # setting field palette 6 to battle palette 6 will change various npcs (most noticably save points)
        # need to check if any other sprites were changed to use palette 6 so the change happens in both field/battle
        EXTRA_PALETTE = 6  # extra palette available to users for esper terra/npcs which differs between field/battle
        for sprite_index, palette_index in enumerate(self.args.sprite_palettes):
            if palette_index == EXTRA_PALETTE and DEFAULT_CHARACTER_SPRITE_PALETTES[sprite_index] != EXTRA_PALETTE:
                modified[palette_index] = True

        for palette_index, palette_file in enumerate(self.args.palette_files):
            if modified[palette_index]:
                from ..graphics.palettes.palettes import get_palette_data
                palette_data = list(get_palette_data(palette_file))

                self.field_palettes[palette_index].data = palette_data
                self.battle_palettes[palette_index].data = palette_data

    def mod_character_palettes(self):
        from ..data.character_sprites import SPRITE_CHARACTERS
        from ..sprite_hash import HASH_CHARACTERS

        # NOTE: palettes >= 6 do not work in menus and should not be used for main characters
        for index, palette_id in enumerate(self.args.sprite_palettes):
            character = SPRITE_CHARACTERS[index]

            self.battle_palette_ids[character] = palette_id

            if character not in HASH_CHARACTERS:
                # sprite hash displayed on save/load menu replaces some characters which will no longer
                # appear in save/load/shop/coliseum/party select menus so skip them
                self.menu_character_sprites.set_palette(character, palette_id)

    def mod_portrait_palettes(self):
        from ..data.character_sprites import PORTRAIT_CHARACTERS, DEFAULT_CHARACTER_PORTRAITS

        for index, portrait_palette_file in enumerate(self.args.portrait_palette_files):
            if self.args.portrait_ids[index] != DEFAULT_CHARACTER_PORTRAITS[index]:
                character = PORTRAIT_CHARACTERS[index]
                from ..graphics.portraits.portraits import get_portrait_data
                palette_data = list(get_portrait_data(portrait_palette_file))
                self.portrait_palettes[character].data = palette_data

    def mod(self):
        if self.args.character_palettes or self.args.character_sprite_palettes:
            self.mod_palette_colors()

        if self.args.character_sprite_palettes:
            self.mod_character_palettes()

        if self.args.character_portraits:
            self.mod_portrait_palettes()

    def write(self):
        for field_palette_index in range(len(self.field_palettes)):
            self.field_palette_data[field_palette_index] = self.field_palettes[field_palette_index].data
        self.field_palette_data.write()

        for battle_palette_index in range(len(self.battle_palettes)):
            self.battle_palette_data[battle_palette_index] = self.battle_palettes[battle_palette_index].data
        self.battle_palette_data.write()

        self.rom.set_bytes(self.BATTLE_ID_DATA_START, self.battle_palette_ids)

        for portrait_palette_index in range(len(self.portrait_palettes)):
            self.portrait_palette_data[portrait_palette_index] = self.portrait_palettes[portrait_palette_index].data
        self.portrait_palette_data.write()
