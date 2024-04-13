import typing
from collections.abc import Callable

from BaseClasses import CollectionState
from worlds.generic.Rules import exclusion_rules, set_rule, add_rule
from worlds.AutoWorld import World

from .Locations import location_data_table

def advanced_player_bias (state: CollectionState, player: int) -> bool: 
   return state.multiworld.skill_level[player].current_key != "easy"

def expert_player_bias (state: CollectionState, player: int) -> bool: 
   return state.multiworld.skill_level[player].current_key == "expert"

def warly_dishes_enabled (state: CollectionState, player: int) -> bool: 
   return state.multiworld.cooking_locations[player].current_key == "warly_enabled"

def has_survived_num_days (day_goal:int, state: CollectionState, player: int) -> bool:
	# Assume number of days lived based on items count
	item_count = state.count_group("all", player)
	if item_count < 4:
		return False
	return (day_goal if day_goal < 50 else 50) > (4 - (item_count/2))

def reached_winter (state: CollectionState, player: int) -> bool: 
   return state.has("Reach Winter", player)

def reached_spring (state: CollectionState, player: int) -> bool: 
   return state.has("Reach Spring", player)

def reached_summer (state: CollectionState, player: int) -> bool: 
   return state.has("Reach Summer", player)

def reached_autumn (state: CollectionState, player: int) -> bool: 
   return state.has("Reach Autumn", player)

def is_winter (state: CollectionState, player: int) -> bool: 
   return reached_winter(state, player) and (not reached_spring(state, player) or late_game(state, player))

def is_spring (state: CollectionState, player: int) -> bool: 
   return reached_spring(state, player) and (not reached_summer(state, player) or late_game(state, player))

def is_summer (state: CollectionState, player: int) -> bool: 
   return reached_summer(state, player) and (not reached_autumn(state, player) or late_game(state, player))

def is_autumn (state: CollectionState, player: int) -> bool: 
   return reached_autumn(state, player) or not reached_winter(state, player)

def butter_luck (state: CollectionState, player: int) -> bool: 
	return has_survived_num_days(40, state, player)

def bug_catching (state: CollectionState, player: int) -> bool:
	return state.has_all(["Bug Net", "Rope"], player)

def digging (state: CollectionState, player: int) -> bool:
	return state.has_any(["Shovel", "Regal Shovel"], player)

def basic_combat (state: CollectionState, player: int) -> bool:
	if advanced_player_bias(state, player):
		return state.has("Rope", player)
	return state.has_all(["Rope", "Spear"], player) and state.has_any(["Log Suit", "Football Helmet"], player)

def backpack (state: CollectionState, player: int) -> bool:
	return state.has("Backpack", player) or (state.has_all(["Piggyback", "Rope"], player) and basic_combat(state, player))

def basic_exploration (state: CollectionState, player: int) -> bool:
	return backpack(state, player) and digging(state, player) and bug_catching(state, player)

def basic_cooking (state: CollectionState, player: int) -> bool:
	return state.has_all(["Cut Stone", "Crock Pot"], player)

def pre_basic_cooking (state: CollectionState, player: int) -> bool:
	return warly_dishes_enabled(state, player) or basic_cooking(state, player)

def healing (state: CollectionState, player: int) -> bool:
	return basic_cooking(state, player) or state.has("Healing Salve", player) or (state.has("Rope", player) and state.has_any(["Tent", "Siesta Lean-to"], player)) or advanced_player_bias(state, player)

def desert_exploration (state: CollectionState, player: int) -> bool:
	return advanced_player_bias(state, player) or (basic_exploration(state, player) and basic_combat(state, player))

def swamp_exploration (state: CollectionState, player: int) -> bool:
	return advanced_player_bias(state, player) or (basic_exploration(state, player) and (basic_combat(state, player) or healing(state, player)))

def base_making (state: CollectionState, player: int) -> bool:
	return state.has_all(["Boards", "Cut Stone", "Electrical Doodad", "Rope", "Chest"], player)

def basic_farming (state: CollectionState, player: int) -> bool:
	return state.has_any(["Garden Hoe", "Splendid Garden Hoe"], player) and state.has("Garden Digamajig", player) and base_making(state, player)

def advanced_combat (state: CollectionState, player: int) -> bool:
	return basic_combat(state, player) and (state.has("Booster Shot",player) or expert_player_bias(state, player)) and (state.has_any(["Hambat", "Dark Sword"], player)) and (base_making(state, player) or advanced_player_bias(state, player))

def winter_survival (state: CollectionState, player: int) -> bool:
	return (state.has("Razor", player) and state.has_any(["Thermal Stone", "Puffy Vest", "Beefalo Hat", "Winter Hat", "Cat Cap"], player) or advanced_player_bias(state, player))

def electric_insulation (state: CollectionState, player: int) -> bool:
	return state.has_any(["Rain Coat", "Rain Hat"], player) or state.has_all(["Eyebrella", "Defeat Deerclops"], player)

def spring_survival (state: CollectionState, player: int) -> bool:
	return (electric_insulation(state, player) or state.has("Umbrella", player) or advanced_player_bias(state, player)) and state.has_all(["Lightning Rod", "Cut Stone"], player)

def has_cooling_source (state: CollectionState, player: int) -> bool:
	return (state.has_all(["Thermal Stone", "Ice Box", "Cut Stone"], player) 
		or state.has_any(["Endothermic Fire", "Chilled Amulet"], player)
		or state.has_all(["Endothermic Fire Pit", "Cut Stone", "Electrical Doodad"], player)
		or(state.has("Mooncaller Staff", player) and advanced_player_bias(state, player))
	) 

def has_summer_insulation (state: CollectionState, player: int) -> bool:
	return (state.has_any(["Umbrella", "Summer Frest", "Thermal Stone"], player) 
		 	or state.has_all(["Floral Shirt", "Papyrus"], player)
			or state.has_all(["Eyebrella", "Defeat Deerclops"], player)
		)

def fire_suppression (state: CollectionState, player: int) -> bool:
	return base_making(state, player) and ((ruins_exploration(state, player) and state.has("Ice Flingomatic", player)) or state.has_all(["Luxury Fan", "Defeat Moose/Goose"], player) or state.has("Empty Watering Can", player))

def summer_survival (state: CollectionState, player: int) -> bool:
	return (has_cooling_source(state, player) and has_summer_insulation(state, player) and fire_suppression(state, player)) or advanced_player_bias(state, player)

def autumn_survival (state: CollectionState, player: int) -> bool:
	return expert_player_bias(state, player) or (cave_exploration(state, player) and basic_boating(state, player) and (basic_combat(state, player)))

def character_switching (state: CollectionState, player: int) -> bool:
	return state.has("Cratered Moonrock", player) and base_making(state, player) and basic_combat(state, player)

