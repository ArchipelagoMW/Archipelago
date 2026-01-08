"""
Functions used to describe Metroid: Zero Mission logic rules
"""

from __future__ import annotations

import builtins
import functools
from typing import TYPE_CHECKING, Any, Callable, NamedTuple
from BaseClasses import CollectionState

if TYPE_CHECKING:
    from . import MZMWorld


class Requirement(NamedTuple):
    rule: Callable[[MZMWorld, CollectionState], bool]

    def create_rule(self, world: MZMWorld):
        return functools.partial(self.rule, world)

    @classmethod
    def item(cls, item: str, count: int = 1):
        return cls(lambda world, state: state.has(item, world.player, count))

    @classmethod
    def location(cls, location: str):
        return cls(lambda world, state: state.can_reach_location(location, world.player))

    @classmethod
    def entrance(cls, entrance: str):
        return cls(lambda world, state: state.can_reach_entrance(entrance, world.player))

    @classmethod
    def setting_enabled(cls, setting: str):
        return cls(lambda world, _: getattr(world.options, setting))

    @classmethod
    def setting_is(cls, setting: str, value: Any):
        return cls(lambda world, _: getattr(world.options, setting) == value)

    @classmethod
    def setting_atleast(cls, setting: str, value: int):
        return cls(lambda world, _: getattr(world.options, setting) >= value)

    @classmethod
    def setting_contains(cls, setting: str, value: Any):
        return cls(lambda world, _: value in getattr(world.options, setting))

    @classmethod
    def has_metroid_dna(cls):
        return cls(lambda world, state: state.has("Metroid DNA", world.player, world.options.metroid_dna_required.value))

    @classmethod
    def trick_enabled(cls, trick: str):
        return cls(lambda world, _: trick in world.trick_allow_list)

    @classmethod
    def trick_rule(cls, trick: str):
        from .tricks import all_tricks
        return all_tricks[trick]


def all(*args: Requirement):
    return Requirement(lambda world, state: builtins.all(req.rule(world, state) for req in args))


def any(*args: Requirement):
    return Requirement(lambda world, state: builtins.any(req.rule(world, state) for req in args))


Ziplines = Requirement.item("Ziplines Activated")
KraidBoss = Requirement.item("Kraid Defeated")
RidleyBoss = Requirement.item("Ridley Defeated")
MotherBrainBoss = Requirement.item("Mother Brain Defeated")
ChozoGhostBoss = Requirement.item("Chozo Ghost Defeated")
MechaRidleyBoss = Requirement.item("Mecha Ridley Defeated")
CanReachLocation = lambda n: Requirement.location(n)
CanReachEntrance = lambda n: Requirement.entrance(n)

UnknownItem1 = Requirement.location("Crateria Unknown Item Statue")
UnknownItem2 = Requirement.location("Kraid Unknown Item Statue")
UnknownItem3 = Requirement.location("Ridley Unknown Item Statue")

CanUseUnknownItems = Requirement.item("Fully Powered Suit")
LayoutPatches = lambda n: any(
    Requirement.setting_is("layout_patches", 1),
    all(
        Requirement.setting_is("layout_patches", 2),
        Requirement.setting_contains("selected_patches", n)
    )
)
Trick = lambda n: all(
    Requirement.trick_enabled(n),
    Requirement.trick_rule(n)
)

NormalMode = Requirement.setting_is("game_difficulty", "normal")
HardMode = Requirement.setting_is("game_difficulty", "hard")

CombinedHiJumpAndSpringBall = Requirement.setting_is("spring_ball", False)


