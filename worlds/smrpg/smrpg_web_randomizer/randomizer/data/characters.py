# Data module for character data.

from ...randomizer.logic import utils
from ...randomizer.logic.patch import Patch

from . import spells
from .utils import color_to_bytes, palette_to_bytes


class StatGrowth:
    """Container class for a stat growth/bonus for a certain level + character."""

    def __init__(self, max_hp, attack, defense, magic_attack, magic_defense):
        self.max_hp = max_hp
        self.attack = attack
        self.defense = defense
        self.magic_attack = magic_attack
        self.magic_defense = magic_defense

    @property
    def best_choices(self):
        """Best choice of attributes for a levelup bonus based on the numbers.  For HP, it must be twice the total of
        the attack + defense options to be considered "better".  This is arbitrary, but HP is less useful.

        :return: Tuple of attributes to select for best choice.
        :rtype: tuple[str]
        """
        options = [
            (self.max_hp / 2, ("max_hp", )),
            (self.attack + self.defense, ("attack", "defense")),
            (self.magic_attack + self.magic_defense, ("magic_attack", "magic_defense")),
        ]
        a, b = max(options)
        options = [(c, d) for (c, d) in options if c == a]
        a, b = options[0]
        return b

    def as_bytes(self):
        """Return byte representation of this stat growth object for the patch.

        :rtype: bytearray
        """
        data = bytearray()

        # HP is one byte on its own.  Attack/defense stats are 4 bits each combined into a single byte together.
        data += utils.ByteField(self.max_hp).as_bytes()

        physical = self.attack << 4
        physical |= self.defense
        data += utils.ByteField(physical).as_bytes()

        magical = self.magic_attack << 4
        magical |= self.magic_defense
        data += utils.ByteField(magical).as_bytes()

        return data


class LevelUpExps:
    """Class for amounts of exp required for each levelup."""
    BASE_ADDRESS = 0x3a1aff

    def __init__(self):
        self.levels = [
            0,
            16,
            48,
            84,
            130,
            200,
            290,
            402,
            538,
            700,
            890,
            1110,
            1360,
            1640,
            1950,
            2290,
            2660,
            3060,
            3490,
            3950,
            4440,
            4960,
            5510,
            6088,
            6692,
            7320,
            7968,
            8634,
            9315,
            9999,
        ]

    def get_xp_for_level(self, level):
        """
        :type level: int
        :return: XP required to reach this level.
        :rtype: int
        """
        if level < 1 or level > 30:
            raise ValueError("Level must be between 1 and 30")
        return self.levels[level - 1]

    def get_patch(self):
        """Get patch for exp required for each level up.

        :return: Patch data.
        :rtype: randomizer.logic.patch.Patch
        """
        # Data is 29 blocks (starting at level 2), 2 bytes each block.
        data = bytearray()
        for level in range(2, 31):
            data += utils.ByteField(self.get_xp_for_level(level), num_bytes=2).as_bytes()

        patch = Patch()
        patch.add_data(self.BASE_ADDRESS, data)
        return patch


