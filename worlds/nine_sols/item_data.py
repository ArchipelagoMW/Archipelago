from .shared_static_logic.items import items_data

jade_items = set(entry["name"] for entry in items_data if (" Jade" in entry["name"]))
