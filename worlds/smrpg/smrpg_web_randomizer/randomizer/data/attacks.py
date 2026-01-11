# Data module for enemy attack data.

from ...randomizer.logic import utils
from ...randomizer.logic.patch import Patch


class EnemyAttack:
    """Class representing an enemy attack."""
    BASE_ADDRESS = 0x391226

    # Default instance attributes.
    index = 0
    attack_level = 0
    damage_types = []
    hit_rate = 0
    status_effects = []
    buffs = []

    def __init__(self, world):
        """

        Args:
            world (randomizer.logic.main.GameWorld):

        """
        self.world = world

    def __str__(self):
        return "<{}>".format(self.name)

    def __repr__(self):
        return str(self)

    @property
    def name(self):
        return self.__class__.__name__

    def get_patch(self):
        """Get patch for this item.

        :return: Patch data.
        :rtype: randomizer.logic.patch.Patch
        """
        patch = Patch()
        base_addr = self.BASE_ADDRESS + (self.index * 4)

        data = bytearray()

        # First byte is attack level + damage type flags in a bitmap.
        attack_flags = [i for i in range(3) if self.attack_level & (1 << i)]
        attack_flags += self.damage_types
        data += utils.BitMapSet(1, attack_flags).as_bytes()

        # Other bytes are hit rate, status effects, and buffs.
        data += utils.ByteField(self.hit_rate).as_bytes()
        data += utils.BitMapSet(1, self.status_effects).as_bytes()
        data += utils.BitMapSet(1, self.buffs).as_bytes()

        patch.add_data(base_addr, data)
        return patch


# ********************* Actual data classes

class PhysicalAttack0(EnemyAttack):
    index = 0
    hit_rate = 95


class PhysicalAttack2(EnemyAttack):
    index = 2
    hit_rate = 95


class PhysicalAttack4(EnemyAttack):
    index = 4
    hit_rate = 95


class PhysicalAttack5(EnemyAttack):
    index = 5
    hit_rate = 95


class PhysicalAttack6(EnemyAttack):
    index = 6
    hit_rate = 95


class PhysicalAttack7(EnemyAttack):
    index = 7
    hit_rate = 95


class PhysicalAttack8(EnemyAttack):
    index = 8
    hit_rate = 95


class PhysicalAttack9(EnemyAttack):
    index = 9
    hit_rate = 95


class PhysicalAttack10(EnemyAttack):
    index = 10
    hit_rate = 95


class PhysicalAttack11(EnemyAttack):
    index = 11
    hit_rate = 95


class PhysicalAttack12(EnemyAttack):
    index = 12
    hit_rate = 95


class PhysicalAttack15(EnemyAttack):
    index = 15
    hit_rate = 95


class Thornet(EnemyAttack):
    index = 17
    attack_level = 1
    hit_rate = 95
    status_effects = [2]


class PhysicalAttack18(EnemyAttack):
    index = 18
    attack_level = 3
    hit_rate = 90


class Funguspike(EnemyAttack):
    index = 19
    attack_level = 2
    hit_rate = 95
    status_effects = [5]


class PhysicalAttack20(EnemyAttack):
    index = 20
    attack_level = 1
    hit_rate = 95


class PhysicalAttack21(EnemyAttack):
    index = 21
    attack_level = 2
    hit_rate = 95


class FullHouse(EnemyAttack):
    index = 22
    attack_level = 2
    hit_rate = 95


class WildCard(EnemyAttack):
    index = 23
    attack_level = 3
    hit_rate = 95


class RoyalFlush(EnemyAttack):
    index = 24
    attack_level = 4
    hit_rate = 90


class SpritzBomb(EnemyAttack):
    index = 26
    attack_level = 2
    hit_rate = 90


class PhysicalAttack27(EnemyAttack):
    index = 27
    attack_level = 1
    hit_rate = 95


class PhysicalAttack28(EnemyAttack):
    index = 28
    attack_level = 1
    hit_rate = 95


class PhysicalAttack29(EnemyAttack):
    index = 29
    hit_rate = 95


class Blazer(EnemyAttack):
    index = 30
    damage_types = [3, 5]
    hit_rate = 90


class PhysicalAttack31(EnemyAttack):
    index = 31
    attack_level = 2
    hit_rate = 95


class PhysicalAttack32(EnemyAttack):
    index = 32
    attack_level = 2
    hit_rate = 95


class Echofinder(EnemyAttack):
    index = 33
    attack_level = 1
    hit_rate = 95
    status_effects = [0]


