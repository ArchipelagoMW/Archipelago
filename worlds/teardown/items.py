from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

import random

if TYPE_CHECKING:
    from .world import TeardownWorld

ITEM_NAME_TO_ID = {

    "Old Building Problem Unlock": 1,
    "Lee Computers Unlock": 2,
    "Login Devices Unlock": 3,
    "Making Space Unlock": 4,
    "Classic Cars Unlock": 5,
    "The GPS Devices Unlock": 6,
    "The Car Wash Unlock": 7,
    "Heavy Lifting Unlock": 8,
    "The Tower Unlock": 9,
    "Fine Arts Unlock": 10,
    "Tool Up Unlock": 11,
    "Art Return Unlock": 12,
    "Covert Chaos Unlock": 13,
    "Insurance Fraud Unlock": 14,
    "The BlueTide Computers Unlock": 15,
    "The Speed Deal Unlock": 15,
    "A Wet Affair Unlock": 16,
    "Power Outage Unlock": 17,
    "Motivational Reminder Unlock": 18,
    "An Assortment Of Dishes Unlock": 19,
    "Flooding Unlock": 20,
    "The Chase Unlock": 21,
    "Roborazzi Unlock": 22,
    "The Secret Ingredients Unlock": 23,
    "The BlueTide Shortage Unlock": 24,
    "The Shipping Logs Unlock": 25,
    "The Alarm System Unlock": 26,
    "Moving The Goods Unlock": 27,
    "Havoc In Paradise Unlock": 28,
    "Elena's Revenge Unlock": 29,
    "Truckload Of Trouble Unlock": 30,
    "Ornament Ordeal Unlock": 31,
    "The Quilez Tools Unlock": 32,
    "Connecting The Dots Unlock": 33,
    "The Pawn Shop Unlock": 34,
    "The Droid Abduction Unlock": 35,
    "Malice In Woonderland Unlock": 36,
    "Handle With Care Unlock": 37,
    "Droid Dismount Unlock": 38,
    "The Final Diversion Unlock": 39,

#   Progressive Tool Upgrades

    "Sledge Hammer Unlock": 41,
    "Spraycan Unlock": 42,
    "Extinguisher Unlock": 43,

    "Blowtorch Unlock": 51,
    "Shotgun Unlock": 52,
    "Plank Unlock": 53,
    "Pipe Unlock": 54,
    "Gun Unlock": 55,
    "Bomb Unlock": 56,
    "Rocket Launcher Unlock": 57,
    "Rocket Booster Unlock": 58,
    "Leaf Blower Unlock": 59,
    "Cable Unlock": 60,
    "Vehicle Thruster Unlock": 61,
    "Nitroglycerin Unlock": 62,
    "Hunting Rifle Unlock": 63,
    "BlueTide Unlock": 64,

    "Blowtorch Fuel Upgrade": 71,

    "Shotgun Rounds Upgrade": 81,
    "Shotgun Range Upgrade": 82,
    "Shotgun Damage Upgrade": 83,

    "Plank Amount Upgrade": 91,
    "Plank Width Upgrade": 92,
    "Plank Max Length Upgrade": 93,

    "Pipe Bomb Rounds Upgrade": 101,
    "Pipe Bomb Blast Upgrade": 102,

    "Gun Rounds Upgrade": 111,
    "Gun Range Upgrade": 112,
    "Gun Damage Upgrade": 113,

    "Bomb Rounds Upgrade": 121,
    "Bomb Blast Upgrade": 122,

    "Rocket Launcher Rounds Upgrade": 131,
    "Rocket Launcher Blast Upgrade": 132,

    "Rocket Booster Rounds Upgrade": 141,
    "Rocket Booster Power Upgrade": 142,
    "Rocket Booster Time Upgrade": 143,

    "Leaf Blower Power Upgrade": 151,

    "Cable Amount Upgrade": 161,
    "Cable Stretch Upgrade": 162,

    "Vehicle Thruster Rounds Upgrade": 171,
    "Vehicle Thruster Power Upgrade": 172,

    "Nitroglycerin Rounds Upgrade": 181,
    "Nitroglycerin Blast Upgrade": 182,

    "Hunting Rifle Rounds Upgrade": 191,

    "BlueTide Bottles Upgrade": 201,
    "BlueTide Duration Upgrade": 202,

    "Extra Nothing": 300,

}

