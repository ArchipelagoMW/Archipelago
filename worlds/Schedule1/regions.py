from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region

if TYPE_CHECKING:
    from .world import Schedule1World as Schedule1World

# A region is a container for locations ("checks"), which connects to other regions via "Entrance" objects.
# Many games will model their Regions after physical in-game places, but you can also have more abstract regions.
# For a location to be in logic, its containing region must be reachable.
# The Entrances connecting regions can have rules - more on that in rules.py.
# This makes regions especially useful for traversal logic ("Can the player reach this part of the map?")

# Every location must be inside a region, and you must have at least one region.
# This is why we create regions first, and then later we create the locations (in locations.py).


def create_and_connect_regions(world: Schedule1World) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: Schedule1World) -> None:
    # Creating a region is as simple as calling the constructor of the Region class.

    # Only regions that are mandatory checks.
    overworld = Region("Overworld", world.player, world.multiworld)   
    missions = Region("Missions", world.player, world.multiworld)
    
    # Let's put all these regions in a list.
    regions = [overworld, missions]

    # Some regions may only exist if the player enables certain options.
    # In our case, the Hammer locks the top middle chest in its own room if the hammer option is enabled.
    if world.options.randomize_level_unlocks:
        level_unlocks = Region("Level Unlocks", world.player, world.multiworld)
        regions.append(level_unlocks)

    if world.options.recipe_checks > 0:
        weed_recipe_checks = Region("Weed Recipe Checks", world.player, world.multiworld)
        meth_recipe_checks = Region("Meth Recipe Checks", world.player, world.multiworld)
        shrooms_recipe_checks = Region("Shrooms Recipe Checks", world.player, world.multiworld)
        cocaine_recipe_checks = Region("Cocaine Recipe Checks", world.player, world.multiworld)
        regions.append(weed_recipe_checks)
        regions.append(meth_recipe_checks)
        regions.append(shrooms_recipe_checks)
        regions.append(cocaine_recipe_checks)
    # cartel regions
    if not world.options.randomize_cartel_influence:
        cartel_region_westville = Region("Cartel Westville", world.player, world.multiworld)
        cartel_region_downtown = Region("Cartel Downtown", world.player, world.multiworld)
        cartel_region_docks = Region("Cartel Docks", world.player, world.multiworld)
        cartel_region_suburbia = Region("Cartel Suburbia", world.player, world.multiworld)
        cartel_region_uptown = Region("Cartel Uptown", world.player, world.multiworld)

        regions.append(cartel_region_westville)
        regions.append(cartel_region_docks)
        regions.append(cartel_region_downtown)
        regions.append(cartel_region_suburbia)
        regions.append(cartel_region_uptown)

    # customer regions
    customer_region_northtown = Region("Customer Northtown", world.player, world.multiworld)
    customer_region_westville = Region("Customer Westville", world.player, world.multiworld)
    customer_region_downtown = Region("Customer Downtown", world.player, world.multiworld)
    customer_region_docks = Region("Customer Docks", world.player, world.multiworld)
    customer_region_suburbia = Region("Customer Suburbia", world.player, world.multiworld)
    customer_region_uptown = Region("Customer Uptown", world.player, world.multiworld)
    regions.append(customer_region_docks)
    regions.append(customer_region_downtown)
    regions.append(customer_region_northtown)
    regions.append(customer_region_suburbia)
    regions.append(customer_region_uptown)
    regions.append(customer_region_westville)

    if world.options.randomize_business_properties or world.options.randomize_drug_making_properties:
        realtor = Region("Realtor", world.player, world.multiworld)
        regions.append(realtor)

    # We now need to add these regions to multiworld.regions so that AP knows about their existence.
    world.multiworld.regions += regions


