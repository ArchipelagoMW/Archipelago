from ..game_data.local_data import item_id_table
import random
from typing import Any

gift_exclusions = [
    "Franklin Badge",
    "Pak of Bubble Gum",
    "Jar of Fly Honey",
    "Tiny Key",
    "Yogurt Dispenser",
    "UFO Engine",
    "Piggy Nose",
    "Shyness Book",
    "King Banana",
    "Letter For Tony",
    "Key to the Shack",
    "Key to the Cabin",
    "Bad Key Machine",
    "Zombie Paper",
    "Hawk Eye",
    "ATM Card",
    "Show Ticket",
    "Tenda Lavapants",
    "Wad of Bills",
    "Receiver Phone",
    "Diamond",
    "Signed Banana",
    "Pencil Eraser",
    "Hieroglyph Copy",
    "Contact Lens",
    "Key to the Tower",
    "Meteorite Piece",
    "Sound Stone",
    "Police Badge",
    "Mining Permit",
    "Key to the Locker",
    "Insignificant Item",
    "Tiny Ruby",
    "Eraser Eraser",
    "Tendakraut",
    "Progressive Bat",
    "Progressive Fry Pan",
    "Progressive Gun",
    "Progressive Bracelet",
    "Progressive Other",
    "Carrot Key"
]

wanted_traits = [
    "Armor",
    "Weapon",
    "Cure",
    "Bomb",
    "Mana",
    "Heal",
    "Life",
    "Neutralizing",
    "Draining",
    "Beef",
    "Jerky",
    "Egg",
    "Chicken",
    "Spicy",
    "Broken",
    "Pasta",
    "Pizza",
    "Condiment",
    "Dairy",
    "AnimalProduct",
    "Copper",
    "Silver",
    "Gold",
    "Diamond",
    "Plastic",
    "Herb",
    "Repellant",
    "Slime",
    "Animal",
    "Juice",
    "Meat",
    "Water",
    "Drink",
    "FastFood",
    "Bread",
    "FrozenFood",
    "Fruit",
    "Toy",
    "Salted",
    "Speed",
    "Guts",
    "Luck",
    "Doll",
    "Legendary",
    "Buff",
    "Pipe",
    "Hat",
    "Trash",
    "ExoticFood",
    "Insect",
    "Fire",
    "Ice",
    "Light",
    "Food",
    "Consumable",
    "Electronics",
    "Candy",
    "Medicine",
    "Coffee",
    "Artifact",
    "Fireworks",
    "Confectionary",
    "Explosive",
    "Jewelry",
    "Rock",
    "Metal"
]