DEFAULT_ITEM_CLASSIFICATIONS = {
    "Old Building Problem Unlock": ItemClassification.progression,
    "Lee Computers Unlock": ItemClassification.progression,
    "Login Devices Unlock": ItemClassification.progression,
    "Making Space Unlock": ItemClassification.progression,
    "Classic Cars Unlock": ItemClassification.progression,
    "The GPS Devices Unlock": ItemClassification.progression,
    "The Car Wash Unlock": ItemClassification.progression,
    "Heavy Lifting Unlock": ItemClassification.progression,
    "The Tower Unlock": ItemClassification.progression,
    "Fine Arts Unlock": ItemClassification.progression,
    "Tool Up Unlock": ItemClassification.progression,
    "Art Return Unlock": ItemClassification.progression,
    "Covert Chaos Unlock": ItemClassification.progression,
    "Insurance Fraud Unlock": ItemClassification.progression,
    "The BlueTide Computers Unlock": ItemClassification.progression,
    "The Speed Deal Unlock": ItemClassification.progression,
    "A Wet Affair Unlock": ItemClassification.progression,
    "Power Outage Unlock": ItemClassification.progression,
    "Motivational Reminder Unlock": ItemClassification.progression,
    "An Assortment Of Dishes Unlock": ItemClassification.progression,
    "Flooding Unlock": ItemClassification.progression,
    "The Chase Unlock": ItemClassification.progression,
    "Roborazzi Unlock": ItemClassification.progression,
    "The Secret Ingredients Unlock": ItemClassification.progression,
    "The BlueTide Shortage Unlock": ItemClassification.progression,
    "The Shipping Logs Unlock": ItemClassification.progression,
    "The Alarm System Unlock": ItemClassification.progression,
    "Moving The Goods Unlock": ItemClassification.progression,
    "Havoc In Paradise Unlock": ItemClassification.progression,
    "Elena's Revenge Unlock": ItemClassification.progression,
    "Truckload Of Trouble Unlock": ItemClassification.progression,
    "Ornament Ordeal Unlock": ItemClassification.progression,
    "The Quilez Tools Unlock": ItemClassification.progression,
    "Connecting The Dots Unlock": ItemClassification.progression,
    "The Pawn Shop Unlock": ItemClassification.progression,
    "The Droid Abduction Unlock": ItemClassification.progression,
    "Malice In Woonderland Unlock": ItemClassification.progression,
    "Handle With Care Unlock": ItemClassification.progression,
    "Droid Dismount Unlock": ItemClassification.progression,
    "The Final Diversion Unlock": ItemClassification.progression,

    "Sledge Hammer Unlock": ItemClassification.progression,
    "Spraycan Unlock": ItemClassification.useful,
    "Extinguisher Unlock": ItemClassification.progression,

    "Blowtorch Unlock": ItemClassification.progression,
    "Shotgun Unlock": ItemClassification.progression,
    "Plank Unlock": ItemClassification.progression,
    "Pipe Unlock": ItemClassification.progression,
    "Gun Unlock": ItemClassification.progression,
    "Bomb Unlock": ItemClassification.progression,
    "Rocket Launcher Unlock": ItemClassification.progression,
    "Rocket Booster Unlock": ItemClassification.progression,
    "Leaf Blower Unlock": ItemClassification.progression,
    "Cable Unlock": ItemClassification.progression,
    "Vehicle Thruster Unlock": ItemClassification.progression,
    "Nitroglycerin Unlock": ItemClassification.progression,
    "Hunting Rifle Unlock": ItemClassification.progression,
    "BlueTide Unlock": ItemClassification.progression,

    "Blowtorch Fuel Upgrade": ItemClassification.progression| ItemClassification.useful,

    "Shotgun Rounds Upgrade": ItemClassification.progression| ItemClassification.useful,
    "Shotgun Range Upgrade": ItemClassification.progression| ItemClassification.useful,
    "Shotgun Damage Upgrade": ItemClassification.progression| ItemClassification.useful,

    "Plank Amount Upgrade": ItemClassification.progression| ItemClassification.useful,
    "Plank Width Upgrade": ItemClassification.progression| ItemClassification.useful,
    "Plank Max Length Upgrade": ItemClassification.progression| ItemClassification.useful,

    "Pipe Bomb Rounds Upgrade": ItemClassification.progression| ItemClassification.useful,
    "Pipe Bomb Blast Upgrade": ItemClassification.progression| ItemClassification.useful,

    "Gun Rounds Upgrade": ItemClassification.progression| ItemClassification.useful,
    "Gun Range Upgrade": ItemClassification.progression| ItemClassification.useful,
    "Gun Damage Upgrade": ItemClassification.progression| ItemClassification.useful,

    "Bomb Rounds Upgrade": ItemClassification.progression| ItemClassification.useful,
    "Bomb Blast Upgrade": ItemClassification.progression| ItemClassification.useful,

    "Rocket Launcher Rounds Upgrade": ItemClassification.progression| ItemClassification.useful,
    "Rocket Launcher Blast Upgrade": ItemClassification.progression| ItemClassification.useful,

    "Rocket Booster Rounds Upgrade": ItemClassification.progression| ItemClassification.useful,
    "Rocket Booster Power Upgrade": ItemClassification.progression| ItemClassification.useful,
    "Rocket Booster Time Upgrade": ItemClassification.progression| ItemClassification.useful,

    "Leaf Blower Power Upgrade": ItemClassification.progression| ItemClassification.useful,

    "Cable Amount Upgrade": ItemClassification.progression| ItemClassification.useful,
    "Cable Stretch Upgrade": ItemClassification.progression| ItemClassification.useful,

    "Vehicle Thruster Rounds Upgrade": ItemClassification.progression| ItemClassification.useful,
    "Vehicle Thruster Power Upgrade": ItemClassification.progression| ItemClassification.useful,

    "Nitroglycerin Rounds Upgrade": ItemClassification.progression| ItemClassification.useful,
    "Nitroglycerin Blast Upgrade": ItemClassification.progression| ItemClassification.useful,

    "Hunting Rifle Rounds Upgrade": ItemClassification.progression| ItemClassification.useful,

    "BlueTide Bottles Upgrade": ItemClassification.progression| ItemClassification.useful,
    "BlueTide Duration Upgrade": ItemClassification.progression| ItemClassification.useful,

    "Extra Nothing": ItemClassification.filler,
}

