from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location

if TYPE_CHECKING:
    from .world import TeardownWorld

LOCATION_NAME_TO_ID = {

#   Mission Locations
    "Old Building Problem": 1,

    "Lee Computers Required 1": 11,
    "Lee Computers Required 2": 12,
    "Lee Computers Required 3": 13,

    "Login Devices Required 1": 21,
    "Login Devices Required 2": 22,
    "Login Devices Required 3": 23,

    "Making Space Required 1": 31,
    "Making Space Required 2": 32,
    "Making Space Optional 3": 33,

    "Classic Cars Required 1": 41,
    "Classic Cars Required 2": 42,
    "Classic Cars Optional 1": 43,
    "Classic Cars Optional 2": 44,

    "The GPS Devices Required 1": 51,
    "The GPS Devices Required 2": 52,
    "The GPS Devices Required 3": 53,
    "The GPS Devices Optional 1": 54,
    "The GPS Devices Optional 2": 55,

    "The Car Wash Required 1": 61,
    "The Car Wash Required 2": 62,
    "The Car Wash Required 3": 63,
    "The Car Wash Optional 1": 64,
    "The Car Wash Optional 2": 65,
    "The Car Wash Optional 3": 66,

    "Heavy Lifting Required 1": 71,
    "Heavy Lifting Optional 1": 72,
    "Heavy Lifting Optional 2": 73,
    "Heavy Lifting Optional 3": 74,
    "Heavy Lifting Optional 4": 75,

    "The Tower": 81,

    "Fine Arts Required 1": 91,
    "Fine Arts Required 2": 92,
    "Fine Arts Required 3": 94,
    "Fine Arts Required 4": 95,
    "Fine Arts Optional 1": 96,
    "Fine Arts Optional 2": 97,

    "Tool Up Required 1": 101,
    "Tool Up Required 2": 102,
    "Tool Up Required 3": 103,
    "Tool Up Required 4": 104,
    "Tool Up Optional 1": 105,
    "Tool Up Optional 2": 106,

    "Art Return Required 1": 111,
    "Art Return Required 2": 112,
    "Art Return Required 3": 113,
    "Art Return Required 4": 114,

    "Covert Chaos Required 1": 121,
    "Covert Chaos Optional 1": 122,
    "Covert Chaos Optional 2": 123,

    "Insurance Fraud Required 1": 131,
    "Insurance Fraud Required 2": 132,
    "Insurance Fraud Required 3": 133,
    "Insurance Fraud Optional 1": 134,
    "Insurance Fraud Optional 2": 135,
    "Insurance Fraud Optional 3": 136,

    "The BlueTide Computers Required 1": 141,
    "The BlueTide Computers Required 2": 142,
    "The BlueTide Computers Required 3": 143,
    "The BlueTide Computers Required 4": 144,
    "The BlueTide Computers Optional 1": 145,
    "The BlueTide Computers Optional 2": 146,
    "The BlueTide Computers Optional 3": 147,

    "The Speed Deal Required 1": 151,
    "The Speed Deal Optional 1": 152,
    "The Speed Deal Optional 2": 153,

    "A Wet Affair Required 1": 161,
    "A Wet Affair Required 2": 162,
    "A Wet Affair Required 3": 163,
    "A Wet Affair Optional 1": 164,
    "A Wet Affair Optional 2": 165,
    "A Wet Affair Optional 3": 166,

    "Power Outage Required 1": 171,
    "Power Outage Required 2": 172,
    "Power Outage Required 3": 173,
    "Power Outage Required 4": 174,
    "Power Outage Optional 1": 175,
    "Power Outage Optional 2": 176,
    "Power Outage Optional 3": 177,
    "Power Outage Optional 4": 178,

    "Motivational Reminder Required 1": 181,
    "Motivational Reminder Required 2": 182,
    "Motivational Reminder Required 3": 183,
    "Motivational Reminder Required 4": 184,
    "Motivational Reminder Required 5": 185,
    "Motivational Reminder Optional 1": 186,
    "Motivational Reminder Optional 2": 187,
    "Motivational Reminder Optional 3": 188,

    "An Assortment Of Dishes Required 1": 191,
    "An Assortment Of Dishes Required 2": 192,
    "An Assortment Of Dishes Required 3": 193,
    "An Assortment Of Dishes Required 4": 194,
    "An Assortment Of Dishes Required 5": 195,
    "An Assortment Of Dishes Optional 1": 196,
    "An Assortment Of Dishes Optional 2": 197,
    "An Assortment Of Dishes Optional 3": 198,
    "An Assortment Of Dishes Optional 4": 199,

    "Flooding Required 1": 201,
    "Flooding Required 2": 202,
    "Flooding Required 3": 203,
    "Flooding Required 4": 204,
    "Flooding Required 5": 205,
    "Flooding Optional 1": 206,
    "Flooding Optional 2": 207,
    "Flooding Optional 3": 208,

    "The Chase": 211,

    "Roborazzi Required 1": 221,
    "Roborazzi Required 2": 222,
    "Roborazzi Required 3": 223,
    "Roborazzi Required 4": 224,
    "Roborazzi Required 5": 225,

    "The Secret Ingredients Required 1": 231,
    "The Secret Ingredients Required 2": 232,
    "The Secret Ingredients Required 3": 233,
    "The Secret Ingredients Required 4": 234,
    "The Secret Ingredients Optional 1": 235,
    "The Secret Ingredients Optional 2": 236,

    "The BlueTide Shortage Required 1": 241,
    "The BlueTide Shortage Required 2": 242,
    "The BlueTide Shortage Required 3": 243,
    "The BlueTide Shortage Optional 1": 244,
    "The BlueTide Shortage Optional 2": 245,
    "The BlueTide Shortage Optional 3": 246,

    "The Shipping Logs Required 1": 251,
    "The Shipping Logs Required 2": 252,
    "The Shipping Logs Required 3": 253,
    "The Shipping Logs Required 4": 254,
    "The Shipping Logs Required 5": 255,
    "The Shipping Logs Optional 1": 256,
    "The Shipping Logs Optional 2": 257,
    "The Shipping Logs Optional 3": 258,

    "The Alarm System Required 1": 261,
    "The Alarm System Required 2": 262,
    "The Alarm System Required 3": 263,
    "The Alarm System Required 4": 264,
    "The Alarm System Optional 1": 265,
    "The Alarm System Optional 2": 266,

    "Moving The Goods Required 1": 271,
    "Moving The Goods Required 2": 272,
    "Moving The Goods Required 3": 273,
    "Moving The Goods Optional 1": 274,
    "Moving The Goods Optional 2": 275,

    "Havoc In Paradise Required 1": 281,
    "Havoc In Paradise Required 2": 282,
    "Havoc In Paradise Required 3": 283,
    "Havoc In Paradise Required 4": 284,
    "Havoc In Paradise Optional 1": 285,
    "Havoc In Paradise Optional 2": 286,
    "Havoc In Paradise Optional 3": 287,

    "Elena's Revenge": 291,

    "Truckload Of Trouble Required 1": 301,
    "Truckload Of Trouble Required 2": 302,
    "Truckload Of Trouble Optional 1": 303,

    "Ornament Ordeal Required 1": 311,
    "Ornament Ordeal Required 2": 312,
    "Ornament Ordeal Required 3": 313,
    "Ornament Ordeal Required 4": 314,
    "Ornament Ordeal Optional 1": 315,
    "Ornament Ordeal Optional 2": 316,

    "The Quilez Tools Required 1": 321,
    "The Quilez Tools Required 2": 322,
    "The Quilez Tools Required 3": 323,
    "The Quilez Tools Required 4": 324,
    "The Quilez Tools Optional 1": 325,
    "The Quilez Tools Optional 2": 326,

    "Connecting The Dots Required 1": 331,
    "Connecting The Dots Required 2": 332,
    "Connecting The Dots Required 3": 333,
    "Connecting The Dots Optional 1": 334,
    "Connecting The Dots Optional 2": 335,

    "The Pawn Shop Required 1": 341,
    "The Pawn Shop Required 2": 342,
    "The Pawn Shop Required 3": 343,
    "The Pawn Shop Required 4": 344,
    "The Pawn Shop Required 5": 345,
    "The Pawn Shop Optional 1": 346,
    "The Pawn Shop Optional 2": 347,

    "The Droid Abduction Required 1": 351,
    "The Droid Abduction Optional 1": 352,
    "The Droid Abduction Optional 2": 353,
    "The Droid Abduction Optional 3": 354,

    "Malice In Woonderland Required 1": 361,
    "Malice In Woonderland Required 2": 362,
    "Malice In Woonderland Required 3": 363,
    "Malice In Woonderland Required 4": 364,
    "Malice In Woonderland Required 5": 365,
    "Malice In Woonderland Optional 1": 366,
    "Malice In Woonderland Optional 2": 367,
    "Malice In Woonderland Optional 3": 368,

    "Handle With Care Required 1": 371,
    "Handle With Care Required 2": 372,
    "Handle With Care Required 3": 373,
    "Handle With Care Optional 1": 374,
    "Handle With Care Optional 2": 375,
    "Handle With Care Optional 3": 376,
    "Handle With Care Optional 4": 377,

    "Droid Dismount Required 1": 381,
    "Droid Dismount Required 2": 382,
    "Droid Dismount Required 3": 383,
    "Droid Dismount Required 4": 384,
    "Droid Dismount Required 5": 385,
    "Droid Dismount Optional 1": 386,
    "Droid Dismount Optional 2": 387,

    "The Final Diversion": 393,

#   Upgrade Locations

    "Blowtorch Fuel Upgrade 1": 501,
    "Blowtorch Fuel Upgrade 2": 502,
    "Blowtorch Fuel Upgrade 3": 503,
    "Blowtorch Fuel Upgrade 4": 504,

    "Shotgun Rounds Upgrade 1": 511,
    "Shotgun Rounds Upgrade 2": 512,
    "Shotgun Rounds Upgrade 3": 513,
    "Shotgun Rounds Upgrade 4": 514,
    "Shotgun Rounds Upgrade 5": 515,
    "Shotgun Rounds Upgrade 6": 516,
    "Shotgun Rounds Upgrade 7": 517,

    "Shotgun Range Upgrade 1": 521,
    "Shotgun Range Upgrade 2": 522,

    "Shotgun Damage Upgrade 1": 531,
    "Shotgun Damage Upgrade 2": 532,

    "Plank Amount Upgrade 1": 541,
    "Plank Amount Upgrade 2": 542,
    "Plank Amount Upgrade 3": 543,
    "Plank Amount Upgrade 4": 544,
    "Plank Amount Upgrade 5": 545,
    "Plank Amount Upgrade 6": 546,
    "Plank Amount Upgrade 7": 547,

    "Plank Width Upgrade 1": 551,
    "Plank Width Upgrade 2": 552,

    "Plank Max Length Upgrade 1": 561,
    "Plank Max Length Upgrade 2": 562,
    "Plank Max Length Upgrade 3": 563,

    "Pipe Bomb Rounds Upgrade 1": 571,
    "Pipe Bomb Rounds Upgrade 2": 572,
    "Pipe Bomb Rounds Upgrade 3": 573,
    "Pipe Bomb Rounds Upgrade 4": 574,
    "Pipe Bomb Rounds Upgrade 5": 575,

    "Pipe Bomb Blast Upgrade 1": 581,
    "Pipe Bomb Blast Upgrade 2": 582,

    "Gun Rounds Upgrade 1": 591,
    "Gun Rounds Upgrade 2": 592,
    "Gun Rounds Upgrade 3": 593,
    "Gun Rounds Upgrade 4": 594,
    "Gun Rounds Upgrade 5": 595,

    "Gun Range Upgrade 1": 601,
    "Gun Range Upgrade 2": 602,
    "Gun Range Upgrade 3": 603,

    "Gun Damage Upgrade 1": 611,
    "Gun Damage Upgrade 2": 612,

    "Bomb Rounds Upgrade 1": 621,
    "Bomb Rounds Upgrade 2": 622,
    "Bomb Rounds Upgrade 3": 623,
    "Bomb Rounds Upgrade 4": 624,
    "Bomb Rounds Upgrade 5": 625,

    "Bomb Blast Upgrade 1": 631,
    "Bomb Blast Upgrade 2": 632,

    "Rocket Launcher Rounds Upgrade 1": 641,
    "Rocket Launcher Rounds Upgrade 2": 642,
    "Rocket Launcher Rounds Upgrade 3": 643,

    "Rocket Launcher Blast Upgrade 1": 651,
    "Rocket Launcher Blast Upgrade 2": 652,

    "Rocket Booster Rounds Upgrade 1": 661,
    "Rocket Booster Rounds Upgrade 2": 662,
    "Rocket Booster Rounds Upgrade 3": 663,

    "Rocket Booster Power Upgrade 1": 671,
    "Rocket Booster Power Upgrade 2": 672,

    "Rocket Booster Time Upgrade 1": 681,
    "Rocket Booster Time Upgrade 2": 682,

    "Leaf Blower Power Upgrade 1": 691,
    "Leaf Blower Power Upgrade 2": 692,
    "Leaf Blower Power Upgrade 3": 693,

    "Cable Amount Upgrade 1": 701,
    "Cable Amount Upgrade 2": 702,
    "Cable Amount Upgrade 3": 703,

    "Cable Stretch Upgrade 1": 711,
    "Cable Stretch Upgrade 2": 712,

    "Vehicle Thruster Rounds Upgrade 1": 721,
    "Vehicle Thruster Rounds Upgrade 2": 722,
    "Vehicle Thruster Rounds Upgrade 3": 723,

    "Vehicle Thruster Power Upgrade 1": 731,
    "Vehicle Thruster Power Upgrade 2": 732,

    "Nitroglycerin Rounds Upgrade 1": 741,
    "Nitroglycerin Rounds Upgrade 2": 742,
    "Nitroglycerin Rounds Upgrade 3": 743,

    "Nitroglycerin Blast Upgrade 1": 751,
    "Nitroglycerin Blast Upgrade 2": 752,
    "Nitroglycerin Blast Upgrade 3": 753,

    "Hunting Rifle Rounds Upgrade 1": 761,
    "Hunting Rifle Rounds Upgrade 2": 762,

    "BlueTide Bottles Upgrade 1": 771,
    "BlueTide Bottles Upgrade 2": 772,

    "BlueTide Duration Upgrade 1": 781,
    "BlueTide Duration Upgrade 2": 782,

#   Valuable Locations

#    "... Valuable": 801,
}


