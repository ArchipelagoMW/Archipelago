import typing
from collections.abc import Callable

from BaseClasses import CollectionState
from worlds.generic.Rules import exclusion_rules
from worlds.AutoWorld import World

from . import Constants

# Helper functions
# moved from logicmixin

def has_iron_ingots(state: CollectionState, player: int) -> bool:
    return state.has('Progressive Tools', player) and state.has('Progressive Resource Crafting', player)

def has_copper_ingots(state: CollectionState, player: int) -> bool:
    return state.has('Progressive Tools', player) and state.has('Progressive Resource Crafting', player)

def has_gold_ingots(state: CollectionState, player: int) -> bool: 
    return state.has('Progressive Resource Crafting', player) and (state.has('Progressive Tools', player, 2) or state.can_reach('The Nether', 'Region', player))

def has_diamond_pickaxe(state: CollectionState, player: int) -> bool:
    return state.has('Progressive Tools', player, 3) and has_iron_ingots(state, player)

def craft_crossbow(state: CollectionState, player: int) -> bool: 
    return state.has('Archery', player) and has_iron_ingots(state, player)

def has_bottle(state: CollectionState, player: int) -> bool: 
    return state.has('Bottles', player) and state.has('Progressive Resource Crafting', player)

def has_spyglass(state: CollectionState, player: int) -> bool:
    return has_copper_ingots(state, player) and state.has('Spyglass', player) and can_adventure(state, player)

def can_enchant(state: CollectionState, player: int) -> bool: 
    return state.has('Enchanting', player) and has_diamond_pickaxe(state, player) # mine obsidian and lapis

def can_use_anvil(state: CollectionState, player: int) -> bool: 
    return state.has('Enchanting', player) and state.has('Progressive Resource Crafting', player, 2) and has_iron_ingots(state, player)

def fortress_loot(state: CollectionState, player: int) -> bool: # saddles, blaze rods, wither skulls
    return state.can_reach('Nether Fortress', 'Region', player) and basic_combat(state, player)

def can_brew_potions(state: CollectionState, player: int) -> bool:
    return state.has('Blaze Rods', player) and state.has('Brewing', player) and has_bottle(state, player)

def can_piglin_trade(state: CollectionState, player: int) -> bool:
    return has_gold_ingots(state, player) and (
                state.can_reach('The Nether', 'Region', player) or 
                state.can_reach('Bastion Remnant', 'Region', player))

def overworld_villager(state: CollectionState, player: int) -> bool:
    village_region = state.multiworld.get_region('Village', player).entrances[0].parent_region.name
    if village_region == 'The Nether': # 2 options: cure zombie villager or build portal in village
        return (state.can_reach('Zombie Doctor', 'Location', player) or
                (has_diamond_pickaxe(state, player) and state.can_reach('Village', 'Region', player)))
    elif village_region == 'The End':
        return state.can_reach('Zombie Doctor', 'Location', player)
    return state.can_reach('Village', 'Region', player)

def enter_stronghold(state: CollectionState, player: int) -> bool:
    return state.has('Blaze Rods', player) and state.has('Brewing', player) and state.has('3 Ender Pearls', player)

# Difficulty-dependent functions
def combat_difficulty(state: CollectionState, player: int) -> bool:
    return state.multiworld.combat_difficulty[player].current_key

def can_adventure(state: CollectionState, player: int) -> bool:
    death_link_check = not state.multiworld.death_link[player] or state.has('Bed', player)
    if combat_difficulty(state, player) == 'easy':
        return state.has('Progressive Weapons', player, 2) and has_iron_ingots(state, player) and death_link_check
    elif combat_difficulty(state, player) == 'hard':
        return True
    return (state.has('Progressive Weapons', player) and death_link_check and 
        (state.has('Progressive Resource Crafting', player) or state.has('Campfire', player)))

def basic_combat(state: CollectionState, player: int) -> bool:
    if combat_difficulty(state, player) == 'easy': 
        return state.has('Progressive Weapons', player, 2) and state.has('Progressive Armor', player) and \
               state.has('Shield', player) and has_iron_ingots(state, player)
    elif combat_difficulty(state, player) == 'hard': 
        return True
    return state.has('Progressive Weapons', player) and (state.has('Progressive Armor', player) or state.has('Shield', player)) and has_iron_ingots(state, player)

