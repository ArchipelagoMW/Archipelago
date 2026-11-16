import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

WORLD = Path(__file__).parents[1]
VENDORED = ("AoE2ScenarioParser", "ordered_set")

PROBE = """
import sys
import typing_extensions
sys.path[:] = [p for p in sys.path if "site-packages" not in p]
sys.path.insert(0, sys.argv[1])

import vendored.ordered_set
sys.modules.setdefault("ordered_set", vendored.ordered_set)

from vendored.AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from vendored.AoE2ScenarioParser.scenarios.aoe2_scenario import _get_structure
from vendored.AoE2ScenarioParser.objects.support.area import Area
from vendored.AoE2ScenarioParser.datasets.projectiles import ProjectileInfo
from vendored.AoE2ScenarioParser.datasets.trigger_lists.attribute import Attribute
assert "FileHeader" in _get_structure("DE", "1.59")
assert len(ProjectileInfo) > 0
assert Attribute.FOOD_STORAGE.editor_name
"""


def pack(target: Path) -> Path:
    with zipfile.ZipFile(target, "w") as archive:
        archive.writestr("vendored/__init__.py", "")
        for package in VENDORED:
            for path in (WORLD / package).rglob("*"):
                if path.is_file() and "__pycache__" not in path.parts:
                    archive.write(path, "vendored/" + path.relative_to(WORLD).as_posix())
    return target


class TestTheVendoredPackagesWorkFromAnApworldZip(unittest.TestCase):

    def test_they_import_and_read_their_data_files(self):
        with tempfile.TemporaryDirectory() as folder:
            archive = pack(Path(folder, "vendored.zip"))
            done = subprocess.run([sys.executable, "-I", "-W", "ignore", "-c", PROBE, str(archive)],
                                  capture_output=True, text=True)
        self.assertEqual(0, done.returncode, done.stderr)


if __name__ == "__main__":
    unittest.main()
