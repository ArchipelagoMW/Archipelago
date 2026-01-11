# Data module for spell data.

from ...randomizer.logic import utils
from ...randomizer.logic.patch import Patch

STARTING_FP = 10


class Spell:
    """Class representing a magic spell to be randomized."""
    BASE_ADDRESS = 0x3a20f1

    # Default per-spell attributes.
    index = 0
    fp = 0
    power = 0
    hit_rate = 0
    instant_ko = False

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
        """Get patch for this spell.

        :return: Patch data.
        :rtype: randomizer.logic.patch.Patch
        """
        patch = Patch()

        # FP is byte 3, power is byte 6, hit rate is byte 7.  Each spell is 12 bytes.
        base_addr = self.BASE_ADDRESS + (self.index * 12)
        patch.add_data(base_addr + 2, utils.ByteField(self.fp).as_bytes())
        data = utils.ByteField(self.power).as_bytes()
        data += utils.ByteField(self.hit_rate).as_bytes()
        patch.add_data(base_addr + 5, data)

        return patch


class CharacterSpell(Spell):
    """Grouping class for character-specific spells."""
    pass


class EnemySpell(Spell):
    """Grouping class for enemy-specific spells."""
    status_effects = []

    def get_patch(self):
        """Get patch for this spell.

        Returns:
            randomizer.logic.patch.Patch: Patch data.

        """
        patch = super().get_patch()

        # Add status effects for enemy attacks, if any.
        base_addr = self.BASE_ADDRESS + (self.index * 12)
        data = utils.BitMapSet(1, self.status_effects).as_bytes()
        patch.add_data(base_addr + 7, data)

        return patch


# ********************* Actual data classes

class Jump(CharacterSpell):
    index = 0
    fp = 3
    power = 25
    hit_rate = 100


class FireOrb(CharacterSpell):
    index = 1
    fp = 5
    power = 20
    hit_rate = 100


class SuperJump(CharacterSpell):
    index = 2
    fp = 7
    power = 45
    hit_rate = 100


class SuperFlame(CharacterSpell):
    index = 3
    fp = 9
    power = 40
    hit_rate = 100


class UltraJump(CharacterSpell):
    index = 4
    fp = 11
    power = 65
    hit_rate = 100


class UltraFlame(CharacterSpell):
    index = 5
    fp = 14
    power = 60
    hit_rate = 100


class Therapy(CharacterSpell):
    index = 6
    fp = 2
    power = 40
    hit_rate = 100


class GroupHug(CharacterSpell):
    index = 7
    fp = 4
    power = 30
    hit_rate = 100


class SleepyTime(CharacterSpell):
    index = 8
    fp = 4
    hit_rate = 99


class ComeBack(CharacterSpell):
    index = 9
    fp = 2
    hit_rate = 100


class Mute(CharacterSpell):
    index = 10
    fp = 3
    hit_rate = 99


class PsychBomb(CharacterSpell):
    index = 11
    fp = 15
    power = 60
    hit_rate = 100


class Terrorize(CharacterSpell):
    index = 12
    fp = 6
    power = 10
    hit_rate = 90


class PoisonGas(CharacterSpell):
    index = 13
    fp = 10
    power = 20
    hit_rate = 90


class Crusher(CharacterSpell):
    index = 14
    fp = 12
    power = 60
    hit_rate = 100


class BowserCrush(CharacterSpell):
    index = 15
    fp = 16
    power = 58
    hit_rate = 100


class GenoBeam(CharacterSpell):
    index = 16
    fp = 3
    power = 40
    hit_rate = 100


class GenoBoost(CharacterSpell):
    index = 17
    fp = 4
    hit_rate = 100


class GenoWhirl(CharacterSpell):
    index = 18
    fp = 8
    power = 45
    hit_rate = 100


class GenoBlast(CharacterSpell):
    index = 19
    fp = 12
    power = 50
    hit_rate = 100


class GenoFlash(CharacterSpell):
    index = 20
    fp = 16
    power = 60
    hit_rate = 100


class Thunderbolt(CharacterSpell):
    index = 21
    fp = 2
    power = 15
    hit_rate = 100


class HPRain(CharacterSpell):
    index = 22
    fp = 2
    power = 10
    hit_rate = 100


class Psychopath(CharacterSpell):
    index = 23
    fp = 1
    hit_rate = 100


class Shocker(CharacterSpell):
    index = 24
    fp = 8
    power = 60
    hit_rate = 100


class Snowy(CharacterSpell):
    index = 25
    fp = 12
    power = 40
    hit_rate = 100


class StarRain(CharacterSpell):
    index = 26
    fp = 14
    power = 55
    hit_rate = 100


class Drain(EnemySpell):
    index = 64
    fp = 1
    power = 4
    hit_rate = 90


class LightningOrb(EnemySpell):
    index = 65
    fp = 2
    power = 8
    hit_rate = 90