def complete_raid(state: CollectionState, player: int) -> bool: 
    reach_regions = state.can_reach('Village', 'Region', player) and state.can_reach('Pillager Outpost', 'Region', player)
    if combat_difficulty(state, player) == 'easy': 
        return reach_regions and \
               state.has('Progressive Weapons', player, 3) and state.has('Progressive Armor', player, 2) and \
               state.has('Shield', player) and state.has('Archery', player) and \
               state.has('Progressive Tools', player, 2) and has_iron_ingots(state, player)
    elif combat_difficulty(state, player) == 'hard': # might be too hard?
        return reach_regions and state.has('Progressive Weapons', player, 2) and has_iron_ingots(state, player) and \
               (state.has('Progressive Armor', player) or state.has('Shield', player))
    return reach_regions and state.has('Progressive Weapons', player, 2) and has_iron_ingots(state, player) and \
           state.has('Progressive Armor', player) and state.has('Shield', player)

def can_kill_wither(state: CollectionState, player: int) -> bool: 
    normal_kill = state.has("Progressive Weapons", player, 3) and state.has("Progressive Armor", player, 2) and can_brew_potions(state, player) and can_enchant(state, player)
    if combat_difficulty(state, player) == 'easy': 
        return fortress_loot(state, player) and normal_kill and state.has('Archery', player)
    elif combat_difficulty(state, player) == 'hard': # cheese kill using bedrock ceilings
        return fortress_loot(state, player) and (normal_kill or state.can_reach('The Nether', 'Region', player) or state.can_reach('The End', 'Region', player))
    return fortress_loot(state, player) and normal_kill

def can_respawn_ender_dragon(state: CollectionState, player: int) -> bool:
    return state.can_reach('The Nether', 'Region', player) and state.can_reach('The End', 'Region', player) and \
        state.has('Progressive Resource Crafting', player) # smelt sand into glass

def can_kill_ender_dragon(state: CollectionState, player: int) -> bool:
    if combat_difficulty(state, player) == 'easy': 
        return state.has("Progressive Weapons", player, 3) and state.has("Progressive Armor", player, 2) and \
               state.has('Archery', player) and can_brew_potions(state, player) and can_enchant(state, player)
    if combat_difficulty(state, player) == 'hard': 
        return (state.has('Progressive Weapons', player, 2) and state.has('Progressive Armor', player)) or \
               (state.has('Progressive Weapons', player, 1) and state.has('Bed', player))
    return state.has('Progressive Weapons', player, 2) and state.has('Progressive Armor', player) and state.has('Archery', player)

def has_structure_compass(state: CollectionState, entrance_name: str, player: int) -> bool:
    if not state.multiworld.structure_compasses[player]:
        return True
    return state.has(f"Structure Compass ({state.multiworld.get_entrance(entrance_name, player).connected_region.name})", player)