item_name_groups = {
    "levels": [
        "Old Building Problem Unlock",
        "Lee Computers Unlock",
        "Login Devices Unlock",
        "Making Space Unlock",
        "Classic Cars Unlock",
        "The GPS Devices Unlock",
        "The Car Wash Unlock",
        "Heavy Lifting Unlock",
        "The Tower Unlock",
        "Fine Arts Unlock",
        "Tool Up Unlock",
        "Art Return Unlock",
        "Covert Chaos Unlock",
        "Insurance Fraud Unlock",
        "The BlueTide Computers Unlock",
        "The Speed Deal Unlock",
        "A Wet Affair Unlock",
        "Power Outage Unlock",
        "Motivational Reminder Unlock",
        "An Assortment Of Dishes Unlock",
        "Flooding Unlock",
        "The Chase Unlock",
        "Roborazzi Unlock",
        "The Secret Ingredients Unlock",
        "The BlueTide Shortage Unlock",
        "The Shipping Logs Unlock",
        "The Alarm System Unlock",
        "Moving The Goods Unlock",
        "Havoc In Paradise Unlock",
        "Elena's Revenge Unlock",
        "Truckload Of Trouble Unlock",
        "Ornament Ordeal Unlock",
        "The Quilez Tools Unlock",
        "Connecting The Dots Unlock",
        "The Pawn Shop Unlock",
        "The Droid Abduction Unlock",
        "Malice In Woonderland Unlock",
        "Handle With Care Unlock",
        "Droid Dismount Unlock",
    ],
}


