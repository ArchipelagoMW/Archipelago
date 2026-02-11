"""Rules for Mystical Ninja Starring Goemon (MN64)."""

from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule

from .Logic.mn64_logic_classes import MN64Items

if TYPE_CHECKING:
    from . import MN64World
    from .Logic.mn64_logic_holder import MN64LogicHolder


def create_logic_holder_from_state(state: CollectionState, player: int, context_name: str = "") -> "MN64LogicHolder":
    """Create a logic holder populated with the current state."""
    from .Logic.mn64_logic_holder import MN64LogicHolder

    # Use a global holder instance to maintain door tracking across evaluations
    if not hasattr(create_logic_holder_from_state, '_holder_instance'):
        create_logic_holder_from_state._holder_instance = MN64LogicHolder()
    
    holder = create_logic_holder_from_state._holder_instance
    
    # Reset context but keep door tracking
    holder.reset_lock_tracking()
    holder._current_location_context = context_name

    # Update holder with current state - Keys
    holder.silver_key_count = state.count(MN64Items.SILVER_KEY.value, player)
    holder.gold_key_count = state.count(MN64Items.GOLD_KEY.value, player)
    holder.diamond_key_count = state.count(MN64Items.DIAMOND_KEY.value, player)
    holder.jump_gym_key = state.has(MN64Items.JUMP_GYM_KEY.value, player)

    # Equipment and Tools
    holder.windup_camera = state.has(MN64Items.WINDUP_CAMERA.value, player) and state.has(MN64Items.EBISUMARU.value, player)
    holder.chain_pipe = state.has(MN64Items.CHAIN_PIPE.value, player) and state.has(MN64Items.GOEMON.value, player)
    holder.ice_kunai = state.has(MN64Items.ICE_KUNAI.value, player) and state.has(MN64Items.SASUKE.value, player)
    holder.medal_of_flames = state.has(MN64Items.MEDAL_OF_FLAMES.value, player) and state.has(MN64Items.GOEMON.value, player)
    holder.bazooka = state.has(MN64Items.BAZOOKA.value, player) and state.has(MN64Items.YAE.value, player)
    holder.flute = state.has(MN64Items.FLUTE.value, player) and state.has(MN64Items.YAE.value, player)
    holder.meat_hammer = state.has(MN64Items.MEAT_HAMMER.value, player) and state.has(MN64Items.EBISUMARU.value, player)

    # Abilities
    holder.mermaid = state.has(MN64Items.MERMAID.value, player) and state.has(MN64Items.YAE.value, player)
    holder.mini_ebisumaru = state.has(MN64Items.MINI_EBISUMARU.value, player) and state.has(MN64Items.EBISUMARU.value, player)
    holder.sudden_impact = state.has(MN64Items.SUDDEN_IMPACT.value, player) and state.has(MN64Items.GOEMON.value, player)
    holder.jetpack = state.has(MN64Items.JETPACK.value, player) and state.has(MN64Items.SASUKE.value, player)

    # Characters
    holder.goemon = state.has(MN64Items.GOEMON.value, player)
    holder.yae = state.has(MN64Items.YAE.value, player)
    holder.ebisumaru = state.has(MN64Items.EBISUMARU.value, player)
    holder.sasuke = state.has(MN64Items.SASUKE.value, player)

    # Character Upgrades
    holder.sasuke_battery_1 = state.has(MN64Items.SASUKE_BATTERY_1.value, player)
    holder.sasuke_battery_2 = state.has(MN64Items.SASUKE_BATTERY_2.value, player)
    holder.strength_upgrade_1 = state.has(MN64Items.STRENGTH_UPGRADE_1.value, player)
    holder.strength_upgrade_2 = state.has(MN64Items.STRENGTH_UPGRADE_2.value, player)

    # Boss Defeats (Event Items)
    holder.beat_tsurami = state.has(MN64Items.beat_tsurami.value, player)
    holder.congo_defeated = state.has(MN64Items.BEAT_CONGO.value, player)
    holder.ghost_toys_defeated = state.has(MN64Items.BEAT_DHARUMANYO.value, player)
    holder.beat_thaisambda = state.has(MN64Items.BEAT_THAISAMBDA.value, player)

    # Event Flags
    holder.power_on_crane_game = state.has(MN64Items.CRANE_GAME_POWER_ON.value, player)
    holder.visited_witch = state.has(MN64Items.VISITED_WITCH.value, player)
    holder.requires_visiting_ghost_toys_entrance_ebisumaru = state.has(MN64Items.VISITED_GHOST_TOYS_ENTRANCE.value, player)
    holder.kyushu_fly = state.has(MN64Items.KUYSHU_FLY.value, player)
    holder.sasuke_dead = state.has(MN64Items.SASUKE_DEAD.value, player)
    holder.event_cucumber_quest_find_priest = state.has(MN64Items.CUCUMBER_QUEST_PRIEST.value, player)
    holder.event_cucumber_quest_need_key = state.has(MN64Items.CUCUMBER_QUEST_START.value, player)
    # holder.fish_quest = state.has(MN64Items.FISH_QUEST_START.value, player)
    holder.moving_boulder_in_forest = state.has(MN64Items.MOVING_BOULDER_IN_FOREST.value, player)
    holder.mokubei_brother = state.has(MN64Items.MOKUBEI_BROTHER.value, player)

    # Quest Items
    holder.superpass = state.has(MN64Items.SUPER_PASS.value, player)
    holder.triton_horn = state.has(MN64Items.TRITON_HORN.value, player)
    holder.cucumber = state.has(MN64Items.CUCUMBER.value, player)
    holder.achilles_heel = state.has(MN64Items.ACHILLES_HEEL.value, player)

    # Miracle Items
    holder.all_miracle_items = (
        state.has(MN64Items.MIRACLE_STAR.value, player)
        and state.has(MN64Items.MIRACLE_SNOW.value, player)
        and state.has(MN64Items.MIRACLE_MOON.value, player)
        and state.has(MN64Items.MIRACLE_FLOWER.value, player)
    )

    # Additional flags that may be referenced in logic
    # holder.bombs - not an actual item in the game (stays False)
    # holder.omitsu_talked - not an actual item in the game (stays False)

    return holder


