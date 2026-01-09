from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items

if TYPE_CHECKING:
    from .world import Schedule1World

# Every location must have a unique integer ID associated with it.
# We will have a lookup from location name to ID here that, in world.py, we will import and bind to the world class.
# Even if a location doesn't exist on specific options, it must be present in this lookup.
# There has to be a better way to do this...
LOCATION_NAME_TO_ID = {
    # Main/sub quests
    "Welcome To Hyland Point 1, open Phone" : 1,
    "Welcome To Hyland Point 2, talk to U.N at payphone" : 2,
    "Welcome To Hyland Point 3, collect stash near fountain" : 3,
    "welcome To Hyland Point 4, collect stage near canal" : 4,
    "Welcome To Hyland Point 5, collect stash behind supermarket" : 5,
    "Welcome To Hyland Point 6, head back to RV" : 6,
    "Welcome To Hyland Point 7, investigate the explosion" : 7,
    "Welcome To Hyland Point 8, read the note" : 8,
    "welcome To Hyland Point 9, talk on payphone" : 9,
    "Getting Started 1, talk to the manager in motel" : 10,
    "Getting Started 2, rent a motel room" : 11,
    "Getting Started 3, check out the motel room" : 12,
    "Gearing up 1, go to the hardware store " : 13,
    "Gearing up 2, buy 1x grow tent" : 14,
    "Gearing up 3, buy 1x soil" : 15,
    "Gearing up 4, buy 1x watering can" : 16,
    "Gearing up 5, head back to motel room" : 17,
    "Gearing up 6, place the grow tent and fill it with soil" : 18,
    "Gearing up 7, talk to uncle nelson on the phone" : 19,
    "Gearing up 8, Order 1x OG Kush Seed from Albert Hoover" : 20,
    "Gearing up 9, Wait for the dead drop" : 21,
    "Gearing up 10, Collect the dead drop" : 22,
    "Gearing up 11, Sow a weed seed" : 23,
    "Gearing up 12, Water the weed plant" : 24,
    "Gearing up 13, Harvest the weed plant once fully grown" : 25,
    "Gearing up 14, Package at least 3x weed" : 26,
    "Gearing up 15, List OG Kush for sale" : 27,
    "Packin 1, Buy 1x plant trimmers" : 28,
    "Packin 2, Buy 1x packaging station" : 29,
    "Packin 3, Buy 10x baggies" : 30,
    "packin 4, Place the packaging station in the motel room" : 31,
    "Keepin it fresh 1, Place the soil bag and vial in trash can" : 32,
    "Keepin it fresh 2, Buy a trash bag from the hardware store" : 33,
    "Keepin it fresh 3, Bag the contents of the trash can" : 34,
    "Keepin it fresh 4, Dispose of the trash bag" : 35,
    "On the Grind 1, Wait for a message from a customer" : 36,
    "On the Grind 2, Schedule your first deal" : 37,
    "On the Grind 3, Complete your first deal" : 38,
    "On the Grind 4, Buy and place another grow tent" : 39,
    "On the Grind 5, Complete 3 deals" : 40,
    "On the Grind 6, Talk to Uncle Nelson at a payphone" : 41,
    "On the Grind 7, Open the contacts app" : 42,
    "On the Grind 8, Select a friend of an unlocked customer in app" : 43,
    "On the Grind 9, Open the map app to see your potential customers" : 44,
    "On the Grind 10, Offer a free sample to a potential customer" : 45,
    "Moving up 1, Save $800 for a new property" : 46,
    "Moving up 2, Talk to Mrs. Ming at the Chinese restaurant" : 47,
    "Moving up 3, Purchase the room above the Chinese Restaurant" : 48,
    "Moving up 4, Move the grow tents and packaging station to the new room" : 49,
    "Moving up 5, Unlock 10 customers" : 50,
    "Dodgy Dealing 1, Talk to Uncle Nelson at a payphone" : 51,
    "Dodgy Dealing 2, Unlock Chloe, Ludwig, or Beth as customers" : 52,
    "Dodgy Dealing 3, friendly status with Chloe, Ludwig, or Beth" : 53,
    "Dodgy Dealing 4, Talk to Benji Coleman in Motel Room #2" : 54,
    "Dodgy Dealing 5, Recruit Benji Coleman as a dealer" : 55,
    "Dodgy Dealing 6, Provide Benji with at least 10x Weed" : 56,
    "Dodgy Dealing 7, Assign at least 3 customers to Benji" : 57,
    "Dodgy Dealing 8, Wait for Benji to complete a deal" : 58,
    "Dodgy Dealing 9, Collect the cash from Benji" : 59,
    "Mixing Mania 1, Talk to Uncle Nelson at a payphone" : 60,
    "Mixing Mania 2, Purchase a mixing station from the hardware store" : 61,
    "Mixing Mania 3, Place the mixing station" : 62,
    "Mixing Mania 4, Go to Gas-Mart" : 63,
    "Mixing Mania 5, Purchase at least one mixing ingredient" : 64,
    "Mixing Mania 6, Start a new mix at the mixing station" : 65,
    "Mixing Mania 7, Wait for the mix to complete" : 66,
    "Mixing Mania 8, Collect the new product" : 67,
    "Mixing Mania 9, Talk to Uncle Nelson at a payphone" : 68,
    "Mixing Mania 10, Mix a strain worth at least $60" : 69,
    "Making the Rounds 1, Talk to the real estate agent" : 70,
    "Making the Rounds 2, Talk to the dealership manager" : 71,
    "Making the Rounds 3, Talk to the mechanic" : 72,
    "Needin the Green, Earn $10,000" : 73,
    "Wretched Hive of Scum and Villany 1, Talk to Uncle Nelson at a payphone" : 74,
    "Wretched Hive of Scum and Villany 2, Gain access to the warehouse" : 75,
    "Wretched Hive of Scum and Villany 3, Talk to the merchant" : 76,
    "Wretched Hive of Scum and Villany 4, Talk to the arms dealer" : 77,
    "Wretched Hive of Scum and Villany 5, Talk to the fixer" : 78,
    "We Need to Cook 1, Talk to Uncle Nelson at a payphone" : 79,
    "We Need to Cook 2, Unlock the pseudo supplier in Westville" : 80,
    "We Need to Cook 3, Purchase a chemistry station from Oscar" : 81,
    "We Need to Cook 4, Purchase a lab oven from Oscar" : 82,
    "We Need to Cook 5, Purchase acid from Oscar" : 83,
    "We Need to Cook 6, Purchase phosphorus from Oscar" : 84,
    "We Need to Cook 7, Message Shirley about buying some pseudo" : 85,
    "We Need to Cook 8, Cook liquid meth at the chemistry station" : 86,
    "We Need to Cook 9, Bake the liquid meth with the lab oven" : 87,
    "Money Management, Deposit cash at an ATM" : 88,
    "Clean Cash 1, Talk to Uncle Nelson at a payphone" : 89,
    "Clean Cash 2, Purchase a business at Ray's Realty" : 90,
    "Clean Cash 3, Go to your new business" : 91,
    "Clean Cash 4, Use the laundering station" : 92,
    "Clean Cash 5, Wait for the laundering operation to complete" : 93,
    "Vibin' on the 'Cybin 1, Purchase a grain bag" : 94,
    "Vibin' on the 'Cybin 2, Purchase a spore syringe" : 95,
    "Vibin' on the 'Cybin 3, Purchase a mushroom spawn station" : 96,
    "Vibin' on the 'Cybin 4, Use the mushroom spawn station to inocculate a grain bag" : 97,
    "Vibin' on the 'Cybin 5, Purchase a mushroom bed from Oscar" : 98,
    "Vibin' on the 'Cybin 6, Purchase mushroom substrate from Fungal Phil" : 99,
    "Vibin' on the 'Cybin 7, Mix the shroom spawn into a mushroom bed" : 100,
    "Vibin' on the 'Cybin 8, Purchase an AC unit from a hardware store" : 101,
    "Vibin' on the 'Cybin 9, Use the AC unit to cool the mushroom bed" : 102,
    "Vibin' on the 'Cybin 10, Harvest the shrooms once fully grown" : 103,
    # Workers - criminal warehouse needed for this
    "Clearners 1, assign the cleaner to a locker" : 104,
    "Clearners 2, Assign a trash can to the cleaner" : 105,
    "Clearners 3, Place cash in the locker of the cleaner" : 106,
    "Botanists 1, assign the botanist to a locker" : 107,
    "Botanists 2, Assign a supplies source to the botanist" : 108,
    "Botanists 3, Assign a pot or grow tent to the botanist" : 109,
    "Botanists 4, Set the pot/grow tent destination" : 110,
    "Botanists 5, Place cash in the locker of the botanist" : 111,
    "Handlers 1, assign the packager to a locker" : 112,
    "Handlers 2, Assign a packaging station to the packager" : 113,
    "Handlers 3, Place cash in the locker of the packager" : 114,
    "Chemists 1, assign the chemist to a locker" : 115,
    "Chemists 2, Assign a station to the chemist" : 116,
    "Chemists 3, Place cash in the locker of the chemist" : 117,
    # Cartel - deal for the benzies not included as that's optional!
    "Unfavorable Agreements 1, Read the message from the unknown contact" : 118,
    "Unfavorable Agreements 2, Meet the stranger at the parking lot next to Taco Ticklers" : 119,
    "Finishing the job 1, Talk to Uncle Nelson at a payphone" : 120,
    "Finishing the job 2, Talk to Billy about buying explosives" : 121,
    "Finishing the job 3, Trade Billy 20x cocaine in return for RDX" : 122,
    "Finishing the job 4, Get Sam to dig access to the tunnel under Hyland Manor" : 123,
    "Finishing the job 5, Wait for Sam to dig access to the tunnel" : 124,
    "Finishing the job 6, Talk to Stan about turning the RDX into a bomb" : 125,
    "Finishing the job 7, Kill Stan's theif in docks at night" : 126,
    "Finishing the job 8, Get Stan to turn the RDX into a bomb" : 127,
    "Finishing the job 9, Plant the bomb under Hyland Manor" : 128,
    "Finishing the job 10, Wait for the bomb to detonate" : 129, 
    # level unlocks
    "Rank Street Rat III" : 130,
    "Rank Street Rat IV" : 131,
    "Rank Street Rat V" : 132,
    "Rank Hoodlum I" : 133,
    "Rank Hoodlum II" : 134,
    "Rank Hoodlum III" : 135,
    "Rank Hoodlum IV" : 136,
    "Rank Hoodlum V" : 137,
    "Rank Peddler I" : 138,
    "Rank Peddler II" : 139,
    "Rank Peddler III" : 140,
    "Rank Peddler IV" : 141,
    "Rank Peddler V" : 142,
    "Rank Hustler I" : 143,
    "Rank Hustler II" : 144,
    "Rank Hustler III" : 145,
    "Bagman V" : 146,
    "Enforcer I" : 147,
    "Block Boss I" : 148,
    # cartel influnce checks
    "Westville cartel influence 1" : 149,
    "Westville cartel influence 2" : 150,
    "Westville cartel influence 3" : 151,
    "Westville cartel influence 4" : 152,
    "Westville cartel influence 5" : 153,
    "Westville cartel influence 6" : 154,
    "Westville cartel influence 7" : 155,
    "Downtown cartel influence 1" : 156,
    "Downtown cartel influence 2" : 157,
    "Downtown cartel influence 3" : 158,
    "Downtown cartel influence 4" : 159,
    "Downtown cartel influence 5" : 160,
    "Downtown cartel influence 6" : 161,
    "Downtown cartel influence 7" : 162,
    "Docks cartel influence 1" : 163,
    "Docks cartel influence 2" : 164,
    "Docks cartel influence 3" : 165,
    "Docks cartel influence 4" : 166,
    "Docks cartel influence 5" : 167,
    "Docks cartel influence 6" : 168,
    "Docks cartel influence 7" : 169,
    "Suburbia cartel influence 1" : 170,
    "Suburbia cartel influence 2" : 171,
    "Suburbia cartel influence 3" : 172,
    "Suburbia cartel influence 4" : 173,
    "Suburbia cartel influence 5" : 174,
    "Suburbia cartel influence 6" : 175,
    "Suburbia cartel influence 7" : 176,
    "Uptown cartel influcence 1" : 177,
    "Uptown cartel influcence 2" : 178,
    "Uptown cartel influcence 3" : 179,
    "Uptown cartel influcence 4" : 180,
    "Uptown cartel influcence 5" : 181,
    "Uptown cartel influcence 6" : 182,
    "Uptown cartel influcence 7" : 183,
    # Drug Making Properties
    "Drug Making Property, Barn" : 184,
    "Drug Making Property, Bungalow" : 185,
    "Drug Making Property, Docks Warehouse" : 186,
    "Drug Making Property, Motel Room" : 187,
    "Drug Making Property, Sewer" : 188,
    "Drug Making Property, Storage Unit" : 189,
    "Drug Making Property, Sweatshop" : 190,
    # Business Properties
    "Business Property, Car Wash" : 191,
    "Business Property, Laundromat" : 192,
    "Business Property, Post Office" : 193,
    "Business Property, Taco Ticklers" : 194,
    # Recipe checks
    "Weed Recipe 1" : 195,
    "Weed Recipe 2" : 196,
    "Weed Recipe 3" : 197,
    "Weed Recipe 4" : 198,
    "Weed Recipe 5" : 199,
    "Weed Recipe 6" : 200,
    "Weed Recipe 7" : 201,
    "Weed Recipe 8" : 202,
    "Weed Recipe 9" : 203,
    "Weed Recipe 10" : 204,
    "Weed Recipe 11" : 205,
    "Weed Recipe 12" : 206,
    "Weed Recipe 13" : 207,
    "Weed Recipe 14" : 208,
    "Weed Recipe 15" : 209,
    "Meth Recipe 1" : 210,
    "Meth Recipe 2" : 211,
    "Meth Recipe 3" : 212,
    "Meth Recipe 4" : 213,
    "Meth Recipe 5" : 214,
    "Meth Recipe 6" : 215,
    "Meth Recipe 7" : 216,
    "Meth Recipe 8" : 217,
    "Meth Recipe 9" : 218,
    "Meth Recipe 10" : 219,
    "Meth Recipe 11" : 220,
    "Meth Recipe 12" : 221,
    "Meth Recipe 13" : 222,
    "Meth Recipe 14" : 223,
    "Meth Recipe 15" : 224,
    "Shrooms Recipe 1" : 225,
    "Shrooms Recipe 2" : 226,
    "Shrooms Recipe 3" : 227,
    "Shrooms Recipe 4" : 228,
    "Shrooms Recipe 5" : 229,
    "Shrooms Recipe 6" : 230,
    "Shrooms Recipe 7" : 231,
    "Shrooms Recipe 8" : 232,
    "Shrooms Recipe 9" : 233,
    "Shrooms Recipe 10" : 234,
    "Shrooms Recipe 11" : 235,
    "Shrooms Recipe 12" : 236,
    "Shrooms Recipe 13" : 237,
    "Shrooms Recipe 14" : 238,
    "Shrooms Recipe 15" : 239,
    "Cocaine Recipe 1" : 240,
    "Cocaine Recipe 2" : 241,
    "Cocaine Recipe 3" : 242,
    "Cocaine Recipe 4" : 243,
    "Cocaine Recipe 5" : 244,
    "Cocaine Recipe 6" : 245,
    "Cocaine Recipe 7" : 246,
    "Cocaine Recipe 8" : 247,
    "Cocaine Recipe 9" : 248,
    "Cocaine Recipe 10" : 249,
    "Cocaine Recipe 11" : 250,
    "Cocaine Recipe 12" : 251,
    "Cocaine Recipe 13" : 252,
    "Cocaine Recipe 14" : 253,
    "Cocaine Recipe 15" : 254,
    # Cash for Trash checks
    "Cash for Trash 1, Collect 10 pieces of trash" : 255,
    "Cash for Trash 2, Collect 20 pieces of trash" : 256,
    "Cash for Trash 3, Collect 30 pieces of trash" : 257,
    "Cash for Trash 4, Collect 40 pieces of trash" : 258,
    "Cash for Trash 5, Collect 50 pieces of trash" : 259,
    "Cash for Trash 6, Collect 60 pieces of trash" : 260,
    "Cash for Trash 7, Collect 70 pieces of trash" : 261,
    "Cash for Trash 8, Collect 80 pieces of trash" : 262,
    "Cash for Trash 9, Collect 90 pieces of trash" : 263,
    "Cash for Trash 10, Collect 100 pieces of trash" : 264,
    "Cash for Trash 11, Collect 110 pieces of trash" : 265,
    "Cash for Trash 12, Collect 120 pieces of trash" : 266,
    "Cash for Trash 13, Collect 130 pieces of trash" : 267,
    "Cash for Trash 14, Collect 140 pieces of trash" : 268,
    "Cash for Trash 15, Collect 150 pieces of trash" : 269,
    "Cash for Trash 16, Collect 160 pieces of trash" : 270,
    "Cash for Trash 17, Collect 170 pieces of trash" : 271,
    "Cash for Trash 18, Collect 180 pieces of trash" : 272,
    "Cash for Trash 19, Collect 190 pieces of trash" : 273,
    "Cash for Trash 20, Collect 200 pieces of trash" : 274,
    "Cash for Trash 21, Collect 210 pieces of trash" : 275,
    "Cash for Trash 22, Collect 220 pieces of trash" : 276,
    "Cash for Trash 23, Collect 230 pieces of trash" : 277,
    "Cash for Trash 24, Collect 240 pieces of trash" : 278,
    "Cash for Trash 25, Collect 250 pieces of trash" : 279,
    "Cash for Trash 26, Collect 260 pieces of trash" : 280,
    "Cash for Trash 27, Collect 270 pieces of trash" : 281,
    "Cash for Trash 28, Collect 280 pieces of trash" : 282,
    "Cash for Trash 29, Collect 290 pieces of trash" : 283,
    "Cash for Trash 30, Collect 300 pieces of trash" : 284,
    "Cash for Trash 31, Collect 310 pieces of trash" : 285,
    "Cash for Trash 32, Collect 320 pieces of trash" : 286,
    "Cash for Trash 33, Collect 330 pieces of trash" : 287,
    "Cash for Trash 34, Collect 340 pieces of trash" : 288,
    "Cash for Trash 35, Collect 350 pieces of trash" : 289,
    "Cash for Trash 36, Collect 360 pieces of trash" : 290,
    "Cash for Trash 37, Collect 370 pieces of trash" : 291,
    "Cash for Trash 38, Collect 380 pieces of trash" : 292,
    "Cash for Trash 39, Collect 390 pieces of trash" : 293,
    "Cash for Trash 40, Collect 400 pieces of trash" : 294,
    "Cash for Trash 41, Collect 410 pieces of trash" : 295,
    "Cash for Trash 42, Collect 420 pieces of trash" : 296,
    "Cash for Trash 43, Collect 430 pieces of trash" : 297,
    "Cash for Trash 44, Collect 440 pieces of trash" : 298,
    "Cash for Trash 45, Collect 450 pieces of trash" : 299,
    "Cash for Trash 46, Collect 460 pieces of trash" : 300,
    "Cash for Trash 47, Collect 470 pieces of trash" : 301,
    "Cash for Trash 48, Collect 480 pieces of trash" : 302,
    "Cash for Trash 49, Collect 490 pieces of trash" : 303,
    "Cash for Trash 50, Collect 500 pieces of trash" : 304,
    # Customers
    "Unlock Northtown Customer: Austin Steiner" : 305,
    "Unlock Northtown Customer: Beth Penn" : 306,
    "Unlock Northtown Customer: Chloe Bowers" : 307,
    "Unlock Northtown Customer: Donna Martin" : 308,
    "Unlock Northtown Customer: Geraldine Poon" : 309,
    "Unlock Northtown Customer: Jessi Waters" : 310,
    "Unlock Northtown Customer: Kathy Henderson" : 311,
    "Unlock Northtown Customer: Kyle Cooley" : 312,
    "Unlock Northtown Customer: Ludwig Meyer" : 313,
    "Unlock Northtown Customer: Mick Lubbin" : 314,
    "Unlock Northtown Customer: Mrs. Ming" : 315,
    "Unlock Northtown Customer: Peggy Myers" : 316,
    "Unlock Northtown Customer: Peter File" : 317,
    "Unlock Northtown Customer: Sam Thompson" : 318,
    "Unlock Westville Customer: Charles Rowland" : 319,
    "Unlock Westville Customer: Dean Webster" : 320,
    "Unlock Westville Customer: Doris Lubbin" : 321,
    "Unlock Westville Customer: George Greene" : 322,
    "Unlock Westville Customer: Jerry Montero" : 323,
    "Unlock Westville Customer: Joyce Ball" : 324,
    "Unlock Westville Customer: Keith Wagner" : 325,
    "Unlock Westville Customer: Kim Delaney" : 326,
    "Unlock Westville Customer: Meg Cooley" : 327,
    "Unlock Westville Customer: Trent Sherman" : 328,
    "Unlock Downtown Customer: Bruce Norton" : 329,
    "Unlock Downtown Customer: Elizabeth Homley" : 330,
    "Unlock Downtown Customer: Eugene Buckley" : 331,
    "Unlock Downtown Customer: Greg Figgle" : 332,
    "Unlock Downtown Customer: Jeff Gilmore" : 333,
    "Unlock Downtown Customer: Jennifer Rivera" : 334,
    "Unlock Downtown Customer: Kevin Oakley" : 335,
    "Unlock Downtown Customer: Louis Fourier" : 336,
    "Unlock Downtown Customer: Philip Wentworth" : 337,
    "Unlock Downtown Customer: Randy Caulfield" : 338,
    "Unlock Downtown Customer: Lucy Pennington" : 339,
    "Unlock Docks Customer: Anna Chesterfield" : 340,
    "Unlock Docks Customer: Billy Kramer" : 341,
    "Unlock Docks Customer: Cranky Frank" : 342,
    "Unlock Docks Customer: Genghis Barn" : 343,
    "Unlock Docks Customer: Javier Perez" : 344,
    "Unlock Docks Customer: Kelly Reynolds" : 345,
    "Unlock Docks Customer: Lisa Gardner" : 346,
    "Unlock Docks Customer: Mac Cooper" : 347,
    "Unlock Docks Customer: Marco Barone" : 348,
    "Unlock Docks Customer: Melissa Wood" : 349,
    "Unlock Docks Customer: Sherman Giles" : 350,
    "Unlock Suburbia Customer: Alison Knight" : 351,
    "Unlock Suburbia Customer: Carl Bundy" : 352,
    "Unlock Suburbia Customer: Chris Sullivan" : 353,
    "Unlock Suburbia Customer: Dennis Kennedy" : 354,
    "Unlock Suburbia Customer: Hank Stevenson" : 355,
    "Unlock Suburbia Customer: Harold Colt" : 356,
    "Unlock Suburbia Customer: Jack Knight" : 357,
    "Unlock Suburbia Customer: Jackie Stevenson" : 358,
    "Unlock Suburbia Customer: Jeremy Wilkinson" : 359,
    "Unlock Suburbia Customer: Karen Kennedy" : 360,
    "Unlock Uptown Customer: Fiona Hancock" : 361,
    "Unlock Uptown Customer: Herbert Bleuball" : 362,
    "Unlock Uptown Customer: Irene Meadows" : 363,
    "Unlock Uptown Customer: Jen Heard" : 364,
    "Unlock Uptown Customer: Lily Turner" : 365,
    "Unlock Uptown Customer: Michael Boog" : 366,
    "Unlock Uptown Customer: Pearl Moore" : 367,
    "Unlock Uptown Customer: Ray Hoffman" : 368,
    "Unlock Uptown Customer: Tobias Wentworth" : 369,
    "Unlock Uptown Customer: Walter Cussler" : 370,
    # Recruit Dealers - benji not included as that's quest tied
    "Recruit Westville Dealer: Molly Presley" : 372,
    "Recruit Downtown Dealer: Brad Crosby" : 373,
    "Recruit Docks Dealer: Jane Lucero" : 374,
    "Recruit Suburbia Dealer: Wei Long" : 375,
    "Recruit Uptown Dealer: Leo Rivers" : 376,
}   