class Character:
    """Class for handling a character."""
    BASE_ADDRESS = 0x3a002c
    BASE_STAT_GROWTH_ADDRESS = 0x3a1b39
    BASE_STAT_BONUS_ADDRESS = 0x3a1cec
    BASE_LEARNED_SPELLS_ADDRESS = 0x3a42f5

    # Stats used during levelups.
    LEVEL_STATS = ["max_hp", "attack", "defense", "magic_attack", "magic_defense"]

    # Base stats.
    original_name = ''
    index = 0
    starting_level = 1
    max_hp = 1
    speed = 1
    attack = 1
    defense = 1
    magic_attack = 1
    magic_defense = 1
    xp = 0
    learned_spells = {}
    palette = None
    forest_maze_sprite_id = 0x0
    mway_3_npc_id = []
    mway_2_npc_id = []
    mway_1_npc_id = []
    moleville_sprite_id = 0x0

    # Placeholders for vanilla starting levelup growth and bonus numbers.
    starting_growths = ()
    starting_bonuses = ()

    def __init__(self, world):
        """

        Args:
            world (randomizer.logic.main.GameWorld):

        """
        self.world = world
        self.starting_spells = set()

        # Level-up stat growth and bonuses.
        self.levelup_growths = []
        for max_hp, attack, defense, magic_attack, magic_defense in self.starting_growths:
            self.levelup_growths.append(StatGrowth(max_hp, attack, defense, magic_attack, magic_defense))

        self.levelup_bonuses = []
        for max_hp, attack, defense, magic_attack, magic_defense in self.starting_bonuses:
            self.levelup_bonuses.append(StatGrowth(max_hp, attack, defense, magic_attack, magic_defense))

    def __str__(self):
        return "<{}>".format(self.name)

    def __repr__(self):
        return str(self)

    @property
    def name(self):
        return self.__class__.__name__

    def get_stat_at_level(self, attr, level):
        """Get natural value of the given stat at the given level using just the levelup growths.

        :type attr: str
        :type level: int
        :rtype: int
        """
        if level < 1 or level > 30:
            raise ValueError("Level must be between 1 and 30")

        value = getattr(self, attr)
        for g in self.levelup_growths[:level - 1]:
            value += getattr(g, attr)
        return value

    def get_optimal_stat_at_level(self, attr, level):
        """Get optimal value of the given stat at the given level using the levelup growths and best choice bonuses.

        :type attr: str
        :type level: int
        :rtype: int
        """
        if level < 1 or level > 30:
            raise ValueError("Level must be between 1 and 30")

        value = self.get_stat_at_level(attr, level)
        for b in self.levelup_bonuses[:level - 1]:
            if attr in b.best_choices:
                value += getattr(b, attr)
        return value

    def get_max_stat_at_level(self, attr, level):
        """Get max value of the given stat at the given level using the levelup growths and bonuses.

        :type attr: str
        :type level: int
        :rtype: int
        """
        if level < 1 or level > 30:
            raise ValueError("Level must be between 1 and 30")

        value = self.get_stat_at_level(attr, level)
        for b in self.levelup_bonuses[:level - 1]:
            value += getattr(b, attr)
        return value

    def get_patch(self):
        """Build patch data for this character.

        :return: Patch data for this character.
        :rtype: randomizer.logic.patch.Patch
        """
        patch = Patch()

        # Build character patch data.
        char_data = bytearray()
        char_data += utils.ByteField(self.starting_level).as_bytes()
        char_data += utils.ByteField(self.max_hp, num_bytes=2).as_bytes()  # Current HP
        char_data += utils.ByteField(self.max_hp, num_bytes=2).as_bytes()  # Max HP
        char_data += utils.ByteField(self.speed).as_bytes()
        char_data += utils.ByteField(self.attack).as_bytes()
        char_data += utils.ByteField(self.defense).as_bytes()
        char_data += utils.ByteField(self.magic_attack).as_bytes()
        char_data += utils.ByteField(self.magic_defense).as_bytes()
        char_data += utils.ByteField(self.xp, num_bytes=2).as_bytes()
        # Set starting weapon/armor/accessory as blank for all characters.
        char_data += utils.ByteField(0xff).as_bytes()
        char_data += utils.ByteField(0xff).as_bytes()
        char_data += utils.ByteField(0xff).as_bytes()
        char_data.append(0x00)  # Unused byte
        char_data += utils.BitMapSet(4, [spell.index for spell in self.starting_spells]).as_bytes()

        # Base address plus offset based on character index.
        addr = self.BASE_ADDRESS + (self.index * 20)
        patch.add_data(addr, char_data)

        # Add levelup stat growth and bonuses to the patch data for this character.  Offset is 15 bytes for each stat
        # object, 3 bytes per character.
        for i, stat in enumerate(self.levelup_growths):
            addr = self.BASE_STAT_GROWTH_ADDRESS + (i * 15) + (self.index * 3)
            patch.add_data(addr, stat.as_bytes())

        for i, stat in enumerate(self.levelup_bonuses):
            addr = self.BASE_STAT_BONUS_ADDRESS + (i * 15) + (self.index * 3)
            patch.add_data(addr, stat.as_bytes())

        # Add learned spells data.
        # Data is 29 blocks (starting at level 2), 5 bytes each block (1 byte per character in order)
        base_addr = self.BASE_LEARNED_SPELLS_ADDRESS + self.index
        for level in range(2, 31):
            level_addr = base_addr + ((level - 2) * 5)
            # If we have a spell for this level, add the index.  Otherwise it should be 0xff for no spell learned.
            if self.learned_spells.get(level):
                patch.add_data(level_addr, utils.ByteField(self.learned_spells[level].index).as_bytes())
            else:
                patch.add_data(level_addr, utils.ByteField(0xff).as_bytes())

        if self.palette:
            colourbytes = palette_to_bytes(self.palette.colours)
            poisonbytes = palette_to_bytes(self.palette.poison_colours)
            underwaterbytes = palette_to_bytes(self.palette.underwater_colours)
            for address in self.palette.starting_addresses:
                patch.add_data(address, colourbytes)
            for address in self.palette.poison_addresses:
                patch.add_data(address, poisonbytes)
            for address in self.palette.underwater_addresses:
                patch.add_data(address, underwaterbytes)

            if self.palette.rename_character:
                name = self.palette.name
                clone_name = self.palette.name.upper()
                while len(name) < 10:
                    name += " "
                if len(clone_name) < 8:
                    clone_name = clone_name + " CLONE"
                else:
                    clone_name = clone_name + " 2"
                while len(clone_name) < 13:
                    clone_name += " "
                patch.add_data(self.palette.name_address, name)
                patch.add_data(self.palette.clone_name_address, clone_name)

        return patch


