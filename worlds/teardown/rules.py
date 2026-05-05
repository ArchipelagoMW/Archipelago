from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.field_resolvers import FromOption
from rule_builder.rules import Has, HasGroup
from .options import MissionAmount

#, ValuableSanity

if TYPE_CHECKING:
    from .world import TeardownWorld

def set_all_rules(world: TeardownWorld) -> None:

    set_all_entrance_rules(world)
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
    world.set_rule(menu_to_oldbuildingproblem, Has("Old Building Problem Unlock"))

    world.set_rule(menu_to_leecomputers, Has("Lee Computers Unlock"))

    world.set_rule(menu_to_logindevices, Has("Login Devices Unlock"))

    world.set_rule(menu_to_makingspace, Has("Making Space Unlock"))

    world.set_rule(menu_to_classiccars, Has("Classic Cars Unlock"))

    world.set_rule(menu_to_gpsdevices, Has("The GPS Devices Unlock"))

    world.set_rule(menu_to_carwash, Has("The Car Wash Unlock"))

    world.set_rule(menu_to_heavylifting, Has("Heavy Lifting Unlock"))

    world.set_rule(menu_to_tower, Has("The Tower Unlock"))

    world.set_rule(menu_to_finearts, Has("Fine Arts Unlock"))

    world.set_rule(menu_to_toolup, Has("Tool Up Unlock"))

    world.set_rule(menu_to_artreturn, Has("Art Return Unlock"))

    world.set_rule(menu_to_covertchaos, Has("Covert Chaos Unlock"))

    world.set_rule(menu_to_insurancefraud, Has("Insurance Fraud Unlock"))

    world.set_rule(menu_to_bluetidecomputers, Has("The BlueTide Computers Unlock"))

    world.set_rule(menu_to_speeddeal, Has("The Speed Deal Unlock"))

    world.set_rule(menu_to_wetaffair, Has("A Wet Affair Unlock"))

    world.set_rule(menu_to_poweroutage, Has("Power Outage Unlock"))

    world.set_rule(menu_to_motivationalreminder, Has("Motivational Reminder Unlock"))

    world.set_rule(menu_to_assortmentofdishes, Has("An Assortment Of Dishes Unlock"))

    world.set_rule(menu_to_flooding, Has("Flooding Unlock"))

    world.set_rule(menu_to_chase, Has("The Chase Unlock"))

    world.set_rule(menu_to_roborazzi, Has("Roborazzi Unlock"))

    world.set_rule(menu_to_secretingredients, Has("The Secret Ingredients Unlock"))

    world.set_rule(menu_to_bluetideshortage, Has("The BlueTide Shortage Unlock"))

    world.set_rule(menu_to_shippinglogs, Has("The Shipping Logs Unlock"))

    world.set_rule(menu_to_alarmsystem, Has("The Alarm System Unlock"))

    world.set_rule(menu_to_movingthegoods, Has("Moving The Goods Unlock"))

    world.set_rule(menu_to_havocinparaside, Has("Havoc In Paradise Unlock"))

    world.set_rule(menu_to_elenasrevenge, Has("Elena's Revenge Unlock"))

    world.set_rule(menu_to_truckloadoftrouble, Has("Truckload Of Trouble Unlock"))

    world.set_rule(menu_to_ornamentordeal, Has("Ornament Ordeal Unlock"))

    world.set_rule(menu_to_quileztools, Has("The Quilez Tools Unlock"))

    world.set_rule(menu_to_connectingthedots, Has("Connecting The Dots Unlock"))

    world.set_rule(menu_to_pawnshop, Has("The Pawn Shop Unlock"))

    world.set_rule(menu_to_droidabduction, Has("The Droid Abduction Unlock"))

    world.set_rule(menu_to_maliceinwoonderland, Has("Malice In Woonderland Unlock"))

    world.set_rule(menu_to_handlewithcare, Has("Handle With Care Unlock"))

    world.set_rule(menu_to_droiddismount, Has("Droid Dismount Unlock"))

    world.set_rule(menu_to_finaldiversion, HasGroup("levels", count=FromOption(MissionAmount)))



    world.set_rule(menu_to_blowtorchupgrade, Has("Blowtorch Unlock"))

    world.set_rule(menu_to_shotgunupgrade, Has("Shotgun Unlock"))

    world.set_rule(menu_to_plankupgrade, Has("Plank Unlock"))

    world.set_rule(menu_to_pipebombupgrade, Has("Pipe Unlock"))

    world.set_rule(menu_to_gunupgrade, Has("Gun Unlock"))

    world.set_rule(menu_to_bombupgrade, Has("Bomb Unlock"))

    world.set_rule(menu_to_rocketlauncherupgrade, Has("Rocket Launcher Unlock"))

    world.set_rule(menu_to_rocketboosterupgrade, Has("Rocket Booster Unlock"))

    world.set_rule(menu_to_leafblowerupgrade, Has("Leaf Blower Unlock"))

    world.set_rule(menu_to_cableupgrade, Has("Cable Unlock"))

    world.set_rule(menu_to_vehiclethrusterupgrade, Has("Vehicle Thruster Unlock"))

    world.set_rule(menu_to_nitroglycerinupgrade, Has("Nitroglycerin Unlock"))

    world.set_rule(menu_to_huntingrifleupgrade, Has("Hunting Rifle Unlock"))

    world.set_rule(menu_to_bluetideupgrade, Has("BlueTide Unlock"))


def set_completion_condition(world: TeardownWorld) -> None:

    world.set_completion_rule(HasGroup("levels", count=FromOption(MissionAmount)))