# Each Location instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Location class and override the "game" field.
class Schedule1Location(Location):
    game = "Schedule1"


# Let's make one more helper method before we begin actually creating locations.
# Later on in the code, we'll want specific subsections of LOCATION_NAME_TO_ID.
# To reduce the chance of copy-paste errors writing something like {"Chest": LOCATION_NAME_TO_ID["Chest"]},
# let's make a helper method that takes a list of location names and returns them as a dict with their IDs.
# Note: There is a minor typing quirk here. Some functions want location addresses to be an "int | None",
# so while our function here only ever returns dict[str, int], we annotate it as dict[str, int | None].
def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: Schedule1World) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: Schedule1World) -> None:
    # Finally, we need to put the Locations ("checks") into their regions.
    # Once again, before we do anything, we can grab our regions we created by using world.get_region()
    overworld = world.get_region("Overworld")
    missions = world.get_region("Missions")
    if world.options.randomize_level_unlocks:
        level_unlocks = world.get_region("Level Unlocks")
    if world.options.randomize_business_properties or world.options.randomize_drug_making_properties:
        realtor = world.get_region("Realtor")
    
    # Customer unlock locations - add to their respective regions
    customer_region_northtown = world.get_region("Customer Northtown")
    customer_region_westville = world.get_region("Customer Westville")
    customer_region_downtown = world.get_region("Customer Downtown")
    customer_region_docks = world.get_region("Customer Docks")
    customer_region_suburbia = world.get_region("Customer Suburbia")
    customer_region_uptown = world.get_region("Customer Uptown")

    # A simpler way to do this is by using the region.add_locations helper.
    # For this, you need to have a dict of location names to their IDs (i.e. a subset of location_name_to_id)
    # Aha! So that's why we made that "get_location_names_with_ids" helper method earlier.
    # You also need to pass your overridden Location class.
    # So dirty, this is horrible
    mission_locations = get_location_names_with_ids([    
        "Welcome To Hyland Point 1, open Phone",
        "Welcome To Hyland Point 2, talk to U.N at payphone",
        "Welcome To Hyland Point 3, collect stash near fountain",
        "welcome To Hyland Point 4, collect stage near canal",
        "Welcome To Hyland Point 5, collect stash behind supermarket",
        "Welcome To Hyland Point 6, head back to RV",
        "Welcome To Hyland Point 7, investigate the explosion",
        "Welcome To Hyland Point 8, read the note",
        "welcome To Hyland Point 9, talk on payphone",
        "Getting Started 1, talk to the manager in motel",
        "Getting Started 2, rent a motel room",
        "Getting Started 3, check out the motel room",
        "Gearing up 1, go to the hardware store ",
        "Gearing up 2, buy 1x grow tent",
        "Gearing up 3, buy 1x soil",
        "Gearing up 4, buy 1x watering can",
        "Gearing up 5, head back to motel room",
        "Gearing up 6, place the grow tent and fill it with soil",
        "Gearing up 7, talk to uncle nelson on the phone",
        "Gearing up 8, Order 1x OG Kush Seed from Albert Hoover",
        "Gearing up 9, Wait for the dead drop",
        "Gearing up 10, Collect the dead drop",
        "Gearing up 11, Sow a weed seed",
        "Gearing up 12, Water the weed plant",
        "Gearing up 13, Harvest the weed plant once fully grown",
        "Gearing up 14, Package at least 3x weed",
        "Gearing up 15, List OG Kush for sale",
        "Packin 1, Buy 1x plant trimmers",
        "Packin 2, Buy 1x packaging station",
        "Packin 3, Buy 10x baggies",
        "packin 4, Place the packaging station in the motel room",
        "Keepin it fresh 1, Place the soil bag and vial in trash can",
        "Keepin it fresh 2, Buy a trash bag from the hardware store",
        "Keepin it fresh 3, Bag the contents of the trash can",
        "Keepin it fresh 4, Dispose of the trash bag",
        "On the Grind 1, Wait for a message from a customer",
        "On the Grind 2, Schedule your first deal",
        "On the Grind 3, Complete your first deal",
        "On the Grind 4, Buy and place another grow tent",
        "On the Grind 5, Complete 3 deals",
        "On the Grind 6, Talk to Uncle Nelson at a payphone",
        "On the Grind 7, Open the contacts app",
        "On the Grind 8, Select a friend of an unlocked customer in app",
        "On the Grind 9, Open the map app to see your potential customers",
        "On the Grind 10, Offer a free sample to a potential customer",
        "Moving up 1, Save $800 for a new property",
        "Moving up 2, Talk to Mrs. Ming at the Chinese restaurant",
        "Moving up 3, Purchase the room above the Chinese Restaurant",
        "Moving up 4, Move the grow tents and packaging station to the new room",
        "Moving up 5, Unlock 10 customers",
        "Dodgy Dealing 1, Talk to Uncle Nelson at a payphone",
        "Dodgy Dealing 2, Unlock Chloe, Ludwig, or Beth as customers",
        "Dodgy Dealing 3, friendly status with Chloe, Ludwig, or Beth",
        "Dodgy Dealing 4, Talk to Benji Coleman in Motel Room #2",
        "Dodgy Dealing 5, Recruit Benji Coleman as a dealer",
        "Dodgy Dealing 6, Provide Benji with at least 10x Weed",
        "Dodgy Dealing 7, Assign at least 3 customers to Benji",
        "Dodgy Dealing 8, Wait for Benji to complete a deal",
        "Dodgy Dealing 9, Collect the cash from Benji",
        "Mixing Mania 1, Talk to Uncle Nelson at a payphone",
        "Mixing Mania 2, Purchase a mixing station from the hardware store",
        "Mixing Mania 3, Place the mixing station",
        "Mixing Mania 4, Go to Gas-Mart",
        "Mixing Mania 5, Purchase at least one mixing ingredient",
        "Mixing Mania 6, Start a new mix at the mixing station",
        "Mixing Mania 7, Wait for the mix to complete",
        "Mixing Mania 8, Collect the new product",
        "Mixing Mania 9, Talk to Uncle Nelson at a payphone",
        "Mixing Mania 10, Mix a strain worth at least $60",
        "Making the Rounds 1, Talk to the real estate agent",
        "Making the Rounds 2, Talk to the dealership manager",
        "Making the Rounds 3, Talk to the mechanic",
        "Needin the Green, Earn $10,000",
        "Wretched Hive of Scum and Villany 1, Talk to Uncle Nelson at a payphone",
        "Wretched Hive of Scum and Villany 2, Gain access to the warehouse",
        "Wretched Hive of Scum and Villany 3, Talk to the merchant",
        "Wretched Hive of Scum and Villany 4, Talk to the arms dealer",
        "Wretched Hive of Scum and Villany 5, Talk to the fixer",
        "We Need to Cook 1, Talk to Uncle Nelson at a payphone",
        "We Need to Cook 2, Unlock the pseudo supplier in Westville",
        "We Need to Cook 3, Purchase a chemistry station from Oscar",
        "We Need to Cook 4, Purchase a lab oven from Oscar",
        "We Need to Cook 5, Purchase acid from Oscar",
        "We Need to Cook 6, Purchase phosphorus from Oscar",
        "We Need to Cook 7, Message Shirley about buying some pseudo",
        "We Need to Cook 8, Cook liquid meth at the chemistry station",
        "We Need to Cook 9, Bake the liquid meth with the lab oven",
        "Money Management, Deposit cash at an ATM",
        "Clean Cash 1, Talk to Uncle Nelson at a payphone",
        "Clean Cash 2, Purchase a business at Ray's Realty",
        "Clean Cash 3, Go to your new business",
        "Clean Cash 4, Use the laundering station",
        "Clean Cash 5, Wait for the laundering operation to complete",
        "Vibin' on the 'Cybin 1, Purchase a grain bag",
        "Vibin' on the 'Cybin 2, Purchase a spore syringe",
        "Vibin' on the 'Cybin 3, Purchase a mushroom spawn station",
        "Vibin' on the 'Cybin 4, Use the mushroom spawn station to inocculate a grain bag",
        "Vibin' on the 'Cybin 5, Purchase a mushroom bed from Oscar",
        "Vibin' on the 'Cybin 6, Purchase mushroom substrate from Fungal Phil",
        "Vibin' on the 'Cybin 7, Mix the shroom spawn into a mushroom bed",
        "Vibin' on the 'Cybin 8, Purchase an AC unit from a hardware store",
        "Vibin' on the 'Cybin 9, Use the AC unit to cool the mushroom bed",
        "Vibin' on the 'Cybin 10, Harvest the shrooms once fully grown",
        "Clearners 1, assign the cleaner to a locker",
        "Clearners 2, Assign a trash can to the cleaner",
        "Clearners 3, Place cash in the locker of the cleaner",
        "Botanists 1, assign the botanist to a locker",
        "Botanists 2, Assign a supplies source to the botanist",
        "Botanists 3, Assign a pot or grow tent to the botanist",
        "Botanists 4, Set the pot/grow tent destination",
        "Botanists 5, Place cash in the locker of the botanist",
        "Handlers 1, assign the packager to a locker",
        "Handlers 2, Assign a packaging station to the packager",
        "Handlers 3, Place cash in the locker of the packager",
        "Chemists 1, assign the chemist to a locker",
        "Chemists 2, Assign a station to the chemist",
        "Chemists 3, Place cash in the locker of the chemist",
        "Unfavorable Agreements 1, Read the message from the unknown contact",
        "Unfavorable Agreements 2, Meet the stranger at the parking lot next to Taco Ticklers",
        "Finishing the job 1, Talk to Uncle Nelson at a payphone",
        "Finishing the job 2, Talk to Billy about buying explosives",
        "Finishing the job 3, Trade Billy 20x cocaine in return for RDX",
        "Finishing the job 4, Get Sam to dig access to the tunnel under Hyland Manor",
        "Finishing the job 5, Wait for Sam to dig access to the tunnel",
        "Finishing the job 6, Talk to Stan about turning the RDX into a bomb",
        "Finishing the job 7, Kill Stan's theif in docks at night",
        "Finishing the job 8, Get Stan to turn the RDX into a bomb",
        "Finishing the job 9, Plant the bomb under Hyland Manor",
        "Finishing the job 10, Wait for the bomb to detonate"
    ])

    missions.add_locations(mission_locations, Schedule1Location)

    
    # Level Unlocks
    if world.options.randomize_level_unlocks:
        level_unlocks_locations = get_location_names_with_ids([
            "Rank Street Rat III",
            "Rank Street Rat IV",
            "Rank Street Rat V",
            "Rank Hoodlum I",
            "Rank Hoodlum II",
            "Rank Hoodlum III",
            "Rank Hoodlum IV",
            "Rank Hoodlum V",
            "Rank Peddler I",
            "Rank Peddler II",
            "Rank Peddler III",
            "Rank Peddler IV",
            "Rank Peddler V",
            "Rank Hustler I",
            "Rank Hustler II",
            "Rank Hustler III",
            "Bagman V",
            "Enforcer I",
            "Block Boss I"
        ])
        level_unlocks.add_locations(level_unlocks_locations, Schedule1Location)

    # property checks
    if world.options.randomize_business_properties:
        business_property_locations = get_location_names_with_ids([
            "Business Property, Car Wash",
            "Business Property, Laundromat",
            "Business Property, Post Office",
            "Business Property, Taco Ticklers"])
        realtor.add_locations(business_property_locations, Schedule1Location)

    # Note: Motel Room, and sweatshop aren't included in checks for realtor
    # These checks are already included within missions
    if world.options.randomize_drug_making_properties:
        drug_making_property_locations = get_location_names_with_ids([
            "Drug Making Property, Barn",
            "Drug Making Property, Bungalow",
            "Drug Making Property, Docks Warehouse",
            "Drug Making Property, Storage Unit",
        ])
        realtor.add_locations(drug_making_property_locations, Schedule1Location)
    
    #sewer is an odd check, I'll add it here instead of with other customer checks
    sewer_location = get_location_names_with_ids(["Drug Making Property, Sewer"])
    
    customer_region_uptown.add_locations(sewer_location, Schedule1Location)

    # Customer locations - extract from LOCATION_NAME_TO_ID and group by region
    customers_by_region = {}
    for location_name in LOCATION_NAME_TO_ID.keys():
        if location_name.startswith("Unlock") and "Customer:" in location_name:
            # Extract region name from "Unlock {Region} Customer: ..."
            region_name = location_name.split()[1]  # Gets "Northtown", "Westville", etc.
            if region_name not in customers_by_region:
                customers_by_region[region_name] = []
            customers_by_region[region_name].append(location_name)
    
    # Add customer locations to their respective regions
    region_mapping = {
        "Northtown": customer_region_northtown,
        "Westville": customer_region_westville,
        "Downtown": customer_region_downtown,
        "Docks": customer_region_docks,
        "Suburbia": customer_region_suburbia,
        "Uptown": customer_region_uptown,
    }
    # Add customer checks to their regions
    for region_name, locations in customers_by_region.items():
        region = region_mapping[region_name]
        region_locations_dict = get_location_names_with_ids(locations)
        region.add_locations(region_locations_dict, Schedule1Location)


    if not world.options.randomize_cartel_influence:
        cartel_region_westville = world.get_region("Cartel Westville")
        cartel_region_downtown = world.get_region("Cartel Downtown")
        cartel_region_docks = world.get_region("Cartel Docks")
        cartel_region_suburbia = world.get_region("Cartel Suburbia")
        cartel_region_uptown = world.get_region("Cartel Uptown")
        # So dirty, but let's just go with it for now.
        cartel_region_westville_locations = get_location_names_with_ids([
            "Westville cartel influence 1",
            "Westville cartel influence 2",
            "Westville cartel influence 3",
            "Westville cartel influence 4",
            "Westville cartel influence 5",
            "Westville cartel influence 6",
            "Westville cartel influence 7"
        ])
        cartel_region_westville.add_locations(cartel_region_westville_locations, Schedule1Location)

        cartel_region_downtown_locations = get_location_names_with_ids([
            "Downtown cartel influence 1",
            "Downtown cartel influence 2",
            "Downtown cartel influence 3",
            "Downtown cartel influence 4",
            "Downtown cartel influence 5",
            "Downtown cartel influence 6",
            "Downtown cartel influence 7"
        ])
        cartel_region_downtown.add_locations(cartel_region_downtown_locations, Schedule1Location)

        cartel_region_docks_locations = get_location_names_with_ids([
            "Docks cartel influence 1",
            "Docks cartel influence 2",
            "Docks cartel influence 3",
            "Docks cartel influence 4",
            "Docks cartel influence 5",
            "Docks cartel influence 6",
            "Docks cartel influence 7"
        ])
        cartel_region_docks.add_locations(cartel_region_docks_locations, Schedule1Location)

        cartel_region_suburbia_locations = get_location_names_with_ids([
            "Suburbia cartel influence 1",
            "Suburbia cartel influence 2",
            "Suburbia cartel influence 3",
            "Suburbia cartel influence 4",
            "Suburbia cartel influence 5",
            "Suburbia cartel influence 6",
            "Suburbia cartel influence 7"
        ])
        cartel_region_suburbia.add_locations(cartel_region_suburbia_locations, Schedule1Location)

        cartel_region_uptown_locations = get_location_names_with_ids([
            "Uptown cartel influence 1",
            "Uptown cartel influence 2",
            "Uptown cartel influence 3",
            "Uptown cartel influence 4",
            "Uptown cartel influence 5",
            "Uptown cartel influence 6",
            "Uptown cartel influence 7"
        ])
        cartel_region_uptown.add_locations(cartel_region_uptown_locations, Schedule1Location)

    # Recipe checks - Only include the number specified by the RecipeChecks option
    if world.options.recipe_checks > 0:
        # Get each recipe region
        weed_recipe_region = world.get_region("Weed Recipe Checks")
        meth_recipe_region = world.get_region("Meth Recipe Checks")
        shrooms_recipe_region = world.get_region("Shrooms Recipe Checks")
        cocaine_recipe_region = world.get_region("Cocaine Recipe Checks")
        
        # Drug types with their regions and starting IDs in LOCATION_NAME_TO_ID
        drug_types = [
            ("Weed Recipe", 195, weed_recipe_region),
            ("Meth Recipe", 210, meth_recipe_region),
            ("Shrooms Recipe", 225, shrooms_recipe_region),
            ("Cocaine Recipe", 240, cocaine_recipe_region),
        ]
        
        # Generate and add recipe locations for each drug type to its respective region
        for drug_name, start_id, region in drug_types:
            recipe_locations = []
            for i in range(1, world.options.recipe_checks + 1):
                recipe_locations.append(f"{drug_name} {i}")
            
            recipe_locations_dict = get_location_names_with_ids(recipe_locations)
            region.add_locations(recipe_locations_dict, Schedule1Location)
        
    # Cash for Trash checks - Only include the number specified by the CashForTrash option
    cash_for_trash_count = world.options.cash_for_trash
    if cash_for_trash_count > 0:
        cash_for_trash_locations = []
        for i in range(1, cash_for_trash_count + 1):
            cash_for_trash_locations.append(f"Cash for Trash {i}, Collect {i * 10} pieces of trash")
        cash_for_trash_locations_dict = get_location_names_with_ids(cash_for_trash_locations)
        overworld.add_locations(cash_for_trash_locations_dict, Schedule1Location)


    # Recruit Dealer locations - add to their respective regions - match them to customer regions
    if not world.options.randomize_dealers:
        westville_dealer_location = get_location_names_with_ids(["Recruit Westville Dealer: Molly Presley"])
        customer_region_westville.add_locations(westville_dealer_location, Schedule1Location)
        downtown_dealer_location = get_location_names_with_ids(["Recruit Downtown Dealer: Brad Crosby"])
        customer_region_downtown.add_locations(downtown_dealer_location, Schedule1Location)
        docks_dealer_location = get_location_names_with_ids(["Recruit Docks Dealer: Jane Lucero"])
        customer_region_docks.add_locations(docks_dealer_location, Schedule1Location)
        suburbia_dealer_location = get_location_names_with_ids(["Recruit Suburbia Dealer: Wei Long"])
        customer_region_suburbia.add_locations(suburbia_dealer_location, Schedule1Location)
        uptown_dealer_location = get_location_names_with_ids(["Recruit Uptown Dealer: Leo Rivers"])
        customer_region_uptown.add_locations(uptown_dealer_location, Schedule1Location)