# If these traits are in the item, then pick randomly from the results
# If multiple fit, pick the combined highest quality.
secondary_trait_list = {
    "Beef": ["Hamburger", "Double Burger", "Mammoth Burger", "Beef Jerky"],
    "Jerky": ["Beef Jerky", "Spicy Jerky", "Luxury Jerky"],
    "Egg": ["Fresh Egg", "Boiled Egg"],
    "Chicken": ["Chicken"],
    "Spicy": ["Jar of Hot Sauce", "Spicy Jerky"],
    "Broken": ["Broken Machine", "Broken Gadget", "Broken Air Gun", "Broken Spray Can",
               "Broken Laser", "Broken Iron", "Broken Pipe", "Broken Cannon", "Broken Tube",
               "Broken Bazooka", "Broken Trumpet", "Broken Harmonica", "Broken Antenna"],
    "Pasta": ["Pasta di Summers", "Cup of Noodles", "Cup of Lifenoodles"],
    "Pizza": ["Pizza", "Large Pizza"],
    "Condiment": ["Ketchup Packet", "Sugar Packet", "Salt Packet", "Tin of Cocoa",
                  "Carton of Cream", "Sprig of Parsley", "Jar of Delisauce", "Jar of Hot Sauce"],
    "Dairy": ["Plain Yogurt", "Trout Yogurt", "Gelato de Resort"],
    "AnimalProduct": ["Fresh Egg"],
    "Copper": ["Copper Bracelet"],
    "Silver": ["Silver Bracelet"],
    "Gold": ["Gold Bracelet"],
    "Diamond": ["Diamond Band"],
    "Plastic": ["Cheap Bracelet", "Bottle of Water", "Bottle of DXwater"],
    "Herb": ["Refreshing Herb", "Secret Herb"],
    "Repellant": ["Repel Sandwich", "Repel Superwich"],
    "Slime": ["Slime Generator"],
    "Animal": ["Chicken", "Chick", "Snake", "Viper"],
    "Juice": ["Can of Fruit Juice"],
    "Meat": ["Hamburger", "Double Burger", "Mammoth Burger", "Beef Jerky",
             "Spicy Jerky", "Luxury Jerky", "Kabob"],
    "Water": ["Bottle of Water", "Bottle of DXwater"],
    "Drink": ["Bottle of Water", "Bottle of DXwater", "Cup of Coffee", "Can of Fruit Juice", "Protein Drink",
              "Royal Iced Tea"],
    "FastFood": ["Hamburger", "Ketchup Packet", "Double Burger", "Bag of Fries"],
    "Bread": ["Plain Roll", "Bread Roll", "Croissant"],
    "FrozenFood": ["Popsicle", "Gelato de Resort"],
    "Fruit": ["Banana", "Can of Fruit Juice"],
    "Toy": ["Toy Air Gun", "Teddy Bear", "Super Plush Bear", "Yo-yo", "Slingshot"],
    "Salted": ["Salt Packet"],
    "Speed": ["Speed Capsule", "Rabbit's Foot"],
    "Guts": ["Guts Capsule", "Sudden Guts Pill", "Gutsy Bat"],
    "Luck": ["Lucky Coin", "Luck Capsule", "Lucky Sandwich"],
    "Doll": ["Teddy Bear", "Super Plush Bear"],
    "Legendary": ["Legendary Bat"],
    "Buff": ["Sudden Guts Pill", "Guts Capsule", "Speed Capsule", "IQ Capsule", "Luck Capsule", "Vital Capsule",
             "Defense Spray", "Defense Shower", "Rock Candy"],
    "Pipe": ["HP-Sucker", "Hungry HP-Sucker", "Broken Pipe"],
    "Hat": ["Holmes Hat", "Hard Hat", "Baseball Cap", "Mr. Baseball Cap"],
    "Trash": ["Broken Machine", "Broken Gadget", "Broken Air Gun", "Broken Spray Can",
              "Broken Laser", "Broken Iron", "Broken Pipe", "Broken Cannon", "Broken Tube",
              "Broken Bazooka", "Broken Trumpet", "Broken Harmonica", "Broken Antenna",
              "Ruler", "Pair of Dirty Socks", "Protractor"],
    "ExoticFood": ["Piggy Jelly", "Peanut Cheese Bar", "Bowl of Rice Gruel",
                   "Molokheiya Soup", "Kabob", "Bean Croquette", "Brain Food Lunch"],
    "Insect": ["Insecticde Spray", "Xterminator Spray", "Stag Beetle"],
    "Fire": ["Flame Pendant"],
    "Ice": ["Rain Pendant"],
    "Light": ["Night Pendant"],
    "Electronics": ["Slime Generator", "Shield Killer", "Neutralizer", "Defense Shower", "Counter-PSI Unit",
                    "HP-Sucker", "Hungry HP-Sucker"],
    "Candy": ["PSI Caramel", "Magic Truffle", "Rock Candy", "Magic Pudding", "Peanut Cheese Bar"],
    "Medicine": ["Vial of Serum", "Cold Remedy", "IQ Capsule", "Guts Capsule", "Speed Capsule", "Vital Capsule", "Luck Capsule"],
    "Coffee": ["Cup of Coffee"],
    "Artifact": ["Metotite", "Meteornium"],
    "Fireworks": ["Bottle Rocket", "Big Bottle Rocket", "Multi Bottle Rocket"],
    "Confectionary": ["Cookie", "Magic Tart"],
    "Explosive": ["Bottle Rocket", "Big Bottle Rocket", "Multi Bottle Rocket", "Heavy Bazooka",
                  "Bazooka", "Bomb", "Super Bomb"],
    "Jewelry": ["Cheap Bracelet", "Copper Bracelet", "Silver Bracelet", "Gold Bracelet",
                "Platinum Band", "Diamond Band", "Flame Pendant", "Sea Pendant", "Star Pendant", "Earth Pendant",
                "Rain Pendant", "Night Pendant"],
    "Rock": ["Rock Candy", "Brain Stone"],
    "Metal": ["Broken Machine", "Broken Gadget", "Broken Air Gun", "Broken Spray Can",
              "Broken Laser", "Broken Iron", "Broken Pipe", "Broken Cannon", "Broken Tube",
              "Broken Bazooka", "Broken Trumpet", "Broken Harmonica", "Broken Antenna", "Slime Generator",
              "Fry Pan", "Magic Fry Pan", "Thick Fry Pan", "Deluxe Fry Pan", "Chef's Fry Pan",
              "French Fry Pan", "Holy Fry Pan", "Non-Stick Frypan"],

    "Food": ["Cookie", "Bag of Fries", "Hamburger", "Boiled Egg", "Fresh Egg", "Picnic Lunch",
             "Pasta di Summers", "Pizza", "Chef's Special", "Large Pizza", "PSI Caramel", "Magic Truffle",
             "Brain Food Lunch", "Rock Candy", "Croissant", "Bread Roll", "Kraken Soup",
             "Trout Yogurt", "Banana", "Calorie Stick", "Gelato de Resort", "Magic Tart",
             "Cup of Noodles", "Repel Sandwich", "Repel Superwich", "Lucky Sandwich", "Double Burger",
             "Peanut Cheese Bar", "Piggy Jelly", "Bowl of Rice Gruel", "Bean Croquette",
             "Molokheiya Soup", "Plain Roll", "Kabob", "Plain Yogurt", "Beef Jerky",
             "Mammoth Burger", "Spicy Jerky", "Luxury Jerky", "Magic Pudding",
             "Popsicle"]

}

