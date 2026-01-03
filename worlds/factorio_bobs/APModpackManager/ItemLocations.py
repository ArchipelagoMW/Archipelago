import hashlib

items_to_id: dict[str, int] = {}
"""
items to id for all loaded packs
This is also given to ap
"""
id_to_items: dict[int, str] = {}
"""
id to items for all loaded packs
"""

def add_item(name: str, item_id: int | None = None, bump = 0) -> int:
    """
    adds a new item to the global item table

    if item_id is None, the hash of the name will be used
    returns item_id

    raises ValueError if item_id is the same as already registered item with different name
    implement and use bump to avoid this
    TODO report which modpacks caused collision
    """
    if item_id is None:
        item_id = int(hashlib.sha256(name.encode("utf-8")).hexdigest(), 16) + bump
    if item_id in id_to_items and id_to_items[item_id] != name:
        raise ValueError(f"Item {id_to_items[item_id]} and {name} has had item collision with id: {item_id}",
                         "discover which packs implement them and report the error to their creators ")
    id_to_items[item_id] = name
    items_to_id[name] = item_id
    return item_id

locations_to_id: dict[str, int] = {}
"""
locations to id for all loaded packs
This is also given to ap
"""
id_to_locations: dict[int, str] = {}
"""
id to locations for all loaded packs
"""

def add_location(name: str, location_id: int | None = None, bump = 0) -> int:
    """
    adds a new location to the global location table

    if location_id is None, the hash of the name will be used
    returns location_id

    raises ValueError if location_id is the same as already registered location with different name
    implement and use bump to avoid this
    TODO report which modpacks caused collision
    """
    if location_id is None:
        location_id = int(hashlib.sha256(name.encode("utf-8")).hexdigest(), 16) + bump
    if location_id in id_to_locations and id_to_locations[location_id] != name:
        raise ValueError(f"location {id_to_locations[location_id]} and {name} has had location collision with id: {location_id}",
                         "discover which packs implement them and report the error to their creators ")
    id_to_locations[location_id] = name
    locations_to_id[name] = location_id
    return location_id
