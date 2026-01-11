# Data module for enemy data.

from ...randomizer.logic import flags, utils
from ...randomizer.logic.battleassembler import BattleScript
from ...randomizer.logic.patch import Patch
from . import attacks
from . import battlescripts
from . import items
from . import spells
from .utils import palette_to_bytes
from .battletables import Monsters, Targets

# Number of enemies
NUM_ENEMIES = 256
NO_SHADOW = 0
SMALL_SHADOW = 1
MED_SHADOW = 2
LARGE_SHADOW = 3
BLOCK_SHADOW = 4


class Enemy:
    """Class representing an enemy in the game."""
    FLOWER_BONUS_BASE_ADDRESS = 0x39bb44
    BASE_PSYCHOPATH_POINTER_ADDRESS = 0x399fd1
    PSYCHOPATH_DATA_POINTER_OFFSET = 0x390000
    BASE_PSYCHOPATH_DATA_ADDRESS = 0x39a1d1
    NAME_BASE_ADDRESS = 0x3992d1

    # Default instance attributes.
    index = 0
    address = 0x000000
    boss = False
    hp = 0
    speed = 0
    attack = 0
    defense = 0
    magic_attack = 0
    magic_defense = 0
    fp = 0
    evade = 0
    magic_evade = 0
    invincible = False
    death_immune = False
    morph_chance = 0
    sound_on_hit = 0
    sound_on_approach = 0
    resistances = []
    weaknesses = []
    status_immunities = []
    palette = 0
    flower_bonus_type = 0
    flower_bonus_chance = 0
    flying = False
    high_flying = False
    one_per_battle = False  # Flag if enemy is unique per battle (only 1 max per formation)
    hp_counter_ratios = []

    # Reward attributes.
    reward_address = 0x000000
    xp = 0
    coins = 0
    yoshi_cookie_item = None
    normal_item = None
    rare_item = None

    # Boss shuffle attributes.
    anchor = False
    ratio_hp = 1.0
    ratio_fp = 1.0
    ratio_attack = 1.0
    ratio_defense = 1.0
    ratio_magic_attack = 1.0
    ratio_magic_defense = 1.0
    ratio_speed = 1.0
    ratio_evade = 1.0
    ratio_magic_evade = 1.0
    name_override = ''

    #shuffled overworld sprites
    overworld_sprite = None
    overworld_npc = None
    battle_sprite = None
    battle_npc = None
    battle_sprite_is_wide = False
    battle_sprite_is_tall = False
    overworld_mold = 0
    overworld_sequence = 0
    overworld_sprite_plus = 0
    battle_mold = 0
    battle_sequence = 0
    battle_sprite_plus = 0
    other_npcs = []
    other_sprites = []
    statue_only = False
    sprite_width = 32;
    sprite_height = 32;
    overworld_sesw_only = False
    battle_sesw_only = False
    overworld_front_sequence = 0
    overworld_back_sequence = 1
    battle_front_sequence = 0
    battle_back_sequence = 1
    overworld_invert_se_sw = False
    battle_invert_se_sw = False
    overworld_freeze = False
    battle_freeze = False
    overworld_extra_sequence = False
    battle_extra_sequence = False
    overworld_push_sequence = False
    overworld_push_length = 0
    battle_push_sequence = False
    battle_push_length = 0
    overworld_northeast_mold = False
    battle_northeast_mold = False
    overworld_dont_reverse_northeast = False
    czar_sprite = []
    overworld_is_skinny = False
    overworld_is_empty = False
    fat_sidekicks = False
    empty_sidekicks = False
    shadow = None
    overworld_solidity = []
    battle_solidity = []
    overworld_y_shift = 0
    battle_y_shift = 0

    statue_east_shift = False
    statue_southeast_shift = False
    statue_south_shift = False
    statue_southwest_shift = False
    statue_west_shift = False
    statue_northwest_shift = False
    statue_north_shift = False
    statue_northeast_shift = False
    opposite_statue_east_shift = False
    opposite_statue_southeast_shift = False
    opposite_statue_south_shift = False
    opposite_statue_southwest_shift = False
    opposite_statue_west_shift = False
    opposite_statue_northwest_shift = False
    opposite_statue_north_shift = False
    opposite_statue_northeast_shift = False

    statue_mold = None

    def __init__(self, world):
        """

        Args:
            world (randomizer.logic.main.GameWorld):

        """
        self.world = world

        # Set instance normal and rare item rewards to the actual item instances for this world.
        if self.normal_item is not None:
            self.normal_item = self.world.get_item_instance(self.normal_item)
        if self.rare_item is not None:
            self.rare_item = self.world.get_item_instance(self.rare_item)
        # Check world type....
        self.script = list(battlescripts.scripts[self.index])

    def __str__(self):
        return "<{}>".format(self.name)

    def __repr__(self):
        return str(self)

    @property
    def name(self):
        return self.__class__.__name__

    @staticmethod
    def round_for_battle_script(val):
        """Round a HP value for battle event data.  This means round to an integer, and make sure it does have the
        values 0xfe or 0xff because these are special values that stop processing the battle script.

        Args:
            val (float|int): Base value to confirm.

        Returns:
            int: Rounded HP value.

        """
        ret = int(round(val))
        m = ret % 256

        # 0xfe
        if m == 254:
            ret += 2
        # 0xff
        elif m == 255:
            ret += 1

        # If starting value was positive, final value must be at least 1 since zero is a death trigger that ends battle.
        if val > 0:
            return max(1, ret)
        else:
            return ret

    @classmethod
    def get_world_instance(cls, world):
        """

        Args:
            world (randomizer.logic.main.GameWorld): World to get instance of this enemy class for.

        Returns:
            Enemy: Instance of the enemy for this world.

        """
        return world.enemies_dict[cls.index]

    @property
    def rank(self):
        """Calculate rough difficulty ranking of enemy based on HP and attack stats.

        :rtype: int
        """
        hp = self.hp if self.hp >= 10 else 100
        return hp * max(self.attack, self.magic_attack, 1)

    @property
    def psychopath_text(self):
        """Make Psychopath text to show elemental weaknesses and immunities.

        :rtype: str
        """
        desc = ''

        # Elemental immunities.
        if self.resistances:
            desc += '\x7C'
            desc += utils.add_desc_fields((
                ('\x7E', 6, self.resistances),
                ('\x7D', 4, self.resistances),
                ('\x7F', 5, self.resistances),
                ('\x85', 7, self.resistances),
            ))
        else:
            desc += '\x20' * 5

        desc += '\x20'

        # Elemental weaknesses.
        if self.weaknesses:
            desc += '\x7B'
            desc += utils.add_desc_fields((
                ('\x7E', 6, self.weaknesses),
                ('\x7D', 4, self.weaknesses),
                ('\x7F', 5, self.weaknesses),
                ('\x85', 7, self.weaknesses),
            ))
        else:
            desc += '\x20' * 5

        desc += '\x20\x20'

        # Status vulnerabilities.
        vulnerabilities = [i for i in range(4) if i not in self.status_immunities]
        if vulnerabilities:
            desc += utils.add_desc_fields((
                ('\x82', 0, vulnerabilities),
                ('\x80', 1, vulnerabilities),
                ('\x83', 2, vulnerabilities),
                ('\x81', 3, vulnerabilities),
                ('\x84\x84', True, not self.death_immune),
            ))
        else:
            desc += '\x20' * 6

        desc += '\x02'

        return desc

    def get_similar(self):
        """Get a similar enemy to this one for formation shuffling based on rank.

        :rtype: Enemy
        """
        # If we're a boss enemy, treat as unique.
        if self.boss:
            return self

        # Get all non-boss candidates sorted by rank.
        candidates = [e for e in self.world.enemies if not e.boss]
        candidates = sorted(candidates, key=lambda e: (e.rank, e.index))

        # If this is a special enemy, don't replace it.
        if self.rank < 0:
            return self
        elif self not in candidates:
            return self

        # Sort by rank and mutate our position within the list to get a replacement enemy.
        index = candidates.index(self)
        index = utils.mutate_normal(index, maximum=len(candidates) - 1)
        return candidates[index]

    def fix_hp_counters(self):
        """Fixes up battlescripts that rely on countering when their HP goes down.

        Returns: None

        """
        dex = 0
        script = self.script
        hps = self.hp_counter_ratios
        for i in range(len(script)):
            (name, val) = script[i]
            # Skip any HP checks for 0 because these are death checks that end the fight.
            if name == 'if_hp' and val[0] > 0:
                hp = self.round_for_battle_script(self.hp * hps[dex])
                script[i] = ('if_hp', [hp])
                dex += 1
                if dex == len(hps):
                    break
        else:
            raise Exception('More HP values than counters')

    def get_patch(self):
        """Get patch for this enemy.

        Returns:
            randomizer.logic.patch.Patch: Patch data

        """
        patch = Patch()

        # Main stats.
        data = bytearray()
        data += utils.ByteField(self.hp, num_bytes=2).as_bytes()
        data += utils.ByteField(self.speed).as_bytes()
        data += utils.ByteField(self.attack).as_bytes()
        data += utils.ByteField(self.defense).as_bytes()
        data += utils.ByteField(self.magic_attack).as_bytes()
        data += utils.ByteField(self.magic_defense).as_bytes()
        data += utils.ByteField(self.fp).as_bytes()
        data += utils.ByteField(self.evade).as_bytes()
        data += utils.ByteField(self.magic_evade).as_bytes()
        patch.add_data(self.address, data)

        # Special defense bits, sound on hit is top half.
        data = bytearray()
        hit_special_defense = 1 if self.invincible else 0
        hit_special_defense |= (1 if self.death_immune else 0) << 1
        hit_special_defense |= self.morph_chance << 2
        hit_special_defense |= self.sound_on_hit
        data.append(hit_special_defense)

        # Elemental resistances.
        data += utils.BitMapSet(1, self.resistances).as_bytes()

        # Elemental weaknesses byte (top half), sound on approach is bottom half.
        weaknesses_approach = self.sound_on_approach
        for weakness in self.weaknesses:
            weaknesses_approach |= 1 << weakness
        data.append(weaknesses_approach)

        # Status immunities.
        data += utils.BitMapSet(1, self.status_immunities).as_bytes()

        patch.add_data(self.address + 11, data)

        # Flower bonus.
        bonus_addr = self.FLOWER_BONUS_BASE_ADDRESS + self.index
        bonus = self.flower_bonus_chance << 4
        bonus |= self.flower_bonus_type
        patch.add_data(bonus_addr, utils.ByteField(bonus).as_bytes())

        # Build reward data patch.
        data = bytearray()
        data += utils.ByteField(self.xp, num_bytes=2).as_bytes()
        data += utils.ByteField(self.coins).as_bytes()
        data += utils.ByteField(self.yoshi_cookie_item.index if self.yoshi_cookie_item else 0xff).as_bytes()
        data += utils.ByteField(self.normal_item.index if self.normal_item else 0xff).as_bytes()
        data += utils.ByteField(self.rare_item.index if self.rare_item else 0xff).as_bytes()
        patch.add_data(self.reward_address, data)

        # If we have an override name, add to the patch data.
        if self.name_override:
            addr = self.NAME_BASE_ADDRESS + (self.index * 13)
            patch.add_data(addr, self.name_override.upper().encode().ljust(13, b'\x20'))

        return patch

    def patch_script(self):
        if self.world.open_mode and self.hp_counter_ratios:
            self.fix_hp_counters()

        if self.world.settings.is_flag_enabled(flags.NoOHKO) and type(self) in (
                MarioClone, MallowClone, GenoClone, BowserClone, PeachClone):
            for i in range(len(self.script)):
                name, args = self.script[i]
                if name == 'if_item':
                    # Good luck using that in battle
                    self.script[i] = ('if_item', [items.BrightCard])

    @classmethod
    def build_psychopath_patch(cls, world):
        """Build patch data for Psychopath text.  These use pointers, so we need to do them all together.

        :type world: randomizer.logic.main.GameWorld
        :return: Patch data.
        :rtype: randomizer.logic.patch.Patch
        """
        patch = Patch()

        # Begin text data with a single null byte to use for all empty text to save space.
        pointer_data = bytearray()
        text_data = bytearray()
        text_data.append(0x00)

        # Make list of blank text for all enemies, and get text for each valid enemy we have based on index.
        descriptions = [''] * NUM_ENEMIES
        for enemy in world.enemies:
            descriptions[enemy.index] = enemy.psychopath_text

        # Now build the actual pointer data.
        for desc in descriptions:
            # If the description is empty, just use the null byte at the very beginning.
            if not desc:
                pointer = cls.BASE_PSYCHOPATH_DATA_ADDRESS - cls.PSYCHOPATH_DATA_POINTER_OFFSET
                pointer_data += utils.ByteField(pointer, num_bytes=2).as_bytes()
                continue

            # Compute pointer from base address and current data length.
            pointer = cls.BASE_PSYCHOPATH_DATA_ADDRESS + len(text_data) - cls.PSYCHOPATH_DATA_POINTER_OFFSET
            pointer_data += utils.ByteField(pointer, num_bytes=2).as_bytes()

            # Add null byte to terminate the text string.
            desc = desc.encode('latin1')
            desc += bytes([0x00])
            text_data += desc

        # Sanity check that pointer data has the correct number of items.
        if len(pointer_data) != NUM_ENEMIES * 2:
            raise ValueError("Wrong length for pointer data, something went wrong...")

        # Add pointer data, then add text data.
        patch.add_data(cls.BASE_PSYCHOPATH_POINTER_ADDRESS, pointer_data)
        patch.add_data(cls.BASE_PSYCHOPATH_DATA_ADDRESS, text_data)

        return patch


# ********************* Actual data classes

class Terrapin(Enemy):
    index = 0
    address = 0x390226
    hp = 10
    speed = 10
    attack = 1
    defense = 8
    magic_defense = 1
    fp = 100
    morph_chance = 3
    sound_on_hit = 80
    palette = 16
    flower_bonus_type = 3

    # Reward attributes
    reward_address = 0x39162a
    yoshi_cookie_item = items.Mushroom


class Spikey(Enemy):
    index = 1
    address = 0x390236
    hp = 20
    speed = 14
    attack = 6
    defense = 11
    magic_attack = 4
    magic_defense = 2
    fp = 100
    morph_chance = 2
    sound_on_approach = 1
    resistances = [7]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 1

    # Reward attributes
    reward_address = 0x391630
    xp = 1
    coins = 2
    yoshi_cookie_item = items.Bracer
    normal_item = items.HoneySyrup


class Skytroopa(Enemy):
    index = 2
    address = 0x390246
    hp = 10
    speed = 18
    attack = 4
    defense = 16
    magic_attack = 6
    magic_defense = 4
    fp = 100
    evade = 8
    morph_chance = 3
    sound_on_hit = 80
    sound_on_approach = 1
    weaknesses = [7]
    palette = 8
    flower_bonus_type = 5
    flower_bonus_chance = 3
    flying = True

    # Reward attributes
    reward_address = 0x391636
    xp = 1
    coins = 1
    yoshi_cookie_item = items.Mushroom
    rare_item = items.Mushroom


class MadMallet(Enemy):
    index = 3
    address = 0x390866
    boss = True
    hp = 200
    speed = 20
    attack = 120
    defense = 80
    magic_attack = 34
    magic_defense = 85
    fp = 100
    morph_chance = 3
    sound_on_hit = 80
    weaknesses = [5]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391888
    xp = 20
    coins = 1
    yoshi_cookie_item = items.Energizer

    # Boss shuffle attributes.
    ratio_hp = 0.2222
    ratio_fp = 0.3333
    ratio_attack = 0.75
    ratio_defense = 0.8
    ratio_magic_attack = 0.7234
    ratio_magic_defense = 1.4167
    ratio_speed = 1.3333
    ratio_evade = 0.0
    ratio_magic_evade = 0.0


class Shaman(Enemy):
    index = 4
    address = 0x390706
    hp = 150
    speed = 9
    attack = 92
    defense = 50
    magic_attack = 80
    magic_defense = 90
    fp = 100
    morph_chance = 3
    sound_on_hit = 80
    palette = 8
    flower_bonus_type = 5
    flower_bonus_chance = 3

    # Reward attributes
    reward_address = 0x3917fe
    xp = 17
    coins = 4
    yoshi_cookie_item = items.RoyalSyrup
    normal_item = items.RoyalSyrup
    rare_item = items.MapleSyrup


class Crook(Enemy):
    index = 5
    address = 0x3902e6
    hp = 38
    speed = 22
    attack = 35
    defense = 32
    magic_attack = 12
    magic_defense = 25
    fp = 100
    evade = 40
    magic_evade = 40
    morph_chance = 3
    palette = 8
    flower_bonus_type = 4
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391672
    xp = 10
    coins = 10
    yoshi_cookie_item = items.MidMushroom
    rare_item = items.HoneySyrup


class Goomba(Enemy):
    index = 6
    address = 0x390256
    hp = 16
    speed = 13
    attack = 3
    defense = 3
    magic_attack = 1
    magic_defense = 1
    fp = 100
    morph_chance = 3
    sound_on_approach = 2
    weaknesses = [6]
    palette = 8
    flower_bonus_type = 3
    flower_bonus_chance = 3

    # Reward attributes
    reward_address = 0x39163c
    xp = 1
    yoshi_cookie_item = items.Mushroom


class PiranhaPlant(Enemy):
    index = 7
    address = 0x390396
    hp = 168
    speed = 6
    attack = 45
    defense = 14
    magic_attack = 20
    magic_defense = 22
    fp = 4
    morph_chance = 2
    sound_on_hit = 16
    sound_on_approach = 2
    resistances = [7]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x3916b4
    xp = 5
    coins = 5
    yoshi_cookie_item = items.SleepyBomb
    normal_item = items.MapleSyrup


class Amanita(Enemy):
    index = 8
    address = 0x390346
    hp = 52
    speed = 12
    attack = 35
    defense = 30
    magic_attack = 31
    magic_defense = 18
    fp = 100
    evade = 10
    magic_evade = 10
    morph_chance = 3
    sound_on_hit = 80
    sound_on_approach = 3
    weaknesses = [6]
    palette = 8
    flower_bonus_type = 3
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391696
    xp = 3
    yoshi_cookie_item = items.BadMushroom
    rare_item = items.Mushroom


class Goby(Enemy):
    index = 9
    address = 0x3902b6
    hp = 40
    speed = 12
    attack = 22
    defense = 14
    magic_attack = 2
    magic_defense = 10
    fp = 100
    evade = 20
    morph_chance = 3
    sound_on_hit = 80
    sound_on_approach = 1
    weaknesses = [5]
    palette = 8
    flower_bonus_type = 4
    flower_bonus_chance = 1
    flying = True
    high_flying = True

    # Reward attributes
    reward_address = 0x391660
    xp = 3
    coins = 2
    yoshi_cookie_item = items.Mushroom
    normal_item = items.Mushroom


class Bloober(Enemy):
    index = 10
    address = 0x390536
    hp = 130
    speed = 23
    attack = 80
    defense = 36
    magic_attack = 21
    magic_defense = 16
    fp = 100
    evade = 20
    morph_chance = 3
    sound_on_hit = 128
    weaknesses = [5, 6]
    palette = 8
    flower_bonus_type = 5
    flower_bonus_chance = 10
    flying = True

    # Reward attributes
    reward_address = 0x391756
    xp = 12
    yoshi_cookie_item = items.Elixir
    normal_item = items.MaxMushroom
    rare_item = items.HoneySyrup


class BandanaRed(Enemy):
    index = 11
    address = 0x390576
    hp = 120
    speed = 20
    attack = 78
    defense = 60
    magic_attack = 25
    magic_defense = 25
    fp = 100
    morph_chance = 2
    sound_on_hit = 16
    weaknesses = [5, 6]
    palette = 8
    flower_bonus_type = 4
    flower_bonus_chance = 3

    # Reward attributes
    reward_address = 0x39176e
    xp = 18
    coins = 10
    yoshi_cookie_item = items.Energizer
    rare_item = items.Mushroom


class Lakitu(Enemy):
    index = 12
    address = 0x3903f6
    hp = 124
    speed = 28
    attack = 45
    defense = 43
    magic_attack = 35
    magic_defense = 40
    fp = 100
    evade = 13
    morph_chance = 3
    sound_on_hit = 112
    resistances = [5]
    palette = 16
    flower_bonus_type = 1
    flower_bonus_chance = 2
    flying = True

    # Reward attributes
    reward_address = 0x3916d8
    xp = 10
    coins = 3
    yoshi_cookie_item = items.MapleSyrup
    normal_item = items.MapleSyrup
    rare_item = items.MidMushroom


class Birdy(Enemy):
    index = 13
    address = 0x3906d6
    hp = 150
    speed = 23
    attack = 110
    defense = 75
    magic_attack = 55
    magic_defense = 13
    fp = 100
    evade = 18
    morph_chance = 3
    sound_on_hit = 16
    sound_on_approach = 2
    resistances = [6]
    weaknesses = [4]
    status_immunities = [1]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2
    flying = True

    # Reward attributes
    reward_address = 0x3917ec
    xp = 16
    coins = 3
    yoshi_cookie_item = items.Energizer
    normal_item = items.Energizer


class Pinwheel(Enemy):
    index = 14
    address = 0x3906f6
    hp = 99
    speed = 32
    attack = 120
    defense = 90
    magic_attack = 70
    magic_defense = 66
    fp = 100
    evade = 35
    morph_chance = 3
    sound_on_hit = 48
    resistances = [5]
    status_immunities = [0, 1, 2, 3]
    palette = 8
    flower_bonus_type = 4
    flower_bonus_chance = 3

    # Reward attributes
    reward_address = 0x3917f8
    xp = 23
    yoshi_cookie_item = items.PickMeUp
    rare_item = items.PickMeUp


