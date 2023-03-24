from .data import data

def location_name_to_label(name: str) -> str:
    return data.locations[name].label
