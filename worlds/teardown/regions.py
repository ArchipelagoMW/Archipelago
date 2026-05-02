from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import TeardownWorld


#Done

def create_and_connect_regions(world: TeardownWorld) -> None:
    create_all_regions(world)
    connect_regions(world)

# Creates all regions
def create_all_regions(world: TeardownWorld) -> None:
    menu = Region("Main Menu", world.player, world.multiworld)
    oldbuildingproblem = Region("Old Building Problem", world.player, world.multiworld)
    leecomputers = Region("Lee Computers", world.player, world.multiworld)
    logindevices = Region("Login Devices", world.player, world.multiworld)
    makingspace = Region("Making Space", world.player, world.multiworld)
    classiccars = Region("Classic Cars", world.player, world.multiworld)
    gpsdevices = Region("The GPS Devices", world.player, world.multiworld)
    carwash = Region("The Car Wash", world.player, world.multiworld)
    heavylifting = Region("Heavy Lifting", world.player, world.multiworld)
    tower = Region("The Tower", world.player, world.multiworld)
    finearts = Region("Fine Arts", world.player, world.multiworld)
    toolup = Region("Tool Up", world.player, world.multiworld)
    artreturn = Region("Art Return", world.player, world.multiworld)
    covertchaos = Region("Covert Chaos", world.player, world.multiworld)
    insurancefraud = Region("Insurance Fraud", world.player, world.multiworld)
    bluetidecomputers = Region("The BlueTide Computers", world.player, world.multiworld)
    speeddeal = Region("The Speed Deal", world.player, world.multiworld)
    wetaffair = Region("A Wet Affair", world.player, world.multiworld)
    poweroutage = Region("Power Outage", world.player, world.multiworld)
    motivationalreminder = Region("Motivational Reminder", world.player, world.multiworld)
    assortmentofdishes = Region("An Assortment Of Dishes", world.player, world.multiworld)
    flooding = Region("Flooding", world.player, world.multiworld)
    chase = Region("The Chase", world.player, world.multiworld)
    roborazzi = Region("Roborazzi", world.player, world.multiworld)
    secretingredients = Region("The Secret Ingredients", world.player, world.multiworld)
    bluetideshortage = Region("The BlueTide Shortage", world.player, world.multiworld)
    shippinglogs = Region("The Shipping Logs", world.player, world.multiworld)
    alarmsystem = Region("The Alarm System", world.player, world.multiworld)
    movingthegoods = Region("Moving The Goods", world.player, world.multiworld)
    havocinparaside = Region("Havoc In Paradise", world.player, world.multiworld)
    elenasrevenge = Region("Elena's Revenge", world.player, world.multiworld)
    truckloadoftrouble = Region("Truckload Of Trouble", world.player, world.multiworld)
    ornamentordeal = Region("Ornament Ordeal", world.player, world.multiworld)
    quileztools = Region("The Quilez Tools", world.player, world.multiworld)
    connectingthedots = Region("Connecting The Dots", world.player, world.multiworld)
    pawnshop = Region("The Pawn Shop", world.player, world.multiworld)
    droidabduction = Region("The Droid Abduction", world.player, world.multiworld)
    maliceinwoonderland = Region("Malice In Woonderland", world.player, world.multiworld)
    handlewithcare = Region("Handle With Care", world.player, world.multiworld)
    droiddismount = Region("Droid Dismount", world.player, world.multiworld)
    finaldiversion = Region("The Final Diversion", world.player, world.multiworld)

    blowtorchupgrade = Region("Blowtorch Upgrade", world.player, world.multiworld)
    shotgunupgrade = Region("Shotgun Upgrade", world.player, world.multiworld)
    plankupgrade = Region("Plank Upgrade", world.player, world.multiworld)
    pipebombupgrade = Region("Pipe Bomb Upgrade", world.player, world.multiworld)
    gunupgrade = Region("Gun Upgrade", world.player, world.multiworld)
    bombupgrade = Region("Bomb Upgrade", world.player, world.multiworld)
    rocketlauncherupgrade = Region("Rocket Launcher Upgrade", world.player, world.multiworld)
    rocketboosterupgrade = Region("Rocket Booster Upgrade", world.player, world.multiworld)
    leafblowerupgrade = Region("Leaf Blower Upgrade", world.player, world.multiworld)
    cableupgrade = Region("Cable Upgrade", world.player, world.multiworld)
    vehiclethrusterupgrade = Region("Vehicle Thruster Upgrade", world.player, world.multiworld)
    nitroglycerinupgrade = Region("Nitroglycerin Upgrade", world.player, world.multiworld)
    huntingrifleupgrade = Region("Hunting Rifle Upgrade", world.player, world.multiworld)
    bluetideupgrade = Region("BlueTide Upgrade", world.player, world.multiworld)