class Ratfunk(Enemy):
    index = 15
    address = 0x390296
    hp = 32
    speed = 21
    attack = 20
    defense = 14
    magic_defense = 6
    fp = 100
    evade = 30
    morph_chance = 3
    weaknesses = [6]
    palette = 8
    flower_bonus_type = 4
    flower_bonus_chance = 4

    # Reward attributes
    reward_address = 0x391654
    xp = 2
    coins = 6
    yoshi_cookie_item = items.Mushroom
    normal_item = items.AbleJuice


class K9(Enemy):
    index = 16
    address = 0x390266
    hp = 30
    speed = 19
    attack = 13
    defense = 13
    magic_attack = 1
    magic_defense = 10
    fp = 100
    morph_chance = 2
    palette = 8
    flower_bonus_type = 4
    flower_bonus_chance = 3

    # Reward attributes
    reward_address = 0x391642
    xp = 2
    yoshi_cookie_item = items.Energizer


class Magmite(Enemy):
    index = 17
    address = 0x3903c6
    hp = 26
    speed = 2
    attack = 45
    defense = 70
    magic_attack = 3
    magic_defense = 1
    fp = 100
    morph_chance = 2
    sound_on_hit = 80
    resistances = [7]
    weaknesses = [4]
    palette = 8
    flower_bonus_type = 5
    flower_bonus_chance = 10

    # Reward attributes
    reward_address = 0x3916c6
    xp = 5
    coins = 1
    yoshi_cookie_item = items.Bracer


class TheBigBoo(Enemy):
    index = 18
    address = 0x3902a6
    hp = 43
    speed = 17
    attack = 18
    magic_attack = 18
    magic_defense = 24
    fp = 12
    evade = 40
    morph_chance = 2
    resistances = [7]
    status_immunities = [3]
    palette = 8
    flower_bonus_type = 2
    flower_bonus_chance = 3

    # Reward attributes
    reward_address = 0x39165a
    xp = 2
    yoshi_cookie_item = items.FrightBomb
    normal_item = items.HoneySyrup
    rare_item = items.PureWater


class DryBones(Enemy):
    index = 19
    address = 0x390596
    boss = True
    speed = 9
    attack = 74
    magic_attack = 7
    fp = 100
    morph_chance = 3
    sound_on_hit = 144
    sound_on_approach = 6
    weaknesses = [5]
    palette = 8
    flower_bonus_type = 2
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x39177a
    xp = 12
    coins = 5
    yoshi_cookie_item = items.Mushroom
    normal_item = items.MaxMushroom
    rare_item = items.PureWater


class Greaper(Enemy):
    index = 20
    address = 0x3905b6
    hp = 148
    speed = 30
    attack = 72
    defense = 50
    magic_attack = 40
    magic_defense = 20
    fp = 100
    evade = 30
    magic_evade = 30
    morph_chance = 3
    sound_on_hit = 16
    resistances = [7]
    weaknesses = [5]
    palette = 8
    flower_bonus_type = 5
    flower_bonus_chance = 3

    # Reward attributes
    reward_address = 0x391786
    xp = 13
    yoshi_cookie_item = items.HoneySyrup
    normal_item = items.HoneySyrup
    rare_item = items.PureWater


class Sparky(Enemy):
    index = 21
    address = 0x390386
    hp = 120
    speed = 19
    attack = 40
    defense = 1
    magic_attack = 38
    magic_defense = 50
    fp = 12
    evade = 6
    morph_chance = 1
    sound_on_approach = 2
    resistances = [6]
    weaknesses = [4]
    palette = 8
    flower_bonus_type = 2
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x3916ae
    xp = 4
    coins = 1
    yoshi_cookie_item = items.FireBomb


class Chomp(Enemy):
    index = 22
    address = 0x390456
    hp = 100
    speed = 10
    attack = 60
    defense = 65
    magic_attack = 5
    magic_defense = 31
    fp = 100
    morph_chance = 2
    sound_on_hit = 32
    weaknesses = [5]
    palette = 16
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x3916fc
    xp = 10
    yoshi_cookie_item = items.Bracer
    normal_item = items.Mushroom


class Pandorite(Enemy):
    index = 23
    address = 0x390936
    boss = True
    hp = 300
    speed = 1
    attack = 30
    defense = 20
    magic_attack = 20
    magic_defense = 20
    fp = 50
    death_immune = True
    sound_on_hit = 32
    resistances = [4, 5, 6]
    weaknesses = [7]
    status_immunities = [0, 1, 2, 3]
    palette = 16
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x3918fa
    xp = 20
    coins = 30
    yoshi_cookie_item = items.Mushroom
    normal_item = items.FlowerJar
    rare_item = items.FlowerJar

    #shuffled overworld sprites
    overworld_sprite = 195
    overworld_npc = 199
    battle_sprite = 279
    overworld_sequence = 4
    statue_only = True
    sprite_width = 37
    sprite_height = 40
    overworld_freeze = True
    battle_sesw_only = True
    overworld_sesw_only = True
    battle_push_sequence = 3
    battle_push_length = 22
    overworld_is_empty = True
    shadow = SMALL_SHADOW
    overworld_solidity = [1, 1, 1]
    overworld_y_shift = 0


class ShyRanger(Enemy):
    index = 24
    address = 0x3903a6
    hp = 300
    speed = 43
    attack = 100
    defense = 80
    magic_attack = 4
    magic_defense = 10
    fp = 100
    evade = 50
    death_immune = True
    morph_chance = 1
    resistances = [4, 5, 6, 7]
    palette = 8
    flower_bonus_type = 5
    flower_bonus_chance = 5

    # Reward attributes
    reward_address = 0x3916ba
    xp = 60
    coins = 1
    yoshi_cookie_item = items.KerokeroCola


class Bobomb(Enemy):
    index = 25
    address = 0x3903b6
    boss = True
    hp = 90
    speed = 1
    attack = 50
    defense = 38
    magic_attack = 1
    magic_defense = 10
    fp = 100
    sound_on_hit = 80
    weaknesses = [6, 7]
    palette = 8
    flower_bonus_type = 2
    flower_bonus_chance = 4

    # Reward attributes
    reward_address = 0x3916c0
    xp = 4
    yoshi_cookie_item = items.Mushroom
    normal_item = items.PickMeUp

    # Boss shuffle attributes.
    ratio_hp = 0.075
    ratio_fp = 10.0
    ratio_attack = 0.83
    ratio_defense = 0.9
    ratio_magic_attack = 0.05
    ratio_magic_defense = 0.25
    ratio_speed = 0.07
    ratio_evade = 0.0
    ratio_magic_evade = 0.0


class Spookum(Enemy):
    index = 26
    address = 0x390436
    hp = 98
    speed = 18
    attack = 50
    defense = 45
    magic_attack = 32
    magic_defense = 5
    fp = 100
    morph_chance = 2
    sound_on_hit = 128
    weaknesses = [4]
    palette = 8
    flower_bonus_type = 4
    flower_bonus_chance = 1

    # Reward attributes
    reward_address = 0x3916f0
    xp = 8
    coins = 4
    yoshi_cookie_item = items.SleepyBomb
    normal_item = items.MidMushroom


class HammerBro(Enemy):
    index = 27
    address = 0x390c26
    boss = True
    hp = 50
    speed = 10
    attack = 6
    defense = 13
    magic_attack = 6
    magic_defense = 8
    fp = 1
    evade = 10
    death_immune = True
    sound_on_hit = 80
    status_immunities = [1]
    palette = 16
    flower_bonus_type = 2
    flower_bonus_chance = 4

    # Reward attributes
    reward_address = 0x391a9e
    xp = 3
    coins = 10
    yoshi_cookie_item = items.Mushroom
    normal_item = items.FlowerJar
    rare_item = items.FlowerJar

    # Boss shuffle attributes.
    ratio_hp = 0.5
    ratio_fp = 0.5

    #shuffled overworld sprites
    overworld_sprite = 545
    overworld_sesw_only = True
    battle_sprite = 283
    battle_npc = 283
    statue_only = True
    battle_sprite_is_tall = True
    sprite_width = 40;
    sprite_height = 45;
    battle_sesw_only = True
    battle_push_sequence = 3
    battle_push_length = 40
    overworld_is_empty = True
    shadow = SMALL_SHADOW
    overworld_solidity = [2, 2, 6]
    battle_solidity = [8, 7, 19]
    overworld_y_shift = 1
    battle_y_shift = 1

class Buzzer(Enemy):
    index = 28
    address = 0x390356
    hp = 43
    speed = 25
    attack = 37
    defense = 15
    magic_attack = 4
    magic_defense = 1
    fp = 100
    evade = 30
    morph_chance = 3
    sound_on_hit = 16
    sound_on_approach = 1
    weaknesses = [5, 7]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2
    flying = True

    # Reward attributes
    reward_address = 0x39169c
    xp = 4
    coins = 1
    yoshi_cookie_item = items.Mushroom


class Ameboid(Enemy):
    index = 29
    address = 0x3908c6
    hp = 220
    speed = 1
    attack = 130
    defense = 1
    magic_attack = 30
    magic_defense = 120
    fp = 100
    magic_evade = 50
    morph_chance = 3
    sound_on_approach = 1
    resistances = [7]
    weaknesses = [6]
    palette = 8
    flower_bonus_type = 3
    flower_bonus_chance = 3

    # Reward attributes
    reward_address = 0x3918ca
    xp = 10
    yoshi_cookie_item = items.MaxMushroom
    normal_item = items.RoyalSyrup


class Gecko(Enemy):
    index = 30
    address = 0x3904f6
    hp = 92
    speed = 22
    attack = 68
    defense = 46
    magic_attack = 9
    magic_defense = 32
    fp = 100
    evade = 14
    morph_chance = 3
    sound_on_hit = 128
    resistances = [5]
    weaknesses = [6]
    palette = 8
    flower_bonus_type = 3
    flower_bonus_chance = 4

    # Reward attributes
    reward_address = 0x39173e
    xp = 10
    yoshi_cookie_item = items.FroggieDrink


class Wiggler(Enemy):
    index = 31
    address = 0x390336
    hp = 120
    speed = 10
    attack = 40
    defense = 25
    magic_attack = 18
    magic_defense = 20
    fp = 100
    morph_chance = 3
    sound_on_hit = 96
    weaknesses = [6]
    palette = 16
    flower_bonus_type = 5
    flower_bonus_chance = 4

    # Reward attributes
    reward_address = 0x391690
    xp = 6
    coins = 10
    yoshi_cookie_item = items.AbleJuice
    rare_item = items.HoneySyrup


class Crusty(Enemy):
    index = 32
    address = 0x390556
    hp = 80
    speed = 6
    attack = 100
    defense = 100
    magic_attack = 12
    magic_defense = 35
    fp = 100
    morph_chance = 2
    sound_on_hit = 32
    resistances = [7]
    weaknesses = [5, 6]
    palette = 24
    flower_bonus_type = 1
    flower_bonus_chance = 8

    # Reward attributes
    reward_address = 0x391762
    xp = 25
    coins = 7
    yoshi_cookie_item = items.Bracer
    normal_item = items.RoyalSyrup
    rare_item = items.HoneySyrup


class Magikoopa(Enemy):
    index = 33
    address = 0x391186
    boss = True
    hp = 1600
    speed = 12
    attack = 100
    defense = 60
    magic_attack = 120
    magic_defense = 100
    fp = 250
    death_immune = True
    sound_on_hit = 16
    status_immunities = [0, 1, 2]
    palette = 16
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391876
    xp = 30
    coins = 10
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 1.0
    ratio_fp = 1.0

    #overworld sprites
    overworld_npc = 190
    overworld_sprite = 129
    battle_npc = 289
    battle_sprite = 353
    sprite_height = 42
    sprite_width = 45
    overworld_extra_sequence = 10
    battle_push_sequence = 3
    battle_push_length = 48
    overworld_push_sequence = 10
    overworld_push_length = 52
    overworld_is_skinny = True
    shadow = MED_SHADOW
    overworld_solidity = [3, 3, 10]
    overworld_y_shift = 1
    statue_east_shift = 2
    opposite_statue_west_shift = 4
    opposite_statue_south_shift = 1



class Leuko(Enemy):
    index = 34
    address = 0x390566
    hp = 220
    speed = 3
    attack = 65
    defense = 50
    magic_attack = 42
    magic_defense = 60
    fp = 100
    magic_evade = 30
    morph_chance = 1
    sound_on_hit = 64
    resistances = [5]
    weaknesses = [6]
    palette = 16
    flower_bonus_type = 3
    flower_bonus_chance = 6

    # Reward attributes
    reward_address = 0x391768
    xp = 20
    coins = 3
    yoshi_cookie_item = items.Megalixir
    normal_item = items.HoneySyrup
    rare_item = items.MidMushroom


class Jawful(Enemy):
    index = 35
    address = 0x390726
    hp = 278
    speed = 200
    attack = 130
    defense = 110
    magic_attack = 8
    magic_defense = 12
    fp = 100
    morph_chance = 1
    sound_on_hit = 32
    status_immunities = [3]
    palette = 16
    flower_bonus_type = 3
    flower_bonus_chance = 3

    # Reward attributes
    reward_address = 0x39180a
    xp = 27
    yoshi_cookie_item = items.RockCandy
    rare_item = items.SleepyBomb


class Enigma(Enemy):
    index = 36
    address = 0x3903d6
    hp = 150
    speed = 25
    attack = 55
    defense = 40
    magic_attack = 30
    magic_defense = 35
    fp = 100
    evade = 20
    morph_chance = 2
    sound_on_hit = 96
    sound_on_approach = 1
    weaknesses = [7]
    palette = 16
    flower_bonus_type = 3
    flower_bonus_chance = 5

    # Reward attributes
    reward_address = 0x3916cc
    xp = 10
    coins = 5
    yoshi_cookie_item = items.Energizer
    normal_item = items.MapleSyrup


class Blaster(Enemy):
    index = 37
    address = 0x390466
    hp = 120
    speed = 1
    attack = 70
    defense = 70
    magic_defense = 10
    fp = 100
    morph_chance = 2
    weaknesses = [5]
    palette = 24
    flower_bonus_type = 2
    flower_bonus_chance = 6

    # Reward attributes
    reward_address = 0x391702
    xp = 12
    yoshi_cookie_item = items.FrightBomb
    rare_item = items.PickMeUp


class Guerrilla(Enemy):
    index = 38
    address = 0x390366
    hp = 135
    speed = 7
    attack = 42
    defense = 32
    magic_attack = 1
    magic_defense = 5
    fp = 100
    morph_chance = 3
    sound_on_hit = 96
    sound_on_approach = 4
    weaknesses = [6]
    palette = 24
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x3916a2
    xp = 8
    coins = 8
    yoshi_cookie_item = items.AbleJuice
    rare_item = items.AbleJuice


class Babayaga(Enemy):
    index = 39
    address = 0x3909a6
    hp = 10
    fp = 100
    morph_chance = 3
    sound_on_hit = 96
    palette = 32
    flower_bonus_type = 2
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391924
    yoshi_cookie_item = items.Mushroom


class Hobgoblin(Enemy):
    index = 40
    address = 0x3902c6
    hp = 50
    speed = 5
    attack = 22
    defense = 22
    magic_attack = 8
    magic_defense = 12
    fp = 8
    morph_chance = 3
    sound_on_hit = 16
    weaknesses = [6]
    palette = 16
    flower_bonus_type = 3
    flower_bonus_chance = 6

    # Reward attributes
    reward_address = 0x391666
    xp = 4
    coins = 3
    yoshi_cookie_item = items.PureWater
    normal_item = items.PureWater
    rare_item = items.PureWater


class Reacher(Enemy):
    index = 41
    address = 0x3905c6
    hp = 184
    speed = 3
    attack = 95
    defense = 75
    magic_attack = 8
    fp = 100
    morph_chance = 3
    sound_on_hit = 32
    weaknesses = [5]
    palette = 24
    flower_bonus_type = 2
    flower_bonus_chance = 6

    # Reward attributes
    reward_address = 0x39178c
    xp = 30
    coins = 8
    yoshi_cookie_item = items.PickMeUp
    normal_item = items.RoyalSyrup
    rare_item = items.PickMeUp


class Shogun(Enemy):
    index = 42
    address = 0x390626
    hp = 150
    speed = 12
    attack = 100
    defense = 80
    magic_attack = 1
    magic_defense = 32
    fp = 100
    morph_chance = 3
    sound_on_hit = 48
    weaknesses = [4]
    status_immunities = [1, 3]
    palette = 16
    flower_bonus_type = 2
    flower_bonus_chance = 3

    # Reward attributes
    reward_address = 0x3917b6
    xp = 24
    coins = 10
    yoshi_cookie_item = items.RoyalSyrup
    rare_item = items.PickMeUp


class Orbuser(Enemy):
    index = 43
    address = 0x390496
    hp = 8
    speed = 15
    attack = 42
    defense = 80
    magic_attack = 28
    magic_defense = 40
    fp = 20
    morph_chance = 3
    sound_on_hit = 80
    resistances = [4, 5, 6]
    palette = 16
    flower_bonus_type = 3
    flower_bonus_chance = 4

    # Reward attributes
    reward_address = 0x391714
    xp = 5
    coins = 2
    yoshi_cookie_item = items.MapleSyrup
    rare_item = items.HoneySyrup


class HeavyTroopa(Enemy):
    index = 44
    address = 0x390736
    hp = 250
    speed = 3
    attack = 160
    defense = 100
    magic_attack = 1
    magic_defense = 50
    fp = 100
    evade = 2
    morph_chance = 1
    sound_on_hit = 96
    sound_on_approach = 1
    weaknesses = [7]
    palette = 16
    flower_bonus_type = 2
    flower_bonus_chance = 8
    flying = True

    # Reward attributes
    reward_address = 0x391810
    xp = 32
    coins = 4
    yoshi_cookie_item = items.Crystalline
    normal_item = items.Crystalline


class Shadow(Enemy):
    index = 45
    address = 0x3902d6
    hp = 85
    speed = 18
    attack = 24
    defense = 5
    magic_attack = 20
    magic_defense = 20
    fp = 14
    evade = 10
    morph_chance = 3
    sound_on_hit = 96
    resistances = [7]
    palette = 16
    flower_bonus_type = 5
    flower_bonus_chance = 3

    # Reward attributes
    reward_address = 0x39166c
    xp = 3
    coins = 2
    yoshi_cookie_item = items.HoneySyrup
    normal_item = items.PickMeUp


class Cluster(Enemy):
    index = 46
    address = 0x3903e6
    hp = 60
    speed = 20
    attack = 50
    defense = 50
    magic_attack = 21
    magic_defense = 10
    fp = 100
    morph_chance = 3
    sound_on_hit = 32
    sound_on_approach = 5
    resistances = [7]
    palette = 16
    flower_bonus_type = 2
    flower_bonus_chance = 4

    # Reward attributes
    reward_address = 0x3916d2
    xp = 8
    coins = 8
    yoshi_cookie_item = items.PickMeUp
    rare_item = items.PickMeUp


class Bahamutt(Enemy):
    index = 47
    address = 0x390996
    boss = True
    hp = 500
    speed = 8
    attack = 170
    defense = 100
    magic_attack = 80
    magic_defense = 20
    fp = 100
    sound_on_hit = 32
    resistances = [6]
    weaknesses = [4]
    status_immunities = [1, 3]
    palette = 32
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x39191e
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.3125
    ratio_fp = 0.4
    ratio_attack = 1.7
    ratio_defense = 1.6667
    ratio_magic_attack = 0.6667
    ratio_magic_defense = 0.2
    ratio_speed = 0.6667
    ratio_evade = 0.0
    ratio_magic_evade = 0.0


class Octolot(Enemy):
    index = 48
    address = 0x390376
    hp = 99
    speed = 3
    attack = 38
    defense = 27
    magic_attack = 25
    magic_defense = 30
    fp = 100
    evade = 10
    morph_chance = 3
    sound_on_hit = 112
    weaknesses = [6, 7]
    palette = 24
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x3916a8
    xp = 6
    coins = 4
    yoshi_cookie_item = items.HoneySyrup
    normal_item = items.HoneySyrup
    rare_item = items.HoneySyrup


class Frogog(Enemy):
    index = 49
    address = 0x390276
    hp = 80
    speed = 8
    attack = 15
    defense = 8
    magic_defense = 8
    fp = 100
    morph_chance = 3
    sound_on_hit = 16
    weaknesses = [5, 6]
    palette = 24
    flower_bonus_type = 3
    flower_bonus_chance = 6

    # Reward attributes
    reward_address = 0x391648
    xp = 3
    coins = 4
    yoshi_cookie_item = items.AbleJuice
    rare_item = items.Mushroom


class Clerk(Enemy):
    index = 50
    address = 0x3911d6
    boss = True
    hp = 500
    speed = 15
    attack = 160
    defense = 100
    magic_attack = 47
    magic_defense = 60
    fp = 100
    death_immune = True
    sound_on_hit = 48
    palette = 32
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x3918a0
    xp = 50
    coins = 20
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    anchor = True
    ratio_hp = 0.5556
    ratio_fp = 0.3333

    #shuffled overworld sprites
    overworld_sprite = 142
    overworld_npc = 19
    battle_sprite = 306
    battle_npc = 306
    other_npcs = [259]
    other_sprites = [259, 259]
    battle_sprite_is_wide = True
    battle_sprite_is_tall = True
    sprite_width = 60
    sprite_height = 58
    battle_push_sequence = 3
    battle_push_length = 32
    overworld_dont_reverse_northeast = True
    overworld_extra_sequence = 2
    shadow = MED_SHADOW
    overworld_solidity = [7, 7, 13]
    overworld_y_shift = 1
    statue_west_shift = 3
    opposite_statue_west_shift = 5


