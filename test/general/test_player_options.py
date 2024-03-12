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
        self.assertTrue("list_2" in new_weights and new_weights["list_2"] == ["string_3"])
        self.assertEqual(new_weights["list_1"], ["string", "string_2"])
        self.assertEqual(new_weights["dict_1"]["option_a"], 50)
        self.assertEqual(new_weights["dict_1"]["option_b"], 0)
        self.assertTrue("option_c" in new_weights["dict_1"] and new_weights["dict_1"]["option_c"] == 50)
        self.assertTrue("option_f" not in new_weights["dict_2"] and new_weights["dict_2"]["option_g"] == 50)
        self.assertTrue(len(new_weights["set_1"]) == 2 and "option_d" in new_weights["set_1"])
