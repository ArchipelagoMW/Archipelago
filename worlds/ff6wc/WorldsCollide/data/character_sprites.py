import pkgutil

from ..data.character_sprite import CharacterSprite
from ..data.structures import DataArray
from ..constants.entities import id_character, name_id

# portrait args are for characters + imp
PORTRAIT_CHARACTERS = list(id_character) + [name_id["Imp"]]

# sprite args are for characters + soldier/imp/esper terra/merchant/ghost/kefka (args do not include leo/banon)
SPRITE_CHARACTERS = list(id_character)
SPRITE_CHARACTERS += [name_id[x] for x in ["Soldier", "Imp", "Esper Terra", "Merchant", "Ghost", "Kefka"]]

DEFAULT_CHARACTER_PORTRAITS = list(range(len(PORTRAIT_CHARACTERS)))
DEFAULT_CHARACTER_SPRITES = list(range(len(SPRITE_CHARACTERS)))


class CharacterSprites:
    # main characters (terra through umaro) + soldier + imp
    DATA_START = 0x150000
    DATA_END = 0x1669ff
    DATA_SIZE = 5792

    # general leo, banon/duncan, esper terra, merchant, ghost, kefka
    OTHER_DATA_START = 0x166a00
    OTHER_DATA_END = 0x16ea3f
    OTHER_DATA_SIZE = 5472

    PORTRAIT_DATA_START = 0x2d1d00
    PORTRAIT_DATA_END = 0x2d585f
    PORTRAIT_DATA_SIZE = 800

    def __init__(self, rom, args):
        self.rom = rom
        self.args = args

        self.character_sprite_data = DataArray(self.rom, self.DATA_START, self.DATA_END, self.DATA_SIZE)
        self.other_sprite_data = DataArray(self.rom, self.OTHER_DATA_START, self.OTHER_DATA_END, self.OTHER_DATA_SIZE)
        self.portrait_sprite_data = DataArray(self.rom, self.PORTRAIT_DATA_START, self.PORTRAIT_DATA_END,
                                              self.PORTRAIT_DATA_SIZE)

        self.sprites = []
        self.character_sprites = []
        for character_sprite_index in range(len(self.character_sprite_data)):
            character_sprite = CharacterSprite(character_sprite_index,
                                               self.character_sprite_data[character_sprite_index])
            self.character_sprites.append(character_sprite)
            self.sprites.append(character_sprite)

        self.other_sprites = []
        for other_sprite_index in range(len(self.other_sprite_data)):
            other_sprite = CharacterSprite(other_sprite_index, self.other_sprite_data[other_sprite_index])
            self.other_sprites.append(other_sprite)
            self.sprites.append(other_sprite)

        self.portrait_sprites = []
        for portrait_sprite_index in range(len(self.portrait_sprite_data)):
            portrait_sprite = CharacterSprite(portrait_sprite_index, self.portrait_sprite_data[portrait_sprite_index])
            self.portrait_sprites.append(portrait_sprite)

    def mod_character_sprites(self):
        for sprite_index, sprite_file in enumerate(self.args.sprite_files):
            character = SPRITE_CHARACTERS[sprite_index]

            if self.args.sprite_ids[sprite_index] != character:
                from ..graphics.sprites.sprites import get_sprite_data
                sprite_data = list(get_sprite_data(sprite_file))

                if len(sprite_data) < len(self.sprites[character].data):
                    # if sprite file does not contain every tile (e.g. missing poses) of sprite it is replacing, pad it with zeros
                    # this will cause the character to go invisible for these poses in-game but does not seem to break anything
                    padding = [0] * (len(self.sprites[character].data) - len(sprite_data))
                    sprite_data += padding
                elif len(sprite_data) > len(self.sprites[character].data):
                    # sprite has more tile information than the original requires, extract only the needed tiles
                    sprite_data = sprite_data[: len(self.sprites[character].data)]

                self.sprites[character].data = sprite_data

    def mod_character_portraits(self):
        for index, portrait_sprite_file in enumerate(self.args.portrait_sprite_files):
            if self.args.portrait_ids[index] != DEFAULT_CHARACTER_PORTRAITS[index]:
                character = PORTRAIT_CHARACTERS[index]

                from ..graphics.portraits.portraits import get_portrait_data
                portrait_data = list(get_portrait_data(portrait_sprite_file))
                self.portrait_sprites[character].data = portrait_data

    def mod(self):
        if self.args.character_sprites:
            self.mod_character_sprites()

        if self.args.character_portraits:
            self.mod_character_portraits()

    def write(self):
        for character_sprite_index in range(len(self.character_sprites)):
            self.character_sprite_data[character_sprite_index] = self.character_sprites[character_sprite_index].data
        self.character_sprite_data.write()

        for other_sprite_index in range(len(self.other_sprites)):
            self.other_sprite_data[other_sprite_index] = self.other_sprites[other_sprite_index].data
        self.other_sprite_data.write()

        for portrait_sprite_index in range(len(self.portrait_sprites)):
            self.portrait_sprite_data[portrait_sprite_index] = self.portrait_sprites[portrait_sprite_index].data
        self.portrait_sprite_data.write()