class ScrowBell(EnemyAttack):
    index = 34
    damage_types = [4, 5, 6]
    hit_rate = 90
    status_effects = [6]


class DoomReverb(EnemyAttack):
    index = 35
    damage_types = [4, 5, 6]
    hit_rate = 90
    status_effects = [0]


class SporeChimes(EnemyAttack):
    index = 36
    damage_types = [4, 5, 6]
    hit_rate = 90
    status_effects = [5]


class InkBlast(EnemyAttack):
    index = 37
    attack_level = 1
    hit_rate = 95


class GunkBall(EnemyAttack):
    index = 38
    attack_level = 1
    hit_rate = 95
    status_effects = [0]


class Endobubble(EnemyAttack):
    index = 39
    damage_types = [4, 5, 6]
    hit_rate = 90
    status_effects = [3]


class PhysicalAttack40(EnemyAttack):
    index = 40
    attack_level = 1
    hit_rate = 95


class VenomDrool(EnemyAttack):
    index = 42
    damage_types = [5, 6]
    hit_rate = 95
    status_effects = [2]


class MushFunk(EnemyAttack):
    index = 43
    damage_types = [4, 5, 6]
    hit_rate = 90
    status_effects = [5]


class Stench(EnemyAttack):
    index = 45
    damage_types = [5, 6]
    hit_rate = 90
    status_effects = [2]


class PhysicalAttack46(EnemyAttack):
    index = 46
    attack_level = 1
    hit_rate = 95


class PhysicalAttack47(EnemyAttack):
    index = 47
    attack_level = 2
    hit_rate = 90
    status_effects = [3]


class ViroPlasm(EnemyAttack):
    index = 48
    damage_types = [5, 6]
    hit_rate = 90
    status_effects = [2]


class PsychoPlasm(EnemyAttack):
    index = 49
    damage_types = [5, 6]
    hit_rate = 90
    status_effects = [3]


class PhysicalAttack50(EnemyAttack):
    index = 50
    damage_types = [5, 6]
    hit_rate = 90
    status_effects = [0]


class PhysicalAttack51(EnemyAttack):
    index = 51
    damage_types = [5, 6]
    hit_rate = 90
    status_effects = [1]


class PollenNap(EnemyAttack):
    index = 52
    damage_types = [5, 6]
    hit_rate = 90
    status_effects = [1]


class ScrowDust(EnemyAttack):
    index = 53
    damage_types = [5, 6]
    hit_rate = 90
    status_effects = [6]


class Sporocyst(EnemyAttack):
    index = 54
    damage_types = [5, 6]
    hit_rate = 90
    status_effects = [5]


class Toxicyst(EnemyAttack):
    index = 55
    damage_types = [5, 6]
    hit_rate = 90
    status_effects = [2]


class PhysicalAttack56(EnemyAttack):
    index = 56
    attack_level = 1
    hit_rate = 95


class PhysicalAttack57(EnemyAttack):
    index = 57
    attack_level = 2
    hit_rate = 90


class LullaBye(EnemyAttack):
    index = 58
    damage_types = [4, 5, 6]
    hit_rate = 99
    status_effects = [1]


class Elegy(EnemyAttack):
    index = 59
    damage_types = [4, 5, 6]
    hit_rate = 99
    status_effects = [0]


class Backfire(EnemyAttack):
    index = 60
    hit_rate = 95


class VaVaVoom(EnemyAttack):
    index = 61
    attack_level = 1
    hit_rate = 95


class FunRun(EnemyAttack):
    index = 62
    attack_level = 1
    hit_rate = 95


class BodySlam(EnemyAttack):
    index = 63
    attack_level = 2
    hit_rate = 95


class Howl(EnemyAttack):
    index = 64
    damage_types = [4, 5, 6]
    hit_rate = 99
    status_effects = [3]


class Scream(EnemyAttack):
    index = 65
    damage_types = [4, 5, 6]
    hit_rate = 99
    status_effects = [3]


class IronMaiden(EnemyAttack):
    index = 66
    damage_types = [4, 5, 6]
    hit_rate = 99
    status_effects = [3]


class Fangs(EnemyAttack):
    index = 67
    attack_level = 1
    hit_rate = 95


class Poison(EnemyAttack):
    index = 68
    attack_level = 1
    hit_rate = 95
    status_effects = [2]


class CarniKiss(EnemyAttack):
    index = 69
    attack_level = 2
    hit_rate = 95


class Claw(EnemyAttack):
    index = 70
    attack_level = 2
    hit_rate = 95


class Grinder(EnemyAttack):
    index = 71
    attack_level = 2
    hit_rate = 95