EnergyTanks = lambda n: Requirement.item("Energy Tank", n)
MissileTanks = lambda n: Requirement.item("Missile Tank", n)
SuperMissileTanks = lambda n: Requirement.item("Super Missile Tank", n)
PowerBombTanks = lambda n: Requirement.item("Power Bomb Tank", n)
LongBeam = Requirement.item("Long Beam")
ChargeBeam = Requirement.item("Charge Beam")
IceBeam = Requirement.item("Ice Beam")
WaveBeam = Requirement.item("Wave Beam")
PlasmaBeam = all(
    Requirement.item("Plasma Beam"),
    CanUseUnknownItems,
)
Bomb = Requirement.item("Bomb")
VariaSuit = Requirement.item("Varia Suit")
GravitySuit = all(
    Requirement.item("Gravity Suit"),
    CanUseUnknownItems
)
MorphBall = Requirement.item("Morph Ball")
SpeedBooster = Requirement.item("Speed Booster")
HiJump = Requirement.item("Hi-Jump")
ScrewAttack = Requirement.item("Screw Attack")
SpaceJump = all(
    Requirement.item("Space Jump"),
    CanUseUnknownItems
)
PowerGrip = Requirement.item("Power Grip")
SpringBall = Requirement.item("Spring Ball")

Missiles = any(
    MissileTanks(1),
    SuperMissileTanks(1),
)
MissileCount = lambda n: Requirement(
    lambda world, state:
        5 * state.count("Missile Tank", world.player) +
        2 * state.count("Super Missile Tank", world.player) >= n if world.options.game_difficulty == "normal"
        else 2 * state.count("Missile Tank", world.player) + state.count("Super Missile Tank", world.player) >= n
)
SuperMissiles = SuperMissileTanks(1)
SuperMissileCount = lambda n: Requirement(
    lambda world, state:
        2 * state.count("Super Missile Tank", world.player) >= n if world.options.game_difficulty == "normal"
        else state.count("Super Missile Tank", world.player) >= n
)
PowerBombs = PowerBombTanks(1)
PowerBombCount = lambda n: Requirement(
    lambda world, state:
        2 * state.count("Power Bomb Tank", world.player) >= n if world.options.game_difficulty == "normal"
        else state.count("Power Bomb Tank", world.player) >= n
)
Energy = lambda n: Requirement(
    lambda world, state:
        100 * state.count("Energy Tank", world.player) + 99 >= n if world.options.game_difficulty == "normal"
        else 50 * state.count("Energy Tank", world.player) + 99 >= n
)


# Various morph/bomb rules
CanRegularBomb = all(
    MorphBall,
    Bomb
)
# Morph tunnels or bomb chains--any block that Screw Attack can't break
CanBombTunnelBlock = all(
    MorphBall,
    any(
        Bomb,
        PowerBombTanks(1),
    ),
)
CanSingleBombBlock = any(
    CanBombTunnelBlock,
    ScrewAttack
)
CanBallCannon = CanRegularBomb
CanSpringBall = all(
    MorphBall,
    any(
        all(
            HiJump,
            CombinedHiJumpAndSpringBall,
        ),
        SpringBall,
    )
)
CanHiSpringBall = all(
    MorphBall,
    HiJump,
    any(
        SpringBall,
        CombinedHiJumpAndSpringBall,
    )
)
CanBallspark = all(
    SpeedBooster,
    CanSpringBall,
)
CanBallJump = all(
    MorphBall,
    any(
        Bomb,
        CanSpringBall
    )
)
CanLongBeam = lambda n: any(
    LongBeam,
    MissileCount(n),
    CanBombTunnelBlock,
)

# Logic option rules
NormalLogic = Requirement.setting_atleast("logic_difficulty", 1)
AdvancedLogic = Requirement.setting_atleast("logic_difficulty", 2)
NormalCombat = Requirement.setting_atleast("combat_logic_difficulty", 1)
MinimalCombat = Requirement.setting_atleast("combat_logic_difficulty", 2)
CanIBJ = all(
    Requirement.setting_atleast("ibj_in_logic", 1),
    CanRegularBomb,
)
CanHorizontalIBJ = all(
    CanIBJ,
    Requirement.setting_atleast("ibj_in_logic", 2)
)
CanWallJump = all(
    Requirement.item("Wall Jump"),
    any(
        Requirement.setting_is("walljumps", 1),  # Shuffled
        Requirement.setting_is("walljumps", 3)   # Enabled
    )
)
CanTrickySparks = all(
    Requirement.setting_enabled("tricky_shinesparks"),
    SpeedBooster,
)
HazardRuns = Requirement.setting_atleast("hazard_runs", 1)

