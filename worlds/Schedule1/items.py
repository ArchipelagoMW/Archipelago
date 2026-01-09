from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import Schedule1World

# Every item must have a unique integer ID associated with it.
# We will have a lookup from item name to ID here that, in world.py, we will import and bind to the world class.
# Even if an item doesn't exist on specific options, it must be present in this lookup.
# 300-329 are reserved for bundles.
# 400-499 are reserved for cartel influence
ITEM_NAME_TO_ID = {
    # Level up rewards
    "Jar Hardware Store Unlock" : 1,
    "PGR Hardware Store Unlock" : 2,
    "Speed Grow Hardware Store Unlock" : 3,
    "Long-Life Soil Hardware Store Unlock" : 4,
    "Fertilizer Hardware Store Unlock" : 5,
    "Sour Diesel Seeds Unlock" : 6,
    "Pot Sprinkler Hardware Store Unlock" : 7,
    "Electric Plant Trimmers Hardware Store Unlock" : 8,
    "Westville Region Unlock" : 9,
    "Low-Quality Pseudo Unlock" : 10,
    "Mixing Station Hardware Store Unlock" : 11,
    "Soil Pourer Hardware StoreUnlock" : 12,
    "Green Crack Seeds Unlock" : 13,
    "Viagor Gas Mart Unlock" : 14,
    "Extra Long-Life Soil Hardware Store Unlock" : 15,
    "Mouth Wash Gas Mart Unlock" : 16,
    "Grandaddy Purple Seeds Unlock" : 17,
    "Flu Medicine Gas Mart Unlock" : 18,
    "Packaging Station Mk II Hardware Store Unlock" : 19,
    "Gasoline Gas Mart Unlock" : 20,
    "Energy Drink Gas Mart Unlock" : 21,
    "Acid Warehouse Unlock" : 22,
    "Phosphorus Warehouse Unlock" : 23,
    "Chemistry Station Warehouse Unlock" : 24,
    "Lab Oven Warehouse Unlock" : 25,
    "Mixing Station Mk II Warehouse Unlock" : 26,
    "Motor Oil Gas Mart Unlock" : 27,
    "Mega Beans Gas Mart Unlock" : 28,
    "Air Pot Warehouse Unlock" : 29,
    "Chili Gas Mart Unlock" : 30,
    "Full Spectrum Grow Light warehouse Unlock" : 31,
    "Warehouse Access": 32,
    "Battery Gas Mart Unlock": 33,
    "Iodine Gas Mart Unlock": 34,
    "Addy Gas Mart Unlock": 35,
    "Drying Rack Warehouse Unlock": 36,
    "Pseudo Unlock": 37,
    "Horse Semen Gas Mart Unlock": 38,
    "Revolver Warehouse Unlock": 39,
    "Revolver Ammo Warehouse Unlock": 40,
    "Brick Press Warehouse Unlock": 41,
    "High Quality Pseudo Unlock": 42,
    "Cauldron Warehouse Unlock": 43,
    "Coca Seed Unlock": 44,
    "M1911 Pistol Warehouse Unlock": 45,
    "M1911 Ammo Warehouse Unlock": 46,
    "Pump Shotgun Warehouse Unlock": 47,
    "Pump Shotgun Ammo Warehouse Unlock": 48,
    # Properties
    "Drug Making Property, Barn" : 54,
    "Drug Making Property, Bungalow" : 55,
    "Drug Making Property, Docks Warehouse" : 56,
    "Drug Making Property, Storage Unit" : 59,
    "Business Property, Car Wash" : 61,
    "Business Property, Laundromat" : 62,
    "Business Property, Post Office" : 63,
    "Business Property, Taco Ticklers" : 64,
    # Customers 
    "Northtown Customer Unlocked: Austin Steiner" : 65,
    "Northtown Customer Unlocked: Beth Penn" : 66,
    "Northtown Customer Unlocked: Chloe Bowers" : 67,
    "Northtown Customer Unlocked: Donna Martin" : 68,
    "Northtown Customer Unlocked: Geraldine Poon" : 69,
    "Northtown Customer Unlocked: Jessi Waters" : 70,
    "Northtown Customer Unlocked: Kathy Henderson" : 71,
    "Northtown Customer Unlocked: Kyle Cooley" : 72,
    "Northtown Customer Unlocked: Ludwig Meyer" : 73,
    "Northtown Customer Unlocked: Mick Lubbin" : 74,
    "Northtown Customer Unlocked: Mrs. Ming" : 75,
    "Northtown Customer Unlocked: Peggy Myers" : 76,
    "Northtown Customer Unlocked: Peter File" : 77,
    "Northtown Customer Unlocked: Sam Thompson" : 78,
    "Westville Customer Unlocked: Charles Rowland" : 79,
    "Westville Customer Unlocked: Dean Webster" : 80,
    "Westville Customer Unlocked: Doris Lubbin" : 81,
    "Westville Customer Unlocked: George Greene" : 82,
    "Westville Customer Unlocked: Jerry Montero" : 83,
    "Westville Customer Unlocked: Joyce Ball" : 84,
    "Westville Customer Unlocked: Keith Wagner" : 85,
    "Westville Customer Unlocked: Kim Delaney" : 86,
    "Westville Customer Unlocked: Meg Cooley" : 87,
    "Westville Customer Unlocked: Trent Sherman" : 88,
    "Downtown Customer Unlocked: Bruce Norton" : 89,
    "Downtown Customer Unlocked: Elizabeth Homley" : 90,
    "Downtown Customer Unlocked: Eugene Buckley" : 91,
    "Downtown Customer Unlocked: Greg Figgle" : 92,
    "Downtown Customer Unlocked: Jeff Gilmore" : 93,
    "Downtown Customer Unlocked: Jennifer Rivera" : 94,
    "Downtown Customer Unlocked: Kevin Oakley" : 95,
    "Downtown Customer Unlocked: Louis Fourier" : 96,
    "Downtown Customer Unlocked: Philip Wentworth" : 97,
    "Downtown Customer Unlocked: Randy Caulfield" : 98,
    "Downtown Customer Unlocked: Lucy Pennington" : 99,
    "Docks Customer Unlocked: Anna Chesterfield" : 100,
    "Docks Customer Unlocked: Billy Kramer" : 101,
    "Docks Customer Unlocked: Cranky Frank" : 102,
    "Docks Customer Unlocked: Genghis Barn" : 103,
    "Docks Customer Unlocked: Javier Perez" : 104,
    "Docks Customer Unlocked: Kelly Reynolds" : 105,
    "Docks Customer Unlocked: Lisa Gardner" : 106,
    "Docks Customer Unlocked: Mac Cooper" : 107,
    "Docks Customer Unlocked: Marco Barone" : 108,
    "Docks Customer Unlocked: Melissa Wood" : 109,
    "Docks Customer Unlocked: Sherman Giles" : 110,
    "Suburbia Customer Unlocked: Alison Knight" : 111,
    "Suburbia Customer Unlocked: Carl Bundy" : 112,
    "Suburbia Customer Unlocked: Chris Sullivan" : 113,
    "Suburbia Customer Unlocked: Dennis Kennedy" : 114,
    "Suburbia Customer Unlocked: Hank Stevenson" : 115,
    "Suburbia Customer Unlocked: Harold Colt" : 116,
    "Suburbia Customer Unlocked: Jack Knight" : 117,
    "Suburbia Customer Unlocked: Jackie Stevenson" : 118,
    "Suburbia Customer Unlocked: Jeremy Wilkinson" : 119,
    "Suburbia Customer Unlocked: Karen Kennedy" : 120,
    "Uptown Customer Unlocked: Fiona Hancock" : 121,
    "Uptown Customer Unlocked: Herbert Bleuball" : 122,
    "Uptown Customer Unlocked: Irene Meadows" : 123,
    "Uptown Customer Unlocked: Jen Heard" : 124,
    "Uptown Customer Unlocked: Lily Turner" : 125,
    "Uptown Customer Unlocked: Michael Boog" : 126,
    "Uptown Customer Unlocked: Pearl Moore" : 127,
    "Uptown Customer Unlocked: Ray Hoffman" : 128,
    "Uptown Customer Unlocked: Tobias Wentworth" : 129,
    "Uptown Customer Unlocked: Walter Cussler" : 130,
    # Dealers
    "Westville Dealer Recruited: Molly Presley" : 131,
    "Downtown Dealer Recruited: Brad Crosby" : 132,
    "Docks Dealer Recruited: Jane Lucero" : 133,
    "Suburbia Dealer Recruited: Wei Long" : 134,
    "Uptown Dealer Recruited: Leo Rivers" : 135,
    # Bad filler Items
    "Cuke" : 138,
    "Banana" : 139,
    "Paracetamol" : 140,
    "Donut" : 141,
    "Viagra" : 142,
    "Mouth Wash": 143,
    "Flu Medicine": 144,
    "Gasoline": 145,
    "Energy Drink": 146,
    "Motor Oil": 147,
    "Mega Bean": 148,
    "Chili": 149,
    "Battery": 150,
    "Iodine": 151,
    "Addy": 152,
    "Horse Semen": 153,
    "Baggies" : 154,
    "Jar" : 155,
    "Coffee Table" : 156,
    "Wooden Square Table" : 157,
    "Metal square Table" : 158,
    "Floor Lamp" : 159,
    "TV" : 160,
    "Display Cabinet" : 161,
    "Trash Bag" : 162,
    "Trash Can" : 163,
    "Plastic table" : 164,
    "Toilet" : 165,
    "Spray Bottle" : 166,
    # Basic filler items
    "OG Kush Seed" : 167,
    "PGR" : 168,
    "Speed Grow" : 169,
    "Grow Tent" : 170,
    "Soil" : 171,
    "Small Storage Rack" : 172,
    "Medium Storage Rack" : 173,
    "Fertilizer" : 174,
    "Pot Sprinkler" : 175,
    "Mixing Station" : 176,
    "soil Pourer" : 177,
    "Extra Long-Life Soil" : 178,
    "Plastic pot" : 179,
    "Moisture-preservative pot" : 180,
    "Air pot" : 181,
    # Better filler items
    "Packaging Station" : 182,
    "Large Storage Rack" : 183,
    "Long-Life Soil" : 184,
    "Suspension Rack" : 185,
    "Halogen Grow Light" : 186,
    "LED Grow Light" : 187,
    # Amazing filler items
    "Packaging Station Mk II" : 188,
    "AC Unit" : 189,
    "Mixing Station Mk II" : 190,
    "Brick Press" : 191,
    "Low-Quality Pseudo" : 192,
    "Pseudo" : 193,
    "High Quality Pseudo" : 194,
    "Grain Bag" : 195,
    "Spore Syringe" : 196,
    "Mushroom Substrate" : 197,
    # Fillers that can skip progression
    "Acid" : 198,
    "Phosphorus" : 199,
    "Chemistry Station" : 200,
    "Mushroom Spawn Station" : 201,
    "Mushroom Bed" : 202,
    "Drying Rack" : 203,
    "Lab oven" : 204,
    "Cauldron" : 205,
    "Coca Seed" : 206,
    # Weapons fillers
    "Revolver" : 207,
    "Revolver Ammo" : 208,
    "M1911 Pistol" : 209,
    "M1911 Ammo" : 210,
    "Pump Shotgun" : 211,
    "Pump Shotgun Ammo" : 212,
    "Machete" : 213,
    "Frying Pan" : 214,
    "Baseball Bat" : 215,
    # Cartel influence items
    "Cartel Influence, Westville" : 400,
    "Cartel Influence, Downtown" : 401,
    "Cartel Influence, Docks" : 402,
    "Cartel Influence, Suburbia" : 403,
    "Cartel Influence, Uptown" : 404

    # Ideas for traps:
    # - Fill inventory with bad items like frying pans.
    # - Arrested Trap (REALLY PUNISHING, maybe unfun)
    # - Kill trap
    # - Drug effects
    # - Police Trap
}   