class Flame(EnemySpell):
    index = 66
    fp = 3
    power = 12
    hit_rate = 90


class Bolt(EnemySpell):
    index = 67
    fp = 4
    power = 20
    hit_rate = 90


class Crystal(EnemySpell):
    index = 68
    fp = 5
    power = 25
    hit_rate = 90


class FlameStone(EnemySpell):
    index = 69
    fp = 6
    power = 32
    hit_rate = 90


class MegaDrain(EnemySpell):
    index = 70
    fp = 7
    power = 40
    hit_rate = 90


class WillyWisp(EnemySpell):
    index = 71
    fp = 8
    power = 48
    hit_rate = 90


class DiamondSaw(EnemySpell):
    index = 72
    fp = 9
    power = 60
    hit_rate = 90


class Electroshock(EnemySpell):
    index = 73
    fp = 10
    power = 72
    hit_rate = 90


class Blast(EnemySpell):
    index = 74
    fp = 11
    power = 89
    hit_rate = 90


class Storm(EnemySpell):
    index = 75
    fp = 12
    power = 108
    hit_rate = 90


class IceRock(EnemySpell):
    index = 76
    fp = 13
    power = 130
    hit_rate = 90


class Escape(EnemySpell):
    index = 77
    hit_rate = 100


class DarkStar(EnemySpell):
    index = 78
    fp = 20
    power = 160
    hit_rate = 90


class Recover(EnemySpell):
    index = 79
    fp = 3
    power = 50
    hit_rate = 100


class MegaRecover(EnemySpell):
    index = 80
    fp = 9
    power = 200
    hit_rate = 100


class FlameWall(EnemySpell):
    index = 81
    fp = 2
    power = 8
    hit_rate = 90


class StaticE(EnemySpell):
    index = 82
    fp = 4
    power = 12
    hit_rate = 90


class SandStorm(EnemySpell):
    index = 83
    fp = 6
    power = 16
    hit_rate = 90
    status_effects = [3]


class Blizzard(EnemySpell):
    index = 84
    fp = 8
    power = 22
    hit_rate = 90


class DrainBeam(EnemySpell):
    index = 85
    fp = 10
    power = 26
    hit_rate = 90


class MeteorBlast(EnemySpell):
    index = 86
    fp = 12
    power = 30
    hit_rate = 90


class LightBeam(EnemySpell):
    index = 87
    fp = 13
    power = 34
    hit_rate = 90
    status_effects = [1]


class WaterBlast(EnemySpell):
    index = 88
    fp = 14
    power = 39
    hit_rate = 90


class Solidify(EnemySpell):
    index = 89
    fp = 15
    power = 47
    hit_rate = 90


class PetalBlast(EnemySpell):
    index = 90
    fp = 16
    power = 40
    hit_rate = 85
    status_effects = [5]


class AuroraFlash(EnemySpell):
    index = 91
    fp = 17
    power = 50
    hit_rate = 85
    status_effects = [1]


class Boulder(EnemySpell):
    index = 92
    fp = 18
    power = 72
    hit_rate = 90


class Corona(EnemySpell):
    index = 93
    fp = 19
    power = 88
    hit_rate = 90


class MeteorSwarm(EnemySpell):
    index = 94
    fp = 20
    power = 100
    hit_rate = 90


class KnockOut(EnemySpell):
    index = 95
    fp = 15
    power = 1
    hit_rate = 60
    instant_ko = True


class WeirdMushroom(EnemySpell):
    index = 96
    power = 30
    hit_rate = 100


class BreakerBeam(EnemySpell):
    index = 97
    fp = 15
    power = 80
    hit_rate = 90


class Shredder(EnemySpell):
    index = 98
    fp = 8
    hit_rate = 100


class Sledge(EnemySpell):
    index = 99
    fp = 6
    power = 50
    hit_rate = 99


class SwordRain(EnemySpell):
    index = 100
    fp = 8
    power = 80
    hit_rate = 99


class SpearRain(EnemySpell):
    index = 101
    fp = 5
    power = 60
    hit_rate = 99


class ArrowRain(EnemySpell):
    index = 102
    fp = 2
    power = 40
    hit_rate = 99

class BigBang(EnemySpell):
    index = 103
    power = 100
    hit_rate = 100

class ChestScrow(EnemySpell):
    index = 104
    power = 0
    hit_rate = 85

class ChestFear(EnemySpell):
    index = 105
    power = 0
    hit_rate = 82

class ChestMute(EnemySpell):
    index = 106
    power = 0
    hit_rate = 85

class ChestPoison(EnemySpell):
    index = 107
    power = 0
    hit_rate = 85

class ChainSaw(EnemySpell):
    index = 108
    power = 50
    hit_rate = 90

class Nothing(EnemySpell):
    index = 251
    power = 0
    hit_rate = 100


# ********************* Default lists for the world.

