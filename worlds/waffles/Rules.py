
from typing import Dict, TYPE_CHECKING
if TYPE_CHECKING:
    from . import WaffleWorld

from .Names import LocationName, ItemName
from .Options import Goal
from .Levels import level_info_dict, hard_gameplay_levels, very_hard_gameplay_levels

from worlds.generic.Rules import CollectionRule, add_rule
from BaseClasses import CollectionState

class WaffleRules:
    player: int
    world: "WaffleWorld"
    connection_rules: Dict[str, CollectionRule]
    carryless_exit_rules: Dict[str, CollectionRule]
    region_rules: Dict[str, CollectionRule]
    location_rules: Dict[str, CollectionRule]

    def __init__(self, world: "WaffleWorld") -> None:
        self.player = world.player
        self.world = world

    def can_carry(self, state: CollectionState) -> bool:
        return state.has(ItemName.mario_carry, self.player)

    def can_carry_or_yoshi_tongue(self, state: CollectionState) -> bool:
        return self.can_carry(state) or self.has_yoshi_carry(state)
    
    def can_run(self, state: CollectionState) -> bool:
        return state.has(ItemName.mario_run, self.player)
    
    def can_wall_run(self, state: CollectionState) -> bool:
        return state.has(ItemName.mario_run, self.player, 2)
    
    def can_swim(self, state: CollectionState) -> bool:
        return state.has(ItemName.mario_swim, self.player)
    
    def can_climb(self, state: CollectionState) -> bool:
        return state.has(ItemName.mario_climb, self.player)
    
    def can_spin_jump(self, state: CollectionState) -> bool:
        return state.has(ItemName.mario_spin_jump, self.player)
    
    def has_mushroom(self, state: CollectionState) -> bool:
        return state.has(ItemName.progressive_powerup, self.player, 1)
    
    def has_fire_flower(self, state: CollectionState) -> bool:
        return state.has(ItemName.progressive_powerup, self.player, 2)
    
    def has_feather(self, state: CollectionState) -> bool:
        return state.has(ItemName.progressive_powerup, self.player, 3)
    
    def has_super_star(self, state: CollectionState) -> bool:
        return state.has(ItemName.super_star_active, self.player, 2)
    
    def has_p_balloon(self, state: CollectionState) -> bool:
        return state.has(ItemName.p_balloon, self.player)
    
    def has_p_switch(self, state: CollectionState) -> bool:
        return state.has(ItemName.p_switch, self.player)
    
    def has_yoshi(self, state: CollectionState) -> bool:
        return state.has(ItemName.yoshi, self.player) and self.can_get_green_yoshi(state)
    
    def has_yoshi_carry(self, state: CollectionState) -> bool:
        return state.has(ItemName.yoshi, self.player, 2) and self.can_get_green_yoshi(state)
    
    def has_special_world(self, state: CollectionState) -> bool:
        return state.has(ItemName.special_world_clear, self.player)
    
    def has_ysp(self, state: CollectionState) -> bool:
        return state.has(ItemName.yellow_switch_palace, self.player)
    
    def has_gsp(self, state: CollectionState) -> bool:
        return state.has(ItemName.green_switch_palace, self.player)

    def has_rsp(self, state: CollectionState) -> bool:
        return state.has(ItemName.red_switch_palace, self.player)

    def has_bsp(self, state: CollectionState) -> bool:
        return state.has(ItemName.blue_switch_palace, self.player)
    
    def has_midway_points(self, state: CollectionState) -> bool:
        return state.has(ItemName.midway_point, self.player)
    
    def has_item_box(self, state: CollectionState) -> bool:
        return state.has(ItemName.item_box, self.player)
    
    def has_extra_defense(self, state: CollectionState) -> bool:
        return state.has(ItemName.extra_defense, self.player)

    def has_tokens(self, state: CollectionState) -> bool:
        return state.has(ItemName.yoshi_egg, self.player, self.world.required_egg_count)


    def can_cape_fly(self, state: CollectionState) -> bool:
        return self.has_feather(state) and self.can_run(state)
    
    def can_yoshi_fly(self, state: CollectionState) -> bool:
        return self.has_yoshi_carry(state) and (self.has_special_world(state) or self.can_get_blue_yoshi(state))
    
    def can_fly(self, state: CollectionState) -> bool:
        return self.can_cape_fly(state) or self.can_yoshi_fly(state)
    
    def butter_bridge_special_case(self, state: CollectionState) -> bool:
        if self.world.options.enemy_shuffle.value:
            return self.has_rsp(state)
        else:
            return True
        
    def twin_bridges_castle_special_case(self, state: CollectionState) -> bool:
        if self.world.using_ut:
            return self.can_climb(state) or (
                state.has(ItemName.glitched, self.player) and self.can_wall_run(state)
            )
        else:
            return self.can_climb(state)
        
    def forest_ghost_house_special_case(self, state: CollectionState) -> bool:
        if self.world.using_ut:
            return self.has_p_switch(state) or (
                state.has(ItemName.glitched, self.player) and self.can_wall_run(state)
            )
        else:
            return self.has_p_switch(state)
        
    def vanilla_dome_1_special_case(self, state: CollectionState) -> bool:
        if self.world.using_ut:
            return self.can_run(state) and (
                self.has_super_star(state) or self.has_mushroom(state)
            ) or state.has(ItemName.glitched, self.player)
        else:
            return self.can_run(state) and (
                self.has_super_star(state) or self.has_mushroom(state)
            )

    def vanilla_dome_4_special_case(self, state: CollectionState) -> bool:
        if self.world.using_ut:
            return self.can_carry(state) or (state.has(ItemName.glitched, self.player) and (
                self.has_feather(state) or self.has_yoshi(state))
            )
        else:
            return True

    def vanilla_secret_1_special_case(self, state: CollectionState) -> bool:
        if self.world.using_ut:
            return self.can_climb(state) or (
                state.has(ItemName.glitched, self.player) and self.can_wall_run(state)
            )
        else:
            return self.can_climb(state)
        
    def vanilla_secret_3_special_case(self, state: CollectionState) -> bool:
        if self.world.using_ut:
            return self.can_swim(state) or state.has(ItemName.glitched, self.player)
        else:
            return self.can_swim(state)
        
    def cheese_bridge_special_case(self, state: CollectionState) -> bool:
        if self.world.using_ut:
            return self.can_cape_fly(state) or (state.has(ItemName.glitched, self.player) and self.has_yoshi(state))
        else:
            return self.can_cape_fly(state)
    
    def cookie_mountain_special_case(self, state: CollectionState) -> bool:
        if self.world.using_ut:
            return self.can_swim(state) or (
                state.has(ItemName.glitched, self.player) and self.can_wall_run(state)
            )
        else:
            return self.can_swim(state)
        
    def forest_of_illusion_1_special_case(self, state: CollectionState) -> bool:
        if self.world.using_ut:
            return self.has_p_balloon(state) or (
                state.has(ItemName.glitched, self.player) and self.has_yoshi(state)
            )
        else:
            return self.has_p_balloon(state)
        
    def forest_of_illusion_2_special_case(self, state: CollectionState) -> bool:
        if self.world.using_ut and self.world.options.enemy_shuffle.value:
            return state.has(ItemName.super_star_active, self.player, 3) or state.has(ItemName.glitched, self.player)
        elif self.world.options.enemy_shuffle.value:
            return state.has(ItemName.super_star_active, self.player, 3)
        else:
            return True
        
    def forest_of_illusion_3_special_case(self, state: CollectionState) -> bool:
        if self.world.using_ut:
            return (self.can_carry_or_yoshi_tongue(state) and self.can_break_turn_blocks(state)) or (
                state.has(ItemName.glitched, self.player) and self.has_yoshi_carry(state)
            )
        else:
            return self.can_carry_or_yoshi_tongue(state) and self.can_break_turn_blocks(state)
        
    def forest_of_illusion_3_can_pass_big_pipe(self, state: CollectionState) -> bool:
        if self.world.using_ut:
            return self.can_carry(state) or self.has_yoshi(state) or state.has(ItemName.glitched, self.player)
        else:
            return self.can_carry(state) or self.has_yoshi(state)
        
    def forest_secret_special_case(self, state: CollectionState) -> bool:
        if self.world.using_ut:
            return self.has_bsp(state) or state.has(ItemName.glitched, self.player)
        else:
            return self.has_bsp(state)
        
    def chocolate_island_1_special_case(self, state: CollectionState) -> bool:
        if self.world.using_ut:
            return self.has_yoshi(state) or (state.has(ItemName.glitched, self.player) and self.can_pass_munchers(state))
        else:
            return self.has_yoshi(state)
        
    def chocolate_secret_special_case(self, state: CollectionState) -> bool:
        if self.world.using_ut:
            return self.can_run(state) or state.has(ItemName.glitched, self.player)
        else:
            return self.can_run(state)
        
    def valley_of_bowser_3_special_case(self, state: CollectionState) -> bool:
        if self.world.using_ut:
            return self.can_carry(state) or (state.has(ItemName.glitched, self.player) and self.has_yoshi(state))
        else:
            return self.can_carry(state)
        
    def valley_of_bowser_4_special_case(self, state: CollectionState) -> bool:
        if self.world.using_ut:
            return self.can_climb(state) or (state.has(ItemName.glitched, self.player) and self.has_yoshi(state))
        else:
            return self.can_climb(state)
        
    def special_zone_4_special_case(self, state: CollectionState) -> bool:
        if self.world.using_ut:
            return state.has(ItemName.glitched, self.player) or (
                (self.can_carry(state) or self.has_p_switch(state)) and self.has_super_star(state)
            )
        else:
            return (self.can_carry(state) or self.has_p_switch(state)) and self.has_super_star(state)
        
    def special_zone_6_special_case(self, state: CollectionState) -> bool:
        if self.world.using_ut:
            if self.world.options.enemy_shuffle:
                return self.can_swim(state) or (state.has(ItemName.glitched, self.player) and state.has(ItemName.super_star_active, self.player, 2))
            else:
                return self.can_swim(state) or state.has(ItemName.glitched, self.player)
        else:
            return self.can_swim(state)

    def can_break_turn_blocks(self, state: CollectionState) -> bool:
        return self.has_mushroom(state) and self.can_spin_jump(state)
    
    def can_pass_munchers(self, state: CollectionState) -> bool:
        return self.has_mushroom(state) or self.has_yoshi(state)
    
    def can_get_green_yoshi(self, state: CollectionState) -> bool:
        if self.world.options.inventory_yoshi_logic.value:
            return True
        else:
            return (
                state.can_reach_region(LocationName.yoshis_island_2_region, self.player) or \
                state.can_reach_region(LocationName.yoshis_island_3_region, self.player) or \
                state.can_reach_region(LocationName.donut_plains_1_region, self.player) or \
                state.can_reach_region(LocationName.donut_plains_4_region, self.player) or \
                state.can_reach_region(LocationName.vanilla_dome_3_region, self.player) or \
                state.can_reach_region(LocationName.vanilla_secret_2_region, self.player) or \
                (state.can_reach_region(LocationName.butter_bridge_2_region, self.player) and self.can_carry(state)) or \
                (state.can_reach_region(LocationName.cookie_mountain_region, self.player) and self.has_rsp(state)) or \
                state.can_reach_region(LocationName.forest_of_illusion_1_region, self.player) or \
                state.can_reach_region(LocationName.forest_of_illusion_3_region, self.player) or \
                state.can_reach_region(LocationName.chocolate_island_1_region, self.player) or \
                state.can_reach_region(LocationName.chocolate_island_2_region, self.player) or \
                (state.can_reach_region(LocationName.valley_of_bowser_4_region, self.player) and self.can_climb(state)) or \
                state.can_reach_region(LocationName.special_zone_5_region, self.player) or \
                state.can_reach_region(LocationName.special_zone_7_region, self.player) or \
                state.can_reach_region(LocationName.special_zone_8_region, self.player)
            )
        
    def can_get_blue_yoshi(self, state: CollectionState) -> bool:
        if self.world.options.inventory_yoshi_logic.value:
            return True
        else:
            return ((
                    self.can_get_green_yoshi(state) or \
                    self.can_get_red_yoshi(state) or \
                    self.can_get_yellow_yoshi(state)
                ) and (
                    state.can_reach_region(LocationName.cheese_bridge_region, self.player) or \
                    state.can_reach_region(LocationName.special_zone_3_region, self.player) or \
                    state.can_reach_region(LocationName.valley_of_bowser_2_region, self.player)
            )) or state.can_reach_region(LocationName.star_road_2_region, self.player)

    
    def can_get_red_yoshi(self, state: CollectionState) -> bool:
        if self.world.options.inventory_yoshi_logic.value:
            return True
        else:
            return (
                state.can_reach_region(LocationName.star_road_1_region, self.player) or \
                state.can_reach_region(LocationName.star_road_4_region, self.player)
            ) and self.can_carry(state)

    def can_get_yellow_yoshi(self, state: CollectionState) -> bool:
        if self.world.options.inventory_yoshi_logic.value:
            return True
        else:
            return (
                state.can_reach_region(LocationName.star_road_3_region, self.player) or \
                (state.can_reach_region(LocationName.star_road_5_region, self.player) and self.can_cape_fly(state) or self.has_p_switch(state))
            )

    def can_beat_hard_level(self, state: CollectionState, difficulty: int) -> bool:
        if difficulty == 0:
            return self.has_mushroom(state) and (self.has_item_box(state) or self.has_midway_points(state))
        elif difficulty == 1:
            return self.has_mushroom(state)
        else:
            return True

    def can_beat_very_hard_level(self, state: CollectionState, difficulty: int) -> bool:
        if difficulty == 0:
            return self.has_fire_flower(state) and (self.has_midway_points(state) or self.has_item_box(state) or self.has_extra_defense(state))
        elif difficulty == 1:
            return self.has_mushroom(state) and (self.has_midway_points(state) or self.has_item_box(state))
        else:
            return True

    def true(self, state: CollectionState) -> bool:
        return True
    
    def set_smw_rules(self) -> None:
        world = self.world
        multiworld = self.world.multiworld
        game_difficulty = world.options.game_logic_difficulty.value

        # Swap exit rules and use carryless rules if needed
        for level_id, level_info in level_info_dict.items():
            # Process carryless firstD
            if level_id in world.carryless_exits:
                level_name = level_info.levelName
                entrance = f"{level_name} -> {level_name} - Secret Exit"
                self.connection_rules[entrance] = self.carryless_exit_rules[entrance]

            # Process swapped locations later
            if level_id in world.swapped_exits:
                level_name = level_info.levelName
                entrance_1 = f"{level_name} -> {level_name} - Normal Exit"
                entrance_2 = f"{level_name} -> {level_name} - Secret Exit"
                entrance_1_data = self.connection_rules[entrance_1]
                entrance_2_data = self.connection_rules[entrance_2]
                self.connection_rules[entrance_1] = entrance_2_data
                self.connection_rules[entrance_2] = entrance_1_data

        # Build entrance rules
        for entrance_name, rule in self.connection_rules.items():
            entrance = multiworld.get_entrance(entrance_name, self.player)
            entrance.access_rule = rule
            if entrance.parent_region.name in hard_gameplay_levels:
                add_rule(entrance, lambda state: self.can_beat_hard_level(state, game_difficulty))
            elif entrance.parent_region.name in very_hard_gameplay_levels:
                add_rule(entrance, lambda state: self.can_beat_very_hard_level(state, game_difficulty))

        # Build location rules
        for loc in multiworld.get_locations(self.player):
            if loc.name in self.location_rules:
                loc.access_rule = self.location_rules[loc.name]
            
            if loc.parent_region.name in hard_gameplay_levels:
                add_rule(loc, lambda state: self.can_beat_hard_level(state, game_difficulty))
            elif loc.parent_region.name in very_hard_gameplay_levels:
                add_rule(loc, lambda state: self.can_beat_very_hard_level(state, game_difficulty))
            # Add generic rules for valid locations
            if "- Midway Point" in loc.name:
                add_rule(loc, lambda state: self.has_midway_points(state))
            elif " - Green Switch Palace Block" in loc.name:
                add_rule(loc, lambda state: self.has_gsp(state))
            elif " - Yellow Switch Palace Block" in loc.name:
                add_rule(loc, lambda state: self.has_ysp(state))

        # Handle goals
        if world.options.goal == Goal.option_yoshi_house:
            add_rule(world.multiworld.get_location(LocationName.yoshis_house, world.player),
                    lambda state: state.has(ItemName.yoshi_egg, world.player, world.required_egg_count))
        elif world.options.goal == Goal.option_bowser:
            add_rule(world.multiworld.get_location(LocationName.bowser, world.player), 
                     lambda state: state.has(ItemName.mario_carry, world.player) and self.has_tokens(state))

        multiworld.completion_condition[self.player] = lambda state: state.has(ItemName.victory, self.player)


    def set_glitched_rules(self) -> None:
        multiworld = self.world.multiworld

        # Build entrance rules
        # Basically skips adding the hard/very hard item requirements
        for entrance_name, rule in self.connection_rules.items():
            entrance = multiworld.get_entrance(entrance_name, self.player)
            add_rule(entrance, lambda state, r=rule: r(state) and state.has(ItemName.glitched, self.player), combine="or")

        # Build location rules
        # Only process this for hard/very hard levels
        for loc in multiworld.get_locations(self.player):
            if loc.parent_region.name in hard_gameplay_levels or loc.parent_region.name in very_hard_gameplay_levels:
                if loc.name in self.location_rules:
                    glitched_rule = self.location_rules[loc.name]
                else:
                    glitched_rule = lambda state: self.true
                    
                # Add generic rules for valid locations
                if "- Midway Point" in loc.name:
                    glitched_rule = lambda state, rule=glitched_rule: self.has_midway_points(state) and rule(state)
                elif " - Green Switch Palace Block" in loc.name:
                    glitched_rule = lambda state, rule=glitched_rule: self.has_gsp(state) and rule(state)
                elif " - Yellow Switch Palace Block" in loc.name:
                    glitched_rule = lambda state, rule=glitched_rule: self.has_ysp(state) and rule(state)

                add_rule(loc, lambda state, r=glitched_rule: r(state) and state.has(ItemName.glitched, self.player), combine="or")