class Gunyolk(Enemy):
    index = 51
    address = 0x391216
    boss = True
    hp = 1500
    speed = 25
    attack = 200
    defense = 130
    magic_attack = 120
    magic_defense = 80
    fp = 100
    death_immune = True
    sound_on_hit = 96
    resistances = [6]
    weaknesses = [4, 5]
    palette = 32
    flower_bonus_type = 1
    flower_bonus_chance = 2
    sprite_width = 71
    sprite_height = 63

    # Reward attributes
    reward_address = 0x3918b8
    xp = 100
    coins = 10
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.6
    ratio_fp = 0.5
    ratio_attack = 1.0
    ratio_defense = 1.04
    ratio_magic_attack = 1.2632
    ratio_magic_defense = 0.9412
    ratio_speed = 0.7143

    #shuffled overworld sprites
    overworld_sprite = 330
    overworld_npc = 484
    battle_sprite = 307
    battle_npc = 307
    battle_sprite_is_wide = True
    battle_sprite_is_tall = True
    battle_sesw_only = True
    battle_push_sequence = 3
    overworld_push_sequence = 3
    battle_push_length = 52
    overworld_push_length = 30
    shadow = MED_SHADOW
    overworld_solidity = [7, 7, 12]
    overworld_y_shift = 1
    statue_west_shift = 2


class Boomer(Enemy):
    index = 52
    address = 0x3911b6
    boss = True
    hp = 2000
    speed = 18
    attack = 200
    defense = 140
    magic_attack = 35
    magic_defense = 26
    fp = 200
    death_immune = True
    sound_on_hit = 48
    status_immunities = [0, 1, 2, 3]
    palette = 24
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x3918dc
    xp = 55
    coins = 9
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 1.0
    ratio_fp = 1.0

    #shuffled overworld sprites
    overworld_sprite = 346
    overworld_npc = 159
    battle_sprite = 169
    battle_npc = 482
    statue_only = True
    battle_sprite_is_tall = True
    sprite_width = 52
    sprite_width = 49
    battle_sesw_only = True
    overworld_extra_sequence = 5
    overworld_push_sequence = 3
    overworld_push_length = 40
    overworld_is_skinny = True
    other_sprites = [346, 346]
    shadow = MED_SHADOW
    overworld_solidity = [3, 3, 7]
    overworld_y_shift = 1
    statue_east_shift = 2
    opposite_statue_west_shift = 2

    def get_patch(self):
        """Update battle events for switching between blue and red states for Boomer with shuffled stat changes.

        Returns:
            randomizer.logic.patch.Patch: Patch data

        """
        patch = super().get_patch()

        # TODO: Get addresses for linear mode.
        if self.world.open_mode:
            # Change to blue state.  Scale shuffled stats based on vanilla ratios.
            patch.add_data(0x353629, utils.ByteField(int(round(min(self.attack * 0.6, 255)))).as_bytes())
            patch.add_data(0x35362d, utils.ByteField(int(round(min(self.defense * 0.6429, 255)))).as_bytes())
            patch.add_data(0x353631, utils.ByteField(int(round(min(self.magic_attack * 2.8571, 255)))).as_bytes())
            patch.add_data(0x353635, utils.ByteField(int(round(min(self.magic_defense * 3.4615, 255)))).as_bytes())

            # Change back to red state (use starting stats).
            patch.add_data(0x3535e2, utils.ByteField(self.attack).as_bytes())
            patch.add_data(0x3535e6, utils.ByteField(self.defense).as_bytes())
            patch.add_data(0x3535ea, utils.ByteField(self.magic_attack).as_bytes())
            patch.add_data(0x3535ee, utils.ByteField(self.magic_defense).as_bytes())

        return patch


class Remocon(Enemy):
    index = 53
    address = 0x390476
    hp = 88
    speed = 5
    attack = 56
    defense = 52
    magic_attack = 25
    magic_defense = 10
    fp = 100
    morph_chance = 3
    sound_on_hit = 80
    resistances = [4, 5]
    weaknesses = [6]
    palette = 16
    flower_bonus_type = 5
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391708
    xp = 8
    coins = 7
    yoshi_cookie_item = items.PickMeUp
    normal_item = items.HoneySyrup


class Snapdragon(Enemy):
    index = 54
    address = 0x390316
    hp = 90
    speed = 4
    attack = 28
    defense = 25
    magic_attack = 31
    magic_defense = 25
    fp = 100
    morph_chance = 2
    sound_on_hit = 64
    weaknesses = [6]
    palette = 16
    flower_bonus_type = 3
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391684
    xp = 4
    coins = 3
    yoshi_cookie_item = items.SleepyBomb
    rare_item = items.Mushroom


class Stumpet(Enemy):
    index = 55
    address = 0x3907a6
    hp = 500
    speed = 1
    attack = 200
    defense = 120
    magic_attack = 6
    magic_defense = 60
    fp = 100
    morph_chance = 3
    sound_on_hit = 96
    resistances = [6]
    weaknesses = [4]
    status_immunities = [0, 1, 2, 3]
    palette = 32
    flower_bonus_type = 2
    flower_bonus_chance = 10

    # Reward attributes
    reward_address = 0x39183a
    xp = 70
    coins = 15
    yoshi_cookie_item = items.RoyalSyrup
    normal_item = items.FireBomb
    rare_item = items.FrightBomb


class Dodo(Enemy):
    index = 56
    address = 0x391116
    boss = True
    hp = 1000
    speed = 10
    attack = 140
    defense = 100
    magic_attack = 9
    magic_defense = 60
    fp = 100
    death_immune = True
    sound_on_hit = 16
    weaknesses = [6]
    status_immunities = [0, 1]
    palette = 24
    flower_bonus_type = 1
    flower_bonus_chance = 2
    hp_counter_ratios = [0.6]

    # Reward attributes
    reward_address = 0x391c12
    xp = 40
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.4167
    ratio_fp = 0.2857
    ratio_attack = 1.1667
    ratio_defense = 1.25
    ratio_magic_attack = 0.1125
    ratio_magic_defense = 1.0
    ratio_speed = 0.05
    ratio_evade = 0.0
    ratio_magic_evade = 1.0

    def get_patch(self):
        """For Dodo solo boss, also update the battle event trigger so he runs away from the solo fight at 60% of his
        shuffled HP, not always 600 HP like the vanilla game.

        Returns:
            randomizer.logic.patch.Patch: Patch data

        """
        patch = super().get_patch()

        # Open mode event address is the same as vanilla, but standard mode patch is in a different spot.
        if not self.world.open_mode:
            run_away = self.round_for_battle_script(self.hp * 0.6)
            patch.add_data(0x393818, utils.ByteField(run_away, num_bytes=2).as_bytes())

        return patch


class Jester(Enemy):
    index = 57
    address = 0x390486
    boss = True
    hp = 151
    speed = 20
    attack = 48
    defense = 35
    magic_attack = 22
    magic_defense = 35
    fp = 12
    magic_evade = 80
    morph_chance = 3
    sound_on_hit = 16
    weaknesses = [4]
    palette = 16
    flower_bonus_type = 1
    flower_bonus_chance = 3

    # Reward attributes
    reward_address = 0x39170e
    xp = 10
    coins = 10
    yoshi_cookie_item = items.HoneySyrup


class Artichoker(Enemy):
    index = 58
    address = 0x390416
    hp = 200
    speed = 7
    attack = 50
    defense = 54
    magic_attack = 27
    magic_defense = 24
    fp = 100
    magic_evade = 20
    morph_chance = 3
    sound_on_hit = 32
    sound_on_approach = 2
    resistances = [5]
    weaknesses = [6, 7]
    palette = 24
    flower_bonus_type = 2
    flower_bonus_chance = 4

    # Reward attributes
    reward_address = 0x3916e4
    xp = 12
    coins = 10
    yoshi_cookie_item = items.MidMushroom
    rare_item = items.FrightBomb


class Arachne(Enemy):
    index = 59
    address = 0x390326
    hp = 82
    speed = 14
    attack = 35
    defense = 35
    magic_attack = 6
    fp = 100
    morph_chance = 2
    sound_on_hit = 32
    weaknesses = [4]
    palette = 24
    flower_bonus_type = 2
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x39168a
    xp = 6
    coins = 6
    yoshi_cookie_item = items.Energizer
    normal_item = items.AbleJuice


class Carriboscis(Enemy):
    index = 60
    address = 0x390426
    hp = 90
    speed = 30
    attack = 55
    defense = 44
    magic_attack = 28
    magic_defense = 22
    fp = 100
    evade = 13
    morph_chance = 3
    sound_on_hit = 16
    weaknesses = [6, 7]
    palette = 24
    flower_bonus_type = 3
    flower_bonus_chance = 3

    # Reward attributes
    reward_address = 0x3916ea
    xp = 10
    coins = 4
    yoshi_cookie_item = items.HoneySyrup
    rare_item = items.AbleJuice


class Hippopo(Enemy):
    index = 61
    address = 0x390926
    hp = 400
    speed = 6
    attack = 150
    defense = 110
    magic_attack = 85
    magic_defense = 53
    fp = 100
    magic_evade = 15
    morph_chance = 1
    sound_on_hit = 96
    weaknesses = [5]
    status_immunities = [0, 1, 2, 3]
    palette = 32
    flower_bonus_type = 5
    flower_bonus_chance = 10
    one_per_battle = True

    # Reward attributes
    reward_address = 0x3918f4
    xp = 80
    coins = 50
    yoshi_cookie_item = items.Megalixir
    normal_item = items.RockCandy


class Mastadoom(Enemy):
    index = 62
    address = 0x390506
    hp = 180
    speed = 3
    attack = 90
    defense = 65
    magic_attack = 30
    magic_defense = 50
    fp = 100
    morph_chance = 1
    sound_on_hit = 96
    resistances = [5]
    weaknesses = [6]
    palette = 32
    flower_bonus_type = 3
    flower_bonus_chance = 10

    # Reward attributes
    reward_address = 0x391744
    xp = 20
    yoshi_cookie_item = items.Crystalline
    rare_item = items.MidMushroom


class Corkpedite(Enemy):
    index = 63
    address = 0x3907d6
    hp = 200
    speed = 5
    attack = 130
    defense = 110
    magic_attack = 80
    magic_defense = 20
    fp = 100
    morph_chance = 1
    sound_on_hit = 96
    resistances = [6]
    weaknesses = [4]
    status_immunities = [0, 1, 2, 3]
    palette = 32
    flower_bonus_type = 1
    flower_bonus_chance = 6

    # Reward attributes
    reward_address = 0x39184c
    xp = 50
    coins = 10
    yoshi_cookie_item = items.Crystalline
    rare_item = items.FrightBomb


class Terracotta(Enemy):
    index = 64
    address = 0x3907f6
    hp = 180
    speed = 23
    attack = 120
    defense = 85
    magic_attack = 36
    magic_defense = 35
    fp = 100
    morph_chance = 3
    resistances = [6]
    palette = 16
    flower_bonus_type = 4
    flower_bonus_chance = 3

    # Reward attributes
    reward_address = 0x391858
    xp = 25
    yoshi_cookie_item = items.MidMushroom
    rare_item = items.Mushroom


class Spikester(Enemy):
    index = 65
    address = 0x390406
    hp = 50
    speed = 19
    attack = 48
    defense = 60
    magic_attack = 12
    magic_defense = 4
    fp = 100
    morph_chance = 2
    sound_on_approach = 1
    resistances = [7]
    weaknesses = [4]
    palette = 8
    flower_bonus_type = 4
    flower_bonus_chance = 5

    # Reward attributes
    reward_address = 0x3916de
    xp = 6
    coins = 2
    yoshi_cookie_item = items.Bracer


class Malakoopa(Enemy):
    index = 66
    address = 0x390806
    hp = 95
    speed = 35
    attack = 130
    defense = 120
    magic_attack = 47
    magic_defense = 98
    fp = 100
    evade = 20
    morph_chance = 3
    sound_on_hit = 80
    sound_on_approach = 1
    weaknesses = [5]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 3
    flying = True

    # Reward attributes
    reward_address = 0x39185e
    xp = 23
    coins = 3
    yoshi_cookie_item = items.MapleSyrup
    rare_item = items.HoneySyrup


class Pounder(Enemy):
    index = 67
    address = 0x390876
    boss = True
    hp = 180
    speed = 25
    attack = 130
    defense = 70
    magic_attack = 45
    magic_defense = 60
    fp = 100
    morph_chance = 3
    sound_on_hit = 80
    weaknesses = [5]
    palette = 8
    flower_bonus_type = 2
    flower_bonus_chance = 4

    # Reward attributes
    reward_address = 0x39188e
    xp = 24
    coins = 2
    yoshi_cookie_item = items.Energizer

    # Boss shuffle attributes.
    ratio_hp = 0.1343
    ratio_fp = 0.25
    ratio_attack = 1.0
    ratio_defense = 0.6364
    ratio_magic_attack = 0.75
    ratio_magic_defense = 0.8571
    ratio_speed = 1.0
    ratio_evade = 0.0
    ratio_magic_evade = 0.0


class Poundette(Enemy):
    index = 68
    address = 0x390886
    boss = True
    hp = 150
    speed = 30
    attack = 140
    defense = 60
    magic_attack = 66
    magic_defense = 45
    fp = 100
    morph_chance = 3
    sound_on_hit = 80
    weaknesses = [5]
    palette = 8
    flower_bonus_type = 4
    flower_bonus_chance = 5

    # Reward attributes
    reward_address = 0x391894
    xp = 28
    coins = 3
    yoshi_cookie_item = items.Energizer

    # Boss shuffle attributes.
    ratio_hp = 0.0938
    ratio_fp = 0.2
    ratio_attack = 0.7368
    ratio_defense = 0.5
    ratio_magic_attack = 1.1579
    ratio_magic_defense = 0.5625
    ratio_speed = 0.8571
    ratio_evade = 0.0
    ratio_magic_evade = 0.0


class Sackit(Enemy):
    index = 69
    address = 0x3904e6
    hp = 152
    speed = 26
    attack = 70
    defense = 53
    magic_attack = 13
    magic_defense = 20
    fp = 100
    evade = 20
    morph_chance = 3
    palette = 8
    flower_bonus_type = 4
    flower_bonus_chance = 3

    # Reward attributes
    reward_address = 0x391738
    xp = 20
    coins = 30
    yoshi_cookie_item = items.MaxMushroom
    normal_item = items.RoyalSyrup
    rare_item = items.MaxMushroom


class GuGoomba(Enemy):
    index = 70
    address = 0x390816
    hp = 132
    speed = 14
    attack = 115
    defense = 66
    magic_attack = 13
    magic_defense = 66
    fp = 100
    magic_evade = 50
    morph_chance = 3
    sound_on_approach = 2
    palette = 8
    flower_bonus_type = 3
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391864
    xp = 15
    coins = 1
    yoshi_cookie_item = items.FroggieDrink
    rare_item = items.MaxMushroom


class Chewy(Enemy):
    index = 71
    address = 0x390686
    hp = 90
    speed = 6
    attack = 110
    defense = 82
    magic_attack = 70
    magic_defense = 52
    fp = 100
    magic_evade = 50
    morph_chance = 3
    sound_on_hit = 16
    sound_on_approach = 2
    resistances = [7]
    status_immunities = [0, 1, 2, 3]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 5

    # Reward attributes
    reward_address = 0x3917ce
    xp = 14
    yoshi_cookie_item = items.BadMushroom
    normal_item = items.SleepyBomb


class Fireball(Enemy):
    index = 72
    address = 0x3904b6
    hp = 10
    speed = 42
    attack = 55
    defense = 16
    magic_attack = 30
    magic_defense = 16
    fp = 100
    evade = 50
    magic_evade = 30
    morph_chance = 1
    sound_on_approach = 2
    resistances = [6]
    weaknesses = [4, 7]
    palette = 8
    flower_bonus_type = 5
    flower_bonus_chance = 5

    # Reward attributes
    reward_address = 0x391720
    xp = 8
    yoshi_cookie_item = items.FireBomb
    normal_item = items.PickMeUp


class MrKipper(Enemy):
    index = 73
    address = 0x390546
    hp = 133
    speed = 23
    attack = 75
    defense = 45
    magic_attack = 14
    magic_defense = 10
    fp = 100
    evade = 13
    morph_chance = 3
    sound_on_hit = 80
    sound_on_approach = 1
    weaknesses = [5, 6]
    palette = 8
    flower_bonus_type = 2
    flower_bonus_chance = 5
    flying = True
    high_flying = True

    # Reward attributes
    reward_address = 0x39175c
    xp = 8
    coins = 2
    yoshi_cookie_item = items.Mushroom
    normal_item = items.AbleJuice


class FactoryChief(Enemy):
    index = 74
    address = 0x391206
    boss = True
    hp = 1000
    speed = 45
    attack = 200
    defense = 120
    magic_attack = 70
    magic_defense = 90
    fp = 100
    death_immune = True
    sound_on_hit = 16
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x3918b2
    xp = 80
    coins = 90
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.4
    ratio_fp = 0.5
    ratio_attack = 1.0
    ratio_defense = 0.96
    ratio_magic_attack = 0.7368
    ratio_magic_defense = 1.0588
    ratio_speed = 1.2857


class BandanaBlue(Enemy):
    index = 75
    address = 0x390586
    boss = True
    hp = 150
    speed = 30
    attack = 80
    defense = 60
    magic_attack = 20
    magic_defense = 30
    fp = 100
    morph_chance = 3
    sound_on_hit = 16
    weaknesses = [5, 6]
    palette = 8
    flower_bonus_type = 5
    flower_bonus_chance = 5

    # Reward attributes
    reward_address = 0x391774
    xp = 20
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.1829
    ratio_fp = 1.0
    ratio_attack = 0.9412
    ratio_defense = 0.75
    ratio_magic_attack = 0.8
    ratio_magic_defense = 0.5
    ratio_speed = 2.3077


class Manager(Enemy):
    index = 76
    address = 0x3911e6
    boss = True
    hp = 800
    speed = 25
    attack = 170
    defense = 110
    magic_attack = 60
    magic_defense = 70
    fp = 100
    death_immune = True
    sound_on_hit = 48
    palette = 32
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x3918a6
    xp = 60
    coins = 40
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    anchor = True
    ratio_hp = 0.597
    ratio_fp = 0.25
    ratio_attack = 1.3077
    ratio_defense = 1.0
    ratio_magic_attack = 1.0
    ratio_magic_defense = 1.0
    ratio_speed = 1.0

    #shuffled overworld sprites
    overworld_sprite = 167
    overworld_npc = 492
    battle_sprite = 332
    other_npcs = [323]
    other_sprites = [323, 323, 323]
    battle_sprite_is_wide = True
    battle_sprite_is_tall = True
    sprite_width = 60
    sprite_height = 58
    battle_push_sequence = 3
    battle_push_length = 32
    overworld_dont_reverse_northeast = True
    overworld_extra_sequence = 2
    shadow = MED_SHADOW
    overworld_solidity = [9, 9, 15]
    overworld_y_shift = 1
    statue_west_shift = 3
    opposite_statue_west_shift = 5


class Bluebird(Enemy):
    index = 77
    address = 0x3906e6
    hp = 200
    speed = 29
    attack = 95
    defense = 50
    magic_attack = 80
    magic_defense = 94
    fp = 100
    evade = 8
    morph_chance = 3
    sound_on_hit = 16
    sound_on_approach = 2
    resistances = [4]
    weaknesses = [6]
    status_immunities = [1]
    palette = 8
    flower_bonus_type = 2
    flower_bonus_chance = 2
    flying = True

    # Reward attributes
    reward_address = 0x3917f2
    xp = 14
    coins = 6
    yoshi_cookie_item = items.Bracer
    normal_item = items.Bracer


class AlleyRat(Enemy):
    index = 79
    address = 0x3905a6
    hp = 105
    speed = 21
    attack = 70
    defense = 55
    magic_attack = 13
    magic_defense = 12
    fp = 100
    evade = 15
    morph_chance = 3
    palette = 8
    flower_bonus_type = 4
    flower_bonus_chance = 3

    # Reward attributes
    reward_address = 0x391780
    xp = 9
    coins = 3
    yoshi_cookie_item = items.AbleJuice
    rare_item = items.Mushroom


class Chow(Enemy):
    index = 80
    address = 0x390606
    hp = 80
    speed = 27
    attack = 82
    defense = 77
    magic_attack = 8
    magic_defense = 28
    fp = 100
    morph_chance = 3
    status_immunities = [1, 3]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 5

    # Reward attributes
    reward_address = 0x3917aa
    xp = 15
    coins = 3
    yoshi_cookie_item = items.FrightBomb


class Magmus(Enemy):
    index = 81
    address = 0x390766
    hp = 50
    speed = 6
    attack = 110
    defense = 140
    magic_attack = 3
    magic_defense = 25
    fp = 100
    magic_evade = 10
    morph_chance = 3
    sound_on_hit = 80
    resistances = [6, 7]
    weaknesses = [4]
    status_immunities = [0, 1, 2, 3]
    palette = 8
    flower_bonus_type = 5
    flower_bonus_chance = 10

    # Reward attributes
    reward_address = 0x391822
    xp = 18
    coins = 3
    yoshi_cookie_item = items.Bracer
    rare_item = items.Bracer


class LilBoo(Enemy):
    index = 82
    address = 0x3908e6
    hp = 66
    speed = 27
    attack = 120
    defense = 20
    magic_attack = 74
    magic_defense = 120
    fp = 100
    evade = 50
    magic_evade = 20
    morph_chance = 3
    resistances = [7]
    palette = 8
    flower_bonus_type = 2
    flower_bonus_chance = 5

    # Reward attributes
    reward_address = 0x3918d6
    xp = 28
    yoshi_cookie_item = items.FreshenUp


class Vomer(Enemy):
    index = 83
    address = 0x390796
    boss = True
    speed = 10
    attack = 110
    magic_attack = 9
    fp = 100
    magic_evade = 5
    morph_chance = 3
    sound_on_hit = 144
    sound_on_approach = 6
    status_immunities = [0, 1, 2, 3]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391834
    xp = 19
    yoshi_cookie_item = items.PureWater
    rare_item = items.PureWater


