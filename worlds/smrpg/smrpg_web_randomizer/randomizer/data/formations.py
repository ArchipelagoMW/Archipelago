# Data module for enemy formation data.

from ...randomizer.logic import utils
from ...randomizer.logic.patch import Patch
from . import enemies
from .bosses import Battlefields


class FormationMember:
    """Class representing a single enemy in a formation with metadata."""

    def __init__(self, index, hidden_at_start, enemy, x_pos, y_pos):
        """
        :type index: int
        :type hidden_at_start: bool
        :type enemy: randomizer.data.enemies.Enemy
        :type x_pos: int
        :type y_pos: int
        """
        self.index = index
        self.hidden_at_start = hidden_at_start
        self.enemy = enemy
        self.x_pos = x_pos
        self.y_pos = y_pos


class EnemyFormation:
    """Class representing an enemy formation for a battle."""
    BASE_ADDRESS = 0x39C000
    BASE_META_ADDRESS = 0x392AAA

    # Valid x,y coordinates for enemies in formations based on vanilla data.
    VALID_COORDINATES = (
        (119, 111),
        (119, 119),
        (119, 127),
        (135, 103),
        (135, 111),
        (135, 119),
        (135, 127),
        (151, 103),
        (151, 111),
        (151, 119),
        (151, 127),
        (151, 135),
        (151, 143),
        (167, 103),
        (167, 111),
        (167, 119),
        (167, 127),
        (167, 135),
        (167, 143),
        (167, 151),
        (183, 103),
        (183, 111),
        (183, 119),
        (183, 127),
        (183, 135),
        (183, 143),
        (183, 151),
        (183, 159),
        (199, 119),
        (199, 135),
        (199, 143),
        (199, 151),
        (199, 159),
        (215, 111),
        (215, 119),
        (215, 127),
        (215, 135),
        (215, 143),
        (215, 151),
        (215, 159),
        (231, 127),
        (231, 135),
        (231, 143),
        (231, 151),
        (231, 159),
    )

    # TODO: Don't need this if we're not mutating coordinates???
    # Upper and lower bounds on the valid coordinates for mutating.
    # LOWER_X = min(c[0] for c in VALID_COORDINATES)
    # UPPER_X = max(c[0] for c in VALID_COORDINATES)
    # LOWER_Y = min(c[1] for c in VALID_COORDINATES)
    # UPPER_Y = max(c[1] for c in VALID_COORDINATES)

    def __init__(self, index, event_at_start, music_run_flags, members, required_battlefield=None,
                 stat_total_enemies=None, stat_scaling_enemies=None):
        """
        Args:
            index (int):
            event_at_start (int|None):
            music_run_flags (int):
            members (list[FormationMember]):
            required_battlefield (int):
            stat_total_enemies (list[randomizer.data.enemies.Enemy|type]): List of enemies needed for stat totals during
                boss shuffle, if this is different than the actual member list in data.  If None, the main member list
                is used.
            stat_scaling_enemies (list[randomizer.data.enemies.Enemy|type]): List of enemies that need to have their
                stats re-scaled during boss shuffle, if this is different than the actual member list in data.  If None,
                the main member list is used with any duplicates removed.
        """
        self.index = index
        self.event_at_start = event_at_start
        self.members = members
        self.leaders = set()
        self.required_battlefield = required_battlefield

        # Check if boss shuffle members are different than regular members.  Otherwise, use main member list.
        if stat_total_enemies is not None:
            self.stat_total_enemies = stat_total_enemies
        else:
            self.stat_total_enemies = [m.enemy for m in self.members]

        # Check if enemies to re-scale are different than the regular members.  Otherwise, use main member list.
        # If we're using the main member list, make sure the order stays the same!
        if stat_scaling_enemies is not None:
            self.stat_scaling_enemies = stat_scaling_enemies
        else:
            self.stat_scaling_enemies = []
            for member in self.members:
                if member.enemy not in self.stat_scaling_enemies:
                    self.stat_scaling_enemies.append(member.enemy)

        # Parse out can't run and music flags.
        self.can_run_away = not bool(music_run_flags & 0x02)
        self.music = music_run_flags & 0xfd

    @property
    def enemies(self):
        return [m.enemy for m in self.members]

    @property
    def bosses(self):
        return [m.enemy for m in self.members if m.enemy.boss]

    @property
    def hidden_enemies(self):
        return [m.enemy for m in self.members if m.hidden_at_start]

    # TODO: Don't need this if we're not mutating coordinates???
    # def mutate_coordinate(self, x, y):
    #     x = utils.mutate_normal(x, minimum=self.LOWER_X, maximum=self.UPPER_X)
    #     y = utils.mutate_normal(y, minimum=self.LOWER_Y, maximum=self.UPPER_Y)
    #     return x, y

    # ********** Properties for getting stat totals for boss shuffle.

    @property
    def shuffle_anchor(self):
        """Get enemy that is the anchor for this formation for boss shuffle.

        Returns:
            randomizer.data.enemies.Enemy: Enemy that is the anchor, None if there is no anchor.

        """
        anchor = [e for e in self.stat_total_enemies if e.anchor]
        if anchor:
            return anchor[0]
        return None

    # ********** Patch stuff.

    def get_patch(self):
        """Get patch for this formation.

        :return: Patch data.
        :rtype: randomizer.logic.patch.Patch
        """
        patch = Patch()

        data = bytearray()

        # Monsters present bitmap.
        monsters_present = [7 - m.index for m in self.members]
        data += utils.BitMapSet(1, monsters_present).as_bytes()

        # Monsters hidden bitmap.
        monsters_hidden = [7 - m.index for m in self.members if m.hidden_at_start]
        data += utils.BitMapSet(1, monsters_hidden).as_bytes()

        # Monster data.
        for member in self.members:
            data += utils.ByteField(member.enemy.index).as_bytes()
            data += utils.ByteField(member.x_pos).as_bytes()
            data += utils.ByteField(member.y_pos).as_bytes()

        base_addr = self.BASE_ADDRESS + (self.index * 26)
        patch.add_data(base_addr, data)

        # Add formation metadata.
        data = bytearray()
        data += utils.ByteField(self.event_at_start if self.event_at_start is not None else 0xff).as_bytes()
        music_run_flags = self.music
        if not self.can_run_away:
            music_run_flags |= 0x03
        data += utils.ByteField(music_run_flags).as_bytes()

        base_addr = self.BASE_META_ADDRESS + self.index * 3 + 1
        patch.add_data(base_addr, data)

        return patch


class FormationPack:
    """Class representing a pack of enemy formations.  For each encounter, the game chooses a random formation of
    enemies from the pack being encountered.  For bosses, all the formations are just the same.
    """
    BASE_ADDRESS = 0x39222A

    def __init__(self, index, formations):
        """
        :type index: int
        :type formations: list[EnemyFormation]
        """
        self.index = index
        self.formations = formations

    @property
    def common_enemies(self):
        """Common enemies between all formations in this pack.

        :rtype: list[Enemy]
        """
        common_enemies = set(m.enemy for m in self.formations[0].members)
        for f in self.formations[1:]:
            common_enemies &= set(m.enemy for m in f.members)
        return sorted(common_enemies, key=lambda e: e.index)

    def get_patch(self):
        """Get patch for this formation pack.

        :return: Patch data.
        :rtype: randomizer.logic.patch.Patch
        """
        patch = Patch()

        data = bytearray()

        hi_num = False
        for formation in self.formations:
            val = formation.index

            # For formations > 255, set the high bank indicator since each formation is a single byte only.
            if val > 255:
                hi_num = True
                val -= 255

            data += utils.ByteField(val).as_bytes()

        # High bank indicator.
        val = 7 if hi_num else 0
        data += utils.ByteField(val).as_bytes()

        base_addr = self.BASE_ADDRESS + (self.index * 4)
        patch.add_data(base_addr, data)

        return patch


# ************************************* Default lists for the world.