def get_rules_lookup(player: int):
    rules_lookup: typing.Dict[str, typing.List[Callable[[CollectionState], bool]]] = {
        "entrances": {
            "Nether Portal": lambda state: (state.has('Flint and Steel', player) and 
                (state.has('Bucket', player) or state.has('Progressive Tools', player, 3)) and 
                has_iron_ingots(state, player)),
            "End Portal": lambda state: enter_stronghold(state, player) and state.has('3 Ender Pearls', player, 4),
            "Overworld Structure 1": lambda state: (can_adventure(state, player) and has_structure_compass(state, "Overworld Structure 1", player)),
            "Overworld Structure 2": lambda state: (can_adventure(state, player) and has_structure_compass(state, "Overworld Structure 2", player)),
            "Nether Structure 1": lambda state: (can_adventure(state, player) and has_structure_compass(state, "Nether Structure 1", player)),
            "Nether Structure 2": lambda state: (can_adventure(state, player) and has_structure_compass(state, "Nether Structure 2", player)),
            "The End Structure": lambda state: (can_adventure(state, player) and has_structure_compass(state, "The End Structure", player)),
        },
        "locations": {
            "Ender Dragon": lambda state: can_respawn_ender_dragon(state, player) and can_kill_ender_dragon(state, player),
            "Wither": lambda state: can_kill_wither(state, player),
            "Blaze Rods": lambda state: fortress_loot(state, player),

            "Who is Cutting Onions?": lambda state: can_piglin_trade(state, player),
            "Oh Shiny": lambda state: can_piglin_trade(state, player),
            "Suit Up": lambda state: state.has("Progressive Armor", player) and has_iron_ingots(state, player),
            "Very Very Frightening": lambda state: (state.has("Channeling Book", player) and 
                can_use_anvil(state, player) and can_enchant(state, player) and overworld_villager(state, player)),
            "Hot Stuff": lambda state: state.has("Bucket", player) and has_iron_ingots(state, player),
            "Free the End": lambda state: can_respawn_ender_dragon(state, player) and can_kill_ender_dragon(state, player),
            "A Furious Cocktail": lambda state: (can_brew_potions(state, player) and
                state.has("Fishing Rod", player) and  # Water Breathing
                state.can_reach("The Nether", "Region", player) and  # Regeneration, Fire Resistance, gold nuggets
                state.can_reach("Village", "Region", player) and  # Night Vision, Invisibility
                state.can_reach("Bring Home the Beacon", "Location", player)),  # Resistance
            "Bring Home the Beacon": lambda state: (can_kill_wither(state, player) and 
                has_diamond_pickaxe(state, player) and state.has("Progressive Resource Crafting", player, 2)),
            "Not Today, Thank You": lambda state: state.has("Shield", player) and has_iron_ingots(state, player),
            "Isn't It Iron Pick": lambda state: state.has("Progressive Tools", player, 2) and has_iron_ingots(state, player),
            "Local Brewery": lambda state: can_brew_potions(state, player),
            "The Next Generation": lambda state: can_respawn_ender_dragon(state, player) and can_kill_ender_dragon(state, player),
            "Fishy Business": lambda state: state.has("Fishing Rod", player),
            "This Boat Has Legs": lambda state: ((fortress_loot(state, player) or complete_raid(state, player)) and 
                state.has("Saddle", player) and state.has("Fishing Rod", player)),
            "Sniper Duel": lambda state: state.has("Archery", player),
            "Great View From Up Here": lambda state: basic_combat(state, player),
            "How Did We Get Here?": lambda state: (can_brew_potions(state, player) and 
                has_gold_ingots(state, player) and  # Absorption
                state.can_reach('End City', 'Region', player) and  # Levitation
                state.can_reach('The Nether', 'Region', player) and  # potion ingredients
                state.has("Fishing Rod", player) and state.has("Archery",player) and  # Pufferfish, Nautilus Shells; spectral arrows
                state.can_reach("Bring Home the Beacon", "Location", player) and  # Haste
                state.can_reach("Hero of the Village", "Location", player)),  # Bad Omen, Hero of the Village
            "Bullseye": lambda state: (state.has("Archery", player) and state.has("Progressive Tools", player, 2) and
                has_iron_ingots(state, player)),
            "Spooky Scary Skeleton": lambda state: basic_combat(state, player),
            "Two by Two": lambda state: has_iron_ingots(state, player) and state.has("Bucket", player) and can_adventure(state, player),
            "Two Birds, One Arrow": lambda state: craft_crossbow(state, player) and can_enchant(state, player),
            "Who's the Pillager Now?": lambda state: craft_crossbow(state, player),
            "Getting an Upgrade": lambda state: state.has("Progressive Tools", player),
            "Tactical Fishing": lambda state: state.has("Bucket", player) and has_iron_ingots(state, player),
            "Zombie Doctor": lambda state: can_brew_potions(state, player) and has_gold_ingots(state, player),
            "Ice Bucket Challenge": lambda state: has_diamond_pickaxe(state, player),
            "Into Fire": lambda state: basic_combat(state, player),
            "War Pigs": lambda state: basic_combat(state, player),
            "Take Aim": lambda state: state.has("Archery", player),
            "Total Beelocation": lambda state: state.has("Silk Touch Book", player) and can_use_anvil(state, player) and can_enchant(state, player),
            "Arbalistic": lambda state: (craft_crossbow(state, player) and state.has("Piercing IV Book", player) and 
                can_use_anvil(state, player) and can_enchant(state, player)),
            "The End... Again...": lambda state: can_respawn_ender_dragon(state, player) and can_kill_ender_dragon(state, player),
            "Acquire Hardware": lambda state: has_iron_ingots(state, player),
            "Not Quite \"Nine\" Lives": lambda state: can_piglin_trade(state, player) and state.has("Progressive Resource Crafting", player, 2),
            "Cover Me With Diamonds": lambda state: (state.has("Progressive Armor", player, 2) and
                state.has("Progressive Tools", player, 2) and has_iron_ingots(state, player)),
            "Sky's the Limit": lambda state: basic_combat(state, player),
            "Hired Help": lambda state: state.has("Progressive Resource Crafting", player, 2) and has_iron_ingots(state, player),
            "Sweet Dreams": lambda state: state.has("Bed", player) or state.can_reach('Village', 'Region', player),
            "You Need a Mint": lambda state: can_respawn_ender_dragon(state, player) and has_bottle(state, player),
            "Monsters Hunted": lambda state: (can_respawn_ender_dragon(state, player) and can_kill_ender_dragon(state, player) and 
                can_kill_wither(state, player) and state.has("Fishing Rod", player)),
            "Enchanter": lambda state: can_enchant(state, player),
            "Voluntary Exile": lambda state: basic_combat(state, player),
            "Eye Spy": lambda state: enter_stronghold(state, player),
            "Serious Dedication": lambda state: (can_brew_potions(state, player) and state.has("Bed", player) and
                has_diamond_pickaxe(state, player) and has_gold_ingots(state, player)),
            "Postmortal": lambda state: complete_raid(state, player),
            "Adventuring Time": lambda state: can_adventure(state, player),
            "Hero of the Village": lambda state: complete_raid(state, player),
            "Hidden in the Depths": lambda state: can_brew_potions(state, player) and state.has("Bed", player) and has_diamond_pickaxe(state, player),
            "Beaconator": lambda state: (can_kill_wither(state, player) and has_diamond_pickaxe(state, player) and
                state.has("Progressive Resource Crafting", player, 2)),
            "Withering Heights": lambda state: can_kill_wither(state, player),
            "A Balanced Diet": lambda state: (has_bottle(state, player) and has_gold_ingots(state, player) and  # honey bottle; gapple
                state.has("Progressive Resource Crafting", player, 2) and state.can_reach('The End', 'Region', player)),  # notch apple, chorus fruit
            "Subspace Bubble": lambda state: has_diamond_pickaxe(state, player),
            "Country Lode, Take Me Home": lambda state: state.can_reach("Hidden in the Depths", "Location", player) and has_gold_ingots(state, player),
            "Bee Our Guest": lambda state: state.has("Campfire", player) and has_bottle(state, player),
            "Uneasy Alliance": lambda state: has_diamond_pickaxe(state, player) and state.has('Fishing Rod', player),
            "Diamonds!": lambda state: state.has("Progressive Tools", player, 2) and has_iron_ingots(state, player),
            "A Throwaway Joke": lambda state: can_adventure(state, player),
            "Sticky Situation": lambda state: state.has("Campfire", player) and has_bottle(state, player),
            "Ol' Betsy": lambda state: craft_crossbow(state, player),
            "Cover Me in Debris": lambda state: (state.has("Progressive Armor", player, 2) and
                state.has("8 Netherite Scrap", player, 2) and state.has("Progressive Resource Crafting", player) and
                has_diamond_pickaxe(state, player) and has_iron_ingots(state, player) and
                can_brew_potions(state, player) and state.has("Bed", player)),
            "Hot Topic": lambda state: state.has("Progressive Resource Crafting", player),
            "The Lie": lambda state: has_iron_ingots(state, player) and state.has("Bucket", player),
            "On a Rail": lambda state: has_iron_ingots(state, player) and state.has('Progressive Tools', player, 2),
            "When Pigs Fly": lambda state: ((fortress_loot(state, player) or complete_raid(state, player)) and 
                state.has("Saddle", player) and state.has("Fishing Rod", player) and can_adventure(state, player)),
            "Overkill": lambda state: (can_brew_potions(state, player) and 
                (state.has("Progressive Weapons", player) or state.can_reach('The Nether', 'Region', player))),
            "Librarian": lambda state: state.has("Enchanting", player),
            "Overpowered": lambda state: (has_iron_ingots(state, player) and 
                state.has('Progressive Tools', player, 2) and basic_combat(state, player)),
            "Wax On": lambda state: (has_copper_ingots(state, player) and state.has('Campfire', player) and
                state.has('Progressive Resource Crafting', player, 2)),
            "Wax Off": lambda state: (has_copper_ingots(state, player) and state.has('Campfire', player) and
                state.has('Progressive Resource Crafting', player, 2)),
            "The Cutest Predator": lambda state: has_iron_ingots(state, player) and state.has('Bucket', player),
            "The Healing Power of Friendship": lambda state: has_iron_ingots(state, player) and state.has('Bucket', player),
            "Is It a Bird?": lambda state: has_spyglass(state, player) and can_adventure(state, player),
            "Is It a Balloon?": lambda state: has_spyglass(state, player),
            "Is It a Plane?": lambda state: has_spyglass(state, player) and can_respawn_ender_dragon(state, player),
            "Surge Protector": lambda state: (state.has("Channeling Book", player) and 
                can_use_anvil(state, player) and can_enchant(state, player) and overworld_villager(state, player)),
            "Light as a Rabbit": lambda state: can_adventure(state, player) and has_iron_ingots(state, player) and state.has('Bucket', player),
            "Glow and Behold!": lambda state: can_adventure(state, player),
            "Whatever Floats Your Goat!": lambda state: can_adventure(state, player),
            "Caves & Cliffs": lambda state: has_iron_ingots(state, player) and state.has('Bucket', player) and state.has('Progressive Tools', player, 2),
            "Feels like home": lambda state: (has_iron_ingots(state, player) and state.has('Bucket', player) and state.has('Fishing Rod', player) and
                (fortress_loot(state, player) or complete_raid(state, player)) and state.has("Saddle", player)),
            "Sound of Music": lambda state: state.has("Progressive Tools", player, 2) and has_iron_ingots(state, player) and basic_combat(state, player),
            "Star Trader": lambda state: (has_iron_ingots(state, player) and state.has('Bucket', player) and
                (state.can_reach("The Nether", 'Region', player) or
                    state.can_reach("Nether Fortress", 'Region', player) or # soul sand for water elevator
                    can_piglin_trade(state, player)) and
                overworld_villager(state, player)),
            "Birthday Song": lambda state: state.can_reach("The Lie", "Location", player) and state.has("Progressive Tools", player, 2) and has_iron_ingots(state, player),
            "Bukkit Bukkit": lambda state: state.has("Bucket", player) and has_iron_ingots(state, player) and can_adventure(state, player),
            "It Spreads": lambda state: can_adventure(state, player) and has_iron_ingots(state, player) and state.has("Progressive Tools", player, 2),
            "Sneak 100": lambda state: can_adventure(state, player) and has_iron_ingots(state, player) and state.has("Progressive Tools", player, 2),
            "When the Squad Hops into Town": lambda state: can_adventure(state, player) and state.has("Lead", player),
            "With Our Powers Combined!": lambda state: can_adventure(state, player) and state.has("Lead", player),
        }
    }
    return rules_lookup


