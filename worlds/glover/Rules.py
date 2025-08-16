from BaseClasses import CollectionState
#from worlds.generic.Rules import add_rule, set_rule, forbid_item, add_item_rule

#Basic rules
def rule_cartwheel(self, state : CollectionState) -> bool:
    return state.has("Cartwheel", self.player)
def rule_crawl(self, state : CollectionState) -> bool:
    return state.has("Crawl", self.player)
def rule_double_jump(self, state : CollectionState) -> bool:
    return state.has("Double Jump", self.player)
def rule_fist_slam(self, state : CollectionState) -> bool:
    return state.has("Fist Slam", self.player)
def rule_ledge(self, state : CollectionState) -> bool:
    return state.has("Ledge Grab", self.player)
def rule_push(self, state : CollectionState) -> bool:
    return state.has("Push", self.player)
def rule_locate_garib(self, state : CollectionState) -> bool:
    return state.has("Locate Garibs", self.player)
def rule_locate_ball(self, state : CollectionState) -> bool:
    return state.has("Locate Ball", self.player)
def rule_dribble(self, state : CollectionState) -> bool:
    return state.has("Dribble", self.player)
def rule_quick_swap(self, state : CollectionState) -> bool:
    return state.has("Quick Swap", self.player)
def rule_slap(self, state : CollectionState) -> bool:
    return state.has("Slap", self.player)
def rule_throw(self, state : CollectionState) -> bool:
    return state.has("Throw", self.player)
def rule_lob_ball(self, state : CollectionState) -> bool:
    return state.has("Ball Toss", self.player)
def rule_rubber_ball(self, state : CollectionState) -> bool:
    return state.has("Rubber Ball", self.player)
def rule_bowling_ball(self, state : CollectionState) -> bool:
    return state.has("Bowling Ball", self.player)
def rule_ball_bearing(self, state : CollectionState) -> bool:
    return state.has("Ball Bearing", self.player)
def rule_crystal(self, state : CollectionState) -> bool:
    return state.has("Crystal", self.player)
def rule_beachball(self, state : CollectionState) -> bool:
    return state.has("Beachball", self.player)
def rule_death_potion(self, state : CollectionState) -> bool:
    return state.has("Death Potion", self.player)
def rule_helicopter_potion(self, state : CollectionState) -> bool:
    return state.has("Helicopter Potion", self.player)
def rule_frog_potion(self, state : CollectionState) -> bool:
    return state.has("Frog Potion", self.player)
def rule_boomerang_ball(self, state : CollectionState) -> bool:
    return state.has("Boomerang Ball", self.player)
def rule_speed_potion(self, state : CollectionState) -> bool:
    return state.has("Speed Potion", self.player)
def rule_sticky_potion(self, state : CollectionState) -> bool:
    return state.has("Sticky Potion", self.player)
def rule_hercules_potion(self, state : CollectionState) -> bool:
    return state.has("Hercules Potion", self.player)
def rule_jump(self, state : CollectionState) -> bool:
    return state.has("Jump", self.player)
def rule_grab(self, state : CollectionState) -> bool:
    return state.has("Grab", self.player)
def rule_power_ball(self, state : CollectionState) -> bool:
    return state.has("Power Ball", self.player)

#Special rules
def rule_not_crystal(self, state : CollectionState) -> bool:
    return state.has_group("Not Crystal", self.player)
def rule_not_bowling(self, state : CollectionState) -> bool:
    return state.has_group("Not Bowling", self.player)
def rule_not_bowling_or_crystal(self, state : CollectionState) -> bool:
    return state.has_group("Not Bowling or Crystal", self.player)
def rule_sinks(self, state : CollectionState) -> bool:
    return state.has_group("Sinks", self.player)
def rule_floats(self, state : CollectionState) -> bool:
    return state.has_group("Floats", self.player)
def rule_ball_up(self, state : CollectionState) -> bool:
    return state.has_group("Ball Up", self.player)

#
def rule_event_atlh_1_star(self, state : CollectionState) -> bool:
	return state.has("AtlH 1 Star", self.player)
def rule_event_atlh_2_gate(self, state : CollectionState) -> bool:
	return state.has("AtlH 2 Gate", self.player)
def rule_event_atlh_2_star(self, state : CollectionState) -> bool:
	return state.has("AtlH 2 Star", self.player)
def rule_event_atlh_3_gate(self, state : CollectionState) -> bool:
	return state.has("AtlH 3 Gate", self.player)
def rule_event_atlh_3_star(self, state : CollectionState) -> bool:
	return state.has("AtlH 3 Star", self.player)
def rule_event_atlh_boss_gate(self, state : CollectionState) -> bool:
	return state.has("AtlH Boss Gate", self.player)
def rule_event_atlh_boss_star(self, state : CollectionState) -> bool:
	return state.has("AtlH Boss Star", self.player)
def rule_event_atlh_bonus_gate(self, state : CollectionState) -> bool:
	return state.has("AtlH Bonus Gate", self.player)
def rule_event_atlh_bonus_star(self, state : CollectionState) -> bool:
	return state.has("AtlH Bonus Star", self.player)
def rule_event_atl1_gate(self, state : CollectionState) -> bool:
	return state.has("Atl1 Gate", self.player)