class WaffleBasicRules(WaffleRules):
    def __init__(self, world: "WaffleWorld") -> None:
        super().__init__(world)


        self.connection_rules = {
            f"{LocationName.yoshis_island_1_region} -> {LocationName.yoshis_island_1_exit_1}": 
                self.true,
            f"{LocationName.yoshis_island_2_region} -> {LocationName.yoshis_island_2_exit_1}": 
                self.true,
            f"{LocationName.yoshis_island_3_region} -> {LocationName.yoshis_island_3_exit_1}": 
                self.true,
            f"{LocationName.yoshis_island_4_region} -> {LocationName.yoshis_island_4_exit_1}": 
                self.true,
            f"{LocationName.yoshis_island_castle_region} -> {LocationName.yoshis_island_castle}": 
                self.can_climb,
                
            f"{LocationName.donut_plains_1_region} -> {LocationName.donut_plains_1_exit_1}": 
                self.true,
            f"{LocationName.donut_plains_1_region} -> {LocationName.donut_plains_1_exit_2}": 
                lambda state: (
                    self.can_carry(state) and (
                        self.has_gsp(state) or
                        self.can_cape_fly(state)
                    )
                ) or self.has_yoshi_carry(state),
            f"{LocationName.donut_plains_2_region} -> {LocationName.donut_plains_2_exit_1}": 
                self.true,
            f"{LocationName.donut_plains_2_region} -> {LocationName.donut_plains_2_exit_2}": 
                lambda state: self.has_yoshi_carry(state) or (
                    self.can_carry(state) and self.can_climb(state) and (
                        self.can_break_turn_blocks(state) or self.has_yoshi(state)
                    )
                ),
            f"{LocationName.donut_plains_3_region} -> {LocationName.donut_plains_3_exit_1}": 
                self.true,
            f"{LocationName.donut_plains_4_region} -> {LocationName.donut_plains_4_exit_1}": 
                self.true,
            f"{LocationName.donut_secret_1_region} -> {LocationName.donut_secret_1_exit_1}": 
                self.can_swim,
            f"{LocationName.donut_secret_1_region} -> {LocationName.donut_secret_1_exit_2}": 
                lambda state: self.can_swim(state) and self.can_carry_or_yoshi_tongue(state) and self.has_p_switch(state),
            f"{LocationName.donut_secret_2_region} -> {LocationName.donut_secret_2_exit_1}": 
                self.true,
            f"{LocationName.donut_ghost_house_region} -> {LocationName.donut_ghost_house_exit_1}": 
                self.can_cape_fly,
            f"{LocationName.donut_ghost_house_region} -> {LocationName.donut_ghost_house_exit_2}": 
                lambda state: self.can_climb(state) or self.can_cape_fly(state),
            f"{LocationName.donut_secret_house_region} -> {LocationName.donut_secret_house_exit_1}": 
                self.has_p_switch,
            f"{LocationName.donut_secret_house_region} -> {LocationName.donut_secret_house_exit_2}": 
                lambda state: self.has_p_switch(state) and self.can_carry(state) and (
                    self.can_climb(state) or self.can_cape_fly(state)
                ),
            f"{LocationName.donut_plains_castle_region} -> {LocationName.donut_plains_castle}": 
                self.true,

            f"{LocationName.vanilla_dome_1_region} -> {LocationName.vanilla_dome_1_exit_1}": 
                self.vanilla_dome_1_special_case,
            f"{LocationName.vanilla_dome_1_region} -> {LocationName.vanilla_dome_1_exit_2}": 
                lambda state: self.can_climb(state) and self.can_carry(state) and (
                    self.has_yoshi(state) or self.has_rsp(state)
                ),
            f"{LocationName.vanilla_dome_2_region} -> {LocationName.vanilla_dome_2_exit_1}": 
                lambda state: self.can_swim(state) and (
                    self.can_climb(state) or self.has_yoshi(state)
                ),
            f"{LocationName.vanilla_dome_2_region} -> {LocationName.vanilla_dome_2_exit_2}": 
                lambda state: self.can_swim(state) and self.can_carry(state) and self.has_p_switch(state) and (
                    self.can_climb(state) or self.has_yoshi(state)
                ),
            f"{LocationName.vanilla_dome_3_region} -> {LocationName.vanilla_dome_3_exit_1}": 
                self.true,
            f"{LocationName.vanilla_dome_4_region} -> {LocationName.vanilla_dome_4_exit_1}": 
                self.true,
            f"{LocationName.vanilla_secret_1_region} -> {LocationName.vanilla_secret_1_exit_1}": 
                self.vanilla_secret_1_special_case,
            f"{LocationName.vanilla_secret_1_region} -> {LocationName.vanilla_secret_1_exit_2}": 
                lambda state: self.vanilla_secret_1_special_case(state) and self.can_carry(state) and self.has_bsp(state),
            f"{LocationName.vanilla_secret_2_region} -> {LocationName.vanilla_secret_2_exit_1}": 
                self.true,
            f"{LocationName.vanilla_secret_3_region} -> {LocationName.vanilla_secret_3_exit_1}": 
                self.vanilla_secret_3_special_case,
            f"{LocationName.vanilla_ghost_house_region} -> {LocationName.vanilla_ghost_house_exit_1}": 
                self.has_p_switch,
            f"{LocationName.vanilla_fortress_region} -> {LocationName.vanilla_fortress}": 
                self.can_swim,
            f"{LocationName.vanilla_dome_castle_region} -> {LocationName.vanilla_dome_castle}": 
                self.true,

            f"{LocationName.butter_bridge_1_region} -> {LocationName.butter_bridge_1_exit_1}": 
                self.butter_bridge_special_case,
            f"{LocationName.butter_bridge_2_region} -> {LocationName.butter_bridge_2_exit_1}": 
                self.true,
            f"{LocationName.cheese_bridge_region} -> {LocationName.cheese_bridge_exit_1}": 
                lambda state: self.can_climb(state) or self.has_yoshi(state),
            f"{LocationName.cheese_bridge_region} -> {LocationName.cheese_bridge_exit_2}": 
                self.cheese_bridge_special_case,
            f"{LocationName.soda_lake_region} -> {LocationName.soda_lake_exit_1}": 
                self.can_swim,
            f"{LocationName.cookie_mountain_region} -> {LocationName.cookie_mountain_exit_1}": 
                self.true,
            f"{LocationName.twin_bridges_castle_region} -> {LocationName.twin_bridges_castle}": 
                self.twin_bridges_castle_special_case,

            f"{LocationName.forest_of_illusion_1_region} -> {LocationName.forest_of_illusion_1_exit_1}": 
                self.true,
            f"{LocationName.forest_of_illusion_1_region} -> {LocationName.forest_of_illusion_1_exit_2}": 
                lambda state: self.can_carry(state) and self.forest_of_illusion_1_special_case(state),
            f"{LocationName.forest_of_illusion_2_region} -> {LocationName.forest_of_illusion_2_exit_1}": 
                lambda state: self.can_swim(state) and self.forest_of_illusion_2_special_case(state),
            f"{LocationName.forest_of_illusion_2_region} -> {LocationName.forest_of_illusion_2_exit_2}": 
                lambda state: self.can_carry_or_yoshi_tongue(state) and self.can_swim(state) and self.forest_of_illusion_2_special_case(state),
            f"{LocationName.forest_of_illusion_3_region} -> {LocationName.forest_of_illusion_3_exit_1}": 
                self.forest_of_illusion_3_can_pass_big_pipe,
            f"{LocationName.forest_of_illusion_3_region} -> {LocationName.forest_of_illusion_3_exit_2}": 
                lambda state: self.forest_of_illusion_3_can_pass_big_pipe(state) and self.forest_of_illusion_3_special_case(state),
            f"{LocationName.forest_of_illusion_4_region} -> {LocationName.forest_of_illusion_4_exit_1}": 
                self.true,
            f"{LocationName.forest_of_illusion_4_region} -> {LocationName.forest_of_illusion_4_exit_2}":
                lambda state: self.can_run(state) and self.can_carry_or_yoshi_tongue(state),
            f"{LocationName.forest_ghost_house_region} -> {LocationName.forest_ghost_house_exit_1}": 
                self.forest_ghost_house_special_case,
            f"{LocationName.forest_ghost_house_region} -> {LocationName.forest_ghost_house_exit_2}": 
                self.forest_ghost_house_special_case,
            f"{LocationName.forest_secret_region} -> {LocationName.forest_secret_exit_1}": 
                self.true,
            f"{LocationName.forest_fortress_region} -> {LocationName.forest_fortress}": 
                self.true,
            f"{LocationName.forest_castle_region} -> {LocationName.forest_castle}": 
                self.true,

            f"{LocationName.chocolate_island_1_region} -> {LocationName.chocolate_island_1_exit_1}": 
                lambda state: self.has_p_switch(state) or self.chocolate_island_1_special_case(state),
            f"{LocationName.chocolate_island_2_region} -> {LocationName.chocolate_island_2_exit_1}": 
                self.true,
            f"{LocationName.chocolate_island_2_region} -> {LocationName.chocolate_island_2_exit_2}": 
                self.can_carry_or_yoshi_tongue,
            f"{LocationName.chocolate_island_3_region} -> {LocationName.chocolate_island_3_exit_1}": 
                lambda state: self.can_climb(state) or self.has_yoshi(state),
            f"{LocationName.chocolate_island_3_region} -> {LocationName.chocolate_island_3_exit_2}": 
                self.can_fly,
            f"{LocationName.chocolate_island_4_region} -> {LocationName.chocolate_island_4_exit_1}": 
                self.true,
            f"{LocationName.chocolate_island_5_region} -> {LocationName.chocolate_island_5_exit_1}": 
                self.true,
            f"{LocationName.chocolate_ghost_house_region} -> {LocationName.chocolate_ghost_house_exit_1}": 
                self.true,
            f"{LocationName.chocolate_fortress_region} -> {LocationName.chocolate_fortress}": 
                self.true,
            f"{LocationName.chocolate_secret_region} -> {LocationName.chocolate_secret_exit_1}": 
                self.chocolate_secret_special_case,
            f"{LocationName.chocolate_castle_region} -> {LocationName.chocolate_castle}": 
                self.true,
            f"{LocationName.sunken_ghost_ship_region} -> {LocationName.sunken_ghost_ship}": 
                self.can_swim,

            f"{LocationName.valley_of_bowser_1_region} -> {LocationName.valley_of_bowser_1_exit_1}": 
                self.true,
            f"{LocationName.valley_of_bowser_2_region} -> {LocationName.valley_of_bowser_2_exit_1}": 
                self.true,
            f"{LocationName.valley_of_bowser_2_region} -> {LocationName.valley_of_bowser_2_exit_2}": 
                self.can_carry,
            f"{LocationName.valley_of_bowser_3_region} -> {LocationName.valley_of_bowser_3_exit_1}": 
                self.true,
            f"{LocationName.valley_of_bowser_4_region} -> {LocationName.valley_of_bowser_4_exit_1}": 
                self.valley_of_bowser_4_special_case,
            f"{LocationName.valley_of_bowser_4_region} -> {LocationName.valley_of_bowser_4_exit_2}": 
                lambda state: self.has_yoshi_carry(state) and self.valley_of_bowser_4_special_case(state),
            f"{LocationName.valley_ghost_house_region} -> {LocationName.valley_ghost_house_exit_1}": 
                self.has_p_switch,
            f"{LocationName.valley_ghost_house_region} -> {LocationName.valley_ghost_house_exit_2}": 
                lambda state: self.has_p_switch(state) and self.can_carry(state) and self.can_run(state),
            f"{LocationName.valley_fortress_region} -> {LocationName.valley_fortress}": 
                self.true,
            f"{LocationName.valley_castle_region} -> {LocationName.valley_castle}": 
                self.true,
            f"{LocationName.front_door} -> {LocationName.bowser_region}": 
                lambda state: self.can_climb(state) and self.can_run(state) and self.can_swim(state) and 
                    self.has_tokens(state),
            f"{LocationName.back_door} -> {LocationName.bowser_region}": 
                self.has_tokens,

            f"{LocationName.star_road_1_region} -> {LocationName.star_road_1_exit_1}": 
                self.can_break_turn_blocks,
            f"{LocationName.star_road_1_region} -> {LocationName.star_road_1_exit_2}": 
                lambda state: self.can_break_turn_blocks(state) and self.can_carry_or_yoshi_tongue(state),
            f"{LocationName.star_road_2_region} -> {LocationName.star_road_2_exit_1}": 
                self.can_swim,
            f"{LocationName.star_road_2_region} -> {LocationName.star_road_2_exit_2}": 
                lambda state: self.can_swim(state) and self.can_carry_or_yoshi_tongue(state),
            f"{LocationName.star_road_3_region} -> {LocationName.star_road_3_exit_1}": 
                self.true,
            f"{LocationName.star_road_3_region} -> {LocationName.star_road_3_exit_2}": 
                lambda state: self.can_carry(state) or (self.has_fire_flower(state) and self.has_yoshi_carry(state)),
            f"{LocationName.star_road_4_region} -> {LocationName.star_road_4_exit_1}": 
                self.true,
            f"{LocationName.star_road_4_region} -> {LocationName.star_road_4_exit_2}": 
                lambda state: self.can_yoshi_fly(state) or (
                    self.can_carry(state) and self.has_gsp(state) and self.has_rsp(state)
                ),
            f"{LocationName.star_road_5_region} -> {LocationName.star_road_5_exit_1}": 
                lambda state: self.has_p_switch(state) or self.can_fly(state),
            f"{LocationName.star_road_5_region} -> {LocationName.star_road_5_exit_2}": 
                lambda state: self.can_yoshi_fly(state) or (
                    self.can_carry(state) and self.can_climb(state) and self.has_p_switch(state) and 
                    self.has_ysp(state) and self.has_gsp(state) and self.has_rsp(state) and self.has_bsp(state)
                ) or (
                    self.can_fly(state) and self.can_carry(state) and self.can_spin_jump(state)
                ),
            f"{LocationName.special_zone_1_region} -> {LocationName.special_zone_1_exit_1}": 
                lambda state: self.can_climb(state) and (
                    self.has_p_switch(state) or self.can_cape_fly(state)
                ),
            f"{LocationName.special_zone_2_region} -> {LocationName.special_zone_2_exit_1}": 
                self.has_p_balloon,
            f"{LocationName.special_zone_3_region} -> {LocationName.special_zone_3_exit_1}": 
                lambda state: self.can_climb(state) or self.has_yoshi(state),
            f"{LocationName.special_zone_4_region} -> {LocationName.special_zone_4_exit_1}": 
                self.special_zone_4_special_case,
            f"{LocationName.special_zone_5_region} -> {LocationName.special_zone_5_exit_1}": 
                self.true,
            f"{LocationName.special_zone_6_region} -> {LocationName.special_zone_6_exit_1}": 
                self.special_zone_6_special_case,
            f"{LocationName.special_zone_7_region} -> {LocationName.special_zone_7_exit_1}": 
                self.can_carry_or_yoshi_tongue,
            f"{LocationName.special_zone_8_region} -> {LocationName.special_zone_8_exit_1}": 
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
        }
    
    
        self.carryless_exit_rules = {
            f"{LocationName.donut_plains_1_region} -> {LocationName.donut_plains_1_exit_2}": 
                lambda state: self.has_gsp(state) or self.can_cape_fly(state) or self.has_yoshi_carry(state),
            f"{LocationName.donut_plains_2_region} -> {LocationName.donut_plains_2_exit_2}": 
                lambda state: self.has_yoshi_carry(state) or (
                    self.can_carry(state) and self.can_climb(state) and (
                        self.can_break_turn_blocks(state) or self.has_yoshi(state)
                    )
                ),
            f"{LocationName.donut_secret_1_region} -> {LocationName.donut_secret_1_exit_2}": 
                lambda state: self.can_swim(state),

            f"{LocationName.vanilla_dome_1_region} -> {LocationName.vanilla_dome_1_exit_2}": 
                lambda state: self.can_climb(state) and (
                    self.has_yoshi(state) or self.has_rsp(state)
                ),
            f"{LocationName.vanilla_dome_2_region} -> {LocationName.vanilla_dome_2_exit_2}": 
                lambda state: self.can_swim(state) and self.can_carry(state) and self.has_p_switch(state) and (
                    self.can_climb(state) or self.has_yoshi(state)
                ),

            f"{LocationName.forest_of_illusion_1_region} -> {LocationName.forest_of_illusion_1_exit_2}": 
                self.forest_of_illusion_1_special_case,
            f"{LocationName.forest_of_illusion_2_region} -> {LocationName.forest_of_illusion_2_exit_2}": 
                lambda state: self.can_swim(state) and self.forest_of_illusion_2_special_case(state),
            f"{LocationName.forest_of_illusion_3_region} -> {LocationName.forest_of_illusion_3_exit_2}": 
                lambda state: self.forest_of_illusion_3_can_pass_big_pipe(state) and self.forest_of_illusion_3_special_case(state),
            f"{LocationName.forest_of_illusion_4_region} -> {LocationName.forest_of_illusion_4_exit_2}":
                lambda state: self.can_run(state) or self.has_yoshi(state),

            f"{LocationName.chocolate_island_2_region} -> {LocationName.chocolate_island_2_exit_2}": 
                self.true,

            f"{LocationName.valley_of_bowser_2_region} -> {LocationName.valley_of_bowser_2_exit_2}": 
                self.true,
            f"{LocationName.valley_of_bowser_4_region} -> {LocationName.valley_of_bowser_4_exit_2}": 
                self.valley_of_bowser_4_special_case,
            f"{LocationName.valley_ghost_house_region} -> {LocationName.valley_ghost_house_exit_2}": 
                lambda state: self.has_p_switch(state) and self.can_run(state),

            f"{LocationName.star_road_1_region} -> {LocationName.star_road_1_exit_2}": 
                self.can_break_turn_blocks,
            f"{LocationName.star_road_2_region} -> {LocationName.star_road_2_exit_2}": 
                self.can_swim,
            f"{LocationName.star_road_3_region} -> {LocationName.star_road_3_exit_2}": 
                lambda state: self.can_carry(state) or self.has_fire_flower(state),
            f"{LocationName.star_road_4_region} -> {LocationName.star_road_4_exit_2}": 
                lambda state: self.can_yoshi_fly(state) or (
                    self.has_gsp(state) and self.has_rsp(state) and (
                        self.can_carry(state) or self.has_feather(state)
                    )
                ),
            f"{LocationName.star_road_5_region} -> {LocationName.star_road_5_exit_2}": 
                lambda state: self.can_yoshi_fly(state) or (
                    self.can_climb(state) and self.has_p_switch(state) and 
                    self.has_ysp(state) and self.has_gsp(state) and self.has_rsp(state) and self.has_bsp(state)
                ) or (
                    self.can_fly(state) and self.can_spin_jump(state)
                ),
        }
    
        self.location_rules = {
            LocationName.yoshis_island_1_dragon:
                self.can_break_turn_blocks,
            LocationName.yoshis_island_1_moon:
                lambda state: self.can_cape_fly(state),
            LocationName.yoshis_island_1_midway:
                self.true,
            LocationName.yoshis_island_1_flying_block_1:
                self.true,
            LocationName.yoshis_island_1_yellow_block_1:
                self.true,
            LocationName.yoshis_island_1_life_block_1:
                self.true,
            LocationName.yoshis_island_1_powerup_block_1:
                self.true,
            LocationName.yoshis_island_1_room_2:
                self.can_break_turn_blocks,

            LocationName.yoshis_island_2_dragon:
                lambda state: self.has_yoshi(state) or self.can_climb(state),
            LocationName.yoshis_island_2_midway:
                self.true,
            LocationName.yoshis_island_2_flying_block_1:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.yoshis_island_2_flying_block_2:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.yoshis_island_2_flying_block_3:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.yoshis_island_2_flying_block_4:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.yoshis_island_2_flying_block_5:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.yoshis_island_2_flying_block_6:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.yoshis_island_2_coin_block_1:
                self.true,
            LocationName.yoshis_island_2_yellow_block_1:
                self.true,
            LocationName.yoshis_island_2_coin_block_2:
                self.true,
            LocationName.yoshis_island_2_coin_block_3:
                self.true,
            LocationName.yoshis_island_2_yoshi_block_1:
                self.true,
            LocationName.yoshis_island_2_coin_block_4:
                self.true,
            LocationName.yoshis_island_2_yoshi_block_2:
                self.true,
            LocationName.yoshis_island_2_coin_block_5:
                self.true,
            LocationName.yoshis_island_2_vine_block_1:
                self.true,
            LocationName.yoshis_island_2_yellow_block_2:
                self.true,

            LocationName.yoshis_island_3_dragon:
                self.has_p_switch,
            LocationName.yoshis_island_3_prize:
                self.true,
            LocationName.yoshis_island_3_midway:
                self.true,
            LocationName.yoshis_island_3_yellow_block_1:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_2:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_3:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_4:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_5:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_6:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_7:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_8:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_9:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_10:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_11:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_12:
                self.true,
            LocationName.yoshis_island_3_yellow_block_13:
                self.true,
            LocationName.yoshis_island_3_yellow_block_14:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.yoshis_island_3_yellow_block_15:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.yoshis_island_3_yellow_block_16:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.yoshis_island_3_yellow_block_17:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.yoshis_island_3_yellow_block_18:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.yoshis_island_3_yellow_block_19:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.yoshis_island_3_yellow_block_20:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.yoshis_island_3_yellow_block_21:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_22:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_23:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_24:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_25:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_26:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_27:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_28:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_29:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_coin_block_1:
                self.true,
            LocationName.yoshis_island_3_yoshi_block_1:
                self.true,
            LocationName.yoshis_island_3_yellow_block_30:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_31:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_32:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_33:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_34:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_35:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_36:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_37:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_38:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_39:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_40:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_41:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_42:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_43:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_44:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_45:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_46:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_47:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_48:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_49:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_50:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_51:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_coin_block_2:
                self.true,
            LocationName.yoshis_island_3_powerup_block_1:
                self.true,
            LocationName.yoshis_island_3_yellow_block_52:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_53:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_54:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_55:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_56:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_57:
                self.true,
            LocationName.yoshis_island_3_yellow_block_58:
                self.true,
            LocationName.yoshis_island_3_yellow_block_59:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_60:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_61:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_62:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_63:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_64:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_65:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_66:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_67:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_68:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_69:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_70:
                self.true,
            LocationName.yoshis_island_3_yellow_block_71:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_72:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_73:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_74:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_75:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_76:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_77:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_78:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_79:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_80:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_81:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_82:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_83:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_84:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_85:
                self.can_yoshi_fly,
            LocationName.yoshis_island_3_yellow_block_86:
                self.can_yoshi_fly,

            LocationName.yoshis_island_4_dragon:
                lambda state: self.has_yoshi(state) or self.can_swim(state) or self.has_p_switch(state),
            LocationName.yoshis_island_4_hidden_1up:
                lambda state: self.has_yoshi(state) or self.can_cape_fly(state),
            LocationName.yoshis_island_4_yellow_block_1:
                self.true,
            LocationName.yoshis_island_4_powerup_block_1:
                self.true,
            LocationName.yoshis_island_4_multi_coin_block_1:
                self.true,
            LocationName.yoshis_island_4_star_block_1:
                self.true,
                
            LocationName.yoshis_island_castle_midway:
                self.can_climb,
            LocationName.yoshis_island_castle_coin_block_1:
                lambda state: self.can_carry(state) or self.can_climb(state),
            LocationName.yoshis_island_castle_coin_block_2:
                lambda state: self.can_carry(state) or self.can_climb(state),
            LocationName.yoshis_island_castle_powerup_block_1:
                lambda state: self.can_carry(state) or self.can_climb(state),
            LocationName.yoshis_island_castle_coin_block_3:
                lambda state: self.can_carry(state) or self.can_climb(state),
            LocationName.yoshis_island_castle_coin_block_4:
                lambda state: self.can_carry(state) or self.can_climb(state),
            LocationName.yoshis_island_castle_flying_block_1:
                self.can_climb,
            LocationName.yoshis_island_castle_room_2:
                self.can_climb,

            LocationName.yellow_switch_palace:
                self.true,

            LocationName.donut_plains_1_dragon:
                lambda state: self.can_climb(state) or self.has_yoshi(state) or self.can_cape_fly(state),
            LocationName.donut_plains_1_hidden_1up:
                self.true,
            LocationName.donut_plains_1_midway:
                self.true,
            LocationName.donut_plains_1_coin_block_1:
                self.true,
            LocationName.donut_plains_1_coin_block_2:
                self.true,
            LocationName.donut_plains_1_yoshi_block_1:
                self.true,
            LocationName.donut_plains_1_vine_block_1:
                self.true,
            LocationName.donut_plains_1_green_block_1:
                self.has_feather,
            LocationName.donut_plains_1_green_block_2:
                self.has_feather,
            LocationName.donut_plains_1_green_block_3:
                self.has_feather,
            LocationName.donut_plains_1_green_block_4:
                self.has_feather,
            LocationName.donut_plains_1_green_block_5:
                self.has_feather,
            LocationName.donut_plains_1_green_block_6:
                self.has_feather,
            LocationName.donut_plains_1_green_block_7:
                self.has_feather,
            LocationName.donut_plains_1_green_block_8:
                self.has_feather,
            LocationName.donut_plains_1_green_block_9:
                self.has_feather,
            LocationName.donut_plains_1_green_block_10:
                self.has_feather,
            LocationName.donut_plains_1_green_block_11:
                self.has_feather,
            LocationName.donut_plains_1_green_block_12:
                self.has_feather,
            LocationName.donut_plains_1_green_block_13:
                self.has_feather,
            LocationName.donut_plains_1_green_block_14:
                self.has_feather,
            LocationName.donut_plains_1_green_block_15:
                self.has_feather,
            LocationName.donut_plains_1_green_block_16:
                self.has_feather,
            LocationName.donut_plains_1_yellow_block_1:
                self.true,
            LocationName.donut_plains_1_yellow_block_2:
                self.true,
            LocationName.donut_plains_1_yellow_block_3:
                self.true,
            LocationName.donut_plains_1_room_2:
                self.has_ysp,

            LocationName.donut_plains_2_dragon:
                self.true,
            LocationName.donut_plains_2_coin_block_1:
                self.true,
            LocationName.donut_plains_2_coin_block_2:
                self.true,
            LocationName.donut_plains_2_coin_block_3:
                self.true,
            LocationName.donut_plains_2_yellow_block_1:
                self.true,
            LocationName.donut_plains_2_powerup_block_1:
                self.true,
            LocationName.donut_plains_2_multi_coin_block_1:
                self.true,
            LocationName.donut_plains_2_flying_block_1:
                self.true,
            LocationName.donut_plains_2_green_block_1:
                self.true,
            LocationName.donut_plains_2_yellow_block_2:
                self.true,
            LocationName.donut_plains_2_vine_block_1:
                lambda state: (self.can_break_turn_blocks(state) and self.can_carry(state)) or self.has_yoshi(state),

            LocationName.donut_plains_3_dragon:
                lambda state: (self.can_break_turn_blocks(state) and self.can_climb(state)) or self.has_yoshi(state) or
                    self.can_cape_fly(state),
            LocationName.donut_plains_3_prize:
                lambda state: (self.can_break_turn_blocks(state) and self.can_climb(state)) or self.has_yoshi(state) or
                    self.can_cape_fly(state),
            LocationName.donut_plains_3_midway:
                self.true,
            LocationName.donut_plains_3_green_block_1:
                self.true,
            LocationName.donut_plains_3_coin_block_1:
                self.true,
            LocationName.donut_plains_3_coin_block_2:
                self.true,
            LocationName.donut_plains_3_vine_block_1:
                self.can_break_turn_blocks,
            LocationName.donut_plains_3_powerup_block_1:
                self.true,

            LocationName.donut_plains_4_dragon:
                self.true,
            LocationName.donut_plains_4_moon:
                self.can_cape_fly,
            LocationName.donut_plains_4_hidden_1up:
                self.can_cape_fly,
            LocationName.donut_plains_4_midway:
                self.true,
            LocationName.donut_plains_4_coin_block_1:
                self.true,
            LocationName.donut_plains_4_powerup_block_1:
                self.true,
            LocationName.donut_plains_4_coin_block_2:
                self.true,
            LocationName.donut_plains_4_yoshi_block_1:
                self.true,

            LocationName.donut_secret_1_dragon:
                self.can_swim,
            LocationName.donut_secret_1_coin_block_1:
                self.can_swim,
            LocationName.donut_secret_1_coin_block_2:
                self.can_swim,
            LocationName.donut_secret_1_powerup_block_1:
                self.can_swim,
            LocationName.donut_secret_1_coin_block_3:
                self.can_swim,
            LocationName.donut_secret_1_powerup_block_2:
                self.can_swim,
            LocationName.donut_secret_1_powerup_block_3:
                lambda state: self.can_swim(state) and self.has_p_balloon(state),
            LocationName.donut_secret_1_life_block_1:
                lambda state: self.can_swim(state) and self.has_p_balloon(state),
            LocationName.donut_secret_1_powerup_block_4:
                lambda state: self.can_swim(state) and self.has_p_balloon(state),
            LocationName.donut_secret_1_powerup_block_5:
                self.can_swim,
            LocationName.donut_secret_1_key_block_1:
                lambda state: self.can_swim(state) and self.can_carry(state) and self.has_p_switch(state),
            LocationName.donut_secret_1_room_2:
                self.can_swim,

            LocationName.donut_secret_2_dragon:
                lambda state: self.can_climb(state) or self.has_yoshi(state),
            LocationName.donut_secret_2_directional_coin_block_1:
                self.true,
            LocationName.donut_secret_2_vine_block_1:
                self.true,
            LocationName.donut_secret_2_star_block_1:
                lambda state: self.can_climb(state) or self.has_yoshi(state),
            LocationName.donut_secret_2_powerup_block_1:
                self.true,
            LocationName.donut_secret_2_star_block_2:
                self.true,

            LocationName.donut_ghost_house_vine_block_1:
                self.true,
            LocationName.donut_ghost_house_directional_coin_block_1:
                self.has_p_switch,
            LocationName.donut_ghost_house_life_block_1:
                self.can_cape_fly,
            LocationName.donut_ghost_house_life_block_2:
                self.can_cape_fly,
            LocationName.donut_ghost_house_life_block_3:
                self.can_cape_fly,
            LocationName.donut_ghost_house_life_block_4:
                self.can_cape_fly,
            LocationName.donut_ghost_house_room_2:
                self.can_cape_fly,
            LocationName.donut_ghost_house_room_5:
                self.has_p_switch,
            LocationName.donut_ghost_house_room_6:
                self.can_climb,

            LocationName.donut_secret_house_powerup_block_1:
                self.true,
            LocationName.donut_secret_house_multi_coin_block_1:
                self.true,
            LocationName.donut_secret_house_life_block_1:
                self.has_p_switch,
            LocationName.donut_secret_house_vine_block_1:
                self.has_p_switch,
            LocationName.donut_secret_house_directional_coin_block_1:
                self.has_p_switch,
            LocationName.donut_secret_house_room_3:
                self.has_p_switch,
            LocationName.donut_secret_house_room_4:
                self.has_p_switch,
            LocationName.donut_secret_house_room_5:
                lambda state: self.has_p_switch(state) and (
                    self.can_climb(state) or self.can_cape_fly(state)
                ),

            LocationName.donut_plains_castle_hidden_1up:
                self.true,
            LocationName.donut_plains_castle_yellow_block_1:
                self.true,
            LocationName.donut_plains_castle_coin_block_1:
                self.true,
            LocationName.donut_plains_castle_powerup_block_1:
                self.true,
            LocationName.donut_plains_castle_coin_block_2:
                self.true,
            LocationName.donut_plains_castle_vine_block_1:
                self.true,
            LocationName.donut_plains_castle_invis_life_block_1:
                self.can_climb,
            LocationName.donut_plains_castle_coin_block_3:
                self.true,
            LocationName.donut_plains_castle_coin_block_4:
                self.true,
            LocationName.donut_plains_castle_coin_block_5:
                self.true,
            LocationName.donut_plains_castle_green_block_1:
                self.true,
            LocationName.donut_plains_castle_room_2:
                self.can_cape_fly,

            LocationName.green_switch_palace:
                self.true,

            LocationName.vanilla_dome_1_dragon:
                lambda state: self.can_carry(state) and self.vanilla_dome_1_special_case(state),
            LocationName.vanilla_dome_1_midway:
                self.vanilla_dome_1_special_case,
            LocationName.vanilla_dome_1_flying_block_1:
                self.true,
            LocationName.vanilla_dome_1_powerup_block_1:
                self.true,
            LocationName.vanilla_dome_1_powerup_block_2:
                self.true,
            LocationName.vanilla_dome_1_coin_block_1:
                self.true,
            LocationName.vanilla_dome_1_life_block_1:
                self.true,
            LocationName.vanilla_dome_1_powerup_block_3:
                self.true,
            LocationName.vanilla_dome_1_vine_block_1:
                lambda state: self.has_rsp(state) or self.can_carry(state) or self.has_yoshi(state),
            LocationName.vanilla_dome_1_star_block_1:
                self.true,
            LocationName.vanilla_dome_1_powerup_block_4:
                self.vanilla_dome_1_special_case,
            LocationName.vanilla_dome_1_coin_block_2:
                self.vanilla_dome_1_special_case,

            LocationName.vanilla_dome_2_dragon:
                lambda state: self.can_swim(state) and self.has_p_switch(state) and self.can_carry(state) and (
                    self.can_climb(state) or self.has_yoshi(state)
                ),
            LocationName.vanilla_dome_2_midway:
                lambda state: self.can_swim(state) and (
                    self.can_climb(state) or self.has_yoshi(state)
                ),
            LocationName.vanilla_dome_2_coin_block_1:
                self.can_swim,
            LocationName.vanilla_dome_2_powerup_block_1:
                self.can_swim,
            LocationName.vanilla_dome_2_coin_block_2:
                self.can_swim,
            LocationName.vanilla_dome_2_coin_block_3:
                self.can_swim,
            LocationName.vanilla_dome_2_vine_block_1:
                self.can_swim,
            LocationName.vanilla_dome_2_invis_life_block_1:
                lambda state: self.can_swim(state) and (
                    self.can_climb(state) or self.has_yoshi(state)
                ),
            LocationName.vanilla_dome_2_coin_block_4:
                lambda state: self.can_swim(state) and (
                    self.can_climb(state) or self.has_yoshi(state)
                ),
            LocationName.vanilla_dome_2_coin_block_5:
                lambda state: self.can_swim(state) and (
                    self.can_climb(state) or self.has_yoshi(state)
                ),
            LocationName.vanilla_dome_2_powerup_block_2:
                lambda state: self.can_swim(state) and (
                    self.can_climb(state) or self.has_yoshi(state)
                ),
            LocationName.vanilla_dome_2_powerup_block_3:
                lambda state: self.can_swim(state) and (
                    self.can_climb(state) or self.has_yoshi(state)
                ),
            LocationName.vanilla_dome_2_powerup_block_4:
                lambda state: self.can_swim(state) and (
                    self.can_climb(state) or self.has_yoshi(state)
                ),
            LocationName.vanilla_dome_2_powerup_block_5:
                lambda state: self.can_swim(state) and (
                    self.can_climb(state) or self.has_yoshi(state)
                ),
            LocationName.vanilla_dome_2_multi_coin_block_1:
                lambda state: self.can_swim(state) and (
                    self.can_climb(state) or self.has_yoshi(state)
                ),
            LocationName.vanilla_dome_2_multi_coin_block_2:
                lambda state: self.can_swim(state) and (
                    self.can_climb(state) or self.has_yoshi(state)
                ),
            LocationName.vanilla_dome_2_room_2:
                lambda state: self.can_swim(state) and (
                    self.can_climb(state) or self.has_yoshi(state)
                ),

            LocationName.vanilla_dome_3_dragon:
                self.true,
            LocationName.vanilla_dome_3_moon:
                self.can_cape_fly,
            LocationName.vanilla_dome_3_midway:
                self.true,
            LocationName.vanilla_dome_3_coin_block_1:
                self.true,
            LocationName.vanilla_dome_3_flying_block_1:
                self.true,
            LocationName.vanilla_dome_3_flying_block_2:
                self.true,
            LocationName.vanilla_dome_3_powerup_block_1:
                self.true,
            LocationName.vanilla_dome_3_flying_block_3:
                self.true,
            LocationName.vanilla_dome_3_invis_coin_block_1:
                self.true,
            LocationName.vanilla_dome_3_powerup_block_2:
                self.true,
            LocationName.vanilla_dome_3_multi_coin_block_1:
                self.true,
            LocationName.vanilla_dome_3_powerup_block_3:
                self.true,
            LocationName.vanilla_dome_3_yoshi_block_1:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.vanilla_dome_3_powerup_block_4:
                self.true,
            LocationName.vanilla_dome_3_pswitch_coin_block_1:
                lambda state: self.can_cape_fly(state) and self.has_p_switch(state),
            LocationName.vanilla_dome_3_pswitch_coin_block_2:
                lambda state: self.can_cape_fly(state) and self.has_p_switch(state),
            LocationName.vanilla_dome_3_pswitch_coin_block_3:
                lambda state: self.can_cape_fly(state) and self.has_p_switch(state),
            LocationName.vanilla_dome_3_pswitch_coin_block_4:
                lambda state: self.can_cape_fly(state) and self.has_p_switch(state),
            LocationName.vanilla_dome_3_pswitch_coin_block_5:
                lambda state: self.can_cape_fly(state) and self.has_p_switch(state),
            LocationName.vanilla_dome_3_pswitch_coin_block_6:
                lambda state: self.can_cape_fly(state) and self.has_p_switch(state),
            LocationName.vanilla_dome_3_room_2:
                self.can_cape_fly,

            LocationName.vanilla_dome_4_dragon:
                self.true,
            LocationName.vanilla_dome_4_hidden_1up:
                self.true,
            LocationName.vanilla_dome_4_powerup_block_1:
                self.true,
            LocationName.vanilla_dome_4_powerup_block_2:
                self.true,
            LocationName.vanilla_dome_4_coin_block_1:
                self.true,
            LocationName.vanilla_dome_4_coin_block_2:
                self.true,
            LocationName.vanilla_dome_4_coin_block_3:
                self.true,
            LocationName.vanilla_dome_4_life_block_1:
                self.true,
            LocationName.vanilla_dome_4_coin_block_4:
                self.true,
            LocationName.vanilla_dome_4_coin_block_5:
                self.true,
            LocationName.vanilla_dome_4_coin_block_6:
                self.true,
            LocationName.vanilla_dome_4_coin_block_7:
                self.true,
            LocationName.vanilla_dome_4_coin_block_8:
                self.vanilla_dome_4_special_case,

            LocationName.vanilla_secret_1_dragon:
                lambda state: self.vanilla_secret_1_special_case(state) and self.can_carry(state),
            LocationName.vanilla_secret_1_coin_block_1:
                self.true,
            LocationName.vanilla_secret_1_powerup_block_1:
                self.true,
            LocationName.vanilla_secret_1_multi_coin_block_1:
                self.true,
            LocationName.vanilla_secret_1_vine_block_1:
                self.true,
            LocationName.vanilla_secret_1_vine_block_2:
                self.vanilla_secret_1_special_case,
            LocationName.vanilla_secret_1_coin_block_2:
                self.vanilla_secret_1_special_case,
            LocationName.vanilla_secret_1_coin_block_3:
                self.vanilla_secret_1_special_case,
            LocationName.vanilla_secret_1_powerup_block_2:
                self.vanilla_secret_1_special_case,
            LocationName.vanilla_secret_1_room_2:
                self.vanilla_secret_1_special_case,
            LocationName.vanilla_secret_1_room_3:
                lambda state: self.vanilla_secret_1_special_case(state) and self.can_carry(state) and self.has_bsp(state),

            LocationName.vanilla_secret_2_dragon:
                self.can_cape_fly,
            LocationName.vanilla_secret_2_yoshi_block_1:
                self.true,
            LocationName.vanilla_secret_2_green_block_1:
                self.true,
            LocationName.vanilla_secret_2_powerup_block_1:
                self.true,
            LocationName.vanilla_secret_2_powerup_block_2:
                self.true,
            LocationName.vanilla_secret_2_multi_coin_block_1:
                self.true,
            LocationName.vanilla_secret_2_gray_pow_block_1:
                self.true,
            LocationName.vanilla_secret_2_coin_block_1:
                self.true,
            LocationName.vanilla_secret_2_coin_block_2:
                self.true,
            LocationName.vanilla_secret_2_coin_block_3:
                self.true,
            LocationName.vanilla_secret_2_coin_block_4:
                self.true,
            LocationName.vanilla_secret_2_coin_block_5:
                self.true,
            LocationName.vanilla_secret_2_coin_block_6:
                self.true,

            LocationName.vanilla_secret_3_dragon:
                self.vanilla_secret_3_special_case,
            LocationName.vanilla_secret_3_powerup_block_1:
                self.vanilla_secret_3_special_case,
            LocationName.vanilla_secret_3_powerup_block_2:
                self.vanilla_secret_3_special_case,
            LocationName.vanilla_secret_3_room_2:
                self.vanilla_secret_3_special_case,

            LocationName.vanilla_ghost_house_dragon:
                self.can_climb,
            LocationName.vanilla_ghost_house_hidden_1up:
                self.true,
            LocationName.vanilla_ghost_house_powerup_block_1:
                self.true,
            LocationName.vanilla_ghost_house_vine_block_1:
                self.true,
            LocationName.vanilla_ghost_house_powerup_block_2:
                self.true,
            LocationName.vanilla_ghost_house_multi_coin_block_1:
                self.true,
            LocationName.vanilla_ghost_house_blue_pow_block_1:
                self.true,
            LocationName.vanilla_ghost_house_room_3:
                self.has_p_switch,
                
            LocationName.vanilla_fortress_hidden_1up:
                self.can_swim,
            LocationName.vanilla_fortress_powerup_block_1:
                self.can_swim,
            LocationName.vanilla_fortress_powerup_block_2:
                self.can_swim,
            LocationName.vanilla_fortress_yellow_block_1:
                self.can_swim,
            LocationName.vanilla_fortress_room_2:
                self.can_swim,

            LocationName.vanilla_dome_castle_life_block_1:
                self.has_mushroom,
            LocationName.vanilla_dome_castle_life_block_2:
                self.has_mushroom,
            LocationName.vanilla_dome_castle_powerup_block_1:
                self.true,
            LocationName.vanilla_dome_castle_life_block_3:
                self.has_p_switch,
            LocationName.vanilla_dome_castle_midway:
                self.has_p_switch,
            LocationName.vanilla_dome_castle_room_2:
                self.has_p_switch,

            LocationName.red_switch_palace:
                self.true,

            LocationName.butter_bridge_1_dragon:
                self.butter_bridge_special_case,
            LocationName.butter_bridge_1_prize:
                self.butter_bridge_special_case,
            LocationName.butter_bridge_1_powerup_block_1:
                self.butter_bridge_special_case,
            LocationName.butter_bridge_1_multi_coin_block_1:
                self.butter_bridge_special_case,
            LocationName.butter_bridge_1_multi_coin_block_2:
                self.butter_bridge_special_case,
            LocationName.butter_bridge_1_multi_coin_block_3:
                self.butter_bridge_special_case,
            LocationName.butter_bridge_1_life_block_1:
                self.butter_bridge_special_case,
            LocationName.butter_bridge_1_room_2:
                self.butter_bridge_special_case,

            LocationName.butter_bridge_2_dragon:
                self.can_fly,
            LocationName.butter_bridge_2_powerup_block_1:
                self.can_carry,
            LocationName.butter_bridge_2_green_block_1:
                self.true,
            LocationName.butter_bridge_2_yoshi_block_1:
                self.can_carry,

            LocationName.cheese_bridge_dragon:
                lambda state: self.can_climb(state) or self.has_yoshi(state),
            LocationName.cheese_bridge_moon:
                self.cheese_bridge_special_case,
            LocationName.cheese_bridge_powerup_block_1:
                self.true,
            LocationName.cheese_bridge_powerup_block_2:
                self.true,
            LocationName.cheese_bridge_wings_block_1:
                self.true,
            LocationName.cheese_bridge_powerup_block_3:
                self.true,
            LocationName.cheese_bridge_room_3:
                self.has_yoshi,

            LocationName.cookie_mountain_dragon:
                lambda state: self.can_climb(state) or self.has_yoshi(state),
            LocationName.cookie_mountain_hidden_1up:
                self.cookie_mountain_special_case,
            LocationName.cookie_mountain_coin_block_1:
                self.true,
            LocationName.cookie_mountain_coin_block_2:
                self.true,
            LocationName.cookie_mountain_coin_block_3:
                self.true,
            LocationName.cookie_mountain_coin_block_4:
                self.true,
            LocationName.cookie_mountain_coin_block_5:
                self.true,
            LocationName.cookie_mountain_coin_block_6:
                self.true,
            LocationName.cookie_mountain_coin_block_7:
                self.true,
            LocationName.cookie_mountain_coin_block_8:
                self.true,
            LocationName.cookie_mountain_coin_block_9:
                self.true,
            LocationName.cookie_mountain_powerup_block_1:
                self.true,
            LocationName.cookie_mountain_life_block_1:
                self.can_climb,
            LocationName.cookie_mountain_vine_block_1:
                self.true,
            LocationName.cookie_mountain_yoshi_block_1:
                self.has_rsp,
            LocationName.cookie_mountain_coin_block_10:
                self.true,
            LocationName.cookie_mountain_coin_block_11:
                self.true,
            LocationName.cookie_mountain_powerup_block_2:
                self.true,
            LocationName.cookie_mountain_coin_block_12:
                self.true,
            LocationName.cookie_mountain_coin_block_13:
                self.true,
            LocationName.cookie_mountain_coin_block_14:
                self.true,
            LocationName.cookie_mountain_coin_block_15:
                self.true,
            LocationName.cookie_mountain_coin_block_16:
                self.true,
            LocationName.cookie_mountain_coin_block_17:
                self.true,
            LocationName.cookie_mountain_coin_block_18:
                self.true,
            LocationName.cookie_mountain_coin_block_19:
                self.true,
            LocationName.cookie_mountain_coin_block_20:
                self.true,
            LocationName.cookie_mountain_coin_block_21:
                self.true,
            LocationName.cookie_mountain_coin_block_22:
                self.true,
            LocationName.cookie_mountain_coin_block_23:
                self.true,
            LocationName.cookie_mountain_coin_block_24:
                self.true,
            LocationName.cookie_mountain_coin_block_25:
                self.true,
            LocationName.cookie_mountain_coin_block_26:
                self.true,
            LocationName.cookie_mountain_coin_block_27:
                self.true,
            LocationName.cookie_mountain_coin_block_28:
                self.true,
            LocationName.cookie_mountain_coin_block_29:
                self.true,
            LocationName.cookie_mountain_coin_block_30:
                self.true,

            LocationName.soda_lake_dragon:
                self.can_swim,
            LocationName.soda_lake_powerup_block_1:
                self.can_swim,
            LocationName.soda_lake_room_2:
                self.can_swim,

            LocationName.twin_bridges_castle_powerup_block_1:
                self.twin_bridges_castle_special_case,

            LocationName.forest_of_illusion_1_powerup_block_1:
                self.true,
            LocationName.forest_of_illusion_1_yoshi_block_1:
                self.true,
            LocationName.forest_of_illusion_1_powerup_block_2:
                self.true,
            LocationName.forest_of_illusion_1_key_block_1:
                self.forest_of_illusion_1_special_case,
            LocationName.forest_of_illusion_1_life_block_1:
                self.true,

            LocationName.forest_of_illusion_2_dragon:
                lambda state: self.can_swim(state) and self.forest_of_illusion_2_special_case(state),
            LocationName.forest_of_illusion_2_green_block_1:
                lambda state: self.can_swim(state) and self.forest_of_illusion_2_special_case(state),
            LocationName.forest_of_illusion_2_powerup_block_1:
                lambda state: self.can_swim(state) and self.forest_of_illusion_2_special_case(state),
            LocationName.forest_of_illusion_2_invis_coin_block_1:
                lambda state: self.can_swim(state) and self.forest_of_illusion_2_special_case(state),
            LocationName.forest_of_illusion_2_invis_coin_block_2:
                lambda state: self.can_swim(state) and self.forest_of_illusion_2_special_case(state),
            LocationName.forest_of_illusion_2_invis_life_block_1:
                lambda state: self.can_swim(state) and self.forest_of_illusion_2_special_case(state),
            LocationName.forest_of_illusion_2_invis_coin_block_3:
                lambda state: self.can_swim(state) and self.forest_of_illusion_2_special_case(state),
            LocationName.forest_of_illusion_2_yellow_block_1:
                lambda state: self.can_swim(state) and self.forest_of_illusion_2_special_case(state),

            LocationName.forest_of_illusion_3_dragon:
                self.forest_of_illusion_3_can_pass_big_pipe,
            LocationName.forest_of_illusion_3_hidden_1up:
                self.forest_of_illusion_3_can_pass_big_pipe,
            LocationName.forest_of_illusion_3_yoshi_block_1:
                self.true,
            LocationName.forest_of_illusion_3_coin_block_1:
                self.true,
            LocationName.forest_of_illusion_3_multi_coin_block_1:
                self.true,
            LocationName.forest_of_illusion_3_coin_block_2:
                self.forest_of_illusion_3_can_pass_big_pipe,
            LocationName.forest_of_illusion_3_multi_coin_block_2:
                self.forest_of_illusion_3_can_pass_big_pipe,
            LocationName.forest_of_illusion_3_coin_block_3:
                self.forest_of_illusion_3_can_pass_big_pipe,
            LocationName.forest_of_illusion_3_coin_block_4:
                self.forest_of_illusion_3_can_pass_big_pipe,
            LocationName.forest_of_illusion_3_coin_block_5:
                self.forest_of_illusion_3_can_pass_big_pipe,
            LocationName.forest_of_illusion_3_coin_block_6:
                self.forest_of_illusion_3_can_pass_big_pipe,
            LocationName.forest_of_illusion_3_coin_block_7:
                self.forest_of_illusion_3_can_pass_big_pipe,
            LocationName.forest_of_illusion_3_coin_block_8:
                self.forest_of_illusion_3_can_pass_big_pipe,
            LocationName.forest_of_illusion_3_coin_block_9:
                self.forest_of_illusion_3_can_pass_big_pipe,
            LocationName.forest_of_illusion_3_coin_block_10:
                self.forest_of_illusion_3_can_pass_big_pipe,
            LocationName.forest_of_illusion_3_coin_block_11:
                self.forest_of_illusion_3_can_pass_big_pipe,
            LocationName.forest_of_illusion_3_coin_block_12:
                self.forest_of_illusion_3_can_pass_big_pipe,
            LocationName.forest_of_illusion_3_coin_block_13:
                self.forest_of_illusion_3_can_pass_big_pipe,
            LocationName.forest_of_illusion_3_coin_block_14:
                self.forest_of_illusion_3_can_pass_big_pipe,
            LocationName.forest_of_illusion_3_coin_block_15:
                self.forest_of_illusion_3_can_pass_big_pipe,
            LocationName.forest_of_illusion_3_coin_block_16:
                self.forest_of_illusion_3_can_pass_big_pipe,
            LocationName.forest_of_illusion_3_coin_block_17:
                self.forest_of_illusion_3_can_pass_big_pipe,
            LocationName.forest_of_illusion_3_coin_block_18:
                self.forest_of_illusion_3_can_pass_big_pipe,
            LocationName.forest_of_illusion_3_coin_block_19:
                self.forest_of_illusion_3_can_pass_big_pipe,
            LocationName.forest_of_illusion_3_coin_block_20:
                self.forest_of_illusion_3_can_pass_big_pipe,
            LocationName.forest_of_illusion_3_coin_block_21:
                self.forest_of_illusion_3_can_pass_big_pipe,
            LocationName.forest_of_illusion_3_coin_block_22:
                self.forest_of_illusion_3_can_pass_big_pipe,
            LocationName.forest_of_illusion_3_coin_block_23:
                self.forest_of_illusion_3_can_pass_big_pipe,
            LocationName.forest_of_illusion_3_coin_block_24:
                self.forest_of_illusion_3_can_pass_big_pipe,

            LocationName.forest_of_illusion_4_dragon:
                lambda state: self.has_yoshi(state) or self.can_carry(state) or 
                    self.has_p_switch(state) or self.has_fire_flower(state),
            LocationName.forest_of_illusion_4_multi_coin_block_1:
                self.true,
            LocationName.forest_of_illusion_4_coin_block_1:
                self.true,
            LocationName.forest_of_illusion_4_coin_block_2:
                self.true,
            LocationName.forest_of_illusion_4_coin_block_3:
                self.true,
            LocationName.forest_of_illusion_4_coin_block_4:
                self.true,
            LocationName.forest_of_illusion_4_powerup_block_1:
                self.true,
            LocationName.forest_of_illusion_4_coin_block_5:
                self.true,
            LocationName.forest_of_illusion_4_coin_block_6:
                self.true,
            LocationName.forest_of_illusion_4_coin_block_7:
                self.true,
            LocationName.forest_of_illusion_4_powerup_block_2:
                self.true,
            LocationName.forest_of_illusion_4_coin_block_8:
                self.true,
            LocationName.forest_of_illusion_4_coin_block_9:
                self.true,
            LocationName.forest_of_illusion_4_coin_block_10:
                self.true,
            LocationName.forest_of_illusion_4_room_2:
                self.can_run,

            LocationName.forest_ghost_house_dragon:
                self.forest_ghost_house_special_case,
            LocationName.forest_ghost_house_moon:
                self.forest_ghost_house_special_case,
            LocationName.forest_ghost_house_coin_block_1:
                self.true,
            LocationName.forest_ghost_house_powerup_block_1:
                self.true,
            LocationName.forest_ghost_house_flying_block_1:
                self.true,
            LocationName.forest_ghost_house_powerup_block_2:
                self.true,
            LocationName.forest_ghost_house_life_block_1:
                self.true,
            LocationName.forest_ghost_house_room_3:
                self.forest_ghost_house_special_case,
            LocationName.forest_ghost_house_room_4:
                self.forest_ghost_house_special_case,

            LocationName.forest_secret_dragon:
                self.true,
            LocationName.forest_secret_powerup_block_1:
                self.true,
            LocationName.forest_secret_powerup_block_2:
                self.true,
            LocationName.forest_secret_life_block_1:
                self.forest_secret_special_case,

            LocationName.forest_fortress_yellow_block_1:
                self.true,
            LocationName.forest_fortress_powerup_block_1:
                self.true,
            LocationName.forest_fortress_life_block_1:
                self.can_cape_fly,
            LocationName.forest_fortress_life_block_2:
                self.can_cape_fly,
            LocationName.forest_fortress_life_block_3:
                self.can_cape_fly,
            LocationName.forest_fortress_life_block_4:
                self.can_cape_fly,
            LocationName.forest_fortress_life_block_5:
                self.can_cape_fly,
            LocationName.forest_fortress_life_block_6:
                self.can_cape_fly,
            LocationName.forest_fortress_life_block_7:
                self.can_cape_fly,
            LocationName.forest_fortress_life_block_8:
                self.can_cape_fly,
            LocationName.forest_fortress_life_block_9:
                self.can_cape_fly,

            LocationName.forest_castle_dragon:
                self.true,
            LocationName.forest_castle_green_block_1:
                self.true,

            LocationName.blue_switch_palace:
                self.true,

            LocationName.chocolate_island_1_dragon:
                lambda state: self.has_p_switch(state) or self.chocolate_island_1_special_case(state),
            LocationName.chocolate_island_1_moon:
                lambda state: self.can_cape_fly(state) or self.chocolate_island_1_special_case(state),
            LocationName.chocolate_island_1_flying_block_1:
                self.true,
            LocationName.chocolate_island_1_flying_block_2:
                lambda state: self.has_p_switch(state) or self.chocolate_island_1_special_case(state),
            LocationName.chocolate_island_1_yoshi_block_1:
                lambda state: self.has_p_switch(state) or self.chocolate_island_1_special_case(state),
            LocationName.chocolate_island_1_green_block_1:
                lambda state: self.has_p_switch(state) or self.chocolate_island_1_special_case(state) and (
                    (self.has_gsp(state) and self.has_bsp(state)) or
                    (self.has_ysp(state) and self.has_bsp(state))
                ),
            LocationName.chocolate_island_1_life_block_1:
                lambda state: self.has_p_switch(state) or self.chocolate_island_1_special_case(state),
            LocationName.chocolate_island_1_room_2:
                lambda state: self.has_p_switch(state) or self.chocolate_island_1_special_case(state),
                
            LocationName.chocolate_island_2_dragon:
                lambda state: self.has_bsp(state) and (
                    self.has_p_switch(state) or self.has_gsp(state) or self.has_yoshi(state) or (
                        self.has_ysp(state) and self.has_rsp(state)
                    )),
            LocationName.chocolate_island_2_hidden_1up:
                self.true,
            LocationName.chocolate_island_2_multi_coin_block_1:
                self.true,
            LocationName.chocolate_island_2_invis_coin_block_1:
                self.true,
            LocationName.chocolate_island_2_yoshi_block_1:
                self.true,
            LocationName.chocolate_island_2_coin_block_1:
                self.true,
            LocationName.chocolate_island_2_coin_block_2:
                self.true,
            LocationName.chocolate_island_2_multi_coin_block_2:
                self.true,
            LocationName.chocolate_island_2_powerup_block_1:
                self.true,
            LocationName.chocolate_island_2_blue_pow_block_1:
                self.true,
            LocationName.chocolate_island_2_yellow_block_1:
                self.true,
            LocationName.chocolate_island_2_yellow_block_2:
                self.true,
            LocationName.chocolate_island_2_green_block_1:
                self.true,
            LocationName.chocolate_island_2_green_block_2:
                self.true,
            LocationName.chocolate_island_2_green_block_3:
                self.true,
            LocationName.chocolate_island_2_green_block_4:
                self.true,
            LocationName.chocolate_island_2_green_block_5:
                self.true,
            LocationName.chocolate_island_2_green_block_6:
                self.true,

            LocationName.chocolate_island_3_dragon:
                self.true,
            LocationName.chocolate_island_3_prize:
                self.true,
            LocationName.chocolate_island_3_powerup_block_1:
                self.true,
            LocationName.chocolate_island_3_powerup_block_2:
                self.true,
            LocationName.chocolate_island_3_powerup_block_3:
                self.true,
            LocationName.chocolate_island_3_green_block_1:
                self.true,
            LocationName.chocolate_island_3_vine_block_1:
                self.true,
            LocationName.chocolate_island_3_life_block_1:
                self.can_fly,
            LocationName.chocolate_island_3_life_block_2:
                self.can_fly,
            LocationName.chocolate_island_3_life_block_3:
                self.can_fly,

            LocationName.chocolate_island_4_dragon:
                lambda state: self.has_p_switch(state) and self.has_feather(state),
            LocationName.chocolate_island_4_yellow_block_1:
                self.has_bsp,
            LocationName.chocolate_island_4_blue_pow_block_1:
                self.true,
            LocationName.chocolate_island_4_powerup_block_1:
                self.true,
            LocationName.chocolate_island_4_room_2:
                self.has_p_switch,

            LocationName.chocolate_island_5_dragon:
                self.true,
            LocationName.chocolate_island_5_yoshi_block_1:
                self.true,
            LocationName.chocolate_island_5_powerup_block_1:
                self.has_p_switch,
            LocationName.chocolate_island_5_life_block_1:
                self.has_p_switch,
            LocationName.chocolate_island_5_yellow_block_1:
                self.has_p_switch,
            LocationName.chocolate_island_5_room_2:
                self.has_p_switch,

            LocationName.chocolate_ghost_house_powerup_block_1:
                self.true,
            LocationName.chocolate_ghost_house_powerup_block_2:
                self.true,
            LocationName.chocolate_ghost_house_life_block_1:
                self.true,

            LocationName.chocolate_secret_powerup_block_1:
                self.true,
            LocationName.chocolate_secret_powerup_block_2:
                self.chocolate_secret_special_case,
            LocationName.chocolate_secret_room_5:
                self.chocolate_secret_special_case,
                
            LocationName.chocolate_fortress_powerup_block_1:
                self.true,
            LocationName.chocolate_fortress_powerup_block_2:
                self.true,
            LocationName.chocolate_fortress_coin_block_1:
                self.true,
            LocationName.chocolate_fortress_coin_block_2:
                self.true,
            LocationName.chocolate_fortress_green_block_1:
                self.true,

            LocationName.chocolate_castle_hidden_1up:
                self.true,
            LocationName.chocolate_castle_yellow_block_1:
                self.true,
            LocationName.chocolate_castle_yellow_block_2:
                self.true,
            LocationName.chocolate_castle_green_block_1:
                self.true,

            LocationName.sunken_ghost_ship_dragon:
                self.can_swim,
            LocationName.sunken_ghost_ship_powerup_block_1:
                self.can_swim,
            LocationName.sunken_ghost_ship_star_block_1:
                self.can_swim,
            LocationName.sunken_ghost_ship_room_2:
                self.can_swim,
            LocationName.sunken_ghost_ship_room_3:
                self.can_swim,

            LocationName.valley_of_bowser_1_dragon:
                self.true,
            LocationName.valley_of_bowser_1_moon:
                self.true,
            LocationName.valley_of_bowser_1_green_block_1:
                self.true,
            LocationName.valley_of_bowser_1_invis_coin_block_1:
                self.true,
            LocationName.valley_of_bowser_1_invis_coin_block_2:
                self.true,
            LocationName.valley_of_bowser_1_invis_coin_block_3:
                self.true,
            LocationName.valley_of_bowser_1_yellow_block_1:
                self.has_feather,
            LocationName.valley_of_bowser_1_yellow_block_2:
                self.has_feather,
            LocationName.valley_of_bowser_1_yellow_block_3:
                self.has_feather,
            LocationName.valley_of_bowser_1_yellow_block_4:
                self.has_feather,
            LocationName.valley_of_bowser_1_vine_block_1:
                self.true,
            LocationName.valley_of_bowser_1_room_2:
                self.can_climb,

            LocationName.valley_of_bowser_2_dragon:
                self.has_yoshi,
            LocationName.valley_of_bowser_2_hidden_1up:
                self.true,
            LocationName.valley_of_bowser_2_powerup_block_1:
                self.true,
            LocationName.valley_of_bowser_2_yellow_block_1:
                self.true,
            LocationName.valley_of_bowser_2_powerup_block_2:
                self.true,
            LocationName.valley_of_bowser_2_wings_block_1:
                self.true,

            LocationName.valley_of_bowser_3_dragon:
                self.true,
            LocationName.valley_of_bowser_3_powerup_block_1:
                self.true,
            LocationName.valley_of_bowser_3_powerup_block_2:
                self.valley_of_bowser_3_special_case,

            LocationName.valley_of_bowser_4_yellow_block_1:
                self.true,
            LocationName.valley_of_bowser_4_powerup_block_1:
                self.true,
            LocationName.valley_of_bowser_4_vine_block_1:
                self.true,
            LocationName.valley_of_bowser_4_yoshi_block_1:
                self.valley_of_bowser_4_special_case,
            LocationName.valley_of_bowser_4_life_block_1:
                lambda state: self.valley_of_bowser_4_special_case(state) and self.can_break_turn_blocks(state),
            LocationName.valley_of_bowser_4_powerup_block_2:
                lambda state: self.valley_of_bowser_4_special_case(state) and self.has_ysp(state),

            LocationName.valley_ghost_house_dragon:
                self.has_p_switch,
            LocationName.valley_ghost_house_pswitch_coin_block_1:
                self.has_p_switch,
            LocationName.valley_ghost_house_multi_coin_block_1:
                self.has_p_switch,
            LocationName.valley_ghost_house_powerup_block_1:
                self.true,
            LocationName.valley_ghost_house_directional_coin_block_1:
                self.has_p_switch,
            LocationName.valley_ghost_house_room_3:
                self.has_p_switch,
            LocationName.valley_ghost_house_room_4:
                self.has_p_switch,

            LocationName.valley_fortress_green_block_1:
                self.true,
            LocationName.valley_fortress_yellow_block_1:
                self.true,
                
            LocationName.valley_castle_dragon:
                self.true,
            LocationName.valley_castle_hidden_1up:
                self.true,
            LocationName.valley_castle_yellow_block_1:
                self.true,
            LocationName.valley_castle_yellow_block_2:
                self.true,
            LocationName.valley_castle_green_block_1:
                self.true,

            LocationName.star_road_1_dragon:
                self.can_break_turn_blocks,
            LocationName.star_road_1_room_2:
                self.can_break_turn_blocks,

            LocationName.star_road_2_star_block_1:
                self.can_swim,
            LocationName.star_road_2_room_2:
                self.can_swim,

            LocationName.star_road_3_key_block_1:
                lambda state: self.can_carry(state) or self.has_fire_flower(state),

            LocationName.star_road_4_powerup_block_1:
                self.true,
            LocationName.star_road_4_green_block_1:
                self.can_yoshi_fly,
            LocationName.star_road_4_green_block_2:
                self.can_yoshi_fly,
            LocationName.star_road_4_green_block_3:
                self.can_yoshi_fly,
            LocationName.star_road_4_green_block_4:
                self.can_yoshi_fly,
            LocationName.star_road_4_green_block_5:
                self.can_yoshi_fly,
            LocationName.star_road_4_green_block_6:
                self.can_yoshi_fly,
            LocationName.star_road_4_green_block_7:
                self.can_yoshi_fly,
            LocationName.star_road_4_key_block_1:
                lambda state: self.can_yoshi_fly(state) or (
                    self.can_carry(state) and self.has_gsp(state) and self.has_rsp(state)
                ),

            LocationName.star_road_5_directional_coin_block_1:
                self.true,
            LocationName.star_road_5_life_block_1:
                self.has_p_switch,
            LocationName.star_road_5_vine_block_1:
                self.has_p_switch,
            LocationName.star_road_5_yellow_block_1:
                self.can_yoshi_fly,
            LocationName.star_road_5_yellow_block_2:
                self.can_yoshi_fly,
            LocationName.star_road_5_yellow_block_3:
                self.can_yoshi_fly,
            LocationName.star_road_5_yellow_block_4:
                self.can_yoshi_fly,
            LocationName.star_road_5_yellow_block_5:
                self.can_yoshi_fly,
            LocationName.star_road_5_yellow_block_6:
                self.can_yoshi_fly,
            LocationName.star_road_5_yellow_block_7:
                self.can_yoshi_fly,
            LocationName.star_road_5_yellow_block_8:
                self.can_yoshi_fly,
            LocationName.star_road_5_yellow_block_9:
                self.can_yoshi_fly,
            LocationName.star_road_5_yellow_block_10:
                self.can_yoshi_fly,
            LocationName.star_road_5_yellow_block_11:
                self.can_yoshi_fly,
            LocationName.star_road_5_yellow_block_12:
                self.can_yoshi_fly,
            LocationName.star_road_5_yellow_block_13:
                self.can_yoshi_fly,
            LocationName.star_road_5_yellow_block_14:
                self.can_yoshi_fly,
            LocationName.star_road_5_yellow_block_15:
                self.can_yoshi_fly,
            LocationName.star_road_5_yellow_block_16:
                self.can_yoshi_fly,
            LocationName.star_road_5_yellow_block_17:
                self.can_yoshi_fly,
            LocationName.star_road_5_yellow_block_18:
                self.can_yoshi_fly,
            LocationName.star_road_5_yellow_block_19:
                lambda state: self.can_yoshi_fly(state) and self.has_gsp(state),
            LocationName.star_road_5_yellow_block_20:
                lambda state: self.can_yoshi_fly(state) and self.has_gsp(state),
            LocationName.star_road_5_green_block_1:
                self.can_yoshi_fly,
            LocationName.star_road_5_green_block_2:
                self.can_yoshi_fly,
            LocationName.star_road_5_green_block_3:
                self.can_yoshi_fly,
            LocationName.star_road_5_green_block_4:
                self.can_yoshi_fly,
            LocationName.star_road_5_green_block_5:
                self.can_yoshi_fly,
            LocationName.star_road_5_green_block_6:
                self.can_yoshi_fly,
            LocationName.star_road_5_green_block_7:
                self.can_yoshi_fly,
            LocationName.star_road_5_green_block_8:
                self.can_yoshi_fly,
            LocationName.star_road_5_green_block_9:
                self.can_yoshi_fly,
            LocationName.star_road_5_green_block_10:
                self.can_yoshi_fly,
            LocationName.star_road_5_green_block_11:
                self.can_yoshi_fly,
            LocationName.star_road_5_green_block_12:
                self.can_yoshi_fly,
            LocationName.star_road_5_green_block_13:
                self.can_yoshi_fly,
            LocationName.star_road_5_green_block_14:
                self.can_yoshi_fly,
            LocationName.star_road_5_green_block_15:
                self.can_yoshi_fly,
            LocationName.star_road_5_green_block_16:
                self.can_yoshi_fly,
            LocationName.star_road_5_green_block_17:
                self.can_yoshi_fly,
            LocationName.star_road_5_green_block_18:
                self.can_yoshi_fly,
            LocationName.star_road_5_green_block_19:
                self.can_yoshi_fly,
            LocationName.star_road_5_green_block_20:
                self.can_yoshi_fly,


            LocationName.special_zone_1_dragon:
                self.can_climb,
            LocationName.special_zone_1_hidden_1up:
                self.can_climb,
            LocationName.special_zone_1_vine_block_1:
                self.true,
            LocationName.special_zone_1_vine_block_2:
                self.true,
            LocationName.special_zone_1_vine_block_3:
                self.true,
            LocationName.special_zone_1_vine_block_4:
                self.true,
            LocationName.special_zone_1_life_block_1:
                self.can_climb,
            LocationName.special_zone_1_vine_block_5:
                self.can_climb,
            LocationName.special_zone_1_blue_pow_block_1:
                self.can_climb,
            LocationName.special_zone_1_vine_block_6:
                self.can_climb,
            LocationName.special_zone_1_powerup_block_1:
                self.can_climb,
            LocationName.special_zone_1_pswitch_coin_block_1:
                lambda state: self.can_climb(state) and self.has_p_switch(state) and self.has_feather(state),
            LocationName.special_zone_1_pswitch_coin_block_2:
                lambda state: self.can_climb(state) and self.has_p_switch(state) and self.has_feather(state),
            LocationName.special_zone_1_pswitch_coin_block_3:
                lambda state: self.can_climb(state) and self.has_p_switch(state) and self.has_feather(state),
            LocationName.special_zone_1_pswitch_coin_block_4:
                lambda state: self.can_climb(state) and self.has_p_switch(state) and self.has_feather(state),
            LocationName.special_zone_1_pswitch_coin_block_5:
                lambda state: self.can_climb(state) and self.has_p_switch(state) and self.has_feather(state),
            LocationName.special_zone_1_pswitch_coin_block_6:
                lambda state: self.can_climb(state) and self.has_p_switch(state) and self.has_feather(state),
            LocationName.special_zone_1_pswitch_coin_block_7:
                lambda state: self.can_climb(state) and self.has_p_switch(state) and self.has_feather(state),
            LocationName.special_zone_1_pswitch_coin_block_8:
                lambda state: self.can_climb(state) and self.has_p_switch(state) and self.has_feather(state),
            LocationName.special_zone_1_pswitch_coin_block_9:
                lambda state: self.can_climb(state) and self.has_p_switch(state) and self.has_feather(state),
            LocationName.special_zone_1_pswitch_coin_block_10:
                lambda state: self.can_climb(state) and self.has_p_switch(state) and self.has_feather(state),
            LocationName.special_zone_1_pswitch_coin_block_11:
                lambda state: self.can_climb(state) and self.has_p_switch(state) and self.has_feather(state),
            LocationName.special_zone_1_pswitch_coin_block_12:
                lambda state: self.can_climb(state) and self.has_p_switch(state) and self.has_feather(state),
            LocationName.special_zone_1_pswitch_coin_block_13:
                lambda state: self.can_climb(state) and self.has_p_switch(state) and self.has_feather(state),
            LocationName.special_zone_1_room_2:
                self.can_climb,

            LocationName.special_zone_2_dragon:
                self.has_p_balloon,
            LocationName.special_zone_2_powerup_block_1:
                self.true,
            LocationName.special_zone_2_coin_block_1:
                self.has_p_balloon,
            LocationName.special_zone_2_coin_block_2:
                self.has_p_balloon,
            LocationName.special_zone_2_powerup_block_2:
                self.has_p_balloon,
            LocationName.special_zone_2_coin_block_3:
                self.has_p_balloon,
            LocationName.special_zone_2_coin_block_4:
                self.has_p_balloon,
            LocationName.special_zone_2_powerup_block_3:
                self.has_p_balloon,
            LocationName.special_zone_2_multi_coin_block_1:
                self.has_p_balloon,
            LocationName.special_zone_2_coin_block_5:
                self.has_p_balloon,
            LocationName.special_zone_2_coin_block_6:
                self.has_p_balloon,

            LocationName.special_zone_3_dragon:
                self.has_yoshi,
            LocationName.special_zone_3_powerup_block_1:
                self.true,
            LocationName.special_zone_3_yoshi_block_1:
                self.true,
            LocationName.special_zone_3_wings_block_1:
                self.true,
            LocationName.special_zone_3_room_3:
                self.has_yoshi,

            LocationName.special_zone_4_dragon:
                self.special_zone_4_special_case,
            LocationName.special_zone_4_powerup_block_1:
                self.special_zone_4_special_case,
            LocationName.special_zone_4_star_block_1:
                lambda state: self.can_carry(state) or self.has_p_switch(state),

            LocationName.special_zone_5_dragon:
                self.true,
            LocationName.special_zone_5_yoshi_block_1:
                self.true,

            LocationName.special_zone_6_dragon:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_powerup_block_1:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_coin_block_1:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_coin_block_2:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_yoshi_block_1:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_life_block_1:
                self.can_swim,
            LocationName.special_zone_6_multi_coin_block_1:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_coin_block_3:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_coin_block_4:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_coin_block_5:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_coin_block_6:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_coin_block_7:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_coin_block_8:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_coin_block_9:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_coin_block_10:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_coin_block_11:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_coin_block_12:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_coin_block_13:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_coin_block_14:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_coin_block_15:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_coin_block_16:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_coin_block_17:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_coin_block_18:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_coin_block_19:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_coin_block_20:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_coin_block_21:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_coin_block_22:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_coin_block_23:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_coin_block_24:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_coin_block_25:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_coin_block_26:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_coin_block_27:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_coin_block_28:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_powerup_block_2:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_coin_block_29:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_coin_block_30:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_coin_block_31:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_coin_block_32:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_coin_block_33:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_room_2:
                self.special_zone_6_special_case,
            LocationName.special_zone_6_room_3:
                self.special_zone_6_special_case,

            LocationName.special_zone_7_dragon:
                self.forest_of_illusion_3_can_pass_big_pipe,
            LocationName.special_zone_7_powerup_block_1:
                self.true,
            LocationName.special_zone_7_yoshi_block_1:
                self.forest_of_illusion_3_can_pass_big_pipe,
            LocationName.special_zone_7_coin_block_1:
                self.forest_of_illusion_3_can_pass_big_pipe,
            LocationName.special_zone_7_powerup_block_2:
                self.forest_of_illusion_3_can_pass_big_pipe,
            LocationName.special_zone_7_coin_block_2:
                self.forest_of_illusion_3_can_pass_big_pipe,

            LocationName.special_zone_8_dragon:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_yoshi_block_1:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.special_zone_8_coin_block_1:
                self.true,
            LocationName.special_zone_8_coin_block_2:
                self.true,
            LocationName.special_zone_8_coin_block_3:
                self.true,
            LocationName.special_zone_8_coin_block_4:
                self.true,
            LocationName.special_zone_8_coin_block_5:
                self.true,
            LocationName.special_zone_8_blue_pow_block_1:
                self.true,
            LocationName.special_zone_8_powerup_block_1:
                self.true,
            LocationName.special_zone_8_star_block_1:
                self.true,
            LocationName.special_zone_8_coin_block_6:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_coin_block_7:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_coin_block_8:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_coin_block_9:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_coin_block_10:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_coin_block_11:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_coin_block_12:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_coin_block_13:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_coin_block_14:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_coin_block_15:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_coin_block_16:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_coin_block_17:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_coin_block_18:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_multi_coin_block_1:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_coin_block_19:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_coin_block_20:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_coin_block_21:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_coin_block_22:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_coin_block_23:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_powerup_block_2:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_flying_block_1:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
        }
