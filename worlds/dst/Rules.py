import typing
from collections.abc import Callable

from BaseClasses import CollectionState
from worlds.generic.Rules import exclusion_rules, set_rule, add_rule, forbid_item
from worlds.AutoWorld import World

from .Locations import location_data_table
from .Options import DSTOptions
from .Items import item_data_table

def set_rules(dst_world: World) -> None:
    multiworld = dst_world.multiworld
    player = dst_world.player
    options:DSTOptions = dst_world.options
    
    ADVANCED_PLAYER_BIAS = options.skill_level.current_key != "easy"
    EXPERT_PLAYER_BIAS = options.skill_level.current_key == "expert"
    WARLY_DISHES_ENABLED = options.cooking_locations.current_key == "warly_enabled"
    CAVES_ENABLED = True # TODO: Replace with caves option
    CRAFT_WITH_LOCKED_RECIPES = True # TODO: Replace with CRAFT_WITH_LOCKED_RECIPES option
    NO_UNLOCK_RECIPES_SHUFFLED = bool(options.shuffle_no_unlock_recipes.value)

    # Rules not dependent on other rules
    def reached_winter (state: CollectionState) -> bool: 
        return state.has("Reach Winter", player)

    def reached_spring (state: CollectionState) -> bool: 
        return state.has("Reach Spring", player)

    def reached_summer (state: CollectionState) -> bool: 
        return state.has("Reach Summer", player)

    def reached_autumn (state: CollectionState) -> bool: 
        return state.has("Reach Autumn", player)

    def reached_late_game (state: CollectionState) -> bool: 
        return state.has("Late Game", player)

    def is_winter (state: CollectionState) -> bool: 
        return reached_winter(state) and (not reached_spring(state) or reached_late_game(state))

    def is_spring (state: CollectionState) -> bool: 
        return reached_spring(state) and (not reached_summer(state) or reached_late_game(state))

    def is_summer (state: CollectionState) -> bool: 
        return reached_summer(state) and (not reached_autumn(state) or reached_late_game(state))

    def is_autumn (state: CollectionState) -> bool: 
        return reached_autumn(state) or not reached_winter(state)

    def mining (state: CollectionState) -> bool: 
        return state.has_any(["Pickaxe", "Opulent Pickaxe", "Woodie"], player)
    
    def chopping (state: CollectionState) -> bool: 
        return state.has_any(["Axe", "Luxury Axe", "Woodie"], player)
    
    def hammering (state: CollectionState) -> bool: 
        return state.has_any(["Hammer", "Woodie"], player)
    
    def bug_catching (state: CollectionState) -> bool:
        return state.has_all(["Bug Net", "Rope"], player)

    def digging (state: CollectionState) -> bool:
        return state.has_any(["Shovel", "Regal Shovel"], player)

    def bird_caging (state: CollectionState) -> bool:
        return state.has_all(["Bird Trap", "Birdcage", "Papyrus"], player)

    def honey_farming (state: CollectionState) -> bool:
        return state.has_all(["Bee Box", "Boards", "Bug Net", "Rope"], player) or ADVANCED_PLAYER_BIAS

    def nightmare_fuel (state: CollectionState) -> bool: 
        return CRAFT_WITH_LOCKED_RECIPES or state.has("Nightmare Fuel", player)

    # Rules dependent on other rules. Avoid recursion by using rules above it    
    def basic_combat (state: CollectionState) -> bool:
        if EXPERT_PLAYER_BIAS: return True
        return state.has_all(["Rope", "Spear"], player) and state.has_any(["Log Suit", "Football Helmet"], player) and chopping(state)
    
    def pre_basic_combat (state: CollectionState) -> bool:
        if EXPERT_PLAYER_BIAS: return True
        return (
            (state.has("Grass Suit", player) and chopping(state)) 
            or basic_combat(state)
        )

    def gem_digging (state: CollectionState) -> bool:
        return digging(state),

    def ice_staff (state: CollectionState) -> bool:
        (state.has_all(["Spear", "Rope", "Ice Staff"], player) and gem_digging(state))

    def fire_staff (state: CollectionState) -> bool:
        (state.has_all(["Spear", "Rope", "Fire Staff"], player) and gem_digging(state) and nightmare_fuel(state))
        
    def firestarting (state: CollectionState) -> bool: 
        return (
            state.has("Torch", player)
            or (state.has("Campfire", player) and chopping(state)) 
            or fire_staff(state)
        )

    def charcoal (state: CollectionState) -> bool: 
        return chopping(state) and firestarting(state) 

    def can_get_feathers (state: CollectionState) -> bool:
        if EXPERT_PLAYER_BIAS: return True
        return (
            (state.has_all(["Boomerang", "Boards"], player) and charcoal(state))
            or state.has("Bird Trap", player) 
            or ice_staff(state) 
        )
    
    def basic_survival (state: CollectionState) -> bool:
        if EXPERT_PLAYER_BIAS:
            return firestarting(state)
        return (
            firestarting(state) 
            and state.has_any(["Axe", "Pickaxe"], player) # Have a flint tool at least
        )

    def has_survived_num_days (day_goal:int, state: CollectionState) -> bool:
        # Prioritize basic survival
        if not basic_survival(state):
            return False
        # Assume number of days lived based on items count
        item_count = state.count_group("all", player)
        if item_count < 4:
            return False
        return (day_goal if day_goal < 50 else 50) > (4 - (item_count/2))

    def butter_luck (state: CollectionState) -> bool: 
        return has_survived_num_days(40, state) or EXPERT_PLAYER_BIAS

    def hostile_flare (state: CollectionState) -> bool: 
        return (
            state.has_all(["Flare", "Hostile Flare"], player) 
            and mining(state) 
            and firestarting(state)
        )

    def backpack (state: CollectionState) -> bool:
        return (
            state.has("Backpack", player)
            or (state.has_all(["Piggyback", "Rope"], player) and pre_basic_combat(state))
        )

    def basic_exploration (state: CollectionState) -> bool:
        if EXPERT_PLAYER_BIAS: return True
        return (
            basic_survival(state) 
            and backpack(state) 
            and chopping(state) 
            and mining(state)
            and state.has_all(["Telltale Heart", "Torch", "Campfire"], player)
        )

    def basic_cooking (state: CollectionState) -> bool:
        return state.has_all(["Cut Stone", "Crock Pot"], player) and charcoal(state)

    def pre_basic_cooking (state: CollectionState) -> bool:
        return WARLY_DISHES_ENABLED or basic_cooking(state)

    def quick_healing (state: CollectionState) -> bool:
        return (
            (basic_cooking(state) and not state.has("Wormwood", player)) # Wormwood can't heal from food
            or (state.has("Healing Salve", player) and firestarting(state) and mining(state)) # Ash and rocks
            or (honey_farming(state) and state.has_all(["Honey Poultice", "Papyrus"], player)) 
            or (state.has("Bat Bat", player) and CAVES_ENABLED and (CRAFT_WITH_LOCKED_RECIPES or state.has("Purple Gem", player)))
        )

    def slow_healing (state: CollectionState) -> bool:
        return (
            state.has_all(["Tent", "Rope"], player) 
            or (state.has_all(["Siesta Lean-to", "Rope", "Boards"], player) and chopping(state))
            or state.has_all(["Rope", "Straw Roll", "Fur Roll"], player)
        )

    def healing (state: CollectionState) -> bool:
        return quick_healing(state) or slow_healing(state) or EXPERT_PLAYER_BIAS

    def desert_exploration (state: CollectionState) -> bool:
        if ADVANCED_PLAYER_BIAS: return True
        return basic_survival(state) and pre_basic_combat(state)

    def swamp_exploration (state: CollectionState) -> bool:
        if ADVANCED_PLAYER_BIAS: return True
        return (
            basic_survival(state) 
            and (pre_basic_combat(state) or healing(state)) # Kinda dangerous
        )

    def base_making (state: CollectionState) -> bool:
        return (
            state.has_all(["Boards", "Cut Stone", "Electrical Doodad", "Rope", "Fire Pit"], player) 
            and chopping(state) 
            and mining(state) 
            and (state.has_all(["Chest", "Ice Box"], player) or EXPERT_PLAYER_BIAS)
        )

    def basic_farming (state: CollectionState) -> bool:
        return (
            state.has("Wormwood", player) or ( # Wormwood can plant directly on the ground
                state.has_any(["Garden Hoe", "Splendid Garden Hoe"], player) 
                and state.has("Garden Digamajig", player) 
                and base_making(state) # Boards and Rope requirement
            )
        )

    def advanced_combat (state: CollectionState) -> bool:
        return (
            basic_combat(state) 
            and (state.has("Booster Shot", player) or EXPERT_PLAYER_BIAS) # Allow players to recover max health
            and (
                state.has("Hambat", player)
                or (state.has("Dark Sword", player) and nightmare_fuel(state))
                or state.has_all(["Glass Cutter", "Boards"], player)
            ) 
            and (base_making(state) or ADVANCED_PLAYER_BIAS)
        )

    def advanced_boss_combat (state: CollectionState) -> bool:
        return (
            advanced_combat(state) 
            and (quick_healing(state) or EXPERT_PLAYER_BIAS)
        )

    def winter_survival (state: CollectionState) -> bool:
        if not firestarting(state): return False
        if ADVANCED_PLAYER_BIAS: return True
        return (
            state.has_all(["Razor", "Thermal Stone", "Rabbit Earmuffs", "Pickaxe"], player) 
            and state.has_any(["Puffy Vest", "Beefalo Hat", "Winter Hat", "Cat Cap"], player)
            and state.has_any(["Campfire", "Fire Pit"], player)
        )

    def electric_insulation (state: CollectionState) -> bool:
        if not hammering(state): return False # Everything requires bones and/or moleworms
        return (
            state.has_any(["Rain Coat", "Rain Hat"], player) 
            or state.has_all(["Eyebrella", "Defeat Deerclops"], player)
        )

    def lightning_rod (state: CollectionState) -> bool:
        return (
            state.has_all(["Lightning Rod", "Cut Stone"], player) 
            or state.has_all(["Lightning Conductor", "Mast Kit", "Rope", "Boards"], player)
        )

    def spring_survival (state: CollectionState) -> bool:
        if ADVANCED_PLAYER_BIAS: return True
        return (
            (electric_insulation(state) or state.has("Umbrella", player)) 
            and lightning_rod(state)
            and state.has_all(["Straw Hat", "Pretty Parasol"], player) # Ensure basic stuff at this point
        )

    def has_cooling_source (state: CollectionState) -> bool:
        return (
            state.has_all(["Thermal Stone", "Ice Box", "Cut Stone", "Pickaxe"], player) 
            or state.has_any(["Endothermic Fire", "Chilled Amulet"], player)
            or state.has_all(["Endothermic Fire Pit", "Cut Stone", "Electrical Doodad"], player)
            or(state.has("Mooncaller Staff", player) and ADVANCED_PLAYER_BIAS)
        )

    def has_summer_insulation (state: CollectionState) -> bool:
        return (
            state.has_any(["Umbrella", "Summer Frest", "Thermal Stone", "Pickaxe"], player) 
            or state.has_all(["Floral Shirt", "Papyrus"], player)
            or state.has_all(["Eyebrella", "Defeat Deerclops"], player)
        )

    def light_source (state: CollectionState) -> bool:
        if not state.has("Torch", player): return False
        if EXPERT_PLAYER_BIAS: return True
        return (
            (
                state.has_all(["Lantern", "Rope"], player) 
                and (CAVES_ENABLED or sea_fishing(state)) # Caves or Skittersquids
            )
            or state.has_all(["Miner Hat", "Rope", "Bug Net", "Straw Hat"], player) 
            or (
                ADVANCED_PLAYER_BIAS 
                and state.has_all(["Cut Stone", "Electrical Doodad"], player)
                and (
                    state.has("Morning Star", player) 
                    and ranged_aggression(state)  # Volt Goats 
                    and mining(state) # Nitre
                )
            )
        )
        
    def cave_exploration (state: CollectionState) -> bool:
        if EXPERT_PLAYER_BIAS: 
            return mining(state) and light_source(state) # Expert players just get a torch and pickaxe
        return ( 
            light_source(state)
            and basic_exploration(state) # Backpack and tools
            and base_making(state) # Have a base at this point
        )

    def ruins_exploration (state: CollectionState) -> bool:
        if not cave_exploration(state): return False
        if EXPERT_PLAYER_BIAS: return True
        return (
            advanced_combat(state) 
            or (healing(state) and basic_combat(state)) 
        ) and (
            basic_cooking(state) # Allow cooking for easy difficulty
            or ADVANCED_PLAYER_BIAS
        )

    def gears (state: CollectionState) -> bool:
        return ruins_exploration(state)

    def ruins_gems (state: CollectionState) -> bool:
        return (ruins_exploration(state) or state.has("Defeat Dragonfly", player))

    def purple_gem (state: CollectionState) -> bool:
        if not ruins_gems(state): return False
        return CRAFT_WITH_LOCKED_RECIPES or state.has("Purple Gem", player)
        
    def fire_suppression (state: CollectionState) -> bool:
        if not base_making(state): return False
        return (
            (gears(state) and state.has("Ice Flingomatic", player)) 
            or state.has_all(["Luxury Fan", "Defeat Moose/Goose"], player) 
            or state.has("Empty Watering Can", player)
        )

    def summer_survival (state: CollectionState) -> bool:
        if ADVANCED_PLAYER_BIAS: return True
        return (
            has_cooling_source(state) 
            and has_summer_insulation(state)
            and fire_suppression(state)
            and state.has_all(["Straw Hat", "Pretty Parasol", "Whirly Fan"], player) # Ensure basic stuff at this point
        )

    def character_switching (state: CollectionState) -> bool:
        if NO_UNLOCK_RECIPES_SHUFFLED:
            if not state.has_all(["Moon Rock Idol", "Portal Paraphernalia"], player):
                return False
        elif not state.has("Celestial Orb", player):
            return False
        return (
            state.has_all(["Cratered Moonrock"], player) # Crafting ingredient for moonrock portal
            and base_making(state) # Board and ropes requirement
            and purple_gem(state)
        )

    def bundling (state: CollectionState) -> bool:
        if EXPERT_PLAYER_BIAS: return True
        return state.has_all(["Bundling Wrap", "Rope"], player) and (
            state.has_all(["Wax Paper", "Beeswax"], player) 
            or state.has("Defeat Klaus", player) # Comes with waxpaper
        )

    def resurrecting (state: CollectionState) -> bool:
        return (
            (state.has("Life Giving Amulet", player) and gem_digging(state) and nightmare_fuel(state)) 
            or (state.has_all(["Meat Effigy", "Boards"], player) and chopping(state) and healing(state))
        )
        
    def leafy_meat (state: CollectionState) -> bool:
        return (
            reached_spring(state) # Lureplants
            or lunar_island(state) # Carrats
            or (ADVANCED_PLAYER_BIAS and cave_exploration(state)) # Carrats in lunar grotto
        )

    def farmplant_cooking (state: CollectionState) -> bool:
        return basic_cooking(state) and basic_farming(state)

    def egg_cooking (state: CollectionState) -> bool:
        return basic_cooking(state) and bird_caging(state)

    def sweet_cooking (state: CollectionState) -> bool:
        return basic_cooking(state) and honey_farming(state)

    def advanced_cooking (state: CollectionState) -> bool:
        return (
            basic_cooking(state) 
            and basic_farming(state) 
            and bird_caging(state)
            and honey_farming(state)
        )

    def advanced_farming (state: CollectionState) -> bool:
        return (
            basic_farming(state) 
            and digging(state) # Digging weeds and debris
            and state.has("Garden Digamajig", player) # Required even if we're Wormwood
            and (state.has("Empty Watering Can", player) or EXPERT_PLAYER_BIAS) # Waterballoons or rain
        )

    def canary (state: CollectionState) -> bool:
        return state.has_all(["Friendly Scarecrow", "Boards"], player) and basic_farming(state) # Pumpkin

    def cannon (state: CollectionState) -> bool: 
        return (
            state.has_all(["Queen of Moon Quay", "Cannon Kit", "Gunpowder", "Cut Stone", "Rope"], player) 
            and charcoal(state) # For gunpowder
            and mining(state) # Nitre for gunpowder
            and bird_caging(state) # Rotten eggs for gunpowder
        )

    def ranged_combat (state: CollectionState) -> bool:
        return (
            can_get_feathers(state) 
            and (
                state.has_all(["Reach Winter", "Blow Dart"], player) 
                or (canary(state) and bird_caging(state) and state.has("Electric Dart", player))
            )
        )

    def ranged_aggression (state: CollectionState) -> bool:
        if EXPERT_PLAYER_BIAS: return True # Chase them down or be creative
        return (
            state.has_all(["Boomerang", "Boards"], player) 
            or (
                can_get_feathers(state) 
                and (
                    state.has("Sleep Dart", player) or
                    (state.has("Fire Dart", player) and firestarting(state))
                )
            ) 
            or ranged_combat(state) 
            or ice_staff(state) 
            or fire_staff(state) 
            or cannon(state)
        )

    def dairy (state: CollectionState) -> bool: 
        return (
            state.has("Defeat Eye Of Terror", player) # Milky whites
            or (
                # Electric milk
                electric_insulation(state)
                and ranged_aggression(state) 
                and state.has_all(["Morning Star", "Electrical Doodad", "Cut Stone"], player)
            ) or (butter_luck(state) and ADVANCED_PLAYER_BIAS)
    )

    def weather_pain (state: CollectionState) -> bool:
        return state.has_all(["Weather Pain", "Defeat Moose/Goose"], player) and gears(state)
                    
    def dark_magic (state: CollectionState) -> bool:
        return (
            nightmare_fuel(state) 
            and (
                state.has("Dark Sword", player) 
                or (state.has("Bat Bat", player) and CAVES_ENABLED)
                or state.has_all(["Papyrus", "Night Armor"], player)
            )
        )

    def fencing (state: CollectionState) -> bool:
        return (
            base_making(state) 
            and state.has("Wood Gate", player) 
            and state.has_any(["Wood Fence", "Hay Wall", "Wood Wall", "Stone Wall"], player)
        )

    def beefalo_domestication (state: CollectionState) -> bool: 
        return (
            state.has_all(["Saddle", "Beefalo Hat", "Beefalo Bell"], player) 
            and (fencing(state) or EXPERT_PLAYER_BIAS)
        )

    def heavy_lifting (state: CollectionState) -> bool:
        return (
            beefalo_domestication(state) 
            or state.has_any(["Walter", "Wolfgang"], player) # Woby, mightiness
            or (state.has_all(["Wanda", "Reach Winter"], player) and purple_gem(state)) # Rift Watch
        )
            
    def basic_boating (state: CollectionState) -> bool:
        return (
            basic_exploration(state) 
            and state.has_all(["Boat Kit", "Boards", "Oar", "Grass Raft Kit", "Boat Patch"], player)
        )

    def autumn_survival (state: CollectionState) -> bool:
        if EXPERT_PLAYER_BIAS: return True
        return (
            cave_exploration(state) 
            and basic_boating(state) 
            and basic_combat(state)
        )

    def salt_crystals (state: CollectionState) -> bool:
        return (
            basic_boating(state) 
            and (basic_combat(state) or ADVANCED_PLAYER_BIAS)
            and mining(state)
        )

    def advanced_boating (state: CollectionState) -> bool:
        return (
            basic_boating(state) 
            and light_source(state) 
            and base_making(state) 
            and state.has_all(["Driftwood Oar", "Kelp Bumper Kit"], player)
            and (state.has_all(["Anchor Kit", "Steering Wheel Kit", "Mast Kit"], player) or EXPERT_PLAYER_BIAS)
        )

    def thulecite (state: CollectionState) -> bool:
        if NO_UNLOCK_RECIPES_SHUFFLED:
            if not state.has("Thulecite", player): return False
        if CAVES_ENABLED:
            return ruins_exploration(state)
        else:
            return advanced_boating(state) and hammering(state) and state.has("Pinchin' Winch", player) # Sunken chests
        
    def pick_axe (state: CollectionState) -> bool:
        if not thulecite(state): return False
        if NO_UNLOCK_RECIPES_SHUFFLED:
            return state.has_all(["Opulent Pickaxe", "Luxury Axe", "Pick/Axe", "Thulecite"], player)
        else:
            return state.has_all(["Opulent Pickaxe", "Luxury Axe"], player)

    def speed_boost (state: CollectionState) -> bool:
        return (
            state.has_all(["Walking Cane", "Reach Winter"], player)
            or (
                NO_UNLOCK_RECIPES_SHUFFLED 
                and thulecite(state) 
                and ruins_gems(state)
                and nightmare_fuel(state)
                and ((state.has_any if EXPERT_PLAYER_BIAS else state.has_all)(["Magiluminescence", "Thulecite Club"], player))
            )
        )

    def epic_combat (state: CollectionState) -> bool:
        if EXPERT_PLAYER_BIAS: 
            return advanced_boss_combat(state)
        return (
            advanced_boss_combat(state) 
            and state.has("Pan Flute", player) 
            and speed_boost(state) 
            and bundling(state)
            and character_switching(state) 
            and resurrecting(state)
        )

    def advanced_exploration (state: CollectionState) -> bool:
        if EXPERT_PLAYER_BIAS: return True
        return basic_exploration(state) and speed_boost(state)

    def late_game_survival (state: CollectionState) -> bool: 
        return (
            reached_autumn(state) 
            and advanced_boating(state) 
            and epic_combat(state) 
            and advanced_cooking(state) 
            and dark_magic(state)
        )
        
    def celestial_sanctum_pieces (state: CollectionState) -> bool:
        return thulecite(state) and state.has("Astral Detector", player) and heavy_lifting(state)

    def freshwater_fishing (state: CollectionState) -> bool:
        return state.has("Freshwater Fishing Rod", player)

    def sea_fishing (state: CollectionState) -> bool:
        return (
            (
                state.has_all(["Ocean Trawler Kit", "Rope", "Tin Fishin' Bin", "Cut Stone"], player) 
                or state.has("Sea Fishing Rod", player)
            ) 
            and basic_boating(state)
        )

    def fishing (state: CollectionState) -> bool:
        return freshwater_fishing(state) or sea_fishing(state)

    def shaving (state: CollectionState) -> bool:
        return state.has("Razor", player) or ADVANCED_PLAYER_BIAS

    def sea_cooking (state: CollectionState) -> bool:
        return (
            basic_cooking(state) 
            and sea_fishing(state) 
            and advanced_boating(state) 
            and shaving(state)
        )

    def lunar_island (state: CollectionState) -> bool:
        return (basic_boating(state) and ADVANCED_PLAYER_BIAS) or advanced_boating(state)

    def hermit_island (state: CollectionState) -> bool:
        return (
            basic_cooking(state)
            and base_making(state) 
            and (
                (basic_boating(state) and ADVANCED_PLAYER_BIAS) 
                or advanced_boating(state)
            )
        )
                            
    def hermit_sea_quests (state: CollectionState) -> bool:
        return (
            (ADVANCED_PLAYER_BIAS or advanced_boating(state)) 
            and sea_fishing(state)
        )

    def crab_king (state: CollectionState) -> bool:
        return (
            advanced_boating(state) 
            and state.count("Crabby Hermit Friendship", player) >= 10 
            and (weather_pain(state) or cannon(state) or EXPERT_PLAYER_BIAS) # Getting rid of sea stacks
        )

    def wall_building (state: CollectionState) -> bool:
        if EXPERT_PLAYER_BIAS: 
            if (
                (not NO_UNLOCK_RECIPES_SHUFFLED and ruins_exploration(state)) # Can otherwise make walls at ancient altar
                or (state.has("Thulecite Wall", player) and thulecite(state))
            ): 
                return True
        return (
            base_making(state) 
            and (state.has_all(["Stone Wall", "Potter's Wheel"], player)) # Sculptures are specifically pretty good for messing with mob pathfinding during moon stone event
        )
    def moonstone_event (state: CollectionState) -> bool:
        if not nightmare_fuel(state): return False # Required to make staff
        if NO_UNLOCK_RECIPES_SHUFFLED:
            if not state.has("Star Caller's Staff", player): return False
            if not ruins_gems(state): return False
        else:
            if not ruins_exploration(state): return False
        return (
            (wall_building(state) or EXPERT_PLAYER_BIAS) 
            and has_survived_num_days(11, state)
        )

    def iridescent_gem (state: CollectionState) -> bool:
        if NO_UNLOCK_RECIPES_SHUFFLED:
            return state.has_all(["Mooncaller Staff", "Deconstruction Staff"], player) and cave_exploration(state)
        else:
            return state.has("Mooncaller Staff", player) # Should already be able to craft Deconstruction Staff
        
    def archive_exploration (state: CollectionState) -> bool:
        return (
            iridescent_gem(state) 
            and (healing(state) or ADVANCED_PLAYER_BIAS)
        )

    def storm_protection (state: CollectionState) -> bool:
        return (
            state.has_all(["Fashion Goggles", "Desert Goggles"], player) 
            or (state.has("Astroggles", player) and basic_farming(state)) # Potato
        )

    def moonstorm_exploration (state: CollectionState) -> bool:
        return (
            state.has("Mysterious Energy", player) # Moonstorms have started
            and storm_protection(state)
            and electric_insulation(state) # Moongleams
        )
                            
    def celestial_champion (state: CollectionState) -> bool:
        return (
            moonstorm_exploration(state) # Getting materials for Incomplete Experiment
            and state.has_all(["Incomplete Experiment", "Celestial Orb"], player) 
            and epic_combat(state) 
            and (ranged_combat(state) or EXPERT_PLAYER_BIAS)
        )

    def shadow_pieces (state: CollectionState) -> bool:
        return (
            advanced_boss_combat(state) 
            and heavy_lifting(state) # Carrying suspicious marble
            and base_making(state) # Potter's wheel ingredients
            and state.has("Potter's Wheel", player) 
            and (state.has("Defeat Celestial Champion", player) or not state.has("Mysterious Energy", player)) # Can't happen during moonstorms
        )

    def ancient_fuelweaver (state: CollectionState) -> bool:
        if not state.has_all(["Shadow Atrium", "Ancient Key"], player): return False
        if EXPERT_PLAYER_BIAS: return advanced_combat(state)
        return (
            dark_magic(state) # Requires nightmare fuel
            and (state.has("Nightmare Amulet", player) or state.has_all(["The Lazy Explorer", "Walking Cane", "Reach Winter"], player)) # Getting around obelisks
            and (weather_pain(state) or state.has("Wendy", player)) # Dealing with woven shadows
        )

    def moon_quay_exploration (state: CollectionState) -> bool:
        if EXPERT_PLAYER_BIAS: return basic_boating(state)
        return (
            cannon(state) # Cannon already requires Queen of Moon Quay
            and ruins_exploration(state) # Bananas
        ) 

    def science_machine (state: CollectionState) -> bool:
        return state.has("Science Machine", player)

    def alchemy_engine (state: CollectionState) -> bool:
        return state.has("Alchemy Engine", player)

    def prestihatitor (state: CollectionState) -> bool:
        return state.has("Prestihatitor", player)

    def shadow_manipulator (state: CollectionState) -> bool:
        return state.has("Shadow Manipulator", player)

    def think_tank (state: CollectionState) -> bool:
        return state.has("Think Tank", player)

    def ancient_altar (state: CollectionState) -> bool:
        return ruins_exploration(state)

    def celestial_orb (state: CollectionState) -> bool:
        return state.has("Celestial Orb", player) or celestial_altar(state)

    def celestial_altar (state: CollectionState) -> bool:
        return lunar_island(state)

    def survival_goal (state: CollectionState) -> bool:
        if options.goal.current_key != "survival": return False # Only relevant if your goal is to survive
        days_to_survive = options.days_to_survive.value
        if days_to_survive < 20:
            return advanced_boss_combat(state) and cave_exploration(state) # Generic non-seasonal goal
        elif days_to_survive < 35:
            return reached_winter(state)
        elif days_to_survive < 55:
            return reached_spring(state)
        elif days_to_survive < 70:
            return reached_summer(state)
        elif days_to_survive < 90:
            return reached_autumn(state)
        return late_game_survival(state)

    rules_lookup: typing.Dict[str, typing.Dict[str, Callable[[CollectionState], bool]]] = {
        "regions": {
            "Cave": lambda state: CAVES_ENABLED, # Will mostly be used as a test
        },
        "locations": {
            # Events
            "Winter": lambda state: winter_survival(state),
            "Spring": lambda state: reached_winter(state) and spring_survival(state) and state.has("Defeat Deerclops", player),
            "Summer": lambda state: reached_spring(state) and summer_survival(state) and state.has("Defeat Moose/Goose", player),
            "Autumn": lambda state: reached_summer(state) and autumn_survival(state) and state.has("Defeat Antlion", player),
            "Late Game": lambda state: reached_autumn(state) and late_game_survival(state),
            "Survival Goal": lambda state: survival_goal(state),
            "Build Science Machine": lambda state: basic_survival(state) and chopping(state) and mining(state),
            "Build Alchemy Engine": lambda state: base_making(state) and state.has("Science Machine", player),
            "Build Prestihatitor": lambda state: state.has_all(["Top Hat", "Boards", "Science Machine", "Trap"], player),	
            "Build Shadow Manipulator": lambda state: ruins_exploration(state) and nightmare_fuel(state) and state.has("Prestihatitor", player),
            "Build Think Tank": lambda state: state.has_all(["Boards", "Science Machine"], player),	
            "Find Celestial Orb": lambda state: has_survived_num_days(5, state) and mining(state),
            "Moon Stone Event Reward": lambda state: moonstone_event(state),
            "Find Celestial Sanctum Icon": lambda state: celestial_sanctum_pieces(state),
            "Find Celestial Sanctum Ward": lambda state: celestial_sanctum_pieces(state),
            "Unite Celestial Altars": lambda state:
                state.has_all(["Celestial Sanctum Icon", "Celestial Sanctum Ward", "Inactive Celestial Tribute", "Pinchin' Winch"], player) 
                and lunar_island(state),
            "Will Get Accursed Trinket": lambda state: advanced_boating(state),
            "Kill Prime Mate": lambda state: basic_combat(state) and moon_quay_exploration(state) and hostile_flare(state),
            "Defeat Crab King with Pearl's Pearl": lambda state: crab_king(state),
            "Defeat Ancient Guardian": lambda state: ruins_exploration(state) and advanced_boss_combat(state),
            "Defeat Shadow Pieces": lambda state: shadow_pieces(state),
            "Defeat Deerclops": lambda state: basic_combat(state) and is_winter(state),
            "Defeat Moose/Goose": lambda state: basic_combat(state) and is_spring(state),
            "Defeat Antlion": lambda state: (freshwater_fishing(state) or advanced_boss_combat(state)) and is_summer(state) and storm_protection(state),
            "Defeat Bearger": lambda state: basic_combat(state) and reached_autumn(state),
            "Defeat Dragonfly": lambda state: advanced_boss_combat(state) and wall_building(state),
            "Defeat Bee Queen": lambda state: advanced_boss_combat(state) and hammering(state) and (state.has_all(["Beekeeper Hat", "Rope"], player) or ADVANCED_PLAYER_BIAS),
            "Defeat Klaus": lambda state: advanced_boss_combat(state) and is_winter(state),
            "Defeat Malbatross": lambda state: advanced_boss_combat(state) and advanced_boating(state),
            "Defeat Toadstool": lambda state: epic_combat(state) and cave_exploration(state) and dark_magic(state),
            "Defeat Ancient Fuelweaver": lambda state: ancient_fuelweaver(state),
            "Defeat Lord of the Fruit Flies": lambda state: basic_combat(state) and advanced_farming(state) and reached_spring(state),
            "Defeat Celestial Champion": lambda state: celestial_champion(state),
            "Defeat Eye Of Terror": lambda state: advanced_boss_combat(state),
            "Defeat Retinazor": lambda state: epic_combat(state),
            "Defeat Spazmatism": lambda state: epic_combat(state),
            "Defeat Nightmare Werepig": lambda state: epic_combat(state) and pick_axe(state),
            "Defeat Scrappy Werepig": lambda state: state.has("Defeat Nightmare Werepig", player),
            "Defeat Frostjaw": lambda state: advanced_boating(state) and advanced_boss_combat(state) and speed_boost(state) and state.has("Sea Fishing Rod", player),

            # Pearl Questline
            "Hermit Home Upgrade (1)": lambda state: hermit_island(state) and bug_catching(state), # Cookie cutters, boards, fireflies
            "Hermit Home Upgrade (2)": lambda state: hermit_island(state), # Marble, cut stone, light bulb
            "Hermit Home Upgrade (3)": lambda state: hermit_island(state) and state.has("Floorings", player), # Moonrock, rope, carpet
            "Hermit Island Drying Racks": lambda state: hermit_island(state),
            "Hermit Island Plant 10 Flowers": lambda state: hermit_island(state) and bug_catching(state),
            "Hermit Island Plant 8 Berry Bushes": lambda state: hermit_island(state) and digging(state),
            "Hermit Island Clear Underwater Salvageables": lambda state: hermit_sea_quests(state) and state.has("Pinchin' Winch", player),
            "Hermit Island Kill Lureplant": lambda state: hermit_island(state) and reached_spring(state),
            "Hermit Island Build Wooden Chair": lambda state: hermit_island(state) and state.has("Sawhorse", player),
            "Give Crabby Hermit Umbrella": lambda state: hermit_island(state) and is_spring(state) and state.has_any(["Umbrella", "Pretty Parasol"], player),
            "Give Crabby Hermit Warm Clothing": lambda state: hermit_island(state) and is_winter (state) and state.has_any(["Breezy Vest", "Puffy Vest"], player),
            "Give Crabby Hermit Flower Salad": lambda state: hermit_island(state) and is_summer(state),
            "Give Crabby Hermit Fallounder": lambda state: hermit_sea_quests(state) and is_autumn(state),
            "Give Crabby Hermit Bloomfin Tuna": lambda state: hermit_sea_quests(state) and is_spring(state),
            "Give Crabby Hermit Scorching Sunfish": lambda state: hermit_sea_quests(state) and is_summer(state),
            "Give Crabby Hermit Ice Bream": lambda state: hermit_sea_quests(state) and is_winter(state),
            "Give Crabby Hermit 5 Heavy Fish": lambda state: hermit_sea_quests(state),

            # Tasks
            "Distilled Knowledge (Yellow)": lambda state: archive_exploration(state),
            "Distilled Knowledge (Blue)": lambda state: archive_exploration(state),
            "Distilled Knowledge (Red)": lambda state: archive_exploration(state),
            "Wagstaff during Moonstorm": lambda state: moonstorm_exploration(state),
            "Queen of Moon Quay": lambda state: moon_quay_exploration(state),
            "Pig King": lambda state: has_survived_num_days(4, state),      
            "Chester": lambda state: has_survived_num_days(8, state),       
            "Hutch": lambda state: cave_exploration(state),         
            "Stagehand": lambda state: basic_survival(state) and hammering(state),     
            "Pirate Stash": lambda state: state.has("Pirate Map", player) and digging(state),  
            "Moon Stone Event": lambda state: state.has("Mooncaller Staff", player),
            "Oasis": lambda state: is_summer(state) and freshwater_fishing(state),
            "Poison Birchnut Tree": lambda state: reached_autumn(state) and chopping(state),
            "W.O.B.O.T.": lambda state: state.has("Defeat Scrappy Werepig", player) or state.has_all(["Auto-Mat-O-Chanic", "Cut Stone", "Electrical Doodad"], player),
            "Friendly Fruit Fly": lambda state: state.has("Defeat Lord of the Fruit Flies", player),

            # Bosses
            "Deerclops": lambda state: state.has("Defeat Deerclops", player),
            "Moose/Goose": lambda state: state.has("Defeat Moose/Goose", player),
            "Antlion": lambda state: state.has("Defeat Antlion", player),
            "Bearger": lambda state: state.has("Defeat Bearger", player),
            "Ancient Guardian": lambda state: state.has("Ancient Key", player),
            "Dragonfly": lambda state: state.has("Defeat Dragonfly", player),
            "Bee Queen": lambda state: state.has("Defeat Bee Queen", player),
            "Crab King": lambda state: state.has("Inactive Celestial Tribute", player),
            "Klaus": lambda state: state.has("Defeat Klaus", player),
            "Malbatross": lambda state: state.has("Defeat Malbatross", player),
            "Toadstool": lambda state: state.has("Defeat Toadstool", player),
            "Shadow Bishop": lambda state: state.has("Shadow Atrium", player),
            "Shadow Knight": lambda state: state.has("Shadow Atrium", player),
            "Shadow Rook": lambda state: state.has("Shadow Atrium", player),
            "Ancient Fuelweaver": lambda state: state.has("Defeat Ancient Fuelweaver", player),
            "Lord of the Fruit Flies": lambda state: state.has("Defeat Lord of the Fruit Flies", player),
            "Celestial Champion": lambda state: state.has("Defeat Celestial Champion", player),
            "Eye Of Terror": lambda state: state.has("Defeat Eye Of Terror", player),
            "Retinazor": lambda state: state.has("Defeat Retinazor", player),
            "Spazmatism": lambda state: state.has("Defeat Spazmatism", player),
            "Nightmare Werepig": lambda state: state.has("Defeat Nightmare Werepig", player),
            "Scrappy Werepig": lambda state: state.has("Defeat Scrappy Werepig", player),
            "Frostjaw": lambda state: state.has("Defeat Frostjaw", player),

            # Creatures
            "Batilisk": lambda state: pre_basic_combat(state) and mining(state),
            "Bee": lambda state: pre_basic_combat(state) or bug_catching(state),
            "Beefalo": lambda state: basic_survival(state),
            "Clockwork Bishop": lambda state: advanced_combat(state) and (healing(state) or ADVANCED_PLAYER_BIAS),
            "Bunnyman": lambda state: basic_combat(state) and cave_exploration(state),
            "Butterfly": lambda state: True,
            "Buzzard": lambda state: basic_combat(state),
            "Canary": lambda state: canary(state) and can_get_feathers(state),
            "Carrat": lambda state: lunar_island(state),
            "Catcoon": lambda state: basic_survival(state),
            "Cookie Cutter": lambda state: advanced_boating(state),
            "Crawling Horror": lambda state: advanced_combat(state),
            "Crow": lambda state: can_get_feathers(state),
            "Red Hound": lambda state: basic_combat(state) and is_summer(state),
            "Frog": lambda state: pre_basic_combat(state),
            "Saladmander": lambda state: lunar_island(state),
            "Ghost": lambda state: basic_exploration(state) and digging(state),
            "Gnarwail": lambda state: basic_combat(state) and advanced_boating(state),
            "Grass Gator": lambda state: basic_combat(state) and advanced_boating(state) and ranged_aggression(state),
            "Grass Gekko": lambda state: desert_exploration(state) and reached_spring(state), # Not guaranteed on world gen so give time for spawned ones
            "Briar Wolf": lambda state: basic_combat(state),
            "Hound": lambda state: basic_combat(state) and desert_exploration(state),
            "Blue Hound": lambda state: basic_combat(state) and is_winter(state),
            "Killer Bee": lambda state: pre_basic_combat(state),
            "Clockwork Knight": lambda state: advanced_combat(state),
            "Koalefant": lambda state: pre_basic_combat(state) and ranged_aggression(state),
            "Krampus": lambda state: basic_combat(state) and can_get_feathers(state) and has_survived_num_days(11, state),
            "Treeguard": lambda state: basic_combat(state) and has_survived_num_days(10, state) and chopping(state),
            "Crustashine": lambda state: moon_quay_exploration(state) and ranged_aggression(state),
            "Bulbous Lightbug": lambda state: cave_exploration(state),
            "Volt Goat": lambda state: basic_combat(state) and ranged_aggression(state) and desert_exploration(state),
            "Merm": lambda state: basic_combat(state) and swamp_exploration(state),
            "Moleworm": lambda state: True,
            "Naked Mole Bat": lambda state: basic_combat(state) and cave_exploration(state),
            "Splumonkey": lambda state: ruins_exploration(state),
            "Moon Moth": lambda state: lunar_island(state),
            "Mosquito": lambda state: swamp_exploration(state) and (pre_basic_combat(state) or bug_catching(state)),
            "Mosling": lambda state: basic_combat(state) and is_spring(state),
            "Mush Gnome": lambda state: basic_combat(state) and cave_exploration(state),
            "Terrorclaw": lambda state: advanced_combat(state) and advanced_boating(state),
            "Pengull": lambda state: basic_combat(state) and is_winter(state),
            "Gobbler": lambda state: basic_exploration(state),
            "Pig Man": lambda state: basic_survival(state),
            "Powder Monkey": lambda state: basic_combat(state) and moon_quay_exploration(state),
            "Prime Mate": lambda state: state.has("Pirate Map", player),
            "Puffin": lambda state: can_get_feathers(state),
            "Rabbit": lambda state: True,
            "Redbird": lambda state: can_get_feathers(state),
            "Snowbird": lambda state: can_get_feathers(state) and is_winter(state),
            "Rock Lobster": lambda state: advanced_combat(state) and cave_exploration(state),
            "Clockwork Rook": lambda state: advanced_combat(state) and (healing(state) or ADVANCED_PLAYER_BIAS),
            "Rockjaw": lambda state: advanced_combat(state) and advanced_boating(state) and (ranged_combat(state) or cannon(state)),
            "Slurper": lambda state: ruins_exploration(state),
            "Slurtle": lambda state: cave_exploration(state) and (firestarting(state) or basic_combat(state)),
            "Snurtle": lambda state: cave_exploration(state) and (firestarting(state) or basic_combat(state)),
            "Ewecus": lambda state: advanced_combat(state) and advanced_exploration(state) and reached_autumn(state),
            "Spider": lambda state: True,
            "Dangling Depth Dweller": lambda state: ruins_exploration(state),
            "Cave Spider": lambda state: basic_combat(state) and cave_exploration(state),
            "Nurse Spider": lambda state: advanced_combat(state) and reached_spring(state),
            "Shattered Spider": lambda state: basic_combat(state) and lunar_island(state),
            "Spitter": lambda state: basic_combat(state) and cave_exploration(state),
            "Spider Warrior": lambda state: basic_combat(state),
            "Sea Strider": lambda state: basic_combat(state) and advanced_boating(state),
            "Spider Queen": lambda state: advanced_combat(state) and reached_spring(state),
            "Tallbird": lambda state: basic_combat(state) and healing(state),
            "Tentacle": lambda state: basic_combat(state) and swamp_exploration(state),
            "Big Tentacle": lambda state: advanced_combat(state) and cave_exploration(state) and healing(state),
            "Terrorbeak": lambda state: advanced_combat(state),
            "MacTusk": lambda state: basic_combat(state) and reached_winter(state),
            "Varg": lambda state: advanced_combat(state) and advanced_exploration(state) and reached_autumn(state),
            "Varglet": lambda state: basic_combat(state) and advanced_exploration(state) and reached_spring(state),
            "Depths Worm": lambda state: ruins_exploration(state),
            "Ancient Sentrypede": lambda state: archive_exploration(state) and advanced_combat(state),
            "Skittersquid": lambda state: basic_combat(state) and advanced_boating(state),
            "Lure Plant": lambda state: reached_spring(state),
            "Glommer": lambda state: has_survived_num_days(11, state),
            "Dust Moth": lambda state: archive_exploration(state),
            "No-Eyed Deer": lambda state: is_winter(state),     
            "Moonblind Crow": lambda state: moonstorm_exploration(state) and basic_combat(state),
            "Misshapen Bird": lambda state: moonstorm_exploration(state) and basic_combat(state),
            "Moonrock Pengull": lambda state: lunar_island(state) and is_winter(state) and basic_combat(state), 
            "Horror Hound": lambda state: moonstorm_exploration(state) and basic_combat(state),
            "Resting Horror": lambda state: ruins_exploration(state),
            "Birchnutter": lambda state: reached_autumn(state) and chopping(state),
            "Mandrake": lambda state: basic_survival(state),
            "Fruit Fly": lambda state: basic_farming(state) and reached_spring(state),
            
            # Cook foods
            "Butter Muffin": lambda state: pre_basic_cooking(state),
            "Froggle Bunwich": lambda state: pre_basic_cooking(state),
            "Taffy": lambda state: sweet_cooking(state),
            "Pumpkin Cookies": lambda state: advanced_cooking(state),
            "Stuffed Eggplant": lambda state: farmplant_cooking(state),
            "Fishsticks": lambda state: basic_cooking(state) and fishing(state),
            "Honey Nuggets": lambda state: sweet_cooking(state),
            "Honey Ham": lambda state: sweet_cooking(state),
            "Dragonpie": lambda state: farmplant_cooking(state) or (basic_cooking(state) and lunar_island(state)),
            "Kabobs": lambda state: pre_basic_cooking(state),
            "Mandrake Soup": lambda state: basic_cooking(state),
            "Bacon and Eggs": lambda state: egg_cooking(state),
            "Meatballs": lambda state: pre_basic_cooking(state),
            "Meaty Stew": lambda state: pre_basic_cooking(state),
            "Pierogi": lambda state: egg_cooking(state),
            "Turkey Dinner": lambda state: basic_cooking(state) and basic_combat(state),
            "Ratatouille": lambda state: pre_basic_cooking(state),
            "Fist Full of Jam": lambda state: pre_basic_cooking(state),
            "Fruit Medley": lambda state: farmplant_cooking(state),
            "Fish Tacos": lambda state: farmplant_cooking(state) and fishing(state),
            "Waffles": lambda state: egg_cooking(state) and butter_luck(state),
            "Monster Lasagna": lambda state: basic_cooking(state),
            "Powdercake": lambda state: advanced_cooking(state),
            "Unagi": lambda state: basic_cooking(state) and cave_exploration(state) and freshwater_fishing(state),
            "Wet Goop": lambda state: basic_cooking(state),
            "Flower Salad": lambda state: basic_cooking(state) and is_summer(state),
            "Ice Cream": lambda state: basic_cooking(state) and dairy(state),
            "Melonsicle": lambda state: farmplant_cooking(state),
            "Trail Mix": lambda state: basic_cooking(state),
            "Spicy Chili": lambda state: basic_cooking(state),
            "Guacamole": lambda state: basic_cooking(state),
            "Jellybeans": lambda state: basic_cooking(state) and state.has("Defeat Bee Queen", player),
            "Fancy Spiralled Tubers": lambda state: farmplant_cooking(state),
            "Creamy Potato Purée": lambda state: farmplant_cooking(state),
            "Asparagus Soup": lambda state: farmplant_cooking(state),
            "Vegetable Stinger": lambda state: farmplant_cooking(state),
            "Banana Pop": lambda state: basic_cooking(state) and (cave_exploration(state) or moon_quay_exploration(state)),
            "Frozen Banana Daiquiri": lambda state: basic_cooking(state) and (cave_exploration(state) or moon_quay_exploration(state)),
            "Banana Shake": lambda state: basic_cooking(state) and (cave_exploration(state) or moon_quay_exploration(state)),
            "Ceviche": lambda state: sea_cooking(state),
            "Salsa Fresca": lambda state: farmplant_cooking(state),
            "Stuffed Pepper Poppers": lambda state: farmplant_cooking(state),
            "California Roll": lambda state: sea_cooking(state),
            "Seafood Gumbo": lambda state: basic_cooking(state) and cave_exploration(state),
            "Surf 'n' Turf": lambda state: sea_cooking(state),
            "Lobster Bisque": lambda state: basic_cooking(state) and sea_fishing(state),
            "Lobster Dinner": lambda state: basic_cooking(state) and sea_fishing(state) and butter_luck(state),
            "Barnacle Pita": lambda state: sea_cooking(state) and shaving(state),
            "Barnacle Nigiri": lambda state: sea_cooking(state) and shaving(state),
            "Barnacle Linguine": lambda state: sea_cooking(state) and shaving(state),
            "Stuffed Fish Heads": lambda state: sea_cooking(state) and shaving(state),
            "Leafy Meatloaf": lambda state: basic_cooking(state) and leafy_meat(state),
            "Veggie Burger": lambda state: farmplant_cooking(state) and leafy_meat(state),
            "Jelly Salad": lambda state: sweet_cooking(state) and leafy_meat(state),
            "Beefy Greens": lambda state: farmplant_cooking(state) and leafy_meat(state),
            "Mushy Cake": lambda state: basic_cooking(state) and cave_exploration(state),
            "Soothing Tea": lambda state: farmplant_cooking(state),
            "Fig-Stuffed Trunk": lambda state: sea_cooking(state),
            "Figatoni": lambda state: sea_cooking(state),
            "Figkabab": lambda state: sea_cooking(state),
            "Figgy Frogwich": lambda state: sea_cooking(state),
            "Bunny Stew": lambda state: basic_cooking(state),
            "Plain Omelette": lambda state: egg_cooking(state),
            "Breakfast Skillet": lambda state: egg_cooking(state),
            "Tall Scotch Eggs": lambda state: basic_cooking(state) and basic_combat(state),
            "Steamed Twigs": lambda state: basic_cooking(state),
            "Beefalo Treats": lambda state: farmplant_cooking(state),
            "Milkmade Hat": lambda state: basic_cooking(state) and cave_exploration(state) and basic_boating(state) and dairy(state),
            "Amberosia": lambda state: basic_cooking(state) and salt_crystals(state) and state.has("Collected Dust", player),
            "Stuffed Night Cap": lambda state: basic_cooking(state) and cave_exploration(state),
            # Warly Dishes
            "Grim Galette": lambda state: farmplant_cooking(state),
            "Volt Goat Chaud-Froid": lambda state: basic_cooking(state) and basic_combat(state),
            "Glow Berry Mousse": lambda state: basic_cooking(state) and cave_exploration(state),
            "Fish Cordon Bleu": lambda state: sea_cooking(state),
            "Hot Dragon Chili Salad": lambda state: farmplant_cooking(state),
            "Asparagazpacho": lambda state: farmplant_cooking(state),
            "Puffed Potato Soufflé": lambda state: advanced_cooking(state),
            "Monster Tartare": lambda state: basic_cooking(state),
            "Fresh Fruit Crepes": lambda state: farmplant_cooking(state) and butter_luck(state),
            "Bone Bouillon": lambda state: farmplant_cooking(state) and hammering(state),
            "Moqueca": lambda state: farmplant_cooking(state) and sea_cooking(state),
            # Farming 
            "Grow Giant Asparagus": lambda state: is_winter(state) or is_spring(state),
            "Grow Giant Garlic": lambda state: reached_winter(state),
            "Grow Giant Pumpkin": lambda state: is_winter(state) or reached_autumn(state),
            "Grow Giant Corn": lambda state: reached_spring(state),
            "Grow Giant Onion": lambda state: reached_spring(state),
            "Grow Giant Potato": lambda state: reached_winter(state),
            "Grow Giant Dragon Fruit": lambda state: reached_spring(state),
            "Grow Giant Pomegranate": lambda state: reached_spring(state),
            "Grow Giant Eggplant": lambda state: reached_spring(state),
            "Grow Giant Toma Root": lambda state: reached_spring(state),
            "Grow Giant Watermelon": lambda state: reached_spring(state),
            "Grow Giant Pepper": lambda state: reached_summer(state),
            "Grow Giant Durian": lambda state: reached_spring(state),
            "Grow Giant Carrot": lambda state: reached_winter(state),
            # Research
            "Science (Nitre)": lambda state: mining(state),			
            "Science (Salt Crystals)": lambda state: salt_crystals(state),	
            "Science (Ice)": lambda state: mining(state),				
            "Science (Slurtle Slime)": lambda state: cave_exploration(state),		
            "Science (Gears)": lambda state: ruins_exploration(state),					
            "Science (Scrap)": lambda state: basic_exploration(state),					
            "Science (Azure Feather)": lambda state: reached_winter(state) and can_get_feathers(state),	
            "Science (Crimson Feather)": lambda state: can_get_feathers(state),	
            "Science (Jet Feather)": lambda state: can_get_feathers(state),	
            "Science (Saffron Feather)": lambda state: canary(state) and can_get_feathers(state),	
            "Science (Kelp Fronds)": lambda state: basic_boating(state),		
            "Science (Steel Wool)": lambda state: advanced_combat(state) and advanced_exploration(state) and reached_autumn(state),			
            "Science (Electrical Doodad)": lambda state: state.has_all(["Electrical Doodad", "Cut Stone"], player) and mining(state),
            "Science (Ashes)": lambda state: firestarting(state),			
            "Science (Cut Grass)": lambda state: True,		
            "Science (Beefalo Horn)": lambda state: basic_combat(state) and has_survived_num_days(15, state),		
            "Science (Beefalo Wool)": lambda state: basic_combat(state) and shaving(state),		
            "Science (Cactus Flower)": lambda state: is_summer(state),		
            "Science (Honeycomb)": lambda state: basic_combat(state),			
            "Science (Petals)": lambda state: True,				
            "Science (Succulent)": lambda state: desert_exploration(state),			
            "Science (Foliage)": lambda state: (CAVES_ENABLED and mining(state)) or desert_exploration(state),				
            "Science (Tillweeds)": lambda state: basic_farming(state) and has_survived_num_days(15, state),	
            "Science (Lichen)": lambda state: ruins_exploration(state),	
            "Science (Banana)": lambda state: moon_quay_exploration(state) or ruins_exploration(state),			
            "Science (Fig)": lambda state: advanced_boating(state),			
            "Science (Tallbird Egg)": lambda state: basic_combat(state),
            "Science (Hound's Tooth)": lambda state: basic_combat(state),					
            "Science (Bone Shards)": lambda state: desert_exploration(state) and hammering(state),					
            "Science (Walrus Tusk)": lambda state: basic_combat(state) and is_winter(state),
            "Science (Silk)": lambda state: True,			
            "Science (Cut Stone)": lambda state: state.has("Cut Stone", player) and mining(state),
            "Science (Palmcone Sprout)": lambda state: moon_quay_exploration(state),	
            "Science (Pine Cone)": lambda state: chopping(state),			
            "Science (Birchnut)": lambda state: chopping(state),				
            "Science (Driftwood Piece)": lambda state: basic_boating(state),		
            "Science (Cookie Cutter Shell)": lambda state: basic_boating(state) and basic_combat(state),	
            "Science (Palmcone Scale)": lambda state: moon_quay_exploration(state),
            "Science (Gnarwail Horn)": lambda state: advanced_boating(state) and basic_combat(state),	
            "Science (Barnacles)": lambda state: sea_cooking(state) and shaving(state),			
            "Science (Frazzled Wires)": lambda state: ruins_exploration(state),	
            "Science (Charcoal)": lambda state: firestarting(state) and chopping(state),			
            "Science (Butter)": lambda state: butter_luck(state),				
            "Science (Asparagus)": lambda state: basic_farming(state) and has_survived_num_days(15, state) and reached_winter(state),			
            "Science (Garlic)": lambda state: basic_farming(state) and has_survived_num_days(15, state),				
            "Science (Pumpkin)": lambda state: basic_farming(state) and has_survived_num_days(15, state),			
            "Science (Corn)": lambda state: basic_farming(state) and has_survived_num_days(15, state),				
            "Science (Onion)": lambda state: basic_farming(state) and has_survived_num_days(15, state),				
            "Science (Potato)": lambda state: basic_farming(state) and has_survived_num_days(15, state),				
            "Science (Dragon Fruit)": lambda state: (basic_farming(state) and has_survived_num_days(15, state)) or lunar_island(state),				
            "Science (Pomegranate)": lambda state: basic_farming(state) and has_survived_num_days(15, state) and reached_spring(state),		
            "Science (Eggplant)": lambda state: basic_farming(state) and has_survived_num_days(15, state),			
            "Science (Toma Root)": lambda state: basic_farming(state) and has_survived_num_days(15, state),				
            "Science (Watermelon)": lambda state: basic_farming(state) and has_survived_num_days(15, state) and reached_spring(state),		
            "Science (Pepper)": lambda state: basic_farming(state) and has_survived_num_days(15, state),				
            "Science (Durian)": lambda state: basic_farming(state) and has_survived_num_days(15, state) and reached_spring(state),				
            "Science (Carrot)": lambda state: True,				
            "Science (Stone Fruit)": lambda state: lunar_island(state),		
            "Magic (Blue Gem)": lambda state: gem_digging(state),
            "Magic (Living Log)": lambda state: chopping(state) or state.has("Wormwood", player),				
            "Magic (Glommer's Goop)": lambda state: has_survived_num_days(11, state),
            "Magic (Dark Petals)": lambda state: True,				
            "Magic (Red Gem)": lambda state: gem_digging(state),
            "Magic (Slurper Pelt)": lambda state: ruins_exploration(state),				
            "Magic (Blue Spore)": lambda state: is_winter(state) and cave_exploration(state) and bug_catching(state),
            "Magic (Red Spore)": lambda state: is_summer(state) and cave_exploration(state) and bug_catching(state),					
            "Magic (Green Spore)": lambda state: is_spring(state) and cave_exploration(state) and bug_catching(state),				
            "Magic (Broken Shell)": lambda state: cave_exploration(state),				
            "Magic (Leafy Meat)": lambda state: leafy_meat(state),				
            "Magic (Canary (Volatile))": lambda state: canary(state) and cave_exploration(state) and bird_caging(state),		
            "Magic (Life Giving Amulet)": lambda state: state.has("Life Giving Amulet", player) and gem_digging(state) and nightmare_fuel(state),			
            "Magic (Nightmare Fuel)": lambda state: basic_combat(state) and nightmare_fuel(state),			
            "Magic (Cut Reeds)": lambda state: swamp_exploration(state),					
            "Magic (Volt Goat Horn)": lambda state: basic_combat(state),			
            "Magic (Beard Hair)": lambda state: True,				
            "Magic (Glow Berry)": lambda state: ruins_exploration(state),								
            "Magic (Tentacle Spots)": lambda state: basic_combat(state),			
            "Magic (Health)": lambda state: healing(state),					
            "Magic (Sanity)": lambda state: True,					
            "Magic (Telltale Heart)": lambda state: healing(state) and state.has("Telltale Heart", player),					
            "Magic (Forget-Me-Lots)": lambda state: basic_farming(state),			
            "Magic (Cat Tail)": lambda state: pre_basic_combat(state),					
            "Magic (Bunny Puff)": lambda state: cave_exploration(state) and basic_combat(state),		
            "Magic (Mosquito Sack)": lambda state: swamp_exploration(state),						
            "Magic (Spider Gland)": lambda state: True,				
            "Magic (Monster Jerky)": lambda state: state.has_all(["Drying Rack", "Rope"], player) and firestarting(state),				
            "Magic (Pig Skin)": lambda state: basic_combat(state),					
            "Magic (Batilisk Wing)": lambda state: mining(state),				
            "Magic (Stinger)": lambda state: True,					
            "Magic (Papyrus)": lambda state: state.has("Papyrus", player) and swamp_exploration(state),		
            "Magic (Green Cap)": lambda state: True,				
            "Magic (Blue Cap)": lambda state: True,					
            "Magic (Red Cap)": lambda state: True,						
            "Magic (Iridescent Gem)": lambda state: iridescent_gem(state),			
            "Magic (Desert Stone)": lambda state: reached_summer(state) and storm_protection(state),		
            "Magic (Naked Nostrils)": lambda state: cave_exploration(state),			
            "Magic (Frog Legs)": lambda state: pre_basic_combat(state),		
            "Magic (Spoiled Fish)": lambda state: sea_fishing(state) and has_survived_num_days(15, state),	
            "Magic (Spoiled Fish Morsel)": lambda state: fishing(state) and  has_survived_num_days(10, state),
            "Magic (Rot)": lambda state: has_survived_num_days(15, state),				
            "Magic (Rotten Egg)": lambda state: advanced_cooking(state) and has_survived_num_days(20, state),		
            "Magic (Carrat)": lambda state: lunar_island(state),				
            "Magic (Moleworm)": lambda state: hammering(state),		
            "Magic (Fireflies)": lambda state: bug_catching(state),
            "Magic (Bulbous Lightbug)": lambda state: cave_exploration(state) and bug_catching(state),			
            "Magic (Rabbit)": lambda state: state.has("Trap", player),	
            "Magic (Butterfly)": lambda state: bug_catching(state),			
            "Magic (Mosquito)": lambda state: bug_catching(state),		
            "Magic (Bee)": lambda state: bug_catching(state),					
            "Magic (Killer Bee)": lambda state: bug_catching(state),	
            "Magic (Crustashine)": lambda state: moon_quay_exploration(state),				
            "Magic (Crow)": lambda state: state.has("Bird Trap", player),						
            "Magic (Redbird)": lambda state: state.has("Bird Trap", player),					
            "Magic (Snowbird)": lambda state: state.has("Bird Trap", player) and is_winter(state),					
            "Magic (Canary)": lambda state: state.has("Bird Trap", player) and canary(state),								
            "Magic (Puffin)": lambda state: state.has("Bird Trap", player) and basic_boating(state),											
            "Think Tank (Freshwater Fish)": lambda state: freshwater_fishing(state),
            "Think Tank (Live Eel)": lambda state: cave_exploration(state) and freshwater_fishing(state),
            "Think Tank (Runty Guppy)": lambda state: sea_fishing(state),
            "Think Tank (Needlenosed Squirt)": lambda state: sea_fishing(state),
            "Think Tank (Bitty Baitfish)": lambda state: sea_fishing(state),
            "Think Tank (Smolt Fry)": lambda state: sea_fishing(state),
            "Think Tank (Popperfish)": lambda state: sea_fishing(state),
            "Think Tank (Fallounder)": lambda state: advanced_boating(state) and sea_fishing(state),
            "Think Tank (Bloomfin Tuna)": lambda state: reached_spring(state) and sea_fishing(state),
            "Think Tank (Scorching Sunfish)": lambda state: advanced_boating(state) and reached_summer(state) and sea_fishing(state),
            "Think Tank (Spittlefish)": lambda state: advanced_boating(state) and sea_fishing(state),
            "Think Tank (Mudfish)": lambda state: sea_fishing(state),
            "Think Tank (Deep Bass)": lambda state: advanced_boating(state) and sea_fishing(state),
            "Think Tank (Dandy Lionfish)": lambda state: advanced_boating(state) and sea_fishing(state),
            "Think Tank (Black Catfish)": lambda state: advanced_boating(state) and sea_fishing(state),
            "Think Tank (Corn Cod)": lambda state: advanced_boating(state) and sea_fishing(state),
            "Think Tank (Ice Bream)": lambda state: advanced_boating(state) and reached_winter(state) and sea_fishing(state),
            "Think Tank (Sweetish Fish)": lambda state: advanced_boating(state) and sea_fishing(state),
            "Think Tank (Wobster)": lambda state: advanced_boating(state) and sea_fishing(state),
            "Think Tank (Lunar Wobster)": lambda state: lunar_island(state) and sea_fishing(state),
            "Pseudoscience (Purple Gem)": lambda state: True,		
            "Pseudoscience (Yellow Gem)": lambda state: True,
            "Pseudoscience (Thulecite)": lambda state: thulecite(state),
            "Pseudoscience (Orange Gem)": lambda state: True,		
            "Pseudoscience (Green Gem)": lambda state: True,			
            "Celestial (Moon Rock)": lambda state: True,				
            "Celestial (Moon Shard)": lambda state: cave_exploration(state) or lunar_island(state),
            "Celestial (Moon Shroom)": lambda state: cave_exploration(state),					
            "Celestial (Moon Moth)": lambda state: bug_catching(state),		
            "Celestial (Lune Tree Blossom)": lambda state: lunar_island(state),			
            "Bottle Exchange (1)": lambda state: state.count("Crabby Hermit Friendship", player) >= 1,
            "Bottle Exchange (2)": lambda state: state.count("Crabby Hermit Friendship", player) >= 1,
            "Bottle Exchange (3)": lambda state: state.count("Crabby Hermit Friendship", player) >= 3,
            "Bottle Exchange (4)": lambda state: state.count("Crabby Hermit Friendship", player) >= 3,
            "Bottle Exchange (5)": lambda state: state.count("Crabby Hermit Friendship", player) >= 3,
            "Bottle Exchange (6)": lambda state: state.count("Crabby Hermit Friendship", player) >= 6,
            "Bottle Exchange (7)": lambda state: state.count("Crabby Hermit Friendship", player) >= 6,
            "Bottle Exchange (8)": lambda state: state.count("Crabby Hermit Friendship", player) >= 8,
            "Bottle Exchange (9)": lambda state: state.count("Crabby Hermit Friendship", player) >= 8,
            "Bottle Exchange (10)": lambda state: state.count("Crabby Hermit Friendship", player) >= 8,
        },
    }
    
    EXISTING_LOCATIONS = [item.name for item in multiworld.get_locations(player)]
    SEASON_HELPER_ITEMS = [name for name, data in item_data_table.items() if "seasonhelper" in data.tags]
    excluded = set()
    PROGRESSION_REQUIRED_BOSSES:set = set()

    if options.goal.current_key != "survival":
        excluded.update(options.required_bosses.value) # Prevent goal bosses from having progression items
        PROGRESSION_REQUIRED_BOSSES.update(options.required_bosses.value) 
        if "Ancient Fuelweaver" in PROGRESSION_REQUIRED_BOSSES: PROGRESSION_REQUIRED_BOSSES.add("Ancient Guardian")
        if "Celestial Champion" in PROGRESSION_REQUIRED_BOSSES: PROGRESSION_REQUIRED_BOSSES.add("Crab King")
        if "Scrappy Werepig" in PROGRESSION_REQUIRED_BOSSES: PROGRESSION_REQUIRED_BOSSES.add("Nightmare Werepig")
        
    PRIORITY_TAGS = {
        "Ancient Fuelweaver": "priority_fuelweaver_boss",
        "Celestial Champion": "priority_celestial_boss",
        "Ancient Guardian": "priority_ruins_boss",
        "Crab King": "priority_crabking_boss",
        "Nightmare Werepig": "priority_ruins_boss",
        "Scrappy Werepig": "priority_scrappywerepig_boss",
        "Antlion": "priority_antlion_boss",
    }

    # Set location rules
    for location_name, rule in rules_lookup["locations"].items():
        if location_name in EXISTING_LOCATIONS:
            location = multiworld.get_location(location_name, player)
            required = False

            # Set the rule
            set_rule(location, rule)

            # Skip event locations
            if not location_name in location_data_table: continue

            location_data = location_data_table[location_name]
            
            # Add respective research station rule to research locations
            if "research" in location_data.tags:
                if "science" in location_data.tags:
                    add_rule(location, (lambda state: alchemy_engine(state)) if "tier_2" in location_data.tags else (lambda state: science_machine(state)))
                elif "magic" in location_data.tags:
                    add_rule(location, (lambda state: shadow_manipulator(state)) if "tier_2" in location_data.tags else (lambda state: prestihatitor(state)))
                elif "celestial" in location_data.tags:
                    add_rule(location, (lambda state: celestial_altar(state)) if "tier_2" in location_data.tags else (lambda state: celestial_orb(state)))
                elif "seafaring" in location_data.tags:
                    add_rule(location, lambda state: think_tank(state))
                elif "ancient" in location_data.tags:
                    add_rule(location, lambda state: ancient_altar(state))
            
            elif "farming" in location_data.tags:
                add_rule(location, lambda state: advanced_farming(state))

            # Prioritize required bosses
            for boss_name, tag_name in PRIORITY_TAGS.items():
                if boss_name in PROGRESSION_REQUIRED_BOSSES and tag_name in location_data.tags:
                    required = True
                    break
            
            if required: 
                multiworld.priority_locations[player].value.add(location_name)
            elif ("priority" in location_data.tags
            or (options.boss_locations.current_key == "prioritized" and "boss" in location_data.tags and not "excluded" in location_data.tags)
            ):
                # Prioritize generic priority tag
                multiworld.priority_locations[player].value.add(location_name)
            # Exclude from having progression items if it meets the conditions
            if not required and ("excluded" in location_data.tags 
            or (not options.seasonal_locations.value and "seasonal" in location_data.tags)
            or (options.boss_locations.current_key == "none" and "boss" in location_data.tags)
            or (options.boss_locations.current_key == "easy" and "raidboss" in location_data.tags)
            or (options.skill_level.current_key == "easy" and "advanced" in location_data.tags)
            or (options.skill_level.current_key != "expert" and "expert" in location_data.tags)
            ):
                excluded.add(location_name)

            # Forbid season helpers in seasonal locations
            if "seasonal" in location_data.tags:
                for item_name in SEASON_HELPER_ITEMS:
                    forbid_item(location, item_name, player)

    exclusion_rules(multiworld, player, excluded)

    # Set region rules
    for region_name, rule in rules_lookup["regions"].items():
        region = multiworld.get_region(region_name, player)
        for entrance in region.entrances:
            set_rule(entrance, rule)
    
