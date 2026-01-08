from ..data.menu_character_sprite import MenuCharacterSprite
from ..data.structures import DataArray, DataPointers

# each menu sprite contains data about a pose and how to draw it
# for the main playable characters (0-13) the menu sprite data alternates betwen standing and hands up (both left facing)
#   these are alternated to play the victory fanfare animation (e.g. when a character can equip something in a shop)
# for the other characters (soldier, imp, leo, banon, esper terra, merchant, ghost, kefka) there is only data for the standing pose

class MenuCharacterSprites:
    # data size can vary but all menu character sprites are 2 tiles (1 byte tile count + 4 bytes OAM data for each)
    OAM_DATA_START = 0x18ea5c
    OAM_DATA_END = 0x18eba8
    OAM_DATA_SIZE = 9

    SPRITE_PTRS_START = 0xff911
    SPRITE_PTRS_END = 0xff968
    SPRITE_PTR_SIZE = 4 # 3 bytes would have been enough

    def __init__(self, rom, args):
        self.rom = rom
        self.args = args

        self.oam_data = DataArray(self.rom, self.OAM_DATA_START, self.OAM_DATA_END, self.OAM_DATA_SIZE)
        self.sprite_pointers = DataPointers(self.rom, self.SPRITE_PTRS_START, self.SPRITE_PTRS_END, self.SPRITE_PTR_SIZE)

        self.sprites = []
        for sprite_index in range(len(self.oam_data)):
            menu_sprite = MenuCharacterSprite(sprite_index, self.oam_data[sprite_index])
            self.sprites.append(menu_sprite)

        from ..data.characters import Characters

        self.standing_sprites = []
        for sprite_index in range(Characters.CHARACTER_COUNT):
            self.standing_sprites.append(self.sprites[sprite_index * 2])
        for sprite_index in range(Characters.CHARACTER_COUNT * 2, len(self.sprites)):
            self.standing_sprites.append(self.sprites[sprite_index])

        self.victory_sprites = []
        for sprite_index in range(1, Characters.CHARACTER_COUNT * 2, 2):
            self.victory_sprites.append(self.sprites[sprite_index])

    def set_sprite_address(self, character_id, address):
        self.sprite_pointers[character_id] = address

    def set_palette(self, character_id, palette_id):
        palette_id += 2 # convert given palette index to menu palette index

        self.standing_sprites[character_id].set_palette(palette_id)

        from ..data.characters import Characters
        if character_id < Characters.CHARACTER_COUNT:
            self.victory_sprites[character_id].set_palette(palette_id)

    def write(self):
        self.sprite_pointers.write()

        for sprite_index in range(len(self.sprites)):
            self.oam_data[sprite_index] = self.sprites[sprite_index].oam_data()
        self.oam_data.write()
