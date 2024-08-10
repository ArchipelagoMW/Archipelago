import typing
from collections.abc import Callable

from BaseClasses import CollectionState
from worlds.generic.Rules import exclusion_rules
from worlds.AutoWorld import World

from . import Constants


# Helper functions
# moved from logicmixin

def has_iron_ingots(self, state: CollectionState, player: int) -> bool:
    return state.has('Progressive Tools', player) and state.has('Progressive Resource Crafting', player)


def has_copper_ingots(self, state: CollectionState, player: int) -> bool:
    return state.has('Progressive Tools', player) and state.has('Progressive Resource Crafting', player)


def has_gold_ingots(self, state: CollectionState, player: int) -> bool:
    return state.has('Progressive Resource Crafting', player) and (
            state.has('Progressive Tools', player, 2) or state.can_reach('The Nether', 'Region', player))


def has_diamond_pickaxe(self, state: CollectionState, player: int) -> bool:
    return state.has('Progressive Tools', player, 3) and has_iron_ingots(self, state, player)


def craft_crossbow(self, state: CollectionState, player: int) -> bool:
    return state.has('Archery', player) and has_iron_ingots(self, state, player)


def has_bottle(self, state: CollectionState, player: int) -> bool:
    return state.has('Bottles', player) and state.has('Progressive Resource Crafting', player)


def has_spyglass(self, state: CollectionState, player: int) -> bool:
    return has_copper_ingots(self, state, player) and state.has('Spyglass', player) and can_adventure(self, state,
                                                                                                      player)


def can_enchant(self, state: CollectionState, player: int) -> bool:
    return state.has('Enchanting', player) and has_diamond_pickaxe(self, state, player)  # mine obsidian and lapis


def can_use_anvil(self, state: CollectionState, player: int) -> bool:
    return state.has('Enchanting', player) and state.has('Progressive Resource Crafting', player,
                                                         2) and has_iron_ingots(self, state, player)


def fortress_loot(self, state: CollectionState, player: int) -> bool:  # saddles, blaze rods, wither skulls
    return state.can_reach('Nether Fortress', 'Region', player) and basic_combat(self, state, player)


def can_brew_potions(self, state: CollectionState, player: int) -> bool:
    return state.has('Blaze Rods', player) and state.has('Brewing', player) and has_bottle(self, state, player)


def can_piglin_trade(self, state: CollectionState, player: int) -> bool:
    return has_gold_ingots(self, state, player) and (
            state.can_reach('The Nether', 'Region', player) or
            state.can_reach('Bastion Remnant', 'Region', player))


def overworld_villager(self, state: CollectionState, player: int) -> bool:
    village_region = state.multiworld.get_region('Village', player).entrances[0].parent_region.name
    if village_region == 'The Nether':  # 2 options: cure zombie villager or build portal in village
        return (state.can_reach('Zombie Doctor', 'Location', player) or
                (has_diamond_pickaxe(self, state, player) and state.can_reach('Village', 'Region', player)))
    elif village_region == 'The End':
        return state.can_reach('Zombie Doctor', 'Location', player)
    return state.can_reach('Village', 'Region', player)


def enter_stronghold(self, state: CollectionState, player: int) -> bool:
    return state.has('Blaze Rods', player) and state.has('Brewing', player) and state.has('3 Ender Pearls', player)


# Difficulty-dependent functions
def combat_difficulty(self, state: CollectionState, player: int) -> bool:
    return self.options.combat_difficulty.current_key


def can_adventure(self, state: CollectionState, player: int) -> bool:
    death_link_check = not self.options.death_link.value or state.has('Bed', player)
    if combat_difficulty(self, state, player) == 'easy':
        return state.has('Progressive Weapons', player, 2) and has_iron_ingots(self, state, player) and death_link_check
    elif combat_difficulty(self, state, player) == 'hard':
        return True
    return (state.has('Progressive Weapons', player) and death_link_check and
            (state.has('Progressive Resource Crafting', player) or state.has('Campfire', player)))


