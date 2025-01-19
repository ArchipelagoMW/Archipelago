from typing import Dict
from datastorage import DataStorage, InvalidArgumentsException
import unittest


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

    def test_raises_on_missing_key(self):
        self.setup_storage({})

        set_cmd: Dict[str, object] = { 
            "operations": [{"operation": "add", "value": 12}] 
        }

        with self.assertRaisesRegex(InvalidArgumentsException, "'key'"):
            self.storage.set(1, set_cmd)

    def test_raises_on_key_invalid_type(self):
        self.setup_storage({})

        set_cmd: Dict[str, object] = { 
            "key": 10,
            "operations": [{"operation": "add", "value": 12}] 
        }

        with self.assertRaisesRegex(InvalidArgumentsException, "key has to be a string"):
            self.storage.set(1, set_cmd)

    def test_raises_on_set_on_read_only_key(self):
        self.setup_storage({})

        set_cmd: Dict[str, object] = { 
            "key": "_read_ReadOnlyKey",
            "operations": [{"operation": "add", "value": 12}] 
        }

        with self.assertRaisesRegex(InvalidArgumentsException, 
                                    "cannot apply `Set` operation to the read only key `_read_ReadOnlyKey`"):
            self.storage.set(1, set_cmd)

    def test_raises_on_missing_operations(self):
        self.setup_storage({})

        set_cmd: Dict[str, object] = { 
            "key": "OperationsMissing"
        }

        with self.assertRaisesRegex(InvalidArgumentsException, "'operations'"):
            self.storage.set(1, set_cmd)

    def test_raises_on_operations_invalid_type(self):
        self.setup_storage({})

        set_cmd: Dict[str, object] = { 
            "key": "OperationsNotAList",
            "operations": {"operation": "add", "value": 12}
        }

        with self.assertRaisesRegex(InvalidArgumentsException, "`operations` is not a list"):
            self.storage.set(1, set_cmd)

    def test_adding_number(self):
        self.setup_storage({"BasicAdd": 10})

        set_cmd: Dict[str, object] = { 
            "key": "BasicAdd", 
            "operations": [{"operation": "add", "value": 12}] 
        }

        result: Dict[str, object] = self.storage.set(1, set_cmd)

        self.assert_result(result, "BasicAdd", 22, 10)

    def test_adding_number_with_default(self):
        self.setup_storage({})

        set_cmd: Dict[str, object] = { 
            "key": "AddWithDefault", 
            "default": 35,
            "operations": [{"operation": "add", "value": 6}]
        }

        result: Dict[str, object] = self.storage.set(1, set_cmd)

        self.assert_result(result, "AddWithDefault", 41, 35)

    # The `default` operation is currently weird in two ways:
    # * The operation requires a "value" but its contents is ignored
    # * The original_value is also updated to the value
    def test_default_operation(self):
        self.setup_storage({})

        set_cmd: Dict[str, object] = { 
            "key": "Default", 
            "default": "Hello",
            "operations": [{"operation": "default", "value": None}]
        }

        result: Dict[str, object] = self.storage.set(1, set_cmd)

        self.assert_result(result, "Default", "Hello", "Hello")

    def test_energy_link_depletion_pattern(self):
        self.setup_storage({"EnergyLink1": 20})

        set_cmd: Dict[str, object] = { 
            "key": "EnergyLink1", 
            "default": 0,
            "operations": [
                {"operation": "add", "value": -50},
                {"operation": "max", "value": 0}
            ]
        }

        result: Dict[str, object] = self.storage.set(1, set_cmd)

        self.assert_result(result, "EnergyLink1", 0, 20)

    def test_should_preserve_fields_from_set(self):
        self.setup_storage({})

        set_cmd: Dict[str, object] = { 
            "key": "NewKey", 
            "default": 100,
            "want_reply": True,
            "operations": [{"operation": "replace", "value": 10}],
            "10GbMovieData": "MTBHYk1vdmllRGF0YQ=="
        }

        result: Dict[str, object] = self.storage.set(1, set_cmd)

        self.assert_result(result, "NewKey", 10, 100)
        self.assertEqual(result["default"], 100)
        self.assertEqual(result["want_reply"], True)
        self.assertEqual(result["10GbMovieData"], "MTBHYk1vdmllRGF0YQ==")

    def test_default_should_not_override_existing_value(self):
        self.setup_storage({ "DefaultWithExistingValue": "ExistingValue" })

        set_cmd: Dict[str, object] = { 
            "key": "DefaultWithExistingValue", 
            "default": "NewValue",
            "operations": [{"operation": "default", "value": "Ignored"}]
        }

        result: Dict[str, object] = self.storage.set(1, set_cmd)

        self.assert_result(result, "DefaultWithExistingValue", "ExistingValue", "ExistingValue")

    def test_should_raise_error_on_failure_if_no_error_handling_is_specified(self):
        self.setup_storage({ "RaiseOnPopWithNonExistingKey": {} })

        set_cmd: Dict[str, object] = { 
            "key": "RaiseOnPopWithNonExistingKey", 
            "operations": [{"operation": "pop", "value": "non_existing_key"}]
        }

        with self.assertRaises(KeyError):
            self.storage.set(1, set_cmd)

    def test_should_raise_error_on_failure_if_handling_is_specified_as_raise(self):
        self.setup_storage({ "RaiseOnPopWithNonExistingKeyAndOnErrorRaise": {} })

        set_cmd: Dict[str, object] = { 
            "key": "RaiseOnPopWithNonExistingKeyAndOnErrorRaise", 
            "on_error": "raise",
            "operations": [{"operation": "pop", "value": "non_existing_key"}]
        }

        with self.assertRaises(KeyError):
            self.storage.set(1, set_cmd)

    def test_should_set_key_to_default_if_on_error_is_set_default(self):
        self.setup_storage({ "DoNotRaiseOnPopWithNonExistingKeyAndOnErrorSetDefault": {} })

        set_cmd: Dict[str, object] = { 
            "key": "DoNotRaiseOnPopWithNonExistingKeyAndOnErrorSetDefault", 
            "default": "Something",
            "on_error": "set_default",
            "operations": [{"operation": "pop", "value": "non_existing_key"}]
        }

        result: Dict[str, object] = self.storage.set(1, set_cmd)

        self.assert_result(result, "DoNotRaiseOnPopWithNonExistingKeyAndOnErrorSetDefault", "Something", {})

    def test_should_undo_any_operations_on_key_if_on_error_is_undo(self):
        self.setup_storage({ "UndoOperationsWithOnErrorUndo": 10 })

        set_cmd: Dict[str, object] = { 
            "key": "UndoOperationsWithOnErrorUndo", 
            "on_error": "undo",
            "operations": [
                {"operation": "add", "value": 9},
                {"operation": "pop", "value": "not_a_dict"}
            ]
        }

        result: Dict[str, object] = self.storage.set(1, set_cmd)

        self.assert_result(result, "UndoOperationsWithOnErrorUndo", 10, 10)

    def test_should_abort_any_further_operations_on_key_if_on_error_abort(self):
        self.setup_storage({ "AbortOperationsWithOnErrorAbort": 10 })

        set_cmd: Dict[str, object] = { 
            "key": "AbortOperationsWithOnErrorAbort", 
            "on_error": "abort",
            "operations": [
                {"operation": "add", "value": 9},
                {"operation": "pop", "value": "not_a_dict"},
                {"operation": "add", "value": 10}
            ]
        }

        result: Dict[str, object] = self.storage.set(1, set_cmd)

        self.assert_result(result, "AbortOperationsWithOnErrorAbort", 19, 10)

    def test_should_ignore_any_errors_on_operations_on_if_on_error_ignore(self):
        self.setup_storage({ "IgnoreErrorsOnOperationsWithOnErrorIgnore": 10 })

        set_cmd: Dict[str, object] = { 
            "key": "IgnoreErrorsOnOperationsWithOnErrorIgnore", 
            "on_error": "ignore",
            "operations": [
                {"operation": "add", "value": 9},
                {"operation": "pop", "value": "not_a_dict"},
                {"operation": "add", "value": 10}
            ]
        }

        result: Dict[str, object] = self.storage.set(1, set_cmd)

        self.assert_result(result, "IgnoreErrorsOnOperationsWithOnErrorIgnore", 29, 10)

    def test_should_set_and_override_slot_argument(self):
        self.setup_storage({})

        set_cmd1: Dict[str, object] = { 
            "key": "SetSlotTo1", 
            "operations": [
                {"operation": "replace", "value": 100}
            ]
        }
        result: Dict[str, object] = self.storage.set(1, set_cmd1)
        self.assertEqual(result["slot"], 1)

        set_cmd2: Dict[str, object] = { 
            "key": "SetSlotTo1", 
            "Slot": "MyDataToOverride",
            "operations": [
                {"operation": "replace", "value": 100}
            ]
        }
        result: Dict[str, object] = self.storage.set(2, set_cmd2)
        self.assertEqual(result["slot"], 2)
