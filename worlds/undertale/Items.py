from BaseClasses import Item, ItemClassification
import typing
from .er_data import door_name_list


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classification: any


class UndertaleItem(Item):
    game: str = "Undertale"


item_table = {
    # "Progressive Plot": ItemData(77700, ItemClassification.progression),
    "Progressive Weapons": ItemData(77701, ItemClassification.progression_skip_balancing),
    "Progressive Armor": ItemData(77702, ItemClassification.progression_skip_balancing),
    "Monster Candy": ItemData(77001, ItemClassification.filler),
    "Croquet Roll": ItemData(77002, ItemClassification.filler),
    "Stick": ItemData(77003, ItemClassification.useful),
    "Bandage": ItemData(77004, ItemClassification.useful),
    "Rock Candy": ItemData(77005, ItemClassification.filler),
    "Pumpkin Rings": ItemData(77006, ItemClassification.filler),
    "Spider Donut": ItemData(77007, ItemClassification.filler),
    "Stoic Onion": ItemData(77008, ItemClassification.filler),
    "Ghost Fruit": ItemData(77009, ItemClassification.filler),
    "Spider Cider": ItemData(77010, ItemClassification.filler),
    "Butterscotch Pie": ItemData(77011, ItemClassification.useful),
    "Faded Ribbon": ItemData(77012, ItemClassification.progression_skip_balancing),
    "Toy Knife": ItemData(77013, ItemClassification.progression_skip_balancing),
    "Tough Glove": ItemData(77014, ItemClassification.progression_skip_balancing),
    "Manly Bandanna": ItemData(77015, ItemClassification.progression_skip_balancing),
    "Snowman Piece": ItemData(77016, ItemClassification.useful),
    "Nice Cream": ItemData(77017, ItemClassification.filler),
    "Puppydough Icecream": ItemData(77018, ItemClassification.useful),
    "Bisicle": ItemData(77019, ItemClassification.filler),
    "Unisicle": ItemData(77020, ItemClassification.filler),
    "Cinnamon Bun": ItemData(77021, ItemClassification.useful),
    "Temmie Flakes": ItemData(77022, ItemClassification.filler),
    "Abandoned Quiche": ItemData(77023, ItemClassification.useful),
    "Old Tutu": ItemData(77024, ItemClassification.progression_skip_balancing),
    "Ballet Shoes": ItemData(77025, ItemClassification.progression_skip_balancing),
    "Punch Card": ItemData(77026, ItemClassification.filler),
    "Annoying Dog": ItemData(77027, ItemClassification.filler),
    "Dog Salad": ItemData(77028, ItemClassification.filler),
    "Dog Residue": ItemData(77029, ItemClassification.filler),
    "Astronaut Food": ItemData(77035, ItemClassification.filler),
    "Instant Noodles": ItemData(77036, ItemClassification.useful),
    "Crab Apple": ItemData(77037, ItemClassification.filler),
    "Hot Dog...?": ItemData(77038, ItemClassification.filler),
    "Hot Cat": ItemData(77039, ItemClassification.filler),
    "Glamburger": ItemData(77040, ItemClassification.useful),
    "Sea Tea": ItemData(77041, ItemClassification.filler),
    "Starfait": ItemData(77042, ItemClassification.filler),
    "Legendary Hero": ItemData(77043, ItemClassification.useful),
    "Cloudy Glasses": ItemData(77044, ItemClassification.progression_skip_balancing),
    "Torn Notebook": ItemData(77045, ItemClassification.progression_skip_balancing),
    "Stained Apron": ItemData(77046, ItemClassification.progression_skip_balancing),
    "Burnt Pan": ItemData(77047, ItemClassification.progression_skip_balancing),
    "Cowboy Hat": ItemData(77048, ItemClassification.progression_skip_balancing),
    "Empty Gun": ItemData(77049, ItemClassification.progression_skip_balancing),
    "Heart Locket": ItemData(77050, ItemClassification.progression_skip_balancing),
    "Worn Dagger": ItemData(77051, ItemClassification.progression_skip_balancing),
    "Real Knife": ItemData(77052, ItemClassification.progression_skip_balancing),
    "The Locket": ItemData(77053, ItemClassification.progression_skip_balancing),
    "Bad Memory": ItemData(77054, ItemClassification.filler),
    "Dream": ItemData(77055, ItemClassification.filler),
    "Undyne Letter EX": ItemData(77057, ItemClassification.progression),
    "Popato Chisps": ItemData(77058, ItemClassification.filler),
    "Junk Food": ItemData(77059, ItemClassification.filler),
    "Mystery Key": ItemData(77060, ItemClassification.progression),
    "Face Steak": ItemData(77061, ItemClassification.useful),
    "Hush Puppy": ItemData(77062, ItemClassification.filler),
    "Snail Pie": ItemData(77063, ItemClassification.filler),
    "temy armor": ItemData(77064, ItemClassification.progression_skip_balancing),
    "Complete Skeleton": ItemData(77779, ItemClassification.progression),
    "Fish": ItemData(77780, ItemClassification.progression),
    "DT Extractor": ItemData(77782, ItemClassification.progression),
    # "Mettaton Plush": ItemData(77786, ItemClassification.progression),
    "Left Home Key": ItemData(77787, ItemClassification.progression),
    "LOVE": ItemData(77788, ItemClassification.progression_skip_balancing),
    "Right Home Key": ItemData(77789, ItemClassification.progression),
    "Key Piece": ItemData(77000, ItemClassification.progression),
    "100G": ItemData(77999, ItemClassification.useful),
    "500G": ItemData(77998, ItemClassification.useful),
    "1000G": ItemData(77997, ItemClassification.progression),
    # "Generated Weapon": ItemData(77996, ItemClassification.useful),
    # "Generated Armor": ItemData(77995, ItemClassification.useful),
    "ATK Up": ItemData(77065, ItemClassification.progression_skip_balancing),
    "DEF Up": ItemData(77066, ItemClassification.progression_skip_balancing),
    "HP Up": ItemData(77067, ItemClassification.progression_skip_balancing),
    "ITEM": ItemData(77079, ItemClassification.progression),
    "Ruins Key": ItemData(77081, ItemClassification.progression),
    "Snowdin Key": ItemData(77082, ItemClassification.progression),
    "Waterfall Key": ItemData(77083, ItemClassification.progression),
    "Hotland Key": ItemData(77084, ItemClassification.progression),
    "Jump": ItemData(77086, ItemClassification.progression),
    "Ruins Population Pack": ItemData(77087, ItemClassification.progression),
    "Snowdin Population Pack": ItemData(77088, ItemClassification.progression),
    "Waterfall Population Pack": ItemData(77089, ItemClassification.progression),
    "Hotland Population Pack": ItemData(77090, ItemClassification.progression),
    "Ruins Spare": ItemData(77092, ItemClassification.progression),
    "Snowdin Spare": ItemData(77093, ItemClassification.progression),
    "Waterfall Spare": ItemData(77094, ItemClassification.progression),
    "Hotland Spare": ItemData(77095, ItemClassification.progression),
    "Ice Trap": ItemData(77091, ItemClassification.trap),
    "LOVE Reduction Trap": ItemData(10001, ItemClassification.trap),
    "Max HP Reduction Trap": ItemData(10002, ItemClassification.trap),
    "ATK Reduction Trap": ItemData(10003, ItemClassification.trap),
    "DEF Reduction Trap": ItemData(10004, ItemClassification.trap),
    "X-Slash": ItemData(5001, ItemClassification.useful),
    "RedBuster": ItemData(5002, ItemClassification.useful),
    "HopefulHeal": ItemData(5003, ItemClassification.useful),
    "BraveBash": ItemData(5004, ItemClassification.useful),
    "PatientStand": ItemData(5005, ItemClassification.useful),
    "Pacify": ItemData(5006, ItemClassification.useful),
    "DefShatter": ItemData(5007, ItemClassification.useful),
    "RestfulSleep": ItemData(5008, ItemClassification.useful),
    "Out of Logic Access": ItemData(None, ItemClassification.progression),
}