def epic_combat (state: CollectionState, player: int) -> bool:
	return advanced_combat(state, player) and healing(state, player) and (state.has("Pan Flute", player) or state.has_all(["Walking Cane","Reach Winter"], player)) and (character_switching(state, player) or expert_player_bias(state, player))

def bird_caging (state: CollectionState, player: int) -> bool:
	return state.has_all(["Bird Trap", "Birdcage", "Papyrus"], player)

def honey_farming (state: CollectionState, player: int) -> bool:
	return state.has_all(["Bee Box", "Boards", "Bug Net", "Rope"], player) or advanced_player_bias(state, player)
	
def leafy_meat (state: CollectionState, player: int) -> bool:
	return reached_spring(state, player) or lunar_island(state, player)

def farmplant_cooking (state: CollectionState, player: int) -> bool:
	return basic_cooking(state, player) and basic_farming(state, player)

def egg_cooking (state: CollectionState, player: int) -> bool:
	return basic_cooking(state, player) and bird_caging(state, player)

def sweet_cooking (state: CollectionState, player: int) -> bool:
	return basic_cooking(state, player) and honey_farming(state, player)

def advanced_cooking (state: CollectionState, player: int) -> bool:
	return basic_cooking(state, player) and basic_farming(state, player) and bird_caging(state, player) and honey_farming(state, player)
						
def advanced_exploration (state: CollectionState, player: int) -> bool:
	return (basic_exploration(state, player) and state.has_all(["Walking Cane", "Reach Winter"], player)) or expert_player_bias(state, player)

def advanced_farming (state: CollectionState, player: int) -> bool:
	return basic_farming(state, player) and state.has("Empty Watering Can", player)

def light_source (state: CollectionState, player: int) -> bool:
	return ((state.has_all(["Lantern", "Rope"], player) or state.has_all(["Miner Hat", "Rope", "Bug Net"], player) or ((state.has_any(["Moggles", "Morning Star"], player) and base_making(state, player))) and advanced_player_bias(state, player)) or expert_player_bias(state, player))

def cave_exploration (state: CollectionState, player: int) -> bool:
	return basic_exploration(state, player) and ((light_source(state, player) and base_making(state, player)) or expert_player_bias(state, player))

def blue_gems (state: CollectionState, player: int) -> bool:
	return reached_winter(state, player) or cave_exploration(state, player) or digging(state, player),

def red_gems (state: CollectionState, player: int) -> bool:
	return reached_summer(state, player) or cave_exploration(state, player) or digging(state, player),	

def ice_staff (state: CollectionState, player: int) -> bool:
	(state.has_all(["Spear", "Rope", "Ice Staff"], player) and blue_gems(state, player))

def fire_staff (state: CollectionState, player: int) -> bool:
	(state.has_all(["Spear", "Rope", "Fire Staff"], player) and red_gems(state, player))

def canary (state: CollectionState, player: int) -> bool:
	return state.has_all(["Friendly Scarecrow", "Boards"], player) and basic_farming(state, player)

def can_get_feathers (state: CollectionState, player: int) -> bool:
	return state.has_all(["Boomerang", "Boards"], player) or state.has("Bird Trap", player) or ice_staff(state, player)

def ranged_combat (state: CollectionState, player: int) -> bool:
	return can_get_feathers(state, player) and (state.has_all(["Reach Winter", "Blow Dart"], player) or (canary(state, player) and bird_caging(state, player) and state.has("Electric Dart", player)))

def ranged_aggression (state: CollectionState, player: int) -> bool:
	return state.has_all(["Boomerang", "Boards"], player) or (state.has("Bird Trap", player) and state.has_any(["Fire Dart", "Sleep Dart"], player)) or ranged_combat(state, player) or ice_staff(state, player) or fire_staff(state, player)

def dairy (state: CollectionState, player: int) -> bool: 
   return state.has("Defeat Eye Of Terror", player) or (electric_insulation(state, player) and ranged_aggression(state, player) and state.has_all(["Morning Star", "Electrical Doodad", "Cut Stone"], player)) or butter_luck(state, player)

def ruins_exploration (state: CollectionState, player: int) -> bool:
	return cave_exploration(state, player) and (advanced_combat(state, player) or (healing(state, player) and basic_combat(state, player)) or expert_player_bias(state, player))
						
def dark_magic (state: CollectionState, player: int) -> bool:
	return state.has_any(["Dark Sword", "Bat Bat", "Night Armor"], player) and state.has("Papyrus", player)

def late_game (state: CollectionState, player: int) -> bool: 
   return reached_autumn(state, player) and advanced_boating(state, player) and epic_combat(state, player) and advanced_cooking(state, player) and dark_magic(state, player)

def heavy_lifting (state: CollectionState, player: int) -> bool:
	return state.has_all(["Saddle", "Beefalo Hat"], player)
						
def basic_boating (state: CollectionState, player: int) -> bool:
	return basic_exploration(state, player) and state.has_all(["Boat Kit", "Boards"], player)

def advanced_boating (state: CollectionState, player: int) -> bool:
	return basic_boating(state, player) and light_source(state, player) and base_making(state, player) and state.has_all(["Anchor Kit", "Steering Wheel Kit", "Mast Kit"], player)

def freshwater_fishing (state: CollectionState, player: int) -> bool:
	return state.has("Freshwater Fishing Rod", player)

def sea_fishing (state: CollectionState, player: int) -> bool:
	return state.has_all(["Sea Fishing Rod", "Boards", "Boat Kit"], player)

def fishing (state: CollectionState, player: int) -> bool:
	return freshwater_fishing(state, player) or sea_fishing(state, player)

def sea_cooking (state: CollectionState, player: int) -> bool:
	return basic_cooking(state, player) and state.has_all(["Razor", "Sea Fishing Rod"], player) and advanced_boating(state, player)

def lunar_island (state: CollectionState, player: int) -> bool:
	return (basic_boating(state, player) and advanced_player_bias(state, player)) or advanced_boating(state, player)

def hermit_island (state: CollectionState, player: int) -> bool:
	return ((basic_boating(state, player) and advanced_player_bias(state, player)) or advanced_boating(state, player)) and basic_cooking(state, player) and base_making(state, player)
						
def hermit_sea_quests (state: CollectionState, player: int) -> bool:
	return ((basic_boating(state, player) and advanced_player_bias(state, player)) or advanced_boating(state, player)) and state.has_all(["Sea Fishing Rod", "Pinchin' Winch"], player)
						
def moonstone_event (state: CollectionState, player: int) -> bool:
	return (ruins_exploration(state, player) or expert_player_bias(state, player)) and has_survived_num_days(11, state, player)

def archive_exploration (state: CollectionState, player: int) -> bool:
	return state.has_any(["Mooncaller Staff", "Iridescent Gem"], player)
						