def create_events(world: Schedule1World) -> None:
    # All mission completions are checks, however, they don't have an item associated with them.
    # We need to associate an event location/ event item for each mission completion.
    # This gives us a way to link missions
    overworld = world.get_region("Overworld")
    missions = world.get_region("Missions")
    
    # If goal is not "Reach Networth Goal", include Cartel Defeated event
    if world.options.goal != 1:
        missions.add_event(
            "Cartel Defeated", "Cartel Defeated", 
            location_type=Schedule1Location, item_type=items.Schedule1Item
        )

    # if goal includes networth, include Networth Goal Reached event
    if world.options.goal < 2:
        overworld.add_event(
            "Networth Goal Reached", "Networth Goal Reached", 
            location_type=Schedule1Location, item_type=items.Schedule1Item
        )
    
    # Checks to see if 700 cartel cleared when cartel are not randomized
    overworld.add_event("Westville Cartel Cleared", "Downtown Customers Unlocked", 
                        location_type=Schedule1Location, item_type=items.Schedule1Item)
    overworld.add_event("Downtown Cartel Cleared", "Docks Customers Unlocked", 
                        location_type=Schedule1Location, item_type=items.Schedule1Item)
    overworld.add_event("Docks Cartel Cleared", "Suburbia Customers Unlocked", 
                        location_type=Schedule1Location, item_type=items.Schedule1Item)
    overworld.add_event("Suburbia Cartel Cleared", "Uptown Customers Unlocked", 
                        location_type=Schedule1Location, item_type=items.Schedule1Item)
    overworld.add_event("Uptown Cartel Cleared", "Finishing The Job Mission Available", 
                        location_type=Schedule1Location, item_type=items.Schedule1Item)