# Items should have a defined default classification.
# In our case, we will make a dictionary from item name to classification.
DEFAULT_ITEM_CLASSIFICATIONS = {
    # Level up rewards
    "Jar Hardware Store Unlock" : ItemClassification.useful,
    "PGR Hardware Store Unlock" : ItemClassification.useful,
    "Speed Grow Hardware Store Unlock" : ItemClassification.useful,
    "Long-Life Soil Hardware Store Unlock" : ItemClassification.useful,
    "Fertilizer Hardware Store Unlock" : ItemClassification.useful,
    "Sour Diesel Seeds Unlock" : ItemClassification.useful,
    "Pot Sprinkler Hardware Store Unlock" : ItemClassification.useful,
    "Electric Plant Trimmers Hardware Store Unlock" : ItemClassification.useful,
    "Westville Region Unlock" : ItemClassification.progression | ItemClassification.useful,
    "Low-Quality Pseudo Unlock" : ItemClassification.progression | ItemClassification.useful,
    "Mixing Station Hardware Store Unlock" : ItemClassification.progression | ItemClassification.useful,
    "Soil Pourer Hardware StoreUnlock" : ItemClassification.useful,
    "Green Crack Seeds Unlock" : ItemClassification.useful,
    "Viagor Gas Mart Unlock" : ItemClassification.useful,
    "Extra Long-Life Soil Hardware Store Unlock" : ItemClassification.useful,
    "Mouth Wash Gas Mart Unlock" : ItemClassification.useful,
    "Grandaddy Purple Seeds Unlock" : ItemClassification.useful,
    "Flu Medicine Gas Mart Unlock" : ItemClassification.useful,
    "Packaging Station Mk II Hardware Store Unlock" : ItemClassification.progression_skip_balancing | ItemClassification.useful,
    "Gasoline Gas Mart Unlock" : ItemClassification.progression,
    "Energy Drink Gas Mart Unlock" : ItemClassification.useful,
    "Acid Warehouse Unlock" : ItemClassification.progression,
    "Phosphorus Warehouse Unlock" : ItemClassification.progression,
    "Chemistry Station Warehouse Unlock" : ItemClassification.progression,
    "Lab Oven Warehouse Unlock" : ItemClassification.progression | ItemClassification.useful,
    "Mixing Station Mk II Warehouse Unlock" : ItemClassification.progression_skip_balancing | ItemClassification.useful,
    "Motor Oil Gas Mart Unlock" : ItemClassification.useful,
    "Mega Beans Gas Mart Unlock" : ItemClassification.useful,
    "Air Pot Warehouse Unlock" : ItemClassification.useful,
    "Chili Gas Mart Unlock" : ItemClassification.useful,
    "Full Spectrum Grow Light warehouse Unlock" : ItemClassification.useful,
    "Warehouse Access": ItemClassification.progression |ItemClassification.useful,
    "Battery Gas Mart Unlock": ItemClassification.useful,
    "Iodine Gas Mart Unlock": ItemClassification.useful,
    "Addy Gas Mart Unlock": ItemClassification.useful,
    "Drying Rack Warehouse Unlock": ItemClassification.progression | ItemClassification.useful,
    "Pseudo Unlock": ItemClassification.useful,
    "Horse Semen Gas Mart Unlock": ItemClassification.useful,
    "Revolver Warehouse Unlock": ItemClassification.useful,
    "Revolver Ammo Warehouse Unlock": ItemClassification.useful,
    "Brick Press Warehouse Unlock": ItemClassification.useful,
    "High Quality Pseudo Unlock": ItemClassification.useful,
    "Cauldron Warehouse Unlock": ItemClassification.progression | ItemClassification.useful,
    "Coca Seed Unlock": ItemClassification.progression | ItemClassification.useful,
    "M1911 Pistol Warehouse Unlock": ItemClassification.useful,
    "M1911 Ammo Warehouse Unlock": ItemClassification.useful,
    "Pump Shotgun Warehouse Unlock": ItemClassification.useful,
    "Pump Shotgun Ammo Warehouse Unlock": ItemClassification.useful,
    # Properties
    "Drug Making Property, Barn" : ItemClassification.progression_skip_balancing,
    "Drug Making Property, Bungalow" : ItemClassification.progression_skip_balancing,
    "Drug Making Property, Docks Warehouse" : ItemClassification.progression_skip_balancing,
    "Drug Making Property, Storage Unit" : ItemClassification.progression_skip_balancing,
    "Business Property, Car Wash" : ItemClassification.progression_skip_balancing,
    "Business Property, Laundromat" : ItemClassification.progression_skip_balancing,
    "Business Property, Post Office" : ItemClassification.progression_skip_balancing,
    "Business Property, Taco Ticklers" : ItemClassification.progression_skip_balancing,
    # Customers 
    "Northtown Customer Unlocked: Austin Steiner" : ItemClassification.useful,
    "Northtown Customer Unlocked: Beth Penn" : ItemClassification.progression | ItemClassification.useful, # Mission related
    "Northtown Customer Unlocked: Chloe Bowers" : ItemClassification.progression | ItemClassification.useful, # Mission related,
    "Northtown Customer Unlocked: Donna Martin" : ItemClassification.useful,
    "Northtown Customer Unlocked: Geraldine Poon" : ItemClassification.useful,
    "Northtown Customer Unlocked: Jessi Waters" : ItemClassification.useful,
    "Northtown Customer Unlocked: Kathy Henderson" : ItemClassification.useful,
    "Northtown Customer Unlocked: Kyle Cooley" : ItemClassification.useful,
    "Northtown Customer Unlocked: Ludwig Meyer" : ItemClassification.progression | ItemClassification.useful, # Mission related,
    "Northtown Customer Unlocked: Mick Lubbin" : ItemClassification.useful,
    "Northtown Customer Unlocked: Mrs. Ming" : ItemClassification.useful,
    "Northtown Customer Unlocked: Peggy Myers" : ItemClassification.useful,
    "Northtown Customer Unlocked: Peter File" : ItemClassification.useful,
    "Northtown Customer Unlocked: Sam Thompson" : ItemClassification.useful | ItemClassification.progression, # Mission related
    "Westville Customer Unlocked: Charles Rowland" : ItemClassification.progression_skip_balancing | ItemClassification.useful, # Unlocks dealer
    "Westville Customer Unlocked: Dean Webster" : ItemClassification.useful,
    "Westville Customer Unlocked: Doris Lubbin" : ItemClassification.useful,
    "Westville Customer Unlocked: George Greene" : ItemClassification.progression_skip_balancing | ItemClassification.useful, # Unlocks dealer
    "Westville Customer Unlocked: Jerry Montero" : ItemClassification.progression_skip_balancing | ItemClassification.useful, # Unlocks dealer
    "Westville Customer Unlocked: Joyce Ball" : ItemClassification.useful,
    "Westville Customer Unlocked: Keith Wagner" : ItemClassification.useful,
    "Westville Customer Unlocked: Kim Delaney" : ItemClassification.useful,
    "Westville Customer Unlocked: Meg Cooley" : ItemClassification.useful,
    "Westville Customer Unlocked: Trent Sherman" : ItemClassification.useful,
    "Downtown Customer Unlocked: Bruce Norton" : ItemClassification.useful,
    "Downtown Customer Unlocked: Elizabeth Homley" : ItemClassification.useful | ItemClassification.progression, # Unlocks supplier
    "Downtown Customer Unlocked: Eugene Buckley" : ItemClassification.progression_skip_balancing | ItemClassification.useful, # Unlocks dealer
    "Downtown Customer Unlocked: Greg Figgle" : ItemClassification.progression_skip_balancing | ItemClassification.useful, # Unlocks dealer
    "Downtown Customer Unlocked: Jeff Gilmore" : ItemClassification.useful,
    "Downtown Customer Unlocked: Jennifer Rivera" : ItemClassification.useful,
    "Downtown Customer Unlocked: Kevin Oakley" : ItemClassification.useful | ItemClassification.progression, # Unlocks supplier
    "Downtown Customer Unlocked: Louis Fourier" : ItemClassification.useful,
    "Downtown Customer Unlocked: Philip Wentworth" : ItemClassification.useful,
    "Downtown Customer Unlocked: Randy Caulfield" : ItemClassification.progression_skip_balancing | ItemClassification.useful, # Unlocks dealer
    "Downtown Customer Unlocked: Lucy Pennington" : ItemClassification.useful,
    "Docks Customer Unlocked: Anna Chesterfield" : ItemClassification.useful,
    "Docks Customer Unlocked: Billy Kramer" : ItemClassification.progression | ItemClassification.useful, # Mission related, Dealer
    "Docks Customer Unlocked: Cranky Frank" : ItemClassification.useful,
    "Docks Customer Unlocked: Genghis Barn" : ItemClassification.useful,
    "Docks Customer Unlocked: Javier Perez" : ItemClassification.useful | ItemClassification.progression, # Unlocks supplier
    "Docks Customer Unlocked: Kelly Reynolds" : ItemClassification.useful,
    "Docks Customer Unlocked: Lisa Gardner" : ItemClassification.useful,
    "Docks Customer Unlocked: Mac Cooper" : ItemClassification.progression | ItemClassification.useful, # Unlocks supplier
    "Docks Customer Unlocked: Marco Barone" : ItemClassification.useful,
    "Docks Customer Unlocked: Melissa Wood" : ItemClassification.progression_skip_balancing | ItemClassification.useful, # Unlocks dealer
    "Docks Customer Unlocked: Sherman Giles" : ItemClassification.useful,
    "Suburbia Customer Unlocked: Alison Knight" : ItemClassification.useful,
    "Suburbia Customer Unlocked: Carl Bundy" : ItemClassification.useful,
    "Suburbia Customer Unlocked: Chris Sullivan" : ItemClassification.useful,
    "Suburbia Customer Unlocked: Dennis Kennedy" : ItemClassification.useful,
    "Suburbia Customer Unlocked: Hank Stevenson" : ItemClassification.useful,
    "Suburbia Customer Unlocked: Harold Colt" : ItemClassification.progression_skip_balancing | ItemClassification.useful, # Unlocks dealer
    "Suburbia Customer Unlocked: Jack Knight" : ItemClassification.useful,
    "Suburbia Customer Unlocked: Jackie Stevenson" : ItemClassification.progression_skip_balancing | ItemClassification.useful, # Unlocks dealer
    "Suburbia Customer Unlocked: Jeremy Wilkinson" : ItemClassification.progression_skip_balancing | ItemClassification.useful, # Unlocks dealer
    "Suburbia Customer Unlocked: Karen Kennedy" : ItemClassification.useful,
    "Uptown Customer Unlocked: Fiona Hancock" : ItemClassification.useful,
    "Uptown Customer Unlocked: Herbert Bleuball" : ItemClassification.useful,
    "Uptown Customer Unlocked: Irene Meadows" : ItemClassification.useful,
    "Uptown Customer Unlocked: Jen Heard" : ItemClassification.progression_skip_balancing | ItemClassification.useful, # Sewer Key
    "Uptown Customer Unlocked: Lily Turner" : ItemClassification.useful,
    "Uptown Customer Unlocked: Michael Boog" : ItemClassification.progression_skip_balancing | ItemClassification.useful, # Unlocks dealer
    "Uptown Customer Unlocked: Pearl Moore" : ItemClassification.useful,
    "Uptown Customer Unlocked: Ray Hoffman" : ItemClassification.progression_skip_balancing | ItemClassification.useful, # Unlocks dealer
    "Uptown Customer Unlocked: Tobias Wentworth" : ItemClassification.useful,
    "Uptown Customer Unlocked: Walter Cussler" : ItemClassification.useful,
    # Dealers
    "Westville Dealer Recruited: Molly Presley" : ItemClassification.progression_skip_balancing,
    "Downtown Dealer Recruited: Brad Crosby" : ItemClassification.progression_skip_balancing,
    "Docks Dealer Recruited: Jane Lucero" : ItemClassification.progression_skip_balancing,
    "Suburbia Dealer Recruited: Wei Long" : ItemClassification.progression_skip_balancing,
    "Uptown Dealer Recruited: Leo Rivers" : ItemClassification.progression_skip_balancing,
    # Bad filler Items
    "Cuke" : ItemClassification.filler,
    "Banana" : ItemClassification.filler,
    "Paracetamol" : ItemClassification.filler,
    "Donut" : ItemClassification.filler,
    "Viagra" : ItemClassification.filler,
    "Mouth Wash": ItemClassification.filler,
    "Flu Medicine": ItemClassification.filler,
    "Gasoline": ItemClassification.filler,
    "Energy Drink": ItemClassification.filler,
    "Motor Oil": ItemClassification.filler,
    "Mega Bean": ItemClassification.filler,
    "Chili": ItemClassification.filler,
    "Battery": ItemClassification.filler,
    "Iodine": ItemClassification.filler,
    "Addy": ItemClassification.filler,
    "Horse Semen": ItemClassification.filler,
    "Baggies" : ItemClassification.filler,
    "Jar" : ItemClassification.filler,
    "Coffee Table" : ItemClassification.filler,
    "Wooden Square Table" : ItemClassification.filler,
    "Metal square Table" : ItemClassification.filler,
    "Floor Lamp" : ItemClassification.filler,
    "TV" : ItemClassification.filler,
    "Display Cabinet" : ItemClassification.filler,
    "Trash Bag" : ItemClassification.filler,
    "Trash Can" : ItemClassification.filler,
    "Plastic table" : ItemClassification.filler,
    "Toilet" : ItemClassification.filler,
    "Spray Bottle" : ItemClassification.filler,
    # Basic filler items
    "OG Kush Seed" : ItemClassification.filler,
    "PGR" : ItemClassification.filler,
    "Speed Grow" : ItemClassification.filler,
    "Grow Tent" : ItemClassification.filler,
    "Soil" : ItemClassification.filler,
    "Small Storage Rack" : ItemClassification.filler,
    "Medium Storage Rack" : ItemClassification.filler,
    "Fertilizer" : ItemClassification.filler,
    "Pot Sprinkler" : ItemClassification.filler,
    "Mixing Station" : ItemClassification.filler,
    "soil Pourer" : ItemClassification.filler,
    "Extra Long-Life Soil" : ItemClassification.filler,
    "Plastic pot" : ItemClassification.filler,
    "Moisture-preservative pot" : ItemClassification.filler,
    "Air pot" : ItemClassification.filler,
    # Better filler items
    "Packaging Station" : ItemClassification.filler,
    "Large Storage Rack" : ItemClassification.filler,
    "Long-Life Soil" : ItemClassification.filler,
    "Suspension Rack" : ItemClassification.filler,
    "Halogen Grow Light" : ItemClassification.filler,
    "LED Grow Light" : ItemClassification.filler,
    # Amazing filler items
    "Packaging Station Mk II" : ItemClassification.filler,
    "AC Unit" : ItemClassification.filler,
    "Mixing Station Mk II" : ItemClassification.filler,
    "Brick Press" : ItemClassification.filler,
    "Low-Quality Pseudo" : ItemClassification.filler,
    "Pseudo" : ItemClassification.filler,
    "High Quality Pseudo" : ItemClassification.filler,
    "Grain Bag" : ItemClassification.filler,
    "Spore Syringe" : ItemClassification.filler,
    "Mushroom Substrate" : ItemClassification.filler,
    # These fillers would allow you to possibly get checks out of logic (fun)
    "Acid" : ItemClassification.filler,
    "Phosphorus" : ItemClassification.filler,
    "Chemistry Station" : ItemClassification.filler,
    "Mushroom Spawn Station" : ItemClassification.filler,
    "Mushroom Bed" : ItemClassification.filler,
    "Drying Rack" : ItemClassification.filler,
    "Lab oven" : ItemClassification.filler,
    "Cauldron" : ItemClassification.filler,
    "Coca Seed" : ItemClassification.filler,
    # Weapons fillers
    "Revolver" : ItemClassification.filler,
    "Revolver Ammo" : ItemClassification.filler,
    "M1911 Pistol" : ItemClassification.filler,
    "M1911 Ammo" : ItemClassification.filler,
    "Pump Shotgun" : ItemClassification.filler,
    "Pump Shotgun Ammo" : ItemClassification.filler,
    "Machete" : ItemClassification.filler,
    "Frying Pan" : ItemClassification.filler,
    "Baseball Bat" : ItemClassification.filler,
    # Cartel influence items
    "Cartel Influence, Westville" : ItemClassification.progression_skip_balancing,
    "Cartel Influence, Downtown" : ItemClassification.progression_skip_balancing,
    "Cartel Influence, Docks" : ItemClassification.progression_skip_balancing,
    "Cartel Influence, Suburbia" : ItemClassification.progression_skip_balancing,
    "Cartel Influence, Uptown" : ItemClassification.progression_skip_balancing
}


