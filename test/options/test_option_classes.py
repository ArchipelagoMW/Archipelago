import unittest

from collections import Counter

from Options import Choice, DefaultOnToggle, Toggle, OptionDict, OptionError, OptionSet, OptionList, OptionCounter


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


class TestContainerOptions(unittest.TestCase):
    def test_option_dict(self):
        class TestOptionDict(OptionDict):
            valid_keys = frozenset({"A", "B", "C"})

        unknown_key_init_dict = {"D": "Foo"}
        test_option_dict = TestOptionDict(unknown_key_init_dict)
        self.assertRaises(OptionError, test_option_dict.verify_keys)

        init_dict = {"A": "foo", "B": "bar"}
        test_option_dict = TestOptionDict(init_dict)

        self.assertEqual(test_option_dict, init_dict)  # Implicit value comparison
        self.assertEqual(test_option_dict["A"], "foo")
        self.assertIn("B", test_option_dict)
        self.assertNotIn("C", test_option_dict)
        self.assertRaises(KeyError, lambda: test_option_dict["C"])

    def test_option_set(self):
        class TestOptionSet(OptionSet):
            valid_keys = frozenset({"A", "B", "C"})

        unknown_key_init_set = {"D"}
        test_option_set = TestOptionSet(unknown_key_init_set)
        self.assertRaises(OptionError, test_option_set.verify_keys)

        init_set = {"A", "B"}
        test_option_set = TestOptionSet(init_set)

        self.assertEqual(test_option_set, init_set)  # Implicit value comparison
        self.assertIn("B", test_option_set)
        self.assertNotIn("C", test_option_set)

    def test_option_list(self):
        class TestOptionList(OptionList):
            valid_keys = frozenset({"A", "B", "C"})

        unknown_key_init_list = ["D"]
        test_option_list = TestOptionList(unknown_key_init_list)
        self.assertRaises(OptionError, test_option_list.verify_keys)

        init_list = ["A", "B"]
        test_option_list = TestOptionList(init_list)

        self.assertEqual(test_option_list, init_list)
        self.assertIn("B", test_option_list)
        self.assertNotIn("C", test_option_list)


    def test_option_counter(self):
        class TestOptionCounter(OptionCounter):
            valid_keys = frozenset({"A", "B", "C"})

            max = 10
            min = 0

        unknown_key_init_dict = {"D": 5}
        test_option_counter = TestOptionCounter(unknown_key_init_dict)
        self.assertRaises(OptionError, test_option_counter.verify_keys)

        wrong_value_type_init_dict = {"A": "B"}
        self.assertRaises(TypeError, TestOptionCounter, wrong_value_type_init_dict)

        violates_max_init_dict = {"A": 5, "B": 11}
        test_option_counter = TestOptionCounter(violates_max_init_dict)
        self.assertRaises(OptionError, test_option_counter.verify_values)

        violates_min_init_dict = {"A": -1, "B": 5}
        test_option_counter = TestOptionCounter(violates_min_init_dict)
        self.assertRaises(OptionError, test_option_counter.verify_values)

        init_dict = {"A": 0, "B": 10}
        test_option_counter = TestOptionCounter(init_dict)
        self.assertEqual(test_option_counter, Counter(init_dict))
        self.assertIn("A", test_option_counter)
        self.assertNotIn("C", test_option_counter)
        self.assertEqual(test_option_counter["A"], 0)
        self.assertEqual(test_option_counter["B"], 10)
        self.assertEqual(test_option_counter["C"], 0)

    def test_culling_option_counter(self):
        class TestCullingCounter(OptionCounter):
            valid_keys = frozenset({"A", "B", "C"})
            cull_zeroes = True

        init_dict = {"A": 0, "B": 10}
        test_option_counter = TestCullingCounter(init_dict)
        self.assertNotIn("A", test_option_counter)
        self.assertIn("B", test_option_counter)
        self.assertNotIn("C", test_option_counter)
        self.assertEqual(test_option_counter["A"], 0)  # It's still a Counter! cull_zeroes is about "in" checks.
        self.assertEqual(test_option_counter, Counter({"B": 10}))
