from BaseClasses import Item
from .BaseID import base_id


class CCCharlesItem(Item):
    game = "Choo-Choo Charles"


optional_items = {
    "Scraps": base_id + 1,
    "30 Scraps Reward": base_id + 2,
    "25 Scraps Reward": base_id + 3,
    "35 Scraps Reward": base_id + 4,
    "40 Scraps Reward": base_id + 5,
    "South Mine Key": base_id + 6,
    "North Mine Key": base_id + 7,
    "Mountain Ruin Key": base_id + 8,
    "Barn Key": base_id + 9,
    "Candice's Key": base_id + 10,
    "Dead Fish": base_id + 11,
    "Lockpicks": base_id + 12,
    "Ancient Tablet": base_id + 13,
    "Blue Box": base_id + 14,
    "Page Drawing": base_id + 15,
    "Journal": base_id + 16,
    "Timed Dynamite": base_id + 17,
    "Box of Rockets": base_id + 18,
    "Breaker": base_id + 19,
    "Broken Bob": base_id + 20,
    "Employment Contracts": base_id + 21,
    "Mob Camp Key": base_id + 22,
    "Jar of Pickles": base_id + 23
}

useless_items = {
    "Orange Paint Can": base_id + 24,
    "Green Paint Can": base_id + 25,
    "White Paint Can": base_id + 26,
    "Pink Paint Can": base_id + 27,
    "Grey Paint Can": base_id + 28,
    "Blue Paint Can": base_id + 29,
    "Black Paint Can": base_id + 30,
    "Lime Paint Can": base_id + 31,
    "Teal Paint Can": base_id + 32,
    "Red Paint Can": base_id + 33,
    "Purple Paint Can": base_id + 34,
    "The Boomer": base_id + 35,
    "Bob": base_id + 36
}

progression_items = {
    "Green Egg": base_id + 37,
    "Blue Egg": base_id + 38,
    "Red Egg": base_id + 39,
    "Remote Explosive": base_id + 40,
    "Remote Explosive x8": base_id + 41, # Originally, Paul gives 8 explosives at once
    "Temple Key": base_id + 42,
    "Bug Spray": base_id + 43 # Should only be considered progressive in Nightmare Mode
}

item_groups = {
    "Weapons": {
        "Bug Spray",
        "The Boomer",
        "Bob"
    },
    "Paint Can": {
        "Orange Paint Can",
        "Green Paint Can",
        "White Paint Can",
        "Pink Paint Can",
        "Grey Paint Can",
        "Blue Paint Can",
        "Black Paint Can",
        "Lime Paint Can",
        "Teal Paint Can",
        "Red Paint Can",
        "Purple Paint Can"
    },
    "Train Upgrade": {
        "Scraps",
        "30 Scraps Reward",
        "25 Scraps Reward",
        "40 Scraps Reward"
    },
    "Dungeon Keys": {
        "South Mine Key",
        "North Mine Key",
        "Mountain Ruin Key"
    },
    "Building Keys": {
        "Barn Key",
        "Candice's Key",
        "Mob Camp Key",
        "Temple Key"
    },
    "Mission Items": {
        "Dead Fish",
        "Lockpicks",
        "Ancient Tablet",
        "Blue Box",
        "Page Drawing",
        "Journal",
        "Timed Dynamite",
        "Box of Rockets",
        "Breaker",
        "Broken Bob",
        "Employment Contracts",
        "Jar of Pickles",
        "Remote Explosive",
        "Remote Explosive x8"
    },
    "Eggs": {
        "Green Egg",
        "Blue Egg",
        "Red Egg"
    }
}


# All items excepted the duplications (no item amount)
unique_item_dict = {**optional_items, **useless_items, **progression_items}

# All 691 items to add to the item pool
full_item_list = []
full_item_list += ["Scraps"] * 637 # 636 + 1 as Scrap Reward (from Ronny)
full_item_list += ["30 Scraps Reward"] * 3
full_item_list += ["25 Scraps Reward"] * 1
full_item_list += ["35 Scraps Reward"] * 2
full_item_list += ["40 Scraps Reward"] * 1
full_item_list += ["South Mine Key"] * 1
full_item_list += ["North Mine Key"] * 1
full_item_list += ["Mountain Ruin Key"] * 1
full_item_list += ["Barn Key"] * 1
full_item_list += ["Candice's Key"] * 1
full_item_list += ["Dead Fish"] * 1
full_item_list += ["Lockpicks"] * 1
full_item_list += ["Ancient Tablet"] * 1
full_item_list += ["Blue Box"] * 1
full_item_list += ["Page Drawing"] * 8
full_item_list += ["Journal"] * 1
full_item_list += ["Timed Dynamite"] * 1
full_item_list += ["Box of Rockets"] * 1
full_item_list += ["Breaker"] * 4
full_item_list += ["Broken Bob"] * 1
full_item_list += ["Employment Contracts"] * 1
full_item_list += ["Mob Camp Key"] * 1
full_item_list += ["Jar of Pickles"] * 1
full_item_list += ["Orange Paint Can"] * 1
full_item_list += ["Green Paint Can"] * 1
full_item_list += ["White Paint Can"] * 1
full_item_list += ["Pink Paint Can"] * 1
full_item_list += ["Grey Paint Can"] * 1
full_item_list += ["Blue Paint Can"] * 1
full_item_list += ["Black Paint Can"] * 1
full_item_list += ["Lime Paint Can"] * 1
full_item_list += ["Teal Paint Can"] * 1
full_item_list += ["Red Paint Can"] * 1
full_item_list += ["Purple Paint Can"] * 1
full_item_list += ["The Boomer"] * 1
full_item_list += ["Bob"] * 1
full_item_list += ["Green Egg"] * 1
full_item_list += ["Blue Egg"] * 1
full_item_list += ["Red Egg"] * 1
full_item_list += ["Remote Explosive x8"] * 1
full_item_list += ["Temple Key"] * 1
full_item_list += ["Bug Spray"] * 1