tertiary_trait_list = {
    "Consumable": ["Cookie", "Bag of Fries", "Hamburger", "Boiled Egg", "Fresh Egg", "Picnic Lunch",
                   "Pasta di Summers", "Pizza", "Chef's Special", "Large Pizza", "PSI Caramel", "Magic Truffle",
                   "Brain Food Lunch", "Rock Candy", "Croissant", "Bread Roll", "Kraken Soup",
                   "Trout Yogurt", "Banana", "Calorie Stick", "Gelato de Resort", "Magic Tart",
                   "Cup of Noodles", "Repel Sandwich", "Repel Superwich", "Lucky Sandwich", "Double Burger",
                   "Peanut Cheese Bar", "Piggy Jelly", "Bowl of Rice Gruel", "Bean Croquette",
                   "Molokheiya Soup", "Plain Roll", "Kabob", "Plain Yogurt", "Beef Jerky",
                   "Mammoth Burger", "Spicy Jerky", "Luxury Jerky", "Magic Pudding",
                   "Popsicle", "Can of Fruit Juice", "Royal Iced Tea", "Protein Drink",
                   "Bottle of Water", "Cold Remedy", "Vial of Serum", "IQ Capsule",
                   "Guts Capsule", "Speed Capsule", "Vital Capsule", "Luck Capsule",
                   "Ketchup Packet", "Sugar Packet", "Tin of Cocoa", "Carton of Cream", "Sprig of Parsley",
                   "Jar of Hot Sauce", "Salt Packet", "Jar of Delisauce", "Wet Towel", "Refreshing Herb",
                   "Secret Herb", "Horn of Life", "Mummy Wrap", "Bottle Rocket", "Big Bottle Rocket",
                   "Multi Bottle Rocket", "Bomb", "Super Bomb", "Insecticide Spray", "Rust Promoter",
                   "Rust Promoter DX", "Pair of Dirty Socks", "Stag Beetle", "Toothbrush",
                   "Handbag Strap", "Pharaoh's Curse", "Sudden Guts Pill", "Bag of Dragonite",
                   "Defense Spray", "Chick", "Chicken", "Hand-Aid", "Snake", "Viper",
                   "Cup of Coffee", "Bottle of DXwater", "Cup of Lifenoodles"]
}