class GlumReaper(Enemy):
    index = 84
    address = 0x3908d6
    hp = 180
    speed = 35
    attack = 120
    defense = 55
    magic_attack = 60
    magic_defense = 80
    fp = 100
    evade = 20
    magic_evade = 10
    morph_chance = 3
    sound_on_hit = 16
    resistances = [7]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 5

    # Reward attributes
    reward_address = 0x3918d0
    xp = 35
    coins = 3
    yoshi_cookie_item = items.PureWater
    normal_item = items.PureWater


class Pyrosphere(Enemy):
    index = 85
    address = 0x390786
    hp = 167
    speed = 24
    attack = 105
    defense = 66
    magic_attack = 100
    magic_defense = 48
    fp = 100
    evade = 7
    morph_chance = 1
    sound_on_approach = 2
    resistances = [6]
    weaknesses = [4]
    status_immunities = [2]
    palette = 8
    flower_bonus_type = 4
    flower_bonus_chance = 4

    # Reward attributes
    reward_address = 0x39182e
    xp = 17
    coins = 2
    yoshi_cookie_item = items.FireBomb


class ChompChomp(Enemy):
    index = 86
    address = 0x390666
    hp = 150
    speed = 10
    attack = 100
    defense = 92
    magic_attack = 14
    magic_defense = 30
    fp = 100
    morph_chance = 3
    sound_on_hit = 32
    weaknesses = [5]
    palette = 16
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x3917c2
    xp = 12
    coins = 5
    yoshi_cookie_item = items.Mushroom
    normal_item = items.Crystalline


class Hidon(Enemy):
    index = 87
    address = 0x390946
    boss = True
    hp = 600
    speed = 1
    attack = 110
    defense = 90
    magic_attack = 60
    magic_defense = 30
    fp = 100
    death_immune = True
    sound_on_hit = 32
    resistances = [4, 5, 6]
    weaknesses = [7]
    status_immunities = [0, 1, 2, 3]
    palette = 16
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391900
    xp = 50
    coins = 100
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 1.0
    ratio_fp = 1.0
    other_sprites = [349, 349, 349, 349]

    #shuffled overworld sprites
    overworld_sprite = 195
    overworld_npc = 199
    battle_sprite = 343
    battle_npc = 343
    overworld_sequence = 4
    statue_only = True
    sprite_width = 37
    sprite_height = 40
    overworld_freeze = True
    battle_sesw_only = True
    battle_push_sequence = 3
    battle_push_length = 44
    overworld_is_empty = True
    shadow = SMALL_SHADOW
    overworld_solidity = [1, 1, 1]
    overworld_y_shift = 0


class SlingShy(Enemy):
    index = 88
    address = 0x390716
    hp = 120
    speed = 16
    attack = 108
    defense = 80
    magic_attack = 42
    magic_defense = 21
    fp = 100
    morph_chance = 3
    palette = 8
    flower_bonus_type = 5
    flower_bonus_chance = 3

    # Reward attributes
    reward_address = 0x391804
    xp = 3
    coins = 20
    yoshi_cookie_item = items.MapleSyrup
    rare_item = items.HoneySyrup


class Robomb(Enemy):
    index = 89
    address = 0x390446
    hp = 42
    speed = 2
    attack = 54
    defense = 63
    magic_attack = 1
    magic_defense = 20
    fp = 100
    morph_chance = 3
    sound_on_hit = 80
    weaknesses = [6, 7]
    palette = 8
    flower_bonus_type = 2
    flower_bonus_chance = 5

    # Reward attributes
    reward_address = 0x3916f6
    xp = 6
    coins = 1
    yoshi_cookie_item = items.PickMeUp
    normal_item = items.PickMeUp


class ShyGuy(Enemy):
    index = 90
    address = 0x3902f6
    hp = 78
    speed = 14
    attack = 29
    defense = 30
    magic_attack = 20
    magic_defense = 6
    fp = 100
    evade = 10
    morph_chance = 3
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391678
    xp = 2
    coins = 1
    yoshi_cookie_item = items.HoneySyrup


class Ninja(Enemy):
    index = 91
    address = 0x3908a6
    boss = True
    hp = 235
    speed = 28
    attack = 130
    defense = 76
    magic_attack = 51
    magic_defense = 67
    fp = 100
    evade = 30
    morph_chance = 1
    sound_on_hit = 16
    resistances = [4, 5, 6]
    status_immunities = [0, 1, 2, 3]
    palette = 8
    flower_bonus_type = 5
    flower_bonus_chance = 7

    # Reward attributes
    reward_address = 0x3918be
    xp = 32
    coins = 6
    yoshi_cookie_item = items.PowerBlast
    normal_item = items.MapleSyrup


class Stinger(Enemy):
    index = 92
    address = 0x3905f6
    hp = 65
    speed = 33
    attack = 78
    defense = 80
    magic_attack = 23
    magic_defense = 10
    fp = 100
    evade = 25
    morph_chance = 3
    sound_on_hit = 16
    sound_on_approach = 1
    palette = 8
    flower_bonus_type = 4
    flower_bonus_chance = 4
    flying = True

    # Reward attributes
    reward_address = 0x3917a4
    xp = 13
    coins = 1
    yoshi_cookie_item = items.AbleJuice
    rare_item = items.AbleJuice


class Goombette(Enemy):
    index = 93
    address = 0x390976
    boss = True
    hp = 100
    speed = 16
    attack = 90
    defense = 80
    magic_attack = 30
    magic_defense = 30
    fp = 100
    evade = 20
    sound_on_approach = 2
    weaknesses = [6]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391912
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.1667
    ratio_fp = 1.0
    ratio_attack = 0.8182
    ratio_defense = 0.8889
    ratio_magic_attack = 0.5
    ratio_magic_defense = 1.0
    ratio_speed = 16.0
    ratio_evade = 1.0
    ratio_magic_evade = 0.0


class Geckit(Enemy):
    index = 94
    address = 0x390696
    hp = 100
    speed = 25
    attack = 84
    defense = 63
    magic_attack = 20
    magic_defense = 8
    fp = 100
    evade = 14
    morph_chance = 3
    sound_on_hit = 128
    resistances = [6]
    weaknesses = [4]
    palette = 8
    flower_bonus_type = 4
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x3917d4
    xp = 18
    yoshi_cookie_item = items.Energizer
    rare_item = items.AbleJuice


class Jabit(Enemy):
    index = 95
    address = 0x390896
    hp = 150
    speed = 13
    attack = 120
    defense = 95
    magic_attack = 27
    magic_defense = 34
    fp = 100
    morph_chance = 3
    weaknesses = [5]
    palette = 8
    flower_bonus_type = 2
    flower_bonus_chance = 1

    # Reward attributes
    reward_address = 0x39189a
    xp = 18
    yoshi_cookie_item = items.Bracer
    normal_item = items.PickMeUp


class Starcruster(Enemy):
    index = 96
    address = 0x390846
    hp = 72
    speed = 11
    attack = 135
    defense = 145
    magic_attack = 16
    magic_defense = 53
    fp = 100
    magic_evade = 10
    morph_chance = 1
    sound_on_hit = 32
    resistances = [7]
    weaknesses = [4]
    palette = 24
    flower_bonus_type = 1
    flower_bonus_chance = 3

    # Reward attributes
    reward_address = 0x39187c
    xp = 36
    coins = 30
    yoshi_cookie_item = items.Crystalline
    normal_item = items.Crystalline


class Merlin(Enemy):
    index = 97
    address = 0x3908f6
    boss = True
    hp = 169
    speed = 20
    attack = 124
    defense = 63
    magic_attack = 90
    magic_defense = 130
    fp = 100
    morph_chance = 3
    sound_on_hit = 16
    palette = 16
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x3918e2
    xp = 50
    coins = 20
    yoshi_cookie_item = items.Mushroom


class Muckle(Enemy):
    index = 98
    address = 0x390746
    boss = True
    hp = 320
    speed = 2
    attack = 90
    defense = 44
    magic_attack = 90
    magic_defense = 44
    fp = 100
    evade = 1
    morph_chance = 1
    sound_on_hit = 64
    resistances = [4]
    weaknesses = [6]
    status_immunities = [0, 1, 2, 3]
    palette = 16
    flower_bonus_type = 3
    flower_bonus_chance = 6

    # Reward attributes
    reward_address = 0x391816
    xp = 6
    coins = 3
    yoshi_cookie_item = items.IceBomb
    normal_item = items.IceBomb


class Forkies(Enemy):
    index = 99
    address = 0x390856
    hp = 350
    speed = 200
    attack = 170
    defense = 120
    magic_attack = 45
    magic_defense = 128
    fp = 100
    morph_chance = 3
    sound_on_hit = 32
    palette = 16
    flower_bonus_type = 3
    flower_bonus_chance = 5

    # Reward attributes
    reward_address = 0x391882
    xp = 32
    coins = 7
    yoshi_cookie_item = items.RoyalSyrup
    rare_item = items.SleepyBomb


class Gorgon(Enemy):
    index = 100
    address = 0x3905d6
    hp = 140
    speed = 16
    attack = 86
    defense = 73
    magic_attack = 24
    magic_defense = 52
    fp = 100
    evade = 11
    morph_chance = 3
    sound_on_hit = 96
    sound_on_approach = 1
    weaknesses = [5]
    palette = 16
    flower_bonus_type = 3
    flower_bonus_chance = 5

    # Reward attributes
    reward_address = 0x391792
    xp = 20
    yoshi_cookie_item = items.MapleSyrup
    rare_item = items.MidMushroom


class BigBertha(Enemy):
    index = 101
    address = 0x390826
    hp = 350
    speed = 1
    attack = 170
    defense = 130
    fp = 100
    morph_chance = 3
    weaknesses = [5]
    palette = 24
    flower_bonus_type = 2
    flower_bonus_chance = 5

    # Reward attributes
    reward_address = 0x39186a
    xp = 35
    coins = 7
    yoshi_cookie_item = items.PickMeUp


class ChainedKong(Enemy):
    index = 102
    address = 0x3907b6
    hp = 355
    speed = 17
    attack = 150
    defense = 80
    magic_attack = 22
    magic_defense = 50
    fp = 100
    evade = 10
    morph_chance = 3
    sound_on_hit = 96
    sound_on_approach = 4
    resistances = [6]
    weaknesses = [4]
    palette = 24
    flower_bonus_type = 3
    flower_bonus_chance = 3

    # Reward attributes
    reward_address = 0x391840
    xp = 35
    coins = 8
    yoshi_cookie_item = items.PickMeUp
    rare_item = items.MaxMushroom


class Fautso(Enemy):
    index = 103
    address = 0x390986
    boss = True
    hp = 420
    speed = 14
    attack = 130
    defense = 100
    magic_attack = 60
    magic_defense = 60
    fp = 100
    evade = 10
    sound_on_hit = 96
    resistances = [5, 6]
    weaknesses = [4, 7]
    status_immunities = [0, 2, 3]
    palette = 32
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391918
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.4667
    ratio_fp = 1.0
    ratio_attack = 0.7222
    ratio_defense = 0.9091
    ratio_magic_attack = 0.75
    ratio_magic_defense = 1.5
    ratio_speed = 14.0
    ratio_evade = 1.0
    ratio_magic_evade = 0.0


class Strawhead(Enemy):
    index = 104
    address = 0x3905e6
    hp = 131
    speed = 9
    attack = 80
    defense = 63
    magic_attack = 18
    magic_defense = 12
    fp = 100
    morph_chance = 3
    sound_on_hit = 16
    weaknesses = [5]
    palette = 16
    flower_bonus_type = 1
    flower_bonus_chance = 3

    # Reward attributes
    reward_address = 0x391798
    xp = 17
    coins = 12
    yoshi_cookie_item = items.PureWater
    normal_item = items.PureWater
    rare_item = items.PureWater


class Juju(Enemy):
    index = 105
    address = 0x3909c6
    hp = 10
    fp = 100
    morph_chance = 3
    sound_on_hit = 32
    palette = 24
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391930
    yoshi_cookie_item = items.Mushroom


class ArmoredAnt(Enemy):
    index = 106
    address = 0x3907c6
    hp = 230
    speed = 12
    attack = 130
    defense = 120
    magic_attack = 24
    magic_defense = 80
    fp = 100
    morph_chance = 1
    sound_on_hit = 48
    resistances = [6]
    weaknesses = [4]
    palette = 16
    flower_bonus_type = 2
    flower_bonus_chance = 5

    # Reward attributes
    reward_address = 0x391846
    xp = 30
    coins = 5
    yoshi_cookie_item = items.PowerBlast
    normal_item = items.PowerBlast


class Orbison(Enemy):
    index = 107
    address = 0x390756
    hp = 30
    speed = 25
    attack = 113
    defense = 140
    magic_attack = 63
    magic_defense = 65
    fp = 100
    morph_chance = 3
    sound_on_hit = 80
    resistances = [4, 5, 6]
    weaknesses = [7]
    palette = 16
    flower_bonus_type = 2
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x39181c
    xp = 18
    yoshi_cookie_item = items.RoyalSyrup
    normal_item = items.PureWater


class TuboTroopa(Enemy):
    index = 108
    address = 0x390836
    hp = 500
    speed = 5
    attack = 200
    defense = 80
    magic_attack = 7
    magic_defense = 34
    fp = 100
    evade = 1
    morph_chance = 3
    sound_on_hit = 96
    weaknesses = [5]
    palette = 16
    flower_bonus_type = 5
    flower_bonus_chance = 6
    flying = True

    # Reward attributes
    reward_address = 0x391870
    xp = 40
    coins = 11
    yoshi_cookie_item = items.Elixir
    normal_item = items.RockCandy


class Doppel(Enemy):
    index = 109
    address = 0x390916
    hp = 333
    speed = 40
    attack = 140
    defense = 60
    magic_attack = 44
    magic_defense = 50
    fp = 100
    evade = 19
    morph_chance = 3
    sound_on_hit = 96
    resistances = [7]
    palette = 16
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x3918ee
    xp = 40
    coins = 12
    yoshi_cookie_item = items.PickMeUp
    rare_item = items.PureWater


class Pulsar(Enemy):
    index = 110
    address = 0x390516
    hp = 69
    speed = 8
    attack = 75
    defense = 90
    magic_attack = 33
    magic_defense = 35
    fp = 100
    evade = 10
    morph_chance = 3
    sound_on_hit = 32
    sound_on_approach = 5
    resistances = [7]
    weaknesses = [6]
    palette = 16
    flower_bonus_type = 5
    flower_bonus_chance = 9

    # Reward attributes
    reward_address = 0x39174a
    xp = 15
    coins = 12
    yoshi_cookie_item = items.PickMeUp
    rare_item = items.PickMeUp


class Octovader(Enemy):
    index = 112
    address = 0x390636
    hp = 250
    speed = 5
    attack = 90
    defense = 50
    magic_attack = 63
    magic_defense = 50
    fp = 100
    evade = 9
    magic_evade = 8
    morph_chance = 3
    sound_on_hit = 112
    resistances = [5]
    weaknesses = [6]
    palette = 24
    flower_bonus_type = 3
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x3917bc
    xp = 30
    coins = 8
    yoshi_cookie_item = items.FroggieDrink
    normal_item = items.PowerBlast


class Ribbite(Enemy):
    index = 113
    address = 0x3906a6
    hp = 250
    speed = 15
    attack = 115
    defense = 20
    magic_attack = 31
    magic_defense = 29
    fp = 100
    morph_chance = 3
    resistances = [6]
    weaknesses = [4]
    status_immunities = [2]
    palette = 24
    flower_bonus_type = 3
    flower_bonus_chance = 4

    # Reward attributes
    reward_address = 0x3917da
    xp = 22
    coins = 8
    yoshi_cookie_item = items.Elixir
    normal_item = items.Elixir


class Director(Enemy):
    index = 114
    address = 0x3911f6
    boss = True
    hp = 1000
    speed = 35
    attack = 190
    defense = 120
    magic_attack = 57
    magic_defense = 80
    fp = 100
    death_immune = True
    sound_on_hit = 48
    palette = 32
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x3918ac
    xp = 70
    coins = 80
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    anchor = True
    ratio_hp = 0.625
    ratio_fp = 0.2

    #shuffled overworld sprites
    overworld_sprite = 168
    overworld_npc = 497
    battle_sprite = 370
    battle_npc = 370
    other_npcs = [324]
    other_sprites = [324, 324, 324, 324]
    battle_sprite_is_wide = True
    battle_sprite_is_tall = True
    sprite_width = 60
    sprite_height = 58
    battle_push_sequence = 3
    battle_push_length = 32
    overworld_dont_reverse_northeast = True
    overworld_extra_sequence = 2
    shadow = MED_SHADOW
    overworld_solidity = [9, 9, 15]
    overworld_y_shift = 1
    statue_west_shift = 3
    opposite_statue_west_shift = 5



class Puppox(Enemy):
    index = 117
    address = 0x390906
    hp = 300
    speed = 9
    attack = 145
    defense = 110
    magic_attack = 20
    magic_defense = 32
    fp = 100
    morph_chance = 1
    sound_on_hit = 80
    resistances = [5]
    weaknesses = [6]
    palette = 16
    flower_bonus_type = 2
    flower_bonus_chance = 1

    # Reward attributes
    reward_address = 0x3918e8
    xp = 30
    coins = 10
    yoshi_cookie_item = items.RockCandy
    rare_item = items.FreshenUp


class FinkFlower(Enemy):
    index = 118
    address = 0x390616
    hp = 200
    speed = 4
    attack = 95
    defense = 32
    magic_attack = 63
    magic_defense = 90
    fp = 100
    magic_evade = 12
    morph_chance = 3
    sound_on_hit = 64
    weaknesses = [6]
    status_immunities = [0, 1, 2, 3]
    palette = 16
    flower_bonus_type = 3
    flower_bonus_chance = 3

    # Reward attributes
    reward_address = 0x3917b0
    xp = 20
    coins = 2
    yoshi_cookie_item = items.MaxMushroom
    rare_item = items.MidMushroom


class Lumbler(Enemy):
    index = 119
    address = 0x390a06
    boss = True
    hp = 10
    fp = 100
    morph_chance = 3
    sound_on_hit = 96
    palette = 32
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391948
    yoshi_cookie_item = items.Mushroom


class Springer(Enemy):
    index = 120
    address = 0x3908b6
    hp = 122
    speed = 16
    attack = 155
    defense = 110
    magic_attack = 100
    magic_defense = 79
    fp = 100
    evade = 30
    morph_chance = 3
    sound_on_hit = 80
    palette = 8
    flower_bonus_type = 4
    flower_bonus_chance = 4

    # Reward attributes
    reward_address = 0x3918c4
    xp = 29
    coins = 2
    yoshi_cookie_item = items.Elixir
    rare_item = items.Energizer


class Harlequin(Enemy):
    index = 121
    address = 0x390a16
    hp = 10
    fp = 100
    morph_chance = 3
    sound_on_hit = 16
    palette = 16
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x39194e
    yoshi_cookie_item = items.Mushroom


class Kriffid(Enemy):
    index = 122
    address = 0x3906b6
    hp = 320
    speed = 8
    attack = 95
    defense = 100
    magic_attack = 50
    magic_defense = 40
    fp = 100
    morph_chance = 1
    sound_on_hit = 32
    sound_on_approach = 2
    resistances = [6]
    weaknesses = [4]
    status_immunities = [2]
    palette = 24
    flower_bonus_type = 2
    flower_bonus_chance = 5

    # Reward attributes
    reward_address = 0x3917e0
    xp = 35
    coins = 6
    yoshi_cookie_item = items.Crystalline
    normal_item = items.BadMushroom


class Spinthra(Enemy):
    index = 123
    address = 0x3906c6
    hp = 230
    speed = 19
    attack = 110
    defense = 70
    magic_attack = 4
    magic_defense = 32
    fp = 100
    morph_chance = 1
    sound_on_hit = 32
    weaknesses = [4]
    status_immunities = [2]
    palette = 24
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x3917e6
    xp = 30
    coins = 4
    yoshi_cookie_item = items.PowerBlast
    rare_item = items.Bracer


class Radish(Enemy):
    index = 124
    address = 0x390a26
    hp = 10
    fp = 100
    morph_chance = 3
    sound_on_hit = 16
    palette = 24
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391954
    yoshi_cookie_item = items.Mushroom


class Crippo(Enemy):
    index = 125
    address = 0x390a36
    hp = 10
    fp = 100
    morph_chance = 3
    sound_on_hit = 96
    palette = 32
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x39195a
    yoshi_cookie_item = items.Mushroom


class MastaBlasta(Enemy):
    index = 126
    address = 0x390a46
    hp = 10
    fp = 100
    morph_chance = 3
    sound_on_hit = 96
    palette = 32
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391960
    yoshi_cookie_item = items.Mushroom


class Piledriver(Enemy):
    index = 127
    address = 0x390a56
    hp = 10
    fp = 100
    morph_chance = 3
    sound_on_hit = 96
    palette = 32
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391966
    yoshi_cookie_item = items.Mushroom


class Apprentice(Enemy):
    index = 128
    address = 0x3904c6
    boss = True
    hp = 120
    speed = 20
    attack = 50
    defense = 50
    magic_attack = 20
    magic_defense = 20
    fp = 32
    sound_on_hit = 128
    weaknesses = [4]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391726
    xp = 1
    coins = 4
    yoshi_cookie_item = items.SleepyBomb
    normal_item = items.MidMushroom


