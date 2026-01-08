from ..data import text as text
from ..data.text.text2 import text_value, value_text

class Item():
    NAME_LENGTH = 13
    NAMES_START_ADDR = 0x12b300

    DATA_SIZE = 30
    DATA_START_ADDR = 0x185000

    ITEM_TYPE_COUNT = 7
    TOOL, WEAPON, ARMOR, SHIELD, HELMET, RELIC, ITEM = range(ITEM_TYPE_COUNT)

    def __init__(self, id, rom, desc_data):
        self.rom = rom

        self.id = id
        self.name_addr = self.NAMES_START_ADDR + self.id * self.NAME_LENGTH
        self.data_addr = self.DATA_START_ADDR + self.id * self.DATA_SIZE
        self.desc_data = desc_data

        self.read()

    def is_equipable(self):
        return self.equipable_characters

    def equipable_by(self, character):
        char_bit = 0x01 << character.id
        return self.equipable_characters & char_bit

    def add_equipable_character(self, character):
        char_bit = 0x01 << character.id
        self.equipable_characters = self.equipable_characters | char_bit

    def remove_equipable_character(self, character):
        char_bit = 0x01 << character.id
        self.equipable_characters = self.equipable_characters & ~char_bit

    def remove_all_equipable_characters(self):
        self.equipable_characters = 0

    def remove_learnable_spell(self):
        self.learnable_spell = 0
        self.learnable_spell_rate = 0

    def get_desc_data(self):
        return text.get_bytes(self.desc, text.TEXT2)

    def scale_price(self, factor):
        self.price = int(self.price * factor)
        self.price = max(min(self.price, 2**16 - 1), 0)

    def read(self):
        name_bytes = self.rom.get_bytes(self.name_addr, self.NAME_LENGTH)
        self.icon = value_text[name_bytes[0]]
        self.name = text.get_string(name_bytes[1:], text.TEXT2).rstrip('\0')
        self.desc = text.get_string(self.desc_data, text.TEXT2).rstrip('\0')

        data = self.rom.get_bytes(self.data_addr, self.DATA_SIZE)
        self.type                   = data[0] & 0x07
        self.throwable              = (data[0] & 0x10) >> 4
        self.usable_in_battle       = (data[0] & 0x20) >> 5
        self.usable_in_menu         = (data[0] & 0x40) >> 6
        self.equipable_characters   = (data[1] & 0xff)
        self.equipable_characters  |= (data[2] & 0x3f) << 8
        self.imp_equipment          = (data[2] & 0x40) >> 6
        self.merit_awardable        = (data[2] & 0x80) >> 7
        self.learnable_spell_rate   = data[3]
        self.learnable_spell        = data[4]
        self.weapon_flag_unknown1   = (data[19] & 0x01) >> 0
        self.enable_swdtech         = (data[19] & 0x02) >> 1
        self.weapon_flag_unknown2   = (data[19] & 0x04) >> 2
        self.weapon_flag_unknown3   = (data[19] & 0x08) >> 3
        self.weapon_flag_unknown4   = (data[19] & 0x10) >> 4
        self.same_damage_back_row   = (data[19] & 0x20) >> 5
        self.allow_two_hands        = (data[19] & 0x40) >> 6
        self.enable_runic           = (data[19] & 0x80) >> 7
        self.price                  = int.from_bytes(data[28:30], "little")

    def write(self):
        name_bytes = [text_value[self.icon]]
        name_bytes += text.get_bytes(self.name, text.TEXT2)
        name_bytes += [text_value['\0']] * (self.NAME_LENGTH - len(name_bytes))
        self.rom.set_bytes(self.name_addr, name_bytes)

        data = [0x00] * self.DATA_SIZE

        data[1]     = (self.equipable_characters & 0x00ff)
        data[2]     = (self.equipable_characters & 0x3f00)  >> 8
        data[2]    |= self.imp_equipment                    << 6
        data[2]    |= self.merit_awardable                  << 7

        data[19]    = self.weapon_flag_unknown1             << 0
        data[19]   |= self.enable_swdtech                   << 1
        data[19]   |= self.weapon_flag_unknown2             << 2
        data[19]   |= self.weapon_flag_unknown3             << 3
        data[19]   |= self.weapon_flag_unknown4             << 4
        data[19]   |= self.same_damage_back_row             << 5
        data[19]   |= self.allow_two_hands                  << 6
        data[19]   |= self.enable_runic                     << 7

        self.rom.set_byte(self.data_addr + 1, data[1])
        self.rom.set_byte(self.data_addr + 2, data[2])
        self.rom.set_byte(self.data_addr + 3, self.learnable_spell_rate)
        self.rom.set_byte(self.data_addr + 4, self.learnable_spell)
        self.rom.set_byte(self.data_addr + 19, data[19])
        self.rom.set_short(self.data_addr + 28, self.price)

    def print(self):
        type_string = {self.TOOL : "TOOL", self.WEAPON : "WEAPON", self.ARMOR : "ARMOR",
                       self.SHIELD : "SHIELD", self.HELMET : "HELMET", self.RELIC : "RELIC", self.ITEM : "ITEM"}
        print("{}: {} {}: {} {}".format(self.id, self.name, type_string[self.type], hex(self.equipable_characters), self.price))