scaled_traits = [
    "Armor",
    "Weapon",
    "Cure",
    "Bomb",
    "Mana",
    "Heal",
    "Life",
    "Neutralizing",
    "Draining"
]

gift_by_quality = {
    "Heal": {
        0.06: "Cookie",
        0.08: "Can of Fruit Juice",
        0.12: "Cup of Coffee",
        0.18: "Popsicle",
        0.22: "Banana",
        0.24: "Bag of Fries",
        0.30: "Trout Yogurt",
        0.35: "Bread Roll",
        0.42: "Bean Croquette",
        0.43: "Cup of Noodles",
        0.45: "Boiled Egg",
        0.48: "Hamburger",
        0.60: "Royal Iced Tea",
        0.63: "Calorie Stick",
        0.65: "Croissant",
        0.70: "Lucky Sandwich",
        0.80: "Picnic Lunch",
        0.82: "Plain Roll",
        0.84: "Fresh Egg",
        0.88: "Molokheiya Soup",
        0.96: "Double Burger",
        1.00: "Peanut Cheese Bar",
        1.10: "Pasta di Summers",
        1.20: "Pizza",
        1.26: "Kabob",
        1.50: "Beef Jerky",
        1.60: "Plain Yogurt",
        2.05: "Mammoth Burger",
        2.16: "Bowl of Rice Gruel",
        2.20: "Chef's Special",
        2.52: "Spicy Jerky",
        2.40: "Large Pizza",
        3.00: "Piggy Jelly",
        3.10: "Luxury Jerky",
        3.50: "Brain Food Lunch",
        4.00: "Kraken Soup",
        4.01: "Hand-Aid"
    },

    "Armor": {
        0.05: "Travel Charm",
        0.10: "Great Charm",
        0.12: "Cheap Bracelet",
        0.13: "Baseball Cap",
        0.14: "Mr. Baseball Cap",
        0.24: "Copper Bracelet",
        0.26: "Holmes Hat",
        0.20: "Crystal Charm",
        0.36: "Silver Bracelet",
        0.38: "Hard Hat",
        0.48: "Ribbon",
        0.50: "Diadem of Kings",
        0.60: "Red Ribbon",
        0.73: "Gold Bracelet",
        0.75: "Bracer of Kings",
        0.78: "Coin of Slumber",
        0.97: "Platinum Band",
        0.98: "Defense Ribbon",
        0.99: "Coin of Defense",
        1.00: "Cloak of Kings",
        1.21: "Diamond Band",
        1.25: "Lucky Coin",
        1.46: "Pixie's Bracelet",
        1.48: "Talisman Coin",
        1.50: "Talisman Ribbon",
        1.70: "Cherub's Band",
        1.75: "Shiny Coin",
        1.95: "Goddess Band",
        2.00: "Souvenir Coin",
        2.19: "Saturn Ribbon",
        2.68: "Goddess Ribbon"
    },

    "Draining": {
        0.50: "HP-Sucker",
        1.00: "Hungry HP-Sucker"
    },
    
    "Bomb": {
        0.50: "Bomb",
        1.00: "Super Bomb"
    },

    "Neutralizing": {
        0.50: "Shield Killer",
        1.00: "Neutralizer"
    },

    "Cure": {
        0.10: "Cold Remedy",
        0.25: "Vial of Serum",
        0.50: "Wet Towel",
        1.00: "Refreshing Herb",
        2.00: "Secret Herb",
        3.00: "Horn of Life",
        3.01: "Cup of Lifenoodles"
    },

    "Life": {
        0.50: "Secret Herb",
        1.00: "Cup of Lifenoodles",
        1.01: "Horn of Life",
    },

    "Weapon": {
        0.01: "Casey Bat",
        0.04: "Cracked Bat",
        0.11: "Yo-yo",
        0.15: "Tee Ball Bat",
        0.19: "Fy Pan",
        0.23: "Slingshot",
        0.28: "Sand Lot Bat",
        0.30: "Pop Gun",
        0.38: "Thick Fry Pan",
        0.40: "Bionic Slingshot",
        0.46: "Stun Gun",
        0.50: "Minor League Bat",
        0.57: "Deluxe Fry Pan",
        0.61: "Toy Air Gun",
        0.69: "Magnum Air Gun",
        0.73: "Mr. Baseball Bat",
        0.76: "Chef's Fry Pan",
        0.78: "Zip Gun",
        0.88: "Trick Yo-yo",
        0.92: "Laser Gun",
        0.95: "T-Rex's Bat",
        0.96: "Non-Stick Frypan",
        1.00: "Big League Bat",
        1.03: "Combat Yo-yo",
        1.11: "Hyper Beam",
        1.15: "French Fry Pan",
        1.19: "Hall of Fame Bat",
        1.26: "Double Beam",
        1.32: "Ultimate Bat",
        1.38: "Crusher Beam",
        1.50: "Spectrum Beam",
        1.53: "Magicant Bat",
        1.73: "Death Ray",
        1.80: "Sword of Kings",
        1.88: "Baddest Beam",
        2.00: "Magic Fry Pan",
        2.11: "Legendary Bat",
        2.15: "Moon Beam Gun",
        2.40: "Holy Fry Pan",
        2.45: "Gaia Beam",
        2.55: "Gutsy Bat",
    },

    "Mana": {
        0.28: "Bottle of Water",
        0.50: "PSI Caramel",
        0.51: "Magic Tart",
        1.14: "Bottle of DXwater",
        1.20: "Magic Pudding",
        2.28: "Magic Truffle"
    }
}