def set_rules(mc_world: World) -> None:
    multiworld = mc_world.multiworld
    player = mc_world.player

    rules_lookup = get_rules_lookup(player)

    # Set entrance rules
    for entrance_name, rule in rules_lookup["entrances"].items():
        multiworld.get_entrance(entrance_name, player).access_rule = rule

    # Set location rules
    for location_name, rule in rules_lookup["locations"].items():
        multiworld.get_location(location_name, player).access_rule = rule

    # Set rules surrounding completion
    bosses = multiworld.required_bosses[player]
    postgame_advancements = set()
    if bosses.dragon:
        postgame_advancements.update(Constants.exclusion_info["ender_dragon"])
    if bosses.wither:
        postgame_advancements.update(Constants.exclusion_info["wither"])

    def location_count(state: CollectionState) -> bool:
        return len([location for location in multiworld.get_locations(player) if
            location.address != None and
            location.can_reach(state)])

    def defeated_bosses(state: CollectionState) -> bool:
        return ((not bosses.dragon or state.has("Ender Dragon", player))
            and (not bosses.wither or state.has("Wither", player)))

    egg_shards = min(multiworld.egg_shards_required[player], multiworld.egg_shards_available[player])
    completion_requirements = lambda state: (location_count(state) >= multiworld.advancement_goal[player]
        and state.has("Dragon Egg Shard", player, egg_shards))
    multiworld.completion_condition[player] = lambda state: completion_requirements(state) and defeated_bosses(state)

    # Set exclusions on hard/unreasonable/postgame
    excluded_advancements = set()
    if not multiworld.include_hard_advancements[player]:
        excluded_advancements.update(Constants.exclusion_info["hard"])
    if not multiworld.include_unreasonable_advancements[player]:
        excluded_advancements.update(Constants.exclusion_info["unreasonable"])
    if not multiworld.include_postgame_advancements[player]:
        excluded_advancements.update(postgame_advancements)
    exclusion_rules(multiworld, player, excluded_advancements)
