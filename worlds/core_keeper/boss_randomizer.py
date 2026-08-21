"""Deterministic one-to-one boss-slot permutation."""

from __future__ import annotations

import random


# Runtime ObjectID names, in progression order.  A single cycle guarantees a
# derangement: every boss moves exactly once and every encounter receives one.
BOSS_SLOTS = (
    "SlimeBoss", "BossLarva", "KingSlime", "LarvaHiveBoss",
    "ShamanBoss", "BirdBoss", "PoisonSlimeBoss", "OctopusBoss",
    "SlipperySlimeBoss", "ScarabBoss", "LavaSlimeBoss",
    "SnakeBossSegment", "HydraBossNature", "HydraBossSea",
    "HydraBossDesert", "CoreBoss", "WallBoss", "GiantCicadaBoss",
    "HydraBossVoid", "RobotBoss",
)


def build_boss_mapping(seed: int) -> dict[str, str]:
    rng = random.Random(seed)
    cycle = list(BOSS_SLOTS)
    rng.shuffle(cycle)
    return {
        source: cycle[(index + 1) % len(cycle)]
        for index, source in enumerate(cycle)
    }