# ******************* Actual character data classes.
class Mario(Character):
    original_name = "Mario"
    index = 0
    starting_level = 1
    max_hp = 20
    speed = 20
    attack = 20
    defense = 0
    magic_attack = 10
    magic_defense = 2
    learned_spells = {
        1: spells.Jump,
        3: spells.FireOrb,
        6: spells.SuperJump,
        10: spells.SuperFlame,
        14: spells.UltraJump,
        18: spells.UltraFlame,
    }

    # Vanilla levelup stat growths
    # (hp, attack, defense, m.attack, m.defense)
    starting_growths = (
        (5, 3, 2, 2, 2),
        (5, 3, 2, 2, 2),
        (5, 3, 3, 2, 2),
        (5, 3, 3, 2, 2),
        (5, 4, 3, 3, 2),
        (6, 4, 3, 3, 2),
        (6, 4, 3, 3, 2),
        (7, 4, 3, 3, 2),
        (7, 4, 3, 3, 2),
        (7, 5, 4, 3, 3),
        (8, 5, 4, 4, 3),
        (8, 5, 4, 4, 3),
        (8, 5, 4, 4, 3),
        (9, 5, 4, 4, 3),
        (9, 6, 4, 4, 3),
        (9, 6, 4, 4, 3),
        (10, 6, 4, 4, 3),
        (10, 6, 4, 5, 3),
        (10, 6, 4, 5, 3),
        (2, 2, 2, 2, 2),
        (2, 2, 2, 2, 2),
        (2, 2, 2, 2, 2),
        (2, 2, 2, 2, 2),
        (2, 2, 2, 2, 2),
        (2, 2, 2, 2, 2),
        (2, 2, 2, 2, 2),
        (2, 2, 2, 2, 2),
        (2, 2, 2, 2, 2),
        (2, 2, 2, 2, 2),
    )

    # Vanilla levelup stat bonus options
    # (hp, attack, defense, m.attack, m.defense)
    starting_bonuses = (
        (3, 1, 1, 3, 1),
        (3, 2, 1, 1, 1),
        (4, 1, 1, 1, 1),
        (3, 1, 1, 3, 1),
        (3, 2, 1, 1, 1),
        (4, 1, 1, 1, 1),
        (3, 1, 1, 3, 1),
        (3, 2, 1, 1, 1),
        (4, 1, 1, 1, 1),
        (3, 1, 1, 3, 1),
        (3, 2, 1, 1, 1),
        (4, 1, 1, 1, 1),
        (3, 1, 1, 3, 1),
        (3, 2, 1, 1, 1),
        (4, 1, 1, 1, 1),
        (3, 1, 1, 3, 1),
        (3, 2, 1, 1, 1),
        (4, 1, 1, 1, 1),
        (3, 1, 1, 3, 1),
        (1, 2, 1, 1, 1),
        (2, 1, 1, 1, 1),
        (1, 1, 1, 3, 1),
        (1, 2, 1, 1, 1),
        (2, 1, 1, 1, 1),
        (1, 1, 1, 3, 1),
        (1, 2, 1, 1, 1),
        (2, 1, 1, 1, 1),
        (1, 1, 1, 3, 1),
        (1, 2, 1, 1, 1),
    )
    forest_maze_sprite_id = 0x03
    mway_3_npc_id = [0x03, 0xB0]
    mway_2_npc_id = [0x03, 0x70]
    mway_1_npc_id = [0x03, 0x40]
    moleville_sprite_id = 0x02

    def get_patch(self):
        patch = super().get_patch()

        def special_palette(colours, address):
            for j in range(0, len(colours)):
                i = colours[j]
                if i is not None:
                    colour = self.palette.colours[i]
                    patch.add_data(address + j*2, color_to_bytes(colour))

        if self.palette is not None:
            special_palette([0, 1, 2, 3, 4, 6, 7, 8, 8, 10, 11, 11, 12, 13, 14], self.palette.doll_addresses[0])
            special_palette([None, 13, 1, 2, None, 5, 3, 6, 7, 9, 4, 9, 8, 10, 11], self.palette.minecart_addresses[0])

        return patch