class TeardownLocation(Location):
    game = "Teardown"


# Helper that helps later
def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}

# Creates all locations above
def create_all_locations(world: TeardownWorld) -> None:
    create_regular_locations(world)

def create_regular_locations(world: TeardownWorld) -> None:
    # Before we do anything, we can grab our regions we created by using world.get_region()
    oldbuildingproblem = world.get_region("Old Building Problem")
    leecomputers = world.get_region("Lee Computers")
    logindevices = world.get_region("Login Devices")
    makingspace = world.get_region("Making Space")
    classiccars = world.get_region("Classic Cars")
    gpsdevices = world.get_region("The GPS Devices")
    carwash = world.get_region("The Car Wash")
    heavylifting = world.get_region("Heavy Lifting")
    tower = world.get_region("The Tower")
    finearts = world.get_region("Fine Arts")
    toolup = world.get_region("Tool Up")
    artreturn = world.get_region("Art Return")
    covertchaos = world.get_region("Covert Chaos")
    insurancefraud = world.get_region("Insurance Fraud")
    bluetidecomputers = world.get_region("The BlueTide Computers")
    speeddeal = world.get_region("The Speed Deal")
    wetaffair = world.get_region("A Wet Affair")
    poweroutage = world.get_region("Power Outage")
    motivationalreminder = world.get_region("Motivational Reminder")
    assortmentofdishes = world.get_region("An Assortment Of Dishes")
    flooding = world.get_region("Flooding")
    chase = world.get_region("The Chase")
    roborazzi = world.get_region("Roborazzi")
    secretingredients = world.get_region("The Secret Ingredients")
    bluetideshortage = world.get_region("The BlueTide Shortage")
    shippinglogs = world.get_region("The Shipping Logs")
    alarmsystem = world.get_region("The Alarm System")
    movingthegoods = world.get_region("Moving The Goods")
    havocinparaside = world.get_region("Havoc In Paradise")
    elenasrevenge = world.get_region("Elena's Revenge")
    truckloadoftrouble = world.get_region("Truckload Of Trouble")
    ornamentordeal = world.get_region("Ornament Ordeal")
    quileztools = world.get_region("The Quilez Tools")
    connectingthedots = world.get_region("Connecting The Dots")
    pawnshop = world.get_region("The Pawn Shop")
    droidabduction = world.get_region("The Droid Abduction")
    maliceinwoonderland = world.get_region("Malice In Woonderland")
    handlewithcare = world.get_region("Handle With Care")
    droiddismount = world.get_region("Droid Dismount")
    finaldiversion = world.get_region("The Final Diversion")

    blowtorchupgrade = world.get_region("Blowtorch Upgrades")
    shotgunupgrade = world.get_region("Shotgun Upgrades")
    plankupgrade = world.get_region("Plank Upgrades")
    pipebombupgrade = world.get_region("Pipe Bomb Upgrades")
    gunupgrade = world.get_region("Gun Upgrades")
    bombupgrade = world.get_region("Bomb Upgrades")
    rocketlauncherupgrade = world.get_region("Rocket Launcher Upgrades")
    rocketboosterupgrade = world.get_region("Rocket Booster Upgrades")
    leafblowerupgrade = world.get_region("Leaf Blower Upgrades")
    cableupgrade = world.get_region("Cable Upgrades")
    vehiclethrusterupgrade = world.get_region("Vehicle Thruster Upgrades")
    nitroglycerinupgrade = world.get_region("Nitroglycerin Upgrades")
    huntingrifleupgrade = world.get_region("Hunting Rifle Upgrades")
    bluetideupgrade = world.get_region("BlueTide Upgrades")