def get_default_spells(world):
    """Get default vanilla item list for the world.

    Args:
        world (randomizer.logic.main.GameWorld):

    Returns:
        list[Spell]: List of default spell objects.

    """
    return [
        Jump(world),
        FireOrb(world),
        SuperJump(world),
        SuperFlame(world),
        UltraJump(world),
        UltraFlame(world),
        Therapy(world),
        GroupHug(world),
        SleepyTime(world),
        ComeBack(world),
        Mute(world),
        PsychBomb(world),
        Terrorize(world),
        PoisonGas(world),
        Crusher(world),
        BowserCrush(world),
        GenoBeam(world),
        GenoBoost(world),
        GenoWhirl(world),
        GenoBlast(world),
        GenoFlash(world),
        Thunderbolt(world),
        HPRain(world),
        Psychopath(world),
        Shocker(world),
        Snowy(world),
        StarRain(world),
        Drain(world),
        LightningOrb(world),
        Flame(world),
        Bolt(world),
        Crystal(world),
        FlameStone(world),
        MegaDrain(world),
        WillyWisp(world),
        DiamondSaw(world),
        Electroshock(world),
        Blast(world),
        Storm(world),
        IceRock(world),
        Escape(world),
        DarkStar(world),
        Recover(world),
        MegaRecover(world),
        FlameWall(world),
        StaticE(world),
        SandStorm(world),
        Blizzard(world),
        DrainBeam(world),
        MeteorBlast(world),
        LightBeam(world),
        WaterBlast(world),
        Solidify(world),
        PetalBlast(world),
        AuroraFlash(world),
        Boulder(world),
        Corona(world),
        MeteorSwarm(world),
        KnockOut(world),
        WeirdMushroom(world),
        BreakerBeam(world),
        Shredder(world),
        Sledge(world),
        SwordRain(world),
        SpearRain(world),
        ArrowRain(world),
        BigBang(world),
        # ChestScrow(world),
        # ChestFear(world),
        # ChestMute(world),
        # ChestPoison(world),
        ChainSaw(world),
        # Nothing(world),
    ]

# BigBang is not in any of these tables. It's just a bad idea.
SingleTargets = [Drain, LightningOrb, Flame, Bolt, Crystal, FlameStone, MegaDrain, WillyWisp, DiamondSaw, Electroshock, Blast, Storm, IceRock, DarkStar]
Heals = [Recover, MegaRecover, WeirdMushroom]
MultiTargets = [FlameWall, StaticE, SandStorm, Blizzard, DrainBeam, MeteorBlast, LightBeam, WaterBlast, Solidify, PetalBlast, AuroraFlash, Boulder, Corona, MeteorSwarm, KnockOut, Shredder, Sledge, SwordRain, SpearRain, ArrowRain, ChestScrow, ChestFear, ChestMute, ChestPoison, ChainSaw]
DoNothing = [Nothing]
Run = [Escape]

SpellsToTargets = {
    Drain.index: SingleTargets,
    LightningOrb.index: SingleTargets,
    Flame.index: SingleTargets,
    Bolt.index: SingleTargets,
    Crystal.index: SingleTargets,
    FlameStone.index: SingleTargets,
    MegaDrain.index: SingleTargets,
    WillyWisp.index: SingleTargets,
    DiamondSaw.index: SingleTargets,
    Electroshock.index: SingleTargets,
    Blast.index: SingleTargets,
    Storm.index: SingleTargets,
    IceRock.index: SingleTargets,
    DarkStar.index: SingleTargets,

    Recover.index: Heals,
    MegaRecover.index: Heals,
    WeirdMushroom.index: Heals,

    FlameWall.index: MultiTargets,
    StaticE.index: MultiTargets,
    SandStorm.index: MultiTargets,
    Blizzard.index: MultiTargets,
    DrainBeam.index: MultiTargets,
    MeteorBlast.index: MultiTargets,
    LightBeam.index: MultiTargets,
    WaterBlast.index: MultiTargets,
    Solidify.index: MultiTargets,
    PetalBlast.index: MultiTargets,
    AuroraFlash.index: MultiTargets,
    Boulder.index: MultiTargets,
    Corona.index: MultiTargets,
    MeteorSwarm.index: MultiTargets,
    KnockOut.index: MultiTargets,
    Shredder.index: MultiTargets,
    Sledge.index: MultiTargets,
    SwordRain.index: MultiTargets,
    SpearRain.index: MultiTargets,
    ArrowRain.index: MultiTargets,
    ChestScrow.index: MultiTargets,
    ChestFear.index: MultiTargets,
    ChestMute.index: MultiTargets,
    ChestPoison.index: MultiTargets,
    ChainSaw.index: MultiTargets,

    # These can really only be done by their specific casters
    BreakerBeam.index: [BreakerBeam] + MultiTargets,
    BigBang.index: [BigBang] + MultiTargets,

    Nothing.index: DoNothing,
    Escape.index: Run,
}
