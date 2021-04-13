from ..generic.Rules import set_rule
from BaseClasses import Region, Entrance, Location, MultiWorld, Item
from Options import AdvancementGoal

def set_rules(world: MultiWorld, player: int):

    # 80 total advancements, 16 are considered "hard" or "postgame". Goal is to complete X advancements and then Free the End. 
    goal_map = {
        0: 25,
        1: 40,
        2: 60
    }
    goal = goal_map[getattr(world, 'advancement_goal')[player].value]

    if world.logic[player] != 'nologic': 
        # Can complete X+1 advancements because Free the End is included
        world.completion_condition[player] = lambda state: len(world.get_reachable_locations(state, player)) > goal and state.can_reach("Free the End", "Location", player)

    set_rule(world.get_location("Who is Cutting Onions?", player), lambda state: state.can_piglin_trade(player))
    set_rule(world.get_location("Oh Shiny", player), lambda state: state.can_piglin_trade(player))
    set_rule(world.get_location("Suit Up", player), lambda state: state.has("Progressive Armor", player) and state.has_iron_ingots(player))
    set_rule(world.get_location("Very Very Frightening", player), lambda state: state.has("Channeling Book", player) and state.can_use_anvil(player) and state.can_enchant(player))
    set_rule(world.get_location("Hot Stuff", player), lambda state: state.has("Bucket", player) and state.has_iron_ingots(player))
    set_rule(world.get_location("Free the End", player), lambda state: state.can_kill_ender_dragon(player))
    set_rule(world.get_location("A Furious Cocktail", player), lambda state: state.can_brew_potions(player))
    set_rule(world.get_location("Best Friends Forever", player), lambda state: True)
    set_rule(world.get_location("Bring Home the Beacon", player), lambda state: state.can_kill_wither(player) and state.has_diamond_pickaxe(player) and state.has("Ingot Crafting", player) and state.has("Resource Blocks", player))
    set_rule(world.get_location("Not Today, Thank You", player), lambda state: state.has("Shield", player) and state.has_iron_ingots(player))
    set_rule(world.get_location("Isn't It Iron Pick", player), lambda state: state.has("Progressive Tools", player, 2) and state.has_iron_ingots(player))
    set_rule(world.get_location("Local Brewery", player), lambda state: state.can_brew_potions(player))
    set_rule(world.get_location("The Next Generation", player), lambda state: True) # unfinished
    set_rule(world.get_location("Fishy Business", player), lambda state: state.has("Fishing Rod", player))
    set_rule(world.get_location("Hot Tourist Destinations", player), lambda state: state.enter_nether(player) and state.has("Fishing Rod", player))
    set_rule(world.get_location("This Boat Has Legs", player), lambda state: state.enter_nether(player) and state.has("Fishing Rod", player))
    set_rule(world.get_location("Sniper Duel", player), lambda state: state.has("Archery", player))
    set_rule(world.get_location("Nether", player), lambda state: state.enter_nether(player))
    set_rule(world.get_location("Great View From Up Here", player), lambda state: state.enter_end(player))
    set_rule(world.get_location("How Did We Get Here?", player), lambda state: True) # unfinished
    set_rule(world.get_location("Bullseye", player), lambda state: state.has("Archery", player) and state.has("Progressive Tools", player, 2) and state.has_iron_ingots(player))
    set_rule(world.get_location("Spooky Scary Skeleton", player), lambda state: state.enter_fortress(player))
    set_rule(world.get_location("Two by Two", player), lambda state: state.has_iron_ingots(player) and state.enter_nether(player)) # shears > seagrass > turtles; nether > striders; gold carrots > horses skips ingots
    set_rule(world.get_location("Stone Age", player), lambda state: True)
    set_rule(world.get_location("Two Birds, One Arrow", player), lambda state: state.craft_crossbow(player) and (state.can_enchant(player) or (state.has("Piercing IV Book", player) and state.can_use_anvil(player))))
    set_rule(world.get_location("We Need to Go Deeper", player), lambda state: state.enter_nether(player))
    set_rule(world.get_location("Who's the Pillager Now?", player), lambda state: state.craft_crossbow(player))
    set_rule(world.get_location("Getting an Upgrade", player), lambda state: state.has("Progressive Tools", player))
    set_rule(world.get_location("Tactical Fishing", player), lambda state: state.has("Bucket", player) and state.has_iron_ingots(player))
    set_rule(world.get_location("Zombie Doctor", player), lambda state: state.can_brew_potions(player) and state.has("Ingot Crafting", player))
    set_rule(world.get_location("The City at the End of the Game", player), lambda state: state.enter_end(player))
    set_rule(world.get_location("Ice Bucket Challenge", player), lambda state: state.has_diamond_pickaxe(player))
    set_rule(world.get_location("Remote Getaway", player), lambda state: state.enter_end(player))
    set_rule(world.get_location("Into Fire", player), lambda state: state.enter_fortress(player))
    set_rule(world.get_location("War Pigs", player), lambda state: state.enter_nether(player))
    set_rule(world.get_location("Take Aim", player), lambda state: state.has("Archery", player))
    set_rule(world.get_location("Total Beelocation", player), lambda state: state.has("Silk Touch Book", player) and state.can_use_anvil(player) and state.can_enchant(player))
    set_rule(world.get_location("Arbalistic", player), lambda state: state.craft_crossbow(player) and state.has("Piercing IV Book", player) and state.can_use_anvil(player) and state.can_enchant(player))
    set_rule(world.get_location("The End... Again...", player), lambda state: True) # unfinished
    set_rule(world.get_location("Acquire Hardware", player), lambda state: state.has_iron_ingots(player))
    set_rule(world.get_location("Not Quite \"Nine\" Lives", player), lambda state: state.can_piglin_trade(player))
    set_rule(world.get_location("Cover Me With Diamonds", player), lambda state: state.has("Progressive Armor", player, 2) and state.can_reach("Diamonds!", "Location", player))
    set_rule(world.get_location("Sky's the Limit", player), lambda state: state.enter_end(player))
    set_rule(world.get_location("Hired Help", player), lambda state: state.has("Resource Blocks", player) and state.has_iron_ingots(player))
    set_rule(world.get_location("Return to Sender", player), lambda state: state.enter_nether(player))
    set_rule(world.get_location("Sweet Dreams", player), lambda state: state.has("Bed", player))
    set_rule(world.get_location("You Need a Mint", player), lambda state: True) # unfinished
    set_rule(world.get_location("Adventure", player), lambda state: True)
    set_rule(world.get_location("Monsters Hunted", player), lambda state: True) # unfinished
    set_rule(world.get_location("Enchanter", player), lambda state: state.can_enchant(player))
    set_rule(world.get_location("Voluntary Exile", player), lambda state: state.has("Progressive Weapons", player))
    set_rule(world.get_location("Eye Spy", player), lambda state: state.enter_end(player))
    set_rule(world.get_location("The End", player), lambda state: state.enter_end(player))
    set_rule(world.get_location("Serious Dedication", player), lambda state: state.can_reach("Hidden in the Depths", "Location", player) and state.has("Ingot Crafting", player))
    set_rule(world.get_location("Postmortal", player), lambda state: state.has("Progressive Weapons", player, 2) and state.has("Progressive Armor", player) and state.has_iron_ingots(player))
    set_rule(world.get_location("Monster Hunter", player), lambda state: True)
    set_rule(world.get_location("Adventuring Time", player), lambda state: True) # please never require this
    set_rule(world.get_location("A Seedy Place", player), lambda state: True)
    set_rule(world.get_location("Those Were the Days", player), lambda state: state.enter_nether(player))
    set_rule(world.get_location("Hero of the Village", player), lambda state: state.has("Progressive Weapons", player, 2) and state.has("Progressive Armor", player) and state.has_iron_ingots(player))
    set_rule(world.get_location("Hidden in the Depths", player), lambda state: state.enter_nether(player) and state.can_brew_potions(player) and state.has("Bed", player) and state.has_diamond_pickaxe(player)) # bed mining :)
    set_rule(world.get_location("Beaconator", player), lambda state: state.can_kill_wither(player) and state.has_diamond_pickaxe(player) and state.has("Ingot Crafting", player) and state.has("Resource Blocks", player))
    set_rule(world.get_location("Withering Heights", player), lambda state: state.can_kill_wither(player))
    set_rule(world.get_location("A Balanced Diet", player), lambda state: state.has("Bottles", player) and state.has("Ingot Crafting", player) and state.has("Resource Blocks", player) and state.enter_end(player)) # honey bottle, gapple, chorus fruit
    set_rule(world.get_location("Subspace Bubble", player), lambda state: state.enter_nether(player) and state.has_diamond_pickaxe(player))
    set_rule(world.get_location("Husbandry", player), lambda state: True)
    set_rule(world.get_location("Country Lode, Take Me Home", player), lambda state: state.can_reach("Hidden in the Depths", "Location", player) and state.has("Ingot Crafting", player))
    set_rule(world.get_location("Bee Our Guest", player), lambda state: state.has("Campfire", player) and state.has("Bottles", player) and state.has("Ingot Crafting", player))
    set_rule(world.get_location("What a Deal!", player), lambda state: True)
    set_rule(world.get_location("Uneasy Alliance", player), lambda state: state.enter_nether(player) and state.has_diamond_pickaxe(player))
    set_rule(world.get_location("Diamonds!", player), lambda state: state.has("Progressive Tools", player, 2) and state.has_iron_ingots(player))
    set_rule(world.get_location("A Terrible Fortress", player), lambda state: state.enter_nether(player)) # since you don't have to fight anything
    set_rule(world.get_location("A Throwaway Joke", player), lambda state: True) # kill drowned
    set_rule(world.get_location("Minecraft", player), lambda state: True)
    set_rule(world.get_location("Sticky Situation", player), lambda state: state.has("Bottles", player) and state.has("Ingot Crafting", player))
    set_rule(world.get_location("Ol' Betsy", player), lambda state: state.craft_crossbow(player))
    set_rule(world.get_location("Cover Me in Debris", player), lambda state: state.has("Progressive Armor", player, 2) and 
                                                                             state.has("8 Ancient Debris", player, 2) and state.has("Ingot Crafting", player) and
                                                                             state.can_reach("Diamonds!", "Location", player) and state.can_reach("Hidden in the Depths", "Location", player))
    set_rule(world.get_location("The End?", player), lambda state: state.enter_end(player))
    set_rule(world.get_location("The Parrots and the Bats", player), lambda state: True)
    set_rule(world.get_location("A Complete Catalogue", player), lambda state: True) # kill fish for raw