# Sets our locations to our regions, this is easier method
    oldbuildingproblem_locations = get_location_names_with_ids(["Old Building Problem"])
    oldbuildingproblem.add_locations(oldbuildingproblem_locations, TeardownLocation)

    leecomputers_locations = get_location_names_with_ids(["Lee Computers Required 1", "Lee Computers Required 2", "Lee Computers Required 3"])
    leecomputers.add_locations(leecomputers_locations, TeardownLocation)

    logindevices_locations = get_location_names_with_ids(["Login Devices Required 1", "Login Devices Required 2", "Login Devices Required 3"])
    logindevices.add_locations(logindevices_locations, TeardownLocation)

    makingspace_locations = get_location_names_with_ids(["Making Space Required 1", "Making Space Required 2", "Making Space Optional 3"])
    makingspace.add_locations(makingspace_locations, TeardownLocation)

    classiccars_locations = get_location_names_with_ids(["Classic Cars Required 1", "Classic Cars Required 2", "Classic Cars Optional 1", "Classic Cars Optional 2"])
    classiccars.add_locations(classiccars_locations, TeardownLocation)

    gpsdevices_locations = get_location_names_with_ids(["The GPS Devices Required 1", "The GPS Devices Required 2", "The GPS Devices Required 3", "The GPS Devices Optional 1", "The GPS Devices Optional 2"])
    gpsdevices.add_locations(gpsdevices_locations, TeardownLocation)

    carwash_locations = get_location_names_with_ids(["The Car Wash Required 1", "The Car Wash Required 2", "The Car Wash Required 3", "The Car Wash Optional 1", "The Car Wash Optional 2", "The Car Wash Optional 3"])
    carwash.add_locations(carwash_locations, TeardownLocation)

    heavylifting_locations = get_location_names_with_ids(["Heavy Lifting Required 1", "Heavy Lifting Optional 1", "Heavy Lifting Optional 2", "Heavy Lifting Optional 3", "Heavy Lifting Optional 4"])
    heavylifting.add_locations(heavylifting_locations, TeardownLocation)

    tower_locations = get_location_names_with_ids(["The Tower"])
    tower.add_locations(tower_locations, TeardownLocation)

    finearts_locations = get_location_names_with_ids(["Fine Arts Required 1", "Fine Arts Required 2", "Fine Arts Required 3", "Fine Arts Required 4", "Fine Arts Optional 1", "Fine Arts Optional 2"])
    finearts.add_locations(finearts_locations, TeardownLocation)

    toolup_locations = get_location_names_with_ids(["Tool Up Required 1", "Tool Up Required 2", "Tool Up Required 3", "Tool Up Required 4", "Tool Up Optional 1", "Tool Up Optional 2"])
    toolup.add_locations(toolup_locations, TeardownLocation)

    artreturn_locations = get_location_names_with_ids(["Art Return Required 1", "Art Return Required 2", "Art Return Required 3", "Art Return Required 4"])
    artreturn.add_locations(artreturn_locations, TeardownLocation)

    covertchaos_locations = get_location_names_with_ids(["Covert Chaos Required 1", "Covert Chaos Optional 1", "Covert Chaos Optional 2"])
    covertchaos.add_locations(covertchaos_locations, TeardownLocation)

    insurancefraud_locations = get_location_names_with_ids(["Insurance Fraud Required 1", "Insurance Fraud Required 2", "Insurance Fraud Required 3", "Insurance Fraud Optional 1", "Insurance Fraud Optional 2", "Insurance Fraud Optional 3"])
    insurancefraud.add_locations(insurancefraud_locations, TeardownLocation)

    bluetidecomputers_locations = get_location_names_with_ids(["The BlueTide Computers Required 1", "The BlueTide Computers Required 2", "The BlueTide Computers Required 3", "The BlueTide Computers Required 4", "The BlueTide Computers Optional 1", "The BlueTide Computers Optional 2", "The BlueTide Computers Optional 3"])
    bluetidecomputers.add_locations(bluetidecomputers_locations, TeardownLocation)

    speeddeal_locations = get_location_names_with_ids(["The Speed Deal Required 1", "The Speed Deal Optional 1", "The Speed Deal Optional 2"])
    speeddeal.add_locations(speeddeal_locations, TeardownLocation)

    wetaffair_locations = get_location_names_with_ids(["A Wet Affair Required 1", "A Wet Affair Required 2", "A Wet Affair Required 3", "A Wet Affair Optional 1", "A Wet Affair Optional 2", "A Wet Affair Optional 3"])
    wetaffair.add_locations(wetaffair_locations, TeardownLocation)

    poweroutage_locations = get_location_names_with_ids(["Power Outage Required 1", "Power Outage Required 2", "Power Outage Required 3", "Power Outage Required 4", "Power Outage Optional 1", "Power Outage Optional 2", "Power Outage Optional 3", "Power Outage Optional 4"])
    poweroutage.add_locations(poweroutage_locations, TeardownLocation)

    motivationalreminder_locations = get_location_names_with_ids(["Motivational Reminder Required 1", "Motivational Reminder Required 2", "Motivational Reminder Required 3", "Motivational Reminder Required 4", "Motivational Reminder Required 5", "Motivational Reminder Optional 1", "Motivational Reminder Optional 2", "Motivational Reminder Optional 3"])
    motivationalreminder.add_locations(motivationalreminder_locations, TeardownLocation)

    assortmentofdishes_locations = get_location_names_with_ids(["An Assortment Of Dishes Required 1", "An Assortment Of Dishes Required 2", "An Assortment Of Dishes Required 3", "An Assortment Of Dishes Required 4", "An Assortment Of Dishes Required 5", "An Assortment Of Dishes Optional 1", "An Assortment Of Dishes Optional 2", "An Assortment Of Dishes Optional 3", "An Assortment Of Dishes Optional 4"])
    assortmentofdishes.add_locations(assortmentofdishes_locations, TeardownLocation)

    flooding_locations = get_location_names_with_ids(["Flooding Required 1", "Flooding Required 2", "Flooding Required 3", "Flooding Required 4", "Flooding Required 5", "Flooding Optional 1", "Flooding Optional 2", "Flooding Optional 3"])
    flooding.add_locations(flooding_locations, TeardownLocation)

    chase_locations = get_location_names_with_ids(["The Chase"])
    chase.add_locations(chase_locations, TeardownLocation)

    roborazzi_locations = get_location_names_with_ids(["Roborazzi Required 1", "Roborazzi Required 2", "Roborazzi Required 3", "Roborazzi Required 4", "Roborazzi Required 5"])
    roborazzi.add_locations(roborazzi_locations, TeardownLocation)

    secretingredients_locations = get_location_names_with_ids(["The Secret Ingredients Required 1", "The Secret Ingredients Required 2", "The Secret Ingredients Required 3", "The Secret Ingredients Required 4", "The Secret Ingredients Optional 1", "The Secret Ingredients Optional 2"])
    secretingredients.add_locations(secretingredients_locations, TeardownLocation)

    bluetideshortage_locations = get_location_names_with_ids(["The BlueTide Shortage Required 1", "The BlueTide Shortage Required 2", "The BlueTide Shortage Required 3", "The BlueTide Shortage Optional 1", "The BlueTide Shortage Optional 2", "The BlueTide Shortage Optional 3"])
    bluetideshortage.add_locations(bluetideshortage_locations, TeardownLocation)

    shippinglogs_locations = get_location_names_with_ids(["The Shipping Logs Required 1", "The Shipping Logs Required 2", "The Shipping Logs Required 3", "The Shipping Logs Required 4", "The Shipping Logs Required 5", "The Shipping Logs Optional 1", "The Shipping Logs Optional 2", "The Shipping Logs Optional 3"])
    shippinglogs.add_locations(shippinglogs_locations, TeardownLocation)

    alarmsystem_locations = get_location_names_with_ids(["The Alarm System Required 1", "The Alarm System Required 2", "The Alarm System Required 3", "The Alarm System Required 4", "The Alarm System Optional 1", "The Alarm System Optional 2"])
    alarmsystem.add_locations(alarmsystem_locations, TeardownLocation)

    movingthegoods_locations = get_location_names_with_ids(["Moving The Goods Required 1", "Moving The Goods Required 2", "Moving The Goods Required 3", "Moving The Goods Optional 1", "Moving The Goods Optional 2"])
    movingthegoods.add_locations(movingthegoods_locations, TeardownLocation)

    havocinparaside_locations = get_location_names_with_ids(["Havoc In Paradise Required 1", "Havoc In Paradise Required 2", "Havoc In Paradise Required 3", "Havoc In Paradise Required 4", "Havoc In Paradise Optional 1", "Havoc In Paradise Optional 2", "Havoc In Paradise Optional 3"])
    havocinparaside.add_locations(havocinparaside_locations, TeardownLocation)

    elenasrevenge_locations = get_location_names_with_ids(["Elena's Revenge"])
    elenasrevenge.add_locations(elenasrevenge_locations, TeardownLocation)

    truckloadoftrouble_locations = get_location_names_with_ids(["Truckload Of Trouble Required 1", "Truckload Of Trouble Required 2", "Truckload Of Trouble Optional 1"])
    truckloadoftrouble.add_locations(truckloadoftrouble_locations, TeardownLocation)

    ornamentordeal_locations = get_location_names_with_ids(["Ornament Ordeal Required 1", "Ornament Ordeal Required 2", "Ornament Ordeal Required 3", "Ornament Ordeal Required 4", "Ornament Ordeal Optional 1", "Ornament Ordeal Optional 2"])
    ornamentordeal.add_locations(ornamentordeal_locations, TeardownLocation)

    quileztools_locations = get_location_names_with_ids(["The Quilez Tools Required 1", "The Quilez Tools Required 2", "The Quilez Tools Required 3", "The Quilez Tools Required 4", "The Quilez Tools Optional 1", "The Quilez Tools Optional 2"])
    quileztools.add_locations(quileztools_locations, TeardownLocation)

    connectingthedots_locations = get_location_names_with_ids(["Connecting The Dots Required 1", "Connecting The Dots Required 2", "Connecting The Dots Required 3", "Connecting The Dots Optional 1", "Connecting The Dots Optional 2"])
    connectingthedots.add_locations(connectingthedots_locations, TeardownLocation)

    pawnshop_locations = get_location_names_with_ids(["The Pawn Shop Required 1", "The Pawn Shop Required 2", "The Pawn Shop Required 3", "The Pawn Shop Required 4", "The Pawn Shop Required 5", "The Pawn Shop Optional 1", "The Pawn Shop Optional 2"])
    pawnshop.add_locations(pawnshop_locations, TeardownLocation)

    droidabduction_locations = get_location_names_with_ids(["The Droid Abduction Required 1", "The Droid Abduction Optional 1", "The Droid Abduction Optional 2", "The Droid Abduction Optional 3"])
    droidabduction.add_locations(droidabduction_locations, TeardownLocation)

    maliceinwoonderland_locations = get_location_names_with_ids(["Malice In Woonderland Required 1", "Malice In Woonderland Required 2", "Malice In Woonderland Required 3", "Malice In Woonderland Required 4", "Malice In Woonderland Required 5", "Malice In Woonderland Optional 1", "Malice In Woonderland Optional 2", "Malice In Woonderland Optional 3"])
    maliceinwoonderland.add_locations(maliceinwoonderland_locations, TeardownLocation)

    handlewithcare_locations = get_location_names_with_ids(["Handle With Care Required 1", "Handle With Care Required 2", "Handle With Care Required 3", "Handle With Care Optional 1", "Handle With Care Optional 2", "Handle With Care Optional 3", "Handle With Care Optional 4"])
    handlewithcare.add_locations(handlewithcare_locations, TeardownLocation)

    droiddismount_locations = get_location_names_with_ids(["Droid Dismount Required 1", "Droid Dismount Required 2", "Droid Dismount Required 3", "Droid Dismount Required 4", "Droid Dismount Required 5", "Droid Dismount Optional 1", "Droid Dismount Optional 2"])
    droiddismount.add_locations(droiddismount_locations, TeardownLocation)

    finaldiversion_locations = get_location_names_with_ids(["The Final Diversion"])
    finaldiversion.add_locations(finaldiversion_locations, TeardownLocation)


    blowtorchupgrade_locations = get_location_names_with_ids([
        "Blowtorch Fuel Upgrade 1",
        "Blowtorch Fuel Upgrade 2",
        "Blowtorch Fuel Upgrade 3",
        "Blowtorch Fuel Upgrade 4"
    ])
    blowtorchupgrade.add_locations(blowtorchupgrade_locations, TeardownLocation)

    shotgunupgrade_locations = get_location_names_with_ids([
        "Shotgun Rounds Upgrade 1",
        "Shotgun Rounds Upgrade 2",
        "Shotgun Rounds Upgrade 3",
        "Shotgun Rounds Upgrade 4",
        "Shotgun Rounds Upgrade 5",
        "Shotgun Rounds Upgrade 6",
        "Shotgun Rounds Upgrade 7",
        "Shotgun Range Upgrade 1",
        "Shotgun Range Upgrade 2",
        "Shotgun Damage Upgrade 1",
        "Shotgun Damage Upgrade 2"
    ])
    shotgunupgrade.add_locations(shotgunupgrade_locations, TeardownLocation)

    plankupgrade_locations = get_location_names_with_ids([
        "Plank Amount Upgrade 1",
        "Plank Amount Upgrade 2",
        "Plank Amount Upgrade 3",
        "Plank Amount Upgrade 4",
        "Plank Amount Upgrade 5",
        "Plank Amount Upgrade 6",
        "Plank Amount Upgrade 7",
        "Plank Width Upgrade 1",
        "Plank Width Upgrade 2",
        "Plank Max Length Upgrade 1",
        "Plank Max Length Upgrade 2",
        "Plank Max Length Upgrade 3"
    ])
    plankupgrade.add_locations(plankupgrade_locations, TeardownLocation)

    pipebombupgrade_locations = get_location_names_with_ids([
        "Pipe Bomb Rounds Upgrade 1",
        "Pipe Bomb Rounds Upgrade 2",
        "Pipe Bomb Rounds Upgrade 3",
        "Pipe Bomb Rounds Upgrade 4",
        "Pipe Bomb Rounds Upgrade 5",
        "Pipe Bomb Blast Upgrade 1",
        "Pipe Bomb Blast Upgrade 2"
    ])
    pipebombupgrade.add_locations(pipebombupgrade_locations, TeardownLocation)

    gunupgrade_locations = get_location_names_with_ids([
        "Gun Rounds Upgrade 1",
        "Gun Rounds Upgrade 2",
        "Gun Rounds Upgrade 3",
        "Gun Rounds Upgrade 4",
        "Gun Rounds Upgrade 5",
        "Gun Range Upgrade 1",
        "Gun Range Upgrade 2",
        "Gun Range Upgrade 3",
        "Gun Damage Upgrade 1",
        "Gun Damage Upgrade 2"
    ])
    gunupgrade.add_locations(gunupgrade_locations, TeardownLocation)

    bombupgrade_locations = get_location_names_with_ids([
        "Bomb Rounds Upgrade 1",
        "Bomb Rounds Upgrade 2",
        "Bomb Rounds Upgrade 3",
        "Bomb Rounds Upgrade 4",
        "Bomb Rounds Upgrade 5",
        "Bomb Blast Upgrade 1",
        "Bomb Blast Upgrade 2"
    ])
    bombupgrade.add_locations(bombupgrade_locations, TeardownLocation)

    rocketlauncherupgrade_locations = get_location_names_with_ids([
        "Rocket Launcher Rounds Upgrade 1",
        "Rocket Launcher Rounds Upgrade 2",
        "Rocket Launcher Rounds Upgrade 3",
        "Rocket Launcher Blast Upgrade 1",
        "Rocket Launcher Blast Upgrade 2"
    ])
    rocketlauncherupgrade.add_locations(rocketlauncherupgrade_locations, TeardownLocation)

    rocketboosterupgrade_locations = get_location_names_with_ids([
        "Rocket Booster Rounds Upgrade 1",
        "Rocket Booster Rounds Upgrade 2",
        "Rocket Booster Rounds Upgrade 3",
        "Rocket Booster Power Upgrade 1",
        "Rocket Booster Power Upgrade 2",
        "Rocket Booster Time Upgrade 1",
        "Rocket Booster Time Upgrade 2"
    ])
    rocketboosterupgrade.add_locations(rocketboosterupgrade_locations, TeardownLocation)

    leafblowerupgrade_locations = get_location_names_with_ids([
        "Leaf Blower Power Upgrade 1",
        "Leaf Blower Power Upgrade 2",
        "Leaf Blower Power Upgrade 3"
    ])
    leafblowerupgrade.add_locations(leafblowerupgrade_locations, TeardownLocation)

    cableupgrade_locations = get_location_names_with_ids([
        "Cable Amount Upgrade 1",
        "Cable Amount Upgrade 2",
        "Cable Amount Upgrade 3",
        "Cable Stretch Upgrade 1",
        "Cable Stretch Upgrade 2"
    ])
    cableupgrade.add_locations(cableupgrade_locations, TeardownLocation)

    vehiclethrusterupgrade_locations = get_location_names_with_ids([
        "Vehicle Thruster Rounds Upgrade 1",
        "Vehicle Thruster Rounds Upgrade 2",
        "Vehicle Thruster Rounds Upgrade 3",
        "Vehicle Thruster Power Upgrade 1",
        "Vehicle Thruster Power Upgrade 2"
    ])
    vehiclethrusterupgrade.add_locations(vehiclethrusterupgrade_locations, TeardownLocation)

    nitroglycerinupgrade_locations = get_location_names_with_ids([
        "Nitroglycerin Rounds Upgrade 1",
        "Nitroglycerin Rounds Upgrade 2",
        "Nitroglycerin Rounds Upgrade 3",
        "Nitroglycerin Blast Upgrade 1",
        "Nitroglycerin Blast Upgrade 2",
        "Nitroglycerin Blast Upgrade 3"
    ])
    nitroglycerinupgrade.add_locations(nitroglycerinupgrade_locations, TeardownLocation)

    huntingrifleupgrade_locations = get_location_names_with_ids([
        "Hunting Rifle Rounds Upgrade 1",
        "Hunting Rifle Rounds Upgrade 2"
    ])
    huntingrifleupgrade.add_locations(huntingrifleupgrade_locations, TeardownLocation)

    bluetideupgrade_locations = get_location_names_with_ids([
        "BlueTide Bottles Upgrade 1",
        "BlueTide Bottles Upgrade 2",
        "BlueTide Duration Upgrade 1",
        "BlueTide Duration Upgrade 2"
    ])
    bluetideupgrade.add_locations(bluetideupgrade_locations, TeardownLocation)



    # Locations may be in different regions depending on the player's options.
    #bonus_level_4_locations = get_location_names_with_ids(["Making Space 1", "Making Space 2", "Making Space 3"])
    #if world.options.Bonus_Level:
    #    bonus_level_4 = world.get_region("Bonus Level 4")
    #    bonus_level_4.add_locations(bonus_level_4_locations, TeardownLocation)

# If bonus level is enabled, create locations and add them to bonus level 4
    #if world.options.Bonus_Level:
    #    making_space = get_location_names_with_ids(["Making Space 1", "Making Space 2", "Making Space 3"])
    #    bonus_level_4.add_locations(making_space, TeardownLocation)