class TeardownItem(Item):
    game = "Teardown"


def get_random_filler_item_name(world: TeardownWorld) -> str:
    return "Extra Nothing"

def create_item_with_correct_classification(world: TeardownWorld, name: str) -> TeardownItem:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]
    if name == "Elena's Revenge Unlock":
        classification = ItemClassification.progression

    return TeardownItem(name, classification, ITEM_NAME_TO_ID[name], world.player)


def create_all_items(world: TeardownWorld) -> None:
    itempool: list[Item] = [
        world.create_item("Blowtorch Fuel Upgrade"),
        world.create_item("Blowtorch Fuel Upgrade"),
        world.create_item("Blowtorch Fuel Upgrade"),
        world.create_item("Blowtorch Fuel Upgrade"),

        world.create_item("Shotgun Rounds Upgrade"),
        world.create_item("Shotgun Rounds Upgrade"),
        world.create_item("Shotgun Rounds Upgrade"),
        world.create_item("Shotgun Rounds Upgrade"),
        world.create_item("Shotgun Rounds Upgrade"),
        world.create_item("Shotgun Rounds Upgrade"),
        world.create_item("Shotgun Rounds Upgrade"),

        world.create_item("Shotgun Range Upgrade"),
        world.create_item("Shotgun Range Upgrade"),

        world.create_item("Shotgun Damage Upgrade"),
        world.create_item("Shotgun Damage Upgrade"),

        world.create_item("Plank Amount Upgrade"),
        world.create_item("Plank Amount Upgrade"),
        world.create_item("Plank Amount Upgrade"),
        world.create_item("Plank Amount Upgrade"),
        world.create_item("Plank Amount Upgrade"),
        world.create_item("Plank Amount Upgrade"),
        world.create_item("Plank Amount Upgrade"),

        world.create_item("Plank Width Upgrade"),
        world.create_item("Plank Width Upgrade"),

        world.create_item("Plank Max Length Upgrade"),
        world.create_item("Plank Max Length Upgrade"),
        world.create_item("Plank Max Length Upgrade"),

        world.create_item("Pipe Bomb Rounds Upgrade"),
        world.create_item("Pipe Bomb Rounds Upgrade"),
        world.create_item("Pipe Bomb Rounds Upgrade"),
        world.create_item("Pipe Bomb Rounds Upgrade"),
        world.create_item("Pipe Bomb Rounds Upgrade"),

        world.create_item("Pipe Bomb Blast Upgrade"),
        world.create_item("Pipe Bomb Blast Upgrade"),

        world.create_item("Gun Rounds Upgrade"),
        world.create_item("Gun Rounds Upgrade"),
        world.create_item("Gun Rounds Upgrade"),
        world.create_item("Gun Rounds Upgrade"),
        world.create_item("Gun Rounds Upgrade"),

        world.create_item("Gun Range Upgrade"),
        world.create_item("Gun Range Upgrade"),
        world.create_item("Gun Range Upgrade"),

        world.create_item("Gun Damage Upgrade"),
        world.create_item("Gun Damage Upgrade"),

        world.create_item("Bomb Rounds Upgrade"),
        world.create_item("Bomb Rounds Upgrade"),
        world.create_item("Bomb Rounds Upgrade"),
        world.create_item("Bomb Rounds Upgrade"),
        world.create_item("Bomb Rounds Upgrade"),

        world.create_item("Bomb Blast Upgrade"),
        world.create_item("Bomb Blast Upgrade"),

        world.create_item("Rocket Launcher Rounds Upgrade"),
        world.create_item("Rocket Launcher Rounds Upgrade"),
        world.create_item("Rocket Launcher Rounds Upgrade"),

        world.create_item("Rocket Launcher Blast Upgrade"),
        world.create_item("Rocket Launcher Blast Upgrade"),

        world.create_item("Rocket Booster Rounds Upgrade"),
        world.create_item("Rocket Booster Rounds Upgrade"),
        world.create_item("Rocket Booster Rounds Upgrade"),

        world.create_item("Rocket Booster Power Upgrade"),
        world.create_item("Rocket Booster Power Upgrade"),

        world.create_item("Rocket Booster Time Upgrade"),
        world.create_item("Rocket Booster Time Upgrade"),

        world.create_item("Leaf Blower Power Upgrade"),
        world.create_item("Leaf Blower Power Upgrade"),
        world.create_item("Leaf Blower Power Upgrade"),

        world.create_item("Cable Amount Upgrade"),
        world.create_item("Cable Amount Upgrade"),
        world.create_item("Cable Amount Upgrade"),

        world.create_item("Cable Stretch Upgrade"),
        world.create_item("Cable Stretch Upgrade"),

        world.create_item("Vehicle Thruster Rounds Upgrade"),
        world.create_item("Vehicle Thruster Rounds Upgrade"),
        world.create_item("Vehicle Thruster Rounds Upgrade"),

        world.create_item("Vehicle Thruster Power Upgrade"),
        world.create_item("Vehicle Thruster Power Upgrade"),

        world.create_item("Nitroglycerin Rounds Upgrade"),
        world.create_item("Nitroglycerin Rounds Upgrade"),
        world.create_item("Nitroglycerin Rounds Upgrade"),

        world.create_item("Nitroglycerin Blast Upgrade"),
        world.create_item("Nitroglycerin Blast Upgrade"),
        world.create_item("Nitroglycerin Blast Upgrade"),

        world.create_item("Hunting Rifle Rounds Upgrade"),
        world.create_item("Hunting Rifle Rounds Upgrade"),

        world.create_item("BlueTide Bottles Upgrade"),
        world.create_item("BlueTide Bottles Upgrade"),

        world.create_item("BlueTide Duration Upgrade"),
        world.create_item("BlueTide Duration Upgrade"),

        world.create_item("Extra Nothing"),
    ]






    if world.options.StartingTool:
        itempool.append(world.create_item("Sledge Hammer Unlock"))
        itempool.append(world.create_item("Spraycan Unlock"))
        itempool.append(world.create_item("Extinguisher Unlock"))

    else:
        world.push_precollected(world.create_item("Sledge Hammer Unlock"))
        world.push_precollected(world.create_item("Spraycan Unlock"))
        world.push_precollected(world.create_item("Extinguisher Unlock"))


    if world.options.StartingLevel:
        predeterminedlevel = world.random.choice(item_name_groups["levels"])
        nonstartinglevel = [lvl for lvl in (item_name_groups["levels"]) if lvl != predeterminedlevel]
        world.push_precollected(world.create_item(predeterminedlevel))

        itempool.append(world.create_item(nonstartinglevel[0]))
        itempool.append(world.create_item(nonstartinglevel[1]))
        itempool.append(world.create_item(nonstartinglevel[2]))
        itempool.append(world.create_item(nonstartinglevel[3]))
        itempool.append(world.create_item(nonstartinglevel[4]))
        itempool.append(world.create_item(nonstartinglevel[5]))
        itempool.append(world.create_item(nonstartinglevel[6]))
        itempool.append(world.create_item(nonstartinglevel[7]))
        itempool.append(world.create_item(nonstartinglevel[8]))
        itempool.append(world.create_item(nonstartinglevel[9]))
        itempool.append(world.create_item(nonstartinglevel[10]))
        itempool.append(world.create_item(nonstartinglevel[11]))
        itempool.append(world.create_item(nonstartinglevel[12]))
        itempool.append(world.create_item(nonstartinglevel[13]))
        itempool.append(world.create_item(nonstartinglevel[14]))
        itempool.append(world.create_item(nonstartinglevel[15]))
        itempool.append(world.create_item(nonstartinglevel[16]))
        itempool.append(world.create_item(nonstartinglevel[17]))
        itempool.append(world.create_item(nonstartinglevel[18]))
        itempool.append(world.create_item(nonstartinglevel[19]))
        itempool.append(world.create_item(nonstartinglevel[20]))
        itempool.append(world.create_item(nonstartinglevel[21]))
        itempool.append(world.create_item(nonstartinglevel[22]))
        itempool.append(world.create_item(nonstartinglevel[23]))
        itempool.append(world.create_item(nonstartinglevel[24]))
        itempool.append(world.create_item(nonstartinglevel[25]))
        itempool.append(world.create_item(nonstartinglevel[26]))
        itempool.append(world.create_item(nonstartinglevel[27]))
        itempool.append(world.create_item(nonstartinglevel[28]))
        itempool.append(world.create_item(nonstartinglevel[29]))
        itempool.append(world.create_item(nonstartinglevel[30]))
        itempool.append(world.create_item(nonstartinglevel[31]))
        itempool.append(world.create_item(nonstartinglevel[32]))
        itempool.append(world.create_item(nonstartinglevel[33]))
        itempool.append(world.create_item(nonstartinglevel[34]))
        itempool.append(world.create_item(nonstartinglevel[35]))
        itempool.append(world.create_item(nonstartinglevel[36]))
        itempool.append(world.create_item(nonstartinglevel[37]))


    else:
        world.push_precollected(world.create_item("Old Building Problem Unlock"))

        itempool.append(world.create_item("Lee Computers Unlock"))
        itempool.append(world.create_item("Login Devices Unlock"))
        itempool.append(world.create_item("Making Space Unlock"))
        itempool.append(world.create_item("Classic Cars Unlock"))
        itempool.append(world.create_item("The GPS Devices Unlock"))
        itempool.append(world.create_item("The Car Wash Unlock"))
        itempool.append(world.create_item("Heavy Lifting Unlock"))
        itempool.append(world.create_item("The Tower Unlock"))
        itempool.append(world.create_item("Fine Arts Unlock"))
        itempool.append(world.create_item("Tool Up Unlock"))
        itempool.append(world.create_item("Art Return Unlock"))
        itempool.append(world.create_item("Covert Chaos Unlock"))
        itempool.append(world.create_item("Insurance Fraud Unlock"))
        itempool.append(world.create_item("The BlueTide Computers Unlock"))
        itempool.append(world.create_item("The Speed Deal Unlock"))
        itempool.append(world.create_item("A Wet Affair Unlock"))
        itempool.append(world.create_item("Power Outage Unlock"))
        itempool.append(world.create_item("Motivational Reminder Unlock"))
        itempool.append(world.create_item("An Assortment Of Dishes Unlock"))
        itempool.append(world.create_item("Flooding Unlock"))
        itempool.append(world.create_item("The Chase Unlock"))
        itempool.append(world.create_item("Roborazzi Unlock"))
        itempool.append(world.create_item("The Secret Ingredients Unlock"))
        itempool.append(world.create_item("The BlueTide Shortage Unlock"))
        itempool.append(world.create_item("The Shipping Logs Unlock"))
        itempool.append(world.create_item("The Alarm System Unlock"))
        itempool.append(world.create_item("Moving The Goods Unlock"))
        itempool.append(world.create_item("Havoc In Paradise Unlock"))
        itempool.append(world.create_item("Elena's Revenge Unlock"))
        itempool.append(world.create_item("Truckload Of Trouble Unlock"))
        itempool.append(world.create_item("Ornament Ordeal Unlock"))
        itempool.append(world.create_item("The Quilez Tools Unlock"))
        itempool.append(world.create_item("Connecting The Dots Unlock"))
        itempool.append(world.create_item("The Pawn Shop Unlock"))
        itempool.append(world.create_item("The Droid Abduction Unlock"))
        itempool.append(world.create_item("Malice In Woonderland Unlock"))
        itempool.append(world.create_item("Handle With Care Unlock"))
        itempool.append(world.create_item("Droid Dismount Unlock"))

    # The length of our itempool is easy to determine, since we have it as a list.
    number_of_items = len(itempool)

    # What we actually want is the number of *unfilled* locations. Luckily, there is a helper method for this:
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))

    # Now, we just subtract the number of items from the number of locations to get the number of empty item slots.
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    # You can just use this function directly to create as many filler items as you need to complete your itempool.
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    # This is how the generator actually knows about the existence of our items.
    world.multiworld.itempool += itempool