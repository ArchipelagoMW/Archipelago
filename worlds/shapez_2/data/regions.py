
regions_list: list[str] = [
    "Menu",
    "Events",
    *(f"Milestone {x}" for x in range(1, 21)),
    *(f"Task line {x}" for x in range(1, 201)),
    *(f"Operator levels (section {x})" for x in range(1, 41)),
]