def basic_combat(self, state: CollectionState, player: int) -> bool:
    if combat_difficulty(self, state, player) == 'easy':
        return state.has('Progressive Weapons', player, 2) and state.has('Progressive Armor', player) and \
            state.has('Shield', player) and has_iron_ingots(self, state, player)
    elif combat_difficulty(self, state, player) == 'hard':
        return True
    return state.has('Progressive Weapons', player) and (
            state.has('Progressive Armor', player) or state.has('Shield', player)) and has_iron_ingots(self, state,
                                                                                                       player)


def complete_raid(self, state: CollectionState, player: int) -> bool:
    reach_regions = state.can_reach('Village', 'Region', player) and state.can_reach('Pillager Outpost', 'Region',
                                                                                     player)
    if combat_difficulty(self, state, player) == 'easy':
        return reach_regions and \
            state.has('Progressive Weapons', player, 3) and state.has('Progressive Armor', player, 2) and \
            state.has('Shield', player) and state.has('Archery', player) and \
            state.has('Progressive Tools', player, 2) and has_iron_ingots(self, state, player)
    elif combat_difficulty(self, state, player) == 'hard':  # might be too hard?
        return reach_regions and state.has('Progressive Weapons', player, 2) and has_iron_ingots(self, state,
                                                                                                 player) and \
            (state.has('Progressive Armor', player) or state.has('Shield', player))
    return reach_regions and state.has('Progressive Weapons', player, 2) and has_iron_ingots(self, state, player) and \
        state.has('Progressive Armor', player) and state.has('Shield', player)


def can_kill_wither(self, state: CollectionState, player: int) -> bool:
    normal_kill = state.has("Progressive Weapons", player, 3) and state.has("Progressive Armor", player,
                                                                            2) and can_brew_potions(self, state,
                                                                                                    player) and can_enchant(
        self, state, player)
    if combat_difficulty(self, state, player) == 'easy':
        return fortress_loot(self, state, player) and normal_kill and state.has('Archery', player)
    elif combat_difficulty(self, state, player) == 'hard':  # cheese kill using bedrock ceilings
        return fortress_loot(self, state, player) and (
                normal_kill or state.can_reach('The Nether', 'Region', player) or state.can_reach('The End',
                                                                                                  'Region', player))
    return fortress_loot(self, state, player) and normal_kill


def can_respawn_ender_dragon(self, state: CollectionState, player: int) -> bool:
    return state.can_reach('The Nether', 'Region', player) and state.can_reach('The End', 'Region', player) and \
        state.has('Progressive Resource Crafting', player)  # smelt sand into glass


def can_kill_ender_dragon(self, state: CollectionState, player: int) -> bool:
    if combat_difficulty(self, state, player) == 'easy':
        return state.has("Progressive Weapons", player, 3) and state.has("Progressive Armor", player, 2) and \
            state.has('Archery', player) and can_brew_potions(self, state, player) and can_enchant(self, state, player)
    if combat_difficulty(self, state, player) == 'hard':
        return (state.has('Progressive Weapons', player, 2) and state.has('Progressive Armor', player)) or \
            (state.has('Progressive Weapons', player, 1) and state.has('Bed', player))
    return state.has('Progressive Weapons', player, 2) and state.has('Progressive Armor', player) and state.has(
        'Archery', player)


def has_structure_compass(self, state: CollectionState, entrance_name: str, player: int) -> bool:
    if not self.options.structure_compasses.value:
        return True
    return state.has(
        f"Structure Compass ({state.multiworld.get_entrance(entrance_name, player).connected_region.name})", player)


