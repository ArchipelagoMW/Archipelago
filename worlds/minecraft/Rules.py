from ..generic.Rules import set_rule, add_rule
from .Locations import exclusion_table, get_postgame_advancements
from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin


class MinecraftLogic(LogicMixin):

    def _mc_has_iron_ingots(self, player: int):
        return self.has('Progressive Tools', player) and self.has('Progressive Resource Crafting', player)

    def _mc_has_copper_ingots(self, player: int):
        return self.has('Progressive Tools', player) and self.has('Progressive Resource Crafting', player)

    def _mc_has_gold_ingots(self, player: int): 
        return self.has('Progressive Resource Crafting', player) and (self.has('Progressive Tools', player, 2) or self.can_reach('The Nether', 'Region', player))

    def _mc_has_diamond_pickaxe(self, player: int):
        return self.has('Progressive Tools', player, 3) and self._mc_has_iron_ingots(player)

    def _mc_craft_crossbow(self, player: int): 
        return self.has('Archery', player) and self._mc_has_iron_ingots(player)

    def _mc_has_bottle(self, player: int): 
        return self.has('Bottles', player) and self.has('Progressive Resource Crafting', player)

    def _mc_has_spyglass(self, player: int):
        return self._mc_has_copper_ingots(player) and self.has('Spyglass', player) and self._mc_can_adventure(player)

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
                    self.can_reach('The Nether', 'Region', player) or 
                    self.can_reach('Bastion Remnant', 'Region', player))

    def _mc_overworld_villager(self, player: int):
        village_region = self.multiworld.get_region('Village', player).entrances[0].parent_region.name
        if village_region == 'The Nether': # 2 options: cure zombie villager or build portal in village
            return (self.can_reach('Zombie Doctor', 'Location', player) or
                    (self._mc_has_diamond_pickaxe(player) and self.can_reach('Village', 'Region', player)))
        elif village_region == 'The End':
            return self.can_reach('Zombie Doctor', 'Location', player)
        return self.can_reach('Village', 'Region', player)

    def _mc_enter_stronghold(self, player: int):
        return self.has('Blaze Rods', player) and self.has('Brewing', player) and self.has('3 Ender Pearls', player)

    # Difficulty-dependent functions
    def _mc_combat_difficulty(self, player: int):
        return self.multiworld.combat_difficulty[player].current_key

    def _mc_can_adventure(self, player: int):
        death_link_check = not self.multiworld.death_link[player] or self.has('Bed', player)
        if self._mc_combat_difficulty(player) == 'easy':
            return self.has('Progressive Weapons', player, 2) and self._mc_has_iron_ingots(player) and death_link_check
        elif self._mc_combat_difficulty(player) == 'hard':
            return True
        return (self.has('Progressive Weapons', player) and death_link_check and 
            (self.has('Progressive Resource Crafting', player) or self.has('Campfire', player)))

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

    def _mc_can_respawn_ender_dragon(self, player: int):
        return self.can_reach('The Nether', 'Region', player) and self.can_reach('The End', 'Region', player) and \
            self.has('Progressive Resource Crafting', player) # smelt sand into glass

    def _mc_can_kill_ender_dragon(self, player: int):
        if self._mc_combat_difficulty(player) == 'easy': 
            return self.has("Progressive Weapons", player, 3) and self.has("Progressive Armor", player, 2) and \
                   self.has('Archery', player) and self._mc_can_brew_potions(player) and self._mc_can_enchant(player)
        if self._mc_combat_difficulty(player) == 'hard': 
            return (self.has('Progressive Weapons', player, 2) and self.has('Progressive Armor', player)) or \
                   (self.has('Progressive Weapons', player, 1) and self.has('Bed', player))
        return self.has('Progressive Weapons', player, 2) and self.has('Progressive Armor', player) and self.has('Archery', player)

    def _mc_has_structure_compass(self, entrance_name: str, player: int):
        if not self.multiworld.structure_compasses[player]:
            return True
        return self.has(f"Structure Compass ({self.multiworld.get_entrance(entrance_name, player).connected_region.name})", player)