# Lists all regions
    regions = [menu, oldbuildingproblem, leecomputers, logindevices, makingspace, classiccars, gpsdevices, carwash, heavylifting,
               tower, finearts, toolup, artreturn, covertchaos, insurancefraud, bluetidecomputers,speeddeal, wetaffair, poweroutage,
               motivationalreminder, assortmentofdishes, flooding, chase, roborazzi, secretingredients, bluetideshortage,
               shippinglogs, alarmsystem, movingthegoods, havocinparaside, elenasrevenge, truckloadoftrouble, ornamentordeal,
               quileztools, connectingthedots, pawnshop, droidabduction, maliceinwoonderland, handlewithcare, droiddismount,
               finaldiversion, blowtorchupgrade, shotgunupgrade, plankupgrade, pipebombupgrade, gunupgrade, bombupgrade,
               rocketlauncherupgrade, rocketboosterupgrade, leafblowerupgrade, cableupgrade, vehiclethrusterupgrade,
               nitroglycerinupgrade, huntingrifleupgrade, bluetideupgrade
               ]

# Creates region if option is enabled
#    if world.options.Bonus_Level:
#        bonus_level_4 = Region("Bonus Level 4", world.player, world.multiworld)
#        regions.append(bonus_level_4)

# Adds all regions to list
    world.multiworld.regions += regions

# Renames the objects we lost creating them
def connect_regions(world: TeardownWorld) -> None:

    menu = world.get_region("Main Menu")
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

    blowtorchupgrade = world.get_region("Blowtorch Upgrade")
    shotgunupgrade = world.get_region("Shotgun Upgrade")
    plankupgrade = world.get_region("Plank Upgrade")
    pipebombupgrade = world.get_region("Pipe Bomb Upgrade")
    gunupgrade = world.get_region("Gun Upgrade")
    bombupgrade = world.get_region("Bomb Upgrade")
    rocketlauncherupgrade = world.get_region("Rocket Launcher Upgrade")
    rocketboosterupgrade = world.get_region("Rocket Booster Upgrade")
    leafblowerupgrade = world.get_region("Leaf Blower Upgrade")
    cableupgrade = world.get_region("Cable Upgrade")
    vehiclethrusterupgrade = world.get_region("Vehicle Thruster Upgrade")
    nitroglycerinupgrade = world.get_region("Nitroglycerin Upgrade")
    huntingrifleupgrade = world.get_region("Hunting Rifle Upgrade")
    bluetideupgrade = world.get_region("BlueTide Upgrade")


