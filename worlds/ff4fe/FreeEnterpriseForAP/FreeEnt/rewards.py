import enum

from . import databases

# must parallel the list in rewards.f4c
class RewardSlot(enum.IntEnum):
    none                        = 0x00
    starting_character          = 0x01
    starting_partner_character  = 0x02
    mist_character              = 0x03
    watery_pass_character       = 0x04
    damcyan_character           = 0x05
    kaipo_character             = 0x06
    hobs_character              = 0x07
    mysidia_character_1         = 0x08
    mysidia_character_2         = 0x09
    ordeals_character           = 0x0A
    baron_inn_character         = 0x0D
    baron_castle_character      = 0x0E
    zot_character_1             = 0x0F
    zot_character_2             = 0x10
    dwarf_castle_character      = 0x11
    cave_eblan_character        = 0x12
    lunar_palace_character      = 0x13
    giant_character             = 0x14
    starting_item               = 0x20
    antlion_item                = 0x21
    fabul_item                  = 0x22
    ordeals_item                = 0x23
    baron_inn_item              = 0x24
    baron_castle_item           = 0x25
    toroia_hospital_item        = 0x26
    magnes_item                 = 0x27
    zot_item                    = 0x28
    babil_boss_item             = 0x29
    cannon_item                 = 0x2A
    luca_item                   = 0x2B
    sealed_cave_item            = 0x2C
    feymarch_item               = 0x2D
    rat_trade_item              = 0x2E
    found_yang_item             = 0x2F
    pan_trade_item              = 0x30
    feymarch_queen_item         = 0x31
    feymarch_king_item          = 0x32
    baron_throne_item           = 0x33
    sylph_item                  = 0x34
    bahamut_item                = 0x35
    lunar_boss_1_item           = 0x36
    lunar_boss_2_item           = 0x37
    lunar_boss_3_item           = 0x38
    lunar_boss_4_item_1         = 0x39
    lunar_boss_4_item_2         = 0x3A
    lunar_boss_5_item           = 0x3B
    zot_chest                   = 0x3C
    eblan_chest_1               = 0x3D
    eblan_chest_2               = 0x3E
    eblan_chest_3               = 0x3F
    lower_babil_chest_1         = 0x40
    lower_babil_chest_2         = 0x41
    lower_babil_chest_3         = 0x42
    lower_babil_chest_4         = 0x43
    cave_eblan_chest            = 0x44
    upper_babil_chest           = 0x45
    cave_of_summons_chest       = 0x46
    sylph_cave_chest_1          = 0x47
    sylph_cave_chest_2          = 0x48
    sylph_cave_chest_3          = 0x49
    sylph_cave_chest_4          = 0x4A
    sylph_cave_chest_5          = 0x4B
    sylph_cave_chest_6          = 0x4C
    sylph_cave_chest_7          = 0x4D
    giant_chest                 = 0x4E
    lunar_path_chest            = 0x4F
    lunar_core_chest_1          = 0x50
    lunar_core_chest_2          = 0x51
    lunar_core_chest_3          = 0x52
    lunar_core_chest_4          = 0x53
    lunar_core_chest_5          = 0x54
    lunar_core_chest_6          = 0x55
    lunar_core_chest_7          = 0x56
    lunar_core_chest_8          = 0x57
    lunar_core_chest_9          = 0x58
    rydias_mom_item             = 0x59
    fallen_golbez_item          = 0x5A
    forge_item                  = 0x5B
    pink_trade_item             = 0x5C
    fixed_crystal               = 0x5D

    MAX_COUNT = 0x60

ACTOR_CODES = {
    '#actor.DKCecil'  : 0x01,
    '#actor.Kain1'    : 0x02,
    '#actor.CRydia'   : 0x03,
    '#actor.Tellah1'  : 0x04,
    '#actor.Edward'   : 0x05,
    '#actor.Rosa1'    : 0x06,
    '#actor.Yang1'    : 0x07,
    '#actor.Palom'    : 0x08,
    '#actor.Porom'    : 0x09,
    '#actor.Tellah2'  : 0x0A,
    '#actor.Yang2'    : 0x0D,
    '#actor.Cid'      : 0x0E,
    '#actor.Kain2'    : 0x0F,
    '#actor.Rosa2'    : 0x10,
    '#actor.ARydia'   : 0x11,
    '#actor.Edge'     : 0x12,
    '#actor.Fusoya'   : 0x13,
    '#actor.Kain3'    : 0x14,    
    }