# Sets rules on entrances and advancements that are always applied
def set_advancement_rules(world: MultiWorld, player: int):

    # Retrieves the appropriate structure compass for the given entrance
    def get_struct_compass(entrance_name): 
        struct = world.get_entrance(entrance_name, player).connected_region.name
        return f"Structure Compass ({struct})"

    set_rule(world.get_entrance("Nether Portal", player), lambda state: state.has('Flint and Steel', player) and 
        (state.has('Bucket', player) or state.has('Progressive Tools', player, 3)) and 
        state._mc_has_iron_ingots(player))
    set_rule(world.get_entrance("End Portal", player), lambda state: state._mc_enter_stronghold(player) and state.has('3 Ender Pearls', player, 4))
    set_rule(world.get_entrance("Overworld Structure 1", player), lambda state: state._mc_can_adventure(player) and state._mc_has_structure_compass("Overworld Structure 1", player))
    set_rule(world.get_entrance("Overworld Structure 2", player), lambda state: state._mc_can_adventure(player) and state._mc_has_structure_compass("Overworld Structure 2", player))
    set_rule(world.get_entrance("Nether Structure 1", player), lambda state: state._mc_can_adventure(player) and state._mc_has_structure_compass("Nether Structure 1", player))
    set_rule(world.get_entrance("Nether Structure 2", player), lambda state: state._mc_can_adventure(player) and state._mc_has_structure_compass("Nether Structure 2", player))
    set_rule(world.get_entrance("The End Structure", player), lambda state: state._mc_can_adventure(player) and state._mc_has_structure_compass("The End Structure", player))

    set_rule(world.get_location("Ender Dragon", player), lambda state: state._mc_can_kill_ender_dragon(player))
    set_rule(world.get_location("Wither", player), lambda state: state._mc_can_kill_wither(player))
    set_rule(world.get_location("Blaze Spawner", player), lambda state: state._mc_fortress_loot(player))

    set_rule(world.get_location("Who is Cutting Onions?", player), lambda state: state._mc_can_piglin_trade(player))
    set_rule(world.get_location("Oh Shiny", player), lambda state: state._mc_can_piglin_trade(player))
    set_rule(world.get_location("Suit Up", player), lambda state: state.has("Progressive Armor", player) and state._mc_has_iron_ingots(player))
    set_rule(world.get_location("Very Very Frightening", player), lambda state: state.has("Channeling Book", player) and 
        state._mc_can_use_anvil(player) and state._mc_can_enchant(player) and state._mc_overworld_villager(player))
    set_rule(world.get_location("Hot Stuff", player), lambda state: state.has("Bucket", player) and state._mc_has_iron_ingots(player))
    set_rule(world.get_location("Free the End", player), lambda state: state._mc_can_respawn_ender_dragon(player) and state._mc_can_kill_ender_dragon(player))
    set_rule(world.get_location("A Furious Cocktail", player), lambda state: state._mc_can_brew_potions(player) and 
                                                                             state.has("Fishing Rod", player) and # Water Breathing
                                                                             state.can_reach('The Nether', 'Region', player) and # Regeneration, Fire Resistance, gold nuggets
                                                                             state.can_reach('Village', 'Region', player) and # Night Vision, Invisibility
                                                                             state.can_reach('Bring Home the Beacon', 'Location', player)) # Resistance
    # set_rule(world.get_location("Best Friends Forever", player), lambda state: True)
    set_rule(world.get_location("Bring Home the Beacon", player), lambda state: state._mc_can_kill_wither(player) and 
        state._mc_has_diamond_pickaxe(player) and state.has("Progressive Resource Crafting", player, 2))
    set_rule(world.get_location("Not Today, Thank You", player), lambda state: state.has("Shield", player) and state._mc_has_iron_ingots(player))
    set_rule(world.get_location("Isn't It Iron Pick", player), lambda state: state.has("Progressive Tools", player, 2) and state._mc_has_iron_ingots(player))
    set_rule(world.get_location("Local Brewery", player), lambda state: state._mc_can_brew_potions(player))
    set_rule(world.get_location("The Next Generation", player), lambda state: state._mc_can_kill_ender_dragon(player))
    set_rule(world.get_location("Fishy Business", player), lambda state: state.has("Fishing Rod", player))
    # set_rule(world.get_location("Hot Tourist Destinations", player), lambda state: True)
    set_rule(world.get_location("This Boat Has Legs", player), lambda state: (state._mc_fortress_loot(player) or state._mc_complete_raid(player)) and 
        state.has("Saddle", player) and state.has("Fishing Rod", player))
    set_rule(world.get_location("Sniper Duel", player), lambda state: state.has("Archery", player))
    # set_rule(world.get_location("Nether", player), lambda state: True)
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
    set_rule(world.get_location("Two by Two", player), lambda state: state._mc_has_iron_ingots(player) and state.has("Bucket", player) and state._mc_can_adventure(player))  # shears > seagrass > turtles; buckets of tropical fish > axolotls; nether > striders; gold carrots > horses skips ingots
    # set_rule(world.get_location("Stone Age", player), lambda state: True)
    set_rule(world.get_location("Two Birds, One Arrow", player), lambda state: state._mc_craft_crossbow(player) and state._mc_can_enchant(player))
    # set_rule(world.get_location("We Need to Go Deeper", player), lambda state: True)
    set_rule(world.get_location("Who's the Pillager Now?", player), lambda state: state._mc_craft_crossbow(player))
    set_rule(world.get_location("Getting an Upgrade", player), lambda state: state.has("Progressive Tools", player))
    set_rule(world.get_location("Tactical Fishing", player), lambda state: state.has("Bucket", player) and state._mc_has_iron_ingots(player))
    set_rule(world.get_location("Zombie Doctor", player), lambda state: state._mc_can_brew_potions(player) and state._mc_has_gold_ingots(player))
    # set_rule(world.get_location("The City at the End of the Game", player), lambda state: True)
    set_rule(world.get_location("Ice Bucket Challenge", player), lambda state: state._mc_has_diamond_pickaxe(player))
    # set_rule(world.get_location("Remote Getaway", player), lambda state: True)
    set_rule(world.get_location("Into Fire", player), lambda state: state._mc_basic_combat(player))
    set_rule(world.get_location("War Pigs", player), lambda state: state._mc_basic_combat(player))
    set_rule(world.get_location("Take Aim", player), lambda state: state.has("Archery", player))
    set_rule(world.get_location("Total Beelocation", player), lambda state: state.has("Silk Touch Book", player) and state._mc_can_use_anvil(player) and state._mc_can_enchant(player))
    set_rule(world.get_location("Arbalistic", player), lambda state: state._mc_craft_crossbow(player) and state.has("Piercing IV Book", player) and 
                                                                     state._mc_can_use_anvil(player) and state._mc_can_enchant(player))
    set_rule(world.get_location("The End... Again...", player), lambda state: state._mc_can_respawn_ender_dragon(player) and state._mc_can_kill_ender_dragon(player))
    set_rule(world.get_location("Acquire Hardware", player), lambda state: state._mc_has_iron_ingots(player))
    set_rule(world.get_location("Not Quite \"Nine\" Lives", player), lambda state: state._mc_can_piglin_trade(player) and state.has("Progressive Resource Crafting", player, 2))
    set_rule(world.get_location("Cover Me With Diamonds", player), lambda state: state.has("Progressive Armor", player, 2) and state.can_reach("Diamonds!", "Location", player))
    set_rule(world.get_location("Sky's the Limit", player), lambda state: state._mc_basic_combat(player))
    set_rule(world.get_location("Hired Help", player), lambda state: state.has("Progressive Resource Crafting", player, 2) and state._mc_has_iron_ingots(player))
    # set_rule(world.get_location("Return to Sender", player), lambda state: True)
    set_rule(world.get_location("Sweet Dreams", player), lambda state: state.has("Bed", player) or state.can_reach('Village', 'Region', player))
    set_rule(world.get_location("You Need a Mint", player), lambda state: state._mc_can_respawn_ender_dragon(player) and state._mc_has_bottle(player))
    # set_rule(world.get_location("Adventure", player), lambda state: True)
    set_rule(world.get_location("Monsters Hunted", player), lambda state: state._mc_can_respawn_ender_dragon(player) and state._mc_can_kill_ender_dragon(player) and 
        state._mc_can_kill_wither(player) and state.has("Fishing Rod", player))  # pufferfish for Water Breathing
    set_rule(world.get_location("Enchanter", player), lambda state: state._mc_can_enchant(player))
    set_rule(world.get_location("Voluntary Exile", player), lambda state: state._mc_basic_combat(player))
    set_rule(world.get_location("Eye Spy", player), lambda state: state._mc_enter_stronghold(player))
    # set_rule(world.get_location("The End", player), lambda state: True)
    set_rule(world.get_location("Serious Dedication", player), lambda state: state.can_reach("Hidden in the Depths", "Location", player) and state._mc_has_gold_ingots(player))
    set_rule(world.get_location("Postmortal", player), lambda state: state._mc_complete_raid(player))
    # set_rule(world.get_location("Monster Hunter", player), lambda state: True)
    set_rule(world.get_location("Adventuring Time", player), lambda state: state._mc_can_adventure(player))
    # set_rule(world.get_location("A Seedy Place", player), lambda state: True)
    # set_rule(world.get_location("Those Were the Days", player), lambda state: True)
    set_rule(world.get_location("Hero of the Village", player), lambda state: state._mc_complete_raid(player))
    set_rule(world.get_location("Hidden in the Depths", player), lambda state: state._mc_can_brew_potions(player) and state.has("Bed", player) and state._mc_has_diamond_pickaxe(player))  # bed mining :)
    set_rule(world.get_location("Beaconator", player), lambda state: state._mc_can_kill_wither(player) and state._mc_has_diamond_pickaxe(player) and
                           state.has("Progressive Resource Crafting", player, 2))
    set_rule(world.get_location("Withering Heights", player), lambda state: state._mc_can_kill_wither(player))
    set_rule(world.get_location("A Balanced Diet", player), lambda state: state._mc_has_bottle(player) and state._mc_has_gold_ingots(player) and  # honey bottle; gapple
                           state.has("Progressive Resource Crafting", player, 2) and state.can_reach('The End', 'Region', player))  # notch apple, chorus fruit
    set_rule(world.get_location("Subspace Bubble", player), lambda state: state._mc_has_diamond_pickaxe(player))
    # set_rule(world.get_location("Husbandry", player), lambda state: True)
    set_rule(world.get_location("Country Lode, Take Me Home", player), lambda state: state.can_reach("Hidden in the Depths", "Location", player) and state._mc_has_gold_ingots(player))
    set_rule(world.get_location("Bee Our Guest", player), lambda state: state.has("Campfire", player) and state._mc_has_bottle(player))
    # set_rule(world.get_location("What a Deal!", player), lambda state: True)
    set_rule(world.get_location("Uneasy Alliance", player), lambda state: state._mc_has_diamond_pickaxe(player) and state.has('Fishing Rod', player))
    set_rule(world.get_location("Diamonds!", player), lambda state: state.has("Progressive Tools", player, 2) and state._mc_has_iron_ingots(player))
    # set_rule(world.get_location("A Terrible Fortress", player), lambda state: True)  # since you don't have to fight anything
    set_rule(world.get_location("A Throwaway Joke", player), lambda state: state._mc_can_adventure(player))  # kill drowned
    # set_rule(world.get_location("Minecraft", player), lambda state: True)
    set_rule(world.get_location("Sticky Situation", player), lambda state: state.has("Campfire", player) and state._mc_has_bottle(player))
    set_rule(world.get_location("Ol' Betsy", player), lambda state: state._mc_craft_crossbow(player))
    set_rule(world.get_location("Cover Me in Debris", player), lambda state: state.has("Progressive Armor", player, 2) and
                           state.has("8 Netherite Scrap", player, 2) and state.has("Progressive Resource Crafting", player) and
                           state.can_reach("Diamonds!", "Location", player) and state.can_reach("Hidden in the Depths", "Location", player))
    # set_rule(world.get_location("The End?", player), lambda state: True)
    # set_rule(world.get_location("The Parrots and the Bats", player), lambda state: True)
    # set_rule(world.get_location("A Complete Catalogue", player), lambda state: True)  # kill fish for raw
    # set_rule(world.get_location("Getting Wood", player), lambda state: True)
    # set_rule(world.get_location("Time to Mine!", player), lambda state: True)
    set_rule(world.get_location("Hot Topic", player), lambda state: state.has("Progressive Resource Crafting", player))
    # set_rule(world.get_location("Bake Bread", player), lambda state: True)
    set_rule(world.get_location("The Lie", player), lambda state: state._mc_has_iron_ingots(player) and state.has("Bucket", player))
    set_rule(world.get_location("On a Rail", player), lambda state: state._mc_has_iron_ingots(player) and state.has('Progressive Tools', player, 2))  # powered rails
    # set_rule(world.get_location("Time to Strike!", player), lambda state: True)
    # set_rule(world.get_location("Cow Tipper", player), lambda state: True)
    set_rule(world.get_location("When Pigs Fly", player), lambda state: (state._mc_fortress_loot(player) or state._mc_complete_raid(player)) and 
        state.has("Saddle", player) and state.has("Fishing Rod", player) and state._mc_can_adventure(player))
    set_rule(world.get_location("Overkill", player), lambda state: state._mc_can_brew_potions(player) and 
        (state.has("Progressive Weapons", player) or state.can_reach('The Nether', 'Region', player)))  # strength 1 + stone axe crit OR strength 2 + wood axe crit
    set_rule(world.get_location("Librarian", player), lambda state: state.has("Enchanting", player))
    set_rule(world.get_location("Overpowered", player), lambda state: state._mc_has_iron_ingots(player) and 
        state.has('Progressive Tools', player, 2) and state._mc_basic_combat(player))  # mine gold blocks w/ iron pick
    set_rule(world.get_location("Wax On", player), lambda state: state._mc_has_copper_ingots(player) and state.has('Campfire', player) and
        state.has('Progressive Resource Crafting', player, 2))
    set_rule(world.get_location("Wax Off", player), lambda state: state._mc_has_copper_ingots(player) and state.has('Campfire', player) and
        state.has('Progressive Resource Crafting', player, 2))
    set_rule(world.get_location("The Cutest Predator", player), lambda state: state._mc_has_iron_ingots(player) and state.has('Bucket', player))
    set_rule(world.get_location("The Healing Power of Friendship", player), lambda state: state._mc_has_iron_ingots(player) and state.has('Bucket', player))
    set_rule(world.get_location("Is It a Bird?", player), lambda state: state._mc_has_spyglass(player) and state._mc_can_adventure(player))
    set_rule(world.get_location("Is It a Balloon?", player), lambda state: state._mc_has_spyglass(player))
    set_rule(world.get_location("Is It a Plane?", player), lambda state: state._mc_has_spyglass(player) and state._mc_can_respawn_ender_dragon(player))
    set_rule(world.get_location("Surge Protector", player), lambda state: state.has("Channeling Book", player) and 
        state._mc_can_use_anvil(player) and state._mc_can_enchant(player) and state._mc_overworld_villager(player))
    set_rule(world.get_location("Light as a Rabbit", player), lambda state: state._mc_can_adventure(player) and state._mc_has_iron_ingots(player) and state.has('Bucket', player))
    set_rule(world.get_location("Glow and Behold!", player), lambda state: state._mc_can_adventure(player))
    set_rule(world.get_location("Whatever Floats Your Goat!", player), lambda state: state._mc_can_adventure(player))
    set_rule(world.get_location("Caves & Cliffs", player), lambda state: state._mc_has_iron_ingots(player) and state.has('Bucket', player) and state.has('Progressive Tools', player, 2))
    set_rule(world.get_location("Feels like home", player), lambda state: state._mc_has_iron_ingots(player) and state.has('Bucket', player) and state.has('Fishing Rod', player) and
        (state._mc_fortress_loot(player) or state._mc_complete_raid(player)) and state.has("Saddle", player))
    set_rule(world.get_location("Sound of Music", player), lambda state: state.can_reach("Diamonds!", "Location", player) and state._mc_basic_combat(player))
    set_rule(world.get_location("Star Trader", player), lambda state: state._mc_has_iron_ingots(player) and state.has('Bucket', player) and
        (state.can_reach("The Nether", 'Region', player) or state.can_reach("Nether Fortress", 'Region', player) or state._mc_can_piglin_trade(player)) and # soul sand for water elevator
        state._mc_overworld_villager(player))

    # 1.19 advancements

    # can make a cake, and a noteblock, and can reach a pillager outposts for allays
    set_rule(world.get_location("Birthday Song", player), lambda state: state.can_reach("The Lie", "Location", player) and state.has("Progressive Tools", player, 2) and state._mc_has_iron_ingots(player))
    # can get to outposts.
    # set_rule(world.get_location("You've Got a Friend in Me", player), lambda state: True)
    # craft bucket and adventure to find frog spawning biome
    set_rule(world.get_location("Bukkit Bukkit", player), lambda state: state.has("Bucket", player) and state._mc_has_iron_ingots(player) and state._mc_can_adventure(player))
    # I don't like this one its way to easy to get. just a pain to find.
    set_rule(world.get_location("It Spreads", player), lambda state: state._mc_can_adventure(player) and state._mc_has_iron_ingots(player) and state.has("Progressive Tools", player, 2))
    # literally just a duplicate of It spreads.
    set_rule(world.get_location("Sneak 100", player), lambda state: state._mc_can_adventure(player) and state._mc_has_iron_ingots(player) and state.has("Progressive Tools", player, 2))
    set_rule(world.get_location("When the Squad Hops into Town", player), lambda state: state._mc_can_adventure(player) and state.has("Lead", player))
    # lead frogs to the nether and a basalt delta's biomes to find magma cubes.
    set_rule(world.get_location("With Our Powers Combined!", player), lambda state: state._mc_can_adventure(player) and state.has("Lead", player))