def rule_event_atl2_elevator(self, state : CollectionState) -> bool:
	return state.has("Atl2 Elevator", self.player)
def rule_event_atl2_ballswitch_drain(self, state : CollectionState) -> bool:
	return state.has("Atl2 Ballswitch Drain", self.player)
def rule_event_atl2_gate(self, state : CollectionState) -> bool:
	return state.has("Atl2 Gate", self.player)
def rule_event_atl3_waterwheel(self, state : CollectionState) -> bool:
	return state.has("Atl3 Waterwheel", self.player)
def rule_event_atl3_cave_platforms(self, state : CollectionState) -> bool:
	return state.has("Atl3 Cave Platforms", self.player)
def rule_event_crnh_1_star(self, state : CollectionState) -> bool:
	return state.has("CrnH 1 Star", self.player)
def rule_event_crnh_2_gate(self, state : CollectionState) -> bool:
	return state.has("CrnH 2 Gate", self.player)
def rule_event_crnh_2_star(self, state : CollectionState) -> bool:
	return state.has("CrnH 2 Star", self.player)
def rule_event_crnh_3_gate(self, state : CollectionState) -> bool:
	return state.has("CrnH 3 Gate", self.player)
def rule_event_crnh_3_star(self, state : CollectionState) -> bool:
	return state.has("CrnH 3 Star", self.player)
def rule_event_crnh_boss_gate(self, state : CollectionState) -> bool:
	return state.has("CrnH Boss Gate", self.player)
def rule_event_crnh_boss_star(self, state : CollectionState) -> bool:
	return state.has("CrnH Boss Star", self.player)
def rule_event_crnh_bonus_gate(self, state : CollectionState) -> bool:
	return state.has("CrnH Bonus Gate", self.player)
def rule_event_crnh_bonus_star(self, state : CollectionState) -> bool:
	return state.has("CrnH Bonus Star", self.player)
def rule_event_crn1_elevator(self, state : CollectionState) -> bool:
	return state.has("Crn1 Elevator", self.player)
def rule_event_crn1_gate(self, state : CollectionState) -> bool:
	return state.has("Crn1 Gate", self.player)
def rule_event_crn1_door_a(self, state : CollectionState) -> bool:
	return state.has("Crn1 Door A", self.player)
def rule_event_crn1_door_b(self, state : CollectionState) -> bool:
	return state.has("Crn1 Door B", self.player)
def rule_event_crn1_door_c(self, state : CollectionState) -> bool:
	return state.has("Crn1 Door C", self.player)
def rule_event_crn1_rocket_1(self, state : CollectionState) -> bool:
	return state.has("Crn1 Rocket 1", self.player)
def rule_event_crn1_rocket_2(self, state : CollectionState) -> bool:
	return state.has("Crn1 Rocket 2", self.player)
def rule_event_crn1_rocket_3(self, state : CollectionState) -> bool:
	return state.has("Crn1 Rocket 3", self.player)
def rule_event_crn2_drop_garibs(self, state : CollectionState) -> bool:
	return state.has("Crn2 Drop Garibs", self.player)
def rule_event_crn2_fan(self, state : CollectionState) -> bool:
	return state.has("Crn2 Fan", self.player)
def rule_event_crn3_spin_door(self, state : CollectionState) -> bool:
	return state.has("Crn3 Spin Door", self.player)
def rule_event_crn3_hands(self, state : CollectionState) -> bool:
	return state.has("Crn3 Hands", self.player)
def rule_event_prth_1_star(self, state : CollectionState) -> bool:
	return state.has("PrtH 1 Star", self.player)
def rule_event_prth_2_gate(self, state : CollectionState) -> bool:
	return state.has("PrtH 2 Gate", self.player)
def rule_event_prth_2_star(self, state : CollectionState) -> bool:
	return state.has("PrtH 2 Star", self.player)
def rule_event_prth_3_gate(self, state : CollectionState) -> bool:
	return state.has("PrtH 3 Gate", self.player)
def rule_event_prth_3_star(self, state : CollectionState) -> bool:
	return state.has("PrtH 3 Star", self.player)
def rule_event_prth_boss_gate(self, state : CollectionState) -> bool:
	return state.has("PrtH Boss Gate", self.player)
def rule_event_prth_boss_star(self, state : CollectionState) -> bool:
	return state.has("PrtH Boss Star", self.player)
def rule_event_prth_bonus_gate(self, state : CollectionState) -> bool:
	return state.has("PrtH Bonus Gate", self.player)
def rule_event_prth_bonus_star(self, state : CollectionState) -> bool:
	return state.has("PrtH Bonus Star", self.player)
def rule_event_prt1_raise_beach(self, state : CollectionState) -> bool:
	return state.has("Prt1 Raise Beach", self.player)
def rule_event_prt1_elevator(self, state : CollectionState) -> bool:
	return state.has("Prt1 Elevator", self.player)
def rule_event_prt1_chest(self, state : CollectionState) -> bool:
	return state.has("Prt1 Chest", self.player)
def rule_event_prt1_sandpile(self, state : CollectionState) -> bool:
	return state.has("Prt1 Sandpile", self.player)
