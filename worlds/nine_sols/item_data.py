import pkgutil

from Utils import restricted_loads

pickled_data = pkgutil.get_data(__name__, "shared_static_logic/static_logic.pickle")
items_data = restricted_loads(pickled_data)["ITEMS"]

jade_items = set(entry["name"] for entry in items_data if (" Jade" in entry["name"]))