# Sets rules on completion condition and postgame advancements
def set_completion_rules(world: MultiWorld, player: int):
    def reachable_locations(state):
        postgame_advancements = get_postgame_advancements(world.required_bosses[player].current_key)
        return [location for location in world.get_locations() if
                location.player == player and
                location.name not in postgame_advancements and
                location.address != None and
                location.can_reach(state)]

    def defeated_required_bosses(state):
        return (world.required_bosses[player].current_key not in {"ender_dragon", "both"} or state.has("Defeat Ender Dragon", player)) and \
            (world.required_bosses[player].current_key not in {"wither", "both"} or state.has("Defeat Wither", player))

    # 103 total advancements. Goal is to complete X advancements and then defeat the dragon. 
    # There are 11 possible postgame advancements; 5 for dragon, 5 for wither, 1 shared between them
    # Hence the max for completion is 92
    egg_shards = min(world.egg_shards_required[player], world.egg_shards_available[player])
    completion_requirements = lambda state: len(reachable_locations(state)) >= world.advancement_goal[player] and \
        state.has("Dragon Egg Shard", player, egg_shards)
    world.completion_condition[player] = lambda state: completion_requirements(state) and defeated_required_bosses(state)
    # Set rules on postgame advancements
    for adv_name in get_postgame_advancements(world.required_bosses[player].current_key):
        add_rule(world.get_location(adv_name, player), completion_requirements)