i = 1
for door in door_name_list:
    item_table.__setitem__("Door Unlock - "+door, ItemData(1000+i, ItemClassification.progression))
    i += 1

spells_heal = {
    "HopefulHeal": 1,
    "PatientStand": 1,
    "RestfulSleep": 1,
}

spells_pacifist = {
    "Pacify": 1,
}

spells_violent = {
    "DefShatter": 1,
}

spells_attack = {
    "X-Slash": 1,
    "RedBuster": 1,
}

spells_gimmicks = {
    "BraveBash": 1,
}

non_key_items = {
    "Butterscotch Pie": 1,
    "Snowman Piece": 1,
    "Instant Noodles": 1,
    "Abandoned Quiche": 1,
    "Punch Card": 3,
    "Hot Dog...?": 1,
}

required_armor = {
    "Cloudy Glasses": 1,
    "Manly Bandanna": 1,
    "Old Tutu": 1,
    "Stained Apron": 1,
    "Heart Locket": 1,
    "Faded Ribbon": 1,
    "Cowboy Hat": 1,
}

required_weapons = {
    "Torn Notebook": 1,
    "Tough Glove": 1,
    "Ballet Shoes": 1,
    "Burnt Pan": 1,
    "Worn Dagger": 1,
    "Toy Knife": 1,
    "Empty Gun": 1,
}