# Each Item instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Item class and override the "game" field.
class Schedule1Item(Item):
    game = "Schedule1"

def add_xp_cash_bundle_items(world: Schedule1World) -> None:
    xp_reserved_num_start = 300
    cash_reserved_num_start = 315
    if world.options.number_of_xp_bundles > 0:
        current_xp_amount = world.options.amount_of_xp_per_bundle_min
        if world.options.number_of_xp_bundles == 1:
            DEFAULT_ITEM_CLASSIFICATIONS[f"XP Bundle {current_xp_amount}"] = ItemClassification.progression_skip_balancing
        else:
            xp_amount_increment = (world.options.amount_of_xp_per_bundle_max - world.options.amount_of_xp_per_bundle_min) // (world.options.number_of_xp_bundles - 1)
            for i in range(world.options.number_of_xp_bundles):
                item_name = f"XP Bundle {current_xp_amount + (xp_amount_increment * i)}"
                ITEM_NAME_TO_ID[item_name] = xp_reserved_num_start + i
                DEFAULT_ITEM_CLASSIFICATIONS[item_name] = ItemClassification.progression | ItemClassification.useful

    if world.options.number_of_cash_bundles > 0:
        current_cash_amount = world.options.amount_of_cash_per_bundle_min
        if world.options.number_of_cash_bundles == 1:
            DEFAULT_ITEM_CLASSIFICATIONS[f"Cash Bundle ${current_cash_amount}"] = ItemClassification.progression_skip_balancing
        else:
            cash_amount_increment = (world.options.amount_of_cash_per_bundle_max - world.options.amount_of_cash_per_bundle_min) // (world.options.number_of_cash_bundles - 1)
            for i in range(world.options.number_of_cash_bundles):
                item_name = f"Cash Bundle ${current_cash_amount + (cash_amount_increment * i)}"
                ITEM_NAME_TO_ID[item_name] = cash_reserved_num_start + i
                DEFAULT_ITEM_CLASSIFICATIONS[item_name] = ItemClassification.progression | ItemClassification.useful     