def get_rules_lookup(self, player: int):
    rules_lookup = {
        "entrances": {
            "Nether Portal": lambda state: state.has('Flint and Steel', player)
                                           and (
                                                   state.has('Bucket', player)
                                                   or state.has('Progressive Tools', player, 3)
                                           )
                                           and has_iron_ingots(self, state, player),
            "End Portal": lambda state: enter_stronghold(self, state, player)
                                        and state.has('3 Ender Pearls', player, 4),
            "Overworld Structure 1": lambda state: can_adventure(self, state, player)
                                                   and has_structure_compass(self, state, "Overworld Structure 1", player),
            "Overworld Structure 2": lambda state: can_adventure(self, state, player)
                                                   and has_structure_compass(self, state, "Overworld Structure 2", player),
            "Nether Structure 1": lambda state: can_adventure(self, state, player)
                                                and has_structure_compass(self, state, "Nether Structure 1", player),
            "Nether Structure 2": lambda state: can_adventure(self, state, player)
                                                and has_structure_compass(self, state, "Nether Structure 2", player),
            "The End Structure": lambda state: can_adventure(self, state, player)
                                               and has_structure_compass(self, state, "The End Structure", player),
        },
        "locations": {
            "Ender Dragon": lambda state: can_respawn_ender_dragon(self, state, player)
                                          and can_kill_ender_dragon(self, state, player),
            "Wither": lambda state: can_kill_wither(self, state, player),
            "Blaze Rods": lambda state: fortress_loot(self, state, player),
            "Who is Cutting Onions?": lambda state: can_piglin_trade(self, state, player),
            "Oh Shiny": lambda state: can_piglin_trade(self, state, player),
            "Suit Up": lambda state: state.has("Progressive Armor", player)
                                     and has_iron_ingots(self, state, player),
            "Very Very Frightening": lambda state: state.has("Channeling Book", player)
                                                   and can_use_anvil(self, state, player)
                                                   and can_enchant(self, state, player)
                                                   and overworld_villager(self, state, player),
            "Hot Stuff": lambda state: state.has("Bucket", player)
                                       and has_iron_ingots(self, state, player),
            "Free the End": lambda state: can_respawn_ender_dragon(self, state, player)
                                          and can_kill_ender_dragon(self, state, player),
            "A Furious Cocktail": lambda state: (can_brew_potions(self, state, player)
                                                 and state.has("Fishing Rod", player)  # Water Breathing
                                                 and state.can_reach("The Nether", "Region", player)  # Regeneration, Fire Resistance, gold nuggets
                                                 and state.can_reach("Village", "Region", player)  # Night Vision, Invisibility
                                                 and state.can_reach("Bring Home the Beacon", "Location", player)),
            # Resistance
            "Bring Home the Beacon": lambda state: can_kill_wither(self, state, player)
                                                   and has_diamond_pickaxe(self, state, player)
                                                   and state.has("Progressive Resource Crafting", player, 2),
            "Not Today, Thank You": lambda state: state.has("Shield", player)
                                                  and has_iron_ingots(self, state, player),
            "Isn't It Iron Pick": lambda state: state.has("Progressive Tools", player, 2)
                                                and has_iron_ingots(self, state, player),
            "Local Brewery": lambda state: can_brew_potions(self, state, player),
            "The Next Generation": lambda state: can_respawn_ender_dragon(self, state, player)
                                                 and can_kill_ender_dragon(self, state, player),
            "Fishy Business": lambda state: state.has("Fishing Rod", player),
            "This Boat Has Legs": lambda state: (
                                                    fortress_loot(self, state, player)
                                                    or complete_raid(self, state, player)
                                                 )
                                                and state.has("Saddle", player)
                                                and state.has("Fishing Rod", player),
            "Sniper Duel": lambda state: state.has("Archery", player),
            "Great View From Up Here": lambda state: basic_combat(self, state, player),
            "How Did We Get Here?": lambda state: (can_brew_potions(self, state, player)
                                                   and has_gold_ingots(self, state, player)  # Absorption
                                                   and state.can_reach('End City', 'Region', player)  # Levitation
                                                   and state.can_reach('The Nether', 'Region', player)  # potion ingredients
                                                   and state.has("Fishing Rod", player)  # Pufferfish, Nautilus Shells; spectral arrows
                                                   and state.has("Archery", player)
                                                   and state.can_reach("Bring Home the Beacon", "Location", player)  # Haste
                                                   and state.can_reach("Hero of the Village", "Location", player)),  # Bad Omen, Hero of the Village
            "Bullseye": lambda state: state.has("Archery", player)
                                      and state.has("Progressive Tools", player, 2)
                                      and has_iron_ingots(self, state, player),
            "Spooky Scary Skeleton": lambda state: basic_combat(self, state, player),
            "Two by Two": lambda state: has_iron_ingots(self, state, player)
                                        and state.has("Bucket", player)
                                        and can_adventure(self, state, player),
            "Two Birds, One Arrow": lambda state: craft_crossbow(self, state, player)
                                                  and can_enchant(self, state, player),
            "Who's the Pillager Now?": lambda state: craft_crossbow(self, state, player),
            "Getting an Upgrade": lambda state: state.has("Progressive Tools", player),
            "Tactical Fishing": lambda state: state.has("Bucket", player)
                                              and has_iron_ingots(self, state, player),
            "Zombie Doctor": lambda state: can_brew_potions(self, state, player)
                                           and has_gold_ingots(self, state, player),
            "Ice Bucket Challenge": lambda state: has_diamond_pickaxe(self, state, player),
            "Into Fire": lambda state: basic_combat(self, state, player),
            "War Pigs": lambda state: basic_combat(self, state, player),
            "Take Aim": lambda state: state.has("Archery", player),
            "Total Beelocation": lambda state: state.has("Silk Touch Book", player)
                                               and can_use_anvil(self, state, player)
                                               and can_enchant(self, state, player),
            "Arbalistic": lambda state: (craft_crossbow(self, state, player)
                                         and state.has("Piercing IV Book", player)
                                         and can_use_anvil(self, state, player)
                                         and can_enchant(self, state, player)
                                         ),
            "The End... Again...": lambda state: can_respawn_ender_dragon(self, state, player)
                                                 and can_kill_ender_dragon(self, state, player),
            "Acquire Hardware": lambda state: has_iron_ingots(self, state, player),
            "Not Quite \"Nine\" Lives": lambda state: can_piglin_trade(self, state, player)
                                                      and state.has("Progressive Resource Crafting", player, 2),
            "Cover Me With Diamonds": lambda state: state.has("Progressive Armor", player, 2)
                                                    and state.has("Progressive Tools", player, 2)
                                                    and has_iron_ingots(self, state, player),
            "Sky's the Limit": lambda state: basic_combat(self, state, player),
            "Hired Help": lambda state: state.has("Progressive Resource Crafting", player, 2)
                                        and has_iron_ingots(self, state, player),
            "Sweet Dreams": lambda state: state.has("Bed", player) or state.can_reach('Village', 'Region', player),
            "You Need a Mint": lambda state: can_respawn_ender_dragon(self, state, player)
                                             and has_bottle(self, state, player),
            "Monsters Hunted": lambda state: (can_respawn_ender_dragon(self, state, player)
                                              and can_kill_ender_dragon(self, state, player)
                                              and can_kill_wither(self, state, player)
                                              and state.has("Fishing Rod", player)),
            "Enchanter": lambda state: can_enchant(self, state, player),
            "Voluntary Exile": lambda state: basic_combat(self, state, player),
            "Eye Spy": lambda state: enter_stronghold(self, state, player),
            "Serious Dedication": lambda state: (can_brew_potions(self, state, player)
                                                 and state.has("Bed", player)
                                                 and has_diamond_pickaxe(self, state, player)
                                                 and has_gold_ingots(self, state, player)),
            "Postmortal": lambda state: complete_raid(self, state, player),
            "Adventuring Time": lambda state: can_adventure(self, state, player),
            "Hero of the Village": lambda state: complete_raid(self, state, player),
            "Hidden in the Depths": lambda state: can_brew_potions(self, state, player)
                                                  and state.has("Bed", player)
                                                  and has_diamond_pickaxe(self, state, player),
            "Beaconator": lambda state: (can_kill_wither(self, state, player)
                                         and has_diamond_pickaxe(self, state, player)
                                         and state.has("Progressive Resource Crafting", player, 2)),
            "Withering Heights": lambda state: can_kill_wither(self, state, player),
            "A Balanced Diet": lambda state: (has_bottle(self, state, player)
                                              and has_gold_ingots(self, state, player)
                                              and state.has("Progressive Resource Crafting", player, 2)
                                              and state.can_reach('The End', 'Region', player)),
            # notch apple, chorus fruit
            "Subspace Bubble": lambda state: has_diamond_pickaxe(self, state, player),
            "Country Lode, Take Me Home": lambda state: state.can_reach("Hidden in the Depths", "Location", player)
                                                        and has_gold_ingots(self, state, player),
            "Bee Our Guest": lambda state: state.has("Campfire", player)
                                           and has_bottle(self, state, player),
            "Uneasy Alliance": lambda state: has_diamond_pickaxe(self, state, player)
                                             and state.has('Fishing Rod', player),
            "Diamonds!": lambda state: state.has("Progressive Tools", player, 2)
                                       and has_iron_ingots(self, state, player),
            "A Throwaway Joke": lambda state: can_adventure(self, state, player),
            "Sticky Situation": lambda state: state.has("Campfire", player)
                                              and has_bottle(self, state, player),
            "Ol' Betsy": lambda state: craft_crossbow(self, state, player),
            "Cover Me in Debris": lambda state: state.has("Progressive Armor", player, 2)
                                                and state.has("8 Netherite Scrap", player, 2)
                                                and state.has("Progressive Resource Crafting", player)
                                                and has_diamond_pickaxe(self, state, player)
                                                and has_iron_ingots(self, state, player)
                                                and can_brew_potions(self, state, player)
                                                and state.has("Bed", player),
            "Hot Topic": lambda state: state.has("Progressive Resource Crafting", player),
            "The Lie": lambda state: has_iron_ingots(self, state, player)
                                     and state.has("Bucket", player),
            "On a Rail": lambda state: has_iron_ingots(self, state, player)
                                       and state.has('Progressive Tools', player, 2),
            "When Pigs Fly": lambda state:  (
                                                fortress_loot(self, state, player)
                                                or complete_raid(self, state, player)
                                            )
                                            and state.has("Saddle", player)
                                            and state.has("Fishing Rod", player)
                                            and can_adventure(self, state, player),
            "Overkill": lambda state: can_brew_potions(self, state, player)
                                       and (
                                               state.has("Progressive Weapons", player)
                                               or state.can_reach('The Nether', 'Region', player)
                                       ),
            "Librarian": lambda state: state.has("Enchanting", player),
            "Overpowered": lambda state: has_iron_ingots(self, state, player)
                                         and state.has('Progressive Tools', player, 2)
                                         and basic_combat(self, state, player),
            "Wax On": lambda state: has_copper_ingots(self, state, player)
                                    and state.has('Campfire', player)
                                    and state.has('Progressive Resource Crafting', player, 2),
            "Wax Off": lambda state: has_copper_ingots(self, state, player)
                                     and state.has('Campfire', player)
                                     and state.has('Progressive Resource Crafting', player, 2),
            "The Cutest Predator": lambda state: has_iron_ingots(self, state, player)
                                                 and state.has('Bucket', player),
            "The Healing Power of Friendship": lambda state: has_iron_ingots(self, state, player)
                                                             and state.has('Bucket', player),
            "Is It a Bird?": lambda state: has_spyglass(self, state, player)
                                           and can_adventure(self, state, player),
            "Is It a Balloon?": lambda state: has_spyglass(self, state, player),
            "Is It a Plane?": lambda state: has_spyglass(self, state, player)
                                            and can_respawn_ender_dragon(self, state, player),
            "Surge Protector": lambda state: state.has("Channeling Book", player)
                                             and can_use_anvil(self, state, player)
                                             and can_enchant(self, state, player)
                                             and overworld_villager(self, state, player),
            "Light as a Rabbit": lambda state: can_adventure(self, state, player)
                                               and has_iron_ingots(self, state, player)
                                               and state.has('Bucket', player),
            "Glow and Behold!": lambda state: can_adventure(self, state, player),
            "Whatever Floats Your Goat!": lambda state: can_adventure(self, state, player),
            "Caves & Cliffs": lambda state: has_iron_ingots(self, state, player)
                                            and state.has('Bucket', player)
                                            and state.has('Progressive Tools', player, 2),
            "Feels like home": lambda state: has_iron_ingots(self, state, player)
                                              and state.has('Bucket', player)
                                              and state.has('Fishing Rod', player)
                                              and (
                                                fortress_loot(self, state, player)
                                                or complete_raid(self, state, player)
                                              )
                                              and state.has("Saddle", player),
            "Sound of Music": lambda state: state.has("Progressive Tools", player, 2)
                                            and has_iron_ingots(self, state, player)
                                            and basic_combat(self, state, player),
            "Star Trader": lambda state: has_iron_ingots(self, state, player)
                                         and state.has('Bucket', player)
                                         and (
                                           state.can_reach("The Nether", 'Region', player)  # soul sand in nether
                                           or state.can_reach("Nether Fortress", 'Region', player)  # soul sand in fortress if not in nether for water elevator
                                           or can_piglin_trade(self, state, player)  # piglins give soul sand
                                         )
                                         and overworld_villager(self, state, player),
            "Birthday Song": lambda state: state.can_reach("The Lie", "Location", player)
                                           and state.has("Progressive Tools", player, 2)
                                           and has_iron_ingots(self, state, player),
            "Bukkit Bukkit": lambda state: state.has("Bucket", player)
                                           and has_iron_ingots(self, state, player)
                                           and can_adventure(self, state, player),
            "It Spreads": lambda state: can_adventure(self, state, player)
                                        and has_iron_ingots(self, state, player)
                                        and state.has("Progressive Tools", player, 2),
            "Sneak 100": lambda state: can_adventure(self, state, player)
                                       and has_iron_ingots(self, state, player)
                                       and state.has("Progressive Tools", player, 2),
            "When the Squad Hops into Town": lambda state: can_adventure(self, state, player)
                                                           and state.has("Lead", player),
            "With Our Powers Combined!": lambda state: can_adventure(self, state, player)
                                                       and state.has("Lead", player),
        }
    }
    return rules_lookup