class DarkClaw(EnemyAttack):
    index = 72
    attack_level = 1
    hit_rate = 95
    status_effects = [2]


class Scythe(EnemyAttack):
    index = 73
    damage_types = [3, 5]
    hit_rate = 90


class Sickle(EnemyAttack):
    index = 74
    attack_level = 1
    hit_rate = 95
    status_effects = [6]


class Deathsickle(EnemyAttack):
    index = 75
    attack_level = 2
    hit_rate = 95
    status_effects = [3]


class EerieJig(EnemyAttack):
    index = 76
    damage_types = [5, 6]
    hit_rate = 99
    status_effects = [6]


class SomnusWaltz(EnemyAttack):
    index = 77
    damage_types = [5, 6]
    hit_rate = 99
    status_effects = [1]


class DahliaDance(EnemyAttack):
    index = 78
    damage_types = [5, 6]
    hit_rate = 99
    status_effects = [5]


class Skewer(EnemyAttack):
    index = 79
    attack_level = 1
    hit_rate = 95


class Pierce(EnemyAttack):
    index = 80
    attack_level = 2
    hit_rate = 90


class PhysicalAttack81(EnemyAttack):
    index = 81
    hit_rate = 95


class Magnum(EnemyAttack):
    index = 82
    damage_types = [3, 5]
    hit_rate = 90


class Psyche(EnemyAttack):
    index = 83
    damage_types = [3, 5]
    hit_rate = 80


class Migraine(EnemyAttack):
    index = 84
    damage_types = [3, 5]
    hit_rate = 80


class PhysicalAttack85(EnemyAttack):
    index = 85
    hit_rate = 99


class PhysicalAttack86(EnemyAttack):
    index = 86
    attack_level = 2
    hit_rate = 95


class Multistrike(EnemyAttack):
    index = 87
    attack_level = 1
    hit_rate = 95


class FlutterHush(EnemyAttack):
    index = 88
    damage_types = [5, 6]
    hit_rate = 90
    status_effects = [0]


class PhysicalAttack89(EnemyAttack):
    index = 89
    hit_rate = 95


class PhysicalAttack90(EnemyAttack):
    index = 90
    hit_rate = 95


class PhysicalAttack91(EnemyAttack):
    index = 91
    damage_types = [5, 6]
    hit_rate = 85
    status_effects = [1]


class FearRoulette(EnemyAttack):
    index = 92
    damage_types = [3, 5]
    hit_rate = 99


class PhysicalAttack93(EnemyAttack):
    index = 93
    hit_rate = 95


class PhysicalAttack94(EnemyAttack):
    index = 94
    hit_rate = 95


class PhysicalAttack95(EnemyAttack):
    index = 95
    hit_rate = 95


class ValorUp(EnemyAttack):
    index = 97
    damage_types = [5, 6]
    hit_rate = 100
    buffs = [5, 6]


class LastShot(EnemyAttack):
    index = 99
    attack_level = 3
    hit_rate = 100


class PhysicalAttack101(EnemyAttack):
    index = 101
    attack_level = 1
    hit_rate = 90


class PhysicalAttack105(EnemyAttack):
    index = 105
    hit_rate = 95


class Gnight(EnemyAttack):
    index = 106
    damage_types = [5, 6]
    hit_rate = 90
    status_effects = [1]


class PhysicalAttack107(EnemyAttack):
    index = 107
    hit_rate = 95


class PhysicalAttack108(EnemyAttack):
    index = 108
    hit_rate = 100


class Chomp(EnemyAttack):
    index = 109
    attack_level = 2
    hit_rate = 90


class GetTough(EnemyAttack):
    index = 110
    damage_types = [5, 6]
    hit_rate = 100
    buffs = [5, 6]


class PhysicalAttack111(EnemyAttack):
    index = 111
    hit_rate = 95


class Missedme(EnemyAttack):
    index = 112
    damage_types = [5, 6]
    hit_rate = 95


class PhysicalAttack113(EnemyAttack):
    index = 113
    attack_level = 1
    hit_rate = 95


class LocoExpress(EnemyAttack):
    index = 114
    attack_level = 3
    hit_rate = 90


class PhysicalAttack115(EnemyAttack):
    index = 115
    hit_rate = 95


class PhysicalAttack116(EnemyAttack):
    index = 116
    attack_level = 1
    hit_rate = 90


class PhysicalAttack117(EnemyAttack):
    index = 117
    hit_rate = 95


class PhysicalAttack118(EnemyAttack):
    index = 118
    hit_rate = 95


