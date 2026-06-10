import unittest
import Generate


class TestPlayerOptions(unittest.TestCase):

    def test_update_weights(self):
        original_weights = {
            "scalar_1": 50,
            "scalar_2": 25,
            "list_1": ["string"],
            "dict_1": {"option_a": 50, "option_b": 50},
            "dict_2": {"option_f": 50},
            "set_1": {"option_c"}
        }

        # test that we don't allow +merge syntax on scalar variables
        with self.assertRaises(BaseException):
            Generate.update_weights(original_weights, {"+scalar_1": 0}, "Tested", "")

        new_weights = Generate.update_weights(original_weights, {"scalar_2": 0,
                                                                 "+list_1": ["string_2"],
                                                                 "+dict_1": {"option_b": 0, "option_c": 50},
                                                                 "+set_1": {"option_c", "option_d"},
                                                                 "dict_2": {"option_g": 50},
                                                                 "+list_2": ["string_3"]},
                                              "Tested", "")

        self.assertEqual(new_weights["scalar_1"], 50)
        self.assertEqual(new_weights["scalar_2"], 0)
        self.assertEqual(new_weights["list_2"], ["string_3"])
        self.assertEqual(new_weights["list_1"], ["string", "string_2"])
        self.assertEqual(new_weights["dict_1"]["option_a"], 50)
        self.assertEqual(new_weights["dict_1"]["option_b"], 50)
        self.assertEqual(new_weights["dict_1"]["option_c"], 50)
        self.assertNotIn("option_f", new_weights["dict_2"])
        self.assertEqual(new_weights["dict_2"]["option_g"], 50)
        self.assertEqual(len(new_weights["set_1"]), 2)
        self.assertIn("option_d", new_weights["set_1"])

    def test_update_dict_supports_negatives_and_zeroes(self):
        original_options = {
            "dict_1": {"a": 1, "b": -1},
            "dict_2": {"a": 1, "b": -1},
        }
        new_weights = Generate.update_weights(
            original_options,
            {
                "+dict_1": {"a": -2, "b": 2},
                "-dict_2": {"a": 1, "b": 2},
            },
            "Tested",
            "",
        )
        self.assertEqual(new_weights["dict_1"]["a"], -1)
        self.assertEqual(new_weights["dict_1"]["b"], 1)
        self.assertEqual(new_weights["dict_2"]["a"], 0)
        self.assertEqual(new_weights["dict_2"]["b"], -3)
        self.assertIn("a", new_weights["dict_2"])