def set_rules(self: World) -> None:
    multiworld = self.multiworld
    player = self.player

    rules_lookup = get_rules_lookup(self, player)

    # Set entrance rules
    for entrance_name, rule in rules_lookup["entrances"].items():
        multiworld.get_entrance(entrance_name, player).access_rule = rule

    # Set location rules
    for location_name, rule in rules_lookup["locations"].items():
        multiworld.get_location(location_name, player).access_rule = rule

    # Set rules surrounding completion
    bosses = self.options.required_bosses
    postgame_advancements = set()
    if bosses.dragon:
        postgame_advancements.update(Constants.exclusion_info["ender_dragon"])
    if bosses.wither:
        postgame_advancements.update(Constants.exclusion_info["wither"])

    def location_count(state: CollectionState) -> int:
        return len([location for location in multiworld.get_locations(player) if
                    location.address is not None and
                    location.can_reach(state)])

    def defeated_bosses(state: CollectionState) -> bool:
        return ((not bosses.dragon or state.has("Ender Dragon", player))
                and (not bosses.wither or state.has("Wither", player)))

    egg_shards = min(self.options.egg_shards_required.value, self.options.egg_shards_available.value)
    completion_requirements = lambda state: (location_count(state) >= self.options.advancement_goal.value
                                             and state.has("Dragon Egg Shard", player, egg_shards))
    multiworld.completion_condition[player] = lambda state: completion_requirements(state) and defeated_bosses(state)

    # Set exclusions on hard/unreasonable/postgame
    excluded_advancements = set()
    if not self.options.include_hard_advancements.value:
        excluded_advancements.update(Constants.exclusion_info["hard"])
    if not self.options.include_unreasonable_advancements.value:
        excluded_advancements.update(Constants.exclusion_info["unreasonable"])
    if not self.options.include_postgame_advancements.value:
        excluded_advancements.update(postgame_advancements)
    exclusion_rules(multiworld, player, excluded_advancements)