def rule_event_prt1_waterspout(self, state : CollectionState) -> bool:
	return state.has("Prt1 Waterspout", self.player)
def rule_event_prt1_lighthouse(self, state : CollectionState) -> bool:
	return state.has("Prt1 Lighthouse", self.player)
def rule_event_prt1_raise_ship(self, state : CollectionState) -> bool:
	return state.has("Prt1 Raise Ship", self.player)
def rule_event_prt1_bridge(self, state : CollectionState) -> bool:
	return state.has("Prt1 Bridge", self.player)
def rule_event_prt2_lower_water(self, state : CollectionState) -> bool:
	return state.has("Prt2 Lower Water", self.player)
def rule_event_prt2_ramp(self, state : CollectionState) -> bool:
	return state.has("Prt2 Ramp", self.player)
def rule_event_prt2_gate(self, state : CollectionState) -> bool:
	return state.has("Prt2 Gate", self.player)
def rule_event_prt3_platform_spin(self, state : CollectionState) -> bool:
	return state.has("Prt3 Platform Spin", self.player)
def rule_event_prt3_trampoline(self, state : CollectionState) -> bool:
	return state.has("Prt3 Trampoline", self.player)
def rule_event_prt3_stairs(self, state : CollectionState) -> bool:
	return state.has("Prt3 Stairs", self.player)
def rule_event_prt3_elevator(self, state : CollectionState) -> bool:
	return state.has("Prt3 Elevator", self.player)
def rule_event_phth_1_star(self, state : CollectionState) -> bool:
	return state.has("PhtH 1 Star", self.player)
def rule_event_phth_2_gate(self, state : CollectionState) -> bool:
	return state.has("PhtH 2 Gate", self.player)
def rule_event_phth_2_star(self, state : CollectionState) -> bool:
	return state.has("PhtH 2 Star", self.player)
def rule_event_phth_3_gate(self, state : CollectionState) -> bool:
	return state.has("PhtH 3 Gate", self.player)
def rule_event_phth_3_star(self, state : CollectionState) -> bool:
	return state.has("PhtH 3 Star", self.player)
def rule_event_phth_boss_gate(self, state : CollectionState) -> bool:
	return state.has("PhtH Boss Gate", self.player)
def rule_event_phth_boss_star(self, state : CollectionState) -> bool:
	return state.has("PhtH Boss Star", self.player)
def rule_event_phth_bonus_gate(self, state : CollectionState) -> bool:
	return state.has("PhtH Bonus Gate", self.player)
def rule_event_phth_bonus_star(self, state : CollectionState) -> bool:
	return state.has("PhtH Bonus Star", self.player)
def rule_event_pht1_life_drop(self, state : CollectionState) -> bool:
	return state.has("Pht1 Life Drop", self.player)
def rule_event_pht2_platform_1(self, state : CollectionState) -> bool:
	return state.has("Pht2 Platform 1", self.player)
def rule_event_pht2_platform_2(self, state : CollectionState) -> bool:
	return state.has("Pht2 Platform 2", self.player)
def rule_event_pht2_lower_ball_switch(self, state : CollectionState) -> bool:
	return state.has("Pht2 Lower Ball Switch", self.player)
def rule_event_pht3_drop_garibs(self, state : CollectionState) -> bool:
	return state.has("Pht3 Drop Garibs", self.player)
def rule_event_pht3_spin_stones(self, state : CollectionState) -> bool:
	return state.has("Pht3 Spin Stones", self.player)
def rule_event_pht3_progressive_lower_monolith_1(self, state : CollectionState) -> bool:
	return state.has("Pht3 Progressive Lower Monolith 1", self.player)
def rule_event_pht3_progressive_lower_monolith_2(self, state : CollectionState) -> bool:
	return state.has("Pht3 Progressive Lower Monolith 2", self.player)
def rule_event_pht3_progressive_lower_monolith_3(self, state : CollectionState) -> bool:
	return state.has("Pht3 Progressive Lower Monolith 3", self.player)
def rule_event_pht3_progressive_lower_monolith_4(self, state : CollectionState) -> bool:
	return state.has("Pht3 Progressive Lower Monolith 4", self.player)
def rule_event_pht3_floating_platforms(self, state : CollectionState) -> bool:
	return state.has("Pht3 Floating Platforms", self.player)
def rule_event_pht3_lava_spinning(self, state : CollectionState) -> bool:
	return state.has("Pht3 Lava Spinning", self.player)
def rule_event_pht3_dirt_elevator(self, state : CollectionState) -> bool:
	return state.has("Pht3 Dirt Elevator", self.player)
def rule_event_fofh_1_star(self, state : CollectionState) -> bool:
	return state.has("FoFH 1 Star", self.player)
def rule_event_fofh_2_gate(self, state : CollectionState) -> bool:
	return state.has("FoFH 2 Gate", self.player)
def rule_event_fofh_2_star(self, state : CollectionState) -> bool:
	return state.has("FoFH 2 Star", self.player)
def rule_event_fofh_3_gate(self, state : CollectionState) -> bool:
	return state.has("FoFH 3 Gate", self.player)
def rule_event_fofh_3_star(self, state : CollectionState) -> bool:
	return state.has("FoFH 3 Star", self.player)