class Jinxed(EnemyAttack):
    index = 119
    hit_rate = 100


class TripleKick(EnemyAttack):
    index = 120
    attack_level = 1
    hit_rate = 95


class Quicksilver(EnemyAttack):
    index = 121
    attack_level = 2
    hit_rate = 90


class BombsAway(EnemyAttack):
    index = 122
    attack_level = 3
    hit_rate = 90


class Vigorup(EnemyAttack):
    index = 123
    damage_types = [5, 6]
    hit_rate = 100
    buffs = [3, 4]


class SilverBullet(EnemyAttack):
    index = 125
    damage_types = [3, 5]
    hit_rate = 99


class Terrapunch(EnemyAttack):
    index = 126
    attack_level = 2
    hit_rate = 95


class ScrowFangs(EnemyAttack):
    index = 127
    damage_types = [5, 6]
    hit_rate = 85
    status_effects = [6]


class Shaker(EnemyAttack):
    index = 128
    damage_types = [3, 5]
    hit_rate = 99


# ********************* Default lists for the world.

def get_default_enemy_attacks(world):
    """

    Args:
        world (randomizer.logic.main.GameWorld):

    Returns:
        list[EnemyAttack]: Default list of objects for the world.

    """
    return [
        PhysicalAttack0(world),
        PhysicalAttack2(world),
        PhysicalAttack4(world),
        PhysicalAttack5(world),
        PhysicalAttack6(world),
        PhysicalAttack7(world),
        PhysicalAttack8(world),
        PhysicalAttack9(world),
        PhysicalAttack10(world),
        PhysicalAttack11(world),
        PhysicalAttack12(world),
        PhysicalAttack15(world),
        Thornet(world),
        PhysicalAttack18(world),
        Funguspike(world),
        PhysicalAttack20(world),
        PhysicalAttack21(world),
        FullHouse(world),
        WildCard(world),
        RoyalFlush(world),
        SpritzBomb(world),
        PhysicalAttack27(world),
        PhysicalAttack28(world),
        PhysicalAttack29(world),
        Blazer(world),
        PhysicalAttack31(world),
        PhysicalAttack32(world),
        Echofinder(world),
        ScrowBell(world),
        DoomReverb(world),
        SporeChimes(world),
        InkBlast(world),
        GunkBall(world),
        Endobubble(world),
        PhysicalAttack40(world),
        VenomDrool(world),
        MushFunk(world),
        Stench(world),
        PhysicalAttack46(world),
        PhysicalAttack47(world),
        ViroPlasm(world),
        PsychoPlasm(world),
        PhysicalAttack50(world),
        PhysicalAttack51(world),
        PollenNap(world),
        ScrowDust(world),
        Sporocyst(world),
        Toxicyst(world),
        PhysicalAttack56(world),
        PhysicalAttack57(world),
        LullaBye(world),
        Elegy(world),
        Backfire(world),
        VaVaVoom(world),
        FunRun(world),
        BodySlam(world),
        Howl(world),
        Scream(world),
        IronMaiden(world),
        Fangs(world),
        Poison(world),
        CarniKiss(world),
        Claw(world),
        Grinder(world),
        DarkClaw(world),
        Scythe(world),
        Sickle(world),
        Deathsickle(world),
        EerieJig(world),
        SomnusWaltz(world),
        DahliaDance(world),
        Skewer(world),
        Pierce(world),
        PhysicalAttack81(world),
        Magnum(world),
        Psyche(world),
        Migraine(world),
        PhysicalAttack85(world),
        PhysicalAttack86(world),
        Multistrike(world),
        FlutterHush(world),
        PhysicalAttack89(world),
        PhysicalAttack90(world),
        PhysicalAttack91(world),
        FearRoulette(world),
        PhysicalAttack93(world),
        PhysicalAttack94(world),
        PhysicalAttack95(world),
        ValorUp(world),
        LastShot(world),
        PhysicalAttack101(world),
        PhysicalAttack105(world),
        Gnight(world),
        PhysicalAttack107(world),
        PhysicalAttack108(world),
        Chomp(world),
        GetTough(world),
        PhysicalAttack111(world),
        Missedme(world),
        PhysicalAttack113(world),
        LocoExpress(world),
        PhysicalAttack115(world),
        PhysicalAttack116(world),
        PhysicalAttack117(world),
        PhysicalAttack118(world),
        Jinxed(world),
        TripleKick(world),
        Quicksilver(world),
        BombsAway(world),
        Vigorup(world),
        SilverBullet(world),
        Terrapunch(world),
        ScrowFangs(world),
        Shaker(world),
    ]