def set_rules(world: "MN64World") -> None:
    """Set up all access rules for regions and locations."""
    player = world.player
    multiworld = world.multiworld

    # Import all region logic definitions
    from .Logic import (
        mn64_bizen,
        mn64_festival_temple_castle,
        mn64_folypoke_village,
        mn64_ghost_toys_castle,
        mn64_gorgeous_music_castle,
        mn64_gourmet_submarine,
        mn64_iyo,
        mn64_kai,
        mn64_musashi,
        mn64_mutsu,
        mn64_oedo_castle,
        mn64_oedo_town,
        mn64_sanuki,
        mn64_tosa,
        mn64_yamamoto,
        mn64_zazen_town,
    )

    # Collect all region definitions from the imported modules
    all_regions = {}
    all_regions.update(mn64_oedo_town.LogicRegions)
    all_regions.update(mn64_zazen_town.LogicRegions)
    all_regions.update(mn64_musashi.LogicRegions)
    all_regions.update(mn64_mutsu.LogicRegions)
    all_regions.update(mn64_yamamoto.LogicRegions)
    all_regions.update(mn64_sanuki.LogicRegions)
    all_regions.update(mn64_folypoke_village.LogicRegions)
    all_regions.update(mn64_tosa.LogicRegions)
    all_regions.update(mn64_iyo.LogicRegions)
    all_regions.update(mn64_kai.LogicRegions)
    all_regions.update(mn64_bizen.LogicRegions)
    all_regions.update(mn64_oedo_castle.LogicRegions)
    all_regions.update(mn64_ghost_toys_castle.LogicRegions)
    all_regions.update(mn64_festival_temple_castle.LogicRegions)
    all_regions.update(mn64_gorgeous_music_castle.LogicRegions)
    all_regions.update(mn64_gourmet_submarine.LogicRegions)

    # Apply rules for each region's locations
    for region_name, region_data in all_regions.items():
        try:
            region = multiworld.get_region(region_name, player)
        except KeyError:
            continue  # Region doesn't exist yet

        # Set location access rules with unique naming
        location_counter = {}  # Track duplicate names within same region
        for location_logic in region_data.locations:
            # Create the same unique location name as in create_regions()
            base_name = location_logic.name

            # Check if this location name was already used in this region
            if base_name in location_counter:
                location_counter[base_name] += 1
                unique_name = f"{region_name} - {base_name} {location_counter[base_name]}"
            else:
                location_counter[base_name] = 1
                unique_name = f"{region_name} - {base_name}"

            try:
                location = next(loc for loc in region.locations if loc.name == unique_name)
                if location_logic.logic:
                    # Wrap the logic function to use state properly
                    def make_location_rule(logic_func, location_name, player_id):
                        def location_rule(state):
                            holder = create_logic_holder_from_state(state, player_id, location_name)
                            return logic_func(holder)
                        return location_rule
                    
                    set_rule(location, make_location_rule(location_logic.logic, unique_name, player))
            except StopIteration:
                continue  # Location doesn't exist

    # Apply entrance rules
    for region_name, region_data in all_regions.items():
        try:
            region = multiworld.get_region(region_name, player)
        except KeyError:
            continue

        for exit_logic in region_data.exits:
            # Find the entrance that connects to this exit
            for entrance in region.exits:
                if entrance.connected_region and entrance.connected_region.name == exit_logic.destinationRegion:
                    if exit_logic.logic:
                        # Wrap the logic function to use state properly
                        def make_entrance_rule(logic_func, entrance_name, player_id):
                            def entrance_rule(state):
                                holder = create_logic_holder_from_state(state, player_id, entrance_name)
                                return logic_func(holder)
                            return entrance_rule
                        
                        entrance_name = f"{region_name} -> {exit_logic.destinationRegion}"
                        if exit_logic.consumes_key:
                            entrance_name += f" ({exit_logic.consumes_key} key)"
                        
                        set_rule(entrance, make_entrance_rule(exit_logic.logic, entrance_name, player))
                    break


def has_item(state: CollectionState, player: int, item: str) -> bool:
    """Helper function to check if player has an item."""
    return state.has(item, player)


def count_item(state: CollectionState, player: int, item: str) -> int:
    """Helper function to count how many of an item the player has."""
    return state.count(item, player)


def can_access_region(state: CollectionState, player: int, region: str) -> bool:
    """Helper function to check if player can access a region."""
    return state.can_reach(region, "Region", player)


def can_access_location(state: CollectionState, player: int, location: str) -> bool:
    """Helper function to check if player can access a location."""
    return state.can_reach(location, "Location", player)