def connect_regions(world: Schedule1World) -> None:
    # We have regions now, but still need to connect them to each other.
    # But wait, we no longer have access to the region variables we created in create_all_regions()!
    # Luckily, once you've submitted your regions to multiworld.regions,
    # you can get them at any time using world.get_region(...).
    overworld = world.get_region("Overworld")
    missions = world.get_region("Missions")
    if not world.options.randomize_cartel_influence:
        cartel_region_westville = world.get_region("Cartel Westville")
        cartel_region_downtown = world.get_region("Cartel Downtown")
        cartel_region_docks = world.get_region("Cartel Docks")
        cartel_region_suburbia = world.get_region("Cartel Suburbia")
        cartel_region_uptown = world.get_region("Cartel Uptown")
    if world.options.randomize_level_unlocks:
        level_unlocks = world.get_region("Level Unlocks")
    
    customer_region_northtown = world.get_region("Customer Northtown")
    customer_region_westville = world.get_region("Customer Westville")
    customer_region_downtown = world.get_region("Customer Downtown")
    customer_region_docks = world.get_region("Customer Docks")
    customer_region_suburbia = world.get_region("Customer Suburbia")
    customer_region_uptown = world.get_region("Customer Uptown")

    overworld.connect(missions, "Overworld to Missions")

    overworld.connect(customer_region_northtown, "Overworld to Customer Northtown")
    if not world.options.randomize_cartel_influence:
        cartel_region_westville.connect(customer_region_downtown, "Cartel Westville to Customer Downtown")
        cartel_region_downtown.connect(customer_region_docks, "Cartel Downtown to Customer Docks")
        cartel_region_docks.connect(customer_region_suburbia, "Cartel Docks to Customer Suburbia")
        cartel_region_suburbia.connect(customer_region_uptown, "Cartel Suburbia to Customer Uptown")
    else:
        #These are fine. We need to set rules to make it always true if they're randomized though
        overworld.connect(customer_region_downtown, "Overworld to Customer Downtown")
        overworld.connect(customer_region_docks, "Overworld to Customer Docks")
        overworld.connect(customer_region_suburbia, "Overworld to Customer Suburbia")
        overworld.connect(customer_region_uptown, "Overworld to Customer Uptown")
    
    if world.options.randomize_level_unlocks: 
        overworld.connect(level_unlocks, "Overworld to Level Unlocks")
        level_unlocks.connect(customer_region_westville, "Level Unlocks to Customer Westville")
        # still need to have randomized for there to even be checks
        if not world.options.randomize_cartel_influence:
            level_unlocks.connect(cartel_region_westville, "Level Unlocks to Cartel Westville")

    if not world.options.randomize_cartel_influence:
        cartel_region_westville.connect(cartel_region_downtown, "Cartel Westville to Cartel Downtown")
        cartel_region_downtown.connect(cartel_region_docks, "Cartel Downtown to Cartel Docks")
        cartel_region_docks.connect(cartel_region_suburbia, "Cartel Docks to Cartel Suburbia")
        cartel_region_suburbia.connect(cartel_region_uptown, "Cartel Suburbia to Cartel Uptown")

    # Okay, now we can get connecting. For this, we need to create Entrances.
    # Entrances are inherently one-way, but crucially, AP assumes you can always return to the origin region.
    # One way to create an Entrance is by calling the Entrance constructor.
    if world.options.recipe_checks > 0:
        weed_recipe_checks = world.get_region("Weed Recipe Checks")
        meth_recipe_checks = world.get_region("Meth Recipe Checks")
        shrooms_recipe_checks = world.get_region("Shrooms Recipe Checks")
        cocaine_recipe_checks = world.get_region("Cocaine Recipe Checks")
        overworld.connect(weed_recipe_checks, "Overworld to Weed Recipe Checks")
        overworld.connect(meth_recipe_checks, "Overworld to Meth Recipe Checks")
        overworld.connect(shrooms_recipe_checks, "Overworld to Shrooms Recipe Checks")
        overworld.connect(cocaine_recipe_checks, "Overworld to Cocaine Recipe Checks")

    if world.options.randomize_business_properties or world.options.randomize_drug_making_properties:
        realtor = world.get_region("Realtor")
        overworld.connect(realtor, "Overworld to Realtor")