REWARD_SLOT_SPOILER_NAMES = {
    RewardSlot.none                        : "(not available)",
    RewardSlot.starting_character          : "Starting character 1",
    RewardSlot.starting_partner_character  : "Starting character 2",
    RewardSlot.mist_character              : "Mist/Package character",
    RewardSlot.watery_pass_character       : "Watery Pass character",
    RewardSlot.damcyan_character           : "Damcyan character",
    RewardSlot.kaipo_character             : "Kaipo/SandRuby character",
    RewardSlot.hobs_character              : "Mt. Hobs character",
    RewardSlot.mysidia_character_1         : "Mysidia character 1",
    RewardSlot.mysidia_character_2         : "Mysidia character 2",
    RewardSlot.ordeals_character           : "Mt. Ordeals character",
    RewardSlot.baron_inn_character         : "Baron Inn character",
    RewardSlot.baron_castle_character      : "Baron Castle character",
    RewardSlot.zot_character_1             : "Zot character 1",
    RewardSlot.zot_character_2             : "Zot character 2",
    RewardSlot.dwarf_castle_character      : "Dwarf Castle character",
    RewardSlot.cave_eblan_character        : "Cave Eblan character",
    RewardSlot.lunar_palace_character      : "Lunar Palace character",
    RewardSlot.giant_character             : "Giant of Bab-il character",
    RewardSlot.starting_item               : "Starting item",
    RewardSlot.antlion_item                : "Antlion Nest item",
    RewardSlot.fabul_item                  : "Defend Fabul reward item",
    RewardSlot.ordeals_item                : "Mt. Ordeals item",
    RewardSlot.baron_inn_item              : "Baron Inn item",
    RewardSlot.baron_castle_item           : "Baron Castle item",
    RewardSlot.toroia_hospital_item        : "Edward/Toroia item",
    RewardSlot.magnes_item                 : "Cave Magnes item",
    RewardSlot.zot_item                    : "Zot item",
    RewardSlot.babil_boss_item             : "Lower Bab-il item (Tower Key slot)",
    RewardSlot.cannon_item                 : "Super Cannon destruction item",
    RewardSlot.luca_item                   : "Dwarf Castle/Luca item",
    RewardSlot.sealed_cave_item            : "Sealed Cave item",
    RewardSlot.feymarch_item               : "Town of Monsters chest item",
    RewardSlot.rat_trade_item              : "Rat Tail trade item",
    RewardSlot.found_yang_item             : "Found Yang item (Pan slot)",
    RewardSlot.pan_trade_item              : "Pan trade item (Spoon slot)",
    RewardSlot.feymarch_queen_item         : "Town of Monsters queen item (Asura slot)",
    RewardSlot.feymarch_king_item          : "Town of Monsters king item (Levia slot)",
    RewardSlot.baron_throne_item           : "Baron Basement item (Odin slot)",
    RewardSlot.sylph_item                  : "Wake Yang item (Sylph slot)",
    RewardSlot.bahamut_item                : "Cave Bahamut item",
    RewardSlot.lunar_boss_1_item           : "Lunar Subterrane altar 1 (Murasame slot)",
    RewardSlot.lunar_boss_2_item           : "Lunar Subterrane altar 2 (Crystal Sword slot)",
    RewardSlot.lunar_boss_3_item           : "Lunar Subterrane altar 3 (White Spear slot)",
    RewardSlot.lunar_boss_4_item_1         : "Lunar Subterrane pillar chest 1 (Ribbon slot)",
    RewardSlot.lunar_boss_4_item_2         : "Lunar Subterrane pillar chest 2 (Ribbon slot)",
    RewardSlot.lunar_boss_5_item           : "Lunar Subterrane altar 4 (Masamune slot)",
    RewardSlot.zot_chest                   : "Tower of Zot MIAB",
    RewardSlot.eblan_chest_1               : "Eblan Castle MIAB",
    RewardSlot.eblan_chest_2               : "Eblan Castle MIAB",
    RewardSlot.eblan_chest_3               : "Eblan Castle MIAB",
    RewardSlot.lower_babil_chest_1         : "Lower Bab-il MIAB",
    RewardSlot.lower_babil_chest_2         : "Lower Bab-il MIAB",
    RewardSlot.lower_babil_chest_3         : "Lower Bab-il MIAB",
    RewardSlot.lower_babil_chest_4         : "Lower Bab-il MIAB",
    RewardSlot.cave_eblan_chest            : "Cave Eblan MIAB",
    RewardSlot.upper_babil_chest           : "Upper Bab-il MIAB",
    RewardSlot.cave_of_summons_chest       : "Cave of Summons MIAB",
    RewardSlot.sylph_cave_chest_1          : "Sylph Cave MIAB",
    RewardSlot.sylph_cave_chest_2          : "Sylph Cave MIAB",
    RewardSlot.sylph_cave_chest_3          : "Sylph Cave MIAB",
    RewardSlot.sylph_cave_chest_4          : "Sylph Cave MIAB",
    RewardSlot.sylph_cave_chest_5          : "Sylph Cave MIAB",
    RewardSlot.sylph_cave_chest_6          : "Sylph Cave MIAB",
    RewardSlot.sylph_cave_chest_7          : "Sylph Cave MIAB",
    RewardSlot.giant_chest                 : "Giant of Bab-il MIAB",
    RewardSlot.lunar_path_chest            : "Lunar Path MIAB",
    RewardSlot.lunar_core_chest_1          : "Lunar Subterrane MIAB",
    RewardSlot.lunar_core_chest_2          : "Lunar Subterrane MIAB",
    RewardSlot.lunar_core_chest_3          : "Lunar Subterrane MIAB",
    RewardSlot.lunar_core_chest_4          : "Lunar Subterrane MIAB",
    RewardSlot.lunar_core_chest_5          : "Lunar Subterrane MIAB",
    RewardSlot.lunar_core_chest_6          : "Lunar Subterrane MIAB",
    RewardSlot.lunar_core_chest_7          : "Lunar Subterrane MIAB",
    RewardSlot.lunar_core_chest_8          : "Lunar Subterrane MIAB",
    RewardSlot.lunar_core_chest_9          : "Lunar Subterrane MIAB",
    RewardSlot.rydias_mom_item             : "D.Mist/Rydia's Mom item",
    RewardSlot.fallen_golbez_item          : "Fallen Golbez item",
    RewardSlot.forge_item                  : "Kokkol forged item",
    RewardSlot.pink_trade_item             : "Pink Tail trade item",
    RewardSlot.fixed_crystal               : "Objective completion", 
}

