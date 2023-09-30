from typing import Dict, List
import operator
import copy

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

class DataStorage:
    stored_data: Dict[str, object]

    def __init__(self, stored_data: Dict[str, object]):
        self.stored_data = stored_data

    def is_valid_set_cmd(set_cmd: Dict[str, object]) -> bool:
        return "key" in set_cmd and type(set_cmd["key"]) == str and not set_cmd["key"].startswith("_read_") \
            and "operations" in set_cmd and not type(set_cmd["operations"]) == list

    def set(self, set_cmd: Dict[str, object]) -> Dict[str, object]:
        response: Dict[str, object] = {
            "cmd": "SetReply",
            "key": set_cmd["key"]
        }

        value = self.stored_data.get(set_cmd["key"], set_cmd.get("default", 0))
        response["original_value"] = copy.copy(value)
        on_error =  set_cmd.get("on_error", "raise")

        try:
            for operation in set_cmd["operations"]:
                try:
                    func = modify_functions[operation["operation"]]
                    value = func(value, operation["value"])
                except:
                    if on_error != "ignore":
                        raise
        except:
            if (on_error == "set_default"):
                value = set_cmd.get("default", 0)
            elif (on_error == "undo"):
                value =  response["original_value"]
            elif (on_error == "abort"):
                pass # dont process further operations
            else:
                raise

        self.stored_data[set_cmd["key"]] = response["value"] = value

        return response







