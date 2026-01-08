from copy import copy, deepcopy
import os

from test.bases import TestBase

from ..codegen.util import get_json_object
from ..codegen.merge import merge

class TestMergeBasic(TestBase):
    auto_construct = False
    list1 = list(range(1, 5))
    list2 = list(range(5, 9))
    list3 = list(range(1, 9))

    dict1 = { f"key{idx}": f"value{idx}" for idx in range(1, 5) }
    dict2 = { f"key{idx}": f"value{idx}" for idx in range(5, 9) }
    dict3 = { f"key{idx}": f"value{idx}" for idx in range(1, 9) }

    def test_merge_list(self):
        original = copy(self.list1)
        addon = self.list2
        result = self.list3

        merge(original, addon)
        self.assertEqual(original, result)

    def test_merge_dict(self):
        original = copy(self.dict1)
        addon = self.dict2
        result = self.dict3

        merge(original, addon)
        self.assertEqual(original, result)

    def test_merge_dict_with_non_dict(self):
        original = copy(self.dict1)
        
        self.assertRaises(RuntimeError, merge, original, self.list2)
        self.assertRaises(RuntimeError, merge, original, "addon")
        self.assertRaises(RuntimeError, merge, original, 2)

    def test_merge_list_with_non_list(self):
        original = copy(self.list1)
        
        self.assertRaises(RuntimeError, merge, original, self.dict2)
        self.assertRaises(RuntimeError, merge, original, "addon")
        self.assertRaises(RuntimeError, merge, original, 2)

    def test_merge_unmergeable_type(self):
        original = "string"

        self.assertRaises(RuntimeError, merge, original, self.list2)
        self.assertRaises(RuntimeError, merge, original, self.dict2)
        self.assertRaises(RuntimeError, merge, original, "addon")
        self.assertRaises(RuntimeError, merge, original, 2)

class TestMergeComplex(TestBase):
    auto_construct = False
    test_pkg = '.'.join(__name__.split('.')[:-1])
    original = get_json_object(test_pkg, "data/merge/original.json")

    def test_complex_patch(self):
        original = deepcopy(self.original)
        result = get_json_object(self.test_pkg, "data/merge/result.json")
        include = get_json_object(self.test_pkg, "data/merge/patch.json")

        original = merge(original, include)
        self.assertEqual(original, result)

base_entry_template = {
    "int": 1,
    "string": "a string",
    "dict": { "one": 1, "two": 2 },
    "list": [ "a", "b" ],
}

addon_entry_template = {
    "boolean": True,
    "dict": { "three": 3 },
    "list": [ "c", "d" ]
}

class TestPatch(TestBase):
    auto_construct = False

    original = { f"key{i}": deepcopy(base_entry_template) for i in range(20) }

    def test_merge_regex(self):
        original = deepcopy(self.original)
        patch = { "/key\\d\\d/": deepcopy(addon_entry_template) }
        result = merge(original, patch)

        for key, value in result.items():
            if len(key) == 4: # does not match regex
                self.assertNotIn("boolean", value)
                self.assertEqual(len(value["dict"]), 2)
                self.assertEqual(len(value["list"]), 2)
            if len(key) == 5: # does not match regex
                self.assertIn("boolean", value)
                self.assertEqual(len(value["dict"]), 3)
                self.assertEqual(len(value["list"]), 4)

    def test_merge_glob(self):
        original = deepcopy(self.original)
        patch = { "*": deepcopy(addon_entry_template) }
        result = merge(original, patch)

        for key, value in result.items():
            self.assertIn("boolean", value)
            self.assertEqual(len(value["dict"]), 3)
            self.assertEqual(len(value["list"]), 4)