class Peach(Character):
    index = 1
    original_name = "Toadstool"
    starting_level = 9
    max_hp = 15
    speed = 24
    attack = 15
    defense = 0
    magic_attack = 14
    magic_defense = 14
    learned_spells = {
        3: spells.Therapy,
        7: spells.GroupHug,
        11: spells.SleepyTime,
        13: spells.ComeBack,
        15: spells.Mute,
        18: spells.PsychBomb,
    }

    # Vanilla levelup stat growths
    # (hp, attack, defense, m.attack, m.defense)
    starting_growths = (
        (2, 2, 2, 1, 1),
        (2, 2, 2, 1, 1),
        (2, 2, 2, 2, 1),
        (2, 2, 3, 2, 1),
        (2, 2, 3, 2, 1),
        (2, 2, 3, 3, 2),
        (2, 2, 3, 3, 2),
        (3, 2, 3, 3, 2),
        # Vanilla growths
        (4, 1, 3, 4, 2),
        (5, 2, 3, 4, 3),
        (6, 3, 3, 4, 3),
        (7, 4, 3, 4, 3),
        (8, 5, 3, 4, 3),
        (9, 6, 3, 4, 3),
        (10, 7, 3, 4, 4),
        (11, 8, 4, 4, 4),
        (12, 9, 4, 4, 4),
        (13, 10, 4, 4, 4),
        (14, 10, 4, 4, 4),
        (2, 2, 2, 2, 2),
        (2, 2, 2, 2, 2),
        (2, 2, 2, 2, 2),
        (2, 2, 2, 2, 2),
        (2, 2, 2, 2, 2),
        (2, 2, 2, 2, 2),
        (2, 2, 2, 2, 2),
        (2, 2, 2, 2, 2),
        (2, 2, 2, 2, 2),
        (2, 2, 2, 2, 2),
    )

    # Vanilla levelup stat bonus options
    # (hp, attack, defense, m.attack, m.defense)
    starting_bonuses = (
        (5, 1, 1, 3, 1),
        (5, 3, 1, 1, 1),
        (9, 1, 1, 1, 1),
        (5, 1, 1, 3, 1),
        (5, 3, 1, 1, 1),
        (9, 1, 1, 1, 1),
        (5, 1, 1, 3, 1),
        (5, 3, 1, 1, 1),
        (9, 1, 1, 1, 1),
        (5, 1, 1, 3, 1),
        (5, 3, 1, 1, 1),
        (9, 1, 1, 1, 1),
        (5, 1, 1, 3, 1),
        (5, 3, 1, 1, 1),
        (9, 1, 1, 1, 1),
        (5, 1, 1, 3, 1),
        (5, 3, 1, 1, 1),
        (9, 1, 1, 1, 1),
        (5, 1, 1, 3, 1),
        (3, 3, 1, 1, 1),
        (2, 1, 1, 1, 1),
        (1, 1, 1, 3, 1),
        (1, 3, 1, 1, 1),
        (2, 1, 1, 1, 1),
        (1, 1, 1, 3, 1),
        (1, 3, 1, 1, 1),
        (2, 1, 1, 1, 1),
        (1, 1, 1, 3, 1),
        (1, 3, 1, 1, 1),
    )
    forest_maze_sprite_id = 0x07
    mway_3_npc_id = [0x07, 0xB0]
    mway_2_npc_id = [0x07, 0x70]
    mway_1_npc_id = [0x07, 0x40]
    moleville_sprite_id = 0x06