def rule_event_fofh_boss_gate(self, state : CollectionState) -> bool:
	return state.has("FoFH Boss Gate", self.player)
def rule_event_fofh_boss_star(self, state : CollectionState) -> bool:
	return state.has("FoFH Boss Star", self.player)
def rule_event_fofh_bonus_gate(self, state : CollectionState) -> bool:
	return state.has("FoFH Bonus Gate", self.player)
def rule_event_fofh_bonus_star(self, state : CollectionState) -> bool:
	return state.has("FoFH Bonus Star", self.player)
def rule_event_fof1_coffin(self, state : CollectionState) -> bool:
	return state.has("FoF1 Coffin", self.player)
def rule_event_fof1_doorway(self, state : CollectionState) -> bool:
	return state.has("FoF1 Doorway", self.player)
def rule_event_fof1_drawbridge(self, state : CollectionState) -> bool:
	return state.has("FoF1 Drawbridge", self.player)
def rule_event_fof2_garibs_fall(self, state : CollectionState) -> bool:
	return state.has("FoF2 Garibs Fall", self.player)
def rule_event_fof2_checkpoint_gates(self, state : CollectionState) -> bool:
	return state.has("FoF2 Checkpoint Gates", self.player)
def rule_event_fof2_mummy_gate(self, state : CollectionState) -> bool:
	return state.has("FoF2 Mummy Gate", self.player)
def rule_event_fof3_gate(self, state : CollectionState) -> bool:
	return state.has("FoF3 Gate", self.player)
def rule_event_fof3_spikes(self, state : CollectionState) -> bool:
	return state.has("FoF3 Spikes", self.player)
def rule_event_otwh_1_star(self, state : CollectionState) -> bool:
	return state.has("OtwH 1 Star", self.player)
def rule_event_otwh_2_gate(self, state : CollectionState) -> bool:
	return state.has("OtwH 2 Gate", self.player)
def rule_event_otwh_2_star(self, state : CollectionState) -> bool:
	return state.has("OtwH 2 Star", self.player)
def rule_event_otwh_3_gate(self, state : CollectionState) -> bool:
	return state.has("OtwH 3 Gate", self.player)
def rule_event_otwh_3_star(self, state : CollectionState) -> bool:
	return state.has("OtwH 3 Star", self.player)
def rule_event_otwh_boss_gate(self, state : CollectionState) -> bool:
	return state.has("OtwH Boss Gate", self.player)
def rule_event_otwh_boss_star(self, state : CollectionState) -> bool:
	return state.has("OtwH Boss Star", self.player)
def rule_event_otwh_bonus_gate(self, state : CollectionState) -> bool:
	return state.has("OtwH Bonus Gate", self.player)
def rule_event_otwh_bonus_star(self, state : CollectionState) -> bool:
	return state.has("OtwH Bonus Star", self.player)
def rule_event_otw1_aliens(self, state : CollectionState) -> bool:
	return state.has("Otw1 Aliens", self.player)
def rule_event_otw1_fans(self, state : CollectionState) -> bool:
	return state.has("Otw1 Fans", self.player)
def rule_event_otw1_flying_platforms(self, state : CollectionState) -> bool:
	return state.has("Otw1 Flying Platforms", self.player)
def rule_event_otw1_goo_platforms(self, state : CollectionState) -> bool:
	return state.has("Otw1 Goo Platforms", self.player)
def rule_event_otw1_ufo(self, state : CollectionState) -> bool:
	return state.has("Otw1 UFO", self.player)
def rule_event_otw1_missile(self, state : CollectionState) -> bool:
	return state.has("Otw1 Missile", self.player)
def rule_event_otw2_mashers(self, state : CollectionState) -> bool:
	return state.has("Otw2 Mashers", self.player)
def rule_event_otw2_ramp(self, state : CollectionState) -> bool:
	return state.has("Otw2 Ramp", self.player)
def rule_event_otw3_hazard_gate(self, state : CollectionState) -> bool:
	return state.has("Otw3 Hazard Gate", self.player)
def rule_event_otw3_sign(self, state : CollectionState) -> bool:
	return state.has("Otw3 Sign", self.player)
def rule_event_otw3_fan(self, state : CollectionState) -> bool:
	return state.has("Otw3 Fan", self.player)
def rule_event_otw3_bridge(self, state : CollectionState) -> bool:
	return state.has("Otw3 Bridge", self.player)
def rule_event_otw3_glass_gate(self, state : CollectionState) -> bool:
	return state.has("Otw3 Glass Gate", self.player)
def rule_event_hubworld_atlantis_gate(self, state : CollectionState) -> bool:
	return state.has("Hubworld Atlantis Gate", self.player)
def rule_event_hubworld_carnival_gate(self, state : CollectionState) -> bool:
	return state.has("Hubworld Carnival Gate", self.player)
def rule_event_hubworld_pirates_cove_gate(self, state : CollectionState) -> bool:
	return state.has("Hubworld Pirate's Cove Gate", self.player)
def rule_event_hubworld_prehistoric_gate(self, state : CollectionState) -> bool:
	return state.has("Hubworld Prehistoric Gate", self.player)
def rule_event_hubworld_fortress_of_fear_gate(self, state : CollectionState) -> bool:
	return state.has("Hubworld Fortress of Fear Gate", self.player)