# Miscellaneous rules
CanFly = any(  # infinite vertical
    CanIBJ,
    SpaceJump
)
CanFlyWall = any(  # infinite vertical with a usable wall
    CanFly,
    CanWallJump
)
CanVertical = any(  # any way of traversing vertically past base jump height, sans a wall
    HiJump,
    PowerGrip,
    CanFly
)
CanVerticalWall = any(  # any way of traversing vertically past base jump height, with a usable wall
    CanVertical,
    CanWallJump
)
CanHiGrip = all(
    HiJump,
    PowerGrip
)
CanHiWallJump = all(
    HiJump,
    CanWallJump
)
CanEnterHighMorphTunnel = any(  # morph tunnel 5 tiles above ground
    CanIBJ,
    all(
        MorphBall,
        PowerGrip
    )
)
CanEnterMediumMorphTunnel = any(  # morph tunnel 3 or 4 tiles above ground
    CanEnterHighMorphTunnel,
    CanHiSpringBall
)
RuinsTestEscape = all(
    any(
        all(
            NormalLogic,
            HiJump,
            CanWallJump
        ),
        CanIBJ,
        Requirement.item("Space Jump")  # Need SJ to escape, but it doesn't need to be active yet
    ),
    CanEnterMediumMorphTunnel
)

# Boss + difficult area combat logic
# TODO: Minimal combat on Hard may need tweaking
KraidCombat = any(
    all(
        MinimalCombat,
        any(
            MissileCount(1),
            SuperMissileCount(3)
        )
    ),
    all(
        NormalCombat,
        MissileTanks(4),
        EnergyTanks(1),
    ),
    all(
        MissileTanks(6),
        EnergyTanks(2)
    )
)
RidleyCombat = any(
    MinimalCombat,
    all(
        NormalCombat,
        MissileTanks(5),
        EnergyTanks(3),
    ),
    all(
        VariaSuit,
        MissileTanks(8),
        SuperMissileTanks(2),
        EnergyTanks(4)
    )
)
MotherBrainCombat = any(
    MinimalCombat,
    all(
        NormalCombat,
        any(
            PowerGrip,
            GravitySuit,
            HiJump,
            all(
                VariaSuit,
                CanWallJump
            )
        ),
        MissileTanks(8),
        SuperMissileTanks(2),
        EnergyTanks(5)
    ),
    all(
        any(
            VariaSuit,
            GravitySuit
        ),
        any(
            ChargeBeam,
            LongBeam,
            WaveBeam,
            PlasmaBeam,
            ScrewAttack
        ),
        PowerGrip,
        MissileTanks(10),
        SuperMissileTanks(3),
        EnergyTanks(6),
    )
)
ChozodiaCombat = any(
    MinimalCombat,
    all(
        NormalCombat,
        any(
            MissileTanks(4),
            IceBeam,
            PlasmaBeam
        ),
        EnergyTanks(3)
    ),
    all(
        any(
            MissileTanks(10),
            IceBeam,
            PlasmaBeam
        ),
        any(
            VariaSuit,
            GravitySuit
        ),
        EnergyTanks(5)
    ),
)
# Currently combat logic assumes non-100% Mecha Ridley
MechaRidleyCombat = any(
    all(
        MinimalCombat,
        Missiles,
        any(
            PlasmaBeam,
            ScrewAttack,
            SuperMissileCount(6)
        )
    ),
    all(
        NormalCombat,
        SuperMissileTanks(3),
        MissileTanks(4),
        EnergyTanks(4)
    ),
    all(
        any(
            HiJump,
            SpaceJump
        ),
        ScrewAttack,
        SuperMissileTanks(4),
        MissileTanks(10),
        EnergyTanks(6)
    )
)

# Goal
ReachedGoal = any(
    all(
        Requirement.setting_is("goal", "mecha_ridley")
    ),
    all(
        Requirement.setting_is("goal", "bosses"),
        MotherBrainBoss,
        ChozoGhostBoss
    ),
    all(
        Requirement.setting_is("goal", "metroid_dna"),
        Requirement.has_metroid_dna(),
    ),
)