class Bowser(Character):
    index = 2
    original_name = "Bowser"
    starting_level = 8
    max_hp = 25
    speed = 15
    attack = 39
    defense = 15
    magic_attack = 1
    magic_defense = 6
    learned_spells = {
        8: spells.Terrorize,
        12: spells.PoisonGas,
        15: spells.Crusher,
        18: spells.BowserCrush,
    }

    # Vanilla levelup stat growths
    # (hp, attack, defense, m.attack, m.defense)
    starting_growths = (
        (6, 6, 5, 1, 3),
        (6, 6, 5, 1, 3),
        (7, 6, 5, 1, 3),
        (7, 6, 5, 1, 3),
        (7, 6, 5, 2, 3),
        (8, 6, 5, 2, 3),
        (8, 6, 5, 2, 3),
        # Vanilla growths
        (8, 3, 3, 4, 2),
        (8, 3, 3, 4, 2),
        (8, 4, 3, 4, 2),
        (8, 4, 3, 4, 2),
        (8, 4, 3, 4, 2),
        (8, 4, 3, 4, 2),
        (8, 4, 3, 4, 2),
        (8, 5, 4, 4, 2),
        (8, 5, 4, 4, 2),
        (9, 5, 4, 4, 2),
        (9, 6, 4, 4, 2),
        (9, 6, 4, 4, 2),
        (4, 2, 2, 2, 2),
        (4, 2, 2, 2, 2),
        (4, 2, 2, 2, 2),
        (4, 2, 2, 2, 2),
        (4, 2, 2, 2, 2),
        (4, 2, 2, 2, 2),
        (4, 2, 2, 2, 2),
        (4, 2, 2, 2, 2),
        (4, 2, 2, 2, 2),
        (4, 2, 2, 2, 2),
    )

    # Vanilla levelup stat bonus options
    # (hp, attack, defense, m.attack, m.defense)
    starting_bonuses = (
        (1, 1, 1, 3, 1),
        (1, 2, 1, 1, 1),
        (3, 1, 1, 1, 1),
        (1, 1, 1, 3, 1),
        (1, 2, 1, 1, 1),
        (3, 1, 1, 1, 1),
        (1, 1, 1, 3, 1),
        (1, 2, 1, 1, 1),
        (3, 1, 1, 1, 1),
        (1, 1, 1, 3, 1),
        (1, 2, 1, 1, 1),
        (3, 1, 1, 1, 1),
        (1, 1, 1, 3, 1),
        (1, 2, 1, 1, 1),
        (3, 1, 1, 1, 1),
        (1, 1, 1, 3, 1),
        (1, 2, 1, 1, 1),
        (3, 1, 1, 1, 1),
        (1, 1, 1, 3, 1),
        (1, 2, 1, 1, 1),
        (3, 1, 1, 1, 1),
        (1, 1, 1, 3, 1),
        (1, 2, 1, 1, 1),
        (3, 1, 1, 1, 1),
        (1, 1, 1, 3, 1),
        (1, 2, 1, 1, 1),
        (3, 1, 1, 1, 1),
        (1, 1, 1, 3, 1),
        (1, 2, 1, 1, 1),
    )
    forest_maze_sprite_id = 0x0B
    mway_3_npc_id = [0x0B, 0xB0]
    mway_2_npc_id = [0x0B, 0x70]
    mway_1_npc_id = [0x0B, 0x40]
    moleville_sprite_id = 0x0A


