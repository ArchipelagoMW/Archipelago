import unittest

from Options import Choice, DefaultOnToggle, Toggle


class TestNumericOptions(unittest.TestCase):
    def test_numeric_option(self) -> None:
        """Tests the initialization and equivalency comparisons of the base Numeric Option class."""
        class TestChoice(Choice):
            option_zero = 0
            option_one = 1
            option_two = 2
            alias_three = 1
            non_option_attr = 2

        class TestToggle(Toggle):
            pass

        class TestDefaultOnToggle(DefaultOnToggle):
            pass

        with self.subTest("choice"):
            choice_option_default = TestChoice.from_any(TestChoice.default)
            choice_option_string = TestChoice.from_any("one")
            choice_option_int = TestChoice.from_any(2)
            choice_option_alias = TestChoice.from_any("three")
            choice_option_attr = TestChoice.from_any(TestChoice.option_two)
            
            self.assertEqual(choice_option_default, TestChoice.option_zero,
                "assigning default didn't match default value")
            self.assertEqual(choice_option_string, "one")
            self.assertEqual(choice_option_int, 2)
            self.assertEqual(choice_option_alias, TestChoice.alias_three)
            self.assertEqual(choice_option_attr, TestChoice.non_option_attr)

            self.assertLess(choice_option_string, "two")
            self.assertGreater(choice_option_string, "zero")
            self.assertLessEqual(choice_option_string, "one")
            self.assertLessEqual(choice_option_string, "two")
            self.assertGreaterEqual(choice_option_string, "one")
            self.assertGreaterEqual(choice_option_string, "zero")

            self.assertGreaterEqual(choice_option_alias, "three")

            self.assertRaises(KeyError, TestChoice.from_any, "four")
            
            self.assertIn(choice_option_int, [1, 2, 3])
            self.assertIn(choice_option_int, {2})
            self.assertIn(choice_option_int, (2,))

            self.assertIn(choice_option_string, ["one", "two", "three"])
            # this fails since the hash is derived from the value
            self.assertNotIn(choice_option_string, {"one"})
            self.assertIn(choice_option_string, ("one",))

        with self.subTest("toggle"):
            toggle_default = TestToggle.from_any(TestToggle.default)
            toggle_string = TestToggle.from_any("false")
            toggle_int = TestToggle.from_any(0)
            toggle_alias = TestToggle.from_any("off")

            self.assertFalse(toggle_default)
            self.assertFalse(toggle_string)
            self.assertFalse(toggle_int)
            self.assertFalse(toggle_alias)

        with self.subTest("on toggle"):
            toggle_default = TestDefaultOnToggle.from_any(TestDefaultOnToggle.default)
            toggle_string = TestDefaultOnToggle.from_any("true")
            toggle_int = TestDefaultOnToggle.from_any(1)
            toggle_alias = TestDefaultOnToggle.from_any("on")

            self.assertTrue(toggle_default)
            self.assertTrue(toggle_string)
            self.assertTrue(toggle_int)
            self.assertTrue(toggle_alias)