class BoxBoy(Enemy):
    index = 134
    address = 0x390956
    boss = True
    hp = 900
    speed = 1
    attack = 180
    defense = 110
    magic_attack = 80
    magic_defense = 40
    fp = 100
    death_immune = True
    sound_on_hit = 32
    resistances = [4, 5, 6]
    weaknesses = [7]
    status_immunities = [0, 1, 2, 3]
    palette = 16
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391906
    xp = 100
    coins = 150
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 1.0
    ratio_fp = 1.0

    #shuffled overworld sprites
    overworld_sprite = 195
    overworld_npc = 199
    battle_sprite = 390
    battle_npc = 390
    overworld_sequence = 4
    statue_only = True
    sprite_width = 37
    sprite_height = 40
    overworld_freeze = True
    battle_sesw_only = True
    battle_push_sequence = 3
    battle_push_length = 90
    overworld_is_empty = True
    shadow = SMALL_SHADOW
    overworld_solidity = [1, 1, 1]
    overworld_y_shift = 0


class Shelly(Enemy):
    index = 135
    address = 0x390e06
    boss = True
    hp = 10
    defense = 80
    fp = 100
    death_immune = True
    status_immunities = [0, 1, 2, 3]
    palette = 24
    flower_bonus_type = 1
    flower_bonus_chance = 2
    hp_counter_ratios = [0.8, 0.6, 0.4, 0.2]

    # Reward attributes
    reward_address = 0x39198a
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.0129
    ratio_fp = 0.0
    ratio_attack = 0.0
    ratio_defense = 0.6154
    ratio_magic_attack = 0.0
    ratio_magic_defense = 0.0
    ratio_speed = 0.0
    ratio_evade = 0.0
    ratio_magic_evade = 0.0

class Superspike(Enemy):
    index = 136
    address = 0x390ab6
    boss = True
    hp = 10
    fp = 100
    morph_chance = 3
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391990
    yoshi_cookie_item = items.Mushroom


class DodoSolo(Enemy):
    index = 137
    address = 0x391126
    boss = True
    hp = 800
    speed = 10
    attack = 140
    defense = 100
    magic_attack = 9
    magic_defense = 60
    fp = 100
    death_immune = True
    sound_on_hit = 16
    weaknesses = [6]
    status_immunities = [0, 1]
    palette = 24
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391c18
    xp = 70
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 1.0
    ratio_fp = 1.0

    #shuffled overworld sprites
    overworld_sprite = 131
    overworld_npc = 131
    overworld_sequence = 2
    battle_sprite = 312
    battle_npc = 21
    statue_only = True
    sprite_height = 56
    sprite_width = 46
    overworld_freeze = True
    battle_sesw_only = True
    battle_push_sequence = 3
    battle_push_length = 16
    overworld_is_empty = True
    shadow = SMALL_SHADOW
    overworld_solidity = [2, 2, 5]
    battle_solidity = [9, 9, 14]
    overworld_y_shift = 0
    battle_y_shift = 0
    statue_south_shift = 3


class Oerlikon(Enemy):
    index = 138
    address = 0x390776
    hp = 85
    speed = 20
    attack = 120
    defense = 125
    magic_attack = 17
    magic_defense = 50
    fp = 100
    morph_chance = 3
    sound_on_approach = 1
    resistances = [6, 7]
    weaknesses = [4]
    status_immunities = [0, 1, 2, 3]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 5

    # Reward attributes
    reward_address = 0x391828
    xp = 22
    yoshi_cookie_item = items.Energizer
    rare_item = items.Energizer


class Chester(Enemy):
    index = 139
    address = 0x390966
    boss = True
    hp = 1200
    speed = 1
    attack = 220
    defense = 120
    magic_attack = 120
    magic_defense = 80
    fp = 100
    death_immune = True
    sound_on_hit = 32
    resistances = [4, 5, 6]
    weaknesses = [7]
    status_immunities = [0, 1, 2, 3]
    palette = 16
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x39190c
    xp = 150
    coins = 200
    yoshi_cookie_item = items.Mushroom


class CorkpediteBody(Enemy):
    index = 140
    address = 0x3907e6
    hp = 300
    speed = 5
    attack = 100
    defense = 99
    magic_attack = 6
    magic_defense = 1
    fp = 100
    morph_chance = 3
    resistances = [6]
    weaknesses = [4]
    status_immunities = [0, 1, 2, 3]
    palette = 16
    flower_bonus_type = 2
    flower_bonus_chance = 8

    # Reward attributes
    reward_address = 0x391852
    xp = 30
    yoshi_cookie_item = items.Mushroom


class Torte(Enemy):
    index = 142
    address = 0x390cc6
    boss = True
    hp = 100
    speed = 99
    attack = 60
    defense = 50
    magic_attack = 8
    magic_defense = 27
    fp = 100
    death_immune = True
    sound_on_hit = 80
    sound_on_approach = 7
    status_immunities = [0, 1, 2, 3]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x39172c
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.0667
    ratio_fp = 0.5
    ratio_attack = 0.8824
    ratio_defense = 3.3333
    ratio_magic_attack = 0.2857
    ratio_magic_defense = 0.675
    ratio_speed = 6.1875
    ratio_evade = 1.0
    ratio_magic_evade = 1.0


class Shyaway(Enemy):
    index = 143
    address = 0x390676
    hp = 140
    speed = 25
    attack = 90
    defense = 50
    magic_attack = 39
    magic_defense = 73
    fp = 100
    evade = 40
    morph_chance = 3
    sound_on_approach = 2
    weaknesses = [4]
    palette = 8
    flower_bonus_type = 5
    flower_bonus_chance = 3

    # Reward attributes
    reward_address = 0x3917c8
    xp = 1
    coins = 30
    yoshi_cookie_item = items.MapleSyrup
    rare_item = items.HoneySyrup


class JinxClone(Enemy):
    index = 144
    address = 0x3911a6
    boss = True
    hp = 320
    speed = 22
    attack = 180
    defense = 120
    magic_defense = 35
    evade = 30
    death_immune = True
    sound_on_hit = 96
    status_immunities = [1, 3]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x39199c
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.2
    ratio_fp = 0.0
    ratio_attack = 1.8
    ratio_defense = 2.0
    ratio_magic_attack = 0.0
    ratio_magic_defense = 0.35
    ratio_speed = 1.8333
    ratio_evade = 1.0
    ratio_magic_evade = 0.0


class MachineMadeShyster(Enemy):
    index = 145
    address = 0x390b06
    hp = 100
    speed = 36
    attack = 135
    defense = 95
    magic_attack = 90
    magic_defense = 65
    fp = 250
    evade = 10
    morph_chance = 3
    sound_on_hit = 80
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x3919a2
    yoshi_cookie_item = items.Mushroom


class MachineMadeDrillBit(Enemy):
    index = 146
    address = 0x390b36
    boss = True
    hp = 180
    speed = 24
    attack = 130
    defense = 82
    magic_attack = 31
    magic_defense = 69
    fp = 100
    morph_chance = 3
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x3919a8
    yoshi_cookie_item = items.Mushroom


class Formless(Enemy):
    index = 147
    address = 0x390646
    boss = True
    hp = 10
    speed = 2
    magic_attack = 50
    fp = 100
    evade = 100
    death_immune = True
    sound_on_hit = 32
    resistances = [5, 7]
    status_immunities = [0, 1, 2, 3]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x3919ae
    yoshi_cookie_item = items.Mushroom


class Mokura(Enemy):
    index = 148
    address = 0x390656
    boss = True
    hp = 620
    speed = 25
    attack = 120
    defense = 75
    magic_attack = 80
    magic_defense = 90
    fp = 100
    evade = 20
    magic_evade = 10
    death_immune = True
    sound_on_hit = 32
    resistances = [5, 7]
    status_immunities = [0, 1, 2, 3]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x3919b4
    xp = 90
    yoshi_cookie_item = items.Mushroom
    normal_item = items.KerokeroCola
    rare_item = items.RoyalSyrup


class FireCrystal(Enemy):
    index = 149
    address = 0x391146
    boss = True
    hp = 2500
    speed = 10
    defense = 100
    magic_attack = 130
    magic_defense = 60
    fp = 250
    evade = 10
    death_immune = True
    resistances = [6]
    weaknesses = [4]
    status_immunities = [0, 1, 2, 3]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x3919ba
    xp = 40
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.6104
    ratio_fp = 1.25
    ratio_attack = 0.0
    ratio_defense = 1.0
    ratio_magic_attack = 1.3
    ratio_magic_defense = 0.75
    ratio_speed = 0.2
    ratio_evade = 1.0
    ratio_magic_evade = 0.0


class WaterCrystal(Enemy):
    index = 150
    address = 0x391156
    boss = True
    hp = 1800
    speed = 12
    defense = 130
    magic_attack = 120
    magic_defense = 50
    fp = 250
    evade = 20
    death_immune = True
    resistances = [4]
    weaknesses = [6]
    status_immunities = [0, 1, 2, 3]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x3919c0
    xp = 30
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.4395
    ratio_fp = 1.25
    ratio_attack = 0.0
    ratio_defense = 1.3
    ratio_magic_attack = 1.2
    ratio_magic_defense = 0.625
    ratio_speed = 0.24
    ratio_evade = 1.0
    ratio_magic_evade = 0.0


class EarthCrystal(Enemy):
    index = 151
    address = 0x391166
    boss = True
    hp = 3200
    speed = 1
    defense = 70
    magic_attack = 80
    magic_defense = 33
    fp = 250
    evade = 5
    death_immune = True
    resistances = [7]
    weaknesses = [5]
    status_immunities = [0, 1, 2, 3]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x3919c6
    xp = 50
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.7813
    ratio_fp = 1.25
    ratio_attack = 0.0
    ratio_defense = 0.7
    ratio_magic_attack = 0.8
    ratio_magic_defense = 0.4125
    ratio_speed = 0.02
    ratio_evade = 1.0
    ratio_magic_evade = 0.0


class WindCrystal(Enemy):
    index = 152
    address = 0x391176
    boss = True
    hp = 800
    speed = 30
    defense = 200
    magic_attack = 60
    magic_defense = 88
    fp = 250
    evade = 30
    death_immune = True
    resistances = [5]
    weaknesses = [7]
    status_immunities = [0, 1, 2, 3]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x3919cc
    xp = 10
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.1953
    ratio_fp = 1.25
    ratio_attack = 0.0
    ratio_defense = 0.2
    ratio_magic_attack = 0.6
    ratio_magic_defense = 1.1
    ratio_speed = 0.6
    ratio_evade = 1.0
    ratio_magic_evade = 0.0


class MarioClone(Enemy):
    index = 153
    address = 0x390d66
    boss = True
    hp = 200
    speed = 20
    attack = 100
    defense = 90
    magic_attack = 33
    magic_defense = 50
    fp = 25
    death_immune = True
    sound_on_hit = 80
    resistances = [6, 7]
    status_immunities = [0, 1, 2, 3]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x3919d2
    xp = 10
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.1667
    ratio_fp = 0.1
    ratio_attack = 0.8333
    ratio_defense = 1.125
    ratio_magic_attack = 1.65
    ratio_magic_defense = 1.25
    ratio_speed = 5.0
    ratio_evade = 0.0
    ratio_magic_evade = 0.0


class PeachClone(Enemy):
    index = 154
    address = 0x390d76
    boss = True
    hp = 120
    speed = 20
    attack = 90
    defense = 60
    magic_attack = 62
    magic_defense = 70
    fp = 180
    death_immune = True
    status_immunities = [0, 1, 2, 3]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x3919d8
    xp = 1
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.1
    ratio_fp = 0.72
    ratio_attack = 0.75
    ratio_defense = 0.75
    ratio_magic_attack = 3.1
    ratio_magic_defense = 1.75
    ratio_speed = 5.0
    ratio_evade = 0.0
    ratio_magic_evade = 0.0


class BowserClone(Enemy):
    index = 155
    address = 0x390d86
    boss = True
    hp = 300
    speed = 12
    attack = 130
    defense = 100
    magic_attack = 12
    fp = 1
    death_immune = True
    sound_on_hit = 32
    resistances = [6, 7]
    weaknesses = [4]
    status_immunities = [0, 1, 2, 3]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x3919de
    xp = 100
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.25
    ratio_fp = 0.004
    ratio_attack = 1.0833
    ratio_defense = 1.25
    ratio_magic_attack = 0.6
    ratio_magic_defense = 0.0
    ratio_speed = 3.0
    ratio_evade = 0.0
    ratio_magic_evade = 0.0


class GenoClone(Enemy):
    index = 156
    address = 0x390d96
    boss = True
    hp = 250
    speed = 30
    attack = 120
    defense = 80
    magic_attack = 60
    magic_defense = 30
    fp = 40
    death_immune = True
    sound_on_hit = 16
    resistances = [4]
    weaknesses = [6]
    status_immunities = [0, 1, 2, 3]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x3919e4
    xp = 40
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.2083
    ratio_fp = 0.16
    ratio_attack = 1.0
    ratio_defense = 1.0
    ratio_magic_attack = 3.0
    ratio_magic_defense = 0.75
    ratio_speed = 7.5
    ratio_evade = 0.0
    ratio_magic_evade = 0.0


class MallowClone(Enemy):
    index = 157
    address = 0x390da6
    boss = True
    hp = 150
    speed = 14
    attack = 80
    defense = 65
    magic_attack = 70
    magic_defense = 80
    fp = 80
    death_immune = True
    sound_on_hit = 80
    resistances = [4, 5]
    status_immunities = [0, 1, 2, 3]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x3919ea
    xp = 60
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.125
    ratio_fp = 0.32
    ratio_attack = 0.6667
    ratio_defense = 0.8125
    ratio_magic_attack = 3.5
    ratio_magic_defense = 2.0
    ratio_speed = 3.5
    ratio_evade = 0.0
    ratio_magic_evade = 0.0


class Shyster(Enemy):
    index = 158
    address = 0x390286
    hp = 30
    speed = 18
    attack = 20
    defense = 26
    magic_attack = 18
    magic_defense = 10
    fp = 2
    evade = 10
    morph_chance = 3
    sound_on_hit = 80
    palette = 8
    flower_bonus_type = 3
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x39164e
    xp = 3
    coins = 2
    yoshi_cookie_item = items.HoneySyrup
    normal_item = items.HoneySyrup


class Kinklink(Enemy):
    index = 159
    address = 0x390ad6
    boss = True
    hp = 60
    speed = 99
    defense = 10
    fp = 100
    morph_chance = 3
    palette = 16
    flower_bonus_type = 1

    # Reward attributes
    reward_address = 0x3919f0
    yoshi_cookie_item = items.Mushroom


class HanginShy(Enemy):
    index = 161
    address = 0x3911c6
    boss = True
    hp = 10
    speed = 200
    fp = 100
    death_immune = True
    palette = 16
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x3919fc
    yoshi_cookie_item = items.Mushroom


class Smelter(Enemy):
    index = 162
    address = 0x390fc6
    boss = True
    hp = 1500
    defense = 120
    magic_defense = 100
    fp = 100
    death_immune = True
    resistances = [6]
    weaknesses = [5]
    status_immunities = [0, 1, 2, 3]
    palette = 16
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391a02
    yoshi_cookie_item = items.Mushroom


class MachineMadeMack(Enemy):
    index = 163
    address = 0x390af6
    boss = True
    hp = 300
    speed = 10
    attack = 160
    defense = 120
    magic_attack = 95
    magic_defense = 40
    fp = 250
    death_immune = True
    sound_on_hit = 48
    weaknesses = [5]
    status_immunities = [0, 1, 2, 3]
    palette = 24
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391a08
    xp = 120
    coins = 30
    yoshi_cookie_item = items.Mushroom
    rare_item = items.FireBomb


class MachineMadeBowyer(Enemy):
    index = 164
    address = 0x390b16
    boss = True
    hp = 1000
    speed = 200
    attack = 150
    defense = 120
    magic_attack = 90
    magic_defense = 80
    fp = 250
    death_immune = True
    sound_on_hit = 16
    status_immunities = [0, 1, 2, 3]
    palette = 32
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391a0e
    xp = 150
    coins = 40
    yoshi_cookie_item = items.Mushroom
    rare_item = items.IceBomb


class MachineMadeYaridovich(Enemy):
    index = 165
    address = 0x390b26
    boss = True
    hp = 800
    speed = 18
    attack = 180
    defense = 130
    magic_attack = 90
    magic_defense = 50
    fp = 250
    death_immune = True
    sound_on_hit = 32
    status_immunities = [0, 1, 2, 3]
    palette = 32
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391a14
    xp = 180
    coins = 50
    yoshi_cookie_item = items.Mushroom
    rare_item = items.RockCandy


class MachineMadeAxemPink(Enemy):
    index = 166
    address = 0x390b46
    hp = 100
    speed = 35
    attack = 95
    defense = 90
    magic_attack = 40
    magic_defense = 100
    fp = 200
    evade = 25
    magic_evade = 10
    death_immune = True
    sound_on_hit = 48
    resistances = [4]
    weaknesses = [6]
    status_immunities = [0, 1]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 4

    # Reward attributes
    reward_address = 0x391a1a
    xp = 30
    yoshi_cookie_item = items.Mushroom
    rare_item = items.MapleSyrup


class MachineMadeAxemBlack(Enemy):
    index = 167
    address = 0x390b56
    hp = 120
    speed = 55
    attack = 120
    defense = 110
    magic_attack = 4
    magic_defense = 40
    fp = 100
    evade = 30
    death_immune = True
    sound_on_hit = 48
    weaknesses = [5]
    status_immunities = [1, 3]
    palette = 8
    flower_bonus_type = 4
    flower_bonus_chance = 3

    # Reward attributes
    reward_address = 0x391a20
    xp = 20
    yoshi_cookie_item = items.Mushroom
    rare_item = items.MaxMushroom


class MachineMadeAxemRed(Enemy):
    index = 168
    address = 0x390b66
    hp = 180
    speed = 45
    attack = 135
    defense = 95
    magic_attack = 24
    magic_defense = 80
    fp = 100
    evade = 10
    death_immune = True
    sound_on_hit = 48
    resistances = [6]
    weaknesses = [4]
    status_immunities = [1, 3]
    palette = 8
    flower_bonus_type = 5
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391a26
    xp = 50
    yoshi_cookie_item = items.Mushroom
    rare_item = items.RoyalSyrup


class MachineMadeAxemYellow(Enemy):
    index = 169
    address = 0x390b76
    hp = 200
    speed = 20
    attack = 140
    defense = 130
    magic_attack = 16
    magic_defense = 20
    fp = 100
    death_immune = True
    sound_on_hit = 48
    resistances = [5]
    weaknesses = [7]
    status_immunities = [1, 2]
    palette = 8
    flower_bonus_type = 3
    flower_bonus_chance = 8

    # Reward attributes
    reward_address = 0x391a2c
    xp = 25
    yoshi_cookie_item = items.Mushroom
    rare_item = items.MaxMushroom


class MachineMadeAxemGreen(Enemy):
    index = 170
    address = 0x390b86
    hp = 80
    speed = 40
    attack = 105
    defense = 80
    magic_attack = 80
    magic_defense = 120
    fp = 250
    magic_evade = 20
    death_immune = True
    sound_on_hit = 48
    weaknesses = [4]
    status_immunities = [0, 1]
    palette = 8
    flower_bonus_type = 2
    flower_bonus_chance = 4

    # Reward attributes
    reward_address = 0x391a32
    xp = 10
    yoshi_cookie_item = items.Mushroom
    rare_item = items.RoyalSyrup


class Starslap(Enemy):
    index = 176
    address = 0x390306
    boss = True
    hp = 62
    speed = 9
    attack = 25
    defense = 24
    magic_attack = 4
    magic_defense = 10
    fp = 100
    morph_chance = 3
    sound_on_hit = 80
    sound_on_approach = 1
    weaknesses = [5, 6]
    palette = 8
    flower_bonus_type = 4
    flower_bonus_chance = 3

    # Reward attributes
    reward_address = 0x39167e
    xp = 2
    coins = 2
    yoshi_cookie_item = items.Mushroom


class Mukumuku(Enemy):
    index = 177
    address = 0x3904d6
    hp = 108
    speed = 11
    attack = 60
    defense = 47
    magic_attack = 22
    magic_defense = 30
    fp = 100
    magic_evade = 80
    morph_chance = 3
    sound_on_hit = 80
    resistances = [5]
    weaknesses = [6]
    palette = 8
    flower_bonus_type = 5
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391732
    xp = 8
    coins = 1
    yoshi_cookie_item = items.MukuCookie
    rare_item = items.MapleSyrup


class Zeostar(Enemy):
    index = 178
    address = 0x390526
    hp = 90
    speed = 10
    attack = 75
    defense = 60
    magic_attack = 28
    magic_defense = 20
    fp = 4
    morph_chance = 2
    sound_on_hit = 80
    sound_on_approach = 1
    weaknesses = [5, 6]
    palette = 8
    flower_bonus_type = 4
    flower_bonus_chance = 3

    # Reward attributes
    reward_address = 0x391750
    xp = 10
    coins = 3
    yoshi_cookie_item = items.SleepyBomb
    rare_item = items.Mushroom


class Jagger(Enemy):
    index = 179
    address = 0x390d06
    boss = True
    hp = 600
    speed = 30
    attack = 120
    defense = 80
    magic_defense = 50
    fp = 100
    evade = 10
    death_immune = True
    sound_on_hit = 80
    resistances = [6, 7]
    status_immunities = [2]
    palette = 16
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391ad4
    xp = 50
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 1.0
    ratio_fp = 1.0

    #shuffled overworld sprites
    overworld_sprite = 237
    overworld_npc = 237
    battle_sprite = 237
    battle_npc = 237
    overworld_extra_sequence = 8
    battle_extra_sequence = 8
    overworld_push_sequence = 4
    battle_push_sequence = 4
    battle_push_length = 48
    overworld_is_skinny = True
    shadow = MED_SHADOW
    overworld_solidity = [4, 4, 11]
    battle_solidity = [4, 4, 11]
    overworld_y_shift = 1
    battle_y_shift = 1


class Chompweed(Enemy):
    index = 180
    address = 0x390be6
    boss = True
    hp = 10
    fp = 100
    morph_chance = 3
    sound_on_hit = 16
    sound_on_approach = 2
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391a56
    yoshi_cookie_item = items.Mushroom


