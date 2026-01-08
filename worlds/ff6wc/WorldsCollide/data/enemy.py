from ..data import text as text
from ..data.status_effects import StatusEffects

class Enemy:
    def __init__(self, id, data, name_data, item_data, special_name_data):
        self.id = id
        self.name = text.get_string(name_data, text.TEXT2).rstrip('\0')

        self.speed              = data[0]
        self.vigor              = data[1]
        self.accuracy           = data[2]
        self.evasion            = data[3]
        self.magic_evasion      = data[4]
        self.defense            = data[5]
        self.magic_defense      = data[6]
        self.magic              = data[7]
        self.hp                 = int.from_bytes(data[8:10], "little")
        self.mp                 = int.from_bytes(data[10:12], "little")
        self.exp                = int.from_bytes(data[12:14], "little")
        self.gold               = int.from_bytes(data[14:16], "little")
        self.level              = data[16]

        self.metamorph_group    = (data[17] & 0x1f) >> 0
        self.metamorph_odds     = (data[17] & 0xe0) >> 5

        self.die_at_zero_mp     = (data[18] & 0x01) >> 0
        self.unknown1           = (data[18] & 0x02) >> 1
        self.no_name            = (data[18] & 0x04) >> 2
        self.unknown2           = (data[18] & 0x08) >> 3
        self.human              = (data[18] & 0x10) >> 4
        self.unknown3           = (data[18] & 0x20) >> 5
        self.criticals_if_imp   = (data[18] & 0x40) >> 6
        self.undead             = (data[18] & 0x80) >> 7

        self.hard_to_run        = (data[19] & 0x01) >> 0
        self.attack_first       = (data[19] & 0x02) >> 1
        self.no_suplex          = (data[19] & 0x04) >> 2
        self.no_run             = (data[19] & 0x08) >> 3
        self.no_scan            = (data[19] & 0x10) >> 4
        self.no_sketch          = (data[19] & 0x20) >> 5
        self.unknown4           = (data[19] & 0x40) >> 6
        self.no_control         = (data[19] & 0x80) >> 7

        status_effect_groups    = [StatusEffects.GROUP_A, StatusEffects.GROUP_B, StatusEffects.GROUP_C]
        self.status_immunities  = StatusEffects(status_effect_groups, data[20 : 23])

        self.absorb_elements    = data[23]
        self.immune_elements    = data[24]
        self.weak_elements      = data[25]

        self.attack_animation   = data[26]

        self.status_effects     = StatusEffects(status_effect_groups, data[27 : 30])

        self.true_knight        = (data[30] & 0x01) >> 0
        self.runic              = (data[30] & 0x02) >> 1
        self.life_3             = (data[30] & 0x04) >> 2
        self.unknown5           = (data[30] & 0x08) >> 3
        self.unknown6           = (data[30] & 0x10) >> 4
        self.unknown7           = (data[30] & 0x20) >> 5
        self.unknown8           = (data[30] & 0x40) >> 6
        self.float              = (data[30] & 0x80) >> 7

        self.special_effect     = (data[31] & 0x3f) >> 0
        self.special_no_damage  = (data[31] & 0x40) >> 6
        self.special_no_dodge   = (data[31] & 0x80) >> 7

        self.steal_rare         = item_data[0]
        self.steal_common       = item_data[1]
        self.drop_rare          = item_data[2]
        self.drop_common        = item_data[3]

        self.special_name       = text.get_string(special_name_data, text.TEXT2).rstrip('\0')

        # copy stats for reference after modifications
        self.original_speed         = self.speed
        self.original_vigor         = self.vigor
        self.original_accuracy      = self.accuracy
        self.original_evasion       = self.evasion
        self.original_magic_evasion = self.magic_evasion
        self.original_defense       = self.defense
        self.original_magic_defense = self.magic_defense
        self.original_magic         = self.magic
        self.original_hp            = self.hp
        self.original_mp            = self.mp
        self.original_exp           = self.exp
        self.original_gold          = self.gold
        self.original_level         = self.level

    def debug_mod(self):
        self.speed              = 1
        self.vigor              = 1
        self.accuracy           = 1
        self.evasion            = 1
        self.magic_evasion      = 1
        self.defense            = 1
        self.magic_defense      = 1
        self.magic              = 1
        self.hp                 = 1
        self.mp                 = 1
        self.level              = 1

        self.no_scan            = 0

    def data(self):
        from ..data.enemies import Enemies
        data = [0x00] * Enemies.DATA_SIZE

        data[0]     = self.speed
        data[1]     = self.vigor
        data[2]     = self.accuracy
        data[3]     = self.evasion
        data[4]     = self.magic_evasion
        data[5]     = self.defense
        data[6]     = self.magic_defense
        data[7]     = self.magic
        data[8:10]  = self.hp.to_bytes(2, "little")
        data[10:12] = self.mp.to_bytes(2, "little")
        data[12:14] = self.exp.to_bytes(2, "little")
        data[14:16] = self.gold.to_bytes(2, "little")
        data[16]    = self.level

        data[17]    = self.metamorph_group  << 0
        data[17]   |= self.metamorph_odds   << 5

        data[18]    = self.die_at_zero_mp   << 0
        data[18]   |= self.unknown1         << 1
        data[18]   |= self.no_name          << 2
        data[18]   |= self.unknown2         << 3
        data[18]   |= self.human            << 4
        data[18]   |= self.unknown3         << 5
        data[18]   |= self.criticals_if_imp << 6
        data[18]   |= self.undead           << 7

        data[19]    = self.hard_to_run      << 0
        data[19]   |= self.attack_first     << 1
        data[19]   |= self.no_suplex        << 2
        data[19]   |= self.no_run           << 3
        data[19]   |= self.no_scan          << 4
        data[19]   |= self.no_sketch        << 5
        data[19]   |= self.unknown4         << 6
        data[19]   |= self.no_control       << 7

        data[20:23] = self.status_immunities.data()

        data[23]    = self.absorb_elements
        data[24]    = self.immune_elements
        data[25]    = self.weak_elements

        data[26]    = self.attack_animation

        data[27:30] = self.status_effects.data()

        data[30]    = self.true_knight      << 0
        data[30]   |= self.runic            << 1
        data[30]   |= self.life_3           << 2
        data[30]   |= self.unknown5         << 3
        data[30]   |= self.unknown6         << 4
        data[30]   |= self.unknown7         << 5
        data[30]   |= self.unknown8         << 6
        data[30]   |= self.float            << 7

        data[31]    = self.special_effect   << 0
        data[31]   |= self.special_no_damage<< 6
        data[31]   |= self.special_no_dodge << 7

        return data

    def name_data(self):
        from ..data.enemies import Enemies
        data = text.get_bytes(self.name, text.TEXT2)
        data.extend([0xff] * (Enemies.NAME_SIZE - len(data)))
        return data

    def item_data(self):
        from ..data.enemies import Enemies
        item_data = [0x00] * Enemies.ITEMS_SIZE

        item_data[0]    = self.steal_rare
        item_data[1]    = self.steal_common
        item_data[2]    = self.drop_rare
        item_data[3]    = self.drop_common

        return item_data

    def special_name_data(self):
        from ..data.enemies import Enemies
        data = text.get_bytes(self.special_name, text.TEXT2)
        data.extend([0xff] * (Enemies.SPECIAL_NAMES_SIZE - len(data)))
        return data

    def print(self):
        print(f"{self.id} {self.name}")