class Reward:
    def __init__(self, low_byte, high_byte):
        self._encoded = (low_byte, high_byte)

    def encode(self):
        return self._encoded

    def __eq__(self, other):
        return self._encoded == other._encoded

    def __hash__(self):
        return hash(self._encoded)

class EmptyReward(Reward):
    def __init__(self):
        super().__init__(0x00, 0x00)

    def __str__(self):
        return 'nothing'

class ItemReward(Reward):
    def __init__(self, item, key_item=False):
        self.item = item
        self.is_key = key_item
        super().__init__(item, (0x02 if key_item else 0x00))

    def __eq__(self, other):
        if type(other) in (int, str):
            return self.item == other
        else:
            return super().__eq__(other)

    __hash__ = Reward.__hash__

    def __str__(self):
        return ('*' if self.is_key else '') + '[' + str(self.item) + ']'

    def encode(self):
        encoding = super().encode()
        if type(self.item) is str:
            return [databases.get_items_dbview().find_one(lambda it: it.const == self.item).code, encoding[1]]
        else:
            return encoding

def KeyItemReward(item):
    return ItemReward(item, True)

class AxtorReward(Reward):
    def __init__(self, axtor):
        super().__init__(axtor, 0x04)
        self.axtor = axtor

    def encode(self):
        encoding = super().encode()
        if encoding[0] in ACTOR_CODES:
            return [ACTOR_CODES[encoding[0]], encoding[1]]
        else:
            return encoding

    def __str__(self):
        return str(self.axtor)

class RewardsAssignment:
    def __init__(self):
        self._assignment = {}

    def __setitem__(self, slot, reward):
        self._assignment[slot] = reward

    def __getitem__(self, slot):
        return self._assignment[slot]

    def __contains__(self, slot):
        return slot in self._assignment

    def __iter__(self):
        for k in self._assignment:
            yield RewardSlot(k)

    def update(self, other):
        for k in other:
            self[k] = other[k]

    def find_slot(self, reward):
        for slot in self._assignment:
            if self._assignment[slot] == reward:
                return slot
        return None

    def generate_table(self):
        output = []
        for index in range(RewardSlot.MAX_COUNT.value):
            try:
                slot = RewardSlot(index)
                has_slot = (slot in self._assignment)
            except ValueError:
                has_slot = False

            if has_slot:
                encoded = self._assignment[slot].encode()
                for b in encoded:
                    if type(b) is int:
                        output.append(b)
                    else:
                        raise ValueError(f'Rewards table cannot contain non-numeric value {b}')
            else:
                output.extend([0, 0])

        return output

    def count_rewards(self, functor):
        count = 0
        for k in self._assignment:
            if functor(self._assignment[k]):
                count += 1
        return count

    def count_key_items(self):
        return self.count_rewards(lambda r : type(r) is ItemReward and r.is_key)

    def count_characters(self):
        return self.count_rewards(lambda r : type(r) is AxtorReward)