# Ontop of our regular itempool, our world must be able to create arbitrary amounts of filler as requested by core.
# To do this, it must define a function called world.get_filler_item_name(), which we will define in world.py later.
# For now, let's make a function that returns the name of a random filler item here in items.py.
def get_random_filler_item_name(world: Schedule1World) -> str:
    # For this purpose, we need to use a random generator.

    # IMPORTANT: Whenever you need to use a random generator, you must use world.random.
    # This ensures that generating with the same generator seed twice yields the same output.
    # DO NOT use a bare random object from Python's built-in random module.
    
    filler_pool_type = world.options.filler_item_pool_type
    
    if filler_pool_type == 0:
        # Random: All items classified as filler
        all_fillers = [name for name, classification in DEFAULT_ITEM_CLASSIFICATIONS.items() 
                       if classification == ItemClassification.filler]
        return world.random.choice(all_fillers)
    
    elif filler_pool_type == 1:
        # Random No Bad Items: Exclude bad fillers (Cuke to Spray Bottle)
        bad_items = [
            "Cuke", "Banana", "Paracetamol", "Donut", "Viagra", "Mouth Wash", "Flu Medicine",
            "Gasoline", "Energy Drink", "Motor Oil", "Mega Bean", "Chili", "Battery", "Iodine",
            "Addy", "Horse Semen", "Baggies", "Jar", "Coffee Table", "Wooden Square Table",
            "Metal square Table", "Floor Lamp", "TV", "Display Cabinet", "Trash Bag", "Trash Can",
            "Plastic table", "Toilet", "Spray Bottle"
        ]
        non_bad_fillers = [name for name, classification in DEFAULT_ITEM_CLASSIFICATIONS.items() 
                       if classification == ItemClassification.filler and name not in bad_items]
        return world.random.choice(non_bad_fillers)
    
    elif filler_pool_type == 2:
        # Random Only Good Items: Items from Packaging Station to Coca Seed
        good_items = [
            "Packaging Station", "Large Storage Rack", "Long-Life Soil", "Suspension Rack",
            "Halogen Grow Light", "LED Grow Light", "Packaging Station Mk II", "AC Unit",
            "Mixing Station Mk II", "Brick Press", "Low-Quality Pseudo", "Pseudo",
            "High Quality Pseudo", "Grain Bag", "Spore Syringe", "Mushroom Substrate",
            "Acid", "Phosphorus", "Chemistry Station", "Mushroom Spawn Station",
            "Mushroom Bed", "Drying Rack", "Lab oven", "Cauldron", "Coca Seed"
        ]
        return world.random.choice(good_items)
    
    # Fallback to a default filler
    return "OG Kush Seed"