class Geno(Character):
    index = 3
    original_name = "Geno"
    starting_level = 6
    max_hp = 20
    speed = 30
    attack = 24
    defense = 6
    magic_attack = 3
    magic_defense = 5
    learned_spells = {
        6: spells.GenoBeam,
        8: spells.GenoBoost,
        11: spells.GenoWhirl,
        14: spells.GenoBlast,
        17: spells.GenoFlash,
    }

    # Vanilla levelup stat growths
    # (hp, attack, defense, m.attack, m.defense)
    starting_growths = (
        (3, 6, 3, 3, 2),
        (4, 6, 3, 3, 2),
        (4, 6, 3, 3, 2),
        (4, 6, 3, 3, 2),
        (4, 6, 3, 4, 2),
        # Vanilla growths
        (8, 5, 3, 4, 2),
        (8, 5, 3, 4, 2),
        (8, 5, 3, 4, 2),
        (8, 5, 3, 4, 2),
        (8, 5, 4, 4, 3),
        (8, 5, 4, 4, 3),
        (8, 5, 4, 4, 3),
        (8, 5, 4, 4, 3),
        (8, 5, 4, 4, 3),
        (8, 5, 4, 5, 3),
        (8, 5, 4, 5, 3),
        (8, 6, 4, 5, 3),
        (8, 6, 4, 5, 3),
        (8, 6, 4, 5, 3),
        (1, 2, 3, 2, 2),
        (1, 2, 3, 2, 2),
        (1, 2, 3, 2, 2),
        (1, 2, 3, 2, 2),
        (1, 2, 3, 2, 2),
        (1, 2, 3, 2, 2),
        (1, 2, 3, 2, 2),
        (1, 2, 3, 2, 2),
        (1, 2, 3, 2, 2),
        (1, 2, 3, 2, 2),
    )

    # Vanilla levelup stat bonus options
    # (hp, attack, defense, m.attack, m.defense)
    starting_bonuses = (
        (5, 1, 1, 3, 1),
        (5, 3, 1, 1, 1),
        (6, 1, 1, 1, 1),
        (5, 1, 1, 3, 1),
        (5, 3, 1, 1, 1),
        (6, 1, 1, 1, 1),
        (5, 1, 1, 3, 1),
        (5, 3, 1, 1, 1),
        (6, 1, 1, 1, 1),
        (5, 1, 1, 3, 1),
        (5, 3, 1, 1, 1),
        (6, 1, 1, 1, 1),
        (5, 1, 1, 3, 1),
        (5, 3, 1, 1, 1),
        (6, 1, 1, 1, 1),
        (5, 1, 1, 3, 1),
        (5, 3, 1, 1, 1),
        (6, 1, 1, 1, 1),
        (5, 1, 1, 3, 1),
        (1, 3, 1, 1, 1),
        (2, 1, 1, 1, 1),
        (1, 1, 1, 3, 1),
        (1, 3, 1, 1, 1),
        (2, 1, 1, 1, 1),
        (1, 1, 1, 3, 1),
        (1, 3, 1, 1, 1),
        (2, 1, 1, 1, 1),
        (1, 1, 1, 3, 1),
        (1, 3, 1, 1, 1),
    )
    forest_maze_sprite_id = 0x13
    mway_3_npc_id = [0x13, 0xB0]
    mway_2_npc_id = [0x13, 0x70]
    mway_1_npc_id = [0x13, 0x40]
    moleville_sprite_id = 0x12