def rule_event_hubworld_out_of_this_world_gate(self, state : CollectionState) -> bool:
	return state.has("Hubworld Out of This World Gate", self.player)
def rule_event_training_sandpit(self, state : CollectionState) -> bool:
	return state.has("Training Sandpit", self.player)
def rule_event_training_lower_target(self, state : CollectionState) -> bool:
	return state.has("Training Lower Target", self.player)
def rule_event_training_stairs(self, state : CollectionState) -> bool:
	return state.has("Training Stairs", self.player)

event_lookup = {
	"AtlH 1 Star" : 						rule_event_atlh_1_star,
	"AtlH 2 Gate" : 						rule_event_atlh_2_gate,
	"AtlH 2 Star" : 						rule_event_atlh_2_star,
	"AtlH 3 Gate" : 						rule_event_atlh_3_gate,
	"AtlH 3 Star" : 						rule_event_atlh_3_star,
	"AtlH Boss Gate" : 						rule_event_atlh_boss_gate,
	"AtlH Boss Star" : 						rule_event_atlh_boss_star,
	"AtlH Bonus Gate" : 					rule_event_atlh_bonus_gate,
	"AtlH Bonus Star" : 					rule_event_atlh_bonus_star,
	"Atl1 Gate" : 						    rule_event_atl1_gate,
	"Atl2 Elevator" : 						rule_event_atl2_elevator,
	"Atl2 Ballswitch Drain" : 				rule_event_atl2_ballswitch_drain,
	"Atl2 Gate" : 						    rule_event_atl2_gate,
	"Atl3 Waterwheel" : 					rule_event_atl3_waterwheel,
	"Atl3 Cave Platforms" : 				rule_event_atl3_cave_platforms,
	"CrnH 1 Star" : 						rule_event_crnh_1_star,
	"CrnH 2 Gate" : 						rule_event_crnh_2_gate,
	"CrnH 2 Star" : 						rule_event_crnh_2_star,
	"CrnH 3 Gate" : 						rule_event_crnh_3_gate,
	"CrnH 3 Star" : 						rule_event_crnh_3_star,
	"CrnH Boss Gate" : 						rule_event_crnh_boss_gate,
	"CrnH Boss Star" : 						rule_event_crnh_boss_star,
	"CrnH Bonus Gate" : 					rule_event_crnh_bonus_gate,
	"CrnH Bonus Star" : 					rule_event_crnh_bonus_star,
	"Crn1 Elevator" : 						rule_event_crn1_elevator,
	"Crn1 Gate" : 						    rule_event_crn1_gate,
	"Crn1 Door A" : 						rule_event_crn1_door_a,
	"Crn1 Door B" : 						rule_event_crn1_door_b,
	"Crn1 Door C" : 						rule_event_crn1_door_c,
	"Crn1 Rocket 1" : 						rule_event_crn1_rocket_1,
	"Crn1 Rocket 2" : 						rule_event_crn1_rocket_2,
	"Crn1 Rocket 3" : 						rule_event_crn1_rocket_3,
	"Crn2 Drop Garibs" : 					rule_event_crn2_drop_garibs,
	"Crn2 Fan" : 						    rule_event_crn2_fan,
	"Crn3 Spin Door" : 						rule_event_crn3_spin_door,
	"Crn3 Hands" : 						    rule_event_crn3_hands,
	"PrtH 1 Star" : 						rule_event_prth_1_star,
	"PrtH 2 Gate" : 						rule_event_prth_2_gate,
	"PrtH 2 Star" : 						rule_event_prth_2_star,
	"PrtH 3 Gate" : 						rule_event_prth_3_gate,
	"PrtH 3 Star" : 						rule_event_prth_3_star,
	"PrtH Boss Gate" : 						rule_event_prth_boss_gate,
	"PrtH Boss Star" : 						rule_event_prth_boss_star,
	"PrtH Bonus Gate" : 					rule_event_prth_bonus_gate,
	"PrtH Bonus Star" : 					rule_event_prth_bonus_star,
	"Prt1 Raise Beach" : 					rule_event_prt1_raise_beach,
	"Prt1 Elevator" : 						rule_event_prt1_elevator,
	"Prt1 Chest" : 						    rule_event_prt1_chest,
	"Prt1 Sandpile" : 						rule_event_prt1_sandpile,
	"Prt1 Waterspout" : 					rule_event_prt1_waterspout,
	"Prt1 Lighthouse" : 					rule_event_prt1_lighthouse,
	"Prt1 Raise Ship" : 					rule_event_prt1_raise_ship,
	"Prt1 Bridge" : 						rule_event_prt1_bridge,
	"Prt2 Lower Water" : 					rule_event_prt2_lower_water,
	"Prt2 Ramp" : 						    rule_event_prt2_ramp,
	"Prt2 Gate" : 						    rule_event_prt2_gate,
	"Prt3 Platform Spin" : 					rule_event_prt3_platform_spin,
	"Prt3 Trampoline" : 					rule_event_prt3_trampoline,
	"Prt3 Stairs" : 						rule_event_prt3_stairs,
	"Prt3 Elevator" : 						rule_event_prt3_elevator,
	"PhtH 1 Star" : 						rule_event_phth_1_star,
	"PhtH 2 Gate" : 						rule_event_phth_2_gate,
	"PhtH 2 Star" : 						rule_event_phth_2_star,
	"PhtH 3 Gate" : 						rule_event_phth_3_gate,
	"PhtH 3 Star" : 						rule_event_phth_3_star,
	"PhtH Boss Gate" : 						rule_event_phth_boss_gate,
	"PhtH Boss Star" : 						rule_event_phth_boss_star,
	"PhtH Bonus Gate" : 					rule_event_phth_bonus_gate,
	"PhtH Bonus Star" : 					rule_event_phth_bonus_star,
	"Pht1 Life Drop" : 						rule_event_pht1_life_drop,
	"Pht2 Platform 1" : 					rule_event_pht2_platform_1,
	"Pht2 Platform 2" : 					rule_event_pht2_platform_2,
	"Pht2 Lower Ball Switch" : 				rule_event_pht2_lower_ball_switch,
	"Pht3 Drop Garibs" : 					rule_event_pht3_drop_garibs,
	"Pht3 Spin Stones" : 					rule_event_pht3_spin_stones,
	"Pht3 Progressive Lower Monolith 1" : 	rule_event_pht3_progressive_lower_monolith_1,
	"Pht3 Progressive Lower Monolith 2" : 	rule_event_pht3_progressive_lower_monolith_2,
	"Pht3 Progressive Lower Monolith 3" : 	rule_event_pht3_progressive_lower_monolith_3,
	"Pht3 Progressive Lower Monolith 4" : 	rule_event_pht3_progressive_lower_monolith_4,
	"Pht3 Floating Platforms" : 		    rule_event_pht3_floating_platforms,
	"Pht3 Lava Spinning" : 				    rule_event_pht3_lava_spinning,
	"Pht3 Dirt Elevator" : 				    rule_event_pht3_dirt_elevator,
	"FoFH 1 Star" : 					    rule_event_fofh_1_star,
	"FoFH 2 Gate" : 					    rule_event_fofh_2_gate,
	"FoFH 2 Star" : 					    rule_event_fofh_2_star,
	"FoFH 3 Gate" : 					    rule_event_fofh_3_gate,
	"FoFH 3 Star" : 					    rule_event_fofh_3_star,
	"FoFH Boss Gate" : 					    rule_event_fofh_boss_gate,
	"FoFH Boss Star" : 					    rule_event_fofh_boss_star,
	"FoFH Bonus Gate" : 				    rule_event_fofh_bonus_gate,
	"FoFH Bonus Star" : 				    rule_event_fofh_bonus_star,
	"FoF1 Coffin" : 					    rule_event_fof1_coffin,
	"FoF1 Doorway" : 					    rule_event_fof1_doorway,
	"FoF1 Drawbridge" : 				    rule_event_fof1_drawbridge,
	"FoF2 Garibs Fall" : 				    rule_event_fof2_garibs_fall,
	"FoF2 Checkpoint Gates" : 			    rule_event_fof2_checkpoint_gates,
	"FoF2 Mummy Gate" : 				    rule_event_fof2_mummy_gate,
	"FoF3 Gate" : 						    rule_event_fof3_gate,
	"FoF3 Spikes" : 					    rule_event_fof3_spikes,
	"OtwH 1 Star" : 					    rule_event_otwh_1_star,
	"OtwH 2 Gate" : 					    rule_event_otwh_2_gate,
	"OtwH 2 Star" : 					    rule_event_otwh_2_star,
	"OtwH 3 Gate" : 					    rule_event_otwh_3_gate,
	"OtwH 3 Star" : 					    rule_event_otwh_3_star,
	"OtwH Boss Gate" : 					    rule_event_otwh_boss_gate,
	"OtwH Boss Star" : 					    rule_event_otwh_boss_star,
	"OtwH Bonus Gate" : 				    rule_event_otwh_bonus_gate,
	"OtwH Bonus Star" : 				    rule_event_otwh_bonus_star,
	"Otw1 Aliens" : 					    rule_event_otw1_aliens,
	"Otw1 Fans" : 						    rule_event_otw1_fans,
	"Otw1 Flying Platforms" : 			    rule_event_otw1_flying_platforms,
	"Otw1 Goo Platforms" : 				    rule_event_otw1_goo_platforms,
	"Otw1 UFO" : 						    rule_event_otw1_ufo,
	"Otw1 Missile" : 					    rule_event_otw1_missile,
	"Otw2 Mashers" : 					    rule_event_otw2_mashers,
	"Otw2 Ramp" : 						    rule_event_otw2_ramp,
	"Otw3 Hazard Gate" : 				    rule_event_otw3_hazard_gate,
	"Otw3 Sign" : 						    rule_event_otw3_sign,
	"Otw3 Fan" : 						    rule_event_otw3_fan,
	"Otw3 Bridge" : 					    rule_event_otw3_bridge,
	"Otw3 Glass Gate" : 				    rule_event_otw3_glass_gate,
	"Hubworld Atlantis Gate" : 			    rule_event_hubworld_atlantis_gate,
	"Hubworld Carnival Gate" : 			    rule_event_hubworld_carnival_gate,
	"Hubworld Pirate's Cove Gate" : 	    rule_event_hubworld_pirates_cove_gate,
	"Hubworld Prehistoric Gate" : 		    rule_event_hubworld_prehistoric_gate,
	"Hubworld Fortress of Fear Gate" : 	    rule_event_hubworld_fortress_of_fear_gate,
	"Hubworld Out of This World Gate" :     rule_event_hubworld_out_of_this_world_gate,
	"Training Sandpit" : 				    rule_event_training_sandpit,
	"Training Lower Target" : 			    rule_event_training_lower_target,
	"Training Stairs" : 				    rule_event_training_stairs,
}

