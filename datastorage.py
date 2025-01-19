from typing import Any, Dict, List
import operator
import copy
import math


def remove_from_list(container, value):
    try:
        container.remove(value)
    except ValueError:
        pass
    return container


def pop_from_container(container, value):
    try:
        container.pop(value)
    except ValueError:
        pass
    return container


def update_dict(dictionary, entries):
    dictionary.update(entries)
    return dictionary


# functions callable on storable data on the server by clients
modify_functions = {
    "add": operator.add,  # add together two objects, using python's "+" operator (works on strings and lists as append)
    "mul": operator.mul,
    "mod": operator.mod,
    "max": max,
    "min": min,
    "replace": lambda old, new: new,
    "default": lambda old, new: old,
    "pow": operator.pow,
    "floor": lambda value, _: math.floor(value),
    "ceil": lambda value, _: math.ceil(value),
    # bitwise:
    "xor": operator.xor,
    "or": operator.or_,
    "and": operator.and_,
    "left_shift": operator.lshift,
    "right_shift": operator.rshift,
    # lists/dicts
    "remove": remove_from_list,
    "pop": pop_from_container,
    "update": update_dict,
}


class InvalidArgumentsException(Exception):
    pass


class DataStorage:
    data: Dict[str, Any]

    def __init__(self, data: Dict[str, Any]):
        self.data = data

    @staticmethod
    def validate_and_get_key(set_cmd: Dict[str, Any]) -> str:
        try:
            key = set_cmd["key"]
            if not isinstance(key, str):
                raise InvalidArgumentsException(f"key has to be a string")
            if key.startswith("_read_"):
                raise InvalidArgumentsException(f"cannot apply `Set` operation to the read only key `{key}`")
            if not isinstance(set_cmd["operations"], List):
                raise InvalidArgumentsException("`operations` is not a list")
        except (KeyError, AttributeError) as e:
            raise InvalidArgumentsException(str(e))
        return key

    def set(self, client_slot: int | None, set_cmd: Dict[str, Any]) -> Dict[str, Any]:
        key = self.validate_and_get_key(set_cmd)
        value = self.data.get(key, set_cmd.get("default", 0))
        on_error = set_cmd.get("on_error", "raise")

        set_cmd.update({
            "cmd": "SetReply",
            "original_value": copy.copy(value),
            "slot": client_slot
        })

        try:
            for operation in set_cmd["operations"]:
                try:
                    func = modify_functions[operation["operation"]]
                    value = func(value, operation["value"])
                except Exception:
                    if on_error != "ignore":
                        raise
        except Exception:
            if on_error == "set_default":
                value = set_cmd.get("default", 0)
            elif on_error == "undo":
                value = set_cmd["original_value"]
            elif on_error == "abort":
                pass  # don't process further operations
            else:
                raise

        self.data[key] = set_cmd["value"] = value

        return set_cmd
