import unittest

import Generate


class TestGenerateWeightQuantity(unittest.TestCase):
    def test_quantity_yaml_entries_do_not_share_nested_meta_triggers(self):
        source = {"SyntheticGame": {"triggers": []}}
        weights = Generate.expand_yaml_quantity(source, 3)

        for yaml in weights:
            yaml["SyntheticGame"]["triggers"].append({"name": "synthetic-meta-trigger"})

        self.assertEqual(
            [1, 1, 1],
            [len(yaml["SyntheticGame"]["triggers"]) for yaml in weights],
        )
        self.assertEqual(3, len({id(yaml) for yaml in weights}))