class Smithy2TankHead(Enemy):
    index = 181
    address = 0x390ff6
    boss = True
    hp = 8000
    speed = 50
    attack = 250
    defense = 130
    magic_attack = 10
    magic_defense = 50
    fp = 30
    death_immune = True
    sound_on_hit = 80
    weaknesses = [5]
    status_immunities = [0, 1, 2, 3]
    palette = 32
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391a5c
    yoshi_cookie_item = items.Mushroom


class Smithy2SafeHead(Enemy):
    index = 182
    address = 0x391006
    boss = True
    hp = 8000
    attack = 40
    defense = 150
    magic_attack = 70
    magic_defense = 100
    fp = 120
    death_immune = True
    resistances = [5, 6, 7]
    weaknesses = [4]
    status_immunities = [0, 1, 2, 3]
    palette = 24
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391a62
    yoshi_cookie_item = items.Mushroom


class Microbomb(Enemy):
    index = 184
    address = 0x390c36
    boss = True
    hp = 30
    speed = 15
    attack = 42
    defense = 30
    magic_attack = 6
    magic_defense = 10
    fp = 100
    sound_on_hit = 80
    weaknesses = [6, 7]
    status_immunities = [1]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 4

    # Reward attributes
    reward_address = 0x391a86
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.025
    ratio_fp = 10.0
    ratio_attack = 0.7
    ratio_defense = 0.71
    ratio_magic_attack = 0.27
    ratio_magic_defense = 0.25
    ratio_speed = 1.0
    ratio_evade = 0.0
    ratio_magic_evade = 0.0


class Grit(Enemy):
    index = 186
    address = 0x390c16
    boss = True
    hp = 10
    fp = 100
    morph_chance = 3
    palette = 16
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391a74
    yoshi_cookie_item = items.Mushroom


class Neosquid(Enemy):
    index = 187
    address = 0x390f76
    boss = True
    hp = 800
    speed = 20
    attack = 180
    defense = 80
    magic_attack = 86
    magic_defense = 50
    fp = 200
    death_immune = True
    sound_on_hit = 32
    status_immunities = [1]
    palette = 16
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391bb2
    xp = 40
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.3636
    ratio_fp = 0.3333
    ratio_attack = 1.5652
    ratio_defense = 0.7407
    ratio_magic_attack = 1.5926
    ratio_magic_defense = 0.8065
    ratio_speed = 0.3077


class YaridovichMirage(Enemy):
    index = 188
    address = 0x390f16
    boss = True
    hp = 500
    speed = 16
    attack = 100
    defense = 40
    magic_attack = 60
    magic_defense = 10
    fp = 100
    sound_on_hit = 32
    weaknesses = [5]
    status_immunities = [0, 1, 2, 3]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391a7a
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.3333
    ratio_fp = 1.0
    ratio_attack = 0.8
    ratio_defense = 0.4706
    ratio_magic_attack = 0.8571
    ratio_magic_defense = 0.1333
    ratio_speed = 0.8


class Helio(Enemy):
    index = 189
    address = 0x390e76
    boss = True
    hp = 10
    attack = 140
    fp = 100
    resistances = [6]
    weaknesses = [4]
    status_immunities = [0, 1, 2, 3]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391a80
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.0031
    ratio_fp = 0.5
    ratio_attack = 0.8
    ratio_defense = 0.0
    ratio_magic_attack = 0.0
    ratio_magic_defense = 0.0
    ratio_speed = 0.0
    ratio_evade = 0.0
    ratio_magic_evade = 0.0


class RightEye(Enemy):
    index = 190
    address = 0x390f86
    boss = True
    hp = 500
    speed = 17
    attack = 128
    defense = 100
    magic_attack = 82
    magic_defense = 36
    fp = 200
    death_immune = True
    resistances = [5]
    weaknesses = [6, 7]
    status_immunities = [1]
    palette = 16
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391ba6
    xp = 30
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.2273
    ratio_fp = 0.3333
    ratio_attack = 1.113
    ratio_defense = 0.9259
    ratio_magic_attack = 1.5185
    ratio_magic_defense = 0.5806
    ratio_speed = 0.2615

    def get_patch(self):
        """Update battle event triggers based on HP to use shuffled HP value instead.

        Returns:
            randomizer.logic.patch.Patch: Patch data

        """
        patch = super().get_patch()

        # TODO: Get addresses for linear mode.
        if self.world.open_mode:
            # Vanilla game gives a 20% bonus when the eye comes back...h*ck it, let's keep it!
            reset_hp = self.round_for_battle_script(self.hp * 1.2)
            patch.add_data(0x35366e, utils.ByteField(reset_hp, num_bytes=2).as_bytes())

        return patch

    def patch_script(self):
        script = BattleScript()
        script.if_bits_set(0x7ee002, 0x01)
        script.if_greater_or_equal(0x7ee004, 0x03)
        script.set_targetable(Monsters.SELF)
        script.zero(0x7ee004)
        script.zero(0x7ee002)
        script.animate(0x0d)
        script.wait_return()

        script.if_bits_set(0x7ee002, 0x01)
        script.inc(0x7ee004)
        script.wait_return()

        script.zero(0x7ee005)
        script.rand(0x07)
        script.if_less_than(0x7ee005, 0x04)
        script.cast_spell(spells.Bolt, spells.DiamondSaw, spells.MegaDrain)
        script.wait_return()

        script.cast_spell(spells.FlameStone, spells.DarkStar, spells.Blast)
        script.start_counter()

        script.if_hp(0x0000)
        script.if_bits_clear(0x7ee008, 0x01)
        script.set(0x7ee002, 0x01)
        script.set(0x7ee000, 0x01)
        script.clear(0x7ee000, 0x04)
        script.set_untargetable(Monsters.SELF)

        if self.world.settings.is_flag_enabled(flags.NoGenoWhirlExor):
            script.set_targetable(Monsters.MONSTER_1)
        else:
            script.uninvuln(Targets.MONSTER_1)

        script.animate(0x0b)
        script.battle_dialog(0xdb)
        script.wait_return()

        self.script = script.fin()


class LeftEye(Enemy):
    index = 191
    address = 0x390f96
    boss = True
    hp = 300
    speed = 21
    attack = 153
    defense = 130
    magic_attack = 47
    magic_defense = 80
    fp = 200
    death_immune = True
    resistances = [5]
    weaknesses = [6, 7]
    status_immunities = [1]
    palette = 16
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391bac
    xp = 30
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.1364
    ratio_fp = 0.3333
    ratio_attack = 1.3304
    ratio_defense = 1.2037
    ratio_magic_attack = 0.8704
    ratio_magic_defense = 1.2903
    ratio_speed = 0.3231

    def get_patch(self):
        """Update battle event triggers based on HP to use shuffled HP value instead.

        Returns:
            randomizer.logic.patch.Patch: Patch data

        """
        patch = super().get_patch()

        # TODO: Get addresses for linear mode.
        if self.world.open_mode:
            patch.add_data(0x35368e, utils.ByteField(self.hp, num_bytes=2).as_bytes())

        return patch

    def patch_script(self):
        script = BattleScript()
        script.if_bits_set(0x7ee003, 0x01)
        script.if_greater_or_equal(0x7ee004, 0x02)
        script.set_targetable(Monsters.SELF)
        script.zero(0x7ee004)
        script.zero(0x7ee003)
        script.animate(0x0d)
        script.wait_return()

        script.if_bits_set(0x7ee003, 0x01)
        script.inc(0x7ee004)
        script.wait_return()

        script.zero(0x7ee005)
        script.rand(0x07)
        script.if_less_than(0x7ee005, 0x04)
        script.set(0x7ee00f, 0x01)
        script.attack(attacks.PhysicalAttack0, attacks.GunkBall, attacks.PhysicalAttack0)
        script.clear(0x7ee00f, 0x01)
        script.wait_return()

        script.set(0x7ee00f, 0x01)
        script.attack(attacks.PhysicalAttack0, attacks.VenomDrool, attacks.ScrowBell)
        script.clear(0x7ee00f, 0x01)
        script.start_counter()

        script.if_hp(0x0000)
        script.if_bits_clear(0x7ee008, 0x01)
        script.set(0x7ee003, 0x01)
        script.set(0x7ee000, 0x02)
        script.clear(0x7ee000, 0x04)
        script.set_untargetable(Monsters.SELF)

        if self.world.settings.is_flag_enabled(flags.NoGenoWhirlExor):
            script.set_targetable(Monsters.MONSTER_1)
        else:
            script.uninvuln(Targets.MONSTER_1)

        script.animate(0x0c)
        script.battle_dialog(0xdb)
        script.wait_return()

        self.script = script.fin()


class KnifeGuy(Enemy):
    index = 192
    address = 0x390c66
    boss = True
    hp = 700
    speed = 25
    attack = 70
    defense = 55
    magic_attack = 20
    magic_defense = 10
    fp = 35
    death_immune = True
    sound_on_hit = 32
    resistances = [5]
    weaknesses = [6]
    status_immunities = [1]
    palette = 24
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391aa4
    xp = 40
    coins = 15
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.44
    ratio_fp = 0.41
    ratio_attack = 1.08
    ratio_defense = 1.15
    ratio_magic_attack = 0.87
    ratio_magic_defense = 0.4
    ratio_speed = 1.25

    #shuffled overworld sprites
    overworld_sprite = 177
    overworld_npc = 452
    battle_sprite = 449
    battle_npc = 449
    other_npcs = [134]
    other_sprites = [134]
    other_battle_sprites = [448]
    other_battle_npcs = [448]
    battle_sprite_is_tall = True
    sprite_width = 41
    sprite_height = 57
    battle_sesw_only = True
    battle_push_length = 44
    battle_push_sequence = 3
    fat_sidekicks = True
    shadow = MED_SHADOW
    overworld_solidity = [3, 3, 12]
    overworld_y_shift = 1
    statue_west_shift = 3
    opposite_statue_west_shift = 2


class GrateGuy(Enemy):
    index = 193
    address = 0x390c76
    boss = True
    hp = 900
    speed = 14
    attack = 60
    defense = 40
    magic_attack = 25
    magic_defense = 40
    fp = 50
    death_immune = True
    sound_on_hit = 96
    resistances = [6]
    weaknesses = [5]
    status_immunities = [1]
    palette = 24
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391aaa
    xp = 50
    coins = 10
    yoshi_cookie_item = items.Mushroom
    normal_item = items.FlowerJar
    rare_item = items.FlowerJar

    # Boss shuffle attributes.
    ratio_hp = 0.56
    ratio_fp = 0.59
    ratio_attack = 0.92
    ratio_defense = 0.83
    ratio_magic_attack = 1.09
    ratio_magic_defense = 1.6
    ratio_speed = 0.7


class Bundt(Enemy):
    index = 194
    address = 0x390c86
    boss = True
    hp = 900
    speed = 16
    attack = 65
    defense = 10
    magic_attack = 25
    magic_defense = 50
    fp = 100
    death_immune = True
    sound_on_hit = 16
    resistances = [4, 5, 6]
    weaknesses = [7]
    status_immunities = [1, 2, 3]
    palette = 16
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391ab0
    xp = 25
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.6
    ratio_fp = 0.5
    ratio_attack = 0.9559
    ratio_defense = 0.6667
    ratio_magic_attack = 0.8929
    ratio_magic_defense = 1.25
    ratio_speed = 1.0

    #shuffled overworld sprites
    overworld_sprite = 470
    overworld_npc = 470
    overworld_sequence = 8
    battle_sprite = 450
    sprite_height = 56
    sprite_width = 35
    overworld_freeze = True
    battle_sesw_only = True
    other_sprites = [398, 398]
    overworld_sesw_only = True
    shadow = LARGE_SHADOW
    overworld_solidity = [7, 7, 8]
    overworld_y_shift = 1
    statue_west_shift = 3

    def get_patch(self):
        """Update battle event triggers based on HP to use shuffled HP value instead.

        Returns:
            randomizer.logic.patch.Patch: Patch data

        """
        patch = super().get_patch()

        if self.world.chocolate_cake:
            data = palette_to_bytes(["A88878", "906858", "906858", "684838", "504028", "382018", "382010", "382818", "201800",
                "484020", "483020", "805848", "483020", "806050", "181818"])
            patch.add_data(0x2547AC, data)
        return patch


class Jinx1(Enemy):
    index = 195
    address = 0x390cd6
    boss = True
    hp = 600
    speed = 30
    attack = 140
    defense = 100
    magic_defense = 80
    fp = 100
    evade = 30
    magic_evade = 25
    death_immune = True
    sound_on_hit = 96
    resistances = [4, 5, 6]
    status_immunities = [0, 1, 2, 3]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2
    hp_counter_ratios = [0.5]

    # Reward attributes
    reward_address = 0x391ac2
    xp = 75
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 1.0
    ratio_fp = 1.0
    name_override = 'JINX 1'

    #shuffled overworld sprites
    overworld_sprite = 207
    overworld_npc = 207
    battle_sprite = 207
    battle_push_sequence = 3
    overworld_push_sequence = 3
    battle_push_length = 10
    overworld_push_length = 10
    overworld_is_empty = True
    shadow = SMALL_SHADOW
    overworld_solidity = [2, 2, 5]
    battle_solidity = [2, 2, 5]
    overworld_y_shift = 0
    battle_y_shift = 0


class Jinx2(Enemy):
    index = 196
    address = 0x390ce6
    boss = True
    hp = 800
    speed = 32
    attack = 160
    defense = 120
    magic_defense = 90
    fp = 100
    evade = 30
    magic_evade = 25
    death_immune = True
    sound_on_hit = 96
    resistances = [4, 5, 6]
    status_immunities = [0, 1, 2, 3]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2
    hp_counter_ratios = [0.5]

    # Reward attributes
    reward_address = 0x391ac8
    xp = 100
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 1.0
    ratio_fp = 1.0
    name_override = 'JINX 2'

    #shuffled overworld sprites
    overworld_sprite = 207
    overworld_npc = 207
    battle_sprite = 207
    battle_push_sequence = 3
    overworld_push_sequence = 3
    battle_push_length = 10
    overworld_push_length = 10
    overworld_is_empty = True
    shadow = SMALL_SHADOW
    overworld_solidity = [2, 2, 5]
    battle_solidity = [2, 2, 5]
    overworld_y_shift = 0
    battle_y_shift = 0

class CountDown(Enemy):
    index = 197
    address = 0x390d26
    boss = True
    hp = 2400
    speed = 5
    defense = 80
    magic_attack = 120
    magic_defense = 80
    fp = 100
    death_immune = True
    weaknesses = [5, 7]
    status_immunities = [0, 1, 2, 3]
    palette = 16
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391ada
    xp = 140
    coins = 100
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.5
    ratio_fp = 0.3333
    ratio_attack = 0.0
    ratio_defense = 0.7477
    ratio_magic_attack = 2.2642
    ratio_magic_defense = 1.3333
    ratio_speed = 0.625

    #shuffled overworld sprites
    overworld_sprite = 454
    overworld_npc = 454
    battle_sprite = 454
    battle_npc = 454
    overworld_sequence = 0
    battle_sequence = 0
    overworld_freeze = True
    battle_freeze = True
    overworld_is_empty = True
    overworld_sesw_only = True
    battle_sesw_only = True
    shadow = LARGE_SHADOW
    overworld_solidity = [11, 11, 10]
    battle_solidity = [11, 11, 10]
    overworld_y_shift = 1
    battle_y_shift = 1


class DingALing(Enemy):
    index = 198
    address = 0x390d36
    boss = True
    hp = 1200
    speed = 10
    attack = 180
    defense = 120
    magic_attack = 20
    magic_defense = 50
    fp = 100
    death_immune = True
    weaknesses = [5]
    status_immunities = [0, 1, 2, 3]
    palette = 16
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391ae0
    xp = 30
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.25
    ratio_fp = 0.3333
    ratio_attack = 1.5
    ratio_defense = 1.1215
    ratio_magic_attack = 0.3774
    ratio_magic_defense = 0.8333
    ratio_speed = 1.25


class Belome1(Enemy):
    index = 199
    address = 0x390d46
    boss = True
    hp = 500
    speed = 4
    attack = 30
    defense = 25
    magic_attack = 15
    magic_defense = 20
    fp = 30
    magic_evade = 10
    death_immune = True
    sound_on_hit = 160
    weaknesses = [5]
    status_immunities = [1]
    palette = 24
    flower_bonus_type = 1
    flower_bonus_chance = 2
    hp_counter_ratios = [300 / 500]

    # Reward attributes
    reward_address = 0x391ae6
    xp = 30
    coins = 40
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 1.0
    ratio_fp = 1.0
    name_override = 'BELOME 1'

    #shuffled overworld sprites
    overworld_sprite = 39
    battle_sprite = 455
    battle_npc = 455
    overworld_sequence = 1
    statue_only = True
    sprite_height = 54
    sprite_width = 49
    overworld_invert_se_sw = True
    battle_sesw_only = True
    battle_push_sequence = 3
    battle_push_length = 38
    overworld_is_empty = True
    shadow = NO_SHADOW
    overworld_solidity = []
    battle_solidity = []
    overworld_y_shift = 0
    battle_y_shift = 0
    overworld_solidity = [8, 3, 10]
    battle_solidity = [10, 10, 18]
    overworld_y_shift = 0
    battle_y_shift = 2


class Belome2(Enemy):
    index = 200
    address = 0x390d56
    boss = True
    hp = 1200
    speed = 4
    attack = 120
    defense = 80
    magic_attack = 20
    magic_defense = 40
    fp = 250
    magic_evade = 25
    death_immune = True
    sound_on_hit = 160
    status_immunities = [1]
    palette = 24
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391aec
    xp = 80
    coins = 20
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 1.0
    ratio_fp = 1.0
    name_override = 'BELOME 2'

    #shuffled overworld sprites
    overworld_sprite = 39
    battle_sprite = 455
    battle_npc = 455
    overworld_sequence = 1
    statue_only = True
    sprite_height = 54
    sprite_width = 49
    overworld_invert_se_sw = True
    battle_sesw_only = True
    battle_push_sequence = 3
    battle_push_length = 38
    overworld_is_empty = True
    shadow = NO_SHADOW
    overworld_solidity = [8, 3, 10]
    battle_solidity = [10, 10, 18]
    overworld_y_shift = 0
    battle_y_shift = 2

class Smilax(Enemy):
    index = 202
    address = 0x390dc6
    boss = True
    hp = 200
    speed = 5
    attack = 100
    defense = 80
    magic_attack = 70
    magic_defense = 50
    fp = 100
    death_immune = True
    sound_on_hit = 16
    weaknesses = [4]
    status_immunities = [0, 1, 2, 3]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391af8
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.0769
    ratio_fp = 0.1111
    ratio_attack = 0.71
    ratio_defense = 1.0
    ratio_magic_attack = 1.0
    ratio_magic_defense = 0.63
    ratio_speed = 2.50


class Thrax(Enemy):
    index = 203
    address = 0x390dd6
    boss = True
    hp = 10
    speed = 200
    fp = 100
    death_immune = True
    status_immunities = [1]
    palette = 24
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391afe
    yoshi_cookie_item = items.Mushroom


class Megasmilax(Enemy):
    index = 204
    address = 0x390de6
    boss = True
    hp = 1000
    speed = 2
    attack = 140
    defense = 80
    magic_attack = 70
    magic_defense = 80
    fp = 100
    death_immune = True
    sound_on_hit = 32
    weaknesses = [4]
    status_immunities = [0, 1, 2, 3]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391b04
    xp = 120
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes
    anchor = True
    ratio_hp = 0.3846
    ratio_fp = 0.1111

    #shuffled overworld sprites
    overworld_sprite = 263
    overworld_npc = 138
    battle_sprite = 460
    battle_npc = 460
    sprite_width = 37
    sprite_height = 37
    battle_push_sequence = 3
    overworld_push_sequence = 3
    battle_push_length = 20
    overworld_push_length = 22
    other_sprites = [263, 263, 263, 263]
    czar_sprite = [458]
    overworld_is_skinny = True
    overworld_sesw_only = True
    battle_sesw_only = True
    shadow = MED_SHADOW
    overworld_solidity = [5, 5, 11]
    overworld_y_shift = 1
    statue_west_shift = 1
    statue_south_shift = 4


class Birdo(Enemy):
    index = 205
    address = 0x390df6
    boss = True
    hp = 777
    speed = 10
    attack = 160
    defense = 130
    magic_attack = 6
    magic_defense = 100
    fp = 100
    death_immune = True
    resistances = [6]
    status_immunities = [0, 1, 2, 3]
    palette = 16
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391b0a
    xp = 60
    coins = 30
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes
    ratio_hp = 1.0
    ratio_fp = 1.0

    #shuffled overworld sprites
    overworld_sprite = 462
    overworld_npc = 462
    battle_sprite = 461
    battle_npc = 461
    statue_only = True
    battle_sprite_is_tall = True
    sprite_height = 57
    sprite_width = 38
    battle_sesw_only = True
    overworld_sesw_only = True
    battle_push_sequence = 3
    battle_push_length = 42
    other_sprites = [462, 462, 462, 462]
    overworld_is_empty = True
    empty_sidekicks = True
    shadow = SMALL_SHADOW
    overworld_solidity = [2, 2, 5]
    battle_solidity = [11, 11, 13]
    overworld_y_shift = 0
    battle_y_shift = 1
    name_override = 'BIRDETTA'


class Eggbert(Enemy):
    index = 206
    address = 0x390e16
    boss = True
    hp = 10
    attack = 210
    fp = 100
    death_immune = True
    status_immunities = [0, 1, 2, 3]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391b10
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.01
    ratio_fp = 1.0
    ratio_attack = 1.31
    ratio_defense = 0.0
    ratio_magic_attack = 0.0
    ratio_magic_defense = 0.0
    ratio_speed = 0.0
    ratio_evade = 0.0
    ratio_magic_evade = 0.0