key_items = {
    "Complete Skeleton": 1,
    "Fish": 1,
    "1000G": 2,
    "DT Extractor": 1,
    "ATK Up": 19,
    "DEF Up": 5,
    "HP Up": 19,
    "LOVE": 19,
    "Ruins Key": 1,
    "Snowdin Key": 1,
    "Waterfall Key": 1,
    "Hotland Key": 1,
    "Mystery Key": 1,
    "Jump": 1,
}

junk_weights_all = {
    "Bisicle": 12,
    "Legendary Hero": 8,
    "Glamburger": 10,
    "Crab Apple": 12,
    "Sea Tea": 12,
    "Nice Cream": 10,
    "Spider Donut": 10,
    "Popato Chisps": 12,
    "Junk Food": 12,
    "Temmie Flakes": 10,
    "Spider Cider": 8,
    "Hot Dog...?": 10,
    "Cinnamon Bun": 10,
    "Starfait": 12,
    "Punch Card": 8,
    "Monster Candy": 6,
    "Face Steak": 3,
    "Astronaut Food": 5,
    "Hot Cat": 8,
    "Hush Puppy": 4,
    "100G": 6,
    "500G": 4,
}

junk_weights_cut_items = {
    "Puppydough Icecream": 8,
    "Pumpkin Rings": 12,
    "Croquet Roll": 10,
    "Ghost Fruit": 10,
    "Stoic Onion": 8,
    "Rock Candy": 6,
}

junk_weights_neutral = {
    "Bisicle": 12,
    "Legendary Hero": 8,
    "Glamburger": 10,
    "Crab Apple": 12,
    "Sea Tea": 12,
    "Nice Cream": 10,
    "Spider Donut": 10,
    "Junk Food": 12,
    "Temmie Flakes": 10,
    "Spider Cider": 8,
    "Cinnamon Bun": 10,
    "Starfait": 12,
    "Punch Card": 8,
    "Monster Candy": 6,
    "Face Steak": 3,
    "Astronaut Food": 5,
    "100G": 6,
    "500G": 4,
}

junk_weights_pacifist = {
    "Bisicle": 12,
    "Legendary Hero": 8,
    "Glamburger": 10,
    "Crab Apple": 12,
    "Sea Tea": 12,
    "Nice Cream": 10,
    "Spider Donut": 10,
    "Popato Chisps": 12,
    "Junk Food": 12,
    "Temmie Flakes": 10,
    "Spider Cider": 8,
    "Hot Dog...?": 10,
    "Cinnamon Bun": 10,
    "Starfait": 12,
    "Punch Card": 8,
    "Monster Candy": 6,
    "Face Steak": 3,
    "Astronaut Food": 5,
    "Hot Cat": 8,
    "Hush Puppy": 4,
    "100G": 6,
    "500G": 4,
}

junk_weights_genocide = {
    "Bisicle": 12,
    "Legendary Hero": 8,
    "Glamburger": 10,
    "Crab Apple": 12,
    "Sea Tea": 12,
    "Spider Donut": 10,
    "Junk Food": 12,
    "Temmie Flakes": 10,
    "Spider Cider": 8,
    "Cinnamon Bun": 10,
    "Starfait": 12,
    "Monster Candy": 6,
    "Face Steak": 3,
    "Astronaut Food": 5,
    "100G": 6,
    "500G": 4,
}
