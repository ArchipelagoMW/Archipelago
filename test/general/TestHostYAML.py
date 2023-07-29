import unittest

import Utils


class TestIDs(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with open(Utils.local_path("host.yaml")) as f:
            cls.yaml_options = Utils.parse_yaml(f.read())

    def testUtilsHasHost(self):
        for option_key, option_set in Utils.get_default_options().items():
            with self.subTest(option_key):
                self.assertIn(option_key, self.yaml_options)
                for sub_option_key in option_set:
                    self.assertIn(sub_option_key, self.yaml_options[option_key])

    def testHostHasUtils(self):
        utils_options = Utils.get_default_options()
        for option_key, option_set in self.yaml_options.items():
            with self.subTest(option_key):
                self.assertIn(option_key, utils_options)
                for sub_option_key in option_set:
                    self.assertIn(sub_option_key, utils_options[option_key])
