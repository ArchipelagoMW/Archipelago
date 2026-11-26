import unittest

from .. import apmw_contract, semantic_projection
from ..apmw_projection import contract, fundamental, models, semantic


class TestProjectionExports(unittest.TestCase):
    def test_semantic_compatibility_exports_are_explicit_and_canonical(self):
        self.assertEqual(semantic.__all__, semantic_projection.__all__)
        for name in semantic.__all__:
            with self.subTest(name=name):
                self.assertIs(
                    getattr(semantic, name),
                    getattr(semantic_projection, name),
                )
        self.assertIs(semantic.SemanticSeeds, models.SemanticSeeds)
        self.assertIs(
            semantic.characterize_fundamental_owned_plan,
            fundamental.characterize_fundamental_owned_plan,
        )

    def test_contract_compatibility_exports_are_explicit_and_canonical(self):
        self.assertNotIn("json", apmw_contract.__all__)
        self.assertNotIn("Path", apmw_contract.__all__)
        for name in apmw_contract.__all__:
            with self.subTest(name=name):
                self.assertIs(
                    getattr(contract, name),
                    getattr(apmw_contract, name),
                )


if __name__ == "__main__":
    unittest.main()