class Mallow(Character):
    index = 4
    original_name = "Mallow"
    starting_level = 2
    max_hp = 16
    speed = 18
    attack = 20
    defense = 0
    magic_attack = 11
    magic_defense = 7
    learned_spells = {
        2: spells.Thunderbolt,
        3: spells.HPRain,
        6: spells.Psychopath,
        10: spells.Shocker,
        14: spells.Snowy,
        18: spells.StarRain,
    }

    # Vanilla levelup stat growths
    # (hp, attack, defense, m.attack, m.defense)
    starting_growths = (
        (4, 2, 3, 2, 2),
        # Vanilla growths
        (4, 2, 3, 2, 2),
        (4, 2, 3, 2, 2),
        (4, 2, 3, 3, 2),
        (5, 2, 3, 3, 2),
        (5, 3, 3, 3, 2),
        (5, 3, 3, 4, 2),
        (6, 3, 3, 4, 3),
        (6, 3, 3, 4, 3),
        (6, 4, 3, 4, 3),
        (7, 4, 3, 5, 3),
        (7, 4, 3, 5, 3),
        (7, 4, 3, 5, 3),
        (8, 5, 3, 5, 3),
        (8, 5, 3, 5, 3),
        (8, 5, 3, 5, 3),
        (9, 5, 3, 5, 4),
        (9, 6, 3, 5, 4),
        (9, 6, 3, 5, 4),
        (2, 2, 2, 2, 2),
        (2, 2, 2, 2, 2),
        (2, 2, 2, 2, 2),
        (2, 2, 2, 2, 2),
        (2, 2, 2, 2, 2),
        (2, 2, 2, 2, 2),
        (2, 2, 2, 2, 2),
        (2, 2, 2, 2, 2),
        (2, 2, 2, 2, 2),
        (2, 2, 2, 2, 2),
    )

    # Vanilla levelup stat bonus options
    # (hp, attack, defense, m.attack, m.defense)
    starting_bonuses = (
        (4, 1, 1, 2, 1),
        (4, 3, 1, 1, 1),
        (6, 1, 1, 1, 1),
        (4, 1, 1, 2, 1),
        (4, 3, 1, 1, 1),
        (6, 1, 1, 1, 1),
        (4, 1, 1, 2, 1),
        (4, 3, 1, 1, 1),
        (6, 1, 1, 1, 1),
        (4, 1, 1, 2, 1),
        (4, 3, 1, 1, 1),
        (6, 1, 1, 1, 1),
        (4, 1, 1, 2, 1),
        (4, 3, 1, 1, 1),
        (6, 1, 1, 1, 1),
        (4, 1, 1, 2, 1),
        (4, 3, 1, 1, 1),
        (6, 1, 1, 1, 1),
        (4, 1, 1, 2, 1),
        (1, 3, 1, 1, 1),
        (2, 1, 1, 1, 1),
        (1, 1, 1, 2, 1),
        (1, 3, 1, 1, 1),
        (2, 1, 1, 1, 1),
        (1, 1, 1, 2, 1),
        (1, 3, 1, 1, 1),
        (2, 1, 1, 1, 1),
        (1, 1, 1, 2, 1),
        (1, 3, 1, 1, 1),
    )
    forest_maze_sprite_id = 0x0F
    mway_3_npc_id = [0x0F, 0xB0]
    mway_2_npc_id = [0x0F, 0x70]
    mway_1_npc_id = [0x0F, 0x40]
    moleville_sprite_id = 0x0E


def get_default_characters(world):
    """Get default vanilla character list for the world.

    Args:
        world (randomizer.logic.main.GameWorld):

    Returns:
        list[Character]: List of default character objects.

    """
    return [
        Mario(world),
        Mallow(world),
        Geno(world),
        Bowser(world),
        Peach(world),
    ]
