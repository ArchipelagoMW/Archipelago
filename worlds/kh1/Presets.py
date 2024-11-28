from typing import Any, Dict

from .Options import *

kh1_option_presets: Dict[str, Dict[str, Any]] = {
    # Standard playthrough where your goal is to defeat Ansem, reaching him by acquiring enough reports.
    "Final Ansem": {
        "goal": Goal.option_final_ansem,
        "end_of_the_world_unlock": EndoftheWorldUnlock.option_reports,
        "final_rest_door": FinalRestDoor.option_reports,
        "required_reports_eotw": 7,
        "required_reports_door": 10,
        "reports_in_pool": 13,
        
        "super_bosses": False,
        "atlantica": False,
        "hundred_acre_wood": False,
        "cups": False,
        "vanilla_emblem_pieces": True,
        
        "exp_multiplier": 48,
        "level_checks": 100,
        "force_stats_on_levels": 1,
        "strength_increase": 24,
        "defense_increase": 24,
        "hp_increase": 23,
        "ap_increase": 18,
        "mp_increase": 7,
        "accessory_slot_increase": 1,
        "item_slot_increase": 3,
        
        "keyblades_unlock_chests": False,
        "randomize_keyblade_stats": True,
        "bad_starting_weapons": False,
        "keyblade_max_str": 14,
        "keyblade_min_str": 3,
        "keyblade_max_mp": 3,
        "keyblade_min_mp": -2,
        
        "puppies": Puppies.option_triplets,
        "starting_worlds": 0,
        "interact_in_battle": False,
        "advanced_logic": False,
        "extra_shared_abilities": False,
        "exp_zero_in_pool": False,
        "donald_death_link": False,
        "goofy_death_link": False
    },
    # Puppies are found individually, and the goal is to return them all.
    "Puppy Hunt": {
        "goal": Goal.option_puppies,
        "end_of_the_world_unlock": EndoftheWorldUnlock.option_item,
        "final_rest_door": FinalRestDoor.option_puppies,
        "required_reports_eotw": 13,
        "required_reports_door": 13,
        "reports_in_pool": 13,
        
        "super_bosses": False,
        "atlantica": False,
        "hundred_acre_wood": False,
        "cups": False,
        "vanilla_emblem_pieces": True,
        
        "exp_multiplier": 48,
        "level_checks": 100,
        "force_stats_on_levels": 1,
        "strength_increase": 24,
        "defense_increase": 24,
        "hp_increase": 23,
        "ap_increase": 18,
        "mp_increase": 7,
        "accessory_slot_increase": 1,
        "item_slot_increase": 3,
        
        "keyblades_unlock_chests": False,
        "randomize_keyblade_stats": True,
        "bad_starting_weapons": False,
        "keyblade_max_str": 14,
        "keyblade_min_str": 3,
        "keyblade_max_mp": 3,
        "keyblade_min_mp": -2,
        
        "puppies": Puppies.option_individual,
        "starting_worlds": 0,
        "interact_in_battle": False,
        "advanced_logic": False,
        "extra_shared_abilities": False,
        "exp_zero_in_pool": False,
        "donald_death_link": False,
        "goofy_death_link": False
    },
    # Advanced playthrough with most settings on.
    "Advanced": {
        "goal": Goal.option_final_ansem,
        "end_of_the_world_unlock": EndoftheWorldUnlock.option_reports,
        "final_rest_door": FinalRestDoor.option_reports,
        "required_reports_eotw": 7,
        "required_reports_door": 10,
        "reports_in_pool": 13,
        
        "super_bosses": True,
        "atlantica": True,
        "hundred_acre_wood": True,
        "cups": True,
        "vanilla_emblem_pieces": False,
        
        "exp_multiplier": 48,
        "level_checks": 100,
        "force_stats_on_levels": 1,
        "strength_increase": 24,
        "defense_increase": 24,
        "hp_increase": 23,
        "ap_increase": 18,
        "mp_increase": 7,
        "accessory_slot_increase": 1,
        "item_slot_increase": 3,
        
        "keyblades_unlock_chests": True,
        "randomize_keyblade_stats": True,
        "bad_starting_weapons": True,
        "keyblade_max_str": 14,
        "keyblade_min_str": 3,
        "keyblade_max_mp": 3,
        "keyblade_min_mp": -2,
        
        "puppies": Puppies.option_triplets,
        "starting_worlds": 0,
        "interact_in_battle": True,
        "advanced_logic": True,
        "extra_shared_abilities": True,
        "exp_zero_in_pool": True,
        "donald_death_link": False,
        "goofy_death_link": False
    },
    # Playthrough meant to enhance the level 1 experience.
    "Level 1": {
        "goal": Goal.option_final_ansem,
        "end_of_the_world_unlock": EndoftheWorldUnlock.option_reports,
        "final_rest_door": FinalRestDoor.option_reports,
        "required_reports_eotw": 7,
        "required_reports_door": 10,
        "reports_in_pool": 13,
        
        "super_bosses": False,
        "atlantica": False,
        "hundred_acre_wood": False,
        "cups": False,
        "vanilla_emblem_pieces": True,
        
        "exp_multiplier": 16,
        "level_checks": 0,
        "force_stats_on_levels": 101,
        "strength_increase": 0,
        "defense_increase": 0,
        "hp_increase": 0,
        "mp_increase": 0,
        "accessory_slot_increase": 6,
        "item_slot_increase": 5,
        
        "keyblades_unlock_chests": False,
        "randomize_keyblade_stats": True,
        "bad_starting_weapons": False,
        "keyblade_max_str": 14,
        "keyblade_min_str": 3,
        "keyblade_max_mp": 3,
        "keyblade_min_mp": -2,
        
        "puppies": Puppies.option_triplets,
        "starting_worlds": 0,
        "interact_in_battle": False,
        "advanced_logic": False,
        "extra_shared_abilities": False,
        "exp_zero_in_pool": False,
        "donald_death_link": False,
        "goofy_death_link": False
    }
}
