from typing import Any

import orjson
import pkgutil

# Factorio technologies are imported from a .json document in /data
def load_json_data(data_name: str) -> list[str] | dict[str, Any]:
    return orjson.loads(pkgutil.get_data(__name__, "data/" + data_name + ".json"))

class FactorioElement:
    name: str

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"

    def __hash__(self):
        return hash(self.name)
