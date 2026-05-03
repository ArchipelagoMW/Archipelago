from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.field_resolvers import FromOption
from rule_builder.rules import Has, HasGroup
from .options import MissionAmount
from .items import item_name_groups

#, ValuableSanity

if TYPE_CHECKING:
    from .world import TeardownWorld

def set_all_rules(world: TeardownWorld) -> None:

    set_all_entrance_rules(world)
    #set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: TeardownWorld) -> None:
    # First, we need to actually grab our entrances. Luckily, there is a helper method for this.
    menu_to_oldbuildingproblem = world.get_entrance("Main Menu to Old Building Problem")
    menu_to_leecomputers = world.get_entrance("Main Menu to Lee Computers")
    menu_to_logindevices = world.get_entrance("Main Menu to Login Devices")
    menu_to_makingspace = world.get_entrance("Main Menu to Making Space")
    menu_to_classiccars = world.get_entrance("Main Menu to Classic Cars")
    menu_to_gpsdevices = world.get_entrance("Main Menu to The GPS Devices")
    menu_to_carwash = world.get_entrance("Main Menu to The Car Wash")
    menu_to_heavylifting = world.get_entrance("Main Menu to Heavy Lifting")
    menu_to_tower = world.get_entrance("Main Menu to The Tower")
    menu_to_finearts = world.get_entrance("Main Menu to Fine Arts")
    menu_to_toolup = world.get_entrance("Main Menu to Tool Up")
    menu_to_artreturn = world.get_entrance("Main Menu to Art Return")
    menu_to_covertchaos = world.get_entrance("Main Menu to Covert Chaos")
    menu_to_insurancefraud = world.get_entrance("Main Menu to Insurance Fraud")
    menu_to_bluetidecomputers = world.get_entrance("Main Menu to The BlueTide Computers")
    menu_to_speeddeal = world.get_entrance("Main Menu to The Speed Deal")
    menu_to_wetaffair = world.get_entrance("Main Menu to A Wet Affair")
    menu_to_poweroutage = world.get_entrance("Main Menu to Power Outage")
    menu_to_motivationalreminder = world.get_entrance("Main Menu to Motivational Reminder")
    menu_to_assortmentofdishes = world.get_entrance("Main Menu to An Assortment Of Dishes")
    menu_to_flooding = world.get_entrance("Main Menu to Flooding")
    menu_to_chase = world.get_entrance("Main Menu to The Chase")
    menu_to_roborazzi = world.get_entrance("Main Menu to Roborazzi")
    menu_to_secretingredients = world.get_entrance("Main Menu to The Secret Ingredients")
    menu_to_bluetideshortage = world.get_entrance("Main Menu to The BlueTide Shortage")
    menu_to_shippinglogs = world.get_entrance("Main Menu to The Shipping Logs")
    menu_to_alarmsystem = world.get_entrance("Main Menu to The Alarm System")
    menu_to_movingthegoods = world.get_entrance("Main Menu to Moving The Goods")
    menu_to_havocinparaside = world.get_entrance("Main Menu to Havoc In Paradise")
    menu_to_elenasrevenge = world.get_entrance("Main Menu to Elena's Revenge")
    menu_to_truckloadoftrouble = world.get_entrance("Main Menu to Truckload Of Trouble")
    menu_to_ornamentordeal = world.get_entrance("Main Menu to Ornament Ordeal")
    menu_to_quileztools = world.get_entrance("Main Menu to The Quilez Tools")
    menu_to_connectingthedots = world.get_entrance("Main Menu to Connecting The Dots")
    menu_to_pawnshop = world.get_entrance("Main Menu to The Pawn Shop")
    menu_to_droidabduction = world.get_entrance("Main Menu to The Droid Abduction")
    menu_to_maliceinwoonderland = world.get_entrance("Main Menu to Malice In Woonderland")
    menu_to_handlewithcare = world.get_entrance("Main Menu to Handle With Care")
    menu_to_droiddismount = world.get_entrance("Main Menu to Droid Dismount")
    menu_to_finaldiversion = world.get_entrance("Main Menu to The Final Diversion")

    menu_to_blowtorchupgrade = world.get_entrance("Main Menu to Blowtorch Upgrade")
    menu_to_shotgunupgrade = world.get_entrance("Main Menu to Shotgun Upgrade")
    menu_to_plankupgrade = world.get_entrance("Main Menu to Plank Upgrade")
    menu_to_pipebombupgrade = world.get_entrance("Main Menu to Pipe Bomb Upgrade")
    menu_to_gunupgrade = world.get_entrance("Main Menu to Gun Upgrade")
    menu_to_bombupgrade = world.get_entrance("Main Menu to Bomb Upgrade")
    menu_to_rocketlauncherupgrade = world.get_entrance("Main Menu to Rocket Launcher Upgrade")
    menu_to_rocketboosterupgrade = world.get_entrance("Main Menu to Rocket Booster Upgrade")
    menu_to_leafblowerupgrade = world.get_entrance("Main Menu to Leaf Blower Upgrade")
    menu_to_cableupgrade = world.get_entrance("Main Menu to Cable Upgrade")
    menu_to_vehiclethrusterupgrade = world.get_entrance("Main Menu to Vehicle Thruster Upgrade")
    menu_to_nitroglycerinupgrade = world.get_entrance("Main Menu to Nitroglycerin Upgrade")
    menu_to_huntingrifleupgrade = world.get_entrance("Main Menu to Hunting Rifle Upgrade")
    menu_to_bluetideupgrade = world.get_entrance("Main Menu to BlueTide Upgrade")


    # Now, let's make some rules!
    # For this, we need a rule that says "player has a Sword".
    # We can use a "Has"-type rule from the rule_builder module for this.
    can_access_oldbuildingproblem = Has("Old Building Problem Unlock")
    world.set_rule(menu_to_oldbuildingproblem, can_access_oldbuildingproblem)

    can_access_leecomputers = Has("Lee Computers Unlock")
    world.set_rule(menu_to_leecomputers, can_access_leecomputers)

    can_access_logindevices = Has("Login Devices Unlock")
    world.set_rule(menu_to_logindevices, can_access_logindevices)

    can_access_makingspace = Has("Making Space Unlock")
    world.set_rule(menu_to_makingspace, can_access_makingspace)

    can_access_classiccars = Has("Classic Cars Unlock")
    world.set_rule(menu_to_classiccars, can_access_classiccars)

    can_access_gpsdevices = Has("The GPS Devices Unlock")
    world.set_rule(menu_to_gpsdevices, can_access_gpsdevices)

    can_access_carwash = Has("The Car Wash Unlock")
    world.set_rule(menu_to_carwash, can_access_carwash)

    can_access_heavylifting = Has("Heavy Lifting Unlock")
    world.set_rule(menu_to_heavylifting, can_access_heavylifting)

    can_access_tower = Has("The Tower Unlock")
    world.set_rule(menu_to_tower, can_access_tower)

    can_access_finearts = Has("Fine Arts Unlock")
    world.set_rule(menu_to_finearts, can_access_finearts)

    can_access_toolup = Has("Tool Up Unlock")
    world.set_rule(menu_to_toolup, can_access_toolup)

    can_access_artreturn = Has("Art Return Unlock")
    world.set_rule(menu_to_artreturn, can_access_artreturn)

    can_access_covertchaos = Has("Covert Chaos Unlock")
    world.set_rule(menu_to_covertchaos, can_access_covertchaos)

    can_access_insurancefraud = Has("Insurance Fraud Unlock")
    world.set_rule(menu_to_insurancefraud, can_access_insurancefraud)

    can_access_bluetidecomputers = Has("The BlueTide Computers Unlock")
    world.set_rule(menu_to_bluetidecomputers, can_access_bluetidecomputers)

    can_access_speeddeal = Has("The Speed Deal Unlock")
    world.set_rule(menu_to_speeddeal, can_access_speeddeal)

    can_access_wetaffair = Has("A Wet Affair Unlock")
    world.set_rule(menu_to_wetaffair, can_access_wetaffair)

    can_access_poweroutage = Has("Power Outage Unlock")
    world.set_rule(menu_to_poweroutage, can_access_poweroutage)

    can_access_motivationalreminder = Has("Motivational Reminder Unlock")
    world.set_rule(menu_to_motivationalreminder, can_access_motivationalreminder)

    can_access_assortmentofdishes = Has("An Assortment Of Dishes Unlock")
    world.set_rule(menu_to_assortmentofdishes, can_access_assortmentofdishes)

    can_access_flooding = Has("Flooding Unlock")
    world.set_rule(menu_to_flooding, can_access_flooding)

    can_access_chase = Has("The Chase Unlock")
    world.set_rule(menu_to_chase, can_access_chase)

    can_access_roborazzi = Has("Roborazzi Unlock")
    world.set_rule(menu_to_roborazzi, can_access_roborazzi)

    can_access_secretingredients = Has("The Secret Ingredients Unlock")
    world.set_rule(menu_to_secretingredients, can_access_secretingredients)

    can_access_bluetideshortage = Has("The BlueTide Shortage Unlock")
    world.set_rule(menu_to_bluetideshortage, can_access_bluetideshortage)

    can_access_shippinglogs = Has("The Shipping Logs Unlock")
    world.set_rule(menu_to_shippinglogs, can_access_shippinglogs)

    can_access_alarmsystem = Has("The Alarm System Unlock")
    world.set_rule(menu_to_alarmsystem, can_access_alarmsystem)

    can_access_movingthegoods = Has("Moving The Goods Unlock")
    world.set_rule(menu_to_movingthegoods, can_access_movingthegoods)

    can_access_havocinparaside = Has("Havoc In Paradise Unlock")
    world.set_rule(menu_to_havocinparaside, can_access_havocinparaside)

    can_access_elenasrevenge = Has("Elena's Revenge Unlock")
    world.set_rule(menu_to_elenasrevenge, can_access_elenasrevenge)

    can_access_truckloadoftrouble = Has("Truckload Of Trouble Unlock")
    world.set_rule(menu_to_truckloadoftrouble, can_access_truckloadoftrouble)

    can_access_ornamentordeal = Has("Ornament Ordeal Unlock")
    world.set_rule(menu_to_ornamentordeal, can_access_ornamentordeal)

    can_access_quileztools = Has("The Quilez Tools Unlock")
    world.set_rule(menu_to_quileztools, can_access_quileztools)

    can_access_connectingthedots = Has("Connecting The Dots Unlock")
    world.set_rule(menu_to_connectingthedots, can_access_connectingthedots)

    can_access_pawnshop = Has("The Pawn Shop Unlock")
    world.set_rule(menu_to_pawnshop, can_access_pawnshop)

    can_access_droidabduction = Has("The Droid Abduction Unlock")
    world.set_rule(menu_to_droidabduction, can_access_droidabduction)

    can_access_maliceinwoonderland = Has("Malice In Woonderland Unlock")
    world.set_rule(menu_to_maliceinwoonderland, can_access_maliceinwoonderland)

    can_access_handlewithcare = Has("Handle With Care Unlock")
    world.set_rule(menu_to_handlewithcare, can_access_handlewithcare)

    can_access_droiddismount = Has("Droid Dismount Unlock")
    world.set_rule(menu_to_droiddismount, can_access_droiddismount)

    can_access_finaldiversion = Has("The Final Diversion Unlock")
    world.set_rule(menu_to_finaldiversion, can_access_finaldiversion)


    can_access_blowtorchupgrade = Has("Blowtorch Unlock")
    world.set_rule(menu_to_blowtorchupgrade, can_access_blowtorchupgrade)

    can_access_shotgunupgrade = Has("Shotgun Unlock")
    world.set_rule(menu_to_shotgunupgrade, can_access_shotgunupgrade)

    can_access_plankupgrade = Has("Plank Unlock")
    world.set_rule(menu_to_plankupgrade, can_access_plankupgrade)

    can_access_pipebombupgrade = Has("Pipe Unlock")
    world.set_rule(menu_to_pipebombupgrade, can_access_pipebombupgrade)

    can_access_gunupgrade = Has("Gun Unlock")
    world.set_rule(menu_to_gunupgrade, can_access_gunupgrade)

    can_access_bombupgrade = Has("Bomb Unlock")
    world.set_rule(menu_to_bombupgrade, can_access_bombupgrade)

    can_access_rocketlauncherupgrade = Has("Rocket Launcher Unlock")
    world.set_rule(menu_to_rocketlauncherupgrade, can_access_rocketlauncherupgrade)

    can_access_rocketboosterupgrade = Has("Rocket Booster Unlock")
    world.set_rule(menu_to_rocketboosterupgrade, can_access_rocketboosterupgrade)

    can_access_leafblowerupgrade = Has("Leaf Blower Unlock")
    world.set_rule(menu_to_leafblowerupgrade, can_access_leafblowerupgrade)

    can_access_cableupgrade = Has("Cable Unlock")
    world.set_rule(menu_to_cableupgrade, can_access_cableupgrade)

    can_access_vehiclethrusterupgrade = Has("Vehicle Thruster Unlock")
    world.set_rule(menu_to_vehiclethrusterupgrade, can_access_vehiclethrusterupgrade)

    can_access_nitroglycerinupgrade = Has("Nitroglycerin Unlock")
    world.set_rule(menu_to_nitroglycerinupgrade, can_access_nitroglycerinupgrade)

    can_access_huntingrifleupgrade = Has("Hunting Rifle Unlock")
    world.set_rule(menu_to_huntingrifleupgrade, can_access_huntingrifleupgrade)

    can_access_bluetideupgrade = Has("BlueTide Unlock")
    world.set_rule(menu_to_bluetideupgrade, can_access_bluetideupgrade)


def set_completion_condition(world: TeardownWorld) -> None:

    world.set_completion_rule(HasGroup("levels", count=FromOption(MissionAmount)))