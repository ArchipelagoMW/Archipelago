"""
Iterative sphere-building for CVAoS routing.

A "sphere" is one round of item collection:
  - Sphere 0: pickups reachable with no abilities from the starting entrance.
  - Sphere N: pickups newly reachable after gaining all abilities from spheres 0..N-1.

This models the dependency chain: collect pickups → gain abilities → reach more pickups.
Run directly to print sphere generation results from Soma's starting entrance:

    python -m worlds.cvaos.data.routing_calculation_spheres
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet, Set, Tuple

from .routing_info import AbilityCombo
from .routing_calculation_entrances import MaskUtils, RoutingQueries
from .routing_calculation_entrances_to_items import (
    PickupNodeId,
    RoutingGraph,
    default_graph,
)
from .pickup_info import pickup_info_collection

NodeId = str
ReqMask = int


# ─────────────────────────────────────────────────────────────
# Pickup-name → ability mapping
# ─────────────────────────────────────────────────────────────

# Maps pickup simple_name → the AbilityCombo flag it grants.
# Technique flags (PixPer, Clip, Enemy, etc.) are situational and not item-based.
_SOUL_NAME_TO_ABILITY: dict[str, AbilityCombo] = {
    "Flying Armor":    AbilityCombo.Glide,
    "Skeleton Blaze":  AbilityCombo.Slide,
    "Malphas":         AbilityCombo.DJump,
    "Hippogryph":      AbilityCombo.HJump,
    "Undine":          AbilityCombo.WWalk,
    "Skula":           AbilityCombo.Dive,
    "Black Panther":   AbilityCombo.Panth,
    "Giant Bat":       AbilityCombo.Bat,
    "Grave Keeper":    AbilityCombo.BDash,
    "Kicker Skeleton": AbilityCombo.Kick,
    "Devil":           AbilityCombo.Tform,
    "Curly":           AbilityCombo.Tform,
    "Manticore":       AbilityCombo.Tform,
}


def build_pickup_to_ability_mask() -> dict[int, ReqMask]:
    """
    Return a mapping from pickup_number → ability ReqMask granted by collecting it.
    Only pickups whose simple_name matches a known soul are included.
    """
    result: dict[int, ReqMask] = {}
    for pickup in pickup_info_collection:
        ability = _SOUL_NAME_TO_ABILITY.get(pickup.simple_name)
        if ability is not None:
            result[pickup.pickup_number] = int(ability)
    return result


# ─────────────────────────────────────────────────────────────
# Result types
# ─────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class Sphere:
    index: int
    have_mask_before: ReqMask          # abilities when entering this sphere
    have_mask_after: ReqMask           # abilities after collecting this sphere's pickups
    newly_reachable_pickups: FrozenSet[int]
    abilities_gained: ReqMask          # new ability bits unlocked this sphere


@dataclass(frozen=True)
class SphereResult:
    spheres: Tuple[Sphere, ...]
    unreachable_pickups: FrozenSet[int]
    final_have_mask: ReqMask


# ─────────────────────────────────────────────────────────────
# Core algorithm
# ─────────────────────────────────────────────────────────────

def build_reachability_spheres(
    graph: RoutingGraph,
    start_entrance: NodeId,
    pickup_to_abilities: dict[int, ReqMask],
    *,
    initial_have_mask: ReqMask = 0,
) -> SphereResult:
    """
    Iteratively expand the reachable pickup set from start_entrance.

    Each iteration (sphere):
      1. BFS the graph with the current have_mask.
      2. Collect all newly reachable pickup_numbers.
      3. OR their ability grants into have_mask.
      4. Repeat until stable.

    Args:
        graph: Combined entrance+pickup routing graph (from default_graph()).
        start_entrance: NodeId to begin BFS from, e.g. ``"000:003"``.
        pickup_to_abilities: Maps pickup_number → ReqMask granted by that pickup.
        initial_have_mask: Abilities assumed before sphere 0 (default 0).

    Returns:
        SphereResult with one Sphere per iteration plus the set of permanently
        unreachable pickups.
    """
    all_pickup_numbers: FrozenSet[int] = frozenset(
        PickupNodeId.number(node_id)
        for node_id in graph.adj
        if PickupNodeId.is_pickup(node_id)
    )

    collected_pickups: Set[int] = set()
    have_mask: ReqMask = initial_have_mask
    spheres: list[Sphere] = []

    while True:
        reachable_nodes = RoutingQueries.reachable_entrance_nodes(graph, start_entrance, have_mask)

        reachable_pickups = {
            PickupNodeId.number(n) for n in reachable_nodes if PickupNodeId.is_pickup(n)
        }

        newly_reachable = reachable_pickups - collected_pickups
        if not newly_reachable:
            break  # stable — nothing new opened up

        # OR together ability grants from every newly reachable pickup
        new_ability_bits: ReqMask = 0
        for pnum in newly_reachable:
            new_ability_bits |= pickup_to_abilities.get(pnum, 0)

        abilities_gained = new_ability_bits & ~have_mask  # bits that are genuinely new

        spheres.append(Sphere(
            index=len(spheres),
            have_mask_before=have_mask,
            have_mask_after=have_mask | new_ability_bits,
            newly_reachable_pickups=frozenset(newly_reachable),
            abilities_gained=abilities_gained,
        ))

        collected_pickups |= newly_reachable
        have_mask |= new_ability_bits

    return SphereResult(
        spheres=tuple(spheres),
        unreachable_pickups=frozenset(all_pickup_numbers - collected_pickups),
        final_have_mask=have_mask,
    )


# ─────────────────────────────────────────────────────────────
# Display
# ─────────────────────────────────────────────────────────────

def print_sphere_result(
    result: SphereResult,
    pickup_to_abilities: dict[int, ReqMask],
    *,
    verbose: bool = True,
) -> None:
    total_reached = sum(len(s.newly_reachable_pickups) for s in result.spheres)
    print(f"=== Sphere Generation: {len(result.spheres)} sphere(s), {total_reached} pickup(s) reached ===\n")

    for sphere in result.spheres:
        count = len(sphere.newly_reachable_pickups)
        before_text = MaskUtils.format(sphere.have_mask_before)
        gained_text = MaskUtils.format(sphere.abilities_gained) if sphere.abilities_gained else "(none)"
        print(f"Sphere {sphere.index}:  {count:3d} pickup(s)  |  entering with: {before_text}  |  new abilities: {gained_text}")  # noqa: E501

        if verbose:
            ability_pickups = sorted(
                pnum for pnum in sphere.newly_reachable_pickups
                if pickup_to_abilities.get(pnum, 0)
            )
            other_pickups = sorted(
                pnum for pnum in sphere.newly_reachable_pickups
                if not pickup_to_abilities.get(pnum, 0)
            )

            for pnum in ability_pickups:
                ability_label = MaskUtils.format(pickup_to_abilities[pnum])
                print(f"    pickup {pnum:3d}  -> grants [{ability_label}]")
            if other_pickups:
                print(f"    + {len(other_pickups)} non-ability pickup(s): {other_pickups}")

    print(f"\nFinal abilities: {MaskUtils.format(result.final_have_mask)}")
    if result.unreachable_pickups:
        print(f"Unreachable ({len(result.unreachable_pickups)}): {sorted(result.unreachable_pickups)}")
    else:
        print("All pickups reachable.")


# ─────────────────────────────────────────────────────────────
# Test / demo entry point
# ─────────────────────────────────────────────────────────────

def test_sphere_generation_from_000_003() -> SphereResult:
    """
    Build reachability spheres starting from Soma's starting entrance (000:003).
    Asserts at least one sphere is produced and returns the result.
    """
    graph = default_graph()
    start = "000:003"
    pickup_to_abilities = build_pickup_to_ability_mask()

    result = build_reachability_spheres(graph, start, pickup_to_abilities)
    print_sphere_result(result, pickup_to_abilities, verbose=True)

    assert result.spheres, "No spheres produced — nothing reachable from start?"
    assert "000:003" in graph.adj, "Start entrance not in graph"
    return result


if __name__ == "__main__":
    test_sphere_generation_from_000_003()