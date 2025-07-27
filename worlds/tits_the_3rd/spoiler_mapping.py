import re

def _add_lower_case_mapping(mapping: dict[str, str]) -> dict[str, str]:
    return {key.lower(): value.lower() for key, value in mapping.items()}

def _build_mapping() -> dict[str, str]:
    base_mapping = {
        "Estelle": "Chapter 5 First Character",
        "Joshua": "Chapter 2 Third Character",
        "Scherazard": "Chapter 4 Third Character",
        "Olivier": "Chapter 4 Second Character",
        "Kloe": "Chapter 3 First Character",
        "Agate": "Chapter 4 Fourth Character",
        "Tita": "Chapter 1 First Character",
        "Zin": "Chapter 4 First Character",
        "Kevin": "Male Default Character",
        "Anelace": "Chapter 4 Third Character",
        "Josette": "Chapter 2 Second Character",
        "Richard": "Chapter 5 Second Character",
        "Mueller": "Chapter 2 First Character",
        "Julia": "Chapter 1 Second Character",
        "Ries": "Female Default Character",
        "Renne": "Chapter 5 Third Character",
    }
    return {
        **base_mapping,
        **_add_lower_case_mapping(base_mapping),
    }

def _is_craft_location(name: str) -> bool:
    return "Craft Unlock" in name

def _add_craft_to_spoiler_mapping(name: str) -> None:
    global _scrub_counter
    global _spoiler_mapping

    match = re.match(r".*Craft Unlock.* - (.+)", name)
    if not match:
        raise ValueError(f"Invalid craft location name: {name}")
    craft_name = match.group(1)
    if craft_name in _spoiler_mapping:
        return
    _spoiler_mapping[craft_name] = f"Craft {str(_scrub_counter)}"
    _spoiler_mapping[craft_name.lower()] = f"craft {str(_scrub_counter)}"
    _scrub_counter += 1

_spoiler_mapping = _build_mapping()
_scrub_counter = 1

def scrub_spoiler_data(data: str) -> str:
    """
    Scrubs the spoiler data from the given string.
    """
    if _is_craft_location(data):
        _add_craft_to_spoiler_mapping(data)
    for key, value in _spoiler_mapping.items():
        # Only replace if the key is a whole word (not part of another word)
        data = re.sub(rf'\b{re.escape(key)}\b', value, data)
    return data