def trait_interpreter(gift: dict[str, Any]) -> int:
    """Converts received gifts into in-game items.
       If the item name perfectly matches an in-game item, that item will be received.
       If any of the traits can be scaled i.e. a healing item, the gift will be converted into an item of roughly that value.
       If any of the traits are not scaled, but are in the secondary trait list i.e. a food item, it will be converted into a random appropriate item.
       If none of the traits are applicable, return a random consumable."""
    item = None
    trait_list = []
    got_trait = False
    if "Traits" in gift:
        gift["traits"] = gift.pop("Traits")

    for trait in gift["traits"]:
        if "Trait" in trait:
            trait["trait"] = trait.pop("Trait")

        if "Quality" in trait:
            trait["quality"] = trait.pop("Quality")

        if "quality" not in trait:
            trait["quality"] = 1

        trait_list.append(trait["trait"])
        if trait["trait"] in scaled_traits:
            item_quality_table = gift_by_quality[trait["trait"]]
            quality = min(item_quality_table.keys(), key=lambda x: abs(x - trait["quality"]))
            item = item_quality_table[quality]
            got_trait = True
            break

    if not got_trait:
        for trait in trait_list:
            if trait in secondary_trait_list:
                item = random.choice(secondary_trait_list[trait])
                got_trait = True
                break

    if not got_trait:
        for trait in trait_list:
            if trait in tertiary_trait_list:
                item = random.choice(tertiary_trait_list[trait])
                break
                
    if item is not None:
        item = item_id_table[item]
    else:
        item = random.choice(secondary_trait_list["Consumable"])
        item = item_id_table[item]
    return item


# IF trait is in special traits, give that item.
# Else if the trait is in a Scaled trait (Food, Armor, etc., then break them up by scaling)