move_lookup = {
    "Cartwheel" :               rule_cartwheel,
    "Crawl" :                   rule_crawl,
    "Double Jump" :             rule_double_jump,
    "Fist Slam" :               rule_fist_slam,
    "Ledge Grab" :              rule_ledge,
    "Push" :                    rule_push,
    "Locate Garib" :            rule_locate_garib,
    "Locate Ball" :             rule_locate_ball,
    "Dribble" :                 rule_dribble,
    "Quick Swap" :              rule_quick_swap,
    "Slap" :                    rule_slap,
    "Throw" :                   rule_throw,
    "Lob Ball" :                rule_lob_ball,
    "Rubber Ball" :             rule_rubber_ball,
    "Bowling Ball" :            rule_bowling_ball,
    "Ball Bearing" :            rule_ball_bearing,
    "Crystal" :                 rule_crystal,
    "Beachball" :               rule_beachball,
    "Death Potion" :            rule_death_potion,
    "Helicopter Potion" :       rule_helicopter_potion,
    "Frog Potion" :             rule_frog_potion,
    "Boomerang Ball" :          rule_boomerang_ball,
    "Speed Potion" :            rule_speed_potion,
    "Sticky Potion" :           rule_sticky_potion,
    "Hercules Potion" :         rule_hercules_potion,
    "Jump" :                    rule_jump,
    "Not Crystal" :             rule_not_crystal,
    "Not Bowling" :             rule_not_bowling,
    "Sinks" :                   rule_sinks,
    "Floats" :                  rule_floats,
    "Grab" :                    rule_grab,
    "Ball Up" :                 rule_ball_up,
    "Power Ball" :              rule_power_ball,
    "Not Bowling or Crystal" :  rule_not_bowling_or_crystal
}

   #"AtlH 1 Star" : 						
   #"AtlH 2 Gate" : 						
   #"AtlH 2 Star" : 						
   #"AtlH 3 Gate" : 						
   #"AtlH 3 Star" : 						
   #"AtlH Boss Gate" : 						
   #"AtlH Boss Star" : 						
   #"AtlH Bonus Gate" : 					
   #"AtlH Bonus Star" : 					