def get_default_enemy_formations(world):
    """Get the default enemy formations and formation packs for the world.

    Args:
        world (randomizer.logic.main.GameWorld):

    Returns:
        tuple[list[EnemyFormation]|list[FormationPack]]: Two tuple of default lists of formations and packs for world.

    """
    # Vanilla enemy formation data.
    formations = [
        EnemyFormation(4, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Spikey), 135, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Spikey), 199, 143),
        ]),
        EnemyFormation(5, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Spikey), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Skytroopa), 199, 151),
        ]),
        EnemyFormation(6, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Spikey), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Spikey), 199, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.Frogog), 199, 119),
        ]),
        EnemyFormation(7, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Spikey), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Spikey), 199, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.Spikey), 199, 151),
        ]),
        EnemyFormation(8, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Skytroopa), 167, 135),
        ]),
        EnemyFormation(9, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Skytroopa), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Skytroopa), 199, 151),
        ]),
        EnemyFormation(10, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Skytroopa), 199, 151),
            FormationMember(1, False, world.get_enemy_instance(enemies.Skytroopa), 135, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.Frogog), 183, 127),
        ]),
        EnemyFormation(11, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Skytroopa), 167, 103),
            FormationMember(1, False, world.get_enemy_instance(enemies.Skytroopa), 231, 135),
            FormationMember(3, False, world.get_enemy_instance(enemies.Goomba), 167, 135),
        ]),
        EnemyFormation(12, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Goomba), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Goomba), 215, 135),
        ]),
        EnemyFormation(13, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Goomba), 167, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.Goomba), 167, 135),
            FormationMember(2, False, world.get_enemy_instance(enemies.Goomba), 215, 135),
        ]),
        EnemyFormation(14, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Goomba), 167, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.Goomba), 215, 135),
            FormationMember(2, False, world.get_enemy_instance(enemies.Spikey), 167, 135),
        ]),
        EnemyFormation(15, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Goomba), 167, 135),
            FormationMember(1, False, world.get_enemy_instance(enemies.Frogog), 167, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.Spikey), 215, 135),
        ]),
        EnemyFormation(16, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.K9), 167, 135),
        ]),
        EnemyFormation(17, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.K9), 199, 159),
            FormationMember(1, False, world.get_enemy_instance(enemies.K9), 151, 119),
        ]),
        EnemyFormation(18, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.K9), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.K9), 199, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.Spikey), 199, 119),
        ]),
        EnemyFormation(19, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.K9), 183, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Frogog), 215, 143),
            FormationMember(2, False, world.get_enemy_instance(enemies.Frogog), 151, 111),
        ]),
        EnemyFormation(20, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Shyster), 183, 127),
        ]),
        EnemyFormation(21, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Shyster), 167, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Shyster), 199, 135),
        ]),
        EnemyFormation(22, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Shyster), 151, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.Shyster), 215, 143),
            FormationMember(2, False, world.get_enemy_instance(enemies.Shyster), 167, 135),
        ]),
        EnemyFormation(23, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Shyster), 151, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Shyster), 199, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.Shyster), 167, 103),
            FormationMember(3, False, world.get_enemy_instance(enemies.Shyster), 215, 127),
        ]),
        EnemyFormation(24, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Ratfunk), 199, 143),
            FormationMember(1, False, world.get_enemy_instance(enemies.Ratfunk), 151, 111),
        ]),
        EnemyFormation(25, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Ratfunk), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Ratfunk), 199, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.Shadow), 199, 119),
        ]),
        EnemyFormation(26, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Ratfunk), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Ratfunk), 199, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.Hobgoblin), 199, 119),
        ]),
        EnemyFormation(27, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Ratfunk), 167, 135),
            FormationMember(2, False, world.get_enemy_instance(enemies.Hobgoblin), 167, 103),
            FormationMember(3, False, world.get_enemy_instance(enemies.Hobgoblin), 231, 135),
        ]),
        EnemyFormation(28, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.TheBigBoo), 167, 135),
        ]),
        EnemyFormation(29, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.TheBigBoo), 151, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Shadow), 199, 143),
        ]),
        EnemyFormation(30, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.TheBigBoo), 119, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Shadow), 167, 135),
            FormationMember(2, False, world.get_enemy_instance(enemies.Hobgoblin), 215, 143),
        ]),
        EnemyFormation(31, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.TheBigBoo), 231, 135),
            FormationMember(1, False, world.get_enemy_instance(enemies.TheBigBoo), 151, 143),
            FormationMember(2, False, world.get_enemy_instance(enemies.TheBigBoo), 167, 103),
            FormationMember(3, False, world.get_enemy_instance(enemies.Shadow), 183, 127),
        ]),
        EnemyFormation(32, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Goby), 167, 135),
        ]),
        EnemyFormation(33, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Goby), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Goby), 199, 151),
        ]),
        EnemyFormation(34, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Goby), 151, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Goby), 215, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.Goby), 183, 151),
        ]),
        EnemyFormation(35, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Goby), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Goby), 215, 127),
            FormationMember(2, False, world.get_enemy_instance(enemies.Goby), 167, 135),
            FormationMember(3, False, world.get_enemy_instance(enemies.Goby), 183, 111),
            FormationMember(4, False, world.get_enemy_instance(enemies.Goby), 199, 151),
        ]),
        EnemyFormation(36, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Crook), 167, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.Crook), 199, 151),
        ]),
        EnemyFormation(37, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Crook), 199, 143),
            FormationMember(1, False, world.get_enemy_instance(enemies.Crook), 151, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.ShyGuy), 199, 119),
        ]),
        EnemyFormation(38, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Crook), 183, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Snapdragon), 151, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.Snapdragon), 215, 143),
        ]),
        EnemyFormation(39, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Crook), 199, 159),
            FormationMember(3, False, world.get_enemy_instance(enemies.Starslap), 215, 127),
            FormationMember(4, False, world.get_enemy_instance(enemies.Arachne), 167, 103),
        ]),
        EnemyFormation(40, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.ShyGuy), 167, 135),
        ]),
        EnemyFormation(41, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.ShyGuy), 151, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.Starslap), 199, 151),
        ]),
        EnemyFormation(42, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.ShyGuy), 135, 103),
            FormationMember(1, False, world.get_enemy_instance(enemies.ShyGuy), 215, 143),
            FormationMember(3, False, world.get_enemy_instance(enemies.Snapdragon), 183, 127),
        ]),
        EnemyFormation(43, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.ShyGuy), 231, 135),
            FormationMember(2, False, world.get_enemy_instance(enemies.Crook), 199, 143),
            FormationMember(3, False, world.get_enemy_instance(enemies.Arachne), 151, 111),
        ]),
        EnemyFormation(44, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Starslap), 199, 159),
            FormationMember(1, False, world.get_enemy_instance(enemies.ShyGuy), 151, 111),
        ]),
        EnemyFormation(45, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Starslap), 215, 151),
            FormationMember(1, False, world.get_enemy_instance(enemies.Arachne), 151, 111),
        ]),
        EnemyFormation(46, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Starslap), 167, 135),
            FormationMember(1, False, world.get_enemy_instance(enemies.Snapdragon), 151, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.Snapdragon), 215, 143),
        ]),
        EnemyFormation(47, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Starslap), 199, 151),
            FormationMember(1, False, world.get_enemy_instance(enemies.Starslap), 167, 103),
            FormationMember(2, False, world.get_enemy_instance(enemies.Starslap), 231, 135),
            FormationMember(3, False, world.get_enemy_instance(enemies.Starslap), 135, 119),
        ]),
        EnemyFormation(48, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Wiggler), 183, 127),
        ]),
        EnemyFormation(49, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Wiggler), 151, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.Amanita), 199, 151),
        ]),
        EnemyFormation(50, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Wiggler), 151, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.Wiggler), 215, 143),
        ]),
        EnemyFormation(51, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Wiggler), 151, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.Guerrilla), 215, 143),
        ]),
        EnemyFormation(52, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Amanita), 135, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Amanita), 199, 143),
        ]),
        EnemyFormation(53, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Amanita), 199, 151),
            FormationMember(1, False, world.get_enemy_instance(enemies.Amanita), 135, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.Buzzer), 199, 119),
        ]),
        EnemyFormation(54, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Amanita), 199, 151),
            FormationMember(1, False, world.get_enemy_instance(enemies.Amanita), 135, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.Octolot), 183, 127),
        ]),
        EnemyFormation(55, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Amanita), 151, 127),
            FormationMember(2, False, world.get_enemy_instance(enemies.Guerrilla), 215, 143),
            FormationMember(3, False, world.get_enemy_instance(enemies.Buzzer), 183, 111),
        ]),
        EnemyFormation(56, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Buzzer), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Octolot), 199, 143),
        ]),
        EnemyFormation(57, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Buzzer), 167, 103),
            FormationMember(1, False, world.get_enemy_instance(enemies.Buzzer), 231, 135),
            FormationMember(2, False, world.get_enemy_instance(enemies.Amanita), 167, 135),
        ]),
        EnemyFormation(58, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Buzzer), 199, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.Guerrilla), 151, 119),
        ]),
        EnemyFormation(59, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Buzzer), 199, 159),
            FormationMember(2, False, world.get_enemy_instance(enemies.Guerrilla), 135, 119),
        ]),
        EnemyFormation(60, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Sparky), 183, 127),
        ]),
        EnemyFormation(61, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Sparky), 167, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.Sparky), 215, 135),
            FormationMember(2, False, world.get_enemy_instance(enemies.ShyRanger), 167, 135),
        ]),
        EnemyFormation(62, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Sparky), 167, 135),
            FormationMember(1, False, world.get_enemy_instance(enemies.Sparky), 151, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.Sparky), 215, 143),
        ]),
        EnemyFormation(63, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Sparky), 151, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Sparky), 183, 143),
            FormationMember(2, False, world.get_enemy_instance(enemies.Sparky), 231, 135),
            FormationMember(3, False, world.get_enemy_instance(enemies.Sparky), 167, 103),
        ]),
        EnemyFormation(64, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Goomba), 183, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.ShyRanger), 135, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.ShyRanger), 167, 103),
            FormationMember(3, False, world.get_enemy_instance(enemies.ShyRanger), 199, 151),
            FormationMember(4, False, world.get_enemy_instance(enemies.ShyRanger), 231, 135),
        ]),
        EnemyFormation(65, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Goomba), 199, 151),
            FormationMember(1, False, world.get_enemy_instance(enemies.Goomba), 135, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.ShyRanger), 183, 111),
            FormationMember(3, False, world.get_enemy_instance(enemies.ShyRanger), 215, 127),
        ]),
        EnemyFormation(66, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Goomba), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Goomba), 199, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.PiranhaPlant), 199, 119),
            FormationMember(3, False, world.get_enemy_instance(enemies.PiranhaPlant), 167, 135),
        ]),
        EnemyFormation(67, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Goomba), 167, 135),
            FormationMember(2, False, world.get_enemy_instance(enemies.PiranhaPlant), 231, 151),
            FormationMember(3, False, world.get_enemy_instance(enemies.PiranhaPlant), 135, 103),
            FormationMember(4, False, world.get_enemy_instance(enemies.Sparky), 199, 119),
        ]),
        EnemyFormation(68, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.PiranhaPlant), 167, 135),
        ]),
        EnemyFormation(69, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.PiranhaPlant), 215, 143),
            FormationMember(1, False, world.get_enemy_instance(enemies.PiranhaPlant), 151, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.ShyRanger), 183, 127),
        ]),
        EnemyFormation(70, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.PiranhaPlant), 167, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.PiranhaPlant), 167, 135),
            FormationMember(2, False, world.get_enemy_instance(enemies.PiranhaPlant), 215, 135),
        ]),
        EnemyFormation(71, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.PiranhaPlant), 151, 143),
            FormationMember(1, False, world.get_enemy_instance(enemies.PiranhaPlant), 151, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.PiranhaPlant), 199, 119),
            FormationMember(3, False, world.get_enemy_instance(enemies.PiranhaPlant), 231, 143),
            FormationMember(4, False, world.get_enemy_instance(enemies.PiranhaPlant), 199, 159),
        ]),
        # Change Bobomb enemies in the normal formations to Robombs so we can boss shuffle Punchinello.
        EnemyFormation(72, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Robomb), 183, 127),
        ]),
        EnemyFormation(73, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Robomb), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Robomb), 199, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.Cluster), 199, 119),
        ]),
        EnemyFormation(74, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Robomb), 151, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Robomb), 167, 103),
            FormationMember(2, False, world.get_enemy_instance(enemies.Robomb), 199, 151),
            FormationMember(3, False, world.get_enemy_instance(enemies.Robomb), 215, 127),
        ]),
        EnemyFormation(75, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Robomb), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Robomb), 199, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.Enigma), 183, 111),
            FormationMember(3, False, world.get_enemy_instance(enemies.Cluster), 215, 127),
        ]),
        EnemyFormation(76, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Sparky), 199, 151),
            FormationMember(1, False, world.get_enemy_instance(enemies.Enigma), 167, 111),
        ]),
        EnemyFormation(77, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Sparky), 167, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.Sparky), 215, 135),
            FormationMember(2, False, world.get_enemy_instance(enemies.Robomb), 167, 135),
        ]),
        EnemyFormation(78, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Sparky), 183, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Cluster), 231, 143),
            FormationMember(2, False, world.get_enemy_instance(enemies.Cluster), 151, 103),
        ]),
        EnemyFormation(79, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Sparky), 183, 143),
            FormationMember(1, False, world.get_enemy_instance(enemies.Sparky), 151, 127),
            FormationMember(2, False, world.get_enemy_instance(enemies.Enigma), 167, 103),
            FormationMember(3, False, world.get_enemy_instance(enemies.Enigma), 231, 135),
        ]),
        EnemyFormation(80, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Magmite), 167, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.Magmite), 199, 151),
        ]),
        EnemyFormation(81, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Magmite), 151, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.Robomb), 183, 127),
            FormationMember(2, False, world.get_enemy_instance(enemies.Sparky), 215, 143),
        ]),
        EnemyFormation(82, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Magmite), 151, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Magmite), 183, 143),
            FormationMember(2, False, world.get_enemy_instance(enemies.Cluster), 167, 103),
            FormationMember(3, False, world.get_enemy_instance(enemies.Cluster), 231, 135),
        ]),
        EnemyFormation(83, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Magmite), 135, 103),
            FormationMember(1, False, world.get_enemy_instance(enemies.Magmite), 231, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.Robomb), 167, 135),
            FormationMember(4, False, world.get_enemy_instance(enemies.Cluster), 199, 119),
        ]),
        EnemyFormation(84, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Lakitu), 183, 127),
        ]),
        EnemyFormation(85, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Lakitu), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Spikester), 199, 159),
            FormationMember(2, False, world.get_enemy_instance(enemies.Artichoker), 183, 119),
        ]),
        EnemyFormation(86, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Lakitu), 151, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.Lakitu), 183, 127),
            FormationMember(2, False, world.get_enemy_instance(enemies.Lakitu), 215, 143),
        ]),
        EnemyFormation(87, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Lakitu), 231, 151),
            FormationMember(1, False, world.get_enemy_instance(enemies.Lakitu), 135, 103),
            FormationMember(3, False, world.get_enemy_instance(enemies.Artichoker), 183, 127),
        ]),
        EnemyFormation(88, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Spikester), 215, 143),
            FormationMember(1, False, world.get_enemy_instance(enemies.Carriboscis), 135, 119),
        ]),
        EnemyFormation(89, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Spikester), 199, 151),
            FormationMember(1, False, world.get_enemy_instance(enemies.Spikester), 135, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.Artichoker), 199, 119),
        ]),
        EnemyFormation(90, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Spikester), 183, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Carriboscis), 135, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.Carriboscis), 199, 151),
        ]),
        EnemyFormation(91, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Spikester), 119, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.Spikester), 215, 159),
            FormationMember(2, False, world.get_enemy_instance(enemies.Spikester), 215, 135),
            FormationMember(3, False, world.get_enemy_instance(enemies.Spikester), 167, 111),
            FormationMember(4, False, world.get_enemy_instance(enemies.Carriboscis), 151, 143),
        ]),
        EnemyFormation(92, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Spookum), 199, 135),
            FormationMember(1, False, world.get_enemy_instance(enemies.Orbuser), 135, 119),
        ]),
        EnemyFormation(93, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Spookum), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Spookum), 199, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.Jester), 199, 119),
        ]),
        EnemyFormation(94, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Spookum), 151, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.Remocon), 167, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.Orbuser), 215, 127),
        ]),
        EnemyFormation(95, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Spookum), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Spookum), 199, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.Remocon), 199, 119),
        ]),
        EnemyFormation(96, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Robomb), 183, 127),
        ]),
        EnemyFormation(97, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Robomb), 183, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Robomb), 199, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.Robomb), 167, 135),
        ]),
        EnemyFormation(98, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Robomb), 215, 143),
            FormationMember(1, False, world.get_enemy_instance(enemies.Robomb), 151, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.Remocon), 183, 127),
        ]),
        EnemyFormation(99, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Robomb), 135, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Robomb), 231, 127),
            FormationMember(2, False, world.get_enemy_instance(enemies.Robomb), 183, 103),
            FormationMember(3, False, world.get_enemy_instance(enemies.Robomb), 183, 151),
            FormationMember(4, False, world.get_enemy_instance(enemies.Orbuser), 183, 127),
        ]),
        EnemyFormation(100, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Chomp), 215, 143),
            FormationMember(1, False, world.get_enemy_instance(enemies.Jester), 167, 111),
        ]),
        EnemyFormation(101, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Chomp), 215, 143),
            FormationMember(1, False, world.get_enemy_instance(enemies.Robomb), 151, 135),
            FormationMember(2, False, world.get_enemy_instance(enemies.Remocon), 167, 103),
        ]),
        EnemyFormation(102, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Chomp), 151, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.Chomp), 215, 143),
            FormationMember(2, False, world.get_enemy_instance(enemies.Orbuser), 183, 127),
        ]),
        EnemyFormation(103, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Chomp), 199, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.Jester), 135, 103),
            FormationMember(3, False, world.get_enemy_instance(enemies.Jester), 231, 151),
        ]),
        EnemyFormation(104, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Blaster), 167, 135),
            FormationMember(1, False, world.get_enemy_instance(enemies.Spookum), 199, 119),
        ]),
        EnemyFormation(105, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Blaster), 167, 135),
            FormationMember(1, False, world.get_enemy_instance(enemies.Spookum), 151, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.Remocon), 215, 143),
        ]),
        EnemyFormation(106, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Blaster), 199, 151),
            FormationMember(1, False, world.get_enemy_instance(enemies.Blaster), 135, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.Spookum), 199, 119),
        ]),
        EnemyFormation(107, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Blaster), 199, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Robomb), 135, 103),
            FormationMember(2, False, world.get_enemy_instance(enemies.Robomb), 231, 151),
            FormationMember(3, False, world.get_enemy_instance(enemies.Spookum), 151, 127),
            FormationMember(4, False, world.get_enemy_instance(enemies.Spookum), 183, 143),
        ]),
        EnemyFormation(108, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Torte), 183, 127),
        ]),
        EnemyFormation(109, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Torte), 215, 143),
            FormationMember(1, False, world.get_enemy_instance(enemies.Torte), 151, 111),
        ]),
        EnemyFormation(110, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Torte), 183, 103),
            FormationMember(1, False, world.get_enemy_instance(enemies.Torte), 151, 135),
            FormationMember(2, False, world.get_enemy_instance(enemies.Torte), 215, 135),
        ]),
        EnemyFormation(111, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Torte), 167, 135),
            FormationMember(1, False, world.get_enemy_instance(enemies.Torte), 199, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.Torte), 151, 111),
            FormationMember(3, False, world.get_enemy_instance(enemies.Torte), 215, 143),
        ]),
        EnemyFormation(112, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Mukumuku), 183, 127),
        ]),
        EnemyFormation(113, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Mukumuku), 151, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Mukumuku), 215, 135),
        ]),
        EnemyFormation(114, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Mukumuku), 151, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.Mukumuku), 215, 143),
            FormationMember(2, False, world.get_enemy_instance(enemies.Pulsar), 167, 135),
        ]),
        EnemyFormation(115, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Mukumuku), 183, 143),
            FormationMember(1, False, world.get_enemy_instance(enemies.Pulsar), 151, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.Gecko), 231, 143),
        ]),
        EnemyFormation(116, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Sackit), 199, 151),
            FormationMember(1, False, world.get_enemy_instance(enemies.Sackit), 167, 111),
        ]),
        EnemyFormation(117, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Sackit), 151, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Sackit), 183, 143),
            FormationMember(2, False, world.get_enemy_instance(enemies.Mukumuku), 167, 103),
            FormationMember(3, False, world.get_enemy_instance(enemies.Gecko), 231, 135),
        ]),
        EnemyFormation(118, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Sackit), 167, 135),
            FormationMember(3, False, world.get_enemy_instance(enemies.Pulsar), 167, 103),
            FormationMember(4, False, world.get_enemy_instance(enemies.Pulsar), 231, 135),
        ]),
        EnemyFormation(119, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Sackit), 215, 143),
            FormationMember(1, False, world.get_enemy_instance(enemies.Mastadoom), 167, 103),
        ]),
        EnemyFormation(120, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Gecko), 151, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Sackit), 199, 143),
        ]),
        EnemyFormation(121, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Gecko), 151, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Mastadoom), 215, 135),
        ]),
        EnemyFormation(122, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Gecko), 183, 143),
            FormationMember(1, False, world.get_enemy_instance(enemies.Gecko), 151, 127),
            FormationMember(2, False, world.get_enemy_instance(enemies.Mukumuku), 135, 103),
            FormationMember(3, False, world.get_enemy_instance(enemies.Mukumuku), 231, 151),
            FormationMember(4, False, world.get_enemy_instance(enemies.Sackit), 183, 111),
            FormationMember(5, False, world.get_enemy_instance(enemies.Sackit), 215, 127),
        ]),
        EnemyFormation(123, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Gecko), 135, 103),
            FormationMember(1, False, world.get_enemy_instance(enemies.Gecko), 231, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.Mastadoom), 199, 119),
        ]),
        EnemyFormation(124, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Zeostar), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Zeostar), 215, 135),
        ]),
        EnemyFormation(125, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Zeostar), 151, 135),
            FormationMember(1, False, world.get_enemy_instance(enemies.Zeostar), 183, 103),
            FormationMember(2, False, world.get_enemy_instance(enemies.Bloober), 215, 135),
        ]),
        EnemyFormation(126, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Zeostar), 199, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Zeostar), 167, 135),
            FormationMember(2, False, world.get_enemy_instance(enemies.Leuko), 167, 103),
            FormationMember(3, False, world.get_enemy_instance(enemies.Leuko), 231, 135),
        ]),
        EnemyFormation(127, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Zeostar), 183, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Leuko), 215, 143),
            FormationMember(2, False, world.get_enemy_instance(enemies.Crusty), 151, 111),
        ]),
        EnemyFormation(128, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Bloober), 151, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.MrKipper), 215, 143),
        ]),
        EnemyFormation(129, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Bloober), 183, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Bloober), 231, 143),
            FormationMember(2, False, world.get_enemy_instance(enemies.Bloober), 135, 111),
        ]),
        EnemyFormation(130, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Bloober), 151, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.Bloober), 231, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.MrKipper), 151, 143),
            FormationMember(3, False, world.get_enemy_instance(enemies.Crusty), 199, 119),
        ]),
        EnemyFormation(131, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Bloober), 231, 135),
            FormationMember(1, False, world.get_enemy_instance(enemies.Bloober), 167, 103),
            FormationMember(2, False, world.get_enemy_instance(enemies.Zeostar), 135, 127),
            FormationMember(3, False, world.get_enemy_instance(enemies.Zeostar), 183, 151),
            FormationMember(4, False, world.get_enemy_instance(enemies.Leuko), 183, 127),
        ]),
        EnemyFormation(132, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.MrKipper), 151, 103),
            FormationMember(1, False, world.get_enemy_instance(enemies.MrKipper), 215, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.MrKipper), 183, 127),
        ]),
        EnemyFormation(133, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.MrKipper), 199, 151),
            FormationMember(1, False, world.get_enemy_instance(enemies.MrKipper), 135, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.Crusty), 199, 119),
        ]),
        EnemyFormation(134, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.MrKipper), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.MrKipper), 231, 135),
            FormationMember(2, False, world.get_enemy_instance(enemies.Crusty), 183, 127),
        ]),
        EnemyFormation(135, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.MrKipper), 215, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.MrKipper), 199, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.MrKipper), 167, 103),
            FormationMember(3, False, world.get_enemy_instance(enemies.MrKipper), 151, 127),
        ]),
        EnemyFormation(136, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.BandanaRed), 151, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.BandanaRed), 183, 143),
            FormationMember(2, False, world.get_enemy_instance(enemies.BandanaRed), 167, 103),
            FormationMember(3, False, world.get_enemy_instance(enemies.BandanaRed), 231, 135),
        ]),
        EnemyFormation(137, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.BandanaRed), 199, 151),
            FormationMember(1, False, world.get_enemy_instance(enemies.BandanaRed), 135, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.BandanaRed), 215, 127),
            FormationMember(3, False, world.get_enemy_instance(enemies.BandanaRed), 167, 135),
            FormationMember(4, False, world.get_enemy_instance(enemies.BandanaRed), 183, 111),
        ]),
        EnemyFormation(138, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.BandanaRed), 135, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.BandanaRed), 183, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.BandanaRed), 167, 111),
            FormationMember(3, False, world.get_enemy_instance(enemies.BandanaRed), 215, 135),
        ]),
        EnemyFormation(139, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.BandanaRed), 199, 151),
            FormationMember(1, False, world.get_enemy_instance(enemies.BandanaRed), 135, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.DryBones), 167, 103),
            FormationMember(3, False, world.get_enemy_instance(enemies.DryBones), 231, 135),
            FormationMember(4, False, world.get_enemy_instance(enemies.Strawhead), 183, 127),
        ]),
        EnemyFormation(140, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.BandanaBlue), 183, 127),
        ]),
        EnemyFormation(141, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.BandanaBlue), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.BandanaBlue), 199, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.Greaper), 183, 127),
        ]),
        EnemyFormation(142, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.BandanaBlue), 135, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.BandanaBlue), 167, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.BandanaBlue), 183, 151),
            FormationMember(3, False, world.get_enemy_instance(enemies.BandanaBlue), 215, 135),
        ]),
        EnemyFormation(143, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.BandanaBlue), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.BandanaBlue), 199, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.Greaper), 167, 103),
            FormationMember(3, False, world.get_enemy_instance(enemies.Greaper), 231, 135),
            FormationMember(4, False, world.get_enemy_instance(enemies.Strawhead), 183, 127),
        ]),
        EnemyFormation(144, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.DryBones), 199, 151),
            FormationMember(1, False, world.get_enemy_instance(enemies.DryBones), 151, 111),
        ]),
        EnemyFormation(145, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.DryBones), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.DryBones), 199, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.Greaper), 199, 119),
        ]),
        EnemyFormation(146, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.DryBones), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Greaper), 199, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.Reacher), 199, 119),
        ]),
        EnemyFormation(147, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.DryBones), 167, 103),
            FormationMember(1, False, world.get_enemy_instance(enemies.DryBones), 231, 135),
            FormationMember(2, False, world.get_enemy_instance(enemies.Greaper), 151, 127),
            FormationMember(3, False, world.get_enemy_instance(enemies.Greaper), 183, 143),
            FormationMember(4, False, world.get_enemy_instance(enemies.Reacher), 199, 119),
        ]),
        EnemyFormation(148, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.AlleyRat), 199, 151),
            FormationMember(1, False, world.get_enemy_instance(enemies.Gorgon), 151, 111),
        ]),
        EnemyFormation(149, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.AlleyRat), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.AlleyRat), 199, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.Greaper), 215, 127),
            FormationMember(3, False, world.get_enemy_instance(enemies.Greaper), 183, 111),
        ]),
        EnemyFormation(150, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.AlleyRat), 151, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.AlleyRat), 199, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.Gorgon), 183, 111),
            FormationMember(3, False, world.get_enemy_instance(enemies.Gorgon), 231, 135),
        ]),
        EnemyFormation(151, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.AlleyRat), 231, 135),
            FormationMember(1, False, world.get_enemy_instance(enemies.Reacher), 167, 135),
            FormationMember(2, False, world.get_enemy_instance(enemies.Gorgon), 167, 103),
        ]),
        EnemyFormation(152, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Greaper), 183, 127),
        ]),
        EnemyFormation(153, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Greaper), 151, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Greaper), 199, 143),
            FormationMember(2, False, world.get_enemy_instance(enemies.Reacher), 199, 119),
        ]),
        EnemyFormation(154, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Greaper), 167, 135),
            FormationMember(1, False, world.get_enemy_instance(enemies.Strawhead), 215, 135),
            FormationMember(2, False, world.get_enemy_instance(enemies.Reacher), 167, 111),
        ]),
        EnemyFormation(155, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Greaper), 167, 135),
            FormationMember(1, False, world.get_enemy_instance(enemies.Gorgon), 199, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.Strawhead), 215, 143),
            FormationMember(3, False, world.get_enemy_instance(enemies.Strawhead), 151, 111),
        ]),
        EnemyFormation(156, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.DrillBit), 183, 127),
        ]),
        EnemyFormation(157, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.DrillBit), 167, 135),
            FormationMember(1, False, world.get_enemy_instance(enemies.DrillBit), 199, 119),
        ]),
        EnemyFormation(158, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.DrillBit), 151, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.DrillBit), 183, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.DrillBit), 215, 119),
        ]),
        EnemyFormation(159, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.DrillBit), 167, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.DrillBit), 199, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.DrillBit), 135, 119),
            FormationMember(3, False, world.get_enemy_instance(enemies.DrillBit), 199, 119),
            FormationMember(4, False, world.get_enemy_instance(enemies.DrillBit), 199, 135),
        ]),
        EnemyFormation(160, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Stinger), 151, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.FinkFlower), 199, 143),
        ]),
        EnemyFormation(161, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Stinger), 135, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.Stinger), 215, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.Octovader), 199, 119),
        ]),
        EnemyFormation(162, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Stinger), 199, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.FinkFlower), 215, 143),
            FormationMember(3, False, world.get_enemy_instance(enemies.FinkFlower), 151, 111),
        ]),
        EnemyFormation(163, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Stinger), 183, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.Stinger), 199, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.Stinger), 215, 127),
            FormationMember(3, False, world.get_enemy_instance(enemies.Stinger), 135, 119),
        ]),
        EnemyFormation(164, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Chow), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Octovader), 199, 151),
        ]),
        EnemyFormation(165, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Chow), 151, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.Shogun), 215, 143),
        ]),
        EnemyFormation(166, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Chow), 199, 151),
            FormationMember(1, False, world.get_enemy_instance(enemies.Shogun), 135, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.Octovader), 199, 119),
        ]),
        EnemyFormation(167, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Chow), 167, 135),
            FormationMember(1, False, world.get_enemy_instance(enemies.FinkFlower), 199, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.Shogun), 135, 119),
            FormationMember(3, False, world.get_enemy_instance(enemies.Shogun), 199, 151),
        ]),
        EnemyFormation(168, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.ChompChomp), 183, 127),
        ]),
        EnemyFormation(169, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.ChompChomp), 151, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.ChompChomp), 215, 143),
        ]),
        EnemyFormation(170, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.ChompChomp), 151, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.ChompChomp), 199, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.ChompChomp), 215, 143),
        ]),
        EnemyFormation(171, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.ChompChomp), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.ChompChomp), 183, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.ChompChomp), 215, 127),
            FormationMember(3, False, world.get_enemy_instance(enemies.ChompChomp), 199, 151),
        ]),
        EnemyFormation(172, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Shyaway), 183, 127),
        ]),
        EnemyFormation(173, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Shyaway), 151, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.Shyaway), 215, 143),
            FormationMember(2, False, world.get_enemy_instance(enemies.Kriffid), 183, 127),
        ]),
        EnemyFormation(174, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Shyaway), 167, 103),
            FormationMember(1, False, world.get_enemy_instance(enemies.Shyaway), 231, 135),
            FormationMember(2, False, world.get_enemy_instance(enemies.Ribbite), 183, 127),
        ]),
        EnemyFormation(175, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Shyaway), 215, 135),
            FormationMember(2, False, world.get_enemy_instance(enemies.Geckit), 167, 143),
            FormationMember(4, False, world.get_enemy_instance(enemies.Ribbite), 167, 111),
        ]),
        EnemyFormation(176, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Chewy), 151, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.Chewy), 183, 151),
        ]),
        EnemyFormation(177, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Chewy), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Chewy), 199, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.Shyaway), 199, 119),
        ]),
        EnemyFormation(178, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Chewy), 151, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.Spinthra), 215, 143),
        ]),
        EnemyFormation(179, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Chewy), 183, 151),
            FormationMember(1, False, world.get_enemy_instance(enemies.Chewy), 135, 127),
            FormationMember(2, False, world.get_enemy_instance(enemies.Geckit), 231, 143),
            FormationMember(3, False, world.get_enemy_instance(enemies.Geckit), 151, 103),
            FormationMember(4, False, world.get_enemy_instance(enemies.Kriffid), 199, 119),
        ]),
        EnemyFormation(180, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Geckit), 199, 151),
            FormationMember(1, False, world.get_enemy_instance(enemies.Spinthra), 151, 111),
        ]),
        EnemyFormation(181, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Geckit), 183, 135),
            FormationMember(1, False, world.get_enemy_instance(enemies.Geckit), 215, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.Spinthra), 151, 111),
        ]),
        EnemyFormation(182, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Geckit), 151, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Geckit), 183, 143),
            FormationMember(2, False, world.get_enemy_instance(enemies.Chewy), 167, 103),
            FormationMember(3, False, world.get_enemy_instance(enemies.Chewy), 231, 135),
            FormationMember(4, False, world.get_enemy_instance(enemies.Shyaway), 199, 119),
        ]),
        EnemyFormation(183, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Geckit), 151, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Geckit), 183, 143),
            FormationMember(2, False, world.get_enemy_instance(enemies.Spinthra), 151, 103),
            FormationMember(3, False, world.get_enemy_instance(enemies.Kriffid), 231, 143),
        ]),
        EnemyFormation(184, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Birdy), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.HeavyTroopa), 215, 135),
        ]),
        EnemyFormation(185, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Birdy), 215, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Birdy), 151, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.Birdy), 183, 151),
        ]),
        EnemyFormation(186, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Birdy), 199, 151),
            FormationMember(1, False, world.get_enemy_instance(enemies.Birdy), 135, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.HeavyTroopa), 199, 119),
        ]),
        EnemyFormation(187, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Birdy), 151, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.Birdy), 215, 143),
            FormationMember(2, False, world.get_enemy_instance(enemies.Birdy), 151, 143),
            FormationMember(3, False, world.get_enemy_instance(enemies.Birdy), 215, 111),
            FormationMember(4, False, world.get_enemy_instance(enemies.Birdy), 183, 127),
        ]),
        EnemyFormation(188, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Bluebird), 199, 151),
            FormationMember(1, False, world.get_enemy_instance(enemies.Bluebird), 151, 111),
        ]),
        EnemyFormation(189, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Bluebird), 167, 103),
            FormationMember(1, False, world.get_enemy_instance(enemies.Bluebird), 231, 135),
            FormationMember(2, False, world.get_enemy_instance(enemies.HeavyTroopa), 167, 135),
        ]),
        EnemyFormation(190, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Bluebird), 183, 143),
            FormationMember(1, False, world.get_enemy_instance(enemies.Bluebird), 183, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.Bluebird), 231, 135),
            FormationMember(3, False, world.get_enemy_instance(enemies.Bluebird), 135, 119),
        ]),
        EnemyFormation(191, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Bluebird), 151, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.Bluebird), 215, 143),
            FormationMember(4, False, world.get_enemy_instance(enemies.HeavyTroopa), 183, 127),
        ]),
        EnemyFormation(192, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Pinwheel), 183, 127),
        ]),
        EnemyFormation(193, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Pinwheel), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Muckle), 215, 143),
        ]),
        EnemyFormation(194, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Pinwheel), 151, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Pinwheel), 183, 143),
            FormationMember(2, False, world.get_enemy_instance(enemies.Muckle), 151, 103),
            FormationMember(3, False, world.get_enemy_instance(enemies.Muckle), 231, 143),
        ]),
        EnemyFormation(195, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Pinwheel), 151, 143),
            FormationMember(1, False, world.get_enemy_instance(enemies.Pinwheel), 135, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.Pinwheel), 199, 151),
            FormationMember(3, False, world.get_enemy_instance(enemies.SlingShy), 167, 111),
            FormationMember(4, False, world.get_enemy_instance(enemies.SlingShy), 215, 135),
        ]),
        EnemyFormation(196, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Shaman), 151, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.Shaman), 199, 151),
        ]),
        EnemyFormation(197, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Shaman), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Orbison), 199, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.Jawful), 199, 119),
        ]),
        EnemyFormation(198, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Shaman), 167, 103),
            FormationMember(1, False, world.get_enemy_instance(enemies.Shaman), 231, 135),
            FormationMember(2, False, world.get_enemy_instance(enemies.Jawful), 167, 135),
        ]),
        EnemyFormation(199, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Shaman), 167, 103),
            FormationMember(1, False, world.get_enemy_instance(enemies.Shaman), 231, 135),
            FormationMember(2, False, world.get_enemy_instance(enemies.SlingShy), 135, 127),
            FormationMember(3, False, world.get_enemy_instance(enemies.SlingShy), 183, 151),
            FormationMember(4, False, world.get_enemy_instance(enemies.Jawful), 183, 127),
        ]),
        EnemyFormation(200, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.SlingShy), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Orbison), 215, 135),
        ]),
        EnemyFormation(201, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.SlingShy), 183, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Orbison), 151, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.Orbison), 215, 143),
        ]),
        EnemyFormation(202, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.SlingShy), 167, 135),
            FormationMember(1, False, world.get_enemy_instance(enemies.Orbison), 151, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.Orbison), 215, 143),
            FormationMember(3, False, world.get_enemy_instance(enemies.Jawful), 199, 119),
        ]),
        EnemyFormation(203, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.SlingShy), 183, 143),
            FormationMember(1, False, world.get_enemy_instance(enemies.SlingShy), 151, 127),
            FormationMember(2, False, world.get_enemy_instance(enemies.Pinwheel), 151, 111),
            FormationMember(3, False, world.get_enemy_instance(enemies.Pinwheel), 215, 143),
            FormationMember(4, False, world.get_enemy_instance(enemies.Muckle), 199, 119),
        ]),
        EnemyFormation(204, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Magmus), 183, 127),
        ]),
        EnemyFormation(205, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Magmus), 151, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.Magmus), 215, 143),
            FormationMember(2, False, world.get_enemy_instance(enemies.ArmoredAnt), 183, 127),
        ]),
        EnemyFormation(206, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Magmus), 151, 103),
            FormationMember(1, False, world.get_enemy_instance(enemies.Magmus), 231, 143),
            FormationMember(2, False, world.get_enemy_instance(enemies.Magmus), 199, 119),
            FormationMember(3, False, world.get_enemy_instance(enemies.Oerlikon), 151, 127),
            FormationMember(4, False, world.get_enemy_instance(enemies.Oerlikon), 183, 143),
        ]),
        EnemyFormation(207, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Magmus), 119, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Magmus), 167, 143),
            FormationMember(2, False, world.get_enemy_instance(enemies.ArmoredAnt), 167, 111),
            FormationMember(3, False, world.get_enemy_instance(enemies.ArmoredAnt), 215, 135),
        ]),
        EnemyFormation(208, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Oerlikon), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Vomer), 215, 135),
        ]),
        EnemyFormation(209, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Oerlikon), 183, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Oerlikon), 135, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.Oerlikon), 231, 135),
        ]),
        EnemyFormation(210, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Oerlikon), 215, 151),
            FormationMember(1, False, world.get_enemy_instance(enemies.ChainedKong), 183, 127),
            FormationMember(2, False, world.get_enemy_instance(enemies.ArmoredAnt), 135, 111),
        ]),
        EnemyFormation(211, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Oerlikon), 135, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Oerlikon), 183, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.ChainedKong), 199, 119),
        ]),
        EnemyFormation(212, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Pyrosphere), 151, 135),
            FormationMember(1, False, world.get_enemy_instance(enemies.Pyrosphere), 215, 135),
            FormationMember(2, False, world.get_enemy_instance(enemies.Pyrosphere), 183, 103),
        ]),
        EnemyFormation(213, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Pyrosphere), 199, 143),
            FormationMember(1, False, world.get_enemy_instance(enemies.Pyrosphere), 151, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.ChainedKong), 199, 119),
        ]),
        EnemyFormation(214, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Corkpedite), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.CorkpediteBody), 151, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.Pyrosphere), 215, 143),
        ]),
        EnemyFormation(215, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Pyrosphere), 199, 151),
            FormationMember(1, False, world.get_enemy_instance(enemies.Pyrosphere), 199, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.Stumpet), 151, 111),
        ]),
        EnemyFormation(216, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Vomer), 151, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.ChainedKong), 215, 143),
        ]),
        EnemyFormation(217, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Vomer), 151, 103),
            FormationMember(1, False, world.get_enemy_instance(enemies.Vomer), 183, 127),
            FormationMember(2, False, world.get_enemy_instance(enemies.Vomer), 215, 151),
        ]),
        EnemyFormation(218, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Corkpedite), 199, 151),
            FormationMember(1, False, world.get_enemy_instance(enemies.CorkpediteBody), 215, 143),
            FormationMember(2, False, world.get_enemy_instance(enemies.Vomer), 135, 119),
        ]),
        EnemyFormation(219, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Vomer), 151, 135),
            FormationMember(1, False, world.get_enemy_instance(enemies.Vomer), 151, 103),
            FormationMember(2, False, world.get_enemy_instance(enemies.Stumpet), 215, 143),
        ]),
        EnemyFormation(220, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Terracotta), 183, 127),
        ]),
        EnemyFormation(221, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Terracotta), 183, 151),
            FormationMember(1, False, world.get_enemy_instance(enemies.Terracotta), 151, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.Terracotta), 215, 119),
        ]),
        EnemyFormation(222, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Terracotta), 183, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Forkies), 151, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.Forkies), 215, 143),
        ]),
        EnemyFormation(223, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Terracotta), 135, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Terracotta), 183, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.GuGoomba), 231, 135),
            FormationMember(3, False, world.get_enemy_instance(enemies.GuGoomba), 167, 103),
            FormationMember(4, False, world.get_enemy_instance(enemies.Forkies), 183, 127),
        ]),
        EnemyFormation(224, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Malakoopa), 135, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.TuboTroopa), 215, 143),
        ]),
        EnemyFormation(225, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Malakoopa), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Malakoopa), 199, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.TuboTroopa), 199, 119),
        ]),
        EnemyFormation(226, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Malakoopa), 135, 103),
            FormationMember(1, False, world.get_enemy_instance(enemies.Malakoopa), 231, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.Terracotta), 167, 135),
            FormationMember(3, False, world.get_enemy_instance(enemies.TuboTroopa), 199, 119),
        ]),
        EnemyFormation(227, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Malakoopa), 183, 127),
            FormationMember(3, False, world.get_enemy_instance(enemies.TuboTroopa), 135, 103),
            FormationMember(4, False, world.get_enemy_instance(enemies.TuboTroopa), 231, 151),
        ]),
        EnemyFormation(228, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.GuGoomba), 151, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.GuGoomba), 199, 151),
        ]),
        EnemyFormation(229, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.GuGoomba), 231, 151),
            FormationMember(1, False, world.get_enemy_instance(enemies.GuGoomba), 135, 103),
            FormationMember(2, False, world.get_enemy_instance(enemies.Starcruster), 167, 135),
        ]),
        EnemyFormation(230, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.GuGoomba), 231, 143),
            FormationMember(1, False, world.get_enemy_instance(enemies.Forkies), 199, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.Starcruster), 151, 103),
        ]),
        EnemyFormation(231, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.GuGoomba), 199, 151),
            FormationMember(1, False, world.get_enemy_instance(enemies.GuGoomba), 135, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.Malakoopa), 167, 135),
            FormationMember(3, False, world.get_enemy_instance(enemies.Malakoopa), 199, 119),
            FormationMember(4, False, world.get_enemy_instance(enemies.Terracotta), 167, 103),
            FormationMember(5, False, world.get_enemy_instance(enemies.Terracotta), 231, 135),
        ]),
        EnemyFormation(232, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.BigBertha), 183, 127),
        ]),
        EnemyFormation(233, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.BigBertha), 151, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.BigBertha), 215, 143),
        ]),
        EnemyFormation(234, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.BigBertha), 215, 143),
            FormationMember(1, False, world.get_enemy_instance(enemies.Forkies), 151, 111),
        ]),
        EnemyFormation(235, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.BigBertha), 135, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.BigBertha), 215, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.Terracotta), 183, 127),
        ]),
        EnemyFormation(236, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Magikoopa), 199, 119),
            FormationMember(1, True, world.get_enemy_instance(enemies.Terracotta), 135, 103),
            FormationMember(2, True, world.get_enemy_instance(enemies.Terracotta), 231, 151),
            FormationMember(3, True, world.get_enemy_instance(enemies.Terracotta), 135, 127),
            FormationMember(4, True, world.get_enemy_instance(enemies.Terracotta), 183, 151),
        ]),
        EnemyFormation(237, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Magikoopa), 199, 119),
            FormationMember(1, True, world.get_enemy_instance(enemies.Malakoopa), 215, 143),
            FormationMember(2, True, world.get_enemy_instance(enemies.Malakoopa), 151, 111),
            FormationMember(3, True, world.get_enemy_instance(enemies.TuboTroopa), 167, 135),
        ]),
        EnemyFormation(238, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Magikoopa), 199, 119),
            FormationMember(1, True, world.get_enemy_instance(enemies.GuGoomba), 119, 119),
            FormationMember(2, True, world.get_enemy_instance(enemies.GuGoomba), 199, 159),
            FormationMember(3, True, world.get_enemy_instance(enemies.Starcruster), 167, 135),
        ]),
        EnemyFormation(239, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Magikoopa), 199, 119),
            FormationMember(1, True, world.get_enemy_instance(enemies.Forkies), 135, 111),
            FormationMember(2, True, world.get_enemy_instance(enemies.Starcruster), 215, 151),
        ]),
        EnemyFormation(240, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Ninja), 183, 127),
        ]),
        EnemyFormation(241, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Ninja), 151, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Doppel), 199, 159),
        ]),
        EnemyFormation(242, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Ninja), 199, 151),
            FormationMember(1, False, world.get_enemy_instance(enemies.Ninja), 135, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.Hippopo), 199, 119),
        ]),
        EnemyFormation(243, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Ninja), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Ninja), 183, 127),
            FormationMember(2, False, world.get_enemy_instance(enemies.Ninja), 167, 103),
            FormationMember(3, False, world.get_enemy_instance(enemies.Ninja), 231, 135),
            FormationMember(4, False, world.get_enemy_instance(enemies.Ninja), 199, 151),
        ]),
        EnemyFormation(244, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Springer), 215, 143),
            FormationMember(1, False, world.get_enemy_instance(enemies.GlumReaper), 135, 119),
        ]),
        EnemyFormation(245, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Springer), 151, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.Ninja), 215, 127),
            FormationMember(2, False, world.get_enemy_instance(enemies.Ameboid), 167, 151),
        ]),
        EnemyFormation(246, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Springer), 231, 135),
            FormationMember(1, False, world.get_enemy_instance(enemies.Springer), 167, 103),
            FormationMember(2, False, world.get_enemy_instance(enemies.Puppox), 167, 135),
        ]),
        EnemyFormation(247, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Springer), 183, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Puppox), 215, 143),
            FormationMember(2, False, world.get_enemy_instance(enemies.Puppox), 151, 111),
        ]),
        EnemyFormation(248, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Ameboid), 183, 127),
            FormationMember(1, True, world.get_enemy_instance(enemies.Ameboid), 167, 103),
            FormationMember(2, True, world.get_enemy_instance(enemies.Ameboid), 135, 119),
            FormationMember(3, True, world.get_enemy_instance(enemies.Ameboid), 231, 135),
            FormationMember(4, True, world.get_enemy_instance(enemies.Ameboid), 199, 151),
        ]),
        EnemyFormation(249, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Ameboid), 151, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.Ameboid), 215, 143),
            FormationMember(2, False, world.get_enemy_instance(enemies.Gunyolk), 167, 135),
        ]),
        EnemyFormation(250, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Ameboid), 199, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Gunyolk), 199, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.Boomer), 135, 119),
        ]),
        EnemyFormation(251, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Ameboid), 199, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Ameboid), 151, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.Ameboid), 215, 143),
            FormationMember(3, False, world.get_enemy_instance(enemies.Ameboid), 167, 135),
            FormationMember(4, False, world.get_enemy_instance(enemies.Ameboid), 183, 159),
            FormationMember(5, False, world.get_enemy_instance(enemies.Ameboid), 119, 127),
        ]),
        EnemyFormation(252, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.GlumReaper), 183, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.GlumReaper), 135, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.GlumReaper), 231, 135),
        ]),
        EnemyFormation(253, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.GlumReaper), 215, 159),
            FormationMember(1, False, world.get_enemy_instance(enemies.Hippopo), 151, 111),
        ]),
        EnemyFormation(254, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.GlumReaper), 151, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.GlumReaper), 183, 143),
            FormationMember(2, False, world.get_enemy_instance(enemies.Doppel), 167, 103),
            FormationMember(3, False, world.get_enemy_instance(enemies.Doppel), 231, 135),
        ]),
        EnemyFormation(255, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.GlumReaper), 135, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.GlumReaper), 215, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.LilBoo), 167, 135),
            FormationMember(3, False, world.get_enemy_instance(enemies.LilBoo), 199, 119),
        ]),
        EnemyFormation(256, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.LilBoo), 183, 127),
        ]),
        EnemyFormation(257, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.LilBoo), 183, 151),
            FormationMember(1, False, world.get_enemy_instance(enemies.LilBoo), 215, 135),
            FormationMember(2, False, world.get_enemy_instance(enemies.Hippopo), 151, 111),
        ]),
        EnemyFormation(258, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.LilBoo), 167, 143),
            FormationMember(1, False, world.get_enemy_instance(enemies.LilBoo), 199, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.Puppox), 151, 103),
            FormationMember(3, False, world.get_enemy_instance(enemies.Doppel), 215, 159),
        ]),
        EnemyFormation(259, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.LilBoo), 167, 135),
            FormationMember(1, False, world.get_enemy_instance(enemies.LilBoo), 151, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.LilBoo), 215, 143),
            FormationMember(3, False, world.get_enemy_instance(enemies.LilBoo), 199, 119),
        ]),
        EnemyFormation(260, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.MadMallet), 151, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.MadMallet), 215, 143),
        ]),
        EnemyFormation(261, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.MadMallet), 151, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.MadMallet), 199, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.MadMallet), 199, 119),
        ]),
        EnemyFormation(262, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.MadMallet), 183, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.MadMallet), 135, 127),
            FormationMember(2, False, world.get_enemy_instance(enemies.MadMallet), 231, 135),
            FormationMember(3, False, world.get_enemy_instance(enemies.MadMallet), 167, 103),
            FormationMember(4, False, world.get_enemy_instance(enemies.MadMallet), 183, 151),
        ]),
        EnemyFormation(263, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.MadMallet), 167, 103),
            FormationMember(1, False, world.get_enemy_instance(enemies.MadMallet), 135, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.MadMallet), 199, 151),
            FormationMember(3, False, world.get_enemy_instance(enemies.MadMallet), 231, 135),
            FormationMember(4, False, world.get_enemy_instance(enemies.Clerk), 183, 127),
        ]),
        EnemyFormation(264, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Pounder), 183, 127),
        ]),
        EnemyFormation(265, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Pounder), 183, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Pounder), 231, 135),
            FormationMember(2, False, world.get_enemy_instance(enemies.Pounder), 167, 103),
        ]),
        EnemyFormation(266, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Pounder), 167, 135),
            FormationMember(1, False, world.get_enemy_instance(enemies.Pounder), 199, 143),
            FormationMember(2, False, world.get_enemy_instance(enemies.Pounder), 151, 119),
            FormationMember(3, False, world.get_enemy_instance(enemies.Pounder), 167, 103),
            FormationMember(4, False, world.get_enemy_instance(enemies.Pounder), 231, 135),
        ]),
        EnemyFormation(267, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Pounder), 119, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Pounder), 167, 103),
            FormationMember(2, False, world.get_enemy_instance(enemies.Pounder), 151, 135),
            FormationMember(3, False, world.get_enemy_instance(enemies.Pounder), 199, 119),
            FormationMember(4, False, world.get_enemy_instance(enemies.Clerk), 215, 151),
        ]),
        EnemyFormation(268, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Pandorite), 183, 127),
        ]),
        EnemyFormation(269, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Hidon), 167, 119),
            FormationMember(1, True, world.get_enemy_instance(enemies.Goombette), 135, 111),
            FormationMember(2, True, world.get_enemy_instance(enemies.Goombette), 135, 135),
            FormationMember(3, True, world.get_enemy_instance(enemies.Goombette), 167, 151),
            FormationMember(4, True, world.get_enemy_instance(enemies.Goombette), 215, 151),
        ], stat_total_enemies=[
            # Only include Hidon for boss shuffle logic.
            world.get_enemy_instance(enemies.Hidon),
        ]),
        EnemyFormation(270, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.BoxBoy), 183, 127),
            FormationMember(1, True, world.get_enemy_instance(enemies.Fautso), 151, 111),
        ], stat_total_enemies=[
            # Only count Box Boy for boss shuffle logic.
            world.get_enemy_instance(enemies.BoxBoy),
        ]),
        EnemyFormation(271, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Chester), 183, 127),
            FormationMember(1, True, world.get_enemy_instance(enemies.Bahamutt), 135, 119),
        ]),
        EnemyFormation(273, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.AxemRangers), 183, 127),
        ]),
        EnemyFormation(274, 12, 7, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Booster), 183, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Snifit), 135, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.Snifit), 151, 143),
            FormationMember(3, False, world.get_enemy_instance(enemies.Snifit), 199, 151),
        ]),
        EnemyFormation(275, None, 7, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Booster2), 183, 127),
        ]),
        EnemyFormation(276, None, 7, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Snifit), 183, 127),
        ]),
        EnemyFormation(277, None, 7, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Croco1), 183, 127),
        ]),
        EnemyFormation(278, None, 7, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Croco2), 183, 127),
        ]),
        EnemyFormation(280, None, 7, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Johnny), 183, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.BandanaBlue), 135, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.BandanaBlue), 135, 135),
            FormationMember(3, False, world.get_enemy_instance(enemies.BandanaBlue), 183, 159),
            FormationMember(4, False, world.get_enemy_instance(enemies.BandanaBlue), 215, 151),
        ], stat_total_enemies=[
            # Only count Johnny himself for boss shuffle logic.
            world.get_enemy_instance(enemies.Johnny),
        ], stat_scaling_enemies=[
            # Also need to scale solo Johnny enemy!
            world.get_enemy_instance(enemies.Johnny),
            world.get_enemy_instance(enemies.BandanaBlue),
            world.get_enemy_instance(enemies.JohnnySolo),
        ]),
        EnemyFormation(281, None, 7, [
            FormationMember(0, False, world.get_enemy_instance(enemies.JohnnySolo), 183, 127),
        ]),
        EnemyFormation(282, None, 7, [
            FormationMember(0, False, world.get_enemy_instance(enemies.RightEye), 199, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.BandanaRed), 167, 135),
        ]),
        EnemyFormation(283, None, 7, [
            FormationMember(0, False, world.get_enemy_instance(enemies.RightEye), 199, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.BandanaRed), 151, 127),
            FormationMember(2, False, world.get_enemy_instance(enemies.BandanaRed), 183, 143),
        ]),
        EnemyFormation(284, None, 7, [
            FormationMember(0, False, world.get_enemy_instance(enemies.RightEye), 199, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.BandanaRed), 151, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.BandanaRed), 215, 143),
            FormationMember(3, False, world.get_enemy_instance(enemies.BandanaRed), 135, 127),
            FormationMember(4, False, world.get_enemy_instance(enemies.BandanaRed), 183, 151),
        ]),
        EnemyFormation(285, 26, 7, [
            FormationMember(0, True, world.get_enemy_instance(enemies.KingCalamari), 222, 94),
            FormationMember(1, True, world.get_enemy_instance(enemies.TentaclesLeft), 136, 115),
            FormationMember(2, True, world.get_enemy_instance(enemies.TentaclesLeft), 112, 127),
            FormationMember(3, True, world.get_enemy_instance(enemies.TentaclesRight), 193, 143),
            FormationMember(4, True, world.get_enemy_instance(enemies.TentaclesRight), 168, 156),
            FormationMember(5, True, world.get_enemy_instance(enemies.TentaclesRight), 135, 143),
        ], required_battlefield=Battlefields.KingCalamari, stat_total_enemies=[
            # Need to include total spawned tentacles for boss shuffle logic.
            world.get_enemy_instance(enemies.TentaclesLeft),
            world.get_enemy_instance(enemies.TentaclesRight),
            world.get_enemy_instance(enemies.TentaclesRight),
            world.get_enemy_instance(enemies.TentaclesLeft),
            world.get_enemy_instance(enemies.TentaclesLeft),
            world.get_enemy_instance(enemies.TentaclesRight),
            world.get_enemy_instance(enemies.TentaclesLeft),
            world.get_enemy_instance(enemies.TentaclesRight),
            world.get_enemy_instance(enemies.KingCalamari),
        ]),
        EnemyFormation(286, None, 7, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Belome1), 183, 127),
        ]),
        EnemyFormation(287, None, 7, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Belome2), 183, 127),
            FormationMember(1, True, world.get_enemy_instance(enemies.MarioClone), 135, 119),
            FormationMember(2, True, world.get_enemy_instance(enemies.PeachClone), 215, 159),
        ], stat_total_enemies=[
            # Don't count clones for boss shuffle logic.
            world.get_enemy_instance(enemies.Belome2),
        ], stat_scaling_enemies=[
            world.get_enemy_instance(enemies.Belome2),
            world.get_enemy_instance(enemies.MarioClone),
            world.get_enemy_instance(enemies.MallowClone),
            world.get_enemy_instance(enemies.GenoClone),
            world.get_enemy_instance(enemies.BowserClone),
            world.get_enemy_instance(enemies.PeachClone),
        ]),
        EnemyFormation(289, None, 7, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Valentina), 183, 127),
            FormationMember(1, True, world.get_enemy_instance(enemies.Dodo), 199, 151),
        ]),
        EnemyFormation(290, None, 7, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Cloaker2), 183, 127),
        ]),
        EnemyFormation(291, None, 7, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Microbomb), 183, 127),
        ]),
        EnemyFormation(293, None, 7, [
            FormationMember(0, False, world.get_enemy_instance(enemies.CzarDragon), 183, 143),
            FormationMember(1, True, world.get_enemy_instance(enemies.Zombone), 183, 143),
            FormationMember(2, True, world.get_enemy_instance(enemies.Helio), 167, 119),
            FormationMember(3, True, world.get_enemy_instance(enemies.Helio), 135, 135),
            FormationMember(4, True, world.get_enemy_instance(enemies.Helio), 199, 167),
            FormationMember(5, True, world.get_enemy_instance(enemies.Helio), 231, 151),
        ], stat_total_enemies=[
            # Only include main boss enemies for boss shuffle logic.
            world.get_enemy_instance(enemies.CzarDragon),
            world.get_enemy_instance(enemies.Zombone),
        ]),
        EnemyFormation(294, 58, 7, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Smilax), 180, 157),
            FormationMember(1, True, world.get_enemy_instance(enemies.Smilax), 164, 175),
            FormationMember(2, True, world.get_enemy_instance(enemies.Smilax), 143, 119),
            FormationMember(3, True, world.get_enemy_instance(enemies.Smilax), 207, 151),
            FormationMember(4, True, world.get_enemy_instance(enemies.Smilax), 191, 127),
            FormationMember(5, True, world.get_enemy_instance(enemies.Megasmilax), 175, 111),
        ], stat_total_enemies=[
            # Need to include all spawned enemies for boss shuffle logic.
            world.get_enemy_instance(enemies.Smilax),
            world.get_enemy_instance(enemies.Smilax),
            world.get_enemy_instance(enemies.Smilax),
            world.get_enemy_instance(enemies.Smilax),
            world.get_enemy_instance(enemies.Smilax),
            world.get_enemy_instance(enemies.Smilax),
            world.get_enemy_instance(enemies.Smilax),
            world.get_enemy_instance(enemies.Smilax),
            world.get_enemy_instance(enemies.Megasmilax),
        ], stat_scaling_enemies=[
            # Order Megasmilax first here so it gets all the exp and coins!
            world.get_enemy_instance(enemies.Megasmilax),
            world.get_enemy_instance(enemies.Smilax),
        ]),
        EnemyFormation(295, None, 7, [
            FormationMember(0, False, world.get_enemy_instance(enemies.CountDown), 150, 93),
            FormationMember(1, False, world.get_enemy_instance(enemies.DingALing), 158, 52),
            FormationMember(2, False, world.get_enemy_instance(enemies.DingALing), 194, 67),
        ], required_battlefield=Battlefields.Countdown),
        EnemyFormation(296, None, 7, [
            FormationMember(0, False, world.get_enemy_instance(enemies.AxemYellow), 183, 127),
        ]),
        EnemyFormation(297, None, 7, [
            FormationMember(0, True, world.get_enemy_instance(enemies.Birdo), 167, 118),
            FormationMember(1, False, world.get_enemy_instance(enemies.Shelly), 171, 103),
            FormationMember(2, True, world.get_enemy_instance(enemies.Eggbert), 135, 119),
            FormationMember(3, True, world.get_enemy_instance(enemies.Eggbert), 135, 135),
            FormationMember(4, True, world.get_enemy_instance(enemies.Eggbert), 167, 151),
            FormationMember(5, True, world.get_enemy_instance(enemies.Eggbert), 199, 151),
        ], stat_total_enemies=[
            # Only include Birdo for boss shuffle logic.
            world.get_enemy_instance(enemies.Birdo),
        ]),
        EnemyFormation(298, None, 7, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Bundt), 199, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Raspberry), 199, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.Torte), 199, 151),
            FormationMember(3, False, world.get_enemy_instance(enemies.Torte), 135, 119),
        ], stat_total_enemies=[
            # Only count the cake for boss shuffle logic.
            world.get_enemy_instance(enemies.Bundt),
            world.get_enemy_instance(enemies.Raspberry),
        ]),
        EnemyFormation(299, 17, 7, [
            FormationMember(0, False, world.get_enemy_instance(enemies.KnifeGuy), 151, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.GrateGuy), 199, 143),
        ]),
        EnemyFormation(300, None, 7, [
            FormationMember(0, False, world.get_enemy_instance(enemies.KingBomb), 151, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.MezzoBomb), 199, 143),
        ]),
        # This formation actually has Jinx 3 in the vanilla data, but it's for the Jinx 1 battle!
        # There's a weird battle event that swaps in the Jinx 1 enemy, but we want Jinx 1 data for boss shuffle.
        EnemyFormation(301, 71, 4, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Jinx1), 183, 127),
        ]),
        EnemyFormation(302, None, 11, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Mack), 199, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Bodyguard), 135, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.Bodyguard), 151, 127),
            FormationMember(3, False, world.get_enemy_instance(enemies.Bodyguard), 183, 143),
            FormationMember(4, False, world.get_enemy_instance(enemies.Bodyguard), 215, 151),
        ]),
        EnemyFormation(303, None, 11, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Yaridovich), 183, 127),
            FormationMember(1, True, world.get_enemy_instance(enemies.YaridovichMirage), 183, 127),
        ], stat_total_enemies=[
            # Only include Yarid himself for the boss shuffle logic.
            world.get_enemy_instance(enemies.Yaridovich),
        ]),
        EnemyFormation(304, 61, 11, [
            FormationMember(0, False, world.get_enemy_instance(enemies.AxemRangers), 201, 79),
            FormationMember(1, True, world.get_enemy_instance(enemies.AxemRed), 135, 111),
            FormationMember(2, True, world.get_enemy_instance(enemies.AxemBlack), 135, 127),
            FormationMember(3, True, world.get_enemy_instance(enemies.AxemPink), 151, 143),
            FormationMember(4, True, world.get_enemy_instance(enemies.AxemGreen), 183, 151),
            FormationMember(5, True, world.get_enemy_instance(enemies.AxemYellow), 215, 151),
        ]),
        EnemyFormation(305, 3, 11, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Bowyer), 183, 127),
        ]),
        EnemyFormation(306, None, 7, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Culex), 183, 127),
        ]),
        EnemyFormation(307, 80, 11, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Exor), 193, 64),
            FormationMember(1, False, world.get_enemy_instance(enemies.Neosquid), 187, 136),
            FormationMember(2, True, world.get_enemy_instance(enemies.RightEye), 174, 145),
            FormationMember(3, True, world.get_enemy_instance(enemies.LeftEye), 203, 157),
        ], required_battlefield=Battlefields.Exor),
        EnemyFormation(308, None, 15, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Smithy1), 199, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Smelter), 87, 87),
            FormationMember(2, True, world.get_enemy_instance(enemies.MachineMadeShyster), 135, 127),
            FormationMember(3, True, world.get_enemy_instance(enemies.MachineMadeShyster), 199, 159),
        ]),
        EnemyFormation(309, 52, 7, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Cloaker), 151, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.Domino), 215, 159),
            FormationMember(2, True, world.get_enemy_instance(enemies.MadAdder), 167, 135),
        ], required_battlefield=Battlefields.CloakerDomino, stat_total_enemies=[
            # Count all four enemies for boss shuffle logic.
            world.get_enemy_instance(enemies.Cloaker),
            world.get_enemy_instance(enemies.Domino),
            world.get_enemy_instance(enemies.Earthlink),
            world.get_enemy_instance(enemies.MadAdder),
        ], stat_scaling_enemies=[
            world.get_enemy_instance(enemies.Cloaker),
            world.get_enemy_instance(enemies.Domino),
            world.get_enemy_instance(enemies.Earthlink),
            world.get_enemy_instance(enemies.MadAdder),
            world.get_enemy_instance(enemies.Cloaker2),
            world.get_enemy_instance(enemies.Domino2),
        ]),
        EnemyFormation(310, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Ratfunk), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Ratfunk), 199, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.Ratfunk), 199, 119),
        ]),
        EnemyFormation(311, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Ratfunk), 135, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Ratfunk), 167, 103),
            FormationMember(2, False, world.get_enemy_instance(enemies.Ratfunk), 183, 151),
            FormationMember(3, False, world.get_enemy_instance(enemies.Ratfunk), 231, 135),
            FormationMember(4, False, world.get_enemy_instance(enemies.Ratfunk), 183, 127),
        ]),
        EnemyFormation(312, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Artichoker), 183, 127),
        ]),
        EnemyFormation(313, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Artichoker), 151, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Artichoker), 215, 143),
        ]),
        EnemyFormation(314, 14, 7, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Punchinello), 199, 119),
            FormationMember(1, True, world.get_enemy_instance(enemies.Microbomb), 135, 119),
            FormationMember(2, True, world.get_enemy_instance(enemies.Microbomb), 151, 135),
            FormationMember(3, True, world.get_enemy_instance(enemies.Microbomb), 183, 151),
            FormationMember(4, True, world.get_enemy_instance(enemies.Microbomb), 215, 159),
        ], stat_total_enemies=[
            # Don't count extra bombs for boss shuffle logic.
            world.get_enemy_instance(enemies.Punchinello),
        ], stat_scaling_enemies=[
            world.get_enemy_instance(enemies.Punchinello),
            world.get_enemy_instance(enemies.Microbomb),
            world.get_enemy_instance(enemies.Bobomb),
            world.get_enemy_instance(enemies.MezzoBomb),
        ]),
        EnemyFormation(315, None, 7, [
            FormationMember(0, False, world.get_enemy_instance(enemies.HammerBro), 135, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.HammerBro), 199, 143),
        ]),
        EnemyFormation(316, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Crook), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Crook), 199, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.Crook), 199, 151),
        ]),
        EnemyFormation(317, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Crook), 167, 103),
            FormationMember(1, False, world.get_enemy_instance(enemies.Crook), 135, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.Crook), 183, 127),
            FormationMember(3, False, world.get_enemy_instance(enemies.Crook), 199, 151),
            FormationMember(4, False, world.get_enemy_instance(enemies.Crook), 231, 135),
        ]),
        EnemyFormation(318, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Snifit), 167, 135),
        ]),
        EnemyFormation(319, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Stumpet), 183, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Magmus), 119, 127),
            FormationMember(2, False, world.get_enemy_instance(enemies.Magmus), 183, 159),
        ]),
        EnemyFormation(320, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Poundette), 183, 127),
        ]),
        EnemyFormation(321, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Poundette), 183, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Poundette), 151, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.Poundette), 215, 143),
        ]),
        EnemyFormation(322, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Poundette), 167, 135),
            FormationMember(1, False, world.get_enemy_instance(enemies.Poundette), 199, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.Poundette), 135, 119),
            FormationMember(3, False, world.get_enemy_instance(enemies.Poundette), 167, 103),
            FormationMember(4, False, world.get_enemy_instance(enemies.Poundette), 199, 151),
            FormationMember(5, False, world.get_enemy_instance(enemies.Poundette), 231, 135),
        ]),
        EnemyFormation(323, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Poundette), 199, 151),
            FormationMember(1, False, world.get_enemy_instance(enemies.Poundette), 135, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.Poundette), 199, 135),
            FormationMember(3, False, world.get_enemy_instance(enemies.Poundette), 167, 119),
            FormationMember(4, False, world.get_enemy_instance(enemies.Clerk), 199, 119),
        ]),
        # Remove Mad Mallet, Pounder, and Poundette so we can use them in boss shuffle.
        EnemyFormation(324, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Jabit), 215, 135),
            FormationMember(1, False, world.get_enemy_instance(enemies.Jabit), 151, 119),
        ]),
        EnemyFormation(325, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Jabit), 151, 143),
            FormationMember(1, False, world.get_enemy_instance(enemies.Jabit), 151, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.Jabit), 215, 143),
        ]),
        EnemyFormation(326, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Jabit), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Jabit), 167, 135),
            FormationMember(2, False, world.get_enemy_instance(enemies.Jabit), 231, 135),
            FormationMember(3, False, world.get_enemy_instance(enemies.Jabit), 167, 103),
            FormationMember(4, False, world.get_enemy_instance(enemies.Jabit), 199, 119),
            FormationMember(5, False, world.get_enemy_instance(enemies.Jabit), 199, 151),
        ]),
        EnemyFormation(327, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Jabit), 151, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Jabit), 183, 143),
            FormationMember(2, False, world.get_enemy_instance(enemies.Jabit), 135, 103),
            FormationMember(3, False, world.get_enemy_instance(enemies.Jabit), 183, 111),
            FormationMember(4, False, world.get_enemy_instance(enemies.Jabit), 215, 127),
            FormationMember(5, False, world.get_enemy_instance(enemies.Jabit), 231, 151),
        ]),
        EnemyFormation(328, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Fireball), 151, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.Fireball), 199, 151),
        ]),
        EnemyFormation(329, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Fireball), 167, 135),
            FormationMember(1, False, world.get_enemy_instance(enemies.Fireball), 167, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.Fireball), 215, 135),
        ]),
        EnemyFormation(330, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Stumpet), 151, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.Magmus), 183, 159),
            FormationMember(2, False, world.get_enemy_instance(enemies.Magmus), 199, 135),
            FormationMember(3, False, world.get_enemy_instance(enemies.Magmus), 231, 159),
        ]),
        EnemyFormation(331, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Corkpedite), 151, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.CorkpediteBody), 167, 103),
            FormationMember(2, False, world.get_enemy_instance(enemies.Oerlikon), 199, 151),
        ]),
        EnemyFormation(332, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Corkpedite), 151, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.CorkpediteBody), 167, 103),
            FormationMember(2, False, world.get_enemy_instance(enemies.Oerlikon), 183, 159),
            FormationMember(3, False, world.get_enemy_instance(enemies.Oerlikon), 215, 143),
        ]),
        EnemyFormation(333, 72, 4, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Jinx2), 183, 127),
        ]),
        EnemyFormation(334, 73, 4, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Jinx3), 183, 127),
        ]),
        EnemyFormation(335, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Jagger), 183, 127),
        ]),
        EnemyFormation(350, None, 31, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Culex), 183, 103),
            FormationMember(1, True, world.get_enemy_instance(enemies.FireCrystal), 135, 103),
            FormationMember(2, True, world.get_enemy_instance(enemies.FireCrystal), 151, 119),
            FormationMember(3, True, world.get_enemy_instance(enemies.FireCrystal), 183, 135),
            FormationMember(4, True, world.get_enemy_instance(enemies.FireCrystal), 215, 143),
        ], stat_total_enemies=[
            # Only count Culex himself for the boss shuffle logic.
            world.get_enemy_instance(enemies.Culex),
        ], stat_scaling_enemies=[
            world.get_enemy_instance(enemies.Culex),
            world.get_enemy_instance(enemies.EarthCrystal),
            world.get_enemy_instance(enemies.FireCrystal),
            world.get_enemy_instance(enemies.WindCrystal),
            world.get_enemy_instance(enemies.WaterCrystal),
        ]),
        EnemyFormation(351, None, 7, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Formless), 167, 135),
            FormationMember(1, True, world.get_enemy_instance(enemies.Mokura), 167, 135),
        ]),
        EnemyFormation(352, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Superspike), 167, 135),
            FormationMember(1, False, world.get_enemy_instance(enemies.Superspike), 151, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.Superspike), 215, 143),
        ]),
        EnemyFormation(353, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Superspike), 167, 103),
            FormationMember(1, False, world.get_enemy_instance(enemies.Superspike), 151, 127),
            FormationMember(2, False, world.get_enemy_instance(enemies.Superspike), 215, 127),
            FormationMember(3, False, world.get_enemy_instance(enemies.Superspike), 199, 151),
        ]),
        EnemyFormation(354, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Shogun), 167, 135),
            FormationMember(1, False, world.get_enemy_instance(enemies.Shogun), 151, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.Shogun), 215, 143),
        ]),
        EnemyFormation(355, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.HeavyTroopa), 167, 135),
            FormationMember(1, False, world.get_enemy_instance(enemies.HeavyTroopa), 151, 103),
            FormationMember(2, False, world.get_enemy_instance(enemies.HeavyTroopa), 231, 143),
        ]),
        EnemyFormation(356, None, 7, [
            FormationMember(0, False, world.get_enemy_instance(enemies.DodoSolo), 183, 127),
        ]),
        EnemyFormation(357, 101, 7, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Magikoopa), 215, 111),
            FormationMember(1, True, world.get_enemy_instance(enemies.Terrapin), 167, 135),
        ], stat_total_enemies=[
            # Only count Magikoopa himself for boss shuffle logic.
            world.get_enemy_instance(enemies.Magikoopa),
        ], stat_scaling_enemies=[
            world.get_enemy_instance(enemies.Magikoopa),
            world.get_enemy_instance(enemies.JinxClone),
            world.get_enemy_instance(enemies.KingBomb),
            world.get_enemy_instance(enemies.Bahamutt),
        ]),
        EnemyFormation(358, None, 7, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Boomer), 215, 143),
            FormationMember(1, False, world.get_enemy_instance(enemies.HanginShy), 66, 115),
            FormationMember(2, False, world.get_enemy_instance(enemies.HanginShy), 186, 74),
        ], stat_total_enemies=[
            # Only count Boomer himself for boss shuffle logic.
            world.get_enemy_instance(enemies.Boomer),
        ], stat_scaling_enemies=[
            world.get_enemy_instance(enemies.Boomer),
        ]),
        EnemyFormation(359, None, 9, [
            FormationMember(0, False, world.get_enemy_instance(enemies.MachineMadeMack), 199, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.MachineMadeShyster), 135, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.MachineMadeShyster), 151, 127),
            FormationMember(3, False, world.get_enemy_instance(enemies.MachineMadeShyster), 183, 143),
            FormationMember(4, False, world.get_enemy_instance(enemies.MachineMadeShyster), 215, 151),
        ]),
        EnemyFormation(360, None, 9, [
            FormationMember(0, False, world.get_enemy_instance(enemies.MachineMadeBowyer), 183, 127),
        ]),
        EnemyFormation(361, None, 9, [
            FormationMember(0, False, world.get_enemy_instance(enemies.MachineMadeYaridovich), 183, 127),
            FormationMember(1, True, world.get_enemy_instance(enemies.MachineMadeDrillBit), 135, 119),
            FormationMember(2, True, world.get_enemy_instance(enemies.MachineMadeDrillBit), 167, 103),
            FormationMember(3, True, world.get_enemy_instance(enemies.MachineMadeDrillBit), 199, 151),
            FormationMember(4, True, world.get_enemy_instance(enemies.MachineMadeDrillBit), 231, 135),
        ]),
        EnemyFormation(362, None, 9, [
            FormationMember(0, False, world.get_enemy_instance(enemies.MachineMadeAxemPink), 151, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.MachineMadeAxemRed), 151, 143),
            FormationMember(4, False, world.get_enemy_instance(enemies.MachineMadeAxemGreen), 215, 143),
        ]),
        EnemyFormation(363, None, 1, [
            FormationMember(0, True, world.get_enemy_instance(enemies.Smithy2Body), 183, 135),
            FormationMember(1, False, world.get_enemy_instance(enemies.Smithy2Head), 183, 175),
        ]),
        EnemyFormation(364, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Clerk), 199, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.MadMallet), 135, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.MadMallet), 199, 151),
        ]),
        EnemyFormation(365, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Manager), 199, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Pounder), 151, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.Pounder), 167, 135),
            FormationMember(3, False, world.get_enemy_instance(enemies.Pounder), 215, 143),
        ]),
        EnemyFormation(366, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Director), 183, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Poundette), 135, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.Poundette), 167, 103),
            FormationMember(3, False, world.get_enemy_instance(enemies.Poundette), 199, 151),
            FormationMember(4, False, world.get_enemy_instance(enemies.Poundette), 231, 135),
        ]),
        EnemyFormation(367, None, 7, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Gunyolk), 199, 103),
            FormationMember(1, False, world.get_enemy_instance(enemies.FactoryChief), 231, 151),
        ]),
        EnemyFormation(368, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.MadMallet), 151, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.MadMallet), 167, 135),
            FormationMember(2, False, world.get_enemy_instance(enemies.MadMallet), 215, 143),
        ]),
        EnemyFormation(369, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Apprentice), 183, 127),
        ]),
        EnemyFormation(370, None, 9, [
            FormationMember(0, False, world.get_enemy_instance(enemies.MachineMadeAxemBlack), 151, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.MachineMadeAxemBlack), 231, 127),
            FormationMember(2, False, world.get_enemy_instance(enemies.MachineMadeAxemYellow), 199, 143),
            FormationMember(3, False, world.get_enemy_instance(enemies.MachineMadeAxemYellow), 183, 103),
        ]),
        EnemyFormation(371, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Terracotta), 135, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Terracotta), 183, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.Terracotta), 183, 151),
            FormationMember(3, False, world.get_enemy_instance(enemies.Terracotta), 231, 135),
        ]),
        EnemyFormation(372, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Oerlikon), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Oerlikon), 199, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.Starcruster), 199, 119),
        ]),
        EnemyFormation(373, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Sackit), 167, 135),
            FormationMember(2, False, world.get_enemy_instance(enemies.BigBertha), 151, 103),
            FormationMember(3, False, world.get_enemy_instance(enemies.BigBertha), 231, 143),
        ]),
        EnemyFormation(374, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Chow), 135, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.Chow), 215, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.Forkies), 199, 119),
        ]),
        EnemyFormation(375, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.AlleyRat), 199, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.ArmoredAnt), 135, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.ArmoredAnt), 199, 151),
        ]),
        EnemyFormation(376, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Bloober), 199, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Bloober), 183, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.Bloober), 231, 151),
            FormationMember(3, False, world.get_enemy_instance(enemies.Starcruster), 135, 103),
        ]),
        EnemyFormation(377, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Stinger), 151, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.Stinger), 167, 127),
            FormationMember(2, False, world.get_enemy_instance(enemies.Stinger), 199, 143),
            FormationMember(3, False, world.get_enemy_instance(enemies.Stinger), 231, 151),
        ]),
        EnemyFormation(378, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Geckit), 215, 151),
            FormationMember(1, False, world.get_enemy_instance(enemies.Geckit), 135, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.ChainedKong), 199, 119),
        ]),
        EnemyFormation(379, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Robomb), 167, 135),
            FormationMember(2, False, world.get_enemy_instance(enemies.BigBertha), 167, 111),
            FormationMember(3, False, world.get_enemy_instance(enemies.BigBertha), 215, 135),
        ]),
        EnemyFormation(380, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Vomer), 151, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Vomer), 183, 143),
            FormationMember(2, False, world.get_enemy_instance(enemies.Vomer), 151, 103),
            FormationMember(3, False, world.get_enemy_instance(enemies.Vomer), 231, 143),
        ]),
        EnemyFormation(381, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Magmus), 151, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Magmus), 183, 143),
            FormationMember(2, False, world.get_enemy_instance(enemies.Pulsar), 151, 103),
            FormationMember(3, False, world.get_enemy_instance(enemies.Pulsar), 231, 143),
        ]),
        EnemyFormation(382, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.GuGoomba), 151, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.GuGoomba), 183, 143),
            FormationMember(2, False, world.get_enemy_instance(enemies.GuGoomba), 199, 119),
            FormationMember(3, False, world.get_enemy_instance(enemies.GuGoomba), 167, 103),
            FormationMember(4, False, world.get_enemy_instance(enemies.GuGoomba), 231, 135),
        ]),
        EnemyFormation(383, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Malakoopa), 135, 111),
            FormationMember(1, False, world.get_enemy_instance(enemies.Malakoopa), 215, 151),
            FormationMember(2, False, world.get_enemy_instance(enemies.TuboTroopa), 199, 119),
        ]),
        EnemyFormation(384, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.TheBigBoo), 183, 143),
            FormationMember(1, False, world.get_enemy_instance(enemies.TheBigBoo), 151, 127),
            FormationMember(2, False, world.get_enemy_instance(enemies.Orbison), 167, 103),
            FormationMember(3, False, world.get_enemy_instance(enemies.Orbison), 231, 135),
        ]),
        EnemyFormation(385, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.SlingShy), 167, 135),
            FormationMember(1, False, world.get_enemy_instance(enemies.SlingShy), 167, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.SlingShy), 199, 135),
            FormationMember(3, False, world.get_enemy_instance(enemies.SlingShy), 167, 103),
            FormationMember(4, False, world.get_enemy_instance(enemies.SlingShy), 231, 135),
        ]),
        EnemyFormation(386, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Chewy), 151, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Chewy), 183, 143),
            FormationMember(2, False, world.get_enemy_instance(enemies.Shyaway), 167, 103),
            FormationMember(3, False, world.get_enemy_instance(enemies.Shyaway), 231, 135),
        ]),
        EnemyFormation(387, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.MrKipper), 167, 135),
            FormationMember(1, False, world.get_enemy_instance(enemies.Muckle), 167, 103),
            FormationMember(2, False, world.get_enemy_instance(enemies.Muckle), 231, 135),
        ]),
        EnemyFormation(388, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Amanita), 215, 143),
            FormationMember(1, False, world.get_enemy_instance(enemies.Amanita), 151, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.Orbison), 183, 127),
        ]),
        EnemyFormation(389, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Greaper), 215, 143),
            FormationMember(1, False, world.get_enemy_instance(enemies.Greaper), 151, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.GlumReaper), 183, 127),
        ]),
        EnemyFormation(390, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Pyrosphere), 183, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Pyrosphere), 151, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.Pyrosphere), 215, 143),
        ]),
        EnemyFormation(391, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Lakitu), 183, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Lakitu), 151, 111),
            FormationMember(2, False, world.get_enemy_instance(enemies.Lakitu), 215, 143),
        ]),
        EnemyFormation(392, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Zeostar), 151, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.Zeostar), 183, 143),
            FormationMember(2, False, world.get_enemy_instance(enemies.Shaman), 167, 103),
            FormationMember(3, False, world.get_enemy_instance(enemies.Shaman), 231, 135),
        ]),
        EnemyFormation(393, None, 3, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Shaman), 135, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Shaman), 167, 103),
            FormationMember(2, False, world.get_enemy_instance(enemies.Shaman), 167, 135),
            FormationMember(3, False, world.get_enemy_instance(enemies.Shaman), 199, 119),
            FormationMember(4, False, world.get_enemy_instance(enemies.Shaman), 199, 151),
            FormationMember(5, False, world.get_enemy_instance(enemies.Shaman), 231, 135),
        ]),
        EnemyFormation(394, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.MachineMadeShyster), 199, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.MachineMadeShyster), 135, 119),
            FormationMember(2, False, world.get_enemy_instance(enemies.MachineMadeShyster), 199, 151),
        ]),
        EnemyFormation(395, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.MachineMadeDrillBit), 183, 127),
            FormationMember(1, False, world.get_enemy_instance(enemies.MachineMadeDrillBit), 167, 103),
            FormationMember(2, False, world.get_enemy_instance(enemies.MachineMadeDrillBit), 231, 135),
        ]),
        EnemyFormation(400, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Smithy2Body), 183, 127),
        ]),
        EnemyFormation(480, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.Cloaker2), 167, 135),
        ]),
        EnemyFormation(496, None, 1, [
            FormationMember(0, False, world.get_enemy_instance(enemies.JinxClone), 167, 135),
        ]),
        EnemyFormation(509, None, 1, [
            FormationMember(0, True, world.get_enemy_instance(enemies.Candle), 151, 119),
            FormationMember(1, False, world.get_enemy_instance(enemies.Raspberry), 199, 119),
            FormationMember(2, True, world.get_enemy_instance(enemies.Terrapin), 135, 143),
            FormationMember(3, True, world.get_enemy_instance(enemies.Terrapin), 151, 159),
        ]),
        EnemyFormation(511, None, 11, [
            FormationMember(0, False, world.get_enemy_instance(enemies.MachineMadeShyster), 183, 127),
        ]),
    ]

    # Internal mapping of formations by index to look up when building formation packs for convenience.
    formations_dict = dict((f.index, f) for f in formations)

    # Vanilla formation pack data.
    formation_packs = [
        FormationPack(2, [
            formations_dict[4],
            formations_dict[5],
            formations_dict[5],
        ]),
        FormationPack(3, [
            formations_dict[7],
            formations_dict[6],
            formations_dict[6],
        ]),
        FormationPack(4, [
            formations_dict[8],
            formations_dict[9],
            formations_dict[9],
        ]),
        FormationPack(5, [
            formations_dict[11],
            formations_dict[10],
            formations_dict[9],
        ]),
        FormationPack(6, [
            formations_dict[12],
            formations_dict[13],
            formations_dict[12],
        ]),
        FormationPack(7, [
            formations_dict[15],
            formations_dict[14],
            formations_dict[13],
        ]),
        FormationPack(8, [
            formations_dict[16],
            formations_dict[17],
            formations_dict[18],
        ]),
        FormationPack(9, [
            formations_dict[19],
            formations_dict[18],
            formations_dict[17],
        ]),
        FormationPack(10, [
            formations_dict[21],
            formations_dict[22],
            formations_dict[21],
        ]),
        FormationPack(11, [
            formations_dict[21],
            formations_dict[22],
            formations_dict[22],
        ]),
        FormationPack(12, [
            formations_dict[24],
            formations_dict[25],
            formations_dict[26],
        ]),
        FormationPack(13, [
            formations_dict[27],
            formations_dict[26],
            formations_dict[25],
        ]),
        FormationPack(14, [
            formations_dict[29],
            formations_dict[29],
            formations_dict[30],
        ]),
        FormationPack(15, [
            formations_dict[31],
            formations_dict[30],
            formations_dict[29],
        ]),
        FormationPack(16, [
            formations_dict[33],
            formations_dict[33],
            formations_dict[34],
        ]),
        FormationPack(17, [
            formations_dict[34],
            formations_dict[34],
            formations_dict[33],
        ]),
        FormationPack(18, [
            formations_dict[36],
            formations_dict[37],
            formations_dict[38],
        ]),
        FormationPack(19, [
            formations_dict[39],
            formations_dict[38],
            formations_dict[37],
        ]),
        FormationPack(20, [
            formations_dict[41],
            formations_dict[41],
            formations_dict[42],
        ]),
        FormationPack(21, [
            formations_dict[43],
            formations_dict[42],
            formations_dict[41],
        ]),
        FormationPack(22, [
            formations_dict[44],
            formations_dict[45],
            formations_dict[46],
        ]),
        FormationPack(23, [
            formations_dict[47],
            formations_dict[46],
            formations_dict[45],
        ]),
        FormationPack(24, [
            formations_dict[48],
            formations_dict[49],
            formations_dict[50],
        ]),
        FormationPack(25, [
            formations_dict[51],
            formations_dict[50],
            formations_dict[49],
        ]),
        FormationPack(26, [
            formations_dict[52],
            formations_dict[53],
            formations_dict[54],
        ]),
        FormationPack(27, [
            formations_dict[55],
            formations_dict[54],
            formations_dict[53],
        ]),
        FormationPack(28, [
            formations_dict[56],
            formations_dict[57],
            formations_dict[58],
        ]),
        FormationPack(29, [
            formations_dict[59],
            formations_dict[58],
            formations_dict[57],
        ]),
        FormationPack(30, [
            formations_dict[60],
            formations_dict[61],
            formations_dict[62],
        ]),
        FormationPack(31, [
            formations_dict[62],
            formations_dict[62],
            formations_dict[61],
        ]),
        FormationPack(32, [
            formations_dict[64],
            formations_dict[65],
            formations_dict[66],
        ]),
        FormationPack(33, [
            formations_dict[67],
            formations_dict[66],
            formations_dict[65],
        ]),
        FormationPack(34, [
            formations_dict[68],
            formations_dict[69],
            formations_dict[70],
        ]),
        FormationPack(35, [
            formations_dict[71],
            formations_dict[70],
            formations_dict[69],
        ]),
        FormationPack(36, [
            formations_dict[72],
            formations_dict[73],
            formations_dict[74],
        ]),
        FormationPack(37, [
            formations_dict[75],
            formations_dict[74],
            formations_dict[73],
        ]),
        FormationPack(38, [
            formations_dict[76],
            formations_dict[77],
            formations_dict[78],
        ]),
        FormationPack(39, [
            formations_dict[79],
            formations_dict[78],
            formations_dict[77],
        ]),
        FormationPack(40, [
            formations_dict[80],
            formations_dict[81],
            formations_dict[82],
        ]),
        FormationPack(41, [
            formations_dict[83],
            formations_dict[82],
            formations_dict[81],
        ]),
        FormationPack(42, [
            formations_dict[84],
            formations_dict[85],
            formations_dict[86],
        ]),
        FormationPack(43, [
            formations_dict[87],
            formations_dict[86],
            formations_dict[85],
        ]),
        FormationPack(44, [
            formations_dict[88],
            formations_dict[89],
            formations_dict[90],
        ]),
        FormationPack(45, [
            formations_dict[91],
            formations_dict[90],
            formations_dict[89],
        ]),
        FormationPack(46, [
            formations_dict[92],
            formations_dict[93],
            formations_dict[94],
        ]),
        FormationPack(47, [
            formations_dict[95],
            formations_dict[94],
            formations_dict[93],
        ]),
        FormationPack(48, [
            formations_dict[96],
            formations_dict[97],
            formations_dict[98],
        ]),
        FormationPack(49, [
            formations_dict[99],
            formations_dict[98],
            formations_dict[97],
        ]),
        FormationPack(50, [
            formations_dict[100],
            formations_dict[101],
            formations_dict[102],
        ]),
        FormationPack(51, [
            formations_dict[103],
            formations_dict[102],
            formations_dict[101],
        ]),
        FormationPack(52, [
            formations_dict[104],
            formations_dict[105],
            formations_dict[106],
        ]),
        FormationPack(53, [
            formations_dict[107],
            formations_dict[106],
            formations_dict[105],
        ]),
        FormationPack(54, [
            formations_dict[108],
            formations_dict[109],
            formations_dict[110],
        ]),
        FormationPack(55, [
            formations_dict[111],
            formations_dict[110],
            formations_dict[109],
        ]),
        FormationPack(56, [
            formations_dict[112],
            formations_dict[113],
            formations_dict[114],
        ]),
        FormationPack(57, [
            formations_dict[115],
            formations_dict[114],
            formations_dict[113],
        ]),
        FormationPack(58, [
            formations_dict[116],
            formations_dict[117],
            formations_dict[118],
        ]),
        FormationPack(59, [
            formations_dict[119],
            formations_dict[118],
            formations_dict[117],
        ]),
        FormationPack(60, [
            formations_dict[120],
            formations_dict[121],
            formations_dict[122],
        ]),
        FormationPack(61, [
            formations_dict[123],
            formations_dict[122],
            formations_dict[121],
        ]),
        FormationPack(62, [
            formations_dict[124],
            formations_dict[125],
            formations_dict[126],
        ]),
        FormationPack(63, [
            formations_dict[127],
            formations_dict[126],
            formations_dict[125],
        ]),
        FormationPack(64, [
            formations_dict[128],
            formations_dict[129],
            formations_dict[130],
        ]),
        FormationPack(65, [
            formations_dict[131],
            formations_dict[130],
            formations_dict[129],
        ]),
        FormationPack(66, [
            formations_dict[132],
            formations_dict[133],
            formations_dict[134],
        ]),
        FormationPack(67, [
            formations_dict[135],
            formations_dict[134],
            formations_dict[133],
        ]),
        FormationPack(68, [
            formations_dict[136],
            formations_dict[136],
            formations_dict[136],
        ]),
        FormationPack(69, [
            formations_dict[137],
            formations_dict[137],
            formations_dict[137],
        ]),
        FormationPack(70, [
            formations_dict[140],
            formations_dict[141],
            formations_dict[142],
        ]),
        FormationPack(71, [
            formations_dict[143],
            formations_dict[142],
            formations_dict[141],
        ]),
        FormationPack(72, [
            formations_dict[144],
            formations_dict[145],
            formations_dict[146],
        ]),
        FormationPack(73, [
            formations_dict[147],
            formations_dict[146],
            formations_dict[145],
        ]),
        FormationPack(74, [
            formations_dict[148],
            formations_dict[149],
            formations_dict[150],
        ]),
        FormationPack(75, [
            formations_dict[151],
            formations_dict[150],
            formations_dict[149],
        ]),
        FormationPack(76, [
            formations_dict[152],
            formations_dict[153],
            formations_dict[154],
        ]),
        FormationPack(77, [
            formations_dict[155],
            formations_dict[154],
            formations_dict[153],
        ]),
        FormationPack(78, [
            formations_dict[156],
            formations_dict[157],
            formations_dict[158],
        ]),
        FormationPack(79, [
            formations_dict[159],
            formations_dict[158],
            formations_dict[157],
        ]),
        FormationPack(80, [
            formations_dict[160],
            formations_dict[161],
            formations_dict[162],
        ]),
        FormationPack(81, [
            formations_dict[163],
            formations_dict[162],
            formations_dict[161],
        ]),
        FormationPack(82, [
            formations_dict[164],
            formations_dict[165],
            formations_dict[166],
        ]),
        FormationPack(83, [
            formations_dict[167],
            formations_dict[166],
            formations_dict[165],
        ]),
        FormationPack(84, [
            formations_dict[168],
            formations_dict[169],
            formations_dict[170],
        ]),
        FormationPack(85, [
            formations_dict[171],
            formations_dict[170],
            formations_dict[169],
        ]),
        FormationPack(86, [
            formations_dict[172],
            formations_dict[173],
            formations_dict[174],
        ]),
        FormationPack(87, [
            formations_dict[175],
            formations_dict[174],
            formations_dict[173],
        ]),
        FormationPack(88, [
            formations_dict[176],
            formations_dict[177],
            formations_dict[178],
        ]),
        FormationPack(89, [
            formations_dict[179],
            formations_dict[178],
            formations_dict[177],
        ]),
        FormationPack(90, [
            formations_dict[180],
            formations_dict[181],
            formations_dict[182],
        ]),
        FormationPack(91, [
            formations_dict[183],
            formations_dict[182],
            formations_dict[181],
        ]),
        FormationPack(92, [
            formations_dict[184],
            formations_dict[185],
            formations_dict[186],
        ]),
        FormationPack(93, [
            formations_dict[187],
            formations_dict[186],
            formations_dict[185],
        ]),
        FormationPack(94, [
            formations_dict[188],
            formations_dict[189],
            formations_dict[190],
        ]),
        FormationPack(95, [
            formations_dict[191],
            formations_dict[190],
            formations_dict[189],
        ]),
        FormationPack(96, [
            formations_dict[192],
            formations_dict[193],
            formations_dict[194],
        ]),
        FormationPack(97, [
            formations_dict[195],
            formations_dict[194],
            formations_dict[193],
        ]),
        FormationPack(98, [
            formations_dict[196],
            formations_dict[197],
            formations_dict[198],
        ]),
        FormationPack(99, [
            formations_dict[199],
            formations_dict[198],
            formations_dict[197],
        ]),
        FormationPack(100, [
            formations_dict[200],
            formations_dict[201],
            formations_dict[202],
        ]),
        FormationPack(101, [
            formations_dict[203],
            formations_dict[202],
            formations_dict[201],
        ]),
        FormationPack(102, [
            formations_dict[204],
            formations_dict[205],
            formations_dict[206],
        ]),
        FormationPack(103, [
            formations_dict[207],
            formations_dict[206],
            formations_dict[205],
        ]),
        FormationPack(104, [
            formations_dict[208],
            formations_dict[209],
            formations_dict[210],
        ]),
        FormationPack(105, [
            formations_dict[211],
            formations_dict[210],
            formations_dict[209],
        ]),
        FormationPack(106, [
            formations_dict[212],
            formations_dict[213],
            formations_dict[214],
        ]),
        FormationPack(107, [
            formations_dict[215],
            formations_dict[214],
            formations_dict[213],
        ]),
        FormationPack(108, [
            formations_dict[216],
            formations_dict[217],
            formations_dict[218],
        ]),
        FormationPack(109, [
            formations_dict[219],
            formations_dict[218],
            formations_dict[217],
        ]),
        FormationPack(110, [
            formations_dict[220],
            formations_dict[221],
            formations_dict[222],
        ]),
        FormationPack(111, [
            formations_dict[223],
            formations_dict[222],
            formations_dict[221],
        ]),
        FormationPack(112, [
            formations_dict[224],
            formations_dict[225],
            formations_dict[226],
        ]),
        FormationPack(113, [
            formations_dict[227],
            formations_dict[226],
            formations_dict[225],
        ]),
        FormationPack(114, [
            formations_dict[228],
            formations_dict[229],
            formations_dict[230],
        ]),
        FormationPack(115, [
            formations_dict[231],
            formations_dict[230],
            formations_dict[229],
        ]),
        FormationPack(116, [
            formations_dict[232],
            formations_dict[233],
            formations_dict[234],
        ]),
        FormationPack(117, [
            formations_dict[235],
            formations_dict[234],
            formations_dict[233],
        ]),
        FormationPack(118, [
            formations_dict[236],
            formations_dict[237],
            formations_dict[238],
        ]),
        FormationPack(119, [
            formations_dict[239],
            formations_dict[238],
            formations_dict[237],
        ]),
        FormationPack(120, [
            formations_dict[240],
            formations_dict[241],
            formations_dict[242],
        ]),
        FormationPack(121, [
            formations_dict[243],
            formations_dict[242],
            formations_dict[241],
        ]),
        FormationPack(122, [
            formations_dict[244],
            formations_dict[246],
            formations_dict[244],
        ]),
        FormationPack(123, [
            formations_dict[247],
            formations_dict[246],
            formations_dict[244],
        ]),
        FormationPack(124, [
            formations_dict[260],
            formations_dict[261],
            formations_dict[262],
        ]),
        FormationPack(125, [
            formations_dict[262],
            formations_dict[261],
            formations_dict[260],
        ]),
        FormationPack(126, [
            formations_dict[264],
            formations_dict[265],
            formations_dict[266],
        ]),
        FormationPack(127, [
            formations_dict[266],
            formations_dict[265],
            formations_dict[264],
        ]),
        FormationPack(128, [
            formations_dict[320],
            formations_dict[321],
            formations_dict[322],
        ]),
        FormationPack(129, [
            formations_dict[322],
            formations_dict[321],
            formations_dict[320],
        ]),
        FormationPack(130, [
            formations_dict[248],
            formations_dict[248],
            formations_dict[248],
        ]),
        FormationPack(131, [
            formations_dict[248],
            formations_dict[248],
            formations_dict[248],
        ]),
        FormationPack(132, [
            formations_dict[252],
            formations_dict[253],
            formations_dict[254],
        ]),
        FormationPack(133, [
            formations_dict[255],
            formations_dict[254],
            formations_dict[253],
        ]),
        FormationPack(134, [
            formations_dict[256],
            formations_dict[257],
            formations_dict[258],
        ]),
        FormationPack(135, [
            formations_dict[259],
            formations_dict[258],
            formations_dict[257],
        ]),
        FormationPack(136, [
            formations_dict[324],
            formations_dict[325],
            formations_dict[326],
        ]),
        FormationPack(137, [
            formations_dict[327],
            formations_dict[326],
            formations_dict[325],
        ]),
        FormationPack(138, [
            formations_dict[310],
            formations_dict[311],
            formations_dict[310],
        ]),
        FormationPack(139, [
            formations_dict[312],
            formations_dict[313],
            formations_dict[312],
        ]),
        FormationPack(140, [
            formations_dict[314],
            formations_dict[314],
            formations_dict[314],
        ]),
        FormationPack(141, [
            formations_dict[316],
            formations_dict[317],
            formations_dict[316],
        ]),
        FormationPack(142, [
            formations_dict[318],
            formations_dict[318],
            formations_dict[318],
        ]),
        FormationPack(143, [
            formations_dict[328],
            formations_dict[329],
            formations_dict[328],
        ]),
        FormationPack(144, [
            formations_dict[319],
            formations_dict[330],
            formations_dict[319],
        ]),
        FormationPack(145, [
            formations_dict[331],
            formations_dict[332],
            formations_dict[331],
        ]),
        FormationPack(146, [
            formations_dict[364],
            formations_dict[364],
            formations_dict[364],
        ]),
        FormationPack(147, [
            formations_dict[365],
            formations_dict[365],
            formations_dict[365],
        ]),
        FormationPack(148, [
            formations_dict[366],
            formations_dict[366],
            formations_dict[366],
        ]),
        FormationPack(149, [
            formations_dict[367],
            formations_dict[367],
            formations_dict[367],
        ]),
        FormationPack(150, [
            formations_dict[368],
            formations_dict[368],
            formations_dict[368],
        ]),
        FormationPack(151, [
            formations_dict[369],
            formations_dict[369],
            formations_dict[369],
        ]),
        FormationPack(152, [
            formations_dict[394],
            formations_dict[394],
            formations_dict[394],
        ]),
        FormationPack(153, [
            formations_dict[395],
            formations_dict[395],
            formations_dict[395],
        ]),
        FormationPack(156, [
            formations_dict[268],
            formations_dict[268],
            formations_dict[268],
        ]),
        FormationPack(157, [
            formations_dict[269],
            formations_dict[269],
            formations_dict[269],
        ]),
        FormationPack(158, [
            formations_dict[270],
            formations_dict[270],
            formations_dict[270],
        ]),
        FormationPack(159, [
            formations_dict[271],
            formations_dict[271],
            formations_dict[271],
        ]),
        FormationPack(161, [
            formations_dict[274],
            formations_dict[274],
            formations_dict[274],
        ]),
        FormationPack(162, [
            formations_dict[275],
            formations_dict[275],
            formations_dict[275],
        ]),
        FormationPack(163, [
            formations_dict[277],
            formations_dict[277],
            formations_dict[277],
        ]),
        FormationPack(164, [
            formations_dict[278],
            formations_dict[278],
            formations_dict[278],
        ]),
        FormationPack(166, [
            formations_dict[280],
            formations_dict[280],
            formations_dict[280],
        ]),
        FormationPack(167, [
            formations_dict[285],
            formations_dict[285],
            formations_dict[285],
        ]),
        FormationPack(168, [
            formations_dict[286],
            formations_dict[286],
            formations_dict[286],
        ]),
        FormationPack(169, [
            formations_dict[287],
            formations_dict[287],
            formations_dict[287],
        ]),
        FormationPack(171, [
            formations_dict[289],
            formations_dict[289],
            formations_dict[289],
        ]),
        FormationPack(172, [
            formations_dict[293],
            formations_dict[293],
            formations_dict[293],
        ]),
        FormationPack(173, [
            formations_dict[294],
            formations_dict[294],
            formations_dict[294],
        ]),
        FormationPack(174, [
            formations_dict[295],
            formations_dict[295],
            formations_dict[295],
        ]),
        FormationPack(175, [
            formations_dict[297],
            formations_dict[297],
            formations_dict[297],
        ]),
        FormationPack(176, [
            formations_dict[298],
            formations_dict[298],
            formations_dict[298],
        ]),
        FormationPack(177, [
            formations_dict[299],
            formations_dict[299],
            formations_dict[299],
        ]),
        FormationPack(178, [
            formations_dict[301],
            formations_dict[301],
            formations_dict[301],
        ]),
        FormationPack(179, [
            formations_dict[302],
            formations_dict[302],
            formations_dict[302],
        ]),
        FormationPack(180, [
            formations_dict[303],
            formations_dict[303],
            formations_dict[303],
        ]),
        FormationPack(181, [
            formations_dict[305],
            formations_dict[305],
            formations_dict[305],
        ]),
        FormationPack(182, [
            formations_dict[304],
            formations_dict[304],
            formations_dict[304],
        ]),
        FormationPack(183, [
            formations_dict[315],
            formations_dict[315],
            formations_dict[315],
        ]),
        FormationPack(184, [
            formations_dict[309],
            formations_dict[309],
            formations_dict[309],
        ]),
        FormationPack(185, [
            formations_dict[308],
            formations_dict[308],
            formations_dict[308],
        ]),
        FormationPack(186, [
            formations_dict[307],
            formations_dict[307],
            formations_dict[307],
        ]),
        FormationPack(187, [
            formations_dict[333],
            formations_dict[333],
            formations_dict[333],
        ]),
        FormationPack(188, [
            formations_dict[334],
            formations_dict[334],
            formations_dict[334],
        ]),
        FormationPack(189, [
            formations_dict[335],
            formations_dict[335],
            formations_dict[335],
        ]),
        FormationPack(190, [
            formations_dict[352],
            formations_dict[353],
            formations_dict[352],
        ]),
        FormationPack(191, [
            formations_dict[355],
            formations_dict[355],
            formations_dict[355],
        ]),
        FormationPack(206, [
            formations_dict[354],
            formations_dict[354],
            formations_dict[354],
        ]),
        FormationPack(207, [
            formations_dict[351],
            formations_dict[351],
            formations_dict[351],
        ]),
        FormationPack(208, [
            formations_dict[356],
            formations_dict[356],
            formations_dict[356],
        ]),
        FormationPack(209, [
            formations_dict[357],
            formations_dict[357],
            formations_dict[357],
        ]),
        FormationPack(210, [
            formations_dict[358],
            formations_dict[358],
            formations_dict[358],
        ]),
        FormationPack(211, [
            formations_dict[359],
            formations_dict[359],
            formations_dict[359],
        ]),
        FormationPack(212, [
            formations_dict[360],
            formations_dict[360],
            formations_dict[360],
        ]),
        FormationPack(213, [
            formations_dict[361],
            formations_dict[361],
            formations_dict[361],
        ]),
        FormationPack(214, [
            formations_dict[362],
            formations_dict[370],
            formations_dict[362],
        ]),
        FormationPack(215, [
            formations_dict[363],
            formations_dict[363],
            formations_dict[363],
        ]),
        FormationPack(216, [
            formations_dict[350],
            formations_dict[350],
            formations_dict[350],
        ]),
        FormationPack(224, [
            formations_dict[371],
            formations_dict[371],
            formations_dict[371],
        ]),
        FormationPack(225, [
            formations_dict[372],
            formations_dict[372],
            formations_dict[372],
        ]),
        FormationPack(226, [
            formations_dict[373],
            formations_dict[373],
            formations_dict[373],
        ]),
        FormationPack(227, [
            formations_dict[374],
            formations_dict[374],
            formations_dict[374],
        ]),
        FormationPack(228, [
            formations_dict[375],
            formations_dict[375],
            formations_dict[375],
        ]),
        FormationPack(229, [
            formations_dict[376],
            formations_dict[376],
            formations_dict[376],
        ]),
        FormationPack(230, [
            formations_dict[377],
            formations_dict[377],
            formations_dict[377],
        ]),
        FormationPack(231, [
            formations_dict[378],
            formations_dict[378],
            formations_dict[378],
        ]),
        FormationPack(232, [
            formations_dict[379],
            formations_dict[379],
            formations_dict[379],
        ]),
        FormationPack(233, [
            formations_dict[380],
            formations_dict[380],
            formations_dict[380],
        ]),
        FormationPack(234, [
            formations_dict[381],
            formations_dict[381],
            formations_dict[381],
        ]),
        FormationPack(235, [
            formations_dict[271],
            formations_dict[271],
            formations_dict[271],
        ]),
        FormationPack(236, [
            formations_dict[382],
            formations_dict[382],
            formations_dict[382],
        ]),
        FormationPack(237, [
            formations_dict[383],
            formations_dict[383],
            formations_dict[383],
        ]),
        FormationPack(238, [
            formations_dict[384],
            formations_dict[384],
            formations_dict[384],
        ]),
        FormationPack(239, [
            formations_dict[385],
            formations_dict[385],
            formations_dict[385],
        ]),
        FormationPack(240, [
            formations_dict[386],
            formations_dict[386],
            formations_dict[386],
        ]),
        FormationPack(241, [
            formations_dict[387],
            formations_dict[387],
            formations_dict[387],
        ]),
        FormationPack(242, [
            formations_dict[388],
            formations_dict[388],
            formations_dict[388],
        ]),
        FormationPack(243, [
            formations_dict[389],
            formations_dict[389],
            formations_dict[389],
        ]),
        FormationPack(244, [
            formations_dict[390],
            formations_dict[390],
            formations_dict[390],
        ]),
        FormationPack(245, [
            formations_dict[391],
            formations_dict[391],
            formations_dict[391],
        ]),
        FormationPack(246, [
            formations_dict[392],
            formations_dict[392],
            formations_dict[392],
        ]),
        FormationPack(247, [
            formations_dict[393],
            formations_dict[393],
            formations_dict[393],
        ]),
    ]

    # Get leaders for each formation based on common enemies in packs.
    for p in formation_packs:
        common_enemies = set(p.common_enemies)
        for f in p.formations:
            f.leaders |= common_enemies

    for f in formations:
        if not f.leaders:
            f.leaders = [m.enemy for m in f.members]
        f.leaders = sorted(f.leaders, key=lambda m: m.index)

    return formations, formation_packs