def crab_king (state: CollectionState, player: int) -> bool:
	return advanced_boating(state, player) and state.count("Crabby Hermit Friendship", player) >= 10 and state.has_all(["Weather Pain", "Defeat Moose/Goose"], player)

def storm_protection (state: CollectionState, player: int) -> bool:
	return state.has_all(["Fashion Goggles", "Desert Goggles"], player) or state.has("Astroggles", player)

def moonstorm_exploration (state: CollectionState, player: int) -> bool:
	return state.has_all(["Celestial Sanctum Icon", "Celestial Sanctum Ward", "Inactive Celestial Tribute", "Pinchin' Winch"], player) and lunar_island(state, player) and storm_protection(state, player) and advanced_exploration(state, player) and electric_insulation(state, player)
						
def celestial_champion (state: CollectionState, player: int) -> bool:
	return moonstorm_exploration(state, player) and state.has_all(["Incomplete Experiment", "Celestial Orb"], player) and ranged_combat(state, player)

def ancient_guardian (state: CollectionState, player: int) -> bool:
	return ruins_exploration(state, player) and (advanced_combat(state, player) or expert_player_bias(state, player))

def shadow_pieces (state: CollectionState, player: int) -> bool:
	return advanced_combat(state, player) and heavy_lifting(state, player) and base_making(state, player) and state.has("Potter's Wheel", player)

def ancient_fuelweaver (state: CollectionState, player: int) -> bool:
	return dark_magic(state, player) and state.has_all(["Shadow Atrium", "Ancient Key"], player) and (state.has_all(["Nightmare Amulet", "Weather Pain", "Defeat Moose/Goose"], player) or expert_player_bias(state, player))

def moon_quay_exploration (state: CollectionState, player: int) -> bool:
	return advanced_boating(state, player) and state.has_all(["Queen of Moon Quay", "Cannon Kit", "Cannonball", "Gunpowder", "Cut Stone"], player)

def wall_building (state: CollectionState, player: int) -> bool:
	return (base_making(state, player) and (state.has_all(["Stone Wall", "Potter's Wheel"], player))) or ruins_exploration(state, player)

def science_machine (state: CollectionState, player: int) -> bool:
	return state.has("Science Machine", player)

def alchemy_engine (state: CollectionState, player: int) -> bool:
	return state.has("Alchemy Engine", player)

def prestihatitor (state: CollectionState, player: int) -> bool:
	return state.has("Prestihatitor", player)

def shadow_manipulator (state: CollectionState, player: int) -> bool:
	return state.has("Shadow Manipulator", player)

def think_tank (state: CollectionState, player: int) -> bool:
	return state.has("Think Tank", player)

def ancient_altar (state: CollectionState, player: int) -> bool:
	return ruins_exploration(state, player)

def celestial_orb (state: CollectionState, player: int) -> bool:
	return state.has("Celestial Orb", player) or celestial_altar(state, player)

def celestial_altar (state: CollectionState, player: int) -> bool:
	return lunar_island(state, player)

def survival_goal (state: CollectionState, player: int) -> bool:
	if state.multiworld.goal[player].current_key != "survival": return False # Only relevant if your goal is to survive
	days_to_survive = state.multiworld.days_to_survive[player].value
	if days_to_survive < 20:
		return advanced_combat(state, player) and cave_exploration(state, player) # Generic non-seasonal goal
	elif days_to_survive < 35:
		return reached_winter(state, player)
	elif days_to_survive < 55:
		return reached_spring(state, player)
	elif days_to_survive < 70:
		return reached_summer(state, player)
	elif days_to_survive < 90:
		return reached_autumn(state, player)
	return late_game(state, player)

