

# TODO: Add sram data for saveslot 2
# TODO: Add the rest of sram data in bulk

LOCATIONS_DATA = {

    #Aboda Village
    "Aboda Clear Rocks": {
        "region_id": "aboda village rocks",
        "vanilla_item": "Red Rupee (20)",
        "stage_id": 0x2F,
        "floor_id": 0,
        "address": 0x265743,
        "value": 0x20,
        "item_override": "Sword (Progressive)"
    },
    "Aboda Bee Tree": {
        "region_id": "aboda village bees",
        "vanilla_item": "Treasure",
        "stage_id": 0x2F,
        "floor_id": 0,
        "x_min": 34192,
        "x_max": 52960,
        "z_min": -34890,
        "z_max": -10024
    },
    "Aboda Stamp Station": {
        "region_id": "aboda village stamp station",
        #"vanilla_item": "Aboda Village Stamp",
        "vanilla_item": "Red Rupee (20)",
        "item_override": "Stamp Book",
        "stage_id": 0x2F,
        "floor_id": 0,
        "stamp": True,
        "require_item": ["Stamp Book"],
        "x_min": -47131,
        "x_max": -29971,
        "z_min": -38607,
        "z_max": -23820
        # 02271CD8 is array of stamp IDs
        # 02271CF4 is bitfield of all stamps found
    },

    # Castle Town
    "Castle Town Stamp Station": {
        "region_id": "castle town stamp station",
        "vanilla_item": "Red Rupee (20)",
        #"vanilla_item": "Castle Town Stamp",
        "stage_id": 0x29,
        "floor_id": 0,
        "x_min": -104858,
        "x_max": -86873,
        "z_min": -76186,
        "z_max": -58479,
        #"y": 0x1333,
        "stamp": True,
        "require_item": ["Stamp Book"]
    },


    # # Shops
    # "Masked Beedle Courage Gem": {
    #     "region_id": "masked ship gem",
    #     "vanilla_item": "Courage Gem",
    #     "stage_id": 5,
    #     "floor_id": 0,
    #     "address": 0x1B558A,
    #     "value": 0x02,
    #     "conditional": True,
    #     "delay_reset": True
    # },

    # # ========== Tower of Spirits ==============

    "ToS Forest Rail Glyph": {
        "region_id": "3f rail map",
        "vanilla_item": "Forest Glyph",
        "stage_id": 0x13,
        #"floor_id": 2,
        #"y": 0x1333,
        'dungeon': "Tower of Spirits",
        "require_item": ["Sword (Progressive)"]
        #'set_bit': [(0x265715, 0x80)]
    },
    # "TotOK 1F Linebeck Key": {
    #     "region_id": "totok",
    #     "vanilla_item": "Small Key (Temple of the Ocean King)",
    #     "stage_id": 37,
    #     "floor_id": 0,
    #     "z_min": 0xB000,
    #     "z_max": 0x11000,
    #     "x_min": -100,
    #     'set_bit': [(0x1B557D, 2)],
    #     'dungeon': "Temple of the Ocean King"
    # },
    # "TotOK 1F Empty Chest": {
    #     "region_id": "totok",
    #     "vanilla_item": "Nothing!",
    #     "stage_id": 37,
    #     "floor_id": 0,
    #     "x_min": 0x4000,
    #     'dungeon': "Temple of the Ocean King"
    # },
    # "TotOK B1 Small Key": {
    #     "region_id": "totok b1 key",
    #     "vanilla_item": "Small Key (Temple of the Ocean King)",
    #     "stage_id": 37,
    #     "floor_id": 1,
    #     "y": 0x1333,
    #     'dungeon': "Temple of the Ocean King"
    # },
    # "TotOK B1 Shoot Eye Chest": {
    #     "region_id": "totok b1 eye chest",
    #     "vanilla_item": "Courage Gem",
    #     "stage_id": 37,
    #     "floor_id": 1,
    #     "x_min": 0xB000,
    #     "x_max": 0x10000,
    #     'dungeon': "Temple of the Ocean King"
    # },
    # "TotOK B2 Bombchu Chest": {
    #     "region_id": "totok b2 bombchu chest",
    #     "vanilla_item": "Wisdom Gem",
    #     "stage_id": 37,
    #     "floor_id": 2,
    #     "x_min": 0xD800,
    #     "x_max": 0x10000,
    #     "require_item": ["Bombchus (Progressive)", "Hammer"],
    #     "delay_pickup": "TotOK B2 Small Key",
    #     'dungeon': "Temple of the Ocean King"
    # },
    # "TotOK B2 Phantom Chest": {
    #     "region_id": "totok b2 phantom chest",
    #     "vanilla_item": "Treasure",
    #     "farmable": True,
    #     "stage_id": 37,
    #     "floor_id": 2,
    #     "z_min": 0x7000,
    #     "z_max": 0xF000,
    #     "delay_pickup": "TotOK B2 Small Key",
    #     'dungeon': "Temple of the Ocean King"
    # },

    # Whittleton

    # Rabbitland Rescue

    # Forest Sanctuary

    # Forest Temple

    # Trading Post

}

for i, name in enumerate(LOCATIONS_DATA):
    LOCATIONS_DATA[name]["id"] = i+1

if __name__ == "__main__":
    for location, data in LOCATIONS_DATA.items():
        print(f"{location} | {data['region_id']} | id: {data['id']} | stage: {data['stage_id']} | room: {data['floor_id']}")
