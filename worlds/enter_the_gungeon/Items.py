from BaseClasses import Item

class GungeonItem(Item):
    game: str = "Enter The Gungeon"

item_table = { }

normal_item_table = {
    "Random D Tier Gun": 8754000,
    "Random C Tier Gun": 8754001,
    "Random B Tier Gun": 8754002,
    "Random A Tier Gun": 8754003,
    "Random S Tier Gun": 8754004,
    "Random D Tier Item": 8754005,
    "Random C Tier Item": 8754006,
    "Random B Tier Item": 8754007,
    "Random A Tier Item": 8754008,
    "Random S Tier Item": 8754009,
    "Gnawed Key": 8754010,
    "Old Crest": 8754011,
    "Weird Egg": 8754012,
}

pickup_item_table = {
    "Chancekin Party": 8754100,
    "50 Casings": 8754101,
    "Key": 8754102,
    "Blank": 8754103,
    "Armor": 8754104,
    "Heart": 8754105,
    "Ammo": 8754106,
}

trap_item_table = {
    "Rat Invasion": 8754200,
    "Shelleton Men": 8754201,
    "Shotgrub Storm": 8754202,
    "Tanker Battalion": 8754203,
    "Ghost Party": 8754204,
    "Gun Nut Gang": 8754205,
    "Triple Jamerlengo Bats": 8754206,
    "Lord of the Jammed": 8754207,
}

item_table.update(normal_item_table)
item_table.update(pickup_item_table)
item_table.update(trap_item_table)
