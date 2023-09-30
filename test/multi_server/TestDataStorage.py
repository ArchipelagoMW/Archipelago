from typing import Dict
import unittest
from DataStorage import DataStorage

class TestDataStorage(unittest.TestCase):
    storage: DataStorage

    def setup_storage(self, initial_data: Dict[str, object]) -> None:
        self.data: Dict[str, object] = initial_data
        self.storage: DataStorage = DataStorage(self.data)

    def assert_result(self, result: Dict[str, object], key: str, value: object, original_value: object) -> None:
        self.assertEqual(self.data[key], value)
        self.assertEqual(result["cmd"], "SetReply")
        self.assertEqual(result["key"], key)
        self.assertEqual(result["value"], value)
        self.assertEqual(result["original_value"], original_value)

    def test_adding_number(self):
        self.setup_storage({ "BasicAdd": 10 })

        set_cmd: Dict[str, object] = { 
            "key": "BasicAdd", 
            "operations": [{"operation": "add", "value": 12}] 
        }

        result: Dict[str, object] = self.storage.apply_set_cmd(set_cmd)

        self.assert_result(result, "BasicAdd", 22, 10)

    def test_adding_number_with_default(self):
        self.setup_storage({})

        set_cmd: Dict[str, object] = { 
            "key": "AddWithDefault", 
            "default": 35,
            "operations": [{"operation": "add", "value": 6}]
        }

        result: Dict[str, object] = self.storage.apply_set_cmd(set_cmd)

        self.assert_result(result, "AddWithDefault", 41, 35)

    # Default is currently weird in two ways:
    # * The operation requires a "value" but its contents is ignored
    # * The original_value is also updated to the value
    def test_default_operation(self):
        self.setup_storage({})

        set_cmd: Dict[str, object] = { 
            "key": "Default", 
            "default": "Hello",
            "operations": [{"operation": "default", "value": None}]
        }

        result: Dict[str, object] = self.storage.apply_set_cmd(set_cmd)

        self.assert_result(result, "Default", "Hello", "Hello")

    def test_default_should_not_override_existing_value(self):
        self.setup_storage({ "DefaultWithExistingValue": "ExistingValue" })

        set_cmd: Dict[str, object] = { 
            "key": "DefaultWithExistingValue", 
            "default": "NewValue",
            "operations": [{"operation": "default", "value": "Ignored"}]
        }

        result: Dict[str, object] = self.storage.apply_set_cmd(set_cmd)

        self.assert_result(result, "DefaultWithExistingValue", "ExistingValue", "ExistingValue")