class AxemYellow(Enemy):
    index = 207
    address = 0x391086
    boss = True
    hp = 600
    speed = 3
    attack = 170
    defense = 130
    magic_attack = 6
    magic_defense = 60
    fp = 100
    death_immune = True
    sound_on_hit = 48
    resistances = [5]
    weaknesses = [7]
    status_immunities = [1, 2]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391b1c
    xp = 30
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.1579
    ratio_fp = 0.125
    ratio_attack = 1.4783
    ratio_defense = 1.3265
    ratio_magic_attack = 0.1538
    ratio_magic_defense = 0.7229
    ratio_speed = 0.0577
    ratio_evade = 0.0
    ratio_magic_evade = 0.0


class Punchinello(Enemy):
    index = 208
    address = 0x390c56
    boss = True
    hp = 1200
    speed = 15
    attack = 60
    defense = 42
    magic_attack = 22
    magic_defense = 40
    fp = 10
    death_immune = True
    sound_on_hit = 32
    resistances = [7]
    status_immunities = [0, 1, 2, 3]
    palette = 16
    flower_bonus_type = 1
    battle_sesw_only = True
    hp_counter_ratios = [2/3, 2/3, 1/3, 1/3]

    # Reward attributes
    reward_address = 0x391a98
    xp = 70
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 1.0
    ratio_fp = 1.0

    #shuffled overworld sprites
    overworld_sprite = 281
    overworld_npc = 145
    battle_sprite = 464
    battle_npc = 464
    other_npcs = [145]
    statue_only = True
    sprite_width = 45
    sprite_height = 45
    battle_push_length = 26
    battle_push_sequence = 3
    other_sprites = [281, 281, 281, 281]
    overworld_is_skinny = True
    shadow = MED_SHADOW
    overworld_solidity = [4, 4, 10]
    battle_solidity = [11, 8, 9]
    overworld_y_shift = 1
    battle_y_shift = 1

class TentaclesRight(Enemy):
    index = 209
    address = 0x390e46
    boss = True
    hp = 260
    speed = 21
    attack = 82
    defense = 50
    magic_attack = 35
    magic_defense = 40
    fp = 100
    sound_on_hit = 64
    weaknesses = [6]
    status_immunities = [0, 1]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391b3a
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.0985
    ratio_fp = 0.1111
    ratio_attack = 0.82
    ratio_defense = 0.625
    ratio_magic_attack = 1.1667
    ratio_magic_defense = 1.0
    ratio_speed = 2.625


class AxemRed(Enemy):
    index = 210
    address = 0x391096
    boss = True
    hp = 800
    speed = 30
    attack = 150
    defense = 100
    magic_attack = 24
    magic_defense = 80
    fp = 100
    evade = 10
    death_immune = True
    sound_on_hit = 48
    resistances = [6]
    weaknesses = [4]
    status_immunities = [1, 3]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391b22
    xp = 40
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.2106
    ratio_fp = 0.125
    ratio_attack = 1.3043
    ratio_defense = 1.0204
    ratio_magic_attack = 0.6154
    ratio_magic_defense = 0.9639
    ratio_speed = 0.5769
    ratio_evade = 0.9091
    ratio_magic_evade = 0.0


class AxemGreen(Enemy):
    index = 211
    address = 0x3910a6
    boss = True
    hp = 450
    speed = 20
    attack = 110
    defense = 60
    magic_attack = 90
    magic_defense = 120
    fp = 200
    magic_evade = 20
    death_immune = True
    sound_on_hit = 48
    weaknesses = [4]
    status_immunities = [0, 1]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391b28
    xp = 20
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.1185
    ratio_fp = 0.25
    ratio_attack = 0.9565
    ratio_defense = 0.6122
    ratio_magic_attack = 0.0
    ratio_magic_defense = 1.4458
    ratio_speed = 0.3846
    ratio_evade = 0.0
    ratio_magic_evade = 4.0


class KingBomb(Enemy):
    index = 212
    address = 0x391196
    boss = True
    hp = 500
    defense = 130
    magic_attack = 80
    fp = 100
    death_immune = True
    sound_on_hit = 96
    weaknesses = [6, 7]
    status_immunities = [0, 1, 2, 3]
    palette = 32
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391a8c
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.3125
    ratio_fp = 0.4
    ratio_attack = 0.0
    ratio_defense = 2.1667
    ratio_magic_attack = 0.6667
    ratio_magic_defense = 0.0
    ratio_speed = 0.0
    ratio_evade = 0.0
    ratio_magic_evade = 0.0

    def patch_script(self):
        script = BattleScript()

        script.if_phase(0x03)
        if self.world.settings.is_flag_enabled(flags.FixMagikoopa):
            script.zero(0x7ee000)
        script.set_targetable(Monsters.MONSTER_1)
        script.cast_spell(spells.BigBang)
        script.remove(0x1b)
        script.wait_return()

        script.start_counter()

        script.if_hp(0x0000)
        script.zero(0x7ee000)
        script.set_targetable(Monsters.MONSTER_1)
        script.animate(0x03)
        script.remove(0x1b)
        script.wait_return()

        self.script = script.fin()

        super().patch_script()

class MezzoBomb(Enemy):
    index = 213
    address = 0x390c46
    boss = True
    hp = 150
    speed = 1
    attack = 70
    defense = 40
    magic_defense = 10
    fp = 100
    sound_on_hit = 96
    weaknesses = [6, 7]
    status_immunities = [1]
    palette = 16
    flower_bonus_type = 3
    flower_bonus_chance = 8

    # Reward attributes
    reward_address = 0x391a92
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.125
    ratio_fp = 10.0
    ratio_attack = 1.17
    ratio_defense = 0.95
    ratio_magic_attack = 0.0
    ratio_magic_defense = 0.25
    ratio_speed = 0.07
    ratio_evade = 0.0
    ratio_magic_evade = 0.0


class Raspberry(Enemy):
    index = 215
    address = 0x390c96
    boss = True
    hp = 600
    speed = 16
    attack = 70
    defense = 20
    magic_attack = 30
    magic_defense = 30
    fp = 100
    death_immune = True
    sound_on_hit = 32
    resistances = [4, 5, 6]
    weaknesses = [7]
    status_immunities = [1, 2, 3]
    palette = 16
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391abc
    xp = 50
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.4
    ratio_fp = 0.5
    ratio_attack = 1.0294
    ratio_defense = 1.3333
    ratio_magic_attack = 1.0714
    ratio_magic_defense = 0.75
    ratio_speed = 1.0

    def get_patch(self):
        """Update battle event triggers based on HP to use shuffled HP value instead.

        Returns:
            randomizer.logic.patch.Patch: Patch data

        """
        patch = super().get_patch()

        if self.world.chocolate_cake:
            data = palette_to_bytes(["A88878", "806858", "704838", "685040", "604838", "503828", "685040", "684028", "482820",
                "584028", "684838", "382820", "402010", "583828", "281808"])
            patch.add_data(0x254770, data)
        return patch


class KingCalamari(Enemy):
    index = 216
    address = 0x390e26
    boss = True
    hp = 800
    speed = 8
    attack = 100
    defense = 80
    magic_attack = 30
    magic_defense = 40
    fp = 100
    death_immune = True
    sound_on_hit = 176
    weaknesses = [6]
    status_immunities = [0, 1, 2, 3]
    palette = 32
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391b40
    xp = 100
    coins = 100
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes
    anchor = True
    ratio_hp = 0.303
    ratio_fp = 0.1111

    #shuffled overworld sprites
    overworld_sprite = 266
    overworld_npc = 266
    overworld_push_sequence = 3
    overworld_push_length = 34
    battle_sprite = 465
    battle_push_sequence = 3
    battle_push_length = 35
    overworld_is_skinny = True
    sprite_width = 34
    sprite_height = 52
    overworld_sesw_only = True
    battle_sesw_only = True
    shadow = MED_SHADOW
    overworld_solidity = [5, 5, 11]
    battle_solidity = [11, 11, 13]
    overworld_y_shift = -2
    battle_y_shift = 1


class TentaclesLeft(Enemy):
    index = 217
    address = 0x390e36
    boss = True
    hp = 200
    speed = 21
    attack = 87
    defense = 70
    magic_attack = 35
    magic_defense = 23
    fp = 100
    death_immune = True
    sound_on_hit = 64
    weaknesses = [6]
    status_immunities = [0, 1]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391b46
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.0758
    ratio_fp = 0.1111
    ratio_attack = 0.87
    ratio_defense = 1.0
    ratio_magic_attack = 1.1667
    ratio_magic_defense = 0.575
    ratio_speed = 2.625


class Jinx3(Enemy):
    index = 218
    address = 0x390cf6
    boss = True
    hp = 1000
    speed = 35
    attack = 180
    defense = 140
    magic_defense = 100
    fp = 100
    evade = 30
    magic_evade = 25
    death_immune = True
    sound_on_hit = 96
    resistances = [4, 5, 6]
    status_immunities = [0, 1, 2, 3]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2
    hp_counter_ratios = [0.6, 0.3]

    # Reward attributes
    reward_address = 0x391ace
    xp = 150
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 1.0
    ratio_fp = 1.0
    name_override = 'JINX 3'

    #shuffled overworld sprites
    overworld_sprite = 207
    overworld_npc = 207
    battle_sprite = 207
    battle_push_sequence = 3
    overworld_push_sequence = 3
    battle_push_length = 10
    overworld_push_length = 10
    overworld_is_empty = True
    shadow = SMALL_SHADOW
    overworld_solidity = [2, 2, 5]
    battle_solidity = [2, 2, 5]
    overworld_y_shift = 0
    battle_y_shift = 0



class Zombone(Enemy):
    index = 219
    address = 0x390e56
    boss = True
    hp = 1800
    speed = 6
    attack = 190
    defense = 60
    magic_attack = 80
    magic_defense = 100
    fp = 100
    magic_evade = 10
    death_immune = True
    sound_on_hit = 32
    resistances = [4, 6]
    weaknesses = [5, 7]
    status_immunities = [1, 2, 3]
    palette = 32
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391b4c
    xp = 50
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.5625
    ratio_fp = 0.5
    ratio_attack = 1.0857
    ratio_defense = 0.75
    ratio_magic_attack = 0.8
    ratio_magic_defense = 1.1765
    ratio_speed = 0.4615
    ratio_evade = 0.0
    ratio_magic_evade = 2.0


class CzarDragon(Enemy):
    index = 220
    address = 0x390e66
    boss = True
    hp = 1400
    speed = 20
    attack = 160
    defense = 100
    magic_attack = 120
    magic_defense = 70
    fp = 100
    evade = 20
    death_immune = True
    sound_on_hit = 32
    resistances = [6]
    weaknesses = [4]
    status_immunities = [1]
    palette = 32
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391b52
    xp = 100
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.4375
    ratio_fp = 0.5
    ratio_attack = 0.9143
    ratio_defense = 1.25
    ratio_magic_attack = 1.2
    ratio_magic_defense = 0.8235
    ratio_speed = 1.5385
    ratio_evade = 2.0
    ratio_magic_evade = 0.0


    #shuffled overworld sprites
    overworld_sprite = 277
    overworld_npc = 277
    battle_sprite = 216
    battle_npc = 216
    statue_only = True
    battle_sprite_is_wide = True
    sprite_width = 59
    sprite_height = 54
    battle_sesw_only = True
    overworld_push_sequence = 3
    overworld_push_length = 30
    other_sprites = [277, 277, 277, 277]
    overworld_is_skinny = True
    overworld_sesw_only = True
    shadow = MED_SHADOW
    overworld_solidity = [5, 5, 11]
    overworld_y_shift = 3


class Cloaker(Enemy):
    index = 221
    address = 0x390e86
    boss = True
    hp = 1200
    speed = 20
    attack = 170
    defense = 130
    magic_attack = 12
    magic_defense = 20
    fp = 100
    death_immune = True
    sound_on_hit = 48
    status_immunities = [0, 1, 2, 3]
    palette = 32
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391b58
    xp = 60
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.3934
    ratio_fp = 0.1429
    ratio_attack = 1.1688
    ratio_defense = 1.3
    ratio_magic_attack = 0.2105
    ratio_magic_defense = 0.2222
    ratio_speed = 1.1111

    #shuffled overworld sprites
    overworld_sprite = 249
    overworld_npc = 249
    battle_sprite = 477
    other_battle_sprites = [478, 499, 479]
    statue_only = True
    battle_sprite_is_tall = True
    sprite_width = 50
    sprite_height = 62
    overworld_freeze = True
    overworld_sesw_only = True
    battle_sesw_only = True
    battle_push_sequence = 3
    battle_push_length = 42
    shadow = BLOCK_SHADOW
    overworld_solidity = [7, 7, 7]
    overworld_y_shift = 0
    statue_west_shift = 4
    statue_south_shift = 3


class Domino(Enemy):
    index = 222
    address = 0x390eb6
    boss = True
    hp = 900
    speed = 25
    attack = 65
    defense = 80
    magic_attack = 120
    magic_defense = 150
    fp = 250
    death_immune = True
    sound_on_hit = 16
    status_immunities = [0, 1, 2, 3]
    palette = 32
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391b5e
    xp = 60
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.2951
    ratio_fp = 0.3571
    ratio_attack = 0.4221
    ratio_defense = 0.8
    ratio_magic_attack = 2.1053
    ratio_magic_defense = 1.6667
    ratio_speed = 1.3889


class MadAdder(Enemy):
    index = 223
    address = 0x390ed6
    boss = True
    hp = 1500
    speed = 10
    attack = 150
    defense = 70
    magic_attack = 90
    magic_defense = 180
    fp = 250
    death_immune = True
    sound_on_hit = 32
    status_immunities = [0, 1, 2, 3]
    palette = 32
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391b64
    xp = 200
    yoshi_cookie_item = items.Mushroom
    normal_item = items.Crystalline
    rare_item = items.Crystalline

    # Boss shuffle attributes.
    ratio_hp = 0.4918
    ratio_fp = 0.3571
    ratio_attack = 0.974
    ratio_defense = 0.7
    ratio_magic_attack = 1.5789
    ratio_magic_defense = 2.0
    ratio_speed = 0.5556


class Mack(Enemy):
    index = 224
    address = 0x390ee6
    boss = True
    hp = 480
    speed = 8
    attack = 22
    defense = 25
    magic_attack = 15
    magic_defense = 20
    fp = 28
    death_immune = True
    sound_on_hit = 48
    weaknesses = [5]
    status_immunities = [0, 1, 2, 3]
    palette = 24
    flower_bonus_type = 1

    # Reward attributes
    reward_address = 0x391b7c
    xp = 24
    coins = 20
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes
    anchor = True
    ratio_hp = 0.8

    #shuffled overworld sprites
    overworld_sprite = 414
    overworld_npc = 414
    battle_sprite = 480
    battle_npc = 480
    battle_sequence = 7
    statue_only = True
    battle_sprite_is_tall = True
    battle_sesw_only = True
    sprite_height = 57
    sprite_width = 43
    overworld_push_sequence = 4
    other_sprites = [414, 414, 414, 414]
    overworld_is_skinny = True
    overworld_push_length = 54
    shadow = MED_SHADOW
    overworld_solidity = [3, 3, 11]
    battle_solidity = [13, 13, 23]
    overworld_y_shift = 1
    battle_y_shift = 1


class Bodyguard(Enemy):
    index = 225
    address = 0x390ef6
    boss = True
    hp = 30
    speed = 15
    attack = 20
    defense = 22
    magic_attack = 19
    magic_defense = 12
    fp = 3
    evade = 10
    sound_on_hit = 80
    status_immunities = [0, 1, 2, 3]
    palette = 8
    flower_bonus_type = 3
    flower_bonus_chance = 3

    # Reward attributes
    reward_address = 0x391b82
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes
    ratio_hp = 0.05
    ratio_fp = 0.1071
    ratio_attack = 0.91
    ratio_defense = 0.88
    ratio_magic_attack = 1.27
    ratio_magic_defense = 0.6
    ratio_speed = 1.88
    ratio_evade = 0.1
    ratio_magic_evade = 0.0


class Yaridovich(Enemy):
    index = 226
    address = 0x390f06
    boss = True
    hp = 1500
    speed = 20
    attack = 125
    defense = 85
    magic_attack = 70
    magic_defense = 75
    fp = 100
    death_immune = True
    sound_on_hit = 32
    weaknesses = [5]
    status_immunities = [0, 1, 2, 3]
    palette = 32
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391b88
    xp = 120
    coins = 50
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 1.0
    ratio_fp = 1.0
    battle_push_length = 78

    #shuffled overworld sprites
    overworld_sprite = 163
    overworld_npc = 40
    battle_sprite = 482
    battle_sprite_is_tall = True
    battle_sesw_only = True
    sprite_width = 56
    sprite_height = 84
    battle_push_sequence = 3
    other_sprites = [162, 162, 162, 162]
    overworld_is_skinny = True
    shadow = MED_SHADOW
    overworld_solidity = [4, 4, 9]
    overworld_y_shift = 1


class DrillBit(Enemy):
    index = 227
    address = 0x390f26
    boss = True
    hp = 80
    speed = 15
    attack = 85
    defense = 70
    magic_attack = 40
    magic_defense = 56
    fp = 100
    status_immunities = [0, 1, 2, 3]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x39179e
    xp = 11
    coins = 1
    yoshi_cookie_item = items.Mushroom


class AxemPink(Enemy):
    index = 228
    address = 0x3910b6
    boss = True
    hp = 400
    speed = 25
    attack = 120
    defense = 80
    magic_attack = 80
    magic_defense = 100
    fp = 200
    evade = 25
    magic_evade = 10
    death_immune = True
    sound_on_hit = 48
    resistances = [4]
    weaknesses = [6]
    status_immunities = [0, 1]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391b2e
    xp = 10
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.1053
    ratio_fp = 0.25
    ratio_attack = 1.0435
    ratio_defense = 0.8163
    ratio_magic_attack = 2.0513
    ratio_magic_defense = 1.2048
    ratio_speed = 0.4808
    ratio_evade = 2.2727
    ratio_magic_evade = 2.0


class AxemBlack(Enemy):
    index = 229
    address = 0x3910c6
    boss = True
    hp = 550
    speed = 35
    attack = 140
    defense = 120
    magic_attack = 4
    magic_defense = 40
    fp = 100
    evade = 30
    death_immune = True
    sound_on_hit = 48
    weaknesses = [5]
    status_immunities = [1, 3]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391b34
    xp = 40
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.1448
    ratio_fp = 0.125
    ratio_attack = 1.2174
    ratio_defense = 1.2245
    ratio_magic_attack = 0.1026
    ratio_magic_defense = 0.4819
    ratio_speed = 0.6731
    ratio_evade = 2.7273
    ratio_magic_evade = 0.0


class Bowyer(Enemy):
    index = 230
    address = 0x390f36
    boss = True
    hp = 720
    speed = 10
    attack = 50
    defense = 40
    magic_attack = 30
    magic_defense = 35
    fp = 250
    death_immune = True
    sound_on_hit = 16
    status_immunities = [0, 1, 2, 3]
    palette = 32
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391b8e
    xp = 60
    coins = 50
    yoshi_cookie_item = items.Mushroom
    normal_item = items.FlowerBox
    rare_item = items.FlowerBox

    #shuffled overworld sprites
    overworld_sprite = 487
    overworld_npc = 487
    battle_sprite = 241
    battle_npc = 241
    statue_only = True
    battle_sprite_is_tall = True
    sprite_width = 47
    sprite_height = 52
    overworld_sesw_only = True
    battle_sesw_only = True
    other_sprites = [487, 487, 487, 487]
    overworld_is_skinny = True
    overworld_freeze = True
    overworld_sequence = 1
    shadow = SMALL_SHADOW
    overworld_solidity = [3, 3, 13]
    battle_solidity = [6, 8, 16]
    overworld_y_shift = 1
    battle_y_shift = 1
    statue_mold = 3


class Aero(Enemy):
    index = 231
    address = 0x390f46
    boss = True
    hp = 10
    fp = 100
    status_immunities = [0, 1, 2, 3]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391b94
    yoshi_cookie_item = items.Mushroom


class Exor(Enemy):
    index = 233
    address = 0x390f66
    boss = True
    hp = 1800
    speed = 200
    defense = 120
    magic_defense = 80
    death_immune = True
    resistances = [5]
    status_immunities = [0, 1, 2, 3]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391ba0
    xp = 100
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.8182
    ratio_fp = 0.0
    ratio_attack = 0.0
    ratio_defense = 1.1111
    ratio_magic_attack = 0.0
    ratio_magic_defense = 1.2903
    ratio_speed = 3.0769

    #shuffled overworld sprites
    overworld_sprite = 0
    battle_sprite = 0
    overworld_sequence = 10
    battle_sequence = 10
    overworld_sprite_plus = 3
    battle_sprite_plus = 3
    overworld_sesw_only = True
    battle_sesw_only = True
    overworld_is_empty = True
    overworld_freeze = True
    battle_freeze = True
    shadow = MED_SHADOW
    overworld_solidity = [3, 3, 12]
    battle_solidity = [3, 3, 12]
    overworld_y_shift = 1
    battle_y_shift = 1
    statue_mold = 22

    def patch_script(self):
        script = BattleScript()
        script.if_bits_clear(0x7ee000, 0x07)
        script.if_target_alive(Targets.MONSTER_3)
        script.if_target_alive(Targets.MONSTER_4)
        script.set(0x7ee000, 0x04)
        script.battle_dialog(0xda)

        if self.world.settings.is_flag_enabled(flags.NoGenoWhirlExor):
            script.set_untargetable(Monsters.MONSTER_1)
        else:
            script.invuln(Targets.MONSTER_1)

        script.wait_return()

        script.start_counter()

        script.if_hp(0x0000)
        script.set(0x7ee008, 0x01)
        script.set_untargetable(Monsters.MONSTER_2)
        script.set_untargetable(Monsters.MONSTER_3)
        script.set_untargetable(Monsters.MONSTER_4)
        script.remove(0x1b)
        script.wait_return()

        self.script = script.fin()


