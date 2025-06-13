DYNAMIC_FLAGS = {
    # "name (for humans)": {
    #   "on_scene": int,        - will trigger on scene
    #   "requires_item": str    - will trigger if got item (from ctx)
    #   "requries_location: str - will trigger if got location (from ctx)
    #   "address": int          - address to write to
    #   "bit": int              - bit in address to set
    #   "unset": bool           - will unset the bit on scene change or item acquisition
    #   "if_not_have_item": bool- will trigger on not having item,
    #   "remove_bit": bool      - unset bit, works with unset
    # }
    "Cannon island buy salvage without cannon": {
        "on_scene": 0x130B,
        "requires_location": "Cannon Island Cannon",
        "bit": 1,
        "address": 0x1B5582,
        "unset": True
    },
    "Cannon island buy cannon with cannon": {
        "on_scene": 0x130B,
        "requires_item": "Cannon",
        "remove_bit": True,
        "bit": 1,
        "address": 0x1B5582,
        "unset": True,
        "stop_on_read": [(0x1BA649, 2)]
    },
    "Cannon island buy salvage arm with arm": {
        "on_scene": 0x130B,
        "requires_item": "Salvage Arm",
        "remove_bit": True,
        "bit": 0x10,
        "address": 0x1BA649,
        "unset": True
    },
    "Astrid basement treasure map": {
        "on_scene": 0xD01,
        "requires_item": "Treasure Map #3",
        "remove_bit": True,
        "address": 0x1BA651,
        "bit": 0x20,
        "unset": True
    },
    "Ember summit treasure map": {
        "on_scene": 0xD01,
        "requires_item": "Treasure Map #4",
        "remove_bit": True,
        "address": 0x1BA651,
        "bit": 0x80,
        "unset": True
    },
    "Mercay yellow guy treasure map": {
        "on_scene": 0xB03,
        "requires_item": "Treasure Map #9",
        "remove_bit": True,
        "address": 0x1BA650,
        "bit": 0x02,
        "unset": True
    },
    "Mercay freedle gift treasure map": {
        "on_scene": 0xB03,
        "requires_item": "Treasure Map #12",
        "remove_bit": True,
        "address": 0x1BA652,
        "bit": 0x20,
        "unset": True
    },
    "Mercay oshus dig treasure map": {
        "on_scene": 0xB03,
        "requires_item": "Treasure Map #10",
        "remove_bit": True,
        "address": 0x1BA651,
        "bit": 0x10,
        "unset": True
    },
}
