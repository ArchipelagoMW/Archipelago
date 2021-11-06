from ..generic.Rules import set_rule
from .Locations import exclusion_table, events_table
from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin


class MinecraftLogic(LogicMixin):

    def _mc_has_iron_ingots(self, player: int):
        return self.has('Progressive Tools', player) and self.has('Progressive Resource Crafting', player)

    def _mc_has_gold_ingots(self, player: int): 
        return self.has('Progressive Resource Crafting', player) and (self.has('Progressive Tools', player, 2) or self.can_reach('The Nether', 'Region', player))

    def _mc_has_diamond_pickaxe(self, player: int):
        return self.has('Progressive Tools', player, 3) and self._mc_has_iron_ingots(player)

    def _mc_craft_crossbow(self, player: int): 
        return self.has('Archery', player) and self._mc_has_iron_ingots(player)

    def _mc_has_bottle(self, player: int): 
        return self.has('Bottles', player) and self.has('Progressive Resource Crafting', player)

    def _mc_can_enchant(self, player: int): 
        return self.has('Enchanting', player) and self._mc_has_diamond_pickaxe(player) # mine obsidian and lapis

    def _mc_can_use_anvil(self, player: int): 
        return self.has('Enchanting', player) and self.has('Progressive Resource Crafting', player, 2) and self._mc_has_iron_ingots(player)

    def _mc_fortress_loot(self, player: int): # saddles, blaze rods, wither skulls
        return self.can_reach('Nether Fortress', 'Region', player) and self._mc_basic_combat(player)

    def _mc_can_brew_potions(self, player: int):
        return self.has('Blaze Rods', player) and self.has('Brewing', player) and self._mc_has_bottle(player)

    def _mc_can_piglin_trade(self, player: int):
        return self._mc_has_gold_ingots(player) and (
                    self.can_reach('The Nether', 'Region', player) or self.can_reach('Bastion Remnant', 'Region',
                                                                                     player))

    def _mc_enter_stronghold(self, player: int):
        return self.has('Blaze Rods', player) and self.has('Brewing', player) and self.has('3 Ender Pearls', player)

    # Difficulty-dependent functions
    def _mc_combat_difficulty(self, player: int):
        return self.world.combat_difficulty[player].current_key

    def _mc_can_adventure(self, player: int):
        if self._mc_combat_difficulty(player) == 'easy':
            return self.has('Progressive Weapons', player, 2) and self._mc_has_iron_ingots(player)
        elif self._mc_combat_difficulty(player) == 'hard':
            return True
        return self.has('Progressive Weapons', player) and (self.has('Progressive Resource Crafting', player) or self.has('Campfire', player))

    def _mc_basic_combat(self, player: int):
        if self._mc_combat_difficulty(player) == 'easy': 
            return self.has('Progressive Weapons', player, 2) and self.has('Progressive Armor', player) and \
                   self.has('Shield', player) and self._mc_has_iron_ingots(player)
        elif self._mc_combat_difficulty(player) == 'hard': 
            return True
        return self.has('Progressive Weapons', player) and (self.has('Progressive Armor', player) or self.has('Shield', player)) and self._mc_has_iron_ingots(player)

    def _mc_complete_raid(self, player: int): 
        reach_regions = self.can_reach('Village', 'Region', player) and self.can_reach('Pillager Outpost', 'Region', player)
        if self._mc_combat_difficulty(player) == 'easy': 
            return reach_regions and \
                   self.has('Progressive Weapons', player, 3) and self.has('Progressive Armor', player, 2) and \
                   self.has('Shield', player) and self.has('Archery', player) and \
                   self.has('Progressive Tools', player, 2) and self._mc_has_iron_ingots(player)
        elif self._mc_combat_difficulty(player) == 'hard': # might be too hard?
            return reach_regions and self.has('Progressive Weapons', player, 2) and self._mc_has_iron_ingots(player) and \
                   (self.has('Progressive Armor', player) or self.has('Shield', player))
        return reach_regions and self.has('Progressive Weapons', player, 2) and self._mc_has_iron_ingots(player) and \
               self.has('Progressive Armor', player) and self.has('Shield', player)

    def _mc_can_kill_wither(self, player: int): 
        normal_kill = self.has("Progressive Weapons", player, 3) and self.has("Progressive Armor", player, 2) and self._mc_can_brew_potions(player) and self._mc_can_enchant(player)
        if self._mc_combat_difficulty(player) == 'easy': 
            return self._mc_fortress_loot(player) and normal_kill and self.has('Archery', player)
        elif self._mc_combat_difficulty(player) == 'hard': # cheese kill using bedrock ceilings
            return self._mc_fortress_loot(player) and (normal_kill or self.can_reach('The Nether', 'Region', player) or self.can_reach('The End', 'Region', player))
        return self._mc_fortress_loot(player) and normal_kill

    def _mc_can_kill_ender_dragon(self, player: int):
        # Since it is possible to kill the dragon without getting any of the advancements related to it, we need to require that it can be respawned. 
        respawn_dragon = self.can_reach('The Nether', 'Region', player) and self.has('Progressive Resource Crafting', player)
        if self._mc_combat_difficulty(player) == 'easy': 
            return respawn_dragon and self.has("Progressive Weapons", player, 3) and self.has("Progressive Armor", player, 2) and \
                   self.has('Archery', player) and self._mc_can_brew_potions(player) and self._mc_can_enchant(player)
        if self._mc_combat_difficulty(player) == 'hard': 
            return respawn_dragon and ((self.has('Progressive Weapons', player, 2) and self.has('Progressive Armor', player)) or \
                   (self.has('Progressive Weapons', player, 1) and self.has('Bed', player)))
        return respawn_dragon and self.has('Progressive Weapons', player, 2) and self.has('Progressive Armor', player) and self.has('Archery', player)

    def _mc_has_structure_compass(self, entrance_name: str, player: int):
        if not self.world.structure_compasses[player]:
            return True
        return self.has(f"Structure Compass ({self.world.get_entrance(entrance_name, player).connected_region.name})", player)