# Connects the regions
    menu.connect(oldbuildingproblem, "Main Menu to Old Building Problem")
    menu.connect(leecomputers, "Main Menu to Lee Computers")
    menu.connect(logindevices, "Main Menu to Login Devices")
    menu.connect(makingspace, "Main Menu to Making Space")
    menu.connect(classiccars, "Main Menu to Classic Cars")
    menu.connect(gpsdevices, "Main Menu to The GPS Devices")
    menu.connect(carwash, "Main Menu to The Car Wash")
    menu.connect(heavylifting, "Main Menu to Heavy Lifting")
    menu.connect(tower, "Main Menu to The Tower")
    menu.connect(finearts, "Main Menu to Fine Arts")
    menu.connect(toolup, "Main Menu to Tool Up")
    menu.connect(artreturn, "Main Menu to Art Return")
    menu.connect(covertchaos, "Main Menu to Covert Chaos")
    menu.connect(insurancefraud, "Main Menu to Insurance Fraud")
    menu.connect(bluetidecomputers, "Main Menu to The BlueTide Computers")
    menu.connect(speeddeal, "Main Menu to The Speed Deal")
    menu.connect(wetaffair, "Main Menu to A Wet Affair")
    menu.connect(poweroutage, "Main Menu to Power Outage")
    menu.connect(motivationalreminder, "Main Menu to Motivational Reminder")
    menu.connect(assortmentofdishes, "Main Menu to An Assortment Of Dishes")
    menu.connect(flooding, "Main Menu to Flooding")
    menu.connect(chase, "Main Menu to The Chase")
    menu.connect(roborazzi, "Main Menu to Roborazzi")
    menu.connect(secretingredients, "Main Menu to The Secret Ingredients")
    menu.connect(bluetideshortage, "Main Menu to The BlueTide Shortage")
    menu.connect(shippinglogs, "Main Menu to The Shipping Logs")
    menu.connect(alarmsystem, "Main Menu to The Alarm System")
    menu.connect(movingthegoods, "Main Menu to Moving The Goods")
    menu.connect(havocinparaside, "Main Menu to Havoc In Paradise")
    menu.connect(elenasrevenge, "Main Menu to Elena's Revenge")
    menu.connect(truckloadoftrouble, "Main Menu to Truckload Of Trouble")
    menu.connect(ornamentordeal, "Main Menu to Ornament Ordeal")
    menu.connect(quileztools, "Main Menu to The Quilez Tools")
    menu.connect(connectingthedots, "Main Menu to Connecting The Dots")
    menu.connect(pawnshop, "Main Menu to The Pawn Shop")
    menu.connect(droidabduction, "Main Menu to The Droid Abduction")
    menu.connect(maliceinwoonderland, "Main Menu to Malice In Woonderland")
    menu.connect(handlewithcare, "Main Menu to Handle With Care")
    menu.connect(droiddismount, "Main Menu to Droid Dismount")
    menu.connect(finaldiversion, "Main Menu to The Final Diversion")

    menu.connect(blowtorchupgrade, "Main Menu to Blowtorch Upgrade")
    menu.connect(shotgunupgrade, "Main Menu to Shotgun Upgrade")
    menu.connect(plankupgrade, "Main Menu to Plank Upgrade")
    menu.connect(pipebombupgrade, "Main Menu to Pipe Bomb Upgrade")
    menu.connect(gunupgrade, "Main Menu to Gun Upgrade")
    menu.connect(bombupgrade, "Main Menu to Bomb Upgrade")
    menu.connect(rocketlauncherupgrade, "Main Menu to Rocket Launcher Upgrade")
    menu.connect(rocketboosterupgrade, "Main Menu to Rocket Booster Upgrade")
    menu.connect(leafblowerupgrade, "Main Menu to Leaf Blower Upgrade")
    menu.connect(cableupgrade, "Main Menu to Cable Upgrade")
    menu.connect(vehiclethrusterupgrade, "Main Menu to Vehicle Thruster Upgrade")
    menu.connect(nitroglycerinupgrade, "Main Menu to Nitroglycerin Upgrade")
    menu.connect(huntingrifleupgrade, "Main Menu to Hunting Rifle Upgrade")
    menu.connect(bluetideupgrade, "Main Menu to BlueTide Upgrade")


# Connects the region if option is enabled
#    if world.options.Bonus_Level:
#        bonus_level_4 = world.get_region("Bonus Level 4")
#        level_3.connect(bonus_level_4, "Level 3 to Bonus Level 4")
