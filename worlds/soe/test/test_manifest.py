import json
from pathlib import Path
from unittest import TestCase, skipUnless


@skipUnless((Path(__file__).parent.parent / "tools" / "make_manifest.py").exists(), "Packaged without tools")
class ManifestTest(TestCase):
    def test_manifest_is_up_to_date(self) -> None:
        from ..tools.make_manifest import make_manifest

        expected_manifest = make_manifest()
        with (Path(__file__).parent.parent / "archipelago.json").open("r", encoding="utf-8") as f:
            actual_manifest = json.load(f)
        self.assertEqual(actual_manifest, expected_manifest, "Manifest is not up to date")