def create_item_with_correct_classification(world: Schedule1World, name: str) -> Schedule1Item:
    # Our world class must have a create_item() function that can create any of our items by name at any time.
    # So, we make this helper function that creates the item by name with the correct classification.
    # Note: This function's content could just be the contents of world.create_item in world.py directly,
    # but it seemed nicer to have it in its own function over here in items.py.
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]

    # Item classification does not need to change based on options in Schedule1's case,
    return Schedule1Item(name, classification, ITEM_NAME_TO_ID[name], world.player)


# With those two helper functions defined, let's now get to actually creating and submitting our itempool.
def create_all_items(world: Schedule1World) -> None:
    # Create bundles
    add_xp_cash_bundle_items(world)
    # This is the function in which we will create all the items that this world submits to the multiworld item pool.
    # There must be exactly as many items as there are locations.

    # Creating items should generally be done via the world's create_item method.
    # First, we create a list containing all the items that always exist.

    itempool: list[Item] = []

    if world.options.randomize_level_unlocks:
        # If the randomize_level_unlocks option is enabled, we create all ten level unlock items.
        level_unlock_items = [
            "Jar Hardware Store Unlock",
            "PGR Hardware Store Unlock",
            "Speed Grow Hardware Store Unlock",
            "Long-Life Soil Hardware Store Unlock",
            "Fertilizer Hardware Store Unlock",
            "Sour Diesel Seeds Unlock",
            "Pot Sprinkler Hardware Store Unlock",
            "Electric Plant Trimmers Hardware Store Unlock",
            "Westville Region Unlock" ,
            "Low-Quality Pseudo Unlock" ,
            "Mixing Station Hardware Store Unlock" ,
            "Soil Pourer Hardware StoreUnlock",
            "Green Crack Seeds Unlock",
            "Viagor Gas Mart Unlock",
            "Extra Long-Life Soil Hardware Store Unlock",
            "Mouth Wash Gas Mart Unlock",
            "Grandaddy Purple Seeds Unlock",
            "Flu Medicine Gas Mart Unlock",
            "Packaging Station Mk II Hardware Store Unlock" ,
            "Gasoline Gas Mart Unlock",
            "Energy Drink Gas Mart Unlock",
            "Acid Warehouse Unlock" ,
            "Phosphorus Warehouse Unlock" ,
            "Chemistry Station Warehouse Unlock" ,
            "Lab Oven Warehouse Unlock" ,
            "Mixing Station Mk II Warehouse Unlock" ,
            "Motor Oil Gas Mart Unlock",
            "Mega Beans Gas Mart Unlock",
            "Air Pot Warehouse Unlock",
            "Chili Gas Mart Unlock",
            "Full Spectrum Grow Light warehouse Unlock",
            "Warehouse Access",
            "Battery Gas Mart Unlock",
            "Iodine Gas Mart Unlock",
            "Addy Gas Mart Unlock",
            "Drying Rack Warehouse Unlock",
            "Pseudo Unlock",
            "Horse Semen Gas Mart Unlock",
            "Revolver Warehouse Unlock",
            "Revolver Ammo Warehouse Unlock",
            "Brick Press Warehouse Unlock",
            "High Quality Pseudo Unlock",
            "Cauldron Warehouse Unlock",
            "Coca Seed Unlock",
            "M1911 Pistol Warehouse Unlock",
            "M1911 Ammo Warehouse Unlock",
            "Pump Shotgun Warehouse Unlock",
            "Pump Shotgun Ammo Warehouse Unlock"
        ]
        itempool += [world.create_item(name) for name in level_unlock_items]

    # Add all items with xp and cash bundles
    for item_name in ITEM_NAME_TO_ID.keys():
        if "XP Bundle" in item_name or "Cash Bundle" in item_name:
            itempool.append(world.create_item(item_name))

    if world.options.randomize_cartel_influence:
        for item_name in ITEM_NAME_TO_ID.keys():
            if "Cartel Influence" in item_name:
                itempool.append(world.create_item(item_name))

    if world.options.randomize_business_properties:
        business_properties = [
            "Business Property, Car Wash",
            "Business Property, Laundromat",
            "Business Property, Post Office",
            "Business Property, Taco Ticklers"
        ]
        itempool += [world.create_item(name) for name in business_properties]
    
    if world.options.randomize_drug_making_properties:
        drug_making_properties = [
            "Drug Making Property, Barn",
            "Drug Making Property, Bungalow",
            "Drug Making Property, Docks Warehouse",
            "Drug Making Property, Storage Unit"
        ]
        itempool += [world.create_item(name) for name in drug_making_properties]

    if world.options.randomize_dealers:
        dealers = [
            "Westville Dealer Recruited: Molly Presley",
            "Downtown Dealer Recruited: Brad Crosby",
            "Docks Dealer Recruited: Jane Lucero",
            "Suburbia Dealer Recruited: Wei Long",
            "Uptown Dealer Recruited: Leo Rivers"
        ]
        itempool += [world.create_item(name) for name in dealers]

    if world.options.randomize_customers:
        customers = [
            "Northtown Customer Unlocked: Austin Steiner",
            "Northtown Customer Unlocked: Beth Penn", # Mission related
            "Northtown Customer Unlocked: Chloe Bowers", # Mission related,
            "Northtown Customer Unlocked: Donna Martin",
            "Northtown Customer Unlocked: Geraldine Poon",
            "Northtown Customer Unlocked: Jessi Waters",
            "Northtown Customer Unlocked: Kathy Henderson",
            "Northtown Customer Unlocked: Kyle Cooley",
            "Northtown Customer Unlocked: Ludwig Meyer", # Mission related,
            "Northtown Customer Unlocked: Mick Lubbin",
            "Northtown Customer Unlocked: Mrs. Ming",
            "Northtown Customer Unlocked: Peggy Myers",
            "Northtown Customer Unlocked: Peter File",
            "Northtown Customer Unlocked: Sam Thompson", # Mission related
            "Westville Customer Unlocked: Charles Rowland", # Unlocks dealer
            "Westville Customer Unlocked: Dean Webster",
            "Westville Customer Unlocked: Doris Lubbin",
            "Westville Customer Unlocked: George Greene", # Unlocks dealer
            "Westville Customer Unlocked: Jerry Montero", # Unlocks dealer
            "Westville Customer Unlocked: Joyce Ball",
            "Westville Customer Unlocked: Keith Wagner",
            "Westville Customer Unlocked: Kim Delaney",
            "Westville Customer Unlocked: Meg Cooley",
            "Westville Customer Unlocked: Trent Sherman",
            "Downtown Customer Unlocked: Bruce Norton",
            "Downtown Customer Unlocked: Elizabeth Homley", # Unlocks supplier
            "Downtown Customer Unlocked: Eugene Buckley", # Unlocks dealer
            "Downtown Customer Unlocked: Greg Figgle", # Unlocks dealer
            "Downtown Customer Unlocked: Jeff Gilmore",
            "Downtown Customer Unlocked: Jennifer Rivera",
            "Downtown Customer Unlocked: Kevin Oakley", # Unlocks supplier
            "Downtown Customer Unlocked: Louis Fourier",
            "Downtown Customer Unlocked: Philip Wentworth",
            "Downtown Customer Unlocked: Randy Caulfield", # Unlocks dealer
            "Downtown Customer Unlocked: Lucy Pennington",
            "Docks Customer Unlocked: Anna Chesterfield",
            "Docks Customer Unlocked: Billy Kramer", # Mission related, Dealer
            "Docks Customer Unlocked: Cranky Frank",
            "Docks Customer Unlocked: Genghis Barn",
            "Docks Customer Unlocked: Javier Perez", # Unlocks supplier
            "Docks Customer Unlocked: Kelly Reynolds",
            "Docks Customer Unlocked: Lisa Gardner",
            "Docks Customer Unlocked: Mac Cooper", # Unlocks supplier
            "Docks Customer Unlocked: Marco Barone",
            "Docks Customer Unlocked: Melissa Wood", # Unlocks dealer
            "Docks Customer Unlocked: Sherman Giles",
            "Suburbia Customer Unlocked: Alison Knight",
            "Suburbia Customer Unlocked: Carl Bundy",
            "Suburbia Customer Unlocked: Chris Sullivan",
            "Suburbia Customer Unlocked: Dennis Kennedy",
            "Suburbia Customer Unlocked: Hank Stevenson",
            "Suburbia Customer Unlocked: Harold Colt", # Unlocks dealer
            "Suburbia Customer Unlocked: Jack Knight",
            "Suburbia Customer Unlocked: Jackie Stevenson", # Unlocks dealer
            "Suburbia Customer Unlocked: Jeremy Wilkinson", # Unlocks dealer
            "Suburbia Customer Unlocked: Karen Kennedy",
            "Uptown Customer Unlocked: Fiona Hancock",
            "Uptown Customer Unlocked: Herbert Bleuball",
            "Uptown Customer Unlocked: Irene Meadows",
            "Uptown Customer Unlocked: Jen Heard", # Sewer Key
            "Uptown Customer Unlocked: Lily Turner",
            "Uptown Customer Unlocked: Michael Boog", # Unlocks dealer
            "Uptown Customer Unlocked: Pearl Moore",
            "Uptown Customer Unlocked: Ray Hoffman", # Unlocks dealer
            "Uptown Customer Unlocked: Tobias Wentworth",
            "Uptown Customer Unlocked: Walter Cussler",
        ]
        itempool += [world.create_item(name) for name in customers]

    # Will add cartel influence items based on options
    if world.options.randomize_cartel_influence:
        for item_name in ITEM_NAME_TO_ID.keys():
            if "Cartel Influence" in item_name:
                for _ in range(world.options.cartel_influence_checks_per_region):
                    itempool.append(world.create_item(item_name))

    # The length of our itempool is easy to determine, since we have it as a list.
    number_of_items = len(itempool)

    # What we actually want is the number of *unfilled* locations. Luckily, there is a helper method for this:
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))

    # Now, we just subtract the number of items from the number of locations to get the number of empty item slots.
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    # Finally, we create that many filler items and add them to the itempool.
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    # This is how the generator actually knows about the existence of our items.
    world.multiworld.itempool += itempool