class Smithy1(Enemy):
    index = 234
    address = 0x390fa6
    boss = True
    hp = 2000
    speed = 30
    attack = 230
    defense = 130
    magic_attack = 100
    magic_defense = 100
    fp = 250
    death_immune = True
    sound_on_hit = 96
    status_immunities = [0, 1, 2, 3]
    palette = 32
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391bb8
    yoshi_cookie_item = items.Mushroom


class Shyper(Enemy):
    index = 235
    address = 0x390fb6
    boss = True
    hp = 400
    speed = 42
    attack = 170
    defense = 80
    magic_attack = 70
    magic_defense = 50
    fp = 30
    evade = 20
    death_immune = True
    sound_on_hit = 80
    status_immunities = [0, 1, 2, 3]
    palette = 32
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391bbe
    yoshi_cookie_item = items.Mushroom


class Smithy2Body(Enemy):
    index = 236
    address = 0x390fd6
    boss = True
    hp = 1000
    speed = 30
    attack = 180
    defense = 80
    magic_attack = 20
    magic_defense = 60
    fp = 50
    death_immune = True
    sound_on_hit = 96
    status_immunities = [0, 1, 2, 3]
    palette = 32
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391bc4
    yoshi_cookie_item = items.Mushroom


class Smithy2Head(Enemy):
    index = 237
    address = 0x390fe6
    boss = True
    hp = 8000
    speed = 40
    attack = 180
    defense = 80
    magic_attack = 60
    magic_defense = 50
    fp = 50
    death_immune = True
    sound_on_hit = 96
    status_immunities = [0, 1, 2, 3]
    palette = 32
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391bca
    yoshi_cookie_item = items.Mushroom


class Smithy2MageHead(Enemy):
    index = 238
    address = 0x391016
    boss = True
    hp = 8000
    speed = 35
    attack = 135
    defense = 50
    magic_attack = 130
    magic_defense = 150
    fp = 250
    death_immune = True
    sound_on_hit = 96
    resistances = [4, 5, 6]
    status_immunities = [0, 1, 2, 3]
    palette = 32
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391bd0
    yoshi_cookie_item = items.Mushroom


class Smithy2ChestHead(Enemy):
    index = 239
    address = 0x391026
    boss = True
    hp = 8000
    speed = 18
    attack = 150
    defense = 120
    magic_attack = 78
    magic_defense = 80
    fp = 250
    death_immune = True
    sound_on_hit = 96
    resistances = [5]
    weaknesses = [6]
    status_immunities = [0, 1, 2, 3]
    palette = 24
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391bd6
    yoshi_cookie_item = items.Mushroom


class Croco1(Enemy):
    index = 240
    address = 0x391036
    boss = True
    hp = 320
    speed = 16
    attack = 25
    defense = 25
    magic_attack = 30
    magic_defense = 18
    fp = 12
    evade = 20
    death_immune = True
    sound_on_hit = 16
    weaknesses = [6]
    status_immunities = [1, 5, 6]
    palette = 8
    flower_bonus_type = 1
    hp_counter_ratios = [100 / 320]

    # Reward attributes
    reward_address = 0x391bdc
    xp = 16
    coins = 10
    yoshi_cookie_item = items.Mushroom
    normal_item = items.FlowerTab
    rare_item = items.FlowerTab

    # Boss shuffle attributes.
    ratio_hp = 1.0
    ratio_fp = 1.0
    name_override = 'CROCO 1'

    #shuffled overworld sprites
    overworld_sprite = 48
    overworld_npc = 48
    battle_sprite = 48
    battle_npc = 48
    overworld_extra_sequence = 5
    battle_extra_sequence = 5
    other_sprites = [261, 261, 261]
    fat_sidekicks = True
    shadow = MED_SHADOW
    overworld_solidity = [5, 5, 10]
    battle_solidity = [5, 5, 10]
    overworld_y_shift = 2
    battle_y_shift = 2
    statue_west_shift = 3

class Croco2(Enemy):
    index = 241
    address = 0x391046
    boss = True
    hp = 750
    speed = 20
    attack = 52
    defense = 50
    magic_attack = 27
    magic_defense = 50
    fp = 12
    evade = 20
    death_immune = True
    sound_on_hit = 16
    weaknesses = [6]
    status_immunities = [1, 5, 6]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2
    hp_counter_ratios = [400 / 750]

    # Reward attributes
    reward_address = 0x391be2
    xp = 30
    coins = 50
    yoshi_cookie_item = items.Mushroom
    rare_item = items.FlowerBox

    # Boss shuffle attributes.
    ratio_hp = 1.0
    ratio_fp = 1.0
    name_override = 'CROCO 2'

    #shuffled overworld sprites
    overworld_sprite = 48
    overworld_npc = 48
    battle_sprite = 48
    battle_npc = 48
    overworld_extra_sequence = 5
    battle_extra_sequence = 5
    other_sprites = [261, 261, 261]
    fat_sidekicks = True
    shadow = MED_SHADOW
    overworld_solidity = [5, 5, 10]
    battle_solidity = [5, 5, 10]
    overworld_y_shift = 2
    battle_y_shift = 2
    statue_west_shift = 3


class Earthlink(Enemy):
    index = 243
    address = 0x390ea6
    boss = True
    hp = 2500
    speed = 16
    attack = 220
    defense = 120
    magic_attack = 5
    magic_defense = 10
    fp = 100
    death_immune = True
    sound_on_hit = 32
    status_immunities = [0, 1, 2, 3]
    palette = 32
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391b6a
    xp = 200
    yoshi_cookie_item = items.Mushroom
    normal_item = items.PowerBlast
    rare_item = items.PowerBlast

    # Boss shuffle attributes.
    ratio_hp = 0.8197
    ratio_fp = 0.1429
    ratio_attack = 1.4286
    ratio_defense = 1.2
    ratio_magic_attack = 0.0877
    ratio_magic_defense = 0.1111
    ratio_speed = 0.8889


class Bowser(Enemy):
    index = 244
    address = 0x391066
    boss = True
    hp = 320
    speed = 15
    attack = 1
    defense = 12
    fp = 100
    death_immune = True
    sound_on_hit = 32
    status_immunities = [0, 1, 2, 3]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391bee
    yoshi_cookie_item = items.Mushroom


class AxemRangers(Enemy):
    index = 245
    address = 0x391076
    boss = True
    hp = 999
    speed = 200
    defense = 100
    magic_attack = 120
    magic_defense = 100
    fp = 100
    death_immune = True
    sound_on_hit = 96
    weaknesses = [5]
    status_immunities = [0, 1, 2, 3]
    palette = 24
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391b16
    xp = 50
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.263
    ratio_fp = 0.125
    ratio_attack = 0.0
    ratio_defense = 1.0204
    ratio_magic_attack = 3.0769
    ratio_magic_defense = 1.2048
    ratio_speed = 3.8462
    ratio_evade = 0.0
    ratio_magic_evade = 0.0

    #shuffled overworld sprites
    overworld_sprite = 466
    overworld_npc = 466
    battle_sprite = 466
    battle_npc = 466
    other_npcs = [209, 210, 211, 212]
    other_sprites = [209, 210, 211, 212]
    battle_push_sequence = 3
    battle_push_length = 24
    overworld_push_sequence = 3
    overworld_push_length = 24
    fat_sidekicks = True
    shadow = MED_SHADOW
    overworld_solidity = [5, 5, 12]
    battle_solidity = [5, 5, 12]
    overworld_y_shift = 0
    battle_y_shift = 0
    overworld_sesw_only = True
    battle_sesw_only = True
    statue_west_shift = 6


class Booster(Enemy):
    index = 246
    address = 0x3910d6
    boss = True
    hp = 800
    speed = 24
    attack = 75
    defense = 55
    magic_attack = 1
    magic_defense = 40
    fp = 2
    death_immune = True
    sound_on_hit = 96
    sound_on_approach = 3
    weaknesses = [7]
    status_immunities = [1]
    palette = 16
    flower_bonus_type = 1
    flower_bonus_chance = 2
    hp_counter_ratios = [500 / 800]

    # Reward attributes
    reward_address = 0x391bf4
    xp = 60
    coins = 100
    yoshi_cookie_item = items.Mushroom
    rare_item = items.FlowerBox

    # Boss shuffle attributes
    anchor = True
    ratio_hp = 0.57
    ratio_fp = 0.02

    #shuffled overworld sprites
    overworld_sprite = 50
    overworld_npc = 50
    battle_sprite = 50
    battle_npc = 50
    other_npcs = [504]
    other_sprites = [504, 504, 504]
    overworld_extra_sequence = 2
    battle_extra_sequence = 2
    overworld_push_sequence = 4
    battle_push_sequence = 4
    overworld_push_length = 72
    battle_push_length = 72
    overworld_is_skinny = True
    shadow = MED_SHADOW
    overworld_solidity = [5, 5, 12]
    battle_solidity = [5, 5, 12]
    overworld_y_shift = 2
    battle_y_shift = 2


class Booster2(Enemy):
    index = 247
    address = 0x3910e6
    boss = True
    hp = 10
    fp = 100
    death_immune = True
    sound_on_hit = 96
    palette = 16
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391bfa
    yoshi_cookie_item = items.Mushroom


class Snifit(Enemy):
    index = 248
    address = 0x3904a6
    boss = True
    hp = 200
    speed = 26
    attack = 60
    defense = 60
    magic_attack = 20
    magic_defense = 20
    fp = 32
    sound_on_hit = 128
    weaknesses = [4]
    palette = 8
    flower_bonus_type = 5
    flower_bonus_chance = 8

    # Reward attributes
    reward_address = 0x39171a
    xp = 2
    coins = 15
    yoshi_cookie_item = items.Mushroom
    rare_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.14
    ratio_fp = 0.33
    ratio_attack = 0.80
    ratio_defense = 1.09
    ratio_magic_attack = 1.0
    ratio_magic_defense = 0.5
    ratio_speed = 1.08
    ratio_evade = 0.0
    ratio_magic_evade = 0.0


class Johnny(Enemy):
    index = 249
    address = 0x3910f6
    boss = True
    hp = 820
    speed = 13
    attack = 85
    defense = 80
    magic_attack = 25
    magic_defense = 60
    fp = 100
    death_immune = True
    sound_on_hit = 32
    status_immunities = [1]
    palette = 32
    flower_bonus_type = 1
    flower_bonus_chance = 2
    hp_counter_ratios = [400 / 820]

    # Reward attributes
    reward_address = 0x391c00
    xp = 90
    coins = 50
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 1.0
    ratio_fp = 1.0

    #shuffled overworld sprites
    overworld_sprite = 55
    overworld_npc = 52
    battle_sprite = 505
    other_npcs = [331]
    battle_sprite_is_wide = True
    sprite_height = 55
    sprite_width = 64
    overworld_extra_sequence = 10
    battle_push_sequence = 3
    battle_push_length = 38
    other_sprites = [331, 331, 331, 331]
    shadow = MED_SHADOW
    overworld_solidity = [5, 5, 11]
    overworld_y_shift = 2


class JohnnySolo(Enemy):
    index = 250
    address = 0x390d16
    boss = True
    hp = 400
    speed = 30
    attack = 90
    defense = 100
    magic_defense = 32
    fp = 100
    evade = 10
    death_immune = True
    sound_on_hit = 32
    resistances = [6, 7]
    status_immunities = [2]
    palette = 32
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391c06
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.4878
    ratio_fp = 1.0
    ratio_attack = 1.0588
    ratio_defense = 1.25
    ratio_magic_attack = 0.0
    ratio_magic_defense = 0.5333
    ratio_speed = 2.3077
    ratio_evade = 1.0
    ratio_magic_evade = 1.0


class Valentina(Enemy):
    index = 251
    address = 0x391106
    boss = True
    hp = 2000
    speed = 200
    attack = 120
    defense = 80
    magic_attack = 80
    magic_defense = 60
    fp = 250
    evade = 10
    death_immune = True
    sound_on_hit = 32
    resistances = [4]
    status_immunities = [0, 1, 2, 3]
    palette = 24
    flower_bonus_type = 1
    flower_bonus_chance = 2
    hp_counter_ratios = [0.6]

    # Reward attributes
    reward_address = 0x391c0c
    xp = 120
    coins = 200
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes
    anchor = True
    ratio_hp = 0.8333
    ratio_fp = 0.7143

    #shuffled overworld sprites
    overworld_sprite = 56
    overworld_npc = 56
    battle_sprite = 507
    battle_sprite_is_tall = True
    sprite_height = 82
    sprite_width = 51
    overworld_extra_sequence = 2
    battle_push_sequence = 3
    battle_push_length = 18
    battle_sesw_only = True
    overworld_is_skinny = True
    shadow = SMALL_SHADOW

    other_sprites = [333, 333, 333, 333]
    fat_sidekicks = True
    overworld_solidity = [3, 3, 12]
    overworld_y_shift = 1
    statue_west_shift = 3
    statue_south_shift = 1
    opposite_statue_west_shift = 2


class Cloaker2(Enemy):
    index = 252
    address = 0x390e96
    boss = True
    hp = 1200
    speed = 20
    attack = 180
    defense = 130
    magic_attack = 12
    magic_defense = 20
    fp = 100
    death_immune = True
    sound_on_hit = 48
    status_immunities = [0, 1, 2, 3]
    palette = 32
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391b70
    xp = 60
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.3934
    ratio_fp = 0.1429
    ratio_attack = 1.1688
    ratio_defense = 1.3
    ratio_magic_attack = 0.2105
    ratio_magic_defense = 0.2222
    ratio_speed = 1.1111


class Domino2(Enemy):
    index = 253
    address = 0x390ec6
    boss = True
    hp = 900
    speed = 25
    attack = 65
    defense = 80
    magic_attack = 120
    magic_defense = 150
    fp = 250
    death_immune = True
    sound_on_hit = 16
    status_immunities = [0, 1, 2, 3]
    palette = 32
    flower_bonus_type = 1

    # Reward attributes
    reward_address = 0x391b76
    xp = 60
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 0.2951
    ratio_fp = 0.3571
    ratio_attack = 0.4221
    ratio_defense = 0.8
    ratio_magic_attack = 2.1053
    ratio_magic_defense = 1.6667
    ratio_speed = 1.3889


class Candle(Enemy):
    index = 254
    address = 0x390cb6
    boss = True
    hp = 10
    fp = 100
    status_immunities = [0, 1, 2, 3]
    palette = 8
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391c1e
    yoshi_cookie_item = items.Mushroom


class Culex(Enemy):
    index = 255
    address = 0x391136
    boss = True
    hp = 4096
    speed = 50
    attack = 250
    defense = 100
    magic_attack = 100
    magic_defense = 80
    fp = 200
    death_immune = True
    sound_on_hit = 32
    status_immunities = [0, 1, 2, 3]
    palette = 32
    flower_bonus_type = 1
    flower_bonus_chance = 2

    # Reward attributes
    reward_address = 0x391c24
    xp = 600
    yoshi_cookie_item = items.Mushroom

    # Boss shuffle attributes.
    ratio_hp = 1.0
    ratio_fp = 1.0

    #shuffled overworld sprites
    overworld_sprite = 511
    battle_sprite = 511
    overworld_sequence = 8
    other_sprites = [786, 789, 789, 786]
    other_sprites_sequences = [1, 0, 1, 0]
    sprite_height = 143
    sprite_width = 90
    overworld_sesw_only = True
    battle_sesw_only = True
    overworld_is_empty = True
    overworld_freeze = True
    shadow = LARGE_SHADOW
    overworld_solidity = [4, 4, 8]
    overworld_y_shift = 1
    statue_mold = 3

# ********************* Default lists for the world.

def get_default_enemies(world):
    """

    Args:
        world (randomizer.logic.main.GameWorld):

    Returns:
        list[Enemy]: Default list of objects for the world.

    """
    return [
        Terrapin(world),
        Spikey(world),
        Skytroopa(world),
        MadMallet(world),
        Shaman(world),
        Crook(world),
        Goomba(world),
        PiranhaPlant(world),
        Amanita(world),
        Goby(world),
        Bloober(world),
        BandanaRed(world),
        Lakitu(world),
        Birdy(world),
        Pinwheel(world),
        Ratfunk(world),
        K9(world),
        Magmite(world),
        TheBigBoo(world),
        DryBones(world),
        Greaper(world),
        Sparky(world),
        Chomp(world),
        Pandorite(world),
        ShyRanger(world),
        Bobomb(world),
        Spookum(world),
        HammerBro(world),
        Buzzer(world),
        Ameboid(world),
        Gecko(world),
        Wiggler(world),
        Crusty(world),
        Magikoopa(world),
        Leuko(world),
        Jawful(world),
        Enigma(world),
        Blaster(world),
        Guerrilla(world),
        Babayaga(world),
        Hobgoblin(world),
        Reacher(world),
        Shogun(world),
        Orbuser(world),
        HeavyTroopa(world),
        Shadow(world),
        Cluster(world),
        Bahamutt(world),
        Octolot(world),
        Frogog(world),
        Clerk(world),
        Gunyolk(world),
        Boomer(world),
        Remocon(world),
        Snapdragon(world),
        Stumpet(world),
        Dodo(world),
        Jester(world),
        Artichoker(world),
        Arachne(world),
        Carriboscis(world),
        Hippopo(world),
        Mastadoom(world),
        Corkpedite(world),
        Terracotta(world),
        Spikester(world),
        Malakoopa(world),
        Pounder(world),
        Poundette(world),
        Sackit(world),
        GuGoomba(world),
        Chewy(world),
        Fireball(world),
        MrKipper(world),
        FactoryChief(world),
        BandanaBlue(world),
        Manager(world),
        Bluebird(world),
        AlleyRat(world),
        Chow(world),
        Magmus(world),
        LilBoo(world),
        Vomer(world),
        GlumReaper(world),
        Pyrosphere(world),
        ChompChomp(world),
        Hidon(world),
        SlingShy(world),
        Robomb(world),
        ShyGuy(world),
        Ninja(world),
        Stinger(world),
        Goombette(world),
        Geckit(world),
        Jabit(world),
        Starcruster(world),
        Merlin(world),
        Muckle(world),
        Forkies(world),
        Gorgon(world),
        BigBertha(world),
        ChainedKong(world),
        Fautso(world),
        Strawhead(world),
        Juju(world),
        ArmoredAnt(world),
        Orbison(world),
        TuboTroopa(world),
        Doppel(world),
        Pulsar(world),
        Octovader(world),
        Ribbite(world),
        Director(world),
        Puppox(world),
        FinkFlower(world),
        Lumbler(world),
        Springer(world),
        Harlequin(world),
        Kriffid(world),
        Spinthra(world),
        Radish(world),
        Crippo(world),
        MastaBlasta(world),
        Piledriver(world),
        Apprentice(world),
        BoxBoy(world),
        Shelly(world),
        Superspike(world),
        DodoSolo(world),
        Oerlikon(world),
        Chester(world),
        CorkpediteBody(world),
        Torte(world),
        Shyaway(world),
        JinxClone(world),
        MachineMadeShyster(world),
        MachineMadeDrillBit(world),
        Formless(world),
        Mokura(world),
        FireCrystal(world),
        WaterCrystal(world),
        EarthCrystal(world),
        WindCrystal(world),
        MarioClone(world),
        PeachClone(world),
        BowserClone(world),
        GenoClone(world),
        MallowClone(world),
        Shyster(world),
        Kinklink(world),
        HanginShy(world),
        Smelter(world),
        MachineMadeMack(world),
        MachineMadeBowyer(world),
        MachineMadeYaridovich(world),
        MachineMadeAxemPink(world),
        MachineMadeAxemBlack(world),
        MachineMadeAxemRed(world),
        MachineMadeAxemYellow(world),
        MachineMadeAxemGreen(world),
        Starslap(world),
        Mukumuku(world),
        Zeostar(world),
        Jagger(world),
        Chompweed(world),
        Smithy2TankHead(world),
        Smithy2SafeHead(world),
        Microbomb(world),
        Grit(world),
        Neosquid(world),
        YaridovichMirage(world),
        Helio(world),
        RightEye(world),
        LeftEye(world),
        KnifeGuy(world),
        GrateGuy(world),
        Bundt(world),
        Jinx1(world),
        Jinx2(world),
        CountDown(world),
        DingALing(world),
        Belome1(world),
        Belome2(world),
        Smilax(world),
        Thrax(world),
        Megasmilax(world),
        Birdo(world),
        Eggbert(world),
        AxemYellow(world),
        Punchinello(world),
        TentaclesRight(world),
        AxemRed(world),
        AxemGreen(world),
        KingBomb(world),
        MezzoBomb(world),
        Raspberry(world),
        KingCalamari(world),
        TentaclesLeft(world),
        Jinx3(world),
        Zombone(world),
        CzarDragon(world),
        Cloaker(world),
        Domino(world),
        MadAdder(world),
        Mack(world),
        Bodyguard(world),
        Yaridovich(world),
        DrillBit(world),
        AxemPink(world),
        AxemBlack(world),
        Bowyer(world),
        Aero(world),
        Exor(world),
        Smithy1(world),
        Shyper(world),
        Smithy2Body(world),
        Smithy2Head(world),
        Smithy2MageHead(world),
        Smithy2ChestHead(world),
        Croco1(world),
        Croco2(world),
        Earthlink(world),
        Bowser(world),
        AxemRangers(world),
        Booster(world),
        Booster2(world),
        Snifit(world),
        Johnny(world),
        JohnnySolo(world),
        Valentina(world),
        Cloaker2(world),
        Domino2(world),
        Candle(world),
        Culex(world),
    ]
