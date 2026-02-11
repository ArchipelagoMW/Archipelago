
base_id = 20010707

zone_names_without_f_zone: list[str] = [
    "Leaf Storm",
    "Water Palace",
    "Mirage Road",
    "Night Carnival",
    "Huge Crisis",
    "Altitude Limit",
    "Dead Line",
]

zone_names: list[str] = zone_names_without_f_zone + ["F-Zone"]

emerald_colors: list[str] = [
    "Red",
    "Blue",
    "Yellow",
    "Green",
    "White",
    "Turquoise",
    "Purple",
]

emerald_bits_by_name: dict[str, int] = {
    "Red": 0,
    "Blue": 1,
    "Yellow": 2,
    "Green": 3,
    "White": 4,
    "Turquoise": 5,
    "Purple": 6,
}

region_names: list[str] = [
    f"{zone} ({char})"
    for zone in zone_names
    for char in ["Sonic", "Blaze"]
] + [
    "Extra Zone",
    "Goal",
    "Menu",
]

zone_number_by_name: dict[str, dict[str, int]] = {
    "Sonic": {
        "Leaf Storm": 1,
        "Water Palace": 2,
        "Mirage Road": 3,
        "Night Carnival": 4,
        "Huge Crisis": 5,
        "Altitude Limit": 6,
        "Dead Line": 7,
    },
    "Blaze": {
        "Leaf Storm": 2,
        "Water Palace": 4,
        "Mirage Road": 3,
        "Night Carnival": 1,
        "Huge Crisis": 6,
        "Altitude Limit": 5,
        "Dead Line": 7,
    },
}

zone_name_by_number: dict[str, dict[int, str]] = {
    "Sonic": {
        1: "Leaf Storm",
        2: "Water Palace",
        3: "Mirage Road",
        4: "Night Carnival",
        5: "Huge Crisis",
        6: "Altitude Limit",
        7: "Dead Line",
    },
    "Blaze": {
        2: "Leaf Storm",
        4: "Water Palace",
        3: "Mirage Road",
        1: "Night Carnival",
        6: "Huge Crisis",
        5: "Altitude Limit",
        7: "Dead Line",
    },
}