all_lookups = {
	**event_lookup,
	**move_lookup
}

switches_to_event_items = {
    #"AtlH: " : "AtlH 1 Star",
    #"AtlH: " : "AtlH 2 Gate",
    #"AtlH: " : "AtlH 2 Star",
    #"AtlH: " : "AtlH 3 Gate",
    #"AtlH: " : "AtlH 3 Star",
    #"AtlH: " : "AtlH Boss Gate",
    #"AtlH: " : "AtlH Boss Star",
    #"AtlH: " : "AtlH Bonus Gate",
    #"AtlH: " : "AtlH Bonus Star",
    "Atl1: Glover Switch" : "Atl1 Gate",
    "Atl2: Drain Block" : "Atl2 Elevator",
    "Atl2: Ball Switch" : "Atl2 Ballswitch Drain",
    "Atl2: Glover Switch" : "Atl2 Gate",
    #"Atl3: " : "Atl3 Waterwheel",
    #"Atl3: " : "Atl3 Cave Platforms",
    #"CrnH: " : "CrnH 1 Star",
    #"CrnH: " : "CrnH 2 Gate",
    #"CrnH: " : "CrnH 2 Star",
    #"CrnH: " : "CrnH 3 Gate",
    #"CrnH: " : "CrnH 3 Star",
    #"CrnH: " : "CrnH Boss Gate",
    #"CrnH: " : "CrnH Boss Star",
    #"CrnH: " : "CrnH Bonus Gate",
    #"CrnH: " : "CrnH Bonus Star",
    #"Crn1: " : "Crn1 Elevator",
    #"Crn1: " : "Crn1 Gate",
    #"Crn1: " : "Crn1 Door A",
    #"Crn1: " : "Crn1 Door B",
    #"Crn1: " : "Crn1 Door C",
    #"Crn1: " : "Crn1 Rocket 1",
    #"Crn1: " : "Crn1 Rocket 2",
    #"Crn1: " : "Crn1 Rocket 3",
    #"Crn2: " : "Crn2 Drop Garibs",
    #"Crn2: " : "Crn2 Fan",
    #"Crn3: " : "Crn3 Spin Door",
    #"Crn3: " : "Crn3 Hands",
    #"PrtH: " : "PrtH 1 Star",
    #"PrtH: " : "PrtH 2 Gate",
    #"PrtH: " : "PrtH 2 Star",
    #"PrtH: " : "PrtH 3 Gate",
    #"PrtH: " : "PrtH 3 Star",
    #"PrtH: " : "PrtH Boss Gate",
    #"PrtH: " : "PrtH Boss Star",
    #"PrtH: " : "PrtH Bonus Gate",
    #"PrtH: " : "PrtH Bonus Star",
    #"Prt1: " : "Prt1 Raise Beach",
    #"Prt1: " : "Prt1 Elevator",
    #"Prt1: " : "Prt1 Chest",
    #"Prt1: " : "Prt1 Sandpile",
    #"Prt1: " : "Prt1 Waterspout",
    #"Prt1: " : "Prt1 Lighthouse",
    #"Prt1: " : "Prt1 Raise Ship",
    #"Prt1: " : "Prt1 Bridge",
    #"Prt2: " : "Prt2 Lower Water",
    #"Prt2: " : "Prt2 Ramp",
    #"Prt2: " : "Prt2 Gate",
    #"Prt3: " : "Prt3 Platform Spin",
    #"Prt3: " : "Prt3 Trampoline",
    #"Prt3: " : "Prt3 Stairs",
    #"Prt3: " : "Prt3 Elevator",
    #"PhtH: " : "PhtH 1 Star",
    #"PhtH: " : "PhtH 2 Gate",
    #"PhtH: " : "PhtH 2 Star",
    #"PhtH: " : "PhtH 3 Gate",
    #"PhtH: " : "PhtH 3 Star",
    #"PhtH: " : "PhtH Boss Gate",
    #"PhtH: " : "PhtH Boss Star",
    #"PhtH: " : "PhtH Bonus Gate",
    #"PhtH: " : "PhtH Bonus Star",
    #"Pht1: " : "Pht1 Life Drop",
    #"Pht2: " : "Pht2 Platform 1",
    #"Pht2: " : "Pht2 Platform 2",
    #"Pht2: " : "Pht2 Lower Ball Switch",
    #"Pht3: " : "Pht3 Drop Garibs",
    #"Pht3: " : "Pht3 Spin Stones",
    #"Pht3: " : "Pht3 Progressive Lower Monolith 1",
    #"Pht3: " : "Pht3 Progressive Lower Monolith 2",
    #"Pht3: " : "Pht3 Progressive Lower Monolith 3",
    #"Pht3: " : "Pht3 Progressive Lower Monolith 4",
    #"Pht3: " : "Pht3 Floating Platforms",
    #"Pht3: " : "Pht3 Lava Spinning",
    #"Pht3: " : "Pht3 Dirt Elevator",
    #"FoFH: " : "FoFH 1 Star",
    #"FoFH: " : "FoFH 2 Gate",
    #"FoFH: " : "FoFH 2 Star",
    #"FoFH: " : "FoFH 3 Gate",
    #"FoFH: " : "FoFH 3 Star",
    #"FoFH: " : "FoFH Boss Gate",
    #"FoFH: " : "FoFH Boss Star",
    #"FoFH: " : "FoFH Bonus Gate",
    #"FoFH: " : "FoFH Bonus Star",
    #"FoF1: " : "FoF1 Coffin",
    #"FoF1: " : "FoF1 Doorway",
    #"FoF1: " : "FoF1 Drawbridge",
    #"FoF2: " : "FoF2 Garibs Fall",
    #"FoF2: " : "FoF2 Checkpoint Gates",
    #"FoF2: " : "FoF2 Mummy Gate",
    #"FoF3: " : "FoF3 Gate",
    #"FoF3: " : "FoF3 Spikes",
    #"OtwH: " : "OtwH 1 Star",
    #"OtwH: " : "OtwH 2 Gate",
    #"OtwH: " : "OtwH 2 Star",
    #"OtwH: " : "OtwH 3 Gate",
    #"OtwH: " : "OtwH 3 Star",
    #"OtwH: " : "OtwH Boss Gate",
    #"OtwH: " : "OtwH Boss Star",
    #"OtwH: " : "OtwH Bonus Gate",
    #"OtwH: " : "OtwH Bonus Star",
    #"Otw1: " : "Otw1 Aliens",
    #"Otw1: " : "Otw1 Fans",
    #"Otw1: " : "Otw1 Flying Platforms",
    #"Otw1: " : "Otw1 Goo Platforms",
    #"Otw1: " : "Otw1 UFO",
    #"Otw1: " : "Otw1 Missile",
    #"Otw2: " : "Otw2 Mashers",
    #"Otw2: " : "Otw2 Ramp",
    #"Otw3: " : "Otw3 Hazard Gate",
    #"Otw3: " : "Otw3 Sign",
    #"Otw3: " : "Otw3 Fan",
    #"Otw3: " : "Otw3 Bridge",
    #"Otw3: " : "Otw3 Glass Gate",
    #"" : "Hubworld Atlantis Gate",
    #"" : "Hubworld Carnival Gate",
    #"" : "Hubworld Pirate's Cove Gate" ,
    #"" : "Hubworld Prehistoric Gate",
    #"" : "Hubworld Fortress of Fear Gate" ,
    #"" : "Hubworld Out of This World Gate",
    #"" : "Training Sandpit",
    #"" : "Training Lower Target",
    #"" : "Training Stairs"
}