def get_rules_lookup(player: int):
	rules_lookup: typing.Dict[str, typing.List[Callable[[CollectionState], bool]]] = {
		"locations": {
			# Events
			"Winter": lambda state: winter_survival(state, player),
			"Spring": lambda state: reached_winter(state, player) and spring_survival(state, player),
			"Summer": lambda state: reached_spring(state, player) and summer_survival(state, player),
			"Autumn": lambda state: reached_summer(state, player) and autumn_survival(state, player),
			"Survival Goal": lambda state: survival_goal(state, player),
			"Build Science Machine": lambda state: has_survived_num_days(1, state, player),
			"Build Alchemy Engine": lambda state: base_making(state, player) and state.has("Science Machine",player),
			"Build Prestihatitor": lambda state: state.has_all(["Top Hat", "Boards", "Science Machine"], player),	
			"Build Shadow Manipulator": lambda state: ruins_exploration(state, player) and state.has("Prestihatitor",player),
			"Build Think Tank": lambda state: state.has_all(["Boards", "Science Machine"], player),	
			"Find Celestial Orb": lambda state: has_survived_num_days(5, state, player),
			"Moon Stone Event": lambda state: moonstone_event(state, player),
			"Find Celestial Sanctum Icon": lambda state: state.has("Astral Detector", player) and heavy_lifting(state, player),
			"Find Celestial Sanctum Ward": lambda state: state.has("Astral Detector", player) and heavy_lifting(state, player),
			"Will Get Accursed Trinket": lambda state: advanced_boating(state, player),
			"Defeat Crab King with Pearl's Pearl": lambda state: crab_king(state, player),
			"Defeat Ancient Guardian": lambda state: ancient_guardian(state, player),
			"Defeat Shadow Pieces": lambda state: shadow_pieces(state, player),
			"Defeat Deerclops": lambda state: basic_combat(state, player) and is_winter(state, player),
			"Defeat Moose/Goose": lambda state: basic_combat(state, player) and is_spring(state, player),
			"Defeat Antlion": lambda state: (freshwater_fishing(state, player) or advanced_combat(state, player)) and is_summer(state, player) and storm_protection(state, player),
			"Defeat Bearger": lambda state: basic_combat(state, player) and reached_autumn(state, player),
			"Defeat Dragonfly": lambda state: advanced_combat(state, player) and wall_building(state, player),
			"Defeat Bee Queen": lambda state: epic_combat(state, player),
			"Defeat Klaus": lambda state: advanced_combat(state, player) and is_winter(state, player),
			"Defeat Malbatross": lambda state: advanced_combat(state, player) and advanced_boating(state, player),
			"Defeat Toadstool": lambda state: epic_combat(state, player) and cave_exploration(state, player) and dark_magic(state, player),
			"Defeat Ancient Fuelweaver": lambda state: ancient_fuelweaver(state, player),
			"Defeat Lord of the Fruit Flies": lambda state: basic_combat(state, player) and advanced_farming(state, player) and reached_spring(state, player),
			"Defeat Celestial Champion": lambda state: celestial_champion(state, player),
			"Defeat Eye Of Terror": lambda state: advanced_combat(state, player),
			"Defeat Retinazor": lambda state: epic_combat(state, player),
			"Defeat Spazmatism": lambda state: epic_combat(state, player),
			"Defeat Nightmare Werepig": lambda state: ruins_exploration(state, player) and epic_combat(state, player) and state.has_all(["Opulent Pickaxe", "Luxury Axe"], player),
			"Defeat Scrappy Werepig": lambda state: state.has("Defeat Nightmare Werepig", player),
			"Defeat Frostjaw": lambda state: advanced_boating(state, player) and advanced_combat(state, player) and advanced_exploration(state, player),

			# Pearl Questline
			"Hermit Home Upgrade (1)": lambda state: hermit_island(state, player), # Cookie cutters, boards, fireflies
			"Hermit Home Upgrade (2)": lambda state: hermit_island(state, player), # Marble, cut stone, light bulb
			"Hermit Home Upgrade (3)": lambda state: hermit_island(state, player), # Moonrock, rope, carpet
			"Hermit Island Drying Racks": lambda state: hermit_island(state, player),
			"Hermit Island Plant 10 Flowers": lambda state: hermit_island(state, player),
			"Hermit Island Plant 8 Berry Bushes": lambda state: hermit_island(state, player),
			"Hermit Island Clear Underwater Salvageables": lambda state: hermit_sea_quests(state, player),
			"Hermit Island Kill Lureplant": lambda state: hermit_island(state, player) and reached_spring(state, player),
			"Hermit Island Build Wooden Chair": lambda state: hermit_island(state, player) and state.has("Sawhorse", player),
			"Give Crabby Hermit Umbrella": lambda state: hermit_island(state, player) and spring_survival(state, player),
			"Give Crabby Hermit Warm Clothing": lambda state: hermit_island(state, player) and is_winter (state, player) and state.has_any(["Breezy Vest", "Puffy Vest"], player),
			"Give Crabby Hermit Flower Salad": lambda state: hermit_island(state, player) and is_summer(state, player),
			"Give Crabby Hermit Fallounder": lambda state: hermit_sea_quests(state, player) and is_autumn(state, player),
			"Give Crabby Hermit Bloomfin Tuna": lambda state: hermit_sea_quests(state, player) and is_spring(state, player),
			"Give Crabby Hermit Scorching Sunfish": lambda state: hermit_sea_quests(state, player) and is_summer(state, player),
			"Give Crabby Hermit Ice Bream": lambda state: hermit_sea_quests(state, player) and is_winter(state, player),
			"Give Crabby Hermit 5 Heavy Fish": lambda state: hermit_sea_quests(state, player),

			# Tasks
			"Distilled Knowledge (Yellow)": lambda state: archive_exploration(state, player),
			"Distilled Knowledge (Blue)": lambda state: archive_exploration(state, player),
			"Distilled Knowledge (Red)": lambda state: archive_exploration(state, player),
			"Given by Wagstaff during Moonstorm": lambda state: moonstorm_exploration(state, player),
			"Given by Queen of Moon Quay": lambda state: moon_quay_exploration(state, player),

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
			"Batilisk": lambda state: basic_exploration(state, player),
			"Bee": lambda state: has_survived_num_days(2, state, player),
			"Beefalo": lambda state: basic_combat(state, player),
			"Clockwork Bishop": lambda state: advanced_combat(state, player),
			"Bunnyman": lambda state: basic_combat(state, player) and cave_exploration(state, player),
			"Butterfly": lambda state: True,
			"Buzzard": lambda state: basic_combat(state, player),
			"Canary": lambda state: canary(state, player) and can_get_feathers(state, player),
			"Carrat": lambda state: lunar_island(state, player),
			"Catcoon": lambda state: has_survived_num_days(3, state, player),
			"Cookie Cutter": lambda state: advanced_boating(state, player),
			"Crawling Horror": lambda state: advanced_combat(state, player),
			"Crow": lambda state: can_get_feathers(state, player),
			"Dragonfly": lambda state: advanced_combat(state, player) and summer_survival(state, player),
			"Red Hound": lambda state: basic_combat(state, player) and is_summer(state, player),
			"Frog": lambda state: True,
			"Saladmander": lambda state: lunar_island(state, player),
			"Ghost": lambda state: basic_exploration(state, player) and digging(state, player),
			"Gnarwail": lambda state: basic_combat(state, player) and advanced_boating(state, player),
			"Grass Gator": lambda state: basic_combat(state, player) and advanced_boating(state, player) and ranged_aggression(state,player),
			"Grass Gekko": lambda state: desert_exploration(state, player),
			"Briar Wolf": lambda state: basic_combat(state, player),
			"Hound": lambda state: basic_combat(state, player) and desert_exploration(state, player),
			"Blue Hound": lambda state: basic_combat(state, player) and is_winter(state, player),
			"Killer Bee": lambda state: basic_combat(state, player),
			"Clockwork Knight": lambda state: advanced_combat(state, player),
			"Koalefant": lambda state: basic_combat(state, player) and ranged_aggression(state, player),
			"Krampus": lambda state: basic_combat(state, player) and can_get_feathers(state, player) and has_survived_num_days(11, state, player),
			"Treeguard": lambda state: basic_combat(state, player) and has_survived_num_days(10, state, player),
			"Crustashine": lambda state: moon_quay_exploration(state, player) and ranged_aggression(state, player),
			"Bulbous Lightbug": lambda state: cave_exploration(state, player),
			"Volt Goat": lambda state: basic_combat(state, player) and ranged_aggression(state, player) and desert_exploration(state, player),
			"Merm": lambda state: basic_combat(state, player) and swamp_exploration(state, player),
			"Moleworm": lambda state: True,
			"Naked Mole Bat": lambda state: cave_exploration(state, player),
			"Splumonkey": lambda state: ruins_exploration(state, player),
			"Moon Moth": lambda state: lunar_island(state, player),
			"Mosquito": lambda state: basic_combat(state, player) and swamp_exploration(state, player),
			"Mosling": lambda state: basic_combat(state, player) and is_spring(state, player),
			"Mush Gnome": lambda state: basic_combat(state, player) and cave_exploration(state, player),
			"Terrorclaw": lambda state: advanced_combat(state, player) and advanced_boating(state, player),
			"Pengull": lambda state: basic_combat(state, player) and is_winter(state, player),
			"Gobbler": lambda state: basic_combat(state, player),
			"Pig Man": lambda state: has_survived_num_days(4, state, player),
			"Powder Monkey": lambda state: basic_combat(state, player) and moon_quay_exploration(state, player),
			"Prime Mate": lambda state: basic_combat(state, player) and moon_quay_exploration(state, player),
			"Puffin": lambda state: sea_cooking(state, player),
			"Rabbit": lambda state: True,
			"Redbird": lambda state: can_get_feathers(state, player),
			"Snowbird": lambda state: can_get_feathers(state, player) and is_winter(state, player),
			"Rock Lobster": lambda state: advanced_combat(state, player) and cave_exploration(state, player),
			"Clockwork Rook": lambda state: advanced_combat(state, player),
			"Rockjaw": lambda state: advanced_combat(state, player) and advanced_boating(state, player) and healing(state, player),
			"Slurper": lambda state: ruins_exploration(state, player),
			"Slurtle": lambda state: cave_exploration(state, player),
			"Snurtle": lambda state: cave_exploration(state, player),
			"Ewecus": lambda state: advanced_combat(state, player) and advanced_exploration(state, player) and reached_autumn(state, player),
			"Spider": lambda state: True,
			"Dangling Depth Dweller": lambda state: ruins_exploration(state, player),
			"Cave Spider": lambda state: basic_combat(state, player) and cave_exploration(state, player),
			"Nurse Spider": lambda state: advanced_combat(state, player) and reached_spring(state, player),
			"Shattered Spider": lambda state: basic_combat(state, player) and lunar_island(state, player),
			"Spitter": lambda state: basic_combat(state, player) and cave_exploration(state, player),
			"Spider Warrior": lambda state: basic_combat(state, player),
			"Sea Strider": lambda state: basic_combat(state, player) and advanced_boating(state, player),
			"Spider Queen": lambda state: advanced_combat(state, player) and reached_spring(state, player),
			"Tallbird": lambda state: basic_combat(state, player) and healing(state, player),
			"Tentacle": lambda state: basic_combat(state, player) and swamp_exploration(state, player),
			"Big Tentacle": lambda state: advanced_combat(state, player) and cave_exploration(state, player),
			"Terrorbeak": lambda state: advanced_combat(state, player),
			"MacTusk": lambda state: basic_combat(state, player) and reached_winter(state, player),
			"Varg": lambda state: advanced_combat(state, player) and advanced_exploration(state, player) and reached_autumn(state, player),
			"Varglet": lambda state: basic_combat(state, player) and advanced_exploration(state, player) and reached_spring(state, player),
			"Depths Worm": lambda state: ruins_exploration(state, player),
			"Ancient Sentrypede": lambda state: archive_exploration(state, player) and advanced_combat(state, player),
			"Skittersquid": lambda state: basic_combat(state, player) and advanced_exploration(state, player) and advanced_boating(state, player),
			
			# Cook foods
			"Butter Muffin": lambda state: pre_basic_cooking(state, player),
			"Froggle Bunwich": lambda state: pre_basic_cooking(state, player),
			"Taffy": lambda state: sweet_cooking(state, player),
			"Pumpkin Cookies": lambda state: advanced_cooking(state, player),
			"Stuffed Eggplant": lambda state: farmplant_cooking(state, player),
			"Fishsticks": lambda state: basic_cooking(state, player) and fishing(state, player),
			"Honey Nuggets": lambda state: sweet_cooking(state, player),
			"Honey Ham": lambda state: sweet_cooking(state, player),
			"Dragonpie": lambda state: farmplant_cooking(state, player) or (basic_cooking(state, player) and lunar_island(state, player)),
			"Kabobs": lambda state: pre_basic_cooking(state, player),
			"Mandrake Soup": lambda state: basic_cooking(state, player),
			"Bacon and Eggs": lambda state: egg_cooking(state, player),
			"Meatballs": lambda state: pre_basic_cooking(state, player),
			"Meaty Stew": lambda state: pre_basic_cooking(state, player),
			"Pierogi": lambda state: egg_cooking(state, player),
			"Turkey Dinner": lambda state: basic_cooking(state, player) and basic_combat(state, player),
			"Ratatouille": lambda state: pre_basic_cooking(state, player),
			"Fist Full of Jam": lambda state: pre_basic_cooking(state, player),
			"Fruit Medley": lambda state: farmplant_cooking(state, player),
			"Fish Tacos": lambda state: farmplant_cooking(state, player) and fishing(state, player),
			"Waffles": lambda state: egg_cooking(state, player) and butter_luck(state, player),
			"Monster Lasagna": lambda state: basic_cooking(state, player),
			"Powdercake": lambda state: advanced_cooking(state, player),
			"Unagi": lambda state: basic_cooking(state, player) and cave_exploration(state, player) and freshwater_fishing(state, player),
			"Wet Goop": lambda state: basic_cooking(state, player),
			"Flower Salad": lambda state: basic_cooking(state, player) and is_summer(state, player),
			"Ice Cream": lambda state: basic_cooking(state, player) and dairy(state, player),
			"Melonsicle": lambda state: farmplant_cooking(state, player),
			"Trail Mix": lambda state: basic_cooking(state, player),
			"Spicy Chili": lambda state: basic_cooking(state, player),
			"Guacamole": lambda state: basic_cooking(state, player),
			"Jellybeans": lambda state: basic_cooking(state, player) and advanced_combat(state, player),
			"Fancy Spiralled Tubers": lambda state: farmplant_cooking(state, player),
			"Creamy Potato Purée": lambda state: farmplant_cooking(state, player),
			"Asparagus Soup": lambda state: farmplant_cooking(state, player),
			"Vegetable Stinger": lambda state: farmplant_cooking(state, player),
			"Banana Pop": lambda state: basic_cooking(state, player) and (cave_exploration(state, player) or moon_quay_exploration(state, player)),
			"Frozen Banana Daiquiri": lambda state: basic_cooking(state, player) and (cave_exploration(state, player) or moon_quay_exploration(state, player)),
			"Banana Shake": lambda state: basic_cooking(state, player) and (cave_exploration(state, player) or moon_quay_exploration(state, player)),
			"Ceviche": lambda state: sea_cooking(state, player),
			"Salsa Fresca": lambda state: farmplant_cooking(state, player),
			"Stuffed Pepper Poppers": lambda state: farmplant_cooking(state, player),
			"California Roll": lambda state: sea_cooking(state, player),
			"Seafood Gumbo": lambda state: basic_cooking(state, player) and cave_exploration(state, player),
			"Surf 'n' Turf": lambda state: sea_cooking(state, player),
			"Lobster Bisque": lambda state: basic_cooking(state, player) and sea_fishing(state, player),
			"Lobster Dinner": lambda state: basic_cooking(state, player) and sea_fishing(state, player) and butter_luck(state, player),
			"Barnacle Pita": lambda state: sea_cooking(state, player),
			"Barnacle Nigiri": lambda state: sea_cooking(state, player),
			"Barnacle Linguine": lambda state: sea_cooking(state, player),
			"Stuffed Fish Heads": lambda state: sea_cooking(state, player),
			"Leafy Meatloaf": lambda state: basic_cooking(state, player) and leafy_meat(state, player),
			"Veggie Burger": lambda state: farmplant_cooking(state, player) and leafy_meat(state, player),
			"Jelly Salad": lambda state: sweet_cooking(state, player) and leafy_meat(state, player),
			"Beefy Greens": lambda state: farmplant_cooking(state, player) and leafy_meat(state, player),
			"Mushy Cake": lambda state: basic_cooking(state, player) and cave_exploration(state, player),
			"Soothing Tea": lambda state: farmplant_cooking(state, player),
			"Fig-Stuffed Trunk": lambda state: sea_cooking(state, player),
			"Figatoni": lambda state: sea_cooking(state, player),
			"Figkabab": lambda state: sea_cooking(state, player),
			"Figgy Frogwich": lambda state: sea_cooking(state, player),
			"Bunny Stew": lambda state: basic_cooking(state, player),
			"Plain Omelette": lambda state: egg_cooking(state, player),
			"Breakfast Skillet": lambda state: egg_cooking(state, player),
			"Tall Scotch Eggs": lambda state: basic_cooking(state, player) and basic_combat(state, player),
			"Steamed Twigs": lambda state: basic_cooking(state, player),
			"Beefalo Treats": lambda state: farmplant_cooking(state, player),
			"Milkmade Hat": lambda state: basic_cooking(state, player) and cave_exploration(state, player) and basic_boating(state, player) and dairy(state, player),
			"Amberosia": lambda state: basic_cooking(state, player) and basic_boating(state, player) and (basic_combat(state, player) or advanced_player_bias(state, player)) and state.has("Collected Dust", player),
			# Warly Dishes
			"Grim Galette": lambda state: farmplant_cooking(state, player) and warly_dishes_enabled(state, player),
			"Volt Goat Chaud-Froid": lambda state: basic_cooking(state, player) and basic_combat(state, player) and warly_dishes_enabled(state, player),
			"Glow Berry Mousse": lambda state: basic_cooking(state, player) and cave_exploration(state, player) and warly_dishes_enabled(state, player),
			"Fish Cordon Bleu": lambda state: sea_cooking(state, player) and warly_dishes_enabled(state, player),
			"Hot Dragon Chili Salad": lambda state: farmplant_cooking(state, player) and warly_dishes_enabled(state, player),
			"Asparagazpacho": lambda state: farmplant_cooking(state, player) and warly_dishes_enabled(state, player),
			"Puffed Potato Soufflé": lambda state: advanced_cooking(state, player) and warly_dishes_enabled(state, player),
			"Monster Tartare": lambda state: basic_cooking(state, player) and warly_dishes_enabled(state, player),
			"Fresh Fruit Crepes": lambda state: farmplant_cooking(state, player) and butter_luck(state, player) and warly_dishes_enabled(state, player),
			"Bone Bouillon": lambda state: farmplant_cooking(state, player) and warly_dishes_enabled(state, player),
			"Moqueca": lambda state: farmplant_cooking(state, player) and sea_cooking(state, player) and warly_dishes_enabled(state, player),
			# Farming 
			"Grow Giant Asparagus": lambda state: is_winter(state, player) or is_spring(state, player),
			"Grow Giant Garlic": lambda state: reached_winter(state, player),
			"Grow Giant Pumpkin": lambda state: is_winter(state, player) or reached_autumn(state, player),
			"Grow Giant Corn": lambda state: reached_spring(state, player),
			"Grow Giant Onion": lambda state: reached_spring(state, player),
			"Grow Giant Potato": lambda state: reached_winter(state, player),
			"Grow Giant Dragon Fruit": lambda state: reached_spring(state, player),
			"Grow Giant Pomegranate": lambda state: reached_spring(state, player),
			"Grow Giant Eggplant": lambda state: reached_spring(state, player),
			"Grow Giant Toma Root": lambda state: reached_spring(state, player),
			"Grow Giant Watermelon": lambda state: reached_spring(state, player),
			"Grow Giant Pepper": lambda state: reached_summer(state, player),
			"Grow Giant Durian": lambda state: reached_spring(state, player),
			"Grow Giant Carrot": lambda state: reached_winter(state, player),
			# Research
			"Science (Nitre)": lambda state: True,			
			"Science (Salt Crystals)": lambda state: basic_boating(state, player) and basic_combat(state, player),	
			"Science (Ice)": lambda state: True,				
			"Science (Slurtle Slime)": lambda state: cave_exploration(state, player),		
			"Science (Gears)": lambda state: ruins_exploration(state, player),					
			"Science (Scrap)": lambda state: basic_exploration(state, player),					
			"Science (Azure Feather)": lambda state: expert_player_bias(state, player) or (reached_winter(state, player) and (can_get_feathers(state, player) or advanced_player_bias(state, player))),	
			"Science (Crimson Feather)": lambda state: expert_player_bias(state, player) or can_get_feathers(state, player) or advanced_player_bias(state, player),	
			"Science (Jet Feather)": lambda state: advanced_player_bias(state, player) or can_get_feathers(state, player),	
			"Science (Saffron Feather)": lambda state: expert_player_bias(state, player) or (state.has_all(["Friendly Scarecrow", "Boards"], player) and basic_farming(state, player) and can_get_feathers(state, player)),	
			"Science (Kelp Fronds)": lambda state: basic_boating(state, player),		
			"Science (Steel Wool)": lambda state: advanced_combat(state, player) and advanced_exploration(state, player) and reached_autumn(state, player),			
			"Science (Electrical Doodad)": lambda state: state.has("Electrical Doodad", player),
			"Science (Ashes)": lambda state: True,			
			"Science (Cut Grass)": lambda state: True,		
			"Science (Beefalo Horn)": lambda state: basic_combat(state, player) and has_survived_num_days(15, state, player),		
			"Science (Beefalo Wool)": lambda state: basic_combat(state, player) and state.has("Razor", player),		
			"Science (Cactus Flower)": lambda state: is_summer(state, player),		
			"Science (Honeycomb)": lambda state: basic_combat(state, player),			
			"Science (Petals)": lambda state: True,				
			"Science (Succulent)": lambda state: True,			
			"Science (Foliage)": lambda state: True,				
			"Science (Tillweeds)": lambda state: basic_farming(state, player) and has_survived_num_days(15, state, player),	
			"Science (Lichen)": lambda state: ruins_exploration(state, player),	
			"Science (Banana)": lambda state: moon_quay_exploration(state, player) or ruins_exploration(state, player),			
			"Science (Fig)": lambda state: advanced_boating(state, player),			
			"Science (Tallbird Egg)": lambda state: basic_combat(state, player),
			"Science (Hound's Tooth)": lambda state: basic_combat(state, player),					
			"Science (Bone Shards)": lambda state: basic_combat(state, player),					
			"Science (Walrus Tusk)": lambda state: basic_combat(state, player) and is_winter(state, player),
			"Science (Silk)": lambda state: True,			
			"Science (Cut Stone)": lambda state: state.has("Cut Stone", player),
			"Science (Palmcone Sprout)": lambda state: moon_quay_exploration(state, player),	
			"Science (Pine Cone)": lambda state: True,			
			"Science (Birchnut)": lambda state: True,				
			"Science (Driftwood Piece)": lambda state: basic_boating(state, player),		
			"Science (Cookie Cutter Shell)": lambda state: basic_boating(state, player) and basic_combat(state, player),	
			"Science (Palmcone Scale)": lambda state: moon_quay_exploration(state, player),
			"Science (Gnarwail Horn)": lambda state: advanced_boating(state, player) and basic_combat(state, player),	
			"Science (Barnacles)": lambda state: sea_cooking(state, player),			
			"Science (Frazzled Wires)": lambda state: ruins_exploration(state, player),	
			"Science (Charcoal)": lambda state: True,			
			"Science (Butter)": lambda state: butter_luck(state, player),				
			"Science (Asparagus)": lambda state: basic_farming(state, player) and has_survived_num_days(15, state, player) and reached_winter(state, player),			
			"Science (Garlic)": lambda state: basic_farming(state, player) and has_survived_num_days(15, state, player),				
			"Science (Pumpkin)": lambda state: basic_farming(state, player) and has_survived_num_days(15, state, player),			
			"Science (Corn)": lambda state: basic_farming(state, player) and has_survived_num_days(15, state, player),				
			"Science (Onion)": lambda state: basic_farming(state, player) and has_survived_num_days(15, state, player),				
			"Science (Potato)": lambda state: basic_farming(state, player) and has_survived_num_days(15, state, player),				
			"Science (Dragon Fruit)": lambda state: (basic_farming(state, player) and has_survived_num_days(15, state, player)) or lunar_island(state, player),				
			"Science (Pomegranate)": lambda state: basic_farming(state, player) and has_survived_num_days(15, state, player) and reached_spring(state, player),		
			"Science (Eggplant)": lambda state: basic_farming(state, player) and has_survived_num_days(15, state, player),			
			"Science (Toma Root)": lambda state: basic_farming(state, player) and has_survived_num_days(15, state, player),				
			"Science (Watermelon)": lambda state: basic_farming(state, player) and has_survived_num_days(15, state, player) and reached_spring(state, player),		
			"Science (Pepper)": lambda state: basic_farming(state, player) and has_survived_num_days(15, state, player),				
			"Science (Durian)": lambda state: basic_farming(state, player) and has_survived_num_days(15, state, player) and reached_spring(state, player),				
			"Science (Carrot)": lambda state: True,				
			"Science (Stone Fruit)": lambda state: lunar_island(state, player),		
			"Magic (Blue Gem)": lambda state: blue_gems(state, player),
			"Magic (Living Log)": lambda state: True,				
			"Magic (Glommer's Goop)": lambda state: has_survived_num_days(11, state, player),
			"Magic (Dark Petals)": lambda state: True,				
			"Magic (Red Gem)": lambda state: red_gems(state, player),
			"Magic (Slurper Pelt)": lambda state: ruins_exploration(state, player),				
			"Magic (Blue Spore)": lambda state: is_winter(state, player) and cave_exploration(state, player) and bug_catching(state, player),
			"Magic (Red Spore)": lambda state: is_summer(state, player) and cave_exploration(state, player) and bug_catching(state, player),					
			"Magic (Green Spore)": lambda state: is_spring(state, player) and cave_exploration(state, player) and bug_catching(state, player),				
			"Magic (Broken Shell)": lambda state: cave_exploration(state, player),				
			"Magic (Leafy Meat)": lambda state: leafy_meat(state, player),				
			"Magic (Canary (Volatile))": lambda state: cave_exploration(state, player) and advanced_cooking(state, player),		
			"Magic (Life Giving Amulet)": lambda state: state.has("Life Giving Amulet", player) and red_gems(state, player),			
			"Magic (Nightmare Fuel)": lambda state: basic_combat(state, player),			
			"Magic (Cut Reeds)": lambda state: True,					
			"Magic (Volt Goat Horn)": lambda state: basic_combat(state, player),			
			"Magic (Beard Hair)": lambda state: True,				
			"Magic (Glow Berry)": lambda state: ruins_exploration(state, player),								
			"Magic (Tentacle Spots)": lambda state: basic_combat(state, player),			
			"Magic (Health)": lambda state: healing(state, player),					
			"Magic (Sanity)": lambda state: True,					
			"Magic (Telltale Heart)": lambda state: healing(state, player),					
			"Magic (Forget-Me-Lots)": lambda state: basic_farming(state, player),			
			"Magic (Cat Tail)": lambda state: True,					
			"Magic (Bunny Puff)": lambda state: cave_exploration(state, player) and basic_combat(state, player),		
			"Magic (Mosquito Sack)": lambda state: True,						
			"Magic (Spider Gland)": lambda state: True,				
			"Magic (Monster Jerky)": lambda state: state.has("Drying Rack", player),				
			"Magic (Pig Skin)": lambda state: basic_combat(state, player),					
			"Magic (Batilisk Wing)": lambda state: True,				
			"Magic (Stinger)": lambda state: True,					
			"Magic (Papyrus)": lambda state: True,		
			"Magic (Green Cap)": lambda state: True,				
			"Magic (Blue Cap)": lambda state: True,					
			"Magic (Red Cap)": lambda state: True,						
			"Magic (Iridescent Gem)": lambda state: state.has_any(["Iridescent Gem", "Mooncaller Staff"],player),			
			"Magic (Desert Stone)": lambda state: reached_summer(state, player) and storm_protection(state, player),		
			"Magic (Naked Nostrils)": lambda state: cave_exploration(state, player),			
			"Magic (Frog Legs)": lambda state: True,		
			"Magic (Spoiled Fish)": lambda state: sea_fishing(state, player) and has_survived_num_days(15, state, player),	
			"Magic (Spoiled Fish Morsel)": lambda state: fishing(state, player) and  has_survived_num_days(10, state, player),
			"Magic (Rot)": lambda state: has_survived_num_days(10, state, player),				
			"Magic (Rotten Egg)": lambda state: advanced_cooking(state, player) and has_survived_num_days(20, state, player),		
			"Magic (Carrat)": lambda state: lunar_island(state, player),				
			"Magic (Moleworm)": lambda state: True,		
			"Magic (Fireflies)": lambda state: bug_catching(state, player),
			"Magic (Bulbous Lightbug)": lambda state: cave_exploration(state, player) and bug_catching(state, player),			
			"Magic (Rabbit)": lambda state: True,	
			"Magic (Butterfly)": lambda state: bug_catching(state, player),			
			"Magic (Mosquito)": lambda state: bug_catching(state, player),		
			"Magic (Bee)": lambda state: bug_catching(state, player),					
			"Magic (Killer Bee)": lambda state: bug_catching(state, player),	
			"Magic (Crustashine)": lambda state: moon_quay_exploration(state, player),				
			"Magic (Crow)": lambda state: state.has("Bird Trap", player),						
			"Magic (Redbird)": lambda state: state.has("Bird Trap", player),					
			"Magic (Snowbird)": lambda state: state.has("Bird Trap", player) and is_winter(state, player),					
			"Magic (Canary)": lambda state: state.has_all(["Friendly Scarecrow", "Boards", "Bird Trap"], player),								
			"Magic (Puffin)": lambda state: state.has("Bird Trap", player) and basic_boating(state, player),											
			"Think Tank (Freshwater Fish)": lambda state: freshwater_fishing(state, player),
			"Think Tank (Live Eel)": lambda state: cave_exploration(state, player) and freshwater_fishing(state, player),
			"Think Tank (Runty Guppy)": lambda state: sea_fishing(state, player),
			"Think Tank (Needlenosed Squirt)": lambda state: sea_fishing(state, player),
			"Think Tank (Bitty Baitfish)": lambda state: sea_fishing(state, player),
			"Think Tank (Smolt Fry)": lambda state: sea_fishing(state, player),
			"Think Tank (Popperfish)": lambda state: sea_fishing(state, player),
			"Think Tank (Fallounder)": lambda state: advanced_boating(state, player) and sea_fishing(state, player),
			"Think Tank (Bloomfin Tuna)": lambda state: reached_spring(state, player) and sea_fishing(state, player),
			"Think Tank (Scorching Sunfish)": lambda state: advanced_boating(state, player) and reached_summer(state, player) and sea_fishing(state, player),
			"Think Tank (Spittlefish)": lambda state: advanced_boating(state, player) and sea_fishing(state, player),
			"Think Tank (Mudfish)": lambda state: sea_fishing(state, player),
			"Think Tank (Deep Bass)": lambda state: advanced_boating(state, player) and sea_fishing(state, player),
			"Think Tank (Dandy Lionfish)": lambda state: advanced_boating(state, player) and sea_fishing(state, player),
			"Think Tank (Black Catfish)": lambda state: advanced_boating(state, player) and sea_fishing(state, player),
			"Think Tank (Corn Cod)": lambda state: advanced_boating(state, player) and sea_fishing(state, player),
			"Think Tank (Ice Bream)": lambda state: advanced_boating(state, player) and reached_winter(state, player) and sea_fishing(state, player),
			"Think Tank (Sweetish Fish)": lambda state: advanced_boating(state, player) and sea_fishing(state, player),
			"Think Tank (Wobster)": lambda state: advanced_boating(state, player) and sea_fishing(state, player),
			"Think Tank (Lunar Wobster)": lambda state: lunar_island(state, player) and sea_fishing(state, player),
			"Pseudoscience (Purple Gem)": lambda state: True,		
			"Pseudoscience (Yellow Gem)": lambda state: True,
			"Pseudoscience (Thulecite)": lambda state: True,
			"Pseudoscience (Orange Gem)": lambda state: True,		
			"Pseudoscience (Green Gem)": lambda state: True,			
			"Celestial (Moon Rock)": lambda state: True,				
			"Celestial (Moon Shard)": lambda state: cave_exploration(state, player) or lunar_island(state, player),
			"Celestial (Moon Shroom)": lambda state: cave_exploration(state, player),					
			"Celestial (Moon Moth)": lambda state: bug_catching(state, player),		
			"Celestial (Lune Tree Blossom)": lambda state: lunar_island(state, player),			
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
	return rules_lookup

def set_rules(dst_world: World) -> None:
	multiworld = dst_world.multiworld
	player = dst_world.player
	rules_lookup = get_rules_lookup(player)
	existing_locations = [item.name for item in multiworld.get_locations(player)]
	excluded = set()

	# Set location rules
	for location_name, rule in rules_lookup["locations"].items():
		if location_name in existing_locations:
			location = multiworld.get_location(location_name, player)
			required = False

			# Set the rule
			set_rule(location, rule)

			# Skip event locations
			if not location_name in location_data_table: continue

			location_data = location_data_table[location_name]
			
			# Add respective research station rule to research locations
			if "research" in location_data.tags:
				if "science" in location_data.tags: add_rule(location, (lambda state: alchemy_engine(state, player)) if "tier_2" in location_data.tags else (lambda state: science_machine(state, player)))
				elif "magic" in location_data.tags: add_rule(location, (lambda state: shadow_manipulator(state, player)) if "tier_2" in location_data.tags else (lambda state: prestihatitor(state, player)))
				elif "celestial" in location_data.tags: add_rule(location, (lambda state: celestial_altar(state, player)) if "tier_2" in location_data.tags else (lambda state: celestial_orb(state, player)))
				elif "seafaring" in location_data.tags: add_rule(location, lambda state: think_tank(state, player))
				elif "ancient" in location_data.tags: add_rule(location, lambda state: ancient_altar(state, player))
			
			elif "farming" in location_data.tags:
				add_rule(location, lambda state: advanced_farming(state, player))

			# Prioritize required bosses
			if (("Ancient Fuelweaver" in multiworld.required_bosses[player].value and "priority_fuelweaver_boss" in location_data.tags)
			or	("Celestial Champion" in multiworld.required_bosses[player].value and "priority_celestial_boss" in location_data.tags)
			):
				required = True
				multiworld.priority_locations[player].value.add(location_name)
			elif ("priority" in location_data.tags
         or (multiworld.boss_locations[player].current_key == "prioritized" and "boss" in location_data.tags and not "excluded" in location_data.tags)
			):
				# Prioritize generic priority tag
				multiworld.priority_locations[player].value.add(location_name)
			# Exclude from having progression items if it meets the conditions
			if not required and ("excluded" in location_data.tags 
		 	or (not multiworld.seasonal_locations[player].value and "seasonal" in location_data.tags)
         or (multiworld.boss_locations[player].current_key == "none" and "boss" in location_data.tags)
         or (multiworld.boss_locations[player].current_key == "easy" and "raidboss" in location_data.tags)
         or (multiworld.skill_level[player].current_key == "easy" and "advanced" in location_data.tags)
         or (multiworld.skill_level[player].current_key != "expert" and "expert" in location_data.tags)
			):
				excluded.add(location_name)

	exclusion_rules(multiworld, player, excluded)
	