def set_rules(world: MultiWorld, player: int):
    def reachable_locations(state):
        postgame_advancements = exclusion_table['postgame'].copy()
        for event in events_table.keys():
            postgame_advancements.add(event)
        return [location for location in world.get_locations() if
                location.player == player and
                location.name not in postgame_advancements and
                location.can_reach(state)]

    # Retrieves the appropriate structure compass for the given entrance
    def get_struct_compass(entrance_name): 
        struct = world.get_entrance(entrance_name, player).connected_region.name
        return f"Structure Compass ({struct})"

    # 92 total advancements. Goal is to complete X advancements and then Free the End. 
    # There are 5 advancements which cannot be included for dragon spawning (4 postgame, Free the End)
    # Hence the true maximum is (92 - 5) = 87
    goal = world.advancement_goal[player]
    egg_shards = min(world.egg_shards_required[player], world.egg_shards_available[player])
    can_complete = lambda state: len(reachable_locations(state)) >= goal and state.has("Dragon Egg Shard", player, egg_shards) and state.can_reach('The End', 'Region', player) and state._mc_can_kill_ender_dragon(player)

    if world.logic[player] != 'nologic':
        world.completion_condition[player] = lambda state: state.has('Victory', player)

    set_rule(world.get_entrance("Nether Portal", player), lambda state: state.has('Flint and Steel', player) and 
        (state.has('Bucket', player) or state.has('Progressive Tools', player, 3)) and 
        state._mc_has_iron_ingots(player))
    set_rule(world.get_entrance("End Portal", player), lambda state: state._mc_enter_stronghold(player) and state.has('3 Ender Pearls', player, 4))
    set_rule(world.get_entrance("Overworld Structure 1", player), lambda state: state._mc_can_adventure(player) and state._mc_has_structure_compass("Overworld Structure 1", player))
    set_rule(world.get_entrance("Overworld Structure 2", player), lambda state: state._mc_can_adventure(player) and state._mc_has_structure_compass("Overworld Structure 2", player))
    set_rule(world.get_entrance("Nether Structure 1", player), lambda state: state._mc_can_adventure(player) and state._mc_has_structure_compass("Nether Structure 1", player))
    set_rule(world.get_entrance("Nether Structure 2", player), lambda state: state._mc_can_adventure(player) and state._mc_has_structure_compass("Nether Structure 2", player))
    set_rule(world.get_entrance("The End Structure", player), lambda state: state._mc_can_adventure(player) and state._mc_has_structure_compass("The End Structure", player))

    set_rule(world.get_location("Ender Dragon", player), lambda state: can_complete(state))
    set_rule(world.get_location("Blaze Spawner", player), lambda state: state._mc_fortress_loot(player))

    set_rule(world.get_location("Who is Cutting Onions?", player), lambda state: state._mc_can_piglin_trade(player))
    set_rule(world.get_location("Oh Shiny", player), lambda state: state._mc_can_piglin_trade(player))
    set_rule(world.get_location("Suit Up", player), lambda state: state.has("Progressive Armor", player) and state._mc_has_iron_ingots(player))
    set_rule(world.get_location("Very Very Frightening", player), lambda state: state.has("Channeling Book", player) and state._mc_can_use_anvil(player) and state._mc_can_enchant(player) and \
        ((world.get_region('Village', player).entrances[0].parent_region.name != 'The End' and state.can_reach('Village', 'Region', player)) or state.can_reach('Zombie Doctor', 'Location', player))) # need villager into the overworld for lightning strike
    set_rule(world.get_location("Hot Stuff", player), lambda state: state.has("Bucket", player) and state._mc_has_iron_ingots(player))
    set_rule(world.get_location("Free the End", player), lambda state: can_complete(state))
    set_rule(world.get_location("A Furious Cocktail", player), lambda state: state._mc_can_brew_potions(player) and 
                                                                             state.has("Fishing Rod", player) and # Water Breathing
                                                                             state.can_reach('The Nether', 'Region', player) and # Regeneration, Fire Resistance, gold nuggets
                                                                             state.can_reach('Village', 'Region', player) and # Night Vision, Invisibility
                                                                             state.can_reach('Bring Home the Beacon', 'Location', player)) # Resistance
    set_rule(world.get_location("Best Friends Forever", player), lambda state: True)
    set_rule(world.get_location("Bring Home the Beacon", player), lambda state: state._mc_can_kill_wither(player) and 
        state._mc_has_diamond_pickaxe(player) and state.has("Progressive Resource Crafting", player, 2))
    set_rule(world.get_location("Not Today, Thank You", player), lambda state: state.has("Shield", player) and state._mc_has_iron_ingots(player))
    set_rule(world.get_location("Isn't It Iron Pick", player), lambda state: state.has("Progressive Tools", player, 2) and state._mc_has_iron_ingots(player))
    set_rule(world.get_location("Local Brewery", player), lambda state: state._mc_can_brew_potions(player))
    set_rule(world.get_location("The Next Generation", player), lambda state: can_complete(state))
    set_rule(world.get_location("Fishy Business", player), lambda state: state.has("Fishing Rod", player))
    set_rule(world.get_location("Hot Tourist Destinations", player), lambda state: True)
    set_rule(world.get_location("This Boat Has Legs", player), lambda state: (state._mc_fortress_loot(player) or state._mc_complete_raid(player)) and 
        state.has("Saddle", player) and state.has("Fishing Rod", player))
    set_rule(world.get_location("Sniper Duel", player), lambda state: state.has("Archery", player))
    set_rule(world.get_location("Nether", player), lambda state: True)
    set_rule(world.get_location("Great View From Up Here", player), lambda state: state._mc_basic_combat(player))
    set_rule(world.get_location("How Did We Get Here?", player), lambda state: state._mc_can_brew_potions(player) and 
                           state._mc_has_gold_ingots(player) and  # Absorption
                           state.can_reach('End City', 'Region', player) and # Levitation
                           state.can_reach('The Nether', 'Region', player) and  # potion ingredients
                           state.has("Fishing Rod", player) and state.has("Archery",player) and  # Pufferfish, Nautilus Shells; spectral arrows
                           state.can_reach("Bring Home the Beacon", "Location", player) and  # Haste
                           state.can_reach("Hero of the Village", "Location", player))  # Bad Omen, Hero of the Village
    set_rule(world.get_location("Bullseye", player), lambda state: state.has("Archery", player) and state.has("Progressive Tools", player, 2) and state._mc_has_iron_ingots(player))
    set_rule(world.get_location("Spooky Scary Skeleton", player), lambda state: state._mc_basic_combat(player))
    set_rule(world.get_location("Two by Two", player), lambda state: state._mc_has_iron_ingots(player) and state._mc_can_adventure(player))  # shears > seagrass > turtles; nether > striders; gold carrots > horses skips ingots
    set_rule(world.get_location("Stone Age", player), lambda state: True)
    set_rule(world.get_location("Two Birds, One Arrow", player), lambda state: state._mc_craft_crossbow(player) and state._mc_can_enchant(player))
    set_rule(world.get_location("We Need to Go Deeper", player), lambda state: True)
    set_rule(world.get_location("Who's the Pillager Now?", player), lambda state: state._mc_craft_crossbow(player))
    set_rule(world.get_location("Getting an Upgrade", player), lambda state: state.has("Progressive Tools", player))
    set_rule(world.get_location("Tactical Fishing", player), lambda state: state.has("Bucket", player) and state._mc_has_iron_ingots(player))
    set_rule(world.get_location("Zombie Doctor", player), lambda state: state._mc_can_brew_potions(player) and state._mc_has_gold_ingots(player))
    set_rule(world.get_location("The City at the End of the Game", player), lambda state: True)
    set_rule(world.get_location("Ice Bucket Challenge", player), lambda state: state._mc_has_diamond_pickaxe(player))
    set_rule(world.get_location("Remote Getaway", player), lambda state: True)
    set_rule(world.get_location("Into Fire", player), lambda state: state._mc_basic_combat(player))
    set_rule(world.get_location("War Pigs", player), lambda state: state._mc_basic_combat(player))
    set_rule(world.get_location("Take Aim", player), lambda state: state.has("Archery", player))
    set_rule(world.get_location("Total Beelocation", player), lambda state: state.has("Silk Touch Book", player) and state._mc_can_use_anvil(player) and state._mc_can_enchant(player))
    set_rule(world.get_location("Arbalistic", player), lambda state: state._mc_craft_crossbow(player) and state.has("Piercing IV Book", player) and 
                                                                     state._mc_can_use_anvil(player) and state._mc_can_enchant(player))
    set_rule(world.get_location("The End... Again...", player), lambda state: can_complete(state))
    set_rule(world.get_location("Acquire Hardware", player), lambda state: state._mc_has_iron_ingots(player))
    set_rule(world.get_location("Not Quite \"Nine\" Lives", player), lambda state: state._mc_can_piglin_trade(player) and state.has("Progressive Resource Crafting", player, 2))
    set_rule(world.get_location("Cover Me With Diamonds", player), lambda state: state.has("Progressive Armor", player, 2) and state.can_reach("Diamonds!", "Location", player))
    set_rule(world.get_location("Sky's the Limit", player), lambda state: state._mc_basic_combat(player))
    set_rule(world.get_location("Hired Help", player), lambda state: state.has("Progressive Resource Crafting", player, 2) and state._mc_has_iron_ingots(player))
    set_rule(world.get_location("Return to Sender", player), lambda state: True)
    set_rule(world.get_location("Sweet Dreams", player), lambda state: state.has("Bed", player) or state.can_reach('Village', 'Region', player))
    set_rule(world.get_location("You Need a Mint", player), lambda state: can_complete(state) and state._mc_has_bottle(player))
    set_rule(world.get_location("Adventure", player), lambda state: True)
    set_rule(world.get_location("Monsters Hunted", player), lambda state: can_complete(state) and state._mc_can_kill_wither(player) and state.has("Fishing Rod", player))  # pufferfish for Water Breathing
    set_rule(world.get_location("Enchanter", player), lambda state: state._mc_can_enchant(player))
    set_rule(world.get_location("Voluntary Exile", player), lambda state: state._mc_basic_combat(player))
    set_rule(world.get_location("Eye Spy", player), lambda state: state._mc_enter_stronghold(player))
    set_rule(world.get_location("The End", player), lambda state: True)
    set_rule(world.get_location("Serious Dedication", player), lambda state: state.can_reach("Hidden in the Depths", "Location", player) and state._mc_has_gold_ingots(player))
    set_rule(world.get_location("Postmortal", player), lambda state: state._mc_complete_raid(player))
    set_rule(world.get_location("Monster Hunter", player), lambda state: True)
    set_rule(world.get_location("Adventuring Time", player), lambda state: state._mc_can_adventure(player))
    set_rule(world.get_location("A Seedy Place", player), lambda state: True)
    set_rule(world.get_location("Those Were the Days", player), lambda state: True)
    set_rule(world.get_location("Hero of the Village", player), lambda state: state._mc_complete_raid(player))
    set_rule(world.get_location("Hidden in the Depths", player), lambda state: state._mc_can_brew_potions(player) and state.has("Bed", player) and state._mc_has_diamond_pickaxe(player))  # bed mining :)
    set_rule(world.get_location("Beaconator", player), lambda state: state._mc_can_kill_wither(player) and state._mc_has_diamond_pickaxe(player) and
                           state.has("Progressive Resource Crafting", player, 2))
    set_rule(world.get_location("Withering Heights", player), lambda state: state._mc_can_kill_wither(player))
    set_rule(world.get_location("A Balanced Diet", player), lambda state: state._mc_has_bottle(player) and state._mc_has_gold_ingots(player) and  # honey bottle; gapple
                           state.has("Progressive Resource Crafting", player, 2) and state.can_reach('The End', 'Region', player))  # notch apple, chorus fruit
    set_rule(world.get_location("Subspace Bubble", player), lambda state: state._mc_has_diamond_pickaxe(player))
    set_rule(world.get_location("Husbandry", player), lambda state: True)
    set_rule(world.get_location("Country Lode, Take Me Home", player), lambda state: state.can_reach("Hidden in the Depths", "Location", player) and state._mc_has_gold_ingots(player))
    set_rule(world.get_location("Bee Our Guest", player), lambda state: state.has("Campfire", player) and state._mc_has_bottle(player))
    set_rule(world.get_location("What a Deal!", player), lambda state: True)
    set_rule(world.get_location("Uneasy Alliance", player), lambda state: state._mc_has_diamond_pickaxe(player) and state.has('Fishing Rod', player))
    set_rule(world.get_location("Diamonds!", player), lambda state: state.has("Progressive Tools", player, 2) and state._mc_has_iron_ingots(player))
    set_rule(world.get_location("A Terrible Fortress", player), lambda state: True)  # since you don't have to fight anything
    set_rule(world.get_location("A Throwaway Joke", player), lambda state: True)  # kill drowned
    set_rule(world.get_location("Minecraft", player), lambda state: True)
    set_rule(world.get_location("Sticky Situation", player), lambda state: state.has("Campfire", player) and state._mc_has_bottle(player))
    set_rule(world.get_location("Ol' Betsy", player), lambda state: state._mc_craft_crossbow(player))
    set_rule(world.get_location("Cover Me in Debris", player), lambda state: state.has("Progressive Armor", player, 2) and
                           state.has("8 Netherite Scrap", player, 2) and state.has("Progressive Resource Crafting", player) and
                           state.can_reach("Diamonds!", "Location", player) and state.can_reach("Hidden in the Depths", "Location", player))
    set_rule(world.get_location("The End?", player), lambda state: True)
    set_rule(world.get_location("The Parrots and the Bats", player), lambda state: True)
    set_rule(world.get_location("A Complete Catalogue", player), lambda state: True)  # kill fish for raw
    set_rule(world.get_location("Getting Wood", player), lambda state: True)
    set_rule(world.get_location("Time to Mine!", player), lambda state: True)
    set_rule(world.get_location("Hot Topic", player), lambda state: state.has("Progressive Resource Crafting", player))
    set_rule(world.get_location("Bake Bread", player), lambda state: True)
    set_rule(world.get_location("The Lie", player), lambda state: state._mc_has_iron_ingots(player) and state.has("Bucket", player))
    set_rule(world.get_location("On a Rail", player), lambda state: state._mc_has_iron_ingots(player) and state.has('Progressive Tools', player, 2))  # powered rails
    set_rule(world.get_location("Time to Strike!", player), lambda state: True)
    set_rule(world.get_location("Cow Tipper", player), lambda state: True)
    set_rule(world.get_location("When Pigs Fly", player), lambda state: (state._mc_fortress_loot(player) or state._mc_complete_raid(player)) and 
        state.has("Saddle", player) and state.has("Fishing Rod", player) and state._mc_can_adventure(player))
    set_rule(world.get_location("Overkill", player), lambda state: state._mc_can_brew_potions(player) and 
        (state.has("Progressive Weapons", player) or state.can_reach('The Nether', 'Region', player)))  # strength 1 + stone axe crit OR strength 2 + wood axe crit
    set_rule(world.get_location("Librarian", player), lambda state: state.has("Enchanting", player))
    set_rule(world.get_location("Overpowered", player), lambda state: state._mc_has_iron_ingots(player) and 
        state.has('Progressive Tools', player, 2) and state._mc_basic_combat(player))  # mine gold blocks w/ iron pick
