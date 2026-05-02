from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule

from .options import MissionAmount, StartingLevel

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

    menu_to_blowtorchupgrade = world.get_entrance("Blowtorch Upgrade")
    menu_to_shotgunupgrade = world.get_entrance("Shotgun Upgrade")
    menu_to_plankupgrade = world.get_entrance("Plank Upgrade")
    menu_to_pipebombupgrade = world.get_entrance("Pipe Bomb Upgrade")
    menu_to_gunupgrade = world.get_entrance("Gun Upgrade")
    menu_to_bombupgrade = world.get_entrance("Bomb Upgrade")
    menu_to_rocketlauncherupgrade = world.get_entrance("Rocket Launcher Upgrade")
    menu_to_rocketboosterupgrade = world.get_entrance("Rocket Booster Upgrade")
    menu_to_leafblowerupgrade = world.get_entrance("Leaf Blower Upgrade")
    menu_to_cableupgrade = world.get_entrance("Cable Upgrade")
    menu_to_vehiclethrusterupgrade = world.get_entrance("Vehicle Thruster Upgrade")
    menu_to_nitroglycerinupgrade = world.get_entrance("Nitroglycerin Upgrade")
    menu_to_huntingrifleupgrade = world.get_entrance("Hunting Rifle Upgrade")
    menu_to_bluetideupgrade = world.get_entrance("BlueTide Upgrade")


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


    # Some entrance rules may only apply if the player enabled certain options.
    # In our case, if the hammer option is enabled, we need to add the Hammer requirement to the Entrance from
    # Overworld to the Top Middle Room.
    #if world.options.Bonus_Level:
    #    level_3_to_bonus_level_4 = world.get_entrance("Level 3 to Bonus Level 4")
    #    can_access_bonus_level_4 = Has("Bonus Level 4")
    #    world.set_rule(level_3_to_bonus_level_4, can_access_bonus_level_4)


#def set_all_location_rules(world: TeardownWorld) -> None:
    # Location rules work no differently from Entrance rules.
    # Most of our locations are chests that can simply be opened by walking up to them.
    # Thus, their logical requirements are covered by the Entrance rules of the Entrances that were required to
    # reach the region that the chest sits in.
    # However, our two enemies work differently.
    # Entering the room with the enemy is not enough, you also need to have enough combat items to be able to defeat it.
    # So, we need to set requirements on the Locations themselves.
    # Since combat is a bit more complicated, we'll use this chance to cover some advanced access rule concepts.

    # In "set_all_entrance_rules", we had a rule for a location that doesn't always exist.
    # In this case, we had to check for its existence (by checking the player's chosen options) before setting the rule.
    # Other times, you may have a situation where a location can have two different rules depending on the options.
    # In our case, the enemy in the right room has more health if hard mode is selected,
    # so ontop of the Sword, the player will either need one more health or a Shield in hard mode.
    # First, let's make our sword condition.
#    can_defeat_basic_enemy: Rule = Has("Sword")

    # Next, we'll check whether hard mode has been chosen in the player options.
#    if world.options.hard_mode:
        # We'll make the condition for "Has a Shield or a Health Upgrade".
        # We can chain two "Has" conditions together with the | operator to make "Has Shield or has Health Upgrade".
#        can_withstand_a_hit = Has("Shield") | Has("Health Upgrade")

        # Now, we chain this rule to our Sword rule.
        # Since we want both conditions to be true, in this case, we have to chain them in an "and" way.
        # For this, we can use the & operator.
#        can_defeat_basic_enemy = can_defeat_basic_enemy & can_withstand_a_hit

    # Finally, we set our rule onto the Right Room Enemy Drop location.
#    right_room_enemy = world.get_location("Right Room Enemy Drop")
#    world.set_rule(right_room_enemy, can_defeat_basic_enemy)

    # For the final boss, we also need to chain multiple conditions.
    # First of all, you always need a Sword and a Shield.
    # So far, we used the | and & operators to chain "Has" rules.
    # Instead, we can also use HasAny for an or-chain of items, or HasAll for an and-chain of items.
#    has_sword_and_shield: Rule = HasAll("Sword", "Shield")

    # In hard mode, the player also needs both Health Upgrades to survive long enough to defeat the boss.
    # For this, we can use the optional "count" parameter for "Has".
#    has_both_health_upgrades = Has("Health Upgrade", count=2)

    # Previously, we used an "if world.options.hard_mode" condition to check if we should apply the extra requirement.
    # However, if you're comfortable with boolean logic, there is another way.
    # OptionFilter is a rule which just resolves to True if the option has the specified value, or False otherwise.
#    hard_mode_is_off = OptionFilter(HardMode, False)

    # Now we can combine our rule as follows.
#    can_defeat_final_boss = has_sword_and_shield & (hard_mode_is_off | has_both_health_upgrades)
    # If you're not as comfortable with boolean logic, it might be somewhat confusing why this is correct.
    # There is nothing wrong with using "if" conditions to check for options, if you find that easier to understand.

    # Finally, we apply the rule to our "Final Boss Defeated" event location.
#    final_boss = world.get_location("Final Boss Defeated")
#    world.set_rule(final_boss, can_defeat_final_boss)


def set_completion_condition(world: TeardownWorld) -> None:
    # Finally, we need to set a completion condition for our world, defining what the player needs to win the game.
    # For this, we can use world.set_completion_rule.
    # You can just set a completion condition directly like any other condition, referencing items the player receives:

    MissionAmount



#    world.set_completion_rule(HasAll("Sword", "Shield"))

    # In our case, we went for the Victory event design pattern (see create_events() in locations.py).
    # So lets undo what we just did, and instead set the completion condition to:
    world.set_completion_rule(Has("Victory"))


# One final comment about rules:
# If your world exclusively uses Rule Builder rules (like APQuest), it's worth trying CachedRuleBuilderWorld.
# CachedRuleBuilderWorld is a subclass of World that has a bunch of caching magic to make rules faster.
# Just have your world class subclass CachedRuleBuilderWorld instead of World:
#   class TeardownWorld(CachedRuleBuilderWorld): ...
# This may speed up your world, or it may make it slower.
# The exact factors are complex and not well understood, but there is no harm in trying it.
# Generate a few seeds and see if there is a noticeable difference!
# If you're wondering, author has checked: APQuest is too simple to see any benefits, so we'll stick with "World".