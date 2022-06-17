from BaseClasses import Item
import typing


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool


class Psychonauts2Item(Item):
    game: str = "Psychonauts 2"


item_table = {
    # PSI Powers
    "Telekinesis": ItemData(20210825, True),
    "PSI Blast": ItemData(20210826, True),
    "Pyrokinesis": ItemData(20210827, True),
    "Levitation": ItemData(20210828, True),
    "Clairvoyance": ItemData(20210829, True),
    "Mental Connection": ItemData(20210830, True),
    "Time Bubble": ItemData(20210831, True),
    "Projection": ItemData(20210832, True),

    # Other important items
    "Thought Tuner": ItemData(20210833, False),
    "Brain in a Jar": ItemData(20210834, True),
    "Empty Specimen Jar": ItemData(20210835, True),
    "Senior League Membership Card": ItemData(20210836, True),

    # Overworld Collectibles (generic)
    "PSI Card": ItemData(20210837, False),
    "Supply Chest": ItemData(20210838, False),
    "Supply Chest Key": ItemData(20210839, False),
    "PSI Challenge Marker": ItemData(20210840, False),

    # Mind Collectibles (generic)
    "Nugget of Wisdom": ItemData(20210841, False),
    "Half-A-Mind": ItemData(20210842, False),

    # Emotional Baggage
    "Steamer Trunk (Loboto's Labyrinth)": ItemData(20210843, False),
    "Steamer Trunk Tag (Loboto's Labyrinth)": ItemData(20210844, False),
    "Dufflebag (Loboto's Labyrinth)": ItemData(20210845, False),
    "Dufflebag Tag (Loboto's Labyrinth)": ItemData(20210846, False),
    "Suitcase (Loboto's Labyrinth)": ItemData(20210847, False),
    "Suitcase Tag (Loboto's Labyrinth)": ItemData(20210848, False),
    "Hatbox (Loboto's Labyrinth)": ItemData(20210849, False),
    "Hatbox Tag (Loboto's Labyrinth)": ItemData(20210850, False),
    "Purse (Loboto's Labyrinth)": ItemData(20210851, False),
    "Purse Tag (Loboto's Labyrinth)": ItemData(20210852, False),

    "Steamer Trunk (Hollis' Classroom)": ItemData(20210853, False),
    "Steamer Trunk Tag (Hollis' Classroom)": ItemData(20210854, False),
    "Hatbox (Hollis' Classroom)": ItemData(20210855, False),
    "Hatbox Tag (Hollis' Classroom)": ItemData(20210856, False),

    "Dufflebag (Hollis' Hot Streak)": ItemData(20210857, False),
    "Dufflebag Tag (Hollis' Hot Streak)": ItemData(20210858, False),
    "Suitcase (Hollis' Hot Streak)": ItemData(20210859, False),
    "Suitcase Tag (Hollis' Hot Streak)": ItemData(20210860, False),
    "Purse (Hollis' Hot Streak)": ItemData(20210861, False),
    "Purse Tag (Hollis' Hot Streak)": ItemData(20210862, False),

    "Steamer Trunk (PSI King's Sensorium)": ItemData(20210863, False),
    "Steamer Trunk Tag (PSI King's Sensorium)": ItemData(20210864, False),
    "Dufflebag (PSI King's Sensorium)": ItemData(20210865, False),
    "Dufflebag Tag (PSI King's Sensorium)": ItemData(20210866, False),
    "Suitcase (PSI King's Sensorium)": ItemData(20210867, False),
    "Suitcase Tag (PSI King's Sensorium)": ItemData(20210868, False),
    "Hatbox (PSI King's Sensorium)": ItemData(20210869, False),
    "Hatbox Tag (PSI King's Sensorium)": ItemData(20210870, False),
    "Purse (PSI King's Sensorium)": ItemData(20210871, False),
    "Purse Tag (PSI King's Sensorium)": ItemData(20210872, False),

    "Steamer Trunk (Compton's Cookoff)": ItemData(20210873, False),
    "Steamer Trunk Tag (Compton's Cookoff)": ItemData(20210874, False),
    "Dufflebag (Compton's Cookoff)": ItemData(20210875, False),
    "Dufflebag Tag (Compton's Cookoff)": ItemData(20210876, False),
    "Suitcase (Compton's Cookoff)": ItemData(20210877, False),
    "Suitcase Tag (Compton's Cookoff)": ItemData(20210878, False),
    "Hatbox (Compton's Cookoff)": ItemData(20210879, False),
    "Hatbox Tag (Compton's Cookoff)": ItemData(20210880, False),
    "Purse (Compton's Cookoff)": ItemData(20210881, False),
    "Purse Tag (Compton's Cookoff)": ItemData(20210882, False),

    "Hatbox (Cruller's Correspondence)": ItemData(20210883, False),
    "Hatbox Tag (Cruller's Correspondence)": ItemData(20210884, False),
    "Dufflebag (Strike City)": ItemData(20210885, False),
    "Dufflebag Tag (Strike City)": ItemData(20210886, False),
    "Suitcase (Strike City)": ItemData(20210887, False),
    "Suitcase Tag (Strike City)": ItemData(20210888, False),
    "Steamer Trunk (Ford's Follicles)": ItemData(20210889, False),
    "Steamer Trunk Tag (Ford's Follicles)": ItemData(20210890, False),
    "Purse (Tomb of the Sharkophagus)": ItemData(20210891, False),
    "Purse Tag (Tomb of the Sharkophagus)": ItemData(20210892, False),

    "Steamer Trunk (Cassie's Collection)": ItemData(20210893, False),
    "Steamer Trunk Tag (Cassie's Collection)": ItemData(20210894, False),
    "Dufflebag (Cassie's Collection)": ItemData(20210895, False),
    "Dufflebag Tag (Cassie's Collection)": ItemData(20210896, False),
    "Suitcase (Cassie's Collection)": ItemData(20210897, False),
    "Suitcase Tag (Cassie's Collection)": ItemData(20210898, False),
    "Hatbox (Cassie's Collection)": ItemData(20210899, False),
    "Hatbox Tag (Cassie's Collection)": ItemData(20210900, False),
    "Purse (Cassie's Collection)": ItemData(20210901, False),
    "Purse Tag (Cassie's Collection)": ItemData(20210902, False),

    "Steamer Trunk (Bob's Bottles)": ItemData(20210902, False),
    "Steamer Trunk Tag (Bob's Bottles)": ItemData(20210903, False),
    "Dufflebag (Bob's Bottles)": ItemData(20210904, False),
    "Dufflebag Tag (Bob's Bottles)": ItemData(20210905, False),
    "Suitcase (Bob's Bottles)": ItemData(20210906, False),
    "Suitcase Tag (Bob's Bottles)": ItemData(20210907, False),
    "Hatbox (Bob's Bottles)": ItemData(20210908, False),
    "Hatbox Tag (Bob's Bottles)": ItemData(20210909, False),
    "Purse (Bob's Bottles)": ItemData(20210910, False),
    "Purse Tag (Bob's Bottles)": ItemData(20210911, False),

    "Steamer Trunk (Lucrecia's Lament)": ItemData(20210912, False),
    "Steamer Trunk Tag (Lucrecia's Lament)": ItemData(20210913, False),
    "Dufflebag (Lucrecia's Lament)": ItemData(20210914, False),
    "Dufflebag Tag (Lucrecia's Lament)": ItemData(20210915, False),
    "Suitcase (Lucrecia's Lament)": ItemData(20210916, False),
    "Suitcase Tag (Lucrecia's Lament)": ItemData(20210917, False),
    "Hatbox (Lucrecia's Lament)": ItemData(20210918, False),
    "Hatbox Tag (Lucrecia's Lament)": ItemData(20210919, False),
    "Purse (Lucrecia's Lament)": ItemData(20210920, False),
    "Purse Tag (Lucrecia's Lament)": ItemData(20210921, False),

    "Steamer Trunk (Fatherland Follies)": ItemData(20210922, False),
    "Steamer Trunk Tag (Fatherland Follies)": ItemData(20210923, False),
    "Dufflebag (Fatherland Follies)": ItemData(20210924, False),
    "Dufflebag Tag (Fatherland Follies)": ItemData(20210925, False),
    "Suitcase (Fatherland Follies)": ItemData(20210926, False),
    "Suitcase Tag (Fatherland Follies)": ItemData(20210927, False),
    "Hatbox (Fatherland Follies)": ItemData(20210928, False),
    "Hatbox Tag (Fatherland Follies)": ItemData(20210929, False),
    "Purse (Fatherland Follies)": ItemData(20210930, False),
    "Purse Tag (Fatherland Follies)": ItemData(20210931, False),


    # Memory Vaults
    "Memory Vault (Loboto's Labyrinth, 1)": ItemData(20210932, False), 
    "Memory Vault (Loboto's Labyrinth, 2)": ItemData(20210933, False), 

    "Memory Vault (Hollis' Classroom)": ItemData(20210934, False), 
    "Memory Vault (Hollis' Hot Streak)": ItemData(20210935, False), 

    "Memory Vault (PSI King's Sensorium, 1)": ItemData(20210936, False), 
    "Memory Vault (PSI King's Sensorium, 2)": ItemData(20210937, False), 

    "Memory Vault (Compton's Cookoff, 1)": ItemData(20210938, False), 
    "Memory Vault (Compton's Cookoff, 2)": ItemData(20210939, False), 

    "Memory Vault (Cruller's Correspondence)": ItemData(20210940, False), 
    "Memory Vault (Strike City)": ItemData(20210941, False), 
    "Memory Vault (Ford's Follicles)": ItemData(20210942, False), 
    "Memory Vault (Tomb of the Sharkophagus)": ItemData(20210943, False), 

    "Memory Vault (Cassie's Collection, 1)": ItemData(20210944, False), 
    "Memory Vault (Cassie's Collection, 2)": ItemData(20210945, False), 

    "Memory Vault (Bob's Bottles, 1)": ItemData(20210946, False), 
    "Memory Vault (Bob's Bottles, 2)": ItemData(20210947, False), 

    "Memory Vault (Lucrecia's Lament, 1)": ItemData(20210948, False), 
    "Memory Vault (Lucrecia's Lament, 2)": ItemData(20210949, False), 

    "Memory Vault (Fatherland Follies, 1)": ItemData(20210950, False), 
    "Memory Vault (Fatherland Follies, 2)": ItemData(20210951, False), 


    "Victory": ItemData(None, True)
}

item_frequencies = {
    "PSI Card": 99,
    "Supply Chest": 16,
    "Supply Chest Key": 16,
    "PSI Challenge Marker": 24,
    "Nugget of Wisdom": 29,
    "Half-A-Mind": 22,
}

required_items = {
    "Telekinesis": 1,
    "PSI Blast": 1,
    "Pyrokinesis": 1,
    "Levitation": 1,
    "Clairvoyance": 1,
    "Mental Connection": 1,
    "Time Bubble": 1,
    "Projection": 1,
    "Brain in a Jar": 1,
    "Empty Specimen Jar": 1,
    "Senior League Membership Card": 1,
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}