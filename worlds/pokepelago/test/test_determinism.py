"""
Determinism tests for the Pokepelago APWorld.

These tests verify that generating a world twice with the same seed produces identical
results regardless of Python's hash randomization (PYTHONHASHSEED). Each test spawns
two subprocesses with different PYTHONHASHSEED values, generates the same world in each,
and compares the outputs.

Running within a single process cannot catch hash-randomization bugs (sets iterate in
the same order for the process lifetime), so subprocess isolation is required.
"""
import json
import os
import pathlib
import subprocess
import sys
import unittest

_REPO_ROOT = str(pathlib.Path(__file__).parent.parent.parent.parent)

# Inline script run in each subprocess. Bootstraps the AP environment, generates a
# Pokepelago world through pre_fill, and prints JSON with the precollected item list.
_GEN_SCRIPT = """\
import sys
sys.path.insert(0, {repo_root!r})

import pathlib, settings, Utils
settings.no_gui = True
settings.skip_autosave = True
import ModuleUpdate
ModuleUpdate.update_ran = True
Utils.local_path.cached_path = pathlib.Path({repo_root!r})
Utils.user_path()

import json, random
from argparse import Namespace
from Generate import get_seed_name
from BaseClasses import MultiWorld, CollectionState
from worlds.AutoWorld import AutoWorldRegister, call_all

options = {options!r}
seed = {seed!r}

world_type = AutoWorldRegister.world_types["Pokepelago"]
multiworld = MultiWorld(1)
multiworld.game = {{1: "Pokepelago"}}
multiworld.player_name = {{1: "Tester"}}
multiworld.set_seed(seed)
random.seed(multiworld.seed)
multiworld.seed_name = get_seed_name(random)
args = Namespace()
for key, option in world_type.options_dataclass.type_hints.items():
    setattr(args, key, {{1: option.from_any(options.get(key, option.default))}})
multiworld.set_options(args)
multiworld.state = CollectionState(multiworld)
for step in ("generate_early", "create_regions", "create_items", "set_rules",
             "connect_entrances", "generate_basic", "pre_fill"):
    call_all(multiworld, step)

precollected = [item.name for item in multiworld.precollected_items[1]]
print(json.dumps({{"precollected": precollected}}))
"""


class TestDeterminism(unittest.TestCase):
    def _run_generation(self, options: dict, seed: int, hashseed: str) -> dict:
        script = _GEN_SCRIPT.format(repo_root=_REPO_ROOT, options=options, seed=seed)
        env = os.environ.copy()
        env["PYTHONHASHSEED"] = hashseed
        result = subprocess.run(
            [sys.executable, "-c", script],
            env=env, capture_output=True, text=True, timeout=120,
        )
        self.assertEqual(
            result.returncode, 0,
            f"Generation subprocess failed (PYTHONHASHSEED={hashseed}):\n{result.stderr}",
        )
        return json.loads(result.stdout.strip())

    def _assert_deterministic(self, options: dict, seed: int = 12345):
        run1 = self._run_generation(options, seed, "1")
        run2 = self._run_generation(options, seed, "2")
        self.assertEqual(
            run1["precollected"], run2["precollected"],
            f"Precollected items differ between runs with different PYTHONHASHSEED:\n"
            f"  HASHSEED=1: {run1['precollected']}\n"
            f"  HASHSEED=2: {run2['precollected']}",
        )

    def test_kanto_type_locks(self):
        """Kanto only, type_locks=on — starter types (Grass/Poison/Fire/Water) must be
        pre-collected in consistent order regardless of PYTHONHASHSEED."""
        self._assert_deterministic({
            "regions": ["Kanto"],
            "type_locks": 1,
            "dexsanity": 0,
        })

    def test_multi_region_type_locks(self):
        """Multiple regions with type_locks=on — larger starter_types set."""
        self._assert_deterministic({
            "regions": ["Kanto", "Hoenn", "Sinnoh"],
            "type_locks": 1,
            "dexsanity": 0,
        })

    def test_type_locks_off(self):
        """type_locks=off — starter Type Keys are still pre-collected unconditionally."""
        self._assert_deterministic({
            "regions": ["Kanto", "Johto"],
            "type_locks": 0,
            "region_locks": 0,
            "dexsanity": 0,
        })

    def test_all_locks_dexsanity(self):
        """All locks on with dexsanity — the fullest feature set."""
        self._assert_deterministic({
            "regions": ["Kanto", "Johto"],
            "type_locks": 1,
            "region_locks": 1,
            "dexsanity": 1,
        })

    def test_explicit_starter_region_and_pokemon(self):
        """Explicit starter_region + starter_pokemon — precollected types must be stable."""
        self._assert_deterministic({
            "regions": ["Kanto", "Johto"],
            "type_locks": 1,
            "region_locks": 1,
            "dexsanity": 1,
            "starter_region": 1,   # Kanto
            "starter_pokemon": 1,  # Bulbasaur → Grass + Poison pre-collected
        })

    def test_all_new_locks(self):
        """All new gate locks enabled — more items in pool, precollected order must be stable."""
        self._assert_deterministic({
            "regions": ["Kanto", "Johto"],
            "type_locks": 1,
            "region_locks": 1,
            "dexsanity": 1,
            "starter_region": 1,  # Kanto
            "legendary_locks": 1,
            "trade_locks": 1,
            "baby_locks": 1,
            "fossil_locks": 1,
            "stone_locks": 1,
        })

    def test_hisui_paldea_no_starters(self):
        """Hisui + Paldea only — Hisui has no starters, so no Type Keys pre-collected from
        there. Paldea starters determine precollected items; order must be stable."""
        self._assert_deterministic({
            "regions": ["Hisui", "Paldea"],
            "type_locks": 1,
            "region_locks": 1,
            "dexsanity": 1,
        })

    def test_all_regions_all_locks(self):
        """All ten regions + all new locks — maximum complexity, full determinism check."""
        self._assert_deterministic({
            "regions": ["Kanto", "Johto", "Hoenn", "Sinnoh", "Unova",
                        "Kalos", "Alola", "Galar", "Hisui", "Paldea"],
            "type_locks": 1,
            "region_locks": 1,
            "dexsanity": 1,
            "legendary_locks": 1,
            "trade_locks": 1,
            "baby_locks": 1,
            "fossil_locks": 1,
            "ultra_beast_locks": 1,
            "paradox_locks": 1,
            "stone_locks": 1,
        })


if __name__ == "__main__":
    unittest.main()
