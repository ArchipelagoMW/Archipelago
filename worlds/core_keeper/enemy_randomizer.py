"""Deterministic ordinary-enemy slot permutation."""

from __future__ import annotations

import random


# Progression order and spawn-region bucket. Structural spawners and plants are
# intentionally absent; their ordinary children still pass through the runtime
# constructor substitution.
ENEMY_SLOTS = (
    ("MushroomEnemy", 0), ("MushroomBrute", 0), ("SlimeBlob", 0),
    ("AggressiveSlimeBlob", 0), ("CavelingSkirmisher", 1),
    ("CavelingSpearman", 1), ("ClayWormSegment", 1), ("Larva@0", 2),
    ("BigLarva@0", 2), ("Larva@1", 3), ("BigLarva@1", 3),
    ("AcidLarva", 2), ("Caveling", 4), ("CavelingShaman", 4),
    ("CavelingBrute", 4), ("AFPestElectric", 4), ("RoyalSlimeBlob", 4),
    ("CavelingHunter", 5), ("CavelingGardener", 5),
    ("PoisonSlimeBlob", 6), ("InfectedCaveling", 6), ("MoldTentacle", 6),
    ("CrabEnemy", 7), ("SmallTentacle", 7), ("SlipperySlimeBlob", 7),
    ("CavelingScholar", 8), ("AncientGolem", 8), ("BombScarab", 9),
    ("CavelingAssassin", 9), ("CavelingMummy", 9), ("LavaSlimeBlob", 10),
    ("LavaButterfly", 10), ("Mimite", 11), ("OrbitalTurret", 11),
    ("WormSegment", 11), ("CrystalBigSnail", 11),
    ("AmoebaWormSegment", 12), ("AmoebaGiantSegment", 12),
    ("CicadaNymph", 12), ("GoldenBombScarab", 13), ("RobotMiner", 13),
    ("RobotPatroller", 13), ("RobotSwarmer", 13), ("VoidLarva", 14),
    ("VoidCaveling", 14), ("VoidCavelingShaman", 14),
    ("VoidCavelingBrute", 14),
)


def build_enemy_mapping(seed: int, difficulty: int = 0) -> dict[str, str]:
    rng = random.Random(seed)
    names = [name for name, _ in ENEMY_SLOTS]
    biome = dict(ENEMY_SLOTS)
    for _attempt in range(256):
        remaining = set(names)
        cycle = [rng.choice(names)]
        remaining.remove(cycle[0])
        while remaining:
            source = cycle[-1]
            cross_biome = [
                candidate for candidate in sorted(remaining)
                if biome[source] != biome[candidate]
            ]
            allow_same_biome = rng.random() < 0.002
            candidates = sorted(remaining) if allow_same_biome else cross_biome
            if not candidates:
                break
            weights = []
            for candidate in candidates:
                # Easy and Medium suppress later-region replacements in earlier
                # slots. Hard and Masochist use an otherwise uniform permutation.
                upward_distance = max(0, biome[candidate] - biome[source])
                if difficulty <= 0:
                    weight = 1.0 / float(1 + upward_distance) ** 3
                elif difficulty == 1:
                    weight = 1.0 / float(1 + upward_distance)
                else:
                    weight = 1.0
                weights.append(weight)
            chosen = rng.choices(candidates, weights=weights, k=1)[0]
            cycle.append(chosen)
            remaining.remove(chosen)
        if remaining:
            continue
        if biome[cycle[-1]] != biome[cycle[0]] or rng.random() < 0.002:
            return {
                source: cycle[(index + 1) % len(cycle)]
                for index, source in enumerate(cycle)
            }
    raise RuntimeError("Unable to construct an enemy randomizer cycle")
